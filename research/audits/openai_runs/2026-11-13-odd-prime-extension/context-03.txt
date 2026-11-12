# A global Haar tail for actual reduced Mumford coordinates

2026-11-13. Focused independent proof after STATE/TRAPS,
`LOCAL_HALVING_SATURATION.md`, `LOCAL_KUMMER_NATIVE_PERTURBATION.md`, the
complete proof-only volume-cover review, and the coset-volume report review.
No API, network, Git, implementation or numerical sweep. Commands used
`/opt/anaconda3/bin/python`. Parent owns shared notes.

## Verdict and explicit theorem

ACCEPT the proposed coordinate-only global-tail mechanism, with the
same-closed-point conjugates handled by embedding DIFFERENCE LINEAR FORMS,
not an independence assumption. This proves a Haar reset bound uniform in
the incoming translate. It does not prove finite-grid transfer, constructive
Mumford reduction, Stoll matrix conditioning, or ONE-HALF.

Let f in Z[x] be monic squarefree of degree 2g+1, g>=1, and let
C:y^2=f(x), G=Jac(C)(Q2). Extend v2 by v2(2)=1 to Q2bar. For the actual
reduced Mumford pair [a_P,b_P], with a_P monic and deg b_P<deg a_P<=g, set

    beta_coord(P)=max(0, -v2(c): c a coefficient of a_P or b_P),

with v2(0)=infinity. This concerns coordinates on ALL of G; no halving
square root or successful-divisibility data enter the definition.

Use the Haar measure mu_omega determined by
omega_0 wedge ... wedge omega_(g-1), omega_j=x^j dx/(2y). Define integers

    D=v2(disc f),       N_c=4D+12,
    M=2ceil(log2 g)+4,  a_free=N_c-(D+2)=3D+10,
    Delta_*=g(1+ceil(log2 g)),
    A_count=3g+gM+2gN_c,
    A_tail=A_count+a_free+Delta_*+3+2ceil(log2 g),
    c_g=6g-3.

Then for every integer s>=0,

    mu_omega{P: beta_coord(P)>c_g*s} <= 2^(A_tail-s).      (1)

In particular, for integer K>=0, a convenient conventional tail is

    mu_omega{beta_coord>=K} <= 2^(A_tail+2-K/c_g).         (2)

All displayed exponents are explicit polynomials in the native parameters:
D=O(g(B+log(g+1))) by the nonzero integer Sylvester discriminant bound.
No regular model, field closure, list of local fields or coordinate chart
is supplied to an algorithm by this theorem.

## 1. Which volume-cover facts are reused

The proved index review
`2026-11-07-local-saturation-index.md`, Sections 2--4, supplies a cover by
at most 2^A_count trace-product charts. A chart is on a product of C(E_i),
with sum_i [E_i:Q2]=g, mapped by

    (P_i) -> sum_i Trace_(E_i/Q2)[P_i-infinity].

For an integral affine chart the FREE coordinate is exactly

    free=free_0+2^a_free z,       z in O_E.                (3)

The other coordinate is the proved strict Hensel graph. Both coordinates
remain integral throughout the chart. The selected partial derivative has
valuation at most D+1; the scaling in (3) and the dependent scaling in the
index proof make every pulled-back omega_j integral.

For the infinity chart use u=1/x and w=y/x^(g+1):

    w^2=u F(u),       F(u)=u^(2g+1)f(1/u),       F(0)=1.

