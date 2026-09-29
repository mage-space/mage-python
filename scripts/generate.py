"""Generate src/mage_space/_generated.py from spec/openapi.json.

Standard library only. The output is deterministic: running this twice leaves no diff.
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "spec" / "openapi.json"
OUT_PATH = ROOT / "src" / "mage_space" / "_generated.py"

HEADER = "# Generated from spec/openapi.json by scripts/generate.py. Do not edit.\n"
GENERATE_PATH = re.compile(r"^/v1/([a-z0-9_]+)/generate$")
RENAMES = {
    "Request": "GenerationRequest",
    "Error": "ErrorBody",
    "GenerateRequest": "GenerateConfig",
}
TAG_TYPES = {"Image models": "image", "Video models": "video", "Audio models": "audio"}

Schema = dict[str, Any]


def pascal(value: str) -> str:
    return "".join(
        part[:1].upper() + part[1:] for part in re.split(r"[^A-Za-z0-9]+", value) if part
    )


def canonical(schema: Any) -> str:
    return json.dumps(schema, sort_keys=True)


def docstring(text: str, indent: str) -> str:
    body = text.strip().replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if "\n" not in body:
        return f'{indent}"""{body}"""\n'
    lines = body.split("\n")
    inner = "\n".join(f"{indent}{line}" if line else "" for line in lines)
    return f'{indent}"""\n{inner}\n{indent}"""\n'


def field_doc(schema: Schema) -> str | None:
    parts = []
    if isinstance(schema.get("description"), str):
        parts.append(schema["description"].strip())
    if "default" in schema:
        parts.append(f"Default: `{json.dumps(schema['default'])}`.")
    return " ".join(parts) or None


def py_literal(value: Any, indent: str = "") -> str:
    """Render JSON as a Python literal, one dict entry per line."""
    if isinstance(value, dict):
        if not value:
            return "{}"
        inner = indent + "    "
        entries = [f"{inner}{json.dumps(k)}: {py_literal(v, inner)}," for k, v in value.items()]
        return "{\n" + "\n".join(entries) + f"\n{indent}}}"
    if isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            return "[" + ", ".join(py_literal(item) for item in value) + "]"
        inner = indent + "    "
        entries = [f"{inner}{py_literal(item, inner)}," for item in value]
        return "[\n" + "\n".join(entries) + f"\n{indent}]"
    if value is True:
        return "True"
    if value is False:
        return "False"
    if value is None:
        return "None"
    return json.dumps(value)


class Generator:
    def __init__(self, spec: Schema) -> None:
        self.spec = spec
        self.components: dict[str, Schema] = spec["components"]["schemas"]
        self.names: dict[str, str] = {name: RENAMES.get(name, name) for name in self.components}
        self.by_shape: dict[str, str] = {
            canonical(schema): name for name, schema in self.components.items()
        }
        error = self.components["Error"]["properties"]["error"]["properties"]["code"]
        self.error_codes: list[str] = error["enum"]
        self.definitions: list[str] = []
        self.defined: dict[str, str] = {}  # python name -> canonical schema
        self.public: list[str] = []

    # Types ---------------------------------------------------------------

    def ensure_component(self, name: str) -> str:
        python_name = self.names[name]
        if python_name not in self.defined:
            self.define_object(python_name, self.components[name])
        return python_name

    def type_expr(self, schema: Schema, hint: str) -> str:
        if "$ref" in schema:
            return self.ensure_component(schema["$ref"].rsplit("/", 1)[-1])
        if "const" in schema:
            return f"Literal[{json.dumps(schema['const'])}]"
        if "enum" in schema:
            if schema["enum"] == self.error_codes:
                return "str"
            return "Literal[" + ", ".join(json.dumps(v) for v in schema["enum"]) + "]"
        if "anyOf" in schema:
            objects = [
                s for s in schema["anyOf"] if s.get("type") == "object" and "properties" in s
            ]
            parts: list[str] = []
            index = 0
            for option in schema["anyOf"]:
                option_hint = hint
                if len(objects) > 1 and option in objects:
                    index += 1
                    option_hint = f"{hint}{index}"
                expr = self.type_expr(option, option_hint)
                if expr not in parts:
                    parts.append(expr)
            if "None" in parts:
                parts.remove("None")
                parts.append("None")
            return " | ".join(parts)
        kind = schema.get("type")
        if kind == "string":
            return "str"
        if kind == "integer":
            return "int"
        if kind == "number":
            return "float"
        if kind == "boolean":
            return "bool"
        if kind == "null":
            return "None"
        if kind == "array":
            return f"list[{self.type_expr(schema['items'], hint + 'Item')}]"
        if kind == "object":
            if "properties" in schema:
                component = self.by_shape.get(canonical(schema))
                if component is not None:
                    return self.ensure_component(component)
                self.define_object(hint, schema)
                return hint
            extra = schema.get("additionalProperties")
            if isinstance(extra, dict):
                return f"dict[str, {self.type_expr(extra, hint + 'Value')}]"
            return "dict[str, Any]"
        raise SystemExit(f"Unsupported schema for {hint}: {json.dumps(schema)[:200]}")

    def define_object(self, name: str, schema: Schema, doc: str | None = None) -> None:
        shape = canonical(schema)
        if name in self.defined:
            if self.defined[name] != shape:
                raise SystemExit(f"Two different schemas want the name {name}")
            return
        self.defined[name] = shape
        required = set(schema.get("required", []))
        fields: list[tuple[str, str, str | None]] = []
        for prop, sub in schema["properties"].items():
            expr = self.type_expr(sub, name + pascal(prop))
            if prop not in required:
                expr = f"NotRequired[{expr}]"
            fields.append((prop, expr, field_doc(sub)))
        doc = doc or schema.get("description")
        if all(prop.isidentifier() and not keyword.iskeyword(prop) for prop, _, _ in fields):
            lines = [f"class {name}(TypedDict):\n"]
            if doc:
                lines.append(docstring(doc, "    "))
            for prop, expr, prop_doc in fields:
                lines.append(f"    {prop}: {expr}\n")
                if prop_doc:
                    lines.append(docstring(prop_doc, "    "))
            if not fields and not doc:
                lines.append("    pass\n")
            definition = "".join(lines)
        else:
            entries = "".join(f"    {json.dumps(prop)}: {expr},\n" for prop, expr, _ in fields)
            definition = (
                f"{name} = TypedDict(\n    {json.dumps(name)},\n    {{\n{entries}    }},\n)\n"
            )
        self.definitions.append(definition)
        self.public.append(name)

    # Architectures ---------------------------------------------------------

    def architectures(self) -> list[tuple[str, str, str, Schema]]:
        found = []
        for path, item in self.spec["paths"].items():
            match = GENERATE_PATH.match(path)
            if not match:
                continue
            operation = item["post"]
            kinds = [TAG_TYPES[tag] for tag in operation.get("tags", []) if tag in TAG_TYPES]
            if len(kinds) != 1:
                raise SystemExit(f"{path} has no single model tag: {operation.get('tags')}")
            body = operation["requestBody"]
            found.append((match.group(1), operation["summary"], kinds[0], body))
        return found

    def render(self) -> str:
        for name in self.components:
            self.ensure_component(name)
        architectures = self.architectures()
        for arch_id, summary, _, body in architectures:
            schema = body["content"]["application/json"]["schema"]
            doc = f"{body.get('description', summary)} Sent to `POST /v1/{arch_id}/generate`."
            self.define_object(pascal(arch_id) + "Config", schema, doc)

        codes = ", ".join(json.dumps(code) for code in self.error_codes)
        ids = ", ".join(json.dumps(arch_id) for arch_id, _, _, _ in architectures)
        catalog = {
            arch_id: {
                "name": summary,
                "type": kind,
                "schema": body["content"]["application/json"]["schema"],
            }
            for arch_id, summary, kind, body in architectures
        }
        extra_public = ["ARCHITECTURES", "ArchitectureId", "ArchitectureInfo", "ErrorCode"]
        public = sorted(self.public + extra_public)

        out = [HEADER, "\n", "from typing import Any\n\n"]
        out.append("from typing_extensions import Literal, NotRequired, TypedDict\n\n")
        out.append("__all__ = [\n" + "".join(f"    {json.dumps(n)},\n" for n in public) + "]\n\n")
        out.append(f"ErrorCode = Literal[{codes}]\n")
        out.append(docstring("Every error code the API documents. New codes may appear.", ""))
        out.append(f"\nArchitectureId = Literal[{ids}]\n")
        out.append(docstring("The architectures this SDK version knows about.", ""))
        for definition in self.definitions:
            out.append("\n\n" + definition)
        out.append("\n\nclass ArchitectureInfo(TypedDict):\n")
        out.append(
            docstring("An architecture's name, output type, and request-body JSON Schema.", "    ")
        )
        out.append("    name: str\n")
        out.append('    type: Literal["image", "video", "audio"]\n')
        out.append("    schema: dict[str, Any]\n")
        out.append(f"\n\nARCHITECTURES: dict[str, ArchitectureInfo] = {py_literal(catalog)}\n")
        out.append(
            docstring("Every architecture in the spec this SDK was generated from, by id.", "")
        )
        return "".join(out)


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    OUT_PATH.write_text(Generator(spec).render(), encoding="utf-8")


if __name__ == "__main__":
    main()
