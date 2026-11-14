import Formal.Schedule1H.Stage
import Mathlib.Data.ZMod.Basic
import Mathlib.GroupTheory.SpecificGroups.Cyclic

/-!
# Schedule 1H⁺, part 1: classes `cl_D`

Source: `docs/papers/rees-hsp/core/main-core.tex`, Section `sec:plus`, paragraph
"Classes".

The paper fixes a coset generator `ξ` and, for `D ∣ N_p`, defines `cl_D(x) ∈ ℤ_D` as the
unique `i` with `x ∈ ξ^i P_D`. It then uses only the following properties:
`cl_D(xy) = cl_D(x) + cl_D(y)`, `x ∈ P_D ⇔ cl_D(x) = 0`, and
`cl_{D'}(x) ≡ cl_D(x) (mod D')` for `D' ∣ D`; also `cl_D(ξ) = 1` (`ξ ∈ ξ^1 P_D`).

* `ClassMap K N` packages a function `cl : (D : ℕ) → K → ZMod D` with exactly these
  properties for all `D ∣ N` (the paper's `N = N_p`), together with `ξ`.
* `ClassMap.mem_coset` / `ClassMap.cl_unique` prove that such a `cl` *is* the paper's
  class: `x ∈ ξ^{cl_D(x)} P_D`, and `x ∈ ξ^i P_D` forces `cl_D(x) = i`. So `ClassMap`
  determines `cl` from `ξ` (no extra freedom).
* `ClassMap.ofGen` is a concrete instance over any finite field: `ξ = g` a generator of
  `Kˣ` (the paper's choice `ξ = g`, the least primitive root, for `p < 2·10^6`),
  `N = |K| - 1`, `cl_D(x) = log_g x mod D`.
* `ClassMap.cl_eq_zero_iff_pow`: over a finite field with `D h = |K| - 1`, class `0` is
  tested by `x^h = 1` (used by the decidable guards in `Audit.lean`).

The paper's general coset generator for `p ≥ 2·10^6` (not a primitive root) is covered by
the abstract structure, but no instance for it is constructed here.
-/

namespace QSearch.Schedule1HPlus

open QSearch.Schedule1H Finset

/-- **Classes** for moduli `D ∣ N`, with respect to `ξ`. -/
structure ClassMap (K : Type*) [Field K] (N : ℕ) where
  xi : K
  cl : (D : ℕ) → K → ZMod D
  N_pos : 0 < N
  xi_ne : xi ≠ 0
  cl_mul : ∀ {D : ℕ}, D ∣ N → ∀ {x y : K}, x ≠ 0 → y ≠ 0 → cl D (x * y) = cl D x + cl D y
  cl_eq_zero_iff : ∀ {D : ℕ}, D ∣ N → ∀ {x : K}, x ≠ 0 → (cl D x = 0 ↔ x ∈ Pow D)
  cl_cast : ∀ {D' D : ℕ}, D' ∣ D → D ∣ N → ∀ {x : K}, x ≠ 0 →
    cl D' x = ZMod.cast (cl D x)
  cl_xi : ∀ {D : ℕ}, D ∣ N → cl D xi = 1

variable {K : Type*} [Field K] {N : ℕ} (C : ClassMap K N)

namespace ClassMap

theorem pos_of_dvd (C : ClassMap K N) {D : ℕ} (hD : D ∣ N) : 0 < D := Nat.pos_of_dvd_of_pos hD C.N_pos

theorem neZero_of_dvd (C : ClassMap K N) {D : ℕ} (hD : D ∣ N) : NeZero D := ⟨(C.pos_of_dvd hD).ne'⟩

theorem cl_one {D : ℕ} (hD : D ∣ N) : C.cl D 1 = 0 := by
  have h := C.cl_mul hD (one_ne_zero (α := K)) one_ne_zero
  rw [mul_one] at h
  exact (add_eq_left.mp h.symm)

theorem cl_inv {D : ℕ} (hD : D ∣ N) {x : K} (hx : x ≠ 0) : C.cl D x⁻¹ = -C.cl D x := by
  have h := C.cl_mul hD hx (inv_ne_zero hx)
  rw [mul_inv_cancel₀ hx, C.cl_one hD] at h
  exact (neg_eq_of_add_eq_zero_right h.symm).symm

theorem cl_div {D : ℕ} (hD : D ∣ N) {x y : K} (hx : x ≠ 0) (hy : y ≠ 0) :
    C.cl D (x / y) = C.cl D x - C.cl D y := by
  rw [div_eq_mul_inv, C.cl_mul hD hx (inv_ne_zero hy), C.cl_inv hD hy, sub_eq_add_neg]

theorem cl_pow {D : ℕ} (hD : D ∣ N) {x : K} (hx : x ≠ 0) :
    ∀ n : ℕ, C.cl D (x ^ n) = (n : ZMod D) * C.cl D x
  | 0 => by simp [C.cl_one hD]
  | n + 1 => by
    rw [pow_succ, C.cl_mul hD (pow_ne_zero _ hx) hx, cl_pow hD hx n]
    push_cast; ring

theorem cl_xi_pow {D : ℕ} (hD : D ∣ N) (n : ℕ) : C.cl D (C.xi ^ n) = n := by
  rw [C.cl_pow hD C.xi_ne, C.cl_xi hD, mul_one]

theorem cl_of_mem_pow {D : ℕ} (hD : D ∣ N) {x : K} (hx : x ∈ Pow D) : C.cl D x = 0 :=
  (C.cl_eq_zero_iff hD hx.1).mpr hx

/-- `ξ^{i}` for `i ∈ ℤ_D`, read through the representative `i.val ∈ {0, …, D-1}` (the
paper's `z_m = ξ^m`). -/
def xiPow {D : ℕ} (i : ZMod D) : K := C.xi ^ i.val

theorem xiPow_ne {D : ℕ} (i : ZMod D) : C.xiPow i ≠ 0 := pow_ne_zero _ C.xi_ne

theorem cl_xiPow {D : ℕ} (hD : D ∣ N) (i : ZMod D) : C.cl D (C.xiPow i) = i := by
  haveI := C.neZero_of_dvd hD
  rw [xiPow, C.cl_xi_pow hD, ZMod.natCast_zmod_val]

theorem xiPow_zero {D : ℕ} : C.xiPow (0 : ZMod D) = 1 := by simp [xiPow]

/-- **The paper's definition of the class**: `x ∈ ξ^{cl_D(x)} P_D`. -/
theorem mem_coset {D : ℕ} (hD : D ∣ N) {x : K} (hx : x ≠ 0) :
    ∃ y ∈ Pow D, x = C.xiPow (C.cl D x) * y := by
  refine ⟨x / C.xiPow (C.cl D x), ?_, ?_⟩
  · have h0 : x / C.xiPow (C.cl D x) ≠ 0 := div_ne_zero hx (C.xiPow_ne _)
    refine (C.cl_eq_zero_iff hD h0).mp ?_
    rw [C.cl_div hD hx (C.xiPow_ne _), C.cl_xiPow hD, sub_self]
  · field_simp [C.xiPow_ne (C.cl D x)]

/-- **Uniqueness of the class**: `x = ξ^{i} y` with `y ∈ P_D` forces `cl_D(x) = i`. -/
theorem cl_unique {D : ℕ} (hD : D ∣ N) (i : ZMod D) {y : K} (hy : y ∈ Pow D) :
    C.cl D (C.xiPow i * y) = i := by
  rw [C.cl_mul hD (C.xiPow_ne i) hy.1, C.cl_xiPow hD, C.cl_of_mem_pow hD hy, add_zero]

/-- The paper's `lift_D(Ω') = {i ∈ ℤ_D : i mod D' ∈ Ω'}`. -/
def lift {D' : ℕ} (D : ℕ) (Ω' : Set (ZMod D')) : Set (ZMod D) :=
  {i | (ZMod.cast i : ZMod D') ∈ Ω'}

/-- The class of `x` mod `D'` lies in `Ω'` iff its class mod `D` lies in `lift_D(Ω')`. -/
theorem mem_lift_iff {D' D : ℕ} (h : D' ∣ D) (hD : D ∣ N) (Ω' : Set (ZMod D')) {x : K}
    (hx : x ≠ 0) : C.cl D x ∈ lift D Ω' ↔ C.cl D' x ∈ Ω' := by
  simp [lift, C.cl_cast h hD hx]

/-- Restrict a class map to a divisor of its modulus. -/
def restrict {N' : ℕ} (h : N' ∣ N) (hN' : 0 < N') : ClassMap K N' where
  xi := C.xi
  cl := C.cl
  N_pos := hN'
  xi_ne := C.xi_ne
  cl_mul hD := C.cl_mul (hD.trans h)
  cl_eq_zero_iff hD := C.cl_eq_zero_iff (hD.trans h)
  cl_cast h1 hD := C.cl_cast h1 (hD.trans h)
  cl_xi hD := C.cl_xi (hD.trans h)

section FiniteField

variable {K : Type*} [Field K] [Fintype K] [DecidableEq K]

/-- Over a finite field with `D h = |K| - 1`, `h > 0`: class `0` iff `x ^ h = 1`. -/
theorem mem_pow_iff_pow_eq_one {D h : ℕ} (hDh : D * h = Fintype.card K - 1) (hh : 0 < h)
    {x : K} (hx : x ≠ 0) : x ∈ Pow D ↔ x ^ h = 1 := by
  constructor
  · rintro ⟨_, r, rfl⟩
    have hr : r ≠ 0 := by
      rintro rfl
      apply hx
      have hD0 : D ≠ 0 := by
        rintro rfl
        have := Fintype.one_lt_card (α := K)
        omega
      exact zero_pow hD0
    exact pow_eq_one_of_root hDh hr
  · intro h1
    exact ⟨hx, exists_root_of_pow_eq_one hDh hh hx h1⟩

theorem cl_eq_zero_iff_pow (C : ClassMap K N) {D h : ℕ} (hD : D ∣ N)
    (hDh : D * h = Fintype.card K - 1) (hh : 0 < h) {x : K} (hx : x ≠ 0) :
    C.cl D x = 0 ↔ x ^ h = 1 := by
  rw [C.cl_eq_zero_iff hD hx, mem_pow_iff_pow_eq_one hDh hh hx]

/-- The discrete logarithm to base `g` (some exponent `k` with `g^k = x`; `0` if none). -/
noncomputable def dlog (g : K) (x : K) : ℕ :=
  open Classical in if h : ∃ k : ℕ, g ^ k = x then Nat.find h else 0

theorem pow_dlog {g x : K} (h : ∃ k : ℕ, g ^ k = x) : g ^ dlog g x = x := by
  classical
  unfold dlog
  rw [dite_eq_left h]
  exact Nat.find_spec h

/-- A generator of `Kˣ` reaches every nonzero element. -/
theorem exists_pow_of_gen {g : Kˣ} (hg : ∀ x : Kˣ, x ∈ Subgroup.zpowers g) {x : K}
    (hx : x ≠ 0) : ∃ k : ℕ, (g : K) ^ k = x := by
  obtain ⟨k, hk⟩ : ∃ k : ℕ, g ^ k = Units.mk0 x hx :=
    mem_powers_iff_mem_zpowers.mpr (hg (Units.mk0 x hx))
  exact ⟨k, by rw [← Units.val_pow_eq_pow_val, hk, Units.val_mk0]⟩

theorem orderOf_gen {g : Kˣ} (hg : ∀ x : Kˣ, x ∈ Subgroup.zpowers g) :
    orderOf g = Fintype.card K - 1 := by
  rw [orderOf_eq_card_of_forall_mem_zpowers hg, Nat.card_eq_fintype_card, Fintype.card_units]

theorem gen_pow_eq_pow_iff {g : Kˣ} (hg : ∀ x : Kˣ, x ∈ Subgroup.zpowers g) (a b : ℕ) :
    (g : K) ^ a = (g : K) ^ b ↔ a ≡ b [MOD Fintype.card K - 1] := by
  rw [← orderOf_gen hg, ← pow_eq_pow_iff_modEq, ← Units.val_pow_eq_pow_val,
    ← Units.val_pow_eq_pow_val, Units.val_inj]

/-- **The concrete class map of a generator `g` of `Kˣ`**: `cl_D(x) = log_g x mod D`. -/
noncomputable def ofGen (g : Kˣ) (hg : ∀ x : Kˣ, x ∈ Subgroup.zpowers g)
    (hK : 1 < Fintype.card K) : ClassMap K (Fintype.card K - 1) where
  xi := g
  cl D x := (dlog (g : K) x : ZMod D)
  N_pos := by omega
  xi_ne := g.ne_zero
  cl_mul := by
    intro D hD x y hx hy
    have h1 := pow_dlog (exists_pow_of_gen hg (mul_ne_zero hx hy))
    have h2 := pow_dlog (exists_pow_of_gen hg hx)
    have h3 := pow_dlog (exists_pow_of_gen hg hy)
    have : (g : K) ^ dlog (g : K) (x * y) = (g : K) ^ (dlog (g : K) x + dlog (g : K) y) := by
      rw [h1, pow_add, h2, h3]
    have hm := ((gen_pow_eq_pow_iff hg _ _).mp this).of_dvd hD
    rw [← Nat.cast_add, ZMod.natCast_eq_natCast_iff]
    exact hm
  cl_eq_zero_iff := by
    intro D hD x hx
    have h2 := pow_dlog (exists_pow_of_gen hg hx)
    rw [ZMod.natCast_eq_zero_iff]
    constructor
    · rintro ⟨k, hk⟩
      refine ⟨hx, (g : K) ^ k, ?_⟩
      rw [← pow_mul, mul_comm, ← hk, h2]
    · rintro ⟨_, r, rfl⟩
      have hr : r ≠ 0 := fun h0 => hx (by
        rw [h0]; exact zero_pow (M₀ := K) (Nat.pos_of_dvd_of_pos hD (by omega)).ne')
      obtain ⟨j, hj⟩ := exists_pow_of_gen hg hr
      have : (g : K) ^ dlog (g : K) (r ^ D) = (g : K) ^ (j * D) := by rw [h2, pow_mul, hj]
      have hm := ((gen_pow_eq_pow_iff hg _ _).mp this).of_dvd hD
      exact (Nat.modEq_zero_iff_dvd.mp (hm.trans (Nat.modEq_zero_iff_dvd.mpr
        (dvd_mul_left D j))))
  cl_cast := by
    intro D' D h _ x _
    rw [ZMod.cast_natCast h]
  cl_xi := by
    intro D hD
    have h1 := pow_dlog (exists_pow_of_gen hg g.ne_zero)
    have : (g : K) ^ dlog (g : K) (g : K) = (g : K) ^ 1 := by rw [h1, pow_one]
    have hm := ((gen_pow_eq_pow_iff hg _ _).mp this).of_dvd hD
    rw [← Nat.cast_one, ZMod.natCast_eq_natCast_iff]
    exact hm

/-- A unit of order `|K| - 1` generates `Kˣ`. -/
theorem gen_of_orderOf {g : Kˣ} (h : orderOf g = Fintype.card K - 1) :
    ∀ x : Kˣ, x ∈ Subgroup.zpowers g := by
  have htop : Subgroup.zpowers g = ⊤ := by
    apply Subgroup.eq_top_of_card_eq
    rw [Nat.card_zpowers, h, Nat.card_eq_fintype_card, Fintype.card_units]
  intro x; rw [htop]; exact Subgroup.mem_top x

end FiniteField

end ClassMap

end QSearch.Schedule1HPlus
