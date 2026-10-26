import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.LinearAlgebra.Prod
import Mathlib.Tactic
import Formal.WeylSourceScalarization

/-!
# One hidden jet across public alignment transcripts

The unknown quadratic map is a proof witness, not an operational input.
The public K/J alignment identities imply the SAME retained linear map
for all batches, including different source/carrier dimensions. This
does not construct the group potential, quantum source or Clifford gates.
-/

namespace QSearch.CommonQuadraticJet

open scoped BigOperators
noncomputable section

variable {F V W C X I : Type*} [Field F]
  [AddCommGroup V] [Module F V] [AddCommGroup W] [Module F W]
  [AddCommGroup C] [Module F C] [AddCommGroup X] [Module F X]
  [Fintype I]

def quadratic (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (q : V) : W := a + L q + B q q

/-- Basis-free version of stack(A,C_1,...,C_m). B need not be symmetric. -/
def commonJet (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W) :
    V →ₗ[F] W × (V →ₗ[F] W) := L.prod (B + B.flip)

def quadraticMap (D : I → W →ₗ[F] C) (s : I → F) (w : W) : C :=
  ∑ i, (s i)^2 • D i w

def linearMap (D : I → W →ₗ[F] C) (s : I → F) (y : I → V)
    (j : W × (V →ₗ[F] W)) : C :=
  ∑ i, s i • D i (j.1 + j.2 (y i))

def displacement (D : I → W →ₗ[F] C) (s : I → F) (y : I → V)
    (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W) (q : V) : C :=
  ∑ i, D i (quadratic a L B (y i + s i • q))

omit [Fintype I] in
theorem quadratic_translation (a : W) (L : V →ₗ[F] W)
    (B : V →ₗ[F] V →ₗ[F] W) (y q : V) (s : F) :
    quadratic a L B (y + s • q) =
      quadratic a L B y + s • ((commonJet L B q).1 + (commonJet L B q).2 y)
        + s^2 • B q q := by
  change a + L (y + s • q) + B (y + s • q) (y + s • q) =
    (a + L y + B y y) + s • (L q + (B q y + B y q)) + s^2 • B q q
  simp only [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply]
  module

theorem displacement_decomposition (D : I → W →ₗ[F] C) (s : I → F)
    (y : I → V) (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (q : V) :
    displacement D s y a L B q = displacement D s y a L B 0
      + linearMap D s y (commonJet L B q) + quadraticMap D s (B q q) := by
  simp only [displacement, quadratic_translation, map_add, map_smul,
    Finset.sum_add_distrib, linearMap, quadraticMap, smul_zero, add_zero]

/-- The quadratic and linear alignment certificates derive the affine law;
the desired retained jet is not an additional assumption. -/
theorem aligned_displacement (D : I → W →ₗ[F] C) (s : I → F)
    (y : I → V) (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (A : C →ₗ[F] X) (E : (W × (V →ₗ[F] W)) →ₗ[F] X)
    (hK : ∀ w, A (quadraticMap D s w) = 0)
    (hJ : ∀ j, A (linearMap D s y j) = E j) (q : V) :
    A (displacement D s y a L B q) =
      A (displacement D s y a L B 0) + E (commonJet L B q) := by
  rw [displacement_decomposition D s y a L B q, map_add, map_add, hK, hJ,
    add_zero]

theorem aligned_difference (D : I → W →ₗ[F] C) (s : I → F)
    (y : I → V) (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (A : C →ₗ[F] X) (E : (W × (V →ₗ[F] W)) →ₗ[F] X)
    (hK : ∀ w, A (quadraticMap D s w) = 0)
    (hJ : ∀ j, A (linearMap D s y j) = E j) (q q' : V) :
    A (displacement D s y a L B q) - A (displacement D s y a L B q') =
      E (commonJet L B (q - q')) := by
  rw [aligned_displacement D s y a L B A E hK hJ q,
    aligned_displacement D s y a L B A E hK hJ q', map_sub, map_sub]
  abel

/-- Two independently chosen public transcripts have the same derivative,
even with different numbers of sources and different carrier spaces. -/
theorem different_batches_same_jet {I' C' : Type*} [Fintype I']
    [AddCommGroup C'] [Module F C']
    (D : I → W →ₗ[F] C) (s : I → F) (y : I → V)
    (D' : I' → W →ₗ[F] C') (s' : I' → F) (y' : I' → V)
    (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (A : C →ₗ[F] X) (A' : C' →ₗ[F] X)
    (E : (W × (V →ₗ[F] W)) →ₗ[F] X)
    (hK : ∀ w, A (quadraticMap D s w) = 0)
    (hJ : ∀ j, A (linearMap D s y j) = E j)
    (hK' : ∀ w, A' (quadraticMap D' s' w) = 0)
    (hJ' : ∀ j, A' (linearMap D' s' y' j) = E j) (q q' : V) :
    A (displacement D s y a L B q) - A (displacement D s y a L B q') =
      A' (displacement D' s' y' a L B q) - A' (displacement D' s' y' a L B q') := by
  rw [aligned_difference D s y a L B A E hK hJ,
    aligned_difference D' s' y' a L B A' E hK' hJ']

theorem retained_and_spectator {S : Type*} [AddCommGroup S] [Module F S]
    (D : I → W →ₗ[F] C) (s : I → F) (y : I → V)
    (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (A : C →ₗ[F] (W × (V →ₗ[F] W)) × S)
    (hK : ∀ w, A (quadraticMap D s w) = 0)
    (hJ : ∀ j, A (linearMap D s y j) = (j, 0)) (q : V) :
    A (displacement D s y a L B q) =
      ((A (displacement D s y a L B 0)).1 + commonJet L B q,
        (A (displacement D s y a L B 0)).2) := by
  calc
    _ = A (displacement D s y a L B 0) + (commonJet L B q, 0) :=
      aligned_displacement D s y a L B A
        (LinearMap.inl F (W × (V →ₗ[F] W)) S) hK hJ q
    _ = _ := by ext <;> simp

/-- Compose the derived common affine displacement with the actual
spectator Kraus sums. The same graphSupport appears in every batch. -/
theorem quadratic_source_to_scalar {S : Type*} [AddCommGroup S] [Module F S]
    [Fintype V] [Fintype (W × (V →ₗ[F] W))] [Fintype S]
    (D : I → W →ₗ[F] C) (s : I → F) (y : I → V)
    (a : W) (L : V →ₗ[F] W) (B : V →ₗ[F] V →ₗ[F] W)
    (A : C →ₗ[F] (W × (V →ₗ[F] W)) × S)
    (hK : ∀ w, A (quadraticMap D s w) = 0)
    (hJ : ∀ j, A (linearMap D s y j) = (j, 0))
    (U : Submodule F V) (gamma : V → ((W × (V →ₗ[F] W)) × S) → ℂ)
    (outcome : S) (x x' : V × (W × (V →ₗ[F] W))) :
    WeylSourceScalarization.spectatorBranch U
      (fun q => A (displacement D s y a L B q)) gamma outcome x x' =
      AffineSupportErasure.invSize S * AffineSupportErasure.rho
        (WeylSourceScalarization.graphSupport U (commonJet L B))
        (WeylSourceScalarization.scalarPhase gamma outcome) x x' := by
  have hA : (fun q => A (displacement D s y a L B q)) =
      WeylSourceScalarization.affineDisplacement (commonJet L B)
        (A (displacement D s y a L B 0)).1
        (A (displacement D s y a L B 0)).2 := by
    funext q
    exact retained_and_spectator D s y a L B A hK hJ q
  rw [hA, WeylSourceScalarization.matrix_source_to_scalar]

/-- info: 'QSearch.CommonQuadraticJet.quadratic_translation' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.quadratic_translation

/-- info: 'QSearch.CommonQuadraticJet.displacement_decomposition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.displacement_decomposition

/-- info: 'QSearch.CommonQuadraticJet.aligned_displacement' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.aligned_displacement

/-- info: 'QSearch.CommonQuadraticJet.aligned_difference' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.aligned_difference

/-- info: 'QSearch.CommonQuadraticJet.different_batches_same_jet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.different_batches_same_jet

/-- info: 'QSearch.CommonQuadraticJet.retained_and_spectator' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.retained_and_spectator

/-- info: 'QSearch.CommonQuadraticJet.quadratic_source_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CommonQuadraticJet.quadratic_source_to_scalar

end
end QSearch.CommonQuadraticJet
