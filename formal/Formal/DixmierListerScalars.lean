import Mathlib

/-!
# Central scalars of the Dixmier–Lister algebra

Source: `research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/core/main-core.tex`,
Section `sec:dixmier-lister` and Proposition `prop:dl-central-scalars`.

`DL R` is the eight-dimensional algebra of the paper over a commutative ring `R`, given
by its structure constants in the basis `e₁,…,e₈` (Lean indices `0,…,7`). The bracket is
defined coordinate by coordinate from the paper's table; Jacobi (in Mathlib's Leibniz
form), bilinearity and `⁅x, x⁆ = 0` are proved, so `DL R` is an actual Mathlib
`LieRing` and `LieAlgebra R`. `table` and `table_zero` check every bracket of two basis
vectors against the table, and `mem_center_iff` identifies the centre with
`span(e₇, e₈)`.

The main theorem `exists_aut_center_smul_iff` is the proposition: over a field `K` with
`2 ≠ 0`, some Lie algebra automorphism of `DL K` acts on the centre as multiplication by
`ζ` if and only if `ζ = 1` or `ζ = -1`. (The paper takes `ζ ∈ K^×`; here `ζ ∈ K`, and
`ζ = 0` is excluded on both sides.)

The proof follows the paper. Over a field containing `i` with `i² = -1`
(`scalar_core`) we use the paper's vectors `u₁,…,u₄, v_±` and the coordinates
`C₁,…,C₄` of the `u`-components. The bracket identities give the vanishing cross
minors and eight coefficient equations (`core_alg`); surjectivity gives the
nondegeneracy `det A ≠ 0` of the `4 × 4` matrix `A` of the induced map on
`L / γ₂`. A Laplace expansion along the `U₊` rows then splits into the keep case
(`A` preserves `U₊` and `U₋`, ending with `ζ = 1`, `keep_final`) and the swap case
(`A` exchanges them, ending with `ζ = -1`, `swap_final`). The paper's rank-one-locus
argument is replaced by this determinant argument; the coefficient comparisons
(`ζ = det P · μ`, `ζ = μ ν`, and so on) are the paper's.

For a general field, an automorphism is base-changed along `K → AlgebraicClosure K`
by its matrix (`bc`), which is again a bracket-preserving surjection (`bc_lie`,
`bc_surj`). This is the paper's "we may assume that `K` is algebraically closed".
The converse uses the identity and the paper's sign automorphism `signEquiv`
(`+` on `e₁, e₃, e₆`, `-` on the other five).

The group-level "in particular" (automorphisms of the Lazard group over `F_p`, `p > 3`)
is `QSearch.DixmierLister.group_center_pow_iff` in `Formal/DixmierListerGroup.lean`,
through the class-three BCH group of `Formal/BCHClassThree.lean`.
-/

namespace QSearch.DixmierLister

/-- The Dixmier–Lister algebra over `R`: coordinates in the basis `e₁,…,e₈`
(Lean indices `0,…,7`). A type synonym, so that no `Pi` Lie structure applies. -/
def DL (R : Type*) : Type _ := Fin 8 → R

section Ring

variable {R : Type*} [CommRing R]

instance : AddCommGroup (DL R) := inferInstanceAs (AddCommGroup (Fin 8 → R))
instance : Module R (DL R) := inferInstanceAs (Module R (Fin 8 → R))

@[simp] theorem add_apply (x y : DL R) (k : Fin 8) : (x + y) k = x k + y k := rfl
@[simp] theorem sub_apply (x y : DL R) (k : Fin 8) : (x - y) k = x k - y k := rfl
@[simp] theorem neg_apply (x : DL R) (k : Fin 8) : (-x) k = -x k := rfl
@[simp] theorem zero_apply (k : Fin 8) : (0 : DL R) k = 0 := rfl
@[simp] theorem smul_apply (t : R) (x : DL R) (k : Fin 8) : (t • x) k = t * x k := rfl

omit [CommRing R] in
theorem ext8 {x y : DL R} (h0 : x 0 = y 0) (h1 : x 1 = y 1) (h2 : x 2 = y 2)
    (h3 : x 3 = y 3) (h4 : x 4 = y 4) (h5 : x 5 = y 5) (h6 : x 6 = y 6)
    (h7 : x 7 = y 7) : x = y := by
  funext k
  fin_cases k <;> assumption

/-- The bracket of the paper's table, coordinate by coordinate:
`[e₁,e₂] = e₅, [e₁,e₃] = e₆, [e₁,e₄] = e₇, [e₁,e₅] = -e₈, [e₂,e₃] = e₈,
[e₂,e₄] = e₆, [e₂,e₆] = -e₇, [e₃,e₄] = -e₅, [e₃,e₅] = -e₇, [e₄,e₆] = -e₈`. -/
def br (x y : DL R) : DL R :=
  ![0, 0, 0, 0,
    (x 0 * y 1 - x 1 * y 0) - (x 2 * y 3 - x 3 * y 2),
    (x 0 * y 2 - x 2 * y 0) + (x 1 * y 3 - x 3 * y 1),
    (x 0 * y 3 - x 3 * y 0) - (x 1 * y 5 - x 5 * y 1) - (x 2 * y 4 - x 4 * y 2),
    -(x 0 * y 4 - x 4 * y 0) + (x 1 * y 2 - x 2 * y 1) - (x 3 * y 5 - x 5 * y 3)]

instance : Bracket (DL R) (DL R) := ⟨br⟩

@[simp] theorem lie_apply_0 (x y : DL R) : ⁅x, y⁆ 0 = 0 := rfl
@[simp] theorem lie_apply_1 (x y : DL R) : ⁅x, y⁆ 1 = 0 := rfl
@[simp] theorem lie_apply_2 (x y : DL R) : ⁅x, y⁆ 2 = 0 := rfl
@[simp] theorem lie_apply_3 (x y : DL R) : ⁅x, y⁆ 3 = 0 := rfl
@[simp] theorem lie_apply_4 (x y : DL R) :
    ⁅x, y⁆ 4 = (x 0 * y 1 - x 1 * y 0) - (x 2 * y 3 - x 3 * y 2) := rfl
@[simp] theorem lie_apply_5 (x y : DL R) :
    ⁅x, y⁆ 5 = (x 0 * y 2 - x 2 * y 0) + (x 1 * y 3 - x 3 * y 1) := rfl
@[simp] theorem lie_apply_6 (x y : DL R) :
    ⁅x, y⁆ 6 = (x 0 * y 3 - x 3 * y 0) - (x 1 * y 5 - x 5 * y 1) - (x 2 * y 4 - x 4 * y 2) :=
  rfl
@[simp] theorem lie_apply_7 (x y : DL R) :
    ⁅x, y⁆ 7 = -(x 0 * y 4 - x 4 * y 0) + (x 1 * y 2 - x 2 * y 1) - (x 3 * y 5 - x 5 * y 3) :=
  rfl

/-- `DL R` is an actual Lie ring: all axioms, Jacobi included, are proved. -/
instance : LieRing (DL R) where
  add_lie x y z := by apply ext8 <;> simp <;> ring
  lie_add x y z := by apply ext8 <;> simp <;> ring
  lie_self x := by apply ext8 <;> simp <;> ring
  leibniz_lie x y z := by apply ext8 <;> simp <;> ring

