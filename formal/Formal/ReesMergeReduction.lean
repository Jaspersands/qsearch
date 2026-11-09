import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.LinearAlgebra.LinearIndependent.Defs
import Mathlib.Algebra.Module.BigOperators

/-!
# Rees merge reduction: step (R) of the exhaustive merge checks

Source: `research/audits/reviews/2026-11-05-rees-receiver-sims.md`, Section 2, and
`theorems/rees_circuit_exhaustive.py` (module docstring, step (R)). AI-written,
pending human review.

The exhaustive merge checks verify by exact finite computation, at one grade `d`:

* (E2) every conditioned branch is a monomial twist of the zero-label branch:
  `φ c g = ζ ^ (∑ j, c j * W g j).val * φ 0 g` for the coordinates `c` of the label in a
  basis `b` of `K^⊥` (and the branches share the support of `φ 0`);
* (E3) for the value set of the witness, on the support `Σ_T` of the zero-label merge
  the vectors `t⁻ᵈ W(δ_t g)` agree, i.e. `W (δ t g) = t ^ d • τ g` there.

Step (R) concludes that for EVERY label tuple and EVERY witness `s` (nonzero entries only
are merged) the merged product `∏_{s_i ≠ 0} φ_{λ_i}(δ_{s_i} g)` equals the zero-label
product `∏_{s_i ≠ 0} φ_0(δ_{s_i} g)` pointwise. Since the merge output (descent and
normalisation) is a function of that product, every pair gives the zero-label output,
which (E3) checks to be `ρ_{H_{d-1}}`. That last sentence is about the code, not
formalized here.

Main results:
* `witness_coords`: the witness equation `∑ s_i^d λ_i = 0` with `λ_i = ∑_j c_ij b_j`
  and `b` linearly independent gives `∑_i s_i^d c_ij = 0` for every `j`;
* `exponent_cancels`: (E3) plus the coordinate witness equation make the total twist
  exponent vanish (inactive indices drop out because `0 ^ d = 0`, `d ≥ 1`);
* `merge_product_eq`: the pointwise product identity (step (R));
* `merge_product_eq_of_labels`: the same, stated for labels in a span with a basis;
* `zero_product_indicator`: the zero-label product is `κ^#A` times the indicator of `Σ_T`.
-/

namespace QSearch.ReesMergeReduction

open Finset

variable {p : ℕ} [NeZero p]

/-- `ζ ^ x.val` is additive in `x : ZMod p` when `ζ ^ p = 1`. -/
theorem pow_val_add {R : Type*} [Monoid R] (ζ : R) (hζ : ζ ^ p = 1) (x y : ZMod p) :
    ζ ^ (x + y).val = ζ ^ x.val * ζ ^ y.val := by
  rw [← pow_add, ZMod.val_add]
  conv_rhs => rw [← Nat.mod_add_div (x.val + y.val) p]
  rw [pow_add, pow_mul, hζ, one_pow, mul_one]

/-- A product of `ζ ^ (e i).val` over a finset is `ζ ^ (∑ e i).val`. -/
theorem prod_pow_val {R : Type*} [CommMonoid R] {ι : Type*} (ζ : R) (hζ : ζ ^ p = 1)
    (S : Finset ι) (e : ι → ZMod p) :
    ∏ i ∈ S, ζ ^ (e i).val = ζ ^ (∑ i ∈ S, e i).val := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | insert a S ha ih => rw [prod_insert ha, sum_insert ha, pow_val_add ζ hζ, ih]

omit [NeZero p] in
/-- Coordinates of the witness equation in a basis. -/
theorem witness_coords {k g M : ℕ} (d : ℕ) (b : Fin k → (Fin g → ZMod p))
    (hb : LinearIndependent (ZMod p) b) (s : Fin M → ZMod p) (c : Fin M → Fin k → ZMod p)
    (hwit : ∑ i, (s i) ^ d • (∑ j, c i j • b j) = 0) :
    ∀ j, ∑ i, (s i) ^ d * c i j = 0 := by
  have h : ∑ j, (∑ i, (s i) ^ d * c i j) • b j = 0 := by
    rw [← hwit]
    simp only [Finset.smul_sum, smul_smul, Finset.sum_smul]
    exact Finset.sum_comm
  exact (Fintype.linearIndependent_iff.mp hb) _ h

