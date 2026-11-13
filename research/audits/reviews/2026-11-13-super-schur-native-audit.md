# Fixed-Durfee Kronecker computation by supersymmetric specialization

2026-11-13. Independent algebraic and BIT audit. Fresh STATE/TRAPS and the
actual retained Panova 2502.20253v2, section 7.5 (physical LF1065--1072),
were read. The parent owns the corpus, literature and finite-control checks.
No network, API, Git, subagent or numerical control was used here.

**Disposition:** the proposed mechanism is sound for FIXED Durfee bounds
d,e and NUMERICAL n. It gives an exact deterministic polynomial-BIT
algorithm for g(lambda,mu,nu), with d(lambda)<=d, d(mu)<=e and arbitrary
nu partitioning n. The proof below supplies injectivity, an integer
triangular extraction, and a conservative explicit clock. No growing-d/e,
polynomial-log(n), full ratio-promise, priority or novelty claim follows.

Panova's actual section 7.5 says that even hook nu and fixed Durfee bounds
on lambda,mu did not have a clear efficient computation there. Section 7.6
explicitly distinguishes that paper's unary/numerical-n convention from
binary input. That motivates checking this proof and its provenance; an
open-problem label is not itself a mathematical obstruction to the argument.

## 1. The formal identity and its signs

For d even variables x=(x_1,...,x_d) and d odd variables y=(y_1,...,y_d),
define the symmetric-function specialization

    p_r(X)=sum_i x_i^r+(-1)^(r-1)sum_i y_i^r,
    hs_alpha(X)=s_alpha specialized by this rule.

Use Z=(u_1,...,u_e | v_1,...,v_e). The tensor alphabet has even letters
    x_i u_j, y_i v_j
and odd letters
    x_i v_j, y_i u_j.
There are 2de letters of each parity, and direct multiplication verifies

    p_r(X tensor Z)=p_r(X)p_r(Z).                         (1)

In particular the odd-times-odd sign is +1 for every r. The standard
internal-coproduct identity, applied by ring homomorphisms, therefore gives

    hs_nu(X tensor Z)
       =sum_(alpha,beta partition n) g(alpha,beta,nu)
                                      hs_alpha(X)hs_beta(Z).           (2)

For completeness, (2) follows by substituting (1) into the Frobenius formula
s_nu=sum_rho chi_nu(rho)p_rho/z_rho, then using
p_rho=sum_alpha chi_alpha(rho)s_alpha. The coefficient is the character
inner product defining g. These possibly exponential sums prove an identity;
THE ALGORITHM DOES NOT ENUMERATE THEM or compute these characters.

## 2. Elementary hook vanishing and unit-leading-monomial injection

The generating series for complete functions is

    sum_(r>=0) h_r(X)t^r=product_j(1+y_j t)/product_i(1-x_i t).          (3)

Jacobi--Trudi and Cauchy--Binet for the product of the two complete-function
Toeplitz matrices give

    hs_alpha(x|y)=sum_(rho subset alpha)
                         s_rho(x) s_(alpha'/rho')(y).                 (4)

This is also an elementary construction of supertableaux: the x boxes form
rho, ordinary semistandard in rows/columns, and transposing the remaining
skew tableau gives y entries weak down columns and strict along rows.
All entries are drawn from x_1<...<x_d<y_1<...<y_d. Formula (4) is used to
prove positivity and leading terms only, not as an exponential algorithm.

If alpha_(d+1)>d, every nonzero s_rho(x) has at most d rows. The skew shape
alpha'/rho' then has a column of length alpha_(d+1)>d, so its semistandard
tableaux in d y letters do not exist. Thus hs_alpha=0 outside the (d,d) hook.
This hook condition alpha_(d+1)<=d is exactly Durfee(alpha)<=d.

Now suppose alpha is in that hook, pad it by zeros, and put

    a=(alpha_1,...,alpha_d),
    tau=(max(alpha'_1-d,0),...,max(alpha'_d-d,0)).

Order monomials lexicographically with x_1>...>x_d>y_1>...>y_d.
An ordinary s_rho in d variables has leading monomial x^rho, coefficient
one: the lex-maximal tableau fills its i-th row by i. Among rho subset alpha
with at most d rows, the unique lex-maximal choice is rho=(alpha_1,...,alpha_d).
For this choice the nonempty rows of alpha'/rho' all start in column d+1;
translation identifies the skew shape with the ordinary partition tau.
Hence

    LM(hs_alpha)=x_1^(alpha_1)...x_d^(alpha_d)
                       y_1^(tau_1)...y_d^(tau_d),
    leading coefficient = 1.                            (5)

No other term in (4) can have the same x exponents. The vector (a,tau)
determines alpha: append the rows of tau' below its first d rows. Its
compatibility condition is alpha_d>=length(tau), with the empty-tail case
included. Thus (5) is injective, and the nonzero hook Schur polynomials are
linearly independent. The same proof applies to the e-hook alphabet Z.

Products hs_alpha(X)hs_beta(Z) have distinct unit leading monomials in the
disjoint 2d+2e variables. Consequently (2) retains EACH desired Kronecker
coefficient separately; it does not merely aggregate indistinguishable
representations. There is no missing inverse-character oracle.

## 3. Polynomial data size and a concrete evaluation/interpolation compiler

Set R=2d+2e and M=(n+1)^R. There are at most (n+1)^(2d) d-hook partitions
of n, since (a,tau) has 2d entries in [0,n]; similarly for e. All admissible
pairs therefore number at most M. Enumerating these arrays and checking
partition order, compatibility and total size is polynomial for fixed d,e.

