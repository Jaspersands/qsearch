import Mathlib.Algebra.Lie.Loop
import Mathlib.Algebra.Lie.Nilpotent
import Lean.Elab.Tactic.Omega

/-!
# The positive lower-central Rees Lie algebra

The ambient algebra is the ordinary current Lie algebra
`AddMonoidAlgebra R ℕ ⊗[R] L`, not a truncated polynomial quotient.
The positive Rees subalgebra is spanned by `t^r x` for `0 < r` and
`x ∈ lowerCentralSeries R L L (r - 1)`.

Only a commutative coefficient ring and a Lie algebra are needed for closure,
evaluation and grade scaling. The cutoff uses the explicit class bound
`lowerCentralSeries R L L c = ⊥`, i.e. `gamma (c + 1) = ⊥`.
The same premise gives `rees_class_bound`. Unit scales give the Lie
automorphisms `dilation`; nonzero scalars need not be units over a ring.
No positive grading, finite dimension, freeness, characteristic restriction,
or exact nilpotence class of the original algebra is assumed.

`mem_rees_iff` identifies the span with positive lower-central coefficients;
`evaluation_formula` gives the actual finite coefficient sum. `gradeOne` is
only a linear embedding, with `evaluation 1` as its left inverse, not a Lie
embedding: the bracket of two degree-one currents has degree two.

This file does not construct BCH groups, prove Lazard functoriality, connect
the Lie maps to the group interface in `ReesHomogenization`, or verify the
quantum algorithm or its resource bounds.
-/

namespace QSearch.ReesLieConstruction

open scoped TensorProduct
open LieModule

noncomputable section

set_option backward.isDefEq.respectTransparency false

variable {R L : Type*} [CommRing R] [LieRing L] [LieAlgebra R L]

/-- The manuscript's indexing: `gamma 1 = L`. Only positive indices are used. -/
def gamma (R L : Type*) [CommRing R] [LieRing L] [LieAlgebra R L]
    (r : ℕ) : LieIdeal R L :=
  lowerCentralSeries R L L (r - 1)

private theorem lcs_bracket (i j : ℕ) :
    ⁅lowerCentralSeries R L L i, lowerCentralSeries R L L j⁆ ≤
      lowerCentralSeries R L L (i + j + 1) := by
  induction i generalizing j with
  | zero => simp [lowerCentralSeries_zero, lowerCentralSeries_succ]
  | succ i ih =>
    apply (LieSubmodule.lie_le_iff _ _ _).mpr
    intro x hx y hy
    rw [lowerCentralSeries_succ] at hx
    change x ∈ (⁅(⊤ : LieIdeal R L), lowerCentralSeries R L L i⁆).toSubmodule at hx
    rw [LieSubmodule.lieIdeal_oper_eq_linear_span'] at hx
    induction hx using Submodule.span_induction with
    | mem z hz =>
      obtain ⟨a, _, b, hb, rfl⟩ := hz
      rw [lie_lie]
      apply (lowerCentralSeries R L L (i + 1 + j + 1)).sub_mem
      · have h := LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a)
          (ih j (LieSubmodule.lie_mem_lie hb hy))
        simpa [← lowerCentralSeries_succ, Nat.add_assoc, Nat.add_comm,
          Nat.add_left_comm] using h
      · have h : ⁅a, y⁆ ∈ lowerCentralSeries R L L (j + 1) := by
          rw [lowerCentralSeries_succ]
          exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a) hy
        simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
          ih (j + 1) (LieSubmodule.lie_mem_lie hb h)
    | zero => simp
    | add a b _ _ ha hb =>
      rw [add_lie]
      exact (lowerCentralSeries R L L (i + 1 + j + 1)).add_mem ha hb
    | smul a b _ hb =>
      rw [smul_lie]
      exact (lowerCentralSeries R L L (i + 1 + j + 1)).smul_mem a hb

/-- Untruncated lower-central closure, proved from Jacobi and the actual series. -/
theorem gamma_bracket_le {r s : ℕ} (hr : 0 < r) (hs : 0 < s) :
    ⁅gamma R L r, gamma R L s⁆ ≤ gamma R L (r + s) := by
  simpa only [gamma, show r - 1 + (s - 1) + 1 = r + s - 1 by omega] using
    (lcs_bracket (R := R) (L := L) (r - 1) (s - 1))

