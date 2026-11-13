import Formal.Schedule1H.Stage

/-!
# Schedule 1H, part 7: the recursion for `T_j`, Corollary `cor:hcd`(i), Remark `rem:kappa-two`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:halving`: the display
`T_0 = P, T_j = T_{j-1} ∪ ε T_{j-1} ∪ {α + εβ}` before Lemma `lem:two-term`,
Corollary `cor:hcd`(i) and the last claim of Remark `rem:kappa-two`.

* `Tset_unit`: `T_0 = T((1)) = P`.
* `mem_Tset_extType`: `T(c, ec) = T(c) ∪ e T(c) ∪ {α + eβ : α, β ∈ T(c)}` (the recursion
  for `T_j`, any `e`).
* `Tset_subset_extType`: `T_j ⊆ T_{j+1}`.
* `zero_not_mem_T1`: over a finite field of odd characteristic with `κ ∣ |K| - 1`,
  `q^h = -1`: `0 ∉ T_1 = T((1, ε))`, so the plan `(1, F0)` is never admissible
  (Remark `rem:kappa-two`).
* `cor_hcd_i`: with `q = -1` (so `ε = 1`), the plan `(⌈log₂ t⌉, F0)` with the zero sum
  placed on the first `t` representations is a `κ`-solver of arity `A_D(a)^{⌈log₂ t⌉}`
  given any `D`-solver (Corollary `cor:hcd`(i), correctness; no table needed).
-/

namespace QSearch.Schedule1H

open Finset

variable {K : Type*} [Field K]

section TRecursion

variable {τ : Type*} [Fintype τ] [DecidableEq τ]

