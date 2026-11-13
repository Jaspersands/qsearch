import Formal.Schedule1H.Halving
import Formal.Schedule1H.TwoTerm
import Formal.ReesSdeWitness

/-!
# Schedule 1H, part 6: the paper's arity `A_κ(a)`, choice rule and Theorem `thm:halving`

Source: `docs/papers/rees-hsp/core/main-core.tex`, the definition of `t_{p,κ}` after
`eq:Bd`, the sets `T_j`, Definition `def:schedule1h` and Theorem `thm:halving`(i),(ii).

Over a finite field `K` (the paper: `K = 𝔽_p`, `p` an odd prime):

* `tMin K κ` is `t_{p,κ}` (least `t` with a nonzero zero sum of `t` `κ`-th powers);
  `zeroSums_nonempty` (Chevalley–Warning, via `ReesSdeWitness.exists_witness`) shows the
  least element exists for `κ ≥ 1`.
* `Tsets κ q s = T(c^{(s)})` with `ε = -q⁻¹`.
* `Admissible κ q s f1`: `s ≥ 1`, and if `|K| < 4κ^4` then `0 ∈ T_s` (F0) or
  `T_s ⊇ K^×` (F1); if `|K| ≥ 4κ^4` only `(1, F1)`.
* `Apaper qf κ a` is `A_κ(a)`: `a + 1` for `κ ≤ 1`, otherwise the least arity among
  candidate (a), `G(κ,a)^{⌈log₂ t_{p,κ}⌉}`, and the admissible plans (for even `κ`),
  `A_{κ/2}(a)^s n_F(a)` (an `sInf` over a nonempty set of naturals, hence attained).
* `paperChoice`: run (a) if it attains `A_κ(a)`, else the plan of least `s` attaining it,
  preferring F0 (the paper's tie rule).
* `paperPrep qf`: `q = qf κ`, the test `x^h = 1`, a root function, a zero sum of length
  `t_{p,κ}`, the imported collision algorithm, and F0/F1 tables (chosen from
  admissibility).

Results.

* `Apaper_le_rounds`: `A_κ(a) ≤ G(κ,a)^{⌈log₂ t_{p,κ}⌉}` for `κ ≥ 2` (inequality of
  `thm:halving`(i)).
* `paper_arity_eq`: the arity of the candidate `paperChoice` runs is `A_κ(a)`.
* `halving_correct` (**Theorem `thm:halving`(ii), correctness**): for `κ ∣ |K| - 1`,
  given the imported collision step at every degree `κ' ∣ κ` with `κ' ≥ 2`, an element
  `q` with `q^h = -1` at every even `κ' ∣ κ`, and `T_1 ⊇ K^×` at every even `κ' ∣ κ` with
  `|K| ≥ 4κ'^4`, the solver `H (paperPrep qf) (paperChoice qf) κ` is a `κ`-solver of
  arity `A_κ(a)`.
* `halving_correct_weil`: the same with the last hypothesis replaced by Weil's bound
  (`WeilLower`, via Lemma `lem:two-term`), and `q` supplied by `exists_q` in odd
  characteristic.
-/

namespace QSearch.Schedule1H

open Finset

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K]

variable (K) in
/-- The lengths of nonzero zero sums of `κ`-th powers. -/
def ZeroSums (κ : ℕ) : Set ℕ := {t | ∃ z : Fin t → K, z ≠ 0 ∧ ∑ i, z i ^ κ = 0}

variable (K) in
/-- `t_{p,κ}`. -/
noncomputable def tMin (κ : ℕ) : ℕ := sInf (ZeroSums K κ)

/-- Chevalley–Warning: `κ + 1` terms always admit a nonzero zero sum. -/
theorem zeroSums_nonempty {κ : ℕ} (hκ : 0 < κ) : (ZeroSums K κ).Nonempty := by
  obtain ⟨s, hs, hsum⟩ := QSearch.ReesSdeWitness.exists_witness (K := K) (M := κ + 1)
    (a := 1) hκ (by omega) (fun _ _ => 1)
  refine ⟨κ + 1, s, hs, ?_⟩
  have := congrFun hsum 0
  simpa using this

theorem tMin_mem {κ : ℕ} (hκ : 0 < κ) : tMin K κ ∈ ZeroSums K κ :=
  Nat.sInf_mem (zeroSums_nonempty hκ)

