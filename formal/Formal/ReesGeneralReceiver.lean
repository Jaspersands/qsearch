import Formal.ReesGeneralLaw
import Formal.CentralQuotientReceiver

/-!
# General-class Rees central receiver steps, conditional on a natural law

Written for item 8 of `research/REES_FULL_CAMPAIGN.md`, target (c), and promoted
into the default build on 2026-11-02. This is the general-class counterpart of
`Formal/ReesClassThreeReceiver.lean`; `ReesGeneralMeasuredReceiver` composes
the steps.
For any class `c`, any degree `d + 1 ≤ c`, a `NilpotentGroupLaw F c` that is
additive on Lie-commuting pairs, and any Lie subalgebra `h` (the logarithm of
`H`; `SubgroupsAreSubalgebras` supplies it for arbitrary `H`):

* `centralEmbedding`, `projectHom_kernel_eq_range`, `centralEmbedding_central`,
  `groupDilation_centralEmbedding`: the step kernel `G̃_{d+1} → G̃_d` is the
  additive top grade `γ_{d+1}`, central, with dilation weight `u^(d+1)`;
* `stageHidden_projection`, `dilation_stageHidden_iff`: the stage hidden
  subgroups are actual images, compatible with projection and dilation;
* `step_output`: the measured scalar quotient channel of
  `CentralQuotientReceiver.scalar_quotient_coset_output` outputs the coset
  source of the next stage, given a valid scalar SDE witness and nonzero
  branch traces (the same inputs as the class-three theorem);
* `canonicalSection`: a public section, so the section premise is discharged;
* `terminal_source`: after the `c - 1` steps the terminal coset source is the
  additive coset source of all of `h`.

The group law, the SDE witness and the nonzero traces are inputs; the solver,
the quantum source preparation and the running time are not modelled.
-/

universe u

namespace QSearch.ReesGeneralReceiver

open LieModule QSearch.ReesLieConstruction QSearch.ReesLieInterpolation
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient QSearch.ReesGeneralCover
  QSearch.ReesGeneralLaw QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver

noncomputable section
attribute [local instance] Classical.propDecidable

set_option backward.isDefEq.respectTransparency false

variable {F : Type u} [Field F] {c : ℕ} {law : NilpotentGroupLaw F c}
  {L : Type u} [LieRing L] [LieAlgebra F L]

/-! ## Central step kernels in general class -/

/-- The top grade embeds additively into the group kernel. -/
def centralEmbedding (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c) :
    Multiplicative (gamma F L (d + 1)) →* TruncGroup (L := L) law (d + 1) hd where
  toFun v := ⟨topEmbedding d v.toAdd⟩
  map_one' := LawGroup.ext (map_zero _)
  map_mul' x y := by
    apply LawGroup.ext
    change topEmbedding d (x.toAdd + y.toAdd) = law.mul _ _ _
    rw [map_add, hadd _ _ _ (topEmbedding_central d _ _)]

@[simp] theorem centralEmbedding_val (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c)
    (v : Multiplicative (gamma F L (d + 1))) :
    (centralEmbedding hadd d hd v).val = topEmbedding d v.toAdd := rfl

theorem centralEmbedding_injective (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c) :
    Function.Injective (centralEmbedding (L := L) hadd d hd) := by
  intro x y h
  exact (topEmbedding_injective d) (congrArg LawGroup.val h)

theorem projectHom_kernel_eq_range (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c) :
    (projectHom (L := L) (law := law) hd (by omega) (Nat.le_succ d)).ker =
      (centralEmbedding hadd d hd).range := by
  ext x
  rw [MonoidHom.mem_ker, MonoidHom.mem_range]
  constructor
  · intro hx
    obtain ⟨v, hv⟩ := (top_kernel_iff d x.val).mp (congrArg LawGroup.val hx)
    exact ⟨Multiplicative.ofAdd v, LawGroup.ext hv⟩
  · rintro ⟨v, rfl⟩
    exact LawGroup.ext (projection_topEmbedding d v.toAdd)

theorem centralEmbedding_central (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c)
    (v : Multiplicative (gamma F L (d + 1))) :
    centralEmbedding hadd d hd v ∈ Subgroup.center (TruncGroup (L := L) law (d + 1) hd) := by
  apply projectHom_kernel_central hadd d hd
  rw [projectHom_kernel_eq_range hadd]
  exact ⟨v, rfl⟩

theorem groupDilation_centralEmbedding (hadd : AdditiveOnCommuting law) (d : ℕ)
    (hd : d + 1 ≤ c) (u : Fˣ) (v : Multiplicative (gamma F L (d + 1))) :
    groupDilation (d + 1) hd u (centralEmbedding hadd d hd v) =
      centralEmbedding hadd d hd (Multiplicative.ofAdd ((u : F) ^ (d + 1) • v.toAdd)) :=
  LawGroup.ext (dilation_topEmbedding d u v.toAdd)

