# Rees HSP paper: the local obstructions of Schedule 2 in Lean (`ReesS2Local`)

5 November 2026. AI-only pass (Claude Code subagent). Machine-checked in Lean; AI-run,
pending human review. No `.tex` file, registry JSON, claim gate, `AGENT_HANDOFF.md`,
`STATE.md` or `formal/README.md` was edited. Edits: the new file
`formal/Formal/ReesS2Local.lean`, one import line in `formal/Formal.lean`, and one import
line plus 14 guards in `formal/Formal/Audit.lean`. No git, no network, no `lake update`.

Source: `docs/papers/rees-hsp/appendix-schedule2.tex`, Subsection `app:s2-local`
(Lemma `lem:app-s2-two-rows`, Proposition `prop:app-s2-cyclotomic`, Lemma
`lem:app-s2-divisor`, Remark `rem:app-s2-local-scope`), with the definitions of
Subsections `app:s2-gcd` and `app:s2-contraction` and Lemma `lem:app-s2-normal`.

## 1. Summary

Formalized, with no `sorry` and no new axioms (every guard prints exactly
`[propext, Classical.choice, Quot.sound]`):

* the definitions of `Q_m`, `Q°_m`, coset generator, `W ⊗ W`, two-level contraction,
  `E_2(κ)` and the cyclotomic count `A(u,v)`;
* Lemma `lem:app-s2-normal`, both directions (needed to apply the two-row lemma to an
  actual contraction);
* the independence of contraction existence from the coset generator (the paragraph
  after the Definition), and existence of coset generators, so `E_2(κ)` can be read
  with "every" or "some" generator (`mem_E2_iff_exists`);
* Lemma `lem:app-s2-two-rows` (all three claims);
* Proposition `prop:app-s2-cyclotomic` (i) and (ii), the headline
  "`p ≤ κ² − 3κ + 3` implies `p ∈ E_2(κ)`";
* Lemma `lem:app-s2-divisor`;
* small instances by `decide` (no `native_decide`): `13, 29 ∈ E_2(4)` via (i);
  `5 ∈ E_2(4)`, `11 ∈ E_2(5)`, `7, 13, 19 ∈ E_2(6)`, `29 ∈ E_2(7)`, `17, 41 ∈ E_2(8)`,
  `19, 37 ∈ E_2(9)` via (ii); `7 ∉ E_2(3)` and `3 ∉ E_2(2)` via explicit contractions
  (non-vacuity of the definition).

Not formalized: part (iii) of `prop:app-s2-cyclotomic` (needs the Weil bound, which is
not in Mathlib in this form), the finite computations and the threshold
`((r−1)κ^r+2)^2` of Remark `rem:app-s2-local-scope`, and anything about thresholds,
schedules or running time.

## 2. Definitions (namespace `QSearch.ReesS2Local`)

Indices `m : ZMod κ` are read through `m.val ∈ [0, κ)`.

```lean
def z (ξ : ZMod p) (m : ZMod κ) : ZMod p := ξ ^ m.val
def MemQo (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Prop := ∃ w : ZMod p, x = ξ ^ m.val * w ^ κ
def MemQ (ξ : ZMod p) (m : ZMod κ) (x : ZMod p) : Prop := x ≠ 0 ∧ MemQo ξ m x
def IsCosetGen (κ : ℕ) (ξ : ZMod p) : Prop := IsPrimitiveRoot (ξ ^ ((p - 1) / κ)) κ
def InWW (ξ : ZMod p) (X : ZMod κ → ZMod κ → ZMod p) : Prop :=
  (∀ j, ∑ i, z ξ i * X i j = 0) ∧ (∀ i, ∑ j, z ξ j * X i j = 0)
structure IsContraction (ξ : ZMod p) (C : ZMod κ → ZMod κ → ZMod p) : Prop where
  mem : ∀ i j, MemQo ξ (0 : ZMod κ) (C i j)
  ne_zero : C 0 0 ≠ 0
  annihilates : ∀ X, InWW ξ X → ∑ i, ∑ j, C i j * X i j = 0
def HasContraction (κ : ℕ) [NeZero κ] (ξ : ZMod p) : Prop := ∃ C, IsContraction ξ C
def E2 (κ : ℕ) [NeZero κ] : Set ℕ :=
  {p | p.Prime ∧ p ≡ 1 [MOD κ] ∧ ∀ ξ : ZMod p, IsCosetGen κ ξ → ¬HasContraction κ ξ}
def A (ξ : ZMod p) (u v : ZMod κ) : ℕ :=
  (univ.filter fun w : ZMod p => MemQ ξ u w ∧ MemQ ξ v (w - 1)).card
```

