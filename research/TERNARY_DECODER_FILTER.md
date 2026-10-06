# Executed Ternary Decoder-to-Filter Audit

LOCAL IMPLEMENTATION AUDIT / REVIEW PENDING. Known literature reduction,
exponential finite-state verification, not a newly discovered or compiled
scalable quantum algorithm. No candidate acceptance or speedup claim.

## Published Component

[arXiv2609.40321v1, Section3](https://arxiv.org/html/2609.40321v1) credits the
reduction to Chen-Liu-Zhandry. It coherently prepares translated signed
two-point states, erases the secret register using a classical binary-error
decoder, then applies a local unitary to obtain signed zero-sum witnesses.
The publication separately bounds decoding errors and coherent missing terms.

## What Actually Runs Here

`theorems/ternary_decoder_filter.py` calls the actual quotient decoder on each
basis observation in a bounded verification table. It does NOT use a secret
oracle or an exhaustive classical root finder to provide the decoder.
Classical decoder failure is extended to output zero as a TOTAL FUNCTION for
the reversible subtraction, not accepted as a certified secret.

We execute controlled preparation, the complete secret-subtraction permutation,
all local readout unitaries, and the final distribution over EVERY residual
register. There is no projection/renormalization onto decoder success.
Every valid signed word is mapped by an invertible last-column shear to a
verified nonempty Boolean zero-sum witness. The shear preserves IID labels.

The simulator/table cost is explicitly exponential:3^(n+m) complex amplitudes
and3^m decoder calls. It audits a physical construction but does not compile
the decoder's classical operations into a scalable reversible gate circuit.
The classical primitive is polynomial only for each fixed degree D; no native
growing-two-power source bridge is supplied by this ternary construction.

## Executed Results

- Complete n1/m4 source: ALL81 IID label matrices, including8 with no signed
  solution. Mean failure0.3465935071. No favorable-instance selection.
- Mean decoder error and mean missing-vector squared norm are both62/243.
  The published coarse collision upper bound is vacuous at this small size;
  it is NOT evidence of a high-probability asymptotic algorithm here.
- Fixed n2/m5/D3 source from seed72105: full unheralded witness success
  0.4575617284. Exact pointwise failure certificate is79/144. Uniform random
  signs succeed1/16; disabling decoder erasure reproduces that mass exactly.
- Exhaustive classical reference also finds those witnesses. Its exponential
  search is NOT an efficient baseline, but these tiny controls establish no
  classical/quantum separation. A better small-instance probability is not
  the research objective and is not treated as a candidate.

## Self-Critique Controls

A constant shift d'(b)=d(b)+c only translates the final residual register by
-c. Tracing that register therefore leaves the witness distribution unchanged.
Our offset control increases the exact-secret error to23/24 while preserving
the physical success probability. Exact-secret error is a sufficient theorem
metric, not a necessary condition for good readout. This simple gauge check
has no novelty claim. The actual failure contrast disables decoder subtraction.

The ideal coherent sum is generally NOT normalized; its squared norm is
3^n times the valid-sign fraction. It is only a comparison vector. Using its
normalized version as the physical input would manufacture postselection.
The missing-vector and nonzero-residual terms are kept separately; pointwise
failure is bounded by their total squared norm, capped at one.

## Specialized Full-Target Source

For original IID A and independent uniform t in F3^n, append
B_last=-t-sum(A_i); keep the earlier columns unchanged. This is an invertible
affine map from (A,t) to an IID signed-sum matrix B. Convert any valid signed
zero word to Boolean form as above, orienting its last sign to+1. The resulting
extended Boolean word has last coordinate1 ALWAYS. Delete it: the remaining
word satisfies A*x=t. Success probability is exactly the signed solver's
unconditional success, with no hidden-marker inclusion factor.

This specializes the known signed-sum interface, NOT arbitrary Boolean
zero-sum solvers. The generic hidden-marker reduction retains its separate
contract. One extra public column and one known prepared qutrit are charged;
no extra unknown native coset state or chosen Fourier-label supply is granted.
The81 complete source controls also cover ALL independent target sources for
n1/original m3. At t0 the original Boolean witness may be empty, which is a
valid full-target witness; nonempty ZERO-SUM search remains a different task.
This ternary wrapper does not change the field or remove the one-word direct
DCP filter's density loss; it is not a universal density no-go for DCP readout.

## Verification and Remaining Work

17 targeted tests check full unitaries/permutations, tensor contraction,
ambiguity, no-solution inputs, all native labels, offset invariance, no-decoder
contrast, nonempty Boolean witness conversion and independent-target source
bijection/witnesses. An independent Node program
rebuilds the physical state and compares decoder tables against bounded root
enumeration. It checks84 matrices,4512 source branches,7128 output basis words
and59364 root-equation evaluations. These are not independent theorem review.

Next THEORY priority: seek a source-valid extension or a substantially better
coherent arithmetic primitive, not more small-instance curves. Ternary results
must not be copied into two-power DCP claims. For any new density window, audit
the strongest current classical subset-sum algorithms, their actual guarantees
and constants, and whether the proposed quantum construction is already known.

Gemini: expose both new reports as REVIEW-PENDING known-component audits,
preserving simulator cost, no-solution instances and no-claim gates. Integrate
CLI/registries/full-suite validation separately; do not accept a CandidateRecord.

```sh
python -m pytest -q tests/test_ternary_decoder_filter.py tests/test_ternary_quotient_decoder.py
python theorems/ternary_decoder_filter.py --save
node research/certificates/ternary_decoder_filter_crosscheck.js
```
