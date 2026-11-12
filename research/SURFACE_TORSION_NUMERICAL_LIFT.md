# Numerical torsion lift from closed divisors

2026-11-12. Scoped classical bridge, independently source-checked in
`audits/reviews/2026-11-12-surface-mascot-lift.md`. This advances the native
surface comparator by paying numerical lifting once a faithful arithmetic
model is available. It does not pay reconstruction precision or that model.

## Exact statement

Given a genus-g curve with good reduction at P, an actual point O, a faithful
separable plane/function-field presentation of its good special curve, and
polynomial-size exact generic Riemann--Roch coordinates, an actual prime-to-P
ell-torsion class represented by closed divisors can be lifted to precision
P^E with polynomial bit cost in the presented sizes, g, numerical E, residue
extension degree, log P and log ell. No geometric support splitting is needed.
This is classical Mascot/Khuri-Makdisi arithmetic; no quantum advantage follows.

For d0=2g+1 and D0=d0 O, a class D-gO becomes D'=D+(d0-g)O,
represented by L(2D0-D'). Closed-place RR constructs this subspace. One common
residue field of polynomial degree supplies more than 5d0 evaluation points
away from denominators and exceptional loci: Hasse--Weil and factoring random
projection fibres give a polynomial capped clock. Unit derivatives lift them
over one unramified local extension. Their supports are independent of D.

Compute exact RR functions in a common-denominator normal form and saturate
their coefficient lattice. Faithful reduction and a nonzero reduced denominator
give independent reduced rational functions. Integrality of evaluations at
more than deg(D0) points forces genuine section integrality: a primitive
nonintegral section scaled into H0(D0) would otherwise have too many zeros
on the special curve. Nakayama then certifies the full integral RR lattice.
Use all products/constraints and full linear systems in the source's practical
randomized shortcuts; these variants remain polynomial.

At each precision-doubling step Mascot Algorithm10 lifts any Jacobian point
modulo P^e to P^(2e), then multiplies by N=0 mod P^e, N=1 mod ell. The error
lies in J_e/J_(2e), whose formal-group law is additive because the ideal is
square-zero; its exponent divides P^e. This proves unique torsion lifting,
including P=2, without the source's excessive global logarithm claim.

## Decisive corrections and remaining inputs

* Good reduction of the abstract curve alone is insufficient. Replacing y
  by Y=P y changes a good equation into Y²=P²f(x), with nonreduced displayed
  reduction. The faithful presentation and RR coordinate-size bound are
  explicit upstream obligations, not supplied by the words "good reduction".
* The source's blanket log:J1->P O^g isomorphism fails at two. On
  y²+xy=x³+4x+1, discriminant -4225, T=(-1/4,1/8) is nonzero 2-torsion
  reducing to O with formal parameter 2. The square-zero proof repairs the
  algorithm, not that assertion.
* Unique effective degree-g extraction requires residue h0(T+gO)=1.
  Its Abel differential then has zero kernel and cokernel by RR, so the
  divisor lifts with unit pivots, even with nonsplit or nonreduced support.
  Generic-characteristic-zero h0=1 alone is insufficient.
* Original Frobenius requires conjugation of O and the appropriate divisor
  correction. A row permutation needs the source's stable evaluation/base
  data. Numerical lift uniqueness does commute with arithmetic Frobenius.

The primary source is Mascot, arXiv:1808.03939, retained July2019 text,
Algorithms9/10, Theorem2.23 and Remark1.6:
`audits/sources/surface_module_2026/mascot_lift.{pdf,txt}`. Remark1.6 explicitly
leaves rational reconstruction uncertified without a height bound. The paid
`2026-11-12-closure-lift` call ended empty/truncated and supplies no evidence;
the independent source proof above is separately recorded.

Next decisive obligation: construct a faithful good auxiliary-prime model
and polynomial-size exact RR coordinates from the growing-degree native
cover, and bound canonical torsion coordinates. No full classical point count,
uniform reconstruction precision, speedup, hardness or separation is claimed.

## Native auxiliary-model input now supplied from a charged plane equation

The entire independent review
audits/reviews/2026-11-12-native-normalization-lattice.md was parent-read.
For a separable geometrically integral plane function field over a charged
number field, one can construct its two finite-free normalization charts,
their multiplication tables and Laurent transition matrices in polynomial
degree and BIT size. Start with a monic generator (scale by the original
leading coefficient if necessary), O=K[x][y], Delta=disc_y F. Trace duality
gives O subset B subset Delta^-1 O. Reduced numerator coefficients modulo
Delta form d*deg Delta unknowns; integrality is exactly a LINEAR vanishing
test on local numerator jets through e_Q ord_alpha Delta, at most d deg Delta.

Kozen's passive residue algebras are kept in direct sum. Center each inverse
Newton map before truncation: X=u^m(v+a)^t, Y=u^n(v+a)^s, with 0<=t<m,
1<=s<=n. Outputs with m or n above the jet order vanish; surviving unit
powers have polynomial degree. Centered compositions use at most N factors
per level, not N^depth, giving polynomial coordinate bits. This fills the
specific jet-height gap; an arithmetic operation count or an absolute
height in an unspecified field basis alone does not fill it.

The lattice Delta B contains Delta K[x]^d. Its Hermite columns can be found
by bounded affine K-linear systems, testing successive monic pivot degrees
0..deg Delta and membership via the ORIGINAL jet matrix. Ratios of minors
bound coefficient heights without recursively accumulating basis bounds.
Normalize infinity separately via u=1/x, z=u^h y. Convert the bases and
verify both transitions are Laurent polynomial inverses.

Record denominators, passive-algebra unit norms, nonzero comparisons,
subresultants and rank witnesses in an explicit nonzero integer M of
polynomial bit length. For every prime away from M, the same local branch
and lattice calculation gives the FULL reduced normalization. Two charts
glue finite flat over P1, with normal curves over perfect residue fields;
proper flatness plus smooth fibres gives a faithful good model. No maximal
number-field order, integer factoring, collective residue splitting, or
growing-variable Groebner smoothness test is used.

For one regular-fibre point O above x=a, the existing two-chart construction
computes L(kO) by polynomial-size coefficient systems: if the transition
exponents have absolute value<=A, write (x-a)^k f in the finite basis with
coefficient degrees<=k+A. Lift the fibre idempotent in B0/(x-a)^k to impose
vanishing at the OTHER fibre points without splitting them. Append required
RR rank/fibre witnesses to M. A prime P above a numerical threshold and
coprime to M*ell*|G| is found among polynomially many small primes because
the excluded integer has polynomial bit length; do not factor it.

This pays the AUXILIARY model/RR prerequisite from the charged plane equation.
The equation/field's native construction remains a separate input theorem.
PRESCRIBED target p might divide M; the argument does not solve that problem.
Intrinsic torsion encoding heights now follow from SURFACE_TORSION_HEIGHT_CHAIN,
while aligned Galois-invariant reconstruction remains separate.

## Canonical closed coordinates are now computed, not supplied

Parent read the entire stable numerical-closed-algebra review, including
its source-checked Section7:
audits/reviews/2026-11-12-numerical-closed-algebra.md. The earlier assertion
that the Abel map is etale was not alone an algorithm producing its inverse.
The following explicit construction pays that interface from the KM point.

After choosing the common basepoint b, initialize KM with D0=d0*b,
d0=2g+1, and E1=(d0-g)b. Existing closed residue classes can be reinitialized
by finite-field RR and uniquely lifted again; no high-precision basis-change
oracle is assumed. Apply Mascot Algorithm7 to x=-t and stop at line5.
Its line2 is the degree-g space in the class gb+t, with residue h0=1,h1=0.
The output is W0=L(B-D_t), B=(d0+g)b, where D_t is the unique effective
representative of t+gb. Only the subspace is computed, not its support/ideal.
Use source equation2.15 and the algorithm's divisor identity: the prose in
Remark2.21 has an opposite-sign typo.

Choose H=pi^*(infinity), monic plane degree D, A0=kH with
deg A0>=d0+3g+1, and A=A0+D H, disjoint from D_t. The KNOWN space
L(A-B) only imposes jets at b. Both its divisor and B-D_t have degree>=2g+1,
so the actual section-product theorem (Mascot DivAdd proof, independently
Anderson4.3.1) gives

    L(A-D_t)=span L(A-B)*W0.

Use all products; residue surjectivity, H1 vanishing and Nakayama certify a
unit-pivot basis at full P^e precision. Source KM spaces remain in L(5D0);
the new pole-A products use the already paid coefficient multiplication or
an enlarged evaluation bank, not an invalid unchanged source ambient.

Now V=L(A), W=L(A-D_t), V0=L(A0). The quotient V/W is the free rank-g
closed divisor algebra, and V0 surjects onto it. Select residue-independent
columns f_i from V0. Both x*f_i and y*f_i lie in V, so reducing in the unit
basis [W,f_i] gives multiplication matrices M_x,M_y and the unit. For a
common residue-good z=x+c*y, its power basis is again a unit basis. Solve
for monic A_t(z)=0 and x=B_t(z), y=C_t(z), preserving all multiplicities.
If the original coordinate was nonmonic, the paid monic change plus a unit
denominator inverse recovers it. All exceptional loci were avoided at residue.

Every solve is polynomial size with unit pivots and preserves full precision.
No canonical divisor ideal, nonfield Groebner solver, individual support
splitting, uncharged inverse-Abel operation, or global torsion field is input.
Intrinsic heights and exact rational reconstruction remain separate bounds;
the first is paid in SURFACE_TORSION_HEIGHT_CHAIN.md.
