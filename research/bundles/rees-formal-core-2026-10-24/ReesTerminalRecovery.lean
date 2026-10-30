import ReesNativeSource
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.Analysis.SpecialFunctions.Complex.CircleAddChar

/-!
The terminal Fourier measurement is defined on arbitrary density entries,
not on a supplied hidden subspace. Exact recovery is conditional on the
sampled linear forms spanning the annihilator; no finite-sample certainty.
-/
namespace QSearch.ReesTerminalRecovery
open scoped BigOperators
open ReesCentralInstrument ReesGroupBridge ReesQuotients ReesStageInstrument
  ReesRecursiveSource ReesNativeSource
noncomputable section
attribute [local instance] Classical.propDecidable

section Fourier
variable {F V : Type*} [Field F] [AddCommGroup V] [Module F V] [Fintype V]

def additiveSource (H : Submodule F V) (x y : V) : ℂ :=
  (Fintype.card V : ℂ)⁻¹ * if x-y ∈ H then 1 else 0

/-- The diagonal entry of U rho U*, with U[l,x]=chi(l(x))/sqrt(|V|). -/
def fourierReadout (psi : AddChar F ℂ) (rho : V → V → ℂ) (l : Module.Dual F V) : ℂ :=
  (Fintype.card V : ℂ)⁻¹ *
    ∑ x, ∑ y, psi (l x) * rho x y * star (psi (l y))

omit [Fintype V] in
theorem character_unit_pair (psi : AddChar F ℂ)
    (unitary : ∀ z, psi z * star (psi z) = 1) (l : Module.Dual F V) (x y : V) :
    psi (l (x+y)) * star (psi (l y)) = psi (l x) := by
  rw [map_add, psi.map_add_eq_mul, mul_assoc, unitary, mul_one]

