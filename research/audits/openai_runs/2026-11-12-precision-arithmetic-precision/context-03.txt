# Canonical torsion-divisor support heights

2026-11-12. Parent derivation independently checked in
audits/reviews/2026-11-12-torsion-height-{finite,analytic}-chain.md; both full
reviews were parent-read. The completed OpenAI contraction report independently
obtained the graph bound. This proves the scoped support-VALUE height theorem
below, not a closed encoding or native surface algorithm. The direct broad
paid book-height request was empty. Retain the book signs and minimality guard.

## Input and proved bound

Let pi:C->P1 be a degree-d cover over Qbar, smooth connected C of genus
g>=1, with fixed total branch orbit <=r and logarithmic branch height hB.
Let T be N degree-zero torsion classes. Choose b over a SMALL NONZERO
INTEGER a outside branch/exceptional values such that every D_t in |t+gb|
is unique and avoids the poles of pi. All divisors are closed; field
extensions below are existential for normalized height bounds, not a
common splitting-field algorithm. Set S_N=d+1+hB+log(N+1). If A additional
geometric points must be avoided, replace log(N+1) by log(N(A+1)+1).

The lemmas below establish:

    sum_(Q with multiplicity in D_t) h(pi(Q)) <= C_r*d^9*S_N.

The exponent is deliberately loose. A supplied plane-model coordinate y
can then be charged using its equation F(pi,y)=0 and its coefficient
height H: h(y(Q))<=poly(deg F)*(H+h(pi(Q))+1), away from the finitely many
places requiring a different affine/normalization chart. Avoiding those
places is a separate finite bad-basepoint condition. A full closed-divisor
encoding still needs a precise primitive-coordinate/jet reconstruction
argument; a polynomial for pi-values alone can lose branch labels.

## Finite model-transfer lemma

Let Z be the regular semistable cover-compatible model from the reviewed
Javanpeykar construction, with pi a MORPHISM to P1 over the integers.
Let f:Z->Y contract to the relatively minimal regular semistable model.
Work after finite extension so horizontal supports and components split.
Every contraction is a rational (-1) tail, inverse to blowing up a smooth
point; blowing up a node would introduce a multiplicity-two component.

For a section b define L_s(b) as the number of smooth blowup centres traversed
by its successive images. Each contributes one. Then

    sum_s L_s(b) log Norm(s) / [K:Q]
       = h_Z(b)-h_Y(b) <= h_Z(b),

by omega_Z=f^*omega_Y+exceptional contributions, identical archimedean
metrics, and nonnegativity of stable Arakelov point height. For every
distinct section P,

    I_Y,s(b,P) <= I_Z,s(b,P)+L_s(b).

Each smooth-point blowup changes the intersection of two sections by one
exactly when both pass through the centre. Consequently, for the degree-d
horizontal zero/pole divisors Z0,Pinf of pi,

    I_Y,s(b,Pinf) <= d L_s(b),
    I_Y,s(b,Z0) <= v_s(a)+d L_s(b).

The first uses that integral a and infinity sections are disjoint on the
base and pi is a morphism on Z. The second uses restriction of div(pi)
near b on Z: it is effective there, so its horizontal zero intersection
is <=v_s(a). This explicitly charges collisions with zero at primes |a.

## Vertical-pole bound on the minimal model

Write div_Y(pi)=Z0-Pinf+sum_C v_C C in a fibre at s. The dual graph is
connected, with unit edges and delta_s geometric nodes; loops are harmless.
Intersecting a principal divisor with components makes v solve the graph
Laplacian equation with current vector from Z0-Pinf. Its total positive
current is <=d. Therefore

    max_C v_C-min_C v_C <= d delta_s.

Proof: choose a threshold between the endpoint values of any
edge. All crossing currents have the same sign, so that edge's voltage
drop is at most the total positive source d. Connect extrema by a path
with <=delta_s edges. No inverse spectral-gap estimate is used.

A section meets a smooth point of a regular semistable fibre. Restriction
of div(pi) to b gives

    v_Cb = v_s(a)-I_Y,s(b,Z0)+I_Y,s(b,Pinf) >= -d L_s(b).

Hence m_s(pi)=max(0,-min_C v_C) <=d(L_s(b)+delta_s), and

    V_pi := sum_s m_s(pi)log Norm(s)/[K:Q]
        <= d[h_Z(b)+Delta_st(C)].

Equivalently use u=pi-(a-1), so u(b)=1. Its zeros and b are disjoint on Z,
its poles and negative vertical valuations agree with pi, and the same
graph proof gives the bound without a v_s(a) term. This pays the vertical
term using stable discriminant, without bounding the nonminimal node count.
Z must be the SPECIFIC source normalization-resolution: its finite
div(d pi) identity bounds h_Z(b), not merely h_Y(b). An arbitrary further
blowup is not free. Splitting fields here prove heights only; node subdivision
under base change preserves normalized Delta and crepant canonical heights.

## Removal of book9.1.3's support-etale assumption

On a regular semistable model and a section Q outside the generic zero and
pole supports, restriction of the principal divisor gives

    max(0,-v_s(pi(Q))) <= I_s(Q,Pinf)+m_s(pi).

When pi(Q)=0, its finite coordinate-height contribution is zero and the
inequality holds directly; do not restrict the zero principal function.
Thus collisions between horizontal zero and pole sections do not by
themselves obstruct the finite inequality. At an archimedean place let
G=gr with log-distance singularity, and put

    u(Q)=0.5 log(1+|pi(Q)|²)+G(Pinf,Q),
    H_pi=0.5 integral_C log(1+|pi|²) mu.

