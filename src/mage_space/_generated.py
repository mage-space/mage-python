# Generated from spec/openapi.json by scripts/generate.py. Do not edit.

from typing import Any

from typing_extensions import Literal, NotRequired, TypedDict

__all__ = [
    "ARCHITECTURES",
    "Account",
    "AccountGems",
    "AnimaConfig",
    "Architecture",
    "ArchitectureId",
    "ArchitectureImageInputs",
    "ArchitectureImageInputsReferences",
    "ArchitectureInfo",
    "ArchitectureInputSchema",
    "ArchitectureList",
    "ArchitectureMentions",
    "ArchitectureVideoInputs",
    "BerryConfig",
    "BlueberryConfig",
    "Character",
    "CharacterList",
    "CherryConfig",
    "ChromaConfig",
    "CreateCharacterRequest",
    "CreateReferenceRequest",
    "ErrorBody",
    "ErrorBodyError",
    "ErrorCode",
    "Flux2Config",
    "GenerateConfig",
    "GenerationRequest",
    "GenerationRequestBilling",
    "GenerationRequestError",
    "GenerationRequestResult",
    "GenerationRequestResultModeration",
    "GptImage2Config",
    "GrokImageConfig",
    "GrokVideoConfig",
    "GuavaConfig",
    "HidreamConfig",
    "KiwiConfig",
    "Krea2Config",
    "LemonConfig",
    "LtxVideoConfig",
    "MangoConfig",
    "MelonConfig",
    "MinimaxH3Config",
    "NanoBananaV2Config",
    "PlumConfig",
    "RaspberryConfig",
    "Reference",
    "ReferenceList",
    "SdxlPlusConfig",
    "SeedAudioConfig",
    "StableDiffusionV15Config",
    "StableDiffusionV35LargeConfig",
    "StableDiffusionXlConfig",
    "UploadRequest",
    "UploadTicket",
    "Wan22Config",
    "ZImageConfig",
]

ErrorCode = Literal["unauthorized", "invalid_request", "invalid_config", "architecture_not_found", "architecture_retired", "request_not_found", "character_not_found", "reference_not_found", "not_found", "insufficient_gems", "forbidden", "content_blocked", "request_finished", "handle_taken", "too_many_requests", "generation_failed", "internal_error"]
"""Every error code the API documents. New codes may appear."""

ArchitectureId = Literal["anima", "chroma", "flux2", "gpt_image_2", "grok_image", "guava", "hidream", "krea_2", "mango", "nano_banana_v2", "sdxl_plus", "stable_diffusion_v15", "stable_diffusion_v35_large", "stable_diffusion_xl", "z_image", "berry", "blueberry", "cherry", "grok_video", "kiwi", "lemon", "ltx_video", "melon", "minimax_h3", "plum", "raspberry", "wan_22", "seed_audio"]
"""The architectures this SDK version knows about."""


class GenerationRequestBilling(TypedDict):
    mode: Literal["gems"]
    """Every API request is paid in gems."""
    gems_charged: float
    """Gems debited for the request."""
    gems_refunded: NotRequired[float]
    """Gems returned to the account; present on failed requests."""


class GenerationRequestResultModeration(TypedDict):
    """Moderation flags on the output."""
    nsfw: bool
    """Whether moderation flagged the output as NSFW."""


class GenerationRequestResult(TypedDict):
    type: Literal["image", "video", "audio"]
    """The media type of the output."""
    url: str
    """Where to download the output."""
    width: int
    """Output width in pixels; 0 for audio."""
    height: int
    """Output height in pixels; 0 for audio."""
    seed: int
    """The seed the generation ran with."""
    expires_at: str | None
    """When `url` stops working: 30 days after the request for temporary media, or null for permanent media."""
    moderation: GenerationRequestResultModeration
    """Moderation flags on the output."""


class GenerationRequestError(TypedDict):
    code: str
    """A stable error code."""
    message: str
    """What went wrong, for a person."""


class GenerationRequest(TypedDict):
    request_id: str
    """The request id, also the id in `status_url` and `cancel_url`."""
    status: Literal["queued", "in_progress", "completed", "failed", "cancelled"]
    """`queued` and `in_progress` are live; `completed`, `failed`, and `cancelled` are final."""
    architecture: str
    """The architecture the request generates with."""
    model_id: str | None
    """The model variant, when the architecture has variants."""
    created_at: str
    """When the request was accepted."""
    updated_at: str
    """When the request last changed."""
    billing: GenerationRequestBilling
    result: GenerationRequestResult | None
    """The output once `status` is `completed`, else null."""
    error: GenerationRequestError | None
    """Why the request failed once `status` is `failed`, else null."""
    status_url: str
    """Poll this URL for the request."""
    cancel_url: str
    """POST to this URL to stop the request."""


class ErrorBodyError(TypedDict):
    """Further fields depend on the code."""
    code: str
    """A stable error code; treat an unknown code by its HTTP status."""
    message: str
    """What went wrong, for a person."""
    request_id: NotRequired[str]
    """The request the refusal belongs to, when one was recorded before the refusal."""
    gems_required: NotRequired[float]
    """The price of the refused generation, on `insufficient_gems`."""
    docs_url: NotRequired[str]
    """Where to read the API reference, on `not_found`."""
    handle: NotRequired[str]
    """The handle that is taken, on `handle_taken`."""


class ErrorBody(TypedDict):
    error: ErrorBodyError
    """Further fields depend on the code."""


