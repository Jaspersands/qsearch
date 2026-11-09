# Two-level SDE threshold: a second moment over β

2 November 2026. AI-only research pass for item 2 of
`research/REES_FULL_CAMPAIGN.md`. It is not human review, a Lean proof, or a
priority claim. Labels: **[proved]** means a written proof here.
**[exact]** means a complete finite computation, with the script named.
**[float]** means exact integer counts combined in long-double arithmetic,
with the margin stated. **[argued]** means a heuristic. Scripts and outputs
are in `2026-11-02-rees-weil-threshold/`; the interpreter is
`/opt/anaconda3/bin/python`. Notation follows
`2026-11-02-rees-small-prime-arity.md` (below "SPA"), §1.

## 0. Result

The SPA report proved the two-level contraction for p > T_W(κ) ≈ (κ−2)²κ^{2κ}
and saw failures only up to about 1.5κ^{(κ+1)/2}. Its open question 1 asked for a proof
that uses the freedom in β. This pass gives one.

1. **Exact moments [proved].** Draw β = (0, y_1, …, y_{κ−1}) with the y_i
   uniform in F_p. Let n_j(y) be the number of α_j that complete column j.
   Then E[n_j] and E[n_j²] are given exactly by the cyclotomic numbers of
   order κ (Lemma B). They do not depend on j.
2. **Certificate [proved].** If Φ(p,κ) := κ(1 − E[n]²/E[n²]) < 1, a
   universal two-level contraction exists at p. In fact a fraction
   ≥ 1 − Φ of all β works (Theorem 1). Φ costs O(p) to compute.
3. **Analytic threshold [proved].** Jacobi-sum bounds on the cyclotomic
   numbers give Φ < 1 for every p ≥ T_A(κ), with
   T_A(κ) = (κ−1)κ^κ(1 + o(1)) ≤ κ^{κ+1} for all κ ≥ 3 (Theorem 2).
   This is 300 to 2.4·10⁹ times below T_W for κ = 4..9 (table in §3).
   The exponent drops from about 2κ to κ+1.
4. **Exact ranges [float + proved].** Φ < 1 at every prime p ≡ 1 (mod κ)
   with p > P_Φ(κ), where P_Φ = 31, 709, 12281, 232987 for κ = 3, 4, 5, 6
   and P_Φ(7) = 4,940,293 (phiscan on [4·10⁶, 5·10⁶], which contains T_A(7) = 4,941,830). Every
   exceptional prime that SPA lists has Φ ≥ 1, so nothing contradicts.
5. **κ = 6 closed [exact + proved].** SPA's DFS is complete for p ≤ 1.5·10⁶,
   and P_Φ(6) = 232,987 < 1.5·10⁶. So E_2(6) is exactly SPA's 53 primes, the
   largest 859. For κ = 7, 8, 9 the exceptional set now lies below 4.95·10⁶,
   1.18·10⁸ and 3.10·10⁹, instead of 1.7·10¹³, 1.0·10¹⁶ and 7.4·10¹⁸.
6. **Sampler [proved].** For p ≥ T_S(κ) ≈ 8κ^{κ+1}, a randomized sampler
   (random β, then random α_j) succeeds with probability ≥ 3/8 per round
   at O(κ^{κ+1} log κ) coset tests (Theorem 3). The SPA band where α_j had
   to be found by enumerating F_p was p < 4((κ−1)κ^κ+1)²; it shrinks to
   p < T_S(κ).
7. **Not reached: the observed threshold.** T_A(κ) is about
   (1 − 1/κ)·(κ^{(κ+1)/2})², roughly the SQUARE of the observed threshold.
   §4 proves that every union-bound certificate over uniform β is stuck
   above (κ−1)κ^{κ−1}. It also explains the observed value as the point
   where the expected number of full solutions crosses 1 **[argued]**.

## 1. Reduction to column counts

