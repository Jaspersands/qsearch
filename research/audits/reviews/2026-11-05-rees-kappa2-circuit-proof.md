# Rees HSP: the κ = 2 coherent SDE circuit writes a valid witness on every input

5 November 2026. AI-only pass (Claude Code). **Status: AI-checked, pending human review.** Not Lean.
No paper, code, registry or handoff file was edited; this report is the only output. Labels as in the
κ = 2 report: **[proved]** written argument here; **[proof-by-computation]** exhaustive over a stated
finite set; **[sampled]** exact on a stated subset; **[argued]** reasoning not machine-checked.

Companion of `2026-11-04-rees-coherent-sde-k2.md` (the κ = 2 circuit, its Theorem 3 and Lemma 4, its
checks) and `2026-11-05-rees-receiver-general-lemma.md` (hypothesis (D2a) and its Section 9, route (ii)).
Code read: `theorems/rees_coherent_sde_k2.py` (class `CoherentSDEK2`), `theorems/rees_coherent_sde.py`
(helpers `_fd` building blocks, `Prog`, `BitSim`), `theorems/rees_circuit_arith.py` (macro contract),
`theorems/rees_circuit_coherent.py` (`MergeBlock`, `sde_circuit`, `remap`),
`theorems/rees_circuit_coherent_k3.py` (`sde_circuit_k` dispatch), `formal/Formal/ReesSdeSolver.lean`.

## 0. Result

**Setting.** p an odd prime, a ≥ 1, d ≥ 2 with κ = gcd(d, p−1) = 2, M = (a+1)(a+2)/2, b = ⌈log₂ p⌉.
U := `CoherentSDEK2(p, a, d).prog` is a permutation program (X, CX, CCX, SWAP and the two arithmetic
macros `add_product`, `add_scaled`) on the wires L[c][r] (label column c, row r; M·a registers of b
qubits), S[c] (M output registers) and a workspace. A *canonical* word is a b-bit word < p.

**Target (`eq:sde-target`, main-core.tex line 372–376, and `check_witness` in the code):** a vector
s ∈ F_p^M, s ≠ 0, with Σ_{i=1}^M s_i^d λ_i = 0 in F_p^a, for the label columns λ_1..λ_M ∈ F_p^a.
(The receiver lemma's (D2) writes the exponent as d+1 because it indexes a block by the grade of the
children it merges; `MergeBlock(cfg, d)` and `sde_circuit(p, g, d)` index by the grade d of the
labels, and the exponent is that d. Nothing below depends on the convention.)

**Theorem (κ = 2 circuit) [proved, conditional only on the macro contract (M) below].** For every
canonical input λ ∈ (F_p^a)^M,

  U |λ⟩_L |0⟩_S |0⟩_work = |λ⟩_L |s(λ)⟩_S |0⟩_work,

where s(λ) is the canonical witness `canonical_witness_k2(p, λ, d)` of the κ = 2 report (Section 1
there; Section 1 here), and s(λ) ≠ 0, every s_i(λ) canonical, Σ s_i(λ)^d λ_i = 0. In particular U
writes a valid witness on every input, with all M·a label registers restored and every non-output wire
returned to 0.

**(M) Macro contract** (`rees_circuit_arith.py`, header items (A1), (A4)): on canonical t, a, b and the
shared 3b+5 arithmetic ancillas at 0, `add_product(t, a, b, κ)` is t ← t + κ·a·b mod p and
`add_scaled(t, a, κ)` is t ← t + κ·a mod p, the operands are never targeted and every ancilla returns
to 0. (M) is [proof-by-computation] on all words for p ∈ {3, 5, 7, 11, 13}
(`2026-11-04-rees-circuit-arith.md` §2–3) and [argued] (standard reversible ripple-carry arithmetic) for
larger p. So for p ∈ {5, 7} the Theorem is unconditional; for every other odd p it holds given (M).

The Theorem upgrades the κ = 2 report's Theorem 5 from "[argued] step-by-step correspondence" to a
written proof: Sections 2 (the algorithm is correct) and 3–4 (the gate list computes the algorithm,
reversibly, with clean workspace). Section 5 records the controls run in this pass (all pass; no
counterexample found), Section 6 the exact relation to the Lean solver, Section 7 the consequence for
(D2a).

## 1. The algorithm the circuit implements (extracted from the code)

Constants, computed in `__init__` from (p, d) only: m = least quadratic non-residue mod p
(`least_nonresidue`); μ = m − 1; p − 1 = 2^S·Q with Q odd (`two_adic`); z = m^Q; u = `bezout_exponent`
= the least u ≥ 1 with u·(d/2) ≡ 1 (mod (p−1)/2) (u = 1 when (p−1)/2 = 1, i.e. p = 3). Write
P = nonzero squares, N = non-squares, χ(y) = y^{(p−1)/2} ∈ {0, 1, p−1}, nq(y) := [χ(y) = p−1] = [y ∈ N].
Blocks: B_k = columns o_k, …, o_k + a − k with o_k = Σ_{j<k}(a+1−j) (`block_offsets`), k = 0..a.

The program is U = F · C · F⁻¹ (`self.prog = Prog(F+C+F.inverse())`, `F.inverse()` the reversed item
list with inverse macros). Every quantity below is a register of the circuit; every branch is realised
obliviously (no data-dependent control flow in the gate list), by flags that are 0 or 1.

