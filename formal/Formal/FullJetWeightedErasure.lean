import Formal.FullTaylorTransport
import Formal.WeightedPhaseErasure

/-!
# Full Taylor coefficient transport and weighted erasure

Auxiliary scale powers INCREASE under substitution, so a coordinate of
weight k depends only on input coordinates of weight at most k. The
matrix is derived from the actual polynomial transport, not assumed.
-/

namespace QSearch.FullJetWeightedErasure

open MvPolynomial Finsupp FullTaylorTransport
open scoped BigOperators Pointwise
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F ι : Type*} [Field F]

theorem correction_positive (z : ι → F) (t : F) (P : Aux ι F)
    (a : Option ι →₀ ℕ) (ha : a ∈ (transport z t P - P).support) : 0 < a none := by
  have h0 : zeroScale (transport z t P - P) = 0 := by
    simp only [map_sub, zeroScale_transport, sub_self]
  apply Nat.pos_of_ne_zero
  intro hz
  have hc := congrArg (fun Q : Aux ι F => Q.coeff a) h0
  rw [coeff_zeroScale, ite_eq_left hz] at hc
  exact (MvPolynomial.mem_support_iff.mp ha) hc

theorem transport_scale_monomial (z : ι → F) (t : F) (k : ℕ) (r : F) :
    transport z t (monomial (single none k) r) = monomial (single none k) (r*t^k) := by
  rw [← C_mul_X_pow_eq_monomial, map_mul, map_pow]
  simp only [transport, bind₁_C_right, bind₁_X_right, substitution, mul_pow]
  rw [← map_pow (C : F →+* Aux ι F) t k, ← C_mul_X_pow_eq_monomial, map_mul]
  ring

/-- All changes beyond the original monomial have strictly MORE auxiliary
scale factors. This is the source of LOWER-weight coordinate dependence. -/
theorem monomial_correction (z : ι → F) (t : F) (b a : Option ι →₀ ℕ)
    (ha : a ∈ (transport z t (monomial b (1 : F)) -
      monomial b (t^(b none))).support) : b none < a none := by
  classical
  have he (r : F) :
      monomial (single none (b none)) r * monomial (b.erase none) (1 : F) = monomial b r := by
    rw [monomial_mul_monomial, mul_one, b.single_add_erase none]
  have hsplit : transport z t (monomial b (1 : F)) - monomial b (t^(b none)) =
      monomial (single none (b none)) (t^(b none)) *
        (transport z t (monomial (b.erase none) 1) - monomial (b.erase none) 1) := by
    rw [mul_sub, he, ← he 1, map_mul, transport_scale_monomial, one_mul]
  rw [hsplit] at ha
  obtain ⟨u, hu, v, hv, huv⟩ := Finset.mem_add.mp (support_mul _ _ ha)
  have hu' : u = single none (b none) := Finset.mem_singleton.mp (support_monomial_subset hu)
  subst u
  subst a
  have hpos := correction_positive z t (monomial (b.erase none) 1) v hv
  simpa using hpos

def entry (z : ι → F) (t : F) (a b : Option ι →₀ ℕ) : F :=
  (transport z t (monomial b 1)).coeff a

/-- At equal or higher input weight, only the SAME coordinate contributes. -/
theorem entry_on_or_above (z : ι → F) (t : F) (a b : Option ι →₀ ℕ)
    (hab : a none ≤ b none) :
    entry z t a b = if b = a then t^(b none) else 0 := by
  classical
  have hz : (transport z t (monomial b 1) - monomial b (t^(b none))).coeff a = 0 := by
    by_contra h
    exact (not_lt_of_ge hab) (monomial_correction z t b a (MvPolynomial.mem_support_iff.mpr h))
  have he : entry z t a b = (monomial b (t^(b none))).coeff a := by
    simpa only [entry, AddMonoidAlgebra.coeff_sub, Finsupp.sub_apply, sub_eq_zero] using hz
  rw [he, coeff_monomial]

