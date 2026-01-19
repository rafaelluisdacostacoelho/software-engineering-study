#!/usr/bin/env python
"""Validate relative Markdown links across the repo.

Rules:
- Checks only local relative links (no scheme, no mailto, no pure anchors).
- Validates that the target file exists.
- Ignores anchors (fragment) existence checks (keeps validator fast/stable).

Exit code:
- 0 if all checked links resolve
- 1 otherwise

Usage:
  python scripts/validate_links.py

Optional env vars:
  ROOT (default: repo root inferred from script location)
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class LinkProblem:
    source: Path
    target: str
    reason: str


def _is_external(target: str) -> bool:
    t = target.strip()
    if not t:
        return True
    if t.startswith("#"):
        return True
    lowered = t.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("tel:")
        or lowered.startswith("data:")
    )


def _strip_fragment(target: str) -> str:
    return target.split("#", 1)[0]


def _strip_title(target: str) -> str:
    # Handles common markdown link syntax: (path "title")
    # We only want the first token if it's not quoted.
    t = target.strip()
    if not t:
        return t
    if t[0] in ("'", '"'):
        return t
    # split on whitespace not inside quotes (simple heuristic)
    parts = t.split()
    return parts[0] if parts else t


def iter_markdown_files(root: Path) -> list[Path]:
    # Canonical content is under book/, but validate all .md files except backups.
    files: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if "/book/_" in f"/{rel}":
            continue
        files.append(path)
    return files


def _strip_fenced_code_blocks(markdown: str) -> str:
    """Remove fenced code blocks so link parsing doesn't treat code as Markdown.

    This is intentionally simple: it handles typical fences that start a line
    with ``` or ~~~ (optionally preceded by whitespace) and treats everything
    until the next matching fence as code.
    """

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
            # drop fence lines themselves
            continue

        if in_fence:
            continue

        out_lines.append(line)

    return "".join(out_lines)


def validate(root: Path) -> tuple[int, list[LinkProblem]]:
    problems: list[LinkProblem] = []
    checked_links = 0

    for md_file in iter_markdown_files(root):
        try:
            text = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md_file.read_text(encoding="utf-8", errors="replace")

        searchable_text = _strip_fenced_code_blocks(text)

        for raw_target in LINK_RE.findall(searchable_text):
            target = raw_target.strip()
            if _is_external(target):
                continue

            target = _strip_title(target)
            target_no_fragment = _strip_fragment(target)
            if not target_no_fragment:
                continue

            checked_links += 1

            # Resolve relative to the markdown file.
            resolved = (md_file.parent / target_no_fragment).resolve()

            # Ensure target stays within repo root once resolved.
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                problems.append(LinkProblem(md_file, target, "target escapes repo root"))
                continue

            if not resolved.exists():
                problems.append(LinkProblem(md_file, target, "target does not exist"))

    return checked_links, problems


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    root = Path(os.environ.get("ROOT", script_dir.parent)).resolve()

    checked_links, problems = validate(root)

    if problems:
        print(f"checked_links={checked_links}")
        print(f"broken_links={len(problems)}")
        for p in problems[:200]:
            rel_source = p.source.relative_to(root).as_posix()
            print(f"- {rel_source}: ({p.target}) -> {p.reason}")
        if len(problems) > 200:
            print(f"... {len(problems) - 200} more")
        return 1

    print(f"checked_links={checked_links}")
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
