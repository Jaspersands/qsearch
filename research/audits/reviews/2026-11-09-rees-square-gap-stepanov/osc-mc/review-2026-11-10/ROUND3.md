# Round 3 (2026-11-10): the §12 draft r3 (`SEC12_DRAFT_r3.md`)

Independent referee (Claude subagent), third round. Read: `SEC12_DRAFT_r3.md`, `SEC12_DRAFT.md`, `REPORT.md` (rounds 1
and 2 with the author's dispositions), §11.6–11.8 of the topic note, and the raw files named in the brief. Ran only
`split_report.py` (all five split runs) and two scripts of my own, `scratch/r3_checks.py` and `scratch/r3_checks2.py`
(outputs `scratch/r3_checks*.out`). About 10 CPU-seconds at nice 19. No existing file was edited; the four
`scratch/r3_checks*` files are new.

## Verdict

r3 applies the round-2 corrections faithfully. Every number I could recompute from the raw files reproduces: the 1789
split rows, F and F·v at the five split primes, the §12.5 item 6 chain, the survey tables, Spearman values, the
prospective N₁/μ₁ scoring and the h-class statistics (up to rounding). None of the six listed overstatements survives
verbatim. One survives as a heading: §12.4 is still called "Mechanism". There are four substantive problems:
- §12.7 identifies |a|/√p with §11.6's |L|/(2√p) and uses that to "explain" a §11.6 result. Both are false whenever 2
  is not a cubic residue.
- F at the sN spike 1627 (1.6–2.1) is left out, so the quoted range at spikes, 2.3–4.4, is too narrow.
- The snapshot is labelled 03:20, but its data predate 03:13. 1867, 1879 and 1987 have finished since. That completes
  λ ≤ 0.25, adds an sN spike (1759) to band 2, and breaks "PW_pair > 1.4". H survives (0 of 16 at h = 3).
- The reading in §12.4 and §12.8 is mis-scoped in places: the 2+2 share does separate spikes from 1621 at λ ≈ 0.21;
  "narrows to three questions" omits what §12.5 item 7 excludes; and Q2 is part of Q1.

Recommendation: record after fixing findings 1–5. Findings 6–12 are precision and wording.

## Findings, by severity

### 1. (High; changes a claim) §12.7 "What ranks symR": |a|/√p is not |L|/(2√p)

- **Location.** "This is |L|/(2√p) in the notation of §11.6", and "This also explains why |L| ≈ 0 failed as a spike
  predictor in §11.6: small |a| goes with low symR."
- **Problem.**
  - Write p = a² + 3b² and 4p = L² + 27M², as in §11.6 and `cubic_LM.py`. Then |L| = 2|a| iff 3 | b, i.e. iff 2 is a
    cubic residue. Otherwise the associate a + b√−3 and the primary J = (L + 3M√−3)/2 differ in argument by ±60°.
  - So |L| ≈ 0 forces |a|/√p ≈ √3/2. The two statistics agree at only 25 of the 60 primes with λ ≤ 0.31, the cube
    primes.
  - Spearman with the detrended log-symR residual (the `scratch/r2_cube2.py` detrending, λ ≤ 0.31) is 0.50 for |a|/√p
    and 0.09 for |L|/(2√p) (h = 0: 0.53 against 0.37; h = 3: 0.47 against 0.08).
  - The §11.6 primes with |L| ≈ 0 contradict the explanation:
    - 1951, 3571 and 4219 have |a|/√p = 0.86, 0.87 and 0.86, near the maximum. The |a| correlation predicts high symR
      there, not low.
    - The one cube prime among them, 3889, has |a|/√p = 0.016. Yet it has the highest symR (5.26) of the 29 primes at
      λ ≈ 0.5, and it is the pre-fix λ = 0.5 spike.
- **Correct wording.**
  - "|a|/√p is |cos| of the argument of the associate a + b√−3 of the cubic Jacobi sum. It equals §11.6's |L|/(2√p)
    only when 2 is a cube (25 of 60 primes). |L|/(2√p) itself has Spearman 0.09 with the residual, consistent with
    its failure as a predictor in §11.6."
  - Delete "This also explains …".
  - Also say that at h = 3 the |a|/√p correlation sits in the cube subclass: 0.79 (n = 13) against 0.19 (n = 17,
    `scratch/r2_cube.out`).
- **Check.** `r3_checks.py`, last block: rep_a and rep_L at all 89 primes, and the residual as in `r2_cube2.py`.

### 2. (Medium; numbers change on update) The snapshot is mislabelled and stale (§12.1, 12.2, 12.3, 12.7, 12.8)

- **Problem.**
  - The `survey_n28.out` content postdates 1951's npz (03:10:22) and predates 1867's (03:13:37). The file was written
    at 03:15:19, so "snapshot 03:20" is wrong. At 03:20 1867 was finished.
  - 1879 finished at 03:21:02 and 1987 at 03:22:22, all three at h = 3. λ ≤ 0.25 is now complete (30 primes).
- **What changes.**

  | prime | λ | N₁/μ₁ | PW_pair | B_L | B_D (z) |
  |---|---|---|---|---|---|
  | 1867 | 0.240 | 0.68 | 1.29 | 0.387 | 0.50 (3.4) |
  | 1879 | 0.242 | 0.57 | 1.14 | 0.374 | 0.32 (2.8) |
  | 1987 | 0.256 | 0.92 | 1.55 | 0.527 | 0.85 (10.2) |

  - **Band 0.222–0.249 is now 15 primes.**
    - Medians: B_L 0.55, B_D 0.59, PW_pair 1.77, N₁/μ₁ 0.82. The N₁/μ₁ median falls from 1.08 because of the gap
      between 0.82 and 1.08.
    - Spikes are now 3: 1759 sN (1.89 > 2 × 0.82), 1789 and 1933. So 1759 (h = 3) joins 1531 and 1627 as a count
      spike without a value spike.
  - **Band 0.251–0.31** (1951, 1987): medians 0.51 / 0.59 / 1.29 / 1.17, no spikes.
  - **§12.2.** "PW_pair is above 1.4 at every prime with λ ≤ 0.25" is false: 1879 has 1.14 and 1867 1.29. All are
    still > 1, so the conclusion stands.
  - **§12.8.** "8 of the 28" becomes 9 of 31.
  - **§12.7.**
    - B_D > 2 at 6 of 15 (h = 0) against 0 of 16 (h = 3); the largest h = 3 value is still 1.00.
    - Exact one-sided Mann–Whitney 0.013 (n = 31). Medians B_D 0.93 / 0.56, N₁/μ₁ 1.16 / 0.68.
    - The prospective set becomes 12 (adding 1867, 1879 and 1987). 6 of the 12 are h = 0, so 1789's null probability
      is 0.50, not 0.67. Mann–Whitney on the 12: 0.066.
    - No band qualifies for (H2): band 2's new primes are 6 at h = 0 and 4 at h = 3. H1 is not refuted.
  - **§12.3.** With 1867 and 1879 the prospective N₁/μ₁ score (15 primes, 1933 excluded) is rms 0.24, mean +0.04 and
    max 0.37 (1879: 0.57 against 0.39).
- **Fix.** Either relabel the snapshot (≈ 03:11, 28 primes) or update to n = 31.
- **Check.** File mtimes; `r3_checks.py` (`analyse` on every finished s13 npz, band flags recomputed).

### 3. (Medium; changes a quoted range) F at 1627 is omitted

- **Location.** §12.5 item 3 table; §12.4 "F (§12.5 item 3: 2.3–4.4 at spikes, 0.30 at 1621)"; §12.8 "F (2.3–4.4
  against 0.3)".
- **Problem.**
  - 1627 (sN, h = 3, B_D 1.00) is in the §12.4 pairsym table (share 0.780) but not in the F table.
  - F(1627) = 0.780 × 2.05 / 0.991 = 1.61 with the pairsym sample, and 0.780 × 2.64 / 0.991 = 2.08 with the survey
    N₁/μ₁.
  - So over the five spikes with a measured share F is 1.6–4.4. The range 2.3–4.4 holds only for the four sD spikes.
  - 1627 is the one case of F ≈ 2 without a value spike. That fits "F and class values both large", but the
    dichotomy as printed hides it.
- **Fix.**
  - Add "1627 | 1.6–2.1".
  - Write "F 1.6–4.4 at the five spike primes with a share (2.3–4.4 at the four sD spikes), against 0.3 at 1621 and
    0.7–0.8 at 2347 and 3877".
- **Check.** `r3_checks.py`, F block.

### 4. (Medium) Leftover overstatement of the 2+2 reading (§12.3, 12.4, 12.8)

- (a) **The §12.4 heading still reads "Mechanism: partial involution symmetry".** §12.3 also points to it ("symR is
  not the mechanism … (§12.4)"). §12.4's own conclusion is that 2+2 marks about 70% of configurations at the typical
  1621 too, and that what makes a spike is open. The heading restates the reading withdrawn in round 2. Suggested
  heading: "Partial involution structure of (C1) configurations".
- (b) **"The 2+2 share does not separate spike primes from typical ones" is contradicted at λ ≈ 0.21.**
  - The spike shares there are 0.83–0.88 (1597, 1657) and 0.78 (1627), against 0.71–0.74 at 1621. The S-batch se is
    ≈ 0.01, so the gap is ≈ 10σ, though against one typical prime.
  - What holds: the share is high at the typical prime as well, and across λ the spike shares (0.70–0.80 at 1789 and
    1933) overlap 1621's.
- (c) **"at spike and typical primes alike" (§12.4, §12.8) rests on one typical prime with a share at λ ≈ 0.21
  (1621).** Say so.
- (d) **§12.8 "Spikes are primes where F … and its class values … are both large …" is measured at 4 of the 8
  spikes** (the split runs). Write "At the four split spike primes …".

### 5. (Medium-Low) §12.8 "narrows to three questions" is too narrow, and Q2 is inside Q1

- **Inconsistent with §12.5.**
  - Item 7 says the analysis "says nothing … about structure that is not projective".
  - Item 4's conclusion for the other bounded-orbit families assumes an O(1) solvability factor and no arithmetic
    enhancement, i.e. their analogue of F is O(1). That is unmeasured.
  - Neither appears among the three questions. Q3 covers only the not-2+2 part at spike primes. The r2 draft had
    "structure that is not projective is not excluded"; it was lost when the round-2 wording was adopted.
- **Q2 is part of Q1.**
  - F is defined as the measured structured rate over R₂₊₂ (item 3), so w = F·R₂₊₂ is an identity.
  - Item 6's bound ΔB_D ≤ F·N_inv²κ²·(n/p) then needs only Minkowski and v ≤ n, and no first-moment assumption. It
    picks up a factor 1/(N₁/μ₁) ≤ B (finding 8). Any failure of independence shows up as F.
  - So "granting the first-moment weight" in item 6 and in Q1 can be dropped. That strengthens the statement.
- **Suggested wording.** (c) narrows to:
  1. Is F(p) = κ^{o(κ)} uniformly over p ≥ p₀? This is unconditional, because F is defined in item 3.
  2. The same question for the arithmetic factors of the other bounded-orbit families of item 4.
  3. What are the not-2+2 part at spike primes and any non-projective structure at κ ≥ 7?

### 6. (Low-Medium; changes a claim) §12.3 "the primes at λ ≤ 0.25 do not test" the λ-term: they do, weakly

- **Lever arm.** The 13 prospective primes sit Δ log λ = +0.10 above the 13 low-λ fit primes.
- **Fits scored on them** (mean / rms log error):

  | fit | mean | rms |
  |---|---|---|
  | as filed | −0.01 | 0.22 |
  | refit without 3877 (λ-coefficient ≈ −2.1 to −2.2) | +0.43 | 0.48 |
  | λ-coefficient fixed at 0, intercept and symR slope refit on the 13 low fit primes | +0.21 | 0.30 |

- **What this gives.**
  - Without using 3877, the prospective primes need a λ-coefficient of 2.0 ± 0.6.
  - They do not separate the filed fit from a 14-prime fit with no λ-term (symR slope 0.75; mean +0.02, rms 0.23).
  - Consistently, N₁/μ₁/symR is 0.038 in the λ < 0.22 band and 0.048 in the 0.22–0.25 band.
- **Caveat.** The λ step coincides with the survey's switch from 5000 to 10⁴ configurations at p = 1700. Under the
  heavy tails of §12.2 that could bias the same way.
- **Suggested wording.** "The prospective primes (0.10 higher in log λ) need a λ-coefficient of 2.0 ± 0.6 given the
  low-λ symR slope, and reject the fit without 3877 (mean error +0.43). They do not separate a λ-term from a flatter
  symR slope, and the configuration count also changes at p = 1700."
- **Check.** `r3_checks2.py`.

### 7. (Low-Medium) §12.2 and §12.5 item 3: the heavy-tail statements

- **"Understates … by up to a factor 2".** At 1789 the survey gives 4.50 ± 0.42 and the pairsym sample 2.53 ± 0.22, a
  gap of 4.2σ. Bringing it to 2σ needs the se scaled by ≥ 2.1, so "by a factor of about 2 or more" is the defensible
  wording.
- **"Smaller samples … come out low" is not general.** At 1933 the largest sample is the lowest:

  | sample | configurations | N₁/μ₁ |
  |---|---|---|
  | bucket_stats, 3·10⁶ S | 19,532 | 2.55 |
  | survey, seed 13 | 10⁴ | 2.67 |
  | survey, seed 11 | 2·10⁴ | 2.63 |
  | pairsym | 2,083 | 2.72 |
  | split (first 5,022 of the seed-13 stream) | 5,022 | 3.07 |

  With the largest sample, F(1933) is 2.5–2.8, so its range is 2.5–3.3 rather than 2.6–3.3.
- **Say which run the 1933 split row is.** It is the first half of the survey stream, not the survey run (full
  stream: N₁/μ₁ 2.67, B_D 3.66).
- **The F uncertainty.** "Uncertain by up to 2×" should say the spread between runs is up to 1.9×, and that the
  direction is not consistent across primes.

### 8. (Low) §12.5 item 6: state the transplant assumption and match the tolerance

- **The assumption.**
  - "The family adds B_D ≈ 16, 11, 6, 3" holds only if the family's absolute D-rms v keeps its κ = 6, p = 1789 value
    at T(κ). That means its B_D in κ²/p units grows about 21× by T(7).
  - With constant family B_D (17.3 κ²/p), as in a constant-B p-law, the addition is w·B_D = 0.78 at κ = 7 and 0.09 at
    κ = 8.
  - Write "would add", and give both numbers.
- **The tolerance.**
  - "§11.8 tolerates B_D up to κ^{(1−o(1))κ}" is the tolerance for keeping the exponent below κ.
  - The (1/2+o(1))κ exponent survives only while log_κ B_D = o(κ). That tolerance is what matches the conclusion "only
    if F = κ^{Ω(κ)}". State both.
- **Share against weight.**
  - The Minkowski step needs the family's share of the measure, which is F·R₂₊₂/(N₁/μ₁). Item 6 sets it equal to
    F·R₂₊₂, i.e. takes N₁/μ₁ = 1.
  - Under (N) the bound gains at most a factor B. That is harmless asymptotically and about 1 at the κ = 7 primes
    (N₁/μ₁ 0.89–1.11), but it should be said.
- **The numbers.**
  - 10.6, 7.4, 3.9, 1.7 reproduce only with §11.8's log_κ T row (5.57, 6.18, 6.78, 7.36, i.e. λ_T 0.433, 0.182,
    0.0685, 0.0229).
  - With the rounded λ_T 0.44, 0.18, 0.07, 0.02 of §11.8(c) they become 10.4, 7.5, 3.8, 2.0; κ = 10 is 15% off. Cite
    the precise λ_T.

### 9. (Low) §12.8 "the heuristic ties spike weight to p, not λ"

- **What the across-κ evidence supports.**
  - At equal λ ≈ 0.3 the 2+2 rate falls from 0.34–0.36 at 2347 (κ = 6) to 0.010–0.048 at κ = 7, a drop of 7–35×.
    R₂₊₂ predicts 22–23×; a λ-law would predict none.
  - That supports "the 2+2 weight is not a function of λ alone and falls as R₂₊₂ does".
- **What it does not support.** The spike excess is F, which the heuristic does not model.
- **Fix.** Replace "spike weight" with "the 2+2 baseline weight".

### 10. (Low) §12.7 bookkeeping

- **"H was formed on 17 of these primes".** The predictions file says 17 survey primes plus the earlier S-batched runs,
  and the 1933 seed-11 run is among "seen so far".
- **"On the 9 that finished after it was written".** Ten survey runs finished after 02:16: 1741, 1777, 1783, 1789,
  1801, 1831, 1861, 1873, 1933 and 1951. The 9 exclude 1933's rerun, a known spike. 1759 finished at 02:14:40 and was
  excluded unseen, as pre-registered.
  - Suggested wording: "on the 9 primes it was pre-registered for (1933's rerun excluded as known)".
  - The value 0.08 reproduces (exact 0.083).
- **"One-sided 0.026 at n = 28".** Exact Mann–Whitney on full-precision B_D gives 0.023. 0.026 reproduces only from the
  2-decimal table with continuity correction. n = 26 gives 0.065 exact (0.07 as printed).
- **Mixed snapshots.** The cut test is quoted at n = 25 (0.024) beside a rank test at n = 28. At n = 28 the cut test is
  0.013 (C(15,6)/C(28,6)). Quote both at n = 28.

### 11. (Low) §12.6, κ = 7

- **"Spearman 0.09".** It hinges on symR 44.22 (34693) against 44.19 (36037), 0.03 apart at 3·10⁴ symmetric S.
  Swapping them gives 0.31. At n = 6 neither is informative (the one-sided 5% critical value is about 0.83). Write
  "no detectable rank relation (n = 6)".
- **"0.84–1.04".** The range mixes samples: 0.84 is the pairsym sample at 35281 and 1.04 bucket_stats at 36037. Within
  one sample it is 0.84–1.01 (pairsym) or 0.86–1.04 (bucket_stats).
- **The κ = 7 F counts (19, 5, 28, 9) are clustered.** A b = 8 bucket gives up to 8 configurations; at 35281, 12 of
  the 19 come from b = 8 buckets. So the relative errors exceed 1/√n, which is already 23–45%.
- **23549: "A p-law predicts N₁/μ₁ ≈ 1".**
  - This holds only if the κ = 7 generic rate stays at its λ = 0.3 level at λ = 0.2. At κ = 6 it fell from 0.44 to
    0.12 between λ = 0.30 and 0.21.
  - The cleaner pre-registered discriminator is the 2+2 share. The p-law gives F·0.048/(N₁/μ₁), a few percent; the
    κ = 6 behaviour gives 0.7–0.9.

### 12. (Trivial) Nits

- **§12.1.** `k6_spike_survey.out` does not exist; only `review-2026-11-10/survey_n28.out` does.
- **§12.3, provenance.** `predictions_N1mu1.txt` and `predict_n1.py` both have mtime 01:48:17, and the header says
  01:20. 1699 finished at 01:33:23, so its prospective status rests on the header. The fit excludes 1699 and the error
  there is −0.16, so there is no sign of leakage.
- **§12.3, the 0.038 ratio.** "0.038·symR, log-sd 0.18 over 13 primes": the snapshot band has 14 primes, giving
  0.038 and log-sd 0.17.
- **§12.3, 1951.** It is off by +0.44 at full precision (1.416 against 0.91), not +0.45.
- **§12.5 item 1, block_rate.**
  - 1579 sits 4.6σ low (0.868 ± 0.029), so "3–4σ" should be 3.3–4.6σ.
  - The largest deficit is 13.2%, not "below 13%".
  - The rank correlation with N₁/μ₁ is now 0.78 over the 10 block_rate primes with a survey value.
