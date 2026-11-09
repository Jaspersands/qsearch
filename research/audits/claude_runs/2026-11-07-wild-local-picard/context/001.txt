# Good-dyadic local images and growing-genus two-Selmer dimension

2026-11-06. REVIEWED WRITTEN bounded-error quantum polynomial-BIT
composition for the exact promised Selmer-dimension family in section1.
Core, source, global-resource and independent endpoint reviews completed.
No full algorithm execution, novelty or speedup claim. Detailed local derivation: audits/reviews/2026-11-06-good-dyadic-
derivation.md (retained draft); final dispositions are in
`audits/reviews/2026-11-06-good-dyadic-selmer.md`. The unverified irreducible
family obstruction in the draft is NOT part of this theorem.

## 1. Selected question and native endpoint

Can the complete two-Selmer DIMENSION be computed in quantum polynomial
BIT time for a nonvacuous growing-genus family, with every local source
and every global class/unit operation paid?

Input: explicit f,h in Z[x], f monic of degree d=2g+1>=3, deg h<=g;
the model C:y^2+h y=f has smooth good reduction over Z_2, including its
unique rational infinity. Form the monic integral polynomial

    F(X)=4^d f(X/4)+4^(d-1)h(X/4)^2.

It is separable. Every global irreducible factor defines an odd-degree
GALOIS field (linear factors allowed). Require p not dividing disc(F)
for every odd prime p<=d. These are model/input promises, not supplied
points, units, maximal orders, class generators or local images. Local
polynomial conditions are explicitly checkable; no polynomial algorithm
to certify arbitrary Galoisness is assumed.

Output: the integer dim_F2 Sel^(2)(Jac(C)/Q), with error<=eta and target
poly(input bits,d,log(1/eta)). Not Mordell-Weil rank, rational points or
covering curves. The curve is isomorphic to Y^2=F via X=4x and
Y=2^(d-1)(2y+h). Numerical degree is charged.

Independent selection compared coherent Gaussian transport, explicit
unipotent tensor transport, Clifford-scrambled magic-state learning and
linear mixing of character product states. The first is already published
with its width-dependent rejection cost; the second has a public-logarithm
classical elimination; the latter two supplied no new decoder. A direct
one-qubit-plane Bell detector is exponentially rare, but this does not
exclude a complete-distribution decoder. No new barrier implementation is
queued for those lines. The present route wins admission ONLY because a
concrete dyadic operation can finish an entire specified arithmetic output.

Corpus been-tried and baselines preceded source selection. The classical
comparator is the SAME Stoll two-descent with classical class/unit/S-unit
arithmetic, including applicable rigorous subexponential methods. The
dyadic and large-prime operations are classical. No classical lower bound
or absence of a polynomial algorithm is asserted. The quantum primitives
are the already audited compact S-unit and odd-Galois class-generator
compositions, not a newly invented HSP receiver. The asymptotic target is
polynomial in the FULL coefficient bit length, numerical degree and
log(1/eta), replacing the global arithmetic costs of the matched classical
descent. Applicable classical index-calculus methods retain their actual
field/discriminant and heuristic/rigorous hypotheses. This comparison is
an upper-bound composition; no proven superpolynomial separation follows.

Decisive falsifiers are an unpaid complete global basis or factor base;
an exponential dependence on genus, residue size or compact exponents;
missing formal/reduction classes at2; a nonintegral differential frame;
a false local rank target; and a polynomial classical counterpart for the
SAME promised output. No cryptographic or hardness promise is added.

## 2. The concrete dyadic operation

Choose the least odd a such that q=2^a>=1024(g+1)^2; q=O(g^2).
Enumerate affine points over F_q with hbar(x)!=0. Solve the remaining
Artin--Schreier equation by F_2 linear algebra. Lift x to the explicit
unramified degree-a field K/Q_2; the y derivative is a unit, so Hensel
provides a point on the chosen residue branch. Only x is needed for its
norm label in L=Q_2[X]/F.

