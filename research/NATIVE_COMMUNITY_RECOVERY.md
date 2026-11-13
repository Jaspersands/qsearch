# Native multi-community weak recovery

2026-11-13. Selected constructive candidate; full recovery theorem OPEN.
STATE/TRAPS and corpus been-tried/baselines preceded the primary-source
comparison. Rank-purity is parked. The single question is whether the
existing native Kikuchi detector can output one correlated labeling, with
all source, classical baseline and finite-clock costs paid.

## Problem, mechanism and honest resource target

Input ONE explicit array of independent conditional Bernoulli p-hyperedges,
fixed even p=2d>=4, fixed k>=3, q=1/4, known rational epsilon. Labels x_i
are IID uniform[k], and edge means are q+epsilon*f_x(E), where
f_x(E)=sum_a product_(i in E)(1[x_i=a]-1/k). No labels, gauge, useful
vector/projector, independent planted graph, QRAM or preparation oracle.
Choose growing polylogarithmic ell, divisible by p for the existing quantum
compiler; ell=o(sqrt n). Let D=binom(ell,d)binom(n-ell,d).
Target signal epsilon²D>=C_(p,k)*ell. Known stronger signal may be
attenuated first to a known constant multiple of this frontier using fresh
null bits; the cloning analysis needs this near-threshold effective signal.
Output ONE z in[k]^n with max_permutation n^-1 count[z_i=pi(x_i)]>=1/k+c_pk,
with probability1-o(1) over input and internal randomness.

First prove the CLASSICAL endpoint in n^(ell+O_p(1))*poly(inputbits).
Only then compose quantum accepted-band preparation, one-particle tomography,
rounding and validation. Expected charged quantum upper bound is the already
compiled n^(ell/4)*exp(O_pk(ell logell))*poly(n^p,inputbits), with the
existing loglog terms outside ell~logn retained if needed. This is a target,
not a new speedup, best-classical dominance, practicality or Shor-level claim.

Strong baselines: existing classical native log-free detector; sharp Boolean
Kikuchi recovery; HCE/color-coded noisy-XOR algorithms; ordinary clustering
at stronger signal. The lower marginals of this model vanish, so ordinary
pairwise SBM is not an automatic comparator. Exact source contracts stay
attached. No low-degree or LCDF inference becomes general hardness.

## Checked source boundary

Full selection audits/reviews/2026-11-13-post-purity-selection.md compares
native recovery, short-path optimization and dissipative PDE output. The
latter two lack a new paid operation. Actual 2510.08494v1 Definition2 gives
this multi-color signal; conclusion LF649-652 leaves label recovery open
in that version. Its original guiding-source proof is NOT imported: use
the repository's independently checked NATIVE_COMMUNITY_SOURCE_REPAIR.md.

Actual 2607.29672v1 Section12.4 already gives accepted-band one-particle
mass, tomography and rounding for BOOLEAN noisy XOR. Section13's transfer
reveals a random literal vector and extracts its XOR channels. Our input is
one Bernoulli edge bit with multi-color means; it does not supply those
literals. These are prior techniques, not a direct HSBM theorem.

Actual Mao2604.10457v1 was fetched to audits/sources/2026-11-13-community-
recovery/; Definition1.3 LF220-254 specifies random Boolean parity samples
with independent sign noise. It is not an automatic multi-color native
recovery theorem. No literature-wide novelty claim follows. All current
arXiv versions checked Nov13. HCE2610.40941 remains a distinct strong
classical method; prior native adaptation paid detection, not recovery.

## Parent operation: energy pays one-particle mass

All following label objects are analysis only. Set w_a(i)=1[x_i=a]-1/k,
W_a=w_a*w_a^T, L=span{w_a}, and Lambda=binom(ell,d)*n^d. On ordered slots,

 B=sum_(J subset[ell],|J|=d) sum_a tensor_(j in J) W_a^(j).

Since W_a<=n*P_L and different-slot projections commute,

 tensor_(j in J) W_a^(j) <= n^d/d * sum_(j in J) P_L^(j),
 B <= k*Lambda/ell * sum_j P_L^(j).

