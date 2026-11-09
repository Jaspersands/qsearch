# Two Gaussian channels: diamond-distance learning admission

2026-11-07. CLOSED WRITTEN composition after five independent source/core/physical/
robustness/final reviews. EVERY exact memoryless mixture of TWO full ordinary
Gaussian CPTP channels has a polynomial-use/BIT/gate learner with an explicit
CPTP output circuit at full raw diamond error epsilon, success>=1-eta.
No weights, branch labels, separation, source environment or inverse are supplied.
Nonadaptive PRODUCT preparations and Pauli readout supply all data; reconstruction
is classical. No coherence/computational advantage, novelty, practical-cost,
human/formal verification, full learner implementation or quantum execution.
The initial OPEN sketches below are retained as derivation history; the complete
composition and final review supersede them. See the final scope section.
Start: STATE/TRAPS match CSA Minimal Modules and Primitive Idempotents.
Previous pass was PROGRESS (reviewed construction, evidence and records).

## Native question and independent choice

Input: fresh ordinary uses of a fixed memoryless n-qubit channel E=p G1+(1-p)G2,
with unknown p and unknown n-mode fermionic Gaussian CPTP components. No branch
label, environment, Stinespring unitary, inverse, controlled channel or parameter
separation is supplied. The FULL ordinary channel is defined by an even Gaussian
unitary on SYSTEM,ENV, with Gaussian environment purified/prepared from vacuum
using O(n) modes, followed by ordinary trace of the LAST environment. This is
not merely the action on even inputs. Use REF,SYSTEM ordering and the even BCS
maximally entangled state Omega=2^(-n/2) sum_x (-1)^binom(|x|,2)|x,x>.
Then J_G(E)=(I_REF tensor E)(Omega) is Gaussian for each component: in
REF,SYSTEM,ENV, quadratic generators on the last registers cancel both
reference parity strings. Ordinary last-register trace preserves Gaussianity.
Omega=(V_REF tensor I)Bell, V=product_(j<k)CZ_jk, a known O(n^2) reference-only
gauge. Thus ordinary CJ and J_G differ only by V, preserving marginal I/2^n.
The source/convention review is closed in
audits/reviews/2026-11-07-gaussian-channel-sources.md. First-half action without
the source's global parity correction is NOT interchangeable with this route.

Target: explicit CPTP preparation/use circuit for Ehat with
||Ehat-E||diamond<=epsilon, success>=1-eta, polynomial(n,1/epsilon,log1/eta)
ordinary channel uses, classical BIT processing and gates. Output may be an
improper learner; it must be a usable channel, not just a normalized Choi state.
This is a quantum-data learning task, not a classical-input speedup claim.
Expected benefit is polynomial learning for a physical switching-noise family
versus unrestricted channel tomography; no classical computational lower bound.

Selection compared independent directions after corpus lookups and literature:
(1) succinct polynomial symmetry retains the classical orbit-module filter;
(2) growing-center quaternion PIP still has an unpaid integral/norm-constrained
operation (the last compact CSA result does not pay it); (3) growing-degree
Legendre reconstruction retains its factorial split-source bound, and no new
joint-label operation was identified. This channel task has a specific new
constructive mechanism: proper Gaussian component recovery at high effective
rank, and a constant-mode CP processor at low rank. It is selected for the
externally useful WORST-INPUT channel endpoint, not merely another state variant.

Corpus been-tried: Gaussian channels mixture Choi diamond learning; baselines:
fermionic Gaussian mixture channel diamond distance tomography. Catalog returned
tensor networks. Stronger matched baselines: supplied-component Gaussian/Wick
simulation and classical processing of measured moments; actual published FLO
and few-nonGaussian-UNITARY diamond learners. Arbitrary channel mixtures need
not be few-gate unitaries. Actual2608.05307 AppendixC TheoremC.2 is BOSONIC,
with Gaussian-measurement-conditioned outputs; it is not a lower bound for this
fermionic mixture-of-two-CPTP-Gaussian-maps promise. Sources fetched under
audits/sources/gaussian_channel_selection.

