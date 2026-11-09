## 12. Spike primes at κ = 6: survey, mechanism, and what reaches the threshold path (follow-up, 10 Nov)

Question (mechanical plan item 1, §11.9): does OSC′ hold at λ ≤ 0.25 at spike primes, and what are spikes made
of? Everything here is Monte Carlo or heuristic, and nothing is a certificate. Code and outputs are in `osc-mc/`.
An independent AI referee checked §12.3–§12.6 (`osc-mc/review-2026-11-10/REPORT.md`, with the author's disposition
of each point). Its corrections are applied: a factor 2 in the heuristic at even κ, an undercount in the first
`pairsym.py`, and the wording of the predictor and split claims.

### 12.1 Survey design [computed]

- **Primes and runs.**
  - Every p ≡ 1 (mod 6) in [1500, 2400] and [3800, 4300]: 89 primes, λ = 0.197–0.307 and 0.49–0.55.
  - Each runs `mc_classes.py 6 p N --seed 13`, S-batched, with N = 5000 configurations below 1700, 10⁴ up to 2400
    and 2·10⁴ above (`survey/k6_survey_primes.txt`, `survey/run_k6_survey.sh`, nice 19, four at a time).
- **Analysis.** `k6_spike_survey.py` (→ `k6_spike_survey.out`) prints, per prime:
  - N₁/μ₁ with its S-batch se;
  - the debiased PW_pair with its null floor and the CS upper estimate;
  - B_L and B_D with jackknife z and 2σ upper end (the `equal_p_chain.py` estimators);
  - the noise-law c and the cluster-corrected B^cl;
  - K and max|D|/√p;
  - ind(−1), ind(2), ind(3), ind(−3) mod 6;
  - symR (§12.3).
- **Spike flags per λ band.** sD: the 2σ lower end of B_D is above twice the band median. sPW and sN apply the same
  rule to PW_pair and N₁/μ₁.
- **Status.** INTERIM: n of 89 primes are finished (λ ≤ …). The rest runs at about 1 core-h per prime at 10⁴
  configurations; `k6_spike_survey.py` rebuilds every table below.

### 12.2 Results so far [computed; interim]

| λ band | primes | median B_L / B_D / PW_pair / N₁/μ₁ | max B_L, B_D (p) | spikes |
|---|---|---|---|---|
| 0.197–0.218 | 14 | 0.50 / 0.82 / 2.81 / 0.97 | 1.88, 10.5 (1657) | 6: 1531 sN; 1597 sD sPW sN; 1627 sN; 1657 sD sPW sN; 1669 sD; 1693 sD sPW |
| 0.222–0.225 | 3 | 0.39 / 0.48 / 1.77 / 0.69 | 0.55, 0.59 (1753) | none |
| earlier, seed 11 | 1933 (0.249) | 1.20 / 3.67 / 7.17 / 2.63 | | spike (§11.6) |
| earlier, seed 11 | 2347 (0.302) | 0.41 / 0.34 / 0.75 / 0.76 | | typical |

- **Largest spike.** 1657 has B_L 1.88 (z 21), B_D 10.5 (z 10.6, 2σ upper 11.5), PW_pair 30.1, N₁/μ₁ 4.47 and c 2.50.
  Next is 1597: B_L 1.20, B_D 4.00, PW_pair 10.9, N₁/μ₁ 4.36.
- **Typical primes.** At λ ≈ 0.21 they have B_L 0.32–0.54, B_D 0.38–0.93 (ν_D 0.69–1.18, so mostly at the noise
  level) and N₁/μ₁ 0.39–1.15.
- **Count spikes without value spikes.** At 1531 and 1627 N₁/μ₁ is 4.11 and 2.64, but B_D is only 0.63 and 1.00
  (§12.7).
- **PW_pair.** It is above 1.4 at every prime with λ ≤ 0.25. The noise-only crossing is λ ≈ 0.22, and the κ = 6
  threshold of §11.8 is λ_T = 1.3, so all of these primes lie below the range a κ = 6 certificate would use.

