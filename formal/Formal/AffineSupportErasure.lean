import Mathlib.Algebra.Module.Submodule.Basic
import Mathlib.Algebra.BigOperators.GroupWithZero.Finset
import Mathlib.Algebra.Star.BigOperators
import Mathlib.Basic.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Fintype.Pi
import Mathlib.Tactic

/-!
# Mixed affine-support erasure

The entrywise Kraus identity for independent kernels with one common unknown
linear support. Phases are arbitrary complex functions; polynomial structure
is not assumed or evaluated by the channel. Unit-modulus hypotheses are needed
only for normalization.

This does not formalize the group-to-kernel source conversion, the diagonal
solver, complexity, the full HSP algorithm, or novelty.
-/

namespace QSearch.AffineSupportErasure

open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F V I : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Fintype V] [Fintype I]

def invSize (V : Type*) [Fintype V] : ℂ := (Fintype.card V : ℂ)⁻¹

def uniformAmplitude (V : Type*) [Fintype V] : ℂ :=
  ((Real.sqrt (Fintype.card V : ℝ))⁻¹ : ℝ)

def affinePoint (c : I → F) (y : I → V) (x : V) : I → V :=
  fun i => y i + c i • x

def rho (U : Submodule F V) (phase : V → ℂ) (x x' : V) : ℂ := by
  classical
  exact if x - x' ∈ U then invSize V * phase x * star (phase x') else 0

def tensorRho (U : Submodule F V) (phase : I → V → ℂ)
    (a b : I → V) : ℂ :=
  ∏ i, rho U (phase i) (a i) (b i)

def combinedPhase (phase : I → V → ℂ) (c : I → F) (y : I → V)
    (x : V) : ℂ :=
  ∏ i, phase i (affinePoint c y x i)

def krausEntry (amplitude : ℂ) (c : I → F) (y : I → V)
    (x : V) (a : I → V) : ℂ := by
  classical
  exact if a = affinePoint c y x then amplitude else 0

