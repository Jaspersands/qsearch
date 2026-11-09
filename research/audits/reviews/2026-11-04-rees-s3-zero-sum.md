# Rees Schedule 3: the zero-sum grade κ = p−1 and the i.i.d. supply (2026-11-04)

**Status: COMPLETE (2026-11-04). AI-checked, pending human review. No paper file edited; no
registry or JSON artifact edited; nothing committed.**

Owner items: `REES_FULL_CONTINUATION.md`, "What full still lacks", item 4, sentence
"Still open: a polynomial-time sampler, and a polynomial-time finder at the zero-sum grade
κ = p−1 for general profiles."  Problem (b) is the second half, problem (a) the first.

Labels: **[proved]** a complete argument here, or one cited by label from the paper;
**[exact]** a finite integer computation in `2026-11-04-rees-s3-zero-sum/`; **[conjecture]**
not proved. **[cited]** marks an outside theorem. Each one was read from the local full texts in
`2026-11-02-rees-linear-arity/lit/`. Every [cited] item NEEDS HUMAN VERIFICATION of its
numbering and hypotheses.

## Summary

**Prior work in this repo (read first; not repeated as new).** The paper already says that at
κ = p−1 the node's search problem is BIS_p of Göös–Kamath–Sotiraki–Zampetakis (main.tex, the
paragraph after `prop:triangular-sde`). `appendix-schedule2.tex` (Scope list) already says
p ∈ E_2(p−1) for p ≥ 5. Proposition D of `2026-11-02-rees-linear-arity.md` §6 already proves
the GPV form of the hardness consequence: p ≥ ω(a² log a) at the Chevalley–Warning arity.

**(b): what is new here.**
1. **Z1 [proved].** An exact two-way equivalence between the zero-sum node on i.i.d. banks and
   average-case binary SIS. The bank is uniform on an *unknown* subspace, so this needs the
   split-bank reduction. The equivalence also realizes hard banks inside actual Rees
   instances, including the node's post-measurement registers.
2. **Z2 [proved, conditional on MP13 Thm 1.1 [cited]].** A sharper obstruction: no
   polynomial-time node of arity ≤ p²·g^{−2δ} on primes p = Θ(g^k), k > 1. In particular the
   exponent of g in the arity of every polynomial-time node must grow with p.
3. **Z3 [proved].** A scope fact. In every regime where Z2 applies, Schedule 3 already costs
   at least 2^{c−1} queries. In the only regime where a polynomial Schedule 3 is possible,
   p = O(log m), Z2 is silent. There the open question is whether average-case BIS_p is FPT
   in p, meaning time and arity f(p)·poly(g).
4. **Z4 [cited].** For fixed p, polynomial-time nodes exist, so the answer to "polynomial in
   g alone for fixed p" is yes. KMOSW Thm 1.11 (worst case, p^{p²}(g+1)^{p−1} columns) and
   Thm 1.10 (average case, p^{p²} g^{1+⌊(p+3)/4⌋}) improve the exponent of Schedule 1 at Γ_0,
   which is (p−1)⌈log₂ p⌉. Linear arity O(g) is open for every fixed p ≥ 3.

**(a).** The i.i.d. supply is not an outside sampler. The algorithm produces it exactly, in
polynomial time (A2 [proved]). The law is exactly the Born law of central Fourier sampling.
Weak Fourier sampling over G_d and measured oracle values give the same law and the same
conversion outputs (A3 [proved]). The coset-copy extension of `thm:free-coordinate`(iii),
which the paper calls "argued, not proved", follows from the proof as written (A4 [proved]).
The open item called "polynomial-time sampler" in the source notes is the *witness* sampler at
FCS grades. At h = (p−1)/κ_d = 2 it is exactly average-case ternary SIS, with the same
obstruction (A5 [proved]+[cited]). For h ≥ 3 the hardness question is open (A5 [conjecture]).

**Left open.** A node at Γ_0 with arity o(g²) (any p), or time and arity f(p)·poly(g).
Hardness for fixed p, or for p ≤ g^{1/2}. A witness sampler at FCS grades with h ≥ 3 below
κ^a trials. Human review of everything here.

## Part 1. Problem statements

### 1.1 Problem (b): the zero-sum node

Setting: `app:fc-mixed`, d ∈ Γ_0. Then d = p−1 = κ_d = c, so p = c+1 ≥ 3. For s ∈ F_p we
have s^{p−1} ∈ {0,1}, equal to 1 exactly when s ≠ 0.

**Problem ZS(p, g; M, τ).** Public data: p, g = g_c and an arity M fixed before measuring.
Input: a bank λ_1,…,λ_M, i.i.d. uniform on an unknown subspace V = K_c^⊥ ≤ F_p^g of unknown
dimension a ≤ g (`lem:s3-law`, `lem:fc-forest`(a)). Output: a nonempty T ⊆ [M] with
Σ_{i∈T} λ_i = 0, or ABORT. Requirement: Pr[ABORT] ≤ τ for every V, with τ = ε/(9(c−1)S n_c)
as in (R1).

