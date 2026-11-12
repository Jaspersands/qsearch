# Condensate pump coefficients and a uniform finite-time comparison

Date: 2026-11-13. Independent mathematical review; no sweep, implementation,
network, API, Git, or mutable paid-report input. Native source contract:
`audits/api_inputs/2026-11-13-macdonald-dynamics/contract.md`; proposed target:
`audits/api_inputs/2026-11-13-condensate-projector/condensate-gaussian-clock.md`.

**Disposition.** The proposed exact coefficients and constants are correct.
The initial-generator estimate can be strengthened to a uniform column bound,
and the parent's normal-ordered contour argument then proves an explicit
finite-time Poisson approximation. This is a restricted classical baseline:
its error is polynomially small in D in the window stated below. It does not
solve arbitrary-precision or arbitrary-binary-time condensate sampling.

## 1. Exact native normalization and coefficients

Throughout, N=D+1, t=D/N, q=t^3, and

    r_k=(1-q^k)/(1-t^k)=1+t^k+t^(2k),
    v=q^(-1)-1,  sigma=(1-t)v=v/N.

The normalized occupation vector is p_mu/sqrt(R_mu), with
R_mu=z_mu product r_k^(m_k). Thus p_k=sqrt(k r_k) a_k^dagger.
The contract's Hamiltonian, with these same global parameters at every degree,
is

    H=N sum_(n=1)^D q^(-n) V_n V_n^*,
    sum V_n z^n=exp(sum_(k>=1) (1-t^k)p_k z^k/k).

Let Omega_D=|D,0,0,...>. The adjoint translates p_k by
(1-q^k)z^k, so exactly

    V_n^* p_1^D=binom(D,n)(1-q)^n p_1^(D-n),
    H p_1^D=N sum_(n=1)^D binom(D,n)v^n V_n p_1^(D-n).       (1)

For an output with m_k particles in modes k>=2, put M=sum k m_k and
m_1=D-M. For M>=2 define the finite polynomial

    L_(D,M)=sum_(l=0)^(D-M) binom(D,M+l) sigma^l/l!.

This is L_(D-M)^(M)(-sigma) in the conventional associated-Laguerre notation,
but its displayed definition is all that is needed. The normalized matrix
coefficient following from (1) is exactly

    <m|H|Omega_D>
      = N v^M L_(D,M) product_(k>=2) [(1-t^k)^m_k/(k^m_k m_k!)]
        * sqrt(product_(k>=2) [k^m_k m_k! r_k^m_k]
               /[(D)_M r_1^M]).                              (2)

All these coefficients are nonnegative. The diagonal and one-mode-2
coefficient are therefore

    h_D=<Omega_D|H|Omega_D>
       =N[sum_(l=0)^D binom(D,l) sigma^l/l! -1],             (3)

    A_D=<D-2,1|H|Omega_D>
       =(1+t)v^2 L_(D,2)/2
          *sqrt(2r_2/[D(D-1)r_1^2]).                        (4)

There is no extra factor of 2 in H. The sign of the limiting coherent
amplitude is negative imaginary for the contract's exp(-i T H).

## 2. Explicit initial-column bounds

For D>=2 the following elementary bounds suffice:

    v=3/D+3/D^2+1/D^3 <=5/D,
    sigma=3/D^2+1/[D^3(D+1)] <=4/D^2,
    r_1>=2,  r_k<=3,  1-t^k<=k/N.

Writing x=1/D, the l=1 term of (3) is 3+3/D+1/D^2. The l=2 term is

    9/(4D) * F(x),
    F(x)=(1-x)/(1+x)*(1+x+x^2/3)^2,
    F(x)-1=-(x^2/3+x^3+5x^4/9+x^5/9)/(1+x).

For 0<=x<=1/2, |F(x)-1|<=x^2. With lambda_0=D sigma<=4/D,
the remaining diagonal sum is bounded by

    N sum_(l>=3) lambda_0^l/(l!)^2
       <=N lambda_0^3 exp(lambda_0)/36 <=64/(3D^2).

In particular,

    |h_D-3-21/(4D)| <=32/D^2.                               (5)

