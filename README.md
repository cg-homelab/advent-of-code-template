# Advent of Code — Single-Year Template

Template repository for one year of [Advent of Code](https://adventofcode.com/).
Create a new repo from this template each year. Every solution lives in its
own directory under `days/`, named `day-NN-<lang>-vN` (`days/day-01-rust-v1`,
`days/day-01-rust-v2`, `days/day-01-zig-v1`, …), so a day can be solved more
than once, in the same language or another one. Every solution exposes the
same `just` recipes regardless of language. Benchmarking is done
with [hyperfine](https://github.com/sharkdp/hyperfine) against the built
artifact directly, so the task-runner wrapper never affects the numbers.

## Getting started

Clone with `git clone --recurse-submodules <url>`, or run
`git submodule update --init` in an existing clone. `lang-templates/` is the
[aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates)
submodule.

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
just new-day 3 rust     # scaffold days/day-03-rust-v1/ from lang-templates/templates/rust
# paste your puzzle input into days/day-03-rust-v1/input.txt
just run 3 1            # run part 1 (day 3 has one solution, so no question asked)
just test 3             # tests against example input
just bench 3            # hyperfine both parts -> days/day-03-rust-v1/bench.md, then refresh benchmarks.md

just new-day 3 rust     # second attempt: days/day-03-rust-v2/ (input.txt copied from v1)
just new-day 3 zig      # another language: days/day-03-zig-v1/
just new-day            # no arguments: prompts for the day and the language
just run 3 1            # day 3 now has three solutions: pick one from a numbered list
just run day-03-rust-v2 1   # or name the solution directory to skip the prompt

just bench-all          # bench every solution, then refresh benchmarks.md
just test-all           # run every solution's tests
just update-templates   # pull newer language templates, then commit the submodule pointer
```

`just new-day [day] [lang]` prompts for whatever you leave out. The new
directory's version is the highest existing version for that day and language
plus one (`-v1` when there is none); gaps left by deleted versions are never
reused, so deleting `-v2` of `-v1`…`-v3` still makes the next one `-v4`.

`just run`, `just test` and `just bench` take a target that is either a day
number or a solution directory name (`day-03-rust-v2`, `days/` prefix
optional). A day number with exactly one solution runs it directly. With
several, an interactive terminal shows a numbered list to choose from; without
a terminal (CI, pipes) the recipe fails and lists the candidates, so pass the
directory name there. The lookup is done by `scripts/resolve_day.py`.

Languages: `rust`, `go`, `python`, `ts`, `php`, `csharp`, `fsharp`, `zig` (see the [aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates) repo).

## Per-solution contract

Each solution directory (`days/day-NN-<lang>-vN`: two-digit day, template
name, version starting at 1) has a `justfile` with the same recipes:

| Recipe | Behavior |
|---|---|
| `just run <part>` | Solve part 1 or 2 against `input.txt`, print the answer |
| `just test` | Language-native tests against `example1.txt`/`example2.txt` |
| `just build` | Produce an optimized artifact (no-op where not applicable) |
| `just bench` | Build, then hyperfine each part, exporting `bench.md` |

The solution executable takes the part number as its only argument
(`<cmd> 1` / `<cmd> 2`) and reads `input.txt` from the solution directory.
Templates ship a working placeholder (part 1: line count, part 2: total
characters across lines) so everything passes right after scaffolding.

`input.txt` and `bench.md` are gitignored — AoC asks that puzzle inputs are
not republished. When you scaffold another solution for a day that already has
one, the scaffolder copies the day's latest non-empty `input.txt` from an
existing sibling solution into the new directory; it creates an empty
`input.txt` only when no sibling has one. The copies are independent
afterwards, so editing one solution's input does not change the others.
Both `just bench <target>` and `just bench-all` merge the per-solution
`bench.md` into `benchmarks.md`: every solution directory gets its own
`## day-NN-<lang>-vN` section, ordered by day, language and version so a day's
solutions sit together. A section is replaced only when that solution is
benchmarked, and carries the date, machine and commit it was produced on. `benchmarks.md` is meant to be committed. Hyperfine's
relative columns are dropped, since they compare part 1 against part 2.

## CI

`.github/workflows/ci.yml` runs on pushes, pull requests and a weekly schedule:

- `scripts`: unit tests and byte-compilation of the scripts in `scripts/`.
- `scaffold`: a smoke test that scaffolds `day-01-python-v1` from the pinned
  templates, then runs test, run and bench on it.
- `days`: `just test-all` over the committed solutions (skipped when there are none).

Benchmarks are not run in CI because puzzle inputs are gitignored and runner
timings are noisy; `benchmarks.md` is produced locally and committed.

## Updating templates

Run `just update-templates` to pull the latest language templates, then commit
the changed `lang-templates` pointer. Dependabot also opens a PR when the
templates repo moves.

## Adding a language

See the README of the
[aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates) repo.
