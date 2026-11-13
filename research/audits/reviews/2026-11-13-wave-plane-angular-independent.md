# Polynomial resonance oval and a finite-bit angular compiler

Date: 2026-11-13. Independent mechanism review after STATE/TRAPS. Actual
primary: Bos--Levenberg--Taylor, *Characterization of smooth, compact
algebraic curves in R2*, retained `sources/new_native_wave/tangential_markov.txt`,
Main Theorem at physical lines 53--69 and proof 1=>2 at lines 71--151.
No live paid angular report, network, API, Git, implementation, or sweep.

**Disposition.** The polynomial embedding is exact, the actual tangential
Markov theorem applies, and algebraic optimization removes any need to
supply its unspecified constant. This yields a classical finite-clock
sampler for the finite-precision cell pushforward of |F|^2 times arclength
on either K or the native resonance curve Gamma. Cost is polynomial in
NUMERICAL exponent radius D, coefficient/input bits, requested output bits,
and log(1/epsilon). It is not a polynomial-in-log(D) result for arbitrary
binary sparse exponents. No spatial Green-law conclusion follows.

A literal finite-output distribution has TV distance one from an absolutely
continuous angular law. The cell-output contract is stated explicitly in
Section 5; no continuous-real output oracle is silently supplied.

## 1. Exact real equivalence and global geometry

Take the principal torus representatives of

    Gamma={ (p,q): 2cos p+2cos q=3 }.

Both cosines lie in [1/2,1], so p,q are uniquely in [-pi/3,pi/3]. Put
x=sin p, y=sin q, u=x^2, v=y^2, s=u+v, d=u-v. Then

    A=cos p=3/4-d/3,   B=cos q=3/4+d/3,
    Q(x,y)=16(x^2-y^2)^2+72(x^2+y^2)-63=0.                 (1)

Conversely every REAL zero of Q gives this native branch. Indeed s>=|d|,
so 16d^2+72|d|<=63 and hence |d|<=3/4. Therefore A,B are in [1/2,1].
A direct calculation from Q=0 gives A^2+x^2=B^2+y^2=1. Thus the unique
p=arcsin x, q=arcsin y in [-pi/2,pi/2] satisfy cos p=A, cos q=B and lie
in [-pi/3,pi/3]. There are no extraneous real components from squaring.
The sine map and its inverse are smooth, with inverse differential norm
between 1 and 2 on tangents.

Let K={Q=0} in R2. In polar coordinates its squared radius s is the unique
positive solution of

    16s^2 cos^2(2theta)+72s-63=0.

It varies smoothly with theta, and

    3/4<=x^2+y^2<=7/8,   |x^2-y^2|<=3/4.                  (2)

This proves compactness, connectedness, and that K is a simple closed oval.
Moreover

    Q_x=16x(9+4d),   Q_y=16y(9-4d),
    48sqrt(3)<=||grad Q||<=192sqrt(7/8).                    (3)

In particular Q has no real singular point on K. These statements concern
the entire real algebraic zero set, not a selected regular subarc.

## 2. Polynomial restriction and the actual BLT theorem

On K the four Laurent generators are EXACT degree-two polynomials:

    exp(+-ip)=A+-ix,   exp(+-iq)=B+-iy.                     (4)

Their positive and negative versions multiply to one. Consequently a
Laurent polynomial

    F(p,q)=sum_(|a|,|b|<=D) c_(a,b) exp(i(ap+bq))

restricts to a complex polynomial f(x,y) of degree <=4D. Negative exponents
use the opposite sign in (4), not division by a variable denominator.
For rational complex input coefficients with total bit length B_in, the
expanded two-variable polynomial has O((D+1)^2) coefficient positions and
coefficient bit height polynomial in B_in+D+log(m+1). For example, the
four generators have denominator 12 and bounded coefficient l1 norm, so
power expansion adds only O(D) bits before summing the input terms.
Repeated squaring or direct polynomial multiplication takes polynomial BIT
work in m,D,B_in. A translation of the exponent support only multiplies F
by a unit phase and may be removed before handling |F|^2. This means one
common integer translation; choosing individual periodic lifts is a separate
interface, since exp(i L p) is not identically one on continuous Gamma.

The primary Main Theorem explicitly assumes a smooth compact connected
plane curve and proves

    ||D_T g||_K <= C_K deg(g) ||g||_K                       (5)

for every polynomial, with D_T the UNIT tangential derivative. Its actual
proof uses the algebraic complexification, local regular charts, a
Lipschitz extremal-function bound, and Cauchy's formula at radius r0/deg(g).
It concludes a constant depending only on the fixed K. Thus it gives the
linear degree exponent needed here, but no explicit numerical C_K.
All its geometric hypotheses are proved in Section 1. It is not a theorem
about an arbitrary analytic curve or about a half-angle rational function.

