# Spend Report

Generated 2026-10-19 by `tools/spend/report.py` from `research/audits/spend_ledger.jsonl`; do not edit by hand.
Days are UTC calendar days. See `tools/spend/README.md` for what each source can and cannot tell you.

## Headline

| Measure | Value |
|---|---|
| Days with recorded activity | 76 (2026-07-06 to 2026-10-18) |
| Runs | 598 |
| Retained negatives added | 976 on 35 days (most: 459 on 2026-07-15) |
| Runs per retained negative | 0.61 |
| Codex tokens | 5,471,259,754 on 71 days (2026-07-06 to 2026-10-18) |
| Codex tokens per retained negative | 6,005,774 (911 negatives on days with token records) |
| Uncached Codex tokens per retained negative | 189,868 |
| Timed runs | 1 (6.3 s wall, 6.8 s CPU) |
| Measured time per retained negative | n/a: no timed run has added a negative yet |

## What the numbers mean

- **Runs** are the experiment runs in `research/experiment_run_history.json`, plus timed runs that did not
  log an experiment run inside their own time window. The history has one timestamp per run and no
  durations.
- **Retained negatives** are records still in `research/registry/negative_results.json`, dated by the
  first commit that contains them. That is the commit day, not the day the work was done. Ids not yet
  committed are dated by the registry file's mtime.
- **Back-fills.** The first commit of a file holds everything made before it, so the busiest days
  are partly history. The first registry commit (2026-07-15) holds 459 retained negatives made at any point up to then. The first theorem commit (2026-08-21) adds 724 theorem files at once.
- The run history's own `negative_results_written` metric sums to 652. Only some runs set it, so it undercounts.
- **Wall and CPU seconds** come only from runs made through `tools/spend/timed.py`. Days before the
  wrapper was used show 0.0 wall seconds and no CPU time: unmeasured, not free.
- **Codex tokens** come from Codex session logs whose working directory is this repo, summed per day.
  The total includes cached input tokens, which dominate; the uncached figure is input minus cached
  input plus output. The Gemini agents are not counted because their logs hold no labelled token
  counts, so tokens per negative is a lower bound for the whole loop.

## Per day

