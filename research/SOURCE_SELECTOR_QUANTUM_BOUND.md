# Before the Final Selector Measurement

Status: derived, review pending. Not formally verified, independently
reviewed, or established as novel. This is a restricted information bound,
not a quantum algorithm, a classical sampler, or a general HSP no-go.

## Result and Scope

The [full-source Walsh bound](SOURCE_CATEGORY_WALSH.md) only bounded a
particular measured transcript. The state BEFORE Walsh can contain more
information. The new argument keeps all classical source labels and the
entire quantum selector, with every physical coset input discarded:

    T_uniform <= min(1, raw_copy_bound,
        2k sqrt(r/M) + D rho_bulk^k + 4 sqrt(D) rho_endpoint^k),

    rho_bulk     = min(1, 1/2 + 3/sqrt(L)),
    rho_endpoint = min(1, (1+2/sqrt(L))/sqrt(2)),
    D=n!, M=(n-1)!!, L=n(n-1)/2, even n>=8.

Here T_uniform means T(Omega_0, E_h Omega_h): h is drawn uniformly ONCE
from the involution class and shared by every copy. It is not
E_h T(Omega_0,Omega_h). The latter obeys the mixture/remainder bound below,
but cannot in general be capped by the raw-copy bound. Central unitary
phases are a special case where covariance makes every output Omega_h equal.

The source partition has r categories. Taking every irrep separately is
covered with r=p(n)<=2^(n-1). Any final POVM on the retained source records
and quantum selector is bounded by this trace distance, even if no efficient
implementation of that POVM is known.

Assumptions:

- Only standard mixed coset inputs rho_0=I/D or rho_h=(I+R_h)/D, with one
  shared h from the fixed-point-free involution class. There is no additional
  hidden-correlated classical side information.
- The source irrep partition and common GROUP-ALGEBRA unitary
  U=sum_g a_g R_g are fixed BEFORE inputs. U need not be central: its
  matrices on irreps may be arbitrary unitaries, not just scalar phases.
  These choices must be independent of h, not selected using an earlier
  hidden-correlated oracle transcript before preparing the coset registers.
  Regular unitarity ensures that the same algebra element is unitary in
  every subset diagonal representation, including the empty-mask scalar.
- Source records are CLASSICAL. Coherent physical source, row or multiplicity
  registers are not secretly retained.
- One coherent common subset query U_S=sum_g a_g tensor_i R_g^(1[i in S])
  uses the full uniform mask, including the correct empty-mask scalar.
- Every physical coset register is discarded. The full selector remains
  quantum until an arbitrary final measurement or processing.

At S1024 k=17528, outward integer rounding gives T_uniform<=2^-1662 for all
source labels. At S4096 k=86488 it gives <=2^-8744. For polynomial
k>=(1+epsilon)log2(D), fixed epsilon>0, the bound is superpolynomially small.
The raw-copy bound separately covers small k. This UNPRUNED estimate left
an intermediate window. The subsequent [typical-mask refinement](TYPICAL_MASK_OBSTRUCTION.md)
closes it asymptotically for every polynomial budget within this architecture.
At S1024 k=8764 the unpruned estimate is vacuous, but the refined bound is
2^-544. The conservative finite all-budget certificate at S1024 remains
vacuous; at S4096 it covers every k<=4096^2 with T<=2^-571.

k is the participating mask length, not the available copy budget. An
algorithm can ignore copies. This does not cover multiple queries,
source-adaptive physical operations, retained physical inputs or
coherent source registers. It does not prove a natural graph/code reduction.

## Unnormalized Local Quantum Kernel

For source category j, let

    p_j(g) = D^-1 sum_(lambda in j) d_lambda chi_lambda(g),
    p_j0(g)=p_j(g), p_jh(g)=p_j(g)+p_j(hg), q_jeta=p_jeta(e).

Keep these unnormalized source weights; sum_j q_jeta=1. With selector row
and column bits in the existing little-endian convention, the local matrix is

    K_jeta(u,v) = (1/2) [[q_jeta,       p_jeta(u^-1)],
                        [p_jeta(v),   p_jeta(u^-1 v)]].

For a fixed source tuple j=(j_1,...,j_k), its subnormalized selector block is

    Omega_eta[j] = sum_(u,v) conjugate(a_u) a_v
                         tensor_i K_(j_i,eta)(u,v).

The complete state is the classical direct sum over source tuples. Average
the SAME h after taking products. Only the central-unitary special case
can use the existing conjugation covariance to reduce to one representative.
A product of averages would be a different input.