theorem groupDilation_groupMk (hnil : lowerCentralSeries F L L c = ⊥) (d : ℕ) (hd : d ≤ c)
    (u : Fˣ) (x : ReesGroup law hnil) :
    groupDilation d hd u (groupMk hnil d hd x) = groupMk hnil d hd (dilationHom hnil u x) :=
  rfl

/-! ## Stage hidden subgroups -/

/-- The stage-`d` hidden subgroup, as an actual image of `exp h̃`. -/
def stageHidden (hnil : lowerCentralSeries F L L c = ⊥) (h : LieSubalgebra F L)
    (points : Fin c → F) (d : ℕ) (hd : d ≤ c) : Subgroup (TruncGroup (L := L) law d hd) :=
  (ReesGeneralLaw.hiddenSubgroup hnil h points).map (groupMk hnil d hd)

theorem stageHidden_projection (hnil : lowerCentralSeries F L L c = ⊥)
    (h : LieSubalgebra F L) (points : Fin c → F) (d : ℕ) (hd : d + 1 ≤ c) :
    (stageHidden (law := law) hnil h points (d + 1) hd).map
        (projectHom hd (by omega) (Nat.le_succ d)) =
      stageHidden hnil h points d (by omega) := by
  simp only [stageHidden, Subgroup.map_map]
  rfl

private theorem dilation_stageHidden_forward (hnil : lowerCentralSeries F L L c = ⊥)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (d : ℕ) (hd : d ≤ c) (u : Fˣ) (x : TruncGroup (L := L) law d hd)
    (hx : x ∈ stageHidden hnil h points d hd) :
    groupDilation d hd u x ∈ stageHidden hnil h points d hd := by
  obtain ⟨y, hy, rfl⟩ := hx
  rw [groupDilation_groupMk]
  exact ⟨dilationHom hnil u y,
    (dilation_hiddenSubgroup_iff hnil h points invertible u y).mpr hy, rfl⟩

theorem dilation_stageHidden_iff (hnil : lowerCentralSeries F L L c = ⊥)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (d : ℕ) (hd : d ≤ c) (u : Fˣ) (x : TruncGroup (L := L) law d hd) :
    groupDilation d hd u x ∈ stageHidden hnil h points d hd ↔
      x ∈ stageHidden hnil h points d hd := by
  constructor
  · intro hx
    have hi := dilation_stageHidden_forward hnil h points invertible d hd u⁻¹ _ hx
    change (groupDilation d hd u).symm (groupDilation d hd u x) ∈
      stageHidden hnil h points d hd at hi
    simpa only [MulEquiv.symm_apply_apply] using hi
  · exact dilation_stageHidden_forward hnil h points invertible d hd u x

/-- A public section of each step projection, chosen without reference to `H`. -/
def canonicalSection (d : ℕ) (hd : d + 1 ≤ c) :
    TruncGroup (L := L) law d (by omega) → TruncGroup (L := L) law (d + 1) hd :=
  Function.surjInv (projectHom_surjective hd (by omega) (Nat.le_succ d))

theorem canonicalSection_right_inverse (d : ℕ) (hd : d + 1 ≤ c)
    (q : TruncGroup (L := L) law d (by omega)) :
    projectHom hd (by omega) (Nat.le_succ d) (canonicalSection d hd q) = q :=
  Function.surjInv_eq _ q

/-! ## The measured channel step in general class -/

section Finite

variable [Finite L]

local instance truncFinite (d : ℕ) : Finite (Trunc (R := F) (L := L) d) :=
  Finite.of_injective _ (finiteCoefficients_injective (R := F) (L := L) d)

local instance stageFintype (d : ℕ) (hd : d ≤ c) :
    Fintype (TruncGroup (L := L) law d hd) :=
  @Fintype.ofFinite _ (Finite.of_injective (fun x : TruncGroup (L := L) law d hd => x.val)
    (fun _ _ h => LawGroup.ext h))

local instance centerFintype (d : ℕ) : Fintype (gamma F L d) := Fintype.ofFinite _