| Date | Runs | Timed runs | Retained negatives | Theorem files added | Wall s | CPU s | Codex tokens |
|---|---|---|---|---|---|---|---|
| 2026-07-06 | 0 | 0 | 0 | 0 | - | - | 9,438,873 |
| 2026-07-07 | 12 | 0 | 0 | 0 | - | - | 167,300,390 |
| 2026-07-08 | 28 | 0 | 0 | 0 | - | - | 159,277,923 |
| 2026-07-09 | 11 | 0 | 0 | 0 | - | - | 91,936,755 |
| 2026-07-10 | 12 | 0 | 0 | 0 | - | - | 81,768,832 |
| 2026-07-11 | 5 | 0 | 0 | 0 | - | - | 47,681,335 |
| 2026-07-12 | 5 | 0 | 0 | 0 | - | - | 26,312,294 |
| 2026-07-13 | 17 | 0 | 0 | 0 | - | - | 101,673,445 |
| 2026-07-14 | 34 | 0 | 0 | 0 | - | - | 361,397,154 |
| 2026-07-15 | 34 | 0 | 459 | 0 | - | - | 351,437,896 |
| 2026-07-17 | 0 | 0 | 0 | 0 | - | - | 10,263,854 |
| 2026-07-18 | 5 | 0 | 16 | 0 | - | - | 134,306,223 |
| 2026-07-19 | 0 | 0 | 13 | 0 | - | - | 144,369,708 |
| 2026-07-21 | 0 | 0 | 3 | 0 | - | - | - |
| 2026-07-22 | 9 | 0 | 0 | 0 | - | - | 94,517,541 |
| 2026-07-23 | 6 | 0 | 10 | 0 | - | - | 63,318,902 |
| 2026-07-24 | 2 | 0 | 2 | 0 | - | - | 97,920,082 |
| 2026-07-27 | 18 | 0 | 7 | 0 | - | - | 94,152,435 |
| 2026-07-28 | 16 | 0 | 15 | 0 | - | - | 211,826,805 |
| 2026-07-29 | 9 | 0 | 0 | 0 | - | - | 40,015,498 |
| 2026-07-30 | 64 | 0 | 0 | 0 | - | - | 191,524,974 |
| 2026-08-05 | 2 | 0 | 0 | 0 | - | - | 54,740,023 |
| 2026-08-06 | 7 | 0 | 111 | 0 | - | - | 118,869,148 |
| 2026-08-07 | 1 | 0 | 1 | 0 | - | - | 24,153,204 |
| 2026-08-08 | 0 | 0 | 79 | 0 | - | - | 215,864,858 |
| 2026-08-09 | 0 | 0 | 37 | 0 | - | - | 128,637,115 |
| 2026-08-10 | 0 | 0 | 38 | 0 | - | - | - |
| 2026-08-11 | 0 | 0 | 10 | 0 | - | - | 281,541,931 |
| 2026-08-12 | 6 | 0 | 0 | 0 | - | - | 39,789,544 |
| 2026-08-13 | 0 | 0 | 0 | 0 | - | - | 138,862,061 |
| 2026-08-14 | 92 | 0 | 0 | 0 | - | - | 46,153,319 |
| 2026-08-20 | 0 | 0 | 0 | 0 | - | - | 69,448,989 |
| 2026-08-21 | 64 | 0 | 1 | 724 | - | - | 102,749,020 |
| 2026-08-24 | 11 | 0 | 5 | 22 | - | - | 86,462,478 |
| 2026-08-25 | 0 | 0 | 4 | 4 | - | - | 53,465,610 |
| 2026-08-26 | 4 | 0 | 11 | 11 | - | - | 58,178,006 |
| 2026-08-27 | 6 | 0 | 1 | 1 | - | - | 37,852,678 |
| 2026-08-28 | 0 | 0 | 0 | 0 | - | - | 28,335,168 |
| 2026-08-30 | 1 | 0 | 0 | 0 | - | - | 11,793,254 |
| 2026-08-31 | 2 | 0 | 0 | 0 | - | - | 16,928,550 |
| 2026-09-01 | 10 | 0 | 0 | 0 | - | - | 76,388,525 |
| 2026-09-02 | 9 | 0 | 0 | 0 | - | - | 53,096,045 |
| 2026-09-03 | 5 | 0 | 0 | 0 | - | - | 38,949,787 |
| 2026-09-08 | 15 | 0 | 66 | 28 | - | - | 26,581,380 |
| 2026-09-09 | 8 | 0 | 5 | 2 | - | - | 19,195,401 |
| 2026-09-10 | 13 | 0 | 4 | 0 | - | - | 19,544,176 |
| 2026-09-11 | 8 | 0 | 7 | 0 | - | - | 11,467,319 |
| 2026-09-12 | 2 | 0 | 0 | 0 | - | - | 7,757,098 |
| 2026-09-13 | 0 | 0 | 3 | 1 | - | - | 12,069,456 |
| 2026-09-14 | 0 | 0 | 6 | 4 | - | - | 21,354,308 |
| 2026-09-15 | 4 | 0 | 6 | 5 | - | - | 19,241,365 |
| 2026-09-16 | 4 | 0 | 3 | 2 | - | - | 16,586,462 |
| 2026-09-17 | 0 | 0 | 0 | 0 | - | - | 1,514,690 |
| 2026-09-22 | 6 | 0 | 5 | 1 | - | - | 19,252,705 |
| 2026-09-23 | 7 | 0 | 1 | 0 | - | - | 26,057,053 |
| 2026-09-24 | 0 | 0 | 0 | 0 | - | - | 23,124,403 |
| 2026-09-25 | 0 | 0 | 4 | 1 | - | - | 11,155,842 |
| 2026-09-26 | 0 | 0 | 0 | 0 | - | - | 8,052,117 |
| 2026-09-27 | 0 | 0 | 0 | 0 | - | - | 19,848,511 |
| 2026-09-28 | 0 | 0 | 0 | 0 | - | - | 6,607,391 |
| 2026-09-29 | 0 | 0 | 0 | 0 | - | - | 10,494,654 |
| 2026-10-03 | 0 | 0 | 0 | 0 | - | - | 2,079,916 |
| 2026-10-04 | 0 | 0 | 0 | 0 | - | - | 107,511,978 |
| 2026-10-05 | 0 | 0 | 0 | 0 | - | - | 69,857,712 |
| 2026-10-06 | 0 | 0 | 1 | 63 | - | - | - |
| 2026-10-07 | 0 | 0 | 0 | 0 | - | - | 103,830,968 |
| 2026-10-08 | 0 | 0 | 2 | 77 | - | - | 92,108,809 |
| 2026-10-10 | 0 | 0 | 7 | 8 | - | - | - |
| 2026-10-11 | 0 | 0 | 16 | 9 | - | - | - |
| 2026-10-12 | 0 | 0 | 17 | 0 | - | - | 785,963 |
| 2026-10-13 | 0 | 0 | 0 | 0 | - | - | 132,804,266 |
| 2026-10-14 | 0 | 0 | 0 | 36 | - | - | 88,849,426 |
| 2026-10-15 | 23 | 0 | 0 | 44 | - | - | 148,474,623 |
| 2026-10-16 | 0 | 0 | 0 | 0 | - | - | 124,449,227 |
| 2026-10-17 | 0 | 0 | 0 | 0 | - | - | 61,804,567 |
| 2026-10-18 | 1 | 1 | 0 | 139 | 6.3 | 6.8 | 96,097,736 |

## Report-file mtimes

398 report files; 100% have an mtime in the hour starting 2026-10-18T12:00 UTC. A fresh checkout or worktree sets mtimes like this, so here they are checkout times, not write times. They are kept in the ledger but not used above.
