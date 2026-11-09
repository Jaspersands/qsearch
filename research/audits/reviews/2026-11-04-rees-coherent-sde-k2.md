# Rees HSP: a coherent (reversible) SDE solve at kappa_d = 2

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels as in `2026-11-04-rees-coherent-sde.md`:
**[proved]** = written argument here; **[proof-by-computation]** = exhaustive check over ALL
inputs of the stated finite set; **[sampled]** = exact on a stated random subset only;
**[exact count]** = counted from the emitted gate list (or exact per-macro closed forms);
**[argued]** = reasoning, not machine-checked.

Scope: grades d with κ_d = gcd(d, p−1) = 2 (in particular d = 2 for every odd p), label
columns in F_p^a (a = g_d), target `eq:sde-target`: a nonzero s ∈ F_p^M with
Σ_i s_i^d λ_i = 0. Solver: the triangular two-level solver of `prop:triangular-sde` at
M = (a+1)(a+2)/2 columns, with an explicit universal contraction, a canonical choice at every
step, and an oblivious Tonelli–Shanks square root. Companion of
`2026-11-04-rees-coherent-sde.md` (κ_d = 1, `lem:coherent-linear-sde`).

This report is written incrementally; sections are appended as they are finished.

## 0. Which solver, and why

Three candidates at κ = 2 (paper notation, a = g_d):

| solver | columns | finding | coherent cost |
|---|---|---|---|
| generated circuits (`rees_circuit_general.Config`) | Chevalley–Warning κa+1 = 2a+1 | classical brute force over F_p^M (or IS when the arity reaches its count) | coherent lex-first search: Θ(p^{2a+1}) candidates, exponential |
| Schedule 2 (`thm:power-sde`(ii), symmetric form) | (a+1)((κ−1)a+1) = (a+1)^2 | two levels, needs a contraction found by rejection (column-independent: precompute) and p ≥ 16·2^6 | polynomial, but more columns than the triangular solver for every a ≥ 1 |
| triangular (`prop:triangular-sde`) | (a+1)(a+2)/2 | deterministic given a non-residue and a contraction; κ-th roots | polynomial; implemented here |

The triangular solver has the fewest columns of the two polynomial schedules for every a ≥ 1
((a+1)(a+2)/2 < (a+1)^2), needs no prime condition at κ = 2 (E_2(2) = ∅; Lemma 1 below gives
an explicit contraction for every odd p), and is deterministic once the non-residue is fixed.
At a = 1 its arity 3 equals the generator's 2a+1 = 3. At a ≥ 2 it is larger
(a = 2: 6 vs 5; a = 3: 10 vs 7), so wiring it into the generated circuits at a ≥ 2 changes
the grade-2 merge arity (an owner decision, as noted in §6 of the κ = 1 report). Grade-2 label
dimensions of the generated instances (cover dims, from `Config`): Heis(F_3) a = 1 (arity 3),
n4(F_5) and n4(F_7) a = 2 (arity 5), n5(F_5) a = 3 (arity 7).

## 1. The canonical witness (definition)

