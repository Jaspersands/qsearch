import Formal.CentralDescentRecords
import Formal.CentralSpectralProjector

/-!
# Finite central descent policies

Active slots may have different automorphisms of an arbitrary finite central
abelian group. Inactive targets remain in the independent input tensor and are
traced with the active targets. Records of zero mass are not removed.

The policy results are matrix-entry and trace identities. They do not extract
a positive/CPTP instrument, a mixed-ring character compiler, or a terminating
solver, and do not establish IID physics or source ownership. Completeness of
a supplied measured-label family is explicit in the abstract policy results;
the full-dual section proves it for the actual central-ancilla measurement
on an independent coset tensor over any finite additive abelian center.
Weighting a packet by a classical choice probability models label-only
processing with private randomness, not correlated auxiliary quantum advice.
-/

namespace QSearch.CentralDescentPolicy

open scoped BigOperators
open QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver
open QSearch.CentralDescentRecords (branchMass projected_mass_normalized zero_mass_source
  tensorMatrix)
open QSearch.AffineSupportErasure (invSize)

noncomputable section
attribute [local instance] Classical.propDecidable

section Witness
variable (I G C : Type*) [Group G] [CommGroup C]

structure Witness where
  active : Finset I
  action : I → G ≃* G
  scale : I → C ≃* C

variable {I G C}

/-- Only active automorphisms require compatibility with the hidden subgroup. -/
def Witness.Valid (w : Witness I G C) (H : Subgroup G) (embed : C →* G)
    (chi : I → C →* ℂ) : Prop :=
  w.active.Nonempty ∧
  (∀ i ∈ w.active, ∀ g, w.action i g ∈ H ↔ g ∈ H) ∧
  (∀ i ∈ w.active, ∀ z, w.action i (embed z) = embed (w.scale i z)) ∧
  (∀ z, ∏ i ∈ w.active, chi i (w.scale i z) = 1)

def paddedAction {Q : Type*} (w : Witness I G C) (representative : Q → G)
    (q : Q) (i : I) : G :=
  if i ∈ w.active then w.action i (representative q) else 1

theorem padded_relative {Q : Type*} (w : Witness I G C)
    (representative : Q → G) (q r : Q) (i : I) :
    (paddedAction w representative r i)⁻¹ * paddedAction w representative q i =
      if i ∈ w.active then w.action i ((representative r)⁻¹ * representative q) else 1 := by
  by_cases hi : i ∈ w.active <;> simp [paddedAction, hi]

end Witness

section Descent
variable {I G C Q : Type*} [Fintype I] [Group G] [CommGroup C]
  [Fintype G] [Fintype C]

def packet (H : Subgroup G) (embed : C →* G) (chi : I → C →* ℂ) :
    Matrix (I → G) (I → G) ℂ :=
  tensorMatrix (fun i => projectedEntry H embed (chi i))

def packetMass (H : Subgroup G) (embed : C →* G) (chi : I → C →* ℂ) : ℂ :=
  ∏ i, branchMass H embed (chi i)

theorem packet_trace (H : Subgroup G) (embed : C →* G) (chi : I → C →* ℂ) :
    (∑ x, packet H embed chi x x) = packetMass H embed chi :=
  (Fintype.prod_sum (fun i x => projectedEntry H embed (chi i) x x)).symm

