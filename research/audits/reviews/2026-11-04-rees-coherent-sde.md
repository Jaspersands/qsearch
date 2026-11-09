# Rees HSP: a coherent (reversible) linear-grade SDE solve

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels as in `2026-11-04-rees-circuit-arith.md`:
**[proved]** = written argument here; **[proof-by-computation]** = exhaustive check over ALL
inputs of the stated finite set; **[sampled]** = exact on a stated random subset only;
**[exact count]** = counted from the emitted gate list (or from exact per-macro closed forms);
**[argued]** = reasoning, not machine-checked.

Scope: the grades with κ_d = gcd(d, p−1) = 1 of Theorem `thm:power-sde`(i), where the
merge arity is M = g+1 columns λ_0, …, λ_g ∈ F_p^g (g = g_d, the paper's a) and the witness
is s_l = y_l^e with y a nonzero linear dependence and e·d ≡ 1 (mod p−1). Nothing here is
about the grades with κ_d ≥ 2 (Schedules 1–3); see Section 6.

This report is written incrementally; sections are appended as they are finished.

## 1. The canonical witness (definition)

Fix an odd prime p, g ≥ 1, and d with gcd(d, p−1) = 1. Let e ∈ {1, …, p−2} be the
representative of d^{−1} mod (p−1) (for p = 3, e = 1). Let A = [λ_0 | … | λ_g] ∈ F_p^{g×(g+1)}.

**Definition (first dependency).** Let

  j* = j*(A) = min { j ∈ {0, …, g} : λ_j ∈ span(λ_0, …, λ_{j−1}) }

(the empty span is {0}, so j* = 0 iff λ_0 = 0). Since λ_0, …, λ_{j*−1} are linearly
independent, there are unique c_0, …, c_{j*−1} ∈ F_p with λ_{j*} = Σ_{i<j*} c_i λ_i. Put

  y_i = −c_i (i < j*),   y_{j*} = 1,   y_i = 0 (i > j*),

and the canonical witness s = s(A) ∈ F_p^{g+1} by s_l = y_l^e. With the "z" representation used
by the circuit, z_l = −y_l (so z_i = c_i for i < j*, z_{j*} = p−1, z_i = 0 beyond), and since e is
odd, s_l = −(z_l^e).

**Lemma 1 [proved].** (a) j*(A) exists for every A, so s is a total function of the columns.
(b) y ≠ 0 and A y = 0. (c) s ≠ 0 and Σ_l s_l^d λ_l = 0. (d) y is the unique vector of ker A
with y_{j*} = 1 and y_i = 0 for i > j*; equivalently, it is the kernel vector read off from the
reduced row echelon form R of A at the first non-pivot column j* (y_{j*} = 1,
y_{piv(r)} = −R_{r, j*}, all other coordinates 0), and the pivots of R before j* are exactly the
columns 0, …, j*−1, in rows 0, …, j*−1.

*Proof.* (a) The set in the definition contains j = g: λ_0, …, λ_{g−1} either are dependent
(then some earlier j is in the set) or span F_p^g ∋ λ_g. (b) y_{j*} = 1, and
A y = λ_{j*} − Σ_{i<j*} c_i λ_i = 0. (c) e·d ≡ 1 (mod p−1) and e·d ≥ 1, so x^{ed} = x for every
x ∈ F_p (Fermat for x ≠ 0; 0^{ed} = 0). Hence s_l^d = y_l^{ed} = y_l and
Σ_l s_l^d λ_l = A y = 0; s_{j*} = 1^e = 1 ≠ 0. (d) If y' ∈ ker A has y'_{j*} = 1 and
y'_i = 0 for i > j*, then y − y' ∈ ker A is supported on {0, …, j*−1}, where the columns are
independent, so y = y'. For the RREF statement: column j is a pivot of R iff λ_j ∉
span(λ_0, …, λ_{j−1}) (row operations preserve all linear relations among columns), so the
first non-pivot is j*, the pivots before it are 0, …, j*−1 in rows 0, …, j*−1, and column j*
of R is (c_0, …, c_{j*−1}, 0, …, 0)^T; the RREF kernel vector at j* has the stated support
and value 1 at j*, so it is y by uniqueness. ∎

Remarks. (i) The witness depends on the column order only (it is a function of the tuple, as
the descent needs: `prop:descent` accepts every valid nonzero witness, branch by branch).
(ii) Rank deficiency needs no special case: zero columns, repeated columns and rank < g all
just make j* smaller. (iii) |supp s| = 1 + #{i < j* : c_i ≠ 0} ≥ 1; targets with s_i = 0 are
consumed and discarded by the descent, as in the paper. (iv) e is odd because e·d ≡ 1 mod the
even number p−1; this is what makes s_l = −(z_l^e).

## 2. The reversible construction

Module `theorems/rees_coherent_sde.py` (new). Encoding as in the generator: one F_p
coordinate = b = ⌈log2 p⌉ qubits, LSB first, canonical words < p. Gate set X, CX, CCX, SWAP
(SWAP only inside the arithmetic macros' modular doubling). Registers: inputs L[c][r]
(column c, row r), output S[c], and workspace. The circuit is

  U = F · C · F^{−1},

where F^{−1} is the reversed gate list of F (every gate is an involution), and C touches only
S, its own local temporaries (which it cleans) and the shared arithmetic ancillas (clean
between macros); it reads z but never writes a wire of F. Hence F^{−1} sees exactly the
state F produced (apart from S), and on every input U restores every wire other than S
[proved: F^{−1}F = id], so **the workspace returns to 0 and the inputs are restored
structurally**; the simulator checks it anyway.

Arithmetic macros (from `theorems/rees_circuit_arith.py`, imported, not edited):
`add_product(t, a, b, κ)`: t += κ·a·b mod p, exactly 40b²+2b CCX and at most 158b²+46b−4
gates; `add_scaled(t, a, κ)`: t += κ·a mod p, 10b²+8b+2H CCX and at most 40b²+44b+10 gates
(H = Σ_{i<b} hw(κ2^i mod p)). Both are guarded (identity if t is padding), never target their
operands, and return the 3b+5 ancillas to 0. A squaring is `add_product(t, x, x, 1)`: the
operands are only controls, so aliasing a = b is safe (t is always a fresh zero register).

**Forward pass F** (oblivious Gauss–Jordan with coherent pivoting):

0. Copy the columns into a workspace matrix W (g(g+1)·b CX). Set the flag act_0 = 1 (one X).
   Invariant before step k: act_k = [λ_0, …, λ_{k−1} independent], and when act_k = 1 the
   first k columns of W are e_0, …, e_{k−1} (RREF), with zeros below row k−1 in the earlier
   columns.
1. For k = 0, …, g−1:
   a. *Pivot search.* For r = k, …, g−1: nz_r = [W[r][k] ≠ 0] by an OR (X the bits, an AND
      ladder into the flag, X back; 2b−3 CCX for b ≥ 3, one CCX for b = 2, b−2 clean temps).
      Prefix chain z_k = act_k, sel_r = z_r ∧ nz_r (r > k), z_{r+1} = z_r ∧ ¬nz_r. Then
      dep_k = z_g = act_k ∧ [column k is 0 in rows k..g−1], and
      piv_k = act_{k+1} = act_k ⊕ dep_k (two CX). sel is one-hot: the FIRST nonzero row ≥ k
      (deterministic choice).
   b. *Controlled row swaps.* For r = k+1..g−1, Fredkin-swap rows k and r on columns k..g,
      controlled by sel_r (b·(g−1−k)(g+1−k) Fredkins, each CX·CCX·CX).
   c. *Fermat inverse.* u = W[k][k]; u_inv = u^{p−2} by left-to-right square-and-multiply
      into fresh registers (I_p = (bitlen(p−2)−1) + (hw(p−2)−1) products), CX-copied into a
      history register, then the chain is uncomputed by its reversed list (2I_p products per
      step, the chain registers are reused). 0^{p−2} = 0, so no branch.
   d. *Guarded multipliers.* w = piv ? u_inv : 1 and wi = piv ? u : 1 (2b CCX controlled on
      piv, the constant 1 loaded under ¬piv by X·CX·CX·X).
   e. *In-place normalisation of row k.* For c = k..g: t' = 0 + w·t (`add_product`), then
      t ← t − wi·t' (`add_product`, κ = −1), which is 0 because wi·w = 1 on both branches;
      relabel t' as W[k][c] and return the zeroed register to the pool. 2(g−k+1) products.
   f. *Elimination with stored multipliers.* For every row j ≠ k: m_j = piv ? W[j][k] : 0
      (b CCX, a history register), W[j][c] += (−1)·m_j·W[k][c] for c = k+1..g, and
      W[j][k] ^= m_j (b CX; equal values, so the entry becomes 0 when piv = 1, untouched when
      m_j = 0). (g−1)(g−k) products.
   When act_k = 0 every step is the identity on W (sel = 0, w = wi = 1, m = 0).
2. dep_g = act_g. Exactly one of dep_0, …, dep_g is 1 and it marks j* (Lemma 2).
3. *Selection.* z_i ^= W[i][k] controlled on dep_k (i < k), and z_k ^= p−1 controlled on
   dep_k (hw(p−1) CX), for every k: b·g(g+1)/2 CCX. Result: z = −y.

**Copy stage C.** For each l = 0..g: z_l^e by square-and-multiply (E_e = (bitlen(e)−1) +
(hw(e)−1) products; nothing if e = 1), `add_scaled(S[l], z_l^e, −1)`, chain uncomputed. Since e
is odd, −(z_l^e) = (−z_l)^e = y_l^e = s_l. For a nonzero initial S the circuit adds s to it
(the standard |x⟩|t⟩ → |x⟩|t + s(x)⟩ form).

**Lemma 2 [proved].** On every canonical input, after F: W holds the RREF data of Lemma 1(d)
in rows 0..j*−1 of column j*, dep is the indicator vector of j*, and z = −y.

*Proof.* Induction on k with the invariant of step 0. If act_k = 1: rows ≥ k of columns < k are
0, so λ_k ∈ span(λ_{<k}) iff column k of W is zero in rows ≥ k (the top-left block is the
identity and row operations preserve column relations). If it is zero, dep_k = 1,
act_{k+1} = 0, sel = 0, w = wi = 1, m = 0, so W is unchanged and k = j*. Otherwise sel marks the
first nonzero row r ≥ k, the swap brings it to row k (rows ≥ k have zeros in columns < k, so
swapping only columns ≥ k is the full row swap), u ≠ 0, w = u^{−1}, the normalisation makes
W[k][k] = 1, and the elimination clears column k in every other row, giving the invariant at
k+1. If act_k = 0 (j* < k) every substep is the identity, so W stays at the state reached at
j*. act is non-increasing, dep_k = act_k ∧ ¬act_{k+1} for k < g and dep_g = act_g, so exactly
one dep is 1 (telescoping), at j*. When j* = g all g pivots exist, W[0..g−1][0..g−1] = I and
column g holds c. Step 3 then writes z_i = W[i][j*] = c_i for i < j*, z_{j*} = p−1 = −1, and 0
elsewhere. ∎

**Theorem (coherent linear-grade SDE) [proved + proof-by-computation, AI-checked].** For
every odd prime p, g ≥ 1 and d with gcd(d, p−1) = 1, the gate list U of
`CoherentSDE(p, g, d)` maps |λ⟩|0⟩_S|0⟩_work ↦ |λ⟩|s(λ)⟩_S|0⟩_work on every canonical input λ,
with s the canonical witness of Lemma 1; s ≠ 0 and Σ s_l^d λ_l = 0. (Lemmas 1–2 plus the
correctness of the arithmetic macros on canonical inputs, which is [proof-by-computation] for
p ≤ 13 in the I146 report and [argued] beyond; Section 4 checks U itself exhaustively.)

## 3. Gate and qubit counts [exact count]

Notation: b = ⌈log2 p⌉, ℓ(n) = (bitlen(n) − 1) + (hw(n) − 1) (multiplications of
left-to-right square-and-multiply for x^n), I_p = ℓ(p−2) (Fermat inverse; 0 for p = 3),
E_e = ℓ(e) (0 for e = 1). Both are ≤ 2b−2.

**Macros (whole circuit U).** F has n_F = g(g+3) [normalisation, 2(g−k+1) at step k]
+ (g−1)g(g+1)/2 [elimination] + 2g·I_p [g inversions, each computed and uncomputed]
multiply-accumulates; C has 2(g+1)E_e products and g+1 `add_scaled` (κ = −1). Hence

  #add_product = P(g, p, d) = 2n_F + 2(g+1)E_e = g³ + 2g² + 5g + 4g·I_p + 2(g+1)E_e,
  #add_scaled = g+1,

so P ≤ g³ + 2g² + 5g + (12g+4)(b−1).

**Data-dependent pivoting (coherent).** OR flags: g(g+1)/2, each (2b−3) CCX (b ≥ 3; one CCX at
b = 2) plus 2b+1 X; prefix chain g(g−1)/2 sel + g(g+1)/2 z CCX; controlled row swaps:
b·(g(g+1)(2g+1)/6 − g) Fredkin gates (2 CX + 1 CCX each); guarded multipliers 2bg CCX
(w, wi) and bg(g−1) CCX (m_j); selection bg(g+1)/2 CCX. All of this is O(g³b), lower order
than the products.

**Toffoli count (exact; `closed_form_toffoli`, equal to the counted CCX for all 36 rows of
`run.json` and the 7 test rows).**

  T_CCX = (40b²+2b)·P + (g+1)(10b²+8b+2H) + 2·[λ_b g(g+1)/2 + g² + b(g(g+1)(2g+1)/6 − g)
          + 2bg + bg(g−1) + bg(g+1)/2],

with λ_b = 2b−3 (b ≥ 3), λ_2 = 1, and H = Σ_{i<b} hw((p−1)2^i mod p) ≤ b². Hence
**T_CCX = 40g³b² + O(g²b² + g³b + g·b³)**, and the total gate count is at most
(158b²+46b)·P + (g+1)(40b²+44b+10) + O(g³b) = O(g³b² + g·b³) (each product is ≤ 158b²+46b−4
gates, each add_scaled ≤ 40b²+44b+10, I146).

**Qubits (exact; `closed_form_qubits`, equal to the allocated wires in every row).**

  Q = b(3g² + 6g + 2 + max(I_p, E_e, 1)) + (3b+5) + max(0, b−2) + 1 + 3g(g+1)/2
    ≤ 3g²b + 2b² + O(gb + g²).

Breakdown: inputs g(g+1)b, output (g+1)b, workspace matrix g(g+1)b, history (u^{−1}, w, wi and
g−1 multipliers per step) g(g+2)b, z (g+1)b, flags 1 + 3g(g+1)/2, the square-and-multiply
register pool max(I_p, E_e, 1)·b (reused by every inversion and power; the zeroed old row
registers of the normalisation go back to the same pool), arithmetic ancillas 3b+5, AND-ladder
temporaries b−2.

Selected rows (`research/audits/reviews/2026-11-04-rees-coherent-sde/run.json`; d is the
smallest odd d ≥ 3 with gcd(d, p−1) = 1; "ratio" = T_CCX / (40 g³ b²)):

| p | b | g | d | I_p | E_e | add_product | Fredkin | CCX | all gates | qubits | ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 3 | 2 | 5 | 3 | 3 | 68 | 9 | 25 364 | 106 142 | 112 | 8.81 |
| 13 | 4 | 4 | 5 | 5 | 3 | 226 | 104 | 148 078 | 591 278 | 366 | 3.62 |
| 101 | 7 | 4 | 3 | 9 | 8 | 340 | 182 | 675 176 | 2 564 254 | 643 | 5.38 |
| 1031 | 11 | 8 | 3 | 12 | 15 | 1 334 | 2 156 | 6 506 872 | 23 753 166 | 2 983 | 2.63 |
| 65537 | 17 | 8 | 3 | 30 | 23 | 2 054 | 3 332 | 23 856 472 | 83 216 842 | 4 804 | 4.03 |
| 2^31−1 | 31 | 8 | 5 | 59 | 45 | 3 378 | 6 076 | 1.30·10^8 | 5.08·10^8 | 9 567 | 6.61 |
| 2^61−1 | 61 | 2 | 17 | 119 | 91 | 1 524 | 183 | 2.27·10^8 | 8.79·10^8 | 9 102 | 190.8 |
| 2^61−1 | 61 | 4 | 17 | 119 | 91 | 2 930 | 1 586 | 4.37·10^8 | 1.69·10^9 | 12 051 | 45.8 |
| 2^61−1 | 61 | 8 | 17 | 119 | 91 | 6 126 | 11 956 | 9.13·10^8 | 3.54·10^9 | 22 377 | 11.98 |
| 2^61−1 | 61 | 16 | 17 | 119 | 91 | 15 398 | 90 280 | 2.29·10^9 | 8.94·10^9 | 60 741 | 3.76 |

At b = 61 and the small g of the paper's instances the g·b³ inversion and power terms
dominate (4g·I_p + 2(g+1)E_e = 1 498 of the 1 524 products at g = 2). Not implemented, but
standard: Montgomery batch inversion of the g pivots (one inversion plus 3(g−1) products) would
cut 4g·I_p to 4I_p + O(g), and a fraction-free sweep with one final batched normalisation
would do the same; the power y^e itself (2(g+1)E_e) is intrinsic to the κ = 1 witness form.

Counting mode: the counts for p > 13 come from the program (gate items counted directly, each
macro by the gate-type counts of one emitted instance at that p, which are asserted equal to
the I146 closed forms `formula_counts`). The program-level count equals the length of the fully
emitted gate list where that list is built (test `test_emitted_counts_equal_program_counts`, and
every exhaustive row: e.g. 106 142 gates at (7, 2, 5)).

## 4. Checks

Simulator: `BitSim`, an exact bit-sliced basis-state simulator (one numpy uint64 bit-plane per
wire, one bit per input; SWAP is a relabelling). The circuit is a permutation of basis
states, so simulating every canonical basis input is a complete check on that input set. The
reference is `canonical_witness_batch` (a vectorised Gauss–Jordan written independently of the
circuit), itself checked against `canonical_witness` (the DEFINITION: incremental span test,
no RREF) and against `is_canonical_bruteforce` (A y = 0, y_{j*} = 1, zeros beyond, and prefix
independence by enumerating all p^{j*} coefficient vectors) on all 729 inputs at (3, 2) and
3 000 random inputs at (5, 2): 0 mismatches.

For every input the check asserts: output S = canonical witness; S canonical (< p); every input
wire restored; every workspace wire 0 (all wires other than inputs and outputs, including the
3b+5 arithmetic ancillas and all history); s ≠ 0; Σ s_l^d λ_l = 0.

**Exhaustive [proof-by-computation], all p^{g(g+1)} canonical inputs, all checks pass:**

| p | g | d | e | inputs | gates | qubits | sim time |
|---|---|---|---|---|---|---|---|
| 3 | 1 | 1, 3 | 1 | 9 | 6 264 | 39 | <0.01 s |
| 5 | 1 | 3 | 3 | 25 | 36 472 | 58 | 0.04 s |
| 7 | 1 | 5 | 5 | 49 | 50 148 | 61 | 0.05 s |
| 3 | 2 | 1, 3 | 1 | 729 | 19 474 | 75 | 0.02 s |
| 5 | 2 | 1 / 3 | 1 / 3 | 15 625 | 63 764 / 81 476 | 109 | 0.06 s |
| 7 | 2 | 1 / 5 | 1 / 5 | 117 649 | 78 566 / 106 142 | 112 | 0.2 s |
| 3 | 3 | 3 | 1 | 531 441 | 44 184 | 126 | 0.2 s |
| 11 | 2 | 3 | 7 | 1 771 561 | 214 950 | 149 | 3.3 s |
| 13 | 2 | 5 | 5 | 4 826 809 | 220 118 | 153 | 12.4 s |

(d = 1 is not a Rees grade; it is included because e = 1 exercises the no-power path.)

**Sampled [sampled], 8 192 structured inputs each** (`structured_inputs`: every column
independently random, zero, a scalar multiple of one earlier column, or a random combination of
earlier columns, so every j* ∈ {0..g} occurs; test `test_structured_inputs_hit_all_jstar`):
(p, g, d) = (5, 3, 3), (7, 3, 5), (11, 3, 7), (13, 3, 5), (5, 4, 3), (7, 4, 5): all pass.

**Sensitivity (the checks are not vacuous).** Dropping one Fredkin gate from F only, changing
the coefficient of one forward multiply-accumulate, or flipping the sign of one output
`add_scaled` each makes the exhaustive check at (5, 2, 3) fail (output and/or workspace);
test `test_mutations_are_detected`.

**Structure.** No gate or macro of U targets an input wire, and C targets only S, the shared
ancillas and its own pool registers (test
`test_inputs_never_targeted_and_copy_stage_writes_only_output`). κ ≠ 1 is refused
(`ValueError`).

Commands:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde.py -k slow   # p = 11, 13 exhaustive
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_coherent_sde --out research/audits/reviews/2026-11-04-rees-coherent-sde/run.json   # ~30 s, log in run.log
```

Results (this session): 30 passed, 2 skipped in 3.4 s; with `REES_SLOW=1 -k slow` 2 passed in
16 s; `run.json` regenerated in ~28 s, all rows pass and all 36 count rows match the closed
forms. `tests/test_rees_circuit_arith.py` still passes unchanged (39 passed, 6 skipped).

## 5. What this closes and what it does not

**Closes (for κ_d = 1 grades only).** The diagonal-equation solve at a grade with
gcd(d, p−1) = 1 no longer needs a mid-circuit measurement and classical feed-forward: a
permutation circuit of O(g³b² + g·b³) gates and 3g²b + 2b² + O(gb + g²) qubits maps the label
registers to the canonical witness with clean workspace, exactly, on every canonical input.
Its column count is g+1, which is the arity the generated circuits already use at κ = 1 (the
Chevalley–Warning arity κg+1), so no arity changes. Where it applies: e.g. grade 3 of n4(F_5)
(gcd(3, 4) = 1, g_3 = 1, M_3 = 2) and grade 3 of n5(F_5); not n4(F_7) (gcd(3, 6) = 3).

Why a coherent witness is enough for the descent [argued, from `prop:descent`]: with labels λ
held in registers and s = s(λ) computed coherently, apply the controlled right actions
R_{δ_{s_i}(σ(q))} controlled on the s registers (δ_0(σ(q)) is the identity element, so a target
with s_i = 0 is untouched and its factor tr(ρ_{λ_i}) = 1, matching "consumed and discarded").
Tracing out (or measuring at the end) the label, witness and target registers gives, by the
deferred-measurement principle, Σ_λ Pr(λ)·ρ_out(λ) on Q, and `prop:descent` says
ρ_out(λ) = ρ_{HZ/Z} for every positive-probability λ and every valid witness. So the reduced
output is exactly ρ_{HZ/Z}. The label/witness registers remain as garbage entangled with the
discarded targets; they cannot and need not be uncomputed (the next stage consumes ρ_{HZ/Z},
a mixed state). This is the deferred-measurement form of the same algorithm, not a new
capability.

**Does not close.**

1. **Grades with κ_d ≥ 2 stay classical.** In particular grade d = 2 always has
   κ_2 = gcd(2, p−1) = 2 for odd p, so **every** Rees instance with c ≥ 2 has a κ ≥ 2 grade,
   and this module alone never removes all classical feed-forward. Schedules 1–3 (Ivanyos–
   Santha, two-level contraction, triangular/free-coordinate) are not made coherent here; see
   Section 6 for a cost sketch.
2. **Not wired into the generated receiver.** `theorems/rees_circuit_general.py` /
   `rees_circuit_sparse.py` still apply a classical s. Wiring needs the merge's controlled
   right translation x ↦ x·(−δ_s(σ(q))) with s a quantum register: grade-j coordinates scale
   by s^j, i.e. j−1 more `add_product` per coordinate and the s^j powers, all with the same
   macros. Not done, not simulated.
3. **Canonical inputs only.** Padding words (≥ p) in the label registers are not claimed.
   They never occur in the generated circuits (every state is supported on canonical words),
   but this module does not check them.
4. **Correctness beyond p ≤ 13 is [argued]** (Lemmas 1–2 are proved for all p; the gate lists
   of the arithmetic macros are proof-by-computation for p ≤ 13 only, sampled to 2^61−1 in the
   I146 report). Exhaustive checks of U itself cover p ≤ 7 with g ≤ 2, p = 3 with g = 3, and
   p = 11, 13 with g = 2; g = 3, 4 are sampled.
5. No QFT_p, oracle, noise, depth or layout optimisation; no asymptotic claim about the
   receiver as a whole. `coherent_receiver_implemented` stays false.

## 6. Higher κ: reversible cost sketches [argued, not implemented]

General principle. Every classical deterministic algorithm with T field operations and
data-dependent branches can be made a permutation circuit by (i) making control flow
oblivious (evaluate every branch under a flag; pad loops to their worst-case trip count),
(ii) replacing each field operation by an I146 macro (O(b²) gates) and (iii) Bennett's
compute–copy–uncompute, with O(T) history registers (or O(T^{1+ε}) gates and
O(W·log T) space by pebbling). Randomised steps are the obstacle: a Las Vegas step has no
canonical output unless its randomness is fixed. Parameters that depend only on (p, κ), such
as a quadratic non-residue, a generator of the π-part of F_p^×, the two-level contraction
(α, β) or the zero sum of κ-th powers (Fact 2), can be computed classically ONCE, before the
quantum computation, and hard-wired as constants; this is legitimate because they do not
depend on the labels.

**Schedule 1 (deterministic Ivanyos–Santha, `theorems/rees_is_sde_solver.py`).** Already
deterministic. Its steps on M = G(κ, a)^L columns (G = κ^{κ(κ−1)/2}(a+1)^κ,
L = ⌈log2 t⌉ ≤ ⌈log2(κ+1)⌉) are: kernel computations (Lemma 12 / Theorem 11, of dimension at
most κ^{κ−1}a), one classification per kernel coefficient (Pohlig–Hellman in ⟨η⟩, O(κ log p)
exponentiations), the sign-permutation recombination of Theorem 11 (κ! subsets, fixed), the
§3.3 accumulation (Σ_{j<L} G^j calls of Theorem 11), and Fact 2 (column-independent:
precompute). Reversible cost:
- kernels: by the Section 2 machine (or its square-matrix variant), O(n³) products for an
  n×(n+1) system, n ≤ κ^{κ−1}a, i.e. O(κ^{3κ}a³·b²) Toffoli per kernel;
- classification: the data-dependent part is "which coset class s does coefficient β_i fall
  in", which decides the set J_a of each column. Coherently: a one-hot class register of κ
  bits per coefficient, and every w_a = Σ_{i ∈ J_a} β_i^κ v_i becomes κ controlled
  multiply-accumulates per column (a factor κ over the classical count). With a precomputed
  generator of the π-part (column-independent), the restart loop of IS §3.1 disappears and each
  logarithm is O(κ·b) products, i.e. O(κ b³) Toffoli;
- early exits (`_Found`) become flags, the accumulation runs to the end;
- total: O(M·poly(κ^κ, a)·b³) Toffoli with M = G(κ, a)^L ≤ B_κ(a), i.e. polynomial for fixed κ
  with the same column count as the classical solver, times a factor O(κ) for oblivious
  branching. Space under plain Bennett is of the same order as the gate count (history), and
  the paper's B_κ(a) is astronomically large (B_4(2) ≈ 3.7·10^16), so this is a polynomial-
  for-fixed-κ statement, not a practical circuit.

**Triangular solver (`prop:triangular-sde`), the cheapest κ = 2 candidate.** Given the
column-independent constants g (a non-residue coset generator) and the contraction (α, β),
it is deterministic: O(a) Gaussian eliminations, O(a²) coset tests y ↦ y^{(p−1)/κ}, and a
κ-th root per output weight. Coset tests are O(b) products each; for κ = 2 the square roots
are deterministic given the fixed non-residue (Tonelli–Shanks with a padded 2-adic loop:
O(b²) products worst case). Rough reversible cost: O(a⁴ + a²b + a²b²)·b² Toffoli at
(a+1)(a+2)/2 columns. Note this differs from the Chevalley–Warning arity 2a+1 the generator
uses at κ = 2, so wiring it changes the merge arities (the owner's K10-type decision).

Schedules 2–3 add rejection sampling (column-independent in Schedule 2: precompute) and, in
Schedule 3, an i.i.d. supply condition that is a property of the input law, not of a circuit;
no sketch is attempted.

## 7. Proposed paper text (not applied; main.tex untouched)

Placement: immediately after the "Gate-level control" paragraph of
Section `sec:uniform-compilation` (main.tex line ~656), plus one sentence changed inside that
paragraph. The macros used (`\Fp`, `\file`) are the paper's.

In the paragraph, replace "The diagonal equation is solved classically between quantum
segments:" by:

```latex
The diagonal equation is solved classically between quantum segments, except that at grades with $\kappa_d=1$ a coherent solve exists (Lemma~\ref{lem:coherent-linear-sde}; it is not wired into these circuits):
```

New lemma (after the paragraph):

```latex
\begin{lemma}[Coherent linear-grade witness; AI-checked, pending human review]
\label{lem:coherent-linear-sde}
Let $p$ be an odd prime, $g\ge1$, and $d$ with $\kappa_d=\gcd(d,p-1)=1$; let $e\in\{1,\dots,p-2\}$ satisfy $ed\equiv1\pmod{p-1}$ and $b=\lceil\log_2p\rceil$. For columns $\lambda_0,\dots,\lambda_g\in\Fp^g$ let $j^*$ be the least $j$ with $\lambda_j\in\operatorname{span}(\lambda_0,\dots,\lambda_{j-1})$, write $\lambda_{j^*}=\sum_{i<j^*}c_i\lambda_i$, and put $y=(-c_0,\dots,-c_{j^*-1},1,0,\dots,0)$ and $s_l=y_l^{e}$. Then $s\ne0$ and $\sum_l s_l^d\lambda_l=0$, and there is a circuit of $X$, CNOT, Toffoli and SWAP gates that maps $|\lambda\rangle|0\rangle|0\rangle$ to $|\lambda\rangle|s(\lambda)\rangle|0\rangle$ for every $\lambda$ with canonical coordinates. It uses $P=g^3+2g^2+5g+4g\,\ell(p-2)+2(g+1)\,\ell(e)$ modular multiply-accumulates, where $\ell(n)$ is the number of multiplications of binary square-and-multiply for $x^n$, so $40g^3b^2+O(g^2b^2+g^3b+gb^3)$ Toffoli gates in all, and $3g^2b+2b^2+O(gb+g^2)$ qubits.
\end{lemma}

\begin{proof}[Proof sketch]
The columns $\lambda_0,\dots,\lambda_{j^*-1}$ are independent, so $c$ is unique, $y\neq0$ and $\sum_l y_l\lambda_l=0$; since $x^{ed}=x$ on $\Fp$, $s_l^d=y_l$, and $s_{j^*}=1$. The vector $y$ is the kernel vector of the reduced row echelon form at its first non-pivot column. The circuit is $F\cdot C\cdot F^{-1}$. $F$ runs Gauss--Jordan elimination over the columns $k=0,\dots,g-1$ on a copy of the input, obliviously: a flag records whether $\lambda_0,\dots,\lambda_{k-1}$ are independent; the pivot is the first nonzero entry in rows $\ge k$ of column $k$, found by OR flags and a prefix chain and moved into row $k$ by controlled swaps; the pivot is inverted by Fermat exponentiation $u^{p-2}$, computed and uncomputed locally; row $k$ is normalised in place by $t'=wt$, $t\leftarrow t-w^{-1}t'$ with $(w,w^{-1})=(u^{-1},u)$ on a pivot and $(1,1)$ otherwise; the other rows are cleared with stored multipliers. One-hot flags then mark $j^*$ and select $z=-y$. $C$ computes $z_l^e$, adds $-z_l^e=s_l$ ($e$ is odd) into the output and uncomputes the powers. $C$ writes only the output, so $F^{-1}$ returns every other wire to its initial value. The multiply-accumulates are those of the arithmetic backend above ($40b^2+2b$ Toffoli gates each).
\end{proof}

The artifact \file{theorems/rees_coherent_sde.py} (report \file{research/audits/reviews/2026-11-04-rees-coherent-sde.md}; finite computation, AI-checked, pending human review) emits this circuit and simulates it on basis states, which suffices for a permutation circuit. On every canonical input for $(p,g)\in\{3,5,7\}\times\{1,2\}$, $(3,3)$, $(11,2)$ and $(13,2)$ the output is the witness of the lemma and every workspace qubit returns to $0$; $g=3,4$ are sampled. Its column count $g+1$ is the arity the generated circuits already use at $\kappa_d=1$. Holding the labels in registers and controlling the descent of Proposition~\ref{prop:descent} on the witness register gives, by deferred measurement, the same output $\rho_{HZ/Z}$. Grade $d=2$ always has $\kappa_2=2$, so this removes the classical solve only at the odd grades with $\gcd(d,p-1)=1$; the solvers for $\kappa_d\ge2$ remain classical, and the receiver is not coherent.
```

## 8. Claim gates

`research/reductions/rees_hsp_reduction.json` untouched. `STATUS` of the new module:
`coherent_receiver_implemented: False`, `general_sde_implemented: False`,
`coherent_higher_kappa_sde_implemented: False`, `wired_into_generated_receiver: False`,
`independent_review: False`, `speedup_claim_allowed: False`; only
`coherent_linear_sde_implemented: True`, scoped to κ_d = 1 and canonical inputs. No claim of a
quantum advantage, an asymptotic receiver cost, or a native application follows.

## 9. Files

- `theorems/rees_coherent_sde.py` (new): `CoherentSDE(p, g, d)` (program, `flatten()`,
  `counts()`), references `canonical_witness`, `canonical_witness_batch`,
  `is_canonical_bruteforce`, closed forms `closed_form_macros/toffoli/qubits`, simulator
  `BitSim`, `exhaustive_check`, `sampled_check`, `count_row`, CLI `main`.
- `tests/test_rees_coherent_sde.py` (new).
- `research/audits/reviews/2026-11-04-rees-coherent-sde/run.json`, `run.log` (artifacts).
- This report. No existing file edited; nothing committed or pushed.

## 10. Next hard question

Make the κ = 2 grade coherent: the triangular solver of `prop:triangular-sde` with a
precomputed non-residue and contraction is deterministic, so a reversible version at
(a+1)(a+2)/2 columns is the next step (Section 6). Acceptance: the same exhaustive
basis-state check for p ∈ {5, 13} (p ∉ E_2(2) = ∅), a ≤ 2, with clean workspace. Then wire both
solvers into the merge with a quantum-controlled δ_s and rerun the n4(F_5) sparse simulation.
