# Gaussian-damped quadratic sums reduce to actual Hiary sums

13 November2026. Parent derivation; under independent check. This is one
specific missing weighted-sum operation in ONE_PULSE_KERR_CDF.md, not a
Krawtchouk, bilinear-Cauchy, native CDF or photon-count sampler theorem.

## Statement

Given binary integers L<=U, rational alpha>=0,mu,a,b of total encoding B,
and requested precision p>=1, compute to absolute error<=2^-p the finite sum

 S=sum_(n=L)^U exp(-alpha*(n-mu)^2)*exp(2pi i*(a*n+b*n^2)).

There is a deterministic polynomial(B,p) BIT reduction to Hiary's actual
Theorem1.1: F(M,j;A,B)=sum_(k=0)^M (k/M)^j exp(2pi i*(A*k+B*k^2)),
with real A,B reduced mod1, positive integer M, and polynomial j. Its native
BIT clock follows from that actual primary theorem, with its constructive
fixed constants and standard finite-precision real arithmetic. No inverse
normalization or exponentially small relative-error target is silently paid.
The desired error is ABSOLUTE. This statement does not replace a coherent
source distribution or a measurement kernel by a Gaussian.

## 1. Truncate using exact rational comparisons

Put H=U-L+1 and let ell(H) be binary bitlength. Set

 T=p+ell(H)+6,  delta=2^-p.

Keep only integers in [L,U] for which alpha*(n-mu)^2<=T. Convexity makes
this either empty or one contiguous interval [L0,U0]. Find its endpoints
by exact rational comparisons and binary search about the nearest integer
to mu clipped into [L,U]. There are O(B) comparisons; squaring and rational
cross multiplication have polynomial bit length. No real-root oracle or
iteration over H integers is needed. Alpha=0 can use Hiary directly.

Every discarded summand has modulus<exp(-T)<=2^-T, so the total discarded
absolute mass is at most H*2^-T<delta/64. An empty interval is now finished.
If L0=U0, evaluate one exponential to the remaining absolute error budget.
All original and retained integer bounds have O(B) bits.

## 2. A polynomial weight on the surviving interval

Let M=U0-L0>=1, x=(n-L0)/M in[0,1], and

 Q(x)=alpha*(L0+M*x-mu)^2.

The convex quadratic satisfies 0<=Q(x)<=T on the whole real interval,
since this holds at both endpoints. Its three coefficients have l1 sum
<=9T: the quadratic coefficient is <=4T because two endpoints are M apart,
the absolute linear coefficient is <=4T, and the constant is <=T.
Take

 J=8*(T+p+ell(H)+4),
 P_J(x)=sum_(j=0)^J (-Q(x))^j/j!.

Taylor's real Lagrange remainder for exp(-t), t>=0, gives

 |exp(-Q(x))-P_J(x)| <= T^(J+1)/(J+1)!
                       <=(e*T/(J+1))^(J+1)
                       <=2^(-J-1) < delta/(64H).

The factorial bound is elementary and J+1>2eT. Thus summing this pointwise
error over the retained integers costs <delta/64. Degree(P_J)<=2J, and
its coefficient l1 norm is bounded by

 sum_(j=0)^J ||Q||_1^j/j! <= exp(9T) <=2^(18T).

The last loose inequality uses e<4. Every coefficient is rational. A
common denominator obtained from the denominator of Q raised to J times
J! gives O(J*(B+log J)) coefficient bits, with harmless polynomial slack
for endpoint products. No repeated rational addition forces exponential
encoding: this displayed common denominator is available constructively.
Compute all coefficients with polynomially many exact rational operations.

## 3. Call only the supported real quadratic-sum theorem

Write P_J(x)=sum_(j=0)^(2J) c_j*x^j. Factoring out the phase at L0 gives

 exp(2pi i*(a*L0+b*L0^2))*
 sum_(j=0)^(2J) c_j*F(M,j;a+2b*L0,b).

These are precisely Hiary's real-argument polynomial-weight sums; no complex
quadratic argument is passed. Reduce a+2bL0 and b mod1 by rational arithmetic.
Request absolute error

 zeta=2^[-p-18T-ell(2J+1)-8]

for each F. The coefficient sum bound limits the combined oracle error
to <delta/256. The polynomial prefactor in Hiary's stated error is absorbed
by choosing its internal error parameter smaller by a fixed polynomial;
nu=(j+1)log(M/eta) stays polynomial(B,p). These are the same effective fixed
constants as in the primary theorem, not user-supplied advice or new
claimed practical numbers. Reading longer rational arguments also costs B.
Alternatively parameter rounding to O(p+T+3ell(M)+log J) bits is safe by
the elementary derivative bounds for the finite sums; it does not require
exact-real access or a gap from an integer in the internal theta algorithm.

Exact coefficients and guard precision O(p+18T+ell(H)+log J) suffice for
the final products/sum. The phase at L0 is computed modulo1 exactly, then
its exponential to error delta/[16(H+1)]. The true retained sum has
modulus<=H and its polynomial approximation differs by <delta/64, so this
phase multiplication adds <delta/8. Choosing each rounding allocation
below delta/256 leaves ample slack for total error<=delta. The number of
calls and every requested operand/output precision are polynomial(B,p).

## Boundary and relevance

This proves that Gaussian damping ALONE is not a blocker to using the actual
real Hiary interface. It does not give a uniform polynomial approximation
for chirped binomial amplitudes times high-degree Krawtchouk functions, their
confluent derivatives, or the bilinear Cauchy sum. Those are still the native
CDF blockers. No normalized sampling distribution, small denominator,
constant rejection cost, novelty, implementation or quantum speedup follows.
Source: audits/sources/2026-11-13-one-pulse/hiary_theta.txt, actual1.1 and
algorithm section4 already parent read. No new finite test is needed for
this exact symbolic reduction; independent proof review is pending.
