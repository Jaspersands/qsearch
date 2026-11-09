# Mechanical queue run, 9 Nov 2026 (AI only; no git; paper untouched)

One session worked through the top of `research/MECHANICAL_FOLLOW_UP_PLAN.md`. Everything is a
finite control or a text/code alignment: no new mathematical claim, no proof conclusion changed.
Interpreter `/opt/anaconda3/bin/python`, `nice -n 19`, no computation above about 25 CPU minutes.
`lrat-check` was taken from another session's scratchpad (`LRAT_CHECK` env). [9 Nov audit: that build was
unsound (it accepted an empty clause without a conflict); `2026-11-09-lrat-and-audit-fixes.md` lists which
results below were re-verified with the fixed checker and which are now CaDiCaL UNSAT, not independently
proof-checked.]

## Status by plan item

| section / item | status | artifact |
|---|---|---|
| SDE Open Directions 1 (wnest.py discrepancies) | DONE | `2026-11-08-rees-sde-p3-nest/wnest.py`; `tables.out` identical numbers; `…-nest-break/crosscheck_wnest_fixed.{py,out}` |
| Open Directions 2 (k = 4 SAT; (6,2), (7,1)) | DONE | `…-p3-nest/pattern_sat_k4.out` (all UNSAT, LRAT-verified; re-verified with the fixed checker, 9 Nov); `…-break/lemma_exhaustive2.out` already complete |
| Open Directions 3 (text per referee) | DONE | `2026-11-08-rees-sde-p3-nest.md` |
| Worst Case Below a² 1 (U⁺ climb J ∈ {4,5}) | DONE | `…-subquad-A-break/climb_uplus.py`, `out/climb_uplus_J45.json`, `out/climb_uplus_J5.json` |
| Worst Case 2 (J = 4, κ = 3, theorem prime) | DONE | `attack_bigp.py`, `la.py` (`QS_BIGP=1`), `bigp_equiv.py`, `out/bigp_J4k3_1.*` |
| Worst Case 3 (KeyError, asserts) | DONE | `…-subquad-A/subquad.py`, `run_tests.py` |
| 2026-11-09 SDE F_q Referees 1, 2 | DONE | `2026-11-08-rees-sde-fq-nest.md`; `tests/test_rees_sde_p5_simple.py` |
| 2026-11-09 SDE F_q Extension 1-3 | DONE | `check_split_cover.py/.out`, `tests/test_rees_sde_fq_cnf5.py`, folder `README.md` |
| 2026-11-09 Exponent p^e 1 | DONE | `tests/test_rees_exponent_pe_blackbox.py` |
| 2026-11-09 Square Gap 1 | DONE | `…-square-gap-stepanov/e2dfs_k89.out` |
| Square Gap 2 (κ = 5 table, p ≤ 2628) | BLOCKED (compute) | see below |
| Square Gap 3 (Lean port) | no action | owner has not asked |
| 2026-11-08 Black-Box Corollary | skipped (already DONE) | |

## Open Directions

- **wnest.py.** `Run.run` default `qmin_kow` 3 → 4; `kow_round` uses pool q + 1 (instead of
  q + ⌈log₃(q+1)⌉) in `wnest`/`wnest+` modes, keeping KOW's pool in the baseline `kow` mode. Result: the
  code's worst-case recursion is `guarantee(n)` (the +2 for odd n is gone). `tables.py` rerun: output identical
  to the old one (guarantee 133, 422, 1433, 3242, … and closed-form check for 4 ≤ n < 3000); `wnest.py`
  rerun: identical (those n are even). Cross-check `crosscheck_wnest_fixed.out`: `wnest.py` against
  `strict_wnest.py` variant `proof` on the same 60 instances: pulled columns equal in all 60; 24 "divergences"
  are an extra logged KOW tuple on the terminating round (22) or a different but valid witness from KOW
  tie-breaking (2), the same kinds as in the earlier cross-check.
- **Pattern SAT.** `pattern_sat.py` got a `solver='cadical'` option (DIMACS, LRAT proof, accepted only after
  lrat-check); `pattern_sat_k4.py` uses it. Results: k = 4 all 80 patterns UNSAT (150 s); 54 patterns
  (δ₁ full support) UNSAT (839 s); 36 patterns UNSAT (1486 s); k = 3, 12 patterns UNSAT (60 s) [all four
  proofs re-verified with the fixed checker, 9 Nov]. The earlier
  stopped pycosat output is kept as `pattern_sat_k4.pycosat_stopped.out`. Lemma M+D (6,2) and (7,1) had
  already finished in `lemma_exhaustive2.out` (529 984 and 2 186 bases; total 1 893 220 bases, 0 failures);
  recorded in the break report.
- **Text.** In `…-p3-nest.md`: dual distance ≥ 2 after peeling (variance 4N*/9 tight; true dual distance ≥ 3
  would give 2N*/9); the KOW comparison now names the note's sharpened `kow_recursion()` versus KOW's own
  recursion (8) (below it for 9 ≤ n < 3000, integer pieces 15 ≤ n; explicit closed form beats KOW's closed form only
  for n > 80, (8) only for n > 105), all numbers from the referee's `recursion_ref.out`; Remark (b) marked
  UNPROVED; "guaranteed 63, 84, 109, 135" relabelled bound(n) (guarantee(n) = 46, 64, 85, 108); k = 4 SAT
  results and the wnest.py fix recorded. A short corrections paragraph sits at the top.

