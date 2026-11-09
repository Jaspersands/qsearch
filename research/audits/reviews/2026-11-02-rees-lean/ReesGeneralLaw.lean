import Formal.ReesLeanExt.ReesGeneralCover
import Mathlib.Algebra.Group.MinimalAxioms
import Mathlib.GroupTheory.Subgroup.Center

/-!
# General-class Rees composition, conditional on a natural group law

Item 8 of `research/REES_FULL_CAMPAIGN.md`, targets (b) and (c).

The general-class BCH/Lazard transport is NOT proved here. It is isolated as
an explicit hypothesis, `NilpotentGroupLaw F c`: one binary operation on every
Lie algebra over `F` (in a fixed universe) that is

* natural in Lie homomorphisms (`φ (x ⋆ y) = φ x ⋆ φ y`), and
* a group law with identity `0` and inverse `-x` on algebras of class at most
  `c` (`lowerCentralSeries F M M c = ⊥`).

The degree-`c` truncated BCH product is the intended instance for `c < p`
(core report §1.2(a)); its construction and these two properties are the
Lazard input that stays outside Lean. Two further optional properties of the
BCH product are separate hypotheses: `AdditiveOnCommuting` (the product of
Lie-commuting elements is their sum) and `SubgroupsAreSubalgebras` (Lazard's
subgroup → Lie subring direction).

From these hypotheses alone, everything else is proved for every class `c`:

* (b) `tuple_hides`, `tuple_hides_coeff`, `tuple_hides_arbitrary_subgroup`:
  the tuple oracle `(f(E_{s_i} a))_i` hides exactly `exp h̃`; the hidden
  subgroup is closed, dilation-invariant (`dilation_hiddenSubgroup_iff`) and
  independent of the admissible points (`hiddenSubgroup_eq`);
* group-level cover facts: `evaluationHom_surjective`,
  `evaluationHom_comp_dilation` (`E_s ∘ δ_u = E_{u s}`),
  `evaluationHom_image_hiddenSubgroup` (`E_s(exp h̃) = H`);
* (c) the central-quotient tower in general class: `groupMk`, its kernel
  (`groupMk_ker`), the centrality of each step kernel in the GROUP
  (`projectHom_kernel_central`), additivity of the law on that kernel
  (`projectHom_kernel_additive`), the terminal group as additive `L`
  (`terminalGroupEquiv`), and retention of all of `h` at the terminal quotient
  (`terminal_hidden_image`).

The quantum part of step 2 (`CentralCharacterDescent` etc.) is already stated
for arbitrary groups in `formal/`; this file supplies the general-class groups
it is applied to.
-/

universe u

namespace QSearch.ReesGeneralLaw

open LieModule QSearch.ReesLieConstruction QSearch.ReesLieInterpolation
  QSearch.ReesHomogenization QSearch.ReesCentralQuotient QSearch.ReesGeneralCover

noncomputable section

set_option backward.isDefEq.respectTransparency false

/-- A natural group law on Lie algebras of class at most `c` (the Lazard input). -/
structure NilpotentGroupLaw (F : Type u) [CommRing F] (c : ℕ) where
  mul : ∀ (M : Type u) [LieRing M] [LieAlgebra F M], M → M → M
  natural : ∀ {M N : Type u} [LieRing M] [LieAlgebra F M] [LieRing N] [LieAlgebra F N]
    (φ : M →ₗ⁅F⁆ N) (x y : M), φ (mul M x y) = mul N (φ x) (φ y)
  mul_assoc : ∀ (M : Type u) [LieRing M] [LieAlgebra F M],
    lowerCentralSeries F M M c = ⊥ → ∀ x y z : M, mul M (mul M x y) z = mul M x (mul M y z)
  zero_mul : ∀ (M : Type u) [LieRing M] [LieAlgebra F M] (x : M), mul M 0 x = x
  neg_mul : ∀ (M : Type u) [LieRing M] [LieAlgebra F M] (x : M), mul M (-x) x = 0

variable {F : Type u} [CommRing F] {c : ℕ}

