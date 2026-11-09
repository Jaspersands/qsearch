import Formal.BCHClassSix
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-six BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 5` (so every
`p > 6`). The words were designed with the exact rational model
`research/audits/reviews/2026-11-05-rees-lean-c6/words6.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of two
  degree-three, three degree-four, six degree-five and nine degree-six iterated
  commutators, has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-6 (one, two, three, six and nine of them) has logarithm exactly
  `x + y`.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`), no degree-five
rule, and three degree-six rules `two6a`-`two6c` (the twelve words `a·w`, `w` a
degree-five normal word, span a space of dimension nine).
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassSixSubgroups

open LieModule QSearch.BCHClassSix
open QSearch.BCHClassFour (jacobi4c)
open QSearch.BCHClassFive (smooth_ne_zero)

noncomputable section

section TwoLetterRules

variable {L : Type*} [LieRing L]

/-- A degree-six two-letter rule, from one `lie_skew` instance. -/
theorem two6a (a b : L) : ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ =
    ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ - ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have e0 := lie_skew (a : L) ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
    neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hba, jacobi4c a b] at e0
  linear_combination (norm := module) e0

/-- A degree-six two-letter rule, from one `lie_skew` instance. -/
theorem two6b (a b : L) : ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ =
    ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ - ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ - ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ - ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have e0 := lie_skew (a : L) ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
    neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hba, jacobi4c a b] at e0
  linear_combination (norm := module) e0

/-- A degree-six two-letter rule, from one `lie_skew` instance. -/
theorem two6c (a b : L) : ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ =
    ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ + ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ - ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have e0 := lie_skew (a : L) ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
    neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hba, jacobi4c a b] at e0
  linear_combination (norm := module) -e0

end TwoLetterRules

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

theorem ne1440 : (1440 : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) 5 2 1
  norm_num at this; exact this

end Numerals

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
theorem sext_central (hnil : lowerCentralSeries F L L 6 = ⊥) (a b c d e f g : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, g⁆⁆⁆⁆⁆⁆ = 0 :=
  classSix_of_lowerCentralSeries hnil a b c d e f g

/-- The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form. -/
def commPoly (a b : L) : L :=
  ⁅a, b⁆ + (1 / 2 : F) • ⁅a, ⁅a, b⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, b⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 4 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆ + (1 / 24 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 12 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 120 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 48 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 8 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 72 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 48 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 120 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x,y))`. -/
def p3x (a b : L) : L :=
  ⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (7 / 12 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-17 / 24 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 4 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 12 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x,y))`. -/
def p3y (a b : L) : L :=
  ⁅b, ⁅a, b⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 6 : F) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 4 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 24 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x,y)))`. -/
def p4xx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (3 / 2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + (5 / 4 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-5 / 4 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x,y)))`. -/
def p4yx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x,y)))`. -/
def p4yy (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, b⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x, C(x,y))))`. -/
def p5xxx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x, C(x,y))))`. -/
def p5yxx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + (3 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(x, C(x,y))))`. -/
def p5xyx (a b : L) : L :=
  ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x, C(x,y))))`. -/
def p5yyx (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(y, C(x,y))))`. -/
def p5xyy (a b : L) : L :=
  ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(y, C(x,y))))`. -/
def p5yyy (a b : L) : L :=
  ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆

set_option maxHeartbeats 0 in
/-- The commutator polynomial, derived from the sextic BCH law. -/
theorem bch_comm (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b) =
      commPoly (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(x,y))`. -/
theorem commPoly_left (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (commPoly (F := F) a b) =
      p3x (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(x,y))`. -/
theorem commPoly_right (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (commPoly (F := F) a b) =
      p3y (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(x, C(x,y)))`. -/
theorem commPoly_ll (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p3x (F := F) a b) =
      p4xx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(x,y)))`. -/
theorem commPoly_rl (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p3x (F := F) a b) =
      p4yx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(x,y)))`. -/
theorem commPoly_rr (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p3y (F := F) a b) =
      p4yy (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne10 (F := F), ne12 (F := F), ne16 (F := F), ne20 (F := F), ne24 (F := F), ne30 (F := F), ne36 (F := F), ne48 (F := F), ne60 (F := F), ne72 (F := F), ne120 (F := F), ne144 (F := F), ne180 (F := F), ne240 (F := F), ne360 (F := F), ne720 (F := F), ne1440 (F := F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(x, C(x, C(x,y))))`. -/
theorem commPoly_xxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p4xx (F := F) a b) =
      p5xxx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(x, C(x,y))))`. -/
theorem commPoly_yxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p4xx (F := F) a b) =
      p5yxx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(x, C(x,y))))`. -/
