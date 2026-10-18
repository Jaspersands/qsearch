import Formal.CycleIndicator
import Formal.StdRepExterior
import Mathlib.LinearAlgebra.Trace

/-!
# Milestone 2 (partial): the `j = 1` coefficient is the trace on `V_std`

Source: `research/PRIME_CHARACTER_EXTERIOR_BOUND.md`, lines 44-56.

The full milestone, `det(1 - tσ | V) = ∏ (1 - t^ℓᵢ)/(1 - t)` for the actual
standard representation together with `χ_j = Tr(σ | Λ^j V)` for every `j`,
is NOT proved here (see `formal/README.md` for where it got stuck).

What is proved is the first nontrivial coefficient: for `σ ∈ S_n` and the
polynomial quotient `Q = ∏ (1 - (-z)^ℓᵢ) / (1 + z)` over the cycle lengths of
`σ` (fixed points included), `Q₁` equals the trace of `σ` on the
standard representation `stdRep` of `Formal.StdRepExterior`, namely
`#fixed points - 1`. So the Python value `chars[1]` is `Tr(σ | Λ¹ V)`.
-/

open Polynomial Finset Equiv

namespace QSearch

/-- Degree-one coefficient of a product. -/
lemma coeff_one_mul (p q : ℤ[X]) :
    (p * q).coeff 1 = p.coeff 0 * q.coeff 1 + p.coeff 1 * q.coeff 0 := by
  rw [coeff_mul, Finset.Nat.antidiagonal_succ]
  simp

lemma neg_X_pow_eq (ℓ : ℕ) : ((-X : ℤ[X]) ^ ℓ) = C ((-1) ^ ℓ) * X ^ ℓ := by
  rw [neg_pow, map_pow, map_neg, map_one]

lemma factor_coeff_zero {ℓ : ℕ} (hℓ : 0 < ℓ) : (1 - (-X : ℤ[X]) ^ ℓ).coeff 0 = 1 := by
  rw [coeff_sub, neg_X_pow_eq, coeff_C_mul_X_pow]
  simp [hℓ.ne]

lemma factor_coeff_one (ℓ : ℕ) : (1 - (-X : ℤ[X]) ^ ℓ).coeff 1 = if ℓ = 1 then 1 else 0 := by
  rw [coeff_sub, neg_X_pow_eq, coeff_C_mul_X_pow, coeff_one]
  by_cases h : ℓ = 1
  · subst h; simp
  · simp [h, Ne.symm h]

lemma permDet_coeff_zero (L : List ℕ) (hpos : ∀ ℓ ∈ L, 0 < ℓ) : (permDet L).coeff 0 = 1 := by
  induction L with
  | nil => simp
  | cons ℓ rest ih =>
    rw [permDet_cons, mul_coeff_zero, factor_coeff_zero (hpos ℓ List.mem_cons_self),
      ih fun k hk => hpos k (List.mem_cons_of_mem _ hk), mul_one]

/-- `[z¹] ∏ (1 - (-z)^ℓᵢ)` counts the fixed points (the `ℓᵢ = 1`). -/
lemma permDet_coeff_one (L : List ℕ) (hpos : ∀ ℓ ∈ L, 0 < ℓ) :
    (permDet L).coeff 1 = (L.count 1 : ℤ) := by
  induction L with
  | nil => rw [permDet_nil, coeff_one]; simp
  | cons ℓ rest ih =>
    have hrest : ∀ k ∈ rest, 0 < k := fun k hk => hpos k (List.mem_cons_of_mem _ hk)
    rw [permDet_cons, coeff_one_mul, factor_coeff_zero (hpos ℓ List.mem_cons_self),
      factor_coeff_one, ih hrest, permDet_coeff_zero rest hrest, List.count_cons]
    by_cases h : ℓ = 1 <;> simp [h, add_comm]

lemma geomFactor_coeff_zero {ℓ : ℕ} (hℓ : 0 < ℓ) : (geomFactor ℓ).coeff 0 = 1 := by
  rw [geomFactor, finsetSum_coeff]
  simp_rw [neg_X_pow_eq, coeff_C_mul_X_pow]
  rw [Finset.sum_ite_eq (range ℓ) 0 (fun i => ((-1 : ℤ) ^ i))]
  simp [hℓ]

lemma geomFactor_coeff_one (ℓ : ℕ) : (geomFactor ℓ).coeff 1 = if 1 < ℓ then -1 else 0 := by
  rw [geomFactor, finsetSum_coeff]
  simp_rw [neg_X_pow_eq, coeff_C_mul_X_pow]
  rw [Finset.sum_ite_eq (range ℓ) 1 (fun i => ((-1 : ℤ) ^ i))]
  simp

/-- `χ₁ = (number of fixed points) - 1`, on the polynomial side. -/
theorem stdDet_coeff_one {L : List ℕ} (hL : L ≠ []) (hpos : ∀ ℓ ∈ L, 0 < ℓ) :
    (stdDet L).coeff 1 = (L.count 1 : ℤ) - 1 := by
  cases L with
  | nil => exact absurd rfl hL
  | cons ℓ rest =>
    have hℓ : 0 < ℓ := hpos ℓ List.mem_cons_self
    have hrest : ∀ k ∈ rest, 0 < k := fun k hk => hpos k (List.mem_cons_of_mem _ hk)
    rw [stdDet_cons, coeff_one_mul, geomFactor_coeff_zero hℓ, geomFactor_coeff_one,
      permDet_coeff_one rest hrest, permDet_coeff_zero rest hrest, List.count_cons]
    by_cases h : ℓ = 1
    · subst h; simp
    · have h1 : 1 < ℓ := by omega
      simp [h, h1, sub_eq_add_neg]

