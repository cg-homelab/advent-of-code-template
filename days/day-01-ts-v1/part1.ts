function isDigit(c: string | undefined): boolean {
  return c !== undefined && c >= "0" && c <= "9";
}

export function process(input: string): string {
  const lines = input.replace(/\n+$/, "").split("\n");
  let sum = 0;
  for (const raw of lines) {
    const line = raw.replace(/\r$/, "");
    let first = -1;
    let last = -1;
    for (const c of line) {
      if (isDigit(c)) {
        const d = c.charCodeAt(0) - 48;
        if (first < 0) first = d;
        last = d;
      }
    }
    if (first < 0) {
      throw new Error(`no digit found in line: ${JSON.stringify(line)}`);
    }
    sum += first * 10 + last;
  }
  return String(sum);
}