**What a solution is [proved, `lem:fc-zero-sum`(d)].** A nonzero s ∈ F_p^M solves
Σ_i s_i^{p−1} λ_i = 0 exactly when T = supp(s) is a nonempty zero-sum subset. Then s = 1_T is
a valid witness for `prop:descent`, with no root extraction. There is no other kind of
witness: the target equation leaves no freedom beyond the support.

**Worst-case variant ZS^wc.** The same with an arbitrary bank. It is total exactly when
M ≥ D(C_p^g) = g(p−1)+1 (Chevalley–Warning; the tight bank repeats each e_j p−1 times)
[proved, `lem:fc-zero-sum`(b), `thm:power-sde`(iii)]. This is BIS_p of [GKSZ20, Def. 6.1]
[cited], with g equations and M columns.

**Efficiency targets.** (b1) time and M polynomial in g and log p; (b2) for fixed p, time and
M polynomial in g. Since p = c+1 ≤ m+1 at this grade, "polynomial in p" is already
polynomial in the input size, so (b1) and "poly(g, p)" are the same requirement here.

### 1.2 Problem (a): the sampler

Two readings, both treated.

- **(a-i), the owner's reading.** Produce in polynomial time the i.i.d. ideal supply that
  `thm:free-coordinate` assumes. Or say exactly what that supply needs, and where it enters.
- **(a-ii), the source notes' reading.** `2026-11-02-rees-schedule3-cost.md` §6.3 and
  `2026-11-02-rees-free-coordinate-appendix.md` §4 mean "a polynomial-time sampler" as the
  FCS *witness* sampler: at a grade with 2 ≤ κ_d < p−1, find a nonzero y ∈ (P_κ ∪ {0})^M with
  Λy = 0 for an i.i.d. bank, in time polynomial in g, at small arity. The free-coordinate
  sampler needs about κ^a trials, and `prop:rc-lower` shows bank-oblivious designs cannot do
  better.

## Part 2. Results on (b)

### Z1. Equivalence with average-case binary SIS [proved]

Let BinSIS(n, m, p) be the problem: given A uniform in F_p^{n×m}, find x ∈ {0,1}^m, x ≠ 0,
with Ax = 0. This is the average case of [KMOSW, Problem 1.9], "F_q^n-Subset-Sum" [cited].

**(i) Node ⇒ solver.** Let L be the direct sum of g filiform algebras of class p−1. Copy t
has basis e_{t,0},…,e_{t,p−1} and brackets [e_{t,0}, e_{t,i}] = e_{t,i+1} for 1 ≤ i < p−1.
- L has class c = p−1 < p, dimension gp, and γ_c(L) of dimension g [exact for
  (p,g) ∈ {(3,1),(3,3),(5,1),(5,2),(7,2)}, T7; the general case follows because brackets
  act copywise].
- Take H = 1. Then the homogeneous lift is 0 and K_c = 0, so V = F_p^g.
- Grade c is the first stage, and its inputs are fresh lifted sources. So the bank of a grade-c
  node is a uniform g × M matrix.
- For H = 1 the post-measurement branch is
  ρ_λ = |G|^{-1} Σ_z χ_λ(−z) R_z (`lem:central` with K = 0). Its entries are
  ⟨x|ρ_λ|y⟩ = |G|^{-1} χ_λ(z_x − z_y) when x = σ(q)z_x and y = σ(q)z_y lie in the same Z-coset,
  and 0 otherwise.
- That is exactly the uniform mixture over q ∈ G_c/Z_c of the pure states
  |Z|^{-1/2} Σ_z χ_λ(z)|σ(q)z⟩. Anyone holding λ can prepare it with one abelian Fourier state.

So a node can be simulated from the labels alone. This holds even if it acts quantumly on the
post-measurement registers, as long as it makes no further oracle queries. Hence any
bank-reading node with Pr[ABORT] ≤ τ solves BinSIS(g, M, p) with probability ≥ 1−τ, in the
node's own time, classical or quantum. ∎

**(ii) Solver ⇒ node.** Let the first t labels have reduced row echelon form R with pivot
set P, and span W. Write every later label in that basis: its coordinates are its entries at
P. If W = V, then the later labels λ_i = E x_i become P' x_i with P' invertible, and P'
depends only on the first block. So the coordinate matrix is uniform on F_p^{a×(M−t)},
independent of the first block. Also Pr[W ≠ V] ≤ (p^a − 1)/(p−1)·p^{−t} ≤ p^{a−t}/(p−1).
- A BinSIS solution x on the later block gives the witness t + supp(x).
- Disjoint blocks are independent by `lem:s3-law`, so k attempts on k disjoint blocks turn
  failure δ into δ^k.
