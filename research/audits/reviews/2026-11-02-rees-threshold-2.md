# Two-level SDE threshold, round 2: the square gap

2 November 2026. AI-only research pass for item 3 of
`research/REES_FULL_CAMPAIGN_2.md`. It is not human review, a Lean proof or a
priority claim, and "AI-checked, pending human review" applies to every claim.
Labels: **[proved]** is a written proof here; **[exact]** is a complete finite
computation, script named; **[float]** is exact integers combined in
floating point, margin stated; **[argued]** is a heuristic. Scripts and outputs
are in `2026-11-02-rees-threshold-2/`, interpreter `/opt/anaconda3/bin/python`.
Notation follows `2026-11-02-rees-weil-threshold.md` (below "WT") §1 and
`2026-11-02-rees-small-prime-arity.md` (below "SPA") §1: χ has order κ,
Q_b = {x ≠ 0 : χ(x) = ω^b}, A_b = Q_b ∪ {0}, h = (p−1)/κ, and a universal
two-level contraction is α, β ∈ F_p^κ with α_j + β_i ∈ A_{−(i+j)} and
α_0 + β_0 ≠ 0. E_2(κ) is the set of primes p ≡ 1 (mod κ) where none exists.

## 0. Result

The goal was a threshold of order κ^{(κ+1)/2+o(κ)}, or at least an exponent
below κ. **Neither was reached.** What this pass does prove or compute:

1. **κ = 7 is closed [exact + proved].** E_2(7) is exactly 56 primes, the
   largest 3221 (list in §1). A new sparse complete DFS (`sdfs.c`) settles
   every prime p ≡ 1 (mod 7) up to 5·10⁶. Above that, WT Theorem 2 applies,
   since T_A(7) = 4,941,830 < 5·10⁶. So E_2(κ) is now known exactly for every
   κ ≤ 7. The largest exceptional prime is 1.34·7⁴, against 1.66, 1.45 and
   1.62 times κ^{(κ+1)/2} for κ = 4, 5, 6.
2. **Exponent κ + o(1) [proved].** WT's Paley–Zygmund step is replaced by
   central moments of order 2m (Theorem 5). These are accurate through Weil
   as long as κ^{2m} ≪ √p. For κ ≥ 32,

       p ≥ 4e⌈ln 4κ⌉²·κ^κ + 1  ⇒  p ∉ E_2(κ),

   so the threshold is κ^{κ + O(ln ln κ / ln κ)}, against WT's (κ−1)κ^κ.
   The computable form beats T_A(κ) from κ = 15 on, by factors of 1.7 at
   κ = 15, 4.4 at κ = 40 and 16 at κ = 200 (table in §2). For κ ≤ 14 it is
   worse than T_A, and it gives nothing new for the paper's small κ.
3. **Barriers [proved / exact / argued].** §3 says why the exponent stalls at
   κ, and why going below it looks as hard as a known open problem.
   - Uniform β with a union bound over columns needs λ = p/κ^κ ≥ 1 − 1/κ
     **[proved, WT §4]**. Theorem 5 reaches λ = O(ln²κ), and the Poisson
     heuristic says ln κ is the true limit of that method.
   - Every square-root (Weil, Deligne, Katz) estimate, applied block by block
     or tuple by tuple, gives an exponent of at least κ **[argued]**.
   - At κ = 3 the full character expansion with the triangle inequality first
     certifies at p = 139. That is above T_A(3) = 79, and every prime is
     feasible there. The largest |S_e| with e ≠ 0 is ≈ (p−4)p⁴ = p^{κ+2},
     above square-root size **[exact]**. That is the size predicted for
     4-cycle supports **[argued]**.
   - The zero-cell sub-family turns the problem into a coloured-clique
     problem on differences in F_p **[proved, exact]**. For the Paley graph,
     the analogous gap between the proven bound (p ≈ 4^k) and the random
     prediction (p ≈ 2^{k/2}) is a well-known open problem (Kunisky–Yu,
     arXiv:2211.02713, §1, eqs. (3)–(4)).
