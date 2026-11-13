# Referee: is the central-moment threshold proved? (13 Nov)

AI-only adversarial referee, "AI-checked, pending human review" for every claim. Labels follow
the shared agent rules: PROVED / PROVED given cited theorems / CONDITIONAL / REFUTED / UNKNOWN /
NOT computed. [float] means 60-digit mpmath, not interval arithmetic, with the margin stated.
Scripts and outputs: `2026-11-13-rees-central-moment-referee/` (`gm.py`, `table.py`,
`checks.py`, `exact_small.py`, and their `.out` files), interpreter `/opt/anaconda3/bin/python`.
The code was written from the statements, not from TH2's `central_moment.py` or from
`tc_vs_ta_prime.py`.

Objects under review:
- `research/audits/reviews/2026-11-02-rees-threshold-2.md` (TH2) §2: Lemma D, Theorem 5 and
  Corollary 5′;
- the m = 2 input to TH9 Corollary 3, range (C)
  (`2026-11-05-rees-threshold-9.md`, lines 169–186);
- the paper's status sentences, `main.tex` rem:two-level-threshold-size (line 860) and
  `appendix-schedule2.tex` rem:app-s2-joint-moments (line 353).

## 0. Verdict

**PROVED WITH FIXES.** Theorem 5 and Corollary 5′ are **PROVED given cited theorems**. The
cited input is the multiplicative-character Weil bound in the form stated in
`appendix-schedule2.tex` §app:s2-weil (Lidl–Niederreiter Thm 5.41, theorem number not checked
against the book). I found no mathematical gap. Every step and constant checks out by hand and
by independent computation. The fixes are scope and wording only:

1. **"T_C improves on T_A for every κ ≥ 15" was supported only for κ ≤ 40, plus κ = 60, 100
   and 200** (TH2 `cm_table*.out`). The range 41 ≤ κ ≤ 881 needed a finite check, because
   Corollary 5′ beats (κ−1)κ^κ only once 4e⌈ln 4κ⌉² < κ − 1, which holds for all κ ≥ 882.
   **Now supplied [float]:** min_m G_m((κ−1)κ^κ) < 1 for every 15 ≤ κ ≤ 926. The maximum is
   0.444, at κ = 15. Beyond 926, Corollary 5′ applies, with an explicit monotone tail (§2.3).
   Together with T_A(κ) > (κ−1)κ^κ (prop:app-s2-TA(ii), proved), this gives T_C(κ) < T_A(κ)
   for every κ ≥ 15. The claim fails at κ = 13 and 14, consistent with the paper.
2. **Strictness.** "Every prime p ≥ T_C(κ)" should read "p > T_C(κ)". The set {p : G_m(p) < 1}
   is an interval open on the left: at its infimum G_m is either 1, by continuity, or +∞, where
   ε_k = 1. The difference is immaterial in practice.
3. **Tail of condition (C) in Corollary 5′.** The step for κ > 20000 ("grows like κ ln κ … O(ln κ)")
   is informal. A one-line explicit version: m = ⌈ln 4κ⌉ ≤ 2 ln κ for κ ≥ 11, so (C) follows
   from f(κ) := (κ/2 − 4 ln κ − 2) ln κ − ln(98 ln κ) − 2 ln 4 · ln κ ≥ 0. f(20000) ≈ 9.9·10⁴,
   and f is increasing there.
4. **TH2 table error (harmless).** The row "κ = 3–5: none (ε_k ≥ 1 throughout)" is false.
   ε_k → 0 as p → ∞, and T_C(3) = 9964.6, T_C(4) = 1.97·10⁵ and T_C(5) = 1.73·10⁶. All three are
   far above T_A, so nothing downstream changes. It is a bisection-window artifact.
