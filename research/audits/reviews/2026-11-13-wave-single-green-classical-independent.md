# Single-source lattice Green sampling: independent classical proof

2026-11-13. CLOSED WRITTEN in the scope below. Independently checked the
completed 624-line report `openai_runs/2026-11-13-wave-single-green/response.md`
in full, especially its equations (12)--(20). Its analytic mechanism is sound.
This note supplies explicit constants and patch boundaries where the report
only says that constants are effective. No Green oracle, unchecked numerical
constant, continuum approximation, paid-report verdict, or finite experiment
is used. No implementation, practicality, novelty, hardness, or multisource
classical match is claimed.

Read current STATE.md and TRAPS.md. Only this review was written. No network,
Git, paid API, other live report, or numerical sweep was used. The contextual
Martin source is not imported as a theorem.

## 1. Native theorem and a normalization that need not be evaluated

Let L=2^n, n>=2, eta=1/L, and

    h(p,q)=-3+2 cos p+2 cos q,
    G_L(x)=L^(-2) sum_k exp(2 pi i k.x/L)/(h(2 pi k/L)+i/L).

There is a classical bounded-clock algorithm sampling
P_L(x)=|G_L(x)|^2/Z_L within TV epsilon, in polynomial BIT work in
n, 1/epsilon, and the explicit tolerance input length. It outputs the full
2n-bit spatial site. A translated source is handled by translating the output;
a nonzero scalar source coefficient cancels on normalization.

It suffices to treat 0<epsilon<=1/4. Parseval gives

    Z_L=L^(-2) sum_k 1/(h(k)^2+L^(-2)),
    L/512 <= Z_L <=64L.                                    (1)

For the lower bound, take at least L/12 first-coordinate grid angles in
[0,pi/6], and round arccos(3/2-cos p) to the nearest second-coordinate
angle. Then |h|<=2pi/L and each mode contributes at least
1/(1+4pi^2). For the upper bound, if |h|<=s<=1/8, one sine magnitude
is >=1/2. The two monotone arcs in that coordinate give

    #{k:|h(k)|<=s} <=4L(Ls+1).

The strip |h|<=1/L contributes <=8L. Successive dyadic shells whose upper
endpoint is <=1/8 contribute <=12L*2^(-j). The remainder is at |h|>1/16
and contributes <=256. Thus for L>=16 the bound is <=32L+256<=48L;
for smaller L, Z_L<=L^2. This proves the conservative (1). The sampler
never computes Z_L.

## 2. Exact infinite kernel and controlled periodization

Define

    g_eta(y)=(2pi)^(-2) integral_[−pi,pi]^2
                       exp(i(p y_1+q y_2))/(h(p,q)+i eta) dp dq.

For 0<eta<=1/4 shift each contour by
i(eta/16)sgn(y_j). Throughout the deformation,
|Im h|<=4 sinh(eta/16)<=eta/2. Hence

    |g_eta(y)| <=(2/eta) exp(−eta ||y||_1/16).                (2)

This implies absolute summability. Fourier inversion on the finite grid
therefore gives the EXACT identity

    G_L(x)=sum_(z in Z^2) g_(1/L)(x+Lz).                    (3)

For centered x and images ||z||_infinity>M, (2), the 8s points in image
shell s, and ||x+Lz||_1>=L(s−1) give

    |tail| <=16L exp(1/16) sum_(s>M) s exp(−s/16)
           <=2^15 L(M+1)(31/32)^M.                         (4)

The last inequality follows directly from the geometric-series derivative;
exp(−1/16)<=16/17 and exp(1/16)<2 suffice with room to spare.
Put s_e=ceil(log_2(1/epsilon)) and M=128(n+s_e+20). Then (4) is at most
epsilon/(2^14 L). For example, use (31/32)^M<=exp(−M/32)
<=2^(−5(n+s_e+20)); the remaining linear M+1 is absorbed by the displayed
constant. Only O(M^2) infinite-kernel evaluations are required at a proposed
site. The values of y have O(n+log(M+1)) bits.

## 3. Residue formula, branch, and a genuinely nonsingular contour

Reflections and interchange reduce y to (a,b), 0<=b<=a. Define

    c_eta(q)=3/2−cos q−i eta/2,
    p_eta(q)=arccos c_eta(q),  Im p_eta>0.

On the real q contour, the root exp(i p_eta) is the root inside the unit
circle of z^2−2 c_eta z+1. Taking its residue gives, including the sign,

    g_eta(a,b)=−i/(4pi) integral_[−pi,pi]
                     exp(i a p_eta(q)+i bq)/sin p_eta(q) dq. (5)

Fix tau=10^(−6). Define the clamped polynomial Q on [0,1] by

    Q(t)=218790 integral_0^t u^8(1−u)^8 du,

