# Adversarial check of `ReesS2Local` (Rees paper, Subsection `app:s2-local`)

5 November 2026. AI-only pass (Claude Code subagent), pending human review. Checks
`formal/Formal/ReesS2Local.lean` and its report
`research/audits/reviews/2026-11-05-rees-lean-s2-local.md` against
`docs/papers/rees-hsp/appendix-schedule2.tex` (Subsections `app:s2-gcd`,
`app:s2-tensor`, `app:s2-contraction`, `app:s2-local`). No git, no network, no
`lake update`; the Lean file was not edited.

## Verdict

**Faithful, with stated differences** (Section 3). The definitions encode the paper's
`Q_m`, `Q°_m`, coset generator, `W`, `W ⊗ W`, two-level contraction and `E_2(κ)`; no
hypothesis is unsatisfiable, `E_2` is neither trivially empty nor trivially full, and
the `decide` instances run through the definitions. Integrated (Section 5).

## 1. Definitions, line by line

| Lean (line) | Paper | Finding |
|---|---|---|
| `z ξ m = ξ ^ m.val` (61) | `z_m = ξ^m`, `m ∈ Z_κ` | Same; `m.val ∈ [0, κ)` is the paper's representative. |
| `MemQo ξ m x := ∃ w, x = ξ^{m.val} w^κ` (64) | `Q°_m = ξ^m Q_0 ∪ {0}`, `Q_0 = {x^κ : x ≠ 0}` | `w = 0` gives `0` (κ ≥ 1), `w ≠ 0` gives `ξ^m Q_0`. Since `ξ^κ ∈ Q_0`, `ξ^m Q_0` depends only on `m mod κ`, so negative indices such as `-(i+j)` (ZMod negation, then `.val`) are read correctly: `memQo_pow_mul_iff`, `memQo_zz_iff` prove the index arithmetic. No off-by-one. |
| `MemQ := x ≠ 0 ∧ MemQo` (68) | `Q_m` | Same. |
| `IsCosetGen κ ξ := IsPrimitiveRoot (ξ^((p-1)/κ)) κ` (71) | `ζ = ξ^h` of exact order `κ`, `ξ ∈ F_p^×` | Same. `ξ ≠ 0` is derived (`ne_zero_of_cosetGen`, since `h ≥ 1`). `(p-1)/κ` is ℕ division, exact under `κ ∣ p - 1`, which `E2` forces through `p ≡ 1 [MOD κ]`. |
| `InWW ξ X` (76) | `X ∈ W ⊗ W`; condition (b) of `lem:app-s2-tensor` | All columns and all rows in `W`. This equals `W ⊗ W` (`(W⊗V) ∩ (V⊗W) = W⊗W`). The reading is also immaterial: `hasContraction_iff` proves that annihilating `InWW` is equivalent to the decoupled form, and its hard direction uses only rank-one tensors `a bᵀ` with `a, b ∈ W` (`testVec`), which lie in `W ⊗ W` under any reading. So `E2` is the same under the rows-and-columns reading and the span-of-`a ⊗ b` reading. |
| `IsContraction` (80) | Definition in `app:s2-contraction` | `mem`: `C_ij ∈ Q°_0` (`MemQo ξ 0` is "is a κ-th power", independent of `ξ`); `ne_zero`: `C_00 ≠ 0`; `annihilates`: `Σ C_ij X_ij = 0` on `InWW`. Same. |
| `E2 κ := {p \| p.Prime ∧ p ≡ 1 [MOD κ] ∧ ∀ ξ, IsCosetGen κ ξ → ¬HasContraction κ ξ}` (91) | "primes `p ≡ 1 (mod κ)` at which no two-level contraction exists" for the fixed `ξ` | Quantified over every coset generator; `mem_E2_iff_exists` proves it equal to "for some coset generator", using the transfer lemma and existence of generators. Matches the paper's definition together with its independence paragraph. |
| `A ξ u v` (107) | `A(u,v) = #{w ∈ Q_u : w - 1 ∈ Q_v}` | Same; depends on `ξ` through the labelling, as in the paper. |
| `ε` as hypothesis `MemQo ξ ε (-1)` | `ε = ind(-1)` | `-1 ≠ 0`, so `index_unique` makes `ε` unique; `card_pairs_le` obtains it from `exists_index`. |

## 2. Vacuity and degeneracy checks

* **Coset-generator guard is load-bearing, and present.** For `ξ = 1` a contraction
  always exists (constant matrix: `α = 1`, `β = 0`). Checked in a scratch file:
  `HasContraction 4 (1 : ZMod 13)` and `¬ IsCosetGen 4 (1 : ZMod 13)` both compile.
  Without the `IsCosetGen` premise, `E2` would be empty. `hasContraction_transfer`
  (contraction for `ξ` gives one for every nonzero `ξ'`) is correct but shows that only
  the guard keeps `E2` non-trivial; this is fine because `E2` has the guard.
* **E2 not trivially empty.** `13, 29 ∈ E2 4` are proved through
  `mem_E2_of_A_eq_zero`, where `decide` evaluates `MemQo` (`-1 ∈ Q_2`), `IsCosetGen`
  (powers of `ξ^h`) and `A ξ u v = 0` on the actual definitions. If `annihilates` were
  vacuous, the all-ones matrix would be a contraction; if `mem` were vacuous,
  `C_ij = z_i z_j` (decoupled, `α = 1`, `β = 0`) would be one. Either would make `E2`
  empty, so these instances also show that both conditions have content.
* **E2 not trivially full.** `7 ∉ E2 3` and `3 ∉ E2 2` give explicit `(α, β)`, checked
  by `decide` and turned into an `IsContraction` by `hasContraction_iff`. Consistent
  with the paper's `E_2(2) = E_2(3) = ∅`.