### 12.3 symR, a cheap spike indicator [computed]

- **The script.** `sym_rate.py k nS p…` samples the S that are unions of κ/2 pairs of a split involution. Every split
  involution is conjugate to x ↦ −x, so these are S = {±r₁, ±r₂, ±r₃}. It prints:
  - symR, their configurations per S relative to Poisson;
  - the share of those configurations coming from involution-fixed buckets (0.69–0.99 at κ = 6, λ ≤ 0.31);
  - the share f ≈ 7.5/p of such S among all S;
  - C_sym = f·symR/Poisson.

  A run uses 10⁵ symmetric S, about 1% of the cost of a survey run.
- **What it omits.** S symmetric under a non-split involution (x ↦ ε/x) are left out. They have no fixed buckets,
  and their rate is small (0.56 and 0.89 × Poisson at 1621 and 1657, but 26 ± 13 at 1531). So C_sym is a lower
  estimate.
- **N₁/μ₁ tracks symR.**
  - Spearman 0.90 over the 17 survey primes (bootstrap 95% interval 0.64–0.98 at n = 15).
  - At λ ≈ 0.2, N₁/μ₁ ≈ 0.038·symR, with log-sd 0.18 over 13 primes. That is about the size of the sampling
    errors (symR se 6–15%, N₁/μ₁ se 2–10%).
  - symR also ranks B_L (0.85) and B_D (0.77).
- **A fit across λ.**
  - The fit log N₁/μ₁ = −0.14 + 0.98 log symR + 1.93 log λ, on 14 primes, reproduced 1933, 2347 and 4219 within 0.15
    in log.
  - Those three were held out only because their log files had other names.
  - The first two prospective primes, 1699 and 1747, came in at −0.16 and +0.33.
  - The λ-term is calibrated on the one λ = 0.5 prime 3877 (without it the coefficient is −2.06). Predictions for
    all unfinished primes were written at 01:20 (`survey/predictions_N1mu1.txt`).
- **symR is not the mechanism.** The fully symmetric S carry only C_sym ≈ 1/8 of N₁/μ₁ (median ratio 8.05,
  quartiles 7.6–10.1). symR measures a property of the prime that also drives the rest of the measure (§12.4).

### 12.4 Mechanism: partial involution symmetry [computed]

- **Definitions.**
  - A Möbius involution ι is fixed by two of its 2-cycles. So a κ-set S has N_inv = C(κ,2)C(κ−2,2)/2 involutions
    swapping two disjoint pairs of S: 45 at κ = 6, 105 at κ = 7.
  - A configuration (S, T) is **2+2 structured** if one of these ι also has two ι-pairs {t, ι(t)} inside T.
  - Involutions over F_p come in two classes. Split ones fix two points of P¹(F_p) and are conjugate to x ↦ −x.
    Non-split ones are conjugate to x ↦ ε/x with ε a non-square. Each class makes up about half.
- **Counting.** `pairsym.py k p nS` counts, for every full S-bucket, the k-subsets T that are 2+2 structured. The
  count is exact: it takes the union over ι, whereas a first max-over-ι version undercounted by up to 16 points.
  `--null` replaces the bucket by a random b-set.

  | p | λ | kind | N₁/μ₁ (same sample) | 2+2 share | 2+2 counting ι-fixed points |
  |---|---|---|---|---|---|
  | 1597 | 0.205 | spike | 3.97 | 0.875 | 0.915 |
  | 1621 | 0.208 | typical | 0.42 | … | … |
  | 1627 | 0.209 | sN | 2.05 | 0.780 | 0.826 |
  | 1657 | 0.213 | spike | 3.71 | 0.830 | 0.886 |
  | 1933 | 0.249 | spike | 2.72 | 0.700 | 0.774 |
  | 2347 | 0.302 | typical | 0.80 | 0.444 | 0.514 |
  | 3877 | 0.499 | typical | 0.84 | 0.167 | 0.192 |
  | random b-sets | | null | | ≈ 0.002 (b = 6) | |

  The κ = 6 samples are seed 5, with 3·10⁵ S (6·10⁴ at 3877, 1.5·10⁶ at 1621).
