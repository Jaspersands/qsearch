import ReesQuotients

/-!
Physical source conversion on every constructed Rees stage. Geometry is
public and has no hidden-subgroup field. Independent source copies are an
explicit tensor-product input, never inferred from their marginals.
-/

namespace QSearch.ReesStageInstrument
open scoped BigOperators
open ReesGroupBridge ReesCancellation ReesCentralInstrument ReesQuotients
noncomputable section
attribute [local instance] Classical.propDecidable

section Geometry
variable {F G Q : Type*} [Field F] [LieRing G] [LieAlgebra F G] [Group G]
  [LieRing Q] [LieAlgebra F Q] [Group Q]

structure StepGeometry (F G Q : Type*) [Field F] [LieRing G] [LieAlgebra F G] [Group G]
    [LieRing Q] [LieAlgebra F Q] [Group Q] where
  lawG : PolynomialGroupLaw F G
  lawQ : PolynomialGroupLaw F Q
  same_expression : lawG.expression = lawQ.expression
  projection : G →ₗ⁅F⁆ Q
  degree : ℕ
  positive : 0 < degree
  kernel_central : ∀ x, projection x = 0 → ∀ y : G, ⁅x,y⁆ = 0
  dilation : ∀ a : F, a ≠ 0 → G ≃ₗ⁅F⁆ G
  kernel_scaled : ∀ a ha x, projection x = 0 → dilation a ha x = a^degree • x
  sigma : Q → G
  section_right : ∀ q, projection (sigma q) = q

def projectionGroup (step : StepGeometry F G Q) : G →* Q :=
  polynomialGroupHom step.lawG step.lawQ step.same_expression step.projection

def kernelEmbed (step : StepGeometry F G Q) : Multiplicative step.projection.ker →* G where
  toFun z := z.toAdd.val
  map_one' := step.lawG.one_eq.symm
  map_mul' x y := (commuting_mul_add step.lawG x.toAdd.val y.toAdd.val
    (step.kernel_central x.toAdd.val x.toAdd.property y.toAdd.val)).symm

theorem kernelEmbed_central (step : StepGeometry F G Q)
    (z : Multiplicative step.projection.ker) (g : G) :
    kernelEmbed step z * g = g * kernelEmbed step z :=
  (commuting_group step.lawG z.toAdd.val g
    (step.kernel_central z.toAdd.val z.toAdd.property g)).eq

theorem kernelEmbed_range (step : StepGeometry F G Q) :
    (kernelEmbed step).range = (projectionGroup step).ker := by
  apply Subgroup.ext
  intro x
  constructor
  · rintro ⟨z, rfl⟩
    change step.projection z.toAdd.val = 1
    rw [step.lawQ.one_eq]
    exact z.toAdd.property
  · intro hx
    have hz : step.projection x = 0 := by
      change step.projection x = 1 at hx
      rwa [step.lawQ.one_eq] at hx
    exact ⟨Multiplicative.ofAdd ⟨x,hz⟩, rfl⟩

theorem hiddenCenter_projection (step : StepGeometry F G Q) (H : Subgroup G) (g : G) :
    inHiddenCenter H (kernelEmbed step) g ↔ projectionGroup step g ∈ H.map (projectionGroup step) := by
  constructor
  · rintro ⟨h, hh, z, rfl⟩
    refine ⟨h, hh, ?_⟩
    have hz : projectionGroup step (kernelEmbed step z) = 1 := by
      apply (kernelEmbed_range step ▸ (show kernelEmbed step z ∈ (kernelEmbed step).range from ⟨z,rfl⟩))
    rw [map_mul, hz, mul_one]
  · rintro ⟨h, hh, he⟩
    have hk : h⁻¹*g ∈ (projectionGroup step).ker := by
      change projectionGroup step (h⁻¹*g) = 1
      rw [map_mul, map_inv, he, inv_mul_cancel]
    rw [← kernelEmbed_range] at hk
    obtain ⟨z, hz⟩ := hk
    refine ⟨h, hh, z, ?_⟩
    rw [hz]
    group

theorem step_relation (step : StepGeometry F G Q) (H : Subgroup G) (q r : Q) :
    quotientRelation H (kernelEmbed step) step.sigma q r ↔
      r⁻¹*q ∈ H.map (projectionGroup step) := by
  unfold quotientRelation
  rw [hiddenCenter_projection, map_mul, map_inv]
  change (step.projection (step.sigma r))⁻¹ * step.projection (step.sigma q) ∈ _ ↔ _
  rw [step.section_right, step.section_right]

