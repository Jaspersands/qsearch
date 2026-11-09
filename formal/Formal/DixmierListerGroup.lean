import Formal.DixmierListerScalars
import Formal.BCHClassThreeSubgroups

/-!
# Central powers of the Dixmier–Lister group

Source: `research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/core/main-core.tex`,
Proposition `prop:dl-central-scalars`, second sentence: for `p > 3` no automorphism of the
Lazard group `exp(L_DL)` over `F_p` acts on its centre as `z ↦ z^ζ` with `ζ ≠ ±1`.

`DL R` has class three (`lcs_three_eq_bot`, any commutative ring), so the class-three BCH
group `BCH (ZMod p) (DL (ZMod p))` of `Formal/BCHClassThree.lean` exists whenever `2` and
`3` are units, i.e. for every prime `p > 3`; class three is below `p`, and this BCH group
is the Lazard group of the paper. A group automorphism is turned into a Lie automorphism
by the explicit power and commutator words of `Formal/BCHClassThreeSubgroups.lean`
(`toLieEquiv`): no Lazard correspondence is assumed. The group centre is the Lie centre
(`mem_center_iff_val`), and `z ^ ζ.val` has logarithm `ζ • log z`. So
`group_center_pow_iff` (exponent `ζ ∈ F_p`) and `group_center_zpow_iff` (integer exponent
`k`, condition `k ≡ ±1 mod p`) follow from `exists_aut_center_smul_iff`, in both
directions.
-/

namespace QSearch.DixmierLister

open LieModule QSearch.BCHClassThree QSearch.BCHClassThreeSubgroups

section Nilpotent

variable {R : Type*} [CommRing R]

/-- The coordinate subspace `{x₁ = x₂ = x₃ = x₄ = 0} = span(e₅, …, e₈)`, a Lie ideal. -/
def gammaTwo : LieSubmodule R (DL R) (DL R) where
  carrier := {x | x 0 = 0 ∧ x 1 = 0 ∧ x 2 = 0 ∧ x 3 = 0}
  add_mem' := by
    rintro x y ⟨a0, a1, a2, a3⟩ ⟨b0, b1, b2, b3⟩
    simp [a0, a1, a2, a3, b0, b1, b2, b3]
  zero_mem' := by simp
  smul_mem' := by
    rintro t x ⟨a0, a1, a2, a3⟩
    simp [a0, a1, a2, a3]
  lie_mem := by
    intro x m _
    simp

/-- The coordinate subspace `span(e₇, e₈)`, a Lie ideal. -/
def gammaThree : LieSubmodule R (DL R) (DL R) where
  carrier := {x | x 0 = 0 ∧ x 1 = 0 ∧ x 2 = 0 ∧ x 3 = 0 ∧ x 4 = 0 ∧ x 5 = 0}
  add_mem' := by
    rintro x y ⟨a0, a1, a2, a3, a4, a5⟩ ⟨b0, b1, b2, b3, b4, b5⟩
    simp [a0, a1, a2, a3, a4, a5, b0, b1, b2, b3, b4, b5]
  zero_mem' := by simp
  smul_mem' := by
    rintro t x ⟨a0, a1, a2, a3, a4, a5⟩
    simp [a0, a1, a2, a3, a4, a5]
  lie_mem := by
    rintro x m ⟨m0, m1, m2, m3, -, -⟩
    simp [m0, m1, m2, m3]

/-- `DL R` has nilpotency class at most three. -/
theorem lcs_three_eq_bot : lowerCentralSeries R (DL R) (DL R) 3 = ⊥ := by
  have h1 : lowerCentralSeries R (DL R) (DL R) 1 ≤ gammaTwo := by
    rw [show (1 : ℕ) = 0 + 1 from rfl, lowerCentralSeries_succ, lowerCentralSeries_zero,
      LieSubmodule.lie_le_iff]
    intro x _ m _
    exact ⟨rfl, rfl, rfl, rfl⟩
  have h2 : lowerCentralSeries R (DL R) (DL R) 2 ≤ gammaThree := by
    rw [show (2 : ℕ) = 1 + 1 from rfl, lowerCentralSeries_succ]
    refine (LieSubmodule.mono_lie_right _ h1).trans ?_
    rw [LieSubmodule.lie_le_iff]
    rintro x _ m ⟨m0, m1, m2, m3⟩
    refine ⟨rfl, rfl, rfl, rfl, ?_, ?_⟩ <;> simp [m0, m1, m2, m3]
  rw [eq_bot_iff, show (3 : ℕ) = 2 + 1 from rfl, lowerCentralSeries_succ]
  refine (LieSubmodule.mono_lie_right _ h2).trans ?_
  rw [LieSubmodule.lie_le_iff]
  rintro x _ m ⟨m0, m1, m2, m3, m4, m5⟩
  rw [LieSubmodule.mem_bot]
  apply ext8 <;> simp [m0, m1, m2, m3, m4, m5]

