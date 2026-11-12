# Closed divisor encoding from support heights

2026-11-12. Independent exact review following
`SURFACE_TORSION_HEIGHT_CHAIN.md` and the completed finite/analytic reviews.
Those reviews supply support-height premises; their geometric/model inputs
are not re-proved here. No Git, network, API, archive, or numerical test was
used.

**Disposition.** There is a polynomial-height rational univariate encoding
of the requested nonreduced divisor. A separating coordinate must also be
unramified at every support point. Derivative denominators and the
confluent interpolation determinant both admit polynomial logarithmic
height bounds. Construction from a closed divisor algebra uses exact
linear algebra, without splitting the support. A numerical bit bound
additionally charges the presentation height of the field of definition,
not only its degree. This is not a construction of that field, a lift, a
good model, or the divisor from its abstract class alone.

## 1. Precise contract and output

Work in characteristic zero. Let K be an explicitly presented number
field over which the plane curve and the effective divisor E are defined.
Take a reduced plane equation F of total degree D; the application has an
absolutely irreducible curve. Its smooth normalization is C. Assume every
point of E maps into the affine nonsingular locus of the plane curve.
There the normalization is an isomorphism. Write geometrically

    E = sum_i m_i P_i,    P_i=(alpha_i,beta_i),
    sum_i m_i=g >= 1,    P_i distinct.

Let h denote absolute logarithmic Weil height. Use the projective
coefficient height H_F of F, and suppose

    sum_i m_i (h(alpha_i)+h(beta_i)) <= H.                 (1)

If the given support-height budget counts distinct points without
multiplicity, g times that budget suffices for (1). All geometric
conjugate points in the divisor are counted. Coefficients of F may be
normalized by one nonzero coefficient; the resulting affine coefficient
vector has height H_F. No bound below depends on its scalar normalization.

For a suitable integer c, put z=x+c y and h_c=log max(1,|c|). There exist

    A(T) monic, deg A=g;     B(T), C(T), deg B,deg C<g,

over K such that K[E] is K[T]/(A), with x=B(T), y=C(T), and z=T.
One absolute constant C_0 gives the joint coefficient-height bound

    h([1, coeff(A), coeff(B), coeff(C)])
       <= C_0 { D g H + g^2[H_F+h_c+log(gD+2)] }.          (2)

This is an intrinsic coefficient-height statement, valid without taking
the support's splitting field as an output field. Section 6 states the
extra field-presentation data needed to turn (2) into a bit bound.

The field must fix E as an effective divisor, not merely its linear
equivalence class. In the canonical application, uniqueness of the
effective representative supplies this distinction: a field fixing the
curve, basepoint, and class also fixes that unique divisor.

## 2. One small coordinate for N divisors

Set

    eta = F_y-c F_x.

On the smooth curve, z is a local parameter precisely when eta(P) is
nonzero. Indeed V=F_y partial_x-F_x partial_y is a nonzero tangent vector
there and V(z)=eta. At a fixed smooth point there is at most one bad c;
if F_x(P)=0, there is none. For two distinct affine plane points there is
at most one c with alpha_i+c beta_i=alpha_j+c beta_j. If beta_i=beta_j,
there is none. Thus a divisor of degree g excludes at most

    binom(s,2)+s <= g(g+1)/2

values, where s is its number of distinct support points. For N divisors,
the integer grid

    {0,1,...,N g(g+1)/2}

contains a c good for all of them, with h_c<=log(1+Ng^2). Divisors of
degrees at most g obey the same bound. Separation is required within
each divisor, not between different divisors. The search cost is
polynomial in N and the presented divisor data; only the height cost is
logarithmic in N. No claim of enumeration time polynomial in log N is
made.

This is where the smooth-plane-support premise matters: two distinct
normalization branches over the same singular plane point cannot be
separated by any function x+c y. The excluded points are counted in
Section 7.

## 3. Exact scheme encoding and descent

Put z_i=alpha_i+c beta_i. Since eta(P_i) is nonzero,
t_i=z-z_i is a uniformizer. Over an algebraic closure,

    Kbar[E] = product_i Kbar[t_i]/(t_i^m_i).

The z_i are distinct, so the Chinese remainder theorem gives

    A(T)=product_i (T-z_i)^m_i,
    Kbar[T]/(A) ~= Kbar[E].                               (3)

There are unique polynomials B,C of degree less than g that match the
Taylor expansions of x,y in t_i through order m_i-1. In particular,

    B+c C = T mod A,
    F(B,C)=0 mod A,
    eta(B,C) is a unit mod A.                             (4)

Equations (3)--(4) and uniqueness are Galois invariant. Consequently
A,B,C belong to K. The affine ideal of the divisor is

    ( A(x+c y), x-B(x+c y), y-C(x+c y) ).                 (5)

Its quotient is K[T]/(A), and F lies in the ideal by (4). On the smooth
curve, its local ideal at P_i is (t_i^m_i), as required. This is the
divisor thickening on the curve, not the m_i-th power of a plane maximal
ideal. Repeated roots of A are intentional and preserve multiplicities.

