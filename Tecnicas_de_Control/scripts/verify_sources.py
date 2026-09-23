#!/usr/bin/env python3
"""Verify source presence, catalog coverage and SHA-256 integrity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SUBJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SUBJECT_ROOT.parent
SOURCES_ROOT = SUBJECT_ROOT / "sources"
CATALOG_PATH = SOURCES_ROOT / "catalog.json"


def repo_path(value: str) -> Path:
    return REPO_ROOT.joinpath(*value.replace("\\", "/").split("/"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
    records = catalog.get("Records", catalog.get("records", []))
    errors: list[str] = []
    catalogued_current: set[Path] = set()

    for record in records:
        current = repo_path(str(record.get("CurrentPath", ""))).resolve()
        expected_hash = str(record.get("Hash", "")).lower()
        status = str(record.get("Status", ""))
        original = repo_path(str(record.get("OriginalPath", ""))).resolve()

        if not current.is_file():
            errors.append(f"missing current source: {current}")
            continue
        catalogued_current.add(current)
        actual_hash = sha256(current)
        if actual_hash != expected_hash:
            errors.append(f"hash mismatch: {current}")
        if status == "duplicate-removed" and original.exists():
            errors.append(f"removed duplicate still exists: {original}")

    ignored = {CATALOG_PATH.resolve(), (SOURCES_ROOT / "INDEX.md").resolve()}
    actual_sources = {path.resolve() for path in SOURCES_ROOT.rglob("*") if path.is_file()} - ignored
    missing_from_catalog = actual_sources - catalogued_current
    if missing_from_catalog:
        errors.extend(f"uncatalogued source: {path}" for path in sorted(missing_from_catalog))

    if errors:
        raise SystemExit("\n".join(errors))

    print(
        f"OK: {len(records)} catalog records, "
        f"{len(catalogued_current)} unique source files, all hashes valid"
    )


if __name__ == "__main__":
    main()
