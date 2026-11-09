# Referee report: κ = 6 spike survey and partial involution structure (2026-11-10)

Independent Claude subagent, briefed by `BRIEF.md` (claims 1–5) and `HEURISTIC.md`. The harness did not let the
subagent write files, so the author transcribed its report here unchanged in substance. The author's disposition of
every point is at the end. The referee's scratch scripts and outputs are in `scratch/` (about 4 CPU-minutes, nice 19).

## Main findings

1. **R₂₊₂ is off by a factor of 2 at even κ.** An involution with no fixed points in P¹(F_p) (non-split) can never
   give a rank-1 2×2 block on its pairs at even κ. About half of the involutions of a random S are non-split, so the
   correct rate is R₂₊₂ = N_inv²κ⁴/p² at every κ.
2. **The old pairsym "max over ι" count undercounted by up to 16 points.** The corrected `pairsym.py` (exact union
   over involutions) prints exactly the values the referee computed independently on the same samples.
3. **The λ-term of the claim-1 fit rests on one prime, 3877.** Leaving 3877 out flips the sign of the λ-coefficient.

## Claim 1 (symR predicts N1/μ1): overstated. The correlation is real; "predicted" needs qualifying

- **Correct:**
  - The `sym_rate.py` sampling, the fixed-bucket test and the share f for split involutions.
  - The fit reproduces exactly (−0.142 + 0.978 log symR + 1.932 log λ, residual sd 0.196).
  - The checks at 1933, 2347 and 4219 reproduce (log errors +0.03, −0.02, +0.15).
  - The two strictly prospective primes, 1699 and 1747, come in at −0.16 and +0.33.
- **Spearman:** 0.96 over 14 primes. With 1747 added it is 0.90 (n = 15, bootstrap 95% interval 0.64–0.98).
- **Problems:**
  - **The λ-term rests on 3877.** 13 of the 14 fit primes span only 0.10 in log λ. Leaving 3877 out moves the
    coefficient from +1.93 to −2.06, and that fit mispredicts 3877 by a factor of 39.
  - **What is solid is narrower.** In the low-λ band N1/μ1 ≈ 0.038·symR, with log-sd 0.18 over 13 primes. That
    scatter is about the size of the sampling errors: symR se about 6–15% at 10⁵ S, N1/μ1 se 2–10%.
  - **The held-out set was an accident of file names.** `survey/predict_n1.py:10` names `mc_k6_p1933_s11.log` and
    similar files, which do not exist. That is the only reason 1933, 2347 and 4219 were held out of the fit.
- **f omits non-split involutions at even κ:**
  - The statement in the `sym_rate.py` docstring, "up to PGL₂, S = {±r_i}", is false at even κ (it holds at odd κ).
  - At κ = 6 the S that are symmetric under a non-split involution have no fixed buckets, and their rate is small:
    0.56 ± 0.17 at 1621 and 0.89 ± 0.31 at 1657.
  - The exception is 1531, at 26 ± 13. 1531 is also the fit's largest residual (+0.56), so C_sym is a lower estimate.
- **symR is a spike indicator, not the mechanism.** It is a second, cheap Monte Carlo measurement at the same prime.
  C_sym is a steady 1/7.8 of N1/μ1.
- **Suggested wording:** "N1/μ1 tracks symR (Spearman 0.90, n = 15; ≈ 0.038·symR with log-sd 0.18 at λ ≈ 0.2). A fit
  whose λ-term is calibrated on one λ = 0.5 prime reproduced 1933, 2347 and 4219 within 0.15 in log."

## Claim 2 (67–86% structured): wrong as worded

- **Checks that passed:**
  - The involution construction is correct (2000 of 2000 random cases; trace 0 in every run).
  - The old counting functions match brute force in 190 cases.
  - The null model is sound: 0.002 at b = 6, against an expected 7·10⁻⁴.
  - The new `pairsym.py` is a correct exact union.
