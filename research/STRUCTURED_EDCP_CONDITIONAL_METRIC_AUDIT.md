# Structured EDCP: Fiber-Adaptive Canonical Gaussian Obstruction

Date: 2026-09-28. LOCAL DERIVATION / REVIEW PENDING.

This addresses the conditional-fiber loophole left by
`STRUCTURED_EDCP_ARCHIMEDEAN_GAUSSIAN_AUDIT.md`. It is a source-overlap
statement, not an efficient decoder, a quantum circuit lower bound, a
novelty claim, or an independently verified theorem. Production wiring and
routine validation belong to Gemini.

## 1. Question And Result

Let d>=4 be a power of two, q>=3 odd, L>=2, N=d*L, Q=q^d+1. Condition
independent uniform scalar labels on the FIRST label being a unit modulo Q,
then divide all labels by it. The resulting labels are

    (1,a_1,...,a_(L-1)), with the remaining a_j iid uniform in Z_Q.

Use the balanced lifts and the specified whole-module order/basis from the
ambient metric audit. In coefficient coordinates write

    v=(1,q,...,q^(d-1), a_1,a_1*q,...,a_(L-1)*q^(d-1)) mod Q,
    K={c in Z^N: v dot c=0 mod Q}, det(K)=Q,
    K_u=K+t_u={c: v dot c=u mod Q}.

For each u, the native normalized amplitude is

    psi_u(c) proportional to exp(-pi*||c||^2/sigma^2), c in K_u.

Compare it to a normalized positive Gaussian on THE SAME integer coset,

    phi_(u,B,m)(c) proportional to exp(-pi*(c-m)^T B (c-m)),

where B is the positive coefficient pullback of a diagonal metric on the
field embeddings. Both B and the real center m may depend arbitrarily on
the labels AND u. Widths are included in B. Units only induce further
positive embedding weights, so are included. Additional target phases
cannot increase the overlap beyond this positive-envelope comparison.

Choose kappa>2, epsilon in (0,1), and s0>=1 with

    r=sigma/(sqrt(2)*s0)>1,
    eta=4/(kappa+2), C_epsilon=(1+epsilon)/(1-epsilon).

On the good-label event of the ambient audit AND the event

    delta_K(s0)=sum_(w in K^*, w!=0) exp(-pi*s0^2*||w||^2)<=epsilon,

the following bound holds SIMULTANEOUSLY for all u,B,m:

    |<psi_u|phi_(u,B,m)>|
      <= E_fiber=min(1,C_epsilon*max(eta^(d/4),
                                      sqrt(2*r/(1+r^2)))).             (1)

Squared fidelity is at most E_fiber^2. This is not deduced from a small
ambient overlap or from matching frequency marginals. Sections 2-4 give a
direct conditional proof; Section 5 bounds the probability of its premises.

The all-center, all-coset result is weaker numerically than the earlier
centered ambient bound, but answers a strictly broader question. It still
does not exclude non-Gaussian conditional samplers, a different coordinate
construction, or operations that actively convert the source state.

## 2. Uniform Coset Gaussian Sums

For any positive precision C and any real center m, put

    Z_C(u,m)=sum_(c in K_u) exp(-pi*(c-m)^T C (c-m)).

Matrix Poisson summation gives

    Z_C(u,m)=det(K)^(-1)*det(C)^(-1/2)*(1+e_C(u,m)),
    |e_C(u,m)| <= sum_(w in K^*,w!=0) exp(-pi*w^T C^(-1)*w).

Consequently, if C<=s0^(-2)*I in positive-semidefinite order, then

    |e_C(u,m)|<=delta_K(s0)<=epsilon                              (2)

uniformly in u AND m. The phase factors introduced by the coset and center
have absolute value one; no union bound over either choice is needed.

