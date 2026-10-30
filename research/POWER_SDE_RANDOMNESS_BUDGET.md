# Finite Randomness For The Symmetric Power SDE

**29 October extension:** supplied first-level relations of width m>=r+1
are now preserved and verified. Their root allowance is h*(m+2)+d*(d+1)/2,
not the default h*(r+3)+d*(d+1)/2. The same downstream allocation is recomputed
from that allowance. See [random regular blocks](RANDOM_KERNEL_REGULAR_SDE.md).
Declared stochastic exhaustion is now distinguished from unexpected backend
errors by RandomnessExhausted; the default width and guarantee below remain.

28 October 2026. A bounded, aborting CLASSICAL subroutine for the proposed
receiver. One independent automated adversarial review found no defect
under the promises below. This is not human review, a new root algorithm,
a fully clocked receiver, or a quantum speedup.

## Question And Scope

The [symmetric contraction](POWER_SDE_SYMMETRIC_CONTRACTION.md) uses
`M=(r+1)*((d-1)*r+1)` arbitrary public label columns. Its original mode
caps scalar proposals but delegates root extraction and integer sampling
to potentially unbounded routines. Can ALL its randomized loops be capped
with one uniform failure guarantee, without resampling quantum labels?

Yes, in the same regime: an odd prime p, fixed d>=2 dividing p-1,
`p>=16*d^(2*d+2)`, and at least M columns of compressed rank r. The new
mode either returns an exactly verified nonzero original-coordinate
witness, or ABORTs. With fresh independent fair bits, the probability of
randomness exhaustion is at most `2^(-k)` for every admissible fixed label
matrix. Malformed inputs, broken arithmetic libraries and adversarial
random sources are not probabilistic failures covered by this claim.

Prime validation and deterministic arithmetic have separate dependencies.
The implementation does not certify their bit complexity, count their
machine steps, or impose an OS deadline. The default backend remains the
reference implementation; the bounded mode is explicit and fails closed
outside its proved regime.

## Capped Root Extraction

For nonzero a satisfying `a^((p-1)/d)=1`, the polynomial `X^d-a` has d
distinct roots in F_p. Its derivative has no common root because d<p.
At a current monic factor f of degree m>=2, choose ALL m coefficients of
a polynomial h of degree <m independently and uniformly. Compute

```
g = gcd(f, h^((p-1)/2) - 1).
```

