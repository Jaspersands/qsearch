# DQI candidate screener

Screens a Decoded Quantum Interferometry (DQI) candidate against the soundness rules of
Mazumder and Niroula, *Discovering New Problems for DQI* (arXiv:2610.06753). It answers the
question the low-rate prime-character OPI line spent weeks on: can this decoding radius beat
Prange completion at all, and is the radius one a decoder is licensed to reach?

The answer is a verdict with the failing rule named:

- **not viable**: a hard rule fails;
- **unknown**: an input is missing, or a soft rule flags;
- **viable**: every rule passes or does not apply.

```bash
python tools/dqi_screen/screen.py --params tools/dqi_screen/examples/opi_prime_character_r19.json
python tools/dqi_screen/screen.py --objective count --q 7 --m 100 --n 30 --rho 0.5 \
    --radius 5 --min-distance 20 --decoder-known
python tools/dqi_screen/screen.py --params cand.json --json --out screen.json
```

Exit codes: 0 viable or unknown, 1 not viable, 2 bad input. Flags override the fields of
`--params`. The same screen is the `screen_dqi_candidate(params)` tool on the corpus MCP
server (`tools/corpus/mcp_server.py`); bad input returns `{"error": ...}`.

## Inputs

| Field | Meaning |
|---|---|
| `name` | label for the report |
| `objective` | `count` (satisfied constraints) or `cosine` (sum of cos(2 pi v / q) over the rows) |
| `q`, `m`, `n` | field size (a prime power), constraints, variables; alpha = n/m |
| `rho` | accepted density of each constraint |
| `radius` | claimed decoding radius l; lam = l/m |
| `min_distance` | minimum distance d of the decoded code, when known; delta = d/m |
| `decoder_known` | an efficient decoder reaches `radius` |
| `encoder_known` | the planted encoder is known |
| `p`, `b`, `c` | subfield parameters for R4: q = p^b with p prime, and c the largest, over the accepted sets, of the smallest F_p-codimension of an affine subspace inside the set (Proposition 9); 1 <= c <= b, and c >= log_p(1/rho) since a set of density rho holds at most rho p^b elements (Appendix A.6). Needed when q is not prime, and checked against q when given |
| `classical_witness` | best value a classical method has reached: a satisfied fraction in [0, 1] (count), or a mean cosine in [-1, 1] |
| `finite_dqi_mean` | DQI's mean at this finite size, when computed; same range as the witness |

Required fields may not be null, and an integer field sent as a float must be below 2^53 (a
larger float cannot hold every integer, so `q = 2^61 - 1` has to be sent as an exact integer).

## Rules

Notation: Q_Pr = rho + (1 - rho) alpha is Prange completion. Q_DQI(lam, rho) =
(sqrt(lam(1-rho)) + sqrt(rho(1-lam)))^2 is the semicircle law, pinned at 1 once lam > 1 - rho.

| Rule | Kind | Passes when | Formula |
|---|---|---|---|
| R1 | hard | every applicable reach bound exceeds the threshold | lambda_crit = (sqrt((1-rho) Q_Pr) - sqrt(rho (1-Q_Pr)))^2 against Singleton alpha/2, distance delta/2, sphere packing H_q^-1(alpha), Plotkin (1 - 1/q) alpha/2; cosine: lambda_crit_cos = (1 - sqrt(1 - 2 alpha^2))/2 against the signed packing reach, the lam <= 1/2 with (H_2(lam) + lam)/log_2 q = alpha (Proposition 13(i)) |
| reach | hard | count: the radius is inside licensed Hamming reach: l <= (d-2)//2 when d is given, and lam <= every Hamming reach bound; not saturated (lam > 1 - rho). Cosine: the radius is inside the signed packing radius | cosine: the largest l with C(m, l) 2^l <= q^n, so the {+-1} patterns of weight l have distinct syndromes; a Hamming licence (d-2)//2 covers signed patterns but does not cap them |
| R2 | hard | the radius beats the threshold | lam > lambda_crit (count) or lambda_crit_cos (cosine) |
| R3 | soft | the claimed value (finite mean, else Q_DQI or the cosine value) is at most the existential line Q* | count: Q* with D_KL(Q* \|\| rho) = alpha ln q when q^alpha rho < 1, else 1 (Definition 5); cosine: the largest mean of cos(2 pi v/q) within relative entropy alpha ln q of uniform, by exponential tilting (Proposition 13(iii); 0.726 for MPI) |
| R3-encoder | hard | the encoder is not known | a known encoder caps the margin at 0 |
| R4 | hard | prime field: not applicable; prime power: the claimed value beats the subfield baseline | alpha_sub = min(1, b alpha/c); baseline rho + (1-rho) floor(alpha_sub m)/m; at rho = 1/2 blocked when alpha >= 2c^2/(b^2+c^2) |
| cap | soft | count only: Q_DQI <= q_cap | q_cap = Q_Pr + kappa, kappa = sqrt(u(1-u)) - u, u = alpha/2 (Proposition 8; at most (sqrt 2 - 1)/2) |
| witness | soft | the classical witness is below DQI's claimed value (finite mean, else Q_DQI or the cosine value) and, for the count, below q_cap - 0.01 | otherwise the classical method already reaches DQI's claim, or no licensed radius beats it by more than 0.01 |
| restarts | soft | m >= the restart length | (1-alpha) R^2 ln(N/eta) / (2 mu^2), R = 1 count / 2 cosine, N = 2^40, eta = 0.05 (Theorem 10) |