- **§12.7, "(5/9)|a|/√p".** It is approximate. The exact value is |20a + 15|/(36√p), a deviation of at most 0.011.
- **§12.2, "therefore".** "(N) … therefore needs B ≈ 2.6" follows from N₁/μ₁ as low as 0.39, not from the noise
  sentence before it. 1741, at 0.37, needs 2.7.
- **§12.4, involutions.** "fixed by two of its 2-cycles" should read "determined by". N_inv is the number of
  pair-pairs, an upper bound on the distinct involutions.
- **§12.5 item 2.** The range 0.020–0.022 covers the four primes with a share; over all six κ = 7 primes it is
  0.020–0.023 (34259: 0.0226).
- **§12.5 item 5.** w is 4.5% at F = 4.41 and T(7) = 7^5.57.

## What reproduces (from the raw files)

- **1789 split** (`split_report.py split/split_k6_p1789`): all three rows exactly.

  | part | share | N₁/μ₁ | PW_pair | B_L | B_D (z) | c |
  |---|---|---|---|---|---|---|
  | all | 1 | 4.50 | 31.68 | 1.773 | 14.83 (9.2) | 2.66 |
  | 2+2 | 0.804 | 3.62 | 36.73 | 1.966 | 17.25 (11.7) | 2.84 |
  | not 2+2 | 0.196 | 0.88 | 11.85 | 1.058 | 5.54 (3.5) | 1.81 |

  The other four split tables also match.
- **F and F·v (split runs, R₂₊₂ = 2,624,400/p²).**

  | p | 1621 | 1933 | 1597 | 1657 | 1789 |
  |---|---|---|---|---|---|
  | F | 0.300 | 3.33 | 3.64 | 3.89 | 4.41 |
  | F·v | 0.0029 | 0.274 | 0.352 | 0.979 | 1.531 |

  The F·v spread is 520×. The pairsym-based ranges in item 3 reproduce (1597 and 1657: 3.22–3.89; 1789: 2.27–4.41;
  1933: 2.66–3.33; 2347: 0.71–0.75; 3877: 0.80–0.81). The exception is 1627, finding 3.
- **R₂₊₂ at κ = 6.** 1.03, 1.00, 0.96, 0.82, 0.70, 0.48 and 0.17. Fixed λ = 0.2: 1.1, 0.048, 0.0010. Along the path:
  0.026, 0.0102, 0.00124, 1.08·10⁻⁴, 7.6·10⁻⁶.
- **Item 6.**
  - Family B_D: 16.2, 11.3, 6.0 and 2.65 at κ = 7–10.
  - 1621 at 2σ: 0.046, 0.032, 0.017 and 0.008.
  - w = 4.5% (κ = 7) and 0.55% (κ = 8).
  - L gain 0.088.
- **Survey snapshot (`survey_n28.out`).**
  - Band medians, maxima and spike lists as printed.
  - Spearman 0.95 / 0.92 / 0.93 / 0.74; K 0.77 and 0.52; max|D| 0.43.
  - C_sym ratio 8.51 (7.78–12.19).
  - 1789 at 25× and 18× the medians, the largest B_D at any κ (κ = 4, 5 max 2.07 and 3.04).
  - Typical-prime ranges as printed.
- **Prospective N₁/μ₁.**
  - 13 primes (1699–1861 and 1873): rms 0.220, mean −0.010, max 0.339 (1831).
  - 1789: 4.50 against 5.25. 1951: +0.44.
- **h-class.**
  - 6 of 15 against 0 of 13; medians 0.93 / 0.60 and 1.16 / 0.69.
  - Prospective 9: 6 at h = 0, giving 0.67; Mann–Whitney 0.083.
- **κ = 7.**
  - The table reproduces from `buckets/*.out` and `sym/sym_rate_k7*.out`: N₁/μ₁, var/mean, the b = 7, 8 ratios and the
    shares (19/446, 5/455, 28/624, 9/428).
  - F: 1.76–1.80, 0.48–0.49, 2.33–2.40 and 0.85–0.91.
  - Expected share 1.9–2.4% with the pairsym samples' own N₁/μ₁. "Eleven others, 9.4–22" is correct.

## Round-2 corrections

- **Done.**
  - The factor 2 at even κ: items 1–2, R_full "averaged over the two kinds".
  - The pairsym undercount, now an exact union.
  - The misattributed cyclotomic correlation: |a|/√p in both classes, the cube effect at h = 0 only. Finding 1 is a new
    error in the sentence added with this fix.
  - The retracted phase mechanism: the 2+2 caveat is included. It could also name the order-6 cyclotomic numbers as a
    remaining route for h.
  - C_sym = f·symR, the cosine scope, "the data fit one … property", 1621 filled in, the heavy tails, and the new
    claim gates.
- **The listed overstatements.**
  - "Spikes are projective structure" is absent from §12.8 but survives as the §12.4 heading (finding 4a).
  - "Small-p not small-λ" is now explicitly not a fixed-κ claim; "spike weight" remains (finding 9).
  - "F ≤ 3.9" and "weight ≤ 1%" are absent. "Up to 4.4% … with the largest measured F" is acceptable.
  - "(c) loses its main evidence" and "the family alone cannot make the constants grow" are absent.

# Author's disposition of round 3 (2026-11-10)

The recorded text is `SEC12_DRAFT_r4.md`, the same as §12 of the topic note. My own checks are in
`scratch/author_r3_verify.py` and `scratch/author_snap_stats.py`; I did not reuse the referee's scripts.

1. **Accepted; verified independently.**
   - I recomputed (a, b) and (L, M) myself:
     - at 1951, 3571 and 4219: |a|/√p 0.86–0.87 and |L|/(2√p) about 0.01;
     - at 3889 (2 a cube): both 0.016;
     - |a| = |L|/2 at the cube primes 1597 and 1657, but not at 1621 (0.32 against 0.98).
   - 3889 has the highest symR of the 29 primes at λ ≈ 0.5.
   - With a plain linear detrend, the residual has Spearman 0.48 with |a|/√p and 0.08 with |L|/(2√p).
   - Changes: the identification is replaced, "This also explains …" is deleted, and the cube-subclass split at h = 3
     (0.79 against 0.19, `r2_cube.out`) is added.
2. **Accepted.**
   - The snapshot is replaced by `survey_snapshot.out`: 35 primes, at 03:45. λ ≤ 0.25 is now complete. I recomputed all
     its statistics at full precision.
   - New since the referee's 31-prime check:
     - 1987 (h = 3) was flagged sD at the 34-prime snapshot, when its band had 5 primes, and loses the flag at 35. The
       text now calls flags in partial bands provisional, and H1 is decided at band completion.
     - PW_pair falls below 1 at 2011 (0.92).
3. **Accepted.** I recomputed F(1627) as 1.61 and 2.08.
4. **Accepted.**
   - The §12.4 heading is renamed.
   - The share sentence now says it separates spikes only modestly.
   - "Alike" is scoped to the one typical prime.
   - The claims are scoped to "the four split spike primes".
5. **Accepted.**
   - The three questions are reworded as suggested.
   - "Granting the first-moment weight" is dropped. Item 6 is labelled an elementary bound, with the share factor
     1/(N₁/μ₁) ≤ B stated.
6. **Accepted.**
   - I reproduced the refit without 3877: coefficient −2.055, prospective mean +0.417, rms 0.471.
   - The 2.0 ± 0.6 is quoted as the referee's estimate.
   - The confound at p = 1700 (5000 vs 10⁴ configurations) is stated.
7. **Accepted.**
   - I confirmed bucket_stats at 1933 (2.55 at 3·10⁶ S, with 71% of configurations from the top 0.1% of S).
   - F(1933) is now 2.5–3.3, and the 1933 split row's provenance is stated.
   - The wording is now "up to 1.8× in N₁/μ₁ and 1.9× in F, in no consistent direction".
8. **Accepted.**
   - Both scalings are given: absolute v fixed (16, 11, 6, 3) and constant B_D (0.78, 0.09).
   - Both tolerances are stated, and the precise λ_T are cited.
   - w is corrected to 4.5% and 0.55%.
9. **Accepted.** The text now says "the 2+2 baseline weight", with the comparison of 2347 against κ = 7 at λ ≈ 0.3.
10. **Accepted.**
    - The tests are exact at full precision.
    - The cut test is quoted at λ ≤ 0.25 (0.011).
    - The pre-registered set is 16 primes. Its test gives 0.010, or 0.057 restricted to λ ≤ 0.25, because h = 3 primes
      are 4 of the 6 above λ = 0.25.
11. **Accepted.**
    - "No detectable rank relation (n = 6)".
    - The generic rate, 0.86–1.04, is from bucket_stats.
    - The clustering of the κ = 7 F counts is noted.
    - The 2+2 share is named as the 23549 discriminator.
12. **All nits accepted.** I verified the block_rate figures (3.3–4.6σ, deficit 13.2%, ρ = 0.78 over 10 primes) and
    |20a + 15|/(36√p) myself.

# Round 3b (referee, 10 Nov 04:10): r3 → r4, the 35-prime snapshot, and κ = 7 at 23549

**Verdict: OK to record after the wording fixes below. None of them changes a number or a conclusion.**
- Every r4 number taken from the 03:45 snapshot reproduces from the 35 npz files. The other r3 → r4 changes check out.
- Findings 1–12 are applied correctly.
- Item 6's algebra and the three questions are right, except that one qualifier is missing: the size of B in (N).
- The 23549 numbers the coordinator sent reproduce. One scoping change is needed: the "not λ alone" conclusion
  should rest on the 2+2 weight, not on the share.
- Script and output: `scratch/r3b_checks.py` and `.out`. It ran in 3 CPU-s, using `k6_spike_survey.analyse` on the 35
  snapshot files, which were all finished by 03:44:13.

## What reproduces

- **Band table.**
  - Medians (B_L / B_D / PW_pair / N₁/μ₁):
    - 0.502 / 0.816 / 2.810 / 0.973;
    - 0.546 / 0.594 / 1.769 / 0.820;
    - 0.430 / 0.435 / 1.247 / 0.638.
  - Maxima: 1.879 and 10.53 (1657); 1.773 and 14.83 (1789); 0.527 (1987) and 0.91 (1993).
  - The flags are as in r4; band 3 has only 1951 sN. 9 of the 29 primes are spikes, 6 of them by sD.
- **1987.**
  - B_D 0.853, z 10.19, 2σ lower end 0.765.
  - Its band median was 0.340 with 5 primes (flagged) and is 0.435 with 6 (not flagged). The r4 statement is right.
- **§12.2.**
  - At λ ≤ 0.25 the PW_pair minimum is 1.138 (1879). 2011 (0.92) is the only value below 1.
  - The N₁/μ₁ minimum is 0.365 (1741), so B = 2.74.
- **§12.3.**
  - N₁/μ₁/symR has geometric means 0.0380 (log-sd 0.172) and 0.0510 (log-sd 0.251), with sd taken with n − 1.
  - Spearman at λ ≤ 0.25:
    - symR against N₁/μ₁, B_L and B_D: 0.921, 0.915, 0.770;
    - K against N₁/μ₁ and B_D: 0.779, 0.556;
    - max|D|/√p against B_D: 0.460.
  - N₁/μ₁/C_sym: median 9.35, quartiles 7.79–12.35.
- **§12.7.**
  - B_D > 2: 6 of 15 against 0 of 14 (h = 3 max 1.00), and 6 of 17 against 0 of 18.
  - The cut test gives 0.0105, and the exact one-sided rank test 0.0184 (n = 29).
  - Pre-registered set: 1741, 1777–1879 without 1933, and 1951–2017, 16 primes. It gives 0.0103, and its 10 primes
    at λ ≤ 0.25 give 0.0571 (its 6 above give 0.13).
  - Medians: B_D 0.93 / 0.56, N₁/μ₁ 1.16 / 0.67. h = 3 is 4 of the 6 above 0.25.
  - The npz times match the 17/16 split. 1747, 1723 and 1753 finished by 02:10, 1759 at 02:14:40, and the 16 from
    02:20:50 on.
- **Prospective N₁/μ₁.**
  - The 15 primes 1699–1879: rms 0.239, mean +0.036, max +0.372 (1879).
  - The 6 above 0.25: rms 0.247, mean +0.063, max +0.442 (1951).
- **Other r4 changes.**
  - Split not-2+2 rates: 0.61 / 0.75 / 0.88 / 0.73, against 0.124 at 1621.
  - κ = 7 F: 1.78, 0.48, 2.34 and 0.91, from 19, 5, 28 and 9 configurations, using each pairsym sample's own ratio.
    12 of the 19 at 35281 come from b = 8 buckets.
  - The 2+2 rate drops 7–34×, against R₂₊₂'s 21.7–23.4×.
  - Typical κ = 6 rates: 0.30 / 0.34 / 0.14 (slope −0.87).
  - Also reproduced: R₂₊₂ at the thresholds; N_inv²κ²/T = 10.6 / 7.4 / 3.9 / 1.7; both κ-exponents.
- **What ranks symR.**
  - 25 of the 60 primes are cube primes.
  - |L| = 2|a| iff 3 | b, and otherwise |L| = |a ± 3b|, at all 60.
  - Every Spearman value and median reproduces exactly, including 0.09 for |L|/(2√p), when log symR is detrended by a
    log–log fit on all 89 primes. A fit on the 60 alone moves them by up to 0.13.

## Findings 1–12

All are applied as accepted:
1. |a| against |L| is rewritten, and the new numbers are right.
2. The 35-prime snapshot is labelled, with the provisional-flag rule.
3. 1627 is in the F table.
4. §12.4 is renamed and says "only modestly". 1627 is kept apart from the four split spike primes.
5. The three questions are rewritten.
6. The λ-term paragraph is fixed.
7. Heavy tails: 1.8× = 4.50/2.53, se factor about 2, and the 1933 values.
8. Item 6:
   - both v scalings (16/11/6/3 with B_D growing 21×; 0.78 and 0.09);
   - the share factor;
   - the tolerances;
   - λ_T.
9. "2+2 baseline weight".
10. The §12.7 bookkeeping.
11. §12.6.
12. The nits.

Item 6's algebra is right:
- s = F·R₂₊₂/(N₁/μ₁) ≤ B·F·R₂₊₂ under (N).
- With v ≤ n, B_D gains s·v·p/κ² ≤ F·B·N_inv²κ²·n/p, and B_L gains s·n = F·B·N_inv²κ⁴·n/p². Both are ≤ F·B·κ^{O(1)}.
- "No independence assumption" is right. F is the measured rate by definition, so the bound is a
  reparametrisation, and the claim gate says so.

## Fixes needed

1. **B in (N)** (item 6, last bullets, and §12.8 Q1).
   - The bound is F·B·κ^{O(1)}, so the family can spoil (1/2+o(1))κ only if F·B = κ^{Ω(κ)}.
   - That reduces to a condition on F alone only if B = κ^{o(κ)}. §11.8's (N) fixes no size for B, and §9 measures B
     up to 9.9.
   - Replace "with N₁/μ₁ bounded below as (N) gives" and "With N₁/μ₁ bounded below" by "if (N) holds with
     B = κ^{o(κ)}".
2. **Tolerances** (item 6).
   - "Survives B_D up to κ^{(1−o(1))κ}" is true only for §11.8's particular o(1).
   - Use §11.8's own form: an exponent below κ survives while log_κ B_D < (1 − 1/ln κ)κ − O(1) and
     log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1). The exponent (1/2+o(1))κ needs both to be o(κ).
   - The family adds to B_L too, so the B_L condition belongs here.
3. **(H3)** (§12.7). "So both classes occur" rests on 1951's flag, which r4's own rule makes provisional. Write "so
   (H3) holds, provisionally".
4. **"0.05·F"** (§12.6, λ ≈ 0.3; left over from round 3).
   - There the 2+2 weight is F·R₂₊₂ ≈ 0.02·F. The measured 0.010–0.048 already includes F.
   - Write "moves N₁/μ₁ by F·R₂₊₂ ≈ 0.02·F (measured 0.010–0.048)".
5. **Nits.**
   - §12.4: the full 1933 run has N₁/μ₁ 2.66 (2.6648), not 2.67.
   - §12.7: 1759's npz is from 02:14:40, so it is not among "those that finished after 02:16". Write: "the 16 that
     finished after 02:16, less 1933's rerun (known). 1759 (file at 02:14–02:16, not looked at) is in neither set."
   - §12.4: the 1789 pairsym row comes from the referee's `scratch/pairsym_k6_p1789_1e5.out` (10⁵ S). Cite it.
   - "What ranks symR": add "detrended by a log–log fit on all 89 primes".

## κ = 7, p = 23549 (the coordinator's two items)

- **Bucket run.**
  - 151 configurations in 6·10⁵ S, against Mλ⁷/7! with M = 5p, give a ratio of 0.836.
  - 135 configurations come from b = 7 buckets and 16 from two b = 8 buckets.
  - The plug-in cluster variance 135 + 2·64 gives se 0.090.
  - var/mean is 0.999, and b = 7 and b = 8 are at 0.914 and 0.542 of Poisson. So "0.84 ± 0.09" is right as a plug-in.
  - The plug-in leaves out b ≥ 9 buckets. None was seen, but under Poisson they carry 1.6% of the configurations, in
    clusters of 36. With Poisson bucket sizes the se is 0.115. Suggest "0.84 ± 0.09 (0.12 with Poisson bucket sizes)".
  - pairsym's 79 configurations in 3·10⁵ S give 0.874–0.876, printed as 0.88. The two runs agree; combined they give
    0.85 ± 0.08.
- **symR law.**
  - 0.038·67.44 = 2.56. That is 1.12 above 0.84 in log, 4.5–6.5 times the κ = 6 law's log-sd. "Fails" is right for
    this prime.
  - "Agrees with the R₂₊₂ reading" is too strong for N₁/μ₁ alone. r4 itself says N₁/μ₁ cannot discriminate while the
    generic κ = 7 rate at λ = 0.2 is unknown. Write "is consistent with". The 2+2 count is the number that
    discriminates.
- **pairsym run.**
  - 5 of 79 = 0.0633, all from b = 7 buckets (63 configurations, 0.079). The 16 b = 8 configurations have none, so the
    5 are unclustered.
  - R₂₊₂ = 26,471,025/23549² = 0.04773.
  - F = 1.11 (with 0.84) to 1.17 (with 0.88). Directly, 5/(nS·μ₁·R₂₊₂) = 1.16, which is the convention of the other
    κ = 7 F values.
  - ±45% is 1/√5. The exact Poisson ranges are 0.66–1.94 (68%) and 0.38–2.71 (95%). Quote the 95% range.
  - The R₂₊₂ share at F = 1 is 5.4–5.7%. For the κ = 6 share, Bin(79, 0.7) gives P(≤ 5) = 8·10⁻³³.
