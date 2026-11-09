## 12. Spike primes at κ = 6: survey, partial involution symmetry, and the threshold path (follow-up, 10 Nov)

Question (mechanical plan item 1, §11.9): does OSC′ hold at λ ≤ 0.25 at spike primes, and what are spikes made of?
Everything here is Monte Carlo or heuristic; nothing is a certificate. Code and outputs are in `osc-mc/`.

An independent AI referee checked the section in two rounds (`osc-mc/review-2026-11-10/REPORT.md`, with the
author's disposition of each point). Its corrections are applied:
- a factor 2 in the heuristic at even κ;
- an undercount in the first `pairsym.py`;
- a misattributed cyclotomic correlation;
- overstated readings of the mechanism and of what it implies.

### 12.1 Survey design [computed]

- **Primes and runs.** Every p ≡ 1 (mod 6) in [1500, 2400] and [3800, 4300]: 89 primes, λ = 0.197–0.307 and
  0.49–0.55. Each runs `mc_classes.py 6 p N --seed 13`, S-batched, with N = 5000 configurations below 1700, 10⁴ up
  to 2400 and 2·10⁴ above. The prime list and driver are `survey/k6_survey_primes.txt` and `survey/run_k6_survey.sh`
  (nice 19, four at a time).
- **Analysis.** `k6_spike_survey.py` (→ `k6_spike_survey.out`) prints, per prime:
  - N₁/μ₁ with its S-batch se;
  - the debiased PW_pair with its null floor and the CS upper estimate;
  - B_L and B_D with jackknife z and 2σ upper end (the `equal_p_chain.py` estimators);
  - the noise law c, the cluster-corrected B^cl, K and max|D|/√p;
  - ind(−1), ind(2), ind(3), ind(−3) mod 6;
  - symR (§12.3).
- **Spike flags, per λ band.** sD: the 2σ lower end of B_D is above twice the band median. sPW and sN apply the
  same rule to PW_pair and N₁/μ₁.
- **Status: interim** (snapshot 03:20, 10 Nov). 28 of 89 primes are finished: every one with λ ≤ 0.25 except 1867
  and 1879, and the first one above, 1951. The rest are running, four at a time. `k6_spike_survey.py` rebuilds
  every table below (this snapshot: `review-2026-11-10/survey_n28.out`).

### 12.2 Results so far [computed; interim]

| λ band | primes | median B_L / B_D / PW_pair / N₁/μ₁ | max B_L, B_D (p) | spikes |
|---|---|---|---|---|
| 0.197–0.218 | 14 | 0.50 / 0.82 / 2.81 / 0.97 | 1.88, 10.5 (1657) | 6: 1531 sN; 1597 sD sPW sN; 1627 sN; 1657 sD sPW sN; 1669 sD; 1693 sD sPW |
| 0.222–0.249 | 13 | 0.56 / 0.60 / 1.82 / 1.08 | 1.77, 14.8 (1789) | 2: 1789 sD sPW sN; 1933 sD sPW sN |
| 0.251–0.31 (so far) | 1 (1951) | 0.49 / 0.34 / 1.03 / 1.42 | | none |
| earlier: 2347 (0.302) | 1 | 0.41 / 0.34 / 0.75 / 0.76 | | typical |

- **Largest spike: 1789.**
  - B_L 1.77, B_D 14.8 (z 9.2, 2σ upper 16.4), PW_pair 31.7, N₁/μ₁ 4.50, c 2.66.
  - This is the largest B_D measured at any κ: 25× its band median and 18× the λ < 0.22 median.
  - Next is 1657: B_L 1.88, B_D 10.5, PW_pair 30.1, N₁/μ₁ 4.47.
- **Typical primes.** At λ ≈ 0.21 they have B_L 0.32–0.54, B_D 0.38–0.93 and N₁/μ₁ 0.39–1.15. The noise level there
  is ν_D 0.69–1.18, so most of these B_D values are noise. (N) of OSC′ therefore needs B ≈ 2.6 at these primes; (N)
  enters only the noise term of §11.8, which never dominates.
- **Count spikes without value spikes.** 1531 and 1627 have N₁/μ₁ 4.11 and 2.64 but B_D only 0.63 and 1.00 (§12.7).
- **N₁/μ₁ is heavy-tailed at spike primes.**
  - Single S with buckets of 10–12 points carry much of the count.
  - Smaller samples of the same prime come out low: 2.53 against 4.50 at 1789, 3.71 against 4.47 at 1657, 2.05
    against 2.64 at 1627.
  - So the S-batch se understates the uncertainty there, by up to a factor 2.
- **What "holds" means here.** At fixed κ any finite set of primes satisfies OSC′ with some constants, so the survey
  measures their size. PW_pair is above 1.4 at every prime with λ ≤ 0.25. The κ = 6 threshold of §11.8 is
  λ_T = 1.3, so none of these primes is in the range a κ = 6 certificate would use.

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
  - Spearman 0.95 over the 27 survey primes with λ ≤ 0.25 (0.92 with 1951 included).
  - At λ ≈ 0.2, N₁/μ₁ ≈ 0.038·symR with log-sd 0.18 over 13 primes, about the size of the sampling errors.
  - symR also ranks B_L (0.93) and B_D (0.74).
- **Prospective test.**
  - The fit log N₁/μ₁ = −0.14 + 0.98 log symR + 1.93 log λ (14 primes) was used at 01:20 to predict every unfinished
    prime (`survey/predictions_N1mu1.txt`).
  - The 13 primes with λ ≤ 0.25 that finished since (1699–1873, λ 0.218–0.241) came in with rms log error 0.22
    (mean −0.01, largest 0.34). That is about the in-sample residual sd of 0.20.
  - They include the largest spike, 1789: 4.50 against a predicted 5.25.
  - The first prime above λ = 0.25, 1951, is off by +0.45 (1.42 against 0.91).
  - The λ-term is calibrated on the one λ = 0.5 prime 3877 (without it the coefficient is −2.06), and the primes at
    λ ≤ 0.25 do not test it.
- **symR is not the mechanism.** The fully symmetric S carry C_sym ≈ 1/8.5 of N₁/μ₁ (median ratio 8.51, quartiles
  7.8–12.2, λ ≤ 0.25). symR measures a property of the prime that also drives the rest of the measure (§12.4).

### 12.4 Mechanism: partial involution symmetry [computed]

- **Definitions.**
  - A Möbius involution ι is fixed by two of its 2-cycles. So a κ-set S has N_inv = C(κ,2)C(κ−2,2)/2 involutions
    swapping two disjoint pairs of S: 45 at κ = 6, 105 at κ = 7.
  - A configuration (S, T) is **2+2 structured** if one of these ι also has two ι-pairs {t, ι(t)} inside T.
  - Over F_p, involutions are split (conjugate to x ↦ −x, two fixed points in P¹(F_p)) or non-split (conjugate to
    x ↦ ε/x, ε a non-square), about half of each.
- **Exact count.** `pairsym.py k p nS` counts, for every full S-bucket, the k-subsets T that are 2+2 structured. It
  takes the union over ι; a first max-over-ι version undercounted by up to 16 points. `--null` replaces the bucket by
  a random b-set.

  | p | λ | kind | N₁/μ₁ (same sample) | 2+2 share | 2+2 counting ι-fixed points |
  |---|---|---|---|---|---|
  | 1597 | 0.205 | spike | 3.97 | 0.875 | 0.915 |
  | 1621 | 0.208 | typical | 0.42 | 0.741 | 0.786 |
  | 1627 | 0.209 | sN | 2.05 | 0.780 | 0.826 |
  | 1657 | 0.213 | spike | 3.71 | 0.830 | 0.886 |
  | 1789 | 0.230 | spike | 2.53 | 0.736 | 0.805 |
  | 1933 | 0.249 | spike | 2.72 | 0.700 | 0.774 |
  | 2347 | 0.302 | typical | 0.80 | 0.444 | 0.514 |
  | 3877 | 0.499 | typical | 0.84 | 0.167 | 0.192 |
  | random b-sets | | null | | ≈ 0.002 (b = 6) | |

  Samples are seed 5 with 3·10⁵ S, except 6·10⁴ at 3877, 1.5·10⁶ at 1621 and 10⁵ at 1789 (the referee's run).
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
  | 1621 | all | 1 | 0.42 | 2.32 | 0.34 | 0.38 (2.4) | 1.03 |
  | | 2+2 | 0.708 | 0.30 | 2.81 | 0.38 | 0.44 (1.7) | 1.07 |
  | | not 2+2 | 0.292 | 0.12 | 3.33 | 0.32 | 0.76 (1.6) | 0.90 |
  | 1789 | all | 1 | 4.50 | 31.7 | 1.77 | 14.8 (9.2) | 2.66 |
  | | 2+2 | 0.804 | 3.62 | 36.7 | 1.97 | 17.3 (11.7) | 2.84 |
  | | not 2+2 | 0.196 | 0.88 | 11.9 | 1.06 | 5.5 (3.5) | 1.81 |

  Runs have 5000 configurations, except 10⁴ at 1789. The 1789 run is the survey run itself (same stream), and its
  2+2 share of 0.804 is higher than the 0.736 of the smaller pairsym sample (heavy tails, §12.2).
- **What the split shows.**
  - The 2+2 share does not separate spike primes from typical ones: it is 70–88% at λ ≈ 0.21 in both (1621: 71–74%).
  - What separates them is the family's weight factor F (§12.5 item 3: 2.3–4.4 at spikes, 0.30 at 1621). The 2+2
    part's class values also separate them: B_D 4.3–17.3 at spikes, against 0.44 (z 1.7, 2σ < 0.65) at 1621.
  - The not-2+2 part is lifted at spike primes as well: rate 0.61–0.88 μ₁ against 0.12 at 1621, and B_D 2.3–5.8
    (z 3.5–8.2). At 1597, 1657 and 1933 the referee also found (not yet computed at 1789):
    - 39–48% of it lies in buckets that also hold 2+2 T's.
    - As a whole it points the same way as the 2+2 part (weighted cosine 0.97–0.98 over L and 0.59–0.92 over D) at
      0.55–0.73 of the size.
    - It carries 1–3% of the total weighted |V|².
  - The data fit one S- and bucket-level property of a spike prime that raises the count and the class values of the
    whole measure. The 2+2 flag marks most of the configurations it acts on, at spike and typical primes alike. Why
    some primes have this property is open (§12.7).

### 12.5 Weight of involution families [heuristic; corrected after review]

1. **The 4×4 block.**
   - Normalise a split ι to x ↦ −x, with rows (a, −a, b, −b) and columns (x, −x, y, −y). Let h = ind(−1),
     P = ind(r − x) and Q = ind(r + x).
   - Then M[r, x] = P, M[r, −x] = Q, M[−r, x] = h + Q and M[−r, −x] = h + P.
   - Rank 1 holds iff P − Q ≡ c on the whole block with 2c ≡ 0, and P itself is rank-1.
   - That has probability 2κ⁻⁵ at even κ (c ∈ {0, κ/2}) and κ⁻⁵ at odd κ, against κ⁻⁹ for a generic 4×4 block.
   - For a non-split ι(x) = ε/x, each 2×2 pair block needs 2(ind(a − x) − ind(ax − ε)) ≡ −ind ε (mod κ). At even κ
     there is no solution, because ind ε is odd. At odd κ there is exactly one.
   - Averaged over the two kinds, the enhancement is κ⁴ at every κ.
   - Checks:
     - The referee measured the 2×2 rate at κ = 6 as 0.332 for split and 0 for non-split involutions, and 0.143 for
       both at κ = 7.
     - `block_rate.py` (split only, 11 primes, 4·10⁶ samples each) finds 0.87–1.03 of 2κ⁻⁵.
     - Three primes sit 3–4σ low, and the ratio has rank correlation 0.67 with N₁/μ₁ (9 primes). The effect is
       below 13%.
2. **The 2+2 weight.**
   - For a fixed ι, a uniform T contains two ι-pairs with probability ≈ N_inv/p².
   - If the other (κ−1)² − 9 conditions behave independently, the structured rate relative to μ₁ is
     R₂₊₂(κ, p) = N_inv(κ)²·κ⁴/p².
   - κ = 6: R₂₊₂ = 2.62·10⁶/p². That is 1.03 at 1597, 1.00 at 1621, 0.96 at 1657, 0.82 at 1789, 0.70 at 1933, 0.48 at
     2347 and 0.17 at 3877.
   - κ = 7: R₂₊₂ = 2.65·10⁷/p², 0.020–0.022 at λ ≈ 0.3.
   - At fixed λ = 0.2 it is 1.1, 0.048 and 0.0010 at κ = 6, 7, 8.
3. **The arithmetic factor F.**
   - The measured structured rate (2+2 share × N₁/μ₁) is F(p)·R₂₊₂.
   - At κ = 6:

     | p | F |
     |---|---|
     | 1621 | 0.30 |
     | 1597, 1657 | 3.2–3.9 |
     | 1789 | 2.3–4.4 |
     | 1933 | 2.6–3.3 |
     | 2347 | 0.7 |
     | 3877 | 0.8 |

     Each range comes from taking the share and N₁/μ₁ from the pairsym sample, or from the survey or split runs. The
     largest value, 4.4, is the 1789 split (share 0.804 × N₁/μ₁ 4.50 over R₂₊₂ = 0.82).
   - At κ = 7: 1.8 at 35281, 0.5 at 35099, 2.3 at 36037 and 0.9 at 34693, from 19, 5, 28 and 9 structured
     configurations.
   - Across κ = 6 and 7, R₂₊₂ changes 50×, and the weight follows it to within F = 0.3–4.4.
   - At fixed κ the p⁻² fall-off is not visible. At the typical κ = 6 primes 1621, 2347 and 3877 the structured rate is
     0.30, 0.34 and 0.14, about p^{−0.9}. Over the same primes R₂₊₂ falls 6× and F rises from 0.3 to 0.8.
   - F is not predicted, its maximum over primes is unknown, and at spike primes it is uncertain by up to 2× (§12.2).
4. **General families.**
   - Take g ∈ PGL₂ of order m, with a g-orbits in S and b in T, and set x = am/κ, y = bm/κ.
   - The codimension in (S, T) is c = (a+b)(m−1) − 2. The rank-1 deficit is E = (m−1)(abm − a − b): E = 4 for the 2+2
     block, and κ²/2 − κ for full involution symmetry.
   - There are κ^{O(κ)} placements and an O(1) solvability factor. At p = κ^{γκ}:
     log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ).
   - Since xy ≤ (x + y)/2, every family with x + y bounded below is negligible once γ > 1/2 + O(1/κ). Families with
     x + y = O(1/κ) satisfy E/c ≤ κ/2 + O(1), which gives the same conclusion.
   - Full involution symmetry (even κ, averaged over the two kinds) has R_full = ((κ−1)!!)²κ^{κ²/2−κ}p^{2−κ}
     (κ = 6: 4.9·10¹¹/p⁴). This is < 1 once p > κ^{κ/2+1−1/ln κ+o(1)}.
5. **Along the threshold path.**
   - The exponent needs OSC′ at T(κ) = κ^{κ/2+κ/(2 ln κ)+O(1)} (§11.8). There R₂₊₂ = κ^{12−κ−κ/ln κ+O(1)} and
     R_full = κ^{−κ²/(2 ln κ)+O(κ)}.
   - At the typical-constant thresholds of §11.8, R₂₊₂ is 0.026 (κ = 6, p ≈ 10⁴), 0.010 (κ = 7), 0.0012 (κ = 8),
     1.1·10⁻⁴ (κ = 9) and 7.6·10⁻⁶ (κ = 10).
   - The weight w = F·R₂₊₂ is up to 4.4% at κ = 7 and 0.5% at κ = 8 with the largest measured F (4.4).
6. **The family's effect on the constants.**
   - Let the family have share w ≪ 1 and noise-subtracted absolute D-group rms v. V is linear in the measure, so
     ρ_D ≤ (1 − w)ρ_rest + w·v. The family adds at most w·v, which is F·v·N_inv²κ²/p in units of κ²/p.
   - At T(κ), N_inv²κ²/p is 10.6, 7.4, 3.9 and 1.7 for κ = 7, 8, 9, 10, and it tends to 0 like
     κ^{10−κ/2−κ/(2 ln κ)+O(1)}.
   - F·v at the five split primes, with F and v (from the 2+2 part's B_D) taken from the same run: 0.003 (1621),
     0.27 (1933), 0.35 (1597), 0.98 (1657) and 1.53 (1789). That is a 500× spread.
     - With the largest value (1789), the family adds B_D ≈ 16, 11, 6 and 3 at κ = 7–10.
     - With 1621's values (2σ) it adds at most 0.05, 0.03, 0.02 and 0.01.
     - OSC′ is stated for every p ≥ p₀, so what matters is the largest F·v over primes near T(κ). That is not measured
       at any κ ≥ 7.
   - **Without v.**
     - |Q| ≤ n, because each symmetrised character has modulus ≤ 1. So v ≤ n.
     - The family then adds at most F·N_inv²κ² to B_D and F·N_inv²κ⁴/p to B_L, both F·κ^{O(1)}.
     - §11.8 tolerates B_D up to κ^{(1−o(1))κ}.
     - So, granting the first-moment weight, the 2+2 family can change the exponent only through F, that is, only if
       F(p) = κ^{Ω(κ)} at some p ≥ p₀.
   - The L group gains at most w·v_L ≈ 0.044·1.97 = 0.09 at κ = 7 with the 1789 values.
7. **What this does not say.**
   - It is a first-moment count with an independence assumption.
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
  | 23549 | 0.200 | 67.4 | … | | | … |

  The se include the bucket clustering.
- **Carry-over test at λ ≈ 0.3.**
  - The two primes with the largest symR (44, against 9.4–22 at eleven others at λ ≈ 0.3) have N₁/μ₁ 1.09 and 0.89.
  - Over the six primes N₁/μ₁ = 0.89–1.11, with no rank relation to symR (Spearman 0.09).
  - The κ = 6 proportionality would give ≈ 2.5. At κ = 7 symR no longer predicts the measure, as expected when the
    2+2 weight is 2%.
  - This tests carry-over of the κ = 6 behaviour, not §12.5. A 2+2 share of 1–4.5% moves N₁/μ₁ by about 0.05·F,
    below these se. The informative κ = 7 number is F (§12.5 item 3).
- **λ = 0.2.**
  - 23549 has the highest symR of the κ = 7 primes sampled (67), and R₂₊₂ = 0.048 there.
  - A p-law predicts N₁/μ₁ ≈ 1; the κ = 6 behaviour at λ = 0.2 would predict about 2.5.
  - Measured: N₁/μ₁ …, 2+2 share ….
- **Class values at 36037.** `mc_classes.py 7 36037 10⁴ --seed 13` gives B_L …, B_D … (2σ < …), PW_pair … and c ….
- **Generic rate.**
  - The not-2+2 rate is 0.84–1.04 μ₁ at κ = 7, λ ≈ 0.3.
  - At κ = 6 it is 0.44 at the same λ (2347), and 0.12 and 0.70 at λ = 0.21 and 0.50 (1621 and 3877; one prime each,
    and 1621 is in the bottom third of its band).
  - So the κ = 6 shortfall of generic configurations is not a function of λ alone.

### 12.7 Arithmetic of spike primes [computed; post hoc]

- **B_D > 2 occurs only at p ≡ 1 (mod 12)** (h = ind(−1) ≡ 0 mod 6).
  - That is 6 of the 15 survey primes there (1597, 1657, 1669, 1693, 1789, 1933), and 0 of the 13 primes ≡ 7 (mod 12),
    where the largest B_D is 1.00.
  - The evidence is weak:
    - With the cut at 2, the one-sided probability at n = 25 was 0.024.
    - It is 0.14 after the residue partitions looked at, and 0.25 with the cut also chosen.
    - A rank test of B_D by class gives one-sided 0.026 at n = 28 (0.07 at n = 26). But H was formed on 17 of these
      primes; on the 9 that finished after it was written, the same test gives 0.08.
  - Class medians: B_D 0.93 against 0.60; N₁/μ₁ 1.16 against 0.69.
  - One prospective sD prime so far: 1789, at h = 0. Since 6 of the 9 prospective primes are h = 0, that had
    probability 0.67 under the null. No band yet qualifies for (H2).
- **No mechanism is known.** For a configuration fully symmetric under x ↦ −x, z and −z contribute equally whatever h
  is: the class modes are sum-zero and taken up to cyclic shifts of the values. For 2+2 configurations only the paired
  coordinates are shifted copies. So this excludes h acting through the z ↔ −z pairing, not h acting at all. At odd κ,
  h = 0 for every p.
- **What ranks symR.**
  - Detrended log symR rises with |a|/√p, where p = a² + 3b². This is |L|/(2√p) in the notation of §11.6.
  - Spearman is 0.53 at h = 0 and 0.47 at h = 3 (30 primes each, λ ≤ 0.31), and 0.50 over all 60.
  - At h = 0 the residual is also higher when 2 is a cubic residue: median +0.57 against −0.05. At h = 3 there is no
    such effect (−0.30 against −0.38).
  - The fixed cyclotomic cell combines both effects at h = 0. When 2 is a cube, 36A(0,0) = p − 17 − 20a exactly
    (a ≡ 1 mod 3, checked at 17 primes), so |A(0,0) − mean|/√p = (5/9)|a|/√p. Otherwise it is ≤ 0.25. Hence its
    Spearman 0.81, against 0.27 for A(0,3).
  - This also explains why |L| ≈ 0 failed as a spike predictor in §11.6: small |a| goes with low symR.
  - All of this is post hoc.
- **Other statistics** (λ ≤ 0.25, n = 27): K has Spearman 0.77 with N₁/μ₁ and 0.52 with B_D; max|D|/√p has 0.43
  with B_D.
- **Prospective tests.** `survey/predictions_hclass.txt` (02:16; mechanism retracted at 02:24) and
  `survey/predictions_N1mu1.txt` (01:20) are checked when the survey finishes.

### 12.8 Answer, and what it changes

- **Answer [computed at κ = 6, 7; heuristic beyond].**
  - At κ = 6, λ ≤ 0.25, the constants are finite at every measured prime, as any finite sample must be at fixed κ.
    Their size is the information.
  - Spike primes reach B_L 1.88 (1657) and B_D 14.8 (1789), 4× and 18–25× the band medians. 8 of the 28 primes are
    spikes by some flag.
- **What spikes are.**
  - At λ ≈ 0.21, 70–88% of (C1) configurations are 2+2 involution-structured, at spike and typical primes alike.
  - Spikes are primes where this family's weight factor F (2.3–4.4 against 0.3) and its class values (B_D 4.3–17.3
    against 0.44) are both large, and where the not-2+2 part is lifted too.
  - Why some primes are like this is not explained. |a|/√p and the cubic character of 2 rank it in part (§12.7).
- **p against λ.**
  - Across κ = 6 and 7 the family's weight follows N_inv²κ⁴/p² to within F = 0.3–4.4. So the heuristic ties spike
    weight to p, not λ.
  - At fixed κ the two cannot be separated. Below λ = 0.3 only κ = 6 is measured (23549 at κ = 7 is pending).
- **κ = 7.** The 2+2 share is 1.1–4.5% at four primes, against an expected 1.9–2.4%. N₁/μ₁ is 0.89–1.11 at six primes
  with symR 16–44.
- **What changes.** Obstruction (c) of §11.8 narrows to three questions:
  1. Is F(p) of order κ^{o(κ)} uniformly over p ≥ p₀? Granting the first-moment weight, this is the only way the
     2+2 family can affect the exponent (§12.5 item 6).
  2. Does the independence assumption behind the first-moment weight hold?
  3. What is the not-2+2 part at spike primes?

  With the largest measured F·v (1789) the family would add B_D ≈ 16 at κ = 7 (≤ 0.05 with typical values), falling
  to 0 as κ grows. That is bounded, so harmless for the exponent if F stays bounded.
- **Claim gates that stay false.**
  - OSC′ in either form at any κ.
  - Any rigorous bound on spike constants.
  - R₂₊₂ or the family estimate as a theorem.
  - Threshold certificates at κ ≥ 6.
  - An unconditional exponent statement.
  - F(p) bounded, or κ^{o(κ)}, over p ≥ p₀.
  - Obstruction (c) resolved.
  - Hypothesis H, or the |a|/√p and cubic-character correlations, as claims.
  - "κ = 7 has no spike primes" (six primes at one λ).
  - The 2+2 family's class values at κ ≥ 7, or v falling with p.
  - The not-2+2 part at spike primes under control.

### 12.9 Next

- **Finish the survey.** Run `k6_spike_survey.py` and score both prediction files. Acceptance: spike frequency and
  amplitude per band; H1–H3 kept or refuted; the N₁/μ₁ log errors per band.
- **F over the survey.**
  - Run `pairsym.py 6 p 300000` at every survey prime with λ ≤ 0.25 (5–20 min each) and compute F with the survey's
    N₁/μ₁.
  - Acceptance: the distribution of F and its maximum, and Spearman with |a|/√p and with the cubic class of 2.
  - A model for F in terms of the cubic Jacobi sum is the first step towards bounding its maximum, which is
    question 1 of §12.8.
- **The direct test of (c)** still needs κ = 8 at λ ≈ 0.18 (p ≈ 3.8·10⁵) with a sampler that builds (C1)
  configurations directly (§11.9). That sampler is the main gap.
- **Proving the weight.**
  - The goal is an upper bound O(N_inv²κ⁴p⁻²μ₁) for the 2+2 count.
  - The block conditions are explicit. The rest is an upper bound for a (C1) count on a codimension-2 family, which
    §9's existence proof does not give.
  - Weil's error terms are κ^{O(κ²)}√p, useless at p = κ^{O(κ)}. So no method is in hand.