The finite verifier assembles these local matrices and independently
compares them with the existing conditional selector kernel and physically
computed source/selector trace distance. It keeps zero source masses,
checks Hermiticity and positivity, and does not normalize selected sources.
Source multisets are used only with exact multinomial multiplicities;
permuting the source tuple also permutes selector qubits.

## The Coset Diagonal Is a Positive Quantum Mixture

Write H_0={e}, H_h={e,h}. On u^-1 v in H_eta, the local matrix reduces to

    F_(eta,g)[j] = (q_jeta I + p_jeta(g) X)/2.

This is positive because |p_jeta(g)|<=q_jeta, and the classical direct sum
over j has trace one. The same coefficient identities as in the Walsh proof
give the full positive comparison states

    Q_0 = sum_g |a_g|^2 F_(0,g)^tensor k,
    Q_h = (1/2) sum_g |a_g+a_(gh)|^2 F_(h,g)^tensor k.

The RIGHT translate gh comes from v=uh on u^-1 v in H_h. Unitarity gives
sum |a_g|^2=1 and sum conjugate(a_g)a_(gh)=0. Also F_(h,gh)=F_(h,g), so
the mixtures are normalized. The earlier central case could replace gh by
hg in the coefficients; that simplification is not used here.

Crucially, ALL F_(eta,g) commute: their blocks are combinations of I and X
in a common classical source basis. Consequently the quantum trace distance
between Q_0 and Q_h equals the classical distance after source/Walsh
diagonalization. The mixed-overlap argument can be rederived WITHOUT a
central coefficient distribution. Define

    B_j(h) = sum_g |a_g|^2 p_j(hg)^2,
    S_j(h) = sum_g |a_g|^2 |p_j(hg)|,
    R_j(h) = sum_g |a_g a_(gh) p_j(g)|.

Projector orthogonality gives sum_x p_j(x)^2=q_j. For each fixed g,
the set {hg : h in C} is a subset of G, hence

    E_h B_j(h) <= q_j/M.

This is an AVERAGED statement. It does not require |a_g|^2 to be central.
Cauchy-Schwarz gives S_j(h)<=sqrt(B_j(h)). It also gives

    R_j(h)^2 <= sum_g |a_(gh)|^2 p_j(g)^2
              = sum_u |a_u|^2 p_j(uh)^2 = B_j(h),

using the class-function identity p_j(uh)=p_j(hu). Jensen therefore bounds
both E_h S_j(h) and E_h R_j(h) by sqrt(q_j/M). Separately,
|p_j(h)|<=sqrt(q_j/M) holds pointwise because p_j IS a class function.

Expand Q_h-Q_0 as the sum of the cross-weight term
sum_g Re(conjugate(a_g)a_(gh)) F_(h,g)^tensor k and the product-law change
sum_g |a_g|^2 [F_(h,g)^tensor k-F_(0,g)^tensor k]. Subtract the reference
product with local law R_h(j,z)=q_jh/2 from the first term, whose weights
sum to zero. Product-law Lipschitz continuity and g -> gh give

    T(Q_0,Q_h) <= k sum_j R_j(h)
                  + (k/2) sum_j (|p_j(h)|+S_j(h)),
    E_h T(Q_0,Q_h) <= 2k sum_j sqrt(q_j/M) <= 2k sqrt(r/M).

This transfers a bound on the COMPARISON mixtures, not on the actual
dephased output. The actual Omega states need not commute. Neither Q is
an exact small-k state or an efficient classical sampler.

## The Quantum Remainder Requires a Different Endpoint Bound

Let R(u,v)=sum_j ||K_jeta(u,v)||_1. The trace norm of tensor products is
multiplicative, and the trace norm of classical direct sums is additive.
Triangle inequality therefore gives

    T(Omega_eta,Q_eta)
      <= (1/2) sum_(u^-1 v outside H_eta) |a_u a_v| R(u,v)^k.

There are three checks:

1. Always R<=1. Each K is a cross-Gram matrix formed from the weighted
   source state and the two group-action columns I,R_u. Their Hilbert-Schmidt
   norms are sqrt(q_jeta). Schatten Cauchy-Schwarz gives ||K_j||_1<=q_jeta;
   summing j gives one. This argument applies to non-Hermitian off-diagonal
   kernels, not just density matrices.
2. If u,v and u^-1 v are all outside H_eta, use the q_jeta/2 matrix unit as
   the nonnegative baseline. Its total trace norm is 1/2. Entrywise triangle
   inequality charges the other three entries. Column orthogonality gives
   sum_j |p_j(g)|<=1/sqrt(class(g)), independent of category count. Each
   alternative entry costs at most 2/sqrt(L), so R<=1/2+3/sqrt(L).
