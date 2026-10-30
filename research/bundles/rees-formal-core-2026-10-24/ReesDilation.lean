import ReesLie

/-!
Graded rescaling on the actual evaluation realization of the Rees cover.
This constructs Lie automorphisms; it does not assume BCH functoriality.
-/

namespace QSearch.ReesDilation
open scoped BigOperators
open LieModule
open ReesLie
noncomputable section

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] {n : ℕ}

def recoverLinear (points : Fin n → F) : (Fin n → L) →ₗ[F] (Fin n → L) where
  toFun := recover points
  map_add' x y := by ext j; simp [recover, ReesHomogenization.applyRows,
    smul_add, Finset.sum_add_distrib]
  map_smul' a x := by ext j; simp [recover, ReesHomogenization.applyRows,
    Finset.smul_sum, smul_smul, mul_comm]

def scaleCoefficients (a : F) : (Fin n → L) →ₗ[F] (Fin n → L) where
  toFun v := fun j => a ^ (j.val+1) • v j
  map_add' x y := by ext j; simp [smul_add]
  map_smul' b x := by ext j; simp [smul_smul, mul_comm]

def dilationLinear (points : Fin n → F) (a : F) :
    (Fin n → L) →ₗ[F] (Fin n → L) :=
  (evaluate points).comp ((scaleCoefficients a).comp (recoverLinear points))

