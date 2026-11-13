import Formal.Schedule1H.Paper

/-!
# Review probe: `T_j` and `A_κ(a)` do not depend on the choice of `q`

Closes the author's Finding 4 (paper l.~688: "`T_j` depends only on `(p, κ)`").
-/

namespace QSearch.Schedule1H.Review

open QSearch.Schedule1H Finset

variable {K : Type*} [Field K]

/-- Exponent of `e` in the entry `k` of `c^{(j)}`. -/
def deg : (j : ℕ) → Typ j → ℕ
  | 0, _ => 0
  | j + 1, Sum.inl k => deg j k
  | j + 1, Sum.inr k => deg j k + 1

theorem cTyp_mul (e m : K) : ∀ (j : ℕ) (k : Typ j), cTyp (e * m) j k = cTyp e j k * m ^ deg j k
  | 0, _ => by simp [cTyp, deg]
  | j + 1, Sum.inl k => by
      show cTyp (e * m) j k = cTyp e j k * m ^ deg j k
      exact cTyp_mul e m j k
  | j + 1, Sum.inr k => by
      show e * m * cTyp (e * m) j k = e * cTyp e j k * m ^ (deg j k + 1)
      rw [cTyp_mul e m j k, pow_succ]; ring

/-- `T(c)` is unchanged when each entry is multiplied by a nonzero `κ`-th power. -/
theorem Tset_scale {τ : Type*} [Fintype τ] [DecidableEq τ] {κ : ℕ} (hκ : 0 < κ)
    (c : τ → K) (π : τ → K) (hπ : ∀ k, π k ≠ 0) :
    Tset κ (fun k => c k * π k ^ κ) = Tset κ c := by
  ext x
  rw [mem_Tset_iff hκ, mem_Tset_iff hκ]
  constructor
  · rintro ⟨ρ, hρ, rfl⟩
    refine ⟨fun k => ρ k * π k, fun h => hρ (funext fun k => ?_), ?_⟩
    · have := congrFun h k
      simpa [hπ k] using this
    · refine sum_congr rfl fun k _ => ?_
      rw [mul_pow]; ring
  · rintro ⟨ρ, hρ, rfl⟩
    refine ⟨fun k => ρ k / π k, fun h => hρ (funext fun k => ?_), ?_⟩
    · have := congrFun h k
      simpa [hπ k] using this
    · refine sum_congr rfl fun k _ => ?_
      rw [div_pow]
      field_simp [pow_ne_zero κ (hπ k)]

variable [Fintype K] [DecidableEq K]

