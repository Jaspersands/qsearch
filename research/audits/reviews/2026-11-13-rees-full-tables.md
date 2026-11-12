# 2026-11-13 Rees full version: tables at the zero-sum depth, preprocessing time, mixed-schedule split

Scope: the full version only (`docs/papers/rees-hsp/main.tex`, `appendix-*.tex`). `core/*` and
`numbers.tex` untouched; `make_numbers.py` not run; no Git; no claim gate touched. Everything here is
AI-checked, pending human review. Finite computations can only falsify; nothing below promotes a
theorem. The depth L_d = ⌈log₂ t_{p,κ_d}⌉ rests on Lemma `lem:rounds` (AI-proved, AI-refereed only;
G. Ivanyos confirmed only the full depth ⌈log₂(κ_d+1)⌉).

Folder: `research/audits/reviews/2026-11-13-rees-full-tables/` (scripts, outputs, `apply_edits.py`,
`paper_edits.diff`, `test_edit.diff`). Backups (pre-edit): `research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-pre-fulltables-2026-11-13/`
(main.tex, all appendix-*.tex, main.pdf, main.log, tests/test_rees_fcs_budget.py).

## 1. Which tables depend on the Schedule-1 depth

| Table | Source | Uses Schedule 1? | Verdict |
|---|---|---|---|
| tab:full-grade-budget (class-3 at p = 65537, class-12 at 2^127−1; macros FgThree*/FgTwelve*/UiThree*/UiTwelve*) | `theorems/uniform_bch_rees.symmetric_recovery_budget` → `rees_full_grade_budget.json`, `rees_uniform_instrument.json` | **No.** Every stage is linear (κ_d = 1) or Schedule 2 under the guard p ≥ 16κ^{2κ+2}; the function raises "field guard" instead of falling back to Schedule 1. | **Unchanged** (PROVED by inspection of the code path + finite check) |
| tab:random-column-budget | `random_column_rees.json` | **No.** Every stage has width M = 4u (Schedule 3). | **Unchanged** |
| tab:fcs-budget, combined column | `theorems/rees_fcs_budget.py` | **Yes** (Schedule-1 fallback grades) | **Recomputed** |
| tab:fcs-budget, other six columns | same | No Schedule-1 grade at these six primes (iii: Γ₀ empty; uniform-kernel: types S3/lin/S2 only; w.-d.: none) | **Unchanged** (recomputed: identical) |

`check_invariant.py` → `check_invariant.out/.json`: re-running `symmetric_recovery_budget` on all
three recorded cases reproduces every JSON field exactly; stage kinds: (6,3,1) at 65537 = [lin, S2];
class 12 at 2^127−1 = 9 × S2 + 2 × lin; random-column cases 0–3 have uniform widths 8, 16, 48, 24.
The "class-3 and class-12 profiles" of the follow-up item are exactly the two columns of
tab:full-grade-budget, so nothing is to be recomputed there.

## 2. tab:fcs-budget combined column: old vs new

Script `recompute_fcs.py` (output `recompute_fcs.out/.json`): imports `theorems/rees_fcs_budget.py`
unchanged; first builds every row as is and asserts it reproduces the printed table (all 42 cells),
the caption's worst-case values 944.9/555.4/61.5 and the triangular 542.0 — **published reproduced:
True**; then replaces the module's `combined_choice` by the same rule with the Schedule-1 arity
B_d(g_d) = G(κ_d,g_d)^{L_d} from `theorems.rees_hsp_reduction.zero_sum_sde_arity`, and rebuilds.

