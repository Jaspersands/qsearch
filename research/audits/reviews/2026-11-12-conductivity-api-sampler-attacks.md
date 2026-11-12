# Conductivity: correlated-tree and Haar sampler attacks

2026-11-13. Independent focused review of the 2026-11-12 reports, after
current STATE/TRAPS. Read both
completed reports in full:
`../openai_runs/2026-11-12-conductivity-correlated-tree/response.md` and
`../openai_runs/2026-11-12-conductivity-wavelet-compression/response.md`.
Use the native endpoint's counting-measure unit eta, or equivalently uniform
spatial measure and the direction-j constant function 1_j. These conventions
give the SAME T_r. Commands used `/opt/anaconda3/bin/python`; no network,
API, Git, implementation or numerical sweep. Parent owns shared notes.

## Disposition

ACCEPT the three narrowly stated attacks:

1. Reusing one empirical translation in all factors is biased: the period-four
   example gives -1/2 instead of T_1=-3/8.
2. The specified unbiased antithetic factor-replica estimator has second moment
   at least 3(H^2/16)^m, m=r+1, for every full-support joint SCALE law in its
   stated class.
3. In the specified separable Haar basis, parity material gives exact absolute
   path sum (n-1)^(r/2) for even r. Every ungrouped single-complete-path
   importance estimator has second moment at least (n-1)^r; for positive
   even r its mean is zero, so this is also its variance.

The reported upper moment constants 64 and 4096 are VALID. The larger V
bound used for the finite transcript is conservative. None of these findings
is a lower bound against all correlated, wavelet or circuit-aware methods.

## 1. Shared-translation bias, with all mixed scales present

On direction-1 fields depending only on x_1, Pi=I-P_mean: every nonconstant
such field is a periodic gradient. Set s=(1,1,1,-1) periodically in x_1,
sigma(x,1)=s(x_1), sigma(x,2)=1. This is a native two-coordinate-bit circuit.
With mu=1/2 and b=s-mu,

    ||b||^2=3/4,       P Sigma P b=-mu b,
    T_r=(3/4)(-1/2)^r.                                  (1)

For one common translation Y, put Ahat=I-S_Y. At r=1 the expanded sample is

    s(x)[Ahat Sigma Ahat s](x)
       =-s(x+Y)+s(x)s(x+Y)s(x+2Y).

Its spatial average is zero for even Y and -1 for odd Y. An exactly uniform
translation, sampled with fair bits, therefore gives mean -1/2; (1) gives
T_1=-3/8. No numerical heat or precision approximation is involved.

For a free heat endpoint at time T, parity has mean exp(-4T), so the shared
sample mean is -(1-exp(-4T))/2. With a=1-exp(-2T), b=1-exp(-4T), the TRUE
two-projection truncated moment is b^2/8-ab/2. Their difference is

    -b exp(-2T)/2-b^2/8 -> -1/8.

This checks the report's finite-T formula too. Summing common-path band
differences telescopes to I-S_Y, so expanding every mixed-scale tuple does
not fix the bias: E[Ahat Sigma Ahat] need not equal E[Ahat] Sigma E[Ahat].

The auxiliary martingale example is also correct. For independent coarse/fine
bits A,B in {+1,-1}, s=(1+A+B-AB)/2 has differences u=A/2 and v=B(1-A)/2.
Direct four-state averaging gives E[uv]=0 but E[u s v]=-1/4. Thus ordinary
martingale orthogonality does not permit deleting the inserted-material cross
term. This is a statement about that operation, not all martingale estimators.

## 2. Antithetic repair and its precise variance class

On a large band [w,2w], the report's four-corner operator is

    Qhat_ij f = w(N-N')(M-M')/(4t^2)
       *[f(Y00)-f(Y10)-f(Y01)+f(Y11)],

with independent pairs N,N' and M,M' of Poisson(t) counts. The plus-i and
minus-j counts are distinct and independent even when i=j. Applying

    E[(N-N')(F(N)-F(N'))]=2E[(N-t)F(N)]

twice proves its correct band mean. Its constant cancellation is pathwise.
The short band uses the displayed four local shifts; no dense conditional
heat expectation is granted.

For the period-four material, the factor estimator preserves the direction-1,
x_2-independent subspace in EVERY realization; all other components cancel
pointwise. If theta is pi/2, pi or 3pi/2, differentiation of the Skellam
characteristic function gives

    g_t(pi/2)=g_t(3pi/2)=4t(1+2t exp(-2t)),
    g_t(pi)=4t(1+exp(-4t)).

Consequently E|qhat_ell(theta)|^2>=w^2/t^2>=1/4. On the short band the
multiplier's squared magnitude is lambda(theta)^2>=4, so the same lower
bound is safe. Parseval therefore yields

    E||Qhat_ell h||^2 >= (1/4)||P h||^2.                 (2)

Each realization has mean-zero output. For mean-zero h, Cauchy--Schwarz gives

    ||P Sigma h||^2=||h||^2-|<s,h>|^2 >=(1/4)||h||^2.

Start with ||Ps||^2=3/4 and condition successively on the independent factor
innovations. For EACH scale tuple ell of length m, the numerator F_ell has

    E|F_ell|^2 >= 3*16^(-m).

For any full-support law p(ell) on all H^m tuples, importance weighting gives

    E Z^2=sum_ell E|F_ell|^2/p(ell)
       >=3*16^(-m) sum_ell 1/p(ell)
       >=3(H^2/16)^m.                                   (3)

