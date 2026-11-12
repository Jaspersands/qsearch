# Native periodic conductivity: endpoint admission

2026-11-12. CLOSED written quantum endpoint and fixed-precision classical
match. Two completed independent core reviews, one completed paid classical
report and two truncated advisory reports checked. One frozen exact control.
No novelty, separation, practical speedup or quantum execution claimed.

## Selection and exact question

Start STATE/TRAPS after the closed scalar-OPI filter pass. Saved corpus
lookups precede primary-source reading: audits/selection/2026-11-12/.
Tensor/HSP and Jones routes had no newly paid operation. The fresh ternary
subset-sum paper is already covered by DCP_BINARY_ERROR_SOURCE_BRIDGE.md;
no new joint processor was identified. The massive-classical-data oracle
sketch is already scoped in WEIGHTED_MOMENT_CHARACTER_ADMISSION.md; it does
not remove native source costs. The wavelet-PDE lookup found no close native
endpoint; the baselines catalog has no named match, which is not an absence
of classical methods.

Actual arXiv2306.11802v3 shows a concrete normalization issue to avoid: its
AppendixE2 infers lambda_min(AP)>=1/kappa(AP) from normAP<=1. That inference
is invalid without a lower bound on normAP. We do not import its Lemma3.
Actual arXiv2610.41690v1 instead absorbs the homogeneous inverse square root
inside a gradient factor, obtaining norm1. Its sections3.5-3.8 pay coherent
wavenumber arithmetic and distinguish large-grid arithmetic from finite
table-multiplexor simulations. Its conclusion explicitly leaves effective
conductivity readout to a companion paper. The present endpoint uses a
nearest-neighbor resistor network, not the source's Q1 finite elements.

Single question: can that normalized-gradient mechanism yield a completely
paid poly(native description,1/epsilon) quantum estimate of effective
conductivity on a succinct periodic two-dimensional material, and does an
output-specific classical algorithm already match it? This is a natural
macroscopic physical observable, not a supplied quantum state or toy oracle.

## Input, output and proposed mechanism

Input: L=2^n, n>=1, the two-dimensional torus X=(Z/LZ)^2, N=L^2 nodes, two oriented
edges (x,j) per node. A Boolean circuit of size B maps (x,j) to a phase bit;
the corresponding edge conductivity is a_e in{1,rho}, with fixed rational
1<rho<=rho0. Both processors receive the entire circuit, not just a black
box. Rational epsilon>0 and failure tolerance delta>0 are explicit. Pay
polynomial in B,n,1/epsilon,log(1/delta); do not claim logarithmic dependence
on 1/epsilon. No IID, regularity, finite-correlation or planted promise.

Let D map node potentials to edge differences phi(x+e_j)-phi(x), and let
eta_j be the unit edge vector equal to1/sqrt(N) on direction-j edges and0
elsewhere. Output an additive-epsilon estimate of
 K_j=(1/N)min_phi sum_e a_e(1_(direction(e)=j)+(D phi)_e)^2.
This is finite-cell effective conductivity; 1<=K_j<=rho. The zero-mean gauge
is analysis, not a supplied solution. A complete field is not the output.

Set S=diag(a/rho), K0=D^*D, V=D K0^(+,-1/2), and P0 the constant-node
projector. V^*V=I-P0 and ||V||=1. Define
 M=V^* S V+P0, q=V^* S eta_j.
Then spectrum(M) is in[1/rho,1] and, by minimizing the energy,
 K_j/rho=<eta_j,S eta_j>-<q,M^-1 q>.                 (ENERGY)
This formula uses the UNNORMALIZED q; q may vanish. Preparing q/||q|| would
introduce an unnecessary rare-source cost and is not the proposed algorithm.

The Fourier symbol of V at nonzero k is the two-component unit vector
 (exp(2pi i k_1/L)-1, exp(2pi i k_2/L)-1)/
 sqrt(sum_j |exp(2pi i k_j/L)-1|^2).
The zero mode is routed to an orthogonal workspace flag. QFT, fixed-point
symbol arithmetic, controlled two-component rotation, and inverse QFT pay
V with polynomial(n,log1/error) gates. The denominator is Omega(1/L) for
nonzero k, so absolute arithmetic precision pays O(n) extra bits. The phase
circuit and a controlled rotation give S with norm1. Use fresh ancillas for
operator products and direct-sum treatment of P0. No free rescaling of a
small-norm block is allowed.

