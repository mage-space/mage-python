from __future__ import annotations

import time
import uuid
from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, cast

import httpx

from ._base import (
    DEFAULT_MAX_POLL_INTERVAL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_TIMEOUT,
    Retry,
    UploadData,
    api_error,
    api_headers,
    check_upload_size,
    is_final,
    list_params,
    next_poll_interval,
    poll_delay,
    read_upload,
    resolve_api_key,
    resolve_base_url,
    retry_delay,
    segment,
    should_retry,
    timeout_message,
    upload_error,
    without_none,
)
from ._errors import MageAPIError, MageConnectionError, MageGenerationError, MageTimeoutError
from ._generated import (
    Account,
    ArchitectureId,
    ArchitectureList,
    Character,
    CharacterList,
    GenerationRequest,
    Reference,
    ReferenceList,
    UploadTicket,
)

__all__ = ["Mage"]

# Indirections so tests can control time.
_sleep = time.sleep
_clock = time.monotonic

OnUpdate = Callable[[GenerationRequest], object]


class Mage:
    """A client for the Mage API.

    ```python
    from mage_space import Mage

    mage = Mage()  # reads MAGE_API_KEY
    request = mage.run("mango", {"prompt": "A lighthouse at dawn"})
    print(request["result"]["url"])
    ```
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
    ) -> None:
        """
        Args:
            api_key: Defaults to the MAGE_API_KEY environment variable.
            base_url: Defaults to MAGE_BASE_URL, else https://api.mage.space.
            timeout: Seconds allowed for each HTTP attempt.
            max_retries: Retries after a failed attempt that is safe to repeat.
            http_client: An httpx.Client to send requests with. The SDK closes only
                the client it creates itself.
        """
        self.api_key = resolve_api_key(api_key)
        self.base_url = resolve_base_url(base_url)
        self.timeout = timeout
        self.max_retries = max_retries
        self._owns_http_client = http_client is None
        self._http = http_client or httpx.Client()
        self.requests = Requests(self)
        self.uploads = Uploads(self)
        self.characters = Characters(self)
        self.references = References(self)
        self.account = AccountResource(self)
        self.architectures = Architectures(self)

    def generate(
        self,
        architecture: ArchitectureId | str,
        config: Mapping[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> GenerationRequest:
        """Submit a generation and return the request right away.

        Args:
            architecture: The model's architecture id, as in its endpoint path (`mango`,
                `cherry`, `seed_audio`, ...). Ids newer than this SDK work too.
            config: The request body. Annotate it with the model's TypedDict from
                `mage_space.types` (for example `MangoConfig`) to have it type-checked.
            idempotency_key: Identifies this submission so a retry is never charged twice.
                Defaults to a fresh UUID, reused by the SDK's own retries.
        """
        key = idempotency_key or str(uuid.uuid4())
        return cast(
            GenerationRequest,
            self._request(
                "POST",
                f"/v1/{segment(architecture)}/generate",
                retry=Retry.GENERATE,
                json=dict(config),
                headers={"Idempotency-Key": key},
            ),
        )

    def run(
        self,
        architecture: ArchitectureId | str,
        config: Mapping[str, Any],
        *,
        idempotency_key: str | None = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        max_poll_interval: float = DEFAULT_MAX_POLL_INTERVAL,
        timeout: float | None = None,
        on_update: OnUpdate | None = None,
    ) -> GenerationRequest:
        """Submit a generation and wait for it to complete.

        Returns the completed request; its `result` holds the output URL.

        Raises:
            MageGenerationError: The request failed or was cancelled.
            MageTimeoutError: `timeout` seconds passed first. The request keeps running.
        """
        submitted = self.generate(architecture, config, idempotency_key=idempotency_key)
        final = self.requests.wait(
            submitted,
            poll_interval=poll_interval,
            max_poll_interval=max_poll_interval,
            timeout=timeout,
            on_update=on_update,
        )
        if final["status"] != "completed":
            raise MageGenerationError(final)
        return final

    def close(self) -> None:
        if self._owns_http_client:
            self._http.close()

    def __enter__(self) -> Mage:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        retry: Retry,
        json: Any = None,
        params: Mapping[str, str | int] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        request_headers = api_headers(self.api_key, json_body=json is not None)
        request_headers.update(headers or {})
        response = self._send(
            method,
            self.base_url + path,
            retry=retry,
            to_error=api_error,
            headers=request_headers,
            json=json,
            params=params,
        )
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def _send(
        self,
        method: str,
        url: str,
        *,
        retry: Retry,
        to_error: Callable[[httpx.Response], MageAPIError],
        headers: Mapping[str, str],
        json: Any = None,
        params: Mapping[str, str | int] | None = None,
        content: bytes | None = None,
    ) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = self._http.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                    params=params,
                    content=content,
                    timeout=self.timeout,
                )
            except httpx.TransportError as exc:
                if retry is Retry.NEVER or attempt >= self.max_retries:
                    raise MageConnectionError(f"{method} {url} failed: {exc!r}") from exc
            else:
                if response.is_success:
                    return response
                error = to_error(response)
                if attempt >= self.max_retries or not should_retry(retry, error):
                    raise error
            _sleep(retry_delay(attempt))
            attempt += 1


class Requests:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def get(self, request_id: str) -> GenerationRequest:
        """Read a request's current state."""
        return cast(
            GenerationRequest,
            self._client._request(
                "GET", f"/v1/requests/{segment(request_id)}/status", retry=Retry.SAFE
            ),
        )

    def cancel(self, request_id: str) -> GenerationRequest:
        """Stop a live request. Gems are not returned for a cancelled request."""
        return cast(
            GenerationRequest,
            self._client._request(
                "POST", f"/v1/requests/{segment(request_id)}/cancel", retry=Retry.SAFE
            ),
        )

    def wait(
        self,
        request: str | GenerationRequest,
        *,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        max_poll_interval: float = DEFAULT_MAX_POLL_INTERVAL,
        timeout: float | None = None,
        on_update: OnUpdate | None = None,
    ) -> GenerationRequest:
        """Poll a request until it is completed, failed, or cancelled, and return it.

        Polling starts at `poll_interval` seconds and grows by half each time, up to
        `max_poll_interval`, with a little jitter. `on_update` receives every state read.

        Raises:
            MageTimeoutError: `timeout` seconds passed first. The request keeps running.
        """
        deadline = None if timeout is None else _clock() + timeout
        if isinstance(request, str):
            current = self.get(request)
            if on_update is not None:
                on_update(current)
        else:
            current = request
        delay = poll_interval
        while not is_final(current):
            pause = poll_delay(delay)
            if deadline is not None:
                remaining = deadline - _clock()
                if remaining <= 0:
                    raise MageTimeoutError(timeout_message(current, timeout), request=current)
                pause = min(pause, remaining)
            _sleep(pause)
            current = self.get(current["request_id"])
            if on_update is not None:
                on_update(current)
            delay = next_poll_interval(delay, max_poll_interval)
        return current


