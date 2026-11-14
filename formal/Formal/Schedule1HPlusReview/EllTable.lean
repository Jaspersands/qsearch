import Formal.Schedule1HPlus.Guards

/-!
# Hostile review (2026-11-14): a real level-3 table satisfies `IsEllContraction`

Not imported by `Formal.lean`. Build with `lake build Formal.Schedule1HPlusReview.EllTable`.

The author instantiated `IsEllContraction` (Definition `def:plus-ell`) only at the trivial
level `ℓ = 1`, `Ω = ℤ_κ`. Here:

* `ann_iff_check`: condition (iii) of `IsEllContraction` (vanishing on *every* family with
  the axis relations) is equivalent to a finite condition: for every `y'`,
  `∑_y C_y E(y, y') = 0`, where `E(y, y') = ∏_r e(y_r, y'_r)` and
  `e(k, m) = 0` if `m = 0`, `-z_m` if `k = 0 ≠ m`, `[k = m]` otherwise. The families
  `E(·, y')` (`y'` without zero coordinate) are the paper's basis tensors
  `⊗_r (e_{y'_r} - z_{y'_r} e_0)` of `W^{⊗ℓ}`; `expand` shows every family with the axis
  relations is their combination. This is the remark after `def:plus-ell`.
* `ell3_13_4`: the paper's table for `(p, κ) = (13, 4)`, level `ℓ = 3`
  (`research/audits/reviews/2026-11-13-rees-k9-below-21/B3_13_4.json`, `C_y = g^{|y|} B(y)`,
  `g = 2`), is an `ℓ`-level `{0}`-contraction for the class map of `ξ = g = 2`, checked by
  `decide` on the Lean definition itself (through `ann_iff_check`).
* `ell3_13_4_solver`: hence Lemma `lem:plus-ell-node` gives a concrete `4`-solver of degree 3
  over `F_13` (candidate (e) is not vacuous at this pair).
* Negative controls: the stored perturbed table (`B3_13_4_perturbed.json`) is rejected, and a
  table with one entry multiplied by a 4th power (classes unchanged) is rejected by (iii).
-/

namespace QSearch.Schedule1HPlus.Review

open QSearch.Schedule1H QSearch.Schedule1HPlus Finset

section Expand

variable {K : Type*} [Field K] [DecidableEq K] {N : ℕ} (C : ClassMap K N)
variable {κ : ℕ} [NeZero κ]

/-- One-axis coefficient, with `z` the value of `ξ`. -/
def ecoefz (z : K) (k m : ZMod κ) : K :=
  if m = 0 then 0 else if k = 0 then -(z ^ m.val) else if k = m then 1 else 0

/-- `E(y, y') = ∏_r e(y_r, y'_r)`. -/
def Ecoefz (z : K) {ℓ : ℕ} (y y' : Fin ℓ → ZMod κ) : K := ∏ r, ecoefz z (y r) (y' r)