and extend it by 0 and 1 on the respective sides. It is C^8, increasing,
Q(1/2)=1/2, and max Q'<17/5. Set

    rho(s)=Q(10(|s|−4/5)),
    q(s)=s−i tau rho(s) sin s.                              (6)

For s>=0 write t=tau rho(s)sin s>=0. Along the entire homotopy,
Im c_eta(s−it)=−sin s sinh t−eta/2<0. The same inequality holds for
negative s because both sine and t change sign. The branch is never crossed,
and periodic endpoint pieces cancel. Formula (5) can therefore be integrated
along (6).

Here are explicit global bounds; they also check the delicate turning points:

    |sin p_eta(q(s))| >=1/2000,
    Im[p_eta(q(s))+theta q(s)] >=0,  0<=theta<=1.             (7)

For the first, Re c>=1/2−tau^2. If |Re c−1|>=1/16, use
|sin p|^2=|1−c||1+c|. Otherwise Re c is in [15/16,17/16], so
cos s<=9/16, |s|>9/10, rho=1, and sin^2 s>=175/256. Thus
|Im c|>=tau sin^2 s and
|sin p|^2>= (31/16)(175/256)tau>1/2000^2.

For the second, write p=u+iv. On 4/5<=s<=pi/2, if v<=1.1t,
the real dispersion equation

    cos u cosh v=3/2−cos s cosh t

implies sin u<0.601, whereas the imaginary equation

    sin u sinh v=sin s sinh t+eta/2

has right side >0.71 sinh t and left side <0.662 sinh t. This is impossible;
the case t=0 follows directly from eta>0. The elementary numerical margins
follow, for instance, from alternating Taylor bounds for sin(4/5), cos(4/5),
and sinh on [0,1.1*10^(−6)]. For s>=pi/2, v>=arcosh(3/2)>1/2>1.1t.
For negative s the term theta Im q is nonnegative instead. Where rho=0,
Im p>0 directly. This proves (7).

Useful stronger bounds, with explicit patch boundaries, are

    Im[p_eta(q(s))+theta q(s)] >=2^(−26),  |s|>=17/20;       (8)
    |sin p_eta(q)| >=2/5,
           |Re q|<=9/10, |Im q|<=tau, eta<=10^(−6).         (9)

For (8), on [17/20,pi/2], rho>=1/2 and sin s>7/10, so
v−theta t>=t/10>=0.035 tau>2^(−26). The other regions use the preceding
symmetry and v>1/2 argument. For (9), cos(9/10)>0.62 gives |c|<0.9;
then |sin p|^2=|1−c^2|>=1−|c|^2>0.19.

## 4. Uniform stationary phase, including a*eta arbitrarily large

