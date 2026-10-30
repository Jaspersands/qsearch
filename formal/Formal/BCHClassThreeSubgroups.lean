import Formal.BCHClassThree
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-three BCH groups

Explicit commutator and power words recover Lie brackets and sums. Thus every
group subgroup has a Lie-subalgebra logarithm over the prime field. Scalar
closure uses that each element of `ZMod p` is the cast of its natural value;
no analogous assertion over a general extension field is made.
-/

namespace QSearch.BCHClassThreeSubgroups

open LieModule QSearch.BCHClassThree

noncomputable section

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)]
  {hnil : lowerCentralSeries F L L 3 = ⊥}

private theorem six_ne_zero : (6 : F) ≠ 0 := by
  rw [show (6 : F) = 2 * 3 by ring]
  exact mul_ne_zero (NeZero.ne 2) (NeZero.ne 3)

private theorem twelve_ne_zero : (12 : F) ≠ 0 := by
  rw [show (12 : F) = 2 * 2 * 3 by ring]
  exact mul_ne_zero (mul_ne_zero (NeZero.ne 2) (NeZero.ne 2)) (NeZero.ne 3)

omit [NeZero (2 : F)] [NeZero (3 : F)] in
theorem triple_central (hnil : lowerCentralSeries F L L 3 = ⊥) (a b c d : L) :
    ⁅a, ⁅b, ⁅c, d⁆⁆⁆ = 0 :=
  classThree_of_lowerCentralSeries hnil a b c d

omit [NeZero (2 : F)] [NeZero (3 : F)] in
theorem bch_of_lie_eq_zero {x y : L} (h : ⁅x, y⁆ = 0) :
    bch (F := F) x y = x + y := by
  have hyx : ⁅y, x⁆ = 0 := by rw [← lie_skew y x, h, neg_zero]
  simp [bch, h, hyx]

/-- Conjugation is the truncated adjoint exponential, derived from the polynomial. -/
theorem bch_conjugate (hnil : lowerCentralSeries F L L 3 = ⊥) (x y : L) :
    bch (F := F) (bch (F := F) x y) (-x) =
      y + ⁅x, y⁆ + (2 : F)⁻¹ • ⁅x, ⁅x, y⁆⁆ := by
  have hfour := triple_central hnil
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  simp only [bch, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    hfour, hyx, lie_neg, neg_lie, lie_self, lie_zero,
    sub_zero, smul_zero, add_zero, zero_add, neg_zero]
  match_scalars <;> field_simp [NeZero.ne (2 : F), twelve_ne_zero (F := F)]
  all_goals ring

/-- Our commutator convention is `x * y * x⁻¹ * y⁻¹`. -/
def comm (x y : BCH F L hnil) : BCH F L hnil := x * y * x⁻¹ * y⁻¹

theorem comm_mem (H : Subgroup (BCH F L hnil)) {x y : BCH F L hnil}
    (hx : x ∈ H) (hy : y ∈ H) : comm x y ∈ H :=
  H.mul_mem (H.mul_mem (H.mul_mem hx hy) (H.inv_mem hx)) (H.inv_mem hy)

theorem val_comm (x y : BCH F L hnil) :
    (comm x y).val = ⁅x.val, y.val⁆ +
      (2 : F)⁻¹ • (⁅x.val, ⁅x.val, y.val⁆⁆ + ⁅y.val, ⁅x.val, y.val⁆⁆) := by
  change bch (F := F) (bch (F := F) (bch (F := F) x.val y.val) (-x.val))
    (-y.val) = _
  rw [bch_conjugate hnil]
  have hfour := triple_central hnil
  simp only [bch, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    hfour, lie_neg, neg_lie, lie_self, lie_zero,
    sub_zero, zero_sub, smul_zero, add_zero, zero_add, neg_zero]
  module

/-- The correction terms in a nested commutator vanish by the class bound. -/
theorem val_nested_comm (z x y : BCH F L hnil) :
    (comm z (comm x y)).val = ⁅z.val, ⁅x.val, y.val⁆⁆ := by
  have hfour := triple_central hnil
  simp only [val_comm, lie_add, lie_smul, hfour, smul_zero, add_zero]

