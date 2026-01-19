#!/usr/bin/env python
"""Insert missing '## Referências e Práticas do Mercado' section into chapters.

This repository uses a strict documentation template. Some chapters may be missing
only the final section:

  ## Referências e Práticas do Mercado

This script inserts that section (with a short, generic bullet list) just before
the final navigation line, preserving the navigation links exactly as-is.

Usage:
  python scripts/fix_missing_references_section.py --check
  python scripts/fix_missing_references_section.py --write

Defaults:
- Scans book/**/*.md
- Skips book/_* backups

Exit codes:
- 0 if nothing to fix (or after successful write)
- 1 if fixes are needed in --check
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_HEADING = "## Referências e Práticas do Mercado"

NAV_LINE_RE = re.compile(
    r"^\[(Anterior|Índice|Próximo)\]\([^)]+\)\s*\|\s*\[(Anterior|Índice|Próximo)\]\([^)]+\)(\s*\|\s*\[(Anterior|Índice|Próximo)\]\([^)]+\))?\s*$"
)


def strip_fenced_code_blocks(markdown: str) -> str:
    out_lines: list[str] = []
    in_fence = False
    fence_marker: str | None = None

    for line in markdown.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            continue

        if in_fence:
            continue

        out_lines.append(line)

    return "".join(out_lines)


def is_nav_line(line: str) -> bool:
    return bool(NAV_LINE_RE.match(line.strip()))


def find_last_nav_line_index(lines: list[str]) -> int | None:
    for i in range(len(lines) - 1, -1, -1):
        if is_nav_line(lines[i]):
            return i
    return None


def insert_references(text: str) -> tuple[str, bool]:
    if REQUIRED_HEADING in strip_fenced_code_blocks(text):
        return text, False

    lines = text.splitlines(keepends=True)
    nav_i = find_last_nav_line_index(lines)
    if nav_i is None:
        return text, False

    # Find a separator line right before the nav block (common pattern).
    # We'll insert References after that separator, and add a new separator
    # before the nav line to keep the usual visual layout.
    insert_at = nav_i
    sep_i: int | None = None
    for j in range(nav_i - 1, max(-1, nav_i - 10), -1):
        if lines[j].strip() == "---":
            sep_i = j
            break

    if sep_i is not None:
        insert_at = sep_i + 1

    block = (
        "\n"
        f"{REQUIRED_HEADING}\n\n"
        "- ThoughtWorks Tech Radar (práticas e tendências em engenharia)\n"
        "- Martin Fowler (refactoring, arquitetura evolutiva, patterns)\n"
        "- Google SRE Book / SRE Workbook (operações e confiabilidade)\n\n"
        "---\n\n"
    )

    # Ensure we don't accidentally double blank lines in odd files.
    if insert_at > 0 and lines[insert_at - 1].endswith("\n"):
        # block already starts with a blank line; keep it consistent.
        pass

    new_lines = lines[:insert_at] + [block] + lines[insert_at:]
    new_text = "".join(new_lines)

    return new_text, True


def iter_chapters(root: Path) -> list[Path]:
    book_dir = root / "book"
    files: list[Path] = []
    for p in book_dir.rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("book/_"):
            continue
        files.append(p)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    chapters = iter_chapters(root)

    to_fix: list[str] = []
    fixed: list[str] = []

    for ch in chapters:
        try:
            text = ch.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = ch.read_text(encoding="utf-8", errors="replace")

        new_text, changed = insert_references(text)
        if changed:
            rel = ch.relative_to(root).as_posix()
            to_fix.append(rel)
            if args.write:
                ch.write_text(new_text, encoding="utf-8")
                fixed.append(rel)

    if args.check:
        if not to_fix:
            print("missing_references_section=0")
            return 0
        print(f"missing_references_section={len(to_fix)}")
        for rel in to_fix:
            print(rel)
        return 1

    print(f"fixed_files={len(fixed)}")
    for rel in fixed:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
