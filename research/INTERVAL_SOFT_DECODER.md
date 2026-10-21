# Interval Soft Decoding: Actual Receiver And Classical Falsifiers

2026-10-18. LOCAL APPLICATION REVIEW PENDING. Known reduction, not a new
quantum algorithm. No asymptotic classical hardness or speedup is claimed.

Run `python theorems/interval_soft_decoder.py --write`. This answers the
independent non-flat-source question selected after the phase/erasure pass.
It is not a new infrastructure layer or another phase-oracle wrapper.

## Problem, Mechanism And Ceiling

Work over a prime p with FULL support0,...,p-1 and block length N=p.
H has d rows H[j,x]=x^j. Its kernel is RS_(p-d), since full-support RS_d
and RS_(p-d) are dual. Given a UNIFORM random public syndrome s, find

    H*e=s mod p, with every centered e_i in[-u,u].

This is an explicit RS-ISIS-infinity instance: no membership oracle or
planted short vector. For any public particular y with H*y=s, the equivalent
OPI output is a polynomial P of degree<p-d with y_i-P(i) in[-u,u]. A canonical
particular y is a LEGAL change of coset representative, not source advice.

These fields p=31,61,127 are literal cardinalities, NOT the earlier61-bit
prime2^61-1. This problem has p sites, includes evaluation0 and is not the
previous fixed-character N127,K39 input. Do not transfer results between them.
The runtime convention includes block/output length N, not only log p.

Proposed route: choose a unit target amplitude a supported on S=[-u,u],
let f be its inverse unitary DFT, prepare F=f^tensor N and coherently erase
errors with a syndrome decoder for RS_d. A public phase selects the desired
dual coset; the full QFT then preferentially outputs words in S^N. This is
the KNOWN soft-decoding/Regev mechanism, not a discovery here.

