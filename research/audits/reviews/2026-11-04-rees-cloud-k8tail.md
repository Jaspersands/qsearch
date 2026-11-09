# Rees cloud harvest: k8tail

- Session: `session_01B1JoCiJqLa7zn8TwVNDiGq` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 01:24 UTC; final message: 2026-11-04 06:45 UTC (last event 2026-11-05 01:23)
- Asked: Run dfs2b (sha256 b7afe1c3...) for κ=8 on [20001, 60000]. It split the work onto six sibling sessions (s26..s56) and later handed its unfinished tail primes to s44, s50, s56. Later user messages asked what else cloud credits could do.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 1020.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 2 distinct primes, 0 bad.
- Witness lines that were truncated in the transcript (verdict only, witness not checkable here; the witness exists only in the cloud container): 79 primes: 20089, 20113, 20129, 20353, 21001, 21121, 21601, 21617, 21649, 21673, 21713, 21737, 21817, 21841, 21881, 21929, 21937, 21961, 21977, 22129, 22153, 22441, 22481, 22697, 22721, 22769, 22777, 22817, 22921, 22937, 22961, 22993, 23081, 23297, 24097, 24113, 24121, 24137, 24169, 24281, 24329, 24337, 24473, 24481, 24593, 24697, 24793, 24809, 24841, 24889, 24953, 24977, 25057, 25073, 25097, 25121, 25153, 25169, 25321, 25409, 25457, 25537, 25561, 25577, 25601, 25609, 25633, 25657, 25673, 25793, 25801, 25841, 25849, 25873, 25889, 25913, 25969, 59009, 59113.
- Against `k8dec.txt` / `k9dec.txt`: 154 agree, 0 conflict, 814 not in the local decided files.
  New entries (all ['FEASIBLE'] for κ=[8]), p from 20113 to 59929.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=8 p=4217 nodes=350972 secs=3.292 ; INFEASIBLE k=8 p=4241 nodes=368188 secs=2.780