instance : LieAlgebra R (DL R) where
  lie_smul t x y := by apply ext8 <;> simp <;> ring

/-- The basis vector `e_{j+1}`. -/
def e (j : Fin 8) : DL R := fun k => if k = j then 1 else 0

@[simp] theorem e_apply (j k : Fin 8) : (e j : DL R) k = if k = j then 1 else 0 := rfl

/-- The basis vector `e_{j+1}` over `R`, with `R` explicit. -/
abbrev E (R : Type*) [CommRing R] (j : Fin 8) : DL R := e j

/-- The ten nonzero brackets of the table (Lean indices are one less). -/
theorem table :
    ⁅E R 0, E R 1⁆ = E R 4 ∧ ⁅E R 0, E R 2⁆ = E R 5 ∧ ⁅E R 0, E R 3⁆ = E R 6 ∧
    ⁅E R 0, E R 4⁆ = -E R 7 ∧ ⁅E R 1, E R 2⁆ = E R 7 ∧ ⁅E R 1, E R 3⁆ = E R 5 ∧
    ⁅E R 1, E R 5⁆ = -E R 6 ∧ ⁅E R 2, E R 3⁆ = -E R 4 ∧ ⁅E R 2, E R 4⁆ = -E R 6 ∧
    ⁅E R 3, E R 5⁆ = -E R 7 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> apply ext8 <;> simp

/-- All other brackets of basis vectors with `j < k` vanish. -/
theorem table_zero (j k : Fin 8) (hjk : j < k)
    (h : (j, k) ∉ ({(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 5), (2, 3), (2, 4),
      (3, 5)} : Finset (Fin 8 × Fin 8))) : ⁅E R j, E R k⁆ = 0 := by
  fin_cases j <;> fin_cases k <;> simp at hjk h ⊢ <;> apply ext8 <;> simp

/-- The centre is `span(e₇, e₈)`: the brackets with `e₁` and `e₂` force the other six
coordinates to vanish (any commutative ring). -/
theorem mem_center_iff (z : DL R) :
    z ∈ LieAlgebra.center R (DL R) ↔
      z 0 = 0 ∧ z 1 = 0 ∧ z 2 = 0 ∧ z 3 = 0 ∧ z 4 = 0 ∧ z 5 = 0 := by
  rw [LieAlgebra.center, LieModule.mem_maxTrivSubmodule]
  constructor
  · intro h
    have h0 := h (E R 0)
    have h1 := h (E R 1)
    have a4 := congrFun h0 4; have a5 := congrFun h0 5
    have a6 := congrFun h0 6; have a7 := congrFun h0 7
    have b4 := congrFun h1 4; have b6 := congrFun h1 6
    simp at a4 a5 a6 a7 b4 b6
    exact ⟨b4, a4, a5, a6, a7, b6⟩
  · rintro ⟨h0, h1, h2, h3, h4, h5⟩ x
    apply ext8 <;> simp [h0, h1, h2, h3, h4, h5]

theorem E6_mem_center : E R 6 ∈ LieAlgebra.center R (DL R) := by
  rw [mem_center_iff]; simp

theorem E7_mem_center : E R 7 ∈ LieAlgebra.center R (DL R) := by
  rw [mem_center_iff]; simp

/-- Every element is the combination of the basis vectors with its coordinates. -/
theorem sum_E (x : DL R) : x = ∑ j : Fin 8, x j • E R j := by
  apply ext8 <;> simp [Fin.sum_univ_eight]

/-- The sign of the paper's automorphism: `+` on `e₁, e₃, e₆`, `-` on the others. -/
def sgn : Fin 8 → R := ![1, -1, 1, -1, -1, 1, -1, -1]

/-- The coordinatewise sign map. -/
def sgnMap (x : DL R) : DL R := fun k => sgn k * x k

@[simp] theorem sgnMap_apply (x : DL R) (k : Fin 8) : sgnMap x k = sgn k * x k := rfl

/-- The paper's sign automorphism. It is defined over `ℤ`, hence over every `R`. -/
def signEquiv : DL R ≃ₗ⁅R⁆ DL R where
  toFun := sgnMap
  map_add' x y := by apply ext8 <;> simp [sgn] <;> ring
  map_smul' t x := by apply ext8 <;> simp [sgn]
  map_lie' := by
    intro x y
    apply ext8 <;> simp [sgn] <;> ring
  invFun := sgnMap
  left_inv x := by apply ext8 <;> simp [sgn]
  right_inv x := by apply ext8 <;> simp [sgn]

@[simp] theorem signEquiv_apply (x : DL R) : signEquiv x = sgnMap x := rfl

theorem signEquiv_center (z : DL R) (hz : z ∈ LieAlgebra.center R (DL R)) :
    signEquiv z = (-1 : R) • z := by
  rw [mem_center_iff] at hz
  obtain ⟨h0, h1, h2, h3, h4, h5⟩ := hz
  rw [signEquiv_apply]
  apply ext8 <;> simp [sgn, h0, h1, h2, h3, h4, h5]

end Ring

/-! ### The algebraic core -/

section Algebra

variable {K : Type*} [Field K]

theorem keep_final {m n ζ : K} (h2 : (2 : K) ≠ 0) (hm : m ^ 3 = 8 * ζ)
    (hn : n ^ 3 = 8 * ζ) (hmn : m * n = 4 * ζ) (hm0 : m ≠ 0) : ζ = 1 := by
  have h64 : (64 : K) ≠ 0 := by
    rw [show (64 : K) = 2 ^ 6 by norm_num]; exact pow_ne_zero _ h2
  have hsq : m ^ 2 = 2 * n := by
    have : m * (m ^ 2 - 2 * n) = 0 := by linear_combination hm - 2 * hmn
    exact sub_eq_zero.mp ((mul_eq_zero.mp this).resolve_left hm0)
  have hζ0 : ζ ≠ 0 := by
    rintro rfl
    apply hm0
    exact pow_eq_zero_iff (n := 3) (by norm_num) |>.mp (by rw [hm]; ring)
  have h : (64 : K) * ζ * (ζ - 1) = 0 := by
    have e1 : (m ^ 2) ^ 3 = (m ^ 3) ^ 2 := by ring
    rw [hsq, hm] at e1
    linear_combination -e1 + 8 * hn
  rcases mul_eq_zero.mp h with h | h
  · exact absurd h (mul_ne_zero h64 hζ0)
  · exact sub_eq_zero.mp h