| p | combined Q old (full depth) | **new (depth L_d)** | worst-case rule old → new | triangular worst old → new | Schedule-1 grades (κ, t, L vs full) |
|---|---|---|---|---|---|
| 11 | 202.1 | **118.7** | 202.1 → 118.7 | 202.1 → 118.7 | d=2,4,6,8 (2,3,2 vs 2); d=5 (5,2,1 vs 3) |
| 1031 | 167.3 | **83.9** | 167.3 → 83.9 | 164.0 → 80.5 | d=5 (5,2,1 vs 3) |
| 5281 | 852.3 | **271.5** | 852.3 → 271.5 | 851.4 → 270.5 | d=3,9 (3,2,1 vs 2); 4 (4,2,1 vs 3; LV); 5 (5,2,1 vs 3); 6 (6,2,1 vs 3; LV); 8 (8,2,1 vs 4) |
| 2^31−1 | 940.3 | **355.0** | 944.9 → **359.6** | 940.5 → 355.2 | 6 (6,3,2 vs 3; LV); 7 (7,2,1 vs 3); 9 (9,2,1 vs 4) |
| 2^61−1 | 533.4 | **164.1** | 555.4 → **186.1** | 542.0 → **172.6** | 9 (9,2,1 vs 4) |
| 2^127−1 | 41.4 | 41.4 | 61.5 → 61.5 | 48.3 → 48.3 | none |

LV = the preprocessing of lem:zero-sum-length(iv) is Las Vegas there (κ even, p ≥ 4κ⁴). Block-steered
grades are identical at both depths (2^31−1: {2,3}; 2^61−1: {2..8}; 2^127−1: all with κ_d ≥ 2), and
the Schedule-2 grades kept are unchanged (1031: {2,4,6,8}; 5281: {2}; 2^31−1: {4,8}), so every
qualitative sentence of the caption stays true. Rounding margins of the new values ≥ 0.016 in log₂
(none borderline). The uniform-kernel record (arities, B, trees, bumps) is byte-identical at both depths.

Mental sanity check: at p = 11 only grade 5 changes: G(5,12)² = (5¹⁰·13⁵)² ≈ 2^{83.4}, and
202.1 − 83.4 = 118.7. At 2^61−1 only grade 9: G(9,1)³ = (9³⁶·2⁹)³ ≈ 2^{369.3}, 533.4 − 369.3 = 164.1.

## 3. Independent cross-checks (second method)

`cross_check.py` (output `cross_check.out/.json`) imports **no** repository code. It computes t_{p,κ}
without Lemma zero-sum-length: own BFS (t = 1 + dist(0,−1) in Cay(F_p, P)) for p ≤ 6000; for large p an
explicit verified witness (y with y^κ = −1 for t = 2; for t = 3, (−1)^h = −1 certifies t > 2 and explicit
x, y with x^κ + y^κ + 1 = 0, found with sympy `nthroot_mod`, checked by `pow`). Then G, B_d, the
worst-case combined rule and Q = c(m+τ)∏M_d straight from eq:Bd / rem:combined-schedule.
- Worst-case combined log₂Q at all six primes: 118.7, 83.9, 271.5, 359.6, 186.1, 61.5 — **all agree**.
  At 11, 1031, 5281 the combined column has no block-steered grade, so these three **table entries are
  independently confirmed**; at the last three rows it confirms the caption's worst-case values.
- Block-steered rows (2^31−1, 2^61−1): published exact combined Q (`2026-11-04-rees-fcs-budget/fcs_budget.json`)
  × ∏_{S1 grades} G^{L_d}/G^{⌈log₂(κ+1)⌉} (own t) gives 355.0 and 164.1 — agree. (Valid because every
  block-steered grade lies below every Schedule-1 grade there, so their guards see the same n_d.)
- E₁(9) at p = 2521 from the definition: κ_d = d, t = 2 except d = 8 (t = 3, L = 2): 1 + 2+3+4+5+6+7+16+9 = **53**.

## 4. Mixed-instance numbers (appendix-schedule3, paragraph after prop:mixed-schedule)

