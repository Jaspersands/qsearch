# dfs2 runs for kappa = 7, 8, 9 (2026-11-02)

Exact computation. Directory: `2026-11-02-rees-schedules/small-prime/`. Argument order (from source): `dfs2 K P0 P1 limit`.
Build: `cc -O2 -o dfs2 dfs2.c`.

Commands (each under `timeout 3600`, background):
- `./dfs2 7 1597 20000 5000000 > dfs2_k7.out`
- `./dfs2 8 2442 20000 5000000 > dfs2_k8.out`
- `./dfs2 9 3584 20000 5000000 > dfs2_k9.out`
- LIMIT reruns (`timeout 3000`, limit 1e8): `./dfs2 7 p p 100000000` for p in 2731 2801 2843 2969 3137 3221; `./dfs2 8 p p 100000000` for p in 4049 4057 (`dfs2_k*_rerun_p.out`).

| k | range completed | INFEASIBLE primes | unresolved LIMIT | largest INFEASIBLE |
|---|---|---|---|---|
| 7 | [1597, 20000], full (DONE line) | k7.out: 1597 1667 1709 1877 2017 2087 2143 2213 2297 2339 2381 2423 2591; reruns add 2731 2801 2843 2969 3137 3221 | none after rerun | 3221 |
| 8 | [2442, 4057] only: no DONE line, run ended at the 3600 s timeout | 44 in k8.out (3137..4001 shown in file) + reruns 4049, 4057 | none in scanned range | 4057 |
| 9 | [3584, 5689] only: no DONE line, run ended at the 3600 s timeout | 36 in k9.out (last 5689) | none | 5689 |

For k = 8 and 9 the scan beyond 4057 / 5689 was NOT completed; absence of a larger INFEASIBLE prime is not established there. Full lists: the .out files.
