import Formal.BCHClassFour
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-four BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over the prime field. The words
were designed with the exact rational model
`research/audits/reviews/2026-11-02-rees-lean-2/words4.py`; Lean checks every
identity independently. Scalar closure uses that each element of `ZMod p` is
the cast of its natural value; no analogous assertion over a general extension
field is made.

Notation in comments: `ab = [a,b]`, `aab = [a,[a,b]]`, `bab = [b,[a,b]]`,
`aaab = [a,[a,[a,b]]]`, `baab = [b,[a,[a,b]]]`, `bbab = [b,[b,[a,b]]]`.
In class four `[a,[b,[a,b]]] = baab` (`jacobi4c`).
-/

namespace QSearch.BCHClassFourSubgroups

open LieModule QSearch.BCHClassFour

noncomputable section

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] in
theorem quad_central (hnil : lowerCentralSeries F L L 4 = ⊥) (a b c d e : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, e⁆⁆⁆⁆ = 0 :=
  classFour_of_lowerCentralSeries hnil a b c d e

/-- The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form. -/
def commPoly (a b : L) : L :=
  ⁅a, b⁆ + (2 : F)⁻¹ • (⁅a, ⁅a, b⁆⁆ + ⁅b, ⁅a, b⁆⁆) + (6 : F)⁻¹ • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ +
    (4 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + (6 : F)⁻¹ • ⁅b, ⁅b, ⁅a, b⁆⁆⁆

/-- Conjugation is the truncated adjoint exponential, derived from the polynomial. -/
theorem bch_conjugate (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) a b) (-a) =
      b + ⁅a, b⁆ + (2 : F)⁻¹ • ⁅a, ⁅a, b⁆⁆ + (6 : F)⁻¹ • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_self, lie_zero, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F),
    six_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twelve_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twentyfour_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F))]
  all_goals ring

theorem bch_comm (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b) = commPoly (F := F) a b := by
  rw [bch_conjugate hnil]
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, commPoly, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_self, lie_zero, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, zero_sub, neg_zero, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F),
    four_ne_zero' (NeZero.ne (2 : F)),
    six_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twelve_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twentyfour_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F))]
  all_goals ring

omit [NeZero (3 : F)] in
/-- `C(a, C(a,b)) = aab + aaab + baab/2`. -/
theorem commPoly_left (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    commPoly (F := F) a (commPoly (F := F) a b) =
      ⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    hfive, lie_self, lie_zero, smul_zero,
    add_zero, sub_zero, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), four_ne_zero' (NeZero.ne (2 : F))]
  all_goals ring

omit [NeZero (3 : F)] in
/-- `C(b, C(a,b)) = bab + baab/2 + bbab`. -/
theorem commPoly_right (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    commPoly (F := F) b (commPoly (F := F) a b) =
      ⁅b, ⁅a, b⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅b, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [commPoly, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    hfive, lie_self, lie_zero, smul_zero,
    add_zero, sub_zero, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), four_ne_zero' (NeZero.ne (2 : F))]
  all_goals ring

omit [NeZero (2 : F)] [NeZero (3 : F)] in
/-- A commutator with a degree-three element is its bracket, a degree-four bracket. -/
theorem commPoly_deg_three (hnil : lowerCentralSeries F L L 4 = ⊥) (a b c d : L) :
    commPoly (F := F) a ⁅b, ⁅c, d⁆⁆ = ⁅a, ⁅b, ⁅c, d⁆⁆⁆ := by
  have hfive := quad_central hnil
  simp only [commPoly,
    hfive, lie_zero, smul_zero,
    add_zero]

omit [NeZero (2 : F)] [NeZero (3 : F)] in
/-- A commutator with a degree-four element is trivial. -/
theorem commPoly_deg_four (hnil : lowerCentralSeries F L L 4 = ⊥) (a b c d e : L) :
    commPoly (F := F) a ⁅b, ⁅c, ⁅d, e⁆⁆⁆ = 0 := by
  have hfive := quad_central hnil
  simp only [commPoly, hfive, lie_zero, smul_zero,
    add_zero]

omit [NeZero (2 : F)] [NeZero (3 : F)] in
/-- `C(a, C(a, C(a,b))) = aaab`, and similarly for the other two degree-four words. -/
theorem commPoly_left_left (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    commPoly (F := F) a (⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆) =
      ⁅a, ⁅a, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  simp only [commPoly, lie_add, lie_smul,
    hfive, lie_zero, smul_zero,
    add_zero]

omit [NeZero (2 : F)] [NeZero (3 : F)] in
theorem commPoly_right_left (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    commPoly (F := F) b (⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆) =
      ⁅b, ⁅a, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  simp only [commPoly, lie_add, lie_smul,
    hfive, lie_zero, smul_zero,
    add_zero]

omit [NeZero (2 : F)] [NeZero (3 : F)] in
theorem commPoly_right_right (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    commPoly (F := F) b (⁅b, ⁅a, b⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅b, ⁅a, b⁆⁆⁆) =
      ⁅b, ⁅b, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  simp only [commPoly, lie_add, lie_smul,
    hfive, lie_zero, smul_zero,
    add_zero]

/-- Removing the bracket from `a ⋆ b` leaves degree-three and degree-four errors. -/
theorem bch_cancel_bracket (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) a b) (-(2 : F)⁻¹ • ⁅a, b⁆) =
      a + b - (6 : F)⁻¹ • ⁅a, ⁅a, b⁆⁆ - (3 : F)⁻¹ • ⁅b, ⁅a, b⁆⁆ -
        (24 : F)⁻¹ • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ - (8 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ -
        (24 : F)⁻¹ • ⁅b, ⁅b, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  have h8 : (8 : F) ≠ 0 := by
    rw [show (8 : F) = 2 * 2 * 2 by ring]
    exact mul_ne_zero (mul_ne_zero (NeZero.ne 2) (NeZero.ne 2)) (NeZero.ne 2)
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_self, lie_zero, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), h8,
    six_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twelve_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twentyfour_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F))]
  all_goals ring

