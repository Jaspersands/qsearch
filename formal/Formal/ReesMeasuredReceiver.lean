import Formal.ReesClassThreeReceiver
import Formal.CentralDescentRecords
import Formal.CentralSpectralProjector
import Formal.RetainedFourier

/-!
# Actual measured class-three Rees descent

The full-register central-ancilla instrument is reindexed by the EXISTING
linear-character equivalence. Tensor Kraus branches, including impossible
records, feed the all-record descent identity. A valid nonzero SDE witness
is still supplied; no solver, recursive clock or circuit extraction occurs.
-/

namespace QSearch.ReesMeasuredReceiver

open scoped BigOperators
open QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver
open QSearch.CentralDescentRecords QSearch.CentralSpectralProjector
open QSearch.ReesClassThreeReceiver QSearch.ReesCentralQuotientBCH
open QSearch.ReesGroupClassThree QSearch.ReesLieConstruction QSearch.BCHClassThree
open QSearch.AffineSupportErasure (invSize)
open LieModule

noncomputable section
attribute [local instance] Classical.propDecidable
set_option backward.isDefEq.respectTransparency false

section LinearInstrument
variable {F V G : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Group G] [Fintype G] [Fintype V] [Fintype (V →ₗ[F] F)]

def linearKraus (embed : Multiplicative V →* G) (chi : AddChar F ℂ)
    (label : V →ₗ[F] F) : Matrix G G ℂ :=
  ancillaKraus embed (RetainedFourier.linearCharacter chi label)

theorem linear_instrument_complete (embed : Multiplicative V →* G)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (x y : G) :
    (∑ label : V →ₗ[F] F, ∑ t,
      star (linearKraus embed chi label t x) * linearKraus embed chi label t y) =
      if x = y then 1 else 0 := by
  calc
    _ = ∑ ch : AddChar V ℂ, ∑ t,
        star (ancillaKraus embed ch t x) * ancillaKraus embed ch t y :=
      Fintype.sum_equiv (RetainedFourier.characterEquiv chi hchi) _ _ (fun _ => rfl)
    _ = _ := ancilla_kraus_complete embed x y

def measuredBranch (H : Subgroup G) (embed : Multiplicative V →* G)
    (chi : AddChar F ℂ) (label : V →ₗ[F] F) : Matrix G G ℂ :=
  linearKraus embed chi label * Matrix.of (CosetSourceFourier.groupEntry H) *
    (linearKraus embed chi label).conjTranspose

