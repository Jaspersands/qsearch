import Formal.CentralRegularSource
import Mathlib.Algebra.BigOperators.Group.Finset.Pi

/-!
# Mixed central-character descent

Derive the normalized character kernel from the original coset matrix,
then evaluate the literal controlled-right-action Kraus sums. A nonempty
active tensor and exact preservation of support are necessary. The source
tensor premise is independence, not a claim inferred from marginals.

Projector idempotence/completeness, the particular dilation/SDE instance,
and trace-distance composition are proved in the accompanying research
note, not by these abstract algebraic identities.
-/

namespace QSearch.CentralCharacterDescent

open scoped BigOperators
open QSearch.AffineSupportErasure (invSize uniformAmplitude)
noncomputable section
attribute [local instance] Classical.propDecidable

section Source
variable {G C : Type*} [Group G] [CommGroup C] [Fintype G] [Fintype C]

def coefficient (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ) (g : G) : ℂ :=
  ∑ z, if g * (embed z)⁻¹ ∈ H then chi z else 0

omit [Fintype G] in
theorem coefficient_at (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (transverse : ∀ z, embed z ∈ H ↔ z = 1) (h : G) (hh : h ∈ H) (z : C) :
    coefficient H embed chi (h * embed z) = chi z := by
  have hf (w : C) : h * embed z * (embed w)⁻¹ ∈ H ↔ w = z := by
    rw [show h * embed z * (embed w)⁻¹ = h * embed (z * w⁻¹) by
      simp only [map_mul, map_inv, mul_assoc]]
    rw [H.mul_mem_cancel_left hh, transverse, mul_inv_eq_one]
    exact eq_comm
  simp [coefficient, hf]

omit [Fintype G] in
theorem coefficient_off (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (g : G) (outside : ∀ z, g * (embed z)⁻¹ ∉ H) :
    coefficient H embed chi g = 0 := by
  simp [coefficient, outside]

def twistedEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ := invSize G * coefficient H embed chi (y⁻¹ * x)

/-- One-sided multiplication by the central spectral projector, with its
actual normalization. For a central embedding this equals Pi*rho*Pi:
commutation and projector idempotence are separate operator facts. -/
def projectedEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ :=
  invSize C * ∑ z, chi z *
    CosetSourceFourier.groupEntry H (x * (embed z)⁻¹) y

theorem projected_source (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : projectedEntry H embed chi x y =
      invSize C * twistedEntry H embed chi x y := by
  have hf (z : C) : (x * (embed z)⁻¹)⁻¹ * y ∈ H ↔
      (y⁻¹ * x) * (embed z)⁻¹ ∈ H := by
    have he : (x * (embed z)⁻¹)⁻¹ * y = ((y⁻¹ * x) * (embed z)⁻¹)⁻¹ := by
      group
    rw [he, H.inv_mem_iff]
  simp only [projectedEntry, CosetSourceFourier.groupEntry, hf,
    twistedEntry, coefficient, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro z _
  split_ifs <;> ring

def rightCorrelation (rho : G → G → ℂ) (g : G) : ℂ :=
  ∑ x, rho x (x * g⁻¹)

theorem twisted_correlation (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (g : G) :
    rightCorrelation (twistedEntry H embed chi) g = coefficient H embed chi g := by
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [rightCorrelation, twistedEntry, invSize, hn]

theorem twisted_trace (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (transverse : ∀ z, embed z ∈ H ↔ z = 1) :
    (∑ x, twistedEntry H embed chi x x) = 1 := by
  have hc := coefficient_at H embed chi transverse 1 H.one_mem 1
  simp only [map_one, mul_one] at hc
  have ht := twisted_correlation H embed chi 1
  simpa [rightCorrelation, hc] using ht

theorem label_probability (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (transverse : ∀ z, embed z ∈ H ↔ z = 1) :
    (∑ x, projectedEntry H embed chi x x) = invSize C := by
  simp_rw [projected_source]
  rw [← Finset.mul_sum, twisted_trace H embed chi transverse, mul_one]
end Source

section ControlledAction
variable {G Q : Type*} [Group G] [Fintype G] [Fintype Q]

/-- Fresh uniform control and right multiplication, followed by tracing
the target. The Kraus index t is the discarded target basis state. -/
def actionKraus (A : Q → G) (t : G) (q : Q) (x : G) : ℂ :=
  if x = t * A q then uniformAmplitude Q else 0

def actionOutput (A : Q → G) (rho : G → G → ℂ) (q r : Q) : ℂ :=
  ∑ t, ∑ x, ∑ y, actionKraus A t q x * rho x y * star (actionKraus A t r y)

theorem action_output (A : Q → G) (rho : G → G → ℂ) (q r : Q) :
    actionOutput A rho q r = invSize Q * rightCorrelation rho ((A r)⁻¹ * A q) := by
  have hc : actionOutput A rho q r = invSize Q * ∑ t, rho (t * A q) (t * A r) := by
    simp only [actionOutput, actionKraus, apply_ite, star_zero,
      ite_mul, mul_zero, zero_mul]
    simp only [Finset.sum_ite_eq', Finset.mem_univ, ite_true]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    rw [mul_comm (uniformAmplitude Q), mul_assoc,
      AffineSupportErasure.uniformAmplitude_normalized, mul_comm]
  rw [hc]
  congr 1
  apply Fintype.sum_equiv (Equiv.mulRight (A q))
  intro t
  dsimp [rightCorrelation]
  congr 1
  group

theorem action_complete [Nonempty Q] (A : Q → G) (x y : G) :
    (∑ q, ∑ t, star (actionKraus A t q x) * actionKraus A t q y) =
      if x = y then 1 else 0 := by
  have he (q : Q) : (∑ t, star (actionKraus A t q x) * actionKraus A t q y) =
      if x = y then invSize Q else 0 := by
    have hx (t : G) : x = t * A q ↔ t = x * (A q)⁻¹ := by
      constructor <;> intro h
      · rw [h]; group
      · rw [h]; group
    have hk (t : G) : actionKraus A t q x =
        if t = x * (A q)⁻¹ then uniformAmplitude Q else 0 := by
      unfold actionKraus
      rw [hx]
    simp only [hk, apply_ite, star_zero, ite_mul, zero_mul,
      Finset.sum_ite_eq', Finset.mem_univ, ite_true]
    by_cases hxy : x = y
    · subst y
      simp only [actionKraus, inv_mul_cancel_right, ite_true]
      rw [mul_comm (star (uniformAmplitude Q)), AffineSupportErasure.uniformAmplitude_normalized]
    · simp [actionKraus, hxy, Ne.symm hxy]
  have hn : (Fintype.card Q : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp_rw [he]
  split_ifs <;> simp [invSize, hn]
end ControlledAction

section Tensor
variable {I G : Type*} [Fintype I] [Group G] [Fintype G]

/-- This is an independent tensor source, not a shared-randomness source. -/
theorem tensor_correlation (rho : I → G → G → ℂ) (a : I → G) :
    rightCorrelation (fun x y : I → G => ∏ i, rho i (x i) (y i)) a =
      ∏ i, rightCorrelation (rho i) (a i) := by
  simp only [rightCorrelation, Pi.mul_apply, Pi.inv_apply]
  exact (Fintype.prod_sum (fun i (x : G) => rho i x (x * (a i)⁻¹))).symm

omit [Group G] [Fintype G] in
/-- For active, nonzero scales only. Support preservation and character
cancellation are logically separate obligations. The all-zero case has
an empty product and would incorrectly give one outside the subgroup. -/
theorem cancelled_tensor [Nonempty I] (support : G → Prop)
    (kernel : I → G → ℂ) (A : I → G → G) (phase : I → G → ℂ)
    (outside : ∀ i g, ¬ support g → kernel i (A i g) = 0)
    (inside : ∀ i g, support g → kernel i (A i g) = phase i g)
    (cancel : ∀ g, support g → ∏ i, phase i g = 1) (g : G) :
    (∏ i, kernel i (A i g)) = if support g then 1 else 0 := by
  classical
  by_cases h : support g
  · simp only [h, ite_true]
    simpa only [inside _ _ h] using cancel g h
  · simp [h, outside _ _ h]

/-- Literal mixed-state channel output after the two independent
obligations (support and phase) have been discharged. A quotient
transversal makes this exactly the quotient subgroup coset matrix. -/
theorem descent_output {Q : Type*} [Fintype Q] [Nonempty I]
    (B : Subgroup G) (representative : Q → G) (A : I → G →* G)
    (rho : I → G → G → ℂ) (phase : I → G → ℂ)
    (outside : ∀ i g, g ∉ B → rightCorrelation (rho i) (A i g) = 0)
    (inside : ∀ i g, g ∈ B → rightCorrelation (rho i) (A i g) = phase i g)
    (cancel : ∀ g, g ∈ B → ∏ i, phase i g = 1) (q r : Q) :
    actionOutput (fun x i => A i (representative x))
      (fun x y : I → G => ∏ i, rho i (x i) (y i)) q r =
        invSize Q * (if (representative q)⁻¹ * representative r ∈ B then 1 else 0) := by
  rw [action_output, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply, ← map_inv, ← map_mul]
  rw [cancelled_tensor (fun g => g ∈ B) (fun i => rightCorrelation (rho i))
    (fun i g => A i g) phase outside inside cancel]
  have he : (representative r)⁻¹ * representative q ∈ B ↔
      (representative q)⁻¹ * representative r ∈ B := by
    rw [show (representative r)⁻¹ * representative q =
      ((representative q)⁻¹ * representative r)⁻¹ by group, B.inv_mem_iff]
  rw [he]
end Tensor

end
end QSearch.CentralCharacterDescent

/-- info: 'QSearch.CentralCharacterDescent.projected_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.projected_source

/-- info: 'QSearch.CentralCharacterDescent.action_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.action_output

/-- info: 'QSearch.CentralCharacterDescent.action_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.action_complete

/-- info: 'QSearch.CentralCharacterDescent.cancelled_tensor' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.cancelled_tensor

/-- info: 'QSearch.CentralCharacterDescent.descent_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.descent_output
