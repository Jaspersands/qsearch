# OPI Filter Tails Without An Exponential State

2026-10-17. Local moment extension and certificates, review pending. Known
DQI mechanism; no new quantum algorithm, hardness result or cost separation.

## The Scientific Gap

The [cubic-target controls](EXPLICIT_CUBIC_OPI.md) have classical best-of-four
scores above a known quantum mean. That is not a comparison of success
probabilities. The next question is whether we can bound the NATIVE filter
tail without assuming a convenient full score distribution or enumerating
all 2^(Kt) RS messages.

## Exact Moment Argument

Let S be the number of accepted coordinates for a UNIFORM RS message. Any
K positions of a dimension-K RS code are independent uniform field symbols,
by the Vandermonde interpolation map. Every fixed balanced predicate then
gives a fair bit at those positions. Consequently E[Q(S)] equals the
Binomial(N,1/2) expectation for every polynomial Q of degree at most K.
No IID predicate ensemble or oracle distribution is needed for this fact.

Use a degree-ell filter P(S). Its ideal DQI probability on a message is
proportional to P(S)^2. The normalization and r-th score moment are therefore
exactly known whenever 2 ell+r <= K. With K_j the unnormalized Krawtchouk
polynomials, choose an EXPLICIT rational filter

```
P(s) = sum_j b_j K_j(s),   b_j rational
Z = sum_j b_j^2 * C(N,j)
E_filtered[(S/N)^r]
  = sum_s C(N,s)/2^N * P(s)^2 * (s/N)^r / Z.
```

The code approximates the known positive mean-filter coefficients with exact
dyadic inverse-square-root factors. It certifies THIS rational polynomial,
not an exactly optimal eigenvector. All sums and moments are rational.
The sum has only N+1 terms, not 2^(Kt) messages.

CRITICAL: the expression on the right computes the permitted moments, NOT
the full native score distribution. Beyond the degree cutoff, code relations
can radically change the distribution. The countercontrol K=1 with identical
predicates has native score either zero or N, not a binomial distribution.
The maximum mean filter at K=39,ell=19 allows only ONE certified moment.
Claiming its variance from the binomial surrogate would be an error.

The [known DQI score/state construction, Appendix A](https://arxiv.org/html/2610.02145v2#A1)
supplies the filter mechanism and distance context. The higher-moment identity
here follows from the explicit interpolation argument; no novelty claim is made.

## Independently Verifiable Tail Bounds

For a threshold k, a numerical moment LP proposes coefficients of a polynomial
q(x) below 1[S>=k] on the finite support x=s/N. Every coefficient is converted
to a rational number. An EXACT support-wide constant repair removes any
numerical infeasibility. The code then verifies

```
q_lower(s/N) <= 1[s>=k] <= q_upper(s/N),   s=0,...,N.
```

Taking certified moment expectations gives rational lower and upper bounds.
No numerical LP optimum is trusted or claimed certified. Failed numerical
optimization gives valid trivial [0,1] bounds, not a research finding.
The saved dual polynomials are checked without rerunning the numerical solver.
One, four and sixteen ideal independent executions have outward-rounded
dyadic success bounds. These are ATTEMPT counts, not matched gate budgets.
An approximate compiled circuit would need its own trace-error allowance.

## Live Findings

At N=127,K=39:

| Filter degree | Certified moments | Mean | Guaranteed Pr[S>=102] |
| --- | --- | --- | --- |
| 16 | 7 | 0.789980 | >=0.022620 |
| 18 | 3 | 0.808256 | >=0.178033 |
| 19 | 1 | 0.816830 | >=0.105285 |

For degree19, Pr[S>=104] >=0.0307255 for EVERY balanced input of the stated
RS form, including the two compact cubic instances. Degree18 also gives a
positive lower bound at104. These are not empirically measured probabilities.
At105 the implemented moment certificates give zero as the lower bound:
UNKNOWN, not zero actual success. Upper bounds remain broad. The lower-degree
filter's better certified102 tail is not proof that its actual tail is better;
the degree19 moment relaxation has less information.

Thus classical105/127 and104/127 remain verified witnesses but do NOT kill
the quantum tail. Conversely, a universal known-algorithm tail guarantee does
not make the explicit input family classically hard, nor supply a new algorithm.
The relevant unresolved comparison is success at a shared threshold under a
charged full-work budget, with stronger adaptive classical attacks retained.

## Run And Review

```
python theorems/opi_filter_tail_certificate.py --write
python -m pytest tests/test_opi_filter_tail_certificate.py -q -W error::RuntimeWarning
```

The report binds its producer, both OPI dependencies and cubic input artifact
by SHA256. Tests compare ALL allowed moments and tail bounds against complete
small native-field enumeration; reject forbidden higher moments, corrupted
dual polynomials and repetition arithmetic; and check numerical-failure and
infeasible-dual countercontrols. This validates the implementation, not the
unreviewed mathematical premises or an actual coherent decoder/filter.

Do not add mean/tail labels to a speedup registry entry. CLI exposure and
production regressions are mechanical follow-up. A new scientific pass needs
an adaptive code-aware classical mechanism, a constructive quantum resource
improvement, or an independent higher-upside algorithmic route, not more
filter/seed scans of these already understood finite controls.
