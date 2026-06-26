# ![Image](https://www.knime.com/sites/default/files/knime_logo_github_40x40_4layers.png) KNIME® - Python API Version Index

This repository is maintained by the KNIME Executor Core team.

This repository holds a machine-readable **version index of the public KNIME Python
API** (`knime.extension`, `knime.scripting.io`, `knime.api.schema`,
`knime.api.table`). It records, for each public API element down to the parameter
level, the first KNIME Analytics Platform version it appeared in. KNIME tooling uses
this to determine the minimum AP version a Python extension requires and to validate
an extension's declared compatibility floor against the API it actually uses.

## Content

The repository contains generated data and a single build script:

* _snapshots/&lt;version&gt;.json_: the curated public API **key-set** for one released
  AP line, at symbol and parameter granularity. Produced by knime-python's API dump
  (the same griffe spec that generates the API docs). Append-only; one file per
  release.

  ```json
  { "knime_version": "5.10",
    "keys": ["knime.extension.EnumParameter",
             "knime.extension.EnumParameter.__init__(hidden_choices)"] }
  ```

* _since-index.json_: derived from all snapshots — `key → first version the key
  appears in`. This is the file consumers read.

  ```json
  { "format": 1, "sampled_versions": ["5.9", "5.10", "5.11"],
    "keys": { "knime.extension.EnumParameter": "5.9",
              "knime.extension.EnumParameter.__init__(hidden_choices)": "5.10" } }
  ```

* _build\_since\_index.py_: regenerates `since-index.json` from `snapshots/`.
  `since(key) = min(version containing key)`; an API element is assumed not to be
  removed and re-added within a major line (a removal is a breaking change handled
  by a major version bump).

### Producers and consumers

* **Producer:** knime-python publishes a new `snapshots/<version>.json` per release
  and re-runs `build_since_index.py`.
* **Consumer:** `knime-extension-bundling` fetches `since-index.json` at build time
  to check an extension's declared compatibility floor against the API it uses.

## Development Notes

You can find instructions on how to work with our code or develop extensions for
KNIME Analytics Platform in the _knime-sdk-setup_ repository on
[GitHub](http://github.com/KNIME/knime-sdk-setup).

## Join the Community

* [KNIME Forum](https://forum.knime.com)