def actionDilation (step : StepGeometry F G Q) (a : F) : G ≃* G :=
  if ha : a ≠ 0 then polynomialGroupEquiv step.lawG (step.dilation a ha) else MulEquiv.refl _

theorem actionDilation_center (step : StepGeometry F G Q) (a : F) (ha : a ≠ 0)
    (z : Multiplicative step.projection.ker) :
    actionDilation step a (kernelEmbed step z) = kernelEmbed step (scaleEquiv a step.degree z) := by
  simp only [actionDilation, scaleEquiv, dite_eq_left ha]
  change step.dilation a ha z.toAdd.val = a^step.degree • z.toAdd.val
  exact step.kernel_scaled a ha z.toAdd.val z.toAdd.property

variable {I : Type*} [Fintype I]

def stepAction (step : StepGeometry F G Q) (s : I → F) : Q → I → G :=
  controlledAction (fun i => s i ≠ 0) (fun i => actionDilation step (s i)) step.sigma

def stepCertificate (step : StepGeometry F G Q) (h : LieSubalgebra F G)
    (preserves : ∀ a ha x, step.dilation a ha x ∈ h ↔ x ∈ h)
    (psi : AddChar F ℂ) (lambda : I → step.projection.ker →ₗ[F] F) (s : I → F)
    (nonempty : ∃ i, s i ≠ 0) (moment : (∑ i, s i ^ step.degree • lambda i) = 0) :
    CancellationCertificate (subgroup step.lawG h) (kernelEmbed step)
      (fun i => linearCharacter psi (lambda i)) (stepAction step s)
      (quotientRelation (subgroup step.lawG h) (kernelEmbed step) step.sigma) := by
  apply automorphismCertificate _ _ _ (fun i => s i ≠ 0) nonempty
    (fun i => actionDilation step (s i)) (fun i => scaleEquiv (s i) step.degree)
  · intro i hi x
    simp only [actionDilation, dite_eq_left hi]
    exact preserves (s i) hi x
  · intro i hi z
    exact actionDilation_center step (s i) hi z
  · exact moment_cancels psi lambda s step.degree step.positive moment

end Geometry

section Physical
variable {G C : Type*} [Group G] [CommGroup C] [Fintype C]

def measuredState (embed : C →* G) (chi : C →* ℂ) (rho : G → G → ℂ)
    (x y : G) : ℂ :=
  (Fintype.card C : ℂ)⁻¹ ^ 2 * ∑ w, ∑ z,
    chi z * star (chi w) * rho (x * (embed z)⁻¹) (y * (embed w)⁻¹)

theorem measuredState_scale (embed : C →* G) (chi : C →* ℂ) (rho : G → G → ℂ)
    (c : ℂ) (x y : G) :
    measuredState embed chi (fun x y => c*rho x y) x y = c * measuredState embed chi rho x y := by
  simp only [measuredState]
  simp_rw [show ∀ w z, chi z * star (chi w) * (c*rho (x*(embed z)⁻¹) (y*(embed w)⁻¹)) =
    c*(chi z * star (chi w) * rho (x*(embed z)⁻¹) (y*(embed w)⁻¹)) from fun _ _ => by ring]
  simp_rw [← Finset.mul_sum]
  ring

end Physical

section Record
variable {F G Q I J : Type*} [Field F] [LieRing G] [LieAlgebra F G] [Group G]
  [LieRing Q] [LieAlgebra F Q] [Group Q] [Fintype G] [Fintype Q] [Fintype I]

def recordOutput (step : StepGeometry F G Q) (psi : AddChar F ℂ)
    (lambda : J → step.projection.ker →ₗ[F] F) (scales : (I → J) → I → F)
    (labels : I → J) (states : I → G → G → ℂ) (q r : Q) : ℂ :=
  controlledDiscard (stepAction step (scales labels))
    (fun (_ _ : Q × Unit) => (Fintype.card Q : ℂ)⁻¹)
    (fun x y => ∏ i, measuredState (kernelEmbed step) (linearCharacter psi (lambda (labels i)))
      (states i) (x i) (y i)) q r () ()

def recordMass (step : StepGeometry F G Q) (h : LieSubalgebra F G) (psi : AddChar F ℂ)
    (lambda : J → step.projection.ker →ₗ[F] F) (labels : I → J) : ℂ :=
  ∏ i, ∑ x, measuredEntry (subgroup step.lawG h) (kernelEmbed step)
    (linearCharacter psi (lambda (labels i))) x x

