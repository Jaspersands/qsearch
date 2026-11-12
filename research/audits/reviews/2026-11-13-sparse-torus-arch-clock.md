# 2026-11-13 — Certified sparse-torus archimedean rows

Independent scope: GENERAL_SPARSE_CONSTANTS_ATTACK §1 and the advisory
2026-11-13-sparse-torus-clock report. ACCEPT the archimedean compiler below,
with an explicit polynomial precision schedule and a fixed stopping rule.
No finite-place compiler, torsion-phase step, fullRel algorithm, implementation,
or advantage follows. Parent shared notes were not edited.

Source checked: Mehlhorn–Sagraloff–Wang, arXiv:1301.4870v2, retained as
`audits/sources/sparse_torus_arch/mehlhorn_sagraloff_wang.txt`. Physical LF lines
299–311 state the approximation-oracle cost assumption; 380–418 give Pan's
approximate factorization and Corollary 1. Corollary 1, unlike Theorem 3
(968–970) and its Theorem 4 refinement (1016ff), does NOT require a supplied
number of distinct roots. We apply Corollary 1 to an explicit finite dyadic
polynomial, at one prescribed precision, then independently certify disks.
There is no adaptive isolation call that can hang on a bad sample.

## 1. Native bounds, independently checked

Let n=delta>=1, F=Q(T)[Y]/f, f monic irreducible of degree n, and u_1,...,u_k
nonzero representatives of Y-degree<n. All sparse coefficient polynomials
have integer coefficients after clearing their rational scalar denominators.
Write L_d for the number of coefficient denominator polynomials, and take
integers b>=1, beta>=1 such that

    H=2^b >= product_P max(2, ||P||_1),
    d0=(L_d+1) beta,

where beta bounds total T-degree. Every coefficient is p/D with numerator
and common denominator norms <=H and degrees <=d0. These common products
are evaluation circuits; their expansions are not constructed. Put

    U=[2(n+1)(d0+1)H]^(2n+4),  e0=(n+1)d0,  V=n! U^n.

For the companion matrix C=A/D, every entry of A has norm<=H and degree<=d0.
For h>=1, an entry of A^h has norm<=n^(h-1)H^h. Summing at most n such powers
with the coefficient numerators and the necessary powers of D gives

    M(u_i)=A_i/D^n,             M(f_Y)=J/D^(n-1),
    M((u_i)_Tj)=T_ji/D^(n+1),  M(f_Tj)=F_j/D^(n+1),
    M((u_i)_Y)=Y_i/D^(n-1).

The coefficient derivative numerator p'D-pD' has norm<=2d0 H^2 and degree
<=2d0. Thus every displayed numerator entry has norm<=U and degree<=e0.
For example A_i has degree<=n d0, J and Y_i have degree<=(n-1)d0, and T_ji,F_j
have degree<=(n+1)d0. The bounds include the coefficient n in f_Y. Determinant
and adjugate norms are <=n!U^n=V by the permutation formula. No sparse
polynomial multiplication or identity test is needed to obtain these bounds.

The q=k+2 protected polynomials

    Pset={D, det J, det A_1,...,det A_k}

are nonzero integer polynomials, have norm<=V and total degree<=Delta=n e0.
Invertibility of f_Y and u_i in F proves their nonvanishing. For n=1, J=1;
constant protected polynomials are allowed and have modulus at least one.
All logarithms of the displayed bounds are polynomial in the native bits,
including log beta. Numerical T-degree is never a runtime parameter.

## 2. A finite grid with constant good probability

All logarithms in the parameter definitions below are base 2. Let

    ell=ceil(log2(n+1)),  v=ceil(log2 V),  q=k+2,
    t=16q(v+1)+4,
    N=t+v+ceil(log2(max(1,Delta)))+4.

Draw independent uniform N-bit integers for the coordinates of phi, divide
by 2^N, and put z_j=exp(2pi i phi_j). Define GOOD by

    |P(z)| >= 2^-t  for every P in Pset.

