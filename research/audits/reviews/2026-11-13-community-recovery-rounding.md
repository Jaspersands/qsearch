# 2026-11-13 Finite native community rounding from one-particle mass

## Statement and scope

Fix k>=3 and a known rational 0<mu<=1. Let R be a rational real PSD n-by-n
matrix with trace one. For hidden labels x in [k]^n put
w_a(i)=1[x_i=a]-1/k and L=span{w_a}. Assume

    Tr(P_L R)>=mu,       n/(2k)<=n_a<=3n/(2k) for every a.            (1)

There is a deterministic finite rational preprocessing algorithm followed
by independent finite-bit rounding that outputs a list of at most C_(k,mu)
labelings. With probability >=1-exp(-2n Delta^2), that list contains z with

    max_permutation agreement(z,permutation(x)) >= 1/k+Delta,
    Delta=mu^2/[1024*k^2*(k-1)].                                   (2)

The BIT clock is polynomial in n and the rational input bit length for
fixed k,mu. No labels, latent projector, spectral-gap promise, eigenvector
oracle, or validation independence is used. This proves a candidate-LIST
lemma; the separately proved uniform original-Y validation selects one
labeling. No full quantum composition or novelty/advantage claim is made.

If the input is a complex Hermitian density rho, R=Re(rho) is real PSD
with the same trace and Tr(P_L R)=Tr(P_L rho), since P_L is real. The present
algorithm takes an exact rational R; approximation/tomography is not assumed
for free. The native classical contraction already provides that R.

## 1. Constant-dimensional subspace without a gap promise

Set r=k-1 and alpha=mu/(4r). Compute an EXACT rational orthogonal matrix Q
such that B=Q^T R Q has off-diagonal Frobenius norm <=alpha. A finite
construction and its bit bounds are supplied in section 2 below. Let

    I={j:B_jj>=alpha},       V=span{Q e_j:j in I},       h=|I|.

All these comparisons are exact rational comparisons, including equality.
As B is PSD of trace one, h<=1/alpha. If D_B is its diagonal part, then

    R <= Q D_B Q^T+alpha*I_n <= P_V+2alpha*I_n.

Consequently Tr(P_L P_V)>=mu-2alpha*r=mu/2. In particular h>=1.
This approximate diagonalization is sufficient; V need not be an exact
spectral subspace. Threshold coincidences cause no loss of correctness.

The balanced planted frame F=sum_a w_a w_a^T obeys

    [n/(2k)]P_L <= F <= [3n/(2k)]P_L.                               (3)

Indeed the column Gram matrix annihilates the all-ones color vector, and
on its orthogonal complement has quadratic form sum_a n_a |u_a|^2.
Thus sum_a ||P_V w_a||^2=Tr(F P_V)>=n*mu/(4k), and some color a satisfies

    ||P_V w_a||>=sqrt(n*mu)/(2k).

Put c0=mu/(4k). Since mu<=1, the normalized real projection v0 satisfies
<v0,w_a> >= 2c0*sqrt(n). Both this vector and the color are analysis-only.

## 2. Explicit finite rational Jacobi clock

The following elementary construction pays the diagonalization step. Let
zeta=alpha, delta=zeta^2/(128n^2), and use at most

    T=n^2*ceil(log2(64/zeta^2))

rotations, enlarging the ceiling by integer bit-length arithmetic if needed.
The balance event has n>=k>=3. Maintain Q exactly orthogonal and B=Q^T R Q
exactly rational. Stop if E=sum_(i!=j) B_ij^2<=zeta^2. Otherwise choose a
largest-magnitude off-diagonal entry B_pq, breaking ties deterministically.

An ideal real Jacobi plane rotation G_* zeros this entry and changes E to

    E_* = E-2 B_pq^2 <= [1-2/(n(n-1))]E.                            (4)

Choose its angle theta in [-pi/4,pi/4]. Approximate u=tan(theta/2) by a
dyadic rational u_hat so that the EXACT rational rotation

    cos(theta_hat)=(1-u_hat^2)/(1+u_hat^2),
    sin(theta_hat)=2u_hat/(1+u_hat^2)

obeys ||G-G_*||op<=delta. Then update Q<-QG and B<-G^T B G exactly.
These rotations are genuinely orthogonal, so PSD, trace and ||B||F<=1 are
preserved with no accumulated orthogonality error.

For clarity, this angle computation needs only rational arithmetic and square
roots. In the two-by-two block [A,b;b,C], form
rho=sqrt((A-C)^2+4b^2), choose sgn(A-C), taking +1 if A=C, and use
cos(2theta)=|A-C|/rho, sin(2theta)=2*sgn(A-C)*b/rho. Half-angle formulas
give u. Whenever a rotation is needed, |b|>=zeta/sqrt(n(n-1)), so rho is
bounded below by 2zeta/n. The other half-angle denominators are bounded
away from zero. Certified rational square-root bisection therefore obtains
u_hat with the required error using polynomial bits and a fixed clock;
|u-u_hat|<=delta/4 is sufficient. There is no small eigenvalue-gap premise.

