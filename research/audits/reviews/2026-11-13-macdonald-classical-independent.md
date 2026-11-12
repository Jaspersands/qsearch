# 2026-11-13 — Independent Macdonald classical-baseline audit

**Both requested claims are valid.** The first is a bounded-clock classical
occupation sampler of cost (D+1)^O(s) poly(D,b), with TV error at most 2^(-b),
for lambda_1>=D-s or length(lambda)>=D-s. The second is the stated positive
uniform TV floor against the alpha=3 Jack ROW law for every D>=200. Neither
is a lower bound against general classical algorithms. In particular both
row laws themselves have classical polynomial-time samplers.

Read: current STATE/TRAPS; MACDONALD_CLASSICAL_BASELINES; actual retained
Borodin–Corwin arXiv v4, §§2.1.3–2.1.6, physical LF 1527–1705; actual
Mickler Theorem 4.1, LF 813–825. In Pieri (2.10), mu_(j+1) and lambda_(j+1)
are partition indices. They are not mu_j+1 or lambda_j+1. This distinction
is essential to the positive finite-factor proof below. No advisory ACCEPT
label, Poisson–Dirichlet limit, numerical sweep or implementation is used.
No network, API or Git was used. Only this independent note was written.

## 1. Native scalar product, row coefficients and transposition

Throughout ALL degrees use the global parameters

    t=D/(D+1), q=t^3, r_k=(1-q^k)/(1-t^k)=1+t^k+t^(2k).

For D=0 handle vacuum directly; below D>=1. Actual source §2.1.3 gives

    <p_mu,p_mu>=R_mu:=z_mu product_k r_k^(m_k),
    g_n=Q_(n)=sum_(mu partition n) p_mu/R_mu.

Since g_n is a nonzero scalar multiple of P_(n), its occupation law is
proportional to product_k w_k^(m_k)/(k^(m_k)m_k!), w_k=1/r_k. This also
identifies the reference row law used in the tilt argument; no infinite
product evaluation or supplied row normalization is needed.

Source (2.3)–(2.4) already pays the column transfer without an integral-form
oracle. The map omega sends p_k to (-1)^(k-1)r_k p_k and P_lambda(q,t) to
Q_lambda'(t,q). It is an isometry to the swapped Hall form, whose factor is
1/r_k. The coefficient-squared occupation weights are therefore unchanged.
The scalar difference between Q and P (or J) cancels upon normalization.
Apply the near-row algorithm to lambda' with the SWAPPED parameters for a
near-column input. In that computation the row weights are w_k=r_k.

## 2. Triangular horizontal-Pieri span, including its diagonal

Assume D>=2s. Index near-row degree-D shapes by

    kappa=(D-j,rho), 0<=j<=s, rho a partition of j.

These are all valid shapes and all such near-row shapes, since D-j>=j.
For each index form F_(j,rho)=g_(D-j) P_rho. If kappa/rho is a horizontal
strip, interlacing is

    kappa_i >= rho_i >= kappa_(i+1).

Consequently sum_(i>=2) kappa_i <= |rho|=j, so kappa_1>=D-j. If equality
holds, every kappa_(i+1)<=rho_i is an equality, hence kappa=(D-j,rho).
Conversely that skew diagram is a horizontal strip. Its Pieri coefficient
is strictly positive by the source product, as justified in §3.

Thus, in the P_kappa basis ordered by tail size D-kappa_1, the matrix of
the F_(j,rho) is triangular by tail size, and its diagonal blocks are
DIAGONAL with nonzero positive entries. It is invertible. Its size is
M=sum_(j=0)^s p(j)<=2^s (also M=1 for s=0). No full degree-D basis is
constructed. Solving it gives

    P_lambda = sum_(j=0)^s g_(D-j) h_j,

where each h_j is a rational linear combination of degree-j P_rho. Lower
coefficients need not be positive; the sampler below includes their signed
cancellations before squaring.

## 3. Finite rational generation and bit complexity

Write f(u)=(tu;q)_infinity/(qu;q)_infinity. Its shift identity is

    f(qu)/f(u)=(1-qu)/(1-tu).

For a horizontal strip and i<=j, the four exponents of q in (2.10) are

    kappa_i-kappa_j,  rho_i-rho_(j+1),
    kappa_i-rho_j,    rho_i-kappa_(j+1).

All are nonnegative, by interlacing and monotonicity. They share the same
factor t^(j-i). Pair each numerator f with a denominator having that same
factor. The ratio f(q^a t^c)/f(q^b t^c), for a,b,c>=0, is a product of
|a-b|<=D shift ratios, or their inverses. At q=t^3 each shift factor is

    (1-t^(3(r+1)+c))/(1-t^(3r+c+1)),    r>=0.

