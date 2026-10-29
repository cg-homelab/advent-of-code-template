from pathlib import Path

import part1
import part2

HERE = Path(__file__).parent


def test_part1_example() -> None:
    assert part1.process((HERE / "example1.txt").read_text()) == "142"


def test_part2_example() -> None:
    assert part2.process((HERE / "example2.txt").read_text()) == "281"
