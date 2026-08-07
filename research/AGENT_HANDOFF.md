# Research Agent Handoff

Last updated: 2026-08-06

## Objective And Operating Policy

Maximize this repository's expected contribution to discovering or falsifying
a Shor-level quantum algorithm. Do not restore legacy tiny-circuit search and
do not promote finite numerical behavior, query-model mismatches, or weak
oracle separations into speedup claims.

The user specifically wants the current high-capability Codex task spent on
hard reasoning: theorem derivation, research-direction selection, structural
falsification, representation-theoretic reductions, and identifying decisive
experiments. Routine wiring, artifact refreshes, broad repetitive test runs,
formatting, and other low-reasoning work should be batched or left clearly
specified for Gemini 3.6 Flash running through Antigravity after Codex usage is
exhausted.

This model allocation is part of the research goal, not an optional efficiency
preference. While high-capability Codex usage remains, choose work whose main
bottleneck is mathematical judgment: prove or kill a mechanism, find the
correct asymptotic boundary, expose a hidden reduction, or specify a decisive
falsifier. Do not consume that budget on copied CLI dispatch, JSON registry
upserts, README command lists, formatting, or broad routine reruns. Before the
task ends, leave every remaining mechanical action executable by Gemini 3.6
Flash without requiring it to reconstruct the mathematical reasoning. Gemini
must preserve theorem scope, claim gates, negative results, and the ban on toy
oracle/circuit search; it should not promote an artifact merely because tests
pass.

## Authoritative Current State

- Branch: `main`.
- Do not commit frequently. The last known pushed commit before the current
  large research pass was `37915e74bb7ec9f69504381cbdab94f0e557323b`.
- The worktree contains a large coherent uncommitted research pass. Do not
  discard, reset, or rewrite it wholesale.
- User-owned deletions under `ag-remote/` must remain untouched.
- Latest registry validation: 8 candidates, 266 experiments, 391 results,
  639 negative results, 782 dequantization checks, and no registry issues.
- Latest theorem-focused physical-transfer/flag check: 20 tests passed in
  18.85 seconds.
- Latest equal-Gram/polar-chain check: 26 tests passed in 19.61 seconds.
- Latest shorted-metric/coefficient/transport theorem chain: 35 tests passed
  in 29.71 seconds.
- Latest common-core atomization plus dependency-homology check: 14 tests
  passed in 29.70 seconds.
- Latest pair-core recoupling-boundary check: 5 tests passed in 12.07 seconds.
- Latest sparse-parity/relative-Cech/augmented-Cech focused check: 18 tests
  passed in 17.17 seconds. The broader affected theorem check passed 31 of 32
  tests; its sole failure was a comparator that incorrectly allowed sign on
  empty patterns and was corrected before the 18-test rerun.
- Latest recursive pair-generation check: 4 tests passed in 46.73 seconds,
  including the complete 11,025-node S5 exhaustive boundary.
- Latest pair-quotient overlap check: 4 tests passed in 6.39 seconds.
- Expanded pair-quotient overlap check: 5 tests passed in 20.87 seconds after
  adding the 693-merge S6 Gram-factor screen.
- Latest carrier-factorization check: 10 tests passed in 2.72 seconds.
- Latest multistar-degree check: 8 tests passed in 16.37 seconds.
- Latest orientation-Laplacian-gap check: 10 tests passed in 14.92 seconds.
- The carrier-factorization and multistar-degree modules are now fully wired
  (registry seed, `qsearch.py` subcommand, runner dispatch, clean-registry
  dispatch tests, README, Sellke literature record). The Laplacian-gap module
  below is **not** wired yet; that is queued mechanical work.
- Latest affected-theorem regression (recoupling boundary, atomization, pair
  angles, triple range, pair-quotient overlap): 30 tests passed in 35.82
  seconds.
- `python -m compileall -q .`, `node --check site/progress.js`, and
  `git diff --check` are clean as of this pass.
- The newest theorem artifacts contain one globally distinct S6 full-merge
  counterexample to universal half-balance. Any older summary saying all
  collision-free S6 merges were neutral is superseded by the sections below.
- The registry counts above predate the newest theorem-only modules. Routine
  registry/CLI refresh is intentionally queued for Gemini rather than charged
  to the high-reasoning pass.
- Root `index.js` no longer exists; the active UI script is
  `site/progress.js`, and `node --check site/progress.js` passes.

## Latest Mathematical Results

### Orientation Fourier Reduction

Files:

- `self_dual_wreath_orientation_fourier_reduction.py`
- `research/representation/self_dual_wreath_orientation_fourier_reduction.json`
- `tests/test_self_dual_wreath_orientation_fourier_reduction.py`

For unequal labels `(lambda_i,mu_i)`, the compressed overlap is

`K_i(s) = [rho_lambda_i(s) tensor I + I tensor rho_mu_i(s)] / 2`.

The collision-free orbit-Gram Fourier block in target irrep `nu` is exactly

`F_nu = 2^-k sum_epsilon E_(nu,epsilon)`,

where every `E_(nu,epsilon)` is an invariant-subspace projector. All 15
collision-free `W_4` controls pass with maximum spectrum residual below
`4.5e-16`.

The cheap support-sparsity proof route is falsified. Every tested portfolio
from `n=6` through `n=12` has full orientation support. At `n=12,k=29`, every
target supports all `2^29` orientations, with full support reached after the
third label.

### Orientation Fusion-Frame Second Moment

Files:

- `self_dual_wreath_orientation_fusion_moment.py`
- `research/representation/self_dual_wreath_orientation_fusion_moment.json`
- `tests/test_self_dual_wreath_orientation_fusion_moment.py`

For orientation projectors `E_a,E_b`, pair overlap has the exact
representation-ring formula

`Tr(E_a E_b) = d_companion sum_tau m_A(tau)m_B(tau)m_D(tau)/d_tau`.

It passes 48 active pair-overlap controls and 300 rank controls over all 15
collision-free `W_4` tuples. The maximum nontrivial canonical correlation is
`0.5`; two finite pairs have nonzero common range.

The complete orientation-averaged second moment is evaluated without
enumerating `4^k` pairs by reconstructing symmetric-group class-product
constants for the cycle types of `s`, `t`, and `st`. Through `n=12,k=29`, the
largest collision lower bound is only `1.060406...` times the target
`2^(1-k)` scale, and maximum effective-rank log2 is `639.9058`. No
second-moment superquartic obstruction appears.

This is nonobstructing structural evidence, not a norm theorem:
`Tr(F^2)/Tr(F)` is a lower bound on `lambda_max(F)` and cannot exclude a thin
high-eigenvalue sector.

### Orientation Common-Range Theorem

Files:

- `self_dual_wreath_orientation_common_range.py`
- `tests/test_self_dual_wreath_orientation_common_range.py`

For two orientations, split the representation into the shared tensor
`R_0`, factors selected only by each orientation `R_a,R_b`, and companion
space `H_c`. The commutator of the two diagonal actions acts only on `R_0`.
Because `[S_n,S_n]=A_n`, the exact intersection formula is

`dim(Ran E_a intersect Ran E_b) = dim(H_c) sum_delta m_0(delta)m_a(delta)m_b(delta)`

for `delta` equal to the trivial or sign representation. The formula passes
all 750 `W_4` matrix controls with zero residual.

An exact Kronecker-support dynamic program counts all `4^k` ordered pairs
without enumeration. Pairwise common ranges proliferate rather than vanish:
at `n=10,k=21` every target exceeds 99.8% common-range incidence; at
`n=12,k=29` the minimum and maximum over all 77 targets are
`0.9999977811` and `0.9999986789`. Pairwise transversality is therefore
falsified. This does not prove a large norm because different pairs can share
different directions.

### Fixed-Family Common-Range Depth

Files:

- `self_dual_wreath_orientation_triple_range.py`
- `research/representation/self_dual_wreath_orientation_triple_range.json`
- `tests/test_self_dual_wreath_orientation_triple_range.py`

For any fixed family of orientations and `n>=5`, group factors by the subset
of orientations selecting them. Simplicity of `A_n` makes its actions
independent on distinct membership patterns. Each pattern tensor must occupy
a trivial/sign sector, and the sign choices solve a linear parity system over
`F_2`. This gives an exact fixed-family intersection multiplicity formula.
It passes all 140 `S_5` matrix controls with zero residual.

The naive exact seven-support dynamic program is not scalable: 18,784 states
at `n=6`, 508,186 at `n=7`, and a 600,000-state cap before completing `n=8`.
Deterministic uniform sampling with exact per-family multiplicity tests shows
a sharp incidence-depth transition at `n=12,k=29`:

- three-way incidence: at least 93.1% estimated on every declared target;
- four-way incidence: at most 5.1% estimated;
- five- and six-way incidence: zero successes in 2,048 samples per target,
  with Wilson upper bounds recorded in the artifact.

Thus exact common cores are dispersed by family size five. This does not
control near-common directions or the frame norm.

### Exact Pair Principal-Angle Spectrum

Files:

- `self_dual_wreath_orientation_pair_angle_spectrum.py`
- `research/representation/self_dual_wreath_orientation_pair_angle_spectrum.json`
- `tests/test_self_dual_wreath_orientation_pair_angle_spectrum.py`

Decompose the shared, left-only, and right-only pair tensor products into
`S_n` irreps. Every nonzero principal correlation between two orientation
ranges is exactly `1/d_alpha`, with multiplicity

`dim(H_c) d_alpha m_0(alpha)m_a(alpha)m_b(alpha)`.

