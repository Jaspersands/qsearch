# Post-purity selection: native multi-community label recovery

Recommendation: if the pending general-rank attacks return only known
barriers, select ONE bounded constructive operation: convert the ALL-LABEL
Kikuchi accepted-band energy into planted one-particle mass, then round and
validate a community labeling. This addresses recovery rather than the
already closed detection endpoint. It uses a concrete operator inequality,
not another rank-fidelity conjecture, a top-projector gap promise, or a new
folded/Kerr/arithmetic/HSP wrapper. No novelty or advantage is asserted.

## Why the current purity gate is not an easy compiler

The copies-only component finder is already conditional on polynomial signal.
For any stabilizer phi, its stabilizer projector and Holder give

    |<phi,psi>|^8 <= Pi(psi).

The retained inverse theorem supplies stabilizer fidelity polynomial in Pi.
Thus a polynomial rank-to-purity bound and a polynomial rank-to-stabilizer-
fidelity bound transfer up to constant exponents. Completing the conditional
circuit does not solve that substantial general-rank inequality. Parent's
rank-two analytic lower bound and the cubic tensor falsifier do not settle
arbitrary rank. The construction report is still pending at this selection;
this note does not preempt its result or order a new paid call.

## Comparison of three external problems

**1. Selected: recover labels in the native p-marginal hypergraph SBM.**
Input is ONE explicit Bernoulli hypergraph, fixed even p>=4, fixed k>=3,
known fixed q in (0,1/2), known near-threshold signal, and chosen growing
polylogarithmic ell=o(sqrt(n)). Labels are IID uniform in [k]. Conditional
edge means are

    q + epsilon * sum_a product_{i in edge}(1_{x_i=a}-1/k).

Output ONE labeling z with permutation-invariant agreement exceeding 1/k by
an absolute c_(p,k)>0, with bounded failure probability. No labels, planted
gauge, independent graph, useful eigenvector, or reduced state is supplied.
This is useful in clustering/inference; an eigenvalue-only detector does not
provide the requested partition.

Honest resource target: first a fully native CLASSICAL decoder costing
n^(ell+O_p(1))*poly(inputbits,log(1/eta)), matching the checked log-free
Kikuchi detection frontier up to polynomial overhead. A quantum composition
may subsequently use the already paid accepted-band preparation, polynomial
n-dimensional tomography and rounding; it earns no best-classical claim.
Input reading, matrix application/filtering, clones, success probability,
output length n, precision and repetitions are all charged. No QRAM,
projector oracle or planted-label gauge is assumed.

Strong classical attacks: the retained sharp-Kikuchi accepted-band decoder
for Boolean noisy XOR; direct multi-community adaptation; color coding and
noisy-XOR detection-to-recovery reductions; spectral/tensor methods and
ordinary hypergraph clustering; exhaustive n^ell lifted-state computation.
At much stronger signal simpler polynomial algorithms may dominate. The
model's vanishing lower marginals forbid silently substituting an ordinary
pairwise SBM. No lower bound against all classical algorithms is available.
The selected contribution must be a valid native multi-color decoder, even
if it is completely classical and ultimately known.

Decisive first falsifier: derive the exact all-label signal lift and bound
its collision-free compression error BEFORE cloning or tomography. If a
high-energy population state can have vanishing one-particle mass on the
planted color span, this operation fails. A pure-community Rayleigh witness
alone proves neither this uniform conclusion nor recovery.

**2. Not selected: native short-path exact optimization.**
Input: an explicit bounded-degree graph (and binary weights/activity if used),
output an exact maximum independent set, with its size and feasibility checked.
The contemplated operation is a public graph-only guide/tail certificate
which pays stationary preparation, mixer gap and enhanced optimum overlap.
Its honest clock is instance dependent and generally exponential; replacing
its Markov-search baseline by “best classical” is unjustified.

Classical attacks are exact branch-and-bound/cut, branching algorithms,
component decomposition, treewidth DP, local search and annealing, rather
than only uniform sampling. The corpus already contains a graph-only
classical falsifier for protected planted MIS. SDP/QAOA entries are leads,
not an unrestricted no-go theorem; one returned annealing no-go is explicitly
quarantined and was NOT adopted.

First falsifier of a uniform cheap-guide claim: complete bipartite components
with large binary-encoded activity give two hard-core occupancy phases and
an empty/small-set bottleneck for single-site Glauber updates, while each
fixed-size component is classically enumerable. Thus activity bit length
alone cannot pay that mixing interface. This does not refute short-path
algorithms using other mixers or their actual restricted hypotheses.
No new source-native certificate is presently in hand; it would repeat an
unpaid mixing/overlap interface, so it loses to candidate1.

**3. Not selected: native dissipative PDE terminal sampling.**
Input: an explicitly circuit-specified sparse local diffusion/advection
operator, initial/source data, binary final time and precision. Natural
output is a physical transition location or bounded terminal expectation;
a normalized squared-amplitude output is a DIFFERENT contract and must be
justified separately. The contemplated operation is a normalization-safe
terminal compiler without a supplied solution-state preparation oracle.

Classical attacks: direct Markov paths/uniformization for nonnegative
mass-preserving generators, Feynman--Kac where its weights/variance permit,
Fourier/heat kernels for homogeneous cases, multigrid/Krylov and sparse
integration for general explicit instances. A path sample of u is not
claimed to sample |u|^2. Any claimed advantage must compare the SAME output.
Honest quantum linear-ODE clocks also charge solution norm ratios, source
preparation, coefficient access, time and measurement overhead.