Every exponent is a positive integer O(D). The factor is positive, finite
and rational. With the swapped parameters q'=t,t'=t^3, the exponents become
r+1+3c and r+3(c+1), again positive O(D). Thus BOTH column and row transfers
avoid all specialized source poles. The index j+1 interpretation is needed
for the displayed nonnegativity.

There are at most O(D^2) pairs and O(D) shifts per pair. Each
1-(D/(D+1))^e has numerator/denominator bits O(D log(D+1)); hence a deliberately
loose O(D^4 log(D+1)) bound pays each exact Pieri rational. All tests and
products are explicit finite integer operations.

The degree-<=s P_rho are also natively computable. Enumerate their monomial
and power-sum bases and perform exact rational Gram–Schmidt in a total order
extending dominance. The positive diagonal power-sum Gram matrix makes every
pivot nonzero. The resulting monic orthogonal basis is the actual P basis;
generic triangular uniqueness and regular continuation give the same
specialized values. A monomial/power-sum change can be generated by finite
set-partition inclusion–exclusion or permutation enumeration, using at most
s^O(s) operations and polynomial-bit integer coefficients. Explicitly, for
parts nu_1,...,nu_l, divide by product_k m_k(nu)! the sum over set partitions
pi of {1,...,l} of product_(B in pi) [(-1)^(|B|-1)(|B|-1)! p_(sum_(i in B)nu_i)].
This is m_nu. Thus the conversion is native and fits (D+1)^O(s).

Exact rational elimination on these matrices and the M-by-M Pieri matrix
has polynomial BIT cost in their dimensions and entry bit lengths. To see
that small pivots do not conceal extra precision, clear all denominators:
the common denominator has at most the sum of their bit lengths, and
Hadamard bounds every required minor by polynomially many additional bits
in the matrix dimension. Fraction-free elimination or reduced rational
arithmetic therefore produces all h_j power-sum coefficients in
(D+1)^O(s) poly(D) bits and operations. There is no spectral-gap division
and no numerical decision that a nearly zero coefficient is zero.

The usual positive Gram argument suffices for regularity at q=t^3; it is
not being promoted to a polynomial full degree-D algorithm. The native
integral J has the same normalized occupation law as P. Mickler's principal
specialization was read but no global J-coefficient or integrality oracle
is needed for these two claims.

## 4. Squared small-cycle tilt and a finite sampling clock

Expand h_j=sum_(beta partition j) c_beta p_beta, and write b_k=m_k(beta).
For any degree-D mu, direct convolution with g_(D-j) gives exactly

    [p_mu]P_lambda * R_mu = Phi(m_1,...,m_s),
    Phi=sum_(|beta|<=s) c_beta
             product_(k<=s) r_k^(b_k) k^(b_k) (m_k)_(b_k).

A falling factorial is zero if b_k>m_k. Thus

    |[p_mu]P_lambda|^2 R_mu = Phi(m_1,...,m_s)^2 / R_mu.

This is the base weighted-cycle law tilted by a squared rational polynomial
in only the first s cycle counts. It includes every interference term.

For w_k=1/r_k (or the swapped row weights), compute restricted coefficients

    Z_0^(>s)=1,
    n Z_n^(>s)=sum_(k=s+1)^n w_k Z_(n-k)^(>s).

Enumerate the at most L=(D+1)^s nonnegative vectors (m_1,...,m_s) with
sum k m_k<=D. Assign the exact nonnegative weight

    Phi(m)^2 * product_(k<=s) (w_k/k)^(m_k)/m_k!
             * Z_(D-sum k m_k)^(>s).

Their total is positive because P_lambda is nonzero; compute it, rather
than supply a norm. Sample this finite vector table. For the remaining
mass n, recursively select k>s with probability

    w_k Z_(n-k)^(>s)/(n Z_n^(>s)),

and append a k-cycle. The recurrence normalizes these probabilities.
Induction verifies the multiset law: summing over the last removed part
multiplies its proposed weight by sum_k k m_k/n=1. Zero residual coefficients
are simply unreachable; zero table entries are tested exactly.

Here is an explicit rational bit guard. Write each w_k=A_k/B_k in reduced
positive integers. Its bit length is O(k log(D+1)). The number

    D! * product_(k=1)^D B_k^floor(D/k)

is a common denominator for every restricted coefficient Z_n: z_mu divides
n!, and m_k<=D/k. Its logarithm is O(D^2 log(D+1)). Since 1/3<=w_k<=3,
Z_n<=3^D; the numerator has the same polynomial bit bound. The c_beta have
the already paid bit bounds. Multiply their denominators AND the factor
product_(k<=s) den(r_k)^floor(s/k) to get a common denominator for every Phi.
The latter factor has O(s^2 log(D+1)) bits. Squaring this guard and combining
it with the cycle guard bounds all vector weights and their total by
(D+1)^O(s) poly(D) bits.
Hence normalization and cancellations introduce no uncharged inverse-small-
probability cost.