theorem swap_final {r t ζ : K} (h2 : (2 : K) ≠ 0) (hr : r ^ 3 = 8 * ζ)
    (ht : t ^ 3 = 8 * ζ) (hrt : r * t = -(4 * ζ)) (hr0 : r ≠ 0) : ζ = -1 := by
  have h64 : (64 : K) ≠ 0 := by
    rw [show (64 : K) = 2 ^ 6 by norm_num]; exact pow_ne_zero _ h2
  have hsq : r ^ 2 = -(2 * t) := by
    have : r * (r ^ 2 + 2 * t) = 0 := by linear_combination hr + 2 * hrt
    exact eq_neg_of_add_eq_zero_left ((mul_eq_zero.mp this).resolve_left hr0)
  have hζ0 : ζ ≠ 0 := by
    rintro rfl
    apply hr0
    exact pow_eq_zero_iff (n := 3) (by norm_num) |>.mp (by rw [hr]; ring)
  have h : (64 : K) * ζ * (ζ + 1) = 0 := by
    have e1 : (r ^ 2) ^ 3 = (r ^ 3) ^ 2 := by ring
    rw [hsq, hr] at e1
    linear_combination -e1 - 8 * ht
  rcases mul_eq_zero.mp h with h | h
  · exact absurd h (mul_ne_zero h64 hζ0)
  · exact eq_neg_of_add_eq_zero_left h

/-- The polynomial core of the proof, in the coordinates `(aₖ, bₖ, cₖ, dₖ)` of the
`u₁, u₂, u₃, u₄`-components of `φ(uₖ)`. The hypotheses are the vanishing cross minors
(`[uₖ, uₗ] ∈ γ₃` for `k ∈ {1,2}`, `l ∈ {3,4}`), the `e₇, e₈` coefficients of
`φ[uₖ, [u₁,u₂]]` and `φ[uₖ, [u₃,u₄]]`, the `e₇` coefficient of `φ[u₁,u₃]` (needed only
when the `u₂, u₄`-components of `φ(u₁), φ(u₃)` vanish), and `det A ≠ 0`. -/
theorem core_alg (h2 : (2 : K) ≠ 0) {a1 b1 c1 d1 a2 b2 c2 d2 a3 b3 c3 d3 a4 b4 c4 d4 ζ : K}
    (x13p : a1 * b3 - b1 * a3 = 0) (x13q : c1 * d3 - d1 * c3 = 0)
    (x14p : a1 * b4 - b1 * a4 = 0) (x14q : c1 * d4 - d1 * c4 = 0)
    (x23p : a2 * b3 - b2 * a3 = 0) (x23q : c2 * d3 - d2 * c3 = 0)
    (x24p : a2 * b4 - b2 * a4 = 0) (x24q : c2 * d4 - d2 * c4 = 0)
    (ev1a : b1 * (a1 * b2 - b1 * a2) + d1 * (c1 * d2 - d1 * c2) = 0)
    (ev1b : a1 * (a1 * b2 - b1 * a2) - c1 * (c1 * d2 - d1 * c2) = 8 * ζ)
    (ev2a : b2 * (a1 * b2 - b1 * a2) + d2 * (c1 * d2 - d1 * c2) = 8 * ζ)
    (ev2b : a2 * (a1 * b2 - b1 * a2) - c2 * (c1 * d2 - d1 * c2) = 0)
    (ev3a : b3 * (a3 * b4 - b3 * a4) + d3 * (c3 * d4 - d3 * c4) = 0)
    (ev3b : a3 * (a3 * b4 - b3 * a4) - c3 * (c3 * d4 - d3 * c4) = -(8 * ζ))
    (ev4a : b4 * (a3 * b4 - b3 * a4) + d4 * (c3 * d4 - d3 * c4) = 8 * ζ)
    (ev4b : a4 * (a3 * b4 - b3 * a4) - c4 * (c3 * d4 - d3 * c4) = 0)
    (h13 : b1 = 0 → d1 = 0 → b3 = 0 → d3 = 0 → a1 * c3 - c1 * a3 = 4 * ζ)
    (hdet : Matrix.det !![a1, a2, a3, a4; b1, b2, b3, b4; c1, c2, c3, c4; d1, d2, d3, d4] ≠ 0) :
    ζ = 1 ∨ ζ = -1 := by
  have hL : Matrix.det !![a1, a2, a3, a4; b1, b2, b3, b4; c1, c2, c3, c4; d1, d2, d3, d4] =
      (a1 * b2 - b1 * a2) * (c3 * d4 - d3 * c4) - (a1 * b3 - b1 * a3) * (c2 * d4 - d2 * c4)
      + (a1 * b4 - b1 * a4) * (c2 * d3 - d2 * c3) + (a2 * b3 - b2 * a3) * (c1 * d4 - d1 * c4)
      - (a2 * b4 - b2 * a4) * (c1 * d3 - d1 * c3)
      + (a3 * b4 - b3 * a4) * (c1 * d2 - d1 * c2) := by
    have s1 : Fin.succAbove (1 : Fin 4) (2 : Fin 3) = 3 := by decide
    have s2 : Fin.succAbove (2 : Fin 4) (2 : Fin 3) = 3 := by decide
    have s3 : Fin.succAbove (3 : Fin 4) (2 : Fin 3) = 2 := by decide
    simp [Matrix.det_succ_row_zero, Fin.sum_univ_succ, s1, s2, s3]
    ring
  have hdet' : (a1 * b2 - b1 * a2) * (c3 * d4 - d3 * c4)
      + (a3 * b4 - b3 * a4) * (c1 * d2 - d1 * c2) ≠ 0 := by
    intro h0; apply hdet; rw [hL, x13p, x14p, x23p, x24p]; linear_combination h0
  by_cases hD12 : a1 * b2 - b1 * a2 = 0
  · -- `A` exchanges `U₊` and `U₋`.
    rw [hD12, zero_mul, zero_add] at hdet'
    have hD34 := left_ne_zero_of_mul hdet'
    have hE12 := right_ne_zero_of_mul hdet'
    have ha1 : a1 = 0 := (mul_eq_zero.mp (show (a3 * b4 - b3 * a4) * a1 = 0 by
      linear_combination a3 * x14p - a4 * x13p)).resolve_left hD34
    have hb1 : b1 = 0 := (mul_eq_zero.mp (show (a3 * b4 - b3 * a4) * b1 = 0 by
      linear_combination b3 * x14p - b4 * x13p)).resolve_left hD34
    have ha2 : a2 = 0 := (mul_eq_zero.mp (show (a3 * b4 - b3 * a4) * a2 = 0 by
      linear_combination a3 * x24p - a4 * x23p)).resolve_left hD34
    have hb2 : b2 = 0 := (mul_eq_zero.mp (show (a3 * b4 - b3 * a4) * b2 = 0 by
      linear_combination b3 * x24p - b4 * x23p)).resolve_left hD34
    have hc3 : c3 = 0 := (mul_eq_zero.mp (show (c1 * d2 - d1 * c2) * c3 = 0 by
      linear_combination -c1 * x23q + c2 * x13q)).resolve_left hE12
    have hd3 : d3 = 0 := (mul_eq_zero.mp (show (c1 * d2 - d1 * c2) * d3 = 0 by
      linear_combination -d1 * x23q + d2 * x13q)).resolve_left hE12
    have hc4 : c4 = 0 := (mul_eq_zero.mp (show (c1 * d2 - d1 * c2) * c4 = 0 by
      linear_combination -c1 * x24q + c2 * x14q)).resolve_left hE12
    have hd4 : d4 = 0 := (mul_eq_zero.mp (show (c1 * d2 - d1 * c2) * d4 = 0 by
      linear_combination -d1 * x24q + d2 * x14q)).resolve_left hE12
    subst ha1 hb1 ha2 hb2 hc3 hd3 hc4 hd4
    have hd1 : d1 = 0 := (mul_eq_zero.mp (show d1 * (c1 * d2 - d1 * c2) = 0 by
      linear_combination ev1a)).resolve_right hE12
    have hc2 : c2 = 0 := (mul_eq_zero.mp (show c2 * (c1 * d2 - d1 * c2) = 0 by
      linear_combination -ev2b)).resolve_right hE12
    have hb3 : b3 = 0 := (mul_eq_zero.mp (show b3 * (a3 * b4 - b3 * a4) = 0 by
      linear_combination ev3a)).resolve_right hD34
    have ha4 : a4 = 0 := (mul_eq_zero.mp (show a4 * (a3 * b4 - b3 * a4) = 0 by
      linear_combination ev4b)).resolve_right hD34
    subst hd1 hc2 hb3 ha4
    have hE : c1 * d2 ≠ 0 := by intro h; apply hE12; linear_combination h
    have hD : a3 * b4 ≠ 0 := by intro h; apply hD34; linear_combination h
    have hd2 : d2 = -c1 := by
      have : (d2 + c1) * (c1 * d2) = 0 := by linear_combination ev2a - ev1b
      exact eq_neg_of_add_eq_zero_left ((mul_eq_zero.mp this).resolve_right hE)
    have hb4 : b4 = -a3 := by
      have : (b4 + a3) * (a3 * b4) = 0 := by linear_combination ev4a + ev3b
      exact eq_neg_of_add_eq_zero_left ((mul_eq_zero.mp this).resolve_right hD)
    subst hd2 hb4
    have hc1 : c1 ≠ 0 := by intro h; apply hE; rw [h]; ring
    have hrt := h13 rfl rfl rfl rfl
    right
    exact swap_final h2 (r := c1) (t := a3) (by linear_combination ev1b)
      (by linear_combination -ev3b) (by linear_combination -hrt) hc1
  · -- `A` preserves `U₊` and `U₋`.
    have ha3 : a3 = 0 := (mul_eq_zero.mp (show (a1 * b2 - b1 * a2) * a3 = 0 by
      linear_combination -a1 * x23p + a2 * x13p)).resolve_left hD12
    have hb3 : b3 = 0 := (mul_eq_zero.mp (show (a1 * b2 - b1 * a2) * b3 = 0 by
      linear_combination -b1 * x23p + b2 * x13p)).resolve_left hD12
    have ha4 : a4 = 0 := (mul_eq_zero.mp (show (a1 * b2 - b1 * a2) * a4 = 0 by
      linear_combination -a1 * x24p + a2 * x14p)).resolve_left hD12
    have hb4 : b4 = 0 := (mul_eq_zero.mp (show (a1 * b2 - b1 * a2) * b4 = 0 by
      linear_combination -b1 * x24p + b2 * x14p)).resolve_left hD12
    subst ha3 hb3 ha4 hb4
    have hE34 : c3 * d4 - d3 * c4 ≠ 0 := by
      intro h; apply hdet'; rw [h]; ring
    have hc1 : c1 = 0 := (mul_eq_zero.mp (show (c3 * d4 - d3 * c4) * c1 = 0 by
      linear_combination c3 * x14q - c4 * x13q)).resolve_left hE34
    have hd1 : d1 = 0 := (mul_eq_zero.mp (show (c3 * d4 - d3 * c4) * d1 = 0 by
      linear_combination d3 * x14q - d4 * x13q)).resolve_left hE34
    have hc2 : c2 = 0 := (mul_eq_zero.mp (show (c3 * d4 - d3 * c4) * c2 = 0 by
      linear_combination c3 * x24q - c4 * x23q)).resolve_left hE34
    have hd2 : d2 = 0 := (mul_eq_zero.mp (show (c3 * d4 - d3 * c4) * d2 = 0 by
      linear_combination d3 * x24q - d4 * x23q)).resolve_left hE34
    subst hc1 hd1 hc2 hd2
    have hb1 : b1 = 0 := (mul_eq_zero.mp (show b1 * (a1 * b2 - b1 * a2) = 0 by
      linear_combination ev1a)).resolve_right hD12
    have ha2 : a2 = 0 := (mul_eq_zero.mp (show a2 * (a1 * b2 - b1 * a2) = 0 by
      linear_combination ev2b)).resolve_right hD12
    have hd3 : d3 = 0 := (mul_eq_zero.mp (show d3 * (c3 * d4 - d3 * c4) = 0 by
      linear_combination ev3a)).resolve_right hE34
    have hc4 : c4 = 0 := (mul_eq_zero.mp (show c4 * (c3 * d4 - d3 * c4) = 0 by
      linear_combination -ev4b)).resolve_right hE34
    subst hb1 ha2 hd3 hc4
    have hD : a1 * b2 ≠ 0 := by intro h; apply hD12; linear_combination h
    have hE : c3 * d4 ≠ 0 := by intro h; apply hE34; linear_combination h
    have hb2 : b2 = a1 := by
      have : (b2 - a1) * (a1 * b2) = 0 := by linear_combination ev2a - ev1b
      exact sub_eq_zero.mp ((mul_eq_zero.mp this).resolve_right hD)
    have hd4 : d4 = c3 := by
      have : (d4 - c3) * (c3 * d4) = 0 := by linear_combination ev4a + ev3b
      exact sub_eq_zero.mp ((mul_eq_zero.mp this).resolve_right hE)
    subst hb2 hd4
    have ha1 : b2 ≠ 0 := by intro h; apply hD; rw [h]; ring
    have hmn := h13 rfl rfl rfl rfl
    left
    exact keep_final h2 (m := b2) (n := d4) (by linear_combination ev1b)
      (by linear_combination -ev3b) (by linear_combination hmn) ha1

