# Compact-source lattice Helmholtz sampling: independent construction

2026-11-13. CLOSED WRITTEN classical polynomial-BIT sampler in the precise
compact-support scope below. The parent construction survives independent
review, with explicit normalization, far-field error, rounding, and finite-clock
details supplied here. No noncancellation, positive-weight, angular-sampling,
Green-oracle, or computed-normalization promise is added. This is not a claim
about arbitrary widely separated sources or a practical implementation.

Read current STATE/TRAPS, the admitted 359-line single-source proof, and the
actual Bos--Levenberg--Taylor Main Theorem and proof of 1=>2 in
`sources/new_native_wave/tangential_markov.txt`, physical lines 53--150.
No other paid report, network, API, Git, numerical test, or external theorem
verdict was used. Only this review was written.

## 1. Native statement, preprocessing, and a universal norm floor

Let L=2^n, n>=2, on Z_L^2, with

    h(p,q)=-3+2cos p+2cos q,   eta=1/L,   A=I−Delta+i eta.

Input is an explicit list of m rational complex source weights and grid sites,
promised to lie in a translate of [-D,D]^2, with numerical D and total rational
coefficient bit length B. Output is a site within TV epsilon of

    |u(x)|^2/Z,    u=A^(-1)f,    Z=||u||_2^2.

There is a bounded-clock classical algorithm with work polynomial in
n,D,m,B,1/epsilon and the explicit tolerance input length. No sampled source,
annulus, direction, algebraic maximizer, or success probability is advice.
It suffices to treat 0<epsilon<=1/4 and f nonzero after combining duplicate
sites exactly.

A supplied center is unnecessary: use the first nonzero source as center and
replace D by 2D. In the large-grid branch below, centered representatives of
the differences then lie in this enlarged box; the small-grid branch enumerates
the grid directly. All subsequent D denotes the resulting radius.

Divide the weights by the largest absolute real or imaginary coefficient.
This is an exact rational rescaling preserving the output law and gives

    1<=||f||_2^2<=2m,      W_1=sum_j|w_j|<=sqrt(m)||f||_2.

No arithmetic on the generally irrational number W_1 is required: use the
last bound whenever a numerical parameter is needed. Since |h|<=7 and
eta<=1/4,

    Z>=||f||_2^2/50.                                      (1)

This lower bound is valid even for a source polynomial vanishing identically
on the real dispersion curve.

## 2. The fixed algebraic oval and computable angular constants

Write F(p,q)=sum_j w_j exp(−i(s_j1 p+s_j2 q)). The real dispersion curve
Gamma has cos p+cos q=3/2, with both cosines >=1/2. In sine coordinates
X=sin p, Y=sin q it is exactly the real zero set of

    K(X,Y)=16(X^2−Y^2)^2+72(X^2+Y^2)−63.                   (2)

Put d=X^2−Y^2 and s=X^2+Y^2. On K=0,

    |d|<=3/4,    3/4<=s<=7/8,
    cos p=3/4−d/3,       cos q=3/4+d/3.

These identities imply cos^2 p+X^2=cos^2 q+Y^2=1 and select the positive
cosines, so the sine map is a bijection with Gamma and its inverse is smooth.
The polar equation 16 r^4 cos^2(2theta)+72r^2−63=0 has exactly one positive
root for every angle. Thus K is one compact connected smooth oval. Moreover

    K_X=16X(9+4d),   K_Y=16Y(9−4d),
    80<=||grad K||<=180.                                  (3)

For example, each multiplier lies between 96 and 192, and
sqrt(3/4)<=sqrt(s)<=sqrt(7/8), which proves the conservative (3).

Replace exp(±ip) by 3/4−d/3±iX, and similarly for q. This gives an exact
complex rational polynomial F_K of degree <=4D restricting to F on Gamma.
Its dense representation has polynomially many coefficients of bit height
poly(D,m,B); negative source exponents use the conjugate sign, not a rational
inverse. Put

    N=(Re F_K)^2+(Im F_K)^2,  deg N<=8D,
    J=K_X N_Y−K_Y N_X,
    S=max_K N,             W=max_K |J|.

