# One-pulse Kerr: coherent count CDF classical attack

13 November2026. Selected after STATE/TRAPS, corpus been-tried/baselines,
actual Hiary theorem and retained quantum primary statements, and full201LF
independent comparison with isogeny vectorization/Jones normalization.
A classical balanced sampler is now established at poly(1/epsilon) error cost
(closure below); the GENERAL-angle problem remains open. Known quantum endpoint and
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
Dai-Wong was subsequently obtained from the actual Fudan publisher after
CiteSeer429 and author-mirror403/nonPDF. Stable PDF/text/metadata are retained
alongside Hiary. Parent read actual scope103-156 and Theorems3.1/4.1 at
1103-1168/1985-2058: fixed n/N limit c in(0,1), separate c<p and p<c<1/2
regimes, expansions uniform in the stated z regions with recursive contour
coefficients. The paper explicitly omits p=q=1/2 and the transition c=p.
Those statements do not supply a uniform native all-angle/all-prefix finite-
BIT kernel compiler or its derivative/precision cost. This is a scoped
source boundary, not absence of other results or a no-go. The original paid
packet accurately records the earlier unavailable status and is immutable.

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
CDF identity. The final exact cyclotomic-field run passed38 prefixes,2016
off-diagonal entries and276 diagonal entries, including projector rank>2.
An initial Sage symbolic-to-QQbar coercion failed before tests; a normalized-
radical rerun was terminated after five minutes without a result. The final
control cancels Fock normalization symbolically using D=L*A*L^-1 and G=L^2,
then uses exact cyclotomic arithmetic. These execution details are retained
in result.json. No asymptotic, CDF-compiler or sampler claim follows.
Two distinct MAX64k paid tasks run: OpenAI68363 fullCDF construction,
Claude38276 uniformcost attack; ceilings4/3USD are not charges. A separate
local review attempts coherent rejection using the proposed theta envelope.
No quantum implementation, broad benchmark sweep or paid retry.

## Exact native parity and CDF stress family

Parent algebraic derivation, all integers K>=1. Take theta1=pi/4, a/b=1/2,
and theta2=theta. The Kerr Fourier expansion has c1=(1-i)/2,c3=(1+i)/2
on number phases i^n and(-i)^n. The two normalized one-particle vectors
alpha+=(i,1)/sqrt2 and alpha-=(-i,1)/sqrt2 are orthogonal eigenvectors of
the real passive matrix [[cos(theta),-sin(theta)],[sin(theta),cos(theta)]],
with eigenvalues exp(+i theta),exp(-i theta). Therefore the K-boson output
amplitude for y photons in the first mode is exactly

 sqrt(binom(K,y))*2^(-K/2)*
 [c1*exp(iKtheta)*i^y+c3*exp(-iKtheta)*(-i)^y],

and hence

 P_theta(y)=2^-K*binom(K,y)*[1+(-1)^y*sin(2Ktheta)].

For theta+=pi/(4K),theta-=-pi/(4K), these are the even/odd-conditioned
binomial laws. Their supports are disjoint, so TV(P_plus,P_minus)=1.
Every gate angle is rational in turns and all input bits are O(logK).
Using the elementary alternating-binomial prefix identity gives

 F_plus(r)-F_minus(r)=2^(1-K)*(-1)^r*binom(K-1,r), 0<=r<K.

Thus their maximal CDF difference is O(K^-1/2), despite TV1. This is an
exact same-input-model falsifier of inferring TV from fixed additive CDF
accuracy, or dropping the cross term in a phase-intensity pushforward.
It does NOT refute a CDF compiler at epsilon/O(K) accuracy or a coherent
proposal/acceptance method. Numerical period4 is already covered by the
retained classical branch sampler; this is a stress control, not a new
classical barrier, hardness argument or advantage. The only estimate used
in the O(K^-1/2) conclusion is the standard central-binomial bound; the
full exact displayed difference holds at every K.

## Gaussian damping reduction under focused review

The parent derived a direct polynomial(B,p) BIT reduction for finite sums
sum_(n=L)^U exp(-alpha*(n-mu)^2)*exp(2pi i*(a*n+b*n^2)), alpha>=0 rational,
all other parameters binary rational/integer, absolute error2^-p. Exact
rational interval truncation to alpha*(n-mu)^2<=T, T=p+bitlength(U-L+1)+6,
leaves small total tails. On the retained normalized interval Q has coefficient
l1<=9T; Taylor degree2J with J=8*(T+p+ell(H)+4) has error<2^-p/(64H)
and coefficient l1<=2^(18T). Polynomially many calls to the ACTUAL REAL
Hiary sums pay this weight with polynomial coefficient/precision bits.
Full proof: audits/reviews/2026-11-13-gaussian-chirp-hiary-reduction.md;
full138LF independent review parent read and checked. No normalization, binomial/Krawtchouk,
confluent diagonal, bilinear Cauchy or native sampler is thereby supplied.