/-- One general-class descent step: all algebraic premises of the scalar
quotient receiver are discharged for the actual Rees stages. -/
theorem step_output {I : Type*} [Fintype I] [Nonempty I]
    (hadd : AdditiveOnCommuting law) (hnil : lowerCentralSeries F L L c = ⊥)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (d : ℕ) (hd : d + 1 ≤ c)
    (representative : TruncGroup (L := L) law d (by omega) →
      TruncGroup (L := L) law (d + 1) hd)
    (section_law : ∀ q, projectHom hd (by omega) (Nat.le_succ d) (representative q) = q)
    (chi : AddChar F ℂ) (labels : I → gamma F L (d + 1) →ₗ[F] F)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden hnil h points (d + 1) hd) (centralEmbedding hadd d hd)
        (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → Fˣ)
    (sde : ∑ i, (scales i : F) ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (L := L) law d (by omega)) :
    actionOutput (fun x i => groupDilation (d + 1) hd (scales i) (representative x))
      (fun x y : I → TruncGroup (L := L) law (d + 1) hd =>
        ∏ i, normalizedEntry (stageHidden hnil h points (d + 1) hd) (centralEmbedding hadd d hd)
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil h points d (by omega)) q r := by
  rw [← stageHidden_projection hnil h points d hd]
  apply scalar_quotient_coset_output
    (projectHom hd (by omega) (Nat.le_succ d)) (centralEmbedding hadd d hd)
    (projectHom_kernel_eq_range hadd d hd)
    (fun z g => (Subgroup.mem_center_iff.mp (centralEmbedding_central hadd d hd z) g).symm)
    (stageHidden hnil h points (d + 1) hd) representative section_law chi labels nonzero_trace
    (fun i => groupDilation (d + 1) hd (scales i)) scales (d + 1)
  · exact fun i g => dilation_stageHidden_iff hnil h points invertible (d + 1) hd (scales i) g
  · exact fun i z => groupDilation_centralEmbedding hadd d hd (scales i) (Multiplicative.ofAdd z)
  · exact sde

/-- The same step with the public section, so only the source, the SDE witness
and the nonzero traces remain as inputs. -/
theorem step_output_canonical {I : Type*} [Fintype I] [Nonempty I]
    (hadd : AdditiveOnCommuting law) (hnil : lowerCentralSeries F L L c = ⊥)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (d : ℕ) (hd : d + 1 ≤ c)
    (chi : AddChar F ℂ) (labels : I → gamma F L (d + 1) →ₗ[F] F)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden hnil h points (d + 1) hd) (centralEmbedding hadd d hd)
        (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → Fˣ)
    (sde : ∑ i, (scales i : F) ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (L := L) law d (by omega)) :
    actionOutput (fun x i => groupDilation (d + 1) hd (scales i) (canonicalSection d hd x))
      (fun x y : I → TruncGroup (L := L) law (d + 1) hd =>
        ∏ i, normalizedEntry (stageHidden hnil h points (d + 1) hd) (centralEmbedding hadd d hd)
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil h points d (by omega)) q r :=
  step_output hadd hnil h points invertible d hd (canonicalSection d hd)
    (canonicalSection_right_inverse d hd) chi labels nonzero_trace scales sde q r

omit [Finite L] in
/-- Terminal membership: the stage-one hidden subgroup is exactly `h`, as an
additive subgroup of `L`. -/
theorem terminal_membership (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (hc : 1 ≤ c)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (v : L) :
    Multiplicative.ofAdd v ∈
        (stageHidden hnil h points 1 hc).map (terminalGroupEquiv hadd hc).toMonoidHom ↔
      v ∈ h := by
  rw [stageHidden, Subgroup.map_map]
  change Multiplicative.ofAdd v ∈
    (ReesGeneralLaw.hiddenSubgroup hnil h points).map (terminalMap hadd hnil hc) ↔ _
  rw [terminal_hidden_image hadd hnil hc h points invertible]
  rfl

local instance originalFintype : Fintype L := Fintype.ofFinite _

/-- After the last step, the recovered source is the additive coset source of
ALL of `h = log H`, including its derived directions, in every class. -/
theorem terminal_source (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (hc : 1 ≤ c)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (x y : L) :
    CosetSourceFourier.groupEntry (stageHidden hnil h points 1 hc)
      ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd x))
      ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd y)) =
      if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  have hm := terminal_membership hadd hnil hc h points invertible (y - x)
  rw [Subgroup.mem_map_equiv] at hm
  have he : (Multiplicative.ofAdd (y - x) : Multiplicative L) =
      (Multiplicative.ofAdd x)⁻¹ * Multiplicative.ofAdd y := by
    change y - x = -x + y
    abel
  rw [he, map_mul, map_inv] at hm
  unfold CosetSourceFourier.groupEntry
  rw [hm]
  have hcard : Fintype.card (TruncGroup (L := L) law 1 hc) = Fintype.card L :=
    Fintype.card_congr ((terminalGroupEquiv hadd hc).toEquiv.trans
      (Multiplicative.toAdd : Multiplicative L ≃ L))
  simp only [AffineSupportErasure.invSize, hcard]

end Finite

end
end QSearch.ReesGeneralReceiver
