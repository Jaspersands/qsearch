import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.Order.Archimedean.Real.Basic
import Mathlib.Data.Nat.Choose.Sum

/-!
# Milestone 4: the field-size threshold

Source: `research/PRIME_CHARACTER_EXTERIOR_BOUND.md`, lines 99-123, and
`exterior_bound` (`theorems/prime_character_exterior_bound.py`, lines 51-84).

With `R = n + b` branch values and `A = (R - 2)(2^(n-1) - 1)` the note's lower
bound on the irreducible-fiber rate is (line 106, Python lines 62-64)

    I/p ≥ max(0, (p + 1 - R - A·⌈√p⌉) / (n·p)),

and the note claims (lines 119-123) that `p ≥ max(16A², 4(R + A))` makes this
at least `1/(2n)`. That arithmetic implication is proved below
(`traceBound_ge_inv_two_n`, `exterior_threshold_suffices`), for all natural
numbers, with no primality or geometric hypothesis.

`irreducible_rate_ge_traceBound` additionally checks the summation step of
lines 101-106 *assuming* the imported cohomological inputs as hypotheses; those
inputs (the étale trace bound) are not formalized here.
-/

namespace QSearch

/-- `⌈√p⌉`, computed exactly as the Python code does:
`isqrt(p) + [isqrt(p)² ≠ p]`. -/
def ceilSqrt (p : ℕ) : ℕ :=
  if Nat.sqrt p * Nat.sqrt p = p then Nat.sqrt p else Nat.sqrt p + 1

lemma ceilSqrt_le_sqrt_add_one (p : ℕ) : ceilSqrt p ≤ Nat.sqrt p + 1 := by
  unfold ceilSqrt; split_ifs <;> omega

/-- `ceilSqrt` really is the ceiling of the real square root. -/
theorem ceilSqrt_eq_ceil_sqrt (p : ℕ) : (ceilSqrt p : ℤ) = ⌈Real.sqrt p⌉ := by
  symm
  rw [Int.ceil_eq_iff]
  have hs : (Nat.sqrt p : ℝ) ≤ Real.sqrt p := Real.nat_sqrt_le_real_sqrt
  have hs' : Real.sqrt p < Nat.sqrt p + 1 := Real.real_sqrt_lt_nat_sqrt_succ
  unfold ceilSqrt
  split_ifs with h
  · have hp : (p : ℝ) = (Nat.sqrt p : ℝ) * Nat.sqrt p := by exact_mod_cast h.symm
    have he : Real.sqrt p = Nat.sqrt p := by
      rw [hp, Real.sqrt_mul_self (Nat.cast_nonneg _)]
    rw [he]; push_cast; constructor <;> linarith
  · push_cast
    refine ⟨?_, hs'.le⟩
    rcases hs.lt_or_eq with hlt | heq
    · linarith
    · exfalso
      apply h
      have h2 : (Nat.sqrt p : ℝ) * Nat.sqrt p = p := by
        rw [heq, Real.mul_self_sqrt (Nat.cast_nonneg _)]
      exact_mod_cast h2

/-- The note's error coefficient `A = (R - 2)(2^(n-1) - 1)` (Python line 61). -/
def errorCoeff (n R : ℕ) : ℕ := (R - 2) * (2 ^ (n - 1) - 1)

/-- The exterior trace bound `max(0, (p + 1 - R - A⌈√p⌉)/(n p))`
(note line 106; Python lines 62-64). -/
def traceBound (p n R A : ℕ) : ℚ :=
  max 0 (((p : ℚ) + 1 - R - A * ceilSqrt p) / (n * p))

/-- Note line 123, first claim: `p ≥ 16A²` gives `A·√p ≤ p/4`. -/
theorem A_mul_sqrt_le {p A : ℕ} (h : 16 * A ^ 2 ≤ p) :
    (A : ℝ) * Real.sqrt p ≤ p / 4 := by
  have hp : (0 : ℝ) ≤ p := Nat.cast_nonneg _
  have hsq : Real.sqrt p * Real.sqrt p = p := Real.mul_self_sqrt hp
  have h4 : 4 * (A : ℝ) ≤ Real.sqrt p := by
    rw [Real.le_sqrt (by positivity) hp]
    have : ((16 * A ^ 2 : ℕ) : ℝ) ≤ p := by exact_mod_cast h
    push_cast at this
    nlinarith
  nlinarith [Real.sqrt_nonneg (p : ℝ)]