omit [Fintype (V →ₗ[F] F)] in
theorem measured_branch_eq_projected (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (label : V →ₗ[F] F) (x y : G) :
    measuredBranch H embed chi label x y =
      projectedEntry H embed (labelCharacter chi label) x y :=
  ancilla_source H embed central (RetainedFourier.linearCharacter chi label) x y

omit [Fintype G] in
theorem linear_projector_sum (embed : Multiplicative V →* G)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    (∑ label : V →ₗ[F] F, projector embed (RetainedFourier.linearCharacter chi label)) = 1 := by
  calc
    _ = ∑ ch : AddChar V ℂ, projector embed ch :=
      Fintype.sum_equiv (RetainedFourier.characterEquiv chi hchi) _ _ (fun _ => rfl)
    _ = 1 := projector_sum embed

theorem measured_branch_sum (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (x y : G) :
    (∑ label : V →ₗ[F] F, measuredBranch H embed chi label x y) =
      CosetSourceFourier.groupEntry H x y := by
  have hb (label : V →ₗ[F] F) : measuredBranch H embed chi label =
      projector embed (RetainedFourier.linearCharacter chi label) *
        Matrix.of (CosetSourceFourier.groupEntry H) := by
    ext a b
    rw [measured_branch_eq_projected H embed central,
      projector_mul_source]
    rfl
  have hs : (∑ label : V →ₗ[F] F, measuredBranch H embed chi label) =
      Matrix.of (CosetSourceFourier.groupEntry H) := by
    simp_rw [hb]
    rw [← Finset.sum_mul, linear_projector_sum embed chi hchi, one_mul]
  simpa only [Matrix.sum_apply, Matrix.of_apply] using congrArg (fun M : Matrix G G ℂ => M x y) hs

theorem measured_mass_sum (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    (∑ label : V →ₗ[F] F, ∑ x, measuredBranch H embed chi label x x) = 1 := by
  rw [Finset.sum_comm]
  simp_rw [measured_branch_sum H embed central chi hchi]
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [CosetSourceFourier.groupEntry, invSize, hn]

theorem branch_mass_sum (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    (∑ label : V →ₗ[F] F, branchMass H embed (labelCharacter chi label)) = 1 := by
  simpa only [measured_branch_eq_projected H embed central, branchMass] using
    measured_mass_sum H embed central chi hchi

theorem packet_mass_sum {I : Type*} [Fintype I]
    (H : Subgroup G) (embed : Multiplicative V →* G)
    (central : ∀ z g, embed z * g = g * embed z)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    (∑ labels : I → V →ₗ[F] F, ∏ i, branchMass H embed (labelCharacter chi (labels i))) = 1 := by
  calc
    _ = ∏ _i : I, ∑ label : V →ₗ[F] F, branchMass H embed (labelCharacter chi label) :=
      (Fintype.prod_sum (fun (_i : I) (label : V →ₗ[F] F) =>
        branchMass H embed (labelCharacter chi label))).symm
    _ = 1 := by simp_rw [branch_mass_sum H embed central chi hchi]; simp

end LinearInstrument

section Rees
variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [Finite L]

local instance stageFintype (d : ℕ) (hd : d ≤ 3) :
    Fintype (TruncGroup (F := ZMod p) (L := L) d hd) := Fintype.ofFinite _
local instance centerFintype (d : ℕ) : Fintype (gamma (ZMod p) L d) := Fintype.ofFinite _
local instance labelFintype (d : ℕ) : Fintype (gamma (ZMod p) L d →ₗ[ZMod p] ZMod p) :=
  Fintype.ofInjective (fun f : gamma (ZMod p) L d →ₗ[ZMod p] ZMod p =>
    (f : gamma (ZMod p) L d → ZMod p)) DFunLike.coe_injective

/-- One complete ideal measured stage on fresh copies of rho. This definition
does not take H or log(H). Tensoring rho means fresh supplied copies, not a
physical cloning map on one unknown input. -/
def convertStep {I : Type*} [Fintype I] (d : ℕ) (hd : d + 1 ≤ 3)
    (representative : TruncGroup (F := ZMod p) (L := L) d (by omega) →
      TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
    (chi : AddChar (ZMod p) ℂ)
    (policy : (I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (rho : Matrix (TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
      (TruncGroup (F := ZMod p) (L := L) (d + 1) hd) ℂ) :
    Matrix (TruncGroup (F := ZMod p) (L := L) d (by omega))
      (TruncGroup (F := ZMod p) (L := L) d (by omega)) ℂ := fun q r =>
  ∑ labels, actionOutput
    (paddedAction (groupDilation (d + 1) hd) (policy labels) representative)
    (let K := tensorMatrix (fun i => linearKraus (centralEmbedding d hd) chi (labels i))
     K * tensorMatrix (fun _ : I => rho) * K.conjTranspose) q r

def measuredPacket {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (chi : AddChar (ZMod p) ℂ)
    (labels : I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) :
    Matrix (I → TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
      (I → TruncGroup (F := ZMod p) (L := L) (d + 1) hd) ℂ :=
  let K := tensorMatrix (fun i => linearKraus (centralEmbedding d hd) chi (labels i))
  K * tensorMatrix (fun _ : I => Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H (d + 1) hd))) *
    K.conjTranspose

theorem measured_packet_eq {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (chi : AddChar (ZMod p) ℂ)
    (labels : I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p)
    (x y : I → TruncGroup (F := ZMod p) (L := L) (d + 1) hd) :
    measuredPacket hnil H d hd chi labels x y =
      ∏ i, projectedEntry (stageHidden hnil H (d + 1) hd) (centralEmbedding d hd)
        (labelCharacter chi (labels i)) (x i) (y i) := by
  unfold measuredPacket
  rw [tensor_two_sided]
  unfold tensorMatrix
  apply Finset.prod_congr rfl
  intro i _
  exact measured_branch_eq_projected _ _
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central d hd z) g).symm)
    chi (labels i) (x i) (y i)

theorem measured_step_output {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (representative : TruncGroup (F := ZMod p) (L := L) d (by omega) →
      TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar (ZMod p) ℂ)
    (labels : I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p)
    (scales : I → ZMod p) (active : ∃ i, scales i ≠ 0)
    (sde : ∑ i, scales i ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) d (by omega)) :
    actionOutput (paddedAction (groupDilation (d + 1) hd) scales representative)
      (measuredPacket hnil H d hd chi labels) q r =
      (∏ i, branchMass (stageHidden hnil H (d + 1) hd) (centralEmbedding d hd)
        (labelCharacter chi (labels i))) *
      CosetSourceFourier.groupEntry (stageHidden hnil H d (by omega)) q r := by
  have hp : measuredPacket hnil H d hd chi labels =
      fun x y => ∏ i, projectedEntry (stageHidden hnil H (d + 1) hd) (centralEmbedding d hd)
        (labelCharacter chi (labels i)) (x i) (y i) := by
    funext x y
    exact measured_packet_eq hnil H d hd chi labels x y
  rw [hp, ← stageHidden_projection hnil H d hd]
  apply all_record_output (projectHom hd (by omega) (Nat.le_succ d)) (centralEmbedding d hd)
    (projectHom_kernel_eq_range d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central d hd z) g).symm)
    (stageHidden hnil H (d + 1) hd) representative section_law chi labels
    (groupDilation (d + 1) hd) (d + 1) (by omega)
    (fun u g => dilation_arbitrary_image hnil H (d + 1) hd u g)
    (fun u z => groupDilation_centralEmbedding d hd u (Multiplicative.ofAdd z))
    scales active sde q r

/-- Deterministic label-dependent witness selection, with ALL records summed.
The input is the literal tensor Kraus branch, not assumed normalized states.
The witness policy is still a supplied total function, with no runtime claim. -/
theorem averaged_step_output {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (representative : TruncGroup (F := ZMod p) (L := L) d (by omega) →
      TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) d (by omega)) :
    (∑ labels, actionOutput
      (paddedAction (groupDilation (d + 1) hd) (policy labels) representative)
      (measuredPacket hnil H d hd chi labels) q r) =
      CosetSourceFourier.groupEntry (stageHidden hnil H d (by omega)) q r := by
  simp_rw [measured_step_output hnil H d hd representative section_law chi _ _
    (active _) (sde _)]
  rw [← Finset.sum_mul, packet_mass_sum (stageHidden hnil H (d + 1) hd)
    (centralEmbedding d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central d hd z) g).symm)
    chi hchi, one_mul]

theorem degree_three_measured {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma (ZMod p) L 3 →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ 3 • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) 2 (by decide)) :
    (∑ labels, actionOutput
      (paddedAction (groupDilation 3 (by decide)) (policy labels) section32)
      (measuredPacket hnil H 2 (by decide) chi labels) q r) =
      CosetSourceFourier.groupEntry (stageHidden hnil H 2 (by decide)) q r :=
  averaged_step_output hnil H 2 (by decide) section32 section32_right_inverse
    chi hchi policy active sde q r

theorem degree_two_measured {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma (ZMod p) L 2 →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ 2 • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) 1 (by decide)) :
    (∑ labels, actionOutput
      (paddedAction (groupDilation 2 (by decide)) (policy labels) section21)
      (measuredPacket hnil H 1 (by decide) chi labels) q r) =
      CosetSourceFourier.groupEntry (stageHidden hnil H 1 (by decide)) q r :=
  averaged_step_output hnil H 1 (by decide) section21 section21_right_inverse
    chi hchi policy active sde q r

