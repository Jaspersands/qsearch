# Balanced one-pulse Kerr: deterministic endpoint amplitudes

13 November 2026. **Proved at the endpoint-amplitude scope below.** Read current
STATE/TRAPS and the checked real-Hiary/Gaussian reduction. No code, numerical
tests, network, API, Git, archives, or shared-status edits. The argument uses
certified polynomial interpolation of the binomial weight; no growing-degree
Hermite or Krawtchouk asymptotic theorem is assumed.

## Statement and exact conventions

Let K>=0 be binary, zeta=a/b rational in binary, p>=1, and 0<=r<=K with
min(r,K-r)<=Y. There is a deterministic algorithm, polynomial in

    Y, bitlength(K+1), bitlength(a/b), p,

which approximates to absolute error 2^-p the complex number

    A_r = 1/sqrt(C(K,r)) sum_{n=0}^K P_K(n) K_r(K-n) e(zeta binom(n,2)),
    P_K(n)=2^-K C(K,n),  e(t)=exp(2 pi i t),
    K_r(x)=[z^r](1-z)^x(1+z)^(K-x).

This is the sum specified in the task. For the literal convention
B(theta)=exp(theta(a†b-b†a)), both rotations +pi/4, and n/r counting mode a,
the physical amplitude is **(-1)^(K+r) A_r**. Indeed
B a† B^-1=(a†-b†)/sqrt2, B b† B^-1=(a†+b†)/sqrt2. The first rotation
contributes (-1)^(K-n), while the second matrix entry contains
(-1)^n K_r(n); use K_r(n)=(-1)^r K_r(K-n). This known output sign costs
nothing, but should not be silently dropped from a complex-amplitude contract.

Two exact polynomial identities pay the endpoint reduction:

    K_r(K-n)=sum_{j=0}^r (-1)^(r-j) 2^j C(K-j,r-j) C(n,j),             (1)
    K_{K-s}(x)=(-1)^x K_s(x),  integer 0<=x<=K.                         (2)

For (1), expand (1-z)^K(1+2z/(1-z))^n. For (2), take the reciprocal
degree-K generating polynomial. Thus (1) has degree r and leading coefficient
2^r/r!. For an upper endpoint r=K-s, replace r by s, multiply by (-1)^K,
and add 1/2 to the linear phase in n. Normalization C(K,K-s)=C(K,s) is
unchanged. It suffices henceforth to compile the lower endpoint and an
arbitrary rational linear/quadratic phase e(A n+B n^2); originally
A=-zeta/2, B=zeta/2. The upper-endpoint shift is exact.

At integer 0<=n<=K, the generating formula and Vandermonde's identity give
|K_r(K-n)|<=C(K,r)<=(K+1)^r. Also 1/sqrt(C(K,r))<=1.
The integer C(K,r) has O(r log(K+1)) bits and is computed with r factors.

## 1. A central window and the only direct branch

K=0 is immediate. Put ell=bitlength(K+1) and

    Q=p+(r+1)ell+20,  J=2048 Q.

If K<=2^30 Q^2, evaluate the original finite sum directly. The number of
terms and even expanded factorial/binomial bit lengths are then polynomial
in the declared resources. The criterion is an exact integer comparison;
it does not presume K is small because its binary encoding is short.

In the other branch put c=K/2, w=ceil(sqrt(KQ)),
L=ceil(c-w), U=floor(c+w), M=U-L. Integer square root gives the endpoints
exactly. The chosen cutoff implies w<K/4 and w>J/2+1, so 0<=L<U<=K.
For a Bin(K,1/2) variable, Hoeffding's bound gives

    sum_{n outside [L,U]} P_K(n) <=2 exp(-2w^2/K)<=2 exp(-2Q).

Consequently deleting this tail changes A_r by at most
2^(r ell+1-2Q)<2^(-p-20), uniformly in the phase. This pays the potentially
large polynomial factor before making any approximation to the central weight.

## 2. Entire-function bound for the binomial weight

For proof only, extend P_K to the entire function

    f(c+u)=2^-K Gamma(K+1)/[Gamma(c+u+1)Gamma(c-u+1)].

Euler's product for Gamma, with the two opposite shifts paired, gives the
locally uniformly convergent product

    f(c+u)=f(c) product_{l=0}^infinity (1-u^2/(c+1+l)^2).              (3)

This identity also follows directly by taking the paired finite products
in Euler's limit formula; their exponential powers cancel. Duplication and
the beta integral give

    f(c)=Gamma(c+1/2)/(sqrt(pi)Gamma(c+1))
        =(1/pi) integral_0^1 t^(c-1/2)(1-t)^(-1/2) dt <=1.

Since sum_{l>=0}(c+1+l)^(-2)<=1/c=2/K, (3) proves for EVERY complex u

    |f(c+u)| <= exp(2|u|^2/K).                                      (4)

No complex Gamma evaluation is needed by the algorithm.

Choose J+1 consecutive integer nodes n_i=n_0+i, with
n_0=floor(c)-J/2, 0<=i<=J. They lie in [L,U]. Let I_J be their exact
degree-J interpolation polynomial for f. On the circle |z-c|=8w,
(4) gives |f(z)|<=exp(128w^2/K)<=exp(512Q)<=2^(1024Q).
For every real n in [L,U], the contour interpolation remainder is bounded by

    |f(n)-I_J(n)|
      <= (8/7) 2^(1024Q) (2/7)^(J+1)
      <= 2^(1024Q-J) = 2^(-1024Q).                                  (5)