omit [NeZero p] in
/-- The total twist exponent of a merged product vanishes. `W i j` stands for
`W_j(δ_{s_i} g)` at a fixed `g` in the support `Σ_T`. -/
theorem exponent_cancels {k M : ℕ} (d : ℕ) (hd : 1 ≤ d)
    (s : Fin M → ZMod p) (c : Fin M → Fin k → ZMod p)
    (W : Fin M → Fin k → ZMod p) (τ : Fin k → ZMod p)
    (hW : ∀ i, s i ≠ 0 → ∀ j, W i j = (s i) ^ d * τ j)
    (hwit : ∀ j, ∑ i, (s i) ^ d * c i j = 0) :
    ∑ i ∈ univ.filter (fun i => s i ≠ 0), ∑ j, c i j * W i j = 0 := by
  classical
  have step : ∀ i ∈ univ.filter (fun i => s i ≠ 0),
      ∑ j, c i j * W i j = ∑ j, (s i) ^ d * c i j * τ j := by
    intro i hi
    have hs : s i ≠ 0 := (mem_filter.mp hi).2
    refine sum_congr rfl fun j _ => ?_
    rw [hW i hs j]; ring
  rw [sum_congr rfl step]
  have hzero : ∀ i ∈ (univ : Finset (Fin M)), i ∉ univ.filter (fun i => s i ≠ 0) →
      ∑ j, (s i) ^ d * c i j * τ j = 0 := by
    intro i _ hi
    have : s i = 0 := by simpa using hi
    have hpow : (s i) ^ d = 0 := by rw [this]; exact zero_pow (by omega)
    simp [hpow]
  rw [sum_subset (filter_subset _ _) hzero, sum_comm]
  refine sum_eq_zero fun j _ => ?_
  rw [← sum_mul, hwit j, zero_mul]

/-- Step (R), pointwise. `φ c` is the branch with label coordinates `c`; `supp0` contains
the support of `φ 0`; `δ t` is the dilation; `τ` the common value of `t⁻ᵈ W(δ_t g)`
from (E3). For every label tuple `c` and every witness `s` in coordinates, the merged
product over the nonzero entries of `s` equals the zero-label product. -/
theorem merge_product_eq {G R : Type*} [CommRing R] {k M : ℕ} (d : ℕ) (hd : 1 ≤ d)
    (ζ : R) (hζ : ζ ^ p = 1)
    (supp0 : Set G) (φ : (Fin k → ZMod p) → G → R) (W : G → Fin k → ZMod p)
    (hE2 : ∀ c g, φ c g = ζ ^ (∑ j, c j * W g j).val * φ 0 g)
    (hsupp : ∀ g, g ∉ supp0 → φ 0 g = 0)
    (δ : ZMod p → G → G) (s : Fin M → ZMod p) (c : Fin M → Fin k → ZMod p)
    (hwit : ∀ j, ∑ i, (s i) ^ d * c i j = 0) (τ : G → Fin k → ZMod p)
    (hE3 : ∀ g, (∀ i, s i ≠ 0 → δ (s i) g ∈ supp0) →
      ∀ i, s i ≠ 0 → ∀ j, W (δ (s i) g) j = (s i) ^ d * τ g j) (g : G) :
    ∏ i ∈ univ.filter (fun i => s i ≠ 0), φ (c i) (δ (s i) g)
      = ∏ i ∈ univ.filter (fun i => s i ≠ 0), φ 0 (δ (s i) g) := by
  classical
  set A := univ.filter (fun i : Fin M => s i ≠ 0)
  by_cases hin : ∀ i, s i ≠ 0 → δ (s i) g ∈ supp0
  · simp only [hE2 (c _)]
    rw [prod_mul_distrib, prod_pow_val ζ hζ]
    have h0 := exponent_cancels d hd s c (fun i j => W (δ (s i) g) j) (τ g) (hE3 g hin) hwit
    rw [h0, ZMod.val_zero, pow_zero, one_mul]
  · push Not at hin
    obtain ⟨i, hi, hnot⟩ := hin
    have hiA : i ∈ A := mem_filter.mpr ⟨mem_univ _, hi⟩
    have z0 : φ 0 (δ (s i) g) = 0 := hsupp _ hnot
    have lhs : ∏ i ∈ A, φ (c i) (δ (s i) g) = 0 :=
      prod_eq_zero hiA (by rw [hE2, z0, mul_zero])
    rw [lhs, prod_eq_zero hiA z0]

