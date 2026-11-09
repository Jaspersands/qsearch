# Learning mixtures of two mixed fermionic Gaussian states

2026-11-07. REVIEWED WRITTEN POLYNOMIAL-COPY/BIT LEARNER.
Exact/core, actual-source and full numerical/resource reviews are complete,
including the final direct four-Gaussian output. No human peer review or
formal verification. Full learner and quantum execution were not performed.
No novelty, classical-input separation, practical cost or quantum execution.

## Native question and independent selection

Input: fresh exact IID copies of an n-mode density matrix
rho=p rho_G(Gamma1)+(1-p)rho_G(Gamma2), 0<=p<=1. Each Gamma_j is an unknown
real antisymmetric2n matrix with operator norm<=1. These are EVEN fermionic
states (odd moments vanish), NOT necessarily states supported only in the
even-parity sector. Physical Majoranas/Jordan-Wigner encoding and ordinary
qubit circuits are known; no components, weights, inverse, gap, separation,
minimum rank, pure-mode information or preparation oracle is given.
Output: a description of a mixture of at most FOUR known Gaussian states
and a finite preparation circuit (ancillas, classical control and discard
allowed) within trace distance epsilon, with probability>=1-eta over learning,
in polynomial(n,1/epsilon,log1/eta) copies and BIT/gate cost. This is quantum
state learning, not a classical-input computational separation.

Question: do degree2/4/6 moments determine the state stably enough for this
ENTIRE class, with a paid preparation endpoint in every degenerate case?
The proposed mechanism is exterior-square inversion at effective rank>=6,
and a small-core Gaussian channel at effective rank<=4. A common attenuation
regularizes conditioning without imposing an input gap. The classical
parameter-processing is polynomial; covariance estimation needs copies.
This models, for example, an unobserved classical switch between two thermal
quadratic-fermion preparations. It does not assert that a generic interacting
thermal state or experimental noise process has only two components. Expected
benefit is polynomial reconstruction within this physically succinct family,
in place of unrestricted exponential-dimensional tomography, not a proved
classical-versus-quantum computational separation.

Selection started with current STATE/TRAPS and corpus been-tried, then
primary literature and baselines. General wild Selmer is parked. Independently
screened Wedderburn decomposition: A tensor A^op already has the classical
regular-module map; known promised-split Amitsur splitting does not extract a
minimal module for arbitrary nonsplit A. Nebe-Steel2009 actual source gives
Schur-index/maximal-order recognition, not the new explicit global module.
The alternative pure stabilizer-rank2 learner is ALREADY covered by actual
2610.03658 Theorem1.1 and2610.06819 Cor1.6/Thm8.2, no branch advice needed.
Those three primary snapshots are in audits/sources/stabilizer_rank_priority;
Nebe-Steel in audits/sources/division_algebra_selection. No new operation
was admitted from these screens or the old sparse-constant-field gap.

This mixed-state task is distinct from the prior coherent sum of two PURE
Gaussians. Strongest matched classical baselines: supplied-component Wick/
Pfaffian evaluation and ordinary two-component moment methods; unrestricted
MPS bond dimension is not assumed small. Corpus returned tensor-network
simulation. Existing one-Gaussian tomography and few-nonGaussian-gate
compression retain their exact promises. No advantage over classical access
to the same measured moments is claimed. Main falsifiers: distinct mixtures
with identical degree<=6 data; unstable inverse away from a small-core
fallback; nonphysical reconstructed core/channel; hidden parity/CJ corrections;
rare uncharged postselection; use of a pure-state fidelity test on mixed input.

## Exact exterior algebra