QSVT can encode M^-1/rho with paid constant-rho normalization. The scalar
<eta_j, S V (M^-1/rho) V^* S eta_j> is a matrix element of a product of
contractions. Its preparation starts from the explicit uniform eta_j, keeps
all success flags, and estimates a matrix element directly; no q norm or
postselection is needed. ENERGY multiplies this scalar by rho^2, and the
first mean by rho. Allocate measurement and synthesis errors accordingly.
The later finite-series construction closes the BIT/error/gate proof using
elementary projection blocks, without this QSVT branch's extra machinery.

Initial intended upside was polynomial in n=logL and1/epsilon
versus full-grid FFT/preconditioned classical solves using at leastN storage/
work. That comparison ALONE is insufficient: sublinear scalar-output methods
could match the same endpoint. No classical lower bound is asserted.

## Strongest classical attacks and decisive falsifiers

1. Constant media and layers are easy: arithmetic/harmonic means computed
   by circuit sampling pay a polynomial classical estimate. They are controls,
   not claimed advantageous instances.
2. Full-grid sparse/FFT-preconditioned conjugate gradient has contrast-bounded
   iteration count. Run an exact small-grid energy solve as the transcription
   control before any quantum circuit work; it cannot establish scaling.
3. Mourrat1609.06674 actual Theorem1.2 gives essentially epsilon^-2 log1/epsilon
   work for an IID stochastic-homogenization endpoint. Its assumptions and
   infinite-volume/ensemble target do NOT automatically cover an arbitrary
   succinct periodic coefficient circuit. Preserve it as a strong baseline
   where applicable, not a generic no-go.
4. Most serious general attack: center a at (rho+1)/2, use the gradient
   projection Pi=D K0^+ D^* and a convergent contrast Neumann series. The
   operator-norm tail decays geometrically, so only O(log1/epsilon) terms
   are needed at fixed contrast. Can their signed convolution expectations
   be sampled in poly(n,1/epsilon), with kernel evaluation, variance and BIT
   costs paid? An l1 norm O(logL) repeated O(log1/epsilon) times gives only
   quasi-polynomial precision scaling, not a matching polynomial theorem.
   Even that bound requires an actual efficient kernel sampler/evaluator.

Falsifiers: material loading sizeOmega(N); norm amplification or rare source
left uncharged; inaccurate low-frequency symbol; dependence on a missing
field/normalization; classical poly(B,n,1/epsilon) estimator for ALL circuits;
or prior literature already giving exactly the complete endpoint. A finite
control, missing classical proof or failed attack does not show advantage.

Frozen classical experiment, completed once: exact L4 constant/layered/nonlayered resistor
networks at rho2 in Sage; compare direct rational minimization with the
projection/Schur-complement form of ENERGY and a bounded Neumann tail.
Check zero-q case and layer orientation. Freeze one fixture set; no scaling
fit, circuit implementation, PDE framework or benchmark sweep.

## Parent derivation: a kernel-free classical attack

Independently reviewed on12November; the final finite-bit specification below
supersedes the initial clipping sketch. This is a
constructive attack at fixed contrast, not an assumed efficient Riesz oracle.
Let c=(rho+1)/2, z=(rho-1)/(rho+1)<1 and a=c(I+z Sigma), with diagonal
Sigma in{+1,-1}. Pi eta_j=0, and the energy identity becomes
 K_j=c[1+z<eta_j,Sigma eta_j>
   -z^2 sum_(r>=0)(-z)^r T_r],
 T_r=<eta_j,Sigma Pi(Sigma Pi)^r Sigma eta_j>.           (SERIES)
Since Pi and Sigma are contractions, |T_r|<=1; keeping r=0,...,k-1
has absolute error<=c z^(k+2)/(1-z). Thus k=O_rho(log1/epsilon).

We can estimate each T_r without evaluating any dense inverse entry.
On the torus let K0=D^*D. The exact projection is
 Pi_ij=integral_0^infinity D_i exp(-tK0) D_j^* dt.
Truncation at T gives Pi_T=V(I-exp(-TK0))V^*, so
 ||Pi-Pi_T||<=exp(-lambda_min^+(K0)T), lambda_min^+>=16/L^2.
