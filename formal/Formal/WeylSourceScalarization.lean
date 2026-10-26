import Formal.AffineSupportErasure

/-!
# Matrix-source scalarization by spectator measurement

Start from the normalized matrix kernel with monomial gauges W(q), and
derive the spectator measurement branch from its two Kraus sums. Affine
X displacement with constant spectator coordinates gives the fixed graph
support required by AffineSupportErasure. The phases are arbitrary, not
assumed polynomial or supplied to the controller.

This does not prove that a group QFT produces the input kernel, synthesize
the alignment Clifford, prove polynomial degree/cancellation, or certify
the complete HSP algorithm. Definitions are finite mathematical kernels,
not an executable quantum implementation.
-/

namespace QSearch.WeylSourceScalarization

open scoped BigOperators
open QSearch.AffineSupportErasure
noncomputable section
attribute [local instance] Classical.propDecidable

section Monomial
variable {Q C : Type*} [AddCommGroup C] [Fintype C]

/-- W(q)|t> = gamma(q,t)|A(q)+t>. For symmetric Weyl gauges,
gamma(q,t)=omega^(psi(q)+A(q).B(q)/2+B(q).t). -/
def gaugeEntry (A : Q → C) (gamma : Q → C → ℂ) (q : Q) (r t : C) : ℂ :=
  if r = A q + t then gamma q t else 0

def gaugeKernel (A : Q → C) (gamma : Q → C → ℂ)
    (q q' : Q) (t t' : C) : ℂ :=
  ∑ r, star (gaugeEntry A gamma q r t) * gaugeEntry A gamma q' r t'

