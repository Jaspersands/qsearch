import Formal.VectorCentralSource
import Formal.FullJetAlignment

/-!
# Noncentral right-fiber source to additive monomial gauges

The generic complete instrument is in CentralRegularSource under its
historical name. Here an abelian quotient gives the precise translation
law used by the induced-phase compiler. The operational source depends
only on public charts and the original oracle; hidden potentials and
alignment identities are correctness witnesses, not operational inputs.
-/

namespace QSearch.InducedRegularSource

open scoped BigOperators
open AffineSupportErasure CentralRegularSource
noncomputable section
attribute [local instance] Classical.propDecidable

variable {N A C : Type*} [Group N] [AddCommGroup A] [AddCommGroup C]

structure AdditiveChart (N A C : Type*) [Group N] [AddCommGroup A] [AddCommGroup C]
    extends RightAbelianChart N A C where
  quotient : N →* Multiplicative A
  projection : ∀ g, (coordinates g).1 = Multiplicative.toAdd (quotient g)

variable (S : AdditiveChart N A C)

def translation (g : N) : A := Multiplicative.toAdd (S.quotient g)

def cocycle (g : N) (x : A) : C := (action S.toRightAbelianChart g x).2

theorem translation_action (g : N) (x : A) :
    (action S.toRightAbelianChart g x).1 = translation S g + x := by
  have hs : S.coordinates (S.sectionMap x) = (x, 0) := by
    have h : S.sectionMap x = S.coordinates.symm (x, 0) := by simp [S.chart]
    rw [h, Equiv.apply_symm_apply]
  have hx : Multiplicative.toAdd (S.quotient (S.sectionMap x)) = x := by
    rw [← S.projection, hs]
  change (S.coordinates (g*S.sectionMap x)).1 = _
  rw [S.projection, map_mul]
  change translation S g + Multiplicative.toAdd (S.quotient (S.sectionMap x)) = _
  rw [hx]

theorem cocycle_mul (g h : N) (x : A) :
    cocycle S (g*h) x = cocycle S h x + cocycle S g (translation S h+x) := by
  have h := congrArg Prod.snd (action_mul S.toRightAbelianChart g h x)
  simpa only [cocycle, translation_action] using h

def phase (chi : AddChar C ℂ) (g : N) (x : A) : ℂ := chi (cocycle S g x)

theorem sector_gauge {Q : Type*} (chi : AddChar C ℂ) (potential : Q → N)
    (q : Q) (x y : A) :
    sector S.toRightAbelianChart chi (potential q) x y =
      WeylSourceScalarization.gaugeEntry (fun q => translation S (potential q))
        (fun q => phase S chi (potential q)) q x y := by
  simp only [sector, translation_action, WeylSourceScalarization.gaugeEntry, phase, cocycle]

section Finite
variable [Fintype A] [Fintype C] [DecidableEq A]

omit [Fintype A] [DecidableEq A] in
theorem phase_unit (chi : AddChar C ℂ) (g : N) (x : A) :
    phase S chi g x * star (phase S chi g x) = 1 :=
  character_unit chi _

theorem potential_kernel {Q : Type*} (chi : AddChar C ℂ) (potential : Q → N)
    (q r : Q) (x y : A) :
    sector S.toRightAbelianChart chi ((potential q)⁻¹*potential r) x y =
      WeylSourceScalarization.gaugeKernel (fun q => translation S (potential q))
        (fun q => phase S chi (potential q)) q r x y := by
  rw [potential_gauge S.toRightAbelianChart chi]
  change (∑ t, star (sector S.toRightAbelianChart chi (potential q) t x) *
    sector S.toRightAbelianChart chi (potential r) t y) = _
  simp_rw [sector_gauge]
  rfl

variable {F V G O : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Group G] [Fintype N] [Fintype V] [Fintype G] [Fintype O]

