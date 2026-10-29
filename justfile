# AoC year repo — every solution (days/day-NN-<lang>-vN) exposes the same recipes (run/test/build/bench)
# regardless of language. See README.md. Requires just >= 1.17.
# lang-templates/ is a git submodule that also holds the shared scripts; a fresh
# clone needs `git submodule update --init` (or `git clone --recurse-submodules`).

# Exported so every recipe and each solution's own justfile (its `scripts` variable)
# find the shared scripts no matter where just was started from.
export AOC_SCRIPTS := justfile_directory() / "lang-templates" / "scripts"

# Layout of benchmarks.md: single (one ranked table) or ranking (one table per day and part).
# Override per call: just tablemode=ranking bench 3
tablemode := "single"

# List available recipes
default:
    @just --list

[private]
submodule:
    #!/usr/bin/env sh
    if [ ! -f "$AOC_SCRIPTS/new_day.py" ]; then
        echo "error: lang-templates/ is empty. Initialise the submodule first:" >&2
        echo "  git submodule update --init" >&2
        exit 1
    fi

# Creates days/day-NN-<lang>-vN; running `just new-day 3 rust` again makes day-03-rust-v2.
# Scaffold a new solution, prompting for anything missing: just new-day [day] [lang]
new-day day="" lang="": submodule
    #!/usr/bin/env sh
    set --
    if [ -n {{quote(day)}} ]; then set -- "$@" {{quote(day)}}; fi
    if [ -n {{quote(lang)}} ]; then set -- "$@" {{quote(lang)}}; fi
    exec python3 "$AOC_SCRIPTS/new_day.py" "$@"

# Pull the latest language templates and stage the new submodule pointer: just update-templates
update-templates:
    git submodule update --remote --merge lang-templates
    @echo "Review the lang-templates pointer change (git diff --staged / git status) and commit it."

# Run a solution against its input.txt: just run 3 1 / just run day-03-rust-v2 1
run target part: submodule
    #!/usr/bin/env sh
    d="$(python3 "$AOC_SCRIPTS/resolve_day.py" {{quote(target)}})" || exit 1
    exec just --justfile "$d/justfile" run {{quote(part)}}

# Run a solution's tests: just test 3 / just test day-03-rust-v2
test target: submodule
    #!/usr/bin/env sh
    d="$(python3 "$AOC_SCRIPTS/resolve_day.py" {{quote(target)}})" || exit 1
    exec just --justfile "$d/justfile" test

# In-process benchmark, then refresh benchmarks.json / benchmarks.md: just bench 3 / just bench day-03-rust-v2 --time 3
bench target *args: submodule
    #!/usr/bin/env sh
    d="$(python3 "$AOC_SCRIPTS/resolve_day.py" {{quote(target)}})" || exit 1
    just --justfile "$d/justfile" bench {{args}} || exit 1
    exec python3 "$AOC_SCRIPTS/collect_benches.py" --tablemode {{quote(tablemode)}}

# Refresh benchmarks.json / benchmarks.md from existing bench.json files, no benchmarking: just benchmarks [single|ranking]
benchmarks mode=tablemode: submodule
    exec python3 "$AOC_SCRIPTS/collect_benches.py" --tablemode {{quote(mode)}}

# Run every solution's tests; attempts all, exits non-zero if any failed
test-all: submodule
    #!/usr/bin/env sh
    failed=""
    for d in days/day-[0-9][0-9]-*-v*/; do
        [ -d "$d" ] || continue
        if [ ! -f "$d/justfile" ]; then
            echo "skip $d (no justfile)"
            continue
        fi
        echo "== $d"
        just --justfile "$d/justfile" test || failed="$failed $d"
    done
    if [ -n "$failed" ]; then
        echo "FAILED:$failed" >&2
        exit 1
    fi

# Benchmark every solution (flags go to each bench), then refresh benchmarks.json / benchmarks.md (only if none failed)
bench-all *args: submodule
    #!/usr/bin/env sh
    failed=""
    for d in days/day-[0-9][0-9]-*-v*/; do
        [ -d "$d" ] || continue
        if [ ! -f "$d/justfile" ]; then
            echo "skip $d (no justfile)"
            continue
        fi
        echo "== $d"
        just --justfile "$d/justfile" bench {{args}} || failed="$failed $d"
    done
    if [ -n "$failed" ]; then
        echo "FAILED:$failed" >&2
        exit 1
    fi
    exec python3 "$AOC_SCRIPTS/collect_benches.py" --tablemode {{quote(tablemode)}}
