#!/usr/bin/env python3
import json
import pathlib
import re

# Suggests normalised versions of distillery names and checks for duplicates
# May be extended to cover other data types in future

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "src" / "reference"

NORMALISATION_RULES = [
    (re.compile(r"\s+"), " "),
    (re.compile(r"[’']"), "'"),
    (re.compile(r"[^a-zA-Z0-9' ]"), ""),
]


def clean_name(name: str) -> str:
    name = name.strip()
    for pat, repl in NORMALISATION_RULES:
        name = pat.sub(repl, name)
    return name.title()


def main():
    dist_path = REFERENCE_DIR / "distilleries.json"
    distilleries = json.loads(dist_path.read_text(encoding="utf-8"))
    seen = {}
    errors = False

    for entry in distilleries:
        label = entry["label"]
        canonical = clean_name(label)
        if canonical != label:
            print(f"⚠️  Suggest normalising '{label}' → '{canonical}'")

        if canonical in seen:
            print(f"❌ Duplicate detected: '{canonical}' appears in:")
            print(f"   - {seen[canonical]}")
            print(f"   - {entry['id']}")
            errors = True
        else:
            seen[canonical] = entry["id"]

        for alias in entry.get("aliases", []):
            alias_canon = clean_name(alias)
            if alias_canon == canonical:
                continue
            if alias_canon in seen:
                print(
                    f"⚠️ Alias collision: '{alias}' normalises to same as existing '{canonical}'"
                )

    if errors:
        exit(1)
    else:
        print("✅ Distillery name hygiene looks good.")


if __name__ == "__main__":
    main()
