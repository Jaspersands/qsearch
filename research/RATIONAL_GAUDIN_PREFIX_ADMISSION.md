# Rational Gaudin prefix norms: constructive admission and exact falsifier

2026-11-07. The proposed delete-site global-norm shortcut is REFUTED on a
native exact eigenstate. Full uniform Bethe preparation remains OPEN; no
quantum speedup, hardness, novelty or general no-go is inferred.

## Selection and native candidate

Previous pass Local Saturation Kernel Structure was PROGRESS; STATE/TRAPS
and newest handoff title matched. Independent re-selection considered the
local Kummer HALF gate, general sparse function-field Rel, native Legendre
reconstruction and full-table scalar OPI. No new operation closed their
conditioning, constant-map, hidden-subspace or adaptive-quality gaps.
The sparse-Puiseux and cyclotomic-specialization ideas still lack a sparse-BIT
clock; OPI prime-field capacity decoding does not transfer to binary fields.
Corpus been-tried and baselines were checked before current literature.
The exact Bethe/XXZ lookup found no applicable catalogue baseline, which is
not evidence of hardness. Actual primary sources then identified the norm
and conditional-state bottleneck; no theorem is inferred from abstracts.

Selected externally motivated question: can determinant structure produce
an efficient complete preparation of an interacting Bethe eigenstate, with
all normalization and classical preprocessing charged? Consider rational
spin-one-half Gaudin/BCS states

    Psi(v;eps)=product_(a=1..M) B(v_a)|0>,
    B(v)=sum_(i=1..N) sigma_i^+/(v-eps_i).

Input for the concrete admission is pairwise distinct REAL RATIONAL site
parameters eps_i and pairwise distinct REAL RATIONAL roots v_a, with no
root/site coincidence, all binary bits charged and growingN,M. Verify that
sum_i1/(v_a-eps_i)-2sum_(b!=a)1/(v_a-v_b)=gamma is the SAME rationalgamma
for alla, and that the state is nonzero. Root data are explicit input to a
state-preparation problem, not a free root-finding subroutine. The exact
counterexample below also refutes this shortcut for broader root-input
models containing rational data. No restriction-to-rational-input theorem
is substituted for arbitrary Bethe-state preparation.

Output target: normalized quantum state within trace error epsilon, with
polynomial BIT/classical preprocessing/gates in input size and log1/epsilon.
No supplied conditional probabilities, normalization, expanded amplitudes,
dual-hole roots or exponentially large Gram matrices. Proposed mechanism:
Cauchy permanent amplitudes via Borchardt; global norm via Gaudin determinant;
compute every prefix norm by replacing the site set in that determinant;
then controlled rotations and exact rational signs prepare the state.

Expected constructive gain would remove binomial/factorial preprocessing
and circuit size in this declared route. It is not itself a classical
separation: specified amplitudes are already classically polynomial-BIT,
and a classical ALL-prefix routine would also give classical Born sampling
and bounded sparse-observable estimation. Actual local form-factor formulas
are further classical comparators. Proof obligations are correct ALL-prefix
norms (both occupied and empty sites), paid dual data if used, finite
precision, gate synthesis and a readout not already matched. A wrong prefix,
uncharged common dual, factorial determinant sum, or exponential conditional
normalization falsifies the proposed polynomial-resource contract.

## Actual source scope and strongest classical attack

Frozen primary PDFs/text/hashes: audits/sources/bethe_prefix_admission/source.json.
Raveh--Nepomechie, https://arxiv.org/pdf/2403.03283 (v3), explicitly has
binomial(L,M) circuit size and expensive recursion coefficients. Ruiz etal,
https://scipost.org/SciPostPhys.18.6.187/pdf , Eq90--93 and following discussion,
requires subset-indexed Gram/Cholesky matrices for its general algebraic
Bethe circuits. Their size is a limitation of the written construction,
NOT a lower bound on all quantum circuits or on all scalar-product methods.

Claeys etal, https://arxiv.org/pdf/1501.05827 , Eq49--50 and following,
uses the Cauchy/Borchardt identity to pay each specified amplitude. Its
Eq62--69 normalization uses normal and dual descriptions of the SAME
normalized eigenstate, related through the RG equations. It does not supply
such a common dual after arbitrary prefix projection.