Then Pr(GOOD)>=15/16. Here is the full transfer argument. For any nonzero
integer polynomial P, its logarithm is integrable on the torus and its
logarithmic Mahler measure is nonnegative. Iterated univariate Jensen proves
both facts: the inner negative-log integral is at most
ln||P||_1-ln|leading_coefficient|, and induction makes that majorant integrable.
Consequently E ln^-|P|<=ln||P||_1<=v ln2, and

    Pr_cont(|P|<2^(1-t)) <= v/(t-1).

Couple a grid point with a uniform displacement in its N-bit cell. Since
P has total degree<=Delta,

    |P(z_grid)-P(z_cont)| <= 2pi Delta V 2^-N < 2^-t.

There is no additional factor s: the sum of the exponents in each monomial
is bounded by total degree. A grid failure implies the continuous event
above. The union bound is qv/(t-1)<1/16. Constant P need no tail argument.
For s=0 every protected polynomial is a nonzero integer and GOOD is certain.
The log Delta term is essential to prevent root-of-unity grid aliasing.

## 3. Every-branch conditioning and explicit precision

Fix a requested original-row error 2^-p, p>=1. Use the following integers:

    h=b+t+1,                 R=2^h,              W=4R=2^(h+2),
    T=n h+ell,
    L_u=t+n^2 b+(n-1)T+2,
    S_sep=t+n(n-1)(b+h+1)+4,  sigma=2^-S_sep,
    J_lip=n(h+2)+2ell+2,
    a=p+L_u+J_lip+S_sep+2n+20,  r=2^-a,
    c=a+(n-1)(S_sep+2),
    Facc=c+n(h+2)+12,         Znorm=h+ell+3,
    b_fac=Facc+Znorm+10+n ell,
    P_f=Facc+ell+10,
    P_u=p+L_u+ell+n(h+2)+20,
    P=max(P_f,P_u).

All these precisions are polynomial in native input size and p. There is no
assertion that the advisory's smaller delta^3 expression is the best bound.
The larger explicit constants here suffice uniformly, with growing n.

On GOOD, every coefficient of f and u_i has modulus<=H2^t=R/2. Cauchy's
bound gives |y_j|<=R for every root. Hence |u_i(y_j)|<=n R^n<=2^T. Moreover

    product_j u_i(y_j)=det A_i(z)/D(z)^(n^2),
    |product_j u_i(y_j)|>=2^(-t-n^2 b).

Dividing by the upper bounds for the other n-1 branches gives

    |u_i(y_j)| >= 4*2^-L_u  for every i,j.

Likewise |disc f_z|=|det J(z)/D(z)^(n(n-1))|>=2^(-t-n(n-1)b).
If n>=2, isolate one squared difference in the discriminant product and
bound every other difference by 2R. This proves every root separation is
at least sigma. For n=1 there is no separation condition; the same artificial
sigma and formulas can harmlessly be used. Thus the norm argument supplies
every-branch bounds only after the Cauchy upper bounds are included.

## 4. Pay the native coefficient oracle before factorization

The following evaluation procedure needs no exact cyclotomic arithmetic.
For each original monomial T^alpha compute alpha dot phi modulo 1 exactly
using the binary exponents and the N-bit residues. Approximate the resulting
unit complex exponential to the requested absolute accuracy. This costs
polynomially in the precision, N and the native exponent bit lengths.
For clarity, such certified elementary evaluation can be implemented with
Machin's formula for pi and the exponential Taylor series: for q-bit output,
q+20 terms in each arctangent series and 64(q+20) exponential terms
more than suffice for arguments of modulus at most 7. Evaluate these rational
series exactly before final dyadic rounding. Factorial/geometric remainder
bounds certify the output in polynomial bits, without accumulated rounding.

One conservative propagation allowance is

    E_nat=(L_d+3)(b+2)+ceil(log2(L_d+3))+8.

To evaluate any common numerator p or D within 2^-Q, approximate every
original monomial within 2^(-Q-E_nat), sum each original sparse polynomial
exactly, and form its at most L_d+1 common-denominator factors exactly as
dyadic numbers. Telescoping gives error at most

    (L_d+1) H (2H)^L_d 2^(-Q-E_nat) <= 2^-Q.

