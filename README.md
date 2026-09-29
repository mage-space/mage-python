# Mage Python SDK

> **Beta.** This SDK is at 0.x: names and behaviour may change between minor versions until 1.0. The [Mage API](https://docs.mage.space/api/overview) itself is versioned separately and is stable within `v1`.

The official Python client for the [Mage API](https://docs.mage.space/api/overview). Generate images, video, and audio with Mage models from your own code. Every request is paid in Gems from your Mage account.

- Sync (`Mage`) and asyncio (`AsyncMage`) clients on [httpx](https://www.python-httpx.org/)
- `run()` submits a generation and waits for the result, backing off as the API recommends
- Safe retries: every submit carries an idempotency key, so a retry is never charged twice
- Uploads of large files through signed URLs in one call
- Typed request and response bodies for every model, generated from the API's OpenAPI spec

## Install

```bash
pip install mage-space
# or
uv add mage-space
```

Python 3.10 or newer.

## Quick start

Create a key in [API → API Keys](https://www.mage.space/api?tab=api-keys) and export it:

```bash
export MAGE_API_KEY="mage_sk_..."
```

```python
from mage_space import Mage

mage = Mage()

request = mage.run("mango", {"prompt": "A lighthouse at dawn, 35mm film", "aspect_ratio": "16:9"})
print(request["result"]["url"])
```

Keys belong to your account and spend your Gems. Keep them on your servers: the API sends no CORS headers, and a key shipped inside an app can be extracted.

## Generating

`run()` is `generate()` followed by `requests.wait()`. Use the parts when you want the request id before the output is ready:

```python
request = mage.generate(
    "cherry",
    {
        "prompt": "Waves rolling onto a black sand beach at sunset",
        "resolution": "720p",
        "duration": "5",
    },
)
print(request["request_id"], request["status"])  # ... in_progress

final = mage.requests.wait(
    request,
    timeout=900,  # seconds; then MageTimeoutError, and the request keeps running
    on_update=lambda r: print(r["status"]),
)
if final["status"] == "completed":
    print(final["result"]["url"])
```

`wait()` polls with growing intervals (2 s, then ×1.5 up to 15 s, with jitter). `run()` raises `MageGenerationError` when the request fails or is cancelled, so what it returns always has a `result`. Cancel a live request with `mage.requests.cancel(request_id)`; Gems are not returned for a cancelled request.

Results are kept for 30 days. Download what you want to keep.

### Async

```python
import asyncio

from mage_space import AsyncMage


async def main() -> None:
    async with AsyncMage() as mage:
        request = await mage.run("seed_audio", {"prompt": "Rain on a tin roof", "duration": "10"})
        print(request["result"]["url"])


asyncio.run(main())
```

`AsyncMage` has the same methods. Its `on_update` may be a plain function or a coroutine function.

## Models

The first argument is the model's architecture id, as in its endpoint path: `mango` for images, `cherry` for video, `seed_audio` for audio, and [many more](https://docs.mage.space/api/models/overview). Choose a variant with `model_id`:

```python
mage.run("mango", {"prompt": "...", "model_id": "mango-v3s"})
```

Each model has a TypedDict in `mage_space.types` with its fields, allowed values, and defaults. Annotate a config with it to have your type checker check it:

```python
from mage_space.types import CherryConfig

config: CherryConfig = {"prompt": "A paper boat in a gutter stream", "resolution": "1080p"}
mage.run("cherry", config)
```

Fields a model's schema does not list pass through to the model unchanged, and a model newer than your SDK works by its id. For the live catalog with each model's options and price, call `mage.architectures.list()`. `mage_space.ARCHITECTURES` holds the name, output type, and request JSON Schema of every model this SDK version was generated from.

## Inputs and uploads

Media fields (`image`, `additional_images`, `first_image`, `last_image`, `video`, `videos`) take an `https` URL or a data URL. Request bodies are capped at 4.5 MB, so upload larger files first and send the returned URL:

```python
photo = mage.uploads.upload("photo.jpg")  # a path, bytes, or a binary file object; 100 MB max
mage.run("kiwi", {"prompt": "The camera slowly pushes in", "first_image": photo["url"]})

clip = mage.uploads.upload("clip.mp4")
mage.run("cherry", {"prompt": "Restyle this clip as watercolor", "videos": [clip["url"]]})
```

The content type comes from the file name; pass `content_type=` for raw bytes. Uploaded files are deleted after 30 days (`url_expires_at`).

## Characters and references

Save a character or a reference once, then mention it by `@handle` in any prompt:

```python
ana = mage.characters.create(name="Ana", handle="ana", image="https://example.com/ana.png")
coat = mage.references.create(name="Red coat", handle="red-coat", kind="outfit", image=photo["url"])

mage.run("mango", {"prompt": "@ana walking through a night market, wearing @red-coat"})

page = mage.characters.list(limit=50)
while page["next_cursor"]:
    page = mage.characters.list(cursor=page["next_cursor"])

mage.references.delete(coat["id"])
```

## Errors

| Exception | When |
| --- | --- |
| `MageAPIError` | The API answered with an error: `status`, `code` (for example `insufficient_gems`, `invalid_config`), `message`, `request_id`, `body`. |
| `MageConnectionError` | No response at all (network error or timeout), after retries. |
| `MageGenerationError` | `run()` ended with a failed or cancelled request: `code` (for example `content_blocked`) and the final `request`. |
| `MageTimeoutError` | `wait()` or `run()` passed its `timeout`. A response that finishes late is never returned; `Mage` checks the deadline between network reads, so a stalled read can overrun it by up to the time that was left when the read began (`AsyncMage` stops on time). `request` is the last state read (None if none was); the request keeps running. |

All four derive from `MageError`.

```python
from mage_space import MageAPIError, MageGenerationError

try:
    mage.run("mango", {"prompt": "..."})
except MageAPIError as error:
    if error.code == "insufficient_gems":
        print("Gems needed:", error.body["error"]["gems_required"])
    else:
        raise
except MageGenerationError as error:
    print("No output:", error.code, error.message)
```

New error codes may appear; treat an unknown `code` by its HTTP `status`.

## Retries and idempotency

Failed calls are retried up to `max_retries` times (default 2) with exponential backoff:

- Reads, deletes, cancels, and uploads retry on connection errors, 408, 429, and 5xx.
- `generate()` sends an `Idempotency-Key` header (a fresh UUID unless you pass `idempotency_key=`) and retries with the same key on connection errors and on 408 or 5xx responses that Mage did not record. A replayed submit returns the original request and charges nothing.
- Creating characters and references is never retried.

Pass your own `idempotency_key`, such as a job id, to make retries across processes safe too. Never reuse a key for a different request.

## Configuration

```python
Mage(
    api_key=None,  # default: MAGE_API_KEY
    base_url=None,  # default: MAGE_BASE_URL, else https://api.mage.space
    timeout=60.0,  # seconds per HTTP attempt
    max_retries=2,
    http_client=None,  # your own httpx.Client (an httpx.AsyncClient for AsyncMage)
)
```

Use `with Mage() as mage:` (or `mage.close()`) to close the connection pool. The SDK closes only an HTTP client it created.

## Documentation

- [API reference](https://docs.mage.space/api/overview): requests, inputs, errors, limits, and every model's fields
- [Changelog](https://github.com/mage-space/mage-python/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/mage-space/mage-python/blob/main/CONTRIBUTING.md)

## License

[MIT](https://github.com/mage-space/mage-python/blob/main/LICENSE)