Both maxima are computable in polynomial BIT time in D,m,B. Use bivariate
resultants and real-root isolation for K=0 with the tangential derivative of
the objective zero, retain the real solutions, and compare their algebraic
values. Positive-dimensional critical sets are handled by exact polynomial
division: the corresponding restricted objective is constant on the connected
oval. For W one can maximize J^2. Degrees, resultant matrix sizes, and
coefficient heights are polynomial, with only a fixed number of variables.
Root-separation bounds therefore require polynomially many bits. A positive
critical value is >=2^(−poly(D,m,B)), so obtaining constant relative accuracy
does not incur a numerical 1/S cost.

For completeness, absolute irreducibility follows from an exact ring
isomorphism. Put a=3/4−(X^2−Y^2)/3 and b=3/4+(X^2−Y^2)/3. Modulo K,
a^2+X^2=b^2+Y^2=1, so U=a+iX and V=b+iY are units with inverses
a−iX and b−iY. They obey P=−3+U+U^(-1)+V+V^(-1)=0. Conversely, in
the Laurent quotient by P, set X=(U−U^(-1))/(2i), Y=(V−V^(-1))/(2i),
a'=(U+U^(-1))/2, and b'=(V+V^(-1))/2. Then a'+b'=3/2 and
(a')^2+X^2=(b')^2+Y^2=1. Subtracting these identities recovers a'=a,
b'=b and K=0. These maps are mutual inverses, proving

    C[X,Y]/(K) is isomorphic to C[U^±1,V^±1]/(P).

The polynomial UVP=U V^2+(U^2−3U+1)V+U has discriminant
(U^2−5U+1)(U^2−U+1). Its four roots are distinct and nonzero, so this
discriminant is not a square in C(U). The quadratic is irreducible over
C(U), and its coefficients are primitive in C[U]. Gauss's lemma followed
by localization at U and V therefore makes the Laurent quotient an integral
domain. Thus K is absolutely irreducible. Real points of its smooth oval
are Zariski dense, so exact division by K detects zero restrictions.
Constant restrictions can also be treated by the same algebraic procedure.

If S=0, record U=0 and omit the angular constants. Otherwise compute rational
dyadic bounds

    S<=U<=2S,
    W<=W_up<=2W   if W>0,      W_up=0 if W=0,
    Hbar=W_up/80,       C=1+ceil(Hbar/U).                   (4)

All these are explicit polynomial-bit numbers. By (3), Hbar bounds the actual
unit tangential derivative of N from above and is at most 9/2 times its
supremum. The actual BLT Main Theorem applies to this smooth compact connected
algebraic curve and gives ||D_T N||<=M_K (deg N) S, with fixed M_K. Hence

    C<=2+36 M_K D = O(D+1).                               (5)

The source's proof of 1=>2 derives the degree-one bound using local algebraic
coordinates, Cauchy's formula, and a Lipschitz extremal function. This is the
needed assertion; no ambient Markov inequality is substituted for it.
The unknown universal M_K is NOT used in any algorithmic parameter. The
actual C in (4) is computed, while (5) proves its polynomial growth.

## 3. Discrete normalization survives arbitrary angular near-vanishing

For U>0 there is the explicit uniform comparison

    L U <= P Z,
    P=2^26(C+1)(D+1)^2(m+1).                              (6)

Here is the discrete proof, including the rounding failure case. At a maximum
point of N, S>=U/2. Along an oval arc of length 1/(64C),
N remains >=U/4, because its drop is at most Hbar/(64C)<=U/64.
At the maximum at least one of |X|,|Y| is >=sqrt(3/8)>0.6. On this short
arc that coordinate remains >1/2. Use the other frequency coordinate as
parameter: its projection speed with respect to oval arclength is >=1/2.
Indeed the inverse sine map increases lengths, and the frequency-curve unit
tangent has the required projection >=(1/2)/sqrt(s)>=1/2.
The projected frequency interval consequently has length >=1/(128C).

If L>=2048C it contains at least L/(2048C) grid coordinates. For each one,
round the other coordinate of its point on Gamma to the nearest grid value.
These grid pairs are distinct and obey

    |h|<=2pi/L,
    |F(grid)−F(curve)|<=pi D W_1/L.                        (7)

If the last quantity is <=sqrt(U)/4, each has |F(grid)|>=sqrt(U)/4.
In the exact formula

    Z=L^(−2) sum_k |F(k)|^2/(h(k)^2+L^(−2)),

each such mode contributes at least U/[16(1+4pi^2)]. This gives
LU<=2^24 C Z, within (6).