For complex f, apply (5) at any point to Re(exp(-i phi)f), choosing phi so
its tangential derivative there has modulus |D_T f|. This gives the same
constant for complex f. In particular

    ||D_T f||_K <=4 C_K D ||f||_K.

Set P=|f|^2, a nonnegative real polynomial of degree <=8D, and define

    S=max_K P,   H=max_K |D_T P|.

Then H<=8 C_K D S. At a maximum, P remains >=S/2 along an arclength
interval of radius min(length(K)/2,S/(2H)), with the constant case treated
separately. Hence

    ||f||_K^2 <= C'_K (D+1) integral_K |f|^2 ds_K.           (6)

The +1 handles D=0. All constants are coefficient-independent. An ambient
expression Q*G+2^(-B)R causes no loss in (5)-(6): only its actual restriction
enters. If S=0, however, the normalized angular law is undefined and must
be detected exactly rather than assigned an arbitrary normalized state.

## 3. Effective extrema without advice or generic-critical-point assumptions

The needed extrema can be computed exactly as real algebraic numbers.
Let

    V=Q_x^2+Q_y^2 >=6912 on K,
    N=Q_x P_y-Q_y P_x.

Then H^2=max_K N^2/V. Encode S, for example, by the first-order formula

    exists x,y: Q(x,y)=0 and P(x,y)=S,
    and for all u,v: Q(u,v)=0 implies P(u,v)<=S.

For H^2 replace P by N^2/V and clear the POSITIVE denominator V.
These formulas use a fixed number of real variables, polynomially many
coefficient bits, and polynomial degrees in D. Complete fixed-dimensional
real quantifier elimination/CAD, using rational polynomial arithmetic,
subresultants, and univariate real-root isolation, has polynomial BIT cost
in these degree/height parameters: its dimension-dependent exponent is
fixed here. It outputs defining polynomials and isolating intervals for
both extrema. This is the standard complete real-algebraic algorithm,
not just a resultant of a presumed finite critical-point set. Constant
restrictions, multiple critical roots, critical arcs, and vanishing
projection polynomials are included in its degenerate cases.

In particular S=0 is decidable exactly. In that case return ZERO, certifying
that this angular target is undefined. If S>0, the output algebraic degree
and coefficient bit height are polynomial in the input parameters. Removing
any zero factors from its defining polynomial and applying the elementary
reciprocal-root bound gives S>=2^(-poly(D,B_in,m)). Thus refining to relative
constant accuracy takes only polynomially many bits, even for a very small
nonzero restriction.

Compute dyadic numbers with

    0<Slo<=S<=2Slo=:Shi,
    H<=Hbar<=H+Slo,
    R=1+ceil(Hbar/Slo).                                    (7)

Square-root isolation gives H from H^2; refine its upper endpoint to width
Slo. All ceilings and ratios in (7) are exact rational operations. Since

    R<=3+2H/S<=3+16 C_K D,                                 (8)

R is O(D+1). The PROGRAM does not know or use C_K: it computes R and uses
that integer in its iteration caps. The theorem supplies the polynomial
worst-case analysis, while the actual input-dependent finite cap is fully
computable. Neither a norm oracle nor an unknown constant is advice.

## 4. Four regular charts and arclength Jacobians

Put a=sqrt(7)/4. The chart y>=|x| is exactly

    -a<=x<=a,
    y=sqrt(x^2-9/4+3sqrt(1-x^2)),   y>=a.                  (9)

The other three charts are its lower, left, and right signed/swapped
versions. They partition K except for four boundary points, a null set
for all laws considered here. Writing c=sqrt(1-x^2), on (9) one has
c>=3/4 and

    y'=(x/y)(1-3/(2c)),   |y'|<=1,
    |y''|<=128/(9sqrt(7))<6.                               (10)

