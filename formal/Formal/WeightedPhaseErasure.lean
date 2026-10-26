import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Algebra.Group.AddChar
import Mathlib.RingTheory.MvPolynomial.Basic
import Mathlib.RingTheory.MvPolynomial.WeightedHomogeneous
import Mathlib.Tactic

/-!
# Coefficientwise weighted phase erasure

The coefficient ring may itself be a polynomial ring in unknown parameters.
No evaluation at hidden coefficients or physical-source independence is
assumed or inferred. The public triangular substitution and the verified
diagonal relation are distinct hypotheses.
-/

namespace QSearch.WeightedPhaseErasure

open MvPolynomial Finsupp
open scoped BigOperators Pointwise
noncomputable section
attribute [local instance] Classical.propDecidable

variable {R σ : Type*} [CommRing R]

def bounded (w : σ → ℕ) (d : ℕ) : Submodule R (MvPolynomial σ R) :=
  restrictSupport R {a | weight w a ≤ d}

def lower (w : σ → ℕ) (d : ℕ) : Submodule R (MvPolynomial σ R) :=
  restrictSupport R {a | weight w a < d}

theorem mem_bounded (w : σ → ℕ) (d : ℕ) (P : MvPolynomial σ R) :
    P ∈ bounded w d ↔ ∀ a ∈ P.support, weight w a ≤ d := Iff.rfl

theorem mem_lower (w : σ → ℕ) (d : ℕ) (P : MvPolynomial σ R) :
    P ∈ lower w d ↔ ∀ a ∈ P.support, weight w a < d := Iff.rfl

theorem lower_le_bounded (w : σ → ℕ) (d : ℕ) :
    (lower w d : Submodule R (MvPolynomial σ R)) ≤ bounded w d :=
  fun _ h a ha => (show weight w a < d from h ha).le

theorem lower_mono (w : σ → ℕ) {d e : ℕ} (h : d ≤ e) :
    (lower w d : Submodule R (MvPolynomial σ R)) ≤ lower w e :=
  fun _ hP _a ha => (hP ha).trans_le h

theorem bounded_mono (w : σ → ℕ) {d e : ℕ} (h : d ≤ e) :
    (bounded w d : Submodule R (MvPolynomial σ R)) ≤ bounded w e :=
  fun _ hP _a ha => (hP ha).trans h

theorem C_bounded (w : σ → ℕ) (r : R) : C r ∈ bounded w 0 := by
  change monomial 0 r ∈ restrictSupport R {a | weight w a ≤ 0}
  exact (monomial_mem_restrictSupport (s := {a | weight w a ≤ 0}) (m := 0) (r := r)).mpr
    (Or.inl (by simp))

theorem X_bounded (w : σ → ℕ) (i : σ) : (X i : MvPolynomial σ R) ∈ bounded w (w i) := by
  rw [bounded, X, monomial_mem_restrictSupport]
  left
  simp [weight_apply]

theorem bounded_mul (w : σ → ℕ) {d e : ℕ} {P Q : MvPolynomial σ R}
    (hP : P ∈ bounded w d) (hQ : Q ∈ bounded w e) : P*Q ∈ bounded w (d+e) := by
  classical
  intro a ha
  obtain ⟨b, hb, c, hc, rfl⟩ := Finset.mem_add.mp (support_mul P Q ha)
  simpa using add_le_add (hP hb) (hQ hc)

theorem lower_mul (w : σ → ℕ) {d e : ℕ} {P Q : MvPolynomial σ R}
    (hP : P ∈ lower w d) (hQ : Q ∈ bounded w e) : P*Q ∈ lower w (d+e) := by
  classical
  intro a ha
  obtain ⟨b, hb, c, hc, rfl⟩ := Finset.mem_add.mp (support_mul P Q ha)
  simpa using add_lt_add_of_lt_of_le (hP hb) (hQ hc)

/-- Agreement modulo strictly smaller weight, with both degree bounds. -/
def Agree (w : σ → ℕ) (d : ℕ) (P Q : MvPolynomial σ R) : Prop :=
  P ∈ bounded w d ∧ Q ∈ bounded w d ∧ P-Q ∈ lower w d

