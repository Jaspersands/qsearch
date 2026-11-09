# Good dyadic images and a nonvacuous growing-genus endpoint

Date: 2026-11-06. Independent mathematical derivation for the parent pass.
Status: proposed proof; the source checks listed below and independent
actual-text review are PENDING. No quantum or complete Selmer algorithm
was executed. This file does not change STATE or the accepted local theorem.

## 1. Exact local input and intended output

Input is an explicit smooth proper hyperelliptic model over Z_2 whose
affine equation is

    C: y^2+h(x)y=f(x),   f monic of degree d=2g+1, deg h<=g,

with g>=1 and the rational section infinity. Coefficients are integral
and explicit; smooth good reduction is a native promise to verify from
this model, not inferred from a completed-square equation modulo 2.
The usual smooth proper model, its genus and its integral differential
basis must have their source scope checked. The affine smoothness test is

    gcd(hbar, hbar'^2 fbar + fbar'^2)=1.

The supplied odd-degree hyperelliptic model has the usual smooth infinity
chart; that chart is part of the model check, not a point search.

Complete the square and scale by

    X=4x,  Y=2^(d-1)(2y+h(x)),
    F(X)=4^d f(X/4)+4^(d-1)h(X/4)^2.

Then F is integral monic of odd degree d, and Y^2=F(X). Let
L=Q_2[X]/F. The output is the complete image of J(Q_2)/2J(Q_2) in
L*/L*^2, in a returned explicit dyadic squareclass frame. Its dimension is
r-1+g, where r is the number of Q_2-irreducible factors of F, by actual
Stoll Lemma 4.4. No Jacobian group order, supplied points, formal-group
coordinates, roots of F, or list of extensions is input advice.

The operation below is CLASSICAL. Its purpose is to finish the dyadic
place in an end-to-end quantum arithmetic composition, not to supply a
new quantum primitive or claim a classical lower bound.

## 2. A polynomial residue set generating the reduction quotient

Choose an odd positive integer a with

    q=2^a >= 1024(g+1)^2,

taking the least such odd a. Then q<4096(g+1)^2 and a=O(log(g+1)).
Construct k=F_q and its unramified degree-a lift K/Q_2. Enumerate the
affine points of C(k) with hbar(x)!=0; call this set S. This is polynomial
work: for each x with hbar(x)!=0, solve

    z^2+z=fbar(x)/hbar(x)^2

by F_2 linear algebra, then put y=hbar(x)z. No discrete logarithm is used.
At most g affine points with hbar(x)=0 and the point infinity are omitted.

Claim: the divisor traces Tr_{k/F_2}(P-infinity), P in S, span
J(F_2)/2J(F_2). No trace/divisor group operation is needed in the
algorithm; this is a proof of the source law for the local norm labels.

Proof. Suppose a nonzero character

    chi:J(F_2) -> Z/2

vanishes on all these trace classes. Let A=J/F_2. The Lang map
L_A=Frob-1:A->A is a separable isogeny with kernel A(F_2): its derivative
is -1 and its geometric kernel consists of the Frobenius-fixed points.
Quotient its source by H=ker chi. The resulting factor

    pi:A/H -> A

is an etale isogeny of degree 2. Pull it back along the based Abel--Jacobi
map j:C->A. The resulting degree-2 cover D->C is GEOMETRICALLY connected.
Indeed, if it split geometrically, the component containing (infinity,0)
would give a based lift C->A/H. The universal property of the Jacobian
would extend it to psi:A->A/H with pi psi=id_A. A right inverse of an
isogeny of degree 2 is impossible: psi is itself an isogeny and degrees
would multiply to 1. This also excludes a purely constant disconnected
cover; the based point matters.

The cover is etale, so Riemann--Hurwitz gives genus(D)=2g-1. Its fiber
over P in C(k) splits precisely when chi(Tr_{k/F_2}j(P))=0. To check this
identity, choose b with Frob(b)-b=j(P); then

    Frob^a(b)-b=sum_{i=0}^{a-1}Frob^i j(P)=Tr j(P),

and pass to the quotient by H. Consequently, if N_- is the number of
points with nonzero trace character,

    N_- = #C(k) - #D(k)/2
         >= (q+1)/2 - (4g-1)sqrt(q).

The displayed q is more than sufficient for N_->g+1. At least one such
point belongs to S, a contradiction. This proves the claim for EVERY
character, without constructing characters, covers, J(F_2), or its order.
Oddness of a is harmless and is not needed by this cover argument.

The external ingredients to check are the Lang-isogeny/quotient statement,
the Jacobian universal property, and the usual Weil and Riemann--Hurwitz
bounds. The connectedness and trace-label assertions above are deductions,
not quotations of a stronger finite-field sampling theorem.

