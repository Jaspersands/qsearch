import Mathlib.FieldTheory.Finite.Basic

/-!
# Rees SDE: the gcd/Bezout reduction of the exponent

Source: `docs/papers/rees-hsp/appendix-schedule2.tex`, Lemma `lem:app-s2-gcd`.

Over `ZMod p`, write `κ = gcd(d, p - 1)`. There is a Bezout exponent `t ≥ 1` with
`(x ^ t) ^ d = x ^ κ` for every `x` (`pow_bezout_exponent`). Hence the `d`-th powers
of nonzero elements are exactly the `κ`-th powers of nonzero elements (part (a),
`range_pow_units_eq`), and a nonzero solution `u` of `∑ u_i ^ κ λ_i = 0` gives the
nonzero solution `s_i = u_i ^ t` of `∑ s_i ^ d λ_i = 0`, with the same support
(part (b), `bezout_witness`). Part (c), the case `κ = 1`, is the linear case of
`QSearch.ReesSdeWitness.exists_witness`.

The label columns live in an arbitrary `ZMod p`-module; nothing about their
number is used here.
-/

namespace QSearch.ReesSdeGcd

/-- A Bezout exponent: `t ≥ 1` with `(x ^ t) ^ d = x ^ gcd(d, p - 1)` on `ZMod p`. -/
theorem pow_bezout_exponent {p : ℕ} [hp : Fact p.Prime] {d : ℕ} (hd : 0 < d) :
    ∃ t : ℕ, 0 < t ∧ ∀ x : ZMod p, (x ^ t) ^ d = x ^ Nat.gcd d (p - 1) := by
  set κ := Nat.gcd d (p - 1) with hκdef
  have hκ : 0 < κ := Nat.gcd_pos_of_pos_left _ hd
  have hp1 : 0 < p - 1 := Nat.sub_pos_of_lt hp.out.one_lt
  set d' := d / κ
  set q' := (p - 1) / κ
  have hcop : Nat.Coprime d' q' := Nat.coprime_div_gcd_div_gcd hκ
  have hdd : d' * κ = d := Nat.div_mul_cancel (Nat.gcd_dvd_left d (p - 1))
  have hqq : q' * κ = p - 1 := Nat.div_mul_cancel (Nat.gcd_dvd_right d (p - 1))
  have hq'pos : 0 < q' := by
    rcases Nat.eq_zero_or_pos q' with h | h
    · rw [h, zero_mul] at hqq; omega
    · exact h
  obtain ⟨m, -, hm⟩ := Nat.exists_mul_mod_eq_of_coprime 1 hcop hq'pos.ne'
  -- `t = m + q'` is positive and still inverts `d'` modulo `q'`.
  refine ⟨m + q', by omega, ?_⟩
  have hmod : d' * (m + q') % q' = 1 % q' := by
    rw [Nat.mul_add, Nat.add_mul_mod_self_right, hm]
  have hpos : 1 ≤ d' * (m + q') := by
    have : 0 < d' := by
      rcases Nat.eq_zero_or_pos d' with h | h
      · rw [h, zero_mul] at hdd; omega
      · exact h
    exact Nat.one_le_iff_ne_zero.mpr (Nat.mul_ne_zero this.ne' (by omega))
  obtain ⟨n, hn⟩ : q' ∣ d' * (m + q') - 1 :=
    (Nat.modEq_iff_dvd' hpos).mp hmod.symm
  have hexp : (m + q') * d = κ + (p - 1) * n := by
    have h1 : d' * (m + q') = 1 + q' * n := by omega
    calc (m + q') * d = (d' * (m + q')) * κ := by rw [← hdd]; ring
      _ = (1 + q' * n) * κ := by rw [h1]
      _ = κ + (q' * κ) * n := by ring
      _ = κ + (p - 1) * n := by rw [hqq]
  intro x
  rw [← pow_mul, hexp]
  by_cases hx : x = 0
  · subst hx
    rw [zero_pow (by omega), zero_pow hκ.ne']
  · rw [pow_add, pow_mul, ZMod.pow_card_sub_one_eq_one hx, one_pow, mul_one]

/-- Part (a): the `d`-th powers of nonzero elements of `ZMod p` are exactly the
`gcd(d, p - 1)`-th powers of nonzero elements. -/
theorem range_pow_units_eq {p : ℕ} [Fact p.Prime] {d : ℕ} (hd : 0 < d) :
    {y : ZMod p | ∃ x : ZMod p, x ≠ 0 ∧ x ^ d = y} =
      {y : ZMod p | ∃ x : ZMod p, x ≠ 0 ∧ x ^ Nat.gcd d (p - 1) = y} := by
  obtain ⟨t, ht, hpow⟩ := pow_bezout_exponent (p := p) hd
  have hdd : d / Nat.gcd d (p - 1) * Nat.gcd d (p - 1) = d :=
    Nat.div_mul_cancel (Nat.gcd_dvd_left d (p - 1))
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    refine ⟨x ^ (d / Nat.gcd d (p - 1)), pow_ne_zero _ hx, ?_⟩
    rw [← pow_mul, hdd]
  · rintro ⟨x, hx, rfl⟩
    exact ⟨x ^ t, pow_ne_zero _ hx, hpow x⟩

/-- Part (b): a nonzero solution at the reduced exponent `κ = gcd(d, p - 1)` gives a
nonzero solution at the exponent `d`, with the same support, by `s_i = u_i ^ t`. -/
theorem bezout_witness {p : ℕ} [Fact p.Prime] {d : ℕ} (hd : 0 < d)
    {ι V : Type*} [Fintype ι] [AddCommGroup V] [Module (ZMod p) V] (col : ι → V)
    (u : ι → ZMod p) (hu : u ≠ 0) (hsum : ∑ i, u i ^ Nat.gcd d (p - 1) • col i = 0) :
    ∃ s : ι → ZMod p, s ≠ 0 ∧ (∀ i, s i = 0 ↔ u i = 0) ∧ ∑ i, s i ^ d • col i = 0 := by
  obtain ⟨t, ht, hpow⟩ := pow_bezout_exponent (p := p) hd
  refine ⟨fun i => u i ^ t, ?_, fun i => pow_eq_zero_iff ht.ne', ?_⟩
  · obtain ⟨i, hi⟩ := Function.ne_iff.mp hu
    exact Function.ne_iff.mpr ⟨i, pow_ne_zero _ hi⟩
  · simpa only [hpow] using hsum

end QSearch.ReesSdeGcd