## Reviewed analytic components and scoped transfer failure

Full138LF Gaussian-chirp review parent checked. It makes Hiary internal error
allocation explicit, charges dyadic phase rounding, and keeps an exact even
common denominator through source recursion: a=A/D,b=C/D maps to denominator
4C<=D when0<C<=D/4. No gap-from-integer assumption is required. The finite
Gaussian sum is CLOSED WRITTEN at absolute-error polynomial-bit scope.

Full221LF coherent-rejection review parent checked:
audits/reviews/2026-11-13-kerr-coherent-rejection.md. A modular theta-density
sampler for a requested binary phase cell has polynomial BIT cost, constant
acceptance (>=1/16 for theta00, >=1/10000 for arbitrary rational Gaussian
centers), with coherence retained when amplitudes are evaluated. It outputs
a rounded-phase law, not a finite atomic law claimed TV-close to a continuous
measure. Parent additionally checked the modular-coordinate bit bound via
integer lattice reduction: scale the initial basis(1,tau) by a common rational
denominator into two integer plane vectors. Centering decreases the second
vector length and inversion swaps vectors only when it is shorter. All vector
coordinates stay within the initial maximum length; inverting the initial
integer basis (nonzero integer determinant) then bounds cumulative SL2 entries
by a polynomial in those lengths. Their BIT lengths are polynomial in input.

The same review gives a decisive scoped native family for full-condensate
Cauchy rejection: K=2r^2,Q=100r,Kerrphase1/Q, balanced input. The coefficient
c_Q(z)=sum_m exp[-pi(m-K/2)^2/Q^2] exp[pi i*m*(m-1)/Q-2pi i*m*z]
produces the true state with a small diagonal damping; after normalization
its output law is within1/1500 TV of the true one. The exact modular matrix
[[-1,0],[Q,-1]] maps tau=1/Q+i/Q^2 to i-1/Q. Consequently
||c_Q||inf<=4sqrtQ and ||c_Q||2^2>=Q/sqrt2, so ||c_Q||1^2>=Q/32.
For ANY phase proposal rho, the generic Cauchy envelope mass
A=int|c_Q|^2/rho >=||c_Q||1^2; acceptance<=32/Q=O(K^-1/2).
Even perfect theta sampling and amplitude evaluation do not repair that
architecture. Output-dependent tighter envelopes and the full native CDF
remain OPEN; there is no general classical lower bound. In particular one
must not normalize a cancelling opposite-phase pair independently: its mass
may vanish. A joint-parity/global envelope would have to pay normalization.

## Terminal paid-report disposition

The original full-CDF construction and uniformattack calls both yielded NO
readable mathematical report. OpenAI68363 ended ReadError, response0bytes,
billingUNKNOWN; no partial counter is a final charge. Claude38276 ended
EMPTY MaxTokens, response0bytes, estimate1.346368. Both processes reaped;
neither is retried. The new balanced construction below arose from parent
analysis and independent local proofs, not a provider result or acceptance.
This adds a seventh UNKNOWN bill at the next clean usage milestone.

## Concrete balanced-rotation construction under proof

The native GENERAL-angle problem remains open. A newly specified end-to-end
candidate covers the canonical balanced subfamily theta1=theta2=pi/4, every
binaryK and rational Kerr phase, with target classical poly(logK,phasebits,
1/epsilon) count sampling. This is not an assumption that arbitrary rotations
can be replaced by balanced ones. New corpus been-tried/baselines and a targeted
literature search found existing Kerr/symmetric-Krawtchouk leads, not an
applicable all-input theorem. Prior Hiary and actual Dai-Wong scope are as above.
The matched quantum endpoint and numerical-period classical comparator remain.

For n=K/2+m (integer or half-integer m), propose a UNIFORM ABSOLUTE kernel
bound for balanced real U, not a relative bound at its zeros:

 phi_r=2*atan(sqrt(r/(K-r))), k=min(r,K-r),
 A_r=sqrt(2/pi)*[r(K-r)]^(-1/4),
 U[r,K/2+m] ~= A_r*cos(m*phi_r-pi*r/2),
 error <= C*A_r*poly(T)/sqrt(k),
 |m|<=sqrt(K*T), k>=C*poly(T).

