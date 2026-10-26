import Formal.CosetSourceFourier
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Tactic

/-!
# Class-three normal-source monomial action

Universal structure-map algebra, not a finite fixture. The central character
has already been applied, so gamma and delta are scalar-valued. No nonzero
character, positive B dimension, irreducibility, or desired action law is
assumed. This does not formalize the ambient filtration, full-jet compiler,
SDE backend or complete HSP algorithm.
-/

namespace QSearch.ClassThreeMonomial

noncomputable section
open scoped BigOperators
attribute [local instance] Classical.propDecidable

variable {F A B : Type*} [Field F] [AddCommGroup A] [Module F A]
  [AddCommGroup B] [Module F B]

structure StructureMaps (F A B : Type*) [Field F] [AddCommGroup A] [Module F A]
    [AddCommGroup B] [Module F B] where
  beta : A →ₗ[F] A →ₗ[F] B
  gamma : A →ₗ[F] A →ₗ[F] F
  delta : A →ₗ[F] B →ₗ[F] F
  beta_alt : ∀ a, beta a a = 0
  gamma_alt : ∀ a, gamma a a = 0
  jacobi : ∀ a b x, delta a (beta b x) + delta b (beta x a) + delta x (beta a b) = 0

variable (S : StructureMaps F A B)

theorem beta_skew (a b : A) : S.beta a b = -S.beta b a := by
  apply eq_neg_iff_add_eq_zero.mpr
  have h := S.beta_alt (a + b)
  simpa only [map_add, LinearMap.add_apply, S.beta_alt, zero_add, add_zero, add_comm] using h

theorem gamma_skew (a b : A) : S.gamma a b = -S.gamma b a := by
  apply eq_neg_iff_add_eq_zero.mpr
  have h := S.gamma_alt (a + b)
  simpa only [map_add, LinearMap.add_apply, S.gamma_alt, zero_add, add_zero, add_comm] using h

abbrev Element (F A B : Type*) := A × B × F
abbrev Carrier (F A B : Type*) [Field F] [AddCommGroup B] [Module F B] :=
  A × (B →ₗ[F] F)

def product (g h : Element F A B) : Element F A B :=
  (g.1 + h.1,
   g.2.1 + h.2.1 + (2 : F)⁻¹ • S.beta g.1 h.1,
   g.2.2 + h.2.2 + (S.gamma g.1 h.1 + S.delta g.1 h.2.1 - S.delta h.1 g.2.1) / 2
     + (S.delta g.1 (S.beta g.1 h.1) - S.delta h.1 (S.beta g.1 h.1)) / 12)

def displacement (g : Element F A B) (t : Carrier F A B) : Carrier F A B :=
  (t.1 + g.1, t.2 + (2 : F)⁻¹ • S.delta g.1)

def rawPhase (g : Element F A B) (x : A) : F :=
  g.2.2 + (S.gamma g.1 x - S.delta x g.2.1) / 2
    + (S.delta g.1 (S.beta g.1 x) - S.delta x (S.beta g.1 x)) / 12

def phase (g : Element F A B) (t : Carrier F A B) : F :=
  rawPhase S g t.1
    - (t.2 + (2 : F)⁻¹ • S.delta g.1) (g.2.1 + (2 : F)⁻¹ • S.beta g.1 t.1)

theorem displacement_comp (g h : Element F A B) (t : Carrier F A B) :
    displacement S g (displacement S h t) = displacement S (product S g h) t := by
  apply Prod.ext
  · simp only [displacement, product]
    abel
  · simp only [displacement, product, map_add, smul_add]
    abel

