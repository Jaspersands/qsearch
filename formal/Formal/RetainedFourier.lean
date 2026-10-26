import Formal.CentralRegularSource
import Formal.ClassThreeMonomial
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.NumberTheory.LegendreSymbol.AddCharacter

/-!
# Complete coherent Fourier transform of the retained B register

The compiler indexes frequencies by linear functionals, while the earlier
partial-Fourier identity uses all additive characters. A nontrivial fixed
base character identifies these index sets over a finite field. The base
character is NOT the measured central label: zero central labels are valid.
No irreducible QFT or measurement of the retained frequency is introduced.
-/

namespace QSearch.RetainedFourier

noncomputable section
open scoped BigOperators
open AffineSupportErasure
attribute [local instance] Classical.propDecidable

variable {F B : Type*} [Field F] [AddCommGroup B] [Module F B]

def linearCharacter (chi : AddChar F ℂ) : (B →ₗ[F] F) →+ AddChar B ℂ where
  toFun mu := chi.compAddMonoidHom mu.toAddMonoidHom
  map_zero' := by ext y; simp
  map_add' mu nu := by ext y; simp [chi.map_add_eq_mul]

@[simp] theorem linearCharacter_apply (chi : AddChar F ℂ) (mu : B →ₗ[F] F) (y : B) :
    linearCharacter chi mu y = chi (mu y) := rfl

