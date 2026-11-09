# Rees Schedule 3 without 2^128 rejection trials (campaign 2, item 6)

AI session only (Claude Code, 2026-11-02). No human review. Edits nothing outside this report
and `2026-11-02-rees-schedule3-cost/`. Builds on `main.tex` Thm `thm:random-column` (lines
465–477), the core check `2026-11-01-rees-core-proof-check.md` §5.5, and the combined-schedule
report `2026-11-02-rees-combined-schedule.md` (§2.3 label law in mixed trees, §3 budgets).

Scripts and outputs (folder `2026-11-02-rees-schedule3-cost/`):

```bash
cd research/audits/reviews/2026-11-02-rees-schedule3-cost && /opt/anaconda3/bin/python -B -u fcs_exact.py > fcs_exact_out.txt
cd research/audits/reviews/2026-11-02-rees-schedule3-cost && /opt/anaconda3/bin/python -B -u fcs_budget.py > fcs_budget_out.txt
```

`fcs_exact.py` takes about 15 minutes and `fcs_budget.py` about 1 minute. Both assert their claims.
`fcs_budget.py` imports `../2026-11-02-rees-schedules/combined/combined_budget.py` for Rule W
and the old W+3 numbers.

## 0. Verdict

- **The 2^128 is not intrinsic to Schedule 3. It is intrinsic to the sampler.** The old sampler
  draws a uniform kernel vector, so every one of its M coordinates must land in
  D = P_κ ∪ {0} by luck. The mean acceptance over banks is exactly (q^{M−r} − p^{−(M−r)})q^r
  ≈ q^M ≈ κ^{−M}, with q = (h+1)/p. So that design needs about κ^M trials on almost every bank
  (§6, Prop. 6.1, proved). At M = 4u this is the 2^128.
- **Fix: free-coordinate sampling (FCS). Proved, AI-checked, pending human review.**
  1. Draw the free coordinates directly in P_κ, as b^κ with b uniform, on the columns after
     the last pivot.
  2. Set the other free columns to 0.
  3. Leave only the r pivot coordinates to chance.

  A second-moment argument on the reduced row echelon form shows the following. Outside a
  bank event of public probability β, each trial is accepted with probability at least
  q^r/2 ≥ 1/(2κ^r). Here r ≤ a_d is the observed rank, and the trials reuse the same saved
  bank (Thm 3.1). The hypotheses are unchanged: labels i.i.d. uniform on the unknown K_d^⊥, and
  witness verified exactly. **No condition p ≥ 16u² is needed. The only requirement is h ≥ 2,
  that is κ_d < p − 1**, which fails only at the zero-sum grade d = c = p − 1.
- **Drop-in (Thm 4.1).** Keep the paper's hypotheses and arity M = 4u, and take n_0 = 2u+1. The
  tree-restart part (ii) holds unchanged, while the trials per node fall from 4κ^{4u}B to
  ⌈2B ln2·q^{−r}⌉ ≤ 2B·u^{u−1}+1. At the class-9 profile with one u = 18 tree, the maximum per
  node drops from 2^{223.8–236.0} to 2^{31.6–34.3} (exact, `fcs_budget_out.txt`).
- **The arity can drop too (Thm 5.1).** The acceptance no longer depends on M, so M_d can be
  the least public arity whose bank bound meets a node-count-weighted target. That arity is
  g_d + O(1 + (g_d log κ_d + log(1/τ))/log(p/κ_d)), usually g_d + 2 to g_d + 6 at large p. With
  the union-bound error split of Schedules 1–2 (no tree restarts) at the class-9 profile:

  | p | Rule W log₂Q | old W+3 log₂Q / max log₂ trials per node | **W+FCS log₂Q / max log₂ trial cap per node / log₂ total trials** |
  |---|---|---|---|
  | 11 | 202.1 | n/a (p < 16u²) | **42.3 / 28.3 / 47.0** |
  | 1031 | 167.3 | n/a | **36.6 / 33.4 / 50.8** |
  | 5281 | 852.3 | 50.3 / 128.2 | **39.1 / 33.8 / 52.2** |
  | 2^61−1 | 555.4 | 52.9 / 128.3 | **34.1 / 33.5 / 51.0** |
  | 2^127−1 | 61.5 | 49.9 / 115.2 | **34.0 / 31.0 / 49.5** |

  So the classical work is at most about 2^34 trials per node and about 2^51 trials in total.
  Queries fall below both Rule W and the old W+3, at every prime tested, including p = 11
  and p = 13.
- **Splitting the bank into blocks (Prop 5.3, proved).** Solve a public block of coordinates
  first. Each level-one output is then again i.i.d. uniform on V ∩ ker π₁ (exact check, Part D).
  So a k-level FCS has arity ∏_j M_j and per-node cost about Σ_j (nodes at level j)·κ^{g_j}, with
  Σ g_j = g. This trades queries for classical time: capping trials at 2^30 per node costs
  +2.5 to +11 bits of queries.
- **Lower bound (Prop 6.2, proved).** Call a design *bank-oblivious* if it picks free-coordinate
  values without looking at the bank's entries. FCS is one. Every such design succeeds within
  T trials with probability at most T·q^a + 2p^{a−M} + 1/(p−1), averaged over banks. So
  q^{−a} ≈ κ^a trials are necessary, and FCS-1 is optimal in this class up to the factor 2B ln 2.
  Adaptive designs escape this bound: sorting at a = 1, and multi-level FCS. Whether an adaptive
  method beats κ^{a−o(a)} at arity a + O(1) is open (§6.3).
- **Not given:** polynomial classical time. FCS is still 2^{Θ(a_d log κ_d)} per node in the worst
  case a_d = g_d. The zero-sum grade κ_d = p−1 (h = 1) is untouched.

