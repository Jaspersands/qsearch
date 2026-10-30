import Formal.ReesCentralQuotient
import Formal.ReesGroupClassThree
import Mathlib.GroupTheory.QuotientGroup.Basic
import Mathlib.GroupTheory.Subgroup.Center

/-!
# BCH groups of the actual Rees central quotients

For `d ≤ 3`, `TruncGroup d` is the BCH group of the actual Lie quotient
`A / F_{>d}`. The maps, central kernels, additive coefficient embeddings, and
unit-dilation weights are derived from that quotient. `fullGroupEquiv` proves
the connection to the original class-three Rees group. The terminal group is
identified with additive `L`, not with `L` carrying its original BCH law.
-/

namespace QSearch.ReesCentralQuotientBCH

open LieModule QSearch.ReesLieConstruction QSearch.ReesCentralQuotient
open QSearch.BCHClassThree QSearch.ReesGroupClassThree

noncomputable section

set_option backward.isDefEq.respectTransparency false

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

/-- The actual quotient bound supplies the premise of the cubic BCH construction. -/
theorem trunc_classThree (d : ℕ) (hd : d ≤ 3) :
    lowerCentralSeries F (Trunc (R := F) (L := L) d) (Trunc (R := F) (L := L) d) 3 = ⊥ := by
  apply eq_bot_iff.mpr
  intro x hx
  have h := antitone_lowerCentralSeries F (Trunc (R := F) (L := L) d)
    (Trunc (R := F) (L := L) d) hd hx
  simpa only [trunc_class_bound, LieSubmodule.mem_bot] using h

abbrev TruncGroup (d : ℕ) (hd : d ≤ 3) :=
  BCH F (Trunc (R := F) (L := L) d) (trunc_classThree d hd)

instance finiteTruncGroup (d : ℕ) (hd : d ≤ 3) [Finite L] :
    Finite (TruncGroup (F := F) (L := L) d hd) :=
  Finite.of_injective BCH.val (fun _ _ h => BCH.ext h)

variable [NeZero (2 : F)] [NeZero (3 : F)]

/-- The actual BCH projection to a lower-degree quotient. -/
def projectHom {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d) :
    TruncGroup (F := F) (L := L) d hd →* TruncGroup (F := F) (L := L) e he :=
  lieHom (trunc_classThree d hd) (trunc_classThree e he) (projection h)

@[simp] theorem projectHom_val {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d)
    (x : TruncGroup (F := F) (L := L) d hd) :
    (projectHom hd he h x).val = projection h x.val := rfl

theorem projectHom_surjective {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d) :
    Function.Surjective (projectHom (F := F) (L := L) hd he h) := by
  intro x
  obtain ⟨y, hy⟩ := projection_surjective h x.val
  exact ⟨BCH.mk y, BCH.ext hy⟩

/-- The first isomorphism theorem applies to these actual projection kernels. -/
def stepQuotientEquiv {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d) :
    TruncGroup (F := F) (L := L) d hd ⧸ (projectHom hd he h).ker ≃*
      TruncGroup (F := F) (L := L) e he :=
  QuotientGroup.quotientKerEquivOfSurjective (projectHom hd he h)
    (projectHom_surjective hd he h)

/-- The original Rees BCH group maps canonically to every truncation. -/
def groupMk (hnil : lowerCentralSeries F L L 3 = ⊥) (d : ℕ) (hd : d ≤ 3) :
    ReesGroup hnil →* TruncGroup (F := F) (L := L) d hd :=
  lieHom (rees_class_bound 3 hnil) (trunc_classThree d hd) (mk d)

@[simp] theorem groupMk_val (hnil : lowerCentralSeries F L L 3 = ⊥)
    (d : ℕ) (hd : d ≤ 3) (x : ReesGroup hnil) :
    (groupMk hnil d hd x).val = mk d x.val := rfl

theorem groupMk_surjective (hnil : lowerCentralSeries F L L 3 = ⊥)
    (d : ℕ) (hd : d ≤ 3) : Function.Surjective (groupMk (L := L) hnil d hd) := by
  intro x
  obtain ⟨y, hy⟩ := mk_surjective d x.val
  exact ⟨BCH.mk y, BCH.ext hy⟩

