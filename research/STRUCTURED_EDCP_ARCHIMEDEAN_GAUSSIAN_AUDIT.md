# Structured EDCP: Approximate Canonical Gaussian Replacement

Date: 2026-09-28. LOCAL DERIVATION / REVIEW PENDING.

This closes an approximation loophole in the whole-module principal-ideal
encoding. It is a source-overlap obstruction, not a quantum circuit lower
bound, a novelty claim, or a proof about every conditional ideal sampler.
Production wiring and routine tests belong to Gemini.

CONDITIONAL FOLLOW-UP (2026-09-28):
`STRUCTURED_EDCP_CONDITIONAL_METRIC_AUDIT.md` supplies a separate smoothing
and exponential-interpolation proof for every integer frequency coset,
including frequency-adaptive metrics AND arbitrary centers. It explicitly
certifies its additional smoothing premise. The ambient-to-fiber warning
below remains necessary when that premise is not established.

## 1. Question And Scope

Section 8 of `STRUCTURED_EDCP_MODULE_GLUING_AUDIT.md` identifies the native
kernel with the known principal ideal J=Y*O in

    O=R[Y]/(Y^L-(q-X)), R=Z[X]/(X^d+1), Q=q^d+1,
    e_0=1, e_j=Y^j+a_j, 1<=j<L.

Exact positive diagonal weighting of embeddings generally cannot restore
the native coefficient metric. Could an APPROXIMATE weighted canonical
Gaussian be close enough, perhaps after multiplying by a unit?

For most normalized uniform labels, the answer is no for DIRECT replacement
of the centered ambient coefficient Gaussian. The bound below is uniform
over all positive embedding weights and all overall widths, including
weights chosen after seeing the labels and weights induced by any unit.
It concerns full integer Gaussians on O in the specified input coordinates.
Arbitrary basis operations, nonzero/adaptive centers, modularly folded target
states, non-Gaussian correction, heralded conversion, or fiber-dependent
metrics need separate arguments. In particular, ambient overlap alone does
not bound all conditioned fibers; Section 6 gives the missing premise.

## 2. Correlated Embeddings Cannot Be Replaced By Independent Ones

Use one base embedding zeta from each conjugate pair, d/2 in total. The
continuous isotropic input Gaussian becomes independent circular complex
Gaussian coefficient vectors across these pairs. At a fixed zeta put
beta^L=q-zeta and omega=exp(2*pi*i/L). Extension embedding r has row

    w_r=(1, a_1(zeta)+beta*omega^r, ...,
                a_(L-1)(zeta)+beta^(L-1)*omega^(r*(L-1))).

Write w_r=a+b_r, with common a=(1,a_1(zeta),...,a_(L-1)(zeta)). Uniformly,

    ||b_r||<=R_q,
    R_q=sqrt(sum_(j=1)^(L-1) (q+1)^(2*j/L)).

A weighted canonical Gaussian has INDEPENDENT circular complex coordinates
in these extension embeddings. The native input instead has covariance
K_(r,s)=w_r*w_s^dagger, up to a common scale. For any two distinct rows,
let c be their normalized complex correlation and a_corr=sqrt(1-|c|^2).
If ||a||>R_q, projection onto the orthogonal complement of the other row gives

    a_corr <= ||w_0-w_1||/||w_0|| <= 2*R_q/(||a||-R_q).                 (1)

For a two-coordinate circular complex Gaussian with unit variances and
correlation c, its Hellinger affinity with an independent Gaussian of
variances t_1,t_2 is

    4*a_corr*sqrt(t_1*t_2)/[(1+t_1)*(1+t_2)-|c|^2].

For fixed sqrt(t_1*t_2), the denominator is minimized when t_1=t_2.
Optimizing then gives the EXACT maximum

    2*a_corr/(1+a_corr), attained at t_1=t_2=a_corr.                     (2)

Marginalization can only increase affinity. Thus this two-coordinate bound
also bounds the entire L-coordinate group, independently of the other
embedding weights. There is no independence assumption on the random labels.

Choose kappa>2 and T=(1+kappa)*R_q. At a base embedding with
|a_1(zeta)|>=T, equations (1)-(2) give affinity at most

    eta=4/(kappa+2)<1.                                                   (3)

The continuous Gaussian groups for different conjugate pairs are independent
under BOTH metrics. If m_good pairs meet this condition, their full
continuous affinity is at most eta^m_good. Counting conjugate pairs twice
would give the wrong exponent. For positive Gaussian wavefunctions this
affinity is the STATE OVERLAP; squared fidelity is its square.

## 3. Natural-Label Probability Without Independent Fourier Coordinates

Assume q odd and use balanced base-q lifts for a uniform a_1 in Z_Q.
The q^d coefficient tuples in [-(q-1)/2,(q-1)/2]^d give distinct residues.
The remaining residue Q/2 has lift ((q+1)/2,(q-1)/2,...,(q-1)/2).