This allows arbitrary correlations between the SCALES, and even a scale law
chosen with knowledge of this material. The class still draws a separate
uniform starting point and uses independent factor innovations conditional
on the tuple. It does not encompass start-/innovation-adaptive importance
laws, a new coupling between factors with covariance corrections, grouped
analytic cancellation, or a material-specific reduction of the universal
H-band cutoff. Unbiasedness of the repaired product uses precisely that
factor independence.

### The upper constants survive checking

For one component on a large band, the four translation norms and its 1/4
prefactor give

    E||Qhat_ij f||_2^2 <=4||f||_2^2,
    E||Qhat_ij f||_4^4 <=196||f||_4^4.

Indeed E(N-N')^2=2t and E(N-N')^4=12t^2+2t; t>=w>=1 gives
(w/t)^4(12+2/t)^2<=196. On the short band the component bounds are 16 and
256. Summing the two input and output directions costs factors 2^2 and
2^4 respectively, giving the report's uniform full-operator bounds 64 and
4096. No independence between different components is needed for this norm
bound.

For the stated PRODUCT scale law with p_ell>=1/(2H),

    sum_ell p_ell^(-1)<=2H^2,   sum_ell p_ell^(-3)<=8H^4.

Factor independence then gives

    E Z^2 <=(128H^2)^m <= V=(256H^2)^m,
    E Z^4 <=(32768H^4)^m <= V^2.

Thus the moment inputs to the reported clipping/coupling bookkeeping are not
invalidated. These UPPER bounds are for the specified near-uniform product
law; they are not uniform over all full-support joint laws. The lower bound
(3) has the broader joint-law scope. The work count pays the 8^m material
tree and O(m) factor-level Poisson innovations reused across its branches.

## 3. Haar parity: exact scalar path sum

Use the separable tensor-product Haar basis and its coordinate subspace
{h(x_1)e_1/sqrt(L)} with the x_2 factor constant. Pi and parity material
sigma(x,j)=(-1)^(x_1) both preserve this subspace, so no omitted nonzero
individual paths leave it. It is isometric to counting-measure functions
on the one-dimensional L-cycle, and eta_1 becomes its normalized constant.

Let q=L/2. Decompose the one-dimensional Haar basis into pair-constant
coarse functions and the q adjacent-pair details. If U is the q-by-q Haar
synthesis matrix on the pair grid, its constant column is
u=q^(-1/2)1 and parity multiplication has matrix

    G=[0,U^T; U,0].

After removing that constant coordinate, put U0=U without the constant
column. Then

    R=Pi Sigma Pi=[0,U0^T; U0,0],    v=Pi Sigma eta=(0,u),
    T_r=v^T R^r v.

Since U0^T u=0, T_0=1 and T_r=0 for all r>=1. Nevertheless for r=2s the
absolute sum of the individual complete index-path terms is

    sum_gamma |t_gamma|=u^T (|U0||U0|^T)^s u.

At each of the n-1 pair-grid Haar levels, the absolute column outer products
sum to that level's dyadic block-averaging projection E_ell. Thus

    |U0||U0|^T=sum_(ell=1)^(n-1) E_ell,    E_ell u=u,
    sum_gamma |t_gamma|=(n-1)^s.                         (4)

For ANY probability distribution on the complete nonzero paths, the
single-term estimator t_gamma/p_gamma satisfies

    E Z_r^2=sum_gamma t_gamma^2/p_gamma
       >=(sum_gamma |t_gamma|)^2=(n-1)^r.                (5)

Equality is attained formally by p_gamma proportional to |t_gamma|, so this
is the optimal second moment in that class, even granting exact access to
all entries. For positive even r, T_r=0 and (5) is also a variance bound.
At r=0 the optimal variance is zero; for odd r the block parity makes every
complete term zero. These cases must not be conflated with positive even r.
For even r=Theta(log n), (5) exceeds every fixed poly(n,r)C^r bound.

Also rho(|R|)=sqrt(n-1): each E_ell has norm one and their sum has eigenvalue
n-1 on u. Positive diagonal similarity cannot lower the spectral radius,
so a weighted induced l1 norm cannot be uniformly bounded by that device.
This is a statement about THIS basis/path expansion, not all wavelet bases.

## Access and final scope

The additional coarse-to-fine example is correct in its displayed dyadic
square basis: parity sends the normalized coarse horizontal wavelet to N/4
finest coefficients of magnitude 2/L. Its l1 norm is L/2 and one-coefficient
unbiased vector sampling has second moment at least N/4. The whole
pair-constant to finest-horizontal sector is an isometry under Sigma_g;
after Pi its minimum singular value is at least 1/2, using
||D*f||^2>=2||f||^2 and lambda_max(D*D)<=8. This rejects a rank-below-N/4
replacement of that ENTIRE overlapping block, not separated-block low rank.
The scalar proof (4) specifically uses the separable basis described above.

Individual Haar material entries can indeed be estimated with one circuit
call per draw from the explicit overlap, weighted by the known envelope
sum_x |w_alpha w_beta|. This gives accuracy relative to that envelope, not
to a possibly zero entry. It supplies neither a sampler proportional to
unknown entry magnitudes nor a free contracted block. Repeated calls count.

Both obstruction families have immediate classical conductivity formulas.
In the Haar case, U0^T u=0 itself groups away the entire problematic scalar
expansion. Consequently no all-wavelet, all-hierarchy, classical-hardness or
quantum-separation conclusion follows. The constructive unresolved operation
remains cancellation-preserving, circuit-accessible contraction with a joint
work/second-moment bound, not merely better evaluation of individual entries.