* **Hypotheses satisfiable.** `κ ∣ p - 1`, `IsCosetGen` (existence: `exists_cosetGen`),
  `MemQo ξ ε (-1)` (existence: `exists_index`), `u ≠ 0, v ≠ ε, u ≠ v` (satisfied in the
  instances) are all inhabited; `mem_E2_of_le` is inhabited by the ten instances.
* **Int vs Nat.** `mem_E2_of_le` states `p ≤ κ² − 3κ + 3` over `ℤ`. Over ℕ the bound
  would read 3 at `κ = 2` and wrongly cover `p = 3`; `three_not_mem_E2_two` shows that
  reading would be false. `card_pairs_le` uses ℕ `(κ−1)(κ−2) ≤ p − 2`, which is exact for
  `κ ≥ 2`, `p ≥ 2` (at `κ = 1` both sides are harmless). The final `nlinarith` step was
  re-derived: with `κ = m + 2`, `(m+1)m + 2 ≤ p ≤ m² + m + 1` is a contradiction.
* **`decide` is kernel `decide`.** `grep` finds no `native_decide`, `sorry`, `axiom`,
  `admit`, `opaque`, `implemented_by` or `extern` in the file (the two `native_decide`
  hits are docstrings).
* **Instances by (ii) only exercise arithmetic** (`p ≡ 1 [MOD κ]`, the ℤ inequality);
  they are corollaries of the proved `mem_E2_of_le`, not further tests of `E2`.

Independent brute force in Python (scratch, straight from the definition: entries in
`Q°_0`, `C_00 ≠ 0`, annihilation of the rank-one basis of `W ⊗ W`): no contraction at
`(13, 4)` and `(5, 4)`; contractions at `(7, 3)` and `(3, 2)`; the Lean matrix for
`(7, 3)`, `ξ = 3`, is `[[1,0,6],[1,1,0],[0,1,1]]`, all entries cubes or 0; `ε = 2` and
`A(1,3) = 0` at `p = 13`, `A(2,0) = 0` at `p = 29` with `ξ = 2`. Larger cases were too
big for the naive search and were not run.

## 3. Differences from the paper (all harmless, as stated)

1. `κ ≥ 1` is allowed (`NeZero κ`); the appendix assumes `κ ≥ 2`. At `κ = 1`, `E2 1 = ∅`.
2. `W ⊗ W` is the rows-and-columns set; not proved equal to a Mathlib `TensorProduct`,
   but `E2` does not depend on the reading (Section 1).
3. `E2` uses "every coset generator"; equivalence with "some" is proved.
4. (ii) is stated over ℤ; the proof uses only `#pairs ≥ (κ−1)(κ−2)` and injectivity of
   the witnesses, not `Σ A(u,v) = p − 2`.
5. Divisor lemma with `D ≥ 1` instead of `D ≥ 2` (weaker hypothesis); proved by
   restricting `C` itself, not the coset form; no `gcd(D, κ/D) = 1`.
6. Normal form proved by test tensors instead of a dimension count; transfer proved for
   every nonzero `ξ'`.
7. Not checked: (iii) (Weil bound), Remark `rem:app-s2-local-scope`, thresholds.

The report's Sections 2–4 state these accurately; I found nothing it omits.

## 4. Build and axioms

From `formal/`, `PATH=$HOME/.elan/bin:$PATH`, `nice -n 10` (load average about 59–100):

| Command | Result |
|---|---|
| `lake build --wfail Formal.ReesS2Local Formal.Audit` | `Build completed successfully (3501 jobs)` (replayed) |
| `lake build --wfail` (default target `Formal`) | `Build completed successfully (3525 jobs)` |
| `lake env lean` on a scratch file with `#print axioms` for all 29 theorems of the module (the 14 guarded ones, `no_contraction_of_A_eq_zero`, `hasContraction_of_dvd`, `isCosetGen_of_dvd`, `exists_cosetGen`, the 10 instances by (ii), `three_not_mem_E2_two`) | every one `[propext, Classical.choice, Quot.sound]`; adversarial examples of Section 2 compile |

`formal/Formal/Audit.lean`: 552 `#print axioms` lines, 14 for `QSearch.ReesS2Local`.
Table `tab:lean-modules` summed to 500 over 40 rows before this pass; with the new row,
514, and 514 + 38 = 552.

## 5. Integration (this pass)

* `docs/papers/rees-hsp/main.tex`: version note (lines ~91–96) names `ReesS2Local` and
  its report; Lean-boundary paragraph: one sentence on the integration, `500 → 514`,
  `538 → 552`, namespace count now also for `ReesS2Local`; new row in Part 3 of
  `tab:lean-modules` (report's text plus the `W ⊗ W` reading), Total `500 → 514`.
* `docs/papers/rees-hsp/appendix-schedule2.tex`: one sentence in the status line of
  `app:s2-local` (Lean check of the two lemmas and (i),(ii); (iii) and the Remark not).
* `formal/README.md`: `Formal/ReesS2Local.lean` in the guarded-file list; new section
  with a one-row table after `ReesMergeReduction`.
* `core/main-core.tex` states no guard counts and does not include the appendix:
  unchanged. No test pins the counts (`tests/tools/test_rees_paper_numbers.py` checks
  `numbers.tex` only).

Paper build in a scratch copy: `latexmk -g -pdf`, exit 0, 176 pages, 0 Overfull, no
LaTeX warning, no undefined reference, no Float too large. `test_rees_paper_numbers.py`:
2 passed; `tests/test_rees_circuit_round2.py` (reads a Lean source): 20 passed, 1
skipped (slow class-five case). `make_numbers.py` not run. Claim gates unchanged.
Machine-checked in Lean; AI-run, pending human review. Nothing committed.
