import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Algebra.Field.ZMod
import Mathlib.Tactic

/-!
# Balanced signed rational separation

Algebraic core of `research/BALANCED_SIGNED_MPI.md`. Positive and negative
roots are multisets, so repeated roots and cancellation are included.
No assumption on the characteristic, or primality of a multiplicative
group order, occurs here.

These theorems do NOT formalize the logarithm/syndrome bridge, quantum
Fourier transfer, preparation, decoder implementation, or complexity.
-/

namespace QSearch.BalancedSigned

open Polynomial
noncomputable section

variable {F : Type*} [Field F]

def rootPoly (roots : Multiset F) : F[X] :=
  (roots.map fun x => X - C x).prod

def signedCoeff [DecidableEq F] (positive negative : Multiset F) (x : F) : ℤ :=
  (positive.count x : ℤ) - negative.count x

def rationalEval (positive negative : Multiset F) (x : F) : F :=
  (rootPoly positive).eval x / (rootPoly negative).eval x

lemma rootPoly_add (a b : Multiset F) :
    rootPoly (a + b) = rootPoly a * rootPoly b := by
  simp [rootPoly, Multiset.map_add, Multiset.prod_add]

lemma rootPoly_degree (a : Multiset F) : (rootPoly a).natDegree = a.card :=
  natDegree_multiset_prod_X_sub_C_eq_card a

lemma rootPoly_roots (a : Multiset F) : (rootPoly a).roots = a :=
  roots_multiset_prod_X_sub_C a

lemma rootPoly_eval_ne_zero (a : Multiset F) (x : F) (hx : x ∉ a) :
    (rootPoly a).eval x ≠ 0 := by
  intro h
  have hn : rootPoly a ≠ 0 := (monic_multisetProd_X_sub_C a).ne_zero
  have hm : x ∈ (rootPoly a).roots := (mem_roots hn).mpr h
  exact hx ((rootPoly_roots a) ▸ hm)

variable [DecidableEq F]

/-- Equality at more points than either cross-product degree identifies the
signed divisor. Neither numerator/denominator disjointness nor squarefreeness
is assumed. -/
theorem rational_separation
    {I : Type*} [Fintype I] (z : I → F) (hz : Function.Injective z)
    (p q p' q' : Multiset F)
    (hq : ∀ i, z i ∉ q) (hq' : ∀ i, z i ∉ q')
    (hdegree : max (p.card + q'.card) (p'.card + q.card) < Fintype.card I)
    (heval : ∀ i, rationalEval p q (z i) = rationalEval p' q' (z i)) :
    ∀ x, signedCoeff p q x = signedCoeff p' q' x := by
  have hcross : rootPoly (p + q') = rootPoly (p' + q) := by
    apply eq_of_natDegree_lt_card_of_eval_eq _ _ hz
    · intro i
      have h := (div_eq_div_iff
        (rootPoly_eval_ne_zero q (z i) (hq i))
        (rootPoly_eval_ne_zero q' (z i) (hq' i))).mp (heval i)
      simpa [rootPoly_add, eval_mul, rationalEval] using h
    · simpa [rootPoly_degree] using hdegree
  have hroots : p + q' = p' + q := by
    simpa only [rootPoly_roots] using congrArg Polynomial.roots hcross
  intro x
  have hcounts : p.count x + q'.count x = p'.count x + q.count x := by
    simpa using congrArg (Multiset.count x) hroots
  unfold signedCoeff
  omega

/-- The balanced box is syndrome-injective after the rational-evaluation
bridge: n > a+b suffices, even when total support can reach a+b. -/
theorem box_injective
    {I : Type*} [Fintype I] (z : I → F) (hz : Function.Injective z)
    (p q p' q' : Multiset F) (a b : ℕ)
    (hp : p.card ≤ a) (hq : q.card ≤ b)
    (hp' : p'.card ≤ a) (hq' : q'.card ≤ b)
    (hzq : ∀ i, z i ∉ q) (hzq' : ∀ i, z i ∉ q')
    (hn : a + b < Fintype.card I)
    (heval : ∀ i, rationalEval p q (z i) = rationalEval p' q' (z i)) :
    ∀ x, signedCoeff p q x = signedCoeff p' q' x :=
  rational_separation z hz p q p' q' hzq hzq' (by omega) heval