If instead pi D W_1/L>sqrt(U)/4, then

    L U <16pi^2 D^2 W_1^2/L
         <=12800 D^2 m Z,                                 (8)

using (1) and pi<4. Finally, if L<2048C, use
U<=2S<=2W_1^2 to obtain LU<=204800 C m Z. Both are covered by (6).
The two alternatives are used only in the proof; the algorithm need not
decide which holds or enumerate these grid modes.

This is the key normalization repair. No coefficient-size lower bound on
S/||f||^2, no continuum-to-grid uniformity assumption, and no transverse
noncancellation promise occurs. If S is extremely small, (8) and the elementary
norm floor pay the proposed far-field envelope instead.

## 4. A globally smooth damped-ray kernel and its translated-cluster error

Use the admitted single-source proof with K_0=2^(1,000,000) and C_g=4K_0.
Its exact residue integral and contour give a stronger damped version of its
stationary-phase remainder. The required refinements are as follows.

On that contour, Im(p_eta+theta q)>=eta/44. On a deformed positive part,
v>=1.1t and v>=eta/4 give v−theta t>=v/11; on the real and negative parts
the estimate is stronger. The central C^4 amplitude bound can retain
exp(−a eta/8), since (1+(a eta)^4)exp(−a eta/4) is bounded by a fixed
constant times exp(−a eta/8). Middle-patch integrations by parts retain
exp(−a eta/44). On the outer patch combine its fixed exponential decay with
half of this damping, retaining exp(−a eta/88) after absorbing a^(3/2).
Thus the remainder O(a^(−3/2)) gains a fixed exp(−c eta a) factor.

Let rho=|y|_2 and nu=y/rho. The strictly convex frequency oval Gamma has a
unique point k(nu) with outward unit normal nu. Its speed and curvature obey

    v(nu)=2sqrt(sin^2 p+sin^2 q) in [sqrt(3),sqrt(7/2)],
    1/2<=kappa(nu)<=2.

Define the GLOBAL real-ray kernel

    ell_eta(y)=exp(−3pi i/4) /
                 [sqrt(2pi) v(nu) sqrt(kappa(nu)) sqrt(rho)]
                *exp(i k(nu).y−eta rho/v(nu)).              (9)

Its coordinate charts agree on diagonals and axes. In the chart a>=b>=0,
theta=b/a, the single-source formula gives
kappa=H_theta/(1+theta^2)^(3/2) and rho/v=a/(2sin p_0).
This converts its leading coefficient exactly into (9). Uniqueness of the
Gauss-map inverse proves global agreement; there is no chart-switch phase.

Taylor expansion at fixed real stationary q gives

    p_eta=p_0+i eta/(2sin p_0)+O(eta^2),
    1/sin p_eta=1/sin p_0+O(eta).

Both exact and linearized exponentials have modulus <=exp(−a eta/4),
so their difference is O(a eta^2 exp(−a eta/4)) even when a eta is large.
Consequently, for eta<=10^(−6) and integer y with rho>=1,

    |g_eta(y)−ell_eta(y)|
      <=A [rho^(−3/2)+eta rho^(−1/2)+eta^2 rho^(1/2)]
                                            exp(−c eta rho),             (10)

with the explicit choices A=K_0^100 and c=2^(−14), also used below.
These deliberately excessive constants absorb the preceding single-source
derivative ledger: the new estimates use only two eta derivatives, at most
four contour derivatives, two ray derivatives, fixed curvature inverses, and
factors below 2^60 from radial sums. Each derivative/product bound is below
K_0^10, leaving ample margin within A.

To translate (9), put psi(y)=k(nu).y. Since y is normal to Gamma,
grad psi=k(nu) and ||Hess psi||<=constant/rho. Its real amplitude and damping
have derivatives bounded by a fixed constant times
(rho^(−3/2)+eta rho^(−1/2))exp(−c eta rho).
For ||s||_infinity<=D and rho>=8(D+1), Taylor's formula therefore gives
ell_eta(y−s)=ell_eta(y)exp(−i k(nu).s) with error bounded by a fixed constant
times (D+1)^2(rho^(−3/2)+eta rho^(−1/2))exp(−c eta rho).
Combining with (10), and absorbing the bounded function
(1+x+x^2)exp(−c x), gives the simpler uniform estimate

    |sum_j w_j g_eta(y−s_j)−ell_eta(y)F(k(nu))|
      <= A W_1(D+1)^2 rho^(−3/2).                          (11)

