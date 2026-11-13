import Formal.Schedule1H.Stage

/-!
# Schedule 1H, part 4: Definition `def:schedule1h` and Theorem `thm:halving`(ii)

Source: `docs/papers/rees-hsp/core/main-core.tex`, Definition `def:schedule1h` and
Theorem `thm:halving` (Section `sec:halving`).

**Layer 1 (any choice, any preprocessing).** `H prep ch κ` is the recursive solver of
Definition `def:schedule1h`, for an arbitrary choice `ch κ a` of candidate at each degree
and each `a`, and arbitrary preprocessing `prep κ` (zero sum, imported collision
algorithm, `q`, coset test, roots, F0/F1 tables). `arity prep ch κ a` is the arity of the
candidate it runs. `H_spec`: if every candidate chosen at a degree `κ' ∣ κ`, `κ' ≥ 2`,
meets its specification (`CandOK`), then `H prep ch κ` is a `κ`-solver of arity
`arity prep ch κ` (Theorem `thm:halving`(ii), correctness).

**Layer 2 (the paper's choice).** Over a finite field `K`, `tMin κ` is `t_{p,κ}`,
`Tsets κ q s` is `T_s`, `Admissible` is the paper's admissibility rule, `Apaper qf κ a` is
`A_κ(a)` (least arity of a candidate), `paperChoice` runs a candidate of least arity
with the paper's tie rule, and `paperPrep` is the preprocessing (`q = qf κ`, the test
`x^h = 1`, a root function, tables chosen from admissibility). `halving_correct`:
`H (paperPrep qf) (paperChoice qf) κ` is a `κ`-solver of arity `A_κ` for every
`κ ∣ |K| - 1`, given (1) the imported collision step at every degree `κ' ∣ κ`, (2) `q` with
`q^h = -1` at every even `κ' ∣ κ`, and (3) `T_1 ⊇ K^×` at every even `κ' ∣ κ` with
`|K| ≥ 4κ'^4` (this is Lemma `lem:two-term`, proved from Weil's bound in
`Formal.Schedule1H.TwoTerm`). `arity_le_rounds` is the inequality of `thm:halving`(i).

Not formalized: running time, Las Vegas behaviour and the expected-time recursion of
`thm:halving`(ii), `thm:halving`(i) computability, `thm:halving`(iii).
-/

namespace QSearch.Schedule1H

open Finset

/-- A candidate of Definition `def:schedule1h`: (a) `rounds` (Lemma `lem:rounds`), or
(H) the plan `(s, F)`, with `f1 = true` for `F = F1`. -/
inductive Cand
  | rounds
  | plan (s : ℕ) (f1 : Bool)

/-- `n_F(a)`: `n_{F0} = 1`, `n_{F1} = a + 1`. -/
def nF (f1 : Bool) (a : ℕ) : ℕ := if f1 then a + 1 else 1

variable {K : Type*} [Field K] [DecidableEq K]

/-- The preprocessing at degree `κ`. -/
structure Prep (K : Type*) (κ : ℕ) where
  /-- length of the zero sum -/
  t : ℕ
  /-- the zero sum of `κ`-th powers -/
  z : Fin t → K
  /-- the imported collision algorithm (Theorem `thm:is-import`) at arity `G(κ, a)` -/
  isRun : (a : ℕ) → (Fin (Garity κ a) → Fin a → K) →
    (Fin (Garity κ a) → K) × (Fin (Garity κ a) → K)
  /-- the element `q` with `q^h = -1` -/
  q : K
  /-- coset test (`x ∈ P`?) -/
  cls : K → Bool
  /-- `κ`-th roots -/
  rt : K → K
  /-- F0 table: a root vector `y` with `∑ y_k^κ c^{(s)}_k = 0` -/
  f0 : (s : ℕ) → Typ s → K
  /-- F1 table: root vectors `y` with `∑ y_k^κ c^{(s)}_k = x` -/
  f1 : (s : ℕ) → K → Typ s → K

/-- The arity of the candidate that `H` runs (`A_D(a)^s n_F(a)` for a plan). -/
def arity (prep : (κ : ℕ) → Prep K κ) (ch : ℕ → ℕ → Cand) (κ a : ℕ) : ℕ :=
  if h : κ ≤ 1 then a + 1 else
    match ch κ a with
    | .rounds => Garity κ a ^ Nat.clog 2 (prep κ).t
    | .plan s f1 => arity prep ch (κ / 2) a ^ s * nF f1 a
termination_by κ
decreasing_by omega

/-- **The solver `H_κ` of Definition `def:schedule1h`.** `κ ≤ 1`: Gaussian elimination
(`kernelVec`) on the first `a + 1` columns. `κ ≥ 2`: run the chosen candidate on the
first `arity` columns (zeros elsewhere); a plan calls `H_{κ/2}` at arity
`A = arity (κ/2) a` inside each stage. -/
def H (prep : (κ : ℕ) → Prep K κ) (ch : ℕ → ℕ → Cand) (κ a n : ℕ)
    (col : Fin n → Fin a → K) : Fin n → K :=
  if _h : κ ≤ 1 then
    padRun (N := a + 1) (fun c => (QSearch.ReesSdeSolver.kernelVec a (a + 1) c).get) col
  else
    match ch κ a with
    | .rounds => padRun (onFin (levEquiv _ _) (roundsBlock κ ((prep κ).isRun a) (prep κ).z)) col
    | .plan s f1 =>
      let orc := stageRun (κ / 2) (prep κ).q (prep κ).cls (prep κ).rt
        (H prep ch (κ / 2) a (arity prep ch (κ / 2) a))
      if f1 then
        padRun (onFin (planF1Equiv (arity prep ch (κ / 2) a) a s)
          (planF1 κ orc s ((prep κ).f1 s))) col
      else
        padRun (onFin (levEquiv (arity prep ch (κ / 2) a) s)
          (planF0 κ orc s ((prep κ).f0 s))) col