At a fixed embedding, condition on every coefficient except the constant.
The disk |a_1(zeta)|<T permits at most floor(2*T)+1 integer constant terms.
Including the exceptional residue, its probability is at most

    epsilon_label = min(1,[(floor(2*T)+1)*q^(d-1)+1]/Q)
                  <= min(1,(2*T+1)/q+1/Q).                              (4)

By Markov, with probability at least 1-2*epsilon_label, at least d/4 of
the d/2 conjugate pairs are good. Therefore the continuous overlap obeys

    overlap_continuous <= eta^(d/4)                                    (5)

SIMULTANEOUSLY for every positive diagonal embedding weighting. We do not
union-bound over weights or assume conjugate evaluations are independent.
The other labels may be arbitrary; a large first label suffices.

This is the specified IDEAL normalized uniform-label law. Initial unit-label
normalization must be charged. Actual label-distribution TV error adds to
the exceptional-event probability, potentially dominating (4). Other lifting
rules require their own counting proof, not an unannounced substitution.

## 4. Finite-Integer Bridge Covering Narrow And Broad Targets

A continuous covariance argument alone is insufficient. Let N=d*L and
define normalized amplitudes on Z^N by

    psi_A(n) proportional to exp(-pi*n^T*A*n), A=sigma^(-2)*I;
    psi_B(n) proportional to exp(-pi*n^T*B*n).

B is any positive-definite pullback of the diagonal embedding metric,
including its arbitrary scale. Write Theta(C)=sum_n exp(-pi*n^T*C*n).
Their exact overlap is Theta(A+B)/sqrt(Theta(2A)*Theta(2B)).

Put b0=pi/[4*log(8*N)] and require sigma^(-2)<=b0. Split into two cases.

### Broad Target: lambda_max(B)<=b0

Poisson summation gives

    overlap_integer = overlap_continuous
      *Theta((A+B)^(-1))/sqrt(Theta((2A)^(-1))*Theta((2B)^(-1))).         (6)

The continuous factor is
2^(N/2)*(det(A)*det(B))^(1/4)/sqrt(det(A+B)). Denominator theta factors
are at least 1. Since A+B<=2*b0*I, the numerator is at most

    [1+2*(8*N)^(-2)/(1-(8*N)^(-6))]^N < 2.

Combining with (5) bounds the INTEGER overlap by 2*eta^(d/4). This retains
all lattice aliases; it does not round a theta correction to zero.

### Narrow Target: lambda_max(B)>b0

Let u be a unit eigenvector of its largest eigenvalue. The centered target
probability proportional to exp(-2*pi*n^T*B*n) has

    E[(u dot n)^2] <= 1/(4*pi*b0).                                      (7)

Complete the Gaussian square in its MGF and use that a shifted lattice
Gaussian sum is no larger than the centered sum. This proves (7) even when
the discrete Gaussian is far from a continuous one.

For the isotropic SOURCE, one coordinate of u has magnitude at least
1/sqrt(N). Conditioning on all other coordinates and using the largest
scalar source atom <=sqrt(2)/sigma gives, for any r>0,

    Pr_source[|u dot n|<=r] <= min(1,sqrt(2)*(2*r*sqrt(N)+1)/sigma).

Split the affinity over this slab and its complement, use Cauchy--Schwarz
and (7), and obtain

    overlap_integer <= sqrt(sqrt(2)*(2*r*sqrt(N)+1)/sigma)
                       +1/(sqrt(4*pi*b0)*r).

Choosing r=(e^2/a)^(1/3), a=2*sqrt(2*N)/sigma and e=1/sqrt(4*pi*b0),
and using sqrt(x+y)<=sqrt(x)+sqrt(y), gives the convenient bound

    E_narrow = 2*[sqrt(2*N)/(sigma*sqrt(pi*b0))]^(1/3)
                 +2^(1/4)/sqrt(sigma).                                 (8)

This case uses only concentration and positivity, not continuous Gaussian
simulation. It is exactly why extremely narrow or ill-conditioned embedding
weights cannot escape the finite-integer source-overlap test.

### Combined Uniform Statement

Outside the label exception in (4), EVERY centered positively weighted
canonical integer Gaussian has overlap with the native Gaussian at most

    E_all=min(1,max(2*eta^(d/4),E_narrow)).                              (9)

The bound is uniform in label-dependent choices of weights and scale, so
unit finding for free does not repair this direct source replacement.
Additional phases cannot increase overlap beyond the positive-envelope
affinity. Actual truncation/preparation errors still require their own
ledger. A target folded modulo Q, centered on another coset, or reweighted
after postselection is not automatically the state in (9).

