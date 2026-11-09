# Rees Schedule 3: a zero-sum node at p = c+1, and Corollary `cor:fpt-r`(ii) without IMS (2026-11-04)

**Status: COMPLETE (2026-11-04). AI-checked, pending human review. No paper file edited; nothing committed.**

Owner item: the "Optional, argued" zero-sum node of
`research/audits/reviews/2026-11-04-rees-fcs-budget.md`, Section B.5.

Labels: **proved** (complete argument here, or cited by label), **exact computation**
(integer/rational arithmetic in a script in this repo), **float check** (floating point or
Monte Carlo), **argued** (a sketch a reader must still check).

## Status log

- [x] Read B.5, `appendix-free-coordinate.tex` (F1-F6, `lem:fc-node`, (R1)-(R4),
      `lem:fc-forest`, `prop:fc-uniform`, Scope), `lem:s3-law`, `rem:s3-caveat`, `lem:s3-tree`,
      `prop:descent`, `thm:power-sde`(iii) and `cor:fpt-r` with its proof.
- [x] Wrote `theorems/rees_zero_sum_node.py` (new; imports `theorems/rees_fcs_budget.py`
      read-only for the other grades).
- [x] Exact budgets for the three filiform profiles (Part C).
- [x] Exhaustive probability checks and node / end-to-end simulations (Part D).
- [x] Tests: `tests/test_rees_zero_sum_node.py`, 25 passed.
- [x] Proposed paper text written (P1-P7).

## Summary of the outcome

The node is a proved lemma, and it fits into `lem:fc-forest` with no gap. Two versions:

- **(Z-rand)** the version asked for. Arity M = 1 + ⌈log2(p^{g_d}/τ_d)⌉. Bank event
  Pr[no nonempty zero-sum subset] ≤ (p^a − 1)/(2^M − 1) < τ_d, by pairwise independence
  and the second moment. **Proved.**
- **(Z-det)** a deterministic version that the B.5 sketch missed. Arity M = g_d(p−1)+1.
  By Chevalley–Warning a nonempty zero-sum subset exists for **every** bank, so the node
  never aborts and needs no label law at that grade. A reachable-sum search finds the subset
  in M·p^{a_d} vector additions. This is a drop-in replacement for the Schedule 1 solver at
  Γ_0, so `lem:fc-forest` holds verbatim. **Proved.**

Both search costs are 2^{O(r log(r+2))} when g_c ≤ r and p = c+1 ≤ r+2. So `cor:fpt-r`(ii)
holds through `thm:free-coordinate`(iii) and the new node, with the same status as part (i):
proved conditional on the steps behind `thm:main` and on the label law `lem:s3-law` for oracle
input, and argued for coset-copy input. No IMS step is needed. Neither node works for general
profiles at fixed c: there p^{g_c} = (c+1)^{g_c} can be exponential in m, and Schedule 1
remains the polynomial choice. So the node is an *option* at Γ_0, and only the FPT corollary
uses it.

No gap was found. Every check passed (Part D).

## Part A. The lemma (proved)

### A.1 Setting

Fix a grade d with κ_d = gcd(d, p−1) = p−1. Inside the paper's range 2 ≤ d ≤ c < p this
forces p−1 | d < p, so d = p−1 = c (`app:fc-mixed`, definition of Γ_0). Then p = c+1 ≥ 3,
because r ≥ 1 makes the algebra nonabelian, so c ≥ 2. *p = 2 never occurs.* (Part A.2 holds at
p = 2 as well, and nothing below uses p odd.) For s ∈ F_p we have s^d = s^{p−1} ∈ {0,1}, and it
is 1 exactly when s ≠ 0. Hence, for a bank λ_1,…,λ_M ∈ F_p^{g_d},

  s ≠ 0 and Σ_i s_i^d λ_i = 0  ⇔  T := supp(s) ≠ ∅ and Σ_{i∈T} λ_i = 0.     (A.1)

So a witness exists iff the bank has a nonempty zero-sum subset, and then s = 1_T is a
witness. Its entries lie in {0,1}, so (F4) needs no root extraction and no Bezout lift: s_i^d = s_i.

**The node (Z1)–(Z4).** It has public arity M, and in (Z-rand) no coins.

- (Z1) = (F1): apply the central instrument of `lem:central` for Z_d to each register and
  record Λ = [λ_1 … λ_M].
- (Z2) Find a nonempty T ⊆ [M] with Σ_T λ_i = 0. Use either the exhaustive search over the
  masks 1, …, 2^M − 1 in increasing order, or the reachable-sum search (A.4). If none exists,
  abort.
- (Z3) = (F5): put s = 1_T and check exactly that s ≠ 0 and Σ_l s_l^d λ_l = 0. Abort otherwise.
  This never fires after (Z2), but it makes the node total.
- (Z4) = (F6): apply `prop:descent` with witness s and output the register on G_{d−1}.

### A.2 Lemma `lem:fc-zero-sum`(a): the bank bound (proved)

*Claim.* Let λ_1,…,λ_M be independent and uniform on a subspace V ≤ F_p^{g} of dimension a,
with p any prime and M ≥ 1. Let X be the number of nonempty T ⊆ [M] with Σ_T λ_i = 0. Then

  E X = (2^M − 1) p^{−a},  Var X = (2^M − 1) p^{−a}(1 − p^{−a}),
  Pr[X = 0] ≤ (p^a − 1)/(2^M − 1).

