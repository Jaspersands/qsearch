import Mathlib.Algebra.Lie.Nilpotent
import Mathlib.Tactic

/-!
# The class-four BCH group

The group law is the degree-four truncated Baker-Campbell-Hausdorff product
`x + y + [x,y]/2 + ([x,[x,y]] + [y,[y,x]])/12 - [y,[x,[x,y]]]/24`.
Associativity is proved from Jacobi and the actual lower-central bound
`lowerCentralSeries F L L 4 = ⊥`. The field may have positive characteristic:
only 2 and 3 must be nonzero, so every prime field `ZMod p` with `p > 3` is
included. No original grading or supplied associativity identity is assumed.

The proof brings both sides to a normal form: right-normed brackets whose
innermost pair is sorted, rewritten by one degree-three Jacobi rule
(`jacobi3`) and three degree-four Jacobi rules (`r1`, `r2`, `r5`, instances of
`jacobi4b`). The rules were chosen with the exact rational model
`research/audits/reviews/2026-11-02-rees-lean-2/rules4_lean.py`, but Lean does
not rely on that model: it only checks that the two normal forms agree.
-/

namespace QSearch.BCHClassFour

open LieModule

noncomputable section

section Jacobi

variable {L : Type*} [LieRing L]

/-- Explicit length-five bracket vanishing, without a group-law hypothesis. -/
def ClassFour (L : Type*) [LieRing L] : Prop :=
  ∀ a b c d e : L, ⁅a, ⁅b, ⁅c, ⁅d, e⁆⁆⁆⁆ = 0

/-- Degree three: `[c,[a,b]] = [b,[a,c]] - [a,[b,c]]`. -/
theorem jacobi3 (a b c : L) : ⁅c, ⁅a, b⁆⁆ = ⁅b, ⁅a, c⁆⁆ - ⁅a, ⁅b, c⁆⁆ := by
  rw [← lie_skew, lie_lie]
  abel

/-- Degree four, `ad a` applied to Jacobi. -/
theorem jacobi4a (a b c : L) :
    ⁅a, ⁅a, ⁅b, c⁆⁆⁆ = ⁅a, ⁅b, ⁅a, c⁆⁆⁆ - ⁅a, ⁅c, ⁅a, b⁆⁆⁆ := by
  have h : ⁅a, ⁅b, c⁆⁆ = ⁅b, ⁅a, c⁆⁆ - ⁅c, ⁅a, b⁆⁆ := by
    rw [jacobi3 b c a, ← lie_skew b a, ← lie_skew c a, lie_neg, lie_neg]
    abel
  rw [h, lie_sub]

/-- Degree four, antisymmetry of `[[a,b],[a,c]]`. -/
theorem jacobi4b (a b c : L) :
    ⁅c, ⁅a, ⁅a, b⁆⁆⁆ = ⁅a, ⁅b, ⁅a, c⁆⁆⁆ - ⁅b, ⁅a, ⁅a, c⁆⁆⁆ + ⁅a, ⁅c, ⁅a, b⁆⁆⁆ := by
  have h := lie_skew ⁅a, c⁆ ⁅a, b⁆
  rw [lie_lie, lie_lie] at h
  rw [← sub_eq_zero, ← sub_eq_zero.mpr h]
  abel

/-- `jacobi4b` with the innermost pair reversed. -/
theorem jacobi4b' (a b c : L) :
    ⁅c, ⁅a, ⁅b, a⁆⁆⁆ = -⁅a, ⁅b, ⁅a, c⁆⁆⁆ + ⁅b, ⁅a, ⁅a, c⁆⁆⁆ - ⁅a, ⁅c, ⁅a, b⁆⁆⁆ := by
  rw [← lie_skew b a, lie_neg, lie_neg, jacobi4b]
  abel

/-- Degree four, antisymmetry of `[[a,b],[a,b]]`. -/
theorem jacobi4c (a b : L) : ⁅a, ⁅b, ⁅a, b⁆⁆⁆ = ⁅b, ⁅a, ⁅a, b⁆⁆⁆ := by
  have h := lie_self ⁅a, b⁆
  rw [lie_lie] at h
  exact sub_eq_zero.mp h

end Jacobi

variable {F L M N : Type*} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classFour_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 4 = ⊥) : ClassFour L := by
  intro a b c d e
  have h : ⁅a, ⁅b, ⁅c, ⁅d, e⁆⁆⁆⁆ ∈ lowerCentralSeries F L L 4 := by
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top b)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top c)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top d) (LieSubmodule.mem_top e)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The degree-four truncated BCH polynomial. -/
def bch (x y : L) : L :=
  x + y + (2 : F)⁻¹ • ⁅x, y⁆ +
    (12 : F)⁻¹ • (⁅x, ⁅x, y⁆⁆ + ⁅y, ⁅y, x⁆⁆) - (24 : F)⁻¹ • ⁅y, ⁅x, ⁅x, y⁆⁆⁆

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

