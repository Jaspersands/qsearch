import Formal.BCHClassFour

/-!
# The class-five BCH group

The group law is the degree-five truncated Baker-Campbell-Hausdorff product
`x + y + [x,y]/2 + ([x,[x,y]] + [y,[y,x]])/12 - [y,[x,[x,y]]]/24
 - ([y,[y,[y,[y,x]]]] + [x,[x,[x,[x,y]]]])/720
 + ([x,[y,[y,[y,x]]]] + [y,[x,[x,[x,y]]]])/360
 + ([y,[x,[y,[x,y]]]] + [x,[y,[x,[y,x]]]])/120`.
Only `2, 3, 5 ≠ 0` is needed in the field, so every `ZMod p` with `p > 5` is
included.

Associativity is proved from Jacobi and the lower-central bound
`lowerCentralSeries F L L 5 = ⊥` exactly as in `BCHClassFour`: both sides are
brought to a normal form of right-normed brackets in `x, y, z` (innermost pair
sorted), rewritten by one degree-three rule (`jacobi3 x y z`), six degree-four
rules `r4a`-`r4f` and six degree-five rules `r5a`-`r5f`. The irreducible words
are a basis of the free class-five Lie algebra on three generators
(3, 3, 8, 18, 48 words in degrees 1-5), so the normal form is unique. The rules
and their `lie_skew` certificates were chosen with the exact rational model
`research/audits/reviews/2026-11-04-rees-lean-c5/rules5.py`; Lean does not rely
on that model, it proves every rule and checks that the two normal forms agree.
-/

namespace QSearch.BCHClassFive

open LieModule
open QSearch.BCHClassFour (jacobi3 jacobi4c)

noncomputable section

/-- Explicit length-six bracket vanishing, without a group-law hypothesis. -/
def ClassFive (L : Type*) [LieRing L] : Prop :=
  ∀ a b c d e f : L, ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, f⁆⁆⁆⁆⁆ = 0

variable {F L M N : Type*} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classFive_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 5 = ⊥) : ClassFive L := by
  intro a b c d e f
  have h : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, f⁆⁆⁆⁆⁆ ∈ lowerCentralSeries F L L 5 := by
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top b)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top c)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top d)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top e) (LieSubmodule.mem_top f)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The degree-five truncated BCH polynomial. -/
def bch (x y : L) : L :=
  x + y + (2 : F)⁻¹ • ⁅x, y⁆ +
    (12 : F)⁻¹ • (⁅x, ⁅x, y⁆⁆ + ⁅y, ⁅y, x⁆⁆) - (24 : F)⁻¹ • ⁅y, ⁅x, ⁅x, y⁆⁆⁆ -
    (720 : F)⁻¹ • (⁅y, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆) +
    (360 : F)⁻¹ • (⁅x, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆) +
    (120 : F)⁻¹ • (⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, x⁆⁆⁆⁆)

@[simp] theorem bch_zero_left (x : L) : bch (F := F) 0 x = x := by
  simp [bch]

@[simp] theorem bch_zero_right (x : L) : bch (F := F) x 0 = x := by
  simp [bch]

@[simp] theorem bch_neg_left (x : L) : bch (F := F) (-x) x = 0 := by
  simp [bch]

@[simp] theorem bch_neg_right (x : L) : bch (F := F) x (-x) = 0 := by
  simp [bch]

/-- Lie-commuting elements multiply by addition. -/
theorem bch_of_lie_eq_zero {x y : L} (h : ⁅x, y⁆ = 0) :
    bch (F := F) x y = x + y := by
  have hyx : ⁅y, x⁆ = 0 := by rw [← lie_skew y x, h, neg_zero]
  simp [bch, h, hyx]

/-- Lie maps preserve the actual BCH polynomial, without any class hypothesis. -/
theorem map_bch (f : L →ₗ⁅F⁆ M) (x y : L) :
    f (bch (F := F) x y) = bch (F := F) (f x) (f y) := by
  simp only [bch, map_add, map_sub, map_smul, LieHom.map_lie]

/-- Scalar multiples of one vector have vanishing mutual brackets. -/
theorem bch_smul_same (a b : F) (x : L) :
    bch (F := F) (a • x) (b • x) = (a + b) • x := by
  simp [bch, smul_lie, lie_smul, add_smul]

section Assoc

variable (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0)
include h2 h3 h5

