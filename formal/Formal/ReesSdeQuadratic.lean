import Mathlib.NumberTheory.LegendreSymbol.QuadraticChar.Basic
import Formal.ReesSdeTriangular

/-!
# Rees SDE: the triangular solver at `κ = 2`, with no contraction hypothesis

Source: `docs/papers/rees-hsp/main.tex`, Proposition `prop:triangular-sde` and the
contraction `(α, β) = ((1, 0), (0, μ))` of Lemma `lem:coherent-quadratic-sde`
(`μ = ν - 1`, `ν` a quadratic non-residue with `ν - 1` a nonzero square).

`QSearch.ReesSdeTriangular` proves the triangular solver from an explicit universal
two-level contraction. At `κ = 2` this file constructs one over `ZMod p` for every odd
prime `p`, so the hypothesis is discharged there (`p ∉ E_2(2)` in the paper's notation):

* `nonsquare_mul_nonsquare`: in a finite field the product of two non-squares is a
  square (quadratic character).
* `exists_consecutive_nonsquare`: over `ZMod p`, `p` odd, the least non-residue `ν`
  gives a nonzero square `μ = ν - 1` with `1 + μ` a non-square.
* `quadratic_contraction`: the functions `A ζ = [ζ square]`, `B δ = μ [δ non-square]`
  satisfy the hypotheses `hAB`, `h1` of `triangular_sde_witness` at `κ = 2`.
* `contraction_two`: the same contraction in the paper's coset form
  `(α_j + β_i) g^(i+j) ∈ P ∪ {0}`, `α = (1, 0)`, `β = (0, μ)`, for every generator `g`
  of `(ZMod p)^×`.
* `triangular_sde_quadratic`: any `(a + 1)(a + 2)/2` columns in `(ZMod p)^a` admit a
  nonzero `s` with `∑ s_i ^ 2 λ_i = 0`; `triangular_sde_gcd_two`: the same at every
  exponent `d` with `gcd(d, p - 1) = 2` (Bezout lift).

This is an existence statement that follows the construction; running time and the
root extraction of the algorithm are not formalized.
-/

namespace QSearch.ReesSdeQuadratic

open QSearch.ReesSdeTriangular

section FiniteField

variable {K : Type*} [Field K] [Fintype K]

/-- In a finite field, the product of two non-squares is a square. -/
theorem nonsquare_mul_nonsquare [DecidableEq K] {a b : K} (ha : ¬IsSquare a)
    (hb : ¬IsSquare b) : IsSquare (a * b) := by
  have ha0 : a ≠ 0 := fun h => ha (h ▸ IsSquare.zero)
  have hb0 : b ≠ 0 := fun h => hb (h ▸ IsSquare.zero)
  rw [← quadraticChar_one_iff_isSquare (mul_ne_zero ha0 hb0), map_mul,
    quadraticChar_neg_one_iff_not_isSquare.mpr ha, quadraticChar_neg_one_iff_not_isSquare.mpr hb]
  norm_num

omit [Fintype K] in
theorem exists_sq_of_isSquare {x : K} (h : IsSquare x) : ∃ w : K, x = w ^ 2 := by
  obtain ⟨r, hr⟩ := h
  exact ⟨r, by rw [hr, sq]⟩

/-- The two-level contraction at `κ = 2`: given a nonzero square `μ` with `1 + μ` a
non-square, `A ζ = [ζ square]` and `B δ = μ [δ non-square]` satisfy
`ζ δ (A ζ + B δ) ∈ (K^×)^2 ∪ {0}` for all nonzero `ζ, δ`, and `A 1 + B 1 = 1`. -/
theorem quadratic_contraction [DecidableEq K] {μ : K} (hμ : IsSquare μ)
    (hν : ¬IsSquare (1 + μ)) :
    (∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 →
      ∃ w : K, ζ * δ * ((if IsSquare ζ then 1 else 0) + (if IsSquare δ then 0 else μ)) =
        w ^ 2) ∧
      (if IsSquare (1 : K) then (1 : K) else 0) + (if IsSquare (1 : K) then 0 else μ) ≠ 0 := by
  classical
  refine ⟨fun ζ δ _ _ => exists_sq_of_isSquare ?_, by simp⟩
  by_cases hζ : IsSquare ζ <;> by_cases hδ : IsSquare δ <;> simp only [hζ, hδ, ↓reduceIte]
  · simpa using hζ.mul hδ
  · rw [mul_assoc]
    exact hζ.mul (nonsquare_mul_nonsquare hδ hν)
  · simp
  · rw [zero_add]
    exact (nonsquare_mul_nonsquare hζ hδ).mul hμ

omit [Fintype K] in
/-- A generator of `K^×` is a non-square when `K` has a non-square. -/
theorem generator_not_isSquare {g : K} (hgen : ∀ y : K, y ≠ 0 → ∃ n : ℕ, g ^ n = y)
    {ν : K} (hν : ¬IsSquare ν) : ¬IsSquare g := by
  rintro ⟨r, hr⟩
  apply hν
  have hν0 : ν ≠ 0 := fun h => hν (h ▸ IsSquare.zero)
  obtain ⟨n, rfl⟩ := hgen ν hν0
  exact ⟨r ^ n, by rw [hr, mul_pow]⟩

end FiniteField

section PrimeField

variable {p : ℕ} [hp : Fact p.Prime]

/-- Over `ZMod p`, `p` odd, the least non-residue `ν` gives a nonzero square
`μ = ν - 1` with `1 + μ = ν` a non-square. -/
theorem exists_consecutive_nonsquare (hp2 : p ≠ 2) :
    ∃ μ : ZMod p, μ ≠ 0 ∧ IsSquare μ ∧ ¬IsSquare (1 + μ) := by
  classical
  have hchar : ringChar (ZMod p) ≠ 2 := by rwa [ZMod.ringChar_zmod_n]
  obtain ⟨x, hx⟩ := FiniteField.exists_nonsquare hchar
  have hex : ∃ n : ℕ, ¬IsSquare ((n : ℕ) : ZMod p) := ⟨x.val, by rwa [ZMod.natCast_zmod_val]⟩
  set n := Nat.find hex with hn
  have hns : ¬IsSquare ((n : ℕ) : ZMod p) := Nat.find_spec hex
  have hnle : n ≤ x.val := Nat.find_min' hex (by rwa [ZMod.natCast_zmod_val])
  have hxlt : x.val < p := ZMod.val_lt x
  have hn0 : n ≠ 0 := fun h => hns (by rw [h, Nat.cast_zero]; exact IsSquare.zero)
  have hn1 : n ≠ 1 := fun h => hns (by rw [h, Nat.cast_one]; exact IsSquare.one)
  obtain ⟨m, hm⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  have hmsq : IsSquare ((m : ℕ) : ZMod p) := by
    have := Nat.find_min hex (show m < n by omega)
    simpa using this
  refine ⟨(m : ZMod p), ?_, hmsq, ?_⟩
  · rw [Ne, ZMod.natCast_eq_zero_iff]
    intro hdvd
    exact absurd (Nat.le_of_dvd (by omega) hdvd) (by omega)
  · have hcast : (1 : ZMod p) + (m : ZMod p) = ((n : ℕ) : ZMod p) := by
      rw [hm, Nat.cast_succ, add_comm]
    rw [hcast]
    exact hns

/-- **The contraction at `κ = 2` exists** (`p ∉ E_2(2)`), in the hypothesis form of
`triangular_sde_witness`. -/
theorem exists_quadratic_contraction (hp2 : p ≠ 2) :
    ∃ A B : ZMod p → ZMod p,
      (∀ ζ δ : ZMod p, ζ ≠ 0 → δ ≠ 0 → ∃ w : ZMod p, ζ * δ * (A ζ + B δ) = w ^ 2) ∧
        A 1 + B 1 ≠ 0 := by
  classical
  obtain ⟨μ, -, hμ, hν⟩ := exists_consecutive_nonsquare hp2
  exact ⟨_, _, quadratic_contraction hμ hν⟩

/-- **The contraction at `κ = 2` in the paper's coset form.** For every generator `g`
of `(ZMod p)^×`, `p` odd, `α = (1, 0)` and `β = (0, μ)` with `μ = ν - 1` satisfy the
normalisation `α_0 = 1`, `β_0 = 0` and `(α_j + β_i) g^(i+j) ∈ P ∪ {0}`. -/
theorem contraction_two (hp2 : p ≠ 2) (g : ZMod p)
    (hgen : ∀ y : ZMod p, y ≠ 0 → ∃ n : ℕ, g ^ n = y) :
    ∃ μ : ZMod p, μ ≠ 0 ∧ ∀ i j : ZMod 2, ∃ w : ZMod p,
      (![1, 0] j + ![0, μ] i) * g ^ (i + j).val = w ^ 2 := by
  classical
  obtain ⟨μ, hμ0, hμ, hν⟩ := exists_consecutive_nonsquare hp2
  have hg := generator_not_isSquare hgen hν
  refine ⟨μ, hμ0, fun i j => ?_⟩
  have hgsq := nonsquare_mul_nonsquare hν hg
  have key : ∀ i j : Fin 2, ∃ w : ZMod p,
      (![1, 0] j + ![0, μ] i) * g ^ ((i + j : Fin 2) : ℕ) = w ^ 2 := by
    intro i j
    fin_cases i <;> fin_cases j
    · exact ⟨1, by simp⟩
    · exact ⟨0, by simp⟩
    · obtain ⟨w, hw⟩ := exists_sq_of_isSquare hgsq
      exact ⟨w, by simpa using hw⟩
    · obtain ⟨w, hw⟩ := exists_sq_of_isSquare hμ
      exact ⟨w, by simpa using hw⟩
  exact key i j

/-- **Triangular solver at `κ = 2`, unconditional.** For every odd prime `p`, any
`M ≥ (a + 1)(a + 2)/2` columns in `(ZMod p)^a` admit a nonzero `s` with
`∑ s_i ^ 2 λ_i = 0`. -/
theorem triangular_sde_quadratic (hp2 : p ≠ 2) {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M)
    (col : Fin M → Fin a → ZMod p) :
    ∃ s : Fin M → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ 2 • col i = 0 := by
  obtain ⟨A, B, hAB, h1⟩ := exists_quadratic_contraction hp2
  exact triangular_sde_witness (by norm_num) A B hAB h1 hM col

/-- **At every exponent `d` with `gcd(d, p - 1) = 2`**, any `(a + 1)(a + 2)/2` columns
in `(ZMod p)^a` admit a nonzero `s` with `∑ s_i ^ d λ_i = 0` (the solver at `κ = 2`
followed by the Bezout lift of `lem:app-s2-gcd`). -/
theorem triangular_sde_gcd_two {d : ℕ} (hd : 0 < d) (hκ : Nat.gcd d (p - 1) = 2)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → ZMod p) :
    ∃ s : Fin M → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0 := by
  have hp2 : p ≠ 2 := by
    rintro rfl
    have := Nat.gcd_dvd_right d (2 - 1)
    rw [hκ] at this
    norm_num at this
  obtain ⟨u, hu, hsum⟩ := triangular_sde_quadratic hp2 hM col
  obtain ⟨s, hs, -, hssum⟩ := QSearch.ReesSdeGcd.bezout_witness hd col u hu
    (by rw [hκ]; exact hsum)
  exact ⟨s, hs, hssum⟩

end PrimeField

end QSearch.ReesSdeQuadratic

/-- info: 'QSearch.ReesSdeQuadratic.nonsquare_mul_nonsquare' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.nonsquare_mul_nonsquare

/-- info: 'QSearch.ReesSdeQuadratic.exists_consecutive_nonsquare' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.exists_consecutive_nonsquare

/-- info: 'QSearch.ReesSdeQuadratic.exists_quadratic_contraction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.exists_quadratic_contraction

/-- info: 'QSearch.ReesSdeQuadratic.contraction_two' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.contraction_two

/-- info: 'QSearch.ReesSdeQuadratic.triangular_sde_quadratic' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.triangular_sde_quadratic

/-- info: 'QSearch.ReesSdeQuadratic.triangular_sde_gcd_two' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeQuadratic.triangular_sde_gcd_two
