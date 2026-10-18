# Low-Rate Character OPI: Source And Coherent Ambiguity

2026-10-18. KNOWN DQI mechanism instantiated analytically; LOCAL APPLICATION
REVIEW PENDING. No new algorithm, quantum speedup, classical hardness or
executed large quantum decoder is claimed.

## Question And Decision

For the explicit low-rate prime-character model, can we control source-error
ambiguity beyond half the minimum distance without randomizing input shifts?
YES for the flat-spectrum primes below. But negligible ambiguity is NOT an
efficient decoder. The full capacity-decoding paper has been inspected past
its abstract, and its finite/running-time qualifications matter severely.

The concrete route is known DQI: generate sparse Fourier errors, compute a
public RS syndrome, coherently erase uniquely decodable errors, then perform
Fourier readout. The goal is a genuine end-to-end comparison on compact public
lists, not an oracle separation. Existing high-rate norm solvers do not meet
the degree budget at N127,K39; existing classical jet repair reaches109/127.
Neither that finite score nor non-applicability proves asymptotic hardness.

The published capacity-DQI score law is an asymptotic target, not the finite
mean/tail of the newly considered radius32 state. The latter is NOT certified
here. No new speedup candidate is admitted on the basis of these source bounds.

FOLLOW-UP: [finite readout certificates](PRIME_CHARACTER_FINITE_READOUT.md)
now supply a conditional finite mean/tail by paying for the observable's
EXTRA radius. This supersedes the missing finite-score status above, not the
unimplemented decoder/circuit or absent runtime advantage.

## Exact Local Source

Let chi be the quadratic character, with chi(0)=0. Write eta=+1 for lists
including zero, eta=-1 for strict lists. For public shift t_i and orientation
sigma_i, the native predicate has density rho=(p+eta)/(2p). Its centered,
unit-variance function is

    g_i(x) = [p*(-1)^sigma_i*chi(x-t_i)
                 +eta*(p*1_(x=t_i)-1)]/sqrt(p^2-1).

With Fourier convention ghat(xi)=E_x g(x)*exp(-2pi*i*xi*x/p), ghat(0)=0.
For xi!=0 the exact formula is

    ghat_i(xi) = exp(-2pi*i*xi*t_i/p)
       *[eta+(-1)^sigma_i*chi(-xi)*tau_p]/sqrt(p^2-1),
    tau_p = sum_x chi(x)*exp(2pi*i*x/p).