`scan_mixed.py` reuses `2026-11-04-rees-mixed-rule/mixed_rule.py` unchanged with its Schedule-1 arity
replaced by G^{L_d}. At the full depth it reproduces the printed 60 columns at p = 151 and 226 primes
below 3600 (`scan_mixed_5000.out`). At depth L_d: **32 columns at p = 151 and 152 primes below 3600**
(largest 3541); the scan to 200,000 (`scan_mixed_200000.out/.json`, 1066 s, 94 MB) finds no
bump prime above 3581 (full depth) or 3541 (depth L_d), 17,896 primes with an S3 node, and no
hypothesis, termination or error-budget failure at either depth; it reproduces the old 60/226 at the full depth. The table instance (four primes) is unchanged: no column added,
weighted bank ≤ 2^{−67.2}, tree-abort 2^{−6.91}..2^{−6.38}, Schedule-2 grades kept as stated.

## 5. Text edits (all via `apply_edits.py`, each old string asserted to occur exactly once)

main.tex:
1. tab:fcs-budget combined column: 202.1/167.3/852.3/940.3/533.4 → 118.7/83.9/271.5/355.0/164.1 (41.4 kept).
2. Caption: worst-case values 944.9/555.4/61.5 → 359.6/186.1/61.5; new sentence: the combined column
   and these values use depth L_d (lem:rounds); at the full depth (rem:is-import(c), covered by Ivanyos)
   the old values are quoted; "No other column uses a Schedule-1 grade at these primes".
3. Triangular paragraph (l. 884): 2^{555.4} → 2^{186.1}, 2^{542.0} → 2^{172.6}, 2^{533.4} → 2^{164.1},
   with the full-depth triple kept in parentheses.
4. rem:is-runtime: the "not re-derived" flag replaced by (i) the merge counts remain upper bounds with
   the zero sum as input; (ii) a **Preprocessing** paragraph: per grade with κ_d ≥ 2, at most
   ⌈log₂(3(c−1)/ε)⌉ attempts (⌈log₂(6(c−1)/ε)⌉ when split), each cut off at 2E_d; E_d = O(κ_d²b) field
   operations = poly(κ_d)·b³ steps for p ≥ 4κ_d⁴, bounded in κ_d alone for p < 4κ_d⁴ (deterministic,
   one attempt); total poly(c)·b³·log(c/ε) plus a term in c alone, once per run.
5. Proof of thm:main: adds that the preprocessing makes ≤ (c−1)⌈log₂(3(c−1)/ε)⌉ cut-off attempts of
   time poly(log p) for fixed c (as in the core).

appendix-sde-side.tex (operation counts): the "not re-derived" flag replaced by the case-by-case count
behind E_d: gcd/parity O(b²); BFS for p < 4κ⁴ (< 4κ⁴ vertices, < 16κ⁷ edges); κ odd: (1,−1);
κ, h even: one exponentiation per trial, success ≥ 1/2; κ even, h odd: O(b) per trial, success
≥ 1/(4κ), one call of Rabin root finding on X^κ − u (κ distinct roots), each split attempt O(n²b),
separates two roots with probability ≥ (p−1)/(2p) ≥ 1/3 [χ((r₁+δ)(r₂+δ)) = 1 for (p−3)/2 values of δ,
plus δ = −r₁, −r₂], smaller factor halves the degree ⇒ O(κ²b); head movement poly(κ).

appendix-schedule3.tex (prop:mixed-schedule):
6. (S1): the preprocessing is run once before any query with ⌈log₂(6(c−1)/ε)⌉ attempts per grade,
   "fail" on abort, and its abort probability ≤ ε/6 **is charged in the error split** (was: "not included").
