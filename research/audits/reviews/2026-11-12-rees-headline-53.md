# Rees headline exponent 145 → 53: integration package (2026-11-12)

AI-prepared. AI-checked, pending human review. No Git actions, no network, and
`make_numbers.py` was not run.

Folder: `research/audits/reviews/2026-11-12-rees-headline-53/`. It holds the scripts, their
outputs, backups, `numbers.tex.new` and `.diff`, and `core.patch.md`.

## Verdict

The owner's change is safe to integrate, provided the paper text changes with the macros.

- **E_1(9) = 53 holds.** Label: PROVED given cited theorems, with an exact computation.
  - Below 26244, an exhaustive computation found the maximum 53.
  - From 26244 on, a short hand argument gives at most 53, with equality exactly for
    p ≡ 2521 (mod 5040).
  - It is attained at p = 2521, 7561 and 12601, and at every larger prime in that class.
  - Two independent codes agree: the generator and `verify_headline.py`, which uses no
    Weil shortcut.
  - The controls reproduce the old 145 and 143.
- **The macros cannot be regenerated alone.** Several sentences in the core and the full
  version would then become false, for example "exponent at most 1+Σ d⌈log₂(d+1)⌉; this is
  \ReesClassNineQueryExp" and "does not depend on p once p ≥ 3/ε". The patch covers all
  of them.

## 1. Numbers (`theorems/rees_hsp_reduction.py` → `research/reductions/rees_hsp_reduction.json`)

Generator changes:
- New functions: `zero_sum_length`, `schedule1_zero_sum_depth`, `zero_sum_sde_arity`,
  `zero_sum_depth_patterns`, `zero_sum_depth_exponent` and `_worst_zero_sum_arities`.
- `recovery_budget`, `black_box_large_prime_budget` and `black_box_copy_budget` take a
  new parameter `depth="published"|"zero_sum_instance"|"zero_sum_worst"`. The default is
  unchanged.
- `main()` now writes the worst case over p > 9 as `profile`, with keys
  `schedule1_depth_rule`, `arity_maximizing_prime` and
  `query_dimension_exponent_maximizing_prime`. It also writes two new keys:
  - `zero_sum_depth_instance_profile` (p = 43);
  - `published_depth_profile` (the old profile verbatim, plus the old envelopes 147/2194
    and the copy envelope 147/147/2194/1918/2194).

Safety of the regenerated JSON: no key was removed, and every claim gate and boolean is
unchanged (checked). Backups are `rees_hsp_reduction.before.{json,py.txt}` and
`test_rees_hsp_reduction.before.py.txt`.

| field | old (145 profile) | new (zero-sum depth, worst p > 9) |
|---|---|---|
| profile.query_dimension_exponent | 145 | **53** (p = 2521) |
| log₂ Q (exact) | 1572.66 | 563.63 |
| original_queries_ceil_log2 | 1573 | 564 |
| complete_instrument_calls_ceil_log2 | 1570 | 561 |
| classical_sde_attempts_per_call | 1081 | 441 |
| instrument_error_per_call, sde_abort_bound_per_call | old | changed (fewer calls) |
| total_error_bound | 1207/5418 | 1207/5418 (unchanged: depends only on the ε split and τ at p = 43) |
| large_prime_query_dimension_exponent (147) | 147 | **55** |
| large_prime_original_queries_ceil_log2 | 2194 | 794 |
| copy-only, large-prime exponent | 147 | 55 |
| copy-only, small-prime exponent | 147 | 147 (κ = p−1 forces t = p; unchanged) |
| copy-only, small_prime_original_copies_ceil_log2 | 1918 | 1918 |
| copy-only, total_original_copies_ceil_log2 | 2194 | 1918 (the small primes now dominate) |
| p = 43 instance (new key) | — | log₂Q 278.29, 279 bits, 271 attempts |

The would-be macros are in `numbers.tex.new`; the diff against the current `numbers.tex`
is in `numbers.tex.diff`. Six macros change:

| macro | old | new |
|---|---|---|
| QueryExp | 145 | 53 |
| SdeAttempts | 1081 | 441 |
| OrigQueriesBits | 1573 | 564 |
| InstCallsBits | 1570 | 561 |
| ReesOuterQueryExp | 147 | 55 |
| ReesOuterOrigQueriesBits | 2194 | 794 |

Every other macro is identical.

Paper-only numbers (`zero_sum_tables.json`, `verify_headline.json`,
`crossover_exact8l.json`):

- **E_1(c), c = 2..9:** 5, 8, 16, 19, 35, 36, 44, 53, against the old 5, 11, 23, 38, 56,
  77, 109, 145.
- **E_W(c)** equals E_1(c) for c ≤ 9. The old values were …107, 143.
- **Crossover table**, maximized over p ≥ 11:

  | family | log₂Q | LB crossover | (v) threshold | copies |
  |---|---|---|---|---|
  | filiform | 20.00 | 9,391 | 3,325 | 218 |
  | free | 23.68 | 3,413 | 1,567 | 293 |
  | Dixmier–Lister | 25.55 | 157 | 97 | 474 |
  | class 9 | 563.63 | 2^{62.60} | 2^{62.35} | 22,548 |

  The Heisenberg row is unchanged. The exact-8ℓ values are 86, 3,375, 1,585 and 98, so
  the prime thresholds are 83, 3,373, 1,583 and 97.
