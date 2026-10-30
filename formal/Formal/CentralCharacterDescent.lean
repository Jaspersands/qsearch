import Formal.CentralRegularSource
import Formal.ReesHomogenization
import Mathlib.Algebra.BigOperators.Group.Finset.Pi

/-!
# Mixed central-character descent

Derive the normalized character kernel from the original coset matrix,
then evaluate the literal controlled-right-action Kraus sums. A nonempty
active tensor and exact preservation of support are necessary. The source
tensor premise is independence, not a claim inferred from marginals.
For an allowed character, normalization divides the raw twisted source
by the cardinality of the full preimage of H in C. No transverse hidden
intersection is assumed by normalized_descent_output.

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
/-- The Rees coefficient lemma applies to the actual source coefficient.
The count is of the preimage, including any kernel of embed. -/
theorem coefficient_allowed (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1)
    (h : G) (hh : h ∈ H) (z : C) :
    coefficient H embed chi (h * embed z) =
      (Fintype.card (H.comap embed) : ℂ) * chi z :=
  ReesHomogenization.coefficient_allowed H embed chi allowed h hh z

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

/-- The trace-one source for an allowed character. The raw twistedEntry
has trace |embed⁻¹(H)|, not one, when the intersection is nontrivial. -/
def normalizedEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ := invSize (H.comap embed) * twistedEntry H embed chi x y

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

theorem twisted_trace_allowed (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, twistedEntry H embed chi x x) = (Fintype.card (H.comap embed) : ℂ) := by
  have hc := coefficient_allowed H embed chi allowed 1 H.one_mem 1
  simp only [map_one, mul_one] at hc
  have ht := twisted_correlation H embed chi 1
  simpa [rightCorrelation, hc] using ht

theorem label_probability_allowed (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, projectedEntry H embed chi x x) =
      invSize C * (Fintype.card (H.comap embed) : ℂ) := by
  simp_rw [projected_source]
  rw [← Finset.mul_sum, twisted_trace_allowed H embed chi allowed]

