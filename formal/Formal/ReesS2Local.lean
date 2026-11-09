import Mathlib.FieldTheory.Finite.Basic
import Mathlib.RingTheory.RootsOfUnity.PrimitiveRoots
import Mathlib.GroupTheory.SpecificGroups.Cyclic
import Mathlib.Tactic.NormNum.Prime

/-!
# Rees Schedule 2: local obstructions and small exceptional primes

Source: `docs/papers/rees-hsp/appendix-schedule2.tex`, Subsection `app:s2-local`
(Lemma `lem:app-s2-two-rows`, Proposition `prop:app-s2-cyclotomic` (i) and (ii),
Lemma `lem:app-s2-divisor`), with the definitions of Subsections `app:s2-gcd` and
`app:s2-contraction` and Lemma `lem:app-s2-normal`. AI-written, pending human review.

## Definitions (faithful to the appendix)

Fix a prime `p`, `κ ≥ 1` with `κ ∣ p - 1` and `h = (p - 1)/κ`.

* `IsCosetGen κ ξ`: `ξ ^ h` is a primitive `κ`-th root of unity (a *coset generator*).
* `MemQo ξ m x`: `x ∈ Q°_m = ξ^m Q_0 ∪ {0}`, written `x = ξ ^ m.val * w ^ κ` for some
  `w` (with `w = 0` giving `0`); `MemQ ξ m x`: `x ∈ Q_m`, that is `x ≠ 0 ∧ MemQo ξ m x`.
  `Q°_0` is the set of `κ`-th powers and does not depend on `ξ`.
* `z ξ m = ξ ^ m.val`, and `InWW ξ X`: the matrix `X` has all rows and all columns in
  `W = {w : ∑ z_m w_m = 0}`, that is `X ∈ W ⊗ W` (the reading of condition (b) of
  `lem:app-s2-tensor`).
* `IsContraction ξ C`: every `C i j ∈ Q°_0`, `C 0 0 ≠ 0`, and `∑ C_ij X_ij = 0` for every
  `X ∈ W ⊗ W` (the Definition in `app:s2-contraction`).
* `E2 κ`: the primes `p ≡ 1 (mod κ)` such that for **every** coset generator `ξ` there
  is no two-level contraction. `mem_E2_iff_exists` shows this equals the reading "for
  some coset generator" (the paper's remark that existence does not depend on `ξ`,
  `hasContraction_transfer`), using that coset generators exist (`exists_cosetGen`).
* `A ξ u v = #{w ∈ Q_u : w - 1 ∈ Q_v}` (computable, so small instances are decided).

## Main results

* `hasContraction_iff` (`lem:app-s2-normal`, both directions): a contraction is the
  same as a pair `(α, β)` with `α_j + β_i ∈ Q°_{-(i+j)}` and `α_0 + β_0 ≠ 0`.
* `beta_injective`, `alpha_injective`, `two_rows_diff` (`lem:app-s2-two-rows`).
* `exists_A_witness`, `no_contraction_of_A_eq_zero`, `mem_E2_of_A_eq_zero`
  (`prop:app-s2-cyclotomic`(i)).
* `card_pairs_le` and `mem_E2_of_le` (`prop:app-s2-cyclotomic`(ii)): every prime
  `p ≡ 1 (mod κ)` with `p ≤ κ² - 3κ + 3` (as integers) lies in `E_2(κ)`.
* `mem_E2_of_dvd` (`lem:app-s2-divisor`): for `D ∣ κ`, `p ∈ E_2(D)` implies
  `p ∈ E_2(κ)` (for `p ≡ 1 (mod κ)`).
* Small instances, checked by `decide` (no `native_decide`): `13, 29 ∈ E_2(4)` by (i);
  `5 ∈ E_2(4)`, `11 ∈ E_2(5)`, `7, 13, 19 ∈ E_2(6)`, `29 ∈ E_2(7)`, `17, 41 ∈ E_2(8)`,
  `19, 37 ∈ E_2(9)` by (ii); `7 ∉ E_2(3)` and `3 ∉ E_2(2)` by explicit contractions.

Not formalized: part (iii) of `prop:app-s2-cyclotomic` (it needs the Weil bound), the
finite computations of Remark `rem:app-s2-local-scope`, and anything about thresholds.
-/

namespace QSearch.ReesS2Local

open Finset

section Defs

variable {p κ : ℕ}

/-- `z_m = ξ ^ m`, with `m ∈ Z/κ` read as its representative in `[0, κ)`. -/
def z (ξ : ZMod p) (m : ZMod κ) : ZMod p := ξ ^ m.val

