import Formal.ClassThreeMonomial
import Formal.WeightedPhaseErasure

/-!
# Universal class-three source phase bounds

Public bilinear structure maps are lifted coefficientwise, not evaluated at
hidden parameters. Two applications of the same filtered-polynomial theorem
bound operational weight and hidden-parameter degree separately. These are
compiler bounds, not a proof of the ambient BCH degree or source preparation.
-/

namespace QSearch.ClassThreePhaseBounds

open MvPolynomial WeightedPhaseErasure
open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F σ ι κ : Type*} [Field F] [Fintype ι] [Fintype κ]

abbrev Poly (F σ : Type*) [CommRing F] := MvPolynomial σ F

def basisVector (i : ι) : ι → F := fun j => if j = i then 1 else 0

theorem basis_expansion (u : ι → F) : u = ∑ i, u i • basisVector i := by
  classical
  ext j
  simp [basisVector]

def bilinear (B : (ι → F) →ₗ[F] (κ → F) →ₗ[F] F)
    (u : ι → Poly F σ) (v : κ → Poly F σ) : Poly F σ :=
  ∑ i, ∑ j, C (B (basisVector i) (basisVector j)) * u i * v j

theorem eval_bilinear (B : (ι → F) →ₗ[F] (κ → F) →ₗ[F] F)
    (u : ι → Poly F σ) (v : κ → Poly F σ) (z : σ → F) :
    aeval z (bilinear B u v) = B (fun i => aeval z (u i)) (fun j => aeval z (v j)) := by
  classical
  conv_rhs => rw [basis_expansion (fun i => aeval z (u i)),
    basis_expansion (fun j => aeval z (v j))]
  simp only [bilinear, map_sum, map_mul, aeval_C, Algebra.algebraMap_self,
    RingHom.id_apply, map_smul, LinearMap.sum_apply, LinearMap.smul_apply, smul_eq_mul]
  rw [Finset.sum_comm]
  simp [Finset.mul_sum, mul_comm, mul_left_comm]

theorem bilinear_bounded (w : σ → ℕ) (B : (ι → F) →ₗ[F] (κ → F) →ₗ[F] F)
    {u : ι → Poly F σ} {v : κ → Poly F σ} {a b : ℕ}
    (hu : ∀ i, u i ∈ bounded w a) (hv : ∀ j, v j ∈ bounded w b) :
    bilinear B u v ∈ bounded w (a+b) := by
  apply (bounded w (a+b)).sum_mem
  intro i _
  apply (bounded w (a+b)).sum_mem
  intro j _
  simpa using bounded_mul w
    (bounded_mul w (C_bounded w (B (basisVector i) (basisVector j))) (hu i)) (hv j)

def dot (u v : κ → Poly F σ) : Poly F σ := ∑ j, u j * v j

theorem dot_bounded (w : σ → ℕ) {u v : κ → Poly F σ} {a b : ℕ}
    (hu : ∀ j, u j ∈ bounded w a) (hv : ∀ j, v j ∈ bounded w b) :
    dot u v ∈ bounded w (a+b) :=
  (bounded w (a+b)).sum_mem (fun j _ => bounded_mul w (hu j) (hv j))

def frequency (v : κ → F) : (κ → F) →ₗ[F] F where
  toFun u := ∑ j, v j * u j
  map_add' u v := by simp [mul_add, Finset.sum_add_distrib]
  map_smul' r u := by simp [Finset.mul_sum, mul_left_comm]

variable (S : ClassThreeMonomial.StructureMaps F (ι → F) (κ → F))

def betaComponent (j : κ) : (ι → F) →ₗ[F] (ι → F) →ₗ[F] F :=
  (LinearMap.proj j).compRight F |>.comp S.beta

def beta (a x : ι → Poly F σ) (j : κ) : Poly F σ :=
  bilinear (betaComponent S j) a x

