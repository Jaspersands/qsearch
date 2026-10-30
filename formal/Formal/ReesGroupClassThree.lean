import Formal.BCHClassThree
import Formal.BCHClassThreeSubgroups
import Formal.ReesLieInterpolation

/-!
# Concrete class-three Rees group hiding

The evaluation group homomorphisms and their coefficient identities are
constructed here, not hypotheses of the tuple-hiding theorem. The hidden
group is induced by a Lie subalgebra, which need not be an ideal or graded.
The prime-field specialization derives the hidden Lie subalgebra from an
arbitrary group subgroup. The quantum receiver is not asserted here.
-/

namespace QSearch.ReesGroupClassThree

open LieModule
open QSearch.ReesLieConstruction QSearch.ReesLieInterpolation
open QSearch.ReesHomogenization QSearch.BCHClassThree

noncomputable section

variable {F L O : Type*} [Field F] [LieRing L] [LieAlgebra F L]

def canonicalPoints : Fin 3 → F := ![1, 2, 3]

theorem canonical_det : (evaluationMatrix (canonicalPoints (F := F))).det = 12 := by
  rw [Matrix.det_fin_three]
  norm_num [evaluationMatrix_apply, canonicalPoints]

variable [NeZero (2 : F)] [NeZero (3 : F)]

theorem canonical_det_unit : IsUnit (evaluationMatrix (canonicalPoints (F := F))).det := by
  rw [canonical_det, isUnit_iff_ne_zero, show (12 : F) = 2 * 2 * 3 by ring]
  exact mul_ne_zero (mul_ne_zero (NeZero.ne 2) (NeZero.ne 2)) (NeZero.ne 3)

/-- A Lie subalgebra is closed under the actual cubic BCH group law. -/
def subgroupOfLie (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) : Subgroup (BCH F L hnil) where
  carrier := {x | x.val ∈ h}
  one_mem' := h.zero_mem
  mul_mem' := by
    intro x y hx hy
    change bch (F := F) x.val y.val ∈ h
    exact h.add_mem
      (h.add_mem (h.add_mem hx hy) (h.smul_mem _ (h.lie_mem hx hy)))
      (h.smul_mem _ (h.add_mem (h.lie_mem hx (h.lie_mem hx hy))
        (h.lie_mem hy (h.lie_mem hy hx))))
  inv_mem' := fun hx => h.neg_mem hx