Constants/exponents and sufficient K must be effective and absolute. The
exact generating polynomial has two saddles +/-i*sqrt(r/(K-r)); normalization
must cancel its m-dependent real Gaussian growth. Kernel proof is pending.
At m0,evenr the exact squared value is
2^-K*binom(r,r/2)*binom(K-r,(K-r)/2), consistent with A_r. This identity
checks scale only. The suggested phase-third-derivative scale is
O(1/[K^(3/2)*sqrt(k)]), giving O(T^(3/2)/sqrt(k)) across the central window;
this is motivation, NOT an imported saddle theorem.

If that bound holds, the normalized balanced binomial input can be replaced
by a discrete Gaussian g_m proportional to exp(-m²/K), with explicit Stirling/
tail l2 error and a direct small-K branch. Kerr preserves this input error.
Since ||g||1=O(K^1/4), summing the squared kernel error over k>=Y gives
O(poly(T)/sqrt(Y)); thus Y polynomial(T,1/epsilon) suffices. This is the
critical distinction from an unsupported pointwise-to-operator inference.
Endpoint counts k<Y need a separate amplitude compiler costing
poly(Y,logK,phasebits,p) at absolute2^-p, currently under independent derivation.

The following sampler composition is conditional on these uniform gates.
Let psi(phi)=sum_m g_m*chirp_m*exp(i*m*phi). The leading bulk probabilities
are A_r²/4 times |psi(phi_r)+(-1)^r psi(-phi_r)|². Define the JOINT density

 f_s(phi)=|psi(phi)+(-1)^s psi(-phi)|²/(4pi),
 phi in[0,pi], s=0,1.

For normalized g, the sum of both integrals is exactly1 by Parseval and
cancellation of cross terms. Sample the full-circle theta density, fold phi
into[0,pi], and draw a fair s. Accept with probability |psi(phi)+(-1)^s
psi(-phi)|²/[2(|psi(phi)|²+|psi(-phi)|²)]. Global acceptance is1/2; no
potentially cancelling parity sector is normalized alone. Round
K*sin²(phi/2) to its nearest count of parity s, retaining interference.
In the bulk, same-parity phase cells have width about2/sqrt(r(K-r)).
A derivative L1 bound from ||psi'||2=O(sqrtK) yields a proposed Riemann-TV
errorO(Y^-1/2); the exact geometric and finite-bit bounds need full review.
Phase resolution O(logK+log1epsilon) pays count-boundary rounding using the
known polynomial-in-K density upper bound. A finite atomic phase law is
compared only with the corresponding rounded continuous law.

To replace the endpoints without conditioning on a tiny bulk mass, mix a
uniform choice from E={k<Y} with weight |E|/(|E|+1) and the full joint-phase
sampler with weight1/(|E|+1). The endpoint branch accepts with the actual
endpoint probability P_r; the phase branch accepts only bulk counts. This
samples an unnormalized measure with masses P_r on E and the phase-derived
R_r in the bulk. Its total mass is1+O(epsilon) if the previous approximation
proofs hold, so acceptance is Omega(1/(Y+1)), with a bounded trial cap.
Endpoint probabilities are computed accurately enough that |E| times their
error is small. No extra normalization or rare-bulk assumption is needed.

Use the explicit real matrix convention [[cos,-sin],[sin,cos]] for the
kernel calculation. With the opposite literal B operator convention, two
balanced rotations change the full count amplitude only by output-row factor
(-1)^(K+r), not its probability. Signs still must be tracked in each proof.
This candidate has three actual obligations: uniform central kernel, endpoint
compiler, and complete finite-bit joint-parity composition. All remain
unadmitted until independently checked. No quantum implementation or claim
that passing finite controls establishes the sampler.

## Checked balanced components and complete composition draft

The full218LF `audits/reviews/2026-11-13-balanced-kerr-kernel.md` and
201LF `...balanced-kerr-endpoints.md` were parent-read and checked. The first
proves the proposed absolute kernel with C=2^16 and k>=2^10(1+T)^2, using
an exact contour entropy bound, shifted Gaussian and Stirling cancellation.
It pays all parities and zeros. The second proves poly(Y,logK,phasebits,p)
absolute2^-p endpoint amplitudes through entire binomial interpolation,
J=2048Q, exact adjacent node ratios, explicit coefficient denominators and
the actual real Hiary interface. Direct enumeration is only K<=2^30Q^2.
These two component claims are established at their written scope.

