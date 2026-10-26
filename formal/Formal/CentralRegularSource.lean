import Formal.CosetMatrixSource
import Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality
import Mathlib.Tactic

/-!
# Complete right-abelian Fourier instrument for regular coset sources

The public chart exposes an abelian RIGHT fiber, which need not be central
or even normal. Central charts are a special case. No irreducibility or
complete nonabelian QFT is assumed. Hidden potentials occur only in the
source correctness theorem, never in the Fourier amplitudes. The namespace
retains its historical name; the source theorems use RightAbelianChart.
-/

namespace QSearch.CentralRegularSource

open scoped BigOperators
open AffineSupportErasure
noncomputable section
attribute [local instance] Classical.propDecidable

variable {N T C : Type*} [Group N] [AddCommGroup C]

structure CentralChart (N T C : Type*) [Group N] [AddCommGroup C] where
  coordinates : N ≃ T × C
  sectionMap : T → N
  center : Multiplicative C →* N
  chart : ∀ x z, coordinates.symm (x, z) = center (Multiplicative.ofAdd z) * sectionMap x
  central : ∀ z g, center (Multiplicative.ofAdd z) * g = g * center (Multiplicative.ofAdd z)

/-- A public transversal and an abelian fiber on the RIGHT. No centrality,
normality or quotient-group structure is assumed by this instrument. -/
structure RightAbelianChart (N T C : Type*) [Group N] [AddCommGroup C] where
  coordinates : N ≃ T × C
  sectionMap : T → N
  fiber : Multiplicative C →* N
  chart : ∀ x z, coordinates.symm (x, z) = sectionMap x * fiber (Multiplicative.ofAdd z)

def CentralChart.toRightAbelianChart (S : CentralChart N T C) : RightAbelianChart N T C where
  coordinates := S.coordinates
  sectionMap := S.sectionMap
  fiber := S.center
  chart x z := (S.chart x z).trans (S.central z (S.sectionMap x))

variable (S : RightAbelianChart N T C)

def action (g : N) (x : T) : T × C := S.coordinates (g * S.sectionMap x)

theorem element_action (g : N) (x : T) (z : C) :
    g * S.coordinates.symm (x, z) =
      S.coordinates.symm ((action S g x).1, z + (action S g x).2) := by
  have he : g * S.sectionMap x =
      S.sectionMap (action S g x).1 * S.fiber (Multiplicative.ofAdd (action S g x).2) := by
    rw [← S.chart]
    exact (S.coordinates.symm_apply_apply _).symm
  rw [S.chart, ← mul_assoc, he, mul_assoc, S.chart, add_comm z]
  rw [show Multiplicative.ofAdd ((action S g x).2 + z) =
    Multiplicative.ofAdd (action S g x).2 * Multiplicative.ofAdd z from rfl, map_mul]

theorem coordinate_action (g : N) (x : T) (z : C) :
    S.coordinates (g * S.coordinates.symm (x, z)) =
      ((action S g x).1, z + (action S g x).2) := by
  rw [element_action, Equiv.apply_symm_apply]

theorem action_one (x : T) : action S 1 x = (x, 0) := by
  have hs : S.sectionMap x = S.coordinates.symm (x, 0) := by simp [S.chart]
  simp [action, hs]

theorem action_mul (g h : N) (x : T) :
    action S (g*h) x =
      ((action S g (action S h x).1).1,
       (action S h x).2 + (action S g (action S h x).1).2) := by
  have hs : h * S.sectionMap x = S.coordinates.symm (action S h x) :=
    (S.coordinates.symm_apply_apply _).symm
  change S.coordinates ((g*h)*S.sectionMap x) = _
  rw [mul_assoc, hs]
  exact coordinate_action S g (action S h x).1 (action S h x).2

section Characters
variable [Fintype C]

theorem character_unit (chi : AddChar C ℂ) (z : C) : chi z * star (chi z) = 1 := by
  have hc : star (chi z) = chi (-z) := (chi.map_neg_eq_conj z).symm
  rw [hc, ← chi.map_add_eq_mul]
  simp

theorem dual_orthogonality (z w : C) :
    (∑ chi : AddChar C ℂ, star (chi z) * chi w) =
      if z = w then (Fintype.card C : ℂ) else 0 := by
  have h (chi : AddChar C ℂ) : star (chi z) * chi w = chi (w-z) := by
    rw [mul_comm]
    exact CosetSourceFourier.character_product chi (character_unit chi) w z
  simp_rw [h]
  rw [AddChar.sum_apply_eq_ite]
  simp [sub_eq_zero, eq_comm]

end Characters

section Instrument
variable [Fintype T] [Fintype C]