/-- Ordinary polynomial currents, with Mathlib's tensor-product Lie bracket. -/
abbrev Current (R L : Type*) [CommRing R] [LieRing L] [LieAlgebra R L] :=
  LieAlgebra.loopAlgebra R ℕ L

/-- The actual homogeneous polynomial current `t^r x`. -/
def monomial (r : ℕ) (x : L) : Current R L :=
  AddMonoidAlgebra.single r 1 ⊗ₜ[R] x

@[simp] theorem monomial_lie (r s : ℕ) (x y : L) :
    ⁅monomial (R := R) r x, monomial (R := R) s y⁆ =
      monomial (R := R) (r + s) ⁅x, y⁆ := by
  simp [monomial]

private def generators : Set (Current R L) :=
  {z | ∃ (r : ℕ) (x : L), 0 < r ∧ x ∈ gamma R L r ∧ z = monomial r x}

private def reesModule : Submodule R (Current R L) :=
  Submodule.span R (generators (R := R) (L := L))

/-- The positive Rees algebra inside the ordinary current Lie algebra. -/
def rees : LieSubalgebra R (Current R L) :=
  { reesModule (R := R) (L := L) with
    lie_mem' := by
      intro x y hx hy
      change ⁅x, y⁆ ∈ reesModule (R := R) (L := L)
      induction hx, hy using Submodule.span_induction₂ with
      | mem_mem x y hx hy =>
        obtain ⟨r, a, hr, ha, rfl⟩ := hx
        obtain ⟨s, b, hs, hb, rfl⟩ := hy
        rw [monomial_lie]
        exact Submodule.subset_span ⟨r + s, ⁅a, b⁆, by omega,
          gamma_bracket_le hr hs (LieSubmodule.lie_mem_lie ha hb), rfl⟩
      | zero_left y hy => rw [zero_lie y]; exact Submodule.zero_mem _
      | zero_right x hx => rw [lie_zero x]; exact Submodule.zero_mem _
      | add_left x y z _ _ _ hx hy =>
        rw [add_lie x y z]
        exact (reesModule (R := R) (L := L)).add_mem hx hy
      | add_right x y z _ _ _ hx hy =>
        rw [lie_add x y z]
        exact (reesModule (R := R) (L := L)).add_mem hx hy
      | smul_left a x y _ _ h =>
        rw [smul_lie a x y]
        exact (reesModule (R := R) (L := L)).smul_mem a h
      | smul_right a x y _ _ h =>
        rw [lie_smul a x y]
        exact (reesModule (R := R) (L := L)).smul_mem a h }

theorem monomial_mem {r : ℕ} {x : L} (hr : 0 < r) (hx : x ∈ gamma R L r) :
    monomial r x ∈ rees (R := R) (L := L) :=
  Submodule.subset_span ⟨r, x, hr, hx, rfl⟩

/-- Polynomial coefficients, using Mathlib's linear equivalence, not an oracle. -/
abbrev coeff : Current R L ≃ₗ[R] (ℕ →₀ L) :=
  LieAlgebra.LoopAlgebra.toFinsupp R ℕ L

@[simp] theorem coeff_monomial (r : ℕ) (x : L) :
    coeff (monomial (R := R) r x) = Finsupp.single r x := by
  simp [coeff, monomial]

private theorem current_induction {P : Current R L → Prop} (z : Current R L)
    (zero : P 0) (add : ∀ x y, P x → P y → P (x + y))
    (single : ∀ r x, P (monomial r x)) : P z := by
  obtain ⟨f, rfl⟩ := (coeff (R := R) (L := L)).symm.surjective z
  induction f using Finsupp.induction_linear with
  | zero => simpa using zero
  | add f g hf hg => simpa using add _ _ hf hg
  | single r x => simpa [coeff, monomial] using single r x

private theorem sum_monomial_coeff (z : Current R L) :
    (coeff z).sum (monomial (R := R)) = z := by
  apply (coeff (R := R) (L := L)).injective
  simpa only [Finsupp.sum, map_sum, coeff_monomial] using (coeff z).sum_single

