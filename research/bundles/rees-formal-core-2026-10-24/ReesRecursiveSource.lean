import ReesStageInstrument
import Mathlib.Algebra.BigOperators.Intervals

/-!
A source tree denotes separately prepared leaves, not reuse of a quantum
register. Recorded branches remain unnormalized throughout composition.
-/
namespace QSearch.ReesRecursiveSource
open scoped BigOperators
open ReesGroupBridge ReesCentralInstrument ReesCancellation ReesQuotients ReesStageInstrument
noncomputable section
attribute [local instance] Classical.propDecidable

universe u v w
inductive SourceTree (I : ℕ → Type u) (J : ℕ → Type v) (top : ℕ) : ℕ → Type (max u v) where
  | leaf : SourceTree I J top top
  | node {d : ℕ} (label : J d) (children : I d → SourceTree I J top (d+1)) : SourceTree I J top d

section Trees
variable {I : ℕ → Type u} {J : ℕ → Type v} {S : ℕ → Type w} {top d : ℕ}

def evaluateTree (leaf : S top) (merge : ∀ k, J k → (I k → S (k+1)) → S k) :
    {k : ℕ} → SourceTree I J top k → S k
  | _, .leaf => leaf
  | _, .node label children => merge _ label (fun i => evaluateTree leaf merge (children i))

theorem tree_source (source : ∀ k, S k) (merge : ∀ k, J k → (I k → S (k+1)) → S k)
    (step : ∀ k label, merge k label (fun _ => source (k+1)) = source k)
    (tree : SourceTree I J top d) : evaluateTree (source top) merge tree = source d := by
  induction tree with
  | leaf => rfl
  | node label children ih =>
    simp only [evaluateTree, ih]
    exact step _ label

variable [∀ k, Fintype (I k)]

def treeWeight (mass : ∀ k, J k → ℂ) : {k : ℕ} → SourceTree I J top k → ℂ
  | _, .leaf => 1
  | _, .node label children => (∏ i, treeWeight mass (children i)) * mass _ label

theorem tree_record [∀ k, MulAction ℂ (S k)] (source : ∀ k, S k)
    (merge : ∀ k, J k → (I k → S (k+1)) → S k) (mass : ∀ k, J k → ℂ)
    (homogeneous : ∀ k label (states : I k → S (k+1)) (weights : I k → ℂ),
      merge k label (fun i => weights i • states i) = (∏ i, weights i) • merge k label states)
    (step : ∀ k label, merge k label (fun _ => source (k+1)) = mass k label • source k)
    (tree : SourceTree I J top d) :
    evaluateTree (source top) merge tree = treeWeight mass tree • source d := by
  induction tree with
  | leaf => exact (one_smul ℂ _).symm
  | node label children ih =>
    simp only [evaluateTree, ih, homogeneous, step, smul_smul, treeWeight]

def leafCount : {k : ℕ} → SourceTree I J top k → ℕ
  | _, .leaf => 1
  | _, .node _ children => ∑ i, leafCount (children i)

theorem duplicate_children_pay_separately (label : J d) (child : SourceTree I J top (d+1)) :
    leafCount (.node label (fun _ => child)) = Fintype.card (I d) * leafCount child := by
  simp only [leafCount, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, Nat.cast_id]

omit [∀ k, Fintype (I k)] in
theorem tree_stage_le_top [∀ k, Nonempty (I k)] (tree : SourceTree I J top d) : d ≤ top := by
  induction tree with
  | leaf => exact le_refl _
  | @node k label children ih =>
    exact Nat.le_of_succ_le (ih (Classical.choice (inferInstance : Nonempty (I k))))

theorem leafCount_product [∀ k, Nonempty (I k)] (tree : SourceTree I J top d) :
    leafCount tree = ∏ k ∈ Finset.Ico d top, Fintype.card (I k) := by
  induction tree with
  | leaf => simp [leafCount]
  | @node k label children ih =>
    have hkt : k < top := tree_stage_le_top
      (children (Classical.choice (inferInstance : Nonempty (I k))))
    rw [Finset.prod_eq_prod_Ico_succ_bot hkt]
    simp only [leafCount, ih, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, Nat.cast_id]