For the second bound, differentiate y^2: its second derivative is
2-3/c^3, of absolute value <=46/9, then use y>=a and |y'|<=1.
Thus the K-arclength Jacobian J_K=sqrt(1+(y')^2) satisfies

    1<=J_K<=sqrt(2),   |J_K'|<=6,
    2sqrt(7)<=length(K)<=2sqrt(14).

For native Gamma arclength, A=cos p and B=cos q on this chart give

    J_Gamma=sqrt(A^(-2)+(y')^2 B^(-2)).

Here A>=3/4, B>=1/2, |A'|,|B'|<=1. Therefore

    1<=J_Gamma<=2sqrt(2)<3,   |J_Gamma'|<=40.               (11)

Indeed the derivative of J_Gamma^2 has magnitude <=16+48+16=80,
and J_Gamma>=1. These fixed algebraic formulas, with denominators uniformly
away from zero, are evaluable to h bits in polynomial BIT time. No arcsine
is needed to evaluate f or either Jacobian.

## 5. A capped sampler with an explicit finite-output contract

Assume 0<epsilon<=1/4; a larger error request can use epsilon=1/4.
Parameterize each chart by t in [0,1], x=a(2t-1). The requested output is
(chart, floor(2^b t)) for a given integer b>=0, under the normalized measure
P ds_K or P ds_Gamma. Boundary ties may be fixed arbitrarily. This is the
finite-precision cell PUSHFORWARD of the continuous law. A point at the
cell midpoint, or corresponding angles p,q to b+O(1) bits, can subsequently
be computed; that is a coordinate-accuracy claim, not literal continuous TV.

Choose the chart uniformly among four and t uniformly in [0,1] as the
ANALYSIS proposal. With J either Jacobian above, accept with probability

    A_c(t)=P(x(t),y(t)) J(x(t))/(3Shi).                     (12)

This lies in [0,1] and gives exactly the desired conditional continuous
law. Its derivative in t has magnitude <=128R, by (7), (10)-(11), and
|dP/dx|<=sqrt(2)H. Some chart has a point with P=S, where A_c>=1/6.
On a one-sided interval of length 1/(1536R), it remains >=1/12. Including
the probability 1/4 of selecting that chart proves the explicit lower bound

    p_accept>=1/(73728R)>p0,   p0=2^(-17)/R.               (13)

No integration or unknown normalization is required for this bound.

The implemented finite-bit sampler needs no continuous uniform real.
Take a power of two N=2^q with

    N>=2^30 R^2/epsilon.

Choose a chart and j uniformly in {0,...,N-1}, using 2+q bits, and evaluate
(12) at t_j=(j+1/2)/N. Its piecewise constant midpoint approximation differs
uniformly from (12) by at most 64R/N<=epsilon p0/128. Evaluate and round
its acceptance probability to a dyadic Ahat_j in [0,1] with error at most
epsilon p0/128; for example use

    h_acc=ceil(log_2(256/(epsilon p0)))

random acceptance bits, an elementary-function evaluation error at most
epsilon p0/256, and a dyadic threshold on that many bits. Clipping preserves
the error bound. The exact finite proposal then succeeds with probability
at least p0/2. Its hypothetical piecewise constant continuous conditional
law has TV error at most epsilon/64, since its unnormalized L1 error is at
most epsilon p0/64 and the true acceptance is at least p0.

On acceptance retain the chart label. If b<=q, return the first b bits of
j; if b>q, append b-q independent fair bits to j. This samples exactly the
b-bit cell pushforward of that piecewise constant law, so the same TV bound
holds for the actual
finite output. No enumeration of N cells is performed.

Cap the number of fresh attempts at

    Ntry=2^18 R ceil(log_2(4/epsilon)).                     (14)

The integer ceiling is computed by rational comparisons with powers of two.
Exhaustion probability is <=epsilon/4; on exhaustion output a fixed legal
cell. Consequently the complete output law is within epsilon TV of the
specified cell pushforward, with a deterministic worst-case clock.

All evaluation precision is paid. At t_j the chart coordinates, derivatives,
and Jacobians are fixed-degree algebraic numbers with heights polynomial
in q. Evaluate the degree-O(D) polynomial P by rational interval Horner
arithmetic. An ambient coefficient l1 bound has polynomial logarithm, and
log(1/Slo) is polynomial by Section 3. Thus absolute accuracy relative to
Shi in (12) requires only polynomially many bits in D,B_in,q,log(1/epsilon).
The square roots in the charts have positive fixed lower bounds. Interval
root refinement or dyadic bisection provides the claimed deterministic
rounding certificate. Together with (8), (14), and q=O(log R+log(1/epsilon)),
this proves polynomial BIT time in m,D,B_in,b,log(1/epsilon).

## 6. Fixed geometric weights and the remaining scope boundary

The closed sampler above covers both pure K and pure Gamma arclength.
Some common native factors are also manifestly positive algebraic functions:

    |grad_(p,q)(2cos p+2cos q-3)|=2sqrt(x^2+y^2)
          in [sqrt(3),sqrt(7/2)],
    curvature_Gamma=(A y^2+B x^2)/(x^2+y^2)^(3/2)
          in [sqrt(2/7),2/sqrt(3)].

A SPECIFIED fixed positive C1 algebraic weight can be incorporated: compute
its positive minimum, maximum, and derivative bound on these fixed charts
by the same constant-variable real-algebraic methods, then replace the
fixed constants in (12)-(14). Products and fixed rational powers of the two
displayed nonvanishing factors have the required nonsingular algebraic formulas.
There is no unknown geometric-weight oracle in this extension.

However, the precise stationary-phase weight of any later spatial proposal
must still be identified and checked against its source formula. No such
unspecified weight, uniform finite-lattice stationary-phase remainder,
source-dependent spatial normalizer, or full spatial sampler is claimed
here. The proved new mechanism is the polynomial compact angular compiler
with the explicit finite-output convention and numerical-D resource bound.