4. **Approaches that failed, recorded so they are not repeated.**
   - Alternating Bonferroni sums: the cancellation is too large on every
     tested κ ≤ 30 (`bonferroni.py`, `bonf_grid.out`).
   - Symmetric β (fixed points of a scaling-and-shift map): these collapse
     to WT's geometric family **[proved, §3.5]**.
   - Arithmetic-progression families: the ratio of conditions to variables
     gets worse **[argued]**.

## 1. κ = 7 exactly

**Method [exact].** `sdfs.c` solves the same problem with the same
normalisation as SPA's `dfs2.c` (β_0 = 0, α_0 = 1, zero cells allowed). It
keeps each candidate set X_j as a list of survivors, and it accepts a
candidate β_i only if every X_j keeps an element, with an early exit. It
tries candidates in cyclic order from a random offset. The search is complete
unless it hits the node limit, and no run hit it. Every FEASIBLE witness has
all κ² cells re-checked. Cross-validation:
- κ = 3..6 on [3, 3000] reproduces SPA's E_2 lists exactly (`xval_k{4,5,6}.out`).
- At κ = 7, each of the 19 INFEASIBLE primes in [1597, 3400] has exactly the
  same node count as `dfs2` (`xval_k7.out` against `dfs2_k7*.out`). The
  20th, 1583, is below the start of those `dfs2` runs. The combined list is
  in `E2_k7.txt`.

That is expected, since a complete search visits the same tree in any order.

| range (p ≡ 1 mod 7) | output | feasible | infeasible | limit |
|---|---|---|---|---|
| [3, 1499] | `k7_low.out` | 2 | 36 | 0 |
| [1500, 3400] | `xval_k7.out` | 21 | 20 | 0 |
| [3401, 4621] | `k7_mid.out` | 21 | 0 | 0 |
| [4622, 10⁶] | `k7_a.out` | 12,963 | 0 | 0 |
| [10⁶+1, 2.3·10⁶] | `k7_b.out` | 15,148 | 0 | 0 |
| [2.3·10⁶+1, 3.7·10⁶] | `k7_c.out` | 15,646 | 0 | 0 |
| [3.7·10⁶+1, 5·10⁶] | `k7_d.out` | 14,158 | 0 | 0 |

**Theorem 6 [exact + proved].** E_2(7) consists of these 56 primes:

    29 43 71 113 127 197 211 239 281 337 379 421 449 463 491 547 617 631 659
    673 701 743 757 827 883 911 953 1009 1051 1093 1163 1289 1303 1373 1471
    1499 1583 1597 1667 1709 1877 2017 2087 2143 2213 2297 2339 2381 2423
    2591 2731 2801 2843 2969 3137 3221

*Proof.* For p ≤ 5·10⁶ use the table, which has no LIMIT line. For
p ≥ 5·10⁶ > T_A(7) = 4,941,830, WT Theorem 2 applies, and WT's
monotonicity lemma shows its condition holds at every p ≥ T_A. ∎

This agrees with SPA's 37 proven primes ≤ 1583 and with the 19 primes that
`2026-11-02-rees-dfs2-runs.md` found in [1597, 20000]. It closes WT's open
item (ii) for κ = 7. A complete-or-witness run costs about 14 ms per prime
at p ≈ 1.6·10⁶. The same sweep for κ = 8 up to T_A(8) ≈ 1.17·10⁸ would cost
about 10⁶ CPU-seconds, so it was not run (§5).

## 2. Theorem 5: central moments of order 2m

Fix κ ≥ 3 and a prime p ≡ 1 (mod κ). Draw y_0 = 0 and y_1, …, y_{κ−1}
independent and uniform on F_p. Put n = n_0(y) = #{x ∈ Q_0 : x + y_i ∈ Q_{−i},
i ≥ 1}. Put Q = κ^{−(κ−1)} and λ = hQ = (p−1)/κ^κ. Every n_j(y) has the same
law as n (WT §6), and WT Lemma A turns "every n_j > 0" into a contraction.

**Lemma D (factorial moments) [proved; checked exact].** For k ≥ 1,

    E[(n)_k] = Σ_{distinct x_1..x_k ∈ Q_0} Π_{i=1}^{κ−1} N_i(x)/p,
    N_i(x) = #{y : x_l + y ∈ Q_{−i}, l = 1..k},
    |N_i(x) − (p−k)κ^{−k}| ≤ E_k(p) := (k−1−k/κ+κ^{−k})√p + k/κ − kκ^{−k}.

