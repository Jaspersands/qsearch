# Linear Erasure Does Not Supply The Missing Quantum Decoder

Local derivation, review pending. No novelty, general DCP no-go, new accepted
candidate or new central negative. This is a decisive test of a CONSTRUCTIVE
shortcut, not another literature-wide barrier. It extends the existing
`ternary_decoder_filter.py` rather than adding a separate research framework.

## Question And Proposed Mechanism

Problem: given explicit IID A in F3^(n by m), find an all-nonzero signed word
c with A*c=0. The existing invertible shear converts this to a nonempty Boolean
zero sum on an IID transformed matrix. This is a natural explicit-input
subset-sum problem, not an invented oracle. A signed word allowing zeros is
NOT the same problem: ordinary nullspace elimination already finds those.

The [CLZ filtering framework](https://arxiv.org/abs/2108.11015) and
[Kothari et al., Section3](https://arxiv.org/html/2609.40321v1) motivate replacing
the hard classical decoder in the coherent prepare/subtract/readout template.
Could public Gaussian elimination suffice, since it can remove the original
secret from the residual register? If so, m=O(n) might bypass the known
high-degree algebraic decoding cost. This would be high upside, but is false
for the linear replacement tested here.

## Complete Source And Instrument

For full row rank A and a public right inverse R with A*R=I_n, prepare

    1/sqrt(3^n*2^m) sum_(s in F3^n,e in {1,2}^m)
        (-1)^(number of e_j=2) |A^T*s+e>|s>.

All registers are KNOWN prepared states in this classical-input construction;
this is not a supply of arbitrary unknown native DCP states. Apply the actual
reversible subtraction d(b)=R^T*b from the secret register, then the existing
local trine readout on b. The residual is -R^T*e, not a clean zero register.
Keep/trace it; do not postselect it or erase it for free. A fixed additional
decoder offset merely translates this residual and changes no word probabilities.

The source, subtraction permutation, all residual branches and complete local
readout execute in the finite statevector controls. R may depend on public A;
no planted s, error, true witness or private source flag enters the decoder.

## Exact Classical Sampler For The ENTIRE Output

Let P=I_m-R*A. For ANY public right inverse R the full quantum output word has
exactly the same distribution as:

1. Draw e uniformly from {1,2}^m using m classical random bits.
2. Return c=P*e modulo3, including every zero coordinate/failure.

This is stronger than a comparison of success probabilities. To derive it,
sum the prepared amplitudes over s after Fourier readout: nonzero amplitude
requires A*c=0. The remaining residual blocks group errors by R^T*e. Parseval
on the residual index gives

    Pr(c) = 1[A*c=0] * 2^(-m)
            * #{z in F3^n : every coordinate of c+R*z is nonzero}.

Because A*R=I, the map (c,z) -> c+R*z is a bijection from
ker(A) times F3^n to F3^m. Its nonzero-coordinate words are exactly the
uniform sign coins above, and P*(c+R*z)=c. This proves the claimed sampler.
The local readout's diagonal phases do not affect these Born probabilities.

Constructing a systematic R costs O(m*n^2) field operations with naive
elimination. The projection arithmetic for each output costs O(m*n), with
O(m*n) field-element storage and m random bits. The CURRENT defensive Python
entry point repeats matrix/inverse construction and validation on every call,
so its charged per-call upper bound is O(m*n^2), not the cached-projection
cost. Bounded all-sign enumeration is ONLY an audit reference,
not how the scalable sampler operates. For an expensive A-adaptive R search,
its search/preprocessing must also be charged; conditional sampling equivalence
does not dequantize a hypothetical quantum search that produces R.

For A=[I_n|C] and the systematic R=(I_n,0)^T, outputs have the form
`(-C*z,z)`, z uniform in {1,2}^(m-n). This is exactly the stronger classical
baseline of guessing free signs and solving pivot coordinates. It improves
over a completely random sign guess by 2^n, but that gain is CLASSICAL.
For IID uniform C and m>n, its expected all-nonzero success is (2/3)^n:
for each fixed nonzero z, the n coordinates of C*z are IID uniform trits.
This expectation does not bound arbitrary adaptive R choices or nonlinear
decoders. It is not asserted for every individual matrix.

## Falsifiers And Actual Evidence

- ALL 26 nonzero one-row width3 matrices and ALL9 right inverses each:
  234 full source/subtraction/readout controls match the classical distribution.
- Vector controls include nontrivial n2/m4 and n2/m5 sources, all output words,
  failed signed witnesses, square invertible sources and global-offset controls.
- ALL81 systematic n2/width4 C matrices reproduce the exact (2/3)^2 average.
- An n32/width96 classical sampler test forbids exponential enumeration and
  the binary-error decoder; it still returns a valid (not necessarily signed)
  nullspace word. This is not a large quantum-state execution or hardness test.
- The independent JavaScript replay reconstructs both the actual quantum output
  and the random-sign projection on the live saved linear control.

An unexpected distribution mismatch would falsify the derivation, not prove
speedup. Allowing zero coordinates, selecting favorable matrices, normalizing
on success, ignoring R-search cost or testing only total mass would give a
misleading positive result. These are explicit test controls.

## Decision And Remaining Constructive Route

REJECT cheap LINEAR decoder replacement as a source of quantum advantage.
Do not compile or benchmark its quantum circuit further: use the exact cheap
classical sampler instead. The published nonlinear quotient decoder, nonlinear
coherent erasure, alternative input models and general DCP receivers remain
unresolved by this result. No generic no-go is established.

The next concrete hypothesis is PUBLIC nonlinear correction
`d(b)=R^T*b+Q(H*b)`, with H*A^T=0 and an explicitly computed low-degree Q.
It preserves shift covariance, but might alter all-nonzero witness mass.
Before scaling it, derive the actual output law, charge construction of Q,
and compare against free-sign Gaussian assignment and the published classical
subset-sum attacks. Enumerating coefficients to choose a favorable Q is an
exponential reference, not an algorithm. A positive result needs a uniform
efficient public rule and asymptotic success, not another small optimized curve.

    PYTHONPATH=theorems python -m pytest -q tests/test_ternary_linear_erasure_physics.py
    python theorems/ternary_decoder_filter.py --save
    node research/certificates/ternary_decoder_filter_crosscheck.js
