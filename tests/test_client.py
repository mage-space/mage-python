from __future__ import annotations

import io
import uuid
from pathlib import Path

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

from mage_space import (
    Mage,
    MageAPIError,
    MageConnectionError,
    MageError,
    MageGenerationError,
    MageTimeoutError,
)

GENERATE = "/v1/mango/generate"
STATUS = f"/v1/requests/{REQUEST_ID}/status"
CANCEL = f"/v1/requests/{REQUEST_ID}/cancel"
UPLOAD_PATH = httpx.URL(UPLOAD_URL).path


def json_reply(status: int, body: object) -> httpx.Response:
    return httpx.Response(status, json=body)


# Configuration ---------------------------------------------------------------


def test_reads_key_and_base_url_from_environment(
    monkeypatch: pytest.MonkeyPatch, server: Server, clock: Clock
) -> None:
    monkeypatch.setenv("MAGE_API_KEY", "mage_sk_from_env")
    monkeypatch.setenv("MAGE_BASE_URL", "https://api.beta.mage.space/")
    server.add("GET", "/v1/account", json_reply(200, {"gems": {"balance": 808}}))
    http = httpx.Client(transport=httpx.MockTransport(server.handler))

    account = Mage(http_client=http).account.get()

    assert account == {"gems": {"balance": 808}}
    call = server.calls[0]
    assert call.url == "https://api.beta.mage.space/v1/account"
    assert call.headers["Authorization"] == "Bearer mage_sk_from_env"


def test_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MAGE_API_KEY", raising=False)
    with pytest.raises(MageError, match="MAGE_API_KEY"):
        Mage()


def test_closes_only_the_http_client_it_created() -> None:
    supplied = httpx.Client()
    Mage(api_key=API_KEY, http_client=supplied).close()
    assert not supplied.is_closed

    with Mage(api_key=API_KEY) as mage:
        owned = mage._http
    assert owned.is_closed


# Generate and retries ---------------------------------------------------------


def test_generate_posts_the_config_with_a_fresh_idempotency_key(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(202, request_body()), json_reply(202, request_body()))

    request = mage.generate("mango", {"prompt": "A lighthouse", "aspect_ratio": "16:9"})
    mage.generate("mango", {"prompt": "A lighthouse"})

    assert request["request_id"] == REQUEST_ID
    first, second = server.calls
    assert Server.json_of(first) == {"prompt": "A lighthouse", "aspect_ratio": "16:9"}
    assert first.headers["Authorization"] == f"Bearer {API_KEY}"
    assert first.headers["Content-Type"] == "application/json"
    uuid.UUID(first.headers["Idempotency-Key"])
    assert first.headers["Idempotency-Key"] != second.headers["Idempotency-Key"]


def test_generate_sends_the_callers_idempotency_key(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(200, request_body()))
    mage.generate("mango", {"prompt": "x"}, idempotency_key="job-42")
    assert server.calls[0].headers["Idempotency-Key"] == "job-42"


def test_generate_accepts_architectures_newer_than_the_sdk(mage: Mage, server: Server) -> None:
    server.add("POST", "/v1/brand_new_model/generate", json_reply(202, request_body()))
    mage.generate("brand_new_model", {"prompt": "x", "some_new_field": 3})
    assert Server.json_of(server.calls[0]) == {"prompt": "x", "some_new_field": 3}


