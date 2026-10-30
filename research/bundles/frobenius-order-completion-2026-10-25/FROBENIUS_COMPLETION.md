# Frobenius Powers Complete A Transported Target Order

2026-10-25. Proposed classical deduction with exact arithmetic controls.
Independent mathematical and prior-art review pending. Not a quantum
algorithm, cryptographic break, or executed attack on a geometric weak
isogeny. The preceding product-corner attack remains unchanged.

## Decision

The earlier completion test required a supplied endomorphism gamma with
L + gamma L = B[ell], where L is the UNKNOWN dual kernel. Replace it by
the weaker cyclicity condition

    L + gamma L + gamma^2 L = B[ell].

For a surface, this is already the full cyclic-span condition. Both-sided
Rosati multiplication then gives the full target endomorphism lattice
from 144 genuine integral maps. A public spectral condition on Frobenius
guarantees cyclicity for EVERY Lagrangian L, without receiving L as advice.
The characteristic polynomial needed for this test can itself be acquired
from the existing weak auxiliary-torsion interface.

This strengthens a SAME-INPUT classical baseline for a geometrically
specified subcase. It does not establish that all, or a positive fraction
of, the project's weak source instances lie in that subcase. In particular,
the actual curve control below has no constructed incoming weak isogeny.

## 1. Input Contract And The Field Trap

Keep the original single, globally consistent ell-polarized isogeny
phi:A=E^2 -> B, ell an odd prime distinct from the characteristic p.
The FULL source order End(A), its evaluations and norm bounds are known,
including the specified abstract split at ell used by the original kernel
output contract. This split does not supply geometric ell-torsion points.
B is a modeled principally polarized superspecial surface. A full target
order, product splitting, Hom basis and ell-torsion point basis are NOT
given. All endomorphism rings below are geometric ones.

At each usable small auxiliary prime r, the existing evaluator supplies
the full ordered image basis W_r=u_r phi_r with ONE common unit u_r.
It permits sufficiently many fresh levels, not only a fixed short
transcript. Source, target and isogeny are defined over the already paid
common field; auxiliary point-field construction and operations stay paid.
Do not form an uncharged compositum of all auxiliary fields.

Additional PUBLICLY CHECKABLE subcase: the target model and its principal
polarization are actually defined over k0=F_(q0). Its own Frobenius
tau=Frob_(q0) can be applied by coordinate powering. The full source order
and phi may be defined only over a larger field. No descent algorithm,
arbitrary isomorphism B^(p)->B, or hidden endomorphism is supplied.

If only the larger model field is available, use that field's Frobenius.
One cannot silently substitute a more useful small-field Frobenius. Scalar
Frobenius is useless here. If phi and its dual are defined over k0, L is
tau-stable and this attack's cyclicity premise cannot hold. The nontrivial
case necessarily uses a map whose dual kernel is not rational over k0.

## 2. The Local Tensor-Span Identity

Let V=B[ell], dim V=4, with alternating form J. Write U for a basis matrix
of L=ker(phi^dagger)=im(phi mod ell), a Lagrangian plane. Source maximality
at ell implies that the reductions of F_a=phi a phi^dagger, with a ranging
over a Z-basis of End(A), span exactly

    N_L = {U X U^T J : X in M_2(F_ell)}.

These are precisely the maps killing L with image contained in L. For an
actual integral endomorphism gamma let gamma^dagger be its Rosati adjoint.
Set S_k=sum_(i=0)^k gamma^i L. Since

    U^T J (gamma^dagger)^j = (gamma^j U)^T J,

the literal linear span of gamma^i N_L (gamma^dagger)^j, 0<=i,j<=k, is the
image of S_k tensor S_k under u tensor v -> u v^T J. This map is injective,
so its dimension is (dim S_k)^2. No freeness of noncommuting words, generic
rank heuristic, or inferred lift of an arbitrary matrix is involved.

If S_k=S_(k+1), S_k is gamma-invariant and no later power can enlarge it.
Starting at dimension two, at most two strict increases can reach four.
Thus eventual cyclicity is equivalent to S_2=V. One power may fail:
the exact local census includes rank sequence (2,3,4), not just (2,4,4).

## 3. Full Integral Order, Not Merely Local Rank

Take the Z-span T of the 144 ACTUAL integral maps

    gamma^i F_a (gamma^dagger)^j,  0<=i,j<=2, a=1,...,16.

If S_2=V, the preceding identity says T surjects onto End(B)/ell End(B).
Superspeciality and ell!=p give this quotient the full M_4(F_ell) action.
Nakayama gives T tensor Z_ell = End(B) tensor Z_ell. At every other prime,
including p, phi is an integral isomorphism after localizing: its inverse
is phi^dagger/ell. The original F_a already span the full target order
there, and T contains them. Hence T=End(B) globally.

