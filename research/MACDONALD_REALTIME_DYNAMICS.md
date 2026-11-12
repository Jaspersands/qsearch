# Native integrable real-time occupation sampling

Question: can a classical algorithm sample the SAME full joint occupation
law after real time under the Nazarov--Sklyanin Hamiltonian, for arbitrary
explicit occupation input, in poly(D,L,b) BIT time? This is the selected
scientific question; all failures below are scoped, never hardness.

Input numerical D>=1; explicit partition mu of D (bosonic occupation m_k),
binary rational tau=a/c (c>0), bit length L, accuracy b. Actual time is
T=2*pi*tau. Global t=D/(D+1), q=t^3; use these parameters at EVERY degree.
Canonical bosonic basis corresponds to p_mu/sqrt(R_mu), where
R_mu=z_mu product_k r_k^m_k, r_k=(1-q^k)/(1-t^k)=1+t^k+t^(2k).
No eigenvector, coefficient table, quantum input, sampler or advice supplied.

Define vertex coefficients V_n by
V(z)=exp(sum_(k>=1) (1-t^k) p_k z^k/k)=sum_n V_n z^n.
Star is adjoint in the Hall(q,t) form. The native self-adjoint Hamiltonian is
H=sum_(n>=1) q^(-n) V_n V_n^*/(1-t), restricted to degree D.
This is actual Nazarov--Sklyanin2015 Eq1.17. Eigenvectors are normalized
Macdonald J_lambda with EXACT rational eigenvalues
E_lambda=sum_(i>=1) (q^(-lambda_i)-1)t^(i-1) (Eq1.18).
The zero-based box sum form is
E_lambda=(q^(-1)-1)sum_(i,j in lambda) t^i q^(-j).
Let U_(nu,lambda) be their real normalized power-sum amplitudes. Target:
P_(mu,tau)(nu)=|sum_lambda U_(nu,lambda) exp(-2*pi*i*tau*E_lambda)
                                      U_(mu,lambda)|^2.
Output one partition nu, within TV 2^-b. Input load costs O(poly D).
Optional simpler observable is a specified normalized mode count k*n_k/D;
its estimation must not be confused with the full sampler.

Existing independently checked WRITTEN transform U and its actual inverse
cost poly(D,b), clean on arbitrary superpositions/reference; no circuit has
been implemented. Accept this interface in this task; do not re-review it.
Then U diag(exp(-2*pi*i*tau*E)) U^dagger is a complete written quantum
candidate costing poly(D,L,b). E is a polynomial-bit rational computable
from lambda. Compute tau*E modulo1 EXACTLY before phase approximation.
Transform error does not grow with |tau|. All lower scratch is retained
and erased up to clean error; no exact-angle or eigenvalue oracle.
This is a direct instance of KNOWN efficient-diagonalization fast forwarding
(Gu--Somma--Sahinoğlu2021 Thm3.1), not novelty or an advantage proof.

Strong baseline: explicit p(D)=exp(O(sqrt D)) symmetric-function linear
algebra, then rational spectral phases, yields exp(O(sqrt D))*poly(D,L,b)
classical sampling. Its time dependence is ALREADY poly(L), so time alone
is not a classical separation. Need improve its dependence on D.
Row/column eigenstate laws have exact weighted-cycle DP. Near-row/column
with deficit s have D^O(s)poly(D,b) samplers (attached note). General
Macdonald eigenstate Born sampling is unresolved. Those eigenstate samplers
do not automatically simulate coherent superpositions or this dynamics.
Jack3 has a stronger bounded-Durfee classical representation (attached
only for the few-phonon obligation), not automatically Macdonald.

Native vertex entries are nonnegative in normalized occupations, so the
positive row eigenvector suggests a Doob transform to a reversible Markov
generator. A stochastic/imaginary-time sampler or stationary-law sampler
is NOT automatically a real-time Born sampler. Exact determinants,
finite-colour lifts and matrix product representations must pay the
representation size, input conversion, output conditionals, signs and
precision. No free trace, random-state loading or physical-position map.
At q=t^3 coincident global contents are legal; do not divide by their gaps.

One-boson useful control: actual Mickler2026 Thm4.1 gives
[p_D]J_lambda=(1-t^D)/D product_(boxes except origin)(t^i-q^j).
Hence it vanishes exactly when lambda_4>=2; first zero (i,j)=(3,1).
This yields polynomial spectral support for mu=(D), but not automatically
an efficient occupation-output sampler. For k>1 do NOT infer individual
p_mu coefficient vanishing from a univariate principal-specialization zero:
cancellations among different mu of the same length are possible.

Falsifiers: exact all-D polynomial classical sampler; a missing native
transform interface; a coefficient/normalization or source-access oracle;
exponential cost hidden in phase precision, conditional sampling or variance.
Do not infer hardness/advantage from failure of any route or finite tests.
No proposal to sweep tiny D unless a concrete identity can be falsified.

## Prior-work and selection

Corpus been-tried/baselines checked before selection; no exact catalog match
is not absence evidence. Actual NS2015 Eq1.17/1.18 and Gu2021 Definitions2.1-2.2,
Theorem3.1 proof read. The old conditional-boson Pauli estimator has different
input/Hamiltonian/output; it is not a sampler here. Unlike another parameter
extension, this candidate uses the closed transform to evolve an easy native
Fock input and asks for a concrete full output. General Selmer classical
matching and conductivity joint-polynomial estimates remain independent high-
upside questions, but require larger unresolved arithmetic/analytic steps;
this pass has a complete quantum endpoint and direct constructive classical
attacks. No claimed separation or circuit implementation.

