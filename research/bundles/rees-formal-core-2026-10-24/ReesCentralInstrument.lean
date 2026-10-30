import ReesHomogenization
import Mathlib.Algebra.BigOperators.Group.Finset.Pi

/-!
Finite central measurement and controlled-target discard. The source is a
coset density, not a promised normalized character branch. Completeness of
the chosen unitary character family is an explicit Fourier identity.
-/

namespace QSearch.ReesCentralInstrument
open scoped BigOperators
open QSearch.ReesHomogenization (coefficient)
noncomputable section
attribute [local instance] Classical.propDecidable

section Characters
variable {C J : Type*} [Group C] [Fintype C] [Fintype J]

omit [Fintype C] [Fintype J] in
theorem character_star (chi : C →* ℂ) (unitary : ∀ z, chi z * star (chi z) = 1)
    (z : C) : star (chi z) = chi z⁻¹ := by
  have nz : chi z ≠ 0 := by
    intro h
    simpa [h] using unitary z
  apply mul_left_cancel₀ nz
  rw [unitary, ← map_mul, mul_inv_cancel, map_one]

theorem character_pair_sum (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (complete : ∀ z, (∑ j, chi j z) = if z = 1 then (Fintype.card C : ℂ) else 0)
    (z w : C) : (∑ j, chi j z * star (chi j w)) =
      if z = w then (Fintype.card C : ℂ) else 0 := by
  simp_rw [character_star _ (unitary _), ← map_mul]
  rw [complete, mul_inv_eq_one]

/-- The Fourier identity used by the physical Kraus completeness proof. -/
theorem fourier_gram (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (complete : ∀ z, (∑ j, chi j z) = if z = 1 then (Fintype.card C : ℂ) else 0)
    (v w : C → ℂ) :
    (∑ j, (∑ z, chi j z * v z) * star (∑ z, chi j z * w z)) =
      (Fintype.card C : ℂ) * ∑ z, v z * star (w z) := by
  have pair (z t : C) :
      (∑ j, (chi j z * v z) * (star (w t) * star (chi j t))) =
      if z = t then (Fintype.card C : ℂ) * (v z * star (w t)) else 0 := by
    calc
      _ = (∑ j, chi j z * star (chi j t)) * (v z * star (w t)) := by
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by rw [character_pair_sum chi unitary complete]; split_ifs <;> ring
  simp only [star_sum, star_mul, Finset.mul_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  conv_lhs => arg 2; ext z; rw [Finset.sum_comm]
  simp_rw [pair]
  simp
end Characters

section Central
variable {G C : Type*} [Group G] [CommGroup C] [Fintype G] [Fintype C]

def sourceEntry (H : Subgroup G) (x y : G) : ℂ :=
  (Fintype.card G : ℂ)⁻¹ * if y⁻¹ * x ∈ H then 1 else 0

def projectedEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ :=
  (Fintype.card C : ℂ)⁻¹ * ∑ z, chi z * sourceEntry H (x * (embed z)⁻¹) y

/-- Both sides of the spectral measurement, including its normalization. -/
def measuredEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ :=
  (Fintype.card C : ℂ)⁻¹ ^ 2 *
    ∑ w, ∑ z, chi z * star (chi w) *
      sourceEntry H (x * (embed z)⁻¹) (y * (embed w)⁻¹)

omit [Fintype C] in
theorem central_source_shift (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (x y : G) (z w : C) :
    sourceEntry H (x * (embed (z * w))⁻¹) (y * (embed w)⁻¹) =
      sourceEntry H (x * (embed z)⁻¹) y := by
  have he : (y * (embed w)⁻¹)⁻¹ * (x * (embed (z * w))⁻¹) =
      y⁻¹ * (x * (embed z)⁻¹) := by
    rw [map_mul]
    calc
      _ = embed w * (y⁻¹ * x) * (embed w)⁻¹ * (embed z)⁻¹ := by group
      _ = y⁻¹ * (x * (embed z)⁻¹) := by rw [central]; group
  simp only [sourceEntry, he]

theorem measurement_eq_projected (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : C →* ℂ)
    (unitary : ∀ z, chi z * star (chi z) = 1) (x y : G) :
    measuredEntry H embed chi x y = projectedEntry H embed chi x y := by
  have inner (w : C) :
      (∑ z, chi z * star (chi w) * sourceEntry H
        (x * (embed z)⁻¹) (y * (embed w)⁻¹)) =
      ∑ z, chi z * sourceEntry H (x * (embed z)⁻¹) y := by
    symm
    apply Fintype.sum_equiv (Equiv.mulRight w)
    intro z
    dsimp
    rw [central_source_shift H embed central, map_mul, mul_assoc (chi z)]
    rw [show chi w * (starRingEnd ℂ) (chi w) = 1 from unitary w, mul_one]
  have hn : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp only [measuredEntry, inner, Finset.sum_const, Finset.card_univ, nsmul_eq_mul,
    projectedEntry]
  field_simp

theorem projected_coefficient (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (x y : G) :
    projectedEntry H embed chi x y =
      (Fintype.card C : ℂ)⁻¹ * (Fintype.card G : ℂ)⁻¹ *
        coefficient H embed chi (y⁻¹ * x) := by
  simp only [projectedEntry, sourceEntry, coefficient, mul_assoc, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro z _
  split_ifs <;> ring

def correlation (rho : G → G → ℂ) (g : G) : ℂ := ∑ x, rho x (x * g⁻¹)

theorem projected_correlation (H : Subgroup G) (embed : C →* G)
    (chi : C →* ℂ) (g : G) :
    correlation (projectedEntry H embed chi) g =
      (Fintype.card C : ℂ)⁻¹ * coefficient H embed chi g := by
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [correlation, projected_coefficient]
  field_simp

def intersectionSize (H : Subgroup G) (embed : C →* G) : ℂ :=
  Fintype.card {z : C // embed z ∈ H}

omit [Fintype G] in
theorem intersectionSize_ne_zero (H : Subgroup G) (embed : C →* G) :
    intersectionSize H embed ≠ 0 := by
  unfold intersectionSize
  exact_mod_cast (Nat.ne_of_gt (QSearch.ReesHomogenization.intersection_card_pos H embed))

def normalizedEntry (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : ℂ :=
  (intersectionSize H embed)⁻¹ * (Fintype.card G : ℂ)⁻¹ *
    coefficient H embed chi (y⁻¹ * x)

theorem allowed_branch_mass (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, projectedEntry H embed chi x x) =
      intersectionSize H embed / (Fintype.card C : ℂ) := by
  have hc := QSearch.ReesHomogenization.coefficient_allowed H embed chi allowed 1 H.one_mem 1
  simp only [map_one, mul_one] at hc
  have ht := projected_correlation H embed chi 1
  simpa [correlation, hc, intersectionSize, div_eq_mul_inv, mul_comm] using ht

theorem normalized_correlation (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (g : G) : correlation (normalizedEntry H embed chi) g =
      coefficient H embed chi g / intersectionSize H embed := by
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [correlation, normalizedEntry]
  field_simp [intersectionSize_ne_zero H embed]

theorem normalized_trace (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) :
    (∑ x, normalizedEntry H embed chi x x) = 1 := by
  have hc := QSearch.ReesHomogenization.coefficient_allowed H embed chi allowed 1 H.one_mem 1
  simp only [map_one, mul_one] at hc
  change coefficient H embed chi 1 = intersectionSize H embed at hc
  have ht := normalized_correlation H embed chi 1
  simpa [correlation, hc, intersectionSize_ne_zero] using ht

theorem normalized_at (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (allowed : ∀ z, embed z ∈ H → chi z = 1) (h : G) (hh : h ∈ H) (z : C) :
    correlation (normalizedEntry H embed chi) (h * embed z) = chi z := by
  rw [normalized_correlation, QSearch.ReesHomogenization.coefficient_allowed H embed chi allowed h hh z]
  change intersectionSize H embed * chi z / intersectionSize H embed = chi z
  field_simp [intersectionSize_ne_zero H embed]

theorem normalized_outside (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (g : G) (outside : ∀ z, g * (embed z)⁻¹ ∉ H) :
    correlation (normalizedEntry H embed chi) g = 0 := by
  rw [normalized_correlation, QSearch.ReesHomogenization.coefficient_outside H embed chi g outside]
  simp

theorem branch_factorization (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (x y : G) : projectedEntry H embed chi x y =
      (intersectionSize H embed / (Fintype.card C : ℂ)) * normalizedEntry H embed chi x y := by
  rw [projected_coefficient, normalizedEntry]
  field_simp [intersectionSize_ne_zero H embed]

theorem forbidden_zero (H : Subgroup G) (embed : C →* G) (chi : C →* ℂ)
    (w : C) (hw : embed w ∈ H) (forbidden : chi w ≠ 1) (x y : G) :
    projectedEntry H embed chi x y = 0 := by
  rw [projected_coefficient, QSearch.ReesHomogenization.coefficient_forbidden H embed chi w hw forbidden]
  simp

theorem complete_branches {J : Type*} [Fintype J] (H : Subgroup G) (embed : C →* G)
    (chi : J → C →* ℂ) (complete : ∀ z, (∑ j, chi j z) =
      if z = 1 then (Fintype.card C : ℂ) else 0) (x y : G) :
    (∑ j, projectedEntry H embed (chi j) x y) = sourceEntry H x y := by
  have hn : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp only [projectedEntry, ← Finset.mul_sum]
  rw [Finset.sum_comm]
  simp_rw [← Finset.sum_mul, complete]
  simp [hn]

theorem complete_mass {J : Type*} [Fintype J] (H : Subgroup G) (embed : C →* G)
    (chi : J → C →* ℂ) (complete : ∀ z, (∑ j, chi j z) =
      if z = 1 then (Fintype.card C : ℂ) else 0) :
    (∑ j, ∑ x, projectedEntry H embed (chi j) x x) = 1 := by
  rw [Finset.sum_comm]
  simp_rw [complete_branches H embed chi complete]
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [sourceEntry, hn]
end Central

section FourierMeasurement
variable {G C J : Type*} [Group G] [Fintype G] [Group C] [Fintype C] [Fintype J]

def spectralAction (embed : C →* G) (chi : C →* ℂ) (v : G → ℂ) (x : G) : ℂ :=
  (Fintype.card C : ℂ)⁻¹ * ∑ z, chi z * v (x * (embed z)⁻¹)

/-- Completeness for every target vector, not just the chosen coset input.
This is the finite-dimensional Kraus completeness identity in quadratic
form. No injectivity of the embedding is needed. -/
theorem measurement_complete (embed : C →* G) (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (complete : ∀ z, (∑ j, chi j z) = if z = 1 then (Fintype.card C : ℂ) else 0)
    (v w : G → ℂ) :
    (∑ j, ∑ x, spectralAction embed (chi j) v x * star (spectralAction embed (chi j) w x)) =
      ∑ x, v x * star (w x) := by
  have localGram (x : G) :
      (∑ j, spectralAction embed (chi j) v x * star (spectralAction embed (chi j) w x)) =
      (Fintype.card C : ℂ)⁻¹ * ∑ z, v (x * (embed z)⁻¹) * star (w (x * (embed z)⁻¹)) := by
    have hn : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
    have hg := fourier_gram chi unitary complete
      (fun z => v (x * (embed z)⁻¹)) (fun z => w (x * (embed z)⁻¹))
    simp only [spectralAction, star_mul, star_inv₀, star_natCast]
    calc
      _ = (Fintype.card C : ℂ)⁻¹ ^ 2 *
          ∑ j, (∑ z, chi j z * v (x * (embed z)⁻¹)) *
            star (∑ z, chi j z * w (x * (embed z)⁻¹)) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = _ := by rw [hg]; field_simp
  rw [Finset.sum_comm]
  simp_rw [localGram]
  rw [← Finset.mul_sum, Finset.sum_comm]
  have translated (z : C) : (∑ x, v (x * (embed z)⁻¹) * star (w (x * (embed z)⁻¹))) =
      ∑ x, v x * star (w x) := by
    exact Fintype.sum_equiv (Equiv.mulRight (embed z)⁻¹) _ _ (fun _ => rfl)
  simp_rw [translated]
  have hn : (Fintype.card C : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [hn]
end FourierMeasurement

section ControlledDiscard
variable {G Q R : Type*} [Group G] [Fintype G]

/-- Literal controlled permutation and target partial trace on an arbitrary
address/reference matrix, with an independent target source. -/
def controlledDiscard (A : Q → G) (rho : Q × R → Q × R → ℂ)
    (tau : G → G → ℂ) (q r : Q) (a b : R) : ℂ :=
  ∑ t, ∑ x, ∑ y, if x = t * A q then
    if y = t * A r then rho (q, a) (r, b) * tau x y else 0 else 0

theorem controlledDiscard_eq (A : Q → G) (rho : Q × R → Q × R → ℂ)
    (tau : G → G → ℂ) (q r : Q) (a b : R) :
    controlledDiscard A rho tau q r a b =
      rho (q, a) (r, b) * correlation tau ((A r)⁻¹ * A q) := by
  classical
  simp only [controlledDiscard, Finset.sum_ite_irrel, Finset.sum_const_zero,
    Finset.sum_ite_eq', Finset.mem_univ, ite_true, ← Finset.mul_sum]
  congr 1
  symm
  apply Fintype.sum_equiv (Equiv.mulRight (A q)).symm
  intro t
  dsimp [correlation]
  congr 1 <;> group

theorem tensor_correlation {I : Type*} [Fintype I] (tau : I → G → G → ℂ)
    (g : I → G) :
    correlation (fun x y : I → G => ∏ i, tau i (x i) (y i)) g =
      ∏ i, correlation (tau i) (g i) := by
  simp only [correlation, Pi.mul_apply, Pi.inv_apply]
  exact (Fintype.prod_sum (fun i (x : G) => tau i x (x * (g i)⁻¹))).symm

/-- Zero scale targets may be retained, but at least one target must be
active and have the outside-support zero. Product phase cancellation alone
does not suffice. -/
theorem supported_product {I : Type*} [Fintype I] (support : Prop)
    (kernel phase : I → ℂ) (active : I → Prop)
    (nonempty : ∃ i, active i)
    (outside : ∀ i, active i → ¬ support → kernel i = 0)
    (inside : support → ∀ i, kernel i = phase i)
    (cancel : support → ∏ i, phase i = 1) :
    (∏ i, kernel i) = if support then 1 else 0 := by
  classical
  by_cases h : support
  · simp only [h, ite_true]
    simpa only [inside h] using cancel h
  · simp only [h, ite_false]
    obtain ⟨i, hi⟩ := nonempty
    exact Finset.prod_eq_zero (Finset.mem_univ i) (outside i hi h)

theorem descent_with_reference {I : Type*} [Fintype I]
    (A : Q → I → G) (rho : Q × R → Q × R → ℂ) (tau : I → G → G → ℂ)
    (relation : Q → Q → Prop) (active : I → Prop) (nonempty : ∃ i, active i)
    (phase : I → Q → Q → ℂ)
    (outside : ∀ i q r, active i → ¬ relation q r →
      correlation (tau i) ((A r i)⁻¹ * A q i) = 0)
    (inside : ∀ q r, relation q r → ∀ i,
      correlation (tau i) ((A r i)⁻¹ * A q i) = phase i q r)
    (cancel : ∀ q r, relation q r → ∏ i, phase i q r = 1)
    (q r : Q) (a b : R) :
    controlledDiscard A rho (fun x y => ∏ i, tau i (x i) (y i)) q r a b =
      rho (q, a) (r, b) * if relation q r then 1 else 0 := by
  rw [controlledDiscard_eq, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply]
  rw [supported_product (relation q r) _ (fun i => phase i q r) active nonempty
    (fun i hi h => outside i q r hi h) (inside q r) (cancel q r)]

theorem scaled_source (A : Q → G) (rho : Q × R → Q × R → ℂ)
    (tau : G → G → ℂ) (mass : ℂ) (q r : Q) (a b : R) :
    controlledDiscard A rho (fun x y => mass * tau x y) q r a b =
      mass * controlledDiscard A rho tau q r a b := by
  simp only [controlledDiscard_eq, correlation, ← Finset.mul_sum]
  ring

theorem zero_actions_identity (rho : Q × R → Q × R → ℂ)
    (tau : G → G → ℂ) (normalized : ∑ x, tau x x = 1) (q r : Q) (a b : R) :
    controlledDiscard (fun _ => 1) rho tau q r a b = rho (q, a) (r, b) := by
  simp [controlledDiscard_eq, correlation, normalized]

/-- Includes zero-probability records without asking for a normalized
state on them. The classical label is retained in this entrywise identity. -/
theorem all_record_factorization {J : Type*}
    (A : J → Q → G) (rho : Q × R → Q × R → ℂ)
    (tau : J → G → G → ℂ) (mass : J → ℂ)
    (relation : Q → Q → Prop)
    (zero : ∀ j, mass j = 0 → ∀ x y, tau j x y = 0)
    (positive : ∀ j, mass j ≠ 0 → ∀ q r,
      correlation (tau j) ((A j r)⁻¹ * A j q) =
        mass j * if relation q r then 1 else 0)
    (j : J) (q r : Q) (a b : R) :
    controlledDiscard (A j) rho (tau j) q r a b =
      mass j * (rho (q, a) (r, b) * if relation q r then 1 else 0) := by
  rw [controlledDiscard_eq]
  by_cases h : mass j = 0
  · simp [correlation, zero j h, h]
  · rw [positive j h]
    ring

theorem complete_instrument {J : Type*} [Fintype J]
    (A : J → Q → G) (rho : Q × R → Q × R → ℂ)
    (tau : J → G → G → ℂ) (mass : J → ℂ)
    (relation : Q → Q → Prop)
    (zero : ∀ j, mass j = 0 → ∀ x y, tau j x y = 0)
    (positive : ∀ j, mass j ≠ 0 → ∀ q r,
      correlation (tau j) ((A j r)⁻¹ * A j q) =
        mass j * if relation q r then 1 else 0)
    (complete : ∑ j, mass j = 1) (q r : Q) (a b : R) :
    (∑ j, controlledDiscard (A j) rho (tau j) q r a b) =
      rho (q, a) (r, b) * if relation q r then 1 else 0 := by
  simp_rw [all_record_factorization A rho tau mass relation zero positive]
  rw [← Finset.sum_mul, complete, one_mul]
end ControlledDiscard

section PhysicalRecords
variable {G C I Q R : Type*} [Group G] [Fintype G] [CommGroup C] [Fintype C] [Fintype I]

/-- Joins the actual two-sided central measurement to the reference-aware
discard theorem. Only support preservation and character cancellation
remain hypotheses; normalized target correlations are derived here. -/
theorem central_record_descent (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : I → C →* ℂ)
    (unitary : ∀ i z, chi i z * star (chi i z) = 1)
    (allowed : ∀ i z, embed z ∈ H → chi i z = 1)
    (A : Q → I → G) (rho : Q × R → Q × R → ℂ)
    (relation : Q → Q → Prop) (active : I → Prop) (nonempty : ∃ i, active i)
    (h : I → Q → Q → G) (z : I → Q → Q → C)
    (outside : ∀ i q r, active i → ¬ relation q r →
      ∀ c, ((A r i)⁻¹ * A q i) * (embed c)⁻¹ ∉ H)
    (inside : ∀ i q r, relation q r →
      h i q r ∈ H ∧ (A r i)⁻¹ * A q i = h i q r * embed (z i q r))
    (cancel : ∀ q r, relation q r → ∏ i, chi i (z i q r) = 1)
    (q r : Q) (a b : R) :
    controlledDiscard A rho
      (fun x y => ∏ i, measuredEntry H embed (chi i) (x i) (y i)) q r a b =
      (∏ _i : I, intersectionSize H embed / (Fintype.card C : ℂ)) *
        (rho (q, a) (r, b) * if relation q r then 1 else 0) := by
  have factor : (fun x y : I → G => ∏ i, measuredEntry H embed (chi i) (x i) (y i)) =
      (fun x y => (∏ _i : I, intersectionSize H embed / (Fintype.card C : ℂ)) *
        ∏ i, normalizedEntry H embed (chi i) (x i) (y i)) := by
    funext x y
    simp_rw [measurement_eq_projected H embed central _ (unitary _), branch_factorization]
    exact Finset.prod_mul_distrib
  rw [factor, scaled_source]
  congr 1
  apply descent_with_reference A rho _ relation active nonempty (fun i q r => chi i (z i q r))
  · intro i q r hi hqr
    exact normalized_outside H embed (chi i) _ (outside i q r hi hqr)
  · intro q r hqr i
    rw [(inside i q r hqr).2]
    exact normalized_at H embed (chi i) (allowed i) _ (inside i q r hqr).1 _
  · exact cancel

theorem forbidden_record_zero (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : I → C →* ℂ)
    (unitary : ∀ i z, chi i z * star (chi i z) = 1)
    (i : I) (w : C) (hw : embed w ∈ H) (forbidden : chi i w ≠ 1)
    (A : Q → I → G) (rho : Q × R → Q × R → ℂ) (q r : Q) (a b : R) :
    controlledDiscard A rho
      (fun x y => ∏ k, measuredEntry H embed (chi k) (x k) (y k)) q r a b = 0 := by
  have zero (x y : I → G) : (∏ k, measuredEntry H embed (chi k) (x k) (y k)) = 0 := by
    apply Finset.prod_eq_zero (Finset.mem_univ i)
    rw [measurement_eq_projected H embed central _ (unitary i)]
    exact forbidden_zero H embed (chi i) w hw forbidden _ _
  simp [controlledDiscard_eq, correlation, zero]

theorem packet_mass_complete {J : Type*} [Fintype J]
    (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (complete : ∀ z, (∑ j, chi j z) = if z = 1 then (Fintype.card C : ℂ) else 0) :
    (∑ labels : I → J, ∏ i, ∑ x, measuredEntry H embed (chi (labels i)) x x) = 1 := by
  rw [← Fintype.prod_sum (fun (_i : I) (j : J) => ∑ x, measuredEntry H embed (chi j) x x)]
  simp_rw [measurement_eq_projected H embed central _ (unitary _)]
  simp [complete_mass H embed chi complete]

/-- The remaining group-theoretic obligations. In the Rees application,
nonzero dilations supply support preservation and the moment equation
supplies cancellation. These are not replaced by an assumed ideal channel. -/
structure CancellationCertificate (H : Subgroup G) (embed : C →* G)
    (chi : I → C →* ℂ) (A : Q → I → G) (relation : Q → Q → Prop) where
  active : I → Prop
  nonempty : ∃ i, active i
  h : I → Q → Q → G
  z : I → Q → Q → C
  outside : ∀ i q r, active i → ¬ relation q r →
    ∀ c, ((A r i)⁻¹ * A q i) * (embed c)⁻¹ ∉ H
  inside : ∀ i q r, relation q r →
    h i q r ∈ H ∧ (A r i)⁻¹ * A q i = h i q r * embed (z i q r)
  cancel : ∀ q r, relation q r → ∏ i, chi i (z i q r) = 1

theorem central_cq_record {J : Type*}
    (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (A : (I → J) → Q → I → G) (rho : Q × R → Q × R → ℂ)
    (relation : Q → Q → Prop)
    (certificate : ∀ labels : I → J,
      (∀ i z, embed z ∈ H → chi (labels i) z = 1) →
        CancellationCertificate H embed (fun i => chi (labels i)) (A labels) relation)
    (labels : I → J) (q r : Q) (a b : R) :
    controlledDiscard (A labels) rho
      (fun x y => ∏ i, measuredEntry H embed (chi (labels i)) (x i) (y i)) q r a b =
      (∏ i, ∑ x, measuredEntry H embed (chi (labels i)) x x) *
        (rho (q, a) (r, b) * if relation q r then 1 else 0) := by
  by_cases allowed : ∀ i z, embed z ∈ H → chi (labels i) z = 1
  · let cert := certificate labels allowed
    have masses (i : I) : (∑ x, measuredEntry H embed (chi (labels i)) x x) =
        intersectionSize H embed / (Fintype.card C : ℂ) := by
      simp_rw [measurement_eq_projected H embed central _ (unitary _)]
      exact allowed_branch_mass H embed _ (allowed i)
    simp_rw [masses]
    exact central_record_descent H embed central (fun i => chi (labels i))
      (fun i => unitary (labels i)) allowed (A labels) rho relation cert.active cert.nonempty
      cert.h cert.z cert.outside cert.inside cert.cancel q r a b
  · push Not at allowed
    obtain ⟨i, w, hw, forbidden⟩ := allowed
    rw [forbidden_record_zero H embed central (fun i => chi (labels i))
      (fun i => unitary (labels i)) i w hw forbidden]
    have zero : (∏ i, ∑ x, measuredEntry H embed (chi (labels i)) x x) = 0 := by
      apply Finset.prod_eq_zero (Finset.mem_univ i)
      simp_rw [measurement_eq_projected H embed central _ (unitary _)]
      simp [forbidden_zero H embed _ w hw forbidden]
    rw [zero, zero_mul]

/-- Complete central measurement, adaptive controlled translations and
discard, on every input/reference matrix. No postselection factor and no
normalized state for forbidden labels is used. -/
theorem central_instrument {J : Type*} [Fintype J]
    (H : Subgroup G) (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) (chi : J → C →* ℂ)
    (unitary : ∀ j z, chi j z * star (chi j z) = 1)
    (complete : ∀ z, (∑ j, chi j z) = if z = 1 then (Fintype.card C : ℂ) else 0)
    (A : (I → J) → Q → I → G) (rho : Q × R → Q × R → ℂ)
    (relation : Q → Q → Prop)
    (certificate : ∀ labels : I → J,
      (∀ i z, embed z ∈ H → chi (labels i) z = 1) →
        CancellationCertificate H embed (fun i => chi (labels i)) (A labels) relation)
    (q r : Q) (a b : R) :
    (∑ labels : I → J, controlledDiscard (A labels) rho
      (fun x y => ∏ i, measuredEntry H embed (chi (labels i)) (x i) (y i)) q r a b) =
      rho (q, a) (r, b) * if relation q r then 1 else 0 := by
  simp_rw [central_cq_record H embed central chi unitary A rho relation certificate]
  rw [← Finset.sum_mul, packet_mass_complete H embed central chi unitary complete, one_mul]

end PhysicalRecords

end
end QSearch.ReesCentralInstrument