```
F (forward pass; _forward):
  run_0 := 1                                         # one X
  V := []                                            # registers v_1, v_2, ... (each a registers)
  for k = 0 .. a:                                    # EVERY round is emitted; nothing is skipped
    (dep, Z) := FD(V + [λ_i : i ∈ B_k])               # _fd: oblivious Gauss–Jordan on a+1 columns in F_p^a
         # dep: one-hot flags; dep[j] = 1 iff column j is the first column in the span of the earlier ones
         # Z = −y where y is the first dependency: y_j* = 1, y_j = 0 for j > j*, Σ_j y_j w_j = 0
    for i in B_k:  δ_i := −Z[k+i]                     # add_scaled κ=−1 into a fresh register; δ_i = y_{k+i}
                   nq_i := [χ(δ_i) = p−1]             # Legendre flag (chain computed, tested, uncomputed)
                   δ'_i := nq_i ? δ_i : 0             # b CCX
    v_{k+1} := μ · Σ_{i∈B_k} δ'_i λ_i                 # add_product κ=μ into a fresh registers
    allP_k := AND_i ¬nq_i                             # X, AND ladder, X
    F_k := run_k ∧ allP_k ;  run_{k+1} := run_k ⊕ F_k # CCX; two CX
    V.append(v_{k+1})
  for l = 1 .. a:   τ_l := − XOR_{k ≥ l} (F_k ? Z^(k)[l−1] : 0)    # one-hot select, then add_scaled κ=−1
  for l = a .. 1:   nζ_l := [χ(τ_l) = p−1]
                    if l > 1: ζ''_l := nζ_l ? 0 : τ_l                # masked copy
                              for j = 1 .. l−1: τ_j += −ζ''_l · Z^(l−1)[j−1]   # = + ζ''_l · y^(l−1)_{j−1}
  for k = 0 .. a, i ∈ B_k (column col = o_k + i):
     w := F_k                                        # CX into bit 0 of a fresh register
     if k < a:  ζ := τ_{k+1}, nζ := nζ_{k+1}
                c := (¬nζ ∧ ¬nq_i) ? 1 : (¬nζ ∧ nq_i) ? m : (nζ ∧ nq_i) ? μ : 0     # constants under 3 flags
                w += ζ · c                           # add_product
     x_col := δ_i · w                                 # add_product into a fresh register
C (copy stage; _copy_stage), for each column i = 0 .. M−1:
     P_i: Tonelli–Shanks on x_i with the fixed z (S−1 rounds, every round emitted), r with r² = x_i;
          σ := (r odd) ? p−1 : 1 ;  ρ := r·σ          # the even square root
          res := ρ^u                                  # square-and-multiply (alias when u = 1)
     S_i += res                                      # add_scaled κ=1 (the only write to S in U)
     P_i⁻¹                                           # all of P_i's registers and flag bits back to 0
F⁻¹.
```

FD (`_fd(F, cols, R)`, here always n = a+1 columns in R = a rows): copy the columns into a work matrix
W (R rows × n columns); act_0 := 1; for k = 0..R−1: nz_r := [W[r][k] ≠ 0] for r ≥ k; sel_r := act_k ∧
(W[k..r−1][k] = 0) ∧ nz_r (one-hot: "row r is the first nonzero row of column k at or below k");
dep_k := act_k ∧ (W[k..R−1][k] = 0); act_{k+1} := act_k ⊕ dep_k (= act_k ∧ ¬dep_k); piv := act_{k+1};
Fredkin-swap rows k and r on columns ≥ k under sel_r; w := piv ? W[k][k]^{−1} : 1 (Fermat chain
u^{p−2}, computed, copied, uncomputed), wi := piv ? W[k][k] : 1; row k ← w·row k (via t' = w·t,
t −= wi·t', so t becomes 0 and is released to the pool, t' is the new row entry); for every row j ≠ k:
mreg := piv ? W[j][k] : 0, W[j][c] −= mreg · W[k][c] for c > k, W[j][k] ⊕= mreg (so W[j][k] := 0 when
piv). Finally dep_R := act_R (n = R+1), and Z[i] := XOR_k (dep_k ? W[i][k] : 0) for i < k, Z[k] ⊕=
dep_k ? p−1 : 0.

## 2. Theorem A: the algorithm is correct on every input [proved]

This re-derives the κ = 2 report's Lemmas 1–4 and Theorem 3 for the algorithm *as implemented* (sign
stop test, no second elimination, c(1, δ) = 1 at the stop round, even root), with the degenerate inputs
made explicit. Notation: U_k = span(v_1..v_k), e_{k+1} := Σ_{i∈B_k} δ_i λ_i,
c(ζ, δ) := α_{n(ζ)} + β_{n(δ)} with α = (1, 0), β = (0, μ), n(y) = [y ∈ N].

**Lemma 1 (contraction).** μ ∈ P, and for ζ, δ ∈ F_p^×: ζδc(ζ, δ) ∈ P ∪ {0}; c(1, δ) ∈ {1, m} ≠ 0.
*Proof.* 1 ∈ P so m ≥ 2, and m−1 ∈ {1..m−1} is a nonzero residue by minimality of m. Cases
(ζ, δ) ∈ (P, P): c = 1, ζδ ∈ P. (P, N): c = m ∈ N, ζδ ∈ N, product ∈ P. (N, P): c = 0. (N, N): c = μ ∈ P,
ζδ ∈ P. ∎