/-- The phase equation for W(g)W(h)=W(g*h), derived rather than assumed. -/
theorem phase_comp (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
    (g h : Element F A B) (t : Carrier F A B) :
    phase S h t + phase S g (displacement S h t) = phase S (product S g h) t := by
  have hj := S.jacobi g.1 h.1 t.1
  have hxa := beta_skew S t.1 g.1
  simp only [hxa, map_neg] at hj
  have h6 : (6 : F) ≠ 0 := by
    rw [show (6 : F) = 2 * 3 by ring]
    exact mul_ne_zero h2 h3
  have h12 : (12 : F) ≠ 0 := by
    rw [show (12 : F) = 2 * 2 * 3 by ring]
    exact mul_ne_zero (mul_ne_zero h2 h2) h3
  simp only [phase, rawPhase, displacement, product, map_add, map_smul,
    LinearMap.add_apply, LinearMap.smul_apply, smul_eq_mul]
  linear_combination (norm := skip) (1 / 6 : F) * hj
  field_simp [h2, h6, h12]
  ring

theorem product_assoc (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
    (g h k : Element F A B) :
    product S (product S g h) k = product S g (product S h k) := by
  apply Prod.ext
  · simp only [product]
    abel
  apply Prod.ext
  · simp only [product, map_add, LinearMap.add_apply, smul_add]
    module
  have hj := S.jacobi g.1 h.1 k.1
  have hka := beta_skew S k.1 g.1
  simp only [hka, map_neg] at hj
  have h6 : (6 : F) ≠ 0 := by
    rw [show (6 : F) = 2 * 3 by ring]
    exact mul_ne_zero h2 h3
  have h12 : (12 : F) ≠ 0 := by
    rw [show (12 : F) = 2 * 2 * 3 by ring]
    exact mul_ne_zero (mul_ne_zero h2 h2) h3
  simp only [product, map_add, map_smul, LinearMap.add_apply, smul_eq_mul]
  linear_combination (norm := skip) (-1 / 6 : F) * hj
  field_simp [h2, h6, h12]
  ring

theorem product_zero_left (g : Element F A B) : product S 0 g = g := by
  simp [product]

theorem product_zero_right (g : Element F A B) : product S g 0 = g := by
  simp [product]

theorem product_neg_left (g : Element F A B) : product S (-g) g = 0 := by
  simp [product, S.beta_alt, S.gamma_alt]

theorem product_neg_right (g : Element F A B) : product S g (-g) = 0 := by
  simp [product, S.beta_alt, S.gamma_alt]

theorem displacement_bijective (g : Element F A B) :
    Function.Bijective (displacement S g) := by
  change Function.Bijective (fun t : Carrier F A B => t + (g.1, (2 : F)⁻¹ • S.delta g.1))
  exact (Equiv.addRight _).bijective

theorem phase_zero (t : Carrier F A B) : phase S 0 t = 0 := by
  simp [phase, rawPhase]

theorem phase_inverse (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
    (g : Element F A B) (t : Carrier F A B) :
    phase S (-g) (displacement S g t) = -phase S g t := by
  have h := phase_comp S h2 h3 (-g) g t
  rw [product_neg_left, phase_zero] at h
  exact eq_neg_of_add_eq_zero_right h

theorem amplitude_comp (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
    (χ : AddChar F ℂ) (g h : Element F A B) (t : Carrier F A B) :
    χ (phase S h t) * χ (phase S g (displacement S h t)) =
      χ (phase S (product S g h) t) := by
  rw [← χ.map_add_eq_mul, phase_comp S h2 h3]

def parameterLinear (t : Carrier F A B) : Element F A B →ₗ[F] F where
  toFun g := g.2.2 - t.2 g.2.1
    + (S.gamma g.1 t.1 - S.delta t.1 g.2.1 - t.2 (S.beta g.1 t.1)) / 2
    - S.delta t.1 (S.beta g.1 t.1) / 12
  map_add' g h := by simp; ring
  map_smul' r g := by simp; ring

def parameterQuadratic (t : Carrier F A B) :
    Element F A B →ₗ[F] Element F A B →ₗ[F] F := by
  refine LinearMap.mk₂ F (fun g h =>
    -S.delta g.1 h.2.1 / 2 - S.delta g.1 (S.beta h.1 t.1) / 6) ?_ ?_ ?_ ?_
  · intro g h k
    simp
    ring
  · intro r g h
    simp
    ring
  · intro g h k
    simp
    ring
  · intro r g h
    simp
    ring

/-- A bundled degree certificate in the unknown group parameters: linear
plus diagonal bilinear evaluation. It is not inferred from scaling tests. -/
theorem quadratic_parameter_decomposition (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0)
    (g : Element F A B) (t : Carrier F A B) :
    phase S g t = parameterLinear S t g + parameterQuadratic S t g g := by
  have h6 : (6 : F) ≠ 0 := by
    rw [show (6 : F) = 2 * 3 by ring]
    exact mul_ne_zero h2 h3
  have h12 : (12 : F) ≠ 0 := by
    rw [show (12 : F) = 2 * 2 * 3 by ring]
    exact mul_ne_zero (mul_ne_zero h2 h2) h3
  simp only [phase, rawPhase, parameterLinear, parameterQuadratic, LinearMap.mk₂_apply,
    LinearMap.coe_mk, AddHom.coe_mk, map_add, map_smul, LinearMap.add_apply,
    LinearMap.smul_apply, smul_eq_mul]
  field_simp [h2, h6, h12]
  ring

section Fourier

variable {C : Type*} [AddCommGroup C] [Fintype C]

/-- Actual two-sum matrix contraction F_- W F_-^dag on the B register. -/
def partialFourierEntry (α : ℂ) (ell mu nu : AddChar C ℂ) (d : C) : ℂ :=
  QSearch.AffineSupportErasure.invSize C *
    ∑ y, ∑ z, star (nu z) * (if z = y + d then α * ell y else 0) * mu y

/-- Negative Fourier turns modulation into a POSITIVE frequency shift and
adds the phase at the shifted frequency, not at the old one. -/
theorem partial_fourier_identity (α : ℂ) (ell mu nu : AddChar C ℂ)
    (hunit : ∀ y, nu y * star (nu y) = 1) (d : C) :
    partialFourierEntry α ell mu nu d =
      if nu = mu + ell then α * star (nu d) else 0 := by
  classical
  have hstar (y : C) : star (nu y) = nu (-y) := by
    rw [nu.map_neg_eq_inv]
    exact eq_inv_of_mul_eq_one_right (hunit y)
  have point (y : C) : star (nu (y + d)) * (α * ell y) * mu y =
      (α * star (nu d)) * ((ell + mu - nu) y) := by
    rw [nu.map_add_eq_mul, star_mul]
    simp only [AddChar.sub_apply, AddChar.add_apply]
    rw [← hstar y]
    ring
  have hz : ell + mu - nu = 0 ↔ nu = mu + ell := by
    constructor
    · intro h
      exact (sub_eq_zero.mp h).symm.trans (add_comm ell mu)
    · intro h
      apply sub_eq_zero.mpr
      simpa only [add_comm] using h.symm
  unfold partialFourierEntry
  simp only [mul_ite, ite_mul, mul_zero, zero_mul, Finset.sum_ite_eq',
    Finset.mem_univ, ite_true]
  simp_rw [point]
  rw [← Finset.mul_sum, AddChar.sum_eq_ite]
  by_cases h : nu = mu + ell
  · rw [ite_eq_left (hz.mpr h), ite_eq_left h]
    have hcard : (Fintype.card C : ℂ) ≠ 0 := by
      exact_mod_cast Fintype.card_ne_zero
    simp only [QSearch.AffineSupportErasure.invSize]
    field_simp
  · rw [ite_eq_right (fun heq => h (hz.mp heq)), ite_eq_right h]
    ring

end Fourier

/-- info: 'QSearch.ClassThreeMonomial.product_assoc' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.product_assoc

/-- info: 'QSearch.ClassThreeMonomial.phase_comp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.phase_comp

/-- info: 'QSearch.ClassThreeMonomial.displacement_bijective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.displacement_bijective

/-- info: 'QSearch.ClassThreeMonomial.phase_inverse' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.phase_inverse

/-- info: 'QSearch.ClassThreeMonomial.amplitude_comp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.amplitude_comp

/-- info: 'QSearch.ClassThreeMonomial.quadratic_parameter_decomposition' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.quadratic_parameter_decomposition

/-- info: 'QSearch.ClassThreeMonomial.partial_fourier_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreeMonomial.partial_fourier_identity

end
end QSearch.ClassThreeMonomial
