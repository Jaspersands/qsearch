import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Algebra.Module.Pi
import Mathlib.Algebra.Module.BigOperators
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/-!
# Schedule 1H, part 1: solutions, solvers, representations, objects, Lemma `lem:finish`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:halving`
("Schedule 1H: Halving the Degree"), paragraphs "Solutions and solvers" and
"Representations and objects", and Lemma `lem:finish`.

Encoding.

* `Pow κ` is the paper's `P = {x ^ κ : x ∈ K^×}` (nonzero `κ`-th powers).
* `IsKSolution κ col w r` is the paper's `κ`-solution `(w, r)`: `w ∈ (P ∪ {0})^M`,
  `w ≠ 0`, `r_b ^ κ = w_b`, `∑ w_b λ_b = 0`. `isKSolution_iff` shows it is the same as a
  nonzero root vector `r` with `∑ r_b ^ κ λ_b = 0` (`IsRootSol`), with `w = r ^ κ`.
  All algorithms below return the root vector `r`; `w` is `r ^ κ`.
* An object of type `c : τ → K` on a column index type `ι` (`Obj`, `IsObj`) is a vector
  `v`, a labelling `part : ι → Option τ` and roots `root : ι → K`. Its representation
  `R_k` is the index set `{i | part i = some k}` with weights `root i ^ κ`. Distinct
  representations are disjoint by construction (each column has at most one label), and
  the support is `{i | part i ≠ none}`. `IsObj.paperRep` restates `IsObj` in the paper's
  form (nonempty index sets, weights in `P`, roots, value `c_k v`, pairwise disjoint).
* Combining `N` objects with pairwise disjoint supports is modelled by the product column
  type `β × ι` (object `b` lives on `{b} × ι`), so disjointness of supports is structural.

Main results.

* `solOf_spec`: a root relation `∑ ρ_b^κ v_b = 0` among objects gives a `κ`-solution
  (first representation of each object, scaled).
* `combine_spec`: two disjoint root vectors `ρ, σ` with `∑ σ^κ v = e ∑ ρ^κ v` give an
  object of type `(c, e c)` (this is the core of Lemmas `lem:stage` and `lem:rounds`).
* `finishGen_spec`, `finishF0_spec`, `finishF1_spec`: Lemma `lem:finish` (F0) and (F1).
  F1 is stated for any nonzero `η` with `∑ η_ν v_ν = 0`; the Gaussian-elimination
  instance is in `Formal.Schedule1H.Levels` (`kernelVec`).

Nothing here is probabilistic; running time is not formalized.
-/

namespace QSearch.Schedule1H

open Finset

variable {K : Type*} [Field K]

/-- The paper's `P`: the nonzero `κ`-th powers. -/
def Pow (κ : ℕ) : Set K := {x | x ≠ 0 ∧ ∃ r : K, r ^ κ = x}

section Solutions

variable {ι V : Type*} [Fintype ι] [AddCommGroup V] [Module K V]

/-- **The paper's `κ`-solution** for columns `col : ι → V`: a pair `(w, r)` with
`w ∈ (P ∪ {0})^ι`, `w ≠ 0`, `r_b ^ κ = w_b` and `∑ w_b λ_b = 0`. -/
def IsKSolution (κ : ℕ) (col : ι → V) (w r : ι → K) : Prop :=
  (∀ b, w b ∈ Pow κ ∨ w b = 0) ∧ w ≠ 0 ∧ (∀ b, r b ^ κ = w b) ∧ ∑ b, w b • col b = 0

/-- Root form of a `κ`-solution: `r ≠ 0` and `∑ r_b ^ κ λ_b = 0`. -/
def IsRootSol (κ : ℕ) (col : ι → V) (r : ι → K) : Prop :=
  r ≠ 0 ∧ ∑ b, r b ^ κ • col b = 0

