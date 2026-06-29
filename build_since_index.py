#!/usr/bin/env python3
"""Build since-index.json from the per-version API snapshots in snapshots/.

Each snapshot is {"knime_version": "X.Y", "keys": [sorted api keys]} produced by
knime-python's API dump (the curated public surface at symbol + parameter
granularity). The since-index maps each key to the *oldest* sampled version it
appears in:

    since(key) = min(version where key is present)

Assumption: an API element is not removed and re-added within a major line (a
removal is a breaking change, handled by a major bump, i.e. outside the
[floor, next-major) window the bundler stamps).

Usage:  python build_since_index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOT_DIR = ROOT / "snapshots"
OUT = ROOT / "since-index.json"

# The producer<->consumer key spelling, see KEY_FORMAT.md. Kept here as a guard so
# a snapshot whose keys drifted from that format fails the build instead of
# silently disabling the downstream compatibility check.
KEY_FORMAT = re.compile(
    r"^(knime\.extension|knime\.scripting\.io|knime\.api\.schema|knime\.api\.table)"
    r"(\.[A-Za-z_][A-Za-z0-9_]*)*(\([A-Za-z_][A-Za-z0-9_]*\))?$"
)


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def main() -> None:
    snapshots = []
    for path in SNAPSHOT_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = [key for key in data["keys"] if not KEY_FORMAT.match(key)]
        if bad:
            raise SystemExit(
                f"{path.name}: {len(bad)} key(s) violate the format in KEY_FORMAT.md, "
                f"e.g. {bad[:3]}"
            )
        snapshots.append((data["knime_version"], data["keys"]))
    if not snapshots:
        raise SystemExit(f"No snapshots found in {SNAPSHOT_DIR}")

    # Oldest first, so the first time we see a key records its since-version.
    snapshots.sort(key=lambda item: version_key(item[0]))

    since: dict[str, str] = {}
    for version, keys in snapshots:
        for key in keys:
            since.setdefault(key, version)

    sampled = [version for version, _ in snapshots]
    OUT.write_text(
        json.dumps(
            {"format": 1, "sampled_versions": sampled, "keys": dict(sorted(since.items()))},
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} — {len(since)} keys from versions {sampled}")


if __name__ == "__main__":
    main()
