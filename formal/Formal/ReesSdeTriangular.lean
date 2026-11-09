import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Dimension.RankNullity
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.RingTheory.IntegralDomain
import Formal.ReesSdeGcd

/-!
# Rees SDE: correctness of the triangular two-level solver

Source: `docs/papers/rees-hsp/main.tex`, Proposition `prop:triangular-sde` and its
proof.

Fix a field `K`, a finite-dimensional `K`-space `V` (the paper's `F_p^a`), label
columns `λ_i ∈ V` and a set `D ⊆ K` of admissible weights containing `0` (the paper's
`P ∪ {0}`, `P` the nonzero `κ`-th powers). A *universal two-level contraction* enters
only through two functions `A B : K → K` (the paper's `ζ ↦ α_{cos ζ}` and
`δ ↦ β_{cos δ}`) with

* `ζ δ (A ζ + B δ) ∈ D` for all nonzero `ζ, δ` (`hAB`), and
* `A 1 + B 1 ≠ 0` (the normalisation `α_0 + β_0 = 1`, `h1`).

Both are explicit hypotheses; the existence of a contraction (the condition
`p ∉ E_2(κ)`) is not formalized.

The proof follows the paper's construction. A round with columns `S'`, a dependence
`δ` with `e = ∑ δ_i λ_i ∈ U` and `v = ∑ β(δ_i) δ_i λ_i` realizes, for every nonzero
`ζ`, the vector `ζ α(ζ) e + ζ v` with weights `ζ δ_i (α(ζ) + β(δ_i)) ∈ D`
(`roundWeight_mem`, `roundWeight_sum`). If `v ∈ U` the round closes the triangle
(`stop_witness`); otherwise `U ⊕ K v` is realized on the used columns
(`realized_extend`, the descent step of the proof read upward), and the next round
needs one column fewer. With `c` the codimension of `U`, a round uses `c + 1`
columns, so `(c + 1)(c + 2)/2` columns always suffice (`witness_aux`). The output is
a nonzero `x ∈ D^M` with `∑ x_i λ_i = 0` (`triangular_witness`). With `D` the `κ`-th
powers this is a nonzero `s` with `∑ s_i ^ κ λ_i = 0` from `(a + 1)(a + 2)/2` columns
(`triangular_sde_witness`).

`triangular_sde_of_contraction` takes the hypothesis in the paper's coset form:
`g` generates `K^×`, `α, β : Z/κ → K` with `α_0 = 1`, `β_0 = 0` and
`(α_j + β_i) g^(i+j) ∈ P ∪ {0}` for all `i, j`. `triangular_sde_zmod` adds the Bezout
lift to an exponent `d` with `gcd(d, p - 1) = κ` over `ZMod p`
(`QSearch.ReesSdeGcd`).

This is an existence proof that follows the construction step by step; it checks the
algebra, not the running time, and it does not extract an executable algorithm.
-/

namespace QSearch.ReesSdeTriangular

open Module

section Abstract

variable {K V ι : Type*} [Field K] [AddCommGroup V] [Module K V] [Fintype ι]

/-- `τ` is a sum `∑ x_i λ_i` with all weights in `D` and support in `T`. -/
def Realized (D : Set K) (col : ι → V) (T : Finset ι) (τ : V) : Prop :=
  ∃ x : ι → K, (∀ i, x i ∈ D) ∧ (∀ i, i ∉ T → x i = 0) ∧ ∑ i, x i • col i = τ

/-- The round weights `ζ δ_i (α(ζ) + β(δ_i))`. -/
def roundWeight (A B : K → K) (δ : ι → K) (ζ : K) (i : ι) : K :=
  ζ * δ i * (A ζ + B (δ i))

/-- The second-level vector `v = ∑ β(δ_i) δ_i λ_i` of a round. -/
def roundVec (B : K → K) (col : ι → V) (δ : ι → K) : V :=
  ∑ i, (B (δ i) * δ i) • col i

variable {D : Set K} {A B : K → K} {col : ι → V}

theorem realized_zero (h0 : (0 : K) ∈ D) : Realized D col ∅ 0 :=
  ⟨0, fun _ => h0, fun _ _ => rfl, by simp⟩

theorem realized_mono {T T' : Finset ι} (hTT' : T ⊆ T') {τ : V}
    (h : Realized D col T τ) : Realized D col T' τ := by
  obtain ⟨x, hxD, hxT, hxs⟩ := h
  exact ⟨x, hxD, fun i hi => hxT i fun hiT => hi (hTT' hiT), hxs⟩

omit [Fintype ι] in
/-- Adding weights with disjoint supports keeps every weight in `D`. -/
theorem add_mem_of_disjoint {S T : Finset ι} (hdisj : Disjoint S T) {x y : ι → K}
    (hxD : ∀ i, x i ∈ D) (hxT : ∀ i, i ∉ T → x i = 0)
    (hyD : ∀ i, y i ∈ D) (hyS : ∀ i, i ∉ S → y i = 0) (i : ι) : (x + y) i ∈ D := by
  by_cases hi : i ∈ S
  · have hiT : i ∉ T := Finset.disjoint_left.mp hdisj hi
    simpa [hxT i hiT] using hyD i
  · simpa [hyS i hi] using hxD i

theorem realized_add [DecidableEq ι] {S T : Finset ι} (hdisj : Disjoint S T) {τ : V}
    (hT : Realized D col T τ) {y : ι → K} (hyD : ∀ i, y i ∈ D)
    (hyS : ∀ i, i ∉ S → y i = 0) : Realized D col (T ∪ S) (τ + ∑ i, y i • col i) := by
  obtain ⟨x, hxD, hxT, hxs⟩ := hT
  refine ⟨x + y, add_mem_of_disjoint hdisj hxD hxT hyD hyS, fun i hi => ?_, ?_⟩
  · rw [Finset.mem_union, not_or] at hi
    simp [hxT i hi.1, hyS i hi.2]
  · simp [add_smul, Finset.sum_add_distrib, hxs]

omit [Fintype ι] in
/-- The round weights lie in `D`. -/
theorem roundWeight_mem (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D)
    (δ : ι → K) {ζ : K} (hζ : ζ ≠ 0) (i : ι) : roundWeight A B δ ζ i ∈ D := by
  by_cases hδ : δ i = 0
  · simpa [roundWeight, hδ] using h0
  · exact hAB ζ (δ i) hζ hδ

omit [Fintype ι] in
theorem roundWeight_support {S : Finset ι} {δ : ι → K} (hδS : ∀ i, i ∉ S → δ i = 0)
    (ζ : K) (i : ι) (hi : i ∉ S) : roundWeight A B δ ζ i = 0 := by
  simp [roundWeight, hδS i hi]

/-- A round realizes `ζ α(ζ) e + ζ v`. -/
theorem roundWeight_sum (δ : ι → K) (ζ : K) :
    ∑ i, roundWeight A B δ ζ i • col i =
      (ζ * A ζ) • (∑ i, δ i • col i) + ζ • roundVec B col δ := by
  rw [roundVec, Finset.smul_sum, Finset.smul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [smul_smul, smul_smul, ← add_smul, roundWeight]
  congr 1
  ring

/-- `c + 1` columns, with `c` the codimension of `U`, have a dependence modulo `U`,
normalised to the value `1` at one of its columns. -/
theorem exists_dependence [FiniteDimensional K V] (col : ι → V) (U : Submodule K V)
    (S' : Finset ι) (hcard : finrank K V < finrank K U + S'.card) :
    ∃ δ : ι → K, (∀ i, i ∉ S' → δ i = 0) ∧ (∃ i0 ∈ S', δ i0 = 1) ∧
      ∑ i, δ i • col i ∈ U := by
  classical
  let f : S' → V ⧸ U := fun j => U.mkQ (col j)
  have hnli : ¬ LinearIndependent K f := by
    intro hli
    have h1 := hli.fintype_card_le_finrank
    rw [Fintype.card_coe] at h1
    have h2 := U.finrank_quotient_add_finrank
    omega
  obtain ⟨g, hg, j0, hj0⟩ := Fintype.not_linearIndependent_iff.mp hnli
  let δ : ι → K := fun i => if h : i ∈ S' then (g j0)⁻¹ * g ⟨i, h⟩ else 0
  refine ⟨δ, fun i hi => by simp [δ, hi], ⟨j0.1, j0.2, by simp [δ, j0.2, hj0]⟩, ?_⟩
  have key : ∑ i, δ i • col i = (g j0)⁻¹ • ∑ j : S', g j • col j := by
    rw [← Finset.sum_subset (Finset.subset_univ S') (fun i _ hi => by simp [δ, hi]),
      ← Finset.sum_coe_sort S', Finset.smul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    simp [δ, j.2, smul_smul]
  have hq : U.mkQ (∑ i, δ i • col i) = 0 := by
    rw [key, map_smul, map_sum]
    simp only [map_smul]
    rw [show (∑ j : S', g j • U.mkQ (col j)) = ∑ j : S', g j • f j from rfl, hg, smul_zero]
  rwa [← LinearMap.mem_ker, Submodule.ker_mkQ] at hq

/-- The descent step, read upward: if `U` is realized on `T` and a round on `S'`
(disjoint from `T`) has `e ∈ U`, then `U ⊔ K v` is realized on `T ∪ S'`. -/
theorem realized_extend [DecidableEq ι] (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D)
    (U : Submodule K V) {T S' : Finset ι} (hdisj : Disjoint S' T) {δ : ι → K}
    (hδS : ∀ i, i ∉ S' → δ i = 0) (he : ∑ i, δ i • col i ∈ U)
    (hU : ∀ τ ∈ U, Realized D col T τ) :
    ∀ τ ∈ U ⊔ K ∙ roundVec B col δ, Realized D col (T ∪ S') τ := by
  intro τ hτ
  obtain ⟨u, hu, w, hw, rfl⟩ := Submodule.mem_sup.mp hτ
  obtain ⟨ζ, rfl⟩ := Submodule.mem_span_singleton.mp hw
  by_cases hζ : ζ = 0
  · subst hζ
    simpa using realized_mono Finset.subset_union_left (hU u hu)
  · have hr := realized_add hdisj
      (hU (u - (ζ * A ζ) • ∑ i, δ i • col i) (U.sub_mem hu (U.smul_mem _ he)))
      (roundWeight_mem h0 hAB δ hζ) (roundWeight_support hδS ζ)
    rw [roundWeight_sum] at hr
    convert hr using 1
    abel

/-- The stopping round: if `v ∈ U`, the realisation `R` with `ζ = 1` lies in `U`, and
`-R`, realized on `T`, closes the triangle with weight `α_0 + β_0 ≠ 0` at `i0`. -/
theorem stop_witness (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (U : Submodule K V) {T S' : Finset ι} (hdisj : Disjoint S' T) {δ : ι → K}
    (hδS : ∀ i, i ∉ S' → δ i = 0) {i0 : ι} (hi0 : i0 ∈ S') (hδi0 : δ i0 = 1)
    (he : ∑ i, δ i • col i ∈ U) (hv : roundVec B col δ ∈ U)
    (hU : ∀ τ ∈ U, Realized D col T τ) :
    ∃ x : ι → K, (∀ i, x i ∈ D) ∧ x ≠ 0 ∧ ∑ i, x i • col i = 0 := by
  set y := roundWeight A B δ 1
  have hR : ∑ i, y i • col i ∈ U := by
    rw [roundWeight_sum]
    exact U.add_mem (U.smul_mem _ he) (U.smul_mem _ hv)
  obtain ⟨x, hxD, hxT, hxs⟩ := hU _ (U.neg_mem hR)
  have hyD := roundWeight_mem h0 hAB δ one_ne_zero (A := A) (B := B)
  refine ⟨x + y, add_mem_of_disjoint hdisj hxD hxT hyD (roundWeight_support hδS 1), ?_, ?_⟩
  · intro hzero
    have hx0 : x i0 = 0 := hxT i0 (Finset.disjoint_left.mp hdisj hi0)
    have := congrFun hzero i0
    simp only [Pi.add_apply, hx0, zero_add, Pi.zero_apply, y, roundWeight, hδi0,
      one_mul] at this
    exact h1 this
  · simp [add_smul, Finset.sum_add_distrib, hxs]

/-- The triangular induction on the codimension `c` of the realized subspace. -/
theorem witness_aux [DecidableEq ι] [FiniteDimensional K V] (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (col : ι → V) (c : ℕ) :
    ∀ (U : Submodule K V) (T S : Finset ι), finrank K V ≤ finrank K U + c →
      Disjoint S T → (c + 1) * (c + 2) ≤ 2 * S.card → (∀ τ ∈ U, Realized D col T τ) →
      ∃ x : ι → K, (∀ i, x i ∈ D) ∧ x ≠ 0 ∧ ∑ i, x i • col i = 0 := by
  induction c using Nat.strong_induction_on with
  | _ c ih =>
  intro U T S hc hdisj hS hU
  obtain ⟨S', hS'S, hS'card⟩ :=
    Finset.exists_subset_card_eq (show c + 1 ≤ S.card by nlinarith)
  obtain ⟨δ, hδS, ⟨i0, hi0, hδi0⟩, he⟩ :=
    exists_dependence col U S' (by omega)
  have hdisj' : Disjoint S' T := Finset.disjoint_of_subset_left hS'S hdisj
  by_cases hv : roundVec B col δ ∈ U
  · exact stop_witness h0 hAB h1 U hdisj' hδS hi0 hδi0 he hv hU
  · set U' := U ⊔ K ∙ roundVec B col δ
    have hlt : U < U' := lt_of_le_of_ne le_sup_left fun h => hv (by
      rw [h]; exact Submodule.mem_sup_right (Submodule.mem_span_singleton_self _))
    have hfr : finrank K U < finrank K U' := Submodule.finrank_lt_finrank_of_lt hlt
    have hle : finrank K U' ≤ finrank K V := Submodule.finrank_le U'
    obtain ⟨c', rfl⟩ : ∃ c', c = c' + 1 := ⟨c - 1, by omega⟩
    have hsd : (S \ S').card + (c' + 2) = S.card := by
      rw [Finset.card_sdiff_of_subset hS'S, hS'card]
      have : c' + 1 + 1 ≤ S.card := hS'card ▸ Finset.card_le_card hS'S
      omega
    refine ih c' (by omega) U' (T ∪ S') (S \ S') (by omega) ?_ ?_
      (realized_extend h0 hAB U hdisj' hδS he hU)
    · exact Finset.disjoint_union_right.mpr
        ⟨Finset.disjoint_of_subset_left Finset.sdiff_subset hdisj, Finset.sdiff_disjoint⟩
    · set P := (c' + 1) * (c' + 2)
      have hP : (c' + 1 + 1) * (c' + 1 + 2) = P + 2 * (c' + 2) := by simp only [P]; ring
      omega

/-- **Triangular two-level solver, abstract form.** If `0 ∈ D`, `hAB` and `h1` hold,
then from `(n + 1)(n + 2)/2` columns, `n = dim V`, there is a nonzero `x ∈ D^ι` with
`∑ x_i λ_i = 0`. -/
theorem triangular_witness [DecidableEq ι] [FiniteDimensional K V] (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (col : ι → V) (hM : (finrank K V + 1) * (finrank K V + 2) ≤ 2 * Fintype.card ι) :
    ∃ x : ι → K, (∀ i, x i ∈ D) ∧ x ≠ 0 ∧ ∑ i, x i • col i = 0 :=
  witness_aux h0 hAB h1 col (finrank K V) ⊥ ∅ Finset.univ (by simp)
    (Finset.disjoint_empty_right _) (by simpa using hM)
    (fun τ hτ => by rw [Submodule.mem_bot] at hτ; subst hτ; exact realized_zero h0)

end Abstract

section Powers

variable {K : Type*} [Field K]

/-- `(a + 1)(a + 2)` is even, so the paper's count `(a + 1)(a + 2)/2` is exact. -/
theorem two_mul_triangle (a : ℕ) : 2 * ((a + 1) * (a + 2) / 2) = (a + 1) * (a + 2) :=
  Nat.mul_div_cancel' (Nat.even_mul_succ_self (a + 1)).two_dvd

/-- **Triangular two-level solver, `κ`-th powers.** Under `hAB` (with `D` the
`κ`-th powers) and `h1`, any `M ≥ (a + 1)(a + 2)/2` columns in `K^a` admit a nonzero
`s` with `∑ s_i ^ κ λ_i = 0`. -/
theorem triangular_sde_witness {κ : ℕ} (hκ : 0 < κ) (A B : K → K)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ∃ w : K, ζ * δ * (A ζ + B δ) = w ^ κ)
    (h1 : A 1 + B 1 ≠ 0) {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M)
    (col : Fin M → Fin a → K) :
    ∃ s : Fin M → K, s ≠ 0 ∧ ∑ i, s i ^ κ • col i = 0 := by
  let D : Set K := {y | ∃ w : K, y = w ^ κ}
  have h0 : (0 : K) ∈ D := ⟨0, (zero_pow hκ.ne').symm⟩
  have hAB' : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D := fun ζ δ hζ hδ => by
    obtain ⟨w, hw⟩ := hAB ζ δ hζ hδ
    exact ⟨w, hw⟩
  have hM' : (finrank K (Fin a → K) + 1) * (finrank K (Fin a → K) + 2) ≤
      2 * Fintype.card (Fin M) := by
    rw [Module.finrank_fin_fun, Fintype.card_fin, ← two_mul_triangle a]
    omega
  obtain ⟨x, hxD, hx0, hxs⟩ := triangular_witness h0 hAB' h1 col hM'
  choose s hs using hxD
  refine ⟨s, fun hs0 => hx0 (funext fun i => ?_), ?_⟩
  · rw [hs i, hs0, Pi.zero_apply, zero_pow hκ.ne']
  · simpa only [hs] using hxs

/-- The arithmetic of the contraction condition: `ζ ∈ g^{n₁} P`, `δ ∈ g^{n₂} P` and
`c g^r ∈ P ∪ {0}` with `n₁ + n₂ = r + q κ` give `ζ δ c ∈ P ∪ {0}`. -/
theorem coset_product {κ : ℕ} {ζ δ c g w₁ w₂ w : K} {n₁ n₂ r q : ℕ}
    (hζ : ζ = g ^ n₁ * w₁ ^ κ) (hδ : δ = g ^ n₂ * w₂ ^ κ) (hw : c * g ^ r = w ^ κ)
    (hn : n₁ + n₂ = r + q * κ) : ζ * δ * c = (w * (g ^ q * w₁ * w₂)) ^ κ := by
  subst hζ hδ
  have hpow : g ^ n₁ * g ^ n₂ = g ^ r * (g ^ q) ^ κ := by
    rw [← pow_add, ← pow_mul, ← pow_add, hn]
  calc g ^ n₁ * w₁ ^ κ * (g ^ n₂ * w₂ ^ κ) * c
      = (g ^ n₁ * g ^ n₂) * w₁ ^ κ * w₂ ^ κ * c := by ring
    _ = (c * g ^ r) * (g ^ q * w₁ * w₂) ^ κ := by rw [hpow]; ring
    _ = (w * (g ^ q * w₁ * w₂)) ^ κ := by rw [hw]; ring

/-- A coset index for a generator: `ind 1 = 0` and `y ∈ g^{ind y} P` for `y ≠ 0`. -/
theorem exists_coset_index (κ : ℕ) [NeZero κ] (g : K)
    (hgen : ∀ y : K, y ≠ 0 → ∃ n : ℕ, g ^ n = y) :
    ∃ ind : K → ZMod κ, ind 1 = 0 ∧
      ∀ y : K, y ≠ 0 → ∃ w : K, y = g ^ (ind y).val * w ^ κ := by
  classical
  refine ⟨fun y => if h : y ≠ 0 ∧ y ≠ 1 then ((Classical.choose (hgen y h.1) : ℕ) : ZMod κ)
    else 0, by simp, fun y hy => ?_⟩
  by_cases h1 : y = 1
  · subst h1
    exact ⟨1, by simp⟩
  · have h : y ≠ 0 ∧ y ≠ 1 := ⟨hy, h1⟩
    set n := Classical.choose (hgen y hy)
    have hn : g ^ n = y := Classical.choose_spec (hgen y hy)
    refine ⟨g ^ (n / κ), ?_⟩
    beta_reduce
    split_ifs
    rw [ZMod.val_natCast, ← pow_mul, ← pow_add, Nat.mod_add_div', hn]

/-- Every finite field has a generator of its multiplicative group. -/
theorem exists_generator [Fintype K] : ∃ g : K, ∀ y : K, y ≠ 0 → ∃ n : ℕ, g ^ n = y := by
  obtain ⟨g, hg⟩ := IsCyclic.exists_generator (α := Kˣ)
  refine ⟨g, fun y hy => ?_⟩
  obtain ⟨n, hn⟩ := Submonoid.mem_powers_iff _ _ |>.mp
    (mem_powers_iff_mem_zpowers.mpr (hg (Units.mk0 y hy)))
  exact ⟨n, by rw [← Units.val_pow_eq_pow_val, hn, Units.val_mk0]⟩

/-- **Proposition `prop:triangular-sde`, coset form.** Let `g` generate `K^×`, `κ ≥ 1`,
and let `α, β : Z/κ → K` be a universal two-level contraction normalised by
`α_0 = 1`, `β_0 = 0`: `(α_j + β_i) g^(i+j) ∈ P ∪ {0}` for all `i, j`. Then any
`M ≥ (a + 1)(a + 2)/2` columns in `K^a` admit a nonzero `s` with
`∑ s_i ^ κ λ_i = 0`. -/
theorem triangular_sde_of_contraction {κ : ℕ} [NeZero κ] (g : K)
    (hgen : ∀ y : K, y ≠ 0 → ∃ n : ℕ, g ^ n = y) (α β : ZMod κ → K)
    (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod κ, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ κ)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → K) :
    ∃ s : Fin M → K, s ≠ 0 ∧ ∑ i, s i ^ κ • col i = 0 := by
  obtain ⟨ind, hind1, hind⟩ := exists_coset_index κ g hgen
  refine triangular_sde_witness (Nat.pos_of_ne_zero (NeZero.ne κ))
    (fun ζ => α (ind ζ)) (fun δ => β (ind δ)) (fun ζ δ hζ hδ => ?_)
    (by simp [hind1, hα0, hβ0]) hM col
  obtain ⟨w₁, hw₁⟩ := hind ζ hζ
  obtain ⟨w₂, hw₂⟩ := hind δ hδ
  obtain ⟨w, hw⟩ := hC (ind δ) (ind ζ)
  refine ⟨_, coset_product hw₁ hw₂ hw (q := ((ind δ).val + (ind ζ).val) / κ) ?_⟩
  rw [ZMod.val_add, add_comm (ind ζ).val]
  have := Nat.mod_add_div ((ind δ).val + (ind ζ).val) κ
  rw [mul_comm]
  omega

/-- **Over `ZMod p`, at exponent `d`.** With `κ = gcd(d, p - 1)`, a generator `g` of
`(ZMod p)^×` and a normalised contraction at `κ`, any `M ≥ (a + 1)(a + 2)/2` columns
in `(ZMod p)^a` admit a nonzero `s` with `∑ s_i ^ d λ_i = 0` (the triangular solver
followed by the Bezout lift of `lem:app-s2-gcd`). -/
theorem triangular_sde_zmod {p : ℕ} [Fact p.Prime] {d : ℕ} (hd : 0 < d) (g : ZMod p)
    (hgen : ∀ y : ZMod p, y ≠ 0 → ∃ n : ℕ, g ^ n = y)
    (α β : ZMod (Nat.gcd d (p - 1)) → ZMod p) (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod (Nat.gcd d (p - 1)), ∃ w : ZMod p,
      (α j + β i) * g ^ (i + j).val = w ^ Nat.gcd d (p - 1))
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → ZMod p) :
    ∃ s : Fin M → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0 := by
  have : NeZero (Nat.gcd d (p - 1)) := ⟨(Nat.gcd_pos_of_pos_left _ hd).ne'⟩
  obtain ⟨u, hu, hsum⟩ := triangular_sde_of_contraction g hgen α β hα0 hβ0 hC hM col
  obtain ⟨s, hs, -, hssum⟩ := QSearch.ReesSdeGcd.bezout_witness hd col u hu hsum
  exact ⟨s, hs, hssum⟩

/-- Non-vacuity at `p = 3`, `κ = 2`, `g = 2`: `α = (1, 0)`, `β = (0, 1)` is a
normalised contraction. -/
theorem contraction_three :
    ∀ i j : ZMod 2, ∃ w : ZMod 3,
      (![1, 0] j + ![0, 1] i) * (2 : ZMod 3) ^ (i + j).val = w ^ 2 := by
  decide

theorem generator_three : ∀ y : ZMod 3, y ≠ 0 → ∃ n : ℕ, (2 : ZMod 3) ^ n = y := by
  intro y hy
  fin_cases y
  · exact absurd rfl hy
  · exact ⟨0, rfl⟩
  · exact ⟨1, rfl⟩

/-- The instance: any `(a + 1)(a + 2)/2` columns in `F_3^a` have a nonzero `s` with
`∑ s_i ^ 2 λ_i = 0`. -/
theorem triangular_sde_three {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M)
    (col : Fin M → Fin a → ZMod 3) :
    ∃ s : Fin M → ZMod 3, s ≠ 0 ∧ ∑ i, s i ^ 2 • col i = 0 :=
  triangular_sde_of_contraction (κ := 2) 2 generator_three ![1, 0] ![0, 1] rfl rfl
    contraction_three hM col

end Powers

end QSearch.ReesSdeTriangular