The existing exact native certificate supplies, on collision-free tuples,
||Pi B Pi-K_x||<=k*d²*binom(ell,d)*n^(d-1)=O_pk(Lambda/n).
For a unit collision-free state of positive observed Rayleigh quotient,
subtract the already paid uniform centered-noise bound and this error. If
its signal energy is >=a_pk*Lambda, the one-particle average rho satisfies
Tr(P_L rho)>=a_pk/k. The same statement is linear for mixed states and
applies to every accepted-band state, with small trace error paid. It does
NOT require a full k-block gap, a special top eigenvector or known labels.
All factorials/set-versus-ordered scaling require independent checking.

A classical unit high-Rayleigh vector should come from O(log N) exact
integer powers, N=binom(n,ell), with Rademacher starts, as in the detector.
Check its Rayleigh quotient directly; repeat logarithmically with a fixed
cap. This avoids constructing a full projector. For set amplitudes v,

 rho_ij=(1/ell) sum_(|T|=ell-1,T disjoint{i,j})
                     v_(T union{i}) conj(v_(T union{j})),

with the analogous diagonal sum. It costs n^(ell+O(1)), trace is one.
Quantumly use the average over ordered slots, or the exact set deletion
isometry. No full lifted-space tomography is needed.

## Parent rounding operation, conditional only on the mass bound

Take real part R=Re(rho), a real PSD trace-one matrix. On the IID balance
high-probability event n_a>=n/(2k), the nonzero eigenvalues of sum_a W_a
are at least n/(2k): on 1^perp in color space, W^T W has quadratic form
sum_a n_a*u_a². The constant mass Tr(P_L R)>=eta implies a leading constant-
dimensional eigenspace V with Tr(P_L P_V)>=eta/2, since R<=P_V+alpha I
for alpha<=eta/(2(k-1)). Thus some w_a has ||P_V w_a||>=c*sqrt(n).
Operator-norm approximation of R and approximate diagonalization suffice;
no eigenvalue-gap promise is allowed. A constant-radius net of V includes
a real unit v with <v,w_a>>=a*sqrt(n), after choosing its sign.

Let L0=2/a and g_i=clip(sqrt(n)*v_i,[-L0,L0]). The removed correlation is
at most n/L0 because sum_i (sqrt(n)*v_i)²=n and |w_a(i)|<=1. Hence
n^-1 sum_i g_i*w_a(i)>=a/2. Round independently: output label1 with
probability h_i=(1+g_i/L0)/2, otherwise a uniform label2..k. For the
permutation sending1 to a, expected agreement is

 (1-n_a/n)/(k-1) + k/(k-1) * n^-1 sum_i h_i*w_a(i).

IID balance and the positive correlation give 1/k+Omega_pk(1).
Hoeffding makes the actual agreement hold with high probability. Do this
for every constant-net vector, creating a finite candidate list. The true
a and a good net index are never queried. Net size/constants depend only
on fixed p,k and the mass margin; output is not yet one labeling.

## Parent native validation and source obligation

For each edge, route the original Y to one of three outputs with weights
(1-2t,t,t), t=1/ceil(log2 n); fill the other two with independent Bern(q)
null bits. The marginals have signal strengths epsilon*(1-2t),epsilon*t,
epsilon*t. Need an exact per-edge chi-square proof giving <=C_q delta^4*t²
against their independent product, delta=epsilon*f_x(E), |delta|<=q/2.
Then total conditional-and-mixed-label TV is
O(sqrt(exp(C*M*beta^4*t²)-1))=o(1) at the effective frontier. Freeze these
three datasets once; transfer TV through the WHOLE algorithm once, not
per quantum call. Fixed coins and original-input attenuation are charged.

Candidates depend only on matrix/guide arrays and internal randomness.
Validate z on the third array with S_z=sum_E f_z(E)*(Y_validation(E)-q).
For C_ab=n^-1 sum_i(1[z_i=a]-1/k)(1[x_i=b]-1/k), the target exact expansion is

 E S_z=epsilon_v*n^p/p!*sum_ab C_ab^p+O_pk(epsilon_v*n^(p-1)),
 Var(S_z)<=O_pk(n^p).

