#!/usr/bin/env python
"""Validate book chapters follow DOCUMENTATION_TEMPLATE headings strictly.

Checks
------
- Each chapter has exactly one H1 ("# ").
- All required H2 headings ("## ") from the template exist.
- Required H2 headings appear in the same order as the template.
- No unexpected H2 headings exist (strict mode).

Notes
-----
- Ignores fenced code blocks (``` or ~~~) when scanning headings.
- Scans book/**/*.md and skips book/_* backups.

Usage
-----
  python scripts/validate_template_structure.py
  python scripts/validate_template_structure.py --template .github/DOCUMENTATION_TEMPLATE.md

Exit codes
----------
- 0 if all chapters pass
- 1 if any chapter fails
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChapterProblem:
    file: Path
    reason: str


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


def extract_headings(markdown: str) -> tuple[list[str], list[str]]:
    """Return (h1_headings, h2_headings) in appearance order."""
    searchable = strip_fenced_code_blocks(markdown)
    h1: list[str] = []
    h2: list[str] = []

    for raw_line in searchable.splitlines():
        line = raw_line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            h1.append(line)
        elif line.startswith("## ") and not line.startswith("### "):
            h2.append(line)

    return h1, h2


def required_h2_from_template(template_path: Path) -> list[str]:
    text = template_path.read_text(encoding="utf-8")
    _, h2 = extract_headings(text)
    return h2


def iter_chapters(root: Path) -> list[Path]:
    book_dir = root / "book"
    chapters: list[Path] = []
    for md_file in book_dir.rglob("*.md"):
        rel = md_file.relative_to(root).as_posix()
        if rel.startswith("book/_"):
            continue
        chapters.append(md_file)
    return sorted(chapters)


def validate_chapter(chapter: Path, required_h2: list[str], root: Path) -> list[ChapterProblem]:
    try:
        text = chapter.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = chapter.read_text(encoding="utf-8", errors="replace")

    h1, h2 = extract_headings(text)
    problems: list[ChapterProblem] = []

    if len(h1) != 1:
        problems.append(ChapterProblem(chapter, f"expected exactly 1 H1, found {len(h1)}"))

    required_set = set(required_h2)
    unexpected = [x for x in h2 if x not in required_set]
    if unexpected:
        # Keep output short and stable
        preview = ", ".join(unexpected[:5])
        suffix = "" if len(unexpected) <= 5 else f" (+{len(unexpected) - 5} more)"
        problems.append(ChapterProblem(chapter, f"unexpected H2 headings: {preview}{suffix}"))

    missing = [x for x in required_h2 if x not in h2]
    if missing:
        preview = ", ".join(missing[:5])
        suffix = "" if len(missing) <= 5 else f" (+{len(missing) - 5} more)"
        problems.append(ChapterProblem(chapter, f"missing required H2 headings: {preview}{suffix}"))
        # If missing, ordering check is less actionable; skip.
        return problems

    # Order check: verify indexes are non-decreasing in file
    indices = [h2.index(req) for req in required_h2]
    if indices != sorted(indices):
        # Find first inversion to report
        for i in range(1, len(indices)):
            if indices[i] < indices[i - 1]:
                problems.append(
                    ChapterProblem(
                        chapter,
                        f"required H2 headings out of order near: {required_h2[i - 1]} -> {required_h2[i]}",
                    )
                )
                break

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        default=str(Path(".github") / "DOCUMENTATION_TEMPLATE.md"),
        help="Path to the documentation template markdown.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    template_path = (root / args.template).resolve()

    if not template_path.exists():
        print(f"template not found: {template_path}")
        return 2

    required_h2 = required_h2_from_template(template_path)
    if not required_h2:
        print("no required H2 headings found in template")
        return 2

    chapters = iter_chapters(root)
    if not chapters:
        print("no chapters found under book/")
        return 2

    all_problems: list[ChapterProblem] = []
    for ch in chapters:
        all_problems.extend(validate_chapter(ch, required_h2, root))

    if all_problems:
        print(f"chapters_with_template_issues={len({p.file for p in all_problems})}")
        for p in all_problems:
            rel = p.file.relative_to(root).as_posix()
            print(f"- {rel}: {p.reason}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
