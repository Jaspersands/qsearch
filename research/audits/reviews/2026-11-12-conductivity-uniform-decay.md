# Periodic conductivity: the uniform integrable decay rate fails

2026-11-12. Scoped proof review of Mourrat's rate hypothesis for the actual
native circuit medium. Read current `STATE.md`, `TRAPS.md`,
`PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`, and the relevant parts of
Sections 1--5 of `audits/sources/periodic_conduction/mourrat.txt`.
No Git, network, API, numerical experiment or shared-note change. Commands
used `/opt/anaconda3/bin/python`.

## Verdict and source scope

REFUTED: for every native circuit medium at fixed contrast, the divergence
source satisfies Mourrat (3.5) with an exponent alpha>1 and a constant
independent of the side length L. A one-bit, two-phase layered medium already
forces that constant to grow at least as L^(2alpha-2). Reversibility and the
squared-semigroup identity do not improve this temporal exponent.

The same family has a positive constant Green--Kubo tail until times of order
L^2. In fact its ordinary truncation time for error epsilon is
Theta_rho(L^2 log(1/epsilon)) for sufficiently small epsilon. A cutoff
polynomial in n=log_2 L and inverse-polynomial precision misses a constant
part of the conductivity correction.

This is a counterexample to a source-rate import, NOT a lower bound for all
classical or multilevel estimators. The family is itself exactly soluble by
a harmonic mean. The source's identities remain valid, and a method that
retains/coarsens large scales or samples a long time efficiently is not
refuted by this argument.

The actual retained source says:

* Section 1, physical lines 46--48, assumes uniformly elliptic IID
  coefficients for its stochastic-homogenization computation. Theorem 1.2
  and its essentially epsilon^-2 log(1/epsilon) work conclusion occur at
  72--99. Stationarity alone is not its stated hypothesis.
* Sections 2--3 use a stationary probability inner product. In the
  reversible case, (2.5)--(2.6), lines 312--321, say
  C(t)=||exp(-t A/2)F||^2 and sigma^2=4 integral ||exp(-t A)F||^2 dt.
* The general rate hypothesis (3.5), lines 424--431, expressly requires
  alpha>1. Its multiplicative constant can be absorbed by redefining F
  mathematically; that rescaling must still be charged when estimating the
  ORIGINAL observable.
* Section 4 Propositions 4.1--4.2 also assume (4.1), a fourth-moment bound.
  Theorem 5.1 needs only integrability (3.4) for its exact resolvent identity.
  Propositions 5.2--5.3 and 5.5, lines 714--775 and 889--903, additionally
  use (3.5) for their stated rates. The distinction is substantive here.

## 1. One-bit medium and matching Hilbert-space normalization

Let L=2^n>=2, X=(Z/LZ)^2 and N=L^2. Let D be the native, UNSCALED forward
edge difference, with adjoint

    (D* v)(x)=sum_j [v(x-e_j,j)-v(x,j)].

Fix the native rational contrast rho>1 and put

    a(x,j)=rho  if 0<=x_1<L/2,
           1   if L/2<=x_1<L,               j=1,2.

The phase bit is the negation of the most significant bit of x_1; the
direction and x_2 inputs are ignored. This is a constant-gate circuit, or
O(n) under an encoding charging all input wires. No geometric advice is
supplied to its evaluator.

Use ordinary Euclidean sums on nodes/edges and the native unit edge vector

    eta(x,1)=1/L,       eta(x,2)=0.

Set

    A_L=D* a D,       f_L=D* a eta,
    C_L(t)=<f_L,exp(-t A_L)f_L>,
    Q_L=<f_L,A_L^+ f_L>,
    R_L(T)=integral_T^infinity C_L(t)dt.

The constant mode is removed by the pseudoinverse; f_L has mean zero.
A_L is the nonnegative generator of a reversible, irreducible continuous-
time walk whose invariant measure is uniform. For comparison with the
source's PROBABILITY inner product, use

    F_L=L f_L=D* a e_1,
    <u,v>_pi=(1/N)sum_x u(x)v(x).

Then <F_L,exp(-t A_L)F_L>_pi=C_L(t) and its Green--Kubo correction is Q_L.
Applying the probability inner product directly to f_L would introduce an
extra factor 1/N and would no longer represent the native correction.

