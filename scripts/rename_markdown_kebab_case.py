#!/usr/bin/env python
"""Rename book markdown files to lowercase kebab-case and update links.

Examples:
- DRY.md -> dry.md
- LawOfDemeter.md -> law-of-demeter.md

This script:
1) Builds a rename plan for all .md under book/
2) Rewrites relative markdown links that resolve to renamed files
3) Applies renames safely on Windows (handles case-only renames via temp names)

Usage:
  python scripts/rename_markdown_kebab_case.py --dry-run
  python scripts/rename_markdown_kebab_case.py --apply

Exit code:
- 0 on success
- 1 on conflicts/errors
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Rename:
    old: Path
    new: Path


def to_kebab_case(stem: str) -> str:
    s = stem.strip().replace("_", "-").replace(" ", "-")
    # fooBar -> foo-Bar
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    # HTTPServer -> HTTP-Server
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.lower()


def is_external_link(target: str) -> bool:
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


def split_target(raw_target: str) -> tuple[str, str, str]:
    """Return (path, fragment, title_part).

    Supports common patterns:
      path#frag
      path "title"
      path#frag "title"

    We preserve fragment and the trailing title (including its leading whitespace).
    """

    t = raw_target.strip()
    if not t:
        return "", "", ""

    # Separate a trailing title (heuristic: whitespace + quote starts title)
    title_part = ""
    # Find first whitespace followed by quote
    m = re.search(r"\s+(?=[\"'])", t)
    if m:
        title_part = t[m.start() :]
        t = t[: m.start()]

    if "#" in t:
        path_part, frag = t.split("#", 1)
        return path_part, "#" + frag, title_part

    return t, "", title_part


def iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if "/book/_" in f"/{rel}":
            continue
        files.append(path)
    return files


def build_renames(repo_root: Path) -> list[Rename]:
    book_root = repo_root / "book"
    renames: list[Rename] = []

    for p in book_root.rglob("*.md"):
        new_name = to_kebab_case(p.stem) + p.suffix.lower()
        if p.name != new_name:
            renames.append(Rename(old=p, new=p.with_name(new_name)))

    # Sort deeper paths first (safer for ops)
    renames.sort(key=lambda r: len(r.old.parts), reverse=True)
    return renames


def validate_no_collisions(renames: list[Rename]) -> None:
    new_paths = {}
    for r in renames:
        key = r.new.resolve().as_posix().lower()
        if key in new_paths and new_paths[key] != r.old:
            raise ValueError(f"collision: {r.old} and {new_paths[key]} -> {r.new}")
        new_paths[key] = r.old


def rewrite_links_in_file(repo_root: Path, md_file: Path, rename_map: dict[str, Path]) -> bool:
    """Rewrite links inside md_file. Returns True if file changed."""

    try:
        text = md_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = md_file.read_text(encoding="utf-8", errors="replace")

    changed = False

    def replace_target(raw_target: str) -> str:
        nonlocal changed

        if is_external_link(raw_target):
            return raw_target

        path_part, frag, title_part = split_target(raw_target)
        if not path_part:
            return raw_target

        # Resolve the current target relative to this file.
        resolved = (md_file.parent / path_part).resolve()

        # Keep within repo root
        try:
            resolved.relative_to(repo_root.resolve())
        except ValueError:
            return raw_target

        resolved_key = resolved.as_posix().lower()
        if resolved_key not in rename_map:
            return raw_target

        new_abs = rename_map[resolved_key]
        new_rel = os.path.relpath(new_abs, md_file.parent).replace("\\", "/")
        new_target = f"{new_rel}{frag}{title_part}"
        if new_target != raw_target:
            changed = True
        return new_target

    # Replace within (...) of markdown links
    def repl(m: re.Match[str]) -> str:
        raw_target = m.group(1)
        new_target = replace_target(raw_target)
        return m.group(0).replace(raw_target, new_target)

    new_text = LINK_RE.sub(repl, text)

    if changed:
        md_file.write_text(new_text, encoding="utf-8")

    return changed


def apply_renames(renames: list[Rename]) -> None:
    """Apply renames with a temp step to support Windows case-only renames."""

    temps: list[tuple[Path, Path]] = []

    # Phase 1: old -> temp
    for r in renames:
        if not r.old.exists():
            raise FileNotFoundError(str(r.old))

        tmp = r.old.with_name(r.old.name + ".__tmp_rename__")
        if tmp.exists():
            tmp.unlink()
        r.old.rename(tmp)
        temps.append((tmp, r.new))

    # Phase 2: temp -> new
    for tmp, new in temps:
        new.parent.mkdir(parents=True, exist_ok=True)
        if new.exists():
            raise FileExistsError(str(new))
        tmp.rename(new)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.apply == args.dry_run:
        print("Choose exactly one: --dry-run or --apply")
        return 1

    repo_root = Path(__file__).resolve().parent.parent
    renames = build_renames(repo_root)

    print(f"planned_renames={len(renames)}")
    for r in renames:
        print(f"- {r.old.relative_to(repo_root).as_posix()} -> {r.new.relative_to(repo_root).as_posix()}")

    if not renames:
        print("Nothing to rename.")
        return 0

    try:
        validate_no_collisions(renames)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    # Map old absolute (resolved) -> new absolute (resolved)
    rename_map = {r.old.resolve().as_posix().lower(): r.new.resolve() for r in renames}

    if args.dry_run:
        return 0

    # Update links before renaming so link resolver finds old targets.
    md_files = iter_markdown_files(repo_root)
    changed_files = 0
    for md in md_files:
        if rewrite_links_in_file(repo_root, md, rename_map):
            changed_files += 1

    print(f"updated_files={changed_files}")

    apply_renames(renames)
    print("Renames applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
