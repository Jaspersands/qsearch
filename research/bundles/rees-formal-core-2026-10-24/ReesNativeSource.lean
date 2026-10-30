import ReesRecursiveSource

/-!
Native copy-only acquisition of the top Rees source. The source interface
uses independent mixed coset states and public controlled translations,
not a hiding-function oracle, inverse source preparation, or postselection.
-/
namespace QSearch.ReesNativeSource
open scoped BigOperators
open ReesGroupBridge ReesCentralInstrument ReesQuotients ReesStageInstrument ReesRecursiveSource
noncomputable section
attribute [local instance] Classical.propDecidable

section Pullback
variable {G A B I R : Type*} [Group G] [Group A] [Group B]
  [Fintype G] [Fintype A] [Fintype B] [Fintype I]

omit [Group A] [Group B] [Fintype A] [Fintype B] [Fintype I] in
theorem source_correlation (H : Subgroup G) (g : G) :
    correlation (sourceEntry H) g = if g ∈ H then 1 else 0 := by
  have hn : (Fintype.card G : ℂ) ≠ 0 := by exact_mod_cast Fintype.card_ne_zero
  simp [correlation, sourceEntry, mul_assoc, hn]

def pulledHidden (maps : I → A →* G) (H : I → Subgroup G) : Subgroup A :=
  ⨅ i, (H i).comap (maps i)

omit [Group G] [Group A] [Group B] [Fintype G] [Fintype A] [Fintype B] in
theorem indicator_product (P : I → Prop) :
    (∏ i, if P i then (1 : ℂ) else 0) = if ∀ i, P i then 1 else 0 := by
  by_cases h : ∀ i, P i
  · simp [h]
  · obtain ⟨i, hi⟩ := not_forall.mp h
    rw [ite_eq_right h]
    exact Finset.prod_eq_zero (Finset.mem_univ i) (ite_eq_right hi)

omit [Group B] [Fintype A] [Fintype B] in
/-- Reference-aware source pullback; no injectivity or surjectivity needed. -/
theorem pullback_with_reference (maps : I → A →* G) (H : I → Subgroup G)
    (rho : A × R → A × R → ℂ) (q r : A) (a b : R) :
    controlledDiscard (fun x i => maps i x) rho
      (fun x y => ∏ i, sourceEntry (H i) (x i) (y i)) q r a b =
    rho (q,a) (r,b) * if r⁻¹*q ∈ pulledHidden maps H then 1 else 0 := by
  rw [controlledDiscard_eq, tensor_correlation]
  simp only [Pi.mul_apply, Pi.inv_apply, source_correlation]
  rw [indicator_product]
  congr 1
  simp only [pulledHidden, Subgroup.mem_iInf, Subgroup.mem_comap, map_mul, map_inv]

def nativePullback (maps : I → A →* G) (states : I → G → G → ℂ) (q r : A) : ℂ :=
  controlledDiscard (fun x i => maps i x)
    (fun (_ _ : A × Unit) => (Fintype.card A : ℂ)⁻¹)
    (fun x y => ∏ i, states i (x i) (y i)) q r () ()

omit [Group B] [Fintype B] in
theorem nativePullback_source (maps : I → A →* G) (H : I → Subgroup G) :
    nativePullback maps (fun i => sourceEntry (H i)) = sourceEntry (pulledHidden maps H) := by
  funext q r
  exact pullback_with_reference maps H _ q r () ()

omit [Group A] [Fintype A] [Fintype I] in
theorem source_relabel (e : G ≃* B) (H : Subgroup G) (x y : B) :
    sourceEntry H (e.symm x) (e.symm y) = sourceEntry (H.map e.toMonoidHom) x y := by
  have hc : Fintype.card G = Fintype.card B := Fintype.card_congr e.toEquiv
  simp only [sourceEntry, hc, Subgroup.mem_map_equiv, map_mul, map_inv]

end Pullback

