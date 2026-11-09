import Formal.ReesGeneralLaw
import Formal.BCHClassThreeSubgroups

/-!
# The hypotheses of `ReesGeneralLaw` hold in class three

The cubic BCH product of `Formal/BCHClassThree.lean` is a
`NilpotentGroupLaw F 3` over any field with `2, 3 ≠ 0`, is additive on
Lie-commuting pairs, and over `ZMod p` (`p > 3`) satisfies Lazard's subgroup
direction by `BCHClassThreeSubgroups.toLieSubalgebra`. So the three hypotheses
of the general-class file are consistent and are met at `c = 3`, and the
general-class theorems specialise to the existing class-three results.

The class-four instance is `ReesGeneralLawClassFour`; for `c ≥ 5` no instance
is constructed.
-/

namespace QSearch.ReesGeneralLawClassThree

open LieModule QSearch.BCHClassThree QSearch.BCHClassThreeSubgroups
  QSearch.ReesGeneralLaw QSearch.ReesLieInterpolation

noncomputable section

variable {F : Type} [Field F] [NeZero (2 : F)] [NeZero (3 : F)]

/-- The cubic BCH product as a natural group law for class at most three. -/
def bchLaw : NilpotentGroupLaw F 3 where
  mul _ _ _ x y := bch (F := F) x y
  natural φ x y := map_bch φ x y
  mul_assoc _ _ _ hM x y z := bch_assoc hM (NeZero.ne 2) (NeZero.ne 3) x y z
  zero_mul _ _ _ x := bch_zero_left x
  neg_mul _ _ _ x := bch_neg_left x

theorem bchLaw_additive : AdditiveOnCommuting (bchLaw (F := F)) :=
  fun _ _ _ _ _ h => bch_of_lie_eq_zero h

section PrimeField

variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]

/-- The law group and the existing `BCH` group are the same group on `val`. -/
def toBCH {M : Type} [LieRing M] [LieAlgebra (ZMod p) M]
    (hM : lowerCentralSeries (ZMod p) M M 3 = ⊥) :
    LawGroup (bchLaw (F := ZMod p)) M hM ≃* BCH (ZMod p) M hM where
  toFun x := ⟨x.val⟩
  invFun x := ⟨x.val⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_mul' _ _ := rfl

/-- Lazard's subgroup direction holds for the cubic law over `ZMod p`, `p > 3`. -/
theorem bchLaw_subgroups : SubgroupsAreSubalgebras (bchLaw (F := ZMod p)) := by
  intro M _ _ hM H
  refine ⟨toLieSubalgebra hM (H.map (toBCH hM).toMonoidHom), ?_⟩
  ext x
  rw [mem_subgroupOfLie, mem_toLieSubalgebra, Subgroup.mem_map_equiv]
  rfl

/-- The general-class tuple theorem, specialised to `c = 3`, for an arbitrary
subgroup `H`: every hypothesis is discharged. -/
theorem classThree_tuple_hides_arbitrary_subgroup {L O : Type} [LieRing L]
    [LieAlgebra (ZMod p) L] (hnil : lowerCentralSeries (ZMod p) L L 3 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil)) (points : Fin 3 → ZMod p)
    (f : BaseGroup (bchLaw (F := ZMod p)) hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧
      ∀ a b : ReesGroup (bchLaw (F := ZMod p)) hnil,
        (fun i => f (evaluationHom hnil (points i) a)) =
            (fun i => f (evaluationHom hnil (points i) b)) ↔
          a⁻¹ * b ∈ ReesGeneralLaw.hiddenSubgroup hnil h points :=
  tuple_hides_arbitrary_subgroup hnil bchLaw_subgroups H points f hides

end PrimeField

end
end QSearch.ReesGeneralLawClassThree