- **The old method undercounts.** On the same seed-5 samples:

  | p | old (max over ι) | exact (union) |
  |---|---|---|
  | 1597 | 0.729 | 0.875 |
  | 1657 | 0.673 | 0.830 |
  | 1933 | 0.560 | 0.700 |
  | 2347 | 0.426 | 0.444 |
  | 3877 | 0.160 | 0.167 |

  The brief's 67% (the old method at 1657) and 86% (mc_split at 1597) mix the two methods.
- **Only split involutions occur.** At κ = 6 no structured T comes from a non-split involution (0 of 845–1459 per
  prime).
- **Suggested wording:**
  - 70–88% at λ ≈ 0.21: about 70% at the typical prime 1621 (mc_split still running, 1261 of 1810), 78–88% at the
    spike primes 1597, 1627 and 1657.
  - 70–76% at 1933, 44% at 2347, 17% at 3877; random b-sets about 0.1%.
  - Counting ι-fixed points as units adds 4–8 points.

## Claim 3 (mc_split): code confirmed, interpretation overstated

- **The code checks out:**
  - The reproduction re-verified at 1933, seed 7, 49 configurations: max |ΔS1| = 0, S2 and counts identical.
  - The parts sum to the total (to 1.6·10⁻¹⁴).
  - `split_report.py` reproduces every quoted constant: B_D structured 11.6 / 4.3 / 4.4 and unstructured 5.8 / 2.6 /
    2.3 at 1657 / 1597 / 1933; B_L 1.24 / 1.32 / 1.00 at 1933.
  - `analyse` applies to a part. V is then the part's conditional mean, which is not linearly additive into the total.
- **The interpretation does not follow:**
  - 39–48% of the non-2+2 configurations at the spikes lie in a bucket that also holds 2+2 T's.
  - Their class values nearly copy the structured part's at 0.55–0.73 of the size: weighted cosine 0.97–0.98 over L,
    0.59–0.92 over D.
  - They carry only 1–3% of the total weighted |V|².
  - So "unstructured" means only "not 2+2".
  - The "typical 0.4–0.9" baseline is the all-configuration B_D and mostly noise-level (z 1.3–5.3, cluster-corrected
    0–0.66).
- **Supporting point the brief misses:** the non-2+2 rate is 0.55–0.79 μ₁ at the spikes against ≈ 0.10 at 1621, so
  those configurations are 5–8× more frequent at spikes.
- **Suggested wording:** the data fit one S- and bucket-level mechanism that the per-T flag only partly captures, not
  a second, independent mechanism.

## Claim 4 (HEURISTIC.md): partly wrong

- **Confirmed by re-derivation:**
  - N_inv = 45 and 105.
  - The split-case 4×4 block probability e_κκ⁻⁵.
  - The codimension c = (a+b)(m−1)−2 and the condition deficit E = (m−1)(abm−a−b).
  - The R_full threshold and the asymptotics.
- **§3 correction** (`HEURISTIC.md:24`): R₂₊₂ = N_inv²κ⁴/p².
  - κ = 6: 2.62·10⁶/p², which is 1.0 at 1621, 0.70 at 1933, 0.48 at 2347 and 0.17 at 3877, and equals 1 at
    p ≈ 1620.
  - At the thresholds: 0.0012 at κ = 8 and 7.6·10⁻⁶ at κ = 10. κ = 7 and κ = 9 are unchanged.
- **R_full** (line 39) is right only because split (e = 2) and non-split (e = 0) involutions average to 1. The note
  should say so.
- **§4 omits a discrete solvability factor.** It is O(1), so the asymptotics are unaffected.
- **§5's range for F changes.** It becomes 0.3 (1621) to 3.6–3.9 (1597, 1657), with 0.7–0.8 at 2347 and 3877,
  instead of 0.15–1.4.
- **Minor:**
  - Over F_p there are two classes of involutions, not one.
  - The leading-term argument does not cover families with x + y = O(1/κ). The conclusion still holds, via
    E/c ≤ κ/2 + O(1).
  - `block_rate.py` tests split involutions only.
  - "No spike dependence" is too strong. Three primes sit 3.3–4.2σ low, and the ratio has rank correlation 0.67 with
    N1/μ1 (n = 9). The effect is under 13%, so it cannot explain 10× spikes.