The error is collision removal from ordered products; p is even. At this
frontier epsilon_v²*n^p grows polynomially in n, so a constant-size list
can be validated with failure o(1). A good candidate gives a positive
constant sum C_ab^p. Conversely a high score forces a constant positive
entry of C, because its rows/columns sum to zero. Averaging permutations
conditioned to include that entry gives assignment advantage at least
k/(k-1)*max_positive C_ab. Exactly sum_a C_(a,pi(a))=agreement_pi-1/k.
Thus choose the largest observed score and output ONE labeling, with no
latent-label check or independent-graph advice. All claims in this section
are under independent derivation; no theorem is promoted yet.

## Decisive falsifiers and next experiment

First test the operator comparison on the exact native mean and every
high-energy state; one counterexample with vanishing planted one-body mass
kills the operation. Then attack clone independence and candidate validation
on the same observed graph, including imbalance, huge-signal attenuation,
constant factors, fixed precision and all-branch clocks. Classical recovery
must close before quantum composition. No new code/sweep is needed for
already proved collision/noise identities. Pending independent proofs:
community-recovery-mass.md and community-recovery-validation.md. Paid calls
will target only a surviving concrete obligation, not a broad open conjecture.

## Stronger native validation: third clone is unnecessary

Subsequent parent/independent derivation supersedes the proposed three-way
validation architecture. Since |f_z(E)|<=1, Hoeffding conditional on x gives
for each fixed z

 Pr(|S_z-E[S_z|x]|>=a*epsilon*n^p |x)
       <=2 exp(-c_p*a²*epsilon²*n^p).

Union over ALL k^n labelings costs only n log k in the exponent. At the
frontier epsilon²D>=C*ell, D<=ell^d*n^d,

 epsilon²*n^p/n >= C*(n/ell)^(d-1) -> infinity.

Thus the score/mean comparison holds uniformly for every labeling on ONE
original Y, with failure o(1). It is valid for any data-dependent candidate
list; the algorithm does NOT enumerate all k^n labelings. Enumerating the
constant geometric net remains the only list cost. No independent validation
graph, third clone, or statistical independence between training and score
is needed. Classical recovery can use original Y directly without splitting
or attenuation; its spectral threshold only needs a lower bound on epsilon.

For the quantum composition, reuse the already paid TWO-way guide/matrix
source (including its own stronger-signal attenuation). Transfer ONLY the
candidate-generation success event, involving labels and cloned arrays,
through that marginal TV bound. Separately the uniform-score event holds on
actual original Y. A union bound joins these two actual-world success events.
Do NOT assert a joint TV comparison between original Y and ideal independent
clones, and do not multiply TV by the number of validation/quantum calls.
Validation uses the original known epsilon and original Y.

The new paid packets were already dispatched before this simplification.
Their three-way-channel algebra is advisory/optional, never a new required
subsystem. Current sessions Claude17167 and OpenAI7540; no retries.

## Mass and validation gates independently checked

Parent fully read the 215-LF mass proof (then its localized >= repair) and
193-LF validation proof. The explicit all-label mass result is: with
c=1/(2k^p), a=c*epsilon*D, r=k*d²*Lambda/n, T=2^300 ceil(sqrt(D ell)),
assume d!*D/Lambda>=1/2, r/d!<=cD/8 and T<=a/8. Every collision-free
ordered density of observed energy>=d!*a/2 has one-body mass
>=mu=1/(16k^(p+1)). For set densities use its W embedding and set energy
>=a/2. The probability event is uniform over graph-dependent complex/mixed
states; no new eigenvalue gap or label input is assumed.

