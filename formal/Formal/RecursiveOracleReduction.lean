import Formal.CosetSourceFourier
import Mathlib.Algebra.Group.Subgroup.Map
import Mathlib.Tactic

/-!
# Quotient hiding oracles with reversible representative cleanup

A public section need not be a homomorphism. Its quotient kernel must be
contained in the hidden subgroup. Composition of public sections preserves
the hiding relation, while leaking the injective representative workspace
destroys every off-diagonal entry. No subgroup solver is assumed implemented.
-/

namespace QSearch.RecursiveOracleReduction

open QSearch.AffineSupportErasure (invSize)
noncomputable section
attribute [local instance] Classical.propDecidable

section Quotient
variable {G Q T O : Type*} [Group G] [Group Q] [Group T]

theorem map_mem_iff (pi : G →* Q) (H : Subgroup G) (kernel : pi.ker ≤ H) (x : G) :
    pi x ∈ H.map pi ↔ x ∈ H := by
  constructor
  · rintro ⟨y, hy, he⟩
    have hk : y⁻¹ * x ∈ pi.ker := by
      change pi (y⁻¹ * x) = 1
      simp [map_mul, map_inv, he]
    simpa using H.mul_mem hy (kernel hk)
  · intro hx
    exact ⟨x, hx, rfl⟩

theorem quotient_hides (pi : G →* Q) (H : Subgroup G) (kernel : pi.ker ≤ H)
    (sectionMap : Q → G) (right_inverse : ∀ q, pi (sectionMap q) = q)
    (f : G → O) (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) (q r : Q) :
    f (sectionMap q) = f (sectionMap r) ↔ q⁻¹ * r ∈ H.map pi := by
  rw [hides, ← map_mem_iff pi H kernel]
  simp only [map_mul, map_inv, right_inverse]

theorem section_labels_equal (pi : G →* Q) (H : Subgroup G) (kernel : pi.ker ≤ H)
    (s t : Q → G) (hs : ∀ q, pi (s q) = q) (ht : ∀ q, pi (t q) = q)
    (f : G → O) (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) (q : Q) :
    f (s q) = f (t q) := by
  rw [hides, ← map_mem_iff pi H kernel]
  simp [map_mul, map_inv, hs, ht]

theorem nested_sections (pi : G →* Q) (tau : Q →* T)
    (s : Q → G) (t : T → Q) (hs : ∀ q, pi (s q) = q)
    (ht : ∀ r, tau (t r) = r) (r : T) :
    (tau.comp pi) (s (t r)) = r := by
  simp [hs, ht]

theorem nested_kernel (pi : G →* Q) (tau : Q →* T)
    (H : Subgroup G) (hp : pi.ker ≤ H) (ht : tau.ker ≤ H.map pi) :
    (tau.comp pi).ker ≤ H := by
  intro x hx
  apply (map_mem_iff pi H hp x).mp
  apply ht
  exact hx

variable [Fintype Q]

def labelKernel (f : Q → O) (q r : Q) : ℂ := if f q = f r then invSize Q else 0

theorem cleaned_kernel (pi : G →* Q) (H : Subgroup G) (kernel : pi.ker ≤ H)
    (s : Q → G) (hs : ∀ q, pi (s q) = q)
    (f : G → O) (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) (q r : Q) :
    labelKernel (f ∘ s) q r = CosetSourceFourier.groupEntry (H.map pi) q r := by
  simp only [labelKernel, Function.comp_apply, quotient_hides pi H kernel s hs f hides,
    CosetSourceFourier.groupEntry]

/-- Tracing an uncomputed representative makes the source diagonal,
regardless of which subgroup the original oracle hides. -/
theorem leaked_kernel (pi : G →* Q) (s : Q → G) (hs : ∀ q, pi (s q) = q)
    (f : G → O) (q r : Q) :
    labelKernel (f ∘ s) q r * (if s q = s r then 1 else 0) =
      if q = r then invSize Q else 0 := by
  have hinj : Function.Injective s := by
    intro x y h
    simpa only [hs] using congrArg pi h
  by_cases h : q = r
  · subst r
    simp [labelKernel]
  · have hne : s q ≠ s r := fun he => h (hinj he)
    simp [hne, h]
end Quotient

section Cleanup
variable {Q W Y : Type*} [AddCommGroup W] [AddCommGroup Y]

def computeWorkspace (s : Q → W) : Q × (W × Y) ≃ Q × (W × Y) where
  toFun v := (v.1, (v.2.1 + s v.1, v.2.2))
  invFun v := (v.1, (v.2.1 - s v.1, v.2.2))
  left_inv v := by simp
  right_inv v := by simp

def labelQuery (f : W → Y) : Q × (W × Y) ≃ Q × (W × Y) where
  toFun v := (v.1, (v.2.1, v.2.2 + f v.2.1))
  invFun v := (v.1, (v.2.1, v.2.2 - f v.2.1))
  left_inv v := by simp
  right_inv v := by simp

/-- Exactly ONE original label query between public compute/uncompute. -/
def cleanOracle (s : Q → W) (f : W → Y) : Q × (W × Y) ≃ Q × (W × Y) :=
  ((computeWorkspace s).trans (labelQuery f)).trans (computeWorkspace s).symm

theorem clean_basis (s : Q → W) (f : W → Y) (q : Q) (b : Y) :
    cleanOracle s f (q, (0, b)) = (q, (0, b + f (s q))) := by
  simp [cleanOracle, computeWorkspace, labelQuery]
end Cleanup

end
end QSearch.RecursiveOracleReduction

/-- info: 'QSearch.RecursiveOracleReduction.quotient_hides' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RecursiveOracleReduction.quotient_hides

/-- info: 'QSearch.RecursiveOracleReduction.leaked_kernel' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RecursiveOracleReduction.leaked_kernel

/-- info: 'QSearch.RecursiveOracleReduction.clean_basis' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RecursiveOracleReduction.clean_basis