end Trees

section Plans
variable {F G Q I J : Type*} [Field F] [LieRing G] [LieAlgebra F G] [Group G]
  [LieRing Q] [LieAlgebra F Q] [Group Q] [Fintype G] [Fintype I] [Fintype J]

/-- Public measurement/solver data; no hidden subalgebra or desired output. -/
structure MeasurementPlan (step : StepGeometry F G Q) (I J : Type*) [Fintype I] [Fintype J] where
  psi : AddChar F ℂ
  unitary : ∀ x, psi x * star (psi x) = 1
  lambda : J → step.projection.ker →ₗ[F] F
  complete : ∀ z, (∑ l, linearCharacter psi (lambda l) z) =
    if z = 1 then (Fintype.card (Multiplicative step.projection.ker) : ℂ) else 0
  scales : (I → J) → I → F
  nonempty : ∀ labels, ∃ i, scales labels i ≠ 0
  moments : ∀ labels, (∑ i, scales labels i ^ step.degree • lambda (labels i)) = 0

theorem plan_packet_nonempty (step : StepGeometry F G Q) (plan : MeasurementPlan step I J) :
    Nonempty I := by
  by_contra hn
  have : IsEmpty I := not_nonempty_iff.mp hn
  obtain ⟨i, _⟩ := plan.nonempty (fun i => isEmptyElim i)
  exact isEmptyElim i

end Plans

section Actual
open ReesLie LieModule
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] [Group L] [Fintype L] {n : ℕ}
variable (law : PolynomialGroupLaw F L) (points : Fin n → F)
  (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
  (nilpotent : lowerCentralSeries F L L n = ⊥)

def ReesPlan (d : ℕ) (I J : Type*) [Fintype I] [Fintype J] :=
  letI := stageGroup law points nilpotent (d+1)
  letI := stageGroup law points nilpotent d
  letI := stageFintype points nilpotent (d+1)
  MeasurementPlan (reesStep law points distinct nonzero nilpotent d) I J

def reesSource (h : LieSubalgebra F L) (d : ℕ) :
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) →
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) → ℂ :=
  letI := stageGroup law points nilpotent d
  letI := stageFintype points nilpotent d
  sourceEntry (subgroup (stageLaw law points nilpotent d) (stageHidden points nilpotent d h))

variable {I J : Type*} [Fintype I] [Fintype J]

def reesRecord (d : ℕ) (plan : ReesPlan law points distinct nonzero nilpotent d I J)
    (labels : I → J)
    (states : I → (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) → ℂ) :
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) →
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) → ℂ :=
  letI := stageGroup law points nilpotent (d+1)
  letI := stageGroup law points nilpotent d
  letI := stageFintype points nilpotent (d+1)
  letI := stageFintype points nilpotent d
  recordOutput (reesStep law points distinct nonzero nilpotent d)
    plan.psi plan.lambda plan.scales labels states

def reesMass (h : LieSubalgebra F L) (d : ℕ)
    (plan : ReesPlan law points distinct nonzero nilpotent d I J) (labels : I → J) : ℂ :=
  letI := stageGroup law points nilpotent (d+1)
  letI := stageGroup law points nilpotent d
  letI := stageFintype points nilpotent (d+1)
  recordMass (reesStep law points distinct nonzero nilpotent d)
    (stageHidden points nilpotent (d+1) h) plan.psi plan.lambda labels

theorem rees_record_source (h : LieSubalgebra F L) (d : ℕ)
    (plan : ReesPlan law points distinct nonzero nilpotent d I J) (labels : I → J) :
    reesRecord law points distinct nonzero nilpotent d plan labels
      (fun _ => reesSource law points nilpotent h (d+1)) =
    reesMass law points distinct nonzero nilpotent h d plan labels • reesSource law points nilpotent h d := by
  let := stageGroup law points nilpotent (d+1)
  let := stageGroup law points nilpotent d
  let := stageFintype points nilpotent (d+1)
  let := stageFintype points nilpotent d
  funext q r
  have hr := record_source (reesStep law points distinct nonzero nilpotent d)
    (stageHidden points nilpotent (d+1) h)
    (fun a ha x => stageDilation_hidden points distinct nonzero nilpotent (d+1) a ha h x)
    plan.psi plan.unitary plan.lambda plan.scales plan.nonempty plan.moments labels q r
  rw [rees_hidden_image law points distinct nonzero nilpotent d h] at hr
  exact hr

