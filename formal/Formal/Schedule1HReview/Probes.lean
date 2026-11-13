import Formal.Schedule1H.Paper
import Formal.Schedule1H.Extras

/-!
# Hostile review probes for `Formal/Schedule1H` (2026-11-13)

Not imported by `Formal.lean`. Build with
`lake build Formal.Schedule1HReview.Probes`.

* `garity_gt`, `isOut_nonempty`: over any finite field, for every `κ ≥ 1`, the imported
  hypothesis `Nonempty (ISOut κ v)` is a *theorem* (Chevalley–Warning, `J = ∅`).
* `halving_correct_noIS`, `halving_correct_weil_noIS`: the main theorems with `hIS`
  discharged.
* `instance13`: all hypotheses of `halving_correct` hold at `K = ZMod 13`, `κ = 4`.
* Non-triviality probes for `IsRootSol` / `IsKSolver`.
-/

namespace QSearch.Schedule1H.Review

open QSearch.Schedule1H Finset

section General

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K]

theorem garity_gt {κ : ℕ} (hκ : 0 < κ) (a : ℕ) : κ * a < Garity κ a := by
  unfold Garity
  have h1 : κ ≤ κ ^ (κ * (κ - 1) / 2) := by
    rcases Nat.lt_or_ge κ 2 with h | h
    · have : κ = 1 := by omega
      subst this; simp
    · have he : 1 ≤ κ * (κ - 1) / 2 := by
        apply (Nat.le_div_iff_mul_le (by norm_num)).mpr
        have h1 : 1 ≤ κ - 1 := by omega
        simpa using Nat.mul_le_mul h h1
      calc κ = κ ^ 1 := (pow_one κ).symm
        _ ≤ κ ^ (κ * (κ - 1) / 2) := Nat.pow_le_pow_right hκ he
  have h2 : a + 1 ≤ (a + 1) ^ κ := by
    calc a + 1 = (a + 1) ^ 1 := (pow_one _).symm
      _ ≤ (a + 1) ^ κ := Nat.pow_le_pow_right (by omega) hκ
  calc κ * a < κ * (a + 1) := by
        have : 0 < κ := hκ
        nlinarith
    _ ≤ κ ^ (κ * (κ - 1) / 2) * (a + 1) ^ κ := Nat.mul_le_mul h1 h2