- **"p > 2^{174.7}"** becomes 2^{62.6}.
- **bb-envelope (main.tex l. 1085):** 2^{2186} becomes 2^{786.7} as the worst over p, or
  2^{423.9} at p = 43. The figures 2^{1833} and 2^{603} at p = 43 both become 2^{324.1}.
  The black-box exponent E_W(9)+1 goes from 144 (146 with Schedule 1 alone) to 54 (54).
- **Class-3 example:** 2^{33.19} becomes 2^{23.68}, at p ≡ 7 (mod 12).
- **Heisenberg example:** 64 becomes 8 or 64, depending on p mod 4.
- **Growth in c:** c(c+1)/2 ≤ E_1(c) ≤ 1+Σ d⌈log₂(d+1)⌉. E_1(10..12) = 69, 80, 94.
- **Deterministic fallback.** If the Las Vegas zero sums were unacceptable: odd κ with
  (1, −1), BFS below 4κ⁴, and van de Woestijne for even κ. This gives **91** at c = 9.
  Label: PROVED given IS Theorem 11 and van de Woestijne, by the same case analysis, and
  computed.

## 2. Tests (`nice -n 19`, `/opt/anaconda3/bin/python -m pytest`)

Four tests were added to `tests/test_rees_hsp_reduction.py`:
- brute force versus the Weil and parity rule;
- the exponents with their maximizing primes, and arity ≤ the published arity;
- the instance profile;
- the committed JSON, including the claim gates.

Results:
- `tests/test_rees_hsp_reduction.py` with `tests/tools/test_rees_paper_numbers.py`: **25
  passed, 1 failed**. The failure is `test_rees_numbers_tex_is_up_to_date` and is expected:
  `numbers.tex` is stale until the integrator runs `make_numbers.py` and syncs `core/` and
  `arxiv/`.
- Other readers of the JSON or of the generator, all passing:

  | test file | passed |
  |---|---|
  | `test_rees_copy_only_outer` | 14 |
  | `test_rees_cover_and_nontransverse_descent_audit` | 5 |
  | `test_cubic_diagonal_solver` | 31 |
  | `test_free_lazard_pullback` | 14 |
  | `test_rees_complete_instrument` | 5 |
  | `test_rees_subspace_source` | 48 |
  | `test_rees_nongradable_control` | 18 |
  | `test_rees_projective_source` | 11 |
  | `test_rees_end_to_end_sim` | 41 |
  | `test_rees_circuit_full` | 11 |

  That is 198 passed. The peak RSS was 1.07 GB.
- The full suite was **not** run (TRAPS 14).

## 3. Patch summary (`core.patch.md`, not applied)

The arity B_d is redefined in the following steps.
- **Arity.** B_d(a) becomes p-dependent: a+1 if κ_d = 1, and G(κ_d,a)^{⌈log₂ t_{p,κ_d}⌉}
  otherwise. The published arity is kept as B̄_d ≥ B_d, so the corollaries need no edit.
- **Import.** `thm:is-import` is cut down to IS Theorem 11. The statement was re-read in
  the local arXiv text, ll. 439–442; J may be empty.
- **New lemmas in the body.**
  - `lem:rounds`: L-round accumulation, the J = ∅ stop, and the zero-sum closing.
  - `lem:zero-sum-length`: t ≤ κ+1 by Chevalley–Warning; t = 2 iff (p−1)/κ is even;
    t ≤ 3 for p ≥ 4κ⁴ by Weil; BFS below 4κ⁴; deterministic for odd κ; Las Vegas for even
    κ, with success probability 1/2 or at least 1/(4κ) per trial.
  - `lem:exponent`: the bounds c(c+1)/2 ≤ E_1(c) ≤ 145-type, and E_1(9) = 53 by the hand
    argument plus the exact computation.
- **Error budget.** The Las Vegas preprocessing runs once per grade, before any query. It
  takes the third of the budget that the merges leave unused, so the total changes from
  2ε/3 to ε.
- **Required text changes.**
  - thm:main(4).
  - rem:main-solver: the Ivanyos wording now says the confirmation covers the full depth
    only.
  - rem:is-import(a)–(d), rem:is-printed and lem:bezout.
  - The Schedule 1 paragraph and the proof of thm:main.
  - rem:oblivious, the examples, and the table with its caption.
  - rem:query-separation, the Outlook ("Smaller arities" corrected, "Shorter zero sums"
    deleted, open problem 1), the abstract and intro wording, and the artifacts list.
