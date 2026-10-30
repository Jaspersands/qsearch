import Mathlib.LinearAlgebra.ExteriorAlgebra.Basic
import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction
import Mathlib.LinearAlgebra.CliffordAlgebra.Conjugation
import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.Basis.VectorSpace
import Mathlib.Tactic.NoncommRing

/-!
The coordinate compression used by the exterior collision construction.
This file proves algebraic recovery, not the entire recursive SDE solver.
-/

namespace QSearch.ExteriorCompression

set_option autoImplicit false
set_option relaxedAutoImplicit false

noncomputable section
open scoped BigOperators

variable {F V : Type*} [Field F] [AddCommGroup V] [Module F V]

abbrev contraction (l : V →ₗ[F] F) :
    ExteriorAlgebra F V →ₗ[F] ExteriorAlgebra F V :=
  CliffordAlgebra.contractLeft (Q := (0 : QuadraticForm F V)) l

def shear (l : V →ₗ[F] F) (e : V) : V →ₗ[F] V :=
  LinearMap.id - l.smulRight e

theorem shear_apply (l : V →ₗ[F] F) (e v : V) :
    shear l e v = v - l v • e := rfl

theorem contraction_square (l : V →ₗ[F] F) (x : ExteriorAlgebra F V) :
    contraction l (contraction l x) = 0 :=
  CliffordAlgebra.contractLeft_contractLeft l x

theorem contraction_right_wedge (l : V →ₗ[F] F) (x : ExteriorAlgebra F V) (v : V) :
    contraction l (x * ExteriorAlgebra.ι F v) =
      contraction l x * ExteriorAlgebra.ι F v + l v • CliffordAlgebra.involute x := by
  induction x using CliffordAlgebra.left_induction with
  | algebraMap r =>
    simp [contraction, Algebra.algebraMap_eq_smul_one, smul_comm r (l v)]
  | add x y hx hy =>
    simp only [add_mul, map_add, hx, hy, smul_add]
    abel
  | ι_mul x u hx =>
    change CliffordAlgebra.contractLeft l
        (ExteriorAlgebra.ι F u * x * ExteriorAlgebra.ι F v) =
      CliffordAlgebra.contractLeft l (ExteriorAlgebra.ι F u * x) * ExteriorAlgebra.ι F v +
        l v • CliffordAlgebra.involute (ExteriorAlgebra.ι F u * x)
    rw [mul_assoc, CliffordAlgebra.contractLeft_ι_mul, hx,
      CliffordAlgebra.contractLeft_ι_mul, map_mul, CliffordAlgebra.involute_ι]
    simp only [mul_add, sub_mul, smul_mul_assoc, mul_smul_comm, mul_assoc,
      neg_mul, smul_neg]
    abel

theorem wedge_update_closed (l : V →ₗ[F] F) {I : Type*} [Fintype I]
    (a : I → F) (x : I → ExteriorAlgebra F V) (v : I → V)
    (closed : ∀ i, contraction l (x i) = 0)
    (relation : ∑ i, a i • (l (v i) • x i) = 0) :
    contraction l (∑ i, a i • (x i * ExteriorAlgebra.ι F (v i))) = 0 := by
  simp only [map_sum, map_smul, contraction_right_wedge, closed, zero_mul, zero_add]
  have image := congrArg CliffordAlgebra.involute relation
  simpa only [map_sum, map_smul, map_zero] using image

theorem shear_formula (l : V →ₗ[F] F) (e : V) (x : ExteriorAlgebra F V) :
    ExteriorAlgebra.map (shear l e) x =
      x - ExteriorAlgebra.ι F e * contraction l x := by
  induction x using CliffordAlgebra.left_induction with
  | algebraMap r => simp [contraction]
  | add x y hx hy =>
    simp only [map_add, hx, hy, mul_add]
    abel
  | ι_mul x v hx =>
    rw [map_mul, ExteriorAlgebra.map_apply_ι, shear_apply, map_sub, map_smul, hx]
    change (ExteriorAlgebra.ι F v - l v • ExteriorAlgebra.ι F e) *
        (x - ExteriorAlgebra.ι F e * contraction l x) =
      ExteriorAlgebra.ι F v * x - ExteriorAlgebra.ι F e *
        CliffordAlgebra.contractLeft l (ExteriorAlgebra.ι F v * x)
    rw [CliffordAlgebra.contractLeft_ι_mul]
    have swap : ExteriorAlgebra.ι F v * ExteriorAlgebra.ι F e =
        -(ExteriorAlgebra.ι F e * ExteriorAlgebra.ι F v) :=
      eq_neg_of_add_eq_zero_left (ExteriorAlgebra.ι_add_mul_swap v e)
    simp only [sub_mul, mul_sub, smul_mul_assoc, mul_smul_comm,
      ← mul_assoc, ExteriorAlgebra.ι_sq_zero, smul_zero, sub_zero, swap, neg_mul]
    abel

theorem shear_fixes_closed (l : V →ₗ[F] F) (e : V) (x : ExteriorAlgebra F V)
    (closed : contraction l x = 0) : ExteriorAlgebra.map (shear l e) x = x := by
  rw [shear_formula, closed, mul_zero, sub_zero]