## 5. Growing References And Counterchecks

Take kappa=d, q=nextprime(d^12), and the following EXACT comparison widths.
They are comparison points, not changes to live source parameters or new
information-sufficiency certificates. All satisfy sigma^(-2)<=b0.

| d | L | sigma | label-exception upper reference | squared fidelity upper reference |
|---:|---:|---:|---:|---:|
| 64 | 4 | 10^7 | 9.91822e-4 | 1.02816e-3 |
| 256 | 3 | 10^12 | 2.39350e-7 | 7.05073e-7 |
| 1024 | 3 | 10^17 | 3.72893e-9 | 5.44312e-10 |

The broad-case overlap log10 references are -19.1787,-115.5108,-616.4253;
the more conservative narrow case controls (9) here. The 110-digit
calculations are numerical references, not outward interval certificates.

Targeted checks performed:

- 480 independent-complex-Gaussian affinity comparisons verify (2), with
  optimum identity residual <=2.40e-16.
- 360 native embedding/positive-twist comparisons at d=2,4,8, L=2,3 and
  q=17,101,1009, including exceptional balanced lifts. Forty-five L=2
  pair optima were attained; largest log-affinity discrepancy 1.25e-11.
  144 cases also satisfied and checked the good-label bound.
- 21 complete small-label small-ball counts checked (4), including the
  exceptional residue. The proof, not a random independence model, supplies
  the growing-label statement.
- A shifted-interval countercontrol prevents the incorrect 2*floor(T)+1
  count: at d=4,q=5,zeta=exp(pi*i/4), X-X^3 evaluates to sqrt(2).
  For T=0.9 both constant terms -2 and -1 lie in the disk, although the
  incorrect bound would allow only one. Use floor(2*T)+1 for arbitrary
  interval centers. The references use the looser valid 2*T+1 throughout.
- 24 broad two-dimensional integer-Gaussian comparisons and eight narrow
  rotated comparisons checked the lattice split. The largest broad
  discrete/continuous ratio was 1.00000003293, explicitly NOT exactly 1.
  Summation boxes used eight maximum widths; these are numerical controls,
  not certified infinite-sum evaluations.
- Three growing references evaluate (4)-(9). No exponential-dimensional
  state simulation or routine full-suite run was used.

## 6. Do Not Infer A Fiber Theorem From Ambient Overlap Alone

Let p_u,q_u be the native and replacement frequency marginals, and let
a_u in [0,1] be the positive-envelope overlap of their normalized states
within fiber u. The ambient overlap is exactly

    A_global=sum_u sqrt(p_u*q_u)*a_u.

If TV(p,q)<=delta, Cauchy--Schwarz gives

    sum_u p_u*a_u <= A_global+sqrt(2*delta).                             (10)

Indeed sum|p-sqrt(p*q)|<=sqrt(2*(1-sum sqrt(p*q)))<=sqrt(2*delta).
Average squared conditional fidelity is no larger than this root-overlap
average. Thus (9) also obstructs average conditional approximation WHEN
the replacement has a proved close frequency marginal.

Alternatively, if q_u>=lambda*p_u on a set of native mass 1-beta,

    sum_u p_u*a_u <= beta+A_global/sqrt(lambda).                         (11)

Two hundred abstract probability controls checked (10)-(11). A necessary
countercontrol has p=(0.9999,0.0001), q reversed, and a_u=1: all conditional
states agree while ambient affinity is only 0.019998999975. Dropping the
marginal premise would falsely rule this out. A per-fiber adaptive metric
or a separate efficient conditional sampler is outside the single-B result.
Heralding, marginal domination and amplitude correction are real obligations,
not automatically supplied by a canonical-ideal representation.

## 7. Research Decision And Gemini Contract

Do not treat positive embedding weights or unit multiplication as an
approximate Gaussian metric repair. This result is stronger than failure
of exact metric equality, but does NOT forbid canonical number-theoretic
primitives as components of another algorithm.

Gemini should extend the existing module/metric audit with the chosen
integer lift, conjugate-pair grouping, public R_q,T,kappa, natural-label
exception, and explicit integer-Gaussian precision matrices. Keep broad
theta correction and narrow anti-concentration as separate certificates.
Do not infer product structure for the discrete embedded distribution: only
the continuous comparison factors; Section 4 transfers it to the lattice.

Record overlap versus squared fidelity correctly. A fiber claim additionally
needs (10) or (11), or a genuinely new conditional proof. Preserve target
centering/folding/truncation and source-change flags. Do not build another
unit-optimization pipeline whose sole justification is approximate metric
matching. No production wiring, full suite, commit or proof-status promotion.

The conditional follow-up now provides such a proof under its stated
premises. Implement it as a separate certificate; do not replace those
premises by the smaller centered-ambient numbers in this note.