theorem rees_record_homogeneous (d : ℕ) (plan : ReesPlan law points distinct nonzero nilpotent d I J)
    (labels : I → J) (states : I → (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) → ℂ) (weights : I → ℂ) :
    reesRecord law points distinct nonzero nilpotent d plan labels (fun i => weights i • states i) =
      (∏ i, weights i) • reesRecord law points distinct nonzero nilpotent d plan labels states := by
  let := stageGroup law points nilpotent (d+1)
  let := stageGroup law points nilpotent d
  let := stageFintype points nilpotent (d+1)
  let := stageFintype points nilpotent d
  funext q r
  exact record_scaled_sources _ _ _ _ _ _ _ _ _

theorem rees_mass_complete (h : LieSubalgebra F L) (d : ℕ)
    (plan : ReesPlan law points distinct nonzero nilpotent d I J) :
    (∑ labels : I → J, reesMass law points distinct nonzero nilpotent h d plan labels) = 1 := by
  let := stageGroup law points nilpotent (d+1)
  let := stageGroup law points nilpotent d
  let := stageFintype points nilpotent (d+1)
  exact record_mass_complete _ _ plan.psi plan.unitary plan.lambda plan.complete

def reesAverage (d : ℕ) (plan : ReesPlan law points distinct nonzero nilpotent d I J)
    (states : I → (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) → ℂ) :=
  ∑ labels : I → J, reesRecord law points distinct nonzero nilpotent d plan labels states

theorem rees_average_source (h : LieSubalgebra F L) (d : ℕ)
    (plan : ReesPlan law points distinct nonzero nilpotent d I J) :
    reesAverage law points distinct nonzero nilpotent d plan
      (fun _ => reesSource law points nilpotent h (d+1)) = reesSource law points nilpotent h d := by
  simp_rw [reesAverage, rees_record_source law points distinct nonzero nilpotent h d plan]
  rw [← Finset.sum_smul, rees_mass_complete, one_smul]

variable {Packets Labels : ℕ → Type*} [∀ k, Fintype (Packets k)] [∀ k, Fintype (Labels k)]

theorem rees_record_tree (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    {top d : ℕ} (tree : SourceTree Packets (fun k => Packets k → Labels k) top d) :
    evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ) (reesSource law points nilpotent h top)
      (fun k => reesRecord law points distinct nonzero nilpotent k (plans k)) tree =
    treeWeight (fun k => reesMass law points distinct nonzero nilpotent h k (plans k)) tree •
      reesSource law points nilpotent h d := by
  exact tree_record (reesSource law points nilpotent h) _ _
    (fun k => rees_record_homogeneous law points distinct nonzero nilpotent k (plans k))
    (fun k => rees_record_source law points distinct nonzero nilpotent h k (plans k)) tree

theorem rees_average_tree (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    {top d : ℕ} (tree : SourceTree Packets (fun _ => Unit) top d) :
    evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ) (reesSource law points nilpotent h top)
      (fun k _ => reesAverage law points distinct nonzero nilpotent k (plans k)) tree =
      reesSource law points nilpotent h d := by
  exact tree_source (reesSource law points nilpotent h) _
    (fun k _ => rees_average_source law points distinct nonzero nilpotent h k (plans k)) tree

theorem rees_tree_leafCount
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    {top d : ℕ} (tree : SourceTree Packets (fun k => Packets k → Labels k) top d) :
    leafCount tree = ∏ k ∈ Finset.Ico d top, Fintype.card (Packets k) := by
  have : ∀ k, Nonempty (Packets k) := by
    intro k
    let := stageGroup law points nilpotent (k+1)
    let := stageGroup law points nilpotent k
    let := stageFintype points nilpotent (k+1)
    exact plan_packet_nonempty _ (plans k)
  exact leafCount_product tree

end Actual
end
end QSearch.ReesRecursiveSource
