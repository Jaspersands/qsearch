import Formal.Schedule1H.Objects
import Formal.ReesSdeSolver
import Mathlib.Data.Nat.Log
import Mathlib.Logic.Equiv.Fin.Basic

/-!
# Schedule 1H, part 2: the level recursion, Lemma `lem:rounds`, the plans `(s, F)`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Lemma `lem:rounds` (Section
`sec:schedule1`) and Definition `def:schedule1h` / Theorem `thm:halving`(ii) (Section
`sec:halving`).

Both Lemma `lem:rounds` and a halving plan `(s, F)` have the same shape: columns are split
into blocks; at each level, groups of `A` objects of type `c^{(j)}` are fed to one call of
a *step oracle*; the call either closes a `κ`-solution or returns an object of type
`c^{(j+1)} = (c^{(j)}, e c^{(j)})`; after the last level a finish (F0 or F1) closes.

* `Lev A j` is the column index type of one block of `A^j` columns (nested pairs; block
  `b` of level `j + 1` is `{b} × Lev A j`, so supports of distinct objects are disjoint by
  construction); `levEquiv : Lev A j ≃ Fin (A ^ j)`.
* `Typ j` indexes the `2^j` entries of the type `c^{(j)}`; `cTyp e j` is `c^{(j)}` with
  `c^{(0)} = (1)`, `c^{(j+1)} = (c^{(j)}, e c^{(j)})`.
* `runLevel κ orc j col` is the level recursion with step oracle `orc`;
  `runLevel_spec`: if every oracle answer satisfies `StepSpec κ e`, the result is a
  `κ`-solution on the block or an object of type `c^{(j)}`.
* `rounds` / `rounds_spec` is **Lemma `lem:rounds`**: step oracle = the imported
  Ivanyos–Santha collision call (`ISOut`, converted by `ISOut.stepSpec`), `e = 1`,
  `L = ⌈log₂ t⌉ = Nat.clog 2 t` levels, finish F0 with the zero sum `z`.
* `planF0` / `planF1` with their `_spec` are the plans `(s, F0)` and `(s, F1)` of
  Definition `def:schedule1h` for an arbitrary step oracle; F1 uses Gaussian elimination
  (`QSearch.ReesSdeSolver.kernelVec`) on the `a + 1` final objects.

The imported Theorem `thm:is-import` is *not* proved: its algorithm is an input
(`isRun`) together with its specification (`ISOut`), exactly as in the paper.
-/

namespace QSearch.Schedule1H

open Finset

/-- Column index type of one block of level `j` (`A ^ j` columns). -/
def Lev (A : ℕ) : ℕ → Type
  | 0 => Unit
  | j + 1 => Fin A × Lev A j

instance instFintypeLev (A : ℕ) : (j : ℕ) → Fintype (Lev A j)
  | 0 => inferInstanceAs (Fintype Unit)
  | j + 1 => letI := instFintypeLev A j; inferInstanceAs (Fintype (Fin A × Lev A j))

instance instDecEqLev (A : ℕ) : (j : ℕ) → DecidableEq (Lev A j)
  | 0 => inferInstanceAs (DecidableEq Unit)
  | j + 1 => letI := instDecEqLev A j; inferInstanceAs (DecidableEq (Fin A × Lev A j))