For eta<=10^(−6) set p_0(s)=arccos(3/2−cos s) on |s|<=9/10 and
theta=b/a when a>0. The phase phi_theta=p_0+theta s has its unique
stationary point q_theta in [0,arccos(3/4)] strictly inside [−3/4,3/4].
There is no endpoint saddle at theta=0 or 1. Implicit differentiation gives

    p_0'=−sin s/sin p_0,
    p_0''=−(cos s+cos p_0*(p_0')^2)/sin p_0.

On |s|<=4/5, 1/2<=−p_0''<=10. Write H_theta=−p_0''(q_theta).
The exact well-conditioned stationary-point formulas are

    t=theta^2,
    Y=cos q_theta=(2+(5/2)t)/(3t+sqrt(4+t+4t^2)),
    q_theta=atan(theta*sqrt(1−(3/2−Y)^2)/Y).                 (10)

They follow by rationalizing the appropriate root of
(1−t)Y^2+3tY−1−(5/4)t=0. They include t=0 and t=1 without division
by 1−t or a small inverse-trigonometric derivative.

Use the explicit cutoffs

    chi_c(s)=1−Q(20(|s|−3/4)),
    chi_o(s)=Q(20(|s|−17/20)).

Their central, middle, and outer partition is
chi_c, (1−chi_c)(1−chi_o), chi_o; chi_c*chi_o=0. The central contour is
real. There the amplitude against exp(i a phi_theta) is

    A_(a,eta)(s)=chi_c(s)/sin p_eta(s)
                         *exp(i a[p_eta(s)−p_0(s)]).

The imaginary dispersion equation gives Im p_eta(s)>=eta/4. For j<=4,
|partial_s^j(p_eta−p_0)|<=C_j eta, with fixed bounds justified below.
Consequently the C^4 amplitude norm is bounded by a fixed constant times

    exp(−a eta/4)*(1+(a eta)^4).

This is uniformly bounded for ALL a eta, not only for a eta small.
That observation is essential; there is no unpaid derivative blow-up.

The uniform Morse coordinate

    t_s=sgn(s−q_theta)*sqrt(2[phi_theta(q_theta)−phi_theta(s)])

has derivative in [1/8,16], and carries the compact support into [−8,8].
For the resulting C^4 amplitude H(t_s), Fourier inversion of the Gaussian
gives a leading term at t_s=0 and an error bounded by

    constant*a^(−3/2) integral_R xi^2 |H_hat(xi)| dxi.

The integral is bounded by the L1 norms of H and H''''. A Gaussian regulator
justifies the oscillatory Fourier interchange. Thus the central remainder is
uniform. Its leading term is

    ell_eta(a,b)=−i/(4pi)*sqrt(2pi/(a H_theta))
       *exp(i a p_eta(q_theta)+i b q_theta−i pi/4)
        /sin p_eta(q_theta).                              (11)

The middle patch is supported on 3/4<=|s|<=9/10. Its COMPLEX phase
Phi=p_eta(q(s))+theta q(s) satisfies |Phi'|>=1/64. Here is a quantitative
check: on the positive real interval |p_0'|>=1+1/40, since
|p_0'|^2−1=(9/4−3 cos s)/sin^2 p_0 and cos(3/4)<0.732.
On the negative interval the sign is instead helpful. On the small complex
rectangle in (9), |partial_q p_eta'|<=20, |partial_eta p_eta'|<=8,
and |p_eta'|<3. Also |q'−1|<=35 tau. The perturbation of p_0'+theta
is therefore less than 1/5000. Two integrations by parts have zero boundary
terms and give O(a^(−2)), with |exp(i a Phi)|<=1 by (7).
The outer patch is O(exp(−2^(−26)a)) by (8). This covers the whole contour.

It follows that |g_eta(a,b)−ell_eta(a,b)|<=K a^(−3/2), with the explicit
universal K specified next. For eta>=10^(−6), (2) alone gives
|g_eta(a,b)|<=2*10^6 exp(−a/(16*10^6))<=2^64 a^(−3/2).
One may use zero instead of (11) in that parameter range.

## 5. Explicit analytic constants and a finite-bit evaluator

Take, deliberately very conservatively,

    K=2^(1,000,000),             C_g=4K.                    (12)

These are proved upper bounds, not constants to be estimated experimentally.
The following elementary derivative ledger substantiates (12):

* The displayed degree-17 polynomial cutoffs, on transitions of width at
  least 1/20, have derivatives through order 8 bounded by 2^100. This follows
  by differentiating their coefficients: their coefficient L1 norm is <2^26,
  17^8<2^33, and 20^8<2^35.
* On the contour, |c|<3 and (7) holds. Local complex polydiscs of radius
  2^(−40) in q and eta keep |1−c^2|>=2^(−23). The local analytic branch
  has |p|<8 and |csc p|<2^14. These follow from the quadratic roots, their
  product 1, and the variation bound |Delta c|<=3*2^(−40). Cauchy's formula
  then bounds every mixed derivative of p and csc p through total order 12
  by 2^1000, also at eta=0 on the central patch. Analytic continuation on
  each local disc is meant; no principal-branch cut is crossed computationally.
* The central C^4 amplitude is bounded by 2^10000: differentiate the
  exponential at most four times and use x^j exp(−x/4)<=16^4 for j<=4.
* Write t_s=(s−q_theta)*sqrt(kappa(s)), with
  kappa=2 integral_0^1 (1−u)(−p_0''(q_theta+u(s−q_theta)))du.
  Then 1/2<=kappa<=10. Its derivative bounds and elementary differentiation
  bound the first six derivatives of t_s by 2^10000. The first five inverse
  derivatives are bounded by 2^100000: inverse differentiation has at most
  eight such factors and powers of 1/t_s'<=8. Thus the transformed amplitude
  and its first four derivatives are bounded by 2^600000.
* Its support lies in [−8,8], so integral xi^2|H_hat(xi)| is at most
  2^6 times that last bound, by splitting |xi|<=1 and integrating by parts
  four times for |xi|>1. The Gaussian remainder constant is <2^600010.
  Middle-patch differentiation through the two integrations by parts is
  bounded by 2^100000 using |Phi'|>=1/64 and the preceding derivative bounds.
  The outer contribution has a^(3/2) times its absolute value <2^64.

All the normalized integrals and their sum are therefore bounded by K.
The leading term has magnitude <=1/sqrt(a), so, including a=0 from the
bounded contour integral,

    |g_eta(y)| <= C_g/sqrt(1+||y||_infinity).                (13)

Given rational 0<delta<=1, compute a rational complex g_tilde with

    |g_tilde−g_eta(y)| <=delta/sqrt(1+a)                    (14)

as follows. If a>=8K/delta, evaluate (11), or use zero in the large-eta
range; the remainder uses less than half of (14). Otherwise integrate the
exact deformed (5) by composite quadrature with
N=ceil(8K(1+a)^2/delta) nodes. The integrand derivative is at most K(1+a),
so its quadrature error uses less than half of (14). N=O(delta^(−3)), with
the fixed K-dependent constant explicitly charged.

Use rational dyadic arithmetic for each returned value and reserve the other
half of (14) for node/elementary-function rounding. Equation (7) prevents a
hidden small denominator. One explicit stable formula is

    w=sqrt(1−c^2) in the first quadrant,
    z=c+i w,              p=−i Log z.

Here c has positive real and negative imaginary part, the selected z is in
the first quadrant and inside the unit circle, and |z|>=1/9. Resolving its
small imaginary part costs O(n) extra bits, not O(L) work. Square root,
logarithm, trigonometric functions, and atan on the displayed domains admit
Taylor/Newton evaluation in polynomial bit work. Large negative real
exponents are clipped only below the allocated absolute error. Large real
phases are evaluated with O(log(2+a)) guard bits before periodic reduction.
Continuous piecewise-polynomial cutoffs can be evaluated at approximate
arguments using their global derivative bound, so comparisons near their
breakpoints introduce no exact-real decision oracle.

The bit precision is O(n+log(2+a)+log(1/delta)) plus fixed constants from
(12). Thus (14) costs poly(n,log(2+a),1/delta), uniformly in a and eta=1/L.
The enormous explicit constants are not a claim of a practical algorithm.

## 6. Spatial envelope, normalization, and bounded-clock sampling

For centered x let r=||x||_infinity. The 8j image points at ||z||_infinity=j
have ||x+Lz||_infinity>=Lj/2. Consequently

    sum_(||z||<=M) (1+||x+Lz||_infinity)^(−1/2)
      <=S_M(x)=(1+r)^(-1/2)+12 M^(3/2)/sqrt(L),
    ||S_M||_2 <=18 M^(3/2) sqrt(L).                        (15)

Use delta=epsilon/[2^14(M+1)^2] in (14) and define v(x) as the rational sum
of the retained image approximations. Equations (4), (14), and (15) give

    ||v−G_L||_2 <=19 epsilon sqrt(L)/2^14.

The normalized Born laws have TV at most 2||v−G_L||_2/||G_L||_2, hence
TV(P_v,P_L)<=epsilon/8 by (1). Also ||v||_2>=||G_L||_2/2. This is a
global additive approximation, including interference zeros; no relative
pointwise Green precision is assumed.

Put R=L/2. The square-shell sizes are N_0=1, N_r=8r for 0<r<R, and
N_R=2L−1. Use the explicitly samplable rational law

    Q(x)=1/[2(R+1)N_r]+1/(2L^2).

It is a fair mixture of a uniform-radius/uniform-square-shell draw and a
uniform torus point. Its two lower bounds are
Q(x)>=1/[16L(1+r)] and Q(x)>=1/(2L^2). Set

    C_E=288(C_g+1)^2,  C_H=18 C_E,  H=C_H L M^3.

Then |v(x)|^2<=C_E[(1+r)^(-1)+M^3/L]<=H Q(x). Rejection with rational
acceptance probability |v(x)|^2/[H Q(x)] has accepted law exactly P_v and
success probability at least 1/(2048 C_H M^3).

Cap the attempts at T=ceil(2048 C_H M^3(s_e+4)); failure is <=epsilon/16.
Uniform integer draws use binary rejection with success >=1/2 and an explicit
per-draw cap ceil(log_2(64T/epsilon)) plus a fixed allowance for the constant
number of draws per trial. Use b-bit acceptance probabilities with
2^(−b)<=epsilon/(64T), obtained by exact integer division. Coupling over all
trials charges at most T*2^(−b); cap failures and proposal failures add another
<=epsilon/8. Output a fixed site on failure. Combined with the field error,
the final spatial law is within epsilon of P_L.

Every trial uses O(M^2) kernels. With the stated quadrature clock its total
work is bounded by O(M^11 epsilon^(−3)(s_e+1) poly(n+s_e)) times explicit
fixed constants. Rational outputs and sums have polynomial bit length; one
may use common dyadic denominators. All random and arithmetic loops have
finite prescribed caps, and the computation can stream images and nodes.

## Disposition

The report's single-source classical polynomial-BIT claim survives adversarial
review. Its missing explicit analytic constants and patch partition are paid
above; no material formula needs replacement. In particular, growing a*eta,
theta=0 or 1, near-turning points, periodization, small spatial amplitudes,
and normalization are all covered. The conclusion is ONLY m=1 (and translated
or rescaled single sources). Arbitrary-source coherent interference remains
a separate problem; neither this proof nor the report supplies its success
probability or its classical sampling clock.
