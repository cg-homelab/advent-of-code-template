# AoC year repo — every day exposes the same recipes (run/test/build/bench)
# regardless of language. See README.md.
# lang-templates/ is a git submodule; a fresh clone needs
# `git submodule update --init` (or `git clone --recurse-submodules`).

# List available recipes
default:
    @just --list

# Scaffold a new day from a language template: just new-day 3 rust
new-day day lang:
    #!/usr/bin/env sh
    if [ ! -f lang-templates/scripts/new_day.py ]; then
        echo "error: lang-templates/ is empty. Initialise the submodule first:" >&2
        echo "  git submodule update --init" >&2
        exit 1
    fi
    python3 lang-templates/scripts/new_day.py {{day}} {{lang}}

# Pull the latest language templates and stage the new submodule pointer: just update-templates
update-templates:
    git submodule update --remote --merge lang-templates
    @echo "Review the lang-templates pointer change (git diff --staged / git status) and commit it."

# Run a day's solution against its input.txt: just run 3 1
run day part:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" run {{part}}

# Run a day's tests: just test 3
test day:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" test

# Benchmark a day and refresh benchmarks.md: just bench 3
bench day:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" bench
    python3 scripts/collect_benches.py

# Run every day's tests; attempts all days, exits non-zero if any failed
test-all:
    #!/usr/bin/env sh
    failed=""
    for d in days/day-*/; do
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

# Benchmark every day, then aggregate into benchmarks.md (only if no day failed)
bench-all:
    #!/usr/bin/env sh
    failed=""
    for d in days/day-*/; do
        [ -d "$d" ] || continue
        if [ ! -f "$d/justfile" ]; then
            echo "skip $d (no justfile)"
            continue
        fi
        echo "== $d"
        just --justfile "$d/justfile" bench || failed="$failed $d"
    done
    if [ -n "$failed" ]; then
        echo "FAILED:$failed" >&2
        exit 1
    fi
    python3 scripts/collect_benches.py