/-- A positive observable frequency may duplicate a root or cancel a
negative root. The extra evaluation coordinate still prevents aliases. -/
theorem positive_readout_separation
    {I : Type*} [Fintype I] (z : I → F) (hz : Function.Injective z)
    (p q p' q' : Multiset F) (a b : ℕ) (t : F)
    (hp : p.card ≤ a) (hq : q.card ≤ b)
    (hp' : p'.card ≤ a) (hq' : q'.card ≤ b)
    (hzq : ∀ i, z i ∉ q) (hzq' : ∀ i, z i ∉ q')
    (hn : a + b + 1 < Fintype.card I)
    (heval : ∀ i, rationalEval (p + {t}) q (z i) = rationalEval p' q' (z i)) :
    ∀ x, signedCoeff p q x + (if x = t then 1 else 0) = signedCoeff p' q' x := by
  have h := rational_separation z hz (p + {t}) q p' q' hzq hzq'
    (by simp only [Multiset.card_add, Multiset.card_singleton]; omega) heval
  intro x
  have hx := h x
  by_cases ht : x = t
  · simp [signedCoeff, ht] at hx ⊢
    omega
  · simp [signedCoeff, ht] at hx ⊢
    omega

/-- The negative observable frequency has the same guard. Its new pole
must, as in the public problem, be disjoint from the evaluation points. -/
theorem negative_readout_separation
    {I : Type*} [Fintype I] (z : I → F) (hz : Function.Injective z)
    (p q p' q' : Multiset F) (a b : ℕ) (t : F)
    (hp : p.card ≤ a) (hq : q.card ≤ b)
    (hp' : p'.card ≤ a) (hq' : q'.card ≤ b)
    (hzq : ∀ i, z i ∉ q) (hzq' : ∀ i, z i ∉ q')
    (hzt : ∀ i, z i ≠ t)
    (hn : a + b + 1 < Fintype.card I)
    (heval : ∀ i, rationalEval p (q + {t}) (z i) = rationalEval p' q' (z i)) :
    ∀ x, signedCoeff p q x - (if x = t then 1 else 0) = signedCoeff p' q' x := by
  have h := rational_separation z hz p (q + {t}) p' q'
    (by intro i; simp [hzq i, hzt i]) hzq'
    (by simp only [Multiset.card_add, Multiset.card_singleton]; omega) heval
  intro x
  have hx := h x
  by_cases ht : x = t
  · simp [signedCoeff, ht] at hx ⊢
    omega
  · simp [signedCoeff, ht] at hx ⊢
    omega

/-- The integer-budget guard in the Python API is precisely the strict
degree/root-count requirement, not a non-strict interpolation bound. -/
theorem budget_guard_iff (n a b moment : ℕ) :
    a + b + moment + 1 ≤ n ↔ a + b + moment < n := by
  omega

def labelRoots {J : Type*} [Fintype J] (t : J → F) (w : J → ℕ) : Multiset F :=
  Finset.univ.val.bind fun j => Multiset.replicate (w j) (t j)

omit [Field F] [DecidableEq F] in
lemma labelRoots_card {J : Type*} [Fintype J] (t : J → F) (w : J → ℕ) :
    (labelRoots t w).card = ∑ j, w j := by
  simp only [labelRoots, Multiset.card_bind, Function.comp_def,
    Multiset.card_replicate, Finset.sum_map_val]

omit [Field F] in
lemma labelRoots_count {J : Type*} [Fintype J] (t : J → F)
    (ht : Function.Injective t) (w : J → ℕ) (j : J) :
    (labelRoots t w).count (t j) = w j := by
  classical
  simp only [labelRoots, Multiset.count_bind, Multiset.count_replicate]
  change (∑ i, if t i = t j then w i else 0) = w j
  simp [ht.eq_iff]

