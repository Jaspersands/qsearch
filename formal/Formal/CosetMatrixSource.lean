import Formal.CosetSourceFourier
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.Group.TypeTags.Hom

/-!
# Ordinary mixed cosets to a representation-valued kernel

The normal coordinate is a possibly nonabelian group. Starting from actual
coset membership, evaluate the conjugated Fourier sector and row trace.
The fixed-sector calculation needs a unitary representation, not a Schur
orthogonality assumption. Completeness of a full chosen QFT family remains
a separate premise before interpreting all sector traces as probabilities.

The section-word identity is group-theoretic. Polynomial degree, effective
coordinates, QFT circuits and the complete HSP algorithm are not proved.
-/

namespace QSearch.CosetMatrixSource

open scoped BigOperators
open QSearch.AffineSupportErasure
open QSearch.CosetSourceFourier (groupEntry)
noncomputable section
attribute [local instance] Classical.propDecidable

section Oracle
variable {G O : Type*} [Group G] [Fintype G] [Fintype O]

def hidingAmplitude (hidingFunction : G → O) (g : G) (y : O) : ℂ :=
  if y = hidingFunction g then uniformAmplitude G else 0

/-- Trace the ordinary hiding-output register after a uniform oracle query.
Retaining a chosen output would be a different conditional source. -/
theorem hiding_output_trace (H : Subgroup G) (hidingFunction : G → O)
    (hides : ∀ g g', hidingFunction g = hidingFunction g' ↔ g⁻¹ * g' ∈ H)
    (g g' : G) :
    (∑ y, hidingAmplitude hidingFunction g y * star (hidingAmplitude hidingFunction g' y)) =
      groupEntry H g g' := by
  classical
  by_cases h : hidingFunction g = hidingFunction g'
  · have hh := (hides g g').mp h
    simpa [hidingAmplitude, apply_ite, h, ite_mul, groupEntry, hh] using
      uniformAmplitude_normalized (V := G)
  · have hh : g⁻¹ * g' ∉ H := fun hx => h ((hides g g').mpr hx)
    simp [hidingAmplitude, apply_ite, Ne.symm h, ite_mul, groupEntry, hh]
end Oracle

section Potential
variable {F V G : Type*} [Field F] [AddCommGroup V] [Module F V] [Group G]

def sectionPotential (U : Submodule F V) (pi : V →ₗ[F] U)
    (sectionMap : V → G) (hidden : Multiplicative U →* G) (q : V) : G :=
  sectionMap (q - (pi q : V)) * hidden (Multiplicative.ofAdd (pi q)) * (sectionMap q)⁻¹

/-- This identity does not require an abelian normal subgroup or a linear
group section. The retraction and hidden homomorphism are proof witnesses. -/
theorem section_word_action (U : Submodule F V) (pi : V →ₗ[F] U)
    (hpi : ∀ u : U, pi (u : V) = u) (sectionMap : V → G)
    (hidden : Multiplicative U →* G) (q : V) (u : U) :
    sectionMap q * hidden (Multiplicative.ofAdd u) =
      (sectionPotential U pi sectionMap hidden q)⁻¹ *
        sectionPotential U pi sectionMap hidden (q + (u : V)) * sectionMap (q + (u : V)) := by
  have hp : pi (q + (u : V)) = pi q + u := by rw [map_add, hpi]
  have remainder : q + (u : V) - (pi (q + (u : V)) : V) = q - (pi q : V) := by
    simp only [hp, Submodule.coe_add]
    abel
  have hh : hidden (Multiplicative.ofAdd (pi (q + (u : V)))) =
      hidden (Multiplicative.ofAdd (pi q)) * hidden (Multiplicative.ofAdd u) := by
    rw [hp]
    exact hidden.map_mul (Multiplicative.ofAdd (pi q)) (Multiplicative.ofAdd u)
  simp only [sectionPotential, remainder, hh]
  group

theorem potential_in_normal_kernel (U : Submodule F V) (pi : V →ₗ[F] U)
    (sectionMap : V → G) (hidden : Multiplicative U →* G)
    (quotientMap : G →* Multiplicative V)
    (hsection : ∀ q, quotientMap (sectionMap q) = Multiplicative.ofAdd q)
    (hhidden : ∀ u : U, quotientMap (hidden (Multiplicative.ofAdd u)) =
      Multiplicative.ofAdd (u : V)) (q : V) :
    sectionPotential U pi sectionMap hidden q ∈ quotientMap.ker := by
  change quotientMap (sectionPotential U pi sectionMap hidden q) = 1
  simp only [sectionPotential, map_mul, map_inv, hsection, hhidden]
  change (q - (pi q : V) + (pi q : V)) + -q = 0
  abel

/-- Transport the group-word identity through an actual normal-first chart.
The potential's N-valued lift is a proof witness, not receiver data. -/
theorem coordinate_action {N : Type*} [Group N]
    (U : Submodule F V) (pi : V →ₗ[F] U)
    (hpi : ∀ u : U, pi (u : V) = u) (sectionMap : V → G)
    (hidden : Multiplicative U →* G) (normalMap : N →* G)
    (coordinates : G ≃ V × N)
    (chart : ∀ q a, coordinates.symm (q, a) = normalMap a * sectionMap q)
    (potential : V → N)
    (hpotential : ∀ q, normalMap (potential q) = sectionPotential U pi sectionMap hidden q)
    (q : V) (a : N) (u : U) :
    coordinates (coordinates.symm (q, a) * hidden (Multiplicative.ofAdd u)) =
      (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))) := by
  have equality : coordinates.symm (q, a) * hidden (Multiplicative.ofAdd u) =
      coordinates.symm (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))) := by
    simp only [chart, map_mul, map_inv, hpotential]
    rw [mul_assoc (normalMap a) (sectionMap q) (hidden (Multiplicative.ofAdd u)),
      section_word_action U pi hpi sectionMap hidden q u]
    group
  rw [equality, Equiv.apply_symm_apply]
