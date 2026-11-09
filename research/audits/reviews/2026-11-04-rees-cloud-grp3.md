# Rees cloud harvest: grp3

- Session: `session_01B1JoChU4Szcy34nT6haqDY` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 07:00 UTC; final message: 2026-11-04 08:42 UTC (last event 08:45)
- Asked: Compute helper for e2k8low (E_2(8) exhaustive-search group 3), same e2 solver.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 18.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 13 distinct primes, 0 bad.
- Against `k8dec.txt` / `k9dec.txt`: 17 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=4 p=53 nodes=14 secs=0.00
INFEASIBLE k=8 p=5009 nodes=2234443 secs=0.85
FEASIBLE k=8 p=10313 g=3 beta=0,57,6719,8720,2172,2901,7844,8048 alpha=1,0,2053,7048,2265,7360,9034,9892
FEASIBLE k=8 p=12953 g=3 beta=0,11639,3843,2004,2228,4429,10942,7894 alpha=1,99,7277,3932,5924,1948,7312,11737
INFEASIBLE k=8 p=13313 nodes=3027222373 secs=569.63
FEASIBLE k=8 p=13729 g=23 beta=0,2753,514,9002,11027,6615,276,4089 alpha=1,69,5665,10899,2486,11002,8967,7124
FEASIBLE k=8 p=14009 g=3 beta=0,10318,2794,12601,11107,2595,13839,1701 alpha=1,60,10949,9481,4624,10559,10689,8616
INFEASIBLE k=8 p=14177 nodes=4517071449 secs=846.68
INFEASIBLE k=8 p=14281 nodes=4822131865 secs=916.83
FEASIBLE k=8 p=15641 g=3 beta=0,14323,11017,15232,13916,2277,6567,3829 alpha=1,31,12695,4754,6190,5018,15383,8374
FEASIBLE k=8 p=15881 g=3 beta=0,3407,488,8688,13086,7616,3809,11831 alpha=1,0,12948,3883,4157,14353,12474,15847
FEASIBLE k=8 p=16553 g=3 beta=0,8027,14761,10203,7274,8566,3496,6516 alpha=1,45,1698,15740,11835,8684,7410,10584
FEASIBLE k=8 p=16921 g=17 beta=0,7418,1539,6583,2500,14887,13302,12933 alpha=1,34,9490,1726,12502,11819,2105,1031
FEASIBLE k=8 p=17257 g=5 beta=0,12483,16628,14453,6767,8548,15605,5653 alpha=1,166,15199,14828,14809,5302,1921,8236
FEASIBLE k=8 p=18041 g=3 beta=0,4806,16911,7471,17718,4645,6784,7764 alpha=1,0,4818,11257,4292,3062,16634,2751
FEASIBLE k=8 p=18169 g=11 beta=0,13243,17584,5785,10100,3810,15325,13151 alpha=1,46,6994,14018,13965,6115,9940,5338
FEASIBLE k=8 p=18521 g=3 beta=0,4525,9018,13526,8597,16093,2679,957 alpha=1,58,8206,6715,12279,3423,9143,12071
FEASIBLE k=8 p=18553 g=5 beta=0,3274,5917,3586,14277,417,8745,7206 alpha=1,11,8376,18234,8502,16143,16365,5746
```

## Final result message (verbatim)

The follow-up batch is finished: 3 primes are FEASIBLE and 3 are INFEASIBLE. I sent these lines to the parent session.

```
FEASIBLE k=8 p=12953 g=3 beta=0,11639,3843,2004,2228,4429,10942,7894 alpha=1,99,7277,3932,5924,1948,7312,11737
INFEASIBLE k=8 p=13313 nodes=3027222373 secs=569.63
FEASIBLE k=8 p=13729 g=23 beta=0,2753,514,9002,11027,6615,276,4089 alpha=1,69,5665,10899,2486,11002,8967,7124
FEASIBLE k=8 p=14009 g=3 beta=0,10318,2794,12601,11107,2595,13839,1701 alpha=1,60,10949,9481,4624,10559,10689,8616
INFEASIBLE k=8 p=14177 nodes=4517071449 secs=846.68
INFEASIBLE k=8 p=14281 nodes=4822131865 secs=916.83
```

- **Witness checks:** the three FEASIBLE witnesses passed the same independent Python check as before (primitive root plus all 64 cells).
- **How it ran:** as requested, I skipped the 120 s pass. Each prime got the uncapped `./e2 8 <p>` run, one at a time in ascending order, from the resumable nohup driver. I used the same e2 binary as the first batch and made no repo changes.
- **Time and cores:** total wall time was 2497 s (about 42 min) on 4 cores (nproc=4).
