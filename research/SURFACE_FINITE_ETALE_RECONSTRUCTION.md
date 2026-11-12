# Finite orbit algebras and original-prime Frobenius

2026-11-12. Selected question: can the classical small-prime torsion route
recover ORIGINAL-prime Frobenius uniformly from a binary smooth quintic input?
Quantum upper bound is the existing fixed-degree curve/torsion-cover route;
this construction seeks a matching classical poly(log p) bound, not a speedup.
Native cover, auxiliary model/lift and intrinsic height interfaces are proved
in the linked topic notes. COMPLETE Galois-invariant reconstruction is now
independently proved under those native hypotheses; parent read all806lines of
audits/reviews/2026-11-12-etale-reconstruction.md, including its anti-circular
auxiliary-prime/RR construction. Full native surface COMPOSITION remains
separate, under review. No full classical match, hardness or separation yet.

## Two admitted bridges and the exact remaining input

Parent read full independent reviews:
- audits/reviews/2026-11-12-target-unramified-orbits.md;
- audits/reviews/2026-11-12-target-prime-model.md.
The strongest direct baseline is Buchmann-Lenstra1994 Algorithm6.1/Prop6.2,
actual Sections5.7-5.9/6.1-6.2 checked in retained source. It computes a
p-maximal order at a KNOWN prime in polynomial bit time; global integer
factorization is not an input. The 2025 lecture Lemma5.24 has a stronger
all-bad-primes hypothesis and is not substituted for this prime-only theorem.

Conditional algorithmic theorem: given the CERTIFIED complete finite reduced
Q-algebra of the intended Galois set, polynomial-size multiplication/unit and
actual operation/deck maps, with target inertia trivial, compute its faithful
finite-etale reduction and Frobenius in polynomial(rank,input bits,log p).
This does not supply that algebra, its coefficient heights, or missing maps.
All ranks must be polynomial in numerical ell with fixed n,r; unrestricted
torsion of a growing-genus Jacobian is excluded.

## Genuine native orbit is unramified

The original smooth surface and transverse cubic Lefschetz pencil over Z_p
have branch divisor finite etale of degree220. On the complement U the
INTRINSIC full GSp frame is finite etale, not a generic ramified twist.
At a branch, work over a strict henselian complete unramified DVR R with
A=R[[t]]. Pull back t=s^ell. Tame Abhyankar kills horizontal inertia; the
cover was already etale at the vertical prime p and elsewhere away from t.
Purity over regular R[[s]] gives a split etale cover. Kummer descent yields
local normalization R[[w]], t=w^e with e|ell. Therefore the compactified
cover is smooth proper over Z_p, without a ramified base extension.
Its product Jacobian ell-torsion is unramified. The full constant-Gamma deck
action makes the natural socle E Galois-stable, so E is unramified too.

Let n=62,r=220,m=(r-2)n=13516,R=nm=837992. The safe backup E is the WHOLE natural
socle, not an assumed parabolic subset. The primary route below reconstructs
the smaller actual Galois-stable subgroup U of rank m. A regular fibre B_a is a
constant-Gamma torsor. One geometric point generates its entire splitting
field, degree<=d=|Gamma|, since sigma(b)=b rho(sigma) and rho is a homomorphism.
The E field has degree<=|GL_R(Fell)|. Thus S=B_a x E has d ell^R points and
splitting degree<=d|GL_R|, polynomial in ell for fixed n,r. Do not split all
ambient torsion or all divisor support roots. Closed canonical divisors lie
in the class/basepoint field by uniqueness, even if their supports do not.

Choose a0 in 1..r+1 regular mod p (the stated large-prime regime suffices),
then a=a0+p k. If auxiliary P!=p exceeds the polynomial number of bad base
images, a bounded grid of k contains a choice satisfying all residue h0=1
and chart conditions, while EVERY a remains target-regular. log a is
O(log p+log badcount). The earlier height chain explicitly depends on log a
through h_Z and the Green moment, so this retains a polynomial bound in the
NATIVE input bits; do not reuse the small-a bound while dropping this term.

Counterexamples: ramified constant twists do not extend etale over U; colliding
branch sections invalidate the tame local normal form; a fibre at a branch
can ramify despite a smooth compact curve. These are excluded explicitly.

## Known-prime maximalization, maps, and Frobenius

From any rational multiplication basis containing 1, multiply its other
basis elements by a common structure-constant denominator. The resulting
full lattice O0 is an integral order of polynomial size. No number-field
factorization is necessary. For a current overorder O of rankD:

1. Choose t with p^t>D. Binary powering and F_p linear algebra find the
   kernel of z->z^(p^t) on O/pO, exactly its nilradical.