end Nilpotent

section Group

variable {p : ℕ} [Fact p.Prime] [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)]

variable (p) in
/-- The Lazard (class-three BCH) group of `DL (ZMod p)`. -/
abbrev DLGroup : Type := BCH (ZMod p) (DL (ZMod p)) lcs_three_eq_bot

theorem map_comm (f : DLGroup p →* DLGroup p) (x y : DLGroup p) :
    f (comm x y) = comm (f x) (f y) := by
  simp [BCHClassThreeSubgroups.comm, map_mul, map_inv]

theorem map_powerScalar (f : DLGroup p →* DLGroup p) (t : ZMod p) (x : DLGroup p) :
    f (powerScalar t x) = powerScalar t (f x) := by
  simp [powerScalar, map_pow]

theorem map_bracketWord (f : DLGroup p →* DLGroup p) (x y : DLGroup p) :
    f (bracketWord x y) = bracketWord (f x) (f y) := by
  simp only [bracketWord, map_mul, map_comm, map_powerScalar]

theorem map_addWord (f : DLGroup p →* DLGroup p) (x y : DLGroup p) :
    f (addWord x y) = addWord (f x) (f y) := by
  simp only [addWord, map_mul, map_comm, map_powerScalar, map_bracketWord]

/-- The map of logarithms induced by a group endomorphism. -/
def toLieMap (f : DLGroup p →* DLGroup p) (x : DL (ZMod p)) : DL (ZMod p) :=
  (f (BCH.mk x)).val

theorem toLieMap_add (f : DLGroup p →* DLGroup p) (x y : DL (ZMod p)) :
    toLieMap f (x + y) = toLieMap f x + toLieMap f y := by
  have h : (BCH.mk (x + y) : DLGroup p) = addWord (BCH.mk x) (BCH.mk y) :=
    BCH.ext (val_addWord (BCH.mk x) (BCH.mk y)).symm
  rw [toLieMap, h, map_addWord, val_addWord]
  rfl

theorem toLieMap_smul (f : DLGroup p →* DLGroup p) (t : ZMod p) (x : DL (ZMod p)) :
    toLieMap f (t • x) = t • toLieMap f x := by
  have h : (BCH.mk (t • x) : DLGroup p) = powerScalar t (BCH.mk x) :=
    BCH.ext (val_powerScalar t (BCH.mk x)).symm
  rw [toLieMap, h, map_powerScalar, val_powerScalar]
  rfl

theorem toLieMap_lie (f : DLGroup p →* DLGroup p) (x y : DL (ZMod p)) :
    toLieMap f ⁅x, y⁆ = ⁅toLieMap f x, toLieMap f y⁆ := by
  have h : (BCH.mk ⁅x, y⁆ : DLGroup p) = bracketWord (BCH.mk x) (BCH.mk y) :=
    BCH.ext (val_bracketWord (BCH.mk x) (BCH.mk y)).symm
  rw [toLieMap, h, map_bracketWord, val_bracketWord]
  rfl

/-- A group automorphism of the Lazard group is a Lie automorphism of its logarithm,
derived from the explicit power and commutator words. -/
def toLieEquiv (f : DLGroup p ≃* DLGroup p) : DL (ZMod p) ≃ₗ⁅ZMod p⁆ DL (ZMod p) where
  toFun := toLieMap f.toMonoidHom
  map_add' := toLieMap_add _
  map_smul' := toLieMap_smul _
  map_lie' := toLieMap_lie _ _ _
  invFun := toLieMap f.symm.toMonoidHom
  left_inv x := by
    simp only [toLieMap, MulEquiv.coe_toMonoidHom]
    have : (BCH.mk (f (BCH.mk x)).val : DLGroup p) = f (BCH.mk x) := rfl
    rw [this, MulEquiv.symm_apply_apply]
  right_inv x := by
    simp only [toLieMap, MulEquiv.coe_toMonoidHom]
    have : (BCH.mk (f.symm (BCH.mk x)).val : DLGroup p) = f.symm (BCH.mk x) := rfl
    rw [this, MulEquiv.apply_symm_apply]

