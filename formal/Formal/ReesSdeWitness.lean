import Mathlib.FieldTheory.ChevalleyWarning
import Formal.ReesSdeGcd

/-!
# Rees SDE: witness existence at arity `κ a + 1` (Chevalley–Warning)

Source: `docs/papers/rees-hsp/appendix-schedule2.tex`, Section "What is not shown"
(a witness exists already among `κ a + 1` columns), and the exhaustive-search arity
`κ_d g_d + 1` of the end-to-end simulation in `main.tex`.

For a finite field `K`, an exponent `κ ≥ 1` and label columns
`λ_1, …, λ_M ∈ K^a` with `M > κ a`, there is a nonzero `s ∈ K^M` with
`∑ s_i ^ κ λ_i = 0` (`exists_witness`). The `a` coordinate equations
`∑_i λ_{i,j} X_i ^ κ = 0` have total degrees summing to at most `κ a < M`, so by the
Chevalley–Warning theorem (Mathlib's `char_dvd_card_solutions_of_sum_lt`) the
characteristic divides the number of common zeros. The zero vector is one of them,
so there are at least two. No divisibility `κ ∣ p - 1` is used.

Over `ZMod p` with any exponent `d ≥ 1`, the gcd reduction of `QSearch.ReesSdeGcd`
lowers the arity to `gcd(d, p - 1) · a + 1` (`exists_witness_gcd`).

This is an existence statement only; finding the witness is not formalized.
-/

namespace QSearch.ReesSdeWitness

open MvPolynomial

variable {K : Type*} [Field K]

/-- The `j`-th coordinate of `∑_i X_i ^ κ λ_i`, as a polynomial in `M` variables. -/
noncomputable def coordPoly {M a : ℕ} (κ : ℕ) (col : Fin M → Fin a → K) (j : Fin a) :
    MvPolynomial (Fin M) K :=
  ∑ i, C (col i j) * X i ^ κ

theorem coordPoly_totalDegree_le {M a : ℕ} (κ : ℕ) (col : Fin M → Fin a → K) (j : Fin a) :
    (coordPoly κ col j).totalDegree ≤ κ := by
  unfold coordPoly
  refine (totalDegree_finsetSum _ _).trans (Finset.sup_le fun i _ => ?_)
  refine (totalDegree_mul _ _).trans ?_
  rw [totalDegree_C, totalDegree_X_pow, zero_add]

theorem eval_coordPoly {M a : ℕ} (κ : ℕ) (col : Fin M → Fin a → K) (j : Fin a)
    (x : Fin M → K) : eval x (coordPoly κ col j) = ∑ i, x i ^ κ * col i j := by
  simp [coordPoly, map_sum, mul_comm]

/-- **Witness existence (Chevalley–Warning).** For `κ ≥ 1` and `M > κ a` columns in
`K^a`, some nonzero `s` has `∑ s_i ^ κ λ_i = 0`. -/
theorem exists_witness [Fintype K] [DecidableEq K] {M a κ : ℕ} (hκ : 0 < κ) (hM : κ * a < M) (col : Fin M → Fin a → K) :
    ∃ s : Fin M → K, s ≠ 0 ∧ ∑ i, s i ^ κ • col i = 0 := by
  obtain ⟨p, hchar⟩ := CharP.exists K
  have hprime : p.Prime := CharP.char_is_prime K p
  have hdeg : (∑ j ∈ (Finset.univ : Finset (Fin a)), (coordPoly κ col j).totalDegree) <
      Fintype.card (Fin M) := by
    rw [Fintype.card_fin]
    calc (∑ j ∈ (Finset.univ : Finset (Fin a)), (coordPoly κ col j).totalDegree)
        ≤ ∑ _j ∈ (Finset.univ : Finset (Fin a)), κ :=
          Finset.sum_le_sum fun j _ => coordPoly_totalDegree_le κ col j
      _ = κ * a := by simp [mul_comm]
      _ < M := hM
  have hdvd := char_dvd_card_solutions_of_sum_lt p hdeg
  set Sol := { x : Fin M → K // ∀ j ∈ (Finset.univ : Finset (Fin a)),
    eval x (coordPoly κ col j) = 0 }
  have hzero : ∀ j ∈ (Finset.univ : Finset (Fin a)),
      eval (0 : Fin M → K) (coordPoly κ col j) = 0 := by
    intro j _
    rw [eval_coordPoly]
    simp [zero_pow hκ.ne']
  let z : Sol := ⟨0, hzero⟩
  have hdvd' : p ∣ Fintype.card Sol := by convert hdvd
  have hcard : 1 < Fintype.card Sol := lt_of_lt_of_le hprime.one_lt
    (Nat.le_of_dvd (Fintype.card_pos_iff.mpr ⟨z⟩) hdvd')
  obtain ⟨y, hy⟩ := Fintype.exists_ne_of_one_lt_card hcard z
  refine ⟨y.1, fun h => hy (Subtype.ext h), ?_⟩
  funext j
  have := y.2 j (Finset.mem_univ j)
  rw [eval_coordPoly] at this
  simpa [Finset.sum_apply] using this

/-- The same bound over `ZMod p`. -/
theorem exists_witness_zmod {p : ℕ} [Fact p.Prime] {M a κ : ℕ} (hκ : 0 < κ) (hM : κ * a < M)
    (col : Fin M → Fin a → ZMod p) :
    ∃ s : Fin M → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ κ • col i = 0 :=
  exists_witness hκ hM col

/-- At exponent `d ≥ 1` over `ZMod p`, `gcd(d, p - 1) · a + 1` columns suffice:
Chevalley–Warning at the reduced exponent, then the Bezout lift. -/
theorem exists_witness_gcd {p : ℕ} [Fact p.Prime] {M a d : ℕ} (hd : 0 < d)
    (hM : Nat.gcd d (p - 1) * a < M) (col : Fin M → Fin a → ZMod p) :
    ∃ s : Fin M → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0 := by
  obtain ⟨u, hu, hsum⟩ := exists_witness_zmod (Nat.gcd_pos_of_pos_left _ hd) hM col
  obtain ⟨s, hs, -, hssum⟩ := QSearch.ReesSdeGcd.bezout_witness hd col u hu hsum
  exact ⟨s, hs, hssum⟩

/-- Lemma `lem:app-s2-gcd`(c): when `gcd(d, p - 1) = 1`, any `a + 1` columns admit a
nonzero solution at exponent `d`. -/
theorem exists_witness_linear {p : ℕ} [Fact p.Prime] {a d : ℕ} (hd : 0 < d)
    (hκ : Nat.gcd d (p - 1) = 1) (col : Fin (a + 1) → Fin a → ZMod p) :
    ∃ s : Fin (a + 1) → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0 :=
  exists_witness_gcd hd (by rw [hκ, one_mul]; omega) col

end QSearch.ReesSdeWitness