The `d_alpha=1` terms are exactly the trivial/sign common ranges. For `n>=5`,
all non-common correlations are at most `1/(n-1)`. The complete spectrum
formula passes 56 active finite controls: all collision-free `W_4` tuples and
three `W_5` controls, with maximum residual below `4.5e-16`. The observed
largest non-common correlations are `1/2` at `n=4` and `1/4` at `n=5`.

This proves dimension-driven pair contraction off the common ranges. The
remaining problem is the Gram operator carried by the trivial/sign incidence
channels across many orientations.

### Structured Block Common Cores

Files:

- `self_dual_wreath_orientation_block_common_core.py`
- `research/representation/self_dual_wreath_orientation_block_common_core.json`
- `tests/test_self_dual_wreath_orientation_block_common_core.py`

Partition the source labels into blocks whose left and right tensor products
contain the same one-dimensional character. Replicate one orientation bit
across every label in a block. For `r` parity-compatible blocks, all `2^r`
resulting orientation projectors have an exact common vector, so

`||sum_e E_e|| >= 2^r` and `||F_nu|| >= 2^(r-k)`.

The exact deterministic portfolio search finds witnesses for all six rows
`n=7,...,12`. At `n=12,k=29`, nine blocks give a family of 512 projectors,
projector-sum norm at least 512, averaged Fourier norm at least `2^-20`, and a
factor 256 violation of the bare `2^(1-k)` target. The common-core dimension
lower bound has log2 `107.7938`. These finite portfolios by themselves do not
establish natural asymptotic mass.

### Typical Plancherel Block Obstruction

Files:

- `self_dual_wreath_plancherel_block_obstruction.py`
- `research/representation/self_dual_wreath_plancherel_block_obstruction.json`
- `tests/test_self_dual_wreath_plancherel_block_obstruction.py`

Primary literature dependency:

- Mark Sellke, *Covering Irrep(S_n) With Tensor Products and Powers*, Theorem
  1.2, `https://arxiv.org/abs/2004.05283`.

Sellke proves that a fixed absolute number `C` of arbitrarily coupled
Plancherel irreps tensor together to cover every `S_n` irrep with probability
`1-o(1)`. Divide the natural `k=ceil(log2(n!))` labels into `C`-sized blocks.
Both the left and right block products cover every irrep except on an
`o(1)` fraction of blocks with high probability. This density statement needs
no convergence rate: Markov applied to the expected bad-block fraction is
enough.

Freeze bad blocks and the bounded leftover. Select a target constituent of
their chosen residual tensor; self-duality of `S_n` irreps makes the target
times residual contain the trivial irrep. Every good block uses its trivial
left/right sectors. The exact fixed-family theorem then yields

`r=(1-o(1))k/C` independent block bits and `2^r` projectors with a common
vector. Intersecting this event with the existing global-distinctness event
shows, for typical natural globally collision-free tuples,

`max_nu ||F_nu|| >= 2^(r-k)`.

Therefore every proposed uniform `poly(n)2^-k` upper bound is asymptotically
false: the ratio is `2^r/poly(n)=2^Omega(k)/poly(n)`. This closes the uniform
orientation-frame norm route as a negative result. It does **not** rule out
whitening, quotienting the common channels, non-projector measurements,
fixed-target behavior, efficient decoders, or quantum advantage. Seven
focused tests pass, all six proof steps are gated true, and three unresolved
scope objections are preserved in the artifact's adversarial audit.

### Spectrally Trimmed Constant-Success Sub-POVM

Files:

- `self_dual_wreath_spectral_trimmed_subpovm.py`
- `research/representation/self_dual_wreath_spectral_trimmed_subpovm.json`
- `tests/test_self_dual_wreath_spectral_trimmed_subpovm.py`

For any `M` equal-rank-`r` projectors, put `B=M^-1 sum_s P_s` and
`mu=Tr(B^2)/r`. For fixed `c>1`, let `R=1[B<=c mu]` and define

`E_s=R P_s R/(M c mu)`.

These effects form a valid sub-POVM. The second-moment Markov bound retains
average projector trace fraction at least `1-1/c`. Rank Cauchy plus Jensen,
without any covariance assumption, proves average exact-label success

`p_correct >= (1-1/c)^2/(M c mu)`.

For the wreath bridge ensemble,

`mu=(2^k+M-1)/(M 2^k)`.

At `M=n!`, `k=ceil(log2 M)`, and `c=2`, `M mu<=2`, hence
`p_correct>=1/16` for every `n`. Three finite covariant-projector controls
pass exactly; one control removes two genuine high-frame eigenvectors. This
proves that the common-core norm spike is not an information-theoretic no-go.
It does not implement the sharp cutoff or the `n!` outcomes.

### Generic Spectral-Filter Degree Obstruction

Files:

- `self_dual_wreath_spectral_filter_degree_obstruction.py`
- `research/representation/self_dual_wreath_spectral_filter_degree_obstruction.json`
- `tests/test_self_dual_wreath_spectral_filter_degree_obstruction.py`

The clipping threshold is `tau=Theta(1/n!)`. A bounded polynomial uniformly
approximating the low-pass must change by a constant between `tau` and
`2tau`. The original Markov estimate was valid but loose. Because QSVT
polynomials are bounded on `[-1,1]` and the transition lies near the interior
point zero, Bernstein's inequality forces degree `Omega(n!)` on eigenvalue
access. Singular-value access widens the transition to
`Theta(1/sqrt(n!))` but still needs degree `Omega(sqrt(n!))`.

This closes generic polynomial/QSVT filtering of the normalization-one frame
encoding. It is not an all-circuit lower bound: a spectral gap, better-scaled
encoding, exact representation transform, or intrinsic quotient remains a
valid bypass target. Scaling is stored in log space to avoid factorial
underflow.

### Black-Box Spectral-Trim Query Lower Bound

Files:

- `self_dual_wreath_spectral_filter_query_lower_bound.py`
- `research/representation/self_dual_wreath_spectral_filter_query_lower_bound.json`
- `tests/test_self_dual_wreath_spectral_filter_query_lower_bound.py`

For search bits `x_j`, the equal-rank projectors `P_j=|x_j><x_j|` have
average `diag(1-|x|/M,|x|/M)` and reflections
`2P_j-I=(-1)^x_j Z`. A generic low-pass that separates zero from a fixed
positive multiple of `1/M` therefore solves promised unstructured search.
BBBV gives `Omega(sqrt(M))` controlled-projector queries, hence
`Omega(sqrt(n!))` at `M=n!`. This closes every generic indexed-projector or
PREPARE/SELECT implementation. It does not cover extra symmetric-group
structure.

### Exact Plancherel Tensor Stationarity

Files:

- `self_dual_wreath_plancherel_block_mass.py`
- `research/representation/self_dual_wreath_plancherel_block_mass.json`
- `tests/test_self_dual_wreath_plancherel_block_mass.py`

For any fixed block size `C>=1` of iid Plancherel irreps and target `nu`,

`E[m_nu/product_i d_lambda_i]=d_nu/n!`,

so the expected normalized `nu`-isotypic mass is exactly `d_nu^2/n!`, the
Plancherel probability of `nu`. This follows because
`E[chi_lambda(g)/d_lambda]` is the regular character divided by `n!`.

Trivial and sign block sectors therefore each have expected normalized mass
`1/n!`, independent of `C`; independent left/right matched one-dimensional
mass is `2/(n!)^2`. Markov gives an `n^a/n!` typical upper bound with failure
`n^-a`. All 540 exact class-sum controls through `n=10` and block sizes
`1,2,3,8` pass.

This explains the coexistence of Sellke-typical support, a large frame-norm
spike, and successful spectral trimming. It kills direct postselection onto
the common-core sectors. Efficiently rejecting or quotienting those thin
sectors remains open.

### Quotient And Local-Filter No-Go Chain

Files:

- `self_dual_wreath_block_common_core_quotient.py`
- `self_dual_wreath_orientation_covariant_quotient_obstruction.py`
- `self_dual_wreath_branch_controlled_invariant_filter.py`
- `self_dual_wreath_paired_block_filter_bypass.py`
- `self_dual_wreath_local_isotypic_filter_no_go.py`
- matching artifacts under `research/representation/`
- matching focused tests under `tests/`

The algebraic quotient that removes trivial/sign sectors from every left and
right block kills the finite common vector with negligible expected dimension
loss, but its naive branchwise physical lift fails: it commutes with the two
uniform orientation actions and has mixed-orientation commutator norm one.
For non-self-conjugate source labels, all orientation signatures generate
independent `A_n` actions. Schur's lemma makes the branchwise commutant scalar,
so a nontrivial branch-independent projector cannot implement that quotient.

An orientation-controlled physical filter does commute with hidden
conjugation and removes the selected one-dimensional block sectors. It is not
enough. Pair two Sellke-good blocks and retain any common nontrivial irrep
`alpha`; self-duality puts trivial inside `alpha tensor alpha`, recreating one
common orientation bit per pair. At `n=12,k=29`, the exact portfolio retains a
16-projector common family after the local filter.

The paired witness generalizes by Plancherel incidence. For arbitrary retained
sets `S_j` of mass at least `q`, double counting forces one irrep to occur in
at least `qb` blocks. Pairing those blocks leaves `floor(qb/2)` common bits.
Thus every constant-mass block-local isotypic filter is asymptotically
bypassed. Nine focused tests across the local and cluster-local modules pass.

### Quantitative Cluster-Locality Lower Bound

Files:

- `self_dual_wreath_cluster_locality_no_go.py`
- `research/representation/self_dual_wreath_cluster_locality_no_go.json`
- `tests/test_self_dual_wreath_cluster_locality_no_go.py`

Treat disjoint clusters of at most `L_n` Sellke-good base blocks as
superblocks. If each cluster retains common left/right Plancherel support mass
`q_n`, incidence and self-dual pairing leave