theorem label_probability_allowed_ne_zero
    (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, projectedEntry H embed chi x x) ≠ 0 := by
  rw [label_probability_allowed H embed chi allowed]
  have hC : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have hH : (Fintype.card (H.comap embed) : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  exact mul_ne_zero (inv_ne_zero hC) hH

/-- This is normalization of the original projected coset matrix by its
actual branch trace, not an independently postulated character kernel. -/
theorem normalized_source (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) (x y : G) :
    normalizedEntry H embed chi x y =
      projectedEntry H embed chi x y / (∑ t, projectedEntry H embed chi t t) := by
  rw [projected_source, label_probability_allowed H embed chi allowed]
  have hC : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  unfold normalizedEntry invSize
  rw [mul_div_mul_left _ _ (inv_ne_zero hC), div_eq_mul_inv, mul_comm]

theorem normalized_correlation (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (g : G) :
    rightCorrelation (normalizedEntry H embed chi) g =
      invSize (H.comap embed) * coefficient H embed chi g := by
  unfold rightCorrelation
  simp only [normalizedEntry, ← Finset.mul_sum]
  rw [← rightCorrelation, twisted_correlation]

theorem normalized_correlation_at (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1)
    (h : G) (hh : h ∈ H) (z : C) :
    rightCorrelation (normalizedEntry H embed chi) (h * embed z) = chi z := by
  rw [normalized_correlation, coefficient_allowed H embed chi allowed h hh z]
  have hn : (Fintype.card (H.comap embed) : ℂ) ≠ 0 := by
    exact_mod_cast Fintype.card_ne_zero
  change (Fintype.card (H.comap embed) : ℂ)⁻¹ *
    ((Fintype.card (H.comap embed) : ℂ) * chi z) = chi z
  rw [← mul_assoc, inv_mul_cancel₀ hn, one_mul]

theorem normalized_correlation_off (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (g : G) (outside : ∀ z, g * (embed z)⁻¹ ∉ H) :
    rightCorrelation (normalizedEntry H embed chi) g = 0 := by
  rw [normalized_correlation, coefficient_off H embed chi g outside, mul_zero]

theorem normalized_trace (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, normalizedEntry H embed chi x x) = 1 := by
  have ht := normalized_correlation_at H embed chi allowed 1 H.one_mem 1
  simpa [rightCorrelation] using ht

omit [Fintype G] [Fintype C] in
/-- Centrality identifies the subgroup support with H times range(embed).
Injectivity is not needed: all normalization counts use the preimage. -/
theorem mem_saturation_iff (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (g : G) :
    g ∈ H ⊔ embed.range ↔ ∃ z, g * (embed z)⁻¹ ∈ H := by
  let : embed.range.Normal := ⟨by
    rintro _ ⟨z, rfl⟩ x
    exact ⟨z, by rw [← central z x]; simp [mul_assoc]⟩⟩
  rw [Subgroup.mem_sup_of_normal_right]
  constructor
  · rintro ⟨h, hh, _, ⟨z, rfl⟩, rfl⟩
    exact ⟨z, by simpa using hh⟩
  · rintro ⟨z, hz⟩
    exact ⟨g * (embed z)⁻¹, hz, embed z, ⟨z, rfl⟩, by simp⟩
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

/-- Specialize descent_output to independent, actually normalized source
branches with arbitrary hidden central intersection. centralPart is a
proof witness for the supported decomposition, not input to actionKraus.
Support preservation and phase cancellation remain explicit obligations. -/
theorem normalized_descent_output {Q C : Type*} [Fintype Q] [CommGroup C]
    [Fintype C] [Nonempty I]
    (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : I → C →* ℂ) (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (representative : Q → G) (A : I → G →* G) (centralPart : I → G → C)
    (preserves : ∀ i g, A i g ∈ H ⊔ embed.range ↔ g ∈ H ⊔ embed.range)
    (decompose : ∀ i g, g ∈ H ⊔ embed.range →
      A i g * (embed (centralPart i g))⁻¹ ∈ H)
    (cancel : ∀ g, g ∈ H ⊔ embed.range → ∏ i, chi i (centralPart i g) = 1)
    (q r : Q) :
    actionOutput (fun x i => A i (representative x))
      (fun x y : I → G => ∏ i, normalizedEntry H embed (chi i) (x i) (y i)) q r =
        invSize Q *
          (if (representative q)⁻¹ * representative r ∈ H ⊔ embed.range then 1 else 0) := by
  apply descent_output (H ⊔ embed.range) representative A
    (fun i => normalizedEntry H embed (chi i)) (fun i g => chi i (centralPart i g))
    ?_ ?_ cancel q r
  · intro i g hg
    apply normalized_correlation_off
    intro z hz
    exact hg ((preserves i g).mp ((mem_saturation_iff H embed central (A i g)).mpr ⟨z, hz⟩))
  · intro i g hg
    have ht := normalized_correlation_at H embed (chi i) (allowed i)
      (A i g * (embed (centralPart i g))⁻¹) (decompose i g hg) (centralPart i g)
    simpa using ht
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

/-- info: 'QSearch.CentralCharacterDescent.coefficient_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.coefficient_allowed

/-- info: 'QSearch.CentralCharacterDescent.label_probability_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.label_probability_allowed

/-- info: 'QSearch.CentralCharacterDescent.label_probability_allowed_ne_zero' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.label_probability_allowed_ne_zero

/-- info: 'QSearch.CentralCharacterDescent.normalized_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_source

/-- info: 'QSearch.CentralCharacterDescent.normalized_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_trace

/-- info: 'QSearch.CentralCharacterDescent.normalized_correlation_at' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_correlation_at

/-- info: 'QSearch.CentralCharacterDescent.mem_saturation_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.mem_saturation_iff

/-- info: 'QSearch.CentralCharacterDescent.normalized_descent_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralCharacterDescent.normalized_descent_output