- **Scoping (needed).**
  - The share is the wrong null for "λ alone".
    - s = w/(N₁/μ₁) also depends on the not-2+2 rate. That rate is 0.12 μ₁ at 1621 but 0.79–0.82 μ₁ at 23549.
    - So the drop from 0.7–0.9 to 0.063 mixes a fall in weight with a rise in the generic rate.
    - A λ-only weight (1621's 0.31 μ₁) on top of 23549's not-2+2 rate would give a share of 0.28, not 0.7–0.9.
  - State the test on the weight instead.
    - w(23549) = 0.055 μ₁. At κ = 6, λ ≈ 0.21, w is 0.31 at 1621 (the smallest) and 1.6–3.5 at 1627, 1657 and 1597.
    - With a λ-only weight this run would have about 28 (1621) to 314 2+2 configurations. It has 5, and the Poisson
      P is 1·10⁻⁷ even at 28.
    - b ≥ 8 buckets are too rare to hide that difference in clusters.
  - The drop is 5.6× against 1621 (F 0.31 → 1.16) and 29–63× against the spikes. R₂₊₂ predicts 20–22×.
  - So "drops as R₂₊₂ predicts, up to F" is fair, with F(23549) = 0.4–2.7 at 95%. That is inside κ = 6's 0.3–4.4 and
    κ = 7's 0.5–2.3.
  - The run rejects a λ-only weight. It does not test R₂₊₂ against other κ-scalings within about 10×. It is one prime
    and 5 events.
- **New number to use.**
  - The not-2+2 rate at 23549 is (1 − 0.063)·(0.84–0.88) = 0.79–0.82 μ₁. That compares with 0.12 at 1621 (λ 0.21)
    and 0.86–1.04 at κ = 7, λ ≈ 0.3.
  - It replaces "the generic κ = 7 rate at λ = 0.2 is not known".
  - It extends "the κ = 6 shortfall of generic configurations is not a function of λ alone" to λ = 0.2, at one prime.
- **Consequential §12.8 edits.**
  - "23549 at κ = 7 is pending".
  - The κ = 7 bullet: add 6.3% at 23549 (expected 5.4–5.7%), and N₁/μ₁ 0.84–1.11 at seven primes, symR 16–67.
  - The claim gate "six primes at one λ" becomes seven primes at two λ.
  - The §12.6 table row.

# Author's disposition of round 3b (10 Nov, 04:16)

Every fix is accepted. The 23549 results are folded in. The text recorded as §12 is `SEC12_DRAFT_r5.md`: r4, plus the
23549 results, plus these fixes. r4 is kept as reviewed.
1. **B in (N): accepted.**
   - Item 6 now says the family can spoil (1/2+o(1))κ only if F·B = κ^{Ω(κ)}. That is a condition on F alone if (N)
     holds with B = κ^{o(κ)}.
   - It adds that §11.8's (N) fixes no size for B, and that §9 measures B up to 9.9.
   - §12.8 Q1 says "If (N) holds with B = κ^{o(κ)} … Otherwise the condition is on F·B". The closing paragraph says "if
     F and B stay bounded".
2. **Tolerances: accepted.** Item 6 uses §11.8's form for both groups: log_κ B_D < (1 − 1/ln κ)κ − O(1) and
   log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1). It adds that the family adds to both.
3. **(H3): accepted.** It now reads "So (H3) holds, provisionally", and states H3 itself.
4. **"0.05·F": accepted.** It now reads "The 2+2 weight F·R₂₊₂ ≈ 0.02·F (measured 0.010–0.048) moves N₁/μ₁ by that
   much".
5. **Nits: all accepted.**
   - 2.66.
   - The pre-registration sentence is rewritten: the primes finishing after 02:16, less 1933's rerun, which is 16 at the
     snapshot. 1759 is in neither set.
   - The 1789 pairsym file is cited.
   - The detrend is a log–log fit on all 89 primes.
6. **23549: accepted as scoped.**
   - N₁/μ₁ reads "0.84 ± 0.09 (0.12 with Poisson bucket sizes)", with the pairsym 0.88 and the combined 0.85 ± 0.08.
     N₁/μ₁ is "consistent with" the R₂₊₂ reading and is said not to discriminate.
   - The "not λ alone" conclusion now rests on the weight, in a bullet "The test is the weight, not the share":
     - w = 0.055 μ₁, against 0.31 (1621) to 1.6–3.5 (spikes).
     - A λ-only weight gives 28–314 2+2 configurations; 5 are seen, P ≈ 10⁻⁷ at 28.
     - The share caveat is stated: the not-2+2 rate goes from 0.12 to 0.79–0.82, and a λ-only weight would give a share
       of 0.28.
   - F(23549) = 1.16, with exact Poisson 95% range 0.4–2.7. The drop is 5.6× and 29–63×, against R₂₊₂'s 20–22×.
   - The not-2+2 rate 0.79–0.82 μ₁ replaces "the generic κ = 7 rate at λ = 0.2 is not known". The generic-rate
     statement is extended to λ = 0.2 at one prime.
   - Scope as suggested: it rejects a λ-only weight, does not separate R₂₊₂ from other κ-scalings within about 10×, and
     rests on one prime and 5 events.
   - §12.8: the p-against-λ bullet now uses the weight, and the κ = 7 bullet has 6.3% against 5.4–5.7% and N₁/μ₁
     0.84–1.11 at seven primes, symR 16–67. The gate already read "seven primes at two λ".
   - Item 3 and the §12.6 table carry the same numbers.

# Round 3c (referee, 10 Nov 04:50): κ = 7 class values at 36037

**Verdict: OK to record after the fixes below.**
- Every number reproduces, and the L lift is robust to heavy tails and clustering.
- Two comparisons must be restated: the PW_pair rise and the κ = 6 factors.
- The D group is stronger in sign than the text says, but not in size.
- Script and output: `scratch/r3c_checks.py` and `.out`. It computes everything from the npz arrays through per-batch
  Gram matrices, does not import k6_spike_survey, and ran in 3 CPU-s.

**(1) Numbers.** All reproduce.
- 36037:
  - N₁/μ₁ 1.080 (se 0.021).
  - PW_pair 2.708, floor 0.998 (c_B 0.3365, own seed), CS upper 3.083.
  - B_L 0.635 (z 6.9; 2σ 0.535–0.721). B_D 9.41 (z 1.6, < 14.12).
  - c 1.121, infl 1.99. 16 S-batches of 519–722 configurations (sd 48, against Poisson 25).
- 47041: B_L 0.219 (z 12.0), B_D 1.06 < 2.60, PW_pair 0.470.
- 58787: B_L 0.270 (z 6.1), B_D < 2.10, PW_pair 0.591.
- All 26 pw_bin_cs bins reproduce at both primes.

**(2) Heavy tails and clustering.** Batches are by S, so a cluster such as a b = 9 bucket's 36 configurations sits in
one batch, and X is the mean of the per-batch values y_b.
- **L is robust.**
  - All 16 y_b are positive, and the largest two carry 19% (12.5% if equal).
  - Leave-one-out gives 0.608–0.647 and the worst leave-two-out 0.583.
  - All 12,870 half-samples (8 of 16 batches) give at least 0.506 (5–95%: 0.56–0.71). At 47041 and 58787 the 95%
    points are 0.24 and 0.31.
  - With 8 super-batches (40 random pairings) z is 4.8–9.8. The four bins in the text are positive in every batch.
  - The 2.4–2.9× is not a one- or two-batch effect.
- **D is one common-mode effect.**
  - Batches 3 and 4 carry 45% of it and are the top two in 16 of the 17 m ≥ 7 bins. The bins' batch profiles
    correlate at a median of 0.97, so the 17 positive z are one effect.
  - Its sign is consistent:
    - 85% of batch pairs are positive, against 50% and 38% at 47041 and 58787.
    - The exact sign-flip test gives p = 3·10⁻⁵. Without batches 3 and 4 it gives 1.2·10⁻⁴, the minimum possible.
      At the comparison primes it gives 0.72 and 1.0.
    - Leaving out any two batches keeps B_D ≥ 5.6.
  - So D is resolved in sign but not in size, and "not resolved" may stay. Optional: "positive in every batch, but
    two batches carry 45%; 5.6–10.0 leaving out one or two batches, < 14.1 at 2σ".
  - L and D share these batches (profile correlation 0.94), so they are not independent evidence.

**(3) κ = 6 comparison.**
- 2347 (λ 0.302) against 3571, 3877 and 4219 gives B_L 1.13–1.51× and PW_pair 2.50–2.88×. "About 1.5× and 2.5×" takes
  the top of one range and the bottom of the other. Write "1.1–1.5× and 2.5–2.9×".
- The 0.25–0.31 band maximum (0.53) is right. Those 6 primes are at λ ≤ 0.259, and at 2347 (0.302) B_L is 0.41; say
  so.

**(4) Fixes.**
1. **PW_pair.** Drop "PW_pair 4.6–5.8×" or restate it.
   - At 47041 and 58787 PW_pair sits at its null floor (0.470 against 0.456, and 0.591 against 0.585), so those
     values are noise and depend on run size.
   - At 36037, 2.50 of the 2.71 (92%) is D-group weight, so it repeats the B_D excess. Its L part is 0.206, against
     0.024 and 0.029.
   - Keep the B_L rise.
2. **"Every L bin is lifted".** (0,6) and (0,7) are noise at both primes (z 0.2 and −0.4 at each). Write "every
   resolved L bin". (2,2) and (0,3) carry 63% and 19% of B_L².
3. **κ = 6 factors.** As in (3).
4. **Selection.** The run started at 02:18 (04:30 less 7920 s). The F of 2.3 (pairsym, 02:36) came after the start,
   though before the class values. The earlier drafts named 36037 and 34693 by symR. Write: "picked on symR (the
   highest at λ ≈ 0.3, with 34693) before its F or class values were known. Its F, 2.3, is the highest at κ = 7."
5. **Wording.** "Value-spike candidate" is fair with the caveats. Better: "an L-group value-spike candidate; the D
   excess has a consistent sign but an unresolved size". Add the PW_pair caveat.
6. **Suggestion.** A 2+2 / not-2+2 split of this run, as at κ = 6, would show whether its 4.5% 2+2 share carries the
   (2,2) and (0,3) lift.

# Author's disposition of round 3c (10 Nov, 05:00)

Every fix is accepted. I checked the material claims myself (the times with `stat`, and a short script of my own
on the npz):
- The run started at 02:18:23. The bucket run (N₁/μ₁ 1.09) finished at 02:08 and the pairsym run (F) at 02:36.
- B_L leave-one-out is 0.608–0.647 and the worst leave-two-out 0.583.
- For D at 36037:
  - y_b > 0 in all 16 batches, and the top two carry 45%;
  - leaving out one or two batches gives B_D 5.63–10.61;
  - the one-sided exact sign-flip test gives p = 3.1·10⁻⁵, and 85% of batch pairs are positive.
- At 47041 my sign-flip p is 0.29, not 0.72. That is presumably a different statistic or sidedness, and the text
  cites only 36037's p.

Applied:
1. The PW_pair rise is dropped. The text says PW_pair is 92% D-group weight at 36037, and that at 47041 and 58787 it
   sits at its null floor.
2. "Every resolved L bin", with the 63% and 19% shares of (2,2) and (0,3).
3. κ = 6 factors: B_L 1.1–1.5×, with the band maximum 0.53 placed at λ ≤ 0.259 and 2347 (λ 0.30) at 0.41. The
   PW_pair factor goes with item 1.
4. Selection is as worded: picked on symR before its F or class values were known, and its F, 2.3, is the highest at
   κ = 7.
5. "An L-group value-spike candidate; the D excess has a consistent sign but an unresolved size", with the
   optional D sentence.
6. The suggestion (a 2+2 split of this run) goes in the mechanical plan, item 3.

r5 has been re-synced with the recorded §12 of the topic note, which includes these 36037 additions (05:05).

# Round 4 (referee, 10 Nov 05:15): final κ = 6 survey and the pre-registered scoring

**Verdict: OK to record after the fixes below.**
- Every number quoted in Parts A–C reproduces.
- H1 is refuted as pre-registered, but by 2143 alone. 2179 and 3823 are threshold cases.
- H2 and H3 hold. They still hold when the primes whose values were known at 02:16 are dropped.
- One reading must change: at λ ≈ 0.5 the symR law has no predictive power, and its slope is rejected there.
- Script and output: `scratch/r4_checks.py` and `.out` (8 CPU-s).
  - Per-prime values come from `k6_spike_survey.analyse`.
  - An own Gram-matrix path reproduces B_L, B_D, z, the 2σ ends, PW_pair and CS to 10⁻¹³, and the floor to 2·10⁻⁴
    (own c_B seed).
  - Bands, flags, sets and tests are re-implemented.
  - The script also runs `leaveout_BD.py`, so its output is now on record.

**(1) Band table.** Confirmed.
- (0.25, 0.31]: 31 primes (15 and 16 by class); medians 0.454 / 0.444 / 1.041 / 0.808; 8 flagged.
- λ ≈ 0.5: 29 primes (13 and 16); medians 0.326 / 0.239 / 0.319 / 0.798; 4 flagged.
- λ ≤ 0.25 is as in §12.2 (6 and 3 flagged), so 21 of 89 in all.
- Also confirmed:
  - the table's λ ranges and maxima, and 2113 and 2269 as quoted;
  - min N₁/μ₁ 0.365 (1741), and 1951 unflagged (1.42 against 1.62);
  - the class medians at λ ≤ 0.31;
  - 2347 at seed 13: B_L 0.414, B_D 0.426, PW_pair 0.838;
  - the maxima 14.8 / 6.6 / 1.4 (B_D) and 32 / 11 / 0.89 (PW_pair).

**(2) PW_pair < 1.** Confirmed.
- Debiased: 0 of 29 at λ ≤ 0.25, 13 of 31 in band 3, 29 of 29 at λ ≈ 0.5.
- By CS: 0, 7 and 28. At 3889 the CS value is 1.009.
- The first band-3 value below 1 is still 2011.

**(3) N₁/μ₁ predictions.**
- The rms values reproduce: 0.239 (15), 0.190 (31), 0.132 (28). Over all 74: 0.183, mean +0.039 ± 0.021.
- The file is not post hoc.
  - Its 75 predictions follow from the stated formula (to 0.009).
  - Refitting the 14 in-sample primes gives −0.139 / 0.978 / 1.933.
  - Only 1699 (01:33) predates the 01:48 mtime, as §12.3 says.
- The 0.196 has n in the denominator. With n − 3 it is 0.22.
- 2347 and 4219 were known from their seed-11 runs. Dropping them changes nothing (0.193 and 0.131).
- **Your λ ≈ 0.5 reading is half right.**
  - Within that band log λ spans only 0.12, so the λ coefficient is barely tested: 1.0 ± 0.4 in a free fit, 2.4 ± 0.7
    with the slope fixed.
  - The band mean (+0.05 ± 0.02) does test the level at λ ≈ 0.5 that 3877 alone had set, and confirms it. Without
    3877 the fit misses by about 4× in band 3 and 50× at λ ≈ 0.5.
  - The scatter tests the symR slope and rejects it: the free slope within the band is 0.40 ± 0.07, against 0.98.
  - The rms of 0.13 is no better than a constant. The spread of log N₁/μ₁ there is 0.12, and 3877's value alone gives
    rms 0.127.
  - The within-band slope falls with λ: 1.00 ± 0.06, 0.86 ± 0.09, 0.73 ± 0.07 and 0.40 ± 0.07.
    - Attenuation by symR's own sampling error does not explain this. symR's sample is larger at λ ≈ 0.5: 5·10⁴ to
      1.2·10⁵ configurations, against 800 to 13,000 at λ ≈ 0.2.
  - So the law predicts with real power at λ ≤ 0.31 (rms 0.24 and 0.19, against band spreads of 0.65 and 0.40), and
    with none at λ ≈ 0.5.
  - "About 20% at all 74 later primes" overstates this. 8 of the 74 are off by more than 0.3 in log.
- **Post hoc.**
  - Given symR, N₁/μ₁ is about 15% higher at p ≡ 7 (mod 12).
    - The mean log error is +0.10 to +0.11 at class 7 and −0.03 to −0.05 at class 1, in every band (MW p 0.0002).
  - symR itself is shifted towards class 1 (stratified p 0.005 on the 70).

**(4) H1.** The refutation is clean under the rule, but it rests on 2143 alone.
- 2143 meets every condition:
  - its npz was written at 03:56:51, so it is new;
  - it is ≡ 7 (mod 12);
  - it is sD as registered: the 2σ lower end, from the jackknife se, is above twice the median of all the band's
    primes.
- So the registered clause applies: "H is refuted if any new sD prime is 7 (mod 12)".
- 2143 stays sD with the median taken over the band's primes, over the 70 or over the strict 66 of (5), and under the
  letter of the file.
- **Margins.** f_max = (z/2)(1 − (thr/B_D)²) is the se factor that removes a flag.
  - 2143: 1.68.
  - 2179: 1.002. Its lower end is 0.8873 against 0.8872, and it is unflagged under the strict-66 median (thr 0.908).
  - 3823: 1.015.
  - Class-1 test flags: 2053 1.07, 2269 1.59, 4129 1.67, 2113 1.82, 3889 1.93, 2137 2.54, 2221 2.62, 2341 4.32,
    1789 4.55.
- **Leave-out check.**
  - `leaveout_BD.py` reproduces the draft's statement: all 16 y_b are positive, and every leave-two-out B_D is above
    thr.
  - But that tests the point estimate, and the flag is defined by the lower end.
  - With one batch left out and the jackknife redone:
    - 2143 keeps its flag 16 times in 16;
    - 2179 keeps it 4 times, and 3823 6 times.
  - 2143 also has 99% of batch pairs positive, a top-2 share of 0.20, and no half-sample below thr.
  - So the check is adequate for 2143: no one or two batches carry it. It does not make 2179 or 3823 independent
    refutations, and it cannot test between-seed variance.
- **Heavy tails.**
  - The §12.2 factor of about 2 was measured on N₁/μ₁, between samplers and run sizes.
  - For B_D the only between-seed evidence is four pairs: 1933 (a spike prime), 2347, 3877 and 4219.
    - They agree within 0.8 combined jackknife se. B_L agrees within 2.0.
    - At 1933, N₁/μ₁ is 2.66 against 2.63.
  - So there is no measured basis for inflating 2143's se by 1.7×.
  - The caveat does not act symmetrically on H1. At se × 2 no class-7 prime is sD, but 4 of the 9 class-1 test flags
    survive (1789, 2137, 2221, 2341). At × 1.5 it is 1 against 8.
  - Invoked after the fact, it would therefore rescue H. It cannot enter the scoring, which fixed the jackknife se.
  - It does bear on the weight. The refuting flag is moderate: B_D 1.28 is 2.9× the band median, like the weakest
    class-1 flags 2053 and 2137.
  - A second-seed run of 2143 is the direct check. It informs the reading, not the scoring.

**(5) H2, H3 and the rank tests.**
- Confirmed:
  - band 3: 15/16, medians 0.923 against 0.337, MW 0.0060 (exact within-band permutation 0.0056);
  - band 4: 13/16, 0.365 against 0.120, MW 0.0123 (0.0132);
  - H3: 1789, 2113 and 2341 (≡ 1), and 2143 (≡ 7);
  - pooled: 0.0002.
- **Test-set purity.** Four of the 70 had values known at 02:16, as 1933 did.
  - The H file says it was formed on "the earlier S-batched runs": 2347 and 4219 at seed 11, and 3877 (sb).
  - It also names 3889 under "Seen so far".
  - Without these four, 66 primes remain:
    - band 3: 15/15, MW 0.0064;
    - band 4: 11/15, 0.365 against 0.086, MW 0.0249;
    - pooled 0.0002.
  - The letter of the file (all 71 written after 02:16, 1933 included) gives the same.
- **Stratification.** The pooled test mixes bands at different levels. Permuting class within bands (van Elteren
  weights) gives 0.0001 on the 70 and 0.0002 on the 66, so it agrees.