theorem dilation_evaluate (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (a : F) (v : Fin n → L) :
    dilationLinear points a (evaluate points v) = evaluate points (scaleCoefficients a v) := by
  change evaluate points (scaleCoefficients a (recover points (evaluate points v))) = _
  rw [recover_evaluate points distinct nonzero]

theorem scale_single (a : F) (j : Fin n) (x : L) :
    scaleCoefficients a (Pi.single j x) = Pi.single j (a^(j.val+1) • x) := by
  classical
  ext k
  by_cases h : k = j
  · subst k; simp [scaleCoefficients]
  · simp [scaleCoefficients, h]

theorem dilation_monomial (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (a : F) (j : Fin n) (x : L) :
    dilationLinear points a (monomial points (j.val+1) x) =
      monomial points (j.val+1) (a^(j.val+1) • x) := by
  rw [← evaluate_single points j x, dilation_evaluate points distinct nonzero,
    scale_single, evaluate_single]

theorem dilation_mem (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (a : F) {x : Fin n → L} (hx : x ∈ evaluationSpace points) :
    dilationLinear points a x ∈ evaluationSpace points := by
  obtain ⟨v, hv, rfl⟩ := hx
  rw [dilation_evaluate points distinct nonzero]
  refine ⟨scaleCoefficients a v, ?_, rfl⟩
  intro j
  exact (lowerCentralSeries F L L j.val).smul_mem _ (hv j)

theorem dilation_lie (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (a : F) {x y : Fin n → L} (hx : x ∈ evaluationSpace points)
    (hy : y ∈ evaluationSpace points) :
    dilationLinear points a ⁅x,y⁆ = ⁅dilationLinear points a x, dilationLinear points a y⁆ := by
  obtain ⟨u, hu, rfl⟩ := hx
  obtain ⟨v, hv, rfl⟩ := hy
  rw [evaluate_eq_sum, evaluate_eq_sum, sum_lie_sum, map_sum, map_sum, map_sum,
    sum_lie_sum]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro s _
  rw [dilation_monomial points distinct nonzero, dilation_monomial points distinct nonzero,
    monomial_bracket, monomial_bracket]
  have hbracket := lowerCentral_bracket r.val s.val
    (LieSubmodule.lie_mem_lie (hu r) (hv s))
  by_cases h : r.val+s.val+1 < n
  · have he : r.val+1+(s.val+1) = (⟨r.val+s.val+1,h⟩ : Fin n).val+1 := by
      change r.val+1+(s.val+1) = (r.val+s.val+1)+1
      omega
    rw [he, dilation_monomial points distinct nonzero, smul_lie, lie_smul, smul_smul]
    rw [← pow_add, he]
  · have hz := antitone_lowerCentralSeries F L L (Nat.le_of_not_gt h) hbracket
    rw [nilpotent, LieSubmodule.mem_bot] at hz
    have he : monomial points (r.val+1+(s.val+1)) (0 : L) = 0 := by
      funext j
      exact smul_zero _
    simp only [smul_lie, lie_smul, hz, smul_zero, he, map_zero]

def dilationHom (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) :
    cover points nilpotent →ₗ⁅F⁆ cover points nilpotent where
  toFun x := ⟨dilationLinear points a x.val, dilation_mem points distinct nonzero a x.property⟩
  map_add' x y := by apply Subtype.ext; exact map_add _ _ _
  map_smul' b x := by apply Subtype.ext; exact map_smul _ _ _
  map_lie' {x y} := by
    apply Subtype.ext
    exact dilation_lie points distinct nonzero nilpotent a x.property y.property

theorem recover_dilation (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (a : F) (x : Fin n → L) :
    recover points (dilationLinear points a x) = scaleCoefficients a (recover points x) := by
  exact recover_evaluate points distinct nonzero _

theorem dilation_mul (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (a b : F) (x : Fin n → L) :
    dilationLinear points a (dilationLinear points b x) = dilationLinear points (a*b) x := by
  change evaluate points (scaleCoefficients a (recover points (dilationLinear points b x))) = _
  rw [recover_dilation points distinct nonzero]
  change evaluate points (scaleCoefficients a (scaleCoefficients b (recover points x))) =
    evaluate points (scaleCoefficients (a*b) (recover points x))
  congr 1
  ext j
  simp [scaleCoefficients, smul_smul, mul_pow]

theorem dilation_one (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    {x : Fin n → L} (hx : x ∈ evaluationSpace points) : dilationLinear points 1 x = x := by
  change evaluate points (scaleCoefficients 1 (recover points x)) = x
  have hs : scaleCoefficients (1 : F) (recover points x) = recover points x := by
    ext j; simp [scaleCoefficients]
  rw [hs, evaluate_recover points distinct nonzero hx]

def dilationEquiv (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) (ha : a ≠ 0) :
    cover points nilpotent ≃ₗ⁅F⁆ cover points nilpotent :=
  { dilationHom points distinct nonzero nilpotent a with
    invFun := dilationHom points distinct nonzero nilpotent a⁻¹
    left_inv := by
      intro x
      apply Subtype.ext
      change dilationLinear points a⁻¹ (dilationLinear points a x.val) = x.val
      rw [dilation_mul points distinct nonzero, inv_mul_cancel₀ ha]
      exact dilation_one points distinct nonzero x.property
    right_inv := by
      intro x
      apply Subtype.ext
      change dilationLinear points a (dilationLinear points a⁻¹ x.val) = x.val
      rw [dilation_mul points distinct nonzero, mul_inv_cancel₀ ha]
      exact dilation_one points distinct nonzero x.property }

theorem dilation_hidden_membership_iff (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (a : F) (ha : a ≠ 0)
    (h : Submodule F L) (x : cover points nilpotent) :
    (∀ i, evaluationHom points nilpotent i
      (dilationEquiv points distinct nonzero nilpotent a ha x) ∈ h) ↔
    ∀ i, evaluationHom points nilpotent i x ∈ h := by
  rw [cover_membership_iff points distinct nonzero, cover_membership_iff points distinct nonzero]
  change (∀ j, recover points (dilationLinear points a x.val) j ∈ h) ↔ _
  rw [recover_dilation points distinct nonzero]
  exact ReesHomogenization.dilation_membership_iff h a ha _

theorem dilation_zero (points : Fin n → F) (x : Fin n → L) :
    dilationLinear points 0 x = 0 := by
  change evaluate points (scaleCoefficients 0 (recover points x)) = 0
  have hs : scaleCoefficients (0 : F) (recover points x) = 0 := by
    ext j; simp [scaleCoefficients]
  rw [hs, map_zero]

theorem highest_monomial_central (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (j : Fin n) (highest : j.val+1 = n) (v : L)
    (hv : v ∈ lowerCentralSeries F L L j.val) (y : Fin n → L) :
    ⁅monomial points n v,y⁆ = 0 := by
  funext k
  change ⁅points k ^ n • v,y k⁆ = 0
  rw [smul_lie]
  have hy : y k ∈ lowerCentralSeries F L L 0 := by simp [lowerCentralSeries_zero]
  have hz := lowerCentral_bracket j.val 0 (LieSubmodule.lie_mem_lie hv hy)
  simp only [Nat.add_zero, highest, nilpotent, LieSubmodule.mem_bot] at hz
  rw [hz, smul_zero]

theorem dilation_highest_grade (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (j : Fin n) (highest : j.val+1 = n) (a : F) (v : L) :
    dilationLinear points a (monomial points n v) = a^n • monomial points n v := by
  have he := dilation_monomial points distinct nonzero a j v
  rw [highest] at he
  rw [he]
  funext k
  simp [monomial, smul_smul, mul_comm]

/-- Uniform scalar multiplication is not the graded automorphism. -/
theorem uniform_scaling_obstruction (a : F) (nonzero : a ≠ 0) (not_one : a ≠ 1)
    (x y : L) (noncommuting : ⁅x,y⁆ ≠ 0) : a • ⁅x,y⁆ ≠ ⁅a • x,a • y⁆ := by
  intro he
  rw [smul_lie, lie_smul, smul_smul] at he
  have hscalar := smul_left_injective F noncommuting he
  have hz : a*(1-a) = 0 := by
    calc
      a*(1-a) = a-a*a := by ring
      _ = 0 := sub_eq_zero.mpr hscalar
  rcases mul_eq_zero.mp hz with h | h
  · exact nonzero h
  · exact not_one (sub_eq_zero.mp h).symm

end
end QSearch.ReesDilation