7. Proof, Restarts: 2^{−2m'} ≤ (ε/3)² ≤ ε/6 (was ≤ ε/3), using m' ≥ log₂(3/ε), ε ≤ 1; new closing
   sentence: total ≤ ε/6 (restarts) + ε/6 (preprocessing) + ε/3 (rank) + ε/3 (implementation) = ε, the
   split of thm:main's proof with its solver third shared by restarts and preprocessing.
   No table value changes: m', B, trees and Q do not depend on this split.
8. p = 151 paragraph: 60 → 32 columns, 226 → 152 primes below 3600, plus the scan range; old values kept.

appendix-provenance.tex: prov:sde-triangular counts (new + full-depth); prov:gc-fcs-budget adds
recompute_fcs.py / cross_check.py / this record; prov:s3-mixed adds scan_mixed.py and the new counts.

tests/test_rees_fcs_budget.py (outside the paper; needed to keep the Rees tests green, backed up, diff in
`test_edit.diff`): `test_printed_table_is_the_live_main_tex_table` now expects the combined column from
`recompute_fcs.json`, asserts that file's published values equal `PRINTED` and that only the combined
column differs. `PRINTED`, the artifact test and `theorems/` are unchanged.

## 6. Compile and tests

`pdflatex; bibtex; pdflatex; pdflatex` (nice -n 19) in `docs/papers/rees-hsp/`: **228 pp.** (was 227),
0 errors, **0 undefined references**, warnings identical to the pre-edit log (1 Overfull 5.87pt at
l. 220–224, 5 Underfull in the bibliography, 1 float too large at l. 289; all pre-existing).
pytest (nice -n 19): test_rees_paper_numbers, test_rees_hsp_reduction, test_rees_fcs_budget,
test_rees_full_grade_budget, test_paper_ingestion, test_paper_numbers: 69 passed; plus
test_rees_circuit_coherent_c4, test_rees_coherent_sde_k3, test_rees_is_sde_solver, test_tools_workflow:
297 passed, 30 skipped. Before the test edit, `test_printed_table_is_the_live_main_tex_table` failed
(it pinned the full-depth combined column).

## 7. NOT done / residual

- The block-steered rows of the combined column (2^31−1 has a Las Vegas Schedule-1 grade, d = 6) are
  runs of rule (R1) under thm:free-coordinate(iii)'s split; the preprocessing there must come out of the
  ε/9 share that split leaves unused (shared with any Schedule-2 calls). Not edited (outside the brief);
  the same holds for other Schedule-3/free-coordinate results that keep Schedule-1 grades. The
  free-coordinate (iii) columns themselves have Schedule-1 nodes only at κ_d = p−1, where the zero sum is
  deterministic (p < 4κ⁴), so they need no charge.
- The preprocessing cost is a sketch (constants not computed), like T^IS_d; Rabin's root-finding count
  is my derivation, not checked against Rabin1980.
- The JSON per-call SDE attempt model (\ReesClassNineSdeAttempts) vs the per-grade preprocessing model:
  untouched (core/numbers matter).
- arxiv/ copies stale; `rees_fcs_budget.py` and its artifact remain full-depth (they now document the
  caption's full-depth values).

## 8. Adversarial self-check

- *Did I recompute the right object?* The combined rule (rem:combined-schedule, already updated in
  main.tex) says M_d = B_d(g_d) at Schedule-1 grades; the old script used base κ_d with depth
  ⌈log₂(κ_d+1)⌉ — exactly B̄ at degree κ_d. Replacing only the exponent is the change of eq:Bd. Yes.
- *Could the block-steered choices move?* Recomputed, not assumed: identical lists at both depths.
- *Hidden Schedule-1 use in "unchanged" columns?* Checked by recomputation (identical records), and
  tab:full-grade-budget by code path (raises instead of fallback) plus exact field-by-field re-run.
- *Second method genuinely independent?* cross_check.py shares no code, finds t without the lemma
  (BFS / explicit witnesses), and agrees on all six worst-case values; but it shares my reading of
  eq:Bd and the combined rule, so a misreading of the definitions would not be caught.
- *Error split:* (ε/3)² ≤ ε/6 needs only ε ≤ 1 (hypothesis of the proposition). The restart bound
  2^{−2m'} was already in the proof; I did not re-derive C(4m',3m')32^{−3m'} ≤ 2^{−2m'} (it holds:
  C(4m',3m') ≤ 2^{4m'}, so the left side ≤ 2^{−11m'}).
- *Rabin split probability:* first draft said 1/2; corrected to (p−1)/(2p) after counting δ = −r_i.
- *Page count 228 vs ~227:* the added paragraphs; no new warnings.