class GenerateConfig(TypedDict):
    prompt: str
    """The text prompt. An `@handle` in it attaches one of your saved characters or references."""
    model_id: NotRequired[str]
    """The model variant; the architecture default when omitted."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    aspect_ratio: NotRequired[str]
    """The output aspect ratio as `W:H` (`16:9`), on models that have one; each model lists its ratios."""
    first_image: NotRequired[str]
    """The first frame image, on models that start a video from one. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image, on models that end a video on one. An https URL or a data URL."""
    resolution: NotRequired[str]
    """The output resolution token, on models that offer one; each model lists its tokens."""
    duration: NotRequired[str]
    """The clip length in seconds as a token, on video and audio models that offer one; each model lists its tokens."""


class ArchitectureImageInputsReferences(TypedDict):
    field: str
    """The field the first reference image goes in."""
    additional_field: str | None
    """The list field further reference images go in, or null."""


class ArchitectureImageInputs(TypedDict):
    """The request field for each image role; an absent role is not supported."""
    first_frame: str | None
    """The field a first frame image goes in, or null."""
    last_frame: str | None
    """The field a last frame image goes in, or null."""
    references: ArchitectureImageInputsReferences | None
    """Reference image fields, or null when the architecture takes none."""


class ArchitectureVideoInputs(TypedDict):
    field: str
    """The field holding the source video or videos."""


class ArchitectureMentions(TypedDict):
    """Which saved characters and references a prompt may mention by `@handle`, per model variant."""
    characters: list[str]
    """Model ids whose prompts may mention `@character` handles; empty when none may."""
    references: list[str]
    """Model ids whose prompts may mention image `@reference` handles; empty when none may."""
    audio_references: list[str]
    """Model ids whose prompts may mention audio `@reference` handles; empty when none may."""
    max_audio_references: int
    """Audio references per request. On a model that also sends character voices, the voices share these slots. 0 when the model takes no audio references, which does not stop it sending voices."""
    character_voices: bool
    """Whether a mentioned character's voice is sent with its image, unless the request sets `use_character_voices` to false."""


class ArchitectureInputSchema(TypedDict):
    """The request body as JSON Schema (draft 2020-12), defaults folded in."""
    properties: dict[str, dict[str, Any]]
    required: list[str]


class Architecture(TypedDict):
    id: str
    """The architecture id, as used in its endpoint path."""
    name: str
    """The display name."""
    type: Literal["image", "video", "audio"]
    """What the architecture generates."""
    description: str
    """What the model is for and its usage rules."""
    image_inputs: ArchitectureImageInputs
    """The request field for each image role; an absent role is not supported."""
    video_inputs: ArchitectureVideoInputs | None
    """The source-video field, or null when the architecture takes no video."""
    base_config: dict[str, Any]
    """The default config every request starts from."""
    options: dict[str, list[str]]
    """Allowed tokens per adjustable field, across all variants."""
    options_by_model: dict[str, dict[str, list[str]]]
    """Per-variant narrowing of `options`, keyed by `model_id`; empty when variants share the lists."""
    mentions: ArchitectureMentions
    """Which saved characters and references a prompt may mention by `@handle`, per model variant."""
    max_images: int
    """Image inputs, characters, and references per request, which share one budget."""
    max_images_by_model: dict[str, int]
    """Per-variant overrides of `max_images`, keyed by `model_id`; empty when every variant shares it."""
    input_schema: ArchitectureInputSchema
    """The request body as JSON Schema (draft 2020-12), defaults folded in."""
    gems: float
    """The gem price of the default config."""
    generate_url: str
    """The endpoint to submit a generation to."""


class ArchitectureList(TypedDict):
    architectures: list[Architecture]


class AccountGems(TypedDict):
    balance: float
    """Gems available to the account."""


class Account(TypedDict):
    gems: AccountGems


class UploadRequest(TypedDict):
    content_type: Literal["image/jpeg", "image/png", "video/mp4", "video/quicktime", "video/webm", "audio/mpeg", "audio/mp3", "audio/wav", "audio/wave", "audio/x-wav"]
    """The media type of the file you will upload: an image or video for a generate request, or an audio clip for a character voice or an audio reference."""


class UploadTicket(TypedDict):
    upload_url: str
    """PUT the file here."""
    method: Literal["PUT"]
    headers: dict[str, str]
    """Headers the PUT must carry exactly; storage checks them against the signature."""
    url: str
    """The URL the file has once the PUT succeeds. Send it in any media field, or as `voice` or `audio` when creating a character or an audio reference."""
    content_type: str
    """The media type the PUT must declare."""
    max_bytes: int
    """The largest body the upload accepts: 100 MB."""
    upload_url_expires_at: str
    """When `upload_url` stops accepting the PUT."""
    url_expires_at: str
    """When the uploaded file is deleted: 30 days after the ticket."""


class Character(TypedDict):
    id: str
    """The character id, as `DELETE /v1/characters/{character_id}` takes it."""
    handle: str
    """Mention the character in a prompt as `@handle`."""
    name: str
    """The display name."""
    description: str | None
    """Your notes, or null."""
    image_url: str
    """The portrait."""
    voice_url: str | None
    """The processed voice clip, or null for a character without one."""
    visibility: Literal["public", "private"]
    """Characters created through the API are private; publishing happens in the app."""
    created_at: str
    """When it was created."""