/-- The number of `1`s among all cycle lengths is the number of fixed points. -/
lemma count_one_partition {α : Type*} [Fintype α] [DecidableEq α] (σ : Perm α) :
    σ.partition.parts.count 1 = (univ.filter fun a => σ a = a).card := by
  rw [Perm.parts_partition, Multiset.count_add, Multiset.count_replicate_self]
  have h0 : σ.cycleType.count 1 = 0 :=
    Multiset.count_eq_zero.mpr fun h => by have := Perm.two_le_of_mem_cycleType h; omega
  rw [h0, zero_add]
  have hsupp : σ.support = univ.filter fun a => ¬ σ a = a := by
    ext a; simp [Perm.mem_support]
  have := Finset.card_filter_add_card_filter_not (s := univ) (fun a => σ a = a)
  rw [hsupp, ← card_univ]
  omega

variable (K : Type*) [Field K] (m : ℕ)

/-- **Trace of `σ` on the standard representation** = `#fixed points - 1`. -/
theorem trace_stdRep (σ : Perm (Fin (m + 1))) :
    LinearMap.trace K _ (stdRep K m σ) = ((univ.filter fun k => σ k = k).card : K) - 1 := by
  rw [LinearMap.trace_eq_matrix_trace K (stdBasis K m), Matrix.trace]
  have hdiag : ∀ i : Fin m, LinearMap.toMatrix (stdBasis K m) (stdBasis K m) (stdRep K m σ) i i =
      (if Fin.castSucc i = σ (Fin.castSucc i) then 1 else 0) -
        (if Fin.castSucc i = σ (Fin.last m) then 1 else 0) := by
    intro i
    rw [LinearMap.toMatrix_apply, stdBasis, Module.Basis.ofEquivFun_repr_apply, ← stdBasis]
    change (stdRep K m σ (stdBasis K m i) : Fin (m + 1) → K) (Fin.castSucc i) = _
    rw [stdRep_stdBasis]
    simp [Pi.single_apply]
  simp only [Matrix.diag, hdiag, Finset.sum_sub_distrib]
  -- fixed points, split off the last coordinate
  have hfix : ((univ.filter fun k => σ k = k).card : K) =
      ∑ i : Fin m, (if Fin.castSucc i = σ (Fin.castSucc i) then 1 else 0) +
        (if σ (Fin.last m) = Fin.last m then 1 else 0) := by
    rw [Finset.card_filter, Nat.cast_sum, Fin.sum_univ_castSucc]
    simp [eq_comm]
  -- exactly one coordinate equals `σ last`
  have hone : ∑ i : Fin m, (if Fin.castSucc i = σ (Fin.last m) then (1 : K) else 0) +
      (if Fin.last m = σ (Fin.last m) then 1 else 0) = 1 := by
    rw [← Fin.sum_univ_castSucc (f := fun k => if k = σ (Fin.last m) then (1 : K) else 0)]
    simp
  rw [hfix]
  have heq : (if σ (Fin.last m) = Fin.last m then (1 : K) else 0) =
      (if Fin.last m = σ (Fin.last m) then 1 else 0) := by
    simp [eq_comm]
  rw [heq]
  linear_combination -hone

/-- **`χ₁` is the trace on `V_std` (milestone 2, `j = 1` only).** For `σ ∈ S_n`
and any `Q` with `∏ (1 - (-z)^ℓ) = (1 + z) Q` over the cycle lengths of `σ`,
the coefficient `Q₁` equals `Tr(σ | V_std)`. -/
theorem quotient_coeff_one_eq_trace (σ : Perm (Fin (m + 1))) (Q : ℤ[X])
    (hQ : permDetM σ.partition.parts = (1 + X) * Q) :
    (Q.coeff 1 : K) = LinearMap.trace K _ (stdRep K m σ) := by
  obtain ⟨L, hL⟩ := Quot.exists_rep σ.partition.parts
  have hcoe : σ.partition.parts = (L : Multiset ℕ) := hL.symm
  have hpos : ∀ ℓ ∈ L, 0 < ℓ := fun ℓ hℓ =>
    σ.partition.parts_pos (by rw [hcoe]; exact Multiset.mem_coe.mpr hℓ)
  have hsum : L.sum = m + 1 := by
    have h := σ.partition.parts_sum
    rw [hcoe, Multiset.sum_coe, Fintype.card_fin] at h
    exact h
  have hne : L ≠ [] := by
    rintro rfl
    simp at hsum
  rw [hcoe, permDetM_coe] at hQ
  rw [stdDet_unique hne hQ, stdDet_coeff_one hne hpos, trace_stdRep]
  have hcount : L.count 1 = (univ.filter fun k => σ k = k).card := by
    rw [← count_one_partition σ, hcoe, Multiset.coe_count]
  rw [hcount]
  push_cast
  ring

end QSearch