*Proof.* (n)_k counts ordered k-tuples of distinct points of X_0(y).
Exchange the sums; the rows i are independent. For the count, use the
convention χ^s(0) = 0 for every s, including s = 0. Then
1_{Q_c}(z) = κ^{−1} Σ_s ω^{−cs} χ^s(z) holds for every z, and

    N = κ^{−k} Σ_{s∈Z_κ^k} ω^{−⟨c,s⟩} Σ_y Π_l χ^{s_l}(y + a_l)

with distinct a_l. The term s = 0 gives p − k. Take s ≠ 0 with support T,
and |T| = t. Its inner sum is W_s minus at most k − t point values of
modulus ≤ 1, where W_s = Σ_y Π_{l∈T} χ^{s_l}(y + a_l). If t = 1 then W_s = 0.
If t ≥ 2, then |W_s| ≤ (t−1)√p by Weil (Lidl–Niederreiter Thm 5.41, as
cited in SPA §7): the polynomial has t distinct roots with exponents in
[1, κ−1], so it is not a constant times a κ-th power. Summing over the
C(k,t)(κ−1)^t vectors of each support size gives E_k(p), as in SPA §2. ∎

`bonferroni.py check` (`bonf_check.out`) compared E[(n)_k], k ≤ 4, with the
Lemma D interval by brute force over all y. It covered κ = 3 (p ≤ 61), κ = 4
(p ≤ 41) and κ = 5 (p ≤ 31), with 0 failures.

**Theorem 5 [proved].** Let m ≥ 1. Put ε_k = κ^k E_k(p)/(p−k), and
δ_k = max((1+ε_k)^{κ−1} − 1, 1 − ((1−k/p)(1−ε_k))^{κ−1}), with δ_k = ∞ if
ε_k ≥ 1. Define

    A_{2m}(λ) = Σ_{j=1}^{m} S₂(2m, j) λ^j      (S₂ = set partitions with no singleton block),
    W_m(λ)    = Σ_{j=0}^{2m} C(2m, j) λ^{−j} T_j(λ),   T_j(λ) = Σ_k S(j,k) λ^k,
    G_m(p)    = κ [ λ^{−2m} A_{2m}(λ) + W_m(λ) · max_{k≤2m} δ_k ].

Then P(n = 0) ≤ G_m(p)/κ. If G_m(p) < 1, at least a fraction 1 − G_m(p) of
all y have every X_j(y) nonempty, so p ∉ E_2(κ). G_m is non-increasing in
real p > 2m, so T_C(κ) := min_m inf{p : G_m(p) < 1} is a threshold: every
prime p ≥ T_C(κ) with p ≡ 1 (mod κ) lies outside E_2(κ).

*Proof.*
1. *Test polynomial.* Let f(n) = (1 − n/λ)^{2m}. It is ≥ 0 and f(0) = 1, so
   P(n = 0) ≤ E f(n).
2. *Comparison with a binomial.* Expand f(n) = Σ_{k≤2m} a_k (n)_k, with
   a_k = Σ_{j≥k} C(2m,j)(−1/λ)^j S(j,k). Let F_k = E[(n)_k], and let
   B_k = (h)_k Q^k be the factorial moments of B ~ Bin(h, Q), whose mean is
   hQ = λ. Then E f(n) = E f(B) + Σ_k a_k (F_k − B_k).
3. *Moment error.* By Lemma D, each factor N_i/p lies in
   κ^{−k}(1 − k/p)(1 ± ε_k). There are (h)_k tuples and κ − 1 rows, so
   F_k/B_k lies in [((1−k/p)(1−ε_k))^{κ−1}, ((1−k/p)(1+ε_k))^{κ−1}]
   ⊂ [1−δ_k, 1+δ_k].
4. *Binomial central moment.* Write B − λ = Σ_{l≤h} X_l, with X_l = 1_l − Q
   independent, E X_l = 0 and |X_l| ≤ 1, so E|X_l|^r ≤ E X_l² ≤ Q for r ≥ 2.
   Expand (Σ X_l)^{2m} and group the terms by the partition of the 2m
   positions that equal indices induce. Partitions with a singleton block
   contribute 0. A partition with j blocks has at most h^j index assignments,
   each of modulus at most Q^j. Hence E(B − λ)^{2m} ≤ A_{2m}(λ), and
   E f(B) ≤ λ^{−2m} A_{2m}(λ).
