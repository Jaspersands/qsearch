import ReesDilation

/-!
Construct the Rees group and its actual evaluation/dilation maps from an
explicit Lie-polynomial law on the base group. The base Lazard/BCH theorem
is an input boundary, not an axiom hidden in an assumed cover homomorphism.
-/

namespace QSearch.ReesGroupBridge
open ReesLie ReesDilation
open LieModule
noncomputable section

inductive Expression (F : Type*) where
  | left
  | right
  | zero
  | add (a b : Expression F)
  | smul (c : F) (a : Expression F)
  | bracket (a b : Expression F)

variable {F L M : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]

def interpret : Expression F → L → L → L
  | .left, x, _ => x
  | .right, _, y => y
  | .zero, _, _ => 0
  | .add a b, x, y => interpret a x y + interpret b x y
  | .smul c a, x, y => c • interpret a x y
  | .bracket a b, x, y => ⁅interpret a x y, interpret b x y⁆

theorem map_interpret (e : Expression F) (f : L →ₗ⁅F⁆ M) (x y : L) :
    f (interpret e x y) = interpret e (f x) (f y) := by
  induction e <;> simp_all [interpret]

theorem interpret_mem (e : Expression F) (S : LieSubalgebra F L)
    {x y : L} (hx : x ∈ S) (hy : y ∈ S) : interpret e x y ∈ S := by
  induction e with
  | left => exact hx
  | right => exact hy
  | zero => exact S.zero_mem
  | add a b ha hb => exact S.add_mem ha hb
  | smul c a ha => exact S.smul_mem c ha
  | bracket a b ha hb => exact S.lie_mem ha hb

def linearPart : Expression F → F × F
  | .left => (1, 0)
  | .right => (0, 1)
  | .zero => (0, 0)
  | .add a b => ((linearPart a).fst + (linearPart b).fst,
                 (linearPart a).snd + (linearPart b).snd)
  | .smul c a => (c * (linearPart a).fst, c * (linearPart a).snd)
  | .bracket _ _ => (0, 0)

theorem interpret_commuting (e : Expression F) (x y : L) (hxy : ⁅x,y⁆ = 0) :
    interpret e x y = (linearPart e).fst • x + (linearPart e).snd • y := by
  have hyx : ⁅y,x⁆ = 0 := by rw [← lie_skew, hxy, neg_zero]
  induction e with
  | left => simp [interpret, linearPart]
  | right => simp [interpret, linearPart]
  | zero => simp [interpret, linearPart]
  | add a b ha hb => simp [interpret, linearPart, ha, hb, add_smul, add_assoc,
      add_left_comm]
  | smul c a ha => simp [interpret, linearPart, ha, smul_add, mul_smul]
  | bracket a b ha hb =>
    simp [interpret, linearPart, ha, hb, add_lie, lie_add, smul_lie, lie_smul, hxy, hyx]

theorem interpret_split (e : Expression F) (x y : L) (hxy : ⁅x,y⁆ = 0) :
    interpret e x y = interpret e x (0 : L) + interpret e 0 y := by
  rw [interpret_commuting e x y hxy, interpret_commuting e x 0 (by simp),
    interpret_commuting e 0 y (by simp)]
  simp

/-- This boundary packages a supplied base group, not the desired Rees group.
For Lazard coordinates the expression is the finite BCH Lie polynomial.
Associativity and the field/degree conditions are not proved by this package. -/
structure PolynomialGroupLaw (F L : Type*) [Field F] [LieRing L]
    [LieAlgebra F L] [Group L] where
  expression : Expression F
  mul_eq : ∀ x y : L, x * y = interpret expression x y
  one_eq : (1 : L) = 0
  inv_eq : ∀ x : L, x⁻¹ = -x

variable [Group L]

theorem commuting_mul_add (law : PolynomialGroupLaw F L) (x y : L)
    (hxy : ⁅x,y⁆ = 0) : x*y = x+y := by
  rw [law.mul_eq, interpret_split law.expression x y hxy,
    ← law.mul_eq x 0, ← law.mul_eq 0 y, ← law.one_eq]
  simp

theorem commuting_group (law : PolynomialGroupLaw F L) (x y : L)
    (hxy : ⁅x,y⁆ = 0) : Commute x y := by
  have hyx : ⁅y,x⁆ = 0 := by rw [← lie_skew, hxy, neg_zero]
  change x*y = y*x
  rw [commuting_mul_add law x y hxy, commuting_mul_add law y x hyx, add_comm]

def subgroup (law : PolynomialGroupLaw F L) (S : LieSubalgebra F L) : Subgroup L where
  carrier := S
  mul_mem' hx hy := by rw [law.mul_eq]; exact interpret_mem law.expression S hx hy
  one_mem' := by rw [law.one_eq]; exact S.zero_mem
  inv_mem' hx := by rw [law.inv_eq]; exact S.neg_mem hx

def toLie (law : PolynomialGroupLaw F L) (S : LieSubalgebra F L) : subgroup law S ≃ S where
  toFun x := ⟨x.val, x.property⟩
  invFun x := ⟨x.val, x.property⟩
  left_inv _ := rfl
  right_inv _ := rfl

theorem toLie_mul (law : PolynomialGroupLaw F L) (S : LieSubalgebra F L)
    (x y : subgroup law S) :
    toLie law S (x*y) = interpret law.expression (toLie law S x) (toLie law S y) := by
  apply Subtype.ext
  change x.val * y.val = S.incl (interpret law.expression (toLie law S x) (toLie law S y))
  rw [map_interpret, law.mul_eq]
  rfl

