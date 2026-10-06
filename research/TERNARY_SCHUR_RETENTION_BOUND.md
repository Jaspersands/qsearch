# Adaptive Native Linear Retention Bound

LOCAL APPLICATION / REVIEW PENDING. Established coding bound, applied to native
top-degree cancellation. Not a decoder, new general coding theorem, accepted
candidate, universal quantum lower bound or complete sieve complexity claim.

## The Gate Does Not Need Saturation

Let A be the native low-label matrix and W a k-dimensional physical frame
with nonzero support size s. Cancelling ALL component top terms at odd level L
requires A*W^(star L)=0. Suppose nonzero kernel words have weight at least d.
The admitted power, as a subcode of kerA, has minimum distance at least d.

Earlier Schur powers have at least that distance too: multiply a minimum-weight
word by a frame word nonzero on one support coordinate. The next power contains
a nonzero word of no greater weight. Puncture unused coordinates, set t=min(L,d)
and apply the known product-Singleton bound. Its product weight ceiling is
max(t-1,s-t*(k-1)); since d>t-1, this implies

```text
k <= 1 + floor((s-d)/min(L,d)).
For d<=L this equals floor(s/d).
```

The established baseline is [Randriambololona, Theorems2 and8, including
Remark3 on support](https://arxiv.org/pdf/1305.4840v3). The local contribution
is its native admission/source application, not the general bound.

This holds for EVERY source-adaptive linear frame: no W/A independence or
projective saturation needed. A distance premise still needs proof. The naive
stronger formula using t=L when d<L is FALSE; disjoint blocks can violate it.
Use actual support s, not only ambient width. Top admission lowers degree by
at least one; it is neither constant-degree admission nor secret decoding.

## Matrix Certificates Versus Statistical Guarantees

Bounded controls enumerate actual projective kernel words, give an exact
minimum-weight witness and histogram, and certify matrix distance. This is
exponential in kernel dimension, capped at eight, NOT a scalable distance
algorithm. Tests exhaust every subspace in five small native kernels at
degrees1,3,5,9. A two-dimensional disjoint frame on four coordinates is sharp;
the three-dimensional full kernel fails the retention bound and mixed gate.

For unfiltered uniform A in F3^(n by m), each projective nonzero word lies in
the kernel with probability3^-n. There are binomial(m,w)*2^(w-1) words of
weight w. The elementary union bound gives

```text
Pr[d_min(kerA)<d]
 <= min(1, sum_(w=1)^(d-1) binomial(m,w)*2^(w-1)/3^n).
```

This GLOBAL distance event bounds ALL adaptive frames simultaneously, unlike
the independent-frame estimate in the closure note. It does not certify a
specific matrix. No full-row-rank conditioning is used. Exact integer/rational
arithmetic avoids numerical tail errors. Postselected or correlated inputs
need a new source-law proof or a charged conditioning argument.

The25 live envelopes use m=2n, n16,32,64,128,256 and levels3,9,19,39,79.
At n256,m512, d>=81 except probability at most1/1000. Corresponding output
dimension ceilings are144,48,23,12,6. These are bounds, not achieved outputs.

## Revised Research Decision

For polynomial m in growing n, d>=floor(sqrt(n)) with overwhelming probability:
the union numerator is at most d*(2m)^d, whose logarithm is o(n), whereas the
denominator is3^n. If L also grows, the admitted fraction obeys

```text
k/m <= 1/min(L,d) + 1/m ->0.
```

Constant-rate exact all-component linear top-degree erasure is therefore
obstructed under this IID polynomial-width source, even before saturation.
Do not spend another pass pursuing that same ambition without changing a
premise. This is a scoped route obstruction, not an arbitrary decoder no-go.

Unsaturated frames might still beat disjoint dependencies: ceiling23 at L19
exceeds the distance-based disjoint ceiling6. Neither such a construction nor
its useful full-depth costs are supplied. Do not multiply stage ceilings into
a full recursion lower bound without proving the source transitions.

Escape routes: directly decode informative entangled native phases; use a
nonlinear/coherent receiver retaining extra information; exploit fewer unresolved
secret parameters with a new identifiability proof; or change the source law
and pay its cost. Fixed n or superpolynomial width also invalidates the stated
asymptotic scope, but is not automatically an efficient loophole.

Next high-upside target: direct shared-parameter entangled-phase decoding or
an implicit full-source modular receiver. Further retention construction is
worthwhile only with a plausible charged full-depth improvement within these
ceilings, compared to known sieves and legal classical measurements.

## Verification

```sh
python theorems/ternary_schur_retention_bound.py
node research/certificates/ternary_schur_retention_crosscheck.js
```

19 focused tests pass. Independent JS checks26 exact kernel words,756 complete
low-source matrices and31 exact probability envelopes. Final eleven-file
related regression:237 passed in26.23s. Scoped syntax/artifact verification is
not full-production validation. Gemini owns routine CLI/registry integration
and full-suite workflows. No candidate accepted or commit/push made.