Choose dyadic T=2^J>=max(1,(L^2/16)log(1/tau)); J=O(n+loglog1/tau).

The free heat kernel is an exactly specified law: independent Poisson(t)
counts N_l^+,N_l^- for l=1,2 and displacement Y_l=N_l^+-N_l^- moduloL.
Poisson integration by parts gives, for every bounded edge test function f,
 (D_i exp(-tK0)D_j^* f)(x)
   =E[(N_i^+/t-1)(N_j^-/t-1) f(x+Y)].                  (MARKS)
The two counts in the product are independent even when i=j. Its second
moment is EXACTLY1/t^2. These are signed weights, not probabilities.

Split [0,T] into [0,1] and [2^ell,2^(ell+1)], ell=0,...,J-1.
Choose one of the J+1 intervals uniformly, then t uniformly in it. On the
small interval use the four-term difference
 S_(e_i-e_j)-S_(e_i)-S_(-e_j)+I:
choose one term uniformly, weight it by4 times its sign, and add its shift
to Y. On a large interval of width2^ell use weight2^ell times the product
in (MARKS). Multiply either weight by J+1. This is an unbiased signed
sampler for the truncated component Pi_T, with second moment at most
16(J+1)^2. Choosing the next edge direction uniformly and multiplying by
d=2 gives a full edge transition with conditional second moment at most
 H^2=16d^2(J+1)^2.

For T_r, start at a uniform node in directionj, multiply by Sigma there,
perform r+1 independent signed transitions, multiply by Sigma at each
visited edge, and finish with the indicator that the final direction isj.
The expected signed product is T_r with every Pi replaced by Pi_T. Its
second moment is at most H^(2(r+1)). The bias from time truncation is at
most(r+1)tau by telescoping contractions. Median-of-means estimates and
the geometric SERIES tail therefore give a classical cost bounded by
 poly(B,n,1/epsilon,log1/delta)*H^O(k),
subject to the finite-bit implementation below. At fixed rho,epsilon this
is polynomial in B,n. At epsilon=n^-O(1), it is only exp[O((logn)^2)]
times poly(B); a full polynomial match in both n and1/epsilon is OPEN.
This upper bound is not a hardness or separation statement.

Initial finite-bit alternatives (superseded by the simpler whole-transcript
coupling below; none is an assumed primitive):
- Replace continuous t by a uniform dyadic midpoint grid. The operator
  derivative of D_i exp(-tK0)D_j^* has norm<=16d. A grid spacing of
  O(tau/(d^2 T)) controls the summed integral error. Although the number
  of grid points is large, its index has O(logT+log1/tau) bits.
- Ideal Poisson(t) can be coupled to Binomial(Q,t/Q) with TV<=t^2/Q.
  Choose integer Q polynomial in numerical t and1/tau; its BIT length is
  O(logT+log1/tau). The two centered binomial factors still have second
  moment at most1/t^2. This pays the weighted coupling by Cauchy-Schwarz,
  not by falsely treating unbounded weights as bounded observables.
- Reuse the already reviewed binary-total binomial sampler in
  BINARY_FOCK_KERR_SAMPLING.md section3a (bounded time polynomial in logQ,
  rational-probability bits and log1/error). No O(t) Poisson loop is allowed.
- Clip each final signed transition weight at a polynomial H^2/tau bound;
  the lost first moment is bounded by its second moment divided by the cap.
  Approximate-binomial TV then costs at most twice the cap times TV. Choose
  each sampler tolerance accordingly. The conditional second-moment bound
  changes by at most a constant after this paid approximation.
- At most k contractions appear in each moment. Choose all step operator
  errors O(epsilon/poly(k,rho)), and note approximate norms<=1+error. Charge
  score-circuit calls, bounded median-of-means samples, weight multiplication,
  and all random-bit clocks. No claim of exact output after finite cutoffs.

The completed review verifies the marked kernel, same-component signs and
variance, and closes finite-BIT costs via the whole-transcript construction.
It does not infer efficient access from an uncomputed dense inverse.

## Simpler constructive quantum endpoint: use the same finite series

