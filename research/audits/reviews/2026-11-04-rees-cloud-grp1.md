# Rees cloud harvest: grp1

- Session: `session_01B1JoCgJUwu3feFkoVCF3FQ` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 06:58 UTC; final message: 2026-11-04 08:32 UTC (last event 08:39)
- Asked: Compute helper for e2k8low: run the parent's e2 solver (C source in the brief) on batches of κ=8 primes from (9769, 20000]; E_2(8) exhaustive-search group 1.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 18.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 16 distinct primes, 0 bad.
- Against `k8dec.txt` / `k9dec.txt`: 17 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=4 p=53 nodes=14 secs=0.00
INFEASIBLE k=8 p=5009 nodes=2234443 secs=0.79
FEASIBLE k=8 p=10313 g=3 beta=0,57,6719,8720,2172,2901,7844,8048 alpha=1,0,2053,7048,2265,7360,9034,9892
FEASIBLE k=8 p=14633 g=3 beta=0,1283,10216,5147,12375,12840,2175,6968 alpha=1,37,5936,13285,14545,7268,13963,1490
FEASIBLE k=8 p=14897 g=3 beta=0,6941,4606,9983,8408,5786,1693,1968 alpha=1,17,10727,952,1287,7079,1861,11220
FEASIBLE k=8 p=14969 g=3 beta=0,3791,8832,10334,13799,8558,257,11526 alpha=1,154,9900,249,871,6780,12776,4925
FEASIBLE k=8 p=15017 g=3 beta=0,9657,10966,1104,7937,9070,14144,4153 alpha=1,245,11354,9239,3936,1297,7891,12675
FEASIBLE k=8 p=15193 g=5 beta=0,11325,3559,2193,5262,12615,7654,5884 alpha=1,56,14170,10073,4722,1791,11562,6376
FEASIBLE k=8 p=15233 g=3 beta=0,9342,4195,6811,5659,10102,13088,5193 alpha=1,261,10883,6510,1077,7589,1991,11914
FEASIBLE k=8 p=15401 g=6 beta=0,5108,14404,5042,13901,5069,9839,580 alpha=1,12,10308,2348,14413,1657,4084,13205
FEASIBLE k=8 p=15817 g=5 beta=0,10037,9179,13454,11190,8670,5142,1453 alpha=1,79,15778,9029,1506,8811,2385,176
FEASIBLE k=8 p=15913 g=5 beta=0,8272,9780,4036,14494,2020,1324,15418 alpha=1,22,15437,2606,12610,13762,10913,2780
FEASIBLE k=8 p=16729 g=13 beta=0,12514,6315,15188,13456,11606,13116,14527 alpha=1,14,7277,10131,9216,10834,6903,7005
FEASIBLE k=8 p=17033 g=3 beta=0,2250,3524,4995,11827,357,7164,900 alpha=1,57,4080,14000,2671,15937,15223,13395
FEASIBLE k=8 p=17321 g=3 beta=0,2536,10656,11655,17183,10539,17117,831 alpha=1,19,638,16098,222,13241,2605,15874
FEASIBLE k=8 p=18089 g=3 beta=0,5884,2235,10163,7247,9434,8415,14232 alpha=1,6,6790,8176,4098,12679,17953,13615
FEASIBLE k=8 p=18329 g=3 beta=0,13423,9904,3390,11377,5390,858,4485 alpha=1,6,7705,14126,8592,5050,12790,16978
FEASIBLE k=8 p=19993 g=10 beta=0,12289,3383,19147,10907,4602,19784,6270 alpha=1,103,5478,7166,5687,7543,13146,1120
```

## Final result message (verbatim)

All 6 primes in the follow-up batch are FEASIBLE: none came out INFEASIBLE and none were left OPEN. I sent the full result lines to the parent session.

- **Run:** as requested, I skipped the 120 s pass and ran the exhaustive `./e2 8 <p>` with no time limit. It ran from a resumable nohup driver, one prime at a time in ascending order, using the same `e2` binary.
- **Run times:** 14633 took 86.4 s, 14897 took 19.9 s, 14969 took 302.3 s, 15017 took 546.2 s, 15193 took 83.6 s and 15233 took 519.9 s.
- **Re-check:** the same Python script as before recomputed the least primitive root and checked all 64 cells for each witness. All 6 passed.
- **Wall time and cores:** 1562 s total (about 26 min) on 4 cores (`nproc`=4).

```
FEASIBLE k=8 p=14633 g=3 beta=0,1283,10216,5147,12375,12840,2175,6968 alpha=1,37,5936,13285,14545,7268,13963,1490
FEASIBLE k=8 p=14897 g=3 beta=0,6941,4606,9983,8408,5786,1693,1968 alpha=1,17,10727,952,1287,7079,1861,11220
FEASIBLE k=8 p=14969 g=3 beta=0,3791,8832,10334,13799,8558,257,11526 alpha=1,154,9900,249,871,6780,12776,4925
FEASIBLE k=8 p=15017 g=3 beta=0,9657,10966,1104,7937,9070,14144,4153 alpha=1,245,11354,9239,3936,1297,7891,12675
FEASIBLE k=8 p=15193 g=5 beta=0,11325,3559,2193,5262,12615,7654,5884 alpha=1,56,14170,10073,4722,1791,11562,6376
FEASIBLE k=8 p=15233 g=3 beta=0,9342,4195,6811,5659,10102,13088,5193 alpha=1,261,10883,6510,1077,7589,1991,11914
```