theorem oracle_to_matrix
    (coordinates : G ≃ V × N) (H : Subgroup G) (f : G → O)
    (hides : ∀ g g', f g = f g' ↔ g⁻¹*g' ∈ H)
    (U : Submodule F V) (pi : V →ₗ[F] U) (hpi : ∀ u : U, pi (u : V) = u)
    (sectionMap : V → G) (hidden : U ≃ H) (hiddenHom : Multiplicative U →* G)
    (hvalues : ∀ u : U, hiddenHom (Multiplicative.ofAdd u) = (hidden u : G))
    (normalMap : N →* G)
    (chart : ∀ q a, coordinates.symm (q,a) = normalMap a * sectionMap q)
    (potential : V → N)
    (hpotential : ∀ q, normalMap (potential q) =
      CosetMatrixSource.sectionPotential U pi sectionMap hiddenHom q)
    (chi : AddChar C ℂ) (q r : V) (x y : A) :
    oracleBranch S.toRightAbelianChart coordinates f chi q r x y =
      invSize C * WeylSourceScalarization.matrixSource U
        (fun q => translation S (potential q)) (fun q => phase S chi (potential q)) (q,x) (r,y) := by
  rw [oracle_source_from_normal_chart S.toRightAbelianChart coordinates H f hides U pi hpi
    sectionMap hidden hiddenHom hvalues normalMap chart potential hpotential]
  have hu : r-q ∈ U ↔ q-r ∈ U := by
    rw [← neg_sub q r, neg_mem_iff]
  simp only [WeylSourceScalarization.matrixSource, hu, potential_kernel]

variable {J Z : Type*} [Module F A] [AddCommGroup J] [Module F J]
  [AddCommGroup Z] [Module F Z] [Fintype J] [Fintype Z]

/-- Actual source, public GL permutation and spectator measurement. The
potential, projected subgroup and curve are absent from this definition. -/
def alignedOracleBranch (coordinates : G ≃ V × N) (f : G → O)
    (chi : AddChar C ℂ) (e : A ≃ₗ[F] J × Z) (outcome : Z) (x x' : V × J) : ℂ :=
  ∑ u, ∑ v, WeylSourceScalarization.measurementKraus outcome x u *
    FullJetAlignment.conjugation e.toEquiv
      (oracleBranch S.toRightAbelianChart coordinates f chi u.1 v.1) u.2 v.2 *
    star (WeylSourceScalarization.measurementKraus outcome x' v)

theorem oracle_aligned_to_scalar
    (coordinates : G ≃ V × N) (H : Subgroup G) (f : G → O)
    (hides : ∀ g g', f g = f g' ↔ g⁻¹*g' ∈ H)
    (U : Submodule F V) (pi : V →ₗ[F] U) (hpi : ∀ u : U, pi (u : V) = u)
    (sectionMap : V → G) (hidden : U ≃ H) (hiddenHom : Multiplicative U →* G)
    (hvalues : ∀ u : U, hiddenHom (Multiplicative.ofAdd u) = (hidden u : G))
    (normalMap : N →* G)
    (chart : ∀ q a, coordinates.symm (q,a) = normalMap a * sectionMap q)
    (potential : V → N)
    (hpotential : ∀ q, normalMap (potential q) =
      CosetMatrixSource.sectionPotential U pi sectionMap hiddenHom q)
    (chi : AddChar C ℂ) (e : A ≃ₗ[F] J × Z) (curve : V → J) (a : J) (b : Z)
    (hA : ∀ q, e (translation S (potential q)) = (a+curve q,b))
    (outcome : Z) (x x' : V × J) :
    alignedOracleBranch S coordinates f chi e outcome x x' =
      invSize C * invSize Z * NonlinearJetChannel.curveRho U curve
        (fun x => chi (-cocycle S (potential x.1) (e.symm (x.2,outcome)))) x x' := by
  let A' : V → A := fun q => translation S (potential q)
  let gamma : V → A → ℂ := fun q => phase S chi (potential q)
  have hk (q r : V) (u v : A) :
      oracleBranch S.toRightAbelianChart coordinates f chi q r u v =
        invSize C * WeylSourceScalarization.matrixSource U A' gamma (q,u) (r,v) :=
    oracle_to_matrix S coordinates H f hides U pi hpi sectionMap hidden hiddenHom
      hvalues normalMap chart potential hpotential chi q r u v
  have he (q r : V) (u v : J × Z) :
      FullJetAlignment.conjugation e.toEquiv
        (oracleBranch S.toRightAbelianChart coordinates f chi q r) u v =
      invSize C * FullJetAlignment.conjugation e.toEquiv
        (fun s t => WeylSourceScalarization.matrixSource U A' gamma (q,s) (r,t)) u v := by
    simp only [FullJetAlignment.conjugation, hk, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro s _
    apply Finset.sum_congr rfl
    intro t _
    ring
  have hbranch : alignedOracleBranch S coordinates f chi e outcome x x' =
      invSize C * FullJetAlignment.alignedSpectatorBranch e U A' gamma outcome x x' := by
    simp only [alignedOracleBranch, he, FullJetAlignment.alignedSpectatorBranch, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro u _
    apply Finset.sum_congr rfl
    intro v _
    ring
  rw [hbranch, FullJetAlignment.aligned_source_to_scalar e U A' gamma curve a b hA]
  have hp : WeylSourceScalarization.scalarPhase (fun q t => gamma q (e.symm t)) outcome =
      fun x : V × J => chi (-cocycle S (potential x.1) (e.symm (x.2,outcome))) := by
    funext x
    exact (chi.map_neg_eq_conj _).symm
  rw [hp]
  ring

omit [Fintype A] [DecidableEq A] [Fintype N] in
theorem scalar_branch_trace (U : Submodule F V) (potential : V → N)
    (chi : AddChar C ℂ) (e : A ≃ₗ[F] J × Z) (curve : V → J) (outcome : Z) :
    (∑ x : V × J, invSize C * invSize Z * NonlinearJetChannel.curveRho U curve
      (fun x => chi (-cocycle S (potential x.1) (e.symm (x.2,outcome)))) x x) =
      invSize C * invSize Z := by
  rw [← Finset.mul_sum, NonlinearJetChannel.curve_trace_one]
  · exact mul_one _
  · intro x
    exact character_unit chi _

end Finite

section ConcreteChart
variable {F B : Type*} [Field F] [Module F A] [AddCommGroup B] [Module F B] [Module F C]
  [Fact ((2 : F) ≠ 0)] [Fact ((3 : F) ≠ 0)]

variable (st : VectorCentralSource.StructureMaps F A B C)

/-- Right I=B+C fiber in the vector BCH group. It is generally noncentral.
The fiber coordinate is NOT the raw logarithmic central coordinate. -/
def vectorCoordinates : VectorCentralSource.Element st ≃ A × (B × C) where
  toFun g := (g.a, (g.b, g.c - (2 : F)⁻¹ • st.delta g.a g.b))
  invFun t := ⟨t.1, t.2.1, t.2.2 + (2 : F)⁻¹ • st.delta t.1 t.2.1⟩
  left_inv g := by apply VectorCentralSource.Element.ext <;> simp
  right_inv t := by rcases t with ⟨a,b,c⟩; simp

def vectorFiber : Multiplicative (B × C) →* VectorCentralSource.Element st where
  toFun z := ⟨0, (Multiplicative.toAdd z).1, (Multiplicative.toAdd z).2⟩
  map_one' := rfl
  map_mul' z w := by apply VectorCentralSource.Element.ext <;> simp

def vectorQuotient : VectorCentralSource.Element st →* Multiplicative A where
  toFun g := Multiplicative.ofAdd g.a
  map_one' := rfl
  map_mul' _ _ := rfl

def vectorRightChart : AdditiveChart (VectorCentralSource.Element st) A (B × C) where
  coordinates := vectorCoordinates st
  sectionMap a := ⟨a,0,0⟩
  fiber := vectorFiber st
  chart a z := by
    apply VectorCentralSource.Element.ext <;>
      simp [vectorCoordinates, vectorFiber, add_comm]
  quotient := vectorQuotient st
  projection g := rfl

theorem vector_fiber_noncentral (a : A) (b : B) (hab : st.delta a b ≠ 0) :
    vectorFiber st (Multiplicative.ofAdd (b,0)) * (vectorRightChart st).sectionMap a ≠
      (vectorRightChart st).sectionMap a * vectorFiber st (Multiplicative.ofAdd (b,0)) := by
  intro h
  have hc : (2 : F)⁻¹ • (-st.delta a b) = (2 : F)⁻¹ • st.delta a b := by
    simpa [vectorFiber, vectorRightChart] using congrArg VectorCentralSource.Element.c h
  have htwo : (2 : F)⁻¹ + (2 : F)⁻¹ = 1 := by
    have h2 : (2 : F) ≠ 0 := Fact.out
    field_simp
    norm_num
  apply hab
  have hz : (2 : F)⁻¹ • st.delta a b + (2 : F)⁻¹ • st.delta a b = 0 := by
    rw [smul_neg] at hc
    exact neg_eq_iff_add_eq_zero.mp hc
  simpa only [← add_smul, htwo, one_smul] using hz

end ConcreteChart

/-- info: 'QSearch.InducedRegularSource.translation_action' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.translation_action
/-- info: 'QSearch.InducedRegularSource.cocycle_mul' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.cocycle_mul
/-- info: 'QSearch.InducedRegularSource.potential_kernel' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.potential_kernel
/-- info: 'QSearch.InducedRegularSource.oracle_to_matrix' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.oracle_to_matrix
/-- info: 'QSearch.InducedRegularSource.oracle_aligned_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.oracle_aligned_to_scalar
/-- info: 'QSearch.InducedRegularSource.scalar_branch_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.scalar_branch_trace
/-- info: 'QSearch.InducedRegularSource.vectorRightChart' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.vectorRightChart
/-- info: 'QSearch.InducedRegularSource.vector_fiber_noncentral' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.InducedRegularSource.vector_fiber_noncentral

end
end QSearch.InducedRegularSource
