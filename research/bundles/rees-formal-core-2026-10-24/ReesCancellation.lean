import ReesGroupBridge
import ReesCentralInstrument
import Mathlib.Algebra.Group.AddChar
import Mathlib.Algebra.Group.Equiv.TypeTags
import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.GroupTheory.Subgroup.Center

/-!
Construct the central cancellation certificate from automorphisms and a
nonzero moment witness. Hidden decompositions occur only in proofs, never
in the public controlled actions.
-/

namespace QSearch.ReesCancellation
open scoped BigOperators
open ReesCentralInstrument
noncomputable section
attribute [local instance] Classical.propDecidable

section Automorphisms
variable {G C I Q : Type*} [Group G] [CommGroup C]

def inHiddenCenter (H : Subgroup G) (embed : C →* G) (g : G) : Prop :=
  ∃ h : G, h ∈ H ∧ ∃ z : C, g = h * embed z

def quotientRelation (H : Subgroup G) (embed : C →* G) (sigma : Q → G)
    (q r : Q) : Prop := inHiddenCenter H embed ((sigma r)⁻¹ * sigma q)

def decomposition (H : Subgroup G) (embed : C →* G) (g : G) : G × C :=
  if hg : inHiddenCenter H embed g then
    (hg.choose, hg.choose_spec.2.choose) else (1, 1)

theorem decomposition_spec (H : Subgroup G) (embed : C →* G) (g : G)
    (hg : inHiddenCenter H embed g) :
    (decomposition H embed g).1 ∈ H ∧
      g = (decomposition H embed g).1 * embed (decomposition H embed g).2 := by
  simp only [decomposition, dite_eq_left hg]
  exact ⟨hg.choose_spec.1, hg.choose_spec.2.choose_spec⟩

def controlledAction (active : I → Prop) (delta : I → G ≃* G) (sigma : Q → G)
    (q : Q) (i : I) : G := if active i then delta i (sigma q) else 1

def centralAction (active : I → Prop) (alpha : I → C ≃* C) (z : C) (i : I) : C :=
  if active i then alpha i z else 1

theorem action_difference (active : I → Prop) (delta : I → G ≃* G)
    (sigma : Q → G) (q r : Q) (i : I) :
    (controlledAction active delta sigma r i)⁻¹ *
      controlledAction active delta sigma q i =
        if active i then delta i ((sigma r)⁻¹ * sigma q) else 1 := by
  by_cases hi : active i <;> simp [controlledAction, hi]

theorem hiddenCenter_preserved (H : Subgroup G) (embed : C →* G)
    (delta : G ≃* G) (alpha : C ≃* C)
    (preserves : ∀ g, delta g ∈ H ↔ g ∈ H)
    (center_map : ∀ z, delta (embed z) = embed (alpha z)) (g : G) :
    inHiddenCenter H embed (delta g) ↔ inHiddenCenter H embed g := by
  constructor
  · rintro ⟨h, hh, z, hz⟩
    refine ⟨delta.symm h, ?_, alpha.symm z, ?_⟩
    · exact (preserves _).mp (by simpa using hh)
    · apply delta.injective
      simpa only [map_mul, center_map, MulEquiv.apply_symm_apply] using hz
  · rintro ⟨h, hh, z, rfl⟩
    exact ⟨delta h, (preserves h).mpr hh, alpha z, by rw [map_mul, center_map]⟩

theorem central_range_normal (embed : C →* G)
    (central : ∀ z g, embed z * g = g * embed z) : embed.range.Normal := by
  apply Subgroup.normal_of_le_center
  rintro g ⟨z, rfl⟩
  exact Subgroup.mem_center_iff.mpr (fun x => (central z x).symm)

theorem hiddenCenter_quotient (H : Subgroup G) (embed : C →* G)
    [embed.range.Normal] (g : G) :
    inHiddenCenter H embed g ↔
      QuotientGroup.mk' embed.range g ∈ H.map (QuotientGroup.mk' embed.range) := by
  constructor
  · rintro ⟨h, hh, z, rfl⟩
    refine ⟨h, hh, ?_⟩
    have hz : QuotientGroup.mk' embed.range (embed z) = 1 :=
      (QuotientGroup.eq_one_iff _).mpr ⟨z, rfl⟩
    rw [map_mul, hz, mul_one]
  · rintro ⟨h, hh, he⟩
    have hk : h⁻¹ * g ∈ embed.range := by
      apply (QuotientGroup.eq_one_iff _).mp
      change QuotientGroup.mk' embed.range (h⁻¹*g) = 1
      rw [map_mul, map_inv, he, inv_mul_cancel]
    obtain ⟨z, hz⟩ := hk
    refine ⟨h, hh, z, ?_⟩
    rw [hz]
    group

