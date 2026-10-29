const WORDS = [
  "one",
  "two",
  "three",
  "four",
  "five",
  "six",
  "seven",
  "eight",
  "nine",
];

function digitAt(line: string, i: number): number {
  for (let w = 0; w < WORDS.length; w++) {
    if (line.startsWith(WORDS[w], i)) return w + 1;
  }
  const c = line[i];
  if (c >= "0" && c <= "9") return c.charCodeAt(0) - 48;
  return -1;
}

export function process(input: string): string {
  const lines = input.replace(/\n+$/, "").split("\n");
  let sum = 0;
  for (const raw of lines) {
    const line = raw.replace(/\r$/, "");
    let first = -1;
    let last = -1;
    for (let i = 0; i < line.length; i++) {
      const d = digitAt(line, i);
      if (d < 0) continue;
      if (first < 0) first = d;
      last = d;
    }
    if (first < 0) {
      throw new Error(`no digit found in line: ${JSON.stringify(line)}`);
    }
    sum += first * 10 + last;
  }
  return String(sum);
}
