import Formal.Schedule1H.Levels
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# Schedule 1H, part 5: Lemma `lem:two-term`, conditional on Weil's bound

Source: `docs/papers/rees-hsp/core/main-core.tex`, Lemma `lem:two-term`.

Weil's bound for diagonal equations is not in Mathlib. It enters as the hypothesis
`WeilLower K κ`, the lower half of the paper's `|N - p| ≤ (κ-1)^2 √p` (only this half is
used): for all `ε, η ≠ 0`, the number `N` of `(u, v) ∈ K²` with `u^κ + ε v^κ = η` is at
least `|K| - (κ-1)^2 √|K|`. Everything else in the proof is checked:

* `card_pow_eq_le`: `X^κ = c` has at most `κ` roots.
* `two_term_count`: if `|K| ≥ 4κ^4` (and `κ ≥ 1`), then
  `2κ · #{u ∈ K^× : ∃ v ≠ 0, η - u^κ = ε v^κ} ≥ |K|` (the paper's "at least `p/(2κ)`
  elements"; the set is the paper's `{u : η - u^κ ∈ εP}` with `u ≠ 0`).
* `two_term_mem_T1`: hence `η ∈ P + εP ⊆ T_1 = T((1, ε))` for every `η ≠ 0`.

The "probability at least `1/(2κ)`" is the count divided by `|K| - 1`; it is not
restated.
-/

namespace QSearch.Schedule1H

open Finset

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K]

/-- `X^κ = c` has at most `κ` solutions. -/
theorem card_pow_eq_le {κ : ℕ} (hκ : 0 < κ) (c : K) :
    #{v : K | v ^ κ = c} ≤ κ := by
  calc #{v : K | v ^ κ = c} ≤ (Polynomial.nthRoots κ c).toFinset.card := by
        apply Finset.card_le_card
        intro v hv
        simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hv
        simpa [Multiset.mem_toFinset, Polynomial.mem_nthRoots hκ] using hv
    _ ≤ Multiset.card (Polynomial.nthRoots κ c) := Multiset.toFinset_card_le _
    _ ≤ κ := Polynomial.card_nthRoots κ c

