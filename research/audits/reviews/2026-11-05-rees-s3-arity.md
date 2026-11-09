# Rees Schedule 3: arity at the zero-sum grade Γ_0 (2026-11-05)

**Status: AI-checked, pending human review.** Overnight AI-only pass, with no owner input. No
`.tex` file, registry/JSON claim gate, `AGENT_HANDOFF.md` or `STATE.md` was edited, and nothing
was committed. Code and outputs: `research/audits/reviews/2026-11-05-rees-s3-arity/`.

Labels: **[proved]** = full proof here. **[computed]** = exact or Monte Carlo computation in
the folder; every algorithmic output was checked exactly. **[cited]** = outside result read
from a local full text in `2026-11-02-rees-linear-arity/lit/`; numbering and hypotheses
**NEED HUMAN VERIFICATION**. **[conjecture]** = not proved.

## Summary

Setting: `lem:fc-zero-sum`, `rem:fc-zero-sum-sis`. At d ∈ Γ_0 we have d = p−1 = κ_d. A node
at d must find a nonempty T ⊆ [M] with Σ_{i∈T} λ_i = 0. Its labels λ_i are i.i.d. uniform on
an unknown subspace K_d^⊥ ≤ F_p^{g_d}. The weights are binary {0,1}, not P∪{0} for a larger
P: at κ = p−1, P = {1}. By Z1 of the 11-04 report, this is average-case BinSIS(a, M, p) with
a = dim K_d^⊥ ≤ g_d.

1. **Targets (1) and (2) are not reached.** I found no polynomial-time node at Γ_0 with arity
   o(g²) for any fixed p, and none with time and arity f(p)·poly(g). Both stay open.
2. **Partial progress on (2) [proved; novelty NEEDS HUMAN VERIFICATION]: the weight-doubling
   node (Theorem P).** For every prime p ≥ 3 there is a deterministic classical algorithm
   with the following properties.
   - **Input and output.** It reads i.i.d. uniform columns of F_p^n one at a time. With
     probability 1 it halts and returns a nonempty zero-sum subset, and the subset is
     checked exactly.
   - **Expected reads.** It reads, in expectation, exactly N_0(n) columns, with
     N_0(n) ≤ (s_p+1)^{j*}·C(n+j*+1, j*+1), where j* = ⌈log₂(p−1)⌉ and
     s_p ≤ min(p, ⌈2 log₂(p−1)⌉+4).
   - **Time.** Its time is O(R(n²+p)) operations in F_p, where R is the number of columns read.
   - **Growth.** The exponent of n is **1+⌈log₂(p−1)⌉**, and the factor depending on p is
     p^{O(log log p)}.
   - **Fixed-arity node (Cor. P.4).** It is a public node at Γ_0 of arity
     O_c(g^{1+⌈log₂ c⌉}·log(1/τ)) that aborts with probability ≤ τ and runs in polynomial
     time.
   - **Comparison at Γ_0.** Schedule 1 has exponent c⌈log₂(c+1)⌉. The best average-case
     bound in the local literature, KMOSW Thm 1.10 [cited], has exponent 1+⌊(c+4)/4⌋ and
     factor p^{p²}, at failure probability 2^{−Ω(n)}. At constant abort probability τ the
     new exponent is smaller for every p ≥ 17 except p = 19, which ties. It is larger at
     p = 7 and 11, and equal at p = 3, 5 and 13. At τ = 2^{−n}, the factor log(1/τ) adds 1:
     the new exponent is then smaller only for p = 29 and every prime p ≥ 31, ties at
     p = 17 and 23, and is larger at p = 19 (7 vs 6) and at every p ≤ 13.
   - **[computed]** The measured mean reads agree with the exact expectation (44 rows, max
     |z| = 2.62 at p = 7, n = 3; reads are heavy-tailed and R ≥ 20) for p = 3, 5, 7, 11, 13, 17 and n up to 96, 32, 14, 8, 8 and 7. All
     outputs passed the exact check.
3. **Barriers [proved]: the natural routes to (1) cannot work.**
   - **B1. Disjoint merge trees** (BKW-type and disjoint-matching variants of
     Wagner/generalized birthday, coordinate-block recursion, Davenport per block). Here a
     merge tree reads linear sketches of the columns in a filtration order and replaces its
     items by pairwise disjoint unions of items. Wagner's k-tree proper keeps all matching
     pairs and reuses elements, so it is not in the model; its superpolynomial cost
     2^{O(n/log(m/n))} is Wagner's own analysis [cited, KMOSW §1.3]. For an
     LSDM, Pr[success with ≥ L stages] ≤ M·(2p/(p+1))^{−L}. With fan-in ≤ F, the
     arity is M ≥ exp(Ω(√(n·ln p·ln(2p/(p+1))/F))). So disjoint BKW-type merging is
     superpolynomial in arity even with unlimited time. With unbounded fan-in and poly arity, some
     stage faces an average-case BinSIS instance in dimension ≥ n·ln(2p/(p+1))/ln(2M/δ):
     informally, the same problem up to a log factor (a reading, not a formal reduction).
   - **B2. Flag-switch recursion** (the KMOSW Thm 1.10 template, which includes Theorem P,
     with arbitrary, even sparse or exponential-time, switch finders). Its arity is
     Ω_p(n²/log n), so this template can never reach n^{2−ε}.
   - **B3. Oblivious information sets.** Success ≤ T·(2/p)^n after T trials.
   - **B4. Zero-sum theorems (EGZ, Olson, Davenport, Chevalley–Warning)** give totality at
     g(p−1)+1 and membership in PPA_p [cited GKSZ]. They give no search algorithm. In the
     average case the existence threshold is ≈ g log₂ p. At fixed p, ℓ₂-short vectors of
     the q-ary lattice are p·e_i, not binary solutions.
   - **B5. Doubling depth.** Any chain of weight sets D^{(j+1)} ⊆ D^{(j)} − D^{(j)} that
     starts at {0,1} needs ⌈log₂(p−1)⌉ steps to reach F_p. This is why Theorem P is not FPT.
4. **Paper impact.** A proposed `rem:fc-zero-sum-arity` (Part F) states Theorem P as a public
   option at Γ_0 and states B1, B2 and B3. Nothing is adopted in (R1), and no table changes.
   For `thm:free-coordinate`(iii) at fixed c the Γ_0 node becomes O_c(g^{1+⌈log₂ c⌉}) instead
   of B_c(g). In the regime p = O(log m) of `rem:fc-zero-sum-sis`(d), the node is polynomial
   whenever log g·log p = O(log m). The reachable-sum node needs g·log p = O(log m).
5. **Side finding [NEEDS HUMAN VERIFICATION].** Imran–Ivanyos (arXiv 2304.08376, end of §6)
   sketch a worst-case-to-average-case reduction with S²/δ blow-up. Its second step applies
   the average-case algorithm to the vectors Σ_{T_g} r_i = −Σ_{T_g} u_i. These are functions
   of the worst-case input and are not uniform in general (with u_i = e for every i, they all
   lie on the line F_p·e). So the sketch looks incomplete. If it held, KMOSW Thm 1.10 would
   give a randomized worst-case bound of n^{2+2⌊(q+3)/4⌋}, which would beat KMOSW
   Thm 1.11 ((n+1)^{q−1}) for q ≥ 11. This report does not use it.

**Claim gates that must stay false:** every Rees gate. No claim of a polynomial node at
o(g²), of FPT, of worst-case improvement, or of any change to Schedule 3's polynomial regime.

## 0. Problem, quantifiers, access model

- **BinSIS(n, M, p), average case.** Given columns v_1, …, v_M i.i.d. uniform in F_p^n, output
  a nonempty T ⊆ [M] with Σ_T v_i = 0. Success probability is over the columns (and coins).
  Weights are binary. Signed weights {0,±1} are "level 1" below, and D^{(j)} is level j.