The Green representation for dd^c u=pi^*FS-d mu is

    u(Q)=integral_C G(Q,R) pi^*FS(R)+H_pi.

It gives u(Q)<=d sup G+H_pi. Summing the local inequalities is precisely
the book coordinate-height inequality, without demanding disjoint
horizontal supports. The actual source's final identity has this plus sign;
its opposite Laplacian convention does not change the final formula.

## Archimedean moment bound

Use the SAME b above a. The established global lower bound is

    G(b,R)>=log dist_ch(a,pi(R))-log(Cd)-Lambda',

away from equal base images, which form a measure-zero set. Since pi has
degree d and FS has total mass one,

    integral_C log dist_ch(a,pi(R)) pi^*FS(R)=-d/2.

Evaluate the Green identity at b, and use G(Pinf,b)<=d sup G:

    H_pi <= d sup G+0.5 log(1+a²)
              +d[log(Cd)+Lambda'+1/2].

All embedding averages are polynomial in d,hB,log(N+1) by the existing
Merkl bound and the small integer choice of a. No charts need to be
constructed algorithmically for this height inequality.

## Assembly with actual book9.2.5

On Y take D=g b. Arakelov adjunction gives b²=-h_Y(b)[K:Q], hence
-(D,D-omega)/2 = g(g+1)h_Y(b)[K:Q]/2. Dropping the nonnegative
log-cardinality term, the source bounds each (D_t,P) by this term plus
2g² Delta_st, the theta-supremum sum, g log(2pi)/2, half the Faltings
height, and (g b,P). For P over infinity the finite cross-intersection
is <=h_Z(b), and the established global Green lower bound pays its
archimedean part by Lambda'+log(Cd)+0.5 log(1+a²).

Sum this over Pinf with multiplicities (total degree d). Then sum the
coordinate-height inequality over the degree-g divisor D_t itself:

    sum_Q h(pi(Q)) <= (D_t,Pinf)/[K:Q]
                      +g[d sup G_bar+H_pi_bar+V_pi].

Known bounds h_Z(b)<=C_r d³ S_N, Delta_st<=C_r d^6(d+1+hB),
Theta_av<=C_r[d³+d log(d+1+hB)], h_Fal<=C_r d^5(d+1+hB) give the
d^9 S_N envelope. This is not yet a certified reconstruction
algorithm and does not address native frame/good-model constructions.

## Finite support avoidance

For any specified forbidden point P and any class t, D_t contains P iff
H0(K_C tensor t^-1 tensor O(P)) has a section vanishing to order >=g at b.
That space has dimension g and degree 2g-1. Its ordinary Wronskian is
nonzero in characteristic zero (or characteristic>2g-1) and has degree
g(2g-1)+g(g-1)²=g³. Thus at most Ng³ times the number of forbidden
geometric points must be added to the common-basepoint bad set. This
pays avoidance of poles and plane-chart exceptions with small log-height
base values; it must not be invoked in unrestricted characteristic.

The combined bad-basepoint count is at most Ng³(1+d+A), plus r branch
values. Choosing an integer a<=r+Ng³(1+d+A)+1 outside their images ensures
EVERY b above a works; its logarithmic height has the advertised bound.

Status: transfer, graph, moment, assembly and avoidance claims are independently
checked and parent-accepted in the stated scope. Existing input theorems and their
precise sources are in SURFACE_UNIFORM_ARITHMETIC_HEIGHT.md and reviews
surface-theta-delta, merkl-log-atlas, surface-faltings-transfer and book-height-
minimality. Closed divisor encoding, faithful input presentation, and rational
reconstruction remain separate interfaces. No full comparator, speedup or
hardness is inferred.

## Closed-coordinate bridge, independently checked

The full review audits/reviews/2026-11-12-closed-divisor-encoding.md was
parent-read. Let F(x,y)=0 be an absolutely irreducible plane model, x=pi,
total degree D and projective coefficient height H_F, and avoid its at most
D² geometric normalization points outside the affine nonsingular locus.
For E=D_t of degree g put H=sum multiplicity*(h(x)+h(y)). Root heights give

    H <= (D+1) sum multiplicity*h(pi Q)+g[H_F+O(log(D+2))].

For N such divisors one integer 0<=c<=Ng(g+1)/2 makes z=x+c y separate
each support and be a local parameter there. The latter requires
eta=F_y-cF_x nonzero, including at repeated support. There are unique
A monic of degree g and B,C of degree<g with

    K[E]=K[z]/A,    x=B(z), y=C(z),
    h([1,coeff A,coeff B,coeff C])
       <= C_0{DgH+g²[H_F+log max(1,|c|)+log(gD+2)]}.

This encodes the entire nonreduced divisor, not just pi-values. The exact
jet recurrence D_z^n f=P_n/eta^(2n-1), deg P_n<=2nD, and linear-in-n
coefficient height pay inverse tangents. Confluent Vandermonde determinants
pay separation denominators with no collective splitting-field cost.
From a CLOSED divisor algebra construct A by the multiplication matrix of
z, test eta invertibility and cyclicity of 1,z,...,z^(g-1), then solve for
B,C. No support factoring is required.

To turn intrinsic heights into coordinate bits over K, charge BOTH its
degree e and its presentation height B_K. Trace-dual basis bounds give
bit length poly(e,B_K,D,g,H_F,H,log(c+1)). A supplied low-degree field in
an arbitrarily high-height basis is not a paid input. This proves polynomial
intrinsic encoding heights once the plane-model size is paid. It does not
supply the global torsion field, canonical divisor, compatible numerical
lift or Galois-invariant rational reconstruction. Those remain separate.