5. *Coefficient sum.* B_k ≤ λ^k and |a_k| ≤ Σ_j C(2m,j) λ^{−j} S(j,k), so
   Σ_k |a_k| B_k δ_k ≤ max_k δ_k · W_m(λ).
6. *Union bound.* Sum over the κ columns.

*Monotonicity.* λ^{−2m}A_{2m} = Σ_j S₂ λ^{j−2m} has j ≤ m. W_m is a sum of
λ^{k−j} with k ≤ j. ε_k has the form (c_1√p + c_2)/(p − k) with c_1, c_2 ≥ 0,
which decreases, as in WT's proof of monotonicity, and 1 − k/p increases. ∎

**Corollary 5′ (explicit asymptotics) [proved; finite range checked].** Let
κ ≥ 32, m = ⌈ln 4κ⌉ and λ* = 4e m². Then every prime p ≡ 1 (mod κ) with
p ≥ λ*κ^κ + 1 is outside E_2(κ). Hence

    T_C(κ) ≤ 4e⌈ln 4κ⌉² κ^κ + 1 = κ^{κ + O(ln ln κ / ln κ)}.

*Proof.* At λ ≥ λ*:
- *Main term.* Σ_j S₂(2m,j) ≤ Bell(2m) ≤ (2m)^{2m}, so
  λ^{−2m}A_{2m}(λ) ≤ ((2m)²/λ)^m ≤ e^{−m} ≤ 1/(4κ).
- *Coefficient sum.* T_j(λ) ≤ (λ+j)^j, because S(j,k) ≤ C(j,k)k^{j−k}. So
  W_m ≤ (2 + 2m/λ)^{2m} ≤ 4^m e^{1/(2e)} ≤ 1.21·4^m.
- *Moment error.* For p ≥ 4m we have E_k ≤ k√p and ε_k ≤ 2kκ^k/√p, so
  every ε_k with k ≤ 2m is at most ε* := 4mκ^{2m}/√p. When (κ−1)ε* ≤ 1,
  e^x − 1 ≤ 2x and Bernoulli's inequality give
  δ_k ≤ 2(κ−1)(ε* + 2m/p) ≤ 10mκ^{2m+1}/√p for k ≤ 2m.
- *Total.* G_m ≤ 1/4 + κ·1.21·4^m·10mκ^{2m+1}/√p = 1/4 + 12.1·m 4^m κ^{2m+2}/√p.
  With √p ≥ κ^{κ/2}, condition (C), κ^{κ/2} ≥ 49·m 4^m κ^{2m+2}, gives
  G_m ≤ 1/4 + 12.1/49 < 1/2. (C) also gives (κ−1)ε* ≤ 4/(49·4^m κ) < 1.

`asymptotic.py` (`asymptotic.out`) verifies (C) for every 32 ≤ κ ≤ 20000;
(C) first fails at κ = 31. For κ > 20000 the left side of
(κ/2 − 2m − 2) ln κ ≥ ln(49m) + m ln 4 grows like κ ln κ, while the right
side is O(ln κ). The script also evaluates G_m(p*) exactly at
p* = λ*κ^κ + 1 for κ = 32..72, 100, 200 and 500, and every value is below 1. ∎

**Independent check [AI].** A separate subagent re-derived Lemma D,
Theorem 5 and Corollary 5′ with its own code. It checked:
- Lemma D exactly for κ = 3 (p ≤ 61) and κ = 4 (p ≤ 41), and on 3000
  sampled tuples each at κ = 3, 4, p ≤ 4993, k ≤ 4;
- E(B−λ)^{2m} ≤ A_{2m}(λ) exactly for h ≤ 200 and m ≤ 6 (largest ratio 0.9997);
- F_k/B_k ∈ [1−δ_k, 1+δ_k] and P(n=0) ≤ E f(n) ≤ G_m/κ against exact laws
  of n (κ = 3, p ≤ 20011; κ = 4, p ≤ 1009);
