#!/usr/bin/env python3
import json
import pathlib
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

# validates reference data against the applicable JSON schema

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "src" / "schema"
REFERENCE_DIR = ROOT / "src" / "reference"


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_registry() -> Registry:
    registry = Registry()
    for path in SCHEMA_DIR.glob("*.schema.json"):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if not schema_id:
            raise RuntimeError(f"Schema {path} missing $id")
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def validate_reference_file(ref_path: pathlib.Path, schema_path: pathlib.Path, registry: Registry) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, registry=registry)
    data = load_json(ref_path)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        print(f"❌ {ref_path.relative_to(ROOT)} failed validation:")
        for err in errors:
            loc = "/".join(str(p) for p in err.path)
            print(f"  - at '{loc}': {err.message}")
        raise SystemExit(1)

    print(f"✅ {ref_path.relative_to(ROOT)} is valid against {schema_path.name}")


def main() -> None:
    registry = build_registry()

    mappings = [
        ("regions.json", "regions.schema.json"),
        ("distilleries.json", "distilleries.schema.json"),
        ("cask_types.json", "cask-types.schema.json"),
        ("wood_types.json", "wood-types.schema.json"),
        ("predecessors.json", "predecessors.schema.json"),
        ("fill_types.json", "fill-types.schema.json"),
        ("spirit_types.json", "spirit-types.schema.json"),
    ]

    for ref_name, schema_name in mappings:
        ref_path = REFERENCE_DIR / ref_name
        schema_path = SCHEMA_DIR / schema_name

        if not ref_path.exists():
            print(f"⚠️  Skipping missing reference file {ref_name}")
            continue

        validate_reference_file(ref_path, schema_path, registry)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Validation failed with error: {e}")
        sys.exit(1)