theorem convert_step_source {I : Type*} [Fintype I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (representative : TruncGroup (F := ZMod p) (L := L) d (by omega) →
      TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ (d + 1) • labels i = 0) :
    convertStep d hd representative chi policy
      (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H (d + 1) hd))) =
      Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H d (by omega))) := by
  ext q r
  exact averaged_step_output hnil H d hd representative section_law chi hchi policy active sde q r

/-- Explicit two-stage expression. The second stage receives a fresh tensor
of first-stage outputs. Each output uses a disjoint original input bank. -/
theorem two_stage_source {I J : Type*} [Fintype I] [Fintype J]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (cubic : (I → gamma (ZMod p) L 3 →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (cubic_active : ∀ labels, ∃ i, cubic labels i ≠ 0)
    (cubic_sde : ∀ labels, ∑ i, cubic labels i ^ 3 • labels i = 0)
    (quadratic : (J → gamma (ZMod p) L 2 →ₗ[ZMod p] ZMod p) → J → ZMod p)
    (quadratic_active : ∀ labels, ∃ j, quadratic labels j ≠ 0)
    (quadratic_sde : ∀ labels, ∑ j, quadratic labels j ^ 2 • labels j = 0) :
    convertStep 1 (by decide) section21 chi quadratic
      (convertStep 2 (by decide) section32 chi cubic
        (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H 3 (by decide))))) =
      Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H 1 (by decide))) := by
  rw [convert_step_source hnil H 2 (by decide) section32 section32_right_inverse
    chi hchi cubic cubic_active cubic_sde]
  exact convert_step_source hnil H 1 (by decide) section21 section21_right_inverse
    chi hchi quadratic quadratic_active quadratic_sde