/-- `x ∈ Q°_m = ξ^m Q_0 ∪ {0}`: `x = ξ^m w^κ` for some `w` (`w = 0` gives `x = 0`). -/
def MemQo (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Prop :=
  ∃ w : ZMod p, x = ξ ^ m.val * w ^ κ

/-- `x ∈ Q_m = ξ^m Q_0`. -/
def MemQ (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Prop := x ≠ 0 ∧ MemQo ξ m x

/-- `ξ` is a coset generator: `ξ ^ ((p - 1)/κ)` has exact multiplicative order `κ`. -/
def IsCosetGen (κ : ℕ) (ξ : ZMod p) : Prop := IsPrimitiveRoot (ξ ^ ((p - 1) / κ)) κ

variable [NeZero κ]

/-- `X ∈ W ⊗ W`: every column and every row of `X` lies in `W = {w : ∑ z_m w_m = 0}`. -/
def InWW (ξ : ZMod p) (X : ZMod κ → ZMod κ → ZMod p) : Prop :=
  (∀ j, ∑ i, z ξ i * X i j = 0) ∧ (∀ i, ∑ j, z ξ j * X i j = 0)

/-- A two-level contraction at `(p, κ)` for the coset generator `ξ`. -/
structure IsContraction (ξ : ZMod p) (C : ZMod κ → ZMod κ → ZMod p) : Prop where
  mem : ∀ i j, MemQo ξ (0 : ZMod κ) (C i j)
  ne_zero : C 0 0 ≠ 0
  annihilates : ∀ X, InWW ξ X → ∑ i, ∑ j, C i j * X i j = 0

/-- Some two-level contraction exists for `ξ`. -/
def HasContraction (κ : ℕ) [NeZero κ] (ξ : ZMod p) : Prop :=
  ∃ C : ZMod κ → ZMod κ → ZMod p, IsContraction ξ C

/-- `E_2(κ)`: primes `p ≡ 1 (mod κ)` at which no two-level contraction exists (for any
coset generator; see `mem_E2_iff_exists` for the equivalent "some generator" form). -/
def E2 (κ : ℕ) [NeZero κ] : Set ℕ :=
  {p | p.Prime ∧ p ≡ 1 [MOD κ] ∧ ∀ ξ : ZMod p, IsCosetGen κ ξ → ¬HasContraction κ ξ}

end Defs

section Decidable

variable {p κ : ℕ} [NeZero p]

instance decMemQo (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Decidable (MemQo ξ m x) :=
  inferInstanceAs (Decidable (∃ w : ZMod p, x = ξ ^ m.val * w ^ κ))

instance decMemQ (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Decidable (MemQ ξ m x) :=
  inferInstanceAs (Decidable (x ≠ 0 ∧ MemQo ξ m x))

/-- The cyclotomic count `A(u, v) = #{w ∈ Q_u : w - 1 ∈ Q_v}`. -/
def A (ξ : ZMod p) (u v : ZMod κ) : ℕ :=
  (univ.filter fun w : ZMod p => MemQ ξ u w ∧ MemQ ξ v (w - 1)).card

end Decidable

section Cosets

variable {p : ℕ} {κ : ℕ} {ξ : ZMod p}

theorem z_zero (ξ : ZMod p) : z ξ (0 : ZMod κ) = 1 := by simp [z]

theorem z_ne_zero [Fact p.Prime] (hξ : ξ ≠ 0) (i : ZMod κ) : z ξ i ≠ 0 := pow_ne_zero _ hξ

theorem memQo_zero_iff {x : ZMod p} : MemQo ξ (0 : ZMod κ) x ↔ ∃ w, x = w ^ κ := by
  simp [MemQo]

theorem memQo_zero_elem [NeZero κ] (m : ZMod κ) : MemQo ξ m 0 :=
  ⟨0, by rw [zero_pow (NeZero.ne κ), mul_zero]⟩

/-- Any natural exponent normalises: `ξ^k w^κ ∈ Q°_{k mod κ}`. -/
theorem memQo_natCast (k : ℕ) (w : ZMod p) :
    MemQo ξ ((k : ℕ) : ZMod κ) (ξ ^ k * w ^ κ) := by
  refine ⟨ξ ^ (k / κ) * w, ?_⟩
  rw [ZMod.val_natCast, mul_pow, ← pow_mul, ← mul_assoc, ← pow_add, Nat.mod_add_div']

theorem memQo_of_eq {x : ZMod p} {m : ZMod κ} (k : ℕ) (hk : ((k : ℕ) : ZMod κ) = m)
    (w : ZMod p) (hx : x = ξ ^ k * w ^ κ) : MemQo ξ m x := by
  subst hk hx; exact memQo_natCast k w

theorem memQo_z (i : ZMod κ) : MemQo ξ i (z ξ i) := ⟨1, by simp [z]⟩

theorem memQo_mul [NeZero κ] {m n : ZMod κ} {x y : ZMod p} (hx : MemQo ξ m x) (hy : MemQo ξ n y) :
    MemQo ξ (m + n) (x * y) := by
  obtain ⟨a, rfl⟩ := hx
  obtain ⟨b, rfl⟩ := hy
  refine memQo_of_eq (m.val + n.val) ?_ (a * b) ?_
  · rw [Nat.cast_add, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val]
  · rw [pow_add, mul_pow]; ring

theorem memQo_of_index_eq {m n : ZMod κ} {x : ZMod p} (h : m = n) (hx : MemQo ξ m x) :
    MemQo ξ n x := h ▸ hx

/-- Multiplying by `ξ^k` shifts the coset index by `k`. -/
theorem memQo_pow_mul_iff [Fact p.Prime] [NeZero κ] (hξ : ξ ≠ 0) (k : ℕ) {m : ZMod κ}
    {y : ZMod p} : MemQo ξ m (ξ ^ k * y) ↔ MemQo ξ (m - (k : ZMod κ)) y := by
  constructor
  · rintro ⟨w, hw⟩
    have hke : k + k * (κ - 1) = k * κ := by
      obtain ⟨c, hc⟩ := Nat.exists_eq_succ_of_ne_zero (NeZero.ne κ)
      rw [hc, Nat.succ_sub_one, Nat.mul_succ, add_comm]
    refine memQo_of_eq (m.val + k * (κ - 1)) ?_ ((ξ⁻¹) ^ k * w) ?_
    · rw [Nat.cast_add, Nat.cast_mul, Nat.cast_sub (Nat.one_le_iff_ne_zero.mpr (NeZero.ne κ)),
        ZMod.natCast_self, ZMod.natCast_zmod_val, Nat.cast_one]
      ring
    · apply mul_left_cancel₀ (pow_ne_zero k hξ)
      have h1 : ξ ^ (k * κ) * (ξ⁻¹) ^ (k * κ) = 1 := by
        rw [← mul_pow, mul_inv_cancel₀ hξ, one_pow]
      calc ξ ^ k * y = ξ ^ m.val * w ^ κ := hw
        _ = ξ ^ m.val * w ^ κ * (ξ ^ (k * κ) * (ξ⁻¹) ^ (k * κ)) := by rw [h1, mul_one]
        _ = ξ ^ k * (ξ ^ (m.val + k * (κ - 1)) * ((ξ⁻¹) ^ k * w) ^ κ) := by
          rw [mul_pow, ← pow_mul, ← hke]
          simp only [pow_add]
          ring
  · intro hy
    have hk : MemQo ξ ((k : ℕ) : ZMod κ) (ξ ^ k) := memQo_of_eq k rfl 1 (by simp)
    exact memQo_of_index_eq (by ring) (memQo_mul hk hy)

/-- `z_i z_j y ∈ Q°_0` iff `y ∈ Q°_{-(i+j)}` (the last claim of `lem:app-s2-normal`). -/
theorem memQo_zz_iff [Fact p.Prime] [NeZero κ] (hξ : ξ ≠ 0) (i j : ZMod κ) {y : ZMod p} :
    MemQo ξ (0 : ZMod κ) (z ξ i * z ξ j * y) ↔ MemQo ξ (-(i + j)) y := by
  have hzz : z ξ i * z ξ j * y = ξ ^ (i.val + j.val) * y := by simp [z, pow_add]
  have hidx : (0 : ZMod κ) - ((i.val + j.val : ℕ) : ZMod κ) = -(i + j) := by
    rw [Nat.cast_add, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val]; ring
  rw [hzz, memQo_pow_mul_iff hξ, hidx]

variable [hp : Fact p.Prime] [NeZero κ] (hκp : κ ∣ p - 1)
include hκp

omit hp [NeZero κ] in
theorem mul_div_eq : κ * ((p - 1) / κ) = p - 1 := Nat.mul_div_cancel' hκp

omit [NeZero κ] in
theorem div_pos' : 0 < (p - 1) / κ := by
  have hp1 : 0 < p - 1 := Nat.sub_pos_of_lt hp.out.one_lt
  rcases Nat.eq_zero_or_pos ((p - 1) / κ) with h | h
  · have := mul_div_eq hκp; rw [h, mul_zero] at this; omega
  · exact h

omit hκp [NeZero κ] in
/-- `(ZMod p)ˣ` is cyclic: a primitive `(p - 1)`-th root of unity exists. -/
theorem exists_primitiveRoot : ∃ g : ZMod p, IsPrimitiveRoot g (p - 1) := by
  obtain ⟨g, hg⟩ := IsCyclic.exists_generator (α := (ZMod p)ˣ)
  refine ⟨g, ?_⟩
  rw [IsPrimitiveRoot.coe_units_iff]
  have h := orderOf_eq_card_of_forall_mem_zpowers hg
  rw [Nat.card_eq_fintype_card, ZMod.card_units] at h
  rw [← h]
  exact IsPrimitiveRoot.orderOf g

omit [NeZero κ] in
/-- The kernel of `x ↦ x ^ h` on `(ZMod p)^×` consists of `κ`-th powers. -/
theorem exists_pow_of_pow_eq_one {y : ZMod p} (hy : y ≠ 0) (h1 : y ^ ((p - 1) / κ) = 1) :
    ∃ w, y = w ^ κ := by
  have hκh : κ * ((p - 1) / κ) = p - 1 := mul_div_eq hκp
  have hpos : 0 < (p - 1) / κ := div_pos' hκp
  generalize (p - 1) / κ = h at h1 hκh hpos
  obtain ⟨g, hg⟩ := exists_primitiveRoot (p := p)
  have : NeZero (p - 1) := ⟨(Nat.sub_pos_of_lt hp.out.one_lt).ne'⟩
  obtain ⟨n, -, rfl⟩ := hg.eq_pow_of_pow_eq_one (ZMod.pow_card_sub_one_eq_one hy)
  rw [← pow_mul, hg.pow_eq_one_iff_dvd, ← hκh] at h1
  obtain ⟨c, rfl⟩ := Nat.dvd_of_mul_dvd_mul_right hpos h1
  exact ⟨g ^ c, by rw [← pow_mul, mul_comm]⟩

omit [NeZero κ] in
theorem kpow_pow_h {w : ZMod p} (hw : w ≠ 0) : (w ^ κ) ^ ((p - 1) / κ) = 1 := by
  rw [← pow_mul, mul_div_eq hκp, ZMod.pow_card_sub_one_eq_one hw]

theorem ne_zero_of_cosetGen (hgen : IsCosetGen κ ξ) : ξ ≠ 0 := by
  rintro rfl
  exact hgen.ne_zero (NeZero.ne κ) (zero_pow (div_pos' hκp).ne')

/-- Coset test: for `x ≠ 0`, `x ∈ Q_m` iff `x ^ h = ζ ^ m` with `ζ = ξ ^ h`. -/
theorem memQo_iff_pow {x : ZMod p} (hx : x ≠ 0) (m : ZMod κ) :
    MemQo ξ m x ↔ x ^ ((p - 1) / κ) = (ξ ^ ((p - 1) / κ)) ^ m.val := by
  constructor
  · rintro ⟨w, rfl⟩
    have hw : w ≠ 0 := by rintro rfl; simp [zero_pow (NeZero.ne κ)] at hx
    rw [mul_pow, kpow_pow_h hκp hw, mul_one, ← pow_mul, ← pow_mul, mul_comm]
  · intro h
    have hξm : ξ ^ m.val ≠ 0 := by
      intro h0
      rw [← pow_mul, mul_comm, pow_mul, h0, zero_pow (div_pos' hκp).ne'] at h
      exact pow_ne_zero _ hx h
    have hy : x * (ξ ^ m.val)⁻¹ ≠ 0 := mul_ne_zero hx (inv_ne_zero hξm)
    have h1 : (x * (ξ ^ m.val)⁻¹) ^ ((p - 1) / κ) = 1 := by
      have hcomm : (ξ ^ ((p - 1) / κ)) ^ m.val = (ξ ^ m.val) ^ ((p - 1) / κ) := by
        rw [← pow_mul, ← pow_mul, mul_comm]
      rw [mul_pow, h, hcomm, inv_pow, mul_inv_cancel₀ (pow_ne_zero _ hξm)]
    obtain ⟨w, hw⟩ := exists_pow_of_pow_eq_one hκp hy h1
    refine ⟨w, ?_⟩
    rw [← hw, mul_comm x, ← mul_assoc, mul_inv_cancel₀ hξm, one_mul]

/-- The cosets cover `(ZMod p)^×`. -/
theorem exists_index (hgen : IsCosetGen κ ξ) {x : ZMod p} (hx : x ≠ 0) :
    ∃ m : ZMod κ, MemQo ξ m x := by
  have hroot : (x ^ ((p - 1) / κ)) ^ κ = 1 := by
    rw [← pow_mul, mul_comm, mul_div_eq hκp, ZMod.pow_card_sub_one_eq_one hx]
  obtain ⟨i, hi, hζ⟩ := hgen.eq_pow_of_pow_eq_one hroot
  refine ⟨(i : ZMod κ), (memQo_iff_pow hκp hx _).mpr ?_⟩
  rw [ZMod.val_natCast, Nat.mod_eq_of_lt hi, hζ]

/-- The cosets are pairwise disjoint. -/
theorem index_unique (hgen : IsCosetGen κ ξ) {x : ZMod p} (hx : x ≠ 0) {m n : ZMod κ}
    (hm : MemQo ξ m x) (hn : MemQo ξ n x) : m = n := by
  rw [memQo_iff_pow hκp hx] at hm hn
  exact ZMod.val_injective _ (hgen.pow_inj (ZMod.val_lt m) (ZMod.val_lt n) (hm.symm.trans hn))

end Cosets

section NormalForm

variable {p : ℕ} {κ : ℕ} [NeZero κ] {ξ : ZMod p}

/-- A decoupled matrix `C_ij = z_i z_j (α_j + β_i)` annihilates `W ⊗ W`. -/
theorem annihilates_of_decoupled (α β : ZMod κ → ZMod p) {X : ZMod κ → ZMod κ → ZMod p}
    (hX : InWW ξ X) : ∑ i, ∑ j, z ξ i * z ξ j * (α j + β i) * X i j = 0 := by
  obtain ⟨hcol, hrow⟩ := hX
  have h1 : ∑ i, ∑ j, z ξ j * α j * (z ξ i * X i j) = 0 := by
    rw [Finset.sum_comm]
    exact Finset.sum_eq_zero fun j _ => by rw [← Finset.mul_sum, hcol j, mul_zero]
  have h2 : ∑ i, ∑ j, z ξ i * β i * (z ξ j * X i j) = 0 :=
    Finset.sum_eq_zero fun i _ => by rw [← Finset.mul_sum, hrow i, mul_zero]
  calc _ = ∑ i, ∑ j, (z ξ j * α j * (z ξ i * X i j) + z ξ i * β i * (z ξ j * X i j)) :=
        Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => by ring
    _ = 0 := by simp only [Finset.sum_add_distrib, h1, h2, add_zero]

/-- The test vector `e_i / z_i - e_0 / z_0` of `W`. -/
def testVec (ξ : ZMod p) (i : ZMod κ) (a : ZMod κ) : ZMod p :=
  (if a = i then (z ξ i)⁻¹ else 0) - (if a = 0 then 1 else 0)

theorem sum_mul_testVec (ξ : ZMod p) (f : ZMod κ → ZMod p) (i : ZMod κ) :
    ∑ a, f a * testVec ξ i a = f i * (z ξ i)⁻¹ - f 0 := by
  simp [testVec, mul_sub, Finset.sum_sub_distrib, mul_ite]

theorem sum_z_testVec [Fact p.Prime] (hξ : ξ ≠ 0) (i : ZMod κ) :
    ∑ a, z ξ a * testVec ξ i a = 0 := by
  rw [sum_mul_testVec, mul_inv_cancel₀ (z_ne_zero hξ i), z_zero, sub_self]

/-- `lem:app-s2-normal`, hard direction: a matrix annihilating `W ⊗ W` is decoupled.
Pairing with the rank-one test tensors `(e_i/z_i - e_0)(e_j/z_j - e_0)^T` gives
`C_ij/(z_i z_j) = C_i0/z_i + C_0j/z_j - C_00`. -/
theorem decoupled_of_annihilates [Fact p.Prime] (hξ : ξ ≠ 0) {C : ZMod κ → ZMod κ → ZMod p}
    (hC : ∀ X, InWW ξ X → ∑ i, ∑ j, C i j * X i j = 0) :
    ∃ α β : ZMod κ → ZMod p, ∀ i j, C i j = z ξ i * z ξ j * (α j + β i) := by
  refine ⟨fun j => C 0 j * (z ξ j)⁻¹ - C 0 0, fun i => C i 0 * (z ξ i)⁻¹, fun i j => ?_⟩
  have hX : InWW ξ (fun a b => testVec ξ i a * testVec ξ j b) := by
    refine ⟨fun b => ?_, fun a => ?_⟩
    · simp only [← mul_assoc, ← Finset.sum_mul, sum_z_testVec hξ, zero_mul]
    · simp only [mul_left_comm (z ξ _), ← Finset.mul_sum, sum_z_testVec hξ, mul_zero]
  have hpair := hC _ hX
  have hinner : ∀ a, ∑ b, C a b * (testVec ξ i a * testVec ξ j b) =
      testVec ξ i a * (C a j * (z ξ j)⁻¹ - C a 0) := by
    intro a
    rw [← sum_mul_testVec ξ (C a) j, Finset.mul_sum]
    exact Finset.sum_congr rfl fun b _ => by ring
  simp only [hinner] at hpair
  rw [show (∑ a, testVec ξ i a * (C a j * (z ξ j)⁻¹ - C a 0)) =
      ∑ a, (C a j * (z ξ j)⁻¹ - C a 0) * testVec ξ i a from
      Finset.sum_congr rfl fun a _ => mul_comm _ _, sum_mul_testVec] at hpair
  have hzi := z_ne_zero (κ := κ) hξ i
  have hzj := z_ne_zero (κ := κ) hξ j
  have hrel : C i j * (z ξ j)⁻¹ * (z ξ i)⁻¹ = (C 0 j * (z ξ j)⁻¹ - C 0 0) +
      C i 0 * (z ξ i)⁻¹ := by linear_combination hpair
  beta_reduce
  calc C i j = C i j * (z ξ i * (z ξ i)⁻¹) * (z ξ j * (z ξ j)⁻¹) := by
        rw [mul_inv_cancel₀ hzi, mul_inv_cancel₀ hzj, mul_one, mul_one]
    _ = z ξ i * z ξ j * (C i j * (z ξ j)⁻¹ * (z ξ i)⁻¹) := by ring
    _ = _ := by rw [hrel]

/-- **`lem:app-s2-normal`.** For `ξ ≠ 0`, a two-level contraction exists iff there are
`α, β` with `α_j + β_i ∈ Q°_{-(i+j)}` for all `i, j` and `α_0 + β_0 ≠ 0`. -/
theorem hasContraction_iff [Fact p.Prime] (hξ : ξ ≠ 0) :
    HasContraction κ ξ ↔ ∃ α β : ZMod κ → ZMod p,
      (∀ i j, MemQo ξ (-(i + j)) (α j + β i)) ∧ α 0 + β 0 ≠ 0 := by
  constructor
  · rintro ⟨C, hC⟩
    obtain ⟨α, β, hαβ⟩ := decoupled_of_annihilates hξ hC.annihilates
    refine ⟨α, β, fun i j => ?_, ?_⟩
    · rw [← memQo_zz_iff hξ, ← hαβ]; exact hC.mem i j
    · have := hC.ne_zero; rwa [hαβ, z_zero, one_mul, one_mul] at this
  · rintro ⟨α, β, hmem, h0⟩
    refine ⟨fun i j => z ξ i * z ξ j * (α j + β i), fun i j => ?_, ?_, fun X hX => ?_⟩
    · exact (memQo_zz_iff hξ i j).mpr (hmem i j)
    · simpa [z_zero] using h0
    · exact annihilates_of_decoupled α β hX

end NormalForm

section TwoRows

variable {p : ℕ} [Fact p.Prime] {κ : ℕ} [NeZero κ] {ξ : ZMod p} (hκp : κ ∣ p - 1)
  (hgen : IsCosetGen κ ξ) {α β : ZMod κ → ZMod p}
  (hC : ∀ i j, MemQo ξ (-(i + j)) (α j + β i)) (h0 : α 0 + β 0 ≠ 0)
include hκp hgen hC h0

/-- `lem:app-s2-two-rows`, first claim: the `β_i` are pairwise distinct. -/
theorem beta_injective : Function.Injective β := by
  intro i k hik
  by_contra hne
  have hzero : ∀ j, α j + β i = 0 := by
    intro j
    by_contra hx
    have := index_unique hκp hgen hx (hC i j) (by rw [hik]; exact hC k j)
    exact hne (by simpa using this)
  have hd : ∀ j, α j + β 0 = β 0 - β i := fun j => by linear_combination hzero j
  have hi := hC 0 i
  have hk := hC 0 k
  rw [hd] at hi hk
  by_cases hb : β 0 - β i = 0
  · exact h0 (by linear_combination hzero 0 + hb)
  · exact hne (by simpa using index_unique hκp hgen hb hi hk)

/-- `lem:app-s2-two-rows`, second claim: the `α_j` are pairwise distinct. -/
theorem alpha_injective : Function.Injective α := by
  intro j l hjl
  by_contra hne
  have hzero : ∀ i, α j + β i = 0 := by
    intro i
    by_contra hx
    have := index_unique hκp hgen hx (hC i j) (by rw [hjl]; exact hC i l)
    exact hne (by simpa using this)
  have hd : ∀ i, α 0 + β i = α 0 - α j := fun i => by linear_combination hzero i
  have hj := hC j 0
  have hl := hC l 0
  rw [hd] at hj hl
  by_cases hb : α 0 - α j = 0
  · exact h0 (by linear_combination hzero 0 + hb)
  · exact hne (by simpa using index_unique hκp hgen hb hj hl)

/-- `lem:app-s2-two-rows`, main claim: `Q°_{-i} - Q°_{-k} ⊇ (ZMod p)^×` for `i ≠ k`. -/
theorem two_rows_diff {i k : ZMod κ} (hik : i ≠ k) {x : ZMod p} (hx : x ≠ 0) :
    ∃ a b, MemQo ξ (-i) a ∧ MemQo ξ (-k) b ∧ x = a - b := by
  have hd : β i - β k ≠ 0 :=
    sub_ne_zero.mpr fun h => hik (beta_injective hκp hgen hC h0 h)
  obtain ⟨m, hm⟩ := exists_index hκp hgen (mul_ne_zero hx (inv_ne_zero hd))
  refine ⟨x * (β i - β k)⁻¹ * (α m + β i), x * (β i - β k)⁻¹ * (α m + β k),
    memQo_of_index_eq (by ring) (memQo_mul hm (hC i m)),
    memQo_of_index_eq (by ring) (memQo_mul hm (hC k m)), ?_⟩
  rw [← mul_sub, show α m + β i - (α m + β k) = β i - β k by ring, mul_assoc,
    inv_mul_cancel₀ hd, mul_one]

end TwoRows

section Cyclotomic

variable {p : ℕ} [Fact p.Prime] {κ : ℕ} [NeZero κ] {ξ : ZMod p} (hκp : κ ∣ p - 1)
  (hgen : IsCosetGen κ ξ)
include hκp hgen

/-- The core of `prop:app-s2-cyclotomic`(i): if a contraction exists for `ξ`, then
`A(u, v) ≥ 1` (an explicit witness) for every `u ≠ 0`, `v ≠ ε`, `u ≠ v`, where
`-1 ∈ Q_ε`. -/
theorem exists_A_witness (hcon : HasContraction κ ξ) {ε u v : ZMod κ}
    (hε : MemQo ξ ε (-1)) (hu : u ≠ 0) (hv : v ≠ ε) (huv : u ≠ v) :
    ∃ w, MemQ ξ u w ∧ MemQ ξ v (w - 1) := by
  have hξ := ne_zero_of_cosetGen hκp hgen
  obtain ⟨α, β, hC, h0⟩ := (hasContraction_iff hξ).mp hcon
  set c : ZMod κ := -u with hc
  set b : ZMod κ := v - u with hb
  have hb0 : b ≠ 0 := sub_ne_zero.mpr huv.symm
  have hrow : (0 : ZMod κ) ≠ -b := fun h => hb0 (by simpa using h.symm)
  have hx : z ξ c ≠ 0 := z_ne_zero hξ c
  obtain ⟨a, y, ha, hy, hxy⟩ := two_rows_diff hκp hgen hC h0 hrow hx
  rw [neg_zero] at ha
  rw [neg_neg] at hy
  by_cases ha0 : a = 0
  · -- `z = -y`: then `y = (-1) z ∈ Q_{ε + c}`, forcing `v = ε`.
    exfalso
    have hy' : y = -1 * z ξ c := by rw [hxy, ha0]; ring
    have hy0 : y ≠ 0 := by rw [hy']; exact mul_ne_zero (neg_ne_zero.mpr one_ne_zero) hx
    have h1 : MemQo ξ (ε + c) y := hy' ▸ memQo_mul hε (memQo_z c)
    have := index_unique hκp hgen hy0 hy h1
    exact hv (by rw [hb, hc] at this; linear_combination this)
  by_cases hy0 : y = 0
  · -- `z = a ∈ Q_0 ∩ Q_c`, forcing `u = 0`.
    exfalso
    have hxa : z ξ c = a := by rw [hxy, hy0, sub_zero]
    have := index_unique hκp hgen hx (hxa ▸ ha) (memQo_z c)
    exact hu (by rw [hc] at this; linear_combination this)
  · -- `w = a / z` is counted by `A(u, v)`.
    refine ⟨a * (z ξ c)⁻¹, ⟨mul_ne_zero ha0 (inv_ne_zero hx), ?_⟩, ?_, ?_⟩
    · have hza : ξ ^ c.val * (a * (z ξ c)⁻¹) = a := by
        rw [show ξ ^ c.val = z ξ c from rfl, mul_comm a, ← mul_assoc,
          mul_inv_cancel₀ hx, one_mul]
      have := (memQo_pow_mul_iff hξ c.val).mp (hza.symm ▸ ha)
      exact memQo_of_index_eq (by rw [ZMod.natCast_zmod_val, hc]; ring) this
    · have : a * (z ξ c)⁻¹ - 1 = y * (z ξ c)⁻¹ := by
        rw [hxy] at hx ⊢
        field_simp
        ring
      rw [this]; exact mul_ne_zero hy0 (inv_ne_zero hx)
    · have hzy : ξ ^ c.val * (a * (z ξ c)⁻¹ - 1) = y := by
        rw [show ξ ^ c.val = z ξ c from rfl, mul_sub, mul_one, mul_comm a, ← mul_assoc,
          mul_inv_cancel₀ hx, one_mul, hxy]
        ring
      have := (memQo_pow_mul_iff hξ c.val).mp (hzy.symm ▸ hy)
      exact memQo_of_index_eq (by rw [ZMod.natCast_zmod_val, hb, hc]; ring) this

/-- **`prop:app-s2-cyclotomic`(i), for a fixed coset generator.** If `A(u, v) = 0` for
some `u ≠ 0`, `v ≠ ε`, `u ≠ v` (with `-1 ∈ Q_ε`), then no contraction exists for `ξ`. -/
theorem no_contraction_of_A_eq_zero {ε u v : ZMod κ} (hε : MemQo ξ ε (-1)) (hu : u ≠ 0)
    (hv : v ≠ ε) (huv : u ≠ v) (hA : A ξ u v = 0) : ¬HasContraction κ ξ := by
  intro hcon
  obtain ⟨w, hw⟩ := exists_A_witness hκp hgen hcon hε hu hv huv
  rw [A, Finset.card_eq_zero, Finset.filter_eq_empty_iff] at hA
  exact hA (Finset.mem_univ w) hw

omit hgen in
/-- **The paper's remark after the Definition of `E_2`:** existence of a contraction
does not depend on the coset generator. (Any nonzero `ξ'` receives one.) -/
theorem hasContraction_transfer (hgen : IsCosetGen κ ξ) {ξ' : ZMod p} (hξ' : ξ' ≠ 0)
    (hcon : HasContraction κ ξ) : HasContraction κ ξ' := by
  have hξ := ne_zero_of_cosetGen hκp hgen
  obtain ⟨u, q, hq⟩ := exists_index hκp hgen hξ'
  obtain ⟨α, β, hC, h0⟩ := (hasContraction_iff hξ).mp hcon
  -- `z_{ξ'}(i) = z_ξ(u i) r_i^κ`.
  have hz : ∀ i : ZMod κ, ∃ r, z ξ' i = z ξ (u * i) * r ^ κ := by
    intro i
    refine ⟨ξ ^ (u.val * i.val / κ) * q ^ i.val, ?_⟩
    simp only [z, hq, ZMod.val_mul, mul_pow, ← pow_mul]
    rw [mul_comm κ i.val, pow_mul q i.val κ, ← mul_assoc, ← pow_add, Nat.mod_add_div']
  refine ⟨fun i j => z ξ' i * z ξ' j * (α (u * j) + β (u * i)), fun i j => ?_, ?_,
    fun X hX => annihilates_of_decoupled _ _ hX⟩
  · obtain ⟨ri, hri⟩ := hz i
    obtain ⟨rj, hrj⟩ := hz j
    obtain ⟨w, hw⟩ := memQo_zero_iff.mp ((memQo_zz_iff hξ (u * i) (u * j)).mpr (hC _ _))
    refine memQo_zero_iff.mpr ⟨ri * rj * w, ?_⟩
    rw [hri, hrj, mul_pow, mul_pow, ← hw]
    ring
  · simpa [z_zero] using h0

end Cyclotomic

section E2

variable {κ : ℕ} [NeZero κ]

omit [NeZero κ] in
theorem dvd_sub_one_of_modEq {p : ℕ} (hp : p.Prime) (h : p ≡ 1 [MOD κ]) : κ ∣ p - 1 :=
  (Nat.modEq_iff_dvd' hp.one_lt.le).mp h.symm

omit [NeZero κ] in
/-- Coset generators exist: every primitive root `g` of `(ZMod p)^×` is one. -/
theorem exists_cosetGen {p : ℕ} [Fact p.Prime] (hκp : κ ∣ p - 1) :
    ∃ ξ : ZMod p, IsCosetGen κ ξ := by
  obtain ⟨g, hg⟩ := exists_primitiveRoot (p := p)
  refine ⟨g, ?_⟩
  have hh := div_pos' (p := p) hκp
  have h := hg.pow_of_dvd hh.ne' (Nat.div_dvd_of_dvd hκp)
  rwa [Nat.div_div_self hκp (Nat.sub_pos_of_lt (Fact.out : p.Prime).one_lt).ne'] at h

/-- `E_2(κ)` does not depend on the reading of "no contraction": for every coset
generator, or for some coset generator. -/
theorem mem_E2_iff_exists {p : ℕ} :
    p ∈ E2 κ ↔ p.Prime ∧ p ≡ 1 [MOD κ] ∧
      ∃ ξ : ZMod p, IsCosetGen κ ξ ∧ ¬HasContraction κ ξ := by
  constructor
  · rintro ⟨hp, hmod, hall⟩
    have := Fact.mk hp
    obtain ⟨ξ, hξ⟩ := exists_cosetGen (κ := κ) (dvd_sub_one_of_modEq hp hmod)
    exact ⟨hp, hmod, ξ, hξ, hall ξ hξ⟩
  · rintro ⟨hp, hmod, ξ, hξ, hno⟩
    have := Fact.mk hp
    have hκp := dvd_sub_one_of_modEq hp hmod
    refine ⟨hp, hmod, fun ξ' hξ' hcon => hno ?_⟩
    exact hasContraction_transfer hκp hξ' (ne_zero_of_cosetGen hκp hξ) hcon

/-- **`prop:app-s2-cyclotomic`(i).** If, for one coset generator `ξ` (with `-1 ∈ Q_ε`),
`A(u, v) = 0` for some `u ≠ 0`, `v ≠ ε`, `u ≠ v`, then `p ∈ E_2(κ)`. -/
theorem mem_E2_of_A_eq_zero {p : ℕ} [Fact p.Prime] (hmod : p ≡ 1 [MOD κ]) {ξ : ZMod p}
    (hgen : IsCosetGen κ ξ) {ε u v : ZMod κ} (hε : MemQo ξ ε (-1)) (hu : u ≠ 0)
    (hv : v ≠ ε) (huv : u ≠ v) (hA : A ξ u v = 0) : p ∈ E2 κ := by
  have hp : p.Prime := Fact.out
  exact mem_E2_iff_exists.mpr ⟨hp, hmod, ξ, hgen,
    no_contraction_of_A_eq_zero (dvd_sub_one_of_modEq hp hmod) hgen hε hu hv huv hA⟩

/-- The counting step of `prop:app-s2-cyclotomic`(ii): if a contraction exists, the
`≥ (κ - 1)(κ - 2)` admissible pairs `(u, v)` have pairwise distinct witnesses
`w ∉ {0, 1}`, so `(κ - 1)(κ - 2) ≤ p - 2`. -/
theorem card_pairs_le {p : ℕ} [Fact p.Prime] (hκp : κ ∣ p - 1) {ξ : ZMod p}
    (hgen : IsCosetGen κ ξ) (hcon : HasContraction κ ξ) : (κ - 1) * (κ - 2) ≤ p - 2 := by
  classical
  obtain ⟨ε, hε⟩ := exists_index hκp hgen (neg_ne_zero.mpr (one_ne_zero (α := ZMod p)))
  set S : Finset (Σ _ : ZMod κ, ZMod κ) :=
    (univ.erase 0).sigma fun u => (univ.erase ε).erase u with hS
  have hw : ∀ s ∈ S, ∃ w, MemQ ξ s.1 w ∧ MemQ ξ s.2 (w - 1) := by
    rintro ⟨u, v⟩ hs
    simp only [hS, Finset.mem_sigma, Finset.mem_erase, Finset.mem_univ, and_true] at hs
    exact exists_A_witness hκp hgen hcon hε hs.1 hs.2.2 (Ne.symm hs.2.1)
  choose! f hf using hw
  set T : Finset (ZMod p) := (univ.erase 0).erase 1 with hT
  have hcardT : T.card = p - 2 := by
    rw [hT, Finset.card_erase_of_mem (Finset.mem_erase.mpr ⟨one_ne_zero, Finset.mem_univ _⟩),
      Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, ZMod.card]
    omega
  have hcardS : (κ - 1) * (κ - 2) ≤ S.card := by
    rw [hS, Finset.card_sigma]
    have hc : (univ.erase (0 : ZMod κ)).card = κ - 1 := by
      rw [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, ZMod.card]
    have hle : ∀ u ∈ univ.erase (0 : ZMod κ), κ - 2 ≤ ((univ.erase ε).erase u).card := by
      intro u _
      have h1 := Finset.pred_card_le_card_erase (s := univ.erase ε) (a := u)
      rw [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, ZMod.card] at h1
      omega
    have := Finset.card_nsmul_le_sum _ _ _ hle
    rwa [hc, smul_eq_mul] at this
  have hST : S.card ≤ T.card := by
    refine Finset.card_le_card_of_injOn f (fun s hs => ?_) (fun s hs t ht hst => ?_)
    · obtain ⟨⟨h0, -⟩, ⟨h1, -⟩⟩ := hf s hs
      simp only [hT, Finset.coe_erase, Finset.coe_univ, Set.mem_sdiff, Set.mem_univ,
        Set.mem_singleton_iff, true_and]
      exact ⟨h0, fun h => h1 (by rw [h, sub_self])⟩
    · obtain ⟨⟨hs0, hs1⟩, ⟨hs2, hs3⟩⟩ := hf s hs
      obtain ⟨⟨-, ht1⟩, ⟨-, ht3⟩⟩ := hf t ht
      rw [hst] at hs1 hs3 hs0 hs2
      have e1 := index_unique hκp hgen hs0 hs1 ht1
      have e2 := index_unique hκp hgen hs2 hs3 ht3
      exact Sigma.ext e1 (heq_of_eq e2)
  omega

/-- **`prop:app-s2-cyclotomic`(ii).** Every prime `p ≡ 1 (mod κ)` with
`p ≤ κ² - 3κ + 3` lies in `E_2(κ)`. -/
theorem mem_E2_of_le (hκ : 2 ≤ κ) {p : ℕ} (hp : p.Prime) (hmod : p ≡ 1 [MOD κ])
    (hle : (p : ℤ) ≤ (κ : ℤ) ^ 2 - 3 * κ + 3) : p ∈ E2 κ := by
  have := Fact.mk hp
  refine ⟨hp, hmod, fun ξ hgen hcon => ?_⟩
  have h := card_pairs_le (dvd_sub_one_of_modEq hp hmod) hgen hcon
  obtain ⟨m, rfl⟩ : ∃ m, κ = m + 2 := ⟨κ - 2, by omega⟩
  have h2 := hp.two_le
  rw [show m + 2 - 1 = m + 1 by omega, show m + 2 - 2 = m by omega] at h
  have h3 : ((m + 1) * m + 2 : ℤ) ≤ p := by
    have : (m + 1) * m + 2 ≤ p := by
      generalize (m + 1) * m = t at h; omega
    exact_mod_cast this
  push_cast at hle
  nlinarith

/-- `lem:app-s2-divisor`, contraction form: a contraction at `κ` for `ξ` restricts to a
contraction at any `D ∣ κ` for the same `ξ` (entries `C_{ij}`, `0 ≤ i, j < D`). -/
theorem hasContraction_of_dvd {p : ℕ} [Fact p.Prime] {D : ℕ} [NeZero D] (hDκ : D ∣ κ)
    {ξ : ZMod p} (hξ : ξ ≠ 0) (hcon : HasContraction κ ξ) : HasContraction D ξ := by
  obtain ⟨C, hC⟩ := hcon
  obtain ⟨α, β, hαβ⟩ := decoupled_of_annihilates hξ hC.annihilates
  have hDle : D ≤ κ := Nat.le_of_dvd (Nat.pos_of_ne_zero (NeZero.ne κ)) hDκ
  let ι : ZMod D → ZMod κ := fun i => ((i.val : ℕ) : ZMod κ)
  have hι : ∀ i : ZMod D, z ξ (ι i) = z ξ i := by
    intro i
    simp only [z, ι, ZMod.val_natCast, Nat.mod_eq_of_lt ((ZMod.val_lt i).trans_le hDle)]
  have hι0 : ι 0 = 0 := by simp [ι]
  refine ⟨fun i j => C (ι i) (ι j), fun i j => ?_, ?_, fun X hX => ?_⟩
  · obtain ⟨w, hw⟩ := memQo_zero_iff.mp (hC.mem (ι i) (ι j))
    refine memQo_zero_iff.mpr ⟨w ^ (κ / D), ?_⟩
    rw [hw, ← pow_mul, Nat.div_mul_cancel hDκ]
  · simpa only [hι0] using hC.ne_zero
  · have := annihilates_of_decoupled (ξ := ξ) (fun j => α (ι j)) (fun i => β (ι i)) hX
    rw [← this]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    rw [hαβ, hι, hι]

/-- A coset generator for `κ` is one for every `D ∣ κ`. -/
theorem isCosetGen_of_dvd {p : ℕ} {D : ℕ} [NeZero D] (hDκ : D ∣ κ) (hκp : κ ∣ p - 1)
    {ξ : ZMod p} (hgen : IsCosetGen κ ξ) : IsCosetGen D ξ := by
  obtain ⟨e, he⟩ := hDκ
  obtain ⟨h, hh⟩ := hκp
  have hD : 0 < D := Nat.pos_of_ne_zero (NeZero.ne D)
  have he0 : e ≠ 0 := by
    rintro rfl; rw [mul_zero] at he; exact NeZero.ne κ he
  have h1 : (p - 1) / κ = h := by
    rw [hh, Nat.mul_div_cancel_left _ (Nat.pos_of_ne_zero (NeZero.ne κ))]
  have h2 : (p - 1) / D = h * e := by
    rw [hh, he, Nat.mul_assoc, Nat.mul_div_cancel_left _ hD, mul_comm]
  unfold IsCosetGen at hgen ⊢
  rw [h1, he] at hgen
  rw [h2, pow_mul]
  have := hgen.pow_of_dvd he0 (Dvd.intro_left D rfl)
  rwa [Nat.mul_div_cancel _ (Nat.pos_of_ne_zero he0)] at this

/-- **`lem:app-s2-divisor`.** Let `D ∣ κ` and let `p ≡ 1 (mod κ)` be prime. If
`p ∈ E_2(D)`, then `p ∈ E_2(κ)`. -/
theorem mem_E2_of_dvd {D : ℕ} [NeZero D] (hDκ : D ∣ κ) {p : ℕ} (hmod : p ≡ 1 [MOD κ])
    (hpD : p ∈ E2 D) : p ∈ E2 κ := by
  obtain ⟨hp, -, hall⟩ := hpD
  have := Fact.mk hp
  have hκp := dvd_sub_one_of_modEq hp hmod
  refine ⟨hp, hmod, fun ξ hgen hcon => hall ξ (isCosetGen_of_dvd hDκ hκp hgen) ?_⟩
  exact hasContraction_of_dvd hDκ (ne_zero_of_cosetGen hκp hgen) hcon

end E2

/-! ## Small instances (`decide`, no `native_decide`) -/

section Instances

theorem isCosetGen_of_lt {p κ : ℕ} {ξ : ZMod p} (hκ : 0 < κ)
    (h1 : (ξ ^ ((p - 1) / κ)) ^ κ = 1)
    (h : ∀ l : ℕ, 0 < l → l < κ → (ξ ^ ((p - 1) / κ)) ^ l ≠ 1) : IsCosetGen κ ξ :=
  IsPrimitiveRoot.mk_of_lt _ hκ h1 h

instance fact_prime_13 : Fact (Nat.Prime 13) := ⟨by norm_num⟩
instance fact_prime_29 : Fact (Nat.Prime 29) := ⟨by norm_num⟩
instance fact_prime_7 : Fact (Nat.Prime 7) := ⟨by norm_num⟩

/-- `13 ∈ E_2(4)` by `prop:app-s2-cyclotomic`(i): `ξ = 2`, `ε = 2`, `A(1, 3) = 0`. -/
theorem thirteen_mem_E2_four : 13 ∈ E2 4 :=
  mem_E2_of_A_eq_zero (ξ := (2 : ZMod 13)) (ε := 2) (u := 1) (v := 3) (by decide)
    (isCosetGen_of_lt (by norm_num) (by decide) (by
      intro l h0 hl; interval_cases l <;> decide))
    (by decide) (by decide) (by decide) (by decide) (by decide)

/-- `29 ∈ E_2(4)` by `prop:app-s2-cyclotomic`(i): `ξ = 2`, `ε = 2`, `A(2, 0) = 0`. -/
theorem twentynine_mem_E2_four : 29 ∈ E2 4 :=
  mem_E2_of_A_eq_zero (ξ := (2 : ZMod 29)) (ε := 2) (u := 2) (v := 0) (by decide)
    (isCosetGen_of_lt (by norm_num) (by decide) (by
      intro l h0 hl; interval_cases l <;> decide))
    (by decide) (by decide) (by decide) (by decide) (by decide)

theorem five_mem_E2_four : 5 ∈ E2 4 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem eleven_mem_E2_five : 11 ∈ E2 5 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem seven_mem_E2_six : 7 ∈ E2 6 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem thirteen_mem_E2_six : 13 ∈ E2 6 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem nineteen_mem_E2_six : 19 ∈ E2 6 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem twentynine_mem_E2_seven : 29 ∈ E2 7 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem seventeen_mem_E2_eight : 17 ∈ E2 8 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem fortyone_mem_E2_eight : 41 ∈ E2 8 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem nineteen_mem_E2_nine : 19 ∈ E2 9 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)
theorem thirtyseven_mem_E2_nine : 37 ∈ E2 9 := mem_E2_of_le (by norm_num) (by norm_num) (by decide) (by norm_num)

/-- Non-vacuity: `7 ∉ E_2(3)`, by the contraction `α = (1, 0, 3)`, `β = (0, 4, 6)` for
the coset generator `ξ = 3` (this contraction has zero entries, as every one at
`(7, 3)` must). -/
theorem seven_not_mem_E2_three : 7 ∉ E2 3 := by
  rintro ⟨-, -, hall⟩
  apply hall 3 (isCosetGen_of_lt (by norm_num) (by decide) (by
    intro l h0 hl; interval_cases l <;> decide))
  refine (hasContraction_iff (by decide)).mpr
    ⟨fun j : ZMod 3 => ![(1 : ZMod 7), 0, 3] j, fun i : ZMod 3 => ![(0 : ZMod 7), 4, 6] i,
      by decide, by decide⟩

instance fact_prime_3 : Fact (Nat.Prime 3) := ⟨by norm_num⟩

/-- Non-vacuity at `κ = 2`: `3 ∉ E_2(2)` (`α = (1, 0)`, `β = (0, 1)`, `ξ = 2`). Note that
`mem_E2_of_le` is stated over `ℤ`: with truncated `ℕ` subtraction, `κ² - 3κ + 3` would
read `3` instead of `1` at `κ = 2` and would wrongly cover `p = 3`. -/
theorem three_not_mem_E2_two : 3 ∉ E2 2 := by
  rintro ⟨-, -, hall⟩
  apply hall 2 (isCosetGen_of_lt (by norm_num) (by decide) (by
    intro l h0 hl; obtain rfl : l = 1 := by omega
    decide))
  refine (hasContraction_iff (by decide)).mpr
    ⟨fun j : ZMod 2 => ![(1 : ZMod 3), 0] j, fun i : ZMod 2 => ![(0 : ZMod 3), 1] i,
      by decide, by decide⟩

end Instances

end QSearch.ReesS2Local
