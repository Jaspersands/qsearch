import Mathlib.Algebra.Lie.Nilpotent
import Mathlib.Tactic

/-!
# The class-three BCH group

The group law is constructed from Lie axioms and a lower-central-series bound.
The field may have positive characteristic: only 2 and 3 must be nonzero.
This module does not assert a correspondence between arbitrary group subgroups
and subalgebras over the coefficient field, or any HSP algorithmic conclusion.
-/

namespace QSearch.BCHClassThree

open LieModule

noncomputable section

variable {F L M N : Type*} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Explicit length-four bracket vanishing, without a group-law hypothesis. -/
def ClassThree (L : Type*) [LieRing L] : Prop :=
  ∀ x y z w : L, ⁅x, ⁅y, ⁅z, w⁆⁆⁆ = 0

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classThree_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 3 = ⊥) : ClassThree L := by
  intro x y z w
  have h : ⁅x, ⁅y, ⁅z, w⁆⁆⁆ ∈ lowerCentralSeries F L L 3 := by
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top x)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top y)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top z) (LieSubmodule.mem_top w)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The truncated BCH polynomial, with the standard symmetric cubic term. -/
def bch (x y : L) : L :=
  x + y + (2 : F)⁻¹ • ⁅x, y⁆ +
    (12 : F)⁻¹ • (⁅x, ⁅x, y⁆⁆ + ⁅y, ⁅y, x⁆⁆)

@[simp] theorem bch_zero_left (x : L) : bch (F := F) 0 x = x := by
  simp [bch]

@[simp] theorem bch_zero_right (x : L) : bch (F := F) x 0 = x := by
  simp [bch]

@[simp] theorem bch_neg_left (x : L) : bch (F := F) (-x) x = 0 := by
  simp [bch]

@[simp] theorem bch_neg_right (x : L) : bch (F := F) x (-x) = 0 := by
  simp [bch]

/-- Associativity follows from Jacobi and the disappearance of length-four brackets. -/
theorem bch_assoc_of_classThree (h : ClassThree L)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
  have h12 : (12 : F) ≠ 0 := by
    rw [show (12 : F) = 2 * 2 * 3 by ring]
    exact mul_ne_zero (mul_ne_zero h2 h2) h3
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have hfour (a b c d : L) : ⁅a, ⁅b, ⁅c, d⁆⁆⁆ = 0 := h a b c d
  have hj : ⁅z, ⁅x, y⁆⁆ = ⁅y, ⁅x, z⁆⁆ - ⁅x, ⁅y, z⁆⁆ := by
    have hj := lie_jacobi x y z
    rw [hzx, lie_neg] at hj
    apply sub_eq_zero.mp
    calc
      _ = ⁅x, ⁅y, z⁆⁆ + -⁅y, ⁅x, z⁆⁆ + ⁅z, ⁅x, y⁆⁆ := by abel
      _ = 0 := hj
  simp only [bch, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    lie_sub, hfour, lie_zero, sub_zero,
    hyx, hzx, hzy, lie_neg, neg_lie, hj, smul_zero, add_zero, zero_add]
  match_scalars <;> field_simp [h2, h12]
  ring

theorem bch_assoc (hnil : lowerCentralSeries F L L 3 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classThree (classThree_of_lowerCentralSeries hnil) h2 h3 x y z

/-- Lie maps preserve the actual BCH polynomial, without any class hypothesis. -/
theorem map_bch (f : L →ₗ⁅F⁆ M) (x y : L) :
    f (bch (F := F) x y) = bch (F := F) (f x) (f y) := by
  simp only [bch, map_add, map_smul, LieHom.map_lie]

/-- Scalar multiples of one vector have vanishing mutual brackets. -/
theorem bch_smul_same (a b : F) (x : L) :
    bch (F := F) (a • x) (b • x) = (a + b) • x := by
  simp [bch, smul_lie, lie_smul, add_smul]

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 3 = ⊥) where
  val : L

@[ext] theorem BCH.ext {hnil : lowerCentralSeries F L L 3 = ⊥}
    {x y : BCH F L hnil} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 3 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 3 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {hL : lowerCentralSeries F L L 3 = ⊥}
  {hM : lowerCentralSeries F M M 3 = ⊥}
  {hN : lowerCentralSeries F N N 3 = ⊥}

@[simp] theorem val_mul (x y : BCH F L hL) :
    (x * y).val = bch (F := F) x.val y.val := rfl

/-- The value formula used to integrate concrete Lie-algebra constructions. -/
theorem val_mul_formula (x y : BCH F L hL) :
    (x * y).val = x.val + y.val + (2 : F)⁻¹ • ⁅x.val, y.val⁆ +
      (12 : F)⁻¹ • (⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅y.val, ⁅y.val, x.val⁆⁆) := rfl

@[simp] theorem val_one : (1 : BCH F L hL).val = 0 := rfl

@[simp] theorem val_inv (x : BCH F L hL) : x⁻¹.val = -x.val := rfl

/-- Natural group powers have the actual scalar-multiple logarithm. -/
@[simp] theorem val_pow (x : BCH F L hL) (n : ℕ) :
    (x ^ n).val = (n : F) • x.val := by
  induction n with
  | zero => simp
  | succ n ih =>
    simp [pow_succ, ih, bch, smul_lie, lie_smul, add_smul]

/-- Integer group powers have the actual scalar-multiple logarithm. -/
@[simp] theorem val_zpow (x : BCH F L hL) (n : ℤ) :
    (x ^ n).val = (n : F) • x.val := by
  cases n with
  | ofNat n => simp
  | negSucc n => simp only [zpow_negSucc, val_inv, val_pow, Int.cast_negSucc, neg_smul]

/-- Every Lie homomorphism between class-at-most-three algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 3 = ⊥)
    (hM : lowerCentralSeries F M M 3 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 3 = ⊥)
    (hM : lowerCentralSeries F M M 3 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
    BCH F L hL ≃* BCH F M hM where
  toFun := lieHom hL hM e.toLieHom
  invFun := lieHom hM hL e.symm.toLieHom
  left_inv x := BCH.ext (e.symm_apply_apply x.val)
  right_inv x := BCH.ext (e.apply_symm_apply x.val)
  map_mul' := (lieHom hL hM e.toLieHom).map_mul

@[simp] theorem lieEquiv_apply (e : L ≃ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieEquiv hL hM e x).val = e x.val := rfl

@[simp] theorem lieHom_id : lieHom hL hL (LieHom.id : L →ₗ⁅F⁆ L) = MonoidHom.id _ := by
  ext x
  rfl

@[simp] theorem lieHom_comp (f : L →ₗ⁅F⁆ M) (g : M →ₗ⁅F⁆ N) :
    lieHom hL hN (g.comp f) = (lieHom hM hN g).comp (lieHom hL hM f) := by
  ext x
  rfl

@[simp] theorem lieEquiv_symm (e : L ≃ₗ⁅F⁆ M) :
    (lieEquiv hL hM e).symm = lieEquiv hM hL e.symm := by
  ext x
  rfl

end
end QSearch.BCHClassThree

/-- info: 'QSearch.BCHClassThree.classThree_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.classThree_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassThree.bch_assoc_of_classThree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.bch_assoc_of_classThree

/-- info: 'QSearch.BCHClassThree.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.bch_assoc

/-- info: 'QSearch.BCHClassThree.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.instGroup

/-- info: 'QSearch.BCHClassThree.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.val_mul_formula

/-- info: 'QSearch.BCHClassThree.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.lieHom

/-- info: 'QSearch.BCHClassThree.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.lieEquiv

/-- info: 'QSearch.BCHClassThree.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThree.val_zpow
