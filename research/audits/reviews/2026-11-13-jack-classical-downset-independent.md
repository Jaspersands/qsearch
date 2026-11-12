# Classical Jack Born sampling on a partition down-set

13 November 2026. The completed 149-line advisory report was read in full.
The following is an unconditional classical algorithm at fixed alpha=3,
using the already source-checked one-box Pieri identity. Degree D is a
charged numerical parameter. No network, API, Git, or CAS sweep was used.
STATE/TRAPS and the retained primary formulas were checked; interpreter:
/opt/anaconda3/bin/python.

For a partition lambda of D, put

    S(lambda)={nu:nu subseteq lambda},    M=|S(lambda)|,
    H_nu=||J_nu||^2.

There is an exact expected-polynomial-time classical sampler for

    pi_lambda(mu)=theta_mu^2 z_mu 3^length(mu)/H_lambda,
    J_lambda=sum_mu theta_mu p_mu,

with cost poly(D)*M^2 on polynomial-bit integers. There is also a bounded
time sampler within TV error epsilon, costing poly(D,log(1/epsilon))*M^2.
This proves polynomial classical Born sampling for all bounded-Durfee
families. It is not a general polynomial sampler, a hardness result, or a
classical construction of the coherent coefficient state.

## 1. Exact derivative sampling identity

For homogeneous nonzero f of degree d, adjointness and Euler's identity give

    sum_(k=1)^d ||V_-k f||^2=3d||f||^2,
    V_-k=3k partial_(p_k),       V_k^dagger=V_-k.

Choose k with probability ||V_-k f||^2/(3d||f||^2), replace f by V_-k f,
and repeat until degree zero. Output the multiset of selected k's.
Zero-norm branches have probability zero and are excluded. Each selected
branch is nonzero; there are at most D selections.

Here is a direct proof of the output law. In the orthonormal power-sum
basis, V_-k takes |mu> to sqrt(3k*m_k(mu)) |mu-k>. For fixed k this map on
the supported basis labels is injective. The norm update therefore has
exactly the same distribution as first drawing mu from the Born law and
then repeatedly removing a part k with probability k*m_k(mu)/d. At the
end the recorded multiset is precisely that original mu. Equivalently,
the report's ordered-path telescoping proof gives the same law. Neither
argument assumes nonnegative Jack coefficients.

## 2. All required operators are computable inside S(lambda)

The hypothesis H_P in the report is now PAID:

    P J_nu:=V_1 J_nu=sum_s tau_(nu,s) J_(nu+s).

Actual sources: Mickler's follow-up Lemma 2.8, (43)--(44), and Stanley
Theorem 6.1 in the integral-Jack normalization; the weights agree with
Mickler--Moll (1.18). See also the independent Lax intertwiner review,
Section 1. No finite test is being substituted for Pieri.

Set E=sum_(b>=1) V_(b+1)V_-b. The source T3 formula and transfer eigenvalue
give

    [T3,V_1]=6E+6V_1,
    T3 J_nu=3(2 sum_(t in nu)c(t)+2|nu|)J_nu,
    E J_nu=sum_s c(s)tau_(nu,s)J_(nu+s),       c(x,y)=3x-y.

Also [E,V_k]=3k V_(k+1), so the raising matrices U_k for multiplication
by p_k are obtained by

    U_1=P,        U_(k+1)=(E U_k-U_k E)/(3k).                       (1)

Equivalently U_k=ad_E^(k-1)(P)/(3^(k-1)(k-1)!).

Restriction is exact. Every P/E word follows a chain of added boxes.
If its endpoints rho,kappa lie in S(lambda), every intermediate diagram
lies inside kappa and hence inside lambda. A path that leaves this down-set
cannot return. Thus the restricted recurrence gives the true coefficients
of p_k J_rho at every retained kappa; it also proves the containment support.

Adjointness then gives the lowering matrix

    [D_k]_(rho,kappa)=[U_k]_(kappa,rho) H_kappa/H_rho,
    D_k=diag(H)^(-1) U_k^T diag(H).                                (2)

It preserves the down-set. Starting with the vector e_lambda, compute
D_k f for every k<=d and their diagonal Hall norms, choose a branch by
Section 1, and retain its coefficient vector. Enumerating the down-set,
forming its one-box edges, and computing (1)--(2) uses polynomial work in
D and M. A safe, nonoptimized count is O(D^2 M^2) rational operations for
preprocessing and one complete sample: E is O(D)-sparse per row/column,
and there are at most D matrices, D selections, and D candidate k's.
No tight arithmetic-operation count from the report is needed.

## 3. An explicit polynomial-BIT bound

