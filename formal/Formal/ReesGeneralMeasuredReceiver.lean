import Formal.ReesGeneralLawClassFour
import Formal.ReesMeasuredReceiver

/-!
# The measured Rees descent in general class, composed over all stages

The general-class counterpart of `ReesMeasuredReceiver`. For any class `c`, a
`NilpotentGroupLaw F c` that is additive on Lie-commuting pairs, a finite field
`F` and a finite Lie algebra `L` of class at most `c`:

* `measured_step_output`, `averaged_step_output`, `convert_step_source`: one
  complete measured stage, summed over ALL label records (impossible records
  included), maps the stage-`(d+1)` coset source to the stage-`d` coset source.
  The input is the literal tensor Kraus branch of the full-register central
  instrument, not an assumed normalized state.
* `descend`: the composition of all `c - 1` stages on fresh banks, defined by
  recursion from the top stage down, with no reference to `H` or `log H`.
* `descend_source`, `measured_terminal_source`: starting from the exact top
  coset source, every stage output is the exact coset source of that stage, and
  the terminal output is the additive coset source of ALL of `h = log H`.
* `classFour_measured_terminal_source`: the same at class four with every
  group-law hypothesis discharged, for an ARBITRARY subgroup `H`.

Fresh tensor powers are supplied copies, not cloning. Total valid SDE witness
policies (`active`, `sde`) and the exact initial lifted coset source remain
inputs. There is no solver, gate implementation, runtime bound or error proof.
-/

universe u

namespace QSearch.ReesGeneralMeasuredReceiver

open scoped BigOperators
open LieModule QSearch.ReesLieConstruction QSearch.ReesLieInterpolation
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient QSearch.ReesGeneralCover
  QSearch.ReesGeneralLaw QSearch.ReesGeneralReceiver
  QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver
  QSearch.CentralDescentRecords QSearch.ReesMeasuredReceiver

noncomputable section
attribute [local instance] Classical.propDecidable
attribute [local instance] ReesGeneralReceiver.truncFinite ReesGeneralReceiver.stageFintype
  ReesGeneralReceiver.centerFintype

set_option backward.isDefEq.respectTransparency false

variable {F : Type u} [Field F] [Finite F] {c : ℕ} {law : NilpotentGroupLaw F c}
  {L : Type u} [LieRing L] [LieAlgebra F L] [Finite L]

local instance labelFintype (d : ℕ) : Fintype (gamma F L d →ₗ[F] F) :=
  @Fintype.ofFinite _ (Finite.of_injective (fun f : gamma F L d →ₗ[F] F =>
    (f : gamma F L d → F)) DFunLike.coe_injective)

local instance originalFintype : Fintype L := Fintype.ofFinite _

/-- One complete ideal measured stage on fresh copies of `rho`. This definition
does not take `H` or `log H`. -/
def convertStep {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (d : ℕ) (hd : d + 1 ≤ c)
    (representative : TruncGroup (L := L) law d (by omega) →
      TruncGroup (L := L) law (d + 1) hd)
    (chi : AddChar F ℂ)
    (policy : (I → gamma F L (d + 1) →ₗ[F] F) → I → F)
    (rho : Matrix (TruncGroup (L := L) law (d + 1) hd)
      (TruncGroup (L := L) law (d + 1) hd) ℂ) :
    Matrix (TruncGroup (L := L) law d (by omega))
      (TruncGroup (L := L) law d (by omega)) ℂ := fun q r =>
  ∑ labels, actionOutput
    (paddedAction (groupDilation (d + 1) hd) (policy labels) representative)
    (let K := tensorMatrix (fun i => linearKraus (centralEmbedding hadd d hd) chi (labels i))
     K * tensorMatrix (fun _ : I => rho) * K.conjTranspose) q r

/-- The literal tensor Kraus branch of one label record on the stage source. -/
def measuredPacket {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (d : ℕ) (hd : d + 1 ≤ c) (chi : AddChar F ℂ)
    (labels : I → gamma F L (d + 1) →ₗ[F] F) :
    Matrix (I → TruncGroup (L := L) law (d + 1) hd)
      (I → TruncGroup (L := L) law (d + 1) hd) ℂ :=
  let K := tensorMatrix (fun i => linearKraus (centralEmbedding hadd d hd) chi (labels i))
  K * tensorMatrix (fun _ : I =>
    Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points (d + 1) hd))) *
    K.conjTranspose

omit [Finite F] in
theorem measured_packet_eq {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (d : ℕ) (hd : d + 1 ≤ c) (chi : AddChar F ℂ)
    (labels : I → gamma F L (d + 1) →ₗ[F] F)
    (x y : I → TruncGroup (L := L) law (d + 1) hd) :
    measuredPacket hadd hnil h points d hd chi labels x y =
      ∏ i, projectedEntry (stageHidden hnil h points (d + 1) hd)
        (centralEmbedding hadd d hd) (labelCharacter chi (labels i)) (x i) (y i) := by
  unfold measuredPacket
  rw [tensor_two_sided]
  unfold tensorMatrix
  apply Finset.prod_congr rfl
  intro i _
  exact measured_branch_eq_projected _ _
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central hadd d hd z) g).symm)
    chi (labels i) (x i) (y i)