`r_n = Omega(q_n k_n/L_n)`

exact common bits. Because `k_n=Theta(n log n)`, the residual norm ratio is
superpolynomial whenever `q_n n/L_n -> infinity`. At constant retained mass,
**every disjoint product isotypic filter acting on `o(n)` source labels per
cluster is ruled out**. A viable high-retention filter must coordinate
`Omega(n)` labels, use overlapping/global structure, leave the isotypic
support-filter model, or change the spectral access model.

This is not a general circuit lower bound. It does not cover overlapping
bounded-depth filters, globally coordinated support decisions, non-isotypic
coherent transforms, or the abstract spectral-trimmed sub-POVM. The report
contains 12 conservative scaling rows, nine finite degree/locality thresholds,
and an explicit unresolved-scope audit.

### Orientation-Character Filter And Circuit Schema

Files:

- `self_dual_wreath_orientation_subspace_filter.py`
- `self_dual_wreath_invariant_projector_circuit.py`
- their artifacts under `research/representation/`
- their focused tests under `tests/`

For a selected orientation subspace `H=F_2^r`, let
`F_H=|H|^-1 sum_h E_h`. Coherently control `E_h`, Fourier transform the
orientation register, and accept a nontrivial character. Character
orthogonality gives the exact effect

`D_H=F_H-F_H^2`.

It is positive, has spectrum at most `1/4`, and annihilates
`intersection_h Ran(E_h)` exactly. This is the first nonlocal filter in the
repository that attacks a selected common core at unit scale rather than
resolving its `|H|/2^k` weight inside the full frame. Seventy-six finite
controls, including all 75 collision-free `W_4` target blocks, validate the
Kraus/Parseval identity.

The internal controlled projector is polynomial. Uniformly prepare
`s in S_n`, apply the target plus orientation-selected source irrep actions,
and unprepare. The top block is exactly
`E_h=(1/n!)sum_s U_h(s)`. Beals' efficient `S_n` QFT implements each irrep
action by conjugating reversible left multiplication. Two complete QFT
intertwining controls and 20 physical projected-block controls pass. No
factorial amplitude amplification or factorial precision is needed *once the
orbit-Gram carrier is available*.

### Physical-Access Obstruction For The Dual Filter

Files:

- `self_dual_wreath_orientation_filter_physical_access.py`
- `research/representation/self_dual_wreath_orientation_filter_physical_access.json`
- `tests/test_self_dual_wreath_orientation_filter_physical_access.py`

This is the required adversarial correction to the preceding positive result.
The orientation Fourier blocks live on the orbit-Gram domain. With synthesis
`T`, physical frame `B=TT^*`, and Gram operator `G=T^*T`, every direct
physical-to-dual filter of the form `D^(1/2)T^*`, `0<=D<=I`, has average
conclusive probability

`Tr(DG^2)/r <= Tr(B^2)/r`.

For the natural wreath ensemble this is `Theta(1/n!)`. Three exact finite
factorization controls pass; at `n=512` the direct-access success upper bound
has log2 `-3874.52`, and generic amplification costs log2 `1937.26`.

Therefore the dual circuit alone is **not** a physical algorithm: reaching
that domain through the obvious synthesis adjoint restores the factorial
barrier. The next subsection records the direct physical branch-interference
circuit that bypasses this specific factorization.

### Direct Physical Orientation Interference

Files:

- `self_dual_wreath_physical_orientation_interference.py`
- `research/representation/self_dual_wreath_physical_orientation_interference.json`
- `tests/test_self_dual_wreath_physical_orientation_interference.py`

The second escape in the preceding paragraph is now constructed. An unequal
wreath irrep has a physical induced-branch qubit. Known rectangular flips
align the two summands, exposing an `F_2^k` orientation register. For a chosen
subspace `H`, the circuit:

1. coherently resolves the diagonal `S_n` isotypic label;
2. applies a reversible binary basis change into `H` plus quotient bits;
3. Hadamard-transforms the `H` bits;
4. accepts a nontrivial `H` character.

This acts directly on the physical carrier and never invokes `T^*`. For every
target `nu`, it obeys the exact trace-transfer identity

`Tr(K_nu,H B K_nu,H^*) = d_nu |H|/2^k sum_q Tr(F_nu,q-F_nu,q^2)`.

Uniform random conjugation makes acceptance independent of the hidden
permutation. All 30 complete collision-free `W_4` controls, using both the
full orientation space and the diagonal block direction, pass. Retained trace
ranges from `0.4444` to `0.75`; covariance spread is below `2.3e-16`, and the
trace-transfer residual is below `2.3e-15`.

The earlier physical-access no-go remains correct **only** for filters that
factor through the direct synthesis adjoint. This direct branch circuit is an
explicit bypass, not a contradiction.

### Natural Information Retention Theorem

Files:

- `self_dual_wreath_orientation_retention_theorem.py`
- `research/representation/self_dual_wreath_orientation_retention_theorem.json`
- `tests/test_self_dual_wreath_orientation_retention_theorem.py`

For source pairs `(lambda_i,mu_i)`, the rejected fraction is exactly

`L_H=|H|^-1 sum_(u in H) (1/n!) sum_s product_(i:u_i=1) r_lambda_i(s)r_mu_i(s^-1)`.

Plancherel normalized-character orthogonality gives

`E[L_H]=1/|H|+(1-1/|H|)/n!`.

For `dim H=Omega(k)` at `k=ceil(log2(n!))`, Markov makes `L_H` smaller than
every fixed inverse polynomial with probability `1-o(1)`. Intersecting with
the existing all-distinct source event transfers this to the natural
collision-free unequal sector. Covariantization equalizes acceptance over
hidden labels, and a coherent implementation plus the gentle measurement
lemma preserves identification success up to `sqrt(L_H)`. Therefore the
existing information-theoretic `1/16` success remains constant after the
physical filter on typical natural tuples.

Thirty exact physical/character controls and eight exact Plancherel controls
through `n=10` pass. At `n=512`, expected rejection has log2 `-484` and the
Markov failure bound for rejection above `n^-10` has log2 `-394`.

This is the strongest positive result in the current pass. It proves a
polynomial direct filter and natural information retention. It does **not**
prove a polynomial postfilter frame norm, an efficient final POVM, a hidden
permutation decoder, or a classical separation.

### Exact Postfilter Frame Compression And Finite No-Gain Result

Files:

- `self_dual_wreath_postfilter_frame_compression.py`
- `research/representation/self_dual_wreath_postfilter_frame_compression.json`
- `tests/test_self_dual_wreath_postfilter_frame_compression.py`

Let `B` be the hidden-label average frame and let the direct filter Kraus
operators be `K_nu=Z_H U_H Pi_nu`. Because `B` commutes with every diagonal
`S_n` isotypic projector, **discarding** the isotypic label gives

`sum_nu K_nu B K_nu^* = Z_H U_H B U_H^* Z_H`.

This is an exact theorem, not a finite ansatz. But the intended circuit says
to retain the label coherently. Its average frame is instead

`direct_sum_nu Z_H U_H Pi_nu B Pi_nu U_H^* Z_H`.

Cross-label average blocks vanish, and the tagged norm is the maximum sector
norm. It can be strictly smaller than the discarded-label principal
compression. This distinction is essential because later decoding may
interfere the coherent label with the carrier.

If `q=rank(I-Z_H)`, Cauchy interlacing gives

`||Z_H U_H B U_H^* Z_H|| >= lambda_(q+1)(B)`.

For `dim(H)=r`, `q/D=2^-r`: a near-unit-retention filter can remove only that
fraction of spectral directions. The raw top norm is preserved exactly iff
the pulled-back accepted subspace `Ran(U_H^*Z_H)` intersects the top
eigenspace of `B`.

Thirty dense complete `W_4` controls verify both output-channel identities,
commutation, equality criterion, and interlacing. Matrix-free Lanczos covers
all 21 current collision-free `W_5` portfolios for the discarded-label
channel. Raw discarded-label top norm is preserved in 45 of 51 controls and
reduced in six. After normalization, none of those 51 improves.

The corrected coherent-tagged result is less negative. At `W_4`, 2 of 30
controls strictly improve conditioned norm, six more are unchanged, and 22
worsen. Complete matrix-free tagged-sector Lanczos over all 21 `W_5`
portfolios finds nine improvements and 12 regressions. The best `W_5` ratio is
`0.8592911`; the worst is `1.1627907`. Across both sizes, 11 of 51 improve.
This is a mixed finite signal, not an asymptotic sector theorem.

This kills the interpretation that discarding the isotypic label can help and
shows that common-core rejection alone is not uniformly useful. It does not
kill coherent tagging: the two finite gains are a real but sparse signal. The
decisive missing theorem is now sectorwise and quantitative: bound the maximum
tagged-sector norm on typical natural tuples while preserving cross-sector
coherence for the decoder.

### Logarithmic Orientation Rank-Retention Regime

Files:

- `self_dual_wreath_orientation_rank_budget.py`
- `research/representation/self_dual_wreath_orientation_rank_budget.json`
- `tests/test_self_dual_wreath_orientation_rank_budget.py`

For physical dimension `D=2^k C`, the exact trace identity is
`Tr(B)/D=2^-k`. Therefore, for every `A>=1`,

`rank(1[B>A 2^-k]) < D/A`.

An orientation subspace of dimension `r` rejects exactly `D/2^r` Hilbert
dimensions. Setting `A=2^r` matches the filter's rejection rank to the entire
high-spectrum count permitted by trace. This is a capacity theorem, not an
alignment theorem.

The correct calibrated regime is now

`r=ceil(a log2 n)`, `A=2^r in [n^a,2n^a)`.