omit [Fintype κ] in
theorem eval_beta (a x : ι → Poly F σ) (z : σ → F) (j : κ) :
    aeval z (beta S a x j) = S.beta (fun i => aeval z (a i)) (fun i => aeval z (x i)) j := by
  rw [beta, eval_bilinear]
  rfl

/-- Expanded form of rawPhase minus the shifted-frequency term. The mixed
quadratic parameter term is retained; the carrier is not hidden advice. -/
def sourcePhase (a : ι → Poly F σ) (b : κ → Poly F σ) (c : Poly F σ)
    (x : ι → Poly F σ) (mu : κ → Poly F σ) : Poly F σ :=
  c + C (2 : F)⁻¹ * (bilinear S.gamma a x - bilinear S.delta x b)
    + C (12 : F)⁻¹ * (bilinear S.delta a (beta S a x) - bilinear S.delta x (beta S a x))
    - dot mu b - C (2 : F)⁻¹ * dot mu (beta S a x)
    - C (2 : F)⁻¹ * bilinear S.delta a b
    - C ((2 : F)⁻¹ * (2 : F)⁻¹) * bilinear S.delta a (beta S a x)

theorem eval_sourcePhase (a : ι → Poly F σ) (b : κ → Poly F σ) (c : Poly F σ)
    (x : ι → Poly F σ) (mu : κ → Poly F σ) (z : σ → F) :
    aeval z (sourcePhase S a b c x mu) =
      ClassThreeMonomial.phase S
        ((fun i => aeval z (a i)), (fun j => aeval z (b j)), aeval z c)
        ((fun i => aeval z (x i)), frequency (fun j => aeval z (mu j))) := by
  simp only [sourcePhase, map_add, map_sub, map_mul, aeval_C, eval_bilinear,
    dot, map_sum, ClassThreeMonomial.phase, ClassThreeMonomial.rawPhase,
    LinearMap.add_apply, LinearMap.smul_apply, map_add, map_smul, smul_eq_mul,
    frequency, LinearMap.coe_mk, AddHom.coe_mk, Algebra.algebraMap_self, RingHom.id_apply,
    eval_beta, mul_add, Finset.mul_sum, mul_comm, div_eq_mul_inv]
  ring

theorem constant_mul_bounded (w : σ → ℕ) (r : F) {P : Poly F σ} {d : ℕ}
    (h : P ∈ bounded w d) : C r * P ∈ bounded w d := by
  simpa using bounded_mul w (C_bounded w r) h

/-- One symbolic estimate used with two different weight functions. -/
theorem sourcePhase_bounded (w : σ → ℕ)
    (a : ι → Poly F σ) (b : κ → Poly F σ) (c : Poly F σ)
    (x : ι → Poly F σ) (mu : κ → Poly F σ) (A X C E : ℕ)
    (ha : ∀ i, a i ∈ bounded w A) (hb : ∀ j, b j ∈ bounded w A)
    (hc : c ∈ bounded w C) (hx : ∀ i, x i ∈ bounded w X)
    (hm : ∀ j, mu j ∈ bounded w X)
    (hC : C ≤ E) (hAX : A+X ≤ E) (hAAX : A+(A+X) ≤ E)
    (hXAX : X+(A+X) ≤ E) (hAA : A+A ≤ E) :
    sourcePhase S a b c x mu ∈ bounded w E := by
  have hbeta j : beta S a x j ∈ bounded w (A+X) :=
    bilinear_bounded w (betaComponent S j) ha hx
  have hgamma := bounded_mono w hAX (bilinear_bounded w S.gamma ha hx)
  have hxb := bounded_mono w (by omega : X+A ≤ E) (bilinear_bounded w S.delta hx hb)
  have habeta := bounded_mono w hAAX (bilinear_bounded w S.delta ha hbeta)
  have hxbeta := bounded_mono w hXAX (bilinear_bounded w S.delta hx hbeta)
  have hmb := bounded_mono w (by omega : X+A ≤ E) (dot_bounded w hm hb)
  have hmbeta := bounded_mono w hXAX (dot_bounded w hm hbeta)
  have hab := bounded_mono w hAA (bilinear_bounded w S.delta ha hb)
  exact (bounded w E).sub_mem ((bounded w E).sub_mem
    ((bounded w E).sub_mem ((bounded w E).sub_mem
      ((bounded w E).add_mem ((bounded w E).add_mem (bounded_mono w hC hc)
        (constant_mul_bounded w _ ((bounded w E).sub_mem hgamma hxb)))
        (constant_mul_bounded w _ ((bounded w E).sub_mem habeta hxbeta))) hmb)
      (constant_mul_bounded w _ hmbeta)) (constant_mul_bounded w _ hab))
    (constant_mul_bounded w _ habeta)

