# dfs2 scans for kappa = 8, 9 up to 20000 (2026-11-02), NOT COMPLETE

> **Update 2026-11-04:** every LIMIT prime listed below is resolved as INFEASIBLE by `dfs2b` (pruned exact DFS); see `2026-11-03-rees-dfs2-prune.md`. Largest known: 8009 ∈ E_2(8), 17551 ∈ E_2(9). Full rescans with dfs2b of κ = 8 on [4202, 20000] and κ = 9 on [5690, 20000] were started on 11-04 (`dfs2b_k8_4202_20000.out`, `dfs2b_k9_<range>.out` in `2026-11-02-rees-schedules/small-prime/`); a run is complete only when its file has a DONE line with limit=0.

Directory: `research/audits/reviews/2026-11-02-rees-schedules/small-prime/`. Round 1: `../2026-11-02-rees-dfs2-runs.md` (kappa 8 to 4057, kappa 9 to 5689).
Status as of this write: no chunk has printed its DONE line. The first wave of chunks hit `timeout 5400` (machine load avg 150-270; each job got ~20 CPU-min). The output of a killed chunk lists only the LIMIT/INFEASIBLE primes found before the kill; the prime reached is unknown (FEASIBLE primes print nothing), so no range below can be called completed.

## Commands
- `./run_chunks.sh` = `timeout 5400 ./dfs2 K P0 P1 5000000 > dfs2_kK_P0_P1.out`, 6 at a time, chunks:
  k8: 4058-6000, 6001-8000, 8001-10000, 10001-12500, 12501-15000, 15001-17500, 17501-20000;
  k9: 5690-7500, 7501-9500, 9501-11500, 11501-13500, 13501-15500, 15501-17500, 17501-20000.
- `./rerun_limits.sh`: `nice -n 10 timeout 5400 ./dfs2 8 p p 50000000 > dfs2_k8_rerun_p.out`, 3 at a time, p = 4073 4129 4153 4201 6073 6089 8009.

## kappa = 8
- Timed out (reach unknown): 4058-6000 (output ends at LIMIT 4201), 6001-8000 (ends at LIMIT 6089), 8001-10000 (ends at LIMIT 8009), 10001-12500, 12501-15000, 15001-17500 (empty output).
- Running (second wave): 17501-20000.
- INFEASIBLE found in the new ranges: none printed.
- LIMIT at 5e6: 4073, 4129, 4153, 4201, 6073, 6089, 8009. Reruns at 5e7 pending.
- Previously resolved (round 1, limit 1e8): 4049, 4057 INFEASIBLE.
- Not scanned: everything above the unknown reach in each timed-out chunk, i.e. certainly 10001-17500, plus 17501-20000 pending.

## kappa = 9
- Running: 5690-7500 (INFEASIBLE 5743 nodes=3729359 so far), 7501-9500, 9501-11500, 11501-13500, 13501-15500.
- Not started: 15501-17500, 17501-20000.
- Nothing above 5689 completed.

## Largest INFEASIBLE prime
kappa 8: 4057 (round 1). kappa 9: 5743 (partial, new).

## Possible stronger prune (not applied; dfs2.c untouched)
None identified that is demonstrably sound; not analysed.

## Update: LIMIT reruns at 5e7 (done)
- INFEASIBLE (kappa 8): 4073 (nodes 5682924), 4129 (6082404), 4153 (6136216), 4201 (6620653). Largest INFEASIBLE kappa 8 so far: 4201.
- 6073, 6089, 8009: killed by `timeout 5400` at the 5e7 limit, no result (empty output); still unresolved.
## Update: kappa 9 partial output (chunks still running; reach unknown)
- 5690-7500: INFEASIBLE 5743, 5779, 5851, 5869, 5923; LIMIT 6067.
- 7501-9500: LIMIT 7507, 7561, 7669. 9501-11500: LIMIT 9613, 9631.
- 11501-13500: LIMIT 11503. 13501-15500: LIMIT 13537. 15501-17500: LIMIT 15607. 17501-20000: empty.
- Largest INFEASIBLE kappa 9 so far: 5923. kappa 9 LIMIT primes at 5e6 are not yet rerun.

## Final state of this pass
- `run_chunks.sh` finished: all 14 chunks ended at `timeout 5400` without a DONE line (load avg 150-270 starved them). No chunk is a completed range; reach inside each is unknown because FEASIBLE primes print nothing and buffered stdout is lost on kill.
- Extra kappa 9 LIMIT lines at 5e6: 15643, 17551 (plus those listed above). No kappa 9 LIMIT rerun was done.
- Totals: kappa 8 INFEASIBLE new: 4073, 4129, 4153, 4201 (largest 4201); LIMIT unresolved: 6073, 6089, 8009. kappa 9 INFEASIBLE new: 5743, 5779, 5851, 5869, 5923 (largest 5923); LIMIT: 6067, 7507, 7561, 7669, 9613, 9631, 11503, 13537, 15607, 15643, 17551.
- The exceptional sets are therefore NOT established above 4201 (kappa 8) / 5923 (kappa 9). Finishing needs rerunning with narrower chunks and per-prime progress output (needs a flush in dfs2.c, left unchanged) on an unloaded machine.


## Update 2026-11-04 ~16:30 (integrator, read from small-prime/dfs2b_*.out)

- K = 8: every prime p ≡ 1 (mod 8) up to 10433 decided (first undecided 10457); largest INFEASIBLE so far 10321 (0.891·8^4.5). No prime has conflicting verdicts.
- K = 9: decided up to 13537 (first undecided 13591); largest INFEASIBLE so far 17659 (0.299·9^5), from the (17501, 20000] scan, which runs ahead of the decided range.
- Paper updated (I170). Screens still running: dfs2b_8_6362, dfs2b_9_11162, dfs2b_9_14501, dfs2b_9_17501.

## Update 2026-11-04 (integrator, I176)
- K = 8: every prime p ≡ 1 (mod 8) up to 11161 decided (first undecided 11177); largest INFEASIBLE 11161 (0.963·8^4.5). INFEASIBLE above 10433: 10457, 10601, 10729, 10753, 10937, 11161.
- K = 9: decided up to 13807 (first undecided 13879); largest INFEASIBLE 17713 (0.2999·9^5), from the (17501, 20000] scan.
- No prime has conflicting verdicts. Screens dfs2b_8_6362, dfs2b_9_11162, dfs2b_9_14501, dfs2b_9_17501 still running.
