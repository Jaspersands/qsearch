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
