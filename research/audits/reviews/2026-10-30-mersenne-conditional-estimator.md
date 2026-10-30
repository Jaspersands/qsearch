# Native Mersenne Conditional Estimation: A Single-Term Variance Certificate

2026-10-30. Bounded mathematical audit. Independent automated review by Raman
completed for Sections 2-4 only: no fatal errors found; table rows and prefix
constants verified. Section 5 has NOT been independently reviewed. These are
written deductions and exact certificate arithmetic, not formal verification
or native sampler execution. **The conditional-sampling blocker is not removed.**

Tiny V_M makes the constant estimate 1 accurate on most syndromes. The lower
bound concerns only unbiased single-term estimation and its independent
arithmetic mean, not arbitrary count approximation.

The concrete result is an exponential LOWER bound for even the optimal
single-dual-character importance estimator, in a window where almost every
residual count is close to its mean. This is intrinsic variance of this
estimator class, not merely inability to sample its optimal proposal. A
complete-list construction below does efficiently estimate a smoothed count;
its exact Boolean Fourier multiplier identifies the information it loses.
Neither statement is a classical search-hardness claim.

## 1. Unchanged Problem And Prior Work

Keep n odd prime >=17, q=2^n, N=n^2=8K+1, K=(N-1)/8,
s=floor((n-3)/4), d=2^s-1, and f(x)=Tr(inv0(x)^d), including f(0)=0.
The original arbitrary distinct public alpha_i, arbitrary bits b_i, and
H[j,i]=alpha_i^j, 0<=j<K, are unchanged. No planted witness, favorable
point layout, replacement predicate, or field-sized input table is used.

Current notes and selectively searched prior work consulted: the AGENT_HANDOFF top,
[target](../../MERSENNE_RECIPROCAL_RESEARCH_TARGET.md),
[global Fourier access](../../MERSENNE_GLOBAL_FOURIER_ACCESS.md),
[completion moments](../../MERSENNE_COMPLETION_MOMENTS.md),
[local access](../../MERSENNE_CLASSICAL_ACCESS_AUDIT.md), and the
[earlier conditional-table audit](2026-10-30-noisy-phase-native-scope.md).
The q^h table / 2^(K-h) rejection tradeoff is not repeated as a new result.
Exact signed Walsh evaluation and approximate local sampling are already
polynomial WRITTEN constructions; neither is claimed executed at native size.

After fixing accepted prefix coordinates, let M=K+t remaining coordinates,
with the original K parity rows and prescribed residual syndrome y. Define

    Z_y = #{x : H_remaining x=y, f(x_i)=b_i for every remaining i},
    mu = q^t / 2^M,                 g_y = Z_y/mu,
    chi(z) = (-1)^Tr(z),            W(u) = sum_x (-1)^f(x) chi(ux),
    r_i(0)=1,                      r_i(u)=(-1)^b_i W(u)/q for u!=0.

Let v(lambda)=H_remaining^T lambda and D={v(lambda):lambda in F_q^K}.
The MDS property gives dim D=K and minimum nonzero weight t+1. Orthogonality
gives the exact expansion

    g_y = 1 + sum_(lambda!=0) a_lambda chi(lambda dot y),
    a_lambda = product_i r_i(v(lambda)_i).                       (1)

Targets and syndromes change signs, not |a_lambda|. Put

    L = sum_(lambda!=0) |a_lambda|,
    V_M = sum_(lambda!=0) |a_lambda|^2 = E_y (g_y-1)^2.            (2)

Uniform y in (2) is an averaging device, not a replacement input promise.

## 2. Exact Optimal Single-Term Second Moment

For any probability law p supported on every nonzero coefficient, sample
Lambda~p and return

    X = 1 + a_Lambda chi(Lambda dot y)/p_Lambda.

Then, exactly,

    E X = g_y,
    E (X-1)^2 = sum_(lambda!=0) |a_lambda|^2/p_lambda,
    Var X = sum |a_lambda|^2/p_lambda - (g_y-1)^2.                (3)

