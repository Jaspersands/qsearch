# 2026-11-09 Rees: Lean check of prop:dl-central-scalars and the unitriangular exp/log condition

Status: machine-checked in Lean 4.35.0 + Mathlib v4.35.0 (the project in `formal/`). There is
no `sorry`, and every headline result depends only on `propext`, `Classical.choice` and
`Quot.sound`; guards are in `formal/Formal/Audit.lean`. The Lean was written by an AI side
session. The kernel checks the proofs; a human still has to check that the Lean *statements*
below say what the paper says (sections 0 and 2 give the comparison). Nothing in the paper, the prep
tree or `STATE.md` was edited, and no git command was run.

Sources checked:

- Proposition `prop:dl-central-scalars` and Section `sec:dixmier-lister` in
  `research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/core/main-core.tex`
  (section l. 391-432, proposition l. 408-411). Referee:
  `2026-11-09-rees-dl-scalars-schedule2-referee.md` §1.
- The item *Unitriangular matrix groups* in
  `research/audits/reviews/2026-11-08-rees-blackbox-corollary-draft.tex` (l. 38).

## 0. Verdict

| Claim | Lean result | Mismatch with the text |
|---|---|---|
| prop:dl-central-scalars, Lie sentence (field `K`, char ≠ 2, `ζ ∈ K^×`) | **proved** for every field with `2 ≠ 0`, `ζ ∈ K` (`exists_aut_center_smul_iff`) | none |
| prop:dl-central-scalars, "in particular" (Lazard group over `F_p`, `p > 3`) | **proved**, both for `ζ ∈ F_p` (`group_center_pow_iff`) and integer exponents `k` (`group_center_zpow_iff`: iff `k ≡ ±1 mod p`) | none |
| Black-box draft: `A^p = 0` when `n ≤ p` | **proved** (`strictUpper_prod_eq_zero`, `unitriangular_condition`) | none |
| Black-box draft: `G ⊆ I + A`, `(I+N)^p = I`, exponent divides `p` | **proved** (`matrix_group_condition`) | none |
| Black-box draft: truncated `exp` and `log` are inverse bijections `A ↔ I + A`, denominators prime to `p` | **proved** (`expEquiv`, `texp_tlog`, `tlog_texp`, `factorial_ne_zero`, `natCast_ne_zero`) | none |

No finding against either text. Three points of form, none a mismatch:

1. **The rank-one-locus step is replaced by a determinant argument, not checked literally.**
   The paper shows that `A` preserves or exchanges `U_±` by looking at the vectors `x` with
   one-dimensional `([x,L]+γ₃)/γ₃`. The Lean proof (`core_alg`) gets the same dichotomy from
   the eight vanishing cross minors (`[φu_i, φu_j] ∈ γ₃` for `i ∈ {1,2}`, `j ∈ {3,4}`) and
   `det A ≠ 0`, via a Laplace expansion along the `U₊` rows. The coefficient steps after
   that (keep: `ζ = μν`, `μ³ = ν³ = ζ`, so `ζ = 1`; swap: `ζ = -αβ`, `α³ = β³ = -ζ`, so
   `ζ = -1`) are the paper's (`keep_final`, `swap_final`). The referee checked the
   rank-one-locus argument by hand (§1.2) and found it correct.
2. **"We may assume K algebraically closed"** is done by an explicit base change. The matrix
   of `φ` over `K` defines a bracket-preserving surjection of `DL (AlgebraicClosure K)`
   (`bc`, `bc_lie`, `bc_surj`) with the same action on the centre. Only `i² = -1` is used.
3. **The Lazard step is proved, not cited.** The paper says that the Lazard correspondence
   identifies the automorphisms of `exp(L_DL)` with those of `L_DL`. Lean uses the repo's
   class-three BCH group of `DL (ZMod p)`, whose multiplication is
   `x*y = x + y + ½[x,y] + (1/12)([x,[x,y]] + [y,[y,x]])`. It turns every group
   automorphism into a Lie automorphism through the explicit power and commutator words of
   `Formal/BCHClassThreeSubgroups.lean` (`toLieEquiv`), and goes back through
   `BCHClassThree.lieEquiv`. So the group statement covers all abstract group automorphisms,
   with no linearity assumed.

## 1. What was formalised

### 1a. `formal/Formal/DixmierListerScalars.lean` (Lie algebra; 773 lines)

`DL R` is `Fin 8 → R` with the bracket defined coordinatewise from the paper's table, over
any commutative ring `R`. Lean index `j` is the paper's `e_{j+1}`. Jacobi, bilinearity and
`[x,x] = 0` are proved, so `DL R` is a genuine Mathlib `LieRing` and `LieAlgebra R`.

