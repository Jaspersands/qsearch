import Formal.CentralCharacterDescent

/-!
# Full-register central spectral measurement

Prepare a uniform central ancilla, control right multiplication by the
inverse of its embedded value, Fourier transform with the negative character
convention, and measure only that ancilla. The resulting Kraus operators
are spectral projectors on the original G register. All additive characters
are included; no quotient chart, hidden data, or linear-label enumeration
is an operational input. Centrality is needed only for the source bridge.
-/

namespace QSearch.CentralSpectralProjector

open scoped BigOperators
open QSearch.AffineSupportErasure (invSize uniformAmplitude)
open QSearch.CentralCharacterDescent (projectedEntry)

noncomputable section
attribute [local instance] Classical.propDecidable
set_option backward.isDefEq.respectTransparency false

variable {G C : Type*} [Group G] [AddCommGroup C] [Fintype G] [Fintype C]

/-- Positive character in the matrix entry; equivalently
`|C|^-1 sum_z conj(chi z) R_(embed z)` for `R_g |x> = |x*g^-1>`. -/
def projector (embed : Multiplicative C →* G) (chi : AddChar C ℂ) : Matrix G G ℂ :=
  fun x y => invSize C * ∑ z : C,
    if x = y * embed (Multiplicative.ofAdd z) then chi z else 0

/-- The controlled operation is a permutation on the full ancilla/target. -/
def controlledRight (embed : Multiplicative C →* G) : C × G ≃ C × G where
  toFun v := (v.1, v.2 * (embed (Multiplicative.ofAdd v.1))⁻¹)
  invFun v := (v.1, v.2 * embed (Multiplicative.ofAdd v.1))
  left_inv v := by simp
  right_inv v := by simp

/-- Uniform preparation, controlled right action, negative ancilla Fourier,
and the observed character. The target G register is not compressed. -/
def ancillaKraus (embed : Multiplicative C →* G) (chi : AddChar C ℂ) : Matrix G G ℂ :=
  fun x y => ∑ z : C, (uniformAmplitude C * star (chi z)) *
    (if x = (controlledRight embed (z, y)).2 then uniformAmplitude C else 0)

omit [Fintype G] in
theorem ancillaKraus_eq_projector (embed : Multiplicative C →* G)
    (chi : AddChar C ℂ) : ancillaKraus embed chi = projector embed chi := by
  have hu : uniformAmplitude C * uniformAmplitude C = invSize C := by
    simpa [uniformAmplitude, Complex.star_def] using
      (AffineSupportErasure.uniformAmplitude_normalized (V := C))
  ext x y
  unfold ancillaKraus projector
  rw [Finset.mul_sum]
  apply Fintype.sum_equiv (Equiv.neg C)
  intro z
  simp only [Equiv.neg_apply, controlledRight, Equiv.coe_fn_mk,
    ofAdd_neg, map_inv, chi.map_neg_eq_conj]
  split_ifs
  · calc
      _ = (uniformAmplitude C * uniformAmplitude C) * star (chi z) := by ring
      _ = _ := by rw [hu]; rfl
  · simp

/-- Left multiplication by the spectral operator, on an arbitrary matrix. -/
theorem projector_mul_apply (embed : Multiplicative C →* G) (chi : AddChar C ℂ)
    (rho : Matrix G G ℂ) (x y : G) :
    (projector embed chi * rho) x y = invSize C * ∑ z : C,
      chi z * rho (x * (embed (Multiplicative.ofAdd z))⁻¹) y := by
  simp only [Matrix.mul_apply, projector, mul_assoc, Finset.sum_mul, ← Finset.mul_sum]
  rw [Finset.sum_comm]
  congr 1
  apply Finset.sum_congr rfl
  intro z _
  have he (t : G) : x = t * embed (Multiplicative.ofAdd z) ↔
      t = x * (embed (Multiplicative.ofAdd z))⁻¹ := by
    constructor <;> intro h
    · rw [h]; simp
    · rw [h]; simp
  simp [he, ite_mul]

