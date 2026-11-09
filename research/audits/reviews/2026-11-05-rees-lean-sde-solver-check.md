# Rees HSP paper: check and integration of `ReesSdeSolver` and `ReesMergeReduction`

5 November 2026. AI-only overnight pass (Claude Code, independent checker and integrator).
Machine-checked in Lean; AI-run, pending human review. No git, no network. Claim gates
untouched: `formal_compiler_checked` and `general_sde_implemented` stay false. No Lean proof
source was changed; `make_numbers.py` was not run. Backups of every edited file and all
scratch files are in the session scratchpad folder `sde-check/` (not in the repo).

Objects:

- (A) `formal/Formal/ReesSdeSolver.lean` and its report
  `research/audits/reviews/2026-11-05-rees-lean-sde-solver.md`;
- (B) `formal/Formal/ReesMergeReduction.lean`, the step-(R) module of receiver round 2
  (`2026-11-05-rees-receiver-round2.md`, `-round2-check.md`).

## 1. Verdict

**PASS, integrated.** Neither module has an Error or a Gap. Both are now imported by
`formal/Formal.lean`, guarded in `formal/Formal/Audit.lean`, have rows in
`formal/README.md` and in `tab:lean-modules`, and a full in-place
`lake build --wfail` succeeded.

## 2. Forbidden constructs and axioms

- `grep` for `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`,
  `unsafe`, `noncomputable`, `opaque`, `csimp` and `set_option` over both files finds
  nothing. The one hit is the word "noncomputable" in a docstring of `ReesSdeSolver`.
- `#print axioms`, run in a scratch file with `lake env lean`:
  - every `ReesSdeSolver` def and theorem guarded below prints
    `[propext, Classical.choice, Quot.sound]`, except `contraction_of_index`, which prints
    `[propext, Quot.sound]`;
  - in `ReesMergeReduction`, `pow_val_add` prints `[propext, Quot.sound]`, and the other six
    theorems print `[propext, Classical.choice, Quot.sound]`.
- The source report explains why computable defs list `Classical.choice`: the proof fields
  of `Fin.fintype`. The defs are not `noncomputable`, and the `#eval` runs below executed
  them.

## 3. Statement fidelity

**`prop:triangular-sde` vs `triSolve_spec`.** The paper's conclusion, a nonzero
`x ∈ (P∪{0})^M` with `∑ x_i λ_i = 0` from any `(a+1)(a+2)/2` columns, is the Lean
conclusion with `D = P ∪ {0}`.

- The contraction enters as `A ζ = α_{cos ζ}` and `B δ = β_{cos δ}`. Its two hypotheses are
  `ζ δ (A ζ + B δ) ∈ D` for nonzero `ζ, δ`, and `A 1 + B 1 ≠ 0`, which is the normalisation
  `α_0 + β_0 = 1`.
- `contraction_of_index` derives the first hypothesis from the paper's coset condition
  `α_j + β_i ∈ g^{-(i+j)} P ∪ {0}`, written as `∃ w, (α_j + β_i) g^{(i+j).val} = w^κ`.
- The Lean is more general than the paper: any field, any `D`, no `κ` or `E_2` hypothesis.
  It adds a support bound.
- The algorithm follows the paper's rounds: `a − k + 1` fresh columns in round `k`, the first
  nonzero fresh entry normalised to 1, then the membership test `v_{k+1} ∈ U_k`.
- Not proved: the paper's `O(a+1)` eliminations and `O((a+1)^2)` coset tests, and the
  Las Vegas root extraction. Roots are found by `O(|K|)` search.

**At `κ = 2`.**
- `quadSolve_spec` accepts any quadratic non-residue `g`, as the paper says.
- `quadSolveZMod_spec` needs only that `p` is an odd prime and `M ≥ (a+1)(a+2)/2`: the
  contraction is computed by `findMu`.
- `quadSolveZModExp_spec` adds the Bezout exponent for `gcd(d, p−1) = 2`.

**`thm:power-sde`(i) vs `linSolve_spec`.** Both use `a + 1` columns and
`gcd(d, q−1) = 1`. The Lean holds over any finite field, while the paper states `F_p`. The
bijection `s ↦ s^d` enters only through `pow_bezoutExp`.

**Chevalley–Warning.** The paper's "nonzero solution among any `gcd(d,p−1)a+1` columns"
matches `cwSearch_zmod_gcd` (hypothesis `gcd(d,p−1)·a < M`). `cwSearch_witness` is the
`κ`-exponent version over any finite field. Both are complete exhaustive searches over all
`p^M` vectors.

**(R) vs main.tex "Instances" (the merge-check paragraph under Gate-level control).** The
paper says that from the exact checks and the witness equation `∑ s_i^d λ_i = 0`, every
merged product equals the zero-label product pointwise, for every label tuple and every
witness. `merge_product_eq_of_labels` states exactly this:

- the label tuple is given by coordinates `c` in a linearly independent `b`;
- the hypotheses are the checks:
  - (E2) as `φ c g = ζ^{(∑ c_j W_j g).val} φ 0 g`, for all `c`;
  - the support of `φ 0` lies in `supp0`;
  - (E3) as `W(δ_{s_i} g) = s_i^d τ g`, wherever all `δ_{s_i} g ∈ supp0`;
- the conclusion is quantified over all `c`, all `s` and all `g`.

`zero_product_indicator` gives the `κ^{#A}`·indicator form. That the merge output depends
only on this product is not formalized. The paper says so, and that sentence is kept.

## 4. Non-vacuity (scratch file `sde-check/Check.lean`, `lake env lean`, no errors)

**Theorems applied to concrete inputs.** These `example`s are kernel-checked:

- `quadSolveZMod_spec` at `p = 5`, `a = 2`, 6 columns;
- `linSolve_zmod_spec` at `p = 5`, `d = 3` (`gcd(3,4) = 1`), `a = 2`, 3 columns;
- `cwSearch_zmod_gcd` at `p = 5`, `d = 2`, `a = 2`, 5 columns;
- `triSolve_spec` at **`κ = 3` over `ZMod 7`**. This case is outside the module's own
  tests. The setup:
  - the cubes are `P = {1, 6}`, so `D = {0} ∪ {y | y² = 1}`;
  - the coset index is `dlog_3 mod 3`;
  - the contraction `α = (1,0,3)`, `β = (0,4,6)` was found by a Python search;
  - the hypothesis `hAB` was proved by `decide`.

**Runs (`#eval`).**

| Run | Output |
|---|---|
| `findMu 5` | `1` |
| `quadSolveZMod 5` | `#[1,1,2,0,0,0]`, residual `[0,0]` |
| `linSolve 5 3` | `#[1,4,1]`, residual `[0,0]` |
| `cwSearch (zmodElems 5) 2` | `#[1,1,2,0,0]` |
| `triSolve` at `κ = 3`, `F_7^2`, 6 columns | `#[0,6,0,1,1,0]` (entries in `{0,1,6}`), residual `[0,0]` |
| `triSolve` at `κ = 3`, `F_7^3`, 10 columns | `#[1,1,1,6,0,0,0,0,0,0]`, residual `[0,0,0]` |

**(R).** `merge_product_eq` was applied to a non-degenerate instance:

- `p = 5`, `R = ZMod 11`, `ζ = 3` (order 5);
- `G = ZMod 5`, `W g = g²`, `δ_t g = t g`, `d = 2`;
- `s = (1, 2)`, `c = (1, 1)`, so the witness equation reads `1·1 + 4·1 = 0`.

The individual factors are nontrivial (`3, 4`, i.e. `ζ, ζ⁴`), and their product is 1 for
every `g`, as the theorem says. All hypotheses were discharged by `decide`, `simp` and
`ring`.

## 5. Integration

- **`formal/Formal.lean`:** added `import Formal.ReesSdeSolver` and
  `import Formal.ReesMergeReduction` after `Formal.ReesSdePolicy`.
- **`formal/Formal/Audit.lean`:** the same two imports. The new guards are appended after the
  last `ReesSdePolicy` guard, in house style (`/-- info: ... -/`,
  `#guard_msgs (whitespace := lax) in`, `#print axioms`).
  - `ReesSdeSolver`: **24** guards. These are the report's 22 plus `contraction_of_index`
    (`[propext, Quot.sound]`) and `findMu_contraction`, both main statements of its
    Section 2.
  - `ReesMergeReduction`: **5** guards, one for each main theorem: `witness_coords`,
    `exponent_cancels`, `merge_product_eq`, `merge_product_eq_of_labels`,
    `zero_product_indicator`.
- **Guard count:** `grep -c "#print axioms" formal/Formal/Audit.lean` = **538** =
  509 + 29. Of these, 500 are for `tab:lean-modules` (471 + 24 + 5) and 38 are unrelated
  (unchanged). The table rows sum to 500. The per-module counts by namespace are 24 and 5.
  The report's proposed figures, 493 and 531, assumed 22 guards and are superseded.
- **`formal/README.md`:** `ReesSdeSolver` added to the local-guards file list; a new
  two-row table (24 / 5) after the SDE section; the "Still outside" sentence qualified.
- **Build:** `pgrep -l lake` was empty first. Then:
  - `nice -n 10 lake build Formal.ReesSdeSolver Formal.ReesMergeReduction`: success,
    18.9 s, max RSS 2.33 GB.
  - Full `cd formal && nice -n 10 lake build --wfail`: **exit 0, "Build completed
    successfully (3524 jobs)"**. `Formal.Audit` and `Formal` were rebuilt. It took 38 s wall
    (other modules cached) with max RSS 3.18 GB, under load average about 150 from other
    agents. The only info line is the pre-existing replayed `Formal/CrossCheck.lean:90:0:
    true`.
  - No clean-copy `--no-cache` build was run.

## 6. Paper edits (exact-string, count asserted 1, file re-read before each edit)

`docs/papers/rees-hsp/main.tex`:

