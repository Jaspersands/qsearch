# Retained-Data Missing-Harmonic Detector

Status: DERIVED / REVIEW-PENDING. Physical finite controls are implemented.
No independent proof review, formal verification, novelty, competitive
algorithm, or general circuit lower bound is claimed.

## What Changed

The preceding fixed-mask bounds discard physical coset registers. This
benchmark retains them and repeats coherent selected-subset reflections.
It supplies a concrete, costed constant-bias detector, not an efficient
implementation of the exact span projector. The smallest positive frame
eigenvalue is unnecessary for this detector. Its factorial-scale normalized
amplification, rather than an unknown minimum gap, is the remaining defect.

Do not confuse three operators:

- The existing hidden-involution support-span module spans the supports of
  hidden states and accepts the alternative with perfect completeness.
- The existing PGM average-frame module averages conditioned hidden states.
- This module spans missing-sign subset subspaces, annihilates the alternative,
  and reports TRIVIAL on acceptance. Its normalized frame has mean 1/n!,
  not 2^-K. It does not condition on source labels.

## Scope And Prior Art

Let G=S_n, D=n!, and take K standard mixed coset states with ONE common hidden
involution h. The null is I/D^K and the alternative is
[(I+R(h))/D]^tensor K, with R(g)|x>=|xg>. The sign character is missing only
if h has an ODD number of transpositions. For fixed-point-free h this requires
n=2 mod 4. In particular, sign does NOT work for fixed-point-free S4.

For each nonempty subset S of the registers define

    P_S = D^-1 sum_g sign(g) R(g)^S.