- **Node at Γ_0.** The bank is λ_1, …, λ_M, i.i.d. uniform on an unknown K_d^⊥ of dimension
  a ≤ g_d (`lem:fc-forest`(a)). The node may abort and must never return a wrong witness. The
  witness is checked as in (F5) and converted as in (F6) (`lem:fc-zero-sum`(d)). An abort
  probability ≤ τ_d is charged to `lem:fc-forest`(b) exactly as for the variant after
  `lem:fc-zero-sum`.
- **Classical access.** Theorem P is classical and deterministic given the bank. The barriers
  B1 and B2 are information-theoretic within their models: they allow unbounded computation.

## P. The weight-doubling recursion

### P.1 Statement

Let j* = ⌈log₂(p−1)⌉ (so j* = 1, 2, 3, 4, 4, 4, 5 at p = 3, 5, 7, 11, 13, 17, 19). Weight
sets: D^{(0)} = {0,1}, and D^{(j)} = {−2^{j−1}, …, 2^{j−1}} ⊂ ℤ for j ≥ 1, read mod p.
Since 2^{j*−1} < p−1, nonzero elements of D^{(j)} are nonzero mod p. Let s_p be the expected
number of i.i.d. uniform β ∈ F_p drawn until the subset sums of the draws cover F_p.

**Theorem P [proved].** For every prime p ≥ 3 and n ≥ 0 there is a deterministic algorithm
𝒜_0(n) with the following properties. Its input is a stream of i.i.d. uniform columns of
F_p^n. With probability 1 it halts and returns a nonempty set T of stream indices with Σ_T v_i = 0. The
number R of columns it reads satisfies

  E[R] = N_0(n),  where  N_{j*}(d) = d+1,  N_j(d) = 1 + s_p Σ_{e=0}^{d−1} N_{j+1}(e)  (j < j*),

and

  N_0(n) ≤ (s_p+1)^{j*}·C(n+j*+1, j*+1),   s_p ≤ min(p, ⌈2 log₂(p−1)⌉ + 4).

It uses O(R(n² + p)) operations in F_p. So
E[R] = p^{O(log log p)}·n^{1+⌈log₂(p−1)⌉} (with (j*+1)! in the denominator).

Exact values [computed, `covering_time`]: s_3 = 3, s_5 = 65/16 = 4.0625, s_7 = 4.638,
s_11 = 5.428, s_13 = 5.726, s_17 = 6.180. Monte Carlo agrees (P.5 table).

### P.2 The algorithm

𝒜_j(d, t), for a level j, a dimension d (it uses only coordinates 1..d of the columns it
reads) and a target t ∈ F_p^d. At j = j* only t = 0 is used.

- **j = j*.** Read d+1 fresh columns and take a nonzero kernel vector of their first d
  coordinates (it exists: d+1 vectors in F_p^d). Represent each entry in
  [−(p−1)/2, (p−1)/2] ⊆ D^{(j*)}, which holds because 2^{j*−1} ≥ (p−1)/2. Return the nonzero
  entries. (At d = 0: one column with weight 1.)