The classical quadratic Gauss evaluation gives tau_p=i*sqrt(p) at p=3 mod4.
See [Murty-Pathak, Theorem1.1](https://www.cmi.ac.in/~siddhi/Quadratic_Gauss_Sum.pdf).
Consequently EVERY nonzero Fourier probability is exactly1/(p-1), regardless
of shifts, orientations and zero convention. The phases remain essential;
uniform classical error samples are not a replacement for their interference.

At p=1 mod4, tau_p is real and these magnitudes are NOT flat. The p5 control
has probability spread sqrt(5)/6. The flat-source wrapper rejects that case
instead of silently importing an IID-uniform error premise.

One may construct a uniform nonzero register by a binary interval-prefix
rotation tree, followed by incrementing its uniform0,...,p-2 value. Only one
boundary prefix per bit needs a non-Hadamard split; controlled gates give
polynomial work in log p. Apply the public shift phase and a two-valued phase
controlled by reversible Legendre computation, then uncompute work bits.
Controlled versions can act on an error-support superposition. Approximate
rotations, modular arithmetic and the support/weight preparation must all be
compiled and charged; this pass does NOT implement that scalable circuit.
Heralding a separate uncontrolled rejection coin for each active support
wire would require a coherence analysis, not a free source shortcut.

## Correct Code And Input Model

Use H[j,i]=a_i^j for j=0,...,K-1, so H maps N error symbols to K syndrome
symbols. Any K columns are independent. Its kernel is the DUAL GRS code of
dimension N-K and minimum distance K+1. This H is not the N-K-row parity
matrix used by the separate affine-quadrics exporter.

Syndrome decoding reduces to ordinary RS list decoding: solve H*y=s publicly,
then recover kernel codewords near y. Known nonzero GRS column multipliers
convert them to ordinary RS while preserving Hamming distance. Thus decoder
rate is (N-K)/N, NOT K/N; radius ell has capacity gap (K-ell)/N. No secret
shift or hidden code is supplied.

For a fixed support S of size j, nonzero error values are independent uniform
in Fp*. This describes basis probabilities of the coherent error state; it
does not assume that public t_i are random. Different coordinates' phases
may be arbitrary. Radial weight superpositions use uniform supports at each
weight, exactly as in the known DQI source.

## Ambiguity Against The Entire Ball

Fix S, |S|=j<=ell<K, and competitor support T of size r<=ell. Let h=|S cap T|.
If |S union T|<=K, MDS independence forbids a distinct collision with both
supports exact/nonzero. Otherwise the intersection of the two syndrome
subspaces has dimension j+r-K. Each support map is injective. At most
p^(j+r-K)-1 possible nonzero source vectors can collide on that T.

The number of such supports at overlap h is C(j,h)*C(N-j,r-h). Therefore

    epsilon_j <= min(1,
      sum_(r=0)^ell sum_h C(j,h)*C(N-j,r-h)
        *(p^(j+r-K)-1)/(p-1)^j ),

where only j+r>K and max(0,j+r-N)<=h<=min(j,r,j+r-K-1) contribute.
Set epsilon=max_j epsilon_j. It bounds bad source mass for ANY normalized
radial weights. All arithmetic is exact, polynomial-size combinatorial
counting; no field/error table is built for the large records.

Equal-weight-only testing would be wrong: a retained weight5 kernel vector
over F7 splits into colliding errors of weights2 and3. Unique-distance checks
at radius2 would miss that radius3 competitor. Every bound here counts the
whole radius-ell ball, including all smaller weights.

## Coherent Error Is Not Bad Mass

Let A coalesce all radius-ell errors with the same syndrome. At most one
error per support maps to any syndrome, so each fiber has size at most

    M=sum_(r=0)^ell C(N,r).

This exponential COUNT is used as an O(N)-bit integer, not enumerated by the
large-input computation. In a calibration, the whole ball really is enumerated
and explicitly charged.

Decompose a normalized source into unique-good and ambiguous-bad vectors.
Their syndrome images G and B have DISJOINT supports. If actual bad mass is
epsilon_actual<=epsilon, then ||G||^2=1-epsilon_actual and
||B||^2<=M*epsilon_actual by Cauchy-Schwarz. Postselecting a coherent unique
decoder's success flag yields G/||G||, not the unheralded full ideal state.
If epsilon<1 the ideal state (G+B)/||G+B|| is well defined, and

    P(unique herald)>=1-epsilon,
    trace_distance^2 <= M*epsilon/(1-epsilon+M*epsilon).

The same bound controls TV after Fourier readout. An explicit aligned M22,
epsilon1/100 countercontrol saturates this pure-distance bound: error can be
over40 times the failed source mass. Do not charge only epsilon as output TV.
This does NOT supply a decoder, a gate budget, or an independent approximation
to arbitrary normalized-coset sampling.

## What The Full Decoder Paper Actually Supplies

[Dao-Kominers-Thaler](https://quangvdao.github.io/papers/authored/reed-solomon-codes-beyond-johnson.pdf),
Section9.1 and Theorem9.16, gives deterministic fixed-gap decoding in the
binary input size, with explicit field-presentation premises. Its stated
runtime is B_delta*N^O(exp(1.5/delta))*polylog(p). Finite parameters depend
on delta; "polynomial" does not mean a practical circuit. Only relevant
statements and recovery construction were audited, not the entire145-page
proof or its Lean development.

For delta<6/25, equation87 and Theorem6.8 have a length threshold at least the
derivative order d=ceil(exp(1.5/delta))>500. The generic finite certificate
therefore cannot be applied directly at N127. Its bounded-length fallback
is exact but is not a useful gate-budget argument. A sharper rate-specific
first-order certificate or an actual alternative decoder would need separate
parameters and implementation; no hidden initial field-value enumeration is
allowed. Prime-field arithmetic supplies the needed field representation,
but does not remove that recovery cost.

Audited author-hosted PDF SHA256:
`b67c188ec477b6063caf9c1c06b214c71e358ff09b9517adcdb1db212ea2700a`.
This supersedes the repository's previous abstract-only decoder assessment,
not its explicit nonimplementation flags.

## Executed Evidence And Limits

At N127,K39,p=2^61-1, both zero conventions, ell32:

- Fixed-input source ambiguity upper bound is about3.198e-99.
- Coherent pure-distance SQUARED upper bound is about5.266e-69; output-TV
  bound is its square root, not that squared number.
- The ell19 unique-distance control has zero ambiguity. Ell24 also has a
  strong analytic bound. Ell38 has only the trivial bound1 and is NOT promoted.
- No error vectors, field tables, coefficient words or quantum decoder were
  generated at these large parameters. These are exact rational proofs-under-
  premises, not measured error estimates or gate-level executions.

Six bounded native controls at N6,K3,ell2 use p7/19/43, both zero conventions.
They enumerate all577/4969/26713 ball errors and343/6859/79507 coefficient
words, respectively. The implemented injective source/syndrome/unique-flag/
conditional-erasure map retains ALL ambiguous errors. A unitary FFT then
produces the heralded native output. Independently evaluating the centered
predicates and their elementary-symmetric filter reproduces the full ideal
complex amplitudes, not just an average score.

Actual bad masses are0.288889/0.100000/0.046032. Including-zero output TV
from the full ideal filter is0.290700/0.189571/0.114454; strict siblings are
also retained. The calibration decoder is explicitly EXHAUSTIVE, not an
implementation of the published efficient decoder. No runtime claim is
inferred from these small controls, and no source is rerolled.

## Attempt To Disprove The Route

- Uniform Fourier magnitude needs p=3 mod4 and this exact predicate family.
  The p5 counterexample rejects a plausible overgeneralization.
- MDS independence and exact support nonzeros are essential. Repeated columns
  collide at radius1 despite the nominal dimension. Real Vandermonde minors
  and a different-weight collision are tested independently.
- Small source ambiguity does not mean small coherent error without paying
  maximum fiber size. The aligned-phase countercontrol makes this concrete.
- Unique erasure changes the state at finite parameters. Full amplitudes and
  TV are checked, with bad branches retained rather than silently discarded.
- The large bounds assume an exact mathematical source. Compiled preparation,
  arithmetic, QFT and decoder synthesis errors must be added; they are NOT0.
- Known fixed-gap polynomial decoding may still be unusable in finite regimes.
  The actual finite decoder, reversibility/space, list verification and
  uncomputation remain the constructive bottleneck, not source randomness.
- Classical low-rate character OPI may still be easy. Existing jet attacks
  and new algebraic attacks must be compared against an ACTUAL finite quantum
  mean/tail and resource budget. No hardness follows from current failures.

Next decisive work is a named, finite, phase-correct capacity-decoder/readout
construction with its parameters, or a different algorithmic mechanism.
Do not add more source seeds, ambiguity meshes or neighboring bridge theorems.

```text
python theorems/prime_character_capacity_source.py --write
python -m pytest -q tests/test_prime_character_capacity_source.py
```