The missing-harmonic span construction and its pairwise trace identities
are established prior art in
[Moore and Russell](https://arxiv.org/abs/quant-ph/0504067).
Here we use those identities to audit a particular two-reflection detector.
The general randomized-iteration and amplification techniques are standard:
[Boyer et al.](https://arxiv.org/abs/quant-ph/9605034),
[Brassard et al.](https://arxiv.org/abs/quant-ph/0005055).

## A Selected Projector Without A Recoupling Basis

Given a coherent subset register, choose its first selected position p
reversibly. On selected positions i != p compute

    (x_p, x_i) -> (x_p, x_i x_p^-1).

Simultaneous right multiplication leaves these relative coordinates fixed
and right-multiplies only x_p. Thus P_S is conjugate to the rank-one projector
onto |sign>=D^-1/2 sum_x sign(x)|x> on the pivot, tensored with identity.
Prepare/unprepare this signed uniform permutation state, reflect its zero
preparation input, and undo the coordinate changes. Reversible permutation
arithmetic and uniform permutation preparation have polynomial descriptions;
the state can be prepared using a reversible insertion encoding and parity.
The inverse encoding must be uncomputed: an entangled insertion-code garbage
register would implement a different projector.

Subset preparation uses a uniform superposition on the 2^K-1 nonempty strings,
not an enumerated table. Exact arithmetic here describes ideal rotations;
finite gate synthesis needs a charged error budget. The finite code explicitly
checks the coordinate permutation against the independent regular group sum.
It does not claim to emit a fault-tolerant gate sequence.

## Moments And A Threshold With Constant Null Mass

Use normalized trace E(X)=Tr(X)/D^K. Write delta=1/D and m=2^K-1.
For distinct nonempty S,T,

    E(P_S)=delta,              E(P_S P_T)=delta^2.

One register in the symmetric difference forces one group summation variable
to identity in the regular trace; a selected register forces the other.
This proves the second identity even for overlapping or nested subsets.
It does NOT mean the projectors commute.

For arbitrary fixed nonnegative weights summing to one on distinct subsets,

    F=sum_S w_S P_S,
    E(F)=delta,
    E(F^2)=delta^2 + delta(1-delta) sum_S w_S^2.

Uniform weights minimize this second-moment certificate. This is not an
optimality proof for all weighted detectors or source-adaptive programs.
For uniform weights let r=1+(D-1)/m. Cauchy-Schwarz gives support mass >=1/r.
More usefully, if lambda is sampled from the raw-null eigenvalue distribution,

    Pr[lambda >= delta/2] >= 1/(4r).

For completeness, split E(lambda) at delta/2. The below-threshold contribution
is at most delta/2. Cauchy-Schwarz bounds the above-threshold contribution by
sqrt(E(lambda^2) Pr[above]), giving the displayed inequality. Arbitrarily tiny
positive eigenvalues may exist, but this detector does not need to detect them.

## The Actual Two-Reflection Detector

In the subset ancilla times retained data space set

    A|v> = |uniform nonempty S> |v>,
    Q = sum_S |S><S| tensor P_S,
    A* Q A = F.

Reflect about the image of A by reflecting only the prepared subset state;
reflect about Q using the coherently selected projector above. No reflection
about an unknown input state or its purification is supplied or needed.
The two-projector invariant-plane calculation gives, for eigenvalue lambda,

    p_t(lambda)=sin^2((2t+1) arcsin(sqrt(lambda))).

Choose T=ceil(sqrt(D)). With probability 1/2 perform the direct Q measurement.
Otherwise choose t uniformly from 0,...,T-1, iterate the two reflections t
times, and measure Q. This uses at most T selected-projector operations and
reuses the same K coset states. Ancillas and physical data stay coherent until
the terminal measurement. This is NOT a fresh sample per Grover iteration.

The response is q_T(lambda)=[lambda + average_t p_t(lambda)]/2. On
lambda in [delta/2,1/2], put theta=arcsin(sqrt(lambda)). Then

    average_t p_t = 1/2 - sin(4T theta)/(4T sin(2theta)),
    sin(2theta) >= sqrt(delta),
    average_t p_t >= 1/4.

For lambda >=1/2 the direct half of the mixture already contributes >=1/4.
Consequently q_T>=1/8 throughout lambda>=delta/2, including near one where
the denominator in the randomized-only argument would be small. Therefore

    Pr[report trivial | null] >= 1/(32r) >= 1/64 if m>=D.

Every P_S annihilates each promised hidden state. Its embedded support lies
in ker(Q); both reflections preserve that failure subspace, so the ideal
false-trivial probability is ZERO for every h, not merely its average.
Under equal priors this gives success at least 1/2+1/128. Repeating a constant
number of independent K-copy blocks improves the constant error. No promise
on the least positive eigenvalue or an exact support projection was used.

## Charge The Cost And Try To Kill It

The selected reflection and subset reflection have polynomial descriptions,
but the schedule has T=Theta(sqrt(n!)) iterations. Total space remains
polynomial and total time is O(poly(K,n,log(1/epsilon))*sqrt(n!)). Per-primitive
operator error must be O(epsilon/T); a telescoping unitary bound then gives
O(epsilon) total error. The extra precision is logarithmic in T, NOT free and
NOT another factorial time factor under standard efficient gate synthesis.

This cost is not just a conservative upper bound for the stated schedule.
The elementary inequality |sin((2t+1)theta)|<=(2t+1)|sin(theta)| gives

    E_null q_T(F) <= min(1, (2T^2+1)/(3D)).

Thus polynomial T cannot produce constant acceptance for this normalized
walk. This is not a lower bound on arbitrary retained-data measurements.

The access model matters when comparing competitors:

- With coherent hiding-function access and known fixed-point-free class C,
  Grover search tests f(h)=f(e) over h in C. It takes O(sqrt(M)) predicate calls,
  M=(n-1)!!, which is asymptotically smaller than sqrt(n!). Uniform perfect
  matching preparation and permutation arithmetic have polynomial overhead.
  This benchmark is unavailable if only coset samples are supplied.
- Classical enumeration under that oracle takes O(M) tests. It is a simple
  upper bound, NOT the best possible classical algorithm or a lower bound.
- On explicit graph inputs, the classical comparison is quasipolynomial GI,
  not factorial enumeration. [Babai](https://arxiv.org/abs/1512.03547)
  establishes that baseline. This says nothing about arbitrary opaque HSP
  labels, and the present sign promise is not a full graph-to-HSP reduction.

Verdict: reject generic amplification as a breakthrough route. Keep this
benchmark because it removes an unnecessary gap obligation and gives a
concrete physical interface for testing genuinely different compilers.

## Stronger Selector-Only Query Boundary

The particular randomized schedule is not essential if the program has the
following RESTRICTED interface: ancillary registers start independently of
the physical data; the only data couplings are controlled phases on selected
missing-sign projectors P_S; all interleaving operations act only on ancillas;
and the final measurement reads only ancillas. Include all controls and
deferred measurement records in those ancillas, and charge every query.
There is no free postselection, source-label extraction, or final data POVM.

For q calls, any phase schedule in this interface satisfies

    T(output_null, output_h) <= min(1, 2q/sqrt(D))

for EVERY promised hidden h and arbitrary K. For a one-sided accept event
whose ideal alternative probability is zero,

    Pr[accept | null] <= min(1, 4q^2/D).

Proof: compare the real null-input program with its identity-query version.
Purify the raw maximally mixed data using an inaccessible reference. Before
the j-th query of the identity-prefix hybrid, the joint state is a pure
ancillary vector times that fixed purification. For a controlled phase
exp(i theta P_S), the squared change in norm is at most

    4 sum_S Pr[select S] Tr(P_S)/D^K <= 4/D.

The empty subset is inactive. The bound permits coherent subset/control
registers: distinct control basis states are orthogonal, so cross terms do
not appear in this squared norm. Telescope the q query differences using
identity prefixes and actual unitary suffixes. Unitaries preserve norm,
giving purified-vector distance <=2q/sqrt(D), which bounds the output trace
distance after discarding data and reference.

For an alternative input, every P_S annihilates its support. Ancilla-only
interleavings leave the physical support unchanged; all query calls therefore
act as identity. Its ancilla output is EXACTLY the same identity-query output
used above. This proves the two-sided distinguishability bound. If an accept
effect has zero probability on that output, its square root annihilates the
baseline purification; applying it to the difference vector gives the squared
one-sided bound. Measurements and classical adaptivity can be deferred into
ancillary history registers. No independence of actual successive query
states, commuting P_S, or resampling of h is assumed.

This is an application of a standard query-hybrid argument; see
[Bennett et al.](https://arxiv.org/abs/quant-ph/9701001) for the method's
provenance, not for a claim that this particular scoped application is novel.
It matches the benchmark's sqrt(D) scale within the stated interface, up to
constant-bias factors. It is NOT a general quantum circuit lower bound.

The excluded final-readout condition is substantive. A free measurement of
the known missing-harmonic span already has nonzero null acceptance and zero
alternative acceptance with q=0 in this accounting. The finite audit retains
this explicit counterexample, as well as random complex ancilla programs,
controlled query phases, quantum memory, and each hidden transposition.
Data-dependent source preparation and other data operations are also outside
the theorem. They require their own cost and information analyses.

Research implication: changing only the ancilla schedule or adding memory
cannot improve this route to polynomial time. A useful next compiler must
specify different charged data operations or a genuinely implemented final
data measurement, not simply optimize the same selected-sign query sequence.

## Falsifiers And Next Work

- Check each hidden member, not an independently resampled h per copy.
- Reject even-transposition sign claims; test S4 transpositions as a valid
  calibration and S4 double transpositions as an invalid premise.
- Compare physical coordinate projectors, all pair traces, the two-reflection
  response and noncommuting overlap examples; never infer joint measurement
  from pairwise trace independence.
- Never drop the 1/m normalization, replace F by F/delta for free, or reflect
  about an unknown data input. A source-adaptive variant needs a new law.
- A useful next proposal needs a structured compiler with costs below this
  walk, not another proof of its known information or polynomial-space use.
- Reject attempts to apply the selector-only query bound to free terminal
  data measurements or source-dependent preparation. The declared-scope
  contract checks literal booleans and is not an arbitrary program verifier.

Implementation: `theorems/coset_missing_harmonic_detector.py`; tests in
`tests/test_coset_missing_harmonic_detector.py`. Live CLI and experiment runner
write the same report and negative-result record, with proof and mutation
obligations preserving the distinction between a costed schema and a speedup.

## Source-Adaptive Extension (Implemented)

The lead below is now implemented and gated as DERIVED / REVIEW-PENDING.
See [the complete conditional argument and physical controls](MISSING_SIGN_SOURCE_ADAPTATION.md).
It is a separate extension, not a license to remove the independent-ancilla
premise from the earlier selector-only theorem.

For a complete source tuple lambda, the conditional raw-null probability of
the sign sector on S is

    r_S(lambda) = mult_sign(tensor_(i in S) lambda_i) / product_(i in S) d_i.

For any j in S, Frobenius reciprocity identifies its numerator with the
multiplicity of sign tensor lambda_j^* in the tensor product of the other
sources. That irrep has dimension d_j, so dimension counting gives

    r_S(lambda) <= 1/d_j^2,
    max_(S nonempty) r_S(lambda) <= sum_(i=1)^K 1/d_i^2.

Under the raw-null Plancherel source law, E(1/d_lambda^2)=p(n)/n! exactly.
Therefore even an arbitrarily costly source-dependent choice of subset has
average marked mass at most K p(n)/n!. This needs no unknown uniform
character-ratio constants and applies to all subset sizes simultaneously.

The source-conditioned identity-prefix hybrid contribution is
2q sqrt(K p(n)/n!). But the alternative's source law differs from the null's:
p_lambda=d_lambda^2/D, q_lambda=d_lambda(d_lambda+chi_lambda(h))/D.
Character orthogonality gives single-copy source TV <=1/(2 sqrt(M)), where
M is the hidden conjugacy-class size. At K copies use the product-TV bound
K/(2 sqrt(M)); the source law is identical for all h in the same class.
The derived combined bound is

    T(outputs) <= min(1, K/(2 sqrt(M)) + 2q sqrt(K p(n)/D)).

Assumptions still include standard mixed inputs, full CENTRAL source labels,
no other carrier operations, selected missing-sign phases as the only further
data coupling, and ancillary/source-label-only final output. This does not
cover measuring noncentral carrier bases or arbitrary final data POVMs.
The q=0 term must NOT be dropped: source labels already reveal weak signal.

Persistent exact rational checks enumerate every source tuple and nonempty
subset in these controls (using the existing character tables):

| n | K | Sector checks | E_null max_S r_S | K p(n)/D |
|---|---|---|---|---|
| 3 | 3 | 189 | 119/216 | 3/2 |
| 4 | 2 | 75 | 23/192 | 5/12 |
| 4 | 3 | 875 | 2819/13824 | 5/8 |
| 6 | 2 | 363 | 719/172800 | 11/360 |

These character/rank calculations are independent of a hidden-class choice.
Using the S4 double-transposition character-table helper is NOT evidence that
sign is missing for that class. A full physical source-adaptive channel test
must use an odd-transposition class, and must check each hidden member.

Independent regular-rank/prior controls, physical source-adaptive programs,
the q=0 source residual and exact scalable certificates are implemented in
`coset_missing_sign_source_adaptation.py`, with proof and negative records.
Independent mathematical review is still pending. No new algorithm is
suggested by this bound; other target sectors and carrier operations remain open.