- **Post hoc robustness.**
  - The shift is not an artefact of the noise subtraction. Unsubtracted √(X/W) gives 0.0001 on the 70, and so does
    B_D^cl. The noise level ν_D is, if anything, higher at class 7.
  - It survives adjusting log B_D for log N₁/μ₁ within bands (0.0011).
  - Adjusting for symR weakens it to 0.016. Part of the shift goes through symR, which is itself class-shifted.

**(6) Post hoc counts.** Confirmed:
- B_D > 2: 8 of 43 against 0 of 46, with P = C(43,8)/C(89,8) = 0.0021 (post hoc);
- the largest class-7 B_D is 1.28 (2143);
- the count-only spikes are 1531, 1627 and 1759, all ≡ 7.

The prospective part alone is weak. The 3 test primes with B_D > 2 (1789, 2113, 2269) are all ≡ 1, with
P = C(34,3)/C(70,3) = 0.11.

**(7) Fixes.**
1. **N₁/μ₁** (Part A; Part B item 4; Part C handoff). Replace "So the symR law predicts N₁/μ₁ to about 20% at all 74
   later primes" and the λ ≈ 0.5 sentence with:
   - "rms log error 0.18 over the 74 later primes: 0.24, 0.19 and 0.13 by band, 8 of 74 above 0.3, the largest 0.44
     at 1951";
   - "at λ ≤ 0.31 this is real prediction (band spreads 0.65 and 0.40)";
   - "the λ ≈ 0.5 primes confirm the level 3877 set (mean +0.05 ± 0.02) but reject the slope there: within the band it
     is 0.40 ± 0.07, and a constant does as well (rms 0.127)";
   - "the within-band slope falls with λ: 1.00, 0.86, 0.73 and 0.40 (post hoc)".

   The handoff's "rms log error 0.13–0.24 at all 74 later primes" needs the same qualifier. The class offset of the
   errors in (3) is optional (post hoc).
2. **H1** (Part A; Part B item 5; Part C).
   - Write "refuted by 2143", with its margin: its flag survives leaving out any one batch, and needs the jackknife se
     accurate to within 1.68×.
   - Call 2179 and 3823 threshold cases, not refutations: f_max 1.00 and 1.02, and they lose the flag with one batch
     left out in 12 and 10 of 16 cases. Drop them from the "refuted by" list.
   - Replace "All three B_D values stay above the threshold … every batch contributes positively" with a sentence that
     keeps B_D and the flag apart.
   - Add the heavy-tail reading of (4):
     - it cannot enter the scoring;
     - applied at 2× it leaves 4 class-1 flags and no class-7 flag, so it would act as a rescue;
     - the seed pairs give no basis for it;
     - a second-seed run of 2143 would show whether its moderate D excess replicates.
3. **Test sets.**
   - Add the 66-prime line, or adopt the 66 and give the reason.
   - Note that the file's own set includes 1933, and that all three sets give the same verdicts.
   - For the N₁/μ₁ scoring, drop 2347 and 4219 or say they were seen at seed 11. That leaves 72 blind primes, and
     nothing changes.
4. **Wording.**
   - "So the test confirms that B_D is shifted" → "H2 held as pre-registered (MW 0.006 and 0.012; stratified
     0.0001), so the data support a shift of B_D towards p ≡ 1 (mod 12)".
   - H2 registered only the medians, so label the MW values as added summaries.
   - In the gate (Part B item 6), "confirmed prospectively" → "held prospectively (H2)".
   - Optional: the shift survives without the noise subtraction and after adjusting for N₁/μ₁, and weakens to 0.016
     given symR (post hoc).
5. **PW_pair.** In Part B items 3 and 6 write "debiased PW_pair below 1 (28 of 29 by the CS upper estimate)".
6. **§12.7 leftovers that Part B item 5 misses.**
   - The sub-bullet "H was pre-registered … 16 primes at the snapshot … 0.010 … 0.057" is stale. Point it to §12.10,
     or mark it as the snapshot value.
   - Scope "The evidence is weak:" to the post hoc λ ≤ 0.25 evidence.
7. **Keep the replication.** Part B item 2 drops the "earlier: 2347" row. Keep one line in §12.10 on the four seed
   pairs (B_D within 0.8 se). They are the only between-seed check of the B_D se that (4) relies on.
8. **Small.**
   - "(1531–1753, less 1741 and 1759)" → "less 1741". 1759 is outside that range.
   - Label the in-sample residual sd: 0.20 with n in the denominator, or 0.22 with n − 3.
   - Next to "Three of the 8 are test primes", add "on their own P = 0.11".

# Author's disposition of round 4 (10 Nov, 05:25)

All eight fixes are accepted and applied in §12.10 and the in-place edits (§12.1–12.9), the handoff entry and STATE.
I re-derived the material numbers with my own scripts before recording them.

- **Checked independently.**
  - N₁/μ₁ scoring: rms 0.183 over the 74 later primes, 8 of them above 0.3 in log; 0.193 and 0.131 without 2347 and
    4219.
  - λ ≈ 0.5: free within-band slope 0.41 ± 0.07 (yours 0.40); a constant fitted in-band gives rms 0.121, and
    3877's value gives your 0.127. I write "rms 0.12–0.13".
  - Without 3877 the fit misses by 3.8× in (0.25, 0.31] and by 52× at λ ≈ 0.5, as you say ("about 4× and 50×").
  - Within-band slopes 1.00 ± 0.06, 0.86 ± 0.09, 0.73 ± 0.07, 0.40–0.41 ± 0.07.
  - H1 margins: with one batch left out and the jackknife redone, 2143 keeps sD 16 times in 16, 2179 4 times and 3823
    6 times. f_max 1.68, 1.002 and 1.015.
  - The strict 66-prime set: MW 0.0064 and 0.0249, medians 0.923 / 0.335 and 0.365 / 0.086.
- **Fix 1 (N₁/μ₁).** Adopted as worded. "About 20% at all 74 later primes" is withdrawn. The record says that the law
  predicts with real power at λ ≤ 0.31 and has none within the λ ≈ 0.5 band, where the level holds but the slope is
  rejected. The class offset of the errors is recorded as post hoc.
- **Fix 2 (H1).** Adopted. H1 is "refuted by 2143" with its two margins. 2179 and 3823 are called threshold cases.
  The leave-two-out sentence now says that it tests B_D, not the flag. The heavy-tail paragraph is recorded as you
  framed it: it cannot enter the scoring, at 2× it would rescue H, the seed pairs give no basis for it, and a
  second-seed run of 2143 informs the reading only. That run is listed as an optional mechanical item, not run now.
- **Fix 3 (sets).** The registered 70 stay primary. The strict 66 and the file's literal 71 are recorded as checks
  with the same verdicts. For N₁/μ₁ the record says 2347 and 4219 were seen at seed 11 and that dropping them changes
  nothing.
- **Fix 4 (wording).** Adopted: "H2 held as pre-registered"; the MW values are labelled as added summaries; the gate
  says "held prospectively (H2)"; the optional robustness lines are recorded as post hoc.
- **Fixes 5–8.** Adopted: "debiased PW_pair below 1 (28 of 29 by the CS upper estimate)"; the stale §12.7
  sub-bullet is marked as a snapshot value with a pointer to §12.10, and "The evidence is weak" is scoped to the post
  hoc λ ≤ 0.25 evidence; the seed-pair line is kept in §12.10; "less 1741"; the residual sd labelled (n: 0.20,
  n − 3: 0.22); "on their own P = 0.11".
- **One consequence I add.** §12.6 compared 36037 with "the κ = 6 maximum in the 0.25–0.31 band so far, 0.53". The
  complete band has median B_L 0.45 (0.33 at λ ≈ 0.5, a rise of 1.4×) and maximum 1.16 at the spike 2113. That
  sentence is updated with these referee-confirmed numbers. It does not change the 36037 reading, which waits for
  35099.

# Round 4b (referee, 10 Nov 05:45)

**Verdict: OK to record (1) with the wording fixes below; (2) and (3) as written.**
- Script and output: `scratch/r4b_checks.py` and `.out` (4 CPU-s).
- My own Gram-matrix path and `k6_spike_survey.analyse` agree to 10⁻¹⁴ on all four κ = 7 files.

**(1) 35099.**
- **Numbers.** Every number reproduces. The floor is 0.901 with my c_B seed, against 0.903.
- **"Spike" is justified, for B_L, at the Monte Carlo level.**
  - The test stated in advance in §12.9 is passed by a wide margin. 35099's 2σ upper end (0.264) is less than half of
    36037's 2σ lower end (0.535).
  - The half-samples do not overlap. 36037's smallest (0.506) is 1.66× 35099's largest (0.304).
  - The κ = 6 calibration is what carries the single comparison. Within a band, no two unflagged κ = 6 primes differ
    by 2.68× in B_L: 0 of 1294 ordered pairs. Only 9 differ by 2.0×, the 2σ ratio.
  - Against the band median, κ = 6 reaches 2.7× only at 1657 (3.7×) and 1789 (3.2×). 2113 is at 2.6×.
  - Say "spike in B_L". 36037 is neither sD (its B_D lower end is 0) nor sN, and B_L is not a κ = 6 flag variable.
- **Fixes.**
  1. **Selection.** 35099 is not the median-symR prime. It is 10th of the 13 λ ≈ 0.3 primes with symR (median 16.3).
     It is the middle of the six in the §12.6 table.
     - Write: "picked as the middle symR of the §12.6 table (21.3; 10th of 13), with its F, 0.5 (the lowest), known".
     - The two selection effects pull in opposite directions. The above-median symR would raise 35099's B_L at κ = 6
       rates; the low F might lower it.
     - The other typical primes (0.22 and 0.27 at λ 0.4 and 0.5) suggest neither effect is large.
  2. **Bins.**
     - Give the 2σ ratios (36037's lower end over 35099's upper end): (2,2) 2.3× (≥ 1.9×), (0,3) 5.7× (≥ 3.4×),
       (2,3) 13× (≥ 6.0×), (3,3) 12× (≥ 5.6×). 35099's z there are 13.1, 2.8, 1.9 and 2.9.
     - Add (0,4) and (2,4). They are resolved at 36037 (z 3.8 and 2.6) and are noise at 35099 (≥ 2.9× and ≥ 4.2×).
     - (2,2) and (0,3) carry 81% of the rise in B_L². (2,3) and (3,3) are 8% and 3% of 36037's B_L².
  3. **Half-sample sentence.** "Above 35099's largest half-sample value, 0.30" (rather than its 95% point).
  4. **"Does not rise (0.27, 0.22, 0.24)".** Add "one prime per λ".
  5. **F.** 35099's F of 0.5 rests on 5 configurations, so its Poisson 95% range is about 0.16–1.2. Say so beside
     "F 2.3 against 0.5".
- **Gates.** They are fine. Make the counterexample read "in B_L, against one equal-λ prime". "The lift is a 2+2
  effect" stays false until the 2+2 split of the 36037 run is done.

**(2) 2143 at seed 14.**
- **Numbers.** All reproduce.
  - The seed-14 run is S-batched (batches of 522–828 configurations), and its S1 arrays differ from seed 13.
  - The seed differences are 0.03 combined se on B_D, 0.47 on B_L and 0.84 on N₁/μ₁.
- **All three flags replicate** against the seed-13 band medians.
  - sD: lower end 1.093 against 0.887, with f_max 1.89.
  - sPW: 2.418 against 2.082.
  - sN: 1.993 against 1.616.
- **The X-scale reading is right.**
  - The estimator sets z = s/se_jk, where s = X − noise and se_jk is the batch jackknife of X.
  - W and the unit are the same at both seeds, so B² ∝ s and se_s = s/z.
  - Computing directly in s, on the B scale by the delta method, or from B² and z all give −0.03 (D) and 0.47 (L).
  - Write "noise-subtracted X". The noise is 2.4% of X for D and negligible for L.
- **The proposed record is fair.** Optionally add that the seed difference matches the four round-4 seed pairs, so
  the jackknife se is borne out at 2143 too.

**(3) Flags.** Confirmed.
- In `r4_checks.py`, sPW and sN use the point value (above twice the band median) and sD uses the 2σ lower end.
- That is the rule of `k6_spike_survey.py` line 176, `score_predictions.py` and the H file ("(H3) sN spikes (N1/mu1
  above twice the band median)").
- The new §12.1 wording matches.

# Author's disposition of round 4b (10 Nov, 05:50)

- **Checked independently.**
  - The 13 κ = 7 primes with λ 0.29–0.31 in `sym/sym_rate_k7_lam03.out` have median symR 16.26. 35099 (21.33) is
    10th from the bottom. My "median symR" was wrong; it is the middle of the six in the §12.6 table.
  - In-band ordered pairs of unflagged κ = 6 primes: 0 of 1294 at ≥ 2.68×, 9 at ≥ 2.0×. That is as you say.
  - The bin 2σ ratios: I re-derived (2,2) from the pw_bin_cs z values (3.390 / 1.792 = 1.89). The 81% rise share
    is reproduced from the bin shares.
  - Poisson 95% range for 5 events: 1.62–11.67, so F(35099) is 0.16–1.2.
- **(2) and (3)** are adopted as written, with "noise-subtracted X" and your optional seed-pair sentence.
- **(1): fixes 1–5 and the gates are adopted.**
- **One part of the calibration I do not adopt.** "0 of 1294 at ≥ 2.68×" is true, but it sits on a knife edge. In
  (0.25, 0.31] the unflagged maximum over minimum is 2.67, from an equal-λ pair: 2281 (λ 0.293, B_L 0.663) over 2293
  (λ 0.295, B_L 0.248). Your output prints that 2.67. So at κ = 6, two primes with no flag at equal λ differ by as much
  as 36037 and 35099. A ratio to one comparison prime does not separate a spike from the two ends of a wide typical
  spread.
- **The better reference is the band median.**
  - Unflagged κ = 6 primes reach at most 1.08, 1.22, 1.46 and 1.54× their band median, from the lowest band to
    λ ≈ 0.5. Their minimum is 0.55–0.83×.
  - Flagged spikes reach 3.74, 3.25, 2.56 and 1.94×, as you say.
  - 36037 is 2.62× the mean of the three typical κ = 7 primes. That is one prime per λ (0.24, 0.22, 0.27 at λ 0.3, 0.4
    and 0.5). So 36037 is a spike if those three sit near the κ = 7 median at λ ≈ 0.3. If 35099 sat at the bottom of
    a κ = 6-like spread (0.55× the median), the median would be about 0.43, and 36037 would be 1.47× it, at the top of
    the unflagged range.
- **So the record says** "a spike in B_L by the §12.9 test, against the three typical κ = 7 primes measured", with
  this caveat stated.
- **The deciding run has started** (05:48), with a pre-registered rule in `osc-mc/predictions_k7_p34847.txt`. The
  prime is 34847, the median symR of the 13 (16.26), with F and class values unknown. It runs 6000 configurations at
  seed 13, about 1 h.
  - Spike if B_L(34847) ≤ 0.41 and its 2σ upper end is below 0.535.
  - Not shown to be a spike if B_L(34847) ≥ 0.43.
  - Inconclusive between.

# Round 4c (referee, 10 Nov 05:53)

**Verdict: (a) confirmed; (b) fair, with one added clause; (c) sensible and conservative, with a reporting
addendum.**
- Script and output: `scratch/r4c_checks.py` and `.out` (3 CPU-s).
- You are right about the knife edge. My "0 of 1294 at ≥ 2.68×" rests on a maximum of 2.67 (2281 against 2293, both
  unflagged, λ 0.293 and 0.295). At the 2σ ratio, 2.02, 9 unflagged pairs already exceed it. The band median is the
  better reference.

**(a) Confirmed.**
- Unflagged B_L / band median: at most 1.08 (1549), 1.22 (1801), 1.46 (2281) and 1.54 (4153), and at least 0.63, 0.57,
  0.55 and 0.83.
- Flagged maxima: 3.74 (1657), 3.25 (1789), 2.56 (2113) and 1.94 (3889).
- 36037 is 2.62× the three-prime mean and 2.68× 35099. Both are above every flagged maximum except bands 1 and 2.
- Flagged primes go as low as 0.90× (2053). The flags are not a B_L criterion, so compare with the unflagged maxima, as
  you do.

**(b) Fair, as a worst case.** Add how extreme it is.
- 36037 falls to 1.54× the median only if 35099 is below 0.58× it. Only 2 of the 68 unflagged κ = 6 primes are (2293
  and 1741).
- The 5, 10 and 25% points of the unflagged ratios are 0.65, 0.68 and 0.85. With 35099 there, 36037 would be 1.74×,
  1.83× and 2.27× the median.
- Suggested clause: "this needs 35099 below 0.58× the κ = 7 median; at κ = 6, 2 of 68 unflagged primes are".
- Precise value: 0.237/0.546 = 0.434, so 1.46×. Your 1.47× is fine.

**(c) The rule is sensible.**
- The file was written at 05:48:01. The run started at 05:48:08 (process start time).
- The prime was chosen by a rule (median symR of the 13), with F and class values unknown.
- The thresholds follow from the calibration. Using 1.54 rather than band 3's 1.46 (0.435) is the conservative
  choice.
- It is conservative in both directions, because it ignores 35099. With the two equal-λ primes averaged, 36037 would
  be 1.96× at 0.41 and 1.90× at 0.43.
- **Point values against a narrow gap.**
  - At 6000 configurations (35099: z 8.2), se(B_L)/B_L is about 6%. So the 2σ half-width near 0.41 is about 0.05,
    against an inconclusive band 0.02 wide.
  - The second condition is automatic: at 0.41 the 2σ upper end is 0.457 < 0.535.
  - The ratio 36037/34847 carries about ±19% at 2σ: 1.25–1.84 at 0.41, and 1.20–1.76 at 0.43.
  - So any result in about 0.36–0.48 is decided by Monte Carlo noise.
- **Suggested timestamped addendum, before the result.** It leaves the calls unchanged.
  - Report B_L(34847) and the ratio with their 2σ ranges.
  - Mark the call as close if the 2σ range of B_L(34847) crosses 0.41 or 0.43.
  - A stricter alternative, also before the result: decide on the 2σ ends. Spike if the upper end is ≤ 0.41; not
    shown if the lower end is ≥ 0.43.

# Author's disposition of round 4c (10 Nov, 05:55)

- **Checked independently.** 2 of the 68 unflagged κ = 6 primes sit below 0.575× their band median: 1741 (0.566)
  and 2293 (0.546). At the 5%, 10% and 25% points of the unflagged ratios, 36037 would be 1.74×, 1.83× and 2.27× the
  implied κ = 7 median.
- **(b) is adopted.** The §12.6 caveat now says how extreme the worst case is: it needs 35099 below 0.58× the κ = 7
  median, and at κ = 6 that holds for 2 of 68 unflagged primes. The percentile values are given too.
- **(c) is adopted as the reporting addendum.** It was appended to `predictions_k7_p34847.txt` at 05:52:33, with the
  run at 418 of 6000 configurations and the result unknown. The calls are unchanged, so I keep the point-value rule
  as registered rather than switch to the 2σ-end option.

# Round 4d (referee, 10 Nov 07:23): the 2+2 / not-2+2 split of the κ = 7 run at 36037

**Verdict: ACCEPT WITH CHANGES.** Claims 1–4 reproduce by my own path. In claim 5 the refutation stands, but "the B_L
lift there is a not-2+2 effect" overstates. Three F sentences in §12.5–12.6 and one gate need updating.
- Scripts and outputs: `scratch/r4d_checks.py` and `.out` (own Gram-matrix path; nothing imported from
  `split36037_decomp.py`), and `scratch/r4d_k6_align.py` and `.out` (sign of the 2+2/rest cross term in every split on
  file). About 2 CPU-s at nice 19.