## 3. Two shallow formal layers, not a deep formal source

Let A_n=ker(J(Z_2)->J(Z/2^n)). The completion of the smooth abelian scheme
at zero has integral formal coordinates, and A_n has coordinate set
(2^n Z_2)^g. For an integral commutative formal group,

    [2](T)=2T + terms of total degree at least 2.

Thus

    [2](4u)/8=u+2P(u),

where P is a convergent integral power series on Z_2^g. Its derivative
is the identity modulo 2. Multivariate Hensel/contraction therefore gives
a bijection [2]:A_2->A_3. This proof requires no numerical logarithm or
formal-group parameter computation. In particular,

    A_3 subset 2J(Q_2).

Every deeper formal point, and every trace of a depth-3 formal point from
an unramified extension, has ZERO Kummer class. Thus a deep-neighborhood
source cannot supply the dyadic tangent contribution.

Use the integral differential basis

    omega_j=x^j dx/(2y+h(x)),  j=0,...,g-1.

For each P=(x,y) in S and each member u of an F_2-basis of k, form the
column

    (Tr_{k/F_2}(u*x^j/hbar(x)))_{j=0}^{g-1} in F_2^g.

These columns span F_2^g. Otherwise a nonzero polynomial
H(x)=sum_j lambda_j x^j of degree<=g-1 would satisfy
Tr(u H(x)/hbar(x))=0 for every u and every P in S. Nondegeneracy of the
finite-field trace pairing gives H(x)=0 at every such x. Weil gives
more than 2(g-1) points in S, hence more than g-1 distinct x-values,
contradicting the degree bound. Gaussian elimination selects g columns.

For a selected pair (P,u), choose an integral lift x_0 and a lift u_0.
Hensel's lemma with derivative 2y+h a unit supplies the unique y-branch
above x_0 reducing to P. For n=1 and n=2, use x_0+2^n u_0 on that SAME
branch, and denote the resulting point by P_{n,u}. Define

    Q_{n,u}=Tr_{K/Q_2}(P_{n,u}-P_0) in A_n.

The differential of Abel--Jacobi identifies the image of Q_{n,u} in
A_n/A_{n+1} with the selected column. This is ordinary first-order
reduction of an integral morphism; quadratic terms vanish modulo 2^(n+1).
The selected n=1 points span A_1/A_2 and the n=2 points span A_2/A_3.
Their union therefore generates the image of A_1 in J(Q_2)/2.
Individual n=2 labels may be zero in J(Q_2)/2; independence there is NOT
asserted. Relations arising from halves outside the formal kernel are
automatically respected by the Kummer-label linear algebra.

Combine these labels with the lifted-point traces from section 2. For any
point of J(Q_2), subtract a combination of the latter to make its reduction
a double. Lift a half of that reduction, solely in the proof, and subtract
its double. What remains lies in A_1 and is covered by the two shallow
layers. This proves completeness in J(Q_2)/2. No algorithm to find that
half, or an explicit Jacobian parameterization, has been smuggled in.

## 4. Norm labels, Weierstrass avoidance and precision

For P in S, hbar(x)!=0 implies v_2(2y+h(x))=0 for every Hensel lift and
every perturbation used above. Consequently

    v_2(F(4x))=2d-2.

The monic integral F has integral geometric roots. Thus each root-distance
valuation v_2(4x-alpha) is nonnegative and is at most 2d-2. In particular
4x-theta is never zero in the descent algebra and cannot be arbitrarily
close to a Weierstrass root. This addresses the precision issue directly;
no random avoidance or unspecified stopping precision is used.

For an original trace label compute

    Norm_{L tensor K/L}(4x-theta).

For a formal difference, compute the two point norms separately and take
the difference of their squareclass coordinate vectors. The sign is
irrelevant over F_2; no division by a small algebraic element is needed.
The norm is the determinant of multiplication in the explicit integral
unramified tower basis, of dimension a=O(log g).

Every transferred component has normalized local valuation at most

    V=d*a*(2d-2).

Indeed the norm is a product of a conjugate factors, each of normalized
2-valuation <=2d-2; conversion to a component's integral valuation costs
at most its ramification index <=d. Its multiplication determinant over
Q_2 has valuation <=dV. Given an exact maximal-order multiplication table,
working modulo 2^P with

    P=dV+5

leaves at least five 2-adic digits after the conservative determinant/
Cramer normalization loss. Three digits suffice for the dyadic unit
quotient below. All evaluations and norm determinants are integral
polynomial operations. The existence of the Hensel y is certified by the
residue point and unit derivative; no high-precision y is needed to compute
these x-only labels.

