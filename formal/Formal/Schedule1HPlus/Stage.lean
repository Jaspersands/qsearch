import Formal.Schedule1HPlus.Refine
import Formal.Schedule1H.Levels

/-!
# Schedule 1H⁺, part 3: Lemma `lem:plus-stage` (two-class stage), Lemma
`lem:plus-finish` (finish `F_𝒦`), and the plans `(𝒩, s, F)`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus`, paragraph
"Stages and finishes with classes", Lemmas `lem:plus-stage` and `lem:plus-finish`, and the
plan clause (f) of Definition `def:plus-schedule` as run in Theorem `thm:plus`(ii).

* `plusStageRun C κ m rt nd v`: one call of a `{0,m}`-node `nd` on the vectors `v`; `I`
  gets the roots of the class-`0` weights, `J` the roots of `x_ν / q`, `q = ξ^m`.
* `plusStage_stepSpec`: the answer meets `StepSpec κ ε` with `ε = -q⁻¹`; with the
  Schedule 1H machinery (`step_spec`) this is **Lemma `lem:plus-stage`**
  (`plusStage_spec`).
* `plusFinish` / `plusFinish_spec`: **Lemma `lem:plus-finish`**.
* `plusPlanF0_spec`, `plusPlanFK_spec`: the plans `(𝒩, s, F0)` and `(𝒩, s, F_𝒦)` with a
  two-class node, run by the level recursion `runLevel` of Schedule 1H, return
  `κ`-solutions.
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset

variable {K : Type*} [Field K] [DecidableEq K] {N : ℕ} (C : ClassMap K N)
variable {V : Type*} [AddCommGroup V] [Module K V]

section Stage

/-- **The two-class stage call** (proof of Lemma `lem:plus-stage`). -/
def plusStageRun (κ : ℕ) (m : ZMod κ) (rt : K → K) {A : ℕ} (nd : (Fin A → V) → Fin A → K)
    (v : Fin A → V) : (Fin A → K) × (Fin A → K) :=
  let x := nd v
  (fun ν => if x ν ≠ 0 ∧ C.cl κ (x ν) = 0 then rt (x ν) else 0,
   fun ν => if x ν ≠ 0 ∧ C.cl κ (x ν) = m then rt (x ν / C.xiPow m) else 0)

theorem plusStage_stepSpec {κ : ℕ} (hκ : κ ∣ N) {m : ZMod κ} (hm : m ≠ 0) (rt : K → K)
    (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x) {A : ℕ} (nd : (Fin A → V) → Fin A → K) (v : Fin A → V)
    (hnd : IsRel C κ {0, m} v (nd v)) :
    StepSpec κ (-(C.xiPow m)⁻¹) v (plusStageRun C κ m rt nd v).1
      (plusStageRun C κ m rt nd v).2 := by
  have hκ0 : 0 < κ := C.pos_of_dvd hκ
  set q := C.xiPow m with hqdef
  have hq : q ≠ 0 := C.xiPow_ne m
  have hclq : C.cl κ q = m := C.cl_xiPow hκ m
  set x := nd v with hx
  set ρ : Fin A → K := fun ν => if x ν ≠ 0 ∧ C.cl κ (x ν) = 0 then rt (x ν) else 0 with hρ
  set σ : Fin A → K := fun ν => if x ν ≠ 0 ∧ C.cl κ (x ν) = m then rt (x ν / q) else 0
    with hσ
  have hrun : plusStageRun C κ m rt nd v = (ρ, σ) := rfl
  rw [hrun]
  have hpt : ∀ ν, x ν = ρ ν ^ κ + q * σ ν ^ κ := by
    intro ν
    by_cases h0 : x ν = 0
    · simp [ρ, σ, h0, zero_pow hκ0.ne']
    · have hcl := hnd.2.1 ν h0
      rcases hcl with h1 | h1
      · have hP : x ν ∈ Pow κ := (C.cl_eq_zero_iff hκ h0).mp h1
        have hnm : ¬ C.cl κ (x ν) = m := fun h => hm (h.symm.trans h1)
        have hc1 : x ν ≠ 0 ∧ C.cl κ (x ν) = 0 := ⟨h0, h1⟩
        have hc2 : ¬ (x ν ≠ 0 ∧ C.cl κ (x ν) = m) := fun h => hnm h.2
        rw [show ρ ν = rt (x ν) from if_pos hc1, show σ ν = 0 from if_neg hc2, hrt _ hP,
          zero_pow hκ0.ne', mul_zero, add_zero]
      · have h1' : C.cl κ (x ν) = m := h1
        have hn0 : ¬ C.cl κ (x ν) = 0 := fun h => hm (h1'.symm.trans h)
        have hP : x ν / q ∈ Pow κ := by
          refine (C.cl_eq_zero_iff hκ (div_ne_zero h0 hq)).mp ?_
          rw [C.cl_div hκ h0 hq, h1', hclq, sub_self]
        have hc1 : ¬ (x ν ≠ 0 ∧ C.cl κ (x ν) = 0) := fun h => hn0 h.2
        have hc2 : x ν ≠ 0 ∧ C.cl κ (x ν) = m := ⟨h0, h1'⟩
        rw [show ρ ν = 0 from if_neg hc1, show σ ν = rt (x ν / q) from if_pos hc2, hrt _ hP,
          zero_pow hκ0.ne', zero_add]
        field_simp
  refine ⟨?_, ?_, ?_⟩
  · obtain ⟨ν, hν⟩ := hnd.1
    intro h0
    have h1 := congrFun h0 ν
    have hcl1 : C.cl κ (x ν) = 0 := by rw [show x ν = 1 from hν, C.cl_one hκ]
    have hx0 : x ν ≠ 0 := by rw [show x ν = 1 from hν]; exact one_ne_zero
    simp only [ρ, hx0, ne_eq, not_false_eq_true, true_and, hcl1, ite_true, Pi.zero_apply] at h1
    have h2 := hrt (x ν) ((C.cl_eq_zero_iff hκ hx0).mp hcl1)
    rw [h1, zero_pow hκ0.ne'] at h2
    exact hx0 h2.symm
  · intro ν
    by_cases h : x ν ≠ 0 ∧ C.cl κ (x ν) = 0
    · right
      have : ¬ (x ν ≠ 0 ∧ C.cl κ (x ν) = m) := fun h' => hm (h'.2.symm.trans h.2)
      simp [σ, this]
    · left; simp [ρ, h]
  · have hsum : ∑ ν, ρ ν ^ κ • v ν + q • ∑ ν, σ ν ^ κ • v ν = 0 := by
      rw [Finset.smul_sum, ← Finset.sum_add_distrib, ← hnd.2.2]
      refine Finset.sum_congr rfl fun ν _ => ?_
      rw [smul_smul, ← add_smul, ← hpt ν]
    have h2 : q • ∑ ν, σ ν ^ κ • v ν = -∑ ν, ρ ν ^ κ • v ν := eq_neg_of_add_eq_zero_right hsum
    have h3 := congrArg (fun y => q⁻¹ • y) h2
    simp only [smul_smul, inv_mul_cancel₀ hq, one_smul, smul_neg] at h3
    rw [h3, neg_smul]

variable {ι τ : Type*} [Fintype ι] [DecidableEq τ]

/-- **Lemma `lem:plus-stage`.** A `{0,m}`-node at modulus `κ` (`m ≠ 0`) on `N` objects of
type `c` with disjoint supports gives a `κ`-solution or an object of type `(c, εc)`,
`ε = -(ξ^m)⁻¹`. -/
theorem plusStage_spec {κ : ℕ} (hκ : κ ∣ N) {m : ZMod κ} (hm : m ≠ 0) (rt : K → K)
    (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x) {A : ℕ} (nd : (Fin A → V) → Fin A → K) (k0 : τ)
    (col : Fin A × ι → V) (c : τ → K) (o : Fin A → Obj ι τ V K)
    (ho : ∀ ν, IsObj κ (fun i => col (ν, i)) c (o ν))
    (hnd : IsRel C κ {0, m} (fun ν => (o ν).v) (nd fun ν => (o ν).v)) :
    ResOK κ col (extType c (-(C.xiPow m)⁻¹))
      (step κ k0 o (plusStageRun C κ m rt nd fun ν => (o ν).v).1
        (plusStageRun C κ m rt nd fun ν => (o ν).v).2) :=
  step_spec (C.pos_of_dvd hκ) k0 col c (neg_ne_zero.mpr (inv_ne_zero (C.xiPow_ne m))) o ho _ _
    (plusStage_stepSpec C hκ hm rt hrt nd _ hnd)

end Stage

section Finish

variable {ι τ β : Type*} [Fintype ι] [Fintype τ] [DecidableEq τ] [Fintype β]

/-- **The finish `F_𝒦` of Lemma `lem:plus-finish`**: `η' = ξ^u η`, and each nonzero
`η'_ν` is written as `∑_k y_k^κ c_k` by `fin`. -/
def plusFinish (κ : ℕ) (u : ZMod κ) (fin : K → τ → K) (o : β → Obj ι τ V K) (η : β → K) :
    β × ι → K :=
  finishGen o (fun b => if η b = 0 then 0 else fin (C.xiPow u * η b))

