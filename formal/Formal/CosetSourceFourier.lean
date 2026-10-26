import Formal.AffineSupportErasure
import Mathlib.Algebra.Group.AddChar
import Mathlib.Algebra.Group.Subgroup.Basic

/-!
# From group cosets to unknown-support phase kernels

The coordinate right-action law is an explicit hypothesis. Starting from
actual group-coset membership, derive the partial Fourier block by its two
normal-register sums. The hidden subgroup may have any rank.

This does not prove that a particular Lie group has the stated coordinates
or cubic potential, construct its QFT, or certify the full HSP algorithm.
-/

namespace QSearch.CosetSourceFourier

open scoped BigOperators
open QSearch.AffineSupportErasure
noncomputable section
attribute [local instance] Classical.propDecidable

variable {F V N G : Type*} [Field F] [AddCommGroup V] [Module F V]
  [AddCommGroup N] [Group G]

/-- A group source relation, not an assumed density-matrix formula.
`hidden` parametrizes every element of H, and the law covers every ambient
coordinate and every hidden element. Neither is a receiver input. -/
theorem coset_relation (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (Q : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a + Q (q + (u : V)) - Q q))
    (q r : V) (a b : N) :
    (coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b) ∈ H ↔
      r - q ∈ U ∧ b - a = Q r - Q q := by
  constructor
  · intro hedge
    let u : U := hidden.symm
      ⟨(coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b), hedge⟩
    have hu : (hidden u : G) =
        (coordinates.symm (q, a))⁻¹ * coordinates.symm (r, b) := by
      exact congrArg Subtype.val (hidden.apply_symm_apply _)
    have hc : (r, b) = (q + (u : V), a + Q (q + (u : V)) - Q q) := by
      simpa only [hu, mul_inv_cancel_left, Equiv.apply_symm_apply] using action q a u
    have hq : r = q + (u : V) := congrArg Prod.fst hc
    have hb : b = a + Q r - Q q := by
      simpa only [← hq] using congrArg Prod.snd hc
    constructor
    · have hd : r - q = (u : V) := by rw [hq]; abel
      rw [hd]
      exact u.property
    · rw [hb]
      abel
  · rintro ⟨hu, hb⟩
    let u : U := ⟨r - q, hu⟩
    have hq : q + (u : V) = r := by dsimp [u]; abel
    have hn : a + Q r - Q q = b := by
      calc
        a + Q r - Q q = a + (Q r - Q q) := by abel
        _ = a + (b - a) := by rw [hb]
        _ = b := by abel
    have hc := action q a u
    rw [hq, hn] at hc
    have hg : coordinates.symm (q, a) * (hidden u : G) =
        coordinates.symm (r, b) := coordinates.injective (by simpa using hc)
    rw [← hg, inv_mul_cancel_left]
    exact (hidden u).property

variable [Fintype G] [Fintype V] [Fintype N]

