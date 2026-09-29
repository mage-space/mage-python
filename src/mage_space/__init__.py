"""The official Python SDK for the Mage API."""

from ._async_client import AsyncMage
from ._base import UploadData
from ._client import Mage
from ._errors import (
    MageAPIError,
    MageConnectionError,
    MageError,
    MageGenerationError,
    MageTimeoutError,
)
from ._generated import ARCHITECTURES, ArchitectureId, ArchitectureInfo, ErrorCode
from ._version import __version__

__all__ = [
    "ARCHITECTURES",
    "ArchitectureId",
    "ArchitectureInfo",
    "AsyncMage",
    "ErrorCode",
    "Mage",
    "MageAPIError",
    "MageConnectionError",
    "MageError",
    "MageGenerationError",
    "MageTimeoutError",
    "UploadData",
    "__version__",
]