Match with the paper:

* `Q°_m = ξ^m Q_0 ∪ {0}` is `MemQo` (the witness `w = 0` gives `0`); `Q°_0` is the set
  of `κ`-th powers, independent of `ξ`. That the `Q_m` partition `F_p^×` is proved
  (`exists_index`, `index_unique`), from `IsCosetGen` and `κ ∣ p − 1`, via the coset test
  `x ∈ Q_m ⇔ x^h = ζ^m` (`memQo_iff_pow`).
* `IsCosetGen` is the paper's "ζ = ξ^h has exact multiplicative order κ".
* `X ∈ W ⊗ W` is formalized as "every row and every column of `X` lies in `W`". This is
  the identification the paper itself uses in condition (b) of `lem:app-s2-tensor`; it is
  not proved in Lean to coincide with a Mathlib `TensorProduct`.
* `E2` quantifies over **every** coset generator. `mem_E2_iff_exists` proves it equal to
  the "some coset generator" reading, so the definition matches the paper's
  ξ-dependent definition together with its independence remark. It is non-vacuous:
  coset generators exist (`exists_cosetGen`) and explicit contractions show
  `7 ∉ E2 3`, `3 ∉ E2 2`.
* `ε = ind(−1)` enters as a hypothesis `MemQo ξ ε (-1)` (it exists and is unique by
  `exists_index`, `index_unique`).

## 3. Lean statements of the main results

```lean
-- lem:app-s2-normal (both directions; ξ ≠ 0 suffices)
theorem hasContraction_iff [Fact p.Prime] (hξ : ξ ≠ 0) :
    HasContraction κ ξ ↔ ∃ α β : ZMod κ → ZMod p,
      (∀ i j, MemQo ξ (-(i + j)) (α j + β i)) ∧ α 0 + β 0 ≠ 0

-- lem:app-s2-two-rows (common hypotheses: κ ∣ p - 1, IsCosetGen κ ξ,
-- hC : ∀ i j, MemQo ξ (-(i + j)) (α j + β i), h0 : α 0 + β 0 ≠ 0)
theorem beta_injective  : Function.Injective β
theorem alpha_injective : Function.Injective α
theorem two_rows_diff {i k : ZMod κ} (hik : i ≠ k) {x : ZMod p} (hx : x ≠ 0) :
    ∃ a b, MemQo ξ (-i) a ∧ MemQo ξ (-k) b ∧ x = a - b

-- prop:app-s2-cyclotomic (i)
theorem exists_A_witness (hκp : κ ∣ p - 1) (hgen : IsCosetGen κ ξ)
    (hcon : HasContraction κ ξ) {ε u v : ZMod κ} (hε : MemQo ξ ε (-1))
    (hu : u ≠ 0) (hv : v ≠ ε) (huv : u ≠ v) : ∃ w, MemQ ξ u w ∧ MemQ ξ v (w - 1)
theorem no_contraction_of_A_eq_zero ... (hA : A ξ u v = 0) : ¬HasContraction κ ξ
theorem mem_E2_of_A_eq_zero [Fact p.Prime] (hmod : p ≡ 1 [MOD κ]) (hgen : IsCosetGen κ ξ)
    (hε : MemQo ξ ε (-1)) (hu : u ≠ 0) (hv : v ≠ ε) (huv : u ≠ v) (hA : A ξ u v = 0) :
    p ∈ E2 κ

-- prop:app-s2-cyclotomic (ii)
theorem card_pairs_le [Fact p.Prime] (hκp : κ ∣ p - 1) (hgen : IsCosetGen κ ξ)
    (hcon : HasContraction κ ξ) : (κ - 1) * (κ - 2) ≤ p - 2
theorem mem_E2_of_le (hκ : 2 ≤ κ) {p : ℕ} (hp : p.Prime) (hmod : p ≡ 1 [MOD κ])
    (hle : (p : ℤ) ≤ (κ : ℤ) ^ 2 - 3 * κ + 3) : p ∈ E2 κ

-- lem:app-s2-divisor
theorem mem_E2_of_dvd {D : ℕ} [NeZero D] (hDκ : D ∣ κ) {p : ℕ} (hmod : p ≡ 1 [MOD κ])
    (hpD : p ∈ E2 D) : p ∈ E2 κ

-- independence of ξ (paragraph after the Definition) and existence of generators
theorem hasContraction_transfer (hκp : κ ∣ p - 1) (hgen : IsCosetGen κ ξ) {ξ' : ZMod p}
    (hξ' : ξ' ≠ 0) (hcon : HasContraction κ ξ) : HasContraction κ ξ'
theorem mem_E2_iff_exists : p ∈ E2 κ ↔
    p.Prime ∧ p ≡ 1 [MOD κ] ∧ ∃ ξ : ZMod p, IsCosetGen κ ξ ∧ ¬HasContraction κ ξ
```

