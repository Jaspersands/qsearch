### 12.13 κ = 4 in closed form, and what its shape predicts for κ = 5 (10 Nov) [derived; computed exactly; referee round 4i]

Scripts: `osc-mc/k4_22.py` (κ = 4, exact per S; all S at p ≤ 401) and `osc-mc/k5_22.py`; outputs
`osc-mc/k4/k4_22_series.out` and `osc-mc/k4/k5_22_series.out`. The κ = 5 predictions were written before any κ = 5
run (`osc-mc/k4/predictions_k5_22.txt`, 12:30:32; `k5_22.py` saved 12:31:12, first κ = 5 output 12:37:18). Referee
checks: `review-2026-11-10/scratch/r4i_checks.py`, `r4i_pole.py` and their `.out`, written independently of these
scripts.

- **Transport identity** [elementary]. For g = (a b; c d) ∈ PGL₂(F_p), g(x) − g(y) = det g·(x − y)/((cx + d)(cy + d)).
  Let ι be an involution swapping s_i ↔ s_j and s_u ↔ s_v, and P(t) ∈ (Z/κ)^κ the profile P(t)_l = ind(s_l − t) mod κ.
  - At a swapped point, P(ιt)_{ι(l)} = P(t)_l + α_l + β(t), with α_l = −ind(c s_l + d) depending only on S and ι, and
    β(t) = −ind(ct + d) not depending on l. Constants such as ind(det) and ind(−1) are absorbed.
  - So on the four swapped coordinates ι carries normalized partial keys by a fixed affine map σ_ι, the same for
    every t.
- **Fixed partial keys** [elementary]. Take ι with trace 0, so d = −a. Then ι(s_i) = s_j gives
  (c s_i + d)(c s_j + d) = −det ι, and likewise for (s_u, s_v). So α_i + α_j = α_u + α_v = −ind(−det ι).
  - σ_ι fixes a partial key iff 2C ≡ −ind(−det ι) (mod κ) has a solution C.
  - At odd κ there is exactly one C, for every ι. At even κ there are two if −det ι is a square, i.e. ι is split
    (its fixed-point discriminant is 4·(−det ι)), and none otherwise.
  - So c_ι, the number of such C, is 1 at odd κ and 2·[ι split] at even κ. A split ι is as likely as a non-split one
    up to O(1/p), so E[c_ι] = 1 + O(1/p) (exactly 1 − 1/(p − 2) at κ = 4).
  - The referee enumerated all κ³ partial keys for 840 involutions at κ = 4–7 and found c_ι·κ fixed ones every time. This is the factor 2κ⁻⁵ (split, even κ) against κ⁻⁵ (odd κ) of §12.5.
