import Mathlib.Algebra.Ring.GeomSum
import Mathlib.Algebra.Polynomial.BigOperators
import Mathlib.Algebra.Polynomial.Eval.Degree
import Mathlib.GroupTheory.Perm.Cycle.Type

/-!
# Milestone 1: the cycle indicator, in polynomial form

Source: `research/PRIME_CHARACTER_EXTERIOR_BOUND.md`, lines 44-58, and its
executable mirror `exterior_characters`
(`theorems/prime_character_exterior_bound.py`, line 33).

For a permutation with cycle lengths `L = [ℓ₁, …, ℓ_c]` the Python code forms the
integer polynomial

    numerator(z) = ∏ᵢ (1 - (-z)^ℓᵢ)          -- `permDet L` below

(this is `det(1 + z σ)` on the permutation representation, i.e. the note's
`∏ (1 - t^ℓᵢ)` at `t = -z`), divides it by `1 + z`, and returns the quotient's
coefficients `χ₀, …, χ_{n-1}` (`stdDet L` below). The note's exact identity
(lines 52-54) is that the alternating sum of those coefficients is `n` when
`c = 1` and `0` otherwise.

Everything here is about integer polynomials only; the link to the actual
standard representation is a separate milestone.
-/

open Polynomial Finset

namespace QSearch

noncomputable section

/-- `∏_{ℓ ∈ L} (1 - (-z)^ℓ)`: the Python `numerator`, i.e. `det(1 + zσ)` on the
permutation representation of a permutation with cycle lengths `L`. -/
def permDet (L : List ℕ) : ℤ[X] :=
  (L.map fun ℓ => (1 - (-X) ^ ℓ : ℤ[X])).prod

/-- `∑_{i<ℓ} (-z)^i`, so that `1 - (-z)^ℓ = (1 + z) * geomFactor ℓ`. -/
def geomFactor (ℓ : ℕ) : ℤ[X] :=
  ∑ i ∈ range ℓ, (-X) ^ i

/-- The quotient `permDet L / (1 + z)`, written down explicitly.
Its coefficients are the Python `chars`. (`stdDet [] = 0` is a junk value;
the Python function rejects the empty list.) -/
def stdDet : List ℕ → ℤ[X]
  | [] => 0
  | ℓ :: rest => geomFactor ℓ * permDet rest

end

@[simp] lemma permDet_nil : permDet [] = 1 := by
  simp [permDet]

@[simp] lemma permDet_cons (ℓ : ℕ) (L : List ℕ) :
    permDet (ℓ :: L) = (1 - (-X) ^ ℓ) * permDet L := by
  simp [permDet]

@[simp] lemma stdDet_cons (ℓ : ℕ) (L : List ℕ) :
    stdDet (ℓ :: L) = geomFactor ℓ * permDet L := rfl

/-- One cycle: `1 - (-z)^ℓ = (1 + z) ∑_{i<ℓ} (-z)^i`. -/
lemma one_sub_neg_X_pow (ℓ : ℕ) :
    (1 - (-X) ^ ℓ : ℤ[X]) = (1 + X) * geomFactor ℓ := by
  rw [geomFactor, ← sub_neg_eq_add (1 : ℤ[X]) X, mul_neg_geom_sum]

/-- **Divisibility, explicit form.** For every nonempty cycle list,
`∏ (1 - (-z)^ℓᵢ) = (1 + z) · stdDet L` in `ℤ[z]`. -/
theorem permDet_eq_mul_stdDet {L : List ℕ} (hL : L ≠ []) :
    permDet L = (1 + X) * stdDet L := by
  cases L with
  | nil => exact absurd rfl hL
  | cons ℓ rest => rw [permDet_cons, stdDet_cons, one_sub_neg_X_pow, mul_assoc]

/-- **Divisibility.** `1 + z` divides `∏ (1 - (-z)^ℓᵢ)` in `ℤ[z]`. -/
theorem one_add_X_dvd_permDet {L : List ℕ} (hL : L ≠ []) :
    (1 + X : ℤ[X]) ∣ permDet L :=
  ⟨_, permDet_eq_mul_stdDet hL⟩

lemma one_add_X_ne_zero : (1 + X : ℤ[X]) ≠ 0 := by
  intro h
  have := congrArg (Polynomial.eval (0 : ℤ)) h
  simp at this