/-- Removing the degree-three errors leaves only central degree-four errors. -/
theorem bch_cancel_cubic (hnil : lowerCentralSeries F L L 4 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F)
      (a + b - (6 : F)⁻¹ • ⁅a, ⁅a, b⁆⁆ - (3 : F)⁻¹ • ⁅b, ⁅a, b⁆⁆ -
        (24 : F)⁻¹ • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ - (8 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ -
        (24 : F)⁻¹ • ⁅b, ⁅b, ⁅a, b⁆⁆⁆)
      ((6 : F)⁻¹ • (⁅a, ⁅a, b⁆⁆ + ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆)))
      ((3 : F)⁻¹ • (⁅b, ⁅a, b⁆⁆ + (2 : F)⁻¹ • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ + ⁅b, ⁅b, ⁅a, b⁆⁆⁆)) =
      a + b + (5 / 24 : F) • ⁅a, ⁅a, ⁅a, b⁆⁆⁆ + (3 / 8 : F) • ⁅b, ⁅a, ⁅a, b⁆⁆⁆ +
        (11 / 24 : F) • ⁅b, ⁅b, ⁅a, b⁆⁆⁆ := by
  have hfive := quad_central hnil
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  have h8 : (8 : F) ≠ 0 := by
    rw [show (8 : F) = 2 * 2 * 2 by ring]
    exact mul_ne_zero (mul_ne_zero (NeZero.ne 2) (NeZero.ne 2)) (NeZero.ne 2)
  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    lie_neg, hfive, lie_self, lie_zero, smul_zero, smul_neg,
    add_zero, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F), h8,
    six_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twelve_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F)),
    twentyfour_ne_zero' (NeZero.ne (2 : F)) (NeZero.ne (3 : F))]
  all_goals ring

end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] {hnil : lowerCentralSeries F L L 4 = ⊥}

/-- Our commutator convention is `x * y * x⁻¹ * y⁻¹`. -/
def comm (x y : BCH F L hnil) : BCH F L hnil := x * y * x⁻¹ * y⁻¹

theorem comm_mem (H : Subgroup (BCH F L hnil)) {x y : BCH F L hnil}
    (hx : x ∈ H) (hy : y ∈ H) : comm x y ∈ H :=
  H.mul_mem (H.mul_mem (H.mul_mem hx hy) (H.inv_mem hx)) (H.inv_mem hy)

theorem val_comm (x y : BCH F L hnil) :
    (comm x y).val = commPoly (F := F) x.val y.val :=
  bch_comm hnil x.val y.val

