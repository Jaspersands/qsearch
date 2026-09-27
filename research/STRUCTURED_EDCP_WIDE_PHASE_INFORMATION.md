# Structured EDCP: Information Bounds For Wide Phase States

Date: 2026-09-26. LOCAL DERIVATION / REVIEW PENDING.

Depends on `STRUCTURED_EDCP_DIRECT_PHASE_SOURCE.md`. This note supplies an
all-divisor information bound at wider Gaussian widths. It is NOT a decoder,
an implementation complexity result, a classical security estimate or an
independently reviewed theorem.

`STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS.md` gives a stronger source-averaged
width budget for the specific upstream Gaussian prior. The information proof
here applies to both source contracts when its actual width/support premises
hold; its first table deliberately retains the general bounded-lift budget.

`STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md` subsequently gives a stronger
ideal-norm/divisor certificate. Keep the bound below as a valid conservative
comparison, not as a necessary block count.

## 1. Why The Earlier Bound Cannot Be Reused

The source in the direct-phase note allows

    sigma <= epsilon*Q /
                 (sqrt(pi)*B*S_q*sqrt(v_K*L*d*M)).             (1)

For q=d^(12+o(1)), fixed n=1,L,K, M=Theta(d*log d) and the upstream
B=O(d^2*sqrt(log d)), this permits sigma of order epsilon*d^9/log d.
The previous information proof required R<=d to make a digit injective
modulo EVERY odd divisor. A wide phase support violates that premise.

Concrete countercontrol: q=17,d=2,Q=290, Gaussian amplitude sigma=6, R=7.
The digit collision probability is about 0.1666689987, but the two-digit
evaluation's collision modulo 5 is about 0.2000000001. The old bound
C_5<=c2 is false here. Small divisors must be handled by Gaussian mixing,
not by pretending the widened alphabet is still injective.

The tensor/core, local-walk, annealing and profile notes also have explicit
width/support hypotheses. Their default sigma=sqrt(d),R=d numerical tables
do not apply at the new widths. Preserve valid scoped results; do not use
them as a blanket impossibility argument against the new regime.

## 2. A Replacement Bound At Every Odd Divisor

Let d>=2 be a power of two, q>=3, Q=q^d+1, n>=1. Let mu be D_(Z,s_G)
conditioned on [-R,R], s_G=sigma/sqrt(2), and require only

    1<=R, 2R<=q-1.

There is NO restriction R<=d. Let

    theta(s)=sum_(j in Z) exp(-pi*j^2/s^2),
    zeta=Pr_(D_(Z,s_G))[|C|<=R],
    c2=sum_j mu(j)^2.