INFEASIBLE k=8 p=4241 nodes=368188 secs=3.581
FEASIBLE k=8 p=5641 g=14 nodes=2958013 secs=25.916 beta=0,5640,4023,1729,4220,100,2198,3552 alpha=1,3443,1112,2910,4592,778,1915,3189
INFEASIBLE k=8 p=5657 nodes=2835157 secs=25.473
INFEASIBLE k=9 p=7723 nodes=1743317 secs=31.142
FEASIBLE k=8 p=20089 g=7 nodes=8102275 secs=242.874 beta=0,41,3223,19684,1164,13485,11613,
FEASIBLE k=8 p=20113 g=10 nodes=406495 secs=11.891 beta=0,38,126,17351,8328,7128,6383,1063
FEASIBLE k=8 p=20129 g=3 nodes=10766172 secs=314.386 beta=0,5,3644,13335,5274,10423,5544,1
FEASIBLE k=8 p=20353 g=5 nodes=182666 secs=5.435 beta=0,14,6
FEASIBLE k=8 p=21001 g=11 nodes=7901255 secs=231.610 beta=0,
FEASIBLE k=8 p=21121 g=19 nodes=18080052 secs=530.176 beta=0
FEASIBLE k=8 p=21601 g=7 nodes=51438448 secs=1830.459
FEASIBLE k=8 p=21617 g=3 nodes=969099 secs=32.235
FEASIBLE k=8 p=21649 g=14 nodes=9695517 secs=328.398
FEASIBLE k=8 p=21673 g=10 nodes=33295488 secs=1196.031
FEASIBLE k=8 p=21713 g=3 nodes=9524152 secs=317.861
FEASIBLE k=8 p=21737 g=6 nodes=851522 secs=29.722
FEASIBLE k=8 p=21817 g=7 nodes=80899843 secs=2876.189
FEASIBLE k=8 p=21841 g=11 nodes=617395 secs=25.578
FEASIBLE k=8 p=21881 g=3 nodes=3157654 secs=121.145
FEASIBLE k=8 p=21929 g=3 nodes=12258662 secs=479.793
FEASIBLE k=8 p=21937 g=7 nodes=13162319 secs=458.369
FEASIBLE k=8 p=21961 g=17 nodes=29119722 secs=1025.918
FEASIBLE k=8 p=21977 g=3 nodes=12010585 secs=426.078
FEASIBLE k=8 p=22129 g=19 nodes=43506261 secs=1238.995 beta=
FEASIBLE k=8 p=22153 g=5 nodes=46837975 secs=1388.552 beta=0
FEASIBLE k=8 p=22441 g=14 nodes=5484781 secs=163.627 beta=0,34,868,2378,21273,27
FEASIBLE k=8 p=22481 g=3 nodes=5097467 secs=151.349 beta=0,10,816,22392,9857,205
FEASIBLE k=8 p=22697 g=3 nodes=61958445 secs=2195.024
FEASIBLE k=8 p=22721 g=3 nodes=15548852 secs=553.297
FEASIBLE k=8 p=22769 g=3 nodes=40197963 secs=1435.692
FEASIBLE k=8 p=22777 g=7 nodes=9908280 secs=354.276
FEASIBLE k=8 p=22817 g=3 nodes=11840763 secs=416.757
FEASIBLE k=8 p=22921 g=7 nodes=1369029 secs=50.132
FEASIBLE k=8 p=22937 g=3 nodes=112096100 secs=4185.522
FEASIBLE k=8 p=22961 g=6 nodes=23510303 secs=861.578
FEASIBLE k=8 p=22993 g=5 nodes=12237514 secs=446.057
FEASIBLE k=8 p=23081 g=3 nodes=5579942 secs=165.972 beta=0,1
FEASIBLE k=8 p=23297 g=3 nodes=170780 secs=5.278 beta=0,5,31
FEASIBLE k=8 p=24097 g=5 nodes=1083268 secs=30.919
FEASIBLE k=8 p=24113 g=3 nodes=8714196 secs=241.319
FEASIBLE k=8 p=24121 g=13 nodes=9099423 secs=258.191
FEASIBLE k=8 p=24137 g=3 nodes=4898846 secs=139.917
FEASIBLE k=8 p=24169 g=11 nodes=233450 secs=7.353
FEASIBLE k=8 p=24281 g=3 nodes=296768 secs=8.765
FEASIBLE k=8 p=24329 g=3 nodes=1545342 secs=42.894
FEASIBLE k=8 p=24337 g=5 nodes=13623861 secs=374.836
FEASIBLE k=8 p=24473 g=3 nodes=19840441 secs=552.059
FEASIBLE k=8 p=24481 g=11 nodes=16880966 secs=480.165
FEASIBLE k=8 p=24593 g=3 nodes=4096345 secs=115.756
FEASIBLE k=8 p=24697 g=5 nodes=29930779 secs=836.147
FEASIBLE k=8 p=24793 g=5 nodes=125410 secs=3.487
FEASIBLE k=8 p=24809 g=6 nodes=894258 secs=24.139
FEASIBLE k=8 p=24841 g=14 nodes=27229549 secs=770.443
FEASIBLE k=8 p=24889 g=11 nodes=67053958 secs=1872.424
FEASIBLE k=8 p=24953 g=3 nodes=5215904 secs=146.266
FEASIBLE k=8 p=24977 g=3 nodes=1203808 secs=34.581
FEASIBLE k=8 p=25057 g=5 nodes=227704 secs=11.817
FEASIBLE k=8 p=25073 g=3 nodes=31173842 secs=1274.569
FEASIBLE k=8 p=25097 g=3 nodes=45519703 secs=1877.911
FEASIBLE k=8 p=25121 g=3 nodes=21504940 secs=880.543
FEASIBLE k=8 p=25153 g=10 nodes=4016480 secs=169.837
FEASIBLE k=8 p=25169 g=3 nodes=108942 secs=3.754
FEASIBLE k=8 p=25321 g=19 nodes=7479360 secs=324.670
FEASIBLE k=8 p=25409 g=3 nodes=42838 secs=1.760
FEASIBLE k=8 p=25457 g=3 nodes=651947 secs=27.665
FEASIBLE k=8 p=25537 g=10 nodes=278314 secs=12.532
FEASIBLE k=8 p=25561 g=11 nodes=105779 secs=4.426
FEASIBLE k=8 p=25577 g=3 nodes=11298455 secs=473.493
FEASIBLE k=8 p=25601 g=3 nodes=1543312 secs=61.566
FEASIBLE k=8 p=25609 g=7 nodes=4707520 secs=193.764
FEASIBLE k=8 p=25633 g=5 nodes=10251680 secs=427.386
FEASIBLE k=8 p=25657 g=5 nodes=1871373 secs=80.643
FEASIBLE k=8 p=25673 g=3 nodes=31983683 secs=1328.944
FEASIBLE k=8 p=25793 g=3 nodes=440297 secs=13.328 beta=0,4,21,25066,7501,2351,12
FEASIBLE k=8 p=25801 g=7 nodes=1147718 secs=35.962
FEASIBLE k=8 p=25841 g=3 nodes=2494216 secs=77.685
FEASIBLE k=8 p=25849 g=7 nodes=70365239 secs=2153.098
FEASIBLE k=8 p=25873 g=10 nodes=6397747 secs=200.745
FEASIBLE k=8 p=25889 g=3 nodes=4493279 secs=138.200
FEASIBLE k=8 p=25913 g=3 nodes=317875 secs=9.511
FEASIBLE k=8 p=25969 g=7 nodes=20679256 secs=633.141
FEASIBLE k=8 p=28001 g=3 nodes=52671 secs=1.547 beta=0,36,12,2003,5071,4296,12914,8333 alpha=1,22186,15781,6428,11464,4650,3393,20536
FEASIBLE k=8 p=59009 g=3 nodes=98856 secs=7.517 beta=0,5,1,406,8797,8350,28534,6841 alpha=
FEASIBLE k=8 p=59113 g=7 nodes=5905 secs=0.494 beta=0,12,16,29,8805,39027,5234,8625 alpha=
```

## Final result message (verbatim)

# E_2(8) scan of [20001, 60000]: no exceptional primes

E_2(8) has no element in [20001, 60000]. All 935 primes p ≡ 1 (mod 8) in the range came out FEASIBLE. No prime returned INFEASIBLE, LIMIT, BUG or UNEXPECTED_EMPTY, and none is unresolved. Nothing was written to the repo, committed or pushed.

## Commands and sanity checks
```bash
mkdir -p ~/dfs2run && cd ~/dfs2run   # dfs2b.c saved exactly; sha256 b7afe1c349e2d654596e657616e8b22e0872f14710d9ce45ce0d9a07bef96c34
cc -O2 -o dfs2b dfs2b.c
```
```bash
for a in $(seq 20001 1000 59001); do echo "$a $((a+999))"; done | xargs -P$(nproc) -n2 sh -c './dfs2b 8 $0 $1 4000000000 print > out/c_$0_$1.txt 2>&1'
```
The sanity checks gave these lines. The node counts match the expected values exactly:
```
INFEASIBLE k=8 p=4217 nodes=350972 secs=3.701
INFEASIBLE k=8 p=4241 nodes=368188 secs=3.581
INFEASIBLE k=8 p=5657 nodes=2835157 secs=25.473
INFEASIBLE k=9 p=7723 nodes=1743317 secs=31.142
FEASIBLE k=8 p=5641 g=14 nodes=2958013 secs=25.916 beta=0,5640,4023,1729,4220,100,2198,3552 alpha=1,3443,1112,2910,4592,778,1915,3189
INFEASIBLE k=8 p=4217 nodes=6706519 secs=27.051        (plain mode)
```
Each sibling session checked the same source hash and reproduced the 4217 and 4241 node counts exactly before scanning.

## How the range was split
Two hours in, this session was the bottleneck at 4 cores, so I split the work:
- **6 sibling sessions,** 4 cores each, took 26001–60000. They ran the same program with the same chunking.
- **This session** kept 20001–26000.
- **Tail primes:** the high ranges finished in minutes, so three idle siblings took over the 57 primes still queued in this session's unfinished chunks. Each ran as its own `./dfs2b 8 p p 4000000000 print` process. This session's chunks were stopped only after their current prime had finished, so nothing ran twice and nothing was skipped.

## Results
- **INFEASIBLE in [20001, 60000]:** none.
- **Unresolved LIMIT primes:** none, so no rerun at 40000000000 was needed. No prime came near 4 hours.
- **DONE lines:**
```
DONE k=8 range=[20001,21000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[23001,24000] feasible=27 infeasible=0 limit=0 mode=full
DONE k=8 range=[26001,27000] feasible=31 infeasible=0 limit=0 mode=full
DONE k=8 range=[27001,28000] feasible=22 infeasible=0 limit=0 mode=full
DONE k=8 range=[28001,29000] feasible=21 infeasible=0 limit=0 mode=full
DONE k=8 range=[29001,30000] feasible=21 infeasible=0 limit=0 mode=full
DONE k=8 range=[30001,31000] feasible=24 infeasible=0 limit=0 mode=full
DONE k=8 range=[31001,32000] feasible=23 infeasible=0 limit=0 mode=full
DONE k=8 range=[32634,33000] feasible=5 infeasible=0 limit=0 mode=full
DONE k=8 range=[33522,34000] feasible=14 infeasible=0 limit=0 mode=full
DONE k=8 range=[34722,35000] feasible=6 infeasible=0 limit=0 mode=full
DONE k=8 range=[35898,36000] feasible=3 infeasible=0 limit=0 mode=full
DONE k=8 range=[36001,37000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[37001,38000] feasible=23 infeasible=0 limit=0 mode=full
DONE k=8 range=[38001,39000] feasible=24 infeasible=0 limit=0 mode=full
DONE k=8 range=[39001,40000] feasible=20 infeasible=0 limit=0 mode=full
DONE k=8 range=[40001,41000] feasible=20 infeasible=0 limit=0 mode=full
DONE k=8 range=[41001,42000] feasible=27 infeasible=0 limit=0 mode=full
DONE k=8 range=[42001,43000] feasible=26 infeasible=0 limit=0 mode=full
DONE k=8 range=[43001,44000] feasible=21 infeasible=0 limit=0 mode=full
DONE k=8 range=[44001,45000] feasible=22 infeasible=0 limit=0 mode=full
DONE k=8 range=[45001,46000] feasible=23 infeasible=0 limit=0 mode=full
DONE k=8 range=[46001,47000] feasible=16 infeasible=0 limit=0 mode=full
DONE k=8 range=[47001,48000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[48001,49000] feasible=23 infeasible=0 limit=0 mode=full
DONE k=8 range=[49001,50000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[50001,51000] feasible=22 infeasible=0 limit=0 mode=full
DONE k=8 range=[51001,52000] feasible=23 infeasible=0 limit=0 mode=full
DONE k=8 range=[52001,53000] feasible=27 infeasible=0 limit=0 mode=full
DONE k=8 range=[53001,54000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[54001,55000] feasible=20 infeasible=0 limit=0 mode=full
DONE k=8 range=[55001,56000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[56001,57000] feasible=25 infeasible=0 limit=0 mode=full
DONE k=8 range=[57001,58000] feasible=21 infeasible=0 limit=0 mode=full
DONE k=8 range=[58001,59000] feasible=24 infeasible=0 limit=0 mode=full
DONE k=8 range=[59001,60000] feasible=22 infeasible=0 limit=0 mode=full
```
In addition there are 65 single-prime DONE lines, all of the form `DONE k=8 range=[p,p] feasible=1 infeasible=0 limit=0 mode=full`. They cover these primes:
- **Run in this session:** 25793–25969 (8 primes).
- **Run on siblings:** 21601–21977 and 22697–22993 (22 primes), 24097–24977 (18), and 25057–25673 (17).

## Coverage: no gaps
Ten chunks have no DONE line of their own, for two different reasons:

| Chunk | Why there is no DONE line | Finished part (FEASIBLE lines) | Remainder covered by |
|---|---|---|---|
| 21001–22000 | stopped here after its current prime | 21001–21577 (15) | single-prime runs on a sibling |
| 22001–23000 | stopped here after its current prime | through 22481 (10) | single-prime runs on a sibling |
| 24001–25000 | stopped here after its current prime | 24001, 24049 (2) | single-prime runs on a sibling |
| 25001–26000 | stopped here after its current prime | 25033 (1) | single-prime runs, here and on a sibling |
| 32001–33000 | sibling container restarted mid-run | 32001–32633 (18) | resumed chunk [32634, 33000] |
| 33001–34000 | sibling container restarted mid-run | 33001–33521 (11) | resumed chunk [33522, 34000] |
| 34001–35000 | sibling container restarted mid-run | 34001–34721 (16) | resumed chunk [34722, 35000] |
| 35001–36000 | sibling container restarted mid-run | 35001–35897 (21) | resumed chunk [35898, 36000] |

The partial outputs from all ten chunks were kept.

I counted the primes p ≡ 1 (mod 8) independently in Python and compared each range with its results:

| Range | Primes | Results |
|---|---|---|
| 20001–26000 | 145 | 145, merged from all sources: none missing, no duplicates |
| 26001–32000 | 142 | 142 |
| 32001–38000 | 142 | 142 |
| 38001–44000 | 138 | 138 |
| 44001–50000 | 134 | 134 |
| 50001–56000 | 142 | 142 |
| 56001–60000 | 92 | 92 |

The total is 935, so [20001, 60000] is covered with no gaps.

## Slowest FEASIBLE prime
- **Slowest:** p=22937, with nodes=112096100 and secs=4185.5 (about 70 minutes).
- **Next slowest:** p=21577 (3883 s) and p=22433 (2971 s).
- **Above 26000:** no prime took longer than 1444 s (p=26833). Above about 44000, no prime took more than about 185 s.

## Wall time and cores
- **Wall time:** about 4.8 hours, from 1793756243 to 1793773540, 17297 s in total.
- **Cores:** 4 cores here for the whole run, plus 6 siblings × 4 cores from about 2 hours in. That makes 28 cores at peak.

## What is not covered
- **The range itself:** every prime p ≡ 1 (mod 8) in [20001, 60000] has a result.
- **Below 20001:** not checked here; your local machine is scanning [4202, 20000].
- **Above 60000:** not checked.
- **Witnesses:** the `beta`/`alpha` witnesses for the 65 single primes run on siblings exist only in those siblings' containers.

The six sibling sessions are finished and idle. I can archive them if you no longer need their files.