For comparison, source words alone satisfy F_a F_b=ell F_(ab). They remain
in Z*1+span(F_a), whose reduction preserves L. This argument brings in a
genuine public geometric map; it does not evade that earlier obstruction
by relabeling products of the same source maps.

## 4. A Spectral Certificate Independent Of The Unknown Kernel

For tau=Frob_(q0), tau^dagger tau=[q0]. Let chi be its degree-four
characteristic polynomial reduced modulo ell. For monic f of degree d
with f(0)!=0, define

    f#(T) = T^d f(q0/T) / f(0).

Sufficient criterion: chi is squarefree, and EVERY irreducible factor has
even degree and equals its own f#. Reciprocity of chi as a whole is NOT
sufficient. Check the factors individually.

Proof: squarefreeness decomposes V into distinct simple F_ell[tau]-modules.
For eigenvectors with eigenvalues alpha,beta over an algebraic closure,
the similitude identity gives (alpha*beta-q0)<u,v>=0. Consequently an
irreducible component pairs only with the component indexed by f#. When
f=f#, that component is nondegenerate: its radical would also be in the
radical of V. Every invariant subspace is a direct sum of simple
components, hence nondegenerate. A proper such subspace of V has dimension
at most two, and cannot contain the dimension-two isotropic L. Therefore
the tau-cyclic span of EVERY Lagrangian L is V. Section 3 applies.

The criterion is sufficient, not necessary. On failure return UNKNOWN,
not hardness, noncyclicity of the actual L, or quantum evidence. One can
still build the lattice and use its full discriminant certificate; the
actual unknown L may be cyclic even though some other L is not.

## 5. Obtain chi Without A Characteristic-Polynomial Oracle

Use a complete weak image basis on B[r]. Apply the actual coordinate
Frobenius to these points and determine its matrix by pairings and small-r
discrete logarithms. A common scalar mask cancels in these coordinates.
The basis pairing is a nonzero scalar times the source alternating form,
so the tau matrix obeys the same q0-similitude equation. These operations
use only the already paid auxiliary access, not B[ell].

Write the integral polynomial as

    T^4 + a1 T^3 + a2 T^2 + q0*a1 T + q0^2.

Weil's bounds give |a1|<=4 sqrt(q0), |a2|<=6q0. At distinct usable small
odd r, collect a1,a2 modulo r. A product M>12q0 makes centered CRT unique
for both coefficients. There are polynomially many bits and small levels
in log(q0); p and ell can simply be excluded. Degree-four finite-field
factorization then checks the criterion in expected polynomial bit time.

The implemented reconstruction receives AUXILIARY MATRICES, not curve
points. It validates their polarization identities, coefficient bounds
and CRT budget, but it cannot certify that arbitrary matrices came from
one genuine surface. It reports geometric_input_verified=false.

## 6. Recover The Lattice And The Original Abstract Kernel

The same weak evaluator computes all F_a via

    (F_a)_r = ell W_r a_r W_r^(-1).

Apply tau and its adjoint on either side. At r!=p the latter has matrix
q0*tau_r^(-1); no costly geometric inversion or inverse-Frobenius oracle
is needed. The implementation returns all 144 small-torsion matrices.
Independent masks on basis vectors do NOT cancel, and are not this input.

Use ||x||^2=Tr(x^dagger x) and a paid bound M0 on all source basis squared
norms. Cyclicity of trace and polarization multipliers give

    ||tau^i F_a (tau^dagger)^j||^2
        = q0^(i+j) ell^2 ||a||^2 <= q0^4 ell^2 M0.

Thus every Gram entry is bounded in absolute value by q0^4 ell^2 M0.
Auxiliary traces and centered CRT at modulus >2q0^4 ell^2 M0 recover the
integer Gram. Only the logarithm of this bound controls the CRT budget.
The 144-by-144 Gram has rank 16. Select a rational basis; use its Gram
systems to express all generators; integer lattice normal form, retaining
generator combinations, gives a Z-basis and its specified auxiliary action.