def branchEntry (amplitude : ℂ) (U : Submodule F V)
    (phase : I → V → ℂ) (c : I → F) (y : I → V) (x x' : V) : ℂ :=
  ∑ a, ∑ b, krausEntry amplitude c y x a * tensorRho U phase a b
    * star (krausEntry amplitude c y x' b)

omit [Fintype V] [Fintype I] in
theorem support_iff (U : Submodule F V) (c : I → F) (y : I → V)
    (hc : ∃ i, c i ≠ 0) (x x' : V) :
    (∀ i, affinePoint c y x i - affinePoint c y x' i ∈ U) ↔ x - x' ∈ U := by
  have difference (i : I) :
      affinePoint c y x i - affinePoint c y x' i = c i • (x - x') := by
    simp only [affinePoint, smul_sub]
    abel
  constructor
  · intro h
    obtain ⟨i, hi⟩ := hc
    exact (U.smul_mem_iff hi).mp (by simpa only [difference] using h i)
  · intro h i
    rw [difference]
    exact U.smul_mem (c i) h

theorem tensor_pullback (U : Submodule F V) (phase : I → V → ℂ)
    (c : I → F) (y : I → V) (hc : ∃ i, c i ≠ 0) (x x' : V) :
    tensorRho U phase (affinePoint c y x) (affinePoint c y x') =
      if x - x' ∈ U then
        invSize V ^ Fintype.card I * combinedPhase phase c y x
          * star (combinedPhase phase c y x')
      else 0 := by
  classical
  simp only [tensorRho, rho, Fintype.prod_ite_zero]
  simp only [support_iff U c y hc x x']
  simp [combinedPhase, Finset.prod_mul_distrib]

omit [Fintype V] in
theorem star_kraus (amplitude : ℂ) (c : I → F) (y : I → V)
    (x : V) (a : I → V) :
    star (krausEntry amplitude c y x a) =
      if a = affinePoint c y x then star amplitude else 0 := by
  classical
  by_cases h : a = affinePoint c y x <;> simp [krausEntry, h]

theorem branch_pullback (amplitude : ℂ) (U : Submodule F V)
    (phase : I → V → ℂ) (c : I → F) (y : I → V) (x x' : V) :
    branchEntry amplitude U phase c y x x' =
      (amplitude * star amplitude)
        * tensorRho U phase (affinePoint c y x) (affinePoint c y x') := by
  classical
  simp only [branchEntry, star_kraus]
  simp [krausEntry, ite_mul, mul_ite]
  ring

omit [AddCommGroup V] in
theorem uniformAmplitude_normalized :
    uniformAmplitude V * star (uniformAmplitude V) = invSize V := by
  simp only [uniformAmplitude, Complex.star_def, Complex.conj_ofReal, invSize]
  norm_cast
  rw [← pow_two, inv_pow, Real.sq_sqrt (Nat.cast_nonneg _)]
  simp

/-- The identity is derived from the two Kraus sums, not assumed as a channel
formula. It holds for every outcome and arbitrary phases. -/
theorem mixed_branch_identity (U : Submodule F V) (phase : I → V → ℂ)
    (c : I → F) (y : I → V) (hc : ∃ i, c i ≠ 0) (x x' : V) :
    branchEntry (uniformAmplitude V) U phase c y x x' =
      invSize V ^ Fintype.card I * rho U (combinedPhase phase c y) x x' := by
  classical
  rw [branch_pullback, uniformAmplitude_normalized, tensor_pullback U phase c y hc]
  by_cases h : x - x' ∈ U
  · simp only [rho, h, ite_true]
    ring
  · simp [rho, h]

omit [Fintype V] in
theorem combinedPhase_unit (phase : I → V → ℂ)
    (hphase : ∀ i x, phase i x * star (phase i x) = 1)
    (c : I → F) (y : I → V) (x : V) :
    combinedPhase phase c y x * star (combinedPhase phase c y x) = 1 := by
  simp only [combinedPhase, star_prod, ← Finset.prod_mul_distrib]
  simp only [hphase, Finset.prod_const_one]

theorem rho_trace_one (U : Submodule F V) (phase : V → ℂ)
    (hphase : ∀ x, phase x * star (phase x) = 1) :
    (∑ x, rho U phase x x) = 1 := by
  classical
  have hcard : (Fintype.card V : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  simp only [rho, sub_self, U.zero_mem, ite_true, mul_assoc, hphase, mul_one,
    Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  simp [invSize, hcard]

/-- Every retained measurement outcome has the same probability, D^(-|I|).
The product-input promise is in tensorRho, not an independence conclusion. -/
theorem branch_probability (U : Submodule F V) (phase : I → V → ℂ)
    (hphase : ∀ i x, phase i x * star (phase i x) = 1)
    (c : I → F) (y : I → V) (hc : ∃ i, c i ≠ 0) :
    (∑ x, branchEntry (uniformAmplitude V) U phase c y x x) =
      invSize V ^ Fintype.card I := by
  simp_rw [mixed_branch_identity U phase c y hc]
  rw [← Finset.mul_sum, rho_trace_one U _ (combinedPhase_unit phase hphase c y)]
  simp

omit [Fintype V] [Fintype I] in
theorem affine_eq_iff (c : I → F) (y a : I → V) (x : V) :
    a = affinePoint c y x ↔ y = fun i => a i - c i • x := by
  constructor
  · intro h
    funext i
    exact (eq_sub_iff_add_eq).mpr (congrFun h i).symm
  · intro h
    rw [h]
    funext i
    simp [affinePoint]

/-- The Kraus family is complete for every choice of scales, independently of
the source kernels and even when every scale is zero. -/
theorem kraus_complete (c : I → F) (a b : I → V) :
    (∑ y, ∑ x, star (krausEntry (uniformAmplitude V) c y x a)
      * krausEntry (uniformAmplitude V) c y x b) = if a = b then 1 else 0 := by
  classical
  rw [Finset.sum_comm]
  have fixed (x : V) :
      (∑ y, star (krausEntry (uniformAmplitude V) c y x a)
        * krausEntry (uniformAmplitude V) c y x b) =
        if a = b then invSize V else 0 := by
    simp only [star_kraus]
    simp only [krausEntry, affine_eq_iff]
    by_cases h : a = b
    · subst b
      simp only [ite_mul, mul_ite, zero_mul, mul_zero]
      simpa [mul_comm] using uniformAmplitude_normalized (V := V)
    · have hshift : (fun i => a i - c i • x) ≠ (fun i => b i - c i • x) := by
        intro heq
        apply h
        funext i
        have hi := congrArg (fun z : V => z + c i • x) (congrFun heq i)
        simpa only [sub_add_cancel] using hi
      simp_all [ite_mul, mul_ite]
      intro heq
      exact (hshift heq.symm).elim
  simp_rw [fixed]
  have hcard : (Fintype.card V : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  by_cases h : a = b <;> simp [h, invSize, hcard]

/-- With no active scale, the channel produces full-support uniform
coherence, not the original hidden support. The nonzero-scale guard is real. -/
theorem all_zero_scale_branch (U : Submodule F V) (phase : I → V → ℂ)
    (hphase : ∀ i x, phase i x * star (phase i x) = 1)
    (y : I → V) (x x' : V) :
    branchEntry (uniformAmplitude V) U phase (fun _ => 0) y x x' =
      invSize V ^ Fintype.card I * invSize V := by
  rw [branch_pullback, uniformAmplitude_normalized]
  simp only [tensorRho, rho, affinePoint, zero_smul, add_zero, sub_self,
    U.zero_mem, ite_true, mul_assoc, hphase, mul_one]
  simp [mul_comm]

/-- info: 'QSearch.AffineSupportErasure.mixed_branch_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.AffineSupportErasure.mixed_branch_identity

/-- info: 'QSearch.AffineSupportErasure.branch_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.AffineSupportErasure.branch_probability

/-- info: 'QSearch.AffineSupportErasure.kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.AffineSupportErasure.kraus_complete

/-- info: 'QSearch.AffineSupportErasure.all_zero_scale_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.AffineSupportErasure.all_zero_scale_branch

end
end QSearch.AffineSupportErasure
