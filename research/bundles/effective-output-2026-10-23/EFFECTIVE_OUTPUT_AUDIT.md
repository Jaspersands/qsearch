# Effective Output And A Common Field

2026-10-23. Proposed composition audit; independent review pending.
The code prepares the exact contravariant module interface. It does NOT run
the published geometric converter or recover a hidden kernel.

## Question And Decision

The existing postprocessor returns the full Hom module and transported
End(B) order GIVEN a correct abstract kernel K. That is not automatically
an efficient evaluator for endomorphisms on arbitrary points of the original
modeled B. The available module-conversion theorem gives a route to this
stronger output, but its reference curve, field and variance conventions
must be respected.

The audit supplies a candidate field-normalization argument and explicit
left-module matrices. It also identifies an important scope restriction:
the reviewed conversion paper assumes p>3 and fixed dimension. Algebraic
controls at p=3 do not validate that geometric dependency at p=3.

## 1. The Reviewed Imported Result

The retained 48-page version of
[Page, Robert and Soumier, 2026/276](https://eprint.iacr.org/2026/276),
Theorem 6.9 and Corollary 6.10 on page 33, converts Hermitian modules into
maximal supersingular PPAVs over F_(p^2) and makes their Hom and End actions
effective. Section 2.1 fixes p>3, fixed dimension, and an explicitly evaluable
reference order. Section 6 uses the module directly. The GRH-dependent PIP
and unpolarized-isomorphism Corollary 6.11 are not necessary for this route.
Remark 6.7 treats arbitrary morphisms, including the bounded 2-primary
cofactor in its pseudo-double paths. We import these results, not their
implementation or an independent proof of the entire paper.

For parameter scope, its stated complexity is polynomial in log p after
reduced module inputs; the geometric source here also has a paid log ell
input. At minimum use ell<=p^C for a fixed C when importing that complexity
verbatim. Extending the conversion's bit accounting to arbitrary larger
ell requires a separate height analysis; it must not be assumed from a
passing large-prime lattice test.

## 2. Reference-Curve Normalization Without A Hidden Isogeny

Let the paid common field be k=F_(p^f). By the source contract every element
of the full supplied End(E) basis, and phi:E^g->B, is defined over k.
As proved in the prime-square flag note, Frobenius on E is an integer
scalar c: it commutes with a full quaternion algebra, whose center is Q.
Thus c^2=p^f, f=2m is even, and c=+/-p^m. Surjectivity of phi gives
Frobenius c on B as well.

Pay for ONE quadratic extension K/k. Frobenius on E_K and B_K is now

    c^2=p^(2m).

Choose a maximal elliptic curve E0/F_(p^2) with the same geometric
j-invariant as E, so its p^2-Frobenius is -p. Over K its Frobenius is
(-p)^(2m)=p^(2m), the same scalar. A geometric isomorphism i:E0_K->E_K
therefore commutes with Frobenius and is defined over K. No unknown isogeny
between different j-invariants is being requested.

For p>3, this reference choice can be made by constructing a curve with
the given j over F_(p^2), enumerating its at most six twist classes, and
selecting the maximal one by polynomial-time elliptic point counting.
Solve the bounded-degree isomorphism equations over K. Transport the
supplied order action by i. Keep the actual source-to-reference order
identification, rather than replacing it with an arbitrary abstract order
isomorphism: the latter can lose the ramified orientation discussed in the
conversion paper.

The same base extension also fixes all 8-torsion: c^2=1 mod 8 for odd p.
This is useful for the level-4 theta model and the field-preserving quotient
steps. It does NOT construct a giant field containing all auxiliary torsion.
At each auxiliary r separately, the r^2-torsion extension degree is bounded
by r(r-1) under scalar Frobenius. Fields and compatible embeddings are paid.

Important distinction: K controls geometric descent. A concrete backend's
theta-coordinate field may require its stipulated bounded coordinate
extension and explicit embeddings. These costs are separately charged;
the abstract argument is not an implemented coordinate-descent algorithm.
Use a common computational model supporting both the source primitives and
the converter. An arbitrary unrelated model does not acquire a free theta
conversion merely because the corresponding PPAV exists.

### Why Omitting The Extension Is Wrong

For p=7,11,19 the controls use E0:y^2=x^3+x over F_(p^2) and its quadratic
twist by a nonsquare d. Their point counts are (p+1)^2 and (p-1)^2, so they
are not isomorphic over that field. Adjoining u with u^2=d gives the map

    (x,y) -> (d x, d u y).

The controls enumerate the base-field points, verify the curve equations,
and check that Frobenius sends the map to its negative, whereas its square
fixes the map. They use SymPy finite-extension arithmetic. These are actual
elliptic-curve descent controls, not higher-dimensional quotient tests.

## 3. The Correct Left Module And Composition Order

Let J=J_K be the full numerator lattice from the preceding postprocessor.
As a right module, M=J/ell identifies with Hom(E,B), and its form is
ell*x^dagger*y. The conversion paper instead uses the LEFT module

    L=J^dagger,       h_L(r,s)=r*s^dagger/ell.

For r=a^dagger, its corresponding map B->E is a^dagger*phi^(-1).
If beta=phi*x*phi^(-1), its pullback is consequently

    beta^*: r -> r*x.

Write J also for the integral coordinate basis matrix of the numerator
columns. In the adjoint-row basis the integer matrix of this pullback is

    T_x = J^(-1) L_(x^dagger) J,

where L_y is left multiplication by the quaternion matrix y on columns.
Thus

    T_(xy)=T_y*T_x.

Treating this as T_x*T_y is wrong for noncommuting endomorphisms. The tests
include noncommuting target-order pairs and verify the reversed product.
They also check that every T_x commutes with the supplied left O action.

The contravariant map for phi itself is the inclusion J^dagger->O^g. In
standard row coordinates its matrix consists of the adjoints of the J
basis columns. Its index is ell^(2g), and the target/source Hermitian forms
satisfy the required ell-similitude identity. No free O-basis or PIP is
needed: the converter accepts a full finitely presented module.

Changing the reference from E to E0 transports the SAME order, split and
abstract kernel through i. It must not choose an unrelated mod-ell split
while leaving K unchanged. No large ell-torsion point basis is required.

## 4. Getting Maps On The Original B

Feed L and its full form to the published module converter, retaining its
reference-curve correspondence. Obtain a maximal polarized B0/F_(p^2) and
explicit maps representing a Z-basis of End(B0). The categorical meaning of
L ensures a polarized geometric isomorphism B0 -> B. After extension to K,
both Frobenius maps are the same scalar, so this isomorphism is K-rational.
Find one using the charged PPAV isomorphism primitive in the common model.

For any such v:B0->B, transport the computed maps by

    beta_j = v*beta_j^0*v^(-1).

This gives the FULL End(B) with evaluators on arbitrary supported points.
No alignment of phi is needed merely to output a full ring basis: any
polarized v transports the full ring. If a specified correspondence to the
earlier phi-conjugated algebra is required, align via the complete ordered
weak markings and one shared automorphism across levels. Do not silently
claim that an arbitrary v preserves that extra correspondence.

This is proposed CLASSICAL POSTPROCESSING after K has been obtained. Before
K is known, the weak image data do not give the full J or full L. Applying
the converter to the available proper submodule/suborder instead is not a
classical recovery algorithm.

## 5. What The Audit Does And Does Not Close

Closed by a proposed explicit argument: the quadratic reference-field
alignment, module convention, opposite composition order, and the reason
arbitrary target-isomorphism alignment suffices for a full ring output.
Checked in code: full integral left action, anti-homomorphism identities,
Hermitian multiplier and elliptic twist descent controls.

Imported, not independently re-proved: module-to-geometry conversion,
PPAV isomorphism/evaluation primitives and their stated parameter ranges.
Not executed: any module-to-PPAV conversion, target geometric endomorphism,
source geometric oracle or quantum receiver.

Remaining blockers: independent review of the source/receiver composition,
full uniform reversible compilation, parameter-height scope for stronger
output, same-input classical attacks, and novelty. No Shor-level algorithm
or classical hardness is established by this audit.
