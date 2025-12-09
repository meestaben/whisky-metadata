# Contributing to Whisky Metadata

This project is currently in **Alpha**. Data structures, identifiers, and schemas are still evolving, and breaking changes may occur at any time. Please do not rely on this project in production systems.

## Principles

- `src/reference/*.json` is the **source of truth**.
- `dist/` is a **generated directory** and must never be committed.
- Every change must pass validation via `tools/validate.py`.
- JSON Schemas must remain consistent with reference data.
- Identifiers should remain stable unless a breaking change is justified.

## How to Contribute

1. Fork this repository.
2. Create a feature or fix branch.
3. Modify files
4. Validate your changes locally:

   ```bash
   python tools/validate.py
   ```

5. Build all output formats to ensure compatibility:

   ```bash
   python tools/build.py
   ```

6. Submit a pull request with a clear description of what changed and why.

## Editing Reference Data

- Keep JSON readable and minimal.
- Do not introduce derived or computed fields.
- Avoid embedding semantics that belong elsewhere (e.g., mixing wood origin with predecessor).
- Use consistent formatting, naming conventions, and IDs.

## Tools and Python Code

- Keep tooling dependency-light.
- Prefer clarity over cleverness.
- Update tests or validation rules when introducing new schema requirements.

## Versioning

This repository uses semantic versioning. 

Before 1.0:

- Breaking changes may occur frequently.
- Schemas may be renamed or restructured.
- Downstream consumers should pin to a specific version.
