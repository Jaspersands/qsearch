import Formal.ReesGeneralLaw
import Formal.BCHClassFiveSubgroups
import Formal.ReesGeneralReceiver
import Formal.ReesGeneralMeasuredReceiver

/-!
# The hypotheses of `ReesGeneralLaw` hold in class five

The quintic BCH product of `Formal/BCHClassFive.lean` is a
`NilpotentGroupLaw F 5` over any field with `2, 3, 5 ≠ 0`, is additive on
Lie-commuting pairs, and over `ZMod p` (`p > 5`) satisfies Lazard's subgroup
direction by `BCHClassFiveSubgroups.toLieSubalgebra`. So all three hypotheses
of the general-class file are discharged at `c = 5`, and every general-class
theorem specialises to an unconditional class-five theorem. This file mirrors
`ReesGeneralLawClassFour` line by line.

For `c ≥ 6` no instance is constructed.
-/

namespace QSearch.ReesGeneralLawClassFive

open LieModule QSearch.BCHClassFive QSearch.BCHClassFiveSubgroups
  QSearch.ReesGeneralLaw QSearch.ReesLieInterpolation QSearch.ReesLieConstruction
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient QSearch.ReesGeneralReceiver
  QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver

noncomputable section

variable {F : Type} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

/-- The quintic BCH product as a natural group law for class at most five. -/
def bchLaw : NilpotentGroupLaw F 5 where
  mul _ _ _ x y := bch (F := F) x y
  natural φ x y := map_bch φ x y
  mul_assoc _ _ _ hM x y z := bch_assoc hM (NeZero.ne 2) (NeZero.ne 3) (NeZero.ne 5) x y z
  zero_mul _ _ _ x := bch_zero_left x
  neg_mul _ _ _ x := bch_neg_left x

theorem bchLaw_additive : AdditiveOnCommuting (bchLaw (F := F)) :=
  fun _ _ _ _ _ h => bch_of_lie_eq_zero h

section PrimeField

variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]
  [NeZero (5 : ZMod p)]

/-- The law group and the `BCHClassFive.BCH` group are the same group on `val`. -/
def toBCH {M : Type} [LieRing M] [LieAlgebra (ZMod p) M]
    (hM : lowerCentralSeries (ZMod p) M M 5 = ⊥) :
    LawGroup (bchLaw (F := ZMod p)) M hM ≃* BCH (ZMod p) M hM where
  toFun x := ⟨x.val⟩
  invFun x := ⟨x.val⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_mul' _ _ := rfl

/-- Lazard's subgroup direction holds for the quintic law over `ZMod p`, `p > 5`. -/
theorem bchLaw_subgroups : SubgroupsAreSubalgebras (bchLaw (F := ZMod p)) := by
  intro M _ _ hM H
  refine ⟨toLieSubalgebra hM (H.map (toBCH hM).toMonoidHom), ?_⟩
  ext x
  rw [mem_subgroupOfLie, mem_toLieSubalgebra, Subgroup.mem_map_equiv]
  rfl