Also, on dividing L_(D,M) by binom(D,M),

    1 <= R_(D,M):=L_(D,M)/binom(D,M)
      <= exp(D sigma/(M+1)).                                (6)

Indeed its l-th summand is (D-M)_l sigma^l/[(M+1)^rising_l l!].
Set kappa=(3/2)sqrt(6). Formula (4) gives

    D A_D/kappa
      =[(1+t)/2] [Dv/3]^2 sqrt(1-1/D)
        sqrt(r_2/3) [3/r_1] R_(D,2).

The six factors are respectively bounded by 1,3,1,1,3/2,2; their distances
from 1 are at most (1/2,4,1,2,3/2,3)/D. Telescoping the product proves

    |D A_D-kappa| <=128/D.                                  (7)

For completeness, the full residual has a direct positive-coefficient bound.
Define

    w_k=(1-t^k)^2 r_k/k,
    B_M=[z^M] exp(sum_(k>=2) w_k z^k).

Summing the squared coefficients (2) at fixed excitation mass M gives

    S_M=N^2 v^(2M) (D)_M R_(D,M)^2 B_M /[(M!)^2 r_1^M].

Since w_k<=3k/N^2 and sum_(k>=2) k/2^k=3/2,
B_M<=9*2^M/N^2 for M>=2. For M>=3, (6) consequently gives

    sum_(M>=3) S_M <=25^3 exp(27/D)/(4D^3).

Thus the requested initial-generator statement has the explicit bound

    ||D(H-h_D)Omega_D-kappa|D-2,1>||
       <=128/D +125 exp(27/(2D))/(2sqrt(D)).                 (8)

This proves the initial O(D^(-1/2)) assertion independently of the stronger
argument below. The D=1 system is a scalar and can be handled separately.

## 3. A uniform contour estimate on every pump column

Write |r;D>=|D-2r,r,0,...>, 0<=r<=R=floor(D/2), and set

    beta_k=(1-t^k)sqrt(r_k/k) q^(-k/2),  1<=k<=D.

Since q^(-D/2)<=exp(3/2), beta_k<=8sqrt(k)/D. Truncating the
vertex to k<=D is exact on the degree-D sector. Introduce a complex grading
variable xi: a mode-1 factor has grade 1 and every mode k>=2 factor has
grade 2. Define the vector-valued polynomial

    F_r(xi)=CT_z exp(xi beta_1 a_1^dagger z
                     +xi^2 sum_(k=2)^D beta_k a_k^dagger z^k)
                   exp(xi beta_1 a_1 z^(-1)
                     +xi^2 sum_(k=2)^D beta_k a_k z^(-k)) |r;D>.

The constant term preserves degree. Each side then has weighted degree at
most D, so F_r really is a finite polynomial; the unprojected creation
exponential is used only for its norm bound. Exactly,

    N(F_r(1)-|r;D>)=H|r;D>.                                (9)

The symmetric q^(-k/2) factors produce q^(-n) when the two weighted degrees
are n. There is no replacement of the native Hamiltonian here.

The needed Fock-space estimate is valid, not a semiclassical approximation:

    ||exp(sum x_k a_k^dagger) exp(sum y_k a_k)|n>||
      <= exp(sum |x_k|^2/2
               +sum (|x_k|+|y_k|)sqrt(n_k)).                (10)

To prove it, write exp(x a^dagger)=exp(|x|^2/2)D(x)exp(conj(x)a),
where D(x) is unitary, and bound the finite annihilation series by
sum_j |z|^j sqrt((n)_j)/j!<=exp(|z|sqrt(n)). Apply this to each mode.
In particular, annihilation in an initially empty mode contributes nothing.

Use the contour |z|=1/2 and

    |xi|=A=sqrt(D)/(r+1)^(1/4).

In (10), the mode-1 linear contribution is at most 20; the mode-2 linear
contribution is at most 34sqrt(2). The quadratic creation contribution is
at most

    8/[D sqrt(r+1)] +32/(r+1) sum_(k>=2) k/4^k
      =8/[D sqrt(r+1)]+56/[9(r+1)].