- **κ = 4: everything is a bucket-size count** [derived; checked exactly].
  - At κ = 4, S has three involutions (its Klein group V₄), each preserving S. So σ_ι acts on full keys. It has 8 fixed
    keys if ι is split and 0 if not.
  - Every point of a σ_ι-fixed bucket is paired with its ι-image in the same bucket, apart from at most 3 exceptional
    points: the two fixed points of ι and the pole t₀ = −d/c (= ι(∞), since d = −a).
  - Hence the 2+2 count of S is a function of bucket sizes alone:
    #2+2(S) = Σ_{ι split} Σ_{K fixed} C(m_K, 2) − 2·#(free V₄-orbits inside one bucket), with m_K = (b_K − e_K)/2 and
    e_K the exceptional points in K. A free V₄-orbit is two ι-pairs for all three ι, so it is counted three times.
  - **The cross-ratio.** Normalize S to {0, ∞, 1, r}. The three involutions are x ↦ r/x, x ↦ (rx − r)/(x − r) and
    x ↦ (x − r)/(x − 1), and their −det are r, r(r − 1) and 1 − r. Their product −r²(r − 1)² is a square because
    p ≡ 1 (mod 4), so #split ∈ {1, 3}, with #split = 1 + 2·[η(r) = η(1 − r) = 1], η the quadratic character.
  - §12.12's "order-4 character sums over the cross-ratio" therefore reduce to two quadratic characters. Exactly
    (p − 5)/4 of the p − 2 values r ∉ {0, 1} have both η(r) and η(1 − r) equal to 1, so E[#split] = 1 + (p − 5)/(2(p − 2)).
    This matches the all-S counts at p = 101, 197 and 401 exactly (0.2424, 0.2462, 0.2481 of S have three).
  - **Checks** (`k4/k4_22_series.out`).
    - No bucket is partially paired.
    - Every split ι has exactly 8 σ-fixed keys and every non-split ι none (enumerated by the referee). When all 64
      buckets are nonempty, each fixed key is witnessed by a non-exceptional point or a fixed point of ι. The
      exception is a fixed bucket consisting of the pole alone (2 of 452 split ι at p = 401 in the referee's sample).
      `k4_22.py`'s "8th key witnessed only by the pole" counter does not check fixedness and is mostly inapplicable;
      no reported number depends on it.
    - The #split formula holds for every S.
    - The formula equals a brute force over all 4-subsets of every bucket in 200 S at each of p = 101, 197 and 401.
    - A 4-set that is a 2+2 for two involutions is invariant under all three, so it is a free orbit (counted three
      times) or a union of two fixed-point pairs (a 2+2 for one involution only). Hence the −2.
- **κ = 4: G is bounded, by Weil** [proof sketch; fixed κ].
  - The leading terms are N₁(S) ≈ μ₁ := 64·λ⁴/4! and #2+2(S) ≈ #split(S)·8·(λ/2)²/2 = #split(S)·λ², with
    λ = p/64. So G(S) → (2/3)·#split(S) ∈ {2/3, 2}, and G(p) → (2/3)·E[#split] → 1.
  - Exactly, G = (2/3)·E[#split]·(N₂₊₂/μ₂₊₂)/(N₁/μ₁), with the Poisson moments μ₁ = 64λ⁴/24 and μ₂₊₂ = E[#split]·λ²
    per S.
  - Each b_K counts t with prescribed quartic characters of (s_l − t)/(s_1 − t), l = 2, 3, 4. Orthogonality and
    Weil (a rational function with at most 4 zeros and poles, not a 4th power) give |b_K − (p − 4)/64| ≤ (63/64)·3√p + O(1)
    for every S and K.
  - So ε := 192/√p bounds the relative error of b_K, and uniformly in S
    G(S)/((2/3)·#split(S)) ∈ [(1 − ε)²/(1 + ε)⁴, (1 + ε)²/(1 − ε)⁴]·(1 + O(1/λ)). The same holds for G(p). The O(1/λ)
    covers the falling factorials, the e_K and the free-orbit correction (≈ 0.34/λ in the data).
  - Hence **G(S) = (2/3)·#split(S)·(1 + O(p^{−1/2})) and G(p) = 1 + O(p^{−1/2}) as p → ∞**. G(S) ≤ 2 + o(1) is
    asymptotic: at p = 101 the 3-split class has G = 2.21.
  - Weil's relative error on b_K is below 1 only for p ≳ 4·10⁴, and it brackets G within a factor 2 only for
    p ≳ 3·10⁶ (factor intervals [0.32, 3.3], [0.52, 1.97] and [0.89, 1.12] at 10⁶, 3·10⁶ and 10⁸). κ = 4's thresholds
    are near p ≈ 100–200. There Weil certifies nothing, but the exact counts do.
- **κ = 4 in the data** (exact; all S at p ≤ 401, sampled S above).

  | p | λ | N₁/μ₁ | N₂₊₂/μ₂₊₂ | G | G, 1-split S | G, 3-split S | overlap correction |
  |---|---|---|---|---|---|---|---|
  | 101 (all S) | 1.6 | 0.257 | 0.393 | 1.52 | 1.32 | 2.21 | 0 |
  | 197 (all S) | 3.1 | 0.525 | 0.614 | 1.16 | 1.02 | 1.51 | 0 |
  | 401 (all S) | 6.3 | 0.720 | 0.796 | 1.10 | 0.79 | 1.85 | 5.4% |
  | 1009 | 15.8 | 0.872 | 0.911 | 1.04 | 0.71 | 2.01 | 2.2% |
  | 2017 | 31.5 | 0.939 | 0.957 | 1.017 | 0.681 | 2.011 | 1.1% |
  | 4001 | 62.5 | 0.968 | 0.978 | 1.008 | 0.671 | 2.013 | 0.5% |
  | 8009 | 125 | 0.984 | 0.989 | 1.005 | 0.671 | 2.004 | 0.3% |
  | 16001 | 250 | 0.992 | 0.996 | 1.008 | 0.668 | 2.007 | 0.1% |
  | 32009 | 500 | 0.996 | 0.998 | 1.003 | 0.668 | 2.002 | 0.07% |

  Sampled S: 40000 at 1009, 20000 at 2017–8009, 10000 above. The predicted per-S classes are 2/3 and 2.

  - At small p, G exceeds 1 (1.52 at p = 101) because N₁/μ₁ is depressed (0.26) more than N₂₊₂/μ₂₊₂ (0.39): bucket
    sizes are under-dispersed, and that cuts C(b, 4) more than C(b/2, 2). G falls to 1 as p grows.
- **What changes at κ ≥ 5: the shape** [derived].
  - S is no longer ι-invariant: κ − 4 points are not swapped. For each such s_l, t and ιt share a bucket only if also
    ind(ι(s_l) − t) − ind(s_l − t) ≡ ω_l(K) := K_j − K_i + ind(c ι(s_l) + d) − ind(c s_j + d) (mod κ), where
    ι(s_i) = s_j. This is a one-variable condition of density 1/κ; the referee checked it against actual pairing at
    κ = 5, 6 and 7 with no mismatch.
  - So for each ι there are c_ι·κ^{κ−3} partial-fixed keys. Within them a point is paired with probability about
    κ^{−(κ−4)}, so m_K ≈ b_K·κ^{4−κ}/2. The 2+2 count of S is Σ_ι Σ_K C(m_K, 2)·C(b_K − 4, κ − 4).
  - Leading terms: with b_K ≈ λ = p/κ^{κ−1}, s = E[c_ι]·N_inv²κ⁴/p²·(1 + O(1/λ) + O(κ^{O(1)}/p)) =
    E[c_ι]·R₂₊₂·(1 + …). So R₂₊₂ is the leading term, and **G → E[c_ι] = 1 at every fixed κ as p → ∞**.
  - The lower-order pieces are: T with three or more ι-pairs (possible from κ = 6), which the sum counts more than
    once; T that is a 2+2 for two involutions; and ι with a third swapped pair or a fixed point inside S, where an
    l-condition degenerates (probability O(κ²/p) per ι).
  - For fixed S both N₁(S) = Σ_K C(b_K, κ) and the 2+2 count are polynomials in one-variable counts. b_K involves κ
    points and m_K involves 2κ − 4 points with 2κ − 5 conditions. Weil bounds each with error O(κ√p) against main
    terms p/κ^{κ−1} (b_K) and p/(2κ^{2κ−5}) (m_K). So b_K is controlled from p ≥ κ^{(2+o(1))κ} and m_K from
    p ≥ κ^{(4+o(1))κ}. With relative errors ε_b and ε_m, G = 1 + O(ε_m + κε_b). **So Weil gives G = 1 + o(1) once
    p ≥ κ^{(4+o(1))κ}.**
  - This corrects §12.12's "relative error κ^{O(κ²)}/√p, useless unless p ≥ κ^{cκ²}", for N₁ as well as for the 2+2
    family. The referee withdrew its round-4g endorsement of that wording.
  - The thresholds are κ^{(1/2+o(1))κ}, so Weil still misses by a factor κ^{(3.5+o(1))κ} in p. There m_K's main term
    is far below 1: the family consists of rare coincidences of a one-variable pattern of length 2κ − 5.
  - Bounding G near the thresholds is therefore a question about the joint factorial moments of (b_K, m_K) at
    λ ≈ 1: do the sparse patterns cluster in buckets by more than κ^{o(κ)} over Poisson? No method is in hand.
- **κ = 5, pre-registered and scored** (`k4/predictions_k5_22.txt`; `k4/k5_22_series.out`).

  | p | λ | S | N₁/μ₁ | witnessed partial-fixed keys | paired fraction | pairs per ι, split / non-split (main) | G |
  |---|---|---|---|---|---|---|---|
  | 1451 | 2.3 | 4000 | 0.75 | 11–25 | 0.195 | 5.64 / 5.68 (5.80) | 1.17 |
  | 2521 | 4.0 | 4000 | 0.86 | 17–25 | 0.197 | 9.93 / 10.00 (10.08) | 1.06 |
  | 5011 | 8.0 | 3000 | 0.93 | 23–25 | 0.199 | 19.85 / 19.97 (20.04) | 1.05 |
  | 20011 | 32 | 1500 | 0.98 | 25 | 0.1995 | 79.84 / 79.85 (80.04) | 1.011 |
  | 50021 | 80 | 600 | 0.99 | 25 | 0.1998 | 199.9 / 200.0 (200.1) | 1.002 |
  | 100151 | 160 | 300 | 1.00 | 25 | 0.1998 | 399.8 / 400.7 (400.6) | 0.999 |

  - P1 held: every ι has exactly 25 partial-fixed keys (a count of keys; the referee enumerated it for 270 ι). No
    paired point lay outside them in 201,000 involutions. At small λ only 11–25 of the 25 buckets hold a witnessing
    point.
  - P2 held: 0.195–0.1998 against 1/5.
  - P3 held: split and non-split agree within 1% at every p. There is no dichotomy, unlike κ = 4.
  - P4 held: G is 1.17 and 1.06 at the threshold-size primes 1451 and 2521 (band 0.4–3), and 1.011, 1.002 and 0.999 at
    p ≥ 20011 (band 0.75–1.33).
  - P5 is a statement: no tested p is in Weil's range for κ = 5.
  - At 1451 a partial-fixed bucket holds about 0.23 ι-pairs on average, so m_K ≪ 1, yet G is 1.17. In this one case
    the sparse patterns do not cluster much. That is an observation at κ = 5, not a bound.
  - G is computed without the overlap correction (T a 2+2 for two involutions), which at κ = 4 was 0 to 5.4%.

- **Consistency with κ = 6 and 7.**
  - Even κ predicts only split involutions in the family. That is what §12.4 found at κ = 6 (0 of 845–1459
    structured T per prime from a non-split ι).
  - G → 1 is consistent with the measured 0.58–1.05 (κ = 6, capped) and 0.5–2 (κ = 7). Those are threshold-range values, which do not test
    the theory: it gives no bound there.
- **What is and is not shown.**
  - Shown at κ = 4 (fixed κ, by Weil; a sketch with explicit constants): G(S) = (2/3)·#split(S)·(1 + O(p^{−1/2})),
    and G(p) = 1 + O(p^{−1/2}). Exact counts and their closed form are checked at p ≤ 32009.
  - Shown at every fixed κ (sketch): G(p) → 1, and Weil gives it from p ≥ κ^{(4+o(1))κ}.
  - Not shown: any bound on G at the thresholds, at κ ≥ 5 or uniformly in κ; anything about ρ_rest.
- **Claim gates stay false:** G bounded near the thresholds; G bounded uniformly in κ; obstruction (c) resolved;
  the fixed-κ sketch as a theorem without a written proof and a human check; "Weil controls G at κ = 4 for
  p ≳ 4·10⁴"; "the pole witnesses the 8th key in about 19% of split ι at p = 401".