| Lean | Content |
|---|---|
| `table`, `table_zero` | the ten nonzero brackets of the paper's table, and `[e_j,e_k] = 0` for every other pair `j < k` (checked against main-core.tex l. 395-398: all ten agree) |
| `mem_center_iff` | `z ∈ center ↔ z₁ = … = z₆ = 0` (any commutative ring), i.e. the centre is `span(e₇,e₈)` |
| `signEquiv`, `signEquiv_center` | the paper's sign automorphism (`+` on `e₁,e₃,e₆`, `-` on the other five) is a Lie automorphism acting as `-1` on the centre |
| `keep_final`, `swap_final` | the two closing coefficient computations (the keep case ends with `ζ = 1`, the swap case with `ζ = -1`) |
| `core_alg` | the `4 × 4` algebra: cross minors and coefficient equations, together with `det A ≠ 0`, force `ζ = ±1` |
| `scalar_core` | over a field with `2 ≠ 0` containing `i`, `i² = -1`: a bracket-preserving linear surjection with `φ(e₇) = ζe₇`, `φ(e₈) = ζe₈` has `ζ = ±1` |
| `bc`, `bc_lie`, `bc_surj`, `scalar_of_equiv` | base change to `AlgebraicClosure K` |
| **`exists_aut_center_smul_iff`** | the proposition, first sentence |

```lean
theorem exists_aut_center_smul_iff {K : Type*} [Field K] (h2 : (2 : K) ≠ 0) (ζ : K) :
    (∃ φ : DL K ≃ₗ⁅K⁆ DL K, ∀ z ∈ LieAlgebra.center K (DL K), φ z = ζ • z) ↔
      ζ = 1 ∨ ζ = -1
```

### 1b. `formal/Formal/DixmierListerGroup.lean` (group; 209 lines)

| Lean | Content |
|---|---|
| `lcs_three_eq_bot` | `γ₄(DL R) = 0` over any commutative ring (`γ₂ ⊆ span(e₅..e₈)`, `γ₃ ⊆ span(e₇,e₈)`) |
| `DLGroup p` | `BCH (ZMod p) (DL (ZMod p)) lcs_three_eq_bot`, the Lazard group |
| `toLieEquiv` | a group automorphism of `DLGroup p` gives a Lie automorphism of `DL (ZMod p)` with the same action on logarithms |
| `mem_center_iff_val` | the group centre is `exp` of the Lie centre (from `bch a b = bch b a + [a,b]`) |
| **`group_center_pow_iff`**, **`group_center_zpow_iff`** | the proposition, second sentence |

```lean
variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]  -- i.e. p > 3
theorem group_center_pow_iff (ζ : ZMod p) :
    (∃ f : DLGroup p ≃* DLGroup p, ∀ z ∈ Subgroup.center (DLGroup p), f z = z ^ ζ.val) ↔
      ζ = 1 ∨ ζ = -1
theorem group_center_zpow_iff (k : ℤ) :
    (∃ f : DLGroup p ≃* DLGroup p, ∀ z ∈ Subgroup.center (DLGroup p), f z = z ^ k) ↔
      (k : ZMod p) = 1 ∨ (k : ZMod p) = -1
```

### 1c. `formal/Formal/UnitriangularExpLog.lean` (black-box draft; 464 lines)

Everything is over `ZMod p` with `p` prime. The exp/log part holds in any (possibly
noncommutative) `ZMod p`-algebra `R`.

| Lean | Content |
|---|---|
| `expPoly`, `logPoly` | `∑_{k<p} X^k/k!` and `∑_{1≤k<p} (-1)^{k+1} X^k/k` in `F_p[X]` |
| `factorial_ne_zero`, `natCast_ne_zero`, `factorial_mul_coeff_expPoly`, `mul_coeff_logPoly` | the denominators `k!` and `k` (`0 < k < p`) are units mod `p`, and the coefficients are their inverses |
| `exp_log_congr`, `log_exp_congr` | `exp(log(1+X)) ≡ 1+X` and `log(exp X) ≡ X` mod `X^p`, by the derivative argument (`exp' ≡ exp`, `(1+X)log' ≡ 1` mod `X^{p-1}`, the chain rule, and uniqueness of the first-order recurrences; `dvd_of_ode`, `dvd_of_deriv`, `dvd_of_mul_dvd`) |
| `one_add_pow` | `N^p = 0 → (1+N)^p = 1` |
| `texp_tlog`, `tlog_texp` | `exp(log(1+N)) = 1+N` and `log(exp N) = N` whenever `N^p = 0` |
| `expEquiv` | for a non-unital subalgebra `A` with `N^p = 0` on `A`: `exp : A ≃ {g // g - 1 ∈ A}`, inverse `log` |
| `unipotent`, `pow_eq_one`, `closure_le_unipotent` | `{u | u - 1 ∈ A}` is a subgroup of units of exponent dividing `p` containing the group generated by any `gᵢ` with `gᵢ - 1 ∈ A` |
| **`matrix_group_condition`** | the draft's sentence, for any `A ∋ gᵢ - 1` with `A^p = 0` |
| `strictUpper`, `strictUpper_prod_eq_zero` | strictly upper triangular `n × n` matrices; every product of `n` of them is `0` |
| **`unitriangular_condition`** | for `gᵢ ∈ UT_n(F_p)` and `n ≤ p`: the algebra generated by the `gᵢ - I` has `A^p = 0`, and the conclusions of `matrix_group_condition` hold |

