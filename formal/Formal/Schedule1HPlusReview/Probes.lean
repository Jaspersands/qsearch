import Formal.Schedule1HPlus.Guards
import Formal.Schedule1HPlus.SecondMoment

/-!
# Hostile review probes for `Formal/Schedule1HPlus` (2026-11-14)

Not imported by `Formal.lean`. Build with `lake build Formal.Schedule1HPlusReview.Probes`.

* `ClassMap` is neither weaker nor more permissive than the paper's `cl_D`:
  `cl_eq_of_xi_eq` (two class maps with the same `ξ` agree on `Kˣ`), `xi_not_mem_pow`
  (`ξ ∉ P_D` for every `1 < D ∣ N`), `xi_of_classMap7` (over `F_7` with `N = 6`, `ξ` must be a
  primitive root, `3` or `5`), `no_classMap_7_4` (no class map over `F_7` with `4 ∣ N`: the
  structure encodes that `ξ` generates `Kˣ/P_D` with `D` classes).
* `IsRel` rejects what it should: `not_isRel_no_one` (no coefficient equal to `1`),
  `not_isRel_class` (a coefficient of class `1` for `Ω = {0}` at modulus `2`), while the same
  vector is a `ℤ_2`-relation (`isRel_univ`).
* A **two-step chain** with nontrivial `Ω_1 = {0}` and `Δ_2 = lift_4{0} = {0,2} ≠ ℤ_4`:
  `(Gaussian elimination; (2, ℤ_2, {0}), (4, {0,2}, {0}))` over `F_17`, `ξ = g = 3`. Both
  contractions were found by exhaustive search
  (`research/audits/reviews/2026-11-14-rees-lean-schedule1hplus-review/search_two_step.py`)
  and are checked here by `decide`. `chainOK17` discharges every hypothesis of `chain_spec`
  at `L = 2`; `chain17_solver` is the resulting `4`-solver of degree 3; `chain17_arity`
  is `(a+1)^3`; `chainOK17_bad` shows `ChainOK` rejects `Δ_2 = {0}` (lift not contained).
-/

namespace QSearch.Schedule1HPlus.Review

open QSearch.Schedule1H QSearch.Schedule1HPlus Finset Module

section General

variable {K : Type*} [Field K] {N : ℕ}