3. If exactly one endpoint is in H_eta, K_j has rank one with norm
   sqrt(q_jeta^2+p_jeta(v)^2)/sqrt(2), up to transposition and translation.
   Thus R<=1/sqrt(2)+sqrt(2)/sqrt(L). The old Walsh endpoint bound 1/2 is
   FALSE for this unmeasured state.

The bulk absolute pair weight is at most (sum_g |a_g|)^2<=D. The endpoint
weight is at most 2||a restricted to H_eta||_1 ||a||_1
<=2 sqrt(|H_eta| D). After the half-trace-norm factor and the two hypotheses,
the endpoint coefficient is at most (1+sqrt(2))sqrt(D), conservatively
bounded by 4sqrt(D). These remainders are bounded uniformly in h. Combining
them with the averaged mixture separation gives

    E_h T(Omega_0,Omega_h)
      <= 2k sqrt(r/M)+D rho_bulk^k+4sqrt(D) rho_endpoint^k.

Convexity bounds T(Omega_0,E_h Omega_h) by this average. Only THIS decision
distance is additionally capped by the raw-copy bound through data
processing on rho_0^tensor k versus E_h rho_h^tensor k. A fixed h must not
be secretly supplied to the operation or final decision rule.

The minimum class estimate L=C(n,2) is justified in
[the source-category note](SOURCE_CATEGORY_WALSH.md). For large n,
rho_bulk=1/2+O(1/n) and rho_endpoint=1/sqrt(2)+O(1/n). Both remainder terms
therefore decay superpolynomially above (1+epsilon)log2(D). The mixture
term also decays for polynomial k and r<=2^(n-1).

The implementation rounds sqrt(L) DOWN and computes the endpoint radius
SQUARED as an exact rational. It never approximates exponentially small
probabilities with floating-point zeros. Component and filter bounds are
rounded outward and the raw-copy bound is retained separately.

## Why the Raw-Copy Cap Needs the Averaged Hypothesis

The cap can be checked independently in the regular basis. Before the
channel, put Delta=E_h rho_h^tensor k-rho_0^tensor k. Expansion gives

    Delta = D^-k M^-1 sum_(nonempty S subset [k]) sum_(h in C) R_h^S.

The regular operators indexed by (S,h) in this sum are Hilbert-Schmidt
orthogonal. Different supports leave a nonidentity action in one coordinate;
equal supports with distinct involutions also have zero regular trace.
Each squared norm is D^k, so

    Tr(Delta^2) = (2^k-1)/(M D^k),
    T(rho_0^tensor k,E_h rho_h^tensor k)
      <= (1/2) sqrt((2^k-1)/M).

Data processing through the SAME hidden-independent channel proves the cap
on the decision output. In contrast, for EACH fixed h the input has
T(rho_0^tensor k,rho_h^tensor k)=1-2^-k, since rho_h^tensor k is uniform
on a rank-D^k/2^k subspace. Thus even the input itself falsifies applying
the cap to the average individual trace distance. This is an elementary
restatement of the input bound, not a new sample-complexity theorem.

## Fixed-Weight and Other Diagonal Mask Filters

Let F be an input-independent diagonal selector operator, ||F||<=1, with
success probability p on the uniform mask. It commutes with the controlled
query and with classical source recording. Every diagonal selector entry,
conditional on any source tuple, is its natural source mass divided by 2^k.
Hence p is independent of the hypothesis and source tuple, and

    Omega_F = F Omega_uniform F^dagger / p,
    T(Omega_(F,0), Omega_(F,h))
        <= T(Omega_(uniform,0), Omega_(uniform,h)) / p,
    T(Omega_(F,0), E_h Omega_(F,h)) <= T_uniform / p.

The first inequality is pointwise; only the second uses T_uniform as defined
above for the class-averaged decision problem. They must not be interchanged
for a noncentral unitary. This corrects an ambiguity in the earlier note.

This is also the output obtained by preparing the normalized filtered mask
BEFORE the query. There is no requirement to prepare it by physical
postselection. It is a mathematical comparison, not a runtime lower bound.

For a weight-m projector, p=C(k,m)/2^k. At m=floor(k/2), p>=1/(k+1).
Thus central fixed-weight masks pay only a polynomial information factor
and remain obstructed in the same large-copy regime. At S1024 k=17528,
the outward filtered bound is 2^-1647. Exponentially rare filters can make
the comparison vacuous, which is not positive evidence for an algorithm.

