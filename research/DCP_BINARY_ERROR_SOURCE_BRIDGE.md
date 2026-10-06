# Binary-Error Source Bridge: Positive Reduction And Missing Quantum Step

LOCAL DERIVATION / REVIEW PENDING. No fast native arithmetic finder, accepted
candidate, independently reviewed theorem, novelty or speedup claim.

Read `BINARY_ERROR_HENSEL_DECODER.md` and `DCP_FOURIER_NOISE_DECODER_BOUND.md`
together. A real classical component exists. The source conversion required
to exploit it is missing, and two simple conversion shortcuts are falsified.

## Literature Update

[Kothari et al., arXiv:2609.40321v1](https://arxiv.org/html/2609.40321v1),
submitted September30,2026, proves a fixed-prime binary-error decoding tradeoff
(Theorem1.7) and a quantum ternary subset-sum tradeoff (Theorem1.3).
At m=epsilon*n^2, fixed epsilon>0, the quantum algorithm is polynomial.
This is a potential, not proved, exponential classical separation.
Section1.3's improved classical constant0.1022 has no complete algorithm
description or formal proof in that paper. Do not register it as a certified
implemented attack. Constants hidden by O_(q,kappa) need not be uniform for
growing q. Finite-field quotient arguments do not automatically extend to
two-power rings. These results are prior literature, not our discovery.

[Chen--Liu--Zhandry](https://arxiv.org/abs/2108.11015) supplies the quantum
filtering framework. Its parameter/source requirements are not a license
to equate a Boolean witness envelope with binary Fourier errors at every
modulus. The source bridge itself implements neither paper's quantum algorithm.
A subsequent pass implements the ternary classical Section4.2 quotient
primitive; see [Ternary Quotient Decoder](TERNARY_QUOTIENT_DECODER.md).

The curated records are in
`research/literature_audits/binary_error_frontier_sources.json`.

## A Positive Zero-Sum To Random-Target Reduction

Initial skepticism about zero sums versus targets was too strong. There is
a simple source-correct reduction, including for any finite abelian group.

Given IID original columns A_1,...,A_m and independent uniform target t,
append -t. Swap its position with a uniformly chosen marker j in {0,...,m}.
The extended matrix H is IID and j is uniform INDEPENDENT of H. Pass only
H and a fresh independent solver seed to a nonempty zero-sum solver.
Do not reveal j, t or the original matrix as side information.

If the returned verified Boolean zero word w includes j, undo the swap and
remove the marker bit. The remaining word solves A*x=t. Otherwise fail.
For ANY output distribution depending only on H and solver randomness,

    beta_target = E_H,seed[successful returned weight]/(m+1)
                >= delta_zero/(m+1).

Thus inverse-polynomial zero-sum coverage transfers with polynomial loss.
The extra column is public arithmetic data, NOT an extra unknown phase state.
This does not change field, alphabet, density or solver complexity. A known
bounded quantum solver still needs accessible purification/inverse for the
preferred direct witness filter; measured output access alone is insufficient.

Falsifier/control: if the zero solver sees j, it can avoid the marker and
have perfect zero-sum success but zero target coverage. The tests implement
that adversary. Exhaustive source controls cover81+1024 marker trials using
an explicitly exponential reference zero solver, not a candidate algorithm.

## Fourier Support Is The Actual Missing Bridge

For a normalized Boolean envelope f=c0*delta0+c1*delta1 with both amplitudes
nonzero, its DFT has at most one zero. Its support is at least q-1, not two.
For two points separated by d, the general support bound is q-gcd(d,q).
The source Boolean witness gap is a unit; an order-two gap silently changes
the witness alphabet and arithmetic problem.

Each Fourier-coordinate mass is at most2/q. Retaining any two coordinates
of a KNOWN envelope has mass at most4/q. This observation does not itself
implement a filter on an unknown translated state.

At q=3 the difference envelope has exactly two Fourier coordinates; the
module constructs an actual isometry from the one-qubit translated family
to its localized two-point target, up to a translation-dependent global phase.
This special positive control is not a growing-modulus algorithm.

## Single-Translation Channel Barrier

Let psi_v=(alpha|0>+beta*omega^v|1>) with both amplitudes nonzero, v uniform
in Z_q. With tau same-v copies its span has rank r=min(q,tau+1).
The desired target g_v=X^v(c0*delta0+c1*delta1) is localized on two points.

The projector sum satisfies sum_v |g_v><g_v| <= 2I (diagonalize its circulant
convolution; |c0+c1*omega^k|^2<=2). Therefore E_v=|g_v><g_v|/2 is a POVM
submeasurement. Pull it back through ANY heralded channel Lambda.
An r-dimensional input ensemble has uniform-index guessing success <=r/q:
each input density operator is <= its common span projector, and POVM traces
sum to at most r. Consequently,

    E_v <g_v|Lambda(|psi_v^tau><psi_v^tau|)|g_v> <= 2r/q.

This is success-weighted fidelity, not uncharged conditional fidelity.
It includes multiple Kraus operators and discarded environments. Polynomial
same-label copies would still be inadequate at exponential q; native inputs
do not even supply those copies.

For an EXACT nonzero pure-target branch K, any tau+1 input columns are
independent (Vandermonde). K cannot kill more than tau distinct translations.
Every q-1 target columns are independent: the target Fourier transform has
at most one zero; if it has one, its one-dimensional kernel has no zero entries.
At least q-tau successful columns then require q-tau<=tau+1. Thus tau>=floor(q/2)
is necessary for any nonzero exact branch. Success on EVERY translation
requires tau>=q-2. Refine Kraus operators to handle pure outputs of general
heralded channels. These are necessary, not sufficient, copy bounds.

Self-critique: NONE of this excludes joint different-label operations across
the native m-register state. Its full secret ensemble can have an exponentially
larger span. Nor does it rule out correlated-error source transforms, nonlinear
reductions, quantum subset-sum algorithms or generalized-dihedral HSP methods.

## Other Transfer Gaps

Ternary and two-power groups have no nontrivial additive homomorphism between
them: their exponents are coprime. Reducing integer representatives mod3 does
not respect two-power wraps. Nonlinear and collective reductions remain open.

A one-witness direct filter pays G/2^m even for a perfect finder. At ternary
m=n^2/16 and n=32,64,128,256 the upper bounds are conservatively
2^-13,2^-154,2^-821,2^-3690. This is a warning about importing high density
into THAT filter, not a no-go against the paper or all HSP algorithms.

## Highest-Value Next Research

Try an explicit public-A-adaptive COLLECTIVE measurement exploiting the native
translation subgroup, rather than another one-register binary-error filter.
The Fourier-noise audit now also proves that merely entangling a Boolean
envelope before the full coordinate DFT cannot evade its collision converse.
Correlated errors help only if a source-valid transformation produces a law
outside that model. Specify the full state, purification, error law, branch
probability and target reconstruction first. Then test whether the Hensel
decoder or a new structured classical decoder applies. Charge every selection,
label reuse and coherent preprocessing step.

Alternative: audit the finite-field quotient decoder's invariant ideal closure
and constants to discover reusable primitives. A bounded Macaulay rank alone
does not supply the actual quotient solver. Do not advertise a complete
uniform ring extension merely because low-bit linearization works.

The hypothesis contract is NOT an accepted CandidateRecord. Gemini owns
CLI/registry integration and production regressions; GPT owns the derivations.
