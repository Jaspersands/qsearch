import Formal.CentralQuotientReceiver

/-!
# All-record central descent with inactive targets retained

Zero scales act trivially on their targets, which are still consumed and
traced out. An unnormalized branch identity keeps its actual probability;
zero-mass records never require division by zero. Source banks are explicit
independent tensors, not merely states with the right marginals.
-/

namespace QSearch.CentralDescentRecords

open scoped BigOperators
open QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver
open QSearch.AffineSupportErasure (invSize)

noncomputable section
attribute [local instance] Classical.propDecidable

section TensorMeasurement
variable {I G : Type*} [Fintype I] [Fintype G]

def tensorMatrix (M : I → Matrix G G ℂ) : Matrix (I → G) (I → G) ℂ :=
  fun x y => ∏ i, M i (x i) (y i)

/-- Literal two-sided product-Kraus action on an independent tensor.
It is not valid for an arbitrary correlated bank with the same marginals. -/
theorem tensor_two_sided (K rho : I → Matrix G G ℂ) :
    tensorMatrix K * tensorMatrix rho * (tensorMatrix K).conjTranspose =
      tensorMatrix (fun i => K i * rho i * (K i).conjTranspose) := by
  ext a b
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, tensorMatrix,
    Finset.sum_mul, star_prod, ← Finset.prod_mul_distrib]
  have hi (y : I → G) :
      (∑ x : I → G, ∏ i, K i (a i) (x i) * rho i (x i) (y i) *
        star (K i (b i) (y i))) =
      ∏ i, ∑ x : G, K i (a i) x * rho i x (y i) * star (K i (b i) (y i)) :=
    (Fintype.prod_sum (fun i x =>
      K i (a i) x * rho i x (y i) * star (K i (b i) (y i)))).symm
  simp_rw [hi]
  exact (Fintype.prod_sum (fun i y =>
    ∑ x : G, K i (a i) x * rho i x y * star (K i (b i) y))).symm

end TensorMeasurement

section Source
variable {G C : Type*} [Group G] [CommGroup C] [Fintype G] [Fintype C]

def branchMass (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ) : ℂ :=
  ∑ x, projectedEntry H embed chi x x