The exact classical algorithm uses Z=Q*A and j=4(bitlength(N)+4), independent
Rademacher starts, and the rational test 2*y^T Z y>=Q*a*y^T y. The same
event gives lambda_max>=7a/8 and lambda_min>=-a/4, so each start passes
with probability>=1/12. Capped logarithmic retries give failure<=eta and
time n^(ell+O_p(1))*poly(B,log(1/eta)). The rational one-particle matrix
uses sum_T y_(T+i)y_(T+j)/(ell*y^T y), costing n^(ell+1) polynomial BIT.
The witness lower bound is >=Lambda/k^p, NOT an exact equality; this repairs
a conservative-equality typo also present in the older preserved proof.
No older frozen artifact is edited; all downstream estimates need only >=.

Actual uniform validation uses C=H P H, H=I-11^T/k, not empirical covariance
P-rho*tau^T. If some candidate has permutation advantage rho>0, set
e0=rho^p/k^(p-1), require n>=8k²*binom(p,2)/e0. The score winner then has
advantage>=rho/[(2k)^(1/p)(k-1)²], except with probability
2 exp(n logk-e0² epsilon² n^p/(32 p!)). The native frontier makes this o(1).
Exact scores have common denominator k^p*denom(q). This works uniformly
for all data-dependent/quantum-generated lists on originalY.

A cleaner rounding operation, independently agreed with the reviewer,
supersedes h=(1+g/L0)/2: set h=1/k+g/(k*L0). This lies in[0,2/k] and
makes expected agreement EXACTLY1/k+average(g*w_a)/[(k-1)*L0] for every
empirical community size. Thus only the coarse balance event needed for
the planted frame remains; no extra tiny balance tolerance is necessary.
Its finite rational spectral/net implementation is under final review.

Claude17167 completed, full report parent-read/reaped, estimateUSD0.576940.
Its set-mass/power/factorial audit checks. Its ordered-noise warning is valid
for the narrow packet, which omitted the earlier proof's section8. Parent
checked that retained section8 again: at most(d!)^(2t) ordered lifts per
trace word, initial(n)_ell<=n^ell, same all-label symmetrization; this pays
the FULL ordered norm d!*T, including non-symmetric sectors. No symmetry
promise or new trace theorem is needed. This resolves its O1 using prior
work; it does not infer an ordered bound merely from set compression.
Its three-way attenuation warning is superseded by original-Y validation.
No new quantum/whole-recovery theorem is asserted from report acceptance.
OpenAI7540 decoder task remains pending.

## Classical comparator source audit and exact coarsening falsifier

Full independent community-recovery-classical-scope.md parent read, including
actual Mao formal Theorem5.8, HCE Theorem4/Cor5 and IID occurrence law, plus
sharp Section13's revealed-literal interface. None of those inspected
statements supplies the same native multi-color Bernoulli recovery theorem
or a fully paid reduction. This is not a literature-wide novelty/hardness
claim and does not rule out a stronger native color-network HCE analysis.

The naive merge-color reduction is explicitly false: at p4,k3, map color1
to+ and colors2/3 to-. Conditional on six minus vertices, write residual
colors t_i=+/-1. Then f_x(E)=[1+sum_pairs t_i*t_j+9*product_E t_i]/72.
For E=1234,F=1256, the only common nonconstant Fourier monomial is t1*t2,
so Cov(Y_E,Y_F|merged colors)=epsilon²/5184>0. Parent independently checked
this expansion and conditional covariance. Boolean independent-noise
theorems cannot be imported by coarsening alone. This does not refute all
reductions or algorithms. No new benchmark or implementation follows.

## Complete CLASSICAL weak recovery: CLOSED WRITTEN

For each fixed even p=2d>=4 and fixed k>=3, q=1/4, growing polylogarithmic
ell=o(sqrt n), and rational0<epsilon<q with epsilon²D>=C_(p,k)*ell, there
is a native classical algorithm outputting ONE z in[k]^n with
max_permutation agreement(z,x)>=1/k+c_(p,k)>1/k with probability1-o(1).
Its all-branch BIT cost is n^(ell+O_p(1))*poly(parameterbits), including the
original binom(n,p) input bits, exact sparse powers, rational one-particle
contraction, diagonalization, finite net, rounding, scoring and n-label output.
Retain the explicit sufficient-n conditions of the checked trace/mass proof;
for example C_(p,k)=2^610*k^(2p) suffices for its noise margin. Constants
are deliberately loose and are not practical-resource estimates.

