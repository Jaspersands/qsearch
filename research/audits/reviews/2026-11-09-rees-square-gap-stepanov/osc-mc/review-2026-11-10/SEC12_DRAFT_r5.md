## 12. Spike primes at κ = 6: survey, partial involution structure, and the threshold path (follow-up, 10 Nov)

Question (mechanical plan item 1, §11.9): does OSC′ hold at λ ≤ 0.25 at spike primes, and what are spikes made of?
Everything here is Monte Carlo or heuristic unless marked otherwise; nothing is a certificate. Code and outputs are in
`osc-mc/`.

An independent AI referee checked the section in eight passes. Rounds 1–2, with the author's disposition of each
point, are in `osc-mc/review-2026-11-10/REPORT.md`; rounds 3, 3b, 3c, 4, 4b and 4c and their dispositions are in
`ROUND3.md`. Its corrections are applied:
- a factor 2 in the heuristic at even κ;
- an undercount in the first `pairsym.py`;
- a misattributed cyclotomic correlation, and a false identification of |a|/√p with §11.6's |L|/(2√p);
- overstated readings of the mechanism and of what it implies;
- a stale survey snapshot, and a spike (1627) missing from the F table;
- an over-read of the N₁/μ₁ prediction at λ ≈ 0.5, and two threshold cases counted as refutations of H1;
- a wrong "median symR" for 35099, and missing 2σ ranges on the bin ratios. The author replaced a knife-edge pairwise
  calibration of 36037 with the ratio to the band median, and the referee confirmed it.

### 12.1 Survey design [computed]

- **Primes and runs.** Every p ≡ 1 (mod 6) in [1500, 2400] and [3800, 4300]: 89 primes.
  - 29 have λ ≤ 0.25, 31 have λ in (0.25, 0.31], and 29 have λ ≈ 0.49–0.55.
  - Each runs `mc_classes.py 6 p N --seed 13`, S-batched. N is 5000 configurations below 1700, 10⁴ up to 2400 and
    2·10⁴ above.
  - The prime list and driver are `survey/k6_survey_primes.txt` and `survey/run_k6_survey.sh` (nice 19, four at a
    time).
- **Analysis.** `k6_spike_survey.py` prints, per prime:
  - N₁/μ₁ with its S-batch se;
  - the debiased PW_pair with its null floor and the CS upper estimate;
  - B_L and B_D with jackknife z and 2σ upper end (the `equal_p_chain.py` estimators);
  - the noise law c, the cluster-corrected B^cl, K and max|D|/√p;
  - ind(−1), ind(2), ind(3), ind(−3) mod 6;
  - symR (§12.3).
- **Spike flags, per λ band.**
  - sD: the 2σ lower end of B_D is above twice the band median.
  - sPW and sN: the debiased PW_pair, or N₁/μ₁, is above twice the band median. These two flags use the point
    value, with no se, as `k6_spike_survey.py` defines them; the H file defines sN the same way.
  - In a band that is not yet complete the medians, and so the flags, are provisional.
- **Status: complete.** §12.2–12.8 were written from the 35-prime snapshot of 03:45 on 10 Nov
  (`review-2026-11-10/survey_snapshot.out`). The final run (04:49, all 89 primes, `k6_spike_survey.out`) changes
  nothing at λ ≤ 0.25. The completed bands are in §12.2's table, and the scored predictions in §12.10. Rerunning
  `k6_spike_survey.py` rebuilds every table.

### 12.2 Results [computed]

| λ band | primes | median B_L / B_D / PW_pair / N₁/μ₁ | max B_L, B_D (p) | flagged |
|---|---|---|---|---|
| 0.197–0.218 | 14 | 0.50 / 0.82 / 2.81 / 0.97 | 1.88, 10.5 (1657) | 6: 1531 sN; 1597 sD sPW sN; 1627 sN; 1657 sD sPW sN; 1669 sD; 1693 sD sPW |
| 0.222–0.249 | 15 | 0.55 / 0.59 / 1.77 / 0.82 | 1.77, 14.8 (1789) | 3: 1759 sN; 1789 sD sPW sN; 1933 sD sPW sN |
| 0.251–0.307 | 31 | 0.45 / 0.44 / 1.04 / 0.81 | 1.16, 6.59 (2113) | 8: 2053 sD sPW; 2113 sD sPW sN; 2137 sD; 2143 sD sPW sN; 2179 sD; 2221 sD sPW; 2269 sD sPW; 2341 sD sPW sN |
| 0.492–0.553 | 29 | 0.33 / 0.24 / 0.32 / 0.80 | 0.63, 1.42 (3889) | 4: 3823 sD sPW; 3889 sD sPW; 4057 sPW; 4129 sD sPW |

- **Largest spike: 1789.**
  - B_L 1.77, B_D 14.8 (z 9.2, 2σ upper 16.4), PW_pair 31.7, N₁/μ₁ 4.50, c 2.66.
  - This is the largest B_D measured at any κ; the κ = 4 and 5 maxima are 2.07 and 3.04. It is 25× its band median
    and 18× the λ < 0.22 median.
  - Next is 1657: B_L 1.88, B_D 10.5, PW_pair 30.1, N₁/μ₁ 4.47.
- **Typical primes.**
  - At λ ≈ 0.21 they have B_L 0.32–0.54, B_D 0.38–0.93 and N₁/μ₁ 0.39–1.15.
  - The noise level there is ν_D 0.69–1.18, so most of these B_D values are noise.
  - N₁/μ₁ goes as low as 0.37 (1741), so (N) of OSC′ needs B ≈ 2.7 at these primes. (N) enters only the noise term
    of §11.8, which never dominates.
- **Count spikes without value spikes.** 1531, 1627 and 1759 have N₁/μ₁ 4.11, 2.64 and 1.89 but B_D only 0.63, 1.00
  and 0.49. All three are ≡ 7 (mod 12) (§12.7).
- **N₁/μ₁ is heavy-tailed at spike primes.**
  - Single S with buckets of 10–12 points carry much of the count. At 1933, 71% of the configurations of a 3·10⁶-S run
    come from the top 0.1% of S (`buckets/bucket_k6_p1933.out`).
  - Samples of the same prime differ by up to 1.8×, in no consistent direction. At 1789 the pairsym sample gives 2.53
    and the survey 4.50. At 1933 the largest sample (3·10⁶ S) gives the lowest value, 2.55, against 2.63–3.07
    elsewhere.
  - So the S-batch se understates the uncertainty at spike primes, by a factor of about 2 or more.
- **What "holds" means here.**
  - At fixed κ any finite set of primes satisfies OSC′ with some constants, so the survey measures their size.
  - PW_pair is above 1 at every prime with λ ≤ 0.25; the lowest is 1.14, at 1879. The κ = 6 threshold of §11.8 is
    λ_T = 1.3, so none of these primes is in the range a κ = 6 certificate would use.
  - The first value below 1 is at 2011 (λ 0.259, PW_pair 0.92). At λ ≈ 0.5 the debiased PW_pair is below 1 at all 29
    primes (28 of 29 by the CS upper estimate; §12.10).

### 12.3 symR, a cheap spike indicator [computed]

