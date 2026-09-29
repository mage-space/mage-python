from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Iterator
from typing import Any

import httpx
import pytest

import mage_space._async_client as async_client_module
import mage_space._client as client_module
from mage_space import AsyncMage, Mage

API_KEY = "mage_sk_test"
BASE = "https://api.mage.space"
REQUEST_ID = "d7e6c0f3-6699-4f6c-bb45-2ad7fd9158ff"
UPLOAD_URL = "https://storage.googleapis.com/mage-temp/temp/30d/uploads/abc?X-Goog-Signature=sig"

Reply = httpx.Response | Exception | Callable[[httpx.Request], httpx.Response]


def request_body(status: str = "in_progress", **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "status": status,
        "architecture": "mango",
        "model_id": "mango-v3",
        "created_at": "2026-09-17T14:52:48.000Z",
        "updated_at": "2026-09-17T14:52:49.000Z",
        "billing": {"mode": "gems", "gems_charged": 135},
        "result": None,
        "error": None,
        "status_url": f"{BASE}/v1/requests/{REQUEST_ID}/status",
        "cancel_url": f"{BASE}/v1/requests/{REQUEST_ID}/cancel",
    }
    if status == "completed":
        body["result"] = {
            "type": "image",
            "url": "https://cdn.mage.space/temp/30d/out.png",
            "width": 1024,
            "height": 1280,
            "seed": 42,
            "expires_at": "2026-10-17T14:52:48.000Z",
            "moderation": {"nsfw": False},
        }
    body.update(overrides)
    return body


def error_body(code: str, message: str = "Refused.", **fields: Any) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, **fields}}


def ticket(content_type: str = "video/mp4", max_bytes: int = 104857600) -> dict[str, Any]:
    return {
        "upload_url": UPLOAD_URL,
        "method": "PUT",
        "headers": {
            "Content-Type": content_type,
            "x-goog-content-length-range": f"0,{max_bytes}",
        },
        "url": "https://cdn.mage.space/temp/30d/uploads/abc",
        "content_type": content_type,
        "max_bytes": max_bytes,
        "upload_url_expires_at": "2026-09-17T15:07:48.000Z",
        "url_expires_at": "2026-10-17T14:52:48.000Z",
    }


class Server:
    """Answers each (method, path) with queued replies, in order, and records every call."""

    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], list[Reply]] = defaultdict(list)
        self.calls: list[httpx.Request] = []

    def add(self, method: str, path: str, *replies: Reply) -> None:
        self.routes[(method, path)].extend(replies)

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        queue = self.routes[(request.method, request.url.path)]
        if not queue:
            raise AssertionError(f"Unexpected call: {request.method} {request.url}")
        reply = queue.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if isinstance(reply, httpx.Response):
            return reply
        return reply(request)

    def calls_to(self, method: str, path: str) -> list[httpx.Request]:
        return [c for c in self.calls if c.method == method and c.url.path == path]

    @staticmethod
    def json_of(request: httpx.Request) -> Any:
        return json.loads(request.content)


class Clock:
    """A fake monotonic clock that sleeping advances."""

    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds

    async def async_sleep(self, seconds: float) -> None:
        self.sleep(seconds)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> Clock:
    fake = Clock()
    monkeypatch.setattr(client_module, "_sleep", fake.sleep)
    monkeypatch.setattr(client_module, "_clock", fake.monotonic)
    monkeypatch.setattr(async_client_module, "_sleep", fake.async_sleep)
    monkeypatch.setattr(async_client_module, "_clock", fake.monotonic)
    return fake


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture
def mage(server: Server, clock: Clock) -> Iterator[Mage]:
    http = httpx.Client(transport=httpx.MockTransport(server.handler))
    with Mage(api_key=API_KEY, http_client=http) as client:
        yield client
    http.close()


@pytest.fixture
def async_mage(server: Server, clock: Clock) -> AsyncMage:
    http = httpx.AsyncClient(transport=httpx.MockTransport(server.handler))
    return AsyncMage(api_key=API_KEY, http_client=http)