Reviewed parent derivation. The fixed-contrast endpoint needs no QSVT
phase-synthesis backend: use SERIES itself. On the physical 2N-dimensional
edge space construct the unitary reflection Rgrad=I-2Pi. Fourier transform
the position, and at each nonzero k reflect the direction qubit about the
unit gradient vector v(k); at k=0 use identity. This avoids introducing an
artificial constant-gradient mode. A Hadamard-LCU using I and -Rgrad gives
Pi as an upper-left block with norm1 and ONE flag qubit.

Explicit symbol arithmetic: for 0<=k_j<L,
 exp(2pi i k_j/L)-1=2i exp(pi i k_j/L) sin(pi k_j/L).
Both sine magnitudes are nonnegative. At nonzero k a real qubit rotation
with angle atan2(sin(pi k_2/L),sin(pi k_1/L)) prepares their normalized
magnitudes; binary-controlled phases exp(pi i k_j/L) supply the phases.
Reflect about that state and uncompute all arithmetic. The nonzero sine
norm is >=2/L; O(n+log1/alpha) absolute bits suffice for operator erroralpha.
Classical elementary-function algorithms and reversible arithmetic cost
polynomial in those bits. Exact k=0 is recognized from the input bits.

For a chosen r, a product of r+1 Pi block encodings and r+2 material-phase
unitaries Sigma has top block Sigma Pi(Sigma Pi)^r Sigma. Use a FRESH
zero flag for every projection block. An ordinary Hadamard test between
the explicit initial eta_j and the full product unitary has expectationT_r.
It is a matrix-element experiment; NO success flags are postselected.
This also covers the exact zero-correction case without an inverse norm.

Sample r in{0,...,k-1} with probabilities z^r/Z, Z=sum_(r<k)z^r<=1/(1-z).
Multiply the Hadamard outcome by(-1)^r. Its expectation is
Z^-1 sum_(r<k)(-z)^r T_r, with variance<=1. Estimate the first material
mean by ordinary classical circuit sampling. Hoeffding/median bounds give
O_rho(epsilon^-2 log1/delta) total trials, each using O(k) material queries
and projection circuits. With k=O_rho(log1/epsilon), total gates are
poly(B,n,log1/epsilon)*epsilon^-2 log1/delta. Degree-sampling probabilities
are rational and finite length; a capped/dyadic sampler pays total error.
Allocate circuit error O_rho(epsilon/k) per reflection and all material
evaluation circuits exact. Controlled versions for the Hadamard test are
explicit because their complete gate descriptions are known.

This construction and the classical marked-path estimator evaluate the SAME
scalar finite series. Their difference is variance, not a changed source or
output contract. It is a written candidate composition using known LCU/
Fourier machinery; no novelty, speedup or execution is inferred.

### Finite-bit simplification for the classical sampler

Reviewed parent repair: weighted local-TV estimates and clipping are
unnecessary if we couple the ENTIRE capped computation. First define the
ideal marked estimator with a finite dyadic time grid and exact Poisson
counts, and choose the finite number R of median-of-means paths from its
proved second-moment bound. There are at most F=4Rk independent Poisson
draws across paths (plus the explicitly bounded choices of degrees/means).
Set per-draw TV allowance beta=delta/(16 max(1,F)). For each rational t,
choose integer Q>=max(t,2t^2/beta), replace Poisson(t) by Binomial(Q,t/Q),
and sample that binomial to TV<=beta/2 with the reused finite-clock lemma.
Le Cam coupling gives total per-draw error<=beta, hence whole-transcript
TV<=F beta, regardless of how large the signed weights are. Do NOT use
TV to bound their unbounded expectations; use it to transfer the success
event of the capped estimator. The final answer may be clipped to[1,rho].

Every actual count is in[0,Q]; every weight is rational with bitlength
polynomial in logT,logF,log1/delta and dyadic time precision. Each product
of at most k weights has polynomial bitlength in those parameters and k.
Round EACH completed path product to a common dyadic absolute precision
before averaging; distinct time numerators otherwise create incompatible
rational denominators whose sizes can accumulate with R. This deterministic
rounding contributes at most its chosen precision to each group mean and
median. Common-denominator sums then add only O(logR) bits. Although R can
be quasi-polynomial, logR is polynomial
in k,log(n+loglog1/epsilon),log1/epsilon,log1/delta. The binomial generator
runs in polynomial BIT work per draw; no numericT or numericQ loop appears.
This gives a complete bounded-clock realization of the same asymptotic
classical estimate once the ideal marked/series bounds are accepted.