/-- The sets `T_s = T(c^{(s)})`, `ε = -q⁻¹`. -/
def Tsets (κ : ℕ) (q : K) (s : ℕ) : Set K := Tset κ (cTyp (-q⁻¹) s)

/-- **Admissibility** of a plan `(s, F)` (Definition `def:schedule1h`(b)). -/
def Admissible (κ : ℕ) (q : K) (s : ℕ) (f1 : Bool) : Prop :=
  1 ≤ s ∧
    (Fintype.card K < 4 * κ ^ 4 →
      (f1 = true → ∀ x : K, x ≠ 0 → x ∈ Tsets κ q s) ∧ (f1 = false → (0 : K) ∈ Tsets κ q s)) ∧
    (4 * κ ^ 4 ≤ Fintype.card K → s = 1 ∧ f1 = true)

/-- **The paper's arity `A_κ(a)`** (Definition `def:schedule1h`): least arity of a
candidate. `qf κ` is the element `q` used at degree `κ`. -/
noncomputable def Apaper (qf : ℕ → K) (κ a : ℕ) : ℕ :=
  if h : κ ≤ 1 then a + 1 else
    sInf (insert (Garity κ a ^ Nat.clog 2 (tMin K κ))
      {n | ∃ s f1, Even κ ∧ Admissible κ (qf κ) s f1 ∧ n = Apaper qf (κ / 2) a ^ s * nF f1 a})
termination_by κ
decreasing_by omega

/-- **Theorem `thm:halving`(i), inequality.** -/
theorem Apaper_le_rounds (qf : ℕ → K) {κ : ℕ} (hκ : 2 ≤ κ) (a : ℕ) :
    Apaper qf κ a ≤ Garity κ a ^ Nat.clog 2 (tMin K κ) := by
  rw [Apaper, dif_neg (by omega)]
  exact Nat.sInf_le (Set.mem_insert _ _)

/-- `A_κ(a)` is attained: either by candidate (a) or by an admissible plan. -/
theorem Apaper_mem (qf : ℕ → K) {κ : ℕ} (hκ : 2 ≤ κ) (a : ℕ) :
    Apaper qf κ a = Garity κ a ^ Nat.clog 2 (tMin K κ) ∨
      ∃ s f1, Even κ ∧ Admissible κ (qf κ) s f1 ∧
        Apaper qf κ a = Apaper qf (κ / 2) a ^ s * nF f1 a := by
  have h : Apaper qf κ a ∈ insert (Garity κ a ^ Nat.clog 2 (tMin K κ))
      {n | ∃ s f1, Even κ ∧ Admissible κ (qf κ) s f1 ∧ n = Apaper qf (κ / 2) a ^ s * nF f1 a} := by
    have he := Apaper.eq_1 qf κ a
    rw [dif_neg (by omega)] at he
    rw [he]
    exact Nat.sInf_mem ⟨_, Set.mem_insert _ _⟩
  rcases h with h | h
  · exact Or.inl h
  · exact Or.inr h

open Classical in
/-- **The paper's choice**: candidate (a) if it attains `A_κ(a)`; otherwise the plan of
least `s` attaining it, with F0 preferred to F1. -/
noncomputable def paperChoice (qf : ℕ → K) (κ a : ℕ) : Cand :=
  if Apaper qf κ a = Garity κ a ^ Nat.clog 2 (tMin K κ) then .rounds
  else if h : ∃ s f1, Even κ ∧ Admissible κ (qf κ) s f1 ∧
      Apaper qf κ a = Apaper qf (κ / 2) a ^ s * nF f1 a then
    if Even κ ∧ Admissible κ (qf κ) (Nat.find h) false ∧
        Apaper qf κ a = Apaper qf (κ / 2) a ^ (Nat.find h) * nF false a then
      .plan (Nat.find h) false
    else .plan (Nat.find h) true
  else .rounds