The full geometric maximal target order has Rosati Gram determinant p^8.
An index-d sublattice has determinant d^2*p^8. Equality certifies fullness
given genuine input. It detects hidden ell-deficiency that small-prime
rank checks cannot. The trace-pairing/lattice method is the one already
used in PRODUCT_CORNER_ATTACK.md; see also
[Page--Robert--Soumier, Section 5.1](https://eprint.iacr.org/2026/276).
No general module-to-geometric-surface converter is inserted here.

Once that full order and evaluation correspondence are known, the
pre-existing target-endomorphism transport/divisibility attack in
research/SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md recovers
the SAME original abstract kernel K. This final composition is a dependency,
not a new kernel algorithm implemented in this bundle. Its field, norm,
small-torsion and source-order costs remain in the complete accounting.

## 7. Exact Controls And Their Limits

The smooth curve C/F_5: y^2=x^5+2x has Cartier--Manin matrix zero. Indeed
f^2=x^10+4x^6+4x^2 has zero coefficients at 4,3,9,8. Its Jacobian is
superspecial, not merely supersingular. For conventions and this distinction
see [Achter--Howe](https://www.math.colostate.edu/~achter/math/hwcm0618.pdf).
There is no semilinear-iteration inference here: the matrix itself is zero.
Direct enumeration and quadratic-character sums independently give
#C(F_5)=6 and #C(F_25)=26, hence chi=T^4+25.

Modulo ell=3 this factors as (T^2+T+2)(T^2+2T+2); each factor is irreducible
and self-reciprocal for multiplier 5. The canonically polarized Jacobian
is indecomposable, unlike the earlier explicit-product-only example.
BUT no incoming ell-isogeny from E^2, weak transcript, or geometric target
order has been constructed. The fixed p=5 curve is a finite consistency
control, not a demonstrated asymptotic family of attacked native inputs.

In a symplectic matrix model of this polynomial at ell=3, all 40 Lagrangian
planes pass. Twenty-four have cyclic ranks (2,4,4) and sixteen (2,3,4).
The corresponding literal matrix-span ranks are (4,16,16) and (4,9,16).
The latter sixteen exhibit a genuine extension beyond one-step mixing.
These counts are NOT frequencies of actual isogenies from a fixed source.

For the same curve polynomial the gate passes ell=31,43 but is UNKNOWN at
ell=47 and ell=2^127-1: distinct factors pair with each other. Keep those
original negative controls; do not replace their input primes to make the
gate pass. At the 127-bit prime an integral polarized-map control with
polynomial (T^2-6T+13)(T^2-4T+13) does pass. That map is NOT asserted to
be a Frobenius of the characteristic-seven arithmetic fixture.

Two full quaternion-order controls, (p,ell)=(7,11),(11,19), complete by
integer HNF to index one and Gram determinant p^8. Every one of 144 public
auxiliary action matrices agrees with its independently evaluated integral
map, and a common weak scalar changes none of them. Those HNF controls use
REFERENCE coordinates, not a geometric extraction algorithm.

## 8. Attempted Falsification And Remaining Debt

- Repeated irreducible factors: an explicit invariant Lagrangian exists;
  its span stays dimension two. Squarefreeness cannot be dropped.
- Distinct reciprocal factors: the whole polynomial is reciprocal but an
  irreducible invariant Lagrangian still exists. Whole-polynomial symmetry
  alone is not a certificate.
- Scalar Frobenius: the generated span stays dimension four as a space of
  endomorphisms. For the curve polynomial tau^4=-25, so extending the base
  field to F_(5^4) replaces the useful Frobenius by a scalar one.
- Rational kernel over k0: Frobenius preserves L. No assertion that merely
  seeing a small-field target makes every supplied isogeny vulnerable.
- Nonmaximal source order or nonsuperspecial B: the full M_4 local action
  used by the proof may fail. Do not generalize to these inputs.
- Fake or insufficient auxiliary transcripts: algebraic matrix checks do
  not establish genuine geometry or global consistency. Short CRT returns
  UNKNOWN; the original source promise and paid access are still essential.
- Geometric applicability: a real target example does not prove that a
  supplied prime-polarized weak source to it exists with the stated cost.
  Construct and verify such inputs before assigning empirical coverage.
- Prior art and independence: this is an unreviewed local deduction. It may
  be an application of known endomorphism-recovery machinery, not a novel
  theorem. No new independent reviewer was commissioned for this pass.

## 9. A Recent Conjugate-Isogeny Route Does Not Close Acquisition

[Pham, arXiv:2609.17330v1, Theorem A and Sections 2.2, 4.2](https://arxiv.org/html/2609.17330v1)
gives a multiplier bound (p^3/2)^(1/5) for a separable polarized isogeny
eta:B->B^(p) when B has p^2-Frobenius [-p]. Its argument fixes an
unpolarized isomorphism to E^2, then constructs a rank-five lattice in
those coordinates. That is not the missing public coordinate-acquisition
algorithm for our weak input. The resulting xi=Frob_p eta is self-adjoint
and satisfies xi^2=[pN]. Neither the size bound nor the written lattice
construction supplies an efficient evaluation oracle on our input.

Our further deduction: xi^2 scalar means L+xi L is already the full cyclic
span; higher powers cannot repair failed one-step mixing. In fact, for ANY
self-adjoint map on a symplectic surface, (u,v)-><u,xi v> restricted to L
is alternating. Its rank is zero or two, so dim(L+xi L) is two or four,
never three. An explicit self-adjoint quadratic control has an invariant
Lagrangian and fails completion. This does not refute Pham's existence
theorem or rule out useful actual xi; it prevents promoting it to the
stronger all-kernel attack without new acquisition and cyclicity arguments.

No remaining step justifies claiming a general classical break, native
hardness, or quantum advantage. The constructive next test is geometric
execution of the complete public interface, followed by a search for
source families that provably avoid this and the previous classical attacks.
More random local matrices or larger finite censuses are not the priority.