/-- Exactly the positive lower-central coefficients, with no extra currents in the span. -/
theorem mem_rees_iff (z : Current R L) :
    z ∈ rees (R := R) (L := L) ↔
      coeff z 0 = 0 ∧ ∀ r, coeff z r ∈ gamma R L r := by
  constructor
  · intro hz
    change z ∈ Submodule.span R (generators (R := R) (L := L)) at hz
    induction hz using Submodule.span_induction with
    | mem z hz =>
      obtain ⟨r, x, hr, hx, rfl⟩ := hz
      rw [coeff_monomial]
      constructor
      · exact Finsupp.single_eq_of_ne (by omega)
      · intro s
        by_cases h : r = s
        · subst s; simpa using hx
        · rw [Finsupp.single_eq_of_ne (Ne.symm h)]
          exact (gamma R L s).zero_mem
    | zero => simp
    | add x y _ _ hx hy =>
      constructor
      · simp [hx.1, hy.1]
      · intro r
        rw [map_add, Finsupp.add_apply]
        exact (gamma R L r).add_mem (hx.2 r) (hy.2 r)
    | smul a x _ hx =>
      constructor
      · simp [hx.1]
      · intro r
        rw [map_smul, Finsupp.smul_apply]
        exact (gamma R L r).smul_mem a (hx.2 r)
  · rintro ⟨h0, h⟩
    rw [← sum_monomial_coeff z]
    apply (rees (R := R) (L := L)).toSubmodule.sum_mem
    intro r _
    by_cases hr : r = 0
    · subst r; simp [h0, monomial]
    · exact monomial_mem (Nat.pos_of_ne_zero hr) (h r)

/-- Above a stated nilpotence bound, coefficients and homogeneous brackets are
actually zero in the untruncated current algebra. -/
theorem nilpotent_cutoff (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥) :
    (∀ z ∈ rees (R := R) (L := L), ∀ r, c < r → coeff z r = 0) ∧
    (∀ r s, 0 < r → 0 < s → c < r + s →
      ∀ x ∈ gamma R L r, ∀ y ∈ gamma R L s,
        ⁅monomial (R := R) r x, monomial (R := R) s y⁆ = 0) := by
  have vanish {r : ℕ} (hr : c < r) {x : L} (hx : x ∈ gamma R L r) : x = 0 := by
    have h := antitone_lowerCentralSeries R L L (show c ≤ r - 1 by omega) hx
    simpa only [hnil, LieSubmodule.mem_bot] using h
  constructor
  · intro z hz r hr
    exact vanish hr ((mem_rees_iff z).mp hz |>.2 r)
  · intro r s hr hs hrs x hx y hy
    rw [monomial_lie, vanish hrs (gamma_bracket_le hr hs
      (LieSubmodule.lie_mem_lie hx hy))]
    simp [monomial]

private def evalLinear (a : R) : Current R L →ₗ[R] L :=
  (Finsupp.lsum R (fun r : ℕ => a ^ r • (LinearMap.id : L →ₗ[R] L))).comp
    (coeff (R := R) (L := L)).toLinearMap

@[simp] private theorem evalLinear_monomial (a : R) (r : ℕ) (x : L) :
    evalLinear a (monomial r x) = a ^ r • x := by
  simp [evalLinear]

/-- Evaluation of the ordinary current algebra; bracket preservation is proved
from the monomial bracket, bilinearity and `a^(r+s) = a^r * a^s`. -/
def currentEval (a : R) : Current R L →ₗ⁅R⁆ L :=
  { evalLinear a with
    map_lie' := by
      intro x y
      change evalLinear a ⁅x, y⁆ = ⁅evalLinear a x, evalLinear a y⁆
      induction x using current_induction with
      | zero => simp [zero_lie y]
      | add x z hx hz => simp only [add_lie x z y, map_add, hx, hz, add_lie]
      | single r x =>
        induction y using current_induction with
        | zero => simp [lie_zero (monomial (R := R) r x)]
        | add y z hy hz =>
          simp only [lie_add (monomial (R := R) r x) y z, map_add, hy, hz, lie_add]
        | single s y => simp [pow_add, smul_lie, lie_smul, smul_smul, mul_comm] }

/-- Actual evaluation restricted to the concrete Rees Lie subalgebra. -/
def evaluation (a : R) : rees (R := R) (L := L) →ₗ⁅R⁆ L :=
  (currentEval a).comp (rees (R := R) (L := L)).incl