omit [Field F] [DecidableEq F] in
lemma labelRoots_not_mem {J : Type*} [Fintype J] (t : J → F) (w : J → ℕ)
    (x : F) (hx : ∀ j, x ≠ t j) : x ∉ labelRoots t w := by
  intro h
  obtain ⟨j, _, hj⟩ := Multiset.mem_bind.mp h
  exact hx j (Multiset.eq_of_mem_replicate hj)

omit [Field F] in
/-- Bridge to actual integer coordinate labels, including magnitudes greater
than one. Injective support points are essential. -/
theorem integer_label_encoding {J : Type*} [Fintype J] (t : J → F)
    (ht : Function.Injective t) (w : J → ℤ) (j : J) :
    signedCoeff (labelRoots t fun i => (w i).toNat)
      (labelRoots t fun i => (-w i).toNat) (t j) = w j := by
  rw [signedCoeff, labelRoots_count t ht, labelRoots_count t ht]
  omega

/-- Separation for arbitrary integer label arrays with asymmetric positive
and negative budgets. This directly covers the score-shifted word with
budgets (a+1,b+1) versus an original word with budgets (a,b). -/
theorem integer_label_separation
    {I J : Type*} [Fintype I] [Fintype J]
    (t : J → F) (ht : Function.Injective t)
    (z : I → F) (hz : Function.Injective z)
    (u v : J → ℤ) (au bu av bv : ℕ)
    (hup : ∑ j, (u j).toNat ≤ au) (hun : ∑ j, (-u j).toNat ≤ bu)
    (hvp : ∑ j, (v j).toNat ≤ av) (hvn : ∑ j, (-v j).toNat ≤ bv)
    (hdisjoint : ∀ i j, z i ≠ t j)
    (hn : max (au + bv) (av + bu) < Fintype.card I)
    (heval : ∀ i,
      rationalEval (labelRoots t fun j => (u j).toNat)
        (labelRoots t fun j => (-u j).toNat) (z i) =
      rationalEval (labelRoots t fun j => (v j).toNat)
        (labelRoots t fun j => (-v j).toNat) (z i)) :
    u = v := by
  have h := rational_separation z hz
    (labelRoots t fun j => (u j).toNat) (labelRoots t fun j => (-u j).toNat)
    (labelRoots t fun j => (v j).toNat) (labelRoots t fun j => (-v j).toNat)
    (fun i => labelRoots_not_mem t _ (z i) (hdisjoint i))
    (fun i => labelRoots_not_mem t _ (z i) (hdisjoint i))
    (by simp only [labelRoots_card]; omega) heval
  funext j
  simpa only [integer_label_encoding t ht] using h (t j)

local instance : Fact (Nat.Prime 11) := ⟨by decide⟩

/-- Three distinct, pole-free evaluation points admit a score alias at
cross-product degree three. The original source and comparison pattern
each have one positive and one negative root; adding a positive frequency
at root 3 produces the repeated-root numerator on the left. -/
theorem readout_guard_counterexample :
    (∀ x : ZMod 11, x = 4 ∨ x = 7 ∨ x = 10 →
      rationalEval ({3, 3} : Multiset (ZMod 11)) {0} x =
        rationalEval {1} {3} x) ∧
    signedCoeff ({3, 3} : Multiset (ZMod 11)) {0} 3 ≠
      signedCoeff {1} {3} 3 := by
  constructor
  · intro x hx
    have h4 : (4 : ZMod 11) ≠ 0 := by decide
    have h7 : (7 : ZMod 11) ≠ 0 := by decide
    have h10 : (10 : ZMod 11) ≠ 0 := by decide
    rcases hx with rfl | rfl | rfl <;>
      norm_num [rationalEval, rootPoly, Polynomial.eval_mul] <;>
      field_simp [h4, h7, h10] <;> decide
  · decide

theorem counterexample_points_valid :
    (4 : ZMod 11) ≠ 7 ∧ (4 : ZMod 11) ≠ 10 ∧ (7 : ZMod 11) ≠ 10 ∧
    ∀ x : ZMod 11, x = 4 ∨ x = 7 ∨ x = 10 → x ≠ 0 ∧ x ≠ 3 := by
  decide

end
end QSearch.BalancedSigned
