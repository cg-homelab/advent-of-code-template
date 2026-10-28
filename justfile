# AoC year repo — every solution (days/day-NN-<lang>-vN) exposes the same recipes (run/test/build/bench)
# regardless of language. See README.md.
# lang-templates/ is a git submodule; a fresh clone needs
# `git submodule update --init` (or `git clone --recurse-submodules`).

# List available recipes
default:
    @just --list

# Creates days/day-NN-<lang>-vN; running `just new-day 3 rust` again makes day-03-rust-v2.
# Scaffold a new solution, prompting for anything missing: just new-day [day] [lang]
new-day day="" lang="":
    #!/usr/bin/env sh
    if [ ! -f lang-templates/scripts/new_day.py ]; then
        echo "error: lang-templates/ is empty. Initialise the submodule first:" >&2
        echo "  git submodule update --init" >&2
        exit 1
    fi
    set --
    if [ -n {{quote(day)}} ]; then set -- "$@" {{quote(day)}}; fi
    if [ -n {{quote(lang)}} ]; then set -- "$@" {{quote(lang)}}; fi
    exec python3 lang-templates/scripts/new_day.py "$@"

# Pull the latest language templates and stage the new submodule pointer: just update-templates
update-templates:
    git submodule update --remote --merge lang-templates
    @echo "Review the lang-templates pointer change (git diff --staged / git status) and commit it."

# Run a solution against its input.txt: just run 3 1 / just run day-03-rust-v2 1
run target part:
    #!/usr/bin/env sh
    d="$(python3 scripts/resolve_day.py {{quote(target)}})" || exit 1
    exec just --justfile "$d/justfile" run {{quote(part)}}

# Run a solution's tests: just test 3 / just test day-03-rust-v2
test target:
    #!/usr/bin/env sh
    d="$(python3 scripts/resolve_day.py {{quote(target)}})" || exit 1
    exec just --justfile "$d/justfile" test

# Benchmark a solution and refresh benchmarks.md: just bench 3 / just bench day-03-rust-v2
bench target:
    #!/usr/bin/env sh
    d="$(python3 scripts/resolve_day.py {{quote(target)}})" || exit 1
    just --justfile "$d/justfile" bench || exit 1
    exec python3 scripts/collect_benches.py

# Run every solution's tests; attempts all, exits non-zero if any failed
test-all:
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

# Benchmark every solution, then aggregate into benchmarks.md (only if none failed)
bench-all:
    #!/usr/bin/env sh
    failed=""
    for d in days/day-[0-9][0-9]-*-v*/; do
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