end Potential

section Source
variable {F V N G : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Group N] [Group G]

/-- The whole hidden subgroup is parametrized, not just selected generators.
Normal-first coordinates multiply on the RIGHT by the potential increment. -/
theorem coset_relation (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))))
    (q r : V) (a b : N) :
    (coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b) ∈ H ↔
      r - q ∈ U ∧ b = a * (potential q)⁻¹ * potential r := by
  constructor
  · intro hedge
    let u : U := hidden.symm
      ⟨(coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b), hedge⟩
    have hu : (hidden u : G) =
        (coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b) := by
      exact congrArg Subtype.val (hidden.apply_symm_apply _)
    have hc : (r, b) =
        (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))) := by
      simpa only [hu, mul_inv_cancel_left, Equiv.apply_symm_apply] using action q a u
    have hq : r = q + (u : V) := congrArg Prod.fst hc
    constructor
    · have hd : r - q = (u : V) := by rw [hq]; abel
      rw [hd]
      exact u.property
    · simpa only [← hq] using congrArg Prod.snd hc
  · rintro ⟨hu, hb⟩
    let u : U := ⟨r - q, hu⟩
    have hq : q + (u : V) = r := by dsimp [u]; abel
    have hc := action q a u
    rw [hq, ← hb] at hc
    have hg : coordinates.symm (q, a) * (hidden u : G) =
        coordinates.symm (r, b) := coordinates.injective (by simpa using hc)
    rw [← hg, inv_mul_cancel_left]
    exact (hidden u).property

variable {D : Type*} [Fintype D] [DecidableEq D]

def UnitaryRepresentation (representation : N →* Matrix D D ℂ) : Prop :=
  ∀ a, (representation a).conjTranspose * representation a = 1

