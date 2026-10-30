# A Native Bielliptic Gate For The Weak Surface Source

2026-10-24. Local mathematical derivation with exact controls. Independent
review and novelty assessment are pending. No complete native weak-isogeny
instance, geometric hiding function or quantum algorithm was executed.

## Decision

The previous source-pullback attack needed an ACTUAL additional target map.
This pass supplies one from a discoverable non-hyperelliptic involution of
the modeled genus-two curve. It also analyzes the zero-image branch instead
of treating it as residual evidence for a new surface quantum problem.

For the original product-polarized source A=E^2 and a smooth bielliptic
target B=Jac(C), a genuine involution gives the following conditional gate:

1. A rank-two source pullback recovers the full original kernel classically.
2. Rank one is impossible. A reduced involution on the x-line can instead
   lift to ORDER FOUR on C; it must not enter this self-adjoint argument.
3. Rank zero gives an explicit unitary exchange of the source factors. The
   original problem reduces to TWO degree-ell elliptic weak isogenies, with
   the input's actual query restrictions preserved. Alternatively, an
   already valid Sp4 hiding function restricts to two SL2 Borel problems.

This is a useful elimination/reduction for a concrete geometric family,
not a new general quantum algorithm. The elliptic and Borel backends are
prior art. Neither the residual branch nor absence of an involution is a
classical-hardness result. Generic targets need not be bielliptic.

## 1. Keep The Original Input

Let p be odd and ell an odd prime different from p. Retain

    phi: A=E^2 -> B,       phi^dagger phi = phi phi^dagger = [ell],
    K=ker(phi),            L=ker(phi^dagger).

E is supersingular, A has its PRODUCT principal polarization, and its full
evaluable order M_2(End(E)) is supplied with integral coordinates, Rosati
adjoint, trace pairing, and legal small-torsion actions. B is the original
modeled principally polarized surface. When using this frontend require
B=Jac(C) for a smooth modeled genus-two curve C, with paid group arithmetic.

The weak responses on one complete source basis at each auxiliary level
have ONE common unit u_r, and all levels refer to ONE actual phi. Preserve
the paid common definition field and compatible extensions. No target
endomorphism ring, Hom module, large-ell torsion points, hidden kernel,
unknown isogeny coefficients or target decomposition is added as advice.

There are two distinct access statements below. A fixed collection of small
auxiliary levels does NOT become an evaluator on arbitrary torsion points.
The stronger full weak-representation corollary is explicitly conditional
on that stronger original interface, not inferred from successful CRT.

## 2. Find A Real Curve Map With Constant-Degree Geometry

Write C as Y^2=F(X,Z), with F a squarefree binary sextic. This includes a
quintic affine model with one branch point at infinity. Over a field where
the six branch points split, a projective automorphism is determined by
the images of one fixed ordered triple. Enumerate its 6*5*4=120 possible
images, construct the corresponding projective matrix and check the whole
branch divisor. This does NOT enumerate the finite field.

For a finite base field, factoring the degree-six polynomial and adjoining
its roots has bounded degree: the maximum lcm of factor degrees summing
to six is six. A further quadratic extension suffices for the lift below.
These field constructions and factorizations must be paid and bounded.
They are ordinary fixed-degree operations, not new hidden advice.

For M in GL2 preserving the divisor, compute and verify the FORM identity

    F(M(X,Z)) = kappa F(X,Z).

The lift acts by (X,Z,Y) -> (M(X,Z), uY), with u^2=kappa. A genuinely
nonidentity reduced involution satisfies M^2=lambda I. Weighted projective
coordinates identify (sX,sZ,s^3Y) with (X,Z,Y), so the lift squares to

    Y -> (kappa/lambda^3) Y.

Consequently it has order two precisely when kappa=lambda^3. If instead
kappa=-lambda^3 its square is the hyperelliptic involution and its order
is FOUR. Both tests are invariant under rescaling M. Failure to obtain a
square root over the base field means a paid quadratic extension, not
nonexistence of the map. Reversing u selects the complementary involution.

The order-two lift is neither identity nor hyperelliptic, hence is elliptic.
Its action gamma on Jac(C) preserves the principal polarization, obeys
gamma^2=1, gamma^dagger=gamma and has two-dimensional +/- Tate eigenspaces.
Its squared Rosati norm is Tr(gamma^dagger gamma)=4. Evaluating it on a
degree-zero divisor is explicit point pushforward. Do not just substitute
into a Mumford pair while forgetting that a chosen base divisor may move.

An order-four lift is still a useful actual map, but has
gamma^2=-1 and gamma^dagger=-gamma. Send it to the EXISTING general/skew
pullback analysis; rejecting it from THIS involution gate is not discarding
all information in that map.

### Explicit Elliptic Quotients

Diagonalize the reduced involution over its lift field. Its fixed points
are not branch points in the order-two case, so a smooth even model has

    C: y^2 = A*x^6+B*x^4+C0*x^2+D,       A*D != 0.

The two degree-two quotient maps and monic cubic equations are

    pi_+: (x,y) -> (A*x^2, A*y),
    E_+: v^2 = u^3+B*u^2+A*C0*u+A^2*D;

    pi_-: (x,y) -> (D/x^2, D*y/x^3),
    E_-: v^2 = u^3+C0*u^2+B*D*u+A*D^2.