class CharacterList(TypedDict):
    data: list[Character]
    """The page, newest first."""
    next_cursor: str | None
    """Send as `cursor` for the next page; null on the last page."""


class CreateCharacterRequest(TypedDict):
    name: str
    """The display name."""
    handle: NotRequired[str]
    """The `@handle` prompts mention it by: 1 to 15 lowercase letters, digits, underscores, or dashes, starting with a letter. Handles such as image1 and image2 are reserved for uploaded images. Derived from the name when omitted. Cannot be changed later."""
    image: str
    """The portrait: an https URL, an upload URL, or a data URL of a JPEG or PNG. Stored permanently with the character."""
    description: NotRequired[str]
    """Optional notes, for your own reference."""
    voice: NotRequired[str]
    """Optional voice clip: an https URL, an upload URL, or a data URL of an MP3 or WAV. Trimmed to 10 seconds and normalized, like a clip uploaded in the app."""


class Reference(TypedDict):
    id: str
    """The reference id, as `DELETE /v1/references/{reference_id}` takes it."""
    handle: str
    """Mention the reference in a prompt as `@handle`."""
    name: str
    """The display name."""
    kind: Literal["object", "location", "pose", "outfit", "audio"]
    """What the reference is."""
    description: str | None
    """Your notes, or null."""
    image_url: str | None
    """The image, for the four image kinds; null for an audio reference."""
    audio_url: str | None
    """The processed clip, for `kind: "audio"`; null otherwise."""
    created_at: str
    """When it was created."""


class ReferenceList(TypedDict):
    data: list[Reference]
    """The page, newest first."""
    next_cursor: str | None
    """Send as `cursor` for the next page; null on the last page."""


class CreateReferenceRequest(TypedDict):
    name: str
    """The display name."""
    handle: NotRequired[str]
    """The `@handle` prompts mention it by: 1 to 15 lowercase letters, digits, underscores, or dashes, starting with a letter. Handles such as image1 and image2 are reserved for uploaded images. Derived from the name when omitted. Cannot be changed later."""
    kind: Literal["object", "location", "pose", "outfit", "audio"]
    """What the reference is. The four image kinds take `image`; `audio` takes `audio`."""
    image: NotRequired[str]
    """The image, for the four image kinds: an https URL, an upload URL, or a data URL of a JPEG or PNG. Stored permanently with the reference."""
    audio: NotRequired[str]
    """The clip, for `kind: "audio"`: an https URL, an upload URL, or a data URL of an MP3 or WAV. Trimmed to 15 seconds and normalized, like a clip uploaded in the app."""
    description: NotRequired[str]
    """Optional notes, for your own reference."""


class AnimaConfig(TypedDict):
    """A partial config for Anima. Sent to `POST /v1/anima/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["anima-v1"]]
    """The model variant to generate with. Default: `"anima-v1"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1k", "2k"]]
    """Output resolution token. Default: `"1k"`."""
    scheduler: NotRequired[str]
    """Default: `"euler"`."""
    shift: NotRequired[float]
    """Default: `3`."""
    prompt_weighting: NotRequired[bool]
    """Default: `true`."""
    num_inference_steps: NotRequired[float]
    """Default: `30`."""
    guidance_scale: NotRequired[float]
    """Default: `5`."""


class ChromaConfig(TypedDict):
    """A partial config for Chroma. Sent to `POST /v1/chroma/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["chroma-v1-hd"]]
    """The model variant to generate with. Default: `"chroma-v1-hd"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    num_inference_steps: NotRequired[float]
    """Default: `40`."""
    guidance_scale: NotRequired[float]
    """Default: `3`."""


class Flux2Config(TypedDict):
    """A partial config for Flux 2. Sent to `POST /v1/flux2/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["flux2-dev"]]
    """The model variant to generate with. Default: `"flux2-dev"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1k", "2k"]]
    """Output resolution token. Default: `"1k"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    num_inference_steps: NotRequired[float]
    """Default: `28`."""
    guidance_scale: NotRequired[float]
    """Default: `4`."""


class GptImage2Config(TypedDict):
    """A partial config for GPT Image 2. Sent to `POST /v1/gpt_image_2/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["gpt-image-2", "gpt-image-2.5-flare", "gpt-image-2.5-sunburst"]]
    """The model variant to generate with. Default: `"gpt-image-2"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1K", "2K"]]
    """Output resolution token. Default: `"1K"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    quality: NotRequired[str]
    """Default: `"low"`."""


class GrokImageConfig(TypedDict):
    """A partial config for Grok Image. Sent to `POST /v1/grok_image/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["grok-imagine-image", "grok-imagine-image-quality", "grok-imagine-image-2.0"]]
    """The model variant to generate with. Default: `"grok-imagine-image-quality"`."""
    aspect_ratio: NotRequired[Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20"]]
    """Aspect ratio as `W:H`. Default: `"1:1"`."""
    resolution: NotRequired[Literal["1k", "2k"]]
    """Output resolution token. Default: `"1k"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    quality: NotRequired[str]
    """Default: `"medium"`."""


class GuavaConfig(TypedDict):
    """A partial config for Guava. Sent to `POST /v1/guava/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["guava", "guava-pro", "guava-pro-v1-5", "guava-2", "guava-2-pro"]]
    """The model variant to generate with. Default: `"guava"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1K", "2K"]]
    """Output resolution token. Default: `"1K"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    prompt_extend: NotRequired[bool]
    """Default: `false`."""