theorem groupMk_kernel (hnil : lowerCentralSeries F L L 3 = ⊥)
    (d : ℕ) (hd : d ≤ 3) (x : ReesGroup hnil) :
    x ∈ (groupMk hnil d hd).ker ↔ x.val ∈ tail d := by
  rw [MonoidHom.mem_ker]
  constructor
  · intro h
    exact (mk_eq_zero d x.val).mp (congrArg BCH.val h)
  · intro h
    exact BCH.ext ((mk_eq_zero d x.val).mpr h)

theorem projectHom_groupMk (hnil : lowerCentralSeries F L L 3 = ⊥)
    {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d) (x : ReesGroup hnil) :
    projectHom hd he h (groupMk hnil d hd x) = groupMk hnil e he x := rfl

/-- This proves that degree-three truncation is the original actual Rees group. -/
def fullGroupEquiv (hnil : lowerCentralSeries F L L 3 = ⊥) :
    ReesGroup hnil ≃* TruncGroup (F := F) (L := L) 3 (by decide) :=
  lieEquiv (rees_class_bound 3 hnil) (trunc_classThree 3 (by decide)) (fullEquiv 3 hnil)

@[simp] theorem fullGroupEquiv_apply (hnil : lowerCentralSeries F L L 3 = ⊥)
    (x : ReesGroup hnil) : fullGroupEquiv hnil x = groupMk hnil 3 (by decide) x := rfl

instance finiteOriginalReesGroup [Finite L] (hnil : lowerCentralSeries F L L 3 = ⊥) :
    Finite (ReesGroup hnil) :=
  Finite.of_injective (fullGroupEquiv hnil) (fullGroupEquiv hnil).injective

/-- A central Lie kernel is central for the proved BCH multiplication. -/
theorem projectHom_kernel_central (d : ℕ) (hd : d + 1 ≤ 3) :
    (projectHom (F := F) (L := L) hd (by omega) (Nat.le_succ d)).ker ≤
      Subgroup.center (TruncGroup (F := F) (L := L) (d + 1) hd) := by
  intro y hy
  apply Subgroup.mem_center_iff.mpr
  intro x
  have hy0 : projection (Nat.le_succ d) y.val = 0 :=
    congrArg BCH.val (MonoidHom.mem_ker.mp hy)
  have hxy := top_kernel_central d x.val y.val hy0
  have hyx : ⁅y.val, x.val⁆ = 0 := by rw [← lie_skew, hxy, neg_zero]
  apply BCH.ext
  simp only [val_mul, bch, hxy, hyx, lie_zero, add_zero, smul_zero]
  exact add_comm _ _

/-- The receiver's coefficient carrier embeds by exponentiating actual top currents. -/
def centralEmbedding (d : ℕ) (hd : d + 1 ≤ 3) :
    Multiplicative (gamma F L (d + 1)) →* TruncGroup (F := F) (L := L) (d + 1) hd where
  toFun v := BCH.mk (topEmbedding d v.toAdd)
  map_one' := BCH.ext (map_zero _)
  map_mul' x y := by
    apply BCH.ext
    change topEmbedding d (x.toAdd + y.toAdd) = bch (F := F) _ _
    rw [map_add]
    simp only [bch, topEmbedding_central, lie_zero, smul_zero, add_zero]

@[simp] theorem centralEmbedding_val (d : ℕ) (hd : d + 1 ≤ 3)
    (v : Multiplicative (gamma F L (d + 1))) :
    (centralEmbedding d hd v).val = topEmbedding d v.toAdd := rfl

theorem centralEmbedding_injective (d : ℕ) (hd : d + 1 ≤ 3) :
    Function.Injective (centralEmbedding (F := F) (L := L) d hd) := by
  intro x y h
  exact (topEmbedding_injective d) (congrArg BCH.val h)