The base maximal order and component frame are obtained by the paid
integral-basis and finite-ring construction from the current local-image
note, with its small-residual-characteristic source hypotheses checked.
Alternatively the global arithmetic preparation already supplies this
order. The point-source precision above must NOT be reused for arbitrary
global squareclass representatives: those require their own coefficient/
norm height bound, exactly as in ELLIPTIC_TWO_SELMER_COMPOSITION section 3.

## 5. Polynomial dyadic squareclass coordinates without enumeration

This replaces the fixed-cubic enumeration of a bounded residue ring.
Fix a completion E/Q_2 of degree n=e*f and its explicit maximal-order
frame, residue map, uniformizer pi and residue F_2-basis lifts a_l.
The finite-ring/idempotent construction of the previous local theorem
works also at 2; its odd-prime TWO-BIT squareclass formula does not.

Put N=3e. Hensel's square-root criterion gives

    U_N=1+pi^N O_E = 1+8O_E subset O_E^{*2},

since N>2e. All needed unit arithmetic therefore takes place in O_E/8O_E.
There is no enumeration of this ring, whose cardinality is exponential
in n. The principal unit quotient U_1/U_N is generated by

    b_{j,l}=1+pi^j a_l,  1<=j<N, 1<=l<=f.

There are k=(3e-1)f<3n generators. Generation follows by removing the
successive leading residues in U_j/U_{j+1}=F_{2^f}, an additive F_2 space.

Compute the EXACT integer relation lattice R of these k generators by
successive kernels. Start with Z^k. At step j its current basis products
lie in U_j; send them to

    (w-1)/pi^j mod pi in F_{2^f}.

This is an additive F_2-linear homomorphism on the current exponent
lattice. Take its full INTEGER kernel modulo 2, compose the lattice bases,
and reduce by HNF. At step N the lattice is exactly R, not its saturation.
Its index is <=|U_1/U_N|=2^((3e-1)f), so all HNF entries and powering
exponents have O(n) bits. There are O(e) polynomial-size linear-algebra
steps. This reuses the exact nilpotent-filtration relation method in
FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION section 7; it is not a
new quantum operation.

For an arbitrary normalized unit u, replace it by u^(2^f-1). The exponent
is odd, so the squareclass is unchanged, and its residue is now 1.
Successive residue removal gives an exponent vector in the above b's.
Its image in

    F_2^k / (R mod 2)

is the unit squareclass; append the original valuation parity. This yields
the full n+2 dimensional local squareclass group, with no finite-field
discrete logarithm or factorization of 2^f-1. Uniformizer choices are fixed
once and returned with the frame. Norm determinant valuation computes
the valuation; division by pi to that valuation loses at most f*v_E(u)
base-2 digits by Cramer, already covered in section 4.

## 6. The irreducible odd-Galois endpoint is obstructed

Do not silently assume the first proposed family has growing-genus members.
Let s=deg(hbar). Smoothness forces hbar!=0. In h^2+4f the final Newton
edge joins (2s,0) to (2g+1,2): all coefficients of degree>2s have valuation
>=2. Thus exactly n_infty=2g+1-2s roots have valuation -2/n_infty.
Since n_infty is odd, these form ONE irreducible totally ramified local
factor of degree n_infty. If the entire irreducible branch root field is
Galois of odd degree, this local root field is Galois. A totally ramified
odd tame Galois extension of Q_2 is trivial, since tame inertia embeds in
F_2*. Hence n_infty=1 and there is a Q_2 branch root. Global Galoisness
then implies that ALL branch roots lie in Q_2.

It follows that dim J[2](Q_2)=2g. Formal-kernel 2-torsion injects into
A_1/A_2 (A_2 is torsion-free by section 3), so has dimension <=g. Reduction
therefore gives at least g independent geometric 2-torsion points. The
special fiber has p-rank g. By Deuring--Shafarevich for the separable
characteristic-2 hyperelliptic cover, this p-rank equals the number of
distinct finite branch points, i.e. the number of distinct roots of hbar.
Every such root is F_2-rational because all characteristic-zero branch
roots are Q_2-rational. Hence g<=2. The Deuring--Shafarevich source is
still a PENDING independent check; this obstruction is not used to prove
the constructive local algorithm.

## 7. Explicit reducible family and unboundedness obligation

The obstruction is avoided by a native branch ALGEBRA with odd-Galois
field factors. Let G be monic irreducible of odd prime degree m, with
Q[X]/G cyclic Galois and Gbar squarefree modulo 2. Set

    H(x)=G(x-4),   B(x)=(H(x)-G(x))/4,
    h(x)=(G(x)+H(x))/2=G(x)+2B(x),
    f(x)=x h(x)^2-(1+4x)B(x)^2.