/-- **`T_s` does not depend on `q`**: any two `q, q'` with `q^h = q'^h = -1` give the same
`T_s`. -/
theorem Tsets_indep {κ : ℕ} (hκ : 0 < κ) (hκQ : κ ∣ Fintype.card K - 1) {q q' : K}
    (hq : q ^ ((Fintype.card K - 1) / κ) = -1) (hq' : q' ^ ((Fintype.card K - 1) / κ) = -1)
    (s : ℕ) : Tsets κ q' s = Tsets κ q s := by
  set h := (Fintype.card K - 1) / κ
  have hQ1 : 1 < Fintype.card K := Fintype.one_lt_card
  have hhpos : 0 < h := Nat.div_pos (Nat.le_of_dvd (by omega) hκQ) hκ
  have hκh : κ * h = Fintype.card K - 1 := Nat.mul_div_cancel' hκQ
  have hne : ∀ y : K, y ^ h = -1 → y ≠ 0 := by
    rintro y hy rfl; rw [zero_pow hhpos.ne'] at hy; exact one_ne_zero (neg_eq_zero.mp hy.symm)
  have hq0 := hne q hq
  have hq'0 := hne q' hq'
  have hm : (q / q') ^ h = 1 := by
    rw [div_pow, hq, hq', div_self (neg_ne_zero.mpr one_ne_zero)]
  obtain ⟨r, hr⟩ := exists_root_of_pow_eq_one hκh hhpos (div_ne_zero hq0 hq'0) hm
  have hr0 : r ≠ 0 := by
    rintro rfl; rw [zero_pow hκ.ne'] at hr; exact div_ne_zero hq0 hq'0 hr.symm
  have he : -q'⁻¹ = -q⁻¹ * r ^ κ := by
    rw [hr]; field_simp
  unfold Tsets
  rw [he]
  have : cTyp (-q⁻¹ * r ^ κ) s = fun k => cTyp (-q⁻¹) s k * (r ^ deg s k) ^ κ := by
    funext k; rw [cTyp_mul, ← pow_mul, ← pow_mul, mul_comm (deg s k)]
  rw [this]
  exact Tset_scale hκ _ _ fun k => pow_ne_zero _ hr0

theorem Admissible_indep {κ : ℕ} (hκ : 0 < κ) (hκQ : κ ∣ Fintype.card K - 1) {q q' : K}
    (hq : q ^ ((Fintype.card K - 1) / κ) = -1) (hq' : q' ^ ((Fintype.card K - 1) / κ) = -1)
    (s : ℕ) (f1 : Bool) : Admissible κ q' s f1 ↔ Admissible κ q s f1 := by
  unfold Admissible
  rw [Tsets_indep hκ hκQ hq hq' s]

/-- **`A_κ(a)` does not depend on the choice of the `q`'s.** -/
theorem Apaper_indep (qf qf' : ℕ → K) :
    ∀ κ : ℕ, 0 < κ → κ ∣ Fintype.card K - 1 →
      (∀ κ', κ' ∣ κ → Even κ' → qf κ' ^ ((Fintype.card K - 1) / κ') = -1) →
      (∀ κ', κ' ∣ κ → Even κ' → qf' κ' ^ ((Fintype.card K - 1) / κ') = -1) →
      ∀ a, Apaper qf' κ a = Apaper qf κ a := by
  intro κ
  induction κ using Nat.strong_induction_on with
  | _ κ ih =>
  intro hκ hκQ hq hq' a
  by_cases h1 : κ ≤ 1
  · rw [Apaper.eq_1 qf' κ a, Apaper.eq_1 qf κ a, dif_pos h1, dif_pos h1]
  · rw [Apaper.eq_1 qf' κ a, Apaper.eq_1 qf κ a, dif_neg h1, dif_neg h1]
    congr 1
    ext n
    simp only [Set.mem_insert_iff, Set.mem_setOf_eq]
    apply or_congr_right
    constructor
    · rintro ⟨s, f1, hev, hadm, rfl⟩
      have hD : κ / 2 ∣ κ := Nat.div_dvd_of_dvd hev.two_dvd
      have hD0 : 0 < κ / 2 := by omega
      refine ⟨s, f1, hev, (Admissible_indep hκ hκQ (hq κ dvd_rfl hev) (hq' κ dvd_rfl hev) s f1).mp hadm, ?_⟩
      rw [ih (κ / 2) (by omega) hD0 (hD.trans hκQ) (fun κ' h e => hq κ' (h.trans hD) e)
        (fun κ' h e => hq' κ' (h.trans hD) e) a]
    · rintro ⟨s, f1, hev, hadm, rfl⟩
      have hD : κ / 2 ∣ κ := Nat.div_dvd_of_dvd hev.two_dvd
      have hD0 : 0 < κ / 2 := by omega
      refine ⟨s, f1, hev, (Admissible_indep hκ hκQ (hq κ dvd_rfl hev) (hq' κ dvd_rfl hev) s f1).mpr hadm, ?_⟩
      rw [ih (κ / 2) (by omega) hD0 (hD.trans hκQ) (fun κ' h e => hq κ' (h.trans hD) e)
        (fun κ' h e => hq' κ' (h.trans hD) e) a]

end QSearch.Schedule1H.Review