Cauchy-Schwarz shows that the minimum second moment is L^2, attained by
p_lambda=|a_lambda|/L. At that optimum X-1 takes values +L and -L.
If L=0, simply return 1. Thus the exact best relative variance, for g_y>0,
is

    R_opt(y) = (L^2-(g_y-1)^2)/g_y^2.                            (4)

The distinction between E(X-1)^2 and Var X matters. The independent
m-sample arithmetic mean has relative mean-square error R_opt(y)/m.
This is not a lower bound for every possible estimator or native sampler.

Sampling p and evaluating its normalizer L are additional algorithmic
requirements. The lower bound below GRANTS both for free. Approximate pi
sampling alone does not supply either a normalized dual p or its exact
likelihoods; total variation alone does not control unbounded importance
weights. However, those access issues are not needed for this obstruction.

## 3. A Positive-Fourier Minorant Gives An Actual Lower Bound

Set Q=ceil(sqrt(q)) and

    A = 2*d*Q+3,                    a=A/q,
    B_M = q^(-t)*(1+1/a)^M.

**Lemma. For every allowed point set and every target pattern,**

    L >= max(0,B_M-1).                                          (5)

Proof has three steps. None reverses an MDS upper bound.

First, define the normalized autocorrelation

    c(z)=q^(-1)*sum_x (-1)^(f(x)+f(x+z)).

For z!=0, the rational function x^(-d)+(x+z)^(-d) has two distinct poles,
each of odd order d. Its Artin-Schreier curve has genus d. Odd poles also
exclude the exceptional form R^2+R+constant. If S_z is the character sum
over x not in {0,z}, the smooth curve has q+2+S_z rational points: one
above each pole and two above infinity, where the right-hand side is zero.
Hasse-Weil therefore gives |S_z+1|<=2*d*sqrt(q). Restoring the ACTUAL native
zero convention adds 2*(-1)^f(z), so

    |c(z)| <= (2*d*sqrt(q)+3)/q <= a.                            (6)

