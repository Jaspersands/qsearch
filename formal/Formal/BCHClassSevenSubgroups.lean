import Formal.BCHClassSeven
import Formal.BCHClassSixSubgroups
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-seven BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 7` (so every
prime `p ≥ 11`). The words were designed with the exact rational model
`research/audits/reviews/2026-11-05-rees-lean-c7/words7.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of two
  degree-three, three degree-four, six degree-five, nine degree-six and eighteen
  central degree-seven iterated commutators, has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-7 (one, two, three, six, nine and eighteen of them) has logarithm
  exactly `x + y`.

Both values are computed in stages: `bwStage k` and `awStage k` are the exact
logarithms after the first `k` correction factors, and one lemma per factor
(`bwStep_k`, `awStep_k`) passes from one stage to the next. Each stage is a
polynomial in normal form, so no single proof expands more than one product.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`), no degree-five
rule, the three degree-six rules `two6a`-`two6c` of `BCHClassSixSubgroups`, and
no degree-seven rule (the eighteen words `a·w`, `w` a degree-six normal word,
are independent).
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassSevenSubgroups

open LieModule QSearch.BCHClassSeven
open QSearch.BCHClassFour (jacobi4c)
open QSearch.BCHClassSixSubgroups (two6a two6b two6c)

noncomputable section

section Numerals

variable {F : Type*} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]
  [NeZero (7 : F)]

theorem ne4 : (4 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 0 0 0
  norm_num at this; exact this

theorem ne6 : (6 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 1 0 0
  norm_num at this; exact this

theorem ne8 : (8 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 0 0 0
  norm_num at this; exact this

theorem ne9 : (9 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 2 0 0
  norm_num at this; exact this

theorem ne10 : (10 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 0 1 0
  norm_num at this; exact this

theorem ne12 : (12 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 1 0 0
  norm_num at this; exact this

theorem ne15 : (15 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 1 1 0
  norm_num at this; exact this

theorem ne16 : (16 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 0 0 0
  norm_num at this; exact this

theorem ne18 : (18 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 2 0 0
  norm_num at this; exact this

theorem ne20 : (20 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 0 1 0
  norm_num at this; exact this

theorem ne21 : (21 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 1 0 1
  norm_num at this; exact this

theorem ne24 : (24 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 1 0 0
  norm_num at this; exact this

theorem ne28 : (28 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 0 0 1
  norm_num at this; exact this

theorem ne30 : (30 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 1 1 0
  norm_num at this; exact this

theorem ne36 : (36 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 2 0 0
  norm_num at this; exact this

theorem ne45 : (45 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 2 1 0
  norm_num at this; exact this

theorem ne48 : (48 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 1 0 0
  norm_num at this; exact this

theorem ne56 : (56 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 0 0 1
  norm_num at this; exact this

theorem ne60 : (60 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 1 1 0
  norm_num at this; exact this

theorem ne63 : (63 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 2 0 1
  norm_num at this; exact this

theorem ne72 : (72 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 2 0 0
  norm_num at this; exact this

theorem ne80 : (80 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 0 1 0
  norm_num at this; exact this

theorem ne84 : (84 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 1 0 1
  norm_num at this; exact this

theorem ne90 : (90 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 2 1 0
  norm_num at this; exact this

theorem ne96 : (96 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 1 0 0
  norm_num at this; exact this

theorem ne105 : (105 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 1 1 1
  norm_num at this; exact this

theorem ne112 : (112 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 0 0 1
  norm_num at this; exact this

theorem ne120 : (120 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 1 1 0
  norm_num at this; exact this

theorem ne126 : (126 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 2 0 1
  norm_num at this; exact this

theorem ne144 : (144 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 2 0 0
  norm_num at this; exact this

theorem ne168 : (168 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 1 0 1
  norm_num at this; exact this

theorem ne180 : (180 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 2 1 0
  norm_num at this; exact this

theorem ne224 : (224 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 0 0 1
  norm_num at this; exact this

theorem ne240 : (240 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 1 1 0
  norm_num at this; exact this

theorem ne252 : (252 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 2 0 1
  norm_num at this; exact this

theorem ne280 : (280 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 0 1 1
  norm_num at this; exact this

theorem ne288 : (288 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 2 0 0
  norm_num at this; exact this

theorem ne315 : (315 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 2 1 1
  norm_num at this; exact this

theorem ne336 : (336 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 1 0 1
  norm_num at this; exact this

theorem ne360 : (360 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 2 1 0
  norm_num at this; exact this

theorem ne378 : (378 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 3 0 1
  norm_num at this; exact this

theorem ne504 : (504 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 2 0 1
  norm_num at this; exact this

theorem ne630 : (630 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 2 1 1
  norm_num at this; exact this

theorem ne672 : (672 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 1 0 1
  norm_num at this; exact this

theorem ne720 : (720 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 2 1 0
  norm_num at this; exact this

theorem ne756 : (756 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 3 0 1
  norm_num at this; exact this

theorem ne840 : (840 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 1 1 1
  norm_num at this; exact this

theorem ne945 : (945 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 0 3 1 1
  norm_num at this; exact this

theorem ne1008 : (1008 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 2 0 1
  norm_num at this; exact this

theorem ne1120 : (1120 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 0 1 1
  norm_num at this; exact this

theorem ne1260 : (1260 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 2 1 1
  norm_num at this; exact this

theorem ne1440 : (1440 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 2 1 0
  norm_num at this; exact this

theorem ne1890 : (1890 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 1 3 1 1
  norm_num at this; exact this

theorem ne2016 : (2016 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 2 0 1
  norm_num at this; exact this

theorem ne2520 : (2520 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 2 1 1
  norm_num at this; exact this

theorem ne3360 : (3360 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 1 1 1
  norm_num at this; exact this

theorem ne3780 : (3780 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 2 3 1 1
  norm_num at this; exact this

theorem ne5040 : (5040 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 2 1 1
  norm_num at this; exact this

theorem ne7560 : (7560 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 3 3 1 1
  norm_num at this; exact this

theorem ne10080 : (10080 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 2 1 1
  norm_num at this; exact this

theorem ne15120 : (15120 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 4 3 1 1
  norm_num at this; exact this

theorem ne30240 : (30240 : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) 5 3 1 1
  norm_num at this; exact this

end Numerals

section SepticPart

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket (coefficient one) added to its first argument. -/
theorem z7_peel_left1 (h : ClassSeven L) (u v p q : L) :
    z7 (F := F) (u + ⁅p, q⁆) v = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

set_option linter.unusedSimpArgs false in
/-- `z7` vanishes when its second argument is a multiple of a bracket. -/
theorem z7_bracket_right (h : ClassSeven L) (u p q : L) (t : F) :
    z7 (F := F) u (t • ⁅p, q⁆) = 0 := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, lie_smul, height, smul_zero, add_zero, sub_zero, sub_self, neg_zero]

/-- `z7 b (-b) = 0`. -/
theorem z7_self_neg (b : L) : z7 (F := F) b (-b) = 0 := by
  simp [z7]

end SepticPart

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
theorem oct_central (hnil : lowerCentralSeries F L L 7 = ⊥) (a b c d e f g k : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
  classSeven_of_lowerCentralSeries hnil a b c d e f g k

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
    + (1 / 720 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 48 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 36 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 240 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 240 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 16 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 36 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 720 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

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
    + (31 / 360 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : F) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 12 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 18 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 12 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 120 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 6 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 6 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

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
    + (1 / 8 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 6 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 120 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 8 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (2 / 9 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 360 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x,y)))`. -/
