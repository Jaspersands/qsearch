import Formal.RetainedFourier

/-!
# Vector-center BCH group and its original-oracle Fourier source

The scalar phase data are projections of ONE physical group with center
coordinate C. Projection by a label, including zero, never replaces C by
its image. Public structure maps and the original hiding oracle determine
the operational source; hidden potentials remain correctness witnesses.
-/

namespace QSearch.VectorCentralSource

noncomputable section
open scoped BigOperators
open AffineSupportErasure
attribute [local instance] Classical.propDecidable

variable {F A B C : Type*} [Field F]
  [AddCommGroup A] [Module F A] [AddCommGroup B] [Module F B]
  [AddCommGroup C] [Module F C]

structure StructureMaps (F A B C : Type*) [Field F]
    [AddCommGroup A] [Module F A] [AddCommGroup B] [Module F B]
    [AddCommGroup C] [Module F C] where
  beta : A →ₗ[F] A →ₗ[F] B
  gamma : A →ₗ[F] A →ₗ[F] C
  delta : A →ₗ[F] B →ₗ[F] C
  beta_alt : ∀ a, beta a a = 0
  gamma_alt : ∀ a, gamma a a = 0
  jacobi : ∀ a b x, delta a (beta b x)+delta b (beta x a)+delta x (beta a b) = 0

variable (S : StructureMaps F A B C)

def project (lam : C →ₗ[F] F) : ClassThreeMonomial.StructureMaps F A B where
  beta := S.beta
  gamma := S.gamma.compr₂ lam
  delta := S.delta.compr₂ lam
  beta_alt := S.beta_alt
  gamma_alt a := by simp [S.gamma_alt]
  jacobi a b x := by
    change lam (S.delta a (S.beta b x))+lam (S.delta b (S.beta x a))+
      lam (S.delta x (S.beta a b)) = 0
    rw [← map_add, ← map_add, S.jacobi, map_zero]

@[ext] structure Element (S : StructureMaps F A B C) where
  a : A
  b : B
  c : C

def coordinates : Element S ≃ (A × B) × C where
  toFun g := ((g.a,g.b),g.c)
  invFun t := ⟨t.1.1,t.1.2,t.2⟩
  left_inv g := by cases g; rfl
  right_inv t := by rcases t with ⟨⟨a,b⟩,c⟩; rfl

instance [Fintype A] [Fintype B] [Fintype C] : Fintype (Element S) :=
  Fintype.ofEquiv ((A × B) × C) (coordinates S).symm

def scalar (lam : C →ₗ[F] F) (g : Element S) : ClassThreeMonomial.Element F A B :=
  (g.a,g.b,lam g.c)

def product (g h : Element S) : Element S where
  a := g.a+h.a
  b := g.b+h.b+(2 : F)⁻¹ • S.beta g.a h.a
  c := g.c+h.c+(2 : F)⁻¹ • (S.gamma g.a h.a+S.delta g.a h.b-S.delta h.a g.b)
    +(12 : F)⁻¹ • (S.delta g.a (S.beta g.a h.a)-S.delta h.a (S.beta g.a h.a))

theorem scalar_product (lam : C →ₗ[F] F) (g h : Element S) :
    scalar S lam (product S g h) =
      ClassThreeMonomial.product (project S lam) (scalar S lam g) (scalar S lam h) := by
  apply Prod.ext
  · rfl
  apply Prod.ext
  · rfl
  simp only [scalar, product, ClassThreeMonomial.product, project, LinearMap.compr₂_apply,
    map_add, map_sub, map_smul, smul_eq_mul, div_eq_mul_inv]
  ring

/-- All linear probes separate central vectors. A single measured label need not. -/
theorem scalar_ext (g h : Element S)
    (he : ∀ lam : C →ₗ[F] F, scalar S lam g = scalar S lam h) : g = h := by
  apply Element.ext
  · exact congrArg Prod.fst (he 0)
  · exact congrArg (fun t => t.2.1) (he 0)
  · apply Module.eval_apply_injective F
    ext lam
    exact congrArg (fun t => t.2.2) (he lam)