/-- The quotient is unique, so `stdDet L` is *the* quotient `permDet L / (1 + z)`. -/
theorem stdDet_unique {L : List ℕ} (hL : L ≠ []) {Q : ℤ[X]}
    (h : permDet L = (1 + X) * Q) : Q = stdDet L :=
  mul_left_cancel₀ one_add_X_ne_zero (h.symm.trans (permDet_eq_mul_stdDet hL))

lemma geomFactor_eval_neg_one (ℓ : ℕ) : (geomFactor ℓ).eval (-1) = ℓ := by
  simp [geomFactor, eval_finsetSum]

lemma permDet_eval_neg_one (L : List ℕ) :
    (permDet L).eval (-1) = if L = [] then 1 else 0 := by
  cases L with
  | nil => simp
  | cons ℓ rest => simp

/-- **Cycle indicator, evaluation form.** `stdDet L` at `z = -1` (equivalently
`det(1 - σ | V)` at `t = 1`) is `n` for one cycle and `0` for two or more. -/
theorem stdDet_eval_neg_one (L : List ℕ) :
    (stdDet L).eval (-1) = if L.length = 1 then (L.sum : ℤ) else 0 := by
  rcases L with _ | ⟨ℓ, _ | ⟨m, rest⟩⟩
  · simp [stdDet]
  · simp [geomFactor_eval_neg_one]
  · simp [permDet_eval_neg_one]

lemma natDegree_geomFactor_le (ℓ : ℕ) : (geomFactor ℓ).natDegree ≤ ℓ - 1 := by
  unfold geomFactor
  refine natDegree_sum_le_of_forall_le _ _ fun i hi => ?_
  have hi : i < ℓ := mem_range.mp hi
  calc ((-X : ℤ[X]) ^ i).natDegree ≤ i * (-X : ℤ[X]).natDegree := natDegree_pow_le
    _ ≤ ℓ - 1 := by rw [natDegree_neg, natDegree_X]; omega

lemma natDegree_permDet_le (L : List ℕ) : (permDet L).natDegree ≤ L.sum := by
  induction L with
  | nil => simp
  | cons ℓ rest ih =>
    rw [permDet_cons, List.sum_cons]
    refine natDegree_mul_le.trans (Nat.add_le_add ?_ ih)
    refine (natDegree_sub_le _ _).trans (max_le (by simp) ?_)
    calc ((-X : ℤ[X]) ^ ℓ).natDegree ≤ ℓ * (-X : ℤ[X]).natDegree := natDegree_pow_le
      _ = ℓ := by rw [natDegree_neg, natDegree_X, mul_one]

/-- The quotient has degree `< n = ∑ ℓᵢ` (it has `n` coefficients `χ₀ … χ_{n-1}`). -/
theorem natDegree_stdDet_lt {L : List ℕ} (hL : L ≠ []) (hpos : ∀ ℓ ∈ L, 0 < ℓ) :
    (stdDet L).natDegree < L.sum := by
  cases L with
  | nil => exact absurd rfl hL
  | cons ℓ rest =>
    have hℓ : 0 < ℓ := hpos ℓ List.mem_cons_self
    rw [stdDet_cons, List.sum_cons]
    calc (geomFactor ℓ * permDet rest).natDegree
        ≤ (geomFactor ℓ).natDegree + (permDet rest).natDegree := natDegree_mul_le
      _ ≤ (ℓ - 1) + rest.sum := Nat.add_le_add (natDegree_geomFactor_le ℓ) (natDegree_permDet_le rest)
      _ < ℓ + rest.sum := by omega