def fourierAmplitude (chi : AddChar C ℂ) (x : T) (a : T × C) : ℂ :=
  if x = a.1 then uniformAmplitude C * chi a.2 else 0

theorem one_character_column (chi : AddChar C ℂ) (a b : T × C) :
    (∑ x, star (fourierAmplitude chi x a) * fourierAmplitude chi x b) =
      if a.1 = b.1 then invSize C * star (chi a.2) * chi b.2 else 0 := by
  classical
  by_cases hab : a.1 = b.1
  · simp only [fourierAmplitude, apply_ite, star_mul, star_zero, ite_mul, zero_mul,
      mul_zero]
    simp only [Finset.sum_ite_eq', Finset.mem_univ, ite_true, hab]
    have hn := uniformAmplitude_normalized (V := C)
    calc
      _ = (uniformAmplitude C * star (uniformAmplitude C)) * star (chi a.2) * chi b.2 := by ring
      _ = _ := by rw [hn]
  · simp [fourierAmplitude, apply_ite, ite_mul, hab, Ne.symm hab]

/-- Sum over ALL characters and the retained carrier. This proves a
complete instrument, not just the norm of one formal representation. -/
theorem fourier_complete (a b : T × C) :
    (∑ chi : AddChar C ℂ, ∑ x,
      star (fourierAmplitude chi x a) * fourierAmplitude chi x b) =
      if a = b then 1 else 0 := by
  classical
  simp_rw [one_character_column]
  by_cases hab : a.1 = b.1
  · simp only [hab, ite_true, mul_assoc, ← Finset.mul_sum]
    rw [dual_orthogonality]
    have hc : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
    by_cases hz : a.2 = b.2
    · have he : a = b := Prod.ext hab hz
      simp [he, invSize, hc]
    · have he : a ≠ b := fun h => hz (congrArg Prod.snd h)
      simp [hz, he]
  · have he : a ≠ b := fun h => hab (congrArg Prod.fst h)
    simp [hab, he]

end Instrument

section Regular
variable [Fintype N] [Fintype T] [Fintype C]

/-- Invert the NORMAL group coordinate, then apply positive right-fiber Fourier.
This fixes the right-regular to left-regular convention. -/
def amplitude (chi : AddChar C ℂ) (x : T) (n : N) : ℂ :=
  fourierAmplitude chi x (S.coordinates n⁻¹)

omit [Fintype N] in
theorem instrument_complete (a b : N) :
    (∑ chi : AddChar C ℂ, ∑ x, star (amplitude S chi x a) * amplitude S chi x b) =
      if a = b then 1 else 0 := by
  rw [show (∑ chi : AddChar C ℂ, ∑ x, star (amplitude S chi x a) * amplitude S chi x b) =
    ∑ chi : AddChar C ℂ, ∑ x, star (fourierAmplitude chi x (S.coordinates a⁻¹)) *
      fourierAmplitude chi x (S.coordinates b⁻¹) from rfl, fourier_complete]
  simp only [S.coordinates.injective.eq_iff, inv_inj]

def sector (chi : AddChar C ℂ) (g : N) : Matrix T T ℂ :=
  fun x y => if x = (action S g y).1 then chi (action S g y).2 else 0

def regularBranch (chi : AddChar C ℂ) (g : N) (x y : T) : ℂ :=
  ∑ a, ∑ b, amplitude S chi x a * (if b = a*g then 1 else 0) * star (amplitude S chi y b)

theorem regular_branch (chi : AddChar C ℂ) (g : N) (x y : T) :
    regularBranch S chi g x y = sector S chi g x y := by
  classical
  have rel (a b : N) : b = a*g ↔ a = b*g⁻¹ := by
    constructor
    · intro h; rw [h]; group
    · intro h; rw [h]; group
  have collapse : regularBranch S chi g x y =
      ∑ b, amplitude S chi x (b*g⁻¹) * star (amplitude S chi y b) := by
    rw [regularBranch, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro b _
    simp only [rel, mul_ite, mul_one, mul_zero, ite_mul, zero_mul]
    simp
  rw [collapse]
  let e : N ≃ T × C := (Equiv.inv N).trans S.coordinates
  let f (a : T × C) : ℂ :=
    fourierAmplitude chi x (S.coordinates (g * S.coordinates.symm a)) *
      star (fourierAmplitude chi y a)
  have he (b : N) : amplitude S chi x (b*g⁻¹) * star (amplitude S chi y b) = f (e b) := by
    simp [amplitude, f, e]
  simp_rw [he]
  rw [Equiv.sum_comp e f]
  simp only [f, Fintype.sum_prod_type, coordinate_action]
  have inner (u : T) (z : C) :
      fourierAmplitude chi x ((action S g u).1, z+(action S g u).2) *
        star (fourierAmplitude chi y (u,z)) =
      if y = u then
        (if x = (action S g u).1 then invSize C * chi (action S g u).2 else 0) else 0 := by
    by_cases hy : y = u <;> by_cases hx : x = (action S g u).1
    · simp only [fourierAmplitude, hy, hx, ite_true, star_mul, chi.map_add_eq_mul]
      calc
        _ = (uniformAmplitude C * star (uniformAmplitude C)) *
          (chi z * star (chi z)) * chi (action S g u).2 := by ring
        _ = _ := by rw [uniformAmplitude_normalized, character_unit, mul_one]
    · simp [fourierAmplitude, hy, hx]
    · simp [fourierAmplitude, hy, hx]
    · simp [fourierAmplitude, hy, hx]
  simp_rw [inner]
  have hc : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [sector, invSize, hc]

omit [Fintype N] [Fintype T] [Fintype C] in
theorem sector_one (chi : AddChar C ℂ) (x y : T) :
    sector S chi 1 x y = if x = y then 1 else 0 := by simp [sector, action_one]

end Regular

section Representation
variable [Fintype T] [Fintype C] [DecidableEq T]

def representation (chi : AddChar C ℂ) : N →* Matrix T T ℂ where
  toFun g := sector S chi g
  map_one' := by ext x y; simp [sector_one, Matrix.one_apply]
  map_mul' g h := by
    ext x y
    simp [Matrix.mul_apply, sector, mul_ite, ite_mul, action_mul,
      chi.map_add_eq_mul, mul_comm]

omit [Fintype T] in
theorem sector_adjoint (chi : AddChar C ℂ) (g : N) (x y : T) :
    star (sector S chi g y x) = sector S chi g⁻¹ x y := by
  have ha := action_mul S g⁻¹ g x
  have hb := action_mul S g g⁻¹ y
  rw [inv_mul_cancel, action_one] at ha
  rw [mul_inv_cancel, action_one] at hb
  have hp : y = (action S g x).1 ↔ x = (action S g⁻¹ y).1 := by
    constructor
    · intro h; rw [h]; exact congrArg Prod.fst ha
    · intro h; rw [h]; exact congrArg Prod.fst hb
  by_cases hy : y = (action S g x).1
  · have hz : (action S g⁻¹ y).2 = -(action S g x).2 := by
      rw [hy]
      exact eq_neg_of_add_eq_zero_right (congrArg Prod.snd ha).symm
    simp only [sector, ite_eq_left hy, ite_eq_left (hp.mp hy)]
    rw [hz]
    exact (chi.map_neg_eq_conj _).symm
  · have hx : x ≠ (action S g⁻¹ y).1 := fun h => hy (hp.mpr h)
    simp [sector, hy, hx]

theorem representation_unitary (chi : AddChar C ℂ) :
    CosetMatrixSource.UnitaryRepresentation (representation S chi) := by
  intro g
  have hs : (representation S chi g).conjTranspose = representation S chi g⁻¹ := by
    ext x y
    exact sector_adjoint S chi g x y
  rw [hs, ← map_mul, inv_mul_cancel, map_one]

theorem potential_gauge (chi : AddChar C ℂ) (a b : N) :
    sector S chi (a⁻¹*b) =
      (representation S chi a).conjTranspose * representation S chi b :=
  CosetMatrixSource.potential_matrix_product (representation S chi) (representation_unitary S chi) a b

end Representation

section Source
variable {F V G : Type*} [Field F] [AddCommGroup V] [Module F V] [Group G]
  [Fintype N] [Fintype T] [Fintype C] [Fintype V] [Fintype G]

def centralBranch (coordinates : G ≃ V × N) (H : Subgroup G)
    (chi : AddChar C ℂ) (q r : V) (x y : T) : ℂ :=
  ∑ a, ∑ b, amplitude S chi x a *
    CosetSourceFourier.groupEntry H (coordinates.symm (q,a)) (coordinates.symm (r,b)) *
    star (amplitude S chi y b)

omit [Fintype V] in
theorem source_identity (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (hact : ∀ q a u, coordinates (coordinates.symm (q,a) * (hidden u : G)) =
      (q+(u : V), a*(potential q)⁻¹*potential (q+(u : V))))
    (chi : AddChar C ℂ) (q r : V) (x y : T) :
    centralBranch S coordinates H chi q r x y =
      if r-q ∈ U then invSize G * sector S chi ((potential q)⁻¹*potential r) x y else 0 := by
  classical
  by_cases hu : r-q ∈ U
  · have he (a b : N) : CosetSourceFourier.groupEntry H
        (coordinates.symm (q,a)) (coordinates.symm (r,b)) =
        invSize G * (if b = a*((potential q)⁻¹*potential r) then 1 else 0) := by
      simp [CosetSourceFourier.groupEntry,
        CosetMatrixSource.coset_relation coordinates H U potential hidden hact, hu, mul_assoc]
    simp only [centralBranch, he, hu, ite_true]
    rw [← regular_branch S chi ((potential q)⁻¹*potential r) x y]
    simp only [regularBranch, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro b _
    ring
  · simp [centralBranch, CosetSourceFourier.groupEntry,
      CosetMatrixSource.coset_relation coordinates H U potential hidden hact, hu]

include S in
omit [AddCommGroup V] [Group G] in
theorem source_size (coordinates : G ≃ V × N) :
    invSize G = invSize V * invSize T * invSize C := by
  simp only [invSize, Fintype.card_congr coordinates, Fintype.card_congr S.coordinates,
    Fintype.card_prod, Nat.cast_mul, mul_inv_rev]
  ring

/-- This is a physical branch mass: completeness was proved independently.
It is NOT the irreducible Plancherel expression d^2/|N|. -/
theorem sector_trace (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (potential : V → N) (hidden : U ≃ H)
    (hact : ∀ q a u, coordinates (coordinates.symm (q,a) * (hidden u : G)) =
      (q+(u : V), a*(potential q)⁻¹*potential (q+(u : V))))
    (chi : AddChar C ℂ) :
    (∑ q, ∑ x, centralBranch S coordinates H chi q q x x) = invSize C := by
  have : Nonempty T := ⟨(S.coordinates 1).1⟩
  simp_rw [source_identity S coordinates H U potential hidden hact chi]
  simp only [sub_self, U.zero_mem, ite_true, inv_mul_cancel, sector_one,
    mul_one, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  rw [source_size S coordinates]
  have hv : (Fintype.card V : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have ht : (Fintype.card T : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp only [invSize]
  field_simp

variable {O : Type*} [Fintype O]

/-- Actual hiding-output trace followed by the public right-fiber instrument. -/
def oracleBranch (coordinates : G ≃ V × N) (f : G → O)
    (chi : AddChar C ℂ) (q r : V) (x y : T) : ℂ :=
  ∑ a, ∑ b, amplitude S chi x a *
    (∑ label, CosetMatrixSource.hidingAmplitude f (coordinates.symm (q,a)) label *
      star (CosetMatrixSource.hidingAmplitude f (coordinates.symm (r,b)) label)) *
    star (amplitude S chi y b)

omit [AddCommGroup V] [Fintype T] [Fintype V] in
theorem oracle_trace (coordinates : G ≃ V × N) (H : Subgroup G) (f : G → O)
    (hides : ∀ g g', f g = f g' ↔ g⁻¹*g' ∈ H)
    (chi : AddChar C ℂ) (q r : V) (x y : T) :
    oracleBranch S coordinates f chi q r x y = centralBranch S coordinates H chi q r x y := by
  simp only [oracleBranch, CosetMatrixSource.hiding_output_trace H f hides]
  rfl

/-- The source action is derived from the shared section-word potential.
Only coordinates, f and right-fiber Fourier occur in the operational left side. -/
theorem oracle_source_from_normal_chart
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
    (chi : AddChar C ℂ) (q r : V) (x y : T) :
    oracleBranch S coordinates f chi q r x y =
      invSize C * (if r-q ∈ U then invSize V * invSize T *
        sector S chi ((potential q)⁻¹*potential r) x y else 0) := by
  have hact : ∀ q a u, coordinates (coordinates.symm (q,a) * (hidden u : G)) =
      (q+(u : V), a*(potential q)⁻¹*potential (q+(u : V))) := by
    intro q a u
    simpa only [hvalues] using CosetMatrixSource.coordinate_action U pi hpi sectionMap
      hiddenHom normalMap coordinates chart potential hpotential q a u
  rw [oracle_trace S coordinates H f hides,
    source_identity S coordinates H U potential hidden hact, source_size S coordinates]
  split_ifs <;> ring

end Source

/-- info: 'QSearch.CentralRegularSource.coordinate_action' depends on axioms: [Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.coordinate_action
/-- info: 'QSearch.CentralRegularSource.fourier_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.fourier_complete
/-- info: 'QSearch.CentralRegularSource.instrument_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.instrument_complete
/-- info: 'QSearch.CentralRegularSource.regular_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.regular_branch
/-- info: 'QSearch.CentralRegularSource.potential_gauge' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.potential_gauge
/-- info: 'QSearch.CentralRegularSource.sector_trace' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.sector_trace
/--
info: 'QSearch.CentralRegularSource.oracle_source_from_normal_chart' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms QSearch.CentralRegularSource.oracle_source_from_normal_chart

end
end QSearch.CentralRegularSource
