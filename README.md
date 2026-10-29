# Advent of Code — Single-Year Template

Template repository for one year of [Advent of Code](https://adventofcode.com/).
Create a new repo from this template each year. Every solution lives in its
own directory under `days/`, named `day-NN-<lang>-vN` (`days/day-01-rust-v1`,
`days/day-01-rust-v2`, `days/day-01-zig-v1`, …), so a day can be solved more
than once, in the same language or another one. Every solution exposes the
same `just` recipes regardless of language. Benchmarking is in-process: a
shared Python driver (`lang-templates/scripts/bench_day.py`) asks the built
executable to time only its `process()` call per part, so runtime startup and
the task-runner wrapper never affect the numbers. When
[hyperfine](https://github.com/sharkdp/hyperfine) is installed it adds the
whole-process wall time as an extra column.

## Getting started

Clone with `git clone --recurse-submodules <url>`, or run
`git submodule update --init` in an existing clone. `lang-templates/` is the
[aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates)
submodule.

## Requirements

- [just](https://github.com/casey/just) 1.17 or newer — task runner
- Python 3 (3.11+ for `just bench`) — scaffolding, benchmarking and aggregation scripts (stdlib only)
- Optional: [hyperfine](https://github.com/sharkdp/hyperfine) — adds the whole-process Wall column to benchmarks
- Per language, only if you use it: `cargo` (rust), `go`, [`uv`](https://github.com/astral-sh/uv) (python), [`bun`](https://bun.sh) (ts), `php`, [.NET 10 SDK](https://dotnet.microsoft.com/download) (csharp, fsharp), [`zig`](https://ziglang.org/download/) 0.17+
- C#/F# `just build` and `just bench` publish a Native AOT binary, which needs a C toolchain (Xcode Command Line Tools on macOS, `clang` + `zlib1g-dev` on Linux, the Visual Studio C++ workload on Windows). The first publish downloads the ILCompiler packages. `just run` uses `dotnet run` (JIT) for fast iteration, while `just bench` times the AOT binary.
  If your `dotnet` comes from Homebrew (a non-portable build), the AOT link step may fail with `ld: library 'ssl' not found`; fix it with `export LIBRARY_PATH=/opt/homebrew/opt/openssl@3/lib:/opt/homebrew/opt/brotli/lib`.

On Windows, install [Git for Windows](https://gitforwindows.org/) and point
just at its shell by adding this to the root `justfile`:

```just
set windows-shell := ["sh", "-cu"]
```

The recipes call `python3`; if your Python is only on PATH as `python`, add a
`python3` alias or change the recipes accordingly. Windows has no peak-RSS
support in the harnesses, so the Peak RSS Δ column shows `n/a` there.

## Workflow

```sh
just new-day 3 rust     # scaffold days/day-03-rust-v1/ from lang-templates/templates/rust
# paste your puzzle input into days/day-03-rust-v1/input.txt
just run 3 1            # run part 1 (day 3 has one solution, so no question asked)
just test 3             # tests against example input
just bench 3            # in-process bench of both parts -> days/day-03-rust-v1/bench.json, then refresh benchmarks.md
just bench 3 --time 3 --no-hyperfine   # extra flags go straight to the bench driver

just new-day 3 rust     # second attempt: days/day-03-rust-v2/ (input.txt copied from v1)
just new-day 3 zig      # another language: days/day-03-zig-v1/
just new-day            # no arguments: prompts for the day and the language
just run 3 1            # day 3 now has three solutions: pick one from a numbered list
just run day-03-rust-v2 1   # or name the solution directory to skip the prompt

just bench-all          # bench every solution (flags pass through too), then refresh benchmarks.md
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
directory name there. The lookup is done by `lang-templates/scripts/resolve_day.py`.

Languages: `rust`, `go`, `python`, `ts`, `php`, `csharp`, `fsharp`, `zig` (see the [aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates) repo).

## Per-solution contract

Each solution directory (`days/day-NN-<lang>-vN`: two-digit day, template
name, version starting at 1) has a `justfile` with the same recipes:

| Recipe | Behavior |
|---|---|
| `just run <part>` | Solve part 1 or 2 against `input.txt`, print the answer |
| `just test` | Language-native tests against `example1.txt`/`example2.txt` |
| `just build` | Produce an optimized artifact (no-op where not applicable) |
| `just bench [flags]` | Build, then time `process()` in-process for both parts (+ hyperfine wall time when installed), writing `bench.json` |

The solution executable takes the part number as its only argument
(`<cmd> 1` / `<cmd> 2`) and reads `input.txt` from the solution directory.
It also has a bench mode, `<cmd> bench <part> <input-path> <iterations>`,
which times `process()` that many times and prints one JSON line for the
driver; the protocol is described under
[Executable contract](https://github.com/cg-homelab/aoc-lang-templates#executable-contract)
in the templates README.
Templates ship a working placeholder (part 1: line count, part 2: total
characters across lines) so everything passes right after scaffolding.

`input.txt` and `bench.json` are gitignored — AoC asks that puzzle inputs are
not republished. When you scaffold another solution for a day that already has
one, the scaffolder copies the day's latest non-empty `input.txt` from an
existing sibling solution into the new directory; it creates an empty
`input.txt` only when no sibling has one. The copies are independent
afterwards, so editing one solution's input does not change the others.
Both `just bench <target>` and `just bench-all` merge the per-solution
`bench.json` into `benchmarks.md`: every solution directory gets its own
`## day-NN-<lang>-vN` section, ordered by day, language and version so a day's
solutions sit together. A section is replaced only when that solution is
benchmarked, and carries the date, machine and commit it was produced on. `benchmarks.md` is meant to be committed.
Each section has one row per part: Min, Median, Mean ± σ and p99 of the
in-process `process()` time, the number of measured Iterations, the Peak RSS Δ
(growth of the process's peak resident memory during the loop), and Wall, the
whole-process time measured by hyperfine (`n/a` when hyperfine is not
installed or `--no-hyperfine` was passed). Answers never appear in it.
Numbers under about 1 µs mostly measure clock overhead, and the RSS delta is
only indicative for garbage-collected runtimes. The driver runs each part for
about a second (at least 10 iterations, plus warmup); for a very slow part use
`just bench 3 --iterations 1 --warmup 0`.

## CI

`.github/workflows/ci.yml` runs on pushes, pull requests and a weekly schedule:

- `scripts`: the unit tests of the shared scripts in the `lang-templates`
  submodule (`lang-templates/scripts`), at the pinned commit.
- `scaffold`: a smoke test that scaffolds `day-01-python-v1` from the pinned
  templates, then runs test, run and bench on it and checks the `bench.json`
  answers and the `benchmarks.md` section.
- `days`: `just test-all` over the committed solutions (skipped when there are none).

The committed solutions are not benchmarked in CI because puzzle inputs are
gitignored and runner timings are noisy (the `scaffold` job only checks that
the bench pipeline works on the placeholder); `benchmarks.md` is produced
locally and committed.

## Updating templates

Run `just update-templates` to pull the latest language templates, then commit
the changed `lang-templates` pointer. Dependabot also opens a PR when the
templates repo moves.

## Migrating an existing year repo to lang-templates v3

lang-templates v3.0.0 moved the scripts into the submodule and replaced the
hyperfine-only `bench.md` with in-process benchmarking. A year repo created
from an older version of this template is migrated once:

1. Move the submodule to the tag and stage it:
   `git -C lang-templates fetch --tags && git -C lang-templates checkout v3.0.0 && git add lang-templates`.
2. Replace the root `justfile`, `.gitignore` and `.github/workflows/ci.yml`
   with the ones from this template repo (keep any local additions, such as
   the Windows `set windows-shell` line).
3. Delete the old scripts, which now live in the submodule: `git rm -r scripts/`.
4. Give each existing solution the v3 bench mode. Either re-scaffold
   (`just new-day 3 rust` makes `day-03-rust-v2`; move your part code into it
   and delete the old directory), or hand-port it from
   `lang-templates/templates/<lang>/`: copy the template `justfile` with
   `__NAME__` replaced by the solution's directory name, copy the harness file
   (for example `bench.py` or `src/bench.rs`) with `__NAME__` and `__DAY__`
   replaced the same way, and add the `bench` dispatch from the template's
   main file (F#: also list `Bench.fs` before `Program.fs` in the `.fsproj`).
5. Run `just bench-all` to rewrite `benchmarks.md` in the new format. Old
   sections stay until their solution is re-benchmarked, and a leftover
   `bench.md` without a `bench.json` makes the aggregation print a warning;
   delete those files (`rm days/*/bench.md`) once every solution is migrated.

## Adding a language

See the README of the
[aoc-lang-templates](https://github.com/cg-homelab/aoc-lang-templates) repo.