For real skew Gamma define omega=sum_{i<j}Gamma_ij e_i wedge e_j. Write
M_{2k}=sum_{|I|=2k} moment_I e_I, using Hermitian Majorana monomials
(-i)^k c_{i1}...c_{i2k} with covariance Gamma_ij=-i Tr(c_i c_j rho).
For the explicit CJ convention use c_(2j-1)=Zprefix X and c_(2j)=-Zprefix Y,
as in Bravyi. A different known Majorana convention is converted by its known
signed orthogonal coordinate map; no hidden physical frame is assumed.
For Gaussian states the generating form is exp(omega), i.e. moments=Pfaffians.
Let q=1-p, Delta=omega1-omega2, omega=p omega1+q omega2 and E=sqrt(pq)Delta.
Then
  M=p exp(omega1)+q exp(omega2)
   =exp(omega)[p exp(qDelta)+q exp(-pDelta)],
  H=2M4-omega²=E²,
  J=6M6-6omega M4+2omega³=pq(q-p)Delta³.
Thus for 0<p<1, J=t E³ where t=(q-p)/sqrt(pq).
Products are exterior products of even forms; they commute. H=0 implies
rank(E)<=2, and then the ENTIRE state is Gaussian with covariance Gamma.
At rank(E)<=4 the entire generating form is exp(omega)(1+H/2); no unknown
higher moments remain. These are exact identities, not finite observations.

In an analysis-only orthonormal Darboux frame E=sum_j a_j u_j wedge v_j,
1>=a1>=a2>=...>=0 (||Delta||op<=2, sqrt(pq)<=1/2). Put S=sum a_j².
The contraction Gram G_ab=<i_ea H,i_eb H> has eigenvalues
  lambda_j=4a_j²(S-a_j²), each twice,
  ||H||²=4 sum_{j<k}a_j² a_k².
Their order agrees with the a_j order since
lambda_i-lambda_j=4(a_i²-a_j²)(S-a_i²-a_j²)>=0 for i<j.
This gives a measured support/gap test without any supplied frame.

## High-rank reconstruction, including exact signs

If a3>=s>0, choose six independent Rademacher columns W. Set A=W^T E W.
For i<j in1..6 define B_ij=(-1)^(i+j+1) H(W_hat{i,j})/2 and skew-complete.
Then B=-Pf(A) A^-1 when A is invertible, det B=Pf(A)^4, and
  A0=-(det B)^(1/4) B^-1
is either A or -A. The global sign will only interchange mixture labels.

For P=Pf(W^T E W), Cauchy-Binet and independent entries give
E[P²]=6! sum_{|I|=6}Pf(E_I)²>=6!s^6. P is multilinear degree6, so
Rademacher hypercontractivity gives E[P^4]<=3^12 E[P²]^2. This can also
be proved elementarily here: for a degree-d decoupled column polynomial
P=sum_j epsilon_j a_j, conditional fourth moments are <=3(sum a_j²)²;
Minkowski and induction give E[P^4]<=3^d E[P²]^2. The looser displayed
3^12 at d=6 is therefore sufficient without a new source assumption.
Paley-Zygmund
therefore gives probability>=1/(4*3^12) that |P|>=sqrt(E[P²]/2)>=s³.
Every column has norm sqrt(2n); all restriction coefficients are polynomially
bounded. A capped O(log1/eta) number of trials with this CONSTANT factor
finds a polynomially conditioned restriction with high probability.
No state copies, postselection or E access is used to choose W: all tests
use the already estimated H. Singular trials are discarded classically.

For each physical basis vector v, recover alpha_i=E(W_i,v) from
  H(W_i,W_j,W_k,v)/2=A_ij alpha_k-A_ik alpha_j+A_jk alpha_i.
The map alpha->A wedge alpha from Lambda1 to Lambda3 in six dimensions is
injective; its smallest singular value is at least sigma_min(A). This follows
by putting A into orthogonal skew normal form: each alpha component has
squared output norm equal to the sum of the other two pair singularvalues².
Choose any reliably nonzero A_ij. Then
  E(v,w)=[H(W_i,W_j,v,w)/2+E(W_i,v)E(W_j,w)-E(W_i,w)E(W_j,v)]/A_ij.