Cheapest falsifiers: two promised mixtures with exponentially close normalized
Choi states but constant diamond distance; Gaussian covariance perturbations
whose full-channel distance is uncontrolled; state reconstruction that breaks
trace preservation; a constant core that still needs exponentially rare Bell
postselection; parity/Jordan-Wigner mismatch. Generic Choi tomography has an
exponential dimension factor and is NOT itself a channel learner. No quantum
implementation or benchmark is admitted before these gates.

## Candidate route and current obligations

MIXED_GAUSSIAN_PAIR_LEARNING.md already pays polynomial-copy/BIT reconstruction
of an exact mixture of two mixed Gaussian STATES. Its final output can be an
improper mixture of four Gaussian states. This does not preserve the input
marginal constraint and therefore cannot be imported as a diamond learner.
High effective covariance-difference rank gives estimates of the actual two
components/weights; enforce the reference block0 and physical covariance LMI
by a polynomial-size convex projection. This requires a uniform diamond
continuity theorem for individual Gaussian channels and a paid small-weight
branch, both OPEN here.

Low effective rank needs a channel-specific endpoint. For EXACT rank<=4
covariance difference and a strictly mixed common regularization, the existing
state lemma factors both Choi states through one Gaussian CPTP state map Psi
from at most two modes to the full output/reference system. Write its covariance
map Gamma -> L Gamma L^T+Z. Let sigma be the core mixture and R be the reference.
Trace preservation of the target gives
  0=Gamma_target,R=Z_R+L_R Gamma_sigma L_R^T.
Hence Z_R is supported on im(L_R), whose dimension is at most4. After a known
reference-only Gaussian rotation, the FULL marginal channel Psi_R has output
  T(tau) tensor I_rest/D_rest
for every core state tau (not merely the Gaussian tau), because Gaussian-channel
characteristic functions factor and all nonconstant core variables enter im L_R.
T acts from a constant-dimensional core to at most two reference modes.
Thus exact TP of the candidate reduces to T(tau)=I_h/h, a constant-size linear
constraint. Physical core repair can be posed as a constant-dimensional SDP.
This is an exact structural observation, not yet a stable noisy reconstruction.

## A general CP norm lemma (independent exact review accepted)

Let Psi:M_r -> M_D tensor M_D be CP/TP, and suppose after a known unitary on
its reference output, Tr_output Psi(tau)=T(tau) tensor I_D0/D0,
where D=h*D0 and T:M_r->M_h is CP/TP. Define Phi_tau by normalized Choi state
J(Phi_tau)=Psi(tau). It is CPTP exactly when T(tau)=I_h/h.

Here J means ORDINARY normalized Choi, after the known reference gauge.
Take the normalized Choi state J(Psi), rearranged with its two reference
registers as the joint input of a CP map Lambda:M_r tensor M_D -> M_D.
Its unnormalized Choi matrix is r*D*J(Psi). Feeding program tau gives
J(Phi_tau)=Psi(tau), by the usual link product. Moreover
  Lambda^dagger(I)=transpose(r*h*J(T) tensor I_D0),
up to the known register/unitary ordering. Therefore
  ||Lambda||diamond=||Lambda^dagger(I)||infinity<=r*h,
since J(T) is positive of trace1. For all core states tau,sigma,
  ||Phi_tau-Phi_sigma||diamond <=r*h*||tau-sigma||1.
The full transpose, not a partial transpose, occurs in the effect formula.
The reference factorization holds on all core operators by the Gaussian map's
Majorana-monomial adjoint: any monomial with a rest index vanishes. Independent
review accepts these exact statements; physical compilation is separate.
No full-input factor D appears. The program dimensions r,h are constant in
the exact low-rank construction. This is a NORM bound only: reshaping a known
large Choi state does NOT automatically provide an efficient circuit Lambda.