The imported genus/Weil ingredients are
[Carmon, Theorem 3.1 and equation (3.6)](https://arxiv.org/html/1409.3694v1#S3).
The pole restoration and subsequent minorant argument are deductions here,
not claims quoted from that paper. No curve is constructed or point-counted.

Second, put pi(u)=W(u)^2/q^2. Balance and Parseval give pi(0)=0,
sum pi=1, and its UNNORMALIZED additive Fourier transform is c(z).
The existing single-pole-plus-linear Walsh bound is
|W(u)|/q<=beta=(1+2^s*Q)/q<=a: its numerator is at most A since s>=3.
Define

    h(u) = [u=0] + pi(u)/a.

For every coordinate, 0<=h(u)<=|r_i(u)|, including u=0. Moreover

    h_hat(z)=sum_u h(u)chi(uz)=1+c(z)/a >=0,
    h_hat(0)=1+1/a.                                             (7)

The z=0 case uses c(0)=1, separately from (6).

Third, let E=D^perp=ker H_remaining, of dimension t. Poisson summation
and (7) give

    1+L = sum_(v in D) product_i |r_i(v_i)|
         >= sum_(v in D) product_i h(v_i)
          = q^(-t) sum_(x in E) product_i h_hat(x_i)
         >= q^(-t) h_hat(0)^M = B_M.

Every discarded summand is nonnegative. This proves (5) for arbitrary
public points; only the dimension enters this step.

## 4. Parameter Window And Exact Finite Certificates

For canonical n>=17,

    a*q^(1/4)
      <= 2^(1/4)*(1+2^(-n/2)) + 3*2^(-3n/4) < 5/4.

Consequently

    log2 B_M >= n*(K-3t)/4 - M*log2(5/4).                        (8)

For any fixed 0<epsilon<1/3 and t<=(1/3-epsilon)*K, this is Omega(nK).
The bound is useful when its right side is positive; no claim is made at
or beyond the uncertified endpoint. This overlaps the existing typical-count
window t=ceil((1+delta)*K/n), fixed delta>0, where V_M=2^-Omega(K).
For B_M>=1 and g_y in [1/2,3/2], equations (4)-(5) yield

    R_opt(y) >= (4/9)*((B_M-1)^2-1/4).                          (9)

Thus near-uniform counts and exponentially bad optimal importance variance
coexist. The cancellation is intrinsic to single-character estimation.

The following are exact rational certificates at t=ceil(4K/n). Bounds on
V_M were recomputed from the support-wise formula in Completion Moments,
not inferred from the lower bound. Lower powers for B_M were checked by
integer cross multiplication of (q+A)^M and q^t*A^M*2^e.

| n | K | t | M | A | B_M >= | L^2 >= | V_M <= |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | 36 | 9 | 45 | 5085 | 2^60 | 2^118 | 2^-63 |
| 31 | 120 | 16 | 136 | 11770617 | 2^526 | 2^1050 | 2^-211 |
| 61 | 465 | 31 | 496 | 49755179191503 | 2^5797 | 2^11592 | 2^-878 |

For each FIXED target and point set, at least a 1-4V_M fraction of uniform
syndromes has g_y in [1/2,3/2]. On that set the three relative-variance
lower bounds exceed 2^116, 2^1048, and 2^11590, respectively. An independent
arithmetic-mean estimator with relative RMS error rho therefore needs more
than those respective bounds divided by rho^2 samples, even with free p*.
These are variance/RMS statements, not unrestricted query lower bounds.

These syndromes are relevant to real prefixes. For F=N-M accepted prefix
coordinates, the prior all-syndrome theorem applies since F>=2K+1 here;
every residual y is reachable by some accepted prefix. With prefix-syndrome
density <=1+eta_F, independently sampled accepted prefixes miss the above
good-count set with probability <=4*(1+eta_F)*V_M. Under the actual uniform
native prefix law the corresponding bound is
6*(1+eta_F)*V_M/(1-eta_N): on |g-1|>1/2, E[g*1_bad]<=4V_M+2V_M.
This is not a planted or favorable-syndrome guarantee.

Removing J explicitly evaluated nonzero terms cannot change this conclusion
for polynomial J in this window: each |a_lambda|<=beta^(t+1), so the
remaining absolute mass is at least L-J*beta^(t+1). General grouped
cancellation or a different estimator is NOT excluded by this observation.

## 5. What Complete RS Lists Can Estimate Constructively

There is a polynomial-access estimator of a precise SMOOTHING of g, not
of g itself. This identifies rather than hides the remaining bias.

Keep y fixed and display the target as g_y(b). Solve H_remaining*x0=y and
use the translated local root states, with paid Fourier phases chi(u*x0_i).
Let psi_b be their product Fourier amplitude and

    B_w = {sigma in {0,1}^M : |sigma|<=w},
    tau_w=|B_w|/2^M,
    u_b(e)=[wt(e)<=w]*psi_b(e),
    k_w(z)=2^(-M)*sum_(sigma in B_w) (-1)^(sigma dot z).

Use a complete RS radius-w decoder with a public list bound P. Draw e
from |u_b|^2/tau_w, draw d0 uniformly from D, and set z=d0+e. Compute

    B(z)=sum_(d in List(z)) u_b(z-d),
    R(z)=sum_(d in List(z)) |u_b(z-d)|^2,
    alpha(z)=|B(z)|^2/(P*R(z)).

Retain signs and translation phases. With an ideal Bernoulli(alpha) coin
J, return T=P*J. The exact Gram/list identity gives

    E T = G_w(y,b)
        = sum_c k_w(b+c)^2*g_y(c)/tau_w,
    E T^2 = P*G_w(y,b),
    Var T = P*G_w(y,b)-G_w(y,b)^2.                              (10)

This has polynomial relative variance whenever G_w>=1/poly and P=poly.
Small tau_w is NOT by itself a source rejection cost: sample a uniform
mask in B_w directly using binomial counts and integer unranking, then
draw active labels from pi. This takes polynomial mask arithmetic even
when tau_w is exponentially small. It does not increase the decoder radius.
Approximate local pi sampling, exact signed Walsh calls, complete decoding,
and capped random-bit/ABORT costs remain charged. For a total one-trial
TV error delta, the bounded output changes the mean by at most P*delta.
The established local construction costs polynomial in 1/delta, not just
log(1/delta); exact ideal pi access is only used to state (10).
For example, allocate delta/(3M) per local label and delta/3 each to mask
and coin errors. The conservative per-trial Walsh work is
O(n^45*M^2*log(M/delta)/delta + P*M*n^45), plus complete decoding and
polynomial field/integer work. Use the explicit interpolation and extraction
budgets in [Binary GS Decoder](../../BINARY_GS_DECODER.md); the fixed-margin
O(M^3) field-operation interpolation bound is not asserted near the boundary.

Here is the exact bias/falsifier. On the Boolean target Fourier coefficient
indexed by a subset S, the smoothing multiplier is

    kappa_w(S)=|B_w intersect (B_w+1_S)|/|B_w|.                  (11)

It vanishes whenever |S|>2w. A uniform word in the affine residual code
has independent uniform values on any t coordinates, so the balanced
predicate bits have zero nonconstant moments through order t. Therefore
if 2w<=t, G_w(y,b)=1 IDENTICALLY for every y,b, regardless of the true
completion count. For w<M/2 the full-order target moment is always erased.
That moment is not identically zero as a function of y: choose a constant
nonzero dual polynomial v with W(v)!=0, whose contribution to its syndrome
Fourier coefficient is (W(v)/q)^M!=0. This works for any evaluation points.

The strict Johnson window w<M-sqrt(M*(K-1)) has w<M/2 whenever
M<=4*(K-1), covering the residual window above. Thus this particular
complete-list mass estimator cannot be inverted on all target moments
there, despite its positive sampling rule and good second moment.
It is not a proof against other RS-based regroupings or estimators.

A separate exact low-order falsifier: if (n-1)t<K, then mu<1, and for
every fixed target at least a 1-mu fraction of syndromes has Z_y=0.
Yet truncating the conditional predicate-moment expansion at any order
<=t gives 1 for all of them. Vanishing low-order moments alone therefore
cannot certify relative counts or sequential conditional probabilities.

## 6. Cost, Scope, And Decision

Computing the lower certificate B_M uses integers of O(nM) bits and
polynomial bit work; it requires no Walsh table or native execution. One
actual character coefficient uses M signed Walsh queries, O(MK) field
operations for v(lambda), and O(nM)-bit products. The inherited conservative
query cost is O(n^45) per Walsh value with reusable O(n^21) workspace.
Proposal construction and normalization are additional, even though the
variance certificate grants them for free.

The list estimator additionally pays its complete-decoder construction
and per-trial decoder cost, not just a list-size bound. Any ultimate native
output must still pass all N original predicates and all K parity equations;
schoolbook evaluation costs O(N*n^3+NK*n^2) bit operations, besides input
validation. Neither a witness nor a uniform native sampler is produced here.

**Blocker status: unchanged.** There is now an actual native-family
certificate against the optimal SINGLE-term importance route, including
polynomially many explicit term subtractions. Local signed access cannot
fix that intrinsic variance. Complete RS lists do give the constructive
smoothed estimator (10), but (11) exhibits missing conditional information.
This does not exclude more effective grouped cancellation, a different
conditional estimator, or a classical witness construction. It establishes
no hardness or quantum advantage claim.

Only this audit file was written. Verification consisted of the derivations,
the cited primary genus/Weil premise, and the exact scalar bounds in the
table; no native Walsh, decoder, search, or sampling execution is claimed.