theorem row_contraction (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) (a t : N) (j k : D) :
    (∑ i, star (representation a i j) * representation (a * t) i k) =
      representation t j k := by
  have identity : (representation a).conjTranspose * representation (a * t) =
      representation t := by
    rw [map_mul, ← Matrix.mul_assoc, hunit, Matrix.one_mul]
  simpa only [Matrix.mul_apply, Matrix.conjTranspose_apply] using
    congrArg (fun M : Matrix D D ℂ => M j k) identity

theorem potential_matrix_product (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) (a b : N) :
    representation (a⁻¹ * b) =
      (representation a).conjTranspose * representation b := by
  have identity : representation b = representation a * representation (a⁻¹ * b) := by
    rw [← map_mul, mul_inv_cancel_left]
  rw [identity, ← Matrix.mul_assoc, hunit, Matrix.one_mul]

variable [Fintype V] [Fintype N] [Fintype G]

/-- d/|N| is the product of the two conjugated-QFT amplitude factors.
The row index i is TRACED, not retained or conditioned upon. -/
def fourierRowTrace (coordinates : G ≃ V × N) (H : Subgroup G)
    (representation : N →* Matrix D D ℂ) (q r : V) (j k : D) : ℂ :=
  (Fintype.card D : ℂ) * invSize N * ∑ a, ∑ i, ∑ b,
    star (representation a i j) *
      groupEntry H (coordinates.symm (q, a)) (coordinates.symm (r, b)) *
      representation b i k