/-- **The imported hypothesis is provable**: over a finite field, every input of the
collision step has an `ISOut` (take a Chevalley–Warning solution, `J = ∅`). -/
theorem isOut_nonempty {κ a : ℕ} (hκ : 0 < κ) (v : Fin (Garity κ a) → Fin a → K) :
    Nonempty (ISOut κ v) := by
  classical
  obtain ⟨s, hs, hsum⟩ := QSearch.ReesSdeWitness.exists_witness (K := K) hκ (garity_gt hκ a) v
  refine ⟨{ I := univ.filter fun i => s i ≠ 0, J := ∅, γ := s,
            hI := ?_, hdisj := disjoint_empty_right _, hγ := ?_, hrel := ?_ }⟩
  · obtain ⟨i, hi⟩ : ∃ i, s i ≠ 0 := by
      by_contra h; push Not at h; exact hs (funext h)
    exact ⟨i, by simp [hi]⟩
  · intro j hj
    simp only [union_empty, mem_filter, mem_univ, true_and] at hj
    exact hj
  · rw [sum_empty, sum_filter]
    refine (sum_congr rfl fun i _ => ?_).trans hsum
    split_ifs with h
    · rfl
    · push Not at h; simp [h, zero_pow hκ.ne']

/-- `halving_correct` with the Ivanyos–Santha hypothesis discharged. -/
theorem halving_correct_noIS (qf : ℕ → K) {κ : ℕ} (hκ : 0 < κ)
    (hκQ : κ ∣ Fintype.card K - 1)
    (hq : ∀ κ', κ' ∣ κ → Even κ' → qf κ' ^ ((Fintype.card K - 1) / κ') = -1)
    (hT1 : ∀ κ', κ' ∣ κ → Even κ' → 4 * κ' ^ 4 ≤ Fintype.card K →
      ∀ x : K, x ≠ 0 → x ∈ Tsets κ' (qf κ') 1) :
    IsKSolver κ (Apaper qf κ) (H (paperPrep qf) (paperChoice qf) κ) :=
  halving_correct qf hκ hκQ hq (fun _ _ h2 _ v => isOut_nonempty (by omega) v) hT1

/-- `halving_correct_weil` with the Ivanyos–Santha hypothesis discharged: only Weil
remains. -/
theorem halving_correct_weil_noIS (hK : ringChar K ≠ 2) {κ : ℕ} (hκ : 0 < κ)
    (hκQ : κ ∣ Fintype.card K - 1)
    (hW : ∀ κ', κ' ∣ κ → Even κ' → 4 * κ' ^ 4 ≤ Fintype.card K → WeilLower K κ') :
    ∃ qf : ℕ → K, (∀ κ', κ' ∣ κ → Even κ' → qf κ' ^ ((Fintype.card K - 1) / κ') = -1) ∧
      IsKSolver κ (Apaper qf κ) (H (paperPrep qf) (paperChoice qf) κ) :=
  halving_correct_weil hK hκ hκQ (fun _ _ h2 _ v => isOut_nonempty (by omega) v) hW

/-- Non-triviality: a solver of arity `0` is impossible (no nonzero `r : Fin 0 → K`). -/
theorem not_solver_arity_zero (κ : ℕ) (run : (a n : ℕ) → (Fin n → Fin a → K) → Fin n → K) :
    ¬ IsKSolver κ (fun _ => 0) run := by
  intro h
  exact (h 0 0 (fun i => i.elim0) le_rfl).1 (funext fun i => i.elim0)

/-- `IsRootSol` rejects the zero vector. -/
theorem zero_not_rootSol (κ : ℕ) {n a : ℕ} (col : Fin n → Fin a → K) :
    ¬ IsRootSol κ col (0 : Fin n → K) := fun h => h.1 rfl

/-- Non-triviality: at `κ ≥ 1`, arity `1` is impossible (one column `λ ≠ 0`). -/
theorem not_solver_arity_one {κ : ℕ} (hκ : 0 < κ)
    (run : (a n : ℕ) → (Fin n → Fin a → K) → Fin n → K) :
    ¬ IsKSolver κ (fun _ => 1) run := by
  intro h
  obtain ⟨h0, hs⟩ := h 1 1 (fun _ _ => 1) le_rfl
  apply h0
  funext i
  have hi : i = 0 := Subsingleton.elim _ _
  subst hi
  have := congrFun hs 0
  simpa [pow_eq_zero_iff hκ.ne'] using this

open Classical in
/-- A choice-function "solver" of arity `κ a + 1` (Chevalley–Warning). -/
noncomputable def cwRun (κ : ℕ) (a n : ℕ) (col : Fin n → Fin a → K) : Fin n → K :=
  if h : κ * a < n ∧ 0 < κ then
    Classical.choose (QSearch.ReesSdeWitness.exists_witness (K := K) h.2 h.1 col)
  else 0

/-- **`IsKSolver` has no computational content**: over a finite field a noncomputable
`κ`-solver of arity `κ a + 1` exists, far below `A_κ(a) ≥ (a+1)^2` at `κ ≥ 2`. So the
content of `halving_correct` is the correctness of the specific procedure `H` (with
oracles meeting their specs), not the existence of a solver of that arity. -/
theorem cwRun_solver {κ : ℕ} (hκ : 0 < κ) : IsKSolver κ (fun a => κ * a + 1) (cwRun (K := K) κ) := by
  intro a n col hn
  have hn' : κ * a + 1 ≤ n := hn
  have h : κ * a < n ∧ 0 < κ := ⟨by omega, hκ⟩
  unfold cwRun
  rw [dif_pos h]
  exact Classical.choose_spec (QSearch.ReesSdeWitness.exists_witness (K := K) h.2 h.1 col)

end General

section Instance13

local instance fact13 : Fact (Nat.Prime 13) := ⟨by norm_num⟩

/-- `q` for `κ' = 2` (`h = 6`): `2` is a non-square mod 13; for `κ' = 4` (`h = 3`): `-1`. -/
def qf13 : ℕ → ZMod 13 := fun κ => if κ = 2 then 2 else -1

theorem card13 : Fintype.card (ZMod 13) = 13 := ZMod.card 13

/-- **All hypotheses of `halving_correct` hold at `K = ZMod 13`, `κ = 4`** (with `hIS`
discharged by `isOut_nonempty`; `hT1` is vacuous since `4·2^4 > 13`). -/
theorem instance13 :
    IsKSolver 4 (Apaper qf13 4) (H (paperPrep qf13) (paperChoice qf13) 4) := by
  refine halving_correct_noIS qf13 (by norm_num) (by rw [card13]; decide) ?_ ?_
  · intro κ' hd hev
    have hle : κ' ≤ 4 := Nat.le_of_dvd (by norm_num) hd
    rw [card13]
    interval_cases κ' <;> first | (exfalso; revert hd; decide) | (exfalso; revert hev; decide) | decide
  · intro κ' hd hev hQ
    exfalso
    have hle : κ' ≤ 4 := Nat.le_of_dvd (by norm_num) hd
    rw [card13] at hQ
    interval_cases κ' <;> first | (revert hd; decide) | (revert hev; decide) | omega

end Instance13

end QSearch.Schedule1H.Review
