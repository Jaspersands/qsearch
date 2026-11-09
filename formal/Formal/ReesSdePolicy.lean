import Formal.ReesSdeWitness
import Formal.ReesGeneralMeasuredReceiver
import Formal.ReesGeneralLawClassSix

/-!
# Rees SDE: Chevalley–Warning witnesses as receiver policies

Source: `docs/papers/rees-hsp/main.tex`, Section `sec:formalization` (the receiver's SDE
policies were supplied inputs) and the Chevalley–Warning arity `gcd(d, p - 1) g_d + 1`.

`QSearch.ReesSdeWitness.exists_witness` works with columns in `K^a`. Here it is moved to
label columns in an arbitrary finite-dimensional space (`exists_witness_module`) and,
over `ZMod p`, to every exponent `d` (`exists_witness_module_gcd`). Choosing such a
witness for every label tuple gives a total SDE policy `cwPolicy` with the two
properties the measured receiver asks for (`cwPolicy_active`, `cwPolicy_sde`), as soon
as each bank at stage `d + 1` has more than `gcd(d + 1, p - 1) · dim` columns, `dim` the
dimension of the label space `(γ_{d+1})^*`. So `measured_terminal_source_cw` is the
general-class measured receiver with the policy inputs replaced by these bank sizes,
and `classSix_measured_terminal_source_cw` is its class-six instance, for an arbitrary
subgroup `H` of the sextic BCH group over `ZMod p` (`p > 6`), with no input left except
the bank sizes (and the exact initial coset source, as in every receiver theorem here).

The policy is chosen with `Classical.choose`: this is an existence statement. No search
procedure, running time or coherent circuit is formalized.
-/

namespace QSearch.ReesSdePolicy

open Module

section Witness

variable {K V ι : Type*} [Field K] [Fintype K] [DecidableEq K] [AddCommGroup V] [Module K V]
  [FiniteDimensional K V] [Fintype ι]

/-- **Chevalley–Warning in an arbitrary finite-dimensional space.** More than
`κ · dim V` columns `λ_i ∈ V` admit a nonzero `s` with `∑ s_i ^ κ λ_i = 0`. -/
theorem exists_witness_module {κ : ℕ} (hκ : 0 < κ) (hM : κ * finrank K V < Fintype.card ι)
    (col : ι → V) : ∃ s : ι → K, s ≠ 0 ∧ ∑ i, s i ^ κ • col i = 0 := by
  classical
  let b := Module.finBasis K V
  let e := Fintype.equivFin ι
  obtain ⟨s', hs', hsum⟩ := QSearch.ReesSdeWitness.exists_witness hκ hM
    (fun j => b.equivFun (col (e.symm j)))
  refine ⟨fun i => s' (e i), fun h => hs' (funext fun j => by simpa using congrFun h (e.symm j)),
    ?_⟩
  have h1 : b.equivFun (∑ j, s' j ^ κ • col (e.symm j)) = 0 := by
    rw [map_sum]
    simpa only [map_smul] using hsum
  have h2 : ∑ j, s' j ^ κ • col (e.symm j) = 0 :=
    b.equivFun.injective (by rw [h1, map_zero])
  rw [Fintype.sum_equiv e _ (fun j => s' j ^ κ • col (e.symm j)) (fun i => by simp), h2]

end Witness

section PrimeField

variable {p : ℕ} [Fact p.Prime]

/-- Over `ZMod p`, at any exponent `d ≥ 1`, more than `gcd(d, p - 1) · dim V` columns in
a finite-dimensional space `V` admit a nonzero solution (Chevalley–Warning at the reduced
exponent, then the Bezout lift). -/
theorem exists_witness_module_gcd {V ι : Type*} [AddCommGroup V] [Module (ZMod p) V]
    [FiniteDimensional (ZMod p) V] [Fintype ι] {d : ℕ} (hd : 0 < d)
    (hM : Nat.gcd d (p - 1) * finrank (ZMod p) V < Fintype.card ι) (col : ι → V) :
    ∃ s : ι → ZMod p, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0 := by
  obtain ⟨u, hu, hsum⟩ := exists_witness_module (Nat.gcd_pos_of_pos_left _ hd) hM col
  obtain ⟨s, hs, -, hssum⟩ := QSearch.ReesSdeGcd.bezout_witness hd col u hu hsum
  exact ⟨s, hs, hssum⟩

open LieModule QSearch.ReesLieConstruction QSearch.ReesGeneralLaw QSearch.ReesGeneralReceiver
  QSearch.ReesGeneralMeasuredReceiver QSearch.ReesLieInterpolation QSearch.ReesCentralQuotient
  QSearch.ReesHomogenization QSearch.CentralCharacterDescent QSearch.CentralQuotientReceiver

attribute [local instance] Classical.propDecidable ReesGeneralReceiver.truncFinite
  ReesGeneralReceiver.stageFintype ReesGeneralReceiver.centerFintype
  ReesGeneralReceiver.originalFintype

variable {c : ℕ} {L : Type} [LieRing L] [LieAlgebra (ZMod p) L] [Finite L]
  {I : ℕ → Type*} [∀ d, Fintype (I d)]

local instance labelFinite (d : ℕ) : Finite (gamma (ZMod p) L d →ₗ[ZMod p] ZMod p) :=
  Finite.of_injective (fun f : gamma (ZMod p) L d →ₗ[ZMod p] ZMod p =>
    (f : gamma (ZMod p) L d → ZMod p)) DFunLike.coe_injective

/-- The bank-size condition: at stage `d + 1` the bank has more than
`gcd(d + 1, p - 1) · dim (γ_{d+1})^*` columns. -/
def BankSizes (c : ℕ) (L : Type) [LieRing L] [LieAlgebra (ZMod p) L] (I : ℕ → Type*)
    [∀ d, Fintype (I d)] : Prop :=
  ∀ d, d + 1 ≤ c → Nat.gcd (d + 1) (p - 1) *
    finrank (ZMod p) (gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) < Fintype.card (I d)

/-- A total SDE policy: for every label tuple, a Chevalley–Warning witness. -/
noncomputable def cwPolicy (hbank : BankSizes (p := p) c L I) :
    ∀ d (_ : d + 1 ≤ c), (I d → gamma (ZMod p) L (d + 1) →ₗ[ZMod p] ZMod p) → I d → ZMod p :=
  fun d hd labels => Classical.choose
    (exists_witness_module_gcd (Nat.succ_pos d) (hbank d hd) labels)

theorem cwPolicy_active (hbank : BankSizes (p := p) c L I) :
    ∀ d hd labels, ∃ i, cwPolicy hbank d hd labels i ≠ 0 := fun d hd labels =>
  Function.ne_iff.mp (Classical.choose_spec
    (exists_witness_module_gcd (Nat.succ_pos d) (hbank d hd) labels)).1

theorem cwPolicy_sde (hbank : BankSizes (p := p) c L I) :
    ∀ d hd labels, ∑ i, cwPolicy hbank d hd labels i ^ (d + 1) • labels i = 0 :=
  fun d hd labels => (Classical.choose_spec
    (exists_witness_module_gcd (Nat.succ_pos d) (hbank d hd) labels)).2

/-- **The general-class measured receiver with Chevalley–Warning policies.** Given a
natural group law, additive on commuting pairs, the composed receiver run with the
policy `cwPolicy` (no policy input) ends at the additive coset source of all of `h`,
provided every bank is larger than `gcd(d + 1, p - 1) · dim (γ_{d+1})^*`. -/
theorem measured_terminal_source_cw {law : NilpotentGroupLaw (ZMod p) c}
    (hadd : AdditiveOnCommuting law) (hnil : lowerCentralSeries (ZMod p) L L c = ⊥)
    (hc : 1 ≤ c) (h : LieSubalgebra (ZMod p) L) (points : Fin c → ZMod p)
    (invertible : IsUnit (evaluationMatrix points).det)
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1) (hbank : BankSizes (p := p) c L I)
    (x y : L) :
    descend hadd chi (cwPolicy hbank)
        (Matrix.of (CosetSourceFourier.groupEntry (stageHidden hnil h points c le_rfl))) 1 hc
        ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd x))
        ((terminalGroupEquiv hadd hc).symm (Multiplicative.ofAdd y)) =
      if y - x ∈ h then AffineSupportErasure.invSize L else 0 :=
  measured_terminal_source hadd hnil hc h points invertible chi hchi (cwPolicy hbank)
    (cwPolicy_active hbank) (cwPolicy_sde hbank) x y