This is standard smoothing/Poisson machinery specialized to a matrix
precision. See the shifted-Gaussian Poisson argument in the proof of
Lemma 4.4 of [Micciancio and Regev, Worst-case to Average-case Reductions
based on Gaussian Measures](https://cims.nyu.edu/~regev/papers/average.pdf).
The conditional affinity and interpolation conclusions below are derived
here, not asserted to be results of that paper.

Set A=sigma^(-2)*I. Completing the numerator's square shows that if
2A,2B<=s0^(-2)*I, the discrete amplitude overlap is the continuous Gaussian
affinity times a correction bounded by

    (1+epsilon)/sqrt((1-epsilon)*(1-epsilon))=C_epsilon.                (3)

Indeed the numerator precision is A+B, its center is (A+B)^(-1)B*m,
and its scalar mean penalty is

    exp(-pi*[m^T B*m-(B*m)^T (A+B)^(-1)*(B*m)])<=1.

The same penalty occurs in the continuous affinity. Arbitrary target
centers can only reduce the continuous value, even though that statement
alone need not hold for unsmoothed discrete cosets.

## 3. Broad Canonical Targets

Put b_star=1/(2*s0^2). If lambda_max(B)<=b_star, all three precision
matrices in (3) meet (2). The ambient audit's continuous result gives

    overlap_continuous(A,B,m)<=overlap_continuous(A,B,0)<=eta^(d/4)

on its good-label event. Thus the coset overlap is at most
C_epsilon*eta^(d/4), simultaneously for every eligible B,m,u.

Only the continuous comparison factors across conjugate embedding pairs.
Do NOT infer that the integer coset distribution factors that way.

## 4. Arbitrarily Narrow Targets: Interpolate Probability Laws

A centered-lattice covariance bound is NOT valid for an arbitrary shifted
coset. Instead let p_0=|psi_u|^2 and p_1=|phi_(u,B,m)|^2 on K_u, and use
their exponential interpolation

    p_t(c) proportional to p_0(c)^(1-t)*p_1(c)^t, 0<=t<=1.

If psi(t) is the log partition function along this affine log-density
path, then its affinity with p_0 has logarithm

    log H(p_0,p_t)=psi(t/2)-(psi(0)+psi(t))/2.

Convexity of psi gives

    d/dt log H(p_0,p_t)=[psi'(t/2)-psi'(t)]/2<=0.                       (4)

This exact probability-law statement applies to the discrete coset; it
does not require smoothing, zero center, or Gaussian approximation.

The interpolated law is a Gaussian with amplitude precision and center

    B_t=(1-t)*A+t*B,
    m_t=B_t^(-1)*t*B*m.

Suppose lambda_max(B)>b_star. Since A is SCALAR and A<b_star*I, choose

    t_star=(b_star-sigma^(-2))/(lambda_max(B)-sigma^(-2)) in (0,1).

Then lambda_max(B_t_star)=b_star. Applying (4), then (3), bounds the
original overlap by C_epsilon times the continuous affinity between A
and B_t_star,m_t_star. The latter precision need NOT be a canonical
diagonal pullback. Use its eigenvalues instead: its largest eigenvalue
relative to A is exactly r^2, so one REAL coordinate contributes

    sqrt(2*r/(1+r^2)).                                                  (5)

Every remaining coordinate contributes at most one, as does the mean
penalty. Equations (3)-(5) prove the narrow branch of (1). Nonzero centers,
extreme condition numbers, and label/frequency-adaptive weights cannot
escape this branch by invalidating a centered-covariance approximation.

Necessary countercontrol: on Z+1/2, precisions A=100 and B=1000 both
concentrate on {-1/2,1/2}, giving discrete affinity essentially one.
Their continuous affinity is only sqrt(2*sqrt(10)/11)=0.7582608882.
The variance for A=100 is essentially 1/4, not <=1/(400*pi).
The smoothing/source-width premise fails. Dropping that premise, or
copying the ambient narrow-target moment bound onto this coset, is wrong.

## 5. Certifying The Smoothing Event From The Native Label Law

All Gaussians in this section are UNWRAPPED integer Gaussians. Do not
silently replace their probability law by a periodized-amplitude law.
Let C_i iid D_(Z,s0), with mass proportional to exp(-pi*C_i^2/s0^2),
and let chi_s0(x)=E exp(2*pi*i*x*C_i). Scalar Poisson summation makes this
characteristic function real and nonnegative. Define

    A_infinite(v;s0)=sum_(k=1)^(Q-1) prod_(i=1)^N chi_s0(k*v_i/Q),
    T_Z(s0)=(sum_(z in Z) exp(-pi*s0^2*z^2))^N=1+epsilon_Z.

Surjectivity of v gives K^*=Z^N+(v/Q)*Z. The exact identities are

    1+delta_K(s0)=T_Z(s0)*(1+A_infinite(v;s0))
                =Q*s0^(-N)*sum_(c in K) exp(-pi*||c||^2/s0^2),
    delta_K(s0)=epsilon_Z+(1+epsilon_Z)*A_infinite(v;s0).               (6)

The scalar theta tail bounds epsilon_Z by

    epsilon_Z <= expm1(N*log1p(2*exp(-pi*s0^2)
                                      /(1-exp(-3*pi*s0^2)))).          (7)

No additional Q factor belongs in (6). Unlike the periodized source
argument, there is no wrapping-error charge in this unwrapped identity.

For t|Q put b_t=Pr[E_q(C_1,...,C_d)=0 mod t]. The ideal-dual maximum-mass
bound in `STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md` gives

    b_t<=alpha*max(1/t,beta), alpha=1+2^(-2d),
    beta=(sqrt(d)/s0)^d.

Before conditioning on the first label's unit event U, uniform independent
labels give E A_infinite=sum_(t|Q,t>1) phi(t)*b_t^L. All terms are
nonnegative. Multiplying all labels by the same unit preserves A_infinite,
so normalization of the first label does not change this quantity.

Here v_2(Q)=1 and every odd p|Q satisfies p=1 mod 2d. With

    r_max=floor(floor(log2 Q)/floor(log2(2d+1))),
    H_r=sum_(j=1)^r 1/j,

the unit probability has the factorization-free lower bound

    p_U=phi(Q)/Q >= p_star=exp(-H_(r_max)/(2d))/2.                      (8)

Proof: the jth distinct odd prime has p_j-1>=2d*j, and
-log(1-1/p_j)<=1/(p_j-1). Prime powers change neither the totient ratio
nor this bound. This exponential bound is positive even when its weaker
linearization (1-H_r/(2d))/2 is not useful.

Let h=L-1. The odd-prime divisor sums obey

    S_h<=expm1((1+1/(h-1))/(2d)^h), h>=2;
    S_1<=expm1(H_(r_max)/(2d)).

The pure parity term after U is at most b_par^d, where
b_par=chi_s0(1/2)<=min(1,4*exp(-pi*s0^2/4)). It has exponent d, NOT 2d:
this is a characteristic-function first moment, not a collision moment.
Pairing odd orders t>1 with 2t uses b_(2t)<=b_t and phi(2t)=phi(t).
Conditioning their nonnegative sum costs at most 1/p_U. Consequently

    E[A_infinite | U] <= B_A
      =b_par^d+(2/p_star)*alpha^L*(S_h+Q*beta^L),
    E[delta_K(s0) | U] <= B_delta=epsilon_Z+(1+epsilon_Z)*B_A,
    Pr[delta_K(s0)>epsilon | U] <= min(1,B_delta/epsilon).              (9)

For the label-metric event, define

    R_q=sqrt(sum_(j=1)^(L-1) (q+1)^(2*j/L)), T=(1+kappa)*R_q,
    epsilon_label<=min(1,(2*T+1)/q+1/Q).

The ambient audit gives failure probability at most 2*epsilon_label.
Combine events by a UNION bound, not by assuming independence:

    delta_bad<=min(1,2*epsilon_label+B_delta/epsilon).                  (10)

Outside that single label exception, (1) holds for ALL frequency outcomes
and all adaptive choices of B,m. No frequency-marginal assumption remains.

## 6. Growing References And Asymptotic Meaning

Use q=nextprime(d^12), kappa=d, epsilon=0.01 and the exact comparison
widths below. Set s0=sigma/(sqrt(2)*r). These are NOT updates to the live
source, hardness parameters, or information-sufficiency certificates.

| d | L | sigma | r | p_star reference | joint exception upper reference | squared fiber fidelity upper reference |
|---:|---:|---:|---:|---:|---:|---:|
| 64 | 4 | 10^7 | 3 | 0.4731421 | 0.00129417 | 0.624488 |
| 256 | 3 | 10^12 | 10 | 0.4917779 | 0.00310316 | 0.206102 |
| 1024 | 3 | 10^17 | 1024 | 0.4975893 | 0.000191663 | 0.00203284 |

The corresponding B_delta references are 3.0234304061e-6,
3.1029133927e-5 and 1.9165898639e-6. The base-10 logs of Q*beta^L
are -12.9878626572,-9.5271615473,-899.589859274. Parity and epsilon_Z
are each charged by a positive 1e-100 upper allowance after checking their
analytic log bounds. They are not rounded to zero. For the latter check,
epsilon_Z<=x*exp(x), x=3*N*exp(-pi*s0^2), suffices when s0>=1.

These are 110-digit numerical references to analytic bounds, NOT outward
interval certificates. The local argument only needs odd q, not primality;
source theorems that require prime q still have their separate obligations.

For a fixed L, q=d^(a+o(1)), sigma=d^(b+o(1)), choose
s0=d^(c+o(1)) with

    1/2+a/L < c < b.

Then Q*beta^L vanishes, r grows polynomially, and S_(L-1) tends to zero.
One may choose epsilon tending to zero more slowly than B_delta, so the
smoothing exception also vanishes. If kappa=d^gamma with 0<gamma<a/L,
the label exception vanishes and eta^(d/4) decays rapidly. Thus squared
fiber fidelity tends to zero under the strict width-slack condition
L*(b-1/2)>a. Logarithmic source factors need their own finite accounting.
This is not a negligible-at-every-polynomial-order statement for fixed L.

## 7. Verification And Adversarial Scope Checks

Targeted calculations used NumPy/SciPy, SymPy and 110-digit mpmath. They
check identities and failure cases, not a new quantum algorithm or a full
repository regression suite.

- 180 coset partition comparisons, 30 broad-target affinity comparisons,
  30 narrow-target interpolations and 2,400 monotonicity steps. Controls
  use Q=3,5,7, v=(1,2), s0=1.15*sqrt(Q), r=2,3 and nonzero centers.
  NumPy RNG seed 282609; rotated target eigenvalues are (0.6,0.95)*b_star
  for broad targets and (0.6,3.5)*b_star for narrow targets. Centers are
  standard normal vectors times s0. Every coset is checked. Integer boxes
  extend ten maximum widths plus the center; dual scalar sums use -12..12.
  These are truncated numerical controls, not certified infinite sums.
  Largest discrete/continuous affinity ratio: 1.04019014301. Largest
  partition relative correction: 0.11658692466. No increasing affinity
  step was observed. Corrections are explicitly NOT assumed to equal zero.
- The first control's intended delta<0.1 fixture was false: its actual
  dual sum is about 0.129324. The controls instead require delta<0.2 and
  use each actual delta in C_delta. No theorem premise was relaxed to
  accommodate a failing conclusion.
- 108 scalar Poisson comparisons and 186 native primal/dual/characteristic
  identity checks at d=2, q=3,5, L=2,3, s0=0.8,1.2,2.8. The d=2 controls
  test the smoothing identities, not the d>=4 good-pair theorem. Direct
  coefficient probabilities and modular convolutions independently check
  the dual sum. Largest absolute discrepancy: 1.85e-13.
- Twelve full-label divisor first moments and twelve unit-normalization
  averages were checked. Largest normalization discrepancy: 3.56e-15.
  Sixteen exactly factored examples at d=2,4,8,16 and q=3,5,7,11 checked
  the exponential unit-probability lower bound (8).
- The unsmoothed Z+1/2 example above explicitly falsifies both an
  unconditional continuous-affinity transfer and the inappropriate
  centered-lattice variance shortcut.
- Three growing analytic references check positive width slack, both
  exception terms, the narrow/broad split, and overlap versus its square.

Remaining loopholes are substantive: a non-Gaussian coherent operation,
state conversion with charged success cost, a different arithmetic
representation with a new source-metric analysis, or exploitation of the
retained multi-block quantum state beyond this replacement ansatz.
Known ideal generators and favorable smoothing do not supply any of those.

In particular, the narrow-branch squared-overlap upper bound decreases only
polynomially in the displayed asymptotic regime. It does NOT exclude a
polynomial-cost amplitude-amplification construction. Such a construction
would need an actual lower overlap bound and efficiently implementable
reflections or a different conversion primitive; this upper bound supplies
neither. Mere coordinate relabeling also cannot change physical fidelity.
The result rules out an uncharged high-fidelity substitution, not every
algorithm that uses a canonical Gaussian as an intermediate resource.

## 8. Physical Transfer And Gemini Contract

Frequency-only selection cannot evade the ideal bound on good labels,
because it already holds in every fiber. Filtering amplitudes WITHIN a
fiber changes the source and needs a new conversion/success analysis.
Selecting exceptional labels also requires its actual acceptance cost.

Do not infer a uniform physical conditional error from small ambient trace
distance. If the actual normalized source ensemble AFTER unit selection
is within trace distance Delta_cond of the ideal one, any adaptive
Gaussian-target fidelity test, averaged over its observed labels and
frequencies, is bounded by

    min(1,E_fiber^2+delta_bad+Delta_cond).                              (11)

This follows by applying the same block-diagonal target-projector test to
both ensembles. It includes classical mixtures of eligible Gaussian
targets. It does not bound arbitrary coherent superpositions of targets.
Additional postselection needs its own conditioning loss. Unconditional
source errors cannot be silently substituted for Delta_cond. Folding or
truncating target states likewise needs its own transfer argument.

Gemini should implement a certificate, not a metric-search demo. Required
inputs: d,q,L,sigma,s0,kappa,epsilon; exact first-unit normalization and
integer-lift conventions; target class and source-error ledger. Required
outputs: p_star, log(Q*beta^L), S_h, parity/epsilon_Z charges, B_delta,
good-label failure, joint exception, broad/narrow overlap branches and
squared fidelity. Do not multiply probabilities of the two good events.

Regression requirements: all-center Poisson normalization; exponential
interpolation with moving center; equality of the three expressions in
(6); conditional unit normalization distinct from merely odd labels;
parity exponent d; unsmoothed-coset countercontrol; and invalid/vacuous
parameter handling (reject invalid parameters; report vacuous bounds as
inconclusive). Keep high-precision references distinct from interval
certificates. No proof-status or speedup promotion without independent
review. The research conclusion is to deprioritize direct fiber-adaptive
canonical Gaussian replacement, not number-theoretic quantum algorithms.

COHERENT-SUM FOLLOW-UP (2026-09-28):
`STRUCTURED_EDCP_GAUSSIAN_SUPERPOSITION_AUDIT.md` charges cancellation and
ancilla-erasure costs for dictionaries of these packets. It excludes an
efficient all-broad LCU repair under that access model, not arbitrary
superposition circuits. Its separate continuous Schmidt-rank bound must
not be imported into the integer fibers or called quantum computational
hardness; explicit Gaussian transport and modular-conditioning controls
demonstrate both limitations.