Parent fully checked the final197-LF rounding proof in
audits/reviews/2026-11-13-community-recovery-rounding.md. It uses exact
rational orthogonal Jacobi rotations, maximum off-diagonal pivots,
T=n² ceil(log2(64/alpha²)) and dyadic half-angle approximations with
operator error alpha²/(128n²). Common denominators grow linearly with T;
the off-diagonal Frobenius potential contracts to the declared threshold.
PSD/trace/orthogonality remain exact. Thus no eigenvalue gap, real-arithmetic
primitive or hidden conditioning is assumed. Exact diagonal thresholding
returns dimension<=4(k-1)/mu, a constant. A rational net, integer floor
sqrt(n), clipping and h=1/k+g/(kL0) give a constant list containing a
candidate of advantage Delta=mu²/[1024*k²*(k-1)], with conditional failure
<=exp(-2n Delta²). All categorical coins have a fixed finite bit budget.

Use the exact rho from the checked integer-vector proof, with
mu=1/(16k^(p+1)), then this rounding lemma, then maximize the ORIGINAL-Y
score. Set e0=Delta^p/k^(p-1). One explicit final advantage is

 c_(p,k)=Delta/[(2k)^(1/p)*(k-1)²].

The total failure is bounded by

 2n^(-2ell)+eta+2k exp(-n/(12k))+exp(-2n Delta²)
       +2 exp(n logk-e0² epsilon² n^p/(32p!)),

for n>=8k² binom(p,2)/e0 and the existing mass/noise scalar conditions.
Choose eta=n^-4 using a fixed number of starts. Each term tends to zero.
No actual label, planted gauge, independent graph, clone, spectral projector
or amplitude oracle enters this classical algorithm. Score ties are handled
deterministically. A failed capped start returns a fixed labeling and is
counted in eta; invalid inputs cannot create an unbounded branch.

This is a complete reviewed WRITTEN composition, not an implemented program,
practical resource claim, human/formal verification or novelty theorem. It
is a stronger-output native classical baseline. There is no general
classical lower bound or speedup conclusion. Exact recovery of every label
was not requested or proved. Quantum recovery remains a separate gate.

## Final paid decoder disposition

OpenAI7540 completed; ALL722 physical LF parent-read, reaped, estimate
USD1.693960. Its separate three-array algorithm is a valid conditional
classical alternative, with exact chi-square formula, finite-abort rational
coins, explicit fine-balance rounding and rational Jacobi ledger. The
parent checked the formula/constants and scope. Its stated necessity of
splitting/data-flow separation is ONLY for that conditional-independent
validation proof, not a barrier to our uniform original-Y argument.
Our centered k-color coin removes its finer balance event; original-Y
validation removes its attenuation, third array and associated TV loss.
Those unnecessary operations are NOT implemented. Its matrix-production
premise is now supplied by the separately checked mass/vector proof.
Both paid reports terminal/full-read/reaped. Round estimate2.270900,
not billing; cumulative expected310.653078/238priced, Anth172.532998/
OpenAI138.120080,7UNKNOWN excluded, owneractual155.99/101.71 separate.
Next hard gate: retain the existing quantum accepted branch and pay
polynomial one-body tomography without changing its native source law.

## Quantum readout lemma checked; retention is the final source gate

Parent fully read/checked177LF community-recovery-tomography.md. For a
fixed accepted density sigma, use independent fresh copies conditional on
frozen input arrays. In every batch deterministically cycle through the
ell slots equally; Hoeffding permits independent nonidentical outcomes.
One shared diagonal batch enforces trace(Rhat)=1 exactly; each pair batch
uses the real two-level Hadamard basis and counts (c_plus-c_minus)/(2m).
With m=ell*ceil(n^4*b/ell), b=ceil(log2(2n²/eta_tom)), the total is at most
2n^6*b accepted copies. Simultaneous entry error<=1/n² has probability
>=1-eta_tom. Then Rtilde=(Rhat+I/n)/2 is rational PSD trace-one and
Rtilde>=Re(rho)/2, retaining half the planted mass. Exact rational PSD
testing protects bad branches; it does not project an unknown matrix.

