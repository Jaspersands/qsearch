import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.LinearAlgebra.BilinearMap
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

/-!
# Conditional label balance, not merely unconditioned uniformity

For a finite weighted experiment, an equivariant selected label stays
balanced after invariant postselection, including a fixed invariant record.
Separate block postselections preserve the product law. Arbitrary record
conditioning or correlated blocks do not satisfy these hypotheses.

The linear-map lemmas connect a controller using only the relation kernel
to equivariance under changes of central basis. This module does not prove
the complete class-four rank bound, GL transitivity, a solver's success
rate, or that a quantum implementation supplies the experiment assumed here.
-/

namespace QSearch.EquivariantLabelSelection

open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

section Mass
variable {G O A : Type*} [Group G] [Fintype O] [Fintype A]
  [MulAction G O] [MulAction G A]

def selectedMass (weight : O → ℝ) (keep : O → Prop) (select : O → A)
    (a : A) : ℝ := ∑ x, if keep x ∧ select x = a then weight x else 0

def keptMass (weight : O → ℝ) (keep : O → Prop) : ℝ :=
  ∑ x, if keep x then weight x else 0

omit [Fintype A] in
/-- Uniform input is a sufficient case of the invariant-weight premise.
Random seeds may have arbitrary independent weights. -/
theorem selected_mass_transport (weight : O → ℝ) (keep : O → Prop)
    (select : O → A) (g : G)
    (hw : ∀ x, weight (g • x) = weight x)
    (hk : ∀ x, keep (g • x) ↔ keep x)
    (hs : ∀ x, select (g • x) = g • select x) (a : A) :
    selectedMass weight keep select (g • a) = selectedMass weight keep select a := by
  classical
  unfold selectedMass
  rw [← Equiv.sum_comp (MulAction.toPerm g)
    (fun x => if keep x ∧ select x = g • a then weight x else 0)]
  apply Finset.sum_congr rfl
  intro x _
  simp only [MulAction.toPerm_apply, hs, hw, hk, smul_left_cancel_iff]

omit [Fintype A] in
theorem selected_mass_equal (weight : O → ℝ) (keep : O → Prop)
    (select : O → A)
    (hw : ∀ g : G, ∀ x, weight (g • x) = weight x)
    (hk : ∀ g : G, ∀ x, keep (g • x) ↔ keep x)
    (hs : ∀ g : G, ∀ x, select (g • x) = g • select x)
    (htrans : ∀ a b : A, ∃ g : G, g • a = b) (a b : A) :
    selectedMass weight keep select a = selectedMass weight keep select b := by
  obtain ⟨g, rfl⟩ := htrans a b
  exact (selected_mass_transport weight keep select g (hw g) (hk g) (hs g) a).symm

omit [Group G] [MulAction G O] [MulAction G A] in
theorem sum_selected_mass (weight : O → ℝ) (keep : O → Prop) (select : O → A) :
    ∑ a, selectedMass weight keep select a = keptMass weight keep := by
  classical
  simp only [selectedMass, keptMass]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro x _
  by_cases h : keep x <;> simp [h]

/-- Unnormalized form is also valid when the event has probability zero. -/
theorem invariant_event_balance (weight : O → ℝ) (keep : O → Prop)
    (select : O → A)
    (hw : ∀ g : G, ∀ x, weight (g • x) = weight x)
    (hk : ∀ g : G, ∀ x, keep (g • x) ↔ keep x)
    (hs : ∀ g : G, ∀ x, select (g • x) = g • select x)
    (htrans : ∀ a b : A, ∃ g : G, g • a = b) (a : A) :
    (Fintype.card A : ℝ) * selectedMass weight keep select a =
      keptMass weight keep := by
  rw [← sum_selected_mass weight keep select]
  have h : ∀ b : A, selectedMass weight keep select b =
      selectedMass weight keep select a :=
    fun b => selected_mass_equal weight keep select hw hk hs htrans b a
  simp only [h, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]

