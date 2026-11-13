import Formal.Schedule1H.Levels
import Mathlib.FieldTheory.Finite.Basic

/-!
# Schedule 1H, part 3: Lemma `lem:stage` and the coset test over a finite field

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:halving`: the paragraph
before Lemma `lem:stage` (`P_D = P ∪ qP` for `q^h = -1`, `ε = -q^{-1}`, the test
`x^h = ±1`) and Lemma `lem:stage`.

* `stageRun D q cls rt Dsol v` is the stage call: one call `r' = Dsol v` of the
  `D`-solver, `x_ν = r'_ν^D`, the coset test `cls`, the root oracle `rt`, and the split
  into `I` (roots `ρ`) and `J` (roots `σ` of `x_ν / q`). If `I = ∅` it returns `(σ, 0)`.
* `StageOK κ D q cls rt` is the specification of the test and the roots (`κ = 2D`, and
  for every `x = r^D ≠ 0`: if `cls x` then `rt x` is a `κ`-th root of `x`, otherwise
  `rt (x / q)` is a `κ`-th root of `x / q`).
* `stageRun_stepSpec`: under `StageOK`, every stage answer satisfies
  `StepSpec κ ε` with `ε = -q⁻¹`. With `step_spec` this is **Lemma `lem:stage`**
  (`stage_spec`).
* Over a finite field `K` with `κ ∣ |K| - 1`, `h = (|K| - 1)/κ`, `κ = 2D` and any `q` with
  `q^h = -1`, the paper's test `cls x = (x^h = 1)` and any root function `rootOf κ`
  satisfy `StageOK` (`ff_stageOK`). The key facts are `exists_root_of_pow_eq_one`
  (`x ≠ 0`, `x^h = 1` implies `x ∈ P`; cyclicity of `K^×`) and
  `pow_h_eq_one_or_neg_one` (`x ∈ P_D` implies `x^h = ±1`).
* `exists_q`: such a `q` exists in odd characteristic (`q = θ^D` for a non-square `θ`).
-/

namespace QSearch.Schedule1H

open Finset

variable {K : Type*} [Field K] [DecidableEq K]

section Abstract

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- **The stage call** (proof of Lemma `lem:stage`). -/
def stageRun (D : ℕ) (q : K) (cls : K → Bool) (rt : K → K) {N : ℕ}
    (Dsol : (Fin N → V) → Fin N → K) (v : Fin N → V) : (Fin N → K) × (Fin N → K) :=
  let x : Fin N → K := fun ν => Dsol v ν ^ D
  let ρ : Fin N → K := fun ν => if x ν ≠ 0 ∧ cls (x ν) = true then rt (x ν) else 0
  let σ : Fin N → K := fun ν => if x ν ≠ 0 ∧ cls (x ν) = false then rt (x ν / q) else 0
  if ∀ ν, ρ ν = 0 then (σ, 0) else (ρ, σ)

/-- Specification of the coset test and of the root oracle at degree `κ = 2D`. -/
def StageOK (κ D : ℕ) (q : K) (cls : K → Bool) (rt : K → K) : Prop :=
  κ = 2 * D ∧ 0 < D ∧ q ≠ 0 ∧
    ∀ r : K, r ≠ 0 →
      (cls (r ^ D) = true → rt (r ^ D) ^ κ = r ^ D) ∧
      (cls (r ^ D) = false → rt (r ^ D / q) ^ κ = r ^ D / q)