## Claim 5 (κ = 7 is Poisson, unlike κ = 6): numbers confirmed, conclusion premature

- **Confirmed:**
  - 35281: var/mean 0.999; b = 7 and b = 8 at 0.95× and 0.92× Poisson; N1/μ1 0.90 ± 0.05.
  - 35099: N1/μ1 0.96; b = 7–9 at 0.93–1.11× Poisson.
  - κ = 6 at 1933: 21× and 690× Poisson.
  - symR 9.4–44 over 13 primes.
  - The 2+2 shares, 0.043 ± 0.014 and 0.011 ± 0.005, are within about 2σ of the corrected expectation ≈ 0.024.
- **Problems:**
  - var/mean says nothing about the tail: the spike prime 1933 also has 0.990.
  - The κ = 6 comparison is to a selected spike prime at a different λ. The typical 1951 shows 1.8× and 4.5× excess
    in the tail, and typical κ = 6 primes at λ ≈ 0.21 sit below Poisson (0.39–0.46).
  - Both κ = 7 primes tested have low or middle symR (15.8, 21.3). The candidate spike primes 36037 and 34693
    (symR 44) are untested; the κ = 6 proportionality would put them near 2.5.

## Other problems, by severity

1. (High) The `pairsym.py:4–7` docstring repeats the factor-2 error: the 2·6⁻⁵ block probability holds only for split
   involutions.
2. (High) Everything downstream of the old shares needs updating: the brief's 56%, 43%, 16% and 67%, and §5's F.
3. (Medium) `sym_rate.py` omits non-split involutions, in its docstring and in f.
4. (Medium) The claim-1 fit is calibrated on one prime, and its held-out set came from a file-name accident.
5. (Low) `k6_spike_survey.analyse` (lines 70–72) breaks on small parts. An empty batch gives NaN, and the round-robin
   assertion misfires below about 30 configurations. Both are likely for κ = 7 structured parts.
6. (Info) Typical κ = 6 primes at λ ≈ 0.21 have N1/μ1 ≈ 0.4, about 70% of it 2+2, so the generic rate is about
   0.1 μ₁. Condition (N) of OSC′ already needs B ≥ 2.6 there.

## Author's disposition (2026-11-10)

- **Factor 2 at even κ: accepted, and checked independently.**
  - For ι(x) = ε/x with ε a non-square, the 2×2 block on rows (a, ιa) and columns (x, ιx) is rank-1 iff
    2(ind(a − x) − ind(ax − ε)) ≡ −ind ε (mod κ).
  - At even κ, ind ε is odd, so there is no solution. At odd κ there is exactly one, as for split involutions.
  - The referee's `scratch/checks_small.out` agrees: at κ = 6 the 2×2 rate is 0.332 for split and 0 for non-split
    involutions; at κ = 7 it is 0.143 for both.
  - Fixed in the topic note §12.5, the `pairsym.py` docstring and a superseded note at the top of `HEURISTIC.md`.
- **Undercount: accepted.** It was already fixed before the report. The author's exact reruns (`pairsym/*.out`, seed 5)
  give 0.875 (1597), 0.830 (1657), 0.780 (1627), 0.700 (1933), 0.444 (2347) and 0.167 (3877), equal to the referee's
  values where both exist.
- **Claim 1: accepted.**
  - The file-name accident is confirmed: the logs are `mc_k6_p1933.log` and so on, without `_s11`.
  - The wording now follows the suggestion. The λ-term is labelled as calibrated on one prime, and the held-out primes
    as unplanned.
- **Non-split omission in `sym_rate.py`: accepted.** The docstring is corrected and C_sym is called a lower estimate.
- **Claim 3: accepted.** The reading is now one S- and bucket-level mechanism, and "unstructured" is called "not 2+2".
- **Claim 4 minor points: accepted** in §12.5. These cover the two involution classes, the O(1) solvability factor,
  families with small x + y, and the block_rate spike dependence (at most 13%).