One may initially prove (10) with c=2^(−10); reducing to 2^(−14) covers
all translated line segments whose radii lie between 3rho/4 and 5rho/4.
The absorption above costs less than 2^32 for this fixed c. This is also
why neither eta*r^(−1/2) amplitude derivatives nor eta^2*r^(1/2) phase
corrections create a separate large-distance error term.
All required ray derivatives are bounded in the explicit well-conditioned
single-source formula for theta in [0,1], and extend by the global geometric
identity, so no differentiation of an absolute-value chart is assumed.

## 5. Polynomial radii and a global approximation to the full torus field

Let s_e=ceil(log_2(1/epsilon)), t_m=ceil(log_2(m+1)), and choose

    M=256(n+s_e+t_m+30),       I=(2M+1)^2,
    R=ceil(2^30 A^2 m(D+1)^4(M+1)^6/epsilon^2).             (12)

If L<=8R, use the explicit full-grid classical algorithm described below.
Otherwise R>>D, eta<10^(−6), and the following near/far construction applies.

For centered x with ||x||_infinity<=R, approximate the FULL field by summing
all m sources and all retained images of the exact infinite kernel. For
||x||_infinity>R use instead

    v_far^*(x)=sum_(||z||_infinity<=M)
                    ell_eta(x+Lz) F(k((x+Lz)/|x+Lz|)).      (13)

Every argument in (13) has radius >=R, so (11) applies to every source.
There is no far-field substitution inside the near patch.

Periodization tails are small uniformly for the whole source. Since
||x−s_j||_1<=L+2D<5L/4, the single-source strip bound gives tail per point
<=2^16 W_1 L(M+1)(31/32)^M. Its global l2 norm is at most
epsilon ||f||_2/8192 for the M in (12). This follows directly by multiplying
by L and using W_1<=sqrt(m)||f||, rather than assuming image cancellation.

For the retained-image error, Cauchy--Schwarz over I images and the injective
map (x,z)->x+Lz give

    ||error_far||_2
      <= A(2M+1)sqrt(m)(D+1)^2
                                      R^(−1/2)||f||_2.    (14)

Here the fixed radial-sum factor is absorbed in A. Explicitly, on square
shell j there are 8j points, so

    sum_(|y|_infinity>R) |y|^(−3) <=8 sum_(j>R) j^(−2)
                                            <=8/R.

There is no remaining eta/L tail term in this error. All coefficients in (11)--(14)
can be taken below the single fixed A by reserving, for example, K_0^20 for
(11) before this sum. Formula (12) makes (14) <=epsilon||f||_2/8192.

For each near-patch kernel use the single-source certified evaluator with

    delta_near=epsilon/[2^20(m+1)I(R+1)].                  (15)

Its inverse accuracy is polynomial in the native parameters. Summing the
evaluation errors over the patch has l2 norm <=3epsilon||f||_2/2^20.
This is exactly where full-kernel quadrature is used; its inverse-accuracy
clock is NEVER applied at accuracy proportional to 1/L over the full grid.

For each far point evaluate the elementary expression (13) to rational
absolute error <=epsilon/(2^20 L). This costs only O(n+B+log(D+1)+log(m+1)
+log(M+1)+log(1/epsilon)) bits plus fixed constants. The stationary point is
given by the explicit square-root/atan formula from the single-source proof;
the large phases need O(n+log M) guard bits. F can be evaluated as its native
m-term trigonometric sum, avoiding coefficient cancellation in its dense
polynomial representation. Each of I terms is assigned its share of the
absolute error. All operations here are elementary-function evaluation, not
the inverse-accuracy kernel quadrature. Total l2 rounding error is
<=epsilon/2^20<=epsilon||f||_2/2^20.

Let v be this deterministic rational-valued piecewise approximation. Combining
these estimates, conservatively,

    ||v−u||_2 <=epsilon||f||_2/2048.

By (1), its normalized Born law has TV <=epsilon/8 from the true law and
||v||_2^2>=Z/4. If U=0, set v_far=0 exactly; (11)--(14) still pay its omitted
mass. No division by U or assumption of radiating source strength is needed.