theorem operational_bound (w : σ → ℕ)
    (a : ι → Poly F σ) (b : κ → Poly F σ) (c : Poly F σ)
    (x : ι → Poly F σ) (mu : κ → Poly F σ) (D cdeg : ℕ)
    (ha : ∀ i, a i ∈ bounded w D) (hb : ∀ j, b j ∈ bounded w D)
    (hc : c ∈ bounded w cdeg) (hx : ∀ i, x i ∈ bounded w D)
    (hm : ∀ j, mu j ∈ bounded w D) :
    sourcePhase S a b c x mu ∈ bounded w (max cdeg (3*D)) :=
  sourcePhase_bounded S w a b c x mu D D cdeg _ ha hb hc hx hm
    (by omega) (by omega) (by omega) (by omega) (by omega)

theorem parameter_bound (w : σ → ℕ)
    (a : ι → Poly F σ) (b : κ → Poly F σ) (c : Poly F σ)
    (x : ι → Poly F σ) (mu : κ → Poly F σ)
    (ha : ∀ i, a i ∈ bounded w 1) (hb : ∀ j, b j ∈ bounded w 1)
    (hc : c ∈ bounded w 1) (hx : ∀ i, x i ∈ bounded w 0)
    (hm : ∀ j, mu j ∈ bounded w 0) :
    sourcePhase S a b c x mu ∈ bounded w 2 :=
  sourcePhase_bounded S w a b c x mu 1 0 1 2 ha hb hc hx hm
    (by decide) (by decide) (by decide) (by decide) (by decide)

section PublicInputs

variable {Q J H : Type*} [Fintype Q] [Fintype J] [Fintype H]

abbrev Variable (Q J H : Type*) := Q ⊕ J ⊕ H

def operationalWeight (w : J → ℕ) : Variable Q J H → ℕ :=
  Sum.elim (fun _ => 1) (Sum.elim w (fun _ => 0))

def parameterWeight : Variable Q J H → ℕ :=
  Sum.elim (fun _ => 0) (Sum.elim (fun _ => 0) (fun _ => 1))

def shifted (Y : Q → F) (s : F) (i : Q) : Poly F (Variable Q J H) :=
  C (Y i) + C s * X (Sum.inl i)

/-- All components use the SAME parameter variable set. Public coefficients
may select a component or incorporate its measured central character. -/
def potential (nu : H → Q → ℕ) (coeff : H → F) (Y : Q → F) (s : F) :
    Poly F (Variable Q J H) :=
  ∑ h, C (coeff h) * X (Sum.inr (Sum.inr h)) * ∏ i, shifted Y s i ^ nu h i

/-- A row of L^-1(t,zeta). The spectator contributes a public constant. -/
def carrier (row : J → F) (offset : F) : Poly F (Variable Q J H) :=
  C offset + ∑ j, C (row j) * X (Sum.inr (Sum.inl j))

theorem bounded_pow (w : σ → ℕ) {P : Poly F σ} {d : ℕ}
    (h : P ∈ bounded w d) (n : ℕ) : P^n ∈ bounded w (n*d) := by
  induction n with
  | zero => simpa using C_bounded w (1 : F)
  | succ n ih => simpa [pow_succ, Nat.succ_mul] using bounded_mul w ih h