abbrev Index (ι : Type*) (D : ℕ) :=
  {a : Option ι →₀ ℕ // a.sum (fun _ e => e) ≤ D ∧ a none ≠ 0}

theorem index_bound (D : ℕ) (a : Index ι D) (i : Option ι) : a.val i ≤ D := by
  classical
  by_cases hi : a.val i = 0
  · simp [hi]
  · exact (Finset.single_le_sum (fun _ _ => Nat.zero_le _)
      (Finsupp.mem_support_iff.mpr hi)).trans a.property.1

instance index_finite [Finite ι] (D : ℕ) : Finite (Index ι D) := by
  let enc (a : Index ι D) (i : Option ι) : Fin (D+1) :=
    ⟨a.val i, Nat.lt_succ_of_le (index_bound D a i)⟩
  apply Finite.of_injective enc
  intro a b h
  apply Subtype.ext
  ext i
  exact congrArg Fin.val (congrFun h i)

instance index_fintype [Finite ι] (D : ℕ) : Fintype (Index ι D) := Fintype.ofFinite _

section Coordinates
variable [Fintype ι]

def coordinates (D : ℕ) (P : jetSpace (ι := ι) (F := F) D) : Index ι D → F :=
  fun a => P.val.coeff a.val

def reconstruct (D : ℕ) (x : Index ι D → F) : Aux ι F :=
  ∑ a, monomial a.val (x a)

theorem coeff_reconstruct (D : ℕ) (x : Index ι D → F) (a : Index ι D) :
    (reconstruct D x).coeff a.val = x a := by
  classical
  simp only [reconstruct, AddMonoidAlgebra.coeff_sum, Finsupp.finsetSum_apply, coeff_monomial]
  have he (b : Index ι D) : b.val = a.val ↔ b = a := Subtype.ext_iff.symm
  simp_rw [he]
  simp

theorem reconstruct_mem (D : ℕ) (x : Index ι D → F) : reconstruct D x ∈ jetSpace D := by
  rw [jetSpace_eq_support]
  exact (restrictSupport F _).sum_mem
    (fun a _ => (monomial_mem_restrictSupport (m := a.val) (r := x a)).mpr
      (Or.inl a.property))

theorem reconstruct_coordinates (D : ℕ) (P : jetSpace (ι := ι) (F := F) D) :
    reconstruct D (coordinates D P) = P.val := by
  classical
  ext a
  by_cases ha : a.sum (fun _ e => e) ≤ D ∧ a none ≠ 0
  · exact coeff_reconstruct D (coordinates D P) ⟨a, ha⟩
  · have hs : P.val ∈ restrictSupport F {a | a.sum (fun _ e => e) ≤ D ∧ a none ≠ 0} := by
      rw [← jetSpace_eq_support]
      exact P.property
    have hr := reconstruct_mem D (coordinates D P)
    rw [jetSpace_eq_support] at hr
    have hzero {Q : Aux ι F} (hQ : Q ∈ restrictSupport F
        {a | a.sum (fun _ e => e) ≤ D ∧ a none ≠ 0}) : Q.coeff a = 0 := by
      by_contra h
      exact ha (hQ (MvPolynomial.mem_support_iff.mpr h))
    rw [hzero hs, hzero hr]

theorem coordinates_transport (D : ℕ) (z : ι → F) (t : F)
    (P : jetSpace (ι := ι) (F := F) D) (a : Index ι D) :
    coordinates D (finiteTransport D z t P) a =
      ∑ b : Index ι D, entry z t a.val b.val * coordinates D P b := by
  change (transport z t P.val).coeff a.val = _
  conv_lhs => rw [← reconstruct_coordinates D P]
  simp only [reconstruct, map_sum, AddMonoidAlgebra.coeff_sum, Finsupp.finsetSum_apply]
  apply Finset.sum_congr rfl
  intro b _
  have hm : monomial b.val (coordinates D P b) =
      C (coordinates D P b) * monomial b.val 1 := by rw [C_mul_monomial, mul_one]
  rw [hm, map_mul]
  simp [entry, transport, coeff_C_mul, mul_comm]

end Coordinates

variable {κ : Type*}

abbrev Variable (ι κ : Type*) (D : ℕ) := ι ⊕ (κ × Index ι D)

def weight (D : ℕ) : Variable ι κ D → ℕ
  | .inl _ => 1
  | .inr (_, a) => a.val none

theorem weight_positive (D : ℕ) (a : Variable ι κ D) : 0 < weight D a := by
  cases a with
  | inl i => exact Nat.zero_lt_one
  | inr j => exact Nat.pos_of_ne_zero j.2.property.2

def matrix (D : ℕ) (z : ι → F) (t : F) : Variable ι κ D → Variable ι κ D → F
  | .inl i, .inl j => if i = j then t else 0
  | .inr (a, i), .inr (b, j) => if a = b then entry z t i.val j.val else 0
  | _, _ => 0

theorem matrix_diagonal (D : ℕ) (z : ι → F) (t : F) (i : Variable ι κ D) :
    matrix D z t i i = t^(weight D i) := by
  cases i with
  | inl i => simp [matrix, weight]
  | inr i => simp [matrix, weight, entry_on_or_above z t i.2.val i.2.val le_rfl]

theorem matrix_upper (D : ℕ) (z : ι → F) (t : F) (i j : Variable ι κ D)
    (hne : i ≠ j) (hw : weight D i ≤ weight D j) : matrix D z t i j = 0 := by
  classical
  cases i with
  | inl i =>
    cases j with
    | inl j => simp [matrix, show i ≠ j from fun h => hne (congrArg Sum.inl h)]
    | inr j => rfl
  | inr i =>
    cases j with
    | inl j => rfl
    | inr j =>
      rcases i with ⟨a, i⟩
      rcases j with ⟨b, j⟩
      by_cases hab : a = b
      · subst b
        have hij : j.val ≠ i.val := by
          intro he
          apply hne
          exact congrArg Sum.inr (Prod.ext rfl (Subtype.ext he.symm))
        simp [matrix, entry_on_or_above z t i.val j.val hw, hij]
      · simp [matrix, hab]

section Erasure
variable [Fintype ι] [Fintype κ]

def pointCoordinates (D : ℕ) (x : (ι → F) × Jets ι κ F D) : Variable ι κ D → F
  | .inl i => x.1 i
  | .inr (a, j) => coordinates D (x.2 a) j

def image (D : ℕ) (t : F) (o : (ι → F) × Jets ι κ F D) :
    Variable ι κ D → MvPolynomial (Variable ι κ D) F :=
  WeightedPhaseErasure.affineImage (pointCoordinates D o) (matrix D o.1 t)

theorem coordinate_point (D : ℕ) (t : F) (o x : (ι → F) × Jets ι κ F D)
    (i : Variable ι κ D) :
    pointCoordinates D (NonlinearJetChannel.publicPoint t (fun z => vectorTransport D z t) o x) i =
      pointCoordinates D o i + ∑ j, matrix D o.1 t i j * pointCoordinates D x j := by
  classical
  cases i with
  | inl i => simp [pointCoordinates, NonlinearJetChannel.publicPoint, matrix]
  | inr i =>
    rcases i with ⟨a, j⟩
    simp only [pointCoordinates, NonlinearJetChannel.publicPoint, Pi.add_apply, coordinates,
      Submodule.coe_add, AddMonoidAlgebra.coeff_add, Finsupp.add_apply]
    have ht : ((vectorTransport D o.1 t) x.2 a).val.coeff j.val =
        ∑ b, entry o.1 t j.val b.val * coordinates D (x.2 a) b :=
      coordinates_transport D o.1 t (x.2 a) j
    rw [ht]
    simp [matrix, coordinates, Fintype.sum_prod_type]

theorem image_eval (D : ℕ) (t : F) (o x : (ι → F) × Jets ι κ F D)
    (i : Variable ι κ D) :
    aeval (pointCoordinates D x) (image D t o i) =
      pointCoordinates D (NonlinearJetChannel.publicPoint t (fun z => vectorTransport D z t) o x) i := by
  rw [coordinate_point]
  simp [image, WeightedPhaseErasure.affineImage]

def mergedPolynomial {I : Type*} [Fintype I] (D : ℕ) (t : I → F)
    (o : I → (ι → F) × Jets ι κ F D) (P : I → MvPolynomial (Variable ι κ D) F) :=
  ∑ i, bind₁ (image D (t i) (o i)) (P i)

/-- No triangularity premise: it is derived from the actual Taylor map. -/
theorem fullJet_cancellation {I : Type*} [Fintype I] (D d : ℕ) (t : I → F)
    (o : I → (ι → F) × Jets ι κ F D) (P : I → MvPolynomial (Variable ι κ D) F)
    (hP : ∀ i, P i ∈ WeightedPhaseErasure.bounded (weight D) d)
    (hr : ∀ a : Variable ι κ D →₀ ℕ, Finsupp.weight (weight D) a = d →
      ∑ i, (t i)^d * (P i).coeff a = 0) :
    mergedPolynomial D t o P ∈ WeightedPhaseErasure.lower (weight D) d :=
  WeightedPhaseErasure.affine_cancellation (weight D) (weight_positive D) t
    (fun i => pointCoordinates D (o i)) (fun i => matrix D (o i).1 (t i))
    (fun i => matrix_diagonal D (o i).1 (t i))
    (fun i => matrix_upper D (o i).1 (t i)) d P hP hr

def polynomialPhase (D : ℕ) (chi : AddChar F ℂ) (P : MvPolynomial (Variable ι κ D) F)
    (x : (ι → F) × Jets ι κ F D) : ℂ := chi (aeval (pointCoordinates D x) P)

/-- Public lift columns suffice for every hidden parameter assignment. -/
theorem fullJet_lift_cancellation {I K : Type*} [Fintype I] [Fintype K]
    (D d : ℕ) (t : I → F) (o : I → (ι → F) × Jets ι κ F D)
    (P : I → MvPolynomial (Variable ι κ D) F)
    (hP : ∀ i, P i ∈ WeightedPhaseErasure.bounded (weight D) d)
    (c : I → (Variable ι κ D →₀ ℕ) → K → F) (theta : K → F)
    (hcoeff : ∀ a, Finsupp.weight (weight D) a = d →
      ∀ i, (P i).coeff a = ∑ k, c i a k * theta k)
    (hcolumn : ∀ a, Finsupp.weight (weight D) a = d →
      ∀ k, ∑ i, (t i)^d * c i a k = 0) :
    mergedPolynomial D t o P ∈ WeightedPhaseErasure.lower (weight D) d := by
  apply fullJet_cancellation D d t o P hP
  intro a ha
  simp_rw [hcoeff a ha]
  exact WeightedPhaseErasure.parameter_relation t d (fun i => c i a) theta (hcolumn a ha)

theorem merged_phase {I : Type*} [Fintype I] (D : ℕ) (chi : AddChar F ℂ)
    (t : I → F) (o : I → (ι → F) × Jets ι κ F D)
    (P : I → MvPolynomial (Variable ι κ D) F) :
    NonlinearJetChannel.mergedPhase (fun i => polynomialPhase D chi (P i)) t
      (fun i z => vectorTransport D z (t i)) o =
      polynomialPhase D chi (mergedPolynomial D t o P) := by
  funext x
  have h := WeightedPhaseErasure.merged_character chi
    (fun i => image D (t i) (o i)) P (pointCoordinates D x)
  simp only [image_eval] at h
  exact h

/-- An actual tensor-input Kraus branch with strictly reduced weighted phase.
No matrix-triangularity or Taylor-transport identity is left as a premise.
The tensor input still requires fresh, independent same-curve sources. -/
theorem degree_reduced_branch {I : Type*} [Fintype I] [Nonempty I] [Fintype F]
    (D d : ℕ) (Q : κ → MvPolynomial ι F) (hQ : ∀ a, (Q a).totalDegree ≤ D)
    (U : Submodule F (ι → F)) (chi : AddChar F ℂ)
    (t : I → F) (ht : ∀ i, t i ≠ 0)
    (o : I → (ι → F) × Jets ι κ F D) (P : I → MvPolynomial (Variable ι κ D) F)
    (hP : ∀ i, P i ∈ WeightedPhaseErasure.bounded (weight D) d)
    (hr : ∀ a : Variable ι κ D →₀ ℕ, Finsupp.weight (weight D) a = d →
      ∑ i, (t i)^d * (P i).coeff a = 0) :
    ∃ R : MvPolynomial (Variable ι κ D) F,
      R ∈ WeightedPhaseErasure.lower (weight D) d ∧
      ∀ x x' : (ι → F) × Jets ι κ F D,
        NonlinearJetChannel.branch
          (AffineSupportErasure.uniformAmplitude ((ι → F) × Jets ι κ F D))
          U (vectorJet D Q hQ) (fun i => polynomialPhase D chi (P i)) t
          (fun i z => vectorTransport D z (t i)) o x x' =
        AffineSupportErasure.invSize ((ι → F) × Jets ι κ F D) ^ Fintype.card I *
          NonlinearJetChannel.curveRho U (vectorJet D Q hQ) (polynomialPhase D chi R) x x' := by
  refine ⟨mergedPolynomial D t o P, fullJet_cancellation D d t o P hP hr, ?_⟩
  intro x x'
  rw [fullJet_mixed_branch D Q hQ U (fun i => polynomialPhase D chi (P i)) t ht o x x',
    merged_phase]

theorem terminal_kernel [Fintype F] (D : ℕ) (U : Submodule F (ι → F))
    (curve : (ι → F) → Jets ι κ F D) (chi : AddChar F ℂ)
    (hchi : ∀ r, chi r * star (chi r) = 1)
    (P : MvPolynomial (Variable ι κ D) F)
    (hP : P ∈ WeightedPhaseErasure.lower (weight D) 1)
    (x x' : (ι → F) × Jets ι κ F D) :
    NonlinearJetChannel.curveRho U curve (polynomialPhase D chi P) x x' =
      NonlinearJetChannel.curveRho U curve (fun _ => 1) x x' := by
  rw [WeightedPhaseErasure.constant_after_weight_one (weight D) (weight_positive D) P hP]
  simp only [polynomialPhase, aeval_C, Algebra.algebraMap_self_apply,
    NonlinearJetChannel.curveRho, mul_assoc, hchi, star_one, mul_one]

/-- A diagonal solver returns a nonzero VECTOR, not an everywhere nonzero
vector. At a positive stage the zero entries contribute nothing. -/
theorem active_relation {I : Type*} [Fintype I] (d : ℕ) (hd : 0 < d)
    (t v : I → F) :
    (∑ i : {i // t i ≠ 0}, (t i.val)^d * v i.val) = ∑ i, (t i)^d * v i := by
  classical
  have hz : (∑ i : {i // ¬t i ≠ 0}, (t i.val)^d * v i.val) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    have hi : t i.val = 0 := by simpa using i.property
    simp [hi, hd.ne']
  simpa only [hz, add_zero] using
    Fintype.sum_subtype_add_sum_subtype (fun i => t i ≠ 0) (fun i => (t i)^d * v i)

/-- The physical weighted branch for any nonzero diagonal witness. First
trace out zero-scale factors using discard_independent_curve_sources;
only this active subtype enters the invertible Taylor channel. The
normalization exponent is the ACTIVE count, not the solver arity. -/
theorem active_degree_reduced_branch {I : Type*} [Fintype I] [Fintype F]
    (D d : ℕ) (hd : 0 < d) (Q : κ → MvPolynomial ι F)
    (hQ : ∀ a, (Q a).totalDegree ≤ D)
    (U : Submodule F (ι → F)) (chi : AddChar F ℂ)
    (t : I → F) (ht : ∃ i, t i ≠ 0)
    (o : I → (ι → F) × Jets ι κ F D) (P : I → MvPolynomial (Variable ι κ D) F)
    (hP : ∀ i, P i ∈ WeightedPhaseErasure.bounded (weight D) d)
    (hr : ∀ a : Variable ι κ D →₀ ℕ, Finsupp.weight (weight D) a = d →
      ∑ i, (t i)^d * (P i).coeff a = 0) :
    ∃ R : MvPolynomial (Variable ι κ D) F,
      R ∈ WeightedPhaseErasure.lower (weight D) d ∧
      ∀ x x' : (ι → F) × Jets ι κ F D,
        NonlinearJetChannel.branch
          (AffineSupportErasure.uniformAmplitude ((ι → F) × Jets ι κ F D))
          U (vectorJet D Q hQ) (fun i : {i // t i ≠ 0} => polynomialPhase D chi (P i.val))
          (fun i => t i.val) (fun i z => vectorTransport D z (t i.val))
          (fun i => o i.val) x x' =
        AffineSupportErasure.invSize ((ι → F) × Jets ι κ F D) ^
          Fintype.card {i // t i ≠ 0} *
          NonlinearJetChannel.curveRho U (vectorJet D Q hQ) (polynomialPhase D chi R) x x' := by
  classical
  obtain ⟨i, hi⟩ := ht
  let : Nonempty {i // t i ≠ 0} := ⟨⟨i, hi⟩⟩
  apply degree_reduced_branch D d Q hQ U chi (fun i : {i // t i ≠ 0} => t i.val)
    (fun i => i.property) (fun i => o i.val) (fun i => P i.val) (fun i => hP i.val)
  intro a ha
  exact (active_relation d hd t (fun i => (P i).coeff a)).trans (hr a ha)

end Erasure

/-- info: 'QSearch.FullJetWeightedErasure.entry_on_or_above' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.entry_on_or_above
/-- info: 'QSearch.FullJetWeightedErasure.reconstruct_coordinates' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.reconstruct_coordinates
/-- info: 'QSearch.FullJetWeightedErasure.coordinates_transport' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.coordinates_transport
/-- info: 'QSearch.FullJetWeightedErasure.coordinate_point' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.coordinate_point
/-- info: 'QSearch.FullJetWeightedErasure.fullJet_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.fullJet_cancellation
/-- info: 'QSearch.FullJetWeightedErasure.degree_reduced_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.degree_reduced_branch
/-- info: 'QSearch.FullJetWeightedErasure.fullJet_lift_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.fullJet_lift_cancellation
/-- info: 'QSearch.FullJetWeightedErasure.terminal_kernel' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.terminal_kernel

/-- info: 'QSearch.NonlinearJetChannel.tensor_curve_trace_one' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.tensor_curve_trace_one
/-- info: 'QSearch.NonlinearJetChannel.discard_independent_curve_sources' depends on axioms: [propext,
 Classical.choice,
 Quot.sound] -/
#guard_msgs in
#print axioms QSearch.NonlinearJetChannel.discard_independent_curve_sources
/-- info: 'QSearch.FullJetWeightedErasure.active_relation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.active_relation
/-- info: 'QSearch.FullJetWeightedErasure.active_degree_reduced_branch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.FullJetWeightedErasure.active_degree_reduced_branch

end
end QSearch.FullJetWeightedErasure