def liftLieEquiv (law : PolynomialGroupLaw F L) (S : LieSubalgebra F L)
    (e : S ≃ₗ⁅F⁆ S) : subgroup law S ≃* subgroup law S where
  toFun x := (toLie law S).symm (e (toLie law S x))
  invFun x := (toLie law S).symm (e.symm (toLie law S x))
  left_inv x := by simp
  right_inv x := by simp
  map_mul' x y := by
    apply (toLie law S).injective
    simp only [Equiv.apply_symm_apply, toLie_mul]
    exact map_interpret law.expression e.toLieHom _ _

variable {n : ℕ}

omit [Group L] in
theorem interpret_pi (e : Expression F) (x y : Fin n → L) (i : Fin n) :
    interpret e x y i = interpret e (x i) (y i) := by
  induction e with
  | left => rfl
  | right => rfl
  | zero => rfl
  | add a b ha hb => simp only [interpret, Pi.add_apply, ha, hb]
  | smul c a ha => simp only [interpret, Pi.smul_apply, ha]
  | bracket a b ha hb =>
    change ⁅interpret a x y i, interpret b x y i⁆ = _
    rw [ha, hb]
    rfl

def piLaw (law : PolynomialGroupLaw F L) : PolynomialGroupLaw F (Fin n → L) where
  expression := law.expression
  mul_eq x y := by funext i; rw [interpret_pi]; exact law.mul_eq (x i) (y i)
  one_eq := by funext i; exact law.one_eq
  inv_eq x := by funext i; exact law.inv_eq (x i)

def groupCover (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) : Subgroup (Fin n → L) :=
  subgroup (piLaw law) (cover points nilpotent)

def evaluationGroupHom (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (i : Fin n) :
    groupCover law points nilpotent →* L where
  toFun x := x.val i
  map_one' := rfl
  map_mul' _ _ := rfl

def dilationGroupEquiv (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) (ha : a ≠ 0) :
    groupCover law points nilpotent ≃* groupCover law points nilpotent :=
  liftLieEquiv (piLaw law) (cover points nilpotent)
    (dilationEquiv points distinct nonzero nilpotent a ha)

theorem dilationGroup_value (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) (ha : a ≠ 0)
    (x : groupCover law points nilpotent) :
    (dilationGroupEquiv law points distinct nonzero nilpotent a ha x).val =
      dilationLinear points a x.val := rfl

theorem group_hidden_membership (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (h : Submodule F L)
    (x : groupCover law points nilpotent) :
    (∀ i, evaluationGroupHom law points nilpotent i x ∈ h) ↔
      ∀ j, recover points x.val j ∈ h := by
  exact cover_membership_iff points distinct nonzero nilpotent h (toLie _ _ x)

theorem dilationGroup_hidden (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) (ha : a ≠ 0)
    (h : Submodule F L) (x : groupCover law points nilpotent) :
    (∀ i, evaluationGroupHom law points nilpotent i
      (dilationGroupEquiv law points distinct nonzero nilpotent a ha x) ∈ h) ↔
      ∀ i, evaluationGroupHom law points nilpotent i x ∈ h := by
  exact dilation_hidden_membership_iff points distinct nonzero nilpotent a ha h (toLie _ _ x)

theorem actual_tuple_hides (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (h : Submodule F L)
    {O : Type*} (f : L → O) (hides : ∀ x y, f x = f y ↔ x⁻¹*y ∈ h)
    (a b : groupCover law points nilpotent) :
    (fun i => f (evaluationGroupHom law points nilpotent i a)) =
      (fun i => f (evaluationGroupHom law points nilpotent i b)) ↔
        ∀ j, recover points (a⁻¹*b).val j ∈ h := by
  apply ReesHomogenization.tuple_hides h points distinct nonzero
    (evaluationGroupHom law points nilpotent) id (fun x => recover points x.val)
    ?_ f hides a b
  intro x i
  have he := evaluate_recover points distinct nonzero x.property
  rw [evaluate_eq_rows] at he
  exact (congrFun he i).symm

def highestGroupElement (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n)
    (highest : j.val+1 = n) (v : L) (hv : v ∈ lowerCentralSeries F L L j.val) :
    groupCover law points nilpotent :=
  ⟨monomial points n v, by
    change monomial points n v ∈ evaluationSpace points
    simpa only [highest] using monomial_mem points j v hv⟩

theorem highestGroup_central (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n)
    (highest : j.val+1 = n) (v : L) (hv : v ∈ lowerCentralSeries F L L j.val)
    (x : groupCover law points nilpotent) :
    Commute (highestGroupElement law points nilpotent j highest v hv) x := by
  have hc := commuting_group (piLaw law) (monomial points n v) x.val
    (highest_monomial_central points nilpotent j highest v hv x.val)
  apply Subtype.ext
  exact hc.eq

theorem highestGroup_scaled (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n)
    (highest : j.val+1 = n) (v : L) (hv : v ∈ lowerCentralSeries F L L j.val)
    (a : F) (ha : a ≠ 0) :
    (dilationGroupEquiv law points distinct nonzero nilpotent a ha
      (highestGroupElement law points nilpotent j highest v hv)).val =
      a^n • monomial points n v := by
  rw [dilationGroup_value]
  exact dilation_highest_grade points distinct nonzero j highest a v

end
end QSearch.ReesGroupBridge