class Uploads:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def create(self, *, content_type: str) -> UploadTicket:
        """Create an upload ticket. Prefer `upload`, which also sends the file."""
        return cast(
            UploadTicket,
            self._client._request(
                "POST", "/v1/uploads", retry=Retry.SAFE, json={"content_type": content_type}
            ),
        )

    def upload(self, data: UploadData, *, content_type: str | None = None) -> UploadTicket:
        """Upload a file to Mage storage and return its ticket.

        Send `ticket["url"]` in any media field of a generate request, or as the image,
        voice, or audio of a character or reference.

        Args:
            data: Bytes, a file path, or a binary file object (at most 100 MB).
            content_type: Required for bytes; otherwise inferred from the file suffix.
        """
        payload, resolved = read_upload(data, content_type)
        ticket = self.create(content_type=resolved)
        check_upload_size(payload, ticket["max_bytes"])
        self._client._send(
            ticket["method"],
            ticket["upload_url"],
            retry=Retry.SAFE,
            to_error=upload_error,
            headers=ticket["headers"],
            content=payload,
        )
        return ticket


class Characters:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def list(self, *, limit: int | None = None, cursor: str | None = None) -> CharacterList:
        """List your characters, newest first. Pass `next_cursor` back as `cursor`."""
        return cast(
            CharacterList,
            self._client._request(
                "GET", "/v1/characters", retry=Retry.SAFE, params=list_params(limit, cursor)
            ),
        )

    def create(
        self,
        *,
        name: str,
        image: str,
        handle: str | None = None,
        description: str | None = None,
        voice: str | None = None,
    ) -> Character:
        """Create a character. `image` and `voice` are https URLs, data URLs, or upload URLs."""
        body = without_none(
            name=name, image=image, handle=handle, description=description, voice=voice
        )
        return cast(
            Character,
            self._client._request("POST", "/v1/characters", retry=Retry.NEVER, json=body),
        )

    def delete(self, character_id: str) -> None:
        self._client._request("DELETE", f"/v1/characters/{segment(character_id)}", retry=Retry.SAFE)


class References:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def list(self, *, limit: int | None = None, cursor: str | None = None) -> ReferenceList:
        """List your references, newest first. Pass `next_cursor` back as `cursor`."""
        return cast(
            ReferenceList,
            self._client._request(
                "GET", "/v1/references", retry=Retry.SAFE, params=list_params(limit, cursor)
            ),
        )

    def create(
        self,
        *,
        name: str,
        kind: str,
        handle: str | None = None,
        image: str | None = None,
        audio: str | None = None,
        description: str | None = None,
    ) -> Reference:
        """Create a reference: `kind` is object, location, pose, or outfit (with `image`),
        or audio (with `audio`)."""
        body = without_none(
            name=name, kind=kind, handle=handle, image=image, audio=audio, description=description
        )
        return cast(
            Reference,
            self._client._request("POST", "/v1/references", retry=Retry.NEVER, json=body),
        )

    def delete(self, reference_id: str) -> None:
        self._client._request("DELETE", f"/v1/references/{segment(reference_id)}", retry=Retry.SAFE)


class AccountResource:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def get(self) -> Account:
        """Your gem balance."""
        return cast(Account, self._client._request("GET", "/v1/account", retry=Retry.SAFE))


class Architectures:
    def __init__(self, client: Mage) -> None:
        self._client = client

    def list(self) -> ArchitectureList:
        """Every architecture the API generates with, with its options, inputs, and price."""
        return cast(
            ArchitectureList,
            self._client._request("GET", "/v1/architectures", retry=Retry.SAFE),
        )
