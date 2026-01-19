#!/usr/bin/env python
"""Normalize relative Markdown links to match current on-disk paths.

Goal:
- After renames on Windows (case-insensitive), many links may still point to the
  old casing (e.g. DRY.md) even though the canonical file name is dry.md.
- This script rewrites relative links to use the actual path casing/spelling
  found in the repo.

Rules:
- Only rewrites local relative links (no scheme, no mailto, no pure anchors).
- Skips fenced code blocks (``` / ~~~) to avoid touching code samples.

Usage:
  python scripts/normalize_markdown_links.py

Exit code:
- 0 on success
- 1 if any file fails to read/write
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _is_external(target: str) -> bool:
    t = target.strip()
    if not t:
        return True
    if t.startswith("#"):
        return True
    lowered = t.lower()
    return lowered.startswith(
        (
            "http://",
            "https://",
            "mailto:",
            "tel:",
            "data:",
        )
    )


def _split_target(raw_target: str) -> tuple[str, str, str]:
    """Return (path, fragment, title_part). Preserves trailing title if present."""

    t = raw_target.strip()
    if not t:
        return "", "", ""

    title_part = ""
    m = re.search(r"\s+(?=[\"'])", t)
    if m:
        title_part = t[m.start() :]
        t = t[: m.start()]

    if "#" in t:
        path_part, frag = t.split("#", 1)
        return path_part, "#" + frag, title_part

    return t, "", title_part


def _strip_fenced_code_blocks_keep_mask(text: str) -> list[tuple[str, bool]]:
    """Return list of (line, is_code) while tracking fenced code blocks."""

    in_fence = False
    fence_marker: str | None = None

    out: list[tuple[str, bool]] = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker == marker:
                in_fence = False
                fence_marker = None
            out.append((line, True))
            continue

        out.append((line, in_fence))

    return out


def iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if "/book/_" in f"/{rel}":
            continue
        files.append(path)
    return files


def build_file_map(root: Path) -> dict[str, Path]:
    """Map lowercased absolute path -> actual absolute path."""

    file_map: dict[str, Path] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        key = p.resolve().as_posix().lower()
        file_map[key] = p.resolve()
    return file_map


def normalize_file(root: Path, md_file: Path, file_map: dict[str, Path]) -> bool:
    try:
        original = md_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        original = md_file.read_text(encoding="utf-8", errors="replace")

    changed = False
    parts = _strip_fenced_code_blocks_keep_mask(original)

    def normalize_target(raw_target: str) -> str:
        nonlocal changed

        if _is_external(raw_target):
            return raw_target

        path_part, frag, title_part = _split_target(raw_target)
        if not path_part:
            return raw_target

        resolved = (md_file.parent / path_part).resolve()

        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            return raw_target

        key = resolved.as_posix().lower()
        if key not in file_map:
            return raw_target

        actual_abs = file_map[key]
        new_rel = os.path.relpath(actual_abs, md_file.parent).replace("\\", "/")
        new_target = f"{new_rel}{frag}{title_part}"

        if new_target != raw_target:
            changed = True
        return new_target

    new_lines: list[str] = []
    for line, is_code in parts:
        if is_code:
            new_lines.append(line)
            continue

        def repl(m: re.Match[str]) -> str:
            raw = m.group(1)
            return m.group(0).replace(raw, normalize_target(raw))

        new_lines.append(LINK_RE.sub(repl, line))

    new_text = "".join(new_lines)
    if changed:
        md_file.write_text(new_text, encoding="utf-8")
    return changed


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    md_files = iter_markdown_files(root)
    file_map = build_file_map(root)

    changed_files = 0
    for md in md_files:
        if normalize_file(root, md, file_map):
            changed_files += 1

    print(f"normalized_files={changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
