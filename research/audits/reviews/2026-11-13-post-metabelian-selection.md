# After native metabelian HSP: selected arithmetic operation — 2026-11-13

Read current STATE/TRAPS and targeted sections of LOCAL_SATURATION_FINITE_PRECISION,
INDEFINITE_TERNARY_SPINOR_ADMISSION, RELATIVE_NORM_TENSOR_SUPPORT,
GLOBAL_COMPACT_ISOTROPY and the later native local/global Selmer endpoint notes.
No API, network, Git, tests, archives, additional agents or implementation.
The metabelian natural-oracle/stabilizer searches are not repeated.

**Recommendation:** reopen native indefinite ternary isometry for ONE concrete
new operation: expand compact fractional norm witnesses by exponent reduction,
then construct an expanded rational isometry with completely charged exceptional
support. The derivation below removes the old common-ambient/support gate under
the already reviewed scalar-norm quantum theorem. Local integral transporter
OFFSETS remain a distinct obligation, so no full integral-isometry theorem follows.
Parent-owned corpus and actual primary-source checks precede further admission;
no novelty or classical separation is claimed.

## 1. Local Kummer conditioning is already completed, not a new candidate

The older finite-precision note's OPEN language is superseded by
LOCAL_KUMMER_NATIVE_END_TO_END (front and lines58–76), LOCAL_KUMMER_ALL_PRIMES
(front), and GENERAL_NATIVE_SELMER_COMPOSITION (front). They explicitly state
reviewed written native classical complete-image algorithms at all primes and the
conditional-GRH global quantum two-Selmer-dimension composition. Their contracts
include arbitrary bad reduction, original-point identities, finite-grid/Smith
conditioning, materialization, fixed clocks and confidence. Do not rebuild them.

This endpoint is externally valuable descent arithmetic, with input monic squarefree
f of growing odd degree and binary prime p, output the complete local Kummer image,
and polynomial(g,B,log p,log(1/eta)) classical target. The strongest comparator is
already the Stoll/local-field/divisor mechanism used by the completed algorithm;
no quantum gain occurs in the local routine. Its old generic-rank falsifier does
not undo the later representative-selection and precision proofs.

STATE's unqualified old recaps around the former LF686–693, LF863–865 and
LF2062–2064 need supersession wording; the Live Kummer row was corrected during
this read. The old general two-Selmer table row also needs the later endpoint.
These are parent-owned documentation corrections, not new research obligations.

## 2. A compact scalar norm witness always gives a small expanded witness

Assume L/K is an explicit number-field extension of relative degree d, a in K*,
and the reviewed scalar solver returns

    beta=product_(i=1)^s b_i^(e_i),       N_(L/K)(beta)=a,

with polynomially many NONZERO expanded L-atoms b_i of polynomial coordinate bit
height and binary integer exponents e_i. This exact power-product contract matters;
an arbitrary arithmetic circuit with additions does not automatically qualify.
Write e_i=d q_i+r_i with 0<=r_i<d, including negative e_i, and form

    beta0=product b_i^(r_i),     gamma=product b_i^(q_i).

Then beta=beta0 gamma^d. beta0 is expanded in polynomial BIT work: there are at most
s(d-1) atom multiplications, and coordinate heights grow polynomially. Compute the
expanded relative norm and put c=N(beta0)/a. Existence of beta implies

    c=N(gamma)^(-d) in K^(*d).

Find ANY root z in K of Z^d-c and return b=beta0/z. Since a base scalar has relative
norm z^d, N(b)=N(beta0)/z^d=a EXACTLY. gamma is never evaluated. Nonzero atoms,
a!=0 and d>=1 include fractional inputs, negative exponents and d=1. The new
witness need not be integral, an S-unit on the old support, or equal to beta.

Root extraction has a native polynomial bit clock, not a new number-field-factor
oracle. One explicit reduction uses the etale K-algebra K[Z]/(Z^d-c), of absolute
degree [K:Q]d. For a primitive theta of K, one of Z+j theta, with
0<=j<=binom([K:Q]d,2), separates all absolute embeddings. Its characteristic
polynomial is squarefree, computable by rational determinants/resultants. Factor
it using the existing polynomial-bit rational factor routine. A degree-[K:Q]
factor corresponding to a K-linear component exists; gcd over K with
(T-j theta)^d-c extracts its linear factor; subtract j theta from its root and
verify z^d=c. Separation ensures distinct components do not share a rational factor.
The finite search,
factor heights, exact gcd and coordinate conversion all have polynomial bit bounds.
Equivalently an already paid uniform number-field factor routine suffices.

Thus the small expanded norm witness is CONSTRUCTED, not merely a small-height
existence theorem. No unit lattice, principalization, expansion of gamma, root
advice or old expanded-input witness-shortening lemma is used.

## 3. Explicit expanded rational ternary transporter

Native input is the existing totally real K with expanded maximal-order data and
nonsingular integral ternary Gram matrices A,B. First diagonalize both by exact
constant-dimensional K-linear algebra. All coefficients and change-of-basis matrices
remain polynomial-bit. Write their diagonal forms as <a1,a2,a3> and <b1,b2,b3>.

For a quaternion (u,v) over an expanded field F, if u is nonsquare solve the scalar
quadratic norm equation N_(F(sqrt(u))/F)(x+y sqrt(u))=v and apply Section2. Then

    i -> [[0,u],[1,0]],       j -> [[x,-u*y],[y,-x]]

