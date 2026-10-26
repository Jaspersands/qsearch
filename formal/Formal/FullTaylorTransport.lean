import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.RingTheory.MvPolynomial.Basic
import Formal.NonlinearJetChannel
import Mathlib.Tactic

/-!
# Public transport of the full Taylor jet

The auxiliary variables are Y_i (`some i`) and s (`none`). The full jet
is the coefficient vector of Q(Y+s*q)-Q(Y). Hidden Q occurs only in the
proof witness; the public substitution depends on z and t alone.
-/

namespace QSearch.FullTaylorTransport

open MvPolynomial
open scoped BigOperators
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F ι : Type*} [Field F]

abbrev Aux (ι F : Type*) [CommSemiring F] := MvPolynomial (Option ι) F

def substitution (z : ι → F) (t : F) : Option ι → Aux ι F
  | none => X none * C t
  | some i => X (some i) + X none * C (z i)

def transport (z : ι → F) (t : F) : Aux ι F →ₐ[F] Aux ι F :=
  bind₁ (substitution z t)

def shifted (q : ι → F) : MvPolynomial ι F →ₐ[F] Aux ι F :=
  bind₁ (fun i => X (some i) + X none * C (q i))

def base : MvPolynomial ι F →ₐ[F] Aux ι F := rename some

def jet (Q : MvPolynomial ι F) (q : ι → F) : Aux ι F :=
  shifted q Q - base Q

theorem transport_comp (z w : ι → F) (t u : F) (P : Aux ι F) :
    transport z t (transport w u P) = transport (z + t • w) (t*u) P := by
  simp only [transport, bind₁_bind₁]
  congr 2
  funext i
  cases i <;> simp [substitution, Pi.add_apply, Pi.smul_apply, smul_eq_mul] <;> ring

theorem transport_identity (P : Aux ι F) : transport 0 1 P = P := by
  have h : substitution (0 : ι → F) 1 = X := by
    funext i
    cases i <;> simp [substitution]
  simp [transport, h]

theorem transport_inverse (z : ι → F) (t : F) (ht : t ≠ 0) (P : Aux ι F) :
    transport (-t⁻¹ • z) t⁻¹ (transport z t P) = P := by
  rw [transport_comp]
  have hz : -t⁻¹ • z + t⁻¹ • z = 0 := by module
  rw [hz, inv_mul_cancel₀ ht, transport_identity]

theorem transport_injective (z : ι → F) (t : F) (ht : t ≠ 0) :
    Function.Injective (transport z t) :=
  Function.LeftInverse.injective (transport_inverse z t ht)