omit [AddCommGroup A] [Module F A] in
theorem carrier_card [Fintype A] [Fintype B] [Fintype (B →ₗ[F] F)] :
    Fintype.card (ClassThreeMonomial.Carrier F A B) = Fintype.card (A × B) := by
  have hb : Fintype.card (B →ₗ[F] F) = Fintype.card B :=
    Fintype.card_congr (Module.Basis.ofVectorSpace F B).toDualEquiv.symm.toEquiv
  simp only [ClassThreeMonomial.Carrier, Fintype.card_prod, hb]

variable [Fact ((2 : F) ≠ 0)] [Fact ((3 : F) ≠ 0)]

instance : Group (Element S) where
  mul := product S
  one := ⟨0,0,0⟩
  inv g := ⟨-g.a,-g.b,-g.c⟩
  mul_assoc g h k := by
    apply scalar_ext S
    intro lam
    change scalar S lam (product S (product S g h) k) =
      scalar S lam (product S g (product S h k))
    simp_rw [scalar_product]
    exact ClassThreeMonomial.product_assoc (project S lam) Fact.out Fact.out _ _ _
  one_mul g := by
    change product S ⟨0,0,0⟩ g = g
    apply Element.ext <;> simp [product]
  mul_one g := by
    change product S g ⟨0,0,0⟩ = g
    apply Element.ext <;> simp [product]
  inv_mul_cancel g := by
    change product S ⟨-g.a,-g.b,-g.c⟩ g = ⟨0,0,0⟩
    apply Element.ext <;> simp [product, S.beta_alt, S.gamma_alt]

theorem bch_associative (g h k : Element S) : (g*h)*k = g*(h*k) := mul_assoc g h k

@[simp] theorem mul_a (g h : Element S) : (g*h).a = g.a+h.a := rfl
@[simp] theorem mul_b (g h : Element S) :
    (g*h).b = g.b+h.b+(2 : F)⁻¹ • S.beta g.a h.a := rfl
@[simp] theorem mul_c (g h : Element S) :
    (g*h).c = g.c+h.c+(2 : F)⁻¹ • (S.gamma g.a h.a+S.delta g.a h.b-S.delta h.a g.b)
      +(12 : F)⁻¹ • (S.delta g.a (S.beta g.a h.a)-S.delta h.a (S.beta g.a h.a)) := rfl

@[simp] theorem scalar_mul (lam : C →ₗ[F] F) (g h : Element S) :
    scalar S lam (g*h) =
      ClassThreeMonomial.product (project S lam) (scalar S lam g) (scalar S lam h) :=
  scalar_product S lam g h

@[simp] theorem scalar_one (lam : C →ₗ[F] F) : scalar S lam 1 = 0 := by
  change (0,0,lam 0) = 0
  simp

def centerMap : Multiplicative C →* Element S where
  toFun z := ⟨0,0,Multiplicative.toAdd z⟩
  map_one' := rfl
  map_mul' z w := by apply Element.ext <;> simp

def sectionMap (t : A × B) : Element S := ⟨t.1,t.2,0⟩

def centralChart : CentralRegularSource.RightAbelianChart (Element S) (A × B) C where
  coordinates := coordinates S
  sectionMap := sectionMap S
  fiber := centerMap S
  chart t z := by apply Element.ext <;> simp [coordinates, centerMap, sectionMap]

theorem sector_projection (chi : AddChar F ℂ) (lam : C →ₗ[F] F)
    (g : Element S) (x y : A × B) :
    CentralRegularSource.sector (centralChart S) (RetainedFourier.linearCharacter chi lam)
      g x y =
      (let out := ClassThreeMonomial.product (project S lam) (scalar S lam g) (y.1,y.2,0)
       if x = (out.1,out.2.1) then chi out.2.2 else 0) := by
  have hp : ClassThreeMonomial.product (project S lam) (scalar S lam g) (y.1,y.2,0) =
      scalar S lam (g*sectionMap S y) := by
    rw [scalar_mul]
    simp [scalar, sectionMap]
  rw [hp]
  simp [CentralRegularSource.sector, CentralRegularSource.action, centralChart,
    coordinates, scalar, RetainedFourier.linearCharacter, sectionMap]

section Finite
variable [Fintype B]