Efficient physical endpoint OPEN: exploit that Psi is Gaussian, so Lambda is a
Gaussian CP map with trace effect confined to program plus O(1) input modes.
If one can compile Lambda/(r*h) by Gaussian dilation and a constant-mode filter,
feasible tau would have success1/(r*h), independent of the unknown channel input.
Failure cannot consume an unknown input and then be silently retried; the final
learner needs a deterministic CPTP realization, or a heralded failure branch
whose probability is reduced without reusing consumed input. A mere constant
postselection probability is not a deterministic channel approximation.
This is the sharp constructive blocker, not a free postselection primitive.

Additional OPEN gates: uniform approximate rank/weight classification; CP/TP
preserving truncation with only constant rank enlargement; transfer from an
attenuated Choi model to original channel in diamond norm; exact ordinary
channel convention; polynomial compilation and all finite clocks.
No algorithm or speedup follows from the CP norm lemma alone.

## Further hard checkpoints, still not a complete learner

Independent derivation gives, for the FULL Gaussian dilation channels,
  ||G(A,B)-G(A',B')||diamond <= min(2,200 n sqrt(alpha+beta)),
where alpha=||A-A'||op and beta=||B-B'||op. Use M=I-AA^T+iB>=0,
sqrt(M)=U+iV, row frame [A,U,V], a fixed pure Gaussian environment, square-root
Holder continuity and a close orthogonal frame completion. Actual FLO stability
Proposition2.6 then pays the full ordinary diamond norm, without a CP gap.
The source excludes inferring full channel action from even covariance inputs.
Closed proof review is being saved separately.

Physical processor proposal under independent attack: Gaussian J_G(Psi) has
ordering P,R,O. The desired ordinary processor CJ gauge is V_P V_R, whereas a
Gaussian map Lambda_G with combined input P,R uses V_(P,R)=V_P V_R W_PR.
Thus Lambda=Lambda_G composed with Ad_W_PR, where W_PR is a known cross-CZ
parity gate on actual program/input registers, O(n) gates for constant program.
Do not silently call the ordinary reshuffle Gaussian. Gaussian purification
and Schmidt decomposition of Lambda_G's CJ may compile it with filters only
on constant many input modes, since its trace effect has constant support.
For feasible known program, the normalized success block obeys K^dagger K=I/C,
C=r*h. Exact phase-matched oblivious amplitude amplification of the COMPILED
circuit and its inverse could make this deterministic, retaining all Kraus
environment. It uses neither inverse source access nor consumed-input retries.
Compilation and this amplification claim remain under independent review.

Near-TP repair proposal: for a learned positive program tau, the effect F of
Phi_tau is known and confined to h input dimensions after the known rotation.
If ||F-I||<=delta<1/2, normalize Phi_tau by input conjugation F^(-1/2).
This is CPTP and changes it by O(delta), with no ill-conditioned linear
feasibility inversion. Implement the constant-mode filter and amplify the
combined constant-success circuit. This removes exact core-SDP feasibility
only after the physical processor is established.

Robust endpoint plan, NOT YET CLOSED: let k=(epsilon/[10^8(n+1)])^2, internal
state-reconstruction parameter u=k^2, attenuation margin k, h=u^8, ell=u^40,
moment error u^10000. Reuse high-rank algebra/finite clocks at u (all earlier
inverse bounds remain conservative with the larger physical margin k).
For low-rank support S of dimension4, enlarge to S+P_REF S (dimension<=8)
and subtract the RR block of the truncated difference. This preserves TP and
costs at most twice the discarded covariance error; the core has <=4 modes.
Mean projection must enforce RR=0 and the strict physical LMI together.
Reconstruct all core moments up to degree8; the constant inverse loses at
most k^-O(1). Small-H output as a mean Gaussian needs a special rank2 repair:
an almost rank2 skew difference with RR=0 must admit a nearby rank2 difference
with RR=0, at square-root error. That geometry is the next cheap falsifier.