Thus reconstruct E up to ONE global sign in polynomial arithmetic.
Recover t=<J,E³>/||E³||² and p=(1-t/sqrt(t²+4))/2; then
  Gamma1=Gamma+sqrt(q/p)E, Gamma2=Gamma-sqrt(p/q)E.
High-rank lower bounds pay p,q and all denominators. Clip small estimation
violations of skew covariance singularvalues to[0,1]; Gaussian continuity
bounds the resulting output error. No actual unknown branch is prepared.

## A paid low-rank endpoint

Suppose Delta is supported on a known real Majorana subspace V of dimension
at most4 (pad to4 if necessary). In a known orthogonal frame write
  Gamma_j=[A_j,C;-C^T,B], with the SAME C,B for both j.
First assume I+iGamma_j>=tau I, I-iGamma_j>=tau I. Put
  D=(I+B²)^-1,
  R=I-C D C^T,
  A0=-C B D C^T.
Schur complementation gives R+i(A_j-A0)>=tau I and its conjugate, hence
R>=tau I; also I+B²>=tau I. Thus all inverses have polynomial conditioning.
Let G_j=R^-1/2(A_j-A0)R^-1/2. These are physical covariances on at most
TWO modes. Set L=[sqrt(R);0] and Z=[A0,C;-C^T,B]. The Gaussian channel
  Gamma_core -> L Gamma_core L^T+Z
is CP/TP: I-LL^T+iZ is positive semidefinite with zero Schur complement.
Its conjugate handles the other sign convention. It maps each G_j to Gamma_j,
and therefore maps their unknown mixture to rho by linearity.

The core is constant-dimensional. Its mean covariance is
R^-1/2(A_mean-A0)R^-1/2, and its connected H is
(R^-1/2)^(wedge4) H|V. Its raw quartic moment is (omega_core²+H_core)/2.
Identity plus all degree2/4 moments specify its even two-mode density matrix;
no physical branch decomposition optimization is required. Clip small negative
eigenvalues of the estimated4x4 matrix, preserve parity blocks, and normalize.

The final endpoint is simpler and deterministic. Any parity-commuting TWO-mode
density matrix has two2x2 parity blocks. Diagonalizing them expresses the core
as a convex mixture of at most FOUR parity-definite pure states. Every such
pure state is Gaussian: u|00>+v|11> is a BCS vacuum, and u|01>+v|10> is a
one-particle Slater determinant. The parity convention explicitly includes
both sectors. Let w_a,G_a be these weights and Gaussian covariances. Return
  sum_{a=1}^4 w_a rho_G(L G_a L^T+Z).
The mathematical Gaussian channel proves equality by linearity and contracts
core trace error. Its physical implementation is unnecessary: compute the
four output covariances and directly prepare their known Gaussian mixture.
There is no Choi state, Bell postselection, retry clock or success-probability
normalization in the FINAL algorithm. Degenerate core eigenvectors require
only an accurate spectral decomposition of the4x4 density matrix, not a
particular eigenbasis; the represented mixture has small trace error. This
also handles n<=2 after direct constant-size parity-block tomography.

## Uniform regularization and proposed quantitative branching