For a retention threshold `n^-b`, `0<b<a`, the exact Plancherel expectation
and Markov give failure `O(n^(b-a))`; gentle information loss is
`O(n^-b/2)`. Thus logarithmic `r` gives all three necessary resources at once:

- a polynomial cutoff `A 2^-k`;
- enough rejection rank to cover the universal trace-allowed tail;
- acceptance `1-o(1)` and vanishing loss of the known constant information.

This replaces `r=Omega(k)` as the default design. Linear `r` proves far more
retention than necessary but rejects exponentially fewer Hilbert dimensions
than trace alone can justify. At `n=512`, the calibrated example uses `r=72`
instead of the old illustrative `r≈484`; its Markov failure bound is below
`2^-36` at rejection threshold `n^-4`.

The decisive missing result is **structured alignment**: prove that a selected
`Theta(log n)` subset of the available source-adapted block directions spans
the actual high-spectrum subspace, not merely the already-known common vector.

### Isotypic Dephasing Identification No-Go

Files:

- `self_dual_wreath_isotypic_dephasing_no_go.py`
- `research/representation/self_dual_wreath_isotypic_dephasing_no_go.json`
- `tests/test_self_dual_wreath_isotypic_dephasing_no_go.py`

For a uniform covariant ensemble under
`R(g)=direct_sum_nu rho_nu(g) tensor I_(M_nu)`, dephasing the irrep label makes
every state block diagonal. Covariant POVM symmetrization and Schur averaging
force the seed effect in sector `nu` to satisfy

`Tr_(V_nu)(E_nu)=d_nu/|G| I_(M_nu)`.

The positive-operator inequality

`X <= d I_d tensor Tr_(C^d)(X)`

then gives the exact decoder bound

`p_success <= sum_nu p_nu d_nu^2/|G| <= max_nu d_nu^2/|G|`.

For `G=S_n`, this is the largest Plancherel atom. Aggarwal--Elboim's maximal
dimension theorem makes it `exp(-(2d+o(1))sqrt(n))`, `d>0`. Data processing
extends the bound through every later filter, unitary, ancilla, and decoder.
Multiplicity spaces do not evade it.

Therefore **any architecture that classically samples `nu` or runs independent
sector decoders is asymptotically dead for constant-success exact hidden-
permutation recovery**. The isotypic transform must remain coherent, and the
final decoder must exploit cross-`nu` coherences. The average tagged frame is
block diagonal, but individual hidden states retain cross-sector terms in the
label/carrier system; those terms are now a proved necessary resource.

The theorem does not rule out coherent cross-sector decoding or a coarser
trivial-vs-nontrivial decision problem.

### Coherent Fourier Decoder Criterion

Files:

- `self_dual_wreath_coherent_fourier_decoder.py`
- `research/representation/self_dual_wreath_coherent_fourier_decoder.json`
- `tests/test_self_dual_wreath_coherent_fourier_decoder.py`

The surviving decoder architecture is now an exact mathematical target. For
any finite group,

`|F_g> = direct_sum_nu sqrt(d_nu/|G|) vec(rho_nu(g))`

is the nonabelian Fourier image of `|g>`. Consider a coherent covariant state

`|psi_g> = direct_sum_nu sqrt(p_nu) (rho_nu(g) tensor I)|phi_nu>`.

If the row/multiplicity Schmidt probabilities in sector `nu` are
`lambda_nu,i`, define

`f_nu=d_nu^-1/2 sum_i sqrt(lambda_nu,i)`.

The exact correct-label probability after inverse group QFT is

`P=[sum_nu d_nu sqrt(p_nu/|G|) f_nu]^2`.

Therefore perfect decoding occurs when:

- `p_nu=d_nu^2/|G|` coherently (Plancherel amplitudes);
- every sector exposes an aligned dual row/column register with a flat Schmidt
  spectrum (`f_nu=1`).

Four exact `S_3`/`S_4` Young-matrix controls verify Fourier unitarity and the
success formula for ideal, weight-mismatched, Schmidt-mismatched, and rank-one
states. The ideal control decodes with probability one.

For `S_n`, Beals makes the final inverse QFT polynomial. This removes “there
are `n!` outcomes” as the conceptual decoder bottleneck: a permutation is only
`O(n log n)` bits and Fourier synthesis outputs it directly. The hard core is
now **coherent carrier normalization**:

1. extract an aligned dual row register from the physical multiplicity carrier;
2. flatten its sector Schmidt spectrum;
3. reweight coherent sector amplitudes to Plancherel;
4. preserve cross-sector phase throughout;
5. apply inverse `S_n` QFT.

No physical extraction, flattening, or polynomial reweighting theorem exists
yet, so this is a research architecture, not an algorithm claim.

### Constant-Success PGM And Quantum-Sampling Normal Form

Files:

- `self_dual_wreath_pgm_success_theorem.py`
- `self_dual_wreath_covariant_pgm_factorization.py`
- `self_dual_wreath_pgm_truncation_robustness.py`
- `self_dual_wreath_pgm_spectral_window.py`
- `self_dual_wreath_pgm_quantum_sampling_reduction.py`

The full covariant projector ensemble has all-n PGM success

`p_PGM >= 1/[1+(n!-1)2^-k]`.

At `k=ceil(log2 n!)` this is constant. Covariance removes the explicit
`sqrt(n!)` Petz environment charge and reduces the PGM to controlled carrier
polars. In an isotypic sector,

`A_nu|m> = sum_j |j> tensor P|nu,j,m>`, `A_nu^*A_nu=D_nu`,

so the required carrier isometry is `A_nu D_nu^-1/2`. The orientation factor
has the equivalent nonorthogonal quantum-sampling form

`R_nu|x> = sum_epsilon |epsilon> E_(nu,epsilon)|x>`.

Truncation removes dependence on the actual minimum eigenvalue, and a fixed
condition-number window of `n! B` retains constant PGM success. Neither result
makes generic QSVT polynomial: raw access still sees a `Theta(1/n!)` scale.
The surviving route must implement the structured polar of `R_nu`, not a
black-box inverse.

### Hierarchical Orientation Polar Chain

Files:

- `self_dual_wreath_pair_polar_sampler.py`
- `self_dual_wreath_hierarchical_polar_tree.py`
- `self_dual_wreath_relative_effect_intersection.py`
- `self_dual_wreath_common_core_polar_bypass.py`
- `self_dual_wreath_early_level_overlap_localization.py`

For a subtree `T=L union R`, put `S_T=sum_(epsilon in T)E_epsilon`. The exact
chain rule is

`Q_T=(Q_L direct_sum Q_R)[S_L^1/2;S_R^1/2]S_T^-1/2`.

The left relative effect is

`C=S_T^-1/2 S_L S_T^-1/2`.

The pair level is polynomial: every noncommon principal correlation is at most
`1/(n-1)`, so the two-projector polar has constant condition. The number of
strictly fractional eigenvalues of `C` is exactly

`dim(range(S_L) intersect range(S_R))`.

This localizes every weighted conditional channel to a child-span
intersection. Exponential block-common cores are not an obstruction to an
aligned tree: each balanced split acts as exactly `C=I/2` on the core. This
explicitly supersedes the old interpretation that recurring-irrep incidence
closed every overlapping transform. Off exact common ranges, child spans are
provably disjoint through `O(log n)` early levels; the theorem does not reach
the full `Theta(n log n)` depth.

### Physical PGM Transfer Is Compiled

Files:

- `self_dual_wreath_polar_factor_transfer.py`
- `self_dual_wreath_physical_pgm_intertwiner.py`
- `tests/test_self_dual_wreath_physical_pgm_intertwiner.py`

Equal Gram factors do not generically expose their output intertwiner. The
wreath factor has additional covariant structure that closes this gate. After
the explicit induced-branch alignment, generalized coherent `S_n` Fourier
sampling gives the row-copy isometry

`C_U|nu,a,m> = d_nu^-1/2 sum_b |nu,a,b>|nu,b,m>`.

Its branch-`epsilon` residual lies exactly in
`range(E_(nu,epsilon))`, and for every coherent Fourier row

`A_(nu,a)=2^(-k/2) R_nu^* C_(U,nu,a)`.

Therefore the physical PGM coisometry is exactly

`(A A^*)^-1/2 A = Q_R^* C_(U,nu,a)`.

This uses a uniform permutation register, controlled diagonal restriction
action, and the Beals `S_n` QFT. It does not compute a Kronecker multiplicity
basis, use the factorially weak synthesis adjoint, or dephase `nu`. Three
physical W3/W4 controls pass. **The physical-output transfer gate is closed.**
The all-n orientation polar `Q_R` is now the sole PGM implementation gate.

### Level-Three Linear-Flag Audit

Files:

- `self_dual_wreath_level_three_flag_audit.py`
- `research/representation/self_dual_wreath_level_three_flag_audit.json`
- `tests/test_self_dual_wreath_level_three_flag_audit.py`

Every ordered basis of `F_2^3` was enumerated: 168 linear flags and seven
merges per flag. Across selected collision-free W5 sectors and the
pairwise-distinct W3 triangle control, every fractional relative eigenvalue is
exactly `1/2`. The current artifact contains 4,704 merge occurrences and 2,520
fractional eigenvalue occurrences.

This is structural, not generic. A fully repeated unequal label produces 648
nonhalf occurrences with exact values including `1/3`, `4/9`, `5/9`, and
`2/3`. Any all-n theorem must use collision-free or stronger label structure.

The old carrier-core explanation for this pattern is now falsified and must
not be used as the all-n conjecture. The replacement results follow.

### Affine Carrier Cores Are Sufficient But Not Necessary

Files:

