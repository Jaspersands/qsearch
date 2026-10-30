# A Classical Pilot Sampler With Priced Sign Cancellation

Date: 2026-10-24. Status: local, unreviewed analysis plus an explicit
rational-arithmetic implementation. No quantum algorithm, general degree-gap
theorem, novelty certification or independent review is claimed.

## 1. Question And Decision

Can the canonical HDQI pilot be sampled in the computational basis without
an amplitude oracle? The previous pass estimated its generating function,
but did NOT give samples. This pass provides a different construction:
conditional signed words and noisy rejection with an exactly computable bias.

It gives a polynomial-time classical sampler whenever beta^2 M=O(log m)
for M=sum J_i^2, fixed polynomial accuracy/failure parameters and beta<=1.
This matches the earlier direct quantum spectral preparation comparator's
mass regime. A stronger cluster-derived ratio bound below also covers some
growing-degree families OUTSIDE both the logarithmic-mass and beta*d-small
regimes. Coherent preparation and the subsequent interfering HDQI decoder
are different tasks and are NOT thereby dequantized.

Outside these regimes the sampler may cost exponentially many signed words.
The actual governing ratio can be much better than either upper bound. Its
large upper bound is not a hardness result or quantum advantage certificate.

## 2. Explicit Input And Commuting Envelope

Input: public simple graph G on m vertices, rational 0<=beta<=1,
real rational |J_i|<=1 and canonical independent generators

    O_i=X_i prod_{j<i,j~i} Z_j, H=sum_i J_i O_i.

The target is the computational-basis distribution of

    |pi> = exp(-beta H/2)|0> / sqrt(Z),
    Z=tau(exp(-beta H)), t=beta/2.

There is no hidden source, restricted classical oracle, supplied pilot,
reflection, partition oracle or amplitude oracle. Coupling signs only change
the signs of pilot amplitudes, so sampling may use |J_i|. Put x_i=t|J_i| and

    b_y=prod_i [cosh(x_i) if y_i=0 else sinh(x_i)],
    Z_c=sum_y b_y^2=prod_i cosh(beta J_i),
    q(y)=b_y^2/Z_c.

The proposal is a product law with bit-one probability

    p_i=sinh(x_i)^2 / [cosh(x_i)^2+sinh(x_i)^2].             (1)

Taking absolute values of the exponential word expansion proves
|a_y|<=b_y, where a_y=<y|exp(-tH)|0>. For q(y)>0 define a real signed ratio
r_y by a_y=(known sign)*b_y*r_y, so |r_y|<=1. Then

    mu(y)=C q(y) r_y^2, C=Z_c/Z>=1, E_q r_y^2=1/C.        (2)

The known sign includes (-1)^|y| and signs of the couplings; it disappears
from probabilities. Labels with b_y=0 never occur under q.

## 3. Sampling r_y Without Knowing It

Independently for every i, sample a nonnegative count N_i with parity y_i:

    Pr[N_i=k | k=y_i mod2] = x_i^k / [k! f_{y_i}(x_i)],
    f_0=cosh, f_1=sinh.

Uniformly shuffle the multiset containing N_i copies of each generator.
Apply its generators successively to a label bit mask, accumulating their
canonical signs. The final label is y; the sign sigma is +/-1. Cancellation
of the multinomial shuffle count against the exponential's factorial gives

    E[sigma | y]=r_y.                                     (3)

This costs polynomial work in the sampled word length and graph input.
At x_i<=1/2 the parity-conditioned mean count is uniformly bounded:
x tanh(x) for even parity and x coth(x) for odd parity. We do not repeatedly
sample an unconditioned Poisson until its rare odd event occurs. That would
give bad conditional cost for a tiny x.

## 4. Squaring The Sample Mean Has A Useful Exact Bias

Given y, draw K independent signs and accept the proposal with probability

    A=(sigma_1+...+sigma_K)^2/K^2.

This probability is in [0,1] and is implemented by an exact integer draw.
Crucially it is NOT asserted to be an unbiased estimate of r_y^2. Instead

    E[A|y]=r_y^2+(1-r_y^2)/K.

After acceptance, the law is exactly

    mu_K=(1-alpha) mu + alpha q,
    alpha=C/(K-1+C).                                      (4)

Thus TV(mu_K,mu)<=alpha, and each proposal's success probability is

    a_K=(K-1+C)/(K C)>=1/C.                               (5)