## 4. Jets: denominator and numerator bounds

The derivative along z on the function field is

    D_z = V/eta,    V=F_y partial_x-F_x partial_y.

For f=x or y, induction gives, for n>=1,

    D_z^n f = P_n/eta^(2n-1),
    P_1=F_y or -F_x,
    P_(n+1)=eta V(P_n)-(2n-1)P_n V(eta).                 (6)

For D>=2,

    deg P_n <= D-1+(n-1)(2D-3) <= 2nD.                  (7)

For D=1 the derivatives of order at least two vanish, so the coarse
bound still holds. At every nonarchimedean place use the coefficient
Gauss norm; at every archimedean place use the coefficient l1 norm.
Multiplication is submultiplicative, differentiation increases the norm
by at most the degree, and the sum in (6) introduces only its two terms.
Each step adds two factors from F/eta and a logarithm O(log(nD+2)); it
does not double the preceding numerator height. After the normalization
of F in Section 1, this proves

    h_aff(coeff P_n) <= C n[H_F+h_c+log(nD+2)].           (8)

The l1-to-coefficient-max conversion contributes O(log(D+2)) per fixed
F factor and is included in (8). Write
h_i=h(alpha_i)+h(beta_i). Polynomial evaluation gives

    h(eta(P_i)) <= H_F+h_c+D h_i+C log(D+2),
    h(P_n(P_i)) <= C n[H_F+h_c+D h_i+log(nD+2)].          (9)

The normalized Taylor coefficient is

    j_(i,n)(f)=P_n(P_i)/(n! eta(P_i)^(2n-1)).

Since h(a^-1)=h(a) for a nonzero algebraic number, and
log(n!)<=n log n, (9) proves

    h(j_(i,n)(f)) <= C n[H_F+h_c+D h_i+log(nD+2)]         (10)

for n>=1; the n=0 coefficient is alpha_i or beta_i. Thus small derivative
denominators and large multiplicities are explicitly paid. In particular
there is no factorial-sized logarithmic precision demand hidden in the
Taylor expansion.

Summing the jet heights for both x and y and n<m_i yields

    J <= C {D g H + g^2[H_F+h_c+log(gD+2)]},             (11)

using sum_i m_i^2<=g^2 and sum_i m_i^2 h_i<=gH.

## 5. Confluent interpolation: no uncharged root separation

In the Taylor normalization above, the interpolation matrix is

    W_((i,n),j)=binom(j,n) z_i^(j-n),
    0<=n<m_i,  0<=j<g,

with entries zero when j<n. Its determinant is, up to the sign of the
row order,

    det W=product_(i<j)(z_j-z_i)^(m_i m_j) != 0.         (12)

There are no extra factorial factors. Put

    H_z=sum_i m_i h(z_i) <= H+g(h_c+log 2).

The height of A's coefficient vector is at most H_z+g log 2. The affine
height of a row of W is at most (g-1)h(z_i)+g log 2. Hence the sum of
these row heights is at most gH_z+g^2 log 2.

Apply Cramer's rule to the two jet right-hand sides. At each place bound
all relevant determinants by the product of the maxima of their rows;
at archimedean places the permutation sum costs log(g!), not g! times
the row-height bound. Use rows enlarged by the two jet entries, so the
same bound covers det W and every numerator determinant simultaneously.
The homogeneous vector

    [det W, all B-numerators, all C-numerators]

therefore has height at most gH_z+g^2 log 2+J+log(g!). It represents
[1,coeff B,coeff C]; the product formula pays the common denominator.
Combining this with A's bound and (11) proves (2).

Although a splitting field can be used for this proof, its degree never
multiplies (2). The auxiliary conjugate computations are normalized
absolute-height inequalities. For a conditioning check, if e=[K:Q], each
support point has degree at most eg over Q, while a pair lies in a field
of degree at most eg^2. Thus the nonzero values eta(P_i) and z_i-z_j have
polynomial logarithmic lower bounds at each embedding by
log|sigma(a)|>=-[Q(a):Q]h(a). No factorial splitting-field degree or
independent separation promise is needed. These lower bounds do not
amount to an algorithm that labels or computes the individual roots.

## 6. Closed-algebra construction and actual bit scope

Suppose E is supplied by its finite K-algebra R=H^0(E,O_E), with unit and
multiplication by x and y, or by a closed ideal from which this algebra
is computed with the input representation cost charged. For a candidate
integer c form M_z=M_x+c M_y. Both goodness conditions have tests over K:

* F_y(M_x,M_y)-cF_x(M_x,M_y) is invertible;
* the columns 1,z,...,z^(g-1) form a basis of R.

The first tests eta on the reduced support. The second tests that z
generates the entire, possibly nonreduced, algebra. At a good c both
hold. Take A=charpoly(M_z); solve the power-basis linear systems for the
coordinates B of x and C of y. Cyclicity makes this characteristic
polynomial the degree-g minimal polynomial, giving precisely (3)--(5).
This needs polynomially many field operations and standard exact linear
algebra. It neither factors A nor constructs the joint support splitting
field. For multiple divisors, the tests can be done separately over their
own charged definition fields with the same integer c.