The approximate rotation changes the exact rotated matrix by Frobenius norm
at most 2delta. Hence, since ||B||F<=1 and delta<=1,

    E_next <= [1-2/(n(n-1))]E+8delta.                               (5)

Writing a0=2/(n(n-1)), we have 8delta<=a0*zeta^2/32. Iterating (5),
E_T<zeta^2, because E_0<=1 and the stated T makes (1-a0)^T<=zeta^2/64.
Thus the fixed cap always suffices; the early stop is optional.

Every rotation has O(log n+log(1/zeta)) coefficient bits. A common
denominator for Q divides the product of these rotation denominators, and
a common denominator for B divides the original denominator times their
squares. Their bit lengths grow linearly with T, not exponentially.
Exact comparisons, updates, and the maximum-pivot searches are polynomial
BIT operations. Clearing initial entry denominators costs at most the total
input bit length. The integer rotation cap and certified scalar intervals
give a uniform algorithm, not a real-arithmetic eigenbasis assumption.

## 3. Constant finite rational net

The selected columns Q_I are an exactly orthonormal rational basis of V.
Let M=ceil(8h/c0). Enumerate coefficient vectors b in the grid
{-1,-1+1/M,...,1}^h with ||b||>=1/2; test the squared norm rationally.
For each, compute a rational upper approximation t_b to ||b|| satisfying

    ||b||<=t_b<=||b||+c0/8,

by bounded bisection, and put v=Q_I b/t_b. These are rational vectors of
norm at most one. The list size is <=(2M+1)^h, a constant depending only
on k,mu. It includes both signs and requires no unknown orientation.

Every unit u in R^h is within c0/16 of a grid vector b; such b has norm
greater than 1/2. Normalizing b changes its distance to u by at most a
factor two, and using t_b instead of ||b|| adds at most c0/4. Thus this is
a net of radius less than c0 on the unit sphere of V. In particular one
listed v satisfies

    ||v||<=1,                  <v,w_a> >= c0*sqrt(n).               (6)

All constants, mesh sizes and square-root precisions are public. The vector
v0 from section 1 is used only to prove that a suitable list index exists.

## 4. Rational clipping and centered k-color rounding

To avoid introducing irrational probabilities, take m=floor(sqrt(n)),
which is computed by integer square root and satisfies sqrt(n)/2<=m<=sqrt(n).
For each net vector put

    f_i=m*v_i,   L0=4/c0,   g_i=clip(f_i,[-L0,L0]).

These are rational, and sum_i f_i^2<=n. For the good vector (6),
sum_i f_i*w_a(i)>=c0*n/2. Since |w_a(i)|<=1 and
|f_i-g_i|<=f_i^2/L0, clipping loses at most n/L0. Therefore

    n^-1 sum_i g_i*w_a(i)>=c0/4.                                  (7)

Independently at each vertex, choose label 1 with probability

    h_i=1/k+g_i/(k*L0) in [0,2/k],

and otherwise choose a uniform label among 2,...,k. This CENTERED k-color
coin repairs the earlier h_i=(1+g_i/L0)/2 formula: it cancels empirical
label imbalance exactly. For any fixed permutation sending output label 1
to true color a, expected agreement is

    (1-n_a/n)/(k-1) + [k/(k-1)]n^-1 sum_i h_i*w_a(i)
      =1/k + [1/((k-1)L0)]n^-1 sum_i g_i*w_a(i)
      >=1/k+c0^2/[16(k-1)] =1/k+4Delta.                            (8)

No finer balance than (1) is needed. All other true colors are treated
uniformly, so any permutation of their output labels has the same mean.

Implement the k-outcome rational distribution with ONE b-bit uniform integer
per vertex, using floored rational cumulative probabilities. Every outcome's
probability changes by at most 2*2^-b. Choose b=ceil(log2(2/Delta))+1,
so the expected agreement still exceeds 1/k+3Delta. The bits are independent
across vertices. Conditional on R and the hidden labels, Hoeffding then gives
probability at most exp(-2n Delta^2) that the good candidate has agreement
below 1/k+Delta. The good net index/permutation is fixed in this conditional
analysis before these coins; the algorithm never identifies it using labels.

One pass over the constant net proves the statement. If an additional
conditional failure target eta is desired, repeat the whole net with fresh
coins a fixed number max(1,ceil(log(1/eta)/(2n Delta^2))) of times. The
list grows by this explicit factor; one-pass size is constant and already
has exponentially small failure in n. There are no unbounded rejection loops.

## 5. Native composition boundary

IID uniform labels satisfy the coarse frame balance with failure at most
2k*exp(-n/(12k)). Combining this lemma with the separately proved mass/vector
event adds this probability and the rounding failure; conditioning on a
graph-dependent R introduces no new statistical assumption. All candidate
construction uses the original data through R and fresh internal coins.

The complete rounding cost is polynomial in n and rational input size,
with constants depending on fixed p,k through mu. Added to the native
n^(ell+O_p(1)) vector/contraction cost it is polynomial overhead. Selecting
the best original-Y validation score is justified only by the separately
proved uniform-over-all-labelings validation event; no independent graph or
third clone is introduced here. Approximate quantum tomography and its
precision/physical preparation remain separate from this exact rational lemma.
