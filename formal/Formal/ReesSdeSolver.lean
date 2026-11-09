import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.Module.Pi
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Module
import Formal.ReesSdeTriangular
import Formal.ReesSdeQuadratic
import Formal.ReesSdeWitness
import Mathlib.Tactic.NormNum.Prime

/-!
# Rees SDE: computable solvers for the diagonal equation `∑ s_i ^ d λ_i = 0`

Source: `docs/papers/rees-hsp/main.tex`, Proposition `prop:triangular-sde` (the
triangular two-level solver), Theorem `thm:power-sde`(i) (the linear case `κ = 1`) and
the Chevalley–Warning arity `κ a + 1`.

`ReesSdeTriangular`, `ReesSdeQuadratic` and `ReesSdeWitness` prove that solutions exist.
This file gives algorithms, as ordinary `def`s that Lean compiles and runs (`#eval` at
the end), and proves that their outputs are solutions.

* **Elimination.** `kernelVec n m w` returns `c` with `c ≠ 0` and `∑ c_j w_j = 0` when
  `n < m` (`kernelVec_spec`); `solveVec n m w t` returns `some c` with `∑ c_j w_j = t`
  (`solveVec_some`) or `none`, and then `t` is not in the span (`solveVec_none`). Both
  eliminate the last coordinate and recurse.
