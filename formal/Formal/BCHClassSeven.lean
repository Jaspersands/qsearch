import Formal.BCHClassSix

/-!
# The class-seven BCH group

The group law is the degree-seven truncated Baker-Campbell-Hausdorff product: the
sextic law of `BCHClassSix` plus the degree-seven part, written with right-normed
words in `x, y` (`xxyyxy` stands for `[x,[x,[y,[y,[x,y]]]]]`):
 + 1/1120·(xyxxyxy)
 - 1/1120·(yxyxyxy)
 + 1/2520·(xyyxyxy)
 - 1/2520·(yxxxyxy)
 + 1/5040·(xyxxxxy)
 - 1/5040·(yxyyyxy)
 + 1/10080·(xxxxyxy + xxyyyxy + xyyyyxy + yxxyyxy)
 - 1/10080·(xyyxxxy + yxxxxxy + yyxxxxy + yyyxyxy)
 + 1/30240·(xxxxxxy + yyyxxxy)
 - 1/30240·(xxxyyxy + yyyyyxy)
The degree-seven coefficients have denominators dividing `2^5 3^3 5 7 = 30240`,
so the law needs `2, 3, 5, 7 ≠ 0` in the field; every `ZMod p` with `p > 7` (so
every prime `p ≥ 11`) is included.

Associativity is proved from Jacobi and the lower-central bound
`lowerCentralSeries F L L 7 = ⊥` in two parts. First, the degree-seven part `z7`
is central and depends only on the degree-one parts of its arguments
(`z7_central`, `z7_peel_left`, `z7_peel_right`, applied to `bch_shape`), and a
central summand passes through the sextic law (`six_central_left/right`), so
both sides reduce to the sextic law of `BCHClassSix` plus `z7` terms. Second,
the remaining identity `defect` is checked as in `BCHClassSix`: both sides are
brought to a normal form of right-normed brackets in `x, y, z` (innermost pair
sorted), rewritten by one degree-three rule (`jacobi3 x y z`), 6 degree-four,
6 degree-five, 28 degree-six and 36 degree-seven rules. The irreducible
words are a basis of the free class-seven Lie algebra on three generators
(3, 3, 8, 18, 48, 116, 312 words in degrees 1-7), so the normal form is unique. Each rule is
proved in Lean from a few `lie_skew` or `lie_self` instances with integer
coefficients. The rules and certificates were chosen with the exact rational
model `research/audits/reviews/2026-11-05-rees-lean-c7/rules7.py`, and the
degree-seven coefficients were cross-checked against Dynkin's formula, a
Varadarajan recursion in Sage and nilpotent matrices (`cross7.py`,
`check_lean_def7.py`); Lean does not rely on any of them, it proves every rule
and checks that the two normal forms agree.
-/

namespace QSearch.BCHClassSeven

open LieModule
open QSearch.BCHClassFour (jacobi3 jacobi4c)

noncomputable section

/-- Explicit length-eight bracket vanishing, without a group-law hypothesis. -/
def ClassSeven (L : Type*) [LieRing L] : Prop :=
  ∀ a b c d e f g k : L, ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0