Pair measurements compile EXACTLY with affine reversible maps and controlled
Hadamard (Clifford+T via VZV*=H), O(log²n) gates per copy. Rational counts
have O(logn+loglog(1/eta_tom)) bits. The closed rounding lemma uses mass
mu_ret/2, giving candidate Delta'=mu_ret²/[4096*k²*(k-1)], then uniform
ORIGINAL-Y validation selects one output. No eigenbasis, preparation oracle,
independent graph or identical-marginals-only assumption is granted.

The final retention audit must match a CONSTANT guide-energy threshold and
produce this SAME actual sigma on every successful fresh attempt. It may
need a smaller fixed c_ret than the classical c; use mu_ret=c_ret/(8k),
not automatically the classical mu. Low-energy leakage, validity of tuples,
source error once, fixed abort caps and exact inverse of the actual compiled
unitary remain explicit before admitting the whole quantum algorithm.

## Complete QUANTUM weak recovery: CLOSED WRITTEN

Parent fully read/checked201LF community-recovery-quantum-retention.md and
its actual source constants in the retained certificate section8, including
Dbar-versus-set-D conventions. Together with the already checked177LF
tomography,197LF rounding,193LF validation and corrected mass proof, this
closes a native end-to-end WRITTEN quantum recovery construction.

Scope: fixed even p=2d>=4, fixed k>=3, q=1/4, ell=p*lambda a growing fixed
polylogarithmic function of n, and known rational0<epsilon<q with
epsilon²D>=C^Q_(p,k)*ell for a computable sufficiently large constant.
The input is ONE explicit Bernoulli p-edge array with IID-uniform latent
labels and the stated centered-color means. Output ONE labeling with
permutation agreement>=1/k+c^Q_(p,k)>1/k with probability1-o(1).

The all-branch gate/BIT upper bound is

 n^(ell/4)*exp(O_pk(ell*(logell+loglogn)))*poly(n^p,B).

For ell=Theta(logn) the subleading factor is exp(O_pk(ell logell)). B charges
the public rational parameter bits; original input reads, reversible scans,
state-preparation inverses, all measurement copies, n-by-n rational
postprocessing and n-label output are included. The classical comparator
is the CLOSED native n^(ell+O_p(1))*poly(B) weak-recovery algorithm above.
Sufficient constants are not optimized or matched; this is no unrestricted
classical lower bound, best-algorithm comparison or quantum advantage claim.

### Exact composition and source/error ledger

1. If needed, attenuate the original known signal by a dyadic2^-j to
epsilon_*, choosing largest j with epsilon_*²D>=C_*ell, so the effective
value lies within a factor4 of that frontier. Choose C_* so matrix strength
(1-1/L)epsilon_* pays every retained constant, L=ceil(log2n). Eventually
epsilon_*<=q/2. Form the already proved TWO-way asymmetric guide/matrix
arrays ONCE. The quantum candidate generator sees only these frozen arrays
and public parameters, not original Y, route masks or latent labels.
Retain original Y only for later uniform scoring. Source rounding is capped
and adds a declared inverse-polynomial TV error.

2. Use the actual constants
 c_full=k^(1-(2p+2)d)/(2^d*d!),
 c_small=binom(p,d)k^(1-2p-2d)/(p^d(2d)^(d-1)),
 c0=min(1,c_full,c_small), theta_G=c0/8, kappa=c0/32,
 c_ret=min(1/(2k^p),theta_G/2), mu_ret=c_ret/(8k).
The guide has public good-instance high-band overlap floor
 gamma=(kappa/(8L))*(c_f*h²/2)^lambda, c_f=k^(1-2p)/2,
 h=epsilon_*/(L*sqrt(q(1-q))). A dyadic lower floor has O(elllogn) bits.
