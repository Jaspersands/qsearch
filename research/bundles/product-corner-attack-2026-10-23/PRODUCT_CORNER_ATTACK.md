# A Classical Attack On Explicit Product Targets

2026-10-23. Proposed deduction with exact arithmetic controls. Independent
review is pending. This removes a nontrivial subfamily from quantum
advantage claims; it is NOT a classical solution for an arbitrary modeled
superspecial surface, and no geometric attack has been executed here.

## Decision

Let the existing weak source be a polarized ell-isogeny

    phi: A=E^2 -> B=E1 x E2,

with ell an odd prime different from the characteristic p. The target is
an EXPLICIT PRODUCT with its product principal polarization. Its factor
inclusions iota_i and projections pi_i are available, not secret data.
The source full order End(E), its action and norm bounds remain supplied
as in the original source contract. No target order or Hom basis is given.

Put L=ker(phi^dagger) in B[ell]. If L intersects each E_i[ell] trivially,
the 64 integral endomorphisms

    e_i * phi * a * phi^dagger * e_j,    e_i=iota_i*pi_i,

for a ranging over a Z-basis of End(A), generate the FULL End(B) as an
abelian group. Their small-torsion actions can be computed from the
original weak evaluator with its scalar canceled. A full lattice basis
and its Rosati Gram can then be recovered by bounded CRT and integer
linear algebra. The existing target-endomorphism transport attack
recovers the original abstract K=ker(phi) in classical polynomial time.

The transversality promise need not be trusted: the resulting lattice's
discriminant certifies completeness. On a failed check, this branch
returns UNKNOWN, not classical hardness or quantum evidence.

## 1. Do Not Misapply OneEnd