- **The script.** `sym_rate.py k nS p…` samples the S that are unions of κ/2 pairs of a split involution. Every
  split involution is conjugate to x ↦ −x, so these are S = {±r₁, ±r₂, ±r₃}. It prints:
  - symR, their configurations per S relative to Poisson;
  - the share of those configurations that come from involution-fixed buckets (0.69–0.99 at κ = 6, λ ≤ 0.31);
  - the share f ≈ 7.5/p of such S;
  - C_sym = f·symR.

  10⁵ symmetric S per prime cost about 1% of a survey run.
- **What it omits.** S symmetric under a non-split involution (x ↦ ε/x) are left out. They have no fixed buckets
  and a small rate: 0.56 and 0.89 × Poisson at 1621 and 1657, but 26 ± 13 at 1531. So C_sym is a lower estimate.
- **N₁/μ₁ tracks symR.**
  - Spearman 0.92 over the 29 survey primes with λ ≤ 0.25.
  - N₁/μ₁ ≈ 0.038·symR at λ < 0.22 (log-sd 0.17 over 14 primes, about the size of the sampling errors), and 0.051·symR
    at 0.22–0.25 (log-sd 0.25 over 15 primes).
  - symR also ranks B_L (0.92) and B_D (0.77).
- **Prospective test.**
  - The fit log N₁/μ₁ = −0.14 + 0.98 log symR + 1.93 log λ, on 14 primes, was used to predict every unfinished prime
    (`survey/predictions_N1mu1.txt`).
  - The file's header says 01:20, and its mtime is 01:48. 1699 finished at 01:33, between the two. The fit does not
    use 1699, and the error there is −0.15.
  - The 15 primes with λ ≤ 0.25 that finished since (1699–1879, λ 0.218–0.242) came in with rms log error 0.24 (mean
    +0.04, largest 0.37 at 1879). That is close to the in-sample residual sd of 0.20.
    - They include the largest spike, 1789: 4.50 against a predicted 5.25.
  - At the snapshot, the 6 primes above λ = 0.25 had rms 0.25 (mean +0.06). The largest error is +0.44, at 1951: 1.42
    against 0.91.
  - Final (§12.10): rms 0.19 over all 31 primes in (0.25, 0.31] and 0.13 over the 28 at λ ≈ 0.5. At λ ≈ 0.5 the level
    holds, but the slope is rejected (0.40 ± 0.07 within the band), so there the law has no predictive power.
  - The λ-term rests mostly on the one λ = 0.5 prime 3877. Without it, the λ coefficient is −2.06 instead of +1.93.
    - The prospective primes test it weakly. They sit 0.10 higher in log λ, and they reject the fit without 3877 (mean
      error +0.42, rms 0.47). The referee estimates that they need a coefficient of 2.0 ± 0.6.
    - They do not separate a λ-term from a flatter symR slope. Also, the configuration count changes at p = 1700.
- **symR is not the mechanism.** The fully symmetric S carry C_sym ≈ 1/9 of N₁/μ₁ (median ratio 9.35, quartiles
  7.8–12.4, λ ≤ 0.25). symR measures a property of the prime that also drives the rest of the measure (§12.4).

### 12.4 Partial involution structure of (C1) configurations [computed]

- **Definitions.**
  - A Möbius involution ι is determined by two of its 2-cycles. A κ-set S has N_inv = C(κ,2)C(κ−2,2)/2 pairs of
    disjoint pairs (45 at κ = 6, 105 at κ = 7). Each pair of pairs determines the involution that swaps both, so N_inv
    bounds the number of distinct such involutions.
  - A configuration (S, T) is **2+2 structured** if one of these ι also has two ι-pairs {t, ι(t)} inside T.
  - Over F_p, involutions are split (conjugate to x ↦ −x, two fixed points in P¹(F_p)) or non-split (conjugate to
    x ↦ ε/x, ε a non-square), about half of each.
- **Exact count.** `pairsym.py k p nS` counts, for every full S-bucket, the k-subsets T that are 2+2 structured.
  - It takes the union over ι; a first max-over-ι version undercounted by up to 16 points.
  - `--null` replaces the bucket by a random b-set.

  | p | λ | kind | N₁/μ₁ (same sample) | 2+2 share | 2+2 counting ι-fixed points |
  |---|---|---|---|---|---|
  | 1597 | 0.205 | sD spike | 3.97 | 0.875 | 0.915 |
  | 1621 | 0.208 | typical | 0.42 | 0.741 | 0.786 |
  | 1627 | 0.209 | sN spike | 2.05 | 0.780 | 0.826 |
  | 1657 | 0.213 | sD spike | 3.71 | 0.830 | 0.886 |
  | 1789 | 0.230 | sD spike | 2.53 | 0.736 | 0.805 |
  | 1933 | 0.249 | sD spike | 2.72 | 0.700 | 0.774 |
  | 2347 | 0.302 | typical | 0.80 | 0.444 | 0.514 |
  | 3877 | 0.499 | typical | 0.84 | 0.167 | 0.192 |
  | random b-sets | | null | | ≈ 0.002 (b = 6) | |

  Samples are seed 5 with 3·10⁵ S, except 6·10⁴ at 3877, 1.5·10⁶ at 1621 and 10⁵ at 1789 (the referee's run,
  `review-2026-11-10/scratch/pairsym_k6_p1789_1e5.out`).
- **Only split involutions occur.** At κ = 6 no structured T comes from a non-split ι (0 of 845–1459 per prime;
  §12.5 item 1).
- **Split of the class values.** `mc_split.py` draws the same random stream as `mc_classes.py` and reproduces it
  configuration by configuration; its parts sum to the total. `split_report.py` gives the constants per part, seed 13.

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
  | 1789 | all | 1 | 4.50 | 31.7 | 1.77 | 14.8 (9.2) | 2.66 |
  | | 2+2 | 0.804 | 3.62 | 36.7 | 1.97 | 17.3 (11.7) | 2.84 |
  | | not 2+2 | 0.196 | 0.88 | 11.9 | 1.06 | 5.5 (3.5) | 1.81 |
  | 1621 | all | 1 | 0.42 | 2.32 | 0.34 | 0.38 (2.4) | 1.03 |
  | | 2+2 | 0.708 | 0.30 | 2.81 | 0.38 | 0.44 (1.7) | 1.07 |
  | | not 2+2 | 0.292 | 0.12 | 3.33 | 0.32 | 0.76 (1.6) | 0.90 |

  Runs have 5000 configurations, except 10⁴ at 1789.
  - The 1597, 1657 and 1621 runs, and the 10⁴-configuration 1789 run, reproduce the survey runs. The 1933 run is the
    first 5022 configurations of the survey's seed-13 stream; the full survey run there has N₁/μ₁ 2.66 and B_D 3.66.
  - At 1789 the split's 2+2 share, 0.804, is higher than the 0.736 of the smaller pairsym sample (heavy tails, §12.2).
- **What the split shows.**
  - The 2+2 share is high at spike and typical primes, and separates them only modestly.
    - At λ ≈ 0.21 it is 0.83–0.88 at the sD spikes 1597 and 1657, and 0.78 at the sN spike 1627. At 1621, the one
      typical prime measured there, it is 0.71–0.74 (se ≈ 0.01).
    - At the spikes 1789 and 1933 (λ 0.23–0.25) it is 0.70–0.80.
  - What separates the four split spike primes from 1621 strongly:
    - the family's weight factor F (§12.5 item 3): 2.3–4.4, against 0.30;
    - the 2+2 part's class values: B_D 4.3–17.3, against 0.44 (z 1.7, 2σ < 0.65).
  - The not-2+2 part is lifted at those spike primes as well: rate 0.61–0.88 μ₁ against 0.12 at 1621, and B_D 2.3–5.8
    (z 3.5–8.2).
  - At 1597, 1657 and 1933 the referee also found the following (not computed at 1789):
    - 39–48% of the not-2+2 part lies in buckets that also hold 2+2 T's.
    - As a whole it points the same way as the 2+2 part, at 0.55–0.73 of the size (weighted cosine 0.97–0.98 over L
      and 0.59–0.92 over D).
    - It carries 1–3% of the total weighted |V|².
  - The data fit one S- and bucket-level property of a spike prime that raises the count and the class values of the
    whole measure. The 2+2 flag marks most of the configurations it acts on. Why some primes have this property is open
    (§12.7).