For U=E(C_0,...,C_(d-1)), define C_t=Pr[U=U' mod t]. The exact identity
from `STRUCTURED_EDCP_INFORMATION_THRESHOLD.md` is unchanged:

    E_A chi2(P_A) = sum_(t|Q,t>1) J_n(t)*C_t^L.               (2)

Labels are independent uniform vectors in Z_Q^n; J_n is the Jordan totient.

Every odd divisor t>1 is at least 2d+1. For such t<q, the periodized scalar
Gaussian obeys

    max_x Pr[D_(Z,s_G)=x mod t]
      <= theta(s_G/t)/theta(s_G)
      <= 1/t+1/s_G.

The first inequality follows by Poisson summation: Gaussian mass on tZ+x
is maximal at x=0. The second uses theta(s)>=s and theta(s)<=1+s.
Collision probability is at most maximum mass. Conditioning TWO independent
digits costs at most zeta^(-2), and convolution with the other digits cannot
increase collision. Thus

    C_t <= zeta^(-2)*(1/t+1/s_G),       1<t<q, t odd.          (3)

For t>=q, put k=floor(log_q t), so 1<=k<=d for divisors of Q. The first k
digits remain injective modulo t: their difference magnitude is at most
2R*(q^k-1)/(q-1)<=q^k-1<t, and base-q differences bounded by q-1 cannot
cancel as integers. Convolution by the remaining digits contracts L2, giving

    C_t <= c2^k,                       t>=q.                 (4)

This includes t=Q. Neither (3) nor (4) needs factorization of Q to evaluate
the uniform upper bounds below. Floating logarithms are not needed to certify
k; compare integer powers instead.

## 3. Sum Over Divisors Without Counting Them Incorrectly

Assume L>n+1 and h=q^(n+1)*c2^L<1. Define

    T_small = zeta^(-2L)*2^L*(2d)^(n+1-L)/(L-n-1),
    T_mid   = zeta^(-2L)*q^(n+1)*(2/s_G)^L,
    T_large = q^(2(n+1))*c2^L/(1-h),
    T_wide  = T_small+T_mid+T_large.                           (5)

Then the ODD-divisor contribution to (2) is at most T_wide.

For t<=s_G, (3) is at most 2/(zeta^2*t). Replace J_n(t) by t^n and sum
t^(n-L) over ALL integers t>=2d+1, obtaining T_small by integration. For
s_G<t<q, (3) is at most 2/(zeta^2*s_G); bounding the sum of t^n by q^(n+1)
gives T_mid. Empty ranges only make these bounds looser.

For q^k<=t<q^(k+1), there are at most q^(k+1) integer possibilities, each
with J_n(t)<=q^(n*(k+1)). Equation (4) bounds their contribution by
q^(n+1)*h^k. Sum this geometric series over all k>=1 to obtain T_large.
This intentionally overcounts nondivisors and extends past Q. It is a valid
factorization-free sufficient bound, not a sharp threshold calculation.

If L<=n+1 or h>=1, report this certificate as VACUOUS. It does not prove
insufficient information. Exact-divisor references, when available, may be
much stronger than (5).

For even q, Q is odd and E chi2<=T_wide directly. For odd q, Q=2 times an
odd number. Let G be full row rank of the n-by-L label matrix modulo 2:

    p_G=prod_(i=0)^(n-1)(1-2^(i-L)),     L>=n.

Let b=sum_j (-1)^j*mu(j). As in the earlier information note,

    E[chi2 | G] <= delta_info,
    delta_info=(2^n-1)*|b|^(2d)+(2^n/p_G)*T_wide.              (6)

The optimal ideal measurement has success at least 1/(1+delta_info) on
average over accepted labels, equally for every secret. Implementing that
measurement remains OPEN. The bound is therefore an information certificate,
not the success of a known efficient quantum algorithm.

## 4. Finite Gaussian Bounds And Asymptotic Reading

An explicit upper bound for the one-coordinate excluded probability is

    eta_1 = sigma^2/(2*pi*R)*exp(-2*pi*R^2/sigma^2).

When eta_1<1, safely use zeta>=1-eta_1, and

    c2 <= min(1, (1+s_G/sqrt(2))/(s_G^2*(1-eta_1)^2)).        (7)

Indeed the full numerator is theta(s_G/sqrt(2)), its denominator is
theta(s_G)^2, and conditioning adds zeta^(-2). The bound theta(s)<=1+s
gives (7). This avoids summing a support whose radius is very large.

Poisson summation also gives a parity bound

    |b| <= min(1,
       2*exp(-pi*s_G^2/4)/(1-exp(-2*pi*s_G^2)) + 2*eta_1).    (8)

The second term is the total variation cost of truncation for this bounded
observable. Evaluate tails in log form; underflow to zero is not a certified
upper bound. Near-unit zeta values must not silently become exact one in a
rigorous production certificate.

For sigma=d^(b0+o(1)), q=d^(a+o(1)), 0<b0<a and R below q/2 with negligible
Gaussian tail, (5) gives the sufficient asymptotic conditions

    L>n+1, b0*L>2*a*(n+1).

The terms scale as d^(n+1-L+o(1)), d^(a*(n+1)-b0*L+o(1)) and
d^(2*a*(n+1)-b0*L+o(1)). For a=12,b0=9,n=1, L=6 suffices for vanishing
mean ideal error conditional on G. This is an asymptotic bound only; the
large constants in the source recipe matter greatly at finite d. Fixed L
again gives chosen polynomial error, not negligible error at every exponent.

For comparison, the uniform-secret converse is still

    P_opt <= min(1,kappa^(d*L)/Q^n),
    kappa=(sum sqrt(mu))^2 ~ sqrt(2)*sigma.

It only forces b0*L>=a*n asymptotically. The sufficient count six is NOT a
proof that six is necessary; the gap is genuine slack in the all-divisor sum.

## 5. Concrete Source-Compatible References

These are 120-digit formula evaluations, NOT interval-certified enclosures,
executed large-dimensional states, decoders or computational hardness evidence.
Reuse q=nextprime(d^12) and the exact source M,B from the upstream review;
primality is not independently certified here. Set n=1,K=4,epsilon=0.001,
choose sigma at equality in (1), and R=ceil(sigma*sqrt(d)).

For each d, the table gives the first L>=3 for which THIS finite certificate
has delta_info<0.001. It is not an optimized physical sample count.

| d | M | B | L | sigma | delta_info upper reference |
|---:|---:|---:|---:|---:|---:|
| 64 | 3195 | 355689673 | 14 | 3614751.35903 | 1.52968005e-5 |
| 256 | 17035 | 13854652906 | 11 | 380343478066.929 | 3.27208616e-12 |
| 1024 | 85174 | 480919424497 | 9 | 4.54445535e16 | 7.56729060e-6 |

The support radii are 28918011, 6085495649071 and 1454225710618960250;
all satisfy 2R<=q-1 using exact integer comparisons. At one fewer block the
same delta_info formulas give approximately 34.159,0.7731,2.1511e11.
Those failures do not establish an information-theoretic lower bound.

The joint infinite/truncated trace-distance bounds sqrt(d*L*eta_1) are
approximately 3.84e-84,1.71e-343,1.09e-1388. Hash errors are bounded by the
earlier L=288 values, since source M,K,q are unchanged and L decreased.
The direct phase error is 0.001 by design. Upstream delta_A, delta_lift and
implementation losses are ADDITIONAL, not included in delta_info.

Use one batch and declare failure outside G. If the ideal optimal measurement
were implemented, unconditional source success would be at least

    p_G/(1+delta_info) - delta_source - delta_measurement.     (9)

Here delta_source is the COMPLETE direct-source ledger, including any desired
infinite/truncated comparison. This avoids unproved fixed-instance retry
assumptions. No efficient measurement achieving (9) has been supplied.

## 6. Adversarial Classical And Representation Checks

The classical synthetic Fourier readout in
`STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md` has the same 0.001 flooding
budget at these parameters, before the additional physical-readout ledger.
Widening the quantum source ALSO improves this classical comparator. No
quantum separation follows just from requiring fewer blocks or smaller noise.

For the native column basis with a UNIT first label normalized to one, the
universal-envelope profile still obeys

    H >= Q/theta(s_G)^d >= Q/(1+s_G)^d.

At the three table points its log10 lower bounds are about
977.0621495,4472.119964,20087.43182. In the asymptotic sigma=d^(9+o(1))
regime, this is exp((3+o(1))*d*log d). Thus the existing native-basis rejection
wrapper remains exponentially expensive. This is NOT a lower bound on a
better basis, all samplers or arbitrary quantum measurements.
This profile comparison is conditioned on that unit-label premise; the
information theorem itself does not impose it. A proposed decoder selecting
that event must charge it separately rather than assume full binary rank
implies a unit first label at composite Q.

Conversely, the old sparse-local-move certificate may become vacuous when R
grows so much. Do not retain its old exponent after changing the support.
Exact fibers can have more useful moves without an efficient way to find or
sample them. That is a concrete next problem, not an already solved route.

The important remaining targets are:

1. A global arithmetic conditional sampler or measurement for O(1) wide
   blocks, with its true bit complexity and coherent error proved.
2. A matched classical decoder exploiting the SAME larger width, label law,
   correlated source access and short-secret prior.
3. A sharper collision/conditional-core analysis if it changes the arithmetic
   task, rather than merely lowering a nonessential block-count constant.

The original lattice hardness/reverse-reduction obligations remain separate.

## 7. Checks And Gemini Contract

Sixteen finite wide-support ensembles used (q,d,R)=(17,2,7),(31,2,12),
(65,2,20),(17,4,6) and sigma=2,3,4,6. Direct finite Fourier convolutions
tested 32 odd-divisor instances of (3)-(4); 37 nonvacuous L in {3,6,9,14}
tested the summed bound (5). All passed. The explicit modulo-5 counterexample
in section 1 falsifies the old injectivity shortcut. Small finite references
use finite Gaussian sums for their normalization checks, not exact infinite
arithmetic. Three growing parameter reports checked the finite constraints
and all terms in the table. No high-dimensional decoder was executed.

Gemini should implement a NEW wide-support branch with explicit applicability
checks, not silently widen the old R<=d theorem. Record T_small,T_mid,T_large,
c2,zeta/parity enclosures, rank-selection probability, and source/measurement
losses separately. Retain vacuous certificates and the old-bound counterexample.
Use log-domain or directed-rounding bounds, exact integer support tests and a
public representable sigma rounded DOWN within its source budget. The decimal
tables here are references to reproduce, not proof certificates to hardcode.

Link the mode to the direct-phase source and existing classical comparator;
do not mark a candidate as having an efficient decoder because (6) is small.
Production integration and routine tests belong to Gemini. Main-model effort
should address the missing algorithm, not rerun large low-value sweeps.
