# 2026-11-07 Attempted break of ALG-T / Theorem A (subquad-A)

Target: `2026-11-07-rees-sde-subquad-A.md`, Theorem A and its algorithm ALG-T. The claim
tested: at M ≥ F(r) = D_J(r) + max(2, 2J−4)·r, ALG-T deterministically reduces any bank to a
solution, or to a leaf satisfying (F1), (F2) and (S). Back substitution (Lemma 2) then succeeds
with probability ≥ 1/2 per pass when p ≥ max(8κ^{2E}E², 2Erκ^E), E = 3J − 2.

Code, outputs and saved banks: `2026-11-07-rees-sde-subquad-A-break/`. Everything is advisory:
these are finite controls, so none of it promotes the theorem.

## Verdict

**Nothing broke.** I saved no counterexample bank because there is none to save.

- **Banks with no stall case:** none. Every stall fell into case 1, 2, 3.0, 3.1, 3.2 or 3.3.
- **Recursion targets with fewer than F(rank) columns:** none.
- **Leaves violating (F1), (F2), (S) or the block rules:** none, as judged by my independent
  checker.
- **Invalid witnesses:** none.
- **Back substitution:** in the theorem's prime range, no bank failed more often than the
  Lemma 2 bound allows. In fact there were 0 failures in 32,190 passes.

Every apparent failure during the work traced to bugs in my own harness. They are documented in
§9 and were all rechecked.

The tightest counts observed are at the boundary but never below it. A recursion target had
exactly F(rank) columns (slack 0) in the case 3.3 U⁺ recursion. The (Y) count reached slack 1
at tiny rank.

## 1. Implementation (independent of `subquad.py`)

I wrote this from the report's text, without copying `subquad.py`.

- `la.py`: mod-p linear algebra on numpy int64, valid for p < 2^31. It contains the κ-th power
  class tables, an incremental RREF and an exact coordinate solver.
- `algt.py`: ALG-T.
  - D_J is computed by brute force from its definition.
  - The forward pass is SSS(J): reserved basis B, greedy circuits mod U, blocks split by the
    "first" rule, the σ swap, pool events, stall.
  - Stall quantities: U, q, b, ε, Fr, Fin, X, Rout, U⁺, q⁺, π, T.
  - Case 1: closure. Case 2: recurse on Y = span(B∩U). Case 3.0: recurse on U⁺.
  - Case 3.1: linear-mod-U × partition matroid intersection with cap c = 2(J−1), plus an
    Edmonds min-max certificate. If the intersection is incomplete, recurse on the Rado flat
    W = U + span(Z).
  - Case 3.2: absorb. Case 3.3: closure on U⁺, or the U⁺ recursion, or the top phase. The top
    phase reserves Z, builds singleton-block circuits, and ends in a leaf or a T_m(b) stall that
    recurses on H_cur.
  - Every count inequality used by the proof is recorded as a named slack. A negative slack
    raises `Fail`.
  - Back substitution follows Lemma 2: τ = −Σ t_σ σ, offsets β per level, Good sets by
    rejection with an exact fallback, coincidences handled, and ρ counted.
- `checker.py`: a separate pure-Python checker that shares no code with `algt.py`.
  - It checks disjoint supports, delta supports, block partition, and that each block lies in
    one class.
  - It checks (F1) and (F2).
  - It checks that Src is nonempty, lies outside the rounds and lies inside U_L.
  - It checks (S) for every cross-class pair.
  - It checks n_l ≤ E, lower rounds ≤ J + c blocks, top rounds ≤ J − 1 blocks and
    singleton-blocked, and ρ ≤ E·dim/2.
  - It verifies every witness.

**Readings chosen where the report is silent.** Where possible I chose the reading most
favourable to the claim and also ran the alternatives in the `conv` group.

- σ is appended at the end of unused. Alternatives run: σ kept at its index, and σ placed at
  random.
- S is sorted. Classes are taken in class order, with ties broken by the first block. An
  alternative with a random split was run.
- The choice of block 0 is immaterial.
- Recursion keeps the columns lying in the flat, in their original order.
- Z is taken from X′ in index order.
- Absorption follows I order. An alternative with a random order was run.
- For the certificate Z I used "can reach X2". The code's complement of "reachable from X1"
  was also run. Both are valid min-max certificates.

