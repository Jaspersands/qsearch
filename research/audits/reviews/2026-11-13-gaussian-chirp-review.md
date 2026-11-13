# Independent Gaussian-chirp / real-Hiary reduction review

13 November 2026. **Accepted at the absolute-error scope below**, with explicit
finite-bit details supplied here. Read current STATE/TRAPS, the full parent
`2026-11-13-gaussian-chirp-hiary-reduction.md`, and actual Hiary Theorem1.1
and section4 in `audits/sources/2026-11-13-one-pulse/hiary_theta.txt`.
No tests, implementation, network, API, Git, archive or shared-status edits.

## Exact statement

For binary integers L<=U and rationals alpha>=0, mu, a, b of total encoding
length B, and p>=1, the finite sum

    sum_{n=L}^U exp(-alpha(n-mu)^2) exp(2 pi i(an+bn^2))

has a deterministic absolute-2^-p approximation in polynomial(B,p) bit time,
using the constructive real-argument Hiary algorithm. There is no restriction
on numerical interval length, positive alpha, displacement mu, or proximity
of rational phase parameters to recursion boundaries. No relative-error or
normalized-distribution guarantee is included.

## Truncation and polynomial weight

Put H=U-L+1, h=bitlength(H), delta=2^-p, T=p+h+6. A nearest integer to mu,
clipped to [L,U], minimizes (n-mu)^2 there. Its exact rational test either
certifies an empty retained set or gives an interior starting point for two
monotone binary searches. Thus the condition alpha(n-mu)^2<=T finds its
entire retained interval with O(B) comparisons on polynomial-bit integers.
This includes mu far outside [L,U], arbitrarily tiny alpha, and huge alpha.
The discarded total modulus is at most H exp(-T)<=H 2^-T<delta/64.
Handle a singleton first; alpha=0 then uses Hiary after translation. A retained singleton is
one exponential with bounded real exponent and an exactly reduced phase.

For at least two retained integers set M=U0-L0>=1 and
Q(x)=alpha(L0+Mx-mu)^2. Both endpoints have Q<=T, hence convexity gives
0<=Q<=T on [0,1]. Write d=L0-mu. The endpoint inequalities imply
sqrt(alpha)|d|<=sqrt(T), sqrt(alpha)M<=2sqrt(T). Therefore

    alpha d^2<=T,  |2alpha dM|<=4T,  alpha M^2<=4T,

and ||Q||_1<=9T. This is valid even when mu is enormous and alpha tiny;
the potentially cancelling coefficients are computed exactly.

The parent's J=8(T+p+h+4) satisfies J+1>2eT. For
P_J(x)=sum_{l=0}^J (-Q(x))^l/l!, the REAL Lagrange remainder has derivative
factor exp(-xi)<=1. Thus

    sup |exp(-Q)-P_J| <= T^(J+1)/(J+1)! <=2^(-J-1)<delta/(64H).

Its contribution to the finite sum is <delta/64. Degree is at most 2J and
||P_J||_1<=exp(9T)<=2^(18T). These are coefficient-norm bounds, not an
assumption of numerically well-conditioned Taylor evaluation.

If Q has common denominator d_Q, then d_Q^J J! is a constructive common
denominator for every coefficient of P_J. Q's coefficient bit lengths are
O(B); consequently these denominators have O(J(B+log(J+1))) bits. The
coefficient-norm bound controls the numerators with an additional O(T) bits.
Exact dense polynomial arithmetic therefore has polynomial bit cost. It does
not generate exponentially long rational representations by repeated addition.

## Matching the actual source and finite precision

Writing P_J=sum c_j x^j and translating n=L0+k gives exactly

    exp(2 pi i(aL0+bL0^2))
      * sum_{j=0}^{2J} c_j F(M,j; a+2bL0, b),

