# knime-python-api-index

Version index of the **public KNIME Python API** (`knime.extension`,
`knime.scripting.io`, `knime.api.schema`, `knime.api.table`), used to determine
the minimum KNIME Analytics Platform version a Python extension requires.

## Contents

- **`snapshots/<version>.json`** — the curated public API *key-set* for one released
  AP line, at symbol **and parameter** granularity. Produced by knime-python's API
  dump (same griffe spec that generates the API docs). Append-only; one per release.

  ```json
  { "knime_version": "5.10", "keys": ["knime.extension.EnumParameter",
    "knime.extension.EnumParameter.__init__(hidden_choices)", ...] }
  ```

- **`since-index.json`** — derived: `key → first version the key appears in`. This is
  the file consumers read.

  ```json
  { "format": 1, "sampled_versions": ["5.9","5.10","5.11"],
    "keys": { "knime.extension.EnumParameter": "5.9",
              "knime.extension.EnumParameter.__init__(hidden_choices)": "5.10" } }
  ```

- **`build_since_index.py`** — regenerates `since-index.json` from `snapshots/`.

## Who writes this

- **Producer:** knime-python publishes a new `snapshots/<version>.json` per release
  and re-runs `build_since_index.py`.
- **Consumer:** `knime-extension-bundling` fetches `since-index.json` at build time
  to check an extension's declared compatibility floor against the API it actually
  uses (EX-85).

## Assumption

`since(key) = min(version containing key)`. An API element is assumed not to be
removed and re-added within a major line — a removal is a breaking change handled
by a major version bump.