theorem paperChoice_spec (qf : ℕ → K) {κ : ℕ} (hκ : 2 ≤ κ) (a : ℕ) :
    (paperChoice qf κ a = .rounds ∧ Apaper qf κ a = Garity κ a ^ Nat.clog 2 (tMin K κ)) ∨
      ∃ s f1, paperChoice qf κ a = .plan s f1 ∧ Even κ ∧ Admissible κ (qf κ) s f1 ∧
        Apaper qf κ a = Apaper qf (κ / 2) a ^ s * nF f1 a := by
  classical
  by_cases hr : Apaper qf κ a = Garity κ a ^ Nat.clog 2 (tMin K κ)
  · left
    refine ⟨?_, hr⟩
    unfold paperChoice
    rw [if_pos hr]
  · right
    have hp := (Apaper_mem qf hκ a).resolve_left hr
    have hs := Nat.find_spec hp
    by_cases h0 : Even κ ∧ Admissible κ (qf κ) (Nat.find hp) false ∧
        Apaper qf κ a = Apaper qf (κ / 2) a ^ (Nat.find hp) * nF false a
    · refine ⟨Nat.find hp, false, ?_, h0⟩
      unfold paperChoice
      rw [if_neg hr, dif_pos hp, if_pos h0]
    · refine ⟨Nat.find hp, true, ?_, ?_⟩
      · unfold paperChoice
        rw [if_neg hr, dif_pos hp, if_neg h0]
      · obtain ⟨f1, hf1⟩ := hs
        cases f1 with
        | false => exact absurd hf1 h0
        | true => exact hf1

open Classical in
/-- **The paper's preprocessing** at degree `κ`. -/
noncomputable def paperPrep (qf : ℕ → K) (κ : ℕ) : Prep K κ where
  t := tMin K κ
  z := if h : tMin K κ ∈ ZeroSums K κ then Classical.choose h else 0
  isRun a v := if h : Nonempty (ISOut κ v) then (Classical.choice h).rs else (0, 0)
  q := qf κ
  cls := powTest ((Fintype.card K - 1) / κ)
  rt := rootOf κ
  f0 s := if h : ∃ ρ : Typ s → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * cTyp (-(qf κ)⁻¹) s k = 0
    then Classical.choose h else 0
  f1 s x := if h : ∃ ρ : Typ s → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * cTyp (-(qf κ)⁻¹) s k = x
    then Classical.choose h else 0

theorem paperPrep_z (qf : ℕ → K) {κ : ℕ} (hκ : 0 < κ) :
    (paperPrep qf κ).z ≠ 0 ∧ ∑ i, (paperPrep qf κ).z i ^ κ = 0 := by
  classical
  have hmem := tMin_mem (K := K) hκ
  have : (paperPrep qf κ).z = Classical.choose hmem := by
    simp only [paperPrep]; rw [dif_pos hmem]
  rw [this]
  exact Classical.choose_spec hmem

theorem paperPrep_isRun (qf : ℕ → K) {κ a : ℕ} (v : Fin (Garity κ a) → Fin a → K)
    (hne : Nonempty (ISOut κ v)) : ∃ o : ISOut κ v, (paperPrep qf κ).isRun a v = o.rs := by
  classical
  refine ⟨Classical.choice hne, ?_⟩
  simp only [paperPrep]; rw [dif_pos hne]

theorem paperPrep_f0 (qf : ℕ → K) {κ s : ℕ}
    (hex : ∃ ρ : Typ s → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * cTyp (-(qf κ)⁻¹) s k = 0) :
    (paperPrep qf κ).f0 s ≠ 0 ∧
      ∑ k, (paperPrep qf κ).f0 s k ^ κ * cTyp (-(qf κ)⁻¹) s k = 0 := by
  classical
  have : (paperPrep qf κ).f0 s = Classical.choose hex := by
    simp only [paperPrep]; rw [dif_pos hex]
  rw [this]
  exact Classical.choose_spec hex

theorem paperPrep_f1 (qf : ℕ → K) {κ s : ℕ} {x : K}
    (hex : ∃ ρ : Typ s → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * cTyp (-(qf κ)⁻¹) s k = x) :
    (paperPrep qf κ).f1 s x ≠ 0 ∧
      ∑ k, (paperPrep qf κ).f1 s x k ^ κ * cTyp (-(qf κ)⁻¹) s k = x := by
  classical
  have : (paperPrep qf κ).f1 s x = Classical.choose hex := by
    simp only [paperPrep]; rw [dif_pos hex]
  rw [this]
  exact Classical.choose_spec hex

/-- The arity of the candidate that `paperChoice` runs is `A_κ(a)`. -/
theorem paper_arity_eq (qf : ℕ → K) :
    ∀ κ a, arity (paperPrep qf) (paperChoice qf) κ a = Apaper qf κ a := by
  intro κ
  induction κ using Nat.strong_induction_on with
  | _ κ ih =>
  intro a
  by_cases h1 : κ ≤ 1
  · rw [arity, dif_pos h1, Apaper, dif_pos h1]
  · rw [arity, dif_neg h1]
    rcases paperChoice_spec qf (by omega : 2 ≤ κ) a with ⟨hc, he⟩ | ⟨s, f1, hc, _, _, he⟩
    · rw [hc, he]; rfl
    · rw [hc, he]
      show arity (paperPrep qf) (paperChoice qf) (κ / 2) a ^ s * nF f1 a = _
      rw [ih (κ / 2) (by omega) a]