The retained full ordered trace controls nonsymmetric sectors. Let
 tau_hi=d!*c_ret*epsilon_M*D, tau_lo=3tau_hi/4.
The source high band is above tau_hi, and enlarged fixed SNR/noise constants
give low-spectrum lower bound -tau_hi/4. Mass below tau_lo<=1/4 therefore
ensures observed energy>=tau_hi/2 and one-particle planted mass>=mu_ret.
No symmetric-state or eigenvector promise is added.

3. Compile ONE actual unitary W for guide preparation, separated-window
QPE/majority filtering and an EXACT final validity AND (indices<n and
all distinct). Keep all filter workspace during amplification. With
nu=gamma/4, B_trials=ceil(8ln(4/eta_call)),
mu_err=min(zeta,eta_call²/B_trials), filter false-pass
delta=nu*mu_err/4096 and column error<=sqrt(nu*mu_err)/64, actual success
mass is>=nu and conditional low-band mass<=mu_err/1024. Actual accepted
support is exactly legal. Use W's actual gate-by-gate inverse and exact
flag/zero reflections. Mixing zero Grover iterations with a uniform
power-of-two schedule of length between4/sqrt(nu) and8/sqrt(nu) succeeds
>=1/8 per trial, whatever actual overlap>=nu. The capped first-success
output is the SAME normalized accepted component on every successful
iterate, up to global phase. No guessed inverse, ideal dilation, free
postselection, or unknown-overlap estimation is needed.

4. Fresh initialized registers and coins give product copies of the SAME
actual accepted density sigma conditional on the frozen arrays, even
conditional on all preparation calls succeeding. Use the SAME W for
M_tom=O(n^6logn) requests, eta_call=n^-4/M_tom, zeta<=1/4. Computational
ABORT probability sums to O(n^-4); accuracy logs remain O(B+elllogn).
The statistical/source good-instance failure is paid ONCE, not per copy.
Apply the checked tomography lemma with eta_tom=n^-4, its exact pair-H
circuits and validity guarantees. It returns rational Rtilde with planted
mass>=mu_ret/2. The rounding lemma yields candidate advantage
 Delta_Q=mu_ret²/[4096*k²*(k-1)].

5. Score the finite candidate list on ORIGINAL Y and output its maximizer.
The existing uniform-over-all-k^n-labelings event applies regardless of
its dependence on original Y. An explicit final advantage is
 c^Q_(p,k)=Delta_Q/[(2k)^(1/p)*(k-1)²].
Transfer ONLY candidate-generation success through the existing joint-label
clone-marginal TV bound; separately intersect the uniform validation event
on actual original Y. Never compare a fictitious joint law containing
original Y and independent clones. No third clone is needed.

Apart from computational/tomography and rounding errors, the source failure
is bounded by the retained ordered-noise event, O_pk(ell^(d+1)L²/n^d),
1/L, and O(sqrt(exp(O_pk(ell^(2-p)/L²))-1)) plus finite-bit source TV.
Frame balance fails with at most2k exp(-n/(12k)). Original-Y validation
has the earlier bound with Delta_Q and ORIGINAL epsilon. All terms are
o(1); source failure cannot be reduced by repeating on a bad frozen graph.
The per-call clock is finite on bad graphs too. At the frontier
gamma^-1/2=O_pk(sqrtL)*h^-lambda*exp(O_pkell), giving the displayed gate
clock after all polynomial measurement/postprocessing factors.

No arbitrary-input, odd-p, sparse-q, growing-k, exact-all-label recovery,
novelty, hardness, practical implementation, human/formal verification or
Shor-level/speedup conclusion is admitted. This pass supplies explicit
reviewed asymptotic recovery upper bounds and a native classical match
in signal scale, with different unoptimized running-time upper bounds.

All recovery proofs/source audits/topic are now STABLE for a milestone
freeze. Both paid reports were fully read/reaped; no new implementation,
benchmark or broad test suite is justified by this analytic closure. Next
selection must compare independent high-upside mechanisms, not automatically
add exact-recovery cleanup or another nearby community variant.