If `0<degree(g)<m`, descend to g; otherwise retry within the stage cap.
This is the known Cantor--Zassenhaus splitting mechanism, not a new
algorithm. See [Sutherland, finite-field arithmetic, Algorithm 3.47 and its derivation](https://ocw.mit.edu/courses/18-783-elliptic-curves-spring-2021/b6d0aef71278ad8c1d8b5144c4138cb7_MIT18_783S21_notes3.pdf).

Evaluation of h at m distinct roots is a Vandermonde bijection. These
values are therefore independent uniforms, including zero. A nonzero
square has probability `a0=(p-1)/(2*p)`; zero belongs to the complement.
The exact proper-split probability is

```
1 - a0^m - (1-a0)^m >= 2*a0*(1-a0) >= 4/9 > 1/3.
```

This argument would NOT justify independent evaluations for a random
linear shift of a degree-m factor. Sampling m coefficients is essential.
There are at most d-1 strict descents. With K trials per stage, abort is
bounded by `(d-1)*(2/3)^K`. There are at most `(d-1)*K` polynomial
power/gcd pairs and `K*(d*(d+1)/2-1)` field draws. The final root is
verified by exact powering against the ORIGINAL a.

`theorems/bounded_power_roots.py` uses a degree-one FLINT field context
with explicit `check_prime=False`, under the externally validated prime
promise. It calls no polynomial factorization/root routine, field-element
enumeration, extension-field construction or hidden random-element API.
The enclosing SDE still performs its ordinary prime validation.

## One Budget For Every Classical Draw

For r>0 write `h=(d-1)*r+1`. The number of root requests is at most

```
R = h*(r+3) + d*(d+1)/2.
```

Indeed, each of h first-level blocks classifies one coefficient before
normalization and at most r+1 afterwards: h*(r+2). The second level
classifies one before and at most h afterwards: h+1. The closure requests
at most `d*(d+1)/2-1` roots since its distinguished coefficient is one.
Caching can only reduce the count. Rank zero needs no randomness.

For requested failure at most `2^(-k)`, choose the following exact integer
budgets (logarithms are ceilings, implemented with integer bit lengths):

```
A = d + R*(d-1)
B = k + 1 + ceil(log2(A))
J = d*B                                  # coset-generator proposals
K = 3*B                                  # root trials per descent
Q = J + sum(j=1..d-1, 2*d^(j+1)*B) + R*d*(d-1)*K
L = k + 1 + ceil(log2(Q))                 # bit-rejection attempts per draw
```

The generator succeeds with probability phi(d)/d>=1/d. Its J failures
cost at most `exp(-B)<=2^(-B)`. Scalar stage j succeeds with probability
at least `1/(2*d^(j+1))`, uniformly over every admissible earlier prefix;
its allocated trials cost at most `2^(-B)`. Each root descent costs at
most `(2/3)^(3*B)<=2^(-B)`. Thus all these failures sum to
`A*2^(-B)<=2^(-k-1)`. No independence between completed stages is assumed.
The scalar bound is proved in the symmetric-contraction note, not inferred
from these finite controls.

At most Q uniform-integer draws occur. For interval width w<=p, use
`b=ceil(log2(w))` fresh bits per attempt, accept integers less than w,
and stop after L attempts. Width one consumes no bits. Acceptance per
attempt is at least 1/2. An accepted single draw is exactly uniform;
its rejection exhaustion is at most `2^(-L)`.

For adaptive calls, use a FIRST-ERROR COUPLING: compare against the same
algorithm with unbounded integer rejection, driven by the same infinite
independent fair-bit tape. Until the first rejection abort the paths are
identical. Conditional on the entire past at a reached call, unused bits
are still independent. A union bound gives

```
Pr[any randomness exhaustion] <= A/2^B + Q/2^L <= 2^(-k).
fair bits consumed           <= Q*L*ceil(log2(p)).
```

Do NOT condition on the entire run succeeding and then assert that its
adaptive draws remain independent uniforms. That conditioning can bias
the paths. No distribution over returned roots is required: every root
only needs to be correct. The implemented exact Fraction bounds also
cover the rank-zero case conservatively, although it uses no random bits.

## Composing With Measured Sources

All solver randomness is independent of the input quantum bank. Its
labels have already been measured. A classical rejection trial uses the
same labels, not new source copies; only after a valid nonzero witness is
selected is the conversion performed. The wrapper never silently restarts
on exhaustion, returns zero weights as success, or redraws labels.

For the exact promised class-three sources, the existing Lean theorem
`ReesMeasuredReceiver.measured_step_output` is pointwise in both labels
and valid witnesses. Let m_lambda be a label branch's probability mass,
q_lambda the solver acceptance probability, and rho' the normalized
target source. The theorem's pointwise identity implies, on paper,

```
rho_success = sum_lambda m_lambda*q_lambda*rho' = alpha*rho',
alpha = sum_lambda m_lambda*q_lambda >= 1-2^(-k).
```

Thus accepted IDEAL source output is exactly rho', even if solver
acceptance biases retained classical labels. This does not erase the
failure probability. Discarding the abort bank and emitting an orthogonal
ABORT flag gives the complete reduced output

```
alpha * |success><success| tensor rho' + (1-alpha) * |abort><abort|.
```

Its trace distance from the always-success ideal output is `1-alpha`.
This statement traces out the label record and refers to the promised
source, not arbitrary-input diamond distance or a reference-entangled
source theorem. It is a written consequence, not newly kernel-verified.
The current Lean averaged receiver still assumes a TOTAL active witness
policy. This aborting implementation does NOT instantiate that premise.

For at most T adaptive solver invocations, allocate local errors delta_t
with `sum_t delta_t<=epsilon_solver`. For a common dyadic target epsilon,
`k=ceil(log2(T/epsilon_solver))` suffices. Charge T over the WHOLE recursive
tree, not just its depth. This raises classical bit/attempt budgets without
extra quantum leaves. Disjoint-bank/source preparation costs remain paid;
consumed quantum targets cannot be reused or cloned. Physical approximate
operations need complete flagged-instrument error bounds of their own.

## Implementation And Falsifiers

```
python qsearch.py power-sde --bounded-randomness --write
```

This writes `research/reductions/power_sde_bounded_randomness.json`.
`budgeted_power_weights` returns the verified witness, exact prior budget,
and actual root/trial/uniform/bit counts. `bounded_randomness_bits=k` is
also accepted by the Bezout controller and both phase-erasure stages.
That explicit option uses the symmetric backend for every nontrivial
supported reduced degree, not the unbudgeted cubic/exterior dispatcher.
Reduced degree one and rank zero remain deterministic. Other nontrivial
field regimes reject instead of falling back silently. Original-degree
equations are checked again after Bezout lifting.

Decisive controls forbid the old root backend, enumerate single-call bit
rejection and small root-splitting distributions, force cap exhaustion,
reject malformed bits, exhaust all d-1 descents, and verify exact original
moments. Weighted tests forbid hidden phase evaluation, check lower output
degree, and retain packets on classical abort. The seeded live fixtures
are reproducibility controls, NOT evidence that the probability bound
holds. Fresh fair bits are a mathematical input assumption.

Remaining blockers: prime/arithmetic implementation refinement; an explicit
failure-aware Lean instrument; the recursive finite call envelope and
physical approximation budget; an implemented quantum receiver; a useful
native application that survives matched classical attacks; and priority
review of the separate symmetric contraction. No result status is promoted.