More generally, a normalized fixed pure mask alpha can be written as such
a filter with p=1/(2^k max_s |alpha_s|^2). The code accepts a certified exact
rational LOWER bound on a common success probability; it does not infer one
from a declaration of efficient preparation. The filter must be a contraction.

The later [environmental-fidelity bound](MASK_TAIL_FIDELITY_OBSTRUCTION.md)
can avoid this overlap penalty for masks with sufficiently small low-weight
tails. It does not obstruct every mask or supersede the sharper uniform bound.

The raw-copy information bound still applies directly to a deterministically
prepared normalized mask. It should not be weakened by dividing that bound
by p. Conversely, one cannot apply the OLD measured-Walsh theorem to a
pre-Walsh filter: that is not classical postprocessing of a Walsh transcript.

## Finite Controls and Attempts to Falsify

Controls cover three phase rules, including complex character-ratio
rotations, S3 at k=1..4 and S4 at k=1..3. ALL weight sectors are tested;
only testing empty, singleton and full masks would miss nontrivial cases.
The tests explicitly include the balanced S3 k=4 weight-two mask and the
S4 k=3 weight-two mask, as well as zero-mass source labels.

At S4 k=3 with complex phases, the full selector/source distance is
0.518263 while the Walsh transcript has 0.443594. Its positive quantum
comparison mixture has distance 0.498055, and the individual comparison
errors are substantial at this small k. Replacing the quantum distance by
the Walsh value or silently dropping the remainder would be incorrect.

The null endpoint kernel norms at S4 range above 0.745; the alternative can
reach one. They cannot use the Walsh radius 1/2. At S3 k=4 with complex
phases, the balanced fixed-weight selector distance is 0.575596; the
uniform-selector distance is 0.592836. Neither is a growing-degree result.