@[simp] theorem mem_subgroupOfLie (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (x : BCH F L hnil) :
    x ∈ subgroupOfLie hnil h ↔ x.val ∈ h := Iff.rfl

abbrev ReesGroup (hnil : lowerCentralSeries F L L 3 = ⊥) :=
  BCH F (rees (R := F) (L := L)) (rees_class_bound 3 hnil)

/-- This group map is induced by the concrete current-algebra evaluation. -/
def evaluationHom (hnil : lowerCentralSeries F L L 3 = ⊥) (s : F) :
    ReesGroup hnil →* BCH F L hnil :=
  lieHom (rees_class_bound 3 hnil) hnil (evaluation s)

@[simp] theorem evaluationHom_val (hnil : lowerCentralSeries F L L 3 = ⊥)
    (s : F) (x : ReesGroup hnil) :
    (evaluationHom hnil s x).val = evaluation s x.val := rfl

theorem evaluation_identity (hnil : lowerCentralSeries F L L 3 = ⊥)
    (points : Fin 3 → F) (x : ReesGroup hnil) (i : Fin 3) :
    (evaluationHom hnil (points i) x).val =
      applyRows (evaluationMatrix points) (positiveCoefficients 3 x.val) i :=
  evaluation_rows hnil points x.val i

/-- The actual hidden subgroup, with no ideal or homogeneity premise on h. -/
def hiddenSubgroup (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F) : Subgroup (ReesGroup hnil) :=
  subgroupOfLie (rees_class_bound 3 hnil) (hiddenCover h points)

theorem mem_hiddenSubgroup_iff (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (evaluationMatrix points).det) (x : ReesGroup hnil) :
    x ∈ hiddenSubgroup hnil h points ↔ ∀ i, positiveCoefficients 3 x.val i ∈ h :=
  mem_hiddenCover_iff hnil h points invertible x.val

/-- The old tuple interface is now instantiated by actual groups and maps. -/
theorem tuple_hides (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (f : BCH F L hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ subgroupOfLie hnil h)
    (a b : ReesGroup hnil) :
    (fun i => f (evaluationHom hnil (points i) a)) =
        (fun i => f (evaluationHom hnil (points i) b)) ↔
      ∀ j, positiveCoefficients 3 (a⁻¹ * b).val j ∈ h := by
  exact tuple_hides_of_isUnit h.toSubmodule points invertible
    (fun i => evaluationHom hnil (points i)) BCH.val
    (fun x => positiveCoefficients 3 x.val)
    (evaluation_identity hnil points) f hides a b

theorem tuple_hides_subgroup (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (f : BCH F L hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ subgroupOfLie hnil h)
    (a b : ReesGroup hnil) :
    (fun i => f (evaluationHom hnil (points i) a)) =
        (fun i => f (evaluationHom hnil (points i) b)) ↔
      a⁻¹ * b ∈ hiddenSubgroup hnil h points := by
  rw [tuple_hides hnil h points invertible f hides a b,
    mem_hiddenSubgroup_iff hnil h points invertible]

/-- Unit dilations are automorphisms of the actual BCH group. -/
def dilationEquiv (hnil : lowerCentralSeries F L L 3 = ⊥) (u : Fˣ) :
    ReesGroup hnil ≃* ReesGroup hnil :=
  lieEquiv (rees_class_bound 3 hnil) (rees_class_bound 3 hnil) (dilation u)

theorem dilation_hidden_iff (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h : LieSubalgebra F L) (points : Fin 3 → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (u : Fˣ) (x : ReesGroup hnil) :
    dilationEquiv hnil u x ∈ hiddenSubgroup hnil h points ↔
      x ∈ hiddenSubgroup hnil h points :=
  dilation_mem_iff hnil h points invertible u x.val

section PrimeField

variable {p : ℕ} [Fact p.Prime] {V : Type*} [LieRing V] [LieAlgebra (ZMod p) V]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]

open QSearch.BCHClassThreeSubgroups

theorem arbitrary_subgroup_roundtrip (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) :
    subgroupOfLie hnil (toLieSubalgebra hnil H) = H := by
  ext x
  rfl

/-- Canonical lifted subgroup for arbitrary H, with no supplied log-H space. -/
def liftedSubgroup (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) : Subgroup (ReesGroup hnil) :=
  hiddenSubgroup hnil (toLieSubalgebra hnil H) canonicalPoints

theorem lifted_mem_coefficients (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) (x : ReesGroup hnil) :
    x ∈ liftedSubgroup hnil H ↔
      ∀ i, BCH.mk (positiveCoefficients 3 x.val i) ∈ H := by
  exact mem_hiddenSubgroup_iff hnil (toLieSubalgebra hnil H)
    canonicalPoints canonical_det_unit x

theorem tuple_hides_arbitrary_subgroup
    (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) (f : BCH (ZMod p) V hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) (a b : ReesGroup hnil) :
    (fun i => f (evaluationHom hnil (canonicalPoints i) a)) =
        (fun i => f (evaluationHom hnil (canonicalPoints i) b)) ↔
      a⁻¹ * b ∈ liftedSubgroup hnil H := by
  apply tuple_hides_subgroup hnil (toLieSubalgebra hnil H)
    canonicalPoints canonical_det_unit f _ a b
  simpa only [arbitrary_subgroup_roundtrip] using hides

theorem dilation_arbitrary_subgroup
    (hnil : lowerCentralSeries (ZMod p) V V 3 = ⊥)
    (H : Subgroup (BCH (ZMod p) V hnil)) (u : (ZMod p)ˣ) (x : ReesGroup hnil) :
    dilationEquiv hnil u x ∈ liftedSubgroup hnil H ↔ x ∈ liftedSubgroup hnil H :=
  dilation_hidden_iff hnil (toLieSubalgebra hnil H)
    canonicalPoints canonical_det_unit u x

end PrimeField

end
end QSearch.ReesGroupClassThree

/-- info: 'QSearch.ReesGroupClassThree.canonical_det' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.canonical_det

/-- info: 'QSearch.ReesGroupClassThree.canonical_det_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.canonical_det_unit

/-- info: 'QSearch.ReesGroupClassThree.subgroupOfLie' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.subgroupOfLie

/-- info: 'QSearch.ReesGroupClassThree.evaluationHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.evaluationHom

/-- info: 'QSearch.ReesGroupClassThree.evaluation_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.evaluation_identity

/-- info: 'QSearch.ReesGroupClassThree.mem_hiddenSubgroup_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.mem_hiddenSubgroup_iff

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides_subgroup

/-- info: 'QSearch.ReesGroupClassThree.dilationEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilationEquiv

/-- info: 'QSearch.ReesGroupClassThree.dilation_hidden_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilation_hidden_iff

/-- info: 'QSearch.ReesGroupClassThree.arbitrary_subgroup_roundtrip' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.arbitrary_subgroup_roundtrip

/-- info: 'QSearch.ReesGroupClassThree.lifted_mem_coefficients' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.lifted_mem_coefficients

/-- info: 'QSearch.ReesGroupClassThree.tuple_hides_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.tuple_hides_arbitrary_subgroup

/-- info: 'QSearch.ReesGroupClassThree.dilation_arbitrary_subgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesGroupClassThree.dilation_arbitrary_subgroup