The total is less than 84. Hence the contour integral also satisfies

    sup_(|xi|=A) ||F_r(xi)|| <=exp(84).                       (11)

This bound includes creation into all initially empty modes. It neither
drops their norm nor assumes independent evolution of occupied modes.
For D>=16, r+1<=D implies A>=2. Cauchy's coefficient bound now shows that
all grades >=5 together have norm at most

    2exp(84) A^(-5)
      =2exp(84)(r+1)^(5/4)/D^(5/2).

After multiplication by DN<=2D^2, their contribution to D H|r;D> is at
most 4exp(84)(r+1)^(5/4)/sqrt(D). This is uniform up to r=R.

## 4. Low grades, boundary, and the uniform column theorem

Grades 1 and 3 vanish under CT. Grade 2 is beta_1^2 n_1. On pump columns,
grade 4 is

    beta_2^2 n_2 + beta_1^4 n_1(n_1-1)/4
      + beta_1^2 beta_2 (a_2^dagger a_1^2+a_1^dagger^2 a_2)/2.

(The full grade-4 diagonal is sum_(k>=2) beta_k^2 n_k.) After multiplying
by N, the three diagonal coefficients and the off-diagonal coefficient are

    v,
    d_2=(1+t)(2v+v^2)/2,
    d_11=v^2/(4N),
    g_D=(1+t)v^2 sqrt(2r_2)/(4r_1), respectively.            (12)

For 0<=r<=R, subtracting the r=0 low-grade diagonal changes it by

    r(d_2-2v)+d_11[(D-2r)(D-2r-1)-D(D-1)].

Its absolute value is at most 54r/D^2: |d_2-2v|<=29/D^2 and the second
term is at most 25r/D^2. By Section 2, replacing that reference diagonal
by the exact h_D costs less than 22/D^2.

The four-factor version of the product estimate in Section 2 gives

    |D^2 g_D-kappa|<=64/D.                                 (13)

For an allowed upward move, its remaining pump factor divided by D is
sqrt((1-2r/D)(1-(2r+1)/D)); its distance from 1 is at most (4r+1)/D.
For a downward move the corresponding bound is (4r-3)/D, r>=1. At r=R
the upward move is absent, both physically and in the truncated comparison.
Combining (12)-(13), the entire low-grade error is bounded by
240(r+1)^(3/2)/D after scaling by D.

Let J_D map the abstract one-mode Fock vector |r> to |r;D> for r<=R,
and to zero for r>R. Let b be the abstract annihilation operator and put

    A_D^cent=D(H-h_D I),       B=kappa(b+b^dagger).

The contour remainder and the low-grade calculation prove, for D>=16,

    ||A_D^cent J_D|r> - J_D B|r>||
       <= C_col (r+1)^2/sqrt(D),  0<=r<=R,
    C_col=8exp(84).                                         (14)

This is an actual norm bound on complete output columns, including leakage
into all other modes. No bound on an individual finite-dimensional matrix
entry has been substituted for it. In particular it also supplies the
requested fixed-r core-generator theorem.

## 5. Finite-time consequence with the omitted boundary charged

For real s, the exact abstract evolution is the normalized coherent vector

    psi(s)=exp(-isB)|0>
      =exp(-lambda/2) sum_(r>=0) (-i kappa s)^r/sqrt(r!) |r>,
    lambda=kappa^2 s^2=(27/2)s^2.

Compare the native vector exp(-is A_D^cent)Omega_D with J_D psi(s).
Duhamel's formula uses the residual (A_D^cent J_D-J_D B)psi(s).
Besides the columns in (14), there is exactly one omitted-input term:

    -kappa sqrt(R+1) <R+1|psi(s)> |R;D>.

Thus the top-pump boundary is explicitly paid; J_D is not treated as a
unitary map. For a Poisson(lambda) variable X,

    E(X+1)^6=1+63lambda+301lambda^2+350lambda^3
               +140lambda^4+21lambda^5+lambda^6
             <=21(1+lambda)^6.