## 1. Setting, notation, access model

Stage-d node, d ∈ {2..c}, κ = κ_d = gcd(d, p−1), h = (p−1)/κ, P_κ = {x^κ : x ∈ F_p^×}
(|P_κ| = h), D = P_κ ∪ {0}, q = (h+1)/p = Pr[u ∈ D] for u uniform on F_p. Note
q = (p−1+κ)/(κp) ≥ 1/κ and q^{−1} = κ/(1 + (κ−1)/p).

Input: M measured labels λ_1..λ_M ∈ F_p^{g}, with g = g_d public. **Label-law hypothesis** (as in
main.tex Thm random-column, from Lemma `lem:central`, and for mixed trees from combined §2.3):
the labels are i.i.d. uniform on an unknown subspace V = K_d^⊥ of dimension a = a_d ≤ g, and
independent of every earlier record. Target: s ∈ F_p^M, s ≠ 0, with Σ_i s_i^d λ_i = 0. After the
gcd reduction this means y_i = s_i^κ ∈ D with Σ y_i λ_i = 0 and y ≠ 0 (core check §5.2–5.3).
Bezout: t ≡ (d/κ)^{−1} mod h exists since gcd(d/κ, h) = 1. For σ ≠ 0, (σ^t)^d = σ^{κ(1+jh)} = σ^κ.

Forbidden knowledge: H, K_d, a_d. Every arity and threshold below uses only (p, d, g_d, ε, m, c).

## 2. The free-coordinate sampler FCS(M, n_0, B)

1. Form Λ = [λ_1 … λ_M] (g × M). Compute its RREF R, with rank r and pivots p_1 < … < p_r. Let
   F' = {p_r+1, …, M} (all of {1..M} if r = 0) and n' = |F'|. **Abort if n' < n_0.**
2. Repeat up to T_r = ⌈2B ln 2 · q^{−r}⌉ times:
   1. Draw b_j uniform in F_p^× for j ∈ F', independently, and put x_j = b_j^κ. This is uniform
      on P_κ, since b ↦ b^κ is κ-to-1.
   2. Compute v_i = −Σ_{j∈F'} R_{ij} x_j for i = 1, 2, …, stopping at the first v_i ∉ D. The test is
      v_i = 0 or v_i^h = 1.
   3. If every v_i ∈ D, set y_j = x_j on F', y_{p_i} = v_i, and y_j = 0 on the remaining columns;
      then stop.
3. Set σ_j = b_j on F', take σ_{p_i} as a κ-th root of v_i (Las Vegas, capped) or 0, and σ = 0
   elsewhere. Put s = σ^t (Bezout) and verify Σ s_i^d λ_i = 0 exactly.

Cost: one RREF, O(gM·min(g, M)) field operations. Then at most T_r trials, each costing
n' exponentiations by κ plus at most r·(n' + 2 log₂ p) multiplications. Finally r root extractions,
poly(κ, log p) each. The three capped random steps are the trial loop, the root extractions,
and fair-bit sampling of F_p^×. Each is capped at failure 2^{−B} per node, exactly as in main.tex
(ii).

## 3. One node

**Theorem 3.1 (proved; AI-checked, pending human review).** Assume the label law, h ≥ 2,
n_0 ≥ 1 and L := M − n_0 ≥ 0. Put
β(M, n_0; a) = 4 / (h^{n_0−1} q^{a}) + (p^{a} − 1)/((p−1) p^{L}). The bound β is increasing in a,
so β(M, n_0; g) is a public bound. Then:

1. With probability at least 1 − β over the bank, step 1 does not abort, and each trial of step 2
   is accepted with probability at least q^r/2 ≥ 1/(2κ^r), independently given the bank.
2. On that event step 2 fails with probability at most (1 − q^r/2)^{T_r} ≤ e^{−T_r q^r/2} ≤ 2^{−B}.
   Its expected number of trials is at most 2q^{−r} ≤ 2κ^r.
3. Every output s is nonzero, satisfies Σ s_i^d λ_i = 0, and depends only on the bank and the node's
   own coins. No further quantum sources are used.

*Proof.*

**(a) Reduction to a uniform matrix.** Fix an injective E : F_p^a → V and write λ_i = Eα_i.
Then the α_i are i.i.d. uniform on F_p^a and Λ = EA with A = [α_1 … α_M]. E is injective, so
ker Λ = ker A, and the row space of Λ equals the row space of A: EA's rows are combinations
of A's rows, and the ranks agree. So the nonzero rows of RREF(Λ) are RREF(A).

**(b) Law of the RREF.** The law of A is invariant under A ↦ AG for G ∈ GL_M(F_p), and so is
the rank. GL_M acts transitively on the Grassmannian Gr(r, M), so the row space W is uniform on
Gr(r, M) conditional on rank r. RREF is a bijection from Gr(r, M) onto RREF matrices. Those with
pivot pattern π = (p_1..p_r) are the matrices with
- R_{i,p_i} = 1,
- R_{i,j} = 0 for j < p_i and for pivot columns j ≠ p_i,
- all other entries free.