Here |n-n_i|<=2w, |z-n_i|>=7w, and |z-n|>=7w. The standard contour
formula follows by residues at the nodes and n; its bound is independent
of how clustered the nodes are. At a node the error is exactly zero.
After summation against K_r and the phase, (5) contributes at most
2^((r+1)ell-1024Q)<2^(-p-20). This is a uniform absolute bound, including
arbitrary rational revivals and all cancellations.

## 3. Construct the interpolant with polynomial bits

Only ONE scalar needs numerical evaluation for the node values (its exact
rational expansion could have numerical K bits):

    b0=P_K(n_0),
    q_i=P_K(n_i)/P_K(n_0)
       =product_{t=0}^{i-1} (K-n_0-t)/(n_0+t+1).

Every q_i is an exactly computed positive rational of O(J ell) bits, with
q_i<=(K+1)^J. In the scaled variable x=(n-L)/M, write I_J(n)=b0 R_J(x),
where R_J interpolates these rational ratios. Its Lagrange basis is

    l_i(x)=product_{j!=i}(Mx-(n_j-L)) / [(-1)^(J-i) i!(J-i)!].

All node offsets lie in [0,M], so

    ||R_J||_1 <=(J+1)[2(K+1)^2]^J.                                  (6)

A common denominator is D_node J!, with
D_node=product_{t=0}^{J-1}(n_0+t+1). Each prefix denominator for q_i
divides D_node, and each i!(J-i)! divides J!. Thus this is a constructive
O(J(ell+log(J+1)))-bit denominator. Bound (6) also pays the numerator
bits. Dense exact polynomial construction is polynomial time; clustered
interpolation is not being treated as floating-point well conditioned.

Formula (1), with n=L+Mx, constructs the other polynomial exactly. Its
coefficient norm is at most (r+1)[4(K+1)]^r: each falling-factorial term
C(L+Mx,j) has coefficient norm <=(2K)^j/j!. A denominator r! suffices.
Therefore W(x)=R_J(x)K_r(K-L-Mx) has degree d=J+r and a constructive
common denominator D_node J! r!. All its coefficient bits are polynomial.
For the explicit integer

    E=bitlength(J+1)+J(1+2ell)+bitlength(r+1)+r(2+ell),

we have ||W||_1<=2^E. In particular, severe coefficient cancellation incurs
only E additional precision bits, not numerical K work.

## 4. Real Hiary calls, scalar precision and total clock

Write W(x)=sum_{j=0}^d w_j x^j. The retained approximating amplitude is

    b0/sqrt(C(K,r)) * e(A L+B L^2)
       * sum_{j=0}^d w_j F(M,j; A+2B L, B).                         (7)

This uses the ACTUAL normalized weights (k/M)^j in Hiary's real-argument
Theorem1.1. There is no missing M^j factor, no complex quadratic argument,
and no need to construct the large cyclotomic field of a/b. Rational phase
reduction, including the constant phase in (7), has polynomial bit cost.

Ask for absolute error 2^(-p-E-bitlength(d+1)-20) in each F. The checked
`2026-11-13-gaussian-chirp-review.md` supplies the source's polynomial error
prefactor conversion, exact rational branch choices, and deterministic
finite-bit clock. Equation (6) bounds the total weighted error. The exact
pre-scalar sum in (7) has modulus <=(K+1)2^E.

It suffices to compute b0, 1/sqrt(C(K,r)), and the unit phase to absolute
error 2^-P, where

    P=p+E+ell+bitlength(d+1)+50.

Clip the first two approximations to [0,1]. Square-root arithmetic uses the
already expanded O(r ell)-bit C(K,r). Compute b0 from

    log(b0)=log(K!)-log(n_0!)-log((K-n_0)!)-K log2.

The finite-bit logfactorial routine in `BINARY_FOCK_KERR_SAMPLING.md`
LF201–216 supplies polynomial(log K,P) evaluation: positive-real Stirling
with O(P+ell) terms and its first-omitted-term remainder, with a short
argument shift when necessary. Exact Bernoulli coefficients and the shift
products have polynomial bits. The extra ell guard bits pay multiplication
by K; no expanded K! or denominator 2^K is formed in this large-K branch.
If a scalar exponential is below the required absolute tolerance, it may
be clipped using a certified margin. No relative probability oracle is used.

Exact polynomial coefficients plus polynomially many guard bits pay the final
products/sum and final rounding. Combining scalar errors, Hiary errors, (5),
and the deleted tail leaves error <2^-p. Every degree, coefficient length,
requested precision, and call count is polynomial in Y,ell,p and phase bits.
All loops are explicitly bounded; there is no rejection or adaptive precision
search. This proves the statement, with the upper endpoint supplied by (2).

## Scope

The endpoint count Y may grow polynomially in log K and inverse sampling
accuracy; it is not a fixed constant. The result is stronger than the minimal
requested endpoint precision, since p is arbitrary and its cost is polynomial.
It does not prove the balanced bulk two-saddle construction, a balanced
sampler, a full CDF compiler, or anything for general passive angles. It does
not substitute a smooth distribution for the native count law. Those separate
operations retain their own normalization, coherence and precision obligations.