In particular K>=1+C/epsilon gives TV<=epsilon. Sign cancellations and
zero amplitudes are not ignored: at r_y=0, acceptance is 1/K, contributing
precisely to the controlled proposal contamination. Setting K=1 gives q,
not the true pilot. Finite simulations never overwrite this analytic bias.

An unbiased product sigma_1*sigma_2 can be negative and is not an acceptance
probability. Clipping it to zero is also biased and does not implement (2).

## 5. Budget With No Partition Oracle

Redundancy-freeness and the zero trace imply

    1<=Z<=Z_c<=exp(beta^2 M/2).

Hence C<=exp(B), B=beta^2 M/2. For any established nonnegative exponent
bound B_star>=log C, the implementation uses the integer envelope

    C_bar=3^ceil(B_star)>=exp(B_star),

with C_bar=1 at B_star=0. Taking B_star=B always works. This loses a
constant in the exponent, not polynomial
tractability. For eps in (0,1) and delta in (0,1/4], choose

    K=1+ceil(4 C_bar/eps),
    r=ceil(log_2(2/delta)), T=C_bar*r.                     (6)

Make at most T proposals, returning an explicit FAILURE if all are rejected.
Ideal failure probability is <=exp(-T/C_bar)<=2^-r<=delta/2. Conditional on
success before this cutoff the ideal accepted law remains mu_K, since the
independent trials have the same joint proposal/acceptance law. Its TV
bias is at most eps/4. Expected attempts are <=C, bounded worst-case attempts
are T. The random-word count is at most TK, never hidden in a wall clock.

The work is polynomial in m, 1/eps and log(1/delta) for B_star=O(log m), with
the fixed implied constant controlling the polynomial degree. No assertion
of a practical runtime for every polynomially bounded instance is made.

Graph components factor exactly. They may be sampled independently with
allocated eps/delta budgets. This removes artificial exponential penalties
from a product of many individually easy components. The live core accepts
a connected component or a whole graph; component splitting is left as an
explicit optimization in the handoff, not silently included in timings.

### Stronger Sign-Ratio Bound From The Previous Cluster Proof

Let D=d+1, lambda=(beta Jmax)^2 and R=16D lambda. In the previous bundle,
Section 6 proves that the absolute cluster contribution of total set-size
h is at most m R^h/(2D). Suppose D lambda<=1/64, so R<=1/4.

In the expansion of log Z, the clusters whose entire host support is one
vertex sum exactly to sum_i log(1+w({i}))=sum_i log cosh(beta J_i)=log Z_c.
This includes ALL repetitions of that singleton, not just its first-order
term. Every remaining cluster has at least two distinct host vertices and
therefore total size h>=2. Subtract the singleton clusters before taking
absolute values. The earlier bound yields

    0<=log C=log Z_c-log Z
       <= sum_{h>=2} m R^h/(2D)
       = 128 m D lambda^2 / (1-16D lambda) = B_cluster.    (7)

The lower bound is the pointwise commuting envelope, not a claim that each
cluster correction has a particular sign. Use B_star=min(B,B_cluster)
when the cluster condition holds, and B otherwise. For an edgeless graph,
C=1 exactly, so B_star=0 at every beta allowed by the implementation.
These choices are made with exact rational inequalities. This deduction
depends on the earlier LOCAL UNREVIEWED cluster proof, not on a fitted C.

For a concrete asymptotic comparison, let N>=2 be even and take a connected
circulant on m=N^8 vertices, degree d=N^4, unit couplings and
beta=1/(16N^3). Then

    beta*d=N/16, beta^2 M=N^2/256,
    B_cluster=[(1+N^-4)/512] / [1-(N^4+1)/(16N^6)] < 1/128.

Thus beta*d diverges, beta^2 M eventually exceeds every constant multiple
of log m, but C_bar=3 suffices for this sampler at all N. This is an explicit
family with polynomial classical pilot sampling beyond the earlier mass
comparator, not a large numerical experiment or a coherent preparation.
The graph has polynomially many explicit edges; their input/read cost is
charged. No novelty or hardness conclusion follows from this comparison.

## 6. Exact Rational Truncation And Implemented Error Budget

The core uses no floating-point probability calculations. For parity p=0,1,
cancel the factor x^p and use rational unnormalized weights

    w_j=x^(2j) p!/(p+2j)!, j>=0, w_0=1.