Sklyanin, https://arxiv.org/pdf/solv-int/9708007 , Theorem2/Eq2.22--2.23
is an ON-SHELL norm determinant. Theorem5/Eq5.9--5.11 is a sum ofM!
determinants for general scalar products; the proof explicitly invokes the
Bethe equations to leave only the identity-permutation term in the norm.
The general correlator formula sums coordinated partitions. These formulas
do not establish a polynomial all-prefix algorithm; their literal factorial
cost does not prove that such an algorithm cannot exist.

The cheapest classical test is exact Cauchy amplitudes and the explicit
pairing Hamiltonian on one small native instance, performed before any
quantum implementation. Finite computation falsifies the asserted identity;
it is not extrapolated into asymptotic hardness.

## Exact two-root identity and counterexample

For two real roots put a_i=1/(v1-eps_i), b_i=1/(v2-eps_i), d=v2-v1.
For any retained site setU define A=sum_U a_i², B=sum_U b_i², K=sum_U a_i b_i.
The amplitude on distinct occupiedsites{i,j} is a_i b_j+a_j b_i. Therefore

    Z_U=sum_(i<j inU)(a_i b_j+a_j b_i)²
       = A B + K² -2sum_U a_i² b_i².

Since a_i-b_i=d*a_i*b_i,

    Z_U=A B+K²-2(A+B)/d²+4K/d².

The same-root Gaudin matrix built usingU has diagonalA-2/d²,B-2/d²
and off-diagonal2/d². Hence

    Z_U-detG_U = K*(K+4/d²).                       (1)

The full two-root Bethe equations with commongamma implyK=-4/d²,
so the global determinant is correct. Deleting a site changesK and need
not preserve this relation. No approximation or asymptotic assumption enters.

TakeN4,M2, eps=(1/2,2,1/5,7/5), rootsv=(-1,1), gamma=-5/4.
Then a=(-2/3,-1/3,-5/6,-5/12), b=(2,-1,5/4,-5/2),
A=205/144,B=205/16,K=-1,d=2. Both equations hold exactly.
The independently constructed six-dimensional hard-core pairing Hamiltonian

    H=sum_i eps_i n_i-(4/5)sum_(i,j) sigma_i^+sigma_j^-

has this permanent-amplitude vector as an eigenstate of energyv1+v2=0.
It is a valid interacting eigenstate; the failure is not an invalid root set.

Full norm=detG=25625/2304. Project the FIRST site EMPTY, retaining both roots.
The true prefix norm is9625/2304 and its probability is77/205. The deleted-site
determinant instead is8601/2304, differing by4/9. HereK'=1/3, and the
Bethe residuals relative to originalgamma are(2/3,-2): the prefix is OFF SHELL.
The direct global-norm-to-prefix shortcut is therefore refuted.

## Common-dual repair also fails on this prefix

After the same empty-first projection there are three sites and two
excitations. A single one-hole Cauchy dual C(w)|111>, up to scalar kappa,
would have missing-site amplitudes kappa/(w-eps_i). For the remaining-site
order(2,1/5,7/5), the actual amplitudes are(25/16,5/4,5/12), and their
reciprocals are(16/25,4/5,12/5). Consecutive slopes versus eps_i are-4/45
and4/3, unequal. They cannot be the affine function(w-eps_i)/kappa.
This rules out that single same-state dual for any finite complexw/scalar;
the scaled w-at-infinity limit gives constant amplitudes and also fails.
A pole limit can have one supported configuration, not all three nonzero.
This is a proof-only exact check, independently reviewed; the frozen
control was not rerun. Sums of duals or other norm algorithms are unexcluded.

## Classical readout if a genuine prefix operation were found

For an M-site configurationS the Cauchy determinant is nonzero under the
input assumptions, so Borchardt computes its signed rational amplitudeA(S)
exactly in polynomial BIT, even when the permanent itself is zero. A common
product of the denominators of all NM Cauchy entries has polynomial bit
length and clears every amplitude. Its square clears every prefix squared
norm; summing at most2^N terms adds at mostN numerator bits. Thus answers
have polynomial bit SIZE, but their computation is not supplied by that fact.