/-- Exact kernel/range identity required by the actual quotient receiver. -/
theorem projectHom_kernel_eq_range (d : ℕ) (hd : d + 1 ≤ 3) :
    (projectHom (F := F) (L := L) hd (by omega) (Nat.le_succ d)).ker =
      (centralEmbedding d hd).range := by
  ext x
  rw [MonoidHom.mem_ker, MonoidHom.mem_range]
  constructor
  · intro hx
    obtain ⟨v, hv⟩ := (top_kernel_iff d x.val).mp (congrArg BCH.val hx)
    exact ⟨Multiplicative.ofAdd v, BCH.ext hv⟩
  · rintro ⟨v, rfl⟩
    exact BCH.ext (projection_topEmbedding d v.toAdd)

theorem centralEmbedding_central (d : ℕ) (hd : d + 1 ≤ 3)
    (v : Multiplicative (gamma F L (d + 1))) :
    centralEmbedding d hd v ∈ Subgroup.center (TruncGroup (F := F) (L := L) (d + 1) hd) := by
  apply projectHom_kernel_central d hd
  rw [projectHom_kernel_eq_range]
  exact ⟨v, rfl⟩

def groupDilation (d : ℕ) (hd : d ≤ 3) (u : Fˣ) :
    TruncGroup (F := F) (L := L) d hd ≃* TruncGroup (F := F) (L := L) d hd :=
  lieEquiv (trunc_classThree d hd) (trunc_classThree d hd) (quotientDilation d u)

@[simp] theorem groupDilation_val (d : ℕ) (hd : d ≤ 3) (u : Fˣ)
    (x : TruncGroup (F := F) (L := L) d hd) :
    (groupDilation d hd u x).val = quotientDilation d u x.val := rfl

/-- The exact `u^(d+1)` center action, on the receiver's additive carrier. -/
theorem groupDilation_centralEmbedding (d : ℕ) (hd : d + 1 ≤ 3) (u : Fˣ)
    (v : Multiplicative (gamma F L (d + 1))) :
    groupDilation (d + 1) hd u (centralEmbedding d hd v) =
      centralEmbedding d hd (Multiplicative.ofAdd ((u : F) ^ (d + 1) • v.toAdd)) :=
  BCH.ext (dilation_topEmbedding d u v.toAdd)

theorem groupDilation_groupMk (hnil : lowerCentralSeries F L L 3 = ⊥)
    (d : ℕ) (hd : d ≤ 3) (u : Fˣ) (x : ReesGroup hnil) :
    groupDilation d hd u (groupMk hnil d hd x) = groupMk hnil d hd (dilationEquiv hnil u x) :=
  rfl