theorem commPoly_xyx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yx (F := F) a b) =
      p5xyx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(x, C(x,y))))`. -/
theorem commPoly_yyx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yx (F := F) a b) =
      p5yyx (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(y, C(x,y))))`. -/
theorem commPoly_xyy (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yy (F := F) a b) =
      p5xyy (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(y, C(x,y))))`. -/
theorem commPoly_yyy (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yy (F := F) a b) =
      p5yyy (F := F) a b := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_xxxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p5xxx (F := F) a b) =
      ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yxxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xxx (F := F) a b) =
      ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_xyxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p5yxx (F := F) a b) =
      ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yyxx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yxx (F := F) a b) =
      ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yxyx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xyx (F := F) a b) =
      ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_xyyx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) a (p5yyx (F := F) a b) =
      ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yyyx (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yyx (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yxyy (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xyy (F := F) a b) =
      ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-six commutator is its central bracket. -/
theorem commPoly_yyyy (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yyy (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ := by
  have hseven := sext_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] {hnil : lowerCentralSeries F L L 6 = ⊥}

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
    (comm y (comm x (comm x y))).val = p4yx (F := F) x.val y.val := by
  rw [val_comm, val_comm_left, commPoly_rl hnil]

theorem val_comm_rr (x y : BCH F L hnil) :
    (comm y (comm y (comm x y))).val = p4yy (F := F) x.val y.val := by
  rw [val_comm, val_comm_right, commPoly_rr hnil]

theorem val_comm_xxx (x y : BCH F L hnil) :
    (comm x (comm x (comm x (comm x y)))).val = p5xxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_ll, commPoly_xxx hnil]

theorem val_comm_yxx (x y : BCH F L hnil) :
    (comm y (comm x (comm x (comm x y)))).val = p5yxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_ll, commPoly_yxx hnil]

theorem val_comm_xyx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm x y)))).val = p5xyx (F := F) x.val y.val := by
  rw [val_comm, val_comm_rl, commPoly_xyx hnil]

theorem val_comm_yyx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm x y)))).val = p5yyx (F := F) x.val y.val := by
  rw [val_comm, val_comm_rl, commPoly_yyx hnil]

theorem val_comm_xyy (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm x y)))).val = p5xyy (F := F) x.val y.val := by
  rw [val_comm, val_comm_rr, commPoly_xyy hnil]

theorem val_comm_yyy (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm x y)))).val = p5yyy (F := F) x.val y.val := by
  rw [val_comm, val_comm_rr, commPoly_yyy hnil]

theorem val_comm_xxxx (x y : BCH F L hnil) :
    (comm x (comm x (comm x (comm x (comm x y))))).val = ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xxx, commPoly_xxxx hnil]

theorem val_comm_yxxx (x y : BCH F L hnil) :
    (comm y (comm x (comm x (comm x (comm x y))))).val = ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xxx, commPoly_yxxx hnil]

theorem val_comm_xyxx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm x (comm x y))))).val = ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxx, commPoly_xyxx hnil]

theorem val_comm_yyxx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm x (comm x y))))).val = ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxx, commPoly_yyxx hnil]

theorem val_comm_yxyx (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm x (comm x y))))).val = ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyx, commPoly_yxyx hnil]

theorem val_comm_xyyx (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm x (comm x y))))).val = ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyx, commPoly_xyyx hnil]

theorem val_comm_yyyx (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm x (comm x y))))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyx, commPoly_yyyx hnil]

theorem val_comm_yxyy (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm y (comm x y))))).val = ⁅y.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyy, commPoly_yxyy hnil]

theorem val_comm_yyyy (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm y (comm x y))))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyy, commPoly_yyyy hnil]

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
  {hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val

/-- Removing the degree-three, -four, -five and then the central degree-six
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
    powerScalar (-(1 / 4) : ZMod p) (comm y (comm y (comm y (comm x y)))) *
    powerScalar (1 / 5 : ZMod p) (comm x (comm x (comm x (comm x (comm x y))))) *
    powerScalar (9 / 8 : ZMod p) (comm y (comm x (comm x (comm x (comm x y))))) *
    powerScalar (-1 : ZMod p) (comm x (comm y (comm x (comm x (comm x y))))) *
    powerScalar (47 / 72 : ZMod p) (comm y (comm y (comm x (comm x (comm x y))))) *
    powerScalar (19 / 24 : ZMod p) (comm y (comm x (comm y (comm x (comm x y))))) *
    powerScalar (-(4 / 3) : ZMod p) (comm x (comm y (comm y (comm x (comm x y))))) *
    powerScalar (35 / 24 : ZMod p) (comm y (comm y (comm y (comm x (comm x y))))) *
    powerScalar (-(4 / 3) : ZMod p) (comm y (comm x (comm y (comm y (comm x y))))) *
    powerScalar (1 / 5 : ZMod p) (comm y (comm y (comm y (comm y (comm x y)))))

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, val_comm, val_comm_left, val_comm_right, val_comm_ll, val_comm_rl, val_comm_rr, val_comm_xxx, val_comm_yxx, val_comm_xyx, val_comm_yyx, val_comm_xyy, val_comm_yyy, val_comm_xxxx, val_comm_yxxx, val_comm_xyxx, val_comm_yyxx, val_comm_yxyx, val_comm_xyyx, val_comm_yyyx, val_comm_yxyy, val_comm_yyyy]
  have hseven := sext_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c x.val y.val, two6a x.val y.val, two6b x.val y.val, two6c x.val y.val]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne16 (F := ZMod p), ne20 (F := ZMod p), ne24 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne48 (F := ZMod p), ne60 (F := ZMod p), ne72 (F := ZMod p), ne120 (F := ZMod p), ne144 (F := ZMod p), ne180 (F := ZMod p), ne240 (F := ZMod p), ne360 (F := ZMod p), ne720 (F := ZMod p), ne1440 (F := ZMod p)])
  all_goals ring

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
  have m_c2 := comm_mem H hx hy
  have m_c3x := comm_mem H hx m_c2
  have m_c3y := comm_mem H hy m_c2
  have m_c4xx := comm_mem H hx m_c3x
  have m_c4yx := comm_mem H hy m_c3x
  have m_c4yy := comm_mem H hy m_c3y
  have m_c5xxx := comm_mem H hx m_c4xx
  have m_c5yxx := comm_mem H hy m_c4xx
  have m_c5xyx := comm_mem H hx m_c4yx
  have m_c5yyx := comm_mem H hy m_c4yx
  have m_c5xyy := comm_mem H hx m_c4yy
  have m_c5yyy := comm_mem H hy m_c4yy
  have m_c6xxxx := comm_mem H hx m_c5xxx
  have m_c6yxxx := comm_mem H hy m_c5xxx
  have m_c6xyxx := comm_mem H hx m_c5yxx
  have m_c6yyxx := comm_mem H hy m_c5yxx
  have m_c6yxyx := comm_mem H hy m_c5xyx
  have m_c6xyyx := comm_mem H hx m_c5yyx
  have m_c6yyyx := comm_mem H hy m_c5yyx
  have m_c6yxyy := comm_mem H hy m_c5xyy
  have m_c6yyyy := comm_mem H hy m_c5yyy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (m_c2)
    (powerScalar_mem H _ m_c3x))
    (powerScalar_mem H _ m_c3y))
    (powerScalar_mem H _ m_c4xx))
    (powerScalar_mem H _ m_c4yx))
    (powerScalar_mem H _ m_c4yy))
    (powerScalar_mem H _ m_c5xxx))
    (powerScalar_mem H _ m_c5yxx))
    (powerScalar_mem H _ m_c5xyx))
    (powerScalar_mem H _ m_c5yyx))
    (powerScalar_mem H _ m_c5xyy))
    (powerScalar_mem H _ m_c5yyy))
    (powerScalar_mem H _ m_c6xxxx))
    (powerScalar_mem H _ m_c6yxxx))
    (powerScalar_mem H _ m_c6xyxx))
    (powerScalar_mem H _ m_c6yyxx))
    (powerScalar_mem H _ m_c6yxyx))
    (powerScalar_mem H _ m_c6xyyx))
    (powerScalar_mem H _ m_c6yyyx))
    (powerScalar_mem H _ m_c6yxyy))
    (powerScalar_mem H _ m_c6yyyy)

/-- Addition is recovered by removing the bracket, then the degree-three to
central degree-six errors, each by a power of an exact bracket monomial. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x * y *
    powerScalar (-(1 / 2) : ZMod p) (bracketWord x y) *
    powerScalar (1 / 6 : ZMod p) (bracketWord x (bracketWord x y)) *
    powerScalar (1 / 3 : ZMod p) (bracketWord y (bracketWord x y)) *
    powerScalar (-(1 / 24) : ZMod p) (bracketWord x (bracketWord x (bracketWord x y))) *
    powerScalar (-(1 / 8) : ZMod p) (bracketWord y (bracketWord x (bracketWord x y))) *
    powerScalar (-(1 / 8) : ZMod p) (bracketWord y (bracketWord y (bracketWord x y))) *
    powerScalar (1 / 120 : ZMod p) (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))) *
    powerScalar (1 / 20 : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord x y)))) *
    powerScalar (1 / 10 : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord x y)))) *
    powerScalar (-(1 / 60) : ZMod p) (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))) *
    powerScalar (-(1 / 20) : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))) *
    powerScalar (1 / 30 : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord x y)))) *
    powerScalar (-(1 / 720) : ZMod p) (bracketWord x (bracketWord x (bracketWord x (bracketWord x (bracketWord x y))))) *
    powerScalar (-(1 / 72) : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord x (bracketWord x y))))) *
    powerScalar (-(5 / 72) : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord x (bracketWord x y))))) *
    powerScalar (1 / 144 : ZMod p) (bracketWord y (bracketWord x (bracketWord x (bracketWord x (bracketWord x y))))) *
    powerScalar (7 / 72 : ZMod p) (bracketWord y (bracketWord x (bracketWord y (bracketWord x (bracketWord x y))))) *
    powerScalar (-(1 / 24) : ZMod p) (bracketWord y (bracketWord x (bracketWord y (bracketWord y (bracketWord x y))))) *
    powerScalar (-(1 / 24) : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord x (bracketWord x y))))) *
    powerScalar (1 / 36 : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord x (bracketWord x y))))) *
    powerScalar (-(1 / 144) : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord x y)))))

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
  have hseven := sext_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c x.val y.val, two6a x.val y.val, two6b x.val y.val, two6c x.val y.val]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne16 (F := ZMod p), ne20 (F := ZMod p), ne24 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne48 (F := ZMod p), ne60 (F := ZMod p), ne72 (F := ZMod p), ne120 (F := ZMod p), ne144 (F := ZMod p), ne180 (F := ZMod p), ne240 (F := ZMod p), ne360 (F := ZMod p), ne720 (F := ZMod p), ne1440 (F := ZMod p)])
  all_goals ring

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
  have b_xy := bracketWord_mem H hx hy
  have b_xxy := bracketWord_mem H hx b_xy
  have b_yxy := bracketWord_mem H hy b_xy
  have b_xxxy := bracketWord_mem H hx b_xxy
  have b_yxxy := bracketWord_mem H hy b_xxy
  have b_yyxy := bracketWord_mem H hy b_yxy
  have b_xxxxy := bracketWord_mem H hx b_xxxy
  have b_xyxxy := bracketWord_mem H hx b_yxxy
  have b_xyyxy := bracketWord_mem H hx b_yyxy
  have b_yxxxy := bracketWord_mem H hy b_xxxy
  have b_yyxxy := bracketWord_mem H hy b_yxxy
  have b_yyyxy := bracketWord_mem H hy b_yyxy
  have b_xxxxxy := bracketWord_mem H hx b_xxxxy
  have b_xyxxxy := bracketWord_mem H hx b_yxxxy
  have b_xyyxxy := bracketWord_mem H hx b_yyxxy
  have b_yxxxxy := bracketWord_mem H hy b_xxxxy
  have b_yxyxxy := bracketWord_mem H hy b_xyxxy
  have b_yxyyxy := bracketWord_mem H hy b_xyyxy
  have b_yyxxxy := bracketWord_mem H hy b_yxxxy
  have b_yyyxxy := bracketWord_mem H hy b_yyxxy
  have b_yyyyxy := bracketWord_mem H hy b_yyyxy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem hx hy)
    (powerScalar_mem H _ b_xy))
    (powerScalar_mem H _ b_xxy))
    (powerScalar_mem H _ b_yxy))
    (powerScalar_mem H _ b_xxxy))
    (powerScalar_mem H _ b_yxxy))
    (powerScalar_mem H _ b_yyxy))
    (powerScalar_mem H _ b_xxxxy))
    (powerScalar_mem H _ b_xyxxy))
    (powerScalar_mem H _ b_xyyxy))
    (powerScalar_mem H _ b_yxxxy))
    (powerScalar_mem H _ b_yyxxy))
    (powerScalar_mem H _ b_yyyxy))
    (powerScalar_mem H _ b_xxxxxy))
    (powerScalar_mem H _ b_xyxxxy))
    (powerScalar_mem H _ b_xyyxxy))
    (powerScalar_mem H _ b_yxxxxy))
    (powerScalar_mem H _ b_yxyxxy))
    (powerScalar_mem H _ b_yxyyxy))
    (powerScalar_mem H _ b_yyxxxy))
    (powerScalar_mem H _ b_yyyxxy))
    (powerScalar_mem H _ b_yyyyxy)

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
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥)
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
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {x | x.val ∈ K}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    unfold bch
    repeat' first
      | exact hx | exact hy
      | apply K.add_mem | apply K.sub_mem | apply K.smul_mem | apply K.lie_mem

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
end QSearch.BCHClassSixSubgroups

/-- info: 'QSearch.BCHClassSixSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_comm

/-- info: 'QSearch.BCHClassSixSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassSixSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.val_addWord

/-- info: 'QSearch.BCHClassSixSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassSixSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassSixSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassSixSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassSixSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSixSubgroups.toSubgroup_toLieSubalgebra