/-- **Cycle indicator (note, lines 52-54).** For cycle lengths `ℓ₁, …, ℓ_c ≥ 1`
with `n = ∑ ℓᵢ`, the integer coefficients `χ_j` of
`∏ (1 - (-z)^ℓᵢ) / (1 + z)` satisfy
`∑_{j=0}^{n-1} (-1)^j χ_j = n · [c = 1]`. -/
theorem cycle_indicator {L : List ℕ} (hL : L ≠ []) (hpos : ∀ ℓ ∈ L, 0 < ℓ) :
    ∑ j ∈ range L.sum, (-1 : ℤ) ^ j * (stdDet L).coeff j
      = if L.length = 1 then (L.sum : ℤ) else 0 := by
  rw [← stdDet_eval_neg_one, eval_eq_sum_range' (natDegree_stdDet_lt hL hpos)]
  exact sum_congr rfl fun j _ => mul_comm _ _

/-- The same statement phrased for an arbitrary quotient `Q`, as in the Python
check `numerator == (1 + z) * chars`. -/
theorem cycle_indicator_of_eq {L : List ℕ} (hL : L ≠ []) (hpos : ∀ ℓ ∈ L, 0 < ℓ)
    {Q : ℤ[X]} (hQ : permDet L = (1 + X) * Q) :
    ∑ j ∈ range L.sum, (-1 : ℤ) ^ j * Q.coeff j
      = if L.length = 1 then (L.sum : ℤ) else 0 := by
  rw [stdDet_unique hL hQ]
  exact cycle_indicator hL hpos

/-- `χ₀ = 1` (the trivial exterior power `Λ⁰`). -/
theorem stdDet_coeff_zero {L : List ℕ} (hL : L ≠ []) (hpos : ∀ ℓ ∈ L, 0 < ℓ) :
    (stdDet L).coeff 0 = 1 := by
  cases L with
  | nil => exact absurd rfl hL
  | cons ℓ rest =>
    have hrest : ∀ m ∈ rest, 0 < m := fun m hm => hpos m (List.mem_cons_of_mem _ hm)
    have hperm : (permDet rest).eval 0 = 1 := by
      clear hL hpos
      induction rest with
      | nil => simp
      | cons m rest ih =>
        have hm : m ≠ 0 := (hrest m List.mem_cons_self).ne'
        simp [hm, ih fun k hk => hrest k (List.mem_cons_of_mem _ hk)]
    have hℓ : ℓ ≠ 0 := (hpos ℓ List.mem_cons_self).ne'
    rw [coeff_zero_eq_eval_zero, stdDet_cons, eval_mul, hperm, geomFactor,
      eval_finsetSum]
    obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hℓ
    rw [sum_range_succ']
    simp

/-! ### Multiset / permutation form

`Equiv.Perm.partition σ` is the multiset of all cycle lengths of `σ`, fixed
points included (Mathlib's `cycleType` omits the 1-cycles). -/

noncomputable section

/-- `permDet` on a multiset of cycle lengths. -/
def permDetM (s : Multiset ℕ) : ℤ[X] :=
  (s.map fun ℓ => (1 - (-X) ^ ℓ : ℤ[X])).prod

end

lemma permDetM_coe (L : List ℕ) : permDetM (L : Multiset ℕ) = permDet L := by
  simp [permDetM, permDet]

/-- **Cycle indicator for a permutation.** For `σ ∈ S_n` (`n ≥ 1`), with all
of its cycle lengths (fixed points included), `det(1 + zσ) = ∏ (1 - (-z)^ℓ)`
is divisible by `1 + z`, and every quotient `Q` has
`∑_{j<n} (-1)^j Q_j = n` if `σ` has a single cycle and `0` otherwise. -/
theorem perm_cycle_indicator {n : ℕ} (σ : Equiv.Perm (Fin n)) (hn : 0 < n) :
    (1 + X : ℤ[X]) ∣ permDetM σ.partition.parts ∧
    ∀ Q : ℤ[X], permDetM σ.partition.parts = (1 + X) * Q →
      ∑ j ∈ range n, (-1 : ℤ) ^ j * Q.coeff j
        = if Multiset.card σ.partition.parts = 1 then (n : ℤ) else 0 := by
  obtain ⟨L, hL⟩ := Quot.exists_rep σ.partition.parts
  have hcoe : σ.partition.parts = (L : Multiset ℕ) := hL.symm
  have hsum : L.sum = n := by
    have h := σ.partition.parts_sum
    rw [hcoe, Multiset.sum_coe, Fintype.card_fin] at h
    exact h
  have hpos : ∀ ℓ ∈ L, 0 < ℓ := fun ℓ hℓ =>
    σ.partition.parts_pos (by rw [hcoe]; exact Multiset.mem_coe.mpr hℓ)
  have hne : L ≠ [] := by
    rintro rfl
    simp at hsum
    omega
  rw [hcoe, permDetM_coe, Multiset.coe_card]
  refine ⟨one_add_X_dvd_permDet hne, fun Q hQ => ?_⟩
  have h := cycle_indicator_of_eq hne hpos hQ
  rw [hsum] at h
  exact h

end QSearch