/-- A `κ`-solution is exactly a root solution `r`, with `w = r ^ κ` (for `κ ≥ 1`). -/
theorem isKSolution_iff {κ : ℕ} (hκ : 0 < κ) (col : ι → V) (w r : ι → K) :
    IsKSolution κ col w r ↔ w = (fun b => r b ^ κ) ∧ IsRootSol κ col r := by
  constructor
  · rintro ⟨_, hw0, hr, hsum⟩
    have hw : w = fun b => r b ^ κ := funext fun b => (hr b).symm
    refine ⟨hw, fun h0 => hw0 ?_, ?_⟩
    · rw [hw, h0]; funext b; simp [zero_pow hκ.ne']
    · rw [← hsum, hw]
  · rintro ⟨rfl, hr0, hsum⟩
    refine ⟨fun b => ?_, fun h => hr0 ?_, fun b => rfl, hsum⟩
    · by_cases hb : r b = 0
      · right; simp [hb, zero_pow hκ.ne']
      · left; exact ⟨pow_ne_zero _ hb, r b, rfl⟩
    · funext b
      have := congrFun h b
      simpa [pow_eq_zero_iff hκ.ne'] using this

/-- Root solutions are `κ`-solutions with `w = r ^ κ`. -/
theorem IsRootSol.isKSolution {κ : ℕ} (hκ : 0 < κ) {col : ι → V} {r : ι → K}
    (h : IsRootSol κ col r) : IsKSolution κ col (fun b => r b ^ κ) r :=
  (isKSolution_iff hκ col _ r).mpr ⟨rfl, h⟩

/-- Transport of a root solution along a bijection of column indices. -/
theorem IsRootSol.comp_equiv {ι' : Type*} [Fintype ι'] {κ : ℕ} (e : ι' ≃ ι) {col : ι → V}
    {r : ι' → K} (h : IsRootSol κ (col ∘ e) r) : IsRootSol κ col (r ∘ e.symm) := by
  refine ⟨fun h0 => h.1 (funext fun i => by simpa using congrFun h0 (e i)), ?_⟩
  rw [← h.2]
  exact (Fintype.sum_equiv e _ _ (fun b => by simp)).symm

end Solutions

section Solvers

/-- **The paper's `κ`-solver of arity `N(a)`**, in the "further columns get weight `0`"
form: for every `a`, every `n ≥ N(a)` and all columns `λ_1, …, λ_n ∈ K^a`, `run a n col`
is a root solution (so `(r ^ κ, r)` is a `κ`-solution by `IsRootSol.isKSolution`). -/
def IsKSolver (κ : ℕ) (N : ℕ → ℕ) (run : (a n : ℕ) → (Fin n → Fin a → K) → Fin n → K) :
    Prop :=
  ∀ a n (col : Fin n → Fin a → K), N a ≤ n → IsRootSol κ col (run a n col)

/-- Truncate to the first `N` columns and extend the answer by zeros. -/
def padRun {N n a : ℕ} (f : (Fin N → Fin a → K) → Fin N → K) (col : Fin n → Fin a → K) :
    Fin n → K :=
  if h : N ≤ n then
    fun i => if hi : i.val < N then f (fun j => col (Fin.castLE h j)) ⟨i.val, hi⟩ else 0
  else 0

/-- Padding preserves solutions: a solver on exactly `N` columns gives one on `n ≥ N`. -/
theorem padRun_spec {κ N n a : ℕ} (hκ : 0 < κ) (f : (Fin N → Fin a → K) → Fin N → K)
    (col : Fin n → Fin a → K) (hN : N ≤ n)
    (hf : IsRootSol κ (fun j => col (Fin.castLE hN j)) (f (fun j => col (Fin.castLE hN j)))) :
    IsRootSol κ col (padRun f col) := by
  set g := f (fun j => col (Fin.castLE hN j))
  have hval : padRun f col = fun i => if hi : i.val < N then g ⟨i.val, hi⟩ else 0 := by
    simp [padRun, hN, g]
  rw [hval]
  refine ⟨fun h0 => hf.1 (funext fun j => ?_), ?_⟩
  · have := congrFun h0 (Fin.castLE hN j)
    simpa using this
  · rw [← hf.2]
    rw [← Finset.sum_subset (s₁ := (Finset.univ.map (Fin.castLEEmb hN))) (Finset.subset_univ _)]
    · rw [Finset.sum_map]
      refine Finset.sum_congr rfl fun j _ => ?_
      simp
    · intro i _ hi
      have : ¬ i.val < N := by
        intro hlt
        exact hi (Finset.mem_map.mpr ⟨⟨i.val, hlt⟩, Finset.mem_univ _, by ext; simp⟩)
      simp [this, zero_pow hκ.ne']

end Solvers

section Objects

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- Data of an object: vector `v`, the representation label of each column (`none` off the
support), and the root at each column. -/
structure Obj (ι τ V K : Type*) where
  v : V
  part : ι → Option τ
  root : ι → K

instance {ι τ V K : Type*} [Zero V] [Zero K] : Inhabited (Obj ι τ V K) :=
  ⟨⟨0, fun _ => none, fun _ => 0⟩⟩

variable {ι τ : Type*} [Fintype ι] [DecidableEq τ]

/-- The value of representation `R_k`: `∑_{i ∈ R_k} root_i ^ κ λ_i`. -/
def Obj.repSum (κ : ℕ) (col : ι → V) (o : Obj ι τ V K) (k : τ) : V :=
  ∑ i, if o.part i = some k then o.root i ^ κ • col i else 0

/-- **The paper's object of type `c`**: every representation is nonempty, carries nonzero
roots (so weights in `P`), and represents `c_k v`. -/
def IsObj (κ : ℕ) (col : ι → V) (c : τ → K) (o : Obj ι τ V K) : Prop :=
  (∀ i, o.part i ≠ none → o.root i ≠ 0) ∧ (∀ k, ∃ i, o.part i = some k) ∧
    (∀ k, o.repSum κ col k = c k • o.v)

/-- `IsObj` in the paper's words: the index sets `S_k = {i | part i = some k}` are
nonempty and pairwise disjoint, their weights `root_i ^ κ` lie in `P` with roots
`root_i`, and `∑_{i ∈ S_k} w_i λ_i = c_k v`. -/
theorem IsObj.paperRep {κ : ℕ} {col : ι → V} {c : τ → K} {o : Obj ι τ V K}
    (h : IsObj κ col c o) (k : τ) :
    (Finset.univ.filter fun i => o.part i = some k).Nonempty ∧
    (∀ i ∈ Finset.univ.filter (fun i => o.part i = some k), o.root i ^ κ ∈ Pow κ) ∧
    ∑ i ∈ Finset.univ.filter (fun i => o.part i = some k), o.root i ^ κ • col i = c k • o.v ∧
    (∀ k', k' ≠ k → Disjoint (Finset.univ.filter fun i => o.part i = some k)
      (Finset.univ.filter fun i => o.part i = some k')) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · obtain ⟨i, hi⟩ := h.2.1 k
    exact ⟨i, by simp [hi]⟩
  · intro i hi
    have hi' : o.part i = some k := by simpa using hi
    have hr := h.1 i (by simp [hi'])
    exact ⟨pow_ne_zero _ hr, o.root i, rfl⟩
  · rw [Finset.sum_filter]; exact h.2.2 k
  · intro k' hk'
    rw [Finset.disjoint_filter]
    intro i _ h1 h2
    rw [h1] at h2
    exact hk' (Option.some_injective _ h2).symm

/-- A column `x` as an object of type `(1)`: one representation `{the column}`, root `1`. -/
def colObj (x : V) : Obj Unit Unit V K := ⟨x, fun _ => some (), fun _ => 1⟩

theorem colObj_spec (κ : ℕ) (col : Unit → V) :
    IsObj κ col (fun _ => (1 : K)) (colObj (col ())) := by
  refine ⟨fun _ _ => one_ne_zero, fun _ => ⟨(), rfl⟩, fun k => ?_⟩
  simp [Obj.repSum, colObj]

variable {β : Type*} [Fintype β]

/-- **Solution from a relation among objects.** Scale the representation `R_{k0}` of
object `b` by `ρ_b`. -/
def solOf (k0 : τ) (o : β → Obj ι τ V K) (ρ : β → K) : β × ι → K :=
  fun p => if (o p.1).part p.2 = some k0 then ρ p.1 * (o p.1).root p.2 else 0

theorem repSum_scaled (κ : ℕ) (col : ι → V) (o : Obj ι τ V K) (k : τ) (x : K) :
    (∑ i, if o.part i = some k then (x * o.root i) ^ κ • col i else 0) =
      x ^ κ • o.repSum κ col k := by
  rw [Obj.repSum, Finset.smul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  split_ifs <;> simp [mul_pow, mul_smul]

theorem solOf_spec {κ : ℕ} (hκ : 0 < κ) (k0 : τ) (col : β × ι → V) (c : τ → K)
    (o : β → Obj ι τ V K) (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b)) (ρ : β → K)
    (hρ : ρ ≠ 0) (hsum : ∑ b, ρ b ^ κ • (o b).v = 0) :
    IsRootSol κ col (solOf k0 o ρ) := by
  refine ⟨fun h0 => ?_, ?_⟩
  · apply hρ
    funext b
    by_contra hb
    obtain ⟨i, hi⟩ := (ho b).2.1 k0
    have := congrFun h0 (b, i)
    simp only [solOf, hi, ite_true, Pi.zero_apply] at this
    exact mul_ne_zero hb ((ho b).1 i (by simp [hi])) this
  · rw [Fintype.sum_prod_type]
    have : ∀ b, (∑ i, solOf k0 o ρ (b, i) ^ κ • col (b, i)) = c k0 • (ρ b ^ κ • (o b).v) := by
      intro b
      have h1 : (∑ i, solOf k0 o ρ (b, i) ^ κ • col (b, i)) =
          ∑ i, if (o b).part i = some k0 then (ρ b * (o b).root i) ^ κ • col (b, i) else 0 := by
        refine Finset.sum_congr rfl fun i _ => ?_
        simp only [solOf]
        split_ifs <;> simp [zero_pow hκ.ne']
      rw [h1, repSum_scaled κ (fun i => col (b, i)) (o b) k0 (ρ b), (ho b).2.2 k0, smul_comm]
    simp_rw [this, ← Finset.smul_sum, hsum, smul_zero]

/-- The type `(c, e c)` (paper: `(c_1, …, c_r, e c_1, …, e c_r)`), indexed by `τ ⊕ τ`. -/
def extType (c : τ → K) (e : K) : τ ⊕ τ → K := Sum.elim c (fun k => e * c k)

/-- **Combining objects into one object of type `(c, e c)`.** `ρ` and `σ` are root
vectors with disjoint supports (the paper's `I` and `J` with their roots). -/
def combine [DecidableEq K] (o : β → Obj ι τ V K) (ρ σ : β → K) (U : V) : Obj (β × ι) (τ ⊕ τ) V K where
  v := U
  part p := if ρ p.1 ≠ 0 then ((o p.1).part p.2).map Sum.inl
    else if σ p.1 ≠ 0 then ((o p.1).part p.2).map Sum.inr else none
  root p := (if ρ p.1 ≠ 0 then ρ p.1 else σ p.1) * (o p.1).root p.2

theorem combine_spec [DecidableEq K] {κ : ℕ} (hκ : 0 < κ) (col : β × ι → V) (c : τ → K) (e : K)
    (o : β → Obj ι τ V K) (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b)) (ρ σ : β → K)
    (hdisj : ∀ b, ρ b = 0 ∨ σ b = 0) (hρ : ρ ≠ 0) (hσ : σ ≠ 0)
    (hrel : ∑ b, σ b ^ κ • (o b).v = e • ∑ b, ρ b ^ κ • (o b).v) :
    IsObj κ col (extType c e) (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)) := by
  have hne : ∀ f : β → K, f ≠ 0 → ∃ b, f b ≠ 0 := fun f hf => by
    by_contra h; push Not at h; exact hf (funext h)
  have hv : (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)).v = ∑ b, ρ b ^ κ • (o b).v := rfl
  refine ⟨?_, ?_, ?_⟩
  · rintro ⟨b, i⟩ hp
    by_cases hb : ρ b = 0
    · by_cases hs : σ b = 0
      · simp [combine, hb, hs] at hp
      · have hp' : (o b).part i ≠ none := by simpa [combine, hb, hs] using hp
        simpa [combine, hb, hs] using mul_ne_zero hs ((ho b).1 i hp')
    · have hp' : (o b).part i ≠ none := by simpa [combine, hb] using hp
      simpa [combine, hb] using mul_ne_zero hb ((ho b).1 i hp')
  · rintro (k | k)
    · obtain ⟨b, hb⟩ := hne ρ hρ
      obtain ⟨i, hi⟩ := (ho b).2.1 k
      exact ⟨(b, i), by simp [combine, hb, hi]⟩
    · obtain ⟨b, hb⟩ := hne σ hσ
      have hρb : ρ b = 0 := (hdisj b).resolve_right hb
      obtain ⟨i, hi⟩ := (ho b).2.1 k
      exact ⟨(b, i), by simp [combine, hb, hρb, hi]⟩
  · rintro (k | k)
    · simp only [Obj.repSum, extType, Sum.elim_inl]
      rw [hv, Fintype.sum_prod_type, Finset.smul_sum]
      refine Finset.sum_congr rfl fun b _ => ?_
      by_cases hb : ρ b ≠ 0
      · have h1 : (∑ i, if (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)).part (b, i) = some (Sum.inl k)
            then (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)).root (b, i) ^ κ • col (b, i) else 0) =
            ∑ i, if (o b).part i = some k then (ρ b * (o b).root i) ^ κ • col (b, i) else 0 := by
          refine Finset.sum_congr rfl fun i _ => ?_
          simp only [combine, hb, ite_true, ne_eq, not_false_eq_true]
          congr 1
          cases (o b).part i <;> simp
        rw [h1, repSum_scaled κ (fun i => col (b, i)) (o b) k (ρ b), (ho b).2.2 k, smul_comm]
      · push Not at hb
        rw [hb, zero_pow hκ.ne', zero_smul, smul_zero]
        refine Finset.sum_eq_zero fun i _ => ?_
        simp only [combine, hb, ne_eq, not_true_eq_false, ite_false]
        split_ifs with h1 h2 <;> simp_all
    · simp only [Obj.repSum, extType, Sum.elim_inr]
      rw [hv, Fintype.sum_prod_type, mul_comm, mul_smul, ← hrel, Finset.smul_sum]
      refine Finset.sum_congr rfl fun b _ => ?_
      by_cases hs : σ b ≠ 0
      · have hρb : ρ b = 0 := (hdisj b).resolve_right hs
        have h1 : (∑ i, if (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)).part (b, i) = some (Sum.inr k)
            then (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v)).root (b, i) ^ κ • col (b, i) else 0) =
            ∑ i, if (o b).part i = some k then (σ b * (o b).root i) ^ κ • col (b, i) else 0 := by
          refine Finset.sum_congr rfl fun i _ => ?_
          simp only [combine, hρb, hs, ne_eq, not_true_eq_false, ite_false, not_false_eq_true,
            ite_true]
          congr 1
          cases (o b).part i <;> simp
        rw [h1, repSum_scaled κ (fun i => col (b, i)) (o b) k (σ b), (ho b).2.2 k, smul_comm]
      · push Not at hs
        rw [hs, zero_pow hκ.ne', zero_smul, smul_zero]
        refine Finset.sum_eq_zero fun i _ => ?_
        simp only [combine, hs, ne_eq, not_true_eq_false, ite_false]
        split_ifs with h1 h2 <;> simp_all

/-- **The step specification.** `ρ ≠ 0`, `ρ` and `σ` have disjoint supports, and
`∑ σ_b^κ v_b = e ∑ ρ_b^κ v_b`. Both Lemma `lem:stage` (with `e = ε`) and the collision
step of Lemma `lem:rounds` (with `e = 1`) produce such a pair. -/
def StepSpec (κ : ℕ) (e : K) (v : β → V) (ρ σ : β → K) : Prop :=
  ρ ≠ 0 ∧ (∀ b, ρ b = 0 ∨ σ b = 0) ∧ ∑ b, σ b ^ κ • v b = e • ∑ b, ρ b ^ κ • v b

/-- One step: a `κ`-solution if `σ = 0`, otherwise the combined object. -/
def step [DecidableEq K] (κ : ℕ) (k0 : τ) (o : β → Obj ι τ V K) (ρ σ : β → K) :
    (β × ι → K) ⊕ Obj (β × ι) (τ ⊕ τ) V K :=
  if ∀ b, σ b = 0 then Sum.inl (solOf k0 o ρ)
  else Sum.inr (combine o ρ σ (∑ b, ρ b ^ κ • (o b).v))

/-- Correctness predicate for a result: a root solution, or an object of type `c`. -/
def ResOK {ι' τ' : Type*} [Fintype ι'] [DecidableEq τ'] (κ : ℕ) (col : ι' → V) (c : τ' → K) :
    (ι' → K) ⊕ Obj ι' τ' V K → Prop
  | Sum.inl r => IsRootSol κ col r
  | Sum.inr o => IsObj κ col c o

theorem step_spec [DecidableEq K] {κ : ℕ} (hκ : 0 < κ) (k0 : τ) (col : β × ι → V) (c : τ → K) {e : K}
    (he : e ≠ 0) (o : β → Obj ι τ V K) (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b))
    (ρ σ : β → K) (hs : StepSpec κ e (fun b => (o b).v) ρ σ) :
    ResOK κ col (extType c e) (step κ k0 o ρ σ) := by
  obtain ⟨hρ, hdisj, hrel⟩ := hs
  unfold step
  split_ifs with h0
  · refine solOf_spec hκ k0 col c o ho ρ hρ ?_
    have : ∑ b, σ b ^ κ • (o b).v = 0 := by simp [h0, zero_pow hκ.ne']
    rw [this] at hrel
    have h2 := congrArg (fun x => e⁻¹ • x) hrel.symm
    simpa [smul_smul, inv_mul_cancel₀ he] using h2
  · exact combine_spec hκ col c e o ho ρ σ hdisj hρ
      (fun h => h0 fun b => by simpa using congrFun h b) hrel

end Objects

section Finish

variable {V : Type*} [AddCommGroup V] [Module K V]
variable {ι τ β : Type*} [Fintype ι] [Fintype τ] [DecidableEq τ] [Fintype β]

/-- The paper's `T(c) = {∑ y_k c_k : y ∈ (P ∪ {0})^r, y ≠ 0}`. -/
def Tset (κ : ℕ) (c : τ → K) : Set K :=
  {x | ∃ y : τ → K, (∀ k, y k ∈ Pow κ ∨ y k = 0) ∧ y ≠ 0 ∧ ∑ k, y k * c k = x}

omit [DecidableEq τ] in
/-- `T(c)` through roots: `x ∈ T(c)` iff `x = ∑ ρ_k ^ κ c_k` for a nonzero root vector `ρ`. -/
theorem mem_Tset_iff {κ : ℕ} (hκ : 0 < κ) (c : τ → K) (x : K) :
    x ∈ Tset κ c ↔ ∃ ρ : τ → K, ρ ≠ 0 ∧ ∑ k, ρ k ^ κ * c k = x := by
  constructor
  · rintro ⟨y, hy, hy0, rfl⟩
    choose ρ hρ using fun k => (show ∃ r : K, r ^ κ = y k from by
      rcases hy k with ⟨_, r, hr⟩ | h
      · exact ⟨r, hr⟩
      · exact ⟨0, by simp [h, zero_pow hκ.ne']⟩)
    refine ⟨ρ, fun h => hy0 (funext fun k => ?_), by simp [hρ]⟩
    rw [← hρ k, h]; simp [zero_pow hκ.ne']
  · rintro ⟨ρ, hρ, rfl⟩
    refine ⟨fun k => ρ k ^ κ, fun k => ?_, fun h => hρ (funext fun k => ?_), rfl⟩
    · by_cases hk : ρ k = 0
      · right; simp [hk, zero_pow hκ.ne']
      · left; exact ⟨pow_ne_zero _ hk, ρ k, rfl⟩
    · have := congrFun h k
      simpa [pow_eq_zero_iff hκ.ne'] using this

/-- **Generic finish.** Objects `o_b` of type `c`, root vectors `y_b` with
`∑_k y_{b,k}^κ c_k = η_b`, `∑ η_b v_b = 0`, and some `y_b ≠ 0`: the representations
`y_{b,k} R_k(o_b)` form a `κ`-solution. -/
def finishGen (o : β → Obj ι τ V K) (y : β → τ → K) : β × ι → K :=
  fun p => match (o p.1).part p.2 with
    | some k => y p.1 k * (o p.1).root p.2
    | none => 0

theorem finishGen_spec {κ : ℕ} (hκ : 0 < κ) (col : β × ι → V) (c : τ → K)
    (o : β → Obj ι τ V K) (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b))
    (y : β → τ → K) (η : β → K) (hy : ∀ b, ∑ k, y b k ^ κ * c k = η b)
    (hη : ∑ b, η b • (o b).v = 0) (hy0 : ∃ b, y b ≠ 0) :
    IsRootSol κ col (finishGen o y) := by
  refine ⟨fun h0 => ?_, ?_⟩
  · obtain ⟨b, hb⟩ := hy0
    apply hb
    funext k
    obtain ⟨i, hi⟩ := (ho b).2.1 k
    have := congrFun h0 (b, i)
    simp only [finishGen, hi, Pi.zero_apply] at this
    exact (mul_eq_zero.mp this).resolve_right ((ho b).1 i (by simp [hi]))
  · rw [Fintype.sum_prod_type, ← hη]
    refine Finset.sum_congr rfl fun b _ => ?_
    have h1 : (∑ i, finishGen o y (b, i) ^ κ • col (b, i)) =
        ∑ k, ∑ i, if (o b).part i = some k then (y b k * (o b).root i) ^ κ • col (b, i)
          else 0 := by
      rw [Finset.sum_comm]
      refine Finset.sum_congr rfl fun i _ => ?_
      simp only [finishGen]
      cases h : (o b).part i with
      | none => simp [zero_pow hκ.ne']
      | some k' =>
        simp only [Option.some.injEq]
        rw [Finset.sum_ite_eq]
        simp
    rw [h1]
    simp_rw [repSum_scaled κ (fun i => col (b, i)) (o b), (ho b).2.2, smul_smul,
      ← Finset.sum_smul, hy]

/-- **Lemma `lem:finish` (F0).** One object `o` of type `c` and a root vector `ρ ≠ 0`
with `∑ ρ_k^κ c_k = 0` (so `0 ∈ T(c)`) give a `κ`-solution supported in the support of
`o`. (The paper allows `N ≥ 1` objects and uses `o_1`; extra objects get weight `0`.) -/
def finishF0 (o : Obj ι τ V K) (ρ : τ → K) : ι → K :=
  fun i => match o.part i with
    | some k => ρ k * o.root i
    | none => 0

theorem finishF0_spec {κ : ℕ} (hκ : 0 < κ) (col : ι → V) (c : τ → K) (o : Obj ι τ V K)
    (ho : IsObj κ col c o) (ρ : τ → K) (hρ : ρ ≠ 0) (hz : ∑ k, ρ k ^ κ * c k = 0) :
    IsRootSol κ col (finishF0 o ρ) := by
  have h := finishGen_spec (β := Unit) hκ (fun p => col p.2) c (fun _ => o) (fun _ => ho)
    (fun _ => ρ) (fun _ => 0) (fun _ => hz) (by simp) ⟨(), hρ⟩
  exact IsRootSol.comp_equiv (Equiv.punitProd ι) h

/-- Support of a root vector (the indices where it is nonzero). -/
def rootSupport {ι' : Type*} [Fintype ι'] (r : ι' → K) : Set ι' := {i | r i ≠ 0}

omit [AddCommGroup V] [Module K V] [Fintype ι] [Fintype τ] [DecidableEq τ] in
/-- (F0) support claim: the solution is supported in the support of `o`. -/
theorem finishF0_support (o : Obj ι τ V K) (ρ : τ → K) (i : ι) (hi : finishF0 o ρ i ≠ 0) :
    o.part i ≠ none := by
  intro h; simp [finishF0, h] at hi

/-- **Lemma `lem:finish` (F1).** Objects `o_ν` of type `c` with disjoint supports
(`β × ι`), a nonzero `η` with `∑ η_ν v_ν = 0`, and for each `η_ν ≠ 0` a root vector
`fin η_ν ≠ 0` with `∑_k (fin η_ν)_k^κ c_k = η_ν` (this needs `T(c) ⊇ K^×`). The paper
takes `N = a + 1` and `η` from Gaussian elimination; here any such `η` works. -/
def finishF1 [DecidableEq K] (o : β → Obj ι τ V K) (fin : K → τ → K) (η : β → K) :
    β × ι → K :=
  finishGen o (fun b => if η b = 0 then 0 else fin (η b))

theorem finishF1_spec [DecidableEq K] {κ : ℕ} (hκ : 0 < κ) (col : β × ι → V) (c : τ → K)
    (o : β → Obj ι τ V K) (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b))
    (fin : K → τ → K) (hfin : ∀ x : K, x ≠ 0 → fin x ≠ 0 ∧ ∑ k, fin x k ^ κ * c k = x)
    (η : β → K) (hη0 : η ≠ 0) (hη : ∑ b, η b • (o b).v = 0) :
    IsRootSol κ col (finishF1 o fin η) := by
  refine finishGen_spec hκ col c o ho _ η (fun b => ?_) hη ?_
  · by_cases hb : η b = 0
    · simp [hb, zero_pow hκ.ne']
    · simp only [hb, ite_false]; exact (hfin _ hb).2
  · by_contra h
    push Not at h
    apply hη0
    funext b
    by_contra hb
    have hb' : η b ≠ 0 := by simpa using hb
    have := h b
    exact (hfin _ hb').1 (by simpa [hb'] using this)

omit [AddCommGroup V] [Module K V] [Fintype ι] [Fintype τ] [DecidableEq τ] [Fintype β] in
/-- (F1) support claim: the solution is supported in the union of the supports. -/
theorem finishF1_support [DecidableEq K] (o : β → Obj ι τ V K) (fin : K → τ → K) (η : β → K)
    (p : β × ι) (hp : finishF1 o fin η p ≠ 0) : (o p.1).part p.2 ≠ none := by
  intro h; simp [finishF1, finishGen, h] at hp

end Finish

end QSearch.Schedule1H