theorem agree_mul (w : σ → ℕ) {d e : ℕ} {P Q U V : MvPolynomial σ R}
    (h : Agree w d P Q) (k : Agree w e U V) : Agree w (d+e) (P*U) (Q*V) := by
  refine ⟨bounded_mul w h.1 k.1, bounded_mul w h.2.1 k.2.1, ?_⟩
  rw [show P*U-Q*V = (P-Q)*U + (U-V)*Q by ring]
  apply (lower w (d+e)).add_mem (lower_mul w h.2.2 k.1)
  simpa [add_comm] using lower_mul w k.2.2 h.2.1

theorem agree_C (w : σ → ℕ) (r : R) : Agree w 0 (C r) (C r) := by
  exact ⟨C_bounded w r, C_bounded w r, by simp⟩

theorem agree_pow (w : σ → ℕ) {d : ℕ} {P Q : MvPolynomial σ R}
    (h : Agree w d P Q) (n : ℕ) : Agree w (n*d) (P^n) (Q^n) := by
  induction n with
  | zero => simpa using agree_C w (1 : R)
  | succ n ih => simpa [pow_succ, Nat.succ_mul] using agree_mul w ih h

theorem agree_prod {ι : Type*} (w : σ → ℕ) (s : Finset ι) (d : ι → ℕ)
    (P Q : ι → MvPolynomial σ R) (h : ∀ i ∈ s, Agree w (d i) (P i) (Q i)) :
    Agree w (∑ i ∈ s, d i) (∏ i ∈ s, P i) (∏ i ∈ s, Q i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using agree_C w (1 : R)
  | @insert i s hi ih =>
    simpa [hi] using agree_mul w (h i (Finset.mem_insert_self _ _))
      (ih (fun j hj => h j (Finset.mem_insert_of_mem hj)))

def diagonal (w : σ → ℕ) (s : R) : MvPolynomial σ R →ₐ[R] MvPolynomial σ R :=
  bind₁ fun i => C (s^(w i)) * X i

theorem generator_agree (w : σ → ℕ) (s : R) (f : σ → MvPolynomial σ R)
    (hf : ∀ i, f i - C (s^(w i))*X i ∈ lower w (w i)) (i : σ) :
    Agree w (w i) (f i) (C (s^(w i))*X i) := by
  have hg : C (s^(w i))*X i ∈ bounded w (w i) := by
    simpa using bounded_mul w (C_bounded w (s^(w i))) (X_bounded w i)
  refine ⟨?_, hg, hf i⟩
  have h := (bounded w (w i)).add_mem (lower_le_bounded w _ (hf i)) hg
  simpa using h

theorem monomial_agree (w : σ → ℕ) (s : R) (f : σ → MvPolynomial σ R)
    (hf : ∀ i, f i - C (s^(w i))*X i ∈ lower w (w i))
    (a : σ →₀ ℕ) (r : R) :
    Agree w (weight w a) (bind₁ f (monomial a r)) (diagonal w s (monomial a r)) := by
  classical
  simp only [diagonal, bind₁_monomial]
  have hp := agree_prod w a.support (fun i => a i*w i)
    (fun i => f i ^ a i) (fun i => (C (s^(w i))*X i)^a i)
    (fun i _ => agree_pow w (generator_agree w s f hf i) (a i))
  simpa [weight_apply, Finsupp.sum, smul_eq_mul] using agree_mul w (agree_C w r) hp

theorem pullback_agree (w : σ → ℕ) (s : R) (f : σ → MvPolynomial σ R)
    (hf : ∀ i, f i - C (s^(w i))*X i ∈ lower w (w i))
    (d : ℕ) (P : MvPolynomial σ R) (hP : P ∈ bounded w d) :
    Agree w d (bind₁ f P) (diagonal w s P) := by
  classical
  have hmono (a) (ha : a ∈ P.support) := monomial_agree w s f hf a (P.coeff a)
  constructor
  · rw [P.as_sum, map_sum]
    exact (bounded w d).sum_mem (fun a ha => bounded_mono w (hP ha) (hmono a ha).1)
  constructor
  · rw [P.as_sum, map_sum]
    exact (bounded w d).sum_mem (fun a ha => bounded_mono w (hP ha) (hmono a ha).2.1)
  · rw [P.as_sum, map_sum, map_sum, ← Finset.sum_sub_distrib]
    exact (lower w d).sum_mem (fun a ha => lower_mono w (hP ha) (hmono a ha).2.2)

theorem diagonal_monomial (w : σ → ℕ) (s : R) (a : σ →₀ ℕ) (r : R) :
    diagonal w s (monomial a r) = monomial a (r*s^(weight w a)) := by
  classical
  simp only [diagonal, bind₁_monomial, mul_pow, ← map_pow, Finset.prod_mul_distrib, ← map_prod]
  have hp : (∏ i ∈ a.support, (s^(w i))^(a i)) = s^(weight w a) := by
    simp [← pow_mul, Finset.prod_pow_eq_pow_sum, weight_apply, Finsupp.sum, smul_eq_mul, mul_comm]
  rw [hp, ← mul_assoc, ← map_mul, monomial_eq]
  rfl

theorem coeff_diagonal (w : σ → ℕ) (s : R) (P : MvPolynomial σ R) (a : σ →₀ ℕ) :
    (diagonal w s P).coeff a = s^(weight w a)*P.coeff a := by
  classical
  induction P using MvPolynomial.induction_on' with
  | add P Q hP hQ => simp [hP, hQ, mul_add]
  | monomial b r =>
    rw [diagonal_monomial]
    by_cases h : b = a
    · subst b
      simp [coeff_monomial, mul_comm]
    · simp [coeff_monomial, h]

theorem lower_coeff_zero (w : σ → ℕ) {d : ℕ} {P : MvPolynomial σ R}
    (hP : P ∈ lower w d) (a : σ →₀ ℕ) (ha : d ≤ weight w a) : P.coeff a = 0 := by
  by_contra h
  exact (not_lt_of_ge ha) (hP (MvPolynomial.mem_support_iff.mpr h))

theorem leading_coefficient (w : σ → ℕ) (s : R) (f : σ → MvPolynomial σ R)
    (hf : ∀ i, f i - C (s^(w i))*X i ∈ lower w (w i))
    (d : ℕ) (P : MvPolynomial σ R) (hP : P ∈ bounded w d)
    (a : σ →₀ ℕ) (ha : weight w a = d) :
    (bind₁ f P).coeff a = s^d*P.coeff a := by
  have hz := lower_coeff_zero w (pullback_agree w s f hf d P hP).2.2 a ha.ge
  simp only [AddMonoidAlgebra.coeff_sub, Finsupp.sub_apply, sub_eq_zero] at hz
  rw [hz, coeff_diagonal, ha]

/-- Each formal lift coordinate may be a parameter, a product of parameters,
or a constant. Public column cancellation works for ALL their values. -/
theorem parameter_relation {I K : Type*} [Fintype I] [Fintype K]
    (s : I → R) (d : ℕ) (c : I → K → R) (theta : K → R)
    (hc : ∀ k, ∑ i, (s i)^d * c i k = 0) :
    ∑ i, (s i)^d * (∑ k, c i k * theta k) = 0 := by
  simp_rw [Finset.mul_sum, ← mul_assoc]
  rw [Finset.sum_comm]
  simp_rw [← Finset.sum_mul, hc, zero_mul]
  simp

/-- The relation is coefficientwise in R, which may contain formal unknown
parameters. It is not enough for it to vanish at one sampled parameter. -/
theorem diagonal_cancellation {I : Type*} [Fintype I]
    (w : σ → ℕ) (s : I → R) (f : I → σ → MvPolynomial σ R)
    (hf : ∀ i j, f i j - C ((s i)^(w j))*X j ∈ lower w (w j))
    (d : ℕ) (P : I → MvPolynomial σ R) (hP : ∀ i, P i ∈ bounded w d)
    (hrelation : ∀ a : σ →₀ ℕ, weight w a = d →
      ∑ i, (s i)^d * (P i).coeff a = 0) :
    (∑ i, bind₁ (f i) (P i)) ∈ lower w d := by
  classical
  have hb : (∑ i, bind₁ (f i) (P i)) ∈ bounded w d :=
    (bounded w d).sum_mem (fun i _ => (pullback_agree w (s i) (f i) (hf i) d (P i) (hP i)).1)
  intro a ha
  have hle : weight w a ≤ d := hb ha
  change weight w a < d
  apply lt_of_le_of_ne hle
  intro heq
  have hz : (∑ i, bind₁ (f i) (P i)).coeff a = 0 := by
    rw [AddMonoidAlgebra.coeff_sum, Finsupp.finsetSum_apply]
    simp_rw [leading_coefficient w _ _ (hf _) d _ (hP _) a heq]
    exact hrelation a heq
  exact (MvPolynomial.mem_support_iff.mp ha) hz

section Triangular
variable [Fintype σ]

/-- Every affine map with the required diagonal and strictly lower-weight
off-diagonal entries has this form. Coefficients and offsets are public. -/
def triangular (w : σ → ℕ) (s : R) (b : σ → R) (M : σ → σ → R) (i : σ) :
    MvPolynomial σ R :=
  C (s^(w i))*X i + C (b i) + ∑ j ∈ Finset.univ.filter (fun j => w j < w i), C (M i j)*X j

theorem triangular_lower (w : σ → ℕ) (hw : ∀ i, 0 < w i)
    (s : R) (b : σ → R) (M : σ → σ → R) (i : σ) :
    triangular w s b M i - C (s^(w i))*X i ∈ lower w (w i) := by
  have move : triangular w s b M i - C (s^(w i))*X i =
      C (b i) + ∑ j ∈ Finset.univ.filter (fun j => w j < w i), C (M i j)*X j := by
    unfold triangular
    ring
  rw [move]
  apply (lower w (w i)).add_mem
  · intro a ha
    exact (C_bounded w (b i) ha).trans_lt (hw i)
  · apply (lower w (w i)).sum_mem
    intro j hj a ha
    have hb : C (M i j)*X j ∈ bounded w (w j) := by
      simpa using bounded_mul w (C_bounded w (M i j)) (X_bounded w j)
    exact (hb ha).trans_lt (Finset.mem_filter.mp hj).2

theorem triangular_cancellation {I : Type*} [Fintype I]
    (w : σ → ℕ) (hw : ∀ i, 0 < w i) (s : I → R)
    (b : I → σ → R) (M : I → σ → σ → R)
    (d : ℕ) (P : I → MvPolynomial σ R) (hP : ∀ i, P i ∈ bounded w d)
    (hrelation : ∀ a : σ →₀ ℕ, weight w a = d →
      ∑ i, (s i)^d * (P i).coeff a = 0) :
    (∑ i, bind₁ (triangular w (s i) (b i) (M i)) (P i)) ∈ lower w d :=
  diagonal_cancellation w s _ (fun i => triangular_lower w hw (s i) (b i) (M i))
    d P hP hrelation

def affineImage (b : σ → R) (M : σ → σ → R) (i : σ) : MvPolynomial σ R :=
  C (b i) + ∑ j, C (M i j)*X j

/-- A directly checkable matrix certificate, in the Python row convention.
No forbidden equal-weight mixing is hidden in a generic triangular claim. -/
theorem affineImage_lower (w : σ → ℕ) (hw : ∀ i, 0 < w i)
    (s : R) (b : σ → R) (M : σ → σ → R)
    (hdiag : ∀ i, M i i = s^(w i))
    (hupper : ∀ i j, i ≠ j → w i ≤ w j → M i j = 0) (i : σ) :
    affineImage b M i - C (s^(w i))*X i ∈ lower w (w i) := by
  classical
  have he : affineImage b M i - C (s^(w i))*X i =
      C (b i) + ∑ j, (C (M i j)*X j - if j = i then C (s^(w i))*X i else 0) := by
    rw [Finset.sum_sub_distrib]
    simp [affineImage]
    ring
  rw [he]
  apply (lower w (w i)).add_mem
  · intro a ha
    exact (C_bounded w (b i) ha).trans_lt (hw i)
  · apply (lower w (w i)).sum_mem
    intro j _
    by_cases hji : j = i
    · subst j
      simp [hdiag]
    · simp only [ite_eq_right hji, sub_zero]
      by_cases hj : w j < w i
      · intro a ha
        have hb : C (M i j)*X j ∈ bounded w (w j) := by
          simpa using bounded_mul w (C_bounded w (M i j)) (X_bounded w j)
        exact (hb ha).trans_lt hj
      · simp [hupper i j (Ne.symm hji) (Nat.le_of_not_gt hj)]

theorem affine_cancellation {I : Type*} [Fintype I]
    (w : σ → ℕ) (hw : ∀ i, 0 < w i) (s : I → R)
    (b : I → σ → R) (M : I → σ → σ → R)
    (hdiag : ∀ i j, M i j j = (s i)^(w j))
    (hupper : ∀ i j k, j ≠ k → w j ≤ w k → M i j k = 0)
    (d : ℕ) (P : I → MvPolynomial σ R) (hP : ∀ i, P i ∈ bounded w d)
    (hrelation : ∀ a : σ →₀ ℕ, weight w a = d →
      ∑ i, (s i)^d * (P i).coeff a = 0) :
    (∑ i, bind₁ (affineImage (b i) (M i)) (P i)) ∈ lower w d :=
  diagonal_cancellation w s _
    (fun i => affineImage_lower w hw (s i) (b i) (M i) (hdiag i) (hupper i))
    d P hP hrelation

end Triangular

theorem constant_after_weight_one (w : σ → ℕ) (hw : ∀ i, 0 < w i)
    (P : MvPolynomial σ R) (hP : P ∈ lower w 1) : P = C (P.coeff 0) := by
  have hn : NonTorsionWeight w := nonTorsionWeight_of (fun i => Nat.ne_of_gt (hw i))
  rw [C_apply]
  apply eq_monomial_of_support_subset_singleton
  intro a ha
  have hz : weight w a = 0 := by
    have hlt : weight w a < 1 := hP ha
    omega
  ext i
  exact (weightedDegree_eq_zero_iff hn).mp hz i

theorem character_sum {I M : Type*} [CommMonoid M] (chi : AddChar R M)
    (s : Finset I) (a : I → R) : chi (∑ i ∈ s, a i) = ∏ i ∈ s, chi (a i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert i s hi ih => simp [hi, chi.map_add_eq_mul, ih]

/-- This is the phase product appearing in the mixed-channel theorem.
The degree-reduced polynomial is the sum, not an average or selected term. -/
theorem merged_character {I M : Type*} [Fintype I] [CommMonoid M]
    (chi : AddChar R M) (f : I → σ → MvPolynomial σ R)
    (P : I → MvPolynomial σ R) (x : σ → R) :
    (∏ i, chi (aeval (fun j => aeval x (f i j)) (P i))) =
      chi (aeval x (∑ i, bind₁ (f i) (P i))) := by
  simp only [map_sum, character_sum, aeval_bind₁]

/-- info: 'QSearch.WeightedPhaseErasure.pullback_agree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.pullback_agree
/-- info: 'QSearch.WeightedPhaseErasure.leading_coefficient' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.leading_coefficient
/-- info: 'QSearch.WeightedPhaseErasure.parameter_relation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.parameter_relation
/-- info: 'QSearch.WeightedPhaseErasure.diagonal_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.diagonal_cancellation
/-- info: 'QSearch.WeightedPhaseErasure.triangular_lower' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.triangular_lower
/-- info: 'QSearch.WeightedPhaseErasure.triangular_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.triangular_cancellation
/-- info: 'QSearch.WeightedPhaseErasure.affine_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.affine_cancellation
/-- info: 'QSearch.WeightedPhaseErasure.constant_after_weight_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.constant_after_weight_one
/-- info: 'QSearch.WeightedPhaseErasure.merged_character' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeightedPhaseErasure.merged_character

end
end QSearch.WeightedPhaseErasure