- monotonicity of G_m;
- κ_0 = 32, and T_C at κ = 7, 15, 20, 40.

It found one error. The "Total" constant had been written as 48.4, which
together with (C) does not give G_m < 1. The correct constant, 12.1, is in
the proof above. It also suggested stating the ε* bound uniformly in k,
which is now done. This is an AI check, not a human review.

**Numbers [float, 50 digits; `cm_table.out`, `cm_table_large.out`].**
T_C(κ) is computed by bisection on the monotone G_m, m ≤ 16. The comparison
column uses (κ−1)κ^κ, a lower bound for T_A (WT Prop. (ii)), so the ratios
below understate T_C's advantage slightly.

| κ | T_C(κ) | best m | T_C/κ^κ | (κ−1)κ^κ | (κ−1)κ^κ / T_C | log_κ T_C − κ |
|---|---|---|---|---|---|---|
| 3–5 | none (ε_k ≥ 1 throughout) | – | – | | | |
| 7 | 4.87e7 | 1 | 59.1 | 4.94e6 | 0.10 | 2.10 |
| 9 | 4.79e9 | 1 | 12.4 | 3.10e9 | 0.65 | 1.15 |
| 14 | 1.56e17 | 1 | 14.0 | 1.44e17 | 0.93 | 1.00 |
| 15 | 3.57e18 | 2 | 8.15 | 6.13e18 | 1.72 | 0.77 |
| 20 | 8.29e26 | 2 | 7.91 | 1.99e27 | 2.40 | 0.69 |
| 40 | 1.08e65 | 3 | 8.93 | 4.71e65 | 4.37 | 0.59 |
| 60 | 4.81e107 | 4 | 9.84 | 2.88e108 | 6.00 | 0.56 |
| 100 | 1.11e201 | 4 | 11.1 | 9.90e201 | 8.94 | 0.52 |
| 200 | 2.06e461 | 5 | 12.8 | 3.20e462 | 15.5 | 0.48 |

At m = 1 Theorem 5 is Chebyshev's inequality, so it needs λ > κ and is
slightly weaker than WT's Paley–Zygmund certificate. The gain comes from
m ≥ 2, and that needs √p ≫ κ^{2m+1}. So it starts at κ ≈ 15.

