import Formal.ClassThreePotential
import Formal.WeightedPhaseErasure
import Mathlib.Algebra.Lie.Nilpotent

/-!
# Ambient filtration behind the full-jet potential bound

Right-nested Lie words of length k lie in gamma_k. The last two possible
homogeneous degrees of a class-c section potential centralize [L,L].
The input-to-Lie-polynomial BCH identity is a separate certificate/prior-art
dependency, not an assumed identification of sampled polynomial values.
-/

namespace QSearch.AmbientPotentialFiltration

open ClassThreePotential WeightedPhaseErasure MvPolynomial
open scoped BigOperators
noncomputable section

variable {F L σ : Type*} [Field F] [LieRing L] [LieAlgebra F L]

def nested : List L → L
  | [] => 0
  | [x] => x
  | x :: y :: tail => ⁅x, nested (y :: tail)⁆

theorem nested_mem (word : List L) :
    nested word ∈ LieModule.lowerCentralSeries F L L (word.length-1) := by
  induction word with
  | nil => simp [nested]
  | cons x tail ih =>
    cases tail with
    | nil => simp [nested]
    | cons y tail =>
      simpa [nested, LieModule.lowerCentralSeries_succ] using
        LieSubmodule.lie_mem_lie (LieSubmodule.mem_top x) ih

theorem nested_derived (word : List L) (h : 2 ≤ word.length) :
    nested word ∈ derived (F := F) := by
  cases word with
  | nil => simp at h
  | cons x tail =>
    cases tail with
    | nil => simp at h
    | cons y tail => exact bracket_mem x (nested (y :: tail))

/-- gamma_(c-1) commutes with gamma_2 when gamma_(c+1)=0. Mathlib's
lowerCentralSeries is indexed from gamma_1 at zero. -/
theorem high_centralizes_derived (c : ℕ) (hc : 2 ≤ c)
    (hnil : LieModule.lowerCentralSeries F L L c = ⊥)
    (x : L) (hx : x ∈ LieModule.lowerCentralSeries F L L (c-2))
    (n : L) (hn : n ∈ derived (F := F)) : ⁅x, n⁆ = 0 := by
  have double (u v : L) : ⁅u, ⁅v, x⁆⁆ = 0 := by
    have h1 : ⁅v, x⁆ ∈ LieModule.lowerCentralSeries F L L ((c-2)+1) := by
      rw [LieModule.lowerCentralSeries_succ]
      exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top v) hx
    have h2 : ⁅u, ⁅v, x⁆⁆ ∈ LieModule.lowerCentralSeries F L L (((c-2)+1)+1) := by
      rw [LieModule.lowerCentralSeries_succ]
      exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top u) h1
    have he : ((c-2)+1)+1 = c := by omega
    simpa only [he, hnil, LieSubmodule.mem_bot] using h2
  induction hn using Submodule.span_induction with
  | mem z hz =>
    obtain ⟨⟨u, v⟩, rfl⟩ := hz
    rw [← lie_skew, lie_lie, double u v, double v u, sub_self, neg_zero]
  | zero => simp
  | add a b _ _ ha hb => simp only [lie_add, ha, hb, add_zero]
  | smul r a _ ha => simp only [lie_smul, ha, smul_zero]

theorem long_word_central (c : ℕ) (hc : 3 ≤ c)
    (hnil : LieModule.lowerCentralSeries F L L c = ⊥)
    (word : List L) (hlong : c-1 ≤ word.length) :
    nested word ∈ derived (F := F) ∧
      ∀ (n : L), n ∈ derived (F := F) → ⁅nested word, n⁆ = 0 := by
  constructor
  · exact nested_derived word (by omega)
  · intro n hn
    exact high_centralizes_derived c (by omega) hnil (nested word)
      (LieModule.antitone_lowerCentralSeries F L L (by omega) (nested_mem word)) n hn

/-- Scalar coordinates of N/Z(N) must kill the ACTUAL center of N, not
merely a selected central subspace. This is the projection premise. -/
def KillsDerivedCenter (P : L →ₗ[F] F) : Prop :=
  ∀ x ∈ derived (F := F), (∀ (n : L), n ∈ derived (F := F) → ⁅x, n⁆ = 0) → P x = 0

theorem long_word_projection_zero (c : ℕ) (hc : 3 ≤ c)
    (hnil : LieModule.lowerCentralSeries F L L c = ⊥)
    (P : L →ₗ[F] F) (hP : KillsDerivedCenter P)
    (word : List L) (hlong : c-1 ≤ word.length) : P (nested word) = 0 := by
  obtain ⟨hd, hz⟩ := long_word_central c hc hnil word hlong
  exact hP _ hd hz

