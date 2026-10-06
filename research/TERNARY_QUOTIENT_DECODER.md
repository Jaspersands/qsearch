# Ternary Quotient Decoder

LOCAL IMPLEMENTATION AUDIT / REVIEW PENDING. This implements a published
classical primitive, not a new quantum algorithm, accepted candidate or speedup.

## Literature Component

[Kothari et al., arXiv:2609.40321v1](https://arxiv.org/html/2609.40321v1),
Section4.2/Definition4.11, supplies the algorithm. Inputs are explicit ternary
equations b=A^T*s+e with binary errors. The decoder builds polynomial
annihilators, certifies degree-D leading surjectivity in the truncated algebra,
then constructs low-degree multiplication operators. Their commutator, field
and sample relations are closed under every variable operator. The resulting
quotient determines whether there are zero, one or multiple compatible secrets.

Theorem4.12 requires 500n<=m<=n^2 with D=ceil(500n^2/m). None of our small-degree
controls meets that regime. The complete published sample-time algorithm also
has enumeration branches that we have not implemented. Runtime is polynomial
in the low-monomial dimension, not uniformly polynomial in growing D.

## Implementation Checks

`theorems/ternary_quotient_decoder.py` does not enumerate secret assignments.
It returns a secret ONLY when the full invariant quotient has dimension one
and the recovered vector satisfies every binary-error equation. Deficient
leading certificates, inconsistency and ambiguity remain distinct failures.

Fixed seed72105 is used without favorable rerolls:

| n | m | D | low dimension | leading rank/dimension | compatible secrets | result |
|---|---|---|---|---|---|---|
|2|5|3|6|2/2|1|recovered|
|4|8|3|15|16/16|6|ambiguous|
|6|18|3|28|50/50|2|ambiguous|
|8|30|3|45|112/112|1|recovered|

The last case fails degree-two leading surjectivity:30 samples cannot span36
quadratic features. This demonstrates a working higher-degree primitive on
one instance, NOT an asymptotic improvement or an empirical success theorem.
Independent bounded root enumeration checks small quotients; SymPy's Groebner
engine checks actual rewrite identities, multiplication lifts and relations.
Those checks are not independent implementation review or theorem review.

## Exact Counting Guard

In R=F3[x]/(x_j^3), multiplication by ell^2 for any nonzero linear ell has rank
dim(R_(D-2) on n-1 variables). A linear coordinate change sends ell to x1:
the cube ideal is invariant by Frobenius; x1^2 kills precisely multipliers
containing x1. All remaining monomials have distinct images.

Thus at least ceil(dim(R_D)/dim(R_(D-2),n-1)) nonzero samples are necessary for
leading surjectivity. At n8,D3 this is16. It is NOT sufficient: overlaps can
lower joint rank, and full leading rank does not ensure a unique secret.
This is a local exact algebraic check, with no novelty assertion. AppendixC
of the paper separately studies dependencies in degree-three XL; its full
linearized column-count criterion is not this leading-only criterion.

## Source and Research Boundary

Binary-error learning and Boolean zero-sum search are different tasks. A
classical binary-error decoder does not itself solve Boolean subset sum.
Nor does a fixed-prime decoder supply a native growing-two-power DCP source
conversion. Scalable quantum compilation and classical subset-sum competition remain
essential unimplemented work. Full production integration belongs to Gemini.

Subsequent finite-state audit: [Executed Ternary Decoder Filter](TERNARY_DECODER_FILTER.md)
implements the published coherent reduction on bounded controls, with source,
failures and full output distribution charged. No scalable reversible decoder
circuit is compiled. Compare any new parameter window against current
classical subset-sum methods before claiming advantage.

```sh
python -m pytest -q tests/test_ternary_quotient_decoder.py
python theorems/ternary_quotient_decoder.py --save
```
