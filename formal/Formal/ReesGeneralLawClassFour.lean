import Formal.ReesGeneralLaw
import Formal.BCHClassFourSubgroups
import Formal.ReesGeneralReceiver

/-!
# The hypotheses of `ReesGeneralLaw` hold in class four

The quartic BCH product of `Formal/BCHClassFour.lean` is a
`NilpotentGroupLaw F 4` over any field with `2, 3 ≠ 0`, is additive on
Lie-commuting pairs, and over `ZMod p` (`p > 3`) satisfies Lazard's subgroup
direction by `BCHClassFourSubgroups.toLieSubalgebra`. So all three hypotheses
of the general-class file are discharged at `c = 4`, and every general-class
theorem specialises to an unconditional class-four theorem.

For `c ≥ 5` no instance is constructed.
-/

namespace QSearch.ReesGeneralLawClassFour

open LieModule QSearch.BCHClassFour QSearch.BCHClassFourSubgroups
  QSearch.ReesGeneralLaw QSearch.ReesLieInterpolation QSearch.ReesLieConstruction
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient QSearch.ReesGeneralReceiver
  QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver

noncomputable section

variable {F : Type} [Field F] [NeZero (2 : F)] [NeZero (3 : F)]

/-- The quartic BCH product as a natural group law for class at most four. -/
def bchLaw : NilpotentGroupLaw F 4 where
  mul _ _ _ x y := bch (F := F) x y
  natural φ x y := map_bch φ x y
  mul_assoc _ _ _ hM x y z := bch_assoc hM (NeZero.ne 2) (NeZero.ne 3) x y z
  zero_mul _ _ _ x := bch_zero_left x
  neg_mul _ _ _ x := bch_neg_left x

theorem bchLaw_additive : AdditiveOnCommuting (bchLaw (F := F)) :=
  fun _ _ _ _ _ h => bch_of_lie_eq_zero h

section PrimeField

variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]

/-- The law group and the `BCHClassFour.BCH` group are the same group on `val`. -/
def toBCH {M : Type} [LieRing M] [LieAlgebra (ZMod p) M]
    (hM : lowerCentralSeries (ZMod p) M M 4 = ⊥) :
    LawGroup (bchLaw (F := ZMod p)) M hM ≃* BCH (ZMod p) M hM where
  toFun x := ⟨x.val⟩
  invFun x := ⟨x.val⟩
  left_inv _ := rfl
  right_inv _ := rfl
  map_mul' _ _ := rfl

/-- Lazard's subgroup direction holds for the quartic law over `ZMod p`, `p > 3`. -/
theorem bchLaw_subgroups : SubgroupsAreSubalgebras (bchLaw (F := ZMod p)) := by
  intro M _ _ hM H
  refine ⟨toLieSubalgebra hM (H.map (toBCH hM).toMonoidHom), ?_⟩
  ext x
  rw [mem_subgroupOfLie, mem_toLieSubalgebra, Subgroup.mem_map_equiv]
  rfl

/-- The general-class tuple theorem, specialised to `c = 4`, for an arbitrary
subgroup `H`: every hypothesis is discharged. -/
theorem classFour_tuple_hides_arbitrary_subgroup {L O : Type} [LieRing L]
    [LieAlgebra (ZMod p) L] (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil)) (points : Fin 4 → ZMod p)
    (f : BaseGroup (bchLaw (F := ZMod p)) hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧
      ∀ a b : ReesGroup (bchLaw (F := ZMod p)) hnil,
        (fun i => f (evaluationHom hnil (points i) a)) =
            (fun i => f (evaluationHom hnil (points i) b)) ↔
          a⁻¹ * b ∈ ReesGeneralLaw.hiddenSubgroup hnil h points :=
  tuple_hides_arbitrary_subgroup hnil bchLaw_subgroups H points f hides

/-- The canonical points `1, 2, 3, 4`. -/
def canonicalPoints (p : ℕ) : Fin 4 → ZMod p := fun i => ((i.val + 1 : ℕ) : ZMod p)

omit [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] in
/-- For `p > 4` the canonical points are distinct and nonzero, so they are admissible. -/
theorem canonicalPoints_isUnit (hp : 4 < p) :
    IsUnit (evaluationMatrix (canonicalPoints p)).det := by
  apply ReesGeneralCover.field_points_isUnit
  · intro i j hij
    have h := (ZMod.natCast_eq_natCast_iff' _ _ _).mp hij
    rw [Nat.mod_eq_of_lt (by omega), Nat.mod_eq_of_lt (by omega)] at h
    exact Fin.ext (by omega)
  · intro i hi
    have h := (ZMod.natCast_eq_zero_iff _ _).mp hi
    exact absurd (Nat.le_of_dvd (by omega) h) (by omega)

/-- Class four, every hypothesis discharged, with explicit admissible points:
for every subgroup `H` of the class-four BCH group over `ZMod p` (`p > 4`) there is
a Lie subalgebra `h` with `H = exp h`, and the tuple of original oracle values at
the points `1, 2, 3, 4` hides exactly the elements all of whose Rees coefficients
lie in `h`. -/
theorem classFour_tuple_hides_coeff {L O : Type} [LieRing L]
    [LieAlgebra (ZMod p) L] (hp : 4 < p) (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
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

/-- One measured class-four descent step, with the quartic law, the public
section and the canonical points: only the source, the SDE witness and the
nonzero branch traces remain as inputs. -/
theorem classFour_step_output {I : Type*} [Fintype I] [Nonempty I] (hp : 4 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥) (h : LieSubalgebra (ZMod p) L)
    (d : ℕ) (hd : d + 1 ≤ 4)
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

/-- Class four, for an ARBITRARY subgroup `H`: `H = exp h` for a Lie subalgebra
`h`, and the terminal coset source of the tower retains all of `h`. -/
theorem classFour_terminal_source (hp : 4 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 4 = ⊥)
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

end PrimeField

end
end QSearch.ReesGeneralLawClassFour

/-- info: 'QSearch.ReesGeneralLawClassFour.bchLaw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.bchLaw

/-- info: 'QSearch.ReesGeneralLawClassFour.bchLaw_subgroups' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.bchLaw_subgroups

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_tuple_hides_coeff

/-- info: 'QSearch.ReesGeneralLawClassFour.classFour_terminal_source' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesGeneralLawClassFour.classFour_terminal_source