An initially tempting argument was to obtain one non-scalar endomorphism
of each factor and invoke a polynomial-time OneEnd-to-EndRing reduction.
That is insufficient. [Page--Wesolowski, Theorem 7.1](https://arxiv.org/html/2309.10432)
uses a solver on queried curves, not a single supplied endomorphism.
Transporting an endomorphism alpha along a path eta and back only returns
deg(eta)^2*alpha when duals are used; it does not supply independent data.
The distinct [given-one-endomorphism problem](https://arxiv.org/html/2309.11912)
has a discriminant-dependent bound, not the claimed generic polynomial
solution. The corner argument below does not use either reduction.

## 2. Obtain Enough Genuine Endomorphisms Without Exact phi

For every source basis element a, define F_a=phi*a*phi^dagger. On auxiliary
r-torsion, choose actual coordinates on the full A[r] and B[r], with
r distinct, small and coprime to p*ell. If the weak evaluator gives
W=u_r*phi_r, where the same unit u_r masks the complete ordered basis,

    (F_a)_r = ell * W * a_r * W^(-1).

The scalar cancels. The image basis can be converted to the target product
basis with pairings and small-r discrete logarithms. No inverse of phi
on arbitrary points, exact weak scalars or large ell-torsion is obtained.
Apply the known product projections on both sides to obtain each corner's
exact small-torsion matrix. These matrices describe actual integral maps;
they are not merely arbitrary matrices hypothesized to lift to maps.

The weak source must permit fresh evaluations at sufficiently many small
levels, with the original common-scalar promise. A fixed insufficient
torsion transcript is NOT the same input. Field degrees and point access
remain paid; no common compositum of all auxiliary fields is constructed.

## 3. Local Completion At ell

In Tate coordinates let M denote phi modulo ell, and M^dagger its adjoint.
Both have rank two; im(M)=ker(M^dagger)=L. Because L is Lagrangian in
V=V1 orthogonal_sum V2, transversality to both V_i implies

    rank(pi_i*M)=2,       rank(M^dagger*iota_j)=2

for every i,j. Source maximality at the unramified prime ell gives
End(A)/ell End(A)=M_4(F_ell). Consequently

    { pi_i*M*X*M^dagger*iota_j : X in M_4(F_ell) }
        = M_2(F_ell).

Indeed, the first rectangular factor has a right inverse and the second
has a left inverse, so any desired 2-by-2 matrix has such an X. Thus the
corner lattice maps onto each of the four independent 2-by-2 blocks of
End(B)/ell End(B). Nakayama's lemma gives the full ell-adic target lattice.
Here End(B) has the full matrix reduction because B is superspecial and
ell is prime to p. This step would be false for a supplied deficient
source order or a nontransverse dual kernel.

## 4. All Other Primes, Including p

At every rational prime q != ell, phi is invertible in the integral
q-adic Hom category, since phi^dagger/ell is its inverse. Therefore

    span_Zq(F_a) = End(B) tensor Z_q.

The corner lattice contains every F_a, since sum_i e_i=1 on BOTH sides.
It is already full at every such q. Combined with the ell-adic statement,
equality of lattices follows globally. In particular, there is no hidden
p-saturation or factorization assumption in this argument.

## 5. Recover The Lattice And Certify It Without Knowing L

For the product Rosati norm, each e_i is an orthogonal projector. Therefore

    ||e_i F_a e_j||^2 <= ||F_a||^2 = ell^2 ||a||^2.

The inner products of any two of the 64 maps are bounded by the geometric
mean of these squared norms. Small-torsion matrices give their exact
residues using Tr(X^dagger*Y); the adjoint uses the known polarized
pairing. Choose a CRT modulus strictly greater than twice the largest
absolute bound, so centered reconstruction yields the full integral Gram.

Pick a rationally independent set of 16 generators. Gram linear systems
express every other generator in this rational basis. Integer lattice
normal form, retaining the generator combinations, produces a Z-basis
of their span and its Gram. Only polynomial-sized rational/integer
calculations are required, in fixed dimension. No general geometric
module-to-PPAV converter is needed for these sufficiently explicit maps.
This is the trace-pairing technique of
[Page--Robert--Soumier, Section 5.1](https://eprint.iacr.org/2026/276),
applied after the generation argument above, not before it.

For a maximal order M_2(O) in M_2(B_(p,infinity)), the determinant of the
reduced-trace pairing has absolute value p^8: O has determinant p^2,
and the matrix-algebra pairing has four quaternion blocks. Rosati
adjunction is an integral automorphism of determinant +/-1, so the
positive Rosati Gram also has determinant p^8. All superspecial product
target orders are locally maximal with this same discriminant.

If the computed lattice has index d in End(B), its Gram determinant is
d^2*p^8. Thus equality to p^8 certifies FULLNESS given the geometric input
contract. It does not validate a malicious source or a fabricated Gram.
Unlike checking ranks at small auxiliary primes, this certificate detects
deficiency at the hidden prime ell as well.

The resulting full basis, its exact small-torsion actions and Gram meet
the prior transport attack's requirements. Reconstruct coordinates of
all F_a, reduce those coordinates modulo ell, find the stabilizer algebra
P_K, and recover K as the image span of its trace-pairing annihilator.
This composes with the existing proof; it does not assume K as advice.

## 6. Failure Cases And Actual Scope

If L has a nonzero intersection with V1, isotropy forces
L=l1 direct_sum l2 with a line in each factor. Each corner then has only
one-dimensional image as a space of matrices modulo ell, not four.
Corner completion alone cannot saturate at ell.

For the diagonal Gaussian control

    phi=diag(6+5i,6-5i),    ell=61,

the completed lattice still has index 61^16. Its Gram determinant is
p^8*61^32 and is rejected. This is a failure of this particular completion
method, NOT a hardness result for that explicit example.

For the mixed controls

    phi=[[a+bi,c],[-c,a-bi]],  ell=a^2+b^2+c^2,

with (a,b,c)=(1,0,2),(3,2,2),(6,3,4), corner completion gives the complete
M_2(O) at ell=5,17,61 respectively. The initial transported lattice had
index ell^16. The test uses the full noncommutative quaternion order,
not only its Gaussian suborder.

There are (ell+1)^2 split Lagrangians and ell*(ell^2-1) transverse ones in
the abstract four-dimensional symplectic space. The tests enumerate all
40 at ell=3 and all 156 at ell=5. These are COMBINATORIAL counts, not a
claim about the frequency among real isogenies from a fixed E^2 to a
product target. Conditioning on that geometric source can change the
distribution radically.

Most importantly, an arbitrary modeled principally polarized surface is
not supplied with these product projections. A polarized-indecomposable
Jacobian has no such orthogonal splitting. Although a superspecial
surface is geometrically an unpolarized product, this does not give an
efficient splitting map or small projector norms. Computing those maps
can itself contain the missing information. Do not import them as free
representation-conversion advice.

The proof assumes a full known source order, actual product geometry,
prime-to-characteristic polarized isogeny, valid weak evaluations and
paid auxiliary access. Remove any of these and the conclusion requires
another proof. Independent mathematical/prior-art review is pending.

## 7. A Single Mixing Endomorphism Suffices More Generally

There is a useful extension which does NOT assume a product target. Suppose
one actual integral gamma in End(B), its small-torsion actions and a bound
on its Rosati norm are already available. If

    L direct_sum gamma(L) = B[ell],

then the lattice generated by F_a, gamma*F_a, F_a*gamma and gamma*F_a*gamma
is full End(B). The equality is only a sufficient condition; the algorithm
can again use the discriminant certificate without knowing L.

Proof: in a basis starting with L, the image of all F_a modulo ell is

    N={ [[0,X],[0,0]] : X in M_2(F_ell) }.

Write gamma=[[A,B],[C,D]]. The displayed condition is precisely that C is
invertible. The span of N, gamma*N, N*gamma and gamma*N*gamma is all M_4:
their four block patterns give an invertible block-triangular linear map
on four independent matrices X. Equivalently, the columns generated by
[I;0] and gamma*[I;0], and the rows generated by [0,I] and [0,I]*gamma,
are both full bases. Away from ell the F_a already suffice, so the same
local-to-global proof applies. This argument extends to fixed g with
g-dimensional L and an invertible g-by-g lower-left block.

The norm budget grows by a known polynomial factor: with
G=max(1,||gamma||_Rosati), every new generator has norm at most
G^2*ell*max_a ||a||. Thus its logarithmic CRT budget is still polynomial
in the paid norm descriptions. No unproved efficient division is used.

In the product case gamma=e_1 is a mixing map under transversality. An
integral involution with two symplectic two-dimensional eigenspaces is
another possible source: an explicitly evaluable extra automorphism of
a bielliptic genus-two Jacobian can supply this input, IF the same mixing
condition holds. This is a conditional route, not a claim that every such
curve or every kernel satisfies the condition.

Scalar Frobenius, +/-1, and any gamma preserving L fail this condition.
The integral controls show that a known diagonal sign involution completes
the mixed source order, while a scalar map leaves index 61^16. A target
with only scalar known automorphisms supplies no useful map by this route;
one may not grant an arbitrary mixing endomorphism to fill that gap.

The same local lemma holds in dimension one, provided the weak isogeny
from a known full source order is ALSO given. It is not a reduction from
one supplied endomorphism alone. Do not transfer its conclusion to that
weaker input model.

### A Concrete Geometric Probe: Frobenius Self-Conjugacy

Test whether the polarized target B is isomorphic to its coefficientwise
p-Frobenius conjugate B^(p). If an actual polarized isomorphism
u:B^(p)->B is found, the composite

    gamma = u * Frobenius_p

is an explicitly evaluable integral endomorphism with
gamma^dagger*gamma=[p] and squared Rosati norm 4p for a surface. This uses
the target's real geometry and the paid isomorphism primitive, not an
unknown full target order. The norm budget is only logarithmic in p.
Apply the full-lattice certificate to the four-map family using this
gamma. There is no need to construct its action on inaccessible ell-torsion.

For a target already modeled over F_p, u is the identity. This can be
useful even when its polarized automorphism group contains only +/-1.
It is DIFFERENT from the scalar Frobenius of the larger paid common field.
For targets not polarized-isomorphic to B^(p), the test supplies no map.
Every field and the actual isomorphism evaluation must still be paid.

An important failure control: if the original isogeny and its source and
target are all defined over F_p, its dual kernel is Frobenius-stable, so
this gamma preserves L and fails the mixing condition. Thus F_p descent
alone is not a general break. More generally failure of the discriminant
certificate remains UNKNOWN. This probe has not been run on actual
surface models in the present bundle.

### Why Source-Map Algebra Alone Cannot Supply The Missing Map

For every a,b in End(A),

    F_a*F_b = ell*F_(ab).

Consequently the integral ring generated by the F_a and 1 is exactly
Z*1 + span_Z{F_a}. Modulo ell it is F_ell*I + N, with N^2=0 and
dimension 1+g^2. It preserves L. Arbitrarily long noncommutative words,
linear combinations, or inverses of its units cannot produce a mixing
gamma. The surface controls check dimension five and show the useful
involution lies outside that span.

This rules out an entire unproductive symbolic search space, not all
classical algorithms. A successful extension must bring in actual
geometric information or justified integral division/saturation outside
that ring. Merely rewriting the known transported maps is insufficient.

## Research Consequence

Exclude certified transverse explicit-product instances from speedup
claims. They are a same-input classical falsifier, stronger than the
opaque-label square-root baseline for this subfamily.

Next ask whether one can obtain an integral mixing endomorphism OUTSIDE
the transported local parabolic algebra on an
indecomposable target from its actual public geometry. Rational
conjugates of source projectors are not automatically integral. Repeated
products of already available integral maps need not escape the same
ell-adic obstruction. A new source claim must survive that attack, not
merely an equality-only benchmark.