### 12.5 Weight of involution families [heuristic, except item 3 (a definition) and item 6 (an elementary bound)]

1. **The 4×4 block.**
   - Normalise a split ι to x ↦ −x, with rows (a, −a, b, −b) and columns (x, −x, y, −y). Let h = ind(−1),
     P = ind(r − x) and Q = ind(r + x).
   - Then M[r, x] = P, M[r, −x] = Q, M[−r, x] = h + Q and M[−r, −x] = h + P.
   - Rank 1 holds iff P − Q ≡ c on the whole block, with 2c ≡ 0, and P itself is rank-1.
   - That has probability 2κ⁻⁵ at even κ (c ∈ {0, κ/2}) and κ⁻⁵ at odd κ, against κ⁻⁹ for a generic 4×4 block.
   - Non-split ι(x) = ε/x: each 2×2 pair block needs 2(ind(a − x) − ind(ax − ε)) ≡ −ind ε (mod κ). At even κ there is
     no solution, because ind ε is odd. At odd κ there is exactly one.
   - Averaged over the two kinds, the enhancement is κ⁴ at every κ.
   - Checks:
     - The referee measured the 2×2 rate at κ = 6 as 0.332 for split and 0 for non-split involutions, and 0.143 for
       both at κ = 7.
     - `block_rate.py` (split only, 11 primes, 4·10⁶ samples each) finds 0.87–1.03 of 2κ⁻⁵.
     - Three primes sit 3.3–4.6σ low. The largest deficit is 13.2%. The ratio has rank correlation 0.78 with N₁/μ₁
       (10 primes).
2. **The 2+2 weight.**
   - For a fixed ι, a uniform T contains two ι-pairs with probability ≈ N_inv/p².
   - If the other (κ−1)² − 9 conditions behave independently, the structured rate relative to μ₁ is
     R₂₊₂(κ, p) = N_inv(κ)²·κ⁴/p².
   - κ = 6: R₂₊₂ = 2.62·10⁶/p². That is 1.03 at 1597, 1.00 at 1621, 0.96 at 1657, 0.82 at 1789, 0.70 at 1933, 0.48 at
     2347 and 0.17 at 3877.
   - κ = 7: R₂₊₂ = 2.65·10⁷/p², 0.020–0.023 at the six κ = 7 primes at λ ≈ 0.3.
   - At fixed λ = 0.2 it is 1.1, 0.048 and 0.0010 at κ = 6, 7, 8.
3. **The arithmetic factor F.**
   - Definition: F(p) is the measured 2+2 rate (2+2 share × N₁/μ₁) divided by R₂₊₂(κ, p). So w := F·R₂₊₂ is the
     measured weight, by definition. The heuristic of item 2 predicts F ≈ 1.
   - At κ = 6:

     | p | kind | F |
     |---|---|---|
     | 1597 | sD | 3.4–3.7 |
     | 1627 | sN | 1.6–2.1 |
     | 1657 | sD | 3.2–3.9 |
     | 1789 | sD | 2.3–4.4 |
     | 1933 | sD | 2.5–3.3 |
     | 1621 | typical | 0.30–0.31 |
     | 2347 | typical | 0.7 |
     | 3877 | typical | 0.8 |

     - Each range takes the share and N₁/μ₁ from the pairsym sample, or from the survey, split or largest runs.
     - The largest value, 4.4, is the 1789 split: share 0.804 × N₁/μ₁ 4.50, over R₂₊₂ = 0.82.
     - Between runs F differs by up to 1.9×, in no consistent direction (heavy tails, §12.2).
   - At κ = 7:
     - F is 1.8 at 35281, 0.5 at 35099, 2.3 at 36037 and 0.9 at 34693, from 19, 5, 28 and 9 structured
       configurations.
     - These counts are clustered: a b = 8 bucket gives up to 8 configurations, and 12 of the 19 at 35281 come from
       b = 8 buckets. So the relative errors exceed the 23–45% of 1/√n.
     - At λ = 0.2, F is 1.16 at 23549 (exact Poisson 95% range 0.4–2.7), from 5 unclustered configurations (§12.6).
   - Across κ = 6 and 7 at λ ≈ 0.3:
     - The 2+2 rate falls from 0.34–0.36 (2347) to 0.010–0.048 (κ = 7), a drop of 7–35×.
     - R₂₊₂ predicts 22–23×, and a λ-law predicts none.
     - So the 2+2 baseline weight is not a function of λ alone, and it falls as R₂₊₂ does.
   - At fixed κ the p⁻² fall-off is not visible.
     - At the typical κ = 6 primes 1621, 2347 and 3877, the structured rate is 0.30, 0.34 and 0.14, about p^{−0.9}.
     - Over the same primes R₂₊₂ falls 6×, and F rises from 0.3 to 0.8.
   - F is not predicted by the heuristic, and its maximum over primes is unknown.
4. **General families.**
   - Take g ∈ PGL₂ of order m, with a g-orbits in S and b in T, and set x = am/κ and y = bm/κ.
   - The codimension in (S, T) is c = (a+b)(m−1) − 2. The rank-1 deficit is E = (m−1)(abm − a − b): E = 4 for the 2+2
     block, and κ²/2 − κ for full involution symmetry.
   - With κ^{O(κ)} placements and an O(1) solvability factor, at p = κ^{γκ}:
     log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ).
   - Since xy ≤ (x + y)/2, every family with x + y bounded below is negligible once γ > 1/2 + O(1/κ). Families with
     x + y = O(1/κ) satisfy E/c ≤ κ/2 + O(1), which gives the same conclusion.
   - This assumes that each family's analogue of F is O(1), with no arithmetic enhancement. That is unmeasured.
   - Full involution symmetry (even κ, averaged over the two kinds) has R_full = ((κ−1)!!)²κ^{κ²/2−κ}p^{2−κ}
     (κ = 6: 4.9·10¹¹/p⁴). This is < 1 once p > κ^{κ/2+1−1/ln κ+o(1)}.
5. **Along the threshold path.**
   - The exponent needs OSC′ at T(κ) = κ^{κ/2+κ/(2 ln κ)+O(1)} (§11.8).
     - λ_T is 0.433, 0.182, 0.0685 and 0.0229 for κ = 7–10, from §11.8's log_κ T = 5.57, 6.18, 6.78 and 7.36.
   - There R₂₊₂ = κ^{12−κ−κ/ln κ+O(1)} and R_full = κ^{−κ²/(2 ln κ)+O(κ)}.
   - At the typical-constant thresholds of §11.8, R₂₊₂ is:
     - 0.026 at κ = 6 (p ≈ 10⁴);
     - 0.010 at κ = 7 and 0.0012 at κ = 8;
     - 1.1·10⁻⁴ at κ = 9 and 7.6·10⁻⁶ at κ = 10.
   - With the largest measured F (4.4), the weight w = F·R₂₊₂ is up to 4.5% at κ = 7 and 0.55% at κ = 8.