For analysis, any nonzero chi:J(F_2)->Z/2 quotients the Lang isogeny to
a degree2 etale isogeny J'->J. Pullback along Abel--Jacobi is geometrically
connected: otherwise a based section C->J' would extend by the Jacobian
universal property to a right inverse of that degree2 isogeny. Its genus
is 2g-1. Frobenius telescoping identifies the fiber sign at P in C(F_q)
with chi(Tr(P-infinity)). Two ordinary Weil bounds give at least
(q+1)/2-(4g-1)sqrt(q) negative signs. More than g+1 remain, so excluding
the hbar-zero fibers and infinity cannot remove all of them. Thus all
allowed point traces span J(F_2)/2 without computing the group or its order.

Let A_n be the level-2^n formal kernel of the good Jacobian. Smoothness
gives A_n/A_(n+1)=F_2^g. In integral formal coordinates,
[2](4u)/8=u+2R(u), so multivariate Hensel gives [2]A_2=A_3. Deep formal
points therefore have ZERO Kummer class; deep sampling was falsified.
Use two SHALLOW layers instead. The differential basis is

    omega_j=x^j dx/(2y+h),  0<=j<g.

For each allowed residue point and residue-field basis element u, form
the column (Tr(u*x^j/hbar(x)))_j. They span F_2^g, because a nonzero
polynomial of degree<g cannot vanish at all the available distinct x.
Select g independent columns. Perturb the corresponding x lifts by 2u
and by 4u on the same Hensel branch. Trace point DIFFERENCES generate
A_1/A_2 and A_2/A_3 respectively. Together with the reduction traces,
their Kummer labels generate all J(Q_2)/2. No half-point algorithm or
formal Jacobian parameterization is used; those appear only in the proof.

All selected points have 2y+h a unit. Therefore v_2(F(4x))=2d-2 exactly,
so no x-theta factor vanishes or approaches a root without a paid bound.
Point norm labels have every normalized component valuation at most
V=d*a*(2d-2). An exact integral multiplication table and working precision
P=dV+5 cover determinant valuation detection and Cramer normalization.
Compute difference labels by subtracting the two point coordinate vectors,
not by numerically dividing close algebraic numbers.

The integral differential basis is checked directly: on the infinity chart
u=1/x,v=y/x^(g+1), the equation is v^2+u H(u)v=u F1(u), F1(0)=1.
Its u derivative at infinity is -1, a unit; omega_j becomes, up to sign,
u^(g-1-j) dv/(partial equation/partial u), hence is regular. Affine
regularity follows from the hypersurface differential relation. These
g differential reductions are independent: hbar!=0 makes x a separating
parameter, so dx!=0 in F_2(C). Nakayama then gives the integral relative
canonical basis; independence over Q_2 alone would not suffice.

## 3. Dyadic coordinates without exponential unit enumeration

For each completion E/Q_2, n=e*f, obtain an explicit maximal-order frame,
residue map and uniformizer using the paid order/finite-algebra procedures.
The previous odd-prime TWO-BIT formula is inapplicable here.
After extracting valuation m and normalizing a/pi^m, raise its unit to
2^f-1. This odd exponent preserves squareclass and removes the residue
unit. Work in O_E/8O_E, with principal units U_1/U_(3e); U_(3e) consists
of squares by Hensel since 3e>2e.

The (3e-1)f<3n elements 1+pi^j*b_l generate this quotient by residue-digit
peeling. Compute their EXACT relation lattice using successive integer
congruence kernels in U_j/U_(j+1)=F_(2^f), HNF-reducing each step. Every
index is at most 2^((3e-1)f), so exponents and matrices have polynomial
bits. Do not saturate the lattice. Peeling any input unit gives an exponent
vector; reduce it modulo R+2Z^k and append valuation parity. Fix and return
the coordinate frame. No DLog or enumeration of all ring units is needed.

This reuses the already reviewed nilpotent-relation mechanism in
FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION.md section7. The independent Claude audit found no mixed-characteristic or quotient
counterexample. The proof is direct: a unit whose square lies in U_1 has
residue1, since the residue multiplicative group has odd order, so
U_1 intersect E*^2=U_1^2. Actual products, not linearized digits, define
all filtration homomorphisms. Extract a leading digit by solving pi^j z=w-1
in O/8; its ambiguity lies in pi^(3e-j), so its residue is unique for j<3e.
Check every current basis product lies in U_j before extracting it.
No saturation is allowed. The quoted n+2 dimension is a consistency test,
not the generation proof. For conservative arithmetic, compute component frames, tables and
uniformizers modulo 2^Q with Q=2dV+10 before normalizing point labels.
This covers even the audit's sufficient P+f*m table precision; exact
global-order arithmetic and idempotent lifting make this polynomial.
Determinant/Cramer loss f*m is an upper bound, not the sharper intrinsic
ceil(m/e) loss; no sharper estimate is needed.
The point precision V is NOT a universal
bound for arbitrary global compact units; each atomic factor is charged
by its own coefficient/norm height before its parity coordinates are
combined. Expanded huge unit products are forbidden.

