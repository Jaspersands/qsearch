import Formal.FullTaylorTransport
import Mathlib.LinearAlgebra.Basis.VectorSpace

/-!
# Public full-jet source alignment

Scalar feature injectivity lifts through every map a -> (a,ell_i a),
including ell_i=0. A public left-inverse certificate splits the carrier
into the common jet and a spectator kernel. Polynomial coefficients are
proof witnesses only. This does not prove random feature-rank success,
weighted cancellation, circuit cost or the entire HSP algorithm.
-/

namespace QSearch.FullJetAlignment

open MvPolynomial FullTaylorTransport
open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F ι κ I B : Type*} [Field F] [AddCommGroup B] [Module F B]

/-- Evaluate the auxiliary polynomial at the PUBLIC scale and outcome. -/
def feature (D : ℕ) (y : I → ι → F) (s : I → F) :
    jetSpace (ι := ι) (F := F) D →ₗ[F] (I → F) :=
  LinearMap.pi fun i => ((aeval (fun o : Option ι => o.elim (s i) (y i))).toLinearMap).comp
    (jetSpace D).subtype

theorem feature_jet (D : ℕ) (Q : MvPolynomial ι F) (hQ : Q.totalDegree ≤ D)
    (y : I → ι → F) (s : I → F) (q : ι → F) (i : I) :
    feature D y s (finiteJet D Q hQ q) i =
      aeval (y i + s i • q) Q - aeval (y i) Q := by
  change aeval (fun o : Option ι => o.elim (s i) (y i)) (jet Q q) = _
  simp only [jet, map_sub, shifted, base, aeval_bind₁, aeval_rename]
  congr 1
  congr 2
  funext a
  simp [Pi.add_apply, Pi.smul_apply, smul_eq_mul]

section Lift
variable {J : Type*} [AddCommGroup J] [Module F J]

def vectorFeature (E : J →ₗ[F] (I → F)) : (κ → J) →ₗ[F] (I → κ → F) where
  toFun P i a := E (P a) i
  map_add' P R := by ext i a; simp
  map_smul' c P := by ext i a; simp

def lift (E : J →ₗ[F] (I → F)) (ell : I → (κ → F) →ₗ[F] B) :
    (κ → J) →ₗ[F] (I → (κ → F) × B) where
  toFun P i := (vectorFeature E P i, ell i (vectorFeature E P i))
  map_add' P R := by ext i : 1; simp [map_add]
  map_smul' c P := by ext i : 1; simp [map_smul]

/-- Rank comes from the identity block, not randomness or nonzero labels. -/
theorem lift_injective (E : J →ₗ[F] (I → F)) (hE : Function.Injective E)
    (ell : I → (κ → F) →ₗ[F] B) : Function.Injective (lift E ell) := by
  intro P R h
  funext a
  apply hE
  funext i
  exact congrFun (congrArg Prod.fst (congrFun h i)) a

end Lift

def displacement (Q : κ → MvPolynomial ι F) (y : I → ι → F) (s : I → F)
    (ell : I → (κ → F) →ₗ[F] B) (q : ι → F) : I → (κ → F) × B :=
  fun i => let a := fun j => aeval (y i + s i • q) (Q j)
    (a, ell i a)

theorem displacement_decomposition (D : ℕ) (Q : κ → MvPolynomial ι F)
    (hQ : ∀ a, (Q a).totalDegree ≤ D) (y : I → ι → F) (s : I → F)
    (ell : I → (κ → F) →ₗ[F] B) (q : ι → F) :
    displacement Q y s ell q = displacement Q y s ell 0 +
      lift (feature D y s) ell (vectorJet D Q hQ q) := by
  have ha (i : I) :
      (fun a => aeval (y i + s i • q) (Q a)) =
        (fun a => aeval (y i) (Q a)) + vectorFeature (feature D y s) (vectorJet D Q hQ q) i := by
    funext a
    change _ = _ + feature D y s (finiteJet D (Q a) (hQ a) q) i
    rw [feature_jet]
    ring
  ext i : 1
  simp only [displacement, smul_zero, add_zero, Pi.add_apply, lift, LinearMap.coe_mk,
    AddHom.coe_mk, ha, map_add, Prod.mk_add_mk]

section Split
variable {J C : Type*} [AddCommGroup J] [Module F J] [AddCommGroup C] [Module F C]

/-- Explicit linear splitting from a public certificate P*T=I.
The inverse reconstructs T*j+k, so no unknown chart enters either map. -/
def split (T : J →ₗ[F] C) (P : C →ₗ[F] J) (h : ∀ j, P (T j) = j) :
    C ≃ₗ[F] J × LinearMap.ker P where
  toFun x := (P x, ⟨x - T (P x), by simp [LinearMap.mem_ker, h]⟩)
  invFun x := T x.1 + x.2.val
  left_inv x := by dsimp; abel
  right_inv x := by
    apply Prod.ext
    · simp [h]
    · apply Subtype.ext
      simp [h]
  map_add' x y := by
    apply Prod.ext
    · exact map_add P x y
    · apply Subtype.ext
      change (x + y) - T (P (x + y)) = (x - T (P x)) + (y - T (P y))
      simp only [map_add]
      abel
  map_smul' c x := by
    apply Prod.ext
    · exact map_smul P c x
    · apply Subtype.ext
      simp [smul_sub]

