import Formal.BCHClassFive
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-five BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 5`. The words
were designed with the exact rational model
`research/audits/reviews/2026-11-04-rees-lean-c5/words5.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of the
  two degree-three, three degree-four and six degree-five iterated commutators,
  has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-5 (one, two, three and six of them) has logarithm exactly `x + y`.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, and `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`). In two
letters no degree-five rule is needed: the six words `a·w` (`w` one of the three
degree-four normal words) are a basis.
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassFiveSubgroups

open LieModule QSearch.BCHClassFive
open QSearch.BCHClassFour (jacobi4c)

noncomputable section

section Numerals

variable {F : Type*} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

theorem ne4 : (4 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 0 0
  norm_num at this; exact this

theorem ne6 : (6 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 1 1 0
  norm_num at this; exact this

theorem ne8 : (8 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 0 0
  norm_num at this; exact this

theorem ne10 : (10 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 1 0 1
  norm_num at this; exact this

theorem ne12 : (12 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 1 0
  norm_num at this; exact this

theorem ne15 : (15 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 0 1 1
  norm_num at this; exact this

theorem ne16 : (16 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 4 0 0
  norm_num at this; exact this

theorem ne20 : (20 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 0 1
  norm_num at this; exact this

theorem ne24 : (24 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 1 0
  norm_num at this; exact this

theorem ne30 : (30 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 1 1 1
  norm_num at this; exact this

theorem ne36 : (36 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 2 0
  norm_num at this; exact this

theorem ne40 : (40 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 0 1
  norm_num at this; exact this

theorem ne48 : (48 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 4 1 0
  norm_num at this; exact this

theorem ne60 : (60 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 1 1
  norm_num at this; exact this

theorem ne72 : (72 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 2 0
  norm_num at this; exact this

theorem ne120 : (120 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 1 1
  norm_num at this; exact this

theorem ne144 : (144 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 4 2 0
  norm_num at this; exact this

theorem ne180 : (180 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 2 2 1
  norm_num at this; exact this

theorem ne240 : (240 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 4 1 1
  norm_num at this; exact this

theorem ne360 : (360 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 3 2 1
  norm_num at this; exact this

theorem ne720 : (720 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 4 2 1
  norm_num at this; exact this

end Numerals

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
theorem quint_central (hnil : lowerCentralSeries F L L 5 = ⊥) (a b c d e f : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, f⁆⁆⁆⁆⁆ = 0 :=
  classFive_of_lowerCentralSeries hnil a b c d e f

/-- The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form. -/
def commPoly (a b : L) : L :=
  ⁅a, b⁆ + (1 / 2 : F) • ⁅a, ⁅a, b⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, b⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 4 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆ + (1 / 24 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 12 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x,y))`. -/
def p3x (a b : L) : L :=
  ⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (7 / 12 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x,y))`. -/
def p3y (a b : L) : L :=
  ⁅b, ⁅a, b⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 6 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x,y)))`. -/
def p4xx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (3 / 2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x,y)))`. -/
def p4yx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x,y)))`. -/
def p4yy (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, b⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆

set_option maxHeartbeats 4000000 in
/-- The commutator polynomial, derived from the quintic BCH law. -/
theorem bch_comm (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b) =
      commPoly (F := F) a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne40 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F)]
  all_goals ring

set_option maxHeartbeats 1000000 in
/-- `C(a, C(a,b))`. -/
theorem commPoly_left (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) a (commPoly (F := F) a b) =
      p3x (F := F) a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne40 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F)]
  all_goals ring

set_option maxHeartbeats 1000000 in
/-- `C(b, C(a,b))`. -/
theorem commPoly_right (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (commPoly (F := F) a b) =
      p3y (F := F) a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne40 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F)]
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 1000000 in
/-- `C(a, C(a, C(a,b)))`. -/
theorem commPoly_ll (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) a (p3x (F := F) a b) =
      p4xx (F := F) a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F)]
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 1000000 in
/-- `C(b, C(a, C(a,b)))`. -/
theorem commPoly_rl (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (p3x (F := F) a b) =
      p4yx a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F)]
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 1000000 in
/-- `C(b, C(b, C(a,b)))`. -/
theorem commPoly_rr (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (p3y (F := F) a b) =
      p4yy (F := F) a b := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F)]
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_xxx (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) a (p4xx (F := F) a b) =
      ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_yxx (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (p4xx (F := F) a b) =
      ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_xyx (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yx a b) =
      ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_yyx (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yx a b) =
      ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_xyy (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yy (F := F) a b) =
      ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
/-- A degree-five commutator is its central bracket. -/
theorem commPoly_yyy (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yy (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ := by
  have hsix := quint_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]

end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] {hnil : lowerCentralSeries F L L 5 = ⊥}

/-- Our commutator convention is `x * y * x⁻¹ * y⁻¹`. -/
def comm (x y : BCH F L hnil) : BCH F L hnil := x * y * x⁻¹ * y⁻¹

theorem comm_mem (H : Subgroup (BCH F L hnil)) {x y : BCH F L hnil}
    (hx : x ∈ H) (hy : y ∈ H) : comm x y ∈ H :=
  H.mul_mem (H.mul_mem (H.mul_mem hx hy) (H.inv_mem hx)) (H.inv_mem hy)

theorem val_comm (x y : BCH F L hnil) :
    (comm x y).val = commPoly (F := F) x.val y.val :=
  bch_comm hnil x.val y.val

theorem val_comm_left (x y : BCH F L hnil) :
    (comm x (comm x y)).val = p3x (F := F) x.val y.val := by
  rw [val_comm, val_comm, commPoly_left hnil]

theorem val_comm_right (x y : BCH F L hnil) :
    (comm y (comm x y)).val = p3y (F := F) x.val y.val := by
  rw [val_comm, val_comm, commPoly_right hnil]

theorem val_comm_ll (x y : BCH F L hnil) :
    (comm x (comm x (comm x y))).val = p4xx (F := F) x.val y.val := by
  rw [val_comm, val_comm_left, commPoly_ll hnil]

theorem val_comm_rl (x y : BCH F L hnil) :
    (comm y (comm x (comm x y))).val = p4yx x.val y.val := by
  rw [val_comm, val_comm_left, commPoly_rl hnil]

theorem val_comm_rr (x y : BCH F L hnil) :
    (comm y (comm y (comm x y))).val = p4yy (F := F) x.val y.val := by
  rw [val_comm, val_comm_right, commPoly_rr hnil]

theorem val_comm_xxx (x y : BCH F L hnil) :
    (comm x (comm x (comm x (comm x y)))).val = ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_ll, commPoly_xxx hnil]

theorem val_comm_yxx (x y : BCH F L hnil) :
    (comm y (comm x (comm x (comm x y)))).val = ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_ll, commPoly_yxx hnil]

theorem val_comm_xyx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm x y)))).val = ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_rl, commPoly_xyx hnil]

theorem val_comm_yyx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm x y)))).val = ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_rl, commPoly_yyx hnil]

theorem val_comm_xyy (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm x y)))).val = ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_rr, commPoly_xyy hnil]

theorem val_comm_yyy (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm x y)))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_rr, commPoly_yyy hnil]

end Words

/-- Install with `letI := neZeroTwo hp` when the characteristic bound is explicit. -/
theorem neZeroTwo {p : ℕ} (hp : 5 < p) : NeZero (2 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 2 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroThree hp` when the characteristic bound is explicit. -/
theorem neZeroThree {p : ℕ} (hp : 5 < p) : NeZero (3 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 3 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroFive hp` when the characteristic bound is explicit. -/
theorem neZeroFive {p : ℕ} (hp : 5 < p) : NeZero (5 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 5 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) hp)⟩

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)]
  {hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val

/-- Removing the degree-three, degree-four and then the central degree-five
corrections from the group commutator recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  comm x y *
    powerScalar (-(1 / 2) : ZMod p) (comm x (comm x y)) *
    powerScalar (-(1 / 2) : ZMod p) (comm y (comm x y)) *
    powerScalar (1 / 3 : ZMod p) (comm x (comm x (comm x y))) *
    powerScalar (1 / 4 : ZMod p) (comm y (comm x (comm x y))) *
    powerScalar (1 / 3 : ZMod p) (comm y (comm y (comm x y))) *
    powerScalar (-(1 / 4) : ZMod p) (comm x (comm x (comm x (comm x y)))) *
    powerScalar (-(3 / 4) : ZMod p) (comm y (comm x (comm x (comm x y)))) *
    powerScalar (7 / 12 : ZMod p) (comm x (comm y (comm x (comm x y)))) *
    powerScalar (-(2 / 3) : ZMod p) (comm y (comm y (comm x (comm x y)))) *
    powerScalar (1 / 2 : ZMod p) (comm x (comm y (comm y (comm x y)))) *
    powerScalar (-(1 / 4) : ZMod p) (comm y (comm y (comm y (comm x y))))

set_option maxHeartbeats 8000000 in
theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, val_comm, val_comm_left, val_comm_right, val_comm_ll,
    val_comm_rl, val_comm_rr, val_comm_xxx, val_comm_yxx, val_comm_xyx, val_comm_yyx,
    val_comm_xyy, val_comm_yyy]
  have hsix := quint_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, commPoly, p3x, p3y, p4xx, p4yx, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c x.val y.val]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne20 (F := ZMod p), ne24 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne40 (F := ZMod p), ne48 (F := ZMod p), ne60 (F := ZMod p), ne72 (F := ZMod p), ne120 (F := ZMod p), ne144 (F := ZMod p), ne180 (F := ZMod p), ne240 (F := ZMod p), ne360 (F := ZMod p), ne720 (F := ZMod p)])
  all_goals ring

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
  have hc := comm_mem H hx hy
  have hcx := comm_mem H hx hc
  have hcy := comm_mem H hy hc
  have hcxx := comm_mem H hx hcx
  have hcyx := comm_mem H hy hcx
  have hcyy := comm_mem H hy hcy
  have m5xxx := comm_mem H hx hcxx
  have m5yxx := comm_mem H hy hcxx
  have m5xyx := comm_mem H hx hcyx
  have m5yyx := comm_mem H hy hcyx
  have m5xyy := comm_mem H hx hcyy
  have m5yyy := comm_mem H hy hcyy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (hc)
    (powerScalar_mem H _ hcx))
    (powerScalar_mem H _ hcy))
    (powerScalar_mem H _ hcxx))
    (powerScalar_mem H _ hcyx))
    (powerScalar_mem H _ hcyy))
    (powerScalar_mem H _ m5xxx))
    (powerScalar_mem H _ m5yxx))
    (powerScalar_mem H _ m5xyx))
    (powerScalar_mem H _ m5yyx))
    (powerScalar_mem H _ m5xyy))
    (powerScalar_mem H _ m5yyy)

/-- Addition is recovered by removing the bracket, then the degree-three,
degree-four and central degree-five errors, each by a power of an exact
bracket monomial. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x * y *
    powerScalar (-(1 / 2) : ZMod p) (bracketWord x y) *
    powerScalar (1 / 6 : ZMod p) (bracketWord x (bracketWord x y)) *
    powerScalar (1 / 3 : ZMod p) (bracketWord y (bracketWord x y)) *
    powerScalar (-(1 / 24) : ZMod p) (bracketWord x (bracketWord x (bracketWord x y))) *
    powerScalar (-(1 / 8) : ZMod p) (bracketWord y (bracketWord x (bracketWord x y))) *
    powerScalar (-(1 / 8) : ZMod p) (bracketWord y (bracketWord y (bracketWord x y))) *
    powerScalar (1 / 120 : ZMod p) (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))) *
    powerScalar (-(1 / 60) : ZMod p) (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))) *
    powerScalar (1 / 20 : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord x y)))) *
    powerScalar (-(1 / 20) : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))) *
    powerScalar (1 / 10 : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord x y)))) *
    powerScalar (1 / 30 : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord x y))))

set_option maxHeartbeats 8000000 in
theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
  have hsix := quint_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c x.val y.val]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne20 (F := ZMod p), ne24 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne40 (F := ZMod p), ne48 (F := ZMod p), ne60 (F := ZMod p), ne72 (F := ZMod p), ne120 (F := ZMod p), ne144 (F := ZMod p), ne180 (F := ZMod p), ne240 (F := ZMod p), ne360 (F := ZMod p), ne720 (F := ZMod p)])
  all_goals ring

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
  have b2 := bracketWord_mem H hx hy
  have b3x := bracketWord_mem H hx b2
  have b3y := bracketWord_mem H hy b2
  have b4xx := bracketWord_mem H hx b3x
  have b4yx := bracketWord_mem H hy b3x
  have b4yy := bracketWord_mem H hy b3y
  have b5xxx := bracketWord_mem H hx b4xx
  have b5yxx := bracketWord_mem H hy b4xx
  have b5xyx := bracketWord_mem H hx b4yx
  have b5yyx := bracketWord_mem H hy b4yx
  have b5xyy := bracketWord_mem H hx b4yy
  have b5yyy := bracketWord_mem H hy b4yy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem hx hy)
    (powerScalar_mem H _ b2))
    (powerScalar_mem H _ b3x))
    (powerScalar_mem H _ b3y))
    (powerScalar_mem H _ b4xx))
    (powerScalar_mem H _ b4yx))
    (powerScalar_mem H _ b4yy))
    (powerScalar_mem H _ b5xxx))
    (powerScalar_mem H _ b5yxx))
    (powerScalar_mem H _ b5xyx))
    (powerScalar_mem H _ b5yyx))
    (powerScalar_mem H _ b5xyy))
    (powerScalar_mem H _ b5yyy)

theorem mk_smul_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p) {x : L}
    (hx : BCH.mk x ∈ H) : BCH.mk (t • x) ∈ H := by
  have heq : powerScalar t (BCH.mk x : BCH (ZMod p) L hnil) = BCH.mk (t • x) :=
    BCH.ext (val_powerScalar t (BCH.mk x))
  rw [← heq]
  exact powerScalar_mem H t hx

theorem mk_lie_mem (H : Subgroup (BCH (ZMod p) L hnil)) {x y : L}
    (hx : BCH.mk x ∈ H) (hy : BCH.mk y ∈ H) : BCH.mk ⁅x, y⁆ ∈ H := by
  have heq : bracketWord (BCH.mk x : BCH (ZMod p) L hnil) (BCH.mk y) = BCH.mk ⁅x, y⁆ :=
    BCH.ext (val_bracketWord (BCH.mk x) (BCH.mk y))
  rw [← heq]
  exact bracketWord_mem H hx hy

theorem mk_add_mem (H : Subgroup (BCH (ZMod p) L hnil)) {x y : L}
    (hx : BCH.mk x ∈ H) (hy : BCH.mk y ∈ H) : BCH.mk (x + y) ∈ H := by
  have heq : addWord (BCH.mk x : BCH (ZMod p) L hnil) (BCH.mk y) = BCH.mk (x + y) :=
    BCH.ext (val_addWord (BCH.mk x) (BCH.mk y))
  rw [← heq]
  exact addWord_mem H hx hy

/-- The logarithm of an arbitrary subgroup, with all Lie closure derived from
the group subgroup axioms. The prime-field hypotheses exclude 2, 3 and 5. -/
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) : LieSubalgebra (ZMod p) L where
  carrier := {x | BCH.mk x ∈ H}
  zero_mem' := H.one_mem
  add_mem' := mk_add_mem H
  smul_mem' t _ hx := mk_smul_mem H t hx
  lie_mem' := mk_lie_mem H

@[simp] theorem mem_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil)) (x : L) :
    x ∈ toLieSubalgebra hnil H ↔ BCH.mk x ∈ H := Iff.rfl

@[simp] theorem val_mem_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil))
    (x : BCH (ZMod p) L hnil) : x.val ∈ toLieSubalgebra hnil H ↔ x ∈ H := Iff.rfl

/-- The reverse construction uses only BCH closure of a Lie subalgebra. -/
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {x | x.val ∈ K}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    unfold bch
    have hxy := K.lie_mem hx hy
    have hyx := K.lie_mem hy hx
    exact K.add_mem (K.add_mem (K.sub_mem (K.sub_mem (K.add_mem (K.add_mem (K.add_mem hx hy)
      (K.smul_mem _ hxy)) (K.smul_mem _ (K.add_mem (K.lie_mem hx hxy) (K.lie_mem hy hyx))))
      (K.smul_mem _ (K.lie_mem hy (K.lie_mem hx hxy))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hy (K.lie_mem hy (K.lie_mem hy hyx)))
        (K.lie_mem hx (K.lie_mem hx (K.lie_mem hx hxy))))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hx (K.lie_mem hy (K.lie_mem hy hyx)))
        (K.lie_mem hy (K.lie_mem hx (K.lie_mem hx hxy))))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hy (K.lie_mem hx (K.lie_mem hy hxy)))
        (K.lie_mem hx (K.lie_mem hy (K.lie_mem hx hyx)))))

@[simp] theorem mem_toSubgroup (K : LieSubalgebra (ZMod p) L)
    (x : BCH (ZMod p) L hnil) : x ∈ toSubgroup hnil K ↔ x.val ∈ K := Iff.rfl

@[simp] theorem toLieSubalgebra_toSubgroup (K : LieSubalgebra (ZMod p) L) :
    toLieSubalgebra hnil (toSubgroup hnil K) = K := by
  ext x
  rfl

@[simp] theorem toSubgroup_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil)) :
    toSubgroup hnil (toLieSubalgebra hnil H) = H := by
  ext x
  rfl

end PrimeField

end
end QSearch.BCHClassFiveSubgroups

/-- info: 'QSearch.BCHClassFiveSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_comm

/-- info: 'QSearch.BCHClassFiveSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassFiveSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.val_addWord

/-- info: 'QSearch.BCHClassFiveSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassFiveSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassFiveSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassFiveSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassFiveSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFiveSubgroups.toSubgroup_toLieSubalgebra