theorem quotientRelation_iff (H : Subgroup G) (embed : C →* G) [embed.range.Normal]
    (sigma : G ⧸ embed.range → G)
    (section_law : ∀ q, QuotientGroup.mk' embed.range (sigma q) = q)
    (q r : G ⧸ embed.range) :
    quotientRelation H embed sigma q r ↔ r⁻¹*q ∈ H.map (QuotientGroup.mk' embed.range) := by
  unfold quotientRelation
  rw [hiddenCenter_quotient, map_mul, map_inv, section_law, section_law]

variable [Fintype I]

def automorphismCertificate (H : Subgroup G) (embed : C →* G)
    (chi : I → C →* ℂ) (active : I → Prop) (nonempty : ∃ i, active i)
    (delta : I → G ≃* G) (alpha : I → C ≃* C)
    (preserves : ∀ i, active i → ∀ g, delta i g ∈ H ↔ g ∈ H)
    (center_map : ∀ i, active i → ∀ z, delta i (embed z) = embed (alpha i z))
    (moment : ∀ z, (∏ i, chi i (centralAction active alpha z i)) = 1)
    (sigma : Q → G) : CancellationCertificate H embed chi
      (controlledAction active delta sigma) (quotientRelation H embed sigma) where
  active := active
  nonempty := nonempty
  h i q r := if active i then
    delta i (decomposition H embed ((sigma r)⁻¹ * sigma q)).1 else 1
  z i q r := centralAction active alpha
    (decomposition H embed ((sigma r)⁻¹ * sigma q)).2 i
  outside i q r hi hout c hc := by
    rw [action_difference, ite_eq_left hi] at hc
    apply hout
    apply (hiddenCenter_preserved H embed (delta i) (alpha i)
      (preserves i hi) (center_map i hi) _).mp
    refine ⟨_, hc, c, ?_⟩
    group
  inside i q r hin := by
    have hd := decomposition_spec H embed ((sigma r)⁻¹ * sigma q) hin
    rw [action_difference]
    by_cases hi : active i
    · simp only [ite_eq_left hi, centralAction]
      refine ⟨(preserves i hi _).mpr hd.1, ?_⟩
      calc
        _ = delta i ((decomposition H embed ((sigma r)⁻¹ * sigma q)).1 *
            embed (decomposition H embed ((sigma r)⁻¹ * sigma q)).2) :=
          congrArg (delta i) hd.2
        _ = _ := by rw [map_mul, center_map i hi]
    · simp [hi, centralAction]
  cancel q r _ := moment _

end Automorphisms

section Moments
variable {F V I : Type*} [Field F] [AddCommGroup V] [Module F V] [Fintype I]

def linearCharacter (psi : AddChar F ℂ) (lambda : V →ₗ[F] F) :
    Multiplicative V →* ℂ := (psi.compAddMonoidHom lambda.toAddMonoidHom).toMonoidHom

def scalarEquiv (a : F) (ha : a ≠ 0) : Multiplicative V ≃* Multiplicative V :=
  (LinearEquiv.smulOfNeZero F V a ha).toAddEquiv.toMultiplicative

def scaleEquiv (s : F) (d : ℕ) : Multiplicative V ≃* Multiplicative V :=
  if hs : s ≠ 0 then scalarEquiv (s^d) (pow_ne_zero _ hs) else MulEquiv.refl _

omit [Fintype I] in
theorem zero_scale_discard (s : I → F) (d : ℕ) (positive : 0 < d)
    (z : Multiplicative V) (i : I) :
    centralAction (fun i => s i ≠ 0) (fun i => scaleEquiv (s i) d) z i =
      Multiplicative.ofAdd (s i ^ d • z.toAdd) := by
  by_cases hi : s i ≠ 0
  · simp [centralAction, scaleEquiv, hi, scalarEquiv,
      LinearEquiv.smulOfNeZero, LinearEquiv.smulOfUnit]
  · have hz : s i = 0 := not_ne_iff.mp hi
    simp [centralAction, hz, Nat.ne_of_gt positive]

theorem character_sum (psi : AddChar F ℂ) (x : I → F) :
    psi (∑ i, x i) = ∏ i, psi (x i) := by
  have h := map_sum psi.toAddMonoidHom x Finset.univ
  exact h

theorem moment_cancels (psi : AddChar F ℂ) (lambda : I → V →ₗ[F] F)
    (s : I → F) (d : ℕ) (positive : 0 < d)
    (moment : (∑ i, s i ^ d • lambda i) = 0) (z : Multiplicative V) :
    (∏ i, linearCharacter psi (lambda i)
      (centralAction (fun i => s i ≠ 0) (fun i => scaleEquiv (s i) d) z i)) = 1 := by
  simp_rw [zero_scale_discard s d positive]
  change (∏ i, psi (lambda i (s i ^ d • z.toAdd))) = 1
  simp_rw [map_smul, smul_eq_mul]
  rw [← character_sum]
  have hm := LinearMap.congr_fun moment z.toAdd
  simp only [LinearMap.sum_apply, LinearMap.smul_apply, smul_eq_mul, LinearMap.zero_apply] at hm
  rw [hm, psi.map_zero_eq_one]

end Moments

section Rees
open ReesLie ReesDilation ReesGroupBridge LieModule
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] [Group L] {n : ℕ}

def hiddenSubgroup (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (h : LieSubalgebra F L) :
    Subgroup (groupCover law points nilpotent) :=
  ⨅ i, (subgroup law h).comap (evaluationGroupHom law points nilpotent i)

theorem mem_hiddenSubgroup (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (h : LieSubalgebra F L)
    (x : groupCover law points nilpotent) :
    x ∈ hiddenSubgroup law points nilpotent h ↔
      ∀ i, evaluationGroupHom law points nilpotent i x ∈ h := by
  simp only [hiddenSubgroup, Subgroup.mem_iInf, Subgroup.mem_comap]
  rfl

def highestEmbed (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n) (highest : j.val+1 = n) :
    Multiplicative (lowerCentralSeries F L L j.val) →* groupCover law points nilpotent where
  toFun v := highestGroupElement law points nilpotent j highest v.toAdd.val v.toAdd.property
  map_one' := by
    apply Subtype.ext
    funext i
    change points i ^ n • (0 : L) = 1
    rw [smul_zero, law.one_eq]
  map_mul' x y := by
    apply Subtype.ext
    change monomial points n (x.toAdd.val + y.toAdd.val) =
      monomial points n x.toAdd.val * monomial points n y.toAdd.val
    rw [commuting_mul_add (piLaw law) _ _
      (highest_monomial_central points nilpotent j highest x.toAdd.val x.toAdd.property _)]
    funext i
    exact smul_add _ _ _

theorem highestEmbed_injective (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (j : Fin n) (highest : j.val+1 = n) :
    Function.Injective (highestEmbed law points nilpotent j highest) := by
  intro x y hxy
  have he := congrFun (congrArg Subtype.val hxy) j
  change points j ^ n • x.toAdd.val = points j ^ n • y.toAdd.val at he
  have hval := (smul_right_injective (M := L) (pow_ne_zero n (nonzero j))) he
  exact congrArg Multiplicative.ofAdd (Subtype.ext hval)

theorem highestEmbed_central (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n) (highest : j.val+1 = n)
    (z : Multiplicative (lowerCentralSeries F L L j.val))
    (g : groupCover law points nilpotent) :
    highestEmbed law points nilpotent j highest z * g =
      g * highestEmbed law points nilpotent j highest z :=
  (highestGroup_central law points nilpotent j highest z.toAdd.val z.toAdd.property g).eq

def publicDilation (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (s : F) :
    groupCover law points nilpotent ≃* groupCover law points nilpotent :=
  if hs : s ≠ 0 then dilationGroupEquiv law points distinct nonzero nilpotent s hs
  else MulEquiv.refl _

theorem publicDilation_hidden (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (h : LieSubalgebra F L)
    (s : F) (hs : s ≠ 0) (x : groupCover law points nilpotent) :
    publicDilation law points distinct nonzero nilpotent s x ∈
      hiddenSubgroup law points nilpotent h ↔ x ∈ hiddenSubgroup law points nilpotent h := by
  rw [mem_hiddenSubgroup, mem_hiddenSubgroup]
  simp only [publicDilation, dite_eq_left hs]
  exact dilationGroup_hidden law points distinct nonzero nilpotent s hs h.toSubmodule x

theorem publicDilation_center (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n) (highest : j.val+1 = n)
    (s : F) (hs : s ≠ 0) (z : Multiplicative (lowerCentralSeries F L L j.val)) :
    publicDilation law points distinct nonzero nilpotent s
      (highestEmbed law points nilpotent j highest z) =
      highestEmbed law points nilpotent j highest (scaleEquiv s n z) := by
  simp only [publicDilation, scaleEquiv, dite_eq_left hs]
  apply Subtype.ext
  rw [dilationGroup_value]
  change dilationLinear points s (monomial points n z.toAdd.val) =
    monomial points n (s ^ n • z.toAdd.val)
  have he := dilation_monomial points distinct nonzero s j z.toAdd.val
  rwa [highest] at he

variable {I Q : Type*} [Fintype I]

def reesCertificate (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n) (highest : j.val+1 = n)
    (h : LieSubalgebra F L) (psi : AddChar F ℂ)
    (lambda : I → (lowerCentralSeries F L L j.val) →ₗ[F] F) (s : I → F)
    (nonempty : ∃ i, s i ≠ 0) (moment : (∑ i, s i ^ n • lambda i) = 0)
    (sigma : Q → groupCover law points nilpotent) :
    CancellationCertificate (hiddenSubgroup law points nilpotent h)
      (highestEmbed law points nilpotent j highest) (fun i => linearCharacter psi (lambda i))
      (controlledAction (fun i => s i ≠ 0)
        (fun i => publicDilation law points distinct nonzero nilpotent (s i)) sigma)
      (quotientRelation (hiddenSubgroup law points nilpotent h)
        (highestEmbed law points nilpotent j highest) sigma) :=
  automorphismCertificate _ _ _ _ nonempty _ (fun i => scaleEquiv (s i) n)
    (fun i hi => publicDilation_hidden law points distinct nonzero nilpotent h (s i) hi)
    (fun i hi => publicDilation_center law points distinct nonzero nilpotent j highest (s i) hi)
    (moment_cancels psi lambda s n (by omega) moment) sigma

variable {J R : Type*} [Fintype L] [Fintype J]

/-- Every measurement record is included. The witness finder and Fourier
completeness remain explicit inputs; the group certificate does not. -/
theorem rees_instrument (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (j : Fin n) (highest : j.val+1 = n)
    (h : LieSubalgebra F L) (psi : AddChar F ℂ)
    (unitary : ∀ x, psi x * star (psi x) = 1)
    (lambda : J → (lowerCentralSeries F L L j.val) →ₗ[F] F)
    (complete : ∀ z, (∑ l, linearCharacter psi (lambda l) z) =
      if z = 1 then (Fintype.card (Multiplicative (lowerCentralSeries F L L j.val)) : ℂ) else 0)
    (scales : (I → J) → I → F)
    (nonempty : ∀ labels, ∃ i, scales labels i ≠ 0)
    (moments : ∀ labels, (∑ i, scales labels i ^ n • lambda (labels i)) = 0)
    (sigma : Q → groupCover law points nilpotent) (rho : Q × R → Q × R → ℂ)
    (q r : Q) (a b : R) :
    (∑ labels : I → J, controlledDiscard
      (controlledAction (fun i => scales labels i ≠ 0)
        (fun i => publicDilation law points distinct nonzero nilpotent (scales labels i)) sigma)
      rho (fun x y => ∏ i, measuredEntry (hiddenSubgroup law points nilpotent h)
        (highestEmbed law points nilpotent j highest) (linearCharacter psi (lambda (labels i)))
        (x i) (y i)) q r a b) =
      rho (q, a) (r, b) * if quotientRelation (hiddenSubgroup law points nilpotent h)
        (highestEmbed law points nilpotent j highest) sigma q r then 1 else 0 := by
  apply central_instrument _ _ (highestEmbed_central law points nilpotent j highest)
    (fun l => linearCharacter psi (lambda l)) (fun l z => unitary (lambda l z.toAdd))
    (by intro z; split_ifs with hz <;> simpa [hz] using complete z)
  intro labels _
  exact reesCertificate law points distinct nonzero nilpotent j highest h psi
    (fun i => lambda (labels i)) (scales labels) (nonempty labels) (moments labels) sigma

end Rees

end
end QSearch.ReesCancellation