theorem shear_is_closed (l : V →ₗ[F] F) (e : V) (unit : l e = 1)
    (x : ExteriorAlgebra F V) : contraction l (ExteriorAlgebra.map (shear l e) x) = 0 := by
  rw [shear_formula, map_sub]
  change contraction l x - CliffordAlgebra.contractLeft l
    (ExteriorAlgebra.ι F e * contraction l x) = 0
  rw [CliffordAlgebra.contractLeft_ι_mul, unit, one_smul, contraction_square,
    mul_zero, sub_zero, sub_self]

theorem contraction_map_zero {U : Type*} [AddCommGroup U] [Module F U]
    (l : V →ₗ[F] F) (f : U →ₗ[F] V) (annihilates : ∀ u, l (f u) = 0)
    (x : ExteriorAlgebra F U) : contraction l (ExteriorAlgebra.map f x) = 0 := by
  induction x using CliffordAlgebra.left_induction with
  | algebraMap r => simp [contraction]
  | add x y hx hy => simp only [map_add, hx, hy, add_zero]
  | ι_mul x u hx =>
    rw [map_mul, ExteriorAlgebra.map_apply_ι]
    change CliffordAlgebra.contractLeft l
      (ExteriorAlgebra.ι F (f u) * ExteriorAlgebra.map f x) = 0
    rw [CliffordAlgebra.contractLeft_ι_mul, annihilates, zero_smul, hx, mul_zero, sub_self]

def closedDegree (l : V →ₗ[F] F) (j : ℕ) : Submodule F (⋀[F]^j V) :=
  LinearMap.ker ((contraction l).comp (ExteriorAlgebra.exteriorPower F j V).subtype)

section SplitCoordinate

variable {E : Type*} [AddCommGroup E] [Module F E]

def covector (l : E →ₗ[F] F) (z : F) : E × F →ₗ[F] F :=
  l.comp (LinearMap.fst F E F) + z • LinearMap.snd F E F

def lift (l : E →ₗ[F] F) (z : F) : E →ₗ[F] E × F :=
  LinearMap.prod LinearMap.id (-(z⁻¹ • l))

theorem lift_fst (l : E →ₗ[F] F) (z : F) (x : E) : (lift l z x).1 = x := rfl

theorem covector_lift (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) (x : E) :
    covector l z (lift l z x) = 0 := by
  simp [covector, lift, nz]

theorem fst_comp_lift (l : E →ₗ[F] F) (z : F) :
    (LinearMap.fst F E F).comp (lift l z) = LinearMap.id := by
  apply LinearMap.ext
  exact lift_fst l z

theorem lift_comp_fst (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) :
    (lift l z).comp (LinearMap.fst F E F) = shear (covector l z) (0, z⁻¹) := by
  apply LinearMap.ext
  intro x
  apply Prod.ext
  · simp [lift, shear, covector]
  · change -(z⁻¹ * l x.1) = x.2 - (l x.1 + z*x.2)*z⁻¹
    field_simp
    ring

theorem recover_closed (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0)
    (x : ExteriorAlgebra F (E × F)) (closed : contraction (covector l z) x = 0) :
    ExteriorAlgebra.map (lift l z) (ExteriorAlgebra.map (LinearMap.fst F E F) x) = x := by
  change (ExteriorAlgebra.map (lift l z)).comp
    (ExteriorAlgebra.map (LinearMap.fst F E F)) x = x
  rw [ExteriorAlgebra.map_comp_map, lift_comp_fst l z nz]
  exact shear_fixes_closed _ _ _ closed

theorem projection_injective_on_closed (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0)
    (x y : ExteriorAlgebra F (E × F))
    (hx : contraction (covector l z) x = 0) (hy : contraction (covector l z) y = 0)
    (same : ExteriorAlgebra.map (LinearMap.fst F E F) x =
      ExteriorAlgebra.map (LinearMap.fst F E F) y) : x = y := by
  rw [← recover_closed l z nz x hx, ← recover_closed l z nz y hy, same]

theorem projected_relation_is_full (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0)
    {I : Type*} [Fintype I] (a : I → F) (x : I → ExteriorAlgebra F (E × F))
    (closed : ∀ i, contraction (covector l z) (x i) = 0)
    (relation : ∑ i, a i • ExteriorAlgebra.map (LinearMap.fst F E F) (x i) = 0) :
    ∑ i, a i • x i = 0 := by
  apply projection_injective_on_closed l z nz
  · simp [map_sum, closed]
  · exact map_zero _
  · simpa using relation

def closedProjection (l : E →ₗ[F] F) (z : F) (j : ℕ) :
    closedDegree (covector l z) j →ₗ[F] (⋀[F]^j E) :=
  (exteriorPower.map j (LinearMap.fst F E F)).comp (closedDegree (covector l z) j).subtype

