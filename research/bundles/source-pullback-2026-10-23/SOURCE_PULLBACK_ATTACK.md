# Recover Kernel Directions Directly In The Known Source Order

2026-10-23. Local mathematical deduction and exact arithmetic prototype.
Independent review and novelty determination pending. No real surface
geometry, new quantum algorithm, cryptographic break, or general classical
solution is asserted.

## Decision

The existing product/mixing-map attack reconstructs the FULL target order
before extracting the hidden kernel. That intermediate step is unnecessary
when an additional target endomorphism is genuinely available. Pull it back
to the already known source order instead. Its reduction modulo ell directly
reveals a subspace of the original kernel.

For a surface, products of length at most TWO in the known maps and their
adjoints exhaust this particular orbit-span test. They can recover the full
kernel even when every first-level image together spans only a line. No new
weak evaluations, target-order computation, or ell-torsion point construction
is needed for these products. The arithmetic prototype demonstrates that
strict improvement over the single mixing-map condition.

This is a stronger CLASSICAL gate on the existing application, not another
quantum candidate. Most importantly, it does not supply the missing target
map on an arbitrary indecomposable target. That is still the application
bottleneck. A failed test does not establish classical hardness.

## 1. Preserve The Actual Input

Keep the existing prime-to-characteristic polarized weak-isogeny input:

    phi: A=E^2 -> B,       phi^dagger phi = [ell],
    phi phi^dagger = [ell],
    K=ker(phi),            L=ker(phi^dagger).

Here ell is an odd prime different from the characteristic p. Both kernels
are Lagrangian of dimension two on ell-torsion. The full source order
End(A)=M_2(End(E)), its integral basis, multiplication, Rosati adjoint, trace
Gram, norm bounds and small-torsion actions are already part of the source
contract. The target is modeled with its principal polarization. No full
End(B), Hom basis, target splitting, exact phi, or kernel is granted.

For this attack ONLY, an additional actual integral map gamma in End(B)
must be computable from the public geometry or otherwise genuinely supplied.
Its small-torsion action and a bound on its squared Rosati norm must be paid.
A target with no such useful map cannot be declared dequantized. The
existing product projections, a real self-conjugacy/Frobenius map, or an
explicit nontrivial automorphism are possible inputs; their existence is
not automatic. A hypothetical map from a reference target order is not an
acceptable substitute.

At each auxiliary prime r, the weak images of a complete ordered source
basis must have ONE common unit scalar:

    W_r = u_r * phi_r,     u_r in F_r^*.

Scalars may differ between levels. Independent per-point masks, fixed
insufficient transcripts, or incompatible maps at different levels violate
the contract. Local pairing checks are necessary, not sufficient, to prove
global compatibility with one phi. The prototype never claims to certify
that promise.

## 2. Recover One Integral Source Endomorphism By Bounded CRT

Define the actual integral source map

    alpha_gamma = phi^dagger * gamma * phi in End(A).

For r coprime to p*ell, phi is invertible on r-torsion and hence

    (alpha_gamma)_r = ell * W_r^(-1) * gamma_r * W_r.

The unknown common scalar cancels exactly. There is no evaluation of phi
on ell-torsion and no interpolation of a large-degree isogeny.

Let e_1,...,e_16 be the known integral source basis, with positive integral
Gram G_ij=Tr(e_i^dagger e_j), using reduced trace. Write alpha=sum_j x_j e_j.
At each auxiliary level the action matrices give residues of

    b_i = Tr(e_i^dagger alpha),      b = G*x.

The Tate-module matrix trace equals this reduced trace. Cyclicity and the
polarized isogeny identities give the EXACT norm equality

    Tr(alpha^dagger alpha) = ell^2 * Tr(gamma^dagger gamma).

If the latter target norm is at most C, Cauchy--Schwarz gives

    |b_i| <= ell * sqrt(C*G_ii).

Use distinct legal small primes with product M strictly greater than twice
the largest integral bound. Centered CRT then recovers every b_i uniquely;
the exact rational system x=G^(-1)b gives the integral coordinates of alpha.
The implementation checks integrality, the resulting norm, the known
source discriminant p^8, the level plan, and all supplied source splittings.
These checks do not turn dishonest norm or geometry promises into a
certified input. In particular, finite residues cannot certify arbitrarily
large unknown maps without the supplied global norm bound.