/-- `Lev A j` has `A ^ j` elements. -/
def levEquiv (A : ℕ) : (j : ℕ) → Lev A j ≃ Fin (A ^ j)
  | 0 => (Equiv.ofUnique Unit (Fin 1)).trans (finCongr (pow_zero A).symm)
  | j + 1 => ((Equiv.refl (Fin A)).prodCongr (levEquiv A j)).trans
      (finProdFinEquiv.trans (finCongr (pow_succ' A j).symm))

/-- Index type of the `2 ^ j` entries of the type `c^{(j)}`. -/
def Typ : ℕ → Type
  | 0 => Unit
  | j + 1 => Typ j ⊕ Typ j

instance instFintypeTyp : (j : ℕ) → Fintype (Typ j)
  | 0 => inferInstanceAs (Fintype Unit)
  | j + 1 => letI := instFintypeTyp j; inferInstanceAs (Fintype (Typ j ⊕ Typ j))

instance instDecEqTyp : (j : ℕ) → DecidableEq (Typ j)
  | 0 => inferInstanceAs (DecidableEq Unit)
  | j + 1 => letI := instDecEqTyp j; inferInstanceAs (DecidableEq (Typ j ⊕ Typ j))

/-- `Typ j` has `2 ^ j` elements. -/
def typEquiv : (j : ℕ) → Typ j ≃ Fin (2 ^ j)
  | 0 => (Equiv.ofUnique Unit (Fin 1)).trans (finCongr (pow_zero 2).symm)
  | j + 1 => (Equiv.sumCongr (typEquiv j) (typEquiv j)).trans
      (finSumFinEquiv.trans (finCongr (by rw [pow_succ]; ring)))

/-- The first representation index (the paper's `R_1`). -/
def k0 : (j : ℕ) → Typ j
  | 0 => ()
  | j + 1 => Sum.inl (k0 j)

variable {K : Type*} [Field K]

/-- The type `c^{(j)}`: `c^{(0)} = (1)`, `c^{(j+1)} = (c^{(j)}, e c^{(j)})`. -/
def cTyp (e : K) : (j : ℕ) → Typ j → K
  | 0 => fun _ => 1
  | j + 1 => extType (cTyp e j) e

/-- With `e = 1` (Lemma `lem:rounds`, and Corollary `cor:hcd`(i)) every entry is `1`. -/
theorem cTyp_one : ∀ (j : ℕ) (k : Typ j), cTyp (1 : K) j k = 1
  | 0, _ => rfl
  | j + 1, Sum.inl k => cTyp_one j k
  | j + 1, Sum.inr k => by
    show 1 * cTyp (1 : K) j k = 1
    rw [cTyp_one j k, one_mul]

section Run

variable [DecidableEq K] {V : Type*} [AddCommGroup V] [Module K V]

/-- The first block whose sub-run returned a solution. -/
def firstSol {A : ℕ} {X Y : Type*} (f : Fin A → X ⊕ Y) : Option (Fin A × X) :=
  (List.finRange A).findSome? fun b => match f b with
    | Sum.inl x => some (b, x)
    | Sum.inr _ => none

theorem firstSol_some {A : ℕ} {X Y : Type*} {f : Fin A → X ⊕ Y} {b : Fin A} {x : X}
    (h : firstSol f = some (b, x)) : f b = Sum.inl x := by
  obtain ⟨b', _, hb'⟩ := List.exists_of_findSome?_eq_some h
  revert hb'
  cases hf : f b' with
  | inl x' => intro hx; simp only [Option.some.injEq, Prod.mk.injEq] at hx; obtain ⟨rfl, rfl⟩ := hx; exact hf
  | inr _ => intro hx; cases hx

theorem firstSol_none {A : ℕ} {X Y : Type*} {f : Fin A → X ⊕ Y} (h : firstSol f = none)
    (b : Fin A) : ∃ y, f b = Sum.inr y := by
  have := List.findSome?_eq_none_iff.mp h b (List.mem_finRange b)
  revert this
  cases f b with
  | inl x => intro hx; cases hx
  | inr y => intro _; exact ⟨y, rfl⟩

/-- Extend a solution on block `b` by zeros. -/
def extendSol {A : ℕ} {ι : Type*} (b : Fin A) (r : ι → K) : Fin A × ι → K :=
  fun p => if p.1 = b then r p.2 else 0

omit [DecidableEq K] in
theorem extendSol_spec {κ A : ℕ} (hκ : 0 < κ) {ι : Type*} [Fintype ι] (b : Fin A)
    (col : Fin A × ι → V) (r : ι → K) (h : IsRootSol κ (fun i => col (b, i)) r) :
    IsRootSol κ col (extendSol b r) := by
  refine ⟨fun h0 => h.1 (funext fun i => by simpa [extendSol] using congrFun h0 (b, i)), ?_⟩
  rw [Fintype.sum_prod_type, Finset.sum_eq_single b]
  · simpa [extendSol] using h.2
  · intro b' _ hb'
    exact Finset.sum_eq_zero fun i _ => by simp [extendSol, hb', zero_pow hκ.ne']
  · simp

/-- The object carried by a sub-run that did not return a solution. -/
def objOf {X ι τ : Type*} : X ⊕ Obj ι τ V K → Obj ι τ V K := Sum.elim (fun _ => default) id

/-- **The level recursion.** Level `0`: each column is an object of type `(1)`.
Level `j + 1`: run level `j` on each of the `A` blocks; if a block returns a solution,
output it (zeros elsewhere); otherwise call the step oracle on the `A` vectors and
apply `step`. -/
def runLevel (κ : ℕ) {A : ℕ} (orc : (Fin A → V) → (Fin A → K) × (Fin A → K)) :
    (j : ℕ) → (Lev A j → V) → (Lev A j → K) ⊕ Obj (Lev A j) (Typ j) V K
  | 0, col => Sum.inr (colObj (col ()))
  | j + 1, col =>
    match firstSol (fun b : Fin A => runLevel κ orc j (fun i => col (b, i))) with
    | some (b, r) => Sum.inl (extendSol b r)
    | none =>
      let objs := fun b : Fin A => objOf (runLevel κ orc j (fun i => col (b, i)))
      let w := orc (fun b => (objs b).v)
      step κ (k0 j) objs w.1 w.2

/-- **Correctness of the level recursion** (the induction on `j` in the proofs of
Lemma `lem:rounds` and Theorem `thm:halving`(ii)). -/
theorem runLevel_spec {κ A : ℕ} (hκ : 0 < κ) {e : K} (he : e ≠ 0)
    (orc : (Fin A → V) → (Fin A → K) × (Fin A → K))
    (horc : ∀ v, StepSpec κ e v (orc v).1 (orc v).2) :
    ∀ (j : ℕ) (col : Lev A j → V), ResOK κ col (cTyp e j) (runLevel κ orc j col)
  | 0, col => colObj_spec κ col
  | j + 1, col => by
    have ih := fun b : Fin A => runLevel_spec hκ he orc horc j (fun i => col (b, i))
    simp only [runLevel]
    cases hf : firstSol (fun b : Fin A => runLevel κ orc j (fun i => col (b, i))) with
    | some br =>
      obtain ⟨b, r⟩ := br
      have hb := firstSol_some hf
      have := ih b
      rw [hb] at this
      exact extendSol_spec hκ b col r this
    | none =>
      have ho : ∀ b, IsObj κ (fun i => col (b, i)) (cTyp e j)
          (objOf (runLevel κ orc j (fun i => col (b, i)))) := by
        intro b
        obtain ⟨y, hy⟩ := firstSol_none hf b
        have := ih b
        rw [hy] at this ⊢
        exact this
      exact step_spec hκ (k0 j) col (cTyp e j) he _ ho _ _ (horc _)

/-- Plan with finish F0 on one block of level `s`: `ρ0` is a root vector with
`∑ ρ0_k^κ c^{(s)}_k = 0` (it witnesses `0 ∈ T_s`). -/
def planF0 (κ : ℕ) {A : ℕ} (orc : (Fin A → V) → (Fin A → K) × (Fin A → K)) (s : ℕ)
    (ρ0 : Typ s → K) (col : Lev A s → V) : Lev A s → K :=
  match runLevel κ orc s col with
  | Sum.inl r => r
  | Sum.inr o => finishF0 o ρ0

theorem planF0_spec {κ A : ℕ} (hκ : 0 < κ) {e : K} (he : e ≠ 0)
    (orc : (Fin A → V) → (Fin A → K) × (Fin A → K))
    (horc : ∀ v, StepSpec κ e v (orc v).1 (orc v).2) (s : ℕ) (ρ0 : Typ s → K) (hρ0 : ρ0 ≠ 0)
    (hz : ∑ k, ρ0 k ^ κ * cTyp e s k = 0) (col : Lev A s → V) :
    IsRootSol κ col (planF0 κ orc s ρ0 col) := by
  have h := runLevel_spec hκ he orc horc s col
  unfold planF0
  revert h
  cases runLevel κ orc s col with
  | inl r => intro h; exact h
  | inr o => intro h; exact finishF0_spec hκ col (cTyp e s) o h ρ0 hρ0 hz

/-- Plan with finish F1: `a + 1` blocks of level `s`, Gaussian elimination on the final
vectors, and a finisher `fin` writing each nonzero `η` as `∑ y_k^κ c^{(s)}_k`. -/
def planF1 (κ : ℕ) {A a : ℕ} (orc : (Fin A → Fin a → K) → (Fin A → K) × (Fin A → K))
    (s : ℕ) (fin : K → Typ s → K) (col : Fin (a + 1) × Lev A s → Fin a → K) :
    Fin (a + 1) × Lev A s → K :=
  match firstSol (fun b : Fin (a + 1) => runLevel κ orc s (fun i => col (b, i))) with
  | some (b, r) => extendSol b r
  | none =>
    let objs := fun b : Fin (a + 1) => objOf (runLevel κ orc s (fun i => col (b, i)))
    finishF1 objs fin (QSearch.ReesSdeSolver.kernelVec a (a + 1) (fun b => (objs b).v)).get

theorem planF1_spec {κ A a : ℕ} (hκ : 0 < κ) {e : K} (he : e ≠ 0)
    (orc : (Fin A → Fin a → K) → (Fin A → K) × (Fin A → K))
    (horc : ∀ v, StepSpec κ e v (orc v).1 (orc v).2) (s : ℕ) (fin : K → Typ s → K)
    (hfin : ∀ x : K, x ≠ 0 → fin x ≠ 0 ∧ ∑ k, fin x k ^ κ * cTyp e s k = x)
    (col : Fin (a + 1) × Lev A s → Fin a → K) :
    IsRootSol κ col (planF1 κ orc s fin col) := by
  have ih := fun b : Fin (a + 1) => runLevel_spec hκ he orc horc s (fun i => col (b, i))
  unfold planF1
  cases hf : firstSol (fun b : Fin (a + 1) => runLevel κ orc s (fun i => col (b, i))) with
  | some br =>
    obtain ⟨b, r⟩ := br
    have := ih b
    rw [firstSol_some hf] at this
    exact extendSol_spec hκ b col r this
  | none =>
    have ho : ∀ b, IsObj κ (fun i => col (b, i)) (cTyp e s)
        (objOf (runLevel κ orc s (fun i => col (b, i)))) := by
      intro b
      obtain ⟨y, hy⟩ := firstSol_none hf b
      have := ih b
      rw [hy] at this ⊢
      exact this
    obtain ⟨hη0, hη⟩ := QSearch.ReesSdeSolver.kernelVec_spec a (a + 1)
      (fun b => (objOf (runLevel κ orc s (fun i => col (b, i)))).v) (Nat.lt_succ_self a)
    exact finishF1_spec hκ col (cTyp e s) _ ho fin hfin _ hη0 hη

end Run

section FinSolvers

variable [DecidableEq K]

/-- An algorithm on columns indexed by `ι`, moved to `Fin N` along `ι ≃ Fin N`. -/
def onFin {ι : Type*} {N a : ℕ} (eq : ι ≃ Fin N) (alg : (ι → Fin a → K) → ι → K)
    (col : Fin N → Fin a → K) : Fin N → K :=
  alg (col ∘ eq) ∘ eq.symm

omit [DecidableEq K] in
theorem onFin_spec {ι : Type*} [Fintype ι] {κ N a : ℕ} (eq : ι ≃ Fin N)
    (alg : (ι → Fin a → K) → ι → K) (halg : ∀ col, IsRootSol κ col (alg col))
    (col : Fin N → Fin a → K) : IsRootSol κ col (onFin eq alg col) :=
  IsRootSol.comp_equiv eq (halg (col ∘ eq))

/-- Column index of the plan `(s, F1)`: `n_F1 = a + 1` blocks of `A ^ s` columns. -/
def planF1Equiv (A a s : ℕ) : Fin (a + 1) × Lev A s ≃ Fin (A ^ s * (a + 1)) :=
  ((Equiv.refl _).prodCongr (levEquiv A s)).trans
    (finProdFinEquiv.trans (finCongr (Nat.mul_comm _ _)))

end FinSolvers

section Rounds

variable [DecidableEq K]

/-- The arity `G(κ, a) = κ^{κ(κ-1)/2} (a+1)^κ` of the imported collision step
(`eq:Bd`). -/
def Garity (κ a : ℕ) : ℕ := κ ^ (κ * (κ - 1) / 2) * (a + 1) ^ κ

/-- **The output of the imported Theorem `thm:is-import`** on vectors `v_1, …, v_G`:
disjoint `I ≠ ∅` and `J`, and nonzero `γ_j` on `I ∪ J`, with
`∑_{i ∈ I} γ_i^κ v_i = ∑_{j ∈ J} γ_j^κ v_j`. -/
structure ISOut {G a : ℕ} (κ : ℕ) (v : Fin G → Fin a → K) where
  I : Finset (Fin G)
  J : Finset (Fin G)
  γ : Fin G → K
  hI : I.Nonempty
  hdisj : Disjoint I J
  hγ : ∀ j ∈ I ∪ J, γ j ≠ 0
  hrel : ∑ i ∈ I, γ i ^ κ • v i = ∑ j ∈ J, γ j ^ κ • v j

/-- The roots `ρ = γ` on `I`, `σ = γ` on `J` (zero elsewhere). -/
def ISOut.rs {G a κ : ℕ} {v : Fin G → Fin a → K} (o : ISOut κ v) : (Fin G → K) × (Fin G → K) :=
  (fun b => if b ∈ o.I then o.γ b else 0, fun b => if b ∈ o.J then o.γ b else 0)

omit [DecidableEq K] in
/-- An Ivanyos–Santha output is a step answer with `e = 1`. -/
theorem ISOut.stepSpec {G a κ : ℕ} (hκ : 0 < κ) {v : Fin G → Fin a → K} (o : ISOut κ v) :
    StepSpec κ 1 v o.rs.1 o.rs.2 := by
  refine ⟨fun h => ?_, fun b => ?_, ?_⟩
  · obtain ⟨i, hi⟩ := o.hI
    have := congrFun h i
    simp only [ISOut.rs, hi, ite_true, Pi.zero_apply] at this
    exact o.hγ i (Finset.mem_union_left _ hi) this
  · by_cases hb : b ∈ o.I
    · right; simp [ISOut.rs, Finset.disjoint_left.mp o.hdisj hb]
    · left; simp [ISOut.rs, hb]
  · simp only [ISOut.rs, one_smul]
    simp_rw [ite_pow, zero_pow hκ.ne', ite_smul, zero_smul]
    rw [← Finset.sum_filter, ← Finset.sum_filter]
    simp only [Finset.filter_mem_eq_inter, Finset.univ_inter]
    exact o.hrel.symm

/-- **Lemma `lem:rounds`, the algorithm.** `isRun` is the imported collision algorithm of
arity `G(κ, a)`; `z` is a zero sum of `κ`-th powers of length `t`; `L = ⌈log₂ t⌉`. On
the first `G^L` columns run `L` levels of collisions and finish F0 with `z`. -/
def roundsBlock (κ : ℕ) {a : ℕ}
    (isRun : (Fin (Garity κ a) → Fin a → K) → (Fin (Garity κ a) → K) × (Fin (Garity κ a) → K))
    {t : ℕ} (z : Fin t → K) (col : Lev (Garity κ a) (Nat.clog 2 t) → Fin a → K) :
    Lev (Garity κ a) (Nat.clog 2 t) → K :=
  planF0 κ isRun (Nat.clog 2 t)
    (fun k => if h : (typEquiv _ k).val < t then z ⟨_, h⟩ else 0) col

omit [DecidableEq K] in
/-- The zero sum placed on the first `t` of the `2^L` representations. -/
theorem zeroSum_lift {κ t : ℕ} (hκ : 0 < κ) (z : Fin t → K) (hz0 : z ≠ 0)
    (hz : ∑ i, z i ^ κ = 0) (L : ℕ) (hL : t ≤ 2 ^ L) :
    let ρ0 : Typ L → K := fun k => if h : (typEquiv L k).val < t then z ⟨_, h⟩ else 0
    ρ0 ≠ 0 ∧ ∑ k, ρ0 k ^ κ * cTyp (1 : K) L k = 0 := by
  intro ρ0
  refine ⟨fun h => hz0 (funext fun i => ?_), ?_⟩
  · have := congrFun h ((typEquiv L).symm (Fin.castLE hL i))
    simpa [ρ0] using this
  · simp_rw [cTyp_one, mul_one]
    rw [← (typEquiv L).symm.sum_comp]
    simp only [ρ0, Equiv.apply_symm_apply]
    rw [← hz, ← Finset.sum_subset (s₁ := Finset.univ.map (Fin.castLEEmb hL))
      (Finset.subset_univ _)]
    · rw [Finset.sum_map]
      refine Finset.sum_congr rfl fun i _ => ?_
      simp
    · intro i _ hi
      have : ¬ i.val < t := by
        intro hlt
        exact hi (Finset.mem_map.mpr ⟨⟨i.val, hlt⟩, Finset.mem_univ _, by ext; simp⟩)
      simp [this, hz, hκ.ne']

/-- **Lemma `lem:rounds`.** Let `κ ≥ 1`, `z ∈ K^t` nonzero with `∑ z_i^κ = 0`,
`L = ⌈log₂ t⌉`, and let `isRun` answer every collision call as Theorem `thm:is-import`
says (`hIS`). Then for every `M ≥ G(κ, a)^L` and all columns `λ_1, …, λ_M ∈ K^a`, the
output `s` is nonzero and `∑ s_i^κ λ_i = 0`. (The paper's hypotheses `κ ≥ 2`,
`κ ∣ p - 1` are needed only by the imported theorem, i.e. for `hIS` to be satisfiable.) -/
theorem rounds_spec {κ a t : ℕ} (hκ : 0 < κ)
    (isRun : (Fin (Garity κ a) → Fin a → K) → (Fin (Garity κ a) → K) × (Fin (Garity κ a) → K))
    (hIS : ∀ v, ∃ o : ISOut κ v, isRun v = o.rs)
    (z : Fin t → K) (hz0 : z ≠ 0) (hz : ∑ i, z i ^ κ = 0) {M : ℕ}
    (hM : Garity κ a ^ Nat.clog 2 t ≤ M) (col : Fin M → Fin a → K) :
    IsRootSol κ col
      (padRun (onFin (levEquiv _ _) (roundsBlock κ isRun z)) col) := by
  refine padRun_spec hκ _ col hM (onFin_spec _ _ (fun col' => ?_) _)
  have horc : ∀ v, StepSpec κ 1 v (isRun v).1 (isRun v).2 := by
    intro v
    obtain ⟨o, ho⟩ := hIS v
    rw [ho]
    exact o.stepSpec hκ
  have hz' := zeroSum_lift hκ z hz0 hz (Nat.clog 2 t) (Nat.le_pow_clog one_lt_two t)
  exact planF0_spec hκ one_ne_zero isRun horc _ _ hz'.1 hz'.2 col'

/-- The number of collision calls of `L` levels with `A`-ary steps satisfies
`calls 0 = 0`, `calls (ℓ + 1) = A · calls ℓ + 1` (the count in the proof of
`lem:rounds`); it equals `∑_{j < ℓ} A^j`. This counts the calls in the recursion
`runLevel` (one oracle call per level-`(ℓ+1)` block whose sub-blocks all return
objects, so at most this many); the inequality to the run itself is not formalized. -/
def calls (A : ℕ) : ℕ → ℕ
  | 0 => 0
  | ℓ + 1 => A * calls A ℓ + 1

theorem calls_eq (A : ℕ) : ∀ ℓ, calls A ℓ = ∑ j ∈ Finset.range ℓ, A ^ j
  | 0 => rfl
  | ℓ + 1 => by
    rw [calls, calls_eq A ℓ, Finset.sum_range_succ', Finset.mul_sum]
    simp [pow_succ']

end Rounds

end QSearch.Schedule1H