## 2. Cross-check against `subquad.py`

I compared stall traces (depth, r, q, b, ε, π) and the multiset of branches. All banks agree.

| run | banks | agree | notes |
|---|---|---|---|
| `cross_1.out` (the agent's Q1 families) | 76 | 76 | |
| `cross_2.out` (my families) | 157 | 157 | 3 generator failures, not compared |
| `out/cross_interesting.log` | 71 | 71 | saved banks that reached rare branches, rank ≤ 40, standard conventions |
| `out/cross_topstall.log` | 4 | 4 | banks reaching T_m(b), ranks 44–50 |

The 71 rare-branch banks include 22 in case 3.0, 16 in 3.1 W, 30 in 3.3 U⁺, 14 in 3.3 closure
and 6 top-phase leaves.

Across both implementations the branches seen are: direct, case 1, reach V, case 2, 3.0,
3.1 W, 3.2, 3.3 closure, 3.3 U⁺, top leaf and T_m(b). On the shared banks my code took about
50 s against about 261 s for `subquad.py`.

## 3. Banks per family and group

Counts are bank-runs: one bank run once through ALG-T and checked. Back-substitution passes
are counted separately.

| group | banks | what |
|---|---|---|
| `fams` (1, 2) | 1647 | 15 families × κ ∈ {2,3} × J ∈ {2,3,4} × r ∈ {8,12,16,20,24,30,40}, p = 10007 / 100003 |
| `conv` | 1875 | the same families under the five alternative conventions |
| `agent` | 352 | the agent's generators (planted 84, vtwist 40, topbank 36, 16 Q1 families × 12), run by my code |
| `thmprime` (1, 3) | 585 + 45 | 315 at primes inside the theorem range, 270 below it |
| `smallp` (2) | 6784 | p ∈ {3,5,7,11,13,17,31} for κ = 2 and {7,13,19,31,37} for κ = 3, J ∈ {2,3,4} |
| `budgetC` (1, rest) | 630 + 90 | the side claim C = max(2, J−3) at J ∈ {4,5} |
| `topstall` (1, rest) | 33 + 21 | stall designs aimed at T_m(b), J ∈ {4,5}, ranks 36–56, including the J = 4, κ = 2 theorem prime |
| climbs (slack, load, top) | 29,477 evaluations | simulated annealing (§5) |
| exhaustive ex2 (a = 2) | 711,417 | see §6 |
| random tiny banks, rnd 2 | 779,140 | a ∈ {3..6}, p ≤ 19, M ∈ {F(a), F(a)+1, F(a)+2} |

The sizes of the first group follow from its grid. The theorem primes used were 32771
(J = 2, κ = 2), 6422531 (J = 3, κ = 2), about 1.875·10^9 (J = 3, κ = 3) and a prime above
838,860,800 (J = 4, κ = 2). J = 4, κ = 3 needs about 2.8·10^12, beyond int64 table range, and
was not run.

Per family, totals across groups, from `summary.json`:

- My families:
  - 215 each: uniform, lines, nested, planted, planted2, repeat.
  - twist 212 (it cannot be generated at r = 8).
  - 305 each: adapt_rado, adapt_top, adapt_mix, adapt_case2.
  - 200 each: design_rado, design_top, design_u30, design_mix.
- Other groups: budgetC 720, small 6784, thm_in 315, thm_below 270, topstall 54.
- The agent's families: planted 84, vtwist 40, topbank 36, and 12 each of 16 Q1 families.

Outcomes over the attack groups: 9909 leaves, 2108 solutions and **0 failures**.

**Topstall note.** Two runs were killed, and the cause was my back-substitution sampler, not
ALG-T:

- `budgetC` at κ = 3, J = 5, r = 24.
- `topstall` at p = 100003, κ = 3, J = 5.

In both, a case 3.2 leaf had a 12-block lower round, which my checker allows (≤ J + c = 13).
At p = 100003 and κ = 3 its Good set is expected to be empty, since p·3^{−12} ≈ 0.19, and the
rejection cap of 200·3^12 draws took about 100 s per pass (`out/diag_budgetC_r24.out`). That
prime is far below the theorem's range, about 3·10^15 for J = 5, κ = 3. Both remainders were
rerun deterministically, with no back-substitution passes for that (κ, J), in `budgetCrest_1`
and `topstallrest_1`.

## 4. Branch coverage

Totals over the attack groups (not climbs or exhaustive runs):

| branch | count |
|---|---|
| calls | 13,992 |
| reach V | 6670 |
| direct solution | 2089 |
| stalls | 5214 |
| case 1 closure | 1533 |
| case 2 (Y) | 1131 |
| 3.0 (U⁺) | 95 |
| 3.1 Rado flat W | 298 |
| 3.2 absorb leaf | 1524 |
| 3.3 closure | 124 |
| 3.3 U⁺ | 446 |
| 3.3 top | 63 |
| top leaf | 58 |
| T_m(b) top-stall recursion | 5 |
| zero column | 19 |

The climbs add 10,948 stalls, including 955 W, 45 in 3.0, 1012 in 3.3 U⁺ and 98 top leaves.

- **T_m(b)** was reached in `topstall` (J = 4, κ = 3, r = 44, and J = 4, κ = 2, r = 47 at the
  theorem prime 838,860,817, with 0 of 20 passes failing) and in budgetC under
  C = max(2, J−3) (J = 4, r = 40; J = 5, r = 24 and 40). The `design_smoke2` banks `ts_0`, `ts_1`
  and `ts_9` (J = 4, r = 46 and 50) also reached it.
- **Not reached:** "direct_top", a witness found inside the top phase.
- **Exhaustive runs at a = 2** reach only direct, reach V and case 1. Rank 2 is too small for
  case 2 or case 3.

## 5. Minimal slacks (smallest value seen over all runs; none negative)

| count | least slack | where it is used |
|---|---|---|
| recursion target count, cols − F(rank) | **0** (3.3 U⁺ recursion), Y 1, W 19, H_cur 18, 3.0 U⁺ 15 | every recursion |
| (Y) b + (C−1)r + D_J(q) − q − F(b) | 1 (tiny a), 2 in the load climb, 6 in `fams` | case 2 |
| Lemma M outside bound | 5 | case 3.1 |
| (I1) | 14 | case 3.1 |
| (I2) / 3.0 outside | 13 / 15 | case 3.0 |
| (TS) | 6 | T_m(b) |
| T_m(b) outside ≤ m + m′ | 2 | T_m(b) |
| T_m(c) m ≤ J−2, load ≤ c, π lower bound, T2(b) round count | 0 (equalities attained, valid) | |
| π ≥ 2 | 2 | stall classification |

The climbs, which minimise the recursion slack, reached rec_count 1, (Y) 2 and W 25. They
pushed the least absorption load to 7 at J = 4 (c = 6) and to 5 at J = 2 (c = 2). Every such
bank went to the Rado flat with enough columns, as the report's §10 says it must (the load alone
is unbounded). No climb produced a failure.