theorem measured_terminal_source {I J : Type*} [Fintype I] [Fintype J]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (cubic : (I → gamma (ZMod p) L 3 →ₗ[ZMod p] ZMod p) → I → ZMod p)
    (cubic_active : ∀ labels, ∃ i, cubic labels i ≠ 0)
    (cubic_sde : ∀ labels, ∑ i, cubic labels i ^ 3 • labels i = 0)
    (quadratic : (J → gamma (ZMod p) L 2 →ₗ[ZMod p] ZMod p) → J → ZMod p)
    (quadratic_active : ∀ labels, ∃ j, quadratic labels j ≠ 0)
    (quadratic_sde : ∀ labels, ∑ j, quadratic labels j ^ 2 • labels j = 0)
    (x y : L) :
    convertStep 1 (by decide) section21 chi quadratic
      (convertStep 2 (by decide) section32 chi cubic
        (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil H 3 (by decide)))))
      (terminalGroupEquiv.symm (Multiplicative.ofAdd x))
      (terminalGroupEquiv.symm (Multiplicative.ofAdd y)) =
      if BCH.mk (y - x) ∈ H then (Fintype.card (TruncGroup (F := ZMod p) (L := L) 1 (by decide)) : ℂ)⁻¹
        else 0 := by
  rw [two_stage_source hnil H chi hchi cubic cubic_active cubic_sde
    quadratic quadratic_active quadratic_sde]
  let : Fintype L := Fintype.ofFinite L
  have hc : Fintype.card (TruncGroup (F := ZMod p) (L := L) 1 (by decide)) =
      Fintype.card L :=
    Fintype.card_congr (terminalGroupEquiv.toEquiv.trans (Multiplicative.toAdd : Multiplicative L ≃ L))
  simpa only [Matrix.of_apply, hc, invSize] using terminal_source hnil H x y

end Rees
end
end QSearch.ReesMeasuredReceiver

/-- info: 'QSearch.ReesMeasuredReceiver.linear_instrument_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.linear_instrument_complete

/-- info: 'QSearch.ReesMeasuredReceiver.measured_branch_eq_projected' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_branch_eq_projected

/-- info: 'QSearch.ReesMeasuredReceiver.linear_projector_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.linear_projector_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_branch_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_branch_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.branch_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.branch_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.packet_mass_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.packet_mass_sum

/-- info: 'QSearch.ReesMeasuredReceiver.measured_packet_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_packet_eq

/-- info: 'QSearch.ReesMeasuredReceiver.measured_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_step_output

/-- info: 'QSearch.ReesMeasuredReceiver.averaged_step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.averaged_step_output

/-- info: 'QSearch.ReesMeasuredReceiver.degree_three_measured' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.degree_three_measured

/-- info: 'QSearch.ReesMeasuredReceiver.degree_two_measured' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.degree_two_measured

/-- info: 'QSearch.ReesMeasuredReceiver.convert_step_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.convert_step_source

/-- info: 'QSearch.ReesMeasuredReceiver.two_stage_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.two_stage_source

/-- info: 'QSearch.ReesMeasuredReceiver.measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesMeasuredReceiver.measured_terminal_source