That set is a copy of F_p^{f(π)}. So conditional on (r, π) the free entries are i.i.d. uniform. Every
entry in a column j > p_r is free. Hence **C := −R_{·,F'} is uniform on F_p^{r×n'} given (r, π).**
Exact check (Part B): R[:, F'] is exactly uniform for every pivot pattern, over every bank in seven
exhaustive cases.

**(c) Pivot event.** If n' < n_0 then p_r > L, so the first L columns of A have rank < r ≤ a. Then
Pr ≤ Σ_{[v]∈P(F_p^a)} Pr[vᵀA_{[L]} = 0] = ((p^a−1)/(p−1))·p^{−L}.

**(d) Second moment.** Fix (r, π) with n' ≥ n_0, and let N = #{x ∈ P_κ^{n'} : Cx ∈ D^r}. These are
exactly the accepted draws.
- *Mean.* For x ≠ 0, Cx is uniform on F_p^r, so Pr[Cx ∈ D^r] = q^r and E N = h^{n'} q^r.
- *Independent pairs.* If x, x' are linearly independent, (Cx, Cx') is uniform on (F_p^r)²: each
  row c of C gives (c·x, c·x') uniform on F_p², and the rows are independent. So the two indicators
  are independent and have covariance 0.
- *Proportional pairs.* If x' = tx with both in P_κ^{n'}, then t ∈ P_κ (compare one coordinate;
  n' ≥ 1). Since tD = D, Cx' ∈ D^r ⇔ Cx ∈ D^r. Each x has exactly h such partners, including itself.

Hence Var N = Σ_x Σ_{x'∝x} (Pr_x − Pr_x²) ≤ h·E N. By Chebyshev,
Pr[N < EN/2] ≤ 4h/E N = 4/(h^{n'−1} q^r) ≤ 4/(h^{n_0−1} q^a), using n' ≥ n_0, h ≥ 1, r ≤ a and
q ≤ 1. Outside this event the acceptance is N/h^{n'} ≥ q^r/2. Draws are i.i.d. given the bank, so
(2) follows; q ≥ 1/κ gives the κ forms.

**(e) Witness.** R y = 0 row by row: y_{p_i} + Σ_{j∈F'} R_{ij} y_j = 0, and y vanishes on the other
non-pivot columns. So y ∈ ker Λ. Also y ≠ 0, because n' ≥ 1 and y_j ∈ P_κ on F'. Then
s_i^d = σ_i^κ = y_i, so Σ s_i^d λ_i = Λy = 0. ∎

Nothing here uses r = a, p ≥ 16u², or M = 4u. The old proof needed p ≥ 16u² only to make μ large
at M = 4u. Here μ_FCS = h^{n'−1}q^r grows by a factor h with each extra free column.

## 4. Drop-in replacement for main.tex Theorem random-column

**Theorem 4.1 (proved; AI-checked, pending human review).** Keep main.tex's hypotheses: u ≥ 2,
c ≤ u, a_d ≤ u − 1, p ≥ 16u², and M = 4u at every grade. Use FCS with n_0 = 2u + 1 (so L = 2u − 1).

1. *Per node.* β ≤ 4·15^{−2u}u^{−u−1} + 2p^{−u−1}, and step 2 uses at most ⌈2B ln 2·q^{−r}⌉ ≤
   2B ln 2·u^{u−1} + 1 trials. Compare the old 4κ_d^{4u}B.
2. *Tree.* With B = ⌈log₂(64(4u)^{c−1})⌉, the bank events sum to at most 1/64 over the at most
   (4u)^{c−1} nodes of a tree. The three capped failures add at most 3/64. So one tree aborts with
   probability at most 1/16, and main.tex (ii) holds verbatim: 4m' trees, keep m', total cost
   2^{O(u log(u+2))}·poly(m, log p, log 1/ε).

*Proof.* The bound h = (p−1)/κ ≥ (16u²−1)/u ≥ 15u holds since κ ≤ c ≤ u, and q ≥ 1/κ ≥ 1/u.
1. *Second-moment term:*
   h^{n_0−1}q^{a} ≥ (15u)^{2u} u^{−(u−1)} = 15^{2u}u^{u+1}.
2. *Pivot term:* (p^a−1)/((p−1)p^L) ≤ 2p^{a−1−L} ≤ 2p^{−u−1}, using a ≤ u−1 and L = 2u−1.
3. *Tree sum:* (4u)^{u−1}(4·15^{−2u}u^{−u−1} + 2(16u²)^{−u−1}) ≤ 1/64. This holds for all u ≥ 2:
   the first part is ≤ (4/225)^u·u^{−2} and the second is far smaller. It is exact-checked for
   2 ≤ u ≤ 60.
4. *Trials:* q^{−r} ≤ κ^r ≤ u^{u−1}.

The rest is main.tex (ii) word for word, including Hoeffding on 4m' trees and the fact that kept trees
output i.i.d. ρ_th by (2d) of the core check. ∎

Exact (`fcs_budget_out.txt`, one u = 18 tree at the class-9 profile, B = 56, 10171889243785
nodes per tree):

| p | log₂ bank sum per tree | max log₂ trials/node, FCS | old 4κ^M B |
|---|---|---|---|
| 5281 | −234.9 | 34.3 | 223.8 |
| 105019 | −316.9 | 31.6 | 193.9 |
| 2^31−1 | −589.0 | 31.6 | 236.0 |
| 2^61−1 | −1159.0 | 34.1 | 236.0 |
| 194522647344910884721 (≡ 1 mod 2520) | −1280.6 | 34.3 | 236.0 |
| 2^127−1 | −2413.0 | 31.6 | 236.0 |

Downstream uses carry over unchanged because the asymptotic form 2^{O(u log(u+2))} is unchanged:
the derived-dimension corollary (main.tex line 570, u = r+1) and the hidden-codimension
corollary (ii) (line 585, u = 2k, M = 8k = 4u).

## 5. Every prime, public arities, and bank splitting

**Theorem 5.1 (W+FCS rule; proved modulo the inherited hypotheses).** Fix ε. Let t = ⌈log_p(3/ε)⌉,
S = m + t, and n_d = ∏_{2≤d'<d} M_{d'}. Choose grades in the order d = 2, …, c:

- κ_d = 1: linear schedule, M_d = g_d + 1 (deterministic).
- κ_d = p − 1, so h = 1 (only at d = c = p−1): Rule W's choice.
- otherwise: FCS with τ_d = ε/(9(c−1) S n_d) and any (M_d, n_0) with β(M_d, n_0; g_d) ≤ τ_d. One
  explicit choice is
  n_0 = 1 + ⌈(g_d log(1/q) + log(8/τ_d))/log h⌉ and M_d = n_0 + g_d + ⌈log_p(2/τ_d)⌉.
  The tables use the least such M_d.

  The rule may also use Rule W's choice whenever its arity is smaller.

Cap each sampler node's three random steps at 2^{−B}, with B = ⌈log₂(27N/ε)⌉ and N the number
of sampler nodes. Then the composition of main.tex §`sec:recursion` returns 𝔥 with probability at
least 1 − ε, using Q = c·S·∏_d M_d queries. The error splits as
- rank ≤ ε/3,
- Schedule-2 Las Vegas ≤ ε/9,
- bank events ≤ Σ_d S n_d τ_d ≤ ε/9,
- capped steps ≤ 3N·2^{−B} ≤ ε/9,
- approximation ≤ ε/3.

*Proof.* The explicit choice gives 4/μ ≤ τ/2 by construction. For the pivot term,
(p^g−1)/((p−1)p^L) < p^{g−L}/(p−1) ≤ τ/2. The run fails only if some node aborts or the rank
step fails. Each node's abort event is a function of its record. By (2d) of the core check, the state
a node outputs given its record does not depend on the record. So conditioning on "no abort
anywhere" leaves the terminal samples i.i.d. from the correct law. This is the same argument
as main.tex (ii), with one global union bound in place of tree restarts. The label law at each FCS
grade in a mixed tree is the one supplied in combined §2.3. The approximation term is main.tex's
hybrid over complete instruments. ∎

Asymptotically M_d = g_d·(1 + O(log κ_d / log(p/κ_d))) + O(log(1/τ_d)/log(p/κ_d)) + O(1).
At fixed c this is linear in g_d at every prime with h ≥ 2. The classical time is
O(S Σ_d n_d · q_d^{−g_d} · B · poly(M_d, log p)), which is 2^{O(max_d g_d log κ_d)}·poly.

**Lemma 5.2 (law transfer; proved).** Let π be a public coordinate projection of F_p^g, and let
V_1 = V ∩ ker π. Run FCS on the π-images of one block of i.i.d. labels uniform on V, and output
w = Σ_i y_i λ_i. Then w ∈ V_1 and, given the block's π-images and coins and given success, w is
uniform on V_1. Outputs of disjoint blocks are independent.

*Proof.*
1. Take any complement V' of V_1 in V. Then π|V' is injective, because V' ∩ ker π ⊆ V' ∩ V_1 = 0.
2. Write λ_i = β_i + γ_i with β_i ∈ V_1 and γ_i ∈ V'. These are independent and uniform, since
   λ_i is uniform on V = V_1 ⊕ V'.
3. π(λ_i) = π(γ_i) determines γ_i. So y depends only on (γ, coins), and Σ y_i γ_i ∈ V' has
   π-image Σ y_i π(λ_i) = 0, hence equals 0.
4. So w = Σ y_i β_i. The β's are independent of (γ, coins), and y ≠ 0, so w is uniform on V_1. ∎

Exact check (Part D): over all first-coordinate banks with a witness, the second coordinate of w
is exactly uniform at (p, κ) = (5, 2), (7, 3), (7, 2), (11, 2) with M_1 = 3.

**Proposition 5.3 (k-level FCS).** Split the g public coordinates into blocks of sizes
g_1 + … + g_k = g. Level j runs FCS of dimension bound g_j on the outputs of level j − 1; by
Lemma 5.2 its input law is again i.i.d. uniform. A level-j witness z lifts to the original columns
with coefficients z_k y_i^{(k)} ∈ D (since D·D ⊆ D) and roots ζ_k σ_i^{(k)}. The result is nonzero
because some z_k ≠ 0 and every y^{(k)} ≠ 0. A grade node then has
- arity ∏_j M_j,
- bank bound Σ_j (∏_{i>j} M_i) β_j,
- trial cap Σ_j (∏_{i>j} M_i) T_j with T_j ≈ 2B ln 2·q^{−g_j}.

This is "splitting the bank into blocks". Part D verifies end-to-end witnesses at degree d for
split arities 6×6, 7×7, 5×5 and 6×6.

## 6. Lower bounds

**Proposition 6.1 (the old design; proved).** Condition on rank r and the generic pivot pattern
{1..r}, so that C is uniform r × n with n = M − r. A uniform kernel vector has x uniform on
F_p^n, and its acceptance is α(bank) = Pr_x[x ≠ 0, x ∈ D^n, Cx ∈ D^r]. Its mean is
E α = (q^n − p^{−n})q^r ≤ q^M. By Markov, Pr_bank[α ≥ s·q^M] ≤ 1/s. So outside probability
1/s + Pr[non-generic] + Pr[r < a] ≤ 1/s + 1/(p−1) + 2p^{a−M}, any T trials succeed with
probability at most T s q^M. Success 1/2 needs T ≥ q^{−M}/(2s) ≥ κ^M e^{−M(κ−1)/p}/(2s).

At the class-9 profile with M = 4u this is 2^{120.7} at (κ, M) = (5, 52) and 2^{126.8} at (9, 40).
The 2^128 is therefore intrinsic to uniform-kernel rejection, not a slack bound. Part C
measures the old acceptance on the same banks, and it matches q^M (for example 3.91e−3
against 3.94e−3 at p = 1031, M = 8).

**Proposition 6.2 (bank-oblivious designs; proved).** A design is bank-oblivious if it fixes,
given (r, π) and its own coins but not the free entries of R, a joint law of candidates
x^{(1)}, …, x^{(T)} ∈ F_p^{non-pivot}. It outputs the first y(x^{(t)}) that is a witness. For the
generic pattern, Pr_C[Cx ∈ D^r] = q^r exactly for every fixed x ≠ 0. This is exact-checked in Part A
for 5 vectors x in each of 12 cases, including x ∉ P_κ^n. So
Pr[success within T] ≤ Σ_t Pr[x^{(t)} ∈ D∖0]·q^r + 1/(p−1) + 2p^{a−M} ≤ T q^a + 1/(p−1) + 2p^{a−M}.
Success 1/2 therefore needs T ≥ (1/2 − o(1))·κ^a e^{−a(κ−1)/p}. FCS-1 meets this up to the
factor 4B ln 2 (about 2^{6.6}–2^{7.3} at the class-9 values B = 36–56). Within the class, structured kernel bases,
other free/pivot splits and other distributions on the free coordinates cannot help.

**6.3 What adaptivity buys, and the open question.** Designs that look at the bank's values can
beat Prop. 6.2:
- **a = 1, sorting by characters.** Two columns with χ(λ_j) = χ(−1)χ(λ_i), for χ of order κ, give
  a support-2 witness in O(M log M) time. Such a pair exists whenever χ(−1) = 1 and M ≥ κ+1.
- **Multi-level FCS** at arity M_1 M_2 costs about M_2 κ^{g/2} instead of κ^g.
- **Coordinate by coordinate** (k = g levels) is the BKW extreme: arity exponential in g,
  polynomial time.

Open: at arity a + O(1), can an adaptive algorithm find a D-witness in time κ^{a−Ω(a)}? With one
effective free direction, the task becomes: given affine forms α_i + β_i t, find t ∈ P_κ with
every α_i + β_i t ∈ D. This is a prescribed-power-residue-pattern search. I know no method
faster than about κ^a trials, and I claim no hardness. A lattice route through {0, ±1} ⊂ D needs
arity about a·log₂p and is not attractive here.

## 7. The brief's five ideas, and what each gives

| Idea | Result |
|---|---|
| Structured kernel bases | No gain among bank-oblivious designs (Prop 6.2). The free-coordinate basis of the RREF is what turns κ^M into κ^r. |
| Solving coordinate by coordinate with characters | Lazy residue testing gives O(1) expected tests per trial. Sorting gives O(M) at a = 1. One coordinate per level is BKW: polynomial time, exponential arity. |
| Choosing which columns enter the kernel | Free values only on columns after the last pivot; the rest are 0. This makes C exactly uniform (§3(b)) and costs only the pivot event 2p^{a−1−L}. |
| Splitting the bank into blocks | Lemma 5.2 and Prop 5.3: k-level FCS, a query-for-time trade. |
| Schedule 2's two-level contraction inside the bank | Not needed under the label law. Rule W+FCS(T) takes Schedule 2 where it gives the smaller arity, which happens only under a tight trial cap (T ≤ 2^20 at large p, grades 3–6). |

## 8. Exact checks (`fcs_exact_out.txt`)

- **Part A.** Exhaustive over C ∈ F_p^{r×n}, 12 cases with p ≤ 13 and up to 1771561 matrices.
  E N = h^n q^r holds exactly and Var N ≤ h E N in every case. The bad fraction is at most 4/μ
  wherever 4/μ < 1. The oblivious identity Pr_C[Cx ∈ D^r] = q^r holds exactly for every tested
  x ≠ 0.
- **Part B.** Exhaustive over all banks A ∈ F_p^{a×M}, seven cases up to 923521 banks. R[:, F'] is
  exactly uniform given the pivot pattern. The fraction of bad banks (pivot fail or acceptance
  < q^r/2) is at most β in every case. Meaningful cases (β < 1): (13, κ=2, a=1, M=5, n_0=3) has
  0.0073 against β = 0.212, and (31, 3, 1, 4, 3) has 0.0342 against 0.145. The remaining cases have
  β ≥ 1 and test only the identities.
- **Part B2.** Random banks with the exact per-bank acceptance, enumerating all h^{n'} draws, six
  cases with a = 2, 3. The bad fraction is at most β in each, for example 0.0377 against 0.0651 at
  (31, 3, a=2, M=6, n_0=4). The mean of acceptance/q^r is 1.000 ± 0.006.
- **Part C.** End-to-end on random subspaces V ⊂ F_p^g at p ∈ {5, 7, 11, 13, 31, 61, 1031, 2521} and
  d ∈ {2, 3, 4, 5, 6, 9}. Every output was verified at the true degree d after roots and the Bezout
  lift. Mean trials track 1/q^a, for example 661.7 against 621.1 at p = 2521, κ = 5, a = 4. In the
  cases with β < 1 the abort fraction stays within β: 0/40 at β = 0.247, 3/40 at β = 0.288 and
  11/40 at β = 0.827. The other cases have β = 1 and come with no promise. The old design's
  acceptance matches q^M within Monte-Carlo noise.
- **Part D.** The law transfer is exact in four cases. Two-level witnesses verify at degree d,
  and the mean trials beat the single level: 430.9 against 4066.9 at p = 2521, κ = 4, a = 6 with a
  3+3 split and arity 6×6, and 903.0 against 3100.3 at p = 2521, κ = 5, a = 5.
- The script ends with `ALL CHECKS PASSED`.

## 9. Class-9 numbers (`fcs_budget_out.txt`, ε = 1/3; g = (19, 17, 16, 14, 12, 9, 6, 3, 1))

"cap" is the worst-case trial cap per grade node, summed over level nodes. Expected trials are
at most twice q^{−a}. W+FCS(2^30) forces multi-level FCS wherever a single level would exceed
2^30 trials.

| p | W | old W+3: Q / trials per node | W+FCS: Q / cap / total | W+FCS(2^30): Q / cap / total |
|---|---|---|---|---|
| 11 | 202.1 | n/a | 42.3 / 28.3 / 47.0 | 42.3 / 28.3 / 47.0 |
| 13 | 401.2 | n/a | 47.2 / 29.8 / 49.4 | same |
| 31 | 407.4 | n/a | 44.9 / 31.7 / 52.2 | 54.6 / 27.5 / 60.9 |
| 1031 | 167.3 | n/a | 36.6 / 33.4 / 50.8 | 40.1 / 23.7 / 42.4 |
| 2521 | 1562.3 | 281.4 / 127.4 | 41.0 / 33.8 / 52.6 | 51.7 / 29.4 / 61.9 |
| 5281 | 852.3 | 50.3 / 128.2 | 39.1 / 33.8 / 52.2 | 49.3 / 29.4 / 61.0 |
| 105019 | 222.0 | 46.3 / 115.1 | 36.6 / 31.0 / 49.9 | 39.7 / 29.0 / 53.0 |
| 2^31−1 | 944.9 | 50.9 / 121.6 | 35.9 / 31.0 / 49.8 | 38.7 / 29.1 / 52.6 |
| 2^61−1 | 555.4 | 52.9 / 128.3 | 34.1 / 33.5 / 51.0 | 38.7 / 29.1 / 54.5 |
| 194522647344910884721 | 71.1 | 52.9 / 128.3 | 34.1 / 33.6 / 51.0 | 41.1 / 29.2 / 56.9 |
| 2^127−1 | 61.5 | 49.9 / 115.2 | 34.0 / 31.0 / 49.5 | 36.5 / 29.0 / 52.1 |
| 2^61−1, ε = 10^{−6} | 555.4 | 53.7 / 128.3 | 35.0 / 34.1 / 51.7 | 40.1 / 29.6 / 55.4 |

The arities at p = 2^61−1 are 19, 18, 16, 14, 11, 8, 5, 3 for grades 2–9, against the old
72, 68, 60, 52, 40, 28, 16 (S2), 36. Every row passes total error ≤ ε, asserted in the script.

Small cases, log₂Q, W against W+FCS:
- c = 2, g = (4, 3): p = 5 gives 13.6 → 7.9.
- c = 3, g = (6, 4, 2): p = 7 gives 34.9 → 13.5, and p = 105019 gives 12.9 → 9.3.
- c = 4, g = (8, 5, 3, 1): p = 13 gives 87.0 → 17.6.
- c = 5, g = (10, 7, 5, 3, 1): p = 11 gives 117.0 → 21.9.

In these cases every per-node cap is at most 2^{12.4}.

## 10. Consequences for other items (for the integrator; not applied)

- **Item 5 (linear arity at small p).** Under the i.i.d. label law, FCS gives arity
  g + O(g log κ/log h + log(1/τ)/log h) at every p with κ < p−1. Examples (`fcs_budget_out.txt`,
  single node, bank bound ≤ 1/64): p = 11, κ = 2, g = 6 gives M = 15, against a worst-case
  floor of 13 and IS arity 2^13.2. p = 13, κ = 4, g = 4 gives M = 16, below the worst-case floor
  of 17 (possible only because the bank is random). The classical
  time is about q^{−g}. This uses the label law, so it is not a worst-case SDE solver and does not
  answer item 5's worst-case question.
- **Derived-dimension corollary (main.tex line 570).** Its random-column branch could drop
  p ≥ 16(r+1)^2, except at κ = p−1. Not worked out here; the IMS branch stays as it is.
- **Table `tab:random-column-budget` and `random_column_rees.json`.** Their trial counts
  (4κ^M B) describe the old sampler. With FCS, M = 4u stays valid, but the trial column changes.
  `make_numbers.py` would need a new artifact, so I propose a literal table instead (below).

## 11. Exact statement that now holds

Assume the hypotheses inherited by Schedule 3: the i.i.d. uniform label law at each stage (Lemma
`lem:central`, combined §2.3), and (2d) of the core check. Then:

1. At a node with h ≥ 2, the FCS sampler succeeds on all but β of banks. It uses at most
   ⌈2B ln 2·q^{−r}⌉ trials and fails with probability at most 2^{−B} (Thm 3.1).
2. main.tex Theorem random-column holds with this sampler, at the same arity and tree budget,
   with trials per node 2B ln 2·u^{u−1} + 1 in place of 4κ^{4u}B (Thm 4.1).
3. With public per-grade arities M_d = g_d + O(·), the composition succeeds with probability at least
   1 − ε at every prime p > c, using Rule W at the zero-sum grade (Thm 5.1).
4. Within bank-oblivious designs, about κ^a trials per node are necessary (Prop 6.2).

All four are proved here, AI-checked, pending human review. Every number is an exact computation.

**Still missing:**
- Human review of §3–§6.
- A polynomial-time sampler, and in particular an adaptive method below κ^a at arity a + O(1)
  (§6.3, open).
- The zero-sum grade κ = p−1.
- An artifact (JSON) and `make_numbers.py` support for the new tables.
- The derived-dimension and codimension corollaries restated at every prime.

**Claim gates that must stay false:** every gate in `research/registry/conjectures.json` and
`claim_gates` blocks, including polynomial-time Schedule 3, worst-case (law-free) small arity,
and human-reviewed status. This note flips nothing.

## 12. Proposed paper text

Status label throughout: "proved in the project notes; AI-checked, pending human review;
conditional on the label law".

Test-compiled: blocks (a)–(d) were spliced into a scratch copy of `main.tex` (2026-11-02 16:40)
and built with pdflatex and bibtex. There were no errors and no new warnings. The only undefined
reference is `thm:bb-envelope`, which another session owns. The only overfull box (line 322)
predates this change. Block (a) adds `prop:rc-lower` and block (d) adds `tab:fcs-budget`.
Theorem `thm:random-column` keeps its label, so every existing reference to it, including (ii),
still resolves. Note for the item-15 appendix (`appendix-schedule3.tex`): its proof should
follow §3–§4 here, since the sampler changed.

**(a) Replace main.tex lines 465–477 (paragraph "Schedule 3" through the status paragraph after
the theorem) with:**

```latex
\paragraph{Schedule 3: random-column kernel rejection.}
By Lemma~\ref{lem:central}, labels of fresh ideal sources at stage $d$ are independent and uniform on the unknown subspace $K_d^\perp$ of dimension $a_d$. Unlike Schedules~1 and~2, this schedule uses that law. Write $\kappa = \kappa_d$, $h = (p-1)/\kappa$, $P_\kappa = \{x^\kappa : x \in \Fp^\times\}$, $D = P_\kappa \cup \{0\}$ and $q = (h+1)/p \ge 1/\kappa$.

\emph{Free-coordinate sampler.} A node with $M$ columns computes the reduced row echelon form $R$ of its measured label matrix, with rank $r$ and pivot columns $p_1 < \dots < p_r$. Let $F'$ be the $n' = M - p_r$ columns after $p_r$ (all columns if $r = 0$); the node aborts if $n' < n_0$. A trial draws $b \in (\Fp^\times)^{F'}$ uniformly, sets $y_j = b_j^\kappa$ for $j \in F'$, $y_j = 0$ on the other non-pivot columns and $y_{p_i} = -\sum_{j \in F'} R_{ij} b_j^\kappa$, and accepts if every $y_{p_i}$ lies in $D$. After acceptance the node extracts $\kappa$-th roots of the $y_{p_i}$ (the roots $b_j$ of the other entries are known), converts by a Bezout exponent and verifies the original equation exactly. The earlier version sampled a uniform kernel vector, so that all $M$ coordinates had to fall in $D$; its acceptance is about $\kappa^{-M}$ on almost every bank (Proposition~\ref{prop:rc-lower}).

\begin{theorem}[Random-column schedule; restated from the project notes]
\label{thm:random-column}
Assume the labels at a stage-$d$ node are independent and uniform on a subspace of dimension $a \le g_d$, and $\kappa_d < p-1$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item For $n_0 \ge 1$ and $L = M - n_0$, outside a bank event of probability at most
  \[
    \beta = \frac{4}{h^{\,n_0-1} q^{a}} + \frac{p^{a}-1}{(p-1)\,p^{L}},
  \]
  each trial is accepted with probability at least $q^r/2 \ge 1/(2\kappa_d^{\,r})$, where $r \le a$ is the observed rank. Hence $\lceil 2B\ln 2\cdot q^{-r}\rceil$ classical trials on the \emph{same} saved bank fail with probability at most $2^{-B}$. Root extraction and fair-bit field sampling are capped so that each also fails with probability at most $2^{-B}$ per node. No further quantum sources are consumed. No condition on $p$ beyond $\kappa_d < p-1$ is used.
  \item Choose an integer $u \ge 2$ with $c \le u$ and $a_d \le u-1$ for every $d$, suppose $p \ge 16u^2$, and use $M = 4u$ columns and $n_0 = 2u+1$ at every grade. Then $\beta \le 4\cdot 15^{-2u}u^{-u-1} + 2p^{-u-1}$, and each node uses at most $2B\ln 2\cdot u^{u-1}+1$ trials. With $B = \lceil \log_2(64 (4u)^{c-1})\rceil$, the three capped arithmetic failures and the bank events make one tree of $(4u)^{c-1}$ leaves abort with probability at most $1/16$. Put $m' = m + \lceil\log_2(3/\eps)\rceil$, run $4m'$ independent trees and keep the first $m'$ successes. Fewer than $m'$ successes occur with probability at most $2^{-2m'} \le \eps/3$. The final rank failure is at most $\eps/3$, and the remaining $\eps/3$ is spread over all complete instruments of all attempted trees. The procedure therefore succeeds with probability at least $1-\eps$, at total cost $2^{O(u\log(u+2))}\cdot\poly(m,\log p,\log(1/\eps))$ with the oracle's internal cost charged separately.
  \item For every prime $p > c$, the arity can instead be chosen grade by grade from public data. Let $S = m + \lceil\log_p(3/\eps)\rceil$ and $n_d = \prod_{2 \le d' < d} M_{d'}$. At a grade with $\kappa_d \ge 2$ and $\kappa_d < p-1$, take $\tau_d = \eps/(9(c-1)Sn_d)$, $n_0 = 1 + \lceil (g_d\log(1/q) + \log(8/\tau_d))/\log h\rceil$ and $M_d = n_0 + g_d + \lceil\log_p(2/\tau_d)\rceil$, so that $\beta \le \tau_d$. At the other grades use the combined rule above. Cap the three random steps of every sampler node at $2^{-B}$ with $B = \lceil\log_2(27N/\eps)\rceil$, $N$ the number of sampler nodes. Then the recursion returns $\hh$ with probability at least $1-\eps$ from $c\,S\prod_d M_d$ oracle queries. The arity is $M_d = g_d\bigl(1 + O(\log\kappa_d/\log(p/\kappa_d))\bigr) + O(\log(1/\tau_d)/\log(p/\kappa_d)) + O(1)$, and the classical time is $2^{O(\max_d g_d\log\kappa_d)}\cdot\poly(m,\log p,\log(1/\eps))$.
\end{enumerate}
\end{theorem}

The proof (\file{research/audits/reviews/2026-11-02-rees-schedule3-cost.md}, Sections~3--5) is a second-moment argument on the reduced row echelon form. Conditional on the rank and the pivot pattern, the entries of $R$ in the columns after the last pivot are independent and uniform. For $x \in P_\kappa^{n'}$ the vectors $-R_{\cdot,F'}x$ are pairwise independent unless proportional, and proportional ones are accepted together. Part~(iii) uses one union bound in place of tree restarts, and the label law in mixed trees from \file{research/audits/reviews/2026-11-02-rees-combined-schedule.md}, Section~2.3. Both arguments have been checked by AI sessions only, and finite exact checks are in \file{research/audits/reviews/2026-11-02-rees-schedule3-cost/}. The probability bound concerns an independent bank, not every fixed matrix. The previous version's statement used arity $d g_d + 2$ at every prime and a sampler ``conditioned on'' a solution, and it is withdrawn. A second-moment bound shows only that a solution exists, not how to find one. Moreover, its claim that the group of $d$-th powers has at least two elements fails at $d = p-1$, which is exactly the case $h = 1$ excluded above.

\begin{proposition}[Rejection cost; restated from the project notes]
\label{prop:rc-lower}
Condition on rank $r = a$ and on the pivot pattern $\{1,\dots,r\}$, which fails with probability at most $1/(p-1) + 2p^{a-M}$. A uniform kernel vector is accepted with mean probability $(q^{M-r} - p^{-(M-r)})q^r \le q^M$ over banks, so by Markov's inequality uniform-kernel rejection needs about $q^{-M} \ge \kappa^M e^{-M(\kappa-1)/p}$ trials on almost every bank. More generally, let candidates $x^{(1)},\dots,x^{(T)}$ for the non-pivot coordinates be drawn from any law that depends on the pivot pattern and private coins but not on the other entries of $R$. Then a witness appears with probability at most $Tq^{a}$, so about $q^{-a} \ge \kappa^a e^{-a(\kappa-1)/p}$ trials are necessary, and the free-coordinate sampler meets this within the factor $4B\ln 2$.
\end{proposition}

Algorithms that read the bank before choosing coordinates are not covered. Splitting the public coordinates of $\gamma_d$ into $k$ blocks and solving them in turn keeps the label law at each level, because each level's outputs are again independent and uniform on $K_d^\perp \cap \ker\pi$. It reduces the per-node cost to about $\kappa^{g_d/k}$ at arity $\prod_j M_j$. Whether some method finds a witness in time $\kappa^{a-\Omega(a)}$ at arity $a + O(1)$ is open.
```

**(b) Replace the last two sentences of main.tex line 462** ("The rule does not mix in Schedule 3.
The abort bound … instead.") with:

```latex
Theorem~\ref{thm:random-column}(iii) mixes Schedule~3 into this rule at every grade with $2 \le \kappa_d < p-1$, with node-count-weighted bank bounds and one union bound, and needs the label law at those grades.
```

**(c) Table `tab:main-regimes`, replace the Random-column row (line 202) with:**

```latex
Random column & $\kappa_d < p-1$ at the grades that use it (any $p$ for part~(iii)); $p \ge 16u^2$, $u \ge c$, $u > \max_d a_d$ for part~(ii) & free-coordinate kernel rejection (Thm.~\ref{thm:random-column}) & $\prod_d M_d$ with $M_d = g_d + O(1 + (g_d\log\kappa_d + \log(1/\eps))/\log(p/\kappa_d))$ for part~(iii); $(4u)^{c-1}$ per tree attempt for part~(ii) \\
```

**(d) New table after `tab:random-column-budget`, literal numbers from
`fcs_budget_out.txt`. The integrator may move them into `numbers.tex` later.**

```latex
\begin{table}[htbp]
\centering
\caption{Class-nine profile $g = (19,17,16,14,12,9,6,3,1)$, $\eps = 1/3$: $\log_2$ of the query count $Q$ under the worst-case combined rule (no label law), under the earlier random-column sampler mixed into that rule, and under Theorem~\ref{thm:random-column}(iii). ``Trials'' is the largest $\log_2$ per-node classical trial count (a worst-case cap with $a_d = g_d$), and ``total'' the $\log_2$ total over all nodes. Exact computation, \file{research/audits/reviews/2026-11-02-rees-schedule3-cost/fcs_budget_out.txt}.}
\label{tab:fcs-budget}
\small
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
$p$ & combined $Q$ & earlier $Q$ & earlier trials & (iii) $Q$ & (iii) trials & (iii) total \\
\midrule
$11$ & $202.1$ & -- & -- & $42.3$ & $28.3$ & $47.0$ \\
$1031$ & $167.3$ & -- & -- & $36.6$ & $33.4$ & $50.8$ \\
$5281$ & $852.3$ & $50.3$ & $128.2$ & $39.1$ & $33.8$ & $52.2$ \\
$2^{31}-1$ & $944.9$ & $50.9$ & $121.6$ & $35.9$ & $31.0$ & $49.8$ \\
$2^{61}-1$ & $555.4$ & $52.9$ & $128.3$ & $34.1$ & $33.5$ & $51.0$ \\
$2^{127}-1$ & $61.5$ & $49.9$ & $115.2$ & $34.0$ & $31.0$ & $49.5$ \\
\bottomrule
\end{tabular}
\end{table}
```

**(e) Abstract and introduction (line 100), optional:** after "a random-column schedule that
exploits the uniform law of the measured labels", add "(with a free-coordinate sampler whose
classical cost per node is about $\kappa_d^{a_d}$ rather than $\kappa_d^{4u}$)".