The intermediate bit sizes grow polynomially; exact dyadic multiplication
avoids any uncharged rounding cascade. No common product is expanded in T.

First evaluate D within 2^(-t-8). ABORT unless its approximation has modulus
at least 3*2^(-t-2), checked by an exact rational squared-modulus comparison.
Passing proves |D(z)|>2^(-t-1); GOOD always passes. Therefore on every sample
that proceeds, all true f/u coefficients have modulus<=R.

To produce absolute coefficient error 2^-P, evaluate p,D within 2^-Q with

    Q=P+b+2t+10,

perform exact rational complex division, and round real and imaginary parts
to P+3 fractional bits. The division sensitivity is bounded by
2^(b+2t+5)2^-Q; together with rounding it is less than 2^-P. Thus the largest
native monomial accuracy needed is Q+E_nat, a specified polynomial integer.
This produces an explicit monic dyadic polynomial ftilde and dyadic utilde_i.
Its leading coefficient is exactly one, not a numerical approximation.

## 5. Fixed factorization and independent acceptance certificate

We have ||ftilde||_1<=2^Znorm and all its roots have modulus<=W. For n>=2
apply actual Corollary 1 at the single prescribed b_fac above to this EXPLICIT
finite dyadic polynomial. Its internal approximation queries are answered
by rounding its stored coefficients; their cost is polynomial and does not
make new requests to the native rational-function oracle. The source gives
dyadic centers zhat_j and the monic polynomial qhat=product_j(Y-zhat_j), with

    ||ftilde-qhat||_1 <= 2^(-Facc-10).

Here b_fac>=n log2 n, and the source bit cost is
O-tilde(n^2(h+2)+n b_fac), in addition to the explicitly paid input formation.
The centers have polynomial bit sizes. For n=1 take zhat_1=-ftilde_0 and
qhat=ftilde directly; this avoids the source's degree>=2 convention.

Run these finite rational acceptance tests, regardless of GOOD:

1. All centers have |zhat_j|<=2R, and every pair is at distance>=sigma/2.
   Use exact squared-modulus comparisons. Our constants give r<=sigma/16.
2. Form qhat exactly (dense in Y only), and set

       e_f=sum_{h<n} (|Re(ftilde_h-qhat_h)|+|Im(ftilde_h-qhat_h)|)
                     + n*2^-P.

   Require W^n e_f < 2^(-c-2).
3. For each i,j compute v_ij=utilde_i(zhat_j) exactly. Require
   |v_ij|>=2^-L_u. The error allowance is

       e_u=n*2^-P W^(n-1)+2^J_lip r <= 2^(-L_u-p-6).

   This last inequality follows from the fixed constants and can also be
   checked as a rational inequality. Otherwise ABORT.

Soundness is unconditional. On |Y-zhat_j|=r all other factors of qhat have
modulus at least sigma/4, so |qhat(Y)|>=r(sigma/4)^(n-1)=2^-c.
The circle is inside |Y|<=W, where |f_z-qhat|<=W^n e_f. Rouché puts exactly
one root of f_z, counted with multiplicity, in each of the n disjoint disks.
Thus all roots are present and simple. Notice the candidate-center bound is
2R, not R; the true Cauchy bound alone would not justify the latter test.

After the denominator precheck, coefficients of u_i have modulus<=R, so
|u_i'(Y)|<=2^J_lip on |Y|<=W. The coefficient-evaluation and root-disk errors
therefore give |u_i(y_j)-v_ij|<=e_u. The value test certifies nonvanishing and
relative error at most 2^(-p-6); consequently the logarithm changes by less
than 2^(-p-5). Compute ln|v_ij| to absolute error 2^(-p-2) and output it.
The final error is less than 2^-p.

This logarithm has a finite explicit clock. We have
2^-L_u<=|v_ij|<=2^(n(h+2)+ell+1). For the positive rational w=|v_ij|^2,
find the integer j with w/2^j in [1,2) by binary comparisons. Use
ln x=2 sum_{l>=0} ((x-1)/(x+1))^(2l+1)/(2l+1) on that interval, and the same
series for ln 2. A number of terms

    p+ceil(log2(2L_u+2n(h+2)+2ell+10))+10