/-- The BCH property that Lie-commuting elements multiply by addition. -/
def AdditiveOnCommuting (law : NilpotentGroupLaw F c) : Prop :=
  ∀ (M : Type u) [LieRing M] [LieAlgebra F M] (x y : M), ⁅x, y⁆ = 0 → law.mul M x y = x + y

/-- The group carried by a Lie algebra of class at most `c`. -/
structure LawGroup (law : NilpotentGroupLaw F c) (M : Type u) [LieRing M] [LieAlgebra F M]
    (hM : lowerCentralSeries F M M c = ⊥) where
  val : M

variable {law : NilpotentGroupLaw F c}

section Groups

variable {M N K : Type u} [LieRing M] [LieAlgebra F M] [LieRing N] [LieAlgebra F N]
  [LieRing K] [LieAlgebra F K]
  {hM : lowerCentralSeries F M M c = ⊥} {hN : lowerCentralSeries F N N c = ⊥}
  {hK : lowerCentralSeries F K K c = ⊥}

@[ext] theorem LawGroup.ext {x y : LawGroup law M hM} (h : x.val = y.val) : x = y := by
  cases x; cases y; cases h; rfl

instance : Mul (LawGroup law M hM) := ⟨fun x y => ⟨law.mul M x.val y.val⟩⟩
instance : One (LawGroup law M hM) := ⟨⟨0⟩⟩
instance : Inv (LawGroup law M hM) := ⟨fun x => ⟨-x.val⟩⟩

@[simp] theorem val_mul (x y : LawGroup law M hM) : (x * y).val = law.mul M x.val y.val := rfl
@[simp] theorem val_one : (1 : LawGroup law M hM).val = 0 := rfl
@[simp] theorem val_inv (x : LawGroup law M hM) : x⁻¹.val = -x.val := rfl

instance instGroup : Group (LawGroup law M hM) :=
  Group.ofLeftAxioms
    (fun x y z => LawGroup.ext (law.mul_assoc M hM x.val y.val z.val))
    (fun x => LawGroup.ext (law.zero_mul M x.val))
    (fun x => LawGroup.ext (law.neg_mul M x.val))

/-- Every Lie homomorphism is a group homomorphism of the law groups. -/
def lawHom (hM : lowerCentralSeries F M M c = ⊥) (hN : lowerCentralSeries F N N c = ⊥)
    (φ : M →ₗ⁅F⁆ N) : LawGroup law M hM →* LawGroup law N hN where
  toFun x := ⟨φ x.val⟩
  map_one' := LawGroup.ext (map_zero φ)
  map_mul' x y := LawGroup.ext (law.natural φ x.val y.val)

@[simp] theorem lawHom_val (φ : M →ₗ⁅F⁆ N) (x : LawGroup law M hM) :
    (lawHom hM hN φ x).val = φ x.val := rfl

theorem lawHom_surjective (φ : M →ₗ⁅F⁆ N) (hφ : Function.Surjective φ) :
    Function.Surjective (lawHom (law := law) hM hN φ) := by
  intro y
  obtain ⟨x, hx⟩ := hφ y.val
  exact ⟨⟨x⟩, LawGroup.ext hx⟩

/-- Every Lie equivalence is a group isomorphism of the law groups. -/
def lawEquiv (hM : lowerCentralSeries F M M c = ⊥) (hN : lowerCentralSeries F N N c = ⊥)
    (e : M ≃ₗ⁅F⁆ N) : LawGroup law M hM ≃* LawGroup law N hN where
  toFun := lawHom hM hN e.toLieHom
  invFun := lawHom hN hM e.symm.toLieHom
  left_inv x := LawGroup.ext (e.symm_apply_apply x.val)
  right_inv x := LawGroup.ext (e.apply_symm_apply x.val)
  map_mul' := (lawHom hM hN e.toLieHom).map_mul

@[simp] theorem lawEquiv_val (e : M ≃ₗ⁅F⁆ N) (x : LawGroup law M hM) :
    (lawEquiv hM hN e x).val = e x.val := rfl