- **Only split involutions occur.** At κ = 6 no structured T comes from a non-split ι (0 of 845–1459 per prime,
  referee); §12.5 says why.
- **Split of the class values.** `mc_split.py` uses the same random stream as `mc_classes.py` and reproduces it
  configuration by configuration. Its parts sum to the total, and `split_report.py` reports them (seed 13, 5000
  configurations).

  | p | part | share | N₁/μ₁ | PW_pair | B_L | B_D (z) | c |
  |---|---|---|---|---|---|---|---|
  | 1657 | all | 1 | 4.47 | 30.1 | 1.88 | 10.5 (10.6) | 2.50 |
  | | 2+2 | 0.833 | 3.72 | 33.0 | 2.00 | 11.6 (12.0) | 2.60 |
  | | not 2+2 | 0.167 | 0.75 | 15.9 | 1.35 | 5.8 (3.8) | 2.00 |
  | 1597 | all | 1 | 4.36 | 10.9 | 1.20 | 4.00 (7.4) | 1.53 |
  | | 2+2 | 0.860 | 3.75 | 11.5 | 1.25 | 4.28 (7.9) | 1.57 |
  | | not 2+2 | 0.140 | 0.61 | 7.6 | 0.93 | 2.59 (4.5) | 1.29 |
  | 1933 | all | 1 | 3.07 | 7.25 | 1.24 | 3.84 (7.4) | 1.36 |
  | | 2+2 | 0.762 | 2.34 | 8.23 | 1.32 | 4.42 (7.4) | 1.39 |
  | | not 2+2 | 0.238 | 0.73 | 4.76 | 1.00 | 2.28 (8.2) | 1.25 |
  | 1621 | … | | | | | | |