The largest auxiliary level can be polynomial in the bit lengths of the
norm bounds, ell and p. Number and size of the levels, not just the number
of callback calls, enter the complexity. This prototype accepts and checks
a bounded public level plan rather than silently escalating to ell-sized
queries. The source-field audit supplies separate paid small torsion fields
under its scalar common-Frobenius promise; no compositum is free.

### No Independent Target Torsion Basis Is Needed

The four weak images themselves form a basis of B[r]. Pairings and small-r
discrete logarithms express gamma on that basis. For the implementation's
standard symplectic-frame convention, obtain the common pairing multiplier
mu=u_r^2 ell from those points and rescale each second basis vector by
mu^(-1). This normalizes the target form to the same J as the source.
No square root of mu and no recovery of u_r is required. The resulting W
is a similitude with multiplier mu, as checked by weak_pullback_actions.

Per used level, one map requires four weak source basis images and four
target-map images. If source basis actions are not already cached, 64 source
basis-map point evaluations suffice. Pairing/coordinate extraction and all
point-field work are additionally charged. Recorded point counts are access
REQUIREMENTS, not claims of executed geometric operations.

## 3. A Rank Test That Directly Recovers K

On ell-torsion put M=phi_ell and D=(phi^dagger)_ell. Then

    ker M = im D = K,       im M = ker D = L.

For every known gamma,

    (alpha_gamma)_ell = D * gamma_ell * M,
    im(alpha_gamma)_ell is contained in K,
    rank(alpha_gamma)_ell = dim(L+gamma(L))-2.

The first inclusion holds regardless of the rank. Thus a rank-two image IS
K; a rank-one image is a certified kernel line under the input promises;
rank zero supplies no image information. This avoids full target lattice
generation, integer saturation of that target lattice, and a target-order
discriminant test.

The reduction uses an abstract PUBLIC splitting End(A)/ell -> M_4(F_ell),
not points of A[ell]. Its construction or supply must be charged. The
prototype checks a supplied quaternion splitting and then uses exact finite
field linear algebra. Its fixture-only splitting routine enumerates only
small test fields and is not a claimed large-ell implementation.

The old single-map transversality condition L+gamma(L)=B[ell] is exactly
the rank-two case. This is a simpler way to exploit that same condition,
not a new input or a proof that the condition is common on natural sources.

## 4. Products Can Complete Partial Information

Include adjoints of the known maps at no additional source query cost:

    alpha_(gamma^dagger) = alpha_gamma^dagger.

For two maps,

    alpha_gamma * alpha_delta = ell * alpha_(gamma*delta).

Consequently compute each product pullback by multiplying in the KNOWN
source order and dividing every coordinate by ell. This division is proved
integral by the displayed identity. It is not an arbitrary saturation
oracle and not the invalid attempt to divide a transported source map
without a kernel-stability proof. Input inconsistency is rejected if exact
division fails.

Here is a completeness statement for this particular test, independent of
the unknown kernel. Let Gamma be the chosen target maps, optionally closed
under adjoint. For words of length at most t define

    R_t = span { w(L) : length(w)<=t },     R_0=L,
    U_t = span { im(alpha_w)_ell : 1<=length(w)<=t }.

Since M maps onto L and D has kernel L,

    U_t = D(R_t),       dim R_t = 2 + dim U_t.

Moreover R_(t+1)=R_t+sum_(gamma in Gamma) gamma(R_t). If a step fails to
increase its dimension, R_t is invariant under the whole generated algebra
and no longer word can increase it. Starting at dimension two in dimension
four, either R_1 already fills the space, R_1=L and stabilizes, or R_1 has
dimension three. In the last case R_2 either fills the space or stabilizes.
Therefore length at most TWO exhausts this orbit-span test.

It returns K exactly iff the Gamma-generated algebra takes L onto the whole
target vector space. Otherwise it returns the exact image span available
from ALL words in that algebra, not just a failure of an arbitrarily short
search. This is not completeness for all classical algorithms or for all
information in the integral pullbacks.

With s original maps, adjoints make at most 2s letters and there are at most
2s+(2s)^2 pullbacks. No new torsion queries are needed after reconstructing
the original s maps. Each multiplication has polynomial bit cost, with
only two word levels. For general dimension g the same proof gives g levels,
but naive enumeration is s^g; this prototype and polynomial bound are
deliberately SURFACE-only.

If the returned isotropic subspace has rank r, the Lagrangian extensions
consistent with THAT SUBSPACE number

    product_(i=1)^(2-r) (ell^i+1).