/-- The coefficient formula required on the Lie side of the interpolation interface. -/
theorem evaluation_formula (a : R) (z : rees (R := R) (L := L)) :
    evaluation a z = (coeff (z : Current R L)).sum (fun r x => a ^ r • x) := rfl

/-- Grade one contains all of `L`, including its derived directions.
This is a linear map, not a claimed Lie homomorphism. -/
def gradeOne : L →ₗ[R] rees (R := R) (L := L) :=
  LinearMap.codRestrict (rees (R := R) (L := L)).toSubmodule
    (TensorProduct.mk R (AddMonoidAlgebra R ℕ) L (AddMonoidAlgebra.single 1 1))
    (fun x => monomial_mem (by decide) (by simp [gamma, lowerCentralSeries_zero]))

/-- Evaluation at one is a left inverse, so grade one retains `L` injectively,
not merely the abelianization `L / [L,L]`. -/
theorem grade_one_retention :
    Function.LeftInverse (evaluation (R := R) (L := L) 1) (gradeOne (R := R) (L := L)) := by
  intro x
  change evalLinear 1 (monomial 1 x) = x
  simp

private def scaleLinear (a : R) : Current R L →ₗ[R] Current R L :=
  (coeff (R := R) (L := L)).symm.toLinearMap.comp
    ((Finsupp.lsum R (fun r : ℕ => a ^ r • (Finsupp.lsingle r : L →ₗ[R] ℕ →₀ L))).comp
      (coeff (R := R) (L := L)).toLinearMap)

@[simp] private theorem scaleLinear_monomial (a : R) (r : ℕ) (x : L) :
    scaleLinear a (monomial r x) = a ^ r • monomial r x := by
  simp [scaleLinear, coeff, monomial]

/-- Substitution `t ↦ a*t` in the ordinary current algebra. -/
def currentScale (a : R) : Current R L →ₗ⁅R⁆ Current R L :=
  { scaleLinear a with
    map_lie' := by
      intro x y
      change scaleLinear a ⁅x, y⁆ = ⁅scaleLinear a x, scaleLinear a y⁆
      induction x using current_induction with
      | zero => simp only [zero_lie y, map_zero, zero_lie (scaleLinear a y)]
      | add x z hx hz =>
        simp only [add_lie x z y, map_add, hx, hz,
          add_lie (scaleLinear a x) (scaleLinear a z) (scaleLinear a y)]
      | single r x =>
        induction y using current_induction with
        | zero =>
          simp only [lie_zero (monomial (R := R) r x), map_zero,
            lie_zero (scaleLinear a (monomial (R := R) r x))]
        | add y z hy hz =>
          simp only [lie_add (monomial (R := R) r x) y z, map_add, hy, hz,
            lie_add (scaleLinear a (monomial (R := R) r x)) (scaleLinear a y) (scaleLinear a z)]
        | single s y =>
          rw [monomial_lie, scaleLinear_monomial, scaleLinear_monomial, scaleLinear_monomial,
            smul_lie (a ^ r) (monomial (R := R) r x) (a ^ s • monomial (R := R) s y),
            lie_smul (a ^ s) (monomial (R := R) r x) (monomial (R := R) s y),
            monomial_lie, smul_smul, pow_add] }

@[simp] theorem coeff_currentScale (a : R) (z : Current R L) (r : ℕ) :
    coeff (currentScale a z) r = a ^ r • coeff z r := by
  induction z using current_induction with
  | zero => simp
  | add x y hx hy => simp [hx, hy, smul_add]
  | single s x =>
    change coeff (scaleLinear a (monomial s x)) r = _
    rw [scaleLinear_monomial, map_smul, Finsupp.smul_apply, coeff_monomial]
    by_cases h : r = s
    · subst r; rfl
    · simp [Finsupp.single_eq_of_ne h]

/-- Every scalar gives an actual Lie endomorphism of the positive Rees algebra. -/
def scaling (a : R) : rees (R := R) (L := L) →ₗ⁅R⁆ rees (R := R) (L := L) where
  toFun z := ⟨currentScale a z, (mem_rees_iff _).mpr ⟨by
    rw [coeff_currentScale, (mem_rees_iff _).mp z.property |>.1, smul_zero],
    fun r => by
      rw [coeff_currentScale]
      exact (gamma R L r).smul_mem _ ((mem_rees_iff _).mp z.property |>.2 r)⟩⟩
  map_add' x y := Subtype.ext (map_add (currentScale a) (x : Current R L) y)
  map_smul' b x := Subtype.ext (map_smul (currentScale a) b (x : Current R L))
  map_lie' {x y} := Subtype.ext ((currentScale a).map_lie (x : Current R L) y)