is an expanded splitting: i^2=u, j^2=v, ij=-ji. If u is square, the diagonal/swap
splitting is immediate from an expanded square root. The extension, its order,
embedding and factoring costs are charged; all degrees increase by at most two.
An insoluble norm gives the correct nonsplit answer.

Apply the already checked quaternary descent in GLOBAL_COMPACT_ISOTROPY lines75–101
to q4=<a1,a2,a3,-b1>. It uses a discriminant quadratic extension, one quaternion
splitting there, and constant-size minors/intersections. Section2 makes this entire
calculation EXPANDED; the auxiliary absolute degree is at most4[K:Q]. If q4 is
anisotropic, reject rational isometry. Otherwise take its nonzero zero (v,t).
If t!=0, v/t has q_A-value b1. If t=0, v is an isotropic vector of q_A; choose a
basis vector w with B_A(v,w)!=0 and turn v,w into a hyperbolic pair by the usual
linear subtraction. Then v+(b1/2)w', with B_A(v,w')=1 and q_A(w')=0, has value b1.
Thus the t=0 branch does not require a random retry or a special isotropic vector.

Call this vector v1. Project basis vectors onto v1-perp using the KNOWN nonzero
denominator b1, choose two independent vectors, and diagonalize its binary form
as <alpha,beta>. Construct a vector (x,y) of value b2 by

    N_(K(sqrt(-beta/alpha))/K)(x+y sqrt(-beta/alpha))=b2/alpha.

Use Section2 again; a split quadratic algebra is handled by the elementary
product formula instead. Its perpendicular vector (-beta*y,alpha*x) has value
alpha*beta*b2. Scale it by a square root of b3/(alpha*beta*b2). Failure of this
square test or the binary norm test rejects isometry; Witt cancellation justifies
these decisions after the chosen norm-b1 line. Success gives all three orthogonal
columns and an exact U with U^T A U=B. There are only a constant number of scalar
norm calls and fixed-size operations, so polynomial height/time composes uniformly
in growing [K:Q]. Allocate eta across the constant number of norm calls and
charged field preprocessing; subsequent expanded equalities are checked exactly.
This is a direct construction, not an unspecified CSA map.

Compute U inverse in expanded coordinates. An integer clearing coordinates of
both U and U inverse has polynomial bit length. Factoring it, together with
2, the native field discriminant and Gram determinant supports, gives an explicit
finite exceptional set. Outside it U and its inverse are integral. No compact
coordinate sum, hidden pivot prime or enormous unit is factored.

## 4. Independent check of the parent's direct quaternion route

The later EXPANDED_NORM_TERNARY_TRANSPORT construction is also correct.
For isomorphic division quaternions Q=(c,d0), B=(a0,b), c is nonsquare.
Set E=K(sqrt(c)); B_E splits. If a0 is nonsquare in E, an expanded quadratic
norm solution z in E(sqrt(a0)) of norm b makes q=z+j a nonzero norm-zero
element of B_E. Write q=u+v sqrt(c), u,v in B. Division of B forces v!=0.
The two norm coefficients give Nrd(u)+c Nrd(v)=0 and
u*bar(v)+v*bar(u)=0. Hence x=u v^-1 has trace0, norm -c and x^2=c.
If a0 is square in E, it is nonsquare in K (B is division), so a0/c is a
square in K; x=i/sqrt(a0/c) gives the same embedding without that norm call.

The anticommuter of x is two-dimensional; any nonzero y0 in it has trace0 and
y0^2=t in K*. Identify K(x) with E. Equality of the quaternion classes implies
d0/t is an E/K norm. Solve and expand w by Section2; y=w(x)y0 satisfies
y^2=d0 and xy=-yx. Thus 1,x,y,xy give the actual expanded algebra isomorphism.
For split quaternions use the two explicit M2 splittings instead.

For a ternary q, its volume element omega obeys omega^2=-det(q), and
v->omega*v identifies V with pure even-Clifford elements with reduced norm
det(q)*q(v). A Clifford isomorphism induces a similarity of factor detA/detB;
a base-field square root supplies the isometry precisely when that determinant
ratio is square. This checks the parent's normalization and both division branches.
All this stays in absolute degree at most4[K:Q] with expanded polynomial data.

## 5. Why this is the selected next question, and its boundary

This removes an actual prerequisite of the existing spinor/ray-class decision
mechanism for integral indefinite ternary forms. The endpoint remains decision,
not a short integral transporter or positive-definite HAWK/LIP. The best classical
comparison is the same rational norm/isotropy and spinor/ray-class reduction with
classical factoring/class/unit arithmetic; rational and quadratic-tower bases
have stronger already retained factoring-based competitors. No lower bound follows.

Next decisive question: from these EXPANDED common-ambient lattices, construct
local integral transporter offsets with a polynomial finite-precision clock, then
compose the actual ray-class quotient. Stabilizer spinor GENERATORS alone are
insufficient; scaling a nonnested pair to an inclusion changes its transporter
coset. The retained same-genus/nonisometric 3-neighbor pair is the cheapest exact
acceptance/falsification target, but no test is run here and finite success proves
no uniform theorem. Full local-offset, ray-class and error composition remain due.
