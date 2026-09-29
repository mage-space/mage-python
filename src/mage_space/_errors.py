from __future__ import annotations

from typing import Any

import httpx

from ._generated import GenerationRequest

__all__ = [
    "MageAPIError",
    "MageConnectionError",
    "MageError",
    "MageGenerationError",
    "MageTimeoutError",
]


class MageError(Exception):
    """Base class for every error this SDK raises."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class MageAPIError(MageError):
    """The API (or the upload storage) answered with an error status."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        code: str | None,
        request_id: str | None,
        body: Any,
        headers: httpx.Headers,
    ) -> None:
        super().__init__(message)
        self.status = status
        """The HTTP status code."""
        self.code = code
        """The error code from the envelope, or None when the body is not a Mage error
        envelope (for example an HTML 502 from a proxy). Treat an unknown code by `status`."""
        self.request_id = request_id
        """The request the refusal was recorded under, when there is one."""
        self.body = body
        """The parsed JSON body, or the raw text when it is not JSON."""
        self.headers = headers

    def __str__(self) -> str:
        label = f"{self.status} {self.code}" if self.code else str(self.status)
        return f"{label}: {self.message}"


class MageConnectionError(MageError):
    """The HTTP call never got a response (network error or timeout), after retries."""


class MageTimeoutError(MageError):
    """`wait` or `run` passed its deadline. The request keeps running on Mage."""

    def __init__(self, message: str, *, request: GenerationRequest) -> None:
        super().__init__(message)
        self.request = request
        """The last state seen before the deadline."""


class MageGenerationError(MageError):
    """`run` ended with a failed or cancelled request."""

    def __init__(self, request: GenerationRequest) -> None:
        error = request.get("error")
        if request["status"] == "cancelled":
            code = "cancelled"
            message = f"Request {request['request_id']} was cancelled."
        elif error:
            code = error["code"]
            message = error["message"]
        else:
            code = "generation_failed"
            message = f"Request {request['request_id']} failed."
        super().__init__(message)
        self.request = request
        """The final state of the request."""
        self.code = code
        """`error.code` of the failed request (for example `content_blocked`), or `cancelled`."""

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