where the actual source defines F as sum_{k=0}^M (k/M)^j times the quadratic
phase. There is NO missing M^j, 1/M, or interval-length normalization. At
j=0 the k=0 weight is1; Hiary explicitly adopts 0^0=1 (physical LF424).
All quadratic arguments remain real. The relevant primary locations are
LF62–95 (definition and Theorem1.1), LF1104–1198 (normalization and algorithm),
and LF1022–1045 (small-quadratic-argument boundary case).

Use the parent's zeta=2^(-p-18T-bitlength(2J+1)-8) as the allowed error per F.
Then sum |c_j| zeta<delta/256. The theorem's error is A1 nu^kappa1 eta,
not eta itself; the following allocation makes that conversion noncircular.
Fix source-dependent integers a0>=log2(max(1,A1)) and
s>=max(1,kappa1). Put

    q0=ceil(log2(1/zeta)), m=ceil(log2(M+1)),
    X=q0+m+j+a0+s+10,
    q=16(s+1)^2 X^2,  eta=2^-q.

Then nu=(j+1)log(M/eta)<=32 X^5, so log2(nu)<=3X (X>=10).
Hence A1 nu^kappa1 eta<=2^(a0+3sX-q)<=zeta/2. Every parameter and the
source's operation/operand-bit bounds remain polynomial(B,p). The constants
are fixed effective constants of its explicit analytic algorithm, not advice
depending on the input. This review does not claim optimized numerical values
for them or an implemented version of the source algorithm.

Exact-real input and floor decisions need no separation promise. One option
is to round both phase arguments, modulo1, to dyadics with
R=q0+3m+8 bits. Since (k/M)^j<=1,

    |partial_a F|<=pi M(M+1),
    |partial_b F|<=2 pi sum_{k=0}^M k^2.

The total perturbation is <=16(M+1)^3 2^-R<=zeta/16. This leaves room for
the preceding Hiary error. Rational phases could instead be retained exactly.

There is also a useful exact guard for Hiary's internal floor/ceiling branches.
Represent a normalized pair as a=A/D, b=C/D with common EVEN denominator D,
0<=A<D and 0<=C<=D/4. The nonboundary iteration b>0 sends the pair to

    a*=A/(2C),  b*=-D/(4C).

A common even denominator is D'=4C<=D, with numerators 2A and -D.
Integer reductions, conjugation, and the half-shifts of Lemma4.1 preserve that
denominator. Thus the denominators of these exact rational branch parameters
never grow; numerator reductions and floor(a+2bM) use polynomially many bits.
At b=0 the source uses its boundary procedure. In an iteration the new length
is floor(a+2bM)<1+M/2, so outside its explicit small-length cutoff there are
O(log(M+1)) iterations. This supplies an exact branch implementation even
arbitrarily close to an integer, rather than assuming rounded comparisons work.

The source's small-length case evaluates directly only when
M<=1000((j+1)log(M/eta))^6, which is polynomial in the charged parameters.
It does not silently enumerate a binary-large interval. Elementary exponential
and logarithm evaluation at its stated polynomial operand precision has
polynomial bit cost; source section4 supplies the finite algorithm and clock.

## Assembly and boundary of the result

Keep the rational c_j exact, or round them with their explicitly bounded
product magnitudes included. Each F has modulus<=M+1; intermediate products
and sums need O(18T+h) integer bits and polynomially many fractional guard bits.
The exact coefficient denominator storage above is separately charged.
Reduce aL0+bL0^2 modulo1 exactly, and approximate its unit complex phase to
delta/[16(H+1)]. The true polynomial-weight sum has modulus at most H+delta/64,
so this phase error contributes <delta/8. Polynomially allocated rounding,
the two truncation errors, and the F errors leave total error strictly <delta.

The parent statement survives; no counterexample or change of hypotheses is
needed. This closes Gaussian damping of a finite quadratic chirp ONLY. It
does not pay binomial/Krawtchouk approximation, confluent derivatives, bilinear
Cauchy sums, a native count CDF, rejection probabilities, or photon sampling.
