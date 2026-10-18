import Mathlib.LinearAlgebra.ExteriorPower.Basic
import Mathlib.LinearAlgebra.Basis.Defs
import Mathlib.RepresentationTheory.Invariants
import Mathlib.Algebra.BigOperators.Fin

/-!
# Milestone 3: `Λ^j V_std` has no `S_n`-invariants for `j ≥ 1`

Source: `research/PRIME_CHARACTER_EXTERIOR_BOUND.md`, lines 60-66.

`V = stdSpace K m` is the standard representation of `S_n`, `n = m + 1`, over a
field `K` of characteristic zero: the vectors of `K^n` with coordinate sum `0`,
with `σ` acting by `(σ x)(i) = x(σ⁻¹ i)`. It has the basis
`bᵢ = e_{i} - e_{n}` (`i < n`), as in the note.

The proof follows the note's idea (a transposition acts by `-1` on a basis
wedge) but uses averaging instead of coefficient extraction: the operator
`∑_{σ ∈ S_n} Λ^j(σ)` is zero on `Λ^j V` for `j ≥ 1`, because on each basis
wedge `b_{v₁} ∧ ⋯ ∧ b_{v_j}` (with distinct `vₖ`) some transposition `τ`
satisfies `Λ^j(τ)(w) = -w`:

* `j ≥ 2`: `τ = (v₁ v₂)` swaps two wedge factors;
* `j = 1`: `τ = (v₁ n)` sends `b_{v₁}` to `-b_{v₁}`.

An invariant vector `x` then satisfies `n! • x = 0`, so `x = 0`.
-/

open Module Equiv Finset

namespace QSearch

variable (K : Type*) [Field K] (m : ℕ)

/-- The standard representation space of `S_{m+1}`: sum-zero vectors in `K^{m+1}`. -/
def stdSpace : Submodule K (Fin (m + 1) → K) where
  carrier := {x | ∑ i, x i = 0}
  add_mem' {a b} ha hb := by
    change ∑ i, a i = 0 at ha
    change ∑ i, b i = 0 at hb
    change ∑ i, (a + b) i = 0
    simp only [Pi.add_apply, Finset.sum_add_distrib]
    rw [ha, hb, add_zero]
  zero_mem' := by
    change ∑ i, (0 : Fin (m + 1) → K) i = 0
    simp
  smul_mem' c x hx := by
    change ∑ i, x i = 0 at hx
    change ∑ i, (c • x) i = 0
    simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum]
    rw [hx, mul_zero]

variable {K m}

lemma mem_stdSpace {x : Fin (m + 1) → K} : x ∈ stdSpace K m ↔ ∑ i, x i = 0 := Iff.rfl

variable (K m)

/-- The permutation action `(σ x)(i) = x(σ⁻¹ i)` on `K^{m+1}`. -/
def permAct (σ : Perm (Fin (m + 1))) : (Fin (m + 1) → K) →ₗ[K] (Fin (m + 1) → K) :=
  LinearMap.funLeft K K σ.symm

lemma permAct_mem (σ : Perm (Fin (m + 1))) (x : Fin (m + 1) → K) (hx : x ∈ stdSpace K m) :
    permAct K m σ x ∈ stdSpace K m := by
  rw [mem_stdSpace] at hx ⊢
  simp only [permAct, LinearMap.funLeft_apply]
  rw [Equiv.sum_comp σ.symm x, hx]

/-- The standard representation of `S_{m+1}` on `stdSpace K m`. -/
def stdRep : Representation K (Perm (Fin (m + 1))) (stdSpace K m) where
  toFun σ := (permAct K m σ).restrict (permAct_mem K m σ)
  map_one' := by
    ext x i
    rfl
  map_mul' σ τ := by
    ext x i
    simp [permAct, LinearMap.funLeft_apply, Perm.mul_def]

lemma stdRep_apply_coe (σ : Perm (Fin (m + 1))) (x : stdSpace K m) (i : Fin (m + 1)) :
    (stdRep K m σ x : Fin (m + 1) → K) i = (x : Fin (m + 1) → K) (σ.symm i) := rfl

/-- Coordinates of `stdSpace` in the basis `e_i - e_last`: drop the last coordinate. -/
def stdEquiv : stdSpace K m ≃ₗ[K] (Fin m → K) where
  toFun x := Fin.init (x : Fin (m + 1) → K)
  invFun y := ⟨Fin.snoc y (-∑ i, y i), by
    rw [mem_stdSpace, Fin.sum_univ_castSucc]
    simp⟩
  map_add' x y := rfl
  map_smul' c x := rfl
  left_inv x := by
    apply Subtype.ext
    have hx : ∑ i, (x : Fin (m + 1) → K) i = 0 := x.2
    rw [Fin.sum_univ_castSucc] at hx
    have hlast : -∑ i, Fin.init (x : Fin (m + 1) → K) i = (x : Fin (m + 1) → K) (Fin.last m) :=
      neg_eq_of_add_eq_zero_right hx
    show Fin.snoc (Fin.init (x : Fin (m + 1) → K)) (-∑ i, Fin.init (x : Fin (m + 1) → K) i) =
      (x : Fin (m + 1) → K)
    rw [hlast, Fin.snoc_init_self]
  right_inv y := by
    funext i
    simp [Fin.init]