**Lemma 2 (first dependency).** Let w_0..w_n (n+1 = a+1 vectors in F_p^a). Then j* := min{j : w_j ∈
span(w_0..w_{j−1})} exists (j* ≤ a), w_0..w_{j*−1} are independent, and there is exactly one y with
y_{j*} = 1, y_j = 0 for j > j*, Σ y_j w_j = 0 (write FD(w) = y). If the first k vectors are independent
then j* ≥ k. *Proof.* a+1 vectors in F_p^a are dependent, so some w_j lies in the span of its
predecessors; minimality gives the independence of w_{<j*}; uniqueness of the coordinates of w_{j*} in
that independent family gives uniqueness of y. ∎ (Zero vectors: w_j = 0 ⇒ j* ≤ j, with
y = e_j if j = j*. Repeated vectors w_i = w_j, i < j ⇒ j* ≤ j.)

**Lemma 3 (round identity).** In a round k with v_1..v_k independent, y = FD(v_1..v_k, λ_{B_k}),
δ_i = y_{k+i} (i ∈ B_k): δ ≠ 0 (δ_{j*−k} = 1), e_{k+1} = −Σ_{l≤k} y_{l−1} v_l ∈ U_k, and for any ζ ∈ F_p
the weights x_i = ζ δ_i c(ζ, δ_i) on B_k lie in P ∪ {0} and satisfy
Σ_{i∈B_k} x_i λ_i = ζ α_{n(ζ)} e_{k+1} + ζ v_{k+1}, where v_{k+1} = μ Σ_{δ_i∈N} δ_i λ_i.
*Proof.* j* ≥ k by Lemma 2 since the v's are independent, so δ_{j*−k} = 1; the relation Σ y_j w_j = 0
split into the v part and the λ part gives e_{k+1}. Lemma 1 gives x_i ∈ P ∪ {0} (x_i = 0 when ζ = 0 or
δ_i = 0). Expanding c: Σ x_i λ_i = ζ α_{n(ζ)} Σ δ_i λ_i + ζ Σ β_{n(δ_i)} δ_i λ_i, and β_{n(δ)}δ = μδ on N,
0 on P ∪ {0}. ∎