## Worst Case Below a²

See `…-subquad-A-break.md` §11. Climb: 24 200 bank evaluations, 0 failures, no negative slack; least
`rec_count_U+33` slack 0 at J = 4 (3 538 banks reaching the branch) and J = 5 (364). J = 4, κ = 3 at
p = 2 789 427 520 807: 131 banks, 0 assertion failures, 3 480 back-substitution passes, 0 failures. New
asserts in `subquad.py` held on all eleven stored test groups. `la.py` is unchanged unless `QS_BIGP=1`.
[9 Nov audit P8: a sentence saying `attack_bigp.py` wrote new p ≈ 2.8e12 banks to `interesting/` was deleted;
no such files exist.]

## 2026-11-09 sections

- **Referees 1.** Edited only `2026-11-08-rees-sde-fq-nest.md` (and two comment lines in
  `adversarial_p5.py`): Lemma R wording (referee B finding 3, the per-slot re-basing, transcribed from the
  report); N(q) ≤ 5q/4 + √(2q) + 7 argument via N₀ = ⌈5q/4 + √(2q) + 6⌉ (finding 6); Lemma Z statement
  (finding 6 of referee C: allowed nonzero values {−2, −1, 1}, 3 values); Theorem C: κ = 3 needs p ≡ 1 mod 3,
  running time poly(a, log p), gain a²/(2p) − O(a log a), positive only for a ≫ p log a; chain3/chain4 labelled
  proportional-column families. **Please check these against the two referee reports; the Lemma R and N(q)
  rewrites copy the referees' repairs and were not re-derived.**
- **Referees 2.** `tests/test_rees_sde_p5_simple.py`: SIMPLE5 on the eight `attack_ref.py` families (generators
  loaded from its source) at n ∈ {3, 4, 6, 9, 12}, m = guarantee_simple(n): 40 witnesses, nonzero, entries in
  {0, ±1}, zero sum; 4.8 s.
- **Extension.** `check_split_cover.py`: 3751/3751, 6253/6253, 686/686 sub-cases LRAT-verified UNSAT [9 Nov: the
  "LRAT VERIFIED" strings came from the unsound build, so these are CaDiCaL UNSAT, not independently
  proof-checked (checker was unsound, 9 Nov); the coverage itself is exact; the k = 3, p = 7 and (11,2)
  cells were re-verified with the fixed checker as their 2 and 31 cases without the γ_(1,1) split,
  `2026-11-09-lrat-checker-fix/recheck/{k3_7_cases,cases11_cases,cases11_c10}.out`]; negative
  controls (deleted line, a SAT line) fail it; `int13_split.out` is empty (no coverage claimed). The test
  `tests/test_rees_sde_fq_cnf5.py` (p = 7 case UNSAT with LRAT VERIFIED; p = 5 nest SAT) takes 2 s and skips
  without lrat-check [9 Nov: it now uses the fixed build and has a negative-control test; 3 passed]. README: eight `big_*.out` files are empty; parameters inferred from names; supersession
  map; `big_13_int_nest.out` has no superseding result.
- **Exponent p^e.** `tests/test_rees_exponent_pe_blackbox.py`: 81_3, 243_24, 625_8 each recover every subgroup
  with calls_max ≤ cap; 11.7 s.
- **Square gap.** `e2dfs_k89.out`: all primes p ≡ 1 mod 8 up to 336 (13) and mod 9 up to 504 (14) lie in
  E₂(κ). Item 2 BLOCKED: `orbit_types.py 5 p` takes 0.5-1.2 h per prime at p ≈ 270-520 and grows like p³ (p = 641
  alone hit 7 200 s), `sep_types.py` enumerates about p³ bases; ~130 primes up to 2628 exceed the 2-core-hour
  cap by orders of magnitude, and another session is already running the faster `orbit_types_fast.py` and
  `osc-k5/osc_k5.py` sweeps (`sweep_A.out`, `sweep_B1.out`) whose JSON lines carry PW and N1/mu1;
  `osc-k5/summarize.py` can build the table once those finish.

## Tests run (this session only)

`pytest -q tests/test_rees_sde_fq_cnf5.py` (with `LRAT_CHECK`): 2 passed; without: 2 skipped. [With the unsound
build; on 9 Nov, with the fixed build and the new negative-control test: 3 passed.]
`tests/test_rees_exponent_pe_blackbox.py`: 3 passed. `tests/test_rees_sde_p5_simple.py`: 1 passed.
No other tests were run; the full suite was not run.

## Caveats

- `lrat-check` came from another session's scratchpad (`…/193e5e8e…/scratchpad/drat-trim/lrat-check`), copied
  to this session's scratchpad. [9 Nov audit: that build had line 161 of `lrat-check.c` commented out (as
  upstream ships it) and verified a one-line bogus proof on any CNF; fixed build and controls in
  `2026-11-09-lrat-checker-fix/`.]
- Another session was concurrently editing `research/MECHANICAL_FOLLOW_UP_PLAN.md` (the "SDE F_q Referees"
  section appeared mid-run); my plan edits are inline "DONE/BLOCKED" notes only.
- Unrelated modified files in the working tree (handoff, STATE, dfs2b outputs) were not touched.