- So a solver for every n ≤ g with failure δ gives a node of arity k(t + M') with
  Pr[ABORT] ≤ (δ + p^{g−t}/(p−1))^k. The first-block columns get s_i = 0; they are consumed
  and discarded, as in `prop:descent`. ∎
- [exact] T5: on three cases, complete enumeration over all banks shows that, given
  W = V, the coordinate matrix is exactly uniform for every first block. The cases are
  (p,g,a,t,M') = (3,3,2,3,2), (3,2,1,2,3) and (5,2,1,2,2), with 59049, 243 and 625 banks.
  The span-failure counts 8505/59049, 27/243 and 25/625 meet the bound.
- T5b: the reduction with a brute-force solver returns valid witnesses (554 of 560 random
  instances; the rest are span failures or banks with no binary solution).

### Z2. Obstruction when p grows [proved, conditional on a cited theorem]

[cited] MP13 Thm 1.1 (author copy of 13 Feb 2013; corollary of its Thm 3.8). Let m = poly(n)
and β ≥ β_∞ ≥ 1, and let q ≥ β·n^δ for a constant δ > 0; Thm 3.8 also asks that q have at most
poly(n) divisors below β_∞, which holds for prime q. Then average-case SIS with solutions
‖z‖₂ ≤ β, ‖z‖_∞ ≤ β_∞ is as hard as worst-case lattice approximation within
γ = max{1, ββ_∞/q}·Õ(β√n). The reduction is classical and uses the solver as a black box, so a
quantum solver gives a quantum lattice algorithm.

**Claim.** Fix constants k > 1 and δ > 0. Suppose a bank-reading node F has, for primes
p ∈ [g^k, 2g^k], arity M(g,p) ≤ p² g^{−2δ} and M ≤ poly(g), runs in time poly(g), and aborts
with probability ≤ 1 − 1/poly(g). Then worst-case approximate lattice problems in dimension g
are solvable in polynomial (quantum, if F is quantum) time within γ = Õ(√(Mg)).

*Proof.* By Z1(i), F solves BinSIS(g, M, p) with non-negligible probability. A binary
solution z = 1_T has ‖z‖₂ ≤ √M =: β and ‖z‖_∞ = 1 =: β_∞. The arity bound gives
p ≥ √M·g^δ = β n^δ with n = g. Since p = poly(g), m = M = poly(n), and β β_∞/p ≤ 1. Apply the
cited theorem. ∎

**Corollaries.**
- *Arity at the existence threshold.* At M = g(p−1)+1 the condition is p ≥ g^{1+2δ}. Prop. D
  of the linear-arity report needed p ≥ ω(g² log g) via GPV Prop. 5.7.
- *Exponent growth.* Under the standard assumption that polynomial-factor worst-case lattice
  approximation is not in BQP, no node has arity ≤ C g^{e} p^{j}, with constants C, e and j < 2,
  and time poly(g, p) for all p. So the exponent of g in the arity of any efficient node grows
  without bound in p, or the p-dependence is at least quadratic. The known algorithms fit
  this: Schedule 1 has exponent (p−1)⌈log₂ p⌉, KMOSW Thm 1.11 has p−1, and KMOSW Thm 1.10
  has 1+⌊(p+3)/4⌋.

The assumption is the standard post-quantum one. It is a hypothesis, not a theorem, so the
nonexistence statements are **[conjecture]** and the implication is **[proved]**.

### Z3. Where Z2 can matter for the paper [proved]

In `thm:free-coordinate`(iii) the query count is c S ∏_{d=2}^{c} M_d, with M_d ≥ g_d+1 ≥ 2. So
it is at least 2^{c−1}, and the classical time is at least that. At Γ_0, c = p−1. Z2 needs
p ≥ g^{1+2δ}. So every family where Z2 bites already has Schedule 3 superpolynomial, at least
2^{g^{1+2δ}}, whatever node it uses.

Conversely, Schedule 3 can be polynomial only if c = O(log m), that is p = O(log m). Then the
zero-sum node matters only when p^{g_c} is superpolynomial, that is
g_c ≫ log m/log log m ≥ p^{1−o(1)}. Z2 needs g ≤ p^{1/(1+2δ)}, so it says nothing there. MP13
needs q ≥ β n^δ, and GKSZ OP4 and KOW footnote 7 record that no reduction is known for
constant q [cited]. **So "(b) for general
profiles" cannot by itself make Schedule 3 polynomial. Its relevant form is:**

> **Open question Q_b.** Is average-case BIS_p solvable in time f(p)·poly(g) from
> f(p)·poly(g) columns, uniformly in p? More modestly, for fixed p, is it solvable at O(g)
> or o(g²) columns?

Known algorithms use g^{Θ(p)} columns (Z4). The o(g²) question is open even at p = 3 for
classical algorithms; KMOSW Thm 1.3 gives a quantum algorithm at ε g² [cited]. At m = Θ(n)
every known attack is exponential (KMOSW §1.3) [cited].

### Z4. Fixed p: polynomial nodes exist [cited]; better than Schedule 1 at Γ_0

Read from the local full texts in `2026-11-02-rees-linear-arity/lit/` (their
`LITERATURE_SUMMARY.md` §2). In the notation n = number of equations ≤ g, m = M:

| result | case | columns | time |
|---|---|---|---|
| Schedule 1 = IS17 Thm 3 (`thm:is-import`, d = p−1) | worst | B_{p−1}(g) = [(p−1)^{(p−1)(p−2)/2}(g+1)^{p−1}]^{⌈log₂ p⌉} | poly(M, log p) |
| II24 Thm 2 | worst | p^{O(p log² p)} g^{O(p log p)} | poly |
| KMOSW Thm 1.11 | worst | p^{p²}(g+1)^{p−1} | poly(m) |
| KMOSW Thm 1.10 | average, failure 2^{−Ω(n)} | p^{p²} g^{1+⌊(p+3)/4⌋} | poly(m) |
| KOW Thm 1.2 (p = 3) | worst | g²/3 + C g log g | poly |
| `prop:triangular-sde` at (3,2) | worst | (g+1)(g+2)/2 | poly |
| two-level (3,2), implemented here | worst | (g+1)² | O(g⁴) field ops |

- **Use at Γ_0 (an option for the owner, [cited]).** KMOSW Thm 1.11 never aborts on any bank,
  so it drops in for Schedule 1 in (R1) exactly as the zero-sum node (Z-det) does: the proof
  of `lem:fc-forest` needs only that the node is deterministic and total.
- **Size of the change.** At fixed c = p−1 it lowers the exponent of g_c in M_c from
  (p−1)⌈log₂ p⌉ to p−1, for example from 12 to 4 at p = 5.
- **The average-case Thm 1.10.** It needs Z1(ii) to handle an unknown V, plus Z1(ii)'s
  amplification, because 2^{−Ω(n)} is not small when a = dim V is small. Small a can be
  handled by reachable sums, since a is observed as the rank.
- **Status.** Not proposed for the paper text until a human checks KMOSW (a Sept-2026 arXiv
  preprint; references.bib already flags its identifier).

### Z5. Two-level contractions fail at κ = p−1 for p ≥ 5 [proved; re-derivation]

This is already stated in `appendix-schedule2.tex` (Scope) from
`POWER_SDE_SYMMETRIC_CONTRACTION.md`. Here is a short independent proof and check.

A contraction has the form C_ij = z_i z_j(α_j+β_i) with C_00 ≠ 0 and entries in
Q_0° = {0,1}. Here z_m = ξ^m runs over all of F_p^× and z_0 = 1. Such a C is determined by
its first row and column:

  C_ij = z_i C_0j + z_j C_i0 − z_i z_j C_00.

Put C_00 = 1 and fix i ≥ 1 with f = C_i0 ∈ {0,1}. For j ≥ 1 and e = C_0j, the entry
V = z_i e + z_j f − z_i z_j lies in {0,1} only if z_j takes one value determined by (e, f, z_i):

| (e, f) | V | allowed z_j |
|---|---|---|
| (0, 0) | −z_i z_j | z_j = −1/z_i |
| (1, 0) | z_i(1 − z_j) | z_j = 1 − 1/z_i |
| (0, 1) | z_j(1 − z_i) | z_j = 1/(1 − z_i) |
| (1, 1) | 1 − (1−z_i)(1−z_j) | z_j = −z_i/(1−z_i) |

- With f fixed, every z_j, j = 1,…,p−2, must lie in a set of at most 2 values. They are
  p−2 distinct values, so p ≤ 4. ∎
- So `prop:decoupled-sde` and `prop:triangular-sde` never apply at Γ_0 for p ≥ 5. At p = 3
  they apply: 3 contractions.
- [exact] T6: contraction counts 3, 0, 0, 0, 0 at p = 3, 5, 7, 11, 13 (normal form). A direct
  search over all C ∈ {0,1}^{4×4} at p = 5, against a basis of W⊗W and with no normal form,
  finds 0, and at p = 3 it finds the same 3.
- The p = 3 two-level finder `p3_two_level` is implemented. Level 1 takes a kernel vector of
  each block of g+1 columns, and T_1 = {w=1}, T_2 = {w=−1} have equal sums u_b. So u_b has
  realizations of 0, u_b and 2u_b. Level 2 takes a kernel vector of the g+1 vectors u_b.
- [exact] T3: valid witnesses on all 81 banks at g = 1, and on all 262144 banks at g = 2 with
  columns in {0, e_1, e_2, e_1+e_2}. Also valid on 806, 806, 806, 806, 206, 206, 206 random,
  random-subspace and adversarial banks at g = 1, …, 7.

### Z6. Baselines [proved, exact]

- **Reachable sums (`lem:fc-zero-sum`(c)).** M·min(2^M, p^g) operations. [exact] T1: agrees
  with exhaustive search on 3300 random banks with p ∈ {2,3,5,7}, g ≤ 3, M ≤ 11.
- **Davenport.** [exact] T2: every bank of length g(p−1)+1 has a zero-sum subset,
  exhaustively for (p,g) = (3,1), (3,2), (5,1), (7,1), (2,3), (2,4). That is
  27 + 59049 + 3125 + 823543 + 4096 + 1048576 banks. The tight bank of length g(p−1) has none.
- **Coordinate-block recursion [proved; implemented].** Split the g coordinates into L blocks
  of sizes k_j. At level j, group the current items in groups of D_j = k_j(p−1)+1. Each group
  has a nonempty subfamily summing to 0 on block j (Davenport in F_p^{k_j}). Reachable sums
  find it in D_j p^{k_j} steps, and the merged item is that sum, with the union of the
  disjoint supports. After L levels one item remains: a zero-sum subset of the bank, for
  *every* bank. Arity ∏_j D_j, time ≤ arity·max_j p^{k_j}·poly.
  - With k_j ≈ √g, both are exp(O(√g·log(gp))): subexponential, but not polynomial.
  - [exact] T4: valid witnesses for p ∈ {3,5,7}, g ≤ 4 and every k with arity ≤ 3000,
    36 instances each (random and adversarial).
- **Lattice probe** (linear-arity report §7, float): BKZ-20 solves random banks at linear
  arity for 10 ≤ a ≤ 40 at small p. Finite data; it says nothing for all a.
- **Arity table** (`results.json`, `arity_table`; log₂ values are floors):

| p | g | Davenport | p^g states | log₂ B_{p−1}(g) | two-level (p=3) |
|---|---|---|---|---|---|
| 3 | 8 | 17 | 6561 | 14 | 81 |
| 3 | 16 | 33 | 4.3e7 | 18 | 289 |
| 5 | 8 | 33 | 3.9e5 | 74 | n/a |
| 5 | 16 | 65 | 1.5e11 | 85 | n/a |
| 7 | 16 | 97 | 3.3e13 | 189 | n/a |
| 11 | 16 | 161 | 4.6e16 | 761 | n/a |

### Z7. Conjectures (not proved)

- **[conjecture]** For every fixed p ≥ 3 (classically) and every fixed p ≥ 5 (quantumly),
  average-case BIS_p at O(g) columns has no polynomial-time algorithm. No evidence beyond the
  failure of known attacks [KMOSW §1.3]. Not a claim gate.
- **[conjecture]** Q_b has a negative answer (BIS_p not FPT in p). No evidence either way.

## Part 3. Results on (a)

### A1. Where the i.i.d. requirement enters [proved, by reading the proofs]

- **E1, leaves.** Fresh lifted sources ρ_{exp(\hat h)} on G_c, from c queries
  (`lem:homogeneous`) or c copies (`lem:copy-lift`). Both are exact.
- **E2, one bank (`lem:s3-law`).** If a node's M inputs are in the state ρ_{H_d}^{⊗M} ⊗ ω_X,
  its labels are i.i.d. uniform on K_d^⊥, independent of X.
- **E3, every bank (`lem:s3-tree`(a), `lem:fc-forest`(a)).** Induction: E2's hypothesis holds
  at every node. This uses three facts:
  - `prop:descent` is pointwise in the record;
  - no label is read twice (`rem:s3-caveat`);
  - parents measure registers that differ from their children's.
- **E4, the only uses of uniformity.** These are the bank bounds: `lem:s3-moment`,
  `thm:free-coordinate`(i) (β), and `lem:fc-zero-sum`(a). Schedule 1, the linear nodes and
  (Z-det) never use the law.
- **E5, implementation.** `lem:s3-hybrid` moves the ideal-law bounds to the compiled circuit,
  at additive cost N_instr·η in total variation.

### A2. The supply is produced exactly, in polynomial time [proved]

By E1, a leaf costs c oracle queries (or c copies) plus the gates of
`thm:uniform-compilation`(i)–(iii), which number poly(n, log p, log(1/η)). By E3, every
internal node's inputs are the exact outputs of disjoint child nodes. The central instrument
costs 2g_d single-coordinate QFTs plus controlled central translations. So the "i.i.d. ideal
supply" is not an outside resource. The procedure generates it, and its law is the Born law of
the procedure's own measurements.

What the guarantee needs, and cannot drop:
1. Inputs exactly of the form in Definition `def:input-contract`(iii): an oracle, or fresh
   independent copies of ρ_H.
2. No reuse of labels or registers.

Both are needed. For (1), the separable bank after `prop:refresh` has correct one-copy
marginals and breaks the lift. For the arity at Γ_0: below g(p−1)+1, the tight bank (each e_j
repeated p−1 times, padded) has no witness. So no node of smaller arity has a guarantee that
holds without the label law. [proved; exact T2]

### A3. Fourier sampling gives the law exactly [proved]

Work in the right regular representation. Let ρ_H = |G|^{-1} Σ_{h∈H} R_h (the coset density of
`lem:copy-lift`), Π_λ = R(e_λ) with e_λ = |Z|^{-1} Σ_z χ_λ(−z) z, and let P_π = R(e_π) be the
isotypic projectors of the irreps π of G_d.

1. **Central instrument.** This is abelian Fourier sampling of Z_d on a central ancilla. By
   `lem:central` the label is exactly uniform on K^⊥, and the branch is ρ_λ.
2. **Weak Fourier sampling over G_d (measure the irrep name π).**
   - Every z ∈ Z is central, so π(z) = ω_π(z)·I. Hence e_λ e_π = e_π if ω_π matches λ, and 0
     otherwise. Since Σ_π e_π = 1, Π_λ = Σ_{π over λ} P_π.
   - ρ_H lies in R(C[G]), so it commutes with every P_π. Hence the central character of the
     measured π has law tr(Π_λ ρ_H), which is uniform on K^⊥.
   - Forgetting π given λ leaves Σ_{π over λ} P_π ρ_H / Pr[λ] = Π_λ ρ_H / Pr[λ] = ρ_λ.
   - So the joint law of (λ, branch) is that of item 1. If π is kept in the record and
     never read, nothing downstream changes. If π is read, the branch P_π ρ_H/Pr[π] need not
     satisfy the trace formula of `lem:central`, and `prop:descent` is no longer guaranteed.
3. **Measured oracle values.** Standard coset-state preparation with the function value kept
   gives |aH⟩ for a uniform coset, together with its recorded value. Left translations L_a
   commute with every R_g, so:
   - Pr[λ | aH] = ⟨H|Π_λ|H⟩ for every coset. The labels are i.i.d. uniform on K^⊥ and
     independent of the recorded values.
   - tr(Π_λ|aH⟩⟨aH|Π_λ R_g) = ⟨H|Π_λ R_g Π_λ|H⟩ = Pr[λ]·tr(ρ_λ R_g).
   - The output entries of `prop:descent` are products of exactly these per-target traces.
     So the output is ρ_{HZ/Z} for every record of function values, labels and witness.

### A4. Coset-copy input for `thm:free-coordinate`(iii) [proved, conditional as (iii) is]

The proof of `lem:fc-forest`(a) uses the leaves only through the sentence "Leaves are fresh
lifted sources ρ_{H_c} in product". With coset-copy input, `lem:copy-lift` makes each leaf
exactly ρ_{exp(\hat h)} from c fresh copies. Those copies are independent of everything else
by Definition `def:input-contract`(iii), so the leaves are in product with every record and
register. Nothing else changes:
- (b) of `lem:fc-forest` and the proof of (iii) do not mention the oracle;
- the leaf instrument (uniform address, c controlled right actions, cleanup) is compiled by
  `thm:uniform-compilation`(ii)–(iii) with the same n transforms per leaf that q_max counts.
  `lem:copy-lift` is already one of "the steps behind Theorem `thm:main`".

So (iii) holds for coset-copy input with c S ∏_d M_d copies in place of queries. So do
`cor:fpt-r`(i) and the Rees route of (ii), since the vote evaluates no oracle. The IMS
alternative in (ii) still needs a coherent oracle.

### A5. The witness sampler at FCS grades (reading a-ii)

- **[proved]** At κ = (p−1)/2 (h = 2; such a grade exists iff p ≤ 2c+1 and p ≥ 5) the digit set
  is P_κ ∪ {0} = {0, ±1} ([exact] T8, all primes 5 ≤ p < 400). So the FCS witness problem is
  exactly average-case ternary SIS: SIS_∞ with β_∞ = 1, the average case of [GKSZ20,
  Def. 6.2]. Z1(i) and Z1(ii) hold verbatim with {0,±1} in place of {0,1}. Z2 holds verbatim,
  since ternary solutions have ‖z‖₂ ≤ √M and ‖z‖_∞ = 1. Z3 holds too: such a grade forces
  c ≥ (p−1)/2.
- **[cited]** For fixed κ there are polynomial nodes: Schedule 1, and `thm:power-sde`(ii) /
  `prop:decoupled-sde` above their thresholds.
- **[conjecture]** For fixed h ≥ 3 the problem is average-case module-SIS over Z[ζ_h] with a
  degree-one prime modulus 𝔭 | p. Lift F_p = Z[ζ_h]/𝔭; roots of unity are short. Then a
  witness sampler that is polynomial uniformly in p would solve that problem. No hardness
  theorem for this modulus is known to me, and I did not search.
- The bank-adaptive question of the paper, about κ^{a−Ω(a)} trials at arity a+O(1), is not
  settled here.

## Part 4. Counterexamples and baselines

- **Tight bank.** e_1,…,e_g, each p−1 times: no zero-sum subset at arity g(p−1)
  ([exact] T2, `thm:power-sde`(iii)).
- **No two-level contraction at κ = p−1, p ≥ 5** (Z5).
- **Correct marginals are not enough**: the separable bank after `prop:refresh` (paper).
- **Classical baselines**: reachable sums p^g; exhaustive 2^M; block recursion (Z6);
  Wagner/BKW 2^{O(n/log(m/n))} [cited, KMOSW §1.3]; the Z4 table.
- **Smallest failing instance of any claim here.** None found. Every check passed.

## Part 5. Scripts

Folder `research/audits/reviews/2026-11-04-rees-s3-zero-sum/`:
- `zs_lib.py`: the code. It contains
  - F_p linear algebra;
  - the exhaustive and reachable-sum searches;
  - `p3_two_level` and `block_recursion`;
  - the two reductions `zs_from_binsis` and `binsis_from_zs`;
  - the contraction enumerator at κ = p−1, in normal form and directly;
  - the filiform-sum structure constants and the lower central series;
  - `is_arity`.
- `test_zs.py`: checks T1–T8 and the arity table. Every check is exact integer arithmetic
  with fixed seeds, and finite checks can only falsify.
- `results.json`: the output.

Command (about 40 s, one core):

    cd research/audits/reviews/2026-11-04-rees-s3-zero-sum
    nice -n 10 /opt/anaconda3/bin/python -I test_zs.py

Result: all 10 checks PASS.

## Part 6. Proposed paper text (AI-checked, pending human review)

Not applied: no .tex edits in this pass. Each item gives the location, the current text and
the replacement.

**P1. `appendix-free-coordinate.tex`, paragraph after `lem:fc-zero-sum`, last sentence.**
Current: "For $g_d \le r$ and $p = c+1 \le r+2$ the search costs $2^{O(r\log(r+2))}$; for
general profiles $p^{g_d}$ can be exponential in $m$, and Schedule~1 remains the polynomial
choice at fixed $c$." Replacement:

    For $g_d \le r$ and $p = c+1 \le r+2$ the search costs $2^{O(r\log(r+2))}$; for general
    profiles $p^{g_d}$ can be exponential in $m$, and Schedule~1 remains the polynomial choice
    at fixed $c$. Remark~\ref{rem:fc-zero-sum-sis} shows that a node of this kind that is
    polynomial uniformly in $p$ would solve average-case SIS, and why that question does not
    affect whether Schedule~3 is polynomial.

**P2. New remark after that paragraph** (AI-checked, pending human review):

    \begin{remark}[The zero-sum node is average-case binary SIS; AI-checked, pending human review]
    \label{rem:fc-zero-sum-sis}
    Call a node at a grade $d \in \Gamma_0$ \emph{bank-reading} if, after (F1), it computes its
    witness from the bank (with private coins, classically or quantumly, possibly also acting on
    the post-measurement registers, but with no further oracle query or source) and converts as in
    (F6). By Lemma~\ref{lem:fc-zero-sum}(d) its search problem on the ideal support is: given
    labels independent and uniform on an unknown subspace of $\Fp^{g_d}$, find a nonempty
    zero-sum subset. This is the average case of $\mathrm{BIS}_p$~\cite[Definition~6.1]{GoosKamathSotirakiZampetakis2020}.
    \begin{enumerate}[label=(\alph*),leftmargin=2em]
      \item Let $\mathcal{L}$ be the direct sum of $g$ filiform algebras of class $p-1$, so that
      $c = p-1$ and $g_c = g$, and let $H = 1$. Then the bank of a grade-$c$ node is a uniform
      $g \times M$ matrix, and each post-measurement register is the state $\rho_\lambda$ of
      Lemma~\ref{lem:central}, which is the uniform mixture over $q \in G_c/Z_c$ of
      $|Z_c|^{-1/2}\sum_{z}\chi_\lambda(z)|\sigma(q)z\rangle$ and so can be prepared from
      $\lambda$. Hence a bank-reading node that aborts with probability at most $\tau$ finds,
      with probability at least $1-\tau$ and in the same time, a nonzero $x \in \{0,1\}^M$ with
      $Xx = 0$ for a uniform $X \in \Fp^{g\times M}$.
      \item Conversely, write the last $M-t$ labels in the reduced echelon basis of the span of
      the first $t$. Unless that span differs from $K_d^\perp$, which has probability at most
      $p^{g_d-t}/(p-1)$, the coordinates form a uniform $a_d\times(M-t)$ matrix independent of
      the first $t$ labels, and a binary solution $x$ gives the witness $\{t+i : x_i = 1\}$.
      Disjoint blocks are independent by Lemma~\ref{lem:s3-law}, so $k$ blocks raise a solver's
      failure probability to the $k$-th power.
      \item A binary solution has Euclidean norm at most $\sqrt M$ and maximum norm $1$. Fix
      constants $k > 1$ and $\delta > 0$. If a bank-reading node runs in time $\poly(g_d)$ with
      abort probability at most $1 - 1/\poly(g_d)$ and arity $M_d \le p^2 g_d^{-2\delta}$ on primes
      $p = \Theta(g_d^k)$, then by~\cite[Theorem~1.1]{MicciancioPeikert2013} worst-case lattice
      problems in dimension $g_d$ can be approximated within $\tilde O(\sqrt{M_dg_d})$ in
      polynomial time, quantum if the node is. In particular the exponent of $g_d$ in the arity
      of a polynomial-time node cannot stay bounded as $p$ grows unless such approximation is
      easy; it is $(p-1)\lceil\log_2 p\rceil$ for Schedule~1.
      \item Part~(c) needs $p \ge g_d^{1+2\delta}$. At such a grade $c = p-1$, and the query count
      $cS\prod_d M_d \ge 2^{c-1}$ of Theorem~\ref{thm:free-coordinate}(iii) is superpolynomial for
      every choice of node. Where that count can be polynomial, $p = O(\log m)$ and part~(c)
      gives nothing. Whether binary SIS modulo $p$ is solvable in time and arity
      $f(p)\,\poly(g_d)$ is open, and so is arity $o(g_d^2)$ in polynomial time even at $p = 3$.
    \end{enumerate}
    For $p \ge 5$ no two-level contraction exists at $\kappa = p-1$ (Appendix~\ref{app:schedule2}),
    so Propositions~\ref{prop:decoupled-sde} and~\ref{prop:triangular-sde} do not apply at
    $\Gamma_0$; at $p = 3$ they give $(g_d+1)^2$ and $(g_d+1)(g_d+2)/2$ columns.
    % NEEDS HUMAN VERIFICATION: MicciancioPeikert2013 Theorem 1.1 (and Theorem 3.8) as read from the
    % author copy of 13 Feb 2013 (research/audits/reviews/2026-11-02-rees-linear-arity/lit/mp13_LWsE.txt);
    % numbering may differ in the CRYPTO version.
    \end{remark}

New bibliography entry (NEEDS HUMAN VERIFICATION: volume and pages from memory):

    @inproceedings{MicciancioPeikert2013,
      author    = {Daniele Micciancio and Chris Peikert},
      title     = {Hardness of {SIS} and {LWE} with Small Parameters},
      booktitle = {Advances in Cryptology -- CRYPTO 2013},
      series    = {Lecture Notes in Computer Science},
      volume    = {8042},
      pages     = {21--39},
      publisher = {Springer},
      year      = {2013}
    }

**P3. `appendix-free-coordinate.tex`, Scope paragraph.** Current clause: "…and at the zero-sum
grade $\kappa_d = p-1$ it falls back on Schedule~1 or on the zero-sum node of
Lemma~\ref{lem:fc-zero-sum}, whose search costs $p^{O(g_d)}$." Replacement:

    …and at the zero-sum grade $\kappa_d = p-1$ it falls back on Schedule~1 or on the zero-sum
    node of Lemma~\ref{lem:fc-zero-sum}, whose search costs $p^{O(g_d)}$; a node there that is
    polynomial uniformly in $p$ would solve average-case binary SIS
    (Remark~\ref{rem:fc-zero-sum-sis}).

**P4. `main.tex`, after "Whether some method finds a witness in time $\kappa^{a-\Omega(a)}$ at
arity $a + O(1)$ is open."** Add:

    At $h = (p-1)/\kappa_d = 2$ the witness entries lie in $\{0,\pm1\}$, and at $\kappa_d = p-1$
    in $\{0,1\}$, so at these grades any method that reads the bank solves average-case SIS with
    ternary or binary solutions; by Remark~\ref{rem:fc-zero-sum-sis}(c), a method polynomial
    uniformly in $p$ there would approximate worst-case lattice problems for $p \ge g_d^{1+2\delta}$.

**P5. Coset-copy input (A4).**
- In `cor:fpt-r`(i) and (ii), replace "(for coset-copy input this is argued, not proved)" by
  "(also for coset-copy input, with $c$ copies of $\rho_H$ in place of $c$ queries per lifted
  source)".
- In the proof of (i), replace "since that theorem is stated for oracle input, this extension
  is argued rather than proved." by:

      the proof of Lemma~\ref{lem:fc-forest}(a) uses the leaves only as fresh copies of
      $\rho_{H_c}$ in product with everything else, which Lemma~\ref{lem:copy-lift} provides from
      fresh copies, and the leaf instrument is compiled by
      Theorem~\ref{thm:uniform-compilation}(ii)--(iii) with the same transform count, so
      Theorem~\ref{thm:free-coordinate}(iii) holds for coset-copy input with $c\,S\prod_dM_d$
      copies.

- In `tab:main-regimes`, coset-copy row, replace "(extending Thm.~\ref{thm:free-coordinate},
  stated for oracle input, is argued, not proved)" by "(for
  Thm.~\ref{thm:free-coordinate}(iii), see the proof of Cor.~\ref{cor:fpt-r})".