- **How to read the split** (with the referee's correction).
  - 39–48% of the not-2+2 configurations at the spike primes lie in a bucket that also holds 2+2 T's.
  - Their class values point the same way as the 2+2 part's, at 0.55–0.73 of the size: weighted cosine 0.97–0.98
    over L and 0.59–0.92 over D.
  - The not-2+2 rate is 0.55–0.79 μ₁ at the spike primes, against ≈ 0.1 μ₁ at 1621.
  - So one S- and bucket-level mechanism lifts the whole (C1) measure at a spike prime. The per-T 2+2 flag captures
    its core, about 80% of the configurations; "not 2+2" does not mean unstructured.

### 12.5 Why such families matter only at small p [heuristic; corrected after review]

1. **The 4×4 block.**
   - Normalise a split ι to x ↦ −x, with rows (a, −a, b, −b), columns (x, −x, y, −y) and h = ind(−1). Write
     P = ind(r − x) and Q = ind(r + x).
   - Then M[r, x] = P, M[r, −x] = Q, M[−r, x] = h + Q and M[−r, −x] = h + P.
   - Rank 1 forces P − Q ≡ c on the whole block, with 2c ≡ 0, and forces P itself to be rank-1.
   - So the probability is 2κ⁻⁵ at even κ (c ∈ {0, κ/2}) and κ⁻⁵ at odd κ, against κ⁻⁹ for a generic 4×4 block.
   - For a non-split ι(x) = ε/x, each 2×2 pair block needs 2(ind(a − x) − ind(ax − ε)) ≡ −ind ε (mod κ). At even κ
     there is no solution, because ind ε is odd; at odd κ there is exactly one.
   - Averaged over the two classes, the enhancement is κ⁴ at every κ.
   - Checks: the referee measured the 2×2 rate at κ = 6 as 0.332 for split and 0 for non-split involutions, and
     0.143 for both at κ = 7. `block_rate.py` (split only, 11 primes, 4·10⁶ samples each) finds 0.87–1.03 of 2κ⁻⁵.
     Three primes sit 3–4σ low, and the ratio has rank correlation 0.67 with N₁/μ₁ over 9 primes, but the effect
     is under 13%.
2. **The 2+2 weight.**
   - For a fixed ι, a uniform T contains two ι-pairs with probability ≈ N_inv/p².
   - If the remaining (κ−1)² − 9 conditions behave independently, the structured configurations have rate
     R₂₊₂(κ, p) = N_inv(κ)²·κ⁴/p² relative to μ₁.
   - κ = 6: R₂₊₂ = 2.62·10⁶/p². That is 1.03 at 1597, 1.00 at 1621, 0.96 at 1657, 0.70 at 1933, 0.48 at 2347 and 0.17
     at 3877.
   - κ = 7: R₂₊₂ = 2.65·10⁷/p², 0.021 at 35281.
   - At fixed λ = 0.2 it is 1.1, 0.048 and 0.0010 at κ = 6, 7, 8.
3. **The arithmetic factor.**
   - The measured structured rate (2+2 share × N₁/μ₁) is F(p)·R₂₊₂.
   - At κ = 6: F ≈ 0.3 at 1621, 3.2–3.9 at 1597 and 1657, 2.6–3.3 at 1933, 0.7 at 2347 and 0.8 at 3877. Each range
     comes from using N₁/μ₁ from the pairsym sample or from the survey or split runs.
   - At κ = 7: 1.8 at 35281 (19 structured configurations) and 0.5 at 35099 (5).
   - The p⁻² law matches the size and the fall-off with p. F varies 13× between κ = 6 primes and is not predicted
     (§12.7).
4. **General families.**
   - Take g ∈ PGL₂ of order m, with a g-orbits in S and b in T, and set x = am/κ, y = bm/κ.
   - The codimension in (S, T) is c = (a+b)(m−1) − 2. The rank-1 deficit is E = (m−1)(abm − a − b): E = 4 for the 2+2
     block and κ²/2 − κ for full involution symmetry.
   - There are κ^{O(κ)} placements and an O(1) solvability factor. At p = κ^{γκ} this gives
     log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ).
   - Since xy ≤ (x + y)/2, every family with x + y bounded below is negligible once γ > 1/2 + O(1/κ). Families with
     x + y = O(1/κ) satisfy E/c ≤ κ/2 + O(1), which gives the same conclusion.
   - Full involution symmetry (even κ, averaged over the two classes): R_full = ((κ−1)!!)²κ^{κ²/2−κ}p^{2−κ}
     (κ = 6: 4.9·10¹¹/p⁴). This is < 1 once p > κ^{κ/2+1−1/ln κ+o(1)}.
5. **Along the threshold path.**
   - The exponent needs OSC′ at T(κ) = κ^{κ/2+κ/(2 ln κ)+O(1)} (§11.8). There R₂₊₂ = κ^{12−κ−κ/ln κ+O(1)} and
     R_full = κ^{−κ²/(2 ln κ)+O(κ)}.
   - At the typical-constant thresholds of §11.8, R₂₊₂ is 0.026 (κ = 6, p ≈ 10⁴), 0.010 (κ = 7), 0.0012 (κ = 8),
     1.1·10⁻⁴ (κ = 9) and 7.6·10⁻⁶ (κ = 10).
6. **The family's effect on the constants.**
   - Suppose a family has share w ≪ 1 and absolute D-group rms v. It changes ρ_D by at most w·v, which is
     F·v·N_inv²κ²/p in units of κ²/p.
   - At T(κ), N_inv²κ²/p is 10.6, 7.4, 3.9 and 1.7 for κ = 7, 8, 9, 10, and it tends to 0 like
     κ^{10−κ/2−κ/(2 ln κ)+O(1)}.
   - With the largest κ = 6 values (1657: F ≈ 3.9, v = 0.25), the family would add B_D ≈ 10, 7, 4, 2 at κ = 7–10.
     With typical values (1621: F ≈ 0.3, v = …) it would add ….
   - The L group (absolute units) gains at most w·v_L ≤ 0.04·2.0 = 0.08 at κ = 7, and less beyond.
   - So the family alone cannot make the constants grow along the path. At κ = 7–9 it could hold B_D at spike size
     only if both F and v stay at their κ = 6 maxima. How v scales with p and κ is not measured.