/-- No conditional distribution is asserted for a zero-mass event. -/
theorem conditional_label_uniform (weight : O → ℝ) (keep : O → Prop)
    (select : O → A)
    (hw : ∀ g : G, ∀ x, weight (g • x) = weight x)
    (hk : ∀ g : G, ∀ x, keep (g • x) ↔ keep x)
    (hs : ∀ g : G, ∀ x, select (g • x) = g • select x)
    (htrans : ∀ a b : A, ∃ g : G, g • a = b)
    (hkeep : keptMass weight keep ≠ 0) (a : A) :
    selectedMass weight keep select a / keptMass weight keep =
      1 / (Fintype.card A : ℝ) := by
  let : Nonempty A := ⟨a⟩
  have hc : (Fintype.card A : ℝ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have h := invariant_event_balance weight keep select hw hk hs htrans a
  apply (div_eq_iff hkeep).2
  calc
    selectedMass weight keep select a = keptMass weight keep / (Fintype.card A : ℝ) :=
      (eq_div_iff hc).2 (by simpa [mul_comm] using h)
    _ = 1 / (Fintype.card A : ℝ) * keptMass weight keep := by ring

/-- Conditioning on a witness/index/seed record is legal only if that
record is invariant too. The full list of labels is generally NOT invariant. -/
theorem invariant_record_balance {R : Type*}
    (weight : O → ℝ) (keep : O → Prop) (select : O → A) (record : O → R)
    (hw : ∀ g : G, ∀ x, weight (g • x) = weight x)
    (hk : ∀ g : G, ∀ x, keep (g • x) ↔ keep x)
    (hs : ∀ g : G, ∀ x, select (g • x) = g • select x)
    (hr : ∀ g : G, ∀ x, record (g • x) = record x)
    (htrans : ∀ a b : A, ∃ g : G, g • a = b) (r : R) (a : A) :
    (Fintype.card A : ℝ) *
        selectedMass weight (fun x => keep x ∧ record x = r) select a =
      keptMass weight (fun x => keep x ∧ record x = r) := by
  apply invariant_event_balance weight _ select hw _ hs htrans a
  intro g x
  simp only [hk, hr]
end Mass

section Product
variable {O P A B : Type*} [Fintype O] [Fintype P]

/-- Independent preparation and separate acceptance events, not just
uniform single-block marginals, justify multiplying block probabilities. -/
theorem separate_postselection_product
    (w : O → ℝ) (v : P → ℝ) (keep : O → Prop) (accept : P → Prop)
    (select : O → A) (choose : P → B) (a : A) (b : B) :
    selectedMass (fun x : O × P => w x.1 * v x.2)
        (fun x => keep x.1 ∧ accept x.2)
        (fun x => (select x.1, choose x.2)) (a, b) =
      selectedMass w keep select a * selectedMass v accept choose b := by
  classical
  simp only [selectedMass, Fintype.sum_prod_type, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro y _
  apply Finset.sum_congr rfl
  intro x _
  by_cases hx : keep x <;> by_cases hy : accept y <;>
    by_cases ha : select x = a <;> by_cases hb : choose y = b <;>
    simp [hx, hy, ha, hb]
end Product

section Controller
variable {F U V Seed Output : Type*} [Field F]
  [AddCommGroup U] [Module F U] [AddCommGroup V] [Module F V]

theorem postcompose_kernel (f : U →ₗ[F] V) (A : V ≃ₗ[F] V) :
    LinearMap.ker (A.toLinearMap.comp f) = LinearMap.ker f := by
  ext x
  simp

theorem kernel_controller_invariant
    (controller : Submodule F U → Seed → Output)
    (f : U →ₗ[F] V) (A : V ≃ₗ[F] V) (seed : Seed) :
    controller (LinearMap.ker (A.toLinearMap.comp f)) seed =
      controller (LinearMap.ker f) seed := by
  rw [postcompose_kernel]

theorem selected_column_equivariant {I : Type*} [DecidableEq I]
    (index : Submodule F (I → F) → Seed → I)
    (f : (I → F) →ₗ[F] V) (A : V ≃ₗ[F] V) (seed : Seed) :
    (A.toLinearMap.comp f)
        (Pi.single (index (LinearMap.ker (A.toLinearMap.comp f)) seed) 1) =
      A (f (Pi.single (index (LinearMap.ker f) seed) 1)) := by
  rw [postcompose_kernel]
  rfl
end Controller

theorem block_schedule_bound (p : ℝ) (hp : 5 ≤ p) (L : ℕ) :
    (p^L-1) * (2/p)^(2*L+2) ≤ 1/p := by
  have hpos : 0 < p := by linarith
  have hnz : p ≠ 0 := ne_of_gt hpos
  have hratio : 0 ≤ 4/p := by positivity
  have hratio_one : 4/p ≤ 1 := (div_le_one hpos).2 (by linarith)
  have hsquare : (2/p)^2 = 4/p^2 := by ring
  have hbase : p*((2/p)^2) = 4/p := by field_simp; ring
  have hid : p^L * (2/p)^(2*L+2) = (4/p)^L * (4/p^2) := by
    rw [pow_add, pow_mul, ← mul_assoc, ← mul_pow, hbase, hsquare]
  calc
    (p^L-1) * (2/p)^(2*L+2) ≤ p^L * (2/p)^(2*L+2) := by
      apply mul_le_mul_of_nonneg_right (by linarith)
      positivity
    _ = (4/p)^L * (4/p^2) := hid
    _ ≤ 1 * (4/p^2) := mul_le_mul_of_nonneg_right
      (pow_le_one₀ hratio hratio_one) (by positivity)
    _ ≤ 1/p := by
      have h : 4 ≤ p := by linarith
      apply (le_div_iff₀ hpos).2
      field_simp
      nlinarith

end

/-- info: 'QSearch.EquivariantLabelSelection.selected_mass_transport' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms selected_mass_transport

/-- info: 'QSearch.EquivariantLabelSelection.invariant_event_balance' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms invariant_event_balance

/-- info: 'QSearch.EquivariantLabelSelection.conditional_label_uniform' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms conditional_label_uniform

/-- info: 'QSearch.EquivariantLabelSelection.invariant_record_balance' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms invariant_record_balance

/-- info: 'QSearch.EquivariantLabelSelection.separate_postselection_product' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms separate_postselection_product

/-- info: 'QSearch.EquivariantLabelSelection.postcompose_kernel' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms postcompose_kernel

/-- info: 'QSearch.EquivariantLabelSelection.selected_column_equivariant' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms selected_column_equivariant

/-- info: 'QSearch.EquivariantLabelSelection.block_schedule_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms block_schedule_bound

end QSearch.EquivariantLabelSelection