/-- The basis `bᵢ = e_i - e_last` of the standard representation. -/
noncomputable def stdBasis : Basis (Fin m) K (stdSpace K m) :=
  Basis.ofEquivFun (stdEquiv K m)

lemma stdBasis_coe (i : Fin m) :
    (stdBasis K m i : Fin (m + 1) → K) =
      Pi.single (Fin.castSucc i) 1 - Pi.single (Fin.last m) 1 := by
  rw [stdBasis, Basis.coe_ofEquivFun]
  funext k
  induction k using Fin.lastCases with
  | last =>
    simp [stdEquiv, Pi.single_apply, (Fin.castSucc_lt_last i).ne]
  | cast k =>
    simp [stdEquiv, Pi.single_apply, Fin.castSucc_inj, (Fin.castSucc_lt_last k).ne]

lemma permAct_single (σ : Perm (Fin (m + 1))) (a : Fin (m + 1)) :
    permAct K m σ (Pi.single a 1) = Pi.single (σ a) 1 := by
  funext k
  simp only [permAct, LinearMap.funLeft_apply, Pi.single_apply, Equiv.symm_apply_eq]

/-- `σ (e_i - e_last) = e_{σ i} - e_{σ last}`. -/
lemma stdRep_stdBasis (σ : Perm (Fin (m + 1))) (i : Fin m) :
    (stdRep K m σ (stdBasis K m i) : Fin (m + 1) → K) =
      Pi.single (σ (Fin.castSucc i)) 1 - Pi.single (σ (Fin.last m)) 1 := by
  have h : (stdRep K m σ (stdBasis K m i) : Fin (m + 1) → K) =
      permAct K m σ (stdBasis K m i : Fin (m + 1) → K) := rfl
  rw [h, stdBasis_coe, map_sub, permAct_single, permAct_single]

lemma eq_zero_of_eq_neg [CharZero K] {E : Type*} [AddCommGroup E] [Module K E] {x : E}
    (h : x = -x) : x = 0 := by
  have h2 : (2 : K) • x = 0 := by
    rw [two_smul]
    nth_rw 1 [h]
    exact neg_add_cancel x
  exact (smul_eq_zero.mp h2).resolve_left two_ne_zero

/-- The averaged wedge `∑_σ (σ w₁) ∧ ⋯ ∧ (σ w_j)`. -/
noncomputable def avgWedge (j : ℕ) (w : Fin j → stdSpace K m) : ⋀[K]^j (stdSpace K m) :=
  ∑ σ : Perm (Fin (m + 1)), exteriorPower.ιMulti K j (fun k => stdRep K m σ (w k))

/-- Averaging is invariant under first acting by any `τ`. -/
lemma avgWedge_act (j : ℕ) (w : Fin j → stdSpace K m) (τ : Perm (Fin (m + 1))) :
    avgWedge K m j (fun k => stdRep K m τ (w k)) = avgWedge K m j w := by
  unfold avgWedge
  have h : ∀ σ : Perm (Fin (m + 1)),
      exteriorPower.ιMulti K j (fun k => stdRep K m σ (stdRep K m τ (w k))) =
        exteriorPower.ιMulti K j (fun k => stdRep K m (σ * τ) (w k)) := by
    intro σ
    rw [map_mul]
    rfl
  simp_rw [h]
  exact Fintype.sum_equiv (Equiv.mulRight τ) _ _ (fun σ => rfl)

variable [CharZero K]