* **The triangular solver** (`triSolve`, `triSolve_spec`). Input: the contraction as two
  functions `A, B : K → K` (the paper's `ζ ↦ α_{cos ζ}`, `δ ↦ β_{cos δ}`) and columns
  `λ_1, …, λ_M ∈ K^a`. Round `k` takes the next `a - k + 1` columns, finds a dependence
  modulo `U_k = span(v_1, …, v_k)` by one `kernelVec` call, normalises its first nonzero
  entry on the fresh columns to `1`, forms `v_{k+1} = ∑ β(δ_i) δ_i λ_i`, and tests
  `v_{k+1} ∈ U_k` by one `solveVec` call. The back substitution is a function `R` that
  realizes every vector of `U_k`. If `0 ∈ D`, `ζ δ (A ζ + B δ) ∈ D` for nonzero
  `ζ, δ`, `A 1 + B 1 ≠ 0` and `M ≥ (a + 1)(a + 2)/2`, the output is a nonzero
  `x ∈ D^M`, supported on the first `(a + 1)(a + 2)/2` columns, with `∑ x_i λ_i = 0`.
* **`κ = 2`** (`quadSolve_spec`). Over a finite field of odd characteristic, given
  `(α, β)` normalised by `α_0 = 1`, `β_0 = 0` with `(α_j + β_i) g^(i+j) ∈ P ∪ {0}` for a
  quadratic non-residue `g`: coset test by Euler's criterion, the triangular solver,
  then square roots by search through a list of all field elements. Over `ZMod p` the
  contraction `α = (1, 0)`, `β = (0, μ)` is computed by search (`findMu`), so
  `quadSolveZMod_spec` has no hypothesis but `p` odd and `M ≥ (a + 1)(a + 2)/2`;
  `quadSolveZModExp_spec` adds the Bezout exponent for `gcd(d, p - 1) = 2`.
* **`κ = 1`** (`linSolve_spec`): one `kernelVec` call on `a + 1` columns, then
  `s_i = c_i ^ t` with `t` the inverse of `d` modulo `q - 1` (`bezoutExp`).
* **Exhaustive search** (`cwSearch_witness`, `cwSearch_zmod_gcd`): the first nonzero
  solution in a list of all `K^M`; Chevalley–Warning (`ReesSdeWitness.exists_witness`)
  says it exists once `M > κ a`.

Solvers return a `Tab` (an array with its length), read by `Tab.get`; see `Tab` for why.
The running time is not formalized. The square-root step and the exhaustive search
visit up to `|K|` and `|K|^M` candidates; the paper's root extraction is Las Vegas and
is not formalized.
-/

namespace QSearch.ReesSdeSolver

variable {K : Type*} [Field K] [DecidableEq K]

/-- The first index where a Boolean test succeeds. -/
def findIdx : (m : ℕ) → (Fin m → Bool) → Option (Fin m)
  | 0, _ => none
  | m + 1, f => if f 0 then some 0 else (findIdx m (fun j => f j.succ)).map Fin.succ

theorem findIdx_some : ∀ {m : ℕ} {f : Fin m → Bool} {j : Fin m}, findIdx m f = some j →
    f j = true
  | 0, _, j, _ => j.elim0
  | m + 1, f, j, h => by
    unfold findIdx at h
    split_ifs at h with h0
    · cases h; exact h0
    · obtain ⟨j', hj', rfl⟩ := Option.map_eq_some_iff.mp h
      exact findIdx_some (m := m) hj'

theorem findIdx_none : ∀ {m : ℕ} {f : Fin m → Bool}, findIdx m f = none → ∀ j, f j = false
  | 0, _, _, j => j.elim0
  | m + 1, f, h, j => by
    unfold findIdx at h
    split_ifs at h with h0
    · simp at h0
      refine Fin.cases ?_ (fun j => ?_) j
      · exact h0
      · exact findIdx_none (Option.map_eq_none_iff.mp h) j

/-- The first `n` coordinates of a vector in `K^(n+1)`. -/
def headCoords {n : ℕ} (x : Fin (n + 1) → K) : Fin n → K := fun i => x i.castSucc

/-- A vector of length `m`, stored in an array. Every solver below returns a `Tab`, not a
function: Lean compiles a definition whose value is a function by eta-expanding it, so a
function-valued result would recompute the whole elimination at every index it is read
at. `Tab.get` reads it as a function, and `get_tab` says that `tab` does not change it. -/
structure Tab (m : ℕ) (α : Type*) where
  arr : Array α
  size_eq : arr.size = m

/-- Read a `Tab` as a function. -/
def Tab.get {α : Type*} {m : ℕ} (t : Tab m α) (i : Fin m) : α :=
  t.arr[i.val]'(by rw [t.size_eq]; exact i.isLt)

/-- Tabulate a function. -/
def tab {α : Type*} {m : ℕ} (f : Fin m → α) : Tab m α := ⟨Array.ofFn f, Array.size_ofFn⟩

omit [Field K] [DecidableEq K] in
@[simp] theorem get_tab {α : Type*} {m : ℕ} (f : Fin m → α) : (tab f).get = f :=
  funext fun i => by simp [tab, Tab.get]

/-- Tabulate a matrix, row by row. -/
def tabMat {m n : ℕ} (w : Fin m → Fin n → K) : Tab m (Tab n K) := tab fun j => tab (w j)

omit [Field K] [DecidableEq K] in
@[simp] theorem tabMat_get {m n : ℕ} (w : Fin m → Fin n → K) (j : Fin m) :
    ((tabMat w).get j).get = w j := by
  simp [tabMat]

/-- **Kernel vector by elimination of the last coordinate.** -/
def kernelVec : (n m : ℕ) → (Fin m → Fin n → K) → Tab m K
  | 0, _, _ => tab fun j => if j.val = 0 then 1 else 0
  | _ + 1, 0, _ => tab 0
  | n + 1, m' + 1, w =>
    match findIdx (m' + 1) (fun j => w j (Fin.last n) != 0) with
    | none =>
      let rows := tabMat fun j => headCoords (w j)
      kernelVec n (m' + 1) (fun j => (rows.get j).get)
    | some j0 =>
      let r := tab fun j => w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n)
      let rows := tabMat fun j => headCoords (w (j0.succAbove j)) - r.get j • headCoords (w j0)
      let c' := (kernelVec n m' (fun j => (rows.get j).get)).get
      tab (Fin.insertNth j0 (-(∑ j, c' j * r.get j)) c')

omit [Field K] [DecidableEq K] in
theorem vec_ext_last {n : ℕ} {x y : Fin (n + 1) → K} (h1 : headCoords x = headCoords y)
    (h2 : x (Fin.last n) = y (Fin.last n)) : x = y := by
  funext i
  rcases Fin.eq_castSucc_or_eq_last i with ⟨i, rfl⟩ | rfl
  · exact congrFun h1 i
  · exact h2

omit [DecidableEq K] in
theorem headCoords_sum {n m : ℕ} (c : Fin m → K) (w : Fin m → Fin (n + 1) → K) :
    headCoords (∑ j, c j • w j) = ∑ j, c j • headCoords (w j) := by
  funext i
  simp [headCoords, Finset.sum_apply]

omit [DecidableEq K] in
/-- The pivot step: if the reduced vectors `w_j - r_j w_{j0}` (`j ≠ j0`, first `n`
coordinates) combine to `t - t0 w_{j0}`, then inserting `t0 - ∑ c'_j r_j` at `j0`
combines the original vectors to `t`, provided `r_j piv = w_j(last)` and
`t0 piv = t(last)`. -/
theorem pivot_combine {n m' : ℕ} (w : Fin (m' + 1) → Fin (n + 1) → K) (j0 : Fin (m' + 1))
    (t : Fin (n + 1) → K) (r : Fin m' → K) (t0 : K) (c' : Fin m' → K)
    (hr : ∀ j, r j * w j0 (Fin.last n) = w (j0.succAbove j) (Fin.last n))
    (ht : t0 * w j0 (Fin.last n) = t (Fin.last n))
    (hsum : ∑ j, c' j • (headCoords (w (j0.succAbove j)) - r j • headCoords (w j0)) =
      headCoords t - t0 • headCoords (w j0)) :
    ∑ j, (Fin.insertNth j0 (t0 - ∑ j, c' j * r j) c' : Fin (m' + 1) → K) j • w j = t := by
  rw [Fin.sum_univ_succAbove _ j0]
  simp only [Fin.insertNth_apply_same, Fin.insertNth_apply_succAbove]
  apply vec_ext_last
  · funext i
    have hi := congrFun hsum i
    simp only [headCoords, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.sub_apply,
      Pi.add_apply, mul_sub] at hi ⊢
    rw [Finset.sum_sub_distrib] at hi
    have : ∑ x, c' x * (r x * w j0 i.castSucc) = (∑ x, c' x * r x) * w j0 i.castSucc := by
      rw [Finset.sum_mul]; exact Finset.sum_congr rfl fun _ _ => by ring
    rw [this] at hi
    linear_combination hi
  · simp only [Pi.add_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
    simp only [← hr, ← ht]
    have : ∑ x, c' x * (r x * w j0 (Fin.last n)) = (∑ x, c' x * r x) * w j0 (Fin.last n) := by
      rw [Finset.sum_mul]; exact Finset.sum_congr rfl fun _ _ => by ring
    rw [this]
    ring

/-- **Correctness of `kernelVec`.** More vectors than coordinates: the returned
coefficients are not all zero and give the zero combination. -/
theorem kernelVec_spec : ∀ (n m : ℕ) (w : Fin m → Fin n → K), n < m →
    (kernelVec n m w).get ≠ 0 ∧ ∑ j, (kernelVec n m w).get j • w j = 0
  | 0, m, w, hm => by
    refine ⟨fun h => ?_, funext fun i => i.elim0⟩
    have := congrFun h ⟨0, hm⟩
    simp [kernelVec] at this
  | n + 1, 0, w, hm => absurd hm (by omega)
  | n + 1, m' + 1, w, hm => by
    unfold kernelVec
    cases hfind : findIdx (m' + 1) (fun j => w j (Fin.last n) != 0) with
    | none =>
      simp only [tabMat_get]
      obtain ⟨hne, hsum⟩ := kernelVec_spec n (m' + 1) (fun j => headCoords (w j)) (by omega)
      refine ⟨hne, vec_ext_last ?_ ?_⟩
      · rw [headCoords_sum, hsum]; rfl
      · have hz := findIdx_none hfind
        simp only [bne_eq_false_iff_eq] at hz
        simp [Finset.sum_apply, hz]
    | some j0 =>
      have hpiv : w j0 (Fin.last n) ≠ 0 := by
        simpa using findIdx_some hfind
      simp only [get_tab, tabMat_get]
      obtain ⟨hne, hsum⟩ := kernelVec_spec n m'
        (fun j => headCoords (w (j0.succAbove j)) -
          (w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n)) • headCoords (w j0)) (by omega)
      set c' := (kernelVec n m'
        (fun j => headCoords (w (j0.succAbove j)) -
          (w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n)) • headCoords (w j0))).get
      refine ⟨fun h => hne (funext fun j => ?_), ?_⟩
      · have := congrFun h (j0.succAbove j)
        simpa [Fin.insertNth_apply_succAbove] using this
      have := pivot_combine w j0 0 (fun j => w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n))
        0 c' (fun j => by simp [hpiv]) (by simp) (by simp only [zero_smul, sub_zero]; exact hsum)
      simpa using this

/-- **Solving `∑ c_j w_j = t` by elimination of the last coordinate.** -/
def solveVec : (n m : ℕ) → (Fin m → Fin n → K) → (Fin n → K) → Option (Tab m K)
  | 0, _, _, _ => some (tab 0)
  | _ + 1, 0, _, t => if t = 0 then some (tab 0) else none
  | n + 1, m' + 1, w, t =>
    match findIdx (m' + 1) (fun j => w j (Fin.last n) != 0) with
    | none =>
      if t (Fin.last n) = 0 then
        let rows := tabMat fun j => headCoords (w j)
        solveVec n (m' + 1) (fun j => (rows.get j).get) (tab (headCoords t)).get
      else none
    | some j0 =>
      let r := tab fun j => w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n)
      let t0 := t (Fin.last n) / w j0 (Fin.last n)
      let rows := tabMat fun j => headCoords (w (j0.succAbove j)) - r.get j • headCoords (w j0)
      (solveVec n m' (fun j => (rows.get j).get)
        (tab (headCoords t - t0 • headCoords (w j0))).get).map
        (fun c' => tab (Fin.insertNth j0 (t0 - ∑ j, c'.get j * r.get j) c'.get))

/-- `some c` from `solveVec` solves the system. -/
theorem solveVec_some : ∀ (n m : ℕ) (w : Fin m → Fin n → K) (t : Fin n → K) (c : Tab m K),
    solveVec n m w t = some c → ∑ j, c.get j • w j = t
  | 0, _, _, t, _, _ => funext fun i => i.elim0
  | n + 1, 0, w, t, c, h => by
    unfold solveVec at h
    split_ifs at h with ht
    simp [ht]
  | n + 1, m' + 1, w, t, c, h => by
    unfold solveVec at h
    cases hfind : findIdx (m' + 1) (fun j => w j (Fin.last n) != 0) with
    | none =>
      rw [hfind] at h
      simp only [get_tab, tabMat_get] at h
      split_ifs at h with ht
      have hsum := solveVec_some n (m' + 1) _ _ c h
      refine vec_ext_last ?_ ?_
      · rw [headCoords_sum, hsum]
      · have hz := findIdx_none hfind
        simp only [bne_eq_false_iff_eq] at hz
        simp [Finset.sum_apply, hz, ht]
    | some j0 =>
      rw [hfind] at h
      simp only [get_tab, tabMat_get] at h
      have hpiv : w j0 (Fin.last n) ≠ 0 := by
        simpa using findIdx_some hfind
      obtain ⟨c', hc', rfl⟩ := Option.map_eq_some_iff.mp h
      rw [get_tab]
      exact pivot_combine w j0 t (fun j => w (j0.succAbove j) (Fin.last n) / w j0 (Fin.last n))
        _ c'.get (fun j => by simp [hpiv]) (by simp [hpiv]) (solveVec_some n m' _ _ c' hc')

/-- `none` from `solveVec`: `t` is not a combination of the `w_j`. -/
theorem solveVec_none : ∀ (n m : ℕ) (w : Fin m → Fin n → K) (t : Fin n → K),
    solveVec n m w t = none → ∀ c : Fin m → K, ∑ j, c j • w j ≠ t
  | 0, _, _, _, h, _ => by simp [solveVec] at h
  | n + 1, 0, w, t, h, c => by
    unfold solveVec at h
    split_ifs at h with ht
    simpa [eq_comm] using ht
  | n + 1, m' + 1, w, t, h, c => by
    unfold solveVec at h
    cases hfind : findIdx (m' + 1) (fun j => w j (Fin.last n) != 0) with
    | none =>
      rw [hfind] at h
      simp only [get_tab, tabMat_get] at h
      have hz := findIdx_none hfind
      simp only [bne_eq_false_iff_eq] at hz
      intro hc
      split_ifs at h with ht
      · refine solveVec_none n (m' + 1) _ _ h c ?_
        rw [← headCoords_sum, hc]
      · apply ht
        rw [← hc]
        simp [Finset.sum_apply, hz]
    | some j0 =>
      rw [hfind] at h
      simp only [get_tab, tabMat_get, Option.map_eq_none_iff] at h
      have hpiv : w j0 (Fin.last n) ≠ 0 := by
        simpa using findIdx_some hfind
      intro hc
      refine solveVec_none n m' _ _ h
        (fun j => c (j0.succAbove j)) ?_
      have hlast := congrFun hc (Fin.last n)
      have hhead := congrArg headCoords hc
      rw [headCoords_sum, Fin.sum_univ_succAbove _ j0] at hhead
      rw [Finset.sum_apply, Fin.sum_univ_succAbove _ j0] at hlast
      simp only [Pi.smul_apply, smul_eq_mul] at hlast
      funext i
      have hi := congrFun hhead i
      simp only [headCoords, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.sub_apply,
        Pi.add_apply, mul_sub] at hi ⊢
      rw [Finset.sum_sub_distrib, ← hi]
      have key : t (Fin.last n) / w j0 (Fin.last n) =
          c j0 + ∑ x, c (j0.succAbove x) *
            (w (j0.succAbove x) (Fin.last n) / w j0 (Fin.last n)) := by
        rw [← hlast, add_div, Finset.sum_div, mul_div_cancel_right₀ _ hpiv]
        exact congrArg _ (Finset.sum_congr rfl fun x _ => mul_div_assoc _ _ _)
      rw [key, add_mul, Finset.sum_mul]
      have : ∀ x, c (j0.succAbove x) * (w (j0.succAbove x) (Fin.last n) /
          w j0 (Fin.last n) * w j0 i.castSucc) = c (j0.succAbove x) *
          (w (j0.succAbove x) (Fin.last n) / w j0 (Fin.last n)) * w j0 i.castSucc :=
        fun x => by ring
      simp only [this]
      ring

/-- Linear independence as "only the trivial combination vanishes". -/
def IndepVec {k n : ℕ} (v : Fin k → Fin n → K) : Prop :=
  ∀ γ : Fin k → K, ∑ l, γ l • v l = 0 → γ = 0

omit [DecidableEq K] in
theorem indepVec_zero {n : ℕ} (v : Fin 0 → Fin n → K) : IndepVec v :=
  fun _ _ => funext fun l => l.elim0

omit [DecidableEq K] in
/-- Adding a vector outside the span keeps the family independent. -/
theorem indepVec_snoc {k n : ℕ} {v : Fin k → Fin n → K} (hv : IndepVec v) {u : Fin n → K}
    (hu : ∀ c : Fin k → K, ∑ l, c l • v l ≠ u) :
    IndepVec (Fin.snoc v u : Fin (k + 1) → Fin n → K) := by
  intro γ hγ
  rw [Fin.sum_univ_castSucc] at hγ
  simp only [Fin.snoc_castSucc, Fin.snoc_last] at hγ
  have hlast : γ (Fin.last k) = 0 := by
    by_contra hne
    apply hu (fun l => -(γ (Fin.last k))⁻¹ * γ l.castSucc)
    have : u = -(γ (Fin.last k))⁻¹ • ∑ l, γ l.castSucc • v l := by
      have h2 := eq_neg_of_add_eq_zero_right hγ
      rw [← inv_smul_smul₀ hne u, h2, smul_neg, neg_smul]
    rw [this, Finset.smul_sum]
    exact Finset.sum_congr rfl fun l _ => by rw [smul_smul]
  rw [hlast, zero_smul, add_zero] at hγ
  have hinit := hv _ hγ
  funext l
  rcases Fin.eq_castSucc_or_eq_last l with ⟨l, rfl⟩ | rfl
  · exact congrFun hinit l
  · exact hlast

/-- More than `n` vectors in `K^n` are never independent. -/
theorem not_indepVec_of_lt {k n : ℕ} (hk : n < k) (v : Fin k → Fin n → K) : ¬IndepVec v := by
  intro hv
  obtain ⟨hne, hsum⟩ := kernelVec_spec n k v hk
  exact hne (hv _ hsum)

/-! ### The triangular recursion -/

/-- Columns used by rounds `0, …, k - 1`: round `l` takes `a - l + 1` columns. -/
def roundStart (a : ℕ) : ℕ → ℕ
  | 0 => 0
  | k + 1 => roundStart a k + (a - k + 1)

theorem two_mul_roundStart (a : ℕ) : ∀ k, k ≤ a + 1 →
    2 * roundStart a k + k * k = k * (2 * a + 3)
  | 0, _ => by simp [roundStart]
  | k + 1, hk => by
    have ih := two_mul_roundStart a k (by omega)
    obtain ⟨t, rfl⟩ : ∃ t, a = k + t := ⟨a - k, by omega⟩
    simp only [roundStart, show k + t - k + 1 = t + 1 by omega]
    nlinarith

/-- All rounds together use `(a + 1)(a + 2)/2` columns. -/
theorem roundStart_top (a : ℕ) : roundStart a (a + 1) = (a + 1) * (a + 2) / 2 := by
  have := two_mul_roundStart a (a + 1) le_rfl
  have h2 : (a + 1) * (a + 2) = 2 * roundStart a (a + 1) := by nlinarith
  rw [h2, Nat.mul_div_cancel_left _ (by norm_num)]

theorem roundStart_mono (a : ℕ) {k k' : ℕ} (h : k ≤ k') : roundStart a k ≤ roundStart a k' := by
  induction h with
  | refl => exact le_rfl
  | step _ ih => exact ih.trans (Nat.le_add_right _ _)

/-- The coefficient vector `δ` of a block, spread to all `M` columns. -/
def spread {M : ℕ} (s r : ℕ) (δ : Fin r → K) (i : Fin M) : K :=
  if h : s ≤ i.val ∧ i.val < s + r then δ ⟨i.val - s, by omega⟩ else 0

omit [DecidableEq K] in
theorem spread_eq_zero {M s r : ℕ} {δ : Fin r → K} {i : Fin M}
    (hi : i.val < s ∨ s + r ≤ i.val) : (spread s r δ i : K) = 0 := by
  unfold spread
  split_ifs with h
  · omega
  · rfl

omit [DecidableEq K] in
theorem spread_apply {M s r : ℕ} (δ : Fin r → K) (j : Fin r) (h : s + j.val < M) :
    spread s r δ (⟨s + j.val, h⟩ : Fin M) = δ j := by
  unfold spread
  split_ifs with h
  · congr 1
    ext
    simp
  · exfalso
    exact h ⟨by simp, by simp⟩

omit [DecidableEq K] in
theorem spread_sum {V : Type*} [AddCommMonoid V] {M s r : ℕ} (hsr : s + r ≤ M)
    (δ : Fin r → K) (g : Fin M → K → V) (hg : ∀ i, g i 0 = 0) :
    ∑ i, g i (spread s r δ i) = ∑ j : Fin r, g ⟨s + j.val, by omega⟩ (δ j) := by
  classical
  let e : Fin r → Fin M := fun j => ⟨s + j.val, by omega⟩
  have he : Set.InjOn e ↑(Finset.univ : Finset (Fin r)) := by
    intro j _ j' _ h
    ext
    simpa [e] using congrArg Fin.val h
  rw [← Finset.sum_subset (Finset.subset_univ (Finset.univ.image e)), Finset.sum_image he]
  · exact Finset.sum_congr rfl fun j _ => by rw [spread_apply]
  · intro i _ hi
    rw [spread_eq_zero, hg]
    by_contra hcon
    apply hi
    refine Finset.mem_image.mpr ⟨⟨i.val - s, by omega⟩, Finset.mem_univ _, ?_⟩
    ext
    simp [e]
    omega

section Triangular

open QSearch.ReesSdeTriangular

variable (A B : K → K) {a M : ℕ} (col : Fin M → Fin a → K)

theorem block_lt (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a) (j : Fin (a - k + 1)) :
    roundStart a k + j.val < M := by
  have h1 := roundStart_mono a (show k + 1 ≤ a + 1 by omega)
  have : roundStart a (k + 1) = roundStart a k + (a - k + 1) := rfl
  omega

/-- The `a - k + 1` fresh columns of round `k`. -/
def block (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) : Fin (a - k + 1) → Fin a → K :=
  fun j => col ⟨roundStart a k + j.val, block_lt hM hk j⟩

/-- Scale making the first nonzero entry of `c` on the first `r` indices equal to `1`. -/
def pivotScale {r k : ℕ} (c : Fin (r + k) → K) : K :=
  match findIdx r (fun j => c (Fin.castAdd k j) != 0) with
  | none => 1
  | some j => (c (Fin.castAdd k j))⁻¹

theorem pivotScale_ne_zero {r k : ℕ} (c : Fin (r + k) → K) : pivotScale c ≠ 0 := by
  unfold pivotScale
  cases h : findIdx r (fun j => c (Fin.castAdd k j) != 0) with
  | none => exact one_ne_zero
  | some j =>
    have hcj := findIdx_some h
    simp only [bne_iff_ne, ne_eq] at hcj
    exact inv_ne_zero hcj

/-- If `c` is nonzero somewhere on the first `r` indices, the scaled vector is `1` at
the first such index. -/
theorem pivotScale_pivot {r k : ℕ} (c : Fin (r + k) → K)
    (hc : ∃ j, c (Fin.castAdd k j) ≠ 0) : ∃ j0, pivotScale c * c (Fin.castAdd k j0) = 1 := by
  unfold pivotScale
  cases h : findIdx r (fun j => c (Fin.castAdd k j) != 0) with
  | none =>
    obtain ⟨j, hj⟩ := hc
    have := findIdx_none h j
    simp only [bne_eq_false_iff_eq] at this
    exact absurd this hj
  | some j =>
    have hcj := findIdx_some h
    simp only [bne_iff_ne, ne_eq] at hcj
    exact ⟨j, inv_mul_cancel₀ hcj⟩

/-- Round `k`'s elimination: a dependence among its fresh columns and the basis
`v_1, …, v_k` (`a + 1` vectors in `K^a`), scaled so that its first nonzero entry on the
fresh columns is `1`. -/
def roundCoeff (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) (v : Fin k → Fin a → K) :
    Tab ((a - k + 1) + k) K :=
  let rows := tabMat (Fin.append (block col hM k hk) v)
  let c := (kernelVec a _ (fun j => (rows.get j).get)).get
  let s := pivotScale c
  tab (s • c)

theorem roundCoeff_eq (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a)
    (v : Fin k → Fin a → K) :
    (roundCoeff col hM k hk v).get =
      pivotScale (kernelVec a _ (Fin.append (block col hM k hk) v)).get •
        (kernelVec a _ (Fin.append (block col hM k hk) v)).get := by
  simp [roundCoeff]

/-- `δ` of round `k`, on all `M` columns. -/
def roundDelta (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) (v : Fin k → Fin a → K) :
    Tab M K :=
  let c := (roundCoeff col hM k hk v).get
  tab (spread (roundStart a k) (a - k + 1) (fun j => c (Fin.castAdd k j)))

/-- The basis part of round `k`'s dependence: `e = ∑ δ_i λ_i = -∑ γ_l v_l`. -/
def roundGamma (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) (v : Fin k → Fin a → K) :
    Tab k K :=
  let c := (roundCoeff col hM k hk v).get
  tab fun l => c (Fin.natAdd (a - k + 1) l)

/-- **The triangular solver, round `k`.** `v` is the basis of `U_k` and `R` realizes
`U_k`: `R γ` is a weight vector with value `∑ γ_l v_l`. If the new vector
`v_{k+1} = ∑ β(δ_i) δ_i λ_i` lies in `U_k` (found by `solveVec`), the round stops;
otherwise `U_{k+1} = U_k ⊕ K v_{k+1}` is realized by `R'` (the back substitution step)
and the next round runs. -/
def triRound (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) (v : Fin k → Fin a → K)
    (R : (Fin k → K) → Tab M K) : Tab M K :=
  let δ := (roundDelta col hM k hk v).get
  let γe := (roundGamma col hM k hk v).get
  let u := (tab (roundVec B col δ)).get
  match solveVec a k v u with
  | some η => tab (roundWeight A B δ 1 + (R (tab fun l => A 1 * γe l - η.get l).get).get)
  | none =>
    if hk' : k < a then
      let rows := tabMat (Fin.snoc v u : Fin (k + 1) → Fin a → K)
      triRound hM (k + 1) hk' (fun l => (rows.get l).get)
        (fun γ =>
          let ζ := γ (Fin.last k)
          let Aζ := A ζ
          tab (roundWeight A B δ ζ + (R (tab fun l => γ l.castSucc + ζ * Aζ * γe l).get).get))
    else tab 0
termination_by a - k

/-- **The triangular two-level solver** (Proposition `prop:triangular-sde`, the part
before root extraction). Input: the two contraction functions `A, B : K → K` and the
columns. Output: weights `x`, computed by elimination and back substitution. -/
def triSolve : Tab M K :=
  if hM : (a + 1) * (a + 2) / 2 ≤ M then
    triRound A B col (by rwa [roundStart_top]) 0 (Nat.zero_le a) Fin.elim0 (fun _ => tab 0)
  else tab 0

theorem roundCoeff_spec (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a)
    (v : Fin k → Fin a → K) :
    (roundCoeff col hM k hk v).get ≠ 0 ∧
      ∑ j, (roundCoeff col hM k hk v).get j • Fin.append (block col hM k hk) v j = 0 := by
  obtain ⟨hne, hsum⟩ := kernelVec_spec a _ (Fin.append (block col hM k hk) v) (by omega)
  rw [roundCoeff_eq]
  refine ⟨smul_ne_zero (pivotScale_ne_zero _) hne, ?_⟩
  simp only [Pi.smul_apply, smul_eq_mul, ← smul_smul, ← Finset.smul_sum, hsum,
    smul_zero]

/-- With `v` independent, round `k`'s dependence has the value `1` at some fresh column. -/
theorem roundCoeff_pivot (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a)
    {v : Fin k → Fin a → K} (hv : IndepVec v) :
    ∃ j0, (roundCoeff col hM k hk v).get (Fin.castAdd k j0) = 1 := by
  obtain ⟨hne, hsum⟩ := kernelVec_spec a _ (Fin.append (block col hM k hk) v) (by omega)
  rw [roundCoeff_eq]
  set c := (kernelVec a _ (Fin.append (block col hM k hk) v)).get
  refine pivotScale_pivot c ?_
  by_contra hz
  push Not at hz
  rw [Fin.sum_univ_add] at hsum
  simp only [Fin.append_left, Fin.append_right, hz, zero_smul, Finset.sum_const_zero,
    zero_add] at hsum
  have hg := hv _ hsum
  apply hne
  funext i
  exact Fin.addCases (fun j => hz j) (fun l => congrFun hg l) i

theorem roundDelta_relation (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a)
    (v : Fin k → Fin a → K) :
    ∑ i, (roundDelta col hM k hk v).get i • col i +
      ∑ l, (roundGamma col hM k hk v).get l • v l = 0 := by
  have hsum := (roundCoeff_spec col hM hk v).2
  rw [Fin.sum_univ_add] at hsum
  simp only [Fin.append_left, Fin.append_right] at hsum
  simp only [roundDelta, roundGamma, get_tab]
  rw [← hsum, spread_sum (block_lt hM hk (Fin.last _)) _ (fun i x => x • col i)
    (fun i => zero_smul _ _)]
  rfl

theorem roundDelta_support (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a)
    (v : Fin k → Fin a → K) (i : Fin M)
    (hi : i.val < roundStart a k ∨ roundStart a (k + 1) ≤ i.val) :
    (roundDelta col hM k hk v).get i = 0 := by
  simp only [roundDelta, get_tab]
  exact spread_eq_zero hi

theorem roundDelta_pivot (hM : roundStart a (a + 1) ≤ M) {k : ℕ} (hk : k ≤ a)
    {v : Fin k → Fin a → K} (hv : IndepVec v) :
    ∃ i0 : Fin M, roundStart a k ≤ i0.val ∧ (roundDelta col hM k hk v).get i0 = 1 := by
  obtain ⟨j0, hj0⟩ := roundCoeff_pivot col hM hk hv
  exact ⟨⟨roundStart a k + j0.val, block_lt hM hk j0⟩, by simp, by
    simp only [roundDelta, get_tab]
    rw [spread_apply, hj0]⟩

omit [DecidableEq K] in
theorem roundWeight_eq_zero {δ : Fin M → K} {ζ : K} {i : Fin M} (h : δ i = 0) :
    roundWeight A B δ ζ i = 0 := by
  simp [roundWeight, h]

omit [DecidableEq K] in
/-- Weights with supports on either side of `s` add up inside `D`. -/
theorem add_mem_split {D : Set K} (s : ℕ) {x y : Fin M → K} (hx : ∀ i, x i ∈ D)
    (hxs : ∀ i : Fin M, s ≤ i.val → x i = 0) (hy : ∀ i, y i ∈ D)
    (hys : ∀ i : Fin M, i.val < s → y i = 0) (i : Fin M) : (y + x) i ∈ D := by
  by_cases hi : i.val < s
  · simpa [hys i hi] using hx i
  · simpa [hxs i (by omega)] using hy i

/-- **Correctness of the rounds.** If `v` is independent and `R` realizes `U_k` with
weights in `D` on the columns before round `k`, the solver's output is a nonzero weight
vector in `D^M`, supported on the first `(a + 1)(a + 2)/2` columns, with
`∑ x_i λ_i = 0`. -/
theorem triRound_spec {D : Set K} (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (hM : roundStart a (a + 1) ≤ M) (k : ℕ) (hk : k ≤ a) (v : Fin k → Fin a → K)
    (R : (Fin k → K) → Tab M K) (hv : IndepVec v) (hRD : ∀ γ i, (R γ).get i ∈ D)
    (hRs : ∀ γ (i : Fin M), roundStart a k ≤ i.val → (R γ).get i = 0)
    (hRv : ∀ γ, ∑ i, (R γ).get i • col i = ∑ l, γ l • v l) :
    (triRound A B col hM k hk v R).get ≠ 0 ∧ (∀ i, (triRound A B col hM k hk v R).get i ∈ D) ∧
      (∀ i : Fin M, roundStart a (a + 1) ≤ i.val → (triRound A B col hM k hk v R).get i = 0) ∧
      ∑ i, (triRound A B col hM k hk v R).get i • col i = 0 := by
  rw [triRound]
  simp only [get_tab, tabMat_get]
  set δ := (roundDelta col hM k hk v).get with hδ
  set γe := (roundGamma col hM k hk v).get with hγe
  have hrel := roundDelta_relation col hM hk v
  rw [← hδ, ← hγe] at hrel
  have he : ∑ i, δ i • col i = -∑ l, γe l • v l := eq_neg_of_add_eq_zero_left hrel
  have hδs : ∀ i : Fin M, i.val < roundStart a k ∨ roundStart a (k + 1) ≤ i.val → δ i = 0 :=
    roundDelta_support col hM hk v
  have hstep : roundStart a (k + 1) = roundStart a k + (a - k + 1) := rfl
  have hwD : ∀ ζ i, roundWeight A B δ ζ i ∈ D := by
    intro ζ i
    by_cases hζ : ζ = 0
    · simpa [roundWeight, hζ] using h0
    · exact roundWeight_mem h0 hAB δ hζ i
  have hws : ∀ ζ (i : Fin M), i.val < roundStart a k → roundWeight A B δ ζ i = 0 :=
    fun ζ i hi => roundWeight_eq_zero A B (hδs i (Or.inl hi))
  have hktop : roundStart a (k + 1) ≤ roundStart a (a + 1) := roundStart_mono a (by omega)
  cases hη : solveVec a k v (roundVec B col δ) with
  | some η =>
    -- the stopping round
    simp only [get_tab]
    have hu := solveVec_some a k v _ η hη
    obtain ⟨i0, hi0s, hi0⟩ := roundDelta_pivot col hM hk hv
    rw [← hδ] at hi0
    refine ⟨fun hx => ?_, add_mem_split _ (hRD _) (hRs _) (hwD 1) (hws 1), fun i hi => ?_, ?_⟩
    · have := congrFun hx i0
      simp only [Pi.add_apply, roundWeight, hi0, hRs _ i0 hi0s, Pi.zero_apply, one_mul,
        add_zero] at this
      exact h1 this
    · simp only [Pi.add_apply]
      rw [hRs _ i (by have := roundStart_mono a (show k ≤ a + 1 by omega); omega),
        roundWeight_eq_zero A B (hδs i (Or.inr (by omega))), add_zero]
    · simp only [Pi.add_apply, add_smul, Finset.sum_add_distrib, roundWeight_sum, hRv, he,
        ← hu, sub_smul, Finset.sum_sub_distrib, mul_smul, ← Finset.smul_sum]
      module
  | none =>
    have hu := solveVec_none a k v _ hη
    split_ifs with hk'
    · refine triRound_spec h0 hAB h1 hM (k + 1) hk' _ _ (indepVec_snoc hv hu)
        (fun γ => by simp only [get_tab]; exact add_mem_split _ (hRD _) (hRs _) (hwD _) (hws _))
        (fun γ i hi => ?_) (fun γ => ?_)
      · simp only [get_tab, Pi.add_apply]
        rw [hRs _ i (by omega), roundWeight_eq_zero A B (hδs i (Or.inr hi)), add_zero]
      · rw [Fin.sum_univ_castSucc]
        simp only [get_tab, Fin.snoc_castSucc, Fin.snoc_last, Pi.add_apply, add_smul,
          Finset.sum_add_distrib, roundWeight_sum, hRv, he, mul_smul, ← Finset.smul_sum]
        module
    · exact absurd (indepVec_snoc hv hu) (not_indepVec_of_lt (by omega) _)
termination_by a - k

/-- **Proposition `prop:triangular-sde`, computable weights.** Let `0 ∈ D` and let
`A, B : K → K` be a universal two-level contraction: `ζ δ (A ζ + B δ) ∈ D` for nonzero
`ζ, δ` and `A 1 + B 1 ≠ 0`. From any `M ≥ (a + 1)(a + 2)/2` columns in `K^a`, `triSolve`
returns a nonzero `x ∈ D^M`, supported on the first `(a + 1)(a + 2)/2` columns, with
`∑ x_i λ_i = 0`. -/
theorem triSolve_spec {D : Set K} (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (hM : (a + 1) * (a + 2) / 2 ≤ M) :
    (triSolve A B col).get ≠ 0 ∧ (∀ i, (triSolve A B col).get i ∈ D) ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (triSolve A B col).get i = 0) ∧
      ∑ i, (triSolve A B col).get i • col i = 0 := by
  unfold triSolve
  simp only [hM, ↓reduceDIte]
  obtain ⟨hx1, hx2, hx3, hx4⟩ := triRound_spec A B col h0 hAB h1 (by rwa [roundStart_top]) 0
    (Nat.zero_le a) Fin.elim0 (fun _ => tab 0) (indepVec_zero _) (fun _ _ => by simpa using h0)
    (fun _ _ _ => by simp) (fun _ => by simp)
  exact ⟨hx1, hx2, fun i hi => hx3 i (by rwa [roundStart_top]), hx4⟩

end Triangular

/-! ### Root extraction by search, the coset test, and the Bezout exponent -/

/-- A square root of `y` by search through a list of field elements (`0` if none). -/
def sqrtSearch (elems : List K) (y : K) : K :=
  match elems.find? (fun w => w * w == y) with
  | some w => w
  | none => 0

theorem sqrtSearch_sq {elems : List K} (hel : ∀ x, x ∈ elems) {y : K} (hy : IsSquare y) :
    sqrtSearch elems y ^ 2 = y := by
  unfold sqrtSearch
  cases h : elems.find? (fun w => w * w == y) with
  | some w =>
    have := List.find?_some h
    simpa [sq] using this
  | none =>
    obtain ⟨r, rfl⟩ := hy
    have := List.find?_eq_none.mp h r (hel r)
    simp at this

/-- Coset test at `κ = 2` (Euler's criterion): `0` for a square, `1` otherwise. -/
def cos2 (q : ℕ) (y : K) : ZMod 2 := if y ^ (q / 2) = 1 then 0 else 1

/-- The Bezout exponent `t ≥ 1` with `(x ^ t) ^ d = x ^ gcd(d, N)` on a field with
`N + 1` elements: `t = (d / g)⁻¹ mod (N / g)`, plus `N / g`, with `g = gcd(d, N)`. -/
def bezoutExp (d N : ℕ) : ℕ :=
  ((d / Nat.gcd d N : ℕ) : ZMod (N / Nat.gcd d N))⁻¹.val + N / Nat.gcd d N

omit [DecidableEq K] in
theorem pow_bezoutExp [Fintype K] {d : ℕ} (hd : 0 < d) (x : K) :
    (x ^ bezoutExp d (Fintype.card K - 1)) ^ d = x ^ Nat.gcd d (Fintype.card K - 1) := by
  set N := Fintype.card K - 1 with hN
  have hq : 1 < Fintype.card K := Fintype.one_lt_card
  have hNpos : 0 < N := by omega
  set g := Nat.gcd d N with hgdef
  have hg : 0 < g := Nat.gcd_pos_of_pos_left _ hd
  set d' := d / g
  set N' := N / g
  have hcop : Nat.Coprime d' N' := Nat.coprime_div_gcd_div_gcd hg
  have hdd : d' * g = d := Nat.div_mul_cancel (Nat.gcd_dvd_left d N)
  have hNN : N' * g = N := Nat.div_mul_cancel (Nat.gcd_dvd_right d N)
  have hN'pos : 0 < N' := by
    rcases Nat.eq_zero_or_pos N' with h | h
    · rw [h, zero_mul] at hNN; omega
    · exact h
  have hd'pos : 0 < d' := by
    rcases Nat.eq_zero_or_pos d' with h | h
    · rw [h, zero_mul] at hdd; omega
    · exact h
  have : NeZero N' := ⟨hN'pos.ne'⟩
  set t0 := ((d' : ℕ) : ZMod N')⁻¹.val
  have hinv : ((d' * t0 : ℕ) : ZMod N') = 1 := by
    rw [Nat.cast_mul, ZMod.natCast_zmod_val]
    exact ZMod.coe_mul_inv_eq_one d' hcop
  have hmod : d' * (t0 + N') % N' = 1 % N' := by
    rw [Nat.mul_add, Nat.add_mul_mod_self_right]
    have := (ZMod.natCast_eq_natCast_iff' (d' * t0) 1 N').mp (by rw [hinv, Nat.cast_one])
    exact this
  have hpos : 1 ≤ d' * (t0 + N') := Nat.one_le_iff_ne_zero.mpr (by positivity)
  obtain ⟨n, hn⟩ : N' ∣ d' * (t0 + N') - 1 := (Nat.modEq_iff_dvd' hpos).mp hmod.symm
  have hexp : bezoutExp d N * d = g + N * n := by
    have h1 : d' * (t0 + N') = 1 + N' * n := by omega
    have : bezoutExp d N = t0 + N' := rfl
    rw [this]
    calc (t0 + N') * d = (d' * (t0 + N')) * g := by rw [← hdd]; ring
      _ = (1 + N' * n) * g := by rw [h1]
      _ = g + (N' * g) * n := by ring
      _ = g + N * n := by rw [hNN]
  rw [← pow_mul, hexp]
  by_cases hx : x = 0
  · subst hx
    rw [zero_pow (by omega), zero_pow hg.ne']
  · rw [pow_add, pow_mul, FiniteField.pow_card_sub_one_eq_one x hx, one_pow, mul_one]

/-! ### The linear case `κ = 1` (Theorem `thm:power-sde`(i)) -/

/-- **The linear solver.** One elimination gives `c ≠ 0` with `∑ c_i λ_i = 0`; then
`s_i = c_i ^ t` with the Bezout exponent `t` of `d` modulo `q - 1`. -/
def linSolve (q d : ℕ) {a M : ℕ} (col : Fin M → Fin a → K) : Tab M K :=
  let rows := tabMat col
  let c := (kernelVec a M (fun j => (rows.get j).get)).get
  let t := bezoutExp d (q - 1)
  tab fun i => c i ^ t

/-- **Theorem `thm:power-sde`(i), computable.** Over a finite field with `q` elements,
at an exponent `d ≥ 1` with `gcd(d, q - 1) = 1`, from any `M ≥ a + 1` columns in `K^a`
the solver returns a nonzero `s` with `∑ s_i ^ d λ_i = 0`. -/
theorem linSolve_spec [Fintype K] {q d a M : ℕ} (hq : Fintype.card K = q) (hd : 0 < d)
    (hκ : Nat.gcd d (q - 1) = 1) (hM : a + 1 ≤ M) (col : Fin M → Fin a → K) :
    (linSolve q d col).get ≠ 0 ∧ ∑ i, (linSolve q d col).get i ^ d • col i = 0 := by
  subst hq
  obtain ⟨hne, hsum⟩ := kernelVec_spec a M col (by omega)
  have hpow : ∀ i, (linSolve (Fintype.card K) d col).get i ^ d = (kernelVec a M col).get i := by
    intro i
    simp only [linSolve, get_tab, tabMat_get]
    rw [pow_bezoutExp hd, hκ, pow_one]
  refine ⟨fun h => hne (funext fun i => ?_), by simpa only [hpow] using hsum⟩
  rw [← hpow i, h, Pi.zero_apply, zero_pow hd.ne']

/-! ### The quadratic case `κ = 2` (Proposition `prop:triangular-sde` at `κ = 2`) -/

section Quadratic

open QSearch.ReesSdeTriangular QSearch.ReesSdeQuadratic

variable [Fintype K]

omit [DecidableEq K] [Fintype K] in
/-- From a coset index, the contraction in the coset form gives the hypothesis `hAB`
of `triSolve_spec` (the computation in the proof of
`ReesSdeTriangular.triangular_sde_of_contraction`). -/
theorem contraction_of_index {κ : ℕ} [NeZero κ] {g : K} (ind : K → ZMod κ)
    (hind : ∀ y : K, y ≠ 0 → ∃ w : K, y = g ^ (ind y).val * w ^ κ) (α β : ZMod κ → K)
    (hC : ∀ i j : ZMod κ, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ κ) :
    ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (α (ind ζ) + β (ind δ)) ∈ {y | ∃ w : K, y = w ^ κ} := by
  intro ζ δ hζ hδ
  obtain ⟨w₁, hw₁⟩ := hind ζ hζ
  obtain ⟨w₂, hw₂⟩ := hind δ hδ
  obtain ⟨w, hw⟩ := hC (ind δ) (ind ζ)
  refine ⟨_, coset_product hw₁ hw₂ hw (q := ((ind δ).val + (ind ζ).val) / κ) ?_⟩
  rw [ZMod.val_add, add_comm (ind ζ).val]
  have := Nat.mod_add_div ((ind δ).val + (ind ζ).val) κ
  rw [mul_comm]
  omega

/-- `cos2` is a coset index for any non-residue `g`. -/
theorem cos2_index (hchar : ringChar K ≠ 2) {g : K} (hg : ¬IsSquare g) :
    cos2 (Fintype.card K) (1 : K) = 0 ∧
      ∀ y : K, y ≠ 0 → ∃ w : K, y = g ^ (cos2 (Fintype.card K) y).val * w ^ 2 := by
  have hg0 : g ≠ 0 := fun h => hg (h ▸ IsSquare.zero)
  refine ⟨by simp [cos2], fun y hy => ?_⟩
  unfold cos2
  split_ifs with h
  · obtain ⟨r, hr⟩ := (FiniteField.isSquare_iff hchar hy).mpr h
    exact ⟨r, by simp [hr, sq]⟩
  · have hns : ¬IsSquare y := fun hs => h ((FiniteField.isSquare_iff hchar hy).mp hs)
    obtain ⟨r, hr⟩ := nonsquare_mul_nonsquare hns hg
    refine ⟨r / g, ?_⟩
    have : (1 : ZMod 2).val = 1 := rfl
    rw [this, pow_one, div_pow, sq r, ← hr]
    field_simp

/-- **The quadratic solver.** The triangular solver with `A ζ = α_{cos ζ}`,
`B δ = β_{cos δ}` (coset test by Euler's criterion), then square roots by search. -/
def quadSolve (q : ℕ) (elems : List K) (α β : ZMod 2 → K) {a M : ℕ}
    (col : Fin M → Fin a → K) : Tab M K :=
  let x := (triSolve (fun ζ => α (cos2 q ζ)) (fun δ => β (cos2 q δ)) col).get
  tab fun i => sqrtSearch elems (x i)

/-- **Proposition `prop:triangular-sde` at `κ = 2`, computable.** Let `K` be a finite
field of odd characteristic with `q` elements, listed by `elems`; let `g` be any
quadratic non-residue and `(α, β)` a universal two-level contraction normalised by
`α_0 = 1`, `β_0 = 0`, with `(α_j + β_i) g^(i+j) ∈ P ∪ {0}`, `P` the nonzero squares.
From any `M ≥ (a + 1)(a + 2)/2` columns in `K^a`, `quadSolve` returns a nonzero `s`,
supported on the first `(a + 1)(a + 2)/2` columns, with `∑ s_i ^ 2 λ_i = 0`. -/
theorem quadSolve_spec {q : ℕ} (hq : Fintype.card K = q) (hchar : ringChar K ≠ 2)
    {elems : List K} (hel : ∀ x, x ∈ elems) {g : K} (hg : ¬IsSquare g) (α β : ZMod 2 → K)
    (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod 2, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ 2)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → K) :
    (quadSolve q elems α β col).get ≠ 0 ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (quadSolve q elems α β col).get i = 0) ∧
      ∑ i, (quadSolve q elems α β col).get i ^ 2 • col i = 0 := by
  subst hq
  obtain ⟨hind1, hind⟩ := cos2_index hchar hg
  have h0 : (0 : K) ∈ {y | ∃ w : K, y = w ^ 2} := ⟨0, by simp⟩
  obtain ⟨hx0, hxD, hxs, hxsum⟩ := triSolve_spec (fun ζ => α (cos2 (Fintype.card K) ζ))
    (fun δ => β (cos2 (Fintype.card K) δ)) col h0 (contraction_of_index _ hind α β hC)
    (by simp [hind1, hα0, hβ0]) hM
  have hsq : ∀ i, (quadSolve (Fintype.card K) elems α β col).get i ^ 2 =
      (triSolve (fun ζ => α (cos2 (Fintype.card K) ζ)) (fun δ => β (cos2 (Fintype.card K) δ))
        col).get i := by
    intro i
    obtain ⟨w, hw⟩ := hxD i
    simp only [quadSolve, get_tab]
    exact sqrtSearch_sq hel ⟨w, by rw [hw, sq]⟩
  refine ⟨fun h => hx0 (funext fun i => ?_), fun i hi => ?_, by simpa only [hsq] using hxsum⟩
  · rw [← hsq i, h, Pi.zero_apply, zero_pow two_ne_zero]
  · have := hsq i
    rw [hxs i hi] at this
    exact pow_eq_zero_iff two_ne_zero |>.mp this

/-- **At an exponent `d` with `gcd(d, q - 1) = 2`**: the quadratic solver followed by the
Bezout exponent, `s_i ↦ s_i ^ t`. -/
def quadSolveExp (q d : ℕ) (elems : List K) (α β : ZMod 2 → K) {a M : ℕ}
    (col : Fin M → Fin a → K) : Tab M K :=
  let s := (quadSolve q elems α β col).get
  let t := bezoutExp d (q - 1)
  tab fun i => s i ^ t

theorem quadSolveExp_spec {q d : ℕ} (hq : Fintype.card K = q) (hd : 0 < d)
    (hκ : Nat.gcd d (q - 1) = 2) (hchar : ringChar K ≠ 2) {elems : List K}
    (hel : ∀ x, x ∈ elems) {g : K} (hg : ¬IsSquare g) (α β : ZMod 2 → K)
    (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod 2, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ 2)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → K) :
    (quadSolveExp q d elems α β col).get ≠ 0 ∧
      ∑ i, (quadSolveExp q d elems α β col).get i ^ d • col i = 0 := by
  obtain ⟨hs0, -, hssum⟩ := quadSolve_spec hq hchar hel hg α β hα0 hβ0 hC hM col
  subst hq
  have hpow : ∀ i, (quadSolveExp (Fintype.card K) d elems α β col).get i ^ d =
      (quadSolve (Fintype.card K) elems α β col).get i ^ 2 := by
    intro i
    simp only [quadSolveExp, get_tab]
    rw [pow_bezoutExp hd, hκ]
  refine ⟨fun h => hs0 (funext fun i => ?_), by simpa only [hpow] using hssum⟩
  have := hpow i
  rw [h, Pi.zero_apply, zero_pow hd.ne'] at this
  exact (pow_eq_zero_iff two_ne_zero).mp this.symm

end Quadratic

/-! ### Over `ZMod p`: the contraction computed, no hypothesis left -/

section ZModP

open QSearch.ReesSdeQuadratic

/-- The elements of `ZMod p`, as `0, 1, …, p - 1`. -/
def zmodElems (p : ℕ) : List (ZMod p) := (List.range p).map (fun n : ℕ => (n : ZMod p))

theorem mem_zmodElems {p : ℕ} [NeZero p] (x : ZMod p) : x ∈ zmodElems p := by
  simp only [zmodElems, List.mem_map, List.mem_range]
  exact ⟨x.val, ZMod.val_lt x, ZMod.natCast_zmod_val x⟩

/-- The search for `μ`: the first `y` with `y` a nonzero square and `1 + y` a
non-residue (Euler's criterion). -/
def findMu (p : ℕ) : ZMod p :=
  ((zmodElems p).find? (fun y => y != 0 && y ^ (p / 2) == 1 && 1 + y != 0 &&
    (1 + y) ^ (p / 2) != 1)).getD 0

theorem findMu_spec {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) :
    findMu p ≠ 0 ∧ IsSquare (findMu p) ∧ ¬IsSquare (1 + findMu p) := by
  have hchar : ringChar (ZMod p) ≠ 2 := by rwa [ZMod.ringChar_zmod_n]
  have hcard : Fintype.card (ZMod p) = p := ZMod.card p
  have hsq : ∀ y : ZMod p, y ≠ 0 → (IsSquare y ↔ y ^ (p / 2) = 1) := fun y hy => by
    rw [FiniteField.isSquare_iff hchar hy, hcard]
  set P : ZMod p → Bool := fun y => y != 0 && y ^ (p / 2) == 1 && 1 + y != 0 &&
    (1 + y) ^ (p / 2) != 1
  have hP : ∀ y, P y = true → y ≠ 0 ∧ IsSquare y ∧ ¬IsSquare (1 + y) := by
    intro y hy
    simp only [P, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hy
    obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hy
    exact ⟨h1, (hsq y h1).mpr h2, fun h => h4 ((hsq _ h3).mp h)⟩
  obtain ⟨μ, hμ0, hμ, hν⟩ := exists_consecutive_nonsquare hp2
  have hPμ : P μ = true := by
    have hν0 : 1 + μ ≠ 0 := fun h => hν (h ▸ IsSquare.zero)
    simp only [P, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq]
    exact ⟨⟨⟨hμ0, (hsq μ hμ0).mp hμ⟩, hν0⟩, fun h => hν ((hsq _ hν0).mpr h)⟩
  unfold findMu
  cases h : (zmodElems p).find? P with
  | some y => exact hP y (List.find?_some h)
  | none => exact absurd hPμ (List.find?_eq_none.mp h μ (mem_zmodElems μ))

/-- The contraction of `lem:coherent-quadratic-sde`: `α = (1, 0)`, `β = (0, μ)`, with
the non-residue `g = 1 + μ`. -/
theorem findMu_contraction {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) :
    ∀ i j : ZMod 2, ∃ w : ZMod p,
      (![1, 0] j + ![0, findMu p] i) * (1 + findMu p) ^ (i + j).val = w ^ 2 := by
  obtain ⟨-, ⟨r, hr⟩, -⟩ := findMu_spec hp2
  have key : ∀ i j : Fin 2, ∃ w : ZMod p,
      (![1, 0] j + ![0, findMu p] i) * (1 + findMu p) ^ ((i + j : Fin 2) : ℕ) = w ^ 2 := by
    intro i j
    fin_cases i <;> fin_cases j
    · exact ⟨1, by simp⟩
    · exact ⟨0, by simp⟩
    · exact ⟨1 + findMu p, by simp [sq]⟩
    · exact ⟨r, by simp [hr, sq]⟩
  exact key

/-- **The `κ = 2` solver over `ZMod p`, with the contraction computed.** -/
def quadSolveZMod (p : ℕ) [Fact p.Prime] {a M : ℕ} (col : Fin M → Fin a → ZMod p) :
    Tab M (ZMod p) :=
  quadSolve p (zmodElems p) ![1, 0] ![0, findMu p] col

/-- **Proposition `prop:triangular-sde` at `κ = 2` over `ZMod p`, unconditional and
computable.** For every odd prime `p` and any `M ≥ (a + 1)(a + 2)/2` columns in
`(ZMod p)^a`, `quadSolveZMod` returns a nonzero `s`, supported on the first
`(a + 1)(a + 2)/2` columns, with `∑ s_i ^ 2 λ_i = 0`. -/
theorem quadSolveZMod_spec {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) {a M : ℕ}
    (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → ZMod p) :
    (quadSolveZMod p col).get ≠ 0 ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (quadSolveZMod p col).get i = 0) ∧
      ∑ i, (quadSolveZMod p col).get i ^ 2 • col i = 0 :=
  quadSolve_spec (ZMod.card p) (by rwa [ZMod.ringChar_zmod_n]) mem_zmodElems
    (findMu_spec hp2).2.2 _ _ rfl rfl (findMu_contraction hp2) hM col

/-- The same at every exponent `d` with `gcd(d, p - 1) = 2`. -/
def quadSolveZModExp (p d : ℕ) [Fact p.Prime] {a M : ℕ} (col : Fin M → Fin a → ZMod p) :
    Tab M (ZMod p) :=
  quadSolveExp p d (zmodElems p) ![1, 0] ![0, findMu p] col

theorem quadSolveZModExp_spec {p : ℕ} [Fact p.Prime] {d : ℕ} (hd : 0 < d)
    (hκ : Nat.gcd d (p - 1) = 2) {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M)
    (col : Fin M → Fin a → ZMod p) :
    (quadSolveZModExp p d col).get ≠ 0 ∧
      ∑ i, (quadSolveZModExp p d col).get i ^ d • col i = 0 := by
  have hp2 : p ≠ 2 := by
    rintro rfl
    have := Nat.gcd_dvd_right d (2 - 1)
    rw [hκ] at this
    norm_num at this
  exact quadSolveExp_spec (ZMod.card p) hd hκ (by rwa [ZMod.ringChar_zmod_n]) mem_zmodElems
    (findMu_spec hp2).2.2 _ _ rfl rfl (findMu_contraction hp2) hM col

/-- **Theorem `thm:power-sde`(i) over `ZMod p`, computable**: `gcd(d, p - 1) = 1` and
`M ≥ a + 1` columns. -/
theorem linSolve_zmod_spec {p : ℕ} [Fact p.Prime] {d a M : ℕ} (hd : 0 < d)
    (hκ : Nat.gcd d (p - 1) = 1) (hM : a + 1 ≤ M) (col : Fin M → Fin a → ZMod p) :
    (linSolve p d col).get ≠ 0 ∧ ∑ i, (linSolve p d col).get i ^ d • col i = 0 :=
  linSolve_spec (ZMod.card p) hd hκ hM col

end ZModP

/-! ### Exhaustive search at the Chevalley–Warning arity -/

section Exhaustive

/-- All vectors `Fin M → K` with entries from `elems`. -/
def allVecs (elems : List K) : (M : ℕ) → List (Fin M → K)
  | 0 => [Fin.elim0]
  | M + 1 => elems.flatMap (fun x => (allVecs elems M).map (Fin.cons x))

omit [Field K] [DecidableEq K] in
theorem mem_allVecs {elems : List K} (hel : ∀ x, x ∈ elems) :
    ∀ (M : ℕ) (s : Fin M → K), s ∈ allVecs elems M
  | 0, s => by
    simp only [allVecs, List.mem_singleton]
    exact funext fun i => i.elim0
  | M + 1, s => by
    simp only [allVecs, List.mem_flatMap, List.mem_map]
    exact ⟨s 0, hel _, Fin.tail s, mem_allVecs hel M _, Fin.cons_self_tail s⟩

/-- **Exhaustive search**: the first nonzero `s` (in the order of `allVecs`) with
`∑ s_i ^ d λ_i = 0`, or `0` if there is none. -/
def cwSearch (elems : List K) (d : ℕ) {a M : ℕ} (col : Fin M → Fin a → K) : Tab M K :=
  tab (((allVecs elems M).find?
    (fun s => decide (s ≠ 0) && decide (∑ i, s i ^ d • col i = 0))).getD 0)

/-- If a solution exists, the search returns one. -/
theorem cwSearch_spec {elems : List K} (hel : ∀ x, x ∈ elems) {d a M : ℕ}
    (col : Fin M → Fin a → K) (hex : ∃ s : Fin M → K, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0) :
    (cwSearch elems d col).get ≠ 0 ∧ ∑ i, (cwSearch elems d col).get i ^ d • col i = 0 := by
  unfold cwSearch
  rw [get_tab]
  cases h : (allVecs elems M).find?
      (fun s => decide (s ≠ 0) && decide (∑ i, s i ^ d • col i = 0)) with
  | some s =>
    have := List.find?_some h
    simp only [Bool.and_eq_true, decide_eq_true_eq] at this
    exact this
  | none =>
    obtain ⟨s, hs0, hs⟩ := hex
    have := List.find?_eq_none.mp h s (mem_allVecs hel M s)
    simp [hs0, hs] at this

/-- **Exhaustive search at `κ a + 1` columns (Chevalley–Warning).** Over a finite field
listed by `elems`, for `κ ≥ 1` and `M > κ a`, the search returns a nonzero `s` with
`∑ s_i ^ κ λ_i = 0`. The search visits up to `|K|^M` vectors. -/
theorem cwSearch_witness [Fintype K] {elems : List K} (hel : ∀ x, x ∈ elems) {κ a M : ℕ}
    (hκ : 0 < κ) (hM : κ * a < M) (col : Fin M → Fin a → K) :
    (cwSearch elems κ col).get ≠ 0 ∧ ∑ i, (cwSearch elems κ col).get i ^ κ • col i = 0 :=
  cwSearch_spec hel col (QSearch.ReesSdeWitness.exists_witness hκ hM col)

/-- **Over `ZMod p`, at any exponent `d ≥ 1`**: `gcd(d, p - 1) · a + 1` columns suffice
for the search. -/
theorem cwSearch_zmod_gcd {p : ℕ} [Fact p.Prime] {d a M : ℕ} (hd : 0 < d)
    (hM : Nat.gcd d (p - 1) * a < M) (col : Fin M → Fin a → ZMod p) :
    (cwSearch (zmodElems p) d col).get ≠ 0 ∧
      ∑ i, (cwSearch (zmodElems p) d col).get i ^ d • col i = 0 :=
  cwSearch_spec mem_zmodElems col (QSearch.ReesSdeWitness.exists_witness_gcd hd hM col)

end Exhaustive

end QSearch.ReesSdeSolver

/-! ### Runs

The definitions compile and run. Each `#eval` is checked by `#guard_msgs`; these are
tests of the compiled code, not proofs (the theorems above are the proofs). -/

namespace QSearch.ReesSdeSolver.Runs

open QSearch.ReesSdeSolver

local instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩
local instance : Fact (Nat.Prime 11) := ⟨by norm_num⟩
local instance : Fact (Nat.Prime 1009) := ⟨by norm_num⟩

/-- Six columns in `F_7^2` (`(a + 1)(a + 2)/2 = 6` at `a = 2`). -/
def demoCols7 : Fin 6 → Fin 2 → ZMod 7 := ![![1, 2], ![3, 4], ![5, 6], ![1, 1], ![2, 3], ![4, 0]]

/-- info: 2 -/
#guard_msgs in #eval findMu 7

/-- info: #[3, 3, 3, 1, 1, 0] -/
#guard_msgs in #eval (quadSolveZMod 7 demoCols7).arr

/-- info: [0, 0] -/
#guard_msgs in
#eval let s := (quadSolveZMod 7 demoCols7).get; (List.finRange 2).map (∑ i, s i ^ 2 • demoCols7 i)

/-- Ten columns in `F_11^3`. -/
def demoCols11 : Fin 10 → Fin 3 → ZMod 11 :=
  ![![1, 0, 0], ![0, 1, 0], ![0, 0, 1], ![1, 1, 1], ![2, 5, 7], ![3, 3, 9], ![4, 1, 6],
    ![10, 2, 8], ![5, 5, 5], ![7, 0, 3]]

/-- info: #[4, 4, 4, 1, 0, 0, 0, 0, 1, 0] -/
#guard_msgs in #eval (quadSolveZMod 11 demoCols11).arr

/-- info: [0, 0, 0] -/
#guard_msgs in
#eval let s := (quadSolveZMod 11 demoCols11).get
  (List.finRange 3).map (∑ i, s i ^ 2 • demoCols11 i)

/-- info: [0, 0, 0] -/
#guard_msgs in -- exponent `d = 4`, `gcd(4, 10) = 2`
#eval let s := (quadSolveZModExp 11 4 demoCols11).get
  (List.finRange 3).map (∑ i, s i ^ 4 • demoCols11 i)

/-- Four columns in `F_11^3`, for the linear case. -/
def demoCols11' : Fin 4 → Fin 3 → ZMod 11 := fun i => demoCols11 (Fin.castLE (by omega) i)

/-- info: #[10, 10, 10, 1] -/
#guard_msgs in -- `d = 3`, `gcd(3, 10) = 1`
#eval (linSolve 11 3 demoCols11').arr

/-- info: [0, 0, 0] -/
#guard_msgs in
#eval let s := (linSolve 11 3 demoCols11').get; (List.finRange 3).map (∑ i, s i ^ 3 • demoCols11' i)

/-- info: #[0, 1, 2, 1, 3] -/
#guard_msgs in -- exhaustive search at `κ a + 1 = 5` columns, `κ = 2`, `a = 2`, over `F_7`
#eval (cwSearch (zmodElems 7) 2 (fun i : Fin 5 => demoCols7 (Fin.castLE (by omega) i))).arr

/-- Pseudo-random numbers (a linear congruential generator). -/
def lcgTable : Array ℕ := ((List.range 400).foldl (fun (p : Array ℕ × ℕ) _ =>
  let x := (1103515245 * p.2 + 12345) % 2147483648; (p.1.push (x / 65536), x)) (#[], 42)).1

/-- 45 pseudo-random columns in `F_1009^8` (`(a + 1)(a + 2)/2 = 45` at `a = 8`). -/
def randCols1009 : Fin 45 → Fin 8 → ZMod 1009 := fun i j => (lcgTable[i.val * 8 + j.val]! : ℕ)

/-- info: ([0, 0, 0, 0, 0, 0, 0, 0], 33) -/
#guard_msgs in -- the residual `∑ s_i^2 λ_i` and the number of nonzero `s_i`
#eval let s := (quadSolveZMod 1009 randCols1009).get
  ((List.finRange 8).map (∑ i, s i ^ 2 • randCols1009 i),
    ((List.finRange 45).filter (fun i => s i != 0)).length)

end QSearch.ReesSdeSolver.Runs

/-! ### Axioms

The definitions are compiled by Lean's code generator (none is `noncomputable`) and run
above. `#print axioms` nevertheless lists `Classical.choice` for them: it enters through
proof fields of Mathlib's `Fin.fintype` instance, which every `∑` over `Fin n` uses;
`finSumProbe`, a one-line sum, shows the same list. -/

/-- `∑ j : Fin n, j` alone already depends on `Classical.choice` (via `Fin.fintype`). -/
def QSearch.ReesSdeSolver.finSumProbe (n : ℕ) : ℕ := ∑ j : Fin n, j.val

/-- info: 'QSearch.ReesSdeSolver.finSumProbe' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.finSumProbe

/-- info: 'QSearch.ReesSdeSolver.kernelVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec

/-- info: 'QSearch.ReesSdeSolver.solveVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec

/-- info: 'QSearch.ReesSdeSolver.triSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod

/-- info: 'QSearch.ReesSdeSolver.linSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve

/-- info: 'QSearch.ReesSdeSolver.cwSearch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch

/-- info: 'QSearch.ReesSdeSolver.kernelVec_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec_spec

/-- info: 'QSearch.ReesSdeSolver.solveVec_some' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_some

/-- info: 'QSearch.ReesSdeSolver.solveVec_none' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_none

/-- info: 'QSearch.ReesSdeSolver.triRound_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triRound_spec

/-- info: 'QSearch.ReesSdeSolver.triSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve_spec

/-- info: 'QSearch.ReesSdeSolver.pow_bezoutExp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.pow_bezoutExp

/-- info: 'QSearch.ReesSdeSolver.linSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_spec

/-- info: 'QSearch.ReesSdeSolver.linSolve_zmod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_zmod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolve_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveExp_spec

/-- info: 'QSearch.ReesSdeSolver.findMu_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.findMu_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveZModExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZModExp_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_witness

/-- info: 'QSearch.ReesSdeSolver.cwSearch_zmod_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_zmod_gcd
