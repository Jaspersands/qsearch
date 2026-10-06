# Full Polar Operators And Pivot-Span Obstructions

LOCAL DERIVATION / REVIEW PENDING. These are necessary conditions for a
particular exact first-layer fixed-pivot architecture, not a decoder, a general
DCP impossibility result, an independently reviewed theorem or a novelty claim.
The first-layer normalizer with background-adaptive pivots remains valid.
The conditional higher-carry quartic obstruction remains unresolved.

## Export The Whole Search Space

Let C=ker(B) be the physical binary parity code of a full-rank zero-origin
packet, with k logical coordinates. Choose a common-isotropic chart U of
dimension d>=n and a complement V of dimension b=k-d. The first residue bit
is quadratic. Its slope in the U coordinates is

    L(y) = L0 + sum_a y_a L_a,                L_a in Mat_(n,d)(F2).

L0 depends on the middle labels. Each L_a depends ONLY on the binary labels.
For each output l the exported operator D_l:U->V* has rows L_a[l,:].
The compiler checks actual isotropy and derives these arrays using public
packet arithmetic at direction/background basis vectors, not assignment or
secret-state enumeration. Both the full operators and provenance are saved.

An n-dimensional pivot span W, represented by n independent vectors in U,
gives a square pencil M(y)=L(y)|W. Its variation dimension is

    r(W) = dim sum_l D_l(W).

Rebasing W multiplies M on the right by an invertible matrix and cannot change
its rank or fix a singular background. Restrict a genuinely different span.
The exported operator family permits that without recompiling every background.
Changing the complement by U directions also leaves the polar variation image
unchanged, because U is common-isotropic.

## A Field-Valid Dimension Gate

If M0+S lies entirely in GL_n(F2), then M0 is invertible and M0^-1 S has no
nonzero eigenvalue in F2. The arbitrary-field dimension bound therefore gives

    dim S <= n(n-1)/2.