If an actual classical routine returns ALL prefix norms Z_z in polynomial
BIT at the needed accuracy, sequential draws with probabilityZ_(z1)/Z_z
sample the Born law. Zero-weight prefixes are never visited. Required
relative/conditional accuracy must be paid; additive inverse-polynomial
error on tiny unnormalized norms is insufficient. Per-step errors sum to
total variation error, and capped rational sampling has a charged failure
probability.

For an efficiently row-sparse observableO with charged bound||O||<=Lambda,
the local estimator on a Born sampleX withA(X)!=0 is

    L_O(X)=sum_Y O_(X,Y)*A(Y)/A(X).

It is unbiased and E|L_O|²<=Lambda², by cancellation and the operator norm.
Independent samples give polynomial additive-error estimation, including
polynomial sums of bounded Pauli strings. Approximate sampling is handled
by clipping atR=O(Lambda²/epsilon), biasO(Lambda²/R), then choosingTVerror
delta with2Rdelta small. This is a matched classical counterpart to the
specific classical-prefix-norm preparation mechanism; it does not simulate
arbitrary later quantum circuits or provide a sampler without that routine.

## Paid one-site marginal baseline

The failed deletion rule must not be confused with the complexity of one
marginal. For fixed finite coupling g=-1/gamma, the Bethe-equation Jacobian
with respect to roots is -Gcal, where Gcal is the on-shell norm matrix.
Differentiating with respect to a single site epsilon_i gives

    Gcal * (dv/depsilon_i) = w_i,
    (w_i)_a = 1/(v_a-epsilon_i)^2.

Nonzero state norm makes detGcal nonzero, so the implicit root branch and
this rational linear solve are paid. For H=sum epsilon_i n_i-g S+ S-,
E=sum v_a. Differentiating H Psi=E Psi and taking its normalized inner
product gives <n_i>=dE/depsilon_i=1^T Gcal^-1 w_i. This argument needs a
differentiable eigenvector branch, supplied here by the implicit equations;
accidental eigenvalue degeneracy alone does not invalidate that identity.
For the retained finite-coupling example, i=first gives128/205 and hence
the correct empty probability77/205. No new control run is needed.

This is a polynomial rational-BIT baseline for one marginal in the stated
on-shell finite-coupling regime. After prior projections the state generally
has no such on-shell description. Higher energy derivatives are response
quantities and cannot be identified with arbitrary joint occupation moments
without an additional proof. This formula does not supply ALL-prefix norms.

## Constructive residual and terminal API outcome

Core and source reviews CLOSED:
audits/reviews/2026-11-07-bethe-prefix-core.md and
2026-11-07-bethe-prefix-sources.md. Parent read both, the relevant primary
statements/proofs and frozen control. One exact Sage run PASS at
 audits/controls/bethe_prefix_admission/control.py and result.json;
independent pairing-Hamiltonian, all six Borchardt checks (including zero),
full norm, wrong prefix, root residuals and two-root identity verified.
No old control rerun; all fullalgorithm/hardness/general-no-go gatesfalse.

The remaining operation is an actual polynomial all-prefix norm formula,
not the false deletion rule. Determinant amplitudes alone do not supply
conditional masses. A common dual after projection is not free advice.
No general inability to prepare Bethe states, #P-hardness or circuit lower
bound is claimed. The narrow Claude constructive request at
`audits/claude_runs/2026-11-07-bethe-prefix-repair` terminated with ReadTimeout
and EMPTY response; the process was reaped. There is no mathematical finding.
The partial counter is USD0.027600, with billing UNKNOWN; it is not a final
charge or zero-cost request. No retry was made. Aggregate72 NONPARTIAL usage
estimates remain USD57.237428/37 completed reports. Two separate timeouts
now have unresolved billing (partial countersUSD0.006250 andUSD0.027600).
Neither this aggregate nor the owner's earlier balance anchor is a current
measured balance. Dedicated expiring-credit authorization remains active.

The focused one-site addendum is CLOSED; parent read its commutator,
Jacobian and Hellmann-Feynman proof. Scoped final artifact:
audits/controls/bethe_prefix_admission/checkpoint.json. Controls are not rerun.
Acceptance for reopening is a proved, paid ALL-prefix operation surviving
both exact counterexamples, with no factorial list or hidden dual input.
Any observable advantage must first face the classical sampler/amplitude
estimator implied by the same operation. If the repair fails, pivot rather
than adding another conditional-norm subsystem.
