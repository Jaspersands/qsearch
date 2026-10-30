import ReesCancellation
import Mathlib.Algebra.Lie.Quotient

/-!
Actual graded tail ideals in the original Rees cover. A later stage is a
quotient by a tail, not a new evaluation realization of a truncated bracket.
-/

namespace QSearch.ReesQuotients
open scoped BigOperators
open ReesLie ReesDilation LieModule
noncomputable section

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L] {n : ℕ}

def lowKernel (d : ℕ) : Submodule F (Fin n → L) where
  carrier := {v | ∀ j, j.val < d → v j = 0}
  zero_mem' _ _ := rfl
  add_mem' hx hy j hj := by simp [hx j hj, hy j hj]
  smul_mem' a _ hx j hj := by simp [hx j hj]

def tailSpace (points : Fin n → F) (d : ℕ) : Submodule F (Fin n → L) :=
  (coefficientSpace ⊓ lowKernel d).map (evaluate points)

theorem tailSpace_le (points : Fin n → F) (d : ℕ) :
    tailSpace (L := L) points d ≤ evaluationSpace points :=
  Submodule.map_mono inf_le_left

theorem tailSpace_antitone (points : Fin n → F) {d e : ℕ} (hde : d ≤ e) :
    tailSpace (L := L) points e ≤ tailSpace points d := by
  apply Submodule.map_mono
  intro v hv
  exact ⟨hv.1, fun j hj => hv.2 j (lt_of_lt_of_le hj hde)⟩