- **Full version (B1–B22).** The same changes, plus:
  - the full-version-only items: the regimes and notation tables, rem:combined-schedule,
    and the profile paragraph (l. 1085);
  - thm:bb-envelope;
  - a replacement for lem:tb-count-exponent;
  - provenance entries.
  - B21 lists the tables NOT recomputed: tab:fcs-budget "combined", tab:full-grade-budget,
    tab:random-column-budget, and the class-3 and class-12 profiles.

## 4. Risks: where 53 is weaker than 145

1. **Human confirmation.** Ivanyos confirmed C ≤ G^{⌈log₂(d+1)⌉}, not the shortened depth.
   - 53 rests on `lem:rounds`. It is proved here, given the AI-read statement of IS
     Theorem 11, but has no human check.
   - The determinism of Theorem 11 (IS §3.1–3.2) is an AI reading for both exponents.
2. **New imports.** Weil's bound, Rabin root finding and Chevalley–Warning.
   - The Weil locator "Lidl–Niederreiter Theorem 6.37" is recalled, NOT verified; it is
     marked NEEDS HUMAN VERIFICATION in A12.
   - A self-contained Jacobi-sum proof for two variables is standard and could replace it.
3. **Exact computation.** E_1(9) = 53 needs the exhaustive search for p < 26244. The
   145 needed no computation.
4. **Determinism lost.** The theorem's algorithm becomes Las Vegas in its classical
   preprocessing whenever κ_d is even and p ≥ 4κ_d⁴. This applies to every large p at
   grade 2.
   - The total error is now exactly ε, with no slack.
   - The black-box corollaries call thm:main with their own ε, so they are unaffected.
   - The JSON keeps the conservative per-call attempts model, not the per-grade
     preprocessing model. The per-grade model would need ⌈log₂(3(c−1)/ε)⌉ = 7 attempts per
     grade at ε = 1/3.
   - Under the combined rule, Schedule 2 grades and the preprocessing must split the
     solver share (B12). This is not in the JSON.
5. **p-dependence.** Q_q now depends on p. Table columns and the crossover now mean "worst
   over p ≥ 11". The claim that (v) needs fewer than Q_q queries refers to that maximum,
   not to the count at each p.
6. **Correction to the referee.** The referee's "only lengths 3–4 are Las Vegas" is
   inaccurate. Length 2 at even κ also needs a κ-th root of −1, so it is Las Vegas too.
   The patch says so.
7. **Growth in c.** "c² log c" is replaced by "at least quadratically". Θ(c²) needs the
   divisor bound, and the Hardy–Wright locator is unverified, so it is full version only.
8. **Turing-machine bound.** The rem:is-runtime bounds (full version) assumed a
   deterministic zero sum. The preprocessing term is NOT re-derived.

## 5. Adversarial self-check

- **Could E_1(9) exceed 53 at some prime?**
  - Above 26244 the case analysis covers every 2-adic valuation, and e_{p,d} ∈ {κ_d, 2κ_d}
    needs t ≤ 3, which is Weil at p ≥ 4·9⁴.
  - Below 26244 there are two independent exhaustive codes, and the brute force uses no
    Weil shortcut.
  - The residue argument uses N = 2·lcm(1..9) = 5040, which contains the needed 2-power
    2⁴.
  - Residual risk: a shared conceptual error in the definition of t. The definition used
    is the least number of nonzero κ-th powers summing to 0. That is the right object for
    `lem:rounds`, because zero coefficients can be dropped.
- **Is `lem:rounds` right when some z_r = 0?** Yes. The solution is still nonzero because
  some z_r ≠ 0 and its S_r is nonempty.
  - Disjointness across blocks and inside blocks is argued.
  - The J′ = ∅ case uses the first representations only.
  - The proof was cross-checked against the IS text ll. 576–594. The simulation in the
    referee folder (60/60) is a finite check only.
- **Does the Las Vegas preprocessing break rem:oblivious or the coherent receiver?**
  - It is classical, depends only on (p, c, ε), makes no query, and has a hard cut-off.
  - The quantum part is unchanged. It is deterministic given z.
  - I found no place that needs the zero sum coherently.
- **Is "no sentence becomes false" really covered?** I grepped for `ReesClassNine`,
  `ReesOuter`, `log_2(d+1)`, `c^2\log c`, `143`–`147`, `2186`, `1833`, `603`, `174.7`,
  `531441`, `1024`, `confirmed` and `2\eps/3` in the core, main.tex and the appendices.
  Each hit is either handled or harmless.
  - `appendix-schedule3.tex:280` 2ε/3 is a separate procedure.
  - `appendix-subspace.tex:51` is a comment.
  - Not re-read: the full-version tables in B21, and `appendix-sde-side.tex` and the
    other appendices beyond the grep. NOT checked line by line.
- **Error total.** 1207/5418 is unchanged because the profile's error bound depends only
  on the ε split and τ at p = 43. This was verified in the JSON, not argued.
- **Over-claiming.** Labels: 53 is PROVED given cited theorems and an exact computation.
  The lower bound c(c+1)/2 is PROVED given Dirichlet. Θ(c²) is CONDITIONAL on an
  unverified citation. The tables in B21 are NOT computed. Everything is AI-checked,
  pending human review.