- **Claim 5: accepted.** The spike candidates were then measured: N1/μ1 = 1.09 at 36037 (symR 44). See §12.6 of the
  topic note.
- **Small parts in `analyse`: noted.** No κ = 7 part was analysed.

# Round 2 (2026-11-10): the §12 draft (`SEC12_DRAFT.md`)

Same referee, resumed with the draft and the 1621 and κ = 7 numbers. About 2.2 CPU-minutes. Its new scratch files are in
`scratch/`: `r2_stats.*`, `r2_hclass25.*`, `r2_cube.*`, `r2_cube2.*`, `pairsym_k6_p1789_1e5.out`, `survey_out_r2b.txt`
and `fixedcell_out.txt`. The summary below is the author's, close to the referee's text.

## Round-2 findings

- **New data confirmed.**
  - `split_report.py split/split_k6_p1621` reproduces the author's table exactly. The part files carry Nunl·share, so the
    noise per part is right.
  - F(1621) = 0.30, v = 0.0098 (2σ < 0.0144), and the family adds ≤ 0.046 at T(7).
  - κ = 7 rates: 34693 0.89 ± 0.05, 34259 1.11 ± 0.08, 36037 1.09 ± 0.06. These se are clustering-aware (a b = 8 bucket
    gives 8 configurations).
  - 36037's 2+2 share is 0.045 (F 2.3–2.4).
  - 1789 (`pairsym.py 6 1789 1e5`): share 0.736 at a sample N₁/μ₁ of 2.53 ± 0.22. The survey has 4.50 ± 0.42, so
    F(1789) = 2.3–4.0.
- **1. §12.5 item 6.** The arithmetic is right (10.6, 7.4, 3.9, 1.7; the step ≤ w·v holds by Minkowski).
  - v and F move together: F·v is 0.003, 0.24, 0.34 and 0.98 at 1621, 1933, 1597 and 1657, a 330× spread. OSC′ quantifies
    over every p ≥ p₀, so the maximum of F·v near T(κ) is what matters, and it is not measured.
  - Asymptotically v is not needed. |Q| ≤ n gives ΔB_D ≤ F·N_inv²κ² and ΔB_L ≤ F·N_inv²κ⁴/p, so, given the first-moment
    weight, the family can change the exponent only if F(p) = κ^{Ω(κ)} at some p ≥ p₀.
  - Delete "the family alone cannot make the constants grow along the path". The weight w = F·R₂₊₂ is up to 4% at κ = 7,
    not ≤ 1%.
- **2. §12.7.**
  - (a) At n = 25, 5 of 13 h = 0 primes have B_D > 2, against 0 of 12 at h = 3. The one-sided probability is 0.024. It
    is 0.14 family-wise over the residue partitions the survey prints, and 0.25 with the cut also free. A rank test with
    no cut gives 0.22, and the class medians are 0.83 and 0.61. The one prospective sD prime, 1789 (h = 0), had
    probability 0.71 under the null.
  - (b) The 02:24 retraction is right for fully symmetric configurations. For 2+2 configurations only the paired
    coordinates are shifted copies, so h drops out only if the other coordinates are independent. h could still enter
    through the order-6 cyclotomic numbers, whose formulas differ between f even and f odd.
  - (c) The fixed-cell correlation (0.81 against 0.27) is robust but misattributed. At h = 0, when 2 is a cube,
    36A(0,0) = p − 17 − 20a with p = a² + 3b², a ≡ 1 (mod 3); when 2 is not a cube, |t| ≤ 0.25. The residual rises with
    |a|/√p in both classes (0.53 and 0.47), and at h = 0 it is also higher when 2 is a cube. So "at h = 3 nothing found
    so far does" is wrong.