/-- **Theorem `thm:halving`(ii), correctness, with the paper's arity and choice.**
Let `κ ≥ 1` divide `|K| - 1`. Assume: at every degree `κ' ∣ κ` with `κ' ≥ 2` the imported
collision step (Theorem `thm:is-import`) has an output on every input (`hIS`); at every
even `κ' ∣ κ`, `q = qf κ'` satisfies `q^h = -1` with `h = (|K| - 1)/κ'` (`hq`); and at
every even `κ' ∣ κ` with `|K| ≥ 4κ'^4`, `T_1 ⊇ K^×` (`hT1`; this is Lemma
`lem:two-term`). Then on all `n ≥ A_κ(a)` columns in `K^a`, `H_κ` returns `r ≠ 0` with
`∑ r_b^κ λ_b = 0`, i.e. the `κ`-solution `(r^κ, r)`. -/
theorem halving_correct (qf : ℕ → K) {κ : ℕ} (hκ : 0 < κ) (hκQ : κ ∣ Fintype.card K - 1)
    (hq : ∀ κ', κ' ∣ κ → Even κ' → qf κ' ^ ((Fintype.card K - 1) / κ') = -1)
    (hIS : ∀ κ', κ' ∣ κ → 2 ≤ κ' → ∀ a (v : Fin (Garity κ' a) → Fin a → K),
      Nonempty (ISOut κ' v))
    (hT1 : ∀ κ', κ' ∣ κ → Even κ' → 4 * κ' ^ 4 ≤ Fintype.card K →
      ∀ x : K, x ≠ 0 → x ∈ Tsets κ' (qf κ') 1) :
    IsKSolver κ (Apaper qf κ) (H (paperPrep qf) (paperChoice qf) κ) := by
  have hQ1 : 1 < Fintype.card K := Fintype.one_lt_card
  have key := H_spec (paperPrep qf) (paperChoice qf) κ hκ (fun κ' a hdiv h2 => ?_)
  · have heq : arity (paperPrep qf) (paperChoice qf) κ = Apaper qf κ :=
      funext (paper_arity_eq qf κ)
    rwa [heq] at key
  have hκ'0 : 0 < κ' := by omega
  rcases paperChoice_spec qf h2 a with ⟨hc, _⟩ | ⟨s, f1, hc, hev, hadm, _⟩
  · rw [hc]
    obtain ⟨hz0, hz⟩ := paperPrep_z qf hκ'0
    exact ⟨hz0, hz, fun a' v => paperPrep_isRun qf v (hIS κ' hdiv h2 a' v)⟩
  · rw [hc]
    -- the stage specification
    have hdvdQ : κ' ∣ Fintype.card K - 1 := hdiv.trans hκQ
    have hD : 2 * (κ' / 2) = κ' := by obtain ⟨m, hm⟩ := hev; omega
    have hh : κ' * ((Fintype.card K - 1) / κ') = Fintype.card K - 1 :=
      Nat.mul_div_cancel' hdvdQ
    have hhpos : 0 < (Fintype.card K - 1) / κ' := by
      apply Nat.div_pos (Nat.le_of_dvd (by omega) hdvdQ) hκ'0
    have hst : StageOK κ' (κ' / 2) (qf κ') (powTest ((Fintype.card K - 1) / κ')) (rootOf κ') := by
      have := ff_stageOK (K := K) (D := κ' / 2) (h := (Fintype.card K - 1) / κ') (by omega)
        (by rw [hD]; exact hh) hhpos (hq κ' hdiv hev)
      rwa [hD] at this
    refine ⟨hst, ?_⟩
    -- the finisher tables
    have hT : ∀ x : K, (∃ ρ : Typ s → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ' * cTyp (-(qf κ')⁻¹) s k = x) ↔
        x ∈ Tsets κ' (qf κ') s := fun x => (mem_Tset_iff hκ'0 _ x).symm
    obtain ⟨_, hsmall, hbig⟩ := hadm
    cases f1 with
    | true =>
      simp only [ite_true]
      intro x hx
      have hxT : x ∈ Tsets κ' (qf κ') s := by
        by_cases hQ : Fintype.card K < 4 * κ' ^ 4
        · exact (hsmall hQ).1 rfl x hx
        · have := hbig (by omega)
          rw [this.1]
          exact hT1 κ' hdiv hev (by omega) x hx
      exact paperPrep_f1 qf ((hT x).mpr hxT)
    | false =>
      simp only [Bool.false_eq_true, ite_false]
      have hQ : Fintype.card K < 4 * κ' ^ 4 := by
        by_contra hQ
        have := (hbig (by omega)).2
        exact Bool.false_ne_true this
      exact paperPrep_f0 qf ((hT 0).mpr ((hsmall hQ).2 rfl))

