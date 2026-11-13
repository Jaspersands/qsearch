# One-pulse Kerr: coherent count CDF classical attack

13 November2026. Selected after STATE/TRAPS, corpus been-tried/baselines,
actual Hiary theorem and retained quantum primary statements, and full201LF
independent comparison with isogeny vectorization/Jones normalization.
No classical polynomial sampler is established. Known quantum endpoint and
small-numerical-period classical sampler remain unchanged.

## Native question and candidate

Binary K, two rational-turn passive angles theta1,theta2, rational a/b,
0<epsilon<=1/4. Start |K,0>, apply B(theta1), exp(2pi i(a/b)binom(N,2)),
B(theta2), and sample one output count in {0,...,K} within epsilon TV.
All angle/phase bits, log(K+1), error and output bits count. The known quantum
endpoint is polynomial in native bits,logK,log1epsilon. Seek a classical
match polynomial in native bits,logK,1/epsilon (a polylog error clock would
be stronger). No smoothing, finite-window oracle, physical exponential-photon
source, hidden state or postselection is supplied.

Mechanism to test: replace the full rotated number-prefix projector by its
exact rank-two DISPLACEMENT/Christoffel-Darboux description; compile the
resulting chirped-binomial quadratic form with certified weighted theta sums.
This attacks the SAME count law and preserves off-diagonal interference.
Strong baselines: direct K+1 evolution; passive/binomial and terminal-Kerr
cases; coherent finite-revival-branch rejection in numerical2b, already proved
in BINARY_FOCK_KERR_SAMPLING.md. Rational approximation alone does not give
poly(logK): denominators can remain of order sqrt(K). No missing comparator,
large Hilbert space or large denominator is hardness evidence.

## Exact identities checked by the parent

Let U=B(theta2) in number coordinates, N=diag(0,...,K), Pi_r the number-prefix
projector, P_r=U^T Pi_r U, and w_n the first rotated binomial amplitude times
the exact Kerr phase. F(r)=w*P_r w. T=U N U^T is tridiagonal. For0<=r<K,
t_r=T[r,r+1], u=U^T e_r,v=U^T e_(r+1):

 [N,P_r]=t_r(vu^T-uv^T),
 P_r[n,m]=t_r(v_n u_m-u_n v_m)/(n-m), n!=m.

P_r still has rankr+1; this is not a low-rank projector. Its diagonal is a
separate confluent CD expression with polynomial derivatives. The exact
Fourier integral for1/(n-m) is not an efficient integration rule.
The classical target is a certified compiler for F(r), uniformly in prefix,
angles, rational phase and K. If it costs poly(logK,anglebits,log1delta),
quantile search at delta=epsilon/[8(K+1)] with a similarly fine uniform
variate gives TV error<=epsilon/2 by coupling outside all CDF-boundary bands.
Only O(logK) queries are needed. O(epsilon) Kolmogorov error is insufficient.
Full201LF proof/selection: audits/reviews/2026-11-13-post-witt-selection.md.

## Actual source boundaries

Hiary Annals2011 Theorem1.1 (actual PDF/text retained under
sources/2026-11-13-one-pulse/) evaluates
K^-j sum_(k=0)^K k^j exp(2pi i(alpha*k+beta*k^2)), REAL alpha,beta mod1,
with arithmetic/operand bits polynomial in nu=(j+1)log(K/eta) and output
error A1*nu^kappa1*eta. Parent read theorem and algorithm scope. Its
arbitrary constants are constructive proof constants, not a supplied numeric
implementation certificate. Gaussian damping, Krawtchouk weights, confluent
diagonal and bilinear Cauchy-kernel sum are NOT included automatically.
Actual DLMF18.2.12/13 supply CD/confluent identities,18.23.3 the Krawtchouk
generating identity. The parent independently derived the displayed matrix
identity. No efficient algorithm follows from that algebra.
Dai-Wong global Krawtchouk source was NOT obtained: CiteSeer returned429 and
author mirror403/nonPDF. Abstracts are not an imported uniform error theorem;
any such theorem must be fetched/read or replaced by a direct derivation.

## Proof obligations and falsifiers

Pay a polynomial number of weighted-sum pieces, their degree and coefficient
bits, all cancellations, diagonal evaluation, integration and all-branch
clocks. Needed accuracy includes delta=epsilon/O(K), so a polynomial cost in
1/delta is not a native polynomial compiler. Central binomial truncation
alone leaves sqrt(K) terms. Bulk asymptotics do not cover turning points,
coalescing saddles, nearly trivial rotations or near-rational revivals.
The period-four cat permits O(1/K) readout-angle changes to move O(1) parity
mass. A smooth/incoherent phase-intensity pushforward cannot be substituted.
No finite test can establish uniform asymptotics, a sampler, or advantage.

An optional parent theta-density envelope may support a coherent rejection
alternative, but the native kernel remains unpaid. For tau=beta+i alpha,
modular reduction to Im(tau')>=sqrt3/2 formally gives a Gaussian-periodic
majorant of |theta(z|tau)|^2. Sampling its integer residue index is cheap even
when the number of peaks is large. This is only a proposed subroutine; retain
interference between opposite phase branches and prove the Krawtchouk/caustic
transfer before using it. It is not the selected full CDF proof by itself.

## Current experiment and API work

Exact Sage control audits/controls/one_pulse_cdf/prefix_kernel.py checks
small native rotations, off-diagonal displacement, confluent diagonal, and
CDF identity. An initial Sage symbolic-to-QQbar coercion failed before tests;
explicit QQ normalization repaired it. Corrected run is pending; no result
is inferred. No quantum implementation or broad benchmark sweep.
Two distinct paid tasks will construct the full CDF compiler and attack its
uniform representation/near-revival clock. Reports remain advisory, no retries.