Weighted Cauchy-Schwarz consequently gives

    sum_(r>=0) sqrt(P(X=r))(r+1)^2 <=sqrt(42)(1+lambda)^3
                                                     <7(1+lambda)^3.

The omitted-input boundary is at most
kappa sqrt(21)(1+lambda)^3/(R+1)^(5/2), hence at most
120(1+lambda)^3/D^(5/2). Integrating the residual, a safe explicit bound is

    ||exp(-is A_D^cent)Omega_D-J_D psi(s)||
       <=64exp(84)|s|(1+lambda)^3/sqrt(D),  D>=16.           (15)

Let Q_(D,lambda) sample X~Poisson(lambda), output |X;D> if X<=R,
and output Omega_D otherwise. To compare normalized states, append an
orthogonal overflow flag of amplitude sqrt(P(X>R)) to J_D psi(s), then map
that flag to the same classical outcome as Omega_D. Its norm cost is at
most sqrt(21)(1+lambda)^3/(R+2)^3. Measurement contraction and (15) prove

    TV(P_native,Q_(D,lambda))
      <= min{1, 64exp(84)|s|(1+lambda)^3/sqrt(D)
                   +sqrt(21)(1+lambda)^3/(R+2)^3}.          (16)

Here native time is tau=uD, so s=2pi u; the removed scalar phase is
exp(-2pi i uD h_D). Therefore

    alpha=-i 3pi sqrt(6) u,       lambda=54pi^2 u^2.

In particular, using pi<4, the following deliberately loose fully explicit
bound holds for all D>=1 and real u (D<16 is covered by TV<=1):

    TV(P_native,Q_(D,54pi^2 u^2))
       <=min{1, C_G (1+|u|)^7/sqrt(D)},
    C_G=2^40 exp(84).                                       (17)

The enormous constant is a proof constant, not a useful numerical claim.
No finite-time conclusion was inferred merely from the initial derivative:
(10)-(14) supply the missing uniform columns, and (15) pays their coherent
sum and the finite-pump boundary.

## 6. Exact scope of the classical consequence

For rational u in any fixed polynomially bounded window, Q_(D,lambda)
has a fixed polynomial BIT/TV sampling clock. Put epsilon=2^(-b). First
compute a nonnegative rational lambda' with |lambda'-lambda|<=epsilon/8.
A mean perturbation changes Poisson laws in TV by at most its magnitude,
by the elementary Poisson-addition coupling. For 0<=r<=R, compute
p_r=exp(-lambda')lambda'^r/r! to absolute error

    delta=epsilon/[32(R+2)].

Clip these approximations into [0,1], put max(0,1-sum p_r) on the overflow
outcome, and normalize. Their total error before adding overflow is at
most epsilon/32; the resulting normalized categorical distribution has TV
error at most 3epsilon/64. Round its CDF to a grid with

    W=b+ceil(log_2(R+2))+4

bits and draw exactly W random bits. This adds at most epsilon/16 TV.
Together with the mean approximation, the sampler error is less than
epsilon/2. Treat u=0 directly as the point mass.

The O(D) probabilities use polynomial-bit elementary exp/log or
range-reduced series; all arguments have polynomial magnitude in this
window (including O(D L) when a nonzero rational u is very small).
The fixed irrational pi is computed to the required bits, not supplied as
advice. Exact factorials, interval elementary-function evaluation, and the
finite CDF therefore have polynomial bit cost in D, input bit length L,
and b, with no rejection loop or unbounded random-bit request.

This sampler's native error is the bound (16) or (17), plus its selected
CDF error. It meets requested accuracy 2^(-b) whenever the explicitly
checked approximation bound is at most 2^(-b-1), with the CDF assigned the
other half. For |u|<=D^gamma, inverse-polynomial accuracy D^(-c) follows
beyond an explicit threshold when 7gamma+c<1/2. Fixed u and fixed accuracy
are included. No exponentially fine accuracy for unrestricted D, no
arbitrary binary-time closure, and no general occupation-input sampler
follows. This is a proved restricted baseline, with no novelty, hardness,
or quantum-advantage conclusion.