def groupEntry (H : Subgroup G) (g g' : G) : ℂ :=
  if g⁻¹ * g' ∈ H then invSize G else 0

/-- The positive-sign partial QFT block, including its 1/|N| factor. -/
def fourierBlock (coordinates : G ≃ V × N) (H : Subgroup G)
    (χ : AddChar N ℂ) (q r : V) : ℂ :=
  invSize N * ∑ a, ∑ b, χ a * groupEntry H (coordinates.symm (q, a))
    (coordinates.symm (r, b)) * star (χ b)

omit [Fintype G] [Fintype V] [Fintype N] in
theorem character_product (χ : AddChar N ℂ)
    (hunit : ∀ a, χ a * star (χ a) = 1) (a b : N) :
    χ a * star (χ b) = χ (a - b) := by
  rw [χ.map_sub_eq_div, div_eq_mul_inv]
  rw [eq_inv_of_mul_eq_one_right (hunit b)]

omit [AddCommGroup V] [AddCommGroup N] [Group G] in
theorem coordinate_size (coordinates : G ≃ V × N) :
    invSize G = invSize V * invSize N := by
  simp only [invSize, Fintype.card_congr coordinates, Fintype.card_prod,
    Nat.cast_mul, mul_inv_rev]
  ring

theorem mixed_source_identity (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (Q : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a + Q (q + (u : V)) - Q q))
    (χ : AddChar N ℂ) (hunit : ∀ a, χ a * star (χ a) = 1) (q r : V) :
    fourierBlock coordinates H χ q r =
      invSize N * rho U (fun x => χ (Q x)) q r := by
  have hsupport : r - q ∈ U ↔ q - r ∈ U := by
    constructor <;> intro h
    · simpa only [neg_sub] using U.neg_mem h
    · simpa only [neg_sub] using U.neg_mem h
  by_cases hu : r - q ∈ U
  · have hentry (a b : N) :
        groupEntry H (coordinates.symm (q, a)) (coordinates.symm (r, b)) =
          if b = a + (Q r - Q q) then invSize G else 0 := by
      have hdiff : b - a = Q r - Q q ↔ b = a + (Q r - Q q) := by
        rw [sub_eq_iff_eq_add]
        simp only [add_comm]
      simp only [groupEntry, coset_relation coordinates H U Q hidden action,
        hu, true_and, hdiff]
    have collapse (a : N) :
        (∑ b, χ a * (if b = a + (Q r - Q q) then invSize G else 0)
          * star (χ b)) = invSize G * χ (Q q - Q r) := by
      simp only [mul_ite, ite_mul, mul_zero, zero_mul]
      simp only [Finset.sum_ite_eq', Finset.mem_univ, ite_true]
      calc
        χ a * invSize G * star (χ (a + (Q r - Q q))) =
            invSize G * (χ a * star (χ (a + (Q r - Q q)))) := by ring
        _ = invSize G * χ (a - (a + (Q r - Q q))) := by
          rw [character_product χ hunit]
        _ = invSize G * χ (Q q - Q r) := by
          congr 2
          abel
    have hcard : (Fintype.card N : ℂ) ≠ 0 := by
      exact_mod_cast Fintype.card_ne_zero
    calc
      fourierBlock coordinates H χ q r =
          invSize N * ((Fintype.card N : ℂ) * (invSize G * χ (Q q - Q r))) := by
        simp only [fourierBlock, hentry, collapse, Finset.sum_const,
          Finset.card_univ, nsmul_eq_mul]
      _ = invSize G * χ (Q q - Q r) := by
        rw [← mul_assoc]
        simp [invSize, hcard]
      _ = invSize N * rho U (fun x => χ (Q x)) q r := by
        rw [coordinate_size coordinates]
        simp only [rho, hsupport.mp hu, ite_true]
        rw [← character_product χ hunit]
        ring
  · have hu' : q - r ∉ U := fun h => hu (hsupport.mpr h)
    simp only [fourierBlock, groupEntry,
      coset_relation coordinates H U Q hidden action, hu, false_and,
      ite_false, mul_zero, zero_mul, Finset.sum_const_zero, rho, hu']

/-- Every additive-character block has trace 1/|N|, including the trivial
character. Unitarity/completeness of a chosen family of characters is a
separate QFT fact, not assumed as this probability conclusion. -/
theorem label_probability (coordinates : G ≃ V × N) (H : Subgroup G)
    (U : Submodule F V) (Q : V → N) (hidden : U ≃ H)
    (action : ∀ q a u, coordinates (coordinates.symm (q, a) * (hidden u : G)) =
      (q + (u : V), a + Q (q + (u : V)) - Q q))
    (χ : AddChar N ℂ) (hunit : ∀ a, χ a * star (χ a) = 1) :
    (∑ q, fourierBlock coordinates H χ q q) = invSize N := by
  simp_rw [mixed_source_identity coordinates H U Q hidden action χ hunit]
  rw [← Finset.mul_sum, rho_trace_one U _ (fun q => hunit (Q q))]
  simp

/-- info: 'QSearch.CosetSourceFourier.coset_relation' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetSourceFourier.coset_relation

/-- info: 'QSearch.CosetSourceFourier.mixed_source_identity' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetSourceFourier.mixed_source_identity

/-- info: 'QSearch.CosetSourceFourier.label_probability' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.CosetSourceFourier.label_probability

end
end QSearch.CosetSourceFourier