6. **The family's effect on the constants** [elementary, given the definitions].
   - Let the family have share s of the (C1) measure and noise-subtracted absolute D-group rms v.
     - V is linear in the measure, and the weighted rms is a norm. So ρ_D ≤ (1 − s)ρ_rest + s·v.
     - The share is s = w/(N₁/μ₁) = F·R₂₊₂/(N₁/μ₁). Under (N) the factor 1/(N₁/μ₁) is at most B. At the κ = 7 primes,
       where N₁/μ₁ = 0.89–1.11, it is about 1. Below, take N₁/μ₁ = 1.
   - So the family adds at most F·v·N_inv²κ²/p to B_D (units κ²/p).
     - At T(κ), N_inv²κ²/p is 10.6, 7.4, 3.9 and 1.7 for κ = 7–10.
     - It tends to 0 like κ^{10−κ/2−κ/(2 ln κ)+O(1)}.
   - F·v at the five split primes, with F and v (from the 2+2 part's B_D) taken from the same run:
     - 0.003 at 1621 and 0.27 at 1933;
     - 0.35 at 1597 and 0.98 at 1657;
     - 1.53 at 1789.

     That is a 500× spread.
   - What the family would add at T(κ) depends on how v scales from p ≈ 1800 to T(κ):
     - If its absolute D-rms v keeps 1789's value, it would add about 16, 11, 6 and 3 at κ = 7–10. Its B_D in κ²/p
       units then grows about 21× by T(7).
     - If its B_D keeps 1789's 17.3 (in κ²/p units, as a constant-B law would have it), it would add w·17.3: 0.78 at
       κ = 7 and 0.09 at κ = 8.
     - With 1621's values (2σ, absolute v fixed), it adds at most 0.05, 0.03, 0.02 and 0.01.
     - OSC′ is stated for every p ≥ p₀, so what matters is the largest F·v over primes near T(κ). That is not measured
       at any κ ≥ 7.
   - **Without v.**
     - |Q| ≤ n, because each symmetrised character has modulus ≤ 1. So v ≤ n.
     - The family then adds at most F·B·N_inv²κ²·(n/p) to B_D and F·B·N_inv²κ⁴·n/p² to B_L. Both are F·B·κ^{O(1)}.
     - Tolerances (§11.8): an exponent below κ survives while log_κ B_D < (1 − 1/ln κ)κ − O(1) and
       log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1). The exponent (1/2+o(1))κ needs both to be o(κ). The family adds to both.
     - So the 2+2 family can spoil the (1/2+o(1))κ exponent only if F·B = κ^{Ω(κ)} at some p ≥ p₀ near the threshold
       path. If (N) holds with B = κ^{o(κ)}, that means F(p) = κ^{Ω(κ)}. §11.8's (N) fixes no size for B, and §9
       measures B up to 9.9.
     - This needs no independence assumption, since F is defined from the measured rate.
   - The L group gains at most w·v_L ≈ 0.045·1.97 = 0.09 at κ = 7 with the 1789 values.
7. **What this does not say.**
   - Items 2, 4 and 5 are first-moment counts with an independence assumption. Item 6 does not need it, but it bounds
     the family's effect only in terms of F, which is unbounded.
   - It concerns projective families of bounded orbit type.
   - It says nothing about the not-2+2 part at spike primes, or about structure that is not projective.

### 12.6 κ = 7 [computed]

- **Runs.** `bucket_stats.py 7 p 2·10⁵ --seed 21` gives configurations per S against Poisson, the occupancy law and
  its tail, from uniform S. `pairsym.py 7 p 10⁵` gives the 2+2 share.

  | p | λ | symR | N₁/μ₁ | var/mean | b = 7, 8 vs Poisson | 2+2 share |
  |---|---|---|---|---|---|---|
  | 35281 | 0.300 | 15.8 | 0.90 ± 0.05 | 0.999 | 0.95, 0.92 | 0.043 |
  | 34469 | 0.293 | 16.7 | 0.91 | 0.999 | 0.88, 1.15 | |
  | 35099 | 0.298 | 21.3 | 0.96 | 0.999 | 0.93, 1.07 | 0.011 |
  | 34259 | 0.291 | 22.1 | 1.11 ± 0.08 | 0.999 | 1.06, 1.07 | |
  | 36037 | 0.306 | 44.2 | 1.09 ± 0.06 | 0.999 | 1.01, 1.42 | 0.045 |
  | 34693 | 0.295 | 44.2 | 0.89 ± 0.05 | 0.999 | 0.91, 0.97 | 0.021 |
  | 23549 | 0.200 | 67.4 | 0.84 ± 0.09 | 0.999 | 0.91, 0.54 (2 buckets) | 0.063 |

  The se include the bucket clustering. 23549 used 6·10⁵ S.
- **Carry-over test at λ ≈ 0.3.**
  - The two primes with the largest symR (44, against 9.4–22 at eleven others at λ ≈ 0.3) have N₁/μ₁ 1.09 and 0.89.
  - Over the six primes N₁/μ₁ = 0.89–1.11. There is no detectable rank relation to symR: n = 6, and Spearman is 0.09,
    or 0.31 if the two near-equal symR values are swapped.
  - The κ = 6 proportionality would give about 2.5 at symR 44. At κ = 7 symR no longer predicts the measure, as
    expected when the 2+2 weight is 2%.
  - This tests carry-over of the κ = 6 behaviour, not §12.5. The 2+2 weight F·R₂₊₂ ≈ 0.02·F (measured 0.010–0.048)
    moves N₁/μ₁ by that much, below these se. The informative κ = 7 number is F (§12.5 item 3).