def closedLift (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) (j : ℕ) :
    (⋀[F]^j E) →ₗ[F] closedDegree (covector l z) j :=
  (exteriorPower.map j (lift l z)).codRestrict _ (by
    intro x
    change contraction (covector l z) ((exteriorPower.map j (lift l z) x).val) = 0
    rw [exteriorPower.coe_map]
    exact contraction_map_zero _ _ (covector_lift l z nz) x.val)

def closedEquiv (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) (j : ℕ) :
    closedDegree (covector l z) j ≃ₗ[F] (⋀[F]^j E) :=
  LinearEquiv.ofLinearMap (closedProjection l z j) (closedLift l z nz j)
    (by
      apply LinearMap.ext
      intro x
      change exteriorPower.map j (LinearMap.fst F E F) (exteriorPower.map j (lift l z) x) = x
      rw [← LinearMap.comp_apply, ← exteriorPower.map_comp, fst_comp_lift, exteriorPower.map_id]
      rfl)
    (by
      apply LinearMap.ext
      intro x
      apply Subtype.ext
      apply Subtype.ext
      change ((exteriorPower.map j (lift l z)
        (exteriorPower.map j (LinearMap.fst F E F) x.val)).val) = x.val.val
      simp only [exteriorPower.coe_map]
      exact recover_closed l z nz x.val.val x.property)

theorem closed_dimension [Module.Finite F E] (l : E →ₗ[F] F) (z : F)
    (nz : z ≠ 0) (j : ℕ) :
    Module.finrank F (closedDegree (covector l z) j) = (Module.finrank F E).choose j := by
  rw [(closedEquiv l z nz j).finrank_eq, exteriorPower.finrank_eq]

theorem closed_top_zero [Module.Finite F E] (l : E →ₗ[F] F) (z : F)
    (nz : z ≠ 0) (j : ℕ) (too_high : Module.finrank F E < j)
    (x : ⋀[F]^j (E × F)) (closed : contraction (covector l z) x.val = 0) : x = 0 := by
  have dim_zero : Module.finrank F (closedDegree (covector l z) j) = 0 := by
    rw [closed_dimension l z nz j, Nat.choose_eq_zero_of_lt too_high]
  have bottom : closedDegree (covector l z) j = ⊥ := Submodule.finrank_eq_zero.mp dim_zero
  have belongs : x ∈ closedDegree (covector l z) j := closed
  rw [bottom, Submodule.mem_bot] at belongs
  exact belongs

set_option backward.isDefEq.respectTransparency false in
theorem closed_rows_dimension [Module.Finite F E] {R : Type*} [Fintype R]
    (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) (j : ℕ) :
    Module.finrank F (R → closedDegree (covector l z) j) =
      Fintype.card R * (Module.finrank F E).choose j := by
  rw [@Module.finrank_pi_fintype F _ _ R _
    (fun _ : R => closedDegree (covector l z) j)
    (fun _ => inferInstance) (fun _ => inferInstance)
    (fun _ => Module.Free.of_divisionRing F (closedDegree (covector l z) j))
    (fun _ => inferInstance)]
  simp [closed_dimension l z nz j]

set_option backward.isDefEq.respectTransparency false in
theorem closed_rows_relation [Module.Finite F E] {R I : Type*} [Fintype R] [Fintype I]
    (l : E →ₗ[F] F) (z : F) (nz : z ≠ 0) (j : ℕ)
    (x : I → R → closedDegree (covector l z) j)
    (enough : Fintype.card R * (Module.finrank F E).choose j < Fintype.card I) :
    ∃ a : I → F, (∑ i, a i • x i = 0) ∧ ∃ i, a i ≠ 0 := by
  apply (Fintype.not_linearIndependent_iff (R := F) (v := x)).mp
  intro independent
  have bound := independent.fintype_card_le_finrank
  rw [closed_rows_dimension l z nz j] at bound
  exact enough.not_ge bound

theorem degenerate_projection_counterexample :
    ∃ x : ExteriorAlgebra F (F × F), x ≠ 0 ∧
      contraction (covector (0 : F →ₗ[F] F) 0) x = 0 ∧
      ExteriorAlgebra.map (LinearMap.fst F F F) x = 0 := by
  refine ⟨ExteriorAlgebra.ι F (0, 1), ?_, ?_, ?_⟩
  · rw [ne_eq, ExteriorAlgebra.ι_eq_zero_iff]
    intro h
    exact one_ne_zero (congrArg Prod.snd h)
  · simp [contraction, covector]
  · simp [ExteriorAlgebra.map_apply_ι]

theorem nonclosed_projection_counterexample :
    ∃ x : ExteriorAlgebra F (F × F), x ≠ 0 ∧
      contraction (covector (0 : F →ₗ[F] F) 1) x ≠ 0 ∧
      ExteriorAlgebra.map (LinearMap.fst F F F) x = 0 := by
  refine ⟨ExteriorAlgebra.ι F (0, 1), ?_, ?_, ?_⟩
  · rw [ne_eq, ExteriorAlgebra.ι_eq_zero_iff]
    intro h
    exact one_ne_zero (congrArg Prod.snd h)
  · simp [contraction, covector]
  · simp [ExteriorAlgebra.map_apply_ι]

end SplitCoordinate
end
end QSearch.ExteriorCompression