- `self_dual_wreath_affine_core_flag_theorem.py`
- `research/representation/self_dual_wreath_affine_core_flag_theorem.json`
- `tests/test_self_dual_wreath_affine_core_flag_theorem.py`

An affine leaf-incidence core is routed by every linear flag with weights only
`0,1/2,1`; a nonaffine three-point core gives `1/3` and `2/3`. This theorem is
exact. However, actual label-distinct W3 overlaps are pairwise-emergent and do
not reduce the leaves, while remaining exactly half-balanced. Selected W5
overlaps also fail leaf reduction. Therefore **exhaustion by reducing affine
carrier cores is not the governing mechanism**.

### Exact Shorted-Overlap Balance Criterion

Files:

- `self_dual_wreath_shorted_overlap_balance.py`
- `research/representation/self_dual_wreath_shorted_overlap_balance.json`
- `tests/test_self_dual_wreath_shorted_overlap_balance.py`

For `A,B>=0`, `K=range(A) intersect range(B)`, and isometry `U` onto `K`, set

`G_A=U^*A^+U`, `G_B=U^*B^+U`.

The fractional spectrum of `(A+B)^-1/2 A (A+B)^-1/2` is exactly the
generalized spectrum of `(G_B,G_A+G_B)`. Hence every fractional channel is
`1/2` iff `G_A=G_B`, equivalently iff the shorted operators of `A` and `B` to
`K` agree. This is now the exact all-n target. It predicts every repeated-
label nonhalf value and has zero finite validation failures.

### Canonical Coefficient-Space Affine Normal Form

Files:

- `self_dual_wreath_canonical_coefficient_affine.py`
- `research/representation/self_dual_wreath_canonical_coefficient_affine.json`
- `tests/test_self_dual_wreath_canonical_coefficient_affine.py`

For child frame `A=sum_e E_e`, the minimum-norm leaf maps
`D_e=E_e A^+U` obey `sum_e D_e=U` and
`sum_e D_e^*D_e=G_A`. All 20 label-simple fractional merges tested have
`G_A=G_B=gI`, scalar equal component effects, and affine active mask support.
W3 uses the affine plane `{0,2,5,7}`; W5 uses the affine line `{3,6}`.
Repeated labels fail ten certificates. The affine structure therefore lives
in the canonical coefficient register, not in reducing carrier cores.

The maps still contain `A^+`. They are a structural normal form, not a
circuit.

### Isolated Single-Anchor Shorting

Files:

- `self_dual_wreath_single_anchor_shorting.py`
- `research/representation/self_dual_wreath_single_anchor_shorting.json`
- `tests/test_self_dual_wreath_single_anchor_shorting.py`

If `K` lies in anchor leaf `E_a` and is orthogonal to
`range(E_a) intersect span(other child leaves)`, minimum-energy synthesis uses
only the anchor and the shorted child operator is exactly `P_K`. A duplicate-
core leaf falsifies the premise and changes the metric. All 11 selected W5
fractional merges are explained exactly by the unique anchor pair `{3,6}` and
a five-dimensional core. No all-n isolated-anchor decomposition is proved.

### Flat Affine Recoupling Bundle

Files:

- `self_dual_wreath_affine_recoupling_bundle.py`
- `research/representation/self_dual_wreath_affine_recoupling_bundle.json`
- `tests/test_self_dual_wreath_affine_recoupling_bundle.py`

Uniform scalar coefficient maps define isometric fibers `V_e`; their
transports `T_(f,e)=V_fV_e^*` are exact flat partial isometries. An affine
support can therefore be prepared by affine Hadamards plus controlled
generator transports if those transports have explicit circuits. W5's line
transport is identity. W3's plane transports are nontrivial, with generator
fiber-map difference as large as `sqrt(3)`. A repeated-label balanced control
has equal child metrics but nonscalar fibers on a nonaffine six-mask support.

### Pair-Polar Transport Network And Degree Gate

Files:

- `self_dual_wreath_pair_polar_transport_network.py`
- `self_dual_wreath_pair_transport_degree_obstruction.py`
- `research/representation/self_dual_wreath_pair_polar_transport_network.json`
- `research/representation/self_dual_wreath_pair_transport_degree_obstruction.json`
- corresponding tests under `tests/`

Every finite W3 fiber transport is a path of at most two leaf-pair polar maps;
the overlap graph is `K_(2,2)` and endpoint gauges are `+I` or `-I`. W5 uses
one direct common-range edge. This is a finite compilation, not an asymptotic
one.

For carrier `alpha`, pair correlation is `c=1/d_alpha`. Any bounded QSVT
polynomial implementing the polar sign on the normalized cross-overlap needs
degree at least

`(1-epsilon)sqrt(1-c^2)/c = Omega(d_alpha)`.

This does not contradict the constant-conditioned stacked pair sampler based
on `E+F`; the two access problems are different. It also does not rule out an
explicit Racah transform outside the cross-overlap QSVT model.

### Transport Carrier-Mass Falsifier

Files:

- `self_dual_wreath_transport_carrier_mass.py`
- `research/representation/self_dual_wreath_transport_carrier_mass.json`
- `tests/test_self_dual_wreath_transport_carrier_mass.py`

Exact representation-ring probes on deterministic natural high-dimension
portfolios show that low-dimensional pair carriers are not typical by
multiplicity. At `n=12,k=29`, sampled intermediate distances have weighted
median carrier dimension `5775`; at most `5.9e-8` of pair-overlap multiplicity
lies in dimensions at most `n^2`, and RMS correlation is at most `2.1e-4`.
This falsifies a generic typical-mass argument for cheap transports. It is not
an algorithm lower bound because the candidate affine fiber may align with an
exceptional low-dimensional sector.

Literature scope warning:

- Moore, Russell, and Sniady, *On the Impossibility of a Quantum Sieve
  Algorithm for Graph Isomorphism*, `https://arxiv.org/abs/quant-ph/0612089`.

Their lower bound rules out Kuperberg-style adaptive tensor-product sieves on
the wreath-product GI reduction in less than `exp(Omega(sqrt(n)))` time. Do
not mutate this filter into a pairwise/small-register Clebsch-Gordan sieve.
The current circuit is outside that stated model only because it performs a
single globally entangled `Theta(n log n)`-register isotypic measurement and
orientation transform. Any claim that it lies outside the theorem must be
checked against the paper's formal algorithm class, not inferred from naming.

## Superseding Dependency And Recoupling Results

The following results replace the earlier conjecture that every
collision-free affine merge is exactly half-balanced.

### Cross-Dependency Normal Form And Cayley Boundary

Files:

- `self_dual_wreath_cross_dependency_neutrality.py`
- `self_dual_wreath_cayley_fiber_reduction.py`
- `self_dual_wreath_matrix_cayley_boundary.py`
- matching artifacts and tests under `research/representation/` and `tests/`

For child syntheses `R_L,R_R`, the canonical cross-dependency space is

`W=ker[R_L,-R_R] intersect (ker R_L direct_sum ker R_R)^perp`.

If `J=diag(I,-I)`, every fractional relative eigenvalue is
`lambda=(1-delta)/2` for `delta in spec(P_W J P_W|_W)`. Exact half-balance is
therefore equivalent to total grading neutrality of `W`.

Scalar XOR-Cayley fibers Fourier-reduce to `[[c,d],[d,c]] tensor I` and are
half-balanced. Matrix-valued Cayley kernels are balanced exactly when their
opposite saturation spaces are orthogonal. A two-dimensional positive
counterfamily gives channels `(1 +/- 1/sqrt(2))/2`; XOR covariance alone is
not a proof.

### Sparse Invariant Dependencies And Weighted Exclusion

Files:

- `self_dual_wreath_sparse_invariant_dependency.py`
- `self_dual_wreath_weighted_overlap_exclusion.py`
- matching artifacts and tests

Invariant leaf ranges are extracted from representation multiplicities and
small coefficient Grams, avoiding dense ambient projectors. S6 controls reach
ambient dimension 22,500, multiplicity five, and seven active orientations.

For common-free leaves with weights `w_ij=||U_i^*U_j||`, the exact comparison
bound is

`||P_LP_R|| <= ||W_LR|| / sqrt((1-rho(W_LL))(1-rho(W_RR)))`.

It strictly excludes all 1,920 screened common-free S6 affine merges. W3 is
the sharp norm-one boundary. This does not handle exact pair-common sectors.

### Pair-Common Homology

Files:

- `self_dual_wreath_dependency_homology.py`
- `research/representation/self_dual_wreath_dependency_homology.json`
- `tests/test_self_dual_wreath_dependency_homology.py`

Let `W_pair` be the span in `W` of exact two-leaf common relations and
`H_em=W/W_pair`. W3 has genuine neutral emergent homology. Earlier W5/S6
controls are pair-generated, but this is not a neutrality theorem.

The new globally distinct S6 control
`W6-COLLISION-FREE-NONCOMMUTING-CORE` has a 34-dimensional child intersection,
is entirely pair-generated, and has grading defect `1/17`. Its channels are:

- nine at `8/17`;
- sixteen at `1/2`;
- nine at `89/170`.

This is a full affine-merge counterexample, not merely a reduced pair model.
Universal collision-free half-balance is false.

### Affine Common Supports And Noncommuting Core Counterexample

Files:

- `self_dual_wreath_common_core_atomization.py`
- `research/representation/self_dual_wreath_common_core_atomization.json`
- `tests/test_self_dual_wreath_common_core_atomization.py`

The fixed-family parity formula is now realized by explicit orthonormal
trivial/sign intertwiners. There is also an all-`n>=5` support theorem:

`intersection(U_a,U_b,U_c) subset U_(a xor b xor c)`.

