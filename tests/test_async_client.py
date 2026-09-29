from __future__ import annotations

import httpx
import pytest
from conftest import (
    API_KEY,
    REQUEST_ID,
    UPLOAD_URL,
    Clock,
    Server,
    error_body,
    request_body,
    ticket,
)

from mage_space import AsyncMage, MageAPIError, MageGenerationError, MageTimeoutError
from mage_space.types import GenerationRequest

pytestmark = pytest.mark.anyio

GENERATE = "/v1/cherry/generate"
STATUS = f"/v1/requests/{REQUEST_ID}/status"
CANCEL = f"/v1/requests/{REQUEST_ID}/cancel"


def json_reply(status: int, body: object) -> httpx.Response:
    return httpx.Response(status, json=body)


async def test_generate_retries_an_unrecorded_5xx_with_the_same_key(
    async_mage: AsyncMage, server: Server, clock: Clock
) -> None:
    server.add("POST", GENERATE, httpx.Response(504), json_reply(202, request_body()))

    request = await async_mage.generate("cherry", {"prompt": "A wave", "duration": "5"})

    assert request["request_id"] == REQUEST_ID
    first, second = server.calls
    assert Server.json_of(first) == {"prompt": "A wave", "duration": "5"}
    assert first.headers["Authorization"] == f"Bearer {API_KEY}"
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"]
    assert len(clock.sleeps) == 1


async def test_generate_does_not_retry_a_recorded_refusal(
    async_mage: AsyncMage, server: Server
) -> None:
    server.add(
        "POST", GENERATE, json_reply(503, error_body("internal_error", request_id=REQUEST_ID))
    )

    with pytest.raises(MageAPIError):
        await async_mage.generate("cherry", {"prompt": "x"})

    assert len(server.calls) == 1


async def test_wait_backs_off_and_awaits_a_coroutine_callback(
    async_mage: AsyncMage, server: Server, clock: Clock
) -> None:
    server.add(
        "GET",
        STATUS,
        json_reply(200, request_body()),
        json_reply(200, request_body()),
        json_reply(200, request_body("completed")),
    )
    seen: list[str] = []

    async def on_update(request: GenerationRequest) -> None:
        seen.append(request["status"])

    final = await async_mage.requests.wait(
        request_body(),  # type: ignore[arg-type]
        poll_interval=5,
        on_update=on_update,
    )

    assert final["status"] == "completed"
    assert seen == ["in_progress", "in_progress", "completed"]
    for actual, base in zip(clock.sleeps, [5.0, 7.5, 11.25], strict=True):
        assert base <= actual <= base + 0.5


async def test_wait_accepts_a_plain_callback(async_mage: AsyncMage, server: Server) -> None:
    server.add("GET", STATUS, json_reply(200, request_body("completed")))
    seen: list[str] = []

    await async_mage.requests.wait(REQUEST_ID, on_update=lambda r: seen.append(r["status"]))

    assert seen == ["completed"]


async def test_wait_times_out(async_mage: AsyncMage, server: Server, clock: Clock) -> None:
    server.add("GET", STATUS, *(json_reply(200, request_body()) for _ in range(5)))

    with pytest.raises(MageTimeoutError) as caught:
        await async_mage.requests.wait(REQUEST_ID, timeout=3)

    assert caught.value.request["request_id"] == REQUEST_ID
    assert sum(clock.sleeps) == pytest.approx(3)


async def test_run_raises_for_a_failed_request(async_mage: AsyncMage, server: Server) -> None:
    failed = request_body(
        "failed", error={"code": "generation_failed", "message": "The model errored."}
    )
    server.add("POST", GENERATE, json_reply(202, request_body()))
    server.add("GET", STATUS, json_reply(200, failed))

    with pytest.raises(MageGenerationError) as caught:
        await async_mage.run("cherry", {"prompt": "x"})

    assert caught.value.code == "generation_failed"


async def test_run_returns_the_completed_request(async_mage: AsyncMage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(202, request_body()))
    server.add("GET", STATUS, json_reply(200, request_body("completed")))

    request = await async_mage.run("cherry", {"prompt": "x"})

    assert request["status"] == "completed"


async def test_cancel(async_mage: AsyncMage, server: Server) -> None:
    server.add("POST", CANCEL, json_reply(200, request_body("cancelled")))
    assert (await async_mage.requests.cancel(REQUEST_ID))["status"] == "cancelled"


async def test_upload_puts_bytes_without_the_api_key(async_mage: AsyncMage, server: Server) -> None:
    server.add("POST", "/v1/uploads", json_reply(200, ticket("image/png")))
    server.add("PUT", httpx.URL(UPLOAD_URL).path, httpx.Response(200))

    result = await async_mage.uploads.upload(b"png-bytes", content_type="image/png")

    assert result["url"].endswith("/uploads/abc")
    put = server.calls[1]
    assert put.content == b"png-bytes"
    assert put.headers["Content-Type"] == "image/png"
    assert "Authorization" not in put.headers


async def test_library_calls(async_mage: AsyncMage, server: Server) -> None:
    server.add("GET", "/v1/characters", json_reply(200, {"data": [], "next_cursor": "c2"}))
    server.add("DELETE", "/v1/characters/c1", httpx.Response(204))
    server.add("GET", "/v1/account", json_reply(200, {"gems": {"balance": 1}}))

    page = await async_mage.characters.list(cursor="c1")
    deleted = await async_mage.characters.delete("c1")
    account = await async_mage.account.get()

    assert page["next_cursor"] == "c2"
    assert deleted is None
    assert account["gems"]["balance"] == 1
    assert dict(server.calls[0].url.params) == {"cursor": "c1"}


async def test_async_context_manager_closes_its_own_client() -> None:
    async with AsyncMage(api_key=API_KEY) as mage:
        http = mage._http
    assert http.is_closed
