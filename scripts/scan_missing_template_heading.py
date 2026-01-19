#!/usr/bin/env python
"""Scan markdown chapters missing a required heading.

Usage:
  python scripts/scan_missing_template_heading.py "## Visão Geral e Contexto de Mercado"

Defaults:
- Scans book/**/*.md
- Skips book/_* backups

Exit code:
- 0 always (reporting tool)
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/scan_missing_template_heading.py <heading>")
        return 2

    required_heading = sys.argv[1]
    root = Path(__file__).resolve().parent.parent
    book_dir = root / "book"

    if not book_dir.exists():
        print("book/ directory not found")
        return 2

    missing: list[Path] = []

    for md_file in book_dir.rglob("*.md"):
        rel = md_file.relative_to(root).as_posix()
        if rel.startswith("book/_"):
            continue

        try:
            text = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md_file.read_text(encoding="utf-8", errors="replace")

        if required_heading not in text:
            missing.append(md_file)

    print(f"chapters_missing_template_heading={len(missing)}")
    for p in sorted(missing):
        print(p.relative_to(root).as_posix())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
