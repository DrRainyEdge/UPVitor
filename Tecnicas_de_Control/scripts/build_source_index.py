#!/usr/bin/env python3
"""Build the human-readable source index from sources/catalog.json."""

from __future__ import annotations

import json
from pathlib import Path


SUBJECT_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SUBJECT_ROOT / "sources" / "catalog.json"
INDEX_PATH = SUBJECT_ROOT / "sources" / "INDEX.md"


def text(value: object) -> str:
    return str(value or "").replace("\\", "/").replace("|", "\\|").replace("\n", " ")


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
    records = catalog.get("Records", catalog.get("records", []))
    records = sorted(records, key=lambda row: (text(row.get("CurrentPath")), text(row.get("OriginalPath"))))

    lines = [
        "# Índice de fuentes",
        "",
        "Catálogo generado a partir de `catalog.json`. Los campos sin evidencia permanecen vacíos.",
        "",
        "Estados: `current`, `complementary`, `review` y `duplicate-removed`.",
        "",
        "| Ruta original | Ruta actual o canónica | Curso | Grupo | Profesor | Unidad | Tipo | Tema | SHA-256 | Estado | Notas |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    keys = (
        "OriginalPath",
        "CurrentPath",
        "Course",
        "Group",
        "Professor",
        "Unit",
        "Type",
        "Topic",
        "Hash",
        "Status",
        "Notes",
    )
    for record in records:
        values = [text(record.get(key)) for key in keys]
        lines.append("| " + " | ".join(values) + " |")

    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {INDEX_PATH} with {len(records)} records")


if __name__ == "__main__":
    main()