(`κ : ℕ` carries `[NeZero κ]` throughout, which `ZMod κ` needs to be a `Fintype`.)

## 4. Differences from the paper's statements and proofs

1. **(ii), hypotheses identical; the bound is stated over `ℤ`.** With truncated `ℕ`
   subtraction, `κ^2 - 3*κ + 3` evaluates to `3` instead of `1` at `κ = 2` and would
   wrongly cover `p = 3` (`3 ∉ E_2(2)` is checked). The proof is the paper's: if a
   contraction exists, the `≥ (κ−1)(κ−2)` pairs `(u,v)` with `u ≠ 0`, `v ≠ ε`, `u ≠ v`
   have witnesses `w ∉ {0,1}` (from (i)), pairwise distinct because the cosets are
   disjoint, so `(κ−1)(κ−2) ≤ p − 2`. Lean uses only this lower bound on the number of
   pairs, not the exact counts `(κ−1)(κ−2)` / `κ²−3κ+3`, and only `≤ p − 2` for
   `Σ A(u,v)` (by injectivity), not the identity `Σ A(u,v) = p − 2`.
2. **(i)** is proved per coset generator (`no_contraction_of_A_eq_zero`), exactly as in
   the paper, and lifted to `p ∈ E2 κ` with the transfer lemma. The proof uses the rows
   `0` and `−b` only, which is the paper's argument without the final shift by
   `ξ^{-i}`.
3. **Divisor lemma.** Lean needs `D ≥ 1` (`NeZero D`) instead of `D ≥ 2`; this is a
   weakening of a hypothesis, not a change. The proof restricts the matrix `C` itself
   to the indices `0 ≤ i, j < D` (entries remain `κ`-th, hence `D`-th, powers; the
   restricted matrix is decoupled, hence annihilates `W_D ⊗ W_D`), instead of going
   through the coset form `α_j + β_i ∈ Q^{(D)}_{-(i+j)}`. As in the paper, `ξ` is shown to
   be a coset generator for `D` (`isCosetGen_of_dvd`), and no `gcd(D, κ/D) = 1`
   hypothesis is needed.
4. **Normal form.** The hard direction (an annihilator of `W ⊗ W` is decoupled) is
   proved by pairing `C` with the rank-one test tensors
   `(e_i/z_i − e_0)(e_j/z_j − e_0)^T`, which gives
   `C_ij/(z_iz_j) = C_i0/z_i + C_0j/z_j − C_00` directly, instead of the paper's dimension
   count. Both directions need only `ξ ≠ 0`.
