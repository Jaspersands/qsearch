# Mersenne Completion Moments

2026-10-29. Written specialization, independently reviewed by an automated
reasoning agent. Not formal verification, human peer review, a novelty
claim, a native completion algorithm, or a quantum advantage result.

## 1. Fixed Problem And Attribution

Keep the [original native relation](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md):
odd prime n>=17, q=2^n, N=n^2=8K+1, s=floor((n-3)/4),
f_s(x)=Tr(inv0(x)^(2^s-1)), distinct arbitrary public alpha_i, arbitrary
target bits b_i, and H[j,i]=alpha_i^j for 0<=j<K. No new exponent,
favorable point layout, planted witness, or altered verification relation.

The central inequality below is **prior art**, not a new general theorem:
[Horinaga--Yamakawa, Theorem 3.1](https://arxiv.org/pdf/2607.14650v2)
is the MDS Brascamp--Lieb inequality. We apply it to exact-support shortened
codes and the existing second/fourth moments of this particular family.
The uniform 2K+1 threshold needs only Parseval and a maximum coefficient
bound; the fourth moment sharpens the average-syndrome result.

For M remaining coordinates, K<M<=N, write t=M-K. Let Z_y count accepted
remaining assignments with syndrome y. Put

    mu=q^t/2^M, g_y=Z_y/mu, E_(uniform y) g_y=1.

The normalized Fourier transform of an accepted local fiber satisfies

    r_i(0)=1;
    r_i(u)=(-1)^b_i W(u)/q for u!=0;
    sum_(u!=0) |r_i(u)|^2=1;
    sum_(u!=0) |r_i(u)|^4 <= A=Delta/q;
    max_(u!=0)|r_i(u)| <= beta.

Here Delta=14 when n-4s=3, and Delta=30 when n-4s=5. These are inherited
from the [local access audit](MERSENNE_CLASSICAL_ACCESS_AUDIT.md), not
inferred from numerical spectra. The exact rational implementation takes
beta=(1+2^s*ceil(sqrt(q)))/q and can tighten A to min(A,beta^2).
For asymptotic displays below, A denotes Delta/q without that tightening.

## 2. Support-Wise Bound

The residual dual is the [M,K] evaluation code on the ORIGINAL remaining
points. A nonzero word has support size w>=t+1. Fix a support S of size w.
Words zero outside S form a shortened [w,d] MDS code, d=w-t: factor their
polynomial by product_(j notin S)(X-alpha_j). On S the remaining polynomial
has degree <d and nonzero coordinate multipliers. Every d-coordinate
projection is bijective. Put each active function h_i(0)=0 so that the
sum over this shortened code counts exactly this support, without leakage
from smaller supports.

For nonnegative h_i and p=w/d, the MDS inequality gives

    sum_v product_i h_i(v_i) <= product_i (sum_a h_i(a)^p)^(d/w).  (1)

An elementary verification applies Holder to all d-element subsets I.
Write the product of h_i as the geometric mean of the functions
product_(i in I) h_i^(w/d). Each corresponding sum factors by the
bijective projection. Each coordinate occurs in a d/w fraction of the
subsets. There is no extra factor q^d.

Applying (1) to |r_i|^2 and interpolating moments gives a bound for this
support's contribution to the variance:

    B2(w) = A^t,                              w>=2t;
          = A^(w-t)*beta^(2*(2t-w)),            t<w<2t.          (2)

For the absolute Fourier mass, interpolation between second and fourth
moments, then between the fourth moment and the maximum, gives

    B1(w) = A^(w-t)*beta^(4t-3w),              t<w<4t/3;
          = A^((2t-w)/2),                      4t/3<=w<=2t;
          = q^((w-2t)/2),                      w>2t.            (3)

The final line follows from the second moment and the number of field
elements. Fractional powers in (3) are rounded UP rationally by the code.
Parseval and the maximum alone also give B1(w)<=beta^(2t-w) for w<=2t.
Take the minimum with the elementary support bounds

    B2(w) <= beta^(2t), (q^(w-t)-1)*beta^(2w);
    B1(w) <= (q^(w-t)-1)*beta^w.

Orthogonality and the triangle inequality now give

    V_M=E_y (g_y-1)^2
       =sum_(v in dual,v!=0) product_i |r_i(v_i)|^2
       <= sum_(w=t+1)^M binom(M,w)*B2(w);                       (4)
    sup_y |g_y-1| <= eta_M
       :=sum_(w=t+1)^M binom(M,w)*B1(w).                        (5)

Targets and syndromes contribute signs, so the same bounds hold for EVERY
target pattern and arbitrary distinct evaluation points. The executable
certificate also takes the minimum with the older MDS count bound.

## 3. Every Accepted Three-Quarter Prefix Extends

When M>=2K, use only the Parseval maximum bound in (5), putting j=M-w:

    eta_M <= sum_(j=0)^(K-1) binom(M,j)*beta^(M-2K+j)
           <= beta^(M-2K)*(1+beta)^M.                          (6)

For all canonical n>=17, beta<(5/8)*2^(-n/4)<1/30.
At M0=2K+1=(n^2+3)/4, M0*beta<5/2: the upper envelope
(5/32)*(n^2+3)*2^(-n/4) is decreasing for real n>=17, and is below
5/2 at n=17. Consequently

    eta_M0 < exp(5/2)/30 < 1.

The envelope in (6) decreases with M since beta*(1+beta)<1.
Therefore **every syndrome has an accepted completion whenever M>=2K+1**.
Any accepted fixed assignment on at most N-(2K+1)=6K coordinates extends.
This improves the earlier 4K-residual sufficient condition, but is an
existence/count statement. No universal M=2K conclusion is asserted.

## 4. Typical Syndromes Near The Entropy Floor

Since beta<=q^(-1/4), (2) implies B2(w)<=A^(w/2) for t<w<2t.
When M*sqrt(A)<1, bounding binomial coefficients by M^w yields

    V_M <= 2^M*A^t + (M*sqrt(A))^(t+1)/(1-M*sqrt(A)).           (7)

For any fixed epsilon>0 and t=ceil((1+epsilon)*K/n), (7) is
2^(-Omega(K)) as n grows. This approaches the counting threshold's leading
constant. It is NOT the first K+O(K/n) residual bound: the previous
maximum/Parseval estimate already gives that order with a worse constant.

Integer counts impose a genuine lower bound independent of this proof:
Z_y^2>=Z_y implies

    V_M >= max(0,1/mu-1), mu=2^((n-1)t-K).                    (8)

Thus near-uniform nonzero counts require roughly (n-1)t>=K. This is
an information/counting constraint, not a computational lower bound.

There is also a scoped transfer to prefixes. Let F=N-M>K and sample F
independent uniform accepted roots. Their syndrome density relative to
uniform is at most 1+eta_F, using the old uniform MDS bound if convenient.
Under this proposal nu, put G=g_residual(syndrome). Then E_nu G=g_full
lies in [1-eta_N,1+eta_N]. The actual uniform-native prefix law is nu*G/E G.
Cauchy--Schwarz gives

    TV(native prefix, independent accepted prefix)
       <= sqrt((1+eta_F)*V_M)/(2*(1-eta_N));                    (9)
    Pr_(independent prefix)[no completion] <= (1+eta_F)*V_M.  (10)

Equations (9)-(10) are analytic deductions, not implemented conditional
samplers. Small probability of an empty fiber does not produce its witness.

## 5. Exact Certificates And Remaining Blocker

`theorems/mersenne_global_structure.py` uses integer/Fraction arithmetic;
outward square roots avoid floating-point underestimation. Its canonical
wrapper supplies the proved local premises; its generic MDS interface
explicitly ASSUMES them and does not certify an arbitrary input code.

The live report records conservative exponents U meaning bound<=2^U.
At M=K+ceil(4K/n), the variance bounds are at most 2^-63, 2^-211,
and 2^-878 for n=17,31,61 respectively. Uniform-syndrome count control
at those lengths is not established by these estimates. At M=2K+1,
all-syndrome nonemptiness is established. Finite F8/F32 controls independently
compute exact primal counts and dual Parseval sums for both target patterns;
they do not execute a native n>=17 completion algorithm.

Replay:

```sh
python -m theorems.mersenne_global_structure --output research/classical_baselines/mersenne_global_structure.json
python -m pytest -q tests/test_mersenne_global_structure.py -W error
```

**BLOCKER UNCHANGED:** a uniformly sampled codeword in the residual affine
code satisfies all M local constraints with probability approximately 2^-M.
The existing systematic accepted-root proposal still pays approximately
2^-K for its K forced symbols. Enumerating the t free field symbols near
the entropy floor still costs q^t=2^Theta(n^2). The better count bound is
not an evaluation of conditional counts and does not evade either cost.
It also does not move the complete quantum receiver's Johnson list-decoding
radius: that receiver still needs its separate M>=4K analysis. A concrete
residual solver, final-Fourier sampler, or useful reduction remains needed.