Four distinct paid obligations, with selected sources and full contracts:
audits/api_inputs/2026-11-13-macdonald-dynamics/dispatch.json. Local ceilings
22USD are not spend or balances. No failed request is repeated.

## Closed written native endpoint

Parent fully read/checked all251lines of
audits/reviews/2026-11-13-macdonald-realtime-independent.md. Exact common
denominator Q_D=D^(3D)(D+1)^D pays all E_lambda. Compute (a*e_lambda) mod
(c*Q_D) exactly before bounded-angle phase gates; phase precision b+O(1),
whole rational arithmetic poly(D,L,b). Same-bank actual U inverse and clean
hybrid give restricted operator error<=2^-b on arbitrary references.
Thus the full native quantum endpoint is CLOSED as a WRITTEN construction.
Explicit monomial conversion/fraction-free positive Gram and separate square
roots pay the exhaustive classical exp(O(sqrt D))*poly(D,L,b) comparator.
Binary time is polynomial for BOTH. No implementation/novelty/hardness/
advantage inferred. Fixed-k full classical sampler is separately under review.

## Terminal Doob report: verified identities and scoped repairs

Claude dynamics-doob-kernel completed190LF lines, parent fully read.
Native positive vertex matrix, positive row Perron vector, exact polynomial
entry computation, Doob conjugation, and update mechanism are accepted.
Let lambda0=q^(-D)-1, R_mu=z_mu product r_k^m_k, pi_mu=1/(Z*R_mu). Then
K_(mu,nu)=[p_nu]H p_mu/lambda0 is row stochastic and reversible. Delete each
part k independently with probability1-q^k, conditional on at least one
deletion; redistribute removed mass n by cycle weights1-t^k. The latter
normalizer is1-t for n>=1. No advice or coefficient table.

Parent checked actual Diaconis--Ram1007.4779v1 Eqs1.3--1.4: their parameters
q_DR=1/q,t_DR=1/t give EXACTLY this kernel. The reported source comparison
was appropriately unchecked; it is now verified, not a new Markov chain.
The reciprocal Hall metric differs only by (t/q)^D on the fixed sector.

Write M=exp(-i theta K), theta=2pi*tau*lambda0. Detailed balance cancels
stationary ratios to give P_(mu,tau)(nu)=M_(mu,nu)*conj(M)_(nu,mu). For
positive theta, a two-leg Poisson trajectory estimator for a bounded O is
v=exp(2theta)*i^(N2-N1)*O(nu)*1{Y=mu}. It is unbiased. For mu=(D),
O=n_D, paths staying at mu give Var(v)>=exp(2theta(1+kappa_D))-1, where
kappa_D=(D+1)(1-t^D)/D>=1/2. Thus this PARTICULAR estimator has exponential
variance, e.g. tau=D. Negative time uses |theta| and conjugated phases.
This is not a lower bound on other estimators or classical samplers.

Repairs: (1) Z<=1 uses native r_k>=1, not arbitrary0<q,t<1. (2) The paid
tight finite-clock BIT exponent omits capped deletion rounds; retain only
poly(D,b). A direct conditioned deletion scan also avoids rejection: track
whether any part was deleted and divide the first-deletion probabilities by
1-product(remaining q^k), all exact polynomial-bit rationals. (3) The
period-time variance example is not decisive against period preprocessing;
raw tau=D suffices to scope the unmodified estimator. (4) The report's
mixing cutoff still depends on theta, so it does not pay logarithmic-time
simulation. No claim that weights are intrinsically unremovable is imported.
(5) At |theta|=O(log D), this estimator gives a polynomial classical
additive-epsilon estimate of one bounded efficiently computed occupation
observable (epsilon^-2 samples, finite-clock truncation paid); this is
not a TV2^-b full sampler. The few-boson construction makes the one-boson
follow-up proposed in the report obsolete if its independent review passes.

## Stronger complete classical match at fixed boson count

MACDONALD_FEW_PHONON_CLASSICAL.md is now independently reviewed and parent-
checked: EVERY explicit mu with fixed k=length(mu), EVERY binary rational
time, FULL output occupation law has a classical bounded-clock sampler
(D+1)^O(k)poly(D,L,b). It keeps all coherent interference. The spectral
hook is lambda_(3k+1)<=k; finite Pieri/Newton lowering on its down-set
pays the output sampler. This closes the few-boson physical-input route,
not arbitrary growing-k dynamics. General bounded-Durfee Macdonald
eigenstate occupation sampling is also classical polynomial.

Claude dynamics-colour-free ended TRUNCATED/EMPTY (0bytes), usage estimate
1.347712USD; no result, no retry, no conclusion about the colour mechanism.
Two OpenAI dynamics jobs remain in flight. Two ADDITIONAL distinct qRSt
condensate jobs are running: api_inputs/2026-11-13-condensate/dispatch.json,
11USD local ceilings (not charges), native spectral/return sampler and
full coherent output. Same scientific question, newly checked source
mechanism, growing rather than fixed initial boson count.

## Terminal dynamics round

All four jobs terminal and reaped. Three completed/nonempty reports fully
parent-checked (Doob190, direct526, few-phonon573LF lines); colour truncated
EMPTY, no retry. Two OpenAI constructions independently supply fixed-k
classical full samplers, no unrestricted one. Material dispositions are in
MACDONALD_FEW_PHONON_CLASSICAL.md. A separate mechanical ledger freeze is
in progress; expected round6.667178USD, cumulative239.449888USD/186priced,
FOUR unknown excluded. Estimates not invoices or balances. The separate
two-job condensate round remains live and is excluded from this milestone.