## 6. A discrete proposal with a computable rejection clock

Let P_near be the (2R+1)^2 near sites and q_near their uniform law. On the
full centered torus take the same radial-plus-uniform law as in the m=1 proof:

    q_far(x)=1/[2(L/2+1)N_r]+1/(2L^2),
    N_0=1, N_r=8r (0<r<L/2), N_(L/2)=2L−1.

It obeys q_far>=1/[16L(1+r)] and q_far>=1/(2L^2), and is sampled using
uniform radii and explicitly ranked square shells. There is no angular sampler.

The near evaluator and its error satisfy

    |v_near(x)|^2 <=(C_g+1)^2 m||f||_2^2 I^2.

Thus choose the exact rational envelope mass

    H_near=(2R+1)^2(C_g+1)^2 m||f||_2^2 I^2.

The ray amplitude in (9), (13), and the image-shell sum in the m=1 proof give
|v_far^*(x)|<=A sqrt(U)[(1+r)^(-1/2)+12M^(3/2)/sqrt(L)]. Put
C_E=288(A+1)^2 and, for U>0, choose

    H_far=36 C_E M^3 L U+1.                               (16)

Then H_far q_far dominates |v_far|^2, including its absolute rounding error.
Indeed square the two summands with factor 2, use the two lower bounds on
q_far, and absorb 2(epsilon/(2^20 L))^2 in its uniform floor. If U=0, set
H_far=0 instead and use only the near proposal.

Use H=H_near+H_far and the explicit mixture

    q=(H_near q_near+H_far q_far)/H.

Since v uses the near value only on the patch and the far value outside it,
Hq dominates |v|^2 everywhere. The extra support overlap causes no error.
All masses are rational polynomial-bit quantities. Using (1) and (6),

    H/Z <= Lambda,
    Lambda=50(2R+1)^2(C_g+1)^2 m I^2
                         +36 C_E M^3 P+50.                (17)

When U=0 the far terms may simply be omitted. Thus rational rejection with
acceptance |v(x)|^2/[Hq(x)] succeeds with probability at least 1/(4Lambda).
The normalization Z is never evaluated.

Cap trials at ceil(4Lambda(s_e+4)). Sample the top rational mixture and the
uniform integer choices with exact integer comparisons, capping each binary
rejection after ceil(log_2(256T/epsilon)) attempts. There are at most three
such calls per trial, each with success probability at least 1/2
per attempt. Round the final acceptance probability down to b bits with
2^(−b)<=epsilon/(64T). Coupling bounds the cap and rounding errors by less
than epsilon/4. Return a fixed site on a cap failure. Together with the field
approximation, the full spatial law is within epsilon.

Every displayed cap is actually computable. Formula (5) shows C=O(D+1), so
(12), (15), (17), the number of images, and all inverse quadrature accuracies
are polynomial in n,D,m,B,1/epsilon. Algebraic maxima and rational arithmetic
have polynomial bit length, including nearly vanishing S. The finite constants
are enormous and charged, not inferred from numerical experiments.

In the branch L<=8R, directly compute all L^2 Fourier coefficients and all
spatial amplitudes to pointwise absolute accuracy epsilon/(2^12 L). Even
naive DFTs use only polynomially many operations because L<=8R. Denominators
are bounded below by 1/L. For example, elementary arithmetic tolerance
epsilon/[2^30(m+1)(L+1)^4], with exact summation or correspondingly budgeted
rounding, suffices: inversion amplifies symbol error by at most L^2.
This gives l2 error <=epsilon/2^12, so (1) pays normalization. Sample the
explicit rational probability table using a binary CDF grid with
ceil(log_2(64L^2/epsilon)) random bits. This is a genuine
polynomial branch in the stated parameters, not an exponential-in-n fallback
left outside the clock.

## Disposition and scope

The full compact-source spatial endpoint is classically matched in
poly(n,D,m,B,1/epsilon), including arbitrary signed/complex weights and exact
or approximate cancellation on Gamma. The decisive operations are algebraic
maximization on the fixed oval, the two-case discrete normalization bound,
and using full kernel evaluation only in a polynomial near patch. A continuous
angular sampler is unnecessary. Dependence on D is NUMERICAL: this proves no
poly(log D) algorithm for an arbitrary widely separated sparse source list.
No result from the independent live compact-source report was read or assumed.
