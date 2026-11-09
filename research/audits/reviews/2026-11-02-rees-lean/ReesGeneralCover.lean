import Formal.ReesLieInterpolation
import Formal.ReesCentralQuotient

/-!
# General-class Rees cover facts at the Lie level

Item 8 of `research/REES_FULL_CAMPAIGN.md`. This file adds to the existing
`ReesLieConstruction`, `ReesLieInterpolation` and `ReesCentralQuotient` the
Lie-level facts of step 1 (core report §1.1 items 1 and 3) that those modules
do not state, for an arbitrary nilpotence class:

* `lowerCentralSeries_rees_eq_bot_iff`, `rees_class_exact`,
  `nilpotencyLength_rees`: the Rees algebra has exactly the class of `L`;
* `top_grade_central`: the top grade is central;
* `evaluation_comp_scaling`: `E_s ∘ δ_a = E_{a s}`;
* `evaluation_surjective`, `evaluation_image_tail`: for a unit `s`,
  `E_s` is onto and `E_s(⊕_{j > d} t^j γ_j) = γ_{d+1}`;
* `mem_hiddenCover_iff_coeff`, `mem_hiddenCover_iff_forall_eval`,
  `hiddenCover_eq`: the hidden cover is `⊕_r t^r (h ∩ γ_r)`, equals the
  intersection of `E_s^{-1}(h)` over every `s`, and does not depend on the
  interpolation points;
* `field_hiddenCover_eq`: over a field, any `c` distinct nonzero points;
* `evaluation_image_hiddenCover`, `gradeOne_mem_hiddenCover_iff`: for a unit
  `s`, `E_s(h̃) = h`, and grade one of `h̃` is exactly `h`.

The hypothesis is only `lowerCentralSeries R L L c = ⊥` (class at most `c`)
over a commutative ring, with unit-determinant points; no characteristic
restriction and no `c < p` is used. Nothing here constructs a group law: the
BCH/Lazard transport is the separate input isolated in `ReesGeneralLaw.lean`.
-/

namespace QSearch.ReesGeneralCover

open LieModule QSearch.ReesLieConstruction QSearch.ReesLieInterpolation
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient
open scoped BigOperators

noncomputable section

set_option backward.isDefEq.respectTransparency false

variable {R L : Type*} [CommRing R] [LieRing L] [LieAlgebra R L]

/-! ## Evaluation on homogeneous and finite-support currents -/

theorem evaluation_eq_sum (a : R) (z : rees (R := R) (L := L)) {S : Finset ℕ}
    (hS : (coeff (z : Current R L)).support ⊆ S) :
    evaluation a z = ∑ r ∈ S, a ^ r • coeff (z : Current R L) r := by
  rw [evaluation_formula, Finsupp.sum_of_support_subset _ hS _ (by intros; simp)]

/-- The homogeneous Rees current `t^r x` as an element of the Rees algebra. -/
def homogeneousElement (r : ℕ) (hr : 0 < r) (x : L) (hx : x ∈ gamma R L r) :
    rees (R := R) (L := L) :=
  ⟨monomial r x, monomial_mem hr hx⟩

@[simp] theorem coeff_homogeneousElement (r : ℕ) (hr : 0 < r) (x : L)
    (hx : x ∈ gamma R L r) (k : ℕ) :
    coeff (homogeneousElement (R := R) r hr x hx : Current R L) k =
      Finsupp.single r x k := by
  change coeff (monomial (R := R) r x) k = _
  rw [coeff_monomial]

theorem evaluation_homogeneousElement (a : R) (r : ℕ) (hr : 0 < r) (x : L)
    (hx : x ∈ gamma R L r) :
    evaluation a (homogeneousElement (R := R) r hr x hx) = a ^ r • x := by
  rw [evaluation_formula]
  change (coeff (monomial (R := R) r x)).sum (fun k y => a ^ k • y) = _
  rw [coeff_monomial, Finsupp.sum_single_index (by simp)]

theorem evaluation_gradeOne (a : R) (x : L) :
    evaluation a (gradeOne (R := R) x) = a • x := by
  have hx : x ∈ gamma R L 1 := by simp [gamma, lowerCentralSeries_zero]
  have hg : gradeOne (R := R) x = homogeneousElement 1 (by decide) x hx := Subtype.ext rfl
  rw [hg, evaluation_homogeneousElement, pow_one]

/-! ## Class exactly `c` -/