/-- Every natural number of the form `2^a 3^b 5^c` is nonzero in `F`. -/
theorem smooth_ne_zero (a b c : ℕ) : ((2 : F) ^ a * 3 ^ b * 5 ^ c) ≠ 0 :=
  mul_ne_zero (mul_ne_zero (pow_ne_zero _ h2) (pow_ne_zero _ h3)) (pow_ne_zero _ h5)

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 4000000 in
/-- Associativity follows from Jacobi and the disappearance of length-six brackets. -/
theorem bch_assoc_of_classFive (h : ClassFive L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
  have h4 : (4 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 2 0 0; norm_num at this; exact this
  have h6 : (6 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 1 1 0; norm_num at this; exact this
  have h8 : (8 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 3 0 0; norm_num at this; exact this
  have h12 : (12 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 2 1 0; norm_num at this; exact this
  have h16 : (16 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 4 0 0; norm_num at this; exact this
  have h24 : (24 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 3 1 0; norm_num at this; exact this
  have h36 : (36 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 2 2 0; norm_num at this; exact this
  have h48 : (48 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 4 1 0; norm_num at this; exact this
  have h72 : (72 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 3 2 0; norm_num at this; exact this
  have h120 : (120 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 3 1 1; norm_num at this; exact this
  have h144 : (144 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 4 2 0; norm_num at this; exact this
  have h180 : (180 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 2 2 1; norm_num at this; exact this
  have h240 : (240 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 4 1 1; norm_num at this; exact this
  have h360 : (360 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 3 2 1; norm_num at this; exact this
  have h720 : (720 : F) ≠ 0 := by
    have := smooth_ne_zero h2 h3 h5 4 2 1; norm_num at this; exact this
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have hsix (a b c d e f : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, f⁆⁆⁆⁆⁆ = 0 := h a b c d e f
  have r4a : ⁅x, ⁅x, ⁅y, z⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, z⁆⁆⁆ + ⁅x, ⁅y, ⁅x, z⁆⁆⁆ - ⁅y, ⁅x, ⁅x, z⁆⁆⁆ - ⁅z, ⁅x, ⁅x, y⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅x, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e
    linear_combination (norm := module) e
  have r4b : ⁅y, ⁅y, ⁅x, z⁆⁆⁆ =
      -⁅x, ⁅y, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, y⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅y, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e
    linear_combination (norm := module) -e
  have r4c : ⁅x, ⁅y, ⁅x, y⁆⁆⁆ =
      ⁅y, ⁅x, ⁅x, y⁆⁆⁆ := by
    exact jacobi4c x y
  have r4d : ⁅x, ⁅z, ⁅x, z⁆⁆⁆ =
      ⁅z, ⁅x, ⁅x, z⁆⁆⁆ := by
    exact jacobi4c x z
  have r4e : ⁅x, ⁅z, ⁅y, z⁆⁆⁆ =
      -⁅y, ⁅z, ⁅x, z⁆⁆⁆ + ⁅z, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, z⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅z, ⁅y, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e
    linear_combination (norm := module) -e
  have r4f : ⁅y, ⁅z, ⁅y, z⁆⁆⁆ =
      ⁅z, ⁅y, ⁅y, z⁆⁆⁆ := by
    exact jacobi4c y z
  have r5a : ⁅x, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅x, ⁅x, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) e
  have r5b : ⁅x, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅x, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) e
  have r5c : ⁅x, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅y, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) -e
  have r5d : ⁅x, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅y, ⁅z, ⁅x, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) -e
  have r5e : ⁅x, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅z, ⁅y, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) -e
  have r5f : ⁅x, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆ =
      ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ := by
    have e := lie_skew (x : L) ⁅z, ⁅z, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e
    linear_combination (norm := module) -e

  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, zero_sub, neg_zero, hyx, hzx, hzy, jacobi3 x y z,
    r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f]
  match_scalars <;> field_simp [h2, h3, h5, h4, h6, h8, h12, h16, h24, h36, h48, h72, h120,
    h144, h180, h240, h360, h720]
  all_goals ring

end Assoc

theorem bch_assoc (hnil : lowerCentralSeries F L L 5 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classFive h2 h3 h5 (classFive_of_lowerCentralSeries hnil) x y z

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 5 = ⊥) where
  val : L

@[ext] theorem BCH.ext {hnil : lowerCentralSeries F L L 5 = ⊥}
    {x y : BCH F L hnil} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 5 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 5 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext
    (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) (NeZero.ne 5) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {hL : lowerCentralSeries F L L 5 = ⊥}
  {hM : lowerCentralSeries F M M 5 = ⊥}
  {hN : lowerCentralSeries F N N 5 = ⊥}

@[simp] theorem val_mul (x y : BCH F L hL) :
    (x * y).val = bch (F := F) x.val y.val := rfl

/-- The value formula used to integrate concrete Lie-algebra constructions. -/
theorem val_mul_formula (x y : BCH F L hL) :
    (x * y).val = x.val + y.val + (2 : F)⁻¹ • ⁅x.val, y.val⁆ +
      (12 : F)⁻¹ • (⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅y.val, ⁅y.val, x.val⁆⁆) -
      (24 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ -
      (720 : F)⁻¹ • (⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, x.val⁆⁆⁆⁆ +
        ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆) +
      (360 : F)⁻¹ • (⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, x.val⁆⁆⁆⁆ +
        ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆) +
      (120 : F)⁻¹ • (⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆ +
        ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, x.val⁆⁆⁆⁆) := rfl

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

/-- Every Lie homomorphism between class-at-most-five algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 5 = ⊥)
    (hM : lowerCentralSeries F M M 5 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 5 = ⊥)
    (hM : lowerCentralSeries F M M 5 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
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
end QSearch.BCHClassFive

/-- info: 'QSearch.BCHClassFive.classFive_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.classFive_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassFive.bch_assoc_of_classFive' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.bch_assoc_of_classFive

/-- info: 'QSearch.BCHClassFive.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.bch_assoc

/-- info: 'QSearch.BCHClassFive.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.instGroup

/-- info: 'QSearch.BCHClassFive.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.val_mul_formula

/-- info: 'QSearch.BCHClassFive.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.lieHom

/-- info: 'QSearch.BCHClassFive.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.lieEquiv

/-- info: 'QSearch.BCHClassFive.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFive.val_zpow