The polynomial F=hs_nu(X tensor Z) has bidegree (n,n) in the two variable
groups. Every individual exponent is at most n, so its dense coefficient
array has at most M entries. Each product basis polynomial has the same
degree bound. There is no exponential-size intermediate alphabet: its
4de tensor letters are explicit bilinear monomials in the R variables.

Here is one fully finite compiler, avoiding assumptions about symbolic
polynomial division. Evaluate a required polynomial on the grid
{0,...,n}^r, with r<=R. At a grid point, compute h_0,...,h_n from (3), or
the tensor version of (3), by truncated power-series multiplication. All
letter values are nonnegative integers of magnitude <=n^2. The determinant

    hs_alpha=det(h_(alpha_i-i+j))_(1<=i,j<=length(alpha))               (6)

has order at most n. Set h_0=1 and h_s=0 for s<0. Its largest required
positive index is alpha_1+length(alpha)-1<=n. A pivoted fraction-free
integer determinant algorithm handles singular evaluations as well.

There are only a fixed number of even/odd letters. Each h_s evaluation has
O_(d,e)(n log(n+1)) bits, by bounding the number of monomial choices times
(n^2)^s. Every determinant minor has O_(d,e)(n^2 log(n+1)) bits by the
Leibniz or Hadamard bound. Fraction-free pivoting therefore uses polynomial
bit length throughout, not only a polynomial count of arithmetic operations.

Interpolate independently in each variable, or use the explicit tensor
Lagrange formula. The univariate cardinal polynomial at i has denominator
i!(n-i)!, dividing n!, and numerator product_(0<=j<=n,j!=i)(z-j).
All interpolation denominators thus divide (n!)^r. Numerator coefficient
bits, evaluation bits and their sum over at most M grid points remain
O_(d,e)(n^2 log(n+1)). Exact rational interpolation then recovers the
integer coefficients. This permits cancellations without uncharged
precision, a root oracle, or a numerical condition-number assumption.

Using schoolbook integer arithmetic, naive dense interpolation and no fast
determinant optimization, one such polynomial costs at most
    C_(d,e) M^2 (n+1)^10
bit operations. This deliberately loose bound includes all evaluations,
minor arithmetic, interpolation products and denominator cancellations.

## 4. Exact triangular extraction and complete BIT bound

Compute F by section 3 and set the residual T=F. Use lexicographic order
x_1>...>x_d>y_1>...>y_d>u_1>...>u_e>v_1>...>v_e. While T is nonzero:

1. Read its leading monomial. By (2) and (5), its exponent blocks decode
   a unique admissible pair (alpha,beta) in the two hooks.
2. Let c be that leading coefficient. Compute hs_alpha(X), hs_beta(Z)
   by (3), (6), and the finite compiler above, then form their product.
3. Record c=g(alpha,beta,nu) and replace
       T <- T-c hs_alpha(X)hs_beta(Z).

Why this terminates correctly: in the residual expansion (2), choose the
largest leading monomial among the remaining nonzero basis coefficients.
Distinctness and unit leading coefficients imply that this is precisely
the observed leading monomial and its coefficient is precisely c. Subtraction
removes one basis element. Induction proves every step, at most M steps.
An unrecorded target pair has coefficient zero. No exponentially long
subtraction cascade or enumeration of all partitions of n is hidden here.

For a particularly simple coefficient-growth bound, all hs polynomials
have nonnegative tableau coefficients and g>=0. The number of fillings of
n boxes by the tensor alphabet is at most (4de)^n, so ||F||_1<=(4de)^n.
At every extraction step the residual is the sum of the remaining positive
basis terms; all its coefficients and each removed term are bounded by
this same number. Each basis factor has coefficient sum at most (2d)^n
or (2e)^n. Thus the actual peeling uses O_(d,e)(n) coefficient bits.
The larger polynomial bit bound in section 3 already pays its exact
interpolation intermediates. No cancellation-growth assumption is needed.

There are at most M polynomial compilations up to a factor two, and dense
products/subtractions have polynomial size. For example the entire
algorithm is bounded by

    C_(d,e) (n+1)^(3R+12)
      = C_(d,e) (n+1)^(6(d+e)+12)                        (7)

BIT operations, with polynomial storage. The exponent is intentionally
unoptimized. Input partitions, their conjugates and numerical n are read
explicitly; no black-box character, Schur expansion or Kronecker operation
is supplied. The output is exact. In particular arbitrary nu is handled
by its own size-at-most-n determinant, rather than by an enumerated Schur sum.

## 5. Boundaries of the conclusion

The proof is uniform over all n and all supplied partitions meeting the
two FIXED Durfee bounds. It remains valid when some bounds exceed the
actual Durfee size. For n=0 the sole coefficient is one. For nonmatching
partition sizes the coefficient is zero. Positive d,e are fixed constants.

The exponent in (7) grows with d+e. Therefore this is not a polynomial
algorithm for growing Durfee bounds, unrestricted Kronecker computation,
or binary-n succinct partitions. It does not settle the full ratio promise
in the surrounding quantum comparison. The primary open-problem passage
and the elementary argument should be reconciled by the parent's source
and priority review; neither a finite Sage control nor this note alone
establishes novelty. No algebraic or bit-complexity gap remains in the
specific fixed-Durfee, numerical-n mechanism proved above.