/-- Each monomial from substituting linear inputs has as many quotient
variables as Lie-word leaves. No finite-field interpolation is used. -/
theorem projected_term_bound (c : ℕ) (hc : 3 ≤ c)
    (hnil : LieModule.lowerCentralSeries F L L c = ⊥)
    (P : L →ₗ[F] F) (hP : KillsDerivedCenter P)
    (word : List L) (a : σ →₀ ℕ) (ha : a.sum (fun _ k => k) = word.length) (r : F) :
    monomial a (r * P (nested word)) ∈ bounded (fun _ => 1) (c-2) := by
  classical
  by_cases hlong : c-1 ≤ word.length
  · simp [long_word_projection_zero c hc hnil P hP word hlong]
  · rw [bounded, monomial_mem_restrictSupport]
    left
    simp only [Set.mem_ofPred_eq, Finsupp.weight_apply, smul_eq_mul, mul_one]
    rw [ha]
    omega

theorem projected_polynomial_bound {I : Type*} (terms : Finset I)
    (c : ℕ) (hc : 3 ≤ c) (hnil : LieModule.lowerCentralSeries F L L c = ⊥)
    (P : L →ₗ[F] F) (hP : KillsDerivedCenter P)
    (word : I → List L) (a : I → σ →₀ ℕ) (r : I → F)
    (ha : ∀ i ∈ terms, (a i).sum (fun _ k => k) = (word i).length) :
    (∑ i ∈ terms, monomial (a i) (r i * P (nested (word i)))) ∈
      bounded (fun _ => 1) (c-2) :=
  (bounded _ _).sum_mem (fun i hi => projected_term_bound c hc hnil P hP _ _ (ha i hi) _)

/-- An adapted coordinate of weight w kills gamma_(w+1). This uses the
actual ambient filtration, not merely a weighted bracket tensor on N. -/
def KillsAboveWeight (P : L →ₗ[F] F) (w : ℕ) : Prop :=
  ∀ x ∈ LieModule.lowerCentralSeries F L L w, P x = 0

theorem filtered_word_projection_zero (P : L →ₗ[F] F) (w : ℕ)
    (hP : KillsAboveWeight P w) (word : List L) (hlong : w < word.length) :
    P (nested word) = 0 := by
  apply hP
  exact LieModule.antitone_lowerCentralSeries F L L (by omega) (nested_mem word)

theorem filtered_term_bound (P : L →ₗ[F] F) (w : ℕ)
    (hP : KillsAboveWeight P w) (word : List L)
    (a : σ →₀ ℕ) (ha : a.sum (fun _ k => k) = word.length) (r : F) :
    monomial a (r * P (nested word)) ∈ bounded (fun _ => 1) w := by
  classical
  by_cases hlong : w < word.length
  · simp [filtered_word_projection_zero P w hP word hlong]
  · rw [bounded, monomial_mem_restrictSupport]
    left
    simp only [Set.mem_ofPred_eq, Finsupp.weight_apply, smul_eq_mul, mul_one]
    rw [ha]
    omega

theorem filtered_polynomial_bound {I : Type*} (terms : Finset I)
    (P : L →ₗ[F] F) (w : ℕ) (hP : KillsAboveWeight P w)
    (word : I → List L) (a : I → σ →₀ ℕ) (r : I → F)
    (ha : ∀ i ∈ terms, (a i).sum (fun _ k => k) = (word i).length) :
    (∑ i ∈ terms, monomial (a i) (r i * P (nested (word i)))) ∈
      bounded (fun _ => 1) w :=
  (bounded _ _).sum_mem (fun i hi => filtered_term_bound P w hP _ _ (ha i hi) _)

/-- The central coordinates keep all BCH words through class c. Their
degree-c bound follows from word length, not from a fitted degree cap. -/
theorem unprojected_polynomial_bound {I : Type*} (terms : Finset I) (c : ℕ)
    (P : L →ₗ[F] F) (word : I → List L) (a : I → σ →₀ ℕ) (r : I → F)
    (ha : ∀ i ∈ terms, (a i).sum (fun _ k => k) = (word i).length)
    (hlen : ∀ i ∈ terms, (word i).length ≤ c) :
    (∑ i ∈ terms, monomial (a i) (r i * P (nested (word i)))) ∈
      bounded (fun _ => 1) c := by
  classical
  apply (bounded _ _).sum_mem
  intro i hi
  rw [bounded, monomial_mem_restrictSupport]
  left
  simpa only [Set.mem_ofPred_eq, Finsupp.weight_apply, smul_eq_mul, mul_one, ha i hi]
    using hlen i hi

/-- info: 'QSearch.AmbientPotentialFiltration.nested_mem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms nested_mem
/-- info: 'QSearch.AmbientPotentialFiltration.high_centralizes_derived' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms high_centralizes_derived
/-- info: 'QSearch.AmbientPotentialFiltration.long_word_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms long_word_central
/--
info: 'QSearch.AmbientPotentialFiltration.projected_polynomial_bound' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms projected_polynomial_bound
/--
info: 'QSearch.AmbientPotentialFiltration.unprojected_polynomial_bound' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms unprojected_polynomial_bound

/--
info: 'QSearch.AmbientPotentialFiltration.filtered_word_projection_zero' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms filtered_word_projection_zero
/--
info: 'QSearch.AmbientPotentialFiltration.filtered_polynomial_bound' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms filtered_polynomial_bound

end
end QSearch.AmbientPotentialFiltration