- **j < j*, d = 0.** Read one fresh column and return it with weight 1.
- **j < j*, d ≥ 1.** Let π drop coordinate d.
  1. *Switches.* Repeat: run 𝒜_{j+1}(d−1, 0) on fresh columns, giving (I_k, α_k) with
     Σ_{i∈I_k} α_{k,i} π(v_i) = 0. Put β_k = Σ_i α_{k,i} v_{i,d}, x_k = ⌈α_k/2⌉ and
     x'_k = −⌊α_k/2⌋ (entrywise). Stop when the subset sums of β_1, …, β_K cover F_p.
     Record T_a ⊆ [K] with Σ_{k∈T_a} β_k = a for each a.
  2. Put c = Σ_k Σ_{i∈I_k} x'_{k,i} v_i[1..d].
  3. *Recurse.* Run 𝒜_j(d−1, π(t − c)) on fresh columns, giving (I', w').
  4. Let a = (t − c − Σ_{I'} w'_i v_i)_d. Return w' on I' and, on each block I_k, x_k if
     k ∈ T_a and x'_k otherwise. Drop zero weights.

The answer to BinSIS is 𝒜_0(n, 0).

### P.3 Proof of Theorem P

*(i) Weights.* For j ≥ 0 and α ∈ D^{(j+1)}, the entries x = ⌈α/2⌉ and x' = −⌊α/2⌋ satisfy
x − x' = α.
- If j ≥ 1, then |α| ≤ 2^j, so |x|, |x'| ≤ 2^{j−1}, and x, x' ∈ D^{(j)}.
- If j = 0, then α ∈ {−1, 0, 1}, so x, x' ∈ {0, 1}.

So every returned weight lies in D^{(j)}. The returned index sets are disjoint because every
read is fresh.

*(ii) Correctness, by induction on (j*−j, d).*
- **j = j*.** Clear.
- **j < j*, d ≥ 1.** Σ_i (x_k − x'_k)_i v_i = Σ_i α_{k,i} v_i = β_k e_d, because the π-part
  is 0. So the returned sum is Σ_{I'} w' v + c + a·e_d.
  - Its π-part is π(t−c) + π(c) = π(t).
  - Its d-th coordinate is t_d, by the choice of a.
  - It is nonempty because the recursion is nonempty; at the bottom there is a column with
    weight 1.

*(iii) Termination and the law of the β's.* 𝒜_{j+1}(d−1, ·) reads only coordinates 1..d−1 of
its columns, and it decides when to stop from those coordinates alone. So, given everything
read before block k and the π-parts of block k, the d-th coordinates of block k are still
i.i.d. uniform. Since α_k ≠ 0 mod p, β_k is uniform. Blocks are fresh runs on fresh columns
with target 0. Hence the pairs (C_k, β_k) are i.i.d., where C_k is the number of reads of
block k, and C_k is independent of β_k.

If R ≠ F_p is the current set of subset sums and β ≠ 0, then R ∪ (R+β) ⊋ R. Otherwise
R + β = R, so R would be a union of cosets of ⟨β⟩ = F_p. So the loop stops after at most
p−1 nonzero β's: a.s., and with E[K] ≤ p.

*(iv) Expected reads.* The stopping index K of the loop is a stopping time for (β_k). Also,
{K ≥ k} depends only on β_1, …, β_{k−1}, which are independent of C_k. By Wald's identity the
switches at dimension d read E[K]·E[C_1] = s_p·N_{j+1}(d−1) in expectation.

By induction, the law of the read count of 𝒜_j(d, t) does not depend on t. The switch part
does not depend on t, and the recursive call reads fresh columns. Hence

  N_j(d) = s_p N_{j+1}(d−1) + N_j(d−1),  N_j(0) = 1,

which is the stated recursion.

*(v) Closed form.* Claim: N_{j*−k}(d) ≤ (s+1)^k C(d+k+1, k+1) for s = s_p.
- **k = 0.** Equality.
- **Step.** N_{j*−k−1}(d) ≤ 1 + s(s+1)^k Σ_{e=0}^{d−1} C(e+k+1, k+1)
  = 1 + s(s+1)^k C(d+k+1, k+2). This is at most (s+1)^{k+1}[C(d+k+1, k+2) + 1]
  ≤ (s+1)^{k+1} C(d+k+2, k+2), by Pascal's rule and C(d+k+1, k+1) ≥ 1.

Now take k = j*.

*(vi) Bound on s_p.*
- **Second-moment bound.** For B draws and a ≠ 0, let X_a count the nonempty T ⊆ [B] with
  Σ_T β = a. For distinct nonempty T, T', the vectors 1_T and 1_{T'} are linearly
  independent over F_p, so the pair (Σ_T β, Σ_{T'} β) is uniform on F_p². Chebyshev gives
  Pr[X_a = 0] ≤ (p−1)/(2^B−1). A union bound over a ≠ 0 gives
  Pr[K > B] ≤ (p−1)²/(2^B−1). (This is KMOSW's Prop. 5.3 computation [cited]; it is
  re-derived here.)
- **Summing.** With B_0 = ⌈2 log₂(p−1)⌉, the terms B = B_0+i are at most 2^{1−i}. So
  s_p = Σ_B Pr[K > B] ≤ B_0 + 4.
- **The bound s_p ≤ p** is from (iii).

*(vii) Time.*
- A base call costs O(d³) for d+1 reads.
- A switch costs O(p) set updates.
- The forward sums c and the backward residuals cost O(R·d) per dimension.
- In total, O(R(n² + p)) operations. ∎

Also (s_p+1)^{j*} ≤ (2 log₂ p + 6)^{log₂ p + 1} = p^{O(log log p)}.

### P.4 The node at Γ_0 (unknown subspace, fixed arity)

**Corollary P.4 [proved].** Let d ∈ Γ_0 (so p = c+1 = d+1) and 0 < τ ≤ 1. Put
t = g_d + ⌈log_p(2/τ)⌉, L = ⌈2N_0(g_d)⌉, k = ⌈log₂(2/τ)⌉ and M = t + kL. The node
proceeds as follows.
1. Take W = span(λ_1, …, λ_t), in reduced echelon form, with a = dim W.
2. Write later labels in the pivot coordinates.
3. Run 𝒜_0(a, 0) on the coordinate vectors of block b of L labels, for b = 1, …, k, until one
   run finishes within its block.
4. Abort if a label it read is outside W, or if all k runs overrun.
5. Otherwise put s = 1_T. Check it as in (F5) and convert it as in (F6).

Then the node never returns a wrong witness. It aborts with probability ≤ τ, and its time is
poly(M, p).

*Proof.* Let a' = dim K_d^⊥ ≤ g_d. W ≠ K_d^⊥ has probability ≤ p^{a'−t}/(p−1) ≤ τ/2, by `lem:s3-moment`(d) and
`rem:fc-zero-sum-sis`(b). Outside that event, the coordinates of the later labels are i.i.d.
uniform in F_p^a (now a = a') and independent of λ_1, …, λ_t. By Markov's inequality each run overruns its
L ≥ 2N_0(a) labels with probability ≤ 1/2, since N_0 is increasing in the dimension. The runs
use disjoint blocks, so they are independent, and all k overrun with probability
≤ 2^{−k} ≤ τ/2. The witness is checked exactly, so on non-abort records the output is as in
`lem:fc-zero-sum`(d). ∎

- *Accounting.* With τ_d = ε/(9(c−1)Sn_d), the abort bound ε/9 of `lem:fc-forest`(b) is
  unchanged, as for the variant after `lem:fc-zero-sum`.
- *Arity.* M_d = O_c(g_d^{1+⌈log₂ c⌉}·log(1/τ_d)).
- *Not total.* On adversarial banks it can abort with probability 1 (Part D).

### P.5 Measurements and comparison

[computed] `exp_doubling.py` (parts A, B; `doubling_A.json`, `doubling_B.json`). R runs per row
on fresh uniform columns. Every output was checked exactly: nonempty, distinct indices,
weight 1, zero over all n coordinates. Columns: mean ± s.e. of reads, the exact expectation
N_0(n), z, and the closed-form bound.

| p | n | runs | mean reads ± s.e. | exact N_0(n) | z | closed-form bound |
|---|---|---|---|---|---|---|
| 3 | 8 | 200 | 107.2 ± 1.2 | 109.0 | -1.57 | 180 |
| 3 | 16 | 200 | 416.1 ± 3.4 | 409.0 | 2.09 | 612 |
| 3 | 32 | 200 | 1565.5 ± 8.5 | 1585.0 | -2.31 | 2244 |
| 3 | 64 | 200 | 6273.5 ± 25.6 | 6241.0 | 1.27 | 8580 |
| 3 | 96 | 200 | 14026.0 ± 47.1 | 13969.0 | 1.21 | 1.901e+04 |
| 5 | 4 | 40 | 183.5 ± 5.5 | 182.3 | 0.22 | 897 |
| 5 | 8 | 40 | 1431.8 ± 35.2 | 1419.8 | 0.34 | 4229 |
| 5 | 12 | 40 | 4794.9 ± 84.9 | 4769.9 | 0.30 | 1.166e+04 |
| 5 | 16 | 40 | 11179.2 ± 165.1 | 11288.7 | -0.66 | 2.483e+04 |
| 5 | 24 | 40 | 37813.9 ± 415.8 | 38057.5 | -0.59 | 7.496e+04 |
| 5 | 32 | 40 | 88588.1 ± 870.9 | 90176.3 | -1.82 | 1.677e+05 |
| 7 | 3 | 25 | 202.4 ± 8.8 | 179.2 | 2.62 | 6272 |
| 7 | 4 | 25 | 704.2 ± 35.2 | 647.4 | 1.61 | 1.254e+04 |
| 7 | 6 | 25 | 4030.4 ± 155.7 | 3843.0 | 1.20 | 3.763e+04 |
| 7 | 8 | 25 | 13273.0 ± 445.3 | 13210.0 | 0.14 | 8.87e+04 |
| 7 | 10 | 25 | 32539.9 ± 790.5 | 33935.9 | -1.77 | 1.794e+05 |
| 7 | 12 | 25 | 72548.1 ± 1794.1 | 72804.1 | -0.14 | 3.261e+05 |
| 7 | 14 | 25 | 140374.7 ± 2959.1 | 138194.6 | 0.74 | 5.484e+05 |
| 11 | 2 | 25 | 39.0 ± 1.3 | 41.3 | -1.84 | 3.586e+04 |
| 11 | 3 | 25 | 265.0 ± 10.6 | 265.6 | -0.06 | 9.563e+04 |
| 11 | 4 | 25 | 1748.2 ± 70.2 | 1707.7 | 0.58 | 2.152e+05 |
| 11 | 5 | 25 | 6959.2 ± 235.9 | 7132.4 | -0.73 | 4.303e+05 |
| 11 | 6 | 25 | 21856.6 ± 691.0 | 21909.7 | -0.08 | 7.89e+05 |
| 11 | 7 | 25 | 54834.2 ± 1586.0 | 54882.9 | -0.03 | 1.352e+06 |
| 11 | 8 | 25 | 113867.8 ± 2514.8 | 119236.9 | -2.13 | 2.198e+06 |
| 13 | 2 | 25 | 45.2 ± 1.7 | 45.2 | -0.04 | 4.297e+04 |
| 13 | 3 | 25 | 302.6 ± 12.2 | 304.2 | -0.14 | 1.146e+05 |
| 13 | 4 | 25 | 2043.1 ± 61.4 | 2046.2 | -0.05 | 2.578e+05 |
| 13 | 5 | 25 | 9112.4 ± 279.8 | 8682.9 | 1.54 | 5.156e+05 |
| 13 | 6 | 25 | 26661.0 ± 624.4 | 26850.5 | -0.30 | 9.453e+05 |
| 13 | 7 | 25 | 65274.4 ± 1676.9 | 67484.1 | -1.32 | 1.621e+06 |
| 13 | 8 | 25 | 151224.8 ± 2843.2 | 146892.3 | 1.52 | 2.633e+06 |
| 17 | 2 | 20 | 52.4 ± 1.8 | 51.6 | 0.44 | 5.582e+04 |
| 17 | 3 | 20 | 369.2 ± 9.9 | 370.2 | -0.10 | 1.488e+05 |
| 17 | 4 | 20 | 2540.1 ± 85.6 | 2658.0 | -1.38 | 3.349e+05 |
| 17 | 5 | 20 | 11800.0 ± 304.9 | 11527.8 | 0.89 | 6.698e+05 |
| 17 | 6 | 20 | 35050.6 ± 1057.5 | 35969.0 | -0.87 | 1.228e+06 |
| 17 | 7 | 20 | 91196.6 ± 2886.9 | 90806.6 | 0.14 | 2.105e+06 |

s_p exact vs Monte Carlo (20000 draws): p=3: 3 = 3.0000 vs 3.0037; p=5: 65/16 = 4.0625 vs 4.0479; p=7: 1127/243 = 4.6379 vs 4.6559; p=11: 10602328/1953125 = 5.4284 vs 5.4369; p=13: 4154499115/725594112 = 5.7257 vs 5.7195; p=17: 434896500819017/70368744177664 = 6.1803 vs 6.1943.

Fitted local slopes of log N_0 between n = 32 and 64 (exact recursion): 1.98 (p=3),
3.00 (p=5), 4.05 (p=7), 5.12 (p=11, 13, 17), 6.21 (p=19, 23). These approach 1+j* as n grows
(from below at p = 3, from above otherwise).

Inhomogeneous targets at levels 0 and 1 (random t, n ≤ 6): p=3 level 0: 10/10, p=5 level 0: 10/10, p=5 level 1: 10/10, p=7 level 0: 10/10, p=7 level 1: 10/10, p=11 level 0: 10/10, p=11 level 1: 10/10, p=13 level 0: 10/10, p=13 level 1: 10/10, p=17 level 0: 10/10, p=17 level 1: 10/10 exact checks passed.

Node of P.4 (`node.py`, `node.json`; random a ∈ [0, g], labels uniform on a random
a-dimensional subspace, τ = 0.05):

| p | g | τ | arity M | t | L | k | trials | aborts | Davenport g(p−1)+1 |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 6 | 0.05 | 778 | 10 | 128 | 6 | 300 | 2 | 13 |
| 3 | 12 | 0.05 | 2836 | 16 | 470 | 6 | 200 | 0 | 25 |
| 5 | 5 | 0.05 | 4226 | 8 | 703 | 6 | 200 | 0 | 21 |
| 5 | 8 | 0.05 | 17051 | 11 | 2840 | 6 | 100 | 0 | 33 |
| 7 | 4 | 0.05 | 7776 | 6 | 1295 | 6 | 100 | 0 | 25 |
| 7 | 6 | 0.05 | 46130 | 8 | 7687 | 6 | 60 | 0 | 37 |

Every non-aborting witness was checked exactly in F_p^g. Observed abort rate ≤ 2/300, against the bound τ = 0.05 (Markov is loose).

Exponent of g in the arity at Γ_0 (c = p−1) (`arity_table.py`, `arity_table.json`):

| p | c | ours 1+⌈log₂c⌉ | KMOSW avg 1+⌊(p+3)/4⌋ [cited] | KMOSW wc p−1 [cited] | Schedule 1 c⌈log₂ p⌉ |
|---|---|---|---|---|---|
| 3 | 2 | 2 | 2 | 2 | 4 |
| 5 | 4 | 3 | 3 | 4 | 12 |
| 7 | 6 | 4 | 3 | 6 | 18 |
| 11 | 10 | 5 | 4 | 10 | 40 |
| 13 | 12 | 5 | 5 | 12 | 48 |
| 17 | 16 | 5 | 6 | 16 | 80 |
| 19 | 18 | 6 | 6 | 18 | 90 |
| 23 | 22 | 6 | 7 | 22 | 110 |
| 29 | 28 | 6 | 9 | 28 | 140 |
| 31 | 30 | 6 | 9 | 30 | 150 |
| 37 | 36 | 7 | 11 | 36 | 216 |
| 41 | 40 | 7 | 12 | 40 | 240 |
| 61 | 60 | 7 | 17 | 60 | 360 |
| 127 | 126 | 8 | 33 | 126 | 882 |
| 257 | 256 | 9 | 66 | 256 | 2304 |

log₂ of the arities at selected (p, g) (node at τ = 10⁻³):

| p | g | log₂ N_0(g) | log₂ node (τ=10⁻³) | log₂ B_{p−1}(g) | log₂ KMOSW avg | log₂ KMOSW wc | Davenport | log₂ p^g (reachable-sum states) |
|---|---|---|---|---|---|---|---|---|
| 3 | 8 | 6.8 | 11.2 | 14.7 | 20.3 | 20.6 | 17 | 12.7 |
| 3 | 32 | 10.6 | 15.1 | 22.2 | 24.3 | 24.4 | 65 | 50.7 |
| 3 | 64 | 12.6 | 17.1 | 26.1 | 26.3 | 26.3 | 129 | 101.4 |
| 5 | 8 | 10.5 | 14.9 | 74.0 | 67.0 | 70.7 | 33 | 18.6 |
| 5 | 32 | 16.5 | 20.9 | 96.5 | 73.0 | 78.2 | 129 | 74.3 |
| 5 | 64 | 19.5 | 23.9 | 108.3 | 76.0 | 82.1 | 257 | 148.6 |
| 7 | 8 | 13.7 | 18.1 | 173.4 | 146.6 | 156.6 | 49 | 22.5 |
| 7 | 32 | 22.0 | 26.4 | 207.1 | 152.6 | 167.8 | 193 | 89.8 |
| 7 | 64 | 26.0 | 30.5 | 224.7 | 155.6 | 173.7 | 385 | 179.7 |
| 11 | 8 | 16.9 | 21.3 | 724.7 | 430.6 | 450.3 | 81 | 27.7 |
| 11 | 32 | 27.6 | 32.1 | 799.7 | 438.6 | 469.0 | 321 | 110.7 |
| 11 | 64 | 32.7 | 37.2 | 838.8 | 442.6 | 478.8 | 641 | 221.4 |
| 13 | 8 | 17.2 | 21.6 | 1098.6 | 640.4 | 663.4 | 97 | 29.6 |
| 13 | 32 | 27.9 | 32.4 | 1188.6 | 650.4 | 685.9 | 385 | 118.4 |
| 13 | 64 | 33.0 | 37.5 | 1235.5 | 655.4 | 697.6 | 769 | 236.8 |
| 17 | 8 | 17.6 | 22.1 | 2653.6 | 1199.3 | 1232.0 | 129 | 32.7 |
| 17 | 32 | 28.4 | 32.8 | 2803.6 | 1211.3 | 1262.0 | 513 | 130.8 |
| 17 | 64 | 33.5 | 37.9 | 2881.8 | 1217.3 | 1277.6 | 1025 | 261.6 |

(The KMOSW constants p^{p²} are "convenient uniform upper bounds" by their own statement, not optimized; compare exponents, not these numbers.)

### P.6 What Theorem P does not give

- **Not o(g²).** At p = 3 it is 1 + 3n(n+1)/2 ≈ 1.5n². That is worse than KOW's worst-case
  n²/3 [cited] and the triangular (g+1)(g+2)/2. By B2 its template cannot go below
  Ω(n²/log n).
- **Not FPT.** The exponent is 1+⌈log₂(p−1)⌉. B5 explains the log₂ p levels.
- **Paper regime** (`rem:fc-zero-sum-sis`(d)): p = c+1 = O(log m). There the node costs
  g^{O(log log m)}·(log m)^{O(log log log m)}, which is polynomial iff log g·log p = O(log m).
  This is a strictly larger window than the reachable-sum node (g·log p = O(log m)). It is
  still not polynomial for all profiles: for example g = m^{1/2} with p ≈ log m gives
  m^{Θ(log log m)}.
- **Not worst case.**

### P.7 Novelty

KMOSW Thm 1.10 (arXiv 2609.40321, §5) [cited] uses the same affine-reducibility step once.
It builds binary solutions from switches given by a *worst-case* signed solver (KOW Thm 5.2,
exponent ⌊(q+3)/4⌋). Theorem P applies the step at every weight level. The level-(j+1)
solver is itself average case, since Prop. 5.3 feeds it only the W-parts, which are i.i.d.
uniform. This turns the multiplicative cost of a level into one extra power of n.

I did not find this in KOW26, KMOSW26, II24, IS17 or GKSZ (local texts). The split
x = ⌈α/2⌉, x' = −⌊α/2⌋ is the halving idea of KOW §3 (their Lemma 3.3 style), applied here
through average-case switches. KOW §5.1 asks whether their *worst-case* SIS∞ bound n^k
(Thm 4.11, weight bound ⌊q/2k⌋) can be improved to n^{o(k)}. The level-j solvers of
Theorem P give, in the *average case only*, weight bound 2^{j−1} with exponent
j* − j + 1 ≈ 1 + log₂ k, where k ≈ q/2^j. That is an average-case
analogue, n^{O(log k)}, not an answer to their question. **NEEDS HUMAN VERIFICATION** (literature after
Sept 2026, Chen–Liu–Zhandry, IPS18 were not read).

Combining with KOW Thm 5.2 at the signed level [cited] gives exponent
1 + min(⌈log₂(p−1)⌉, ⌊(p+3)/4⌋).

## B. Barriers

### B1. Linear-sketch disjoint merging (BKW, disjoint-matching generalized birthday) [proved]

**Model (LSDM).** The columns v_1, …, v_M are i.i.d. uniform in F_p^n. Stage j = 1, …, ℓ:
- **Sketch.** Given what it has read, the algorithm picks a linear map φ_j : F_p^n → F_p^{b_j},
  b_j ≥ 1, such that Φ_j = (φ_1, …, φ_j) has rank Σ_{i≤j} b_i.
- **Read.** It reads φ_j(v_k) for all k.
- **Merge.** From the family F_{j−1} of pairwise disjoint nonempty "items" (F_0 = singletons)
  it forms F_j. Each member of F_j is a union of one or more members of F_{j−1}, with
  pairwise disjoint members, and its φ_j-sum is 0.

The run succeeds if Φ_ℓ is injective and F_ℓ ≠ ∅; every member of F_ℓ is then a zero-sum.
Computation is unbounded. The model contains:
- BKW (coordinate blocks, pairs);
- disjoint-matching variants of Wagner's k-tree (pairs, one block per level, each element
  used in at most one match). Wagner's k-tree proper keeps all matching pairs and reuses
  elements, so it is not an LSDM;
- any generalized-birthday merge with {0,1} weights;
- the coordinate-block recursion of the 11-04 report (Z6), with groups of b_j(p−1)+1 items.

**Lemma B1.1.** Let G_{j−1} be everything read before stage j. Given G_{j−1}, the sums
σ_I = Σ_{k∈I} φ_j(v_k), I ∈ F_{j−1}, are i.i.d. uniform on F_p^{b_j}.

*Proof.* Given G_{j−1}, φ_j is fixed. v_k is uniform on the coset Φ_{j−1}^{−1}(Φ_{j−1}(v_k)),
independently over k. By the rank condition φ_j maps ker Φ_{j−1} onto F_p^{b_j}, so the
φ_j(v_k) are i.i.d. uniform. The items are disjoint, nonempty and G_{j−1}-measurable. ∎

**Theorem B1.** Put γ = 2p/(p+1).
- **(i) Depth.** E[|F_j| | G_{j−1}] ≤ |F_{j−1}|(1+p^{−b_j})/2 ≤ |F_{j−1}|/γ. Hence
  Pr[success ∧ ℓ ≥ L] ≤ M γ^{−L} for every L.
- **(ii) Fan-in.** If every member of F_j is a union of at most F members of F_{j−1}, then
  Pr[F_j ≠ ∅ ∧ b_j ≥ b] ≤ (M+1)^F p^{−b}.
- **(iii) Arity.** So an algorithm succeeding with probability ≥ δ has, for every integer
  b ≥ 2, δ ≤ n(M+1)^F p^{−b} + M γ^{−⌈n/(b−1)⌉}. In particular
  F ln(M+1)·ln(2M/δ) + ln(2n/δ)·ln(2M/δ) ≥ n·ln p·ln γ, so for fixed F and δ,
  M ≥ exp(Ω(√(n ln p ln γ / F))).
- **(iv) Unbounded fan-in.** With probability ≥ δ/2, success occurs with
  ℓ < log_γ(2M/δ). Then some stage has b_j > n ln γ / ln(2M/δ). Given G_{j−1}, that stage
  receives |F_{j−1}| ≤ M i.i.d. uniform items in F_p^{b_j}, and it must output a nonempty
  disjoint zero-sum union: average-case BinSIS(b_j, ≤ M, p).

*Proof.*
- **(i)** Let Z be the number of I ∈ F_{j−1} with σ_I = 0. A member of F_j is either one such
  item or uses at least two items. So |F_j| ≤ Z + (|F_{j−1}| − Z)/2 = (|F_{j−1}| + Z)/2, and
  E[Z | G_{j−1}] = |F_{j−1}| p^{−b_j} by Lemma B1.1. So X_j = γ^j |F_j| is a nonnegative
  supermartingale with X_0 = M. Since ℓ ≤ n, optional stopping gives E[X_ℓ] ≤ M. On
  {success, ℓ ≥ L}, X_ℓ ≥ γ^L.
- **(ii)** A member of F_j is a nonempty union of t ≤ F distinct items. Its sum is uniform
  given G_{j−1}, so it is 0 with probability p^{−b_j}. There are at most (M+1)^F such
  unions. Markov on the conditional expectation gives the bound, uniformly in the adaptive
  b_j.
- **(iii)** Success means either some b_j ≥ b (bound (ii), with a union over ≤ n stages) or
  all b_j ≤ b−1, in which case ℓ ≥ ⌈n/(b−1)⌉ (bound (i)). Choose
  b = ⌈(F ln(M+1) + ln(2n/δ))/ln p⌉.
- **(iv)** From (i), with L = log_γ(2M/δ), and from Σ b_j = n. ∎

*Reading.* At fixed p and poly(g) arity, disjoint merge-tree methods either have fan-in
growing with n, or are superpolynomial in arity, whatever their running time. With poly
arity and unbounded fan-in they face, at some stage, a BinSIS instance of dimension
Ω(n/log n) (a reading of (iv), not a formal reduction). Disjoint-matching k-trees with lists
of size poly(g) are the case F = 2.

What escapes the model: items with several values. These are the switches of Theorem P: a
block with two admissible weightings x, x'. Theorem P is not an LSDM, and it is polynomial.

### B2. Flag-switch recursion needs Ω(n²/log n) columns [proved]

**Model (FSR).** This is KMOSW Def. 5.4 [cited], generalized; Theorem P at level 0 is an
instance. Along a coordinate flag, for d = n, …, 1:
- **Switches.** The algorithm draws fresh columns and builds switches: pairs of binary
  vectors x_k, x'_k on pairwise disjoint fresh index sets I_k, with
  Σ (x_k − x'_k)_i π_{d−1}(v_i) = 0.
- **Choices.** It may use any rule to find switches (sparse, adaptive, exponential time). It
  may use any adaptive number of them. It may read coordinate d of the switch columns.
- **Base and backward pass.** At dimension 0 it reads one fresh column with weight 1. Then it
  goes back up. At dimension d it chooses x_k or x'_k in each switch to hit the residual
  a_d = (t_d − c_d − s)_d, where c_d is the default (all x') sum and s is the sum of what was
  chosen below.
- **Reading restriction (part of the model).** All switches at all dimensions are fixed
  before the backward pass starts. Every action taken at dimension d, forward or backward,
  is a function of coordinates ≤ d of the columns only (and of earlier actions). The flag
  may be fixed in advance, or chosen from earlier columns that are independent of the
  ones used afterwards, as KMOSW do with their basis. Theorem P and KMOSW Def. 5.4 satisfy
  this restriction. Without it, a backward choice at d'' < d could read coordinate d and
  steer a_d, and the proof below fails.

**Theorem B2.** Put μ_p = log₂ p − ⌊log₂ p⌋ > 0 and k_0 = ⌊log₂(4/δ)/μ_p⌋. If an FSR algorithm
reads at most M columns and succeeds with probability ≥ δ, then, with L = n − k_0,

  M ln(2M) ≥ ⌈log₂ p⌉·[ ln p·L(L−1)/2 − L·ln(4n/δ) ].

So M = Ω_p(n²/log n) for fixed δ.

*Proof.*
- **(a) The residual is uniform.** Coordinate d of every column drawn below dimension d is
  unread when a_d is formed. The forward pass at d' < d reads coordinates ≤ d', and the
  backward pass at d'' < d reads coordinates ≤ d''. The chosen set below d is nonempty (the
  base column) and has weights 1. So, given all switches at d (hence their β's and the
  number B'_d of switches with α_k = x_k − x'_k ≠ 0) and everything below, a_d is uniform.
  Hence Pr[a_d is a subset sum of the β's | ·] ≤ 2^{B'_d}/p.
- **(b) Few switches are unlikely.** Π_d min(1, 2^{B'_d}/p)^{−1}·1[success up to d] is a
  nonnegative supermartingale in the order a_1, a_2, …. So Pr[success ∧
  Σ_d (log₂ p − B'_d)^+ ≥ x] ≤ 2^{−x}. Take x = log₂(4/δ). A dimension with
  B'_d < ⌈log₂ p⌉ contributes at least μ_p, so on the complement at most k_0 dimensions have
  B'_d < ⌈log₂ p⌉.
- **(c) Switches are not sparse.** A switch at d with α_k ≠ 0 is a nonzero {0,±1} relation
  on the first d−1 coordinates of at most |I_k| of the M columns. For a fixed support and
  sign pattern the probability is p^{−(d−1)}. Put
  s_d = ⌊((d−1) ln p − ln(4n/δ))/ln(2M)⌋. The expected number of such relations with
  support ≤ s_d, at any d, is ≤ Σ_d 2(2M)^{s_d} p^{−(d−1)} ≤ δ/2.
- **(d) Counting.** So with probability ≥ δ/4 the run succeeds and every useful switch at d
  has ≥ s_d+1 columns. All but k_0 dimensions have ≥ ⌈log₂ p⌉ useful switches. The blocks
  are disjoint, so M ≥ ⌈log₂ p⌉ Σ_{d=1}^{n−k_0} (s_d+1). Sum
  (s_d+1) ≥ ((d−1) ln p − ln(4n/δ))/ln(2M). ∎

*Reading.*
- **No n^{2−ε}.** The affine-reducibility template of KMOSW Thm 1.10 and of Theorem P cannot
  give n^{2−ε} for any p, even with an oracle for the switches.
- **The n²/log n gap.** The gap between Ω(n²/log n) and the Θ(n²) achieved comes only from
  sparse switches. These are low-weight codewords of a random code, and finding them at
  support o(d) is an ISD problem; I know of no polynomial method (an assessment, not a
  theorem).
- **Larger steps (heuristic, not proved).** Steps that quotient t > 1 coordinates at once
  must cover F_p^t. That is BinSIS(t) on the β's, so large steps only move the problem.
  With steps t_k, the analogous counting would involve Σ_k t_k(d_k − t_k) = (n² − Σ t_k²)/2.
  The identity itself is exact; the lower bound for this variant is not proved here.

### B3. Oblivious information sets [proved]

Fix positions P (|P| = n) and condition on X_P invertible. Then A = X_P^{−1}X_F is uniform
and independent of X_P. Suppose an algorithm tries T nonzero free patterns x_F ∈ {0,1}^F,
chosen from X_P and coins only, and not adapted to the outcomes of earlier trials, and outputs x_P = −A x_F when x_P is binary. Each trial
succeeds with probability exactly (2/p)^n, so Pr[success] ≤ T(2/p)^n. This is the Γ_0
analogue of `prop:rc-lower` (there q = 2/p).

### B4. Zero-sum theorems and lattices [proved / cited]

- **Existence thresholds [proved].** Average-case existence starts at M ≈ n log₂ p.
  - If 2^M ≤ τ p^n, then Pr[∃ zero-sum] ≤ (2^M−1)/p^n < τ, by the first moment.
  - If M ≥ 1 + log₂(p^n/τ), then Pr[∃ zero-sum] ≥ 1−τ (`lem:fc-zero-sum`(a)).
  - The Davenport constant g(p−1)+1 is the worst-case threshold. It is attained by
    structured banks, such as each e_i repeated p−1 times. Those are not typical.
- **Totality only [cited, GKSZ Theorem 10(1) in the local text (§6), Open Problem 5].** The existence proofs
  (Chevalley–Warning, Olson's group-ring argument, EGZ) put BIS_p in PPA_p via Chevalley_p.
  Whether BIS_p is PPA_p-hard is open. These theorems supply totality at linear arity, not a
  search algorithm. No known reduction moves worst-case hardness to the average case at
  constant p (11-04 report Z3; KOW footnote 7) [cited].
- **Lattices [proved].** Λ^⊥ = {z : Xz ≡ 0} contains p·e_i, of ℓ₂ norm p. A binary solution
  of support k has norm √k. By the first moment, Pr[some zero-sum has support ≤ k] ≤
  Σ_{i≤k} C(M,i) p^{−n} ≤ (eM/k)^k p^{−n} (for k ≤ M/2, say), so w.h.p. every zero-sum has
  support k with (eM/k)^k ≳ p^n. So for fixed p and M = poly(n), every binary solution is longer
  than p·e_1, and ℓ₂-SVP/approx-SVP methods do not target binary solutions. (Z2's lattice
  obstruction needs p ≥ g^{1+2δ}, 11-04.)

### B5. Doubling depth [proved]

Let D^{(0)} = {0,1} and D^{(j+1)} ⊆ D^{(j)} − D^{(j)} in F_p. Then D^{(1)} ⊆ {0,±1}, and by
induction D^{(j)} lies in the image of [−2^{j−1}, 2^{j−1}] for j ≥ 1, which has at most 2^j+1
residues. So D^{(J)} = F_p, which a
linear-algebra base needs, forces 2^J+1 ≥ p, that is J ≥ ⌈log₂(p−1)⌉ = j*.

Any switch hierarchy whose level-(j+1) relations are split as x − x' with x, x' ∈ D^{(j)}
therefore has depth ≥ j*. Each FSR level would cost at least a factor ⌈log₂ p⌉·Ω(d/log M) by an analogue of B2 at higher weight levels; that analogue is not proved here.
So **[conjecture]** such hierarchies are n^{Θ(log p)}. An FPT method must use non-switch
structure or a base other than linear algebra.

## C. Merge-tree computations [computed]

`merge_barrier.py` → `merge_barrier.json`.

Real columns, pair-merge BKW (outputs checked exactly):

| p | n | M | blocks | successes |
|---|---|---|---|---|
| 3 | 8 | 400 | [2, 2, 2, 2] | 40/40 |
| 3 | 12 | 3000 | [3, 3, 3, 3] | 40/40 |
| 5 | 6 | 2000 | [2, 2, 2] | 40/40 |
| 7 | 6 | 4000 | [2, 2, 2] | 40/40 |

Per-stage survival ratio |F_j|/|F_{j−1}| for N = 20000 items, mean of 50 runs, against the bound (1+p^{−b})/2 of Theorem B1(i):

| p | b | measured | bound |
|---|---|---|---|
| 3 | 1 | 0.6652 | 0.6667 |
| 3 | 2 | 0.5499 | 0.5556 |
| 3 | 3 | 0.5085 | 0.5185 |
| 5 | 1 | 0.5962 | 0.6000 |
| 5 | 2 | 0.5105 | 0.5200 |
| 5 | 3 | 0.4819 | 0.5040 |
| 7 | 1 | 0.5665 | 0.5714 |
| 7 | 2 | 0.4962 | 0.5102 |
| 7 | 3 | 0.4643 | 0.5015 |

Least arity M at which pair-merge BKW (best uniform block size; M on a 2^{1/4} grid; 60 abstract runs per point, justified by Lemma B1.1) succeeds with frequency ≥ 1/2, against the average-case existence scale n log₂ p:

| p | n | least M | block b | n log₂ p |
|---|---|---|---|---|
| 3 | 6 | 21 | 2 | 9.5 |
| 3 | 9 | 73 | 2 | 14.3 |
| 3 | 12 | 185 | 3 | 19.0 |
| 3 | 16 | 453 | 3 | 25.4 |
| 3 | 20 | 1088 | 4 | 31.7 |
| 3 | 25 | 2599 | 4 | 39.6 |
| 3 | 30 | 6194 | 5 | 47.5 |
| 3 | 36 | 14741 | 5 | 57.1 |
| 5 | 4 | 21 | 1 | 9.3 |
| 5 | 6 | 73 | 2 | 13.9 |
| 5 | 9 | 222 | 2 | 20.9 |
| 5 | 12 | 644 | 3 | 27.9 |
| 5 | 16 | 2184 | 3 | 37.2 |
| 5 | 20 | 5207 | 3 | 46.4 |
| 7 | 4 | 40 | 1 | 11.2 |
| 7 | 6 | 106 | 2 | 16.8 |
| 7 | 9 | 453 | 2 | 25.3 |
| 7 | 12 | 1295 | 2 | 33.7 |
| 7 | 16 | 4377 | 3 | 44.9 |

Reading. At p = 3, ln(least M)/√n rises from 1.24 (n = 6) to 1.60 (n = 36). This is consistent with superpolynomial growth, but finite data prove nothing. The closed-form lower bound of Theorem B1(iii) is vacuous at these sizes (it gives M ≥ 2). It is an asymptotic statement, and the table does not test it. Minimizing the arity of the Davenport block recursion alone gives the single block (arity n(p−1)+1, time p^n). Its arity/time trade-off is the Z6 item of the 11-04 report and is not repeated here.

## D. Strongest counterexamples and limits

- **Theorem P is average case only.** Take any bank in which coordinate d equals coordinate 1
  for all columns, with d ≥ 2. Every relation α on coordinates 1..d−1 gives β = 0, so the
  covering loop never ends, and the fixed-arity node aborts with probability 1. In the node,
  coordinates are relative to the echelon basis of the span, so a degenerate span is not a
  counterexample. Correlated coordinates inside the span are. The paper's banks are i.i.d.
  uniform (`lem:fc-forest`(a)), so this is outside the node's contract, as for every
  non-total node.
- **B2 does not cover KOW.** KOW's worst-case n²/3 and KMOSW's 0.1022n² [cited, the latter
  not proved in KMOSW] are below what FSR with non-sparse switches achieves (≈1.5n² for
  Theorem P at p = 3). They reuse columns across dependencies, so they are not FSR, and B2
  says nothing about them. o(n²) for such schemes is exactly the KOW/KMOSW open question.
- **B1 lists only {0,1}-merges.** Merges that subtract items, or let items overlap, leave
  {0,1}. They solve signed or larger-weight problems, which are not the node's problem.

## E. Gates and next step

- Gates that must stay false: all Rees gates; no o(g²); no FPT; no worst-case claim.
- **Next hard question.** Average-case signed SIS∞ (β = 1) mod p at f(p)·n^{C} columns, with C
  absolute. By Theorem P's step (one level) that would make BIS_p FPT with exponent C+1.
  Equivalently, find structure other than switches (B1, B2, B5 close the natural ones).
- **Next command:**
  `cd research/audits/reviews/2026-11-05-rees-s3-arity && nice -n 10 /opt/anaconda3/bin/python exp_doubling.py A doubling_A.json`.
  It is expected to reproduce `doubling_A.json` with |z| ≤ 3 on every row. The acceptance
  test is the human check of P.3 (iii)–(iv) (independence of β_k from C_k and Wald) and of
  P.7 novelty.

## F. Proposed text (LaTeX; after `rem:fc-zero-sum-sis`; AI-checked, pending human review)

Also saved as `2026-11-05-rees-s3-arity/proposed_remark.tex`.

```latex
\begin{remark}[Arity at the zero-sum grade; AI-checked, pending human review]
\label{rem:fc-zero-sum-arity}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-s3-arity.md}, with code in its folder), checked by a second, adversarial AI pass recorded in the same report; no human has checked it, nothing else in the paper uses it, and (R1) is unchanged. Keep the notation of Remark~\ref{rem:fc-zero-sum-sis}. Every statement concerns banks whose labels are independent and uniform on $K_d^\perp$, as in Lemma~\ref{lem:fc-forest}(a), and binary weights, since $s^d \in \{0,1\}$ at $d = p-1$.

\textup{(a)} \emph{A node of polynomial arity with degree $1+\lceil\log_2c\rceil$.} Put $j^* = \lceil\log_2(p-1)\rceil$, $D^{(0)} = \{0,1\}$ and $D^{(j)} = \{-2^{j-1},\dots,2^{j-1}\}$ for $j \ge 1$, read modulo $p$. Then $D^{(j^*)}$ contains every residue, and every $\alpha \in D^{(j+1)}$ equals $x - x'$ with $x = \lceil\alpha/2\rceil$ and $x' = -\lfloor\alpha/2\rfloor$ in $D^{(j)}$. A \emph{level-$j$ solver} in dimension $n$ with target $t \in \Fp^n$ reads independent uniform columns $v_i \in \Fp^n$ one at a time and returns a nonzero weight vector with entries in $D^{(j)}$ on the columns it read, with weighted sum $t$. For $j = j^*$ (used with $t = 0$ only) it returns a kernel vector of $n+1$ columns. For $n = 0$ it returns one column with weight $1$. For $j < j^*$ and $n \ge 1$ it repeats the following until the subset sums of $\beta_1,\dots,\beta_K$ cover $\Fp$: run the level-$(j+1)$ solver with target $0$ on the first $n-1$ coordinates of fresh columns, obtaining $\alpha_k$, and put $\beta_k = \sum_i\alpha_{k,i}v_{i,n}$. It then calls itself in dimension $n-1$, on fresh columns, with target the first $n-1$ coordinates of $t - c$, where $c = \sum_k\sum_i x'_{k,i}v_i$. Finally, on a set of indices $k$ whose $\beta_k$ sum to the remaining last coordinate, it uses $x_k$ in place of $x'_k$. The inner solver reads only the first $n-1$ coordinates of its columns, so given everything else each $\beta_k$ is uniform. Hence the solver halts with probability~$1$, its output is checked exactly, and by Wald's identity its expected number of columns satisfies $N_{j^*}(n) = n+1$ and $N_j(n) = 1 + s_p\sum_{e<n}N_{j+1}(e)$. Here $s_p \le \min(p,\lceil2\log_2(p-1)\rceil+4)$ is the expected number of uniform elements of $\Fp$ drawn until their subset sums cover $\Fp$. So $N_0(n) \le (s_p+1)^{j^*}\binom{n+j^*+1}{j^*+1}$, and the time is $O(R(n^2+p))$ operations in $\Fp$ when $R$ columns are read.

A node at $d \in \Gamma_0$ spans $W$ by its first $g_d + \lceil\log_p(2/\tau)\rceil$ labels and writes later labels in an echelon basis of $W$. It then runs the level-$0$ solver on up to $\lceil\log_2(2/\tau)\rceil$ disjoint blocks of $\lceil2N_0(g_d)\rceil$ labels. It checks as in (F5) and converts as in (F6). By Lemma~\ref{lem:s3-moment}(d) and Markov's inequality it aborts with probability at most $\tau$. With $\tau = \tau_d$ as in the variant after Lemma~\ref{lem:fc-zero-sum}, the bound $\eps/9$ of Lemma~\ref{lem:fc-forest}(b) is unchanged. Since $c = p-1$, the arity is $O_c(g_d^{\,1+\lceil\log_2c\rceil}\log(1/\tau_d))$. For comparison, $B_c(g_d)$ has degree $c\lceil\log_2(c+1)\rceil$; for example, the degrees are $3$ and $12$ at $c = 4$. For $p \ge 5$, the same step applied once, on top of a worst-case signed solver, is~\cite[Theorem~1.10]{KothariMetgerODonnellShuttyWu2026}, of degree $1+\lfloor(c+4)/4\rfloor$ with a factor $p^{p^2}$ and failure probability $2^{-\Omega(g_d)}$. At constant $\tau$ the degree here is smaller for $p = c+1 = 17$ and every prime $p \ge 23$, equal for $p \in \{3,5,13,19\}$, and larger for $p \in \{7,11\}$. At $\tau = 2^{-g_d}$ the factor $\log(1/\tau)$ adds one to the degree, which is then smaller only for primes $p \ge 29$.

The node is not total: if one coordinate of every label in the echelon basis repeats another, every $\beta_k$ vanishes and the node aborts. It gives neither arity $o(g_d^2)$ (at $p = 3$ it uses about $1.5g_d^2$ labels) nor time and arity $f(p)\poly(g_d)$. In the regime $p = O(\log m)$ of Remark~\ref{rem:fc-zero-sum-sis}(d) it is polynomial when $\log g_d\cdot\log p = O(\log m)$. That range is wider than the range $g_d\log p = O(\log m)$ of Lemma~\ref{lem:fc-zero-sum}(c), but it does not cover every profile.

\textup{(b)} \emph{Why the natural routes to arity $o(g_d^2)$ fail.} Write $n = a_d$, $\gamma = 2p/(p+1)$, and let $\delta$ be the success probability. These statements hold whatever the running time.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item \emph{Merging.} Consider an algorithm that works in stages $j = 1,\dots,\ell$. In stage $j$ it chooses, from what it has read, a linear map $\varphi_j$ that raises the rank of $(\varphi_1,\dots,\varphi_j)$ by $b_j \ge 1$, and it reads $\varphi_j$ of every label. It then replaces its family of pairwise disjoint sets of labels (initially the singletons) by pairwise disjoint unions of members whose $\varphi_j$-sum vanishes. BKW-type merging and disjoint-matching variants of Wagner's merging with binary weights, and the block recursion with Davenport groups, are of this form. Wagner's $k$-tree itself reuses elements across matches and is not. Given the past, the $\varphi_j$-sums of the members are independent and uniform. So the expected number of members drops by a factor of at least $\gamma$ per stage, and success with at least $L$ stages has probability at most $M\gamma^{-L}$. If every union has at most $F$ members, a stage with $b_j \ge b$ is nonempty with probability at most $(M+1)^Fp^{-b}$. Hence $(F\ln(M+1)+\ln(2n/\delta))\ln(2M/\delta) \ge n\ln p\ln\gamma$, that is, $M \ge \exp(\Omega(\sqrt{n\ln p\ln\gamma/F}))$. With unbounded $F$ and polynomial $M$, some stage must solve the same average-case problem in dimension at least $n\ln\gamma/\ln(2M/\delta)$.
  \item \emph{Switch recursion.} Consider schemes of the form of~(a) at level $0$, along a coordinate flag, with switches found by any rule, including sparse or exponential-time rules. All switches are fixed before the backward pass, and every action at dimension $d$ depends only on coordinates at most $d$ of the labels. Given the switches, each residual coordinate is uniform. A nonzero $\{0,\pm1\}$ relation on at most $((d-1)\ln p - \ln(4n/\delta))/\ln(2M)$ of $M$ uniform vectors of $\Fp^{d-1}$ exists with small probability. Hence such a scheme that reads $M$ labels satisfies $M\ln(2M) \ge \lceil\log_2p\rceil\,(\ln p\,L(L-1)/2 - L\ln(4n/\delta))$, where $L = n - \lfloor\log_2(4/\delta)/(\log_2p-\lfloor\log_2p\rfloor)\rfloor$. So $M = \Omega_p(n^2/\log n)$.
  \item \emph{Oblivious information sets.} Fix an information set and try $T$ binary patterns on its free labels, chosen without reading the free labels and not adapted to earlier trials. This succeeds with probability at most $T(2/p)^n$, the analogue of Proposition~\ref{prop:rc-lower}.
  \item \emph{Zero-sum theorems.} The Davenport bound of Lemma~\ref{lem:fc-zero-sum}(b) and its Chevalley--Warning proof give totality and membership in $\mathrm{PPA}_p$~\cite{GoosKamathSotirakiZampetakis2020}, but no search procedure. In the average case a zero-sum exists already at about $n\log_2p$ labels.
\end{enumerate}
None of this excludes reusing labels across dependencies as in~\cite{KothariODonnellWu2026}, which reaches about $a^2/3$ labels at $p = 3$. Whether average-case $\mathrm{BinSIS}$ at fixed $p$ is solvable in polynomial time at arity $o(a_d^2)$, or in time and arity $f(p)\poly(a_d)$, remains open.
% NEEDS HUMAN VERIFICATION: Theorem 1.10 of KothariMetgerODonnellShuttyWu2026 (arXiv 2609.40321) and its exponent 1+floor((q+3)/4); novelty of (a); no bib entries exist for Blum--Kalai--Wasserman or Wagner, so none are cited.
\end{remark}
```

## G. Independent adversarial check

Fresh general-purpose subagent (agent a558169fd3cfe9464), briefed with the report and code
paths only. It was asked to find errors in Theorem P, Cor. P.4, B1–B5, the side finding, the
LaTeX and the code. It re-derived every proof and spot-ran the code: s_3, s_5, s_7 exact;
N_0 at p = 3 equals 1+3n(n+1)/2; fresh runs at (5,6), (7,4), (3,20) gave z = −0.65, 1.33,
−1.53, with every output checked.

**Verdict:** no fatal errors.
- Theorem P: TRUE WITH FIXES (wording).
- Cor. P.4: TRUE.
- B1: TRUE WITH FIXES (one substantive scope error).
- B2: TRUE WITH FIXES (one substantive model gap).
- B3, B4, B5: TRUE (wording).
- Side finding: critique RIGHT, consequence misstated.
- Proposed remark: TRUE WITH FIXES.
- Code: TRUE.

**Fixes applied (all in this report and in `proposed_remark.tex`):**
1. "always halts / always succeeds" became "halts with probability 1". A stream whose β's
   are all 0 exists, with probability 0.
2. "|z| ≤ 2.3" became "max |z| = 2.62". The slopes approach 1+j* from below at p = 3.
3. The KMOSW comparison is now qualified by failure probability (substantive). KMOSW get
   2^{−Ω(n)} at fixed m, while the node pays log(1/τ). At τ = 2^{−n} our exponent rises by 1
   and is smaller only for p ≥ 29 (summary item 2 and remark (a)). The remark also says
   that for p = 3, KMOSW Thm 1.10 is KOW Thm 1.2, not the switch step.
4. B1 (substantive): Wagner's k-tree proper reuses elements across matches and is not an
   LSDM. B1 now claims only disjoint-matching variants, and cites Wagner's own
   2^{O(n/log(m/n))} separately. (iv) is labelled a reading, not a reduction.
5. B2 (substantive): the reading restriction is now part of the model. All switches are
   fixed before the backward pass, and every action at dimension d uses only coordinates
   ≤ d. A data-chosen flag from independent earlier columns is allowed. The "larger steps"
   lower bound is labelled heuristic.
6. Smaller wording fixes:
   - P.4 separates a' = dim K_d^⊥ from dim W.
   - P.7 says that KOW's n^{o(k)} question is worst case, and that Theorem P gives only an
     average-case analogue.
   - B3 trials are non-adaptive.
   - B4 uses the first-moment inequality.
   - B5's higher-level cost is an unproved analogue of B2.
   - The GKSZ result is "Theorem 10" in the local text.
7. Side finding: the example is now u_i = e for every i, since all-zero inputs are
   trivial. The consequence is corrected. If the sketch held, KMOSW 1.10 would give a
   randomized worst-case bound n^{2+2⌊(q+3)/4⌋}, beating their Thm 1.11 for q ≥ 11. The
   earlier claim "KOW pose as open" was outdated.

Not changed: the referee's note that subset bookkeeping T+(k,) costs O(K) per insert. That
affects the implementation only; the proved time bound uses O(1)-per-insert bookkeeping (a
parent pointer per reachable value).