theorem prod_update_ecoef {ℓ : ℕ} (y y' : Fin ℓ → ZMod κ) (r : Fin ℓ) (m : ZMod κ) :
    Ecoefz C.xi (Function.update y r m) y' =
      ecoefz C.xi m (y' r) * ∏ s ∈ Finset.univ.erase r, ecoefz C.xi (y s) (y' s) := by
  unfold Ecoefz
  rw [← Finset.mul_prod_erase Finset.univ _ (Finset.mem_univ r), Function.update_self]
  congr 1
  refine Finset.prod_congr rfl fun s hs => ?_
  rw [Function.update_of_ne (Finset.ne_of_mem_erase hs)]

theorem sum_ecoef (k : ZMod κ) : ∑ m : ZMod κ, C.xiPow m * ecoefz C.xi m k = 0 := by
  by_cases hk : k = 0
  · simp [ecoefz, hk]
  · rw [Fintype.sum_eq_add 0 k (Ne.symm hk)]
    · simp [ecoefz, hk, ClassMap.xiPow]
    · intro x ⟨hx0, hxk⟩
      simp [ecoefz, hk, hx0, hxk]

/-- The families `E(·, y')` satisfy the axis relations. -/
theorem axisRel_E {ℓ : ℕ} (y' : Fin ℓ → ZMod κ) :
    AxisRel C ℓ (fun y => Ecoefz C.xi y y') := by
  intro r y
  simp_rw [prod_update_ecoef C y y' r, smul_eq_mul, ← mul_assoc, ← Finset.sum_mul,
    sum_ecoef C, zero_mul]

/-- **Expansion**: a scalar family with the axis relations is determined by its values at
`y'` without zero coordinate: `X_y = ∑_{y'} X_{y'} E(y, y')`. -/
theorem expand {ℓ : ℕ} (X : (Fin ℓ → ZMod κ) → K) (hX : AxisRel C ℓ X) (y : Fin ℓ → ZMod κ) :
    X y = ∑ y', X y' • Ecoefz C.xi y y' := by
  set Y : (Fin ℓ → ZMod κ) → K := fun y => X y - ∑ y', X y' • Ecoefz C.xi y y' with hY
  have hYax : AxisRel C ℓ Y := by
    intro r y
    have h2 := axisRel_sum C ℓ (fun y' y => Ecoefz C.xi y y') X (fun y' => axisRel_E C y') r y
    simp only [hY, smul_sub, Finset.sum_sub_distrib]
    rw [hX r y, h2, sub_zero]
  have hnz : ∀ y, (∀ r, y r ≠ 0) → Y y = 0 := by
    intro y hy
    simp only [hY]
    rw [Finset.sum_eq_single y, sub_eq_zero]
    · have : Ecoefz C.xi y y = 1 := by
        unfold Ecoefz
        exact Finset.prod_eq_one fun r _ => by simp [ecoefz, hy r]
      rw [this, smul_eq_mul, mul_one]
    · intro y' _ hne
      obtain ⟨r, hr⟩ : ∃ r, y' r ≠ y r := by
        by_contra h; push Not at h; exact hne (funext h)
      have : Ecoefz C.xi y y' = 0 := by
        unfold Ecoefz
        refine Finset.prod_eq_zero (Finset.mem_univ r) ?_
        simp [ecoefz, hy r, Ne.symm hr]
      rw [this, smul_zero]
    · simp
  have := axis_zero_of_nz C ℓ Y hYax hnz y
  simp only [hY, sub_eq_zero] at this
  exact this

/-- **Condition (iii) of `def:plus-ell` is a finite check** (the remark after it). -/
theorem ann_iff_check {ℓ : ℕ} (Ct : (Fin ℓ → ZMod κ) → K) :
    (∀ X : (Fin ℓ → ZMod κ) → K, AxisRel C ℓ X → ∑ y, Ct y * X y = 0) ↔
      ∀ y' : Fin ℓ → ZMod κ, ∑ y, Ct y * Ecoefz C.xi y y' = 0 := by
  constructor
  · intro h y'
    exact h _ (axisRel_E C y')
  · intro h X hX
    have hx : ∑ y, Ct y * X y = ∑ y, Ct y * ∑ y', X y' • Ecoefz C.xi y y' :=
      Finset.sum_congr rfl fun y _ => by rw [← expand C X hX y]
    rw [hx]
    simp_rw [Finset.mul_sum, smul_eq_mul]
    rw [Finset.sum_comm]
    refine Finset.sum_eq_zero fun y' _ => ?_
    simp_rw [mul_left_comm (Ct _) (X y'), ← Finset.mul_sum, h y', mul_zero]

/-- Decidable form of `IsEllContraction` for `Ω = {0}` over a finite field. -/
theorem isEll_zero_iff {K : Type*} [Field K] [Fintype K] [DecidableEq K] {N : ℕ}
    (C : ClassMap K N) {κ : ℕ} [NeZero κ] {h : ℕ} (hκ : κ ∣ N)
    (hκh : κ * h = Fintype.card K - 1) (hh : 0 < h) {ℓ : ℕ} (Ct : (Fin ℓ → ZMod κ) → K) :
    IsEllContraction C ℓ {0} Ct ↔
      ((∀ y, Ct y ≠ 0 → Ct y ^ h = 1) ∧ (Ct 0 ≠ 0 ∧ Ct 0 ^ h = 1) ∧
        ∀ y' : Fin ℓ → ZMod κ, ∑ y, Ct y * Ecoefz C.xi y y' = 0) := by
  constructor
  · rintro ⟨hc, hb, ha⟩
    refine ⟨fun y hy => (C.cl_eq_zero_iff_pow hκ hκh hh hy).mp (hc y hy), ⟨hb.1,
      (ClassMap.mem_pow_iff_pow_eq_one hκh hh hb.1).mp hb⟩, (ann_iff_check C Ct).mp ha⟩
  · rintro ⟨hc, ⟨hb0, hb1⟩, ha⟩
    exact ⟨fun y hy => (C.cl_eq_zero_iff_pow hκ hκh hh hy).mpr (hc y hy),
      (ClassMap.mem_pow_iff_pow_eq_one hκh hh hb0).mpr hb1, (ann_iff_check C Ct).mpr ha⟩

end Expand

section P13

instance fact13 : Fact (Nat.Prime 13) := ⟨by norm_num⟩

/-- `2` as a unit of `F_13`. -/
def g13 : (ZMod 13)ˣ := ZMod.unitOfCoprime 2 (by norm_num)

theorem g13_val : (g13 : ZMod 13) = 2 := by simp [g13]

/-- `2` is a primitive root mod `13` (the least one; `12 = 2^2 · 3`). -/
theorem orderOf_g13 : orderOf g13 = Fintype.card (ZMod 13) - 1 := by
  rw [ZMod.card]
  refine orderOf_eq_of_pow_and_pow_div_prime (by norm_num) ?_ ?_
  · rw [Units.ext_iff, Units.val_pow_eq_pow_val, g13_val, Units.val_one]; decide
  · intro q hq hdvd
    have h12 : q ∣ 2 ^ 2 * 3 := by norm_num; exact hdvd
    rw [Ne, Units.ext_iff, Units.val_pow_eq_pow_val, g13_val, Units.val_one]
    rcases (Nat.Prime.dvd_mul hq).mp h12 with h | h
    · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_two).mp (hq.dvd_of_dvd_pow h)
      decide
    · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_three).mp h
      decide

/-- The class map of `ξ = g = 2` over `F_13`. -/
noncomputable def C13 : ClassMap (ZMod 13) (Fintype.card (ZMod 13) - 1) :=
  ClassMap.ofGen g13 (ClassMap.gen_of_orderOf orderOf_g13) (by rw [ZMod.card]; norm_num)

theorem C13_xi : C13.xi = 2 := g13_val

theorem dvd4_13 : 4 ∣ Fintype.card (ZMod 13) - 1 := by rw [ZMod.card]; norm_num

theorem h4_13 : 4 * 3 = Fintype.card (ZMod 13) - 1 := by rw [ZMod.card]

/-- `B(y)` of `B3_13_4.json`, in the order of the digit strings `y_1 y_2 y_3`. -/
def B134 : List (ZMod 13) :=
  [1, 8, 0, 5, 11, 4, 5, 9, 0, 6, 1, 8, 0, 9, 0, 12, 7, 4, 5, 3, 10, 6, 3, 0, 0, 9, 0, 0, 1,
   0, 0, 5, 0, 0, 1, 8, 2, 1, 11, 4, 1, 0, 4, 0, 11, 0, 0, 1, 0, 0, 0, 12, 9, 8, 4, 2, 11, 10,
   0, 1, 0, 2, 1, 7]

/-- `B(y)` of `B3_13_4_perturbed.json`. -/
def B134pert : List (ZMod 13) :=
  [1, 9, 1, 6, 11, 4, 5, 9, 0, 6, 1, 8, 0, 9, 0, 12, 7, 4, 5, 3, 10, 6, 3, 0, 0, 9, 0, 0, 1,
   0, 0, 5, 0, 0, 1, 8, 2, 1, 11, 4, 1, 0, 4, 0, 11, 0, 0, 1, 0, 0, 0, 12, 9, 8, 4, 2, 11, 10,
   0, 1, 0, 2, 1, 7]

/-- The table `C_y = g^{y_1+y_2+y_3} B(y)` (`g = 2`; integer exponent, as in
`prop:plus-tables`). -/
def tab3 (B : List (ZMod 13)) (y : Fin 3 → ZMod 4) : ZMod 13 :=
  2 ^ ((y 0).val + (y 1).val + (y 2).val) * B.getD (16 * (y 0).val + 4 * (y 1).val + (y 2).val) 0

/-- **The paper's level-3 table at `(p, κ) = (13, 4)` is a `{0}`-contraction** in the sense
of the Lean `IsEllContraction` (Definition `def:plus-ell`). -/
theorem ell3_13_4 : IsEllContraction C13 3 ({0} : Set (ZMod 4)) (tab3 B134) := by
  rw [isEll_zero_iff C13 dvd4_13 h4_13 (by norm_num), C13_xi]
  decide +kernel

/-- Negative control 1: the stored perturbed table is rejected. -/
theorem ell3_13_4_pert : ¬ IsEllContraction C13 3 ({0} : Set (ZMod 4)) (tab3 B134pert) := by
  rw [isEll_zero_iff C13 dvd4_13 h4_13 (by norm_num), C13_xi]
  decide +kernel

/-- Negative control 2: entry `y = (0,0,1)` multiplied by `3 = 2^4` (a 4th power, so every
class is unchanged and (i), (ii) still hold); condition (iii) now fails. -/
theorem ell3_13_4_scaled :
    ¬ IsEllContraction C13 3 ({0} : Set (ZMod 4))
      (fun y => if y = ![0, 0, 1] then 3 * tab3 B134 y else tab3 B134 y) := by
  rw [isEll_zero_iff C13 dvd4_13 h4_13 (by norm_num), C13_xi]
  decide +kernel



variable {V : Type} [AddCommGroup V] [Module (ZMod 13) V] [FiniteDimensional (ZMod 13) V]

/-- **Candidate (e) at `(13, 4)` is a real `4`-solver** of arity `M_3(a)` over `F_13`
(Lemma `lem:plus-ell-node` with the paper's table). -/
theorem ell3_13_4_solver (col : tIdx 4 (Module.finrank (ZMod 13) V) 3 → V) :
    IsRootSol 4 col (rootsOf (rootOf 4)
      (ellNode C13 (Module.finrank (ZMod 13) V) 3 (tab3 B134) col)) :=
  ellSolver_spec C13 dvd4_13 ell3_13_4 (rootOf 4) (fun _ hx => rootOf_pow hx.2) col

#print axioms ell3_13_4
#print axioms ell3_13_4_pert
#print axioms ell3_13_4_scaled
#print axioms ell3_13_4_solver
#print axioms ann_iff_check

end P13

end QSearch.Schedule1HPlus.Review
