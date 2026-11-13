import Formal.Schedule1H.Paper
import Formal.Schedule1H.Extras

/-!
# Review probe: the paper's `A_2(a) = (a+1)^2` and tie rule at `p = 7` (Remark `rem:kappa-two`)

Checks that `Apaper` and `paperChoice` reproduce the paper's claimed value and choice
at `K = ZMod 7`, `κ = 2`, `q = 3` (`q^3 = -1`, `ε = -q⁻¹ = 2`), for every `a`.
-/

namespace QSearch.Schedule1H.Review

open QSearch.Schedule1H Finset

local instance fact7 : Fact (Nat.Prime 7) := ⟨by norm_num⟩

def qf7 : ℕ → ZMod 7 := fun _ => 3

theorem card7 : Fintype.card (ZMod 7) = 7 := ZMod.card 7

theorem tMin_ge_two {K : Type*} [Field K] [Fintype K] [DecidableEq K] {κ : ℕ} (hκ : 0 < κ) :
    2 ≤ tMin K κ := by
  obtain ⟨z, hz0, hz⟩ := tMin_mem (K := K) hκ
  by_contra hlt
  push Not at hlt
  interval_cases h : tMin K κ
  · exact hz0 (funext fun i => i.elim0)
  · apply hz0; funext i
    have hi : i = 0 := Subsingleton.elim _ _
    subst hi
    simpa [pow_eq_zero_iff hκ.ne'] using hz

theorem T1_full7 : ∀ x : ZMod 7, x ≠ 0 → x ∈ Tsets 2 (qf7 2) 1 := by
  intro x hx
  rw [Tsets, mem_Tset_iff (by norm_num)]
  have he : -(qf7 2)⁻¹ = (2 : ZMod 7) := by
    have h35 : (3 : ZMod 7) * 5 = 1 := by decide
    rw [show qf7 2 = 3 from rfl, inv_eq_of_mul_eq_one_right h35]; decide
  have key : ∀ u v : ZMod 7, (∑ k, (Sum.elim (fun _ => u) (fun _ => v) : Typ 1 → ZMod 7) k ^ 2 *
      cTyp (-(qf7 2)⁻¹) 1 k) = u ^ 2 + 2 * v ^ 2 := by
    intro u v
    rw [Fintype.sum_sum_type]
    show (∑ _k : Unit, u ^ 2 * (1 : ZMod 7)) + ∑ _k : Unit, v ^ 2 * (-(qf7 2)⁻¹ * 1) = _
    rw [he]; simp; ring
  have hall : ∀ x : ZMod 7, x ≠ 0 → ∃ u v : ZMod 7, (u ≠ 0 ∨ v ≠ 0) ∧ u ^ 2 + 2 * v ^ 2 = x := by
    decide
  obtain ⟨u, v, huv, hx'⟩ := hall x hx
  refine ⟨Sum.elim (fun _ => u) (fun _ => v), fun h => ?_, (key u v).trans hx'⟩
  rcases huv with hu | hv
  · exact hu (congrFun h (Sum.inl ()))
  · exact hv (congrFun h (Sum.inr ()))

theorem adm11 : Admissible 2 (qf7 2) 1 true := by
  refine ⟨le_rfl, fun _ => ⟨fun _ => T1_full7, fun h => absurd h (by decide)⟩, fun h => ?_⟩
  rw [card7] at h; norm_num at h

theorem not_adm10 : ¬ Admissible 2 (qf7 2) 1 false := by
  rintro ⟨_, hs, _⟩
  have h0 := (hs (by rw [card7]; norm_num)).2 rfl
  have hK : ringChar (ZMod 7) ≠ 2 := by rw [ZMod.ringChar_zmod_n]; norm_num
  exact zero_not_mem_T1 (K := ZMod 7) hK (κ := 2) (h := 3) (by norm_num)
    (by rw [card7]) (q := 3) (by decide) h0

theorem Apaper_one (qf : ℕ → ZMod 7) (a : ℕ) : Apaper qf 1 a = a + 1 := by
  rw [Apaper, dite_eq_left le_rfl]

/-- **The paper's `A_2(a) = (a+1)^2` at `p = 7`** (Remark `rem:kappa-two`). -/
theorem Apaper_two7 (a : ℕ) : Apaper qf7 2 a = (a + 1) ^ 2 := by
  have hset := Apaper.eq_1 qf7 2 a
  rw [dite_eq_right (by norm_num)] at hset
  rw [hset]
  apply le_antisymm
  · apply Nat.sInf_le
    refine Set.mem_insert_of_mem _ ⟨1, true, even_two, adm11, ?_⟩
    simp [Apaper_one, nF, pow_two]
  · apply le_csInf ⟨_, Set.mem_insert _ _⟩
    rintro n (rfl | ⟨s, f1, _, hadm, rfl⟩)
    · have hL : 1 ≤ Nat.clog 2 (tMin (ZMod 7) 2) :=
        Nat.one_le_iff_ne_zero.mpr fun h0 => by
          have := tMin_ge_two (K := ZMod 7) (κ := 2) (by norm_num)
          have h2 := Nat.le_pow_clog one_lt_two (tMin (ZMod 7) 2)
          rw [h0, pow_zero] at h2
          omega
      unfold Garity
      have hG : 1 ≤ 2 ^ (2 * (2 - 1) / 2) * (a + 1) ^ 2 :=
        Nat.one_le_iff_ne_zero.mpr (by positivity)
      calc (a + 1) ^ 2 ≤ 2 ^ (2 * (2 - 1) / 2) * (a + 1) ^ 2 :=
            Nat.le_mul_of_pos_left _ (by norm_num)
        _ = (2 ^ (2 * (2 - 1) / 2) * (a + 1) ^ 2) ^ 1 := (pow_one _).symm
        _ ≤ _ := Nat.pow_le_pow_right hG hL
    · rw [show (2 : ℕ) / 2 = 1 from rfl, Apaper_one]
      have hs1 := hadm.1
      rcases Nat.lt_or_ge s 2 with hs | hs
      · have : s = 1 := by omega
        subst this
        cases f1
        · exact absurd hadm not_adm10
        · simp [nF, pow_two]
      · have h1 : (a + 1) ^ 2 ≤ (a + 1) ^ s := Nat.pow_le_pow_right (by omega) hs
        have h2 : 1 ≤ nF f1 a := by cases f1 <;> simp [nF]
        nlinarith

theorem garity_pow_gt7 (a : ℕ) :
    (a + 1) ^ 2 < Garity 2 a ^ Nat.clog 2 (tMin (ZMod 7) 2) := by
  have hL : 1 ≤ Nat.clog 2 (tMin (ZMod 7) 2) :=
    Nat.one_le_iff_ne_zero.mpr fun h0 => by
      have := tMin_ge_two (K := ZMod 7) (κ := 2) (by norm_num)
      have h2 := Nat.le_pow_clog one_lt_two (tMin (ZMod 7) 2)
      rw [h0, pow_zero] at h2
      omega
  have hG : Garity 2 a = 2 * (a + 1) ^ 2 := by simp [Garity]
  have hpos : 0 < (a + 1) ^ 2 := by positivity
  calc (a + 1) ^ 2 < 2 * (a + 1) ^ 2 := by omega
    _ = Garity 2 a ^ 1 := by rw [pow_one, hG]
    _ ≤ _ := Nat.pow_le_pow_right (by rw [hG]; omega) hL

/-- **The paper's tie rule at `p = 7`, `κ = 2`**: `paperChoice` runs the plan `(1, F1)` for
every `a` (including `a = 0`, where every admissible plan ties). -/
theorem paperChoice_two7 (a : ℕ) : paperChoice qf7 2 a = .plan 1 true := by
  classical
  have hA := Apaper_two7 a
  have hne : Apaper qf7 2 a ≠ Garity 2 a ^ Nat.clog 2 (tMin (ZMod 7) 2) := by
    rw [hA]; exact (garity_pow_gt7 a).ne
  have hex : ∃ s f1, Even 2 ∧ Admissible 2 (qf7 2) s f1 ∧
      Apaper qf7 2 a = Apaper qf7 (2 / 2) a ^ s * nF f1 a :=
    ⟨1, true, even_two, adm11, by
      rw [hA, show (2 : ℕ) / 2 = 1 from rfl, Apaper_one]; simp [nF, pow_two]⟩
  have hfind : Nat.find hex = 1 := by
    rw [Nat.find_eq_iff]
    refine ⟨⟨true, even_two, adm11, ?_⟩, fun n hn => ?_⟩
    · rw [hA, show (2 : ℕ) / 2 = 1 from rfl, Apaper_one]; simp [nF, pow_two]
    · rintro ⟨f1, _, hadm, _⟩
      have := hadm.1
      omega
  unfold paperChoice
  rw [ite_eq_right hne, dite_eq_left hex]
  rw [ite_eq_right]
  · rw [hfind]
  · rintro ⟨_, hadm, _⟩
    rw [hfind] at hadm
    exact not_adm10 hadm

end QSearch.Schedule1H.Review