Two initial Claude requests ended max_tokens with EMPTY reports, not reviews:
gaussian-channel-choi USD1.674280 and gaussian-channel-processor USD0.669952,
both32768 output tokens. Terminal known usage, no retry or inferred findings.

## Complete reviewed composition

This supersedes the earlier endpoint sketches. Reviewed written theorem: for EVERY
exact native mixture, an explicit ordinary CPTP circuit is returned within raw
diamond epsilon, with probability>=1-eta, using polynomial(n,1/epsilon,log1/eta)
fresh channel uses, classical BIT work and gates. No weight/gap/branch advice,
source dilation, inverse or controlled-source access. No practical-cost,
novelty or computational-separation claim. The exact, robust and physical
reviews are separate ingredients; the final composition review is closed and
was read in full: audits/reviews/2026-11-07-gaussian-channel-composition.md.

For n>=2,0<epsilon<=1/10 set
  k=(epsilon/[10^8(2n+1)])^2, u=k^2,
  t=1-k, h=u^8, ell=u^40, zeta=u^10000, reconstruction arithmetic=u^12000.
For n=1 ordinary constant-size CPTP Choi tomography/dilation suffices; n=0 is
trivial. Measure ALL even Majorana moments through degree8 of corrected Choi
copies. Nmom=O(n^8), copies/observable=ceil(2 zeta^-2 log(16 Nmom/eta)).
The simultaneous event covers ADAPTIVELY chosen frames: exterior Euclidean
error is O(n^4 zeta) and orthonormal restriction contracts it. Transform
moments classically; no new source or independence assumption is needed.

Scale degree2j moments by t^j. These are exactly the moments of the mixture
with branch covariance t Gamma_j, still RR=0 and with physical margin k.
Channel parameters become t A_j,t B_j; gap-free continuity costs at most
300 n sqrt(k) diamond. No attenuated-channel oracle is invoked. Degree8 and
dimension factors fit the reused u^9900 array-error reserve. Reuse the state
learner's measured h/ell tests, capped six-restrictions and u^300 inverse
guards. Its state-mode parameter is now2n, and physical margin k>=u only helps.

### Small H: a TP-preserving rank-two repair

For the coefficient Euclidean exterior norm, ||H||<=3h implies the second
skew singular value of E=sqrt(pq)Delta is <=sqrt(3h/2). If min(p,q)<=k^8,
the mean Gaussian channel is within O(n k^4)+2k^8 of the mixture by comparing
to the larger branch. This weight split is ANALYSIS ONLY, never an input.
Otherwise pq>=k^8/2, and the top-pair truncation B of Delta has error O(k^4).

Uniform geometric lemma: if RDR=0, ||D||<=2, rank(B)<=2, ||D-B||<=delta<.01,
write B=s u wedge v with orthonormal u,v and rotate so Ru is orthogonal to Rv,
||Ru||<=||Rv||. Then s||Ru||||Rv||<=delta. Taking
  B0=s ((I-R)u) wedge v
preserves rank<=2, gives RB0R=0, and costs
  ||D-B0||<=delta+sqrt((2+delta)delta)<=1.52 sqrt(delta).
No small singular value is inverted; s=0 is immediate. Here this is O(k^2).
Set Gamma1'=mean+q B0 and Gamma2'=mean-p B0. They retain RR=0 and margin>=k/2.
Every Pfaffian is affine in this rank2 difference, since B0 wedge B0=0.
Their mixture is EXACTLY the Gaussian mean, and individual full-channel
continuity costs O(n k). Output the estimated physical Gaussian mean after
joint projection onto the skew covariance ball and RR=0. Estimation contributes
a negligible polynomial factor times sqrt(u^9900).