theorem projectHom_dilation {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (h : e ≤ d)
    (u : Fˣ) (x : TruncGroup (F := F) (L := L) d hd) :
    projectHom hd he h (groupDilation d hd u x) = groupDilation e he u (projectHom hd he h x) :=
  BCH.ext (projection_dilation h u x.val)

/-- Concrete degree-three to degree-two transition. -/
abbrev pi32 : TruncGroup (F := F) (L := L) 3 (by decide) →*
    TruncGroup (F := F) (L := L) 2 (by decide) :=
  projectHom (by decide) (by decide) (by decide)

/-- Concrete degree-two to degree-one transition. -/
abbrev pi21 : TruncGroup (F := F) (L := L) 2 (by decide) →*
    TruncGroup (F := F) (L := L) 1 (by decide) :=
  projectHom (by decide) (by decide) (by decide)

theorem pi32_kernel_eq_range :
    (pi32 (F := F) (L := L)).ker = (centralEmbedding 2 (by decide)).range :=
  projectHom_kernel_eq_range 2 (by decide)

theorem pi21_kernel_eq_range :
    (pi21 (F := F) (L := L)).ker = (centralEmbedding 1 (by decide)).range :=
  projectHom_kernel_eq_range 1 (by decide)

theorem pi32_kernel_central :
    (pi32 (F := F) (L := L)).ker ≤
      Subgroup.center (TruncGroup (F := F) (L := L) 3 (by decide)) :=
  projectHom_kernel_central 2 (by decide)

theorem pi21_kernel_central :
    (pi21 (F := F) (L := L)).ker ≤
      Subgroup.center (TruncGroup (F := F) (L := L) 2 (by decide)) :=
  projectHom_kernel_central 1 (by decide)

-- These checks exercise the concrete receiver carriers without an ambient-current finiteness premise.
example [Finite L] : Fintype (TruncGroup (F := F) (L := L) 3 (by decide)) :=
  Fintype.ofFinite _

example [Finite L] : Fintype (TruncGroup (F := F) (L := L) 2 (by decide)) :=
  Fintype.ofFinite _

example [Finite L] : Fintype (TruncGroup (F := F) (L := L) 1 (by decide)) :=
  Fintype.ofFinite _

example [Finite L] : Fintype (Multiplicative (gamma F L 3)) :=
  Fintype.ofFinite _

example [Finite L] : Fintype (Multiplicative (gamma F L 2)) :=
  Fintype.ofFinite _

/-- Terminal BCH multiplication is exactly the original addition on `L`. -/
def terminalGroupEquiv : TruncGroup (F := F) (L := L) 1 (by decide) ≃* Multiplicative L where
  toFun x := Multiplicative.ofAdd (terminalEquiv x.val)
  invFun x := BCH.mk (terminalEquiv.symm x.toAdd)
  left_inv x := BCH.ext (terminalEquiv.symm_apply_apply x.val)
  right_inv x := terminalEquiv.apply_symm_apply x.toAdd
  map_mul' x y := by
    change terminalEquiv (bch (F := F) x.val y.val) = terminalEquiv x.val + terminalEquiv y.val
    simp only [bch, terminal_bracket, lie_zero, smul_zero, add_zero, map_add]

def terminalMap (hnil : lowerCentralSeries F L L 3 = ⊥) : ReesGroup hnil →* Multiplicative L :=
  terminalGroupEquiv.toMonoidHom.comp (groupMk hnil 1 (by decide))

@[simp] theorem terminalMap_apply (hnil : lowerCentralSeries F L L 3 = ⊥)
    (x : ReesGroup hnil) :
    terminalMap hnil x = Multiplicative.ofAdd (coefficient 1 x.val) := rfl

/-- Hidden subgroups at each stage are actual images, with no normality premise. -/
def hiddenImage (hnil : lowerCentralSeries F L L 3 = ⊥) (h : LieSubalgebra F L)
    (points : Fin 3 → F) (d : ℕ) (hd : d ≤ 3) :
    Subgroup (TruncGroup (F := F) (L := L) d hd) :=
  (hiddenSubgroup hnil h points).map (groupMk hnil d hd)

theorem projectHom_hiddenImage (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    {d e : ℕ} (hd : d ≤ 3) (he : e ≤ 3) (hle : e ≤ d) :
    (hiddenImage hnil h points d hd).map (projectHom hd he hle) =
      hiddenImage hnil h points e he := by
  simp only [hiddenImage, Subgroup.map_map]
  rfl

private theorem dilation_hiddenImage_forward (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (ReesHomogenization.evaluationMatrix points).det)
    (d : ℕ) (hd : d ≤ 3) (u : Fˣ) (x : TruncGroup (F := F) (L := L) d hd)
    (hx : x ∈ hiddenImage hnil h points d hd) :
    groupDilation d hd u x ∈ hiddenImage hnil h points d hd := by
  obtain ⟨y, hy, rfl⟩ := hx
  rw [groupDilation_groupMk]
  exact ⟨dilationEquiv hnil u y,
    (dilation_hidden_iff hnil h points invertible u y).mpr hy, rfl⟩

/-- Dilation preserves each actual hidden image, not just an assumed coordinate subgroup. -/
theorem dilation_hiddenImage_iff (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (ReesHomogenization.evaluationMatrix points).det)
    (d : ℕ) (hd : d ≤ 3) (u : Fˣ) (x : TruncGroup (F := F) (L := L) d hd) :
    groupDilation d hd u x ∈ hiddenImage hnil h points d hd ↔
      x ∈ hiddenImage hnil h points d hd := by
  constructor
  · intro hx
    have hi := dilation_hiddenImage_forward hnil h points invertible d hd u⁻¹ _ hx
    change (groupDilation d hd u).symm (groupDilation d hd u x) ∈
      hiddenImage hnil h points d hd at hi
    simpa only [MulEquiv.symm_apply_apply] using hi
  · exact dilation_hiddenImage_forward hnil h points invertible d hd u x

/-- The terminal hidden image retains all of `h`, including its derived directions. -/
theorem terminal_hidden_image (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (ReesHomogenization.evaluationMatrix points).det) :
    (hiddenSubgroup hnil h points).map (terminalMap hnil) =
      h.toSubmodule.toAddSubgroup.toSubgroup := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    change coefficient 1 x.val ∈ h
    exact (mem_hiddenSubgroup_iff hnil h points invertible x).mp hx 0
  · intro hy
    change y.toAdd ∈ h at hy
    refine ⟨BCH.mk (gradeOne y.toAdd), ?_, ?_⟩
    · apply (mem_hiddenSubgroup_iff hnil h points invertible _).mpr
      intro i
      change coefficient (i.val + 1) (gradeOne y.toAdd) ∈ h
      rw [coefficient_gradeOne]
      by_cases hi : i.val + 1 = 1
      · simpa only [hi, Finsupp.single_eq_same] using hy
      · rw [Finsupp.single_eq_of_ne hi]
        exact h.zero_mem
    · change Multiplicative.ofAdd (coefficient 1 (gradeOne y.toAdd)) = y
      rw [coefficient_gradeOne, Finsupp.single_eq_same]
      rfl

section PrimeField

variable {p : ℕ} [Fact p.Prime] {V : Type*} [LieRing V] [LieAlgebra (ZMod p) V]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]

open QSearch.BCHClassThreeSubgroups

/-- For arbitrary prime-field `H`, terminal membership is exactly its original
logarithm set. Additivity is inherited only from the existing proved prime
correspondence; neither normality nor extension-field linearity is assumed. -/
theorem terminal_arbitrary_subgroup
    (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) (v : V) :
    Multiplicative.ofAdd v ∈ (liftedSubgroup hnil H).map (terminalMap hnil) ↔
      BCH.mk v ∈ H := by
  change Multiplicative.ofAdd v ∈
    (hiddenSubgroup hnil (toLieSubalgebra hnil H) canonicalPoints).map (terminalMap hnil) ↔ _
  rw [terminal_hidden_image hnil (toLieSubalgebra hnil H) canonicalPoints canonical_det_unit]
  rfl

theorem dilation_arbitrary_image
    (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) (d : ℕ) (hd : d ≤ 3) (u : (ZMod p)ˣ)
    (x : TruncGroup (F := ZMod p) (L := V) d hd) :
    groupDilation d hd u x ∈ (liftedSubgroup hnil H).map (groupMk hnil d hd) ↔
      x ∈ (liftedSubgroup hnil H).map (groupMk hnil d hd) :=
  dilation_hiddenImage_iff hnil (toLieSubalgebra hnil H) canonicalPoints
    canonical_det_unit d hd u x

end PrimeField

end
end QSearch.ReesCentralQuotientBCH

/-- info: 'QSearch.ReesCentralQuotientBCH.trunc_classThree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.trunc_classThree

/-- info: 'QSearch.ReesCentralQuotientBCH.finiteTruncGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.finiteTruncGroup

/-- info: 'QSearch.ReesCentralQuotientBCH.stepQuotientEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.stepQuotientEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.fullGroupEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.fullGroupEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.centralEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.centralEmbedding

/-- info: 'QSearch.ReesCentralQuotientBCH.centralEmbedding_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.centralEmbedding_injective

/-- info: 'QSearch.ReesCentralQuotientBCH.pi32_kernel_eq_range' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.pi32_kernel_eq_range

/-- info: 'QSearch.ReesCentralQuotientBCH.pi21_kernel_eq_range' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.pi21_kernel_eq_range

/-- info: 'QSearch.ReesCentralQuotientBCH.projectHom_kernel_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.projectHom_kernel_central

/--
info: 'QSearch.ReesCentralQuotientBCH.groupDilation_centralEmbedding' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.groupDilation_centralEmbedding

/-- info: 'QSearch.ReesCentralQuotientBCH.dilation_hiddenImage_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.dilation_hiddenImage_iff

/-- info: 'QSearch.ReesCentralQuotientBCH.terminalGroupEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.terminalGroupEquiv

/-- info: 'QSearch.ReesCentralQuotientBCH.terminal_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotientBCH.terminal_arbitrary_subgroup