variable (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
include h2 h3

omit h3 in
theorem four_ne_zero' : (4 : F) ≠ 0 := by
  rw [show (4 : F) = 2 * 2 by ring]; exact mul_ne_zero h2 h2

theorem six_ne_zero' : (6 : F) ≠ 0 := by
  rw [show (6 : F) = 2 * 3 by ring]; exact mul_ne_zero h2 h3

theorem twelve_ne_zero' : (12 : F) ≠ 0 := by
  rw [show (12 : F) = 2 * 2 * 3 by ring]; exact mul_ne_zero (mul_ne_zero h2 h2) h3

theorem twentyfour_ne_zero' : (24 : F) ≠ 0 := by
  rw [show (24 : F) = 2 * 2 * 2 * 3 by ring]
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero h2 h2) h2) h3

/-- Associativity follows from Jacobi and the disappearance of length-five brackets. -/
theorem bch_assoc_of_classFour (h : ClassFour L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
  have h12 := twelve_ne_zero' h2 h3
  have h24 := twentyfour_ne_zero' h2 h3
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have hfive (a b c d e : L) : ⁅a, ⁅b, ⁅c, ⁅d, e⁆⁆⁆⁆ = 0 := h a b c d e
  -- Six degree-four rules, each a Jacobi instance in the degree-three normal form.
  have r1 : ⁅x, ⁅x, ⁅y, z⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, z⁆⁆⁆ + ⁅x, ⁅y, ⁅x, z⁆⁆⁆ - ⁅y, ⁅x, ⁅x, z⁆⁆⁆ - ⁅z, ⁅x, ⁅x, y⁆⁆⁆ := by
    have e := jacobi4b x y z
    simp only [jacobi3 x y z, lie_sub] at e
    linear_combination (norm := module) e
  have r2 : ⁅y, ⁅y, ⁅x, z⁆⁆⁆ =
      -⁅x, ⁅y, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, y⁆⁆⁆ := by
    have e := jacobi4b y x z
    simp only [hyx, lie_neg, jacobi3 x y z, lie_sub] at e
    linear_combination (norm := module) e
  have r5 : ⁅x, ⁅z, ⁅y, z⁆⁆⁆ =
      -⁅y, ⁅z, ⁅x, z⁆⁆⁆ + ⁅z, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, z⁆⁆⁆ := by
    have e := jacobi4b z x y
    simp only [hzx, hzy, lie_neg] at e
    linear_combination (norm := module) -e
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_zero, smul_zero,
    add_zero, sub_zero, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r1, r2, r5]
  match_scalars <;> field_simp [h2, h12, h24]
  all_goals ring

end Assoc

theorem bch_assoc (hnil : lowerCentralSeries F L L 4 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classFour h2 h3 (classFour_of_lowerCentralSeries hnil) x y z

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 4 = ⊥) where
  val : L

@[ext] theorem BCH.ext {hnil : lowerCentralSeries F L L 4 = ⊥}
    {x y : BCH F L hnil} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 4 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 4 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {hL : lowerCentralSeries F L L 4 = ⊥}
  {hM : lowerCentralSeries F M M 4 = ⊥}
  {hN : lowerCentralSeries F N N 4 = ⊥}

@[simp] theorem val_mul (x y : BCH F L hL) :
    (x * y).val = bch (F := F) x.val y.val := rfl

/-- The value formula used to integrate concrete Lie-algebra constructions. -/
theorem val_mul_formula (x y : BCH F L hL) :
    (x * y).val = x.val + y.val + (2 : F)⁻¹ • ⁅x.val, y.val⁆ +
      (12 : F)⁻¹ • (⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅y.val, ⁅y.val, x.val⁆⁆) -
      (24 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ := rfl

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

/-- Every Lie homomorphism between class-at-most-four algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 4 = ⊥)
    (hM : lowerCentralSeries F M M 4 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 4 = ⊥)
    (hM : lowerCentralSeries F M M 4 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
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
end QSearch.BCHClassFour

/-- info: 'QSearch.BCHClassFour.classFour_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.classFour_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassFour.bch_assoc_of_classFour' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_assoc_of_classFour

/-- info: 'QSearch.BCHClassFour.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.bch_assoc

/-- info: 'QSearch.BCHClassFour.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.instGroup

/-- info: 'QSearch.BCHClassFour.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_mul_formula

/-- info: 'QSearch.BCHClassFour.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieHom

/-- info: 'QSearch.BCHClassFour.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.lieEquiv

/-- info: 'QSearch.BCHClassFour.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFour.val_zpow
