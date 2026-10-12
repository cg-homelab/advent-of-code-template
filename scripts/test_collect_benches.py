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

    def day(self, n: int, bench: str | None = None) -> None:
        d = self.root / "days" / f"day-{n:02d}"
        d.mkdir(parents=True)
        if bench is not None:
            (d / "bench.md").write_text(bench)

    def existing(self, *days: int) -> str:
        return cb.render({f"day-{n:02d}": f"OLD {n}" for n in days})

    def test_new_day_keeps_others(self) -> None:
        self.day(1)
        self.day(2, V2)
        out = cb.merge_sections(self.existing(1), self.root, META)
        self.assertEqual(out["day-01"], "OLD 1")
        self.assertTrue(out["day-02"].startswith("Benchmarked "))

    def test_replace_existing(self) -> None:
        self.day(1, V1)
        out = cb.merge_sections(self.existing(1), self.root, META)
        self.assertNotIn("OLD", out["day-01"])
        self.assertIn("Min [ms]", out["day-01"])

    def test_drop_missing_dir(self) -> None:
        self.day(1)
        out = cb.merge_sections(self.existing(1, 2), self.root, META)
        self.assertEqual(list(out), ["day-01"])

    def test_sorted(self) -> None:
        self.day(10, V2)
        self.day(2, V2)
        self.day(1, V2)
        out = cb.collect(self.root, META)
        assert out is not None
        self.assertLess(out.index("## day-01"), out.index("## day-02"))
        self.assertLess(out.index("## day-02"), out.index("## day-10"))

    def test_empty_returns_none(self) -> None:
        self.day(1)
        self.assertIsNone(cb.collect(self.root, META))

    def test_render_roundtrip(self) -> None:
        out = cb.render({"day-01": "x", "day-02": "y"})
        self.assertTrue(out.startswith("# Benchmarks\n\n"))
        self.assertEqual(cb.parse_sections(out), {"day-01": "x", "day-02": "y"})

    def test_non_table_bench_passthrough(self) -> None:
        self.day(1, "weird output\n")
        out = cb.merge_sections("", self.root, META)
        self.assertTrue(out["day-01"].endswith("\n\nweird output"))

    def test_mtime_rules(self) -> None:
        self.day(1, V1)
        self.day(2, V1)
        self.day(3, V1)
        bench = lambda n: self.root / "days" / f"day-{n:02d}" / "bench.md"  # noqa: E731
        os.utime(bench(1), (1_000_000, 1_000_000))  # older than benchmarks.md
        os.utime(bench(2), (3_000_000, 3_000_000))  # newer
        os.utime(bench(3), (1_000_000, 1_000_000))  # older, but no section
        existing = self.existing(1, 2)
        out = cb.merge_sections(existing, self.root, META, 2_000_000)
        self.assertEqual(out["day-01"], "OLD 1")
        self.assertNotIn("OLD", out["day-02"])
        self.assertIn("Benchmarked 1970-01-12", out["day-03"])
        out = cb.merge_sections(existing, self.root, META, None)
        self.assertTrue(all("OLD" not in v for v in out.values()))

    def test_collect_uses_benchmarks_md_mtime(self) -> None:
        self.day(1, V1)
        bench = self.root / "days" / "day-01" / "bench.md"
        os.utime(bench, (1_000_000, 1_000_000))
        (self.root / "benchmarks.md").write_text(self.existing(1))
        os.utime(self.root / "benchmarks.md", (2_000_000, 2_000_000))
        out = cb.collect(self.root, META)
        assert out is not None
        self.assertIn("OLD 1", out)


if __name__ == "__main__":
    unittest.main()