Fix a character χ of order κ with χ(g) = ω, so Q_b = {x ≠ 0 : χ(x) = ω^b}
and h = (p−1)/κ. A universal two-level contraction is a pair α, β ∈ F_p^κ
with α_j + β_i ∈ A_{−(i+j)} = Q_{−(i+j)} ∪ {0} for all i, j ∈ Z_κ and
α_0 + β_0 ≠ 0. This is SPA Lemma 1; the labelling does not depend on g,
since replacing g by g^u relabels i, j by u·i, u·j.

**Lemma A [proved].** Let y ∈ F_p^κ with y_0 = 0, and put
X_j(y) = {x ∈ F_p : x + y_i ∈ Q_{−(i+j)} for all i ∈ Z_κ}. If every X_j(y)
is nonempty, then β = y and any α_j ∈ X_j(y) form a contraction.
*Proof.* Every cell lies in its coset, and α_0 + β_0 = α_0 ∈ Q_0, so it is
nonzero. Scaling by α_0^{−1} ∈ H gives SPA's normalisation α_0 = 1. ∎

Only strict cosets are counted. Allowing zero cells can only help.

Cyclotomic data: for b, c ∈ Z_κ put

    m_b = #{v : v ∈ Q_b, v+1 ∈ Q_b},     r_c = #{w ∈ Q_0, w ≠ 1 : w−1 ∈ Q_c}.

**Lemma B (exact moments) [proved; brute-force check exact].** Let y_1, …,
y_{κ−1} be independent and uniform on F_p, y_0 = 0, and n_j = |X_j(y)|.
Then for every j,

    E[n_j]   = h^κ / p^{κ−1},
    E[n_j²]  = E[n_j] + h p^{−(κ−1)} Σ_{c∈Z_κ} r_c Π_{b≠−c} m_b.