/-- `T_0 = T((1)) = P`. -/
theorem Tset_unit {κ : ℕ} (hκ : 0 < κ) : Tset κ (fun _ : Unit => (1 : K)) = Pow κ := by
  ext x
  rw [mem_Tset_iff hκ]
  constructor
  · rintro ⟨ρ, hρ, rfl⟩
    have h0 : ρ () ≠ 0 := fun h => hρ (funext fun u => by cases u; exact h)
    exact ⟨by simpa using pow_ne_zero κ h0, ρ (), by simp⟩
  · rintro ⟨hx, r, rfl⟩
    refine ⟨fun _ => r, fun h => hx ?_, by simp⟩
    have : r = 0 := congrFun h ()
    simp [this, zero_pow hκ.ne']

/-- **The recursion for `T_j`**: `T(c, ec) = T(c) ∪ e T(c) ∪ {α + eβ : α, β ∈ T(c)}`. -/
theorem mem_Tset_extType {κ : ℕ} (hκ : 0 < κ) (c : τ → K) (e x : K) :
    x ∈ Tset κ (extType c e) ↔
      x ∈ Tset κ c ∨ (∃ y ∈ Tset κ c, x = e * y) ∨
        ∃ α ∈ Tset κ c, ∃ β ∈ Tset κ c, x = α + e * β := by
  simp only [mem_Tset_iff hκ]
  have hsplit : ∀ ρ : τ ⊕ τ → K, ∑ k, ρ k ^ κ * extType c e k =
      ∑ k, ρ (Sum.inl k) ^ κ * c k + e * ∑ k, ρ (Sum.inr k) ^ κ * c k := by
    intro ρ
    rw [Fintype.sum_sum_type, Finset.mul_sum]
    simp only [extType, Sum.elim_inl, Sum.elim_inr]
    congr 1
    exact Finset.sum_congr rfl fun k _ => by ring
  have hzero : ∀ f : τ → K, f = 0 → ∑ k, f k ^ κ * c k = 0 := by
    rintro f rfl; simp [zero_pow hκ.ne']
  constructor
  · rintro ⟨ρ, hρ, rfl⟩
    rw [hsplit]
    by_cases h2 : (fun k => ρ (Sum.inr k)) = 0
    · left
      refine ⟨fun k => ρ (Sum.inl k), fun h1 => hρ (funext ?_), ?_⟩
      · rintro (k | k)
        · exact congrFun h1 k
        · exact congrFun h2 k
      · rw [hzero _ h2, mul_zero, add_zero]
    · by_cases h1 : (fun k => ρ (Sum.inl k)) = 0
      · right; left
        refine ⟨_, ⟨fun k => ρ (Sum.inr k), h2, rfl⟩, ?_⟩
        rw [hzero _ h1, zero_add]
      · right; right
        exact ⟨_, ⟨fun k => ρ (Sum.inl k), h1, rfl⟩, _, ⟨fun k => ρ (Sum.inr k), h2, rfl⟩, rfl⟩
  · rintro (⟨ρ, hρ, rfl⟩ | ⟨y, ⟨ρ, hρ, rfl⟩, rfl⟩ | ⟨α, ⟨ρ1, hρ1, rfl⟩, β, ⟨ρ2, hρ2, rfl⟩, rfl⟩)
    · refine ⟨Sum.elim ρ 0, fun h => hρ (funext fun k => congrFun h (Sum.inl k)), ?_⟩
      rw [hsplit]; simp [zero_pow hκ.ne']
    · refine ⟨Sum.elim 0 ρ, fun h => hρ (funext fun k => congrFun h (Sum.inr k)), ?_⟩
      rw [hsplit]; simp [zero_pow hκ.ne']
    · refine ⟨Sum.elim ρ1 ρ2, fun h => hρ1 (funext fun k => congrFun h (Sum.inl k)), ?_⟩
      rw [hsplit]; simp

/-- The sets `T_j` increase: `T(c) ⊆ T(c, ec)` (so `T_j ⊆ T_{j+1}`, and a plan admissible
at some `s` stays admissible for larger `s` when `|K| < 4κ^4`). -/
theorem Tset_subset_extType {κ : ℕ} (hκ : 0 < κ) (c : τ → K) (e : K) :
    Tset κ c ⊆ Tset κ (extType c e) := fun x hx =>
  (mem_Tset_extType hκ c e x).mpr (Or.inl hx)

end TRecursion

section KappaTwo

variable [Fintype K] [DecidableEq K]

/-- **Remark `rem:kappa-two`, last claim**: `0 ∉ T_1 = T((1, ε))`, `ε = -q⁻¹`, so the
plan `(1, F0)` is never admissible. Hypotheses: odd characteristic, `κ h = |K| - 1`,
`q^h = -1`. -/
theorem zero_not_mem_T1 (hK : ringChar K ≠ 2) {κ h : ℕ} (hκ : 0 < κ)
    (hκh : κ * h = Fintype.card K - 1) {q : K} (hq : q ^ h = -1) :
    (0 : K) ∉ Tset κ (extType (fun _ : Unit => (1 : K)) (-q⁻¹)) := by
  have hq0 : q ≠ 0 := by
    rintro rfl
    rcases Nat.eq_zero_or_pos h with h0 | h0
    · subst h0; simp at hq; exact Ring.neg_one_ne_one_of_char_ne_two hK hq.symm
    · rw [zero_pow h0.ne'] at hq; exact one_ne_zero (neg_eq_zero.mp hq.symm)
  rw [mem_Tset_iff hκ]
  rintro ⟨ρ, hρ, hsum⟩
  rw [Fintype.sum_sum_type] at hsum
  simp only [extType, Sum.elim_inl, Sum.elim_inr, Fintype.univ_unit, Finset.sum_singleton,
    mul_one] at hsum
  set u := ρ (Sum.inl ())
  set v := ρ (Sum.inr ())
  have hv : v ≠ 0 := by
    intro hv
    rw [hv, zero_pow hκ.ne', zero_mul, add_zero, pow_eq_zero_iff hκ.ne'] at hsum
    apply hρ; funext k; rcases k with ⟨⟩ | ⟨⟩
    · exact hsum
    · exact hv
  have hu : u ≠ 0 := by
    intro hu
    rw [hu, zero_pow hκ.ne', zero_add, mul_eq_zero, pow_eq_zero_iff hκ.ne'] at hsum
    rcases hsum with h1 | h1
    · exact hv h1
    · exact hq0 (inv_eq_zero.mp (neg_eq_zero.mp h1))
  have hroot : (u / v) ^ κ = q⁻¹ := by
    have hu' : u ^ κ = v ^ κ * q⁻¹ := by linear_combination hsum
    rw [div_pow, hu', mul_comm, mul_div_assoc, div_self (pow_ne_zero _ hv), mul_one]
  have h1 := pow_eq_one_of_root (K := K) hκh (div_ne_zero hu hv)
  rw [hroot, inv_pow, hq] at h1
  exact Ring.neg_one_ne_one_of_char_ne_two hK (by simpa using h1)

end KappaTwo

section CorHcd

variable [DecidableEq K]

/-- **Corollary `cor:hcd`(i), correctness.** If `q = -1` (so `ε = 1`, `c^{(j)}` all
ones), the plan `(⌈log₂ t⌉, F0)` — stages calling any `D`-solver `Hrun` of arity `N`,
then F0 with the zero sum `z` of length `t` on the first `t` representations — is a
`κ`-solver of arity `N(a)^{⌈log₂ t⌉}`. -/
theorem cor_hcd_i {κ D : ℕ} {cls : K → Bool} {rt : K → K}
    (hst : StageOK κ D (-1) cls rt) (N : ℕ → ℕ)
    (Hrun : (a n : ℕ) → (Fin n → Fin a → K) → Fin n → K) (hH : IsKSolver D N Hrun)
    {t : ℕ} (z : Fin t → K) (hz0 : z ≠ 0) (hz : ∑ i, z i ^ κ = 0) :
    IsKSolver κ (fun a => N a ^ Nat.clog 2 t) (fun a n col =>
      padRun (onFin (levEquiv (N a) (Nat.clog 2 t))
        (planF0 κ (stageRun D (-1) cls rt (Hrun a (N a))) (Nat.clog 2 t)
          (fun k => if h : (typEquiv _ k).val < t then z ⟨_, h⟩ else 0))) col) := by
  intro a n col hn
  have hκ : 0 < κ := by obtain ⟨h1, h2, _⟩ := hst; omega
  have he : -(-1 : K)⁻¹ = 1 := by simp
  have horc : ∀ v : Fin (N a) → Fin a → K, StepSpec κ 1 v
      (stageRun D (-1) cls rt (Hrun a (N a)) v).1 (stageRun D (-1) cls rt (Hrun a (N a)) v).2 := by
    intro v
    have := stageRun_stepSpec hst (Hrun a (N a)) v (hH a _ v le_rfl)
    rwa [he] at this
  have hz' := zeroSum_lift hκ z hz0 hz (Nat.clog 2 t) (Nat.le_pow_clog one_lt_two t)
  refine padRun_spec hκ _ col hn (onFin_spec _ _ (fun col' => ?_) _)
  exact planF0_spec hκ one_ne_zero _ horc _ _ hz'.1 hz'.2 col'

end CorHcd

end QSearch.Schedule1H