def p4xx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (3 / 2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + (5 / 4 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-5 / 4 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 4 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 12 : F) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 4 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-55 / 24 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x,y)))`. -/
def p4yx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 12 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 6 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x,y)))`. -/
def p4yy (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, b⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 4 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 3 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 24 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 4 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x, C(x,y))))`. -/
def p5xxx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (13 / 6 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x, C(x,y))))`. -/
def p5yxx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆ + (3 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 4 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(x, C(x,y))))`. -/
def p5xyx (a b : L) : L :=
  ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (-1 / 2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 6 : F) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x, C(x,y))))`. -/
def p5yyx (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (7 / 12 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 12 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(y, C(x,y))))`. -/
def p5xyy (a b : L) : L :=
  ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 4 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (2 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 4 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(y, C(x,y))))`. -/
def p5yyy (a b : L) : L :=
  ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 6 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(x, C(x, C(x, C(x,y)))))`. -/
def p6xxxx (a b : L) : L :=
  ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (5 / 2 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(x, C(x, C(x,y)))))`. -/
def p6yxxx (a b : L) : L :=
  ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (2 : F) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(x, C(x, C(x,y)))))`. -/
def p6xyxx (a b : L) : L :=
  ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (1 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(x, C(x, C(x,y)))))`. -/
def p6yyxx (a b : L) : L :=
  ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (3 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(y, C(x, C(x,y)))))`. -/
def p6yxyx (a b : L) : L :=
  ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (2 : F) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(x, C(y, C(y, C(x, C(x,y)))))`. -/
def p6xyyx (a b : L) : L :=
  ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (1 / 2 : F) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 2 : F) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(y, C(x, C(x,y)))))`. -/
def p6yyyx (a b : L) : L :=
  ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(x, C(y, C(y, C(x,y)))))`. -/
def p6yxyy (a b : L) : L :=
  ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ + (2 : F) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 2 : F) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `C(y, C(y, C(y, C(y, C(x,y)))))`. -/
def p6yyyy (a b : L) : L :=
  ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆ + (1 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 2 : F) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `x y x⁻¹`, in normal form. -/
def commStage1 (a b : L) : L :=
  b + ⁅a, b⁆ + (1 / 2 : F) • ⁅a, ⁅a, b⁆⁆ + (1 / 6 : F) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆
    + (1 / 24 : F) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 120 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 720 : F) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆

set_option maxHeartbeats 0 in
/-- The septic law at `(x y, x⁻¹)`, after removing the central parts. -/
theorem commStage1_eq (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) a b) (-a) + z7 (F := F) a b + z7 (F := F) (a + b) (-a) =
      commStage1 (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [QSearch.BCHClassSix.bch, z7, commStage1, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- The sextic law at `(x y x⁻¹, y⁻¹)`. -/
theorem commStage1_comm (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    QSearch.BCHClassSix.bch (F := F) (commStage1 (F := F) a b) (-b) =
      commPoly (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [QSearch.BCHClassSix.bch, commStage1, commPoly, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

/-- The commutator polynomial, derived from the septic BCH law. -/
theorem bch_comm (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b) =
      commPoly (F := F) a b := by
  have h := classSeven_of_lowerCentralSeries hnil
  have z1 : z7 (F := F) (bch (F := F) a b) (-a) = z7 (F := F) (a + b) (-a) := by
    rw [bch_shape a b]
    simp only [z7_peel_left h]
  have b1 : QSearch.BCHClassSix.bch (F := F) (bch (F := F) a b) (-a) = QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) a b) (-a) + z7 (F := F) a b := by
    rw [bch_eq_six_add a b, six_central_left _ _ _ (fun w => z7_central h a b w)]
  have z2 : z7 (F := F) (commStage1 (F := F) a b) (-b) = 0 := by
    unfold commStage1
    simp only [z7_peel_left h, z7_peel_left1 h, z7_self_neg]
  rw [bch_eq_six_add (bch (F := F) a b) (-a), z1, b1, commStage1_eq hnil,
    bch_eq_six_add (commStage1 (F := F) a b) (-b), z2, add_zero, commStage1_comm hnil]

set_option maxHeartbeats 0 in
/-- `C(x, C(x,y))`. -/
theorem commPoly_left (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (commPoly (F := F) a b) =
      p3x (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(x,y))`. -/
theorem commPoly_right (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (commPoly (F := F) a b) =
      p3y (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(x, C(x,y)))`. -/
theorem commPoly_ll (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p3x (F := F) a b) =
      p4xx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(x,y)))`. -/
theorem commPoly_rl (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p3x (F := F) a b) =
      p4yx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(x,y)))`. -/
theorem commPoly_rr (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p3y (F := F) a b) =
      p4yy (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(x, C(x, C(x,y))))`. -/
theorem commPoly_xxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p4xx (F := F) a b) =
      p5xxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(x, C(x,y))))`. -/
theorem commPoly_yxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p4xx (F := F) a b) =
      p5yxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(x, C(x,y))))`. -/
theorem commPoly_xyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yx (F := F) a b) =
      p5xyx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(x, C(x,y))))`. -/
theorem commPoly_yyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yx (F := F) a b) =
      p5yyx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(y, C(x,y))))`. -/
theorem commPoly_xyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p4yy (F := F) a b) =
      p5xyy (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(y, C(x,y))))`. -/
theorem commPoly_yyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p4yy (F := F) a b) =
      p5yyy (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), NeZero.ne (5 : F), NeZero.ne (7 : F), ne4 (F := F), ne6 (F := F), ne8 (F := F), ne9 (F := F), ne10 (F := F), ne12 (F := F), ne15 (F := F), ne16 (F := F), ne18 (F := F), ne20 (F := F), ne21 (F := F), ne24 (F := F), ne28 (F := F), ne30 (F := F), ne36 (F := F), ne45 (F := F), ne48 (F := F), ne56 (F := F), ne60 (F := F), ne63 (F := F), ne72 (F := F), ne80 (F := F), ne84 (F := F), ne90 (F := F), ne96 (F := F), ne105 (F := F), ne112 (F := F), ne120 (F := F), ne126 (F := F), ne144 (F := F), ne168 (F := F), ne180 (F := F), ne224 (F := F), ne240 (F := F), ne252 (F := F), ne280 (F := F), ne288 (F := F), ne315 (F := F), ne336 (F := F), ne360 (F := F), ne378 (F := F), ne504 (F := F), ne630 (F := F), ne672 (F := F), ne720 (F := F), ne756 (F := F), ne840 (F := F), ne945 (F := F), ne1008 (F := F), ne1120 (F := F), ne1260 (F := F), ne1440 (F := F), ne1890 (F := F), ne2016 (F := F), ne2520 (F := F), ne3360 (F := F), ne3780 (F := F), ne5040 (F := F), ne7560 (F := F), ne10080 (F := F), ne15120 (F := F), ne30240 (F := F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(x, C(x, C(x, C(x,y)))))`. -/
theorem commPoly_xxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p5xxx (F := F) a b) =
      p6xxxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(x, C(x, C(x,y)))))`. -/
theorem commPoly_yxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xxx (F := F) a b) =
      p6yxxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(x, C(x, C(x,y)))))`. -/
theorem commPoly_xyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p5yxx (F := F) a b) =
      p6xyxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F)])

omit [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(x, C(x, C(x,y)))))`. -/
theorem commPoly_yyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yxx (F := F) a b) =
      p6yyxx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F)])
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(y, C(x, C(x,y)))))`. -/
theorem commPoly_yxyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xyx (F := F) a b) =
      p6yxyx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(x, C(y, C(y, C(x, C(x,y)))))`. -/
theorem commPoly_xyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p5yyx (F := F) a b) =
      p6xyyx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F)])

omit [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(y, C(x, C(x,y)))))`. -/
theorem commPoly_yyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yyx (F := F) a b) =
      p6yyyx (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(x, C(y, C(y, C(x,y)))))`. -/
theorem commPoly_yxyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5xyy (F := F) a b) =
      p6yxyy (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F)])
  all_goals ring