/-- Step (R) for labels in the span of a basis `b` of `K^⊥`: labels `λ_i = ∑_j c_ij b_j`
and a witness `∑_i s_i^d λ_i = 0`. -/
theorem merge_product_eq_of_labels {G R : Type*} [CommRing R] {k gdim M : ℕ} (d : ℕ)
    (hd : 1 ≤ d) (ζ : R) (hζ : ζ ^ p = 1)
    (supp0 : Set G) (φ : (Fin k → ZMod p) → G → R) (W : G → Fin k → ZMod p)
    (hE2 : ∀ c g, φ c g = ζ ^ (∑ j, c j * W g j).val * φ 0 g)
    (hsupp : ∀ g, g ∉ supp0 → φ 0 g = 0)
    (δ : ZMod p → G → G) (b : Fin k → (Fin gdim → ZMod p))
    (hb : LinearIndependent (ZMod p) b) (s : Fin M → ZMod p) (c : Fin M → Fin k → ZMod p)
    (hwit : ∑ i, (s i) ^ d • (∑ j, c i j • b j) = 0) (τ : G → Fin k → ZMod p)
    (hE3 : ∀ g, (∀ i, s i ≠ 0 → δ (s i) g ∈ supp0) →
      ∀ i, s i ≠ 0 → ∀ j, W (δ (s i) g) j = (s i) ^ d * τ g j) (g : G) :
    ∏ i ∈ univ.filter (fun i => s i ≠ 0), φ (c i) (δ (s i) g)
      = ∏ i ∈ univ.filter (fun i => s i ≠ 0), φ 0 (δ (s i) g) :=
  merge_product_eq d hd ζ hζ supp0 φ W hE2 hsupp δ s c (witness_coords d b hb s c hwit) τ hE3 g

omit [NeZero p] in
open Classical in
/-- The zero-label product with any multiplicities: if `φ 0` is the constant `κ` on its
support `supp0` (checked exactly as "`φ_0` constant on its support"), the product over the
nonzero entries of `s` is `κ ^ #A` on `Σ_T = {g | δ_{s_i} g ∈ supp0 for all i ∈ A}` and `0`
off it. So it depends on `s` only through the value set `T` and the count `#A`, and the
normalised merge output depends on `T` only. -/
theorem zero_product_indicator {G R : Type*} [CommRing R] {M : ℕ}
    (supp0 : Set G) (φ0 : G → R) (κ : R)
    (hconst : ∀ g, g ∈ supp0 → φ0 g = κ) (hsupp : ∀ g, g ∉ supp0 → φ0 g = 0)
    (δ : ZMod p → G → G) (s : Fin M → ZMod p) (g : G) :
    ∏ i ∈ univ.filter (fun i => s i ≠ 0), φ0 (δ (s i) g)
      = if (∀ i, s i ≠ 0 → δ (s i) g ∈ supp0)
        then κ ^ (univ.filter (fun i : Fin M => s i ≠ 0)).card else 0 := by
  classical
  split_ifs with hin
  · rw [prod_congr rfl (fun i hi => hconst _ (hin i (mem_filter.mp hi).2)), prod_const]
  · push Not at hin
    obtain ⟨i, hi, hnot⟩ := hin
    exact prod_eq_zero (mem_filter.mpr ⟨mem_univ _, hi⟩) (hsupp _ hnot)

end QSearch.ReesMergeReduction