5. **Paper wording (integrator's call; no file edited).** "Argued, not proved here" understates
   the status. The accurate label is: proved in the cited report, given the Weil bound;
   AI-checked, pending human review. The 6κ^κ + 1 (κ ≥ 729) statement also depends on TH9
   ranges (A) and (B), which I did **not** referee. Its m = 2 input is fine (§2.4).

## 1. Line-by-line check

**Setup.** The draw is y_0 = 0 and y_1, …, y_{κ−1} uniform, with
X_j(y) = {x : x + y_i ∈ Q_{−(i+j)} for all i} (nonzero cosets, so no zero cells), and h = (p−1)/κ.
Row 0 forces X_j ⊆ Q_{−j}. Then X_j(y) = ξ^{−j}X_0(ξ^j y), and y ↦ ξ^j y preserves the law with
y_0 = 0, so every n_j has the law of n = n_0. Excluding zero cells only shrinks the event, so
it does no harm: all n_j > 0 gives a contraction with every entry in Q_0 and α_0 + β_0 = α_0 ≠ 0.
This is a valid witness for p ∉ E_2(κ) under the paper's definition, which allows zero cells but
does not require them. **OK.**

**Lemma D.** (n)_k counts ordered k-tuples of *distinct* points of X_0(y) ⊆ Q_0. There are
(h)_k such tuples. The rows i ≥ 1 are independent, so E(n)_k = Σ_x Π_i N_i(x)/p.

N_i(x) is the count of lem:app-s2-weil-count with ℓ = k, distinct roots r_l = −x_l and c_l = 1.
- The convention χ^s(0) = 0 for all s, including s = 0, makes the indicator expansion valid at
  z = 0.
- The s = 0 term is p − k.
- A support-1 term vanishes exactly.
- A term with support t ≥ 2 is a Weil sum of f = Π(X − r_l)^{s_l}, with s_l ∈ [1, κ−1] and t
  distinct roots. Such an f is not a constant times a κ-th power, so the sum is at most
  (t−1)√p, less at most k − t point values of modulus ≤ 1.

The closed form E_k(p) = (k−1−k/κ+κ^{−k})√p + k/κ − kκ^{−k} matches eq:app-s2-error.
**PROVED given Weil.** The per-tuple test (`exact_small.out`, 300 random tuples for each of
seven (κ, p) pairs, k ≤ 6) gives max |N − (p−k)/κ^k| / E_k = 0.49. It is only a falsification
test.

**Theorem 5, steps 1–6.**
1. f(n) = (1 − n/λ)^{2m} ≥ 0 and f(0) = 1, so P(n = 0) ≤ E f(n). **OK.**
2. The expansion a_k = Σ_{j≥k} C(2m,j)(−1/λ)^j S(j,k) follows from n^j = Σ_k S(j,k)(n)_k.
   B ~ Bin(h, Q) with Q = κ^{−(κ−1)} has factorial moments (h)_k Q^k and mean λ = hQ = (p−1)/κ^κ.
   **OK.**
3. Each row factor lies in κ^{−k}(1−k/p)(1 ± ε_k) uniformly over tuples. The product of κ−1
   rows, summed over (h)_k tuples, gives F_k/B_k ∈ [((1−k/p)(1−ε_k))^{κ−1}, ((1−k/p)(1+ε_k))^{κ−1}]
   ⊂ [1−δ_k, 1+δ_k]. The upper end uses 1 − k/p ≤ 1. At k = 1, E_1 = 0 and the bracket is the
   exact value ((p−1)/p)^{κ−1}. **OK.**
4. With X_l = 1_l − Q, |X_l| ≤ 1 gives |E X_l^r| ≤ E X_l² ≤ Q for r ≥ 2. Group the expansion of
   (ΣX_l)^{2m} by the partition of positions that equal indices induce. The blocks get distinct
   indices, so the expectation factorises. A singleton block gives 0. There are at most h^j
   index assignments. So E(B−λ)^{2m} ≤ Σ_{j≤m} S₂(2m,j)λ^j. **OK.** My exact test agrees,
   e.g. 33.19 ≤ 37.33 and 3317 ≤ 4219 at κ = 3, p = 1009.
5. B_k ≤ λ^k and |a_k| ≤ Σ_j C(2m,j)λ^{−j}S(j,k), so Σ_k|a_k|B_kδ_k ≤ max δ · W_m. **OK.**
6. Union bound over the κ columns. **OK.**

*Monotonicity.* λ^{j−2m} has j ≤ m and λ^{k−j} has k ≤ j. For k ≥ 1, ε_k = κ^k(c_1√p + c_2)/(p−k)
with c_1, c_2 ≥ 0 has negative derivative, and (1 − k/p)(1 − ε_k) increases. **OK**, with the
strictness caveat of fix 2.

**Corollary 5′.** The inequalities used, each checked by hand:
- Bell(2m) ≤ (2m)^{2m}, by mapping each element to the minimum of its block;
- S(j,k) ≤ C(j,k)k^{j−k}, by choosing the block minima;
- T_j ≤ (λ+j)^j and W_m ≤ (2 + 2m/λ)^{2m} ≤ 4^m e^{2m²/λ} ≤ 4^m e^{1/(2e)} = 1.2019·4^m;
- E_k ≤ k√p, and ε_k ≤ 2kκ^k/√p for p ≥ 2k;
- the two branches of δ_k: e^x − 1 ≤ 2x on [0, 1], and Bernoulli;
- 2(κ−1)(ε* + 2m/p) ≤ 10mκ^{2m+1}/√p;
- the total 1/4 + 12.1·m4^mκ^{2m+2}/√p;
- (C) ⇒ G_m ≤ 0.497, and (κ−1)ε* ≤ 4/(49·4^m κ).

Each step uses only λ ≥ λ* and √p ≥ κ^{κ/2}, so monotonicity is not needed here. **PROVED.**

## 2. Independent numerics

**2.1 T_C and T_A [float]** (`table.out`). These reproduce TH2's table and
`tc_vs_ta_prime.out` to every printed digit. Examples: T_C(15) = 3.567347·10¹⁸ (m = 2) against
T_A(15) = 6.130514·10¹⁸, ratio 1.7185. T_C(7) = 4.870336·10⁷. T_A(3) = 79.0394 and
T_A(7) = 4,941,830. T_A/T_C = 2.1741 at κ = 17, 15.535 at κ = 200, and 0.928 at κ = 14.

**2.2 Condition (C)** (`checks.out`). Exact integer test for κ ≤ 3000, and log test with margin
1 for κ ≤ 20000. (C) fails exactly at κ ≤ 31, the last failures being 24–31, and holds for every
32 ≤ κ ≤ 20000. Direct evaluation G_m(p*) at p* = 4e⌈ln 4κ⌉²κ^κ + 1, for κ = 32..80, 100, 150,
200, 300, 500 and 1000: the maximum is 5.2·10⁻⁴, at κ = 32.

**2.3 κ ≥ 15 improvement (fix 1)** (`checks.out`). min_m G_m((κ−1)κ^κ) < 1 for every
15 ≤ κ ≤ 926, with maximum 0.4437 at κ = 15, no failures, and a margin far beyond 60-digit
rounding. 4e⌈ln 4κ⌉² < κ − 1 for all 882 ≤ κ ≤ 10⁵. For κ ≥ 926, 4e(ln 4κ + 1)² + 1 < κ − 1:
it holds at 926, and κ − 4e(ln 4κ + 1)² has derivative 1 − 8e(ln 4κ + 1)/κ > 0 there. At κ = 13
and 14, min_m G_m((κ−1)κ^κ) is 1.085 and 1.077, and T_C > T_A.

**2.4 TH9 Corollary 3, range (C).** A_4 = λ + 3λ² and W_2 = 16 + 24/λ + 11/λ² + 1/λ³, both
re-derived by hand. Exact G_2 at p = √(8κ)κ^κ + 1: 0.37664 at κ = 729, 0.37608 at κ = 1677 and
0.37504 at κ = 10⁶, all below 0.9 [float]. The W_2·δ part is below 10⁻⁶⁰ (60-digit noise), and
(κ−1)ε* ≤ 6.5·10⁻¹⁰³⁰. G_2 is non-increasing in p, so the whole range λ ≥ √(8κ) is covered.
**The m = 2 input is PROVED given Weil.** Ranges (A) and (B) of TH9 are NOT checked here.

**2.5 Exact chain test [exact law, float comparison]** (`exact_small.out`). For
(κ, p) = (3, 1009), (3, 3001), (4, 197) and (4, 389), the law of n was computed over all
p^{κ−1} values of y. All F_k/B_k for k ≤ 6 lie inside their Lemma D brackets. At k = 1 the
value equals the endpoint, so a 10⁻⁴⁰ relative tolerance is used. P(n=0) ≤ E f(n) ≤ G_m/κ and
E(B−λ)^{2m} ≤ A_{2m} hold for m = 1, 2, 3. No violation. These tests only falsify.

## 3. Consistency with data

A proved threshold must not certify any known member of E_2.
- κ = 7: over all 56 members of E_2(7) (`E2_k7.txt`), min_m G_m is at least 35148, and the
  largest member, 3221, is 6.6·10⁻⁵ T_C(7).
- 14281 ∈ E_2(8): min_m G_m = 1.05·10⁵.
- 181 ∈ E_2(5): G_m = +∞ for every m.
- 24967 ∈ E_2(9): min_m G_m = 2.1·10⁶.
- 859 ∈ E_2(6): min_m G_m = 7914.
- 53 ∈ E_2(4): G_m = +∞.

**No contradiction.** This is trivially so, since T_C ≫ κ^{(κ+1)/2}.

## 4. Claim gates that stay false

The result changes neither E_2(κ) for κ ≤ 14 nor Table tab:app-s2-thresholds, and it does not
close the square gap (exponent κ against (κ+1)/2). It raises no speedup or novelty claim.

## 5. Adversarial self-check

- *Did I re-derive or rubber-stamp?* I recomputed every constant by hand. The numerics come from
  my own code, which agrees with TH2 and with the 11-13 report, so a shared misreading of the
  statement remains possible. The one hand step I would most want a human to recheck is
  step 4, the partition grouping. The argument is standard, and the exact Bin(h, Q) moments
  agree with it.
- *Weil hypothesis.* The bound needs f not of the form c·g^κ. That holds because every exponent
  is in [1, κ−1]. For composite κ, χ^{s_l} may have smaller order, but the combined character
  is still χ applied to f, so this is fine. The LN theorem number is unverified (a paper TODO,
  `appendix-schedule2.tex` line 22).
- *Distinct points.* (n)_k sums over distinct tuples only. The roots −x_l are distinct, and the
  points x_l + y = 0 are excluded, which gives the p − k main term. Checked.
- *Float rigour.* The threshold comparisons use 60-digit mpmath, not intervals. The smallest
  margin is G = 0.444 against 1 at κ = 15, so rounding cannot flip any comparison, but this
  is [float], not [exact].
- *Scope.* I did not referee TH9 ranges (A) and (B), the 5.5κ^κ variant, or the barrier
  proposition. The 6κ^κ + 1 claim therefore stays CONDITIONAL on those ranges as far as this
  referee goes.
