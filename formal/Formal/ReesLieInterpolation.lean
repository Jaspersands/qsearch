import Formal.ReesLieConstruction
import Formal.ReesPrimePowerInterpolation

/-!
# Concrete Rees interpolation and hidden-subalgebra preservation

This connects the actual current-algebra evaluation to the interpolation
matrix. The hidden cover is an actual Lie subalgebra, defined by evaluation
preimages; its coefficientwise characterization and dilation invariance
are conclusions. The hidden subalgebra need not be an ideal or graded.
BCH/Lazard transport to groups remains a separate obligation.
-/

namespace QSearch.ReesLieInterpolation
open scoped BigOperators
open QSearch.ReesLieConstruction QSearch.ReesHomogenization
noncomputable section

variable {R L : Type*} [CommRing R] [LieRing L] [LieAlgebra R L] {c : ℕ}

def positiveCoefficients (c : ℕ) (z : rees (R := R) (L := L)) (i : Fin c) : L :=
  coeff (z : Current R L) (i.val + 1)

theorem evaluation_finite (hnil : LieModule.lowerCentralSeries R L L c = ⊥)
    (a : R) (z : rees (R := R) (L := L)) :
    evaluation a z = ∑ i : Fin c, a ^ (i.val + 1) • positiveCoefficients c z i := by
  classical
  have hs : (coeff (z : Current R L)).support ⊆ Finset.range (c + 1) := by
    intro r hr
    rw [Finset.mem_range]
    by_contra hn
    exact (Finsupp.mem_support_iff.mp hr)
      ((nilpotent_cutoff c hnil).1 (z : Current R L) z.property r (by omega))
  rw [evaluation_formula, Finsupp.sum_of_support_subset _ hs _ (by intros; simp)]
  rw [Finset.sum_range_succ']
  have h0 := (mem_rees_iff (z : Current R L)).mp z.property |>.1
  simp only [h0, smul_zero, add_zero]
  rw [← Fin.sum_univ_eq_sum_range]
  rfl

theorem evaluation_rows (hnil : LieModule.lowerCentralSeries R L L c = ⊥)
    (points : Fin c → R) (z : rees (R := R) (L := L)) (i : Fin c) :
    evaluation (points i) z =
      applyRows (evaluationMatrix points) (positiveCoefficients c z) i := by
  simpa only [applyRows, evaluationMatrix_apply] using evaluation_finite hnil (points i) z

/-- The intersection of preimages under actual Lie evaluation maps. -/
def hiddenCover (h : LieSubalgebra R L) (points : Fin c → R) :
    LieSubalgebra R (rees (R := R) (L := L)) where
  carrier := {z | ∀ i, evaluation (points i) z ∈ h}
  zero_mem' := by intro i; simp
  add_mem' := by
    intro x y hx hy i
    rw [map_add]
    exact h.add_mem (hx i) (hy i)
  smul_mem' := by
    intro a x hx i
    rw [map_smul]
    exact h.smul_mem a (hx i)
  lie_mem' := by
    intro x y hx hy i
    rw [(evaluation (points i)).map_lie]
    exact h.lie_mem (hx i) (hy i)

theorem mem_hiddenCover_iff (hnil : LieModule.lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det)
    (z : rees (R := R) (L := L)) :
    z ∈ hiddenCover h points ↔ ∀ i, positiveCoefficients c z i ∈ h := by
  change (∀ i, evaluation (points i) z ∈ h) ↔ _
  simp_rw [evaluation_rows hnil]
  exact coefficientwise_iff_of_isUnit h.toSubmodule points invertible (positiveCoefficients c z)

theorem scaling_preserves_hiddenCover (hnil : LieModule.lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det)
    (a : R) (z : rees (R := R) (L := L)) (hz : z ∈ hiddenCover h points) :
    scaling a z ∈ hiddenCover h points := by
  apply (mem_hiddenCover_iff hnil h points invertible _).mpr
  have hz' := (mem_hiddenCover_iff hnil h points invertible z).mp hz
  intro i
  change coeff (scaling a z : Current R L) (i.val + 1) ∈ h
  rw [scaling_coeff]
  exact h.smul_mem _ (hz' i)

theorem dilation_mem_iff (hnil : LieModule.lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det)
    (u : Rˣ) (z : rees (R := R) (L := L)) :
    dilation u z ∈ hiddenCover h points ↔ z ∈ hiddenCover h points := by
  constructor
  · intro hz
    have hi := scaling_preserves_hiddenCover hnil h points invertible
      (↑u⁻¹ : R) (dilation u z) hz
    change (dilation u).symm (dilation u z) ∈ hiddenCover h points at hi
    simpa only [LieEquiv.symm_apply_apply] using hi
  · exact scaling_preserves_hiddenCover hnil h points invertible (u : R) z

theorem prime_power_hiddenCover_iff {p e c : ℕ} {L : Type*}
    [LieRing L] [LieAlgebra (ZMod (p ^ e)) L]
    (hp : p.Prime) (he : 0 < e) (hc : c < p)
    (hnil : LieModule.lowerCentralSeries (ZMod (p ^ e)) L L c = ⊥)
    (h : LieSubalgebra (ZMod (p ^ e)) L)
    (z : rees (R := ZMod (p ^ e)) (L := L)) :
    z ∈ hiddenCover h (ReesPrimePowerInterpolation.points p e c) ↔
      ∀ i, positiveCoefficients c z i ∈ h := by
  exact mem_hiddenCover_iff hnil h _
    (ReesPrimePowerInterpolation.evaluation_det_unit hp he hc) z

end
end QSearch.ReesLieInterpolation

/-- info: 'QSearch.ReesLieInterpolation.evaluation_finite' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.evaluation_finite

/-- info: 'QSearch.ReesLieInterpolation.evaluation_rows' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.evaluation_rows

/-- info: 'QSearch.ReesLieInterpolation.hiddenCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.hiddenCover

/-- info: 'QSearch.ReesLieInterpolation.mem_hiddenCover_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.mem_hiddenCover_iff

/-- info: 'QSearch.ReesLieInterpolation.scaling_preserves_hiddenCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.scaling_preserves_hiddenCover

/-- info: 'QSearch.ReesLieInterpolation.dilation_mem_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.dilation_mem_iff

/-- info: 'QSearch.ReesLieInterpolation.prime_power_hiddenCover_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieInterpolation.prime_power_hiddenCover_iff
