#!/usr/bin/env python3
import json
import csv
import pathlib
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "src" / "reference"
DIST_CSV_DIR = ROOT / "dist" / "csv"
DIST_JSON_DIR = ROOT / "dist" / "json"
DIST_XML_DIR = ROOT / "dist" / "xml"


def load_reference(path: pathlib.Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_meta_keys(entries: List[Dict[str, Any]]) -> List[str]:
    keys = set()
    for entry in entries:
        meta = entry.get("meta") or {}
        keys.update(meta.keys())
    return sorted(keys)


def to_csv(reference_path: pathlib.Path) -> None:
    entries = load_reference(reference_path)
    if not isinstance(entries, list):
        raise ValueError(f"{reference_path} is not a JSON array")

    meta_keys = collect_meta_keys(entries)

    # Core columns: id, label, lifecycle, aliases (as ';'-joined)
    fieldnames = ["id", "label", "lifecycle", "aliases"] + meta_keys

    out_name = reference_path.stem + ".csv"
    out_path = DIST_CSV_DIR / out_name

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            row: Dict[str, Any] = {}

            row["id"] = entry.get("id", "")
            row["label"] = entry.get("label", "")
            row["lifecycle"] = entry.get("lifecycle", "")
            aliases = entry.get("aliases") or []
            if not isinstance(aliases, list):
                aliases = [str(aliases)]
            row["aliases"] = ";".join(str(a) for a in aliases)

            meta = entry.get("meta") or {}
            for key in meta_keys:
                value = meta.get(key)
                # Serialise lists/dicts as JSON strings to avoid losing structure
                if isinstance(value, (list, dict)):
                    row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    row[key] = "" if value is None else value

            writer.writerow(row)

    print(f"✅ Wrote {out_path.relative_to(ROOT)}")


def to_json(reference_path: pathlib.Path) -> None:
    entries = load_reference(reference_path)
    out_path = DIST_JSON_DIR / reference_path.name
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"✅ Wrote {out_path.relative_to(ROOT)}")


def to_xml(reference_path: pathlib.Path) -> None:
    entries = load_reference(reference_path)
    if not isinstance(entries, list):
        raise ValueError(f"{reference_path} is not a JSON array")

    root = ET.Element("reference", {"name": reference_path.stem})

    for entry in entries:
        entry_el = ET.SubElement(root, "entry")

        id_el = ET.SubElement(entry_el, "id")
        id_el.text = str(entry.get("id", ""))

        label_el = ET.SubElement(entry_el, "label")
        label_el.text = str(entry.get("label", ""))

        lifecycle_el = ET.SubElement(entry_el, "lifecycle")
        lifecycle_el.text = str(entry.get("lifecycle", ""))

        aliases_el = ET.SubElement(entry_el, "aliases")
        aliases = entry.get("aliases") or []
        if not isinstance(aliases, list):
            aliases = [str(aliases)]
        for alias in aliases:
            alias_el = ET.SubElement(aliases_el, "alias")
            alias_el.text = str(alias)

        meta_el = ET.SubElement(entry_el, "meta")
        meta = entry.get("meta") or {}
        for key, value in meta.items():
            if value is None:
                continue
            key_el = ET.SubElement(meta_el, key)
            if isinstance(value, (list, dict)):
                key_el.text = json.dumps(value, ensure_ascii=False)
            else:
                key_el.text = str(value)

    tree = ET.ElementTree(root)
    out_path = DIST_XML_DIR / (reference_path.stem + ".xml")
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ Wrote {out_path.relative_to(ROOT)}")


def main() -> None:
    DIST_CSV_DIR.mkdir(parents=True, exist_ok=True)
    DIST_JSON_DIR.mkdir(parents=True, exist_ok=True)
    DIST_XML_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(REFERENCE_DIR.glob("*.json"))
    if not json_files:
        print("No reference JSON files found.")
        return

    for path in json_files:
        to_csv(path)
        to_json(path)
        to_xml(path)


if __name__ == "__main__":
    main()