omit [Finite F] in
/-- One measured record: its output is its branch mass times the next coset source. -/
theorem measured_step_output {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (d : ℕ) (hd : d + 1 ≤ c)
    (representative : TruncGroup (L := L) law d (by omega) →
      TruncGroup (L := L) law (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar F ℂ) (labels : I → gamma F L (d + 1) →ₗ[F] F)
    (scales : I → F) (active : ∃ i, scales i ≠ 0)
    (sde : ∑ i, scales i ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (L := L) law d (by omega)) :
    actionOutput (paddedAction (groupDilation (d + 1) hd) scales representative)
      (measuredPacket hadd hnil h points d hd chi labels) q r =
      (∏ i, branchMass (stageHidden hnil h points (d + 1) hd) (centralEmbedding hadd d hd)
        (labelCharacter chi (labels i))) *
      CosetSourceFourier.groupEntry (stageHidden hnil h points d (by omega)) q r := by
  have hp : measuredPacket hadd hnil h points d hd chi labels =
      fun x y => ∏ i, projectedEntry (stageHidden hnil h points (d + 1) hd)
        (centralEmbedding hadd d hd) (labelCharacter chi (labels i)) (x i) (y i) := by
    funext x y
    exact measured_packet_eq hadd hnil h points d hd chi labels x y
  rw [hp, ← stageHidden_projection hnil h points d hd]
  apply all_record_output (projectHom hd (by omega) (Nat.le_succ d))
    (centralEmbedding hadd d hd) (projectHom_kernel_eq_range hadd d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central hadd d hd z) g).symm)
    (stageHidden hnil h points (d + 1) hd) representative section_law chi labels
    (groupDilation (d + 1) hd) (d + 1) (by omega)
    (fun u g => dilation_stageHidden_iff hnil h points invertible (d + 1) hd u g)
    (fun u z => groupDilation_centralEmbedding hadd d hd u (Multiplicative.ofAdd z))
    scales active sde q r

/-- Label-dependent witness selection with ALL records summed: the stage output
is exactly the next coset source. -/
theorem averaged_step_output {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (d : ℕ) (hd : d + 1 ≤ c)
    (representative : TruncGroup (L := L) law d (by omega) →
      TruncGroup (L := L) law (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma F L (d + 1) →ₗ[F] F) → I → F)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (L := L) law d (by omega)) :
    (∑ labels, actionOutput
      (paddedAction (groupDilation (d + 1) hd) (policy labels) representative)
      (measuredPacket hadd hnil h points d hd chi labels) q r) =
      CosetSourceFourier.groupEntry (stageHidden hnil h points d (by omega)) q r := by
  simp_rw [measured_step_output hadd hnil h points invertible d hd representative
    section_law chi _ _ (active _) (sde _)]
  rw [← Finset.sum_mul, packet_mass_sum (stageHidden hnil h points (d + 1) hd)
    (centralEmbedding hadd d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central hadd d hd z) g).symm)
    chi hchi, one_mul]

theorem convert_step_source {I : Type*} [Fintype I] (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (d : ℕ) (hd : d + 1 ≤ c)
    (representative : TruncGroup (L := L) law d (by omega) →
      TruncGroup (L := L) law (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (policy : (I → gamma F L (d + 1) →ₗ[F] F) → I → F)
    (active : ∀ labels, ∃ i, policy labels i ≠ 0)
    (sde : ∀ labels, ∑ i, policy labels i ^ (d + 1) • labels i = 0) :
    convertStep hadd d hd representative chi policy
      (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points (d + 1) hd))) =
      Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points d (by omega))) := by
  ext q r
  exact averaged_step_output hadd hnil h points invertible d hd representative section_law
    chi hchi policy active sde q r

/-! ## All stages composed on fresh banks -/

section Tower

variable {I : ℕ → Type*} [∀ d, Fintype (I d)]

/-- The composed receiver from stage `c` down to stage `d`: each stage applies
`convertStep` with the public section to fresh copies of the previous stage's
output. Neither `H` nor `log H` is an argument. -/
def descend (hadd : AdditiveOnCommuting law) (chi : AddChar F ℂ)
    (policy : ∀ d (_ : d + 1 ≤ c), (I d → gamma F L (d + 1) →ₗ[F] F) → I d → F)
    (rho : Matrix (TruncGroup (L := L) law c le_rfl) (TruncGroup (L := L) law c le_rfl) ℂ) :
    ∀ d (hd : d ≤ c), Matrix (TruncGroup (L := L) law d hd) (TruncGroup (L := L) law d hd) ℂ
  | d, hd =>
    if h : d + 1 ≤ c then
      convertStep hadd d h (canonicalSection d h) chi (policy d h)
        (descend hadd chi policy rho (d + 1) h)
    else
      have e : c = d := by omega
      e ▸ rho
termination_by d => c - d