/-- **The lower half of Weil's bound** for `u^κ + ε v^κ = η` (hypothesis, not proved). -/
def WeilLower (K : Type*) [Field K] [Fintype K] [DecidableEq K] (κ : ℕ) : Prop :=
  ∀ ε η : K, ε ≠ 0 → η ≠ 0 →
    (Fintype.card K : ℝ) - ((κ : ℝ) - 1) ^ 2 * Real.sqrt (Fintype.card K) ≤
      (#{x : K × K | x.1 ^ κ + ε * x.2 ^ κ = η} : ℝ)

/-- The paper's set `{u ∈ K^× : η - u^κ ∈ εP}`. -/
def goodU (κ : ℕ) (ε η : K) : Finset K :=
  {u : K | u ≠ 0 ∧ ∃ v : K, v ≠ 0 ∧ η - u ^ κ = ε * v ^ κ}

/-- Counting step of the proof (no Weil yet): `N ≤ κ · #goodU + 2κ`. -/
theorem card_sol_le {κ : ℕ} (hκ : 0 < κ) {ε η : K} (hε : ε ≠ 0) :
    #{x : K × K | x.1 ^ κ + ε * x.2 ^ κ = η} ≤ κ * #(goodU κ ε η) + 2 * κ := by
  set S := (Finset.univ : Finset (K × K)).filter fun x => x.1 ^ κ + ε * x.2 ^ κ = η
  have hsplit : S ⊆ S.filter (fun x => x.1 ≠ 0 ∧ x.2 ≠ 0) ∪
      ((S.filter fun x => x.1 = 0) ∪ (S.filter fun x => x.2 = 0)) := by
    intro x hx
    by_cases h1 : x.1 = 0
    · simp [hx, h1]
    · by_cases h2 : x.2 = 0
      · simp [hx, h2]
      · simp [hx, h1, h2]
  have hA : #(S.filter fun x => x.1 ≠ 0 ∧ x.2 ≠ 0) ≤ κ * #(goodU κ ε η) := by
    refine card_le_mul_card_image_of_maps_to (f := Prod.fst) ?_ κ ?_
    · intro x hx
      simp only [S, Finset.mem_filter, Finset.mem_univ, true_and] at hx
      simp only [goodU, Finset.mem_filter, Finset.mem_univ, true_and]
      exact ⟨hx.2.1, x.2, hx.2.2, by rw [← hx.1]; ring⟩
    · intro u _
      calc #{x ∈ S.filter (fun x => x.1 ≠ 0 ∧ x.2 ≠ 0) | x.1 = u}
          ≤ #((Finset.univ.filter fun v : K => v ^ κ = (η - u ^ κ) / ε).map
              (Function.Embedding.sectR u K)) := by
            apply Finset.card_le_card
            intro x hx
            simp only [S, Finset.mem_filter, Finset.mem_univ, true_and] at hx
            simp only [Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
              Function.Embedding.sectR_apply]
            refine ⟨x.2, ?_, ?_⟩
            · rw [eq_div_iff hε, ← hx.2, ← hx.1.1]; ring
            · rw [← hx.2]
        _ ≤ κ := by rw [Finset.card_map]; exact card_pow_eq_le hκ _
  have hB : #(S.filter fun x => x.1 = 0) ≤ κ := by
    calc #(S.filter fun x => x.1 = 0)
        ≤ #((Finset.univ.filter fun v : K => v ^ κ = η / ε).map
            (Function.Embedding.sectR (0 : K) K)) := by
          apply Finset.card_le_card
          intro x hx
          simp only [S, Finset.mem_filter, Finset.mem_univ, true_and] at hx
          simp only [Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
            Function.Embedding.sectR_apply]
          refine ⟨x.2, ?_, ?_⟩
          · rw [eq_div_iff hε, ← hx.1, hx.2, zero_pow hκ.ne']; ring
          · rw [← hx.2]
      _ ≤ κ := by rw [Finset.card_map]; exact card_pow_eq_le hκ _
  have hC : #(S.filter fun x => x.2 = 0) ≤ κ := by
    calc #(S.filter fun x => x.2 = 0)
        ≤ #((Finset.univ.filter fun u : K => u ^ κ = η).map
            (Function.Embedding.sectL K (0 : K))) := by
          apply Finset.card_le_card
          intro x hx
          simp only [S, Finset.mem_filter, Finset.mem_univ, true_and] at hx
          simp only [Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
            Function.Embedding.sectL_apply]
          refine ⟨x.1, ?_, ?_⟩
          · rw [← hx.1, hx.2, zero_pow hκ.ne']; ring
          · rw [← hx.2]
      _ ≤ κ := by rw [Finset.card_map]; exact card_pow_eq_le hκ _
  calc #S ≤ #(S.filter (fun x => x.1 ≠ 0 ∧ x.2 ≠ 0) ∪
        ((S.filter fun x => x.1 = 0) ∪ (S.filter fun x => x.2 = 0))) := card_le_card hsplit
    _ ≤ #(S.filter (fun x => x.1 ≠ 0 ∧ x.2 ≠ 0)) +
        (#(S.filter fun x => x.1 = 0) + #(S.filter fun x => x.2 = 0)) :=
        (card_union_le _ _).trans (by gcongr; exact card_union_le _ _)
    _ ≤ κ * #(goodU κ ε η) + 2 * κ := by omega

/-- **Lemma `lem:two-term`, counting form**, conditional on `WeilLower K κ`: if
`κ ≥ 1`, `ε, η ≠ 0` and `|K| ≥ 4κ^4`, then at least `|K|/(2κ)` elements `u ∈ K^×` satisfy
`η - u^κ ∈ εP`. -/
theorem two_term_count {κ : ℕ} (hκ : 0 < κ) (hW : WeilLower K κ) {ε η : K} (hε : ε ≠ 0)
    (hη : η ≠ 0) (hQ : 4 * κ ^ 4 ≤ Fintype.card K) :
    Fintype.card K ≤ 2 * κ * #(goodU κ ε η) := by
  have hN := hW ε η hε hη
  have hc := card_sol_le (K := K) hκ (η := η) hε
  set Q : ℝ := (Fintype.card K : ℝ)
  set U : ℝ := ((#(goodU κ ε η) : ℕ) : ℝ)
  set N : ℝ := ((#{x : K × K | x.1 ^ κ + ε * x.2 ^ κ = η} : ℕ) : ℝ)
  set k : ℝ := (κ : ℝ)
  have hcR : N ≤ k * U + 2 * k := by
    have : ((#{x : K × K | x.1 ^ κ + ε * x.2 ^ κ = η} : ℕ) : ℝ) ≤
        ((κ * #(goodU κ ε η) + 2 * κ : ℕ) : ℝ) := by exact_mod_cast hc
    simpa [N, k, U] using this
  have hk1 : (1 : ℝ) ≤ k := by simp only [k]; exact_mod_cast hκ
  have hQ0 : (0 : ℝ) ≤ Q := by positivity
  set s := Real.sqrt Q with hs
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hss : s * s = Q := Real.mul_self_sqrt hQ0
  have hQR : 4 * k ^ 4 ≤ Q := by simp only [k, Q]; exact_mod_cast hQ
  have hs2 : 2 * k ^ 2 ≤ s := by
    rw [hs]
    apply Real.le_sqrt_of_sq_le
    nlinarith
  -- `Q/2 ≥ (κ-1)^2 s + 2κ`
  have key : Q / 2 ≥ (k - 1) ^ 2 * s + 2 * k := by
    have h1 : s * s ≥ 2 * k ^ 2 * s := by nlinarith
    have h2 : (2 * k - 1) * s ≥ 2 * k := by nlinarith
    nlinarith
  have hfin : Q ≤ 2 * k * U := by nlinarith
  have : ((Fintype.card K : ℕ) : ℝ) ≤ ((2 * κ * #(goodU κ ε η) : ℕ) : ℝ) := by
    simpa [Q, k, U] using hfin
  exact_mod_cast this

/-- **Lemma `lem:two-term`, consequence**: under the same hypotheses `η ∈ P + εP`, so
`η ∈ T_1 = T((1, ε))`, i.e. `η = ρ_1^κ · 1 + ρ_2^κ · ε` with `ρ ≠ 0` (`ρ = (u, v)`). -/
theorem two_term_mem_T1 {κ : ℕ} (hκ : 0 < κ) (hW : WeilLower K κ) {ε η : K} (hε : ε ≠ 0)
    (hη : η ≠ 0) (hQ : 4 * κ ^ 4 ≤ Fintype.card K) :
    ∃ ρ : Typ 1 → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * cTyp ε 1 k = η := by
  have hcount := two_term_count hκ hW hε hη hQ
  have hpos : 0 < #(goodU κ ε η) := by
    rcases Nat.eq_zero_or_pos #(goodU κ ε η) with h | h
    · rw [h, mul_zero] at hcount
      exact absurd hcount (by have := Fintype.card_pos (α := K); omega)
    · exact h
  obtain ⟨u, hu⟩ := Finset.card_pos.mp hpos
  simp only [goodU, Finset.mem_filter, Finset.mem_univ, true_and] at hu
  obtain ⟨hu0, v, hv0, huv⟩ := hu
  refine ⟨Sum.elim (fun _ => u) (fun _ => v), fun h => hu0 ?_, ?_⟩
  · exact congrFun h (Sum.inl ())
  · show ∑ k : Unit ⊕ Unit, (Sum.elim (fun _ => u) (fun _ => v) k) ^ κ *
      extType (fun _ => (1 : K)) ε k = η
    rw [Fintype.sum_sum_type]
    simp only [Sum.elim_inl, Sum.elim_inr, extType, Fintype.univ_unit, Finset.sum_singleton,
      mul_one]
    linear_combination -huv

end QSearch.Schedule1H