Independent finite matrix checks do not prove the asymptotic theorem. The
common group-algebra operation, classical nature of source records, shared h, complex
conjugation convention, endpoint weight, and filter success assumptions are
the principal review targets. Existing coset-state and measured-sieve
limitations provide context, not an independent certification of this
access contract: [joint coset-state lower bounds](https://arxiv.org/abs/quant-ph/0511148)
and [measured-sieve limitations](https://arxiv.org/abs/quant-ph/0612089).

### Noncentral Adversarial Controls

Twenty additional controls use a predeclared group involution and an ordered
product of three noncommuting involution rotations. The unitary is formed
in the regular basis first, then its group-algebra coefficients are recovered
and checked. Every controlled subset is explicitly unitary, including the
empty subset. Kernel blocks are compared with sparse regular-basis physical
queries applied to full source-projected density matrices. These controls
cover S3 k=1..3 and S4 k=1..2, retaining either all irrep labels or one
aggregate category, and evaluate EVERY hidden member, not one representative.

Let h_star be a publicly fixed reference involution and choose U=R_h_star,
with source labels discarded. If the actual unknown h equals h_star, the
selector is |+><+|^tensor k instead of I/2^k; otherwise the selector equals
the null state. Consequently

    T(Omega_0,E_h Omega_h)=(1-2^-k)/M.

At S4 k=2 the three individual distances are (3/4,0,0), while the decision
distance is 1/4. The overlap B(h_star)=1 violates the pointwise q/M=1/3
bound, but E_h B(h)=1/3 satisfies the averaged bound exactly. h_star was
fixed before the actual h; this is a countercontrol, not hidden-side access.

Replacing the shared h by independent hidden members per copy incorrectly
gives decision distance 7/36 instead of 1/4 in that control; the two output
states differ by 1/9. Averaging and trace norm are also distinct: the S3
k=2 ordered-rotation control with all labels gives decision distance
0.400276, versus average individual distance 0.436881. Tests preserve each
quantity separately. The noncentral extension therefore removes a real
assumption of the earlier theorem without importing its pointwise shortcut.
The noncentral extension alone did not close the intermediate window.
The typical-mask refinement now does so asymptotically, subject to its scope
and review obligations; neither extension establishes novelty.

## Consequence for the Search

Merely omitting measurement of a coherently copied irrep label is NOT a
genuine escape from classical source records. Standard mixed coset states
commute with central source projectors. For V=sum_j |j> P_j,

    V rho_eta V^dagger = sum_j |j><j| tensor P_j rho_eta P_j.

The label copy is already classical. Every common subset group-algebra query
commutes with the individual source projectors and preserves this structure.
S3/S4 checks verify the clean label-copy identity for every hidden member
and the central-projector commutators with every group action. An explicitly
NONSTANDARD pure superposition of the trivial and sign regular vectors has
label-dephasing trace distance 1/2, confirming that the input assumption
matters. It is a counterexample to an overgeneralized identity, not an
available HSP input or a proposed algorithm.

The mutation pipeline therefore requires a real change of physical
information or operation, not a renamed classical/coherent flag. Retaining
nontrivial physical carrier data or changing the input-access model is a
different question; the copied label alone supplies no extra resource.

Changing only the final POVM, common unitary, or polynomial participating-copy
count is no longer a justified escape for the uniform-mask, physical-discard
architecture: see the typical-mask polynomial-budget theorem. Central-weight
masks have a charged polynomial-overlap transfer. A genuinely different
direction must retain useful physical data, use multiple queries, change
operations based on sources, or supply and charge a mask outside that
comparison. All need a normalized joint law and strong baselines. A
source-controlled diagonal selector phase alone can commute to final
processing and is not necessarily a changed physical resource.

Run `python qsearch.py coset-binary-carrier-instruments` for the finite
controls, quantum scaling and filter contracts. Existing registry records,
dequantization findings, proof debt and mutation obligations carry the scoped
result; no candidate is promoted and no speedup claim is enabled.

## Result Readiness and Prior-Art Check

This is a candidate research result, not yet a publishable result. The
distinction is consequential: tests check finite implementations and scope
contracts, not novelty or the correctness of every asymptotic inference.

On 2026-09-13 the following primary-source passages were rechecked:

- [Hallgren, Roetteler and Sen, Theorem 2 and Corollary 3](https://arxiv.org/html/quant-ph/0511148v1):
  these bound measurements on small blocks of coset states, including
  adaptively chosen measurements on fresh blocks. Their bound grows with
  the block size. The present large-k obstruction instead restricts the
  channel before a final unrestricted selector measurement. Applying their
  small-block bound alone does not supply this large-k conclusion.
- [Moore, Russell and Sniady, Section 3](https://arxiv.org/html/quant-ph/0612089v3):
  the modeled sieve combines two current states, measures a tensor-product
  irrep, consumes both states, and decides from the resulting classical
  forest transcript. A coherent superposition of overlapping subsets with
  an unmeasured selector is not identified with that transcript here. No
  simulation establishing such an identification has been supplied.

These are scope comparisons, not a novelty certificate. Targeted arXiv
searches also returned these established barriers but did not establish
the absence of an equivalent result elsewhere. The two exclusions must
not be advertised as overcoming the published barriers: this project has
derived a further restriction on its own architecture, not a successful
algorithm outside them.

Before external dissemination as a new theorem, require:

1. A second derivation or independent review of the quantum-kernel identity,
   the coset-diagonal coefficient reduction, and the norm constants.
2. An explicit prior-art implication check, including whether general
   representation-theoretic measurement bounds already imply this result.
3. A short standalone statement and proof with the physical input, same-h
   convention, filter normalization and every retained register specified.
4. An explanation of why this restricted architecture was a substantive
   algorithmic proposal, rather than a conveniently weak straw target.
5. Reproducible finite controls and disclosed integration-test failures.

Failure of novelty is a legitimate outcome: retain the reusable bound but
credit the existing theorem. Failure of the proof requires retracting the
derived claim and downstream negatives, not adjusting tests to preserve it.
The typical-mask theorem supplies a derived asymptotic closure, not an
independent novelty certificate. A useful physical operation outside its
scope would be further research, not a completion criterion that can be
met by generating additional registry entries.

## Verification Record

Final fresh regression on 2026-09-13: 186 tests passed in 214.51 seconds.
Coverage includes the new quantum controls, binary instruments, mechanism
synthesis, the corrected symmetric-lift source-path regression,
dequantization, mutation, proof provenance and registry IO. Python
compilation, `node --check site/progress.js`, and `git diff --check` passed.

The final live synthesis, dequantize, proofs, conjectures, mutate, progress,
validate and proof-routes workflows completed. The binary artifact contains
21 quantum controls, 267 source multisets, 69 weight-sector controls and
eight standard-input label-copy controls. Registry validation reports no
issues; the quantum-bound status remains derived/review-pending.

The full suite is not green: an earlier full attempt in this pass stopped
after 65 passes on the missing character-moment scaling-registry write at
`tests/test_character_moment_obstruction.py:73`. A separate scoped run
exposed a missing symmetric-lift experiment-result write at
`tests/test_dcp_symmetric_relation_lift.py:117`. Neither failure was hidden
by changing mathematical expectations or disabling tests. See
`research/AGENT_HANDOFF.md` for the bounded maintenance work and next review.