7. **What this does not say.** It is a first-moment count with an independence assumption. It bounds weights, not
   class values, of projective families of bounded orbit type. It says nothing about structure that is not
   projective.

### 12.6 κ = 7 at λ ≈ 0.3 [computed]

- **Runs.** `bucket_stats.py 7 p 2·10⁵ --seed 21`, with uniform S, prints configurations per S against Poisson, the
  occupancy law and its tail. `pairsym.py 7 p 10⁵` counts the 2+2 share.

  | p | λ | symR | N₁/μ₁ | var/mean | b = 7, 8 vs Poisson | 2+2 share |
  |---|---|---|---|---|---|---|
  | 35281 | 0.300 | 15.8 | 0.90 | 0.999 | 0.95, 0.92 | … |
  | 35099 | 0.298 | 21.3 | 0.96 | 0.999 | 0.93, 1.07 | … |
  | 36037 | 0.306 | 44.2 | 1.09 | 0.999 | 1.01, 1.42 | … |
  | 34693 | 0.295 | 44.2 | … | | | … |
  | 34259 | 0.291 | 22.1 | … | | | |
  | 34469 | 0.293 | 16.7 | … | | | |

- **The test.** It is the two primes with the largest symR: 44, against 9.4–22 at the seven others (median 16.7).
  At κ = 6 N₁/μ₁ is proportional to symR, so a 2.6× higher symR would mean N₁/μ₁ ≈ 2.5. Measured: 1.09 at 36037
  and … at 34693. This is what §12.5 predicts: the 2+2 weight is 0.02 at κ = 7, λ = 0.3, against ≈ 1 at κ = 6,
  λ = 0.2.
- **Class values at 36037.** `mc_classes.py 7 36037 10⁴ --seed 13` gives B_L …, B_D … (2σ < …), PW_pair …, c ….
- **The κ = 6 tail at a similar λ, for contrast.** At λ = 0.25 the tail is 1.8× and 4.5× Poisson at b = 7, 8 for
  1951 (N₁/μ₁ 1.42), and 3.7×, 21× and 690× at b = 7, 8, 10 for the spike 1933. The not-2+2 rate at typical κ = 6
  primes is ≈ 0.1, 0.44 and 0.70 μ₁ at λ = 0.21, 0.30 and 0.50. At κ = 7, λ ≈ 0.3 the generic rate is close to the
  random model.

### 12.7 Arithmetic of spike primes [computed; post hoc]

- **B_D spikes sit at p ≡ 1 (mod 12)** (ind(−1) ≡ 0 mod 6).
  - B_D > 2 occurs only there: 1597, 1657, 1669, 1693 and 1933.
  - The 9 survey primes ≡ 7 (mod 12) have B_D ≤ 1.00, though two of them are N₁/μ₁ spikes (1531 at 4.11, 1627 at
    2.64).
  - Class medians: B_D 1.65 against 0.63; N₁/μ₁ 1.22 against 0.65.
  - With no dependence on the class, the top four of 17 would all fall in the class of 8 with probability 0.03, or
    about 0.1 after allowing for the 4 symbols looked at.
- **No mechanism is known.** A first guess was that z and −z contribute with phases e^{2πijh/6}. It fails: the
  class modes are sum-zero and taken up to cyclic shifts of the values. For a configuration symmetric under
  x ↦ −x, U(−z) is a permutation of U(z) plus a constant vector, so z and −z contribute equally whatever h is (the
  correction is appended to the prediction file). At odd κ, h = 0 for every p.