theorem split_columns (T : J →ₗ[F] C) (P : C →ₗ[F] J)
    (h : ∀ j, P (T j) = j) (j : J) : split T P h (T j) = (j, 0) := by
  apply Prod.ext
  · exact h j
  · apply Subtype.ext
    simp [split, h]

theorem public_left_inverse (T : J →ₗ[F] C) (hT : Function.Injective T) :
    ∃ P : C →ₗ[F] J, ∀ j, P (T j) = j := by
  obtain ⟨P, hP⟩ := T.exists_leftInverse_of_injective (LinearMap.ker_eq_bot.mpr hT)
  exact ⟨P, fun j => LinearMap.congr_fun hP j⟩

theorem aligned_curve {V : Type*} (T : J →ₗ[F] C) (P : C →ₗ[F] J)
    (h : ∀ j, P (T j) = j) (curve : V → J) (a : C) (q : V) :
    split T P h (a + T (curve q)) = ((split T P h a).1 + curve q, (split T P h a).2) := by
  rw [map_add, split_columns]
  change ((split T P h a).1 + curve q, (split T P h a).2 + 0) = _
  rw [add_zero]

end Split

theorem fullJet_alignment_exists (D : ℕ) (y : I → ι → F) (s : I → F)
    (ell : I → (κ → F) →ₗ[F] B) (hE : Function.Injective (feature D y s)) :
    ∃ P : (I → (κ → F) × B) →ₗ[F] Jets ι κ F D,
      ∀ j, P (lift (feature D y s) ell j) = j :=
  public_left_inverse _ (lift_injective _ hE ell)

theorem fullJet_aligned_displacement (D : ℕ) (Q : κ → MvPolynomial ι F)
    (hQ : ∀ a, (Q a).totalDegree ≤ D) (y : I → ι → F) (s : I → F)
    (ell : I → (κ → F) →ₗ[F] B)
    (P : (I → (κ → F) × B) →ₗ[F] Jets ι κ F D)
    (hP : ∀ j, P (lift (feature D y s) ell j) = j) (q : ι → F) :
    split _ P hP (displacement Q y s ell q) =
      ((split _ P hP (displacement Q y s ell 0)).1 + vectorJet D Q hQ q,
        (split _ P hP (displacement Q y s ell 0)).2) := by
  rw [displacement_decomposition D Q hQ y s ell]
  exact aligned_curve _ P hP (vectorJet D Q hQ) _ q

section Permutation
variable {C C' : Type*} [Fintype C] [Fintype C']

def permutation (e : C ≃ C') (r : C') (t : C) : ℂ :=
  if t = e.symm r then 1 else 0

def conjugation (e : C ≃ C') (W : C → C → ℂ) (r t : C') : ℂ :=
  ∑ a, ∑ b, permutation e r a * W a b * star (permutation e t b)