For a fixed clock with TV tolerance eta=2^(-b), use

    b'=ceil(log2(2(L+D^2+1)/eta))

fair bits for each CDF draw, compare the dyadic number with the EXACT rational
CDF, and stop after at most D residual draws. Coupling with continuous
uniforms, at most L vector-table boundaries plus D^2 residual boundaries
can alter a choice. Total TV error is <=(L+D^2)2^(-b')<eta. The additional
precision is O(b+s log(D+1)); the complete BIT clock has the stated form.

If D<2s, enumerate all degree-D partitions and perform the same exact
finite-dimensional computation. Even D^D<=D^(2s) for D>=2, so this fallback
also fits (D+1)^O(s) poly(D,b). D=0,1 are direct. One may compute the actual
row/column deficit from the supplied shape and use it as s; no promise
certificate or coefficients are provided as advice. No polynomial bound
for unrestricted growing s is asserted.

## 5. Exact finite uniform TV separation: constants verified

Let Q_D be Ewens(theta=1/3), the alpha=3 Jack row occupation law, and P_D the
deformed row law. Put h=log(1+1/D), u=Dh in [1/2,1], and

    g(x)=log((1+2cosh(x))/3),  G(mu)=sum_k m_k g(hk).

Because w_k=(1/3)exp(hk-g(hk)) and sum k m_k=D, the normalized density is
EXACTLY L(mu)=P_D(mu)/Q_D(mu)=exp(-G(mu))/E_Q exp(-G). The linear exp(u)
factor cancels. No limiting process is used.

The derivatives satisfy g(0)=g'(0)=0 and

    g''(x)=(2cosh(x)+4)/(1+2cosh(x))^2.

For 0<=x<=1, cosh(1)<8/5 gives g''>=6/(21/5)^2=50/147. For the upper bound,
with c=cosh(x)>=1, the inequality g''<=2/3 is equivalent to
(c-1)(8c+10)>=0. Therefore

    (25/147)x^2 <= g(x) <= x^2/3.

Convexity and g(0)=0 imply g(a)+g(b)<=g(a+b) for nonnegative a,b; g is also
increasing. Thus the sum over any remaining cycles is at most g of their
total scaled length.

For D>=200 take the inclusive integer intervals
I_A=[.90D,.91D] and I_B=[.40D,.41D]. Each has at least D/200 integer entries,
since its real length is D/100>=2. Let A mean there is one I_A-cycle and
B mean there are two I_B-cycles, counting multiplicity. There cannot be
two I_A-cycles or three I_B-cycles. On these events,

    G|A >= g(.90u) >= (27/196)u^2,
    G|B <= 2g(.41u)+g(.20u) <= (627/5000)u^2.

The remaining mass on B is at most .20D. The constants subtract to

    [27/196-627/5000]u^2 = (3027/245000)u^2
                              >= delta0:=3027/980000.

For Z_n=(theta)_n/n!, the exact Ewens factorial moments are

    E m_k=theta Z_(D-k)/(k Z_D),
    E[m_k(m_l-1_{k=l})]=theta^2 Z_(D-k-l)/(kl Z_D).

All indices used here are nonnegative. Since Z_(n+1)/Z_n=(n+theta)/(n+1)<1,
each displayed Z-ratio is >=1. The event indicators are exactly

    1_A=sum_(k in I_A) m_k,
    1_B=(1/2)sum_(k,l in I_B) m_k(m_l-1_{k=l}).

The second identity includes repeated equal-sized cycles, and explains the
factor one half. Using k,l<=D and the interval counts gives

    Q_D(A)>=1/600,  Q_D(B)>=1/720000.

Let a_* and b_* be the respective lower and upper G thresholds above.
Every L on B exceeds every L on A by at least

    exp(-b_*)[1-exp(-(a_*-b_*))] / E_Q exp(-G)
       >= delta0/4.

Indeed E_Q exp(-G)<=1, b_*<=627/5000<1/2, exp(-b_*)>1/2, and
1-exp(-delta0)>=delta0/2 because 0<delta0<1. Relative to 1, either ALL of A
has L<=1-delta0/8 or ALL of B has L>=1+delta0/8. Consequently

    TV(P_D,Q_D)=(1/2)E_Q|L-1|
       >= delta0/(16*720000) > 0,     for every D>=200.

This verifies the parent's exact floor, all event counts, the density sign
and the repeated-cycle convention. It refutes approximation of these rows
by merely using the Jack row law to a tolerance tending to zero. It does
not refute a classical deformed-row algorithm (one is explicitly available),
a general classical sampler, or any other parameter-dependent approximation.
