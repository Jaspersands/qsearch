# Explicit Cubic-Target OPI: A Structural Classical Falsifier

2026-10-17. Local derivations, review pending. No new quantum algorithm,
hardness proof, oracle problem or admitted speedup candidate.

## Scientific Question

Does replacing quadratic targets by public cubic circuits remove the large
accepted affine flats exploited by the previous classical attack, or does a
constructive polarization attack still erase the finite mean-score comparison?
The previous quadratic result was progress, not a reason to keep varying its
seeds. Dense symmetric cubics are not an escape: e3=e1*e2 in the Boolean ring.

Input: a scalar Reed-Solomon evaluation code of dimension K at the distinct
nonzero field elements represented by integers 1,...,N in F_(2^t), with
N <= 2^t-1. The FLINT irreducible polynomial and coefficient basis are saved.
Each position supplies a public invertible binary matrix T_i and a public
Boolean polynomial g_i in t-1 variables of degree AT MOST three:

```
z = T_i y
accept_i(y) iff z0 = g_i(z1,...,z[t-1]).
```

All constant, linear, quadratic and cubic coefficients are sampled. Degenerate
polynomials, bad attack attempts and all predeclared sources are retained.
Balance is exact for every input, not a typical-source assertion. The input
description is O(N t^3) bits; classical and quantum algorithms see the SAME
description. No membership table, hidden advice or hard oracle is supplied.
In particular t=31,N=31 does not require materializing a 2^31-entry predicate.

## Constructive Quantum Route And Its Limits

Use the KNOWN balanced-DQI polynomial filter and conventional coherent unique
decoding of the RS dual. Each local Boolean phase is implementable by public
linear gates and bounded-control monomial gates, with O(t^3) predicate work.
An indexed implementation can scan the public descriptions in polynomial
work; no unit-cost QRAM is assumed. Field arithmetic, support preparation,
decoder reversibility and precision must all be charged in an actual circuit.
The retained degree ell obeys the STRICT condition 2 ell+1 < K+1.

The existing rational-filter score enclosure is reused for finite comparisons.
The known optimal layered mean approaches 1/2+sqrt((R/2)(1-R/2)) at fixed
rate R=K/N when ell/N approaches R/2; this is not an asymptotic certification
of the implementation's fixed-denominator rational rounding convention.
This is a known constructive theoretical target, NOT our executed circuit or
certified resource advantage. A major computational separation would require
classical hardness for this explicit family, not the random-oracle theorem.
No such hardness evidence exists here. A best-of-four classical score versus
a one-shot quantum mean is NOT a matched time/tail comparison.