/-- The first correction in the word recovering addition. -/
theorem bch_cancel_bracket (hnil : lowerCentralSeries F L L 3 = ⊥) (x y : L) :
    bch (F := F) (bch (F := F) x y) (-(2 : F)⁻¹ • ⁅x, y⁆) =
      x + y - (6 : F)⁻¹ • ⁅x, ⁅x, y⁆⁆ - (3 : F)⁻¹ • ⁅y, ⁅x, y⁆⁆ := by
  have hfour := triple_central hnil
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  simp only [bch, add_lie, lie_add, smul_lie, lie_smul, lie_lie,
    hfour, hyx, lie_neg, neg_lie, lie_self, lie_zero,
    sub_zero, zero_sub, smul_zero, add_zero, neg_zero]
  match_scalars <;> field_simp [NeZero.ne (2 : F), NeZero.ne (3 : F),
    six_ne_zero (F := F), twelve_ne_zero (F := F)]
  all_goals ring

end PolynomialIdentities

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
  {hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val

/-- The central nested-commutator correction recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  comm x y * powerScalar (-(2 : ZMod p)⁻¹)
    (comm x (comm x y) * comm y (comm x y))

theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  rw [val_mul, val_comm, val_powerScalar, val_mul, val_nested_comm, val_nested_comm]
  rw [bch_of_lie_eq_zero (triple_central hnil _ _ _ _)]
  rw [bch_of_lie_eq_zero (by
    simp only [lie_smul, lie_add, triple_central hnil, add_zero, smul_zero])]
  module

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
  have hc := comm_mem H hx hy
  exact H.mul_mem hc (powerScalar_mem H _
    (H.mul_mem (comm_mem H hx hc) (comm_mem H hy hc)))

/-- Addition is recovered by removing the bracket and then two central errors. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  (x * y * powerScalar (-(2 : ZMod p)⁻¹) (bracketWord x y)) *
    powerScalar (6 : ZMod p)⁻¹ (comm x (comm x y)) *
    powerScalar (3 : ZMod p)⁻¹ (comm y (comm x y))

theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord, val_nested_comm]
  rw [bch_cancel_bracket hnil]
  rw [bch_of_lie_eq_zero (by
    rw [lie_smul, triple_central hnil, smul_zero])]
  rw [bch_of_lie_eq_zero (by
    rw [lie_smul, triple_central hnil, smul_zero])]
  module

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {x y : BCH (ZMod p) L hnil} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
  have hc := comm_mem H hx hy
  exact H.mul_mem (H.mul_mem
    (H.mul_mem (H.mul_mem hx hy) (powerScalar_mem H _ (bracketWord_mem H hx hy)))
    (powerScalar_mem H _ (comm_mem H hx hc)))
    (powerScalar_mem H _ (comm_mem H hy hc))

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
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
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

/-- The reverse construction uses only BCH closure of a Lie subalgebra.
This local definition avoids importing any Rees integration module. -/
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {x | x.val ∈ K}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    exact K.add_mem
      (K.add_mem (K.add_mem hx hy) (K.smul_mem _ (K.lie_mem hx hy)))
      (K.smul_mem _ (K.add_mem
        (K.lie_mem hx (K.lie_mem hx hy)) (K.lie_mem hy (K.lie_mem hy hx))))

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
end QSearch.BCHClassThreeSubgroups

/-- info: 'QSearch.BCHClassThreeSubgroups.val_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_comm

/-- info: 'QSearch.BCHClassThreeSubgroups.val_nested_comm' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_nested_comm

/-- info: 'QSearch.BCHClassThreeSubgroups.val_bracketWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_bracketWord

/-- info: 'QSearch.BCHClassThreeSubgroups.val_addWord' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.val_addWord

/-- info: 'QSearch.BCHClassThreeSubgroups.toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toLieSubalgebra

/-- info: 'QSearch.BCHClassThreeSubgroups.mem_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.mem_toLieSubalgebra

/-- info: 'QSearch.BCHClassThreeSubgroups.toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toSubgroup

/-- info: 'QSearch.BCHClassThreeSubgroups.toLieSubalgebra_toSubgroup' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toLieSubalgebra_toSubgroup

/-- info: 'QSearch.BCHClassThreeSubgroups.toSubgroup_toLieSubalgebra' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.BCHClassThreeSubgroups.toSubgroup_toLieSubalgebra