- The IMS route of (ii) keeps "needs a coherent oracle".

**P6. `REES_FULL_CONTINUATION.md` item 4.** Replace "Still open: a polynomial-time sampler,
and a polynomial-time finder at the zero-sum grade κ = p−1 for general profiles." by:

> Still open: a polynomial-time witness sampler at the free-coordinate grades, and a
> zero-sum node at κ = p−1 with arity and time f(p)·poly(g_c), or arity o(g_c²) at fixed p.
> At the grades with h = (p−1)/κ_d ∈ {1,2} the node is average-case binary or ternary SIS
> (`2026-11-04-rees-s3-zero-sum.md` Z1, A5). Uniformly in p it would break worst-case lattice
> approximation for p ≥ g^{1+2δ} (Z2, via MP13). But any profile in that range already has
> 2^{c−1} queries (Z3), so the question that matters is the fixed-p exponent. Literature
> nodes at Γ_0 reach (g+1)^{p−1} columns worst case and g^{1+⌊(p+3)/4⌋} on average (KMOSW,
> unverified; Z4), against B_{p−1}(g) for Schedule 1. The i.i.d. supply itself is produced
> exactly by the procedure (A2, A3), and the coset-copy extension of (iii) is proved (A4).
> AI-checked, pending human review.

## Part 7. Gates, next question, next command

**Claim gates that must stay false:**
- "polynomial-time Schedule 3";
- "efficient linear-arity (or o(a²)) SDE solver exists";
- "BIS_p/SIS_p or the diagonal SDE search is hard for fixed p or κ";
- any novelty claim for Z2 (an elementary sharpening of Prop. D) or for the p = 3 two-level
  finder (ISS, KOW and `prop:triangular-sde` are better);
- human-reviewed status.

This note flips nothing.

**Next hard question.** Q_b at p = 5: a polynomial-time average-case BIS_5 node at
o(g³) columns (KMOSW Thm 1.10 gives about g³), or a reason none exists.

**Next command, artifact and acceptance test.** A human reads KMOSW Thm 1.11, its §§
behind Thm 1.10, and MP13 Thm 1.1/3.8. Then implement KMOSW Thm 1.11 for p = 5 in
`2026-11-04-rees-s3-zero-sum/`, run under nice. Use the column count the proof actually
needs; the theorem's 5^{25}(g+1)^4 is a loose uniform bound. Acceptance: valid witnesses on
every bank from `adversarial_banks` and on 10³ random banks for g ≤ 6. Record the count used
against B_4(g) = G(4,g)^3.