theorem tailSpace_membership (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (d : ℕ) (x : Fin n → L) :
    x ∈ tailSpace points d ↔ x ∈ evaluationSpace points ∧
      ∀ j, j.val < d → recover points x j = 0 := by
  constructor
  · rintro ⟨v, hv, rfl⟩
    exact ⟨⟨v, hv.1, rfl⟩, by rw [recover_evaluate points distinct nonzero]; exact hv.2⟩
  · rintro ⟨hx, hz⟩
    exact ⟨recover points x, ⟨recover_mem points distinct nonzero hx, hz⟩,
      evaluate_recover points distinct nonzero hx⟩

theorem monomial_tail (points : Fin n → F) (d : ℕ) (j : Fin n) (hj : d ≤ j.val)
    (v : L) (hv : v ∈ lowerCentralSeries F L L j.val) :
    monomial points (j.val+1) v ∈ tailSpace points d := by
  classical
  refine ⟨Pi.single j v, ⟨?_, ?_⟩, evaluate_single points j v⟩
  · intro k
    by_cases hk : k = j
    · subst k; simpa using hv
    · simp [hk]
  · intro k hk
    have hkj : k ≠ j := by intro he; subst k; omega
    simp [hkj]

theorem bracket_tail_raise (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ)
    {x y : Fin n → L} (hx : x ∈ evaluationSpace points) (hy : y ∈ tailSpace points d) :
    ⁅x,y⁆ ∈ tailSpace points (d+1) := by
  obtain ⟨u, hu, rfl⟩ := hx
  obtain ⟨v, hv, rfl⟩ := hy
  rw [evaluate_eq_sum, evaluate_eq_sum, sum_lie_sum]
  apply Submodule.sum_mem
  intro r _
  apply Submodule.sum_mem
  intro s _
  rw [monomial_bracket]
  by_cases hs : s.val < d
  · rw [hv.2 s hs, lie_zero]
    have hz : monomial points (r.val+1+(s.val+1)) (0 : L) = 0 := by
      ext i; exact smul_zero _
    rw [hz]
    exact Submodule.zero_mem _
  · have hb := lowerCentral_bracket r.val s.val
      (LieSubmodule.lie_mem_lie (hu r) (hv.1 s))
    by_cases ht : r.val+s.val+1 < n
    · simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
        monomial_tail points (d+1) ⟨r.val+s.val+1, ht⟩ (by dsimp; omega) ⁅u r,v s⁆ hb
    · have hz := antitone_lowerCentralSeries F L L (Nat.le_of_not_gt ht) hb
      rw [nilpotent, LieSubmodule.mem_bot] at hz
      rw [hz]
      have hm : monomial points (r.val+1+(s.val+1)) (0 : L) = 0 := by
        ext i; exact smul_zero _
      rw [hm]
      exact Submodule.zero_mem _

def tailIdeal (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) : LieIdeal F (cover points nilpotent) where
  carrier := {x | x.val ∈ tailSpace points d}
  zero_mem' := (tailSpace points d).zero_mem
  add_mem' hx hy := (tailSpace points d).add_mem hx hy
  smul_mem' a _ hx := (tailSpace points d).smul_mem a hx
  lie_mem {x _y} hy := tailSpace_antitone points (Nat.le_succ d)
    (bracket_tail_raise points nilpotent d x.property hy)

theorem tailIdeal_antitone (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) {d e : ℕ} (hde : d ≤ e) :
    tailIdeal points nilpotent e ≤ tailIdeal points nilpotent d :=
  fun _ hx => tailSpace_antitone points hde hx

theorem tailIdeal_zero (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) : tailIdeal points nilpotent 0 = ⊤ := by
  apply top_unique
  intro x _
  obtain ⟨v, hv, he⟩ := x.property
  exact ⟨v, ⟨hv, fun j hj => by omega⟩, he⟩

theorem tailIdeal_end (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥) :
    tailIdeal points nilpotent n = ⊥ := by
  apply le_antisymm ?_ bot_le
  intro x hx
  change x = 0
  apply Subtype.ext
  have ht := (tailSpace_membership points distinct nonzero n x.val).mp hx
  have hz : recover points x.val = 0 := by funext j; exact ht.2 j j.isLt
  rw [← evaluate_recover points distinct nonzero x.property, hz, map_zero]
  rfl

theorem tailIdeal_raise (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ)
    (x y : cover points nilpotent) (hy : y ∈ tailIdeal points nilpotent d) :
    ⁅x,y⁆ ∈ tailIdeal points nilpotent (d+1) :=
  bracket_tail_raise points nilpotent d x.property hy

theorem dilation_tail (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (a : F) (ha : a ≠ 0) (x : cover points nilpotent) :
    dilationEquiv points distinct nonzero nilpotent a ha x ∈ tailIdeal points nilpotent d ↔
      x ∈ tailIdeal points nilpotent d := by
  change dilationLinear points a x.val ∈ tailSpace points d ↔ x.val ∈ tailSpace points d
  rw [tailSpace_membership points distinct nonzero, tailSpace_membership points distinct nonzero]
  rw [recover_dilation points distinct nonzero]
  have hx : x.val ∈ evaluationSpace points := x.property
  simp only [dilation_mem points distinct nonzero a hx, hx, true_and]
  constructor
  · intro h j hj
    exact (smul_eq_zero.mp (h j hj)).resolve_left (pow_ne_zero _ ha)
  · intro h j hj
    change a^(j.val+1) • recover points x.val j = 0
    rw [h j hj, smul_zero]

def quotientProjection (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    cover points nilpotent →ₗ⁅F⁆ (cover points nilpotent ⧸ tailIdeal points nilpotent d) where
  __ := (tailIdeal points nilpotent d).toSubmodule.mkQ
  map_lie' := by intros; rfl

theorem quotientProjection_surjective (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    Function.Surjective (quotientProjection points nilpotent d) := Quot.mk_surjective

theorem next_layer_central (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ)
    (x : cover points nilpotent) (hx : x ∈ tailIdeal points nilpotent d)
    (y : cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) :
    ⁅y, quotientProjection points nilpotent (d+1) x⁆ = 0 := by
  obtain ⟨z, rfl⟩ := quotientProjection_surjective points nilpotent (d+1) y
  rw [← (quotientProjection points nilpotent (d+1)).map_lie]
  exact (Submodule.Quotient.mk_eq_zero _).mpr (tailIdeal_raise points nilpotent d z x hx)

def truncate (d : ℕ) : (Fin n → L) →ₗ[F] (Fin n → L) where
  toFun v j := if j.val < d then v j else 0
  map_add' x y := by ext j; split_ifs with hj <;> simp [hj]
  map_smul' a x := by ext j; split_ifs with hj <;> simp [hj]

theorem truncate_mem (d : ℕ) {v : Fin n → L} (hv : v ∈ coefficientSpace (F := F)) :
    truncate (F := F) d v ∈ coefficientSpace (F := F) := by
  intro j
  change (if j.val < d then v j else 0) ∈ lowerCentralSeries F L L j.val
  split_ifs
  · exact hv j
  · exact LieSubmodule.zero_mem _

def prefixRepresentative (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (x : cover points nilpotent) : cover points nilpotent :=
  ⟨evaluate points (truncate d (recover points x.val)),
    ⟨_, truncate_mem d (recover_mem points distinct nonzero x.property), rfl⟩⟩

theorem quotient_eq_iff_prefix (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (x y : cover points nilpotent) :
    quotientProjection points nilpotent d x = quotientProjection points nilpotent d y ↔
      ∀ j, j.val < d → recover points x.val j = recover points y.val j := by
  change Submodule.Quotient.mk x = Submodule.Quotient.mk y ↔ _
  rw [Submodule.Quotient.eq]
  change x.val-y.val ∈ tailSpace points d ↔ _
  rw [tailSpace_membership points distinct nonzero]
  have hm : x.val-y.val ∈ evaluationSpace points :=
    (evaluationSpace (L := L) points).sub_mem x.property y.property
  simp only [hm, true_and]
  change (∀ j, j.val < d → recoverLinear points (x.val-y.val) j = 0) ↔ _
  rw [map_sub]
  simp only [Pi.sub_apply, sub_eq_zero]
  rfl

theorem prefixRepresentative_same (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (x : cover points nilpotent) :
    quotientProjection points nilpotent d (prefixRepresentative points distinct nonzero nilpotent d x) =
      quotientProjection points nilpotent d x := by
  rw [quotient_eq_iff_prefix points distinct nonzero]
  intro j hj
  change recover points (evaluate points (truncate (F := F) d (recover points x.val))) j = _
  rw [recover_evaluate points distinct nonzero]
  simp [truncate, hj]

def hiddenLie (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (h : LieSubalgebra F L) : LieSubalgebra F (cover points nilpotent) where
  carrier := {x | ∀ i, x.val i ∈ h}
  zero_mem' _ := h.zero_mem
  add_mem' hx hy i := h.add_mem (hx i) (hy i)
  smul_mem' a _ hx i := h.smul_mem a (hx i)
  lie_mem' hx hy i := h.lie_mem (hx i) (hy i)

theorem hiddenLie_coefficients (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (h : LieSubalgebra F L) (x : cover points nilpotent) :
    x ∈ hiddenLie points nilpotent h ↔ ∀ j, recover points x.val j ∈ h := by
  change (∀ i, evaluationHom points nilpotent i x ∈ h) ↔ _
  exact cover_membership_iff points distinct nonzero nilpotent h.toSubmodule x

def stageHidden (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (h : LieSubalgebra F L) :
    LieSubalgebra F (cover points nilpotent ⧸ tailIdeal points nilpotent d) :=
  (hiddenLie points nilpotent h).map (quotientProjection points nilpotent d)

theorem stageHidden_prefix (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (h : LieSubalgebra F L) (x : cover points nilpotent) :
    quotientProjection points nilpotent d x ∈ stageHidden points nilpotent d h ↔
      ∀ j, j.val < d → recover points x.val j ∈ h := by
  constructor
  · rintro ⟨y, hy, he⟩
    have hm := (hiddenLie_coefficients points distinct nonzero nilpotent h y).mp hy
    have hp := (quotient_eq_iff_prefix points distinct nonzero nilpotent d y x).mp he
    intro j hj
    rw [← hp j hj]
    exact hm j
  · intro hx
    refine ⟨prefixRepresentative points distinct nonzero nilpotent d x, ?_,
      prefixRepresentative_same points distinct nonzero nilpotent d x⟩
    change prefixRepresentative points distinct nonzero nilpotent d x ∈ hiddenLie points nilpotent h
    rw [hiddenLie_coefficients points distinct nonzero]
    intro j
    change recover points (evaluate points (truncate (F := F) d (recover points x.val))) j ∈ h
    rw [recover_evaluate points distinct nonzero]
    change (if j.val < d then recover points x.val j else 0) ∈ h
    split_ifs with hj
    · exact hx j hj
    · exact h.zero_mem

theorem first_stage_recovers_all_h (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) (h : LieSubalgebra F L) (v : L) :
    quotientProjection points nilpotent 1 (gradeOne points nilpotent positive v) ∈
      stageHidden points nilpotent 1 h ↔ v ∈ h := by
  classical
  rw [stageHidden_prefix points distinct nonzero, recover_gradeOne points distinct nonzero]
  constructor
  · intro hv
    simpa using hv ⟨0,positive⟩ (by simp)
  · intro hv j hj
    have hj0 : j = ⟨0,positive⟩ := by apply Fin.ext; dsimp; omega
    subst j
    simpa using hv

theorem first_stage_surjective (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) :
    Function.Surjective (fun v => quotientProjection points nilpotent 1
      (gradeOne points nilpotent positive v)) := by
  classical
  intro y
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent 1 y
  refine ⟨recover points x.val ⟨0,positive⟩, ?_⟩
  rw [quotient_eq_iff_prefix points distinct nonzero, recover_gradeOne points distinct nonzero]
  intro j hj
  have hj0 : j = ⟨0,positive⟩ := by apply Fin.ext; dsimp; omega
  subst j
  simp

theorem first_stage_injective (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (positive : 0 < n) :
    Function.Injective (fun v => quotientProjection points nilpotent 1
      (gradeOne points nilpotent positive v)) := by
  classical
  intro x y he
  rw [quotient_eq_iff_prefix points distinct nonzero,
    recover_gradeOne points distinct nonzero, recover_gradeOne points distinct nonzero] at he
  simpa using he ⟨0,positive⟩ (by simp)

theorem first_stage_abelian (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (x y : cover points nilpotent ⧸ tailIdeal points nilpotent 1) : ⁅x,y⁆ = 0 := by
  obtain ⟨z, rfl⟩ := quotientProjection_surjective points nilpotent 1 y
  exact next_layer_central points nilpotent 0 z (by rw [tailIdeal_zero]; trivial) x

/-- The original nonzero evaluation cannot be reused after degree-one
truncation of a nonabelian input. Later stages need quotient maps. -/
theorem truncated_evaluation_impossible (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (positive : 0 < n)
    (a : F) (ha : a ≠ 0) (x y : L) (noncommuting : ⁅x,y⁆ ≠ 0)
    (f : (cover points nilpotent ⧸ tailIdeal points nilpotent 1) →ₗ⁅F⁆ L)
    (evaluates : ∀ v, f (quotientProjection points nilpotent 1
      (gradeOne points nilpotent positive v)) = a • v) : False := by
  have he := f.map_lie (x := quotientProjection points nilpotent 1
    (gradeOne points nilpotent positive x)) (y := quotientProjection points nilpotent 1
      (gradeOne points nilpotent positive y))
  rw [first_stage_abelian, map_zero, evaluates, evaluates, smul_lie, lie_smul, smul_smul] at he
  exact noncommuting ((smul_eq_zero.mp he.symm).resolve_left (mul_ne_zero ha ha))

section Descend
variable {A B : Type*} [LieRing A] [LieAlgebra F A] [LieRing B] [LieAlgebra F B]

def quotientMap (I : LieIdeal F A) (J : LieIdeal F B) (f : A →ₗ⁅F⁆ B)
    (preserves : ∀ x, x ∈ I → f x ∈ J) : A ⧸ I →ₗ⁅F⁆ B ⧸ J where
  __ := I.toSubmodule.mapQ J.toSubmodule f.toLinearMap preserves
  map_lie' := by
    intro x y
    induction x using Submodule.Quotient.induction_on with | _ x
    induction y using Submodule.Quotient.induction_on with | _ y
    change Submodule.Quotient.mk (f ⁅x,y⁆) = Submodule.Quotient.mk ⁅f x,f y⁆
    rw [f.map_lie]

def quotientEquiv (I : LieIdeal F A) (e : A ≃ₗ⁅F⁆ A)
    (preserves : ∀ x, e x ∈ I ↔ x ∈ I) : (A ⧸ I) ≃ₗ⁅F⁆ (A ⧸ I) where
  __ := quotientMap I I e.toLieHom (fun x hx => (preserves x).mpr hx)
  invFun := quotientMap I I e.symm.toLieHom
    (fun x hx => (preserves _).mp (by simpa using hx))
  left_inv x := by
    induction x using Submodule.Quotient.induction_on with | _ x
    change Submodule.Quotient.mk (e.symm (e x)) = Submodule.Quotient.mk x
    rw [LieEquiv.symm_apply_apply]
  right_inv x := by
    induction x using Submodule.Quotient.induction_on with | _ x
    change Submodule.Quotient.mk (e (e.symm x)) = Submodule.Quotient.mk x
    rw [LieEquiv.apply_symm_apply]

end Descend

def stageDilation (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (a : F) (ha : a ≠ 0) :
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) ≃ₗ⁅F⁆
      (cover points nilpotent ⧸ tailIdeal points nilpotent d) :=
  quotientEquiv (tailIdeal points nilpotent d)
    (dilationEquiv points distinct nonzero nilpotent a ha)
    (dilation_tail points distinct nonzero nilpotent d a ha)

theorem stageDilation_projection (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (a : F) (ha : a ≠ 0) (x : cover points nilpotent) :
    stageDilation points distinct nonzero nilpotent d a ha (quotientProjection points nilpotent d x) =
      quotientProjection points nilpotent d (dilationEquiv points distinct nonzero nilpotent a ha x) := rfl

theorem stageDilation_hidden (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (a : F) (ha : a ≠ 0) (h : LieSubalgebra F L)
    (x : cover points nilpotent ⧸ tailIdeal points nilpotent d) :
    stageDilation points distinct nonzero nilpotent d a ha x ∈ stageHidden points nilpotent d h ↔
      x ∈ stageHidden points nilpotent d h := by
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent d x
  rw [stageDilation_projection, stageHidden_prefix points distinct nonzero,
    stageHidden_prefix points distinct nonzero]
  change (∀ j, j.val < d → recover points (dilationLinear points a x.val) j ∈ h) ↔ _
  rw [recover_dilation points distinct nonzero]
  constructor
  · intro hm j hj
    have he : a^(j.val+1) • recover points x.val j ∈ h := hm j hj
    exact (h.toSubmodule.smul_mem_iff (pow_ne_zero _ ha)).mp he
  · intro hm j hj
    exact h.smul_mem _ (hm j hj)

def stageFactor (points : Fin n → F) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d e : ℕ) (hde : d ≤ e) :
    (cover points nilpotent ⧸ tailIdeal points nilpotent e) →ₗ⁅F⁆
      (cover points nilpotent ⧸ tailIdeal points nilpotent d) :=
  quotientMap _ _ (LieHom.id)
    (fun _ hx => tailIdeal_antitone points nilpotent hde hx)

theorem stageFactor_projection (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e)
    (x : cover points nilpotent) :
    stageFactor points nilpotent d e hde (quotientProjection points nilpotent e x) =
      quotientProjection points nilpotent d x := rfl

theorem stageFactor_surjective (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e) :
    Function.Surjective (stageFactor points nilpotent d e hde) := by
  intro x
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent d x
  exact ⟨quotientProjection points nilpotent e x, rfl⟩

theorem stageFactor_hidden (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e)
    (h : LieSubalgebra F L) :
    (stageHidden points nilpotent e h).map (stageFactor points nilpotent d e hde) =
      stageHidden points nilpotent d h := by
  apply LieSubalgebra.ext
  intro x
  constructor
  · rintro ⟨y, ⟨z, hz, rfl⟩, rfl⟩
    exact ⟨z, hz, rfl⟩
  · rintro ⟨y, hy, rfl⟩
    exact ⟨quotientProjection points nilpotent e y, ⟨y, hy, rfl⟩, rfl⟩

theorem stageFactor_comp (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d e f : ℕ) (hde : d ≤ e) (hef : e ≤ f) :
    (stageFactor points nilpotent d e hde).comp (stageFactor points nilpotent e f hef) =
      stageFactor points nilpotent d f (hde.trans hef) := by
  apply LieHom.ext
  intro x
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent f x
  rfl

theorem stageFactor_zero_iff (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e)
    (x : cover points nilpotent ⧸ tailIdeal points nilpotent e) :
    stageFactor points nilpotent d e hde x = 0 ↔
      ∃ y : cover points nilpotent, y ∈ tailIdeal points nilpotent d ∧
        quotientProjection points nilpotent e y = x := by
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent e x
  constructor
  · intro hx
    exact ⟨x, (Submodule.Quotient.mk_eq_zero _).mp hx, rfl⟩
  · rintro ⟨y, hy, he⟩
    rw [← he, stageFactor_projection]
    exact (Submodule.Quotient.mk_eq_zero _).mpr hy

theorem prefixRepresentative_eq (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (x y : cover points nilpotent)
    (he : quotientProjection points nilpotent d x = quotientProjection points nilpotent d y) :
    prefixRepresentative points distinct nonzero nilpotent d x =
      prefixRepresentative points distinct nonzero nilpotent d y := by
  have hp := (quotient_eq_iff_prefix points distinct nonzero nilpotent d x y).mp he
  apply Subtype.ext
  change evaluate points (truncate (F := F) d (recover points x.val)) =
    evaluate points (truncate (F := F) d (recover points y.val))
  congr 1
  ext j
  by_cases hj : j.val < d <;> simp [truncate, hj, hp]

/-- Zero-padding in original Rees coordinates; no hidden data or choice of
hidden coset representatives. This section is not claimed homomorphic. -/
def stageSection (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d e : ℕ) : (cover points nilpotent ⧸ tailIdeal points nilpotent d) →
      (cover points nilpotent ⧸ tailIdeal points nilpotent e) :=
  Quotient.lift (fun x => quotientProjection points nilpotent e
    (prefixRepresentative points distinct nonzero nilpotent d x))
    (fun x y hxy => congrArg (quotientProjection points nilpotent e)
      (prefixRepresentative_eq points distinct nonzero nilpotent d x y (Quotient.sound hxy)))

theorem stageSection_right_inverse (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d e : ℕ) (hde : d ≤ e) (x : cover points nilpotent ⧸ tailIdeal points nilpotent d) :
    stageFactor points nilpotent d e hde (stageSection points distinct nonzero nilpotent d e x) = x := by
  obtain ⟨x, rfl⟩ := quotientProjection_surjective points nilpotent d x
  exact prefixRepresentative_same points distinct nonzero nilpotent d x

theorem next_layer_scalar (points : Fin n → F) (distinct : Function.Injective points)
    (nonzero : ∀ i, points i ≠ 0) (nilpotent : lowerCentralSeries F L L n = ⊥)
    (d : ℕ) (a : F) (ha : a ≠ 0) (x : cover points nilpotent)
    (hx : x ∈ tailIdeal points nilpotent d) :
    stageDilation points distinct nonzero nilpotent (d+1) a ha
      (quotientProjection points nilpotent (d+1) x) =
        a^(d+1) • quotientProjection points nilpotent (d+1) x := by
  rw [stageDilation_projection, ← map_smul, quotient_eq_iff_prefix points distinct nonzero]
  have ht := (tailSpace_membership points distinct nonzero d x.val).mp hx
  intro j hj
  change recover points (dilationLinear points a x.val) j =
    recoverLinear points (a^(d+1) • x.val) j
  rw [recover_dilation points distinct nonzero, map_smul]
  change a^(j.val+1) • recover points x.val j = a^(d+1) • recover points x.val j
  by_cases hjd : j.val < d
  · rw [ht.2 j hjd, smul_zero, smul_zero]
  · have he : j.val = d := by omega
    rw [he]

section PolynomialGroups
open ReesGroupBridge
variable {A B : Type*} [LieRing A] [LieAlgebra F A] [Group A]
  [LieRing B] [LieAlgebra F B]

theorem map_product (law : PolynomialGroupLaw F A) (f : A →ₗ⁅F⁆ B) (x y : A) :
    f (x*y) = interpret law.expression (f x) (f y) := by
  rw [law.mul_eq, map_interpret]

/-- Group axioms on a Lie image are inherited through the actual surjection,
not supplied as another BCH theorem for each quotient. -/
@[instance_reducible] def imageGroup (law : PolynomialGroupLaw F A) (f : A →ₗ⁅F⁆ B)
    (surjective : Function.Surjective f) : Group B where
  mul := interpret law.expression
  one := 0
  inv := Neg.neg
  mul_assoc x y z := by
    obtain ⟨x, rfl⟩ := surjective x
    obtain ⟨y, rfl⟩ := surjective y
    obtain ⟨z, rfl⟩ := surjective z
    change interpret law.expression (interpret law.expression (f x) (f y)) (f z) =
      interpret law.expression (f x) (interpret law.expression (f y) (f z))
    simp only [← map_product law f, mul_assoc]
  one_mul x := by
    obtain ⟨x, rfl⟩ := surjective x
    change interpret law.expression 0 (f x) = f x
    have he : f 1 = 0 := by rw [law.one_eq, map_zero]
    rw [← he, ← map_product law f, one_mul]
  mul_one x := by
    obtain ⟨x, rfl⟩ := surjective x
    change interpret law.expression (f x) 0 = f x
    have he : f 1 = 0 := by rw [law.one_eq, map_zero]
    rw [← he, ← map_product law f, mul_one]
  inv_mul_cancel x := by
    obtain ⟨x, rfl⟩ := surjective x
    change interpret law.expression (-f x) (f x) = 0
    have he : f x⁻¹ = -f x := by rw [law.inv_eq, map_neg]
    rw [← he, ← map_product law f, inv_mul_cancel, law.one_eq, map_zero]

def imageLaw (law : PolynomialGroupLaw F A) (f : A →ₗ⁅F⁆ B)
    (surjective : Function.Surjective f) :
    letI := imageGroup law f surjective
    PolynomialGroupLaw F B := by
  letI := imageGroup law f surjective
  exact ⟨law.expression, fun _ _ => rfl, rfl, fun _ => rfl⟩

@[instance_reducible] def subalgebraGroup (law : PolynomialGroupLaw F A) (S : LieSubalgebra F A) : Group S :=
  inferInstanceAs (Group (subgroup law S))

def subalgebraLaw (law : PolynomialGroupLaw F A) (S : LieSubalgebra F A) :
    letI := subalgebraGroup law S
    PolynomialGroupLaw F S := by
  letI := subalgebraGroup law S
  refine ⟨law.expression, ?_, ?_, ?_⟩
  · intro x y
    apply Subtype.ext
    change x.val*y.val = S.incl (interpret law.expression x y)
    rw [map_interpret, law.mul_eq]
    rfl
  · apply Subtype.ext
    exact law.one_eq
  · intro x
    apply Subtype.ext
    exact law.inv_eq x.val

variable [Group B]

def polynomialGroupHom (lawA : PolynomialGroupLaw F A) (lawB : PolynomialGroupLaw F B)
    (same : lawA.expression = lawB.expression) (f : A →ₗ⁅F⁆ B) : A →* B where
  toFun := f
  map_one' := by rw [lawA.one_eq, map_zero, lawB.one_eq]
  map_mul' x y := by rw [map_product lawA f, same, lawB.mul_eq]

def polynomialGroupEquiv (law : PolynomialGroupLaw F A) (e : A ≃ₗ⁅F⁆ A) : A ≃* A where
  __ := e.toLinearEquiv.toEquiv
  map_mul' x y := by
    change e.toLieHom (x*y) = e.toLieHom x * e.toLieHom y
    rw [map_product law e.toLieHom, law.mul_eq]

end PolynomialGroups

section StageGroups
open ReesGroupBridge
variable [Group L]

@[instance_reducible] def coverGroup (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) : Group (cover points nilpotent) :=
  subalgebraGroup (piLaw law) (cover points nilpotent)

def coverLaw (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) :
    letI := coverGroup law points nilpotent
    PolynomialGroupLaw F (cover points nilpotent) := subalgebraLaw (piLaw law) _

@[instance_reducible] def stageGroup (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    Group (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := coverGroup law points nilpotent
  exact imageGroup (coverLaw law points nilpotent) (quotientProjection points nilpotent d)
    (quotientProjection_surjective points nilpotent d)

def stageLaw (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    letI := stageGroup law points nilpotent d
    PolynomialGroupLaw F (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := coverGroup law points nilpotent
  exact imageLaw (coverLaw law points nilpotent) (quotientProjection points nilpotent d)
    (quotientProjection_surjective points nilpotent d)

def stageGroupProjection (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) :
    letI := coverGroup law points nilpotent
    letI := stageGroup law points nilpotent d
    cover points nilpotent →* (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := coverGroup law points nilpotent
  letI := stageGroup law points nilpotent d
  exact polynomialGroupHom (coverLaw law points nilpotent) (stageLaw law points nilpotent d)
    rfl (quotientProjection points nilpotent d)

def stageGroupFactor (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e) :
    letI := stageGroup law points nilpotent e
    letI := stageGroup law points nilpotent d
    (cover points nilpotent ⧸ tailIdeal points nilpotent e) →*
      (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := stageGroup law points nilpotent e
  letI := stageGroup law points nilpotent d
  exact polynomialGroupHom (stageLaw law points nilpotent e) (stageLaw law points nilpotent d)
    rfl (stageFactor points nilpotent d e hde)

def stageGroupDilation (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) (a : F) (ha : a ≠ 0) :
    letI := stageGroup law points nilpotent d
    (cover points nilpotent ⧸ tailIdeal points nilpotent d) ≃*
      (cover points nilpotent ⧸ tailIdeal points nilpotent d) := by
  letI := stageGroup law points nilpotent d
  exact polynomialGroupEquiv (stageLaw law points nilpotent d)
    (stageDilation points distinct nonzero nilpotent d a ha)

theorem next_layer_group_central (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ)
    (x : cover points nilpotent) (hx : x ∈ tailIdeal points nilpotent d)
    (y : cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) :
    letI := stageGroup law points nilpotent (d+1)
    Commute y (quotientProjection points nilpotent (d+1) x) := by
  let := stageGroup law points nilpotent (d+1)
  exact commuting_group (stageLaw law points nilpotent (d+1)) _ _
    (next_layer_central points nilpotent d x hx y)

theorem first_stage_group_additive (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥)
    (x y : cover points nilpotent ⧸ tailIdeal points nilpotent 1) :
    letI := stageGroup law points nilpotent 1
    x*y = x+y := by
  let := stageGroup law points nilpotent 1
  exact commuting_mul_add (stageLaw law points nilpotent 1) x y (first_stage_abelian points nilpotent x y)

theorem stageGroupFactor_hidden (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d e : ℕ) (hde : d ≤ e)
    (h : LieSubalgebra F L) :
    letI := stageGroup law points nilpotent e
    letI := stageGroup law points nilpotent d
    (subgroup (stageLaw law points nilpotent e) (stageHidden points nilpotent e h)).map
      (stageGroupFactor law points nilpotent d e hde) =
        subgroup (stageLaw law points nilpotent d) (stageHidden points nilpotent d h) := by
  let := stageGroup law points nilpotent e
  let := stageGroup law points nilpotent d
  apply Subgroup.ext
  intro x
  change x ∈ (stageHidden points nilpotent e h).map (stageFactor points nilpotent d e hde) ↔
    x ∈ stageHidden points nilpotent d h
  rw [stageFactor_hidden]

theorem stageGroupDilation_hidden (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) (a : F) (ha : a ≠ 0)
    (h : LieSubalgebra F L) (x : cover points nilpotent ⧸ tailIdeal points nilpotent d) :
    letI := stageGroup law points nilpotent d
    stageGroupDilation law points distinct nonzero nilpotent d a ha x ∈
      subgroup (stageLaw law points nilpotent d) (stageHidden points nilpotent d h) ↔
        x ∈ subgroup (stageLaw law points nilpotent d) (stageHidden points nilpotent d h) := by
  exact stageDilation_hidden points distinct nonzero nilpotent d a ha h x

theorem step_kernel_central_and_scaled (law : PolynomialGroupLaw F L) (points : Fin n → F)
    (distinct : Function.Injective points) (nonzero : ∀ i, points i ≠ 0)
    (nilpotent : lowerCentralSeries F L L n = ⊥) (d : ℕ) (a : F) (ha : a ≠ 0)
    (x : cover points nilpotent ⧸ tailIdeal points nilpotent (d+1)) :
    letI := stageGroup law points nilpotent (d+1)
    letI := stageGroup law points nilpotent d
    stageGroupFactor law points nilpotent d (d+1) (Nat.le_succ d) x = 1 →
      (∀ y, Commute y x) ∧
        stageGroupDilation law points distinct nonzero nilpotent (d+1) a ha x = a^(d+1) • x := by
  let := stageGroup law points nilpotent (d+1)
  let := stageGroup law points nilpotent d
  intro hx
  change stageFactor points nilpotent d (d+1) (Nat.le_succ d) x = 0 at hx
  obtain ⟨y, hy, rfl⟩ := (stageFactor_zero_iff points nilpotent d (d+1) (Nat.le_succ d) x).mp hx
  exact ⟨next_layer_group_central law points nilpotent d y hy,
    next_layer_scalar points distinct nonzero nilpotent d a ha y hy⟩

end StageGroups

end
end QSearch.ReesQuotients