If the last retained count is k=p+2j, the omitted mass of these weights is
at most w_j R/(1-R), R=x^2/[(k+1)(k+2)]<1. Stop when this is <=eta.
The true parity law's omitted probability is <=eta, since its normalizer
is >=1. Sampling the normalized retained weights has TV error <=eta.
Integer cumulative weights and `randrange` realize this truncated law.

Write e=cosh x and o=sinh x. Let E be the retained even-weight sum and
O=x times the retained odd-weight sum. Then e-E<=eta and o-O<=x eta.
At x<=1/2, e<2 and o<1, so

    (e^2-E^2)+(o^2-O^2) <=5 eta.

Use proposal probability O^2/(E^2+O^2). Since this removes nonnegative
mass from the exact two-weight proposal with total mass >=1, its TV error
is at most 5 eta. For m bits and K conditionally independent words, one
trial differs from the ideal law by at most m(K+5)eta. Coupling up to T
trials bounds their entire output/failure law by

    zeta=T m(K+5)eta.

The implemented choice is eta=min(eps,delta)/[16 T m(K+5)], so
zeta<=min(eps,delta)/16. The actual failure probability is <=delta/2+zeta
<delta. Both ideal and actual success probabilities exceed 1/2; conditioning
on success changes TV by at most 4zeta. Consequently the returned sample,
conditional on no explicit failure, is within eps/4+4zeta<=eps/2<eps of mu.

All normalization, cutoff, K,T and acceptance decisions are rational/integer
calculations. A cap on preparatory arithmetic or word work must return a
failure, not a fabricated sample. The finite count cutoffs scale with
log(1/eta); their bit costs also charge the input's rational precision.
Very small beta does not cause an underflow or a hidden inverse-beta loop.
The theoretical guarantee assumes independent random bits; seeded PRNG
runs are reproducibility controls, not information-theoretic randomness.

## 7. Attempts To Disprove Or Overextend It

### Bounded Zero-Freeness Does Not Supply Full Sampling

The earlier generating-function theorem controls bounded fields. Results
relating stability to spectral independence require additional hypotheses
that control pinnings; a derivative/positive pin is not covered by simply
substituting zero fields. Chen--Liu--Vigoda, Lemmas 3.1 and 3.3, use an
unbounded zero-free region for automatic differentiation closure:
https://theoretics.episciences.org/13923/pdf . The current sampler bypasses
that inference entirely.

### Dropping The Jordan-Flow Signs Is False

The coefficient anticommutator generator is

    J_H=(H_L+H_R)/2=sum_i J_i O_i (I+prod_{j~i}Z_j)/2.

It flips i only when the occupied-neighbor count is even. Nevertheless
on the graph with edges 01,02,03,12, the legal routes 2,3,0,1 and 1,3,0,2
from vacuum to 1111 have opposite signs. Their closed walk is frustrated;
no diagonal sign gauge makes all edges of this component nonnegative.
This small graph is only a falsifier of that shortcut, not a hard instance.

### No Exact-Amplitude Or Full-Distribution Evaluation In The Core

The core stores adjacency, parity masks and short sampled words, not a
2^m statevector. Dense exponentials occur ONLY in independent small tests.
The upper bound C_bar is sometimes enormous. The code reports K,T and
random-word budgets before execution and refuses an inadequate user-supplied
execution budget without returning a sample. No low success rate is evidence
of quantum hardness.

### What Remains Quantum

The output is a classical bit string. It does not preserve amplitude signs,
coherence, or a decoder's interference. It cannot replace the pilot inside
HDQI as a pure state. The large connected-mass square-root-degree regime
and its thermal weighted gap remain unresolved by this construction.

## 8. Research Decision

The full pilot COMPUTATIONAL-BASIS sampling task in the logarithmic mass
regime is no longer merely suspected easy: this note gives a local,
explicitly priced classical construction, subject to independent scrutiny.
Do not present the earlier quantum mass-regime preparation comparator as
a sampling advantage. Do not build an amplitude-oracle rejection sampler
in its place. The cluster-derived C bound above already extends coverage;
any further probabilistic bound must charge its confidence and arithmetic.

The highest-value remaining question is now the coherent preparation gap
at small beta^2(d+1) but large connected mass, or an explicit physical
decoder/output that uses coherence to outperform the actual comparator.
The sampler is a comparator, not a Shor-level discovery, and no literature
priority is claimed for the rejection/second-moment techniques.
