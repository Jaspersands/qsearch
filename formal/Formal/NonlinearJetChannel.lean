import Formal.WeylSourceScalarization
import Formal.CosetSourceFourier

/-!
# Nonlinear-jet measurement channel

The curve is a proof witness, never an input to a Kraus operator. Public
translation-dependent linear maps transport the curve. We derive the mixed
branch, completeness, spectator reduction and negative-Fourier residual.
Taylor closure, weighted polynomial cancellation, rank/SDE guarantees and
the complete HSP receiver are NOT established by this module.
-/

namespace QSearch.NonlinearJetChannel

open scoped BigOperators
open QSearch.AffineSupportErasure
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F V J I : Type*} [Field F] [AddCommGroup V] [Module F V]
  [AddCommGroup J] [Module F J]

def curveRel (U : Submodule F V) (curve : V → J) (x x' : V × J) : Prop :=
  x.1 - x'.1 ∈ U ∧ curve x.1 + x.2 = curve x'.1 + x'.2

def publicPoint (c : F) (A : V → J →ₗ[F] J) (outcome x : V × J) : V × J :=
  (outcome.1 + c • x.1, outcome.2 + A outcome.1 x.2)

theorem public_support_iff (U : Submodule F V) (curve : V → J)
    (c : F) (A : V → J →ₗ[F] J) (hc : c ≠ 0)
    (hA : ∀ y, Function.Injective (A y))
    (hcurve : ∀ y q, curve (y + c • q) = curve y + A y (curve q))
    (o x x' : V × J) :
    curveRel U curve (publicPoint c A o x) (publicPoint c A o x') ↔
      curveRel U curve x x' := by
  have first : (o.1 + c • x.1) - (o.1 + c • x'.1) = c • (x.1 - x'.1) := by
    rw [smul_sub]
    abel
  have second (v : V × J) :
      curve (o.1 + c • v.1) + (o.2 + A o.1 v.2) =
        (curve o.1 + o.2) + A o.1 (curve v.1 + v.2) := by
    rw [hcurve, map_add]
    abel
  simp only [curveRel, publicPoint, first, U.smul_mem_iff hc, second,
    add_right_inj, (hA o.1).eq_iff]

def point (c : I → F) (A : I → V → J →ₗ[F] J)
    (o : I → V × J) (x : V × J) : I → V × J :=
  fun i => publicPoint (c i) (A i) (o i) x

def inverseOutcome (c : I → F) (A : I → V → J →ₗ[F] J)
    (a : I → V × J) (x : V × J) : I → V × J :=
  fun i => ((a i).1 - c i • x.1, (a i).2 - A i ((a i).1 - c i • x.1) x.2)

theorem point_eq_iff (c : I → F) (A : I → V → J →ₗ[F] J)
    (o a : I → V × J) (x : V × J) :
    a = point c A o x ↔ o = inverseOutcome c A a x := by
  constructor
  · intro h
    funext i
    have hi := congrFun h i
    have hy : (o i).1 = (a i).1 - c i • x.1 :=
      (eq_sub_iff_add_eq).mpr (congrArg Prod.fst hi).symm
    apply Prod.ext
    · exact hy
    · change (o i).2 = (a i).2 - A i ((a i).1 - c i • x.1) x.2
      rw [← hy]
      exact (eq_sub_iff_add_eq).mpr (congrArg Prod.snd hi).symm
  · intro h
    rw [h]
    funext i
    simp [point, publicPoint, inverseOutcome]

section Finite
variable [Fintype V] [Fintype J] [Fintype I]

def curveRho (U : Submodule F V) (curve : V → J) (phase : V × J → ℂ)
    (x x' : V × J) : ℂ :=
  if curveRel U curve x x' then invSize (V × J) * phase x * star (phase x') else 0

def tensorCurve (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ) (a b : I → V × J) : ℂ :=
  ∏ i, curveRho U curve (phase i) (a i) (b i)

def mergedPhase (phase : I → V × J → ℂ) (c : I → F)
    (A : I → V → J →ₗ[F] J) (o : I → V × J) (x : V × J) : ℂ :=
  ∏ i, phase i (point c A o x i)

def kraus (amplitude : ℂ) (c : I → F) (A : I → V → J →ₗ[F] J)
    (o : I → V × J) (x : V × J) (a : I → V × J) : ℂ :=
  if a = point c A o x then amplitude else 0

def branch (amplitude : ℂ) (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ) (c : I → F) (A : I → V → J →ₗ[F] J)
    (o : I → V × J) (x x' : V × J) : ℂ :=
  ∑ a, ∑ b, kraus amplitude c A o x a * tensorCurve U curve phase a b
    * star (kraus amplitude c A o x' b)

theorem branch_pullback (amplitude : ℂ) (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ) (c : I → F) (A : I → V → J →ₗ[F] J)
    (o : I → V × J) (x x' : V × J) :
    branch amplitude U curve phase c A o x x' =
      (amplitude * star amplitude) * tensorCurve U curve phase (point c A o x) (point c A o x') := by
  classical
  simp [branch, kraus, apply_ite, ite_mul]
  ring

/-- No assumption about curve, support, phase, or invertibility is needed
for completeness. The Y-dependent A is evaluated after Y is measured. -/
theorem kraus_complete (c : I → F) (A : I → V → J →ₗ[F] J)
    (a b : I → V × J) :
    (∑ o, ∑ x, star (kraus (uniformAmplitude (V × J)) c A o x a)
      * kraus (uniformAmplitude (V × J)) c A o x b) = if a = b then 1 else 0 := by
  classical
  rw [Finset.sum_comm]
  have fixed (x : V × J) :
      (∑ o, star (kraus (uniformAmplitude (V × J)) c A o x a)
        * kraus (uniformAmplitude (V × J)) c A o x b) =
        if a = b then invSize (V × J) else 0 := by
    simp only [kraus, point_eq_iff, apply_ite, star_zero]
    by_cases h : a = b
    · subst b
      simp only [ite_mul, zero_mul, mul_zero]
      simpa [mul_comm] using uniformAmplitude_normalized (V := V × J)
    · have hshift : inverseOutcome c A a x ≠ inverseOutcome c A b x := by
        intro heq
        have ha : a = point c A (inverseOutcome c A a x) x := (point_eq_iff c A _ a x).mpr rfl
        have hb : b = point c A (inverseOutcome c A b x) x := (point_eq_iff c A _ b x).mpr rfl
        rw [heq] at ha
        exact h (ha.trans hb.symm)
      simp_all [ite_mul]
      intro heq
      exact (hshift heq.symm).elim
  simp_rw [fixed]
  have hcard : (Fintype.card (V × J) : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  by_cases h : a = b
  · simp only [h, ite_true, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, invSize]
    exact mul_inv_cancel₀ hcard
  · simp [h]

omit [Module F J] in
theorem curve_trace_one (U : Submodule F V) (curve : V → J)
    (phase : V × J → ℂ) (hphase : ∀ x, phase x * star (phase x) = 1) :
    (∑ x, curveRho U curve phase x x) = 1 := by
  have hcard : (Fintype.card (V × J) : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  simp only [curveRho, curveRel, sub_self, U.zero_mem, and_self, ite_true,
    mul_assoc, hphase, mul_one, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  simp only [invSize]
  exact mul_inv_cancel₀ hcard

omit [Module F J] in
/-- Tracing a tensor of independently prepared, normalized curve sources
gives one, including the empty tensor. Marginal normalization alone does
not assert this tensor-input premise. -/
theorem tensor_curve_trace_one (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ)
    (hphase : ∀ i x, phase i x * star (phase i x) = 1) :
    (∑ a, tensorCurve U curve phase a a) = 1 := by
  classical
  change (∑ a : I → V × J, ∏ i, curveRho U curve (phase i) (a i) (a i)) = 1
  rw [← Fintype.prod_sum (fun i x => curveRho U curve (phase i) x x)]
  simp_rw [curve_trace_one U curve _ (hphase _)]
  simp

omit [Module F J] in
/-- After publicly splitting independent inputs into retained and discarded
factors, partial trace of the discarded factors preserves the retained
kernel. Apply at a fixed complete classical history, before new outcomes. -/
theorem discard_independent_curve_sources {K : Type*} [Fintype K]
    (U : Submodule F V) (curve : V → J)
    (retained : I → V × J → ℂ) (discarded : K → V × J → ℂ)
    (hdiscarded : ∀ i x, discarded i x * star (discarded i x) = 1)
    (a b : I → V × J) :
    (∑ z, tensorCurve U curve retained a b * tensorCurve U curve discarded z z) =
      tensorCurve U curve retained a b := by
  rw [← Finset.mul_sum, tensor_curve_trace_one U curve discarded hdiscarded, mul_one]

/-- The nonlinear support is derived from public transport, not assumed
to be a submodule. All inputs here are active, independently prepared copies. -/
theorem mixed_branch_identity [Nonempty I] (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ) (c : I → F) (A : I → V → J →ₗ[F] J)
    (hc : ∀ i, c i ≠ 0) (hA : ∀ i y, Function.Injective (A i y))
    (hcurve : ∀ i y q, curve (y + c i • q) = curve y + A i y (curve q))
    (o : I → V × J) (x x' : V × J) :
    branch (uniformAmplitude (V × J)) U curve phase c A o x x' =
      invSize (V × J) ^ Fintype.card I * curveRho U curve (mergedPhase phase c A o) x x' := by
  have hs : (∀ i, curveRel U curve (point c A o x i) (point c A o x' i)) ↔ curveRel U curve x x' := by
    simp only [point, public_support_iff U curve _ _ (hc _) (hA _) (hcurve _), forall_const]
  rw [branch_pullback, uniformAmplitude_normalized]
  simp only [tensorCurve, curveRho, Fintype.prod_ite_zero, hs]
  by_cases h : curveRel U curve x x'
  · simp only [h, ite_true, mergedPhase, Finset.prod_mul_distrib, Finset.prod_const,
      Finset.card_univ, star_prod]
    ring
  · simp [h]

omit [Fintype V] [Fintype J] in
theorem merged_phase_unit (phase : I → V × J → ℂ)
    (hphase : ∀ i x, phase i x * star (phase i x) = 1)
    (c : I → F) (A : I → V → J →ₗ[F] J) (o : I → V × J) (x : V × J) :
    mergedPhase phase c A o x * star (mergedPhase phase c A o x) = 1 := by
  simp only [mergedPhase, star_prod, ← Finset.prod_mul_distrib, hphase,
    Finset.prod_const_one]

theorem branch_probability [Nonempty I] (U : Submodule F V) (curve : V → J)
    (phase : I → V × J → ℂ) (hphase : ∀ i x, phase i x * star (phase i x) = 1)
    (c : I → F) (A : I → V → J →ₗ[F] J) (hc : ∀ i, c i ≠ 0)
    (hA : ∀ i y, Function.Injective (A i y))
    (hcurve : ∀ i y q, curve (y + c i • q) = curve y + A i y (curve q))
    (o : I → V × J) :
    (∑ x, branch (uniformAmplitude (V × J)) U curve phase c A o x x) =
      invSize (V × J) ^ Fintype.card I := by
  simp_rw [mixed_branch_identity U curve phase c A hc hA hcurve]
  rw [← Finset.mul_sum, curve_trace_one U curve _ (merged_phase_unit phase hphase c A o)]
  simp

omit [Module F J] in
/-- If U=0, the entire source is maximally mixed for every curve and phase.
Therefore the source cannot in general reveal the curve coefficients. -/
theorem trivial_support_hides_curve (curve : V → J) (phase : V × J → ℂ)
    (hphase : ∀ x, phase x * star (phase x) = 1) (x x' : V × J) :
    curveRho (⊥ : Submodule F V) curve phase x x' = if x = x' then invSize (V × J) else 0 := by
  rcases x with ⟨q, t⟩
  rcases x' with ⟨r, u⟩
  by_cases hq : q = r <;> by_cases ht : t = u <;>
    simp_all [curveRho, curveRel, sub_eq_zero, mul_assoc]

omit [Module F J] in
/-- Even for nonzero U, an additive curve offset constant on U-cosets is
unidentifiable from this source. This is not an HPGP coefficient oracle. -/
theorem coset_gauge_invariance (U : Submodule F V) (curve offset : V → J)
    (hoffset : ∀ q r, q - r ∈ U → offset q = offset r)
    (phase : V × J → ℂ) (x x' : V × J) :
    curveRho U (fun q => curve q + offset q) phase x x' = curveRho U curve phase x x' := by
  by_cases hu : x.1 - x'.1 ∈ U
  · have left : (curve x.1 + offset x.1) + x.2 = (curve x.1 + x.2) + offset x'.1 := by
      rw [hoffset x.1 x'.1 hu]
      abel
    have right : (curve x'.1 + offset x'.1) + x'.2 = (curve x'.1 + x'.2) + offset x'.1 := by abel
    simp only [curveRho, curveRel, hu, true_and, left, right, add_left_inj]
  · simp [curveRho, curveRel, hu]

end Finite

section Spectator
variable {S : Type*} [AddCommGroup S] [Fintype S] [Fintype V] [Fintype J]

omit [Module F J] in
/-- Compose with the existing actual spectator Kraus sums. No linearity
of the retained curve is imposed. -/
theorem nonlinear_source_to_scalar (U : Submodule F V) (curve : V → J)
    (a : J) (b : S) (gamma : V → J × S → ℂ) (outcome : S) (x x' : V × J) :
    WeylSourceScalarization.spectatorBranch U (fun q => (a + curve q, b)) gamma outcome x x' =
      invSize S * curveRho U curve (WeylSourceScalarization.scalarPhase gamma outcome) x x' := by
  rw [WeylSourceScalarization.spectator_pullback]
  have first : (a + curve x.1) + x.2 = (a + curve x'.1) + x'.2 ↔
      curve x.1 + x.2 = curve x'.1 + x'.2 := by simp [add_assoc]
  have normalization : invSize V * invSize (J × S) = invSize S * invSize (V × J) := by
    simp only [invSize, Fintype.card_prod, Nat.cast_mul, mul_inv_rev]
    ring
  simp only [WeylSourceScalarization.matrixSource, WeylSourceScalarization.gauge_kernel_identity,
    Prod.mk_add_mk, Prod.mk.injEq, first, and_true, curveRho, curveRel,
    WeylSourceScalarization.scalarPhase, star_star]
  by_cases hu : x.1 - x'.1 ∈ U <;> by_cases ht : curve x.1 + x.2 = curve x'.1 + x'.2 <;>
    simp_all [mul_assoc]

end Spectator

section Fourier
variable [Fintype V] [Fintype J]

/-- The negative-character readout block after the first erasure, including
its Fourier normalization. No zero-label postselection is imposed. -/
def jetFourierBlock (U : Submodule F V) (curve : V → J) (χ : AddChar J ℂ)
    (q r : V) : ℂ :=
  invSize J * ∑ a, ∑ b, star (χ a) * curveRho U curve (fun _ => 1) (q, a) (r, b) * χ b

omit [Module F J] in
theorem fourier_residual (U : Submodule F V) (curve : V → J)
    (χ : AddChar J ℂ) (hunit : ∀ a, χ a * star (χ a) = 1) (q r : V) :
    jetFourierBlock U curve χ q r = invSize J * rho U (fun x => χ (curve x)) q r := by
  have hsupport (a b : J) : curve q + a = curve r + b ↔ b = a + (curve q - curve r) := by
    constructor
    · intro h
      calc
        b = (curve r + b) - curve r := by abel
        _ = (curve q + a) - curve r := by rw [← h]
        _ = a + (curve q - curve r) := by abel
    · intro h
      rw [h]
      abel
  by_cases hu : q - r ∈ U
  · have hentry (a b : J) : curveRho U curve (fun _ => 1) (q, a) (r, b) =
        if b = a + (curve q - curve r) then invSize (V × J) else 0 := by
      simp [curveRho, curveRel, hu, hsupport]
    have collapse (a : J) :
        (∑ b, star (χ a) * (if b = a + (curve q - curve r) then invSize (V × J) else 0) * χ b) =
          invSize (V × J) * χ (curve q - curve r) := by
      simp only [mul_ite, ite_mul, mul_zero, zero_mul, Finset.sum_ite_eq',
        Finset.mem_univ, ite_true, χ.map_add_eq_mul]
      calc
        star (χ a) * invSize (V × J) * (χ a * χ (curve q - curve r)) =
            invSize (V × J) * (χ a * star (χ a)) * χ (curve q - curve r) := by ring
        _ = _ := by rw [hunit, mul_one]
    have hcard : (Fintype.card J : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
    simp only [jetFourierBlock, hentry, collapse, Finset.sum_const, Finset.card_univ,
      nsmul_eq_mul, rho, hu, ite_true]
    rw [← QSearch.CosetSourceFourier.character_product χ hunit]
    simp only [invSize, Fintype.card_prod, Nat.cast_mul, mul_inv_rev]
    field_simp
  · simp [jetFourierBlock, curveRho, curveRel, hu, rho]

omit [Module F J] in
theorem fourier_probability (U : Submodule F V) (curve : V → J)
    (χ : AddChar J ℂ) (hunit : ∀ a, χ a * star (χ a) = 1) :
    (∑ q, jetFourierBlock U curve χ q q) = invSize J := by
  simp_rw [fourier_residual U curve χ hunit]
  rw [← Finset.mul_sum, rho_trace_one U _ (fun q => hunit (curve q)), mul_one]

end Fourier

/-- info: 'QSearch.NonlinearJetChannel.public_support_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.public_support_iff
/-- info: 'QSearch.NonlinearJetChannel.kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.kraus_complete
/-- info: 'QSearch.NonlinearJetChannel.mixed_branch_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.mixed_branch_identity
/-- info: 'QSearch.NonlinearJetChannel.branch_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.branch_probability
/-- info: 'QSearch.NonlinearJetChannel.nonlinear_source_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.nonlinear_source_to_scalar
/-- info: 'QSearch.NonlinearJetChannel.fourier_residual' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.fourier_residual
/-- info: 'QSearch.NonlinearJetChannel.fourier_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.fourier_probability
/-- info: 'QSearch.NonlinearJetChannel.trivial_support_hides_curve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.trivial_support_hides_curve
/-- info: 'QSearch.NonlinearJetChannel.coset_gauge_invariance' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.coset_gauge_invariance

end
end QSearch.NonlinearJetChannel
