# Weighted moments and sampled-oracle admission

2026-11-06. Two independently actual-text reviewed admission tests for the
native character-polynomial problem. No new algorithm, hardness theorem, novelty or quantum execution.
The highest-value unresolved question remains a receiver polynomial in
BOTH degree d and logp for the published character-reconstruction problem.

## Contract and comparison

Input is fresh copies of |phi_Q>=p^(-1/2) sum_x chi_p(Q(x))|x>, for an
unknown monic irreducible Q of degree d>=2 over an odd prime field. There
are no rational roots, so padded and unpadded character states agree here.
The proposed general algorithm would have to handle this subfamily. Neither
classical sign labels nor an inverse preparation, full field-value queries,
additive-polynomial phases or extension-field queries are supplied.

The corpus lookup `character polynomial reconstruction collective measurement
extension field phase conversion` leads back to the native Hankel work;
the classical-baselines lookup names Groebner solving. Relevant already
tested/derived comparators are in LEGENDRE_HANKEL_RESULTANT_READOUT.md and
LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md: written native quantum
exp(O(d logd))*poly(logp), Kopparty full-table poly(p) under its actual
degree/radius promises, and exhaustive classical BIT decoding with p^d
candidate enumeration. Oracle and copy-only sources are distinct. No lower
bound on classical computation follows from these upper bounds.