theorem record_source (step : StepGeometry F G Q) (h : LieSubalgebra F G)
    (preserves : ∀ a ha x, step.dilation a ha x ∈ h ↔ x ∈ h)
    (psi : AddChar F ℂ) (unitary : ∀ x, psi x * star (psi x) = 1)
    (lambda : J → step.projection.ker →ₗ[F] F) (scales : (I → J) → I → F)
    (nonempty : ∀ labels, ∃ i, scales labels i ≠ 0)
    (moments : ∀ labels, (∑ i, scales labels i ^ step.degree • lambda (labels i)) = 0)
    (labels : I → J) (q r : Q) :
    recordOutput step psi lambda scales labels (fun _ => sourceEntry (subgroup step.lawG h)) q r =
      recordMass step h psi lambda labels * sourceEntry
        ((subgroup step.lawG h).map (projectionGroup step)) q r := by
  have hr := central_cq_record (subgroup step.lawG h) (kernelEmbed step)
    (kernelEmbed_central step) (fun l => linearCharacter psi (lambda l))
    (fun l z => unitary (lambda l z.toAdd))
    (fun labels => stepAction step (scales labels))
    (fun (_ _ : Q × Unit) => (Fintype.card Q : ℂ)⁻¹)
    (quotientRelation (subgroup step.lawG h) (kernelEmbed step) step.sigma)
    (fun labels _ => stepCertificate step h preserves psi (fun i => lambda (labels i))
      (scales labels) (nonempty labels) (moments labels)) labels q r () ()
  change _ = recordMass step h psi lambda labels *
    ((Fintype.card Q : ℂ)⁻¹ * if _ then 1 else 0) at hr
  rw [step_relation] at hr
  exact hr

theorem record_scaled_sources (step : StepGeometry F G Q) (psi : AddChar F ℂ)
    (lambda : J → step.projection.ker →ₗ[F] F) (scales : (I → J) → I → F)
    (labels : I → J) (states : I → G → G → ℂ) (weights : I → ℂ) (q r : Q) :
    recordOutput step psi lambda scales labels (fun i x y => weights i * states i x y) q r =
      (∏ i, weights i) * recordOutput step psi lambda scales labels states q r := by
  unfold recordOutput
  simp_rw [measuredState_scale, Finset.prod_mul_distrib]
  exact scaled_source _ _ _ _ _ _ _ _

variable [Fintype J]

omit [Fintype Q] in
theorem record_mass_complete (step : StepGeometry F G Q) (h : LieSubalgebra F G)
    (psi : AddChar F ℂ) (unitary : ∀ x, psi x * star (psi x) = 1)
    (lambda : J → step.projection.ker →ₗ[F] F)
    (complete : ∀ z, (∑ l, linearCharacter psi (lambda l) z) =
      if z = 1 then (Fintype.card (Multiplicative step.projection.ker) : ℂ) else 0) :
    (∑ labels : I → J, recordMass step h psi lambda labels) = 1 := by
  exact packet_mass_complete _ _ (kernelEmbed_central step)
    (fun l => linearCharacter psi (lambda l)) (fun l z => unitary (lambda l z.toAdd))
    (by intro z; split_ifs with hz <;> simpa [hz] using complete z)

def prepareNext (step : StepGeometry F G Q) (psi : AddChar F ℂ)
    (lambda : J → step.projection.ker →ₗ[F] F) (scales : (I → J) → I → F)
    (states : I → G → G → ℂ) (q r : Q) : ℂ :=
  ∑ labels : I → J, recordOutput step psi lambda scales labels states q r

theorem prepareNext_source (step : StepGeometry F G Q) (h : LieSubalgebra F G)
    (preserves : ∀ a ha x, step.dilation a ha x ∈ h ↔ x ∈ h)
    (psi : AddChar F ℂ) (unitary : ∀ x, psi x * star (psi x) = 1)
    (lambda : J → step.projection.ker →ₗ[F] F)
    (complete : ∀ z, (∑ l, linearCharacter psi (lambda l) z) =
      if z = 1 then (Fintype.card (Multiplicative step.projection.ker) : ℂ) else 0)
    (scales : (I → J) → I → F) (nonempty : ∀ labels, ∃ i, scales labels i ≠ 0)
    (moments : ∀ labels, (∑ i, scales labels i ^ step.degree • lambda (labels i)) = 0) :
    prepareNext step psi lambda scales (fun _ => sourceEntry (subgroup step.lawG h)) =
      sourceEntry ((subgroup step.lawG h).map (projectionGroup step)) := by
  funext q r
  simp_rw [prepareNext, record_source step h preserves psi unitary lambda scales nonempty moments]
  rw [← Finset.sum_mul, record_mass_complete step h psi unitary lambda complete, one_mul]

