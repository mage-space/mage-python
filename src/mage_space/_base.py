"""Pieces shared by the sync and async clients."""

from __future__ import annotations

import enum
import json
import os
import random
from pathlib import Path
from typing import IO, Any, TypeAlias
from urllib.parse import quote

import httpx

from ._errors import MageAPIError, MageError
from ._generated import GenerationRequest
from ._version import __version__

DEFAULT_BASE_URL = "https://api.mage.space"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_POLL_INTERVAL = 2.0
DEFAULT_MAX_POLL_INTERVAL = 15.0
FINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})
USER_AGENT = f"mage-space-python/{__version__}"

UploadData: TypeAlias = bytes | bytearray | memoryview | str | os.PathLike[str] | IO[bytes]
"""Bytes, a file path, or a binary file object."""

# The content types the upload endpoint accepts, by file suffix.
CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}


class Retry(enum.Enum):
    """Which failures a call may be retried after."""

    SAFE = "safe"
    """Reads, deletes, cancels, and uploads: connection errors, 408, 429, 5xx."""
    GENERATE = "generate"
    """Submits (same Idempotency-Key): connection errors, and 408/5xx not recorded by Mage."""
    NEVER = "never"
    """Creates that are not idempotent."""


def resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("MAGE_API_KEY")
    if not key:
        raise MageError(
            "No API key. Pass api_key=... or set the MAGE_API_KEY environment variable. "
            "Create one at https://www.mage.space/api?tab=api-keys."
        )
    return key


def resolve_base_url(base_url: str | None) -> str:
    return (base_url or os.environ.get("MAGE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def api_headers(api_key: str, *, json_body: bool) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    return headers


def segment(value: str) -> str:
    return quote(value, safe="")


def api_error(response: httpx.Response) -> MageAPIError:
    try:
        body: Any = response.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        body = response.text
    envelope = body.get("error") if isinstance(body, dict) else None
    if isinstance(envelope, dict) and isinstance(envelope.get("code"), str):
        return MageAPIError(
            str(envelope.get("message") or f"HTTP {response.status_code}"),
            status=response.status_code,
            code=envelope["code"],
            request_id=envelope.get("request_id"),
            body=body,
            headers=response.headers,
        )
    return MageAPIError(
        f"HTTP {response.status_code}",
        status=response.status_code,
        code=None,
        request_id=None,
        body=body,
        headers=response.headers,
    )


def should_retry(policy: Retry, error: MageAPIError) -> bool:
    status = error.status
    if policy is Retry.SAFE:
        return status in (408, 429) or status >= 500
    if policy is Retry.GENERATE:
        return (status == 408 or status >= 500) and error.request_id is None
    return False


def retry_delay(attempt: int) -> float:
    """Seconds to wait before retry number `attempt + 1`."""
    return min(0.5 * 2.0**attempt * (1 + random.uniform(0, 0.25)), 8.0)


def poll_delay(delay: float) -> float:
    return delay + random.uniform(0, 0.5)


def next_poll_interval(delay: float, max_poll_interval: float) -> float:
    return min(delay * 1.5, max_poll_interval)


def is_final(request: GenerationRequest) -> bool:
    return request["status"] in FINAL_STATUSES


def timeout_message(request_id: str, request: GenerationRequest | None, timeout: float) -> str:
    state = f"last status: {request['status']}" if request else "no status read yet"
    return (
        f"Request {request_id} did not finish within {timeout} seconds ({state}). "
        "It is still running on Mage; wait for it again or cancel it."
    )


def attempt_timeout(timeout: float, deadline: float | None, now: float) -> float:
    """Seconds one HTTP attempt may take: the client timeout, cut to what is left
    before a wait's deadline (zero or less once it has passed)."""
    return timeout if deadline is None else min(timeout, deadline - now)


def retry_pause(attempt: int, deadline: float | None, now: float) -> float:
    """The backoff before a retry, never past a wait's deadline."""
    delay = retry_delay(attempt)
    return delay if deadline is None else max(0.0, min(delay, deadline - now))


def read_upload(data: UploadData, content_type: str | None) -> tuple[bytes, str]:
    """Read the bytes to upload and settle their content type."""
    name: str | None = None
    if isinstance(data, (bytes, bytearray, memoryview)):
        payload = bytes(data)
    elif isinstance(data, (str, os.PathLike)):
        path = Path(data)
        payload = path.read_bytes()
        name = path.name
    else:
        payload = data.read()
        file_name = getattr(data, "name", None)
        name = file_name if isinstance(file_name, str) else None
    if content_type is None and name is not None:
        content_type = CONTENT_TYPES.get(Path(name).suffix.lower())
    if content_type is None:
        raise MageError(
            "Could not tell the file's content type. Pass content_type=, for example "
            "'image/png', 'video/mp4', or 'audio/mpeg'."
        )
    return payload, content_type


def check_upload_size(payload: bytes, max_bytes: int) -> None:
    if len(payload) > max_bytes:
        raise MageError(
            f"The file is {len(payload)} bytes; an upload accepts at most {max_bytes} bytes."
        )


def upload_error(response: httpx.Response) -> MageAPIError:
    return MageAPIError(
        f"Upload failed with HTTP {response.status_code}",
        status=response.status_code,
        code=None,
        request_id=None,
        body=response.text,
        headers=response.headers,
    )


def list_params(limit: int | None, cursor: str | None) -> dict[str, str | int]:
    params: dict[str, str | int] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    return params


def without_none(**fields: Any) -> dict[str, Any]:
    return {key: value for key, value in fields.items() if value is not None}