- **3. §12.6.**
  - The comparison is fair, but it tests carry-over of the κ = 6 proportionality, not §12.5. With a 2+2 share of 1–4.5%,
    any symR effect moves N₁/μ₁ by about 0.05·F, which these se cannot see.
  - The informative κ = 7 number is F.
  - The "seven others" have median 16.3, not 16.7, and `sym/sym_rate_k7.out` has four more λ = 0.30 primes (symR
    10.9–17.4).
  - The generic κ = 7 rate (0.84–1.04) is fair; contrast it with κ = 6 at the same λ (2347: 0.44).
  - The κ = 6 not-2+2 trend is one prime per λ, and 1621 is in the bottom third of its band.
- **4. §12.8.**
  - "OSC′_rms holds at every measured prime" is vacuous at fixed κ. Keep the sizes: B_D now reaches 14.8 (1789), 18–25×
    the band medians.
  - "The spikes are projective structure" is overstated. The typical 1621 is 72% 2+2. What marks a spike is that F and
    the family's class values are both large. The not-2+2 part at spikes (B_D 2.3–5.8) is not covered by item 6.
  - "F ≤ 3.9" is the largest measured value, not a bound.
  - "A small-p effect, not small-λ" is vacuous at fixed κ (p = λκ^{κ−1}). The p⁻² fall-off is not visible at fixed κ:
    the typical-prime structured rate falls about like p^{−0.9}, with F rising 0.3 → 0.8. The support is across κ.
  - "(c) loses its main evidence" is overstated. (c) is narrowed to three questions: whether F is κ^{o(κ)} uniformly,
    whether the independence assumption holds, and what the not-2+2 part is at spike primes.
  - Add claim gates: F bounded; (c) resolved; H and the Jacobi-sum correlations as claims; "κ = 7 has no spike primes";
    the family's class values at κ ≥ 7; the not-2+2 part under control.
- **5. §12.3–12.4 against round 1.** Faithful, with five fixes:
  - C_sym = f·symR, not f·symR/Poisson.
  - Update the statistics to n = 25.
  - The cosines compare the whole not-2+2 part with the 2+2 part, and that part carries only 1–3% of the weighted |V|².
  - Say "the data fit one … mechanism".
  - Fill in 1621.
- **Other.**
  - (Medium) N₁/μ₁ at spike primes is heavy-tailed: single S with buckets of 10–12 points. Smaller runs come out low (1789
    2.53 against 4.50, 1657 3.71 against 4.47, 1627 2.05 against 2.64). Use the largest run, and run
    `mc_split.py 6 1789 10000 --seed 13`.
  - (Medium) §12.2 lags the survey.
  - (Low) Update K and max|D| to n = 25.
  - (Suggestion) Test p against λ at κ = 7, λ = 0.2: `bucket_stats.py 7 23549` and `pairsym.py 7 23549`.

## Author's disposition, round 2

- **Accepted and checked independently:**
  - The cyclotomic identity and the |a|/√p correlation (`scratchpad` check, reproduced in §12.7). 36A(0,0) = p − 17 − 20a
    exactly at all 17 primes with h = 0 where 2 is a cube. Spearman of the symR residual with |a|/√p is 0.53 (h = 0),
    0.47 (h = 3) and 0.50 over all 60 primes with λ ≤ 0.31. At h = 0 the median residual is +0.57 when 2 is a cube and
    −0.05 when it is not; at h = 3 it is −0.30 and −0.38.
  - The trivial bound |Q| ≤ n: |Sym_R| ≤ 1 and there are n points z.
- **Accepted as worded:** items 1, 3, 4 and 5 and the claim gates. §12.5 item 6, §12.6, §12.7 and §12.8 are rewritten.
- **The 1621 share.** The referee's 0.724 is from the old max-over-ι file, read before the exact rerun finished. The exact
  value is 0.741, or 0.786 counting fixed points.
- **H with the survey at n = 26.**
  - 1933's seed-13 run is now in: 6 of the 14 h = 0 primes have B_D > 2, against 0 of 12 at h = 3.
  - 1933 was a known spike before the prediction, so it is not prospective. The rank-test caveat stands.
- **Runs started on the referee's suggestions:** `mc_split.py 6 1789 10000 --seed 13`, and `bucket_stats.py 7 23549 6·10⁵`
  with `pairsym.py 7 23549 3·10⁵`.