/-- Nontriviality, rather than pointwise injectivity of chi, suffices.
This also covers extension fields, whose additive characters have kernels. -/
theorem linearCharacter_injective (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    Function.Injective (linearCharacter chi : (B →ₗ[F] F) → AddChar B ℂ) := by
  intro mu nu h
  ext y
  apply AddChar.to_mulShift_inj_of_isPrimitive (AddChar.IsPrimitive.of_ne_one hchi)
  ext c
  have hc := DFunLike.congr_fun h (c • y)
  simpa [AddChar.mulShift_apply, map_smul, smul_eq_mul, mul_comm] using hc

section Finite
variable [Fintype B]

theorem linearCharacter_bijective [Fintype (B →ₗ[F] F)]
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    Function.Bijective (linearCharacter chi : (B →ₗ[F] F) → AddChar B ℂ) := by
  rw [Fintype.bijective_iff_injective_and_card, AddChar.card_eq]
  refine ⟨linearCharacter_injective chi hchi, ?_⟩
  exact Fintype.card_congr (Module.Basis.ofVectorSpace F B).toDualEquiv.symm.toEquiv

def characterEquiv [Fintype (B →ₗ[F] F)] (chi : AddChar F ℂ) (hchi : chi ≠ 1) :
    (B →ₗ[F] F) ≃ AddChar B ℂ :=
  Equiv.ofBijective (linearCharacter chi) (linearCharacter_bijective chi hchi)

def amplitude (chi : AddChar F ℂ) (mu : B →ₗ[F] F) (y : B) : ℂ :=
  uniformAmplitude B * star (chi (mu y))

/-- All linear frequencies, including zero, form a complete coherent transform. -/
theorem columns_orthonormal [Fintype (B →ₗ[F] F)]
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (y z : B) :
    (∑ mu : B →ₗ[F] F, star (amplitude chi mu y) * amplitude chi mu z) =
      if y = z then 1 else 0 := by
  have point (mu : B →ₗ[F] F) :
      star (amplitude chi mu y) * amplitude chi mu z =
        invSize B * (star (linearCharacter chi mu z) * linearCharacter chi mu y) := by
    simp only [amplitude, star_mul, star_star, linearCharacter_apply]
    calc
      _ = (uniformAmplitude B * star (uniformAmplitude B)) *
          (star (chi (mu z)) * chi (mu y)) := by ring
      _ = _ := by rw [uniformAmplitude_normalized]
  simp_rw [point]
  rw [← Finset.mul_sum]
  have he := Equiv.sum_comp (characterEquiv (B := B) chi hchi)
    (fun ch : AddChar B ℂ => star (ch z) * ch y)
  change (∑ mu : B →ₗ[F] F, star (linearCharacter chi mu z) * linearCharacter chi mu y) = _ at he
  rw [he, CentralRegularSource.dual_orthogonality]
  have hc : (Fintype.card B : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  by_cases h : y = z <;> simp [h, eq_comm, invSize, hc]

theorem rows_orthonormal [Fintype F]
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (mu nu : B →ₗ[F] F) :
    (∑ y, amplitude chi mu y * star (amplitude chi nu y)) =
      if mu = nu then 1 else 0 := by
  have point (y : B) : amplitude chi mu y * star (amplitude chi nu y) =
      invSize B * linearCharacter chi (nu-mu) y := by
    simp only [amplitude, star_mul, star_star]
    calc
      _ = (uniformAmplitude B * star (uniformAmplitude B)) *
          (chi (nu y) * star (chi (mu y))) := by ring
      _ = _ := by
        rw [uniformAmplitude_normalized,
          CosetSourceFourier.character_product chi (CentralRegularSource.character_unit chi)]
        rfl
  simp_rw [point]
  rw [← Finset.mul_sum, AddChar.sum_eq_ite]
  have hz : linearCharacter chi (nu-mu) = 0 ↔ mu = nu := by
    rw [← map_zero (linearCharacter (B := B) chi),
      (linearCharacter_injective chi hchi).eq_iff, sub_eq_zero, eq_comm]
  have hc : (Fintype.card B : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp only [hz]
  by_cases h : mu = nu <;> simp [h, invSize, hc]

/-- Actual F_- M F_-^dag, with the frequency still a coherent register. -/
def branch (chi : AddChar F ℂ) (alpha : ℂ) (ell mu nu : B →ₗ[F] F) (d : B) : ℂ :=
  ∑ y, ∑ z, amplitude chi nu z *
    (if z = y+d then alpha * chi (ell y) else 0) * star (amplitude chi mu y)

theorem branch_eq_partial (chi : AddChar F ℂ) (alpha : ℂ)
    (ell mu nu : B →ₗ[F] F) (d : B) :
    branch chi alpha ell mu nu d = ClassThreeMonomial.partialFourierEntry alpha
      (linearCharacter chi ell) (linearCharacter chi mu) (linearCharacter chi nu) d := by
  unfold branch ClassThreeMonomial.partialFourierEntry
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro y _
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro z _
  by_cases h : z = y+d
  · simp only [ite_eq_left h, amplitude, star_mul, star_star, linearCharacter_apply]
    calc
      _ = (uniformAmplitude B * star (uniformAmplitude B)) *
          (star (chi (nu z)) * (alpha * chi (ell y)) * chi (mu y)) := by ring
      _ = _ := by rw [uniformAmplitude_normalized]
  · simp [h]

/-- The phase is evaluated at the SHIFTED output frequency nu=mu+ell. -/
theorem branch_formula (chi : AddChar F ℂ) (hchi : chi ≠ 1) (alpha : ℂ)
    (ell mu nu : B →ₗ[F] F) (d : B) :
    branch chi alpha ell mu nu d =
      if nu = mu+ell then alpha * star (chi (nu d)) else 0 := by
  rw [branch_eq_partial, ClassThreeMonomial.partial_fourier_identity alpha _ _ _
    (CentralRegularSource.character_unit (linearCharacter chi nu))]
  simp only [← map_add, (linearCharacter_injective chi hchi).eq_iff, linearCharacter_apply]

variable {A : Type*} [AddCommGroup A] [Module F A]

omit [Fintype B] in
/-- The modulation and shift are derived from the actual BCH coordinate product. -/
theorem coordinate_action (S : ClassThreeMonomial.StructureMaps F A B)
    (g : ClassThreeMonomial.Element F A B) (x : A) (y : B) :
    ClassThreeMonomial.product S g (x,y,0) =
      (x+g.1, y+(g.2.1+(2 : F)⁻¹ • S.beta g.1 x),
       ClassThreeMonomial.rawPhase S g x+((2 : F)⁻¹ • S.delta g.1) y) := by
  apply Prod.ext
  · simp only [ClassThreeMonomial.product]; abel
  apply Prod.ext
  · simp only [ClassThreeMonomial.product]; abel
  simp only [ClassThreeMonomial.product, ClassThreeMonomial.rawPhase,
    add_zero, LinearMap.smul_apply, smul_eq_mul]
  ring

def classThreeEntry (S : ClassThreeMonomial.StructureMaps F A B)
    (chi : AddChar F ℂ) (g : ClassThreeMonomial.Element F A B)
    (x x' : A) (mu nu : B →ₗ[F] F) : ℂ :=
  ∑ y, ∑ z, amplitude chi nu z *
    (let out := ClassThreeMonomial.product S g (x,y,0)
     if (x',z) = (out.1,out.2.1) then chi out.2.2 else 0) * star (amplitude chi mu y)

theorem classThree_eq_branch (S : ClassThreeMonomial.StructureMaps F A B)
    (chi : AddChar F ℂ) (g : ClassThreeMonomial.Element F A B)
    (x x' : A) (mu nu : B →ₗ[F] F) :
    classThreeEntry S chi g x x' mu nu =
      if x' = x+g.1 then
        branch chi (chi (ClassThreeMonomial.rawPhase S g x)) ((2 : F)⁻¹ • S.delta g.1)
          mu nu (g.2.1+(2 : F)⁻¹ • S.beta g.1 x)
      else 0 := by
  by_cases hx : x' = x+g.1
  · simp only [classThreeEntry, coordinate_action, Prod.mk.injEq, hx, true_and,
      chi.map_add_eq_mul, ite_true, branch]
  · simp [classThreeEntry, coordinate_action, hx]

/-- The complete B transform yields the compiler's actual displacement and phase.
The scalar maps here are central-character projections; they can all vanish. -/
theorem classThree_formula [Fintype F] (S : ClassThreeMonomial.StructureMaps F A B)
    (chi : AddChar F ℂ) (hchi : chi ≠ 1) (g : ClassThreeMonomial.Element F A B)
    (x x' : A) (mu nu : B →ₗ[F] F) :
    classThreeEntry S chi g x x' mu nu =
      if (x', nu) = ClassThreeMonomial.displacement S g (x, mu) then
        chi (ClassThreeMonomial.phase S g (x, mu)) else 0 := by
  rw [classThree_eq_branch, branch_formula chi hchi]
  by_cases hx : x' = x+g.1
  · by_cases hn : nu = mu+(2 : F)⁻¹ • S.delta g.1
    · simp only [hx, hn, ite_true, ClassThreeMonomial.displacement]
      rw [CosetSourceFourier.character_product chi (CentralRegularSource.character_unit chi)]
      rfl
    · simp [hx, hn, ClassThreeMonomial.displacement]
  · simp [hx, ClassThreeMonomial.displacement]

theorem trivial_character_columns_equal (mu : B →ₗ[F] F) (y z : B) :
    amplitude (1 : AddChar F ℂ) mu y = amplitude 1 mu z := by
  simp [amplitude]

end Finite

/-- info: 'QSearch.RetainedFourier.linearCharacter_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.linearCharacter_injective

/-- info: 'QSearch.RetainedFourier.linearCharacter_bijective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.linearCharacter_bijective

/-- info: 'QSearch.RetainedFourier.columns_orthonormal' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.columns_orthonormal

/-- info: 'QSearch.RetainedFourier.rows_orthonormal' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.rows_orthonormal

/-- info: 'QSearch.RetainedFourier.coordinate_action' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.coordinate_action

/-- info: 'QSearch.RetainedFourier.branch_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.branch_formula

/-- info: 'QSearch.RetainedFourier.classThree_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.classThree_formula

/-- info: 'QSearch.RetainedFourier.trivial_character_columns_equal' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.RetainedFourier.trivial_character_columns_equal

end
end QSearch.RetainedFourier
