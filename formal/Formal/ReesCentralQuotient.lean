import Formal.ReesLieConstruction
import Mathlib.Algebra.Lie.Quotient
import Mathlib.Tactic

/-!
# Actual positive-grade central quotients of the Rees Lie algebra

`tail d` is the ideal of actual currents whose coefficients through degree `d`
vanish. `Trunc d` is the Mathlib Lie quotient by this ideal, not a supplied
coordinate carrier. Positivity proves the class bound and centrality of each
successive kernel. No nilpotence premise on the original Lie algebra is needed
for these truncated quotients.
-/

namespace QSearch.ReesCentralQuotient

open LieModule QSearch.ReesLieConstruction

noncomputable section

set_option backward.isDefEq.respectTransparency false

variable {R L : Type*} [CommRing R] [LieRing L] [LieAlgebra R L]

abbrev Algebra (R L : Type*) [CommRing R] [LieRing L] [LieAlgebra R L] :=
  rees (R := R) (L := L)

/-- Coefficient extraction on the actual Rees subalgebra. -/
def coefficient (r : ℕ) : Algebra R L →ₗ[R] L :=
  (Finsupp.lapply r).comp
    ((coeff (R := R) (L := L)).toLinearMap.comp (rees (R := R) (L := L)).incl.toLinearMap)

theorem coefficient_apply (r : ℕ) (x : Algebra R L) :
    coefficient r x = coeff (x : Current R L) r := rfl

@[simp] theorem coefficient_zero (x : Algebra R L) : coefficient 0 x = 0 :=
  (mem_rees_iff _).mp x.property |>.1

private theorem current_sum (x : Current R L) :
    (coeff x).sum (monomial (R := R)) = x := by
  apply (coeff (R := R) (L := L)).injective
  simpa only [Finsupp.sum, map_sum, coeff_monomial] using (coeff x).sum_single

/-- Positive degrees add in the actual current bracket. -/
theorem bracket_vanishes (i j : ℕ) (x y : Current R L)
    (hx : ∀ r ≤ i, coeff x r = 0) (hy : ∀ r ≤ j, coeff y r = 0) :
    ∀ r ≤ i + j + 1, coeff ⁅x, y⁆ r = 0 := by
  classical
  intro k hk
  conv_lhs => rw [← current_sum x, ← current_sum y]
  simp only [Finsupp.sum]
  rw [sum_lie_sum (coeff x).support (coeff y).support]
  simp only [map_sum, Finsupp.finsetSum_apply, monomial_lie, coeff_monomial]
  apply Finset.sum_eq_zero
  intro r hr
  apply Finset.sum_eq_zero
  intro s hs
  have hir : i < r := by
    by_contra h
    exact (Finsupp.mem_support_iff.mp hr) (hx r (by omega))
  have hjs : j < s := by
    by_contra h
    exact (Finsupp.mem_support_iff.mp hs) (hy s (by omega))
  exact Finsupp.single_eq_of_ne (by omega)

/-- The actual positive-grade ideal `F_{>d}`. -/
def tail (d : ℕ) : LieIdeal R (Algebra R L) where
  carrier := {x | ∀ r ≤ d, coefficient r x = 0}
  zero_mem' := by simp
  add_mem' := by
    intro x y hx hy r hr
    simp only [map_add, hx r hr, hy r hr, add_zero]
  smul_mem' := by
    intro a x hx r hr
    simp only [map_smul, hx r hr, smul_zero]
  lie_mem := by
    intro x y hy r hr
    exact bracket_vanishes 0 d (x : Current R L) y
      (fun s hs => by
        have : s = 0 := by omega
        subst s
        exact coefficient_zero x)
      hy r (by omega)

@[simp] theorem mem_tail (d : ℕ) (x : Algebra R L) :
    x ∈ tail d ↔ ∀ r ≤ d, coefficient r x = 0 := Iff.rfl

theorem tail_antitone {d e : ℕ} (h : e ≤ d) :
    tail (R := R) (L := L) d ≤ tail e :=
  fun _ hx r hr => hx r (hr.trans h)

/-- Bracketing with any positive current raises the cutoff by one. -/
theorem bracket_mem_tail (d : ℕ) (x y : Algebra R L) (hy : y ∈ tail d) :
    ⁅x, y⁆ ∈ tail (d + 1) := by
  intro r hr
  exact bracket_vanishes 0 d (x : Current R L) y
    (fun s hs => by
      have : s = 0 := by omega
      subst s
      exact coefficient_zero x)
    hy r (by omega)