end Algebra

/-! ### Over a field containing a square root of `-1` -/

section Core

variable {K : Type*} [Field K]

/-- Coordinates of the `u₁,…,u₄`-components (times two) and of the `v₊, v₋`-components
(times two) in the paper's basis `u₁ = ie₁ + e₄, u₂ = e₃ - ie₂, u₃ = e₄ - ie₁,
u₄ = e₃ + ie₂, v_± = e₅ ± ie₆`. -/
def C1 (i : K) : DL K →ₗ[K] K where
  toFun x := x 3 - i * x 0
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

def C2 (i : K) : DL K →ₗ[K] K where
  toFun x := x 2 + i * x 1
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

def C3 (i : K) : DL K →ₗ[K] K where
  toFun x := x 3 + i * x 0
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

def C4 (i : K) : DL K →ₗ[K] K where
  toFun x := x 2 - i * x 1
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

def Dp (i : K) : DL K →ₗ[K] K where
  toFun x := x 4 - i * x 5
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

def Dm (i : K) : DL K →ₗ[K] K where
  toFun x := x 4 + i * x 5
  map_add' x y := by simp; ring
  map_smul' t x := by simp; ring

@[simp] theorem C1_apply (i : K) (x : DL K) : C1 i x = x 3 - i * x 0 := rfl
@[simp] theorem C2_apply (i : K) (x : DL K) : C2 i x = x 2 + i * x 1 := rfl
@[simp] theorem C3_apply (i : K) (x : DL K) : C3 i x = x 3 + i * x 0 := rfl
@[simp] theorem C4_apply (i : K) (x : DL K) : C4 i x = x 2 - i * x 1 := rfl
@[simp] theorem Dp_apply (i : K) (x : DL K) : Dp i x = x 4 - i * x 5 := rfl
@[simp] theorem Dm_apply (i : K) (x : DL K) : Dm i x = x 4 + i * x 5 := rfl

def u1 (i : K) : DL K := ![i, 0, 0, 1, 0, 0, 0, 0]
def u2 (i : K) : DL K := ![0, -i, 1, 0, 0, 0, 0, 0]
def u3 (i : K) : DL K := ![-i, 0, 0, 1, 0, 0, 0, 0]
def u4 (i : K) : DL K := ![0, i, 1, 0, 0, 0, 0, 0]

variable {i : K}

@[simp] theorem u1_apply (k : Fin 8) : u1 i k = ![i, 0, 0, 1, 0, 0, 0, 0] k := rfl
@[simp] theorem u2_apply (k : Fin 8) : u2 i k = ![0, -i, 1, 0, 0, 0, 0, 0] k := rfl
@[simp] theorem u3_apply (k : Fin 8) : u3 i k = ![-i, 0, 0, 1, 0, 0, 0, 0] k := rfl
@[simp] theorem u4_apply (k : Fin 8) : u4 i k = ![0, i, 1, 0, 0, 0, 0, 0] k := rfl

theorem Dp_lie (hi : i * i = -1) (x y : DL K) :
    Dp i ⁅x, y⁆ = C1 i x * C2 i y - C2 i x * C1 i y := by
  simp; linear_combination (x 0 * y 1 - x 1 * y 0) * hi

theorem Dm_lie (hi : i * i = -1) (x y : DL K) :
    Dm i ⁅x, y⁆ = C3 i x * C4 i y - C4 i x * C3 i y := by
  simp; linear_combination (x 0 * y 1 - x 1 * y 0) * hi

theorem lie_lie_6 (hi : i * i = -1) (x y z : DL K) :
    2 * ⁅x, ⁅y, z⁆⁆ 6 = -(C2 i x * Dp i ⁅y, z⁆ + C4 i x * Dm i ⁅y, z⁆) := by
  simp
  linear_combination (-2 * x 1 * (y 0 * z 2 + y 1 * z 3 - y 2 * z 0 - y 3 * z 1)) * hi

theorem lie_lie_7 (hi : i * i = -1) (x y z : DL K) :
    2 * ⁅x, ⁅y, z⁆⁆ 7 = -(i * (C1 i x * Dp i ⁅y, z⁆ - C3 i x * Dm i ⁅y, z⁆)) := by
  simp
  linear_combination (-2 * (x 0 * y 0 * z 1 - x 0 * y 1 * z 0 - x 0 * y 2 * z 3
    + x 0 * y 3 * z 2 + x 3 * y 0 * z 2 + x 3 * y 1 * z 3 - x 3 * y 2 * z 0
    - x 3 * y 3 * z 1)) * hi

theorem lie_6_of (hi : i * i = -1) (x y : DL K) (hx1 : x 1 = 0) (hx2 : x 2 = 0)
    (hy1 : y 1 = 0) (hy2 : y 2 = 0) :
    2 * ⁅x, y⁆ 6 = i * (C1 i x * C3 i y - C3 i x * C1 i y) := by
  simp [hx1, hx2, hy1, hy2]
  linear_combination (2 * (x 0 * y 3 - x 3 * y 0)) * hi

theorem C1_lie (x y : DL K) : C1 i ⁅x, y⁆ = 0 := by simp
theorem C2_lie (x y : DL K) : C2 i ⁅x, y⁆ = 0 := by simp
theorem C3_lie (x y : DL K) : C3 i ⁅x, y⁆ = 0 := by simp
theorem C4_lie (x y : DL K) : C4 i ⁅x, y⁆ = 0 := by simp

set_option hygiene false in
/-- Try the small multiples of `hi : i * i = -1` that the `u`-bracket identities need
(refers to the local hypothesis `hi` and the local `i`). -/
macro "isq" : tactic => `(tactic| first
    | ring1
    | linear_combination hi | linear_combination -hi
    | linear_combination 2 * hi | linear_combination -2 * hi
    | linear_combination 3 * hi | linear_combination -3 * hi
    | linear_combination 4 * hi | linear_combination -4 * hi
    | linear_combination i * hi | linear_combination -i * hi
    | linear_combination 2 * i * hi | linear_combination -2 * i * hi
    | linear_combination 4 * i * hi | linear_combination -4 * i * hi)