Summing the three parity equations gives the fourth orientation's invariance
equation. Hence every exact common vector has affine orientation support, and
any support crossing affine sibling cosets meets them equally. Unequal support
counts are not the source of the S6 defect.

The actual obstruction is noncommuting recoupling. In the counterexample,
balanced affine line cores have principal correlation `1/9` but nonzero
commutator norm `0.110423...`. A direct relative Cech quotient reproduces the
nonhalf spectrum above. This falsifies both universal pair-core commutativity
and the claim that affine support balance alone implies half-balance.

### Pair-Core Recoupling Boundary

Files:

- `self_dual_wreath_pair_core_recoupling_boundary.py`
- `research/representation/self_dual_wreath_pair_core_recoupling_boundary.json`
- `tests/test_self_dual_wreath_pair_core_recoupling_boundary.py`

Two local scalar recoupling laws are exact. With carrier correlation
`gamma=1/d`, an open two-cross-edge star has channels

`(1-gamma)/(2-gamma)` and `(1+gamma)/(2+gamma)`.

After quotienting an equicorrelated internal edge, the high channel becomes

`(1+gamma-gamma^2)/(2+gamma-gamma^2)`.

Selected S6 controls realize `d=5,9,10` exactly. A deterministic screen of 180
controls and 560 pair-core stars found 393 fractional correlations, all equal
to `1/5`, `1/9`, or `1/10`; none exceed `1/(n-1)`. This is finite evidence,
not an all-n carrier-factorization theorem.

If `gamma<=1/(n-1)` and `n>=5`, every isolated scalar star lies in
`[3/7,5/9]`. Nonhalf local blocks are therefore not automatically hard. A
weighted Schur-comparison theorem certifies all three selected endpoint gaps.
However, a broader 100-control, 6,766-merge audit left 33 cases uncertified by
the sign-blind absolute-weight bound even though the exact maximum defect was
only `1/9`. Cech-cycle cancellations and recoupling phases are essential.

### Relative Common-Core Cech Laplacian

Files:

- `self_dual_wreath_common_core_cech_laplacian.py`
- `research/representation/self_dual_wreath_common_core_cech_laplacian.json`
- `tests/test_self_dual_wreath_common_core_cech_laplacian.py`

The phase-sensitive chain groups are

`C_p = direct_sum_(|F|=p+1) intersection_(e in F) U_e`,

with alternating inclusion boundaries. The pair-relation Gram is
`G_1=D_1^*D_1`, so `G_1D_2=0`; `H_1=ker D_1/im D_2` is the pair-cycle
homology not generated by higher common cores.

Three hard S6 affine planes and one eight-orientation affine cube pass. In the
four-way-core controls, the pair
kernel has dimension three and the four triple cells have boundary rank three;
the quadruple cell gives the one relation among those triples. All positive-
degree homology vanishes. The dense control that defeats the sign-blind bound
has exact pair-Laplacian positive spectrum `[2,4]` after the Cech cycle
quotient. The eight-orientation cube has 12 pair cores, the same exact
three-dimensional higher-cell cycle, positive spectrum `[17/9,4]`, and a real
grading defect `1/17`; its sign-blind comparison bound is infinite. This is a
finite pair-cycle prototype only and does not test the augmented leaf-
dependency quotient.

### Sparse Parity Kernel And Augmented Common-Core Cech

Files:

- `self_dual_wreath_orientation_triple_range.py`
- `self_dual_wreath_common_core_atomization.py`
- `self_dual_wreath_augmented_common_core_cech.py`
- `research/representation/self_dual_wreath_augmented_common_core_cech.json`
- `tests/test_self_dual_wreath_augmented_common_core_cech.py`

The old fixed-family implementation enumerated all `2^(2^m-1)` formal parity
assignments, including empty membership patterns forced into the trivial
isotype. It is now an exact sparse XOR dynamic program over at most `2k+1`
occupied patterns for `k` labels. A separate compact enumeration constructs
only viable occupied-pattern intertwiners. This makes eight-orientation cells
exactly computable without changing the theorem.

The Cech complex is now augmented by leaf synthesis:

`... -> C_2 -> C_1 -> C_0 -> V`,

so `H_0=ker(D_0)/im(D_1)` measures many-leaf dependencies not generated by
pair common cores. This is logically independent of the prior `H_1` pair-cycle
audit. The direct W3 distinct plane has `H_0=2` and no pair cores. The repeated
W3 plane has four raw leaf dependencies, pair-boundary rank three, and
`H_0=1`. These exactly reproduce the independent dependency-homology audit.
They are adversarial controls outside the `n>=5` parity theorem, not an all-n
counterexample.

A selected W5 plane is augmented-exact: raw dependency dimension five and
pair-boundary rank five. A low-ambient (`625`) full depth-three W6 cube has all
simplex cells through degree seven, zero homology in every degree, and Hodge
spectrum bounded between `2` and `8`. It is deliberately labeled factorized:
it tests the sparse all-depth machinery but not noncommuting multicarrier
holonomy. Universal pair generation for natural `n>=5` portfolios remains a
separate theorem gate.

### Recursive Pair Generation And Complete S5 Boundary

Files:

- `self_dual_wreath_recursive_pair_generation.py`
- `research/representation/self_dual_wreath_recursive_pair_generation.json`
- `tests/test_self_dual_wreath_recursive_pair_generation.py`

There is an exact short sequence at every sibling merge. If `W/W_pair` is the
cross-dependency quotient after all internal child syzygies are removed, then

`dim H0(parent) = dim H0(left) + dim H0(right) + dim(W/W_pair)`.

The identity recovers the distinct W3 root `H0=2` and repeated W3 root `H0=1`
entirely in the cross quotient, while the selected globally distinct W5 plane
has zero at every node.

The optimized exact screen covers all 105 perfect-match portfolios formed from
six distinct S5 partitions, all seven targets, all 14 affine planes, and the
full orientation cube: 11,025 affine nodes total. Every node has `H0=0`; raw
dependency dimension reaches eight, and the maximum direct `D0D1` residual is
below `2e-15`. This is the complete globally distinct, three-label S5
boundary, not an all-n theorem. A separate live S6 low-dimensional screen
checked all 15 pairings of the six degree-at-most-five-dimensional source
partitions over all 11 targets (165 controls) with no emergent H0; it is not
yet a dedicated artifact.

### Pair-Core Quotient Overlap Criterion

Files:

- `self_dual_wreath_pair_quotient_overlap.py`
- `research/representation/self_dual_wreath_pair_quotient_overlap.json`
- `tests/test_self_dual_wreath_pair_quotient_overlap.py`

For child spans `A,B`, let `K` be the physical span of all crossing leaf-pair
common cores. Crossing pair relations generate exactly `K` after internal
dependencies are quotiented. Therefore the local emergent quotient vanishes
exactly when

`||P_(A minus K) P_(B minus K)|| < 1`.

This isolates the exact phase-sensitive all-n norm target. W3 reaches one and
recovers emergent dimensions two/one. A pair-rich W5 node has `dim K=5`, no
emergent quotient, and exact residual gap `0.659504...`.

The residual absolute-weight graph is not generally adequate. A screen of 539
affine merges for one complete S5 portfolio found 12 phase-only certificates.
The promoted control has exact residual gap `0.591089...`, but the sign-blind
bound is infinite because one child's internal weight radius reaches one.
Thus even common-free pair generation may require signed/Racah block control;
scalar weighted graphs cannot be the all-depth proof.

The canonical Gram-factor screen for the selected globally distinct S6
portfolio covers nine active targets and 693 affine merges. No emergent cross
quotient appears; the minimum exact residual gap is `0.7375`, the minimum
pair-rich gap is `0.8`, and 12 merges are phase-only. These larger finite gaps
are encouraging but do not imply monotonicity or an asymptotic lower bound.

## Exact Pair-Core Carrier Factorization

Files:

- `self_dual_wreath_pair_core_carrier_factorization.py`
- `research/representation/self_dual_wreath_pair_core_carrier_factorization.json`
- `tests/test_self_dual_wreath_pair_core_carrier_factorization.py`

This closes the former open derivation 1. Grade every tensor factor of a
three-orientation family `{a,b,c}` by its membership pattern and write
`m_P(alpha)` for the isotypic multiplicities of block `T_P`. The blocks split
into cluster one `{T_a,T_ab,T_ac,T_abc}`, cluster two `{T_b,T_c,T_bc}`, and the
spectator `T_empty`. Because both pair cores are one-dimensional isotypes on
their groups, both are graded by every block's isotypic label, so the overlap
operator is block diagonal in that grading and never needs the ambient space.
Inside a block the carriers are forced to one irrep per cluster, and
contracting the four (respectively three) maximally entangled carrier pairs
gives the exact closed form

`B_ab^* B_ac = direct_sum (1/(d_beta d_p)) W`, `W` a partial isometry,

with exact multiplicity

`m_a(b) m_ab(b^d') m_ac(b^d) m_abc(b^{d xor d'}) * d_p m_b(p) m_bc(p^d) m_c(p^{d xor d'}) * dim T_empty`,

where `alpha^0=alpha` and `alpha^1` is the conjugate partition.

Three consequences matter.

1. The conjectured single-reciprocal `1/d_alpha` law is **false in general**.
   The exact value is a two-carrier product. Every earlier finite screen saw
   single reciprocals only because its membership blocks were singletons,
   which forces the second carrier to be one dimensional.
2. There is **no nontrivial multiplicity-space Racah/6j block** for a
   shared-vertex star. Two pairings of four self-dual carriers into invariants
   contract to the scalar `1/d`. Genuine Kronecker content first appears for
   vertex-disjoint pair cores, where a waist bound replaces the scalar law.
