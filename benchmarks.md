# Benchmarks

Generated from `benchmarks.json` by `just bench <day>` / `just bench-all` / `just benchmarks [mode]`. In-process columns time `process()` only; Wall is hyperfine's whole-process time when hyperfine was installed. Rank and ×fastest compare medians within one day and part. Numbers from different machines are not comparable; see Runs.

## Results

| Day | Part | Rank | Solution | Median | ×fastest | Min | Mean ± σ | p99 | Iterations | Peak RSS Δ | Wall (hyperfine) |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | 1 | 1 | `day-01-zig-v1` | 27.4 µs | 1.00× | 27.3 µs | 27.6 µs ± 1.17 µs | 31.3 µs | 36440 | 0 B | 509 µs ± 31.1 µs |
| 01 | 1 | 2 | `day-01-go-v1` | 34.8 µs | 1.27× | 31.2 µs | 36.0 µs ± 8.90 µs | 53.5 µs | 28847 | 0 B | 1.01 ms ± 98.0 µs |
| 01 | 1 | 3 | `day-01-rust-v2` | 39.1 µs | 1.43× | 37.9 µs | 39.5 µs ± 1.56 µs | 44.2 µs | 24693 | 0 B | 573 µs ± 34.4 µs |
| 01 | 1 | 4 | `day-01-csharp-v1` | 55.0 µs | 2.01× | 54.2 µs | 56.1 µs ± 5.49 µs | 94.5 µs | 19411 | 8.57 MiB | 1.72 ms ± 39.2 µs |
| 01 | 1 | 5 | `day-01-rust-v1` | 108 µs | 3.94× | 106 µs | 108 µs ± 3.24 µs | 117 µs | 9136 | 0 B | 644 µs ± 33.2 µs |
| 01 | 1 | 6 | `day-01-fsharp-v1` | 268 µs | 9.79× | 264 µs | 273 µs ± 15.7 µs | 340 µs | 3711 | 8.87 MiB | 2.26 ms ± 61.9 µs |
| 01 | 1 | 7 | `day-01-ts-v1` | 513 µs | 18.7× | 508 µs | 517 µs ± 35.3 µs | 566 µs | 1937 | 16.2 MiB | 5.29 ms ± 242 µs |
| 01 | 1 | 8 | `day-01-python-v1` | 878 µs | 32.0× | 872 µs | 880 µs ± 6.64 µs | 910 µs | 1134 | 0 B | 17.4 ms ± 551 µs |
| 01 | 2 | 1 | `day-01-zig-v1` | 108 µs | 1.00× | 106 µs | 109 µs ± 2.96 µs | 116 µs | 9339 | 0 B | 600 µs ± 32.6 µs |
| 01 | 2 | 2 | `day-01-rust-v2` | 147 µs | 1.35× | 146 µs | 147 µs ± 3.04 µs | 154 µs | 6778 | 0 B | 687 µs ± 33.7 µs |
| 01 | 2 | 3 | `day-01-rust-v1` | 468 µs | 4.32× | 464 µs | 469 µs ± 7.20 µs | 478 µs | 2156 | 0 B | 1.01 ms ± 41.5 µs |
| 01 | 2 | 4 | `day-01-go-v1` | 667 µs | 6.15× | 660 µs | 670 µs ± 26.1 µs | 768 µs | 1494 | 0 B | 1.66 ms ± 100 µs |
| 01 | 2 | 5 | `day-01-csharp-v1` | 943 µs | 8.69× | 935 µs | 945 µs ± 11.3 µs | 1.01 ms | 1023 | 8.72 MiB | 2.64 ms ± 65.0 µs |
| 01 | 2 | 6 | `day-01-fsharp-v1` | 1.07 ms | 9.87× | 1.05 ms | 1.09 ms ± 39.6 µs | 1.15 ms | 915 | 8.82 MiB | 2.96 ms ± 72.7 µs |
| 01 | 2 | 7 | `day-01-ts-v1` | 3.01 ms | 27.7× | 2.90 ms | 3.00 ms ± 92.0 µs | 3.24 ms | 337 | 18.3 MiB | 8.38 ms ± 245 µs |
| 01 | 2 | 8 | `day-01-python-v1` | 17.9 ms | 165× | 17.8 ms | 18.0 ms ± 99.3 µs | 18.4 ms | 55 | 0 B | 34.6 ms ± 458 µs |

## Runs

- `day-01-csharp-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-fsharp-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-go-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-python-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-rust-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-rust-v2`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-ts-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
- `day-01-zig-v1`: benchmarked 2026-10-29 on AMD Ryzen 9 3900X 12-Core Processor, Linux 7.3.0-4-cachyos (x86_64), commit 022e24f (dirty)
