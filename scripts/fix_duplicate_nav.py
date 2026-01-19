#!/usr/bin/env python
"""Remove duplicate navigation lines from markdown chapters.

Goal
----
Some chapters ended up with navigation lines repeated in the middle of the file.
This script keeps the FIRST and LAST navigation line and removes any additional
occurrences in between.

Navigation line formats supported (2 or 3 links):
- [Índice](...) | [Próximo](...)
- [Anterior](...) | [Índice](...) | [Próximo](...)

It does NOT change the contents of the kept navigation lines.

Usage
-----
  python scripts/fix_duplicate_nav.py --check
  python scripts/fix_duplicate_nav.py --write

Defaults
--------
- Scans book/**/*.md
- Skips book/_* backups

Exit codes
----------
- 0 if no duplicates (or after successful write)
- 1 if duplicates found in --check
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAV_LINE_RE = re.compile(
    r"^\[(Anterior|Índice|Próximo)\]\([^)]+\)\s*\|\s*\[(Anterior|Índice|Próximo)\]\([^)]+\)(\s*\|\s*\[(Anterior|Índice|Próximo)\]\([^)]+\))?\s*$"
)


def is_nav_line(line: str) -> bool:
    return bool(NAV_LINE_RE.match(line.strip()))


def process_file(path: Path, write: bool) -> tuple[bool, int]:
    """Return (changed, duplicate_count_removed)."""

    try:
        original_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        original_text = path.read_text(encoding="utf-8", errors="replace")

    lines = original_text.splitlines(keepends=True)
    nav_indices = [i for i, line in enumerate(lines) if is_nav_line(line)]

    if len(nav_indices) <= 2:
        return False, 0

    keep = {nav_indices[0], nav_indices[-1]}
    removed_count = 0
    new_lines: list[str] = []
    for i, line in enumerate(lines):
        if i in keep:
            new_lines.append(line)
            continue
        if i in nav_indices:
            removed_count += 1
            continue
        new_lines.append(line)

    new_text = "".join(new_lines)
    if new_text == original_text:
        return False, 0

    if write:
        path.write_text(new_text, encoding="utf-8")

    return True, removed_count


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report files with duplicates")
    mode.add_argument("--write", action="store_true", help="rewrite files to remove duplicates")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    book_dir = root / "book"
    if not book_dir.exists():
        print("book/ directory not found")
        return 2

    touched: list[tuple[str, int]] = []
    total_removed = 0

    for md_file in sorted(book_dir.rglob("*.md")):
        rel = md_file.relative_to(root).as_posix()
        if rel.startswith("book/_"):
            continue

        changed, removed = process_file(md_file, write=bool(args.write))
        if changed:
            touched.append((rel, removed))
            total_removed += removed

    if args.check:
        if not touched:
            print("duplicate_nav_files=0")
            return 0

        print(f"duplicate_nav_files={len(touched)}")
        for rel, removed in touched:
            print(f"{rel} removed_lines={removed}")
        return 1

    # --write
    print(f"fixed_files={len(touched)}")
    print(f"removed_nav_lines={total_removed}")
    for rel, removed in touched:
        print(f"{rel} removed_lines={removed}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