omit [Fintype V] in
theorem mixed_matrix_identity (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))))
    (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) (q r : V) (j k : D) :
    fourierRowTrace coordinates H representation q r j k =
      if r - q ∈ U then (Fintype.card D : ℂ) * invSize G *
        representation ((potential q)⁻¹ * potential r) j k else 0 := by
  classical
  by_cases hu : r - q ∈ U
  · have hentry (a b : N) :
        groupEntry H (coordinates.symm (q, a)) (coordinates.symm (r, b)) =
          if b = a * ((potential q)⁻¹ * potential r) then invSize G else 0 := by
      simp only [groupEntry, coset_relation coordinates H U potential hidden action,
        hu, true_and, mul_assoc]
    have collapse (a : N) :
        (∑ i, ∑ b, star (representation a i j) *
          groupEntry H (coordinates.symm (q, a)) (coordinates.symm (r, b)) *
          representation b i k) =
        invSize G * representation ((potential q)⁻¹ * potential r) j k := by
      simp only [hentry, mul_ite, ite_mul, mul_zero, zero_mul]
      simp only [Finset.sum_ite_eq', Finset.mem_univ, ite_true]
      calc
        _ = invSize G * ∑ i, star (representation a i j) *
            representation (a * ((potential q)⁻¹ * potential r)) i k := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro i _
          ring
        _ = _ := by rw [row_contraction representation hunit]
    have hcard : (Fintype.card N : ℂ) ≠ 0 := by
      exact_mod_cast Fintype.card_ne_zero
    simp only [fourierRowTrace, collapse, Finset.sum_const, Finset.card_univ,
      nsmul_eq_mul, hu, ite_true]
    simp only [invSize]
    field_simp
  · simp [fourierRowTrace, groupEntry,
      coset_relation coordinates H U potential hidden action, hu]

/-- The normalized sector kernel. A complete correctly normalized QFT is
still needed to call the denominator an actual measurement probability. -/
theorem normalized_matrix_identity [Nonempty D]
    (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))))
    (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) (q r : V) (j k : D) :
    fourierRowTrace coordinates H representation q r j k /
      ((Fintype.card D : ℂ)^2 * invSize N) =
      if q - r ∈ U then invSize V * invSize D *
        ((representation (potential q)).conjTranspose * representation (potential r)) j k
      else 0 := by
  have support : r - q ∈ U ↔ q - r ∈ U := by
    constructor <;> intro h
    · simpa only [neg_sub] using U.neg_mem h
    · simpa only [neg_sub] using U.neg_mem h
  rw [mixed_matrix_identity coordinates H U potential hidden action representation hunit]
  have size : invSize G = invSize V * invSize N := by
    simp only [invSize, Fintype.card_congr coordinates, Fintype.card_prod,
      Nat.cast_mul, mul_inv_rev]
    ring
  by_cases hu : q - r ∈ U
  · simp only [support, hu, ite_true, size, potential_matrix_product representation hunit]
    have hd : (Fintype.card D : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
    have hn : (Fintype.card N : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
    simp only [invSize]
    field_simp
  · simp [support, hu]

/-- Compose the section-word chart with the normalized matrix-source theorem.
The action law is derived, not assumed. No hidden potential value is an
operational input to the QFT or row trace. -/
theorem source_from_normal_chart [Nonempty D]
    (coordinates : G ≃ V × N) (H : Subgroup G) (U : Submodule F V)
    (pi : V →ₗ[F] U) (hpi : ∀ u : U, pi (u : V) = u)
    (sectionMap : V → G) (hidden : U ≃ H)
    (hiddenHom : Multiplicative U →* G)
    (hvalues : ∀ u : U, hiddenHom (Multiplicative.ofAdd u) = (hidden u : G))
    (normalMap : N →* G)
    (chart : ∀ q a, coordinates.symm (q, a) = normalMap a * sectionMap q)
    (potential : V → N)
    (hpotential : ∀ q, normalMap (potential q) = sectionPotential U pi sectionMap hiddenHom q)
    (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) (q r : V) (j k : D) :
    fourierRowTrace coordinates H representation q r j k /
      ((Fintype.card D : ℂ)^2 * invSize N) =
      if q - r ∈ U then invSize V * invSize D *
        ((representation (potential q)).conjTranspose * representation (potential r)) j k
      else 0 := by
  apply normalized_matrix_identity coordinates H U potential hidden _ representation hunit
  intro x a u
  simpa only [hvalues] using
    coordinate_action U pi hpi sectionMap hiddenHom normalMap coordinates chart potential hpotential x a u

theorem sector_trace (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a * (potential q)⁻¹ * potential (q + (u : V))))
    (representation : N →* Matrix D D ℂ)
    (hunit : UnitaryRepresentation representation) :
    (∑ q, ∑ j, fourierRowTrace coordinates H representation q q j j) =
      (Fintype.card D : ℂ)^2 * invSize N := by
  simp_rw [mixed_matrix_identity coordinates H U potential hidden action representation hunit]
  have hv : (Fintype.card V : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp only [sub_self, U.zero_mem, ite_true, inv_mul_cancel, map_one,
    Matrix.one_apply_eq, mul_one, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  simp only [invSize, Fintype.card_congr coordinates, Fintype.card_prod, Nat.cast_mul]
  field_simp

end Source

/-- info: 'QSearch.CosetMatrixSource.hiding_output_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.hiding_output_trace

/-- info: 'QSearch.CosetMatrixSource.source_from_normal_chart' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.source_from_normal_chart

/-- info: 'QSearch.CosetMatrixSource.section_word_action' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.section_word_action

/-- info: 'QSearch.CosetMatrixSource.potential_in_normal_kernel' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.potential_in_normal_kernel

/-- info: 'QSearch.CosetMatrixSource.coordinate_action' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.coordinate_action

/-- info: 'QSearch.CosetMatrixSource.coset_relation' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.coset_relation

/-- info: 'QSearch.CosetMatrixSource.mixed_matrix_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.mixed_matrix_identity

/-- info: 'QSearch.CosetMatrixSource.normalized_matrix_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.normalized_matrix_identity

/-- info: 'QSearch.CosetMatrixSource.sector_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetMatrixSource.sector_trace

end
end QSearch.CosetMatrixSource