section Rees
open ReesLie ReesDilation LieModule
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] [Group L] {n : ℕ}
variable (law : PolynomialGroupLaw F L) (points : Fin n → F)
  (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
  (nilpotent : lowerCentralSeries F L L n = ⊥)

omit [Group L] in
theorem full_prefix (x : cover points nilpotent) :
    prefixRepresentative points distinct nonzero nilpotent n x = x := by
  apply Subtype.ext
  change evaluate points (truncate (F := F) n (recover points x.val)) = x.val
  have ht : truncate (F := F) n (recover points x.val) = recover points x.val := by
    funext j
    simp [truncate]
  rw [ht]
  exact evaluate_recover points distinct nonzero x.property

/-- The inverse top-coordinate map is the public full prefix, not hidden advice. -/
def topSection : (cover points nilpotent ⧸ tailIdeal points nilpotent n) → cover points nilpotent :=
  Quotient.lift (prefixRepresentative points distinct nonzero nilpotent n)
    (fun x y hxy => prefixRepresentative_eq points distinct nonzero nilpotent n x y (Quotient.sound hxy))

omit [Group L] in
theorem topSection_left (x : cover points nilpotent) :
    topSection points distinct nonzero nilpotent (quotientProjection points nilpotent n x) = x :=
  full_prefix points distinct nonzero nilpotent x

omit [Group L] in
theorem topSection_right (x : cover points nilpotent ⧸ tailIdeal points nilpotent n) :
    quotientProjection points nilpotent n (topSection points distinct nonzero nilpotent x) = x := by
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent n x
  rw [topSection_left]

def topGroupEquiv :
    letI := coverGroup law points nilpotent
    letI := stageGroup law points nilpotent n
    cover points nilpotent ≃* (cover points nilpotent ⧸ tailIdeal points nilpotent n) := by
  letI := coverGroup law points nilpotent
  letI := stageGroup law points nilpotent n
  exact {
    toFun := quotientProjection points nilpotent n
    invFun := topSection points distinct nonzero nilpotent
    left_inv := topSection_left points distinct nonzero nilpotent
    right_inv := topSection_right points distinct nonzero nilpotent
    map_mul' := (stageGroupProjection law points nilpotent n).map_mul }

theorem top_hidden_image (h : LieSubalgebra F L) :
    letI := coverGroup law points nilpotent
    letI := stageGroup law points nilpotent n
    (subgroup (coverLaw law points nilpotent) (hiddenLie points nilpotent h)).map
      (topGroupEquiv law points distinct nonzero nilpotent).toMonoidHom =
      subgroup (stageLaw law points nilpotent n) (stageHidden points nilpotent n h) := by
  rfl

def coverEvaluation (i : Fin n) :
    letI := coverGroup law points nilpotent
    cover points nilpotent →* L := evaluationGroupHom law points nilpotent i

theorem cover_hidden_pullback (h : LieSubalgebra F L) :
    letI := coverGroup law points nilpotent
    pulledHidden (coverEvaluation law points nilpotent) (fun _ => subgroup law h) =
      subgroup (coverLaw law points nilpotent) (hiddenLie points nilpotent h) := by
  let := coverGroup law points nilpotent
  apply Subgroup.ext
  intro x
  simp only [pulledHidden, Subgroup.mem_iInf, Subgroup.mem_comap]
  rfl

variable [Fintype L]

def acquireTop (states : Fin n → L → L → ℂ) :
    (cover points nilpotent ⧸ tailIdeal points nilpotent n) →
    (cover points nilpotent ⧸ tailIdeal points nilpotent n) → ℂ :=
  letI := coverGroup law points nilpotent
  fun x y => nativePullback (coverEvaluation law points nilpotent) states
    (topSection points distinct nonzero nilpotent x) (topSection points distinct nonzero nilpotent y)

theorem acquireTop_source (h : LieSubalgebra F L) :
    acquireTop law points distinct nonzero nilpotent (fun _ => sourceEntry (subgroup law h)) =
      reesSource law points nilpotent h n := by
  let := coverGroup law points nilpotent
  let := stageGroup law points nilpotent n
  let := stageFintype points nilpotent n
  funext x y
  unfold acquireTop
  rw [nativePullback_source, cover_hidden_pullback]
  have hr := source_relabel (topGroupEquiv law points distinct nonzero nilpotent)
    (subgroup (coverLaw law points nilpotent) (hiddenLie points nilpotent h)) x y
  rw [top_hidden_image] at hr
  exact hr

variable {Packets Labels : ℕ → Type*} [∀ k, Fintype (Packets k)] [∀ k, Fintype (Labels k)]

theorem native_average_tree (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    {d : ℕ} (tree : SourceTree Packets (fun _ => Unit) n d) :
    evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ)
      (acquireTop law points distinct nonzero nilpotent (fun _ => sourceEntry (subgroup law h)))
      (fun k _ => reesAverage law points distinct nonzero nilpotent k (plans k)) tree =
      reesSource law points nilpotent h d := by
  rw [acquireTop_source]
  exact rees_average_tree law points distinct nonzero nilpotent h plans tree

theorem native_record_tree (h : LieSubalgebra F L)
    (plans : ∀ k, ReesPlan law points distinct nonzero nilpotent k (Packets k) (Labels k))
    {d : ℕ} (tree : SourceTree Packets (fun k => Packets k → Labels k) n d) :
    evaluateTree (S := fun k => (cover points nilpotent ⧸ tailIdeal points nilpotent k) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent k) → ℂ)
      (acquireTop law points distinct nonzero nilpotent (fun _ => sourceEntry (subgroup law h)))
      (fun k => reesRecord law points distinct nonzero nilpotent k (plans k)) tree =
      treeWeight (fun k => reesMass law points distinct nonzero nilpotent h k (plans k)) tree •
        reesSource law points nilpotent h d := by
  rw [acquireTop_source]
  exact rees_record_tree law points distinct nonzero nilpotent h plans tree

end Rees
end
end QSearch.ReesNativeSource