section ClassSix

open QSearch.ReesGeneralLawClassSix

variable [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)]

/-- **Class six, policies discharged.** For an ARBITRARY subgroup `H` of the sextic BCH
group over `ZMod p` (`p > 6`): `H = exp h`, and the five measured stages, run with the
Chevalley–Warning policies on banks of the stated sizes and started from the exact top
coset source at the points `1, ..., 6`, end at the additive coset source of all of `h`. -/
theorem classSix_measured_terminal_source_cw (hp : 6 < p)
    (hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥)
    (H : Subgroup (BaseGroup (bchLaw (F := ZMod p)) hnil))
    (chi : AddChar (ZMod p) ℂ) (hchi : chi ≠ 1) (hbank : BankSizes (p := p) 6 L I) :
    ∃ h : LieSubalgebra (ZMod p) L, H = subgroupOfLie hnil h ∧ ∀ x y : L,
      descend bchLaw_additive chi (cwPolicy hbank)
          (Matrix.of (CosetSourceFourier.groupEntry
            (stageHidden hnil h (canonicalPoints p) 6 le_rfl))) 1 (by norm_num)
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd x))
          ((terminalGroupEquiv bchLaw_additive (by norm_num)).symm (Multiplicative.ofAdd y)) =
        if y - x ∈ h then AffineSupportErasure.invSize L else 0 := by
  obtain ⟨h, rfl⟩ := bchLaw_subgroups L hnil H
  exact ⟨h, rfl, measured_terminal_source_cw bchLaw_additive hnil (by norm_num) h
    (canonicalPoints p) (canonicalPoints_isUnit hp) chi hchi hbank⟩

end ClassSix

end PrimeField

end QSearch.ReesSdePolicy

/-- info: 'QSearch.ReesSdePolicy.exists_witness_module' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.exists_witness_module

/-- info: 'QSearch.ReesSdePolicy.exists_witness_module_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.exists_witness_module_gcd

/-- info: 'QSearch.ReesSdePolicy.cwPolicy_active' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.cwPolicy_active

/-- info: 'QSearch.ReesSdePolicy.cwPolicy_sde' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.cwPolicy_sde

/-- info: 'QSearch.ReesSdePolicy.measured_terminal_source_cw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.measured_terminal_source_cw

/-- info: 'QSearch.ReesSdePolicy.classSix_measured_terminal_source_cw' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdePolicy.classSix_measured_terminal_source_cw
