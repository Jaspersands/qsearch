# Local saturation index: proof-only analytic cover

2026-11-07. CLOSED independent addendum to
`2026-11-07-local-saturation-core.md`. The argument below proves a
polynomial bound on the number of index-two saturation steps at every p for
the native monic integral input; Section 6 supplies the odd-prime extension.
It does not prove a stable polynomial-BIT
implementation of each step. No local fields, analytic chart centers,
Neron model or component groups are supplied to the algorithm as advice.
No finite control, network request or implementation was used here.

## 1. Statement and constants

Let f in Z[x] be monic and squarefree of degree d=2g+1, g>=1, and let
C:y^2=f(x), J=Jac(C). Write D=v_2(disc f). Use the formal seeds of the
core review with t_i=2^(N_s)i, N_s>=2 (one can fix N_s=2), and let

    D0=N_s g^2+sum_i v_2(i)+sum_(i<j) v_2(j^2-i^2).

Let Hbar0 be their closed span together with all rational 2-torsion, and
t=dim_F2 J(Q_2)[2]. Define

    A=D+2,    N_c=4A+4=4D+12,
    M=2 ceil(log_2 g)+4.

Then the exact number kappa of successful index-two enlargements in the
abstract saturation procedure satisfies the coarse bound

    kappa <= D0+2g N_c+g M+3g-t
           <= D0+2g N_c+g M+3g.

For coefficient bit size B, the nonzero integer discriminant has
log_2 |disc f|=O(g(B+log(g+1))) by the Sylvester determinant bound.
Consequently D obeys this bound, and the displayed kappa bound is
polynomial in the native input size. The proof controls the actual
index directly, rather than separately bounding a Neron differential
correction and a component group.

## 2. Counting local field types without constructing them

The following elementary bound works over Q_p. Put
M=2 ceil(log_p g)+4. For e<=g the number of degree-e extensions of Q_p,
up to Q_p-isomorphism, is at most e p^(eM).