Primary reference: [balanced folded DQI, score law and phase implementation,
Appendix A](https://arxiv.org/html/2610.02145v2#A1). Its oracle lower bound is
not transferred to these compact predicates.

## Stronger Classical Attack

For a Boolean cubic g, the third finite difference
T(v,w,a)=Delta_v Delta_w Delta_a g is an alternating trilinear form.

1. Build independent directions v_1,...,v_d with T zero on every triple.
   Each extension is a Gaussian nullspace problem: T(v_i,v_j,v)=0.
2. Solve LINEAR affine-base equations
   T(v_i,v_j,a)=Delta_vi Delta_vj g(0). Inconsistent bases trigger charged
   retries and then smaller dimension. They are not an OPI UNSAT result.
3. The restriction g(a+sum s_i v_i) is now affine. Lift its graph to an
   accepted d-flat in the transformed symbol coordinates. Check EVERY point
   in this small flat, derive its parity checks, and compose with the actual
   binary RS evaluation map.
4. Interpolate inside successive accepted flats using exact binary Gaussian
   elimination. Keep all failures; never select a favorable new source.
5. On the remaining affine message space, recover each restricted degree-3
   polynomial by at most sum_(j<=3) C(d_free,j) evaluations. A Boolean Mobius
   transform evaluates all 2^d_free messages. Optimize the full native score,
   not merely the forced prefix. Verify the winner with independent FLINT
   Horner evaluation, not the binary surrogate used by the optimizer.

All contractions, flat polynomial evaluations, Gaussian solves, residual
candidates, transform XOR cells, table storage and native checks are exposed.
The residual enumeration is exponential in d_free, not a free polynomial-time
subroutine. Caps return UNKNOWN with a verified uniform affine fallback.
There is no maximum-flat, global optimum, mixing or attack-success theorem.
The default requested local dimension obeys C(d,2)+d <= t-1; this avoids
assuming a generically full-rank base system where rank is impossible.

Finding constant/low-degree restrictions is established prior art, not a new
idea: [Cohen and Tal, Sections 3-4](https://arxiv.org/abs/1404.0654), and
[Boyar and Find, algebraic thickness and normality](https://arxiv.org/abs/1410.1318).
The implementation here directly exploits the public cubic tensor and graph
lift; no claim that it improves those theorems is made.

## Why The Quadratic Rank Argument Does Not Automatically Transfer

For an IID uniform RM(3,t-1) coefficient vector, its restriction to any
d-dimensional base flat is a uniform RM(3,d) polynomial. A graph-flat projects
injectively to a base flat, and there are 2^(d+1) possible affine graph heights.
Thus, with [m choose d]_2 the exact Gaussian binomial and
D3(d)=sum_(j=0)^min(3,d) C(d,j), the first moment gives

```
Pr(any accepted d-flat among N predicates)
 <= min(1, N * 2^t * [t-1 choose d]_2 * 2^(-D3(d))).
```

This counts ARBITRARY affine flats, not just the constructor's restricted
search. Invertible T_i preserve dimensions. For sufficiently large t, a
constant-fraction-dimensional flat is unlikely in the stated coefficient
ensemble. This is only a geometric obstruction to the previous attack's
particular large-flat premise. It does NOT prove OPI hardness or eliminate
nonlinear, global, decoding, differential or code-aware classical algorithms.
The seeded examples are not IID probability certificates. Small t=3,d=2 is
independently calibrated against all sixteen Boolean polynomials.

## Execution And Falsifiers

```
python theorems/explicit_cubic_opi.py --write
python -m pytest tests/test_explicit_cubic_opi.py -q -W error::RuntimeWarning
```

Predeclared controls: (t,N,K)=(4,7,3),(15,31,9),(31,31,9),(31,127,39),
seeds 29 and 71, four paid attacks each. The first is an exact calibration,
not an algorithmic result. Saved specifications permit native witness replay.

Falsifiers: verified classical scores erase the claimed mean-score target;
larger native flats or residual optimizers make the finite comparison easy;
or the apparent quantum route needs uncharged preparation/readout work.
Absence of a successful attack is NOT a hardness certificate. Even beating
these classical implementations would leave matched resources, tail laws,
stronger classical algorithms and an actual quantum implementation unresolved.

## Live Results

Both seeds retained, four paid attempts each:

| t,N,K | Best classical scores, seeds 29/71 | Known chosen-filter mean |
| --- | --- | --- |
| 4,7,3 | 7/7, 7/7 | 0.688982 |
| 15,31,9 | 27/31, 27/31 | 0.747358 |
| 31,31,9 | 30/31, 30/31 | 0.747358 |
| 31,127,39 | 105/127, 104/127 | 0.816830 |

At 127 positions each attempt forces 50 accepted predicates, leaves nine
free bits, and exactly optimizes 512 residual messages. At t=31,N=31 it
forces eleven predicates and enumerates 32,768 messages per attempt. All
32 attempts finish below the residual cap; every attempt and native witness
is saved, not just the winners. Flat construction and four-trial selection
are charged. There is no finite best-score advantage in these comparisons,
but the test has NOT matched quantum repetition, tails or runtime.

## Why This Does Not Settle The Asymptotic Question

The producer also records a scoped exact IID-model tail bound. Suppose the
union of candidate message pools is determined using only the first E
predicate polynomials, BEFORE the remaining scores are seen, and has at most
S messages. Uniform independent suffix constants make each fixed message's
suffix score Binomial(N-E,1/2). Whatever dependencies exist BETWEEN messages,

```
Pr(best pool score >= k) <= min(1, S * Pr(Binomial(N-E,1/2) >= k-E)).
```

Allow all exposed predicates a free success. The maximum stopping prefix
over the fixed four attacks is a stopping time; conditioning on that prefix
leaves the suffix polynomials independent. Residual optimization may use all
suffix scores to SELECT a winner, but may not change the previously fixed
pool. Unused terminal flats and failed interpolations count as exposed.
This is not an empirical confidence bound for seeded sources. At the present
sizes it can be vacuous; that is recorded rather than converted to hardness.

Conditional asymptotic interpretation: if E/N -> R and log S=o(N), this attack
cannot beat (1+R)/2 by a constant with nonvanishing IID-model probability.
For 0<R<1 the known DQI target is strictly above that limit, since
R/2-R^2/4 > R^2/4. The premise is plausible for a full-rank prefix of flats
of dimension O(sqrt(t)), with t=Theta(log N) and polynomial-sized residual
pools. A uniform constructor/rank analysis and an extension beyond this
reference's finite field/dimension caps are NOT supplied. If many failures
expose most predicates or a new repair adapts pools using suffix information,
the premise fails and this bound cannot be used against that algorithm.

Thus the observed finite win does not prove asymptotic dequantization, and
an asymptotic weakness of THIS pool would not prove classical hardness.
Both mistakes would manufacture a result from the same limited evidence.

## Next Decision

Do not spend main-model research on more seed/degree/field-size scans. The
concrete next classical challenge is a code-aware NONLINEAR repair that can
change pools using the remaining predicates, rather than paying exponentially
for a released large flat. The quantum challenge is a charged decoder/filter
resource analysis and a matched tail comparison, not a new oracle promise.
Compare that work against independent constructive directions before extending
this line. CLI wiring and production-wide regression are mechanical follow-up;
no central candidate admission, generic negative result or proof promotion.