**Lemma 4 (the sign test is the stop test).** With v_1..v_k independent and δ as in Lemma 3:
v_{k+1} ∈ U_k ⟺ no δ_i ∈ N ⟺ v_{k+1} = 0. Hence at a stop round the weights δ_i c(1, δ_i) equal δ_i,
and the second first dependency y' = FD(v_1..v_k, v_{k+1}) of the paper's definition is (0..0, 1).
*Proof.* (⇐) trivial (μ ≠ 0; empty sum). (⇒) Let δ^P be δ with its N-entries set to 0. Then
Σ δ^P_i λ_i = e_{k+1} − μ^{−1} v_{k+1} ∈ U_k, so for some c the vector (c, δ^P) is a relation on the list
(v_1..v_k, λ_{B_k}); its entry at position j* is δ_{j*−k} = 1 (kept, as 1 ∈ P) and its entries beyond j*
are 0 (δ's are). By the uniqueness in Lemma 2, (c, δ^P) = y, so δ^P = δ: no entry of δ is in N, and
v_{k+1} = 0. ∎ (The proof uses that δ is the *minimal* dependency with a residue entry; the κ = 2
report records the reviewer's counterexample p = 5, δ = (2, 1) for a non-minimal δ.)

**Definition (the canonical witness, as computed).** Rounds k = 0, 1, …: given independent v_1..v_k,
y^(k) := FD(v_1..v_k, λ_{B_k}), δ^(k), v_{k+1} as in Lemma 3; stop at K := the first k with no
δ^(k)_i ∈ N (⟺ v_{k+1} ∈ U_k by Lemma 4); otherwise append v_{k+1} (∉ U_k, so v_1..v_{k+1} independent)
and continue. Weights: x_i := δ^(K)_i on B_K; τ_l := y^(K)_{l−1} (l = 1..K); for l = K..1 with
ζ_l := τ_l (current value): x_i := ζ_l δ^(l−1)_i c(ζ_l, δ^(l−1)_i) on B_{l−1}, and if ζ_l ∈ P ∪ {0}
then τ_j += ζ_l y^(l−1)_{j−1} for j < l; x_i := 0 on B_k for k > K. Roots: s_i := ρ(x_i)^u with ρ(x) the
even r ∈ {0..p−1} with r² ≡ x.

**Theorem A.** For every λ ∈ (F_p^a)^M: (i) the definition is total (K ≤ a exists) and reads only
B_0..B_K; (ii) every x_i ∈ P ∪ {0}, so ρ(x_i) exists; (iii) x ≠ 0, indeed x_{i*} = 1 at
i* = o_K + (j*_K − K); (iv) Σ_i x_i λ_i = 0; (v) s_i^d = x_i, s_{i*} = (−1)^u ≠ 0, every s_i canonical,
and Σ_i s_i^d λ_i = 0.

*Proof.* (i) By induction the v's stay independent, so each round is as in Lemma 3. If rounds 0..a−1 all
continue, v_1..v_a span F_p^a and the single column λ_{o_a} of B_a lies in U_a: j* = a, δ^(a) = (1),
1 ∈ P, so round a stops. (ii) Lemma 3 for blocks B_{l−1}, l ≤ K; on B_K, x_i = δ_i ∈ P ∪ {0} by
Lemma 4; 0 elsewhere. (iii) δ^(K)_{j*−K} = 1. (iv) Let R := Σ_{B_K} x_i λ_i = e_{K+1} =
−Σ_{l≤K} y^(K)_{l−1} v_l = −Σ_l τ_l v_l with the initial τ. Invariant: T^(l) := Σ_{j≤l} τ_j v_j (current
τ). T^(K) = −R. Step l adds the B_{l−1} weights, whose sum is C_l = ζ_l α_{n(ζ_l)} e_l + ζ_l v_l
(Lemma 3), and e_l = −Σ_{j<l} y^(l−1)_{j−1} v_j, so T^(l) − C_l = Σ_{j<l}(τ_j + ζ_l α_{n(ζ_l)} y^(l−1)_{j−1}) v_j
= T^(l−1) after the update (the update is applied exactly when α_{n(ζ_l)} = 1, i.e. ζ_l ∈ P ∪ {0}; for
ζ_l = 0 both sides add 0). At l = 0, T^(0) = 0 = −R − Σ_l C_l, so Σ_i x_i λ_i = R + Σ_l C_l = 0 (the
blocks are disjoint). (v) For x ∈ P with ρ² = x: (ρ^u)^d = x^{u·d/2} = x·(x^{(p−1)/2})^t = x, where
u·(d/2) = 1 + t(p−1)/2 (u exists since gcd(d, p−1) = 2 makes d/2 invertible mod (p−1)/2; for p = 3,
d even and x = 1 give 2^d = 1 = x); x = 0 gives 0. ρ(1) = p−1 (the even root of 1), so
s_{i*} = (p−1)^u = (−1)^u ≠ 0. ρ(x)^u mod p is canonical by definition. ∎

*Degenerate inputs, explicitly.* All columns zero: round 0 has j* = 0, δ = e_0, stop, x = e_0,
s = ((−1)^u, 0, …). A zero column anywhere in B_k: j* ≤ its index; FD is unaffected otherwise.
Repeated or proportional columns λ_j = cλ_i (i < j in the same block): j* ≤ j and δ has entries
(…, −c, …, 1); whether −c ∈ N (e.g. c = 1 and p ≡ 3 mod 4) decides only whether the round stops or
continues, both handled by the same formulas. Columns in a proper subspace: K is smaller. p ≡ 1 vs 3
mod 4 enters only through S (the number of Tonelli–Shanks rounds) and through which δ-entries are
residues; no formula branches on it. Lemma 4 excludes the only conceivable bad case, "v_{k+1} ∈ U_k but
some δ_i ∈ N", for every input.

## 3. Theorem B: the gate list computes the algorithm [proved given (M)]

Throughout, "register holds v" means the b wires hold the canonical word v. Induction hypothesis along
the gate list of F on a canonical input: **every register holds a canonical word, every flag wire is 0
or 1 with the stated meaning, the arithmetic ancillas and the ladder temporaries are 0 between
macros/ladders, and every register in the pool `self.free` / `self.free_bits` is 0.** Every step
below preserves it: CX-copies of canonical words are canonical; masked copies (CCX from a flag) give the
word or 0; constants loaded by X/CX under mutually exclusive flags are < p; Fredkin swaps permute
canonical words; macros produce canonical words by (M) and restore their ancillas; AND/OR ladders
(`_and_into`, `_or_into`) compute into their target and uncompute their temporaries by the reversed
ladder (code: `P += lad; P.ccx(...); P += lad.inverse()`); `_eq_const_into` conjugates the ladder by X
gates on the bits where the constant is 0, so the flag receives [reg = const] and the register is
restored; `_pow_copy` computes a square-and-multiply chain (products of canonical words), calls the
sink, and appends the reversed chain, so its registers return to 0 before they are released.

**B1 (FD).** `_fd` computes, for any canonical list of n = a+1 columns in F_p^a, the one-hot flags dep
and Z = −FD(list). *Proof.* Invariant at the start of step k when act_k = 1: columns 0..k−1 are
independent and reduced to the unit vectors e_0..e_{k−1} (in the current row order), the row
operations applied so far are invertible and were applied to every column, so the linear relations
among columns are those of the input. The OR flags read column k in rows ≥ k; sel_r is one-hot at the
first nonzero row (prefix chain z_r = act ∧ ¬nz_k ∧ … ∧ ¬nz_{r−1}); dep_k = act_k ∧ "column k is zero
in rows ≥ k", which given the invariant says exactly "column k ∈ span(columns < k)". If dep_k = 1,
piv = 0: the Fredkins (controlled by sel, all 0), the normalisation (w = wi = 1: t' = t, t −= t' = 0)
and the elimination (mreg = 0) are the identity on W; act_{k+1} = 0 and every later step is the identity
too (all its flags are conjunctions with act). If dep_k = 0 and act_k = 1, piv = 1: the first nonzero
row r is swapped into row k on the columns ≥ k (columns < k are zero in rows ≥ k, so skipping them is
exact), u = W[k][k] ≠ 0, row k is scaled by u^{−1} (t' = u^{−1}t, t −= u·t' = 0, so the released
register is 0), every other row j gets W[j][c] −= W[j][k]·W[k][c] for c > k and W[j][k] := 0 (the XOR
with the stored multiplier equals W[j][k] − W[j][k]·1), which restores the invariant at k+1. Steps with
act_k = 0 are the identity. Since n = R+1, if all R columns are independent (act_R = 1) column R is in
their span, and dep_R := act_R; so exactly one dep_j is 1, at j = j*. Then Z[i] = W[i][j*] for i < j*
(the coordinates of column j* in the unit columns, i.e. −y_i) and Z[j*] = p−1 = −1 = −y_{j*},
Z[i] = 0 beyond: Z = −FD. Registers released to the pool (the normalisation's t) are 0; the Fermat
chain is uncomputed. ∎

**B2 (genuine rounds).** Claim: for k ≤ K (K as in Section 2) run_k = 1 and V holds v_1..v_k; for
k > K run_k = 0. Induction: run_0 = 1. In round k ≤ K the FD is that of the definition (B1 on the
genuine list), δ_i = −Z[k+i] = y^(k)_{k+i} (`add_scaled` κ = −1 into a 0 register), nq_i = [δ_i ∈ N]
(Euler: χ(0) = 0, χ(P) = 1, χ(N) = p−1; the flag tests the chain register against p−1), δ' is the
N-mask, v_{k+1} = μΣδ'_iλ_i (`add_product` κ = μ into 0 registers), allP_k = [no δ_i ∈ N], F_k = run_k ∧
allP_k, run_{k+1} = run_k ∧ ¬allP_k. By Lemma 4, allP_k = [stop at k]; so F_k = 1 exactly at k = K,
run_{k} = 1 for k ≤ K, 0 after. Rounds k > K are emitted and run on whatever V holds (canonical words;
B1 applies to any list), but F_k = 0 there and their Z^(k), nq, δ enter later gates only under F_k or
multiplied by a τ that is 0 (B3–B4). Round a, when genuine, stops (Theorem A(i)), so exactly one F_k is 1.

**B3 (τ).** τ_l = −XOR_{k≥l}(F_k ? Z^(k)[l−1] : 0) = −Z^(K)[l−1] = y^(K)_{l−1} if l ≤ K, else 0 (one-hot
F; `add_scaled` κ = −1 into a 0 register). The back substitution runs l = a..1; at step l the flag
nζ_l = [τ_l ∈ N] is taken from the *current* τ_l (all updates to τ_l come from steps l' > l, already
done); ζ'' = τ_l if τ_l ∈ P ∪ {0} else 0; τ_j += −ζ''·Z^(l−1)[j−1] = +ζ''·y^(l−1)_{j−1} (`add_product`
κ = −1, in place on τ_j, which is read by no gate of this step other than as a target). For l > K,
τ_l = 0 so ζ'' = 0 and nothing is added; for l ≤ K this is the definition's update, using the genuine
y^(l−1) (round l−1 ≤ K−1 is genuine). ∎

**B4 (weights).** For column col ∈ B_k: w = F_k + τ_{k+1}·c (w starts 0; CX from F_k sets the word 1 or
0; the three case flags ¬nζ∧¬nq, ¬nζ∧nq, nζ∧nq are mutually exclusive, so c ∈ {1, m, μ, 0} equals
c(τ_{k+1}, δ_i) by Lemma 1's case table; for k = a there is no τ_{a+1} and w = F_a), then
x_col = δ_i·w. Cases: k = K: F_K = 1 and τ_{K+1} = 0 (B3), so x = δ_i = δ_i c(1, δ_i) (Lemma 4).
k < K: F_k = 0, x = τ_{k+1} δ_i c(τ_{k+1}, δ_i) = ζ_{k+1} δ_i c(ζ_{k+1}, δ_i) with ζ_{k+1} the current τ_{k+1}
at the time the weight is computed, which is after the whole back substitution and equals the value
ζ_{k+1} the definition reads (τ_{k+1} is last modified at back-substitution step k+1, before its own flag
is taken, and never afterwards). k > K: F_k = 0, τ_{k+1} = 0, x = 0. So X holds exactly the x of the
Definition. ∎

**B5 (copy stage).** Fix i; x := x_i ∈ P ∪ {0} (Theorem A(ii)). P_i computes, into pool registers that
are 0 (induction hypothesis), r_0 = x^{(Q+1)/2} and t_0 = x^Q (aliases r = t = x when Q = 1), then for
j = 0..S−2: u_j = t_j^{2^{S−2−j}} (S−2−j squarings), k_j = [u_j = p−1], t_{j+1} = t_j·(k_j ? z^{−2^{j+1}} : 1)
(omitted at j = S−2), r_{j+1} = r_j·(k_j ? z^{−2^j} : 1); the constants are loaded into a register
initialised to 1 by one X and then XORed with (1 ⊕ const) under k_j. *Correctness for x ∈ P:* x = y²,
and y^Q has order dividing 2^S, so t_0 = (y^Q)² = z^{2k} for some k ∈ [0, 2^{S−1}) (z generates the
2-Sylow subgroup: z^{2^{S−1}} = m^{(p−1)/2} = −1). Invariant t_j = z^{2^{j+1}⌊k/2^j⌋}: then
u_j = z^{2^{S−1}⌊k/2^j⌋} = (−1)^{k_j} (bit j of k), so the flag k_j is that bit, and
t_{j+1} = z^{2^{j+1}(⌊k/2^j⌋ − k_j)} = z^{2^{j+2}⌊k/2^{j+1}⌋}. Finally r = r_0 z^{−Σ_j k_j 2^j} = r_0 z^{−k}
with r² = x^{Q+1} z^{−2k} = x^{Q+1}/t_0 = x. For x = 0 every power is 0, every flag is 0, r = 0. For S = 1
(p ≡ 3 mod 4) there are no rounds and r = x^{(p+1)/4}. Then σ = 1 ⊕ (r_0-bit ? 1 ⊕ (p−1) : 0) ∈ {1, p−1},
ρ = r·σ ∈ {r, p−r} is the even root (p odd), res = ρ^u (square-and-multiply, alias for u = 1),
S_i += res, so S_i = ρ(x_i)^u = s_i(λ) (S_i was 0 and no other gate of U targets S_i). P_i⁻¹ is the
reversed item list of P_i; P_i never targets S_i or x_i (its X gates on x_i come in restoring pairs
inside `_eq_const_into`, when a chain register aliases x_i), so P_i⁻¹ returns all its registers and flag
bits to 0 and they go back to the pools as zeros. ∎

Theorems A and B give: F maps |λ⟩|0⟩_S|0⟩_W to |λ⟩|0⟩_S|w(λ)⟩_W with the X registers holding x(λ) and
all pool registers 0; C maps it to |λ⟩|s(λ)⟩_S|w(λ)⟩_W. Section 4 finishes.

## 4. Reversibility and clean workspace [proved]

Every item of U is a permutation of the 2^{nw} basis words: X, CX, CCX, SWAP are, and each macro is a
fixed gate list of those. `Prog.inverse()` reverses the item order and flags macros inverse, and
`flatten` expands an inverse macro as the reversed gate list; since every elementary gate is an
involution, the flattened U contains F⁻¹ as the exact inverse permutation of the flattened F, on every
basis word (canonical or not). F acts as the identity on the S wires (no item of F has an S wire as a
target: S is allocated before F and never enters a macro of F or a CX/CCX target of F; checked in code
and by the κ = 2 report's `test_inputs_never_targeted_and_copy_stage_footprint`). C targets only S wires
and wires it restores itself (B5). Hence on the state after C, F⁻¹ acts on (L, W) only, where the word is
exactly F(λ, 0_W), and returns it to (λ, 0_W): U|λ⟩|0⟩|0⟩ = |λ⟩|s(λ)⟩|0⟩. No "garbage" remains: the
Gauss–Jordan histories (nz, sel, dep, multipliers, uinv), the Legendre and stop flags, V, Z, τ, the
case flags, the X registers, all live on W and are undone by F⁻¹; the macro ancillas are 0 after every
macro by (M); the ladder temporaries after every ladder; the pools after every local uncompute. ∎

Domain remark. The Theorem is about canonical inputs (every label word < p), which is the receiver
lemma's setting ((CLEAN): states supported on canonical words). For padding words the macro contract
(A2)–(A3) makes U still a permutation, but nothing is claimed about the value written; the receiver
never produces such words.

## 5. Checks run in this pass (controls for the proof; all pass)

Script: `k2check.py` (scratchpad; the calls are `exhaustive_check`, `check_circuit`,
`structured_inputs`, `canonical_witness_k2`, `check_witness` of `rees_coherent_sde_k2`, plus a
hand-built degenerate set). `nice -n 19`, `/opt/anaconda3/bin/python`; 197 s wall including circuit
construction under a saturated CPU; each bit-sliced simulation < 1.5 s. Every row asserts: S equals
the batched canonical witness, inputs restored, every non-IO wire 0, s ≠ 0, Σ s_i^d λ_i = 0, every s_i
< p.

| (p, a, d), u | inputs | result | label |
|---|---|---|---|
| (5, 1, 2), (7, 1, 2), (11, 1, 2), (13, 1, 2), 1 | all 125 / 343 / 1 331 / 2 197 | pass | proof-by-computation |
| (7, 1, 4), u = 2 (class-four grade 4 over F_7) | all 343 | pass | proof-by-computation |
| (3, 2, 2) | all 531 441 | pass | proof-by-computation |
| (7, 2, 2) (n4(F_7) grade 2) | 4 096 uniform random | pass, K = (1529, 1605, 962) | sampled |
| (7, 2, 2) | 4 096 structured (zero / proportional / dependent columns, low-rank) | pass, K = (3010, 926, 160) | sampled |
| (7, 2, 2) | 81 hand-built degenerate: all-zero; all equal; multiples 0..5 of one vector; ±v; v, mv alternating; each single column zero; each adjacent pair equal; each adjacent pair with ratio −1; rank-1 and rank-(a−1) subspaces; unit-vector columns | pass, K = (48, 31, 2) | proof-by-computation on that set |
| (7, 2, 2) | 381 inputs (the 81 + 300 uniform) against the definition-level `canonical_witness_k2` (second first dependency, general c(1, δ) and y'); also x_{i*} = 1 | equal | sampled |
| (5, 2, 2), (13, 2, 2), (17, 2, 2) (S = 2, 2, 4) | 81 degenerate + 512 uniform each | pass | sampled |
| (7, 3, 2) (class-four grade 2 over F_7, M = 10) | 93 degenerate + 512 uniform + 512 structured | pass, K = (507, 318, 198, 94) | sampled |

Existing controls that the proof must agree with (κ = 2 report §4): exhaustive at (5, 2, 2) on all
5^12 = 244 140 625 inputs (1 781 s), at (p, 1, 2) for 12 primes to 41, at (3, 2, 4); root circuit
exhaustive to p = 65537; mutation tests (m, μ, signs, dropped gates all detected). Nothing in this pass
contradicts them; no counterexample was found.

Merge-block level (script `blockcheck.py`, same conditions): the fifth backend's `MergeBlockK` for
n4(F_7) at grade 2 builds `sde_circuit_k(7, 2, 2)` = `CoherentSDEK2(7, 2, 2)` (κ ≤ 2 falls through to
the fourth backend's `sde_circuit`), and `block.U = remap(sde.prog, wmap)` with wmap the bijection
L → lam, S → S, anc → anc, rest → `sde_work` (disjoint fresh ranges). U alone on 2 048 label tuples at
n4(F_7) grade 2 and on all 343 triples at class-four grade 4 writes the canonical witness with labels
restored and workspace 0 (table in the addendum at the end of this report).

## 6. Relation to the Lean module `formal/Formal/ReesSdeSolver.lean`

What Lean proves (`quadSolveZModExp_spec`, no `sorry`, standard axioms; report
`2026-11-05-rees-lean-sde-solver.md`): for every prime p, d > 0 with gcd(d, p−1) = 2, M ≥ (a+1)(a+2)/2
and every `col : Fin M → Fin a → ZMod p`, `quadSolveZModExp p d col` is nonzero and Σ s_i^d col_i = 0.
Its algorithm is `triSolve` with A ζ = α_{cos2 ζ}, B δ = β_{cos2 δ}, α = (1, 0), β = (0, findMu p),
then `sqrtSearch` and `^ bezoutExp d (p−1)`.

Same as the circuit: the contraction. `findMu p` is the first y ∈ {0..p−1} with y ∈ P and 1+y ∈ N;
that is m−1 = μ (if y < m−1 had 1+y ∈ N then 1+y < m would contradict minimality of m), and
`cos2` is Euler's criterion, so A, B are the circuit's α_{n(·)}, β_{n(·)}. The block structure
(`roundStart`, `block`) and the back-substitution recursion (`triRound`: weights
`roundWeight A B δ ζ = ζ δ_i (A ζ + B δ_i)`, coordinate update γ_l + ζ·A ζ·γe_l) are the Definition's.

Different from the circuit (so the Lean theorem is about a *sibling* algorithm, not the gate list):
1. **The dependence.** Lean's `roundCoeff` is `kernelVec` (elimination of the last coordinate,
   recursively) on the list (block, v), rescaled so that its first nonzero *fresh* entry is 1
   (`pivotScale`). It is some kernel vector, not the first dependency; `triRound_spec` uses only
   `roundDelta_relation` (a relation), `roundDelta_support` and `roundDelta_pivot` (value 1 at a fresh
   column when v is independent). The circuit's FD-δ has all three properties, but the two δ's (hence
   the two witnesses) need not coincide.
2. **The stop test.** Lean decides v_{k+1} ∈ U_k by `solveVec` (exact span membership), the paper's
   test; the circuit uses the sign test of Lemma 4, which is equivalent *only* for a minimal δ with a
   residue entry (the circuit's), not for Lean's general kernel vector (the reviewer's counterexample).
3. **The stop-round weights.** Lean uses the general `roundWeight A B δ 1` = δ_i c(1, δ_i) and
   A 1·γe − η (the two relations); the circuit uses δ_i and y^(K) alone, which Lemma 4 shows equal.
4. **Roots and exponent.** `sqrtSearch` returns the first root in the order 0, 1, …, p−1 (the smaller
   representative), the circuit the even root; `bezoutExp d (p−1)` = (d/2)^{−1} mod (p−1)/2 plus
   (p−1)/2, the circuit's u is the least positive representative. Both are valid; the outputs differ
   as words.

Consequence. (D2a) is **not** "the Lean theorem plus a code-equivalence check": there is no Lean
definition whose output equals `canonical_witness_k2`. What the Lean development does supply is a
machine-checked version of Theorem A's hardest part under weaker hypotheses: `triRound_spec` proves
(ii)–(iv) for *any* choice of δ satisfying the three properties and *any* correct stop test. To turn
(D2a) into a Lean consequence one would (a) add an FD-based `roundCoeff` (first dependency, pivot 1)
and prove the three properties for it (the pivot property is immediate from y_{j*} = 1 at a fresh
column, j* ≥ k), (b) prove Lemma 4 in Lean and replace `solveVec` by the sign test, (c) replace
`sqrtSearch` by the even root, and (d) prove that the gate list computes this definition (Section 3
here), which is a statement about the Python-generated circuit that Lean cannot see without a
formalised circuit semantics. (a)–(c) are small; (d) is the real gap and is what this report proves
on paper.

## 7. Consequence for (D2a)

The receiver lemma (Section 9, route (ii)) asked for exactly this: "a written proof that
`CoherentSDEK2(p, a, d)` computes `canonical_witness_k2` on every canonical input given the macros,
upgrading the κ = 2 report's [argued] to [proved]; acceptance test: an independent re-derivation plus
the existing exhaustive runs as controls". Sections 2–4 are that proof; Section 5 the controls.

- **n4(F_7), grade 2** (p = 7, a = g_2 = 2, d = 2, M = 6, 7^12 label tuples): (D2a) at grade 2 now
  holds for every label tuple as a **theorem** [proved given (M), and (M) is proof-by-computation at
  p = 7], not as a sample. The block's U is `CoherentSDEK2(7, 2, 2).prog` under a wire bijection
  (`MergeBlock.__init__` via `sde_circuit_k`), and a wire bijection preserves the action. With (D2b)
  (symbolic, `merge_proofs_f7.json`) and (D2c) (`block_structure`), Proposition 4 of the receiver lemma
  gives (D2) at grade 2 for all 7^12 tuples, and Corollary 3 then applies to the fifth backend's root
  for all grade-2 label tuples. Grade 3 of n4(F_7) is κ_3 = 3 (`CoherentSDEKappa`), outside this
  report; it was already label-complete by the κ = 3 report's Lemma 5 plus the 7^3 run.
- **Class four over F_7** (grades d = 4, 3, 2 with κ = 2, 3, 2; label dims g = 1, 2, 3; coherent arities
  3, 6, 10): this report covers the two κ = 2 grades, d = 4 (a = 1, u = 2; the 343 inputs are also
  exhaustive, Section 5) and d = 2 (a = 3, M = 10, 7^30 inputs, previously sampled: 65 536 uniform +
  4 096 structured in the c4 report). Both are now (D2a)-complete as theorems. Grade 3 (κ = 3) stays
  as the κ = 3 report left it (representatives per row space, Lemma 5 there), and the c4 report's
  footprint checks are unchanged.
- **The 28 CPU-hour exhaustive run at (7, 2, 2) is no longer needed for (D2a)**; it would remain a
  useful control if someone wants a proof-by-computation label instead of a hand proof. The chunked
  mode exists (`--chunked 7,2,2`).

What stays conditional. (1) The macro contract (M) beyond p ≤ 13 is [argued]; irrelevant for the two
F_7 instances and n4(F_5). (2) This proof is an AI hand proof, pending human review, like Theorem 3 and
Lemma 4 of the κ = 2 report that it re-derives. (3) Nothing here concerns κ ≥ 3 grades, the QFT_p
synthesis, the oracle, or any claim gate; `coherent_receiver_implemented` and
`general_sde_implemented` stay false.

## 8. Proposed paper text (one sentence, full version, where the coherent κ = 2 solve is described)

"The κ = 2 solver circuit computes the canonical triangular witness on every label tuple, for every
odd prime p and every label dimension, with all workspace returned to zero (a written proof from the
first-dependency, sign-test and Tonelli–Shanks invariants, given the arithmetic macros, which are
checked exhaustively for p ≤ 13; the circuit is also checked exhaustively on all 5^12 inputs at
n4(F_5)), so the coherent receiver's block action no longer depends on sampled label tuples at the
κ = 2 grades of n4(F_7) and of the class-four instance over F_7."

Shorter alternative for main-core.tex (status sentence): "At κ = 2 the coherent solver is proved to
write a valid witness on every label tuple for every odd p (AI-checked, pending human review); the
exhaustive 5^12 run at n4(F_5) is a control, not the proof."

## 9. Next hard question and acceptance test

Formalise the gap named in Section 6: an FD-based `triRound` with the sign test and the even root in
`ReesSdeSolver.lean` (items (a)–(c)), with `#eval` agreement against `canonical_witness_k2` on the 381
inputs of Section 5 as the acceptance test. The remaining (D2a) gap at the κ = 3 grades is the
κ = 3 report's, not this one's.

## Addendum: merge-block results (`blockcheck.py`, 1.1 s of simulation)

| block | U = remapped `CoherentSDEK2` | inputs (U alone) | witness = canonical, ≠ 0, equation, labels restored, workspace 0 |
|---|---|---|---|
| n4(F_7) grade 2 (`MergeBlockK(job_config("n4_f7"), 2)`, d = 2, g = 2, M = 6; U 469 238 gates on 537 wires) | same item list and item types as `CoherentSDEK2(7, 2, 2).prog`, κ(7, 2) = 2 | 2 048 random label 6-tuples, 16 of them all-zero and 16 with all six columns equal | all true |
| class four over F_7 grade 4 (`MergeBlockK(coherent_config_k(filiform5(7)), 4)`, d = 4, g = 1, M = 3, u = 2; U 177 454 gates on 298 wires) | `CoherentSDEK2(7, 1, 4)` | all 343 label triples | all true |

Grades of the class-four instance over F_7 as the config reports them: d = 2: κ = 2, g = 3, arity 10;
d = 3: κ = 3, g = 2, arity 6; d = 4: κ = 2, g = 1, arity 3 (Section 7 uses these).