## 4. Paid global composition

1. Factor F over Q classically and factor its integer discriminant with
   the paid quantum factoring routine. Compute maximal orders of ALL
   field components in growing degree. The actual Fast Integral Bases
   Theorem1, with the now supplied discriminant factorization, pays this;
   do not reuse a fixed-cubic claim without its growing-degree proof.
2. Let S contain all primes over 2 disc(F). On each odd-Galois component
   use ODD_GALOIS_CLASS_GROUP_COMPOSITION.md's polynomial-bit raw generating
   prime source, then one complete compact T-unit basis for T=S plus that
   source. A degree-one Q component is handled directly: Cl(Q)=0 and
   its complete S-unit basis consists of the rational primes in S, plus -1.
   Do not apply a log-discriminant field bound to disc(Q)=1.
   Roots of unity are exactly +/-1 since odd-Galois fields are
   totally real. Append a SEPARATE (-1) sign unit in EACH factor, not just
   diagonal -1. Source completeness is a budgeted probabilistic event.
3. Kernel the valuations at T outside S modulo2 to obtain L(S,2). Intersect
   the rational norm-square condition, retaining signs and all rational
   prime valuations. This is the prior virtual-unit argument componentwise,
   not an arbitrary finite subset of valid units.
4. At odd p<=d, the good-reduction image is the unramified norm-square
   image. At p>d use LARGE_PRIME_LOCAL_KUMMER_IMAGE.md. At2 use the new
   operation above, with actual Stoll target dimension r-1+g. At infinity,
   real-root isolation and the actual positive-sign intervals give the
   real Kummer image. Apply these maps to compact-unit ATOMS and combine
   their exponent parities; never expand huge units.
5. Intersect the local subspaces by F_2 linear algebra and return dimension.
   Allocate error across complete source/S-unit events and local routines;
   use constant-cap verified Las Vegas attempts with logarithmic restarts,
   not a clock proportional to 1/eta. Actual Biasse--Song v2 Theorem5
   explicitly accepts failure parameter mu. Set mu_j=1/(100r) for r field
   factors and allocate the remaining internal failures in one shared
   constant budget. Independent unamplified 2/3-success bases would give
   exponentially small joint success and are forbidden. Repeat whole
   constant-success runs O(log(1/eta)) and majority-vote ONLY the final
   integer dimension, never arbitrary unit bases.

Global source/product/compact-output and local/core/integrated reviews are
complete. To make atom precision explicit, clear every small representative's
coordinate denominators by a rational SQUARE, preserving its squareclass.
For the resulting nonzero integral alpha, set
V_alpha=ceil(log2|Norm(alpha)|)+1 (take1 when the norm is +/-1).
Every normalized local valuation is at most V_alpha, since ideal norms
multiply to this nonzero integer. The norm determinant and V_alpha have
polynomial bit size. Use P_alpha=d*V_alpha+5 and Q_alpha=2d*V_alpha+10 for
local component/table arithmetic. These bounds replace the point-source
V where necessary. Before fixing a local frame, take the maximum required
precision over its point-source bound and all the finitely many compact
atoms. All vectors in one local intersection use that SAME frame. The complete original valuations, not those of the
small representative, still supply global norm/virtual-unit parity rows.

This proves a WRITTEN bounded-error composition under the exact native
promises and the cited standard arithmetic theorems. No experiment or
reviewer's label is used as the proof.

## 5. Nonvacuous growing-genus family

The initial irreducible odd-Galois branch-field family appears incompatible
with growing-genus smooth dyadic reduction; the draft records a local
Newton/2-torsion obstruction. Its final p-rank source step is not yet used
as a theorem here. The actual candidate allows REDUCIBLE branch algebras.