variable {F L M N : Type*} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classSeven_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 7 = ⊥) : ClassSeven L := by
  intro a b c d e f g k
  have h : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ ∈ lowerCentralSeries F L L 7 := by
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top b)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top c)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top d)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top e)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top f)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top g) (LieSubmodule.mem_top k)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The degree-seven truncated BCH polynomial. -/
def bch (x y : L) : L :=
  x + y + (2 : F)⁻¹ • ⁅x, y⁆ +
    (12 : F)⁻¹ • (⁅x, ⁅x, y⁆⁆ + ⁅y, ⁅y, x⁆⁆) - (24 : F)⁻¹ • ⁅y, ⁅x, ⁅x, y⁆⁆⁆ -
    (720 : F)⁻¹ • (⁅y, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆) +
    (360 : F)⁻¹ • (⁅x, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆) +
    (120 : F)⁻¹ • (⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, x⁆⁆⁆⁆) -
    (720 : F)⁻¹ • ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + (240 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ +
    (1440 : F)⁻¹ • (⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆) +
    (1120 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (1120 : F)⁻¹ • ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (2520 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (2520 : F)⁻¹ • ⁅y, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (5040 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (5040 : F)⁻¹ • ⁅y, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (10080 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆) -
    (10080 : F)⁻¹ • (⁅x, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆) +
    (30240 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆) -
    (30240 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆)

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

/-- The degree-seven part of `bch`. -/
def z7 (x y : L) : L :=
  (1120 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (1120 : F)⁻¹ • ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (2520 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (2520 : F)⁻¹ • ⁅y, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (5040 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ -
    (5040 : F)⁻¹ • ⁅y, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ +
    (10080 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆) -
    (10080 : F)⁻¹ • (⁅x, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆) +
    (30240 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆) -
    (30240 : F)⁻¹ • (⁅x, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆)

theorem bch_eq_six_add (x y : L) :
    bch (F := F) x y = QSearch.BCHClassSix.bch (F := F) x y + z7 (F := F) x y := by
  simp only [bch, QSearch.BCHClassSix.bch, z7]
  abel

/-- `bch` as `x + y` plus scalar multiples of single brackets `[p, q]`. -/
theorem bch_shape (x y : L) :
    bch (F := F) x y =
      x + y + (2 : F)⁻¹ • ⁅x, y⁆ + (12 : F)⁻¹ • ⁅x, ⁅x, y⁆⁆ + (12 : F)⁻¹ • ⁅y, ⁅y, x⁆⁆
      + (-(24 : F)⁻¹) • ⁅y, ⁅x, ⁅x, y⁆⁆⁆ + (-(720 : F)⁻¹) • ⁅y, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆
      + (-(720 : F)⁻¹) • ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆ + (360 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅y, x⁆⁆⁆⁆
      + (360 : F)⁻¹ • ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆ + (120 : F)⁻¹ • ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆
      + (120 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅y, x⁆⁆⁆⁆ + (-(720 : F)⁻¹) • ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆
      + (240 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆
      + (1440 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆
      + (1440 : F)⁻¹ • ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆
      + (30240 : F)⁻¹ • ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (10080 : F)⁻¹ • ⁅x, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(30240 : F)⁻¹) • ⁅x, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (10080 : F)⁻¹ • ⁅x, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (5040 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (1120 : F)⁻¹ • ⁅x, ⁅y, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(10080 : F)⁻¹) • ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (2520 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (10080 : F)⁻¹ • ⁅x, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(10080 : F)⁻¹) • ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(2520 : F)⁻¹) • ⁅y, ⁅x, ⁅x, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (10080 : F)⁻¹ • ⁅y, ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(1120 : F)⁻¹) • ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(5040 : F)⁻¹) • ⁅y, ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(10080 : F)⁻¹) • ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (30240 : F)⁻¹ • ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(10080 : F)⁻¹) • ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆
      + (-(30240 : F)⁻¹) • ⁅y, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
  simp only [bch]
  module

section Central

variable (h : ClassSeven L)
include h

set_option linter.unusedSimpArgs false in
/-- Every degree-seven term is central. -/
theorem z7_central (a b w : L) : ⁅w, z7 (F := F) a b⁆ = 0 := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, lie_add, lie_sub, lie_neg, lie_smul, height, smul_zero, add_zero, sub_zero,
    neg_zero]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket added to its first argument. -/
theorem z7_peel_left (u v p q : L) (t : F) :
    z7 (F := F) (u + t • ⁅p, q⁆) v = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket added to its second argument. -/
theorem z7_peel_right (u v p q : L) (t : F) :
    z7 (F := F) u (v + t • ⁅p, q⁆) = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

omit h in
/-- A central summand passes through the sextic law (first argument). -/
theorem six_central_left (u v c : L) (hc : ∀ w : L, ⁅w, c⁆ = 0) :
    QSearch.BCHClassSix.bch (F := F) (u + c) v = QSearch.BCHClassSix.bch (F := F) u v + c := by
  have hc' : ∀ w : L, ⁅c, w⁆ = 0 := fun w => by rw [← lie_skew, hc, neg_zero]
  simp only [QSearch.BCHClassSix.bch, add_lie, lie_add, hc, hc', add_zero]
  abel

omit h in
/-- A central summand passes through the sextic law (second argument). -/
theorem six_central_right (u v c : L) (hc : ∀ w : L, ⁅w, c⁆ = 0) :
    QSearch.BCHClassSix.bch (F := F) u (v + c) = QSearch.BCHClassSix.bch (F := F) u v + c := by
  have hc' : ∀ w : L, ⁅c, w⁆ = 0 := fun w => by rw [← lie_skew, hc, neg_zero]
  simp only [QSearch.BCHClassSix.bch, add_lie, lie_add, hc, hc', add_zero]
  abel

end Central

section Assoc

variable (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (h7 : (7 : F) ≠ 0)
include h2 h3 h5 h7

/-- Products of the excluded primes are nonzero. -/
theorem smooth7_ne_zero (a b c d : ℕ) : ((2 : F) ^ a * 3 ^ b * 5 ^ c * 7 ^ d) ≠ 0 :=
  mul_ne_zero (mul_ne_zero (mul_ne_zero (pow_ne_zero _ h2) (pow_ne_zero _ h3))
    (pow_ne_zero _ h5)) (pow_ne_zero _ h7)

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- The associativity defect of the sextic law in class seven, balanced by `z7`. -/
theorem defect (h : ClassSeven L) (x y z : L) :
    QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y +
        z7 (F := F) (x + y) z =
      QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) +
        z7 (F := F) y z + z7 (F := F) x (y + z) := by
  have h4 : (4 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 2 0 0 0; norm_num at this; exact this
  have h6 : (6 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 1 1 0 0; norm_num at this; exact this
  have h8 : (8 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 0 0 0; norm_num at this; exact this
  have h12 : (12 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 2 1 0 0; norm_num at this; exact this
  have h16 : (16 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 0 0 0; norm_num at this; exact this
  have h24 : (24 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 1 0 0; norm_num at this; exact this
  have h36 : (36 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 2 2 0 0; norm_num at this; exact this
  have h48 : (48 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 1 0 0; norm_num at this; exact this
  have h72 : (72 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 2 0 0; norm_num at this; exact this
  have h120 : (120 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 1 1 0; norm_num at this; exact this
  have h144 : (144 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 2 0 0; norm_num at this; exact this
  have h180 : (180 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 2 2 1 0; norm_num at this; exact this
  have h240 : (240 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 1 1 0; norm_num at this; exact this
  have h360 : (360 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 2 1 0; norm_num at this; exact this
  have h720 : (720 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 2 1 0; norm_num at this; exact this
  have h1120 : (1120 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 5 0 1 1; norm_num at this; exact this
  have h1440 : (1440 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 5 2 1 0; norm_num at this; exact this
  have h2520 : (2520 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 3 2 1 1; norm_num at this; exact this
  have h5040 : (5040 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 4 2 1 1; norm_num at this; exact this
  have h10080 : (10080 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 5 2 1 1; norm_num at this; exact this
  have h30240 : (30240 : F) ≠ 0 := by
    have := smooth7_ne_zero h2 h3 h5 h7 5 3 1 1; norm_num at this; exact this
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  have r4a : ⁅x, ⁅x, ⁅y, z⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, z⁆⁆⁆ + ⁅x, ⁅y, ⁅x, z⁆⁆⁆ - ⁅y, ⁅x, ⁅x, z⁆⁆⁆ - ⁅z, ⁅x, ⁅x, y⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e0
    linear_combination (norm := module) e0
  have r4b : ⁅y, ⁅y, ⁅x, z⁆⁆⁆ =
      -⁅x, ⁅y, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅y, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, y⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e0
    linear_combination (norm := module) -e0
  have r4c : ⁅x, ⁅y, ⁅x, y⁆⁆⁆ =
      ⁅y, ⁅x, ⁅x, y⁆⁆⁆ := by
    exact jacobi4c x y
  have r4d : ⁅x, ⁅z, ⁅x, z⁆⁆⁆ =
      ⁅z, ⁅x, ⁅x, z⁆⁆⁆ := by
    exact jacobi4c x z
  have r4e : ⁅x, ⁅z, ⁅y, z⁆⁆⁆ =
      -⁅y, ⁅z, ⁅x, z⁆⁆⁆ + ⁅z, ⁅x, ⁅y, z⁆⁆⁆ + ⁅z, ⁅y, ⁅x, z⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, z⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z] at e0
    linear_combination (norm := module) -e0
  have r4f : ⁅y, ⁅z, ⁅y, z⁆⁆⁆ =
      ⁅z, ⁅y, ⁅y, z⁆⁆⁆ := by
    exact jacobi4c y z
  have r5a : ⁅x, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅x, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) e0
  have r5b : ⁅x, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) e0
  have r5c : ⁅x, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) -e0
  have r5d : ⁅x, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅x, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) -e0
  have r5e : ⁅x, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) -e0
  have r5f : ⁅x, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆ =
      ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅y, z⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f] at e0
    linear_combination (norm := module) -e0
  have r6a : ⁅x, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6b : ⁅x, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ =
      -⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6c : ⁅x, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0 e1
    linear_combination (norm := module) e0 - e1
  have r6d : ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6e : ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6f : ⁅x, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ =
      -⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0 e1
    linear_combination (norm := module) -e0 + e1
  have r6g : ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6h : ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6i : ⁅x, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6j : ⁅x, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0 e1
    linear_combination (norm := module) -e0 + e1
  have r6k : ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6l : ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ =
      ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6m : ⁅x, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6n : ⁅x, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6o : ⁅x, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0 e1
    linear_combination (norm := module) -e0 + e1
  have r6p : ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6q : ⁅x, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6r : ⁅x, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6s : ⁅x, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6t : ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0 e1
    linear_combination (norm := module) e0 + e1
  have r6u : ⁅x, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6v : ⁅x, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6w : ⁅x, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6x : ⁅x, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ =
      ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6y : ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ =
      -⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r6z : ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (y : L) ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6aa : ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (y : L) ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) e0
  have r6bb : ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ =
      ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (y : L) ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f] at e0
    linear_combination (norm := module) -e0
  have r7a : ⁅x, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) e0
  have r7b : ⁅x, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) e0 + e1
  have r7c : ⁅x, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) e0
  have r7d : ⁅x, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) e0
  have r7e : ⁅x, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) e0 - e1
  have r7f : ⁅x, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7g : ⁅x, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆
    have e2 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1 e2
    linear_combination (norm := module) e0 - e1 - e1 - e2 - e2
  have r7h : ⁅x, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7i : ⁅x, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) e0 + e1
  have r7j : ⁅x, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7k : ⁅x, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) e0
  have r7l : ⁅x, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) -e0 - e1
  have r7m : ⁅x, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) e0 - e1
  have r7n : ⁅x, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7o : ⁅x, ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    have e1 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0 e1
    linear_combination (norm := module) -e0 + e1
  have r7p : ⁅x, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7q : ⁅x, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7r : ⁅x, ⁅y, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7s : ⁅x, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7t : ⁅x, ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7u : ⁅x, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7v : ⁅x, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7w : ⁅x, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅x, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) e0
  have r7x : ⁅x, ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7y : ⁅x, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7z : ⁅x, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7aa : ⁅x, ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7bb : ⁅x, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7cc : ⁅x, ⁅z, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7dd : ⁅x, ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      -⁅x, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7ee : ⁅x, ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7ff : ⁅x, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ =
      ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅x, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅x, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅x, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅x, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅x, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7gg : ⁅x, ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7hh : ⁅x, ⁅z, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅y, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅y, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅y, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅y, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7ii : ⁅x, ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      -⁅y, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅y, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅y, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, y⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅z, ⁅y, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0
  have r7jj : ⁅x, ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆⁆ =
      ⁅y, ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅y, ⁅z, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅y, ⁅z, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ - ⁅z, ⁅z, ⁅z, ⁅y, ⁅z, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅z, ⁅x, ⁅y, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ + ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, ⁅x, z⁆⁆⁆⁆⁆⁆ := by
    have e0 := lie_skew (x : L) ⁅z, ⁅z, ⁅z, ⁅z, ⁅y, z⁆⁆⁆⁆⁆
    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z, r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb] at e0
    linear_combination (norm := module) -e0

  simp (maxSteps := 100000000) only [QSearch.BCHClassSix.bch, z7, add_lie, lie_add, sub_lie,
    lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, zero_sub, neg_zero, hyx, hzx, hzy, jacobi3 x y z,
    r4a, r4b, r4c, r4d, r4e, r4f, r5a, r5b, r5c, r5d, r5e, r5f, r6a, r6b, r6c, r6d, r6e, r6f, r6g, r6h, r6i, r6j, r6k, r6l, r6m, r6n, r6o, r6p, r6q, r6r, r6s, r6t, r6u, r6v, r6w, r6x, r6y, r6z, r6aa, r6bb, r7a, r7b, r7c, r7d, r7e, r7f, r7g, r7h, r7i, r7j, r7k, r7l, r7m, r7n, r7o, r7p, r7q, r7r, r7s, r7t, r7u, r7v, r7w, r7x, r7y, r7z, r7aa, r7bb, r7cc, r7dd, r7ee, r7ff, r7gg, r7hh, r7ii, r7jj]
  match_scalars <;> field_simp [h2, h3, h5, h7, h4, h6, h8, h12, h16, h24, h36, h48, h72, h120, h144, h180, h240, h360, h720, h1120, h1440, h2520, h5040, h10080, h30240]
  all_goals ring

omit h2 h3 h5 h7 in
/-- Associativity follows from Jacobi and the disappearance of length-eight brackets. -/
theorem bch_assoc_of_classSeven' (hdef : ∀ x y z : L,
      QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y +
          z7 (F := F) (x + y) z =
        QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) +
          z7 (F := F) y z + z7 (F := F) x (y + z))
    (h : ClassSeven L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
  have e1 : z7 (F := F) (bch (F := F) x y) z = z7 (F := F) (x + y) z := by
    rw [bch_shape x y]
    simp only [z7_peel_left h]
  have e2 : QSearch.BCHClassSix.bch (F := F) (bch (F := F) x y) z =
      QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y := by
    rw [bch_eq_six_add x y, six_central_left _ _ _ (fun w => z7_central h x y w)]
  have e3 : z7 (F := F) x (bch (F := F) y z) = z7 (F := F) x (y + z) := by
    rw [bch_shape y z]
    simp only [z7_peel_right h]
  have e4 : QSearch.BCHClassSix.bch (F := F) x (bch (F := F) y z) =
      QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) + z7 (F := F) y z := by
    rw [bch_eq_six_add y z, six_central_right _ _ _ (fun w => z7_central h y z w)]
  rw [bch_eq_six_add (bch (F := F) x y) z, bch_eq_six_add x (bch (F := F) y z), e1, e2, e3, e4]
  exact hdef x y z

/-- Associativity follows from Jacobi and the disappearance of length-eight brackets. -/
theorem bch_assoc_of_classSeven (h : ClassSeven L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classSeven' (defect h2 h3 h5 h7 h) h x y z

end Assoc

theorem bch_assoc (hnil : lowerCentralSeries F L L 7 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (h7 : (7 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classSeven h2 h3 h5 h7 (classSeven_of_lowerCentralSeries hnil) x y z

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 7 = ⊥) where
  val : L

@[ext] theorem BCH.ext {hnil : lowerCentralSeries F L L 7 = ⊥}
    {x y : BCH F L hnil} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 7 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 7 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext
    (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) (NeZero.ne 5) (NeZero.ne 7) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {hL : lowerCentralSeries F L L 7 = ⊥}
  {hM : lowerCentralSeries F M M 7 = ⊥}
  {hN : lowerCentralSeries F N N 7 = ⊥}

@[simp] theorem val_mul (x y : BCH F L hL) :
    (x * y).val = bch (F := F) x.val y.val := rfl

/-- The value formula used to integrate concrete Lie-algebra constructions. -/
theorem val_mul_formula (x y : BCH F L hL) :
    (x * y).val = x.val + y.val + (2 : F)⁻¹ • ⁅x.val, y.val⁆ +
      (12 : F)⁻¹ • (⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅y.val, ⁅y.val, x.val⁆⁆) - (24 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ -
      (720 : F)⁻¹ • (⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, x.val⁆⁆⁆⁆ + ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆) +
      (360 : F)⁻¹ • (⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, x.val⁆⁆⁆⁆ + ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆) +
      (120 : F)⁻¹ • (⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆ + ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, x.val⁆⁆⁆⁆) -
      (720 : F)⁻¹ • ⁅x.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ + (240 : F)⁻¹ • ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ +
      (1440 : F)⁻¹ • (⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ + ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆) +
      (1120 : F)⁻¹ • ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ -
      (1120 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ +
      (2520 : F)⁻¹ • ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ -
      (2520 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ +
      (5040 : F)⁻¹ • ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ -
      (5040 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ +
      (10080 : F)⁻¹ • (⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅x.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅x.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆) -
      (10080 : F)⁻¹ • (⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆) +
      (30240 : F)⁻¹ • (⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆) -
      (30240 : F)⁻¹ • (⁅x.val, ⁅x.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ + ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆) := rfl

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

/-- Every Lie homomorphism between class-at-most-seven algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 7 = ⊥)
    (hM : lowerCentralSeries F M M 7 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 7 = ⊥)
    (hM : lowerCentralSeries F M M 7 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
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
end QSearch.BCHClassSeven

/-- info: 'QSearch.BCHClassSeven.classSeven_of_lowerCentralSeries' depends on axioms: [propext, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.classSeven_of_lowerCentralSeries

/-- info: 'QSearch.BCHClassSeven.bch_assoc_of_classSeven' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.bch_assoc_of_classSeven

/-- info: 'QSearch.BCHClassSeven.bch_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.bch_assoc

/-- info: 'QSearch.BCHClassSeven.instGroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.instGroup

/-- info: 'QSearch.BCHClassSeven.val_mul_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.val_mul_formula

/-- info: 'QSearch.BCHClassSeven.lieHom' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.lieHom

/-- info: 'QSearch.BCHClassSeven.lieEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.lieEquiv

/-- info: 'QSearch.BCHClassSeven.val_zpow' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSeven.val_zpow
