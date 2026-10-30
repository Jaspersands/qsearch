import Mathlib.LinearAlgebra.Vandermonde
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Analysis.Complex.Basic
import Mathlib.Algebra.Group.Subgroup.Basic

/-!
Isolated checked successor to the previously uncompiled repository draft.
Reproduce with verify.py on Lean/mathlib v4.35.0. Audit.lean prints the
axioms of every theorem; the receipt records the precise checked scope.
The main repository draft and its default build have not been changed.

Exact coefficientwise hiding from nonzero-point interpolation, and the
central-source coefficient with a nontrivial hidden central intersection.
A concrete Lie realization is checked separately in ReesLie. The BCH
group construction and whole quantum algorithm remain outside this check;
they are not inferred from these interface theorems.
-/

namespace QSearch.ReesHomogenization
open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

section Interpolation
variable {F V : Type*} [Field F] [AddCommGroup V] [Module F V] {n : ℕ}

def applyRows (M : Matrix (Fin n) (Fin n) F) (v : Fin n → V) (i : Fin n) : V :=
  ∑ j, M i j • v j

theorem applyRows_mul (A B : Matrix (Fin n) (Fin n) F) (v : Fin n → V) :
    applyRows (A * B) v = applyRows A (applyRows B v) := by
  funext i
  simp only [applyRows, Matrix.mul_apply, Finset.sum_smul, Finset.smul_sum, mul_smul]
  exact Finset.sum_comm

theorem applyRows_one (v : Fin n → V) : applyRows (1 : Matrix _ _ F) v = v := by
  ext i
  simp [applyRows, Matrix.one_apply]

def evaluationMatrix (points : Fin n → F) : Matrix (Fin n) (Fin n) F :=
  Matrix.diagonal points * Matrix.vandermonde points

theorem evaluationMatrix_apply (points : Fin n → F) (i j : Fin n) :
    evaluationMatrix points i j = points i ^ (j.val + 1) := by
  simp [evaluationMatrix, Matrix.diagonal_mul, Matrix.vandermonde_apply, pow_succ']

theorem evaluation_det_ne_zero (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0) :
    (evaluationMatrix points).det ≠ 0 := by
  rw [evaluationMatrix, Matrix.det_mul, Matrix.det_diagonal]
  exact mul_ne_zero (Finset.prod_ne_zero_iff.mpr fun i _ => nonzero i)
    (Matrix.det_vandermonde_ne_zero_iff.mpr distinct)

theorem rows_mem (h : Submodule F V) (M : Matrix (Fin n) (Fin n) F)
    (v : Fin n → V) (hv : ∀ j, v j ∈ h) (i : Fin n) : applyRows M v i ∈ h := by
  exact h.sum_mem fun j _ => h.smul_mem _ (hv j)

/-- No constant term: exactly n distinct NONZERO points determine n
coefficients modulo any linear subspace, even a nonhomogeneous one. -/
theorem coefficientwise_iff (h : Submodule F V) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (v : Fin n → V) :
    (∀ i, applyRows (evaluationMatrix points) v i ∈ h) ↔ ∀ j, v j ∈ h := by
  constructor
  · intro hv
    have hi : (evaluationMatrix points)⁻¹ * evaluationMatrix points = 1 :=
      Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr (evaluation_det_ne_zero points distinct nonzero))
    have he : applyRows (evaluationMatrix points)⁻¹ (applyRows (evaluationMatrix points) v) = v := by
      rw [← applyRows_mul, hi, applyRows_one]
    intro j
    rw [← he]
    exact rows_mem h _ _ hv j
  · exact fun hv i => rows_mem h _ _ hv i

/-- Coefficientwise hidden membership is invariant under every NONZERO
graded dilation. No grading of the original hidden subspace is assumed. -/
theorem dilation_membership_iff (h : Submodule F V) (s : F) (nonzero : s ≠ 0)
    (v : Fin n → V) :
    (∀ j, s ^ (j.val + 1) • v j ∈ h) ↔ ∀ j, v j ∈ h := by
  constructor
  · intro hv j
    have hx := h.smul_mem ((s ^ (j.val + 1))⁻¹) (hv j)
    simpa [smul_smul, inv_mul_cancel₀ (pow_ne_zero _ nonzero)] using hx
  · intro hv j
    exact h.smul_mem _ (hv j)

/-- A zero scale destroys support and cannot be treated as an automorphism. -/
theorem zero_dilation_erases (v : Fin n → V) (j : Fin n) :
    (0 : F) ^ (j.val + 1) • v j = 0 := by
  simp

variable {G K O : Type*} [Group G] [Group K]

/-- The operational oracle is the ordered tuple of original evaluations.
Evaluation homomorphisms and their coefficient identity must be supplied
by the concrete Rees construction, not by hidden advice. -/
theorem tuple_hides (h : Submodule F V) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (e : Fin n → G →* K) (log : K → V) (coeff : G → Fin n → V)
    (evaluation : ∀ g i, log (e i g) = applyRows (evaluationMatrix points) (coeff g) i)
    (f : K → O) (hides : ∀ x y, f x = f y ↔ log (x⁻¹ * y) ∈ h)
    (a b : G) :
    (fun i => f (e i a)) = (fun i => f (e i b)) ↔ ∀ j, coeff (a⁻¹ * b) j ∈ h := by
  rw [funext_iff, ← coefficientwise_iff h points distinct nonzero]
  apply forall_congr'
  intro i
  rw [hides, ← map_inv, ← map_mul, evaluation]
