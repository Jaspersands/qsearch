import Formal.Schedule1HPlus.Refine
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.Algebra.BigOperators.Intervals

/-!
# Schedule 1H⁺, part 4: axis relations, Lemma `lem:plus-tensor` (ℓ-level tensor),
Definition `def:plus-ell` and Lemma `lem:plus-ell-node`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus`, paragraph
"Multi-level contractions", Lemma `lem:plus-tensor`, Definition `def:plus-ell`, the remark
after it, and Lemma `lem:plus-ell-node`.

Encoding.

* `z_m = ξ^m` is `C.xiPow m` (`m : ZMod κ`, read through `m.val`).
* `AxisRel C ℓ T`: the axis relations `∑_m z_m T_{y[r:=m]} = 0` for every axis `r` and
  every `y`, with `y[r:=m] = Function.update y r m`.
* `tIdx κ a ℓ`: the column index type of the tensor (`M_ℓ(a)` columns, `card_tIdx`);
  level `ℓ+1` is `N` blocks of level `ℓ`, `N = (κ-1)^ℓ a + 1`.
* `tensor C a ℓ col = (lab, wt)`: `lab b = some y` means `b ∈ S_y`, `wt b = w_b`. The sets
  `S_y` are disjoint by construction (one label per column). `famT` is `T_y`.
* The recursion starts at `ℓ = 0` (one column, `S_() = {it}`, weight `1`, no axes); its
  first step is exactly the paper's case `ℓ = 1`.
* `tensor_spec` is **Lemma `lem:plus-tensor`** (correctness; the linear dependences are
  chosen by `depOf`, the paper uses Gaussian elimination; time not formalized).
* `IsEllContraction` is **Definition `def:plus-ell`**; `ellNode_spec` is **Lemma
  `lem:plus-ell-node`** (correctness), `card_tIdx_le` its constant
  `(κ-1)^{ℓ(ℓ-1)/2}`.
* `axis_zero_of_nz` is the "induction on the number of zero coordinates" of the proof of
  Lemma `lem:plus-tensor`. The remark after Definition `def:plus-ell` (condition (iii) is
  equivalent to vanishing on the product basis tensors) is proved as `ann_iff_check` in the
  review module `Formal.Schedule1HPlusReview.EllTable`, not here.
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset Module

variable {K : Type*} [Field K] [DecidableEq K] {N : ℕ} (C : ClassMap K N)
variable {κ : ℕ} [NeZero κ]

section Axis

variable {W : Type*} [AddCommGroup W] [Module K W]

/-- **The axis relations.** -/
def AxisRel (ℓ : ℕ) (T : (Fin ℓ → ZMod κ) → W) : Prop :=
  ∀ (r : Fin ℓ) (y : Fin ℓ → ZMod κ), ∑ m : ZMod κ, C.xiPow m • T (Function.update y r m) = 0

theorem axisRel_sum {β : Type*} [Fintype β] (ℓ : ℕ) (F : β → (Fin ℓ → ZMod κ) → W)
    (θ : β → K) (h : ∀ μ, AxisRel C ℓ (F μ)) : AxisRel C ℓ (fun y => ∑ μ, θ μ • F μ y) := by
  intro r y
  simp_rw [Finset.smul_sum, smul_comm (C.xiPow _) (θ _)]
  rw [Finset.sum_comm]
  exact Finset.sum_eq_zero fun μ _ => by rw [← Finset.smul_sum, h μ r y, smul_zero]

theorem axisRel_map {W' : Type*} [AddCommGroup W'] [Module K W'] (ℓ : ℕ)
    (T : (Fin ℓ → ZMod κ) → W) (φ : W →ₗ[K] W') (h : AxisRel C ℓ T) :
    AxisRel C ℓ (fun y => φ (T y)) := by
  intro r y
  simp_rw [← φ.map_smul, ← map_sum, h r y, map_zero]

/-- **Induction on the number of zero coordinates.** A family with the axis relations
that vanishes at every `y` without zero coordinate vanishes everywhere. -/
theorem axis_zero_of_nz (ℓ : ℕ) (G : (Fin ℓ → ZMod κ) → W) (hG : AxisRel C ℓ G)
    (hnz : ∀ y, (∀ r, y r ≠ 0) → G y = 0) : ∀ y, G y = 0 := by
  have key : ∀ n, ∀ y : Fin ℓ → ZMod κ,
      (Finset.univ.filter fun r => y r = 0).card ≤ n → G y = 0 := by
    intro n
    induction n with
    | zero =>
      intro y hy
      apply hnz
      intro r hr
      have hmem : r ∈ Finset.univ.filter (fun r => y r = 0) := by simp [hr]
      rw [Finset.card_eq_zero.mp (Nat.le_zero.mp hy)] at hmem
      simp at hmem
    | succ n ih =>
      intro y hy
      by_cases hall : ∀ r, y r ≠ 0
      · exact hnz y hall
      push Not at hall
      obtain ⟨r, hr⟩ := hall
      have hrel := hG r y
      rw [← Finset.add_sum_erase _ _ (Finset.mem_univ 0)] at hrel
      have hrest : ∀ m ∈ Finset.univ.erase (0 : ZMod κ),
          C.xiPow m • G (Function.update y r m) = 0 := by
        intro m hm
        have hm0 : m ≠ 0 := (Finset.mem_erase.mp hm).1
        have hsub : Finset.univ.filter (fun s => Function.update y r m s = 0) ⊆
            (Finset.univ.filter fun s => y s = 0).erase r := by
          intro s hs
          simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_erase] at hs ⊢
          by_cases hsr : s = r
          · subst hsr; simp at hs; exact absurd hs hm0
          · rw [Function.update_of_ne hsr] at hs; exact ⟨hsr, hs⟩
        have hc := Finset.card_le_card hsub
        rw [Finset.card_erase_of_mem (by simp [hr])] at hc
        rw [ih _ (by omega), smul_zero]
      have hupd : Function.update y r 0 = y := by rw [← hr, Function.update_eq_self]
      rw [Finset.sum_eq_zero hrest, add_zero, ClassMap.xiPow_zero, one_smul, hupd] at hrel
      exact hrel
  exact fun y => key _ y le_rfl

end Axis

section Tensor

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- `T_y = ∑_{b ∈ S_y} w_b λ_b`. -/
def famT {ι : Type*} [Fintype ι] {ℓ : ℕ} (lab : ι → Option (Fin ℓ → ZMod κ)) (wt : ι → K)
    (col : ι → V) (y : Fin ℓ → ZMod κ) : V :=
  ∑ b, if lab b = some y then wt b • col b else 0

/-- What Lemma `lem:plus-tensor` asserts of `(S_y, w)`: weights in `P` on `⋃ S_y`, an
index `b* ∈ S_0` of weight `1`, and the axis relations for `T_y`. -/
def TensorOK {ι : Type*} [Fintype ι] (ℓ : ℕ) (col : ι → V) (lab : ι → Option (Fin ℓ → ZMod κ))
    (wt : ι → K) : Prop :=
  (∀ b, lab b ≠ none → wt b ∈ Pow κ) ∧ (∃ b, lab b = some 0 ∧ wt b = 1) ∧
    AxisRel C ℓ (famT lab wt col)

/-- `snoc` into `ℤ_κ^{ℓ+1}`: the paper's `(y, j)`. -/
def snocZ {ℓ : ℕ} (y : Fin ℓ → ZMod κ) (j : ZMod κ) : Fin (ℓ + 1) → ZMod κ := Fin.snoc y j

omit [NeZero κ] in
theorem snocZ_inj {ℓ : ℕ} {y y' : Fin ℓ → ZMod κ} {j j' : ZMod κ} :
    snocZ y' j' = snocZ y j ↔ y' = y ∧ j' = j := by
  constructor
  · intro h
    refine ⟨funext fun r => ?_, ?_⟩
    · have := congrFun h (Fin.castSucc r)
      simpa [snocZ] using this
    · have := congrFun h (Fin.last ℓ)
      simpa [snocZ] using this
  · rintro ⟨rfl, rfl⟩; rfl

omit [NeZero κ] in
theorem snocZ_zero {ℓ : ℕ} : snocZ (0 : Fin ℓ → ZMod κ) 0 = 0 := by
  funext r
  refine Fin.lastCases ?_ (fun r => ?_) r <;> simp [snocZ]

/-- The column index type of the `ℓ`-level tensor. -/
def tIdx (κ a : ℕ) : ℕ → Type
  | 0 => Unit
  | ℓ + 1 => Fin ((κ - 1) ^ ℓ * a + 1) × tIdx κ a ℓ

instance instFintypeTIdx (κ a : ℕ) : (ℓ : ℕ) → Fintype (tIdx κ a ℓ)
  | 0 => inferInstanceAs (Fintype Unit)
  | ℓ + 1 => letI := instFintypeTIdx κ a ℓ
      inferInstanceAs (Fintype (Fin ((κ - 1) ^ ℓ * a + 1) × tIdx κ a ℓ))

/-- `|tIdx κ a ℓ| = M_ℓ(a) = ∏_{t<ℓ} ((κ-1)^t a + 1)`. -/
theorem card_tIdx (κ a : ℕ) : ∀ ℓ : ℕ,
    Fintype.card (tIdx κ a ℓ) = ∏ t ∈ Finset.range ℓ, ((κ - 1) ^ t * a + 1)
  | 0 => rfl
  | ℓ + 1 => by
    show Fintype.card (Fin ((κ - 1) ^ ℓ * a + 1) × tIdx κ a ℓ) = _
    rw [Fintype.card_prod, Fintype.card_fin, card_tIdx κ a ℓ, Finset.prod_range_succ, mul_comm]

/-- **The constant of Lemma `lem:plus-ell-node`**: `M_ℓ(a) ≤ (κ-1)^{ℓ(ℓ-1)/2} (a+1)^ℓ`
for `κ ≥ 2`. -/
theorem card_tIdx_le (hκ2 : 2 ≤ κ) (a ℓ : ℕ) :
    Fintype.card (tIdx κ a ℓ) ≤ (κ - 1) ^ (ℓ * (ℓ - 1) / 2) * (a + 1) ^ ℓ := by
  rw [card_tIdx]
  calc ∏ t ∈ Finset.range ℓ, ((κ - 1) ^ t * a + 1)
      ≤ ∏ t ∈ Finset.range ℓ, ((κ - 1) ^ t * (a + 1)) := by
        refine Finset.prod_le_prod' fun t _ => ?_
        have : 1 ≤ (κ - 1) ^ t := Nat.one_le_pow _ _ (by omega)
        nlinarith
    _ = (κ - 1) ^ (∑ t ∈ Finset.range ℓ, t) * (a + 1) ^ ℓ := by
        rw [Finset.prod_mul_distrib, Finset.prod_pow_eq_pow_sum, Finset.prod_const,
          Finset.card_range]
    _ = (κ - 1) ^ (ℓ * (ℓ - 1) / 2) * (a + 1) ^ ℓ := by rw [Finset.sum_range_id]

/-- One level of the tensor recursion (proof of Lemma `lem:plus-tensor`, `ℓ ≥ 2`). -/
noncomputable def tensorStep {ℓ n : ℕ} {ι : Type*} [Fintype ι]
    (sub : Fin n → (ι → Option (Fin ℓ → ZMod κ)) × (ι → K)) (col : Fin n × ι → V) :
    (Fin n × ι → Option (Fin (ℓ + 1) → ZMod κ)) × (Fin n × ι → K) :=
  let Tμ : Fin n → (Fin ℓ → ZMod κ) → V := fun μ y =>
    famT (sub μ).1 (sub μ).2 (fun b => col (μ, b)) y
  let θ := normalize (depOf (K := K)
    (fun μ (y : Fin ℓ → {m : ZMod κ // m ≠ 0}) => Tμ μ (fun r => (y r).1)))
  (fun p => if θ p.1 = 0 then none
      else ((sub p.1).1 p.2).map (fun y => snocZ y (C.cl κ (θ p.1))),
   fun p => θ p.1 / C.xiPow (C.cl κ (θ p.1)) * (sub p.1).2 p.2)

/-- **The tensor of Lemma `lem:plus-tensor`**, on `M_ℓ(a)` columns. -/
noncomputable def tensor (a : ℕ) : (ℓ : ℕ) → (tIdx κ a ℓ → V) →
    (tIdx κ a ℓ → Option (Fin ℓ → ZMod κ)) × (tIdx κ a ℓ → K)
  | 0, _ => (fun _ => some 0, fun _ => 1)
  | ℓ + 1, col => tensorStep C (fun μ => tensor a ℓ (fun b => col (μ, b))) col

omit [DecidableEq K] in
theorem finrank_nz [FiniteDimensional K V] (ℓ : ℕ) :
    finrank K ((Fin ℓ → {m : ZMod κ // m ≠ 0}) → V) = (κ - 1) ^ ℓ * finrank K V := by
  rw [Module.finrank_pi_fintype, Finset.sum_const, Finset.card_univ, smul_eq_mul,
    Fintype.card_fun, Fintype.card_fin]
  congr 2
  simp [Fintype.card_subtype_compl, ZMod.card]

theorem tensorStep_spec [FiniteDimensional K V] (hκ : κ ∣ N) {ℓ n : ℕ} {ι : Type*}
    [Fintype ι] (sub : Fin n → (ι → Option (Fin ℓ → ZMod κ)) × (ι → K)) (col : Fin n × ι → V)
    (hn : (κ - 1) ^ ℓ * finrank K V < n)
    (hsub : ∀ μ, TensorOK C ℓ (fun b => col (μ, b)) (sub μ).1 (sub μ).2) :
    TensorOK C (ℓ + 1) col (tensorStep C sub col).1 (tensorStep C sub col).2 := by
  set Tμ : Fin n → (Fin ℓ → ZMod κ) → V := fun μ y =>
    famT (sub μ).1 (sub μ).2 (fun b => col (μ, b)) y with hTμ
  set U := fun μ (y : Fin ℓ → {m : ZMod κ // m ≠ 0}) => Tμ μ (fun r => (y r).1) with hU
  set θ := normalize (depOf (K := K) U) with hθ
  set j : Fin n → ZMod κ := fun μ => C.cl κ (θ μ) with hj
  have hrun : tensorStep C sub col =
      (fun p => if θ p.1 = 0 then none else ((sub p.1).1 p.2).map (fun y => snocZ y (j p.1)),
       fun p => θ p.1 / C.xiPow (j p.1) * (sub p.1).2 p.2) := rfl
  rw [hrun]
  -- the dependence
  have hfr : finrank K ((Fin ℓ → {m : ZMod κ // m ≠ 0}) → V) < Fintype.card (Fin n) := by
    rw [finrank_nz, Fintype.card_fin]; exact hn
  obtain ⟨hd0, hdep⟩ := depOf_spec U hfr
  have hθrel : ∑ μ, θ μ • U μ = 0 := normalize_rel U _ hd0 hdep
  -- vanishing on all `y`
  have hall : ∀ y, ∑ μ, θ μ • Tμ μ y = 0 := by
    refine axis_zero_of_nz C ℓ _ (axisRel_sum C ℓ Tμ θ fun μ => (hsub μ).2.2) ?_
    intro y hy
    have := congrFun hθrel (fun r => ⟨y r, hy r⟩)
    simpa [Finset.sum_apply, U] using this
  -- `z_{j_μ} w'_μ = θ_μ`
  have hzw : ∀ μ, C.xiPow (j μ) * (θ μ / C.xiPow (j μ)) = θ μ := fun μ => by
    field_simp [C.xiPow_ne (j μ)]
  -- the new family at `(y, j)`
  have hfam : ∀ (y : Fin ℓ → ZMod κ) (jj : ZMod κ),
      famT (fun p : Fin n × ι => if θ p.1 = 0 then none
          else ((sub p.1).1 p.2).map (fun y => snocZ y (j p.1)))
        (fun p => θ p.1 / C.xiPow (j p.1) * (sub p.1).2 p.2) col (snocZ y jj) =
      ∑ μ, if θ μ ≠ 0 ∧ j μ = jj then (θ μ / C.xiPow (j μ)) • Tμ μ y else 0 := by
    intro y jj
    unfold famT
    rw [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun μ _ => ?_
    by_cases hθμ : θ μ = 0
    · simp [hθμ]
    · by_cases hjμ : j μ = jj
      · subst hjμ
        simp only [hθμ, ite_false, ne_eq, not_false_eq_true, true_and, ite_true, Tμ, famT,
          Finset.smul_sum]
        refine Finset.sum_congr rfl fun b _ => ?_
        cases hl : (sub μ).1 b with
        | none => simp
        | some y' =>
          simp only [Option.map_some, Option.some.injEq, snocZ_inj, and_true]
          split_ifs <;> simp [mul_smul]
      · simp only [hθμ, ite_false, ne_eq, not_false_eq_true, true_and, hjμ]
        refine Finset.sum_eq_zero fun b _ => ?_
        cases hl : (sub μ).1 b with
        | none => simp
        | some y' =>
          simp only [Option.map_some, Option.some.injEq, snocZ_inj]
          rw [if_neg (fun h => hjμ h.2)]
  refine ⟨?_, ?_, ?_⟩
  · -- weights in `P`
    rintro ⟨μ, b⟩ hb
    simp only at hb ⊢
    have hθμ : θ μ ≠ 0 := fun h => hb (by simp [h])
    have hlab : (sub μ).1 b ≠ none := fun h => hb (by simp [hθμ, h])
    have hw := (hsub μ).1 b hlab
    have hw' : θ μ / C.xiPow (j μ) ∈ Pow κ := by
      have hne : θ μ / C.xiPow (j μ) ≠ 0 := div_ne_zero hθμ (C.xiPow_ne _)
      refine (C.cl_eq_zero_iff hκ hne).mp ?_
      rw [C.cl_div hκ hθμ (C.xiPow_ne _), C.cl_xiPow hκ, sub_self]
    have hne : θ μ / C.xiPow (j μ) * (sub μ).2 b ≠ 0 := mul_ne_zero hw'.1 hw.1
    refine (C.cl_eq_zero_iff hκ hne).mp ?_
    rw [C.cl_mul hκ hw'.1 hw.1, C.cl_of_mem_pow hκ hw', C.cl_of_mem_pow hκ hw, add_zero]
  · -- designated index
    obtain ⟨μ, hμ⟩ : ∃ μ, θ μ = 1 := normalize_one _ hd0
    obtain ⟨b, hb, hw⟩ := (hsub μ).2.1
    have hjμ : j μ = 0 := by simp only [j, hμ, C.cl_one hκ]
    refine ⟨(μ, b), ?_, ?_⟩
    · simp only [hμ, one_ne_zero, ite_false, hb, Option.map_some, hjμ, snocZ_zero]
    · simp only [hμ, hjμ, hw, ClassMap.xiPow_zero, div_one, mul_one]
  · -- axis relations
    intro r y
    rw [← Fin.snoc_init_self y]
    refine Fin.lastCases ?_ (fun r' => ?_) r
    · -- the new axis
      have hupd : ∀ m : ZMod κ, Function.update (Fin.snoc (Fin.init y) (y (Fin.last ℓ)) :
          Fin (ℓ + 1) → ZMod κ) (Fin.last ℓ) m = snocZ (Fin.init y) m := fun m => by
        rw [Fin.update_snoc_last]; rfl
      simp_rw [hupd, hfam, Finset.smul_sum]
      rw [Finset.sum_comm]
      have : ∀ μ, ∑ m : ZMod κ, C.xiPow m •
          (if θ μ ≠ 0 ∧ j μ = m then (θ μ / C.xiPow (j μ)) • Tμ μ (Fin.init y) else 0) =
          θ μ • Tμ μ (Fin.init y) := by
        intro μ
        by_cases hθμ : θ μ = 0
        · simp [hθμ]
        · rw [Finset.sum_eq_single (j μ)]
          · simp only [ne_eq, hθμ, not_false_eq_true, true_and, ite_true, smul_smul]
            rw [hzw μ]
          · intro m _ hm
            rw [if_neg (fun h => hm h.2.symm), smul_zero]
          · simp
      simp_rw [this]
      exact hall _
    · -- an old axis
      have hupd : ∀ m : ZMod κ, Function.update (Fin.snoc (Fin.init y) (y (Fin.last ℓ)) :
          Fin (ℓ + 1) → ZMod κ) (Fin.castSucc r') m =
          snocZ (Function.update (Fin.init y) r' m) (y (Fin.last ℓ)) := fun m => by
        rw [← Fin.snoc_update]; rfl
      simp_rw [hupd, hfam, Finset.smul_sum]
      rw [Finset.sum_comm]
      refine Finset.sum_eq_zero fun μ _ => ?_
      by_cases hc : θ μ ≠ 0 ∧ j μ = y (Fin.last ℓ)
      · rw [Finset.sum_congr rfl (fun m _ => by rw [if_pos hc])]
        simp_rw [smul_comm (C.xiPow _) (θ μ / C.xiPow (j μ))]
        rw [← Finset.smul_sum, (hsub μ).2.2 r' (Fin.init y), smul_zero]
      · simp [hc]

/-- **Lemma `lem:plus-tensor`.** On `M_ℓ(a)` columns (`a = finrank V`) the tensor gives
disjoint sets `S_y`, weights in `P`, an index `b* ∈ S_0` of weight `1`, and vectors `T_y`
satisfying the axis relations. -/
theorem tensor_spec [FiniteDimensional K V] (hκ : κ ∣ N) :
    ∀ (ℓ : ℕ) (col : tIdx κ (finrank K V) ℓ → V),
      TensorOK C ℓ col (tensor C (finrank K V) ℓ col).1 (tensor C (finrank K V) ℓ col).2
  | 0, col => by
    refine ⟨fun _ _ => ⟨one_ne_zero, 1, one_pow _⟩, ⟨(), rfl, rfl⟩, fun r => r.elim0⟩
  | ℓ + 1, col =>
    tensorStep_spec C hκ _ col (Nat.lt_succ_self _)
      (fun μ => tensor_spec hκ ℓ (fun b => col (μ, b)))

end Tensor

section EllNode

variable {V : Type*} [AddCommGroup V] [Module K V]

/-- **Definition `def:plus-ell`**: an `ℓ`-level `Ω`-contraction. -/
structure IsEllContraction (ℓ : ℕ) (Ω : Set (ZMod κ)) (Ct : (Fin ℓ → ZMod κ) → K) : Prop where
  cls : ∀ y, Ct y ≠ 0 → C.cl κ (Ct y) ∈ Ω
  base : Ct 0 ∈ Pow κ
  ann : ∀ X : (Fin ℓ → ZMod κ) → K, AxisRel C ℓ X → ∑ y, Ct y * X y = 0

/-- **The node of Lemma `lem:plus-ell-node`**: `x_b = C_y w_b / C_0` for `b ∈ S_y`. -/
noncomputable def ellNode (a ℓ : ℕ) (Ct : (Fin ℓ → ZMod κ) → K) (col : tIdx κ a ℓ → V) :
    tIdx κ a ℓ → K :=
  fun b => match (tensor C a ℓ col).1 b with
    | some y => Ct y * (tensor C a ℓ col).2 b / Ct 0
    | none => 0

/-- **Lemma `lem:plus-ell-node`.** An `ℓ`-level `Ω`-contraction turns the tensor into an
`Ω`-relation at modulus `κ` (an `Ω`-node of arity `M_ℓ(a)`). -/
theorem ellNode_spec [FiniteDimensional K V] (hκ : κ ∣ N) {ℓ : ℕ} {Ω : Set (ZMod κ)}
    {Ct : (Fin ℓ → ZMod κ) → K} (hC : IsEllContraction C ℓ Ω Ct) :
    IsNode C κ Ω (tIdx κ (finrank K V) ℓ) (ellNode C (finrank K V) ℓ Ct (V := V)) := by
  intro col
  obtain ⟨hw, ⟨bs, hbs, hws⟩, hax⟩ := tensor_spec C hκ ℓ col
  set lab := (tensor C (finrank K V) ℓ col).1
  set wt := (tensor C (finrank K V) ℓ col).2
  have hC0 : Ct 0 ≠ 0 := hC.base.1
  have hx : ellNode C (finrank K V) ℓ Ct col = fun b => match lab b with
      | some y => Ct y * wt b / Ct 0
      | none => 0 := rfl
  rw [hx]
  refine ⟨⟨bs, ?_⟩, ?_, ?_⟩
  · simp only [hbs, hws, mul_one]; exact div_self hC0
  · intro b hb
    cases hl : lab b with
    | none => simp [hl] at hb
    | some y =>
      simp only [hl] at hb ⊢
      have hCy : Ct y ≠ 0 := fun h => hb (by simp [h])
      have hwb := hw b (by simp [hl])
      rw [C.cl_div hκ (mul_ne_zero hCy hwb.1) hC0, C.cl_mul hκ hCy hwb.1,
        C.cl_of_mem_pow hκ hwb, C.cl_of_mem_pow hκ hC.base, add_zero, sub_zero]
      exact hC.cls y hCy
  · -- `C_0 ∑ x_b λ_b = ∑_y C_y T_y = 0`
    have hreg : ∑ b, (match lab b with
        | some y => Ct y * wt b / Ct 0
        | none => 0) • col b = (Ct 0)⁻¹ • ∑ y, Ct y • famT lab wt col y := by
      simp only [famT, Finset.smul_sum]
      rw [Finset.sum_comm]
      refine Finset.sum_congr rfl fun b _ => ?_
      cases hl : lab b with
      | none => simp
      | some y =>
        rw [Finset.sum_eq_single y]
        · simp only [ite_true, smul_smul]; congr 1; field_simp
        · intro y' _ hy'; rw [if_neg (fun h => hy' (Option.some_injective _ h).symm)]; simp
        · simp
    rw [hreg]
    have hzero : ∑ y, Ct y • famT lab wt col y = 0 := by
      refine (Module.forall_dual_apply_eq_zero_iff K _).mp fun φ => ?_
      rw [map_sum]
      simp_rw [map_smul, smul_eq_mul]
      exact hC.ann _ (axisRel_map C ℓ _ φ hax)
    rw [hzero, smul_zero]

/-- With `Ω = {0}` and `κ`-th roots, the `ℓ`-level node is a `κ`-solver of arity
`M_ℓ(a)` (Lemma `lem:plus-ell-node`, last sentence). -/
theorem ellSolver_spec [FiniteDimensional K V] (hκ : κ ∣ N) {ℓ : ℕ}
    {Ct : (Fin ℓ → ZMod κ) → K} (hC : IsEllContraction C ℓ {0} Ct) (rt : K → K)
    (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x) (col : tIdx κ (finrank K V) ℓ → V) :
    IsRootSol κ col (rootsOf rt (ellNode C (finrank K V) ℓ Ct col)) :=
  rootSol_of_rel C hκ rt hrt (ellNode_spec C hκ hC col)

end EllNode

end QSearch.Schedule1HPlus