The literature inputs used are [Chailloux--Tillich](https://arxiv.org/abs/2411.12553),
Theorems5/7, and [Sun--Wootters](https://arxiv.org/abs/2610.12357), Theorem1.8.
The former uses the sufficient soft-decoding condition d/p<C, where
C=sum_e |f(e)|^4, and gives an inhomogeneous UNIFORM-target average guarantee.
The latter supplies a known perfect-search algorithm at fixed rates with
target rate+density>1. Neither statement supplies our finite gate compiler.
Their oracle hardness claims do not apply to these public intervals.

An elementary independent bound limits this proposal. For ANY complex a
supported on L elements, Cauchy gives |f(e)|^2<=L/p. Since sum|f|^2=1,

    C <= L/p = rho.

Thus d/p<C implies(1-d/p)+rho>1. At fixed rates and fixed positive gaps,
this entire support-SEARCH range is already covered by the newer known
algorithm. This is NOT a weighted-coset-sampling algorithm and NOT a finite
decoder-runtime comparison. An initial broader subsumption interpretation
was rejected: when rho vanishes or gaps shrink with p, that fixed-rate
runtime theorem cannot silently be transferred. The report retains this
unresolved sparse-growing regime explicitly.

There is a second ceiling. When4u<=p-1, the uniform interval profile has

    C_uniform = 2L/(3p) + 1/(3pL).

Consequently ANY amplitude tuning changes the real KV codimension cutoff
by a factor LESS than3/2 over that simple profile. Small integer thresholds
are not replaced by this real-valued ratio. A profile optimizer alone is a
low-ceiling research direction, including in the sparse-growing regime.

## Actual Finite Quantum Receiver

Eight complete controls use p=N=5: dimensions d1/2 with profiles(1,1,1),
(4,5,4),(1,2,1); one asymmetric complex-source profile(1,1,2); and an explicit
S={0} empty-target control. These are calibration identities, not proposed
toy-oracle speedups. Every source vector, codeword, target and failed branch
is accounted for. Main QFT dimension is3125; pre-erasure sparse source pairs
number15625 or78125. There is no efficient KV circuit in these controls.

The decoder is an EXHAUSTIVE deterministic maximum-posterior syndrome table.
For p5, source probabilities lie in Q(sqrt5), including the asymmetric source.
Exact rational coefficients and square comparisons resolve all MAP ties;
floating Fourier arithmetic is used only for the subsequent bounded quantum
calibration. An independent numerical complete-MAP calculation also checks
its mass. The table has625/125 entries, NOT polynomial-size large access.

The source map(c,e)->(c+e,e-dec(H_decode(c+e))) is checked injective on its
ENTIRE support. Good residual0 is postselected with probability P_dec;
all failure mass1-P_dec is retained. For every uniform target s, a public
particular phase v solves-H*v=s. The actually accumulated code/error source
and QFT agree in COMPLEX amplitudes with the independent transform of the
truncated error function, restricted to the ORIGINAL target syndrome coset.
The target is NOT changed to an easier syndrome after observing failure.

| d | Target Profile | P_dec | Mean Conditional Valid | Worst Target Valid |
| --- | --- | ---: | ---: | ---: |
| 1 | 1,1,1 | .868911 | .883646 | .873585 |
| 1 | 4,5,4 | .903397 | .920170 | .899840 |
| 2 | 1,1,1 | .697592 | .755340 | .723325 |
| 2 | 4,5,4 | .770203 | .797986 | .722780 |
| 2 | 1,2,1 | .718780 | .807938 | .724174 |

Decisive controls:

- Replacing signed source amplitudes by their magnitudes changes output TV
  by up to.72064; the complex-source control changes by.85778. Probabilities
  are not a replacement for a coherent source.
- At profile(4,5,4),d2,target(2,0), valid probability.722780 and squared
  fidelity.719020 are BOTH below P_dec=.770203, despite a nonempty target.
  The uniform-average P_dec fidelity/validity bound is not pointwise. This
  does NOT contradict the paper's weaker average-TV theorem. No target is
  sampled from a planted solution or reweighted by its partition mass.
- Profile(1,2,1) improves finite conditional acceptance while REDUCING C
  enough to FAIL the d2 sufficient KV condition. Finite MAP success does not
  certify a scalable soft decoder or validate a proxy-based discovery claim.
- S={0},d1 retains all five uniform targets, four empty. Average valid
  probability is.2, not1 obtained by discarding the empty cosets. Equality
  d/p=C is not accepted as the STRICT sufficient condition.

For completeness, the uniform-average search bound can be derived directly.
Let G be the normalized restriction of F to the selected decoding set.
Every syndrome receives one representative. Writing A_s for the coset inner
product between transformed F and G, and Z_s for the ideal coset mass,
Cauchy yields sum_s |A_s|^2/Z_s >= |sum_s A_s|^2=P_dec. Empty targets have
zero fidelity. This is the UNIFORM average squared fidelity of normalized
receiver states. Interval-valid probability dominates fidelity, so the
UNCONDITIONAL one-attempt uniform-average valid probability is at least
P_dec^2, after paying the herald. This local elementary bound is not a new
algorithm or a pointwise statement. Actual validation evaluates all targets.

## Classical Baselines And Stronger Certificates

An exact integer dynamic program counts weighted interval words by syndrome.
Backward sampling uses squared integer target amplitudes and EXACT integer
draws. Its transition probabilities telescope to product_i a(e_i)^2/Z_s;
tests check every legal word, not merely empirical histograms. It exactly
matches the ideal weighted quantum target, unlike the approximate receiver.
All small controls are therefore classically tractable.

The table costs O(N*L*d*p^d) arithmetic operations and O(N*p^d) entries.
This is exponential in growing codimension. But if L is CONSTANT, the KV
condition and C<=L/p force d<L, also constant. Thus the ENTIRE certified
constant-width full-RS SEARCH window has a polynomial classical uniform
coset sampler in the same block/output-length convention. The exact weighted
claim applies to supplied integer profiles; arbitrary complex amplitudes
are not assumed freely available as exact classical probabilities. No such
conclusion is drawn for growing L or d. State-cap exhaustion returns UNKNOWN,
not hardness.

The larger attack builds the PUBLIC systematic integer lattice

    Lambda={z in Z^p : H*z=0 mod p}, determinant p^d.

Its basis comes only from the target code. FLINT exact-Gram LLL supplies a
checked unimodular transform. An existing exact-rational Babai implementation
produces residuals from each public particular target. Centering modulo p
preserves every original modular equation. Independent Lagrange/Horner
interpolation verifies every saved polynomial witness. One canonical
interpolation attempt has exact uniform-target success rho^d; no false
independence of repeated fixed-target attempts is assumed.

Six declared native families cover dense intervals with a fixed absolute
KV gap and intervals u=floor(sqrt(p)) with a fixed relative gap. ONE public
basis is used per family, four uniform syndrome replays, no seed/basis
restarts or planted short vectors. All24 solve the original interval problem.
This replay alone is NOT a confidence interval or an asymptotic attack proof.

Stronger evidence does not rely on those trials. Let b_i^* be the exact GS
vectors of a public basis. Every Babai residual has GS coordinates in
[-1/2,1/2]. Hence for EVERY integer target:

    ||residual||_2^2 <= (1/4)*sum_i ||b_i^*||_2^2,
    ||residual||_infinity <= (1/2)*max_j sum_i |b_i^*[j]|.

Integral coordinates permit exact floor bounds; centering can only improve
them. Both bounds are rounded UP to128-bit dyadics before applying the
integer floor. The producer checks full GS orthogonality exactly, lattice
membership, index and unimodularity. Certified bases are saved. A DIFFERENT
Fraction/explicit-vector GS implementation checks the saved certificates.

| p | d | u | Uniform Integer Bound | ALL Syndromes Certified |
| --- | ---: | ---: | ---: | --- |
| 31 | 8 | 7 | 6 | Yes |
| 31 | 5 | 5 | 5 | Yes |
| 61 | 17 | 15 | 14 | Yes |
| 61 | 8 | 7 | 7 | Yes |
| 127 | 35 | 31 | 63 | No |
| 127 | 12 | 11 | 12 | No |

The first four are finite all-syndrome classical certificates, not just
selected witnesses. The last two bounds are inconclusive, NOT counterexamples
to the attack: every declared trial still succeeds. No all-p covering family
bound, all-code dequantization, or efficient exact growing-codimension sampler
is established.

## Decision And Next Scientific Question

Cut profile tuning as a claimed breakthrough route; cut claims of a
SUPERPOLYNOMIAL quantum-search separation at constant full-RS interval width;
cut the tested finite families as advantage evidence. Retain the actual
non-flat receiver, exact ideal sampler, complete
failure accounting, feasible-coset counterexample and replayable covering
certificates. No central result is promoted before independent review.

Resources still missing for a quantum candidate: efficient coherent KV/list
selection rather than an exhaustive table, source and Fourier gate synthesis,
decoder-workspace precision and repetition costs, and a matched asymptotic
classical comparison. The abstract reduction needs two N-field registers,
code/phase arithmetic and reversible decoder workspace; the exhaustive
calibration does not discharge those costs.

The meaningful remaining sparse-growing question is whether a CONSTRUCTIVE
public RS-lattice basis has a covering bound scaling through
u~sqrt(p),d~(16/15)sqrt(p). An analytic basis/rounding argument could falsify
that published quantum-advantage candidate; another filter, LLL seed sweep,
finite radius adjustment or DCP bridge will not. Failing that, compare a
genuinely different code/source mechanism, with its own classical baseline.
Do not transfer the fixed-rate capacity theorem to vanishing density or
mistake an easy support search for exact weighted sampling.

Verification:20 focused tests pass in43.25s and145 related regressions pass
in22.48s across separate commands, with RuntimeWarning as error. Not a full
repository suite. Live producer, SHA replay, strict finite JSON/evidence paths,
Python compilation, site JS, plain registry validation and whitespace checks
pass. No central candidate, negative or proof was promoted.