They are not necessarily compatible with the full weak input, the integral
pullbacks, or the public geometry. The count is not a hardness or posterior
probability claim. Output PARTIAL or NO_INFORMATION never resolves those
other classical possibilities.

## 5. Exact Controls And Attempts To Disprove The Claim

The controls use genuine integral quaternion orders and polarized matrix
endomorphisms, but do not construct elliptic curves or surface quotients.
The extraction routines receive only the public source data, residue
callbacks, and bounds. Secret phi appears only in the arithmetic fixture
callbacks and final independent reference comparison, not as an argument
to either extraction routine.

### Strictly Stronger Than The First-Level Test

Use the maximal order Z[1,i,(1+j)/2,(i+ij)/2] in (-1,-11), with i^2=-1,
j^2=-11 and ij=-ji. Let phi=[[1,2],[-2,1]], so ell=5. In row-major
quaternion-basis coordinates take the target endomorphism

    gamma = (0,1,0,0, -1,-1,0,0, -1,1,1,-1, 1,0,-1,-1).

The exactly reconstructed alpha has coordinates

    (8,1,-6,-2, 1,-3,-2,6, 1,7,3,1, -3,4,1,-3).

The combined images of alpha and alpha^dagger have rank ONE modulo five.
The second word layer has rank TWO and equals the actual ker(phi). Even
gamma alone gives ranks one then two, so this is not only an adjoint trick.
This fixture shows that the earlier single mixing-map gate missed a valid
classical recovery route. The target here is an explicit product already
covered by other attacks; it is not a new naturally hard surface instance.

### Frobenius Relations Are Not An Automatic Break

In (-1,-7), set gamma=diag(j,j), ell=11, and choose phi diagonal with
entries selected from 2+j and 2+ij. Both have norm eleven. Then

    gamma^2=-7,       gamma^dagger=-gamma,
    Tr(gamma^dagger gamma)=28.

Using zero, one, or two factors 2+ij gives final kernel-image ranks zero,
one, or two respectively. The rank-one case remains rank one at the second
layer because gamma^2 is scalar. There are twelve Lagrangian extensions of
the returned line, not twelve proven equivalent full inputs.

These are exact Frobenius-RELATION controls, not a claim that a modeled
target Frobenius was evaluated. Actual polarized Frobenius self-conjugacy
still has to be supplied by the geometry. In particular, if phi is defined
over the same smaller field, its dual kernel is Frobenius-stable and the
image test fails, as the earlier audit requires.

### Things That Deliberately Fail

- A scalar target map gives alpha=ell times a scalar and no kernel image.
- A map manufactured only as phi*a*phi^dagger gives alpha=ell^2*a and no
  image. Its words cannot supply the missing extra geometry.
- Independent point masks can violate the similitude test. Conversely,
  an incorrect local similitude can pass; local checks do not certify one
  global weak source. A regression test keeps this distinction explicit.
- Insufficient CRT range, illegal levels, repeated primes, nonintegral
  coordinates, incorrect source discriminant, and visibly incompatible
  common-kernel maps are rejected rather than treated as evidence.
- No inference about general OneEnd follows. The weak phi and a FULL source
  order are essential additional inputs.

## 6. Relation To Literature And Existing Work

[Chen et al., IsERP](https://arxiv.org/html/2305.19897) supply the established
weak-isogeny setting and existing quantum elliptic result. Do not advertise
an elliptic specialization here as the discovery of that application.
[Montessinos](https://arxiv.org/html/2601.18050) studies conversions between
superspecial-surface problems under specified representation assumptions;
its existence results do not grant our extractor an unknown target order.

The trace/CRT ingredient is the same standard reconstruction idea already
used in the neighboring product-corner audit, with the known SOURCE Gram
instead of an unknown target lattice. The new local composition being
checked here is the direct source-image and two-layer orbit criterion. No
claim that this composition is unpublished is made.

## Research Decision

Run this gate BEFORE constructing a large geometric quantum source whenever
an actual additional target map is available. The existing single-map gate
is too weak: partial maps and their products can suffice. Record precisely
which maps came from the real input and their costs.

On an indecomposable target without a useful known map, nothing here closes
the missing-source problem. An actual geometric self-conjugacy computation,
a different justified source of a target map, or a complete real source
execution remains more valuable than more matrix fixtures. No new registry
negative result should be admitted until an original-input replay succeeds.