/-- A class map is determined on `Kˣ` by `ξ`. -/
theorem cl_eq_of_xi_eq (C C' : ClassMap K N) (h : C.xi = C'.xi) {D : ℕ} (hD : D ∣ N) {x : K}
    (hx : x ≠ 0) : C.cl D x = C'.cl D x := by
  obtain ⟨y, hy, hxy⟩ := C.mem_coset hD hx
  have : C.xiPow (C.cl D x) = C'.xiPow (C.cl D x) := by simp [ClassMap.xiPow, h]
  rw [hxy, this, C'.cl_unique hD _ hy, ← this, C.cl_unique hD _ hy]

/-- `ξ` is not in `P_D` for `1 < D ∣ N` (so it is a coset generator). -/
theorem xi_not_mem_pow (C : ClassMap K N) {D : ℕ} (hD : D ∣ N) (h1 : 1 < D) :
    C.xi ∉ Pow D := by
  intro hP
  have h0 := C.cl_of_mem_pow hD hP
  rw [C.cl_xi hD] at h0
  have : Fact (1 < D) := ⟨h1⟩
  exact one_ne_zero h0

/-- Nodes can be reindexed along an equivalence (needed to feed a chain node, indexed by
`chainIdx`, or an `ℓ`-level node, indexed by `tIdx`, to the plan theorems, which take
`Fin A`). Not in `Schedule1HPlus`. -/
theorem isNode_reindex [DecidableEq K] (C : ClassMap K N) {V : Type*} [AddCommGroup V]
    [Module K V] {D : ℕ} {Ω : Set (ZMod D)} {ι ι' : Type*} [Fintype ι] [Fintype ι']
    (e : ι' ≃ ι) {nd : (ι → V) → ι → K} (h : IsNode C D Ω ι nd) :
    IsNode C D Ω ι' (fun col => nd (col ∘ e.symm) ∘ e) := by
  intro col
  obtain ⟨⟨b, hb⟩, hcl, hsum⟩ := h (col ∘ e.symm)
  refine ⟨⟨e.symm b, by simpa using hb⟩, fun b' hb' => hcl _ hb', ?_⟩
  rw [← hsum]
  exact Fintype.sum_equiv e _ _ (fun b' => by simp)

/-- `Ω`-relations are monotone in `Ω` (a `{0}`-node is a `{0,m}`-node). -/
theorem isRel_mono [DecidableEq K] (C : ClassMap K N) {V : Type*} [AddCommGroup V]
    [Module K V] {D : ℕ} {Ω Ω' : Set (ZMod D)} (hΩ : Ω ⊆ Ω') {ι : Type*} [Fintype ι]
    {col : ι → V} {w : ι → K} (h : IsRel C D Ω col w) : IsRel C D Ω' col w :=
  ⟨h.1, fun b hb => hΩ (h.2.1 b hb), h.2.2⟩

/-- The pair-count hypothesis `hN` of `plus_sm_i` is never vacuous: it always holds with the
trivial `γ_{ij} = |A_{ij}|` (with a useless bound). The paper's
`γ_{ij} = γ|A_{ij}|²/p` is the Weil input, not formalized. -/
theorem hN_trivial {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G] (A : Finset G)
    (x x' : G) :
    ((Finset.univ.filter fun c => x + c ∈ A ∧ x' + c ∈ A).card : ℝ) ≤ (A.card : ℝ) := by
  have h := card_translate x A
  have hsub : (Finset.univ.filter fun c => x + c ∈ A ∧ x' + c ∈ A) ⊆
      Finset.univ.filter fun c => x + c ∈ A := by
    intro c hc
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hc ⊢
    exact hc.1
  exact_mod_cast (Finset.card_le_card hsub).trans h.le

end General

section F7

theorem xi_of_classMap7 (C : ClassMap (ZMod 7) 6) : C.xi = 3 ∨ C.xi = 5 := by
  have h2 := xi_not_mem_pow C (D := 2) (by norm_num) (by norm_num)
  have h3 := xi_not_mem_pow C (D := 3) (by norm_num) (by norm_num)
  have hne := C.xi_ne
  revert h2 h3 hne
  generalize C.xi = x
  revert x
  unfold QSearch.Schedule1H.Pow
  decide

/-- No class map over `F_7` admits the modulus `4` (`4 ∤ 6`). -/
theorem no_classMap_7_4 (C : ClassMap (ZMod 7) 4) : False := by
  have hsq : ∀ x : ZMod 7, x ≠ 0 → ∃ r : ZMod 7, r ^ 4 = x ^ 2 := by decide
  obtain ⟨r, hr⟩ := hsq C.xi C.xi_ne
  have hP : C.xi ^ 2 ∈ Pow 4 := ⟨pow_ne_zero _ C.xi_ne, r, hr⟩
  have h0 := C.cl_of_mem_pow (dvd_refl 4) hP
  rw [C.cl_xi_pow (dvd_refl 4)] at h0
  exact absurd h0 (by decide)

/-- `C7` from the author's guards: `ξ = 3`. -/
theorem C7_xi : C7.xi = 3 := g7_val

/-- `cl_2(6) = 1` for `ξ = 3` (`6 = 3 · 2`, `2 = 3^2 ∈ P_2`). -/
theorem cl2_six : C7.cl 2 6 = 1 := by
  have hP : (2 : ZMod 7) ∈ Pow 2 := ⟨by decide, 3, by decide⟩
  have := C7.cl_unique (D := 2) (by rw [ZMod.card]; norm_num) 1 hP
  rw [show C7.xiPow (1 : ZMod 2) = 3 by rw [ClassMap.xiPow, C7_xi]; rfl] at this
  rw [show (6 : ZMod 7) = 3 * 2 by decide]
  exact this

/-- `w = (1, -1)` on columns `(1, 1)` of `F_7`. -/
def col7 : Fin 2 → ZMod 7 := ![1, 1]

theorem isRel_univ : IsRel C7 2 Set.univ col7 ![1, 6] :=
  ⟨⟨0, rfl⟩, fun _ _ => Set.mem_univ _, by decide⟩

/-- Rejected for `Ω = {0}` at modulus `2`: the weight `6` has class `1`. -/
theorem not_isRel_class : ¬ IsRel C7 2 {0} col7 ![1, 6] := by
  rintro ⟨_, hcl, _⟩
  have := hcl 1 (by decide)
  change C7.cl 2 6 ∈ ({0} : Set (ZMod 2)) at this
  rw [cl2_six, Set.mem_singleton_iff] at this
  exact absurd this (by decide)

/-- Rejected: no coefficient equal to `1` (the designated index is required). -/
theorem not_isRel_no_one : ¬ IsRel C7 2 Set.univ col7 ![2, 5] := by
  rintro ⟨⟨b, hb⟩, _, _⟩
  fin_cases b <;> exact absurd hb (by decide)

end F7

section F17

instance fact17 : Fact (Nat.Prime 17) := ⟨by norm_num⟩

def g17 : (ZMod 17)ˣ := ZMod.unitOfCoprime 3 (by norm_num)

theorem g17_val : (g17 : ZMod 17) = 3 := by simp [g17]

/-- `3` is a primitive root mod `17` (`16 = 2^4`). -/
theorem orderOf_g17 : orderOf g17 = Fintype.card (ZMod 17) - 1 := by
  rw [ZMod.card]
  refine orderOf_eq_of_pow_and_pow_div_prime (by norm_num) ?_ ?_
  · rw [Units.ext_iff, Units.val_pow_eq_pow_val, g17_val, Units.val_one]; decide
  · intro q hq hdvd
    have h16 : q ∣ 2 ^ 4 := by norm_num; exact hdvd
    rw [Ne, Units.ext_iff, Units.val_pow_eq_pow_val, g17_val, Units.val_one]
    obtain rfl := (Nat.prime_dvd_prime_iff_eq hq Nat.prime_two).mp (hq.dvd_of_dvd_pow h16)
    decide

noncomputable def C17 : ClassMap (ZMod 17) (Fintype.card (ZMod 17) - 1) :=
  ClassMap.ofGen g17 (ClassMap.gen_of_orderOf orderOf_g17) (by rw [ZMod.card]; norm_num)

theorem C17_xi : C17.xi = 3 := g17_val

/-- Step 1: `(2, ℤ_2, {0})`, `α = (2, 0)`, `β = (0, 1)`. (A first transcription with
`α = (1, 0)`, the `p = 5` certificate, was rejected by `decide`.) -/
abbrev σ1 : Step (ZMod 17) :=
  ⟨2, Finset.univ, {0}, fun i => ([2, 0] : List (ZMod 17)).getD i.val 0,
    fun i => ([0, 1] : List (ZMod 17)).getD i.val 0⟩

/-- Step 2: `(4, {0,2}, {0})`, `α = (1, 11, 0, 5)`, `β_0 = 0`, `β_2 = 1`. -/
abbrev σ2 : Step (ZMod 17) :=
  ⟨4, {0, 2}, {0}, fun i => ([1, 11, 0, 5] : List (ZMod 17)).getD i.val 0,
    fun i => ([0, 0, 1, 0] : List (ZMod 17)).getD i.val 0⟩

theorem rc1_17 : IsRC C17 2 ↑(Finset.univ : Finset (ZMod 2)) {0} σ1.α σ1.β := by
  rw [isRC_zero_iff_check C17 (by rw [ZMod.card]; norm_num) (h := 8) (by rw [ZMod.card])
    (by norm_num), C17_xi]
  decide

theorem rc2_17 : IsRC C17 4 ↑({0, 2} : Finset (ZMod 4)) {0} σ2.α σ2.β := by
  rw [isRC_zero_iff_check C17 (by rw [ZMod.card]; norm_num) (h := 4) (by rw [ZMod.card])
    (by norm_num), C17_xi]
  decide

/-- `lift_4 {0} ⊆ {0, 2}` (indeed equal). -/
theorem lift17 : ClassMap.lift 4 ({0} : Set (ZMod 2)) ⊆ (↑({0, 2} : Finset (ZMod 4)) : Set (ZMod 4)) := by
  intro i hi
  simp only [ClassMap.lift, Set.mem_setOf_eq, Set.mem_singleton_iff] at hi
  simp only [Finset.coe_insert, Finset.coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff]
  revert i
  decide

/-- **Every hypothesis of `chain_spec` holds for a real two-step chain.** -/
theorem chainOK17 : ChainOK C17 1 Set.univ [σ2, σ1] := by
  refine ⟨⟨one_dvd _, one_dvd _, by rw [ZMod.card]; norm_num, fun i _ => ?_, rc1_17⟩,
    by show 2 ∣ 4; norm_num, by rw [ZMod.card]; norm_num, lift17, rc2_17⟩
  exact Finset.mem_coe.mpr (Finset.mem_univ _)

/-- `ChainOK` rejects `Δ_2 = {0}`: `2 ∈ lift_4{0}` but `2 ∉ {0}`. -/
theorem chainOK17_bad :
    ¬ ChainOK C17 1 Set.univ [⟨4, {0}, {0}, σ2.α, σ2.β⟩, σ1] := by
  rintro ⟨_, _, _, hl, _⟩
  have h2 : (2 : ZMod 4) ∈ ClassMap.lift 4 ({0} : Set (ZMod 2)) := by
    simp only [ClassMap.lift, Set.mem_setOf_eq, Set.mem_singleton_iff]; decide
  have := hl h2
  simp at this
  exact absurd this (by decide)

variable {V : Type} [AddCommGroup V] [Module (ZMod 17) V] [FiniteDimensional (ZMod 17) V]

theorem chain17_node :
    IsNode C17 4 {0} (chainIdx (finrank (ZMod 17) V) (Fin (finrank (ZMod 17) V + 1)) [σ2, σ1])
      (chainRun C17 (finrank (ZMod 17) V) (gauss (K := ZMod 17) (V := V)) [σ2, σ1]) :=
  chain_spec C17 (gauss_spec C17 (V := V) 1 (by simp)) [σ2, σ1] chainOK17

omit [FiniteDimensional (ZMod 17) V] in
theorem chain17_arity :
    Fintype.card (chainIdx (finrank (ZMod 17) V) (Fin (finrank (ZMod 17) V + 1)) [σ2, σ1]) =
      (finrank (ZMod 17) V + 1) ^ 3 := by
  have h2 : ({0, 2} : Finset (ZMod 4)).card = 2 := by decide
  rw [card_chainIdx]
  simp [σ1, σ2, h2]
  ring

/-- **The two-step chain is a `4`-solver of degree 3 over `F_17`.** -/
theorem chain17_solver
    (col : chainIdx (finrank (ZMod 17) V) (Fin (finrank (ZMod 17) V + 1)) [σ2, σ1] → V) :
    IsRootSol 4 col (rootsOf (rootOf 4)
      (chainRun C17 (finrank (ZMod 17) V) (gauss (K := ZMod 17) (V := V)) [σ2, σ1] col)) :=
  rootSol_of_rel C17 (by rw [ZMod.card]; norm_num) (rootOf 4) (fun _ hx => rootOf_pow hx.2)
    (chain17_node col)

end F17

#print axioms cl_eq_of_xi_eq
#print axioms xi_of_classMap7
#print axioms no_classMap_7_4
#print axioms not_isRel_class
#print axioms not_isRel_no_one
#print axioms chainOK17
#print axioms chainOK17_bad
#print axioms chain17_solver
#print axioms chain17_arity

end QSearch.Schedule1HPlus.Review
