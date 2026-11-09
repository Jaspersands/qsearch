# Draft for review (round 4): final κ = 6 survey and the scored predictions

Part A is a new §12.10 for the topic note. Part B lists the in-place changes to §12.1–12.9, and Part C the changes to
the handoff, STATE and the mechanical plan.

## Part A: new subsection

### 12.10 Final survey and the scored predictions (10 Nov, 04:49) [computed; the scoring is pre-registered]

- **Run.** All 89 primes had finished by 04:49 (`k6_spike_survey.out`). The scoring script is
  `survey/score_predictions.py`, with output in `survey/score_predictions.out`. It uses the flags and bands of
  `k6_spike_survey.py`. Nothing changes at λ ≤ 0.25.

  | λ band | primes | median B_L / B_D / PW_pair / N₁/μ₁ | max B_L, B_D (p) | max PW_pair | flagged |
  |---|---|---|---|---|---|
  | 0.197–0.218 | 14 | 0.50 / 0.82 / 2.81 / 0.97 | 1.88, 10.5 (1657) | 30.1 | 6 (§12.2) |
  | 0.222–0.249 | 15 | 0.55 / 0.59 / 1.77 / 0.82 | 1.77, 14.8 (1789) | 31.7 | 3 (§12.2) |
  | 0.251–0.307 | 31 | 0.45 / 0.44 / 1.04 / 0.81 | 1.16, 6.59 (2113) | 11.1 | 8: 2053 sD sPW; 2113 sD sPW sN; 2137 sD; 2143 sD sPW sN; 2179 sD; 2221 sD sPW; 2269 sD sPW; 2341 sD sPW sN |
  | 0.492–0.553 | 29 | 0.33 / 0.24 / 0.32 / 0.80 | 0.63, 1.42 (3889) | 0.89 | 4: 3823 sD sPW; 3889 sD sPW; 4057 sPW; 4129 sD sPW |

- **Spikes.** 21 of the 89 primes are flagged.
  - Amplitude falls as λ rises. The largest B_D is 14.8, 6.6 and 1.4 at λ ≤ 0.25, 0.25–0.31 and ≈ 0.5. The largest
    PW_pair is 32, 11 and 0.89.
  - In (0.25, 0.31] the largest spikes are 2113 (B_D 6.6, z 3.7; PW_pair 11.1; N₁/μ₁ 2.06) and 2269 (B_D 5.4, z 3.3;
    PW_pair 8.0; N₁/μ₁ 0.87).
  - At λ ≈ 0.5 every prime has debiased PW_pair below 1. The largest is 0.89, at 3889, whose CS upper estimate is
    1.01. In (0.25, 0.31], 13 of the 31 are below 1 (7 by the CS upper estimate). At λ ≤ 0.25 none is. These are
    Monte Carlo estimates, not certificates.
  - The smallest N₁/μ₁ in the survey is 0.37 (1741), so B ≈ 2.7 in (N) covers all 89 primes.
- **N₁/μ₁ predictions** (`survey/predictions_N1mu1.txt`, 01:20).
  - Log errors:

    | primes | n | rms | mean | largest |
    |---|---|---|---|---|
    | later primes, λ ≤ 0.25 | 15 | 0.24 | +0.04 | +0.37 (1879) |
    | (0.25, 0.31] | 31 | 0.19 | +0.04 | +0.44 (1951) |
    | λ ≈ 0.5 | 28 | 0.13 | +0.05 | −0.26 (3889) |

    The in-sample residual sd was 0.20.
  - So the symR law predicts N₁/μ₁ to about 20% at all 74 later primes.
  - The λ ≈ 0.5 primes sit at 3877's λ, so they test the symR slope there, not the λ-term. The (0.25, 0.31] band
    tests the interpolation between λ 0.21 and 0.5.
  - Spearman of symR with N₁/μ₁ is 0.92, 0.80 and 0.82 at λ ≤ 0.25, 0.25–0.31 and ≈ 0.5.
