import Formal.CentralCharacterDescent
import Formal.RecursiveOracleReduction
import Mathlib.Algebra.Group.AddChar

/-!
# Central descent to an actual quotient coset state

The quotient map has exactly the supplied central kernel. The public section
need not be a homomorphism. Support preservation and the supported phases are
derived from automorphisms preserving H and their action on the central group,
not assumed as correlation identities. Only active (unit) scales occur here.
The independent normalized input tensor and the character cancellation
equation remain explicit. This is not a solver/runtime or instrument theorem.
-/

namespace QSearch.CentralQuotientReceiver

open QSearch.CentralCharacterDescent
open QSearch.AffineSupportErasure (invSize)

noncomputable section
attribute [local instance] Classical.propDecidable

section Groups

variable {G Q C I : Type*} [Group G] [Group Q] [CommGroup C]

theorem disallowed_character_sum [Fintype C]
    (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (z : C) (hz : embed z ∈ H) (nontrivial : chi z ≠ 1) :
    (∑ w : C, if embed w ∈ H then chi w else 0) = 0 := by
  apply eq_zero_of_mul_eq_self_left nontrivial
  rw [Finset.mul_sum]
  apply Fintype.sum_equiv (Equiv.mulLeft z)
  intro w
  change chi z * (if embed w ∈ H then chi w else 0) =
    if embed (z * w) ∈ H then chi (z * w) else 0
  simp only [map_mul, H.mul_mem_cancel_left hz]
  split_ifs <;> simp

theorem disallowed_coefficient [Fintype C]
    (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (z : C) (hz : embed z ∈ H) (nontrivial : chi z ≠ 1) (g : G) :
    coefficient H embed chi g = 0 := by
  by_cases hg : ∃ w, g * (embed w)⁻¹ ∈ H
  · obtain ⟨w, hw⟩ := hg
    have ht := QSearch.ReesHomogenization.coefficient_translate H embed chi
      (g * (embed w)⁻¹) hw w
    rw [disallowed_character_sum H embed chi z hz nontrivial, zero_mul] at ht
    simpa [QSearch.ReesHomogenization.coefficient, coefficient] using ht
  · exact coefficient_off H embed chi g (by simpa using hg)

/-- A disallowed character has a zero source matrix, not a rare normalized
branch that must be divided by its probability. -/
theorem disallowed_projected_source [Fintype G] [Fintype C]
    (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (z : C) (hz : embed z ∈ H) (nontrivial : chi z ≠ 1) (x y : G) :
    projectedEntry H embed chi x y = 0 := by
  rw [projected_source]
  simp [twistedEntry, disallowed_coefficient H embed chi z hz nontrivial]

theorem nonzero_branch_iff_allowed [Fintype G] [Fintype C]
    (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ) :
    (∑ x, projectedEntry H embed chi x x) ≠ 0 ↔
      ∀ z, embed z ∈ H → chi z = 1 := by
  constructor
  · intro positive z hz
    by_contra hn
    exact positive (by simp [disallowed_projected_source H embed chi z hz hn])
  · exact label_probability_allowed_ne_zero H embed chi

theorem quotient_membership (pi : G →* Q) (embed : C →* G)
    (kernel : pi.ker = embed.range) (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (g : G) :
    pi g ∈ H.map pi ↔ g ∈ H ⊔ embed.range := by
  constructor
  · rintro ⟨h, hh, he⟩
    have hk : h⁻¹ * g ∈ pi.ker := by
      change pi (h⁻¹ * g) = 1
      simp [he]
    rw [kernel] at hk
    obtain ⟨z, hz⟩ := hk
    apply (mem_saturation_iff H embed central g).mpr
    refine ⟨z, ?_⟩
    simpa [hz] using hh
  · intro hg
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central g).mp hg
    have hk : embed z ∈ pi.ker := by rw [kernel]; exact ⟨z, rfl⟩
    have hp : pi (embed z) = 1 := hk
    exact ⟨g * (embed z)⁻¹, hz, by simp [hp]⟩

theorem dilation_preserves_saturation (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (A : G ≃* G) (scale : C ≃* C)
    (preserves : ∀ g, A g ∈ H ↔ g ∈ H)
    (on_center : ∀ z, A (embed z) = embed (scale z)) (g : G) :
    A g ∈ H ⊔ embed.range ↔ g ∈ H ⊔ embed.range := by
  constructor
  · intro hg
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central (A g)).mp hg
    apply (mem_saturation_iff H embed central g).mpr
    refine ⟨scale.symm z, (preserves _).mp ?_⟩
    simpa [on_center] using hz
  · intro hg
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central g).mp hg
    apply (mem_saturation_iff H embed central (A g)).mpr
    refine ⟨scale z, ?_⟩
    simpa [on_center] using (preserves _).mpr hz

variable [Fintype G] [Fintype C] [Fintype I] [Nonempty I]

theorem cancelled_normalized_correlation (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : I → C →* ℂ) (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (A : I → G ≃* G) (scale : I → C ≃* C)
    (preserves : ∀ i g, A i g ∈ H ↔ g ∈ H)
    (on_center : ∀ i z, A i (embed z) = embed (scale i z))
    (cancel : ∀ z, ∏ i, chi i (scale i z) = 1) (g : G) :
    (∏ i, rightCorrelation (normalizedEntry H embed (chi i)) (A i g)) =
      if g ∈ H ⊔ embed.range then 1 else 0 := by
  classical
  by_cases hg : g ∈ H ⊔ embed.range
  · rw [ite_eq_left hg]
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central g).mp hg
    have hi (i : I) :
        rightCorrelation (normalizedEntry H embed (chi i)) (A i g) =
          chi i (scale i z) := by
      have ht := normalized_correlation_at H embed (chi i) (allowed i)
        (A i (g * (embed z)⁻¹)) ((preserves i _).mpr hz) (scale i z)
      simpa [on_center] using ht
    simpa only [hi] using cancel z
  · rw [ite_eq_right hg]
    have hi (i : I) :
        rightCorrelation (normalizedEntry H embed (chi i)) (A i g) = 0 := by
      apply normalized_correlation_off
      intro z hz
      apply hg
      apply (dilation_preserves_saturation H embed central (A i) (scale i)
        (preserves i) (on_center i) g).mp
      exact (mem_saturation_iff H embed central (A i g)).mpr ⟨z, hz⟩
    simp [hi]

/-- Every admissible label/witness branch gives the same actual quotient coset
matrix. No normality of H, trivial H-intersection, or homomorphic section. -/
theorem quotient_coset_output [Fintype Q]
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : I → C →* ℂ) (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (A : I → G ≃* G) (scale : I → C ≃* C)
    (preserves : ∀ i g, A i g ∈ H ↔ g ∈ H)
    (on_center : ∀ i z, A i (embed z) = embed (scale i z))
    (cancel : ∀ z, ∏ i, chi i (scale i z) = 1) (q r : Q) :
    actionOutput (fun x i => A i (representative x))
      (fun x y : I → G => ∏ i, normalizedEntry H embed (chi i) (x i) (y i)) q r =
        QSearch.CosetSourceFourier.groupEntry (H.map pi) q r := by
  classical
  rw [action_output, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply, ← map_inv, ← map_mul]
  rw [cancelled_normalized_correlation H embed central chi allowed A scale
    preserves on_center cancel]
  rw [← quotient_membership pi embed kernel central H]
  simp only [map_mul, map_inv, section_law]
  have he : r⁻¹ * q ∈ H.map pi ↔ q⁻¹ * r ∈ H.map pi := by
    rw [show r⁻¹ * q = (q⁻¹ * r)⁻¹ by group, Subgroup.inv_mem_iff]
  rw [he]
  simp only [QSearch.CosetSourceFourier.groupEntry, mul_ite, mul_one, mul_zero]

end Groups

section ScalarLabels

variable {F V I : Type*} [Field F] [AddCommGroup V] [Module F V] [Fintype I]

def scalarAutomorphism (u : Fˣ) : Multiplicative V ≃* Multiplicative V where
  toFun z := Multiplicative.ofAdd ((u : F) • z.toAdd)
  invFun z := Multiplicative.ofAdd (((u⁻¹ : Fˣ) : F) • z.toAdd)
  left_inv z := by simp [smul_smul]
  right_inv z := by simp [smul_smul]
  map_mul' z w := by
    change (u : F) • (z.toAdd + w.toAdd) = (u : F) • z.toAdd + (u : F) • w.toAdd
    exact smul_add _ _ _

def labelCharacter (chi : AddChar F ℂ) (label : V →ₗ[F] F) : Multiplicative V →* ℂ :=
  (chi.compAddMonoidHom label.toAddMonoidHom).toMonoidHom

theorem active_sde (d : ℕ) (positive : 0 < d)
    (labels : I → V →ₗ[F] F) (scales : I → F)
    (sde : ∑ i, scales i ^ d • labels i = 0) :
    ∑ i : {i // scales i ≠ 0}, scales i.val ^ d • labels i.val = 0 := by
  have hz : (∑ i : {i // ¬scales i ≠ 0}, scales i.val ^ d • labels i.val) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    have hi : scales i.val = 0 := not_not.mp i.property
    simp [hi, zero_pow (Nat.ne_of_gt positive)]
  have ht := Fintype.sum_subtype_add_sum_subtype (fun i => scales i ≠ 0)
    (fun i => scales i ^ d • labels i)
  simpa only [hz, add_zero, sde] using ht

omit [Fintype I] in
theorem active_nonempty (scales : I → F) (witness : ∃ i, scales i ≠ 0) :
    Nonempty {i // scales i ≠ 0} := by
  obtain ⟨i, hi⟩ := witness
  exact ⟨⟨i, hi⟩⟩

/-- The SDE equation is an equality of linear functionals, not a sampled
test on selected central elements. Zero-scale removal needs d>0. -/
theorem sde_character_cancellation (chi : AddChar F ℂ) (d : ℕ)
    (labels : I → V →ₗ[F] F) (scales : I → F)
    (sde : ∑ i, scales i ^ d • labels i = 0) (z : V) :
    (∏ i, chi (labels i (scales i ^ d • z))) = 1 := by
  have hs : ∑ i, labels i (scales i ^ d • z) = 0 := by
    have h := congrArg (fun f : V →ₗ[F] F => f z) sde
    simpa [LinearMap.sum_apply, LinearMap.smul_apply] using h
  have hsum (s : Finset I) :
      chi (∑ i ∈ s, labels i (scales i ^ d • z)) =
        ∏ i ∈ s, chi (labels i (scales i ^ d • z)) := by
    classical
    induction s using Finset.induction_on with
    | empty => simp
    | @insert i s hi ih =>
      simp only [Finset.sum_insert hi, Finset.prod_insert hi, chi.map_add_eq_mul, ih]
  rw [← hsum Finset.univ, hs, chi.map_zero_eq_one]

/-- The central phase hypothesis of quotient_coset_output is discharged by
the full vector SDE. Unit scales are precisely the active-target interface. -/
theorem scalar_quotient_coset_output {G Q : Type*} [Group G] [Group Q]
    [Fintype G] [Fintype Q] [Fintype V] [Nonempty I]
    (pi : G →* Q) (embed : Multiplicative V →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : AddChar F ℂ) (labels : I → V →ₗ[F] F)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry H embed (labelCharacter chi (labels i)) x x) ≠ 0)
    (A : I → G ≃* G) (scales : I → Fˣ) (d : ℕ)
    (preserves : ∀ i g, A i g ∈ H ↔ g ∈ H)
    (on_center : ∀ i z, A i (embed (Multiplicative.ofAdd z)) =
      embed (Multiplicative.ofAdd (((scales i : F) ^ d) • z)))
    (sde : ∑ i, (scales i : F) ^ d • labels i = 0) (q r : Q) :
    actionOutput (fun x i => A i (representative x))
      (fun x y : I → G =>
        ∏ i, normalizedEntry H embed (labelCharacter chi (labels i)) (x i) (y i)) q r =
        QSearch.CosetSourceFourier.groupEntry (H.map pi) q r := by
  apply quotient_coset_output pi embed kernel central H representative section_law
    (fun i => labelCharacter chi (labels i))
    (fun i => (nonzero_branch_iff_allowed H embed (labelCharacter chi (labels i))).mp
      (nonzero_trace i))
    A (fun i => scalarAutomorphism (scales i ^ d)) preserves
  · intro i z
    simpa [scalarAutomorphism] using on_center i z.toAdd
  · intro z
    simpa [labelCharacter, scalarAutomorphism] using
      sde_character_cancellation chi d labels (fun i => (scales i : F)) sde z.toAdd

end ScalarLabels

end
end QSearch.CentralQuotientReceiver

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_character_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_character_sum

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_coefficient' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_coefficient

/-- info: 'QSearch.CentralQuotientReceiver.disallowed_projected_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.disallowed_projected_source

/-- info: 'QSearch.CentralQuotientReceiver.nonzero_branch_iff_allowed' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.nonzero_branch_iff_allowed

/-- info: 'QSearch.CentralQuotientReceiver.quotient_membership' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.quotient_membership

/-- info: 'QSearch.CentralQuotientReceiver.dilation_preserves_saturation' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.dilation_preserves_saturation

/-- info: 'QSearch.CentralQuotientReceiver.cancelled_normalized_correlation' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.cancelled_normalized_correlation

/-- info: 'QSearch.CentralQuotientReceiver.quotient_coset_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.quotient_coset_output

/-- info: 'QSearch.CentralQuotientReceiver.active_sde' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.active_sde

/-- info: 'QSearch.CentralQuotientReceiver.active_nonempty' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.active_nonempty

/-- info: 'QSearch.CentralQuotientReceiver.sde_character_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.sde_character_cancellation

/-- info: 'QSearch.CentralQuotientReceiver.scalar_quotient_coset_output' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralQuotientReceiver.scalar_quotient_coset_output