- **What drives symR at h = 0.** Detrend log symR in λ; the residual has sd 0.54. At p ≡ 1 (mod 12) it is ranked by
  |A(0,0) − mean|/√p, where A(0,0) is the order-6 cyclotomic number #{x ∈ H : x + 1 ∈ H}. Spearman is 0.81 over 30
  primes with λ ≤ 0.31. At p ≡ 7 (mod 12) the matching cell A(0,3) gives only 0.27. So at h = 0 one Jacobi-sum
  statistic tracks symR. At h = 3 nothing found so far does.
- **Other statistics.** K (§11.5) has Spearman 0.73 with N₁/μ₁ and 0.54 with B_D; max|D|/√p has 0.38 with B_D. Both
  are weaker than symR.
- **Prospective tests** (`survey/predictions_hclass.txt`, 02:16).
  - (H1) Every new sD prime is ≡ 1 (mod 12).
  - (H2) In each band, the median B_D is larger at p ≡ 1 (mod 12).
  - (H3) sN spikes occur in both classes.
  - Together with the N₁/μ₁ predictions of §12.3, these are checked when the survey finishes. 1789 (h = 0,
    symR 115, predicted N₁/μ₁ 5.3) is the sharpest single test.

### 12.8 Answer, and what it changes

- **Answer [computed at κ = 6, 7; heuristic beyond].**
  - At κ = 6, λ ≤ 0.25, the group form OSC′_rms holds at every measured prime. The constants reach
    (B_L, B_D) = (1.88, 10.5) at 1657, against band medians (0.50, 0.82), and 6 of the 14 primes below λ = 0.22 are
    spikes by some flag.
  - At fixed κ OSC′ asks only for finite constants, so this is no counterexample. But spike constants at κ = 6 are
    up to 4× (B_L) and 13× (B_D) typical.
- **The spikes are projective structure.**
  - 78–88% of the configurations at the spike primes 1597, 1627 and 1657 are 2+2 involution-structured (70% at
    1933). The rest share their buckets and point the same way.
  - The family's weight follows N_inv²κ⁴/p² up to F(p) ≤ 3.9. So spike strength at fixed κ is a small-p effect,
    not a small-λ one.
  - The steep rise of spike amplitude as λ falls (§11.8 (c)) is a rise as p falls.
- **κ = 7 agrees.** At λ ≈ 0.3 the 2+2 share is 1–4% (expected 2.4%), and N₁/μ₁ is 0.90–1.09 across symR 16–44.
- **What changes.**
  - Obstruction (c) of §11.8 loses its main evidence. Along the threshold path, the 2+2 family has weight ≤ 1% from
    κ = 7 on. With the largest κ = 6 values it would add B_D ≤ 10 at κ = 7, falling to 0 (§12.5, item 6). That is a
    bounded constant, harmless for the exponent statement.
  - (c) is not removed. F(p) is unexplained and could be large at rare primes, the family's class values are
    measured only at κ = 6, and structure that is not projective is not excluded.
- **Claim gates that stay false.**
  - OSC′ in either form at any κ.
  - Any rigorous bound on spike constants.
  - R₂₊₂ as a theorem.
  - Threshold certificates at κ ≥ 6.
  - An unconditional exponent statement.

### 12.9 Next

- **Finish the survey.** Run `k6_spike_survey.py` and check `survey/predictions_N1mu1.txt` and
  `survey/predictions_hclass.txt`. Acceptance: spike frequency and amplitude per band, and H1–H3 kept or refuted.
- **The direct test of (c)** still needs κ = 8 at λ ≈ 0.18 (p ≈ 3.8·10⁵) with a sampler that builds (C1)
  configurations (§11.9). That sampler is the main gap.
- **A cheaper proxy.** Measure the 2+2 family's absolute D-rms v at a second κ (κ = 7 at λ ≈ 0.3 through
  `mc_split.py`; the share there is only ~2%, so the sampler must be conditioned on 2+2 structure). That would show
  whether v falls with p.
- **Prove the weight.** Bound the number of 2+2-structured (C1) configurations above by O(N_inv²κ⁴p⁻²μ₁). The 4×4
  block conditions are explicit, and the rest is the (N)-type count of §9 on a codimension-2 family.