- **Hypothesis H** (`survey/predictions_hclass.txt`, 02:16).
  - The sets:
    - test set: the 70 primes whose npz was written after 02:16, less 1933;
    - formation set: the 17 primes written by 02:16 (1531–1753, less 1741 and 1759);
    - 1759 is in neither.
  - **(H1)**, that every new sD prime is ≡ 1 (mod 12), is **refuted**.
    - 2143 (≡ 7, λ 0.276) is sD: B_D 1.28, z 6.4, 2σ lower end 1.07 against the threshold 0.89.
    - 2179 (≡ 7) and 3823 (≡ 7, λ 0.49) are flagged at the threshold: lower ends 0.89 against 0.89, and 0.50 against
      0.48.
    - All three B_D values stay above the threshold leaving out any two of the 16 batches, and every batch contributes
      positively (`review-2026-11-10/scratch/leaveout_BD.py`).
    - So H as pre-registered is refuted.
  - **(H2) holds** in both bands that qualify:
    - (0.25, 0.31]: class medians 0.92 against 0.34 (15 and 16 primes, one-sided Mann–Whitney 0.006);
    - λ ≈ 0.5: 0.36 against 0.12 (13 and 16 primes, 0.012).
  - **(H3) holds.** The new sN spikes are 1789, 2113 and 2341 (≡ 1) and 2143 (≡ 7).
  - Over the 70 test primes, the one-sided Mann–Whitney of B_D by class gives 0.0002 (medians 0.61 against 0.32).
  - So the test confirms that B_D is shifted towards p ≡ 1 (mod 12). It refutes the strict form, value spikes only at
    p ≡ 1 (mod 12). No mechanism is known.
  - Post hoc:
    - B_D > 2 still occurs only at p ≡ 1 (mod 12): 8 of 43 primes against 0 of 46. Three of the 8 are test primes
      (1789, 2113, 2269). The largest B_D at p ≡ 7 (mod 12) is 1.28 (2143).
    - The count spikes without value spikes are still 1531, 1627 and 1759, all ≡ 7 (mod 12). 1951 is not flagged
      once its band is complete.
    - At λ ≤ 0.31 the class medians are N₁/μ₁ 1.04 against 0.67 and B_D 0.93 against 0.47 (30 primes each).

## Part B: in-place changes to §12.1–12.9

1. §12.1, "Status: interim …" becomes: "Status: complete. The tables in §12.2–12.8 were written from the 35-prime
   snapshot of 03:45 (`review-2026-11-10/survey_snapshot.out`). The final run (04:49, all 89 primes) changes nothing at
   λ ≤ 0.25. The completed bands and the scored predictions are in §12.10."
2. §12.2 table: replace the row "0.251–0.31 (6 of 31 so far) … provisional: 1951 sN" with the final band-3 row, add
   the λ ≈ 0.5 row, and drop the "earlier: 2347" row. 2347 is now a typical band-3 prime at seed 13 (B_L 0.41, B_D
   0.43, PW_pair 0.84).
3. §12.2 "What holds means": after "The first value below 1 is at 2011 (λ 0.259, PW_pair 0.92)", add "At λ ≈ 0.5 all
   29 primes are below 1 (§12.10)."
4. §12.3 prospective test: after the "6 primes above λ = 0.25" bullet, add "Final (§12.10): rms 0.19 over all 31
   primes in (0.25, 0.31] and 0.13 over the 28 at λ ≈ 0.5."
5. §12.7:
   - The "Pre-registered predictions …, interim" bullet and its three sub-bullets become: "Pre-registered predictions,
     scored in §12.10: (H1) is refuted by 2143 (≡ 7 mod 12, sD). (H2) and (H3) hold, and the class shift of B_D has
     one-sided Mann–Whitney 0.0002 on the 70 test primes."
   - "Over all 35 finished primes it is 6 of 17 against 0 of 18" becomes "Over all 89 primes, B_D > 2 is 8 of 43
     against 0 of 46 (post hoc)".
   - "(1531, 1627, 1759, and provisionally 1951)" becomes "(1531, 1627 and 1759)".
   - "are scored when the survey finishes" becomes "are scored in §12.10".
6. §12.8:
   - The Answer gets a bullet: "Over all 89 primes (§12.10), 21 are spikes. Spike amplitude falls with λ (largest
     B_D 14.8, 6.6 and 1.4; PW_pair 32, 11 and 0.89), and at λ ≈ 0.5 every prime has PW_pair below 1."
   - The gate "Hypothesis H, or the |a|/√p and cubic-character correlations, as claims" becomes "Hypothesis H (refuted
     in its strict form; the class shift of B_D is confirmed prospectively but has no mechanism), or the |a|/√p and
     cubic-character correlations, as claims".
7. §12.9: "Finish the survey" becomes "Done (§12.10)".

## Part C: handoff, STATE, mechanical plan

- **Handoff, my 2026-11-10 entry.**
  - "It is INTERIM: 35 primes were done at 03:45 …" becomes "It is complete (89 primes, 04:49, §12.10)."
  - The Arithmetic bullet gets: "Pre-registered scoring: (H1) refuted by 2143 (≡ 7, sD); (H2) and (H3) hold; class
    shift of B_D, Mann–Whitney 0.0002 on 70 test primes."
  - Add: "symR predicts N₁/μ₁ prospectively, with rms log error 0.13–0.24 at all 74 later primes."
  - "Next command": the survey scoring is done. The next command becomes the 35099 comparison (running), then
    mechanical item 2 (F over the survey).
- **STATE.**
  - The live-obstruction bullet's "The kappa=6 survey is INTERIM; lambda <= 0.25 is complete (29 primes)" becomes
    "The kappa=6 survey is complete (89 primes)".
  - Add: "Pre-registered: H1 (B_D spikes only at p = 1 mod 12) refuted by 2143; the class shift (H2) holds,
    MW 0.0002."
  - Next: drop "finish the kappa=6 survey …".
- **Mechanical plan, item 1:** DONE (§12.10).
</content>
</invoke>