For clarity, use F_-(k,x)=exp(-2pi i k.x/L)/sqrt(N). Then the forward
difference has symbol exp(+2pi i k_j/L)-1. In the quantum construction let
A_k=diag(exp(pi i k1/L),exp(pi i k2/L))*R_y(2theta),
theta=atan2(sin(pi k2/L),sin(pi k1/L)); at k!=0 the direction reflection is
A_k(I-2|0><0|)A_k^*. This fixes the Fourier sign and rotation-angle convention.

## Quantum review and source scope

audits/reviews/2026-11-12-conductivity-quantum.md is a completed independent
proof, fully parent-read. It verifies the finite-series all-circuit upper
bound and supplies a finite inverse-CDF degree sampler and full error budget.
Use U_Pi=(H tensor I)diag(I,-Rgrad)(H tensor I); the CONTROLLED minus sign
is essential. If the input bit f=1 denotes rho then Sigma=2f-1, the negative
of the common(-1)^f phase; that controlled sign also must be retained.
The explicit n>=1 model avoids the trivial L1 torus; it is directly soluble.
Known LCU/product machinery is prior art: actual Gilyen1806.01838 Lemmas52/53
was read, including the separate-ancilla requirement. No quantum code was built.

Let C*=max(1,c z^2/(1-z)). Choose the series tail<=epsilon/4, degree law TV
<=epsilon/(16C*), and reflection operator error<=epsilon/(8C*k). A combined
bounded trial Y=c+c z sigma-c z^2 Z(-1)^r h has contrast-bounded range;
O_rho(epsilon^-2 log1/delta) independent trials estimate its mean. Bias from
degree/synthesis plus statisticalepsilon/2 stays belowepsilon. Degree
probabilities are rational: floor the cumulative probabilities onto a b-bit
dyadic inverse-CDF grid with k/2^b total variation, using exactly b fair bits.
The complete written quantum gate bound is established by this proof, not
by a passing finite control or the truncated paid QSVT review.

Classical signed path Monte Carlo is also established machinery, not a new
principle. Actual Stahlke1305.2186 Definition6 explicitly requires efficient
sampling AND ratio evaluation, beyond an abstract low-interference norm.
Our marked heat-kernel construction directly pays a particular sampler;
we do not silently grant the dense kernel access required by that framework.
Novelty and a full polynomial classical match in both parameters remain
unestablished. The completed classical review and dispositions follow.

## Classical review, paid-report dispositions and decision

audits/reviews/2026-11-12-conductivity-heat.md is a completed independent
proof, fully parent-read. Its conservative finite experiment is authoritative:
take k>=1 with c z^(k+2)/(1-z)<=epsilon/8,
 tau=epsilon(1-z)^2/(32c), a=epsilon(1-z)/(8c),
 T=2^J>=max(1,(L^2/16)ln(2/tau)), h<=tau/(32T), H^2=64(J+1)^2.
The FULL block integrand derivative has norm<=64. This grid and cutoff give
operator error<=tau; no l1 tail estimate is assumed. Use
 s_r=ceil(8H^(2(r+1))/a^2), g=8ceil(log2(4k/delta))+1,
 R=g sum_(r<k)s_r, U=g sum_(r<k)(r+1)s_r, F=4U.
Round each completed path product to a common dyadic spacing<=a before
forming the group means/medians. Cap interval-index rejection at
ceil(log2(16U/delta)) attempts. With beta=delta/(16F), a common power-of-two
Q>=max(T,2T^2/beta) and binomial sampling TV<=beta/2 couple all count draws
to the ideal experiment with error<=delta/16; all interval choices add at
mostdelta/16. The complete bias/statistical/failure allocation in the review
is belowepsilon/delta. This is a bounded algorithm, not an expected-time
claim or an expectation bound from total variation of unbounded weights.

Hence, for EVERY native circuit at fixed contrast, the written classical cost
is poly(B,n,1/epsilon,log1/delta,native scalar bits) times
 [n+loglog(e^2/epsilon)]^O_rho(log(1/epsilon)+1).
For fixed precision this is polynomial in B,n. For epsilon=n^-a, fixeda>0,
it is poly(B,log1/delta,nativebits)*exp[O_rho,a(log^2 n)]. Full polynomial
dependence jointly in n and1/epsilon remains OPEN.