/-- The key computation: the averaged wedge of distinct basis vectors vanishes. -/
lemma avgWedge_basis_eq_zero (j : ℕ) (hj : 1 ≤ j) (v : Fin j → Fin m)
    (hv : Function.Injective v) :
    avgWedge K m j (fun k => stdBasis K m (v k)) = 0 := by
  apply eq_zero_of_eq_neg K
  rcases Nat.lt_or_ge j 2 with hj2 | hj2
  · -- `j = 1`: the transposition `(v₀, last)` negates `b_{v₀}`.
    obtain rfl : j = 1 := by omega
    set a := v 0
    set τ := Equiv.swap (Fin.castSucc a) (Fin.last m)
    have hτ : stdRep K m τ (stdBasis K m a) = -stdBasis K m a := by
      apply Subtype.ext
      rw [stdRep_stdBasis]
      simp only [τ, Equiv.swap_apply_left, Equiv.swap_apply_right, Submodule.coe_neg,
        stdBasis_coe, neg_sub]
    have hw : (fun k : Fin 1 => stdRep K m τ (stdBasis K m (v k))) =
        Function.update (fun k : Fin 1 => stdBasis K m (v k)) 0 (-stdBasis K m a) := by
      funext k
      rw [Subsingleton.elim k 0, Function.update_self, hτ]
    conv_lhs => rw [← avgWedge_act K m 1 _ τ]
    unfold avgWedge
    rw [← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun σ _ => ?_
    have e1 : (fun k : Fin 1 => stdRep K m σ (stdRep K m τ (stdBasis K m (v k)))) =
        Function.update (fun k : Fin 1 => stdRep K m σ (stdBasis K m (v k))) 0
          (-stdRep K m σ (stdBasis K m a)) := by
      funext k
      rw [Subsingleton.elim k 0, Function.update_self, hτ, map_neg]
    have e2 : (fun k : Fin 1 => stdRep K m σ (stdBasis K m (v k))) =
        Function.update (fun k : Fin 1 => stdRep K m σ (stdBasis K m (v k))) 0
          (stdRep K m σ (stdBasis K m a)) := by
      funext k
      rw [Subsingleton.elim k 0, Function.update_self]
    rw [e1, AlternatingMap.map_update_neg, ← e2]
  · -- `j ≥ 2`: the transposition `(v₀ v₁)` swaps the first two wedge factors.
    set i0 : Fin j := ⟨0, by omega⟩
    set i1 : Fin j := ⟨1, by omega⟩
    have hi : i0 ≠ i1 := by simp [i0, i1, Fin.ext_iff]
    set τ := Equiv.swap (Fin.castSucc (v i0)) (Fin.castSucc (v i1))
    have hlast : τ (Fin.last m) = Fin.last m :=
      Equiv.swap_apply_of_ne_of_ne (Fin.castSucc_lt_last _).ne' (Fin.castSucc_lt_last _).ne'
    have hτ : ∀ k, stdRep K m τ (stdBasis K m (v k)) = stdBasis K m (v (Equiv.swap i0 i1 k)) := by
      intro k
      apply Subtype.ext
      rw [stdRep_stdBasis, hlast, stdBasis_coe, hv.map_swap,
        Fin.castSucc_injective m |>.map_swap]
    conv_lhs => rw [← avgWedge_act K m j _ τ]
    unfold avgWedge
    rw [← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun σ _ => ?_
    simp_rw [hτ]
    exact (exteriorPower.ιMulti K j).map_swap
      (fun k => stdRep K m σ (stdBasis K m (v k))) hi

/-- **`∑_{σ ∈ S_n} Λ^j(σ) = 0` on `Λ^j V_std` for `j ≥ 1`.** -/
theorem sum_map_stdRep_eq_zero (j : ℕ) (hj : 1 ≤ j) :
    ∑ σ : Perm (Fin (m + 1)), exteriorPower.map j (stdRep K m σ) = 0 := by
  apply exteriorPower.linearMap_ext
  apply (stdBasis K m).ext_alternating
  intro v hv
  have h := avgWedge_basis_eq_zero K m j hj v hv
  simp only [avgWedge] at h
  simp [LinearMap.sum_apply, exteriorPower.map_apply_ιMulti, Function.comp_def, h]

/-- **No nontrivial exterior power of `V_std` has `S_n`-invariants (note, line 60).**
For `j ≥ 1`, a vector of `Λ^j V_std` fixed by every `σ ∈ S_n` is zero. -/
theorem exterior_std_no_invariants (j : ℕ) (hj : 1 ≤ j) (x : ⋀[K]^j (stdSpace K m))
    (hx : ∀ σ : Perm (Fin (m + 1)), exteriorPower.map j (stdRep K m σ) x = x) : x = 0 := by
  have h := congrArg (fun f => f x) (sum_map_stdRep_eq_zero K m j hj)
  simp only [LinearMap.sum_apply, hx, LinearMap.zero_apply, Finset.sum_const,
    Finset.card_univ] at h
  rw [← Nat.cast_smul_eq_nsmul K] at h
  exact (smul_eq_zero.mp h).resolve_left (Nat.cast_ne_zero.mpr Fintype.card_ne_zero)

/-- `Λ^j V_std` as a representation of `S_n`. -/
noncomputable def extStdRep (j : ℕ) :
    Representation K (Perm (Fin (m + 1))) (⋀[K]^j (stdSpace K m)) where
  toFun σ := exteriorPower.map j (stdRep K m σ)
  map_one' := by
    rw [map_one]
    exact exteriorPower.map_id
  map_mul' σ τ := by
    rw [map_mul]
    exact exteriorPower.map_comp _ _

/-- The same statement in Mathlib's language: the invariant subspace is `⊥`. -/
theorem extStdRep_invariants_eq_bot (j : ℕ) (hj : 1 ≤ j) :
    Representation.invariants (extStdRep K m j) = ⊥ := by
  rw [eq_bot_iff]
  intro x hx
  rw [Submodule.mem_bot]
  exact exterior_std_no_invariants K m j hj x hx

end QSearch