1. **Abstract / introduction boundary sentence.** It adds that Lean compiles and runs, with
   correctness proofs, the triangular solver (contraction as input), solvers at `κ = 1, 2`
   over `F_p` with no contraction input, and exhaustive search at the Chevalley–Warning
   arity. In the outside list, "the SDE algorithms" became "SDE algorithms for κ ≥ 3";
   running time stays outside.
2. **"Instances" paragraph (the merge checks under Gate-level control).** The three
   "standalone" sentences are replaced. `ReesMergeReduction` is imported by `Formal.lean`
   and its five main theorems are guarded (machine-checked in Lean; AI-run, pending human
   review). The merge-output dependence "is still read off the code, not machine-checked".
3. **"Scope" paragraph.** "the standalone module above" became "the module
   `ReesMergeReduction` above".
4. **Formalization paragraph.** It has a new 5 November integration sentence: 29 guards, an
   in-place `lake build --wfail`, and no clean-copy build. The counts changed from 471 to
   500 and from 509 to 538 "in all", and the counting note now includes the merge-identity
   module.
5. **`tab:lean-modules`.**
   - New rows: `ReesSdeSolver` 24 (solver text of the report's 6.3) and
     `ReesMergeReduction` 5. The Total is now 500.
   - The table is now in **three parts**. The four general-class rows moved to Part 1;
     Part 2 runs from `BCHClassFour` to `ReesGeneralMeasuredReceiver`; Part 3 holds the six
     SDE rows, the merge row and the Total.
   - Reason for the split: with two parts, Part 2 could not be placed and floated to the end
     of the document. The I217 build already reported it on p. 170, after the
     bibliography, and with the new rows it went to p. 171. All three parts are now on
     pp. 72–74.
6. **SDE Lean paragraph.**
   - "Lean checks existence and algebra but no algorithm" was replaced by "... and the
     computable solvers described at the end of this paragraph; it has no algorithm for
     κ ≥ 3 and proves no running time".
   - The sentence "Lean takes g to generate F_p^×" was replaced as the report's 6.1 proposes.
   - The report's 6.1 solver paragraph was appended, with `D∋0` rewritten as "D that
     contains 0", because the macro checker of `test_rees_paper_numbers` flags `\ni`.
7. **"Inside and outside".** "any computed SDE policy" became "any computed SDE policy of
   the receiver (... the solvers of `ReesSdeSolver` are not composed with it), every SDE
   algorithm for κ ≥ 3".

`docs/papers/rees-hsp/core/main-core.tex`, Lean paragraph:

- "but no algorithm" is removed. A new sentence lists the solvers: triangular with the
  contraction as input, κ = 2 over F_p with search, κ = 1 at a+1, and exhaustive search at
  the CW arity. It adds that their running time is not formalized and that Lean has no
  algorithm for κ ≥ 3.
- The outside list now reads "every solver for κ ≥ 3, the polynomial-time root extraction,
  the arity bounds of the schedules".
- The closing sentence "machine-checked; ... AI-run and pending human review" is kept.

No `\mathsf`, `\mathrel`, `\begingroup` or `\aa` was introduced; the counts of these are the
same as in the backup.

**Builds** (scratch copies, `latexmk -g -pdf -interaction=nonstopmode`):

| Paper | Exit | Pages | Overfull | Undefined refs/cites | Float too large |
|---|---|---|---|---|---|
| `main.tex` | 0 | 172 | 0 | none | none |
| `main-core.tex` | 0 | 27 | 0 | none | none |

## 7. Tests

- `tests/tools/test_rees_paper_numbers.py`: **2 passed**. The first run failed on `\ni`,
  which was then fixed.
- Lean/formal/audit sweep (`ls tests | grep -i -E "lean|formal|audit"`, plus
  `tests/test_rees_circuit_round2.py`, which reads `ReesMergeReduction.lean`; 84 files):
  **1109 passed, 1 skipped, 4 failed** in 14 min 36 s. Three of the failures are listed in
  `tests/KNOWN_FAILURES.txt` (`test_coset_two_copy_transition_audit`,
  `test_coset_typical_commutant_moment_audit`, `test_coset_typical_irrep_transfer_audit`).
  The fourth, `test_native_refresh_crossover_scope_audit::test_independent_js_replays_all_current_audit_records`,
  is the same failure the I217 sweep recorded: a working-tree change to
  `native_refresh_lottery_crossover.json`, unrelated to Lean or the paper.
- Integration-log row: **I218**.

## 8. Remaining limits (unchanged by this pass)

- Running time is not formalized. Roots are found by `O(p)` search, not by the
  `poly(log p)` Las Vegas extraction.
- There is no coset index or contraction for `κ ≥ 3`.
- The arities of Schedules 2 and 3 and the use of the label rank `a_{d+1}` are not
  formalized.
- The policies of `ReesSdePolicy` are still chosen, not replaced by the solvers.
- Not machine-checked: that the merge output is a function of the (R) product, and the tie
  to the gate lists.
- No clean-copy build was run.
- Human review is pending.
