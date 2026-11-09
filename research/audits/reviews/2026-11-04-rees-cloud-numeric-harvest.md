# Rees cloud numeric harvest: E_2(8) and E_2(9) sessions of 2-5 Nov 2026

AI-only, pending human review. Harvested 2026-11-05 (~22:30 AEDT) from 16 claude.ai/code cloud
sessions by reading their event streams. Nothing was committed or pushed, and the paper was not
edited. Per-session files are `2026-11-04-rees-cloud-<key>.md`, plus `2026-11-02-rees-cloud-dfs2_k89.md`.
Each file holds the final result message verbatim, with a checksum match against the stream, and
every extracted verdict line. The sweep8 witness lines are in `2026-11-04-rees-cloud-sweep8-witnesses.txt`.

Method:
- Every complete FEASIBLE/FOUND witness was re-verified with `wcheck.py`, which recomputes the
  least primitive root and checks all κ² cells by the power test.
- Every verdict was compared with the local decided lists `k8dec.txt` (677 primes) and
  `k9dec.txt` (1790114 primes). These are verdict lines, verdicts stated in prose, and verdicts
  claimed for whole ranges.
- No cloud session printed a κ=9 FEASIBLE witness, so `verify_k9.py` was not needed.

## Per session

| key | asked | decided (cloud claim) | witnesses re-verified | conflicts | new vs local lists |
|---|---|---|---|---|---|
| e2k8low | 145 undecided κ=8 primes in (9769, 20000], own solver | all 145: 110 FEAS, 35 INF (max 14281); also 1553, 3089, 3121 FEAS | 112/112 ok (incl. 9697, 1553) | 0 | 0 |
| grp1 | helper of e2k8low, same e2.c | 16 FEAS, 5009 INF | 16/16 ok | 0 | 0 |
| grp2 | helper | 14 FEAS; INF 5009, 12889, 13417, 13649 | 14/14 ok | 0 | 0 |
| grp3 | helper | 13 FEAS; INF 5009, 13313, 14177, 14281 | 13/13 ok | 0 | 0 |
| indep | independent solver: 9769, 9473 (κ=8), 17623 (κ=9) | INF 9769, 9473, 6073 (κ=8); INF 17623, 6067 (κ=9); FEAS 9697; E_2(4), E_2(5) match | 9697 witness ok | 0 | 0 |
| k8tail | dfs2b κ=8 on [20001, 60000] (split onto s26..s56) | all 935 primes FEAS, no INF/LIMIT | 2 ok (5641, 28001); 79 lines truncated | 0 | 814 FEAS (20113-59929) |
| s26 | dfs2b [26001, 32000] | 142 FEAS | 1 ok; 5 truncated | 0 | 103 FEAS |
| s32 | dfs2b [32001, 38000] | 142 FEAS (resumed after a restart) | 0; 4 truncated | 0 | 125 FEAS |
| s38 | dfs2b [38001, 44000] | 138 FEAS | none printed | 0 | 133 FEAS |
| s44 | dfs2b [44001, 50000] + 22 tail primes | 134 + 22 FEAS | 6 ok; 22 truncated | 0 | 147 FEAS |
| s50 | dfs2b [50001, 56000] + 18 tail primes | 142 + 18 FEAS | 0; 21 truncated | 0 | 150 FEAS |
| s56 | dfs2b [56001, 60000] + 17 tail primes | 92 + 17 FEAS | 0; 17 truncated | 0 | 104 FEAS |
| hard29 | the 29 hard κ=8 primes in (20000, 49417], own solver | all 29 FEAS; 9473, 9769 INF | 31/31 ok (29 + 9697 + 22921) | 0 | 0 |
| sweep8 | κ=8 witness sweep over (8^8/2, 1.17e8] | all 1528786 primes in (8388608, **117000000**] FEAS (strict) | 101/101 sample lines ok | 0 | 100 FEAS (samples) |
| k9_100k | plain dfs2 κ=9 on [20001, 100000] | nothing: 20071, 20089, 20107, 20143 unresolved after 3 h each | none | 0 | 0 |
| dfs2_k89 (11-02) | plain dfs2 scans, κ=8 from 4058, κ=9 from 5690 | INF κ=8 4049-5441 (24 primes), FEAS 4657, 5233; INF κ=9 5743-6949 (13); κ=7 3221 INF | none printed | 0 | 0 |

## Totals

- **Witnesses:** 250 distinct primes have a complete witness. All of them pass, with 0 bad. That is
  296 witness lines, plus the transposed 9697 witnesses of indep and hard29 and a second
  witness for 8388617.
- **Witnesses not captured:** 83 FEASIBLE primes in (20000, 60000] had their witness line cut
  off in the transcript. Their witnesses exist only in the cloud containers.
- **Conflicts:** 0, over every κ=7, 8 and 9 verdict.
- **New decisions relative to `k8dec`/`k9dec`:** 914, all κ=8 FEASIBLE. 814 lie in (20000, 60000]
  and 100 are sweep samples in (8^8/2, 1.17e8]. There are none ≤ 20000, no new INFEASIBLE
  prime anywhere, and no new κ=9 decision. In particular no κ=9 exception prime above 20000 was
  decided in the cloud.
- **None of the 914 is new to the paper.** Local explicit contractions already cover
  (20000, ⌈T_A(8)⌉] (`2026-11-04-rees-threshold-5.md`, `2026-11-04-rees-t1-sweep-hi.md`).
  The 914 are only absent from `k8dec.txt`.

## What this changes for STATE.md (no numbers change)

1. **Second, independent implementations now agree with dfs2b:**
   - **indep:** a forward-checking solver with no symmetry pruning (`e2ind.c`). It re-decides
     9473, 9769 ∈ E_2(8) and 17623 ∈ E_2(9), plus 6073 and 6067. It needed about 13× more nodes
     than dfs2b.
   - **hard29:** a rows-first solver (`rows.c`) with a different symmetry rule. It re-decides
     9473 and 9769, checked with the prune off and by a second solver.
   - **e2k8low:** a CSP solver (`e2.c`) with arc consistency and a different symmetry key. It
     re-decides all 145 primes of (9769, 20000] that were undecided on 11-04, with the same
     35/110 split as local dfs2b. Its helpers grp1-3 ran the same code, so they are not
     independent of e2k8low.
   - So the paper's sentence that each decided verdict "rests on a single run of the pruned
     search" is now out of date for these primes. The paper is not edited here.
2. **sweep8 re-derives the T_A sweep by a different method** (small-integer cosets, randomized
   DFS). Its range is (8^8/2, 117000000], not ⌈T_A(8)⌉ = 117441563. About 5929 primes in
   (117000000, 117441563] are covered only by the local t1-sweep-hi. The correction was never
   delivered to this session, because it received one user message.
3. **k8tail plus six siblings ran dfs2b exhaustively over all 935 κ=8 primes in [20001, 60000].**
   All are FEASIBLE, which is consistent with E_2(8) ⊆ [3, 20000]. Complete witnesses were
   captured for only 30 distinct primes in (20000, 60000], and most of those come from hard29.
4. **Plain dfs2 is out of reach for κ=9 above 20000.** At p=20071 it runs at about 520 nodes/s,
   so the full range would take 38 or more days on 4 cores. The open κ=9 exception primes need
   dfs2b or a faster solver.
