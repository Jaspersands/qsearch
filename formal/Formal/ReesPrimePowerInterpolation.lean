import Formal.ReesHomogenization
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-!
# Prime-power Rees interpolation

The public points 1,...,c have unit Vandermonde determinant over Z/(p^e)
when c < p. The coefficientwise hiding argument consequently works for any
module and submodule, without assuming a field or a free quotient. This is
the interpolation step only, not BCH/Lazard or the quantum algorithm.
-/

namespace QSearch.ReesPrimePowerInterpolation
open scoped BigOperators
open QSearch.ReesHomogenization
noncomputable section

variable {p e c : ℕ}

def points (p e c : ℕ) (i : Fin c) : ZMod (p ^ e) := (i.val + 1 : ℕ)

theorem small_nat_unit (hp : p.Prime) (he : 0 < e) {a : ℕ}
    (ha : 0 < a) (hap : a < p) : IsUnit (a : ZMod (p ^ e)) := by
  apply (ZMod.isUnit_natCast_iff_not_dvd_pow hp he).mpr
  exact Nat.not_dvd_of_pos_of_lt ha hap

theorem points_unit (hp : p.Prime) (he : 0 < e) (hc : c < p) (i : Fin c) :
    IsUnit (points p e c i) := by
  apply small_nat_unit hp he (by omega)
  omega

theorem difference_unit (hp : p.Prime) (he : 0 < e) (hc : c < p)
    (i j : Fin c) (hij : i < j) :
    IsUnit (points p e c j - points p e c i) := by
  have hv : i.val < j.val := hij
  have hd : 0 < j.val - i.val := Nat.sub_pos_of_lt hv
  have hdp : j.val - i.val < p := by omega
  have heq : points p e c j - points p e c i =
      ((j.val - i.val : ℕ) : ZMod (p ^ e)) := by
    simp only [points, Nat.cast_add, Nat.cast_one]
    rw [Nat.cast_sub (Nat.le_of_lt hv)]
    ring
  rw [heq]
  exact small_nat_unit hp he hd hdp

theorem evaluation_det_unit (hp : p.Prime) (he : 0 < e) (hc : c < p) :
    IsUnit (evaluationMatrix (points p e c)).det := by
  classical
  rw [evaluationMatrix, Matrix.det_mul, Matrix.det_diagonal, Matrix.det_vandermonde]
  apply IsUnit.mul
  · exact IsUnit.prod_iff.mpr fun i _ => points_unit hp he hc i
  · apply IsUnit.prod_iff.mpr
    intro i _
    apply IsUnit.prod_iff.mpr
    intro j hj
    exact difference_unit hp he hc i j (Finset.mem_Ioi.mp hj)

theorem coefficientwise_iff {V : Type*} [AddCommGroup V] [Module (ZMod (p ^ e)) V]
    (hp : p.Prime) (he : 0 < e) (hc : c < p)
    (h : Submodule (ZMod (p ^ e)) V) (v : Fin c → V) :
    (∀ i, applyRows (evaluationMatrix (points p e c)) v i ∈ h) ↔ ∀ j, v j ∈ h := by
  exact coefficientwise_iff_of_isUnit h (points p e c) (evaluation_det_unit hp he hc) v

theorem tuple_hides {V G K O : Type*} [AddCommGroup V] [Module (ZMod (p ^ e)) V]
    [Group G] [Group K] (hp : p.Prime) (he : 0 < e) (hc : c < p)
    (h : Submodule (ZMod (p ^ e)) V) (eval : Fin c → G →* K)
    (log : K → V) (coeff : G → Fin c → V)
    (evaluation : ∀ g i, log (eval i g) =
      applyRows (evaluationMatrix (points p e c)) (coeff g) i)
    (f : K → O) (hides : ∀ x y, f x = f y ↔ log (x⁻¹ * y) ∈ h)
    (a b : G) :
    (fun i => f (eval i a)) = (fun i => f (eval i b)) ↔
      ∀ j, coeff (a⁻¹ * b) j ∈ h := by
  exact tuple_hides_of_isUnit h (points p e c) (evaluation_det_unit hp he hc)
    eval log coeff evaluation f hides a b

/-- Distinct unit points still need unit differences over a prime-power ring. -/
def badPoints : Fin 2 → ZMod 9 := ![1, 4]

def badCoefficients : Fin 2 → ZMod 9 := ![6, 3]

theorem bad_points_distinct_units :
    badPoints 0 ≠ badPoints 1 ∧ IsUnit (badPoints 0) ∧ IsUnit (badPoints 1) := by
  exact ⟨by decide, isUnit_one, (ZMod.isUnit_iff_coprime 4 9).mpr (by decide)⟩

theorem bad_points_nonzero_nonunit_determinant :
    (evaluationMatrix badPoints).det ≠ 0 ∧ ¬ IsUnit (evaluationMatrix badPoints).det := by
  have hd : (evaluationMatrix badPoints).det = (3 : ZMod 9) := by
    rw [Matrix.det_fin_two]
    simp only [evaluationMatrix_apply]
    decide
  rw [hd]
  exact ⟨by decide, fun h => (by decide : ¬ Nat.Coprime 3 9)
    ((ZMod.isUnit_iff_coprime 3 9).mp h)⟩

theorem bad_points_lose_coefficients :
    (∀ i, applyRows (evaluationMatrix badPoints) badCoefficients i = 0) ∧
      badCoefficients 0 ≠ 0 := by
  constructor
  · intro i
    fin_cases i <;>
      norm_num [applyRows, Fin.sum_univ_two, evaluationMatrix_apply, badPoints,
        badCoefficients] <;> decide
  · decide

end
end QSearch.ReesPrimePowerInterpolation

/-- info: 'QSearch.ReesHomogenization.coefficientwise_iff_of_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.coefficientwise_iff_of_isUnit

/-- info: 'QSearch.ReesHomogenization.tuple_hides_of_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesHomogenization.tuple_hides_of_isUnit

/-- info: 'QSearch.ReesPrimePowerInterpolation.evaluation_det_unit' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.evaluation_det_unit

/-- info: 'QSearch.ReesPrimePowerInterpolation.coefficientwise_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.coefficientwise_iff

/-- info: 'QSearch.ReesPrimePowerInterpolation.tuple_hides' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesPrimePowerInterpolation.tuple_hides

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_distinct_units' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_distinct_units

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_nonzero_nonunit_determinant' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_nonzero_nonunit_determinant

/-- info: 'QSearch.ReesPrimePowerInterpolation.bad_points_lose_coefficients' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesPrimePowerInterpolation.bad_points_lose_coefficients
