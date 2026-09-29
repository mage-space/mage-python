from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any, Literal

import pytest
from typing_extensions import get_type_hints

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("generate", ROOT / "scripts" / "generate.py")
assert _spec is not None and _spec.loader is not None
generate = importlib.util.module_from_spec(_spec)
sys.modules["generate"] = generate
_spec.loader.exec_module(generate)

CODES = ["unauthorized", "not_found"]
THING = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "detail": {
            "anyOf": [
                {"type": "object", "properties": {"n": {"type": "integer"}}, "required": ["n"]},
                {"type": "null"},
            ]
        },
        "tags": {
            "type": "object",
            "additionalProperties": {"type": "array", "items": {"type": "string"}},
        },
    },
    "required": ["id", "detail", "tags"],
}


def spec_with(**config_properties: Any) -> dict[str, Any]:
    body = {
        "description": "A partial config for Foo Bar.",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {"prompt": {"type": "string"}, **config_properties},
                    "required": ["prompt"],
                    "additionalProperties": True,
                }
            }
        },
    }
    return {
        "paths": {
            "/v1/{architecture}/generate": {"post": {"tags": ["Requests"], "requestBody": body}},
            "/v1/foo_bar/generate": {
                "post": {"summary": "Foo Bar", "tags": ["Video models"], "requestBody": body}
            },
        },
        "components": {
            "schemas": {
                "Request": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "anyOf": [
                                {
                                    "type": "object",
                                    "properties": {"code": {"type": "string", "enum": CODES}},
                                    "required": ["code"],
                                },
                                {"type": "null"},
                            ]
                        }
                    },
                    "required": ["error"],
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {
                            "type": "object",
                            "properties": {"code": {"type": "string", "enum": CODES}},
                            "required": ["code"],
                        }
                    },
                    "required": ["error"],
                },
                "ThingList": {
                    "type": "object",
                    "properties": {"data": {"type": "array", "items": THING}},
                },
                "Thing": THING,
            }
        },
    }


def load(spec: dict[str, Any]) -> dict[str, Any]:
    module = types.ModuleType("generated_under_test")
    sys.modules[module.__name__] = module
    exec(
        compile(generate.Generator(spec).render(), "_generated.py", "exec", dont_inherit=True),
        module.__dict__,
    )
    return module.__dict__


def test_generates_a_config_per_architecture_and_the_catalog() -> None:
    spec = spec_with(duration={"type": "string", "enum": ["5", "10"], "default": "5"})
    ns = load(spec)

    config = ns["FooBarConfig"]
    assert config.__required_keys__ == {"prompt"}
    assert config.__optional_keys__ == {"duration"}
    assert get_type_hints(config)["duration"] == Literal["5", "10"]
    assert ns["ArchitectureId"].__args__ == ("foo_bar",)
    schema = spec["paths"]["/v1/foo_bar/generate"]["post"]["requestBody"]["content"][
        "application/json"
    ]["schema"]
    assert ns["ARCHITECTURES"] == {
        "foo_bar": {"name": "Foo Bar", "type": "video", "schema": schema}
    }


def test_names_nested_types_and_reuses_components() -> None:
    ns = load(spec_with())

    thing = ns["Thing"]
    assert get_type_hints(ns["ThingList"])["data"] == list[thing]
    thing_hints = get_type_hints(ns["Thing"])
    assert thing_hints["detail"] == ns["ThingDetail"] | None
    assert thing_hints["tags"] == dict[str, list[str]]
    assert "GenerationRequest" in ns and "ErrorBody" in ns


def test_error_codes_are_open_strings_with_a_literal_alias() -> None:
    ns = load(spec_with())

    assert get_type_hints(ns["ErrorBodyError"])["code"] is str
    assert get_type_hints(ns["GenerationRequestError"])["code"] is str
    assert ns["ErrorCode"].__args__ == tuple(CODES)


def test_properties_that_are_not_identifiers_use_the_functional_syntax() -> None:
    ns = load(spec_with(**{"class": {"type": "boolean"}, "top-k": {"type": "integer"}}))

    hints = get_type_hints(ns["FooBarConfig"])
    assert hints["prompt"] is str
    assert "class" in hints and "top-k" in hints


def test_unsupported_schemas_stop_generation() -> None:
    with pytest.raises(SystemExit, match="Unsupported"):
        load(spec_with(weird={"not": {"type": "string"}}))


def test_output_is_deterministic() -> None:
    spec = json.loads((ROOT / "spec" / "openapi.json").read_text())
    assert generate.Generator(spec).render() == generate.Generator(spec).render()