Indeed a degree-e field has a unique maximal unramified subfield U of
degree f dividing e, with total ramification degree m=e/f over U. A
uniformizer pi generates the field over U and has a monic Eisenstein
minimal polynomial F of degree m. With v_p(p)=1, the derivative terms
at pi have, in the integer-valued extension valuation, distinct residues
0,...,m-1 modulo m. Thus there is no cancellation at the least-valued
term, and

    v_p(F'(pi)) <= v_p(m)+(m-1)/m < log_p(g)+1.

If another monic Eisenstein G has the same coefficients modulo p^M,
then v_p(G(pi))>=M and G'(pi) has the same valuation as F'(pi).
The strict Hensel inequality M>2v_p(G'(pi)) gives a root of G in the
original extension. Since G is Eisenstein of the same degree m over U,
this root generates the same extension. Thus a coefficient residue
class determines at most one U-isomorphism type. There are p^(fMm)=p^(eM)
coefficient residue choices for each f, and at most e choices of f.
This avoids invoking a field count with an unspecified degree-dependent
constant. Krasner's lemma is not needed after this Hensel argument.

For ordered tuples (E_1,...,E_r) with sum_i [E_i:Q_p]=g, sum over
compositions e_1+...+e_r=g. There are at most 2^(g-1) compositions,
product_i e_i<=2^g, and every product of field-type counts is at most
(product_i e_i)p^(gM). Therefore the total number of tuples is bounded
by 4^g p^(gM). Counting ordered tuples and duplicates only enlarges
the upper bound. This is a counting proof, not an enumeration algorithm.

## 3. Integral analytic charts on C(E)

Fix one degree-e extension E/Q_p and its ring of integers O_E. Here f
is monic integral and D=v_p(disc f). Every affine point either has
x,y in O_E, or lies in the infinity region described below.

There are integral polynomials U,V with

    U f+V f'=disc f

up to an irrelevant sign, by the integral Sylvester-adjugate identity.
At an integral point (x_0,y_0), f(x_0)=y_0^2, so

    min(v_p(2y_0),v_p(f'(x_0))) <= D+1 < A=D+2.

For example, if v_p(f'(x_0))>D, the Bezout identity forces
2v_p(y_0)<=D, which gives the claimed bound for 2y_0. This applies
uniformly to ramified E; fractional valuations cause no change.

There are p^(2eN_c) residue pairs modulo p^(N_c)O_E. For each nonempty
pair choose one exact point for this existence proof. Select as dependent
coordinate the coordinate whose partial derivative delta in
y^2-f(x) has smaller valuation a, so a<A. Put R=N_c-A and write

    free coordinate = free_0+p^R z,
    dependent coordinate = dependent_0+p^(R-A) w.

Divide the defining equation by delta p^(R-A). Its w-linear term at
(z,w)=(0,0) is w. All other coefficients are in p O_E: the free-only
part has valuation at least A-a>=1, and the higher dependent terms
have valuation at least R-A-a>0. The cross terms have the same or
better bounds. Thus it is a uniform strict contraction in w on O_E,
giving a restricted analytic w(z) for all z in O_E. This chart contains
the entire original residue pair: both coordinate differences divisible
by p^(N_c) fit the displayed scales, and uniqueness of the contraction
solution gives the original point. It may also cover extra points,
which is harmless.

On the chart the selected partial derivative has its constant valuation
a: its variation is divisible by p^(R-A), of valuation greater than a.
For omega_j=x^j dx/(2y), 0<=j<g, use either

    omega_j=x^j dx/(2y),  or  omega_j=x^j dy/f'(x),

according to the selected dependent coordinate. The free differential
contributes p^R, and p^R/delta is integral. The reciprocal of the selected
partial is delta^(-1) times an integral analytic unit. Hence every
pullback omega_j has integral restricted analytic coefficients on O_E.
This assertion concerns the whole chart, not just its center.

The remaining points have u=1/x in the maximal ideal. Write
w=y/x^(g+1). Then

    w^2=u F(u),   F(u)=u^(2g+1)f(1/u),   F(0)=1.

The map u -> uF(u) has an integral formal inverse near zero. Hence one
chart w=pi_E z, z in O_E, with u that inverse evaluated at w^2, covers
all the infinity region, including infinity itself. On this chart

    omega_j=-u^(g-1-j)/(F(u)+uF'(u)) dw.

Its coefficients are integral, since the denominator is a unit and
0<=j<g. Thus C(E) has a cover by at most

    p^(2eN_c)+1 <= 2p^(2eN_c)

one-E-dimensional analytic charts with all these differential
pullbacks integral. The centers and pi_E are proof-only choices.

## 4. Trace-map coverage and the volume inequality

There is no exceptional-locus coverage assumption. Every point of J(Q_p)
has its effective reduced Mumford divisor of degree d'<=g, as in the
actual Stoll Section 5 setup. Add (g-d') copies of infinity. Decompose
this rational effective divisor of degree g into closed points, with
multiplicity. Its residue fields have degrees totaling g. Consequently
every point lies in the image of one of the trace maps

    product_i C(E_i) -> J(Q_p),
    (P_i) |-> sum_i Trace_(E_i/Q_p)[P_i-infinity].

Repeated field types or repeated points are permitted. Replacing a
residue field by its chosen Q_p-isomorphic representative preserves
the image. This is only a finite existence cover, so no effective
divisor decomposition is being given to the saturation algorithm.

Normalize the Haar measure mu_omega on J by the invariant top
differential omega_0 wedge ... wedge omega_(g-1). Identify each O_E
with Z_p^e using any integral Z_p-basis, with domain Haar volume one.
Pullback through the trace map is the trace of the pullback through
the point map. A matrix entry of its derivative is therefore

    Trace_(E/Q_p)(h(z)b_i),

where h(z) is integral analytic and b_i belongs to the integral basis.
The trace of an integral element is integral. Thus the g-by-g Jacobian
of every product chart, measured by omega, has integral entries and
absolute determinant at most one.

The nonarchimedean analytic area inequality now gives
mu_omega(image chart)<=1. This inequality does not require injectivity:
on the noncritical locus the inverse function theorem and
change-of-variables formula count preimages with multiplicity at least
one. The critical image has measure zero, by analytic rank
stratification; equivalently one applies the local constant-rank theorem
on maximal-rank strata and induction on the lower-rank analytic loci.
Hence discarding multiplicity only decreases image volume. These are
existence statements about analytic maps, not numerical algorithms.

Each tuple requires at most 2^g p^(2gN_c) product charts. Combining
with the field-tuple count gives

    mu_omega(J(Q_p)) <= 8^g p^(gM+2gN_c).

No discriminant-dual denominator is omitted here: the chosen domain
bases are integral bases, and ordinary traces of integral products
are integral, even for wildly ramified fields.

## 5. Dyadic saturation consequence and remaining gate

At p=2 let L be the closed span of the formal seeds. On the formal
logarithm domain, the invariant differentials are the differentials of
their logarithm coordinates. The core determinant formula therefore
gives mu_omega(L)=2^(-D0). The rational 2-torsion intersects L trivially,
so mu_omega(Hbar0)=2^t mu_omega(L). Since G_(2) is contained in J(Q_2),

    2^kappa=[G_(2):Hbar0]
       =mu_omega(G_(2))/mu_omega(Hbar0)
       <=2^(D0-t) * 8^g * 2^(gM+2gN_c),

which proves the stated bound. The possibly enormous cover was used
only through its logarithm; executing or listing it would not be a
polynomial algorithm and is not part of this conclusion.

This closes the dyadic polynomial-ITERATION gate of the abstract
saturation route. It does not repair Stoll's stated finite-precision
halving issues, provide an exact p-adic equality oracle, or prove
uniformly conditioned point/factor/squareclass representations along
the successive halves. Those implementation requirements must still be
proved before the native complete-local-image algorithm is admitted.
No odd-prime iteration claim is inferred merely by applying a real
Haar-volume bound to the finite 2-primary torsion subgroup there.

## 6. Odd primes: an auxiliary open pro-p lattice

For odd p, the actual saturation algorithm starts with J(Q_p)[2] and
stays in the finite 2-primary torsion subgroup. Its step count is

    kappa_odd=v_2 |J(Q_p)[2^infinity]|-t.

To bound this number, use a separate analysis-only lattice. Set
N_s=4g^2 and choose the near-infinity points with t_i=p^(N_s)i,
1<=i<=g. They belong to the first Neron kernel K1. At odd p the
formal logarithm is already an isomorphism on K1, because
1>1/(p-1). No construction of K1 or its coordinates is required.

For odd p all coefficients c_m of F(t^2)^(-1/2) are integral: their
binomial denominators are powers of 4. Use the same Cauchy--Binet
expansion as in the core review. For an increasing tuple
l_0<...<l_(g-1), put Delta=sum l_j-g(g-1)/2. Its A-minor has an
integral numerator over product_j(2l_j+1). Relative to the leading
minor, whose numerator is 1 and denominator is product_j(2j+1),
its coefficient valuation is therefore at least

    -sum_j v_p(2l_j+1) >= -g log_p(2g+2Delta).

Here l_(g-1)<=g-1+Delta. The Schur factor contributes at least
2N_s Delta. For Delta>=1,

    g log_p(2g+2Delta)
       <=g(log_2(2g)+Delta)
       <=4g^2 Delta.

Thus every nonleading term relative to the leading one has valuation
at least 4g^2 Delta>0. The infinite sum converges for the same reason,
and the exact leading-term valuation is

    D_p=4g^4+sum_i v_p(i)+sum_(i<j) v_p(j^2-i^2)
             -sum_(k=0)^(g-1) v_p(2k+1).

In particular the logarithms are independent, and
D_p<=4g^4+O(g^2 log(g+1)). Let L_p be the closed Z_p span of these
seed points. It is a torsion-free open pro-p subgroup with
mu_omega(L_p)=p^(-D_p). It is an auxiliary object in the proof, not
an additional point source for the odd-prime saturation algorithm.

Set H_open=L_p+J(Q_p)[2]. The intersection is trivial and

    mu_omega(H_open)=2^t p^(-D_p).

The quotient J(Q_p)/H_open is finite. Passing modulo an open pro-p
subgroup preserves the prime-to-p torsion: for example, a lift of an
element of order 2^a can be corrected to a 2^a-torsion lift because
multiplication by 2^a is an automorphism on L_p. It follows that

    v_2[J(Q_p):H_open]=kappa_odd.

Now, and only now, apply the volume bound to this finite index. With
M=2 ceil(log_p g)+4 and N_c=4v_p(disc f)+12, Sections 2--4 give

    kappa_odd
       <=log_2[J(Q_p):H_open]
       <=3g+(D_p+gM+2gN_c)log_2 p-t.

This is polynomial in g, the coefficient bit size and log p. In
particular v_p(disc f)log_2 p<=log_2|disc f| has the native polynomial
bound already recorded above. There is no inference from the measure
of the finite torsion subgroup, which would be zero. The crucial
intermediate object is the open pro-p lattice and the finite index of
its sum with rational 2-torsion.

This closes the polynomial-ITERATION gate at odd primes as well.
It neither enumerates local extension fields nor computes an analytic
cover, a Neron model or the auxiliary lattice. The complete finite-BIT
local Kummer-image algorithm remains conditional on the separate
finite-precision/representation gate in the core review.