/-- Evaluation at one is onto, since `gradeOne` is a right inverse. -/
theorem evaluation_one_surjective :
    Function.Surjective (evaluation (R := R) (L := L) 1) :=
  (grade_one_retention (R := R) (L := L)).surjective

/-- The lower central series of the Rees algebra vanishes at exactly the same
indices as that of `L`. -/
theorem lowerCentralSeries_rees_eq_bot_iff (k : ℕ) :
    lowerCentralSeries R (rees (R := R) (L := L)) (rees (R := R) (L := L)) k = ⊥ ↔
      lowerCentralSeries R L L k = ⊥ := by
  constructor
  · intro h
    rw [← LieIdeal.lowerCentralSeries_map_eq k evaluation_one_surjective, h]
    simp only [LieIdeal.map_eq_bot_iff, bot_le]
  · exact rees_class_bound k

/-- Class exactly `c` in Mathlib's indexing (`lowerCentralSeries 0 = L`):
`γ_{c+1} = 0` and `γ_c ≠ 0` pass from `L` to the Rees algebra. -/
theorem rees_class_exact (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥)
    (hexact : lowerCentralSeries R L L (c - 1) ≠ ⊥) :
    lowerCentralSeries R (rees (R := R) (L := L)) (rees (R := R) (L := L)) c = ⊥ ∧
      lowerCentralSeries R (rees (R := R) (L := L)) (rees (R := R) (L := L)) (c - 1) ≠ ⊥ :=
  ⟨rees_class_bound c hnil, fun h => hexact ((lowerCentralSeries_rees_eq_bot_iff _).mp h)⟩