First falsifier of a uniform dissipative normalization claim: A=diag(-1,0),
u(0)=(1,0) has ||u(T)||=exp(-T), although its normalized endpoint is trivial.
A contraction promise does not pay an exp(T) norm ratio. Conversely, positive
mass-preserving terminal transition sampling is already directly classical.
A new general sign-cancellation operation was not identified, so select none
of these broad PDE wrappers.

## The selected concrete operation and proof route

The following constructive route was sharpened with the parent while this
selection was running. Put d=p/2, w_a(i)=1_{x_i=a}-1/k, W_a=w_a w_a^*, and
L=span{w_a}. These objects are ONLY used to analyze the native operator;
no w_a, P_L or labels enter the algorithm. On ell ordered slots let

    B_lift = sum_{|J|=d} sum_{a=1}^k tensor_{j in J} W_a^(j),
    rho_1 = (1/ell) sum_j partial_trace_except_j(sigma).

Since ||w_a||^2<=n and W_a<=n P_L, commuting different-slot projectors give

    tensor_{j in J} W_a^(j) <= (n^d/d) sum_{j in J} P_L^(j),
    B_lift <= k*n^d*binom(ell,d)*(1/ell) sum_j P_L^(j).

This inequality is elementary and has no projector-gap assumption. The NEW
model-specific operation is to identify the exact scaled population
Kikuchi signal with its collision-free compression and pay the collision
remainder uniformly. Combine the retained noise bound with accepted-band
energy: if the normalizations/remainder work, EVERY accepted density state
has Tr(P_L rho_1)>=c_(p,k)>0. The proof must give all factorials, tuple/set
normalizations, imbalance probabilities, spectral thresholds and error
constants. Merely testing a preferred population eigenvector is insufficient.

Trace one makes the leading constant-dimensional eigenspace of rho_1 retain
constant mass on L. Since k is fixed, some w_a then has constant projection
on that computed subspace. A fixed net and clipped randomized rounding give
a finite list with a weakly correlated labeling. Only that low-dimensional
subspace is reconstructed; no full lifted-state tomography is requested.
Classically, thin filtered vectors can be contracted as

    M_ij = (1/ell) sum_T P_{T union{i},T union{j}},

with the exact ordered/set isometry normalization used consistently. The
coefficient counts and contractions must fit n^(ell+O_p(1)); P is not a
free matrix oracle. Quantumly the ordinary deletion isometry and a partial
trace supply rho_1, followed by paid tomography. A full k-block eigenvalue
gap for M is stronger than needed and is NOT an assumption.

To output one labeling rather than merely a list, validate against a weak
clone of the SAME graph. The proposed new three-way asymmetric splitter has
strengths (1-2t,t,t) for matrix, guide and validation; its target total TV
error is O(sqrt(M*beta^4*t^2)), M=binom(n,p). This estimate must be derived
from the actual per-edge channel, not assumed because two-way cloning was
proved earlier. With polylog ell and t=1/log n the prospective near-threshold
regime makes that error small while preserving the training signal.
The validation score is explicitly computable from a candidate z; its mean
has the form epsilon_v*n^p*sum_ab C_ab^p/p! with exact finite-n corrections,
where C is the doubly centered color-confusion matrix. Prove variance,
permutation-advantage extraction and finite bit/repetition costs. The proof
must not expose C or true labels to the algorithm. No independent-graph
advice or source-conditioned “clone” may replace the one-graph channel.

## Actual source gates and next action

Retained `sources/2026-11-13-community-selection/schmidhuber_zlokapa.txt`:
Definition2 LF184--205 gives the exact all-label rank-k signal tensor;
LF649--652 explicitly leaves community-label recovery open in that retained
version. LF281--283 only anticipates tomography/rounding; it is not a decoder.
Its old guided-state theorem is NOT imported without the prior source repair.

Retained `sources/2026-11-13-community-baselines/sharp_kikuchi.txt`:
model LF248--296 is BOOLEAN planted noisy XOR, with support occurrences and
sign labels, not this multi-community Bernoulli HSBM. Proposition12.6 and
Section12.4 LF2866--2929 already supply uniform accepted-band one-particle
mass and rounding in that Boolean model. Partial trace/tomography/rounding
are therefore PRIOR ART. The new obligation is the exact multi-color
population comparison plus native list validation, not renaming that source.
Theorem/model conditions must stay attached when importing its noise methods.

Retained compendium LF2636--2701 and2831--2934 motivate the rejected PDE and
short-path candidates but are not primary theorem authority. No missing
hypothesis was filled from an abstract. Parent-fetch targets if either is
reconsidered: actual generalized short-path2410.23270 AND Le Gall--Tamaki
2604.12131; for the selected classical comparator, Mao2604.10457, cited by
sharp-Kikuchi LF3287. Read actual model/algorithm theorem before deciding
whether it already transfers to the multi-community decoder. The retained
version's “open” paragraph is not a claim that all current literature lacks
this operation. Novelty and advantage remain false.

Corpus gate was performed first with been-tried --no-refresh, then baselines,
for all three precise candidates. Community/PDE baselines returned no catalog
match, which is NOT evidence of absence; actual methods above replace that
empty result. Optimization returned SDP and tensor-network leads plus the
protected-MIS note. No full archive, credentials, status or registry edits,
Git/network/API call, numerical sweep or implementation was used.

Single next action: one independent derivation of the all-label operator
comparison and uniform planted one-body mass, followed by its exact failure
case if it breaks. Read the existing native community certificate, clone
proof and source model; retain fixed q,p,k. Only if this algebraic step
survives should the same task join the three-way channel and validation into
one complete recovery clock. Stop on a counterexample; do not extend into
another generic spectral/mixing promise or a rank-fidelity interface.