Then f is monic of degree 2m+1, deg h=m, and

    h^2+4f=(1+4x)G(x)G(x-4).

Modulo 2, hbar=Gbar and Bbar=Gbar'. At a root of hbar, the curve point
has y=Bbar, and the x derivative of its equation is Gbar'^2!=0.
Thus the dyadic model is smooth. Infinity has the usual good odd-degree
chart. The scaled monic branch polynomial is

    F(T)=(T+1)G_4(T)G_4(T-16),  G_4(T)=4^m G(T/4).

Its algebra is Q times K times K, with K=Q[X]/G. The existing odd-Galois
class-generator and complete compact-unit primitives apply componentwise;
no even-degree field or normal-closure advice is introduced.

For good reduction at every odd p<=d=2m+1, require G mod p irreducible,
and at p=m require additionally G(X-4)!=G(X) mod p. When p!=m,
translation invariance by nonzero 4 would force p to divide deg G=m, so
the two irreducibles are distinct. Neither has the rational root -1/4.
Consequently the completed-square branch polynomial is separable at p.
All these local conditions are directly checkable in polynomial time.

Unboundedness source obligation: odd-order Grunwald gives, for EACH odd
prime m, a cyclic degree-m number field unramified/inert at every
p<=2m+1. CRT in its maximal order chooses an integral primitive element
with any prescribed irreducible residue polynomial of degree m at these
primes. At p=m, choose one not invariant under translation by 4. Such a
choice exists: the total number of monic irreducibles of degree m over F_m
is m^(m-1)-1, while at most m-1 are translation-invariant polynomials
X^m-X-c. Thus the native family has members for unbounded m, PROVIDED the
precise cited Grunwald theorem is verified. This is an existence argument,
not a polynomial algorithm to generate input fields or a height bound for
their smallest representations. The supplied input's full bit length is
charged.

A small explicit nonvacuity lead is

    G(X)=X^3-22X^2-25X-1,
    disc(G)=(22^2+3*22+9)^2=559^2.

Hand calculations give irreducibility modulo 2,3,5,7 and non-invariance
under translation by 4 modulo 3. Irreducibility and square discriminant
then make the cubic field cyclic. This would give genus 3, already beyond
the obstructed irreducible family's bound. These calculations are a LEAD
for one exact control, not a recorded CAS verification or unboundedness
proof. Do not launch a parameter sweep from this note.

## 8. Endpoint, baselines and exact source requests

The proposed endpoint is the INTEGER dim_F2 Sel^2(J/Q) on the explicit
good-dyadic, good-small-odd-prime family with odd-Galois field factors.
Large bad primes are handled by LARGE_PRIME_LOCAL_KUMMER_IMAGE. Good odd
places use the usual unramified local condition. Real images, mod-2
valuation kernels and compact squareclass representatives reuse the
odd-degree descent construction, with growing-degree costs checked rather
than presumed from the cubic note. Shor factoring and the existing complete
compact S-unit primitive are the quantum operations. There is no claimed
new circuit, novelty, separation, Mordell--Weil rank or covering output.

The matched classical baseline is the SAME descent with classical
class/unit arithmetic. The new local operation is itself classical and
does not establish the absence of a classical polynomial global algorithm.
The original Stoll local routines and their tiny-generator warning remain
the local comparison; here good reduction is used explicitly.

Sources now retained under audits/sources/good_dyadic_selmer/ include
milne_av.txt, milne_jac.txt, grunwald.txt and morgan_parity.txt. Parent owns
the source audit. Requested exact gates:

1. Lang isogeny, quotient by a finite etale subgroup, and based Jacobian
   universal property; then check the cover deduction in section 2.
2. Abel--Jacobi differential, smooth formal coordinates and the integral
   differential basis for the explicit generalized hyperelliptic model.
   The formal doubling/Hensel argument above avoids an extra log theorem.
3. Deuring--Shafarevich only for the separate irreducible-family obstruction.
4. grunwald.txt section 2.1 explicitly states solvability for cyclic odd G
   and cites NSW08 (9.2.8). Verify that theorem's exact local-completion
   scope; do NOT substitute the later Hilbert-specialization theorem with
   its large-residue hypotheses.
5. The global integral-order/S-unit/source interfaces and all local
   squareclass evaluations must retain their charged growing degrees.

No pending source is promoted by this derivation, a reviewer label or a
passing finite example. The cheapest decisive checks are the depth-3 zero
law, the explicit genus-3 shifted-G model, exact principal-unit quotient
coordinates, and the full local rank r-1+g on that ONE input.