Use raw density trace norm for conservative error estimates below (trace
distance is half). Actual2409.17953 Theorem1 Eq9 proves for Gaussian states
  ||rho_G(Gamma)-rho_G(Gamma')||1 <= (1/2)||Gamma-Gamma'||_Schatten1,
with NO gap assumption. Apply it separately to branches, never to a general
nonGaussian mixture. Attenuating BOTH branch covariances by1-tau costs at
most n tau in density trace norm, and gives the strict margins used above.
The attenuated degree2k moments are obtained by rescaling by(1-tau)^k,
so no input preparation oracle is needed. This is a known Gaussian channel.

Reviewed hierarchy for n>=3,0<epsilon<=1/10:
  kappa=epsilon/[10^6(n+1)], tau=kappa,
  h=kappa^8, ell=kappa^40, moment precision zeta=kappa^10000.
All exponents are absolute constants; no practical sample claim. Estimate
all O(n^6) moments with simultaneous failure<=eta/4 using independent Pauli
measurements. The remaining random-restriction failure gets eta/4. BIT cost
of precision is O(log(n/epsilon)), with the displayed constant factor.

SMALL H: if ||H||<=O(h), output the Gaussian mean. Proof split is analysis-only:
if min(p,q)<=sqrt(h), distance to the mean Gaussian is O(n sqrt(h)) by
convexity and the Gaussian continuity bound. Otherwise sqrt(pq)>=Omega(h^1/4).
Since a2<=O(sqrt(h)), deleting all but the largest skew pair of Delta changes
each covariance by O(sqrt(h)/sqrt(pq))=O(h^1/4)<<tau. The modified branches
are physical and their mixture is EXACTLY the mean Gaussian (rank2 difference).
Weighted Gaussian continuity costs O(n sqrt(h)). No weight recovery is needed.

LOW THIRD EIGENVALUE: if ||H||>=Omega(h) but fifth Gram eigenvalue<=O(ell),
then pq>=Omega(h/n), a1²>=Omega(h/n), a3²<=O(n ell/h). Truncation to the
top FOUR Majorana directions changes Delta in operator norm by
O(n sqrt(ell)/h)<<tau, so both modified covariances remain physical with
unchanged mean and physical margin at least tau/2. Invoke the channel
lemma with tau/2 here. Their weighted density trace error is O(n^(3/2)sqrt(ell/h)).
The top4 support gap is Omega(h²/n²), since
lambda_2>=4a1²a2²>=2||H||²/n² while lambda_3 is tiny.
Davis-Kahan controls the estimated support. Projection commutes with exterior
products: H|V=pq(P Delta P)² EXACTLY, so the measured projected data supply
the nearby core directly. No truncation-error amplification through the core
inverse occurs; only moment-estimation errors are amplified by tau^-O(1).
Use the small-core channel to prepare this state.

HIGH THIRD EIGENVALUE: if the fifth eigenvalue>=Omega(ell), then
a3>=Omega(sqrt(ell/n)). The high-rank reconstruction above applies. Threshold
bands overlap; choose tolerances so either branch remains valid near a boundary.
A trial with det B>=kappa^300 suffices; good random trials have determinant
well above this threshold. All matrices in the six-dimensional inverse have
polynomial norm and inverse norm. The quantitative ledger below justifies exponent10000 and physical clipping.
For n<=2 use direct constant-size parity-block tomography. Larger requested
epsilon can be replaced by min(epsilon,1/10), and n=0 is trivial.

## Finite clocks and physical output

Use measured thresholds ||Hhat||<=2h; otherwise fifth Gram eigenvalue<=2ell
selects the low branch; otherwise the high branch. On simultaneous moment
accuracy, the corresponding true bounds are ||H||<=3h, or ||H||>=h and
lambda5<=3ell, or lambda5>=ell. All nearby cases satisfy a valid branch.
Cap random six-restrictions at ceil(4*3^12 log(8/eta)); accept only when the
estimated detB>=kappa^300. If none accepts, return ABORT. Moment-error events
and numerical inconsistencies may also return ABORT; no while-loop has an
unbounded search clock. Compute all arrays/skew symmetrizations and spectral
operations to polynomial BIT precision finer than zeta. The reviewed
ledger below justifies these guard thresholds on good data.

Conservative high-branch guards: require the six-dimensional Lefschetz map's
smallest singular value and selected |A_ij| to exceed kappa^300; require
||Ehat³||>=kappa^300; otherwise ABORT. Clip computed p to
[kappa^100,1-kappa^100] before branch rescaling. On good data the true p lies
strictly within this interval. Clip each returned skew covariance to the
physical operator-norm ball. These guards bound every inverse and source-free
arithmetic clock, including failed/noisy runs. They are output thresholds,
not input promises or extra advice.

In the low branch, project the estimated mean skew covariance onto the ball
of radius1-tau/2 before constructing its Schur channel. The true attenuated
mean is in this ball, so Frobenius error does not increase. The channel then
has a strict Schur margin; numerical work can be charged without unknown
eigengaps. Project the constant-size core onto its parity-block PSD cone and
normalize. Its trace is close to1 on good data (and positive-part clipping
cannot reduce a trace-one estimate below1).

Compute a backward-accurate spectral decomposition of each2x2 parity block.
Each of the at most4 normalized parity-sector eigenvectors specifies a pure
Gaussian covariance; compute and clip its output covariance L G_a L^T+Z to
the physical ball. Approximation in the core spectral decomposition is
controlled in density trace norm BEFORE the mathematical channel, so no
individual eigenvector gap or branch-weight lower bound is needed. Normalized
sector vectors remain exactly pure Gaussian states, even if degenerate
vectors are chosen arbitrarily. The channel's CP property supplies contraction
for this comparison, not an unimplemented oracle or required physical backend.

Sample the at most4 explicitly known probabilities to the allocated accuracy
and prepare the corresponding Gaussian state. Gaussian covariance
diagonalization is required only to backward error in operator/Frobenius norm;
degeneracies do not require identifying particular eigenvectors. Decompose
into O(n²) elementary Gaussian rotations and thermal single-mode states;
allocate per-operation error so the total raw trace error is <=epsilon/10^4.
Compiling these known rotations into ordinary qubit gates costs at most a
further polynomial(n,log1/epsilon). The global orthogonal frame is known
from classical linear algebra; determinant-minus-one/odd Majorana corrections
and odd Fock states are allowed by the ordinary-qubit gate model. Clipping
returned covariances and approximating mixture probabilities add only the
Gaussian continuity and total-variation errors. All output branches have
explicit finite clocks; no postselection is used in this final endpoint.

There are Nmom=sum_{j=1}^3 binom(2n,2j)=O(n^6) measured observables. Taking
ceil(2 zeta^-2 log(8Nmom/eta)) fresh copies per mean makes simultaneous error
<=zeta with failure<=eta/4. Each Hermitian Majorana product is a known Pauli
string, measured in O(n) ordinary single-qubit operations. Total copies are
O(n^6 kappa^-20000 log(n/eta)); all algebra, random restrictions, precision,
frame rotations and output size are polynomial as well. This is an extremely
conservative polynomial upper bound, not an optimized or practical algorithm.
Gaussian output-state error is established analytically; no mixed-state
candidate selection via a pure-state fidelity/inverse test is performed.

## Reviewed numerical and total-error ledger

Full derivations are retained in
`audits/reviews/2026-11-07-mixed-gaussian-composition.md`; parent read the
complete review and checked each conditioning inequality. Let k=kappa;
k<10^-7 and n<k^-1. Use arithmetic roundoff k^12000. Simultaneous moment
accuracy zeta=k^10000 implies all constructed covariance/H/J/Gram arrays and
ALL Rademacher restrictions have norm error<=delta0=k^9900. These are
fixed-degree polynomial expressions; dimension factors and Rademacher
column norms consume fewer than the reserved100 powers. Reuse of the same
estimated H across trials is classical and introduces no new source law.

In HIGH THIRD, a3>=k^21, pq>=k^42, ||E³||>=k^63. A good random restriction
has detB>=k^252 and passes the acceptance threshold. EVERY accepted
restriction has true detB>=k^301 and ||A||,||B||<=k^-10. The following are
conservative sufficient absolute bounds, not optimized estimates:

| Step | Bound |
|---|---|
| B inverse | sigma_min(B)>=k^351, ||B^-1||<=k^-351 |
| Determinant error | <=k^-60 delta0 |
| Fourth-root error | <=k^-287 delta0 |
| Inverse error | <=k^-703 delta0 |
| A0=−(detB)^(1/4) B^-1 | error<=k^-720 delta0=k^9180 |
| A conditioning | detA>=k^151, sigma_min(A)>=k^201>=k^210 |
| Chosen A entry | true magnitude>=k^211 |
| All cross-vector recovery | error per vector<=k^8950 |
| Entire E, one global sign | matrix/form error<=k^8600 |
| t,p | absolute errors<=k^8300 |
| Reconstructed branch covariances | operator error<=k^8000 |

For example sigma_min(B)>=detB/||B||^5, the root derivative uses determinant
>=k^301, and the inverse identity bounds perturbation by twice inverse-norm
squared. The fourth root is at mostk^-15. These give the720-power loss.
Then detA=sqrt(detB) and the same singular-value bound pay the Lefschetz
least squares. The entry formula divides only by the chosen A entry. For
t, exterior multiplication gives error<=k^8590 in E³; its true norm>=k^63
and |t|<=k^-21 control the quotient. The derivative of p(t) has magnitude
<=1/4; true p,q>=k^42 pay derivatives of the branch rescalings (<=k^-70).
The whole high-branch ledger loses fewer than2000 powers. Guards at k^300
therefore pass on good data. Covariance clipping is a Frobenius projection
onto the physical skew ball, so the final Gaussian mixture error, including
weight error, is conservatively <=k^7990.

In LOW THIRD, the gap>=h²/n²>=k^18 and Davis-Kahan give projector error
<=k^9881; internal degeneracies require no eigenvector recovery. Pivoted QR
on a rank4 coordinate minor and Householder completion cost polynomial
factors only. The ideal nearby reference uses THIS estimated projector and
exact mean. Its covariance truncation is <=k^10, physical margin>=k/2 and
raw density error<=k^14. This truncation error is outside all inverse steps.
The projected H describes the reference exactly.

Here ||D||<=2/k, ||R^-1/2||<=sqrt(2/k). Perturbation bounds give D error
<=k^-6 delta0, R error<=k^-8 delta0, A0 error<=k^-9 delta0, and square-root/
inverse-square-root errors<=k^-10 delta0 and k^-11 delta0. Core moments,
exterior powers and constant-size density reconstruction consume fewer
than30 further powers. Retain k^9800 as the core and output-channel parameter
error budget. R is positive and <=I, so ||L||,||Lhat||<=1. Uniformly for a
physical core Gaussian covariance G_a,
  ||Lhat G_a Lhat^T+Zhat-(L G_a L^T+Z)||op
  <= ||Zhat-Z||op+2||Lhat-L||op.
Thus the four-Gaussian output's parameter error is bounded by n times the
right side. Abstract CP contracts core density error; no eigenvector gap or
positive mixture-weight lower bound is needed. Clipping/probability errors
are paid separately. The small branch's raw error is <=4(n+1)k^4.

Allocate epsilon/20 raw error to known output Gaussian/weight/gate preparation
in every branch (the earlier epsilon/10^4 suballocations are smaller). Then
n*k plus the applicable approximation error plus preparation error is LESS
THAN epsilon in RAW trace norm, stronger than the requested trace distance.
Moment failure<=eta/4 and capped restriction failure<=eta/4 give total
learning failure<=eta/2, with slack; other work has deterministic finite
precision/clocks. On success the output is an explicit mixture of <=4
known Gaussians, not necessarily the original components. No uncharged
verification oracle or pure-state fidelity test is needed.

## Evidence and claim boundaries

Primary snapshots: audits/sources/mixed_gaussian_pair/source.json, including
2409.17953 trace bounds,1604.01954 channels,quant-ph/0404180 Gaussian maps.
Core independent reasoning accepts exact Schur signs, regularization,
contraction Gram and low-rank endpoint. Actual source audit passed, including
trace-bound proof and parity/CJ signs. One focused Fable/high16384-token run
ended max_tokens with a 397-character unfinished verdict/convention prefix;
it supplies NO usable proof or completed review. Estimate USD0.828720, retained
at audits/claude_runs/2026-11-07-mixed-gaussian-exterior; no retry or pendingcall.
An exact classical CAS control passed H/J, minus adjugate identity, local
Lefschetz rank, zero CP Schur complement and actual THREE-output/TWO-input
mode CJ contraction. Bell success=1/16 exactly; missing reference correction
fails. This is neither a full learner nor quantum execution. The complete numerical composition and direct-output addendum are accepted
at their written scope, as are the exact/core and source reviews. All three
review files were read; the quantitative deductions above are independent
of the truncated Claude verdict prefix.

The written result is complete for the native exact-IID two-component promise.
The exact control at audits/controls/mixed_gaussian_pair/control.py/.json also
checks eight-dimensional cross-vector reconstruction and the rank2 Gaussian
identity. None is a full learner run; the uniform proof is separate.
False claim gates: novelty, classical-input separation/hardness, practical
resource scale, noisy/off-model source, arbitrary many components, physical
parity-restricted-only gates, human/formal verification and quantum execution.
No component-recovery claim: nonunique low-rank inputs are learned as states.

Next pass: independently compare externally valuable native mechanisms before
any extension or implementation. No tomography backend, nearby rank sweep,
CJ backend or practical benchmark is queued. Mechanical work is limited to
preserving source/control/review links and claim gates at the milestone.

## Checked alternative CJ interface (not used by the final learner)

An earlier output realization was independently source-audited and tested.
It is retained as a convention control, not a prerequisite for the direct
four-Gaussian endpoint above:

The channel endpoint is charged. Primary Gaussian-channel theory supplies a
Gaussian fermionic CJ state. Its covariance in OUR minus-i convention is
  Gamma_CJ=[Z,-L;L^T,0].
The source plus-i convention instead uses [-Z,L;-L^T,0]. This sign change
is required, not an unspecified phase choice.
Bravyi's fermionic tensor identification differs from ordinary Jordan-Wigner
registers by W=(-1)^(N_output N_reference), an explicit O(n) CZ circuit because
the reference has at most2 modes. Under the stated occupation ordering, J(rho_I)=(I tensor V_r)|Omega><Omega|
(I tensor V_r^dagger), where
  V_1=X S,
  V_2=(X tensor X)(S^dagger tensor S) CZ,
  |Omega>=d_core^-1/2 sum_x |x,x>, S=diag(1,i).
Apply V_r^dagger on the reference AFTER W. These include bit complements;
reference phases alone are insufficient. Ordinary qubit gates are authorized.
After these corrections, preparing the normalized ordinary CJ state and Bell
postselecting the identity outcome with the prepared core succeeds exactly
with probability1/d_core²>=1/16. Capped O(log1/epsilon) retries, each using
fresh PREPARED resources, and a fallback on total failure give a deterministic
trace-preserving approximate preparation circuit. No unknown source copies
or free success conditioning are used in this output stage. The source convention and exact finite algebra control agree. A physical
Gaussian CJ approximation with raw trace error e changes the unnormalized
Bell output by at most e, success remains >=1/d_core²-e, and normalized
output raw trace error is at most2 d_core² e. Spectral clipping of an
estimated CJ covariance need not preserve its exact TP marginal: this
success/error bound handles that approximation. Gaussian normal-form
preparation requires O((n+2)²) rotations and thermal probabilities; approximate
their gates/probabilities so the summed trace error is at most e. Their
individual precision is polynomial BIT, with no eigenvector-gap assumption.


## Final scoped milestone

2026-11-07: STATE full title/Now/table and matching handoff/mechanical entries
checked. All three scientific-source PDFs and four selection-source PDFs
match retained SHA256 manifests. Three closed independent reviews retain
the direct four-Gaussian endpoint. Saved exact control is PASS, including
8D cross recovery/rank-two identity, with execution/speedup gates false.
Claude result is terminal truncated/max_tokens, not a completed review;
47 reported estimates total USD38.642370, not an account balance. Scoped
`git diff --check` passed. No broad suite, control rerun or Git action.