The full parent composition is `...balanced-kerr-sampler.md`, independently
under review. It makes Y=ceil(2^100(1+T)^12 delta^-4), delta=epsilon/2^10;
handles K<=2Y directly; rationalizes the theta imaginary parameter; keeps
joint parity normalization; proves summed bulk quadrature with a sufficient
O(1/Y) relative geometry estimate; and replaces endpoint mass by explicit
probabilities with acceptance Omega(1/Y). Finite phase grid pays BOTH
acceptance-ratio continuity and count boundaries, with capped inner/outer
clocks and pertrial error allocations. No balanced fullsampler is admitted
until this composition review and the new independent proof attacks resolve.
General passive angles remain OPEN. No practical or quantum speedup claim.

Two distinct paid attacks now target these concrete new components:
Claude25093/high on kernel, OpenAI37356/max on endpoint BIT compilation.
Exact packets/ceilings are in api_inputs/2026-11-13-balanced-kerr/dispatch.json.
They are not retries of the failed generalCDF jobs. Previous analyticround
is frozen40hashes once at controls/one_pulse_cdf_round: cumulative estimated
301.179324 over230priced records, Anth169.248014/OpenAI131.931310; seven
UNKNOWN bills excluded. Owner actual spent155.99/101.71 remains separate.

### Paid kernel attack disposition

Claude25093 completed; full180LF report parent-read, process reaped exit0.
Its contour derivatives, entropy cancellation, all-parity reflection and
summed l2 arithmetic were checked against the original proof. No material
kernel gap found. Its requested sign qualification is accepted explicitly:
the two-gate row sign assumes native input |K,0>, already fixed in the
contract. Input |0,K> would instead add (-1)^n to the intermediate phase;
no transfer to that different contract is inferred. The kernel proof now
states |K,0> explicitly. Paid snapshot is immutable. The report's categorical
"no counterfamily exists" is not independent evidence; only its displayed
checks are used. It did not assess the endpoint/compiler/full sampler.

### Paid endpoint attack disposition

OpenAI37356 completed; full346LF report parent-read, process reaped exit0.
Estimate1.255670 plus Claude0.620804 gives round1.876474USD, not an invoice.
The report's identities, entire Gamma product, contour remainder, exact common
coefficient denominators and Hiary precision conversion were checked. Its
scalar citation gap is a PACKET COVERAGE limitation: BINARY_FOCK_KERR_SAMPLING.md
LF201-216 had already been parent-read and pays logfactorial via positive-real
Stirling. The report independently supplies the same valid fixed-term/shift
construction; no mathematical source gap remains at that scalar scope.
Its conservative integer Hiary direct cutoff
1000[(j+1)(ceil(log2(M+1))+q)]^6 is accepted as an explicit finite-comparison
implementation of the already polynomial small-interval branch. No exact
comparison of a transcendental logarithm is needed. Its integerKerr and K1
symbolic controls agree with B(pi/4)^2 and the retained row sign; no new test
is needed to establish those exact identities. The report does not independently
reprove Hiary's analytic theorem; that primary-source dependency stays explicit.
No endpoint claim is promoted into the complete sampler before composition
review. Both new paid reports are terminal/full-read/reaped with no retry.

## Balanced full-count sampler: repaired written closure

The full225LF independent composition review was parent-read and checked.
The repaired parent sampler now explicitly stores rational turns, retains
SEPARATE characteristic-shift phases for z0+x and z0-x, uses an exact rational
isqrt(K) rejection threshold, and caps/allocates every grid and sampling error.
For oddK,zeta0, dropping the shift sign after reducing -x to1-x swaps the
joint parity sectors and gives TV1 at the subroutine level. This concrete
falsifier is retained; the corrected algorithm does not drop those signs.
The strengthened Gaussian density bound, quadrature bootstrap and endpoint
replacement normalization were checked in the review. No finite examples
were used to infer the algorithm.

Established WRITTEN: for EVERY binary K, rational Kerr zeta and requested
0<epsilon<=1/4, with input |K,0> and exactly B(pi/4), Kerr, B(pi/4), sample
one output count within epsilon TV in classical polynomial(logK,phasebits,
1/epsilon) BIT time. This is not a polynomial-log(1/epsilon) claim. General
angles, arbitrary input and multiple pulses are excluded. Constants are huge.
All endpoint/kernel/theta/realHiary access is charged; no hidden advice or
postselection probability is supplied. The known quantum endpoint remains
prior art. No novelty, classical lower bound, advantage, implementation,
practicality or human/formal verification is asserted.

This closes the balanced constructive classical challenge. Next choose by
external value, not by the remaining general-angle caustic. Independent
comparison has a new folded-chain homogeneous-product Gaussian projection
lead; it is not yet admitted and belongs to a separate pass after sources.