theorem gauge_kernel_identity (A : Q → C) (gamma : Q → C → ℂ)
    (q q' : Q) (t t' : C) :
    gaugeKernel A gamma q q' t t' =
      if A q + t = A q' + t' then star (gamma q t) * gamma q' t' else 0 := by
  classical
  by_cases h : A q + t = A q' + t'
  · simp [gaugeKernel, gaugeEntry, apply_ite, h, ite_mul]
  · have h' : A q' + t' ≠ A q + t := Ne.symm h
    simp [gaugeKernel, gaugeEntry, apply_ite, h, h', ite_mul]

theorem gauge_isometry (A : Q → C) (gamma : Q → C → ℂ)
    (hunit : ∀ q t, gamma q t * star (gamma q t) = 1)
    (q : Q) (t t' : C) :
    gaugeKernel A gamma q q t t' = if t = t' then 1 else 0 := by
  rw [gauge_kernel_identity]
  by_cases h : t = t'
  · subst t'
    simpa [mul_comm] using hunit q t
  · simp [h]
end Monomial

section Source
variable {F Q C : Type*} [Field F] [AddCommGroup Q] [Module F Q]
  [Fintype Q] [AddCommGroup C] [Fintype C]

def matrixSource (U : Submodule F Q) (A : Q → C) (gamma : Q → C → ℂ)
    (x x' : Q × C) : ℂ :=
  if x.1 - x'.1 ∈ U then
    invSize Q * invSize C * gaugeKernel A gamma x.1 x'.1 x.2 x'.2
  else 0

/-- Full readout preserves only U intersect ker T, even when T is not
injective on the entire quotient. Affine constants do not repair this. -/
theorem full_carrier_support [Module F C] (U : Submodule F Q)
    (T : Q →ₗ[F] C) (a : C) (gamma : Q → C → ℂ) (q q' : Q) (t : C) :
    matrixSource U (fun x => a + T x) gamma (q, t) (q', t) =
      invSize C * rho (U ⊓ LinearMap.ker T) (fun x => star (gamma x t)) q q' := by
  have same : (a + T q) + t = (a + T q') + t ↔ T (q - q') = 0 := by
    simp [map_sub, sub_eq_zero]
  simp only [matrixSource, gauge_kernel_identity, same, rho,
    Submodule.mem_inf, LinearMap.mem_ker, star_star]
  by_cases hu : q - q' ∈ U <;> by_cases ht : T (q - q') = 0 <;>
    simp_all [mul_assoc, mul_left_comm]

/-- Measuring all carrier coordinates destroys all quotient coherence when
the X displacement is injective. This is not the spectator instrument. -/
theorem full_carrier_measurement_dephases (U : Submodule F Q)
    (A : Q → C) (hinj : Function.Injective A) (gamma : Q → C → ℂ)
    (hunit : ∀ q t, gamma q t * star (gamma q t) = 1)
    (q q' : Q) (t : C) :
    matrixSource U A gamma (q, t) (q', t) =
      if q = q' then invSize Q * invSize C else 0 := by
  by_cases h : q = q'
  · subst q'
    simp [matrixSource, gauge_isometry A gamma hunit]
  · have ha : A q ≠ A q' := fun heq => h (hinj heq)
    simp [matrixSource, gauge_kernel_identity, h, ha]
end Source

section Spectator
variable {F Q J S : Type*} [Field F] [AddCommGroup Q] [Module F Q]
  [AddCommGroup J] [Module F J] [AddCommGroup S]
  [Fintype Q] [Fintype J] [Fintype S]

def graphSupport (U : Submodule F Q) (T : Q →ₗ[F] J) : Submodule F (Q × J) where
  carrier := {x | x.1 ∈ U ∧ T x.1 + x.2 = 0}
  zero_mem' := by simp
  add_mem' := by
    intro x y hx hy
    refine ⟨U.add_mem hx.1 hy.1, ?_⟩
    change T (x.1 + y.1) + (x.2 + y.2) = 0
    calc
      _ = (T x.1 + x.2) + (T y.1 + y.2) := by rw [map_add]; abel
      _ = 0 := by rw [hx.2, hy.2, add_zero]
  smul_mem' := by
    intro c x hx
    refine ⟨U.smul_mem c hx.1, ?_⟩
    change T (c • x.1) + c • x.2 = 0
    rw [map_smul, ← smul_add, hx.2, smul_zero]

def affineDisplacement (T : Q →ₗ[F] J) (a : J) (b : S) (q : Q) : J × S :=
  (a + T q, b)

def scalarPhase (gamma : Q → (J × S) → ℂ) (s : S) (x : Q × J) : ℂ :=
  star (gamma x.1 (x.2, s))

def measurementKraus (s : S) (x : Q × J) (u : Q × (J × S)) : ℂ :=
  if u = (x.1, (x.2, s)) then 1 else 0

def spectatorBranch (U : Submodule F Q) (A : Q → J × S)
    (gamma : Q → (J × S) → ℂ) (s : S) (x x' : Q × J) : ℂ :=
  ∑ u, ∑ v, measurementKraus s x u * matrixSource U A gamma u v
    * star (measurementKraus s x' v)

omit [Module F J] in
theorem spectator_pullback (U : Submodule F Q) (A : Q → J × S)
    (gamma : Q → (J × S) → ℂ) (s : S) (x x' : Q × J) :
    spectatorBranch U A gamma s x x' =
      matrixSource U A gamma (x.1, (x.2, s)) (x'.1, (x'.2, s)) := by
  classical
  simp [spectatorBranch, measurementKraus, ite_mul, mul_ite]

omit [Fintype Q] [Fintype J] [Fintype S] in
theorem affine_support_iff (T : Q →ₗ[F] J) (a : J) (b s : S)
    (x x' : Q × J) :
    affineDisplacement T a b x.1 + (x.2, s) =
      affineDisplacement T a b x'.1 + (x'.2, s) ↔
      T (x.1 - x'.1) + (x.2 - x'.2) = 0 := by
  have difference : T (x.1 - x'.1) + (x.2 - x'.2) =
      (T x.1 + x.2) - (T x'.1 + x'.2) := by rw [map_sub]; abel
  rw [difference, sub_eq_zero]
  simp [affineDisplacement, add_assoc]

/-- Every spectator outcome produces the same hidden graph support. The
equality is derived from W(q)^dagger W(q') and K_s rho K_s^dagger. -/
theorem matrix_source_to_scalar (U : Submodule F Q) (T : Q →ₗ[F] J)
    (a : J) (b : S) (gamma : Q → (J × S) → ℂ)
    (s : S) (x x' : Q × J) :
    spectatorBranch U (affineDisplacement T a b) gamma s x x' =
      invSize S * rho (graphSupport U T) (scalarPhase gamma s) x x' := by
  rw [spectator_pullback]
  have normalization : invSize Q * invSize (J × S) =
      invSize S * invSize (Q × J) := by
    simp only [invSize, Fintype.card_prod, Nat.cast_mul, mul_inv_rev]
    ring
  simp only [matrixSource, gauge_kernel_identity, affine_support_iff,
    rho, graphSupport, Submodule.mem_mk, scalarPhase, star_star]
  by_cases hu : x.1 - x'.1 ∈ U <;>
    by_cases ht : T (x.1 - x'.1) + (x.2 - x'.2) = 0 <;>
    simp_all [mul_assoc]

/-- A spectator with nonconstant affine displacement leaks Lq. The branch
still normalizes, but its support is restricted to U intersect ker L. -/
theorem matrix_source_with_leakage [Module F S] (U : Submodule F Q)
    (T : Q →ₗ[F] J) (L : Q →ₗ[F] S) (a : J) (b : S)
    (gamma : Q → (J × S) → ℂ) (s : S) (x x' : Q × J) :
    spectatorBranch U (fun q => (a + T q, b + L q)) gamma s x x' =
      invSize S * rho (graphSupport (U ⊓ LinearMap.ker L) T)
        (scalarPhase gamma s) x x' := by
  rw [spectator_pullback]
  have first : (a + T x.1) + x.2 = (a + T x'.1) + x'.2 ↔
      T (x.1 - x'.1) + (x.2 - x'.2) = 0 := by
    simpa [affineDisplacement] using affine_support_iff T a b s x x'
  have second : (b + L x.1) + s = (b + L x'.1) + s ↔
      L (x.1 - x'.1) = 0 := by simp [map_sub, sub_eq_zero]
  have normalization : invSize Q * invSize (J × S) =
      invSize S * invSize (Q × J) := by
    simp only [invSize, Fintype.card_prod, Nat.cast_mul, mul_inv_rev]
    ring
  simp only [matrixSource, gauge_kernel_identity, Prod.mk_add_mk, Prod.mk.injEq,
    first, second, rho, graphSupport, Submodule.mem_mk, Submodule.mem_inf,
    LinearMap.mem_ker, scalarPhase, star_star]
  by_cases hu : x.1 - x'.1 ∈ U <;>
    by_cases ht : T (x.1 - x'.1) + (x.2 - x'.2) = 0 <;>
    by_cases hl : L (x.1 - x'.1) = 0 <;> simp_all [mul_assoc]

omit [Fintype Q] [Fintype J] [Fintype S]
  [AddCommGroup Q] [AddCommGroup J] [AddCommGroup S] in
theorem scalar_phase_unit (gamma : Q → (J × S) → ℂ)
    (hunit : ∀ q t, gamma q t * star (gamma q t) = 1)
    (s : S) (x : Q × J) :
    scalarPhase gamma s x * star (scalarPhase gamma s x) = 1 := by
  simpa [scalarPhase, mul_comm] using hunit x.1 (x.2, s)

theorem spectator_probability (U : Submodule F Q) (T : Q →ₗ[F] J)
    (a : J) (b : S) (gamma : Q → (J × S) → ℂ)
    (hunit : ∀ q t, gamma q t * star (gamma q t) = 1) (s : S) :
    (∑ x, spectatorBranch U (affineDisplacement T a b) gamma s x x) =
      invSize S := by
  simp_rw [matrix_source_to_scalar]
  rw [← Finset.mul_sum, rho_trace_one _ _ (scalar_phase_unit gamma hunit s), mul_one]

omit [AddCommGroup Q] [AddCommGroup J] [AddCommGroup S] in
theorem spectator_complete (u v : Q × (J × S)) :
    (∑ s, ∑ x, star (measurementKraus s x u) * measurementKraus s x v) =
      if u = v then 1 else 0 := by
  classical
  rcases u with ⟨q, j, s⟩
  rcases v with ⟨q', j', s'⟩
  by_cases hq : q = q' <;> by_cases hj : j = j' <;> by_cases hs : s = s' <;>
    simp_all [measurementKraus, Fintype.sum_prod_type, ite_and, apply_ite,
      Finset.sum_ite_irrel]

end Spectator

/-- info: 'QSearch.WeylSourceScalarization.matrix_source_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.matrix_source_to_scalar

/-- info: 'QSearch.WeylSourceScalarization.matrix_source_with_leakage' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.matrix_source_with_leakage

/-- info: 'QSearch.WeylSourceScalarization.spectator_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.spectator_probability

/-- info: 'QSearch.WeylSourceScalarization.spectator_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.spectator_complete

/-- info: 'QSearch.WeylSourceScalarization.full_carrier_support' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.full_carrier_support

/-- info: 'QSearch.WeylSourceScalarization.full_carrier_measurement_dephases' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.full_carrier_measurement_dephases

/-- info: 'QSearch.WeylSourceScalarization.gauge_isometry' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.WeylSourceScalarization.gauge_isometry

end
end QSearch.WeylSourceScalarization