2. Let I be its preimage. Compute O'=(I:I), with O subset O' subset p^-1 O,
   by lattice/linear algebra. Strict changes lower v_p(disc O) by>=2.
3. Stop at equality. Buchmann-Lenstra proves the terminal order p-maximal;
   original-order Hermite coordinates bound ALL intermediate bits uniformly.

There are <=log|disc O0|/(2 log p) strict iterations, each polynomial, with
no p>rank requirement. Under intrinsic unramifiedness, final discriminant is
a p-unit. Its reduction is finite etale. Any actual Q-algebra map preserves
p-integral closures; tensor products of these etale orders are already
p-normal. Thus group, deck, zero, scalar, relation and quotient operations
extend. Their reduced coordinate denominators are p-units, with exact checks.
F:a->a^p is computed by binary powering. On geometric points phi, phi o F
sends values to their pth powers, hence represents ARITHMETIC Frobenius.

For explicit E labels use ONE finite extension killing GL_R(Fell), e.g.
ell^ceil(log_ell R)*product_(j=1..R)(ell^j-1); R is fixed. Standard finite-field
factoring and group-operation tables recover an F_ell basis and F_E matrix.
No arbitrary lcm of a growing unrelated list. Equivariant Hom linear algebra
then gives W with phi g^T=P(g)phi, retaining actual frame arithmetic.

## Direct reduction falsified; reconstructed algebra still required

Completed OpenAI native-reconstruction-orbit report was fully parent-read.
Its useful counterexample is Q(T)=T(T-p): separable rational algebra Q x Q
has a nonreduced monogenic reduction, while p-maximal order Z x Z is faithful.
More generally p^k-scaled canonical coordinates preserve every polynomial
height and auxiliary-P promise while defeating ALL integer separating
functionals modulo p. Large p relative ell does not repair inputs varying
with p. Treat this direct-reduction route as falsified, not the comparator.

The now-reviewed reconstruction: encode ALL (b,t) using b and redundant
canonical divisors indexed by all constant deck translates, including the
cyclotomic component coordinate. Choose common z and a separating gamma
modulo the SMALL P, whose numerical size can exceed the known polynomial
bad-parameter counts. Lift at certified precision from intrinsic encoding
heights. Product polynomials and interpolation tables for Galois-equivariant
operations are rational; all heights have polynomial Lagrange/minor bounds.
A relation idempotent e in A tensor A marking equal torsion labels can descend
away the torsor factor by the linear equalizer

    A_E = ker[f -> e*(f tensor1-1tensor f)].

Its multiplication and genuine group/deck maps are computed in this subalgebra.
Then apply the admitted p-maximal procedure. This exact reconstruction,
including extraction of a closed algebra from numerical RR, compatible
all-component descent, and an effective precision bound, is now proved in
the full independent review above and summarized next.
The original transcript/packet is audits/api_inputs/2026-11-12-target-closure/
etale-reconstruction.md. The later independent proof pays additional inputs;
height bounds alone would not have supplied them.

Final cohomological assembly is now independently proved and parent-checked
in SURFACE_BOUNDARY_DETERMINANT.md. Explicit nodal-boundary determinant
division removes the need to construct/transport a parabolic subspace.
Full native composition remains separately reviewed.

## Complete reconstruction, with an actual smaller subgroup

For S=Ndual constant and nonzero s0, evaluation

    Hom_Gamma(S,J_full[ell]) -> J_full[ell], phi -> phi(s0)

is injective: any nonzero map from the simple S is injective. It is Galois
equivariant because Gamma/deck maps and S are constant. Its image U is an
ACTUAL Galois-stable torsion group of rank m, whose Frobenius is F_W. It is
generally NOT Gamma-stable, so no deck action on U is reconstructed. Given
the one-component Hom basis phi_j and multiplier representatives g_a,
the full-component formula is

    (u_j)_a=P(g_a)*phi_j(g_a^(-T)*s0).

The precomposition is essential. There are m independent full tuples, not
(ell-1)m unrelated component points. Unique prime-to-P lifting preserves all
group/deck/intertwiner identities. Full E remains a correct larger fallback.

Construct a GLOBAL Q-rational plane coordinate by a primitive combination
Y+c*zeta if necessary; include component intersections in the bad plane set.
For all (b,t) in B_a x U encode actual b coordinates/zeta and the unique
closed canonical divisors at every fixed deck translate R_h b, using that
component of the full t. Rational deck maps and uniqueness give
sigma enc(b,t)=enc(sigma b,sigma t). No component-labelled field basis is
an encoding scalar. One fibre point has constructible Galois field degree
<=|Gamma|; the U splitting field has degree<=|GL_m| but need not be constructed.