The square-root repair cannot be improved uniformly: R onto e1,e2,
u=sqrt(delta)e1+sqrt(1-delta)e3, v=sqrt(delta)e2+sqrt(1-delta)e4, and
D=u wedge v-R(u wedge v)R. Distance to a rank2 matrix is delta, whereas every
TP rank2 B0 has reference/output cross-block rank<=1. RD(I-R) has TWO singular
values sqrt(delta(1-delta)), forcing that much repair error. This is an
analytic all-delta counterexample, not a scaling inference from fixtures.

### Low third eigenvalue: invariant support and physical core

The reused state estimates yield an estimated rank4 projector P with
||Delta-P Delta P||<=u^10, or u^9 after slack. SVD the REFERENCE and OUTPUT
parts of its four-column frame SEPARATELY, retaining values above theta=u^20
with numerical guard band[theta,2theta]. A constant grid avoids the at-most8
observed singular values by a constant multiple of theta; no input gap is
promised. Pad each retained part to even
dimension<=4 using known coordinate vectors. The resulting Q commutes with R,
rank(Q)<=8, and ||(I-Q)P||=O(theta), without a principal-angle gap. Only retained
values are inverted (bound theta^-1). Thus
  Delta'=Q Delta Q, R Delta' R=0,
  ||Delta-Delta'||<=2||Delta-P Delta P||+O(theta)<=u^8.
This improves the earlier sketch: no RR block subtraction is required.

Project the measured mean onto skew RR=0 matrices of norm<=1-k/2. The true
attenuated mean is feasible; Frobenius error increases only by the numerical
tolerance. Weak polynomial-precision convex projection suffices, with explicit
interior point0 and paid radius/margin. Enforce skew/RR linearly and shrink
by the certified final norm tolerance for an actually physical description.
For analysis set Gamma1'=mean_hat+q Delta', Gamma2'=mean_hat-p Delta'. These
are proper Gaussian channel covariances with margin>=k/3, differing from the
attenuated source by O(u^8). Channel replacement costs O(n u^4).

Construct the Schur map Psi from mean_hat,Q using the preceding formulas.
Its input core has <=4 modes; Rcore>=k/3. The nearby mixture is Psi(sigma)
for a physical even sigma, never supplied. Psi's reference support lies in
T_REF, dimension<=4 Majoranas. Consequently r<=16,h_ref<=4,Cprog=r*h_ref<=64.
The all-operator constant-reference-marginal lemma applies.

Restriction to Q removes the discarded covariance tail EXACTLY: the nearby
branch's projected covariance differs from the true projected branch only by
Q(mean_hat-mean_true)Q. Pfaffians of size<=8 are Lipschitz by at most4 times
this error. Thus the discarded u^8 tail is NOT amplified through a core inverse.
For d<=8 core Majoranas, invert the moment map by multiplying the Grassmann
polynomial by exp(-quadratic(A0)), then substituting Rcore^-1/2. Its norm is
at most C_d (k/3)^(-d/2)<=C_d' k^-4. Noise coefficients are bounded Pfaffians.
Reconstruct the even trace-one density matrix, clip its negative parity-block
spectrum and normalize (trace error factor<=3). No branch weights or density
eigengaps are inverted. Threshold/SVD/Schur/exterior operations lose fewer
than1000 powers of u: theta^-1=u^-20, retained dimension<=8, remaining inverses
polynomial in k^-1. Reserve ||tau-sigma||1<=u^8000 conservatively.
Full independent robust proof: audits/reviews/2026-11-07-gaussian-channel-low-rank.md.

### Near-TP normalization and deterministic physical use

The CP program norm bound gives ||Phi_tau-Phi_sigma||diamond<=Cprog d_core=v.
Hence F=Phi_tau^dagger(I) obeys ||F-I||<=v. F is a known h_ref-dimensional
matrix tensor identity, up to known rotation, V gauge and transpose. For
v<=1/2, B=F^-1/2 has ||B||<=sqrt2 and ||B-I||<=v. Thus
  Q_tau=Phi_tau composed_with Ad_B