**Exact count lemmas** (`ineq.py`, r ≤ 300, J = 2..12, checked only where the stall can occur):
all hold.

- With the theorem's C, the least slacks are (I1) 14 / 15 / 31, (I2) 12 / 19 / 38, (TS) 5 / 3 / 3
  and (Y) 2 / 2 / 8, for J = 2 / 3 / 4.
- With C = max(2, J−3), J = 4..12, (TS) has slack ≥ 1. That supports the report's side claim.

The report's own check uses wider domains. It has no q ≤ (r−2)/2 or 2m+2 ≤ r restriction, and
there it finds (Y) and (TS) tight at 0. The two results are consistent.

## 6. Exhaustive and massive tiny-parameter search

- **ex2, every multiset of F(2) columns of F_p^2 up to P-scaling:**
  - exhaustive: p = 3 (J = 2: 11,440; J = 3: 6435) and p = 5 (J = 2: 167,960; J = 3: 75,582);
  - sampled, 150,000 each: p = 7 (κ = 2 with J = 2 and J = 3; κ = 3 with J = 3).

  All passed with 0 failures.
- **rnd 2:** 779,140 random banks at a ∈ {3..6}, p ≤ 19, J ∈ {2,3,4}, short-support palettes,
  with M up to F(a)+2. There were 0 failures. The stalls reached case 1, 2, 3.2, 3.3 U⁺ and
  3.3 closure.

