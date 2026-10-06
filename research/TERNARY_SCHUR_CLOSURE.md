# Higher Schur Admission And Projective Saturation

LOCAL APPLICATION / REVIEW PENDING. Known coding-theory structure, applied to
the actual native phase hierarchy. No decoder, new source construction,
accepted candidate, generic source-adaptive no-go or speedup claim.

SUCCESSOR: `TERNARY_SCHUR_RETENTION_BOUND.md` supplies a scoped adaptive
retention ceiling WITHOUT saturation, using kernel distance and the known
product-Singleton theorem. Unsaturated frames are not an unrestricted
constant-rate escape under growing-depth IID inputs.

## Why This Pass Matters

`TERNARY_PHASE_DEPTH.md` gives a weighted L-fold Schur tensor at odd native
level L=2r+1. Expanding all basis multisets has binomial(k+L-1,L) terms for a
k-dimensional restriction. That is the wrong representation for screening
depth-sensitive subspaces.

Compute W^(star d) recursively: multiply a basis of the previous span by the
k original basis words and perform exact GF3 elimination. Every span has
dimension at most m, the number of physical coordinates. Store actual product
words with their factor indices, rather than exponentially many monomials.
At most k+(L-1)*m*k candidates are processed. Elimination has a conservative
O(L*k*m^3) arithmetic bound; this is not a bound on quantum decoding.

A has all native low-label rows. The exact top-degree restriction gate is

```text
A*W^(star L)=0.
```

Any failed basis word gives an explicit list of L logical directions and an
exact nonzero native mixed derivative. Checking all span basis words certifies
ALL mixed top terms, not just diagonal polarization. Admission lowers degree
by at least one; it does not certify constant degree or a useful state decoder.
The top tensor is affine-branch independent, so this gate is not zero-syndrome
postselection. No full quantum restriction instrument is executed here.

## Stable Odd Powers Have Disjoint Projective Blocks

Let rho_i in F3^k be row i of the physical frame. Discard zero rows. Group the
remaining rows by proportionality, rho_i=epsilon_i*rho_C with epsilon_i in
{1,2}, using a representative whose first nonzero entry is1. Let g_C have
entry epsilon_i on this class and zero elsewhere. The g_C have disjoint
supports; c is the number of nonzero projective classes.

Any odd homogeneous product is a linear combination of g_C. Conversely, odd
functions on F3^k are spanned by canonical monomials with exponents0,1,2 and
positive odd total degree at most2k-1. A lower odd degree can be raised by two
without changing its evaluation, using x^3=x. Therefore

```text
W^(star L)=span{g_C} for every odd L>=2k-1.
```

Earlier saturation can be certified by the computed rank c. Padding a known
odd product by two copies of an existing factor preserves its values and
produces a valid witness at the higher requested order. No exponential
enumeration is hidden in this jump.

This stable structure is established coding theory. The general regularity
bound is c-k+1; see [Randriambololona, Theorem2.35 and
Corollary2.36](https://arxiv.org/pdf/1312.0022v3). The implementation records
that known bound and directly certifies actual saturation. Its separate
characteristic-three bound above follows from canonical finite-field functions.
Neither Schur stabilization nor disjoint stable generators are claimed novel.

Stable admission is exactly A*g_C=0 for every class. In that case the original
frame lies inside span{g_C}, a disjoint-support kernel subspace of dimension
c>=k. Its reconstruction is explicit from the projective representatives.
If kerA has minimum nonzero word weight delta, then each class contains at
least delta coordinates, giving k<=c<=floor(m/delta). A useful delta bound
needs its own certificate; this module does not solve code minimum distance.

This rules out interpreting a saturated overlapping frame as retention beyond
ALL disjoint-support kernel constructions. It does not say that fixed blocks
of n+1 are optimal: shorter native dependencies can exist, and finding useful
disjoint dependencies is a separate construction problem.

## Actual Native Controls

1. The27-coordinate evaluation frame A(x)=x3, W=(x1,x2,x3) passes level3:
 its cubic Schur span has dimension10. Its fifth span has dimension13 and
 saturates all nonzero projective classes. Levels5,9,19 fail with exact native
 mixed witnesses. Higher-order witnesses are padded legally, not guessed.
2. An overlapping two-column native frame on six coordinates is saturated
 and admitted at L19. Explicit refinement produces three disjoint signed
 kernel words. This is positive geometry, not a charged source sampler or
 an implementation of a complete full-secret receiver.
3. An unfiltered native label calibration at n3,m24,L19 has retained width21.
 Its Schur ranks are21,24,24 at degrees1,2,3. Saturation avoids the
 68,923,264,410 degree19 basis multisets:966 candidates, at most23,184
 coordinate products and556,416 elimination-entry operations. The exact
 native derivative witness is(13122,13122,6561) mod19683.

## Fixed-Frame Source Probabilities Are Not Adaptive Search Costs

For a frame fixed independently of uniform low A, an odd span of dimension
b admits with probability3^(-n*b). Conditional on AW=0, admission probability
is3^(-n*(b-k)): W lies inside every odd power. Complete enumeration of27 and
729 low-source matrices verifies these two formulas in small controls.

These probabilities are INVALID after selecting W from A, including choosing
its kernel chart. Native records explicitly disable their application to the
displayed source-adaptive frame. They are reference source laws, not rarity
bounds against all adaptive algorithms, union bounds over unspecified search
spaces or quantum sample-complexity claims.

## Try To Kill The Direction

The top gate can often saturate very early, leaving only disjoint kernel
geometry. A proposal relying on overlapping high retention must either remain
unsaturated at the required native degree or explain how its disjoint
dependencies improve total source throughput. Full residual phase order,
lower-degree source correlations, all outcomes, informative parameter rank,
source acquisition and complete secret-digit recovery remain unproved.

Escape routes still open: unsaturated spaces with k substantially larger than
phase depth; source-adapted low-Schur-growth evaluation codes; useful entangled
packets without degree elimination; high-label-adaptive transforms with a new
conditioning proof; nonlinear instruments or implicit full-source decoders.
No theorem here forbids them. Slow Schur growth engineered in a code is not
evidence that its weighted constraints can be found in an IID native matrix.

The next high-upside question is CONSTRUCTION under the actual random source,
not further diagonal or fixed-level tensor sweeps. Candidate admission needs
an efficiently found informative family, charged full-depth pipeline and a
decoder beating applicable known phase algorithms and quantum sieves.

## Verification

```sh
python theorems/ternary_schur_closure.py
node research/certificates/ternary_schur_closure_crosscheck.js
```

23 focused tests pass: complete mixed monomials versus compact spans, signed
projective reconstruction, odd nesting, higher native falsifiers, exact source
probabilities, adaptive-scope gates and large-width resources. Independent JS
uses direct reduced monomials, separate batch rank, and native trace recurrence:
79 projective classes,1,824 monomial words,6 native witness components,3
disjoint refinement words and756 complete low-source matrices.
Routine CLI/registry integration and full-production validation remain
Gemini's work; the report is not an accepted CandidateRecord.