/-- The general-class tuple theorem, specialised to `c = 5`, for an arbitrary
subgroup `H`: every hypothesis is discharged. -/
theorem classFive_tuple_hides_arbitrary_subgroup {L O : Type} [LieRing L]
    [LieAlgebra (ZMod p) L] (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil)) (points : Fin 5 → ZMod p)
    (f : BaseGroup (bchLaw (F := ZMod p)) hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧
      ∀ a b : ReesGroup (bchLaw (F := ZMod p)) hnil,
        (fun i => f (evaluationHom hnil (points i) a)) =
            (fun i => f (evaluationHom hnil (points i) b)) ↔
          a⁻¹ * b ∈ ReesGeneralLaw.hiddenSubgroup hnil h points :=
  tuple_hides_arbitrary_subgroup hnil bchLaw_subgroups H points f hides

/-- The canonical points `1, 2, 3, 4, 5`. -/
def canonicalPoints (p : ℕ) : Fin 5 → ZMod p := fun i => ((i.val + 1 : ℕ) : ZMod p)

omit [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)] in
/-- For `p > 5` the canonical points are distinct and nonzero, so they are admissible. -/
theorem canonicalPoints_isUnit (hp : 5 < p) :
    IsUnit (evaluationMatrix (canonicalPoints p)).det := by
  apply ReesGeneralCover.field_points_isUnit
  · intro i j hij
    have h := (ZMod.natCast_eq_natCast_iff' _ _ _).mp hij
    rw [Nat.mod_eq_of_lt (by omega), Nat.mod_eq_of_lt (by omega)] at h
    exact Fin.ext (by omega)
  · intro i hi
    have h := (ZMod.natCast_eq_zero_iff _ _).mp hi
    exact absurd (Nat.le_of_dvd (by omega) h) (by omega)

/-- Class five, every hypothesis discharged, with explicit admissible points:
for every subgroup `H` of the class-five BCH group over `ZMod p` (`p > 5`) there is
a Lie subalgebra `h` with `H = exp h`, and the tuple of original oracle values at
the points `1, 2, 3, 4, 5` hides exactly the elements all of whose Rees coefficients
lie in `h`. -/
theorem classFive_tuple_hides_coeff {L O : Type} [LieRing L]
    [LieAlgebra (ZMod p) L] (hp : 5 < p) (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil))
    (f : BaseGroup (bchLaw (F := ZMod p)) hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧
      ∀ a b : ReesGroup (bchLaw (F := ZMod p)) hnil,
        (fun i => f (evaluationHom hnil (canonicalPoints p i) a)) =
            (fun i => f (evaluationHom hnil (canonicalPoints p i) b)) ↔
          ∀ r, coeff ((a⁻¹ * b).val : Current (ZMod p) L) r ∈ h := by
  obtain ⟨h, rfl⟩ := bchLaw_subgroups L hnil H
  exact ⟨h, rfl, tuple_hides_coeff hnil h (canonicalPoints p) (canonicalPoints_isUnit hp)
    f hides⟩

section Receiver

attribute [local instance] Classical.propDecidable ReesGeneralReceiver.truncFinite
  ReesGeneralReceiver.stageFintype ReesGeneralReceiver.centerFintype
  ReesGeneralReceiver.originalFintype

variable {L : Type} [LieRing L] [LieAlgebra (ZMod p) L] [Finite L]

/-- One measured class-five descent step, with the quintic law, the public
section and the canonical points: only the source, the SDE witness and the
nonzero branch traces remain as inputs. -/
theorem classFive_step_output {I : Type*} [Fintype I] [Nonempty I] (hp : 5 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥) (h : LieSubalgebra (ZMod p) L)
    (d : ℕ) (hd : d + 1 ≤ 5)
    (chi : AddChar (ZMod p) ℂ) (labels : I → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p)
    (nonzero_trace : ∀ i,
      (∑ x, projectedEntry (stageHidden (law := bchLaw) hnil h (canonicalPoints p) (d + 1) hd)
        (centralEmbedding bchLaw_additive d hd) (labelCharacter chi (labels i)) x x) ≠ 0)
    (scales : I → (ZMod p)ˣ)
    (sde : ∑ i, (scales i : ZMod p) ^ (d + 1) • labels i = 0)
    (q r : TruncGroup (L := L) (bchLaw (F := ZMod p)) d (by omega)) :
    actionOutput (fun x i => groupDilation (d + 1) hd (scales i) (canonicalSection d hd x))
      (fun x y : I → TruncGroup (L := L) (bchLaw (F := ZMod p)) (d + 1) hd =>
        ∏ i, normalizedEntry (stageHidden hnil h (canonicalPoints p) (d + 1) hd)
          (centralEmbedding bchLaw_additive d hd)
          (labelCharacter chi (labels i)) (x i) (y i)) q r =
      CosetSourceFourier.groupEntry (stageHidden hnil h (canonicalPoints p) d (by omega)) q r :=
  step_output_canonical bchLaw_additive hnil h (canonicalPoints p) (canonicalPoints_isUnit hp)
    d hd chi labels nonzero_trace scales sde q r

/-- Class five, for an ARBITRARY subgroup `H`: `H = exp h` for a Lie subalgebra
`h`, and the terminal coset source of the tower retains all of `h`. -/
theorem classFive_terminal_source (hp : 5 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil)) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧ ∀ x y : L,
      CosetSourceFourier.groupEntry (stageHidden hnil h (canonicalPoints p) 1 (by norm_num))
        ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd x))
        ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd y)) =
      if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  obtain ⟨h, rfl⟩ := bchLaw_subgroups L hnil H
  exact ⟨h, rfl, terminal_source bchLaw_additive hnil (by norm_num) h (canonicalPoints p)
    (canonicalPoints_isUnit hp)⟩

end Receiver

section Measured

open QSearch.ReesGeneralMeasuredReceiver

attribute [local instance] Classical.propDecidable ReesGeneralReceiver.truncFinite
  ReesGeneralReceiver.stageFintype ReesGeneralReceiver.centerFintype
  ReesGeneralReceiver.originalFintype

variable {L : Type} [LieRing L] [LieAlgebra (ZMod p) L] [Finite L]
  {I : ℕ → Type*} [∀ d, Fintype (I d)]

/-- Class five, for an ARBITRARY subgroup `H` of the quintic BCH group over
`ZMod p` (`p > 5`): `H = exp h`, and the four measured stages composed on
fresh banks, started from the exact top coset source at the points `1, ..., 5`,
end at the additive coset source of all of `h`. (Mirrors
`ReesGeneralMeasuredReceiver.classFour_measured_terminal_source`.) -/
theorem classFive_measured_terminal_source (hp : 5 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1)
    (policy : ∀ d (_ : d + 1 ≤ 5),
      (I d → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I d → ZMod p)
    (active : ∀ d hd labels, ∃ i, policy d hd labels i ≠ 0)
    (sde : ∀ d hd labels, ∑ i, policy d hd labels i ^ (d + 1) • labels i = 0) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧ ∀ x y : L,
      descend bchLaw_additive chi policy
          (Matrix.of (CosetSourceFourier.groupEntry
            (stageHidden hnil h (canonicalPoints p) 5 le_rfl))) 1 (by norm_num)
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd x))
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd y)) =
        if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  obtain ⟨h, rfl⟩ := bchLaw_subgroups L hnil H
  exact ⟨h, rfl, measured_terminal_source bchLaw_additive hnil (by norm_num) h
    (canonicalPoints p) (canonicalPoints_isUnit hp) chi hchi policy active sde⟩

end Measured

end PrimeField

end
end QSearch.ReesGeneralLawClassFive

/-- info: 'QSearch.ReesGeneralLawClassFive.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassFive.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_terminal_source

/-- info: 'QSearch.ReesGeneralLawClassFive.classFive_measured_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFive.classFive_measured_terminal_source
