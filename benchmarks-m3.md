# Benchmarks

Generated from `benchmarks.json` by `just bench <day>` / `just bench-all` / `just benchmarks [mode]`. In-process columns time `process()` only; Wall is hyperfine's whole-process time when hyperfine was installed. Rank and ×fastest compare medians within one day and part. Numbers from different machines are not comparable; see Runs.

## Results

| Day | Part | Rank | Solution | Median | ×fastest | Min | Mean ± σ | p99 | Iterations | Peak RSS Δ | Wall (hyperfine) |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | 1 | 1 | `day-01-zig-v1` | 13.0 µs | 1.00× | 12.1 µs | 13.2 µs ± 999 ns | 18.5 µs | 37442 | 48.0 KiB | 1.59 ms ± 47.9 µs |
| 01 | 1 | 2 | `day-01-rust-v2` | 15.1 µs | 1.16× | 15.0 µs | 15.7 µs ± 1.34 µs | 23.4 µs | 31088 | 32.0 KiB | 1.46 ms ± 43.4 µs |
| 01 | 1 | 3 | `day-01-go-v1` | 19.3 µs | 1.48× | 18.9 µs | 20.5 µs ± 6.63 µs | 29.2 µs | 42629 | 5.86 MiB | 1.95 ms ± 125 µs |
| 01 | 1 | 4 | `day-01-csharp-v1` | 22.6 µs | 1.73× | 22.3 µs | 23.2 µs ± 3.65 µs | 49.9 µs | 28369 | n/a | 4.05 ms ± 198 µs |
| 01 | 1 | 5 | `day-01-rust-v1` | 76.4 µs | 5.86× | 71.0 µs | 75.3 µs ± 3.02 µs | 84.5 µs | 7355 | 144 KiB | 1.54 ms ± 42.7 µs |
| 01 | 1 | 6 | `day-01-fsharp-v1` | 161 µs | 12.3× | 149 µs | 163 µs ± 12.9 µs | 218 µs | 4641 | n/a | 4.28 ms ± 157 µs |
| 01 | 1 | 7 | `day-01-ts-v1` | 368 µs | 28.2× | 310 µs | 370 µs ± 30.9 µs | 449 µs | 2647 | 11.8 MiB | 5.78 ms ± 254 µs |
| 01 | 1 | 8 | `day-01-python-v1` | 415 µs | 31.8× | 383 µs | 420 µs ± 38.9 µs | 541 µs | 2389 | 96.0 KiB | 18.7 ms ± 451 µs |
| 01 | 2 | 1 | `day-01-zig-v1` | 69.4 µs | 1.00× | 69.2 µs | 69.9 µs ± 1.94 µs | 79.0 µs | 14354 | 48.0 KiB | 1.66 ms ± 37.0 µs |
| 01 | 2 | 2 | `day-01-rust-v2` | 104 µs | 1.49× | 103 µs | 105 µs ± 2.39 µs | 116 µs | 9623 | 16.0 KiB | 1.54 ms ± 33.1 µs |
| 01 | 2 | 3 | `day-01-rust-v1` | 358 µs | 5.16× | 357 µs | 360 µs ± 5.67 µs | 385 µs | 2804 | 64.0 KiB | 1.80 ms ± 39.5 µs |
| 01 | 2 | 4 | `day-01-go-v1` | 411 µs | 5.92× | 406 µs | 418 µs ± 19.3 µs | 493 µs | 2419 | 5.45 MiB | 2.33 ms ± 72.8 µs |
| 01 | 2 | 5 | `day-01-csharp-v1` | 711 µs | 10.3× | 661 µs | 704 µs ± 21.4 µs | 756 µs | 1420 | n/a | 4.70 ms ± 171 µs |
| 01 | 2 | 6 | `day-01-fsharp-v1` | 736 µs | 10.6× | 682 µs | 742 µs ± 25.9 µs | 849 µs | 1361 | n/a | 4.91 ms ± 311 µs |
| 01 | 2 | 7 | `day-01-ts-v1` | 1.50 ms | 21.6× | 1.39 ms | 1.50 ms ± 33.1 µs | 1.60 ms | 644 | 15.2 MiB | 7.48 ms ± 266 µs |
| 01 | 2 | 8 | `day-01-python-v1` | 5.81 ms | 83.8× | 5.78 ms | 5.81 ms ± 18.5 µs | 5.90 ms | 172 | 112 KiB | 24.5 ms ± 2.14 ms |

## Runs

- `day-01-csharp-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-fsharp-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-go-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-python-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-rust-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-rust-v2`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-ts-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
- `day-01-zig-v1`: benchmarked 2026-10-29 on Apple M3 Pro, macOS 26.5.1 (arm64), commit 8641ef0