theorem bounded_product (w : σ → ℕ) (P : Q → Poly F σ) (d : Q → ℕ)
    (h : ∀ i, P i ∈ bounded w (d i)) : ∏ i, P i ∈ bounded w (∑ i, d i) := by
  classical
  have aux (t : Finset Q) : ∏ i ∈ t, P i ∈ bounded w (∑ i ∈ t, d i) := by
    induction t using Finset.induction_on with
    | empty => simpa using C_bounded w (1 : F)
    | @insert i t hi ih => simpa [hi] using bounded_mul w (h i) ih
  exact aux Finset.univ

omit [Fintype Q] [Fintype J] [Fintype H] in
theorem shifted_bounded (w : Variable Q J H → ℕ) (Y : Q → F) (s : F)
    (d : ℕ) (hw : ∀ i, w (Sum.inl i) ≤ d) (i : Q) :
    shifted Y s i ∈ bounded w d :=
  (bounded w d).add_mem (bounded_mono w (Nat.zero_le d) (C_bounded w (Y i)))
    (constant_mul_bounded w s (bounded_mono w (hw i) (X_bounded w (Sum.inl i))))

omit [Fintype J] in
theorem potential_bounded (w : Variable Q J H → ℕ)
    (nu : H → Q → ℕ) (coeff : H → F) (Y : Q → F) (s : F) (A B E : ℕ)
    (hh : ∀ h, w (Sum.inr (Sum.inr h)) ≤ A)
    (hq : ∀ i, w (Sum.inl i) ≤ B)
    (hdegree : ∀ h, coeff h ≠ 0 → A + (∑ i, nu h i)*B ≤ E) :
    potential nu coeff Y s ∈ bounded w E := by
  classical
  apply (bounded w E).sum_mem
  intro h _
  by_cases hz : coeff h = 0
  · simp [hz]
  have hprod := bounded_product w
    (fun i => (shifted Y s i : Poly F (Variable Q J H)) ^ nu h i)
    (fun i => nu h i * B)
    (fun i => bounded_pow w (shifted_bounded w Y s B hq i) (nu h i))
  have hp := bounded_mul w
    (constant_mul_bounded w (coeff h)
      (bounded_mono w (hh h) (X_bounded w (Sum.inr (Sum.inr h))))) hprod
  apply bounded_mono w (hdegree h hz)
  simpa [Finset.sum_mul] using hp

omit [Fintype J] in
theorem potential_operational (w : J → ℕ)
    (nu : H → Q → ℕ) (coeff : H → F) (Y : Q → F) (s : F) (D : ℕ)
    (hdegree : ∀ h, coeff h ≠ 0 → ∑ i, nu h i ≤ D) :
    potential nu coeff Y s ∈ bounded (operationalWeight w) D := by
  apply potential_bounded (operationalWeight w) nu coeff Y s 0 1 D
  · intro h; exact le_refl 0
  · intro i; exact le_refl 1
  · simpa using hdegree

omit [Fintype J] in
theorem potential_parameter (nu : H → Q → ℕ) (coeff : H → F) (Y : Q → F) (s : F) :
    (potential nu coeff Y s : Poly F (Variable Q J H)) ∈ bounded parameterWeight 1 := by
  apply potential_bounded parameterWeight nu coeff Y s 1 0 1
  · intro h; exact le_refl 1
  · intro i; exact le_refl 0
  · simp

omit [Fintype Q] [Fintype H] in
theorem carrier_bounded (w : Variable Q J H → ℕ) (row : J → F) (offset : F) (D : ℕ)
    (hw : ∀ j, w (Sum.inr (Sum.inl j)) ≤ D) : carrier row offset ∈ bounded w D := by
  apply (bounded w D).add_mem (bounded_mono w (Nat.zero_le D) (C_bounded w offset))
  exact (bounded w D).sum_mem (fun j _ =>
    constant_mul_bounded w (row j) (bounded_mono w (hw j) (X_bounded w _)))

