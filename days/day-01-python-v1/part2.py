DIGITS = "0123456789"
WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def process(text: str) -> str:
    total = 0
    for n, line in enumerate(text.splitlines(), start=1):
        found: list[int] = []
        for i, c in enumerate(line):
            for value, word in enumerate(WORDS, start=1):
                if line.startswith(word, i):
                    found.append(value)
                    break
            else:
                if c in DIGITS:
                    found.append(int(c))
        if not found:
            raise ValueError(f"line {n} has no digit: {line!r}")
        total += found[0] * 10 + found[-1]
    return str(total)