- **λ = 0.2.**
  - 23549 has the highest symR of the κ = 7 primes sampled (67), and R₂₊₂ = 0.048 there.
  - Measured N₁/μ₁: 0.84 ± 0.09 (0.12 with Poisson bucket sizes), from 151 configurations in 6·10⁵ S (135 from b = 7
    buckets, 16 from two b = 8 buckets; `buckets/bucket_k7_p23549.out`). The pairsym sample gives 0.88; together,
    0.85 ± 0.08.
    - So the κ = 6 proportionality (about 2.5 at symR 67) fails at λ = 0.2 as well.
    - N₁/μ₁ alone is consistent with the R₂₊₂ reading but does not discriminate. The 2+2 count does.
  - Measured 2+2 share: 0.063 (`pairsym/pairsym_k7_p23549.out`, `pairsym.py 7 23549 300000`: 5 of 79 configurations,
    all from b = 7 buckets, so unclustered).
    - The R₂₊₂ law at F = 1 gives 5.4–5.7%.
    - F(23549) = 1.16 (1.1–1.2 with either N₁/μ₁). The exact Poisson 95% range is 0.4–2.7.
  - **The test is the weight, not the share.**
    - The share also depends on the not-2+2 rate. That is (1 − 0.063)·(0.84–0.88) = 0.79–0.82 μ₁ here, against 0.12
      at 1621. A λ-only weight on top of 23549's not-2+2 rate would give a share of 0.28, not 0.7–0.9.
    - The 2+2 weight here is w = 0.055 μ₁. At κ = 6, λ ≈ 0.21 it is 0.31 at 1621 (the smallest measured) and 1.6–3.5
      at the spikes 1627, 1657 and 1597.
    - With a weight depending on λ alone, this run would have about 28 (1621's weight) to 314 2+2 configurations. It
      has 5. The Poisson probability is about 10⁻⁷ even at 28, and buckets with b ≥ 8 are too rare to hide the
      difference in clusters.
  - So at λ = 0.2 the 2+2 weight drops from κ = 6 to κ = 7 by 5.6× against 1621 and 29–63× against the spikes. R₂₊₂
    predicts 20–22×. That is "as R₂₊₂ predicts, up to F": F(23549) lies inside κ = 6's 0.3–4.4 and κ = 7's 0.5–2.3.
  - The run rejects a λ-only weight. It does not distinguish R₂₊₂ from other κ-scalings within about 10×. It is one
    prime and 5 events.
- **Class values at 36037** [computed]. The run is `mc_classes.py 7 36037 10⁴ --seed 13`, 1.57·10⁶ S.
  - The analysis is in `review-2026-11-10/scratch/k7_class_values.out` and `pw_bin_cs_k7.out`, and the referee's check
    in `r3c_checks.out` (round 3c of `ROUND3.md`).
  - 36037 was picked on symR (the highest at λ ≈ 0.3, with 34693) before its F or class values were known. Its F, 2.3,
    is the highest at κ = 7.
  - N₁/μ₁ is 1.08, so it is not a count spike.
  - **B_L.**
    - It is 0.635 (z 6.9, 2σ 0.54–0.72). At 47041 and 58787 (λ 0.40, 0.50) the same estimators give 0.22 and 0.27.
    - Every resolved L bin is lifted against 47041: (0,3) 3.70 against 0.44, (2,2) 3.78 against 1.65, (2,3) 0.53
      against 0.03, (3,3) 0.25 against 0.02. (2,2) and (0,3) carry 63% and 19% of B_L².
    - The lift is not a heavy-tail or cluster effect. All 16 S-batches contribute positively to B_L, and leaving out
      any two keeps it ≥ 0.58 (checked). The referee also finds every half-sample of 8 batches ≥ 0.51, and z 4.8–9.8 on
      8 super-batches.
  - **B_D.**
    - It is 9.4 (z 1.6), < 14.1 at 2σ, so its size is not resolved.
    - Its sign is consistent (checked). It is positive in every batch, the exact sign-flip test gives p ≈ 3·10⁻⁵, and
      it stays ≥ 5.6 leaving out any one or two batches.
    - But two batches carry 45% of it. All 17 m ≥ 7 bins have positive z (0.6–2.2), yet their batch profiles correlate
      at 0.97 (referee), so this is one effect.
    - At 47041 and 58787, B_D is < 2.6 and < 2.1 at 2σ.
  - L and D share these batches (profile correlation 0.94, referee), so they are not independent evidence.
  - PW_pair is 2.71 (null floor 1.00, CS upper 3.08). 92% of it is D-group weight, so it repeats the B_D excess. At
    47041 and 58787 PW_pair sits at its null floor.
  - **Comparison.**
    - From λ 0.4–0.5 to 0.31, B_L rises 2.4–2.9×. At κ = 6 it rises 1.1–1.5× from λ ≈ 0.5 to 0.30 (2347, B_L 0.41,
      against 0.27–0.37).
    - In the complete κ = 6 survey the median B_L is 0.45 in (0.25, 0.31] and 0.33 at λ ≈ 0.5, a rise of 1.4×. The
      band maximum is 1.16, at the spike 2113 (§12.10).
  - **The equal-λ comparison 35099** (λ 0.298; `mc_classes.py 7 35099 6000 --seed 13`, 1.29·10⁶ S; the 17 MB npz is
    kept outside the repo). The checks are in `review-2026-11-10/scratch/r4b_checks.out` (referee rounds 4b and 4c).
    - It was picked as the middle symR of the table above: 21.3, 10th of the 13 λ ≈ 0.3 primes in
      `sym/sym_rate_k7_lam03.out`, whose median is 16.3.
    - Its F, 0.5, the lowest at κ = 7, was known when it was picked. F rests on 5 configurations, so its Poisson 95%
      range is about 0.16–1.2. At κ = 6 rates the above-median symR would raise its B_L, and the low F might lower it.
    - B_L is 0.237 (z 8.2, 2σ 0.21–0.26). It is stable: all 16 batches contribute positively, leaving out any two
      keeps it ≥ 0.225, and half-samples range over 0.18–0.30.
    - B_D is 1.76 (z 0.7, < 3.4), with no consistent sign (sign-flip p 0.12). N₁/μ₁ is 0.95 ± 0.02. PW_pair sits at
      its null floor (0.93 against 0.90; CS upper 0.53).
    - Its L bins match 47041's: (2,2) 1.67 against 1.65, and (0,3) 0.65 against 0.44.
  - **So 36037 is a spike in B_L by the test set in §12.9**, against the three typical κ = 7 primes measured.
    - Its B_L is 2.7× 35099's at nearly equal λ (0.306 against 0.298). 35099's 2σ upper end, 0.264, is less than
      half of 36037's 2σ lower end, 0.535. 36037's smallest half-sample value, 0.51, is 1.7× 35099's largest, 0.30.
    - Every resolved L bin is lifted. The central ratios are given first, then 36037's 2σ lower end over 35099's 2σ
      upper end:
      - (2,2) 2.3× (≥ 1.9×);
      - (0,3) 5.7× (≥ 3.4×);
      - (2,3) 13× (≥ 6.0×);
      - (3,3) 12× (≥ 5.6×).
    - (0,4) and (2,4) are resolved at 36037 (z 3.8 and 2.6) and are noise at 35099 (≥ 2.9× and ≥ 4.2×).
    - (2,2) and (0,3) carry 81% of the rise in B_L².
    - At κ = 7 the typical B_L does not rise from λ 0.5 to 0.3: it is 0.27, 0.22 and 0.24 at λ 0.5, 0.4 and 0.3, one
      prime per λ. At κ = 6 the band medians rise 1.4× (0.33 to 0.45).
    - 36037's D excess has a consistent sign, which 35099's does not, but its size is unresolved.
    - F 2.3 against 0.5 (0.16–1.2) fits the κ = 6 pattern that spikes carry a large F. That is two primes, with the
      selection caveat above.
    - 36037 is neither sD nor sN, and B_L is not one of the κ = 6 flags.
  - **The calibration is the weak point** (referee round 4c).
    - At κ = 6, two unflagged primes at equal λ differ by as much: 2281 (λ 0.293, B_L 0.663) and 2293 (λ 0.295, B_L
      0.248), 2.67×. So a ratio to one comparison prime cannot separate a spike from the two ends of a wide typical
      spread.
    - The better reference is the band median. Unflagged κ = 6 primes reach at most 1.08, 1.22, 1.46 and 1.54× their
      band median, from λ ≈ 0.21 to λ ≈ 0.5. Spikes reach 3.74, 3.25, 2.56 and 1.94×.
    - 36037 is 2.6× the mean of the three typical κ = 7 primes. That makes it a spike if they sit near the κ = 7
      median at λ ≈ 0.3.
    - If 35099 sat at the bottom of a κ = 6-like spread (0.55× the median), the median would be about 0.43. 36037 would
      then be 1.47× it, at the top of the unflagged range.
    - That worst case is extreme. It needs 35099 below 0.58× the κ = 7 median, and at κ = 6 only 2 of the 68
      unflagged primes are (1741 and 2293). If 35099 sat at the 5%, 10% or 25% point of the unflagged ratios, 36037
      would be 1.74×, 1.83× or 2.27× the median.
    - A second equal-λ prime decides this. 34847 is running: it has the median symR of the 13 (16.3), and its F is
      unknown. Its rule was written before the run (`predictions_k7_p34847.txt`, 05:48):
      - a spike if B_L(34847) ≤ 0.41 and its 2σ upper end is below 0.535;
      - not shown to be a spike if B_L(34847) ≥ 0.43;
      - otherwise inconclusive.
    - An addendum (05:52, result unknown) asks for both 2σ ranges to be reported. The call is marked "close" if the 2σ
      range of B_L(34847) crosses 0.41 or 0.43.
- **Generic rate.**
  - The not-2+2 rate is 0.86–1.04 μ₁ at κ = 7, λ ≈ 0.3 (bucket_stats rates at the four primes with a share), and
    0.79–0.82 μ₁ at 23549 (λ = 0.2).
  - At κ = 6 it is 0.44 at λ ≈ 0.3 (2347), and 0.12 and 0.70 at λ = 0.21 and 0.50 (1621 and 3877). That is one
    prime each, and 1621 is in the bottom third of its band.
  - So the κ = 6 shortfall of generic configurations is not a function of λ alone: at λ ≈ 0.3, and at λ = 0.2 on one
    κ = 7 prime.

### 12.7 Arithmetic of spike primes [computed; post hoc]

- **B_D > 2 occurs only at p ≡ 1 (mod 12)** (h = ind(−1) ≡ 0 mod 6).
  - At λ ≤ 0.25 (complete) that is 6 of the 15 primes ≡ 1 (mod 12): 1597, 1657, 1669, 1693, 1789 and 1933. It is 0 of
    the 14 primes ≡ 7 (mod 12), where the largest B_D is 1.00 (1627).
  - Over all 89 primes it is 8 of 43 against 0 of 46 (post hoc; §12.10).
  - The post hoc evidence at λ ≤ 0.25 is weak:
    - H was formed on 17 survey primes, plus earlier S-batched runs (1933 at seed 11 among them).
    - With the cut at 2, the one-sided probability at λ ≤ 0.25 is 0.011 (C(15,6)/C(29,6)). With the residue
      partitions looked at and the cut chosen, it was 0.14–0.25 at n = 25 (referee, round 2).
    - An exact rank test of B_D by class gives one-sided 0.018 at λ ≤ 0.25 (n = 29).
    - At the 35-prime snapshot (the final scoring is in §12.10): H was pre-registered for the primes that finish after
      02:16, less 1933's rerun (known), which were 16 primes at the snapshot. 1759 (file written at 02:14–02:16, not looked at) is in neither the formation set nor the test set.
      On the 16 the same test gives 0.010. But h = 3 primes are 4 of the 6 above λ = 0.25 there. Restricted to the 10
      at λ ≤ 0.25 it gives 0.057.
  - Class medians (λ ≤ 0.25): B_D 0.93 against 0.56; N₁/μ₁ 1.16 against 0.67.
  - Pre-registered predictions (`survey/predictions_hclass.txt`), scored in §12.10: (H1) is refuted by 2143 (≡ 7 mod
    12, sD). (H2) held as pre-registered, and (H3) holds. So the data support a shift of B_D towards p ≡ 1 (mod 12),
    not value spikes only there.
  - The count spikes without value spikes (1531, 1627 and 1759) are all ≡ 7 (mod 12).
- **No mechanism is known.**
  - For a configuration fully symmetric under x ↦ −x, z and −z contribute equally whatever h is. This is because the
    class modes are sum-zero and taken up to cyclic shifts of the values.
  - For 2+2 configurations only the paired coordinates are shifted copies.
  - So this excludes h acting through the z ↔ −z pairing, not h acting at all. The order-6 cyclotomic numbers remain a
    route.
  - At odd κ, h = 0 for every p.
- **What ranks symR.**
  - Write p = a² + 3b², with a ≡ 1 mod 3. Log symR, detrended by a log–log fit in p on all 89 primes, rises with
    |a|/√p.
    - Spearman is 0.53 at h = 0 and 0.47 at h = 3 (30 primes each, λ ≤ 0.31), and 0.50 over all 60.
    - At h = 0 this holds whether or not 2 is a cubic residue (0.64 and 0.62). At h = 3 it sits in the cube subclass:
      0.79 (n = 13), against 0.19 (n = 17).
  - |a|/√p is |cos| of the argument of the associate a + b√−3 of the cubic Jacobi sum.
    - It equals §11.6's |L|/(2√p) (4p = L² + 27M²) only when 2 is a cubic residue, which holds at 25 of the 60 primes.
      Otherwise |L| = |a ± 3b|.
    - |L|/(2√p) itself has Spearman 0.09 with the residual, consistent with its failure as a predictor in §11.6.
  - At h = 0 the residual is also higher when 2 is a cubic residue: median +0.57 against −0.05. At h = 3 there is no
    such effect (−0.30 against −0.38).
  - The fixed cyclotomic cell combines both effects at h = 0.
    - When 2 is a cube, 36A(0,0) = p − 17 − 20a exactly (a ≡ 1 mod 3, checked at 17 primes). So
      |A(0,0) − mean|/√p = |20a + 15|/(36√p) ≈ (5/9)|a|/√p.
    - Otherwise it is ≤ 0.25.
    - Hence its Spearman of 0.81, against 0.27 for A(0,3).
  - All of this is post hoc.
- **Other statistics** (λ ≤ 0.25, n = 29): K has Spearman 0.78 with N₁/μ₁ and 0.56 with B_D; max|D|/√p has 0.46 with
  B_D.
- **Prospective tests.** `survey/predictions_hclass.txt` (02:16; mechanism retracted at 02:24) and
  `survey/predictions_N1mu1.txt` (01:20) are scored in §12.10.

### 12.8 Answer, and what it changes

- **Answer [computed at κ = 6, 7; heuristic beyond].**
  - At κ = 6, λ ≤ 0.25 (29 primes, complete), the constants are finite at every prime, as any finite sample must be at
    fixed κ. Their size is the information.
  - Spike primes reach B_L 1.88 (1657) and B_D 14.8 (1789). These are 4× and 18–25× the band medians.
  - 9 of the 29 primes are spikes by some flag, 6 of them by sD.
  - Over all 89 primes (§12.10), 21 are spikes. Spike amplitude falls as λ rises: the largest B_D is 14.8, 6.6 and
    1.4, and the largest PW_pair 32, 11 and 0.89, at λ ≤ 0.25, in (0.25, 0.31] and at λ ≈ 0.5. At λ ≈ 0.5 the
    debiased PW_pair is below 1 at every prime (28 of 29 by the CS upper estimate).
- **What spikes are.**
  - At λ ≈ 0.21, 71–88% of (C1) configurations are 2+2 involution-structured. This holds at the spike primes and at
    the one typical prime measured there (1621).
  - At the four split spike primes, this family's weight factor F and its class values are both large: F 2.3–4.4
    against 0.3 at 1621, and B_D 4.3–17.3 against 0.44. The not-2+2 part is lifted too.
  - The sN spike 1627 has F 1.6–2.1 without a value spike.
  - Why some primes are like this is not explained. |a|/√p and the cubic character of 2 rank it in part (§12.7).
- **p against λ.**
  - Across κ = 6 and 7, at λ ≈ 0.3 and at λ = 0.2, the 2+2 baseline weight falls as R₂₊₂ = N_inv²κ⁴/p² does (up to
    F), not as a function of λ.
  - The spike excess is F, which the heuristic does not model.
  - At fixed κ the two cannot be separated.
  - At κ = 7, λ = 0.2 there is one prime, 23549, the highest symR sampled.
    - Its 2+2 weight is 0.055 μ₁ (5 of 79 configurations), against 0.31–3.5 at κ = 6, λ ≈ 0.21. A weight depending on
      λ alone would give at least 28 such configurations (P ≈ 10⁻⁷).
    - Its share is 6.3%, against 5.4–5.7% from R₂₊₂ at F = 1 (F 1.16, 95% range 0.4–2.7).
    - Its N₁/μ₁ is 0.84 ± 0.09, against about 2.5 for the κ = 6 proportionality.
  - This rejects a weight depending on λ alone. It does not distinguish R₂₊₂ from other κ-scalings within about 10×.
- **κ = 7.**
  - At λ ≈ 0.3 the 2+2 share is 1.1–4.5% at four primes, against an expected 1.9–2.4%. At 23549 (λ 0.2) it is 6.3%,
    against an expected 5.4–5.7%.
  - N₁/μ₁ is 0.84–1.11 at seven primes (six at λ ≈ 0.3, and 23549), with symR 16–67.
  - Class values at λ ≈ 0.3: at 36037, picked on symR, B_L is 0.635. That is 2.4–2.9× the λ = 0.4–0.5 values, against
    1.1–1.5× for the same step at κ = 6. N₁/μ₁ there is 1.08, and the D excess has a consistent sign but an unresolved
    size.
  - Against the equal-λ typical prime 35099 (B_L 0.237) it is a spike in B_L by §12.9's test (2.7×; §12.6). At κ = 6,
    two unflagged equal-λ primes differ by 2.67×, so the call rests on 35099 sitting near the κ = 7 median. At κ = 6,
    only 2 of 68 unflagged primes sit as low as that would need. A second equal-λ prime (34847) decides it under a
    pre-registered rule.
- **What changes.** Obstruction (c) of §11.8 narrows to three questions:
  1. Is F(p) = κ^{o(κ)} uniformly over p ≥ p₀ near the threshold path?
     - If (N) holds with B = κ^{o(κ)}, this is the only way the 2+2 family can spoil the (1/2+o(1))κ exponent (§12.5
       item 6). Otherwise the condition is on F·B.
     - It needs no independence assumption, since F is defined from the measured rate.
  2. The same question for the arithmetic factors of the other bounded-orbit families of §12.5 item 4.
  3. What are the not-2+2 part at spike primes, and any non-projective structure at κ ≥ 7?

  With the largest measured F·v (1789), the family would add B_D ≈ 16 at κ = 7 if its absolute D-rms did not fall
  with p. It would add 0.8 if its B_D in κ²/p units stayed constant, and at most 0.05 with typical values. Either way
  it is bounded and falls to 0 as κ grows, so it is harmless for the exponent if F and B stay bounded.
- **Claim gates that stay false.**
  - OSC′ in either form at any κ.
  - Any rigorous bound on spike constants.
  - R₂₊₂ or the family estimate as a theorem. Item 6's bound is elementary, but it bounds the family's effect only in
    terms of F.
  - Threshold certificates at κ ≥ 6.
  - An unconditional exponent statement.
  - F(p) bounded, or κ^{o(κ)}, over p ≥ p₀.
  - Obstruction (c) resolved.
  - Hypothesis H (refuted in its strict form; the class shift of B_D held prospectively (H2) but has no mechanism),
    or the |a|/√p and cubic-character correlations, as claims.
  - "κ = 7 has no spike primes". 36037 is a counterexample in B_L, against one equal-λ prime.
  - 36037 a spike against the spread of κ = 7 class values at λ ≈ 0.3, until 34847 is scored; 36037's B_D size; the
    lift as a 2+2 effect, until the 2+2 split of the 36037 run is done.
  - The 2+2 family's class values at κ ≥ 7, or v falling with p.
  - The not-2+2 part at spike primes under control.

### 12.9 Next

- **Finish the survey.** Done (§12.10).
  - Done: 2143 at seed 14 replicates its D excess and all three flags (§12.10).
- **F over the survey.**
  - Run `pairsym.py 6 p 300000` at every survey prime with λ ≤ 0.25 (5–20 min each), and compute F with the survey's
    N₁/μ₁.
  - Acceptance: the distribution of F and its maximum, and Spearman with |a|/√p and with the cubic class of 2.
  - A model for F in terms of the cubic Jacobi sum is the first step towards bounding its maximum, which is question 1
    of §12.8.
- **κ = 7 at typical λ ≈ 0.3 primes.** 35099 is done (§12.6): by this test 36037 is a spike in B_L, with the
  calibration caveat.
  - Running: `mc_classes.py 7 34847 6000 --seed 13` (`mc_k7_p34847.log`, npz outside the repo). Score it with the
    rule in `predictions_k7_p34847.txt` (05:48, addendum 05:52), via `review-2026-11-10/scratch/k7_class_values.py`.
  - Then a 2+2 / not-2+2 split of the 36037 run, as at κ = 6, to see whether its 4.5% 2+2 share carries the (2,2) and
    (0,3) lift.
- **The direct test of (c)** still needs κ = 8 at λ ≈ 0.18 (p ≈ 3.8·10⁵), with a sampler that builds (C1)
  configurations directly (§11.9). That sampler is the main gap.
- **Bounding F.**
  - By §12.5 item 6, the 2+2 family's effect on the exponent is controlled by F. So the proof target is an upper bound
    O(κ^{o(κ)}·N_inv²κ⁴p⁻²μ₁) for the 2+2 count.
  - The block conditions are explicit. The rest is an upper bound for a (C1) count on a codimension-2 family, which
    §9's existence proof does not give.
  - Weil's error terms are κ^{O(κ²)}√p, useless at p = κ^{O(κ)}. So no method is in hand.

### 12.10 Final survey and the scored predictions (10 Nov, 04:49) [computed; the scoring is pre-registered]

- **Reviewed** by an independent AI referee: round 4 of `review-2026-11-10/ROUND3.md`, with the author's disposition.
  Its checks are `review-2026-11-10/scratch/r4_checks.py` and `.out`.
- **Run.** All 89 primes had finished by 04:49 (`k6_spike_survey.out`). The scoring script is
  `survey/score_predictions.py`, with output in `survey/score_predictions.out`. It uses the flags and bands of
  `k6_spike_survey.py`. Nothing changes at λ ≤ 0.25. The completed bands are in §12.2's table.
- **Spikes.** 21 of the 89 primes are flagged.
  - Amplitude falls as λ rises. The largest B_D is 14.8, 6.6 and 1.4 at λ ≤ 0.25, in (0.25, 0.31] and at λ ≈ 0.5.
    The largest PW_pair is 32, 11 and 0.89.
  - In (0.25, 0.31] the largest spikes are 2113 (B_D 6.6, z 3.7; PW_pair 11.1; N₁/μ₁ 2.06) and 2269 (B_D 5.4, z 3.3;
    PW_pair 8.0; N₁/μ₁ 0.87).
  - The debiased PW_pair is below 1 at none of the 29 primes with λ ≤ 0.25, at 13 of the 31 in (0.25, 0.31] and at
    all 29 at λ ≈ 0.5. By the CS upper estimate the counts are 0, 7 and 28. The exception at λ ≈ 0.5 is 3889
    (debiased 0.89, CS 1.01). These are Monte Carlo estimates, not certificates.
  - The smallest N₁/μ₁ in the survey is 0.37 (1741), so B ≈ 2.7 in (N) covers all 89 primes.
- **Replication.** The four primes run at two seeds (1933, 2347, 3877 and 4219) agree on B_D within 0.8 combined
  jackknife se, and on B_L within 2.0. At 1933, N₁/μ₁ is 2.66 against 2.63. This is the only between-seed check of
  the B_D se.
- **N₁/μ₁ predictions** (`survey/predictions_N1mu1.txt`, 01:20; §12.3).
  - Log errors at the 74 later primes:

    | primes | n | rms | mean | largest |
    |---|---|---|---|---|
    | later primes, λ ≤ 0.25 | 15 | 0.24 | +0.04 | +0.37 (1879) |
    | (0.25, 0.31] | 31 | 0.19 | +0.04 | +0.44 (1951) |
    | λ ≈ 0.5 | 28 | 0.13 | +0.05 | −0.26 (3889) |

  - Over all 74 the rms is 0.18 (mean +0.04 ± 0.02), and 8 of the 74 are off by more than 0.3. The in-sample residual
    sd was 0.20 with n in the denominator, or 0.22 with n − 3.
  - 2347 and 4219 had been seen at seed 11. Without them nothing changes (rms 0.19 and 0.13 in their bands).
  - At λ ≤ 0.31 this is real prediction: the spreads of log N₁/μ₁ among the predicted primes in the first two rows
    are 0.65 and 0.40.
  - At λ ≈ 0.5 the errors confirm the level that 3877 alone had set (mean +0.05 ± 0.02). Without 3877 the fit misses
    by 3.8× in (0.25, 0.31] and by 52× at λ ≈ 0.5.
  - But they reject the symR slope there. Within the band it is 0.40 ± 0.07, against 0.98, and a constant does as
    well (rms 0.12–0.13). So within the λ ≈ 0.5 band the law has no predictive power.
  - Post hoc:
    - The within-band slope falls with λ: 1.00 ± 0.06, 0.86 ± 0.09, 0.73 ± 0.07 and 0.40 ± 0.07. symR's own sampling
      error does not explain this, since its sample is larger at λ ≈ 0.5.
    - Given symR, N₁/μ₁ is about 15% higher at p ≡ 7 (mod 12), in every band (Mann–Whitney 0.0002).
- **Hypothesis H** (`survey/predictions_hclass.txt`, 02:16; §12.7).
  - The sets:
    - test set: the 70 primes whose npz was written after 02:16, less 1933, whose value was known from seed 11;
    - formation set: the 17 primes written by 02:16 (1531–1753, less 1741);
    - 1759 is in neither (§12.7);
    - the file's own wording gives 71, with 1933;
    - a strict set of 66 also drops 2347 and 4219 (seen at seed 11), 3877 (seen in an earlier S-batched run) and
      3889 (named in the file).

    All three test sets give the same verdicts.
  - **(H1)**, that every new sD prime is ≡ 1 (mod 12), is **refuted by 2143** (≡ 7, λ 0.276, npz written at 03:56).
    - 2143 is sD as registered: B_D 1.28, z 6.4, 2σ lower end 1.07 (jackknife se) against the threshold 0.89, twice
      the band median.
    - The flag survives leaving out any one of the 16 batches with the jackknife redone (16 of 16). It would fall
      only if the jackknife se were understated by more than 1.68×.
    - 2179 (≡ 7) and 3823 (≡ 7, λ 0.49) are also flagged, but at the threshold: their se margins are 1.00 and 1.02,
      and they lose the flag with one batch left out in 12 and 10 of 16 cases. They are threshold cases, not
      refutations.
    - The B_D point values of all three stay above the threshold with any two batches left out, and every batch
      contributes positively (`review-2026-11-10/scratch/leaveout_BD.py`). That tests B_D, not the flag, which is
      defined by the lower end.
    - Heavy tails. §12.2's factor of about 2 was measured on N₁/μ₁. Inflating the B_D se after the fact cannot enter
      the scoring, which fixed the jackknife se. At 2× it would leave 4 class-1 flags and no class-7 flag, so it would
      rescue H. The seed pairs above give no basis for it.
    - The refuting excess is moderate. 2143's B_D is 2.9× its band median, like the weakest class-1 flags (2053 and
      2137).
    - It replicates (referee round 4b). A second-seed run (`mc_classes.py 6 2143 10000 --seed 14`,
      `survey/mc_k6_p2143_s14.npz`) gives B_D 1.29 (z 7.2, 2σ lower end 1.09), B_L 0.90 and N₁/μ₁ 1.99. At seed 13
      they were 1.28 (z 6.4, 1.07), 0.91 and 2.08. All three flags (sD, sPW, sN) recur against the seed-13 band
      medians.
    - The seeds differ by 0.03 combined se on B_D, 0.47 on B_L and 0.84 on N₁/μ₁. The se is that of the
      noise-subtracted X, the scale of the jackknife z. This matches the four seed pairs above, so the jackknife se is
      borne out at 2143 too.
    - So the refutation of H1 is not a seed artefact (one replication). This informs the reading, not the score.
  - **(H2) held as pre-registered** in both bands that qualify. The registered statistic is the class medians of B_D:
    - (0.25, 0.31]: 0.92 against 0.34 (15 and 16 primes);
    - λ ≈ 0.5: 0.36 against 0.12 (13 and 16 primes).

    Added summaries, one-sided Mann–Whitney: 0.006 and 0.012 (0.006 and 0.025 on the strict 66). Stratified by band
    it is 0.0001 on the 70 (0.0002 on the 66).
  - **(H3) holds.** The new sN spikes are 1789, 2113 and 2341 (≡ 1) and 2143 (≡ 7).
  - So H is refuted in its strict form, value spikes only at p ≡ 1 (mod 12). H2 held, so the data support a shift of
    B_D towards p ≡ 1 (mod 12). No mechanism is known.
  - Post hoc:
    - The shift does not come from the noise subtraction: unsubtracted values give 0.0001 on the 70.
    - It survives adjusting for N₁/μ₁ within bands (0.001). Given symR it weakens to 0.016; symR is itself shifted
      towards p ≡ 1 (mod 12) (stratified 0.005).
    - B_D > 2 still occurs only at p ≡ 1 (mod 12): 8 of 43 primes against 0 of 46 (P = 0.002). Three of the 8 are
      test primes (1789, 2113 and 2269); on their own P = 0.11. The largest B_D at p ≡ 7 (mod 12) is 1.28 (2143).
    - The count spikes without value spikes are still 1531, 1627 and 1759, all ≡ 7 (mod 12). 1951 is not flagged once
      its band is complete (N₁/μ₁ 1.42 against the threshold 1.62).
    - At λ ≤ 0.31 the class medians are N₁/μ₁ 1.04 against 0.67 and B_D 0.93 against 0.47 (30 primes each).
- **For the question asked.** The completed bands leave §12.8's answer and its three questions as they were. Spikes
  are frequent at κ = 6 (21 of 89), and their amplitude falls as λ rises.