5. **Transfer.** Proved for any nonzero `ξ'`, not only for coset generators
   `ξ' = ξ^u q` with `gcd(u, κ) = 1`: with `ξ' ∈ Q_u`, the matrix
   `z'_i z'_j (α_{uj} + β_{ui})` is a contraction for `ξ'`. Coprimality of `u` is not
   needed for this direction.
6. **Two rows.** As stated. The cover `⋃_j ξ^j d Q_0 = F_p^×` is `exists_index`.

## 5. Build commands and results

All commands from `formal/`, with `PATH=$HOME/.elan/bin:$PATH`, one Lean process at a
time, under `nice -n 10` (machine load average about 130 to 150 during the pass).

| Command | Result |
|---|---|
| `lake env lean Formal/ReesS2Local.lean` (iteration) | final run: no output (no error or warning), about 7 s |
| `lake build --wfail Formal.ReesS2Local` | `Build completed successfully (2013 jobs)`, module 5.6 s |
| scratch file `#print axioms` on 24 declarations | all `[propext, Classical.choice, Quot.sound]` |
| `lake build --no-build Formal.Audit` (after the edits) | only `Formal.Audit` out of date; every other module replayed |
| `lake build --wfail Formal.Audit` | `Build completed successfully (3501 jobs)`, Audit 15 s |
| `lake build --wfail` (default target `Formal`) | `Build completed successfully (3525 jobs)` |

`grep` finds no `sorry`, `native_decide` or `axiom` in the new file (the two hits of
`native_decide` are the docstrings saying it is not used). No clean-copy build was run.

## 6. Guards

`formal/Formal/Audit.lean`: 538 → 552 `#print axioms` guards (+14), in the existing
`#guard_msgs (whitespace := lax)` style, all expecting
`[propext, Classical.choice, Quot.sound]`:
`hasContraction_iff`, `two_rows_diff`, `beta_injective`, `alpha_injective`,
`exists_A_witness`, `mem_E2_of_A_eq_zero`, `hasContraction_transfer`,
`mem_E2_iff_exists`, `card_pairs_le`, `mem_E2_of_le`, `mem_E2_of_dvd`,
`thirteen_mem_E2_four`, `twentynine_mem_E2_four`, `seven_not_mem_E2_three`.
`formal/Formal.lean` now imports `Formal.ReesS2Local` (after `Formal.ReesMergeReduction`).

If the paper's counts are updated, the guards for modules of the Lean table go from
`500` to `514`, with `38` unrelated guards, `552` in all.

## 7. Proposed paper text (not applied)

Row for `tab:lean-modules` in `main.tex`:

```latex
\texttt{ReesS2Local} & 14 & Subsection~\ref{app:s2-local}: Lemmas~\ref{lem:app-s2-two-rows} and~\ref{lem:app-s2-divisor} and Proposition~\ref{prop:app-s2-cyclotomic}(i),(ii), so every prime $p\equiv1\pmod\kappa$ with $p\le\kappa^2-3\kappa+3$ lies in $E_2(\kappa)$, with the normal form of Lemma~\ref{lem:app-s2-normal} and the independence of $E_2(\kappa)$ from $\xi$; part~(iii) is not checked \\
```

One sentence for the status line of `app:s2-local` or the formalization paragraph, if
wanted: "Lemmas~\ref{lem:app-s2-two-rows} and~\ref{lem:app-s2-divisor} and
Proposition~\ref{prop:app-s2-cyclotomic}(i),(ii) are also checked in Lean, in the module
\texttt{ReesS2Local} (\file{research/audits/reviews/2026-11-05-rees-lean-s2-local.md};
machine-checked in Lean; AI-run, pending human review); part~(iii) and the finite
computations of Remark~\ref{rem:app-s2-local-scope} are not."

## 8. Claim gates and next steps

No claim gate changes; nothing here bears on `formal_compiler_checked` or
`general_sde_implemented`. Possible follow-ups: a `formal/README.md` entry for the module
(left to the integrator, since the README is already modified in the working tree); an
independent review pass; (iii) would need a Weil-bound statement for the character sums
`K'(s,t)`, which Mathlib does not provide.