theorem lie_u1_u3 : ⁅u1 i, u3 i⁆ = (2 * i) • E K 6 := by
  apply ext8 <;> simp; ring

theorem lie_u1_u4 (hi : i * i = -1) : ⁅u1 i, u4 i⁆ = 0 := by
  apply ext8 <;> simp
  linear_combination hi

theorem lie_u2_u3 (hi : i * i = -1) : ⁅u2 i, u3 i⁆ = 0 := by
  apply ext8 <;> simp
  linear_combination -hi

theorem lie_u2_u4 : ⁅u2 i, u4 i⁆ = (-(2 * i)) • E K 7 := by
  apply ext8 <;> simp; ring

theorem lie_u1_u12 (hi : i * i = -1) : ⁅u1 i, ⁅u1 i, u2 i⁆⁆ = (-(4 * i)) • E K 7 := by
  apply ext8 <;> simp
  linear_combination i * hi

theorem lie_u2_u12 (hi : i * i = -1) : ⁅u2 i, ⁅u1 i, u2 i⁆⁆ = (-4 : K) • E K 6 := by
  apply ext8 <;> simp
  linear_combination 3 * hi

theorem lie_u3_u34 (hi : i * i = -1) : ⁅u3 i, ⁅u3 i, u4 i⁆⁆ = (4 * i) • E K 7 := by
  apply ext8 <;> simp
  linear_combination -i * hi

theorem lie_u4_u34 (hi : i * i = -1) : ⁅u4 i, ⁅u3 i, u4 i⁆⁆ = (-4 : K) • E K 6 := by
  apply ext8 <;> simp
  linear_combination 3 * hi

/-- `2x` in the basis `u₁,…,u₄, e₅,…,e₈`. -/
theorem two_smul_decomp (hi : i * i = -1) (x : DL K) :
    (2 : K) • x = C1 i x • u1 i + C2 i x • u2 i + C3 i x • u3 i + C4 i x • u4 i +
      (2 * x 4) • E K 4 + (2 * x 5) • E K 5 + (2 * x 6) • E K 6 + (2 * x 7) • E K 7 := by
  apply ext8 <;> simp
  · linear_combination (2 * x 0) * hi
  · linear_combination (2 * x 1) * hi
  all_goals ring

