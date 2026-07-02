#!/usr/bin/env python3
"""Scaffold a new AoC day from a language template.

Usage: python3 scripts/new_day.py <day 1-25> <lang>

Copies lang-templates/<lang> to days/day-NN, replaces the __DAY__ token with the
zero-padded day number in file contents and names, and creates an empty
input.txt (gitignored) ready for the puzzle input to be pasted in.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "lang-templates"
TOKEN = "__DAY__"


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        fail(f"usage: {sys.argv[0]} <day 1-25> <lang>")

    day_arg, lang = sys.argv[1], sys.argv[2]

    try:
        day = int(day_arg)
    except ValueError:
        fail(f"day must be a number, got {day_arg!r}")
    if not 1 <= day <= 25:
        fail(f"day must be 1-25, got {day}")
    padded = f"{day:02d}"

    src = TEMPLATES / lang
    if not src.is_dir():
        available = ", ".join(sorted(p.name for p in TEMPLATES.iterdir() if p.is_dir()))
        fail(f"unknown lang {lang!r} (available: {available})")

    dest = ROOT / "days" / f"day-{padded}"
    if dest.exists():
        fail(f"days/{dest.name} already exists")

    dest.parent.mkdir(exist_ok=True)
    shutil.copytree(src, dest)

    # Depth-first so renames don't invalidate child paths.
    for path in sorted(dest.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_file():
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if TOKEN in text:
                path.write_text(text.replace(TOKEN, padded))
        if TOKEN in path.name:
            path.rename(path.with_name(path.name.replace(TOKEN, padded)))

    (dest / "input.txt").touch()

    print(f"created days/{dest.name}/ from lang-templates/{lang}")
    print(f"paste your puzzle input into days/{dest.name}/input.txt, then:")
    print(f"  just run {day} 1   just test {day}   just bench {day}")


if __name__ == "__main__":
    main()