omit [Fintype C'] in
theorem conjugation_pullback (e : C ≃ C') (W : C → C → ℂ) (r t : C') :
    conjugation e W r t = W (e.symm r) (e.symm t) := by
  simp [conjugation, permutation, ite_mul, mul_ite]

variable [AddCommGroup C] [Module F C] [AddCommGroup C'] [Module F C']

omit [Fintype C'] in
theorem conjugation_gauge {V : Type*} (e : C ≃ₗ[F] C') (A : V → C)
    (gamma : V → C → ℂ) (q : V) (r t : C') :
    conjugation e.toEquiv (WeylSourceScalarization.gaugeEntry A gamma q) r t =
      WeylSourceScalarization.gaugeEntry (fun q => e (A q))
        (fun q t => gamma q (e.symm t)) q r t := by
  rw [conjugation_pullback]
  have h : e.symm r = A q + e.symm t ↔ r = e (A q) + t := by
    constructor
    · intro h
      simpa using congrArg e h
    · intro h
      simpa using congrArg e.symm h
  have he (v : C') : e.toEquiv.symm v = e.symm v := rfl
  simp only [WeylSourceScalarization.gaugeEntry, he, h]

variable {V : Type*} [AddCommGroup V] [Module F V] [Fintype V]

/-- Actual two-sum density conjugation, including its normalization. -/
theorem conjugation_source (e : C ≃ₗ[F] C') (U : Submodule F V)
    (A : V → C) (gamma : V → C → ℂ) (q q' : V) (r t : C') :
    conjugation e.toEquiv
      (fun a b => WeylSourceScalarization.matrixSource U A gamma (q, a) (q', b)) r t =
      WeylSourceScalarization.matrixSource U (fun q => e (A q))
        (fun q t => gamma q (e.symm t)) (q, r) (q', t) := by
  rw [conjugation_pullback]
  have hc : AffineSupportErasure.invSize C = AffineSupportErasure.invSize C' := by
    simp only [AffineSupportErasure.invSize, Fintype.card_congr e.toEquiv]
  have hs : A q + e.symm r = A q' + e.symm t ↔ e (A q) + r = e (A q') + t := by
    constructor
    · intro h
      simpa using congrArg e h
    · intro h
      simpa using congrArg e.symm h
  have he (v : C') : e.toEquiv.symm v = e.symm v := rfl
  simp only [WeylSourceScalarization.matrixSource, WeylSourceScalarization.gauge_kernel_identity,
    he, hs, hc]

end Permutation

section Spectator
variable {V J S C : Type*} [AddCommGroup V] [Module F V]
  [AddCommGroup J] [Module F J] [AddCommGroup S] [Module F S]
  [AddCommGroup C] [Module F C] [Fintype V] [Fintype J] [Fintype S] [Fintype C]

def alignedSpectatorBranch (e : C ≃ₗ[F] J × S) (U : Submodule F V)
    (A : V → C) (gamma : V → C → ℂ) (outcome : S) (x x' : V × J) : ℂ :=
  ∑ u, ∑ v, WeylSourceScalarization.measurementKraus outcome x u *
    conjugation e.toEquiv
      (fun a b => WeylSourceScalarization.matrixSource U A gamma (u.1, a) (v.1, b)) u.2 v.2 *
    star (WeylSourceScalarization.measurementKraus outcome x' v)

theorem aligned_source_to_scalar (e : C ≃ₗ[F] J × S) (U : Submodule F V)
    (A : V → C) (gamma : V → C → ℂ) (curve : V → J) (a : J) (b : S)
    (hA : ∀ q, e (A q) = (a + curve q, b)) (outcome : S) (x x' : V × J) :
    alignedSpectatorBranch e U A gamma outcome x x' =
      AffineSupportErasure.invSize S * NonlinearJetChannel.curveRho U curve
        (WeylSourceScalarization.scalarPhase (fun q t => gamma q (e.symm t)) outcome) x x' := by
  simp only [alignedSpectatorBranch, conjugation_source, hA]
  exact NonlinearJetChannel.nonlinear_source_to_scalar U curve a b
    (fun q t => gamma q (e.symm t)) outcome x x'

end Spectator

theorem fullJet_source_to_scalar [Fintype ι] [Fintype κ] [Fintype I] [Fintype F] [Fintype B]
    (D : ℕ) (Q : κ → MvPolynomial ι F) (hQ : ∀ a, (Q a).totalDegree ≤ D)
    (y : I → ι → F) (s : I → F) (ell : I → (κ → F) →ₗ[F] B)
    (P : (I → (κ → F) × B) →ₗ[F] Jets ι κ F D)
    (hP : ∀ j, P (lift (feature D y s) ell j) = j)
    (U : Submodule F (ι → F)) (gamma : (ι → F) → (I → (κ → F) × B) → ℂ)
    (outcome : LinearMap.ker P) (x x' : (ι → F) × Jets ι κ F D) :
    alignedSpectatorBranch (split _ P hP) U (displacement Q y s ell) gamma outcome x x' =
      AffineSupportErasure.invSize (LinearMap.ker P) *
        NonlinearJetChannel.curveRho U (vectorJet D Q hQ)
          (WeylSourceScalarization.scalarPhase
            (fun q t => gamma q ((split _ P hP).symm t)) outcome) x x' :=
  aligned_source_to_scalar (split _ P hP) U _ gamma (vectorJet D Q hQ)
    (split _ P hP (displacement Q y s ell 0)).1
    (split _ P hP (displacement Q y s ell 0)).2
    (fullJet_aligned_displacement D Q hQ y s ell P hP) outcome x x'

/-- info: 'QSearch.FullJetAlignment.feature_jet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.feature_jet

/-- info: 'QSearch.FullJetAlignment.lift_injective' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.lift_injective

/-- info: 'QSearch.FullJetAlignment.split_columns' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.split_columns

/-- info: 'QSearch.FullJetAlignment.fullJet_alignment_exists' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.fullJet_alignment_exists

/-- info: 'QSearch.FullJetAlignment.fullJet_aligned_displacement' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.fullJet_aligned_displacement

/-- info: 'QSearch.FullJetAlignment.conjugation_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.conjugation_source

/-- info: 'QSearch.FullJetAlignment.fullJet_source_to_scalar' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetAlignment.fullJet_source_to_scalar

end
end QSearch.FullJetAlignment
