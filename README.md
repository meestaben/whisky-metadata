

# Whisky Metadata Standards

This repository contains an **Alpha-stage** set of structured whisky metadata taxonomies intended to support digital cask workflows, delivery order interoperability, and malt whisky-related applications. The project is under active development and **should not be used in production**. Until version 1.0, all formats, schemas, and identifiers may change.

## Repository Structure

```
whisky-metadata/
├── src/reference/        # Canonical hand-edited metadata (source of truth)
├── src/schema/           # JSON schema files (currently draft-2020-12)
├── tools/                # Validation and build scripts
└── dist/                 # Build output
```

## Published Data (GitHub Pages)

Build artefacts are automatically published on tagged releases.

### Latest build

```
https://meestaben.github.io/whisky-metadata/latest/json/<file>.json
https://meestaben.github.io/whisky-metadata/latest/csv/<file>.csv
https://meestaben.github.io/whisky-metadata/latest/xml/<file>.xml
```

### Versioned builds

```
https://meestaben.github.io/whisky-metadata/vX.Y.Z/json/<file>.json
https://meestaben.github.io/whisky-metadata/vX.Y.Z/csv/<file>.csv
https://meestaben.github.io/whisky-metadata/vX.Y.Z/xml/<file>.xml
```

Do not rely on these for production systems. Version numbers below 1.0 indicate unstable formats and semantics.

## Usage

### Fetch directly over HTTP

```bash
curl -L https://meestaben.github.io/whisky-metadata/latest/json/distilleries.json
```

JavaScript:

```js
const url = "https://meestaben.github.io/whisky-metadata/latest/json/distilleries.json";
const data = await fetch(url).then(r => r.json());
```

Python:

```python
import requests
data = requests.get("https://meestaben.github.io/whisky-metadata/latest/json/distilleries.json").json()
```

### Vendor a specific version

```bash
curl -L https://meestaben.github.io/whisky-metadata/v0.1.0/json/distilleries.json \
  -o ./vendor/whisky/distilleries.json
```

### Build locally

```bash
git clone https://github.com/meestaben/whisky-metadata.git
cd whisky-metadata
python -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt
python tools/build.py
```

Outputs will appear under `dist/`.

## Development and CI

Pull requests and changes to `main` run validation through `tools/validate.py`.

Tagged releases (e.g. `v0.1.0`) perform:

1. Validation  
2. Build of CSV, XML, and JSON artefacts  
3. Publication to GitHub Pages under versioned and `latest` paths  

## Status

This project is in **Alpha**. Data structures, schemas, and naming conventions are expected to change. Do not depend on this repository for production use until a stable 1.0 release.