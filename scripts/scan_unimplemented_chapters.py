#!/usr/bin/env python
"""Scan for chapters that still look unimplemented (template placeholders).

This repo uses a strict documentation template. A chapter can have all headings
present and still be "unimplemented" if it contains template placeholder text.

Heuristics
----------
Flags a chapter if, outside fenced code blocks, it contains any of:
- Template title placeholder: "# [Título do Assunto]"
- Template instruction phrases (e.g. "Explique o conceito com profundidade")
- Common placeholder markers like "TODO" / "TBD" / "WIP"
- Too-short content (optional) can be enabled with --min-chars

Usage
-----
  python scripts/scan_unimplemented_chapters.py
  python scripts/scan_unimplemented_chapters.py --min-chars 800

Defaults
--------
- Scans book/**/*.md
- Skips book/_* backups
- Ignores fenced code blocks (``` or ~~~)

Exit code
---------
- 0 always (reporting tool)
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    file: Path
    matched: str


PLACEHOLDER_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^#\s+\[Título do Assunto\]\s*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"Explique o conceito com profundidade", re.IGNORECASE),
    re.compile(r"Ex:\s*\"", re.IGNORECASE),
    re.compile(r"Apresente estratégia", re.IGNORECASE),
    re.compile(r"Gersção de relatórios", re.IGNORECASE),
    # Intentionally case-sensitive to avoid flagging Portuguese "todo".
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bWIP\b"),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
]


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


def iter_chapters(root: Path) -> list[Path]:
    book_dir = root / "book"
    if not book_dir.exists():
        return []

    files: list[Path] = []
    for p in book_dir.rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("book/_"):
            continue
        files.append(p)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--min-chars",
        type=int,
        default=0,
        help="Flag chapters whose non-code content is shorter than this many characters.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    chapters = iter_chapters(root)
    if not chapters:
        print("book/ directory not found or empty")
        return 0

    findings: list[Finding] = []
    short: list[tuple[Path, int]] = []

    for ch in chapters:
        try:
            text = ch.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = ch.read_text(encoding="utf-8", errors="replace")

        searchable = strip_fenced_code_blocks(text)
        for pat in PLACEHOLDER_PATTERNS:
            if pat.search(searchable):
                findings.append(Finding(ch, pat.pattern))
                break

        if args.min_chars > 0:
            length = len(searchable.strip())
            if length < args.min_chars:
                short.append((ch, length))

    flagged_files = {f.file for f in findings}
    if args.min_chars > 0:
        flagged_files |= {p for p, _ in short}

    print(f"chapters_flagged={len(flagged_files)}")

    if findings:
        print(f"flagged_by_placeholders={len({f.file for f in findings})}")
        for f in sorted(findings, key=lambda x: x.file.as_posix()):
            rel = f.file.relative_to(root).as_posix()
            print(f"- {rel}: matched={f.matched}")

    if args.min_chars > 0 and short:
        print(f"flagged_by_short_content={len(short)} (min_chars={args.min_chars})")
        for p, length in sorted(short, key=lambda x: x[0].as_posix()):
            rel = p.relative_to(root).as_posix()
            print(f"- {rel}: chars={length}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
