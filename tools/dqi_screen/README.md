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
| `p`, `b`, `c` | subfield parameters for R4: q = p^b with p prime, and the subfield F_(p^c) with c dividing b; needed when q is not prime, and checked against q when given |
| `classical_witness` | best satisfied fraction a classical method has reached |
| `finite_dqi_mean` | DQI's mean at this finite size, when computed |

## Rules

Notation: Q_Pr = rho + (1 - rho) alpha is Prange completion. Q_DQI(lam, rho) =
(sqrt(lam(1-rho)) + sqrt(rho(1-lam)))^2 is the semicircle law, pinned at 1 once lam > 1 - rho.

| Rule | Kind | Passes when | Formula |
|---|---|---|---|
| R1 | hard | every applicable reach bound exceeds the threshold | lambda_crit = (sqrt((1-rho) Q_Pr) - sqrt(rho (1-Q_Pr)))^2; cosine: lambda_crit_cos = (1 - sqrt(1 - 2 alpha^2))/2 |
| reach | hard | the radius is inside licensed Hamming reach: l <= (d-2)//2 when d is given, and lam <= every reach bound; not saturated (count, lam > 1 - rho) | Singleton alpha/2; distance delta/2; sphere packing H_q^-1(alpha); Plotkin (1 - 1/q) alpha/2 |
| R2 | hard | the radius beats the threshold | lam > lambda_crit (count) or lambda_crit_cos (cosine) |
| R3 | soft | count only: the claimed value (finite mean, else Q_DQI) is at most the existential line | Q* with D_KL(Q* \|\| rho) = alpha ln q when q^alpha rho < 1, else 1 |
| R3-encoder | hard | the encoder is not known | a known encoder caps the margin at 0 |
| R4 | hard | prime field: not applicable; prime power: the claimed value beats the subfield baseline | alpha_sub = min(1, b alpha/c); baseline rho + (1-rho) floor(alpha_sub m)/m; at rho = 1/2 blocked when alpha >= 2c^2/(b^2+c^2) |
| cap | soft | count only: Q_DQI <= q_cap | q_cap = Q_Pr + kappa, kappa = sqrt(u(1-u)) - u, u = alpha/2 (Proposition 8; at most (sqrt 2 - 1)/2) |
| witness | soft | the classical witness is below q_cap - 0.01 | otherwise no licensed radius beats it by more than 0.01 |
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
| `opi_prime_character_r19.json` (q = 2^61 - 1, m = 127, n = 39, l = 19, d = 40) | unknown | witness 0.8583 >= q_cap - 0.01 = 0.8505; restarts need m >= 399.2, m = 127 |
| `opi_prime_character_r32.json` (same, l = 32) | not viable | outside licensed Hamming reach: 32 > (40-2)//2 = 19, lam = 0.252 beyond Singleton 0.1535 |
| `mpi_signed_cosine.json` (q = 8191, m = 6000, n = 420, l = 209) | viable | lam = 0.0348 > lambda_crit_cos = 0.00246, inside Plotkin reach 0.035; restarts need 1594.5 <= 6000 |
| `hermite_half_rate.json` (q = 8191, m = 1000, n = 500, l = 124, d = 250) | unknown | restarts need m >= 1212.7, m = 1000; R4 not applicable (prime field) |

Smoke run on the real checkout (2026-10-21):
`python tools/dqi_screen/screen.py --params tools/dqi_screen/examples/opi_prime_character_r32.json`
exits 1 and the report says "outside licensed Hamming reach".

## What it does not prove

- The rules are asymptotic. A "viable" verdict is not a finite-size certificate; compute the
  finite DQI mean and run `prange_restarts` on the instance.
- Reach is worst-case Hamming decoding only. A list decoder or an average-case decoder beyond
  (d-2)//2 is outside these rules, not refuted by them.
- "unknown" is not "probably fine": read the reasons.
- The cosine objective is cos(2 pi v / q) with values in [-1, 1]. Its semicircle value is
  sqrt(2 lam(1-lam)) (Proposition 13(ii): standard deviation 1/sqrt(2) times 2 sqrt(lam(1-lam))),
  not the 2 sqrt(lam(1-lam)) of a +-1 objective, and it meets Prange's alpha exactly at
  lambda_crit_cos, so R2 passes exactly when the cosine margin is positive. The paper states
  the law for lam <= 1/2; the screen holds the value at 1/sqrt(2) beyond.

Tests: `python -m pytest -q tests/tools/test_dqi_screen.py`.
