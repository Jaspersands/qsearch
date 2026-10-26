import Formal.WeylSourceScalarization
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.BigOperators.Ring.Finset

/-!
# Matrix-valued common-support batch shear

Evaluate the full Kraus sums for independent matrix sources with arbitrary
finite carrier dimensions. The fresh uniform quotient register is part of
the Kraus operator. No unknown support, gauge or polynomial coefficient is
an operational input. Independence is a premise, not a consequence of
correct single-source marginals.

This does not synthesize the alignment Clifford, prove degree cancellation,
or certify the full HSP algorithm. The kernels are mathematical objects,
not an executable state-table implementation.
-/

namespace QSearch.MatrixBatchShear

open scoped BigOperators
open QSearch.AffineSupportErasure (invSize uniformAmplitude affinePoint)
noncomputable section
attribute [local instance] Classical.propDecidable

section Kernel
variable {Q C : Type*} [Fintype C]

def gaugeKernel (W : Q → Matrix C C ℂ) (q q' : Q) (a b : C) : ℂ :=
  ∑ r, star (W q r a) * W q' r b

theorem gauge_matrix_product (W : Q → Matrix C C ℂ) (q q' : Q) (a b : C) :
    gaugeKernel W q q' a b = ((W q).conjTranspose * W q') a b := by
  rfl
end Kernel

section Source
variable {F Q C : Type*} [Field F] [AddCommGroup Q] [Module F Q]
  [Fintype Q] [Fintype C]

def matrixSource (U : Submodule F Q) (W : Q → Matrix C C ℂ)
    (x x' : Q × C) : ℂ :=
  if x.1 - x'.1 ∈ U then
    invSize Q * invSize C * gaugeKernel W x.1 x'.1 x.2 x'.2
  else 0

theorem monomial_source [AddCommGroup C] (U : Submodule F Q)
    (A : Q → C) (gamma : Q → C → ℂ) (x x' : Q × C) :
    matrixSource U (QSearch.WeylSourceScalarization.gaugeEntry A gamma) x x' =
      QSearch.WeylSourceScalarization.matrixSource U A gamma x x' := by
  rfl

theorem source_trace_one [Nonempty C] (U : Submodule F Q) (W : Q → Matrix C C ℂ)
    (hunit : ∀ q a, gaugeKernel W q q a a = 1) :
    (∑ x, matrixSource U W x x) = 1 := by
  have hq : (Fintype.card Q : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have hc : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [matrixSource, hunit, invSize]
  field_simp

variable [DecidableEq C]

def carrierConjugation (U : Submodule F Q) (W : Q → Matrix C C ℂ)
    (S : Matrix C C ℂ) (x x' : Q × C) : ℂ :=
  ∑ a, ∑ b, S x.2 a * matrixSource U W (x.1, a) (x'.1, b) * star (S x'.2 b)

omit [AddCommGroup Q] [Fintype Q] in
theorem gauge_covariance (W : Q → Matrix C C ℂ) (S : Matrix C C ℂ)
    (hS : S.conjTranspose * S = 1) (q q' : Q) :
    (S * W q * S.conjTranspose).conjTranspose * (S * W q' * S.conjTranspose) =
      S * ((W q).conjTranspose * W q') * S.conjTranspose := by
  simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose]
  calc
    _ = S * (W q).conjTranspose * (S.conjTranspose * S) * W q' * S.conjTranspose := by
      noncomm_ring
    _ = _ := by rw [hS]; noncomm_ring

omit [AddCommGroup Q] [Fintype Q] in
theorem gauge_covariance_entry (W : Q → Matrix C C ℂ) (S : Matrix C C ℂ)
    (hS : S.conjTranspose * S = 1) (q q' : Q) (a b : C) :
    gaugeKernel (fun x => S * W x * S.conjTranspose) q q' a b =
      ∑ r, ∑ t, S a r * gaugeKernel W q q' r t * star (S b t) := by
  rw [gauge_matrix_product, gauge_covariance W S hS]
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, Finset.sum_mul]
  rw [Finset.sum_comm]
  rfl

/-- Physical carrier conjugation is represented by conjugating every gauge.
S is independent of q. This does not prove a claimed symplectic formula. -/
theorem carrier_conjugation_identity (U : Submodule F Q) (W : Q → Matrix C C ℂ)
    (S : Matrix C C ℂ) (hS : S.conjTranspose * S = 1) (x x' : Q × C) :
    carrierConjugation U W S x x' =
      matrixSource U (fun q => S * W q * S.conjTranspose) x x' := by
  by_cases h : x.1 - x'.1 ∈ U
  · simp only [carrierConjugation, matrixSource, h, ite_true]
    rw [gauge_covariance_entry W S hS]
    simp only [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro b _
    ring
  · simp [carrierConjugation, matrixSource, h]
end Source

section ScalarBridge
variable {F Q J T : Type*} [Field F] [AddCommGroup Q] [Module F Q]
  [AddCommGroup J] [Module F J] [AddCommGroup T]
  [Fintype Q] [Fintype J] [Fintype T]

/-- Compose physical carrier conjugation and spectator Kraus sums. The
exact aligned-gauge identity is a premise, not inferred from rank alone. -/
theorem conjugation_to_scalar (U : Submodule F Q) (W : Q → Matrix (J × T) (J × T) ℂ)
    (S : Matrix (J × T) (J × T) ℂ) (hS : S.conjTranspose * S = 1)
    (L : Q →ₗ[F] J) (a : J) (b : T) (gamma : Q → (J × T) → ℂ)
    (hmono : ∀ q, S * W q * S.conjTranspose =
      QSearch.WeylSourceScalarization.gaugeEntry
        (QSearch.WeylSourceScalarization.affineDisplacement L a b) gamma q)
    (s : T) (x x' : Q × J) :
    (∑ u, ∑ v, QSearch.WeylSourceScalarization.measurementKraus s x u *
      carrierConjugation U W S u v *
        star (QSearch.WeylSourceScalarization.measurementKraus s x' v)) =
      invSize T * QSearch.AffineSupportErasure.rho
        (QSearch.WeylSourceScalarization.graphSupport U L)
        (QSearch.WeylSourceScalarization.scalarPhase gamma s) x x' := by
  simp_rw [carrier_conjugation_identity U W S hS]
  have hg : (fun q => S * W q * S.conjTranspose) =
      QSearch.WeylSourceScalarization.gaugeEntry
        (QSearch.WeylSourceScalarization.affineDisplacement L a b) gamma := funext hmono
  rw [hg]
  simp_rw [monomial_source]
  exact QSearch.WeylSourceScalarization.matrix_source_to_scalar U L a b gamma s x x'
end ScalarBridge

section Tensor
variable {F Q I : Type*} [Field F] [AddCommGroup Q] [Module F Q]
  [Fintype Q] [Fintype I] {C : I → Type*} [∀ i, Fintype (C i)]

def tensorSource (U : Submodule F Q) (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (x x' : (I → Q) × (∀ i, C i)) : ℂ :=
  ∏ i, matrixSource U (W i) (x.1 i, x.2 i) (x'.1 i, x'.2 i)

def combinedGauge (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (c : I → F) (y : I → Q) (q : Q) : Matrix (∀ i, C i) (∀ i, C i) ℂ :=
  fun a b => ∏ i, W i (affinePoint c y q i) (a i) (b i)

theorem invSize_pi : invSize (∀ i, C i) = ∏ i, invSize (C i) := by
  simp [invSize, Fintype.card_pi, Nat.cast_prod, Finset.prod_inv_distrib]

omit [Fintype Q] in
theorem combined_kernel (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (c : I → F) (y : I → Q) (q q' : Q) (a b : ∀ i, C i) :
    gaugeKernel (combinedGauge W c y) q q' a b =
      ∏ i, gaugeKernel (W i) (affinePoint c y q i) (affinePoint c y q' i) (a i) (b i) := by
  simp only [gaugeKernel, combinedGauge, star_prod, ← Finset.prod_mul_distrib]
  exact (Fintype.prod_sum (fun i (r : C i) =>
    star (W i (affinePoint c y q i) r (a i)) * W i (affinePoint c y q' i) r (b i))).symm

omit [Fintype Q] in
theorem combined_isometry (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (hunit : ∀ i q a b, gaugeKernel (W i) q q a b = if a = b then 1 else 0)
    (c : I → F) (y : I → Q) (q : Q) (a b : ∀ i, C i) :
    gaugeKernel (combinedGauge W c y) q q a b = if a = b then 1 else 0 := by
  rw [combined_kernel]
  simp [hunit, Fintype.prod_ite_zero, funext_iff]

theorem tensor_pullback (U : Submodule F Q) (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (c : I → F) (y : I → Q) (hc : ∃ i, c i ≠ 0) (x x' : Q × (∀ i, C i)) :
    tensorSource U W (affinePoint c y x.1, x.2) (affinePoint c y x'.1, x'.2) =
      if x.1 - x'.1 ∈ U then invSize Q ^ Fintype.card I * invSize (∀ i, C i) *
        gaugeKernel (combinedGauge W c y) x.1 x'.1 x.2 x'.2 else 0 := by
  simp only [tensorSource, matrixSource, Fintype.prod_ite_zero,
    QSearch.AffineSupportErasure.support_iff U c y hc]
  simp [combined_kernel, invSize_pi, Finset.prod_mul_distrib]

def krausEntry (amplitude : ℂ) (c : I → F) (y : I → Q)
    (x : Q × (∀ i, C i)) (a : (I → Q) × (∀ i, C i)) : ℂ :=
  if a.2 = x.2 then
    QSearch.AffineSupportErasure.krausEntry amplitude c y x.1 a.1 else 0

def branchEntry (amplitude : ℂ) (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ) (c : I → F) (y : I → Q)
    (x x' : Q × (∀ i, C i)) : ℂ :=
  ∑ a, ∑ b, krausEntry amplitude c y x a * tensorSource U W a b
    * star (krausEntry amplitude c y x' b)

theorem branch_pullback (amplitude : ℂ) (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ) (c : I → F) (y : I → Q)
    (x x' : Q × (∀ i, C i)) :
    branchEntry amplitude U W c y x x' =
      (amplitude * star amplitude) *
        tensorSource U W (affinePoint c y x.1, x.2) (affinePoint c y x'.1, x'.2) := by
  classical
  simp [branchEntry, krausEntry, QSearch.AffineSupportErasure.krausEntry,
    Fintype.sum_prod_type, apply_ite, ite_mul]
  ring

/-- Exact branch from TWO Kraus sums. Carrier dimensions can differ, and
zero scales are allowed provided at least one scale is nonzero. -/
theorem mixed_branch_identity (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ) (c : I → F) (y : I → Q)
    (hc : ∃ i, c i ≠ 0) (x x' : Q × (∀ i, C i)) :
    branchEntry (uniformAmplitude Q) U W c y x x' =
      invSize Q ^ Fintype.card I * matrixSource U (combinedGauge W c y) x x' := by
  rw [branch_pullback, QSearch.AffineSupportErasure.uniformAmplitude_normalized,
    tensor_pullback U W c y hc]
  by_cases h : x.1 - x'.1 ∈ U
  · simp only [matrixSource, h, ite_true]
    ring
  · simp [matrixSource, h]

def alignedBranch (U : Submodule F Q) (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (c : I → F) (y : I → Q) (S : Matrix (∀ i, C i) (∀ i, C i) ℂ)
    (x x' : Q × (∀ i, C i)) : ℂ :=
  ∑ a, ∑ b, S x.2 a * branchEntry (uniformAmplitude Q) U W c y (x.1, a) (x'.1, b)
    * star (S x'.2 b)

theorem aligned_branch_identity (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ) (c : I → F) (y : I → Q)
    (hc : ∃ i, c i ≠ 0) (S : Matrix (∀ i, C i) (∀ i, C i) ℂ)
    (hS : S.conjTranspose * S = 1) (x x' : Q × (∀ i, C i)) :
    alignedBranch U W c y S x x' = invSize Q ^ Fintype.card I *
      matrixSource U (fun q => S * combinedGauge W c y q * S.conjTranspose) x x' := by
  rw [← carrier_conjugation_identity U (combinedGauge W c y) S hS]
  simp only [alignedBranch, mixed_branch_identity U W c y hc, carrierConjugation,
    Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  ring

theorem branch_probability [∀ i, Nonempty (C i)] (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (hunit : ∀ i q a b, gaugeKernel (W i) q q a b = if a = b then 1 else 0)
    (c : I → F) (y : I → Q) (hc : ∃ i, c i ≠ 0) :
    (∑ x, branchEntry (uniformAmplitude Q) U W c y x x) =
      invSize Q ^ Fintype.card I := by
  classical
  simp_rw [mixed_branch_identity U W c y hc]
  have hu : ∀ q a, gaugeKernel (combinedGauge W c y) q q a a = 1 := by
    intro q a
    simpa using combined_isometry W hunit c y q a a
  rw [← Finset.mul_sum, source_trace_one U _ hu, mul_one]

omit [Fintype Q] [Fintype I] in
/-- A zero-weight input contributes only an identity carrier kernel. Its
carrier is maximally mixed and can be discarded, but not reused as a source. -/
theorem zero_weight_kernel (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (hunit : ∀ i q a b, gaugeKernel (W i) q q a b = if a = b then 1 else 0)
    (c : I → F) (y : I → Q) (i : I) (hi : c i = 0)
    (q q' : Q) (a b : C i) :
    gaugeKernel (W i) (affinePoint c y q i) (affinePoint c y q' i) a b =
      if a = b then 1 else 0 := by
  simp [affinePoint, hi, hunit]

theorem all_zero_scale_branch (U : Submodule F Q)
    (W : ∀ i, Q → Matrix (C i) (C i) ℂ)
    (hunit : ∀ i q a b, gaugeKernel (W i) q q a b = if a = b then 1 else 0)
    (y : I → Q) (x x' : Q × (∀ i, C i)) :
    branchEntry (uniformAmplitude Q) U W (fun _ => 0) y x x' =
      invSize Q ^ Fintype.card I * invSize Q * invSize (∀ i, C i) *
        (if x.2 = x'.2 then 1 else 0) := by
  rw [branch_pullback, QSearch.AffineSupportErasure.uniformAmplitude_normalized]
  have ht : tensorSource U W (affinePoint (fun _ : I => (0 : F)) y x.1, x.2)
      (affinePoint (fun _ : I => (0 : F)) y x'.1, x'.2) =
      invSize Q ^ Fintype.card I * invSize (∀ i, C i) * (if x.2 = x'.2 then 1 else 0) := by
    simp [tensorSource, matrixSource, affinePoint, hunit, Finset.prod_mul_distrib,
      invSize_pi, Fintype.prod_ite_zero, funext_iff]
  rw [ht]
  ring

omit [Fintype Q] in
theorem kraus_carrier_sum (amplitude : ℂ) (c : I → F) (y : I → Q)
    (q : Q) (a b : (I → Q) × (∀ i, C i)) :
    (∑ t, star (krausEntry amplitude c y (q, t) a) * krausEntry amplitude c y (q, t) b) =
      if a.2 = b.2 then
        star (QSearch.AffineSupportErasure.krausEntry amplitude c y q a.1) *
          QSearch.AffineSupportErasure.krausEntry amplitude c y q b.1 else 0 := by
  classical
  by_cases h : a.2 = b.2
  · simp [krausEntry, h, apply_ite, ite_mul]
  · simp [krausEntry, h, apply_ite, ite_mul]

/-- Completeness holds even for all-zero weights and without source promises. -/
theorem kraus_complete (c : I → F) (a b : (I → Q) × (∀ i, C i)) :
    (∑ y, ∑ x, star (krausEntry (uniformAmplitude Q) c y x a) *
      krausEntry (uniformAmplitude Q) c y x b) = if a = b then 1 else 0 := by
  classical
  simp only [Fintype.sum_prod_type, kraus_carrier_sum]
  by_cases h : a.2 = b.2
  · simp only [h, ite_true]
    rw [QSearch.AffineSupportErasure.kraus_complete]
    simp [Prod.ext_iff, h]
  · have hab : a ≠ b := fun heq => h (congrArg Prod.snd heq)
    simp [h, hab]

end Tensor

/-- info: 'QSearch.MatrixBatchShear.mixed_branch_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.mixed_branch_identity

/-- info: 'QSearch.MatrixBatchShear.branch_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.branch_probability

/-- info: 'QSearch.MatrixBatchShear.kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.kraus_complete

/-- info: 'QSearch.MatrixBatchShear.all_zero_scale_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.all_zero_scale_branch

/-- info: 'QSearch.MatrixBatchShear.combined_isometry' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.combined_isometry

/-- info: 'QSearch.MatrixBatchShear.aligned_branch_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.aligned_branch_identity

/-- info: 'QSearch.MatrixBatchShear.carrier_conjugation_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.carrier_conjugation_identity

/-- info: 'QSearch.MatrixBatchShear.conjugation_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.MatrixBatchShear.conjugation_to_scalar
end
end QSearch.MatrixBatchShear
