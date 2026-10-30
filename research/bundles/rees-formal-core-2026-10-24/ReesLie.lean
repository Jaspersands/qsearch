import ReesHomogenization
import Mathlib.Algebra.Lie.Nilpotent

/-!
The positive lower-central Rees cover represented by its evaluations.
This file constructs a genuine Lie subalgebra, not a truncated bracket
whose Jacobi identity or evaluation homomorphisms are assumed.
It does not construct BCH groups or quantum operations.
-/

namespace QSearch.ReesLie
open scoped BigOperators
open LieModule
noncomputable section

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

/-- Mathlib indexes the series from zero: index i is gamma_(i+1). -/
theorem lowerCentral_bracket (i j : ℕ) :
    ⁅lowerCentralSeries F L L i, lowerCentralSeries F L L j⁆ ≤
      lowerCentralSeries F L L (i + j + 1) := by
  induction i generalizing j with
  | zero => simp [lowerCentralSeries_zero, lowerCentralSeries_succ]
  | succ i ih =>
    rw [LieSubmodule.lie_le_iff]
    intro x hx
    rw [lowerCentralSeries_succ] at hx
    change x ∈ LieSubmodule.toSubmodule
      ⁅(⊤ : LieIdeal F L), lowerCentralSeries F L L i⁆ at hx
    rw [LieSubmodule.lieIdeal_oper_eq_linear_span'] at hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨a, _, b, hb, rfl⟩ := hx
      intro y hy
      rw [lie_lie]
      apply (lowerCentralSeries F L L (i+1+j+1)).sub_mem
      · have hby := ih j (LieSubmodule.lie_mem_lie hb hy)
        have haby := LieSubmodule.lie_mem_lie (I := (⊤ : LieIdeal F L))
          (LieSubmodule.mem_top a) hby
        simpa [← lowerCentralSeries_succ, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
          using haby
      · have hay := LieSubmodule.lie_mem_lie (I := (⊤ : LieIdeal F L))
          (LieSubmodule.mem_top a) hy
        rw [← lowerCentralSeries_succ] at hay
        have hbay := ih (j + 1) (LieSubmodule.lie_mem_lie hb hay)
        simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hbay
    | zero => intro y _; simp
    | add x z _ _ hx hz =>
      intro y hy
      rw [add_lie]
      exact (lowerCentralSeries F L L (i+1+j+1)).add_mem (hx y hy) (hz y hy)
    | smul a x _ hx =>
      intro y hy
      rw [smul_lie]
      exact (lowerCentralSeries F L L (i+1+j+1)).smul_mem a (hx y hy)

variable {n : ℕ}

instance evaluationLieRing : LieRing (Fin n → L) where
  bracket x y i := ⁅x i, y i⁆
  add_lie x y z := by funext i; exact add_lie (x i) (y i) (z i)
  lie_add x y z := by funext i; exact lie_add (x i) (y i) (z i)
  lie_self x := by funext i; exact lie_self (x i)
  leibniz_lie x y z := by funext i; exact leibniz_lie (x i) (y i) (z i)

instance evaluationLieAlgebra : LieAlgebra F (Fin n → L) where
  lie_smul a x y := by funext i; exact lie_smul a (x i) (y i)

def monomial (points : Fin n → F) (degree : ℕ) (x : L) : Fin n → L :=
  fun i => points i ^ degree • x

theorem monomial_bracket (points : Fin n → F) (r s : ℕ) (x y : L) :
    ⁅monomial points r x, monomial points s y⁆ = monomial points (r+s) ⁅x,y⁆ := by
  funext i
  change ⁅points i ^ r • x, points i ^ s • y⁆ = points i ^ (r+s) • ⁅x,y⁆
  rw [smul_lie, lie_smul, smul_smul, pow_add]

def coefficientSpace : Submodule F (Fin n → L) where
  carrier := {v | ∀ j, v j ∈ lowerCentralSeries F L L j.val}
  zero_mem' j := (lowerCentralSeries F L L j.val).zero_mem
  add_mem' hx hy j := (lowerCentralSeries F L L j.val).add_mem (hx j) (hy j)
  smul_mem' a _ hx j := (lowerCentralSeries F L L j.val).smul_mem a (hx j)

def evaluate (points : Fin n → F) : (Fin n → L) →ₗ[F] (Fin n → L) where
  toFun v := fun i => ∑ j, points i ^ (j.val + 1) • v j
  map_add' x y := by ext i; simp [smul_add, Finset.sum_add_distrib]
  map_smul' a x := by ext i; simp [Finset.smul_sum, smul_smul, mul_comm]

theorem evaluate_eq_rows (points : Fin n → F) (v : Fin n → L) :
    evaluate points v = ReesHomogenization.applyRows
      (ReesHomogenization.evaluationMatrix points) v := by
  ext i
  simp [evaluate, ReesHomogenization.applyRows, ReesHomogenization.evaluationMatrix_apply]

theorem evaluate_single (points : Fin n → F) (j : Fin n) (x : L) :
    evaluate points (Pi.single j x) = monomial points (j.val+1) x := by
  classical
  ext i
  simp [evaluate, Pi.single_apply, monomial]

def evaluationSpace (points : Fin n → F) : Submodule F (Fin n → L) :=
  coefficientSpace.map (evaluate points)

theorem monomial_mem (points : Fin n → F) (j : Fin n) (x : L)
    (hx : x ∈ lowerCentralSeries F L L j.val) :
    monomial points (j.val+1) x ∈ evaluationSpace points := by
  classical
  refine ⟨Pi.single j x, ?_, evaluate_single points j x⟩
  intro k
  by_cases h : k = j
  · subst k; simpa using hx
  · simp [h]

theorem evaluate_eq_sum (points : Fin n → F) (v : Fin n → L) :
    evaluate points v = ∑ j, monomial points (j.val+1) (v j) := by
  ext i
  simp [evaluate, monomial]

theorem evaluationSpace_bracket (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    {x y : Fin n → L} (hx : x ∈ evaluationSpace points)
    (hy : y ∈ evaluationSpace points) : ⁅x,y⁆ ∈ evaluationSpace points := by
  obtain ⟨a, ha, rfl⟩ := hx
  obtain ⟨b, hb, rfl⟩ := hy
  rw [evaluate_eq_sum, evaluate_eq_sum, sum_lie_sum]
  apply Submodule.sum_mem
  intro r _
  apply Submodule.sum_mem
  intro s _
  rw [monomial_bracket]
  have hbracket := lowerCentral_bracket r.val s.val
    (LieSubmodule.lie_mem_lie (ha r) (hb s))
  by_cases h : r.val + s.val + 1 < n
  · simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
      monomial_mem points ⟨r.val+s.val+1, h⟩ ⁅a r,b s⁆ hbracket
  · have hz := antitone_lowerCentralSeries F L L (Nat.le_of_not_gt h) hbracket
    rw [nilpotent, LieSubmodule.mem_bot] at hz
    rw [hz]
    have he : monomial points (r.val+1+(s.val+1)) (0 : L) = 0 := by
      ext i
      exact smul_zero _
    rw [he]
    exact (evaluationSpace points).zero_mem

/-- Concrete finite-dimensional evaluation realization of the Rees cover. -/
def cover (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥) :
    LieSubalgebra F (Fin n → L) :=
  { evaluationSpace points with lie_mem' := evaluationSpace_bracket points nilpotent }

/-- Evaluations are constructed Lie homomorphisms, not assumptions. -/
def evaluationHom (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (i : Fin n) : cover points nilpotent →ₗ⁅F⁆ L where
  toFun x := x.val i
  map_add' _ _ := rfl
  map_smul' _ _ := rfl
  map_lie' := rfl

theorem cover_nilpotent (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) :
    lowerCentralSeries F (cover points nilpotent) (cover points nilpotent) n = ⊥ := by
  apply le_antisymm ?_ bot_le
  intro x hx
  rw [LieSubmodule.mem_bot]
  apply Subtype.ext
  funext i
  have himage := LieIdeal.mem_map (f := evaluationHom points nilpotent i) hx
  have hz := LieIdeal.map_lowerCentralSeries_le n
    (f := evaluationHom points nilpotent i) himage
  rw [nilpotent, LieSubmodule.mem_bot] at hz
  exact hz

theorem evaluate_injective (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0) :
    Function.Injective (evaluate points : (Fin n → L) →ₗ[F] (Fin n → L)) := by
  intro a b hab
  have hz : evaluate points (a-b) = 0 := by rw [map_sub, hab, sub_self]
  have hmem : ∀ i, ReesHomogenization.applyRows
      (ReesHomogenization.evaluationMatrix points) (a-b) i ∈ (⊥ : Submodule F L) := by
    rw [← evaluate_eq_rows, hz]
    simp
  have hcoeff := (ReesHomogenization.coefficientwise_iff
    (⊥ : Submodule F L) points distinct nonzero (a-b)).mp hmem
  ext j
  exact sub_eq_zero.mp (hcoeff j)

/-- Explicit inverse interpolation; no hidden subgroup data is used. -/
def recover (points : Fin n → F) (x : Fin n → L) : Fin n → L :=
  ReesHomogenization.applyRows (ReesHomogenization.evaluationMatrix points)⁻¹ x

theorem recover_evaluate (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (v : Fin n → L) : recover points (evaluate points v) = v := by
  rw [recover, evaluate_eq_rows, ← ReesHomogenization.applyRows_mul]
  rw [Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr
    (ReesHomogenization.evaluation_det_ne_zero points distinct nonzero))]
  exact ReesHomogenization.applyRows_one v

theorem recover_mem (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    {x : Fin n → L} (hx : x ∈ evaluationSpace points) :
    recover points x ∈ coefficientSpace (F := F) := by
  obtain ⟨v, hv, rfl⟩ := hx
  rwa [recover_evaluate points distinct nonzero]

theorem evaluate_recover (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    {x : Fin n → L} (hx : x ∈ evaluationSpace points) :
    evaluate points (recover points x) = x := by
  obtain ⟨v, _, rfl⟩ := hx
  rw [recover_evaluate points distinct nonzero]

/-- The actual constructed evaluation maps determine hidden membership
coefficientwise, without any homogeneity assumption on the original h. -/
theorem cover_membership_iff (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (h : Submodule F L) (x : cover points nilpotent) :
    (∀ i, evaluationHom points nilpotent i x ∈ h) ↔
      ∀ j, recover points x.val j ∈ h := by
  have he := evaluate_recover points distinct nonzero x.property
  rw [evaluate_eq_rows] at he
  change (∀ i, x.val i ∈ h) ↔ _
  conv_lhs => rw [← he]
  exact ReesHomogenization.coefficientwise_iff h points distinct nonzero _

/-- Grade one contains the whole original L, not just its abelianization.
This is a linear inclusion; it is NOT asserted to be a Lie homomorphism. -/
def gradeOne (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) (x : L) : cover points nilpotent :=
  ⟨monomial points 1 x, monomial_mem points ⟨0, positive⟩ x
    (by simp [lowerCentralSeries_zero])⟩

theorem recover_gradeOne (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) (x : L) :
    recover points (gradeOne points nilpotent positive x).val =
      Pi.single ⟨0,positive⟩ x := by
  change recover points (monomial points 1 x) = _
  rw [← evaluate_single points ⟨0,positive⟩ x, recover_evaluate points distinct nonzero]

theorem gradeOne_membership_iff (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) (h : Submodule F L) (x : L) :
    (∀ i, evaluationHom points nilpotent i (gradeOne points nilpotent positive x) ∈ h) ↔
      x ∈ h := by
  classical
  rw [cover_membership_iff points distinct nonzero, recover_gradeOne points distinct nonzero]
  constructor
  · intro hx
    simpa using hx ⟨0,positive⟩
  · intro hx j
    by_cases hj : j = ⟨0,positive⟩
    · subst j; simpa using hx
    · simp [hj]

end
end QSearch.ReesLie
