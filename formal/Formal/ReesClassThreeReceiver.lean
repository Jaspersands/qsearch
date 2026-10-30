import Formal.ReesCentralQuotientBCH
import Formal.CentralQuotientReceiver

/-!
# Concrete class-three Rees central receiver steps

The group, projections, central embeddings, dilation weights and hidden-image
preservation are derived from the actual positive Rees construction. The
sections below insert zero top coefficients and do not use H. The channel
theorem is branchwise for independent normalized sources and a supplied valid
SDE witness; no quantum source, solver, recursive clock or runtime is extracted.
-/

namespace QSearch.ReesClassThreeReceiver

open LieModule QSearch.ReesLieConstruction QSearch.ReesCentralQuotient
open QSearch.ReesCentralQuotientBCH QSearch.ReesGroupClassThree
open QSearch.BCHClassThree QSearch.CentralCharacterDescent
open QSearch.CentralQuotientReceiver

noncomputable section
attribute [local instance] Classical.propDecidable

section Sections

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

theorem quotient_coefficient_mem (d r : ℕ) (hr : r ≤ d)
    (x : Trunc (R := F) (L := L) d) :
    quotientCoefficient d r hr x ∈ gamma F L r := by
  obtain ⟨a, rfl⟩ := mk_surjective d x
  exact (mem_rees_iff _).mp a.property |>.2 r

/-- The degree-two representative with zero degree-three coefficient. -/
def sectionLie32 (x : Trunc (R := F) (L := L) 2) : Trunc (R := F) (L := L) 3 :=
  mk 3 (gradeOne (quotientCoefficient 2 1 (by decide) x) +
    homogeneous 2 (by decide)
      ⟨quotientCoefficient 2 2 le_rfl x, quotient_coefficient_mem 2 2 le_rfl x⟩)

theorem sectionLie32_right_inverse (x : Trunc (R := F) (L := L) 2) :
    projection (show 2 ≤ 3 by decide) (sectionLie32 x) = x := by
  obtain ⟨a, rfl⟩ := mk_surjective 2 x
  apply (mk_eq_mk_iff 2 _ _).mpr
  intro r hr
  interval_cases r <;>
    simp [coefficient_gradeOne, coefficient_homogeneous]

variable [NeZero (2 : F)] [NeZero (3 : F)]

def section32 (x : TruncGroup (F := F) (L := L) 2 (by decide)) :
    TruncGroup (F := F) (L := L) 3 (by decide) := BCH.mk (sectionLie32 x.val)

theorem section32_right_inverse (x : TruncGroup (F := F) (L := L) 2 (by decide)) :
    pi32 (section32 x) = x := BCH.ext (sectionLie32_right_inverse x.val)

/-- Grade one is lifted linearly, not as a group homomorphism. -/
def section21 (x : TruncGroup (F := F) (L := L) 1 (by decide)) :
    TruncGroup (F := F) (L := L) 2 (by decide) :=
  BCH.mk (mk 2 (gradeOne (terminalEquiv x.val)))

theorem section21_right_inverse (x : TruncGroup (F := F) (L := L) 1 (by decide)) :
    pi21 (section21 x) = x := BCH.ext (terminalEquiv.left_inv x.val)

end Sections

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [Finite L]

local instance stageFintype (d : ℕ) (hd : d ≤ 3) :
    Fintype (TruncGroup (F := ZMod p) (L := L) d hd) := Fintype.ofFinite _

local instance centerFintype (d : ℕ) : Fintype (gamma (ZMod p) L d) := Fintype.ofFinite _

def stageHidden (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d ≤ 3) :
    Subgroup (TruncGroup (F := ZMod p) (L := L) d hd) :=
  (liftedSubgroup hnil H).map (groupMk hnil d hd)

omit [Finite L] in
theorem stageHidden_projection (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3) :
    (stageHidden hnil H (d + 1) hd).map (projectHom hd (by omega) (Nat.le_succ d)) =
      stageHidden hnil H d (by omega) := by
  simp only [stageHidden, Subgroup.map_map]
  rfl

/-- All algebraic premises of scalar quotient descent are discharged for the
actual Rees stages. Only the public section and the source/SDE inputs remain. -/
theorem step_output {I : Type*} [Fintype I] [Nonempty I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (d : ℕ) (hd : d + 1 ≤ 3)
    (representative : TruncGroup (F := ZMod p) (L := L) d (by omega) →
      TruncGroup (F := ZMod p) (L := L) (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar (ZMod p) ℂ) (labels : I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden hnil H (d + 1) hd) (centralEmbedding d hd)
        (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → (ZMod p)ˣ)
    (sde : ∑ i, (scales i : ZMod p) ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) d (by omega)) :
    actionOutput (fun x i => groupDilation (d + 1) hd (scales i) (representative x))
      (fun x y : I → TruncGroup (F := ZMod p) (L := L) (d + 1) hd =>
        ∏ i, normalizedEntry (stageHidden hnil H (d + 1) hd) (centralEmbedding d hd)
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil H d (by omega)) q r := by
  rw [← stageHidden_projection hnil H d hd]
  apply scalar_quotient_coset_output
    (projectHom hd (by omega) (Nat.le_succ d)) (centralEmbedding d hd)
    (projectHom_kernel_eq_range d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central d hd z) g).symm)
    (stageHidden hnil H (d + 1) hd) representative section_law chi labels nonzero_trace
    (fun i => groupDilation (d + 1) hd (scales i)) scales (d + 1)
  · exact fun i g => dilation_arbitrary_image hnil H (d + 1) hd (scales i) g
  · exact fun i z => groupDilation_centralEmbedding d hd (scales i) (Multiplicative.ofAdd z)
  · exact sde