suffices also for multiplication by j and division by 2. Rational arithmetic
and geometric remainder bounds give the asserted log error in polynomial bits.

Completeness on GOOD also has a direct proof, independent of root-isolation
claims. The true and approximate polynomial satisfy

    ||f_z-qhat||_1<=2^(-Facc-9).

On a circle of radius r/8 about a true root, |f_z| is at least
(r/8)(sigma/4)^(n-1)=2^(-c-3), whereas the above coefficient error gives
|f_z-qhat|<=2^(-c-21). Rouché pairs all n centers with distinct true roots
within r/8. Hence the 2R and sigma/2 tests pass. The rational e_f test passes
with a margin of at least 18 bits. Finally |u_i(y_j)|>=4*2^-L_u, so every
value test passes. This covers n=1 with the empty products interpreted as 1.

Every trial has a polynomial clock, including bad samples. There is no test
of exact nonvanishing of a general computable complex number, no supplied
root-count oracle, and no loop that increases precision until success.
Only an entire accepted n-by-k matrix from one common z is returned.
Independent repetition max(1,ceil(log2(1/eta))+1) times gives ABORT probability
at most eta. Accepted rows are always correct; randomness affects completion
only. Corollary 1 is used as its stated algorithmic theorem, not an additional
random root-finder success assumption.

## 6. Joint constant embeddings and their exact multiplicity

Let C0 be the algebraic closure of Q in F and c0=[C0:Q]. At any ACCEPT point,
the implicit function theorem gives n distinct holomorphic root germs y_j(T)
at z. The fraction field of holomorphic germs contains Q(T) injectively:
T remains a varying germ, even when z itself is a tuple of roots of unity.
Since f is irreducible, sending Y to each root germ defines a Q(T)-embedding
of F; the n embeddings exhaust them all. When s=0 this is the ordinary list
of n number-field embeddings into C.

Every algebraic constant must map to a constant complex root of its minimal
polynomial. Thus each row determines ONE embedding sigma_j:C0->C, and

    product_i u_i(z,y_j)^e_i = sigma_j(product_i u_i^e_i)

simultaneously for EVERY e in Alg. Negative exponents are legitimate because
the acceptance certificate proves each u_i value nonzero. Each embedding
of C0 extends to exactly [F:C0(T)]=n/c0 of the n embeddings. The germ field
contains all f roots, so the usual extension count loses no embeddings.
Therefore the multiplicities are uniform, and for any function Phi,

    (1/n) sum_j Phi(ln|sigma_j(c)|)
      = (1/c0) sum_{sigma:C0->C} Phi(ln|sigma(c)|).

Taking Phi(x)=max(0,x) gives the archimedean contribution to the usual
logarithmic Weil height. Taking Phi(x)=|x| gives the weighted absolute-log
norm. These are different normalizations; the advisory's absolute-log
average is not literally the Weil-height archimedean contribution. Complex
embeddings occur twice per complex place, as required by the usual weights.
No constant-field construction, conjugate grouping or knowledge of c0 is
needed by the compiler.

For an Alg basis with original-coordinate entries bounded by Balg, multiply
the original row matrix by that integer basis. Errors are at most
k Balg 2^-p per resulting entry. Taking

    p >= p_target+ceil(log2(max(1,k Balg)))+3

pays this operation. One never evaluates enormous products u^e separately.
Correct computation of Alg remains its separate reviewed premise; correctness
of the original arch rows does not require an Alg oracle.

## Disposition

The actual primary Corollary 1 closes the report's root-approximation import.
The explicit schedule above closes its unspecified precision constant and
native-oracle clock; the original U,V bounds, grid probability, all-branch
conditioning and joint-embedding multiplicity survive independent checking.
The only normalization repair is to distinguish absolute logs from positive
parts when naming Weil height. This is a randomized polynomial sparse-BIT
compiler for certified archimedean rows with constant success and ABORT.
Arch rows still miss both nonconstant torus units and constants such as
(3+4i)/5; no finite-place or full relation theorem is inferred.