The formulas extend over x=0 and infinity; the code checks these points
using weighted projective coordinates. The two involutions correspond to
(x,y)->(-x,y) and (x,y)->(-x,-y), respectively. Align their signs with the
selected gamma. This is standard bielliptic geometry, not a new discovery;
see [Shaska's computational treatment](https://arxiv.org/abs/1209.3187).

The implemented frontend validates supplied split branch points over a
PRIME field, discovers the maps, distinguishes the lift orders, evaluates
curve points and evaluates the quotient maps on an already even model.
It does NOT implement extension-field factoring, automatic even-model
transport, Jacobian torsion arithmetic or a full native phi instance.

## 3. The Self-Adjoint Rank Dichotomy

Use the existing source-pullback reconstruction, with target norm bound 4:

    alpha = phi^dagger gamma phi,
    alpha_r = ell W_r^(-1) gamma_r W_r,       W_r=u_r phi_r.

The scalar cancels. The previous trace-pairing height bound and bounded
CRT recover EXACT integral source coordinates, not merely an ell residue.
They retain every original access, compatibility and norm assumption.

The resulting relations are

    alpha^dagger=alpha,     alpha^2=ell^2 I,     Tr(alpha)=0,
    im(alpha mod ell) subset K,                 K subset ker(alpha mod ell).

In an adapted symplectic basis with K first, the last two conditions give
alpha mod ell = [[0,T],[0,0]]. Self-adjointness gives T=-T^T. Since T is
two by two over an odd field, it has rank zero or two. Thus rank two
directly reveals K, while rank one contradicts this particular input.
This is a proof over all allowed ell, not extrapolation from finite counts.

If the image is zero, faithfulness of the PUBLIC full-order splitting gives
alpha in ell End(A). Consequently the coordinatewise division

    beta=alpha/ell in End(A)

is justified. This is NOT an arbitrary saturation oracle. It satisfies
beta^dagger=beta, beta^2=I, Tr(beta)=0 and phi beta=gamma phi. Therefore K
is beta invariant. The +/- eigenspaces V_+,V_- on A[ell] are orthogonal
nondegenerate symplectic planes, and

    K = k_+ direct_sum k_-,      dim(k_+)=dim(k_-)=1.

Conversely these are exactly the Lagrangians compatible with integrality
of the single map gamma on the neighboring lattice. Since beta is already
integral on the source lattice Lambda, it preserves
Lambda+K_tilde/ell iff beta(K)=K modulo ell. Entire words in gamma add no
new constraint; Z[gamma] is already generated by 1 and gamma. Other actual
target maps or the original geometry can of course give further information.

## 4. Use The Product Polarization, Not Only Abstract Linear Algebra

Beta is an INTEGRAL unitary automorphism of E^2 with its product
polarization. In a quaternion matrix, each column of beta has squared
norm one. Every nonzero entry has a positive integral norm. Hence each
column contains precisely one unit, and unitarity forces different rows:
beta is monomial. Self-adjointness, beta^2=1 and trace zero leave only

    diag(1,-1), diag(-1,1), or [[0,u],[u^dagger,0]],   u^dagger u=1.

In a diagonal case K is a product of two elliptic kernel lines. Its
principally polarized quotient is a product, contradicting smooth
B=Jac(C). Thus the zero branch on the actual smooth target is a unitary
EXCHANGE. This step fails for an arbitrary different source polarization;
do not generalize the conclusion to that input.

For the exchange define explicit source embeddings

    i_+(P)=(P,u^dagger P),       i_-(P)=(P,-u^dagger P).

They are available from the known source order and satisfy
i_s^dagger i_s=2, i_+^dagger i_-=0. Their combined map is a (2,2)-isogeny
onto A, invertible on ell-torsion. No elliptic-subvariety extraction of
degree growing with ell has been assumed.

## 5. Actual Reduction To Two Elliptic Weak Isogenies

Let q_s=(pi_s)_*:B->E_s and j_s=pi_s^*:E_s->B be the explicit norm and
pullback maps of the degree-two covers. They obey

    j_s=q_s^dagger,   q_s j_s=2,   j_s q_s=1+s gamma.

Define t_s=q_s phi i_s:E->E_s. Its degree is 4ell, since

    t_s^dagger t_s
      = i_s^dagger (ell I+s alpha) i_s
      = ell i_s^dagger (I+s beta) i_s = 4ell.

Moreover q_s phi i_(-s)=0: intertwining makes this map equal to its negative,
and Hom of abelian varieties is torsion free. On E[2], i_+=i_-, hence t_s
kills ALL E[2]. There is therefore a unique actual isogeny

    psi_s:E->E_s,       t_s=psi_s [2],       deg(psi_s)=ell.

The factor of TWO is essential. Calling t_s itself degree ell, or dividing
a general map just because its norm contains four, would be incorrect.
Here E[2]-annihilation proves the division. Also phi i_s=j_s psi_s: apply
j_s to t_s and cancel [2] in the torsion-free Hom group. It follows that

    K = i_+(ker psi_+) direct_sum i_-(ker psi_-)

on ell-torsion. A solver returning the two cyclic kernels/ideals therefore
recovers the SAME original kernel in the public source chart, without
ever constructing geometrically inaccessible ell-torsion points.

### Preserve Weak Masks And Access

For a point P of odd order d, query the original weak evaluator on i_s(P)
and compute

    [2^(-1) mod d] q_s( u_d phi(i_s(P)) ) = u_d psi_s(P).

The same common scalar applies to a whole d-basis. This gives a weak
representation at every odd level actually available in the original input.
It does not invent new levels.

If the original representation supports arbitrary even-order points too,
choose Q with [2]Q=P. For even d=ord(P), ord(Q)=2d. Then one query gives

    q_s( u_(2d) phi(i_s(Q)) ) = u_(2d) psi_s(P).

All choices of Q give the same result because t_s kills E[2]. Point
halving uses a constant-degree extension whose construction is charged.
The new mask depends only on d, as required. This extends to the full
weak-representation contract ONLY when those doubled levels and point
fields are actually allowed. A small odd-level transcript is insufficient.

Under the full interface this is a reduction to the established elliptic
problem, not a fresh higher-dimensional speedup. [Chen et al., Definition 2
and Sections 4-5](https://arxiv.org/html/2305.19897v1) provide the comparison.
Their displayed PQLP path assumes ell=p^{O(1)}, has GRH-related setup and
Heuristics 5.2/5.3; do not label that imported arithmetic backend an
unconditional implemented polynomial-time solver here. No such backend
was run or re-proved. Restricted access requires a separate matching audit.

## 6. Alternative: Stay Inside The Original Symplectic Source

If the original fully paid source f(g) hiding Stab(K) in Sp4(F_ell) is
already valid, a PUBLIC symplectic eigenbasis S gives legal embeddings

    h_+(a)=S diag(a,I2) S^(-1),
    h_-(a)=S diag(I2,a) S^(-1),          a in SL2(F_ell).

The two restricted functions hide the stabilizers of k_+ and k_-, which
are SL2 Borel subgroups. Each restricted query is ONE query to the original
source. No GL extension is manufactured. [Denney--Moore--Russell](
https://arxiv.org/abs/0809.2445) directly cover the SL2 case; citing only a
GL theorem would leave an avoidable access mismatch.

This route inherits all unproved/unimplemented surface-source obligations.
The geometric reduction in Section 5 does not require that surface HSP
source; it has its own explicit elliptic-access obligations instead.
Neither route is a classical solver for the zero branch. The implementation
only constructs the subgroup embeddings and composes returned lines.

## 7. Decisive Tests And Why This May Fail To Matter

- Complete local censuses at ell=3,5,7 give image-rank counts
  ((ell+1)^2, 0, ell*(ell^2-1)). For the zero branch, exact neighboring
  lattice integrality gives precisely (ell+1)^2 line pairs. These are
  ABSTRACT counts, not a distribution of genuine surface isogenies. No
  claimed success probability follows by conditioning on bielliptic targets.
- Smoothness further excludes equal lines after the exchange's two
  eigenspaces are identified with E[ell]: they give a product quotient.
  Distinct lines are NOT sufficient for a smooth Jacobian target. The
  product-target arithmetic fixture below already falsifies that shortcut.
- Exact CRT controls use the full order in (-1,-11) and ell=5. The mixing
  fixture recovers K; the commuting exchange fixture reconstructs beta
  exactly and leaves 36 algebra-compatible pairs, not an answer. Both
  fixtures have PRODUCT targets. They do not connect the tested genus-two
  curve to a secret native isogeny and must not be described as doing so.
- The exchange control gives psi_+=1+2i and psi_-=1-2i, each norm five,
  while t_+/-=2 psi_+/- each have degree twenty. Odd and even mask controls
  check the actual factor-of-two and common-scalar rules.
- The curve with branch set {1,-1,2,1/2,3,1/3} over F13 supplies x->1/x
  whose lift squares to the hyperelliptic involution. The code rejects its
  use in the self-adjoint gate while retaining its actual map metadata.
- Changed projective frames, a branch point at infinity, quadratic lift
  fields, nonmonic sextics, both elliptic quotient maps and all small
  rational curve points are checked. A 127-bit prime discovery run uses
  the same 120 triples, not a field-sized table.
- Original-Sp4 opaque labels at ell=5 verify the two SL2 restrictions' exact
  collision relation. They are tests of the interface, NOT a manufactured
  oracle benchmark offered as a research algorithm.

The chief limitations are substantive: generic C may have no extra
involution; an explicit curve/Jacobian bridge must be implemented correctly;
the weak-input promises cannot be certified by finite residue checks;
and the residual elliptic problem is already studied. A successful real
bielliptic test would validate a useful gate, not establish new quantum
advantage. Novelty of this particular combination remains unchecked.

Next useful work is a genuine native-instance composition with the exact
input contract, or an informative map on a target outside this now-reduced
family. Do not spend another theorizing pass on more bielliptic matrix
examples or the already published Borel receiver.
