import Formal.Schedule1HPlus.Classes
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

/-!
# Schedule 1H⁺, part 2: class-restricted nodes, refinement contractions, Lemma
`lem:plus-refine` and Corollary `cor:plus-chain`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus`: Definition
`def:plus-node`, the paragraph after it, Definition `def:plus-rc`, Lemma
`lem:plus-refine` and Corollary `cor:plus-chain`.

Encoding.

* Columns live in an arbitrary finite-dimensional `K`-space `V` (the paper: `F_p^a`, so
  `a = finrank K V`).
* `IsRel C D Ω col w` is the paper's `Ω`-relation at modulus `D`: `∑ w_b λ_b = 0`, every
  nonzero `w_b` has `cl_D(w_b) ∈ Ω`, and some `w_{b*} = 1` (the designated index; it can
  be read off `w`, so only its existence is recorded).
* `IsNode C D Ω ι nd`: the algorithm `nd` returns an `Ω`-relation on every family of
  columns indexed by `ι` (the paper's node of arity `N(a) = |ι|`).
* `IsRC C D Δ Ω α β` is Definition `def:plus-rc` (`β` is given on all of `ℤ_D`; only its
  values on `Δ` matter).
* `depOf` is a nonzero linear dependence (chosen; the paper uses Gaussian elimination)
  and `normalize` scales a nonzero vector so that one entry is `1`.
* `refine` is the construction of Lemma `lem:plus-refine` on `n` blocks of the inner
  node (`β × ι`, block `ν` is `{ν} × ι`); `refine_spec` is the lemma.
* `chainRun` / `chain_spec` / `card_chainIdx` / `card_chainIdx_le` are Corollary
  `cor:plus-chain` (correctness, the exact arity, and the degree/constant bound).
* `gauss_spec`: Gaussian elimination, scaled, is a `ℤ_D`-node at every modulus
  (`D = 1` included).
* `rel_of_rootSol`: a `D`-solver output, scaled, is a `{0}`-relation at modulus `D` and
  a `lift_κ {0}`-relation (= `Dℤ_κ`, `mem_lift_zero_iff`) at modulus `κ`.
* `rootSol_of_rel`: a `{0}`-relation at modulus `κ` followed by `κ`-th roots is a
  `κ`-solution.

Time, determinism and the operation counts are not formalized.
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset Module

variable {K : Type*} [Field K] {N : ℕ} (C : ClassMap K N)

section Defs

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- **Definition `def:plus-node`**: an `Ω`-relation at modulus `D`. -/
def IsRel (D : ℕ) (Ω : Set (ZMod D)) {ι : Type*} [Fintype ι] (col : ι → V) (w : ι → K) :
    Prop :=
  (∃ b, w b = 1) ∧ (∀ b, w b ≠ 0 → C.cl D (w b) ∈ Ω) ∧ ∑ b, w b • col b = 0

/-- **Definition `def:plus-node`**: an `Ω`-node at modulus `D` on columns indexed by `ι`. -/
def IsNode (D : ℕ) (Ω : Set (ZMod D)) (ι : Type*) [Fintype ι] (nd : (ι → V) → ι → K) :
    Prop :=
  ∀ col, IsRel C D Ω col (nd col)

/-- **Definition `def:plus-rc`**: an `RC(D; Δ → Ω)` contraction `(α, β)`. -/
structure IsRC (D : ℕ) (Δ Ω : Set (ZMod D)) (α β : ZMod D → K) : Prop where
  base : α 0 + β 0 ∈ Pow D
  cond : ∀ i ∈ Δ, ∀ j : ZMod D, α j + β i = 0 ∨ C.cl D (α j + β i) + i + j ∈ Ω

end Defs

section Dep

variable {β W : Type*} [Fintype β] [AddCommGroup W] [Module K W]

open Classical in
/-- A nonzero linear dependence among `vs` (`0` if there is none). -/
noncomputable def depOf (vs : β → W) : β → K :=
  if h : ∃ θ : β → K, θ ≠ 0 ∧ ∑ ν, θ ν • vs ν = 0 then h.choose else 0

theorem depOf_spec [FiniteDimensional K W] (vs : β → W) (hcard : finrank K W < Fintype.card β) :
    depOf (K := K) vs ≠ 0 ∧ ∑ ν, depOf (K := K) vs ν • vs ν = 0 := by
  classical
  have hex : ∃ θ : β → K, θ ≠ 0 ∧ ∑ ν, θ ν • vs ν = 0 := by
    have hli : ¬ LinearIndependent K vs := fun h =>
      absurd h.fintype_card_le_finrank (not_le.mpr hcard)
    obtain ⟨g, hg, i, hi⟩ := Fintype.not_linearIndependent_iff.mp hli
    exact ⟨g, fun h => hi (by simp [h]), hg⟩
  unfold depOf
  rw [dite_eq_left hex]
  exact hex.choose_spec

open Classical in
/-- Scale a vector by the inverse of one of its nonzero entries. -/
noncomputable def normalize (θ : β → K) : β → K :=
  if h : ∃ ν, θ ν ≠ 0 then (θ h.choose)⁻¹ • θ else θ

theorem normalize_spec (θ : β → K) (hθ : θ ≠ 0) :
    ∃ ν, θ ν ≠ 0 ∧ normalize θ = (θ ν)⁻¹ • θ := by
  classical
  have h : ∃ ν, θ ν ≠ 0 := by
    by_contra h; push Not at h; exact hθ (funext h)
  refine ⟨h.choose, h.choose_spec, ?_⟩
  unfold normalize
  rw [dite_eq_left h]

theorem normalize_one (θ : β → K) (hθ : θ ≠ 0) : ∃ ν, normalize θ ν = 1 := by
  obtain ⟨ν, hν, h⟩ := normalize_spec θ hθ
  exact ⟨ν, by rw [h]; simp [inv_mul_cancel₀ hν]⟩

theorem normalize_rel (vs : β → W) (θ : β → K) (hθ : θ ≠ 0)
    (h : ∑ ν, θ ν • vs ν = 0) : ∑ ν, normalize θ ν • vs ν = 0 := by
  obtain ⟨ν, _, he⟩ := normalize_spec θ hθ
  rw [he]
  simp only [Pi.smul_apply, smul_eq_mul, mul_smul, ← Finset.smul_sum, h, smul_zero]

end Dep

variable [DecidableEq K]

section Gauss

variable {V : Type*} [AddCommGroup V] [Module K V] {ι : Type*} [Fintype ι]

/-- Gaussian elimination, scaled so that one coefficient is `1`. -/
noncomputable def gauss (col : ι → V) : ι → K := normalize (depOf (K := K) col)

/-- **Gaussian elimination is a `ℤ_D`-node** of arity `a + 1` (any `D`; the paper: a
`ℤ_1`-node at modulus `1` and a `ℤ_κ`-node at modulus `κ`). -/
theorem gauss_spec [FiniteDimensional K V] (D : ℕ) (hcard : finrank K V < Fintype.card ι) :
    IsNode C D Set.univ ι (gauss (K := K) (V := V)) := by
  intro col
  obtain ⟨h0, hrel⟩ := depOf_spec col hcard
  exact ⟨normalize_one _ h0, fun _ _ => Set.mem_univ _, normalize_rel col _ h0 hrel⟩

end Gauss

section Refine

variable {V : Type*} [AddCommGroup V] [Module K V] {ι β : Type*} [Fintype ι] [Fintype β]

/-- The paper's `U^ν_i = ∑ c_b λ_b` over the `b` with `c_b ≠ 0`, `cl_D(c_b) = i`. -/
def Uvec (D : ℕ) (col : ι → V) (c : ι → K) (i : ZMod D) : V :=
  ∑ b, if c b ≠ 0 ∧ C.cl D (c b) = i then c b • col b else 0

/-- Regrouping `∑_b f(cl(c_b)) c_b λ_b` by classes. -/
theorem sum_Uvec (D : ℕ) (Δ : Finset (ZMod D)) (col : ι → V) (c : ι → K)
    (hc : ∀ b, c b ≠ 0 → C.cl D (c b) ∈ Δ) (f : ZMod D → K) :
    ∑ i ∈ Δ, f i • Uvec C D col c i = ∑ b, f (C.cl D (c b)) • c b • col b := by
  simp only [Uvec, Finset.smul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun b _ => ?_
  by_cases hb : c b = 0
  · simp [hb]
  · rw [Finset.sum_eq_single (C.cl D (c b))]
    · simp [hb]
    · intro i _ hi
      have : ¬ C.cl D (c b) = i := fun h => hi h.symm
      simp [this]
    · intro h; exact absurd (hc b hb) h

/-- **The construction of Lemma `lem:plus-refine`.** Block `ν` of the columns is
`{ν} × ι`; `c ν` is the inner node's relation on it; `η` is a normalized dependence of
the vectors `(U^ν_i)_{i ∈ Δ \ {0}}`; the output is
`w_b = (α_0 + β_0)⁻¹ η_ν (α_{cl η_ν} + β_{cl c_b}) c_b`. -/
noncomputable def refine (D : ℕ) (Δ : Finset (ZMod D)) (α β' : ZMod D → K)
    (nd : (ι → V) → ι → K) (col : β × ι → V) : β × ι → K :=
  let c : β → ι → K := fun ν => nd (fun b => col (ν, b))
  let U : β → ((Δ.erase 0) → V) := fun ν i => Uvec C D (fun b => col (ν, b)) (c ν) i
  let η := normalize (depOf (K := K) U)
  fun p => (α 0 + β' 0)⁻¹ * (η p.1 * (α (C.cl D (η p.1)) + β' (C.cl D (c p.1 p.2))) * c p.1 p.2)

omit [Fintype ι] in
theorem finrank_blocks [FiniteDimensional K V] (D : ℕ) (Δ : Finset (ZMod D))
    (h0 : (0 : ZMod D) ∈ Δ) :
    finrank K ((Δ.erase 0) → V) = (Δ.card - 1) * finrank K V := by
  rw [Module.finrank_pi_fintype, Finset.sum_const, Finset.card_univ, Fintype.card_coe,
    Finset.card_erase_of_mem h0, smul_eq_mul]

/-- **Lemma `lem:plus-refine` (refinement step).** Let `D' ∣ D ∣ N`, let `nd` be an
`Ω'`-node at modulus `D'` on the block index type `ι`, let `(α, β)` be an
`RC(D; Δ → Ω)` contraction with `Δ ⊇ lift_D(Ω')`, and let there be more than
`(|Δ| - 1) a` blocks (`a = finrank V`; the paper takes exactly `(|Δ|-1)a + 1`). Then the
refined output is an `Ω`-relation at modulus `D` on all `|β| · |ι|` columns. -/
theorem refine_spec [FiniteDimensional K V] {D' D : ℕ} (hD'D : D' ∣ D) (hDN : D ∣ N)
    {Ω' : Set (ZMod D')} {Δ : Finset (ZMod D)} {Ω : Set (ZMod D)}
    (hΔ : ClassMap.lift D Ω' ⊆ (↑Δ : Set (ZMod D)))
    {α β' : ZMod D → K} (hrc : IsRC C D ↑Δ Ω α β')
    {nd : (ι → V) → ι → K} (hnd : IsNode C D' Ω' ι nd)
    (hn : (Δ.card - 1) * finrank K V < Fintype.card β) (col : β × ι → V) :
    IsRel C D Ω col (refine C D Δ α β' nd col) := by
  have hD'N : D' ∣ N := hD'D.trans hDN
  set c : β → ι → K := fun ν => nd (fun b => col (ν, b)) with hcdef
  set Ui : β → ZMod D → V := fun ν i => Uvec C D (fun b => col (ν, b)) (c ν) i with hUi
  set U : β → ((Δ.erase 0) → V) := fun ν i => Ui ν i with hU
  set η := normalize (depOf (K := K) U) with hηdef
  set s := α 0 + β' 0 with hs
  have hs0 : s ≠ 0 := hrc.base.1
  -- `0 ∈ Ω'` (the inner designated coefficient `1` has class `0`), so `0 ∈ Δ`
  have h0Ω' : (0 : ZMod D') ∈ Ω' := by
    obtain ⟨⟨b, hb⟩, hcl, _⟩ := hnd (fun _ => 0)
    have := hcl b (by rw [hb]; exact one_ne_zero)
    rwa [hb, C.cl_one hD'N] at this
  have h0Δ : (0 : ZMod D) ∈ Δ := hΔ (by simp [ClassMap.lift, h0Ω'])
  have hc : ∀ ν b, c ν b ≠ 0 → C.cl D (c ν b) ∈ Δ := by
    intro ν b hb
    have h1 := (hnd (fun b => col (ν, b))).2.1 b hb
    exact hΔ ((C.mem_lift_iff hD'D hDN Ω' hb).mpr h1)
  have hrelc : ∀ ν, ∑ b, c ν b • col (ν, b) = 0 := fun ν => (hnd _).2.2
  -- the dependence
  have hfr : finrank K ((Δ.erase 0) → V) < Fintype.card β := by
    rw [finrank_blocks D Δ h0Δ]; exact hn
  obtain ⟨hθ0, hθ⟩ := depOf_spec U hfr
  have hηrel : ∑ ν, η ν • U ν = 0 := normalize_rel U _ hθ0 hθ
  have hηi : ∀ i ∈ Δ, ∑ ν, η ν • Ui ν i = 0 := by
    intro i hi
    by_cases hi0 : i = 0
    · subst hi0
      have hsplit : ∀ ν, Ui ν 0 = -∑ j ∈ Δ.erase 0, Ui ν j := by
        intro ν
        have h1 := sum_Uvec C D Δ (fun b => col (ν, b)) (c ν) (hc ν) (fun _ => 1)
        simp only [one_smul] at h1
        rw [hrelc ν, ← Finset.add_sum_erase Δ _ h0Δ] at h1
        exact eq_neg_of_add_eq_zero_left h1
      simp_rw [hsplit, smul_neg, Finset.sum_neg_distrib, Finset.smul_sum]
      rw [Finset.sum_comm, neg_eq_zero]
      refine Finset.sum_eq_zero fun j hj => ?_
      have := congrFun hηrel ⟨j, hj⟩
      simpa [Finset.sum_apply, U] using this
    · have := congrFun hηrel ⟨i, Finset.mem_erase.mpr ⟨hi0, hi⟩⟩
      simpa [Finset.sum_apply, U] using this
  refine ⟨?_, ?_, ?_⟩
  · -- designated index
    obtain ⟨ν, hν⟩ : ∃ ν, η ν = 1 := normalize_one _ hθ0
    obtain ⟨b, hb⟩ := (hnd (fun b => col (ν, b))).1
    refine ⟨(ν, b), ?_⟩
    show s⁻¹ * (η ν * (α (C.cl D (η ν)) + β' (C.cl D (c ν b))) * c ν b) = 1
    rw [hν, show c ν b = 1 from hb, C.cl_one hDN]
    simp only [one_mul, mul_one]; exact inv_mul_cancel₀ hs0
  · -- classes
    rintro ⟨ν, b⟩ hw
    change s⁻¹ * (η ν * (α (C.cl D (η ν)) + β' (C.cl D (c ν b))) * c ν b) ≠ 0 at hw
    change C.cl D (s⁻¹ * (η ν * (α (C.cl D (η ν)) + β' (C.cl D (c ν b))) * c ν b)) ∈ Ω
    have hη : η ν ≠ 0 := fun h => hw (by simp [h])
    have hcb : c ν b ≠ 0 := fun h => hw (by simp [h])
    have hA : α (C.cl D (η ν)) + β' (C.cl D (c ν b)) ≠ 0 := fun h => hw (by simp [h])
    rcases hrc.cond _ (hc ν b hcb) (C.cl D (η ν)) with h | h
    · exact absurd h hA
    · rw [C.cl_mul hDN (inv_ne_zero hs0) (mul_ne_zero (mul_ne_zero hη hA) hcb),
        C.cl_inv hDN hs0, C.cl_of_mem_pow hDN hrc.base, C.cl_mul hDN (mul_ne_zero hη hA) hcb,
        C.cl_mul hDN hη hA]
      convert h using 1
      ring
  · -- the relation
    have hblock : ∀ ν, ∑ b, (s⁻¹ * (η ν * (α (C.cl D (η ν)) + β' (C.cl D (c ν b))) * c ν b)) •
        col (ν, b) = s⁻¹ • (η ν • ∑ i ∈ Δ, β' i • Ui ν i) := by
      intro ν
      rw [sum_Uvec C D Δ (fun b => col (ν, b)) (c ν) (hc ν) β']
      have e1 : ∀ b, (s⁻¹ * (η ν * (α (C.cl D (η ν)) + β' (C.cl D (c ν b))) * c ν b)) •
          col (ν, b) = (s⁻¹ * η ν * α (C.cl D (η ν))) • (c ν b • col (ν, b)) +
            s⁻¹ • (η ν • (β' (C.cl D (c ν b)) • c ν b • col (ν, b))) := by
        intro b
        simp only [smul_smul, ← add_smul]
        congr 1; ring
      simp_rw [e1, Finset.sum_add_distrib, ← Finset.smul_sum, hrelc ν, smul_zero, zero_add]
    show ∑ p : β × ι, (s⁻¹ * (η p.1 * (α (C.cl D (η p.1)) + β' (C.cl D (c p.1 p.2))) *
      c p.1 p.2)) • col p = 0
    rw [Fintype.sum_prod_type]
    simp_rw [hblock, ← Finset.smul_sum, Finset.smul_sum (s := Δ)]
    rw [Finset.sum_comm]
    have : ∀ i ∈ Δ, ∑ ν, η ν • β' i • Ui ν i = 0 := by
      intro i hi
      simp_rw [smul_comm (η _) (β' i), ← Finset.smul_sum, hηi i hi, smul_zero]
    rw [Finset.sum_eq_zero this, smul_zero]

end Refine

section Chain

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- A refinement step `σ = (D, Δ, Ω)` with its contraction `(α, β)`. -/
structure Step (K : Type*) where
  D : ℕ
  Δ : Finset (ZMod D)
  Ω : Set (ZMod D)
  α : ZMod D → K
  β : ZMod D → K

/-- Column index type of a chain; the list is `[σ_L, …, σ_1]` (last step first). Step `σ`
uses `(|Δ| - 1) a + 1` blocks. -/
def chainIdx (a : ℕ) (ι : Type) : List (Step K) → Type
  | [] => ι
  | σ :: l => Fin ((σ.Δ.card - 1) * a + 1) × chainIdx a ι l

instance instFintypeChainIdx (a : ℕ) (ι : Type) [Fintype ι] :
    (l : List (Step K)) → Fintype (chainIdx a ι l)
  | [] => inferInstanceAs (Fintype ι)
  | σ :: l => letI := instFintypeChainIdx a ι l
      inferInstanceAs (Fintype (Fin ((σ.Δ.card - 1) * a + 1) × chainIdx a ι l))

/-- **The chain** `(N_0; σ_1, …, σ_L)`: `L` refinements of the base node `nd0`. -/
noncomputable def chainRun (a : ℕ) {ι : Type} [Fintype ι] (nd0 : (ι → V) → ι → K) :
    (l : List (Step K)) → (chainIdx a ι l → V) → chainIdx a ι l → K
  | [] => nd0
  | σ :: l => refine C σ.D σ.Δ σ.α σ.β (chainRun a nd0 l)

/-- Modulus at the top of the chain. -/
def topD (D0 : ℕ) : List (Step K) → ℕ
  | [] => D0
  | σ :: _ => σ.D

/-- Class set at the top of the chain. -/
def topΩ (D0 : ℕ) (Ω0 : Set (ZMod D0)) : (l : List (Step K)) → Set (ZMod (topD D0 l))
  | [] => Ω0
  | σ :: _ => σ.Ω

/-- The chain's hypotheses: `D_{t-1} ∣ D_t ∣ N`, `Δ_t ⊇ lift_{D_t}(Ω_{t-1})` (the paper
has equality), and a contraction for every step. -/
def ChainOK (D0 : ℕ) (Ω0 : Set (ZMod D0)) : List (Step K) → Prop
  | [] => D0 ∣ N
  | σ :: l => ChainOK D0 Ω0 l ∧ topD D0 l ∣ σ.D ∧ σ.D ∣ N ∧
      ClassMap.lift σ.D (topΩ D0 Ω0 l) ⊆ (↑σ.Δ : Set (ZMod σ.D)) ∧
      IsRC C σ.D ↑σ.Δ σ.Ω σ.α σ.β

/-- **Corollary `cor:plus-chain` (correctness).** `L` applications of Lemma
`lem:plus-refine` to an `Ω_0`-node at modulus `D_0` give an `Ω_L`-node at modulus
`D_L`. -/
theorem chain_spec [FiniteDimensional K V] {D0 : ℕ} {Ω0 : Set (ZMod D0)} {ι : Type}
    [Fintype ι] {nd0 : (ι → V) → ι → K} (h0 : IsNode C D0 Ω0 ι nd0) :
    ∀ l : List (Step K), ChainOK C D0 Ω0 l →
      IsNode C (topD D0 l) (topΩ D0 Ω0 l) (chainIdx (finrank K V) ι l)
        (chainRun C (finrank K V) nd0 l)
  | [], _ => h0
  | σ :: l, ⟨hl, hdvd, hDN, hΔ, hrc⟩ => by
    intro col
    exact refine_spec C hdvd hDN hΔ hrc (chain_spec h0 l hl) (by simp) col

/-- **Corollary `cor:plus-chain` (arity)**: `|ι| · ∏_t ((|Δ_t| - 1) a + 1)`. -/
theorem card_chainIdx (a : ℕ) (ι : Type) [Fintype ι] :
    ∀ l : List (Step K), Fintype.card (chainIdx a ι l) =
      Fintype.card ι * (l.map fun σ => (σ.Δ.card - 1) * a + 1).prod
  | [] => by rw [List.map_nil, List.prod_nil, mul_one]; rfl
  | σ :: l => by
    show Fintype.card (Fin ((σ.Δ.card - 1) * a + 1) × chainIdx a ι l) = _
    rw [Fintype.card_prod, Fintype.card_fin, card_chainIdx a ι l, List.map_cons,
      List.prod_cons]
    ring

/-- **Corollary `cor:plus-chain` (degree and constant).** If `|ι| ≤ K_0 (a+1)^{e_0}` and
every `|Δ_t| ≥ 2`, the chain has arity at most
`K_0 ∏_t (|Δ_t| - 1) · (a+1)^{e_0 + L}`. -/
theorem card_chainIdx_le (a : ℕ) (ι : Type) [Fintype ι] {K0 e0 : ℕ}
    (hι : Fintype.card ι ≤ K0 * (a + 1) ^ e0) :
    ∀ l : List (Step K), (∀ σ ∈ l, 2 ≤ σ.Δ.card) →
      Fintype.card (chainIdx a ι l) ≤
        (K0 * (l.map fun σ => σ.Δ.card - 1).prod) * (a + 1) ^ (e0 + l.length)
  | [], _ => by
    rw [List.map_nil, List.prod_nil, mul_one, List.length_nil, add_zero]
    exact hι
  | σ :: l, h => by
    show Fintype.card (Fin ((σ.Δ.card - 1) * a + 1) × chainIdx a ι l) ≤ _
    rw [Fintype.card_prod, Fintype.card_fin]
    have ih := card_chainIdx_le a ι hι l (fun τ hτ => h τ (List.mem_cons_of_mem _ hτ))
    have h2 : 2 ≤ σ.Δ.card := h σ List.mem_cons_self
    have hstep : (σ.Δ.card - 1) * a + 1 ≤ (σ.Δ.card - 1) * (a + 1) := by
      have : 1 ≤ σ.Δ.card - 1 := by omega
      nlinarith
    calc ((σ.Δ.card - 1) * a + 1) * Fintype.card (chainIdx a ι l)
        ≤ ((σ.Δ.card - 1) * (a + 1)) *
            ((K0 * (l.map fun σ => σ.Δ.card - 1).prod) * (a + 1) ^ (e0 + l.length)) :=
          Nat.mul_le_mul hstep ih
      _ = (K0 * ((σ :: l).map fun σ => σ.Δ.card - 1).prod) *
            (a + 1) ^ (e0 + (σ :: l).length) := by
          simp only [List.map_cons, List.prod_cons, List.length_cons]
          rw [show e0 + (l.length + 1) = (e0 + l.length) + 1 by ring, pow_succ]
          ring

end Chain

section Roots

variable {V : Type*} [AddCommGroup V] [Module K V] {ι : Type*} [Fintype ι]

/-- Roots of the weights of a relation (`0` stays `0`). -/
def rootsOf (rt : K → K) (w : ι → K) : ι → K := fun b => if w b = 0 then 0 else rt (w b)

/-- **A `{0}`-relation at modulus `κ` followed by `κ`-th roots is a `κ`-solution**
(Definition `def:plus-node` remark; Corollary `cor:plus-chain`, last sentence;
Lemma `lem:plus-ell-node`, last sentence). -/
theorem rootSol_of_rel {κ : ℕ} (hκ : κ ∣ N) (rt : K → K) (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x)
    {col : ι → V} {w : ι → K} (h : IsRel C κ {0} col w) :
    IsRootSol κ col (rootsOf rt w) := by
  have hκ0 : 0 < κ := C.pos_of_dvd hκ
  have hpow : ∀ b, rootsOf rt w b ^ κ = w b := by
    intro b
    unfold rootsOf
    split_ifs with hb
    · rw [hb, zero_pow hκ0.ne']
    · exact hrt _ ((C.cl_eq_zero_iff hκ hb).mp (h.2.1 b hb))
  refine ⟨fun h0 => ?_, ?_⟩
  · obtain ⟨b, hb⟩ := h.1
    have := hpow b
    rw [h0, Pi.zero_apply, zero_pow hκ0.ne', hb] at this
    exact zero_ne_one this
  · simp_rw [hpow]; exact h.2.2

/-- **A `D`-solver output, scaled, is a `{0}`-relation at modulus `D`** (paragraph after
Definition `def:plus-node`). -/
theorem rel_of_rootSol {D : ℕ} (hD : D ∣ N) {col : ι → V} {r : ι → K}
    (h : IsRootSol D col r) : IsRel C D {0} col (normalize fun b => r b ^ D) := by
  have hD0 : 0 < D := C.pos_of_dvd hD
  have hne : (fun b => r b ^ D) ≠ 0 := by
    intro h0; apply h.1; funext b
    have := congrFun h0 b
    simpa [pow_eq_zero_iff hD0.ne'] using this
  obtain ⟨ν, hν, he⟩ := normalize_spec _ hne
  refine ⟨normalize_one _ hne, fun b hb => ?_, normalize_rel col _ hne h.2⟩
  rw [he] at hb ⊢
  simp only [Pi.smul_apply, smul_eq_mul] at hb ⊢
  have hrb : r b ^ D ≠ 0 := fun h0 => hb (by simp [h0])
  rw [C.cl_mul hD (inv_ne_zero hν) hrb, C.cl_inv hD hν,
    C.cl_of_mem_pow hD ⟨hν, r ν, rfl⟩, C.cl_of_mem_pow hD ⟨hrb, r b, rfl⟩]
  simp

/-- The class mod `κ` of an element of `P_D` (`D ∣ κ ∣ N`) lies in `lift_κ {0}`. -/
theorem cl_mem_lift_of_mem_pow {D κ : ℕ} (hDκ : D ∣ κ) (hκN : κ ∣ N) {x : K}
    (hx : x ∈ Pow D) : C.cl κ x ∈ ClassMap.lift κ ({0} : Set (ZMod D)) :=
  (C.mem_lift_iff hDκ hκN _ hx.1).mpr (C.cl_of_mem_pow (hDκ.trans hκN) hx)

/-- **A `D`-solver output, scaled, is a `Dℤ_κ`-relation at modulus `κ`** (paragraph
after Definition `def:plus-node`; `lift_κ {0} = Dℤ_κ` by `mem_lift_zero_iff`). -/
theorem rel_of_rootSol' {D κ : ℕ} (hDκ : D ∣ κ) (hκN : κ ∣ N) {col : ι → V} {r : ι → K}
    (h : IsRootSol D col r) :
    IsRel C κ (ClassMap.lift κ ({0} : Set (ZMod D))) col (normalize fun b => r b ^ D) := by
  have hD : D ∣ N := hDκ.trans hκN
  obtain ⟨h1, h2, h3⟩ := rel_of_rootSol C hD h
  refine ⟨h1, fun b hb => ?_, h3⟩
  have : normalize (fun b => r b ^ D) b ∈ Pow D :=
    (C.cl_eq_zero_iff hD hb).mp (h2 b hb)
  exact cl_mem_lift_of_mem_pow C hDκ hκN this

/-- `lift_κ {0} = Dℤ_κ` for `D ∣ κ`. -/
theorem mem_lift_zero_iff {D κ : ℕ} [NeZero κ] (hDκ : D ∣ κ) (i : ZMod κ) :
    i ∈ ClassMap.lift κ ({0} : Set (ZMod D)) ↔ ∃ k : ZMod κ, i = (D : ZMod κ) * k := by
  simp only [ClassMap.lift, Set.mem_ofPred_eq, Set.mem_singleton_iff]
  constructor
  · intro h
    rw [ZMod.cast_eq_val, ZMod.natCast_eq_zero_iff] at h
    obtain ⟨m, hm⟩ := h
    refine ⟨m, ?_⟩
    rw [← Nat.cast_mul, ← hm, ZMod.natCast_zmod_val]
  · rintro ⟨k, rfl⟩
    rw [← ZMod.castHom_apply (h := hDκ) (R := ZMod D), map_mul, map_natCast,
      ZMod.natCast_self, zero_mul]

end Roots

end QSearch.Schedule1HPlus