class HidreamConfig(TypedDict):
    """A partial config for HiDream. Sent to `POST /v1/hidream/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["hidream-fast"]]
    """The model variant to generate with. Default: `"hidream-fast"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `16`."""
    guidance_scale: NotRequired[float]
    """Default: `0`."""


class Krea2Config(TypedDict):
    """A partial config for Krea 2. Sent to `POST /v1/krea_2/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["krea-2-turbo"]]
    """The model variant to generate with. Default: `"krea-2-turbo"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1k", "2k"]]
    """Output resolution token. Default: `"1k"`."""
    scheduler: NotRequired[str]
    """Default: `"euler"`."""
    num_inference_steps: NotRequired[float]
    """Default: `8`."""
    guidance_scale: NotRequired[float]
    """Default: `0`."""


class MangoConfig(TypedDict):
    """A partial config for Mango. Sent to `POST /v1/mango/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["mango", "mango-v2", "mango-v3s", "mango-v3", "mango-v3-turbo"]]
    """The model variant to generate with. Default: `"mango-v3"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1K", "2K", "3K", "4K"]]
    """Output resolution token. Default: `"2K"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""


class NanoBananaV2Config(TypedDict):
    """A partial config for Nano Banana 2. Sent to `POST /v1/nano_banana_v2/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["nano-banana-v2"]]
    """The model variant to generate with. Default: `"nano-banana-v2"`."""
    aspect_ratio: NotRequired[Literal["1:1", "3:2", "2:3", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"]]
    """Aspect ratio as `W:H`. Default: `"1:1"`."""
    resolution: NotRequired[Literal["512", "1K", "2K", "4K"]]
    """Output resolution token. Default: `"512"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    thinking_level: NotRequired[str]
    """Default: `"minimal"`."""
    web_search: NotRequired[bool]
    """Default: `false`."""
    image_search: NotRequired[bool]
    """Default: `false`."""


class SdxlPlusConfig(TypedDict):
    """A partial config for SDXL Plus. Sent to `POST /v1/sdxl_plus/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"]]
    """The model variant to generate with. Default: `"6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `50`."""
    guidance_scale: NotRequired[float]
    """Default: `5`."""
    scheduler: NotRequired[str]
    """Default: `"euler"`."""
    prompt_embed_version: NotRequired[str]
    """Default: `"v1"`."""
    hires: NotRequired[bool]
    """Default: `true`."""
    hires_strength: NotRequired[float]
    """Default: `0.5`."""
    adetailer_face: NotRequired[bool]
    """Default: `true`."""
    adetailer_face_strength: NotRequired[float]
    """Default: `0.4`."""
    adetailer_face_blur: NotRequired[float]
    """Default: `4`."""
    adetailer_face_dilation: NotRequired[float]
    """Default: `4`."""
    adetailer_hands: NotRequired[bool]
    """Default: `true`."""
    adetailer_hands_strength: NotRequired[float]
    """Default: `0.4`."""
    adetailer_hands_blur: NotRequired[float]
    """Default: `4`."""
    adetailer_hands_dilation: NotRequired[float]
    """Default: `4`."""


class StableDiffusionV15Config(TypedDict):
    """A partial config for Stable Diffusion v1.5. Sent to `POST /v1/stable_diffusion_v15/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["15012C538F503CE2EBFC2C8547B268C75CCDAFF7A281DB55399940FF1D70E21D"]]
    """The model variant to generate with. Default: `"15012C538F503CE2EBFC2C8547B268C75CCDAFF7A281DB55399940FF1D70E21D"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `20`."""
    guidance_scale: NotRequired[float]
    """Default: `7.5`."""
    scheduler: NotRequired[str]
    """Default: `"kdpm2_karras"`."""


class StableDiffusionV35LargeConfig(TypedDict):
    """A partial config for Stable Diffusion v3.5 Large. Sent to `POST /v1/stable_diffusion_v35_large/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["sd-3-5-large"]]
    """The model variant to generate with. Default: `"sd-3-5-large"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `28`."""
    guidance_scale: NotRequired[float]
    """Default: `7.5`."""


class StableDiffusionXlConfig(TypedDict):
    """A partial config for Stable Diffusion XL. Sent to `POST /v1/stable_diffusion_xl/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"]]
    """The model variant to generate with. Default: `"6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `30`."""
    guidance_scale: NotRequired[float]
    """Default: `7`."""
    prompt_embed_version: NotRequired[str]
    """Default: `"v1"`."""