theorem smulE6_6 (c : K) : (c • E K 6) 6 = c := by simp
theorem smulE6_7 (c : K) : (c • E K 6) 7 = 0 := by simp
theorem smulE7_6 (c : K) : (c • E K 7) 6 = 0 := by simp
theorem smulE7_7 (c : K) : (c • E K 7) 7 = c := by simp

theorem coords_of_C2_C4 (h2 : (2 : K) ≠ 0) (hi0 : i ≠ 0) {x : DL K}
    (hb : C2 i x = 0) (hd : C4 i x = 0) : x 1 = 0 ∧ x 2 = 0 := by
  simp only [C2_apply, C4_apply] at hb hd
  constructor
  · have : (2 * i) * x 1 = 0 := by linear_combination hb - hd
    exact (mul_eq_zero.mp this).resolve_left (mul_ne_zero h2 hi0)
  · have : 2 * x 2 = 0 := by linear_combination hb + hd
    exact (mul_eq_zero.mp this).resolve_left h2

/-- The coordinates `C_j(φ x)` in terms of `C_k(x)` and the images of the `u_k`:
`φ` maps `γ₂ = [L, L]` into `γ₂`, on which every `C_j` vanishes. -/
theorem two_mul_apply (hi : i * i = -1) (φ : DL K →ₗ[K] DL K)
    (hφ : ∀ x y, φ ⁅x, y⁆ = ⁅φ x, φ y⁆) (L : DL K →ₗ[K] K) (hL : ∀ a b : DL K, L ⁅a, b⁆ = 0)
    (x : DL K) :
    2 * L (φ x) = C1 i x * L (φ (u1 i)) + C2 i x * L (φ (u2 i)) + C3 i x * L (φ (u3 i)) +
      C4 i x * L (φ (u4 i)) := by
  have hd := congrArg (fun v => L (φ v)) (two_smul_decomp hi x)
  simp only [map_add, map_smul, smul_eq_mul] at hd
  have t := (table (R := K))
  have e4 : L (φ (E K 4)) = 0 := by rw [← t.1, hφ, hL]
  have e5 : L (φ (E K 5)) = 0 := by rw [← t.2.1, hφ, hL]
  have e6 : L (φ (E K 6)) = 0 := by rw [← t.2.2.1, hφ, hL]
  have e7 : L (φ (E K 7)) = 0 := by rw [← t.2.2.2.2.1, hφ, hL]
  rw [e4, e5, e6, e7] at hd
  linear_combination hd

