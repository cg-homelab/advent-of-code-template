# Advent of Code — Single-Year Template

Template repository for one year of [Advent of Code](https://adventofcode.com/).
Create a new repo from this template each year. Every day lives in its own
directory under `days/` (`days/day-01` … `days/day-25`), can be written in any
supported language, and
exposes the same `just` recipes regardless of language. Benchmarking is done
with [hyperfine](https://github.com/sharkdp/hyperfine) against the built
artifact directly, so the task-runner wrapper never affects the numbers.

## Requirements

- [just](https://github.com/casey/just) — task runner
- [hyperfine](https://github.com/sharkdp/hyperfine) — benchmarking
- Python 3 — scaffolding/aggregation scripts (stdlib only)
- Per language, only if you use it: `cargo` (rust), `go`, [`uv`](https://github.com/astral-sh/uv) (python), [`bun`](https://bun.sh) (ts), `php`, [.NET 10 SDK](https://dotnet.microsoft.com/download) (csharp, fsharp), [`zig`](https://ziglang.org/download/) 0.17+
- C#/F# `just build` and `just bench` publish a Native AOT binary, which needs a C toolchain (Xcode Command Line Tools on macOS, `clang` + `zlib1g-dev` on Linux, the Visual Studio C++ workload on Windows). The first publish downloads the ILCompiler packages. `just run` uses `dotnet run` (JIT) for fast iteration, while `just bench` times the AOT binary.
  If your `dotnet` comes from Homebrew (a non-portable build), the AOT link step may fail with `ld: library 'ssl' not found`; fix it with `export LIBRARY_PATH=/opt/homebrew/opt/openssl@3/lib:/opt/homebrew/opt/brotli/lib`.

On Windows, install [Git for Windows](https://gitforwindows.org/) and point
just at its shell by adding this to the root `justfile`:

```just
set windows-shell := ["sh", "-cu"]
```

## Workflow

```sh
just new-day 3 rust     # scaffold days/day-03/ from lang-templates/rust
# paste your puzzle input into days/day-03/input.txt
just run 3 1            # run part 1
just test 3             # tests against example input
just bench 3            # hyperfine both parts -> days/day-03/bench.md, then refresh benchmarks.md
just bench-all          # bench every day, then refresh benchmarks.md
just test-all           # run every day's tests
```

Languages: `rust`, `go`, `python`, `ts`, `php`, `csharp`, `fsharp`, `zig` (see `lang-templates/`).

## Per-day contract

Each day directory has a `justfile` with the same recipes:

| Recipe | Behavior |
|---|---|
| `just run <part>` | Solve part 1 or 2 against `input.txt`, print the answer |
| `just test` | Language-native tests against `example1.txt`/`example2.txt` |
| `just build` | Produce an optimized artifact (no-op where not applicable) |
| `just bench` | Build, then hyperfine each part, exporting `bench.md` |

The solution executable takes the part number as its only argument
(`<cmd> 1` / `<cmd> 2`) and reads `input.txt` from the day directory.
Templates ship a working placeholder (part 1: line count, part 2: total
characters across lines) so everything passes right after scaffolding.

`input.txt` and `bench.md` are gitignored — AoC asks that puzzle inputs are
not republished. Both `just bench <day>` and `just bench-all` merge the
per-day `bench.md` into `benchmarks.md`: each `## day-NN` section is replaced
only when that day is benchmarked, and carries the date, machine and commit it
was produced on. `benchmarks.md` is meant to be committed. Hyperfine's
relative columns are dropped, since they compare part 1 against part 2.

## CI

`.github/workflows/ci.yml` scaffolds every language template on Ubuntu and
runs test, run and bench on pushes, pull requests and a weekly schedule.

## Adding a language

Add a directory under `lang-templates/` containing a `justfile` with the four
recipes above, `example1.txt`/`example2.txt`, and a placeholder solution. Use
the literal token `__DAY__` anywhere the zero-padded day number should appear;
`scripts/new_day.py` replaces it in file contents and names.