/-- The two degree-three commutator words. -/
theorem val_comm_left (x y : BCH F L hnil) :
    (comm x (comm x y)).val = ⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ +
      (2 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ := by
  rw [val_comm, val_comm, commPoly_left hnil]

theorem val_comm_right (x y : BCH F L hnil) :
    (comm y (comm x y)).val = ⁅y.val, ⁅x.val, y.val⁆⁆ +
      (2 : F)⁻¹ • ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ + ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆ := by
  rw [val_comm, val_comm, commPoly_right hnil]

/-- The three central degree-four commutator words. -/
theorem val_comm_left_left (x y : BCH F L hnil) :
    (comm x (comm x (comm x y))).val = ⁅x.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ := by
  rw [val_comm, val_comm_left, commPoly_left_left hnil]

theorem val_comm_right_left (x y : BCH F L hnil) :
    (comm y (comm x (comm x y))).val = ⁅y.val, ⁅x.val, ⁅x.val, y.val⁆⁆⁆ := by
  rw [val_comm, val_comm_left, commPoly_right_left hnil]

theorem val_comm_right_right (x y : BCH F L hnil) :
    (comm y (comm y (comm x y))).val = ⁅y.val, ⁅y.val, ⁅x.val, y.val⁆⁆⁆ := by
  rw [val_comm, val_comm_right, commPoly_right_right hnil]

end Words

/-- Install with `letI := neZeroTwo hp` when the characteristic bound is explicit. -/
theorem neZeroTwo {p : ℕ} (hp : 3 < p) : NeZero (2 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 2 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroThree hp` when the characteristic bound is explicit. -/
theorem neZeroThree {p : ℕ} (hp : 3 < p) : NeZero (3 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 3 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) hp)⟩

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]
  {hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val

/-- Removing the degree-three and then the central degree-four corrections
from the group commutator recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  comm x y * powerScalar (-(2 : ZMod p)⁻¹) (comm x (comm x y)) *
    powerScalar (-(2 : ZMod p)⁻¹) (comm y (comm x y)) *
    powerScalar (3 : ZMod p)⁻¹ (comm x (comm x (comm x y))) *
    powerScalar (4 : ZMod p)⁻¹ (comm y (comm x (comm x y))) *
    powerScalar (3 : ZMod p)⁻¹ (comm y (comm y (comm x y)))

set_option maxHeartbeats 1000000 in
theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, val_comm,
    ]
  have hfive := quad_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, commPoly, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_self, lie_zero, smul_zero,
    neg_smul, add_zero, sub_zero, neg_zero, jacobi4c x.val y.val]
  match_scalars <;> field_simp [NeZero.ne (2 : ZMod p), NeZero.ne (3 : ZMod p),
    four_ne_zero' (NeZero.ne (2 : ZMod p)),
    six_ne_zero' (NeZero.ne (2 : ZMod p)) (NeZero.ne (3 : ZMod p)),
    twelve_ne_zero' (NeZero.ne (2 : ZMod p)) (NeZero.ne (3 : ZMod p)),
    twentyfour_ne_zero' (NeZero.ne (2 : ZMod p)) (NeZero.ne (3 : ZMod p))]
  all_goals ring

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
  have hc := comm_mem H hx hy
  have hcx := comm_mem H hx hc
  have hcy := comm_mem H hy hc
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem hc
    (powerScalar_mem H _ hcx)) (powerScalar_mem H _ hcy))
    (powerScalar_mem H _ (comm_mem H hx hcx))) (powerScalar_mem H _ (comm_mem H hy hcx)))
    (powerScalar_mem H _ (comm_mem H hy hcy))

/-- Addition is recovered by removing the bracket, then the two degree-three
errors, then three central degree-four errors. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x * y * powerScalar (-(2 : ZMod p)⁻¹) (bracketWord x y) *
    powerScalar (6 : ZMod p)⁻¹ (comm x (comm x y)) *
    powerScalar (3 : ZMod p)⁻¹ (comm y (comm x y)) *
    powerScalar (-(5 / 24 : ZMod p)) (comm x (comm x (comm x y))) *
    powerScalar (-(3 / 8 : ZMod p)) (comm y (comm x (comm x y))) *
    powerScalar (-(11 / 24 : ZMod p)) (comm y (comm y (comm x y)))

theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord,
    val_comm_left_left, val_comm_right_left, val_comm_right_right]
  simp only [val_comm_left, val_comm_right]
  rw [bch_cancel_bracket hnil, bch_cancel_cubic hnil]
  have hfive := quad_central hnil
  simp only [bch, lie_add, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hfive, lie_self, lie_zero, smul_zero,
    neg_smul, add_zero, sub_zero, zero_sub, neg_zero]
  module

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
  have hc := comm_mem H hx hy
  have hcx := comm_mem H hx hc
  have hcy := comm_mem H hy hc
  exact H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem (H.mul_mem
    (H.mul_mem hx hy) (powerScalar_mem H _ (bracketWord_mem H hx hy)))
    (powerScalar_mem H _ hcx)) (powerScalar_mem H _ hcy))
    (powerScalar_mem H _ (comm_mem H hx hcx))) (powerScalar_mem H _ (comm_mem H hy hcx)))
    (powerScalar_mem H _ (comm_mem H hy hcy))

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
the group subgroup axioms. The prime-field hypotheses exclude 2 and 3. -/
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
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
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {x | x.val ∈ K}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    have hxy := K.lie_mem hx hy
    exact K.sub_mem (K.add_mem (K.add_mem (K.add_mem hx hy) (K.smul_mem _ hxy))
      (K.smul_mem _ (K.add_mem (K.lie_mem hx hxy) (K.lie_mem hy (K.lie_mem hy hx)))))
      (K.smul_mem _ (K.lie_mem hy (K.lie_mem hx hxy)))

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
end QSearch.BCHClassFourSubgroups

/-- info: 'QSearch.BCHClassFourSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_comm

/-- info: 'QSearch.BCHClassFourSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassFourSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.val_addWord

/-- info: 'QSearch.BCHClassFourSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassFourSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassFourSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassFourSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassFourSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.BCHClassFourSubgroups.toSubgroup_toLieSubalgebra