**Exact test of the inequality chain [exact; `cm_fft_check.py`,
`cm_fft_check.out`].** For κ = 3, p ∈ {331, 1009, 3001, 10009, 20011}, the
exact law of n over all p² values of y was computed by cyclic correlation.
It is integer valued, with rounding residue < 10⁻⁶. At every point,
P(n=0) ≤ E f(n) ≤ G_m/κ wherever G_m is finite, and the exact binomial
central moment is ≤ A_{2m}(λ), for m = 1, 2, 3. A side observation: P(n=0)
is about 3/p, not e^{−λ}. The floor comes from degenerate y with
y_i = y_{i'} or y_i = 0, which are always empty. It costs κ³/(2p) in the
union bound, which is negligible.

## 3. Why the exponent stalls at κ, and what going lower would take

**3.1 Uniform β [proved, WT §4; Theorem 5].** For uniform y,
P(X_j ≠ ∅) ≤ E n_j = λ. So any union-bound certificate needs
κ(1 − λ) < 1. If n were Poisson, κe^{−λ} < 1 would be both necessary and
sufficient, that is λ ≈ ln κ. Theorem 5 gets λ = O(ln²κ). So the β-average
method is now within O(ln κ) of its own limit. Every method that draws β
from a fixed distribution and then fills the columns independently faces
the same issue. Each column variable α_j must meet κ coset conditions alone,
and E n_j is p/κ^κ for any β whose entries are distinct. That is the column
barrier.

**3.2 Square-root cancellation [argued].** Below κ^κ a solution must be
found jointly. A block of t columns and t rows chosen together, with the
rest fixed, has 2t variables and 2tκ − t² conditions. A square-root
estimate gives a main term p^{2t}κ^{−(2tκ−t²)} and an error of order p^t, so
it certifies only for p ≳ κ^{2κ−t}. The best case, t = κ, is the full
expansion at exponent κ (κ + 1 once translation and scaling are counted, as
in WT §4). Every Weil, Deligne or Katz estimate applied to one character
tuple or one block at a time therefore stays at exponent ≥ κ. Going lower
needs cancellation across the κ^{κ²} tuples, or a different method.

**3.3 The full expansion at κ = 3 [exact; `triangle_k3.py`,
`triangle_k3.out`].** Write N_c = κ^{−κ²} Σ_e ω^{−⟨e,c⟩} S_e, where
S_e = Σ_{α,β} Π χ^{e_ij}(α_j + β_i). Translation gives S_e = p·Σ_{β_0=0},
and that sum factorises over columns. All 3⁹ values S_e were computed for
p ≡ 1 (mod 3), p ≤ 199. The expansion reproduces the direct count N_c for
every p ≤ 61.
- The triangle-inequality certificate S_0 > Σ_{e≠0}|S_e| fails at every
  p ≤ 127 and holds at every tested p from 139 to 199, so it first holds at
  p = 139 (L1/S_0 = 0.89; at p = 127 it is 1.004).
- That is worse than T_A(3) = 79, and every prime is feasible at κ = 3.
- max_{e≠0}|S_e| ≈ (p−4)p⁴ = p^{κ+2}, above square-root size. That is the
  size p^{2κ+1−v/2} that a support on v = 4 vertices (a 4-cycle) would have
  **[argued]**; the maximising tuples were not identified.

So the full expansion, bounded term by term, is not a route below κ+1 even
at κ = 3.

**3.4 A Paley-type sub-problem [proved; exact check].** Suppose −1 ∈ H
(h even) and s ≠ 0. Put β_i = −α_{i−s}. Cell (i, i−s) is then 0 and cell
(i, j) is α_j − α_{i−s}. The contraction conditions become

    α_j − α_k ∈ Q_{−(j+k+s)} for all j ≠ k,

which is symmetric in j, k because −1 ∈ H. The (0,0) cell is
α_0 − α_{−s} ≠ 0. This is a κ-clique in the Cayley colouring of F_p by
cosets of differences, with the colour of each edge fixed by j + k.
`zero_cell.py` (`zero_cell_k{3,4}.out`) found solutions and re-checked all
κ² cells: at every p ≡ 1 (mod 6) up to 400 for κ = 3, and at every
p ≡ 1 (mod 8) in [73, 1500] for κ = 4. It found none at 17, 41 and 97 for
κ = 4, and 41 and 97 are not in E_2(4). So the sub-family is strictly
smaller.

Its first-moment point is still κ^{(κ+1)/2}, and greedy Weil still gives
κ^{2κ}. For the Paley graph, the same gap is a well-known open problem. The
lower bound known for all primes is (1/2 + o(1)) log₂ p, from Erdős–Szekeres;
the random graph has 2 log₂ p; and number-theoretic arguments give
log p · log log log p only for infinitely many p (Graham–Ringrose). This is
as summarised in Kunisky–Yu, arXiv:2211.02713, §1, eqs. (1)–(4), read in
full text. Our problem is not known to be equivalent to the Paley question.
The analogy says only that the standard tools stop at the same place there
**[argued]**.

**3.5 Structured β [proved].** Column j is feasible for β iff
β ∈ B_j := Π_i Q_{−(i+j)} + F_p·1. Let σ be the index shift,
(σβ)_i = β_{i−1}. Then σ^m B_j = B_{j−m} and g^{−u}B_j = B_{j+u}, so
ψ = g^{−u}σ^m maps B_j to B_{j+u−m}. A β fixed by ψ modulo the diagonal, and
lying in B_0, is therefore feasible for every column in 0 + (u−m)Z_κ.

Now solve ψβ ≡ β, that is, γβ_{i−m} = β_i + t with γ = g^{−u}. Put
d = gcd(m, κ). The indices split into d cycles of length L = κ/d.
- If γ^L ≠ 1, going round a cycle forces every β_i to equal the same
  constant, and the rows coincide.
- So γ^L = 1. Then u is a multiple of (p−1)/L = hd, and the solutions are
  β_{r+km} = c_r γ^k + const, with one free c_r per cycle.

So the fixed space has dimension d. But d divides both m and u = hd·v, so
d divides u − m. The orbit of column 0 then covers only κ/d columns, and the
other d − 1 orbits each need their own column variable with κ conditions.
In all there are 2d variables and dκ conditions, which is the ratio κ/2 of
the unrestricted problem. With d = 1 there is one parameter: WT's geometric
family, which needs one-variable Weil with κ conditions and so κ^{2κ}.
Symmetric ansätze of this kind therefore cannot lower the exponent of a
square-root method (§3.2).

**3.6 Bonferroni sums fail [exact; `bonferroni.py`].** The truncated
alternating sums Σ_{k≤m} (−1)^k E[(n)_k]/k! need m ≳ eλ for the truncation
error to be small. On the tested grid (κ ∈ {3,5,7,9,12,16,20,30},
m ∈ {2,4,8,16,24}, λ ∈ {1,2,4,8}·ln κ; `bonf_grid.py`, `bonf_grid.out`),
κ·B_m was never below 2.53, so the certificate never fired. Theorem 5's squared test
polynomial avoids the alternating cancellation, and it replaces this.

## 4. Literature

- Weil bound: Lidl–Niederreiter, *Finite Fields*, Thm 5.41, as cited and
  checked in SPA §7 (via Martin–Yip, arXiv:2403.04312v2, Lemma 2.2).
- Paley clique bounds: D. Kunisky and X. Yu, "A degree 4 sum-of-squares
  lower bound for the clique number of the Paley graph", arXiv:2211.02713,
  §1. The full text was read: eq. (3), (1/2+o(1)) log₂ p from Erdős–Szekeres
  [ES35]; eq. (4), log p log log log p for infinitely many p [GR90]; log log p
  under GRH [Mon71, Thm 13.5].
- No priority review was made for Theorem 5. It is a standard moment method
  (Chebyshev with higher central moments) on top of WT's set-up.

## 5. Statement that now holds; what is missing; gates

**Holds.**
- (a) E_2(κ) is known exactly for every κ ≤ 7:
  - E_2(2) = E_2(3) = ∅;
  - E_2(4) and E_2(5) are SPA's 6 and 9 primes;
  - E_2(6) is SPA/WT's 53 primes ≤ 859;
  - E_2(7) is the 56 primes of Theorem 6, the largest 3221.
- (b) For every κ ≥ 3, p ≥ min(T_A(κ), T_C(κ)) implies p ∉ E_2(κ), where
  T_C(κ) ≤ 4e⌈ln 4κ⌉²κ^κ + 1 for κ ≥ 32. Hence p ≥ κ^{κ+o(1)} suffices
  (exponent κ + O(ln ln κ/ln κ)).
- (c) At every prime with G_m(p) < 1, a fraction ≥ 1 − G_m(p) of uniform β
  extend. So a random β works with constant probability, and each α_j is
  found by scanning F_p with O(κp) coset tests. Where T_C < p < T_S this is a
  constant for fixed κ. For p ≥ T_S, WT's sampler is unchanged. Theorem 5
  gives no polylog(p) sampler below T_S.

No new access model is involved: the columns are arbitrary and the scalars
are public precomputation.

**Missing.**
- (i) Any threshold with exponent below κ. §3 says why the known tools stop
  there.
- (ii) E_2(8) on (20000, T_A(8) ≈ 1.17·10⁸] and E_2(9) on
  (20000, 3.10·10⁹]. Item 4 covers κ = 8, 9 up to 20000. Above that it is
  mechanical but costs about 10⁶ CPU-seconds for κ = 8 with `sdfs.c`, since
  each prime needs an O(p) coset table. Theorem 5 does not lower T_A at
  κ = 8, 9.
- (iii) A human check of Lemma D, Theorem 5 and the κ = 7 computation.

**Claim gates that must stay false.**
- "The two-level threshold is ≈ κ^{(κ+1)/2}" as a theorem.
- "Exponent below κ proved".
- "E_2(κ) is known for κ ≥ 8".
- "Schedule 2 is optimal".
- Any priority or novelty claim for Theorem 5 or the barrier remarks.
- Any claim that the threshold question is equivalent to the Paley clique
  problem.
- SPA's and WT's gates are unchanged.

## 6. Proposed paper text

Status label for all of it: AI-checked, pending human review.

**(A) Target: `main.tex`, the paragraph after Proposition
`prop:decoupled-sde` (line 458).** Replace the clause "and $E_2(6)$ equal to
a set of $53$ primes, the largest $859$; for $\kappa \ge 7$ only bounds on
$E_2(\kappa)$ are known." with:

```latex
$E_2(6)$ equal to a set of $53$ primes, the largest $859$, and $E_2(7)$ equal to a set of $56$ primes, the largest $3221$ (exact search over every prime $p \equiv 1 \pmod 7$ below $5\cdot10^6 > T_A(7)$, \file{research/audits/reviews/2026-11-02-rees-threshold-2.md}, Section~1); for $\kappa \ge 8$ only bounds on $E_2(\kappa)$ are known.
```

**(B) Target: `main.tex`, a remark after that paragraph** (or the end of the
Schedule 2 appendix, `appendix-schedule2.tex`, after Proposition
`prop:app-s2-TA`, if the integrator prefers).

```latex
\begin{remark}[Size of the two-level threshold; AI-checked, pending human review]
\label{rem:two-level-threshold-size}
Replacing the second moment over $\beta$ by central moments of order $2m$, with the factorial moments of $|X_j(\beta)|$ controlled by the Weil bound, shows that $p \notin E_2(\kappa)$ for every prime $p \equiv 1 \pmod\kappa$ with $p \ge 4e\lceil\ln 4\kappa\rceil^2\kappa^\kappa + 1$ when $\kappa \ge 32$, and the computable form of the same bound improves on $T_A(\kappa)$ for every $\kappa \ge 15$ (\file{research/audits/reviews/2026-11-02-rees-threshold-2.md}, Theorem~5). The two-level threshold is therefore at most $\kappa^{\kappa+o(1)}$. The exceptional primes found by exhaustive search lie below $1.7\,\kappa^{(\kappa+1)/2}$ for $\kappa \le 7$, and $\kappa^{(\kappa+1)/2}$ is where the expected number of contractions crosses one. Closing this square gap is open. Any argument that averages over $\beta$ and then fills the columns separately needs $p \ge (1-1/\kappa)\kappa^\kappa$, and square-root bounds for character sums applied one tuple at a time do not go below exponent $\kappa$; a sub-family of the problem is a coloured-clique question in $\Fp$ of the same type as the clique number of the Paley graph, where the analogous gap is a long-standing open problem.
\end{remark}
```

The integrator should check that `\file` is defined in `main.tex`; it is
used at line 458. No bibliography entry is needed. If the Paley sentence is
kept with a citation, a bib entry for Kunisky–Yu (arXiv:2211.02713) is
needed.

**(C) Not proposed.** Nothing in the theorem statements, the arity claims or
Table `tab:main-regimes` changes. The prime hypothesis of Proposition
`prop:decoupled-sde` stays "p ∉ E_2(κ), in particular p ≥ κ^{κ+1}". For the
paper's small κ, T_A is still the better explicit bound.

## 7. Artifacts (`2026-11-02-rees-threshold-2/`)

| file | role |
|---|---|
| `sdfs.c` | sparse complete DFS (`cc -O2 -o sdfs sdfs.c`; `./sdfs K P0 P1 limit seed [print]`) |
| `run_k7.sh`, `k7_{low,mid,a,b,c,d}.out`, `xval_k{4,5,6,7}.out`, `E2_k7.txt` | κ = 7 sweep, cross-validation, final list |
| `central_moment.py` | Theorem 5: G_m, T_C table (`table`), brute-force check (`check`) |
| `cm_table.out`, `cm_table_large.out`, `cm_check.out` | T_C tables; small-p check (vacuous there, 0 failures) |
| `cm_fft_check.py`, `cm_fft_check.out` | exact κ = 3 test of the inequality chain, p up to 20011 |
| `asymptotic.py`, `asymptotic.out` | Corollary 5′: condition (C) and exact G_m(p*) |
| `bonferroni.py`, `bonf_check.out`, `bonf_grid.py`, `bonf_grid.out` | Lemma D brute-force check; the failed Bonferroni route |
| `triangle_k3.py`, `triangle_k3.out` | full character expansion at κ = 3 |
| `zero_cell.py`, `zero_cell_k{3,4}.out` | zero-cell (coloured clique) sub-family |