Equivalently, give the periodic medium a uniform random translation. Its
finite translation-orbit law is stationary and ergodic, and the environment
process has exactly these correlations. Its periodic homogenized coefficient
is the finite-cell coefficient. Thus the counterexample does not depend on
changing the physical observable; it fails the uniform quantitative rate.

## 2. Exact corrector, energy and norms

Write delta=rho-1 and z=delta/(rho+1). Let

    h(i)=min(i,L-i),       0<=i<L,
    u_L(i,x_2)=(z/L)(h(i)-L/4).

This is mean zero. Its direction-1 difference is z/L on the high-conductivity
half and -z/L on the other half; its direction-2 difference vanishes.
Consequently

    a(x,1)[(D_1u_L)(x)-1/L]=-2rho/[(rho+1)L]

is constant. Taking divergence proves A_L u_L=f_L, including at both
interfaces. In particular u_L=A_L^+ f_L, without an eigenfunction ansatz.

The source is supported on the two interface columns:

    f_L(0,x_2)=-delta/L,      f_L(L/2,x_2)=delta/L.

Direct sums give the EXACT formulas

    ||f_L||^2 = 2delta^2/L,
    ||u_L||^2 = z^2(L^2+8)/48,
    Q_L = <u_L,A_Lu_L> = z^2(rho+1)/2
        = delta^2/[2(rho+1)].                            (1)

For the middle identity, with M=L/2,
sum_i(h(i)-L/4)^2=M(M^2+2)/6; the x_2 sum supplies another factor L.
These formulas also hold at L=2, where the native oriented torus edges
represent the two parallel bonds.

The minimizing potential is -u_L in the normalized energy formulation.
Thus the actual conductivity is

    K_1=(rho+1)/2-Q_L=2rho/(rho+1).                       (2)

The correction Q_L is positive and independent of L even though the source
variance in (1) tends to zero. This is the source of the nonuniform tail.

## 3. A quantitative low-frequency mass certificate

This proof needs no continuum approximation or numerical diagonalization.
On mean-zero functions, ellipticity gives A_L>=D*D and therefore

    lambda_min(A_L)>=4 sin^2(pi/L)>=16/L^2.               (3)

Put b_rho=48(rho+1). The exact Rayleigh quotient in (1) is

    <u_L,A_Lu_L>/||u_L||^2
       =24(rho+1)/(L^2+8)<=b_rho/(2L^2).

Hence at least half of the squared norm of u_L is in the spectral interval
[16/L^2,b_rho/L^2]: the complementary mass bound follows simply by
integrating lambda against its positive spectral measure. If w_lambda is
that measure, then

    C_L(t)=sum_lambda lambda^2 exp(-lambda t) w_lambda,
    R_L(T)=sum_lambda lambda exp(-lambda T) w_lambda.

Restricting to the indicated interval and using (1)--(3) yields, for EVERY
L>=2 and t,T>=0,

    C_L(t) >= (8z^2/(3L^2)) exp(-b_rho*t/L^2),            (4)
    R_L(T) >= (z^2/6) exp(-b_rho*T/L^2).                 (5)

The spectral gap also gives the matching upper tail estimate

    R_L(T)<=Q_L exp(-16T/L^2).                            (6)

All constants depend only on the fixed contrast. For rho=2 these data are
z=1/3, b_rho=144, Q_L=1/6 and K_1=4/3.

## 4. Consequences for (3.5), squared moments and cutoffs

If C_L(t)<=C_alpha(1+t)^(-alpha) were uniform in L, evaluate (4) at
t=L^2/b_rho. It would imply

    C_alpha >= [8z^2/(3e*b_rho^alpha)] L^(2alpha-2).       (7)

Every fixed alpha>1 therefore requires an unbounded, exponentially-in-n
prefactor. This does not contradict (3.5) for any single finite chain:
each such chain has exponential decay, with L-dependent constants.

The reversible squared-semigroup moment is exactly

    E_pi[(exp(-t A_L)F_L)^2]=C_L(2t).

It has the SAME obstruction, at t=L^2/(2b_rho). Squaring a conditional
expectation can reduce sampling variance, as the source explains, but it
does not square the temporal decay exponent of this expectation.

The native conductivity correction obeys

    Q_L=integral_0^infinity C_L(t)dt
       =2 integral_0^infinity ||exp(-t A_L)F_L||_pi^2 dt.