*Proof.* Choose (in the proof only) a basis matrix E ∈ F_p^{g×a} of V and write λ_i = E x_i,
with x_1,…,x_M i.i.d. uniform on F_p^a. E is injective, so Σ_T λ_i = 0 iff Σ_T x_i = 0. Write
X_mat = [x_1 … x_M] ∈ F_p^{a×M}, a uniform matrix, so that Σ_T x_i = X_mat 1_T.

1. *One subset.* For T ≠ ∅ the vector 1_T is nonzero. Each row ξ of X_mat is uniform on
   F_p^M, so ξ·1_T is uniform on F_p, and the a rows are independent. Hence X_mat 1_T is
   uniform on F_p^a, and Pr[Σ_T x_i = 0] = p^{−a} =: π.
2. *Two subsets.* Let T ≠ T' be nonempty. Then 1_T and 1_{T'} are linearly independent
   over F_p. Suppose α1_T + α'1_{T'} = 0 with (α, α') ≠ 0. If α ≠ 0 and α' = 0, then 1_T = 0, which is
   impossible; the case α = 0 is the same. If both are nonzero, the supports agree, so T = T'
   and α = −α', a contradiction. (So 0/1 vectors are never proportional unless equal, for every p,
   including p = 2.) The map ξ ↦ (ξ·1_T, ξ·1_{T'}) from F_p^M to F_p^2 is therefore surjective
   and linear, so it pushes the uniform law to the uniform law. Applied row by row,
   (X_mat 1_T, X_mat 1_{T'}) is uniform on F_p^a × F_p^a. So the indicators I_T = [X_mat 1_T = 0]
   and I_{T'} are independent.
3. *Second moment.* The indicators I_T are pairwise independent Bernoulli(π) variables, with
   N = 2^M − 1 of them. So E X = Nπ and Var X = Nπ(1−π). By Chebyshev,
   Pr[X = 0] ≤ Pr[|X − EX| ≥ EX] ≤ Var X/(EX)² = (1−π)/(Nπ) = (p^a − 1)/(2^M − 1).
   At a = 0 every sum is zero, X = N and the bound is 0, which is correct. ∎

This is the bound of B.5 sharpened from p^a to p^a − 1, and it is exactly the variance
ratio. It increases with a, so (p^{g}−1)/(2^M−1) is a public bound for every a ≤ g, as β
is in (eq:fc-beta).

### A.3 Lemma `lem:fc-zero-sum`(b): arities (proved)

- *(Z-rand), explicit.* Let 0 < τ ≤ 1. Put M = 1 + k_0, where k_0 is the least k ≥ 0 with
  2^k ≥ p^{g}/τ, that is, M = ⌈g log2 p + log2(1/τ)⌉ + 1. Then 2^M ≥ 2p^g/τ, and since
  p^g/τ ≥ 1, 2^M − 1 ≥ p^g/τ. Hence (p^g − 1)/(2^M − 1) ≤ τ(1 − p^{−g}) < τ, and by A.2 the
  bank event at any a ≤ g has probability < τ. The least such M can be found exactly by
  comparing integers; Part C uses it as well.
- *(Z-det).* Let M = g(p−1)+1. Then **every** bank λ_1,…,λ_M ∈ F_p^{g} has a nonempty
  zero-sum subset. *Proof (Chevalley–Warning).* Consider the g polynomials
  f_j(s) = Σ_{i=1}^M λ_{ij} s_i^{p−1}, j = 1,…,g, in M variables over F_p. Their degrees sum to
  g(p−1) < M. By the Chevalley–Warning theorem the number of common zeros in F_p^M is
  divisible by p. Since s = 0 is one of them, there is a common zero s ≠ 0, and by (A.1) its
  support is a nonempty zero-sum subset. ∎ This is the Davenport constant
  D(C_p^g) = g(p−1)+1 (Olson 1969), which `thm:power-sde`(iii) quotes at p = 5, g = 2.
  The arity is tight. Repeat each of e_1,…,e_g exactly p−1 times. This gives g(p−1) columns
  with no nonempty zero-sum subset, since a subset sum is Σ_j k_j e_j with 0 ≤ k_j ≤ p−1. This
  is the example of `thm:power-sde`(iii).
  (Z-det) uses only the public g = g_d, so the guarantee covers every bank, not only the
  ideal support.

### A.4 Lemma `lem:fc-zero-sum`(c): search and cost (proved)

- *Exhaustive.* Visit the masks 1, …, 2^M−1 in increasing order. The sum of a mask is the sum
  of mask & (mask−1) plus one label. So the cost is at most 2^M − 1 vector additions in
  F_p^{g}, that is, (2^M)·O(g log p) bit operations, plus O(M) for the output.
- *Reachable sums.* Let R_j be the set of sums of nonempty subsets of {λ_1,…,λ_j}, stored with
  one representative subset per value. Then R_{j+1} = R_j ∪ {λ_{j+1}} ∪ (R_j + λ_{j+1}), and a
  zero-sum subset exists iff 0 ∈ R_M. When 0 first appears, follow the representatives back to
  output T. Every R_j lies in span(λ) ⊆ V, so |R_j| ≤ min(2^j − 1, p^a). The cost is at most
  M·min(2^M, p^{a})·O(g log p) bit operations, with a hash table keyed by vectors. This bound
  holds for every bank with p^a replaced by p^{g}.
- In both searches the witness is a deterministic function of Λ. The node draws no coins and
  has no capped random step. After (Z1) it measures and prepares no quantum register.

### A.5 Lemma `lem:fc-zero-sum`(d): output (proved)

On every record that does not abort, s = 1_T is a valid nonzero witness of (sde-target) by
(A.1), so (Z3) passes. By `prop:descent`, applied to G_d, Z_d, H_d and the public section,
the output is exactly ρ_{H_d Z_d/Z_d} = ρ_{H_{d−1}}, for every positive-probability label tuple
and every valid witness. The joint state of the record, the output and any outside system 𝒳 is
therefore as in `lem:s3-node`(d). The proof of `lem:s3-node`(d) applies word for word, since it
uses only that (N2)–(N5) are a classical map from Λ and coins to a record. Here the coins are
absent.

## Part B. The fit into `lem:fc-forest` (proved; no gap found)

### B.1 The modified rule

Change (R1) and (R3) of `app:fc-mixed` only at d ∈ Γ_0, where Γ_0 ⊆ {p−1} and Γ_0 ≠ ∅ iff
p = c+1. At such a grade the public rule may now choose one of three options:

- **(S1)** Schedule 1 with M_d = B_d(g_d). This is unchanged and is the default. It is
  polynomial for fixed c.
- **(Z-det)** the zero-sum node (Z1)–(Z4) with M_d = g_d(p−1)+1.
- **(Z-rand)** the zero-sum node with τ_d = ε/(9(c−1)S n_d), as at FCS grades, and any public
  M_d with (p^{g_d} − 1)/(2^{M_d} − 1) ≤ τ_d, for example M_d = 1 + ⌈log2(p^{g_d}/τ_d)⌉
  (A.3).

N and B in (R2) are unchanged. A zero-sum node has no capped step, so it is not counted in N.
No other grade's choice changes. n_d for d < p−1 does not involve M_{p−1}, and grade p−1 = c is
the top grade, whose n_c involves only the lower grades.

### B.2 Lemma `lem:fc-forest` with the new node: the proof

*(a) Factorization and label law.* Use the induction of `lem:fc-forest`(a) and
`lem:s3-tree`(a), with one more case. Let v_{j+1} be a zero-sum node of degree d = p−1, and
suppose the claim holds for j. Its M_d inputs are open registers, so restricted to 𝓔_j they
are ρ_{H_d}^{⊗M_d}, in product with the record and the other open registers. Take 𝒳 to be the
record together with those registers. `lem:s3-law` then gives labels that are i.i.d. uniform
on K_d^⊥ and independent of 𝒳, with post-measurement state ρ_{λ_1}⊗…⊗ρ_{λ_M}⊗ω_𝒳. Steps
(Z2)–(Z3) are a deterministic classical map from Λ to a record. By A.5, on every record that
does not abort, the output register is exactly ρ_{H_{d−1}}, in product with everything else.
So the claim holds for j+1.
- *(Z-det)*: the node never aborts (A.3), so this is literally the Γ_0 sentence of the current
  proof, with "Schedule 1 solver" replaced by "zero-sum search at arity g_d(p−1)+1".
- *(Z-rand)*: the node aborts on the bank event only, as an FCS node does.

*Reuse and consumption (the point B.5 left open).*

1. Each node measures only its own M_d input registers. These are outputs of M_d distinct
   children, or fresh leaves at d = c, and each register is measured exactly once.
2. The witness reads only that node's bank, and no later step reads the bank. Columns with
   s_i = 0 are consumed and discarded (`prop:descent`). The non-abort event depends on the
   node's own labels, which tilts their conditional law as in `rem:s3-caveat`. Nothing
   conditions on those labels again, and by A.5 the output state does not depend on them.
3. The parent's bank is measured on different registers, which are in product with every
   earlier record, so `lem:s3-law` applies again. This is `rem:s3-caveat`(i)–(iii) word for word.
4. The node draws no coins, so the freshness of coins is not needed.

No label is reused across nodes, and nothing consumed is re-prepared.

*(b) Abort bound.* As in `lem:s3-tree`(b),
Pr[some node aborts] ≤ Σ_j Pr[v_{j+1} aborts | 𝓔_j]. By (a), conditional on any record in 𝓔_j, the
bank of a zero-sum node v_{j+1} is i.i.d. uniform on K_d^⊥, of dimension a_d ≤ g_d. A.2 bounds
its abort term by (p^{a_d} − 1)/(2^{M_d} − 1) ≤ (p^{g_d} − 1)/(2^{M_d} − 1) ≤ τ_d. Under (Z-det)
the term is 0. There are S n_d such nodes, so they contribute at most S n_d τ_d = ε/(9(c−1)).
The grades in Γ_F ∪ Γ_0 are distinct elements of {2,…,c}, so there are at most c−1 of them, and

  Σ_{d∈Γ_F∪Γ_0} S n_d τ_d ≤ ε/9,

which is the same bound as before. The capped steps still give 3N·2^{−B} ≤ ε/9, with N
unchanged. So `lem:fc-forest`(b) holds with Γ_F replaced by Γ_F ∪ Γ_0 in the bank sum, and
the total stays ≤ 2ε/9.

*(c) The rest of the proof of (iii).* The proof of `thm:free-coordinate`(iii) is unchanged:
the rank failure ≤ ε/3, the hybrid over N_instr complete instruments ≤ ε/3, and the total
≤ 8ε/9. Indeed:
- N_instr = S(P + Σ_d n_d(M_d+1) + 1) counts the M_d central instruments and the conversion of
  every node, whatever its kind.
- `lem:s3-hybrid` lists "kernel computation, rejection sampling, …, conversion channel and
  abort branches" as ideal steps that preserve the canonical subspaces. The zero-sum search is a
  classical computation on the record, of the same kind.
- The query count is still c S ∏_d M_d.

The cost changes only at Γ_0. Replace t_S1 in `prop:fc-uniform`(b) by the time of one
zero-sum search. That is at most M_d·min(2^{M_d}, p^{g_d})·O(g_d log p) bit operations
(reachable sums), or (2^{M_d})·O(g_d log p) bit operations (exhaustive).

*Smallest failing instance.* None. No step of the argument fails. A natural place to look for
a failure was the claim that the label law survives a bank-dependent witness. Part D.3 tests
it exactly: every stage output equals ρ_{H_{d−1}} exactly, on all instances, including runs
where some zero-sum nodes abort and the run is discarded.

### B.3 Why this does not replace Schedule 1 in general (proved, by the cost formula)

For fixed c and a general profile, g_c can be of order m. Then p^{g_c} = (c+1)^{g_c} is
exponential in m, and so are both searches. (Z-rand) needs 2^{M} ≥ p^{g_c}/τ, and (Z-det)
reaches p^{a_c} reachable sums when a_c = g_c. Schedule 1 is polynomial in B_c(g_c) for fixed c.
So the zero-sum node is an option for profiles with small g_c, in particular under g_d ≤ r,
and the Scope paragraph's "falls back on Schedule 1" stays the default for general profiles.

## Part C. Corollary `cor:fpt-r`(ii) at p = c+1 through (iii) and the new node

### C.1 Statement (proved, conditional exactly as part (i))

*Claim (ii').* Let r = dim[L,L] ≥ 1 and p = c+1, with the class not fixed. Assume the
following, exactly as in part (i):
- the steps behind `thm:main`;
- `thm:free-coordinate`(iii), with Γ_0 run by the zero-sum node (B.1, either variant);
- the i.i.d. label law of fresh ideal sources, `lem:s3-law` (AI-checked).

Then the HSP of `def:input-contract` with a coherent oracle is solved with probability
≥ 1−ε, from 2^{O(r log(r+2))}·poly(m, log(1/ε)) oracle queries, in time
2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)). The internal cost of the oracle is charged
separately.

With fresh copies of ρ_H in place of the oracle, the same bound holds with copies in place of
queries. This is **argued**, not proved, for the same reason as in part (i):
`thm:free-coordinate`(iii) is stated for oracle input, and `lem:copy-lift` supplies the lifted
sources.

The imported IMS branch stays a valid alternative proof for coherent-oracle input. It is in
fact the *less* conditional one, since it uses no Rees step and no label law. What the new
branch adds is that IMS is no longer needed, that the corollary has one proof at every p > c,
and that coset-copy input is covered at p = c+1 at the same (argued) level as in part (i).
The IMS branch does not cover coset-copy input, because its certification evaluates f.

*Proof.*
1. *The grades.* As in (i), g_2 > … > g_c ≥ 1, c ≤ r+1 and a_d ≤ g_d ≤ r. At p = c+1 and
   d < c, κ_d = gcd(d, c) ≤ c/2 < p−1, so every grade d < c lies in Γ_F ∪ Γ_1, and Γ_0 = {c}.
2. *Grades d < c.* The bounds of the proof of (i) at these grades use only Lemma
   `lem:fc-choice`, ln(p/κ_d) ≥ ln 2 (true, since p/κ_d ≥ (c+1)/(c/2) > 2) and κ_d ≤ c. So they
   hold verbatim: M_d ≤ α + 3 log2 n_d at FCS grades and M_d = g_d + 1 ≤ α at linear grades, with
   α = (1+2log2 c) r + 3 log2(216cS) + 3 and ε = 1/3.
3. *Grade c.*
   - Under (Z-det), M_c = g_c c + 1 ≤ rc + 1 ≤ αc ≤ 4αc.
   - Under (Z-rand) with the explicit arity,
     M_c ≤ 2 + g_c log2(c+1) + log2(27(c−1)S) + log2 n_c ≤ α + log2 n_c, using
     log2(c+1) ≤ 1 + 2 log2 c and log2(27(c−1)S) + 2 ≤ 3 log2(216cS) + 3.
   In both cases M_c ≤ α + 3 log2 n_c, so the induction of (i) gives log2 n_d ≤ (d−2) log2(4αc)
   and M_d ≤ 4αc at every grade. Hence Q_1 = cS∏M_d ≤ cS(4αc)^{c−1} = 2^{O(r log(r+2))} S²,
   as in (i).
4. *Correctness of one run.* By B.2 (`lem:fc-forest` with the new node) and the unchanged rest
   of the proof of (iii), one run returns 𝔥 with probability ≥ 2/3.
5. *Time of one run.* The FCS and linear nodes cost what they cost in (i). The run has
   S n_c ≤ Q_1 zero-sum nodes.
   - Under (Z-det) each costs at most M_c (c+1)^{g_c}·O(r log p) ≤ (r(r+1)+1)(r+2)^r·O(r log p)
     bit operations (A.4).
   - Under (Z-rand) each costs at most 2^{M_c}·O(r log p) ≤ 4(r+2)^r·27(c−1)S n_c·O(r log p).
   Both are 2^{O(r log(r+2))}·poly(m, log p), since n_c ≤ Q_1.
   B ≤ log2(81Q_1) + 1 and the compilation of the ≤ 3Q_1 complete instruments are as in (i).
6. *Amplification.* Run R = ⌈18 ln(1/ε)⌉ independent runs and output the plurality subspace
   (Hoeffding, as in (i)). The vote evaluates no oracle. ∎

The dependence on the label law is the same as in (i). (Z-det) needs no label law *at grade c*,
but the FCS grades d < c still need it, so the corollary is conditional on `lem:s3-law` either
way.

### C.2 Exact numbers on the filiform profiles (exact computation)

Script: `theorems/rees_zero_sum_node.py` (output
`research/audits/reviews/2026-11-04-rees-zero-sum-node/zero_sum_budget.json`).
- *Profile.* Filiform, m = r+2, g_d = m−d (so g_c = 1), at ε = 1/3, with the least public FCS
  arities of rule (R1), exactly as in the fcs-budget report.
- *Grade c.* The rows differ only in the choice at grade c.
- *Reproduction.* The "S1" row reproduces the B.5 numbers 58.9 / 155.8 / 676.8 exactly.

| r, c, p | S | grade-c rule | M_c | log2 Q | log2 |G'| (IMS) | log2 bank term at c (S n_c × β_c) | zero-sum search steps, log2 (exh. / reach.) |
|---|---|---|---|---|---|---|---|
| 3, 4, 5 | 7 | S1, B_4(1) | 2^48 | 58.9 | 7.0 | 0 | — |
| | | Z-rand least | 18 | 15.0 | | −7.15 (β_c = 2^{−16.0}) | 26.9 / 15.3 |
| | | Z-rand explicit | 19 | 15.1 | | −8.15 | 27.9 / 15.4 |
| | | **Z-det** | **5** | **13.2** | | 0 | 13.8 / 13.5 |
| 5, 6, 7 | 9 | S1, B_6(1) | 2^134.3 | 155.8 | 14.0 | 0 | — |
| | | Z-rand least | 29 | 26.3 | | −7.5 | 47.9 / 26.6 |
| | | Z-rand explicit | 30 | 26.4 | | −8.5 | 48.9 / 26.6 |
| | | **Z-det** | **7** | **24.3** | | 0 | 25.9 / 24.5 |
| 9, 10, 11 | 12 | S1, B_10(1) | 2^637.9 | 676.8 | 31.1 | 0 | — |
| | | Z-rand least | 47 | 44.4 | | −8.1 | 82.5 / 44.6 |
| | | Z-rand explicit | 48 | 44.4 | | −9.1 | 83.5 / 44.6 |
| | | **Z-det** | **11** | **42.3** | | 0 | 46.5 / 42.5 |

Columns:
- *Search steps.* The total number of vector additions over all S n_c zero-sum nodes of one
  run: S n_c (2^{M_c} − 1) for the exhaustive search, and S n_c M_c min(2^{M_c}−1, p^{g_c}) for
  the reachable-sum search, at the worst case a_c = g_c. These are worst-case caps.
- *Other grades.* These are unchanged from the fcs-budget computation:
  - the grade arities, e.g. r = 9: (23, 9, 26, 52, 30, 5, 33, 3) at d = 2..9;
  - B = 10 / 19 / 36;
  - the largest FCS per-node trial cap, 2^{6.0} / 2^{9.6} / 2^{16.9};
  - the total FCS trial cap per run, 2^{8.8} / 2^{20.0} / 2^{37.3}.
- *Error budget.* It holds exactly in every row: rank ≤ ε/3, bank sum ≤ ε/9 (it is
  2^{−5.8}, 2^{−5.6}, 2^{−5.9} for Z-rand, against ε/9 = 2^{−4.75}), and capped ≤ ε/9.

Readings:
1. *Compared with Schedule 1.* The zero-sum node cuts log2 Q from 58.9 / 155.8 / 676.8 to
   13.2 / 24.3 / 42.3. That is a cut of 46 / 132 / 634 bits.
2. *Z-det against Z-rand.* On filiform profiles g_c = 1, so Z-det needs only p columns. This is
   the prefix-sum pigeonhole in F_p. Z-det beats Z-rand, whose arity carries log2(1/τ_c)
   ≈ 15 / 26 / 43 bits. Z-rand is smaller only when g_c(p−1−log2 p) > log2(1/τ_c) + O(1),
   which needs large g_c.
3. *Against IMS.* The node does not beat IMS's |G'| = p^r on these profiles: 2^{13.2} queries
   against a 2^{7.0} time term at r = 3, and 2^{42.3} against 2^{31.1} at r = 9. The
   comparison is loose, because IMS's time is poly(input) + |G'| with unstated polynomial
   factors. Both are 2^{O(r log r)}. The point of the node is to remove the import, not to
   beat it.

## Part D. Exact checks and simulations

All scripts are in `research/audits/reviews/2026-11-04-rees-zero-sum-node/`, and all were run
niced, one at a time.

### D.1 The probability bound (exact computation)

`check_probability.py` writes `check_probability_out.json` and `check_probability_log.txt`.
It reports **ALL OK**.

1. *Exact probabilities.* For 66 cases (p ∈ {2,3,5,7}, a ≤ 3, M ≤ 6) it computes
   Pr[no nonempty zero-sum subset] exactly. The method is a dynamic programme over the set of
   nonempty subset sums, with the first label fixed to e_1 by GL(a,p)-invariance. Every case
   satisfies Pr ≤ (p^a−1)/(2^M−1). Every case with M ≥ a(p−1)+1 has Pr = 0 exactly. Skipped:
   (5,3,5) and (5,3,6), whose state count exceeds 2·10^6, and p = 7, a = 3.
   Examples:
   - (5,1,4): 4/625, the four constant sequences;
   - (7,2,6): 3288027504/13841287201 ≈ 0.2376, against the bound 0.762;
   - (3,3,6): ≈ 0.0578, against 0.413.
2. *Independent cross-check.* Full enumeration of all p^{aM} banks in 7 cases ((2,1,4),
   (2,2,4), (3,1,5), (3,2,4), (5,1,4), (5,2,3), (7,1,3)). It reproduces the same probability,
   and E X and E X² equal the formulas of A.2 exactly.
3. *Pairwise independence.* For every pair of distinct nonempty subsets T, T',
   (Σ_T, Σ_{T'}) is exactly uniform on (F_p^a)². Cases (p,a,M) = (3,1,3), (2,2,3), (5,1,3);
   all 21 pairs in each.
4. *Tightness of (Z-det).* The tight zero-sum-free bank at M = a(p−1) is confirmed by both
   searches in 6 cases.

The bound is loose by a factor of 2–7 at these sizes, and it is > 1 (vacuous) for small M.
Only its use at M ≈ g log2 p + log2(1/τ) matters.

### D.2 The node alone (float check, Monte Carlo)

`simulate_node.py 1` writes `simulate_node_part1.json`. There are 9 cases of (p, g, a, M),
20000 banks each. Each bank uses a random subspace of dimension a in F_p^g, given by a random
full-rank basis.
- The exhaustive and reachable-sum searches always agree on existence.
- Every returned s passes the exact (F5) check at d = p−1.
- The abort frequency is within 4 standard errors of the exact probability wherever that was
  computed. Examples: 0.23625 against 0.23755 at (7,2,2,6), and 0.0192 against 0.0190 at
  (11,1,1,5).
- It is 0 in the Davenport regime (5,1,1,7) and (3,2,2,9).

### D.3 The whole recursion (exact computation on the states, sampled labels)

`simulate_node.py 2` writes `simulate_node_part2.json`. It uses the exact simulator
`theorems/rees_end_to_end_ext.py`, imported read-only, and passes it custom schedules and a
custom solver.
- *Arities and solvers.* The zero-sum node runs at the top grade d = c = p−1. Lower grades use
  the Chevalley–Warning arity κ_d g_d + 1 with the round-1 brute-force solver, a test solver
  and not FCS.
- *Seeds.* Two per instance.

| group (c, p) | grade-c node | M_c | runs | aborted | recovered 𝔥 | every stage output = ρ_{H_{d−1}} exactly | every measured law uniform on K_d^⊥ |
|---|---|---|---|---|---|---|---|
| Heis(F_3) (2, 3) | Z-det | 3 | 14 | 0 | 14 | 14 | 14 |
| Heis(F_3) | Z-rand, τ = 1/8 | 6 | 14 | 0 | 14 | 14 | 14 |
| Heis(F_3) | M = 2 (abort path) | 2 | 14 | 4 | 10 | 10 | 10 |
| n5(F_5) (4, 5), the r = 3 filiform | Z-det | 5 | 18 | 0 | 18 | 18 | 18 |
| n5(F_5) | Z-rand, τ = 1/8 | 7 | 18 | 0 | 18 | 18 | 18 |

Notes on the table:
- *Instances.* The n5 rows cover 9 hidden subgroups, 7 of them with a nontrivial top-grade
  label support of size 5. The Heis rows cover 7 subgroups.
- *Support sizes.* The witnesses' support sizes at grade c show that the search did more than
  pick a zero label. At n5 with Z-det they were 1: 2107, 2: 889, 3: 315, 4: 91.
- *The abort path.* The M = 2 row runs the abort path deliberately. An aborted run outputs
  ABORT and is not retried inside the run. All non-aborted runs, which are conditioned on every
  zero-sum node's non-abort, are still exact at every stage. This is the finite form of B.2(a).
- *Scope.* These are finite runs on two groups. They can falsify and did not. They prove
  nothing for other (G, H).

### D.4 Tests

`tests/test_rees_zero_sum_node.py`: **25 passed** in 0.3 s. It covers the witness
equivalence (A.1), the moments and the bound by enumeration, the Davenport arity and its
tightness, agreement of the two searches, the arities, and the filiform budgets, including
the reproduction of the B.5 numbers.

## The exact statement that now holds

AI-checked, pending human review. All of it is conditional exactly as stated.

1. **(proved)** `lem:fc-zero-sum`. Let d have κ_d = p−1 (so d = p−1 = c, and p ≥ 3).
   - (a) For M i.i.d. uniform labels on a subspace of dimension a, Pr[no nonempty zero-sum
     subset] ≤ (p^a−1)/(2^M−1).
   - (b) M = 1 + ⌈log2(p^{g_d}/τ)⌉ makes this < τ for every a ≤ g_d. For **every** bank in
     F_p^{g_d}, M = g_d(p−1)+1 columns contain a nonempty zero-sum subset (Chevalley–Warning),
     and this is tight.
   - (c) A zero-sum subset T is found, or shown not to exist, deterministically, in 2^M or in
     M·min(2^M, p^{a}) vector additions, and s = 1_T is a valid nonzero witness of
     (sde-target).
   - (d) The node's output is exactly ρ_{H_{d−1}} on every non-aborting record.
2. **(proved)** `lem:fc-forest`(a) and (b), and hence `thm:free-coordinate`(iii), hold with Γ_0
   run by either zero-sum node. The bank sum is over Γ_F ∪ Γ_0, and the error split is
   unchanged.
3. **(proved, conditional as part (i))** `cor:fpt-r`(ii'): at p = c+1, through (iii) and the
   node, the HSP with a coherent oracle is solved in 2^{O(r log(r+2))}·poly(m, log(1/ε))
   queries and 2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)) time. The conditions are the steps
   behind `thm:main`, (iii), and `lem:s3-law`. Coset-copy input is **argued**, as in (i).
4. **(exact computation)** On the filiform profiles r = 3/5/9 at p = 5/7/11, the node at
   M_c = p gives log2 Q = 13.2/24.3/42.3, against 58.9/155.8/676.8 with Schedule 1.

## What is still missing

- Human review of everything above, and of `lem:s3-law`, on which the FCS grades still depend.
- A proof of `thm:free-coordinate`(iii) for coset-copy input. It is still argued, for (i) and
  (ii) alike.
- For general profiles at fixed c, efficient zero-sum *finding* at the Davenport arity. Both
  searches cost p^{Θ(a_c)}, so Schedule 1 stays the default there. This is the "o(a²) SDE
  finding" item, unchanged.
- The owner's decision whether to adopt the proposed text. It changes the stated scope of
  `cor:fpt-r`(ii), which is the owner's call.

## Claim gates that must stay false

All Rees claim gates stay false: no human-reviewed claim, no novelty or priority claim, no
quantum-advantage or native-application claim, no outreach, and no registry promotion. The node
does not make `cor:fpt-r`(ii) less conditional than the IMS branch. It is strictly *more*
conditional for oracle input. It must not be described as removing a hypothesis.

## Proposed paper text

Status label for all items: *AI-checked, pending human review.* Nothing below has been applied.

**P1.** Target: `docs/papers/rees-hsp/appendix-free-coordinate.tex`, a new lemma immediately
before `\begin{lemma}[Mixed trees]` (`lem:fc-forest`).

```latex
\begin{lemma}[Zero-sum node; AI-checked, pending human review]
\label{lem:fc-zero-sum}
Let $d \in \Gamma_0$, so $d = p-1 = \kappa_d$, and $s^d \in \{0,1\}$ with $s^d = 1$ exactly when $s \ne 0$. A \emph{zero-sum node} of arity $M$ measures its bank as in (F1), searches the nonempty $T \subseteq \{1,\dots,M\}$ for one with $\sum_{i\in T}\lambda_i = 0$, aborts if there is none, and otherwise puts $s = \mathbf{1}_T$, checks as in (F5) and converts as in (F6).
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item If $\lambda_1,\dots,\lambda_M$ are independent and uniform on a subspace of dimension $a$, the node aborts with probability at most $(p^a-1)/(2^M-1)$.
  \item If $M = g_d(p-1)+1$, every bank in $\Fp^{g_d}$ has a nonempty zero-sum subset, so the node never aborts.
  \item The search is deterministic and costs at most $M\min(2^M,p^{g_d})$ additions in $\Fp^{g_d}$. The node draws no coins and, after (F1), consumes no quantum source.
  \item On every record that does not abort, $s$ is a nonzero witness of~\eqref{eq:sde-target}, and the output and the joint state are as in Lemma~\ref{lem:fc-node}(d).
\end{enumerate}
\end{lemma}

\begin{proof}
A nonzero $s$ satisfies $\sum_i s_i^d\lambda_i = 0$ exactly when $T = \{i : s_i \ne 0\}$ is nonempty with $\sum_{i\in T}\lambda_i = 0$, which gives~(d) together with Proposition~\ref{prop:descent}, exactly as in the proof of Lemma~\ref{lem:fc-node}(d).
(a) Write $\lambda_i = Ex_i$ with $E$ injective and $X = [x_1\cdots x_M]$ uniform in $\Fp^{a\times M}$, so $\sum_T\lambda_i = 0$ if and only if $X\mathbf{1}_T = 0$. For $T \ne \emptyset$, $X\mathbf{1}_T$ is uniform on $\Fp^a$. For distinct nonempty $T, T'$ the vectors $\mathbf{1}_T$ and $\mathbf{1}_{T'}$ are linearly independent (two nonzero $0/1$ vectors are proportional only if their supports agree), so $(X\mathbf{1}_T, X\mathbf{1}_{T'})$ is uniform on $\Fp^a\times\Fp^a$, as in the proof of Lemma~\ref{lem:s3-moment}(b). The number $Z$ of zero-sum nonempty subsets is therefore a sum of $2^M-1$ pairwise independent indicators of mean $p^{-a}$, and Chebyshev's inequality gives $\Pr[Z=0] \le \operatorname{Var}Z/(\mathbb{E}Z)^2 = (p^a-1)/(2^M-1)$.
(b) The $g_d$ polynomials $f_j(s) = \sum_i\lambda_{ij}s_i^{p-1}$ have degree sum $g_d(p-1) < M$. By the Chevalley--Warning theorem their number of common zeros in $\Fp^M$ is divisible by $p$, and $s = 0$ is one, so there is a common zero $s \ne 0$.
(c) Keep the set $R_j$ of sums of nonempty subsets of $\lambda_1,\dots,\lambda_j$, with one subset per value. Then $R_{j+1} = R_j \cup \{\lambda_{j+1}\} \cup (R_j + \lambda_{j+1})$, a zero-sum subset exists if and only if $0 \in R_M$, and $|R_j| \le \min(2^j, p^{g_d})$.
\end{proof}

By~(a), $M_d = 1 + \lceil\log_2(p^{g_d}/\tau_d)\rceil$ bounds the abort probability by $\tau_d$ for every $a_d \le g_d$. For $g_d \le r$ and $p = c+1 \le r+2$ the search costs $2^{O(r\log(r+2))}$; for general profiles $p^{g_d}$ can be exponential in $m$, and Schedule~1 remains the polynomial choice at fixed $c$.
```

**P2.** Target: same file, (R1). After "if $d \in \Gamma_0$, $M_d = B_d(g_d)$" insert:

```latex
, or, as a public alternative, a zero-sum node (Lemma~\ref{lem:fc-zero-sum}) with $M_d = g_d(p-1)+1$, or with $\tau_d = \eps/(9(c-1)Sn_d)$ and any $M_d$ with $(p^{g_d}-1)/(2^{M_d}-1) \le \tau_d$
```

**P3.** Target: same file, proof of `lem:fc-forest`.
- In (a), after "deterministically, as in the proof of Theorem~\ref{thm:main}." insert:

```latex
If $d \in \Gamma_0$ runs a zero-sum node, Lemma~\ref{lem:fc-zero-sum}(d) gives the output $\rho_{H_{d-1}}$, in product, on every non-aborting record; its witness reads only its own bank, which no later step reads, and the parent measures different registers, as in Remark~\ref{rem:s3-caveat}.
```

- In (b), replace "Nodes in $\Gamma_1\cup\Gamma_0$ contribute zero." with:

```latex
Nodes in $\Gamma_1$, Schedule~1 nodes and zero-sum nodes of arity $g_d(p-1)+1$ contribute zero; any other zero-sum node of grade $d$ contributes at most $\tau_d$, by~(a) and Lemma~\ref{lem:fc-zero-sum}(a), and has no capped step.
```

- Read the sum in (b) and in the statement of `lem:fc-forest`(b) over $\Gamma_{\mathrm F}\cup\Gamma_0$ (where a zero-sum node is used), with "since $|\Gamma_{\mathrm F}\cup\Gamma_0| \le c-1$".

**P4.** Target: same file, Scope paragraph. Replace "and at the zero-sum grade
$\kappa_d = p-1$ it falls back on Schedule~1" with:

```latex
and at the zero-sum grade $\kappa_d = p-1$ it falls back on Schedule~1 or on the zero-sum node of Lemma~\ref{lem:fc-zero-sum}, whose search costs $p^{O(g_d)}$
```

**P5.** Target: `docs/papers/rees-hsp/main.tex`, `cor:fpt-r`, item (ii). Replace it with:

```latex
  \item If $p = c+1$, the conclusion of~(i) holds under the same conditions, with Theorem~\ref{thm:free-coordinate}(iii) run with the zero-sum node of Lemma~\ref{lem:fc-zero-sum} at the grade $d = c$ (for coset-copy input this is argued, not proved). For a coherent oracle the same time bound also follows from an imported algorithm with no Rees step and no label law.
```

**P6.** Target: `main.tex`, proof of `cor:fpt-r`. Insert a new first paragraph of (ii) before
"If $p = c+1$, then $c \le r+1$ gives":

```latex
(ii) If $p = c+1$, every grade $d < c$ has $\kappa_d = \gcd(d,c) \le c/2 < p-1$, so the bounds of~(i) hold there verbatim, and $\Gamma_0 = \{c\}$. Run the grade $c$ with the zero-sum node of Lemma~\ref{lem:fc-zero-sum} at $M_c = g_cc + 1 \le rc + 1 \le 4\alpha c$; it never aborts, and Lemma~\ref{lem:fc-forest} holds with it. The induction of~(i) is unchanged, so $Q_1 \le cS(4\alpha c)^{c-1} = 2^{O(r\log(r+2))}S^2$. Each of the at most $Q_1$ zero-sum nodes costs at most $M_c(c+1)^{g_c}\poly(r,\log p) \le (r^2+r+1)(r+2)^r\poly(r,\log p)$ by Lemma~\ref{lem:fc-zero-sum}(c). Amplify, compile and count as in~(i). Alternatively, for a coherent oracle:
```

and keep the existing IMS paragraph after it as the alternative proof.

**P7.** Target: `main.tex`, the paragraph after the proof of `cor:fpt-r`. Replace "this is why
part~(ii) is imported." with:

```latex
the zero-sum node of Lemma~\ref{lem:fc-zero-sum} replaces it there at arity $g_c(p-1)+1$, at a classical search cost $p^{O(g_c)} = 2^{O(r\log(r+2))}$. On the filiform profiles $r = 3, 5, 9$ at $p = c+1$ this gives $\log_2 Q = 13.2$, $24.3$ and $42.3$, against $58.9$, $155.8$ and $676.8$ with Schedule~1 (exact computation, \file{research/audits/reviews/2026-11-04-rees-zero-sum-node/}; AI-checked, pending human review).
```