Let e=[K:Q], and charge a concrete field presentation of height B_K,
including any basis changes. For example K=Q(theta) in its power basis
has h(theta) bounded by the height of its supplied defining polynomial.
The trace Gram matrix

    T_ij=Tr_(K/Q)(theta^(i+j)),    0<=i,j<e,

has entries of height polynomial in e and B_K; its determinant is
nonzero by separability. Cramer's rule gives a trace-dual basis beta_j
of height polynomial in e and B_K, with no lower-discriminant assumption.
If a=sum_j q_j theta^j, then q_j=Tr(a beta_j), so

    h(q_j) <= e h(a)+poly(e,B_K).                        (13)

Using (2) in (13), every rational coordinate of A,B,C has numerator and
denominator of binary length at most

    L=poly(e,B_K,D,g,H_F,H,h_c).                          (14)

There are O(eg) such coordinates, hence polynomial total output size.
An arbitrary field basis of arbitrarily large height can destroy a bound
stated using e alone; its presentation height must not be omitted.
Exact construction time additionally depends on the actual input
ideal/algebra's size and coefficient heights. A support-height existence
bound does not itself supply those input matrices for free.

For a reconstruction threshold, enlarge L so every rational coordinate
has numerator and denominator of absolute value <=2^L. If its residue
modulo an integer M is available and its denominator is coprime to M,
M>2^(2L+1) makes that coordinate unique by the cross-product bound for
two distinct fractions. Standard rational reconstruction then recovers
it in polynomial bit time. Certified real coordinate approximations
of error less than 2^(-2L-2) also isolate at most one such fraction.
These are conditional precision thresholds for correctly aligned
coordinates in the charged field presentation. They do not supply a
good prime, compatible field embeddings, the residues, a numerical lift,
or Galois descent from incompatible local data. A bad denominator prime
cannot simply be called good because its size is convenient.

## 7. Polynomial chart-exception count and use of support premises

Let the projective plane closure have degree D. The normalization's
pullback of a line has degree D. Therefore at most D geometric points
lie over the line at infinity. A nonzero polar of the defining homogeneous
equation has degree D-1, vanishes at all plane singular points, and can
be chosen to share no component with the reduced curve in characteristic
zero. Its pullback zero divisor has degree D(D-1). Every normalization
branch above a singular point contributes at least one. Consequently

    # {points outside the affine nonsingular plane locus} <= D^2. (15)

For D=1 there are no singular points. On the remaining locus the
normalization is an isomorphism, so the xy construction needs no extra
inverse-chart denominator. If a different supplied chart is used, its
additional denominator divisors must be charged: equations of degrees
k_i add at most D sum_i k_i preimages, unless a denominator vanishes
identically on a component and that chart is invalid there.

Thus the common-basepoint avoidance argument can charge A<=D^2 in
S_(N,A)=d+1+h_B+log(N(A+1)+1), in addition to whatever other exceptions
the chosen representation actually needs. This does not pay the degree
or coefficient height of a plane model that has not yet been produced.

If the preceding height theorem bounds only x=pi, there is a short
additional coordinate step when F is absolutely irreducible of positive
y-degree (or the x-map is nonconstant on every relevant component).
F(alpha,Y) is not the zero polynomial: otherwise x-alpha would be a
component. Specialization of the coefficient vector and the elementary
root-height bound give

    h(beta) <= H_F+D h(alpha)+C log(D+2).                 (16)

This remains true when the leading y-coefficient vanishes at alpha;
use the actual nonzero specialized polynomial. Summing with
multiplicities supplies (1) with

    H <= (D+1) sum_i m_i h(alpha_i)
         + g[H_F+C log(D+2)].                            (17)

No such deduction is valid on a vertical component with constant x.
In the intended finite-cover setting (17) transfers the established
pi-value bound to both plane coordinates once a polynomial-degree,
polynomial-height plane equation has been supplied.

## 8. Claim boundary and falsifiers

The accepted bridge is (2), the closed-algebra construction, and the
charged-field bit threshold (14). It includes arbitrary multiplicities
up to g, with explicit tangent denominators and interpolation denominators.
The strongest simple failures of a weaker statement are:

* Two branches over a plane singularity have identical x,y, so no c can
  give the asserted generator. Avoid those points as in (15).
* At a ramified support point, z-z_i need not generate the local maximal
  ideal; distinct support values alone do not encode a thickened divisor.
  The eta test is essential.
* Values x(P),y(P) without the curve equation do not determine jets.
  Equations (6)--(10), including H_F, are essential for the height claim.
* A degree-only number-field budget omits arbitrary basis conditioning;
  (13)--(14) require a charged field presentation.
* A height bound and an abstract divisor class do not provide a closed
  ideal, a canonical choice, an appropriate lift, or aligned local data.

No original-prime Frobenius identification, new native good-model theorem,
or unconditional reconstruction of unavailable torsion data follows here.