/-- **Theorem `thm:halving`(ii) with Lemma `lem:two-term` discharged by Weil's bound**,
and `q` supplied in odd characteristic: if `ringChar K ≠ 2`, `κ ∣ |K| - 1`, the imported
collision step holds at every `κ' ∣ κ` with `κ' ≥ 2`, and `WeilLower K κ'` holds at every
even `κ' ∣ κ` with `|K| ≥ 4κ'^4`, then for some choice of `q`'s the solver
`H (paperPrep qf) (paperChoice qf) κ` is a `κ`-solver of arity `Apaper qf κ`. -/
theorem halving_correct_weil (hK : ringChar K ≠ 2) {κ : ℕ} (hκ : 0 < κ)
    (hκQ : κ ∣ Fintype.card K - 1)
    (hIS : ∀ κ', κ' ∣ κ → 2 ≤ κ' → ∀ a (v : Fin (Garity κ' a) → Fin a → K),
      Nonempty (ISOut κ' v))
    (hW : ∀ κ', κ' ∣ κ → Even κ' → 4 * κ' ^ 4 ≤ Fintype.card K → WeilLower K κ') :
    ∃ qf : ℕ → K, (∀ κ', κ' ∣ κ → Even κ' → qf κ' ^ ((Fintype.card K - 1) / κ') = -1) ∧
      IsKSolver κ (Apaper qf κ) (H (paperPrep qf) (paperChoice qf) κ) := by
  classical
  have hex : ∀ κ', ∃ q : K, κ' ∣ κ → Even κ' → q ^ ((Fintype.card K - 1) / κ') = -1 := by
    intro κ'
    by_cases hc : κ' ∣ κ ∧ Even κ'
    · obtain ⟨hdiv, hev⟩ := hc
      have hdvdQ : κ' ∣ Fintype.card K - 1 := hdiv.trans hκQ
      have hD : 2 * (κ' / 2) = κ' := by obtain ⟨m, hm⟩ := hev; omega
      obtain ⟨q, hq⟩ := exists_q (K := K) hK (D := κ' / 2) (h := (Fintype.card K - 1) / κ')
        (by rw [hD]; exact Nat.mul_div_cancel' hdvdQ)
      exact ⟨q, fun _ _ => hq⟩
    · exact ⟨0, fun h1 h2 => absurd ⟨h1, h2⟩ hc⟩
  choose qf hqf using hex
  refine ⟨qf, hqf, halving_correct qf hκ hκQ hqf hIS fun κ' hdiv hev hQ x hx => ?_⟩
  have hκ'0 : 0 < κ' := by
    rcases Nat.eq_zero_or_pos κ' with h | h
    · subst h; exact absurd (Nat.eq_zero_of_zero_dvd hdiv) (by omega)
    · exact h
  have hq0 : qf κ' ≠ 0 := by
    intro h0
    have := hqf κ' hdiv hev
    rw [h0, zero_pow] at this
    · exact one_ne_zero (neg_eq_zero.mp this.symm)
    · have hdvdQ : κ' ∣ Fintype.card K - 1 := hdiv.trans hκQ
      have hQ1 : 1 < Fintype.card K := Fintype.one_lt_card
      exact (Nat.div_pos (Nat.le_of_dvd (by omega) hdvdQ) hκ'0).ne'
  obtain ⟨ρ, hρ, hsum⟩ := two_term_mem_T1 hκ'0 (hW κ' hdiv hev hQ)
    (neg_ne_zero.mpr (inv_ne_zero hq0)) hx hQ
  exact (mem_Tset_iff hκ'0 _ x).mpr ⟨ρ, hρ, hsum⟩

end QSearch.Schedule1H