/-- The grade-r coefficient is multiplied by exactly `a^r`. -/
theorem scaling_coeff (a : R) (z : rees (R := R) (L := L)) (r : ℕ) :
    coeff (scaling a z : Current R L) r = a ^ r • coeff (z : Current R L) r := by
  change coeff (currentScale a (z : Current R L)) r = _
  exact coeff_currentScale a (z : Current R L) r

private theorem scaling_mul (a b : R) (z : rees (R := R) (L := L)) :
    scaling a (scaling b z) = scaling (a * b) z := by
  apply Subtype.ext
  apply (coeff (R := R) (L := L)).injective
  ext r
  simp only [scaling_coeff, mul_pow, mul_smul]

private theorem scaling_one (z : rees (R := R) (L := L)) : scaling (1 : R) z = z := by
  apply Subtype.ext
  apply (coeff (R := R) (L := L)).injective
  ext r
  simp [scaling_coeff]

set_option maxRecDepth 2048 in
/-- Unit scales give Lie automorphisms over a general commutative ring.
Over a field this applies to every nonzero scale; nonzero alone is not
sufficient over a general ring. -/
def dilation (u : Rˣ) : rees (R := R) (L := L) ≃ₗ⁅R⁆ rees (R := R) (L := L) :=
  { scaling (u : R) with
    invFun := scaling (↑u⁻¹ : R)
    left_inv := fun z => by
      change scaling (↑u⁻¹ : R) (scaling (u : R) z) = z
      rw [scaling_mul]
      simpa using scaling_one z
    right_inv := fun z => by
      change scaling (u : R) (scaling (↑u⁻¹ : R) z) = z
      rw [scaling_mul]
      simpa using scaling_one z }

/-- The Rees algebra has nilpotence class at most the given bound for `L`. -/
theorem rees_class_bound (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥) :
    lowerCentralSeries R (rees (R := R) (L := L)) (rees (R := R) (L := L)) c = ⊥ := by
  have hb : lowerCentralSeries (AddMonoidAlgebra R ℕ) (Current R L) (Current R L) c = ⊥ := by
    rw [LieSubmodule.lowerCentralSeries_tensor_eq_baseChange, hnil, LieSubmodule.baseChange_bot]
  have hc : lowerCentralSeries R (Current R L) (Current R L) c = ⊥ := by
    rw [SetLike.ext'_iff] at hb ⊢
    rw [coe_lowerCentralSeries_eq_int R,
      ← coe_lowerCentralSeries_eq_int (AddMonoidAlgebra R ℕ)]
    exact hb
  apply LieIdeal.bot_of_map_eq_bot (f := (rees (R := R) (L := L)).incl) Subtype.val_injective
  rw [eq_bot_iff, ← hc]
  exact LieIdeal.map_lowerCentralSeries_le c

end
end QSearch.ReesLieConstruction

/-- info: 'QSearch.ReesLieConstruction.gamma_bracket_le' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.gamma_bracket_le

/-- info: 'QSearch.ReesLieConstruction.rees' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.rees

/-- info: 'QSearch.ReesLieConstruction.mem_rees_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.mem_rees_iff

/-- info: 'QSearch.ReesLieConstruction.nilpotent_cutoff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.nilpotent_cutoff

/-- info: 'QSearch.ReesLieConstruction.currentEval' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.currentEval

/-- info: 'QSearch.ReesLieConstruction.evaluation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.evaluation

/-- info: 'QSearch.ReesLieConstruction.evaluation_formula' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.evaluation_formula

/-- info: 'QSearch.ReesLieConstruction.grade_one_retention' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.grade_one_retention

/-- info: 'QSearch.ReesLieConstruction.currentScale' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.currentScale

/-- info: 'QSearch.ReesLieConstruction.scaling_coeff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.scaling_coeff

/-- info: 'QSearch.ReesLieConstruction.dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.dilation

/-- info: 'QSearch.ReesLieConstruction.rees_class_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesLieConstruction.rees_class_bound