omit [Fintype V] in
theorem restriction_trivial_iff (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (H : Submodule F V) (l : Module.Dual F V) :
    psi.compAddMonoidHom (l.comp H.subtype).toAddMonoidHom = 0 ↔
      l ∈ H.dualAnnihilator := by
  rw [Submodule.mem_dualAnnihilator]
  constructor
  · intro he x hx
    have hh := congrArg (fun f : AddChar H ℂ => f ⟨x,hx⟩) he
    apply faithful
    simpa using hh
  · intro he
    ext x
    simp [he x.val x.property]

theorem subgroup_character_sum (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (H : Submodule F V) (l : Module.Dual F V) :
    (∑ x : H, psi (l x)) =
      if l ∈ H.dualAnnihilator then (Fintype.card H : ℂ) else 0 := by
  have hs := (psi.compAddMonoidHom (l.comp H.subtype).toAddMonoidHom).sum_eq_ite
  simpa only [AddChar.compAddMonoidHom_apply, LinearMap.toAddMonoidHom_coe,
    LinearMap.comp_apply, Submodule.subtype_apply, restriction_trivial_iff psi faithful H l] using hs

theorem fourier_source (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (unitary : ∀ z, psi z * star (psi z) = 1) (H : Submodule F V)
    (l : Module.Dual F V) :
    fourierReadout psi (additiveSource H) l =
      if l ∈ H.dualAnnihilator then (Fintype.card H : ℂ) / Fintype.card V else 0 := by
  have hn : (Fintype.card V : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have inner (y : V) :
      (∑ x, psi (l x) * additiveSource H x y * star (psi (l y))) =
        (Fintype.card V : ℂ)⁻¹ * ∑ x : H, psi (l x) := by
    calc
      _ = ∑ x, psi (l (x+y)) * additiveSource H (x+y) y * star (psi (l y)) := by
        symm
        exact Fintype.sum_equiv (Equiv.addRight y) _ _ (fun x => rfl)
      _ = (Fintype.card V : ℂ)⁻¹ * ∑ x, if x ∈ H then psi (l x) else 0 := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro x _
        simp only [additiveSource, add_sub_cancel_right]
        split_ifs <;> simp_all only [mul_one, mul_zero, zero_mul]
        rw [mul_right_comm, character_unit_pair psi unitary]
        exact mul_comm _ _
      _ = _ := by
        congr 1
        rw [← Finset.sum_filter]
        exact Finset.sum_subtype _ (by simp) _
  unfold fourierReadout
  rw [Finset.sum_comm]
  simp only [inner, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  rw [subgroup_character_sum psi faithful]
  split_ifs <;> field_simp
  ring

theorem readout_smul (psi : AddChar F ℂ) (rho : V → V → ℂ) (a : ℂ)
    (l : Module.Dual F V) :
    fourierReadout psi (a • rho) l = a * fourierReadout psi rho l := by
  simp only [fourierReadout, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro x _
  apply Finset.sum_congr rfl
  intro y _
  ring

end Fourier

section CompleteCharacters
variable {F V : Type*} [Field F] [AddCommGroup V] [Module F V]
  [Fintype V] [FiniteDimensional F V] [Fintype (Module.Dual F V)]

theorem dual_card : Fintype.card (Module.Dual F V) = Fintype.card V :=
  (Fintype.card_congr (Module.Free.chooseBasis F V).toDualEquiv.toEquiv).symm

omit [Fintype V] [Fintype (Module.Dual F V)] in
theorem evaluation_character_trivial (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (x : V) : psi.compAddMonoidHom ((Module.Dual.eval F V) x).toAddMonoidHom = 0 ↔ x = 0 := by
  constructor
  · intro he
    apply (Module.forall_dual_apply_eq_zero_iff F x).mp
    intro l
    apply faithful
    have hh := congrArg (fun f : AddChar (Module.Dual F V) ℂ => f l) he
    simpa using hh
  · intro he
    subst x
    ext l
    simp

theorem complete_linear_characters (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (x : V) : (∑ l : Module.Dual F V, psi (l x)) =
      if x = 0 then (Fintype.card V : ℂ) else 0 := by
  have hs := (psi.compAddMonoidHom ((Module.Dual.eval F V) x).toAddMonoidHom).sum_eq_ite
  simpa only [AddChar.compAddMonoidHom_apply, LinearMap.toAddMonoidHom_coe,
    Module.Dual.eval_apply, evaluation_character_trivial psi faithful x, dual_card] using hs

theorem fourier_columns (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (unitary : ∀ z, psi z * star (psi z) = 1) (x y : V) :
    (∑ l : Module.Dual F V, psi (l x) * star (psi (l y))) =
      if x = y then (Fintype.card V : ℂ) else 0 := by
  have hp (l : Module.Dual F V) : psi (l x) * star (psi (l y)) = psi (l (x-y)) := by
    have hh := character_unit_pair psi unitary l (x-y) y
    simpa using hh
  simp_rw [hp]
  rw [complete_linear_characters psi faithful, sub_eq_zero]

theorem readout_complete (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (unitary : ∀ z, psi z * star (psi z) = 1) (rho : V → V → ℂ) :
    (∑ l : Module.Dual F V, fourierReadout psi rho l) = ∑ x, rho x x := by
  have hn : (Fintype.card V : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  have hp (x y : V) : (∑ l : Module.Dual F V, psi (l x) * rho x y * star (psi (l y))) =
      if x = y then (Fintype.card V : ℂ) * rho x y else 0 := by
    calc
      _ = (∑ l : Module.Dual F V, psi (l x) * star (psi (l y))) * rho x y := by
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro l _
        ring
      _ = _ := by rw [fourier_columns psi faithful unitary]; split_ifs <;> ring
  simp only [fourierReadout, ← Finset.mul_sum]
  rw [Finset.sum_comm]
  conv_lhs => arg 2; arg 2; ext x; rw [Finset.sum_comm]
  simp_rw [hp]
  simp
  rw [← Finset.mul_sum]
  field_simp

end CompleteCharacters

section Recovery
variable {F V I : Type*} [Field F] [AddCommGroup V] [Module F V]

def recovered (samples : I → Module.Dual F V) : Submodule F V :=
  (Submodule.span F (Set.range samples)).dualCoannihilator

theorem recovered_membership (samples : I → Module.Dual F V) (x : V) :
    x ∈ recovered samples ↔ ∀ i, samples i x = 0 := by
  rw [recovered, Submodule.mem_dualCoannihilator]
  constructor
  · intro h i
    exact h _ (Submodule.subset_span ⟨i,rfl⟩)
  · intro h l hl
    exact Submodule.span_induction (fun f hf => by obtain ⟨i,rfl⟩ := hf; exact h i)
      (by simp) (fun a b _ _ ha hb => by simp [ha,hb])
      (fun a b _ hb => by simp [hb]) hl

theorem recovery_contains_hidden (H : Submodule F V) (samples : I → Module.Dual F V)
    (legal : ∀ i, samples i ∈ H.dualAnnihilator) : H ≤ recovered samples := by
  intro x hx
  rw [recovered_membership]
  intro i
  exact (Submodule.mem_dualAnnihilator _).mp (legal i) x hx

theorem recovery_exact (H : Submodule F V) (samples : I → Module.Dual F V)
    (spans : Submodule.span F (Set.range samples) = H.dualAnnihilator) :
    recovered samples = H := by
  rw [recovered, spans]
  exact Subspace.dualAnnihilator_dualCoannihilator_eq

theorem recovery_exact_iff [FiniteDimensional F V] (H : Submodule F V)
    (samples : I → Module.Dual F V) : recovered samples = H ↔
      Submodule.span F (Set.range samples) = H.dualAnnihilator := by
  constructor
  · intro he
    have hh := congrArg Submodule.dualAnnihilator he
    simpa only [recovered, Subspace.dualCoannihilator_dualAnnihilator_eq] using hh
  · exact recovery_exact H samples

end Recovery

section PrimeCharacter
variable (p : ℕ) [NeZero p]

theorem standard_character_faithful :
    Function.Injective (ZMod.stdAddChar : AddChar (ZMod p) ℂ) :=
  ZMod.injective_stdAddChar

theorem standard_character_unitary (x : ZMod p) :
    ZMod.stdAddChar x * star (ZMod.stdAddChar x) = 1 := by
  rw [ZMod.stdAddChar_apply]
  change _ * (starRingEnd ℂ) _ = 1
  rw [Complex.mul_conj, Circle.normSq_coe, Complex.ofReal_one]

end PrimeCharacter

section Terminal
open ReesLie LieModule
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] [Group L] [Fintype L] {n : ℕ}
variable (law : PolynomialGroupLaw F L) (points : Fin n → F)
  (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
  (nilpotent : lowerCentralSeries F L L n = ⊥)

theorem terminal_source (h : LieSubalgebra F L) :
    letI := stageFintype points nilpotent 1
    reesSource law points nilpotent h 1 =
      additiveSource (stageHidden points nilpotent 1 h).toSubmodule := by
  let := stageGroup law points nilpotent 1
  let := stageFintype points nilpotent 1
  funext x y
  have hm := commuting_mul_add (stageLaw law points nilpotent 1) (-y) x
    (first_stage_abelian points nilpotent _ _)
  simp only [reesSource, sourceEntry, (stageLaw law points nilpotent 1).inv_eq,
    hm, additiveSource]
  congr 2
  apply propext
  change -y+x ∈ stageHidden points nilpotent 1 h ↔ x-y ∈ stageHidden points nilpotent 1 h
  rw [sub_eq_add_neg, add_comm]

variable {Packets Labels : ℕ → Type*} [∀ k, Fintype (Packets k)] [∀ k, Fintype (Labels k)]

theorem native_terminal_readout (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    (tree : SourceTree Packets (fun _ => Unit) n 1)
    (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (unitary : ∀ z, psi z * star (psi z) = 1)
    (l : Module.Dual F (cover points nilpotent ⧸ tailIdeal points nilpotent 1)) :
    letI := stageFintype points nilpotent 1
    fourierReadout psi
      (evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
        (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ)
        (acquireTop law points distinct nonzero nilpotent (fun _ => sourceEntry (subgroup law h)))
        (fun k _ => reesAverage law points distinct nonzero nilpotent k (plans k)) tree) l =
      if l ∈ (stageHidden points nilpotent 1 h).toSubmodule.dualAnnihilator
        then (Fintype.card (stageHidden points nilpotent 1 h) : ℂ) /
          Fintype.card (cover points nilpotent ⧸ tailIdeal points nilpotent 1) else 0 := by
  let := stageFintype points nilpotent 1
  rw [native_average_tree, terminal_source]
  exact fourier_source psi faithful unitary _ l

theorem native_record_readout (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    (tree : SourceTree Packets (fun k => Packets k → Labels k) n 1)
    (psi : AddChar F ℂ) (faithful : Function.Injective psi)
    (unitary : ∀ z, psi z * star (psi z) = 1)
    (l : Module.Dual F (cover points nilpotent ⧸ tailIdeal points nilpotent 1)) :
    letI := stageFintype points nilpotent 1
    fourierReadout psi
      (evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
        (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ)
        (acquireTop law points distinct nonzero nilpotent (fun _ => sourceEntry (subgroup law h)))
        (fun k => reesRecord law points distinct nonzero nilpotent k (plans k)) tree) l =
      treeWeight (fun k => reesMass law points distinct nonzero nilpotent h k (plans k)) tree *
        (if l ∈ (stageHidden points nilpotent 1 h).toSubmodule.dualAnnihilator
          then (Fintype.card (stageHidden points nilpotent 1 h) : ℂ) /
            Fintype.card (cover points nilpotent ⧸ tailIdeal points nilpotent 1) else 0) := by
  let := stageFintype points nilpotent 1
  rw [native_record_tree, readout_smul, terminal_source]
  rw [fourier_source psi faithful unitary]
  rfl

include distinct nonzero in
omit [Group L] [Fintype L] [∀ k, Fintype (Packets k)] [∀ k, Fintype (Labels k)] in
theorem native_hidden_recovery {I : Type*} (h : LieSubalgebra F L) (positive : 0 < n)
    (samples : I → Module.Dual F (cover points nilpotent ⧸ tailIdeal points nilpotent 1))
    (spans : Submodule.span F (Set.range samples) =
      (stageHidden points nilpotent 1 h).toSubmodule.dualAnnihilator) (v : L) :
    quotientProjection points nilpotent 1 (gradeOne points nilpotent positive v) ∈
      recovered samples ↔ v ∈ h := by
  rw [recovery_exact _ samples spans]
  exact first_stage_recovers_all_h points distinct nonzero nilpotent positive h v

end Terminal

end
end QSearch.ReesTerminalRecovery