/-- The proposition over a field containing `i` with `i² = -1`, for a bracket-preserving
linear surjection `φ` acting on `e₇, e₈` by `ζ`. -/
theorem scalar_core (h2 : (2 : K) ≠ 0) (hi : i * i = -1)
    (φ : DL K →ₗ[K] DL K) (hφ : ∀ x y, φ ⁅x, y⁆ = ⁅φ x, φ y⁆)
    (hs : Function.Surjective φ) (ζ : K)
    (h6 : φ (E K 6) = ζ • E K 6) (h7 : φ (E K 7) = ζ • E K 7) : ζ = 1 ∨ ζ = -1 := by
  have hi0 : i ≠ 0 := by rintro rfl; simp at hi
  -- The bracket relations, transported by `φ`.
  have r13 : ⁅φ (u1 i), φ (u3 i)⁆ = (2 * i * ζ) • E K 6 := by
    rw [← hφ, lie_u1_u3, map_smul, h6, smul_smul]
  have r14 : ⁅φ (u1 i), φ (u4 i)⁆ = 0 := by rw [← hφ, lie_u1_u4 hi, map_zero]
  have r23 : ⁅φ (u2 i), φ (u3 i)⁆ = 0 := by rw [← hφ, lie_u2_u3 hi, map_zero]
  have r24 : ⁅φ (u2 i), φ (u4 i)⁆ = (-(2 * i) * ζ) • E K 7 := by
    rw [← hφ, lie_u2_u4, map_smul, h7, smul_smul]
  have r1 : ⁅φ (u1 i), ⁅φ (u1 i), φ (u2 i)⁆⁆ = (-(4 * i) * ζ) • E K 7 := by
    rw [← hφ, ← hφ, lie_u1_u12 hi, map_smul, h7, smul_smul]
  have r2 : ⁅φ (u2 i), ⁅φ (u1 i), φ (u2 i)⁆⁆ = (-4 * ζ) • E K 6 := by
    rw [← hφ, ← hφ, lie_u2_u12 hi, map_smul, h6, smul_smul]
  have r3 : ⁅φ (u3 i), ⁅φ (u3 i), φ (u4 i)⁆⁆ = (4 * i * ζ) • E K 7 := by
    rw [← hφ, ← hφ, lie_u3_u34 hi, map_smul, h7, smul_smul]
  have r4 : ⁅φ (u4 i), ⁅φ (u3 i), φ (u4 i)⁆⁆ = (-4 * ζ) • E K 6 := by
    rw [← hφ, ← hφ, lie_u4_u34 hi, map_smul, h6, smul_smul]
  -- Vanishing cross minors.
  have x13p := (Dp_lie hi (φ (u1 i)) (φ (u3 i))).symm.trans
    (show Dp i ⁅φ (u1 i), φ (u3 i)⁆ = 0 by rw [r13]; simp)
  have x13q := (Dm_lie hi (φ (u1 i)) (φ (u3 i))).symm.trans
    (show Dm i ⁅φ (u1 i), φ (u3 i)⁆ = 0 by rw [r13]; simp)
  have x14p := (Dp_lie hi (φ (u1 i)) (φ (u4 i))).symm.trans
    (show Dp i ⁅φ (u1 i), φ (u4 i)⁆ = 0 by rw [r14]; simp)
  have x14q := (Dm_lie hi (φ (u1 i)) (φ (u4 i))).symm.trans
    (show Dm i ⁅φ (u1 i), φ (u4 i)⁆ = 0 by rw [r14]; simp)
  have x23p := (Dp_lie hi (φ (u2 i)) (φ (u3 i))).symm.trans
    (show Dp i ⁅φ (u2 i), φ (u3 i)⁆ = 0 by rw [r23]; simp)
  have x23q := (Dm_lie hi (φ (u2 i)) (φ (u3 i))).symm.trans
    (show Dm i ⁅φ (u2 i), φ (u3 i)⁆ = 0 by rw [r23]; simp)
  have x24p := (Dp_lie hi (φ (u2 i)) (φ (u4 i))).symm.trans
    (show Dp i ⁅φ (u2 i), φ (u4 i)⁆ = 0 by rw [r24]; simp)
  have x24q := (Dm_lie hi (φ (u2 i)) (φ (u4 i))).symm.trans
    (show Dm i ⁅φ (u2 i), φ (u4 i)⁆ = 0 by rw [r24]; simp)
  -- The `e₇, e₈` coefficients of `φ[u_k, [u₁,u₂]]` and `φ[u_k, [u₃,u₄]]`.
  have ev1a := lie_lie_6 hi (φ (u1 i)) (φ (u1 i)) (φ (u2 i))
  rw [r1, smulE7_6, Dp_lie hi, Dm_lie hi] at ev1a
  have ev1b := lie_lie_7 hi (φ (u1 i)) (φ (u1 i)) (φ (u2 i))
  rw [r1, smulE7_7, Dp_lie hi, Dm_lie hi] at ev1b
  have ev2a := lie_lie_6 hi (φ (u2 i)) (φ (u1 i)) (φ (u2 i))
  rw [r2, smulE6_6, Dp_lie hi, Dm_lie hi] at ev2a
  have ev2b := lie_lie_7 hi (φ (u2 i)) (φ (u1 i)) (φ (u2 i))
  rw [r2, smulE6_7, Dp_lie hi, Dm_lie hi] at ev2b
  have ev3a := lie_lie_6 hi (φ (u3 i)) (φ (u3 i)) (φ (u4 i))
  rw [r3, smulE7_6, Dp_lie hi, Dm_lie hi] at ev3a
  have ev3b := lie_lie_7 hi (φ (u3 i)) (φ (u3 i)) (φ (u4 i))
  rw [r3, smulE7_7, Dp_lie hi, Dm_lie hi] at ev3b
  have ev4a := lie_lie_6 hi (φ (u4 i)) (φ (u3 i)) (φ (u4 i))
  rw [r4, smulE6_6, Dp_lie hi, Dm_lie hi] at ev4a
  have ev4b := lie_lie_7 hi (φ (u4 i)) (φ (u3 i)) (φ (u4 i))
  rw [r4, smulE6_7, Dp_lie hi, Dm_lie hi] at ev4b
  -- Nondegeneracy from surjectivity: `A S = 4`.
  let Cf : Fin 4 → (DL K →ₗ[K] K) := ![C1 i, C2 i, C3 i, C4 i]
  let Wf : Fin 4 → DL K := ![φ (u1 i), φ (u2 i), φ (u3 i), φ (u4 i)]
  let uf : Fin 4 → DL K := ![u1 i, u2 i, u3 i, u4 i]
  choose sf hsf using fun m => hs (uf m)
  have hCf : ∀ j (a b : DL K), Cf j ⁅a, b⁆ = 0 := by
    intro j a b; fin_cases j <;> simp [Cf]
  have hCu : ∀ j m, Cf j (uf m) = if j = m then 2 else 0 := by
    intro j m
    fin_cases j <;> fin_cases m <;> simp [Cf, uf]
    all_goals isq
  have hentry : ∀ j m, ∑ k, Cf j (Wf k) * Cf k (sf m) = 2 * (2 * if j = m then (1 : K) else 0) := by
    intro j m
    have h := two_mul_apply hi φ hφ (Cf j) (hCf j) (sf m)
    rw [hsf m, hCu j m] at h
    simp only [Fin.sum_univ_four]
    have e0 : Cf 0 = C1 i := rfl
    have e1 : Cf 1 = C2 i := rfl
    have e2 : Cf 2 = C3 i := rfl
    have e3 : Cf 3 = C4 i := rfl
    have w0 : Wf 0 = φ (u1 i) := rfl
    have w1 : Wf 1 = φ (u2 i) := rfl
    have w2 : Wf 2 = φ (u3 i) := rfl
    have w3 : Wf 3 = φ (u4 i) := rfl
    rw [e0, e1, e2, e3, w0, w1, w2, w3]
    split_ifs at h ⊢ <;> linear_combination -h
  let A : Matrix (Fin 4) (Fin 4) K := Matrix.of fun j k => Cf j (Wf k)
  let S : Matrix (Fin 4) (Fin 4) K := Matrix.of fun k m => Cf k (sf m)
  have hAS : A * S = (4 : K) • (1 : Matrix (Fin 4) (Fin 4) K) := by
    ext j m
    rw [Matrix.mul_apply, Matrix.smul_apply, Matrix.one_apply]
    simp only [A, S, Matrix.of_apply]
    rw [hentry j m]
    split_ifs <;> simp; ring
  have hdetA : A.det ≠ 0 := by
    intro h0
    have := congrArg Matrix.det hAS
    rw [Matrix.det_mul, h0, zero_mul, Matrix.det_smul, Matrix.det_one, Fintype.card_fin,
      mul_one] at this
    exact pow_ne_zero 4 (show (4 : K) ≠ 0 by
      rw [show (4 : K) = 2 * 2 by norm_num]; exact mul_ne_zero h2 h2) this.symm
  have hA : !![C1 i (φ (u1 i)), C1 i (φ (u2 i)), C1 i (φ (u3 i)), C1 i (φ (u4 i));
      C2 i (φ (u1 i)), C2 i (φ (u2 i)), C2 i (φ (u3 i)), C2 i (φ (u4 i));
      C3 i (φ (u1 i)), C3 i (φ (u2 i)), C3 i (φ (u3 i)), C3 i (φ (u4 i));
      C4 i (φ (u1 i)), C4 i (φ (u2 i)), C4 i (φ (u3 i)), C4 i (φ (u4 i))] = A := by
    ext j k; fin_cases j <;> fin_cases k <;> rfl
  refine core_alg h2 x13p x13q x14p x14q x23p x23q x24p x24q
    (by linear_combination ev1a) ?_ (by linear_combination ev2a) ?_
    (by linear_combination ev3a) ?_ (by linear_combination ev4a) ?_ ?_ (hA ▸ hdetA)
  · have : i * (C1 i (φ (u1 i)) * (C1 i (φ (u1 i)) * C2 i (φ (u2 i)) -
        C2 i (φ (u1 i)) * C1 i (φ (u2 i))) - C3 i (φ (u1 i)) * (C3 i (φ (u1 i)) *
        C4 i (φ (u2 i)) - C4 i (φ (u1 i)) * C3 i (φ (u2 i))) - 8 * ζ) = 0 := by
      linear_combination ev1b
    exact sub_eq_zero.mp ((mul_eq_zero.mp this).resolve_left hi0)
  · have : i * (C1 i (φ (u2 i)) * (C1 i (φ (u1 i)) * C2 i (φ (u2 i)) -
        C2 i (φ (u1 i)) * C1 i (φ (u2 i))) - C3 i (φ (u2 i)) * (C3 i (φ (u1 i)) *
        C4 i (φ (u2 i)) - C4 i (φ (u1 i)) * C3 i (φ (u2 i)))) = 0 := by
      linear_combination ev2b
    exact (mul_eq_zero.mp this).resolve_left hi0
  · have : i * (C1 i (φ (u3 i)) * (C1 i (φ (u3 i)) * C2 i (φ (u4 i)) -
        C2 i (φ (u3 i)) * C1 i (φ (u4 i))) - C3 i (φ (u3 i)) * (C3 i (φ (u3 i)) *
        C4 i (φ (u4 i)) - C4 i (φ (u3 i)) * C3 i (φ (u4 i))) + 8 * ζ) = 0 := by
      linear_combination ev3b
    exact eq_neg_of_add_eq_zero_left ((mul_eq_zero.mp this).resolve_left hi0)
  · have : i * (C1 i (φ (u4 i)) * (C1 i (φ (u3 i)) * C2 i (φ (u4 i)) -
        C2 i (φ (u3 i)) * C1 i (φ (u4 i))) - C3 i (φ (u4 i)) * (C3 i (φ (u3 i)) *
        C4 i (φ (u4 i)) - C4 i (φ (u3 i)) * C3 i (φ (u4 i)))) = 0 := by
      linear_combination ev4b
    exact (mul_eq_zero.mp this).resolve_left hi0
  · intro hb1 hd1 hb3 hd3
    obtain ⟨hx1, hx2⟩ := coords_of_C2_C4 h2 hi0 hb1 hd1
    obtain ⟨hy1, hy2⟩ := coords_of_C2_C4 h2 hi0 hb3 hd3
    have h := lie_6_of hi _ _ hx1 hx2 hy1 hy2
    rw [r13, smulE6_6] at h
    have : i * (C1 i (φ (u1 i)) * C3 i (φ (u3 i)) - C3 i (φ (u1 i)) * C1 i (φ (u3 i)) -
        4 * ζ) = 0 := by linear_combination -h
    exact sub_eq_zero.mp ((mul_eq_zero.mp this).resolve_left hi0)

