#!/usr/bin/env python3
"""Aggregate every days/day-NN/bench.md (hyperfine markdown export) into benchmarks.md."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    sections = []
    for day_dir in sorted((ROOT / "days").glob("day-*")):
        bench = day_dir / "bench.md"
        if not bench.is_file():
            continue
        sections.append(f"## {day_dir.name}\n\n{bench.read_text().strip()}\n")

    if not sections:
        print("no days/day-*/bench.md files found — run `just bench <day>` first", file=sys.stderr)
        sys.exit(1)

    out = ROOT / "benchmarks.md"
    out.write_text("# Benchmarks\n\n" + "\n".join(sections))
    print(f"wrote {out.name} ({len(sections)} days)")


if __name__ == "__main__":
    main()