omit [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- `C(y, C(y, C(y, C(y, C(x,y)))))`. -/
theorem commPoly_yyyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p5yyy (F := F) a b) =
      p6yyyy (F := F) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : F)])
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xxxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6xxxx (F := F) a b) =
      ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yxxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6xxxx (F := F) a b) =
      ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yxxx (F := F) a b) =
      ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyxxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yxxx (F := F) a b) =
      ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xxyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6xyxx (F := F) a b) =
      ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yxyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6xyxx (F := F) a b) =
      ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yyxx (F := F) a b) =
      ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyyxx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yyxx (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyxyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yxyx (F := F) a b) =
      ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyxyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yxyx (F := F) a b) =
      ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xxyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6xyyx (F := F) a b) =
      ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yxyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6xyyx (F := F) a b) =
      ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yyyx (F := F) a b) =
      ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyyyx (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yyyx (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyxyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yxyy (F := F) a b) =
      ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyxyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yxyy (F := F) a b) =
      ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_xyyyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) a (p6yyyy (F := F) a b) =
      ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
set_option maxHeartbeats 0 in
/-- A degree-seven commutator is its central bracket. -/
theorem commPoly_yyyyy (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    commPoly (F := F) b (p6yyyy (F := F) a b) =
      ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, p3x, p3y, p4xx, p4yx, p4yy, p5xxx, p5yxx, p5xyx, p5yyx, p5xyy, p5yyy, p6xxxx, p6yxxx, p6xyxx, p6yyxx, p6yxyx, p6xyyx, p6yyyx, p6yxyy, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]

end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]
  {hnil : lowerCentralSeries F L L 7 = ⊥}

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
    (comm x (comm x (comm x (comm x (comm x y))))).val = p6xxxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_xxx, commPoly_xxxx hnil]

theorem val_comm_yxxx (x y : BCH F L hnil) :
    (comm y (comm x (comm x (comm x (comm x y))))).val = p6yxxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_xxx, commPoly_yxxx hnil]

theorem val_comm_xyxx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm x (comm x y))))).val = p6xyxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_yxx, commPoly_xyxx hnil]

theorem val_comm_yyxx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm x (comm x y))))).val = p6yyxx (F := F) x.val y.val := by
  rw [val_comm, val_comm_yxx, commPoly_yyxx hnil]

theorem val_comm_yxyx (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm x (comm x y))))).val = p6yxyx (F := F) x.val y.val := by
  rw [val_comm, val_comm_xyx, commPoly_yxyx hnil]

theorem val_comm_xyyx (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm x (comm x y))))).val = p6xyyx (F := F) x.val y.val := by
  rw [val_comm, val_comm_yyx, commPoly_xyyx hnil]

theorem val_comm_yyyx (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm x (comm x y))))).val = p6yyyx (F := F) x.val y.val := by
  rw [val_comm, val_comm_yyx, commPoly_yyyx hnil]

theorem val_comm_yxyy (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm y (comm x y))))).val = p6yxyy (F := F) x.val y.val := by
  rw [val_comm, val_comm_xyy, commPoly_yxyy hnil]

theorem val_comm_yyyy (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm y (comm x y))))).val = p6yyyy (F := F) x.val y.val := by
  rw [val_comm, val_comm_yyy, commPoly_yyyy hnil]

theorem val_comm_xxxxx (x y : BCH F L hnil) :
    (comm x (comm x (comm x (comm x (comm x (comm x y)))))).val = ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xxxx, commPoly_xxxxx hnil]

theorem val_comm_yxxxx (x y : BCH F L hnil) :
    (comm y (comm x (comm x (comm x (comm x (comm x y)))))).val = ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xxxx, commPoly_yxxxx hnil]

theorem val_comm_xyxxx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm x (comm x (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxxx, commPoly_xyxxx hnil]

theorem val_comm_yyxxx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm x (comm x (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxxx, commPoly_yyxxx hnil]

theorem val_comm_xxyxx (x y : BCH F L hnil) :
    (comm x (comm x (comm y (comm x (comm x (comm x y)))))).val = ⁅x.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyxx, commPoly_xxyxx hnil]

theorem val_comm_yxyxx (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm x (comm x (comm x y)))))).val = ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyxx, commPoly_yxyxx hnil]