theorem lowerCentralSeries_le_tail (d : ℕ) :
    lowerCentralSeries R (Algebra R L) (Algebra R L) d ≤ tail d := by
  induction d with
  | zero =>
    intro x _ r hr
    have : r = 0 := by omega
    subst r
    exact coefficient_zero x
  | succ d ih =>
    rw [lowerCentralSeries_succ]
    apply (LieSubmodule.lie_le_iff _ _ _).mpr
    intro x _ y hy
    exact bracket_mem_tail d x y (ih hy)

/-- The actual Lie quotient `A / F_{>d}`. -/
abbrev Trunc (d : ℕ) := Algebra R L ⧸ tail (R := R) (L := L) d

/-- Canonical quotient map, with the quotient Lie bracket. -/
def mk (d : ℕ) : Algebra R L →ₗ⁅R⁆ Trunc (R := R) (L := L) d :=
  { (tail (R := R) (L := L) d).toSubmodule.mkQ with
    map_lie' := by intro x y; rfl }

theorem mk_surjective (d : ℕ) : Function.Surjective (mk (R := R) (L := L) d) :=
  Submodule.mkQ_surjective _

@[simp] theorem mk_eq_zero (d : ℕ) (x : Algebra R L) :
    mk d x = 0 ↔ x ∈ tail d :=
  Submodule.Quotient.mk_eq_zero _

@[simp] theorem ker_mk (d : ℕ) : (mk (R := R) (L := L) d).ker = tail d := by
  ext x
  exact mk_eq_zero d x

/-- The degree cutoff itself proves nilpotence, even for nonnilpotent `L`. -/
theorem trunc_class_bound (d : ℕ) :
    lowerCentralSeries R (Trunc (R := R) (L := L) d) (Trunc (R := R) (L := L) d) d = ⊥ := by
  rw [← LieIdeal.lowerCentralSeries_map_eq d (mk_surjective d),
    LieIdeal.map_eq_bot_iff, ker_mk]
  exact lowerCentralSeries_le_tail d

/-- A local universal property for the actual Lie quotient. -/
def lift {M : Type*} [LieRing M] [LieAlgebra R M] (d : ℕ)
    (f : Algebra R L →ₗ⁅R⁆ M) (hf : tail d ≤ f.ker) :
    Trunc (R := R) (L := L) d →ₗ⁅R⁆ M :=
  { (tail (R := R) (L := L) d).toSubmodule.liftQ f.toLinearMap hf with
    map_lie' := by
      intro x y
      obtain ⟨x, rfl⟩ := mk_surjective d x
      obtain ⟨y, rfl⟩ := mk_surjective d y
      exact f.map_lie x y }

@[simp] theorem lift_mk {M : Type*} [LieRing M] [LieAlgebra R M] (d : ℕ)
    (f : Algebra R L →ₗ⁅R⁆ M) (hf : tail d ≤ f.ker) (x : Algebra R L) :
    lift d f hf (mk d x) = f x := rfl

/-- Canonical transition between actual quotients. -/
def projection {d e : ℕ} (h : e ≤ d) :
    Trunc (R := R) (L := L) d →ₗ⁅R⁆ Trunc (R := R) (L := L) e :=
  lift d (mk e) (by rw [ker_mk]; exact tail_antitone h)

@[simp] theorem projection_mk {d e : ℕ} (h : e ≤ d) (x : Algebra R L) :
    projection h (mk d x) = mk e x := rfl

theorem projection_surjective {d e : ℕ} (h : e ≤ d) :
    Function.Surjective (projection (R := R) (L := L) h) := by
  intro x
  obtain ⟨y, rfl⟩ := mk_surjective e x
  exact ⟨mk d y, rfl⟩

theorem projection_comp {d e f : ℕ} (he : e ≤ d) (hf : f ≤ e) :
    (projection (R := R) (L := L) hf).comp (projection he) = projection (hf.trans he) := by
  ext x
  obtain ⟨y, rfl⟩ := mk_surjective d x
  rfl

/-- The kernel is precisely the top-grade layer; its bracket with everything is zero. -/
theorem top_kernel_central (d : ℕ) (x y : Trunc (R := R) (L := L) (d + 1))
    (hy : projection (Nat.le_succ d) y = 0) : ⁅x, y⁆ = 0 := by
  obtain ⟨a, rfl⟩ := mk_surjective (d + 1) x
  obtain ⟨b, rfl⟩ := mk_surjective (d + 1) y
  rw [projection_mk, mk_eq_zero] at hy
  rw [← LieHom.map_lie, mk_eq_zero]
  exact bracket_mem_tail d a b hy

/-- Retained coefficients descend to the actual quotient. -/
def quotientCoefficient (d r : ℕ) (hr : r ≤ d) :
    Trunc (R := R) (L := L) d →ₗ[R] L :=
  (tail (R := R) (L := L) d).toSubmodule.liftQ (coefficient r)
    (fun _ hx => hx r hr)

@[simp] theorem quotientCoefficient_mk (d r : ℕ) (hr : r ≤ d) (x : Algebra R L) :
    quotientCoefficient d r hr (mk d x) = coefficient r x := rfl

theorem mk_eq_mk_iff (d : ℕ) (x y : Algebra R L) :
    mk d x = mk d y ↔ ∀ r ≤ d, coefficient r x = coefficient r y := by
  rw [← sub_eq_zero, ← map_sub, mk_eq_zero, mem_tail]
  simp only [map_sub, sub_eq_zero]

/-- Equality of retained coefficients is proved to be equality in the quotient. -/
theorem trunc_ext (d : ℕ) (x y : Trunc (R := R) (L := L) d)
    (h : ∀ r (hr : r ≤ d), quotientCoefficient d r hr x = quotientCoefficient d r hr y) :
    x = y := by
  obtain ⟨a, rfl⟩ := mk_surjective d x
  obtain ⟨b, rfl⟩ := mk_surjective d y
  exact (mk_eq_mk_iff d a b).mpr h

/-- Finite coordinates for the actual quotient, including its identically zero degree zero. -/
def finiteCoefficients (d : ℕ) (x : Trunc (R := R) (L := L) d) : Fin (d + 1) → L :=
  fun r => quotientCoefficient d r.val (by omega) x

theorem finiteCoefficients_injective (d : ℕ) :
    Function.Injective (finiteCoefficients (R := R) (L := L) d) := by
  intro x y h
  apply trunc_ext d x y
  intro r hr
  exact congrFun h ⟨r, by omega⟩

/-- No finiteness of the infinite polynomial-current ambient is assumed. -/
instance finiteTrunc (d : ℕ) [Finite L] : Finite (Trunc (R := R) (L := L) d) :=
  Finite.of_injective (finiteCoefficients d) (finiteCoefficients_injective d)

@[simp] theorem coefficient_scaling (a : R) (x : Algebra R L) (r : ℕ) :
    coefficient r (scaling a x) = a ^ r • coefficient r x :=
  scaling_coeff a x r

/-- Scalar substitution descends because it preserves the actual tail ideal. -/
def quotientScaling (d : ℕ) (a : R) :
    Trunc (R := R) (L := L) d →ₗ⁅R⁆ Trunc (R := R) (L := L) d :=
  lift d ((mk d).comp (scaling a)) (by
    intro x hx
    change mk d (scaling a x) = 0
    rw [mk_eq_zero]
    intro r hr
    simp only [coefficient_scaling, hx r hr, smul_zero])

@[simp] theorem quotientScaling_mk (d : ℕ) (a : R) (x : Algebra R L) :
    quotientScaling d a (mk d x) = mk d (scaling a x) := rfl

theorem quotientScaling_coeff (d : ℕ) (a : R) (x : Trunc (R := R) (L := L) d)
    (r : ℕ) (hr : r ≤ d) :
    quotientCoefficient d r hr (quotientScaling d a x) =
      a ^ r • quotientCoefficient d r hr x := by
  obtain ⟨x, rfl⟩ := mk_surjective d x
  exact coefficient_scaling a x r

set_option maxRecDepth 2048 in
/-- Unit substitutions are automorphisms of the quotient, with proved inverse. -/
def quotientDilation (d : ℕ) (u : Rˣ) :
    Trunc (R := R) (L := L) d ≃ₗ⁅R⁆ Trunc (R := R) (L := L) d :=
  { quotientScaling d (u : R) with
    invFun := quotientScaling d (↑u⁻¹ : R)
    left_inv := by
      intro x
      obtain ⟨x, rfl⟩ := mk_surjective d x
      change mk d ((dilation u).symm (dilation u x)) = mk d x
      rw [LieEquiv.symm_apply_apply]
    right_inv := by
      intro x
      obtain ⟨x, rfl⟩ := mk_surjective d x
      change mk d (dilation u ((dilation u).symm x)) = mk d x
      rw [LieEquiv.apply_symm_apply] }

@[simp] theorem quotientDilation_mk (d : ℕ) (u : Rˣ) (x : Algebra R L) :
    quotientDilation d u (mk d x) = mk d (dilation u x) := rfl

theorem projection_dilation {d e : ℕ} (h : e ≤ d) (u : Rˣ)
    (x : Trunc (R := R) (L := L) d) :
    projection h (quotientDilation d u x) = quotientDilation e u (projection h x) := by
  obtain ⟨x, rfl⟩ := mk_surjective d x
  rfl

/-- On the actual top kernel, substitution is exactly weight `d+1`. -/
theorem top_kernel_scaling (d : ℕ) (a : R) (x : Trunc (R := R) (L := L) (d + 1))
    (hx : projection (Nat.le_succ d) x = 0) :
    quotientScaling (d + 1) a x = a ^ (d + 1) • x := by
  obtain ⟨x, rfl⟩ := mk_surjective (d + 1) x
  rw [projection_mk, mk_eq_zero] at hx
  rw [quotientScaling_mk, ← map_smul]
  apply (mk_eq_mk_iff (d + 1) _ _).mpr
  intro r hr
  rw [coefficient_scaling, map_smul]
  by_cases h : r = d + 1
  · rw [h]
  · rw [hx r (by omega), smul_zero, smul_zero]

theorem top_kernel_dilation (d : ℕ) (u : Rˣ)
    (x : Trunc (R := R) (L := L) (d + 1))
    (hx : projection (Nat.le_succ d) x = 0) :
    quotientDilation (d + 1) u x = (u : R) ^ (d + 1) • x :=
  top_kernel_scaling d (u : R) x hx

/-- At an actual nilpotence bound, truncation discards no Rees current. -/
theorem tail_eq_bot (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥) :
    tail (R := R) (L := L) c = ⊥ := by
  apply eq_bot_iff.mpr
  intro x hx
  change x = 0
  apply Subtype.ext
  apply (coeff (R := R) (L := L)).injective
  ext r
  change coeff (x : Current R L) r = coeff (0 : Current R L) r
  rw [map_zero, Finsupp.zero_apply]
  by_cases hr : r ≤ c
  · exact hx r hr
  · exact (nilpotent_cutoff c hnil).1 x x.property r (by omega)

/-- This is the proved bridge from the original Rees algebra to its full truncation. -/
def fullEquiv (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥) :
    Algebra R L ≃ₗ⁅R⁆ Trunc (R := R) (L := L) c :=
  LieEquiv.ofBijective (mk c) ⟨by
    intro x y hxy
    have h : x - y ∈ tail c := (mk_eq_zero c _).mp (by rw [map_sub, hxy, sub_self])
    rw [tail_eq_bot c hnil, LieSubmodule.mem_bot] at h
    exact sub_eq_zero.mp h, mk_surjective c⟩

@[simp] theorem fullEquiv_apply (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥)
    (x : Algebra R L) : fullEquiv c hnil x = mk c x := rfl

/-- Finiteness of the untruncated Rees algebra follows from its proved cutoff. -/
theorem finiteRees [Finite L] (c : ℕ) (hnil : lowerCentralSeries R L L c = ⊥) :
    Finite (Algebra R L) :=
  Finite.of_injective (fullEquiv c hnil) (fullEquiv c hnil).injective

@[simp] theorem coefficient_gradeOne (r : ℕ) (x : L) :
    coefficient r (gradeOne (R := R) x) = Finsupp.single 1 x r := by
  change coeff (monomial (R := R) 1 x) r = _
  rw [coeff_monomial]

/-- The degree-one quotient is all of additive `L`, not its abelianization.
This is deliberately a linear equivalence: the original bracket on `L`
need not vanish. -/
def terminalEquiv : Trunc (R := R) (L := L) 1 ≃ₗ[R] L :=
  { quotientCoefficient 1 1 le_rfl with
    invFun := fun x => mk 1 (gradeOne x)
    left_inv := by
      intro x
      obtain ⟨x, rfl⟩ := mk_surjective 1 x
      apply (mk_eq_mk_iff 1 _ _).mpr
      intro r hr
      interval_cases r
      · simp
      · simp
    right_inv := by intro x; simp }

@[simp] theorem terminalEquiv_mk (x : Algebra R L) :
    terminalEquiv (mk 1 x) = coefficient 1 x := rfl

theorem terminal_bracket (x y : Trunc (R := R) (L := L) 1) : ⁅x, y⁆ = 0 := by
  obtain ⟨x, rfl⟩ := mk_surjective 1 x
  obtain ⟨y, rfl⟩ := mk_surjective 1 y
  rw [← LieHom.map_lie, mk_eq_zero]
  apply bracket_mem_tail 0 x y
  intro r hr
  have : r = 0 := by omega
  subst r
  exact coefficient_zero y

/-- An actual homogeneous Rees current, with the required lower-central coefficient. -/
def homogeneous (r : ℕ) (hr : 0 < r) : gamma R L r →ₗ[R] Algebra R L where
  toFun x := ⟨monomial r x, monomial_mem hr x.property⟩
  map_add' x y := by
    apply Subtype.ext
    simp [monomial, TensorProduct.tmul_add]
  map_smul' a x := by
    apply Subtype.ext
    simp [monomial]

@[simp] theorem coefficient_homogeneous (r : ℕ) (hr : 0 < r)
    (x : gamma R L r) (s : ℕ) :
    coefficient s (homogeneous r hr x) = Finsupp.single r (x : L) s := by
  change coeff (monomial (R := R) r (x : L)) s = _
  rw [coeff_monomial]

/-- The top-degree coefficient space embeds in its actual truncation. -/
def topEmbedding (d : ℕ) : gamma R L (d + 1) →ₗ[R] Trunc (R := R) (L := L) (d + 1) :=
  (mk (d + 1)).toLinearMap.comp (homogeneous (d + 1) (by omega))

@[simp] theorem topEmbedding_coefficient (d : ℕ) (v : gamma R L (d + 1)) :
    quotientCoefficient (d + 1) (d + 1) le_rfl (topEmbedding d v) = (v : L) := by
  change coefficient (d + 1) (homogeneous (d + 1) _ v) = _
  simp

theorem topEmbedding_injective (d : ℕ) :
    Function.Injective (topEmbedding (R := R) (L := L) d) := by
  intro x y h
  apply Subtype.ext
  simpa only [topEmbedding_coefficient] using
    congrArg (quotientCoefficient (d + 1) (d + 1) le_rfl) h

@[simp] theorem projection_topEmbedding (d : ℕ) (v : gamma R L (d + 1)) :
    projection (Nat.le_succ d) (topEmbedding d v) = 0 := by
  change mk d (homogeneous (d + 1) _ v) = 0
  rw [mk_eq_zero]
  intro r hr
  rw [coefficient_homogeneous, Finsupp.single_eq_of_ne (by omega)]

/-- Surjectivity onto the actual kernel, not an assumed coordinate decomposition. -/
theorem top_kernel_iff (d : ℕ) (x : Trunc (R := R) (L := L) (d + 1)) :
    projection (Nat.le_succ d) x = 0 ↔ ∃ v, topEmbedding d v = x := by
  constructor
  · obtain ⟨x, rfl⟩ := mk_surjective (d + 1) x
    intro hx
    rw [projection_mk, mk_eq_zero] at hx
    let v : gamma R L (d + 1) :=
      ⟨coefficient (d + 1) x, (mem_rees_iff _).mp x.property |>.2 (d + 1)⟩
    refine ⟨v, (mk_eq_mk_iff (d + 1) _ _).mpr ?_⟩
    intro r hr
    rw [coefficient_homogeneous]
    by_cases h : r = d + 1
    · subst r; exact Finsupp.single_eq_same
    · rw [Finsupp.single_eq_of_ne h, hx r (by omega)]
  · rintro ⟨v, rfl⟩
    exact projection_topEmbedding d v

theorem topEmbedding_central (d : ℕ) (x : Trunc (R := R) (L := L) (d + 1))
    (v : gamma R L (d + 1)) : ⁅x, topEmbedding d v⁆ = 0 :=
  top_kernel_central d x _ (projection_topEmbedding d v)

theorem dilation_topEmbedding (d : ℕ) (u : Rˣ) (v : gamma R L (d + 1)) :
    quotientDilation (d + 1) u (topEmbedding d v) =
      topEmbedding d ((u : R) ^ (d + 1) • v) := by
  rw [top_kernel_dilation d u _ (projection_topEmbedding d v), map_smul]

end
end QSearch.ReesCentralQuotient

/-- info: 'QSearch.ReesCentralQuotient.bracket_vanishes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.bracket_vanishes

/-- info: 'QSearch.ReesCentralQuotient.tail' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.tail

/-- info: 'QSearch.ReesCentralQuotient.trunc_class_bound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.trunc_class_bound

/-- info: 'QSearch.ReesCentralQuotient.projection' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.projection

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_central' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_central

/-- info: 'QSearch.ReesCentralQuotient.finiteCoefficients_injective' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.finiteCoefficients_injective

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_dilation' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_dilation

/-- info: 'QSearch.ReesCentralQuotient.fullEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.fullEquiv

/-- info: 'QSearch.ReesCentralQuotient.terminalEquiv' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.terminalEquiv

/-- info: 'QSearch.ReesCentralQuotient.top_kernel_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.top_kernel_iff

/-- info: 'QSearch.ReesCentralQuotient.dilation_topEmbedding' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ReesCentralQuotient.dilation_topEmbedding
