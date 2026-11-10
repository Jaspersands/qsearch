### 12.14 Obstruction (c) as a tail question, and its next test (11 Nov) [heuristic; computed; pre-registered; referee rounds 4k-a and 4k-b]

- **Why the spread, not single primes.** OSC′ is a statement for every p ≥ p₀, so §11.8's exponent uses the sup of
  B_L and B_D over the primes near the threshold T(κ), not a typical value.
  - There are N_T ≈ T/(φ(κ) ln T) primes p ≡ 1 (mod κ) in [T, 2T], so log_κ N_T = (1/2 + o(1))κ. It is 3.42 at κ = 7
    and 4.29, 4.74 and 5.53 at κ = 8–10.
  - Write X = B/median(B) across primes at the relevant λ. Under a power tail P(X > x) ≈ x^{−1/γ}, the sup is about
    median·N_T^γ. Under a lognormal tail with log-sd σ, it is about median·exp(σ√(2 ln N_T)).
  - **Finite κ.** Against the rooms log_κ B_L < (1/2 − 1/(2 ln κ))κ − O(1) and log_κ B_D < (1 − 1/ln κ)κ − O(1), a
    power tail uses the whole L room at γ_L ≈ 0.50, 0.48, 0.52 and 0.51 for κ = 7–10, and the whole D room at
    γ_D ≈ 0.99, 0.97, 1.04 and 1.02. Both ignore the O(1)s: an O(1) of 1 would be 60% of κ = 7's L room of 1.70.
  - **Asymptotically** the thresholds become γ_L → 1 and γ_D → 2, since log_κ N_T grows like κ/2 while the L and D
    rooms grow like κ/2 and κ.
  - **Obstruction (c) in spread form: is the tail heavy enough that the sup over N_T primes fills the room?** This is
    a heuristic. It extrapolates a tail fitted on tens of primes out to quantile 1/N_T, and Hill > 0 does not show a
    power tail: a lognormal with σ = 0.45 gives Hill ≈ 0.28.
- **The κ = 6 reference** [computed; `osc-mc/tail_index.py` → `review-2026-11-10/scratch/tail_k6.out`, rerun 09:51]. The table gives
  the spread scale σ_L = sd(ln B_L) and Hill estimates on the top quarter, each with a 95% bootstrap range over primes.

  | λ band | N | σ_L | γ_L (Hill) | γ_D (Hill) | primes with X > 2, L / D | max ratio B_L / B_D |
  |---|---|---|---|---|---|---|
  | [0.19, 0.25] | 29 | 0.49 (0.35–0.60) | 0.46 (0.19–0.68) | 1.43 (0.42–1.89) | 4 / 6 | 3.5 / 23 |
  | (0.25, 0.31] | 31 | 0.35 (0.25–0.43) | 0.33 (0.11–0.49) | 0.83 (0.25–1.26) | 3 / 11 | 2.6 / 15 |
  | [0.49, 0.56] | 29 | 0.24 (0.18–0.29) | 0.23 (0.08–0.32) | 0.73 (0.15–0.99) | 0 / 5 | 1.9 / 5.9 |

  - **The B_L spread grows as λ falls at κ = 6** [computed]. σ_L falls from 0.49 to 0.24 between λ ≈ 0.2 and 0.5,
    with disjoint ranges (about 3.8σ). The tail indices rise only at about 1.1σ (not shown), and the B_D count of
    X > 2 does not rise (6, 11, 5).
  - The threshold path has λ_T(κ) → 0 (0.43, 0.18, 0.07 and 0.02 at κ = 7–10), so the live form of (c) is whether
    the spread keeps growing along the path.
  - Against the finite-κ rooms, κ = 6's γ_L of 0.46 at λ ≈ 0.2 is near the L room, and γ_D of 1.43 is above the D
    room. κ = 6's own log₆ N_T is not computed, and κ = 6's λ_T lies above these bands, so this is an indication,
    not a call.
  - At κ = 7, λ ≈ 0.3, the seven band primes give σ_L 0.46 (0.23–0.60), 1.30× κ = 6's at equal λ (0.61–2.02). Their
    lognormal extrapolation gives log₇ sup B_L ≈ 0.14 (power form −0.23), against the room of 1.70 before the O(1).
    It has two parts: log₇ median = −0.72, measured below λ_T and the same size as the unknown O(1); and the part that
    grows with κ, log₇(sup/median) = 0.86 (power form 0.49), which is half the room. Seven primes are too few to use.
- **The next test** (mechanical item 8; `osc-mc/predictions_k7_tail.txt`, revision 1 after referee round 4k-a,
  written before any run).
  - **Quantity:** σ_L(7) at λ ≈ 0.3, from N = 24 primes. These are the 7 band primes plus 17 drawn as
    `default_rng(2026).choice(pool, 17, replace=False)` from the 30 not yet run, never selected on symR or B_L.
    36037 and 34693 enter only a secondary analysis. 7 of the 24 values were known when the rule was written.
  - Each prime gets `mc_classes.py 7 p 6000` at seeds 31–63 (odd), about 22 core-h in all.
  - **Rule T1′:** take the ratio σ_L(7)/σ_L(6, λ (0.25, 0.31]) = σ_L(7)/0.352, with a 95% range from 2000 independent
    bootstrap pairs. WIDER if the lower end is above 1, NARROWER if the upper end is below 1, otherwise COMPATIBLE.
    σ_L is about 2.7× sharper than Hill (referee simulation), but the power is modest: a spread 1.25×, 1.5× or 2×
    wider is called WIDER about 21%, 53% or 91% of the time.
  - **Reported only:** Hill and the count of X > 2; the extrapolated log₇ sup under the lognormal and power forms,
    against 1.70; γ_D if the top 7 B_D values are resolved.
  - **Predictions:** σ_L(7) in 0.35–0.55, ratio 1.0–1.6, T1′ COMPATIBLE, lognormal log₇ sup below 0.6. The last
    is not independent: it follows from the σ_L prediction unless the median moves (it needs only σ_L < 0.70).
  - **What it decides.** WIDER would be the first evidence that the spread grows with κ at equal λ. COMPATIBLE or
    NARROWER would say it does not between κ = 6 and 7, at this λ only.
  - One κ step cannot measure growth with κ. The decisive version is the same quantity at κ = 8 near
    λ_T(8) = 0.18, which needs the (C1) sampler of §11.9.
- **Limits.**
  - Measurement noise in each B moves Hill by under 2% and does not make the test conservative. It adds to σ_L in
    quadrature. The band primes' per-prime log-sd 1/(2z) is 0.024–0.115 (rms 0.071), which moves 0.352 to 0.359;
    κ = 6's rms is 0.025. So the ratio is inflated by about 1.8%.
  - For outlier-prone values (t₄-like), the percentile bootstrap of an sd gives a false NARROWER about 8% of the time.
  - The 7 band primes came from the symmetric-S table, not from B_L.
  - The λ ≈ 0.3 window is below κ = 7's λ_T = 0.43.
  - The tail form is an assumption: it could be capped (|V| ≤ n), or heavier far out.
- **Claim gates stay false:**
  - obstruction (c) resolved in either direction, and any extrapolated sup as a bound;
  - "κ = 7's tail is no heavier than κ = 6's", or "its spread is no wider", from a COMPATIBLE;
  - "within budget at κ = 7" from any extrapolation;
  - "the κ = 6 tail index grows as λ falls" as a fact (the σ_L rise is resolved; the Hill rise is not);
  - "γ > 0 shows a power tail".