3. A correlation equals one exactly when both carriers are one dimensional.
   Two isotype channels can meet in one carrier sector only when both carriers
   are self-conjugate, hence of dimension at least `n-1`, and the collision
   term `4/(n-1)^2` is dominated for `n>=5`. Therefore **every off-common star
   correlation is at most `1/(n-1)` for all `n>=5`**, which upgrades the
   180-control reciprocal screen to a theorem.

Validation: 168 screened controls plus the three named `d=5,9,10` controls
reproduce every dense ambient singular value, rank, and multiplicity with
maximum residual `5.83e-16`. Forty vertex-disjoint controls respect the waist
bound and are exactly tight on all forty. Forty repeated-source-label controls
outside the collision-free sector obey the same closed form, so the theorem
does not depend on global distinctness. Ten focused tests pass.

## Sign-Blind Multistar Route Is Dead At Natural Depth

Files:

- `self_dual_wreath_multistar_degree_obstruction.py`
- `research/representation/self_dual_wreath_multistar_degree_obstruction.json`
- `tests/test_self_dual_wreath_multistar_degree_obstruction.py`

This settles former open derivation 4 in the negative for the technique the
repository was using. Block Gershgorin on the crossing relation Gram needs

`max_e sum_{f adjacent to e} ||G_ef|| < 2`.

The carrier factorization makes every term exact, and a sibling merge has a
complete bipartite crossing graph, so each live edge has exactly
`2(2^(j-1)-1)` adjacent crossing edges at merge depth `j`. Deterministic
sampling on the natural high-dimension collision-free threshold portfolios
gives:

| `n` | `k` | live stars | mean off-common weight | projected degree (log2) |
| --- | --- | --- | --- | --- |
| 7 | 7 | 14/40 | `2^-10.86` | `-3.88` |
| 8 | 11 | 29/40 | `2^-8.81` | `2.19` |
| 9 | 15 | 39/40 | `2^-4.93` | `10.07` |
| 10 | 21 | 40/40 | `2^-3.66` | `17.34` |
| 11 | 26 | 40/40 | `2^-3.61` | `22.39` |
| 12 | 29 | 40/40 | `2^-3.57` | `25.50` |

The mechanism is visible in the data. At `n=7` no sampled star has a
one-dimensional carrier and every weight is a small two-carrier product. By
`n=12` thirty-seven of forty sampled stars have a one-dimensional carrier in
one cluster and the mean weight has reached `0.975` times `1/(n-1)`. That is
Sellke covering saturating the membership blocks, the same mechanism already
used by the Plancherel block obstruction. Weighted degree therefore grows like
`2^(j-1)/(n-1)`, which is `Theta(n!/n)` at `j=k=ceil(log2 n!)`.

Conclusion: **no absolute-weight comparison can certify the residual quotient
at natural depth.** The 33 of 6,766 finite planes the sign-blind bound failed
to certify were not an edge case; they were the leading edge of the asymptotic
regime. The certificate is already vacuous at `n=8`.

The surviving object is identified. Let `C` be the signed subspace incidence
map sending an edge coefficient in `K_e` to `+` its vector at one endpoint and
`-` at the other. Then `C^*C` is exactly the relation Gram the Cech modules
already use, and `CC^*` is the projector-weighted orientation Laplacian

`Delta = D - A`, `D_uu = sum_{e containing u} P_{K_e}`, `A_uv = P_{K_uv}`.

Their positive spectra coincide; two finite controls verify this with maximum
residual `4.2e-14`. All-depth conditioning is therefore a **subspace
connectivity** question about projector-weighted orientation graphs, not a
weighted-degree question. No Laplacian gap is proved. Eight focused tests pass.

## Model-Scope Analysis For The Two Literature Lower Bounds

These are reasoning notes, not resolved obligations. They exist so the next
pass does not have to re-derive the scope question.

### Moore--Russell--Sniady

`https://arxiv.org/abs/quant-ph/0612089` rules out Kuperberg-style adaptive
sieves on the wreath-product graph-isomorphism reduction below
`exp(Omega(sqrt n))`. Their algorithm class combines a bounded number of coset
registers at a time, applies Clebsch-Gordan, and measures or discards between
combination steps.

The hierarchical polar tree superficially looks like such a sieve because it
recurses on sibling merges. The degree obstruction above is the argument that
it is not: at natural depth the crossing graph of a single merge is complete
bipartite with saturated weights, so no bounded-arity, locally measured
combination reproduces one level. The architecture needs one globally coherent
`Theta(n log n)`-register transform with no intermediate label measurement.
That is outside the stated class.

This is a structural argument, not a formal separation. Before any speedup
claim, the polar tree must be written in MRS's own formal algorithm model and
shown either to violate their locality hypothesis or to be simulable by it.
Do not infer the separation from naming, and do not mutate the current filter
into a pairwise or small-register Clebsch-Gordan sieve.

### Ozols--Roetteler--Roland

The rejection-sampling lower bound is a *state conversion* bound, and the
repository currently holds an *information* bound (`1/16` PGM success) and a
*filter retention* bound. These are not comparable as stated. The decisive
missing computation is explicit: take the coherent Fourier decoder criterion's
sector Schmidt probabilities `lambda_{nu,i}`, form the source amplitude vector
of the physical post-filter frame state and the target amplitude vector
required by `p_nu=d_nu^2/|G|` with flat `f_nu=1`, and evaluate the
water-filling cost of that conversion. Until that vector pair is written down,
no claim that representation labels evade the oracle model is admissible.

## Width-Independent Metric Floor: The Sign-Blind Pessimism Is Withdrawn

Files:

- `self_dual_wreath_orientation_laplacian_gap.py`
- `research/representation/self_dual_wreath_orientation_laplacian_gap.json`
- `tests/test_self_dual_wreath_orientation_laplacian_gap.py`

The previous pass proved that absolute-weight comparison is vacuous at natural
depth and left the impression that the hierarchy is badly conditioned. **That
reading was wrong, and this section supersedes it.** Keeping the incidence
signs shows the relation metric does not degrade with merge width at all.

**Dirichlet form.** For the signed subspace incidence map `C` and
`Delta = CC^*`,

`<x, Delta x> = sum_e ||P_(K_e)(x_a - x_b)||^2`,

so `ker Delta` is exactly the set of vertex assignments whose edge differences
avoid every live pair core.

**Commuting case, solved exactly.** When the live pair-core projectors commute
they have Boolean atoms `A_S` and

`M = direct_sum_S L_S tensor I_(A_S)`,

with `L_S` the scalar graph Laplacian of the atom's edge set. The affine-
support theorem forces each atom's orientation set to be an affine subspace,
so `S` is a **complete** graph and `lambda_2(L_S) = |F_S| >= 2`. Hence
`lambda_min+(M) >= 2` **regardless of how many pair cores meet one
orientation**. Both commuting controls reproduce the atom prediction exactly,
with every atom support affine.

**Exact p-star law.** For a star of `p` edges at one vertex with residual
correlation `gamma`,

`spec(M) = {2-gamma} with multiplicity p-1, together with 2+(p-1)gamma`.

The smallest eigenvalue **does not move as `p` grows**. This reproduces the
known S6 noncommuting counterexample exactly: `gamma=1/9`, `p=3`, spectrum
`17/9` and `20/9`, residual `2.7e-15`. The `d=5` plane gives `gamma=1/5`,
`p=2`, spectrum `9/5` and `11/5`.

**Uniform-transport floor.** If the residual overlaps factor through vertex
isometries `W_(e,v)` with one common `gamma`, then

`M = 2(1-gamma)I + gamma C~^* C~`,

so `spec(M) = 2(1-gamma) + gamma spec(L~)` for the twisted graph Laplacian.
Since `C~^*C~` is positive semidefinite **for any holonomy**,

`lambda_min(M) >= 2 - 2 gamma >= 2 - 2/(n-1)`,

independent of merge width. At `n=12` that floor is `1.8182`; the sign-blind
estimate for the same merge was `-4.88e7`.

**Evidence.** 270 full-live-graph controls, zero violations of the
`2-2gamma_max` floor. On natural threshold portfolios the number of distinct
off-common correlations per sampled star collapses monotonically as the label
count grows — 16, 13, 8, 2, 1 for `n = 8,9,10,11,12` — reaching a **single**
value `1/(n-1)` at `n=12`. The same Sellke saturation that killed the
sign-blind bound is exactly what makes the transport uniform.

**Two traps recorded.** First, the floor is a statement about the **full live
graph**; evaluating the same form on a star subgraph deletes edges and drops
the minimum to `lambda_2` of a star, which is one. A screen that restricted to
star subgraphs produced 20 spurious "violations". Second, disjoint pair cores
overlap geometrically but contribute **nothing** to the relation Gram, whose
off-diagonal blocks are indexed by shared vertices only.

**Scope.** The vertex trivialization is a hypothesis. Only its
single-correlation half is measured; no isometry factorization is constructed
and the holonomy of the residual transport bundle is untested. Nothing here
bounds the graded form, so endpoint gaps for the relative polar are still
open, and no circuit follows.

## Highest-Value Open Derivation

The PGM still has constant information-theoretic success and physical
transfer. The pair-core overlap operator is now exact, and the sign-blind
route to all-depth conditioning is dead. Work in this revised order:

1. Construct or refute the **vertex trivialization of the residual transport**
   at natural depth. This is now the single decisive statement. The
   single-correlation half of the hypothesis is measured and holds at `n=12`;
   what is missing is the isometry factorization
   `B_e^* B_f = gamma W_(e,v)^* W_(f,v)` for adjacent live cores. Build the
   `W_(e,v)` from the carrier factorization's explicit index bijection, or
   exhibit a natural adjacent pair whose normalized overlap is not a
   restriction of a common vertex isometry.
   Note holonomy does **not** need to vanish: `C~^*C~ >= 0` for any
   connection, so the floor `2-2gamma` survives arbitrary holonomy. Only the
   factorization itself is at stake.
   Falsifier: a natural full live graph with `lambda_min+(M) < 2 - 2gamma_max`.