theorem stageRun_stepSpec {κ D : ℕ} {q : K} {cls : K → Bool} {rt : K → K}
    (hok : StageOK κ D q cls rt) {N : ℕ} (Dsol : (Fin N → V) → Fin N → K) (v : Fin N → V)
    (hD : IsRootSol D v (Dsol v)) :
    StepSpec κ (-q⁻¹) v (stageRun D q cls rt Dsol v).1 (stageRun D q cls rt Dsol v).2 := by
  obtain ⟨hκD, hD0, hq, hrt⟩ := hok
  have hκ : 0 < κ := by omega
  set x : Fin N → K := fun ν => Dsol v ν ^ D with hx
  set ρ : Fin N → K := fun ν => if x ν ≠ 0 ∧ cls (x ν) = true then rt (x ν) else 0 with hρ
  set σ : Fin N → K := fun ν => if x ν ≠ 0 ∧ cls (x ν) = false then rt (x ν / q) else 0
    with hσ
  -- the pointwise identity `x = ρ^κ + q σ^κ`
  have hpt : ∀ ν, x ν = ρ ν ^ κ + q * σ ν ^ κ := by
    intro ν
    by_cases h0 : x ν = 0
    · simp [ρ, σ, h0, zero_pow hκ.ne']
    · have hr : Dsol v ν ≠ 0 := fun h => h0 (by simp [x, h, zero_pow hD0.ne'])
      cases hc : cls (x ν)
      · have := (hrt _ hr).2 hc
        simp only [ρ, σ, h0, hc, ne_eq, not_false_eq_true, true_and, Bool.false_eq_true,
          and_false, ite_false, ite_true]
        rw [this, zero_pow hκ.ne', zero_add]
        field_simp
        rfl
      · have := (hrt _ hr).1 hc
        simp only [ρ, σ, h0, hc, ne_eq, not_false_eq_true, true_and, ite_true,
          Bool.true_eq_false, and_false, ite_false]
        rw [this, zero_pow hκ.ne', mul_zero, add_zero]
  have hdisj : ∀ ν, ρ ν = 0 ∨ σ ν = 0 := by
    intro ν
    by_cases hc : cls (x ν) = true
    · right; simp [σ, hc]
    · left; simp [ρ, hc]
  have hsum : ∑ ν, ρ ν ^ κ • v ν + q • ∑ ν, σ ν ^ κ • v ν = 0 := by
    rw [Finset.smul_sum, ← Finset.sum_add_distrib, ← hD.2]
    refine Finset.sum_congr rfl fun ν _ => ?_
    rw [smul_smul, ← add_smul, ← hpt ν]
  have hrel : ∑ ν, σ ν ^ κ • v ν = -q⁻¹ • ∑ ν, ρ ν ^ κ • v ν := by
    have h2 : q • ∑ ν, σ ν ^ κ • v ν = -∑ ν, ρ ν ^ κ • v ν := eq_neg_of_add_eq_zero_right hsum
    have h3 := congrArg (fun y => q⁻¹ • y) h2
    simp only [smul_smul, inv_mul_cancel₀ hq, one_smul, smul_neg] at h3
    rw [h3, neg_smul]
  -- some `x ν ≠ 0`
  obtain ⟨ν0, hν0⟩ : ∃ ν, x ν ≠ 0 := by
    by_contra h
    push Not at h
    apply hD.1
    funext ν
    have := h ν
    simpa [x, pow_eq_zero_iff hD0.ne'] using this
  have hstage : stageRun D q cls rt Dsol v = if ∀ ν, ρ ν = 0 then (σ, 0) else (ρ, σ) := rfl
  rw [hstage]
  split_ifs with hall
  · -- `I = ∅`: return `(σ, 0)`
    have hρ0 : ∑ ν, ρ ν ^ κ • v ν = 0 := by simp [hall, zero_pow hκ.ne']
    refine ⟨fun h => ?_, fun _ => Or.inr rfl, ?_⟩
    · have h1 := hpt ν0
      rw [hall ν0, show σ ν0 = 0 from congrFun h ν0] at h1
      simp [zero_pow hκ.ne'] at h1
      exact hν0 h1
    · rw [hρ0, smul_zero] at hrel
      simp [hrel, zero_pow hκ.ne']
  · exact ⟨fun h => hall fun ν => congrFun h ν, hdisj, hrel⟩

variable {ι τ : Type*} [Fintype ι] [DecidableEq τ]

/-- **Lemma `lem:stage`.** Let `κ = 2D` with the test and roots as specified, let
`o_1, …, o_N` be objects of type `c` (disjoint supports: column type `Fin N × ι`), and let
`Dsol` be a `D`-solver call that returns a `D`-solution on the vectors `v_ν`. Then one
stage returns either a `κ`-solution or an object of type `(c, εc)`, `ε = -q⁻¹`. -/
theorem stage_spec {κ D : ℕ} {q : K} {cls : K → Bool} {rt : K → K}
    (hok : StageOK κ D q cls rt) {N : ℕ} (Dsol : (Fin N → V) → Fin N → K) (k0 : τ)
    (col : Fin N × ι → V) (c : τ → K) (o : Fin N → Obj ι τ V K)
    (ho : ∀ ν, IsObj κ (fun i => col (ν, i)) c (o ν))
    (hD : IsRootSol D (fun ν => (o ν).v) (Dsol fun ν => (o ν).v)) :
    ResOK κ col (extType c (-q⁻¹))
      (step κ k0 o (stageRun D q cls rt Dsol fun ν => (o ν).v).1
        (stageRun D q cls rt Dsol fun ν => (o ν).v).2) := by
  have hκ : 0 < κ := by obtain ⟨h1, h2, _⟩ := hok; omega
  have hq : q ≠ 0 := hok.2.2.1
  exact step_spec hκ k0 col c (neg_ne_zero.mpr (inv_ne_zero hq)) o ho _ _
    (stageRun_stepSpec hok Dsol _ hD)

end Abstract

section FiniteField

variable [Fintype K]

/-- **Cyclicity**: if `κ h = |K| - 1`, `h > 0`, `x ≠ 0` and `x ^ h = 1`, then `x` is a
`κ`-th power (the paper's "`x ∈ P` exactly when `x^h = 1`", direction `⇐`). -/
theorem exists_root_of_pow_eq_one {κ h : ℕ} (hκh : κ * h = Fintype.card K - 1) (hh : 0 < h)
    {x : K} (hx : x ≠ 0) (hxh : x ^ h = 1) : ∃ r : K, r ^ κ = x := by
  obtain ⟨g, hg⟩ := IsCyclic.exists_generator (α := Kˣ)
  have hord : orderOf g = Fintype.card K - 1 := by
    rw [orderOf_eq_card_of_forall_mem_zpowers hg, Nat.card_eq_fintype_card,
      Fintype.card_units]
  obtain ⟨m, hm⟩ : ∃ m : ℕ, g ^ m = Units.mk0 x hx :=
    mem_powers_iff_mem_zpowers.mpr (hg (Units.mk0 x hx))
  have h1 : g ^ (m * h) = 1 := by
    rw [pow_mul, hm]
    ext
    simp [hxh]
  rw [← orderOf_dvd_iff_pow_eq_one, hord, ← hκh] at h1
  obtain ⟨k, rfl⟩ := Nat.dvd_of_mul_dvd_mul_right hh h1
  refine ⟨((g ^ k : Kˣ) : K), ?_⟩
  rw [← Units.val_pow_eq_pow_val, ← pow_mul, mul_comm, hm, Units.val_mk0]

omit [DecidableEq K] in
/-- The converse: a nonzero `κ`-th power satisfies `x ^ h = 1`. -/
theorem pow_eq_one_of_root {κ h : ℕ} (hκh : κ * h = Fintype.card K - 1) {r : K}
    (hr : r ≠ 0) : (r ^ κ) ^ h = 1 := by
  rw [← pow_mul, hκh]
  exact FiniteField.pow_card_sub_one_eq_one r hr

omit [DecidableEq K] in
/-- For `x = r^D ≠ 0` with `2 D h = |K| - 1`: `x ^ h = 1` or `x ^ h = -1`
(the paper's "for `x ∈ P_D`, `x^h = ±1`"). -/
theorem pow_h_eq_one_or_neg_one {D h : ℕ} (hDh : 2 * D * h = Fintype.card K - 1) {r : K}
    (hr : r ≠ 0) : (r ^ D) ^ h = 1 ∨ (r ^ D) ^ h = -1 := by
  have h2 : ((r ^ D) ^ h) ^ 2 = 1 := by
    rw [← pow_mul, ← pow_mul, show D * (h * 2) = 2 * D * h by ring, hDh]
    exact FiniteField.pow_card_sub_one_eq_one r hr
  exact mul_self_eq_one_iff.mp (by rw [← pow_two]; exact h2)


/-- A root function: some `κ`-th root of `x` if one exists, else `0` (the paper uses
tables or Las Vegas root finding; any function with this property will do). -/
noncomputable def rootOf (κ : ℕ) (x : K) : K :=
  if h : ∃ r : K, r ^ κ = x then Classical.choose h else 0

theorem rootOf_pow {κ : ℕ} {x : K} (h : ∃ r : K, r ^ κ = x) : rootOf κ x ^ κ = x := by
  unfold rootOf
  rw [dite_eq_left h]
  exact Classical.choose_spec h

/-- The paper's coset test: `x ∈ P` iff `x ^ h = 1`. -/
def powTest (h : ℕ) (x : K) : Bool := decide (x ^ h = 1)

/-- **The paper's test and roots meet `StageOK`.** Over a finite field with
`2 D h = |K| - 1`, `h > 0`, and `q ^ h = -1`. -/
theorem ff_stageOK {D h : ℕ} (hD : 0 < D) (hDh : 2 * D * h = Fintype.card K - 1)
    (hh : 0 < h) {q : K} (hq : q ^ h = -1) :
    StageOK (2 * D) D q (powTest h) (rootOf (2 * D)) := by
  have hq0 : q ≠ 0 := by
    rintro rfl
    rw [zero_pow hh.ne'] at hq
    exact one_ne_zero (neg_eq_zero.mp hq.symm)
  refine ⟨rfl, hD, hq0, fun r hr => ⟨fun hc => ?_, fun hc => ?_⟩⟩
  · have h1 : (r ^ D) ^ h = 1 := by simpa [powTest] using hc
    exact rootOf_pow (exists_root_of_pow_eq_one hDh hh (pow_ne_zero _ hr) h1)
  · have h1 : (r ^ D) ^ h = -1 :=
      (pow_h_eq_one_or_neg_one hDh hr).resolve_left (by simpa [powTest] using hc)
    have h2 : (r ^ D / q) ^ h = 1 := by
      rw [div_pow, h1, hq, div_self (neg_ne_zero.mpr one_ne_zero)]
    exact rootOf_pow (exists_root_of_pow_eq_one hDh hh (div_ne_zero (pow_ne_zero _ hr) hq0) h2)

omit [DecidableEq K] in
/-- **Existence of `q`** (paper: "`q = θ^D` for a quadratic nonresidue `θ`"): in odd
characteristic, with `2 D h = |K| - 1`, some `q` has `q ^ h = -1`. -/
theorem exists_q (hK : ringChar K ≠ 2) {D h : ℕ} (hDh : 2 * D * h = Fintype.card K - 1) :
    ∃ q : K, q ^ h = -1 := by
  obtain ⟨θ, hθ⟩ := FiniteField.exists_nonsquare hK
  have hθ0 : θ ≠ 0 := by rintro rfl; exact hθ ⟨0, by simp⟩
  have hodd := FiniteField.odd_card_of_char_ne_two hK
  have h2 : 2 * (D * h) = Fintype.card K - 1 := by rw [← hDh]; ring
  have hhalf : Fintype.card K / 2 = D * h := by omega
  have hne : θ ^ (D * h) ≠ 1 := by
    rw [← hhalf]; exact fun h1 => hθ ((FiniteField.isSquare_iff hK hθ0).mpr h1)
  refine ⟨θ ^ D, ?_⟩
  rw [← pow_mul]
  rcases pow_h_eq_one_or_neg_one hDh hθ0 with h1 | h1
  · rw [← pow_mul] at h1; exact absurd h1 hne
  · rwa [← pow_mul] at h1

omit [DecidableEq K] [Fintype K] in
/-- The paper's other choice: `q = -1` when `h` is odd. -/
theorem neg_one_pow_odd {h : ℕ} (hh : Odd h) : (-1 : K) ^ h = -1 := hh.neg_one_pow

end FiniteField

end QSearch.Schedule1H