Fix an odd prime p, a ≥ 1, and d with gcd(d, p−1) = 2. Notation: P = (F_p^×)^2 (nonzero
squares), N = F_p^× \ P (non-squares), χ(y) = y^{(p−1)/2} ∈ {0, 1, −1} (Euler's criterion).

**Constants (depend on p and d only).**
- m = the least quadratic non-residue mod p (m ≥ 2), and μ = m − 1.
- The contraction α = (α_0, α_1) = (1, 0), β = (β_0, β_1) = (0, μ). For a class index
  n(y) = 0 if y ∈ P ∪ {0}, n(y) = 1 if y ∈ N, put c(ζ, δ) = α_{n(ζ)} + β_{n(δ)}.
- p − 1 = 2^S·Q with Q odd; z = m^Q (generates the 2-Sylow subgroup of F_p^×, order 2^S).
- u = the least positive integer with u·(d/2) ≡ 1 (mod (p−1)/2) (u = 1 for d = 2, and for p = 3).

**First dependency.** For a list w_0, …, w_{n−1} of vectors in F_p^a let
j* = min{ j : w_j ∈ span(w_0, …, w_{j−1}) } if it exists. Then w_{<j*} are independent, so
w_{j*} = Σ_{i<j*} c_i w_i with unique c, and FD(w) := y with y_i = −c_i (i < j*), y_{j*} = 1,
y_i = 0 (i > j*). (This is the κ = 1 report's Lemma 1 witness with e = 1.)

**Blocks.** M = (a+1)(a+2)/2. The columns are split, in order, into blocks B_0, …, B_a with
|B_k| = a+1−k (offset o_k = Σ_{j<k}(a+1−j)).

**Rounds (k = 0, 1, …).** Given independent v_1, …, v_k (U_k = span, U_0 = 0):
1. y^(k) = FD(v_1, …, v_k, λ_{o_k}, …, λ_{o_k+a−k}) (a+1 vectors in F_p^a, so a dependency
   exists, and j* ≥ k because the v's are independent). δ^(k)_i = y^(k)_{k+i} (i ∈ B_k, local
   index), so e_{k+1} := Σ_i δ^(k)_i λ_i = −Σ_{l≤k} y^(k)_{l−1} v_l ∈ U_k, and δ^(k) ≠ 0 with
   δ^(k)_{j*−k} = 1.
2. v_{k+1} := μ · Σ_{i : δ^(k)_i ∈ N} δ^(k)_i λ_i (= Σ_i β_{n(δ_i)} δ_i λ_i).
3. If v_{k+1} ∈ U_k, stop: K := k, and y' := FD(v_1, …, v_k, v_{k+1}) (first dependency at
   index k), so v_{K+1} = −Σ_{l≤K} y'_{l−1} v_l. Otherwise append v_{k+1} and continue.

U_a = F_p^a would force a stop at round a, so K ≤ a exists and only blocks B_0..B_K are read.

**Weights.** x ∈ F_p^M, initially 0.
- Round K at ζ = 1: x_i = δ^(K)_i · c(1, δ^(K)_i) for i ∈ B_K (= δ_i if δ_i ∈ P ∪ {0}, m·δ_i if
  δ_i ∈ N).
- τ ∈ F_p^K, τ_l := y^(K)_{l−1} + y'_{l−1} (l = 1..K): the coordinates of −R in the basis
  v_1..v_K, where R := Σ_{i∈B_K} x_i λ_i = e_{K+1} + v_{K+1}.
- Back substitution, l = K, K−1, …, 1: ζ_l := τ_l (current value). For i ∈ B_{l−1}:
  x_i = ζ_l·δ^(l−1)_i·c(ζ_l, δ^(l−1)_i). If ζ_l ∈ P ∪ {0} (α_{n(ζ_l)} = 1), update
  τ_j += ζ_l·y^(l−1)_{j−1} for j = 1..l−1; if ζ_l ∈ N, no update.
- Blocks B_{K+1}..B_a get x_i = 0.

**Roots.** ρ(x) := the unique even integer r ∈ {0, …, p−1} with r^2 ≡ x (ρ(0) = 0; for x ∈ P
the two roots r, p−r have opposite parity). The canonical witness is

  s_i := ρ(x_i)^u mod p.

**Lemma 1 (universal contraction for κ = 2) [proved].** For every odd p, μ = m−1 ∈ P, and for
all ζ, δ ∈ F_p^× the product ζ·δ·c(ζ, δ) lies in P ∪ {0}. Equivalently ((α_1+β_0, α_0+β_1,
α_1+β_1) = (0, m, μ)) the pair (α, β) is a universal two-level contraction in the normalisation
of `prop:triangular-sde` (α_j + β_i ∈ g^{−(i+j)}P ∪ {0}), for every odd prime p.

*Proof.* m ≥ 2 since 1 ∈ P; m−1 ∈ {1, …, m−1} is not a non-residue by minimality and is
nonzero, so μ ∈ P. Cases: ζ, δ ∈ P: c = 1, product in P. ζ ∈ P, δ ∈ N: c = 1 + μ = m ∈ N,
ζδ ∈ N, product ∈ P. ζ ∈ N, δ ∈ P: c = 0. ζ, δ ∈ N: c = μ ∈ P, ζδ ∈ P. ∎

(This is an explicit instance of E_2(2) = ∅; the paper's search found the set empty, Lemma 1
just writes one contraction down.)

**Lemma 2 (round realisation) [proved].** For a round k, ζ ∈ F_p and weights
x_i = ζ δ_i c(ζ, δ_i) on B_k: every x_i ∈ P ∪ {0}, and
Σ_{i∈B_k} x_i λ_i = ζ·α_{n(ζ)}·e_{k+1} + ζ·v_{k+1}.

*Proof.* Lemma 1 for ζ, δ_i ≠ 0; x_i = 0 if ζ = 0 or δ_i = 0. The sum is
ζ α_{n(ζ)} Σ δ_i λ_i + ζ Σ β_{n(δ_i)} δ_i λ_i, and β_{n(δ)} δ = μδ on N, 0 otherwise. ∎

**Theorem 3 (canonical witness) [proved].** For every tuple of M columns in F_p^a, the
definition above is total and deterministic (a function of the column tuple and p, d), and
s satisfies: s ≠ 0, s_i^d = x_i for all i, and Σ_i s_i^d λ_i = 0. More precisely x_{i*} = 1
at the column i* = o_K + (j*_K − K) of round K.

*Proof.* (Totality.) By induction v_1..v_k are independent (v_{k+1} ∉ U_k when we continue),
so in round k the list of a+1 vectors in F_p^a has a first dependency at j* ≥ k; FD is unique.
If rounds 0..a−1 all continue, U_a = F_p^a and round a stops. Every choice is fixed (first
dependency, m, the fixed contraction, ρ, u), so x and s are functions of the tuple.
(Equation for x.) R = e_{K+1} + v_{K+1} by Lemma 2 with ζ = 1 (α_0 = 1), and −R = Σ_l τ_l v_l
with τ as defined (from the two first-dependency relations). Invariant: before step l,
τ^(l) := Σ_{j≤l} τ_j v_j and τ^(K) = −R. Step l adds the round-(l−1) weights with ζ = ζ_l,
whose sum is C_l = ζ_l α_{n(ζ_l)} e_l + ζ_l v_l (Lemma 2), and replaces τ by τ − C_l, which in
coordinates is: drop τ_l (the ζ_l v_l term), and add ζ_l α_{n(ζ_l)}·y^(l−1)_{j−1} to τ_j for
j < l (since e_l = −Σ_{j<l} y^(l−1)_{j−1} v_j). So τ^(l−1) = τ^(l) − C_l ∈ U_{l−1}, and at the
end 0 = τ^(0) = −R − Σ_l C_l, i.e. Σ_i x_i λ_i = R + Σ_l C_l = 0 (the blocks are disjoint).
(Nonzero.) On B_K, x_i = δ_i c(1, δ_i) with c(1, δ) ∈ {1, m} ≠ 0, so x_i ≠ 0 iff δ_i ≠ 0, and
x_{i*} = 1·1 = 1. (Roots.) Every x_i ∈ P ∪ {0} (Lemmas 1–2), so ρ(x_i) exists. For x ∈ P,
ρ(x)^2 = x and (ρ(x)^u)^d = ρ(x)^{2·u·(d/2)} = x^{u·(d/2)} = x·x^{t(p−1)/2} = x for
u·(d/2) = 1 + t(p−1)/2, since x^{(p−1)/2} = 1; x = 0 gives 0. (u exists because
gcd(d, p−1) = 2 makes d/2 invertible mod (p−1)/2.) So s_i^d = x_i, s_{i*} = ρ(1)^u ≠ 0
(ρ(1) ∈ {1, p−1}), and Σ s_i^d λ_i = Σ x_i λ_i = 0. ∎

Remarks. (i) Rank deficiency needs no special case: zero or repeated columns only change the
first dependencies and make K smaller (all-zero columns: K = 0, x = e_0, s = e_0).
(ii) |supp s| ≥ 1; zero weights are targets "consumed and discarded" by `prop:descent`, as in
the paper. (iii) Columns outside B_0..B_K are never read; the circuit still runs every round
(obliviously) and masks the unused ones. (iv) ρ is chosen for a canonical answer; any root
would do for the descent.

**Lemma 4 (the stop test is a sign test) [proved; also proof-by-computation].** In round k,
with v_1..v_k independent and δ = δ^(k) the first-dependency coefficients:

  v_{k+1} ∈ U_k  ⟺  no δ_i lies in N  ⟺  v_{k+1} = 0.

Hence at the stop round K: x_i = δ_i on B_K (c(1, δ) = 1, the constant m is never used there),
y' = (0, …, 0, 1), and τ_l = y^(K)_{l−1}, so −R = −e_{K+1} has coordinates y^(K)_{<K}.

*Proof.* (⇐) and the last ⇔ are immediate from the definition of v_{k+1} (μ ≠ 0, and the sum
over the empty set is 0). (⇒) Let v_{k+1} ∈ U_k and let δ^P be δ with its N-entries replaced by 0.
Then Σ_i δ^P_i λ_i = e_{k+1} − μ^{−1} v_{k+1} ∈ U_k, so (c', δ^P) is a linear relation among the
list (v_1, …, v_k, λ_B) for suitable c'. Its entry at j* is δ_{j*−k} = 1 (1 ∈ P is kept) and its
entries beyond j* are 0. The first j* vectors of the list are independent, so the relation with
value 1 at j* and zeros beyond is unique (κ = 1 report, Lemma 1(d)); hence δ^P = δ. Then
v_{k+1} = 0 and FD(v_1, …, v_k, 0) = (0, …, 0, 1). ∎

The proof uses two properties of δ: the relations supported on the first j*+1 list entries
form a line (δ is a minimal dependency), and δ has a residue entry (here δ_{j*−k} = 1). Any
scaling of the first dependency with a residue entry has both, including the paper's
normalisation "first nonzero entry 1" (we normalise the last nonzero entry instead; this is
harmless). A non-minimal δ breaks the equivalence. Counterexample (independent reviewer): p = 5,
k = 1, both block columns equal to v_1, δ = (2, 1). Then e = 3v_1 ∈ U_1 and the stop test passes,
but v_2 = 2v_1 ≠ 0 and δ_1 = 2 is a non-residue. It was found by mutation testing (§4): perturbing the constant
m in the round-K weights, or the sign of the y' term, was undetectable on every input, and
Lemma 4 explains why. The circuit uses it (no second elimination per round); the two reference
implementations keep the paper-faithful stop test and second first dependency, so their
agreement with the circuit is also a computational check of Lemma 4, and
`test_stop_lemma4_on_references` checks the three-way equivalence directly.

## 2. The reversible construction

Module `theorems/rees_coherent_sde_k2.py` (new). Encoding, gate set and arithmetic as in the
κ = 1 module: b = ⌈log2 p⌉ qubits per coordinate, LSB first, canonical words < p; X, CX, CCX,
SWAP; `add_product(t, a, b, κ)` (t += κab, 40b²+2b CCX) and `add_scaled(t, a, κ)` from
`theorems/rees_circuit_arith.py`; register allocation, OR flags, Fredkin swaps,
square-and-multiply chains and the simulator `BitSim` reused from
`theorems/rees_coherent_sde.py` (class `CoherentSDEK2` subclasses `CoherentSDE`; neither file
is edited). Registers: inputs L[c][r] (column c, row r), outputs S[c], workspace.

  U = F · C · F^{−1}

with the same Bennett argument as the κ = 1 report: C writes only S, the shared ancillas and
pool registers it cleans itself (X gates on the x registers come in restoring pairs, an
aliasing artefact of the equality test), so F^{−1} returns every non-output wire to 0
[proved: F^{−1}F = id]; the simulator checks it anyway.

**Forward pass F** (every round runs; nothing is skipped on data):

0. run_0 = 1 (one X). Invariant: run_k = [rounds 0..k−1 all continued], and when run_k = 1 the
   registers V hold the genuine v_1..v_k.
1. For k = 0..a:
   a. *First dependency* of the list (v_1..v_k, λ_{B_k}) (a+1 columns in F_p^a) by the κ = 1
      Gauss–Jordan machine, generalised to R × n inputs (`_fd`): workspace copy, coherent
      first-nonzero pivoting (OR flags, prefix chain, Fredkin row swaps), Fermat inverse
      u^{p−2} computed and uncomputed locally, in-place normalisation (t' = wt, t −= w^{−1}t'),
      elimination with stored multipliers, one-hot dep flags, z = −y.
   b. δ_i = −z_{k+i} (`add_scaled`, κ = −1) for the a+1−k block columns.
   c. *Legendre flags* nq_i = [δ_i^{(p−1)/2} = p−1]: square-and-multiply into pool registers,
      an equality test against the constant p−1 (X on the zero bits, AND ladder into the flag,
      X back), chain uncomputed (Euler's criterion; 0 ↦ flag 0).
   d. *v_{k+1}*: masked δ'_i = nq_i ? δ_i : 0 (b CCX), then v_{k+1}[r] += μ·δ'_i·λ_i[r]
      (a(a+1−k) products).
   e. *Stop flag* (Lemma 4): allP_k = AND_i ¬nq_i (X, AND ladder, X), F_k = run_k ∧ allP_k
      (CCX), run_{k+1} = run_k ⊕ F_k (two CX). Exactly one F_k is 1, at k = K: genuine rounds
      reproduce the definition, run_k = 0 after K, and round a always stops when it is genuine
      (U_a = F_p^a).
   Rounds after K run on garbage (V may be dependent); their outputs only enter through
   F_k = 0 or ζ = 0 below.
2. *Coordinates* τ_l = −z^(K)_{l−1} (= y^(K)_{l−1}) for l = 1..a: XOR-select over k ≥ l under
   the one-hot F_k (b CCX per term), then `add_scaled` κ = −1. τ_l = 0 for l > K.
3. *Back substitution*, l = a..1: nζ_l = Legendre flag of τ_l; masked ζ'' = nζ_l ? 0 : τ_l
   (α_{n(ζ)}); τ_j += −ζ''·z^(l−1)_{j−1} for j < l (`add_product` κ = −1, in place; τ_l itself is
   read only). For l > K, τ_l = 0, so these steps add nothing.
4. *Weights* x_i, i ∈ B_k: w = [F_k] (one CX into bit 0, the round-K term of Lemma 4) and, for
   k < a, w += τ_{k+1}·c with c = c(τ_{k+1}, δ_i) ∈ {1, m, μ, 0} loaded as a constant under the
   three case flags (¬nζ∧¬nq, ¬nζ∧nq, nζ∧nq; one CCX each); then x_i = δ_i·w (`add_product`).
   This is x_i = δ_i(F_k + ζ_{k+1}c(ζ_{k+1}, δ_i)), which equals the definition: F_k = 1 only
   in round K, where ζ_{K+1} = τ_{K+1} = 0, and ζ_{k+1} = 0 for k > K.

**Copy stage C** (per column, local compute–copy–uncompute):
- *Oblivious Tonelli–Shanks* with the fixed z = m^Q: a = x^{(Q−1)/2}, r = a·x = x^{(Q+1)/2},
  t = a·r = x^Q (r = t = x when Q = 1); then for j = 0..S−2: u = t^{2^{S−2−j}} by S−2−j
  squarings, k_j = [u = p−1] (equality flag), t ← t·(k_j ? z^{−2^{j+1}} : 1) (skipped at the
  last j) and r ← r·(k_j ? z^{−2^j} : 1), the constants loaded into a zero register by one X and
  CX gates from k_j. Invariant: t_j = z^{2^{j+1}·⌊k/2^j⌋} where t_0 = z^{2k}, so u = (−1)^{k_j} and
  finally r = x^{(Q+1)/2} z^{−k}, r² = x^{Q+1}/x^Q = x [proved, standard]; x = 0 gives r = 0.
  No data-dependent loop bound: S−1 rounds always.
- *Even root*: σ = r_0 ? p−1 : 1 (X on bit 0, CX from bit r_0 onto the bits of p = 1 ⊕ (p−1)),
  ρ = r·σ (`add_product`): r even ↦ r, r odd ↦ p−r (even).
- *Power*: ρ^u by square-and-multiply (nothing for u = 1, e.g. d = 2), `add_scaled(S_i, ρ^u, 1)`,
  then the whole chain is uncomputed (reversed list) and its registers and flag bits go back to
  the pools.

**Theorem 5 (coherent κ = 2 SDE) [proved, conditional on the arithmetic macros on canonical
inputs (proof-by-computation for p ≤ 13, argued beyond); proof-by-computation on the §4 sets;
AI-checked].** For every odd
prime p, a ≥ 1 and d with gcd(d, p−1) = 2, the gate list U of `CoherentSDEK2(p, a, d)` maps
|λ⟩|0⟩_S|0⟩_work ↦ |λ⟩|s(λ)⟩_S|0⟩_work on every canonical input λ ∈ (F_p^a)^M,
M = (a+1)(a+2)/2, with s the canonical witness of §1; s ≠ 0 and Σ s_i^d λ_i = 0. (Theorem 3,
Lemma 4, the step-by-step correspondence above, and the correctness of the arithmetic macros
on canonical inputs, which is [proof-by-computation] for p ≤ 13 in the I146 report and
[argued] beyond; §4 checks U itself.)

## 3. Gate and qubit counts [exact count]

Notation: b = ⌈log2 p⌉; ℓ(n) = (bitlen(n)−1) + (hw(n)−1) for n ≥ 2 and ℓ(1) = 0 (products of
left-to-right square-and-multiply); I_p = ℓ(p−2) (Fermat inverse), L_p = ℓ((p−1)/2) (Euler
test), p−1 = 2^S Q (Q odd), h = (Q−1)/2, and the Tonelli–Shanks product count

  T_p = [h ≥ 1]·(ℓ(h) + 2) + (S−1)(S−2)/2 + 2(S−1) − [S ≥ 2]

(T_p = 0 at p = 3; T_p = ℓ(h)+2 for p ≡ 3 mod 4; T_p ≤ 2b + S²/2 + 2S). M = (a+1)(a+2)/2,
λ_b = 2b−3 (b ≥ 3), λ_2 = 1 (one b-wire AND ladder).

**Macros (whole circuit U)** (`closed_form_macros`, `closed_form_products_poly`):

  n_F = (a⁴ + 4a³ + 13a² + 12a + 2)/2 + I_p(2a² + 2a) + L_p(a² + 5a + 2),
  #add_product = 2n_F + 2M(T_p + 1 + ℓ(u)),   #add_scaled = 2(M + a) + M.

Breakdown of n_F: (a+1) first dependencies on a+1 columns in F_p^a, each
a² + 3a + (a−1)a(a+1)/2 + 2aI_p products (the κ = 1 count at g = a); 2L_p per Legendre flag for
the M δ's and a ζ's; aM for the v's; a(a−1)/2 for the back substitution; M−1 for ζ·c; M for
x = δ·w. Copy stage: per column T_p + 1 (even root) + ℓ(u), computed and uncomputed.

**Toffoli (exact; `closed_form_toffoli`)**:

  T_CCX = (40b²+2b)·#add_product + 2(M+a)·H_{−1} + M·H_{1}
          + 2·[(a+1)·fd_ccx(a, a+1) + (M+a)λ_b + bM + Σ_{k=0}^{a}(and(a+1−k) + 1)
               + b·a(a+1)/2 + b(a−1) + 3(M−1)] + 2M(S−1)λ_b,

with H_κ the add_scaled CCX count of `formula_counts` (10b²+8b+2H), and(n) = 0, 1, 2n−3 for
n = 1, 2, ≥ 3, and fd_ccx(R, n) = Σ_{k<min(n,R)} [(R−k)λ_b + 2(R−k) − 1 + b(R−1−k)(n−k) + 2b +
b(R−1)] + b·s'(s'−1)/2 (s' = min(n,R) + [n = R+1]; OR flags, prefix chain, Fredkins, w/w^{−1}
loads, multipliers, selection). Hence

  **T_CCX = 40a⁴b² + O(a³b² + a²b³ + a²S²b²)**, and the total gate count is
  O(a⁴b² + a²b³ + a²S²b²) (each product ≤ 158b²+46b−4 gates).

**Qubits (exact; `closed_form_qubits`)**:

  Q = b(5a³/2 + 23a²/2 + 19a + 8) + 3a³/2 + 5a² + 25a/2 + 11 + max(0, b−2, a−1)
      + b·max(1, I_p, L_p, T_p + W_S + 2 + ℓ(u)) + (S−1),     W_S = max(0, 2S−3),

i.e. Q = (5/2)a³b + O(a²b + a³ + b·T_p). The last max is the shared register pool (largest
local demand: a normalisation, a Fermat chain, a Legendre chain, or one copy-stage root with its
W_S constant-multiplier registers); S−1 Tonelli–Shanks flag bits.

All three closed forms equal the generator on 55 rows of `run.json` (p ∈ {3, 5, 7, 13, 17, 101,
257, 1031, 65537, 2³¹−1, 2⁶¹−1}, a ∈ {1, 2, 3, 4, 8}, d = 2) and in 120 further rows
(d ∈ {2, 4, 6, 10} with κ_d = 2, p up to 65537, a ≤ 4; `test_closed_forms` keeps 12). The
program-level count equals the length of the emitted gate list
(`test_emitted_counts_equal_program_counts`).

Selected rows (d = 2, so u = 1):

| p | b | a | M | I_p | L_p | T_p | add_product | CCX | all gates | qubits |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 1 | 3 | 0 | 0 | 0 | 38 | 6 966 | 30 104 | 116 |
| 3 | 2 | 2 | 6 | 0 | 0 | 0 | 138 | 24 238 | 104 738 | 297 |
| 5 | 3 | 2 | 6 | 2 | 1 | 1 | 230 | 87 334 | 351 466 | 418 |
| 13 | 4 | 2 | 6 | 5 | 3 | 3 | 390 | 257 946 | 1 027 796 | 543 |
| 13 | 4 | 8 | 45 | 5 | 3 | 3 | 9 510 | 6 222 114 | 24 877 664 | 9 935 |
| 101 | 7 | 4 | 15 | 9 | 7 | 7 | 2 262 | 4 502 682 | 17 089 786 | 3 309 |
| 1031 | 11 | 2 | 6 | 12 | 11 | 11 | 910 | 4 456 786 | 16 201 024 | 1 452 |
| 65537 | 17 | 2 | 6 | 30 | 15 | 134 | 2 946 | 3.42·10^7 | 1.19·10^8 | 4 807 |
| 2³¹−1 | 31 | 4 | 15 | 59 | 58 | 58 | 11 668 | 4.50·10^8 | 1.75·10^9 | 15 394 |
| 2⁶¹−1 | 61 | 1 | 3 | 119 | 118 | 118 | 3 586 | 5.35·10^8 | 2.07·10^9 | 9 910 |
| 2⁶¹−1 | 61 | 2 | 6 | 119 | 118 | 118 | 8 186 | 1.22·10^9 | 4.72·10^9 | 14 279 |
| 2⁶¹−1 | 61 | 8 | 45 | 119 | 118 | 118 | 77 072 | 1.15·10^10 | 4.45·10^10 | 141 314 |

Where the cost goes. At the small a of the paper's instances, the field-exponentiation terms
dominate: at (2⁶¹−1, a = 2), 2I_p(2a²+2a) = 2 856 (Fermat inversions), 2L_p(a²+5a+2) = 3 776
(Euler tests) and 2M·T_p = 1 416 (roots) of the 8 186 products; the a-polynomial part is 126 and
the even-root products 12. Standard savings, not implemented: Montgomery batch inversion of the a pivots per round,
and a single batched Euler test (the M + a Legendre flags are independent). The a⁴ term comes
from re-eliminating the v's in every round; keeping an incremental RREF of V would lower its
constant but not its order. Against the κ = 1 solver at the same label dimension
(g³ + O(g²) + 4gI_p + … products), the κ = 2 solver costs a factor ≈ a more products at large a
(a⁴ against g³), plus the Legendre and root terms.

## 4. Checks

Simulator: `BitSim` (exact bit-sliced basis-state simulation; the circuit is a permutation, so
basis inputs suffice). Two references, both written independently of the circuit and both
paper-faithful (they run the second first dependency of step 3 and use the general y' and
c(1, δ) formulas that Lemma 4 removes from the circuit):
`canonical_witness_k2` (definition level: incremental span tests, a separate Tonelli–Shanks
made even) and `canonical_witness_k2_batch` (vectorised Gauss–Jordan). They agree on all inputs
at (3, 1), (5, 1), (7, 1), (13, 1) and on 2 600 structured inputs at (3, 2), (5, 2), (13, 2),
(5, 3), (7, 3); there every definition-level witness passes `check_witness` (s ≠ 0, canonical,
Σ s_i^d λ_i = 0) and has x_{i*} = 1 (Theorem 3). `first_dependency` equals the κ = 1 module's
`canonical_witness` (e = 1) on 300 random lists. The circuit is also compared with the
definition-level reference directly on 310 structured inputs at (5, 2), (7, 3), (13, 2)
(`test_circuit_equals_definition_reference`).

For every input the circuit check asserts: S = the canonical witness (batched reference);
S canonical (< p); every input wire restored; every workspace wire 0 (all wires other than
inputs and outputs: arithmetic ancillas, ladder temporaries, pools and all history); s ≠ 0;
Σ s_i^d λ_i = 0; for u = 1, every s_i even (the root normalisation).

**Exhaustive [proof-by-computation], all p^{aM} canonical inputs, all checks pass**
(`run.json`; "K" = how many inputs stop at each round):

| p | a | d | u | inputs | gates | qubits | K = 0, 1, (2) | sim time |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 2 | 1 | 27 | 30 104 | 116 | 21, 6 | 0.05 s |
| 5 | 1 | 2 | 1 | 125 | 117 826 | 167 | 85, 40 | 0.2 s |
| 7 | 1 | 2 | 1 | 343 | 168 262 | 166 | 217, 126 | 0.2 s |
| 11 | 1 | 2 | 1 | 1 331 | 360 678 | 216 | 781, 550 | 0.4 s |
| 13 | 1 | 2 | 1 | 2 197 | 381 416 | 221 | 1 261, 936 | 0.5 s |
| 17 | 1 | 2 | 1 | 4 913 | 706 578 | 316 | 2 737, 2 176 | 0.8 s |
| 19 | 1 | 2 | 1 | 6 859 | 661 502 | 268 | 3 781, 3 078 | 0.8 s |
| 23 | 1 | 2 | 1 | 12 167 | 797 896 | 273 | 6 601, 5 566 | 1.0 s |
| 29 | 1 | 2 | 1 | 24 389 | 829 922 | 279 | 13 021, 11 368 | 1.3 s |
| 31 | 1 | 2 | 1 | 29 791 | 939 998 | 278 | 15 841, 13 950 | 1.8 s |
| 37 | 1 | 2 | 1 | 50 653 | 1 138 816 | 329 | 26 677, 23 976 | 2.2 s |
| 41 | 1 | 2 | 1 | 68 921 | 1 248 870 | 354 | 36 121, 32 800 | 2.8 s |
| 7 | 1 | 4 | 2 | 343 | 177 454 | 169 | 217, 126 | 0.3 s |
| 11 | 1 | 4 | 3 | 1 331 | 391 686 | 224 | 781, 550 | 0.5 s |
| 13 | 1 | 10 | 5 | 2 197 | 427 928 | 233 | 1 261, 936 | 0.7 s |
| 3 | 2 | 2 | 1 | 531 441 | 104 738 | 297 | 303 993, 176 904, 50 544 | 0.7 s |
| 3 | 2 | 4 | 1 | 531 441 | 104 738 | 297 | same | 0.8 s |
| 5 | 2 | 2 | 1 | 244 140 625 | 351 466 | 418 | 105 390 625, 94 350 000, 44 400 000 | 1 781 s (chunked, `exhaustive_p5_a2.json`) |

(p = 5, 13, 17, 41 have S = 2, 2, 4, 3, so the Tonelli–Shanks rounds are exercised; at p = 3
the only nonzero square is 1, so s depends only on supp x there.)

**Root circuit, exhaustive [proof-by-computation]** (`root_check`: the copy stage alone on
every x ∈ P ∪ {0}; output ρ(x)^u, x restored, workspace 0): p ∈ {3, 5, 7, 11, 13, 17, 41, 97,
257, 65537} (S up to 16; 32 769 squares at 65537, 1.09·10^7 gates), and with u > 1 at
(7, 4), (11, 4), (13, 10), (29, 6). All pass.

**Sampled [sampled], 8 192 structured inputs each** (`structured_inputs`: columns random, zero,
multiples or combinations of earlier columns, and a quarter of the inputs inside a random
lower-rank subspace; every K ∈ {0..a} occurs, `test_structured_inputs_hit_every_K`):
(p, a, d) = (5, 2, 2), (7, 2, 2), (11, 2, 2), (13, 2, 2), (17, 2, 2), (41, 2, 2), (7, 2, 4),
(13, 2, 10), (3, 3, 2), (5, 3, 2), (7, 3, 2), (11, 3, 2), (13, 3, 2), (3, 4, 2), (5, 4, 2): all
pass. K = a occurs 4–420 times per row (e.g. 106 at (13, 3), 13 at (5, 4)).

**Mutations (the checks are not vacuous)** (`test_*mutations_detected`): changing the constant m
in the back-substitution weights ((5, 2) and (7, 2)), μ in v ((5, 1) exhaustive), the sign of the
τ term ((3, 2) exhaustive) or the sign of the output `add_scaled` ((5, 1)); dropping the first,
middle or 97th-percentile CCX of F, or its first X ((3, 2) exhaustive); dropping the last
multiply-accumulate of F ((5, 1)): every mutant fails the check. Two mutants of the first
version survived on every input (m in the round-K weights; the sign of the y' term): that led to
Lemma 4, and both terms were removed from the circuit. Mutating m at p = 3 is undetectable by
design (m·δ and δ are both nonzero, and ρ(1) = ρ(2) = 2 there).

**Structure.** No gate or macro of U targets an input wire; macros of C target only S or pool
registers, CX/CCX of C never target an x register, and X gates of C on x registers come in
pairs (`test_inputs_never_targeted_and_copy_stage_footprint`). d with κ_d ≠ 2 is refused
(`ValueError`).

Commands:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde_k2.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_coherent_sde_k2.py -k slow
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_coherent_sde_k2 --out research/audits/reviews/2026-11-04-rees-coherent-sde-k2/run.json      # ~3 min, log in run.log
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_coherent_sde_k2 --chunked 5,2,2 --out research/audits/reviews/2026-11-04-rees-coherent-sde-k2/exhaustive_p5_a2.json   # ~35 min
```

## 5. What this closes and what it does not

**Closes (κ_d = 2 grades).** At every grade with gcd(d, p−1) = 2, in particular d = 2 for
every odd p, the diagonal-equation solve no longer needs a mid-circuit measurement and classical
feed-forward: a permutation circuit of 40a⁴b² + O(a³b² + a²b³ + a²S²b²) Toffoli gates and
(5/2)a³b + O(a²b + a³ + b² + S²b) qubits maps the labels to the canonical witness with clean
workspace, exactly, on every canonical input (given the macros; item 4 below). Its only constants are m (or any consecutive pair
μ ∈ P, μ+1 ∈ N: Lemma 1 uses nothing else), z = m^Q and u, all column-independent. The
least-non-residue search is deterministic, with a proven bound p^{1/(4√e)+o(1)} unconditionally
(Burgess) and O(log² p) under GRH. Given any non-residue n (the input `prop:triangular-sde`
assumes), a pair (j, j+1) with j ∈ P, j+1 ∈ N comes from binary search on [1, n] in O(log p)
Euler tests [argued; elementary]. Nothing is randomised: the Las Vegas κ-th roots of
`prop:triangular-sde` become an oblivious Tonelli–Shanks with S−1 fixed rounds.

With `lem:coherent-linear-sde` (κ_d = 1) and the deferred-measurement argument of the κ = 1
report §5 (labels held in registers, the controlled right actions of `prop:descent` controlled
on the witness register, and `prop:descent` holding for every positive-probability label tuple
and every valid witness), the SDE solve is coherent at **every** grade with κ_d ≤ 2:

- **Class 2 (every instance, every odd p): yes, modulo wiring.** The only SDE grade is d = 2.
  So the receiver of a class-2 instance has no classical step between quantum segments, apart
  from the final Fourier-sampling measurement, provided the merge applies the controlled δ_s
  with s a quantum register. That wiring is not done and not simulated. The arity
  is (g_2+1)(g_2+2)/2: 3 for the Heis(F_p) cover (g_2 = 1, the same as the generator's 2g_2+1 = 3),
  but larger than 2g_2+1 when g_2 ≥ 2 (owner decision: changing the merge arity at κ = 2).
- **Class 3: yes iff p ≡ 2 (mod 3)**, modulo wiring. Then κ_3 = 1 (`lem:coherent-linear-sde`) and
  κ_2 = 2 (here). Example: n4(F_5), with grade 2 at a = 2 (arity 6, against the generator's 5) and
  grade 3 at g = 1 (arity 2). For p ≡ 1 (mod 3), e.g. n4(F_7), grade 3 has κ_3 = 3 and stays
  classical.
- **Class c in general: every grade iff gcd(p−1, lcm(2, …, c)) = 2**, i.e. p ≢ 1 (mod q) for every
  odd prime q ≤ c and, if c ≥ 4, p ≡ 3 (mod 4). Even grades then have κ_d = 2 (covered here with
  the Bezout exponent u; d = 4, 6, 10 tested) and odd grades κ_d = 1. Example: every safe prime
  p = 2q+1 with q > c. Not n5(F_5) (κ_4 = 4).

**Does not close.**

1. **κ_d ≥ 3 stays classical** (e.g. grade 3 at p ≡ 1 mod 3, grade 4 at p ≡ 1 mod 4). Lemma 4 is
   special to κ = 2. With κ−1 ≥ 2 nonzero classes, v ∈ U_k constrains only a β-weighted
   combination of the class sums, so the second elimination per round would be needed again.
2. **Not wired into the generated receiver** (`rees_circuit_general.py` / `rees_circuit_sparse.py`
   still apply a classical s), and the n4(F_5) end-to-end simulation has not been rerun at
   grade-2 arity 6. `coherent_receiver_implemented` stays false.
3. **Canonical inputs only**; padding words in the label registers are not claimed.
4. **Correctness beyond the checked sets is [argued]**: Theorem 3 and Lemma 4 are proved for all p
   and a. The macro gate lists are proof-by-computation for p ≤ 13 only (I146 report). U itself is
   exhaustive for a = 1 at every prime p ≤ 41 (and the d = 4, 10 cases) and for a = 2 at p = 3
   and p = 5, and sampled for a = 2 (p ∈ {5, 7, 11, 13, 17, 41}), a = 3 (p ≤ 13) and a = 4
   (p ≤ 5).
5. No QFT_p, oracle, noise, depth or layout work, and no asymptotic claim about the receiver. The
   triangular arity is not adopted by the paper's counts (`rem:triangular-scope`), and this
   module does not change Theorem `thm:main`, Table `tab:main-regimes` or any budget.

## 6. Proposed paper text (not applied; main.tex untouched)

Placement: immediately after the artifact paragraph that follows `lem:coherent-linear-sde`
(main.tex, Section `sec:uniform-compilation`, before `\subsection{Reproducible Resource
Profiles}`). Macros as in the paper (`\Fp`, `\file`).

```latex
\begin{lemma}[Coherent witness at $\kappa_d=2$; AI-checked, pending human review]
\label{lem:coherent-quadratic-sde}
Let $p$ be an odd prime, $a\ge1$, and $d$ with $\kappa_d=\gcd(d,p-1)=2$; let $b=\lceil\log_2p\rceil$, $p-1=2^SQ$ with $Q$ odd, $m$ the least quadratic non-residue, $\mu=m-1$, and $u\ge1$ with $u\,d/2\equiv1\pmod{(p-1)/2}$. Then $(\alpha,\beta)=((1,0),(0,\mu))$ is a universal two-level contraction at $\kappa=2$ in the normalisation of Proposition~\ref{prop:triangular-sde}. Run that proposition on $M=(a+1)(a+2)/2$ columns $\lambda_1,\dots,\lambda_M\in\Fp^a$ with this contraction, taking for $\delta$ in round $k$ the first linear dependency (as in Lemma~\ref{lem:coherent-linear-sde} with $e=1$, so normalised by its last nonzero entry) of the list $v_1,\dots,v_k$ followed by the columns of block $k$, and put $s_i=\rho(x_i)^u$, where $\rho(x)$ is the even one of the square roots of $x$ in $\{0,\dots,p-1\}$. Then the stop test $v_{k+1}\in U_k$ of round $k$ holds if and only if no $\delta_i$ is a non-residue, if and only if $v_{k+1}=0$; moreover $s\ne0$ and $\sum_i s_i^d\lambda_i=0$. There is a circuit of $X$, CNOT, Toffoli and SWAP gates that maps $|\lambda\rangle|0\rangle|0\rangle$ to $|\lambda\rangle|s(\lambda)\rangle|0\rangle$ for every $\lambda$ with canonical coordinates. It uses $2n_F+2M\bigl(T_p+1+\ell(u)\bigr)$ modular multiply-accumulates, where $n_F=\tfrac12(a^4+4a^3+13a^2+12a+2)+(2a^2+2a)\,\ell(p-2)+(a^2+5a+2)\,\ell(\tfrac{p-1}2)$, $\ell$ is as in Lemma~\ref{lem:coherent-linear-sde}, and $T_p\le 2b+S^2/2+2S$ is the multiplication count of a Tonelli--Shanks square root with $S-1$ fixed rounds. In all it uses $40a^4b^2+O(a^3b^2+a^2b^3+a^2S^2b^2)$ Toffoli gates and $\tfrac52a^3b+O(a^2b+a^3+b^2+S^2b)$ qubits.
\end{lemma}

\begin{proof}[Proof sketch]
By minimality of $m$, $\mu\in P=(\Fp^\times)^2$, so $\alpha_1+\beta_0=0$, $\alpha_0+\beta_1=m\notin P$ and $\alpha_1+\beta_1=\mu\in P$, which is the contraction condition. The stop test: if $v_{k+1}=\mu\sum_{\delta_i\notin P\cup\{0\}}\delta_i\lambda_i$ lies in $U_k$, then so does $\sum_{\delta_i\in P}\delta_i\lambda_i$, which gives a dependency of the list with the same last index $j^*$ and the same value $1$ there; the first dependency is unique, so $\delta$ has no non-residue entry. In particular the final round has weights $x_i=\delta_i$, and the coordinates of $-R$ are those of $-e_{K+1}$, read off the same dependency. Proposition~\ref{prop:triangular-sde} gives $x\in(P\cup\{0\})^M$, $x\ne0$ and $\sum_ix_i\lambda_i=0$; since $\rho(x)^{ud}=x^{u d/2}=x$ on $P\cup\{0\}$, $s$ solves~\eqref{eq:sde-target}. The circuit is $F\cdot C\cdot F^{-1}$. $F$ runs all $a+1$ rounds obliviously: the first dependency by the machine of Lemma~\ref{lem:coherent-linear-sde} on $a+1$ columns, Legendre flags by Euler's criterion, $v_{k+1}$ with masked coefficients, one-hot stop flags from the Legendre flags, the coordinates selected under the stop flags, the back substitution with $\alpha$ masked by the Legendre flag of $\zeta$, and the weights with the constants $1,m,\mu$ loaded under flags. $C$ computes, per column, a square root by Tonelli--Shanks with the fixed generator $m^Q$ of the $2$-Sylow subgroup (each round an equality flag and two multiplications by constants loaded under it), normalises it to the even root, raises it to the power $u$, adds the result into the output and uncomputes. $C$ leaves every wire of $F$ unchanged, so $F^{-1}$ clears the workspace.
\end{proof}

The artifact \file{theorems/rees_coherent_sde_k2.py} (report \file{research/audits/reviews/2026-11-04-rees-coherent-sde-k2.md}; finite computation, AI-checked, pending human review) emits this circuit and checks it on every canonical input for $a=1$, $p\le41$, and for $a=2$, $p\in\{3,5\}$, with $a\le4$ sampled; together with Lemma~\ref{lem:coherent-linear-sde} it makes the solve of~\eqref{eq:sde-target} coherent at every grade with $\kappa_d\le2$, hence at every grade when $\gcd(p-1,\operatorname{lcm}(2,\dots,c))=2$, at merge arity $(g_d+1)(g_d+2)/2$ when $\kappa_d=2$, which equals the generated arity $2g_d+1$ only for $g_d=1$, and it is not wired into the generated circuits.
```

(The final sentence is the "one sentence". The p = 5, a = 2 exhaustive run it cites is complete:
all 5^12 inputs pass, §4.)

## 7. Claim gates

`research/reductions/rees_hsp_reduction.json` untouched. `STATUS` of the new module:
`coherent_receiver_implemented: False`, `general_sde_implemented: False`,
`coherent_kappa_ge3_sde_implemented: False`, `wired_into_generated_receiver: False`,
`independent_review: False`, `speedup_claim_allowed: False`; only
`coherent_kappa2_sde_implemented: True`, scoped to κ_d = 2, the triangular arity and canonical
inputs. No claim of quantum advantage, of an asymptotic receiver cost or of a native
application follows.

## 8. Files

- `theorems/rees_coherent_sde_k2.py` (new): `CoherentSDEK2(p, a, d)` (program, `flatten()`,
  `counts()`), references `canonical_witness_k2`, `canonical_witness_k2_batch`,
  `first_dependency`, `check_witness`, closed forms `closed_form_macros / _toffoli / _qubits /
  _products_poly`, `root_circuit` / `root_check`, `exhaustive_check(_chunked)`, `sampled_check`,
  `count_row`, CLI `main`.
- `tests/test_rees_coherent_sde_k2.py` (new).
- `research/audits/reviews/2026-11-04-rees-coherent-sde-k2/run.json`, `run.log`,
  `exhaustive_p5_a2.json`, `exhaustive_p5_a2.log` (artifacts).
- This report. No existing file edited; nothing committed or pushed.

## 9. Next hard question

Wire both coherent solvers into the merge: replace the classical s of
`rees_circuit_general.merge_ops` by the witness register, with the controlled right translation
x ↦ x·(−δ_s(σ(q))) (grade-j coordinates scaled by s^j: j−1 more products per coordinate), and
rerun the n4(F_5) sparse simulation at grade-2 arity 6. Acceptance: the coherent pipeline's
reduced output on Q equals ρ_{HZ/Z} on every positive-probability label tuple of the existing
n4(F_5) instances, with exact (Z[ζ_5]) state comparison. For κ = 3 (n4(F_7)), the triangular
solver needs a precomputed contraction (E_2(3) = ∅), cube roots by an oblivious
Adleman–Manders–Miller with a fixed non-cube, and the second elimination per round (Lemma 4
fails).

## 10. Independent review (AI subagent, unanchored)

A separate AI agent was given the report's §1–2, the paper's `prop:triangular-sde` and the code,
but not this session's conclusions. It wrote its own implementation of the definition (equal to
`canonical_witness_k2` on 43 200 random inputs, p ≤ 97, a ≤ 4, several d with κ_d = 2, with
Lemma 4 and x_{i*} = 1 asserted throughout) and emulated the forward pass including the garbage
rounds and masks. It checked the oblivious Tonelli–Shanks on every square for every prime below
4000 and sampled S ≤ 30. It ran the circuit exhaustively at a = 1 for p = 19, 23, 31, 37 and
sampled it at a = 2 for p = 19, 97.

Verdicts: Lemma 1, Theorem 3, the masking and `_sqrt_chain` are correct. Lemma 4's proof is
correct, but its stated scope was too narrow (now fixed in §1, with the reviewer's
counterexample for a non-minimal δ). The overclaims it found are fixed: the a = 1 prime list
(now every p ≤ 41 in `run.json`), the Theorem 5 tag (now conditional on the macros above
p = 13), the sampled-prime list, the module docstring, and the missing direct
circuit-versus-definition test (added). No mathematical error was found. This is not human
review.