omit [Fintype J] in
theorem eval_potential (nu : H → Q → ℕ) (coeff : H → F) (Y : Q → F) (s : F)
    (q : Q → F) (t : J → F) (theta : H → F) :
    aeval (Sum.elim q (Sum.elim t theta)) (potential nu coeff Y s) =
      ∑ h, coeff h * theta h * ∏ i, (Y i + s*q i)^nu h i := by
  simp [potential, shifted]

omit [Fintype Q] [Fintype H] in
theorem eval_carrier (row : J → F) (offset : F)
    (q : Q → F) (t : J → F) (theta : H → F) :
    aeval (Sum.elim q (Sum.elim t theta)) (carrier row offset) = offset + ∑ j, row j*t j := by
  simp [carrier]

/-- A single source block, with fixed shared coefficient names. No hidden
coefficient values appear in this public compilation data. -/
structure Block (F Q J H ι κ : Type*) where
  exponents : H → Q → ℕ
  aCoeff : ι → H → F
  bCoeff : κ → H → F
  cCoeff : H → F
  outcome : Q → F
  scale : F
  aRow : ι → J → F
  aOffset : ι → F
  muRow : κ → J → F
  muOffset : κ → F

def compileBlock (data : Block F Q J H ι κ) : Poly F (Variable Q J H) :=
  sourcePhase S
    (fun i => potential data.exponents (data.aCoeff i) data.outcome data.scale)
    (fun j => potential data.exponents (data.bCoeff j) data.outcome data.scale)
    (potential data.exponents data.cCoeff data.outcome data.scale)
    (fun i => carrier (data.aRow i) (data.aOffset i))
    (fun j => carrier (data.muRow j) (data.muOffset j))

theorem compileBlock_operational (w : J → ℕ) (D cdeg : ℕ) (hw : ∀ j, w j ≤ D)
    (data : Block F Q J H ι κ)
    (ha : ∀ i h, data.aCoeff i h ≠ 0 → ∑ q, data.exponents h q ≤ D)
    (hb : ∀ j h, data.bCoeff j h ≠ 0 → ∑ q, data.exponents h q ≤ D)
    (hc : ∀ h, data.cCoeff h ≠ 0 → ∑ q, data.exponents h q ≤ cdeg) :
    compileBlock S data ∈ bounded (operationalWeight w) (max cdeg (3*D)) := by
  apply operational_bound S (operationalWeight w)
  · intro i; exact potential_operational w _ _ _ _ D (ha i)
  · intro j; exact potential_operational w _ _ _ _ D (hb j)
  · exact potential_operational w _ _ _ _ cdeg hc
  · intro i; exact carrier_bounded _ _ _ D hw
  · intro j; exact carrier_bounded _ _ _ D hw

theorem compileBlock_parameter (data : Block F Q J H ι κ) :
    compileBlock S data ∈ bounded parameterWeight 2 := by
  apply parameter_bound S parameterWeight
  · intro i; exact potential_parameter _ _ _ _
  · intro j; exact potential_parameter _ _ _ _
  · exact potential_parameter _ _ _ _
  · intro i; exact carrier_bounded _ _ _ 0 (fun _ => le_refl 0)
  · intro j; exact carrier_bounded _ _ _ 0 (fun _ => le_refl 0)

theorem compileBlock_evaluation (data : Block F Q J H ι κ)
    (q : Q → F) (t : J → F) (theta : H → F) :
    aeval (Sum.elim q (Sum.elim t theta)) (compileBlock S data) =
      ClassThreeMonomial.phase S
        ((fun i => ∑ h, data.aCoeff i h * theta h *
            ∏ v, (data.outcome v + data.scale*q v)^data.exponents h v),
         (fun j => ∑ h, data.bCoeff j h * theta h *
            ∏ v, (data.outcome v + data.scale*q v)^data.exponents h v),
         ∑ h, data.cCoeff h * theta h *
            ∏ v, (data.outcome v + data.scale*q v)^data.exponents h v)
        ((fun i => data.aOffset i + ∑ j, data.aRow i j*t j),
         frequency (fun j => data.muOffset j + ∑ k, data.muRow j k*t k)) := by
  rw [compileBlock, eval_sourcePhase]
  simp_rw [eval_potential, eval_carrier]