The map u->uF(u) has an integral inverse on the maximal ideal. It is useful
here to use w ITSELF as parameter on m_E, measured by additive Haar with
mu_E(O_E)=1. This is the same region as the index proof's w=pi_E z chart,
but its parameter domain now has volume at most one, not renormalized to
volume one. The formula

    omega_j=-u^(g-1-j) dw/(F(u)+uF'(u))

still has integral coefficients. This avoids silently unscaling a
uniformizer while retaining the old domain normalization.

Choose integral Z2-bases in the E_i. Derivatives of the trace map have
entries Trace_(E_i/Q2)(an integral element), so its omega-Jacobian has
absolute value at most one. The analytic area inequality used in the
index proof applies to EVERY measurable parameter subset B:

    mu_omega(Phi(B)) <= mu_parameters(B).                (4)

The noncritical part follows by local change of variables, discarding
preimage multiplicity; critical images have measure zero. Thus a bad-set
estimate in parameter volume transfers to G without an inverse-Jacobian
denominator. All the field types, bases and centers remain proof-only.

## 2. An explicit bound for dependent conjugate linear forms

Let E/Q2 have degree e<=g and field discriminant exponent d_E. Its maximal
unramified subfield has residue degree f_E, and E over it has ramification
index r_E. A uniformizer has an Eisenstein polynomial of degree r_E. Its
derivative terms at that uniformizer have distinct valuation residues modulo
r_E, so the smallest term cannot cancel. Therefore the different exponent
is at most r_E*v2(r_E)+r_E-1, and

    d_E <= e(1+log2 e) <= Delta_*.                       (5)

Take an integral Z2-basis e_1,...,e_e of O_E with e_1=1. Such a basis exists
because 1 is primitive. Its embedding matrix has determinant valuation
d_E/2. For DISTINCT embeddings sigma,tau:E->Q2bar, subtract the tau row
from the sigma row. All other entries are integral and the determinant is
unchanged. Hence some j satisfies

    v2(sigma(e_j)-tau(e_j)) <= d_E/2.                    (6)

For the PLUS form, e_1=1 gives sigma(e_1)+tau(e_1)=2, of valuation one.
This proves both nonvanishing and a polynomial content bound; it does not
treat conjugates as independent random variables.

Here is the elementary measure consequence. For z=sum_j z_j e_j with
z_j in Z2, freeze all but a coordinate whose linear coefficient has valuation
at most b. A set satisfying

    v2(c+linear_form(z))>=q

is empty or lies in one Z2 ball of measure at most 2^(b-q). Indeed subtract
two solutions and divide by that nonzero coefficient. The bound is valid
also when its right side exceeds one. Fubini gives the same upper bound
on O_E. It is uniform in the affine constant c, regardless of how close a
chart center is to an exact collision.

We also use the elementary degree-two version: for a variable z_j in Z2,

    mu{v2((c+2^a z_j)^2-d)>=2s} <= 2^(a+1-s).           (7)

Factor over Q2bar and note that one root distance has valuation at least
s-a. The root may lie outside Q2; intersection with Z2 is still empty or
one such ball. No support splitting field is constructed.

## 3. Pairwise x-collision tubes on every product chart

Consider any TWO DISTINCT geometric support points supplied by a trace
tuple, and the event v2(x_i-x_j)>=2s. All chart parameters are free before
we later restrict to a Jacobian coset. There are three location cases.

**Both points integral, from different closed points.** Freeze all parameters
of the second point. If the first chart is x-free, freeze all but the basis-1
coordinate in (3): x_i-x_j is affine linear with coefficient 2^a_free.
The event has measure at most 2^(a_free-2s).

If the first chart is y-free, integrality of f gives

    v2(y_i^2-y_j^2)=v2(f(x_i)-f(x_j))>=v2(x_i-x_j).

Apply (7) to its free y coordinate, with y_j fixed. The bound is
2^(a_free+1-s). This includes arbitrary dependence within the second point;
only the parameters of different product factors were conditioned separately.

**Both points integral, conjugates within the SAME closed point.** In an
x-free chart, x_i-x_j is the affine form
const+2^a_free(sigma(z)-tau(z)); (6) gives measure at most
2^(a_free+d_E/2-2s). In a y-free chart the collision implies

    v2((sigma(y)-tau(y))(sigma(y)+tau(y)))>=2s.

One of its TWO factors has valuation at least s. Apply (6) to the difference
and the basis-1 coefficient 2 to the sum. Their union has measure at most

    (2^(a_free+d_E/2)+2^(a_free+1))*2^(-s).              (8)

This is the missing dependent-conjugate argument.

**Infinity points.** If one point is integral and the other has nonintegral
x, their x-difference has negative valuation and never enters this event.
For two infinity points, write x_i=1/u_i. Then

    v2(x_i-x_j)>=2s
      => v2(u_i-u_j)>=2s+v2(u_i)+v2(u_j)>=2s.

Because uF(u) is integral, this implies v2(w_i^2-w_j^2)>=2s. Different
closed points are covered by (7) with a=0. Conjugates within one closed
point are covered by the two linear forms sigma(w) plus/minus tau(w),
using (6) and the coefficient 2. These estimates may be made on all O_E
and then restricted to m_E; the latter restriction only lowers measure.

Every case is therefore bounded by the single safe expression

    mu_parameters{v2(x_i-x_j)>=2s}
       <=2^(a_free+Delta_*+2-s).                        (9)

Embeddings are only labels in this proof. Their normal closure is neither
built nor counted as a computational field degree.

## 4. Pole tails and actual Mumford coefficient bounds

For an infinity point, F(u) is a unit, so

    v2(u)=2v2(w),
    v2(x)=-2v2(w),       v2(y)=-(2g+1)v2(w).

These are the needed equalities; the stronger literal assertion x=w^-2
would be false in general because of the unit F(u). For integer s>=0,

    mu_E{w in m_E: v2(w)>s} <=2^(-[E:Q2]s)<=2^(-s).    (10)

On a product chart exclude the at most g events in (10), and the at most
binom(g,2) events in (9). Outside them every geometric support point obeys

    v2(x_i)>=-2s,       v2(y_i)>=-(2g+1)s,
    v2(x_i-x_j)<=2s   for i!=j.                         (11)

It suffices to argue on the full-measure open subset of G where the unique
degree-g effective representative of P+g infinity has distinct finite
x-coordinates. The degree-drop, repeated-support and hyperelliptic-pair
loci form a proper algebraic subset. Its Q2-points have Haar measure zero,
also inside every positive-volume open coset. This follows from the usual
birational Abel map Sym^g C->J; equivalently from the generic reduced Mumford
chart. Every trace-product representative of a point in this open set is
that SAME unique effective divisor, not an unrelated good representation.

For these actual support coordinates,

    a_P(X)=product_i (X-x_i),
    b_P(X)=sum_i y_i product_(j!=i)(X-x_j)
                       /product_(j!=i)(x_i-x_j).

Equation (11) gives coefficient valuations at least -2g*s in a_P and at
least

    -(2g+1)s-2(g-1)s-2(g-1)s=-(6g-3)s

in b_P. Nonarchimedean addition introduces no further loss. Thus
beta_coord(P)<=c_g*s. The exceptional set can retain its actual lower-degree
or repeated-support Mumford coordinates; its measure-zero contribution
does not change any bound. This is not an infimum over favorable charts.

For one product chart the union of excluded parameter events has measure
at most

    g^2*2^(a_free+Delta_*+3-s).

Apply (4), then sum over at most 2^A_count charts. This proves (1), with
the stated A_tail. Taking s=floor((K-1)/c_g) proves (2) for K>=1; K=0
follows from the already proved total-volume bound.

## 5. Uniform translation into the actual subgroup U

The native perturbation note proves

    mu_omega(U)=2^(-gR-H),
    log U=2^R W Z2^g,

with R=D0+1 and H=v2(det W). The order reversal between its differential
basis and omega_0,...,omega_(g-1) is a unit determinant and does not change
the Haar normalization. For EVERY h in G and integer k>=0, set

    s=A_tail+gR+H+k,       S_coord=c_g*s.

Translation invariance and (1) give

    Pr_(e Haar on U)[beta_coord(h+e)>S_coord]
       <=2^(gR+H) mu_omega{beta_coord>S_coord}
       <=2^(-k).                                       (12)

There is no dependence on h, on an incoming reduced-coordinate height, or
on whether h is divisible by two. The actual sigma parameterization pushes
Haar measure on Z2^g to Haar measure on U by its already proved strict-
contraction coordinate change. Thus (12) applies to h+sigma(z) for Haar z.
For h+2sigma(z), use 2U instead and add g to s, since mu(2U)=2^-g mu(U).

With fixed seed exponent n_s, the displayed S_coord is, conservatively,
O(g^3 B+g^4 log(g+1)+g*k); allowing the actual seed exponent adds
O(n_s*g^4). The explicit formulas, rather than this coarse envelope, are
the theorem's precision parameters.

## Boundary of what has been proved

This closes a coordinate-pole HAAR tail and its all-coset probability
transfer. It uses an analysis-only chart cover and integral bases, without
constructing or enumerating them. It does not compute the canonical pair,
bound the intermediate pivots of an RR/Cantor implementation, transfer the
event to a finite parameter grid, or prove stability at a materialization
error scale. It says nothing about the Stoll square root, all tested
M_j/B_j matrices, or successful halving outside its promised domain.
ONE-HALF and the complete native local Kummer image remain OPEN.