theorem degree_three_output {I : Type*} [Fintype I] [Nonempty I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (labels : I → gamma (ZMod p) L 3 →ₗ[ZMod p] ZMod p)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden hnil H 3 (by decide)) (centralEmbedding 2 (by decide))
        (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → (ZMod p)ˣ)
    (sde : ∑ i, (scales i : ZMod p) ^ 3 • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) 2 (by decide)) :
    actionOutput (fun x i => groupDilation 3 (by decide) (scales i) (section32 x))
      (fun x y : I → TruncGroup (F := ZMod p) (L := L) 3 (by decide) =>
        ∏ i, normalizedEntry (stageHidden hnil H 3 (by decide)) (centralEmbedding 2 (by decide))
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil H 2 (by decide)) q r :=
  step_output hnil H 2 (by decide) section32 section32_right_inverse
    chi labels nonzero_trace scales sde q r

theorem degree_two_output {I : Type*} [Fintype I] [Nonempty I]
    (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil))
    (chi : AddChar (ZMod p) ℂ) (labels : I → gamma (ZMod p) L 2 →ₗ[ZMod p] ZMod p)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden hnil H 2 (by decide)) (centralEmbedding 1 (by decide))
        (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → (ZMod p)ˣ)
    (sde : ∑ i, (scales i : ZMod p) ^ 2 • labels i = 0)
    (q r : TruncGroup (F := ZMod p) (L := L) 1 (by decide)) :
    actionOutput (fun x i => groupDilation 2 (by decide) (scales i) (section21 x))
      (fun x y : I → TruncGroup (F := ZMod p) (L := L) 2 (by decide) =>
        ∏ i, normalizedEntry (stageHidden hnil H 2 (by decide)) (centralEmbedding 1 (by decide))
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil H 1 (by decide)) q r :=
  step_output hnil H 1 (by decide) section21 section21_right_inverse
    chi labels nonzero_trace scales sde q r

omit [Finite L] in
theorem terminal_membership (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (v : L) :
    Multiplicative.ofAdd v ∈
      (stageHidden hnil H 1 (by decide)).map terminalGroupEquiv.toMonoidHom ↔
      BCH.mk v ∈ H := by
  rw [stageHidden, Subgroup.map_map]
  exact terminal_arbitrary_subgroup hnil H v

local instance originalFintype : Fintype L := Fintype.ofFinite _

/-- After relabeling the terminal quotient, the recovered source is the
additive coset source of ALL logarithms in H, including derived directions. -/
theorem terminal_source (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) (x y : L) :
    CosetSourceFourier.groupEntry (stageHidden hnil H 1 (by decide))
      (terminalGroupEquiv.symm (Multiplicative.ofAdd x))
      (terminalGroupEquiv.symm (Multiplicative.ofAdd y)) =
      if BCH.mk (y - x) ∈ H then AffineSupportErasure.invSize L else 0 := by
  have hm := terminal_membership hnil H (y - x)
  rw [Subgroup.mem_map_equiv] at hm
  have he : (Multiplicative.ofAdd (y - x) : Multiplicative L) =
      (Multiplicative.ofAdd x)⁻¹ * Multiplicative.ofAdd y := by
    change y - x = -x + y
    abel
  rw [he, map_mul, map_inv] at hm
  unfold CosetSourceFourier.groupEntry
  rw [hm]
  have hc : Fintype.card (TruncGroup (F := ZMod p) (L := L) 1 (by decide)) =
      Fintype.card L :=
    Fintype.card_congr (terminalGroupEquiv.toEquiv.trans (Multiplicative.toAdd : Multiplicative L ≃ L))
  simp only [AffineSupportErasure.invSize, hc]

end PrimeField

end
end QSearch.ReesClassThreeReceiver

/-- info: 'QSearch.ReesClassThreeReceiver.sectionLie32_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.sectionLie32_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.section32_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.section32_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.section21_right_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.section21_right_inverse

/-- info: 'QSearch.ReesClassThreeReceiver.stageHidden_projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.stageHidden_projection

/-- info: 'QSearch.ReesClassThreeReceiver.step_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.step_output

/-- info: 'QSearch.ReesClassThreeReceiver.degree_three_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.degree_three_output

/-- info: 'QSearch.ReesClassThreeReceiver.degree_two_output' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.degree_two_output

/-- info: 'QSearch.ReesClassThreeReceiver.terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesClassThreeReceiver.terminal_source