termination_by κ
decreasing_by omega

/-- Specification of a chosen candidate at degree `κ`, with `ε = -q⁻¹`. -/
def CandOK (κ : ℕ) (P : Prep K κ) : Cand → Prop
  | .rounds => P.z ≠ 0 ∧ ∑ i, P.z i ^ κ = 0 ∧ ∀ a v, ∃ o : ISOut κ v, P.isRun a v = o.rs
  | .plan s f1 => StageOK κ (κ / 2) P.q P.cls P.rt ∧
      if f1 then ∀ x : K, x ≠ 0 → P.f1 s x ≠ 0 ∧ ∑ k, P.f1 s x k ^ κ * cTyp (-P.q⁻¹) s k = x
      else P.f0 s ≠ 0 ∧ ∑ k, P.f0 s k ^ κ * cTyp (-P.q⁻¹) s k = 0

/-- **Theorem `thm:halving`(ii), correctness, for any choice and preprocessing.** If
every candidate chosen at every degree `κ' ∣ κ` with `κ' ≥ 2` meets its specification,
then `H prep ch κ` is a `κ`-solver of arity `arity prep ch κ`: on every `n ≥ arity κ a`
columns in `K^a` it returns `r ≠ 0` with `∑ r_b^κ λ_b = 0`. -/
theorem H_spec (prep : (κ : ℕ) → Prep K κ) (ch : ℕ → ℕ → Cand) :
    ∀ κ : ℕ, 0 < κ → (∀ κ' a, κ' ∣ κ → 2 ≤ κ' → CandOK κ' (prep κ') (ch κ' a)) →
      IsKSolver κ (arity prep ch κ) (H prep ch κ) := by
  intro κ
  induction κ using Nat.strong_induction_on with
  | _ κ ih =>
  intro hκ hok a n col hn
  by_cases h1 : κ ≤ 1
  · have hκ1 : κ = 1 := by omega
    subst hκ1
    rw [arity, dite_eq_left h1] at hn
    rw [H, dite_eq_left h1]
    refine padRun_spec (by norm_num) _ col hn ?_
    obtain ⟨hne, hsum⟩ := QSearch.ReesSdeSolver.kernelVec_spec a (a + 1)
      (fun j => col (Fin.castLE hn j)) (Nat.lt_succ_self a)
    exact ⟨hne, by simpa using hsum⟩
  · have hκ2 : 2 ≤ κ := by omega
    rw [arity, dite_eq_right h1] at hn
    rw [H, dite_eq_right h1]
    have hc0 := hok κ a dvd_rfl hκ2
    revert hn hc0
    cases ch κ a with
    | rounds =>
      intro hn hc0
      obtain ⟨hz0, hz, hIS⟩ := hc0
      exact rounds_spec hκ _ (hIS a) _ hz0 hz hn col
    | plan s f1 =>
      intro hn hc0
      obtain ⟨hst, hfin⟩ := hc0
      have hκD : κ = 2 * (κ / 2) := hst.1
      have hD0 : 0 < κ / 2 := hst.2.1
      have hq : (prep κ).q ≠ 0 := hst.2.2.1
      have hε : -(prep κ).q⁻¹ ≠ 0 := neg_ne_zero.mpr (inv_ne_zero hq)
      have ihD : IsKSolver (κ / 2) (arity prep ch (κ / 2)) (H prep ch (κ / 2)) :=
        ih (κ / 2) (by omega) hD0 fun κ' a' hκ' h2 =>
          hok κ' a' (hκ'.trans ⟨2, by omega⟩) h2
      have horc : ∀ v : Fin (arity prep ch (κ / 2) a) → Fin a → K,
          StepSpec κ (-(prep κ).q⁻¹) v
            (stageRun (κ / 2) (prep κ).q (prep κ).cls (prep κ).rt
              (H prep ch (κ / 2) a (arity prep ch (κ / 2) a)) v).1
            (stageRun (κ / 2) (prep κ).q (prep κ).cls (prep κ).rt
              (H prep ch (κ / 2) a (arity prep ch (κ / 2) a)) v).2 :=
        fun v => stageRun_stepSpec hst _ v (ihD a _ v le_rfl)
      cases f1 with
      | true =>
        simp only [ite_true]
        simp only [nF, ite_true] at hn
        refine padRun_spec hκ _ col hn (onFin_spec _ _ (fun col' => ?_) _)
        exact planF1_spec hκ hε _ horc s _ hfin col'
      | false =>
        simp only [Bool.false_eq_true, ite_false]
        simp only [nF, Bool.false_eq_true, ite_false, mul_one] at hn
        refine padRun_spec hκ _ col hn (onFin_spec _ _ (fun col' => ?_) _)
        simp only [Bool.false_eq_true, ite_false] at hfin
        exact planF0_spec hκ hε _ horc s _ hfin.1 hfin.2 col'

end QSearch.Schedule1H