end Interpolation

section CentralIntersection
variable {G C : Type*} [Group G] [CommGroup C] [Fintype C]

/-- Same finite coefficient as CentralCharacterDescent.coefficient.
Kept independent of that module's operator stack for this algebraic lemma. -/
def coefficient (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ) (g : G) : ℂ :=
  ∑ z, if g * (embed z)⁻¹ ∈ H then chi z else 0

/-- General source coefficient; no transversality or centrality assumption
is needed for this finite-sum identity. Centrality is needed by the
separate spectral-projector/channel interpretation. -/
theorem coefficient_translate (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (h : G) (hh : h ∈ H) (z : C) :
    coefficient H embed chi (h * embed z) =
      (∑ w : C, if embed w ∈ H then chi w else 0) * chi z := by
  unfold coefficient
  rw [Finset.sum_mul]
  symm
  apply Fintype.sum_equiv (Equiv.mulRight z)
  intro w
  have he : h * embed z * (embed (w * z))⁻¹ = h * (embed w)⁻¹ := by
    simp [map_mul, mul_inv_rev, mul_assoc]
  change (if embed w ∈ H then chi w else 0) * chi z =
    if h * embed z * (embed (w * z))⁻¹ ∈ H then chi (w * z) else 0
  rw [he, H.mul_mem_cancel_left hh, H.inv_mem_iff]
  split_ifs <;> simp [map_mul]

theorem coefficient_allowed (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ w, embed w ∈ H → chi w = 1)
    (h : G) (hh : h ∈ H) (z : C) :
    coefficient H embed chi (h * embed z) =
      (Fintype.card {w : C // embed w ∈ H} : ℂ) * chi z := by
  rw [coefficient_translate H embed chi h hh z]
  congr 1
  simp only [show (fun w : C => if embed w ∈ H then chi w else 0) =
      (fun w : C => if embed w ∈ H then (1 : ℂ) else 0) by
    funext w; split_ifs with hw; exact allowed w hw; rfl]
  simp [Fintype.card_subtype]

/-- Every hidden/embedded intersection contains the identity. The
multiplicity in the allowed branch therefore cannot vanish. -/
theorem intersection_card_pos (H : Subgroup G) (embed : C →* G) :
    0 < Fintype.card {w : C // embed w ∈ H} := by
  apply Fintype.card_pos_iff.mpr
  exact ⟨⟨1, by simp⟩⟩

/-- Off H * range(embed), all coefficients are exactly zero. -/
theorem coefficient_outside (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (g : G) (outside : ∀ z, g * (embed z)⁻¹ ∉ H) :
    coefficient H embed chi g = 0 := by
  simp [coefficient, outside]

/-- A character nontrivial on the hidden intersection contributes the
zero operator, not an allowed branch which may be normalized. -/
theorem coefficient_forbidden (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (w : C) (hw : embed w ∈ H) (forbidden : chi w ≠ 1) (g : G) :
    coefficient H embed chi g = 0 := by
  let S : ℂ := ∑ z : C, if embed z ∈ H then chi z else 0
  have hmem : coefficient H embed chi (embed w) = S := by
    simpa [S] using coefficient_translate H embed chi (embed w) hw (1 : C)
  have hshift : coefficient H embed chi (embed w) = S * chi w := by
    simpa [S] using coefficient_translate H embed chi 1 H.one_mem w
  have hz : S * (chi w - 1) = 0 := by
    rw [mul_sub, mul_one, ← hshift, hmem, sub_self]
  have hS : S = 0 := (mul_eq_zero.mp hz).resolve_right (sub_ne_zero.mpr forbidden)
  by_cases represented : ∃ z : C, g * (embed z)⁻¹ ∈ H
  · obtain ⟨z, hz⟩ := represented
    have he : g = (g * (embed z)⁻¹) * embed z := by simp [mul_assoc]
    calc
      coefficient H embed chi g = coefficient H embed chi ((g * (embed z)⁻¹) * embed z) :=
        congrArg (coefficient H embed chi) he
      _ = S * chi z := coefficient_translate H embed chi _ hz z
      _ = 0 := by rw [hS, zero_mul]
  · apply coefficient_outside H embed chi g
    intro z hz
    exact represented ⟨z, hz⟩
end CentralIntersection

section Countercontrols
variable {F : Type*} [Field F]

/-- Distinctness alone is insufficient if an evaluation point is zero. -/
theorem zero_evaluation_loses_coefficient :
    ∃ (points : Fin 1 → F) (v : Fin 1 → F),
      (∀ i, applyRows (evaluationMatrix points) v i = 0) ∧ v 0 ≠ 0 := by
  refine ⟨fun _ => 0, fun _ => 1, ?_, one_ne_zero⟩
  intro i
  simp [applyRows, evaluationMatrix_apply]

/-- Nonzero but repeated points do not determine the coefficients. -/
theorem repeated_evaluation_loses_coefficient :
    ∃ (points : Fin 2 → F) (v : Fin 2 → F),
      (∀ i, applyRows (evaluationMatrix points) v i = 0) ∧ v 0 ≠ 0 := by
  refine ⟨fun _ => 1, ![1, -1], ?_, one_ne_zero⟩
  intro i
  simp [applyRows, evaluationMatrix_apply, Fin.sum_univ_two]
end Countercontrols

end
end QSearch.ReesHomogenization