theorem val_comm_xyyxx (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm x (comm x (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyxx, commPoly_xyyxx hnil]

theorem val_comm_yyyxx (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm x (comm x (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyxx, commPoly_yyyxx hnil]

theorem val_comm_xyxyx (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm y (comm x (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxyx, commPoly_xyxyx hnil]

theorem val_comm_yyxyx (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm y (comm x (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxyx, commPoly_yyxyx hnil]

theorem val_comm_xxyyx (x y : BCH F L hnil) :
    (comm x (comm x (comm y (comm y (comm x (comm x y)))))).val = ⁅x.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyyx, commPoly_xxyyx hnil]

theorem val_comm_yxyyx (x y : BCH F L hnil) :
    (comm y (comm x (comm y (comm y (comm x (comm x y)))))).val = ⁅y.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_xyyx, commPoly_yxyyx hnil]

theorem val_comm_xyyyx (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm y (comm x (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyyx, commPoly_xyyyx hnil]

theorem val_comm_yyyyx (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm y (comm x (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyyx, commPoly_yyyyx hnil]

theorem val_comm_xyxyy (x y : BCH F L hnil) :
    (comm x (comm y (comm x (comm y (comm y (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxyy, commPoly_xyxyy hnil]

theorem val_comm_yyxyy (x y : BCH F L hnil) :
    (comm y (comm y (comm x (comm y (comm y (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅x.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yxyy, commPoly_yyxyy hnil]

theorem val_comm_xyyyy (x y : BCH F L hnil) :
    (comm x (comm y (comm y (comm y (comm y (comm x y)))))).val = ⁅x.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyyy, commPoly_xyyyy hnil]

theorem val_comm_yyyyy (x y : BCH F L hnil) :
    (comm y (comm y (comm y (comm y (comm y (comm x y)))))).val = ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆⁆⁆⁆ := by
  rw [val_comm, val_comm_yyyy, commPoly_yyyyy hnil]

end Words

/-- Install with `letI := neZeroTwo hp` when the characteristic bound is explicit. -/
theorem neZeroTwo {p : ℕ} (hp : 7 < p) : NeZero (2 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 2 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroThree hp` when the characteristic bound is explicit. -/
theorem neZeroThree {p : ℕ} (hp : 7 < p) : NeZero (3 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 3 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroFive hp` when the characteristic bound is explicit. -/
theorem neZeroFive {p : ℕ} (hp : 7 < p) : NeZero (5 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 5 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroSeven hp` when the characteristic bound is explicit. -/
theorem neZeroSeven {p : ℕ} (hp : 7 < p) : NeZero (7 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 7 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) hp)⟩

section StageValues

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]

/-- The logarithm of `bracketWord` after its first 1 correction factor(s). -/
def bwStage1 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 2 : ZMod p) • ⁅b, ⁅a, b⁆⁆ + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-3 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (17 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 120 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 8 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 240 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 2 correction factor(s). -/
def bwStage2 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (-1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-3 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-13 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (29 / 48 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-13 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (19 / 48 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 60 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 8 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 3 correction factor(s). -/
def bwStage3 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-3 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 48 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-13 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (19 / 48 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 60 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 9 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-65 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 12 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 4 correction factor(s). -/
def bwStage4 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 4 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 60 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 9 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-65 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 36 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 5 correction factor(s). -/
def bwStage5 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 4 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 4 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (2 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 9 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-65 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 9 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 9 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 6 correction factor(s). -/
def bwStage6 (a b : L) : L :=
  ⁅a, b⁆ + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 4 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (2 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 72 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 9 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 48 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 9 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 7 correction factor(s). -/
def bwStage7 (a b : L) : L :=
  ⁅a, b⁆ + (-7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (2 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-5 / 6 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-17 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 72 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 9 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 9 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 8 correction factor(s). -/
def bwStage8 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (2 / 3 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-9 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-17 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 16 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (53 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 36 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 9 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 9 correction factor(s). -/
def bwStage9 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 2 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-9 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 6 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-65 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-65 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 10 correction factor(s). -/
def bwStage10 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-9 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-47 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-4 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (3 / 10 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 4 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 11 correction factor(s). -/
def bwStage11 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 5 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-9 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-47 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 12 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 12 correction factor(s). -/
def bwStage12 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-9 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-47 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 8 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 13 correction factor(s). -/
def bwStage13 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆ + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-47 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-7 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 14 correction factor(s). -/
def bwStage14 (a b : L) : L :=
  ⁅a, b⁆ + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-47 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-29 / 48 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 15 correction factor(s). -/
def bwStage15 (a b : L) : L :=
  ⁅a, b⁆ + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-19 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 4 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 18 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 16 correction factor(s). -/
def bwStage16 (a b : L) : L :=
  ⁅a, b⁆ + (4 / 3 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (35 / 48 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 17 correction factor(s). -/
def bwStage17 (a b : L) : L :=
  ⁅a, b⁆ + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-35 / 24 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 12 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 18 correction factor(s). -/
def bwStage18 (a b : L) : L :=
  ⁅a, b⁆ + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (3 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 19 correction factor(s). -/
def bwStage19 (a b : L) : L :=
  ⁅a, b⁆ + (-1 / 5 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 20 correction factor(s). -/
def bwStage20 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 6 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 21 correction factor(s). -/
def bwStage21 (a b : L) : L :=
  ⁅a, b⁆ + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (37 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 22 correction factor(s). -/
def bwStage22 (a b : L) : L :=
  ⁅a, b⁆ + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 23 correction factor(s). -/
def bwStage23 (a b : L) : L :=
  ⁅a, b⁆ + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (9 / 16 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 24 correction factor(s). -/
def bwStage24 (a b : L) : L :=
  ⁅a, b⁆ + (7 / 60 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 25 correction factor(s). -/
def bwStage25 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (4 / 3 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 26 correction factor(s). -/
def bwStage26 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 27 correction factor(s). -/
def bwStage27 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 18 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 28 correction factor(s). -/
def bwStage28 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 29 correction factor(s). -/
def bwStage29 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (305 / 144 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 30 correction factor(s). -/
def bwStage30 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 16 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 31 correction factor(s). -/
def bwStage31 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 32 correction factor(s). -/
def bwStage32 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 33 correction factor(s). -/
def bwStage33 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (59 / 15 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 34 correction factor(s). -/
def bwStage34 (a b : L) : L :=
  ⁅a, b⁆ + ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 35 correction factor(s). -/
def bwStage35 (a b : L) : L :=
  ⁅a, b⁆ + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 36 correction factor(s). -/
def bwStage36 (a b : L) : L :=
  ⁅a, b⁆ + (11 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `bracketWord` after its first 37 correction factor(s). -/
def bwStage37 (a b : L) : L :=
  ⁅a, b⁆ + (1 / 6 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 1 correction factor(s). -/
def awStage1 (a b : L) : L :=
  a + b + (-1 / 6 : ZMod p) • ⁅a, ⁅a, b⁆⁆ + (-1 / 3 : ZMod p) • ⁅b, ⁅a, b⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (-1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (-1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-7 / 240 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-47 / 720 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (17 / 720 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (17 / 240 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 288 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 16 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 96 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 30240 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-2 / 315 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 5040 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (73 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 105 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (101 / 30240 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (41 / 2520 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 1260 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 3360 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 280 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-2 / 105 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-23 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (8 / 945 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 30240 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 2 correction factor(s). -/
def awStage2 (a b : L) : L :=
  a + b + (-1 / 3 : ZMod p) • ⁅b, ⁅a, b⁆⁆ + (1 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + (-1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 80 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-11 / 720 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-47 / 720 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 80 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (61 / 720 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 288 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 96 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-23 / 7560 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 7560 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 3780 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-209 / 15120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 105 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (187 / 15120 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 756 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-61 / 15120 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 2520 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 1890 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-173 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-23 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (247 / 15120 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 378 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 30240 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 3 correction factor(s). -/
def awStage3 (a b : L) : L :=
  a + b + (1 / 24 : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆
    + (1 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (1 / 80 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 80 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-3 / 80 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (3 / 80 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (9 / 80 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 240 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 288 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 96 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 504 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 4 correction factor(s). -/
def awStage4 (a b : L) : L :=
  a + b + (1 / 8 : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + (1 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (-1 / 120 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 80 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-3 / 80 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (9 / 80 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 240 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 360 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 288 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 96 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 96 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 504 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 5 correction factor(s). -/
def awStage5 (a b : L) : L :=
  a + b + (1 / 8 : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆
    + (-1 / 120 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 20 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-3 / 80 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (7 / 240 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 360 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 288 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 288 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 96 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 96 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 288 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 1440 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 504 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 6 correction factor(s). -/
def awStage6 (a b : L) : L :=
  a + b + (-1 / 120 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 20 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 10 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (-1 / 360 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 18 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 36 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 504 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 7 correction factor(s). -/
def awStage7 (a b : L) : L :=
  a + b + (-1 / 20 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 10 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 18 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (13 / 720 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 36 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 3360 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 3360 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 504 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 8 correction factor(s). -/
def awStage8 (a b : L) : L :=
  a + b + (-1 / 10 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 45 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 18 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (19 / 360 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 2520 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1260 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-53 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 63 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-89 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-41 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 63 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 9 correction factor(s). -/
def awStage9 (a b : L) : L :=
  a + b + (1 / 60 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 45 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (17 / 180 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 120 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 2520 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 630 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 5040 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (137 / 5040 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-53 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 2520 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-163 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (61 / 2520 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 10 correction factor(s). -/
def awStage10 (a b : L) : L :=
  a + b + (1 / 20 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆
    + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (17 / 180 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 120 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (17 / 630 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 5040 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (29 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 2520 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-163 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 11 correction factor(s). -/
def awStage11 (a b : L) : L :=
  a + b + (-1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆
    + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 120 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 90 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 720 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-13 / 5040 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 1260 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (127 / 10080 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-163 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (109 / 5040 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 2016 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 12 correction factor(s). -/
def awStage12 (a b : L) : L :=
  a + b + (1 / 720 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 2016 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 672 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 13 correction factor(s). -/
def awStage13 (a b : L) : L :=
  a + b + (1 / 72 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (5 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 14 correction factor(s). -/
def awStage14 (a b : L) : L :=
  a + b + (5 / 72 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 15 correction factor(s). -/
def awStage15 (a b : L) : L :=
  a + b + (-1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 672 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 224 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 16 correction factor(s). -/
def awStage16 (a b : L) : L :=
  a + b + (-7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-17 / 504 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-43 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 17 correction factor(s). -/
def awStage17 (a b : L) : L :=
  a + b + (1 / 24 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-3 / 112 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 18 correction factor(s). -/
def awStage18 (a b : L) : L :=
  a + b + (1 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (13 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 19 correction factor(s). -/
def awStage19 (a b : L) : L :=
  a + b + (-1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆
    + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 504 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (19 / 1008 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 20 correction factor(s). -/
def awStage20 (a b : L) : L :=
  a + b + (1 / 144 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆
    + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (31 / 2016 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (23 / 10080 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 21 correction factor(s). -/
def awStage21 (a b : L) : L :=
  a + b + (-1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 22 correction factor(s). -/
def awStage22 (a b : L) : L :=
  a + b + (-1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 23 correction factor(s). -/
def awStage23 (a b : L) : L :=
  a + b + (-1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 24 correction factor(s). -/
def awStage24 (a b : L) : L :=
  a + b + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 25 correction factor(s). -/
def awStage25 (a b : L) : L :=
  a + b + (5 / 336 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 26 correction factor(s). -/
def awStage26 (a b : L) : L :=
  a + b + (-1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 27 correction factor(s). -/
def awStage27 (a b : L) : L :=
  a + b + (5 / 1008 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 28 correction factor(s). -/
def awStage28 (a b : L) : L :=
  a + b + (1 / 28 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 29 correction factor(s). -/
def awStage29 (a b : L) : L :=
  a + b + (1 / 84 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 30 correction factor(s). -/
def awStage30 (a b : L) : L :=
  a + b + (-11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 31 correction factor(s). -/
def awStage31 (a b : L) : L :=
  a + b + (-19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 32 correction factor(s). -/
def awStage32 (a b : L) : L :=
  a + b + (-5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 33 correction factor(s). -/
def awStage33 (a b : L) : L :=
  a + b + (1 / 126 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 34 correction factor(s). -/
def awStage34 (a b : L) : L :=
  a + b + (1 / 168 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 35 correction factor(s). -/
def awStage35 (a b : L) : L :=
  a + b + (-1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 36 correction factor(s). -/
def awStage36 (a b : L) : L :=
  a + b + (1 / 504 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 37 correction factor(s). -/
def awStage37 (a b : L) : L :=
  a + b + (11 / 336 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆
    + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

/-- The logarithm of `addWord` after its first 38 correction factor(s). -/
def awStage38 (a b : L) : L :=
  a + b + (-1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆

end StageValues

section Stages

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)] [NeZero (7 : ZMod p)]

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 1. -/
theorem bwStep1 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (commPoly (F := ZMod p) a b) ((-(1 / 2) : ZMod p) • (p3x (F := ZMod p) a b)) =
      bwStage1 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, commPoly, bwStage1, p3x, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 2. -/
theorem bwStep2 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage1 (p := p) a b) ((-(1 / 2) : ZMod p) • (p3y (F := ZMod p) a b)) =
      bwStage2 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage1, bwStage2, p3y, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 3. -/
theorem bwStep3 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage2 (p := p) a b) ((1 / 3 : ZMod p) • (p4xx (F := ZMod p) a b)) =
      bwStage3 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage2, bwStage3, p4xx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 4. -/
theorem bwStep4 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage3 (p := p) a b) ((1 / 4 : ZMod p) • (p4yx (F := ZMod p) a b)) =
      bwStage4 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage3, bwStage4, p4yx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 5. -/
theorem bwStep5 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage4 (p := p) a b) ((1 / 3 : ZMod p) • (p4yy (F := ZMod p) a b)) =
      bwStage5 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage4, bwStage5, p4yy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 6. -/
theorem bwStep6 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage5 (p := p) a b) ((-(1 / 4) : ZMod p) • (p5xxx (F := ZMod p) a b)) =
      bwStage6 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage5, bwStage6, p5xxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 7. -/
theorem bwStep7 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage6 (p := p) a b) ((-(3 / 4) : ZMod p) • (p5yxx (F := ZMod p) a b)) =
      bwStage7 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage6, bwStage7, p5yxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 8. -/
theorem bwStep8 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage7 (p := p) a b) ((7 / 12 : ZMod p) • (p5xyx (F := ZMod p) a b)) =
      bwStage8 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage7, bwStage8, p5xyx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 9. -/
theorem bwStep9 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage8 (p := p) a b) ((-(2 / 3) : ZMod p) • (p5yyx (F := ZMod p) a b)) =
      bwStage9 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage8, bwStage9, p5yyx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 10. -/
theorem bwStep10 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage9 (p := p) a b) ((1 / 2 : ZMod p) • (p5xyy (F := ZMod p) a b)) =
      bwStage10 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage9, bwStage10, p5xyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 11. -/
theorem bwStep11 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage10 (p := p) a b) ((-(1 / 4) : ZMod p) • (p5yyy (F := ZMod p) a b)) =
      bwStage11 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage10, bwStage11, p5yyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 12. -/
theorem bwStep12 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage11 (p := p) a b) ((1 / 5 : ZMod p) • (p6xxxx (F := ZMod p) a b)) =
      bwStage12 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage11, bwStage12, p6xxxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 13. -/
theorem bwStep13 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage12 (p := p) a b) ((9 / 8 : ZMod p) • (p6yxxx (F := ZMod p) a b)) =
      bwStage13 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage12, bwStage13, p6yxxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 14. -/
theorem bwStep14 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage13 (p := p) a b) ((-1 : ZMod p) • (p6xyxx (F := ZMod p) a b)) =
      bwStage14 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage13, bwStage14, p6xyxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 15. -/
theorem bwStep15 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage14 (p := p) a b) ((47 / 72 : ZMod p) • (p6yyxx (F := ZMod p) a b)) =
      bwStage15 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage14, bwStage15, p6yyxx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 16. -/
theorem bwStep16 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage15 (p := p) a b) ((19 / 24 : ZMod p) • (p6yxyx (F := ZMod p) a b)) =
      bwStage16 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage15, bwStage16, p6yxyx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 17. -/
theorem bwStep17 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage16 (p := p) a b) ((-(4 / 3) : ZMod p) • (p6xyyx (F := ZMod p) a b)) =
      bwStage17 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage16, bwStage17, p6xyyx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 18. -/
theorem bwStep18 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage17 (p := p) a b) ((35 / 24 : ZMod p) • (p6yyyx (F := ZMod p) a b)) =
      bwStage18 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage17, bwStage18, p6yyyx, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 19. -/
theorem bwStep19 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage18 (p := p) a b) ((-(4 / 3) : ZMod p) • (p6yxyy (F := ZMod p) a b)) =
      bwStage19 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage18, bwStage19, p6yxyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 20. -/
theorem bwStep20 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage19 (p := p) a b) ((1 / 5 : ZMod p) • (p6yyyy (F := ZMod p) a b)) =
      bwStage20 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage19, bwStage20, p6yyyy, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 21. -/
theorem bwStep21 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage20 (p := p) a b) ((-(1 / 6) : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage21 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage20, bwStage21, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 22. -/
theorem bwStep22 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage21 (p := p) a b) ((-(37 / 24) : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage22 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage21, bwStage22, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 23. -/
theorem bwStep23 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage22 (p := p) a b) ((187 / 120 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage23 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage22, bwStage23, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 24. -/
theorem bwStep24 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage23 (p := p) a b) ((-(9 / 16) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage24 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage23, bwStage24, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 25. -/
theorem bwStep25 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage24 (p := p) a b) ((-(7 / 60) : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage25 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage24, bwStage25, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 26. -/
theorem bwStep26 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage25 (p := p) a b) ((-(4 / 3) : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage26 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage25, bwStage26, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 27. -/
theorem bwStep27 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage26 (p := p) a b) ((37 / 24 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage27 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage26, bwStage27, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 28. -/
theorem bwStep28 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage27 (p := p) a b) ((-(17 / 18) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage28 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage27, bwStage28, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 29. -/
theorem bwStep29 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage28 (p := p) a b) ((1 / 3 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage29 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage28, bwStage29, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 30. -/
theorem bwStep30 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage29 (p := p) a b) ((-(305 / 144) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage30 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage29, bwStage30, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 31. -/
theorem bwStep31 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage30 (p := p) a b) ((-(1 / 16) : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage31 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage30, bwStage31, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 32. -/
theorem bwStep32 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage31 (p := p) a b) ((25 / 12 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage32 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage31, bwStage32, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 33. -/
theorem bwStep33 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage32 (p := p) a b) ((91 / 48 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage33 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage32, bwStage33, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 34. -/
theorem bwStep34 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage33 (p := p) a b) ((-(59 / 15) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage34 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage33, bwStage34, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 35. -/
theorem bwStep35 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage34 (p := p) a b) ((-1 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage35 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage34, bwStage35, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 36. -/
theorem bwStep36 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage35 (p := p) a b) ((103 / 24 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage36 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage35, bwStage36, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 37. -/
theorem bwStep37 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage36 (p := p) a b) ((-(11 / 24) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      bwStage37 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage36, bwStage37, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `bracketWord`, factor 38. -/
theorem bwStep38 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bwStage37 (p := p) a b) ((-(1 / 6) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      ⁅a, b⁆ := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, bwStage37, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 1. -/
theorem awStep1 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (bch (F := ZMod p) a b) ((-(1 / 2) : ZMod p) • ⁅a, b⁆) =
      awStage1 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (bch (F := ZMod p) a b) ((-(1 / 2) : ZMod p) • ⁅a, b⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, bch, awStage1, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 2. -/
theorem awStep2 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage1 (p := p) a b) ((1 / 6 : ZMod p) • ⁅a, ⁅a, b⁆⁆) =
      awStage2 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage1 (p := p) a b) ((1 / 6 : ZMod p) • ⁅a, ⁅a, b⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage1, awStage2, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 3. -/
theorem awStep3 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage2 (p := p) a b) ((1 / 3 : ZMod p) • ⁅b, ⁅a, b⁆⁆) =
      awStage3 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage2 (p := p) a b) ((1 / 3 : ZMod p) • ⁅b, ⁅a, b⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage2, awStage3, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 4. -/
theorem awStep4 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage3 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆) =
      awStage4 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage3 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage3, awStage4, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 5. -/
theorem awStep5 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage4 (p := p) a b) ((-(1 / 8) : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆) =
      awStage5 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage4 (p := p) a b) ((-(1 / 8) : ZMod p) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage4, awStage5, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 6. -/
theorem awStep6 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage5 (p := p) a b) ((-(1 / 8) : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆) =
      awStage6 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage5 (p := p) a b) ((-(1 / 8) : ZMod p) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage5, awStage6, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 7. -/
theorem awStep7 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage6 (p := p) a b) ((1 / 120 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆) =
      awStage7 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage6 (p := p) a b) ((1 / 120 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage6, awStage7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 8. -/
theorem awStep8 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage7 (p := p) a b) ((1 / 20 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆) =
      awStage8 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage7 (p := p) a b) ((1 / 20 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage7, awStage8, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 9. -/
theorem awStep9 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage8 (p := p) a b) ((1 / 10 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆) =
      awStage9 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage8 (p := p) a b) ((1 / 10 : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage8, awStage9, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 10. -/
theorem awStep10 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage9 (p := p) a b) ((-(1 / 60) : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆) =
      awStage10 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage9 (p := p) a b) ((-(1 / 60) : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage9, awStage10, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 11. -/
theorem awStep11 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage10 (p := p) a b) ((-(1 / 20) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆) =
      awStage11 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage10 (p := p) a b) ((-(1 / 20) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage10, awStage11, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 12. -/
theorem awStep12 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage11 (p := p) a b) ((1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆) =
      awStage12 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage11 (p := p) a b) ((1 / 30 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage11, awStage12, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 13. -/
theorem awStep13 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage12 (p := p) a b) ((-(1 / 720) : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage13 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage12 (p := p) a b) ((-(1 / 720) : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage12, awStage13, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 14. -/
theorem awStep14 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage13 (p := p) a b) ((-(1 / 72) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage14 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage13 (p := p) a b) ((-(1 / 72) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage13, awStage14, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 15. -/
theorem awStep15 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage14 (p := p) a b) ((-(5 / 72) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage15 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage14 (p := p) a b) ((-(5 / 72) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage14, awStage15, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 16. -/
theorem awStep16 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage15 (p := p) a b) ((1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage16 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage15 (p := p) a b) ((1 / 144 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage15, awStage16, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 17. -/
theorem awStep17 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage16 (p := p) a b) ((7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage17 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage16 (p := p) a b) ((7 / 72 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage16, awStage17, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 18. -/
theorem awStep18 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage17 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage18 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage17 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage17, awStage18, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 19. -/
theorem awStep19 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage18 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage19 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage18 (p := p) a b) ((-(1 / 24) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage18, awStage19, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 20. -/
theorem awStep20 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage19 (p := p) a b) ((1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage20 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage19 (p := p) a b) ((1 / 36 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage19, awStage20, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 21. -/
theorem awStep21 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage20 (p := p) a b) ((-(1 / 144) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆) =
      awStage21 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage20 (p := p) a b) ((-(1 / 144) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage20, awStage21, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 22. -/
theorem awStep22 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage21 (p := p) a b) ((1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage22 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage21 (p := p) a b) ((1 / 5040 : ZMod p) • ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage21, awStage22, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 23. -/
theorem awStep23 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage22 (p := p) a b) ((1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage23 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage22 (p := p) a b) ((1 / 252 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage22, awStage23, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 24. -/
theorem awStep24 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage23 (p := p) a b) ((1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage24 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage23 (p := p) a b) ((1 / 84 : ZMod p) • ⁅a, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage23, awStage24, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 25. -/
theorem awStep25 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage24 (p := p) a b) ((-(5 / 1008) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage25 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage24 (p := p) a b) ((-(5 / 1008) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage24, awStage25, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 26. -/
theorem awStep26 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage25 (p := p) a b) ((-(5 / 336) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage26 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage25 (p := p) a b) ((-(5 / 336) : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage25, awStage26, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 27. -/
theorem awStep27 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage26 (p := p) a b) ((1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage27 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage26 (p := p) a b) ((1 / 56 : ZMod p) • ⁅a, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage26, awStage27, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 28. -/
theorem awStep28 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage27 (p := p) a b) ((-(5 / 1008) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage28 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage27 (p := p) a b) ((-(5 / 1008) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage27, awStage28, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 29. -/
theorem awStep29 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage28 (p := p) a b) ((-(1 / 28) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage29 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage28 (p := p) a b) ((-(1 / 28) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage28, awStage29, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 30. -/
theorem awStep30 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage29 (p := p) a b) ((-(1 / 84) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage30 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage29 (p := p) a b) ((-(1 / 84) : ZMod p) • ⁅a, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage29, awStage30, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 31. -/
theorem awStep31 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage30 (p := p) a b) ((11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage31 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage30 (p := p) a b) ((11 / 5040 : ZMod p) • ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage30, awStage31, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 32. -/
theorem awStep32 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage31 (p := p) a b) ((19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage32 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage31 (p := p) a b) ((19 / 1008 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage31, awStage32, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 33. -/
theorem awStep33 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage32 (p := p) a b) ((5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage33 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage32 (p := p) a b) ((5 / 168 : ZMod p) • ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage32, awStage33, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 34. -/
theorem awStep34 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage33 (p := p) a b) ((-(1 / 126) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage34 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage33 (p := p) a b) ((-(1 / 126) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage33, awStage34, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 35. -/
theorem awStep35 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage34 (p := p) a b) ((-(1 / 168) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage35 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage34 (p := p) a b) ((-(1 / 168) : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage34, awStage35, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 36. -/
theorem awStep36 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage35 (p := p) a b) ((1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage36 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage35 (p := p) a b) ((1 / 21 : ZMod p) • ⁅b, ⁅b, ⁅a, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage35, awStage36, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 37. -/
theorem awStep37 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage36 (p := p) a b) ((-(1 / 504) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage37 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage36 (p := p) a b) ((-(1 / 504) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage36, awStage37, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 38. -/
theorem awStep38 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage37 (p := p) a b) ((-(11 / 336) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      awStage38 (p := p) a b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage37 (p := p) a b) ((-(11 / 336) : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage37, awStage38, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

set_option maxHeartbeats 0 in
/-- `addWord`, factor 39. -/
theorem awStep39 (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :
    bch (F := ZMod p) (awStage38 (p := p) a b) ((1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆) =
      a + b := by
  have height := oct_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  rw [bch_eq_six_add (awStage38 (p := p) a b) ((1 / 840 : ZMod p) • ⁅b, ⁅b, ⁅b, ⁅b, ⁅b, ⁅a, b⁆⁆⁆⁆⁆⁆),
    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]
  simp only [QSearch.BCHClassSix.bch, awStage38, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, two6a a b, two6b a b, two6c a b]
  all_goals match_scalars
  all_goals (try field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p), NeZero.ne (5 : ZMod p), NeZero.ne (7 : ZMod p), ne4 (F := ZMod p), ne6 (F := ZMod p), ne8 (F := ZMod p), ne9 (F := ZMod p), ne10 (F := ZMod p), ne12 (F := ZMod p), ne15 (F := ZMod p), ne16 (F := ZMod p), ne18 (F := ZMod p), ne20 (F := ZMod p), ne21 (F := ZMod p), ne24 (F := ZMod p), ne28 (F := ZMod p), ne30 (F := ZMod p), ne36 (F := ZMod p), ne45 (F := ZMod p), ne48 (F := ZMod p), ne56 (F := ZMod p), ne60 (F := ZMod p), ne63 (F := ZMod p), ne72 (F := ZMod p), ne80 (F := ZMod p), ne84 (F := ZMod p), ne90 (F := ZMod p), ne96 (F := ZMod p), ne105 (F := ZMod p), ne112 (F := ZMod p), ne120 (F := ZMod p), ne126 (F := ZMod p), ne144 (F := ZMod p), ne168 (F := ZMod p), ne180 (F := ZMod p), ne224 (F := ZMod p), ne240 (F := ZMod p), ne252 (F := ZMod p), ne280 (F := ZMod p), ne288 (F := ZMod p), ne315 (F := ZMod p), ne336 (F := ZMod p), ne360 (F := ZMod p), ne378 (F := ZMod p), ne504 (F := ZMod p), ne630 (F := ZMod p), ne672 (F := ZMod p), ne720 (F := ZMod p), ne756 (F := ZMod p), ne840 (F := ZMod p), ne945 (F := ZMod p), ne1008 (F := ZMod p), ne1120 (F := ZMod p), ne1260 (F := ZMod p), ne1440 (F := ZMod p), ne1890 (F := ZMod p), ne2016 (F := ZMod p), ne2520 (F := ZMod p), ne3360 (F := ZMod p), ne3780 (F := ZMod p), ne5040 (F := ZMod p), ne7560 (F := ZMod p), ne10080 (F := ZMod p), ne15120 (F := ZMod p), ne30240 (F := ZMod p)])
  all_goals ring

end Stages

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)] [NeZero (7 : ZMod p)]
  {hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val

/-- Removing the degree-three to degree-six and then the central degree-seven
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
    powerScalar (1 / 5 : ZMod p) (comm y (comm y (comm y (comm y (comm x y))))) *
    powerScalar (-(1 / 6) : ZMod p) (comm x (comm x (comm x (comm x (comm x (comm x y)))))) *
    powerScalar (-(37 / 24) : ZMod p) (comm y (comm x (comm x (comm x (comm x (comm x y)))))) *
    powerScalar (187 / 120 : ZMod p) (comm x (comm y (comm x (comm x (comm x (comm x y)))))) *
    powerScalar (-(9 / 16) : ZMod p) (comm y (comm y (comm x (comm x (comm x (comm x y)))))) *
    powerScalar (-(7 / 60) : ZMod p) (comm x (comm x (comm y (comm x (comm x (comm x y)))))) *
    powerScalar (-(4 / 3) : ZMod p) (comm y (comm x (comm y (comm x (comm x (comm x y)))))) *
    powerScalar (37 / 24 : ZMod p) (comm x (comm y (comm y (comm x (comm x (comm x y)))))) *
    powerScalar (-(17 / 18) : ZMod p) (comm y (comm y (comm y (comm x (comm x (comm x y)))))) *
    powerScalar (1 / 3 : ZMod p) (comm x (comm y (comm x (comm y (comm x (comm x y)))))) *
    powerScalar (-(305 / 144) : ZMod p) (comm y (comm y (comm x (comm y (comm x (comm x y)))))) *
    powerScalar (-(1 / 16) : ZMod p) (comm x (comm x (comm y (comm y (comm x (comm x y)))))) *
    powerScalar (25 / 12 : ZMod p) (comm y (comm x (comm y (comm y (comm x (comm x y)))))) *
    powerScalar (91 / 48 : ZMod p) (comm x (comm y (comm y (comm y (comm x (comm x y)))))) *
    powerScalar (-(59 / 15) : ZMod p) (comm y (comm y (comm y (comm y (comm x (comm x y)))))) *
    powerScalar (-1 : ZMod p) (comm x (comm y (comm x (comm y (comm y (comm x y)))))) *
    powerScalar (103 / 24 : ZMod p) (comm y (comm y (comm x (comm y (comm y (comm x y)))))) *
    powerScalar (-(11 / 24) : ZMod p) (comm x (comm y (comm y (comm y (comm y (comm x y)))))) *
    powerScalar (-(1 / 6) : ZMod p) (comm y (comm y (comm y (comm y (comm y (comm x y))))))

theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, val_comm, commPoly_left hnil, commPoly_right hnil, commPoly_ll hnil, commPoly_rl hnil, commPoly_rr hnil, commPoly_xxx hnil, commPoly_yxx hnil, commPoly_xyx hnil, commPoly_yyx hnil, commPoly_xyy hnil, commPoly_yyy hnil, commPoly_xxxx hnil, commPoly_yxxx hnil, commPoly_xyxx hnil, commPoly_yyxx hnil, commPoly_yxyx hnil, commPoly_xyyx hnil, commPoly_yyyx hnil, commPoly_yxyy hnil, commPoly_yyyy hnil, commPoly_xxxxx hnil, commPoly_yxxxx hnil, commPoly_xyxxx hnil, commPoly_yyxxx hnil, commPoly_xxyxx hnil, commPoly_yxyxx hnil, commPoly_xyyxx hnil, commPoly_yyyxx hnil, commPoly_xyxyx hnil, commPoly_yyxyx hnil, commPoly_xxyyx hnil, commPoly_yxyyx hnil, commPoly_xyyyx hnil, commPoly_yyyyx hnil, commPoly_xyxyy hnil, commPoly_yyxyy hnil, commPoly_xyyyy hnil, commPoly_yyyyy hnil]
  rw [bwStep1 hnil, bwStep2 hnil, bwStep3 hnil, bwStep4 hnil, bwStep5 hnil, bwStep6 hnil,
    bwStep7 hnil, bwStep8 hnil, bwStep9 hnil, bwStep10 hnil, bwStep11 hnil, bwStep12 hnil,
    bwStep13 hnil, bwStep14 hnil, bwStep15 hnil, bwStep16 hnil, bwStep17 hnil, bwStep18 hnil,
    bwStep19 hnil, bwStep20 hnil, bwStep21 hnil, bwStep22 hnil, bwStep23 hnil, bwStep24 hnil,
    bwStep25 hnil, bwStep26 hnil, bwStep27 hnil, bwStep28 hnil, bwStep29 hnil, bwStep30 hnil,
    bwStep31 hnil, bwStep32 hnil, bwStep33 hnil, bwStep34 hnil, bwStep35 hnil, bwStep36 hnil,
    bwStep37 hnil, bwStep38 hnil]

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
  have m_c7xxxxx := comm_mem H hx m_c6xxxx
  have m_c7yxxxx := comm_mem H hy m_c6xxxx
  have m_c7xyxxx := comm_mem H hx m_c6yxxx
  have m_c7yyxxx := comm_mem H hy m_c6yxxx
  have m_c7xxyxx := comm_mem H hx m_c6xyxx
  have m_c7yxyxx := comm_mem H hy m_c6xyxx
  have m_c7xyyxx := comm_mem H hx m_c6yyxx
  have m_c7yyyxx := comm_mem H hy m_c6yyxx
  have m_c7xyxyx := comm_mem H hx m_c6yxyx
  have m_c7yyxyx := comm_mem H hy m_c6yxyx
  have m_c7xxyyx := comm_mem H hx m_c6xyyx
  have m_c7yxyyx := comm_mem H hy m_c6xyyx
  have m_c7xyyyx := comm_mem H hx m_c6yyyx
  have m_c7yyyyx := comm_mem H hy m_c6yyyx
  have m_c7xyxyy := comm_mem H hx m_c6yxyy
  have m_c7yyxyy := comm_mem H hy m_c6yxyy
  have m_c7xyyyy := comm_mem H hx m_c6yyyy
  have m_c7yyyyy := comm_mem H hy m_c6yyyy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (m_c2)
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
    (powerScalar_mem H _ m_c6yyyy))
    (powerScalar_mem H _ m_c7xxxxx))
    (powerScalar_mem H _ m_c7yxxxx))
    (powerScalar_mem H _ m_c7xyxxx))
    (powerScalar_mem H _ m_c7yyxxx))
    (powerScalar_mem H _ m_c7xxyxx))
    (powerScalar_mem H _ m_c7yxyxx))
    (powerScalar_mem H _ m_c7xyyxx))
    (powerScalar_mem H _ m_c7yyyxx))
    (powerScalar_mem H _ m_c7xyxyx))
    (powerScalar_mem H _ m_c7yyxyx))
    (powerScalar_mem H _ m_c7xxyyx))
    (powerScalar_mem H _ m_c7yxyyx))
    (powerScalar_mem H _ m_c7xyyyx))
    (powerScalar_mem H _ m_c7yyyyx))
    (powerScalar_mem H _ m_c7xyxyy))
    (powerScalar_mem H _ m_c7yyxyy))
    (powerScalar_mem H _ m_c7xyyyy))
    (powerScalar_mem H _ m_c7yyyyy)

/-- Addition is recovered by removing the bracket, then the degree-three to
central degree-seven errors, each by a power of an exact bracket monomial. -/
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
    powerScalar (-(1 / 144) : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord x y))))) *
    powerScalar (1 / 5040 : ZMod p) (bracketWord x (bracketWord x (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (1 / 252 : ZMod p) (bracketWord x (bracketWord x (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (1 / 84 : ZMod p) (bracketWord x (bracketWord x (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(5 / 1008) : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(5 / 336) : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (1 / 56 : ZMod p) (bracketWord x (bracketWord y (bracketWord x (bracketWord y (bracketWord y (bracketWord x y)))))) *
    powerScalar (-(5 / 1008) : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(1 / 28) : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(1 / 84) : ZMod p) (bracketWord x (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord x y)))))) *
    powerScalar (11 / 5040 : ZMod p) (bracketWord y (bracketWord x (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (19 / 1008 : ZMod p) (bracketWord y (bracketWord x (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (5 / 168 : ZMod p) (bracketWord y (bracketWord x (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(1 / 126) : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(1 / 168) : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (1 / 21 : ZMod p) (bracketWord y (bracketWord y (bracketWord x (bracketWord y (bracketWord y (bracketWord x y)))))) *
    powerScalar (-(1 / 504) : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord x (bracketWord x (bracketWord x y)))))) *
    powerScalar (-(11 / 336) : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord x (bracketWord x y)))))) *
    powerScalar (1 / 840 : ZMod p) (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord y (bracketWord x y))))))

theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
  rw [awStep1 hnil, awStep2 hnil, awStep3 hnil, awStep4 hnil, awStep5 hnil, awStep6 hnil,
    awStep7 hnil, awStep8 hnil, awStep9 hnil, awStep10 hnil, awStep11 hnil, awStep12 hnil,
    awStep13 hnil, awStep14 hnil, awStep15 hnil, awStep16 hnil, awStep17 hnil, awStep18 hnil,
    awStep19 hnil, awStep20 hnil, awStep21 hnil, awStep22 hnil, awStep23 hnil, awStep24 hnil,
    awStep25 hnil, awStep26 hnil, awStep27 hnil, awStep28 hnil, awStep29 hnil, awStep30 hnil,
    awStep31 hnil, awStep32 hnil, awStep33 hnil, awStep34 hnil, awStep35 hnil, awStep36 hnil,
    awStep37 hnil, awStep38 hnil, awStep39 hnil]

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
  have b_xxxxxxy := bracketWord_mem H hx b_xxxxxy
  have b_xxyxxxy := bracketWord_mem H hx b_xyxxxy
  have b_xxyyxxy := bracketWord_mem H hx b_xyyxxy
  have b_xyxxxxy := bracketWord_mem H hx b_yxxxxy
  have b_xyxyxxy := bracketWord_mem H hx b_yxyxxy
  have b_xyxyyxy := bracketWord_mem H hx b_yxyyxy
  have b_xyyxxxy := bracketWord_mem H hx b_yyxxxy
  have b_xyyyxxy := bracketWord_mem H hx b_yyyxxy
  have b_xyyyyxy := bracketWord_mem H hx b_yyyyxy
  have b_yxxxxxy := bracketWord_mem H hy b_xxxxxy
  have b_yxyxxxy := bracketWord_mem H hy b_xyxxxy
  have b_yxyyxxy := bracketWord_mem H hy b_xyyxxy
  have b_yyxxxxy := bracketWord_mem H hy b_yxxxxy
  have b_yyxyxxy := bracketWord_mem H hy b_yxyxxy
  have b_yyxyyxy := bracketWord_mem H hy b_yxyyxy
  have b_yyyxxxy := bracketWord_mem H hy b_yyxxxy
  have b_yyyyxxy := bracketWord_mem H hy b_yyyxxy
  have b_yyyyyxy := bracketWord_mem H hy b_yyyyxy
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem hx hy)
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
    (powerScalar_mem H _ b_yyyyxy))
    (powerScalar_mem H _ b_xxxxxxy))
    (powerScalar_mem H _ b_xxyxxxy))
    (powerScalar_mem H _ b_xxyyxxy))
    (powerScalar_mem H _ b_xyxxxxy))
    (powerScalar_mem H _ b_xyxyxxy))
    (powerScalar_mem H _ b_xyxyyxy))
    (powerScalar_mem H _ b_xyyxxxy))
    (powerScalar_mem H _ b_xyyyxxy))
    (powerScalar_mem H _ b_xyyyyxy))
    (powerScalar_mem H _ b_yxxxxxy))
    (powerScalar_mem H _ b_yxyxxxy))
    (powerScalar_mem H _ b_yxyyxxy))
    (powerScalar_mem H _ b_yyxxxxy))
    (powerScalar_mem H _ b_yyxyxxy))
    (powerScalar_mem H _ b_yyxyyxy))
    (powerScalar_mem H _ b_yyyxxxy))
    (powerScalar_mem H _ b_yyyyxxy))
    (powerScalar_mem H _ b_yyyyyxy)

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
the group subgroup axioms. The prime-field hypotheses exclude 2, 3, 5 and 7. -/
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥)
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
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥)
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
end QSearch.BCHClassSevenSubgroups

/-- info: 'QSearch.BCHClassSevenSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_comm

/-- info: 'QSearch.BCHClassSevenSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassSevenSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.val_addWord

/-- info: 'QSearch.BCHClassSevenSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassSevenSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassSevenSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassSevenSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassSevenSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassSevenSubgroups.toSubgroup_toLieSubalgebra