theorem descend_top (hadd : AdditiveOnCommuting law) (chi : AddChar F ℂ)
    (policy : ∀ d (_ : d + 1 ≤ c), (I d → gamma F L (d + 1) →ₗ[F] F) → I d → F)
    (rho : Matrix (TruncGroup (L := L) law c le_rfl) (TruncGroup (L := L) law c le_rfl) ℂ) :
    descend hadd chi policy rho c le_rfl = rho := by
  rw [descend]
  split_ifs with h
  · omega
  · rfl

theorem descend_step (hadd : AdditiveOnCommuting law) (chi : AddChar F ℂ)
    (policy : ∀ d (_ : d + 1 ≤ c), (I d → gamma F L (d + 1) →ₗ[F] F) → I d → F)
    (rho : Matrix (TruncGroup (L := L) law c le_rfl) (TruncGroup (L := L) law c le_rfl) ℂ)
    (d : ℕ) (hd : d + 1 ≤ c) :
    descend hadd chi policy rho d (by omega) =
      convertStep hadd d hd (canonicalSection d hd) chi (policy d hd)
        (descend hadd chi policy rho (d + 1) hd) := by
  rw [descend]
  split_ifs
  rfl

/-- From the exact top coset source, every stage output of the composed
receiver is the exact coset source of that stage, in every class. -/
theorem descend_source (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (policy : ∀ d (_ : d + 1 ≤ c), (I d → gamma F L (d + 1) →ₗ[F] F) → I d → F)
    (active : ∀ d hd labels, ∃ i, policy d hd labels i ≠ 0)
    (sde : ∀ d hd labels, ∑ i, policy d hd labels i ^ (d + 1) • labels i = 0)
    (d : ℕ) (hd : d ≤ c) :
    descend hadd chi policy
        (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points c le_rfl))) d hd =
      Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points d hd)) := by
  induction hm : c - d generalizing d with
  | zero =>
    obtain rfl : d = c := by omega
    exact descend_top hadd chi policy _
  | succ m ih =>
    have h1 : d + 1 ≤ c := by omega
    rw [descend_step hadd chi policy _ d h1, ih (d + 1) h1 (by omega)]
    exact convert_step_source hadd hnil h points invertible d h1 (canonicalSection d h1)
      (canonicalSection_right_inverse d h1) chi hchi (policy d h1) (active d h1) (sde d h1)

/-- The composed general-class receiver ends at the additive coset source of
ALL of `h = log H`, derived directions included. -/
theorem measured_terminal_source (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (hc : 1 ≤ c) (h : LieSubalgebra F L)
    (points : Fin c → F) (invertible : IsUnit (evaluationMatrix points).det)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (policy : ∀ d (_ : d + 1 ≤ c), (I d → gamma F L (d + 1) →ₗ[F] F) → I d → F)
    (active : ∀ d hd labels, ∃ i, policy d hd labels i ≠ 0)
    (sde : ∀ d hd labels, ∑ i, policy d hd labels i ^ (d + 1) • labels i = 0)
    (x y : L) :
    descend hadd chi policy
        (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points c le_rfl))) 1 hc
        ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd x))
        ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd y)) =
      if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  rw [descend_source hadd hnil h points invertible chi hchi policy active sde 1 hc,
    Matrix.of_apply]
  convert terminal_source hadd hnil hc h points invertible x y

end Tower

/-! ## Class four, with every group-law hypothesis discharged -/

section ClassFour

open QSearch.ReesGeneralLawClassFour

variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]
  {L : Type} [LieRing L] [LieAlgebra (ZMod p) L] [Finite L]
  {I : ℕ → Type*} [∀ d, Fintype (I d)]

/-- Class four, for an ARBITRARY subgroup `H` of the quartic BCH group over
`ZMod p` (`p > 4`): `H = exp h`, and the three measured stages composed on
fresh banks, started from the exact top coset source at the points `1, 2, 3, 4`,
end at the additive coset source of all of `h`. -/
theorem classFour_measured_terminal_source (hp : 4 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : ∀ d (_ : d + 1 ≤ 4),
      (I d → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I d → ZMod p)
    (active : ∀ d hd labels, ∃ i, policy d hd labels i ≠ 0)
    (sde : ∀ d hd labels, ∑ i, policy d hd labels i ^ (d + 1) • labels i = 0) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧ ∀ x y : L,
      descend bchLaw_additive chi policy
          (Matrix.of (CosetSourceFourier.groupEntry
            (stageHidden hnil h (canonicalPoints p) 4 le_rfl))) 1 (by norm_num)
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd x))
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd y)) =
        if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  obtain ⟨h, rfl⟩ := bchLaw_subgroups L hnil H
  exact ⟨h, rfl, measured_terminal_source bchLaw_additive hnil (by norm_num) h
    (canonicalPoints p) (canonicalPoints_isUnit hp) chi hchi policy active sde⟩

end ClassFour

end
end QSearch.ReesGeneralMeasuredReceiver

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.convert_step_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.convert_step_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.descend_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.descend_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.measured_terminal_source

/-- info: 'QSearch.ReesGeneralMeasuredReceiver.classFour_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralMeasuredReceiver.classFour_measured_terminal_source
