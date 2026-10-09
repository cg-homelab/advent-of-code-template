# AoC year repo — every day exposes the same recipes (run/test/build/bench)
# regardless of language. See README.md.

# List available recipes
default:
    @just --list

# Scaffold a new day from a language template: just new-day 3 rust
new-day day lang:
    python3 scripts/new_day.py {{day}} {{lang}}

# Run a day's solution against its input.txt: just run 3 1
run day part:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" run {{part}}

# Run a day's tests: just test 3
test day:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" test

# Benchmark a day (writes days/day-NN/bench.md): just bench 3
bench day:
    @just --justfile "$(printf 'days/day-%02d' {{day}})/justfile" bench

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
