import Formal.Schedule1HPlus.Refine
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Real.Basic

/-!
# Schedule 1H⁺, part 6: Lemma `lem:plus-sm`(i), its counting skeleton

Source: `docs/papers/rees-hsp/core/main-core.tex`, Lemma `lem:plus-sm` and its proof.

The paper draws `β_i` (`i ∈ Δ \ {0}`) uniformly, puts `β_0 = 0`, and studies
`n_j = |X_j|`, `X_j = {x ∈ A_{0j} : x + β_i ∈ A_{ij} ∀ i ≠ 0}`. Probabilities over the
uniform `β` are written here as counts over all `β : (Δ \ {0}) → K` (`T = |K|^{r-1}`
of them).

Formalized:

* `rc_of_good` (deterministic core): if every `X_j` is nonempty, any `α_j ∈ X_j` give a
  contraction with every `α_j + β_i ≠ 0` (needs `0 ∈ Ω`).
* `sum_cnt`, `sum_cnt_sq` (first and second moments as exact counts), `sum_cnt_sq_le`
  (the second-moment bound from a **pair-count hypothesis**
  `#{c : x + c ∈ A_i, x' + c ∈ A_i} ≤ γ_i` for `x ≠ x'`; in the paper this is the
  consequence `N_{ij}(u) ≤ γ|A_{ij}|²/p` of Weil's bound), `card_ne_zero_ge`
  (Cauchy–Schwarz: `#{n ≠ 0} · ∑ n² ≥ (∑ n)²`).
* `plus_sm_i`: the count of `β` for which a contraction with all `α_j + β_i ≠ 0` exists
  is at least `T (1 - Φ)` with `Φ = ∑_j (1 - 1/ρ_j)`,
  `ρ_j = T/S_j + T ∏_i γ_{ij} / ∏_i |A_{ij}|²`, `S_j = |A_{0j}| ∏_i |A_{ij}|`
  (= `1/E[n_j] + γ^{r-1}` when `γ_{ij} = γ |A_{ij}|²/p`, as in the paper).

Not formalized: the coset sizes `|A_{00}| = h_D`, `|A_{ij}| = ω h_D` (so `E[n_j] = μ_0`,
`μ_1`), the derivation of the pair-count bound from Weil's bound (the hypothesis), the
monotonicity of `Φ`, and part (ii) (Chebyshev and the sampling rounds).
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset

section Counting

variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- `n(β) = #{x ∈ A_0 : ∀ i, x + β_i ∈ A_i}`. -/
def cnt (A0 : Finset G) (A : I → Finset G) (b : I → G) : ℕ :=
  (A0.filter fun x => ∀ i, x + b i ∈ A i).card

theorem card_translate (x : G) (A : Finset G) :
    (Finset.univ.filter fun c => x + c ∈ A).card = A.card := by
  refine Finset.card_bij' (fun c _ => x + c) (fun y _ => -x + y) ?_ ?_ ?_ ?_
  · intro c hc; simpa using hc
  · intro y hy; simpa using hy
  · intro c _; simp
  · intro y _; simp

theorem card_pi_filter (P : I → G → Prop) [∀ i, DecidablePred (P i)] :
    (Finset.univ.filter fun b : I → G => ∀ i, P i (b i)).card =
      ∏ i, (Finset.univ.filter (P i)).card := by
  rw [← Fintype.card_piFinset]
  congr 1
  ext b
  simp [Fintype.mem_piFinset]

/-- **First moment**: `∑_β n(β) = |A_0| ∏_i |A_i|`. -/
theorem sum_cnt (A0 : Finset G) (A : I → Finset G) :
    ∑ b : I → G, cnt A0 A b = A0.card * ∏ i, (A i).card := by
  simp only [cnt, Finset.card_filter]
  rw [Finset.sum_comm]
  have : ∀ x ∈ A0, (∑ b : I → G, if ∀ i, x + b i ∈ A i then 1 else 0) = ∏ i, (A i).card := by
    intro x _
    rw [← Finset.card_filter, card_pi_filter (fun i c => x + c ∈ A i)]
    simp_rw [card_translate]
  rw [Finset.sum_congr rfl this, Finset.sum_const, smul_eq_mul]

/-- **Second moment** as a sum over ordered pairs. -/
theorem sum_cnt_sq (A0 : Finset G) (A : I → Finset G) :
    ∑ b : I → G, cnt A0 A b ^ 2 =
      ∑ x ∈ A0, ∑ x' ∈ A0, ∏ i, (Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card := by
  have hsq : ∀ b : I → G, cnt A0 A b ^ 2 = ∑ x ∈ A0, ∑ x' ∈ A0,
      (if ∀ i, x + b i ∈ A i ∧ x' + b i ∈ A i then 1 else 0) := by
    intro b
    rw [cnt, Finset.card_filter, sq, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl fun x _ => Finset.sum_congr rfl fun x' _ => ?_
    by_cases h1 : ∀ i, x + b i ∈ A i <;> by_cases h2 : ∀ i, x' + b i ∈ A i <;>
      simp [h1, h2, forall_and]
  rw [Finset.sum_congr rfl fun b _ => hsq b, Finset.sum_comm]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun x' _ => ?_
  rw [← Finset.card_filter, card_pi_filter (fun i c => x + c ∈ A i ∧ x' + c ∈ A i)]

/-- **Second-moment bound from the pair-count hypothesis.** -/
theorem sum_cnt_sq_le (A0 : Finset G) (A : I → Finset G) (γ : I → ℝ) (hγ : ∀ i, 0 ≤ γ i)
    (hN : ∀ i x x', x ≠ x' →
      ((Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card : ℝ) ≤ γ i) :
    ((∑ b : I → G, cnt A0 A b ^ 2 : ℕ) : ℝ) ≤
      (A0.card * ∏ i, (A i).card : ℕ) + (A0.card : ℝ) ^ 2 * ∏ i, γ i := by
  rw [sum_cnt_sq]
  push_cast
  have hdiag : ∀ x ∈ A0, (∑ x' ∈ A0, ∏ i,
      ((Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card : ℝ)) ≤
      ∏ i, ((A i).card : ℝ) + A0.card * ∏ i, γ i := by
    intro x hx
    rw [← Finset.add_sum_erase _ _ hx]
    refine add_le_add (le_of_eq ?_) ?_
    · refine Finset.prod_congr rfl fun i _ => ?_
      simp only [and_self]
      rw [card_translate]
    · calc ∑ x' ∈ A0.erase x, ∏ i,
            ((Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card : ℝ)
          ≤ ∑ x' ∈ A0.erase x, ∏ i, γ i := by
            refine Finset.sum_le_sum fun x' hx' => ?_
            exact Finset.prod_le_prod₀ (fun i _ => Nat.cast_nonneg _)
              (fun i _ => hN i x x' (Finset.ne_of_mem_erase hx').symm)
        _ ≤ A0.card * ∏ i, γ i := by
            rw [Finset.sum_const, nsmul_eq_mul]
            refine mul_le_mul_of_nonneg_right ?_ (Finset.prod_nonneg fun i _ => hγ i)
            exact_mod_cast Finset.card_erase_le
  calc (∑ x ∈ A0, ∑ x' ∈ A0, ∏ i,
        ((Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card : ℝ))
      ≤ ∑ x ∈ A0, (∏ i, ((A i).card : ℝ) + A0.card * ∏ i, γ i) := Finset.sum_le_sum hdiag
    _ = A0.card * ∏ i, ((A i).card : ℝ) + (A0.card : ℝ) ^ 2 * ∏ i, γ i := by
      rw [Finset.sum_const, nsmul_eq_mul]; ring

/-- **Cauchy–Schwarz** (`Pr[n = 0] ≤ 1 - E[n]²/E[n²]`, in counts). -/
theorem card_ne_zero_ge {β : Type*} [Fintype β] (n : β → ℕ) :
    (∑ b, n b) ^ 2 ≤ (Finset.univ.filter fun b => n b ≠ 0).card * ∑ b, n b ^ 2 := by
  have h1 : ∑ b, n b = ∑ b ∈ Finset.univ.filter (fun b => n b ≠ 0), n b := by
    rw [Finset.sum_filter_ne_zero]
  have h2 : ∑ b, n b ^ 2 = ∑ b ∈ Finset.univ.filter (fun b => n b ≠ 0), n b ^ 2 := by
    rw [Finset.sum_filter]
    refine Finset.sum_congr rfl fun b _ => ?_
    split_ifs with h
    · rfl
    · push Not at h; simp [h]
  rw [h1, h2]
  exact sq_sum_le_card_mul_sum_sq

/-- The real-number step of the proof of Lemma `lem:plus-sm`(i). -/
theorem real_step {T a0 PA Pg Gc S1 Q : ℝ} (hT : 0 < T) (ha0 : 0 < a0) (hPA : 0 < PA)
    (hPg : 0 ≤ Pg) (hG0 : 0 ≤ Gc) (hS1 : S1 = a0 * PA) (hcs : S1 ^ 2 ≤ Gc * Q)
    (hQ : Q ≤ a0 * PA + a0 ^ 2 * Pg) :
    T / (T / (a0 * PA) + T * Pg / PA ^ 2) ≤ Gc := by
  subst hS1
  have hkey : (a0 * PA) ^ 2 ≤ Gc * (a0 * PA + a0 ^ 2 * Pg) :=
    hcs.trans (mul_le_mul_of_nonneg_left hQ hG0)
  have hρ : 0 < T / (a0 * PA) + T * Pg / PA ^ 2 := by
    have h1 : 0 < T / (a0 * PA) := div_pos hT (mul_pos ha0 hPA)
    have h2 : 0 ≤ T * Pg / PA ^ 2 := div_nonneg (mul_nonneg hT.le hPg) (sq_nonneg _)
    linarith
  rw [div_le_iff₀ hρ]
  have hexp : Gc * (T / (a0 * PA) + T * Pg / PA ^ 2) =
      T * (Gc * (a0 * PA + a0 ^ 2 * Pg)) / (a0 * PA) ^ 2 := by
    field_simp
  rw [hexp, le_div_iff₀ (by positivity)]
  nlinarith

/-- **Per column**: `#{β : n(β) ≠ 0} ≥ T / ρ`, `ρ = T/S + T ∏γ / (∏|A_i|)²`,
`S = |A_0| ∏ |A_i|` (`T` = number of `β`). -/
theorem good_one (A0 : Finset G) (A : I → Finset G) (γ : I → ℝ) (hγ : ∀ i, 0 ≤ γ i)
    (hN : ∀ i x x', x ≠ x' →
      ((Finset.univ.filter fun c => x + c ∈ A i ∧ x' + c ∈ A i).card : ℝ) ≤ γ i)
    (hS : 0 < A0.card * ∏ i, (A i).card) :
    (Fintype.card (I → G) : ℝ) / ((Fintype.card (I → G) : ℝ) /
        ((A0.card : ℝ) * ∏ i, ((A i).card : ℝ)) +
        (Fintype.card (I → G) : ℝ) * (∏ i, γ i) / (∏ i, ((A i).card : ℝ)) ^ 2) ≤
      ((Finset.univ.filter fun b => cnt A0 A b ≠ 0).card : ℝ) := by
  have hT : (0 : ℝ) < (Fintype.card (I → G) : ℝ) := Nat.cast_pos.mpr Fintype.card_pos
  have ha0 : (0 : ℝ) < (A0.card : ℝ) := Nat.cast_pos.mpr (Nat.pos_of_mul_pos_right hS)
  have hPA : (0 : ℝ) < ∏ i, ((A i).card : ℝ) := by
    have h' : 0 < ∏ i, (A i).card := Nat.pos_of_mul_pos_left hS
    rw [← Nat.cast_prod]; exact Nat.cast_pos.mpr h'
  have hS1 : ((∑ b, cnt A0 A b : ℕ) : ℝ) = (A0.card : ℝ) * ∏ i, ((A i).card : ℝ) := by
    rw [sum_cnt]; push_cast; rfl
  have hcs : ((∑ b, cnt A0 A b : ℕ) : ℝ) ^ 2 ≤
      ((Finset.univ.filter fun b => cnt A0 A b ≠ 0).card : ℝ) *
        ((∑ b, cnt A0 A b ^ 2 : ℕ) : ℝ) := by
    exact_mod_cast card_ne_zero_ge (cnt A0 A)
  have hQ := sum_cnt_sq_le A0 A γ hγ hN
  have hQ' : ((∑ b : I → G, cnt A0 A b ^ 2 : ℕ) : ℝ) ≤
      (A0.card : ℝ) * (∏ i, ((A i).card : ℝ)) + (A0.card : ℝ) ^ 2 * ∏ i, γ i := by
    have : ((A0.card * ∏ i, (A i).card : ℕ) : ℝ) = (A0.card : ℝ) * ∏ i, ((A i).card : ℝ) := by
      push_cast; rfl
    rw [this] at hQ; exact hQ
  exact real_step hT ha0 hPA (Finset.prod_nonneg fun i _ => hγ i) (Nat.cast_nonneg _) hS1 hcs hQ'

/-- **Union bound** over finitely many columns `j`. -/
theorem good_count {J : Type*} [Fintype J] (A0 : J → Finset G) (A : J → I → Finset G)
    (γ : J → I → ℝ) (hγ : ∀ j i, 0 ≤ γ j i)
    (hN : ∀ j i x x', x ≠ x' →
      ((Finset.univ.filter fun c => x + c ∈ A j i ∧ x' + c ∈ A j i).card : ℝ) ≤ γ j i)
    (hS : ∀ j, 0 < (A0 j).card * ∏ i, (A j i).card) :
    (Fintype.card (I → G) : ℝ) * (1 - ∑ j, (1 - 1 / ((Fintype.card (I → G) : ℝ) /
        (((A0 j).card : ℝ) * ∏ i, ((A j i).card : ℝ)) +
        (Fintype.card (I → G) : ℝ) * (∏ i, γ j i) / (∏ i, ((A j i).card : ℝ)) ^ 2))) ≤
      ((Finset.univ.filter fun b => ∀ j, cnt (A0 j) (A j) b ≠ 0).card : ℝ) := by
  set T : ℝ := (Fintype.card (I → G) : ℝ)
  set ρ : J → ℝ := fun j => T / (((A0 j).card : ℝ) * ∏ i, ((A j i).card : ℝ)) +
    T * (∏ i, γ j i) / (∏ i, ((A j i).card : ℝ)) ^ 2
  have hsplit : ∀ (P : (I → G) → Prop) [DecidablePred P],
      ((Finset.univ.filter P).card : ℝ) + ((Finset.univ.filter fun b => ¬ P b).card : ℝ) = T := by
    intro P _
    have := Finset.card_filter_add_card_filter_not (s := (Finset.univ : Finset (I → G))) P
    have h2 : ((Finset.univ : Finset (I → G)).card : ℝ) = T := by simp [T]
    rw [← h2]
    exact_mod_cast this
  have hbad : ∀ j, ((Finset.univ.filter fun b => ¬ cnt (A0 j) (A j) b ≠ 0).card : ℝ) ≤
      T * (1 - 1 / ρ j) := by
    intro j
    have h1 := good_one (A0 j) (A j) (γ j) (hγ j) (hN j) (hS j)
    have h2 := hsplit (fun b => cnt (A0 j) (A j) b ≠ 0)
    have : T * (1 - 1 / ρ j) = T - T / ρ j := by ring
    rw [this]; linarith
  have hU : (Finset.univ.filter fun b : I → G => ¬ ∀ j, cnt (A0 j) (A j) b ≠ 0) ⊆
      Finset.univ.biUnion fun j => Finset.univ.filter fun b => ¬ cnt (A0 j) (A j) b ≠ 0 := by
    intro b hb
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, not_forall] at hb
    obtain ⟨j, hj⟩ := hb
    exact Finset.mem_biUnion.mpr ⟨j, Finset.mem_univ _, by simpa using hj⟩
  have h1 : ((Finset.univ.filter fun b : I → G => ¬ ∀ j, cnt (A0 j) (A j) b ≠ 0).card : ℝ) ≤
      ∑ j, ((Finset.univ.filter fun b => ¬ cnt (A0 j) (A j) b ≠ 0).card : ℝ) := by
    exact_mod_cast (Finset.card_le_card hU).trans Finset.card_biUnion_le
  have h2 := hsplit (fun b => ∀ j, cnt (A0 j) (A j) b ≠ 0)
  have h3 : ∑ j, ((Finset.univ.filter fun b => ¬ cnt (A0 j) (A j) b ≠ 0).card : ℝ) ≤
      T * ∑ j, (1 - 1 / ρ j) := by
    rw [Finset.mul_sum]; exact Finset.sum_le_sum fun j _ => hbad j
  have : T * (1 - ∑ j, (1 - 1 / ρ j)) = T - T * ∑ j, (1 - 1 / ρ j) := by ring
  rw [this]
  linarith

end Counting

section Contraction

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K] {N : ℕ} (C : ClassMap K N)

/-- `I = Δ \ {0}`. -/
abbrev DI {D : ℕ} (Δ : Finset (ZMod D)) := {i // i ∈ Δ.erase 0}

/-- `β` on `Δ`, with `β_0 = 0`. -/
def betaFull {D : ℕ} {Δ : Finset (ZMod D)} (b : DI Δ → K) (i : ZMod D) : K :=
  if h : i ∈ Δ.erase 0 then b ⟨i, h⟩ else 0

/-- The paper's `A_{0j}` (`A_{00} = Q_0`). -/
def A0set (D : ℕ) (Ω : Set (ZMod D)) [DecidablePred (· ∈ Ω)] (j : ZMod D) : Finset K :=
  Finset.univ.filter fun x => x ≠ 0 ∧ (if j = 0 then C.cl D x = 0 else C.cl D x + j ∈ Ω)

/-- The paper's `A_{ij}`, `i ≠ 0`: `⋃_{k ∈ Ω} Q_{k-i-j}`. -/
def Aset (D : ℕ) (Ω : Set (ZMod D)) [DecidablePred (· ∈ Ω)] (i j : ZMod D) : Finset K :=
  Finset.univ.filter fun x => x ≠ 0 ∧ C.cl D x + i + j ∈ Ω

/-- **Deterministic core of Lemma `lem:plus-sm`**: if `α_j ∈ X_j` for every `j`, then
`(α, β)` is a contraction with every `α_j + β_i` nonzero. -/
theorem rc_of_good {D : ℕ} (hD : D ∣ N) {Δ : Finset (ZMod D)} {Ω : Set (ZMod D)}
    [DecidablePred (· ∈ Ω)] (h0Ω : (0 : ZMod D) ∈ Ω) (_h0Δ : (0 : ZMod D) ∈ Δ)
    (b : DI Δ → K) (α : ZMod D → K)
    (hα : ∀ j, α j ∈ A0set C D Ω j ∧ ∀ i : DI Δ, α j + b i ∈ Aset C D Ω i.1 j) :
    IsRC C D ↑Δ Ω α (betaFull b) ∧ ∀ i ∈ Δ, ∀ j, α j + betaFull b i ≠ 0 := by
  have hb0 : betaFull b 0 = 0 := by simp [betaFull]
  have hcase : ∀ i ∈ Δ, ∀ j, α j + betaFull b i ≠ 0 ∧
      C.cl D (α j + betaFull b i) + i + j ∈ Ω := by
    intro i hi j
    by_cases hi0 : i = 0
    · subst hi0
      have h1 := (hα j).1
      simp only [A0set, Finset.mem_filter, Finset.mem_univ, true_and] at h1
      rw [hb0, add_zero, add_zero]
      refine ⟨h1.1, ?_⟩
      by_cases hj : j = 0
      · rw [if_pos hj] at h1; subst hj; rw [add_zero, h1.2]; exact h0Ω
      · rw [if_neg hj] at h1; exact h1.2
    · have hmem : i ∈ Δ.erase 0 := Finset.mem_erase.mpr ⟨hi0, hi⟩
      have h1 := (hα j).2 ⟨i, hmem⟩
      simp only [Aset, Finset.mem_filter, Finset.mem_univ, true_and] at h1
      have hbi : betaFull b i = b ⟨i, hmem⟩ := by simp [betaFull, hmem]
      rw [hbi]
      exact h1
  refine ⟨⟨?_, fun i hi j => Or.inr (hcase i hi j).2⟩, fun i hi j => (hcase i hi j).1⟩
  have h1 := (hα 0).1
  simp only [A0set, Finset.mem_filter, Finset.mem_univ, true_and, ite_true] at h1
  rw [hb0, add_zero]
  exact (C.cl_eq_zero_iff hD h1.1).mp h1.2

/-- `n_j(β)` for the paper's sets. -/
def nj (D : ℕ) (Δ : Finset (ZMod D)) (Ω : Set (ZMod D)) [DecidablePred (· ∈ Ω)]
    (j : ZMod D) (b : DI Δ → K) : ℕ :=
  cnt (A0set C D Ω j) (fun i : DI Δ => Aset C D Ω i.1 j) b

/-- **Lemma `lem:plus-sm`(i), counting form, from the pair-count hypothesis.** With
`T = |K|^{|Δ|-1}` choices of `β`, `S_j = |A_{0j}| ∏_i |A_{ij}| > 0`, and
`#{c : x + c, x' + c ∈ A_{ij}} ≤ γ_{ij}` for `x ≠ x'`, there is a set of at least
`T (1 - Φ)` choices of `β`, `Φ = ∑_j (1 - 1/ρ_j)`, `ρ_j = T/S_j + T ∏_i γ_{ij} /
(∏_i |A_{ij}|)²`, for each of which some `α` gives a contraction with every
`α_j + β_i ≠ 0`. -/
theorem plus_sm_i {D : ℕ} (hD : D ∣ N) {Δ : Finset (ZMod D)} {Ω : Set (ZMod D)}
    [DecidablePred (· ∈ Ω)] (h0Ω : (0 : ZMod D) ∈ Ω) (h0Δ : (0 : ZMod D) ∈ Δ)
    (γ : ZMod D → DI Δ → ℝ) (hγ : ∀ j i, 0 ≤ γ j i)
    (hN : ∀ j (i : DI Δ) (x x' : K), x ≠ x' →
      ((Finset.univ.filter fun c => x + c ∈ Aset C D Ω i.1 j ∧ x' + c ∈ Aset C D Ω i.1 j).card
        : ℝ) ≤ γ j i)
    (hS : ∀ j, 0 < (A0set C D Ω j).card * ∏ i : DI Δ, (Aset C D Ω i.1 j).card) :
    haveI := C.neZero_of_dvd hD
    ∃ s : Finset (DI Δ → K),
      (∀ b ∈ s, ∃ α : ZMod D → K, IsRC C D ↑Δ Ω α (betaFull b) ∧
        ∀ i ∈ Δ, ∀ j, α j + betaFull b i ≠ 0) ∧
      (Fintype.card (DI Δ → K) : ℝ) * (1 - ∑ j : ZMod D, (1 - 1 /
        ((Fintype.card (DI Δ → K) : ℝ) /
          (((A0set C D Ω j).card : ℝ) * ∏ i : DI Δ, ((Aset C D Ω i.1 j).card : ℝ)) +
        (Fintype.card (DI Δ → K) : ℝ) * (∏ i, γ j i) /
          (∏ i : DI Δ, ((Aset C D Ω i.1 j).card : ℝ)) ^ 2))) ≤ (s.card : ℝ) := by
  haveI := C.neZero_of_dvd hD
  refine ⟨Finset.univ.filter fun b => ∀ j, nj C D Δ Ω j b ≠ 0, ?_,
    good_count (fun j => A0set C D Ω j) (fun j (i : DI Δ) => Aset C D Ω i.1 j) γ hγ hN hS⟩
  intro b hb
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hb
  have hex : ∀ j, ∃ x, x ∈ A0set C D Ω j ∧ ∀ i : DI Δ, x + b i ∈ Aset C D Ω i.1 j := by
    intro j
    obtain ⟨x, hx⟩ := Finset.card_pos.mp (Nat.pos_of_ne_zero (hb j))
    simp only [Finset.mem_filter] at hx
    exact ⟨x, hx⟩
  choose α hα using hex
  exact ⟨α, rc_of_good C hD h0Ω h0Δ b α hα⟩

end Contraction

end QSearch.Schedule1HPlus