def test_generate_retries_an_unrecorded_5xx_with_the_same_key(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add(
        "POST",
        GENERATE,
        httpx.Response(502, text="<html>Bad gateway</html>"),
        json_reply(202, request_body()),
    )

    request = mage.generate("mango", {"prompt": "x"})

    assert request["status"] == "in_progress"
    first, second = server.calls
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"]
    assert len(clock.sleeps) == 1


def test_generate_retries_a_connection_error_with_the_same_key(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, httpx.ConnectError("reset"), json_reply(202, request_body()))

    mage.generate("mango", {"prompt": "x"})

    first, second = server.calls
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"]


def test_generate_does_not_retry_a_refusal_mage_recorded(mage: Mage, server: Server) -> None:
    server.add(
        "POST",
        GENERATE,
        json_reply(500, error_body("internal_error", "Something broke.", request_id=REQUEST_ID)),
    )

    with pytest.raises(MageAPIError) as caught:
        mage.generate("mango", {"prompt": "x"})

    assert caught.value.request_id == REQUEST_ID
    assert len(server.calls) == 1


def test_generate_does_not_retry_too_many_requests(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(429, error_body("too_many_requests")))

    with pytest.raises(MageAPIError) as caught:
        mage.generate("mango", {"prompt": "x"})

    assert caught.value.status == 429
    assert caught.value.code == "too_many_requests"
    assert len(server.calls) == 1


def test_safe_calls_retry_rate_limits_and_server_errors(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add(
        "GET",
        "/v1/account",
        json_reply(429, error_body("too_many_requests")),
        httpx.Response(503, text="unavailable"),
        json_reply(200, {"gems": {"balance": 5}}),
    )

    assert mage.account.get() == {"gems": {"balance": 5}}
    assert len(server.calls) == 3
    assert len(clock.sleeps) == 2
    assert 0.5 <= clock.sleeps[0] <= 0.625
    assert 1.0 <= clock.sleeps[1] <= 1.25


def test_retries_stop_after_max_retries(mage: Mage, server: Server) -> None:
    server.add("GET", "/v1/account", *(httpx.Response(503) for _ in range(3)))

    with pytest.raises(MageAPIError) as caught:
        mage.account.get()

    assert caught.value.status == 503
    assert len(server.calls) == 3


def test_unreachable_api_raises_a_connection_error(mage: Mage, server: Server) -> None:
    server.add("GET", "/v1/account", *(httpx.ConnectTimeout("slow") for _ in range(3)))

    with pytest.raises(MageConnectionError):
        mage.account.get()

    assert len(server.calls) == 3


def test_creates_are_never_retried(mage: Mage, server: Server) -> None:
    server.add("POST", "/v1/characters", httpx.Response(503), httpx.ConnectError("reset"))

    with pytest.raises(MageAPIError):
        mage.characters.create(name="Ana", image="https://example.com/ana.png")
    with pytest.raises(MageConnectionError):
        mage.characters.create(name="Ana", image="https://example.com/ana.png")

    assert len(server.calls) == 2


# Errors ----------------------------------------------------------------------


def test_api_error_carries_the_envelope(mage: Mage, server: Server) -> None:
    body = error_body(
        "insufficient_gems", "This costs 40 gems.", request_id=REQUEST_ID, gems_required=40
    )
    server.add("POST", GENERATE, json_reply(402, body))

    with pytest.raises(MageAPIError) as caught:
        mage.generate("mango", {"prompt": "x"})

    error = caught.value
    assert (error.status, error.code, error.message) == (
        402,
        "insufficient_gems",
        "This costs 40 gems.",
    )
    assert error.request_id == REQUEST_ID
    assert error.body["error"]["gems_required"] == 40
    assert str(error) == "402 insufficient_gems: This costs 40 gems."


def test_non_json_error_bodies_have_no_code(mage: Mage, server: Server) -> None:
    server.add("DELETE", "/v1/characters/abc", httpx.Response(404, text="<html>Not found</html>"))

    with pytest.raises(MageAPIError) as caught:
        mage.characters.delete("abc")

    assert caught.value.code is None
    assert caught.value.message == "HTTP 404"
    assert caught.value.body == "<html>Not found</html>"


def test_unknown_error_codes_are_kept(mage: Mage, server: Server) -> None:
    server.add("GET", "/v1/architectures", json_reply(418, error_body("brand_new_code", "Hmm.")))

    with pytest.raises(MageAPIError) as caught:
        mage.architectures.list()

    assert caught.value.code == "brand_new_code"
    assert caught.value.status == 418


# Waiting and running -------------------------------------------------------------


def test_wait_returns_a_final_request_without_polling(mage: Mage, server: Server) -> None:
    done = request_body("completed")
    assert mage.requests.wait(done) == done  # type: ignore[arg-type]
    assert server.calls == []


def test_wait_polls_with_growing_intervals_until_final(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add(
        "GET",
        STATUS,
        *(json_reply(200, request_body()) for _ in range(6)),
        json_reply(200, request_body("completed")),
    )
    seen: list[str] = []

    final = mage.requests.wait(
        request_body(),  # type: ignore[arg-type]
        on_update=lambda request: seen.append(request["status"]),
    )

    assert final["status"] == "completed"
    assert seen == ["in_progress"] * 6 + ["completed"]
    expected = [2.0, 3.0, 4.5, 6.75, 10.125, 15.0, 15.0]
    assert len(clock.sleeps) == len(expected)
    for actual, base in zip(clock.sleeps, expected, strict=True):
        assert base <= actual <= base + 0.5


def test_wait_by_id_reads_the_request_first(mage: Mage, server: Server, clock: Clock) -> None:
    server.add("GET", STATUS, json_reply(200, request_body("failed")))
    seen: list[str] = []

    final = mage.requests.wait(REQUEST_ID, on_update=lambda r: seen.append(r["status"]))

    assert final["status"] == "failed"
    assert seen == ["failed"]
    assert clock.sleeps == []


def test_wait_raises_after_its_timeout_without_cancelling(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add("GET", STATUS, *(json_reply(200, request_body()) for _ in range(10)))

    with pytest.raises(MageTimeoutError) as caught:
        mage.requests.wait(REQUEST_ID, timeout=5)

    assert caught.value.request["status"] == "in_progress"
    assert sum(clock.sleeps) == pytest.approx(5)
    assert server.calls_to("POST", CANCEL) == []


def test_wait_does_not_start_a_read_after_the_deadline(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add("GET", STATUS, *(json_reply(200, request_body()) for _ in range(10)))

    with pytest.raises(MageTimeoutError):
        mage.requests.wait(request_body(), poll_interval=2, timeout=3)

    # One read after the first pause; the next pause ends at the deadline.
    assert len(server.calls_to("GET", STATUS)) == 1


def test_wait_cuts_a_status_read_to_the_time_left(mage: Mage, server: Server) -> None:
    server.add("GET", STATUS, json_reply(200, request_body("completed")))

    mage.requests.wait(REQUEST_ID, timeout=0.25)

    (read,) = server.calls_to("GET", STATUS)
    assert read.extensions["timeout"]["read"] == pytest.approx(0.25)


def test_wait_stops_retrying_a_read_at_the_deadline(
    mage: Mage, server: Server, clock: Clock
) -> None:
    server.add("GET", STATUS, httpx.Response(503))

    with pytest.raises(MageTimeoutError) as caught:
        mage.requests.wait(REQUEST_ID, timeout=0.3)

    assert caught.value.request is None
    assert len(server.calls_to("GET", STATUS)) == 1
    assert sum(clock.sleeps) == pytest.approx(0.3)


def test_run_returns_the_completed_request(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(202, request_body()))
    server.add("GET", STATUS, json_reply(200, request_body("completed")))

    request = mage.run("mango", {"prompt": "A lighthouse"})

    assert request["result"] is not None
    assert request["result"]["url"].endswith("out.png")


def test_run_raises_when_the_request_fails(mage: Mage, server: Server) -> None:
    failed = request_body(
        "failed",
        error={"code": "content_blocked", "message": "The output was blocked."},
        billing={"mode": "gems", "gems_charged": 135},
    )
    server.add("POST", GENERATE, json_reply(202, request_body()))
    server.add("GET", STATUS, json_reply(200, failed))

    with pytest.raises(MageGenerationError) as caught:
        mage.run("mango", {"prompt": "x"})

    assert caught.value.code == "content_blocked"
    assert caught.value.message == "The output was blocked."
    assert caught.value.request["status"] == "failed"


def test_run_raises_when_the_request_is_cancelled(mage: Mage, server: Server) -> None:
    server.add("POST", GENERATE, json_reply(202, request_body("cancelled")))

    with pytest.raises(MageGenerationError) as caught:
        mage.run("mango", {"prompt": "x"})

    assert caught.value.code == "cancelled"


def test_cancel_posts_to_the_cancel_endpoint(mage: Mage, server: Server) -> None:
    server.add("POST", CANCEL, json_reply(200, request_body("cancelled")))
    assert mage.requests.cancel(REQUEST_ID)["status"] == "cancelled"


# Uploads -------------------------------------------------------------------------


def test_upload_puts_the_bytes_with_exactly_the_ticket_headers(mage: Mage, server: Server) -> None:
    server.add("POST", "/v1/uploads", json_reply(200, ticket("video/mp4")))
    server.add("PUT", UPLOAD_PATH, httpx.Response(200))

    result = mage.uploads.upload(b"\x00\x01video", content_type="video/mp4")

    assert result["url"] == "https://cdn.mage.space/temp/30d/uploads/abc"
    create, put = server.calls
    assert Server.json_of(create) == {"content_type": "video/mp4"}
    assert str(put.url) == UPLOAD_URL
    assert put.content == b"\x00\x01video"
    assert put.headers["Content-Type"] == "video/mp4"
    assert put.headers["x-goog-content-length-range"] == "0,104857600"
    assert "Authorization" not in put.headers


def test_upload_infers_the_content_type_from_the_file_name(
    mage: Mage, server: Server, tmp_path: Path
) -> None:
    clip = tmp_path / "clip.MOV"
    clip.write_bytes(b"mov")
    server.add(
        "POST",
        "/v1/uploads",
        json_reply(200, ticket("video/quicktime")),
        json_reply(200, ticket("audio/wav")),
    )
    server.add("PUT", UPLOAD_PATH, httpx.Response(200), httpx.Response(200))

    mage.uploads.upload(clip)
    voice = io.BytesIO(b"wav")
    voice.name = "voice.wav"
    mage.uploads.upload(voice)

    creates = server.calls_to("POST", "/v1/uploads")
    assert [Server.json_of(c)["content_type"] for c in creates] == ["video/quicktime", "audio/wav"]
    assert [c.content for c in server.calls_to("PUT", UPLOAD_PATH)] == [b"mov", b"wav"]


def test_upload_needs_a_content_type_for_raw_bytes(mage: Mage, server: Server) -> None:
    with pytest.raises(MageError, match="content_type"):
        mage.uploads.upload(b"data")
    assert server.calls == []


def test_upload_refuses_a_file_over_the_ticket_limit(mage: Mage, server: Server) -> None:
    server.add("POST", "/v1/uploads", json_reply(200, ticket("image/png", max_bytes=4)))

    with pytest.raises(MageError, match="at most 4 bytes"):
        mage.uploads.upload(b"12345", content_type="image/png")

    assert server.calls_to("PUT", UPLOAD_PATH) == []


def test_upload_retries_storage_errors_and_reports_refusals(mage: Mage, server: Server) -> None:
    server.add(
        "POST",
        "/v1/uploads",
        json_reply(200, ticket("image/png")),
        json_reply(200, ticket("image/png")),
    )
    server.add("PUT", UPLOAD_PATH, httpx.Response(503), httpx.Response(200), httpx.Response(403))

    mage.uploads.upload(b"png", content_type="image/png")
    with pytest.raises(MageAPIError) as caught:
        mage.uploads.upload(b"png", content_type="image/png")

    assert caught.value.status == 403
    assert caught.value.code is None
    assert len(server.calls_to("PUT", UPLOAD_PATH)) == 3


# Library --------------------------------------------------------------------------


def test_list_sends_pagination_params_only_when_given(mage: Mage, server: Server) -> None:
    page = {"data": [], "next_cursor": None}
    server.add("GET", "/v1/characters", json_reply(200, page), json_reply(200, page))
    server.add("GET", "/v1/references", json_reply(200, page))

    mage.characters.list()
    mage.characters.list(limit=10, cursor="abc")
    mage.references.list(limit=200)

    first, second, third = server.calls
    assert first.url.query == b""
    assert dict(second.url.params) == {"limit": "10", "cursor": "abc"}
    assert dict(third.url.params) == {"limit": "200"}


def test_create_sends_only_the_fields_given(mage: Mage, server: Server) -> None:
    server.add("POST", "/v1/references", json_reply(201, {"id": "r1"}))

    mage.references.create(name="Red coat", kind="outfit", image="https://example.com/coat.png")

    assert Server.json_of(server.calls[0]) == {
        "name": "Red coat",
        "kind": "outfit",
        "image": "https://example.com/coat.png",
    }


def test_delete_returns_none(mage: Mage, server: Server) -> None:
    server.add("DELETE", "/v1/references/r1", httpx.Response(204))
    assert mage.references.delete("r1") is None