/-- Naturality alone closes every Lie subalgebra under the law. -/
def subgroupOfLie (hM : lowerCentralSeries F M M c = ⊥) (h : LieSubalgebra F M) :
    Subgroup (LawGroup law M hM) where
  carrier := {x | x.val ∈ h}
  one_mem' := h.zero_mem
  mul_mem' := by
    intro x y hx hy
    change law.mul M x.val y.val ∈ h
    have hn := law.natural h.incl ⟨x.val, hx⟩ ⟨y.val, hy⟩
    change _ = law.mul M x.val y.val at hn
    rw [← hn]
    exact (law.mul h ⟨x.val, hx⟩ ⟨y.val, hy⟩).property
  inv_mem' := fun hx => h.neg_mem hx

@[simp] theorem mem_subgroupOfLie (h : LieSubalgebra F M) (x : LawGroup law M hM) :
    x ∈ subgroupOfLie (law := law) hM h ↔ x.val ∈ h := Iff.rfl

theorem comap_subgroupOfLie (φ : M →ₗ⁅F⁆ N) (h : LieSubalgebra F N) (x : LawGroup law M hM) :
    x ∈ (subgroupOfLie (law := law) hN h).comap (lawHom hM hN φ) ↔ φ x.val ∈ h := Iff.rfl

/-- Lazard's subgroup → Lie subring direction, as a property of the law. -/
def SubgroupsAreSubalgebras (law : NilpotentGroupLaw F c) : Prop :=
  ∀ (M : Type u) [LieRing M] [LieAlgebra F M] (hM : lowerCentralSeries F M M c = ⊥)
    (H : Subgroup (LawGroup law M hM)), ∃ h : LieSubalgebra F M, H = subgroupOfLie hM h

/-- Under `AdditiveOnCommuting`, Lie-commuting elements commute in the group,
and their product is their sum. -/
theorem mul_eq_add_of_lie_eq_zero (hadd : AdditiveOnCommuting law)
    (x y : LawGroup law M hM) (hxy : ⁅x.val, y.val⁆ = 0) :
    (x * y).val = x.val + y.val ∧ x * y = y * x := by
  have hyx : ⁅y.val, x.val⁆ = 0 := by rw [← lie_skew, hxy, neg_zero]
  refine ⟨hadd M _ _ hxy, LawGroup.ext ?_⟩
  change law.mul M x.val y.val = law.mul M y.val x.val
  rw [hadd M _ _ hxy, hadd M _ _ hyx, add_comm]

end Groups

/-! ## The general-class Rees group and its tuple oracle -/

section Rees

variable {L : Type u} [LieRing L] [LieAlgebra F L]

abbrev ReesGroup (law : NilpotentGroupLaw F c) (hnil : lowerCentralSeries F L L c = ⊥) :=
  LawGroup law (rees (R := F) (L := L)) (rees_class_bound c hnil)

abbrev BaseGroup (law : NilpotentGroupLaw F c) (hnil : lowerCentralSeries F L L c = ⊥) :=
  LawGroup law L hnil

variable (hnil : lowerCentralSeries F L L c = ⊥)

/-- `E_s` as a group homomorphism `G̃ → G`. -/
def evaluationHom (s : F) : ReesGroup law hnil →* BaseGroup law hnil :=
  lawHom _ hnil (evaluation s)

@[simp] theorem evaluationHom_val (s : F) (x : ReesGroup law hnil) :
    (evaluationHom hnil s x).val = evaluation s x.val := rfl

/-- `δ_u` as a group automorphism of `G̃`. -/
def dilationHom (u : Fˣ) : ReesGroup law hnil ≃* ReesGroup law hnil :=
  lawEquiv _ _ (dilation u)

theorem evaluationHom_surjective {s : F} (hs : IsUnit s) :
    Function.Surjective (evaluationHom (law := law) hnil s) :=
  lawHom_surjective _ (evaluation_surjective hs)

/-- `E_s ∘ δ_u = E_{u s}` on the group. -/
theorem evaluationHom_comp_dilation (s : F) (u : Fˣ) :
    (evaluationHom (law := law) hnil s).comp (dilationHom hnil u).toMonoidHom =
      evaluationHom hnil ((u : F) * s) := by
  ext x
  exact evaluation_comp_dilation s u x.val

