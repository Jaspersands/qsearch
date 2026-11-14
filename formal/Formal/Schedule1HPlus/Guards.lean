import Formal.Schedule1HPlus.Tensor
import Formal.Schedule1HPlus.Stage
import Mathlib.Data.ZMod.Units

/-!
# Schedule 1H⁺, part 5: decidable guards and a concrete instance

* `isRC_zero_iff_check`: over a finite field, an `RC(D; Δ → {0})` contraction is the
  decidable condition "`(α_0+β_0)^h = 1`, and for all `i ∈ Δ`, `j`: `α_j + β_i = 0` or
  `((α_j + β_i) ξ^{i+j})^h = 1`" (`D h = |K| - 1`).
* At `p = 229` with `ξ = g = 6` (a primitive root, proved here by `decide`), the certificate
  of `TL_6 = (6, ℤ_6, {0})` stored in
  `research/audits/reviews/2026-11-13-rees-headline-below-38/v2/certs_tl6_all.json`
  (entry `"229"`) is checked by `decide` (`tl6_229`), and a perturbed table is rejected
  (`tl6_229_perturbed`). `p = 229` is the least prime there with a `TL_6` certificate.
* `tl6_chain_229` / `tl6_solver_229`: the chain `(Gaussian elimination; TL_6)` of
  Corollary `cor:plus-chain` over `F_229` is a `{0}`-node at modulus `6` and, with sixth
  roots, a `6`-solver, of arity `(a+1)(5a+1)` (`tl6_arity_229`), for every
  finite-dimensional space of columns. This shows that the hypotheses of `chain_spec` are
  satisfiable at a real step.
* `TL_3` at `p = 7`, `ξ = g = 3`, entry `"7"` of `certs_stage1.json` (`tl3_7`).

`decide` only; no `native_decide`.
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset Module

section Check

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K] {N : ℕ}

/-- **Decidable form of Definition `def:plus-rc` for `Ω = {0}`.** -/
theorem isRC_zero_iff_check (C : ClassMap K N) {D h : ℕ} (hD : D ∣ N)
    (hDh : D * h = Fintype.card K - 1) (hh : 0 < h) (Δ : Finset (ZMod D))
    (α β : ZMod D → K) :
    IsRC C D ↑Δ {0} α β ↔
      ((α 0 + β 0 ≠ 0 ∧ (α 0 + β 0) ^ h = 1) ∧
        ∀ i ∈ Δ, ∀ j : ZMod D, α j + β i = 0 ∨ ((α j + β i) * C.xi ^ (i + j).val) ^ h = 1) := by
  haveI := C.neZero_of_dvd hD
  have hcl : ∀ (x : K) (i j : ZMod D), x ≠ 0 →
      (C.cl D x + i + j = 0 ↔ (x * C.xi ^ (i + j).val) ^ h = 1) := by
    intro x i j hx
    have hne : x * C.xi ^ (i + j).val ≠ 0 := mul_ne_zero hx (pow_ne_zero _ C.xi_ne)
    rw [← C.cl_eq_zero_iff_pow hD hDh hh hne, C.cl_mul hD hx (pow_ne_zero _ C.xi_ne),
      C.cl_xi_pow hD, ZMod.natCast_zmod_val, add_assoc]
  constructor
  · rintro ⟨hb, hc⟩
    refine ⟨⟨hb.1, (ClassMap.mem_pow_iff_pow_eq_one hDh hh hb.1).mp hb⟩, fun i hi j => ?_⟩
    rcases hc i hi j with h0 | h1
    · exact Or.inl h0
    · by_cases hx : α j + β i = 0
      · exact Or.inl hx
      · exact Or.inr ((hcl _ i j hx).mp h1)
  · rintro ⟨⟨hb0, hb1⟩, hc⟩
    refine ⟨(ClassMap.mem_pow_iff_pow_eq_one hDh hh hb0).mpr hb1, fun i hi j => ?_⟩
    rcases hc i hi j with h0 | h1
    · exact Or.inl h0
    · by_cases hx : α j + β i = 0
      · exact Or.inl hx
      · exact Or.inr ((hcl _ i j hx).mpr h1)

end Check

section P229

instance fact229 : Fact (Nat.Prime 229) := ⟨by norm_num⟩

/-- `6` as a unit of `F_229`. -/
def g229 : (ZMod 229)ˣ := ZMod.unitOfCoprime 6 (by norm_num)

theorem g229_val : (g229 : ZMod 229) = 6 := by simp [g229]