Assume D>=1; the empty partition is trivial. Define

    L=lcm(1,2,...,4D),          Q=L^(D^2+4D).

Computing L requires only integer gcd/lcm, not factoring. The elementary
bound log_2 L<=4D log_2(4D) suffices.

The ACTUAL norm formula, Stanley Theorem 5.8 / Mickler Proposition 3.1, is

    H_nu=prod_(b in nu) (3a(b)+l(b)+1)(3(a(b)+1)+l(b)).             (3)

Every factor is an integer in [1,4D]. Consequently H_nu divides L^(2D)
and 1<=H_nu<=(4D)^(2D). We do not compute norms by inverting the report's
path-DP quantity T_nu.

Every Pieri denominator is a product of at most D nonzero integer corner
differences, each of absolute value at most 4D. Thus P and E entries have
denominators dividing L^D. Since tau>=0 and sum_s tau=1 before restriction,

    ||P||_1<=1,       ||E||_1<=3D.

Induction in (1) gives

    denom(U_k) divides L^((D+2)k),
    ||U_k||_1 <= (2D)^(k-1)/(k-1)!.                               (4)

For the denominator claim, one multiplication by E adds exponent D and
division by 3k adds at most two more, since both 3 and k divide L.
For the norm claim, (1) multiplies the preceding bound by at most 2D/k.
These bounds also control every intermediate commutator product and sum.

For a derivative history k_1,...,k_j of total removed degree m<=D, the
diagonal norm factors in (2) TELESCOPE. Its coefficient at nu is

    f_nu=(H_lambda/H_nu)
          (U_(k_1)...U_(k_j))_(lambda,nu).                         (5)

By (3)--(5), every f_nu has denominator dividing
L^((D+2)m+2D), hence dividing Q, and

    |f_nu| <= (4D)^(2D)(2D)^m <= (4D)^(3D).

The same bounds hold for EVERY candidate vector D_k f considered while
sampling, because its total removed degree is still at most D. Thus no
sequence of rational divisions can hide exponential intermediate height.

Writing f_nu=a_nu/Q, its Hall norm is

    ||f||^2=Q^(-2) sum_nu a_nu^2 H_nu.

There are M<=sum_(d=0)^D p(d)<=2^D summands. Numerators, denominators,
matrix entries, norms, and conditional probabilities therefore require
O(D^3 log(D+1)) bits. This is a proved coarse bound, replacing the report's
unsupported O(D^2.5)-bit estimate. Standard exact integer/rational
arithmetic makes the operation count in Section 2 polynomial BIT time.

## 4. Exact versus bounded-clock sampling

Clearing the common norm denominator gives exact nonnegative integer
transition weights with polynomial bit length. Uniform-integer rejection
sampling implements each transition exactly, with fewer than two expected
trials. This gives the exact expected-polynomial-time sampler.

A deterministic polynomial clock with TV guarantee is even simpler. At
each step use

    b=ceil(log_2(2D^2/epsilon))

fair bits to choose U uniformly from {0,...,2^b-1}/2^b and compare it with
the EXACT cumulative rational probabilities. Couple this to a continuous
uniform U before rounding. At most D cumulative boundaries can change the
choice, so conditional error is at most D/2^b. Over at most D adaptive
steps the total TV error is at most D^2/2^b<=epsilon. Empty intervals are
skipped, so a zero-norm branch is never selected. The bit count is
O(D(log D+log(1/epsilon))); arithmetic precision is the previous bound
plus O(log(1/epsilon)). Arbitrary rational probabilities cannot in general
be sampled exactly with a fixed finite number of fair bits, so these two
clock statements should remain distinct.

## 5. Shape scope and report corrections

If h is the Durfee-square size of lambda, every box of lambda lies in its
first h rows or first h columns. Recording those h row lengths and h column
heights determines any nu subseteq lambda. Hence

    M <= (D+1)^(2h).

All bounded-h families have polynomial classical Born samplers, including
hooks and bounded-row/column families. For h=(log D)^O(1), this algorithm
has a quasipolynomial upper bound. That DOES NOT exclude a possible
polynomial-versus-quasipolynomial quantum advantage. The report's asserted
requirement h=(log D)^omega(1) for ANY advantage is rejected. The correct
comparison is against poly(D)*M^O(1) on the actual target family; some
additional families can have small M without bounded h.

The general upper bound M<=sum_(d<=D)p(d)=exp(O(sqrt(D))) remains useful,
but its maximizing constant is irrelevant to this result. No general
sampler or hardness follows from the cost of this representation. The
degree-12/14 sweeps and worst-case-constant project recommended in the
report are unnecessary and are not queued. A polynomial native method
for the required derivative norms at unrestricted shapes would still
change the general comparison; this review supplies no such method.