/-- `exp h̃`, a subgroup of `G̃` by naturality. -/
def hiddenSubgroup (h : LieSubalgebra F L) (points : Fin c → F) :
    Subgroup (ReesGroup law hnil) :=
  subgroupOfLie _ (hiddenCover h points)

/-- `exp h̃ = ∩_i E_{s_i}^{-1}(exp h)` as subgroups. -/
theorem hiddenSubgroup_eq_iInf (h : LieSubalgebra F L) (points : Fin c → F) :
    hiddenSubgroup (law := law) hnil h points =
      ⨅ i, (subgroupOfLie hnil h).comap (evaluationHom hnil (points i)) := by
  ext x
  simp only [Subgroup.mem_iInf]
  rfl

theorem mem_hiddenSubgroup_iff_coeff (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (x : ReesGroup law hnil) :
    x ∈ hiddenSubgroup hnil h points ↔ ∀ r, coeff (x.val : Current F L) r ∈ h :=
  mem_hiddenCover_iff_coeff hnil h points invertible x.val

theorem hiddenSubgroup_eq (h : LieSubalgebra F L) (points points' : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (invertible' : IsUnit (evaluationMatrix points').det) :
    hiddenSubgroup (law := law) hnil h points = hiddenSubgroup hnil h points' := by
  simp only [hiddenSubgroup, hiddenCover_eq hnil h points points' invertible invertible']

/-- (b) The general-class tuple criterion: the ordered tuple of original
oracle values hides exactly `exp h̃`. No invertibility is needed here. -/
theorem tuple_hides {O : Type*} (h : LieSubalgebra F L) (points : Fin c → F)
    (f : BaseGroup law hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ subgroupOfLie hnil h)
    (a b : ReesGroup law hnil) :
    (fun i => f (evaluationHom hnil (points i) a)) =
        (fun i => f (evaluationHom hnil (points i) b)) ↔
      a⁻¹ * b ∈ hiddenSubgroup hnil h points := by
  rw [funext_iff]
  apply forall_congr'
  intro i
  rw [hides, ← map_inv, ← map_mul]
  rfl

/-- The same criterion in coefficients: every coefficient of `a⁻¹ ⋆ b` lies in `h`. -/
theorem tuple_hides_coeff {O : Type*} (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det)
    (f : BaseGroup law hnil → O)
    (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ subgroupOfLie hnil h)
    (a b : ReesGroup law hnil) :
    (fun i => f (evaluationHom hnil (points i) a)) =
        (fun i => f (evaluationHom hnil (points i) b)) ↔
      ∀ r, coeff ((a⁻¹ * b).val : Current F L) r ∈ h := by
  rw [tuple_hides hnil h points f hides, mem_hiddenSubgroup_iff_coeff hnil h points invertible]

/-- For an ARBITRARY subgroup `H` of `G`, given Lazard's subgroup direction:
the tuple oracle hides `exp h̃` for `h = log H`. -/
theorem tuple_hides_arbitrary_subgroup {O : Type*} (lazard : SubgroupsAreSubalgebras law)
    (H : Subgroup (BaseGroup law hnil)) (points : Fin c → F)
    (f : BaseGroup law hnil → O) (hides : ∀ x y, f x = f y ↔ x⁻¹ * y ∈ H) :
    ∃ h : LieSubalgebra F L, H = subgroupOfLie hnil h ∧
      ∀ a b : ReesGroup law hnil,
        (fun i => f (evaluationHom hnil (points i) a)) =
            (fun i => f (evaluationHom hnil (points i) b)) ↔
          a⁻¹ * b ∈ hiddenSubgroup hnil h points := by
  obtain ⟨h, rfl⟩ := lazard L hnil H
  exact ⟨h, rfl, tuple_hides hnil h points f hides⟩

/-- Every unit dilation preserves `exp h̃`. -/
theorem dilation_hiddenSubgroup_iff (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) (u : Fˣ) (x : ReesGroup law hnil) :
    dilationHom hnil u x ∈ hiddenSubgroup hnil h points ↔ x ∈ hiddenSubgroup hnil h points :=
  dilation_mem_iff hnil h points invertible u x.val

/-- `E_s(exp h̃) = exp h` for every unit `s`. -/
theorem evaluationHom_image_hiddenSubgroup (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) {s : F} (hs : IsUnit s) :
    (hiddenSubgroup (law := law) hnil h points).map (evaluationHom hnil s) =
      subgroupOfLie hnil h := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact (mem_hiddenCover_iff_forall_eval hnil h points invertible x.val).mp hx s
  · intro hy
    have hy' : y.val ∈ (evaluation s) '' (hiddenCover h points : Set _) := by
      rw [evaluation_image_hiddenCover hnil h points invertible hs]
      exact hy
    obtain ⟨z, hz, hzy⟩ := hy'
    exact ⟨⟨z⟩, hz, LawGroup.ext hzy⟩

end Rees

/-! ## (c) The general-class central-quotient tower -/

section Tower

variable {L : Type u} [LieRing L] [LieAlgebra F L]

theorem trunc_class_le {d : ℕ} (hd : d ≤ c) :
    lowerCentralSeries F (Trunc (R := F) (L := L) d) (Trunc (R := F) (L := L) d) c = ⊥ :=
  eq_bot_iff.mpr ((antitone_lowerCentralSeries F _ _ hd).trans
    (trunc_class_bound (R := F) (L := L) d).le)

/-- The group of the actual Lie quotient `A / F_{>d}`, for `d ≤ c`. -/
abbrev TruncGroup (law : NilpotentGroupLaw F c) (d : ℕ) (hd : d ≤ c) :=
  LawGroup law (Trunc (R := F) (L := L) d) (trunc_class_le hd)

def groupMk (hnil : lowerCentralSeries F L L c = ⊥) (d : ℕ) (hd : d ≤ c) :
    ReesGroup law hnil →* TruncGroup (L := L) law d hd :=
  lawHom _ _ (mk d)

theorem groupMk_surjective (hnil : lowerCentralSeries F L L c = ⊥) (d : ℕ) (hd : d ≤ c) :
    Function.Surjective (groupMk (law := law) hnil d hd) :=
  lawHom_surjective _ (mk_surjective d)

theorem groupMk_ker (hnil : lowerCentralSeries F L L c = ⊥) (d : ℕ) (hd : d ≤ c)
    (x : ReesGroup law hnil) : x ∈ (groupMk hnil d hd).ker ↔ x.val ∈ tail d := by
  rw [MonoidHom.mem_ker]
  constructor
  · intro hx
    exact (mk_eq_zero d x.val).mp (congrArg LawGroup.val hx)
  · intro hx
    exact LawGroup.ext ((mk_eq_zero d x.val).mpr hx)

def projectHom {d e : ℕ} (hd : d ≤ c) (he : e ≤ c) (h : e ≤ d) :
    TruncGroup (L := L) law d hd →* TruncGroup (L := L) law e he :=
  lawHom _ _ (projection h)

theorem projectHom_surjective {d e : ℕ} (hd : d ≤ c) (he : e ≤ c) (h : e ≤ d) :
    Function.Surjective (projectHom (L := L) (law := law) hd he h) :=
  lawHom_surjective _ (projection_surjective h)

theorem projectHom_groupMk (hnil : lowerCentralSeries F L L c = ⊥)
    {d e : ℕ} (hd : d ≤ c) (he : e ≤ c) (h : e ≤ d) :
    (projectHom hd he h).comp (groupMk (law := law) hnil d hd) = groupMk hnil e he := by
  ext x
  rfl

/-- Each step kernel is central in the GROUP `G̃_{d+1}`, given only that the law
is additive on Lie-commuting pairs. -/
theorem projectHom_kernel_central (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c)
    (x : TruncGroup (L := L) law (d + 1) hd)
    (hx : x ∈ (projectHom hd (by omega) (Nat.le_succ d)).ker) :
    x ∈ Subgroup.center (TruncGroup (L := L) law (d + 1) hd) := by
  rw [Subgroup.mem_center_iff]
  intro y
  have hxv : projection (Nat.le_succ d) x.val = 0 := congrArg LawGroup.val hx
  exact (mul_eq_add_of_lie_eq_zero hadd y x (top_kernel_central d y.val x.val hxv)).2

/-- On each step kernel the group law is the vector addition of `L`'s top grade:
the kernel is elementary abelian when `L` is an `F_p`-space. -/
theorem projectHom_kernel_additive (hadd : AdditiveOnCommuting law) (d : ℕ) (hd : d + 1 ≤ c)
    (x y : TruncGroup (L := L) law (d + 1) hd)
    (hy : y ∈ (projectHom hd (by omega) (Nat.le_succ d)).ker) :
    (x * y).val = x.val + y.val := by
  have hyv : projection (Nat.le_succ d) y.val = 0 := congrArg LawGroup.val hy
  exact (mul_eq_add_of_lie_eq_zero hadd x y (top_kernel_central d x.val y.val hyv)).1

/-- The terminal group `G̃_1` is additive `L` (not `L` with its own law). -/
def terminalGroupEquiv (hadd : AdditiveOnCommuting law) (hc : 1 ≤ c) :
    TruncGroup (L := L) law 1 hc ≃* Multiplicative L where
  toFun x := Multiplicative.ofAdd (terminalEquiv x.val)
  invFun x := ⟨terminalEquiv.symm x.toAdd⟩
  left_inv x := LawGroup.ext (terminalEquiv.symm_apply_apply x.val)
  right_inv x := terminalEquiv.apply_symm_apply x.toAdd
  map_mul' x y := by
    change terminalEquiv (law.mul _ x.val y.val) = terminalEquiv x.val + terminalEquiv y.val
    rw [hadd _ _ _ (terminal_bracket x.val y.val), map_add]

def terminalMap (hadd : AdditiveOnCommuting law) (hnil : lowerCentralSeries F L L c = ⊥)
    (hc : 1 ≤ c) : ReesGroup law hnil →* Multiplicative L :=
  (terminalGroupEquiv hadd hc).toMonoidHom.comp (groupMk hnil 1 hc)

@[simp] theorem terminalMap_apply (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (hc : 1 ≤ c) (x : ReesGroup law hnil) :
    terminalMap hadd hnil hc x = Multiplicative.ofAdd (ReesCentralQuotient.coefficient 1 x.val) := rfl

/-- In general class, the terminal hidden image retains all of `h`, including
its derived directions. -/
theorem terminal_hidden_image (hadd : AdditiveOnCommuting law)
    (hnil : lowerCentralSeries F L L c = ⊥) (hc : 1 ≤ c)
    (h : LieSubalgebra F L) (points : Fin c → F)
    (invertible : IsUnit (evaluationMatrix points).det) :
    (hiddenSubgroup (law := law) hnil h points).map (terminalMap hadd hnil hc) =
      h.toSubmodule.toAddSubgroup.toSubgroup := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    change ReesCentralQuotient.coefficient 1 x.val ∈ h
    exact (mem_hiddenSubgroup_iff_coeff hnil h points invertible x).mp hx 1
  · intro hy
    change y.toAdd ∈ h at hy
    refine ⟨⟨gradeOne y.toAdd⟩, ?_, ?_⟩
    · exact (gradeOne_mem_hiddenCover_iff hnil h points invertible y.toAdd).mpr hy
    · change Multiplicative.ofAdd (ReesCentralQuotient.coefficient 1 (gradeOne (R := F) y.toAdd)) = y
      rw [coefficient_gradeOne, Finsupp.single_eq_same]
      rfl

/-- Dilations descend to every truncated group. -/
def groupDilation (d : ℕ) (hd : d ≤ c) (u : Fˣ) :
    TruncGroup (L := L) law d hd ≃* TruncGroup (L := L) law d hd :=
  lawEquiv _ _ (quotientDilation d u)

end Tower

end
end QSearch.ReesGeneralLaw