/-- `6` is a primitive root mod `229` (`228 = 2^2 · 3 · 19`). -/
theorem orderOf_g229 : orderOf g229 = Fintype.card (ZMod 229) - 1 := by
  rw [ZMod.card]
  refine orderOf_eq_of_pow_and_pow_div_prime (by norm_num) ?_ ?_
  · rw [Units.ext_iff, Units.val_pow_eq_pow_val, g229_val, Units.val_one]; decide
  · intro q hq hdvd
    have h228 : q ∣ 2 ^ 2 * 3 * 19 := by norm_num; exact hdvd
    rw [Ne, Units.ext_iff, Units.val_pow_eq_pow_val, g229_val, Units.val_one]
    rcases (Nat.Prime.dvd_mul hq).mp h228 with h | h
    · rcases (Nat.Prime.dvd_mul hq).mp h with h | h
      · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_two).mp (hq.dvd_of_dvd_pow h)
        decide
      · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_three).mp h
        decide
    · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq (by norm_num)).mp h
      decide

/-- The class map of `ξ = g = 6` over `F_229` (`N = 228`). -/
noncomputable def C229 : ClassMap (ZMod 229) (Fintype.card (ZMod 229) - 1) :=
  ClassMap.ofGen g229 (ClassMap.gen_of_orderOf orderOf_g229) (by rw [ZMod.card]; norm_num)

theorem C229_xi : C229.xi = 6 := g229_val

/-- `α` of the `TL_6` certificate at `p = 229`. -/
def al229 : ZMod 6 → ZMod 229 := fun i =>
  ([1, 198, 100, 141, 0, 223] : List (ZMod 229)).getD i.val 0

/-- `β` of the `TL_6` certificate at `p = 229`. -/
def be229 : ZMod 6 → ZMod 229 := fun i =>
  ([0, 6, 228, 31, 129, 88] : List (ZMod 229)).getD i.val 0

theorem dvd6_229 : 6 ∣ Fintype.card (ZMod 229) - 1 := by rw [ZMod.card]; norm_num

theorem h6_229 : 6 * 38 = Fintype.card (ZMod 229) - 1 := by rw [ZMod.card]

/-- **`TL_6` is available at `p = 229`** (certificate checked by `decide`). -/
theorem tl6_229 : IsRC C229 6 ↑(Finset.univ : Finset (ZMod 6)) {0} al229 be229 := by
  rw [isRC_zero_iff_check C229 dvd6_229 h6_229 (by norm_num), C229_xi]
  decide

/-- Negative control: the table with `α_1` changed is **not** a contraction. -/
theorem tl6_229_perturbed :
    ¬ IsRC C229 6 ↑(Finset.univ : Finset (ZMod 6)) {0} (al229 + Pi.single 1 1) be229 := by
  rw [isRC_zero_iff_check C229 dvd6_229 h6_229 (by norm_num), C229_xi]
  decide

/-- The step `TL_6` with its certificate. -/
abbrev σ229 : Step (ZMod 229) := ⟨6, Finset.univ, {0}, al229, be229⟩

theorem chainOK_229 : ChainOK C229 1 Set.univ [σ229] := by
  refine ⟨one_dvd _, one_dvd _, dvd6_229, fun i _ => by
    show i ∈ ((Finset.univ : Finset (ZMod 6)) : Set (ZMod 6))
    exact Finset.mem_coe.mpr (Finset.mem_univ _), tl6_229⟩

variable {V : Type} [AddCommGroup V] [Module (ZMod 229) V] [FiniteDimensional (ZMod 229) V]

/-- **The chain `(Gaussian elimination; TL_6)` over `F_229` is a `{0}`-node at modulus
`6`** (Corollary `cor:plus-chain`, instantiated). -/
theorem tl6_chain_229 :
    IsNode C229 6 {0} (chainIdx (finrank (ZMod 229) V) (Fin (finrank (ZMod 229) V + 1)) [σ229])
      (chainRun C229 (finrank (ZMod 229) V) (gauss (K := ZMod 229) (V := V)) [σ229]) :=
  chain_spec C229 (gauss_spec C229 (V := V) 1 (by simp)) [σ229] chainOK_229

omit [FiniteDimensional (ZMod 229) V] in
/-- Its arity is `(a + 1)(5a + 1)`, `a = finrank V`. -/
theorem tl6_arity_229 :
    Fintype.card (chainIdx (finrank (ZMod 229) V) (Fin (finrank (ZMod 229) V + 1)) [σ229]) =
      (finrank (ZMod 229) V + 1) * (5 * finrank (ZMod 229) V + 1) := by
  rw [card_chainIdx]
  simp [σ229]

