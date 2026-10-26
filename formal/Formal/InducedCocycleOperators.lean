import Formal.AmbientPotentialFiltration

/-!
# Universal operator specialization for the right-fiber cocycle

On an abelian ideal containing all brackets, ad A and ad X commute.
These lemmas justify the B_ij,C_ij normal-form certificate over arbitrary
Lie algebras, not just sampled structure tensors. The exponential-word
identity is still an external rational coefficient certificate.
-/

namespace QSearch.InducedCocycleOperators

noncomputable section
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

structure AbelianIdealData (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L] where
  ideal : LieIdeal F L
  derived_mem : ∀ a b : L, ⁅a,b⁆ ∈ ideal
  abelian : ∀ u ∈ ideal, ∀ v ∈ ideal, ⁅u,v⁆ = 0

variable (st : AbelianIdealData F L)

theorem actions_commute (a x z : L) (hz : z ∈ st.ideal) :
    ⁅a,⁅x,z⁆⁆ = ⁅x,⁅a,z⁆⁆ := by
  apply sub_eq_zero.mp
  rw [← lie_lie]
  exact st.abelian _ (st.derived_mem a x) _ hz

def iterate (a : L) : ℕ → L → L
  | 0, z => z
  | n+1, z => ⁅a, iterate a n z⁆

theorem iterate_mem (a z : L) (hz : z ∈ st.ideal) (n : ℕ) :
    iterate a n z ∈ st.ideal := by
  induction n with
  | zero => exact hz
  | succ n ih => exact st.ideal.lie_mem ih

theorem action_iterate_swap (a x z : L) (hz : z ∈ st.ideal) (n : ℕ) :
    ⁅x, iterate a n z⁆ = iterate a n ⁅x,z⁆ := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change ⁅x,⁅a,iterate a n z⁆⁆ = ⁅a,iterate a n ⁅x,z⁆⁆
    rw [actions_commute st x a _ (iterate_mem st a z hz n), ih]

def normal (a x z : L) (i j : ℕ) : L := iterate a i (iterate x j z)

theorem normal_mem (a x z : L) (hz : z ∈ st.ideal) (i j : ℕ) :
    normal a x z i j ∈ st.ideal :=
  iterate_mem st a _ (iterate_mem st x z hz j) i

theorem normal_action_a (a x z : L) (i j : ℕ) :
    ⁅a,normal a x z i j⁆ = normal a x z (i+1) j := rfl

theorem normal_action_x (a x z : L) (hz : z ∈ st.ideal) (i j : ℕ) :
    ⁅x,normal a x z i j⁆ = normal a x z i (j+1) :=
  action_iterate_swap st a x _ (iterate_mem st x z hz j) i

theorem normal_bracket_zero (a x u v : L) (hu : u ∈ st.ideal)
    (hv : v ∈ st.ideal) (i j s t : ℕ) :
    ⁅normal a x u i j, normal a x v s t⁆ = 0 :=
  st.abelian _ (normal_mem st a x u hu i j) _ (normal_mem st a x v hv s t)

theorem action_add_ideal (a b z : L) (hb : b ∈ st.ideal) (hz : z ∈ st.ideal) :
    ⁅a+b,z⁆ = ⁅a,z⁆ := by
  rw [add_lie, st.abelian _ hb _ hz, add_zero]

theorem affine_iterate (a b x : L) (hb : b ∈ st.ideal) (n : ℕ) :
    iterate (a+b) (n+1) x = iterate a n (⁅a,x⁆ - ⁅x,b⁆) := by
  induction n with
  | zero => simp only [iterate, add_lie, lie_skew b x, sub_eq_add_neg]
  | succ n ih =>
    change ⁅a+b,iterate (a+b) (n+1) x⁆ = ⁅a,iterate a n (⁅a,x⁆-⁅x,b⁆)⁆
    rw [ih, action_add_ideal st a b _ hb
      (iterate_mem st a _ (st.ideal.sub_mem (st.derived_mem a x) (st.ideal.lie_mem hb)) n)]

theorem coordinate_bracket (a x u v : L) (hu : u ∈ st.ideal) (hv : v ∈ st.ideal)
    (s t s' t' : F) :
    ⁅s • a + t • x + u, s' • a + t' • x + v⁆ =
      (s*t'-t*s') • ⁅a,x⁆ + s • ⁅a,v⁆ + t • ⁅x,v⁆ - s' • ⁅a,u⁆ - t' • ⁅x,u⁆ := by
  simp only [add_lie, lie_add, smul_lie, lie_smul, lie_self, smul_zero,
    st.abelian u hu v hv, smul_add]
  rw [← lie_skew x a, ← lie_skew u a, ← lie_skew u x]
  module

theorem iterate_mem_lower (a z : L) (d n : ℕ)
    (hz : z ∈ LieModule.lowerCentralSeries F L L d) :
    iterate a n z ∈ LieModule.lowerCentralSeries F L L (d+n) := by
  induction n with
  | zero => simpa only [Nat.add_zero, iterate] using hz
  | succ n ih =>
    simpa only [Nat.add_succ, iterate, LieModule.lowerCentralSeries_succ] using
      LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a) ih

theorem normal_vanishes (a x z : L) (d i j k : ℕ)
    (hz : z ∈ LieModule.lowerCentralSeries F L L d)
    (hnil : LieModule.lowerCentralSeries F L L k = ⊥) (hdegree : k ≤ d+i+j) :
    normal a x z i j = 0 := by
  have hm := iterate_mem_lower a _ (d+j) i (iterate_mem_lower x z d j hz)
  have hk := LieModule.antitone_lowerCentralSeries F L L (show k ≤ (d+j)+i by omega) hm
  simpa only [normal, hnil, LieSubmodule.mem_bot] using hk

/-- info: 'QSearch.InducedCocycleOperators.actions_commute' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms actions_commute
/-- info: 'QSearch.InducedCocycleOperators.normal_action_x' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms normal_action_x
/-- info: 'QSearch.InducedCocycleOperators.normal_bracket_zero' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms normal_bracket_zero
/-- info: 'QSearch.InducedCocycleOperators.affine_iterate' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms affine_iterate
/-- info: 'QSearch.InducedCocycleOperators.coordinate_bracket' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms coordinate_bracket
/-- info: 'QSearch.InducedCocycleOperators.normal_vanishes' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms normal_vanishes

end
end QSearch.InducedCocycleOperators