class ZImageConfig(TypedDict):
    """A partial config for Z-Image. Sent to `POST /v1/z_image/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["z-image-turbo"]]
    """The model variant to generate with. Default: `"z-image-turbo"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"4:5"`."""
    resolution: NotRequired[Literal["1k", "2k"]]
    """Output resolution token. Default: `"1k"`."""
    num_inference_steps: NotRequired[float]
    """Default: `9`."""
    guidance_scale: NotRequired[float]
    """Default: `0`."""


class BerryConfig(TypedDict):
    """A partial config for Berry. Sent to `POST /v1/berry/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["berry", "berry-2"]]
    """The model variant to generate with. Default: `"berry-2"`."""
    aspect_ratio: NotRequired[Literal["16:9", "9:16", "1:1", "4:3", "3:4", "4:5", "5:4"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["720p", "1080p", "480p"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"3"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    video: NotRequired[str]
    """The source video. An https URL or a data URL."""


class BlueberryConfig(TypedDict):
    """A partial config for Blueberry. Sent to `POST /v1/blueberry/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["blueberry", "blueberry-v2"]]
    """The model variant to generate with. Default: `"blueberry-v2"`."""
    aspect_ratio: NotRequired[Literal["16:9", "4:3", "1:1", "3:4", "9:16"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["720p", "1080p"]]
    """Output resolution token. Default: `"720p"`."""
    duration: NotRequired[Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"4"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image. An https URL or a data URL."""
    shot_type: NotRequired[str]
    """Default: `"single"`."""
    prompt_extend: NotRequired[bool]
    """Default: `false`."""
    audio: NotRequired[bool]
    """Default: `true`."""


class CherryConfig(TypedDict):
    """A partial config for Cherry. Sent to `POST /v1/cherry/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["cherry-mini", "cherry", "cherry-pro", "cherry-2-pro"]]
    """The model variant to generate with. Default: `"cherry-2-pro"`."""
    aspect_ratio: NotRequired[Literal["16:9", "9:16", "1:1"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["480p", "720p", "1080p", "4k"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["4", "5", "8", "10", "15", "20", "25", "30"]]
    """Clip length in seconds, as a token. Default: `"4"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    videos: NotRequired[list[str]]
    """The source videos. Each an https URL or a data URL."""
    use_character_voices: NotRequired[bool]
    """Default: `true`."""


class GrokVideoConfig(TypedDict):
    """A partial config for Grok Video. Sent to `POST /v1/grok_video/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["grok-imagine-video"]]
    """The model variant to generate with. Default: `"grok-imagine-video"`."""
    aspect_ratio: NotRequired[Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["480p", "720p"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    video: NotRequired[str]
    """The source video. An https URL or a data URL."""


class KiwiConfig(TypedDict):
    """A partial config for Kiwi. Sent to `POST /v1/kiwi/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["kiwi"]]
    """The model variant to generate with. Default: `"kiwi"`."""
    aspect_ratio: NotRequired[Literal["16:9", "4:3", "1:1", "3:4", "9:16"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["480p", "720p", "1080p"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["5", "10"]]
    """Clip length in seconds, as a token. Default: `"5"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""


class LemonConfig(TypedDict):
    """A partial config for Lemon. Sent to `POST /v1/lemon/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["lemon"]]
    """The model variant to generate with. Default: `"lemon"`."""
    aspect_ratio: NotRequired[Literal["16:9", "4:3", "1:1", "3:4", "9:16"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["480p", "720p", "1080p"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]]
    """Clip length in seconds, as a token. Default: `"3"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    videos: NotRequired[list[str]]
    """The source videos. Each an https URL or a data URL."""
    audio: NotRequired[bool]
    """Default: `true`."""
    prompt_extend: NotRequired[bool]
    """Default: `false`."""
    use_character_voices: NotRequired[bool]
    """Default: `true`."""


class LtxVideoConfig(TypedDict):
    """A partial config for LTX Video. Sent to `POST /v1/ltx_video/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["ltx-video-096-distilled", "ltx-video-096-dev"]]
    """The model variant to generate with. Default: `"ltx-video-096-distilled"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"3:2"`."""
    resolution: NotRequired[Literal["240p", "360p", "480p", "720p"]]
    """Output resolution token. Default: `"480p"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `"worst quality, inconsistent motion, blurry, jittery, distorted"`."""
    num_inference_steps: NotRequired[float]
    """Default: `8`."""
    guidance_scale: NotRequired[float]
    """Default: `3`."""
    decode_timestep: NotRequired[float]
    """Default: `0.05`."""
    decode_noise_scale: NotRequired[float]
    """Default: `0.025`."""
    prompt_enhance: NotRequired[bool]
    """Default: `true`."""


class MelonConfig(TypedDict):
    """A partial config for Melon. Sent to `POST /v1/melon/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["melon", "melon-pro"]]
    """The model variant to generate with. Default: `"melon"`."""
    aspect_ratio: NotRequired[Literal["16:9", "9:16", "1:1", "3:4", "4:3"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["540p", "720p", "1080p"]]
    """Output resolution token. Default: `"540p"`."""
    duration: NotRequired[Literal["3", "4", "5", "6", "8", "10", "16"]]
    """Clip length in seconds, as a token. Default: `"4"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    generate_audio: NotRequired[bool]
    """Default: `false`."""


class MinimaxH3Config(TypedDict):
    """A partial config for MiniMax-H3. Sent to `POST /v1/minimax_h3/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["minimax-h3-turbo", "minimax-h3"]]
    """The model variant to generate with. Default: `"minimax-h3-turbo"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["480p", "544p", "720p", "768p"]]
    """Output resolution token. Default: `"480p"`."""
    duration: NotRequired[Literal["5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"5"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    videos: NotRequired[list[str]]
    """The source videos. Each an https URL or a data URL."""
    use_character_voices: NotRequired[bool]
    """Default: `true`."""


class PlumConfig(TypedDict):
    """A partial config for Plum. Sent to `POST /v1/plum/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["plum", "plum-max"]]
    """The model variant to generate with. Default: `"plum-max"`."""
    aspect_ratio: NotRequired[Literal["16:9", "9:16", "1:1", "4:3", "3:4", "21:9"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["768P", "2K", "480P"]]
    """Output resolution token. Default: `"480P"`."""
    duration: NotRequired[Literal["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"5"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    last_image: NotRequired[str]
    """The last frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    videos: NotRequired[list[str]]
    """The source videos. Each an https URL or a data URL."""
    use_character_voices: NotRequired[bool]
    """Default: `true`."""


class RaspberryConfig(TypedDict):
    """A partial config for Raspberry. Sent to `POST /v1/raspberry/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["raspberry"]]
    """The model variant to generate with. Default: `"raspberry"`."""
    aspect_ratio: NotRequired[Literal["16:9", "4:3", "1:1", "3:4", "9:16"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["720p", "1080p"]]
    """Output resolution token. Default: `"720p"`."""
    duration: NotRequired[Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
    """Clip length in seconds, as a token. Default: `"4"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    additional_images: NotRequired[list[str]]
    """Additional reference images. Each an https URL or a data URL."""
    use_character_voices: NotRequired[bool]
    """Default: `true`."""


class Wan22Config(TypedDict):
    """A partial config for Wan Video v2.2. Sent to `POST /v1/wan_22/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["wan22-video", "wan22-video-lightning"]]
    """The model variant to generate with. Default: `"wan22-video"`."""
    aspect_ratio: NotRequired[Literal["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]]
    """Aspect ratio as `W:H`. Default: `"16:9"`."""
    resolution: NotRequired[Literal["240p", "360p", "480p", "720p"]]
    """Output resolution token. Default: `"240p"`."""
    first_image: NotRequired[str]
    """The first frame image. An https URL or a data URL."""
    negative_prompt: NotRequired[str]
    """Default: `""`."""
    num_inference_steps: NotRequired[float]
    """Default: `15`."""
    guidance_scale: NotRequired[float]
    """Default: `4`."""
    flow_shift: NotRequired[float]
    """Default: `12`."""
    num_frames: NotRequired[float]
    """Default: `81`."""


class SeedAudioConfig(TypedDict):
    """A partial config for Seed Audio. Sent to `POST /v1/seed_audio/generate`."""
    prompt: str
    """The text prompt."""
    seed: NotRequired[int | None]
    """Integer seed for reproducible output; omit or send null for a random seed."""
    model_id: NotRequired[Literal["seed-audio-1.0"]]
    """The model variant to generate with. Default: `"seed-audio-1.0"`."""
    duration: NotRequired[Literal["5", "10", "30", "60", "120"]]
    """Clip length in seconds, as a token. Default: `"5"`."""
    image: NotRequired[str]
    """The reference image. An https URL or a data URL."""
    sample_rate: NotRequired[float]
    """Default: `48000`."""
    speech_rate: NotRequired[float]
    """Default: `0`."""
    loudness_rate: NotRequired[float]
    """Default: `0`."""
    pitch_rate: NotRequired[float]
    """Default: `0`."""


class ArchitectureInfo(TypedDict):
    """An architecture's name, output type, and request-body JSON Schema."""
    name: str
    type: Literal["image", "video", "audio"]
    schema: dict[str, Any]


ARCHITECTURES: dict[str, ArchitectureInfo] = {
    "anima": {
        "name": "Anima",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["anima-v1"],
                    "description": "The model variant to generate with.",
                    "default": "anima-v1",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1k", "2k"],
                    "description": "Output resolution token.",
                    "default": "1k",
                },
                "scheduler": {
                    "type": "string",
                    "default": "euler",
                },
                "shift": {
                    "type": "number",
                    "default": 3,
                },
                "prompt_weighting": {
                    "type": "boolean",
                    "default": True,
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 30,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 5,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "chroma": {
        "name": "Chroma",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["chroma-v1-hd"],
                    "description": "The model variant to generate with.",
                    "default": "chroma-v1-hd",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 40,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 3,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "flux2": {
        "name": "Flux 2",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["flux2-dev"],
                    "description": "The model variant to generate with.",
                    "default": "flux2-dev",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1k", "2k"],
                    "description": "Output resolution token.",
                    "default": "1k",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 28,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 4,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "gpt_image_2": {
        "name": "GPT Image 2",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["gpt-image-2", "gpt-image-2.5-flare", "gpt-image-2.5-sunburst"],
                    "description": "The model variant to generate with.",
                    "default": "gpt-image-2",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1K", "2K"],
                    "description": "Output resolution token.",
                    "default": "1K",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "quality": {
                    "type": "string",
                    "default": "low",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "grok_image": {
        "name": "Grok Image",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["grok-imagine-image", "grok-imagine-image-quality", "grok-imagine-image-2.0"],
                    "description": "The model variant to generate with.",
                    "default": "grok-imagine-image-quality",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "2:1", "1:2", "19.5:9", "9:19.5", "20:9", "9:20"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "1:1",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1k", "2k"],
                    "description": "Output resolution token.",
                    "default": "1k",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "quality": {
                    "type": "string",
                    "default": "medium",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "guava": {
        "name": "Guava",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["guava", "guava-pro", "guava-pro-v1-5", "guava-2", "guava-2-pro"],
                    "description": "The model variant to generate with.",
                    "default": "guava",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1K", "2K"],
                    "description": "Output resolution token.",
                    "default": "1K",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "prompt_extend": {
                    "type": "boolean",
                    "default": False,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "hidream": {
        "name": "HiDream",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["hidream-fast"],
                    "description": "The model variant to generate with.",
                    "default": "hidream-fast",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 16,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 0,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "krea_2": {
        "name": "Krea 2",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["krea-2-turbo"],
                    "description": "The model variant to generate with.",
                    "default": "krea-2-turbo",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1k", "2k"],
                    "description": "Output resolution token.",
                    "default": "1k",
                },
                "scheduler": {
                    "type": "string",
                    "default": "euler",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 8,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 0,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "mango": {
        "name": "Mango",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["mango", "mango-v2", "mango-v3s", "mango-v3", "mango-v3-turbo"],
                    "description": "The model variant to generate with.",
                    "default": "mango-v3",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1K", "2K", "3K", "4K"],
                    "description": "Output resolution token.",
                    "default": "2K",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "nano_banana_v2": {
        "name": "Nano Banana 2",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["nano-banana-v2"],
                    "description": "The model variant to generate with.",
                    "default": "nano-banana-v2",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["1:1", "3:2", "2:3", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "1:1",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["512", "1K", "2K", "4K"],
                    "description": "Output resolution token.",
                    "default": "512",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "thinking_level": {
                    "type": "string",
                    "default": "minimal",
                },
                "web_search": {
                    "type": "boolean",
                    "default": False,
                },
                "image_search": {
                    "type": "boolean",
                    "default": False,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "sdxl_plus": {
        "name": "SDXL Plus",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"],
                    "description": "The model variant to generate with.",
                    "default": "6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 50,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 5,
                },
                "scheduler": {
                    "type": "string",
                    "default": "euler",
                },
                "prompt_embed_version": {
                    "type": "string",
                    "default": "v1",
                },
                "hires": {
                    "type": "boolean",
                    "default": True,
                },
                "hires_strength": {
                    "type": "number",
                    "default": 0.5,
                },
                "adetailer_face": {
                    "type": "boolean",
                    "default": True,
                },
                "adetailer_face_strength": {
                    "type": "number",
                    "default": 0.4,
                },
                "adetailer_face_blur": {
                    "type": "number",
                    "default": 4,
                },
                "adetailer_face_dilation": {
                    "type": "number",
                    "default": 4,
                },
                "adetailer_hands": {
                    "type": "boolean",
                    "default": True,
                },
                "adetailer_hands_strength": {
                    "type": "number",
                    "default": 0.4,
                },
                "adetailer_hands_blur": {
                    "type": "number",
                    "default": 4,
                },
                "adetailer_hands_dilation": {
                    "type": "number",
                    "default": 4,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "stable_diffusion_v15": {
        "name": "Stable Diffusion v1.5",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["15012C538F503CE2EBFC2C8547B268C75CCDAFF7A281DB55399940FF1D70E21D"],
                    "description": "The model variant to generate with.",
                    "default": "15012C538F503CE2EBFC2C8547B268C75CCDAFF7A281DB55399940FF1D70E21D",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 20,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 7.5,
                },
                "scheduler": {
                    "type": "string",
                    "default": "kdpm2_karras",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "stable_diffusion_v35_large": {
        "name": "Stable Diffusion v3.5 Large",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["sd-3-5-large"],
                    "description": "The model variant to generate with.",
                    "default": "sd-3-5-large",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 28,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 7.5,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "stable_diffusion_xl": {
        "name": "Stable Diffusion XL",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80"],
                    "description": "The model variant to generate with.",
                    "default": "6A35A7855770AE9820A3C931D4964C3817B6D9E3C6F9C4DABB5B3A94E5643B80",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 30,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 7,
                },
                "prompt_embed_version": {
                    "type": "string",
                    "default": "v1",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "z_image": {
        "name": "Z-Image",
        "type": "image",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["z-image-turbo"],
                    "description": "The model variant to generate with.",
                    "default": "z-image-turbo",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "4:5",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["1k", "2k"],
                    "description": "Output resolution token.",
                    "default": "1k",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 9,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 0,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "berry": {
        "name": "Berry",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["berry", "berry-2"],
                    "description": "The model variant to generate with.",
                    "default": "berry-2",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1", "4:3", "3:4", "4:5", "5:4"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["720p", "1080p", "480p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "3",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "video": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The source video. An https URL or a data URL.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "blueberry": {
        "name": "Blueberry",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["blueberry", "blueberry-v2"],
                    "description": "The model variant to generate with.",
                    "default": "blueberry-v2",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["720p", "1080p"],
                    "description": "Output resolution token.",
                    "default": "720p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "4",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "last_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The last frame image. An https URL or a data URL.",
                },
                "shot_type": {
                    "type": "string",
                    "default": "single",
                },
                "prompt_extend": {
                    "type": "boolean",
                    "default": False,
                },
                "audio": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "cherry": {
        "name": "Cherry",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["cherry-mini", "cherry", "cherry-pro", "cherry-2-pro"],
                    "description": "The model variant to generate with.",
                    "default": "cherry-2-pro",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["480p", "720p", "1080p", "4k"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["4", "5", "8", "10", "15", "20", "25", "30"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "4",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "videos": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "The source videos. Each an https URL or a data URL.",
                },
                "use_character_voices": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "grok_video": {
        "name": "Grok Video",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["grok-imagine-video"],
                    "description": "The model variant to generate with.",
                    "default": "grok-imagine-video",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["480p", "720p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "video": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The source video. An https URL or a data URL.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "kiwi": {
        "name": "Kiwi",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["kiwi"],
                    "description": "The model variant to generate with.",
                    "default": "kiwi",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["480p", "720p", "1080p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["5", "10"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "5",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "lemon": {
        "name": "Lemon",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["lemon"],
                    "description": "The model variant to generate with.",
                    "default": "lemon",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["480p", "720p", "1080p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "3",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "last_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The last frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "videos": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "The source videos. Each an https URL or a data URL.",
                },
                "audio": {
                    "type": "boolean",
                    "default": True,
                },
                "prompt_extend": {
                    "type": "boolean",
                    "default": False,
                },
                "use_character_voices": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "ltx_video": {
        "name": "LTX Video",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["ltx-video-096-distilled", "ltx-video-096-dev"],
                    "description": "The model variant to generate with.",
                    "default": "ltx-video-096-distilled",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "3:2",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["240p", "360p", "480p", "720p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "worst quality, inconsistent motion, blurry, jittery, distorted",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 8,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 3,
                },
                "decode_timestep": {
                    "type": "number",
                    "default": 0.05,
                },
                "decode_noise_scale": {
                    "type": "number",
                    "default": 0.025,
                },
                "prompt_enhance": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "melon": {
        "name": "Melon",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["melon", "melon-pro"],
                    "description": "The model variant to generate with.",
                    "default": "melon",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1", "3:4", "4:3"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["540p", "720p", "1080p"],
                    "description": "Output resolution token.",
                    "default": "540p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["3", "4", "5", "6", "8", "10", "16"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "4",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "last_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The last frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "generate_audio": {
                    "type": "boolean",
                    "default": False,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "minimax_h3": {
        "name": "MiniMax-H3",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["minimax-h3-turbo", "minimax-h3"],
                    "description": "The model variant to generate with.",
                    "default": "minimax-h3-turbo",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["480p", "544p", "720p", "768p"],
                    "description": "Output resolution token.",
                    "default": "480p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "5",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "last_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The last frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "videos": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "The source videos. Each an https URL or a data URL.",
                },
                "use_character_voices": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "plum": {
        "name": "Plum",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["plum", "plum-max"],
                    "description": "The model variant to generate with.",
                    "default": "plum-max",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "9:16", "1:1", "4:3", "3:4", "21:9"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["768P", "2K", "480P"],
                    "description": "Output resolution token.",
                    "default": "480P",
                },
                "duration": {
                    "type": "string",
                    "enum": ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "5",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "last_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The last frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "videos": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "The source videos. Each an https URL or a data URL.",
                },
                "use_character_voices": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "raspberry": {
        "name": "Raspberry",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["raspberry"],
                    "description": "The model variant to generate with.",
                    "default": "raspberry",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["720p", "1080p"],
                    "description": "Output resolution token.",
                    "default": "720p",
                },
                "duration": {
                    "type": "string",
                    "enum": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "4",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "additional_images": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "uri",
                            },
                            {
                                "type": "string",
                                "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                            },
                        ],
                    },
                    "description": "Additional reference images. Each an https URL or a data URL.",
                },
                "use_character_voices": {
                    "type": "boolean",
                    "default": True,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "wan_22": {
        "name": "Wan Video v2.2",
        "type": "video",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["wan22-video", "wan22-video-lightning"],
                    "description": "The model variant to generate with.",
                    "default": "wan22-video",
                },
                "aspect_ratio": {
                    "type": "string",
                    "enum": ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"],
                    "description": "Aspect ratio as `W:H`.",
                    "default": "16:9",
                },
                "resolution": {
                    "type": "string",
                    "enum": ["240p", "360p", "480p", "720p"],
                    "description": "Output resolution token.",
                    "default": "240p",
                },
                "first_image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The first frame image. An https URL or a data URL.",
                },
                "negative_prompt": {
                    "type": "string",
                    "default": "",
                },
                "num_inference_steps": {
                    "type": "number",
                    "default": 15,
                },
                "guidance_scale": {
                    "type": "number",
                    "default": 4,
                },
                "flow_shift": {
                    "type": "number",
                    "default": 12,
                },
                "num_frames": {
                    "type": "number",
                    "default": 81,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
    "seed_audio": {
        "name": "Seed Audio",
        "type": "audio",
        "schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "minLength": 1,
                    "description": "The text prompt.",
                },
                "seed": {
                    "anyOf": [
                        {
                            "type": "integer",
                        },
                        {
                            "type": "null",
                        },
                    ],
                    "description": "Integer seed for reproducible output; omit or send null for a random seed.",
                },
                "model_id": {
                    "type": "string",
                    "enum": ["seed-audio-1.0"],
                    "description": "The model variant to generate with.",
                    "default": "seed-audio-1.0",
                },
                "duration": {
                    "type": "string",
                    "enum": ["5", "10", "30", "60", "120"],
                    "description": "Clip length in seconds, as a token.",
                    "default": "5",
                },
                "image": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "uri",
                        },
                        {
                            "type": "string",
                            "pattern": "^data:[^;,]+(?:;[^;,]+)*;base64,",
                        },
                    ],
                    "description": "The reference image. An https URL or a data URL.",
                },
                "sample_rate": {
                    "type": "number",
                    "default": 48000,
                },
                "speech_rate": {
                    "type": "number",
                    "default": 0,
                },
                "loudness_rate": {
                    "type": "number",
                    "default": 0,
                },
                "pitch_rate": {
                    "type": "number",
                    "default": 0,
                },
            },
            "required": ["prompt"],
            "additionalProperties": True,
        },
    },
}
"""Every architecture in the spec this SDK was generated from, by id."""