end Core

/-! ### Base change and the proposition -/

section BaseChange

variable {K K' : Type*} [Field K] [Field K'] (f : K →+* K')

/-- Coordinatewise image under `f`. -/
def bmap : DL K →+ DL K' where
  toFun x := fun k => f (x k)
  map_zero' := funext fun _ => map_zero f
  map_add' x y := funext fun k => map_add f (x k) (y k)

@[simp] theorem bmap_apply (x : DL K) (k : Fin 8) : bmap f x k = f (x k) := rfl

theorem bmap_smul (t : K) (x : DL K) : bmap f (t • x) = f t • bmap f x := by
  apply ext8 <;> simp

theorem bmap_lie (x y : DL K) : bmap f ⁅x, y⁆ = ⁅bmap f x, bmap f y⁆ := by
  apply ext8 <;> simp

theorem bmap_E (j : Fin 8) : bmap f (E K j) = E K' j := by
  funext k
  simp only [bmap_apply, e_apply]
  split_ifs <;> simp

/-- The coordinate functional. -/
def coord (k : Fin 8) : DL K' →ₗ[K'] K' where
  toFun x := x k
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- Base change of a `K`-linear endomorphism of `DL K`, by its matrix. -/
def bc (g : DL K →ₗ[K] DL K) : DL K' →ₗ[K'] DL K' where
  toFun x := ∑ j : Fin 8, x j • bmap f (g (E K j))
  map_add' x y := by simp [add_smul, Finset.sum_add_distrib]
  map_smul' t x := by simp [Finset.smul_sum, mul_smul]

theorem bc_apply (g : DL K →ₗ[K] DL K) (x : DL K') :
    bc f g x = ∑ j : Fin 8, x j • bmap f (g (E K j)) := rfl

theorem bc_base (g : DL K →ₗ[K] DL K) (x : DL K) : bc f g (bmap f x) = bmap f (g x) := by
  conv_rhs => rw [sum_E x]
  rw [map_sum, map_sum, bc_apply]
  simp [map_smul, bmap_smul]

theorem bc_E (g : DL K →ₗ[K] DL K) (j : Fin 8) : bc f g (E K' j) = bmap f (g (E K j)) := by
  rw [← bmap_E f j, bc_base]

theorem bc_lie (g : DL K →ₗ[K] DL K) (hg : ∀ x y, g ⁅x, y⁆ = ⁅g x, g y⁆) (x y : DL K') :
    bc f g ⁅x, y⁆ = ⁅bc f g x, bc f g y⁆ := by
  have hb : ∀ j l, bc f g ⁅E K' j, E K' l⁆ = ⁅bc f g (E K' j), bc f g (E K' l)⁆ := by
    intro j l
    rw [← bmap_E f j, ← bmap_E f l, ← bmap_lie, bc_base, bc_base, bc_base, hg, bmap_lie]
  rw [sum_E x, sum_E y]
  simp only [sum_lie, lie_sum, smul_lie, lie_smul, map_sum, map_smul, hb]

theorem bc_surj (φ : DL K ≃ₗ⁅K⁆ DL K) :
    Function.Surjective (bc f φ.toLieHom.toLinearMap) := by
  intro y
  refine ⟨bc f φ.symm.toLieHom.toLinearMap y, ?_⟩
  conv_rhs => rw [sum_E y]
  conv_lhs => rw [sum_E y]
  simp only [map_sum, map_smul]
  refine Finset.sum_congr rfl fun j _ => ?_
  congr 1
  rw [bc_E, bc_base]
  simp [bmap_E]

end BaseChange

section Main

variable {K : Type*} [Field K]

/-- Only `±1` can occur. -/
theorem scalar_of_equiv (h2 : (2 : K) ≠ 0) (φ : DL K ≃ₗ⁅K⁆ DL K) (ζ : K)
    (hz : ∀ z ∈ LieAlgebra.center K (DL K), φ z = ζ • z) : ζ = 1 ∨ ζ = -1 := by
  let f : K →+* AlgebraicClosure K := algebraMap K (AlgebraicClosure K)
  obtain ⟨i, hi⟩ := IsAlgClosed.exists_pow_nat_eq (-1 : AlgebraicClosure K) (n := 2)
    (by norm_num)
  have h2' : (2 : AlgebraicClosure K) ≠ 0 := by
    intro h; apply h2; apply f.injective; rw [map_ofNat f 2, h, map_zero]
  have h6 : φ (E K 6) = ζ • E K 6 := hz _ E6_mem_center
  have h7 : φ (E K 7) = ζ • E K 7 := hz _ E7_mem_center
  have key := scalar_core h2' (i := i) (by rw [← sq]; exact hi) (bc f φ.toLieHom.toLinearMap)
    (bc_lie f _ (fun x y => φ.map_lie x y)) (bc_surj f φ) (f ζ)
    (by rw [bc_E]; simp [h6, bmap_smul, bmap_E])
    (by rw [bc_E]; simp [h7, bmap_smul, bmap_E])
  rcases key with h | h
  · left; apply f.injective; rw [h, map_one]
  · right; apply f.injective; rw [h, map_neg, map_one]

/-- **Proposition `prop:dl-central-scalars`** (Lie algebra part). Over a field `K` of
characteristic other than two, some automorphism of `DL K` acts on its centre
`span(e₇, e₈)` as multiplication by `ζ` if and only if `ζ = ±1`. -/
theorem exists_aut_center_smul_iff (h2 : (2 : K) ≠ 0) (ζ : K) :
    (∃ φ : DL K ≃ₗ⁅K⁆ DL K, ∀ z ∈ LieAlgebra.center K (DL K), φ z = ζ • z) ↔
      ζ = 1 ∨ ζ = -1 := by
  constructor
  · rintro ⟨φ, hφ⟩
    exact scalar_of_equiv h2 φ ζ hφ
  · rintro (rfl | rfl)
    · exact ⟨LieEquiv.refl, fun z _ => by simp⟩
    · exact ⟨signEquiv, signEquiv_center⟩

end Main

end QSearch.DixmierLister