def retainedSector (chi : AddChar F ℂ) (lam : C →ₗ[F] F) (g : Element S) :
    Matrix (ClassThreeMonomial.Carrier F A B) (ClassThreeMonomial.Carrier F A B) ℂ :=
  fun out inp => ∑ y, ∑ z, RetainedFourier.amplitude chi out.2 z *
    CentralRegularSource.sector (centralChart S) (RetainedFourier.linearCharacter chi lam)
      g (out.1,z) (inp.1,y) * star (RetainedFourier.amplitude chi inp.2 y)

theorem retained_sector_formula [Fintype F] (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (lam : C →ₗ[F] F) (g : Element S) (out inp : ClassThreeMonomial.Carrier F A B) :
    retainedSector S chi lam g out inp =
      if out = ClassThreeMonomial.displacement (project S lam) (scalar S lam g) inp then
        chi (ClassThreeMonomial.phase (project S lam) (scalar S lam g) inp) else 0 := by
  unfold retainedSector
  simp_rw [sector_projection]
  exact RetainedFourier.classThree_formula (project S lam) chi hchi (scalar S lam g)
    inp.1 out.1 inp.2 out.2

section Representation
variable [Fintype F] [Fintype A] [Fintype (B →ₗ[F] F)]

def representation (chi : AddChar F ℂ) (hchi : chi ≠ 1) (lam : C →ₗ[F] F) :
    Element S →* Matrix (ClassThreeMonomial.Carrier F A B) (ClassThreeMonomial.Carrier F A B) ℂ where
  toFun := retainedSector S chi lam
  map_one' := by
    ext out inp
    simp [retained_sector_formula S chi hchi, ClassThreeMonomial.displacement,
      ClassThreeMonomial.phase_zero, Matrix.one_apply]
  map_mul' g h := by
    ext out inp
    simp only [Matrix.mul_apply, retained_sector_formula S chi hchi,
      mul_ite, mul_zero, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
    rw [scalar_mul, ← ClassThreeMonomial.displacement_comp]
    split_ifs
    · simpa only [mul_comm] using
        (ClassThreeMonomial.amplitude_comp (project S lam) Fact.out Fact.out chi
          (scalar S lam g) (scalar S lam h) inp).symm
    · ring

theorem representation_unitary (chi : AddChar F ℂ) (hchi : chi ≠ 1) (lam : C →ₗ[F] F) :
    CosetMatrixSource.UnitaryRepresentation (representation S chi hchi lam) := by
  intro g
  ext x y
  have hi := (ClassThreeMonomial.displacement_bijective (project S lam) (scalar S lam g)).injective
  by_cases h : x = y
  · subst y
    simp [representation, Matrix.mul_apply, Matrix.conjTranspose_apply,
      retained_sector_formula S chi hchi, apply_ite, mul_comm]
    exact CentralRegularSource.character_unit chi _
  · simp [representation, Matrix.mul_apply, Matrix.conjTranspose_apply,
      retained_sector_formula S chi hchi, apply_ite, ite_mul,
      hi.eq_iff, h, Ne.symm h]

theorem retained_potential_gauge (chi : AddChar F ℂ) (hchi : chi ≠ 1)
    (lam : C →ₗ[F] F) (a b : Element S) :
    retainedSector S chi lam (a⁻¹*b) =
      (retainedSector S chi lam a).conjTranspose * retainedSector S chi lam b :=
  CosetMatrixSource.potential_matrix_product (representation S chi hchi lam)
    (representation_unitary S chi hchi lam) a b

end Representation

variable [Fintype A] [Fintype C]

/-- Reindex the COMPLETE physical central instrument by linear labels.
Neither a faithful/nonzero label nor a scalar central quotient is used. -/
theorem central_complete [Fintype (C →ₗ[F] F)]
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (g h : Element S) :
    (∑ lam : C →ₗ[F] F, ∑ t : A × B,
      star (CentralRegularSource.amplitude (centralChart S)
        (RetainedFourier.linearCharacter chi lam) t g) *
      CentralRegularSource.amplitude (centralChart S)
        (RetainedFourier.linearCharacter chi lam) t h) =
      if g = h then 1 else 0 := by
  have he := Equiv.sum_comp (RetainedFourier.characterEquiv (B := C) chi hchi)
    (fun ch : AddChar C ℂ => ∑ t : A × B,
      star (CentralRegularSource.amplitude (centralChart S) ch t g) *
        CentralRegularSource.amplitude (centralChart S) ch t h)
  change (∑ lam : C →ₗ[F] F, ∑ t : A × B,
      star (CentralRegularSource.amplitude (centralChart S)
        (RetainedFourier.linearCharacter chi lam) t g) *
      CentralRegularSource.amplitude (centralChart S)
        (RetainedFourier.linearCharacter chi lam) t h) = _ at he
  rw [he]
  exact CentralRegularSource.instrument_complete (centralChart S) g h

section Source
variable {V G O : Type*} [AddCommGroup V] [Module F V] [Group G]
  [Fintype V] [Fintype G] [Fintype O]

/-- Actual hiding-output trace, central branch and COHERENT B transform.
No subgroup, hidden retraction or potential occurs in this definition. -/
def oracleBranch (chart : G ≃ V × Element S) (f : G → O)
    (chi : AddChar F ℂ) (lam : C →ₗ[F] F) (q r : V)
    (out inp : ClassThreeMonomial.Carrier F A B) : ℂ :=
  ∑ y, ∑ z, RetainedFourier.amplitude chi out.2 z *
    CentralRegularSource.oracleBranch (centralChart S) chart f
      (RetainedFourier.linearCharacter chi lam) q r (out.1,z) (inp.1,y) *
    star (RetainedFourier.amplitude chi inp.2 y)

/-- Original hiding oracle to the explicit class-three monomial source.
The prefactor is the FULL 1/|C| even when lam=0. All hidden data occur
only as witnesses for the normal-first chart and section-word identity. -/
theorem original_source [Fintype F] [Fintype (B →ₗ[F] F)]
    (chart : G ≃ V × Element S) (H : Subgroup G) (f : G → O)
    (hides : ∀ g g', f g = f g' ↔ g⁻¹*g' ∈ H)
    (U : Submodule F V) (pi : V →ₗ[F] U) (hpi : ∀ u : U, pi (u : V) = u)
    (publicSection : V → G) (hidden : U ≃ H) (hiddenHom : Multiplicative U →* G)
    (hvalues : ∀ u : U, hiddenHom (Multiplicative.ofAdd u) = (hidden u : G))
    (normalMap : Element S →* G)
    (hchart : ∀ q a, chart.symm (q,a) = normalMap a * publicSection q)
    (potential : V → Element S)
    (hpotential : ∀ q, normalMap (potential q) =
      CosetMatrixSource.sectionPotential U pi publicSection hiddenHom q)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (lam : C →ₗ[F] F)
    (q r : V) (out inp : ClassThreeMonomial.Carrier F A B) :
    oracleBranch S chart f chi lam q r out inp =
      invSize C * (if r-q ∈ U then invSize V * invSize (A × B) *
        ((retainedSector S chi lam (potential q)).conjTranspose *
          retainedSector S chi lam (potential r)) out inp
        else 0) := by
  rw [← retained_potential_gauge S chi hchi lam (potential q) (potential r)]
  unfold oracleBranch retainedSector
  simp_rw [CentralRegularSource.oracle_source_from_normal_chart (centralChart S)
    chart H f hides U pi hpi publicSection hidden hiddenHom hvalues normalMap hchart
    potential hpotential (RetainedFourier.linearCharacter chi lam)]
  by_cases hu : r-q ∈ U
  · simp only [hu, ite_true, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro y _
    apply Finset.sum_congr rfl
    intro z _
    ring
  · simp [hu]

end Source
end Finite

/-- info: 'QSearch.VectorCentralSource.scalar_product' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.scalar_product

/-- info: 'QSearch.VectorCentralSource.scalar_ext' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.scalar_ext

/-- info: 'QSearch.VectorCentralSource.carrier_card' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.carrier_card

/-- info: 'QSearch.VectorCentralSource.bch_associative' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.bch_associative

/-- info: 'QSearch.VectorCentralSource.sector_projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.sector_projection

/-- info: 'QSearch.VectorCentralSource.retained_sector_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.retained_sector_formula

/-- info: 'QSearch.VectorCentralSource.central_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.central_complete

/-- info: 'QSearch.VectorCentralSource.representation_unitary' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.representation_unitary

/-- info: 'QSearch.VectorCentralSource.retained_potential_gauge' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.retained_potential_gauge

/-- info: 'QSearch.VectorCentralSource.original_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.VectorCentralSource.original_source

end
end QSearch.VectorCentralSource