/-- **Lemma `lem:plus-finish`.** Objects of type `c` with disjoint supports, an
`Ω`-relation `η` at modulus `κ` among their vectors, `u` with `ξ^{u+k} P ⊆ T(c)` for every
`k ∈ Ω`, and `fin` writing every nonzero element of `T(c)` with roots: the finish is a
`κ`-solution. -/
theorem plusFinish_spec {κ : ℕ} (hκ : κ ∣ N) {Ω : Set (ZMod κ)} (u : ZMod κ) (c : τ → K)
    (hT : ∀ k ∈ Ω, ∀ y ∈ Pow κ, C.xiPow (u + k) * y ∈ Tset κ c)
    (fin : K → τ → K)
    (hfin : ∀ x : K, x ≠ 0 → x ∈ Tset κ c → fin x ≠ 0 ∧ ∑ k, fin x k ^ κ * c k = x)
    (col : β × ι → V) (o : β → Obj ι τ V K)
    (ho : ∀ b, IsObj κ (fun i => col (b, i)) c (o b)) (η : β → K)
    (hη : IsRel C κ Ω (fun b => (o b).v) η) :
    IsRootSol κ col (plusFinish C κ u fin o η) := by
  have hκ0 : 0 < κ := C.pos_of_dvd hκ
  have hmem : ∀ b, η b ≠ 0 → C.xiPow u * η b ∈ Tset κ c := by
    intro b hb
    have hne : C.xiPow u * η b ≠ 0 := mul_ne_zero (C.xiPow_ne u) hb
    obtain ⟨y, hy, hxy⟩ := C.mem_coset hκ hne
    have hcl : C.cl κ (C.xiPow u * η b) = u + C.cl κ (η b) := by
      rw [C.cl_mul hκ (C.xiPow_ne u) hb, C.cl_xiPow hκ]
    rw [hxy, hcl]
    exact hT _ (hη.2.1 b hb) y hy
  refine finishGen_spec hκ0 col c o ho _ (fun b => C.xiPow u * η b) (fun b => ?_) ?_ ?_
  · by_cases hb : η b = 0
    · simp [hb, zero_pow hκ0.ne']
    · simp only [hb, ite_false]
      exact (hfin _ (mul_ne_zero (C.xiPow_ne u) hb) (hmem b hb)).2
  · simp_rw [mul_smul, ← Finset.smul_sum, hη.2.2, smul_zero]
  · obtain ⟨b, hb⟩ := hη.1
    have hb0 : η b ≠ 0 := by rw [hb]; exact one_ne_zero
    refine ⟨b, ?_⟩
    simp only [hb0, ite_false]
    exact (hfin _ (mul_ne_zero (C.xiPow_ne u) hb0) (hmem b hb0)).1

end Finish

section Plans

variable {A : ℕ}

/-- **Plan `(𝒩, s, F0)` with a two-class node** (Definition `def:plus-schedule`(f)): the
Schedule 1H level recursion with the two-class stage as its step oracle. -/
def plusPlanF0 (κ : ℕ) (m : ZMod κ) (rt : K → K) (nd : (Fin A → V) → Fin A → K) (s : ℕ)
    (ρ0 : Typ s → K) (col : Lev A s → V) : Lev A s → K :=
  planF0 κ (plusStageRun C κ m rt nd) s ρ0 col

theorem plusPlanF0_spec {κ : ℕ} (hκ : κ ∣ N) {m : ZMod κ} (hm : m ≠ 0) (rt : K → K)
    (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x) (nd : (Fin A → V) → Fin A → K)
    (hnd : IsNode C κ {0, m} (Fin A) nd) (s : ℕ) (ρ0 : Typ s → K) (hρ0 : ρ0 ≠ 0)
    (hz : ∑ k, ρ0 k ^ κ * cTyp (-(C.xiPow m)⁻¹) s k = 0) (col : Lev A s → V) :
    IsRootSol κ col (plusPlanF0 C κ m rt nd s ρ0 col) :=
  planF0_spec (C.pos_of_dvd hκ) (neg_ne_zero.mpr (inv_ne_zero (C.xiPow_ne m))) _
    (fun v => plusStage_stepSpec C hκ hm rt hrt nd v (hnd v)) s ρ0 hρ0 hz col

/-- **Plan `(𝒩, s, F_𝒦)` with a two-class node**: `n_F` blocks of level `s`, then the
`Ω`-node `kn` on the final vectors and the finish of Lemma `lem:plus-finish`. -/
def plusPlanFK (κ : ℕ) (m : ZMod κ) (rt : K → K) (nd : (Fin A → V) → Fin A → K) (s : ℕ)
    (u : ZMod κ) (fin : K → Typ s → K) {nF : ℕ} (kn : (Fin nF → V) → Fin nF → K)
    (col : Fin nF × Lev A s → V) : Fin nF × Lev A s → K :=
  match firstSol (fun b : Fin nF => runLevel κ (plusStageRun C κ m rt nd) s
      (fun i => col (b, i))) with
  | some (b, r) => extendSol b r
  | none =>
    let objs := fun b : Fin nF =>
      objOf (runLevel κ (plusStageRun C κ m rt nd) s (fun i => col (b, i)))
    plusFinish C κ u fin objs (kn fun b => (objs b).v)

theorem plusPlanFK_spec {κ : ℕ} (hκ : κ ∣ N) {m : ZMod κ} (hm : m ≠ 0) (rt : K → K)
    (hrt : ∀ x ∈ Pow κ, rt x ^ κ = x) (nd : (Fin A → V) → Fin A → K)
    (hnd : IsNode C κ {0, m} (Fin A) nd) (s : ℕ) {Ω : Set (ZMod κ)} (u : ZMod κ)
    (hT : ∀ k ∈ Ω, ∀ y ∈ Pow κ, C.xiPow (u + k) * y ∈ Tset κ (cTyp (-(C.xiPow m)⁻¹) s))
    (fin : K → Typ s → K)
    (hfin : ∀ x : K, x ≠ 0 → x ∈ Tset κ (cTyp (-(C.xiPow m)⁻¹) s) →
      fin x ≠ 0 ∧ ∑ k, fin x k ^ κ * cTyp (-(C.xiPow m)⁻¹) s k = x)
    {nF : ℕ} (kn : (Fin nF → V) → Fin nF → K) (hkn : IsNode C κ Ω (Fin nF) kn)
    (col : Fin nF × Lev A s → V) :
    IsRootSol κ col (plusPlanFK C κ m rt nd s u fin kn col) := by
  have hκ0 : 0 < κ := C.pos_of_dvd hκ
  have he : -(C.xiPow m)⁻¹ ≠ 0 := neg_ne_zero.mpr (inv_ne_zero (C.xiPow_ne m))
  have horc := fun v => plusStage_stepSpec C hκ hm rt hrt nd v (hnd v)
  have ih := fun b : Fin nF => runLevel_spec hκ0 he _ horc s (fun i => col (b, i))
  unfold plusPlanFK
  cases hf : firstSol (fun b : Fin nF => runLevel κ (plusStageRun C κ m rt nd) s
      (fun i => col (b, i))) with
  | some br =>
    obtain ⟨b, r⟩ := br
    have := ih b
    rw [firstSol_some hf] at this
    exact extendSol_spec hκ0 b col r this
  | none =>
    have ho : ∀ b, IsObj κ (fun i => col (b, i)) (cTyp (-(C.xiPow m)⁻¹) s)
        (objOf (runLevel κ (plusStageRun C κ m rt nd) s (fun i => col (b, i)))) := by
      intro b
      obtain ⟨y, hy⟩ := firstSol_none hf b
      have := ih b
      rw [hy] at this ⊢
      exact this
    exact plusFinish_spec C hκ u _ hT fin hfin col _ ho _ (hkn _)

end Plans

end QSearch.Schedule1HPlus