## 7. Back substitution vs the Lemma 2 bound

At theorem primes the bound per bank is ρ·max(1/G*, κ/(p−1)), with G* taken from the Lemma W
lower bound. It ranges from about 2·10^−6 to 0.027, far below 1/2. The harness flags any bank whose rate
exceeds bound + 4σ; none was flagged.

| setting | passes | failures | coincidences |
|---|---|---|---|
| theorem range, J = 2, κ = 2 | 18,400 | 0 | 7 |
| theorem range, J = 3, κ = 2 | 4650 | 0 | 0 |
| theorem range, J = 3, κ = 3 | 4300 | 0 | 0 |
| theorem range, J = 4, κ = 2 | 4600 + 240 (topstall) | 0 | 0 |
| below range, J = 2 / J = 3 κ = 2 / J = 3 κ = 3 | 11,500 / 8000 / 4000 | 2 / 1 / 0 | 68 / 1 / 0 |
| `fams` group, p = 10007 / 100003 | 14,440 | 15 | 13 |
| small primes (no bound claimed) | 163,620 | 70,860 | |

At the small primes, failures rise with κ^{n} / p, as Lemma W predicts.

## 8. Discrepancies between the report and its code (`subquad.py`)

None of these affects correctness.

1. The recursion count asserts `len(idx) ≥ F(dim flat)` (line 298). The report states
   "≥ F(rank)". Both coincide, since the flat is spanned by its columns.
2. §9 lists (Y) among the strict asserts, but `subquad.py` has no separate (Y) assert. (Y) is
   covered only through the recursion count at line 298. (TS) is asserted only inside the top
   stall (line 384).
3. The bound of J − 1 blocks for top rounds and the T_m(c) condition m ≤ J − 2 are not
   asserted in `subquad.py`. My checker asserts both, and both held.
4. The min-max certificate is Z = complement of "reachable from X1". The report's text reads
   more naturally as "can reach X2". Both are valid, and my code runs both.
5. The docstring labels for 3.2 and 3.3 differ from the report's table in §6.
6. The §12 table, row (j), claims "smallest recursion slack 15 columns". I observed slack 0 (the 3.3 U⁺
   recursion at exactly F(rank)) and 1 (Y), on branch types that `subquad.py` processes
   identically in the cross-check (§2). The claim is not wrong for the agent's own sample, but it is not a margin.
7. The agent's `planted` generator raises `KeyError 'Ub'` when called directly. I caught it
   as a generator failure.
8. The §12 table, row (b), says "(Y) and (TS) are tight (slack 0)". That holds only on the wider domain of
   `check/ineq_check.py`. Restricted to where the stall can occur, the slacks are ≥ 2 and ≥ 3
   (§5).

## 9. Harness bugs found and fixed (mine, not the report's)

- **Field cache keyed by p only.** In `thmprime_2` and `exhaust rnd 1` a κ = 3 field was reused
  for κ = 2 runs at the same p. This produced 44 and 19 false "failures": block not inside a
  class, x not in P, and a split assertion with 3 classes > J.
  - Fix: key by (p, κ), plus an assert in `run_bank`.
  - All 63 artifact banks were rechecked with the correct field: 46 leaves, 17 solutions,
    0 failures. They are in `harness_bug_thm2/` and `harness_bug_exhaust_rnd/`.
  - The 15 affected keys were removed from `out/thmprime_2.json` (the raw file is kept as
    `out/thmprime_2_raw_with_harness_bug.json.txt`) and rerun as `thmprime_3`: 45 banks,
    0 failures.
- **Generator bugs.** `fam_planted` had an offset that was not advanced, and `planted2` could
  call randrange on an empty range. Both are fixed; the crashed partial run is kept as
  `out/fams_1_crashed.*`.
- **The sampler cap** described in §3.

## 10. Limits and gates

- These are finite controls only: ranks ≤ 56 and J ≤ 5, and J = 4, κ = 3 was not run in the
  theorem range. They do not prove Theorem A, and no theorem is promoted from them.
- Coverage of T_m(b) is thin: only a handful of banks, all J ∈ {4,5}. "direct_top" was never
  reached.