theorem toLieEquiv_apply (f : DLGroup p ≃* DLGroup p) (x : DL (ZMod p)) :
    toLieEquiv f x = (f (BCH.mk x)).val := rfl

omit [NeZero (3 : ZMod p)] in
/-- `bch a b = bch b a + [a, b]`. -/
theorem bch_comm (a b : DL (ZMod p)) :
    bch (F := ZMod p) a b = bch (F := ZMod p) b a + ⁅a, b⁆ := by
  have hs : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [bch, hs, lie_neg]
  match_scalars <;> field_simp [NeZero.ne (2 : ZMod p)]
  all_goals ring

/-- The centre of the Lazard group is `exp` of the centre of the Lie algebra. -/
theorem mem_center_iff_val (z : DLGroup p) :
    z ∈ Subgroup.center (DLGroup p) ↔ z.val ∈ LieAlgebra.center (ZMod p) (DL (ZMod p)) := by
  rw [Subgroup.mem_center_iff, LieAlgebra.center, LieModule.mem_maxTrivSubmodule]
  constructor
  · intro h x
    have hx := congrArg BCH.val (h (BCH.mk x))
    rw [val_mul, val_mul, bch_comm] at hx
    simpa using hx
  · intro h g
    apply BCH.ext
    rw [val_mul, val_mul, bch_comm, h g.val, add_zero]

/-- **Proposition `prop:dl-central-scalars`** (group part). For a prime `p > 3` (encoded
by `2, 3 ≠ 0` in `ZMod p`), some automorphism of the Lazard group of `DL (ZMod p)` acts on
its centre as `z ↦ z ^ ζ` if and only if `ζ = ±1`. -/
theorem group_center_pow_iff (ζ : ZMod p) :
    (∃ f : DLGroup p ≃* DLGroup p, ∀ z ∈ Subgroup.center (DLGroup p), f z = z ^ ζ.val) ↔
      ζ = 1 ∨ ζ = -1 := by
  have h2 : (2 : ZMod p) ≠ 0 := NeZero.ne 2
  constructor
  · rintro ⟨f, hf⟩
    rw [← exists_aut_center_smul_iff h2]
    refine ⟨toLieEquiv f, fun z hz => ?_⟩
    have hz' : (BCH.mk z : DLGroup p) ∈ Subgroup.center (DLGroup p) :=
      (mem_center_iff_val _).mpr hz
    have h := congrArg BCH.val (hf _ hz')
    rw [val_pow, ZMod.natCast_zmod_val] at h
    rw [toLieEquiv_apply, h]
  · intro h
    obtain ⟨φ, hφ⟩ := (exists_aut_center_smul_iff h2 ζ).mpr h
    refine ⟨lieEquiv lcs_three_eq_bot lcs_three_eq_bot φ, fun z hz => ?_⟩
    apply BCH.ext
    rw [val_pow, ZMod.natCast_zmod_val]
    exact hφ _ ((mem_center_iff_val z).mp hz)

/-- The same with an integer exponent: some automorphism of the Lazard group acts on its
centre as `z ↦ z ^ k` if and only if `k ≡ ±1 (mod p)`. -/
theorem group_center_zpow_iff (k : ℤ) :
    (∃ f : DLGroup p ≃* DLGroup p, ∀ z ∈ Subgroup.center (DLGroup p), f z = z ^ k) ↔
      (k : ZMod p) = 1 ∨ (k : ZMod p) = -1 := by
  rw [← group_center_pow_iff]
  have key : ∀ z : DLGroup p, z ^ k = z ^ (k : ZMod p).val := by
    intro z
    apply BCH.ext
    rw [val_zpow, val_pow, ZMod.natCast_zmod_val]
  simp only [key]

end Group

end QSearch.DixmierLister