/-- Integer form of the same step: `4 A ⌊√p⌋ ≤ p`. -/
lemma four_A_mul_sqrt_le {p A : ℕ} (h : 16 * A ^ 2 ≤ p) : 4 * (A * Nat.sqrt p) ≤ p := by
  have h4 : 4 * A ≤ Nat.sqrt p := Nat.le_sqrt.mpr (by nlinarith)
  calc 4 * (A * Nat.sqrt p) = (4 * A) * Nat.sqrt p := by ring
    _ ≤ Nat.sqrt p * Nat.sqrt p := Nat.mul_le_mul_right _ h4
    _ ≤ p := Nat.sqrt_le p

/-- Note line 123, second claim: `A·⌈√p⌉ ≤ p/4 + A` (stated as `4A⌈√p⌉ ≤ p + 4A`). -/
theorem four_A_mul_ceilSqrt_le {p A : ℕ} (h : 16 * A ^ 2 ≤ p) :
    4 * (A * ceilSqrt p) ≤ p + 4 * A := by
  have h1 := four_A_mul_sqrt_le h
  have h2 : A * ceilSqrt p ≤ A * (Nat.sqrt p + 1) :=
    Nat.mul_le_mul_left _ (ceilSqrt_le_sqrt_add_one p)
  nlinarith

/-- **Field threshold (note lines 119-123).** If `p > 0`, `p ≥ 16A²` and
`p ≥ 4(R + A)`, then the trace bound is at least `1/(2n)`.
(For `n = 0` both sides degenerate and the inequality still holds.) -/
theorem traceBound_ge_inv_two_n {p n R A : ℕ} (hp : 0 < p)
    (h1 : 16 * A ^ 2 ≤ p) (h2 : 4 * (R + A) ≤ p) :
    1 / (2 * n : ℚ) ≤ traceBound p n R A := by
  unfold traceBound
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp
  apply le_max_of_le_right
  have hc := four_A_mul_ceilSqrt_le h1
  -- 2 (R + A ⌈√p⌉) ≤ p
  have key : 2 * (R + A * ceilSqrt p) ≤ p := by omega
  have keyQ : (2 : ℚ) * (R + A * ceilSqrt p) ≤ p := by exact_mod_cast key
  have hnQ : (0 : ℚ) < n := by exact_mod_cast hn
  have hpQ : (0 : ℚ) < p := by exact_mod_cast hp
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith

/-- **Field threshold, as the note writes it.** With `R = n + b` branch values
and `A = (R - 2)(2^(n-1) - 1)`, `p ≥ max(16A², 4(R + A))` (and `p > 0`) implies
that the exterior trace bound is at least `1/(2n)`. -/
theorem exterior_threshold_suffices (n b p : ℕ) (hp : 0 < p)
    (h : max (16 * errorCoeff n (n + b) ^ 2) (4 * (n + b + errorCoeff n (n + b))) ≤ p) :
    1 / (2 * n : ℚ) ≤ traceBound p n (n + b) (errorCoeff n (n + b)) :=
  traceBound_ge_inv_two_n hp (le_of_max_le_left h) (le_of_max_le_right h)