2. Bound the **graded defect**, not just the metric. The metric floor says
   nothing about `||M^(-1/2) J M^(-1/2)||`, which is what endpoint gaps for
   the relative polar actually require. Redo the star and commuting-atom
   calculations with the `J` grading in place and determine whether the
   defect is also width independent.
3. Prove or falsify the **uniform residual pair-quotient gap**: an all-n bound
   below one on `||P_(A minus K)P_(B minus K)||`. This is a *geometric*
   statement about child spans, and unlike the relation Gram it **does** see
   vertex-disjoint core overlaps, which are nonzero at natural depth. Absolute
   weights are proved inadequate; the Laplacian floor does not transfer here
   automatically.
4. Derive the **exact vertex-disjoint pair-core overlap**. The shared-vertex
   case is a scalar; the disjoint case is a grid contraction with genuine
   Kronecker content, currently controlled only by the waist upper bound. That
   bound is exactly tight on all forty screened controls, so either prove
   equality or exhibit a strictly smaller grid. This feeds item 3, not the
   relation Gram.
5. Extend the finite **phase-sensitive relative Cech/Laplacian prototype** to
   all depth. Prove exactness or classify `H_p`, `p>=1`, for the noncommuting
   multiplicity sheaf. Use the `C^*C`/`CC^*` duality so that homology is
   computed on the vertex side, and reuse the commuting-atom splitting: under
   commutativity the whole complex is a direct sum of scalar complete-graph
   complexes on affine supports.
6. Determine the **physical PGM mass** of the noncommuting blocks. A finite
   S6 defect does not establish asymptotic relevance. Compute frame-weighted,
   not raw multiplicity-weighted, mass on natural threshold portfolios. The
   carrier factorization now supplies exact per-sector weights for this.
7. Compile or kill a coherent **Racah/common-core transform**. The scalar
   shared-vertex result removes one imagined obstruction: there is no
   nontrivial 6j block to compile at the star level. The compilation target is
   therefore the Cech quotient and the disjoint-pair grid blocks, in
   polynomial gates, with multiplicity spaces kept in quantum registers.
8. Extend the weighted common-free exclusion to the residual after exact
   affine common supports and noncommuting pair cores are removed. Note the
   same asymptotic caution as item 3: any successor must not be sign blind.
9. Write the hierarchical polar tree in the **Moore--Russell--Sniady** formal
   algorithm model and either prove simulation (killing the route) or isolate
   the coherent operation that escapes it. See the scope analysis above; the
   degree obstruction is evidence, not a separation.
10. Compute the **Ozols--Roetteler--Roland** water-filling cost for the
    explicit source/target amplitude pair named in the scope analysis above.
11. Only after 1--7, compose
    `physical row-copy -> Q_R^* -> inverse S_n QFT` and audit total gates,
    copies, memory, and approximation error.
12. Maintain the falsification route: a residual quotient gap closing on
    positive natural mass, a superpolynomial Racah transform, or an
    extended-sieve simulation is a reason to abandon this PGM architecture.

Do not resume claims of universal exact half-balance. Do not use pair
generation, affine support balance, XOR covariance, or finite reciprocal
spectra as substitutes for the missing Laplacian-gap and conditioning
theorems. In particular, do not reintroduce any absolute-weight or block
Gershgorin certificate as an all-depth argument: it is now proved vacuous at
natural depth. Additional finite work is justified only when it attacks one of
those statements with a declared counterfamily.

Two corrections that must not be re-broken. The metric floor is about the
**full live graph**: a star-subgraph evaluation is not evidence about a merge.
And the relation Gram has **no vertex-disjoint off-diagonal blocks**; disjoint
core overlaps matter for the child-span geometry in item 3, not for `M`.

## Mechanical Follow-Up For Antigravity / Gemini 3.6 Flash

These tasks are useful but should not consume the scarce high-reasoning pass:

1. Re-run and record the standard downstream workflows after any new module:
   `dequantize`, `proofs`, `query-models`, `frontiers`, `conjectures`,
   `mutate`, and `validate`.
2. Add routine CLI/experiment-runner/registry plumbing by copying the pattern
   used for `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT`.
   The common-range experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE`, and its intended CLI
   name is `code-wreath-orientation-common-ranges`.
   The fixed-family experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE`, and its intended CLI
   name is `code-wreath-orientation-family-ranges`.
   The pair-angle experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES`, and its intended CLI
   name is `code-wreath-orientation-pair-angles`.
   The finite block-core experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE`, and its intended
   CLI name is `code-wreath-orientation-block-core`.
   The asymptotic obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION`, and its intended
   CLI name is `code-wreath-plancherel-block-obstruction`.
   The trimmed measurement experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM`, with intended CLI
   `code-wreath-spectral-trim`.
   The generic degree obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION`, with
   intended CLI `code-wreath-spectral-filter-degree`.
   The Plancherel mass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS`, with intended CLI
   `code-wreath-plancherel-block-mass`.
   The algebraic quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT`.
   The branchwise commutant experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION`.
   The physical branch-filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER`.
   The paired-filter bypass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS`.
   The all-local-filter no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO`.
   The cluster-locality lower-bound experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO`.
   The black-box spectral query lower-bound experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND`.
   The orientation-character filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER`.
   The invariant-projector circuit experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT`.
   The physical-access audit experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS`.
   The direct physical filter experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE`.
   The natural retention theorem experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM`.
   The exact postfilter-compression experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION`.
   The logarithmic rank-retention experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET`.
   The isotypic-dephasing no-go experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO`.
   The coherent Fourier decoder experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER`.
   The quantum-sampling normal-form experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION`.
   The pair-polar experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER`.
   The hierarchical-chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE`.
   The relative-intersection experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION`.
   The common-core bypass experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS`.
   The early-overlap experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION`.
   The generic equal-Gram transfer-gate experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER`.
   The resolved physical transfer experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER`.
   The exhaustive three-bit flag experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT`.
   The canonical cross-dependency experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY`.
   The scalar Cayley reduction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION`.
   The matrix Cayley failure-boundary experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY`.
   The sparse invariant dependency experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY`.
   The common-free weighted exclusion experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION`.
   The pair/emergent quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY`.
   The affine-support/noncommuting-core experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION`, with suggested CLI
   `code-wreath-common-core-atomization`.
   The local recoupling-conditioning experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY`, with suggested
   CLI `code-wreath-pair-core-recoupling`.
   The phase-sensitive common-core chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN`, with suggested CLI
   `code-wreath-common-core-cech`.
   The augmented leaf-dependency chain experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH`, with suggested CLI
   `code-wreath-augmented-common-core-cech`.
   The recursive H0 experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION`, with suggested CLI
   `code-wreath-recursive-pair-generation`.
   The exact residual quotient experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP`, with suggested CLI
   `code-wreath-pair-quotient-overlap`.
   The pair-core carrier factorization experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION`, with suggested
   CLI `code-wreath-pair-core-carrier-factorization`.
   The multistar degree obstruction experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION`, with suggested
   CLI `code-wreath-multistar-degree`.
   The orientation Laplacian gap experiment ID is
   `EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP`, with suggested CLI
   `code-wreath-orientation-laplacian-gap`. This one is not wired yet.
3. Add Sellke's paper to `research/literature_index.json` and
   `research/literature_records.json`, preserving the precise mechanism,
   theorem, reuse, and no-overclaim fields.
4. Add clean-registry dispatch tests and update README command examples.
   The step-by-step version of items 1-6 with exact commands, acceptance
   checks, and forbidden actions is in
   `research/MECHANICAL_FOLLOW_UP_PLAN.md`. Work from that file, not from
   this summary.
5. Run focused tests first, then `python -m compileall -q .`,
   `node --check site/progress.js`, `git diff --check`, and
   `python qsearch.py validate`.
6. Do not run the multi-hour full suite after every narrow change. The last
   complete repository suite before these two modules was 1,494 tests passed;
   use affected tests unless a shared contract changes.
7. Do not commit or push each subsystem. Make one intentional checkpoint only
   after several coherent research passes or when the user requests it.

## Resume Commands

```bash
python qsearch.py code-wreath-orientation-fourier
python qsearch.py code-wreath-orientation-moments
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT
python self_dual_wreath_physical_pgm_intertwiner.py
python self_dual_wreath_level_three_flag_audit.py
python self_dual_wreath_common_core_atomization.py
python self_dual_wreath_dependency_homology.py
python self_dual_wreath_pair_core_recoupling_boundary.py
python self_dual_wreath_common_core_cech_laplacian.py
python self_dual_wreath_augmented_common_core_cech.py
python self_dual_wreath_recursive_pair_generation.py
python self_dual_wreath_pair_quotient_overlap.py
python self_dual_wreath_pair_core_carrier_factorization.py
python self_dual_wreath_multistar_degree_obstruction.py
python self_dual_wreath_orientation_laplacian_gap.py
python qsearch.py code-wreath-subpovm-moments
python qsearch.py validate
```

Before claiming progress, inspect the current artifact and verify that every
claimed theorem has a proof gate and every finite experiment has an explicit
falsifier. Keep `speedup_claim_allowed` false until the asymptotic norm,
coherent measurement, decoder, end-to-end complexity, and classical-baseline
obligations are all resolved.