Freeze all polynomial bad counts and base-value candidates before P.
Choose P above them, excluding the fixed curve/deck/chart certificate.
Known-b RR AFTER this choice is paid without adding a new excluded integer:
the regular fibre has a P-unit discriminant separating polynomial, giving
an etale semilocal power-basis order R_b=Z_(P)[y(b)]. For H_a=pi^-1(a),
H=pi^-1(infinity), H0(jH_a)=(x-a)^(-j)H0(jH). Lift the b-idempotent in
the thick fibre; (1-e_b)g=0 selects H0(jb). Known b-jet kernels similarly
give H0(A-B). Exact semilocal linear/Hermite/Smith saturation and residue
patching yield unit bases with polynomial bits. No global maximal order or
circular later prime choice. Canonical h0=1 and unit RR extraction then give
all closed coordinates to the requested precision.

Write N=|Gamma|*ell^m and q for encoding length. Common integer separators
alpha=sum_(j<q) u^j enc_j exclude at most (q-1)*binom(N,2) values moduloP.
Every pair difference is a P-unit after successful separation. If each scalar
has absolute logarithmic height<=H and u<=U0, use

    H_alpha=qH+q^2 log(U0+2)+log(q+1),
    H_lambda=3(N-1)H_alpha+2(N-1)log2,
    K=N^2(H_alpha+2H_lambda)+2logN

as safe dominating bounds for product/interpolation/relation coefficients.
They are rational by global equivariance and P-integral by unit interpolation.
Choose a computable integer T>=exp(K), P^e>2T^2; exact rational reconstruction
is then UNIQUE. All these bit sizes are polynomial in ell,B at fixed m,n,r.

Interpolate the equality relation on U-labels, take its linear equalizer,
and descend ((b,t),(c,u))->(b,t+u), inversion, scalars and zero. This constructs
the true finite etale COORDINATE algebra Q[U] with Hopf maps, not a split
Q^N or a group ring. Quotient BEFORE target maximalization: only U needs
to be unramified at p, so no target-regular basepoint or target-good canonical
encoding is required. The proved known-prime algorithm and following Hopf
readout recover F_U=F_W. No additional reconstruction oracle remains inside
this bridge; native geometry and the final surface assembly keep their own
proof obligations.

## Deterministic Frobenius readout without a splitting field

The completed Claude composition-kernel-frobenius report was parent-read in
full. Its Hopf-algebra construction is accepted with the corrections below.
Input: the actually reconstructed finite etale F_p group algebra C=F_p[U],
rank N=ell^m, its multiplication, comultiplication Delta, and identity counit
epsilon. U is geometrically elementary abelian. All these maps must be paid;
this lemma does not construct them from a curve.

Construct the identity-point idempotent e0 by solving

    e0*(b_i-epsilon(b_i)*1)=0 for every basis element b_i,
    epsilon(e0)=1.

The annihilator is one-dimensional because the identity is an F_p-rational
point and C is etale. The algebra map Phi:a->a^p induces ARITHMETIC Frobenius
on geometric points x via x composed with Phi. Given endomorphism pullbacks
A,B, the sum of their point maps has pullback

    mu composed with (A tensor B) composed with Delta.

Contract back to an N by N matrix after EACH operation. Scalar maps use binary
addition; polynomial f(F) uses Horner evaluation. Thus no tensor power grows
with degree or coefficient size. For its pullback Psi, multiplication by
Psi(e0) has rank exactly |ker f(F)|: its finite-etale direct factor has precisely
those geometric points. Compute INTEGER rank by elimination, not trace mod p.

Enumerate monic irreducibles f over F_ell of degrees d<=m, by deterministic
enumeration and modular-power/gcd irreducibility tests. For J=floor(m/d),
rank of multiplication by (f(F)^J)^*e0 is ell^k. Exact integer divisions
recover k, and the contribution to chi_F is f^(k/d). Intermediate powers
also recover Jordan block sizes if desired. The Frobenius here is actual F_U;
convert chi_F(X) to det(1-TF_U), not to geometric inverse Frobenius by accident.

The largest objects are C tensor C and N-square endomorphism matrices.
Straight dense contractions give poly(N,m,log p,ell) bit cost; field inversions
carry their usual logarithmic factors. No finite-field splitting algorithm,
extension of degree |GL_m|, geometric labels, or spectral semisimplicity is
needed at this readout step. For fixed m and ell=O(log p) this IS polynomial
in log p, with an enormous fixed exponent.

Rejected report claim: it called m=13516 a blocker because output polynomial
degree53 allegedly limits runtime exponent to53. No such resource condition
exists. Output degree and polynomial runtime exponent are different quantities.
Its practical-size warning is valid; its claimed asymptotic obstruction is
false. We also retain only a polynomial/soft-O bit bound, not its displayed
bound that suppresses inversion factors. No finite control is needed to infer
these algebraic identities; none was run and no algorithm follows from tests.