/-- **With sixth roots it is a `6`-solver** (degree 2) over `F_229`. -/
theorem tl6_solver_229
    (col : chainIdx (finrank (ZMod 229) V) (Fin (finrank (ZMod 229) V + 1)) [σ229] → V) :
    IsRootSol 6 col (rootsOf (rootOf 6)
      (chainRun C229 (finrank (ZMod 229) V) (gauss (K := ZMod 229) (V := V)) [σ229] col)) :=
  rootSol_of_rel C229 dvd6_229 (rootOf 6) (fun _ hx => rootOf_pow hx.2) (tl6_chain_229 col)

end P229

section P7

instance fact7 : Fact (Nat.Prime 7) := ⟨by norm_num⟩

/-- `3` as a unit of `F_7`. -/
def g7 : (ZMod 7)ˣ := ZMod.unitOfCoprime 3 (by norm_num)

theorem g7_val : (g7 : ZMod 7) = 3 := by simp [g7]

theorem orderOf_g7 : orderOf g7 = Fintype.card (ZMod 7) - 1 := by
  rw [ZMod.card]
  refine orderOf_eq_of_pow_and_pow_div_prime (by norm_num) ?_ ?_
  · rw [Units.ext_iff, Units.val_pow_eq_pow_val, g7_val, Units.val_one]; decide
  · intro q hq hdvd
    have h6 : q ∣ 2 * 3 := hdvd
    rw [Ne, Units.ext_iff, Units.val_pow_eq_pow_val, g7_val, Units.val_one]
    rcases (Nat.Prime.dvd_mul hq).mp h6 with h | h
    · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_two).mp h; decide
    · obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_three).mp h; decide

/-- The class map of `ξ = g = 3` over `F_7`. -/
noncomputable def C7 : ClassMap (ZMod 7) (Fintype.card (ZMod 7) - 1) :=
  ClassMap.ofGen g7 (ClassMap.gen_of_orderOf orderOf_g7) (by rw [ZMod.card]; norm_num)

/-- **`TL_3` is available at `p = 7`** (entry `"7"` of `certs_stage1.json`:
`α = (6, 2, 0)`, `β = (0, 1, 5)`). -/
theorem tl3_7 : IsRC C7 3 ↑(Finset.univ : Finset (ZMod 3)) {0}
    (fun i => ([6, 2, 0] : List (ZMod 7)).getD i.val 0)
    (fun i => ([0, 1, 5] : List (ZMod 7)).getD i.val 0) := by
  rw [isRC_zero_iff_check C7 (by rw [ZMod.card]; norm_num) (h := 2) (by rw [ZMod.card])
    (by norm_num), show C7.xi = 3 from g7_val]
  decide

end P7

end QSearch.Schedule1HPlus

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset

section EllOne

variable {K : Type*} [Field K] [DecidableEq K] {N : ℕ} (C : ClassMap K N)

/-- **Non-vacuity of Definition `def:plus-ell`**: at level `ℓ = 1`, `C_m = z_m` is an
`ℓ`-level `ℤ_κ`-contraction (it gives back Gaussian elimination, a `ℤ_κ`-node). There is
no level-`1` `{0}`-contraction for `κ ≥ 2`. The paper's five level-`3`/`4` tables are
checked against `IsEllContraction` by `decide +kernel` in the review modules
`Formal.Schedule1HPlusReview.EllCheck*` (not imported by `Formal.lean`). -/
theorem ell1_contraction {κ : ℕ} [NeZero κ] :
    IsEllContraction C 1 (Set.univ : Set (ZMod κ)) (fun y => C.xiPow (y 0)) := by
  refine ⟨fun _ _ => Set.mem_univ _, ?_, fun X hX => ?_⟩
  · show C.xiPow ((0 : Fin 1 → ZMod κ) 0) ∈ Pow κ
    rw [Pi.zero_apply, ClassMap.xiPow_zero]
    exact ⟨one_ne_zero, 1, one_pow _⟩
  · have h := hX 0 0
    have hupd : ∀ m : ZMod κ, Function.update (0 : Fin 1 → ZMod κ) 0 m =
        (Equiv.funUnique (Fin 1) (ZMod κ)).symm m := by
      intro m; funext r; fin_cases r; simp
    simp_rw [hupd, smul_eq_mul] at h
    rw [← h]
    exact (Fintype.sum_equiv (Equiv.funUnique (Fin 1) (ZMod κ)) _ _ (fun y => by
      congr 2 <;> (funext r; fin_cases r; rfl))).trans rfl

end EllOne

end QSearch.Schedule1HPlus