*Proof.* Row 0 forces x ∈ Q_{−j}. Rows are independent, and for fixed x the
row-i condition holds for exactly h values of y_i. So
E[n_j] = Σ_{x∈Q_{−j}} (h/p)^{κ−1}. For the second moment, sum over pairs
(x, x') in Q_{−j}. The diagonal gives E[n_j]. For x ≠ x', put d = x' − x ∈ Q_c'.
Row i requires u = y_i + x ∈ Q_a and u + d ∈ Q_a, with a = −(i+j).
Substituting u = dv shows this holds for exactly m_{a−c'} values of y_i.
Write x' = xw with w ∈ Q_0 \ {1}. Then d = x(w−1) ∈ Q_c' iff w − 1 ∈ Q_{c'+j},
so h·r_{c'+j} pairs have difference in Q_c'. With k = c' + j, the row indices
a − c' = −(i+k), i = 1..κ−1, run over every residue except −k. ∎

`second_moment.py check` enumerated all y ∈ F_p^{κ−1} and compared both
moments for every j: κ = 3 (p ≤ 43), κ = 4 (p ≤ 41), κ = 5 (p ≤ 31) and
κ = 6 (p ≤ 13). All matched, and the empirical fraction of good y was
never below 1 − Φ (`check.out`) **[exact]**.

## 2. The certificate

**Theorem 1 [proved].** Put R = E[n_j²]/E[n_j]², which does not depend on j,
and Φ = κ(1 − 1/R). If Φ < 1, then at least a fraction
1 − Φ of all y ∈ {0} × F_p^{κ−1} have every X_j(y) nonempty. So p ∉ E_2(κ).
*Proof.* By Cauchy–Schwarz (Paley–Zygmund),
E[n] = E[n·1_{n>0}] ≤ (E[n²]·P(n > 0))^{1/2}. Hence
P(n_j = 0) ≤ 1 − 1/R, and a union bound over the κ columns finishes. ∎

Closed form: R = p^{κ−1}/h^κ + Σ_c (r_c/h) Π_{b≠−c} (m_b p/h²).

**Consistency with the exact exceptional sets [exact].** `second_moment.py exc`
(`exc.out`) gives Φ ≥ 1 at every listed exceptional prime. For κ = 4 at
p = 5 … 53, Φ = 3.97 … 3.31. For κ = 5 at p = 11 … 181, Φ = 4.99 … 4.73. No
contradiction is possible in the other direction: Φ ≥ 1 does not imply
infeasibility.

**Per-prime scans (`phiscan.c`) [float].** It computes the integers m_b and r_c
exactly, then R in long double. The smallest margin 1 − Φ among certified primes is
6.5·10⁻², 2.6·10⁻², 5.6·10⁻³, 4.6·10⁻⁴, 1.9·10⁻⁵ for κ = 3..7, far above rounding
error. For κ = 4 the Python exact-fraction version agrees on p ≤ 3000.

| κ | range scanned | certified | uncertified | largest uncertified P_Φ(κ) | output |
|---|---|---|---|---|---|
| 3 | [3, 2·10⁵] | 8984 | 4 (7, 13, 19, 31) | 31 | `phiscan_k3.out` |
| 4 | [3, 2·10⁵] | 8916 | 61 | 709 | `phiscan_k4.out` |
| 5 | [3, 2·10⁵] | 4117 | 361 | 12281 | `phiscan_k5.out` |
| 6 | [3, 4·10⁵] | 6582 | 10310 | 232987 | `phiscan_k6.out` |
| 7 | [4·10⁶, 5·10⁶] | 647 | 10225 | 4,940,293 | `phiscan_k7_hi.out` |

Each scan range contains T_A(κ) (§3). So every prime above the listed P_Φ(κ)
is certified, by the scan up to T_A and by Theorem 2 beyond.

## 3. The analytic threshold

**Lemma C (cyclotomic estimates) [proved; checked exact].** Put
μ = (p−κ−1)/κ² and Δ(p) = ((κ−1)(κ−2)√p + 2(κ−1))/(p−κ−1). Then
Σ_b m_b = Σ_c r_c = κμ exactly, and |m_b/μ − 1|, |r_c/μ − 1| ≤ Δ(p).
*Proof.* Expand the indicators with χ:
κ² m_b = Σ_{s,t} ω^{−b(s+t)} K(s,t), with K(s,t) = Σ_{v≠0,−1} χ^s(v)χ^t(v+1).
The values are as follows:
- K(0,0) = p − 2.
- K(s,0) = −χ^s(−1) and K(0,t) = −1.
- K(s,−s) = −1, because v ↦ v/(v+1) is a bijection onto F_p \ {0,1}.
- For s, t, s+t ≠ 0, K(s,t) = χ^s(−1)J(χ^s, χ^t), which has modulus √p.

Summing gives κ² m_b = p − κ + 1 − κ[b=0] − κ[b=ε] + G_b, where χ(−1) = ω^ε
and G_b is a sum of (κ−1)(κ−2) terms of modulus √p with Σ_b G_b = 0. The
analysis of r_c is the same, with K'(s,t) = Σ_{w≠0,1} χ^s(w)χ^t(w−1). ∎
`analytic.py verify` checked both identities and the bound at every prime
p ≡ 1 (mod κ) up to 2·10⁴ for κ = 2..5, 6·10⁴ for κ = 6, 7 and 4·10⁴ for
κ = 8, 9 (`verify.out`). The worst ratio |deviation|/Δ was 0.88 to 1.00, so
the bound is nearly tight **[exact]**.

**Theorem 2 [proved].** Let κ ≥ 2 and p > κ+1 with Δ := Δ(p) ≤ 1/2. Put

    U(p) = κ^κ p^{κ−1}/(p−1)^κ + exp(E_max),
    E_max = max_{0 ≤ s ≤ √κ Δ} (−A s² + B s),
    A = 1/2 − Δ/3 − 1/(κ(1−Δ)),   B = Δ/(√κ (1−Δ)).

Then R ≤ U(p). Hence U(p) < κ/(κ−1) implies Φ < 1.
*Proof.* Write m_b = μ(1+δ_b) and r_c = μ(1+η_c), with Σδ = Ση = 0 and all
|δ|, |η| ≤ Δ (Lemma C). The closed form becomes R = p^{κ−1}/h^κ + L·F.
Here L = ((p−κ−1)/(p−1))^κ (p/(p−1))^{κ−1} ≤ 1, using (p−2)p ≤ (p−1)². The
other factor is F = Π_b(1+δ_b) · (1/κ)Σ_c (1+η_c)/(1+δ_{−c}), with
D = Σ_b δ_b². Since log(1+x) ≤ x − x²/2 + x³/3 and Σδ = 0,
Π_b(1+δ_b) ≤ exp(−D(1/2 − Δ/3)). Since Σ_c(η_c − δ_{−c}) = 0,
(1/κ)Σ_c (1+η_c)/(1+δ_{−c}) = 1 + (1/κ)Σ_c (δ_{−c}² − η_cδ_{−c})/(1+δ_{−c})
≤ 1 + (D + √(D·κΔ²))/(κ(1−Δ)). Use 1 + x ≤ e^x and set s = √D ≤ √κΔ.
Then F ≤ exp(−A s² + B s) ≤ exp(E_max). ∎

**Monotonicity [proved].** Δ(p) decreases for p > κ+1, and E_max increases
with Δ. The first term of U decreases, because d/dp log = (κ−1)/p − κ/(p−1) < 0.
So U decreases in real p, and T_A(κ) := inf{p : Δ ≤ 1/2, U(p) < κ/(κ−1)}
is found by bisection. The condition holds for every p ≥ T_A.

**Size [proved].** U(κ^{κ+1}) < κ/(κ−1) was checked for every 3 ≤ κ ≤ 40
(`kk1.out`). For κ ≥ 6 it follows in general: at p = κ^{κ+1} the bound
gives Δ ≤ 1.01κ^{(3−κ)/2} ≤ 0.1 and A ≥ 0.18, so E_max ≤ B²/(4A) ≤ 1.8κ^{2−κ}.
The first term is ≤ 1/κ + 2κ^{−κ−1}, and 1/κ + 2κ^{−κ−1} + 2κ^{2−κ}
< 1/(κ−1) once κ^{4−κ}·2 < 1. So T_A(κ) ≤ κ^{κ+1} for every κ ≥ 3.
Expansion gives T_A(κ) = (κ−1)κ^κ + O(κ^5).

`table.out`:

| κ | T_A(κ) (Φ < 1 above) | (κ−1)κ^κ | T_W(κ) (SPA) | T_W/T_A | observed ≈ 1.5κ^{(κ+1)/2} | T_S(κ) (sampler) | SPA sampler 4((κ−1)κ^κ+1)² |
|---|---|---|---|---|---|---|---|
| 3 | 79 | 54 | 837 | 10.6 | 13.5 | 735 | 1.21e4 |
| 4 | 869 | 768 | 263,681 | 303 | 48 | 8,596 | 2.37e6 |
| 5 | 12,658 | 12,500 | 8.79e7 | 6.9e3 | 188 | 1.26e5 | 6.25e8 |
| 6 | 233,577 | 233,280 | 3.48e10 | 1.5e5 | 794 | 2.24e6 | 2.18e11 |
| 7 | 4.94e6 | 4.94e6 | 1.70e13 | 3.4e6 | 3,602 | 4.61e7 | 9.77e13 |
| 8 | 1.17e8 | 1.17e8 | 1.01e16 | 8.6e7 | 1.74e4 | 1.07e9 | 5.52e16 |
| 9 | 3.10e9 | 3.10e9 | 7.35e18 | 2.4e9 | 8.86e4 | 2.79e10 | 3.84e19 |

At κ = 2 the bound is weaker than SPA's (8.4 against 6.6). It is not needed
there, since E_2(2) = ∅.

**Theorem 3 (sampler) [proved].** Suppose U(p) ≤ 1 + 1/(8κ), which holds
for p ≥ T_S(κ). Each round does the following:
1. Draw y uniformly.
2. For each j, draw K = ⌈2(p/h)^κ ln(4κ)⌉ uniform x ∈ F_p.
3. Test x ∈ X_j(y) exactly, using κ coset tests.

A round succeeds with probability ≥ 3/8. So B rounds all fail with
probability ≤ (5/8)^B, at κK = O(κ^{κ+1} log κ) coset tests per round.
*Proof.* By Chebyshev, P(n_j < E[n]/2) ≤ 4(R−1). Summed over the κ columns
this is ≤ 4κ(U−1) ≤ 1/2. Given n_j ≥ E[n]/2 = h^κ/(2p^{κ−1}), one draw
hits X_j with probability ≥ h^κ/(2p^κ). So K draws all miss with probability
≤ exp(−ln 4κ) = 1/(4κ), and summed over the columns ≤ 1/4. ∎

For T_W < p < T_S, SPA had to find α_j by enumerating F_p. Now that is
needed only for p < T_S(κ), which is still a constant for fixed κ.

## 4. Why this stops at about κ^{κ+1} [proved / argued]

- **Column barrier [proved].** For uniform y,
  P(X_j(y) ≠ ∅) ≤ E[n_j] = h^κ/p^{κ−1} < p/κ^κ. So a union-bound certificate
  Σ_j P(X_j = ∅) < 1 needs E[n_j] > 1 − 1/κ, that is
  p ≳ (κ−1)κ^{κ−1}. Theorem 1 is within a factor of about κ of this.
  Moreover, for p < κ^κ a uniform β works with probability < p/κ^κ. Near
  the observed threshold the good β have density ≤ 1.5κ^{−(κ−1)/2}. A proof
  there has to find RARE β, which means using correlations between columns.
- **Where the observed threshold comes from [argued].** There are 2κ−2
  free scalars after normalisation and κ² − 1 coset conditions, so the
  expected number of full solutions is about p^{2κ−2}/κ^{κ²−1}. This equals 1
  at p = κ^{(κ+1)/2}. SPA's largest exceptional primes are 1.66, 1.45
  and 1.62 times this value for κ = 4, 5, 6. So the observed threshold is
  the first-moment point, and T_A ≈ (1 − 1/κ)·(first-moment point)².
- **Other routes in the brief [argued].** A joint square-root (Deligne-type)
  bound for the full character sum over all 2κ−2 variables would give
  p^{κ−1} ≳ C·κ^{κ²−1}, i.e. the same exponent κ+1. It would also need
  nondegeneracy of the hyperplane-arrangement sums Π χ^{e_ij}(x_j + y_i),
  which this pass did not establish. So the elementary second moment already
  matches what joint Weil/Deligne cancellation for each character tuple
  e could give. Going lower would need cancellation ACROSS the κ^{κ²} tuples e.
  Lang–Weil on the variety {x_j + y_i = c_ij u_ij^κ} has dimension 2κ−2 and
  degree about κ^{κ²}, and gives a worse threshold. The Combinatorial
  Nullstellensatz controls non-vanishing on grids, not multiplicative coset
  conditions, and was not pursued. Explicit β (SPA's β_i = g^{−i} − 1, or
  geometric families y_i = cζ^i) collapses the freedom to O(1) parameters.
  Each column then needs one-variable Weil, which brings back κ^{2κ}.

## 5. Statement that now holds

For every prime p, every d with κ = gcd(d, p−1) ≥ 3 and every a ≥ 1: if
p ≥ T_A(κ) (where T_A(κ) ≤ κ^{κ+1}), or, for κ ≤ 7, p > P_Φ(κ), a
universal two-level contraction C_ij = z_i z_j(α_j + β_i) with C_00 ≠ 0
exists. So Schedule 2's arity (a+1)((κ−1)a+1) finds a nonzero solution of
Σ_i s_i^d λ_i = 0 for arbitrary columns λ_i ∈ F_p^a. The contraction depends
only on (p, κ, g). It is found in randomized poly(log p)·O(κ^{κ+1} log κ)
time for p ≥ T_S(κ) (Theorem 3), and by constant-size search for fixed κ
below that. There is no extra access model: the columns are arbitrary and
the scalars are public precomputation. Combined with SPA:

| κ | E_2(κ) |
|---|---|
| 2, 3 | ∅ (SPA) |
| 4 | {5, 13, 17, 29, 37, 53} (SPA; now also certified above 709) |
| 5 | {11, 31, 41, 61, 71, 101, 131, 151, 181} (SPA; certified above 12281) |
| 6 | exactly SPA's 53 primes ≤ 859 (**new: closed**) |
| 7 | SPA's 37 proven primes ⊂ E_2(7) ⊂ primes ≤ 4621 ∪ (2·10⁵, P_Φ(7)] |
| 8 | contains SPA's 82 proven primes; ⊂ primes < 1.18·10⁸ |
| 9 | contains SPA's 82 proven primes; ⊂ primes < 3.10·10⁹ |

**Still missing.**
- (i) A threshold near the observed κ^{(κ+1)/2}. This needs cross-column
  correlations (§4).
- (ii) E_2(7) on (2·10⁵, P_Φ(7)], plus SPA's 22 unresolved κ = 7 primes. Also
  E_2(8) on (8353, 1.18·10⁸] and E_2(9) on (10333, 3.10·10⁹]. These are
  mechanical: a DFS or witness scan per prime (`dfs2.c`). Item 3 runs dfs2
  for κ = 7, 8, 9 only at small p, so this upper end is not covered there.
- (iii) An independent human check of Lemmas B and C.

**Claim gates that must stay false.**
- "The two-level threshold is ≈1.5κ^{(κ+1)/2}" as a theorem.
- "E_2(κ) is known for κ ≥ 7".
- "Schedule 2 is optimal".
- Any priority or novelty claim for Theorems 1–3. They are a standard
  second-moment argument plus classical cyclotomic/Jacobi-sum bounds, with
  no literature-priority review.
- SPA's gates are unchanged.

**Text fixes for `main.tex` (listed, not applied).**
1. Thm `thm:power-sde` (ii), line 429. Replace "p ≥ 16κ^{2κ+2}, the two-level
   symmetric construction" with "p ≥ κ^{κ+1} (κ ≥ 3), or p ∉ E_2(κ), the
   two-level decoupled construction C_ij = z_i z_j(α_j + β_i)". Cite this
   report and SPA §§1–3. (The symmetric form α = β is strictly weaker: SPA §3.)
2. Same item, cost sentence. For p ≥ T_S(κ) (≤ 10κ^{κ+1}; ≤ 9κ^{κ+1} for κ ≥ 4) the scalars cost
   O(κ^{κ+1} log κ)·poly(log p, k) for abort 2^{−k}. Below that, the cost is
   a constant search for fixed κ.
3. The paragraph after the theorem. "the single condition p ≥ 16c^{2c+2}"
   becomes "p ≥ c^{c+1}", valid since p ≥ c^{c+1} ≥ κ_d^{κ_d+1} ≥ T_A(κ_d)
   for every grade with κ_d ≥ 3. For κ_d = 2 use SPA Thm 2, which holds for all p ≥ 7, with
   E_2(2) = ∅ at every prime.
4. Mark part (ii) as proved in the AI-checked reports, not "restated from the
   project notes".

## 6. Independent check

A separate subagent re-derived Lemmas A–C and Theorems 1–3 with its own
code. It used brute force over all y at eight (p, κ) and two generators
each, compared U with the exact R at every prime with Δ ≤ 1/2 up to 2·10⁴
(κ ≤ 6) and 8000 (κ = 7, 8), and checked U(κ^{κ+1}) < κ/(κ−1) for
κ = 3..80. It found no mathematical error. It also found that the full
distribution of n_j, not only the moments, is the same for every j (scale
x and y by g^j). Its five text corrections are applied above. This is an
AI check, not a human review.

## 7. Artifacts

| file | role |
|---|---|
| `second_moment.py` | exact moments, brute-force check, exceptional-prime check, sampler check |
| `phiscan.c` | per-prime Φ in C; `cc -O2 -o phiscan phiscan.c; ./phiscan κ P0 P1` |
| `analytic.py` | T_A, T_S, Lemma C verification, κ^{κ+1} check |
| `check.out`, `exc.out`, `verify.out`, `table.out`, `kk1.out`, `phiscan_k*.out` | outputs quoted above |