is exactly CPTP and differs from Phi_sigma by <5v (reserve10v). This avoids
inverting a possibly ill-conditioned affine TP constraint. The explicit
constant-dimensional guard F>=I/2 either passes or returns ABORT on bad data.

Compile Lambda/Cprog as in the exact physical review, including actual-input
cross-CZ. Prepend B/sqrt2 and known program purification. Its successful
Stinespring block satisfies K^dagger K=I/(2 Cprog). Coin dilution and
O(sqrt(2 Cprog)) Grover rotations make the ideal isometry deterministic.
Only the known compiled unitary and its inverse are used, all Kraus work kept.
No consumed-input retries, source inverses or postselected output remain.
Ordinary qubit gates are allowed; Gaussian-only output is not promised.

Finite precision is controlled in Stinespring/operator norm, never by
multiplying normalized Choi error by dimension. Request successful-Stinespring
error u^1000 and use a Schmidt cutoff u^1500. Compiler-internal working
precision is a SEPARATE finite polynomial clock supplied by the physical lemma:
retained-link inverse<=2u^-1500, bulk links1, residual polar condition bounded.
Choose primitive evaluation tolerances from these explicit operation bounds
and the target residuals, with fixed finite accurate-matrix/gate routines.
This reevaluates the KNOWN learned finite-description model; it does not require
more data, an unbounded refinement loop, or a universal12000-power compiler
roundoff assertion. The reconstruction arithmetic setting is unchanged.
The physical review's near-TP/small-link cutoff addendum is CLOSED. Discard
constant-core links below a chosen tolerance with direct operator error; bulk
links equal1, retained links have a paid inverse, and the residual polar
completion is uniformly conditioned. Robust amplification depends only on
successful-block singular values, not closeness of arbitrary failure dilations.
The final unitary circuit followed by discard is always CPTP, including residual flags.

### High branch, finite clocks and total ledger

Reuse high-rank exterior recovery at parameter u: true weights>=u^42, inverse
guards u^300, branch covariance error<=u^8000, weight error<=u^8300. Jointly
project each covariance onto physical skew matrices with RR=0, then certified
tiny shrink. True branches are feasible, so error grows only polynomially.
Single-channel continuity gives a conservative O(n u^3000) diamond error;
weight error is paid in total variation. Compile known Gaussian channels by
the square-root row dilation, sample the known weight and discard environment.

Random restrictions are capped at ceil(4*3^12 log(8/eta)); failed guards ABORT.
Moment and random-clock failure sum to <=eta/2. All algebra has finite clocks.
Attenuation costs<=300n sqrt(k), largest branch error O(n k), and gate synthesis
is allocated epsilon/20. The displayed k leaves ample constant slack for total
raw diamond error<epsilon. Query count O(n^8 u^-20000 log(n/eta)); classical
matrix/precision clocks and circuit size are polynomial. These huge sufficient
exponents are neither optimized costs nor lower bounds. Final independent composition review accepts this WRITTEN end-to-end contract;
implementation/execution and novelty/separation remain explicitly unclaimed.

## Checked Claude findings and exact classical falsifiers

Fable/high gaussian-rank-two-repair: completed17072 output tokens,
estimateUSD0.863400. Accepted uniform1.52sqrt(delta) repair and analytic matching
lower exponent. Its corollary uses the repository coefficient Euclidean norm;
charge BOTH channel parameter blocks in continuity (extra sqrt2 versus its
shorthand). Its source promise is independently established, not imported.
Opus/high gaussian-core-inverse: completed16328 output tokens,
estimateUSD0.329628. Accepted exact bounded inverse, PSD repair and restricted
Pfaffian Lipschitz bound. Its optional rotated-measurement plan is unused; no
universal necessity of polynomial k^-1 in every learning task is imported.
These are checked lemmas, not completed full-learner reviews.