mu is the finite margin (`finite_dqi_mean` minus Prange) when given, else the asymptotic one
(Q_DQI - Q_Pr, or sqrt(2 lam(1-lam)) - alpha for the cosine). With mu <= 0 no length suffices.
A cosine candidate with alpha >= 1/sqrt(2) has no threshold and is not viable. A check that is
"not applicable" does not affect the verdict; one waiting for an input ("give radius",
"give p, b, c", or `decoder_known` false) makes it unknown. Count-only quantities are `-` for
a cosine candidate and the other way round. The report also lists rho_crit(alpha) =
(1 - sqrt(2(1-alpha)/(2-alpha)))/2, the density below which lambda_crit exceeds alpha/2.

`prange.py` gives the finite-length baseline on an actual instance:
`prange_restarts(B, accepted, q, restarts, seed)` runs best-of-N Prange completion over a
prime field on Python ints (exact for q = 2^61 - 1) and returns the best and every score.

## The four examples

| Example | Verdict | Why |
|---|---|---|
| `opi_prime_character_r19.json` (q = 2^61 - 1, m = 127, n = 39, l = 19, d = 40) | unknown | witness 0.8583 >= finite DQI mean 0.8168 and >= q_cap - 0.01 = 0.8505; restarts need m >= 399.2, m = 127 |
| `opi_prime_character_r32.json` (same, l = 32) | not viable | outside licensed Hamming reach: 32 > (40-2)//2 = 19, lam = 0.252 beyond Singleton 0.1535 |
| `mpi_signed_cosine.json` (q = 8191, m = 6000, n = 420, l = 209) | viable | lam = 0.0348 > lambda_crit_cos = 0.00246; signed packing reach 0.196 (Table 3), radius 209 inside the signed packing radius 1178; restarts need 1594.5 <= 6000 |
| `hermite_half_rate.json` (q = 8191, m = 1000, n = 500, l = 124, d = 250) | unknown | restarts need m >= 1212.7, m = 1000; R4 not applicable (prime field) |

Smoke run on the real checkout (2026-10-21):
`python tools/dqi_screen/screen.py --params tools/dqi_screen/examples/opi_prime_character_r32.json`
exits 1 and the report says "outside licensed Hamming reach".

## What it does not prove

- The rules are asymptotic. A "viable" verdict is not a finite-size certificate; compute the
  finite DQI mean and run `prange_restarts` on the instance.
- Reach is worst-case decoding: of Hamming errors for the count objective, of signed {+-1}
  error patterns for the cosine (Proposition 13: the Hamming-based Singleton, sphere-packing,
  Plotkin and distance bounds do not limit signed reach, so for the cosine they are only
  listed). A list decoder or an average-case decoder beyond these is outside the rules, not
  refuted by them.
- "unknown" is not "probably fine": read the reasons.
- The cosine objective is cos(2 pi v / q) with values in [-1, 1]. Its semicircle value is
  sqrt(2 lam(1-lam)) (Proposition 13(ii): standard deviation 1/sqrt(2) times 2 sqrt(lam(1-lam))),
  not the 2 sqrt(lam(1-lam)) of a +-1 objective, and it meets Prange's alpha exactly at
  lambda_crit_cos, so R2 passes exactly when the cosine margin is positive. The paper states
  the law for lam <= 1/2; the screen holds the value at 1/sqrt(2) beyond.

Tests: `python -m pytest -q tests/tools/test_dqi_screen.py`.