Paid packets and dispositions (all parent-read; paths relative to audits/):
- openai_runs/2026-11-12-conductivity-classical: completed. Independently
  derives heat-kernel signed sampling and the same asymptotic classical
  upper bound, plus reflection acceleration. Parent checked the energy,
  Poisson signs, Fourier remainder normalization and variance logic. Its
  asserted4096 Poisson-rejection envelope is not sufficiently derived to
  import; the reviewed binary-binomial whole-transcript construction pays
  that operation instead. No second Poisson backend is built.
- claude_runs/2026-11-12-conductivity-endpoint: TRUNCATED midway through
  unitary construction. ENERGY/model/zero-q discussion is useful and
  independently verified; its assertion that the full algorithm is closed
  is not a completed review. The later elementary-series proof supplies
  the complete endpoint. No retry or claim from its proposed detailed gate
  count; that count was not fully substantiated in the returned fragment.
- claude_runs/2026-11-12-conductivity-heat: TRUNCATED at final corrections,
  with substantive ideal and clipped-kernel reasoning. Parent checked
  MARKS/variance/series; rejected l1 wording for time truncation, repaired
  full-matrix quadrature, bounded interval selection and rational-sum bits.
  Its speculative inherent row-l1 lower bound is not used. The separate
  completed review validates the final whole-transcript implementation.

The accelerated baseline is known Eyre--Milton machinery, confirmed in the
actual1711.05880 equations12-18,37-43. Parent also rederived it: with
 Rref=2Pi-I, r=(sqrt(rho)-1)/(sqrt(rho)+1),
 K_j=sqrt(rho)[1+2 sum_(m>=0)(-1)^m r^(m+1)
                    <eta_j,Sigma(Rref Sigma)^m eta_j>].
Use E=(I-rSigma)w, J=sqrt(rho)(I+rSigma)w and the projected field equations
to obtain (I+rRref Sigma)w=eta. The tail is bounded by
2sqrt(rho)r^(M+2)/(1-r); this improves contrast constants, not the above
fixed-precision versus joint-polynomial boundary. The same paid Pi sampler
gives Rref by a signed mixture with identity. No novelty is assigned to it.
The independent report's growing variance on even easy layered inputs is
a warning about ITS independent signed estimator, not a classical lower bound.

Frozen control: audits/controls/periodic_conductivity/control.py and result.json,
ONE Sage run, exactly six L4/rho2 cases. Parent read script and result fields.
Direct rational minimization equals the projection energy in every case.
Constant K=(1,1); layer K=(4/3,3/2); nonlayer K=
(12247689/9496630,5880256/4748315). Zero-q cases and six-term Neumann tails
pass. This neither runs the succinct estimator nor proves its scaling.
No further quantum simulation, grid sweep or kernel numerical test is needed
to establish the algebraic identities; the written proofs carry them.

DECISION: retain a completely paid written quantum scalar algorithm, with
a constructive classical match at fixed precision. Reject the full-grid-only
case for an exponential fixed-accuracy advantage. No complete field output,
growing contrast, general elliptic PDE theorem, novelty, practical advantage,
hardness, separation or quantum execution is claimed. The inverse-polynomial
precision case is unmatched by the established upper bounds, not hard.

Next scientific action: independently reselect by external value. This line
re-enters for a concrete classical variance-reduction theorem polynomial in
BOTH parameters, or a motivated native endpoint with a new paid mechanism.
Do not add a PDE framework, more mesh plots, or another source/readout wrapper.

## 2026-11-13 completed shortcut pass and priority pivot

The scoped full-output nearby-band falsifier and two specified sampler variance
attacks are checked; details in CONDUCTIVITY_SEPARATED_SCALE_ATTACK and
CONDUCTIVITY_MULTISCALE_API_DISPOSITIONS. No generic classical lower bound.
Independent heat sampling remains the strongest general written comparator:
polynomial at fixed epsilon, quasipolynomial for inverse-polynomial epsilon.
Joint-poly matching is OPEN. A return requires a concrete cancellation-
preserving contraction with paid work/second moment, not another nearby
barrier. Current selection is the native dyadic half compiler; no new quantum
implementation or speedup/novelty claim.
