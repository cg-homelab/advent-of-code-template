from __future__ import annotations

import os
import tempfile
import unittest
from datetime import date
from pathlib import Path

import collect_benches as cb


def META(d: date) -> str:
    return f"Benchmarked {d.isoformat()} on Test CPU, TestOS 1 (arm64), commit abc1234"


V2 = (
    "| Command | Mean Wall Time [ms] | Change | Factor |\n"
    "|:---|---:|---:|:---|\n"
    "| `a part1` | 4.1 ± 0.5 |  |  |\n"
    "| `a part2` | 3.9 ± 0.2 | -5.2% |  |\n"
)
V1 = (
    "| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |\n"
    "|:---|---:|---:|---:|---:|\n"
    "| `a part1` | 4.1 ± 0.5 | 3.0 | 5.0 | 1.00 |\n"
    "| `a part2` | 3.9 ± 0.2 | 3.1 | 4.9 | 1.00 ± 0.1 |\n"
)


class CleanTableTest(unittest.TestCase):
    def test_v2_columns_removed(self) -> None:
        self.assertEqual(
            cb.clean_table(V2),
            "| Command | Mean Wall Time [ms] |\n|:---|---:|\n"
            "| `a part1` | 4.1 ± 0.5 |\n| `a part2` | 3.9 ± 0.2 |",
        )

    def test_v1_columns_removed(self) -> None:
        self.assertEqual(
            cb.clean_table(V1),
            "| Command | Mean [ms] | Min [ms] | Max [ms] |\n|:---|---:|---:|---:|\n"
            "| `a part1` | 4.1 ± 0.5 | 3.0 | 5.0 |\n| `a part2` | 3.9 ± 0.2 | 3.1 | 4.9 |",
        )

    def test_non_table_verbatim(self) -> None:
        self.assertEqual(cb.clean_table("just some text\nmore\n"), "just some text\nmore")

    def test_ragged_table_verbatim(self) -> None:
        bad = "| a | Change |\n|:--|--:|\n| 1 |\n"
        self.assertEqual(cb.clean_table(bad), bad.strip())


class MergeTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def day(self, n: int, bench: str | None = None, lang: str = "rust", version: int = 1) -> None:
        d = self.root / "days" / f"day-{n:02d}-{lang}-v{version}"
        d.mkdir(parents=True)
        if bench is not None:
            (d / "bench.md").write_text(bench)

    def existing(self, *days: int) -> str:
        return cb.render({f"day-{n:02d}-rust-v1": f"OLD {n}" for n in days})

    def test_new_day_keeps_others(self) -> None:
        self.day(1)
        self.day(2, V2)
        out = cb.merge_sections(self.existing(1), self.root, META)
        self.assertEqual(out["day-01-rust-v1"], "OLD 1")
        self.assertTrue(out["day-02-rust-v1"].startswith("Benchmarked "))

    def test_replace_existing(self) -> None:
        self.day(1, V1)
        out = cb.merge_sections(self.existing(1), self.root, META)
        self.assertNotIn("OLD", out["day-01-rust-v1"])
        self.assertIn("Min [ms]", out["day-01-rust-v1"])

    def test_drop_missing_dir(self) -> None:
        self.day(1)
        out = cb.merge_sections(self.existing(1, 2), self.root, META)
        self.assertEqual(list(out), ["day-01-rust-v1"])

    def test_sorted(self) -> None:
        self.day(10, V2)
        self.day(2, V2)
        self.day(1, V2)
        out = cb.collect(self.root, META)
        assert out is not None
        self.assertLess(out.index("## day-01-rust-v1"), out.index("## day-02-rust-v1"))
        self.assertLess(out.index("## day-02-rust-v1"), out.index("## day-10-rust-v1"))

    def test_several_solutions_per_day(self) -> None:
        self.day(1, V1, "zig", 1)
        self.day(1, V2, "rust", 10)
        self.day(1, V1, "rust", 2)
        self.day(1, V2, "rust", 1)
        self.day(2, V1, "go", 1)
        out = cb.collect(self.root, META)
        assert out is not None
        names = ["day-01-rust-v1", "day-01-rust-v2", "day-01-rust-v10", "day-01-zig-v1", "day-02-go-v1"]
        self.assertEqual(list(cb.parse_sections(out)), names)
        positions = [out.index(f"## {n}\n") for n in names]
        self.assertEqual(positions, sorted(positions))
        sections = cb.parse_sections(out)
        self.assertIn("Mean Wall Time", sections["day-01-rust-v1"])
        self.assertIn("Min [ms]", sections["day-01-rust-v2"])
        self.assertIn("Min [ms]", sections["day-01-zig-v1"])

    def test_ignores_other_directory_names(self) -> None:
        for name in ["day-01", "day-1-rust-v1", "day-01-rust"]:
            d = self.root / "days" / name
            d.mkdir(parents=True)
            (d / "bench.md").write_text(V1)
        self.assertIsNone(cb.collect(self.root, META))

    def test_empty_returns_none(self) -> None:
        self.day(1)
        self.assertIsNone(cb.collect(self.root, META))

    def test_render_roundtrip(self) -> None:
        out = cb.render({"day-02-go-v1": "y", "day-01-rust-v1": "x"})
        self.assertTrue(out.startswith("# Benchmarks\n\n"))
        self.assertEqual(cb.parse_sections(out), {"day-01-rust-v1": "x", "day-02-go-v1": "y"})
        self.assertEqual(list(cb.parse_sections(out)), ["day-01-rust-v1", "day-02-go-v1"])

    def test_unrecognised_heading_dropped(self) -> None:
        text = (
            "# Benchmarks\n\nintro\n\n"
            "## day-01-rust-v1\n\nNEW 1\n\n"
            "## day-02\n\nSTALE 2\n\n"
            "## day-03-go-v1\n\nNEW 3\n"
        )
        self.assertEqual(cb.parse_sections(text), {"day-01-rust-v1": "NEW 1", "day-03-go-v1": "NEW 3"})
        self.day(1)
        self.day(3, lang="go")
        (self.root / "benchmarks.md").write_text(text)
        out = cb.collect(self.root, META)
        assert out is not None
        self.assertNotIn("STALE", out)
        self.assertNotIn("## day-02", out)
        self.assertIn("## day-01-rust-v1\n\nNEW 1\n\n## day-03-go-v1\n\nNEW 3\n", out)

    def test_non_table_bench_passthrough(self) -> None:
        self.day(1, "weird output\n")
        out = cb.merge_sections("", self.root, META)
        self.assertTrue(out["day-01-rust-v1"].endswith("\n\nweird output"))

    def test_mtime_rules(self) -> None:
        self.day(1, V1)
        self.day(2, V1)
        self.day(3, V1)
        bench = lambda n: self.root / "days" / f"day-{n:02d}-rust-v1" / "bench.md"  # noqa: E731
        os.utime(bench(1), (1_000_000, 1_000_000))  # older than benchmarks.md
        os.utime(bench(2), (3_000_000, 3_000_000))  # newer
        os.utime(bench(3), (1_000_000, 1_000_000))  # older, but no section
        existing = self.existing(1, 2)
        out = cb.merge_sections(existing, self.root, META, 2_000_000)
        self.assertEqual(out["day-01-rust-v1"], "OLD 1")
        self.assertNotIn("OLD", out["day-02-rust-v1"])
        self.assertIn("Benchmarked 1970-01-12", out["day-03-rust-v1"])
        out = cb.merge_sections(existing, self.root, META, None)
        self.assertTrue(all("OLD" not in v for v in out.values()))

    def test_collect_uses_benchmarks_md_mtime(self) -> None:
        self.day(1, V1)
        bench = self.root / "days" / "day-01-rust-v1" / "bench.md"
        os.utime(bench, (1_000_000, 1_000_000))
        (self.root / "benchmarks.md").write_text(self.existing(1))
        os.utime(self.root / "benchmarks.md", (2_000_000, 2_000_000))
        out = cb.collect(self.root, META)
        assert out is not None
        self.assertIn("OLD 1", out)


if __name__ == "__main__":
    unittest.main()
