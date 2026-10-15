# Noise-Matched Zero-Label Source Restoration

CONDITIONAL LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This repairs a source
composition statement under explicit assumptions. It does not certify actual
lattice-source noise, improve supply, or claim a new quantum speedup.

Run `python qsearch.py dcp-noise-matched-source` and
`node research/certificates/dcp_noise_matched_source_crosscheck.js`.

## The Gap

The coarse-only pairing theorem gives uniform descended labels before the
paid zero filter, and uniform NONZERO labels afterward. In the pure case,
inserting label0 with a known |+> restores the uniform label source.
For noisy outputs this fails: the true label0 block can be dephased, and pure
|+> has excess coherence. Earlier tests correctly expose the discrepancy.

The repair is to keep the public visibility record and MATCH that noise at
the injected zero label, rather than automatically assuming purity.

## Conditional Source Theorem

Assume original phase qubits are independent balanced dephasings, conditioned
on one fixed unknown classical secret. Their public visibilities are independent
of the fresh higher label lifts. The pairing program uses only coarse public
labels; the original diagonal is flat. On a pair x,y the emitted visibility is
v=product_{i:x_i!=y_i} v_i and its label is uniform in G=Z_(2^(t-h))^n,
conditional on that coarse pair and its visibility. At least one coefficient
of the higher-label sum is +/-1, so character translation is bijective.

Discard the original HIGHER-label transcript at the output interface. Retain
coarse records, output label and visibility. The joint classical-quantum law is

```text
sum_v pi(v) sum_{lambda in G} |lambda,v><lambda,v| / |G|
                            tensor rho_s(lambda,v),
rho_s(lambda,v) = [[1, v*exp(-2*pi*i*<s,lambda>/|cyclic factor|)],
                   [conjugate, 1]] / 2.
```

Here a sum over v may also include other coarse public metadata; its label
independence is conditional on that metadata. Merely checking uniform LABEL
marginals is insufficient. Zero rejection costs1/|G| and leaves pi unchanged.

Starting with one PAID nonzero output, draw a public zero coin of probability
1/|G|. On nonzero keep its label/qubit/visibility. On zero discard the paid
qubit, prepare |+>, apply Z with probability(1-v)/2, and set label0. Retain v.
This prepares rho_s(0,v) without knowing s and exactly restores the whole joint
label/visibility/CQ law. The reset is a known-state CPTP operation, not an inverse
of the unknown source or an uncharged copy of an unknown state.

The module exports exact dyadic stochastic channel instructions. Density tests
execute their CPTP mixture on actual finite phase states. A hardware reset/Z-coin
backend is NOT implemented. Finite census validation is not a proof that real
source premises hold; the artifact explicitly marks them ASSUMED, not inferred.

## Closure And Paid Supply

Fresh independent batches give independent outputs conditional on s, with
uniform labels independent of their public visibilities. These satisfy the
same abstract input promise for another coarse-only descent. Heterogeneous
public visibilities are allowed; their products must be tracked using ORIGINAL
lineage, not merge depth. This supplies a conditional induction for this source
family, not a natural-problem noisy-source certificate.

The live workflow checks two COMPLETE levels. First: q32 to q8 on four scalar
inputs of visibility3/4, fixed coarse labels(1,1,1,1), all8^4 higher lifts and
all eight pair outcomes. The output tag law is visibility(3/4)^2 with mass3/4
and visibility(3/4)^4 with mass1/4, independent of all eight labels.
Second: four independent restored q8 inputs, ALL8^4 label tuples, ALL16
visibility-tag tuples with exact3:1 weights, and ALL eight physical pair
outcomes. Descended label modulo2 is exactly independent of its visibility
tag. Matched injection restores the complete joint law again.

These finite levels are source-channel calibrations, not candidate oracle
problems or evidence of scalable secret recovery. The symbolic proof, not the
small census, is what extends to vector labels and growing moduli.

For THIS wrapper (which always consumes a nonzero output BEFORE its zero coin),
the first level costs4/(1-1/8)=32/7 original qubits in expectation; the second
costs4/(1-1/2)=8 first-level outputs, hence256/7 original qubits. Ideal no-failure
cost was16. These are implemented-protocol costs, NOT lower bounds on all
wrappers: a known public visibility distribution could sometimes be sampled
classically before deciding to spend quantum supply. No such saving removes
the preceding baseline's exponential depth or native visibility barrier.

## How This Can Fail

- Pure zero replacement overstates noisy coherence. Tests retain that negative
  control, then verify the matched dephasing repair.
- Public visibility may correlate with higher labels. Even uniform label
  marginals do not imply a product label/visibility law. The finite gate rejects
  such joint histograms; the theorem explicitly requires independence.
- Retaining old full A makes descended label deterministic conditional on the
  pair, rather than uniform. The interface must really discard that transcript.
- Correlated faults can share the same per-register marginals but different
  pair coherence. Marginal visibility is not an independent-source certificate.
- Reused batches, unmodelled purifying work or coherent secret side information
  can invalidate the product-state induction. Only the stated conditional
  classical-secret product model is covered.
- An exact source-family closure is not efficient supply, useful visibility,
  a decoder, or a hard natural-problem reduction. All those remain open.

Any mismatch in the joint label/visibility probabilities, or in the actual
zero-block density produced by the channel, falsifies this repair directly.
The independent checker regenerates both source censuses and all channel
probabilities using integer/rational arithmetic; it does not trust pass flags.