end Record

section ActualRees
open ReesLie ReesDilation LieModule
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] [Group L] {n : ℕ}

def reesStep (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    letI := stageGroup law points nilpotent (d+1)
    letI := stageGroup law points nilpotent d
    StepGeometry F (cover points nilpotent ⧸ tailIdeal points nilpotent (d+1))
      (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := stageGroup law points nilpotent (d+1)
  letI := stageGroup law points nilpotent d
  refine {
    lawG := stageLaw law points nilpotent (d+1)
    lawQ := stageLaw law points nilpotent d
    same_expression := rfl
    projection := stageFactor points nilpotent d (d+1) (Nat.le_succ d)
    degree := d+1
    positive := Nat.zero_lt_succ d
    kernel_central := ?_
    dilation := stageDilation points distinct nonzero nilpotent (d+1)
    kernel_scaled := ?_
    sigma := stageSection points distinct nonzero nilpotent d (d+1)
    section_right := stageSection_right_inverse points distinct nonzero nilpotent d (d+1)
      (Nat.le_succ d) }
  · intro x hx y
    obtain ⟨z, hz, rfl⟩ := (stageFactor_zero_iff points nilpotent d (d+1) (Nat.le_succ d) x).mp hx
    rw [← lie_skew, next_layer_central points nilpotent d z hz y, neg_zero]
  · intro a ha x hx
    obtain ⟨z, hz, rfl⟩ := (stageFactor_zero_iff points nilpotent d (d+1) (Nat.le_succ d) x).mp hx
    exact next_layer_scalar points distinct nonzero nilpotent d a ha z hz

theorem rees_hidden_image (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) (h : LieSubalgebra F L) :
    letI := stageGroup law points nilpotent (d+1)
    letI := stageGroup law points nilpotent d
    let step := reesStep law points distinct nonzero nilpotent d
    (subgroup step.lawG (stageHidden points nilpotent (d+1) h)).map (projectionGroup step) =
      subgroup step.lawQ (stageHidden points nilpotent d h) := by
  exact stageGroupFactor_hidden law points nilpotent d (d+1) (Nat.le_succ d) h

variable {I J : Type*} [Fintype I] [Fintype J] [Fintype L]

@[instance_reducible] def stageFintype (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    Fintype (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  have : Finite (cover points nilpotent) := inferInstance
  have := Finite.of_surjective (quotientProjection points nilpotent d)
    (quotientProjection_surjective points nilpotent d)
  exact Fintype.ofFinite _

theorem rees_prepareNext_source (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) (h : LieSubalgebra F L) :
    letI := stageGroup law points nilpotent (d+1)
    letI := stageGroup law points nilpotent d
    letI := stageFintype points nilpotent (d+1)
    letI := stageFintype points nilpotent d
    let step := reesStep law points distinct nonzero nilpotent d
    ∀ (psi : AddChar F ℂ) (_unitary : ∀ x, psi x * star (psi x) = 1)
      (lambda : J → step.projection.ker →ₗ[F] F)
      (_complete : ∀ z, (∑ l, linearCharacter psi (lambda l) z) =
        if z = 1 then (Fintype.card (Multiplicative step.projection.ker) : ℂ) else 0)
      (scales : (I → J) → I → F) (_nonempty : ∀ labels, ∃ i, scales labels i ≠ 0)
      (_moments : ∀ labels, (∑ i, scales labels i ^ step.degree • lambda (labels i)) = 0),
      prepareNext step psi lambda scales
        (fun _ => sourceEntry (subgroup step.lawG (stageHidden points nilpotent (d+1) h))) =
      sourceEntry (subgroup step.lawQ (stageHidden points nilpotent d h)) := by
  let := stageGroup law points nilpotent (d+1)
  let := stageGroup law points nilpotent d
  let := stageFintype points nilpotent (d+1)
  let := stageFintype points nilpotent d
  dsimp only
  intro psi unitary lambda complete scales nonempty moments
  rw [← rees_hidden_image law points distinct nonzero nilpotent d h]
  exact prepareNext_source _ _ (fun a ha x =>
    stageDilation_hidden points distinct nonzero nilpotent (d+1) a ha h x)
    psi unitary lambda complete scales nonempty moments

end ActualRees

end
end QSearch.ReesStageInstrument