/-- Mathlib's nilpotency length of the Rees algebra equals that of `L`. -/
theorem nilpotencyLength_rees :
    nilpotencyLength (rees (R := R) (L := L)) (rees (R := R) (L := L)) =
      nilpotencyLength L L := by
  have h (k : ℕ) :
      lowerCentralSeries ℤ (rees (R := R) (L := L)) (rees (R := R) (L := L)) k = ⊥ ↔
        lowerCentralSeries ℤ L L k = ⊥ := by
    have aux1 : lowerCentralSeries R (rees (R := R) (L := L)) (rees (R := R) (L := L)) k = ⊥ ↔
        lowerCentralSeries ℤ (rees (R := R) (L := L)) (rees (R := R) (L := L)) k = ⊥ := by
      simp [SetLike.ext'_iff, coe_lowerCentralSeries_eq_int R]
    have aux2 : lowerCentralSeries R L L k = ⊥ ↔ lowerCentralSeries ℤ L L k = ⊥ := by
      simp [SetLike.ext'_iff, coe_lowerCentralSeries_eq_int R]
    rw [← aux1, ← aux2]
    exact lowerCentralSeries_rees_eq_bot_iff k
  unfold nilpotencyLength
  congr 1
  ext k
  exact h k

/-- Under class at most `d + 1`, every current with no coefficient in degrees
`≤ d` (the top grade `t^{d+1} γ_{d+1}`) is central in the Rees algebra. -/
theorem top_grade_central (d : ℕ) (hnil : lowerCentralSeries R L L (d + 1) = ⊥)
    (z : rees (R := R) (L := L)) (hz : z ∈ tail (R := R) (L := L) d)
    (w : rees (R := R) (L := L)) : ⁅w, z⁆ = 0 := by
  have h := bracket_mem_tail d w z hz
  rw [tail_eq_bot (d + 1) hnil, LieSubmodule.mem_bot] at h
  exact h

/-! ## Evaluations and dilations -/

/-- `E_s ∘ δ_a = E_{a s}`; for a unit `a`, this is `E_s ∘ dilation a`. -/
theorem evaluation_comp_scaling (s a : R) (z : rees (R := R) (L := L)) :
    evaluation s (scaling a z) = evaluation (a * s) z := by
  classical
  set S := (coeff (z : Current R L)).support
  have hS : (coeff (scaling a z : Current R L)).support ⊆ S := by
    intro r hr
    rw [Finsupp.mem_support_iff] at hr ⊢
    intro h0
    apply hr
    rw [scaling_coeff, h0, smul_zero]
  rw [evaluation_eq_sum s _ hS, evaluation_eq_sum (a * s) z subset_rfl]
  apply Finset.sum_congr rfl
  intro r _
  rw [scaling_coeff, smul_smul, ← mul_pow, mul_comm s a]

theorem evaluation_comp_dilation (s : R) (u : Rˣ) (z : rees (R := R) (L := L)) :
    evaluation s (dilation u z) = evaluation ((u : R) * s) z :=
  evaluation_comp_scaling s (u : R) z

/-- Every evaluation maps the filtration step `⊕_{j > d} t^j γ_j` into `γ_{d+1}`. -/
theorem evaluation_mem_gamma_of_tail (s : R) (d : ℕ) (z : rees (R := R) (L := L))
    (hz : z ∈ tail (R := R) (L := L) d) : evaluation s z ∈ gamma R L (d + 1) := by
  classical
  rw [evaluation_eq_sum s z subset_rfl]
  apply Submodule.sum_mem
  intro r _
  apply Submodule.smul_mem
  by_cases hr : r ≤ d
  · have h0 : coeff (z : Current R L) r = 0 := hz r hr
    rw [h0]
    exact (gamma R L (d + 1)).zero_mem
  · have hmem := (mem_rees_iff (z : Current R L)).mp z.property |>.2 r
    exact antitone_lowerCentralSeries R L L (show d + 1 - 1 ≤ r - 1 by omega) hmem

/-- For a unit `s`, `E_s(⊕_{j > d} t^j γ_j) = γ_{d+1}` exactly. -/
theorem evaluation_image_tail {s : R} (hs : IsUnit s) (d : ℕ) :
    (evaluation s) '' (tail (R := R) (L := L) d : Set (rees (R := R) (L := L))) =
      (gamma R L (d + 1) : Set L) := by
  ext x
  constructor
  · rintro ⟨z, hz, rfl⟩
    exact evaluation_mem_gamma_of_tail s d z hz
  · intro hx
    obtain ⟨v, rfl⟩ := hs
    let y : L := ((v⁻¹ : Rˣ) : R) ^ (d + 1) • x
    have hy : y ∈ gamma R L (d + 1) := (gamma R L (d + 1)).smul_mem _ hx
    refine ⟨homogeneousElement (d + 1) (by omega) y hy, ?_, ?_⟩
    · intro r hr
      rw [coefficient_apply, coeff_homogeneousElement, Finsupp.single_eq_of_ne (by omega)]
    · rw [evaluation_homogeneousElement, smul_smul, ← mul_pow]
      simp

/-- For a unit `s`, `E_s` is onto (the case `d = 0` of `evaluation_image_tail`). -/
theorem evaluation_surjective {s : R} (hs : IsUnit s) :
    Function.Surjective (evaluation (R := R) (L := L) s) := by
  intro x
  obtain ⟨v, rfl⟩ := hs
  refine ⟨gradeOne (((v⁻¹ : Rˣ) : R) • x), ?_⟩
  rw [evaluation_gradeOne, smul_smul]
  simp

/-! ## The hidden cover `h̃ = ⊕_r t^r (h ∩ γ_r)` -/

variable {c : ℕ}

/-- `h̃` is exactly the set of Rees currents all of whose coefficients lie in
`h`; this is the graded description `⊕_r t^r (h ∩ γ_r)`, since each
coefficient already lies in `γ_r`. -/
theorem mem_hiddenCover_iff_coeff (hnil : lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det) (z : rees (R := R) (L := L)) :
    z ∈ hiddenCover h points ↔ ∀ r, coeff (z : Current R L) r ∈ h := by
  rw [mem_hiddenCover_iff hnil h points invertible]
  constructor
  · intro hz r
    rcases Nat.eq_zero_or_pos r with rfl | hr
    · rw [(mem_rees_iff (z : Current R L)).mp z.property |>.1]
      exact h.zero_mem
    · by_cases hrc : r ≤ c
      · have := hz ⟨r - 1, by omega⟩
        simpa [positiveCoefficients, show r - 1 + 1 = r by omega] using this
      · rw [(nilpotent_cutoff c hnil).1 _ z.property r (by omega)]
        exact h.zero_mem
  · intro hz i
    exact hz _

theorem mem_hiddenCover_iff_graded (hnil : lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det) (z : rees (R := R) (L := L)) :
    z ∈ hiddenCover h points ↔
      ∀ r, coeff (z : Current R L) r ∈ h.toSubmodule ⊓ (gamma R L r).toSubmodule := by
  rw [mem_hiddenCover_iff_coeff hnil h points invertible]
  exact forall_congr' fun r =>
    ⟨fun hr => ⟨hr, (mem_rees_iff (z : Current R L)).mp z.property |>.2 r⟩, fun hr => hr.1⟩

/-- `h̃ = ∩_{s ∈ R} E_s^{-1}(h)`: the `c` interpolation conditions already imply
the condition at every scalar, zero included. -/
theorem mem_hiddenCover_iff_forall_eval (hnil : lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det) (z : rees (R := R) (L := L)) :
    z ∈ hiddenCover h points ↔ ∀ s : R, evaluation s z ∈ h := by
  constructor
  · intro hz s
    rw [mem_hiddenCover_iff_coeff hnil h points invertible] at hz
    rw [evaluation_eq_sum s z subset_rfl]
    exact h.toSubmodule.sum_mem fun r _ => h.toSubmodule.smul_mem _ (hz r)
  · exact fun hz i => hz (points i)

/-- The hidden cover does not depend on the choice of admissible points. -/
theorem hiddenCover_eq (hnil : lowerCentralSeries R L L c = ⊥) (h : LieSubalgebra R L)
    (points points' : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det)
    (invertible' : IsUnit (evaluationMatrix points').det) :
    hiddenCover h points = hiddenCover h points' := by
  ext z
  rw [mem_hiddenCover_iff_forall_eval hnil h points invertible,
    mem_hiddenCover_iff_forall_eval hnil h points' invertible']

/-- `h̃` maps into `h` under every evaluation, and onto `h` under a unit one:
`E_s(h̃) = h`. -/
theorem evaluation_image_hiddenCover (hnil : lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det) {s : R} (hs : IsUnit s) :
    (evaluation s) '' (hiddenCover h points : Set (rees (R := R) (L := L))) =
      (h : Set L) := by
  ext x
  constructor
  · rintro ⟨z, hz, rfl⟩
    exact (mem_hiddenCover_iff_forall_eval hnil h points invertible z).mp hz s
  · intro hx
    obtain ⟨v, rfl⟩ := hs
    refine ⟨gradeOne (((v⁻¹ : Rˣ) : R) • x), ?_, ?_⟩
    · intro i
      rw [evaluation_gradeOne]
      exact h.smul_mem _ (h.smul_mem _ hx)
    · rw [evaluation_gradeOne, smul_smul]
      simp

/-- Grade one of `h̃` is exactly `h` (no `h ∩ γ_2` loss in degree one). -/
theorem gradeOne_mem_hiddenCover_iff (hnil : lowerCentralSeries R L L c = ⊥)
    (h : LieSubalgebra R L) (points : Fin c → R)
    (invertible : IsUnit (evaluationMatrix points).det) (x : L) :
    gradeOne (R := R) x ∈ hiddenCover h points ↔ x ∈ h := by
  rw [mem_hiddenCover_iff_forall_eval hnil h points invertible]
  constructor
  · intro hx
    simpa [evaluation_gradeOne] using hx 1
  · intro hx s
    rw [evaluation_gradeOne]
    exact h.smul_mem s hx

/-! ## Fields: any `c` distinct nonzero points -/

section Field

variable {F V : Type*} [Field F] [LieRing V] [LieAlgebra F V]

theorem field_points_isUnit (points : Fin c → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) : IsUnit (evaluationMatrix points).det :=
  isUnit_iff_ne_zero.mpr (evaluation_det_ne_zero points distinct nonzero)

/-- Over a field, for ANY `c` distinct nonzero points, `∩_i E_{s_i}^{-1}(h)` is
the same subalgebra `⊕_r t^r (h ∩ γ_r) = ∩_{s ≠ 0} E_s^{-1}(h)`. -/
theorem field_hiddenCover_mem_iff (hnil : lowerCentralSeries F V V c = ⊥)
    (h : LieSubalgebra F V) (points : Fin c → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (z : rees (R := F) (L := V)) :
    z ∈ hiddenCover h points ↔ ∀ s : F, s ≠ 0 → evaluation s z ∈ h := by
  have hu := field_points_isUnit points distinct nonzero
  constructor
  · intro hz s _
    exact (mem_hiddenCover_iff_forall_eval hnil h points hu z).mp hz s
  · exact fun hz i => hz (points i) (nonzero i)

theorem field_hiddenCover_eq (hnil : lowerCentralSeries F V V c = ⊥)
    (h : LieSubalgebra F V) (points points' : Fin c → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (distinct' : Function.Injective points') (nonzero' : ∀ i, points' i ≠ 0) :
    hiddenCover h points = hiddenCover h points' :=
  hiddenCover_eq hnil h points points' (field_points_isUnit points distinct nonzero)
    (field_points_isUnit points' distinct' nonzero')

end Field

end
end QSearch.ReesGeneralCover