theorem zero_mass_source (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (hz : branchMass H embed chi = 0) (x y : G) :
    projectedEntry H embed chi x y = 0 := by
  have hn : ¬ ∀ z, embed z ∈ H → chi z = 1 := by
    intro h
    exact label_probability_allowed_ne_zero H embed chi h hz
  push Not at hn
  obtain ⟨z, hz, hchi⟩ := hn
  exact disallowed_projected_source H embed chi z hz hchi x y

theorem projected_mass_normalized (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (x y : G) :
    projectedEntry H embed chi x y =
      branchMass H embed chi * normalizedEntry H embed chi x y := by
  by_cases hz : branchMass H embed chi = 0
  · simp [hz, zero_mass_source H embed chi hz]
  · have ha := (nonzero_branch_iff_allowed H embed chi).mp hz
    rw [normalized_source H embed chi ha]
    change _ = branchMass H embed chi * (_ / branchMass H embed chi)
    field_simp

end Source

section Scalar
variable {F V I G Q : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Group G] [Group Q] [Fintype I] [Fintype G] [Fintype Q] [Fintype V]

/-- Inactive targets receive the identity, NOT a nonexistent zero dilation. -/
def paddedAction (A : Fˣ → G ≃* G) (scales : I → F)
    (representative : Q → G) (q : Q) (i : I) : G :=
  if h : scales i = 0 then 1 else A (Units.mk0 (scales i) h) (representative q)

omit [Group Q] [Fintype I] [Fintype G] [Fintype Q] in
theorem padded_relative (A : Fˣ → G ≃* G) (scales : I → F)
    (representative : Q → G) (q r : Q) (i : I) :
    (paddedAction A scales representative r i)⁻¹ *
      paddedAction A scales representative q i =
      if h : scales i = 0 then 1 else
        A (Units.mk0 (scales i) h) ((representative r)⁻¹ * representative q) := by
  by_cases h : scales i = 0 <;> simp [paddedAction, h]

theorem normalized_padded_correlation
    (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (labels : I → V →ₗ[F] F)
    (allowed : ∀ i z, embed z ∈ H → labelCharacter chi (labels i) z = 1)
    (A : Fˣ → G ≃* G) (d : ℕ) (positive : 0 < d)
    (preserves : ∀ u g, A u g ∈ H ↔ g ∈ H)
    (on_center : ∀ u z, A u (embed (Multiplicative.ofAdd z)) =
      embed (Multiplicative.ofAdd (((u : F) ^ d) • z)))
    (scales : I → F) (active : ∃ i, scales i ≠ 0)
    (sde : ∑ i, scales i ^ d • labels i = 0) (g : G) :
    (∏ i, rightCorrelation (normalizedEntry H embed (labelCharacter chi (labels i)))
      (if h : scales i = 0 then 1 else A (Units.mk0 (scales i) h) g)) =
      if g ∈ H ⊔ embed.range then 1 else 0 := by
  have hc (u : Fˣ) (z : Multiplicative V) : A u (embed z) =
      embed (Multiplicative.ofAdd (((u : F) ^ d) • z.toAdd)) := on_center u z.toAdd
  by_cases hg : g ∈ H ⊔ embed.range
  · rw [ite_eq_left hg]
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central g).mp hg
    have hi (i : I) :
        rightCorrelation (normalizedEntry H embed (labelCharacter chi (labels i)))
          (if h : scales i = 0 then 1 else A (Units.mk0 (scales i) h) g) =
        chi (labels i (scales i ^ d • z.toAdd)) := by
      by_cases h : scales i = 0
      · simp only [h, zero_pow (Nat.ne_of_gt positive), zero_smul,
          map_zero, chi.map_zero_eq_one]
        simpa [rightCorrelation] using normalized_trace H embed
          (labelCharacter chi (labels i)) (allowed i)
      · simp only [dite_eq_right h]
        have ht := normalized_correlation_at H embed (labelCharacter chi (labels i))
          (allowed i) (A (Units.mk0 (scales i) h) (g * (embed z)⁻¹))
          ((preserves _ _).mpr hz)
          (Multiplicative.ofAdd (scales i ^ d • z.toAdd))
        simpa [hc, labelCharacter] using ht
    simpa only [hi] using sde_character_cancellation chi d labels scales sde z.toAdd
  · rw [ite_eq_right hg]
    obtain ⟨i, hi⟩ := active
    apply Finset.prod_eq_zero (Finset.mem_univ i)
    simp only [dite_eq_right hi]
    apply normalized_correlation_off
    intro z hz
    apply hg
    apply (dilation_preserves_saturation H embed central
      (A (Units.mk0 (scales i) hi))
      (scalarAutomorphism ((Units.mk0 (scales i) hi) ^ d))
      (preserves _) (by
        intro v
        simpa [scalarAutomorphism] using (hc (Units.mk0 (scales i) hi) v)) g).mp
    exact (mem_saturation_iff H embed central _).mpr ⟨z, hz⟩

theorem normalized_padded_output
    (pi : G →* Q) (embed : Multiplicative V →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : AddChar F ℂ) (labels : I → V →ₗ[F] F)
    (allowed : ∀ i z, embed z ∈ H → labelCharacter chi (labels i) z = 1)
    (A : Fˣ → G ≃* G) (d : ℕ) (positive : 0 < d)
    (preserves : ∀ u g, A u g ∈ H ↔ g ∈ H)
    (on_center : ∀ u z, A u (embed (Multiplicative.ofAdd z)) =
      embed (Multiplicative.ofAdd (((u : F) ^ d) • z)))
    (scales : I → F) (active : ∃ i, scales i ≠ 0)
    (sde : ∑ i, scales i ^ d • labels i = 0) (q r : Q) :
    actionOutput (paddedAction A scales representative)
      (fun x y : I → G => ∏ i,
        normalizedEntry H embed (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (H.map pi) q r := by
  rw [action_output, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply, padded_relative]
  rw [normalized_padded_correlation H embed central chi labels allowed A d positive
    preserves on_center scales active sde]
  rw [← quotient_membership pi embed kernel central H]
  simp only [map_mul, map_inv, section_law]
  have he : r⁻¹ * q ∈ H.map pi ↔ q⁻¹ * r ∈ H.map pi := by
    rw [show r⁻¹ * q = (q⁻¹ * r)⁻¹ by group, Subgroup.inv_mem_iff]
  rw [he]
  simp only [CosetSourceFourier.groupEntry, mul_ite, mul_one, mul_zero]

/-- All measured records, including impossible records and zero scales.
Every target is retained in the input tensor and consumed by actionOutput.
No positive-probability or admissible-label premise is needed. -/
theorem all_record_output
    (pi : G →* Q) (embed : Multiplicative V →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : AddChar F ℂ) (labels : I → V →ₗ[F] F)
    (A : Fˣ → G ≃* G) (d : ℕ) (positive : 0 < d)
    (preserves : ∀ u g, A u g ∈ H ↔ g ∈ H)
    (on_center : ∀ u z, A u (embed (Multiplicative.ofAdd z)) =
      embed (Multiplicative.ofAdd (((u : F) ^ d) • z)))
    (scales : I → F) (active : ∃ i, scales i ≠ 0)
    (sde : ∑ i, scales i ^ d • labels i = 0) (q r : Q) :
    actionOutput (paddedAction A scales representative)
      (fun x y : I → G => ∏ i,
        projectedEntry H embed (labelCharacter chi (labels i)) (x i) (y i)) q r =
      (∏ i, branchMass H embed (labelCharacter chi (labels i))) *
        CosetSourceFourier.groupEntry (H.map pi) q r := by
  by_cases hp : ∀ i, branchMass H embed (labelCharacter chi (labels i)) ≠ 0
  · have ha (i : I) :=
      (nonzero_branch_iff_allowed H embed (labelCharacter chi (labels i))).mp (hp i)
    have ht := normalized_padded_output pi embed kernel central H representative section_law
      chi labels ha A d positive preserves on_center scales active sde q r
    rw [action_output, tensor_correlation] at ht ⊢
    have hc (i : I) (g : G) :
        rightCorrelation (projectedEntry H embed (labelCharacter chi (labels i))) g =
        branchMass H embed (labelCharacter chi (labels i)) *
          rightCorrelation (normalizedEntry H embed (labelCharacter chi (labels i))) g := by
      simp only [rightCorrelation, projected_mass_normalized, Finset.mul_sum]
    simp_rw [hc]
    rw [Finset.prod_mul_distrib]
    rw [← mul_assoc, mul_comm (invSize Q), mul_assoc, ht]
  · push Not at hp
    obtain ⟨i, hi⟩ := hp
    have hs (x y : I → G) :
        (∏ j, projectedEntry H embed (labelCharacter chi (labels j)) (x j) (y j)) = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i)
        (zero_mass_source H embed (labelCharacter chi (labels i)) hi (x i) (y i))
    have hm : (∏ j, branchMass H embed (labelCharacter chi (labels j))) = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) hi
    simp only [actionOutput, hs, hm, mul_zero, zero_mul, Finset.sum_const_zero]

end Scalar
end
end QSearch.CentralDescentRecords

/-- info: 'QSearch.CentralDescentRecords.tensor_two_sided' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.tensor_two_sided

/-- info: 'QSearch.CentralDescentRecords.zero_mass_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.zero_mass_source

/-- info: 'QSearch.CentralDescentRecords.projected_mass_normalized' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.projected_mass_normalized

/-- info: 'QSearch.CentralDescentRecords.padded_relative' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.padded_relative

/-- info: 'QSearch.CentralDescentRecords.normalized_padded_correlation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.normalized_padded_correlation

/-- info: 'QSearch.CentralDescentRecords.normalized_padded_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.normalized_padded_output

/-- info: 'QSearch.CentralDescentRecords.all_record_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentRecords.all_record_output