theorem mul_projector_apply (embed : Multiplicative C →* G) (chi : AddChar C ℂ)
    (rho : Matrix G G ℂ) (x y : G) :
    (rho * projector embed chi) x y = invSize C * ∑ z : C,
      chi z * rho x (y * embed (Multiplicative.ofAdd z)) := by
  simp only [Matrix.mul_apply, projector, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro z _
  simp [mul_ite, mul_comm, mul_assoc]

omit [Fintype G] in
theorem projector_self_adjoint (embed : Multiplicative C →* G) (chi : AddChar C ℂ) :
    (projector embed chi).conjTranspose = projector embed chi := by
  ext x y
  simp only [Matrix.conjTranspose_apply, projector, star_mul', star_sum,
    apply_ite, star_zero]
  rw [show star (invSize C) = invSize C by simp [invSize]]
  congr 1
  apply Fintype.sum_equiv (Equiv.neg C)
  intro z
  have he : y = x * embed (Multiplicative.ofAdd z) ↔
      x = y * (embed (Multiplicative.ofAdd z))⁻¹ := by
    constructor <;> intro h
    · rw [h]; simp
    · rw [h]; simp
  simp only [Equiv.neg_apply, ofAdd_neg, map_inv,
    chi.map_neg_eq_conj, he]
  rfl

omit [Fintype G] in
theorem projector_translate (embed : Multiplicative C →* G) (chi : AddChar C ℂ)
    (z : C) (x y : G) :
    projector embed chi (x * embed (Multiplicative.ofAdd z)) y =
      chi z * projector embed chi x y := by
  unfold projector
  rw [← Equiv.sum_comp (Equiv.addRight z)
    (fun w : C => if x * embed (Multiplicative.ofAdd z) =
      y * embed (Multiplicative.ofAdd w) then chi w else 0)]
  simp only [Equiv.coe_addRight, ofAdd_add, map_mul,
    ← mul_assoc, mul_left_inj, chi.map_add_eq_mul]
  have point (w : C) :
      (if x = y * embed (Multiplicative.ofAdd w) then chi w * chi z else 0) =
        (if x = y * embed (Multiplicative.ofAdd w) then chi w else 0) * chi z := by
    split_ifs <;> simp
  simp_rw [point]
  rw [← Finset.sum_mul]
  ring

theorem projector_mul (embed : Multiplicative C →* G) (chi psi : AddChar C ℂ) :
    projector embed chi * projector embed psi =
      if chi = psi then projector embed chi else 0 := by
  ext x y
  rw [projector_mul_apply]
  have ht (z : C) : projector embed psi (x * (embed (Multiplicative.ofAdd z))⁻¹) y =
      psi (-z) * projector embed psi x y := by
    simpa only [ofAdd_neg, map_inv] using projector_translate embed psi (-z) x y
  simp_rw [ht, ← mul_assoc, ← AddChar.sub_apply]
  rw [← Finset.sum_mul, AddChar.sum_eq_ite]
  have hc : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  by_cases h : chi = psi <;> simp [h, sub_eq_zero, invSize, hc]

theorem projector_idempotent (embed : Multiplicative C →* G) (chi : AddChar C ℂ) :
    projector embed chi * projector embed chi = projector embed chi := by
  simp [projector_mul]

theorem projector_orthogonal (embed : Multiplicative C →* G) (chi psi : AddChar C ℂ)
    (different : chi ≠ psi) : projector embed chi * projector embed psi = 0 := by
  simp [projector_mul, different]

omit [Fintype G] in
/-- Reuse the existing full-dual orthogonality; every additive character occurs. -/
theorem projector_sum (embed : Multiplicative C →* G) :
    (∑ chi : AddChar C ℂ, projector embed chi) = 1 := by
  have hs (z : C) : (∑ chi : AddChar C ℂ, chi z) =
      if z = 0 then (Fintype.card C : ℂ) else 0 := by
    simpa [eq_comm] using CentralRegularSource.dual_orthogonality (0 : C) z
  ext x y
  simp only [Matrix.sum_apply, projector, ← Finset.mul_sum]
  rw [Finset.sum_comm]
  simp_rw [Finset.sum_ite_irrel, hs]
  have hc : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  rw [Finset.sum_eq_single (0 : C)]
  · simp [invSize, hc, Matrix.one_apply]
  · intro z _ hz
    simp [hz]
  · simp

theorem projector_kraus_sum (embed : Multiplicative C →* G) :
    (∑ chi : AddChar C ℂ, (projector embed chi).conjTranspose * projector embed chi) = 1 := by
  simp_rw [projector_self_adjoint, projector_idempotent]
  exact projector_sum embed

theorem projector_kraus_complete (embed : Multiplicative C →* G) (x y : G) :
    (∑ chi : AddChar C ℂ, ∑ t : G,
      star (projector embed chi t x) * projector embed chi t y) =
      if x = y then 1 else 0 := by
  have h := congrArg (fun M : Matrix G G ℂ => M x y) (projector_kraus_sum embed)
  simpa [Matrix.sum_apply, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Matrix.one_apply] using h

theorem ancilla_kraus_complete (embed : Multiplicative C →* G) (x y : G) :
    (∑ chi : AddChar C ℂ, ∑ t : G,
      star (ancillaKraus embed chi t x) * ancillaKraus embed chi t y) =
      if x = y then 1 else 0 := by
  simp_rw [ancillaKraus_eq_projector]
  exact projector_kraus_complete embed x y

theorem projector_mul_source (H : Subgroup G) (embed : Multiplicative C →* G)
    (chi : AddChar C ℂ) (x y : G) :
    (projector embed chi * Matrix.of (CosetSourceFourier.groupEntry H)) x y =
      projectedEntry H embed chi.toMonoidHom x y := by
  rw [projector_mul_apply]
  unfold projectedEntry
  have hc : invSize (Multiplicative C) = invSize C := by
    simp [invSize, Fintype.card_congr (Multiplicative.toAdd : Multiplicative C ≃ C)]
  rw [hc]
  congr 1
  exact Equiv.sum_comp (Multiplicative.ofAdd : C ≃ Multiplicative C)
    (fun z => chi.toMonoidHom z *
      CosetSourceFourier.groupEntry H (x * (embed z)⁻¹) y)

theorem projector_commutes_source (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : AddChar C ℂ) :
    projector embed chi * Matrix.of (CosetSourceFourier.groupEntry H) =
      Matrix.of (CosetSourceFourier.groupEntry H) * projector embed chi := by
  ext x y
  rw [projector_mul_apply, mul_projector_apply]
  congr 1
  apply Finset.sum_congr rfl
  intro z _
  have he : (x * (embed (Multiplicative.ofAdd z))⁻¹)⁻¹ * y =
      x⁻¹ * (y * embed (Multiplicative.ofAdd z)) := by
    calc
      _ = embed (Multiplicative.ofAdd z) * (x⁻¹ * y) := by group
      _ = (x⁻¹ * y) * embed (Multiplicative.ofAdd z) := central _ _
      _ = _ := mul_assoc _ _ _
  change chi z * CosetSourceFourier.groupEntry H
    (x * (embed (Multiplicative.ofAdd z))⁻¹) y =
      chi z * CosetSourceFourier.groupEntry H x (y * embed (Multiplicative.ofAdd z))
  simp only [CosetSourceFourier.groupEntry, he]

/-- Actual two-sided measurement branch, including zero-probability labels.
H may be nonnormal and have any intersection with the embedded center. -/
theorem two_sided_source (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : AddChar C ℂ) (x y : G) :
    (projector embed chi * Matrix.of (CosetSourceFourier.groupEntry H) *
      (projector embed chi).conjTranspose) x y =
      projectedEntry H embed chi.toMonoidHom x y := by
  rw [projector_self_adjoint, Matrix.mul_assoc,
    ← projector_commutes_source H embed central chi, ← Matrix.mul_assoc,
    projector_idempotent, projector_mul_source]

theorem ancilla_source (H : Subgroup G) (embed : Multiplicative C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : AddChar C ℂ) (x y : G) :
    (ancillaKraus embed chi * Matrix.of (CosetSourceFourier.groupEntry H) *
      (ancillaKraus embed chi).conjTranspose) x y =
      projectedEntry H embed chi.toMonoidHom x y := by
  rw [ancillaKraus_eq_projector]
  exact two_sided_source H embed central chi x y

end
end QSearch.CentralSpectralProjector

/-- info: 'QSearch.CentralSpectralProjector.ancillaKraus_eq_projector' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.ancillaKraus_eq_projector

/-- info: 'QSearch.CentralSpectralProjector.projector_self_adjoint' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.projector_self_adjoint

/-- info: 'QSearch.CentralSpectralProjector.projector_idempotent' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.projector_idempotent

/-- info: 'QSearch.CentralSpectralProjector.projector_orthogonal' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.projector_orthogonal

/-- info: 'QSearch.CentralSpectralProjector.projector_sum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.projector_sum

/-- info: 'QSearch.CentralSpectralProjector.projector_kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.projector_kraus_complete

/-- info: 'QSearch.CentralSpectralProjector.ancilla_kraus_complete' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.ancilla_kraus_complete

/-- info: 'QSearch.CentralSpectralProjector.two_sided_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.two_sided_source

/-- info: 'QSearch.CentralSpectralProjector.ancilla_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CentralSpectralProjector.ancilla_source