Let m be an odd prime and G in Z[x] monic of degree m, defining a cyclic
degree-m field and irreducible modulo every p<=2m+1. At p=m additionally
exclude G(x-4)=G(x). Put

    H=G(x-4), B=(H-G)/4, h=(G+H)/2,
    f=x*h^2-(1+4x)*B^2 = x*G*H-B^2.

These are integral; f is monic of degree2m+1, deg h=m, and
h^2+4f=(1+4x)G H. Mod2, B=G', h=G, and f=xG^2+(G')^2. At a zero of G,
the unique y is G' and the x derivative is (G')^2!=0. Infinity is smooth.
The scaled F factors as (X+1)G4(X)G4(X-16), G4(X)=4^mG(X/4), so its
field components are Q and two copies of the same odd-Galois field.

At odd p<=2m+1, the two nonlinear polynomials are irreducible and distinct,
and neither has the linear root. Translation-invariance is impossible if
p!=m, by the x^(m-1) coefficient, and explicitly excluded at p=m. Thus
all small odd primes are good. Odd-order Grunwald plus CRT on integral elements supplies such G for
EVERY odd prime m. Prescribe the unramified degree-m local extension at
every p<=2m+1 (including p=m); the actual Grunwald paragraph in
Debes--Ghazi section2.1 allows this. Do not substitute their later theorem
requiring p not dividing the group order. At p=m choose a residue t in
F_(m^m) with t^m-t not in F_m: the map t->t^m-t has kernel F_m and image
the trace-zero space, so at most m^2 elements fail, fewer than m^m.
This excludes base-field elements and translation-invariant degree-m
minimal polynomials. At other primes choose any full-degree residue.
CRT in O_K gives an integral element with those residues, primitive since
m is prime. Its minimal polynomial is the required G. No efficient input
generator or small-height promise follows; the entire supplied input is
charged. Independent family review checked this existence argument.

The exact Sage control verifies G=x^3-22x^2-25x-1, disc=559^2,
irreducibility mod2,3,5,7, the scaled factors of degrees1,3,3, smooth
reduction at2 and separability of F at3,5,7. At q=2^15=32768 it finds
16683 allowed distinct x and tangent rank3. This establishes only those
finite identities; it does not execute a local image or Selmer computation.

The strongest duplicate-field simplification is exact: for L=Q x K x K,
the global norm-kernel equals K(S_K,2)^2 through
(b,c)->(N(b)N(c),b,c). Compute K arithmetic once and reuse it. This does
not remove the S-unit quotient or the Cl_(K,S)[2] contribution; no
classical polynomial counterpart follows from repeated fields alone.

## 6. Sources, reviews and exact control

Primary snapshots: audits/sources/good_dyadic_selmer/. Milne's actual AV
notes supply quotients, the Lang map, Jacobian universal property and Weil;
Debes--Ghazi section2.1 states the odd-cyclic Grunwald result. Morgan16.4--
16.5 already constructs related good-ordinary product families, so no
novelty follows from our shifted-polynomial construction. Stoll and the
audited compact S-unit/classgroup sources are reused with their exact scope.

Two distinct narrow Opus/high calls are terminal, with saved packets:
2026-11-06-good-dyadic-trace-opus refused with an empty report, estimated
USD0.02434, no findings and no retry. 2026-11-06-dyadic-coordinates-opus
completed, estimated USD0.199348; findings are verified/repaired above.
These estimates are not invoices or an exact remaining balance. Independent
Codex global/family and local core/source reviews completed. The local
review checked the actual Milne text and the characteristic2 constant
etale kernel, rather than treating it as mu_2. Final integrated review is complete. The exact Sage control is retained under
`audits/controls/good_dyadic_selmer/exact_control.{py,json}`. In
Q_2(sqrt2), its O/8 filtration has indices2,4,8,16,32, 32 units and4
unit squares, unit squareclass dimension3 and total dimension4; every
product respects the coordinate map. Saturating the relation lattice
would incorrectly erase all unit bits. No finite success establishes the
full endpoint. This pass closes the written composition at its stated
scope. No larger implementation or adjacent extension is queued. The next
pass must independently compare native high-upside mechanisms before
choosing another experiment.