The first candidate tries the weighted moments used in
[Childs et al.,1509.09271](https://arxiv.org/abs/1509.09271).
The actual source's Section2.1 supplies the FIELD-VALUE oracle
|x,y> -> |x,y+Q(x)>, and Theorem3/its footnote discuss the moment inversion.
That stronger source cannot be imported. The alternative below uses only
native copies and public character-weight phases, hoping for direct
coefficient recovery with polynomial resources. Its exact success test fails.

The independent candidate uses the classical-data-to-oracle construction in
[Zhao et al.,2604.07639v2](https://arxiv.org/abs/2604.07639v2), hoping to pay
controlled/oracle-inverse access needed by a stronger measurement. Corpus
lookup `Exponential quantum advantage processing massive classical data
succinct classical models` gives only generic nearby kernel/memory entries;
none substitutes for reading this source. The source's actual sample cost
and input model fail that proposed import. This preserves its stated space
advantage; it is not an external-paper-error claim.

## 1. A paid weighted-moment source and its exact failure probability

Let d=2m-1>=3, p>=m. Take m copies, project onto distinct x_i (probability
alpha=(p)_m/p^m), and attach independent uniform nonzero weights w_i with
the PUBLIC phase chi_p(w_i). Reversibly sort pairs by x and unprepare the
independent permutation register. Encode

    y_j=sum_(i=1)^m w_i*x_i^j,  0<=j<2m.

This is genuinely a different support/readout from the split-resultant
Fourier/Hankel receiver. The Hankel matrix (y_(i+j))_(0<=i,j<m) factors as
V diag(w_i) V^T, so is invertible for every supported distinct tuple. The
usual recurrence yields product_i(X-x_i); factoring this PUBLIC split
polynomial and solving the Vandermonde system recovers sorted x and w.
Thus original registers can be erased coherently. The prior capped public
split-factorization procedure pays polynomial(m,logp,log1eta) work with
its stated failure/approximation budget. No hidden-Q factoring is used.
The following probabilities describe the exact ideal source on its good
conversion branch; compilation error must be charged separately.

Moment encoding is injective on sorted pairs. Its source support has size

    N=binom(p,m)*(p-1)^m,

and the Fourier ambient space has size p^(2m). Measure the coefficient
label c=(c_0,...,c_(2m-1)), and if the top coefficient is nonzero, normalize
it to a monic polynomial. Correct output occurs EXACTLY at c=aQ, a!=0.
With the positive Fourier convention and tau=sum_w chi(w) exp(2pi*i*w/p),
each weight sum on such a label is

    sum_(w!=0) chi(w) exp(2pi*i*a*w*Q(x)/p)
       =tau*chi(a)*chi(Q(x)).

Multiplying by the original chi(Q(x)) cancels the target sign. Hence the
amplitude at each aQ is

    tau^m chi(a)^m binom(p,m) / sqrt(N*p^(2m)).

Since |tau|²=p, summing its square over the p-1 distinct nonzero scalars
gives the EXACT conditional ideal probability

    P_correct = binom(p,m) / [p^m*(p-1)^(m-1)].             (1)

For fixed m this is asymptotic to1/[m! p^(m-1)]. In particular d=3,m=2
gives1/(2p) EXACTLY, and joint success before the distinctness flag is
(p-1)/(2p²). Independent repetition costs Omega(p) already at degree3;
even hypothetical standard amplitude amplification with a paid coherent
success predicate would leave an Omega(sqrtp) cost. No such predicate or
source inverse is granted here. The existing fixed-degree receiver is a
stronger upper bound, so this direct readout merits no implementation.

Equation(1) rejects this operation's claimed success. It says nothing about
other processing of all its outcomes, different moment maps, adaptive
circuits or general collective measurements. No finite scan is needed to
establish this exact all-p normalization calculation.

## 2. Quantum oracle sketching retains the field-size cost

The primary PDF/text is `audits/sources/quantum_oracle_sketch_2604_07639v2.*`.
Parent and independent source helper read Theorems D.12/D.13 and the main
cost/space discussion. D.12 takes IID CLASSICAL labeled samples (x,f(x)),
x drawn from a distribution mu, and applies one basis-selective rotation
per sample. It approximates

    U=sum_x exp(i*t*mu(x)*f(x)) |x><x|

with M>=2*mu_max*t²/epsilon samples. The guarantee is diamond error for
the EXPECTED CHANNEL, not every particular sampled unitary. This is a
valid operational channel guarantee; discarding classical randomness does
not invalidate it. D.13 handles Q oracle/inverse/controlled calls with
fresh independent blocks and O(mu_max*t²*Q²/epsilon) total samples.

For a uniform domain of sizep and Boolean f encoding the character sign,
t=pi_math*p gives the desired phase oracle. The supplied construction
therefore uses O(p*Q²/epsilon) classical samples. Measuring |phi_Q> gives
x without f(x), so the given native copy source does not even supply these
labeled samples. The theorem is no copy-to-inverse conversion.

A direct falsifier strengthens this COST CHECK for the stated raw updates,
without claiming a general structured-learning lower bound. After M
basis-selective diagonal phase gates applied to |+>, at most M coordinates
have changed phase. For every realization, let S be those coordinates and
v_x their unit phases. Then

    |<phi_Q|v>| <= |sum_x chi(Q(x))|/p + 2|S|/p
                <= (d-1)/sqrtp + 2M/p,                    (2)

using the standard Weil bound for irreducible Q, d>=2. Thus the averaged
output's target fidelity is at most the square of the right side (capped
at1). When p is large compared with d², constant target fidelity requires
M=Omega(p) for THIS update construction, regardless of the chosen angles
or sample positions, with no interleaved mixing or separately learned model.
For example p>=64(d-1)² and M<=p/8 give fidelity
at most9/64. This tests a necessary oracle action on the uniform input;
it is not a lower bound for arbitrary circuits that exploit Q's structure.

The source itself states that allowing classical Omega(N) memory restores
asymptotically comparable runtime in its setting. Its NOPE lower-bound
transfer has separate noisy-encoding/discrepancy and query-complexity
premises, which have not been established for these structured characters.
No general classical simulation or rejection of its quantum space advantage
is asserted. Numerical datasets and its other applications were not audited.

## Decision

No new quantum implementation, benchmark or registry barrier is queued.
The weighted-moment normalization is the decisive experiment in analytical
form; the independent data-stream comparison supplies no unpaid inverse.
The next admitted operation must change the receiver beyond(1) while
preserving the native source, or solve a separately motivated task with
all access paid. Another source wrapper or finite scan cannot meet that
condition. No new source, hardness, novelty or speedup gate is opened.

Independent actual-text mathematical review accepted(1), coherent erasure,
conditional/joint probabilities, (2), the9/64 example and every scope guard.
The parent independently derived both calculations. A separate source helper
checked the formal oracle-sketch theorem inputs and costs. No additional
finite control or broader test suite is justified for these exact arguments.
