DIGITS = "0123456789"


def process(text: str) -> str:
    total = 0
    for n, line in enumerate(text.splitlines(), start=1):
        digits = [c for c in line if c in DIGITS]
        if not digits:
            raise ValueError(f"line {n} has no digit: {line!r}")
        total += int(digits[0]) * 10 + int(digits[-1])
    return str(total)
