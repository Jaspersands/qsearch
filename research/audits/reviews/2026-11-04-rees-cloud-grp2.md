# Rees cloud harvest: grp2

- Session: `session_01B1JoCg8ipTEu395ddCgUWT` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 06:59 UTC; final message: 2026-11-04 08:32 UTC (last event 2026-11-05 01:23)
- Asked: Compute helper for e2k8low (E_2(8) exhaustive-search group 2), same e2 solver.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 19.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 14 distinct primes, 0 bad.
- Against `k8dec.txt` / `k9dec.txt`: 18 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=4 p=53 nodes=14 secs=0.00
INFEASIBLE k=8 p=5009 nodes=2234443 secs=0.71
FEASIBLE k=8 p=10313 g=3 beta=0,57,6719,8720,2172,2901,7844,8048 alpha=1,0,2053,7048,2265,7360,9034,9892
INFEASIBLE k=8 p=12889 nodes=2352297710 secs=360.96
INFEASIBLE k=8 p=13417 nodes=3137244921 secs=485.09
INFEASIBLE k=8 p=13649 nodes=3425608601 secs=529.89
FEASIBLE k=8 p=13921 g=7 beta=0,2900,1514,9743,10093,11967,6941,3752 alpha=1,105,10667,13324,9212,9370,6177,12628
FEASIBLE k=8 p=14057 g=3 beta=0,765,4414,9897,7830,6367,11639,1243 alpha=1,22,871,11838,13576,9603,2425,10560
FEASIBLE k=8 p=14489 g=3 beta=0,10468,1768,3274,9236,1232,8607,2961 alpha=1,44,12517,7775,12073,6876,8618,8644
FEASIBLE k=8 p=15241 g=11 beta=0,3055,8566,2568,710,8220,12066,11280 alpha=1,171,6657,13137,1287,11118,14006,8899
FEASIBLE k=8 p=15737 g=3 beta=0,4977,12317,10389,6083,6335,10112,12776 alpha=1,41,14092,12762,6347,52,32,7122
FEASIBLE k=8 p=15889 g=21 beta=0,3918,1496,12581,14966,11635,13640,4353 alpha=1,42,3093,3604,6656,6747,13664,1233
FEASIBLE k=8 p=16249 g=17 beta=0,10068,4818,1666,14794,2925,6999,13018 alpha=1,138,12095,7070,2043,5028,4566,2732
FEASIBLE k=8 p=16889 g=3 beta=0,5106,12613,5903,3764,1472,7971,13166 alpha=1,52,11191,10045,14930,2074,8120,16598
FEASIBLE k=8 p=17209 g=14 beta=0,5433,5680,13453,15315,13693,13855,9012 alpha=1,82,490,16582,17177,16864,12545,14166
FEASIBLE k=8 p=17657 g=3 beta=0,1387,13662,7667,7611,8193,2553,9566 alpha=1,40,7682,766,3924,1593,12083,13357
FEASIBLE k=8 p=18121 g=23 beta=0,962,16452,2005,13085,4612,8159,3660 alpha=1,57,9988,15112,2128,7367,3272,6975
FEASIBLE k=8 p=18457 g=5 beta=0,6627,11377,18456,2129,14043,2120,15532 alpha=1,0,6144,12732,11428,9826,4262,15157
FEASIBLE k=8 p=19081 g=17 beta=0,12648,17346,1533,8035,1554,5150,17695 alpha=1,35,8208,13504,5962,5382,10643,15834
```

## Final result message (verbatim)

The follow-up batch is finished: three primes are INFEASIBLE and three are FEASIBLE. The results went to the parent session, and the delivery was confirmed.

```
INFEASIBLE k=8 p=12889 nodes=2352297710 secs=360.96
INFEASIBLE k=8 p=13417 nodes=3137244921 secs=485.09
INFEASIBLE k=8 p=13649 nodes=3425608601 secs=529.89
FEASIBLE k=8 p=13921 g=7 beta=0,2900,1514,9743,10093,11967,6941,3752 alpha=1,105,10667,13324,9212,9370,6177,12628
FEASIBLE k=8 p=14057 g=3 beta=0,765,4414,9897,7830,6367,11639,1243 alpha=1,22,871,11838,13576,9603,2425,10560
FEASIBLE k=8 p=14489 g=3 beta=0,10468,1768,3274,9236,1232,8607,2961 alpha=1,44,12517,7775,12073,6876,8618,8644
```

- **Separate re-check:** the Python script passed all 64 cells for each of the three FEASIBLE witnesses.
- **Runs:** same `e2` binary as before (md5 `3d808c16cccc4384ef7084b81a20c46f`). As the parent asked, I skipped the 120 s witness pass and ran only the uncapped searches, one prime at a time.
- **Wall time and cores:** the batch took 1527 s (about 25.5 minutes) on 4 cores (`nproc`=4).