/-- `∑_{j=1}^{n-1} C(n-1, j) = 2^(n-1) - 1`: the total rank of the nontrivial
exterior powers (Python `rank_sum`, line 60). -/
lemma sum_choose_Ico (n : ℕ) :
    ∑ j ∈ Finset.Ico 1 n, (n - 1).choose j = 2 ^ (n - 1) - 1 := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  have h := Nat.sum_range_choose m
  rw [Finset.sum_range_succ', Nat.choose_zero_right] at h
  have h2 : ∑ j ∈ Finset.Ico 1 (m + 1), m.choose j = ∑ k ∈ Finset.range m, m.choose (k + 1) := by
    rw [Finset.sum_Ico_eq_sum_range]
    simp [add_comm]
  rw [Nat.add_sub_cancel, h2]
  exact Nat.eq_sub_of_add_eq h

/-- **Summation step (note lines 99-106), conditional on the imported inputs.**
Suppose, as the note derives from the cycle indicator and the étale trace
formula (NOT formalized here):

* `n I = #U + ∑_{j=1}^{n-1} (-1)^j S_j` (the indicator summed over fibers),
* `#U ≥ p + 1 - R`,
* `|S_j| ≤ (R - 2) C(n-1, j) √p` for `1 ≤ j ≤ n - 1`, with `R ≥ 2`,
* `I ≥ 0`.

Then `I / p ≥ max(0, (p + 1 - R - A⌈√p⌉)/(n p))` with `A = (R-2)(2^(n-1)-1)`. -/
theorem irreducible_rate_ge_traceBound {n R p : ℕ} (hn : 0 < n) (hp : 0 < p) (hR : 2 ≤ R)
    (I U : ℝ) (S : ℕ → ℝ) (hI : 0 ≤ I)
    (hind : n * I = U + ∑ j ∈ Finset.Ico 1 n, (-1 : ℝ) ^ j * S j)
    (hU : (p : ℝ) + 1 - R ≤ U)
    (hS : ∀ j ∈ Finset.Ico 1 n, |S j| ≤ ((R : ℝ) - 2) * (n - 1).choose j * Real.sqrt p) :
    (traceBound p n R (errorCoeff n R) : ℝ) ≤ I / p := by
  set A := errorCoeff n R
  have hA : (A : ℝ) = ((R : ℝ) - 2) * ∑ j ∈ Finset.Ico 1 n, ((n - 1).choose j : ℝ) := by
    have h1 : 1 ≤ 2 ^ (n - 1) := Nat.one_le_two_pow
    have hsum : (∑ j ∈ Finset.Ico 1 n, ((n - 1).choose j : ℝ)) = ((2 ^ (n - 1) - 1 : ℕ) : ℝ) := by
      rw [← sum_choose_Ico]; push_cast; rfl
    rw [hsum]
    simp only [A, errorCoeff]
    push_cast [hR, h1]
    ring
  -- the error sum is at most A √p
  have herr : -((A : ℝ) * Real.sqrt p) ≤ ∑ j ∈ Finset.Ico 1 n, (-1 : ℝ) ^ j * S j := by
    have : |∑ j ∈ Finset.Ico 1 n, (-1 : ℝ) ^ j * S j| ≤ A * Real.sqrt p := by
      calc |∑ j ∈ Finset.Ico 1 n, (-1 : ℝ) ^ j * S j|
          ≤ ∑ j ∈ Finset.Ico 1 n, |(-1 : ℝ) ^ j * S j| := Finset.abs_sum_le_sum_abs _ _
        _ = ∑ j ∈ Finset.Ico 1 n, |S j| := by simp [abs_mul]
        _ ≤ ∑ j ∈ Finset.Ico 1 n, ((R : ℝ) - 2) * (n - 1).choose j * Real.sqrt p :=
            Finset.sum_le_sum hS
        _ = A * Real.sqrt p := by rw [hA, Finset.mul_sum, Finset.sum_mul]
    exact (abs_le.mp this).1
  -- √p ≤ ⌈√p⌉
  have hceil : Real.sqrt p ≤ (ceilSqrt p : ℝ) := by
    have h := Int.le_ceil (Real.sqrt p)
    rw [← ceilSqrt_eq_ceil_sqrt] at h
    exact_mod_cast h
  have hlow : (p : ℝ) + 1 - R - A * ceilSqrt p ≤ n * I := by
    have : (A : ℝ) * Real.sqrt p ≤ A * ceilSqrt p :=
      mul_le_mul_of_nonneg_left hceil (Nat.cast_nonneg _)
    linarith
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  have hpR : (0 : ℝ) < p := by exact_mod_cast hp
  unfold traceBound
  push_cast
  apply max_le (div_nonneg hI hpR.le)
  rw [div_le_div_iff₀ (by positivity) hpR]
  calc ((p : ℝ) + 1 - R - A * ceilSqrt p) * p ≤ (n * I) * p :=
        mul_le_mul_of_nonneg_right hlow hpR.le
    _ = I * (n * p) := by ring

end QSearch