The source's additive-functional variance is sigma^2=2Q_L, so the
conductivity is mean(a)-sigma^2/2, NOT mean(a)-sigma^2. Truncating the
first formula at T loses R_L(T); truncating the squared formula at T
loses R_L(2T). In particular, to make the ordinary tail at
most epsilon<z^2/6, (5) requires

    T >= (L^2/b_rho) log[z^2/(6epsilon)].                 (8)

Together with (6), this proves the stated Theta_rho(L^2 log(1/epsilon))
cutoff scale as epsilon decreases. There is no uniform cutoff depending
only on epsilon. More explicitly, contractivity and (1) give

    R_L(T)>=Q_L-2delta^2*T/L.

For T polynomial in n and 1/epsilon with epsilon=n^-a, the right side tends
to Q_L. Such a cutoff misses essentially the ENTIRE nonzero correction.

There IS a uniform critical-rate bound for every native medium:

    C_L(t)<=C_rho/(1+t),                                 (9)

for example C_rho=16rho^2. Indeed, put g=A_L^(-1/2)f_L. Energy minimization
gives ||g||^2=Q_L<=rho, while sup_lambda lambda exp(-t lambda)<=1/(et).
Thus C_L(t)<=rho/(et) for t>0; the elementary bound ||f_L||^2<=8rho^2
handles t<=1. Equation (7) shows that exponent one is sharp for an
L-uniform power bound over all circuit media. Its nonintegrability cannot
be repaired by knowing only the uniform total energy Q_L<=rho: the spectral
contribution can move to progressively later time scales.

## 5. Rescalings and the exact Section 5 remainder

The source's permission to absorb C_alpha into f is not free here. Replacing
f_L by f_L/sqrt(C_alpha,L) divides Q_L by C_alpha,L; restoring the original
conductivity multiplies the answer and its error by that factor. Bound (7)
must be paid in a native accuracy/work estimate.

Even unit-variance normalization does not help. For fhat=f_L/||f_L||,

    <fhat,A_L^+fhat>=L/[4(rho+1)],
    <fhat,exp(-L^2 A_L/b_rho)fhat>
       >=4/[3e(rho+1)^2 L].

The native prefactor ||f_L||^2=2delta^2/L restores the constant correction.
Alternatively using grid gradient L D gives A'=L^2 A_L and f'=L f_L.
Then C'(t)=L^2 C_L(L^2 t) and the correction is unchanged. A macroscopic
time cutoff now hides jump rates of order L^2, and ||f'||^2=2delta^2 L.
This change of time units is not an L-independent version of the source's
unit-lattice rate or simulation-cost assumption. Fixed contrast rescalings
by rho, in contrast, only change harmless fixed constants.

The exact resolvent decomposition in Theorem 5.1 still holds. Its geometric
choice mu_j=2^-j has

    f_k=r_k(A_L)f_L,       r_k(lambda)=product_(j=0)^k(1+2^j lambda)^(-1).

Its uncomputed remainder is

    E_k=<f_k,A_L^+f_k>
       >=(z^2/6) exp[-2b_rho(2^(k+1)-1)/L^2].           (10)

To prove (10), use the same low spectral band and
log r_k(lambda)>=-lambda sum_(j=0)^k 2^j. Thus the uniform
C*2^(-k(alpha-1)) remainder asserted after imposing (3.5) cannot be
imported: a constant-size remainder persists up to k about 2log_2 L.
For epsilon sufficiently small depending only on rho, the necessary scale
is k>=2log_2 L+log_2 log(1/epsilon)-O_rho(1), not O(log(1/epsilon))
independently of L. This is still only O(n) coarse
levels; it does not preclude an efficient method that pays those levels.

## Claim boundary

This counterexample rejects an L-uniform integrable Green--Kubo decay
assumption and the resulting short time/level cutoff for arbitrary native
circuits. It does not reject Mourrat's IID theorem or its exact reversible
identities, prove a variance lower bound for every estimator, or establish
classical hardness or quantum advantage. In particular, it leaves correlated,
wavelet, variational and cross-scale estimators untouched. The existing native
free-heat sampler already charges a cutoff of order L^2 and samples long
FREE heat-kernel times with paid bit complexity; nothing here invalidates it.
The present family itself has the immediate classical answer (2).