variable {I : Type*} [Fintype I]

def compileBatch (structureMaps : I → ClassThreeMonomial.StructureMaps F (ι → F) (κ → F))
    (data : I → Block F Q J H ι κ) : Poly F (Variable Q J H) :=
  -∑ i, compileBlock (structureMaps i) (data i)

theorem compileBatch_bounds
    (structureMaps : I → ClassThreeMonomial.StructureMaps F (ι → F) (κ → F))
    (data : I → Block F Q J H ι κ) (w : J → ℕ) (D cdeg : ℕ) (hw : ∀ j, w j ≤ D)
    (ha : ∀ n i h, (data n).aCoeff i h ≠ 0 → ∑ q, (data n).exponents h q ≤ D)
    (hb : ∀ n j h, (data n).bCoeff j h ≠ 0 → ∑ q, (data n).exponents h q ≤ D)
    (hc : ∀ n h, (data n).cCoeff h ≠ 0 → ∑ q, (data n).exponents h q ≤ cdeg) :
    compileBatch structureMaps data ∈ bounded (operationalWeight w) (max cdeg (3*D)) ∧
    compileBatch structureMaps data ∈ bounded parameterWeight 2 := by
  constructor
  · exact (bounded _ _).neg_mem ((bounded _ _).sum_mem (fun n _ =>
      compileBlock_operational (structureMaps n) w D cdeg hw (data n) (ha n) (hb n) (hc n)))
  · exact (bounded _ _).neg_mem ((bounded _ _).sum_mem (fun n _ =>
      compileBlock_parameter (structureMaps n) (data n)))

/-- No branch-dependent hidden values enter the compiler; evaluation is a
semantic theorem for every single assignment of the shared parameters. -/
theorem compileBatch_evaluation
    (structureMaps : I → ClassThreeMonomial.StructureMaps F (ι → F) (κ → F))
    (data : I → Block F Q J H ι κ) (q : Q → F) (t : J → F) (theta : H → F) :
    aeval (Sum.elim q (Sum.elim t theta)) (compileBatch structureMaps data) =
    -∑ n, ClassThreeMonomial.phase (structureMaps n)
        ((fun i => ∑ h, (data n).aCoeff i h * theta h *
            ∏ v, ((data n).outcome v + (data n).scale*q v)^(data n).exponents h v),
         (fun j => ∑ h, (data n).bCoeff j h * theta h *
            ∏ v, ((data n).outcome v + (data n).scale*q v)^(data n).exponents h v),
         ∑ h, (data n).cCoeff h * theta h *
            ∏ v, ((data n).outcome v + (data n).scale*q v)^(data n).exponents h v)
        ((fun i => (data n).aOffset i + ∑ j, (data n).aRow i j*t j),
         frequency (fun j => (data n).muOffset j + ∑ k, (data n).muRow j k*t k)) := by
  simp only [compileBatch, map_neg, map_sum, compileBlock_evaluation]

end PublicInputs

/-- info: 'QSearch.ClassThreePhaseBounds.eval_bilinear' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms eval_bilinear
/-- info: 'QSearch.ClassThreePhaseBounds.eval_sourcePhase' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms eval_sourcePhase
/-- info: 'QSearch.ClassThreePhaseBounds.operational_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms operational_bound
/-- info: 'QSearch.ClassThreePhaseBounds.parameter_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms parameter_bound
/-- info: 'QSearch.ClassThreePhaseBounds.potential_operational' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms potential_operational
/-- info: 'QSearch.ClassThreePhaseBounds.potential_parameter' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms potential_parameter
/-- info: 'QSearch.ClassThreePhaseBounds.compileBatch_bounds' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms compileBatch_bounds
/-- info: 'QSearch.ClassThreePhaseBounds.compileBatch_evaluation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms compileBatch_evaluation

end

end QSearch.ClassThreePhaseBounds