- The randomised part was tested only through observed rates. The Lemma W constant is used,
  not re-derived.
- **Next hard question.** Is there a structured family that makes the 3.3 U⁺ recursion slack
  negative at larger J? It sits at 0 here.
- **Next command.** `climb.py slack` restricted to J ∈ {4,5} with the slack objective set to
  `rec_count_U+33`. Expected artifact: `out/climb_slack_<seed>.json`. Acceptance: its minslack
  for `rec_count_U+33` stays ≥ 0, with every bank checked.

## 11. Mechanical-queue follow-up (9 Nov 2026; finite controls, nothing promoted)

Details and commands: `2026-11-09-mechanical-queue-run.md`. All harness changes are opt-in or additive.

1. **U⁺ recursion slack climb, J ∈ {4, 5}, κ = 2** (`climb_uplus.py`; `out/climb_uplus_J45.json`,
   `out/climb_uplus_J5.json`). Every evaluated bank was run through `algt.py` and `checker.py`:
   8 591 + 15 609 evaluations, 0 failures, 0 violations, no negative slack of any kind. The climb reached
   the case-3.3 U⁺ recursion on 3 538 banks at J = 4 and 364 at J = 5, and the least `rec_count_U+33`
   slack is **0** at both (the recursion target had exactly F(rank) columns), never below. J = 4 climbs
   started from 19 saved banks that reach the branch (`interesting/`); the J = 5 climbs started from the
   families (the J45 run reached the branch only at J = 4, hence the second file).
2. **J = 4, κ = 3 inside the theorem prime range** (`attack_bigp.py`, `la.py` with `QS_BIGP=1`, i.e.
   Python-int arithmetic; `bigp_equiv.py` shows identical traces to the int64 build on 79 banks at
   p < 2³¹: the 22 family banks, which reach none of the case-3.x branches, plus, since 9 Nov (audit
   P6), the 57 saved `interesting/*case33_Uplus*` banks, which reach case 3.3 U⁺ (57), 3.0 U⁺ (25),
   3.1 W (1) and the 3.3 closure (6), but not the top phase; `out/bigp_equiv_{int64,bigp}.json`,
   `out/bigp_equiv_compare.out`, 0 differences. Adding them exposed a `QS_BIGP`-only `IndexError` in
   `algt.good_exact` (object-dtype index), fixed; that function needs the class table, which exists
   only for p ≤ 3·10⁶, so it was unreachable in the theorem-prime run). p = 2 789 427 520 807 ≥ 8·3²⁰·10² (E = 10), 131 banks (12 top-stall designs up to rank 49
   plus the families at r ≤ 24), 120 leaves and 11 direct solutions, **0 assertion/check failures**,
   3 480 back-substitution passes with 0 failures (`out/bigp_J4k3_1.{out,json}`; one `twist` generator
   failure at r = 8, as before). The case-3.3 U⁺ recursion was reached on 4 banks (least `rec_count_U+33`
   slack 0) and case 3.0 U⁺ on 1. The top phase, the top-stall recursion, case 3.1 W and ranks above 49
   were not reached, so the T_m and top-round asserts were not exercised at this prime (BRANCHES line of
   `out/bigp_J4k3_1.out`: `case33_Uplus` 4, `case30_Uplus` 1; no `case33_top`, `top_stall_rec`, `case31_W`,
   `direct_top`). [Corrected 9 Nov per the mechanical-queue audit, P3: the earlier sentence said the
   3.3 U⁺ branch was not reached.]
3. §8 items 2, 3 and 7: `subquad.py` now asserts (Y) (hypothesis r ≥ q + b, the inequality for C ≥ 2, and
   b + π ≥ F(b)), the T_m(c) condition m ≤ J − 2 before the top phase, and the top-round block count
   |S| ≤ m + 1 ≤ J − 1; `run_tests.py: planted()` no longer raises `KeyError 'Ub'` (forward returned
   "direct" before setting `Ub`; 672 parameter combinations now run without error). The eleven test groups
   (planted, topbank, topbank2, vtwist, vtwist2, critical, heavy, stress, fams, thmprime, climb) were rerun with the
   asserts on: identical totals to the stored `*.out` files (vtwist differs only by the later `trace` key).