The primary proof is [de Seguins Pazzis, Theorem9 and Proposition10](https://arxiv.org/pdf/1004.0579).
Its induction works over arbitrary fields, including F2; it is not the
field-size-qualified classification theorem in a later paper. We checked that
proof's field assumptions, but this project still needs independent review.

Thus r(W)>n(n-1)/2 excludes EVERY constant part for that W, even when its
variation is correlated and the earlier column-separable gate is inconclusive.
This bound is necessary, not sufficient. Correlated binary nonsingular pencils
with nonzero variation remain real positive controls.

There is also a cheap ALL-SPAN bound. Restriction Mat_(n,d)->Mat_(n,n) loses
at most n(d-n) dimensions, so

    r(W) >= dim span{L_a} - n(d-n), for every n-dimensional W.

If this exceeds n(n-1)/2, every such fixed span in this U fails. This says
nothing about a different isotropic U, adaptive pivots or a quantum decoder.

Finding some bad background is not automatically a useful mass estimate.
Here 1+det(M(y)) is a nonzero Boolean polynomial of degree at most n, in r(W)
independent image coordinates. The elementary Boolean minimum-support bound
gives failure fraction at least 2^(-min(n,r(W))) under UNIFORM background.
This can be exponentially small. The certificate does not call it constant
failure unless the following stronger block structure is actually present.

## Complete Row Blocks Give Stronger Failure Mass

Let S=span{L_a} and use entrywise binary pairing to form S_perp. Define E as
the annihilator of the span of ALL rows of ALL matrices in S_perp. Exactly

    F2^n tensor E is contained in S.

This is the largest row space with that property: e_l*x is orthogonal to S_perp
for every l precisely when x annihilates every such row. Binary elimination
computes E without background enumeration. For every basis vector of E and
every output row, the report gives a background producing that private row
variation and verifies the resulting matrix exactly.

On W put t=dim(E|W). The pencil image contains completely independent variation
in t columns after rebasing W. Conditional on the other columns, those t columns
are uniform independent n-bit vectors. Unless the other n-t columns already
have full column rank, success is zero. Otherwise their probability of extension
to a basis is

    product_(j=1)^t (1-2^(-j)).

Consequently t>=1 forces failure fraction at least1/2. Exact all-background
pivots must satisfy W subset E_perp. Since t>=max(0,n-codim(E)), codim(E)<n
rules out EVERY n-dimensional fixed span inside this U with a quantified bound.

These are deterministic statements for the actual chart and constant part.
W may be chosen from public middle labels, but must stay FIXED as y varies.
Nonuniform/postselected background distributions cannot borrow these fractions.

## Weighted Radicals: A Charged Necessary Search Filter

For a direction w, its background variation is the map y->(D_l(w) dot y)_l.
If that map is surjective, some y cancels L0(w), and any pivot W containing w
fails. A direction that can belong to an exact all-background W must therefore
lie in

    union_(lambda != 0) ker(sum_l lambda_l D_l).

The code computes the SPAN of this union, with an explicit 2^n-1 combination
budget. If its dimension is below n, all eligible W in this U are excluded.
Passing is not enough: a span of a union need not lie in the union, much less
support a nonsingular pencil. Exceeding the combination budget is recorded as
SKIPPED, not as a mathematical negative result. This is not a scalable search
algorithm. The selected-span gate additionally probes its basis directions and
pairwise sums and supplies a verified singular background when it finds a
surjective direction. Failing to find one is not a success proof.

## Exact Code-Theoretic Reformulation

Write R=C_perp=rowspace(B) and W_phys for the physical image of W. The polar
form is beta_l(w,z)=sum_i B_li*w_i*z_i in F2. A physical covector vanishes on
C exactly when it lies in R. Therefore, using coordinatewise multiplication,

    r(W) = dim(R + R*W_phys) - n.                    (1)

Because U is common-isotropic, the covectors already vanish on U; restricting
them to V loses no further rank. The physical Schur-product calculation is an
independent representation of the same actual pencil image. This is an
application of standard code-product structure, not a novelty assertion.
Small product dimension is necessary here; it does not prove an inverse.

One tempting construction fails cleanly. If physical basis vectors of W have
disjoint supports and the UNUSED physical columns of B still span F2^n, then
any assignment on those supports can be completed outside them into C.
The polar column variations can thus be varied independently: the pencil image
is column-separable. If every column varies, the earlier cycle certificate
excludes every constant part. Disjoint short code relations are not by
themselves a usable nonsingular correlated pencil.

The outside-rank hypothesis matters. The existing native n2 positive control
has disjoint supports, but unused-column rank only1; its variation columns are
correlated and its two matrices are invertible. The new test preserves it.

## Actual Findings And Next Decision

For the three existing systematic finite profiles (n2,3,4), the full chart
dimensions d are19,23,32 and background-image ranks are13,29,48. All three
complete row blocks have dimension1. Weighted-radical span dimensions are18,
22,31. The previously selected basis pivots fail, but these gates do NOT close
all alternative n-dimensional spans. Small-n zero-label columns make these
profiles unsuitable as asymptotic evidence. The subsequent
`DCP_SYSTEMATIC_SOURCE_TRANSPORT.md` resolves the identity-prefix source concern:
a low-only row transform gives this exact systematic law at constant native
acceptance cost. This does not make three profiles a source-average decoder
success theorem, nor remove rare structured-tail penalties.

The revised target is a NEW physical subcode W with useful correlated
R*W structure, a genuinely source-valid nonsingular pencil, and a compact
higher-carry graph that survives the fixed-pivot quartic control. A merely
low-rank product, rebased failed span or favorable determinant sample is not
that target. The classical two-forward-call arithmetic baseline still applies
if the final transport is a classical public evaluator.

[Noncommutative-rank certificates](https://arxiv.org/abs/1512.03531) and
[shrunk-subspace algorithms](https://arxiv.org/abs/2207.08311) are possible
structural leads, not implemented solutions. The first abstract specifies
sufficiently large base fields; the second specifies the complex field.
Neither abstract supplies this prescribed-dimension binary pivot search or a
descent to F2. Do not equate low Schur expansion with the usual shrunk-subspace
inequality. The curated source audit records these unresolved applicability
checks rather than adding them as supporting evidence for an accepted candidate.

## Verification And Delegation

Sixteen focused tests include all4,096 two-by-two two-generator pencils, all
seven two-planes in a three-dimensional binary control, physical operator
identities, private-row witnesses, source-bit dependencies, exact Schur ranks,
disjoint-support controls, rebasing and positive correlated/triangular controls.
The independent Node checker verifies saved operators directly from physical
binary labels, block witnesses, code-product ranks and bounded fractions.
These checks are not theorem peer review or complete production validation.

Gemini: expose the report and source audit using existing registry/CLI paths,
retain the unaccepted dense-transport contract and all scope gates, and run
production regressions. GPT: derive a constructible source-valid correlated
subcode/pencil or abandon this exact fixed-pivot architecture if its required
native coverage cannot be proved. Do not restore circuit search or spend GPT
usage on routine frontend wiring.