theorem transport_shifted (z q : ι → F) (t : F) (Q : MvPolynomial ι F) :
    transport z t (shifted q Q) = shifted (z + t • q) Q := by
  simp only [transport, shifted, bind₁_bind₁]
  congr 2
  funext i
  simp [substitution, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem transport_base (z : ι → F) (t : F) (Q : MvPolynomial ι F) :
    transport z t (base Q) = shifted z Q := by
  simp [transport, base, shifted, bind₁_rename, substitution, Function.comp_def]

theorem jet_transport (Q : MvPolynomial ι F) (z q : ι → F) (t : F) :
    jet Q (z + t • q) = jet Q z + transport z t (jet Q q) := by
  simp only [jet, map_sub, transport_shifted, transport_base]
  abel

/-- Substitution by linear forms cannot increase total degree. -/
theorem bind_degree_le {κ : Type*} (f : ι → MvPolynomial κ F)
    (hf : ∀ i, (f i).totalDegree ≤ 1) (Q : MvPolynomial ι F) :
    (bind₁ f Q).totalDegree ≤ Q.totalDegree := by
  classical
  conv_lhs => rw [Q.as_sum]
  simp only [map_sum, bind₁_monomial]
  apply totalDegree_finsetSum_le
  intro d hd
  calc
    _ ≤ (C (Q.coeff d)).totalDegree +
        (∏ i ∈ d.support, f i ^ d i).totalDegree := totalDegree_mul _ _
    _ ≤ 0 + ∑ i ∈ d.support, d i := by
      simp only [totalDegree_C, zero_add]
      exact (totalDegree_finsetProd _ _).trans (Finset.sum_le_sum fun i _ =>
        (totalDegree_pow _ _).trans (by simpa using Nat.mul_le_mul_left (d i) (hf i)))
    _ ≤ Q.totalDegree := by simpa [Finsupp.sum] using le_totalDegree hd

theorem substitution_degree (z : ι → F) (t : F) (i : Option ι) :
    (substitution z t i).totalDegree ≤ 1 := by
  cases i with
  | none =>
    simpa [substitution] using totalDegree_mul (X (none : Option ι) : Aux ι F) (C t)
  | some i =>
    apply (totalDegree_add _ _).trans
    simp only [totalDegree_X, max_le_iff, le_refl, true_and]
    simpa using totalDegree_mul (X (none : Option ι) : Aux ι F) (C (z i))

def zeroScale : Aux ι F →ₐ[F] Aux ι F := transport 0 0

/-- Degree at most D, with no s^0 coefficients. This is the actual full
jet space, not the entire infinite polynomial algebra. -/
def jetSpace (D : ℕ) : Submodule F (Aux ι F) :=
  restrictTotalDegree (Option ι) F D ⊓ LinearMap.ker zeroScale.toLinearMap

theorem mem_jetSpace (D : ℕ) (P : Aux ι F) :
    P ∈ jetSpace D ↔ P.totalDegree ≤ D ∧ zeroScale P = 0 := by
  simp [jetSpace, mem_restrictTotalDegree, LinearMap.mem_ker]

theorem zeroScale_transport (z : ι → F) (t : F) (P : Aux ι F) :
    zeroScale (transport z t P) = zeroScale P := by
  simp [zeroScale, transport_comp]

theorem transport_mem (D : ℕ) (z : ι → F) (t : F) {P : Aux ι F}
    (hP : P ∈ jetSpace D) : transport z t P ∈ jetSpace D := by
  rw [mem_jetSpace] at hP ⊢
  exact ⟨(bind_degree_le _ (substitution_degree z t) P).trans hP.1,
    (zeroScale_transport z t P).trans hP.2⟩

theorem jet_mem (D : ℕ) (Q : MvPolynomial ι F) (hQ : Q.totalDegree ≤ D)
    (q : ι → F) : jet Q q ∈ jetSpace D := by
  rw [mem_jetSpace]
  constructor
  · apply (totalDegree_sub _ _).trans
    apply max_le
    · exact (bind_degree_le _ (fun i => substitution_degree q 1 (some i)) Q).trans hQ
    · exact (totalDegree_rename_le some Q).trans hQ
  · simp only [zeroScale, jet, map_sub, transport_shifted, transport_base,
      zero_smul, add_zero]
    simp [shifted]

theorem zeroScale_monomial (d : Option ι →₀ ℕ) (a : F) :
    zeroScale (monomial d a) = if d none = 0 then monomial d a else 0 := by
  classical
  simp only [zeroScale, transport, bind₁_monomial]
  by_cases hd : d none = 0
  · rw [ite_eq_left hd, monomial_eq]
    congr 1
    apply Finset.prod_congr rfl
    intro i hi
    cases i with
    | none => simp_all
    | some i => simp [substitution]
  · rw [ite_eq_right hd]
    have hp : (∏ i ∈ d.support, substitution (0 : ι → F) 0 i ^ d i) = 0 := by
      apply Finset.prod_eq_zero (Finsupp.mem_support_iff.mpr hd)
      simp [substitution, hd]
    rw [hp, mul_zero]

theorem coeff_zeroScale (P : Aux ι F) (d : Option ι →₀ ℕ) :
    (zeroScale P).coeff d = if d none = 0 then P.coeff d else 0 := by
  classical
  induction P using MvPolynomial.induction_on' with
  | add P R hP hR =>
    simp_all only [map_add]
    split_ifs <;> simp_all
  | monomial e a =>
    rw [zeroScale_monomial]
    by_cases hed : e = d
    · subst e
      by_cases hd : d none = 0 <;> simp [hd, coeff_monomial]
    · by_cases hd : d none = 0 <;> by_cases he : e none = 0 <;>
        simp [hd, he, hed, coeff_monomial]

/-- Exactly the (alpha,k) coordinates with k>0 and |alpha|+k<=D.
No extra s^0 coordinates or degrees beyond D are introduced. -/
theorem jetSpace_eq_support (D : ℕ) :
    (jetSpace D : Submodule F (Aux ι F)) =
      restrictSupport F {d | d.sum (fun _ e => e) ≤ D ∧ d none ≠ 0} := by
  ext P
  rw [mem_jetSpace, mem_restrictSupport_iff]
  constructor
  · rintro ⟨hD, h0⟩ d hd
    refine ⟨(le_totalDegree hd).trans hD, ?_⟩
    intro he
    have hz := congrArg (fun P : Aux ι F => P.coeff d) h0
    rw [coeff_zeroScale, ite_eq_left he] at hz
    exact (mem_support_iff.mp hd) hz
  · intro h
    constructor
    · exact Finset.sup_le (fun d hd => (h hd).1)
    · ext d
      rw [coeff_zeroScale]
      split_ifs with hd
      · by_contra hc
        exact (h (mem_support_iff.mpr hc)).2 hd
      · rfl

instance jetSpace_finite [Finite ι] (D : ℕ) :
    FiniteDimensional F (jetSpace (ι := ι) (F := F) D) :=
  Submodule.finiteDimensional_of_le (show jetSpace D ≤
    restrictTotalDegree (Option ι) F D from inf_le_left)

def finiteTransport (D : ℕ) (z : ι → F) (t : F) :
    jetSpace (ι := ι) (F := F) D →ₗ[F] jetSpace (ι := ι) (F := F) D :=
  (transport z t).toLinearMap.restrict (fun _ h => transport_mem D z t h)

def finiteJet (D : ℕ) (Q : MvPolynomial ι F) (hQ : Q.totalDegree ≤ D)
    (q : ι → F) : jetSpace (ι := ι) (F := F) D := ⟨jet Q q, jet_mem D Q hQ q⟩

theorem finiteTransport_injective (D : ℕ) (z : ι → F) (t : F) (ht : t ≠ 0) :
    Function.Injective (finiteTransport D z t) := by
  intro x y h
  exact Subtype.ext (transport_injective z t ht (congrArg Subtype.val h))

/-- The inverse is an explicit public substitution, not dimension counting. -/
def transportEquiv (D : ℕ) (z : ι → F) (t : F) (ht : t ≠ 0) :
    jetSpace (ι := ι) (F := F) D ≃ₗ[F] jetSpace (ι := ι) (F := F) D where
  __ := finiteTransport D z t
  invFun := finiteTransport D (-t⁻¹ • z) t⁻¹
  left_inv x := Subtype.ext (transport_inverse z t ht x.val)
  right_inv x := by
    apply Subtype.ext
    change transport z t (transport (-t⁻¹ • z) t⁻¹ x.val) = x.val
    rw [transport_comp]
    have hz : z + t • (-t⁻¹ • z) = 0 := by simp [smul_smul, ht]
    rw [hz, mul_inv_cancel₀ ht, transport_identity]

theorem finiteJet_transport (D : ℕ) (Q : MvPolynomial ι F)
    (hQ : Q.totalDegree ≤ D) (z q : ι → F) (t : F) :
    finiteJet D Q hQ (z + t • q) =
      finiteJet D Q hQ z + finiteTransport D z t (finiteJet D Q hQ q) :=
  Subtype.ext (jet_transport Q z q t)

/-- Discharges both transport premises of the existing support theorem. -/
theorem fullJet_public_support (D : ℕ) (Q : MvPolynomial ι F)
    (hQ : Q.totalDegree ≤ D) (U : Submodule F (ι → F)) (t : F) (ht : t ≠ 0)
    (o x x' : (ι → F) × jetSpace (ι := ι) (F := F) D) :
    NonlinearJetChannel.curveRel U (finiteJet D Q hQ)
      (NonlinearJetChannel.publicPoint t (fun z => finiteTransport D z t) o x)
      (NonlinearJetChannel.publicPoint t (fun z => finiteTransport D z t) o x') ↔
    NonlinearJetChannel.curveRel U (finiteJet D Q hQ) x x' :=
  NonlinearJetChannel.public_support_iff U _ _ _ ht
    (fun z => finiteTransport_injective D z t ht) (fun z q => finiteJet_transport D Q hQ z q t)
    o x x'

variable {κ : Type*}

abbrev Jets (ι κ F : Type*) [Field F] (D : ℕ) :=
  κ → jetSpace (ι := ι) (F := F) D

def vectorTransport (D : ℕ) (z : ι → F) (t : F) : Jets ι κ F D →ₗ[F] Jets ι κ F D where
  toFun P a := finiteTransport D z t (P a)
  map_add' P R := by ext a : 1; exact map_add (finiteTransport D z t) (P a) (R a)
  map_smul' c P := by ext a : 1; exact map_smul (finiteTransport D z t) c (P a)

def vectorJet (D : ℕ) (Q : κ → MvPolynomial ι F) (hQ : ∀ a, (Q a).totalDegree ≤ D)
    (q : ι → F) : Jets ι κ F D := fun a => finiteJet D (Q a) (hQ a) q

theorem vectorTransport_injective (D : ℕ) (z : ι → F) (t : F) (ht : t ≠ 0) :
    Function.Injective (vectorTransport (κ := κ) D z t) := by
  intro P R h
  funext a
  exact finiteTransport_injective D z t ht (congrFun h a)

theorem vectorJet_transport (D : ℕ) (Q : κ → MvPolynomial ι F)
    (hQ : ∀ a, (Q a).totalDegree ≤ D) (z q : ι → F) (t : F) :
    vectorJet D Q hQ (z + t • q) =
      vectorJet D Q hQ z + vectorTransport D z t (vectorJet D Q hQ q) := by
  funext a
  exact finiteJet_transport D (Q a) (hQ a) z q t

noncomputable instance jetSpace_fintype [Finite ι] [Finite F] (D : ℕ) :
    Fintype (jetSpace (ι := ι) (F := F) D) :=
  @Fintype.ofFinite _ (Module.finite_of_finite F)

/-- The actual mixed quantum-channel identity now consumes bounded-degree
polynomials, not an assumed curve-transport law or hidden coefficients. -/
theorem fullJet_mixed_branch {I : Type*} [Fintype I] [Nonempty I]
    [Fintype ι] [Fintype κ] [Fintype F]
    (D : ℕ) (Q : κ → MvPolynomial ι F) (hQ : ∀ a, (Q a).totalDegree ≤ D)
    (U : Submodule F (ι → F)) (phase : I → (ι → F) × Jets ι κ F D → ℂ)
    (c : I → F) (hc : ∀ i, c i ≠ 0)
    (o : I → (ι → F) × Jets ι κ F D) (x x' : (ι → F) × Jets ι κ F D) :
    NonlinearJetChannel.branch (AffineSupportErasure.uniformAmplitude ((ι → F) × Jets ι κ F D))
      U (vectorJet D Q hQ) phase c (fun i z => vectorTransport D z (c i)) o x x' =
      AffineSupportErasure.invSize ((ι → F) × Jets ι κ F D) ^ Fintype.card I *
        NonlinearJetChannel.curveRho U (vectorJet D Q hQ)
          (NonlinearJetChannel.mergedPhase phase c (fun i z => vectorTransport D z (c i)) o) x x' :=
  NonlinearJetChannel.mixed_branch_identity U _ phase c _ hc
    (fun i z => vectorTransport_injective D z (c i) (hc i))
    (fun i z q => vectorJet_transport D Q hQ z q (c i)) o x x'

/-- info: 'QSearch.FullTaylorTransport.transport_comp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.transport_comp

/-- info: 'QSearch.FullTaylorTransport.jet_transport' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.jet_transport

/-- info: 'QSearch.FullTaylorTransport.jetSpace_eq_support' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.jetSpace_eq_support

/-- info: 'QSearch.FullTaylorTransport.transportEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.transportEquiv

/-- info: 'QSearch.FullTaylorTransport.fullJet_public_support' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.fullJet_public_support

/-- info: 'QSearch.FullTaylorTransport.fullJet_mixed_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullTaylorTransport.fullJet_mixed_branch

end
end QSearch.FullTaylorTransport