- My numbers agree with `split36037_decomp.out` in every printed digit.

**Files.**
- The three parts add up: S1 to 2·10⁻¹¹ relative, cnt exactly. They share P, orb, supp and rb with the full run.
- The split's 'all' part is a prefix of the full run: 947,379 of its 1,570,353 S, and at most the full run's count in
  every batch.
- Each of the 16 batches holds 4–21 of the 185 2+2 configurations.

**Claim 1: confirmed.**
- Share 0.0308, S-batch jackknife se 0.0027. A bucket lies in one S-batch, so this se already includes the clustering
  that inflates pairsym's error.
- F = 0.0308 × 1.074 / 0.0204 = 1.63 ± 0.14 (share error only). With the full-run N₁/μ₁ of 1.080 it is also 1.63.
- pairsym's 28/624 = 0.045 is 1.7 binomial se above 0.031, and less once its b = 8 clustering is counted. So the two
  agree, and the split supersedes pairsym.

**Claim 2: confirmed.**
- The rest on its own scale gives 0.573 (z 6.6, 2σ 0.478–0.654), against 0.237 (0.206–0.264) at 35099. That is 2.41×,
  or 1.81× at the 2σ ends.
- It is robust:
  - y_b > 0 in 16 of 16 batches, and the top two batches make 19% of the sum;
  - worst leave-two-out 0.524;
  - half-samples min 0.454 (5/50/95%: 0.502, 0.569, 0.645), above 35099's largest half-sample, 0.304.
- On the contribution scale it is 0.555 (z 6.7, 0.464–0.632): 2.34×, or 1.76× at the ends.
- The rest keeps 82–87% of 36037's B_L excess over 35099 (76–82% in B²).

**Claim 3: confirmed, but give the errors.**
- The identity holds to 2·10⁻¹⁶.
- Shares of X_L, with jackknife se:

  | part | share of X_L |
  |---|---|
  | 2+2 alone | 1.5 ± 0.7% |
  | rest alone | 79.3 ± 5.1% |
  | cross | 19.2 ± 4.4% |
  | 2+2 total (alone + cross) | 21 ± 5% |

- The parts are in phase: cos = cross/(2√(X_str X_uns)) = 0.89.
- In amplitude, removing the 2+2 configurations takes B_L from 0.623 to 0.555, so they add 0.068.
- "Exactly" applies to the identity, not to the shares.

**Claim 4: confirmed.**
- Rest against 35099's whole run, central then at the 2σ ends: (2,2) 2.10× (≥ 1.72×), (0,3) 5.11× (≥ 3.12×), (2,3)
  10.7× (≥ 4.64×), (3,3) 10.0× (≥ 3.81×).
- (0,4) and (2,4) are noise at 35099 but resolved in the rest: ≥ 2.70× and ≥ 1.99× at the ends (rest z 3.6 and 2.2).
- In these six bins the rest alone makes 57–85% of the bin's X(all), the cross term 15–37%, and the 2+2 part alone
  1–6%.
- (0,5), (0,6) and (0,7) are unresolved in both runs.

**Claim 5: the first half stands, the second overstates.**
- The refutation holds as tested. The hypothesis predicted that without the 2+2 configurations B_L would drop to about
  35099's level. It stays 2.4× above, and ≥ 1.8× at the 2σ ends.
- "A not-2+2 effect" goes too far, for two reasons.
  1. "Not 2+2" is mc_split's flag: no Möbius involution swapping two pairs of S has ≥ 2 ι-pairs in T. The rest can
     still hold other structure, such as one ι-pair, involutions of other cycle types or order-3 symmetry. None of
     that has been examined, so the split shows what the lift is not, not what it is.
  2. The 2+2 configurations are not inert. They are in phase with the rest (cos 0.89) and make 21 ± 5% of X_L. On
     their own scale they are 3.8× the rest (2.16 against 0.573), but only at z 2.0.
- **Alignment in every split on file** (`r4d_k6_align.out`). This covers 16 κ = 6 runs at 15 primes with λ ≤ 0.25
  (1933 twice), plus 36037.
  - In L, the cos between the 2+2 part and the rest is +0.68 (1621) to +0.99, and ≥ 0.88 in 16 of 17.
  - The 2+2 part's own-scale amplitude is 1.1–2.0× the rest's at κ = 6, and 3.8× at 36037.
  - So in L the 2+2 part carries nearly the rest's profile, amplified. This describes 17 runs; it is not a mechanism.
  - In D the cos is −0.01 to +0.99.
- **D.** B_D is unresolved in every part (z 1.2–1.4). The 2+2 configurations make 54% of X_D (alone 0.11 ± 0.06, cross
  0.43 ± 0.05). Do not extend the conclusion to D.

**Your four questions.**
1. **Own scale against 35099's whole is the right comparison.**
   - It is B_L as if the 2+2 configurations had not been sampled, which is what the hypothesis makes a prediction
     about.
   - The strict like-for-like quantity is 35099's rest. By Minkowski that is ≤ (B_all + s·B_str,own)/(1 − s), so at
     s ≈ 1% it differs from 35099's whole only through s·B_str,own (question 2).
   - The contribution scale gives the same answer (≥ 1.76×), so the choice of scale does not matter.