```lean
theorem matrix_group_condition {p : ℕ} [Fact p.Prime] {R : Type*} [Ring R] [Algebra (ZMod p) R]
    (A : NonUnitalSubalgebra (ZMod p) R) {ι : Type*} (g : ι → Rˣ) (hg : ∀ i, (g i : R) - 1 ∈ A)
    (hA : ∀ l : List R, l.length = p → (∀ a ∈ l, a ∈ A) → l.prod = 0) :
    (∀ u ∈ Subgroup.closure (Set.range g), (u : R) - 1 ∈ A ∧ u ^ p = 1) ∧
    (∀ N ∈ A, texp p N - 1 ∈ A ∧ tlog p (texp p N - 1) = N) ∧
    (∀ x : R, x - 1 ∈ A → tlog p (x - 1) ∈ A ∧ texp p (tlog p (x - 1)) = x)
```

## 2. How the statements are encoded (for the human check)

- `ζ ∈ K` rather than `K^×`: slightly stronger. `ζ = 0` is false on both sides.
- `L_DL ⊗ K` is `DL K`, the same structure constants over `K`; an automorphism is a
  `LieEquiv` (`≃ₗ⁅K⁆`). "Characteristic other than 2" is `(2 : K) ≠ 0`.
- "Its centre `γ₃(L_DL) = Span(e₇,e₈)`": Lean uses `LieAlgebra.center` and proves that it
  is `span(e₇,e₈)`. The equality with `γ₃` is not needed and only `γ₃ ⊆ span(e₇,e₈)` is
  proved.
- "`p > 3`" is `[Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]`. "`z ↦ z^ζ`" is
  `z ^ ζ.val` for `ζ ∈ ZMod p`, and separately `z ^ k` for `k ∈ ℤ`.
- "`A^p = 0`" is "every product of `p` elements of `A` is `0`" (the `List.prod`
  hypothesis). It is used only through its consequence `N^p = 0` for `N ∈ A`, which is all
  that the exp/log bijection and the exponent need.
- "`G ⊆ I + A`" is `u - 1 ∈ A` for every `u` in `Subgroup.closure (Set.range g)` inside the
  unit group `Rˣ`, with `R = Matrix (Fin n) (Fin n) (ZMod p)` in `unitriangular_condition`.

## 3. Not formalised

- Section `sec:dixmier-lister` outside the proposition: the 12-dimensional derivation space,
  the row certificates, the absence of a positive grading, the dimensions `(8, 4, 2)` and
  `γ₃ = span(e₇,e₈)` as an equality. Also the GAP automorphism-group orders at `p = 5, 7`,
  and whether the paper's table is the algebra of Dixmier–Lister 1957.
- In the black-box item: "`G` has class below `p`", the truncated BCH identity
  `exp X exp Y = exp BCH(X,Y)` on `A`, the identification of `log` on `G` with the Lazard
  logarithm, `L' = log G`, the `poly(n,s,log p)` linear algebra, and the `F_p ⋉ F_p^m`
  remark.

## 4. Build

```text
cd formal
export PATH=$HOME/.elan/bin:$PATH
nice -n 19 lake exe cache get        # prebuilt Mathlib; already present on this machine
nice -n 19 lake build Formal.DixmierListerScalars Formal.DixmierListerGroup Formal.UnitriangularExpLog
nice -n 19 lake build --wfail        # whole project, including the guards in Formal/Audit.lean
```

The three modules are imported by `Formal.lean` (the default target) and `Formal/Audit.lean`,
which guards the headline theorems with `#guard_msgs` on `#print axioms`.

Result, 2026-11-09, on this machine with `nice -n 19`:

- `lake build --wfail` of the three modules: success, with no errors and no warnings.
- Full `lake build --wfail`: success (9123 jobs). `Formal/Audit.olean` and `Formal.olean`
  were rebuilt after the guards were added.
- Each guarded declaration depends on exactly `[propext, Classical.choice, Quot.sound]`.
- `grep sorry` finds nothing in the three files.

The 23 guards cover:

- in `DixmierLister`: `table`, `table_zero`, `mem_center_iff`, `signEquiv_center`,
  `core_alg`, `scalar_core`, `exists_aut_center_smul_iff`, `lcs_three_eq_bot`,
  `toLieEquiv`, `mem_center_iff_val`, `group_center_pow_iff`, `group_center_zpow_iff`;
- in `UnitriangularExpLog`: `natCast_ne_zero`, `factorial_ne_zero`, `exp_log_congr`,
  `log_exp_congr`, `texp_tlog`, `tlog_texp`, `expEquiv`, `pow_eq_one`,
  `matrix_group_condition`, `strictUpper_prod_eq_zero`, `unitriangular_condition`.

Optional cleanup: the two new modules `import Mathlib` whole. Mathlib's `minImports` linter
proposed an import set that reaches the needed instances through unrelated modules (such as
`Mathlib.RingTheory.Henselian`), so it was not adopted.