theorem normalized_padded_correlation
    (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : I → C →* ℂ) (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (w : Witness I G C) (valid : w.Valid H embed chi) (g : G) :
    (∏ i, rightCorrelation (normalizedEntry H embed (chi i))
      (if i ∈ w.active then w.action i g else 1)) =
      if g ∈ H ⊔ embed.range then 1 else 0 := by
  obtain ⟨active, preserves, on_center, cancel⟩ := valid
  by_cases hg : g ∈ H ⊔ embed.range
  · rw [ite_eq_left hg]
    obtain ⟨z, hz⟩ := (mem_saturation_iff H embed central g).mp hg
    have hi (i : I) :
        rightCorrelation (normalizedEntry H embed (chi i))
          (if i ∈ w.active then w.action i g else 1) =
        if i ∈ w.active then chi i (w.scale i z) else 1 := by
      by_cases h : i ∈ w.active
      · simp only [ite_eq_left h]
        have ht := normalized_correlation_at H embed (chi i) (allowed i)
          (w.action i (g * (embed z)⁻¹)) ((preserves i h _).mpr hz) (w.scale i z)
        simpa [on_center i h] using ht
      · simpa [h, rightCorrelation] using normalized_trace H embed (chi i) (allowed i)
    simpa only [hi, Finset.prod_ite_mem, Finset.univ_inter] using cancel z
  · rw [ite_eq_right hg]
    obtain ⟨i, hi⟩ := active
    apply Finset.prod_eq_zero (Finset.mem_univ i)
    simp only [ite_eq_left hi]
    apply normalized_correlation_off
    intro z hz
    apply hg
    apply (dilation_preserves_saturation H embed central (w.action i) (w.scale i)
      (preserves i hi) (on_center i hi) g).mp
    exact (mem_saturation_iff H embed central _).mpr ⟨z, hz⟩

variable [Group Q] [Fintype Q]

theorem normalized_padded_output
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : I → C →* ℂ) (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (w : Witness I G C) (valid : w.Valid H embed chi) (q r : Q) :
    actionOutput (paddedAction w representative)
      (fun x y : I → G => ∏ i, normalizedEntry H embed (chi i) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (H.map pi) q r := by
  rw [action_output, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply, padded_relative]
  rw [normalized_padded_correlation H embed central chi allowed w valid]
  rw [← quotient_membership pi embed kernel central H]
  simp only [map_mul, map_inv, section_law]
  have he : r⁻¹ * q ∈ H.map pi ↔ q⁻¹ * r ∈ H.map pi := by
    rw [show r⁻¹ * q = (q⁻¹ * r)⁻¹ by group, Subgroup.inv_mem_iff]
  rw [he]
  simp only [CosetSourceFourier.groupEntry, mul_ite, mul_one, mul_zero]

/-- No admissibility or positive-mass premise, including on inactive slots. -/
theorem all_record_output
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : I → C →* ℂ) (w : Witness I G C) (valid : w.Valid H embed chi) (q r : Q) :
    actionOutput (paddedAction w representative) (packet H embed chi) q r =
      packetMass H embed chi * CosetSourceFourier.groupEntry (H.map pi) q r := by
  by_cases hp : ∀ i, branchMass H embed (chi i) ≠ 0
  · have ha (i : I) := (nonzero_branch_iff_allowed H embed (chi i)).mp (hp i)
    have ht := normalized_padded_output pi embed kernel central H representative section_law
      chi ha w valid q r
    change actionOutput (paddedAction w representative)
      (fun x y : I → G => ∏ i, projectedEntry H embed (chi i) (x i) (y i)) q r = _
    rw [action_output, tensor_correlation] at ht ⊢
    have hc (i : I) (g : G) :
        rightCorrelation (projectedEntry H embed (chi i)) g =
        branchMass H embed (chi i) * rightCorrelation (normalizedEntry H embed (chi i)) g := by
      simp only [rightCorrelation, projected_mass_normalized, Finset.mul_sum]
    simp_rw [hc]
    rw [Finset.prod_mul_distrib]
    rw [← mul_assoc, mul_comm (invSize Q), mul_assoc, ht]
    rfl
  · push Not at hp
    obtain ⟨i, hi⟩ := hp
    have hs (x y : I → G) : packet H embed chi x y = 0 :=
      Finset.prod_eq_zero (Finset.mem_univ i) (zero_mass_source H embed (chi i) hi (x i) (y i))
    have hm : packetMass H embed chi = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hi
    simp only [actionOutput, hs, hm, mul_zero, zero_mul, Finset.sum_const_zero]

end Descent

section FiniteRecords
variable {R T : Type*} [Fintype R] [Fintype T]

/-- Algebraic weights; stochastic choice weights are supplied below. -/
def selectedMass (accept : R → Prop) (weight mass : R → ℂ) : ℂ :=
  ∑ record, if accept record then weight record * mass record else 0

def discardedOutput (accept : R → Prop) (weight : R → ℂ)
    (rho : R → Matrix T T ℂ) : ℂ :=
  ∑ record, if accept record then 0 else weight record * ∑ x, rho record x x

theorem discarded_output_eq (accept : R → Prop) (weight : R → ℂ)
    (rho : R → Matrix T T ℂ) :
    discardedOutput accept weight rho =
      selectedMass (fun record => ¬ accept record) weight (fun record => ∑ x, rho record x x) := by
  simp only [discardedOutput, selectedMass, ite_not]

omit [Fintype T] in
theorem selected_mass_partition (accept : R → Prop) (weight mass : R → ℂ) :
    selectedMass accept weight mass + selectedMass (fun record => ¬ accept record) weight mass =
      ∑ record, weight record * mass record := by
  rw [selectedMass, selectedMass, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro record _
  by_cases h : accept record <;> simp [h]

end FiniteRecords

section AcceptedRecords
variable {R I G C Q : Type*} [Fintype R] [Fintype I] [Group G] [CommGroup C]
  [Group Q] [Fintype G] [Fintype C] [Fintype Q]

def acceptedOutput (H : Subgroup G) (embed : C →* G) (representative : Q → G)
    (chi : R → I → C →* ℂ) (w : R → Witness I G C)
    (accept : R → Prop) (weight : R → ℂ) (q r : Q) : ℂ :=
  ∑ record, if accept record then weight record *
    actionOutput (paddedAction (w record) representative) (packet H embed (chi record)) q r else 0

/-- Validity is required only for accepted records, even if their mass is zero. -/
theorem accepted_output_factorization
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : R → I → C →* ℂ) (w : R → Witness I G C)
    (accept : R → Prop) (weight : R → ℂ)
    (valid : ∀ record, accept record → (w record).Valid H embed (chi record)) (q r : Q) :
    acceptedOutput H embed representative chi w accept weight q r =
      selectedMass accept weight (fun record => packetMass H embed (chi record)) *
        CosetSourceFourier.groupEntry (H.map pi) q r := by
  rw [acceptedOutput, selectedMass, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro record _
  by_cases h : accept record
  · simp only [ite_eq_left h]
    rw [all_record_output pi embed kernel central H representative section_law
      (chi record) (w record) (valid record h), mul_assoc]
  · simp [h]

theorem accepted_output_trace
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : R → I → C →* ℂ) (w : R → Witness I G C)
    (accept : R → Prop) (weight : R → ℂ)
    (valid : ∀ record, accept record → (w record).Valid H embed (chi record)) :
    (∑ q, acceptedOutput H embed representative chi w accept weight q q) =
      selectedMass accept weight (fun record => packetMass H embed (chi record)) := by
  simp_rw [accepted_output_factorization pi embed kernel central H representative section_law
    chi w accept weight valid]
  rw [← Finset.mul_sum]
  have hn : (Fintype.card Q : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [CosetSourceFourier.groupEntry, invSize, hn]

omit [Group Q] [Fintype Q] in
theorem abort_output_factorization
    (H : Subgroup G) (embed : C →* G) (chi : R → I → C →* ℂ)
    (accept : R → Prop) (weight : R → ℂ) :
    discardedOutput accept weight (fun record => packet H embed (chi record)) =
      selectedMass (fun record => ¬ accept record) weight
        (fun record => packetMass H embed (chi record)) := by
  rw [discarded_output_eq]
  simp_rw [packet_trace]

omit [Group Q] [Fintype Q] in
/-- The right side is the trace of the entire weighted projected-record input. -/
theorem accepted_abort_mass_conservation
    (H : Subgroup G) (embed : C →* G) (chi : R → I → C →* ℂ)
    (accept : R → Prop) (weight : R → ℂ) :
    selectedMass accept weight (fun record => packetMass H embed (chi record)) +
      discardedOutput accept weight (fun record => packet H embed (chi record)) =
      ∑ x, ∑ record, weight record * packet H embed (chi record) x x := by
  rw [abort_output_factorization, selected_mass_partition, Finset.sum_comm]
  simp_rw [← Finset.mul_sum, packet_trace]

/-- Trace conservation for the computed accepted matrix and discarded scalar. -/
theorem accepted_abort_trace_conservation
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : R → I → C →* ℂ) (w : R → Witness I G C)
    (accept : R → Prop) (weight : R → ℂ)
    (valid : ∀ record, accept record → (w record).Valid H embed (chi record)) :
    (∑ q, acceptedOutput H embed representative chi w accept weight q q) +
      discardedOutput accept weight (fun record => packet H embed (chi record)) =
      ∑ x, ∑ record, weight record * packet H embed (chi record) x x := by
  rw [accepted_output_trace pi embed kernel central H representative section_law
    chi w accept weight valid]
  exact accepted_abort_mass_conservation H embed chi accept weight

end AcceptedRecords

section RandomizedPolicy
variable {L W : Type*} [Fintype L] [Fintype W]

/-- Conditional choice probabilities may depend on the entire measured label. -/
structure ChoicePolicy (L W : Type*) [Fintype W] where
  weight : L → W → ℝ
  nonnegative : ∀ label choice, 0 ≤ weight label choice
  normalized : ∀ label, ∑ choice, weight label choice = 1

def ChoicePolicy.recordWeight (policy : ChoicePolicy L W) (record : L × W) : ℂ :=
  policy.weight record.1 record.2

theorem randomized_record_sum (policy : ChoicePolicy L W) (f : L → ℂ) :
    (∑ record : L × W, policy.recordWeight record * f record.1) = ∑ label, f label := by
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro label _
  simp only [ChoicePolicy.recordWeight, ← Finset.sum_mul, ← Complex.ofReal_sum,
    policy.normalized, Complex.ofReal_one, one_mul]

variable {I G C : Type*} [Fintype I] [Group G] [CommGroup C] [Fintype G] [Fintype C]

/-- Use R = L x W in accepted_output_factorization. Witnesses and acceptance
may depend on both measured labels and the extra policy choice. -/
theorem randomized_mass_conservation
    (H : Subgroup G) (embed : C →* G) (chi : L → I → C →* ℂ)
    (policy : ChoicePolicy L W) (accept : L × W → Prop) :
    selectedMass accept policy.recordWeight (fun record => packetMass H embed (chi record.1)) +
      discardedOutput accept policy.recordWeight (fun record => packet H embed (chi record.1)) =
      ∑ label, packetMass H embed (chi label) := by
  rw [abort_output_factorization, selected_mass_partition]
  exact randomized_record_sum policy (fun label => packetMass H embed (chi label))

/-- Completeness is an input-ensemble premise, never the desired output identity. -/
theorem randomized_mass_conservation_of_complete
    (H : Subgroup G) (embed : C →* G) (chi : L → I → C →* ℂ)
    (policy : ChoicePolicy L W) (accept : L × W → Prop)
    (input : Matrix (I → G) (I → G) ℂ)
    (complete : ∀ x y, ∑ label, packet H embed (chi label) x y = input x y) :
    selectedMass accept policy.recordWeight (fun record => packetMass H embed (chi record.1)) +
      discardedOutput accept policy.recordWeight (fun record => packet H embed (chi record.1)) =
      ∑ x, input x x := by
  rw [randomized_mass_conservation]
  simp_rw [← packet_trace]
  rw [Finset.sum_comm]
  simp_rw [complete]

theorem randomized_output_trace_conservation
    {Q : Type*} [Group Q] [Fintype Q]
    (pi : G →* Q) (embed : C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (chi : L → I → C →* ℂ) (w : L × W → Witness I G C)
    (policy : ChoicePolicy L W) (accept : L × W → Prop)
    (valid : ∀ record, accept record → (w record).Valid H embed (chi record.1))
    (input : Matrix (I → G) (I → G) ℂ)
    (complete : ∀ x y, ∑ label, packet H embed (chi label) x y = input x y) :
    (∑ q, acceptedOutput H embed representative (fun record => chi record.1) w
      accept policy.recordWeight q q) +
      discardedOutput accept policy.recordWeight (fun record => packet H embed (chi record.1)) =
      ∑ x, input x x := by
  rw [accepted_output_trace pi embed kernel central H representative section_law
    (fun record => chi record.1) w accept policy.recordWeight valid]
  exact randomized_mass_conservation_of_complete H embed chi policy accept input complete

end RandomizedPolicy

section FullDualMeasurement
variable {I G C : Type*} [Fintype I] [Group G] [AddCommGroup C]
  [Fintype G] [Fintype C]

open QSearch.CentralSpectralProjector

/-- Actual product ancilla-Kraus branch on supplied independent copies of rho.
The operation takes no hidden subgroup; tensoring rho is not a cloning map.
This full-dual definition does not provide an efficient character compiler. -/
def measuredBank (embed : Multiplicative C →* G) (labels : I → AddChar C ℂ)
    (rho : Matrix G G ℂ) : Matrix (I → G) (I → G) ℂ :=
  let K := tensorMatrix (fun i => ancillaKraus embed (labels i))
  K * tensorMatrix (fun _ : I => rho) * K.conjTranspose

/-- Every label record, including zero-mass records, is a literal Kraus branch. -/
theorem measured_bank_eq_packet (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (labels : I → AddChar C ℂ) :
    measuredBank embed labels (Matrix.of (CosetSourceFourier.groupEntry H)) =
      packet H embed (fun i => (labels i).toMonoidHom) := by
  unfold measuredBank
  rw [CentralDescentRecords.tensor_two_sided]
  ext x y
  unfold tensorMatrix packet
  apply Finset.prod_congr rfl
  intro i _
  exact ancilla_source H embed central (labels i) (x i) (y i)

omit [Fintype I] in
/-- Full-dual completeness of the one-sided projected source needs no centrality. -/
theorem projected_sum (H : Subgroup G) (embed : Multiplicative C →* G) (x y : G) :
    (∑ chi : AddChar C ℂ, projectedEntry H embed chi.toMonoidHom x y) =
      CosetSourceFourier.groupEntry H x y := by
  have hs : (∑ chi : AddChar C ℂ,
      projector embed chi * Matrix.of (CosetSourceFourier.groupEntry H)) =
      Matrix.of (CosetSourceFourier.groupEntry H) := by
    rw [← Finset.sum_mul, projector_sum, one_mul]
  simpa only [Matrix.sum_apply, projector_mul_source, Matrix.of_apply] using
    congrArg (fun M : Matrix G G ℂ => M x y) hs

/-- All full-dual records sum to the original independent tensor, without filtering. -/
theorem packet_sum (H : Subgroup G) (embed : Multiplicative C →* G) (x y : I → G) :
    (∑ labels : I → AddChar C ℂ, packet H embed (fun i => (labels i).toMonoidHom) x y) =
      tensorMatrix (fun _ : I => Matrix.of (CosetSourceFourier.groupEntry H)) x y := by
  calc
    _ = ∏ i, ∑ chi : AddChar C ℂ, projectedEntry H embed chi.toMonoidHom (x i) (y i) :=
      (Fintype.prod_sum (fun (i : I) (chi : AddChar C ℂ) =>
        projectedEntry H embed chi.toMonoidHom (x i) (y i))).symm
    _ = _ := by simp only [projected_sum, tensorMatrix, Matrix.of_apply]

omit [AddCommGroup C] [Fintype C] in
theorem independent_source_trace (H : Subgroup G) :
    (∑ x : I → G,
      tensorMatrix (fun _ : I => Matrix.of (CosetSourceFourier.groupEntry H)) x x) = 1 := by
  calc
    _ = ∏ _i : I, ∑ x : G, CosetSourceFourier.groupEntry H x x :=
      (Fintype.prod_sum (fun (_i : I) (x : G) =>
        CosetSourceFourier.groupEntry H x x)).symm
    _ = 1 := by
      have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
      simp [CosetSourceFourier.groupEntry, invSize, hn]

/-- Forgetting the measured labels preserves this source, not arbitrary input matrices. -/
theorem measured_bank_sum (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) :
    (∑ labels : I → AddChar C ℂ,
      measuredBank embed labels (Matrix.of (CosetSourceFourier.groupEntry H))) =
      tensorMatrix (fun _ : I => Matrix.of (CosetSourceFourier.groupEntry H)) := by
  ext x y
  simp only [Matrix.sum_apply, measured_bank_eq_packet H embed central]
  exact packet_sum H embed x y

theorem measured_bank_mass_sum (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) :
    (∑ labels : I → AddChar C ℂ, ∑ x,
      measuredBank embed labels (Matrix.of (CosetSourceFourier.groupEntry H)) x x) = 1 := by
  rw [Finset.sum_comm]
  simp_rw [measured_bank_eq_packet H embed central, packet_sum]
  exact independent_source_trace H

variable {Q W : Type*} [Group Q] [Fintype Q] [Fintype W]

/-- Label-only policy with private classical coins acting on actual measured matrices.
This does not model auxiliary information correlated with the residual source. -/
def measuredAcceptedOutput (embed : Multiplicative C →* G) (representative : Q → G)
    (w : (I → AddChar C ℂ) × W → Witness I G (Multiplicative C))
    (policy : ChoicePolicy (I → AddChar C ℂ) W)
    (accept : (I → AddChar C ℂ) × W → Prop) (rho : Matrix G G ℂ) (q r : Q) : ℂ :=
  ∑ record, if accept record then policy.recordWeight record *
    actionOutput (paddedAction (w record) representative) (measuredBank embed record.1 rho) q r
    else 0

/-- The selected mass is the trace of the actual measured branches, including zero mass. -/
theorem measured_accepted_output_factorization
    (pi : G →* Q) (embed : Multiplicative C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (w : (I → AddChar C ℂ) × W → Witness I G (Multiplicative C))
    (policy : ChoicePolicy (I → AddChar C ℂ) W)
    (accept : (I → AddChar C ℂ) × W → Prop)
    (valid : ∀ record, accept record →
      (w record).Valid H embed (fun i => (record.1 i).toMonoidHom)) (q r : Q) :
    measuredAcceptedOutput embed representative w policy accept
      (Matrix.of (CosetSourceFourier.groupEntry H)) q r =
      selectedMass accept policy.recordWeight (fun record => ∑ x,
        measuredBank embed record.1 (Matrix.of (CosetSourceFourier.groupEntry H)) x x) *
      CosetSourceFourier.groupEntry (H.map pi) q r := by
  unfold measuredAcceptedOutput
  simp_rw [measured_bank_eq_packet H embed central, packet_trace]
  simpa only [acceptedOutput] using
    (accepted_output_factorization pi embed kernel central H representative section_law
      (fun (record : (I → AddChar C ℂ) × W) i => (record.1 i).toMonoidHom)
      w accept policy.recordWeight valid q r)

/-- Computed accepted and abort outputs have total trace one. Completeness follows
from the full dual and the independent coset source, not an additional premise. -/
theorem measured_randomized_output_trace_conservation
    (pi : G →* Q) (embed : Multiplicative C →* G) (kernel : pi.ker = embed.range)
    (central : ∀ z g, embed z * g = g * embed z)
    (H : Subgroup G) (representative : Q → G)
    (section_law : ∀ q, pi (representative q) = q)
    (w : (I → AddChar C ℂ) × W → Witness I G (Multiplicative C))
    (policy : ChoicePolicy (I → AddChar C ℂ) W)
    (accept : (I → AddChar C ℂ) × W → Prop)
    (valid : ∀ record, accept record →
      (w record).Valid H embed (fun i => (record.1 i).toMonoidHom)) :
    (∑ q, measuredAcceptedOutput embed representative w policy accept
      (Matrix.of (CosetSourceFourier.groupEntry H)) q q) +
      discardedOutput accept policy.recordWeight (fun record =>
        measuredBank embed record.1 (Matrix.of (CosetSourceFourier.groupEntry H))) = 1 := by
  have ht := randomized_output_trace_conservation pi embed kernel central H representative
    section_law (fun labels i => (labels i).toMonoidHom) w policy accept valid
    (tensorMatrix (fun _ : I => Matrix.of (CosetSourceFourier.groupEntry H)))
    (packet_sum H embed)
  rw [independent_source_trace] at ht
  simpa only [measuredAcceptedOutput, measured_bank_eq_packet H embed central,
    acceptedOutput] using ht

end FullDualMeasurement
end
end QSearch.CentralDescentPolicy

/-- info: 'QSearch.CentralDescentPolicy.padded_relative' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.padded_relative

/-- info: 'QSearch.CentralDescentPolicy.packet_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.packet_trace

/-- info: 'QSearch.CentralDescentPolicy.normalized_padded_correlation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.normalized_padded_correlation

/-- info: 'QSearch.CentralDescentPolicy.normalized_padded_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.normalized_padded_output

/-- info: 'QSearch.CentralDescentPolicy.all_record_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.all_record_output

/-- info: 'QSearch.CentralDescentPolicy.discarded_output_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.discarded_output_eq

/-- info: 'QSearch.CentralDescentPolicy.selected_mass_partition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.selected_mass_partition

/-- info: 'QSearch.CentralDescentPolicy.accepted_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.accepted_output_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_output_trace

/-- info: 'QSearch.CentralDescentPolicy.abort_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.abort_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.accepted_abort_mass_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_abort_mass_conservation

/-- info: 'QSearch.CentralDescentPolicy.accepted_abort_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.accepted_abort_trace_conservation

/-- info: 'QSearch.CentralDescentPolicy.randomized_record_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_record_sum

/-- info: 'QSearch.CentralDescentPolicy.randomized_mass_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_mass_conservation

/-- info: 'QSearch.CentralDescentPolicy.randomized_mass_conservation_of_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_mass_conservation_of_complete

/-- info: 'QSearch.CentralDescentPolicy.randomized_output_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.randomized_output_trace_conservation

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_eq_packet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_eq_packet

/-- info: 'QSearch.CentralDescentPolicy.projected_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.projected_sum

/-- info: 'QSearch.CentralDescentPolicy.packet_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.packet_sum

/-- info: 'QSearch.CentralDescentPolicy.independent_source_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.independent_source_trace

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_sum

/-- info: 'QSearch.CentralDescentPolicy.measured_bank_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_bank_mass_sum

/-- info: 'QSearch.CentralDescentPolicy.measured_accepted_output_factorization' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_accepted_output_factorization

/-- info: 'QSearch.CentralDescentPolicy.measured_randomized_output_trace_conservation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.CentralDescentPolicy.measured_randomized_output_trace_conservation