2. **35099's unsplit 2+2 part cannot plausibly close the gap.**
   - Suppose 35099's rest reaches 0.478 (36037's 2σ low end) with B_all(35099) at its 2σ high end, 0.264. Then 35099's
     2+2 part needs an own-scale B_L of at least:
     - 18.9 at pairsym's s = 0.011;
     - 27.6 at s = 0.0076 (pairsym scaled by 36037's split/pairsym ratio);
     - 7.7 at s = 0.026 (the top of 35099's F range).
   - 36037's own-scale value is 2.16 (2σ upper 3.07).
   - The 2+2 part would also have to be anti-aligned: closing the gap forces cos < 0. Every split on file has cos
     between +0.68 and +0.99.
   - Even the weaker target 0.372 (36037's rest / 1.54, the κ = 6 unflagged maximum) needs ≥ 9.4 at s = 0.011 and
     ≥ 3.8 at s = 0.026, still anti-aligned.
   - A split of 35099 would settle it but is not needed for this claim.
3. **The 6000-configuration prefix is enough for the rest, not for the 2+2 part alone.**
   - For the rest: z 6.6, the robustness above, and split-all 0.623 against the full run's 0.635, each within the
     other's 2σ range.
   - For the 2+2 part alone it is not enough: 185 configurations, z 2.0. Give no κ = 7 class value for the 2+2 part
     beyond "unresolved, < 3.1 in B_L".
4. **Wording.** Changes below.

**Exact wording changes.**
- (a) Claim 3: "With c_q,b = S1_q,b/cnt_all,b, X_L(all) splits exactly into 2+2 alone 1.5 ± 0.7%, rest alone 79 ± 5%
  and cross 19 ± 4% (jackknife), so the 2+2 configurations account for 21 ± 5%. The two parts are in phase (cos 0.89).
  In amplitude, removing the 2+2 configurations lowers B_L from 0.62 to 0.56."
- (b) Claim 4: "In every lifted L bin the rest alone is lifted against 35099's whole run: (2,2) 2.1×, (0,3) 5.1×,
  (2,3) 10.7×, (3,3) 10.0×, and 1.7×, 3.1×, 4.6×, 3.8× from the 2σ ends. (0,4) and (2,4) are noise at 35099 but
  resolved in the rest (≥ 2.7× and ≥ 2.0×). In these bins the rest alone makes 57–85% of the bin's X and the cross term
  15–37%."
- (c) Claim 5. Replace "the B_L lift there is a not-2+2 effect" with: "Hence 'the lift is a 2+2 effect' is refuted for
  B_L at 36037, against 35099. Without the 2+2 configurations B_L is 0.57 (2.4× 35099, ≥ 1.8× at the 2σ ends). The 2+2
  configurations (3.1%) add about 0.07, in phase with the rest. 'Not 2+2' means mc_split's flag, and other structure
  in the rest is unexamined. B_D is not covered: it stays unresolved, and about half its X involves the 2+2
  configurations."
- (d) §12.5, κ = 7 F list (note line 994). Use: "F is 1.8 at 35281, 0.5 at 35099, 1.6 at 36037 and 0.9 at 34693. The
  36037 value comes from the split: 185 structured configurations among 6000, S-batch se 0.14. The others are
  pairsym's, from 19, 5 and 9 structured configurations. pairsym gave 2.3 at 36037 from 28." Keep the clustering bullet
  for the pairsym values.
- (e) §12.6 (line 1115). Replace "Its F, 2.3, is the highest at κ = 7" with: "Its F is 1.6 (split). pairsym's 2.3,
  from 28 clustered configurations, was 1.5× too high. 35281's pairsym 1.8 is within that error, so the κ = 7 ranking by
  F is not resolved."
- (f) §12.6 (line 1165). Replace the "F 2.3 against 0.5 … fits the κ = 6 pattern" bullet with: "F is 1.6 against 0.5
  (0.16–1.2). The split shows that the B_L lift does not come from the 2+2 configurations, so a large F does not explain
  it here."
- (g) §12.8 gates (line 1308). Replace "the lift as a 2+2 effect, until the 2+2 split of the 36037 run is done" with:
  "the B_L lift at 36037 explained. The split refutes it as a 2+2 effect (a 6000-configuration prefix, against 35099),
  but other structure in the rest is unexamined."
- (h) §12.9 (line 1330). Mark the split done, with the 3.1% share (the 4.5% was pairsym's). It does not carry the (2,2)
  and (0,3) lift: the rest alone makes 85% and 75% of those bins' X.

# Round 4e (referee, 10 Nov 07:30): scoring of the κ = 7 run at 34847

**Verdict: ACCEPT WITH CHANGES.** The rule was applied exactly as written, and claims 1–5 reproduce. Claim 6 needs
three fixes:
- it calls two primes "typical";
- it sets a two-prime mean against κ = 6 ratios taken to all-prime band medians;
- it should say what the shared seed does and does not do.

The call itself (spike in B_L, not close) does not depend on any of this.
- Script and output: `scratch/r4e_checks.py` and `.out`. It uses my own Gram-matrix path for 34847, 35099 and 36037,
  and checks the result against `ks.analyse`. About 4 CPU-s at nice 19.

**The rule as written.**
- **Timing.** The rule was written at 05:48:01 and the run started at 05:48:08 (round 4c). The addendum was written at
  05:52:33, and the file's mtime is still 05:52:33. The npz and the log were written at 07:21:13.
  `score_k7_34847.py` was last modified at 05:56:16, before the result, so the scorer was fixed in advance too.
- **The run matches the specification:** κ = 7, p = 34847, 6000 configurations, seed 13, 1,378,329 S. Batches are by S
  (counts 299–519 per batch, so the pre-fix guard in `analyse` passes).
- **The decision logic matches the text:**
  - spike if B_L ≤ 0.41 and the 2σ upper end is < 0.535;
  - not shown if B_L ≥ 0.43, inconclusive otherwise;
  - close if the 2σ range contains 0.41 or 0.43.
  The 2σ ends are `analyse`'s (s ± 2 se on the noise-subtracted X scale). That is the convention behind the rule's 0.535
  for 36037.
- **One procedural difference, not material.** The rule names `k7_class_values.py` as the reader, and the scorer calls
  `ks.analyse` directly. `k7_class_values.py` is itself a wrapper around `ks.analyse`, so the estimator is the same.
- **No deviation from `ks.analyse`.** The scorer adds only the ratio and the call. My own path reproduces `analyse` to 4
  decimals at all three primes (B_L, z, both ends, B_D).

**Claims 1–5: confirmed.**
1. B_L(34847) is 0.2452 (z 9.44, 2σ 0.2177–0.2699).
   - The call is SPIKE. It is not close, and the prediction of 0.20–0.32 held.
   - The realised 2σ half-width is 0.026, half the addendum's estimate of 0.05. My round-4c estimate was rough, and the
     difference only makes the call less close.
2. The ratio is 2.588. Its 2σ range is 2.12–3.05 by the delta method and 1.98–3.31 from the ends.
3. **Stability of 34847.**
   - y_b > 0 in 16 of 16 batches; the top two make 17%.
   - Leave-one-out 0.237–0.250; worst leave-two-out 0.233.
   - Half-samples 0.178–0.297.
   - 36037's smallest half-sample, 0.506, is 1.70× 34847's largest (1.66× 35099's).
4. **The bins are as claimed:** (2,2) 2.0× (≥ 1.6×), (0,3) 9.6× (≥ 4.2×), (2,3) 15.7× (≥ 6.0×), (3,3) 11.2× (≥ 4.2×).
   - Add that (0,4) and (2,4), which are noise at 34847, put 36037 at ≥ 2.5× and ≥ 3.8× 34847's 2σ upper ends.
5. **The 34847 values are as claimed:**
   - B_L 1.034× 35099;
   - (2,2) 1.93 against 1.67;
   - B_D 0 (z −0.7, < 2.33);
   - N₁/μ₁ 0.934 ± 0.037;
   - PW_pair 0.955 against its floor 0.930 (CS 0.200).

   For balance, add that (0,3) is unresolved at 34847: 0.39 (z 0.9), against 0.65 (z 2.8) at 35099.

**Claim 6.**
- **The shared seed** (`r4e_checks.out` §3).
  - mc_classes draws S with `rng.choice(p, k)` from `default_rng(13)` and makes no other random calls. So the three runs
    draw the same S positions scaled to p: the first three S have s/p equal to within 10⁻⁴ at 34847, 35099 and 36037.
  - That does not correlate the class values. Buckets depend on k-th-power residues of differences mod p, and scaling
    does not preserve those.
  - The data agree:

    | pair | batch y_b corr. | cell-level ρ | shift null sd | batch-count corr. |
    |---|---|---|---|---|
    | 34847–35099 | 0.03 | −0.017 | 0.029 | 0.43 |
    | 34847–36037 | 0.05 | 0.023 | 0.035 | 0.04 |
    | 35099–36037 | −0.06 | −0.048 | 0.025 | 0.04 |

    The null sd for a correlation of 16 batches is 0.26, so none of these is significant. The cell-level ρ is the
    correlation of batch deviations over L cells, and every value lies inside its cyclic-shift null (max |ρ|
    0.050–0.065).
  - So the 3% agreement is not a seed artifact. Record that the κ = 7 runs share their S stream. Use distinct seeds for
    future comparison primes, as hygiene.
- **The agreement itself is weak evidence.** At κ = 6, 65 of 647 unflagged same-band pairs (10%) agree to within
  1.034×. The informative fact is that both primes are low, not that they agree.
- **How far two primes answer the worry, under the κ = 6 spread as a model.**
  - For 36037 to sit at the unflagged maximum, 1.54× the band median, that median must be ≥ 0.412. Then 35099 and 34847
    sit at 0.575 and 0.594 of it.
  - At κ = 6, 2.9% of the 68 unflagged primes sit that low. So two independent primes both do so with probability
    about 0.1%.
  - With 36037 at its 2σ lower end, the probability is 1.2%. Against band 3's maximum of 1.46×, it is 0% centrally and
    0.35% from the 2σ lower end.
  - This assumes the κ = 6 spread carries over and that picking by symR does not bias B_L.
- **The reference mismatch.**
  - The κ = 6 ratios (≤ 1.54× for unflagged primes, 1.94–3.74× for spikes) are to all-prime band medians.
  - Both κ = 7 comparison primes look unflagged (B_D ≈ 0, PW_pair at its floor, N₁/μ₁ < 1). At κ = 6 the unflagged
    median is 3–16% below the all-prime median, and 10% below in (0.25, 0.31].
  - So on the κ = 6 footing 36037 is about 2.4× the implied band median, not 2.6×. That is still far above the 1.46×
    unflagged maximum in that band, and close to its largest spike (2.56×).
- **"Typical" overstates.** Two primes give a mean, not a typical value.

**Exact wording for claim 6.**
> "So the round-4c worry is answered as far as two primes can answer it. The worry was that 35099 might sit at the
> bottom of a κ = 6-like spread. 34847 was picked at the median symR, with its F and class values unknown. Its B_L,
> 0.245, is 1.03× 35099's. All three κ = 7 runs use seed 13 and so share their S positions, but their class values are
> uncorrelated at batch and cell level, so this is not a seed artifact.
>
> If 36037 were at most the κ = 6 unflagged maximum (1.54× the band median), both comparison primes would have to lie
> below 0.6× the κ = 7 median. At κ = 6, 2.9% of unflagged primes do, so for two independent primes the chance is about
> 0.1%, or 1.2% with 36037 at its 2σ lower end.
>
> The two primes average 0.241, and 36037 is 2.6× that. Both look unflagged, and at κ = 6 the unflagged median is
> about 10% below the all-prime median in (0.25, 0.31]. So 36037 is about 2.4× the implied band median, against at most
> 1.46× for unflagged κ = 6 primes in that band and 2.56× for its largest spike."

**Gates.** Keep the three you list, and widen the first.
- Use "the κ = 7 spread at λ ≈ 0.3, and so the transfer of the κ = 6 calibration to κ = 7 (two primes are not a
  distribution)".
- Optional, for §12.6:
  - Against the two comparison primes, 36037's PW_pair (2.71, against 0.93–0.96) would raise sPW by the κ = 6 rule.
  - PW_pair reads the same class values as B_L, so this is not independent evidence. It does mean that "neither sD nor
    sN" should not be read as "unflagged".

# Author's disposition of rounds 4d and 4e (10 Nov 07:36)

**Round 4d: all accepted, applied in §12.5, §12.6, §12.8 and §12.9 and in the handoff and STATE.**
- (a)–(c) The split's shares, alignment, bins and the refutation are recorded in the referee's wording. "A not-2+2
  effect" is gone: the note says what the split refutes, that "not 2+2" is mc_split's flag, and that B_D is not
  covered.
- (d)–(f) 36037's F is 1.6 from the split in the §12.5 list and in §12.6. The "highest F at κ = 7" ranking and the
  "large F fits the κ = 6 pattern" bullet are replaced as worded.
- (g)–(h) The gate reads "the B_L lift at 36037 explained", and §12.9 marks the split done with the 3.1% share.
- Added from your answers: 35099's unsplit 2+2 part cannot plausibly close the gap (it would need an own-scale
  B_L ≥ 19, pointing against the rest; every split on file points with it), and the 2+2 part alone stays unresolved.
- Verified myself before recording: the decomposition identity, the share and F (my `split36037_decomp.out`
  matches yours digit for digit), and cos ≈ 0.88–0.89 from the printed shares.

**Round 4e: all accepted, applied in §0, §12.6, §12.8 and §12.9 and in the handoff and STATE.**
- The call (spike in B_L against two equal-λ primes, not close; prediction held) is recorded as scored.
- Claim 6 is replaced by your wording, with the seed note, the 10% agreement rate, the 0.1% (1.2%) two-prime
  probability and its assumptions, and the like-for-like 2.4× against 1.46×. "Typical" is dropped for the two
  comparison primes.
- Verified myself: the band-3 medians (0.454 all-prime, 0.413 unflagged, ratio 1.099, from `k6_spike_survey.out`
  with the §12.2 flags), and 36037 at 2.63× the two-prime mean and 2.39× the implied band median.
- The gate is widened to "the κ = 7 spread at λ ≈ 0.3, and so the transfer of the κ = 6 calibration to κ = 7".
- The (0,3) caveat at 34847, the (0,4)/(2,4) end ratios, and the sPW note are added to §12.6.
- Future comparison primes get distinct seeds. The proposed 34693 run (mechanical plan item 5) uses seed 17.

# Round 4f (referee, 10 Nov 10:56): scoring of mechanical item 2 (F over the κ = 6 survey, λ ≤ 0.25)

**Verdict: ACCEPT WITH CHANGES.** Every prediction is scored as written, with the right scope, and every number
reproduces. But three of the six "kept" calls were fixed before the runs by the survey N₁/μ₁, which was already known.
The record must say so:
- **F2** could not fail;
- **F3 and F5** are near-automatic;
- **F7**'s three directions already held with F at share 0.8.

The informative results are F1 (refuted), F4, F6, and the λ and class dependence of the share.
- Script and output: `scratch/r4f_checks.py` and `.out`. It is my own code for the shares, N₁/μ₁, F, the arithmetic
  (pow-based, no primitive root) and the ranks, and imports nothing from `score_F.py`. About 15 CPU-s at nice 19.

**1. Scoring as written.**
- **Timing.** The predictions were written at 05:59:59 and the erratum at 06:04:42. `score_F.py` was last modified at
  06:03:48, and the first split13 log at 06:05:59. So the scorer has not changed since before any result, and the
  07:37 partial run could not have altered it.
- **Scopes.** F1–F6 are scored over the 25 new primes and F7 over the 29, as written. The 29-prime figures for F1–F5
  are reported alongside, as the file promises.
  - F2 "above 4.0" is scored as max ≤ 4.0.
  - F4's threshold of 0.34 is the one-sided 5% point for n = 25.
  - The sD set {1669, 1693, 1933} matches the file.
  - F6 uses `ks.analyse` on the _str/_uns npz. That is exactly what `split_report.py` does.
- **"Reproduces the survey run" holds more strictly than the scorer checks.** The scorer compares log lines. I compared
  the arrays (nS, cnt, S1, S2, N1) of each _all npz with `survey/mc_k6_p*_s13.npz`: all 29 match. The parts add up at
  all 29.
- **Numbers.**
  - Shares, N₁/μ₁ and F agree with `score_F.out` to the printed digits (share to 0.001).
  - F4 is 0.521 with average ranks. The scorer's 0.511 comes from 3-decimal log shares with ties (0.614 twice) and ranks
    without tie averaging. Over the 29 the values are 0.616 and 0.609. Not material.
  - F1: range 0.496–0.792, and the same six primes below 0.60.
- **Arithmetic columns** (own code): h from p mod 12, 2 a cube from 2^((p−1)/3) = 1, a by direct search, and t from
  χ₆(x) = x^((p−1)/6). There are 0 mismatches in h and in the cube class, and |a|/√p and t agree to 0.000. The
  representation p = a² + 3b² with a ≡ 1 (mod 3) is unique at all 29. A(0, h) is generator-free for h ∈ {0, 3}, so the
  primitive root plays no role.

**2. What the data known in advance already fixed** (survey N₁/μ₁ at all 29).
- **F2 could not fail.** Even at share 1, the largest F any new prime can reach is 3.79 (1933), below 4.0. Record it as
  "automatically kept".
- **F3 is near-automatic.**
  - At any constant share, Spearman(F, N₁/μ₁) = Spearman(N p², N) = 0.969.
  - With the 25 shares permuted at random, so that share and N₁/μ₁ are unlinked, F3's 0.90 is met in 99.9% of
    permutations (median 0.950, minimum 0.875).
  - The reason: over the 25, var log N₁/μ₁ = 0.373, against 0.014 for log share and 0.018 for log p².
- **F5 is automatic too.** Under the same permutations it is met in 100% of them (median 0.909, minimum 0.789).
- **The content of F4 and F5 is better given as elasticities** against N₁/μ₁ over the 25 (bootstrap 95%):
  - 2+2 count, share·N₁/μ₁: 1.10 (1.04–1.17);
  - rest count, (1 − share)·N₁/μ₁: 0.79 (0.64–0.91);
  - share: 0.10 (0.04–0.17).

  So both parts grow with the excess, the 2+2 part slightly faster. The share moves by only about ±12% (sd of log
  share 0.12).
- **F7 was fixed in advance.** With F at share 0.8, which was known before the runs, all three directions already held:
  - Spearman with |a|/√p 0.475;
  - h = 0 medians 3.04 (2 a cube) against 0.82;
  - Spearman with |t| 0.746.

  The results after the runs (0.494; 2.80 against 0.72; 0.789) are N₁/μ₁'s own correlations: N₁/μ₁ alone gives
  0.507 and 0.718. Likewise Spearman(F, symR), 0.921, equals Spearman(N₁/μ₁, symR), 0.921.

**3. What F3 and F5 mean.** F3 says F inherits N₁/μ₁'s ranking. That is a property of the definition, not a finding.
F5 says that the rest's count rises with the excess (elasticity 0.79), which is the substantive part of "the rest is
lifted too". Neither shows F to be a factor separate from N₁/μ₁.

**4. Wording.**
- F6 is a point-value comparison, as written. The 2+2 B_D is 2.0–3.0× the rest's, with z 7.7–10.4 against 2.1–10.7.
  1933 is not fully independent of what was seen: its new run contains the earlier split's first 5022 configurations
  (erratum).
- **The exploratory share-by-class result** (post hoc).
  - It survives a check for confounding by λ. The share falls with λ (Spearman −0.40), but the classes are balanced
    across bands (h = 0: 7 and 8; h = 3: 7 and 7).
  - The class difference appears in both bands: permutation MW p 0.054 below λ 0.22, and < 0.001 from 0.22 to 0.25. With
    a linear λ trend removed, p is < 0.001.
  - It is still post hoc. Pre-register it on new primes before stating it.
- **The F7 cube split** has an exact permutation p of 0.011 (n 7 against 8). But it is direction-only by pre-registration
  and was fixed in advance, so it supports no claim.

**Exact wording.**
- F2: "(F2) kept automatically: even at share 1 no new prime could exceed F = 3.79 (1933), so this prediction could not
  fail. The largest new F is 2.80 (1933), and the maximum stays at 1789 (4.41)."
- F3: "(F3) kept, near-automatically: Spearman(F, N₁/μ₁) is 0.982. It is 0.969 at any constant share and ≥ 0.90 in 99.9%
  of share permutations, because log N₁/μ₁ carries most of the variance of log F (0.37 of 0.47). F is N₁/μ₁ rescaled by
  a share that moves by about ±12%; it is not a factor separate from N₁/μ₁."
- F4: "(F4) kept: Spearman(share, N₁/μ₁) 0.52 (0.51 with the scorer's tie handling). The share's elasticity in N₁/μ₁ is
  0.10 (0.04–0.17)."
- F5: "(F5) kept, automatically in rank: 0.845, and ≥ 0.5 in every share permutation. Its content is that the rest's
  count grows with N₁/μ₁ (elasticity 0.79, 0.64–0.91; the 2+2 count 1.10)."
- F7: "(F7) all three directions held, but they were already fixed by the known N₁/μ₁: with F at share 0.8 all three
  held before the runs. No claim."
- Exploratory: "Spearman(F, symR) 0.92 is N₁/μ₁'s (0.92). Post hoc: the share is higher at p ≡ 1 than p ≡ 7 (mod 12),
  median 0.71 against 0.62, in both λ bands (permutation p 0.054 and < 0.001), with λ balanced across classes. To be
  pre-registered before use."
- §12 text: where F is called the family's "weight factor", add "F carries N₁/μ₁'s ranking (Spearman 0.98)". At κ = 6, a
  large F and a large N₁/μ₁ are the same observation.

# Author's disposition of round 4f (10 Nov 10:58)

All accepted, and applied in a new §12.11, §0, §12.4, §12.8 and §12.9, the handoff, STATE and mechanical plan item 2.
- Each prediction is recorded in your wording: F1 refuted, F2 kept automatically, F3 and F5 near-automatic and
  automatic in rank, F4 at 0.52 with the elasticity 0.10, F6 as point values with 1933's overlap noted, and F7 settled
  in advance with no claim.
- Every "weight factor" or "family factor" phrase now says that F carries N₁/μ₁'s ranking. "F bounded" is restated as
  "(N)'s B bounded at spike primes" for κ = 6.
- The share-by-class result is recorded as post hoc, to be pre-registered before use.
- Verified myself before recording: F2's ceiling (1933 at share 1: 2.665 × 1933²/2,624,400 = 3.79), and that
  N₁/μ₁·p² alone has Spearman 0.98 with N₁/μ₁ (0.97 over the 25), with F/N₁/μ₁ in 0.58–1.05.

# Round 4g (referee, 10 Nov 11:07): the §12.12 draft (G = s/R₂₊₂)

**Verdict: ACCEPT WITH CHANGES.**
- The correction to §12.11 is right. The G chain is right, and it is never weaker than the F·B form.
- Fix one factual slip (the N₁/μ₁ range at the spikes) and one wrong threshold scale (κ^{(1+o(1))κ} should be
  κ^{(1/2+o(1))κ}).
- Say that the bound is asymptotic only: at κ = 7–10 it certifies nothing.
- Qualify the named methods and the κ = 4 "cyclotomic numbers" remark.
- Re-express §12.5 item 6's illustrations in G. They used F with N₁/μ₁ taken as 1, at κ = 6 primes where N₁/μ₁ is up
  to 4.5, so they are about 4.5× too large.
- Script and output: `scratch/r4g_checks.py` and `.out` (about 3 CPU-s at nice 19).

**1. The inequality chain: correct.**
- **The mixture bound.** V is an expectation over the (C1) measure, so V_all = s·V_fam + (1 − s)V_rest exactly at the
  population level. The weighted rms is a weighted L² norm, so the triangle inequality gives the bound.
  - The noise allowance carries through: ν_rest = ν_all/√(1 − s), so (1 − s)ν_rest ≤ ν_all.
  - The Monte Carlo estimators satisfy this only approximately. State it for population quantities.
- **|Q| ≤ n.** Q = Σ_z Sym_R·Sym_C over the n = p + 1 − 2κ points of P¹ outside S ∪ T, with |Sym| ≤ 1, so v ≤ n.
- **The additions.** In κ²/p units the family adds to B_D at most s·n·p/κ² = G·N_inv²κ²(n/p) < G·N_inv²κ². To B_L it
  adds at most s·n < G·N_inv²κ⁴/p.
- **The exponents.** N_inv = κ(κ−1)(κ−2)(κ−3)/8 < κ⁴/8. log_κ N_inv²κ² is 6.78, 7.14, 7.40 and 7.60 at κ = 7–10.
- **"Never weaker".** (N) gives μ₁/N₁ ≤ B, so G = F·μ₁/N₁ ≤ F·B.
- **Notation.** The draft uses G for both the parameter and the group ("ρ_G … for either group G"). Rename the group,
  e.g. ρ_𝒢 or "for each group, L or D".
- **(N) is still needed elsewhere.** The step needs no lower bound on N₁, but OSC′ still contains (N): it enters the
  noise term (§12.2). Say "this step needs no (N)", not that the argument does.

**2. "Spoils only if G = κ^{Ω(κ)}": it follows, asymptotically.**
- The exponent (1/2+o(1))κ needs log_κ B_L, log_κ B_D = o(κ) (§11.8). The family adds G·κ^{O(1)}. So if
  log_κ G = o(κ), the family cannot break it, and the rest enters only through (1 − s)ρ_rest ≤ ρ_rest.
- **Missing: the elementary bound certifies nothing at accessible κ.**
  - At κ = 7–10, N_inv²κ² = κ^{6.8–7.6}. The D tolerance for any exponent below κ is (1 − 1/ln κ)κ − O(1) = 3.4–5.7.
  - At T(κ) the L bound is G·κ^{2.2–3.2}, against (1/2 − 1/(2 ln κ))κ = 1.7–2.8.
  - So with v ≤ n the bound is asymptotic only. Finite κ still needs the family's v, as in item 6.
- **Also missing: nothing elementary excludes G = κ^{Ω(κ)}.**
  - The only cap is s ≤ 1, i.e. G ≤ 1/R₂₊₂. At the §11.8 thresholds that is κ^{2.4}, κ^{3.2}, κ^{4.2} and κ^{5.1} at
    κ = 7–10, and κ^{κ+κ/ln κ−12+O(1)} in general.
  - So the question is open, not settled trivially.

**3. G values: confirmed.**
- **κ = 6** (29 primes, shares from the npz counts, R₂₊₂ = 2,624,400/p²):
  - G is 0.584–1.051, median 0.738, with the maximum at 1933.
  - The caps 1/R₂₊₂ are 0.893–1.424, and G/cap is the share, 0.50–0.86. So this is no test, as the draft says.
  - At the spikes:

    | prime | G | F | N₁/μ₁ |
    |---|---|---|---|
    | 1789 | 0.98 | 4.41 | 4.50 |
    | 1657 | 0.87 | 3.89 | 4.47 |
    | 1597 | 0.84 | 3.64 | 4.36 |
    | 1933 | 1.05 | 2.80 | 2.66 |
    | 1531 | 0.64 | 2.63 | 4.11 |

- **κ = 7** (R₂₊₂ = 105²·7⁴/p²):

  | prime | share | G | cap | source |
  |---|---|---|---|---|
  | 35281 | 0.043 | 2.02 | 47.0 | pairsym, 19 configurations |
  | 35099 | 0.011 | 0.51 | 46.5 | pairsym, 5 |
  | 36037 | 0.0308 | 1.51 | 49.1 | split, 185 |
  | 34693 | 0.021 | 0.96 | 45.5 | pairsym, 9 |
  | 23549 | 0.063 | 1.33 | 20.9 | pairsym, 5 of 79 |

  The caps span 21–49, and "5–185 configurations" is right.
- **"No measured prime has G above 2"** is false by rounding (35281: 2.02, from 19 clustered pairsym configurations).
  Use "about 2".
- **"At spike and typical primes alike" overstates.** At κ = 6 G is capped, so no spike tests anything. At κ = 7 there
  is one spike, 36037 (G 1.5).

**4. "What a proof would need": four fixes.**
- **Threshold scale.**
  - "at p = κ^{(1+o(1))κ} near the thresholds" is wrong. The thresholds are T = κ^{(1/2+o(1))κ}: log_κ T = 5.57–7.36 at
    κ = 7–10, below κ − 1.
  - The pattern length is then κ ≍ log p/log log p, with constant about 2.
- **"About κ² shifted values of one variable set".**
  - The conditions are on the κ² differences t_i − s_j of 2κ variables: the profile of each t_i in the κ shifts s_j.
  - Weil's error should be stated as relative: about κ^{O(κ²)}/√p. That exceeds the main term unless p ≥ κ^{cκ²}, which
    is right as drafted. One-variable Weil suffices; Deligne is not needed.
- **Named methods.**
  - Burgess, and Graham–Ringrose (smooth moduli), bound short-interval character sums. They do not address fixed-length
    patterns with variable shifts, so calling them "the methods known there" misattributes them.
  - Hanson–Petridis bounds sets whose sumset lies in a multiplicative subgroup. Its sizes are of order √p, which is
    vacuous for sets of size κ.
  - Suggested: "Weil-type square-root bounds are the general tool for such counts, and they fail here. Short-interval
    methods (Burgess; Graham–Ringrose) and sumset bounds in multiplicative subgroups (Hanson–Petridis) address other
    questions and give nothing at set sizes κ ≍ log p." Keep "no formal reduction to a named conjecture is claimed".
- **κ = 3.** Fine as a statement: there is no 2+2 family at κ = 3. Better: "κ = 3 has no 2+2 family (two disjoint pairs
  need κ ≥ 4), so §11.2's exact method says nothing about G."
- **κ = 4, checked** (300 cases: 25 random S at each of p = 197, 389, 1009, 2017, × 3 pairings).
  - Every 4-set has one involution per pairing (ι(z) = (αz + β)/(γz − α)). It preserves S.
  - It maps mc_classes bucket keys to bucket keys bijectively in every case. The one exception is the pole α/γ, which ι
    sends to ∞, outside the F_p buckets.
  - Two ι-pairs in T force x and ιx into one bucket, and ι permutes buckets, so that bucket is ι-invariant. "The 2+2
    count is a sum over ι-invariant buckets" is right.
  - "Computable by cyclotomic numbers of order 4" is not checked and is doubtful. The buckets depend on the cross-ratio
    of S (S ∼ {0, ∞, 1, μ}), so the count is a sum over μ of joint order-4 character counts for two points of a bucket.
    These need not reduce to the field's cyclotomic numbers.
  - Suggested: "reduces to order-4 character sums over the cross-ratio of S; whether these close in cyclotomic numbers
    is not checked. Either way it gives κ = 4 values, not a bound uniform in κ."
- **The spike range in the correction.**
  - "N₁/μ₁ 2.6–4.5 at the κ = 6 spikes" is wrong for the sD spikes: 1669 and 1693 have 1.28 and 1.36.
  - Use "N₁/μ₁ 1.3–4.5 at the six sD spikes at λ ≤ 0.25 (2.7–4.5 at the four with the largest F)".
  - The 1741 statement (0.37, the survey minimum) is right.
- **The Consequence bullet.** "Unless G grows with κ" should be "unless G grows like κ^{Ω(κ)}": polynomial growth is
  harmless.

**5. The §12.11 correction: right.**
- (N) bounds N₁/μ₁ from below. The spikes' large N₁/μ₁ never stresses it, and the family's effect runs through
  s = G·R₂₊₂, not through N₁/μ₁. So F, which includes the N₁/μ₁ factor, was the wrong parameter.

**What else changes with it.**
- **§12.5 item 5.** Replace "With the largest measured F (4.4), the weight w = F·R₂₊₂ is up to 4.5% at κ = 7 and 0.55% at
  κ = 8" with "With the largest measured G (about 2, κ = 7), the share s = G·R₂₊₂ at the thresholds is about 2% at κ = 7
  and 0.24% at κ = 8".
- **§12.5 item 6.**
  - Replace "s = F·R₂₊₂/(N₁/μ₁) … take N₁/μ₁ = 1" with s = G·R₂₊₂. That step applied N₁/μ₁ = 1 to κ = 6 data where it is
    up to 4.5.
  - Re-express the illustrations as G·v = F·v/(N₁/μ₁), using the note's F·v and the survey N₁/μ₁ (approximate for
    1933, whose v is from the earlier split):

    | prime | G·v |
    |---|---|
    | 1621 | 0.007 |
    | 1933 | 0.10 |
    | 1597 | 0.08 |
    | 1657 | 0.22 |
    | 1789 | 0.34 |

    The spread is then about 50×, not 500×.
  - With 1789's values, the additions at T(7–10) become about 3.6, 2.4, 1.3 and 0.7 (not 16, 11, 6, 3). The
    constant-B_D variant becomes 0.17 and 0.02 (not 0.78, 0.09), and the L gain about 0.02 (not 0.09).
  - These scale 1789's κ = 6 G, which is capped there. At κ = 7 the measured G reaches 2, so say they are illustrations.
  - "Without v": replace F·B by G, as in the draft.
  - Item 7: replace "in terms of F, which is unbounded" with "in terms of G, which nothing beyond the trivial cap
    1/R₂₊₂ bounds".
- **§12.8.**
  - Question 1 becomes "Is G(p) = κ^{o(κ)} uniformly over p ≥ p₀ near the threshold path?". Drop "If (N) holds with
    B = κ^{o(κ)} … otherwise the condition is on F·B": the G condition needs no (N) for this step.
  - The "B_D ≈ 16 at κ = 7" sentence becomes ≈ 3.6, with the same caveat.
  - Gate: "F(p) bounded, or κ^{o(κ)}" becomes "G(p) bounded, or κ^{o(κ)}".
- **§12.9 "Bounding F" becomes "Bounding G".**
  - The target is the share: #2+2 ≤ κ^{o(κ)}·R₂₊₂·N₁.
  - A bound O(κ^{o(κ)}·N_inv²κ⁴p⁻²·μ₁) on the 2+2 count suffices only together with (N) at B = κ^{o(κ)}.
- **§12.11.**
  - Replace "which is (N)'s constant B" with: "At κ = 6 F's size is N₁/μ₁'s, since G = 0.58–1.05 and s ≤ 1 caps it at
    1.42. A large count does not stress (N), and the family's effect runs through G (§12.12)."
  - Its gate "F(p) bounded or κ^{o(κ)}" becomes the G gate.
- **STATE.md and the handoff.**
  - STATE.md line 63 ("at kappa=6 'F bounded' is '(N)'s B …'") should carry the correction, with the proof target
    restated as G.
  - Correct AGENT_HANDOFF.md line 60 by a new top entry rather than an edit, and restate the gate at line 146 as G
    there.

### Author's disposition of round 4g (10 Nov)

All points accepted and applied.
- §12.11's backwards (N) sentence is corrected in the note; §12.12 opens with the correction. The spike N₁/μ₁ range is
  restated as 1.3–4.5 over the six sD spikes at λ ≤ 0.25 (2.7–4.5 at the four with the largest F).
- §12.12 uses "for each group (L or D)" in place of the clashing symbol, says "this step needs no (N)" and states the
  bound for population quantities.
- Added: the bound certifies nothing at κ = 7–10 (D κ^{6.8–7.6} against tolerance 3.4–5.7; L G·κ^{2.2–3.2} against
  1.7–2.8), and the only cap G ≤ 1/R₂₊₂ is κ^{2.4}, κ^{3.2}, κ^{4.2}, κ^{5.1} at the κ = 7–10 thresholds.
- "above 2" became "about 2"; "spike and typical alike" is dropped (κ = 6 is capped; κ = 7 has one spike).
- Thresholds κ^{(1/2+o(1))κ}, pattern length κ ≍ log p/log log p, κ² differences of 2κ variables, relative error
  κ^{O(κ²)}/√p, and the named-methods sentence are as the referee worded them. No formal reduction is claimed.
- κ = 3 and κ = 4 sentences as worded (κ = 4 cyclotomic closure not checked).
- §0's F·B line is restated as G. STATE line 63 and the handoff's F·B statements are corrected by a new top
  handoff entry and a STATE rewrite, not by editing the old entry.

# Round 4h-a (referee, 10 Nov 11:13): the inserted §12.12, the §0 line, and the round-4g edits

**Verdict: six fixes, all small; the rest landed as worded.**
- Every round-4g fix in §12.12 landed: the correction and its spike range, the group notation, population quantities,
  "this step needs no (N)", the asymptotic-only bullet, the cap, "about 2", the threshold scale, the κ² differences,
  the relative Weil error, the methods sentence, κ = 3, κ = 4, "κ^{Ω(κ)}" in the Consequence, and the new gate.
- The §12.5 item 5 and 6, §12.8, §12.9 and §12.11 restatements also landed.
- "Twelve passes" is right through 4g (1, 2, 3, 3b, 3c, 4, 4b–4g). It becomes thirteen with this round.
- No new computation: the numbers are from `scratch/r4g_checks.out`.

**Fixes.**
1. **§12.12 "asymptotic only".** The L half is not true at κ = 10. The L additions at T(κ) are G·κ^{3.21, 2.96, 2.62,
   2.24} against L tolerances of 1.70, 2.08, 2.45 and 2.83 for κ = 7–10, so at κ = 10 it is within tolerance for G ≈ 1.
   The conclusion stands, because D fails at every κ. Use: "the D addition κ^{6.8–7.6} exceeds the D tolerance of
   3.4–5.7 in log_κ at every κ = 7–10, and the L addition at T(κ), G·κ^{3.2, 3.0, 2.6, 2.2}, exceeds the L tolerance
   (1.7, 2.1, 2.5, 2.8) at κ = 7–9".
2. **§12.12 "κ^{κ+κ/ln κ−12+O(1)} in general".**
   - The exponent is correct. 1/R₂₊₂ = T²/(N_inv²κ⁴), with 2 log_κ T = κ + κ/ln κ + O(1) and
     log_κ N_inv²κ⁴ = 12 + O(1). It matches item 5's R₂₊₂ = κ^{12−κ−κ/ln κ+O(1)}.
   - But the −12 sits inside an unspecified O(1). The O(1) there is about +2.8 at κ = 10: actual 5.12, against
     κ + κ/ln κ − 12 = 2.34.
   - Either write κ^{κ+κ/ln κ+O(1)}, here and in item 5, or keep both as they are. It is not wrong; do not drop the
     statement.
3. **§12.5 item 6: the 1621 line was not rescaled.** "With 1621's values … at most 0.05, 0.03, 0.02 and 0.01" is still
   F-based. At 1621 N₁/μ₁ = 0.42, so G = F/0.42 = 2.4·F: there the correction raises the numbers. Use "at most about
   0.12, 0.07, 0.05 and 0.02".
   - The same applies to §12.8's "and at most 0.05 with typical values", which should be about 0.12.
4. **§12.5 item 6, leftover F.** "what matters is the largest F·v over primes near T(κ)" should be G·v.
5. **§12.9 "Bounding G", last bullet.** "Weil's error terms are κ^{O(κ²)}√p, useless at p = κ^{O(κ)}" is the old
   wording. Use "Weil's relative error is about κ^{O(κ²)}/√p, useless at the thresholds p = κ^{(1/2+o(1))κ}", as in
   §12.12.
6. **"No measured prime has G above about 2"** is fine as a statement, but say what it rests on. Use: "no measured prime
   has G above about 2 (κ = 7's 2.0 is a pairsym value from 19 clustered configurations; κ = 6 values cannot exceed
   1.42)".
   - In "G in the data", "to within about 2×" is a statement about point values, and 35099 and 23549 rest on 5
     configurations each. Add "(point values; 35099 and 23549 rest on 5 configurations each)".

**Gate list: fine as it stands.** Optionally add "the κ = 4 2+2 count in closed form", since cyclotomic closure is not
checked.

**§0 line: accept.** Optionally "this step needs no (N)", for consistency with §12.12, since OSC′ itself contains (N).
"Measured G is 0.5–2 at κ = 7" is right (0.51–2.02).

### Author's disposition of round 4h-a (10 Nov)

Items 1 and 3–6 applied as worded, and the κ = 4 closed-form gate added. Item 2: both exponents are left as they are,
since the −12 is absorbed into the O(1) and does no harm. §0 left as accepted.

# Round 4h-b (referee, 10 Nov 12:21): scoring of the κ = 7 split at 34693

**Verdict: ACCEPT WITH CHANGES.**
- The call (INCONCLUSIVE) and the failed prediction are right.
- The 2σ ends are credible; the reason for z = 34 is given below.
- Fix three items of wording:
  - "not close" sits on a 0.002 margin;
  - the B_D contrast with 36037 is not shown;
  - 1.65× should be 1.64×.
- Script and output: `scratch/r4hb_checks.py` and `.out`. It uses my own Gram-matrix path and imports nothing from
  the scorer. About 3 CPU-s at nice 19.

**Rule and timing.**
- The rule was written at 10:59:29. The log ends at 12:18:28 after 4736 s, so the run started at about 10:59:32. Seed
  17 is distinct, as round 4e advised.
- The scorer was written at 12:19:03, after the result. That is acceptable: the rule names `split_report.py` as the
  reader, the scorer's logic matches the rule's text line by line, and my path reproduces every value.
- **Files.**
  - The parts add up.
  - Batches are by S: 319–437 configurations per batch, and 3–13 2+2 configurations per batch.
  - The run has 6007 configurations, 1,467,329 S, and N₁/μ₁ 0.906 (0.89 ± 0.05 was known).

**1. The call is right, but "not close" has almost no margin.**
- Rest B_L is 0.3861 (2σ 0.3741–0.3977). LIFTED fails only on the point threshold, since its second condition (lower
  end > 0.270) holds. LIKE fails.
- The range crosses neither 0.33 nor 0.40, so it is not close by the rule's definition. But the upper end is 0.0023
  below 0.40: about 2.3 se(B) from the point value, with a jackknife se that is itself uncertain by about 18% on 15
  degrees of freedom.
- The prediction (0.22–0.35) failed.

**2. The ends are credible: why z is 34.**
- 95% of X_L is in the (2,2) bin, which carries large class values (|V| ≈ 3.2), spread evenly over six cells. Their
  batch-to-batch cv is 0.09–0.10.
- At 34847, X_L sits in three (2,2) cells with batch cv 0.12–0.18. The rest of the L group adds noise without signal
  ((0,7) is −12% of X).
- 34693 therefore has a larger X (3.7·10³ against 1.5·10³) and a smaller jackknife se (108 against 157). se/X is 0.03,
  against 0.11 (34847), 0.12 (35099) and 0.15 (36037).
- The batches genuinely agree: y_b > 0 in 16 of 16, with a cv of only 0.05, and half-samples 0.363–0.410. So the narrow
  range is real, not a broken se.
- 36037's rest has a wider range because its X is spread over noisier bins: (0,3) 19%, (2,3) 8%, and (0,4) and (2,4)
  3% each.

**3. The other numbers are confirmed.**
- Whole-run B_L 0.3869 (0.375–0.398).
- Ratios:
  - rest / 0.241 = 1.60;
  - rest / 36037's rest = 0.67;
  - 36037 whole / 34693 whole = 1.64 (your 1.65 rounds 0.6347/0.3869 the wrong way).
- Share 0.0231, R₂₊₂ 0.0220, G 1.05 (pairsym 0.96), F 0.95.
- "At least three levels" holds at more than 2σ:
  - 34847 and 35099: upper ends ≤ 0.270;
  - 34693: 0.374–0.398;
  - 36037: lower end 0.535.
- **The profile differs from 36037's.**
  - 34693's excess is mostly (2,2): 2.81 against 1.93 and 1.67, and 3.78 at 36037.
  - (0,3) is 1.07 (z 4.3), against 0.39 and 0.65, and 3.70 at 36037.
  - (3,3) is 0.052 (z 8.8) and (0,4) is 0.29 (z 2.6), both resolved.
  - So 34693 is intermediate in level and puts less of its X outside (2,2): 5%, against 37% at 36037.

**4. B_D: the reading is right, the contrast is not shown.**
- X_D is negative at 34693 (−80, se 69). B_D = 0, with upper ends 1.61 (whole run) and 1.53 (rest), in κ²/p units. It is
  noise-level.
- But 36037's own B_D is unresolved: 9.4, z 1.6, and its 2σ range reaches 0. So "unlike 36037" overstates. The D group
  separates neither prime from the comparison primes.
- PW_pair is at its floor at 34693 (0.944 against 0.90), unlike 36037's 2.71. I have not decomposed PW_pair here,
  so I give no reason for the difference.

**5. The symR remark is fine as post hoc.** Add that both high-symR primes sitting above both low ones is an ordering
random assignment gives with probability 1/6.

**Wording for the record.**
> "34693 (λ 0.295, symR 44.22, equal to 36037's; seed 17; rule written before the run) is scored INCONCLUSIVE.
> - Its not-2+2 B_L is 0.386 (2σ 0.374–0.398). That is above the comparison primes (upper ends ≤ 0.270) and below the
>   LIFTED threshold 0.40. It is not close by the rule's definition, but the upper end is only 0.002 below 0.40. The
>   prediction (0.22–0.35) failed.
> - The whole run gives 0.387: 1.60× the comparison mean, and 36037's whole run is 1.64× it. So the four κ = 7 primes
>   at λ ≈ 0.3 sit at three separated levels.
> - The excess is mostly in (2,2) (95% of X_L). (0,3), (3,3) and (0,4) are also above the comparison primes, with less
>   outside (2,2) than at 36037.
> - The 2+2 share is 0.023, so G is 1.05 and F 0.95.
> - B_D is noise-level (< 1.6 at 2σ), and so is 36037's (z 1.6), so the D group separates neither.
>
> Post hoc: the two equal-symR primes differ 1.64× in B_L, though both sit above both low-symR primes (an ordering of
> probability 1/6 at random). symR does not fix B_L at κ = 7, and four primes support no correlation."

**Gates to add.**
- "34693 lifted" or "34693 like the comparison primes" (the call is inconclusive).
- A κ = 7 spike/typical dichotomy at λ ≈ 0.3: three levels in four primes.
- Any symR–B_L relation at κ = 7.

# Round 4i (referee, 10 Nov 12:47): §12.13 draft, κ = 4 in closed form and the κ = 5 shape

**Verdict: ACCEPT WITH CHANGES** (14 fixes below). The algebra is right. One script diagnostic is wrong, and the
draft's sentence about it must change; no reported number depends on it. Several statements are stronger than
what is shown.

**Own checks** (`scratch/r4i_checks.py`, `.out`; `scratch/r4i_pole.py`, `.out`; nice 19, about 10 s of CPU in total).
Own code builds ι as (αz + β)/(γz − α), with γ = a + b − c − d, α = ab − cd and β = γab − α(a + b). It does not use
`mob_from`, `k4_22.py` or `k5_22.py`. It enumerates the κ³ normalised partial keys instead of relying on witnesses.
- A. (c s_i + d)(c s_j + d) = −det ι held for both swapped pairs of all 840 involutions tested: κ = 4 (p 197, 401),
  κ = 5 (1451, 2521), κ = 6 (1933) and κ = 7 (1009). The transport P(ιt)_{ι(l)} = P(t)_l + α_l + β(t) held at
  every finite, non-exceptional t. The number of σ_ι-fixed partial keys equalled c_ι·κ every time: 8 per split ι and
  0 per non-split ι at κ = 4; κ per ι at κ = 5 and 7 (5 and 7); 12 per split ι and 0 per non-split ι at κ = 6.
- B. The κ ≥ 5 pairing predicate (sign fixed in item 6) agreed with actual pairing at every point of every
  partial-fixed bucket. That is 0 mismatches in 10060, 8706, 10610 and 4264 points at κ = 5, 5, 6 and 7. My first
  run had the right-hand side's sign reversed and gave about 30% mismatches at κ = 5. The sign is load-bearing.
- C. #{r : η(r) = η(1 − r) = 1} = (p − 5)/4 at p = 101, 197, 401, 1009 and 2017, by direct count.
- D. The κ = 4 Weil numbers are in item 5.
- E. The pole rule of `k4_22.py`, against the enumerated fixed keys, is in item 2.

**Checked and correct as written.**
- The transport identity and the trace-0 identity: d = −a gives (c s_i + d)(c s_j + d) = a² + bc = −det. Hence
  α_i + α_j = −ind(−det).
- Solvability of 2C ≡ −ind(−det) (mod κ).
- c_ι = 1 at odd κ and 2·[split] at even κ; the discriminant is 4(−det).
- The −det values r, r(r − 1) and 1 − r. Their product −r²(r − 1)² is a square at p ≡ 1 (mod 4), so
  #split ∈ {1, 3}, and #split = 1 + 2·[η(r) = η(1 − r) = 1].
- The count (p − 5)/4, and E[#split] = 1 + (p − 5)/(2(p − 2)).
- "No partially paired bucket" is a consequence of the transport, and so is "paired ⇒ σ-fixed key". The brute force
  confirms both.
- The −2 free-orbit correction. If T is a 2+2 for two involutions, T is invariant under both and hence under V₄. A
  V₄-invariant 4-set is either a free orbit, which is two pairs for all three ι and so counted 3 times, or
  Fix(ι₁) ∪ Fix(ι₂). In the second case only ι₃ has two pairs in T; ι₁ and ι₂ each fix two points of T. So "a 2+2
  for exactly two involutions" cannot happen, and −2 is right.
  - Note that the brute force tests the correction only at p = 401: the overlap correction is 0 at 101 and 197.
- The one-variable shape at κ ≥ 5, and the Weil range p ≥ κ^{(4+o(1))κ} (item 7).
- P2–P5 scored correctly; P1 needs rewording (item 9).
- Pre-registration order: predictions 12:30:32, `k5_22.py` saved 12:31:12, first output 12:37:18. The order holds.

**Fixes.**

1. **Exceptional points (line 24).** For an involution, d = −a, so ι(∞) = a/c = −d/c = t₀: the pole and ι(∞) are
   the same point. Write "apart from at most 3 exceptional points: the two fixed points of ι and the pole
   t₀ = −d/c (= ι(∞))". The bound 3 stands.

2. **The pole sentence in Checks (lines 35–36) is wrong.**
   - What the script does: `k4_22.py` adds key(t₀) as the 8th fixed key whenever 7 keys are witnessed. It does not
     check that key(t₀) is σ-fixed.
   - Why that fails in general: σ maps key(t₀) to key(ι t₀) = key(∞), which is the zero key. So key(t₀) is σ-fixed
     only when key(t₀) = 0, about 1 split ι in 10 in my samples (62 of 622 at p = 197, 43 of 452 at p = 401).
   - What `r4i_pole.py` found at p = 401 (452 split ι), with witnesses counted as in `k4_22.py`:
     - The rule fired 75 times.
     - 73 of those were in S with an empty bucket. In all 73 the added key is **not** σ-fixed: the missing fixed key
       has an empty bucket.
     - Only 2 were in S with all 64 buckets nonempty, and there the rule was right.
     - At p = 197 the rule fired 5 times (3 in S with an empty bucket) and was right each time.
   - Why the full-bucket case is a theorem: if all 64 buckets are nonempty and a fixed key K is unwitnessed, then
     every point of K's bucket is exceptional. A fixed point of ι would witness K, so the bucket holds only t₀, and
     K = key(t₀).
   - So "about 19% of split ι at p = 401 … the 8th is witnessed only by the pole, whose bucket then holds only
     exceptional points" mostly counts S with an empty bucket, where the parenthesis is false.
   - Harmless for every reported number:
     - G and the 2+2 count use the actual pairings;
     - check (b)'s "exactly 8" is applied only when all 64 buckets are nonempty;
     - the subset check cannot be masked, since paired keys are provably σ-fixed.
   - Replace with: "every split ι has exactly 8 σ-fixed keys and every non-split ι none (enumerated by the referee,
     r4i_checks.py). When all 64 buckets are nonempty, each fixed key is witnessed by a non-exceptional point or a
     fixed point of ι, except that a fixed bucket may consist of the pole alone (2 of 452 split ι at p = 401 in the
     referee's sample)."
   - Drop the 19% and 1% figures, or label them as the firing rate of a script counter that is mostly
     inapplicable. The script's comment on line 87 has the same error. I have not edited it.

3. **μ₁ and μ₂₊₂ notation (line 39).** `k4_22.py` uses the Poisson factorial moments μ₁ = 64·λ⁴/24 and
   μ₂₊₂ = E[#split]·λ², not 64·C(λ, 4) or 8·C(λ/2, 2). These differ greatly at small λ: at λ = 1.6,
   64·C(λ, 4) = 1.43 against 64λ⁴/24 = 17.5.
   - The "Exactly, G = (2/3)·E[#split]·(N₂₊₂/μ₂₊₂)/(N₁/μ₁)" line (line 41) is an identity only with the Poisson
     moments, because R₂₊₂ = 9·256/p² and μ₂₊₂/μ₁ = 1536·E[#split]/p².
   - Write: "N₁(S) ≈ μ₁ := 64·λ⁴/4! and #2+2(S) ≈ #split(S)·8·(λ/2)²/2 = #split(S)·λ², with λ = p/64".

4. **E[c_ι] = 1 (lines 18–19).**
   - A split ι is as likely as a non-split one only to O(1/p). At κ = 4, E[c_ι] = 2E[#split]/3 = 1 − 1/(p − 2).
   - Write "so E[c_ι] = 1 + O(1/p) (exactly 1 − 1/(p − 2) at κ = 4)".
   - Likewise, "G(p) → (2/3)·E[#split] = 1" holds in the limit.

5. **Weil at κ = 4: "with explicit constants" (lines 42–49).** Either give the constants or delete the phrase.
   The constants are:
   - |b_K − (p − 4)/64| ≤ (63/64)·3√p + O(1). The O(1) covers the points of S, and it is right.
   - So ε := 192/√p bounds the relative error of b_K. Then
     G(S) / ((2/3)·#split(S)) ∈ [(1 − ε)²/(1 + ε)⁴, (1 + ε)²/(1 − ε)⁴]·(1 + O(1/λ)), and the same holds for G(p).
     The O(1/λ) covers the falling factorials, the e_K and the free-orbit correction, which is ≈ 0.34/λ in the
     data.
   - ε < 1 needs p > 3.7·10⁴. That is where Weil first certifies b_K > 0, not where it controls G. The factor
     interval is:

     | p | 10⁵ | 10⁶ | 3·10⁶ | 10⁷ | 10⁸ |
     |---|---|---|---|---|---|
     | interval | [0.02, 108] | [0.32, 3.3] | [0.52, 1.97] | [0.70, 1.45] | [0.89, 1.12] |

     The upper end is ≤ 2 from p ≈ 2.9·10⁶ and ≤ 1.1 from p ≈ 1.5·10⁸.
   - Line 48: replace "The error is below 1 only for p ≳ 4·10⁴" with "Weil's relative error on b_K is below 1
     only for p ≳ 4·10⁴, and it brackets G within a factor 2 only for p ≳ 3·10⁶".
   - Also: G(S) ≤ 2 + O(p^{−1/2}) is asymptotic. At p = 101 the 3-split class has G = 2.21 (the draft's own table).

6. **κ ≥ 5 extra condition: state ω_l(K) and its sign (line 70).**
   - Derivation: s_l − ιt = ι(ι s_l) − ι(t) = det·(ι s_l − t)/((c ι s_l + d)(ct + d)), and the same for s_i − ιt with
     ι(s_j) = s_i. So the condition is
     ind(ι(s_l) − t) − ind(s_l − t) ≡ P(t)_j − P(t)_i + ind(c ι(s_l) + d) − ind(c s_j + d) (mod κ),
     where ι(s_i) = s_j.
   - P_j − P_i is read off K, so ω_l(K) = K_j − K_i + ind(c ι(s_l) + d) − ind(c s_j + d). Verified (check B).
   - Line 73: "R₂₊₂ is exactly the main term" → "R₂₊₂ is the leading term:
     s = E[c_ι]·R₂₊₂·(1 + O(1/λ) + O(κ^{O(1)}/p))".
   - Name the lower-order pieces:
     - T with ≥ 3 ι-pairs (possible from κ = 6), which Σ C(m_K, 2)·C(b_K − 4, κ − 4) counts more than once;
     - T that is a 2+2 for two involutions;
     - ι with a third swapped pair, or a fixed point, inside S. Here ι(s_l) ∈ S, so the l-condition degenerates.
       This has probability O(κ²/p) per ι.

7. **The §12.12 correction is right, and Round 4g's endorsement of "κ^{cκ²}" is withdrawn.**
   - b_K involves κ points, and m_K involves 2κ − 4 points (S and the ι(s_l)) with 2κ − 5 conditions. Weil errors
     are O(κ√p) against p/κ^{κ−1} and p/(2κ^{2κ−5}).
   - So b_K is controlled from p ≥ κ^{(2+o(1))κ}, and m_K from p ≥ κ^{(4+o(1))κ}. The range is set by m_K.
   - With relative errors ε_b and ε_m, G = 1 + O(ε_m + κ·ε_b) = 1 + O(κε). This needs m_K ≫ 1 and b_K ≫ κ, both
     true in that range.
   - The same correction applies to N₁(S) = Σ_K C(b_K, κ), which is a polynomial in the b_K. Say so: §12.12's
     κ^{cκ²} estimate is too pessimistic for N₁ as well. I endorsed that wording in Round 4g; that endorsement was
     wrong.

8. **Line 82: "second-moment question".** Replace with "a question about the joint factorial moments of
   (b_K, m_K) at λ ≈ 1: do the sparse patterns cluster in buckets by more than κ^{o(κ)} over Poisson?"

9. **P1 scoring (lines 92–93).**
   - The pre-registered P1 says "exactly 25", but the measured witnessed counts are 11–25, 17–25 and 23–25 at
     1451–5011.
   - What is true: every ι has exactly c_ι·κ^{κ−3} = 25 partial-fixed keys. I enumerated this for 270 κ = 5 ι, as
     5 partial keys × 5 values of the free coordinate. The shortfall is buckets that are empty or hold only
     exceptional points (the pole and the ι(s_l)).
   - Write: "P1 held: every ι has exactly 25 partial-fixed keys (a count of keys; enumerated for 270 ι by the
     referee). No paired point lay outside them in 201,000 involutions. At small λ only 11–25 of the 25 buckets hold
     a witnessing point." Scoring P1 as held is fair on that reading.

10. **Line 107: "§12.2 found".** Change to "§12.4 found (0 of 845–1459 structured T per prime from a non-split ι)".

11. **Line 108: "matches".** Change to "is consistent with … Those are threshold-range values, where the theory
    gives no bound, so they do not test it."

12. **Line 97: overlap correction.** "0.07–5%" → "0 (p = 101, 197) to 5.4% (p = 401), falling as ≈ 0.34/λ".

13. **Line 18: section reference.** "§12.5" is right (item 1). Nothing to fix there.

14. **Pre-registration line (lines 4–5).** Add the script and output times: "k5_22.py saved 12:31:12, first output
    12:37:18". Any "about 12:40" in messages should read 12:37.

**Gates.** The list on lines 113–114 is right. Add two:
- "Weil controls G at κ = 4 for p ≳ 4·10⁴" (it certifies only b_K > 0 there);
- "the pole witnesses the 8th key in about 19% of split ι at p = 401".

### Author's disposition of round 4i (10 Nov)

All 14 points accepted and applied in §12.13 as worded. That covers the pole/ι(∞) identification, the replacement pole
sentence (the 19%/1% figures dropped, and the counter labelled in `k4_22.py`'s comment), the Poisson moments, E[c_ι] =
1 + O(1/p), the explicit Weil constants and factor intervals, the signed ω_l(K), "leading term" with the lower-order
pieces named, and the §12.12 correction extended to N₁ (§12.12's Weil bullet is marked superseded). Also: joint
factorial moments, the P1 wording, §12.4, "is consistent with", 0 to 5.4%, and the pre-registration times. Both
gates are added. The scripts were not rerun: no reported number depends on the pole counter.


# Round 4j (referee, 11 Nov 09:33): scoring of mechanical item 6, the κ = 7 band at λ ≈ 0.3

**Verdict: the calls are right.**
- R1 is NOT SHOWN, R2 is INSIDE, and R3 is inconclusive.
- Both 34259's 0.519 and 34469's 0.131 are credible measurements.
- What must change is the interpretation built on two primes: "36037 is a spike in B_L", and the κ = 6 calibration
  transfer. Fixes follow.

**Own path** (`scratch/r4j_checks.py` → `.out`; nice 19, under 1 s of CPU).
- It uses its own Gram estimator and noise term, the same as r4hb_checks.py, not `k6_spike_survey.analyse`.
- Its point values and 2σ ends agree with `score_k7_band.out` to 3 decimals at all nine primes.
- All nine files share one configuration set: P, orb, supp and rb are identical.

**Timing.**
- Rules file: 12:24:39.
- Runs, from log end times minus elapsed time:
  - 34259 and 34273 started 12:24:45–46;
  - 34469 and 35281 started 13:35:50;
  - 36541 started 14:43:17 and finished at 15:26:15.
- The scorer was saved at 15:26:46, after every result was known.
- The rules came first, and the scorer only applies them. I reproduced its calls independently, so this is
  acceptable. It should still be stated (fix 7).

**1. The calls.**
- **R1.** The SPIKE conditions fail.
  - 36037's 2σ lower end, 0.535, is below 34259's 2σ upper end, 0.608. The ratio condition holds (2.59 ≥ 1.54).
  - Since SPIKE fails, the clause order does not matter here: NOT SHOWN applies, because 34259's point value 0.519
    is ≥ 0.50.
  - The scorer tests NOT SHOWN before SPIKE, while the rule text lists SPIKE first. That would matter only if both
    held, which is possible in principle. Future rules should state the precedence.
  - The call rests on one prime. Without 34259, the band's largest 2σ upper end is 0.419 and its median 0.241, and
    36037 would be a SPIKE (0.535 > 0.419; ratio 2.63). That is the case the NOT SHOWN clause was written for.
- **R2.**
  - ABOVE fails: 0.375 < 0.608. The rule text says 0.374; the difference is immaterial.
  - INSIDE holds: three band primes have point values ≥ 0.387 (34259, 35281 and 36541).
- **R3.** ρ = 0.350 over nine primes by hand ranking, with no ties, so the result is inconclusive. Over the seven band
  primes alone, ρ = 0.179, which is not pre-registered.
- **Predictions.**
  - "Each new prime in 0.18–0.35" failed: only 34273 is inside.
  - R1 SPIKE and R2 ABOVE failed.
  - The band median (0.245, inside 0.22–0.30) and R3's ρ range held.

**2. Credibility.** Columns: point value, leave-one-batch-out range, all C(16,8) half-samples, positive batch row
means, top cell's share of X_L, (2,2) and (0,3) bin shares of X_L, and N₁/μ₁.

| p | B_L | leave-one-out | half-samples (5–95%) | rows > 0 | top cell | (2,2) / (0,3) | N₁/μ₁ |
|---|---|---|---|---|---|---|---|
| 34259 | 0.519 | 0.471–0.527 | 0.432–0.605 (0.450–0.585) | 16/16 | 0.14 | 0.78 / 0.15 | 1.045 |
| 34469 | 0.131 | 0.124–0.138 | 0.057–0.197 (0.099–0.162) | 16/16 | 0.24 | 0.55 / 0.08 | 0.947 |
| typical band (34273, 34847, 35099, 35281, 36541) | — | — | — | 16/16 | 0.16–0.35 | 0.89–1.11 / 0.01–0.05 | 0.93–0.96 |
| 36037 | 0.635 | 0.608–0.647 | 0.506–0.771 | 16/16 | 0.09 | 0.63 / 0.19 | 1.080 |

- **34259.**
  - Every batch contributes positively, and no single cell carries the value (top cell 14%, top three 38%). Its
    lowest half-sample, 0.43, is above every half-sample 95% point of the four lowest band primes (≤ 0.27).
  - z is 5.4 rather than 7–21 because the batches disagree more (se/X larger), not because the signal is small.
  - Post hoc, not a claim: its secondary readings look like a milder 36037.
    - Only 0.78 of X_L sits in (2,2), and 0.15 in (0,3), against 0.89–1.11 and ≤ 0.05 at the typical primes;
      36037 has 0.63 and 0.19.
    - N₁/μ₁ is 1.045, and PW_pair is 1.17 against a floor of 1.02.
    - It also has the highest symR in the band (22.05).
- **34469.**
  - It is noisier: its half-samples reach 0.06, but its 5–95% range is 0.099–0.162.
  - Every batch contributes positively, leaving out one batch gives 0.124–0.138, and the top cell carries 24%.
  - Its 2σ upper end, 0.158, is below the 2σ lower ends of 34273, 34847 and 35099 (0.199–0.218). So it is genuinely
    low, not an extreme draw from their level.
- **Levels.** The band separates at 2σ into at least three levels:
  - 34469 (≤ 0.158);
  - 34273, 34847 and 35099 (0.199–0.270);
  - 35281 and 36541 (0.366–0.419).
  - 34259 (0.412–0.608) only just overlaps the third level, and 36037 overlaps 34259.
- B_D is unresolved at every band prime (z ≤ 0.8).

**3. Spread, and the κ = 6 comparison.**
- Ratios to the band median, 0.245:
  - band primes: 34259 2.12, 35281 1.60, 36541 1.60, 34847 1.00, 35099 0.97, 34273 0.96, 34469 0.53;
  - the two symR-picked primes: 34693 1.58 and 36037 2.59.
- The band spans 3.96× (0.131–0.519), and 4.85× with 36037.
- Against κ = 6 (§12.6):
  - 3 of the 7 unselected primes exceed κ = 6's unflagged maximum of 1.54×;
  - 34259, at 2.12×, sits inside κ = 6's spike range of 1.94–3.74×;
  - 34469, at 0.53×, is below the 0.58× that only 2 of κ = 6's 68 unflagged primes reach.
- So, with B_L the only reading available, either:
  - κ = 7 at λ ≈ 0.3 has spikes among unselected primes at a high rate (1–3 of 7); or
  - its typical spread is wider than κ = 6's unflagged spread.
- Seven primes cannot tell these apart, and κ = 7 has no flag analogous to sD/sN. Either way, the κ = 6 numbers do not
  transfer.
- Note what the band confirmed: the old worry is answered. 35099 and 34847 sit at the band median (0.97× and 1.00×),
  not at its bottom.
- What failed is the other premise of the 0.1% / 1.2% computation: that the κ = 6 unflagged spread carries over.

**Fixes.**

1. **§0, the 36037 bullet (note lines 59–61).** Replace with:
   "At κ = 7, λ ≈ 0.3, 36037 (picked on symR) has the highest B_L of nine primes. Its B_L is 0.635, 2.6× the median
   of seven primes not picked on symR (mechanical item 6, pre-registered). Against those seven it is not shown to be a
   spike: 34259 reaches 0.519 (2σ 0.41–0.61), and the seven span 0.131–0.519 (4.0×). The earlier call, a spike
   against two equal-λ primes (35099 and 34847), stands as scored, but only as a two-prime statement."
   - Lines 64–65 need updating too. Replace "The four primes at λ ≈ 0.3 sit at three separated levels" with "The
     nine primes at λ ≈ 0.3 sit at four or more levels separated at 2σ; symR does not fix B_L (ρ 0.35, inconclusive)".

2. **§12.6.** Keep the 34847 scoring as written, since it is a pre-registered call. Add one line after the call (line
   1216): "Superseded as a spike claim by the seven-prime band (mechanical item 6): not shown." Mark lines 1199–1204
   and 1236–1241 as superseded. These are the ratio-to-median argument, the 0.1% / 1.2% probabilities, and "2.4× the
   implied band median against ≤ 1.46×". Their premise, that the κ = 6 spread carries over, fails at κ = 7, λ ≈ 0.3.
   - Add a band paragraph with the table from `score_k7_band.out`, the three calls, the failed predictions and the
     2σ levels.
   - Add the post hoc observation on 34259, labelled post hoc.

3. **§12.8.**
   - Line 38: "it is a spike in B_L: 2.7× and 2.6×" → "it was scored a spike against two equal-λ primes (2.7× and
     2.6×); against the seven-prime band it is not shown (2.6× the median; 34259 at 2.1×)".
   - Lines 41–43: delete the probability sentence and the 2.4× sentence, or mark them superseded.
   - Line 54 (item 3): "the B_L spike at 36037 sits in the not-2+2 part" → "the B_L lift at 36037 sits in the
     not-2+2 part (its split). Whether the high band primes, 34259 in particular, share that is unexamined".

4. **§12.8 gates.**
   - "'κ = 7 has no spike primes'. 36037 is a counterexample in B_L, against two equal-λ primes." → keep the gate,
     but change the reason to: "Undecided. No prime at λ ≈ 0.3 is separated from the seven-prime band at 2σ, and that
     band spreads 4×."
   - "The κ = 7 spread at λ ≈ 0.3, and so the transfer of the κ = 6 calibration to κ = 7 (two primes are not a
     distribution)" → "The κ = 7 spread at λ ≈ 0.3 beyond seven primes. The κ = 6 calibration transfer is refuted
     there (3 of 7 unselected primes exceed κ = 6's unflagged 1.54×)."
   - Add these gates:
     - "36037 is a spike" at κ = 7, in any form beyond the two-prime call;
     - "34259 is a spike";
     - "κ = 7 spikes are rarer, or more common, than κ = 6's";
     - "symR predicts B_L at κ = 7".

5. **STATE.md (lines 80–85, and the summary at line 2643).**
   - Replace "a spike in B_L against two equal-lambda primes … About 2.4x the implied band median, against <= 1.46x
     … Two primes do not give the kappa=7 spread" with: "highest B_L of nine primes at lambda ~ 0.3 (0.635, 2.6x the
     seven-prime band median 0.245); a spike against two equal-lambda primes (pre-registered), but not shown against
     the band (34259 0.519, 2-sigma 0.41-0.61; band 0.131-0.519, 4.0x; R1 NOT SHOWN, R2 INSIDE, R3 rho 0.35
     inconclusive). The kappa=6 calibration does not transfer."
   - Line 90's "Four primes … three separated levels" needs the same update as §0.
   - At line 2643, "36037 is a B_L spike against two equal-lambda primes (pre-registered)" should add "; not shown
     against the seven-prime band (item 6)". If line 2643 is an archived entry rather than live text, leave it.

6. **Obstruction (c).** This does not resolve or worsen it in the sense that matters.
   - In magnitude, the band's spread is small against OSC′'s L tolerance at κ = 7. A 4.0–4.85× spread is
     log₇ = 0.71–0.81, against a tolerance of 1.70 in log_κ (a factor of about 27).
   - Obstruction (c) is about how class values grow with κ, and one κ cannot measure growth.
   - What changes is the framing. At κ = 7, λ ≈ 0.3, the large B_L values are not isolated spikes against a tight
     typical level. So the question "control the spikes" becomes "control the spread", or at least "control the
     upper tail of B_L".
   - Item 3 of §12.8 should say that the not-2+2 question is now posed for 36037 only. 34259 was not split.

7. **Record wording.**
   - Add: "scorer saved 15:26:46, after the results; the rule was applied as written, and the referee reproduced
     the calls by an independent path".
   - Add: "R1 rests on 34259 alone. Without it, 36037 would score SPIKE".
   - Add: "the rule text lists SPIKE before NOT SHOWN, and the scorer tests NOT SHOWN first. That is immaterial
     here, because SPIKE fails."

**Next action, if one is wanted (not run).** The decisive measurement is cheap and bounded: the not-2+2 split of
34259 (`mc_split.py 7 34259 6000 --seed 19`). Pre-register first whether its rest stays ≥ 0.45, as 36037's did, and
whether its 2+2 share is outside 1.1–4.3%. A second seed at 34259 and 34469 would also test whether the 4× spread is
a property of the primes or of the S draws. All the band runs use distinct seeds, so seed sharing is not an issue here.

### Author's disposition of round 4j (11 Nov)

All points accepted. Fixes 1–7 are applied as worded: §0's 36037 bullet and its levels line, the §12.6 supersession
line and the band paragraph (table, calls, failed predictions, credibility, post hoc 34259, obstruction (c)), the
§12.8 class-value bullet, item 3 and the gates, and STATE lines 80–85, 90 and the summary row. The superseded §12.6
passages are marked, not deleted. The record wording on the scorer's timing, R1 resting on 34259, and the clause order
is in §12.6. The suggested 34259 split is proposed as mechanical item 7, not started.