Exact CLASSICAL Sage control: audits/controls/gaussian_channel_admission.
Corrected Omega passes127 even Wick identities, marginalI4/4 and reference-CZ.
Raw ordinary Bell fails15 identities (first indices0,1,2,7: actual-1/Pfaffian0).
Complex-core CP linking matches all4 matrix units with the required transpose;
without it tau^T is returned. Effect spectrum4,4,0^6 has norm4<=8. Non-TP even
core gives trace2 on E00. These are convention/normalization falsifiers and a
supplied-component classical Wick baseline, not learner execution or scaling.

## Stronger matched experimental baseline: no coherent query advantage

Every measured corrected-CJ Majorana monomial is an ordinary Pauli
P_R tensor Q_O. Conjugating the reference factor by the known Clifford V_R
and transposing gives a signed Pauli P on the input. The desired expectation
is exactly Tr[Q E(P)]/D. For P!=I, sample b uniformly from+-1 and uniformly
sample local Pauli eigenvalues with product b, using random Z bits on identity
positions. The resulting product-state ensemble has density
  rho_b=(I+b P)/D.
Measure output Q after one ordinary channel use; if m is its signed product
outcome, E[b*m]=Tr[Q E(P)]/D. For P=I use I/D. Known transpose signs are included.
Therefore the ENTIRE data acquisition can use nonadaptive product preparations,
classical randomness and single-qubit Pauli readout, with the SAME bounded
variance and query count. The reconstruction is already classical processing.
This is a stronger matched baseline than supplied-component Wick simulation.

Consequently no coherent-query, entangled-reference or computational quantum
advantage is established by this learner. Its constructive value is a succinct
worst-input-accurate physical channel model/circuit for a structured family.
The efficient output circuit and full diamond guarantee still require the
proved processor and robustness, but one must not present Choi access as an
inherently stronger learning resource. This baseline should affect the next
independent direction selection; do not extend this line by inertia.

## Final scope and research decision

Five closed reviews were read and their obligations incorporated: source convention,
single-channel continuity/program norm, physical processor including near-TP/cutoff/
robust amplification, low-rank geometry, and full composition. Six primary source
snapshots are retained across the selection and reused mixed-Gaussian directories.
One exact supplied-component Sage control checks conventions and CP linking; it
does NOT execute the learner. Four terminal Claude bundles cost an estimated
USD3.537260: two empty truncations and two useful checked lemmas, no live request
or retry. No evidence from empty output was imported.

Established: the written uniform polynomial-query/BIT/circuit construction under
the exact native promise; uniform TP rank2 repair with a sharp square-root
exponent; gap-free single-Gaussian diamond continuity; a constant-core deterministic
processor and stable effect normalization. Falsified shortcuts: naive ordinary
Bell-as-Gaussian, omitted program transpose, TP inferred from a positive core alone,
and any claim that these data inherently require entangled probes.

Assumptions retained: exact full ordinary Gaussian Stinespring components, fixed
memoryless two-map mixture, known physical Majoranas, exact ordinary channel uses,
and ordinary qubit operations. No off-model guarantee, many-component extension,
parity-restricted implementation, human/formal proof audit, practical-cost, novelty,
classical hardness or computational speedup is established. No full learner or
quantum circuit execution occurred. Finite controls never supply the theorem.

Next research action is independent direction selection from STATE/TRAPS, corpus
then literature and matched baselines. The product-query baseline lowers this
line's priority for Shor-level algorithm discovery. No Gaussian learning backend,
nearby rank variant, numerical sweep or demonstration is queued.

Scoped milestone PASS: STATE/handoff/mechanical titles match; six source PDF
hashes, five closed reviews, exact control receipt/syntax/false claim gates and
four terminal API prompt/usage snapshots checked. Pass estimateUSD3.537260.
Scoped git diff --check passed. No full suite, repeated control, Git commit or
push. An initial bookkeeping check required a case-insensitive closure label;
no scientific artifact or claim was changed to satisfy that label check.
