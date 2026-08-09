# Quantum Algorithm Research Engine

This project is being reshaped around one goal: increase the chance of finding
or clarifying a genuinely major quantum algorithmic idea. It should not optimize
for demos, toy circuits, small benchmark wins, or unsupported speedup claims.

Model usage is part of that objective. Spend high-capability Codex time on the
work whose bottleneck is research judgment: theorem derivation, structural
falsification, asymptotic analysis, representation-theoretic reductions, and
the design of decisive experiments. Batch routine plumbing, registry/CLI
wiring, formatting, artifact refreshes, and repetitive validation for Gemini
3.6 Flash through Antigravity after Codex usage is exhausted. Before any Codex
session ends, maintain `research/AGENT_HANDOFF.md` as an executable continuation
queue that preserves theorem scope, unresolved assumptions, falsifiers,
negative results, and exact mechanical tasks. The successor must not restore
toy circuit search or promote a finite experiment into a speedup claim.

## Blunt Diagnosis

The original project was not a credible path to a Shor-level discovery.

- It searched N<=3 toy circuits and arbitrary oracle puzzles.
- It asked an LLM to infer asymptotic complexity from tiny simulations.
- Most "successful" runs rediscovered Bernstein-Vazirani-like parity structure.
- Many exotic result names were just custom bitwise secret-finding oracles with
  no natural scalable problem family.
- The dashboard treated `success_rate >= 1.0` on tiny instances as "solved novel
  algorithms", which is not a research result.
- State preparation and unitary synthesis are useful subroutines only when tied
  to a larger algorithmic mechanism; as standalone discovery targets they are
  low ceiling.

The old simulator and raw legacy outputs have been removed or distilled into
negative-result records. The source of truth is now the proof-gated research
registry.

## Revised Direction

The project is now a research-lab operating system in early form: research
agenda generation, literature memory, problem/reduction ontology, proof
obligations, and structural-test harnesses.

It ranks hypotheses by:

- Scalable problem family, not one-off oracle code.
- Plausible classical barrier or lower-bound target.
- Quantum mechanism tied to known sources of advantage: Fourier sampling, hidden
  subgroup or hidden shift structure, phase estimation, quantum walks,
  block-encoding, Hamiltonian simulation, or collective measurements.
- Explicit positive signals and kill criteria.
- Clear path from finite experiments to asymptotic proof obligations.

## Current Research Frontier

- No new quantum algorithm or speedup has been found.
- An exact XOR re-rooting induction now controls every ordered frame-subword
  support at arbitrary width and over every finite group.
- For contiguous A/B frame words, arbitrary support profiles have scalar
  crossing pressure at most the obstruction threshold; the surviving target
  character reduces exactly to one centralizer-weighted frame word.
- Scalar-pressure saturation forces target identity. An exact `S3`
  identity-frame lift once made the real entropy certificate margin tend to
  zero, but the stronger suffix-branch generator theorem restores a uniform
  gap on that lift. Independently, exact surface reduction forces every
  appended frame to identity and makes every nontrivial nonsign target vanish
  in growing `S_n` (the standard target is asymptotic to `2/n^2`).
- Pruning that lift to support sizes `2^k-1` and `2^k` does make the strongest
  generic integer-certificate margin tend to zero. Exact reduction still kills
  it: every depth is a genus-two surface group with one free generator, the
  target remains one handle commutator, and the true scalar pressure margin is
  greater than one. Generic certificate failure is therefore not a surviving
  asymptotic channel.
- The active theorem target is a growing-width `S_n` bound for weighted frame
  presentations outside that genus-two seed, followed by the interleaved-leaf
  multi-boundary case.
- A nonidentity periodic `S3` frame assignment initially looked more dangerous:
  its older real entropy pressure margin vanishes exponentially without identity
  padding. That mechanism is now closed. An exact suffix-branch theorem leaves
  at most three frame generators for every `k=6m+1`; the full presentation has
  at most `|S_n|^(4+o(1))` solutions and a uniform pressure margin of at least
  `1-0.5*log2(3/2)`. The next structural question is whether comparable rank
  collapse holds for every dense fixed-state frame automaton. If so, viable
  constructions must use growing-state algebra or genuinely interleaved leaves.

## High-Upside Search Areas

The first agenda focuses on:

1. Nonabelian hidden subgroup problems and collective coset-state measurements.
2. Hidden shift, dihedral HSP, and phase-state sieving.
3. Lattice and number-field approximate periodicity.
4. Code equivalence and algebraic isomorphism.
5. Graph isomorphism beyond strong Fourier sampling.
6. Quantum walks on algebraic and combinatorial state spaces.
7. Query complexity separations with recursive structure.
8. Hamiltonian simulation, block-encoding, and tensor-network discovery.

## How To Run

Regenerate the audit, agenda, registry seeds, ontology, literature index, and
negative-result database:

```bash
python qsearch.py audit
```

Extract structured mechanism records from the curated seed literature, with
optional arXiv refresh:

```bash
python qsearch.py literature
python qsearch.py literature --refresh-arxiv
```

Generate proof-gated hypotheses from the literature records and problem
ontology:

```bash
python qsearch.py hypothesize
```

Run the hidden-shift/DHSP phase-state workbench:

```bash
python qsearch.py hidden-shift
python qsearch.py hidden-shift --sample-count 8 --min-bits 5 --max-bits 8
python qsearch.py dcp-samples --n-values 8,10,12 --sample-count 4096
python qsearch.py dcp-decode --n-values 8,10,12 --samples-per-stage 4096
python qsearch.py dcp-recurrence --n-values 8,12,16,20,24 --trials-per-point 12
python qsearch.py dcp-schedules --n-values 20,24,28,32 --budget-multiplier 2.0 --train-trials 8 --holdout-trials 24
python qsearch.py dcp-uniform-schedules --train-n-values 20,24,28 --unseen-n-values 32,36,40
python qsearch.py dcp-bad-registers --n-values 12,16,20,24
python qsearch.py dcp-contamination --n-values 8,10,12,14,16 --register-fractions 0.25,0.5,1.0
python qsearch.py dcp-witness-search --n-values 12,16,20,24 --maximum-weight 4
python qsearch.py dcp-clifford-witnesses --n-values 8,10,12,14,16
python qsearch.py dcp-clifford-contamination --n-values 6,8,10,12
python qsearch.py dcp-hadamard-scaling --n-values 6,8,10,12 --register-ratios 0.5,1.0,1.5,2.0
python qsearch.py dcp-random-decoder --n-values 8,10,12,14,16 --sample-multipliers 2,4,8,16
python qsearch.py dcp-decoder-frontier
python qsearch.py dcp-multiscale-aliasing
python qsearch.py dcp-fourier-bridge
python qsearch.py dcp-sparse-fourier-audit
python qsearch.py dcp-iid-hash-audit
python qsearch.py dcp-likelihood-search
python qsearch.py dcp-biased-linear-audit
python qsearch.py dcp-multirecord-audit
python qsearch.py dcp-ustatistic-audit
python qsearch.py dcp-factorized-contraction
python qsearch.py dcp-low-rank-contraction
python qsearch.py dcp-subset-sum-measurement
python qsearch.py dcp-hashed-fiber-measurement
python qsearch.py dcp-reference-projection
python qsearch.py dcp-covariant-pgm
python qsearch.py dcp-contaminated-pgm
python qsearch.py dcp-subset-sum-bridge
python qsearch.py dcp-subset-sum-lattice
python qsearch.py dcp-subset-sum-two-adic
python qsearch.py dcp-subset-sum-resource-frontier
python qsearch.py dcp-subset-sum-carry-anf
python qsearch.py dcp-subset-sum-synthesize
python qsearch.py dcp-subset-sum-low-bit-bdd
python qsearch.py dcp-subset-sum-conditioned-quotient
python qsearch.py dcp-subset-sum-carry-slice-lattice
python qsearch.py dcp-carry-high-part
python qsearch.py dcp-boolean-coset-separation
python qsearch.py dcp-marker-list-decoder
python qsearch.py dcp-marker-deviations
python qsearch.py dcp-marker-all-targets
python qsearch.py dcp-marker-vulnerable-coordinates
python qsearch.py dcp-marker-chart-union
python qsearch.py dcp-marker-target-beam
python qsearch.py dcp-subset-sum-preconditioned-geometry
python qsearch.py dcp-subset-sum-fourth-moment
python qsearch.py dcp-subset-sum-smith-moments
python qsearch.py dcp-subset-sum-smith-transfer
python qsearch.py dcp-subset-sum-fixed-moments
python qsearch.py dcp-subset-sum-conditioned-tail
python qsearch.py dcp-subset-sum-growing-moments
python qsearch.py dcp-subset-sum-growing-chain
python qsearch.py dcp-subset-sum-signed-l2
python qsearch.py dcp-subset-sum-sparse-characters
python qsearch.py dcp-subset-sum-qtt
python qsearch.py dcp-subset-sum-embedding-volume
python qsearch.py dcp-subset-sum-short-relations
python qsearch.py dcp-subset-sum-carry-relations
python qsearch.py dcp-subset-sum-marker-coset
python qsearch.py dcp-subset-sum-affine-cvp
python qsearch.py dcp-subset-sum-affine-scaling
python qsearch.py dcp-subset-sum-affine-bdd
python qsearch.py dcp-subset-sum-target-distribution
python qsearch.py dcp-coherent-matching
python qsearch.py dcp-quantum-relation-fidelity
python qsearch.py dcp-quantum-walk-source-audit
python qsearch.py dcp-symmetric-relation-lift
python qsearch.py dcp-fiber-transport
python qsearch.py dcp-fiber-graph
python qsearch.py dcp-signed-permutation-transport
python qsearch.py dcp-affine-transport
python qsearch.py dcp-fiber-balance
python qsearch.py dcp-partial-relations
python qsearch.py dcp-target-locality
python qsearch.py dcp-fiber-entanglement
python qsearch.py dcp-adaptive-layouts
python qsearch.py dcp-subset-sum-randomize
python qsearch.py dcp-odd-unit-geometry
python qsearch.py run EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION
python qsearch.py run EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER
python qsearch.py run EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY
python qsearch.py run EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE
python qsearch.py run EXP-DHS-DCP-MARKER-VULNERABLE-COORDINATE-DECODER
python qsearch.py run EXP-DHS-DCP-MARKER-CHART-UNION-DECODER
python qsearch.py run EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN-THEOREM
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-SIGNED-L2-OBSTRUCTION
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-QTT-DENSE-CONTRACTION
python qsearch.py dcp-pgm-gram
python qsearch.py run EXP-DHS-DCP-PGM-GRAM-BLOCK-ENCODING
python qsearch.py dcp-pgm-qsvt
python qsearch.py run EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION
python qsearch.py dcp-quenched-occupancy
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-QUENCHED-OCCUPANCY-THEOREM
python qsearch.py dcp-fiber-erasure-boundary
python qsearch.py run EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY
python qsearch.py dcp-erasure-inversion
python qsearch.py run EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION
python qsearch.py dcp-erasure-coherence
python qsearch.py run EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION
python qsearch.py dcp-erasure-perturbation
python qsearch.py run EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION
python qsearch.py run EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE
python qsearch.py run EXP-DHS-DCP-RECURSIVE-DECODER
python qsearch.py run EXP-DHS-DCP-RECURRENCE-SCALING
python qsearch.py run EXP-DHS-DCP-SCHEDULE-SEARCH
python qsearch.py run EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY
python qsearch.py run EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS
python qsearch.py run EXP-DHS-DCP-CONTAMINATION-WITNESS
python qsearch.py run EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH
python qsearch.py run EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH
python qsearch.py run EXP-DHS-DCP-CLIFFORD-CONTAMINATION
python qsearch.py run EXP-DHS-DCP-HADAMARD-SCALING
python qsearch.py run EXP-DHS-DCP-RANDOM-DESIGN-DECODER
python qsearch.py run EXP-DHS-DCP-DECODER-FRONTIER
python qsearch.py run EXP-DHS-DCP-MULTISCALE-ALIASING
python qsearch.py run EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE
python qsearch.py run EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT
python qsearch.py run EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR
python qsearch.py run EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT
python qsearch.py run EXP-DHS-DCP-REFERENCE-PROJECTION-AUDIT
python qsearch.py run EXP-DHS-DCP-COVARIANT-PGM-AUDIT
python qsearch.py run EXP-DHS-DCP-CONTAMINATED-PGM-AUDIT
python qsearch.py run EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH
python qsearch.py run EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND
python qsearch.py run EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN
python qsearch.py run EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY
python qsearch.py run EXP-DHS-DCP-IID-USTATISTIC-VARIANCE
python qsearch.py run EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION
python qsearch.py run EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION
python qsearch.py run EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT
python qsearch.py quarantine-invalid
```

The DCP sample audit is the authoritative sieve baseline. It starts from the
independent coset/phase states supplied by the exact reduction contract,
forbids evaluator access, charges the `1/2` sum/difference branch, and does not
mistake an `N/2` parity endpoint for full hidden-reflection recovery.
The exact Regev `f=1` contract also permits an arbitrary bad basis-state
register with probability up to `1/log N`; perfect-state sieve artifacts do not
cover that promise and are now explicitly marked incomplete.
The recursive decoder audit then composes fresh state batches with exact
known-residue phase corrections. Finite full recoveries remain blocked evidence
until a uniform endpoint probability, total failure bound, asymptotic resource
comparison, and lattice composition theorem are supplied.

Random-label X/Y measurements now have an exact observation contract. Their
conditional first moment is the hidden Fourier character on good DCP registers
and zero on every allowed computational-basis bad register. Exhaustive
correlation therefore gives a proved `O(log N)` sample decoder at the exact
`f=1` contamination rate, but still costs `Theta(N)` time. This separates the
information question from the computational question instead of treating a
full FFT as an algorithmic advance. Query-model audits reject direct use of
chosen/correlated-query sparse Fourier algorithms. A Parseval certificate rules
out exact unbiased one-pass linear iid bucket estimators with jointly
polynomial sample and bucket complexity, while exact nonlinear likelihood
branch-and-bound currently scores every one of the `N` candidates. Neither
restricted failure is represented as a general nonlinear lower bound.
Biased or smoothed one-score linear responses also retain an exponential
margin-resolution tradeoff. Fixed-degree signed products on disjoint record
blocks do not help: their aggregate label remains uniform and their second
moment grows as `4^r`. Overlapping U-statistics, adaptive score families,
implicit contractions, and premeasurement collective observables remain open.
An exact Hoeffding-decomposition audit further rules out explicit all-subsets
product U-statistics: fixed degree needs exponentially many records, while
growing degree can reduce records only by requiring exponentially many tuple
terms. Polynomial implicit contraction remains open and is now the relevant
exception.
The first implicit contraction has also been audited: a scalar rank-one product
kernel can be contracted with elementary-symmetric dynamic programming in
`O(mr)`, but its first Hoeffding projection forces `Omega(r^2 N/B)` records for
`B` equal buckets. Polynomial-rank projection cancellation and low-bond tensor
contractions remain open.
The polynomial-rank search optimizes worst-point margins over closed-form
cosine, Fejer, and hybrid dictionaries and evaluates every cross-component
Hoeffding projection exactly. Finite uniform separation occurs, but every such
row is sample-superpolynomial; no row survives all resource gates.
For collective measurements, computing the public-label subset sum and applying
a QFT to its ancilla is exactly uninformative while the input register retains
which-subset garbage. A straightforward exact residue MPS has exponential bond
dimension with high probability. Approximate hashed residue networks and
coherent collision-fiber symmetrization remain open.

The primary-source Regev bridge now makes the most useful target narrower than
full PGM implementation: a deterministic polynomial-time solver for an
inverse-polynomial fraction of legal random modular subset-sum inputs at density
one is sufficient for the exact `f=1` DCP route. Tested centered LLL embeddings
show only transient finite recovery and no coverage theorem. The 2-adic lifting
audit additionally measures exact carry-predicate ANF degree and affine-hull
overcoverage over `Z_(2^n)`. It is an exponential structural microscope, not a
solver: finite low-degree interpolation, affine overapproximations, and compact
equation descriptions remain blocked until a uniform polynomial witness
algorithm, legal-input coverage proof, and reversible matching interface exist.

The logarithmic low-bit route now has three separate gates. An exact
`O(n 2^b)` branching program proves polynomial low-fiber preparation for
`b=O(log n)`, but the conditioned high-bit quotient remains broad in the live
exact sweep and has no implicit decoder theorem. Enumerating every reachable
low carry gives a genuine deterministic polynomial carry-sliced LLL class; in
paired tests it did not improve the largest-size tail and still lacks uniform
legal-input coverage. The exact carry high-part theorem further proves that a
carry selected from low data leaves the translated high quotient identically
uniform; trying all polynomially many carries cannot rescue an exponentially
rare generic high-only event. This closes only high-only quotient bias, not a
joint low/high basis or a concrete generic LLL-event analysis. Complete target tables also separate independent uniform,
uniform legal, and planted-witness targets: planting measurably size-biases
representation multiplicity, so planted success is rejected unless it transfers
to an efficiently detectable inverse-polynomial source-target subfamily with a
polynomial witness algorithm. Finite entropy, finite LLL recovery, and two
factorial moments are never promoted to lower bounds.

The low-fiber fourth-moment audit now goes beyond a finite trend. Residuals are
exactly three-wise independent; fourth-order deviations occur only on affine
xor-zero quadruples. Exact integer-rank and Smith-(1,1,1,2) counting proves the
source-averaged fixed-fourth excess decays as `O((3/4)^n) + O(2^-n)` at fixed
register offset. This closes generic fixed-fourth source-average mechanisms,
but deliberately leaves atypical-fiber concentration, growing-order moments,
reduced-basis geometry, and implicit decoding open.

The Smith moment spectrum then extends the structural microscope to orders five
and above. Complete rows compute exact source factorial moments from the integer
Smith form of assignment-target matrices; larger rows are labeled
`sampled-type-probe` and are explicitly unusable as absence evidence because
exponentially rare affine classes can dominate a moment. The next theorem target
is a uniform class-count recurrence, not another finite moment fit. Exact
five-set classification already proves the source-average fixed-fifth excess
also decays as `O((3/4)^n) + O(2^-n)`. The order-six transfer closes the next
layer too: exhaustive
HNF state closure finds 2,336 reachable lattices, and every non-generic terminal
state has Boolean growth/rank-penalty ratio at most `3/4`. Thus fixed-sixth
source excess is `poly(n)*(3/4)^n`-bounded.

The general projection theorem removes every larger fixed order too. For
every fixed order `k`, an injective coordinate projection bounds Boolean points
in a rank-`r` transfer lattice by `2^r`; equality would force duplicate rows, or
a full-rank 2-adic lattice would contain every basis vector and cease to be
proper. Every bad distinct-row state therefore contracts by at most
`1-2^-k`. All fixed source moments are closed. Only `k=k(n)` with fully charged
resources, atypical conditioned fibers, and non-moment geometry remain open.

For nonnegative fixed-order bad-tuple signal, even the atypical-fiber loophole
is closed. Conditioning on all exposed low bits preserves the exponentially
small mean by the tower property; Markov bounds the source mass of fibers with
conditional signal at least `n^-d` by `poly(n)*(1-2^-k)^n`. Growing order,
signed observables not dominated by this contribution, and explicit
reduced-basis events remain open and must carry decoder implications.

Growing order is now closed almost to logarithmic order. The original transfer
bound allowed `2^k` proper lattice enlargements and proved decay only when
`4^k log n=o(n)`. Saturation index gives a sharper chain theorem: at rank `r`,
the lattice index is at most an `r x r` Boolean determinant, hence
`r^(r/2)`, and each proper same-span extension drops that integer index by at
least two. Rank increases at most `k-1` times, so every non-self path has
`O(k^2 log k)` transitions. The bad contribution therefore vanishes when
`2^k O(k^2 log k)(log n+k)=o(n)`, including every
`k <= (1-epsilon) log_2 n` and a conservative
`log_2 n-(4+epsilon)log_2 log_2 n` schedule. Exact transfer DAGs through order
five satisfy the bound. The final near-log window, signed observables,
reduced-basis events, estimation resources, and decoder implications remain
open.

The lattice route now has an exact volume gate. The standard embedding has
covolume `2^m(2s2^n)`. Cauchy-Binet gives an exact carry-sliced covolume, and
for `b=O(log n)` both determinant roots tend to 4. The planted witness remains
at limiting Gaussian-volume ratio `sqrt(2*pi*e)/4`, about 1.033. This rules out
volume-only separation, not local Gram-Schmidt structure or an average
short-vector count theorem.

The standard embedding now has a stronger local obstruction. Weight-one-quarter
signed modular relations produce marker-zero vectors no longer than the planted
witness. An exact second moment proves exponentially many such competitors with
high probability at density one. Standard shortest-vector uniqueness is therefore
dead; only added constraints such as carry slicing or a proved marker-aware
extractor remain admissible lattice mechanisms.

Logarithmic carry slicing does not restore a uniform isolation argument. A
balanced signed family satisfies the exact low equation with collision
probability at least `1/(h 2^b)` and the high modular equation with probability
`2^{-(n-b)}`. A joint-probability bound and Paley-Zygmund theorem give
inverse-polynomial source mass with exponentially many competitors. This is not
a high-probability LLL failure theorem; it forces any surviving proposal to
separate a different legal source subset or prove marker-aware extraction.

The uniform-legal Boolean-coset theorem sharpens that boundary. For independent
uniform labels and an independent uniform target conditioned legal, the expected
number of ordered witness pairs within Hamming radius `r` is exact, and a
Paley-Zygmund conditioning bound proves exponentially small close-pair
probability for every fixed relative radius below `1/2` at `m=n+O(1)`. Thus
abundant short marker-zero relations do not by themselves imply close valid
Boolean witnesses. This is source-average separation geometry, not an
algorithm: it does not handle far witnesses, prove a Babai/LLL cell, construct a
marker-aware decoder, or establish source coverage. Per-instance comparisons
to the source-average bound and planted-target substitutions are invalid.

The first decoder derived from that boundary is a fixed-depth marker-aware
nearest-plane list. After LLL reduction it branches on at most `k` rounding
decisions and enumerates exactly `sum_{j<=k} 2^j binom(d,j)` target-dependent
cells; every reachable carry adds only an `O(n)` factor. For fixed `k` this is a
polynomial classical attack, and every output is verified against the original
equation. The live audit compares depths zero, one, and two on independently
sampled uniform targets with exact meet-in-the-middle legality. Its finite
success is dequantization pressure, not a coverage theorem; finite failure
closes only those bounded lists, not general affine-CVP decoding.

The exact deviation-geometry audit explains that list without enumerating it.
For every completely enumerated witness it solves the witness lattice point in
the LLL-reduced row basis, then replays nearest plane with the true later
coefficients. A witness is in the one-step tree at depth `k` exactly when every
rounding offset has magnitude at most one and at most `k` offsets are nonzero.
This separates depth growth from offsets outside the branch grammar. Truncated
witness sets are excluded from complete conclusions, and finite growth is not
an asymptotic source theorem or a lower bound against other affine decoders.

Target sampling noise is removed by the all-target census. Both reduced kernels
are target-independent, and witness-path offsets equal exact rounded
Gram-Schmidt projections of the `+/-1` witness error. The census Gray-codes the
entire Boolean cube, groups every assignment by its modular target, and reports
the exact fraction of all legal targets covered at each fixed depth for each
label row. This is exhaustive over targets and witnesses for that row. It is
still finite over random labels, so the remaining proof obligation is a
random-label concentration theorem, not another target Monte Carlo sweep.

A growing-depth polynomial attack now tests the most direct escape from that
fixed-depth grammar. It ranks target-independent Gram-Schmidt coordinates by a
public Rademacher rounding-risk score and branches on bounded offsets at
`c ceil(log2 n)` selected coordinates, giving `(2q+1)^(c ceil(log2 n))`
paths and only a linear carry factor. The executable decoder and complete
small-`n` censuses agree exactly. A deterministic fiber-count theorem separates
assignment-weighted witness coverage from uniform-legal target coverage. In the
preregistered `c=2`, `q=1` sweep, carry assignment coverage falls from about
`22%` at `n=36` to `2.3%` at `n=42`, `0.33%` at `n=48`, and below `0.013%`
on every `n=56` label row tested. This is a serious finite negative result for
that selector, not an asymptotic lower bound; the open task is to prove its
random-label decay or find a different public polynomial coordinate geometry.

The next stronger baseline learns a polynomial atlas instead of one coordinate
subspace. From target-independent random-sign probes it freezes up to `n^2`
charts, each with `2 ceil(log2 n)` coordinates, and evaluates the union on
disjoint held-out probes. Training and held-out budgets scale as `16n^2` and
`8n^2`, so the legal chart budget is populated at the tail. Carry held-out
coverage is about `44.5%` at `n=42`, `20.9%` at `n=48`, `1.78%` at `n=56`,
and `0.053%` at `n=64`, despite 4,096 charts at the tail. Exact small-size
target censuses and the assignment-to-target transfer theorem remain valid.
This falsifies the current learned chart family at finite scale; proving
active-mask entropy or designing a non-coordinate decoder remains open.

Target independence is not a legal restriction on the decoder, because Regev's
subset-sum target is part of the observed instance. The stronger K-best beam
baseline therefore uses the actual independent uniform target to rank partial
nearest-plane paths by accumulated orthogonal residual energy. At each level it
retains `n^a` paths, branches by a fixed offset radius, charges every reachable
carry, and verifies every marker candidate against the original congruence.
Exact nearest-integer decisions are separated from floating-point path
priorities. This is a source-native polynomial classical attack. A finite
survivor is dequantization pressure and a finite collapse is not a lower bound;
the research obligation is a uniform source law for the required beam width.
In the live independent-target sweep, standard `n^3` beam success is `3/3` at
`n=40`, `0/3` at `n=44`, `1/3` at `n=48`, and `0/3` at `n=56`; standard and
carry-sliced `n^2` are also `0/3` at `n=56`. Wilson intervals are stored with
every row. These sparse finite counts reject a stable finite survivor but do
not prove negligible success for every fixed polynomial degree.

Sparse signed exact-hit statistics chosen from exposed low labels are now
closed analytically. After conditioning on those low labels, every pair of
distinct nonzero Boolean high equations is exactly independent because its
coefficient matrix has a unit `2x2` minor. Thus a signed score has exact
conditional variance `Q^-1(1-Q^-1) sum c_x^2`, and a support of size `M`
departs from its deterministic no-hit baseline with probability at most
`M/Q`. The exhaustive control verifies all 21 assignment pairs and the exact
variance identity with zero failures. This does not cover coefficients computed
from full high labels, dense implicit contractions, nonlinear statistics, or
reduced-basis geometry; those are the remaining signed-observable directions.

Full-label adaptation does not rescue a polynomially sparse Fourier route.
For the exact subset-sum generating product
`P(r)=prod_i(1+exp(2 pi i r a_i/2^n))`, low-order characters are annihilated
by random antipodal labels. An alias-free growing root moment controls every
remaining character simultaneously. Consequently, after all labels and the
target are visible, any adaptive set of at most `m^B` nonzero characters has
total contribution at most `2^(m-n)m^(B-A)` for every fixed `A`, outside
superpolynomially small source mass. Exact Fourier and root-moment controls pass
with zero failures; three of five finite scaling rows are already conclusive.
This closes sparse dictionaries, not polynomial-size circuits that implicitly
contract exponentially many characters. Dense contraction is now the explicit
Fourier frontier.

The first dense architecture audit tensorizes the exact target count vector
into binary target axes and tests quantized tensor trains. Central-cut singular
tails give necessary bond ranks for entrywise additive count error below
`1/2`, the threshold needed to recover integer counts. Across `n=8–18`, the
best required ranks are `5–6`, `13–14`, `23–28`, `46–47`, and `100–106`;
at `n=18` they reach `218–224`, and the fitted `log2(rank)` slope is `0.519`.
True capped TT-SVD still rounds about `24.5%` of legal counts correctly at the
tail, but the mean excess is only `4.86%` over the zero-frequency constant and
`4.73%` over histogram-permuted controls, below `1/n`, with a fitted excess
slope of `-0.407`. The registered linear bond cap has no uniform survivor after
`n=8`, and TT-SVD itself materializes the full vector. This is finite negative
evidence against direct target-bit QTT, not a lower bound against every
polynomial bond degree or a different algebraic tensorization.

The clean PGM Gram operator now has an exact projected implementation audit.
Uniform subset preparation, reversible modular subset-sum evaluation, and an
equality flag block-encode `diag(c_s/2^m)=G/N` without an exponential table.
That construction does not implement the PGM: at density one, conditioned
first/second-moment bounds put all but inverse-polynomial legal-source mass in
polynomial-size fibers, so generic equality amplification or inverse-square-root
resolution still costs `sqrt(2^m/c_s)=2^Omega(n)`. The generic block-encoding
task is retired. The open implementation frontier is a source-structured
preconditioner, collision walk, or different full-rank measurement with
polynomial normalization, precision, and complete resource accounting.
Generic QSVT does not repair the normalization. Markov's inequality forces
degree `Omega(2^(m/2))` on the direct count encoding and
`Omega(2^(m/4))` on the square-root amplitude encoding whenever singleton and
doubleton fibers coexist. An explicit source family proves this uniformly in
the worst case. A two-target extension of the fixed-order lattice-transfer
argument resolves the average-source prevalence question: products of
empirical factorial moments concentrate, yielding a
quenched Poisson(1) fiber law. Thus singleton and doubleton residues occupy
asymptotically positive fractions with high probability over random public
labels. Generic direct QSVT is now blocked on the average-source contract; this
still does not cover source-aware encodings, preconditioners, or collision
walks.

Coherent fiber erasure now has an explicit access boundary. The tight
square-root black-box lower bound for non-coherent index erasure is retained as
a generic state-generation baseline, but it is not transferred to public
arithmetic subset-sum maps. Conversely, a target-addressable flagged
normalized-fiber preparer would decide support, and fixed-variable stability
would yield witness search. A global collective PGM channel that never exposes
that interface remains open and must be audited directly on independent DCP
state input.

The apparent global coherent-erasure escape is also conditional on solving the
hard primitive. Erasure before a cyclic QFT must leave target-independent
garbage or it dephases the target register. With common preparable garbage the
erasure circuit is invertible into normalized-fiber preparation. The quenched
support law gives `q_s <= (D/L) pi_s` with
`D/L -> 1/(1-e^-1)`, so source-weighted average fidelity transfers to
uniform-legal targets at constant loss. Measuring and verifying then yields an
average subset-sum witness solver. Arbitrary full-rank POVMs without an
erasure-plus-QFT factorization remain open.

Target-dependent garbage does not rescue an exact erasure factorization. Its
relative QFT success is
`R = ||sum_s sqrt(c_s)/Z |g_s>||^2`. The same weighted mean garbage state is
preparable from the public zero-frequency input. Jensen plus a multiplicity
truncation gives uniform-legal inverse fidelity at least `(L/D)R^2/4`.
Therefore every inverse-polynomial-success exact erasure-plus-QFT decoder is
already an inverse-polynomial average witness solver. Approximate-isometry
perturbation bounds and arbitrary non-erasure POVMs remain open.

Uniform operator-norm approximation does not reopen erasure. If relative
decoding success is `R` and legal support fraction is at least `rho`, error
`delta <= rho^2 R^(5/2)/128` preserves polynomial reference preparation and
`Omega(rho R^2)` witness success. For `R=1/poly(n)`, this is still only
inverse-polynomial circuit precision. The remaining approximation loophole is
strictly average-state channel control, not ordinary uniform circuit
approximation.

Marker awareness is now formalized as an exact reduction. The relation vectors
form the marker-zero kernel and witnesses live in its marker-one affine coset.
With constraint quanta above `sqrt(m+1)`, finding a marker-one vector at radius
`sqrt(m+1)` is equivalent to finding a binary subset-sum witness. Marker gcd
normalization is polynomial but has no norm guarantee, so filtering or Bezout
normalization is not a decoder; a surviving route needs a genuine affine-CVP
algorithm with legal source coverage.

The first marker-aware classical attack is implemented directly in that affine
coset. It LLL-reduces the marker-zero kernel and runs exact-rational Babai
nearest plane against the target row, both before and after carry slicing. Every
candidate is checked against the original equation, and radius, constraint, and
binary defects are retained. Its finite results are diagnostics only; there is
still no source-conditioned BDD-radius or inverse-polynomial coverage theorem.

The affine attack also has a larger-scale source-native audit. It keeps labels
and targets independent and uniform, computes exact legality for every failed
and successful run by meet in the middle, and scales standard/carry nearest
plane beyond truth-table sizes. Persistent success is treated as a classical
dequantization attack; collapse is treated as a falsifier. Neither is promoted
to a coverage theorem from finite rows.

Nearest-plane behavior is also audited at the mechanism level. Exact
meet-in-the-middle witness enumeration supplies every tractable witness; its
`+/-1` zero-constraint error is tested against the exact Gram-Schmidt Babai
cell of the reduced marker kernel. The stronger global BDD condition is tracked
separately. This explains finite recovery without mistaking cell frequencies
for a source-distribution theorem.

Run the coset-state/nonabelian HSP workbench:

```bash
python qsearch.py coset-state
```

Run adversarial collective-observable search on CFI and graph-isomorphism
boundary pairs:

```bash
python qsearch.py collective-observables --verbose
```

Audit graphlet/homomorphism tensor observables against classical small-pattern
count shadows:

```bash
python qsearch.py tensor-observables --verbose
```

Search Godsil-McKay switched cospectral graph rows and immediately attack them:

```bash
python qsearch.py gm-switching --verbose
```

Probe CFI parity scaling boundaries:

```bash
python qsearch.py cfi-scaling --verbose
```

Search CFI parity twists over non-complete base families:

```bash
python qsearch.py cfi-base-search --verbose
```

Run the promised complete-CFI gadget parity decoder baseline:

```bash
python qsearch.py cfi-parity-solver --verbose
```

Run the promised regular-CFI gadget structural decoder across non-complete bases:

```bash
python qsearch.py cfi-structural-decoder --verbose
```

Run the promised degree-separated irregular-CFI gadget structural decoder:

```bash
python qsearch.py cfi-irregular-decoder --verbose
```

Run the bipartition-based CFI structural decoder, including non-degree-separated stress rows:

```bash
python qsearch.py cfi-bipartite-decoder --verbose
```

Certify the faithful CFI graph-to-binary-code equivalence reduction, recover
graphs from scrambled explicit generators, and run every legal graph-side
decoder. This command treats graph recovery as a reduction back to GI, not as
a GI solution or quantum signal:

```bash
python qsearch.py cfi-code-reduction --verbose
```

Audit random binary code-equivalence instances against the source-linked
trivial-hull projector reduction to weighted graph isomorphism:

```bash
python qsearch.py code-hull-projector --verbose
```

This command samples hull dimensions without conditioning, certifies the
basis-independent projector `G^T (G G^T)^(-1) G`, verifies planted coordinate
permutations and independent nulls, and records the access-model boundary. A
successful projector/GI match rejects independent code-native hardness; it is
not a polynomial-time graph-isomorphism result. Nontrivial-hull rows remain
open only after charging the source hull-parameterized shortening bound and
proving an asymptotic growing-hull law.

Run individualization-refinement WL graph baselines:

```bash
python qsearch.py individualized-wl --verbose
```

Run individualized rooted tensor-shadow baselines:

```bash
python qsearch.py individualized-tensors --verbose
```

Aggregate coset frontier rows across all current classical baselines:

```bash
python qsearch.py coset-triage --verbose
```

Audit symmetric-group representation growth and strong-Fourier no-go pressure:

```bash
python qsearch.py representation-obstructions --verbose
```

Audit weak Fourier irrep-label signal for symmetric involution hidden subgroups:

```bash
python qsearch.py weak-fourier --verbose
```

Audit multi-copy distinguishability obligations for involution coset states:

```bash
python qsearch.py coset-distinguishability --verbose
```

Audit PGM copy/capacity obligations and explicit-measurement proof debt:

```bash
python qsearch.py coset-pgm --verbose
python qsearch.py coset-holevo --verbose
python qsearch.py coset-covariant-frame
python qsearch.py coset-two-copy-frame
python qsearch.py coset-same-hidden-target-law
python qsearch.py coset-commutant-information-no-go
python qsearch.py coset-carrier-information
python qsearch.py coset-strong-fourier-information
python qsearch.py coset-entanglement-width
python qsearch.py coset-growing-width-architecture
python qsearch.py coset-two-copy-transitions
python qsearch.py coset-three-copy-recoupling
python qsearch.py coset-jm-labels
python qsearch.py coset-multiplicity-commutant
python qsearch.py coset-recoupling-capabilities
python qsearch.py coset-recoupling-synthesize
```

The Holevo audit derives the exact one-copy information from symmetric-group
character ratios and applies entropy subadditivity plus Fano's inequality to
every same-hidden multi-copy proposal. It rejects under-sampled mechanisms,
but the resulting hard-family requirement is only `Omega(n log n)` copies and
therefore does not replace the missing collective measurement or decoder.

The two-copy audit computes exact Murnaghan-Nakayama characters and Kronecker-sector frame spectra, but explicitly
rejects the false shortcut from frame support rank to mixed-state PGM success. Its `S_3` regular-representation control
records the nonzero state/frame commutator; cross-sector transition coefficients, a coherent recoupling transform, and
a compressed hidden-involution decoder remain proof obligations.

The shared-hidden target-law audit converts that frame scalar into the exact
operational distribution
`p(nu|lambda,mu)=[g d_nu/(d_lambda d_mu)]`
`[1+r_lambda+r_mu+r_nu]/[(1+r_lambda)(1+r_mu)]`.
All eight finite controls through `n=10` normalize exactly and match the
two-copy frame identity.  The correction from dimension-weighted coupling has
expected total variation as high as `0.0978`; the known `n=6` scalar blocks
carry `0.9877%` true joint target mass, versus `2.469%` source-pair mass.  This
closes target-frequency accounting, not coherent recoupling or decoding:
coupled target labels are conjugacy-class invariant and cannot identify the
individual hidden involution.

The commutant-information theorem makes that limitation exact for every copy
count.  If every final POVM effect commutes with the diagonal group action,
its outcome distribution is identical for all hidden involutions in the
conjugacy class, hence `I(H;Y)=0`.  This covers target shapes, intermediate
coupling shapes, multiplicity commutant observables, and Racah labels when
measured alone.  A nontrivial `S_5` multiplicity control verifies invariance of
the full separator spectra across all 15 hidden involutions.  The route is not
discarded, but its role changes: commutant/Racah machinery may preprocess the
state only if carrier registers survive to a carrier-sensitive covariant
measurement with a proved decoder.

The first carrier-sensitive search changes the optimization metric from
spectral gap to `I(H;Y)` and one-shot Bayes recovery.  It exhausts all 1,744
parity-complete coefficient rules on nontrivial `S_5` and `S_6` controls.
Joint YJM-plus-separator outcomes do add information over YJM alone, but the
best values are only about `0.253` and `0.109` bits; direct product Young-basis
strong Fourier outcomes give about `0.446` and `0.748` bits.  Every searched
refinement is therefore dominated by a simpler quantum baseline.  Future
observable search must beat strong Fourier on frozen holdouts before gap or
circuit work receives priority.

The natural strong-Fourier baseline removes the selected-source conditioning.
It enumerates every near/fixed-point-free hidden involution and every natural
source/tableau outcome through `S_8`.  Weak labels have exactly zero
hidden-element information within one conjugacy class.  Young-basis carrier
information drops to about `0.0785` bits at `n=6` and `0.0244` bits at `n=8`,
although the one-copy Holevo bound stays near one bit; two separate samples
are nearly additive.  This finite trend is not an asymptotic theorem, but it
sets the correct target: a collective covariant carrier measurement must
extract substantially more of the available Holevo information under natural
source weighting.

The literature-backed width gate then applies the known architecture lower
bound: single-register strong Fourier sampling fails even with an arbitrary
POVM, and nonnegligible information for the GI-relevant hidden involution
requires a measurement entangled across `Omega(n log n)` coset states.  The
current 11 frame, transition, separator, carrier, and Racah mechanisms have
joint width at most three.  They are now explicitly classified as local
primitives.  Progress requires a uniform growing-copy associator/measurement
network, compressed covariant outcomes, and a decoder; collecting many copies
and measuring them separately does not meet this gate.

The growing-width architecture compiler makes the replacement machine
checkable.  It verifies balanced merge schedules for
`k=ceil(n log2 n)`, carrier preservation, natural source access, intermediate
and final effect algebras, outcome compression, information, decoding, and
classical comparison.  Separate strong Fourier and bounded Racah-label designs
are structurally rejected.  One balanced carrier-preserving covariant skeleton
survives, but it has no proved growing associator circuit, state-dependent
POVM, compressed outcome, information theorem, decoder, or classical
separation.  It is a typed research target, not an algorithm.

The transition audit verifies the character-theoretic spectrum against explicit regular `S_3`/`S_4` matrices and
reconstructs mixed-state PGM success from cross-eigenspace transition weights. It records the commuting Klein-four
class as an exceptional control and rejects the general explicit construction because it materializes `|S_n|^4`
dense entries.

The three-copy audit proves an asymptotic obstruction in the standard representation: for the transposition class,
`[K_12,K_23]_(000,001)=n` for every `n>=3`. Thus one pairwise Kronecker basis cannot diagonalize the overlapping
subset terms. This does not rule out a collective algorithm; it makes a uniform coherent Racah/associator transform
and a polynomial multiplicity-space decoder mandatory.

The diagonal Young--Jucys--Murphy audit splits the formerly monolithic internal
Kronecker bottleneck. It verifies the seminormal Coxeter relations, commuting
diagonal YJM operators, and complete content-vector spectrum against exact
Kronecker coefficients. Under the known `S_n` QFT, reversible group action,
and standard block-encoding primitives, target tableau labels have a polynomial
measurement contract. That result is label-only: the YJM algebra is exactly
degenerate on each `g(lambda,mu,nu)` multiplicity register. The coherent
multiplicity basis, Racah moves, transition filter, and hidden-involution
decoder remain separate blocked obligations.

The multiplicity-commutant search then acts inside that residual register. It
constructs simultaneous-conjugacy orbit sums with at most `O(n^5)` terms and
searches small-integer Hermitian combinations after charging the full LCU
normalization. The current combination splits every audited multiplicity block
through `S_7`, including all 224 nontrivial tableau-labeled blocks of the
maximum-dimension `(4,2,1)` self-product and multiplicity nine. All four
original generators are pairwise noncommuting there. Adding the support-three
shared-transposition generator yields four coefficient rules that split every
audited block at `n=5,6,7`; the best finite rule is `H=TC2-2 TT1`, with minimum
charged normalized gap about `2.68e-3`. The naive sum `TC2+TT1` fails at `n=6,7`.
These remain finite structural witnesses rather than scalable transforms: each
single-generator extrapolation has exact scalar targets, and no all-`n` joint
gap theorem exists.

One restricted family now goes further. For
`lambda=mu=(n-2,2)` and `nu=(n-3,2,1)`, an exact 12-term Specht-polytabloid
certificate constructs the symmetric and antisymmetric multiplicity copies and
derives their eigenvalues symbolically. Their raw gap is `2(n-2)` for every
`n>=6`; after the exact `n(n-1)(n-2)` LCU normalization, the gap is
`2/[n(n-1)]`. This proves polynomial phase-estimation resolution for that label
family only. It does not prove a general internal Kronecker transform, balanced
sector coverage, a Racah network, or a hidden-involution decoder.

```bash
python qsearch.py coset-commutant-gap-scaling
python qsearch.py coset-commutant-gap-proof
```

The first three-copy Racah control uses that solved pair channel at `n=6`.
Across four final targets, the left/right parity overlap subblocks are
tableau-independent and reconstruct to small rationals, but every `2x2`
subblock is nonunitary: probability leaks into other intermediate partitions.
This rejects the shortcut from a pairwise gap to a closed associator. A valid
next construction must include all intermediate channels, produce complete
unitary Racah blocks, and avoid dense tableau enumeration.

```bash
python qsearch.py coset-racah-control
```

That next finite construction is now explicit. Pair transposition and 3-cycle
central signatures identify every intermediate partition; the first orbit
Hamiltonian resolves pair multiplicity. For the five sectors with
multiplicity-free second coupling, including every intermediate channel gives
complete signed unitary Racah matrices and exactly explains the earlier
`2x2` leakage.

A second bounded-support Hamiltonian then acts between the pair-diagonal
representation and the third copy. Its joint spectrum with the first-stage
labels resolves second-stage multiplicities up to four and completes all ten
final `S_6` sectors, including a 16-dimensional multiplicity space. This is a
complete finite table, not a uniform circuit.

```bash
python qsearch.py coset-racah-complete-control
python qsearch.py coset-racah-hierarchical-control
```

Finite scaling on `W_n=(n-2,2)` and final
`xi_n=(n-3,2,1)` splits every audited second-stage block through `n=8`.
A sparse target-block extractor extends the hardest multiplicity-four channel
through `n=11` without materializing dense Hamiltonians and reconstructs five
monic integer characteristic polynomials. The trace rows at `n=7..10` generate
the cubic target `4n^3-46n^2+149n-118`, which matches the held-out `n=11` row.
That trace target is now proved exactly for every `n>=7`: the stable characters
are expanded in falling cycle counts, 48 monomial products are reduced through
canonical partial-permutation equality patterns, and the resulting shifted
character correlation is the cubic divided by the exact orbit size. An exact
`S_7` character sum closes the endpoint. The theorem supplies only `Tr(H)`;
the same machinery now also proves
`Tr(H^2)=4n^6-92n^5+828n^4-3678n^3+8355n^2-8992n+3624`.
Fixing the first orbit term collapses the double sum to 17 relative
simultaneous-conjugacy classes. The symbolic calculation covers `n>=14`, and
exact finite pattern counts close `n=7..13`. Newton's identity therefore gives
the quartic's second coefficient exactly. The same exact engine now fixes one
term in the ordered triple sum, canonicalizes the remaining two terms as
two-colored permutation graphs, and collapses `Tr(H^3)` to 129 relative
classes. Falling-cycle patterns prove
`Tr(H^3)=4n^9-138n^8+2037n^7-16798n^6+84810n^5-270165n^4+539231n^3-646446n^2+422442n-115228`:
the symbolic proof is literal for `n>=17`, exact pattern counts close
`n=7..16`, and all five sparse quartics agree. Newton's third identity proves
the third characteristic coefficient without interpolation. The fourth-moment
pipeline compresses 27,787,968 labeled relative terms by three-support
incidence masks, reduces them to 1,628 simultaneous-conjugacy classes, and
checkpoints 20,607,987,763 exact canonical equality patterns. It proves
`Tr(H^4)` and the determinant for every `n>=7`, completing all four quartic
coefficients. The discriminant factors as `(n-2)^2 q(n)`; positivity after
`n=m+7`, an explicit discriminant lower bound, and a Cauchy root bound prove an
LCU-normalized gap of at least `1/(C*n^53)` for an explicit constant `C`.
This closes the spectral theorem in one stable multiplicity-four channel. The
ordered-triple orbit terms also give a uniform LCU block encoding, so the
proved normalized gap and coherent phase estimation append a polynomial-cost
four-valued eigenlabel in that declared channel. This does not route arbitrary
Kronecker sectors or change coupling trees. Overlapping Racah synthesis,
all-sector coverage, hidden-involution decoding, and any speedup claim remain
open.

The first transition stress test now shows why the one-channel result does not
close that gap. For `n=7..10`, sparse Coxeter-Laplacian nullspaces construct the
`2 x 4 = 8` stable intertwiner branch on both coupling trees. The
basis-independent quantity `Tr(P_left P_right)/8` falls from about `0.350` to
`0.339`, so roughly two thirds of a maximally mixed stable branch leaks into
complementary intermediate sectors. The retained `8 x 8` overlap is full rank
but increasingly ill-conditioned. This is finite scaling evidence, not an
all-`n` leakage theorem; it cuts the single-channel associator direction and
makes complementary-sector classification the next proof target.

That classification is now complete numerically at `n=7,8`. The projector
contributions sum to rank eight within `6.4e-14` and `3.6e-15`. Every
character-allowed complementary partition has nonzero support: seven sectors
at `n=7` and eight stable-shape sectors at `n=8`. The largest sector captures
only `26.3%` of leaked mass, with effective support over more than six sectors.
This refutes a one-complement repair but also reveals a bounded nine-shape
stable family for the audited final irrep. The next constructive target is one
exact transition formula and one coherent gapped label primitive for each
shape, not unrestricted partition enumeration.

The bounded shape list is now exact rather than an extrapolation. Full-rank
irreducible character-polynomial witnesses and factorial cycle moments prove
the nine first/second multiplicity pairs for every `n>=9`; direct characters
close `n=8`. Independently, `E[chi_W^3 chi_xi]=25`, exactly equal to the sum of
the nine branch dimensions, so no omitted positive intermediate sector can
exist. Seven shapes have nontrivial second-stage multiplicity and only the
`(n-3,2,1)` shape currently has a coherent normalized-gap label, leaving six
specific operator families rather than an undefined all-partition problem.

The first shape-resolved operator pass supplies a common target for all six.
At `n=8,9,10`, the same support-intersection-two transposition/three-cycle
orbit Hamiltonian splits every one of the 21 audited nontrivial blocks. Every
restricted characteristic polynomial reconstructs to integer coefficients,
and the smallest observed LCU-normalized gap among the six open shapes is
positive. This is useful compression of the proof search, not a new theorem:
the six exact all-`n` characteristic polynomials, normalized root gaps, and
coherent LCU implementations remain unproved, as do the coupling-tree
transition and hidden-involution decoder.

The first exact coefficient pass is now complete across the family. Each
stable character polynomial is converted to falling cycle counts, and exact
partial-permutation equality patterns evaluate
`n(n-1)(n-2) E[chi_xi(g) chi_eta(g tau) chi_W(g c)]`. Direct `S_8` character
sums close the only symbolic endpoint. This proves all nine trace polynomials,
including the first characteristic coefficient for all six open nontrivial
shapes, with 27/27 agreement against the `n=8,9,10` sparse blocks. Five
multiplicity-two determinants and two higher multiplicity-three coefficients
remain before complete shape spectra can be claimed.

The second-moment pass closes almost all of that debt. The 17 relative
simultaneous-conjugacy classes for `H^2` are reused with each shape character;
53 exact low-`n` endpoint checks bridge the symbolic stability ranges and all
21 independent sparse second coefficients agree. Newton's identity therefore
proves the complete quadratic characteristic polynomial for each of the five
open multiplicity-two shapes. Only the determinant of the multiplicity-three
`(n-4,3,1)` shape remains before all nine stable-shape spectra are exact.
Normalized discriminant/root-gap bounds and coherent circuits are still open.

That final determinant is now exact as well. The third-moment calculation
classifies 18,144 relative term types into 129 simultaneous-conjugacy classes
and compresses 2,212,218,888 raw canonical marked assignments to 4,493 nonzero
rational coefficients. Exact counts close `n=8..16`; the stable symbolic sum
proves the degree-nine determinant from `n>=17`, and all three sparse
determinants agree. All nine stable-shape characteristic polynomials are now
exact. This is a structural representation-theory result, not an algorithmic
breakthrough: six normalized gap families, coherent common-orbit compilation,
left/right transition synthesis, hidden-involution decoding, and classical
separation remain open.

Five of the six remaining gap families are now closed exactly. For every
multiplicity-two complementary shape, the discriminant becomes a polynomial
with nonnegative coefficients after `n=m+8` and has a positive constant term.
The smallest raw-gap lower bound is `12`; dividing by the exact
`n(n-1)(n-2)` orbit normalization proves a uniform normalized gap of at least
`12/n^3` for all five. The multiplicity-three cubic root separation is the
only remaining stable-shape spectral gap obligation.

The cubic gap is now closed too. Its discriminant is
`4(n-2)^3(621n^3-4266n^2+9612n-7192)` and has strictly positive shifted
coefficients at `n=m+8`. A coefficient-L1 Cauchy bound places every root in
`[-903473 n^9, 903473 n^9]`; the discriminant product then gives a raw gap at
least `1/(3265053846916 n^18)` and an LCU-normalized gap at least
`1/(3265053846916 n^21)`. All seven nontrivial stable-shape gap families are
therefore exact. The next bottleneck is no longer spectral: it is coherent
common-orbit compilation, complete coupling-tree transitions, and a decoder.

The common-orbit compilation is now proved at the shape-local interface. A
single reversible ordered-triple PREPARE and shape-controlled Young-basis
SELECT block-encode `H_eta` with normalization `n(n-1)(n-2)` for every fixed
stable shape. Combining that circuit with the seven exact gaps gives coherent
multiplicity eigenlabels of dimensions two, three, or four on all nontrivial
shapes. This theorem assumes the state is already routed into a declared
`eta tensor W -> xi` channel. Coherent channel routing and the complete
left/right coupling-tree transition are still missing, so this is not yet a
Racah associator or decoder.

The first-stage multiplicity gap is now closed as well. In the nine-shape
family, only `W_n` and `xi_n` occur with first-stage multiplicity two. The
`xi_n` block uses the existing exact parity gap `2(n-2)`. For the missing
`W_n` block, exact marked-cycle moments give
`Tr(H)=2n^3-19n^2+51n-36` and
`Tr(H^2)=2n^6-38n^5+283n^4-1048n^3+2021n^2-1904n+688`.
The resulting discriminant is
`n^4-14n^3+73n^2-136n+80`; after `n=m+6` its coefficients are
`[1,10,37,92,164]`, proving a normalized gap above `12/n^3`. Thus all
nine first-stage multiplicities are resolved in the original tensor-register
encoding. A commuting intermediate-shape router and left/right transition are
still required.

The intermediate-shape router is now exact. On the final-`xi_n` branch, the
pair transposition class sum has eigenvalue `sum content(u)` and the pair
3-cycle class sum has eigenvalue
`sum content(u)^2-binomial(n,2)`. An all-36-pair symbolic gcd audit proves
that their joint signatures never collide for `n>=8`; all common collision
points are at most `n=6`. Both class sums have polynomial LCU descriptions and
integer raw gaps, so coherent phase estimation appends a nine-valued shape
label while leaving the state in the original `W_n tensor W_n` encoding. This
is encoded routing, not a compressed Clebsch isometry. The next obligation is
to compose shape, first-stage, and second-stage labels and test whether their
left/right versions provide the transition interface needed by a decoder.

That composition is now proved on the stable final branch. Pair central sums,
the first-stage commutant Hamiltonian, and the pair/third-factor orbit
Hamiltonian commute algebraically; a finite operator audit confirms all six
pairwise commutators below `6e-17`. Their branchwise label products sum to
exactly 25, the known final multiplicity, so the left and mirrored right trees
both have complete coherent encoded labels. The circuit
`T_encoded = U_R U_L^dagger` coherently changes those label interfaces with
maximum inverse-gap exponent 53. It leaves the physical state encoded in
`W_n^tensor3`: no compressed 25-by-25 Racah table is materialized. The direct
frame block encoding and the all-`n` conditioning certificate now supply the
needed inverse filter on this branch; the active bottleneck is demonstrating
that its outcomes reveal the hidden involution beyond classical character or
tensor contractions.

The stable three-copy average frame no longer requires an explicit Racah
matrix. After conditioning on three `W_n` labels and final `xi_n`, it is
exactly
`F=(1+3r_W+r_xi)I+A_12+A_13+A_23`, where each `A_ij` is the normalized
involution class sum on one pair. Uniform involutions with `t` disjoint
transpositions have a polynomial reversible rank/unrank construction, so all
three terms admit direct LCU block encodings on the physical registers. At
`n=8`, all three audited classes have full rank on the 25-dimensional stable
multiplicity block; the two frontier condition numbers are at most `1.599`.
The finite pattern now has an exact all-`n` proof. Each pair operator has the
nine stable character ratios `r_eta` as its spectrum, so Weyl's inequality
gives `lambda_min(F)>=min_eta(1+3r_W+r_xi+3r_eta)`. Substituting the exact
character polynomials and splitting `t=floor(n/4)` and `t=floor(n/2)` by
residue class produces 54 shifted rational functions with nonnegative
numerator and denominator coefficients and positive constants. This proves
`lambda_min(F)>=(71/825)/n^5` for every `n>=8` in both families. Combined with
the direct frame block encoding, it gives polynomial QSVT inverse-square-root
filters. This closes internal conditioning but does not establish that the
conditioned branch is naturally reachable or that its outcomes contain
reconstructible information about the hidden involution.

The first access calculation falsifies this fixed branch as an end-to-end
route. From three natural involution coset states, the exact probability of
the three `W_n` labels and final `xi_n` projection is
`d_W^3*d_xi*Tr(F)/(n!)^3`. Since `Tr(F)<=200`,
`d_W<=n^2/2`, and `d_xi<=n^3/3`, this is at most
`(25/3)n^9/(n!)^3`, or `exp(-Theta(n log n))`. Passive postselection and
generic amplitude amplification are both superpolynomial. The solved stable
branch is therefore quarantined as a mechanism/proof control, not algorithmic
evidence. The representation frontier must now transfer these observables to
typical high-dimensional Fourier labels with nonnegligible natural mass, or
prove a genuinely new direct conditioned-state preparation theorem.

This obstruction extends beyond `W_n`: for every fixed tail budget `K`, the
entire family of partitions `(n-|tau|,tau)` with `|tau|<=K` has weak-Fourier
probability at most `2*P_K*n^(2K)/n!`. Thus no predetermined stable
character-polynomial family is naturally accessible. The typical-irrep audit
uses maximum-Plancherel source partitions as finite controls. By `n=20`, their
self-Kronecker product supports 626 of 627 targets, has maximum multiplicity
6,408,361, needs 148 targets for 90% of coupling mass, and assigns only
`2.60e-10` mass to all targets with tail size at most four. These are not
hardness theorems; they specify the new architecture requirement: every
commutant, recoupling, frame, and decoder operation must be uniform in the bit
description of naturally sampled high-dimensional partitions.

The first character-only transfer test now avoids constructing the enormous
representation matrices. Exact first and second multiplicity-space moments of
three normalized bounded-support orbit averages cover all 32 nontrivial blocks
tested at `n=7,8`. The primary transposition/3-cycle generator is exactly scalar
on two `n=8` blocks, while the portfolio repairs them. Exact mixed moments show
at least two independent traceless directions in 29 blocks; the other three
have multiplicity two, where a non-scalar Hermitian already has simple finite
spectrum. This remains only a mechanism signal: covariance rank does not prove
noncommutation, full matrix-algebra generation, an inverse-polynomial minimum
gap, an efficient uniform transform, or information about the hidden
involution. The next theorem target is an all-`n` class-algebra contraction and
joint spectral separation on Plancherel-typical labels.

The first scaling step toward that target removes factorial group enumeration
for the primary generator. Marked-support injection counts over conjugacy
classes, plus 17 relative pair types for the second moment, give exact results
through `n=10` in `O(p(n)n^6)` finite-evaluator work. They find seven scalar
blocks across `n=6,8,9,10`, despite complete primary-generator splitting at
`n=7`. The one-generator conjecture is therefore falsified. Extending the same
contraction to a second support-three generator and their exact mixed moment
covers every audited block through `n=10` with no common scalar action. The
second generator has its own scalar hook targets, so neither works alone.
Finite covariance rank and non-scalar coverage still do not prove
noncommutation, matrix-algebra generation, simple joint spectrum, or a gap.
Higher mixed moments or commutator norms and an all-`n` joint-separation theorem
are now the representation-theory target; the evaluator itself is not a circuit.

The first higher-moment collision test rejects that two-generator span. On the
two multiplicity-four `n=8` targets where `TC2=0`, exact TT1 traces through
order four give characteristic polynomials
`x^2(504x^2-21x-1)/504` and `x^2(504x^2+21x-1)/504`. Every linear combination
of `TC2` and `TT1` therefore retains a repeated eigenvalue. All four coefficient
rules that split `n<=7` are dead at `n=8`; any surviving portfolio needs at
least a third independent generator and must repeat the collision test before
gap scaling. The first extension also fails symbolically: for
`TT1+c*TTdisjoint`, both characteristic polynomials contain
`(105x +/- 2c)^2` for every `c`. Because `TC2=0` on these targets, the whole
three-generator span remains degenerate. The next admissible test is the
genuinely different `TC-intersection-one` generator, not another coefficient
fit inside the rejected span. That test now survives on both known collision
blocks: exact fourth moments show the discriminant of `TT1+c*TC1` is positive
for every real `c != 0`. This repairs the two finite collisions but does not
establish a common coefficient across all targets, an all-`n` theorem, a
normalized gap, a coherent transform, or a decoder. An exact
simultaneous-conjugacy transfer kernel now evaluates the fixed coefficient
`c=1` through degree 17 with arbitrary-precision weights and finds square-free
characteristic polynomials on all 20 nontrivial `n=8` targets. This closes the
finite `n=8` collision audit. The next falsification frontier is `n=9`,
coefficient perturbations, and normalized gap decay.

Exact rational root isolation also certifies that the minimum raw `n=8` block
gap exceeds `0.002500834486`; after the two-term LCU normalization, the lower
bound is half that value. Dense maximum-dimension controls at `n=5,6,7` split
every block as well. The finite gaps decline sharply, so the four-size trend is
recorded only as a falsification target, not as an inverse-polynomial claim.

The first adjacent-size probe compiles the quotient transfer for `S_9` and
contracts characters directly because the dimension-216 source is not
self-conjugate. At `c=1`, exact transfer through degree 28 proves all 27
nontrivial targets have square-free characteristic polynomials. The global raw
gap lower bound is `0.0004291729185`; after two-term LCU normalization it is
below `0.000215`. This closes the finite `n=9` collision audit, not the
asymptotic algorithm.

The transfer kernel uses parallel local-map accumulation and a kernel-hash-gated
exact TSV cache. A class-Fourier contraction orders `S_9` rows by its 30
conjugacy classes, scans each translation pair once, and amortizes all 27 target
characters. The exact table still occupies 7.81 GB on disk, while fixed 128-row
chunks cap character slices near 93 MB. An all-`n` class-algebra recurrence,
inverse-polynomial normalized gap, coherent transform, outcome law, and decoder
remain open.

The first `n=10` feasibility probe uses the self-conjugate
`(4,3,2,1)` source. Both multiplicity-three conjugate targets have exact
square-free cubics, but this is only `2/40` target coverage. Quotient transfer
reaches 310,071 states by degree five, and the direct class-ordered `S_10`
translation table would require 91.7 GB. Higher multiplicities are blocked
until a scalable representation- or class-algebra contraction is proved.

Exact support profiles close one tempting shortcut: full-support pair orbits
carry 89.5% of the `n=9` degree-28 transfer weight, and support 9 or 10 carries
62.0% at `n=10` degree five. Termwise marked-support injection therefore
degenerates to factorial work on the dominant sector. A separate sparse
invariant-space contraction removes explicit group rows for finite blocks:
on diagonal-`S_n` invariant tensors an orbit average restricts exactly like one
representative. A diagonal Jucys-Murphy content penalty then isolates one target
tableau fiber directly in `V_lambda tensor V_lambda`, removing the
`dim(nu)` factor from the eigensolve. It reproduces the exact `n=10` cubic
traces, but `dim(lambda)^2` is still exponential for typical partitions; this
is a finite collision finder, not a scalable multiplicity transform.

An exact follow-up replaces numerical multiplicity moments with a diagonal
YJM tableau projector. The identity
`Tr(P_T H^d) = Tr(M_nu^d)` follows from the diagonal isotypic decomposition and
the simple joint content spectrum. Rational `n=5,6` controls recover exact
square-free quadratics. The literal evaluator is decisively non-scalable:
degree two at `n=6` reaches 484,912 of 518,400 pair-group states, while the
`n=10` pair space has 13,168,189,440,000 states. The live target is therefore
a Young-tower or centralizer recurrence for these exact traces, not further
explicit group-algebra expansion.

The first exact compressed evaluator now uses Young's rational seminormal form
over finite fields. An explicit polynomial in the integer-valued YJM content
penalty projects onto one multiplicity fiber, rational Gram weights propagate
it through the target tableaux, and modular traces match both exact controls.
For the `n=10` multiplicity-six target this replaces 13.17 trillion pair-group
states with 589,824 tensor coordinates, a 22,325,625-fold finite reduction.
An exact `F_1009` run projects rank six on six independent trials and produces
the residue polynomial
`x^6 + 621x^5 + 659x^4 + 130x^3 + 549x^2 + 650x + 558`, whose gcd with its
derivative is one. Because 1009 is a good reduction prime, this proves the
rational `n=10` multiplicity-six polynomial is square-free. It is still
exponential in `n`; rational coefficient reconstruction, asymptotic
compression, a coherent transform, and a decoder remain open.

The conjugate target `(2,2,2,2,2)` was computed independently and gives the
same polynomial with every odd coefficient negated. This validates an all-`n`
sign-duality theorem for this separator: the source is self-conjugate, twisting
one source factor maps `nu` to `nu'`, and every separator term has an odd left
transposition, so the conjugate block is similar to the negative block.
Square-freeness and absolute gaps therefore transfer exactly to conjugate
targets, cutting the remaining finite ladder in half.

The next primary target `(8,2)` has multiplicity eight. Its exact
`F_1009` polynomial is also square-free, so sign duality certifies the
conjugate target as well. The multiplicity-nine `(8,1,1)` block and both
multiplicity-fifteen primaries `(6,4)` and `(7,3)` also have exact square-free
good reductions. Sign duality raises modular coverage to ten of 40 targets
through multiplicity fifteen; including the older exact cubic pair gives
twelve total. This remains a collision search, not evidence for polynomial
scaling.

Exact denominator clearing makes that distinction quantitative. Combining the
YJM projector denominator, orbit-average denominators, Newton identities, and
the nonzero integer discriminant gives rigorous normalized gap lower bounds.
They are unusably weak: the strongest audited bound is below `10^-2057`, and
the multiplicity-fifteen bounds fall below `10^-21000`. These are safe
existence bounds, not observed gaps, but they prove that finite
square-freeness alone cannot justify efficient phase estimation.

A direct sparse YJM eigensolve supplies the first real-gap trend on exact
blocks. The multiplicity-six LCU-normalized gap is about `0.00299417`; at
multiplicity eight it is about `0.000417600`, a 7.17-fold drop. Both blocks are
exactly square-free, and both numerical gaps survive a declared error budget,
but neither magnitude has a machine-verified interval certificate. This is a
finite warning against stable precision, not an asymptotic gap-collapse proof.

Natural-input coverage is an even stronger blocker than the finite gap trend.
Aggarwal and Elboim's 2026 maximal-dimension theorem
([arXiv:2605.25995](https://arxiv.org/abs/2605.25995)) implies that the largest
`S_n` Plancherel atom is `exp(-Theta(sqrt(n)))`. Involution weak-Fourier atoms
are at most twice as large, so any polynomial catalog of pre-certified source
partitions has superpolynomially small natural mass. Exact coupling accounting
also shows that the current 12-target `n=10` ladder covers only about `1.14%`
of the selected source's dimension-weighted Kronecker target mass; the
unresolved source-shaped
multiplicity-117 block alone carries about `15.23%`. Further one-source finite
ladder work is therefore mechanism control, not algorithmic coverage. The next
valid target is a partition-description-uniform separator, gap theorem, and
coherent transform on arbitrary sampled typical labels.

The first all-source test falsifies the fixed-coefficient version of that
idea. Exact unequal-source character moments audit every ordered source pair
at `n=5,6`. At `n=6`, `TT1+TC1` is exactly scalar on the nontrivial
`(3,2,1) tensor (3,3) -> (3,2,1)` and
`(3,2,1) tensor (2,2,2) -> (3,2,1)` multiplicity-two blocks. A third
multiplicity-four block has a numerical repeated zero root. These source pairs
have nonzero natural fixed-point-free-involution label mass. The fixed
separator is therefore retired as a uniform resolver; the next admissible
search is a reversible partition-dependent coefficient rule over a larger
bounded-support commutant portfolio.

```bash
python qsearch.py coset-racah-gap-scaling
python qsearch.py coset-racah-sparse-gap --n-values 7,8,9,10,11
python qsearch.py coset-racah-trace-conjecture
python qsearch.py coset-racah-trace-proof
python qsearch.py coset-racah-second-moment-proof
python qsearch.py coset-racah-third-moment-proof
python qsearch.py coset-racah-fourth-moment-proof
python qsearch.py coset-racah-root-separation-proof
python qsearch.py coset-racah-coherent-label-proof
python qsearch.py coset-racah-stable-transition --n-values 7,8,9,10
python qsearch.py coset-racah-complementary-sectors --n-values 7,8
python qsearch.py coset-racah-stable-shape-proof
python qsearch.py coset-racah-stable-shape-labels --n-values 8,9,10
python qsearch.py coset-racah-stable-shape-traces
python qsearch.py coset-racah-stable-shape-second-moments
python qsearch.py coset-racah-stable-shape-cubic-determinant
python qsearch.py coset-racah-stable-shape-quadratic-gaps
python qsearch.py coset-racah-stable-shape-cubic-gap
python qsearch.py coset-racah-stable-shape-coherent-labels
python qsearch.py coset-racah-stable-first-stage-labels
python qsearch.py coset-racah-stable-shape-router
python qsearch.py coset-racah-stable-encoded-tree
python qsearch.py coset-racah-stable-three-copy-frame
python qsearch.py coset-racah-stable-three-copy-frame-conditioning
python qsearch.py coset-racah-stable-branch-access
python qsearch.py coset-racah-typical-irrep-transfer
python qsearch.py coset-racah-typical-commutant-moments
python qsearch.py coset-racah-typical-class-contraction
python qsearch.py coset-racah-typical-portfolio-collision
python qsearch.py coset-racah-typical-third-generator
python qsearch.py coset-racah-typical-high-multiplicity --recompute
python qsearch.py coset-racah-typical-separator-gaps
python qsearch.py coset-racah-typical-n9-probe --recompute
python qsearch.py coset-racah-typical-n9-full
python qsearch.py coset-racah-typical-n10-feasibility
python qsearch.py coset-racah-typical-support-growth
python qsearch.py coset-racah-typical-invariant-contraction
python qsearch.py coset-racah-typical-yjm-projector
python qsearch.py coset-racah-typical-modular-yjm
python qsearch.py coset-racah-typical-modular-gaps
python qsearch.py coset-racah-typical-n10-gap-trend
python qsearch.py coset-racah-typical-source-coverage
python qsearch.py coset-racah-typical-uniform-sources
python qsearch.py coset-racah-typical-parity-separator
python qsearch.py coset-racah-typical-parity-holdout
python qsearch.py run EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT
python qsearch.py run EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING
python qsearch.py run EXP-COSET-TYPICAL-PORTFOLIO-COLLISION-CERTIFICATE
python qsearch.py run EXP-COSET-TYPICAL-INDEPENDENT-THIRD-GENERATOR-CERTIFICATE
python qsearch.py run EXP-COSET-TYPICAL-HIGH-MULTIPLICITY-TRANSFER
python qsearch.py run EXP-COSET-TYPICAL-FIXED-SEPARATOR-GAP-SCALING
python qsearch.py run EXP-COSET-TYPICAL-N9-LOW-MULTIPLICITY-PROBE
python qsearch.py run EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH
python qsearch.py run EXP-COSET-TYPICAL-INVARIANT-CONTRACTION
python qsearch.py run EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE
python qsearch.py run EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION
python qsearch.py run EXP-COSET-TYPICAL-MODULAR-GAP-BOUND
python qsearch.py run EXP-COSET-TYPICAL-N10-GAP-TREND
python qsearch.py run EXP-COSET-TYPICAL-SOURCE-COVERAGE
python qsearch.py run EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE
python qsearch.py run EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR
python qsearch.py run EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION
python qsearch.py run EXP-COSET-SAME-HIDDEN-TARGET-LAW
python qsearch.py run EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION
python qsearch.py run EXP-COSET-CARRIER-INFORMATION-AUDIT
python qsearch.py coset-natural-multicopy-pgm
python qsearch.py run EXP-COSET-NATURAL-MULTICOPY-PGM
python qsearch.py coset-pgm-gain-localization
python qsearch.py run EXP-COSET-PGM-GAIN-LOCALIZATION
python qsearch.py coset-pgm-average-frame
python qsearch.py run EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING
python qsearch.py coset-character-ratios
python qsearch.py run EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION
python qsearch.py coset-projector-subpovm
python qsearch.py run EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM
python qsearch.py code-wreath-projector-subpovm
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM
python qsearch.py code-wreath-subpovm-moments
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS
python qsearch.py run EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING
python qsearch.py run EXP-COSET-ENTANGLEMENT-WIDTH-GATE
python qsearch.py run EXP-COSET-GROWING-WIDTH-ARCHITECTURE
```

The natural-source audit is a hard correction to the earlier
maximum-dimension self-pair studies.  At `n=10`, the exact targets already in
the registry cover only about `1.14%` of the dimension-weighted Kronecker
coupling reference; this reference is not the same-hidden-involution outcome
law.  An exact all-source audit at `n=5,6` then finds two multiplicity-two
blocks on which the fixed `TT1+TC1` separator is scalar.  Their source pairs
carry about `2.47%` of the fixed-point-free-involution weak-Fourier source-pair
mass, so the old fixed rule is not a uniform typical-sector resolver.

The parity-complete search adds the tensor-swapped `CT0,CT1,CT2` orientations.
It exhausts 1,744 primitive support-at-most-three integer rules over all 663
ordered-source nontrivial blocks at `n=5,6,7`.  The frozen rule
`TC2+CT1-2CT2` has no numerical collision there and a minimum raw gap of about
`0.00948`; exact rational character moments prove that it repairs the two
former scalar blocks.  The independent holdout falsifies that rule:
class-compressed exact character contractions audit all 2,483 nontrivial
ordered-source blocks at `n=8` and find 10 multiplicity-two scalar
obstructions, arranged in source-swap and sign-conjugate families.  Across
`n=5..8`, 1,608 of 1,618 multiplicity-two blocks split.  The frozen rule is
retired; fitting another small-size coefficient vector is not progress without
an all-`n` algebraic construction.  The higher-value route is a growing-width,
carrier-sensitive covariant measurement with an explicit decoder, while
bounded-support commutants remain preprocessing primitives.

The natural multi-copy PGM benchmark supplies a stricter measurement objective
than the fixed-source separator searches. It averages over the complete
weak-Fourier source-label law on the exact `S_5` fixed-point-free ensemble and
compares the global conditioned PGM with both independent one-copy PGMs and
separate Young-basis measurements. At three copies, the global PGM gains about
`0.717` bits over product PGMs and `0.452` bits over separate Young outcomes,
with normalization/completeness residuals below `1.2e-14`. This is finite
architecture-design evidence only: the PGM is still materialized as dense
branch matrices, and there is no uniform circuit, compressed outcome,
polynomial hidden-involution decoder, asymptotic theorem, or classical
separation.

The gain-localization audit removes two easy explanations for that finite
signal. On all 84 natural three-copy source multisets, 65 branches contribute
positive gain and none contribute negative gain; those branches carry about
`99.67%` of natural source mass. The largest branch supplies only `8.4%` of
aggregate gain, while 80% of gain spans about `69.2%` of source mass. All
finite average frames have condition number below `20`, at most 17 distinct
nonzero eigenvalues, and finite exact inverse-root interpolation degree at most
16. The new bottleneck is an all-`n` harmonic block encoding and spectral
theorem for the average frame, followed by a covariant outcome circuit and
decoder. Dense finite inversion remains non-algorithmic.

The average-frame audit gives the compact operator identity behind the signal:
for any copy count, the frame is the sum of subset diagonal-action class
averages divided by the source normalization. A conditional projected-LCU
schema coherently averages the product of `I+rho_lambda(h)` without storing the
hidden orbit. Exact reconstruction and LCU proportionality pass on all 84
natural `S_5` branches with residuals below `6e-17` and `2.3e-16`. This still
does not solve the measurement problem. At `k=ceil(n log2 n)`, the normalized
operator has roughly `2^-k` average spectral scale when hard-sector character
ratios are small; the conditional generic square-root amplification exponent
is about 159 bits by the `n=64` row. The character-ratio envelope itself still
needs a natural-source theorem. Future work must find a structured harmonic
amplifier, a better frame factorization, or a direct covariant measurement
that avoids this normalization.

The natural character-ratio theorem removes the remaining distributional
assumption from that barrier. For
`r_lambda=chi_lambda(C)/d_lambda`, column orthogonality gives
`E_Plancherel[r_lambda^2]=1/|C|`. The exact coset source law is the Plancherel
law reweighted by `1+r_lambda`, so
`Pr(|r_lambda|>epsilon)<=2/(|C|epsilon^2)`. Across
`k=ceil(n log2 n)` iid source labels, the `epsilon=1/sqrt(n)` failure bound is
`2kn/|C|`; for fixed-point-free involutions its log2 value is below `-338` by
`n=128`. Complete partition-table controls through `n=16` verify source mass,
column orthogonality, and the natural second-moment bound. This makes the
direct projected-LCU normalization obstruction a natural-input result, while
leaving non-LCU collective measurements open.

The whitening-free projector sub-POVM is the first concrete non-LCU
alternative. Each conditioned source state is a normalized projector
`rho_h=P_h/rank(P_h)`. Setting
`E_h=rho_h/||sum_y rho_y||` and adding a failure effect gives a valid covariant
measurement with conclusive probability
`q=Tr(F^2)/||F||>=1/kappa(F)`, so absolute frame normalization disappears.
All 119 natural `S_5` source-branch controls pass the projector, completeness,
and conclusive-formula identities to about `1e-15`. At three copies the
sub-POVM retains about `0.456` bits with conclusive probability `0.598`, beating
product one-copy PGM by `0.161` bits but not separate Young-basis information.
The obvious uniform-label controlled-projector dilation realizes weaker
`P_h/M` effects and retains only about `0.120` bits with conclusive probability
`0.183` on the same control. The stronger condition-normalized effects are a
mathematical POVM, not an implemented circuit. This is now the main measurement
architecture, but it still needs a structured maximal-scale harmonic Naimark
dilation for the exponentially large covariant orbit,
compressed outcomes, an all-`n` frame-condition theorem, a polynomial decoder,
and classical separation.

The projector theorem transfers algebraically to the physical code-equivalence
wreath group because every bridge hidden element is an involution and every
conditioned state is again a normalized support projector. The finite
`S_5` information and condition values do not transfer. Existing exact wreath
moments provide only a moment-based conclusive lower bound with log2 value
about `-295` at `n=64`; this is also the exact conclusive probability of the
direct uniform-label projector dilation. Reaching the maximal condition-
normalized effects requires a new structured dilation or amplification. Four
selected finite information-threshold physical
blocks have inverse-condition floor about `0.364`, but they do not cover the
complete natural source law. The top physical target is therefore an all-sector
wreath frame-condition theorem plus a harmonic covariant Naimark dilation and
compressed permutation decoder.

The moment-certificate bridge replaces an unsupported all-sector condition fit
with a precise proof target. For a physical frame block `B`, the maximal
projector sub-POVM has
`q=Tr(B^2)/(Tr(B)||B||)` and order-`p` moments certify
`q>=Tr(B^2)/(Tr(B)Tr(B^p)^(1/p))`. Across all 84 naturally occupied complete
`W_3` threshold blocks, exact aggregate conclusive probability is `0.725`;
order 4 certifies `0.411` and order 16 certifies `0.650`. A factor-two norm
certificate may require moment order up to `175526` on the `n=64` Hilbert-
dimension bound. That order remains polynomial in `n`. The natural source-law
reduction below removes equal-pair sectors from the asymptotic critical path,
but no growing-order contraction for arbitrary all-unequal tuples, structured
maximal-effect dilation, or decoder is known.

The exact portfolio audit now has both a hard cut and a surviving finite
direction.  On the maximum-dimension `S_8` source, TC2 is zero on targets
`(4,4)` and `(2,2,2,2)`; TT1 has a repeated zero root, and adding the
disjoint-transposition generator preserves a squared linear factor for every
coefficient.  The independent TC-intersection-one generator behaves
differently: exact fourth moments give a discriminant that is strictly
positive for every nonzero real coefficient, repairing both known collisions.
The same exact word basis certifies all six `n=8` targets of multiplicity at
most four. Exact quotient transfer at `c=1` extends finite square-freeness to
all 20 targets through multiplicity 17. Adjacent-size coverage, all-n
square-freeness, inverse-polynomial normalized gaps, coherent implementation,
and hidden-involution decoding remain mandatory blockers.

The capability ledger separates the solved `S_n` QFT, Schur-Weyl transforms,
weak projection, and multiplicity counting from the still-open internal
Kronecker, growing-copy associator, transition-filter, and hidden-involution
decoder primitives. The typed synthesis command composes those primitives into
complete state-interface chains, rejects known Fourier/counting/rank shortcuts,
and records the remaining full recoupling and tensor-associator architectures
as non-promotable proof-debt mutations until every circuit and decoder theorem
is supplied.

The capability ledger is literature-backed and deliberately distinguishes the solved polynomial `S_n` QFT,
Schur-Weyl transforms, weak irrep projection, and multiplicity-counting results from the still-unproved internal
Kronecker transform, overlapping `k`-copy associator network, state-transition implementation, and hidden-involution
decoder. It also records the 2025 classical algorithms that erase many proposed restricted multiplicity speedups.

Run the binary linear-code equivalence workbench:

```bash
python qsearch.py code-equivalence
```

Run structural code-invariant baselines before canonicalization:

```bash
python qsearch.py code-invariants --verbose
```

Run information-set canonicalization baselines:

```bash
python qsearch.py code-info-sets --verbose
```

Run profile-pruned code canonicalization baselines:

```bash
python qsearch.py code-canonicalize --verbose
```

Search for code pairs that collide on coordinate-refinement profiles, then
attack them with canonicalization:

```bash
python qsearch.py code-profile-search --verbose
```

Run higher-order coordinate tuple-profile baselines:

```bash
python qsearch.py code-tuple-profiles --verbose
```

Run low-weight support hypergraph/matroid baselines before trusting any
code-equivalence row:

```bash
python qsearch.py code-low-weight --verbose
python qsearch.py code-low-weight --max-incidence-nodes 300 --verbose
```

Search structured quasi-cyclic code families for tuple-profile collisions:

```bash
python qsearch.py code-qc-search --verbose
```

Search algebraic cyclic code families for tuple-profile collisions and reject
reciprocal/dihedral/multiplier controls:

```bash
python qsearch.py code-cyclic-search --verbose
```

Search primitive BCH code families with cyclotomic defining-set and decimation
controls plus dual/parity-check-side baselines for high-rate rows:

```bash
python qsearch.py code-bch-search --verbose
```

Search binary Goppa/alternant families over small finite fields and reject
semilinear field-automorphism controls:

```bash
python qsearch.py code-goppa-search --verbose
```

Scale punctured rootless Goppa/alternant rows to lengths 48, 96, and 160;
compute exact dual weight/incidence signatures where feasible plus hull and
primal/dual Schur-square invariants; and record unresolved enumeration caps as
classical proof debt rather than hardness evidence:

```bash
python qsearch.py code-goppa-scaling --verbose
python qsearch.py run EXP-CODE-GOPPA-SCALING-FRONTIER
```

Apply the exact low-degree syzygy baseline to the scalable Goppa frontier.
This computes `beta_1,2` from quadratic relations of the dual projective
system, `beta_2,3` from the kernel of their linear multiplication map, and a
complete histogram across every one-coordinate shortening for unresolved
pairs. A mismatch is an exact polynomial classical rejection; a collision or
diagnostic `--coordinate-limit` cap is only proof debt:

```bash
python qsearch.py code-goppa-syzygies --verbose
python qsearch.py run EXP-CODE-GOPPA-SYZYGY-FRONTIER
```

The implementation is linked to the dual-Goppa square bounds, high-rate
alternant shortening attacks, and the higher Betti-number syzygy distinguisher.
It does not treat a family distinguisher as a code-equivalence solver or a
Betti collision as a classical lower bound.

Close public-generator Goppa rows with the exact trivial-hull projector
reduction when applicable. The command certifies
`Sigma_C = G^T (G G^T)^(-1) G`, converts it to a loop-colored graph, applies
polynomial loop/degree/WL invariants, and verifies any graph-isomorphism
mapping on the complete code row spaces. A projector collision transfers debt
to graph isomorphism; it does not preserve a code-native hard row:

```bash
python qsearch.py code-goppa-projectors --verbose
python qsearch.py run EXP-CODE-GOPPA-HULL-PROJECTOR
```

Search graph-structured Tanner/LDPC families and reject Tanner graph or code
canonicalization controls:

```bash
python qsearch.py code-tanner-search --verbose
```

Search punctured Reed-Muller/evaluation-code families and reject affine-support
automorphism controls:

```bash
python qsearch.py code-rm-search --verbose
```

Search binary-expanded Gabidulin/rank-metric families and reject symbol-block
permutation controls:

```bash
python qsearch.py code-rank-metric-search --verbose
```

Resolve tractable rank-metric and quasi-cyclic proof-debt rows exactly by
colored full-code incidence isomorphism, with recovered permutations verified
against complete codeword sets:

```bash
python qsearch.py code-incidence-resolve --verbose
```

This resolver is a finite-instance falsifier, not a scalable algorithm: its
incidence graph contains `2^k` codeword vertices, and caps/timeouts remain proof
debt.

Generate certified self-dual `[I|A]` codes whose hull grows with dimension,
then attack their collisions with Schur-square/cube, column-matroid,
puncture/shorten, full-codeword, and exact finite incidence checks:

```bash
python qsearch.py code-self-dual-search --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH
```

This family evades the trivial-hull projector shortcut, but that removes only
one obstruction. Polynomial-signature collisions, finite exact
non-equivalence, solver caps, and timeouts remain classical proof debt until a
scalable canonicalization lower bound and a nonabelian measurement necessity
are established.

Certify why the bounded local puncture/shorten profiles collapse:

```bash
python qsearch.py code-self-dual-local-obstruction --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION
```

For a self-dual `[2k,k,d]` code and `|S|<d`, puncturing on `S` has dimension
`k`, while shortening and both resulting hulls have dimension `k-|S|`.
Therefore fixed-order local rank-hull collisions are forced on a
growing-distance family. They are a no-go for that baseline, not hardness
evidence.

Audit the remaining global orbit and the Construction-A lattice bridge:

```bash
python qsearch.py code-self-dual-global-orbit --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT
```

Full basis-normalized column-multiset matches are exact equivalence witnesses.
Independent sampled misses are not non-equivalence certificates. The audit also
charges Construction-A determinant, parity, minimum norm, and root counts while
leaving the coordinate-frame reverse implication explicit; a forward
code-to-lattice map is not silently treated as an iff reduction.

Audit the exact code-equivalence HSP and published no-go hypotheses:

```bash
python qsearch.py code-self-dual-hsp --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-HSP-APPLICABILITY
```

The raw scrambler-permutation hidden shift is over `GL_k(F_2) x S_n`, and the
corresponding HSP is over its wreath product with `Z_2`. The
Dinh-Moore-Russell criterion does not cover `k=n/2`, but that apparent opening
does not survive canonicalization of the public generator rowspace:

```bash
python qsearch.py code-self-dual-rowspace-hsp --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION
```

The exact hiding function `f_C(P)=RREF(MP)` removes the `GL_k` row-scrambler
gauge and gives hidden shift over `S_n`, with stabilizer `PAut(C)`. Therefore
the raw high-rate dimension-gate failure is not evidence for a quantum signal.
The real open obligations are to certify the tail automorphism groups and
minimal degrees, apply the appropriate symmetric-group coset-state no-go, and
only then search for a collective measurement and polynomial decoder.

Stratify that automorphism debt with exact bounded-weight supports:

```bash
python qsearch.py code-self-dual-automorphisms --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH
```

Self-duality makes the public generator a parity check, so every codeword
support through weight eight is enumerated exactly by matching size-at-most-four
column subsets with equal XOR. On the current tail, all sampled `k=16`
instances have verified nontrivial full-code automorphisms, all sampled `k=24`
instances have singleton color-refinement rigidity certificates, and `k=32`
remains unresolved because the fixed-weight support hypergraph is too sparse.
These are finite strata, not an infinite-family theorem. Rigid rows inherit the
GI-type single-register/strong-Fourier obstruction, but collective measurements
and polynomial decoding remain open.

Resolve the sparse weight-eight tail without erasing that scaling failure:

```bash
python qsearch.py code-self-dual-high-order --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER
```

The packed order-five meet-in-the-middle pass exactly enumerates supports
through weight ten on the length-64 rows. It resolves all six prior `k=32`
automorphism-debt instances as rigid by singleton coordinate refinement. The
combined current tail is therefore 12 rigid, 8 explicitly nonrigid, and 0
unresolved instances. This still does not prove a growing-family theorem.
For the rigid `k>=24` stratum, single-register Fourier search is now
deprioritized; the relevant quantum target is a genuinely collective
measurement with a polynomial hidden-permutation decoder.

Prove the asymptotic limit of that finite certificate:

```bash
python qsearch.py code-self-dual-sparsity --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION
```

For a uniform binary self-dual length-`n` code, a fixed nontrivial even vector
belongs with probability `1/(2^(n/2-1)+1)`. Thus every fixed-weight support
count vanishes asymptotically. The observed weight-eight/ten counts closely
track this exact ensemble expectation. Nonvanishing support density moves to
linear relative weight at the binary-entropy threshold
`H_2(delta)=1/2`, `delta approximately 0.110028`, making explicit
meet-in-the-middle enumeration exponential. This cuts fixed-order support
enumeration as the family-scale automorphism method. It does not rule out an
implicit growing-weight invariant and is not quantum speedup evidence.

Use the exact group for the surviving rigid HSP:

```bash
python qsearch.py code-self-dual-wreath --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SPECTRUM
```

Rigid code equivalence gives bridge involutions `h_s=(s,s^-1;swap)` in
`(S_n x S_n) semidirect Z_2`, indexed by `n!` hidden permutations. Unequal
irrep pairs have bridge character zero; equal pairs split into `+/-` extensions
with character ratios `+/-1/d_lambda`. This yields an exact one-copy frame,
PGM, Holevo bound, and weak-label zero-information theorem in the correct
group. One-copy PGM success remains below twice uniform guessing. The open
mechanism is now precise: a `Theta(log n!)`-copy diagonal-action transform,
carrier-sensitive covariant POVM, and polynomial hidden-permutation decoder.

Audit the scalar homogeneous-space shortcut before using it:

```bash
python qsearch.py code-self-dual-wreath-hecke --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT
```

The bridge-label stabilizer `C_W(h_e)` does form a Gelfand pair with the
wreath group, and scalar covariant kernels reduce to symmetric-group class
functions. The actual hidden subgroup is instead `H=<h_e>`; its equal-pair
irreps have multiplicity `(d_lambda^2 +/- d_lambda)/2`, so `(W_n,H)` is
non-Gelfand from `n=3` onward. The all-register Gelfand-pair PGM theorem
therefore does not transfer. Moreover, the normalized `k`-copy
Hilbert-Schmidt kernel is `1` for equal hidden permutations and `2^-k`
otherwise, with no cycle-type signal. This removes a factorial scalar table
but leaves the operator-valued subset/carrier algebra, frame inverse, POVM,
and decoder fully open.

Reduce that operator frame to its exact PGM polar problem:

```bash
python qsearch.py code-self-dual-wreath-pgm --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT
```

For `k` copies, the support projectors `P_s` define
`B_k=(1/n!) sum_s P_s` and
`A_k=(1/sqrt(n!)) sum_s |s> tensor P_s`. The PGM is exactly the polar
isometry `A_k B_k^-1/2`, and `B_k` has a compact LCU expansion over a
permutation label and a `k`-bit subset mask. This is a real operator-valued
reduction, but not yet an algorithm. At `k=ceil(log2(n!))`, exact first and
second moments put the relevant polar singular scale at
`Theta((n!)^-1/2)`. Generic frame inversion and even an optimistic reusable
candidate-verifier search are factorial. The new target is a
representation-specific carrier preconditioner or direct polar transform
that is legal under ordinary mixed coset-state access.

Audit the subset-orbit carrier algebra before proposing that preconditioner:

```bash
python qsearch.py code-self-dual-wreath-carrier --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA
```

Writing the average frame as `2^-k sum_A T_A` and grouping by subset size
does reduce formal labels to `U_0,...,U_k`. It does not produce a scalar
algebra. Exact sparse wreath-group calculations show that overlapping
`T_A` operators fail to commute for nonabelian `S_n`, and the fully
register-symmetrized `U_2,U_3` pair first fails to commute at `k=4`. For the
`S_3`, `k=4` control, words through depths `1,2,3` have modular rank lower
bounds `5,16,42`, already exceeding the `k+1` scalar orbit dimension. The
next target is therefore a noncommutative multiplicity-block transform and
conditioned recurrence, not a Hamming-weight/Krawtchouk diagonalization.

Cut explicit carrier-orbit enumeration at scaling:

```bash
python qsearch.py code-self-dual-wreath-orbits --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH
```

A depth-`d` carrier word has `d-1` relative permutations modulo simultaneous
conjugation. Burnside's lemma gives
`sum_{lambda partition n} z_lambda^(d-2)` orbits before the final wreath
swap, which can reduce the count by at most two. At depth three, the identity
cycle type alone contributes `n!`; at depth four it contributes `(n!)^2`.
Thus explicit hidden-label carrier tables are factorial even though
fixed-depth subset-intersection profiles are polynomial in the copy count.
The only viable next architecture is a compressed harmonic transform using
irreducible and multiplicity labels with sparse recoupling rules.

Derive that harmonic schema without mistaking labels for an algorithm:

```bash
python qsearch.py code-self-dual-wreath-harmonics --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA
```

Under conjugation,
`C[S_n]=direct_sum_nu V_nu tensor C^(m_nu)` with
`m_nu=sum_lambda g(lambda,lambda,nu)`. The depth-three invariant carrier
space therefore has dimension `sum_nu m_nu^2`, exactly matching the Burnside
pair-orbit count. This replaces factorial orbit names by partition and
multiplicity labels, but it does not make dense block operations efficient:
some block has at least `n!/p(n)` matrix coordinates. The audit verifies the
identity exactly through `n=12` and records the theorem tail through `n=64`.
The remaining target is a sparse internal Kronecker transform and
carrier-product recurrence; an `S_n` group QFT or compact coordinate address
alone is insufficient.

Transfer the one existing all-`n` equal-source multiplicity gap without
overstating its coverage:

```bash
python qsearch.py code-self-dual-wreath-commutant --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT
```

The bounded-support commutant Hamiltonian for
`lambda=(n-2,2)`, `nu=(n-3,2,1)` genuinely resolves a multiplicity-two
carrier sector with normalized gap `2/[n(n-1)]`. It therefore transfers as a
polynomial conditional label primitive. It resolves only four invariant
matrix coordinates, however, in a carrier space with at least `n!`
coordinates. The audit charges the resulting `4/n!` coverage upper bound and
keeps cross-source carrier action, frame invariance, general multiplicity
gaps, and decoding open.

Construct the actual physical Fourier blocks of the correlated frame:

```bash
python qsearch.py code-self-dual-wreath-frame-blocks --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS
```

For equal-pair wreath irreps, the bridge action is
`+/-[rho_lambda(s) tensor rho_lambda(s^-1)]Swap`, and a physical `k`-tuple
block is the exact average of the corresponding correlated projectors.
Right convolution preserves physical wreath-irrep tuple labels. This is
distinct from, and does not solve, hidden-label harmonic multiplicities. The
probe diagonalizes every sign sector for selected `S_3`, `S_4`, and `S_5`
equal-pair blocks, including all `S_3` information-threshold controls.
Finite conditioning remains only a control until unequal-pair tuples,
growing-`n,k` spectral recurrences, and a coherent blockwise inverse exist.

Retain unequal-pair physical irreps in collective analyses:

```bash
python qsearch.py code-self-dual-wreath-unequal-blocks --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS
```

These induced irreps have exactly zero bridge character, so their one-copy
frame is `I/2` and weak Fourier labels reveal nothing. Their correlated
multi-copy blocks are nevertheless non-scalar and can have kernels. The probe
constructs every unequal `W_3` block through the information threshold, every
unequal `W_4` block through two copies, and representative `W_5` controls.
Discarding zero-character sectors is therefore invalid. Mixed tuples of
different physical irreps, growing spectral recurrences, worst-sector
conditioning, and a coherent inverse remain open.

Close the finite mixed-tuple loophole completely for `W_3`:

```bash
python qsearch.py code-self-dual-wreath-w3-tuples --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES
```

`W_3` has nine physical irreps and 165 unordered three-copy tuples at the
information threshold. Exactly 84 tuples carry all natural coset-state mass;
the remaining tuples contain one of two zero-mass one-dimensional minus
extensions. Every occupied block has minimum positive eigenvalue at least
`1/8` and support condition number at most `4`. More than 80% of the natural
mass lies in blocks with kernels, so a support pseudoinverse is mandatory.
This complete finite theorem is now a regression target for an all-`n`
character-moment recurrence, not evidence that such a recurrence or coherent
inverse already exists.

Derive exact character moments without treating a second moment as an inverse:

```bash
python qsearch.py code-self-dual-wreath-moments --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS
```

The general wreath-character expansion reproduces all 165 complete `W_3`
tuple blocks through moments one to four. Its second moment contracts exactly
to a partition-class sum for arbitrary mixed physical irreps and scales
through the registered all-`n` portfolios. This does not control the smallest
positive eigenvalue. A naive third moment requires factorially many
simultaneous-conjugacy pair orbits, so the active frontier is a symbolic
class-algebra or representation-ring contraction, followed by a genuine
support-gap theorem.

Remove that factorial third-moment sum in one exact physical sector:

```bash
python qsearch.py code-self-dual-wreath-third-moment --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION
```

For repeated copies of the unequal irrep induced from the trivial and standard
`S_n` representations, the third moment depends only on
`fix(r)+fix(q)+fix(r^-1 q)`. A weighted-rook reduction and the permutation
cycle index compute its complete distribution with polynomially many
bivariate coefficient states, eliminating `(n!)^2` pair enumeration. The
recurrence is exact and validated against direct character sums. It covers one
irrep family only: equal-pair commutator terms, arbitrary mixed tuples,
support gaps, coherent pseudoinversion, and decoding all remain open.

Extend exact third moments to every unequal-only mixed tuple:

```bash
python qsearch.py code-self-dual-wreath-all-unequal --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT
```

For unequal physical irreps, the third projector-word character depends only
on the conjugacy classes of `r`, `q`, and `r^-1 q`. Symmetric-group class
connection coefficients therefore give an exact contraction over `p(n)^3`
class triples with at most `p(n)^4` character-kernel terms. This is
subfactorial but still `exp(O(sqrt(n)))`, not polynomial. Equal-pair irreps add
commutator characters. An explicit `S_4` counterexample holds all three class
labels fixed while changing the commutator class. That proves class triples do
not solve worst-sector moments, but the natural source-law reduction below
shows equal sectors need not remain on the average-case critical path.

Reduce the natural asymptotic problem to all-unequal physical sectors:

```bash
python qsearch.py code-wreath-natural-unequal
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE
```

A physical weak-Fourier label is exactly two independent Plancherel partitions
packaged as an equal or unequal pair. Equal-label probability is therefore the
Plancherel collision probability
`C_n=sum_lambda (d_lambda^2/n!)^2`, bounded by the largest Plancherel atom.
The literature theorem
`max_lambda d_lambda=sqrt(n!) exp(-Theta(sqrt(n)))` gives
`C_n=exp(-Theta(sqrt(n)))`; even across
`k=ceil(log2(n!))` labels, `Pr(any equal)<=k C_n=o(1)`. Exact controls through
`n=48` already give all-unequal tuple probability above `0.95`. Thus mixed
equal-pair commutator recoupling is no longer the natural asymptotic
bottleneck. The live target is a growing-order contraction for arbitrary
all-unequal tuples, followed separately by maximal-effect dilation and
hidden-permutation decoding.

Remove the physical-irrep sum from every natural moment order:

```bash
python qsearch.py code-wreath-moment-word-map
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP
```

For the exact natural irrep law, character column orthogonality gives
`E_pi[chi_pi(g)/d_pi]=1[g=e]+1[g in C]/|C|`, where `C` is the bridge
conjugacy class. Expanding every projector word therefore reduces the
source-averaged dimension-normalized order-`m` frame moment to
`E[(2^-m(N_e+N_C/|C|))^k]`, where `N_e` and `N_C` count subset products that
are the identity or another bridge. This identity is exact at every order,
removes all physical-irrep enumeration, and reproduces every complete natural
`W_3` spectral moment through order four. It is not yet a scalable
contraction: direct evaluation costs `(n!)^m 2^m`, and the `n=64` target has
moment order `175526`. The next mathematical target is a compressed
surface-word or cycle-index recurrence for these two subset-word counts,
followed by a concentration theorem from source-averaged moments to
individual natural tuple success.

Prove one-word mixing and expose the multi-copy concentration gap:

```bash
python qsearch.py code-wreath-word-map-mixing
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING
```

The one-label word statistic is a central lazy walk with sector eigenvalue
`(1+chi_pi(h)/d_pi)/2`. Exactly two one-dimensional plus sectors are
stationary, with total natural mass `2/(n!)^2`; every other eigenvalue is at
most `3/4`. Thus the mean word statistic mixes uniformly to `2/(n!)^2`.
At the `n=64` target the nonstationary error is more than 72,000 bits below
that floor. This still does not bound the required `k`th moment: the bridge
sequence is shared across copies, and Jensen plus boundedness leave an
interval about 174,000 bits wide. The coupled-chain theorem below closes the
spectral-gap part of this obstruction but not the typical-source moment scale.

Prove constant-gap shared-generator contraction and isolate rare-sector
contamination:

```bash
python qsearch.py code-wreath-coupled-word-gap
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP
```

The exact `k`th word statistic is an endpoint observable of
`M_k=E_c tensor_i (I+R_c)/2` on the bridge-generated index-two subgroup.
Because every factor is a projection, on any sector with a nonconstant
coordinate `j` the tensor product is bounded by its `j`th factor. The
one-coordinate `3/4` spectral-radius bound therefore tensorizes without a
`1/k` loss: the coupled chain has gap at least `1/4`. Exact dynamic-programming
controls match direct subset-word moments.

This is not yet a typical-source success theorem. At `n=64`, order `175526`,
the transient bound is still far above the stationary `k`th-moment scale, and
the stationary floor is generated by exponentially rare equal
one-dimensional labels. The conditioned-kernel theorem below removes that
contamination exactly.

Condition the source on the asymptotically dominant all-unequal sectors:

```bash
python qsearch.py code-wreath-conditioned-kernel
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL
```

Subtracting diagonal partition pairs from two independent Plancherel draws
gives an exact signed normalized-character kernel. It vanishes on the swap
coset and, on `(a,b,0)`, equals the regular delta kernel minus
`(n!)^-2 sum_lambda d_lambda^2 chi_lambda(a)chi_lambda(b)`, normalized by the
unequal-pair probability. Complete `W_2`, `W_3`, and `W_4` checks and direct
bridge-word expansions agree exactly. Every conditioned one-label annealed
moment is `2^-m`, and projection domination proves `B<=I/2` for every fixed
all-unequal tuple.

That bound is still about `k-1` operator-norm bits too weak: the frame scale
indicated by the second moment is approximately `2^{1-k}`. The active theorem
can be narrowed once more using global source collisions.

Remove repeated source partitions across different physical labels:

```bash
python qsearch.py code-wreath-global-collision
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION
```

Before pair packaging, `k` physical labels are exactly `2k` iid Plancherel
draws. If `C_n` is the Plancherel collision probability, a union bound gives
`Pr(any source repeat) <= binom(2k,2) C_n`. The maximal-atom theorem and
`k=Theta(n log n)` make this `o(1)`. Thus natural threshold tuples have all
`2k` source partitions globally distinct with probability `1-o(1)`. This
excludes the known repeated trivial-sign `W_3` block whose frame norm remains
`1/2`.

Global distinctness is not a norm theorem. The active target is a simultaneous
`k`-coordinate contraction for arbitrary globally distinct source-partition
tuples, at the `2^{1-k}` frame scale, followed separately by a coherent
maximal-effect dilation and hidden-permutation decoder.

Probe the collision-free mixed-frame scale directly:

```bash
python qsearch.py code-wreath-collision-free-frame
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE
```

The probe uses matrix-free Hermitian Lanczos, not dense Kronecker frame
construction. It covers every collision-free `W_4`, `k=2` pairing and an
adversarial `W_5`, `k=3` portfolio. The `W_5` target is `2^{1-k}=1/4`;
observed top eigenvalues range from `0.175` to about `0.25842`. Exact
projector independence is therefore false, but every probe remains within
roughly `1.034` of the target with explicit eigenpair residual checks. The
research target is now the sufficient bound
`||B|| <= poly(n) 2^-k`, not exact equality.

Reduce that norm target to character decay and short-word counting:

```bash
python qsearch.py code-wreath-character-ratios
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT
```

For unequal physical labels, every base-coset normalized character factors
exactly into two products of ordinary `S_n` normalized characters, while the
swap coset vanishes. The contract links Féray-Sniady pointwise bounds,
hypercontractive character bounds, and sharp class-walk cutoff estimates.
Those tools reduce the missing theorem to a precise combinatorial statement:
correlated subset bridge words with short transposition length must have only
polynomially inflated total character weight across all `k` globally distinct
source partitions. Pointwise character decay alone does not prove this joint
anti-concentration statement.

Close the exact marginal part of the short-word problem:

```bash
python qsearch.py code-wreath-short-words
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE
```

For every fixed nonempty even subset mask, each base component of the bridge
word is exactly uniform on `S_n`. Its transposition-length tail is therefore
an exact unsigned-Stirling distribution. Independently chosen masks across
the `k` source coordinates are also pairwise distinct with overwhelming
probability at the certificate order; at `n=64` the collision union bound is
below `2^-175509`. These facts remove marginal and diagonal explanations.
Distinct masks still reuse the same bridge generators, so the remaining
theorem is explicitly non-diagonal joint word-map anti-concentration.

Reduce joint character products to mask-incidence two-cores:

```bash
python qsearch.py code-wreath-mask-hypergraph
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION
```

If any bridge generator is selected by exactly one character word, averaging
that generator applies the zero bridge class-sum operator in its unequal
physical irrep, so the complete joint character product vanishes. Only mask
incidence matrices whose active columns all have weight at least two can
contribute. This exact two-core reduction also proves every distinct two-mask
unequal character covariance is zero. Higher correlations remain: exact
collision-free `W_5` triangle patterns can have nonzero value, including
`1/1600`. The active theorem is now aggregate character decay on dense
incidence two-cores.

Resum the dense two-cores and localize the actual norm theorem:

```bash
python qsearch.py code-wreath-subgroup-twirl
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION
```

The bridge identity `h_s=x_s h_e x_s^-1` makes the entire collision-free
frame a subgroup twirl of one tensor projector. Schur averaging then reduces
its norm exactly to normalized partial traces on diagonal-`S_n` isotypic
multiplicity spaces. All 15 collision-free `W_4` pairings satisfy the direct
frame, twirl, central-projector, multiplicity, and top-sector identities.
This is a reduction, not a bound: at the `n=12`, `k=29` information threshold,
the largest restriction multiplicity is already about `2^640.99`. The next
proof target is uniform partial-trace delocalization, or an asymptotic natural
counterexample.

Resolve the partial-trace block into explicit orientation projectors:

```bash
python qsearch.py code-wreath-orientation-fourier
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION
```

The orbit-Gram Fourier transform writes every target block exactly as
`2^-k` times a sum of invariant-subspace projectors, with the same nonzero
spectrum as the physical frame. All 15 collision-free `W_4` controls pass.
The support-counting route fails decisively: every tested information-
threshold portfolio from `n=6` through `n=12` has full orientation support,
and the `n=12`, `k=29` case is fully saturated after the third label. The live
target is the norm geometry of a fully supported, highly overlapping
projector family via canonical angles, fusion-frame estimates, or recoupling
identities, not orientation sparsity.

Compute pairwise fusion geometry and the complete averaged second moment:

```bash
python qsearch.py code-wreath-orientation-moments
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT
```

An exact character-convolution formula now evaluates every pair overlap
`Tr(E_a E_b)`, and symmetric-group class-product constants evaluate
`Tr(F_nu)` and `Tr(F_nu^2)` without enumerating `4^k` orientation pairs. The
formula passes 48 active pair controls and 300 rank controls across all 15
collision-free `W_4` tuples. Through `n=12`, `k=29`, the largest collision
lower bound is only about `1.06` times the `2^(1-k)` target and the effective
rank reaches roughly `2^639.91`; no second-moment obstruction appears. This
is evidence that the fully supported frame may be delocalized, but it is not
an upper bound on its top eigenvalue. Growing orientation moments or a direct
operator-valued Gram contraction remain necessary.

Factor the pair-core overlap operator exactly:

```bash
python qsearch.py code-wreath-pair-core-carrier-factorization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION
```

For two pair cores sharing an orientation, the overlap is exactly a direct
sum of `1/(d_beta d_p)` times partial isometries, with one carrier per
membership cluster and exact representation-ring multiplicities. The
conjectured single-reciprocal `1/d_alpha` law is therefore false in general;
finite screens saw single reciprocals only because their membership blocks
were singletons. Because a correlation equals one exactly when both carriers
are one dimensional, every off-common correlation is at most `1/(n-1)` for
`n>=5`. There is no nontrivial multiplicity-space 6j block at a shared
vertex; genuine Kronecker content first appears for vertex-disjoint cores,
where a waist bound applies. All 168 screened controls, three named
`d=5,9,10` controls, 40 repeated-label controls, and 40 disjoint controls
agree with the closed form to `5.83e-16`.

Measure the crossing-graph weighted degree:

```bash
python qsearch.py code-wreath-multistar-degree
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION
```

Block Gershgorin on the crossing relation Gram needs the absolute weighted
degree to stay below two. A sibling merge has a complete bipartite crossing
graph, and Sellke covering saturates the off-common weight at `1/(n-1)` as
the label count grows, so the degree grows like `2^(j-1)/(n-1)`. On natural
threshold portfolios the certificate is already vacuous at `n=8` and reaches
about `2^25.5` at `n=12`. No absolute-weight comparison can certify the
residual quotient at natural depth. The surviving object is the
projector-weighted orientation Laplacian `Delta = D - A`, whose positive
spectrum equals that of the relation Gram; no gap is proved for it.

Audit the exact pair-core quotient overlap:

```bash
python qsearch.py code-wreath-pair-quotient-overlap
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP
```

After internal child dependencies are quotiented, crossing pair relations generate
the physical span `K` of all crossing leaf-pair intersections. The cross `H0` quotient
vanishes if and only if the principal correlation between `A` minus `K` and `B` minus `K`
is strictly below one. On `S_6` portfolios, the minimum exact quotient gap is `0.7375`.

Verify the exact recursive H0 short-exact sequence:

```bash
python qsearch.py code-wreath-recursive-pair-generation
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION
```

Parent `H0` is an extension of `H0(left) \oplus H0(right)` by the cross-dependency quotient
`W/W_pair`. Pair generation at every child together with a vanishing cross quotient at every
merge implies pair generation at the root. All 11,025 affine nodes across 105 globally
distinct three-label `S_5` portfolios have `H0 = 0`.

Audit the augmented common-core Cech complex:

```bash
python qsearch.py code-wreath-augmented-common-core-cech
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH
```

The degree-zero boundary `D_0` synthesizes leaf-range coefficients into physical carrier
space. `H_0 = ker(D_0) / im(D_1)` is the exact quotient of all leaf dependencies by
pair-common relations, separating the emergent `H_0` gate from higher pair-cycle exactness.

Verify exact pair-cycle resolution on the relative common-core Cech complex:

```bash
python qsearch.py code-wreath-common-core-cech
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN
```

Higher common cores supply exact boundaries `D_2` that nullify pair-relation cycles `H_1 = ker D_1 / im D_2 = 0`.
On dense `S_6` controls, the exact Cech-quotiented pair Laplacian has positive eigenvalues in `[2, 4]`.

Analyze local scalar recouplings and screen S6 pair-core correlations:

```bash
python qsearch.py code-wreath-pair-core-recoupling --limit 180
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY
```

All 560 screened `S_6` pair-core stars are reciprocal-carrier contractions `1/d`, certifying local frame conditioning.

Construct exact parity intertwiners and verify the relative Cech atom formula:

```bash
python qsearch.py code-wreath-common-core-atomization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION
```

Parity intertwiners prove affine support balance. A third globally distinct `S_6` plane falsifies universal commutativity with exact scalar-star channels 8/17 and 89/170.

Analyze orientation Laplacian spectrum and test width-independent floor:

```bash
python qsearch.py code-wreath-orientation-laplacian-gap
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP
```

The signed incidence structure yields a metric floor `2 - 2 gamma_max` independent of merge width, respecting all 270 screened full-graph controls.

Analyze trivial/sign common-range multiplicities:

```bash
python qsearch.py code-wreath-orientation-common-ranges
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE
```

Analyze fixed-family triple-range multi-way incidence:

```bash
python qsearch.py code-wreath-orientation-family-ranges
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE
```

Analyze orientation pair principal-angle spectrum:

```bash
python qsearch.py code-wreath-orientation-pair-angles
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES
```

Analyze orientation block common-core witness structures:

```bash
python qsearch.py code-wreath-orientation-block-core
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE
```

Evaluate Sellke covering and Plancherel block norm obstruction:

```bash
python qsearch.py code-wreath-plancherel-block-obstruction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION
```

Analyze spectral-trimmed sub-POVM hidden label recovery:

```bash
python qsearch.py code-wreath-spectral-trim
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM
```

Analyze low-pass filter polynomial degree obstructions:

```bash
python qsearch.py code-wreath-spectral-filter-degree
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION
```

Analyze Plancherel tensor stationarity and expected block mass:

```bash
python qsearch.py code-wreath-plancherel-block-mass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS
```

Analyze orientation-covariant quotient scalar-commutant obstructions:

```bash
python qsearch.py code-wreath-orientation-covariant-quotient
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION
```

Analyze branch-controlled physical invariant filter performance:

```bash
python qsearch.py code-wreath-branch-controlled-invariant-filter
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER
```

Analyze block common-core algebraic quotient annihilation:

```bash
python qsearch.py code-wreath-block-core-quotient
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT
```

Analyze paired-block self-dual irrep filter bypass:

```bash
python qsearch.py code-wreath-paired-block-filter-bypass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS
```

Analyze Plancherel-incidence no-go for block-local isotypic filters:

```bash
python qsearch.py code-wreath-local-isotypic-filter-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO
```

Analyze cluster-locality lower bounds for disjoint product filters:

```bash
python qsearch.py code-wreath-cluster-locality-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO
```

Analyze search reduction query lower bounds for low-pass filters:

```bash
python qsearch.py code-wreath-spectral-filter-query-bound
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND
```

Analyze affine core flag balance and linear routing:

```bash
python qsearch.py code-wreath-affine-core-flag
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM
```

Analyze affine node generated subgroups and common outlier rarity:

```bash
python qsearch.py code-wreath-affine-node-common-outlier
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER
```

Analyze scalar affine-plane J3 holonomy positivity:

```bash
python qsearch.py code-wreath-affine-plane-scalar-holonomy
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY
```

Analyze affine plane support demand versus capacity pressure:

```bash
python qsearch.py code-wreath-affine-plane-support-pressure-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO
```

Analyze affine recoupling flat transport bundle structures:

```bash
python qsearch.py code-wreath-affine-recoupling-bundle
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE
```

Analyze code wreath affine relation weighted bulk theorem performance:

```bash
python qsearch.py code-wreath-affine-relation-weighted-bulk
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK
```

Analyze code wreath affine star channel gap theorem performance:

```bash
python qsearch.py code-wreath-affine-star-channel-gap
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP
```

Analyze code wreath augmented h0 dimension obstruction theorem performance:

```bash
python qsearch.py code-wreath-augmented-h0-dimension-obstruction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION
```

Analyze code wreath canonical coefficient affine theorem performance:

```bash
python qsearch.py code-wreath-canonical-coefficient-affine
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE
```

Analyze code wreath cayley fiber reduction theorem performance:

```bash
python qsearch.py code-wreath-cayley-fiber-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION
```

Analyze code wreath central support rank bridge theorem performance:

```bash
python qsearch.py code-wreath-central-support-rank-bridge
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE
```

Analyze code wreath coherent fourier decoder theorem performance:

```bash
python qsearch.py code-wreath-coherent-fourier-decoder
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER
```

Analyze code wreath collision free event transfer theorem performance:

```bash
python qsearch.py code-wreath-collision-free-event-transfer
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER
```

Analyze code wreath common core polar bypass theorem performance:

```bash
python qsearch.py code-wreath-common-core-polar-bypass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS
```

Analyze code wreath complete s6 vertex channel audit theorem performance:

```bash
python qsearch.py code-wreath-complete-s6-vertex-channel-audit
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT
```

Analyze code wreath component defect gap bridge theorem performance:

```bash
python qsearch.py code-wreath-component-defect-gap-bridge
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE
```

Analyze code wreath component povm regular master reduction theorem performance:

```bash
python qsearch.py code-wreath-component-povm-regular-master-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION
```

Analyze code wreath component povm sparse support boundary theorem performance:

```bash
python qsearch.py code-wreath-component-povm-sparse-support-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY
```

Analyze code wreath covariant pgm factorization theorem performance:

```bash
python qsearch.py code-wreath-covariant-pgm-factorization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION
```

Analyze code wreath coverage welch pressure theorem performance:

```bash
python qsearch.py code-wreath-coverage-welch-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE
```

Analyze code wreath cross dependency neutrality theorem performance:

```bash
python qsearch.py code-wreath-cross-dependency-neutrality
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY
```

Analyze code wreath dependency homology theorem performance:

```bash
python qsearch.py code-wreath-dependency-homology
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY
```

Analyze code wreath early level overlap localization theorem performance:

```bash
python qsearch.py code-wreath-early-level-overlap-localization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION
```

Analyze code wreath extended kronecker threshold theorem performance:

```bash
python qsearch.py code-wreath-extended-kronecker-threshold
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD
```

Analyze code wreath final root leverage edge theorem performance:

```bash
python qsearch.py code-wreath-final-root-leverage-edge
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE
```

Analyze code wreath component defect rank mass theorem performance:

```bash
python qsearch.py code-wreath-component-defect-rank-mass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS
```

Analyze code wreath component effect algebra boundary theorem performance:

```bash
python qsearch.py code-wreath-component-effect-algebra-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY
```

Analyze code wreath component povm spectral trim theorem performance:

```bash
python qsearch.py code-wreath-component-povm-spectral-trim
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM
```

Analyze code wreath final root natural common span theorem performance:

```bash
python qsearch.py code-wreath-final-root-natural-common-span
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN
```

Analyze code wreath fixed family common rank dilution theorem performance:

```bash
python qsearch.py code-wreath-fixed-family-common-rank-dilution
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION
```

Analyze code wreath global carrier channel extractor theorem performance:

```bash
python qsearch.py code-wreath-global-carrier-channel-extractor
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR
```

Analyze code wreath global collision free mass theorem performance:

```bash
python qsearch.py code-wreath-global-collision-free-mass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS
```

Analyze code wreath global distinct joint kernel theorem performance:

```bash
python qsearch.py code-wreath-global-distinct-joint-kernel
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL
```

Analyze code wreath global partition collision theorem performance:

```bash
python qsearch.py code-wreath-global-partition-collision
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION
```

Analyze code wreath gpe holonomy resolver reduction theorem performance:

```bash
python qsearch.py code-wreath-gpe-holonomy-resolver-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION
```

Analyze code wreath gpe pair polar transport theorem performance:

```bash
python qsearch.py code-wreath-gpe-pair-polar-transport
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT
```

Analyze code wreath gpe recursive node compiler theorem performance:

```bash
python qsearch.py code-wreath-gpe-recursive-node-compiler
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER
```

Analyze code wreath graded channel graph reduction theorem performance:

```bash
python qsearch.py code-wreath-graded-channel-graph-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION
```

Analyze code wreath graded flat transport no go theorem performance:

```bash
python qsearch.py code-wreath-graded-flat-transport-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO
```

Analyze code wreath graded frobenius trim theorem performance:

```bash
python qsearch.py code-wreath-graded-frobenius-trim
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM
```

Analyze code wreath hamming stratum rank transition theorem performance:

```bash
python qsearch.py code-wreath-hamming-stratum-rank-transition
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION
```

Analyze code wreath hierarchical cokernel resolution theorem performance:

```bash
python qsearch.py code-wreath-hierarchical-cokernel-resolution
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION
```

Analyze code wreath hierarchical polar tree theorem performance:

```bash
python qsearch.py code-wreath-hierarchical-polar-tree
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE
```

Analyze code wreath hierarchy low carrier trim theorem performance:

```bash
python qsearch.py code-wreath-hierarchy-low-carrier-trim
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM
```

Analyze code wreath hierarchy pair common rank budget theorem performance:

```bash
python qsearch.py code-wreath-hierarchy-pair-common-rank-budget
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET
```

Analyze code wreath internal closure graded rescue theorem performance:

```bash
python qsearch.py code-wreath-internal-closure-graded-rescue
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE
```

Analyze code wreath interplane gauge homology theorem performance:

```bash
python qsearch.py code-wreath-interplane-gauge-homology
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY
```

Analyze code wreath invariant projector circuit theorem performance:

```bash
python qsearch.py code-wreath-invariant-projector-circuit
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT
```

Analyze code wreath isotypic dephasing no go theorem performance:

```bash
python qsearch.py code-wreath-isotypic-dephasing-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO
```

Analyze code wreath leaf whitening commutator no go theorem performance:

```bash
python qsearch.py code-wreath-leaf-whitening-commutator-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO
```

Analyze code wreath level three flag audit theorem performance:

```bash
python qsearch.py code-wreath-level-three-flag-audit
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT
```

Analyze code wreath local pair transversality theorem performance:

```bash
python qsearch.py code-wreath-local-pair-transversality
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY
```

Analyze code wreath matrix cayley boundary theorem performance:

```bash
python qsearch.py code-wreath-matrix-cayley-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY
```

Analyze code wreath matrix povm recursive compiler theorem performance:

```bash
python qsearch.py code-wreath-matrix-povm-recursive-compiler
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER
```

Analyze code wreath mixed covariant decoder theorem performance:

```bash
python qsearch.py code-wreath-mixed-covariant-decoder
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER
```

Analyze code wreath common span component universality no go theorem performance:

```bash
python qsearch.py code-wreath-common-span-component-universality-no-go
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO
```

Analyze code wreath mrs coherence escape criterion theorem performance:

```bash
python qsearch.py code-wreath-mrs-coherence-escape-criterion
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION
```

Analyze code wreath mrs transcript povm separation theorem performance:

```bash
python qsearch.py code-wreath-mrs-transcript-povm-separation
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION
```

Analyze code wreath multiscale polar schedule theorem performance:

```bash
python qsearch.py code-wreath-multiscale-polar-schedule
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE
```

Analyze code wreath native frame access boundary theorem performance:

```bash
python qsearch.py code-wreath-native-frame-access-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY
```

Analyze code wreath natural leaf commutator mass theorem performance:

```bash
python qsearch.py code-wreath-natural-leaf-commutator-mass
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS
```

Analyze code wreath natural pair carrier law theorem performance:

```bash
python qsearch.py code-wreath-natural-pair-carrier-law
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW
```

Analyze code wreath operator steiner bulk reduction theorem performance:

```bash
python qsearch.py code-wreath-operator-steiner-bulk-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION
```

Analyze code wreath orientation filter physical access theorem performance:

```bash
python qsearch.py code-wreath-orientation-filter-physical-access
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS
```

Analyze code wreath orientation rank budget theorem performance:

```bash
python qsearch.py code-wreath-orientation-rank-budget
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET
```

Analyze code wreath orientation retention theorem theorem performance:

```bash
python qsearch.py code-wreath-orientation-retention-theorem
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM
```

Analyze code wreath orientation subspace filter theorem performance:

```bash
python qsearch.py code-wreath-orientation-subspace-filter
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER
```

Analyze code wreath pair common covering transition theorem performance:

```bash
python qsearch.py code-wreath-pair-common-covering-transition
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION
```

Analyze code wreath pair core rank concentration theorem performance:

```bash
python qsearch.py code-wreath-pair-core-rank-concentration
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION
```

Analyze code wreath pair polar sampler theorem performance:

```bash
python qsearch.py code-wreath-pair-polar-sampler
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER
```

Analyze code wreath pair polar transport network theorem performance:

```bash
python qsearch.py code-wreath-pair-polar-transport-network
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK
```

Analyze code wreath pair transport degree obstruction theorem performance:

```bash
python qsearch.py code-wreath-pair-transport-degree-obstruction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION
```

Analyze code wreath pair transport native mass boundary theorem performance:

```bash
python qsearch.py code-wreath-pair-transport-native-mass-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY
```

Analyze code wreath partial support child embedding theorem performance:

```bash
python qsearch.py code-wreath-partial-support-child-embedding
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING
```

Analyze code wreath partial support source mass boundary theorem performance:

```bash
python qsearch.py code-wreath-partial-support-source-mass-boundary
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY
```

Analyze code wreath boolean graph stopping core pressure theorem performance:

```bash
python qsearch.py code-wreath-boolean-graph-stopping-core-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE
```

Analyze code wreath component aggregate frame indeterminacy theorem performance:

```bash
python qsearch.py code-wreath-component-aggregate-frame-indeterminacy
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY
```

Analyze code wreath component commutator collision free transfer theorem performance:

```bash
python qsearch.py code-wreath-component-commutator-collision-free-transfer
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER
```

Analyze code wreath component commutator haar benchmark theorem performance:

```bash
python qsearch.py code-wreath-component-commutator-haar-benchmark
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK
```

Analyze code wreath component commutator trace mass bridge theorem performance:

```bash
python qsearch.py code-wreath-component-commutator-trace-mass-bridge
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE
```

Analyze code wreath component green ridge stability theorem performance:

```bash
python qsearch.py code-wreath-component-green-ridge-stability
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY
```

Analyze code wreath component hamming orbit reduction theorem performance:

```bash
python qsearch.py code-wreath-component-hamming-orbit-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION
```

Analyze code wreath component leaf resolved green normal form theorem performance:

```bash
python qsearch.py code-wreath-component-leaf-resolved-green-normal-form
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM
```

Analyze code wreath contiguous all a support pressure theorem performance:

```bash
python qsearch.py code-wreath-contiguous-all-a-support-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE
```

Analyze code wreath contiguous frame target factorization theorem performance:

```bash
python qsearch.py code-wreath-contiguous-frame-target-factorization
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION
```

Analyze code wreath exceptional block graph core pressure theorem performance:

```bash
python qsearch.py code-wreath-exceptional-block-graph-core-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE
```

Analyze code wreath frame subword entropy theorem performance:

```bash
python qsearch.py code-wreath-frame-subword-entropy
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY
```

Analyze code wreath leaf marked green word normal form theorem performance:

```bash
python qsearch.py code-wreath-leaf-marked-green-word-normal-form
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM
```

Analyze code wreath linear code support pressure theorem performance:

```bash
python qsearch.py code-wreath-linear-code-support-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE
```

Analyze code wreath marked pressure obstruction search theorem performance:

```bash
python qsearch.py code-wreath-marked-pressure-obstruction-search
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH
```

Analyze code wreath marked relation topology theorem performance:

```bash
python qsearch.py code-wreath-marked-relation-topology
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY
```

Analyze code wreath mixed split target genus theorem performance:

```bash
python qsearch.py code-wreath-mixed-split-target-genus
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS
```

Analyze code wreath natural leaf commutator trace profile theorem performance:

```bash
python qsearch.py code-wreath-natural-leaf-commutator-trace-profile
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE
```

Analyze code wreath parity stopping core pressure theorem performance:

```bash
python qsearch.py code-wreath-parity-stopping-core-pressure
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE
```

Analyze code wreath periodic frame fiber counterfamily theorem performance:

```bash
python qsearch.py code-wreath-periodic-frame-fiber-counterfamily
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY
```

Analyze code wreath high codimension face word frontier theorem performance:

```bash
python qsearch.py code-wreath-high-codimension-face-word-frontier
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER
```

Analyze code wreath periodic frame rank collapse theorem performance:

```bash
python qsearch.py code-wreath-periodic-frame-rank-collapse
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE
```

Analyze code wreath petz pgm obstruction theorem performance:

```bash
python qsearch.py code-wreath-petz-pgm-obstruction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION
```

Analyze code wreath pgm quantum sampling reduction theorem performance:

```bash
python qsearch.py code-wreath-pgm-quantum-sampling-reduction
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION
```

Analyze code wreath pgm spectral window theorem performance:

```bash
python qsearch.py code-wreath-pgm-spectral-window
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW
```

Analyze code wreath pgm success theorem theorem performance:

```bash
python qsearch.py code-wreath-pgm-success-theorem
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM
```

Analyze code wreath pgm truncation robustness theorem performance:

```bash
python qsearch.py code-wreath-pgm-truncation-robustness
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS
```

Analyze code wreath physical orientation interference theorem performance:

```bash
python qsearch.py code-wreath-physical-orientation-interference
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE
```

Analyze code wreath physical pgm intertwiner theorem performance:

```bash
python qsearch.py code-wreath-physical-pgm-intertwiner
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER
```

Analyze code wreath plancherel kronecker positivity theorem performance:

```bash
python qsearch.py code-wreath-plancherel-kronecker-positivity
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY
```

Isolate the solvable and unresolved equal-pair commutator terms:

```bash
python qsearch.py code-self-dual-wreath-commutators --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT
```

Frobenius' commutator formula contracts a pure product
`product_i chi_lambda_i([r,q])` exactly from tensor-product multiplicities,
with no permutation-pair sum. Complete third moments also couple that
commutator to class functions of `r`, `q`, and `r^-1q`. The sufficient finite
object is therefore a four-class kernel. Controls through `S_6` construct it
exactly and expose splitting of class-triple fibers, but still enumerate
`(n!)^2` pairs. A polynomial recoupling or spin-network contraction remains a
worst-sector and finite-size obligation, not the first natural-source
asymptotic target.

Kill the bounded-tail stable-partition shortcut before investing in it:

```bash
python qsearch.py code-self-dual-wreath-stable-rank --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK
```

The audit measures exact modular ranks of the physical third-moment feature
algebra on finite four-class kernels, then computes the natural mass of
partitions with a fixed number of boxes below the first row. After equal signs
are aggregated, a physical wreath label is an unordered pair of independent
Plancherel source partitions. Fixed-tail source mass is `poly_b(n)/n!`, so
physical pair mass is its square and vanishes rapidly; at `n=64`, the
registered bounded-tail controls are already hundreds of bits below unit
mass. Stable character-polynomial recoupling cannot by itself yield a typical
decoder. The search must move to Plancherel-typical, growing-shape sectors.

Price constant-mass typical portfolios and reject explicit catalogs:

```bash
python qsearch.py code-self-dual-wreath-typical-portfolio --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO
```

The audit computes exact smallest top-Plancherel prefixes reaching 50%, 80%,
and 90% source mass through `n=32`, squares their mass for physical pair-label
coverage, and measures their finite four-class feature rank through `S_6`.
Aggarwal and Elboim's maximal-dimension theorem implies that every fixed-mass
catalog needs `exp(Omega(sqrt(n)))` labels. Precertifying typical partitions is
therefore not a polynomial algorithm. The required object is one reversible
recoupling rule uniform in the sampled partition descriptions.

Type-check known recoupling capabilities before proposing another decoder:

```bash
python qsearch.py code-self-dual-wreath-recoupling-transfer --verbose
python qsearch.py run EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER
```

The transfer audit recognizes three useful partial primitives: the `S_n` QFT,
diagonal YJM target labels, and bounded-support block encodings. It rejects
their substitution for an arbitrary-source internal Kronecker basis,
overlapping `k`-copy associators, the mixed four-class contraction, a uniform
support gap, or a hidden-permutation decoder. The existing fixed typical
separator also has exact scalar collisions on nonzero natural source-pair
mass. The next search target is a partition-description-dependent generator
rule that repairs those collisions and remains coherently implementable.

Apply polynomial-time primal/dual Schur powers and coordinate
puncture/shortening filtrations to every available binary code pair:

```bash
python qsearch.py code-schur-filtration --verbose
```

Schur-profile mismatches are classical rejections. Matching profiles remain
proof debt and still require conductor, support-recovery, and canonical-labeling
attacks.

Run the stronger prime-field conductor and t-closure attack, including a
Reed-Solomon subcode-to-ambient-code recovery calibration:

```bash
python qsearch.py code-closure-attack --verbose
```

Closure mismatches are polynomial-time classical separations. Matching rows
remain proof debt for larger-field support and automorphism recovery.

Search affine-plane incidence-code families and reject AGL(2,q) support
automorphism controls:

```bash
python qsearch.py code-ag-search --verbose
```

Search projective-plane incidence-code families and reject projective-linear
support automorphism controls:

```bash
python qsearch.py code-pg-search --verbose
```

Canonicalize quasi-cyclic collision rows under block automorphisms:

```bash
python qsearch.py code-qc-canonicalize --verbose
```

Resolve quasi-cyclic automorphism proof debt with exact information-set
canonicalization:

```bash
python qsearch.py code-qc-info-resolve --verbose
```

Aggregate code-equivalence rows across structural, tuple-profile,
canonicalization, and quasi-cyclic automorphism baselines:

```bash
python qsearch.py code-triage --verbose
```

Generate weak-invariant code-equivalence collisions and immediately attack them
with stronger classical invariants:

```bash
python qsearch.py code-family-search --verbose
```

Scan candidates and experiment results for classical dequantization blockers:

```bash
python qsearch.py dequantize
```

Run hidden-shift classical baseline sweeps across access models and sample
budgets:

```bash
python qsearch.py baselines
python qsearch.py baselines --sample-counts 4,8,16,32,64,128 --verbose
```

Probe hidden-shift query/time lower-bound gaps with exhaustive sample
fingerprints:

```bash
python qsearch.py query-lower-bounds --verbose
```

Run low-degree and sparse-structure learnability baselines:

```bash
python qsearch.py learnability --verbose
```

Run sparse Fourier and derivative-spectrum compressibility baselines:

```bash
python qsearch.py fourier-learnability --verbose
```

Run multiplicative-character hidden-shift sample/elimination baselines:

```bash
python qsearch.py character-shift --verbose
```

Search for non-exhaustive decoders for multiplicative-character shifts:

```bash
python qsearch.py character-decoders --verbose
```

Build the multiplicative-character sample/decode lower-bound ledger:

```bash
python qsearch.py character-lower-bound --verbose
```

Kill query-lower-bound claims for multiplicative-character shifts by exact
pairwise agreement and random-sample union-bound ceilings:

```bash
python qsearch.py character-query-info --verbose
```

Check exact low-degree moment obstructions for multiplicative-character shifts:

```bash
python qsearch.py character-moments --verbose
```

Audit literature-backed classical upper bounds, fixed-query preprocessing,
advice, amortization, and reduction debt for shifted characters:

```bash
python qsearch.py character-complexity --verbose
```

This audit does not call the nonuniform preprocessing attack a uniform
dequantization. It kills query-advantage and unconditional-online claims, then
requires the remaining single-instance decoding gap to carry explicit
preprocessing exclusions plus a natural reduction or named hardness assumption.

Reject artificial hash/noise/mask phase families:

```bash
python qsearch.py phase-naturalness --verbose
```

Search natural rational finite-field trace-function families:

```bash
python qsearch.py trace-functions --verbose
```

Triage phase families across all hidden-shift baseline artifacts:

```bash
python qsearch.py family-triage --verbose
```

Run executable registry experiments directly:

```bash
python qsearch.py run --list-supported
python qsearch.py run EXP-DHS-GOWERS-SPECTRUM
python qsearch.py run --all-supported
python qsearch.py run-next
python qsearch.py run-next --dry-run
python qsearch.py trends --verbose
```

Run parameter sweeps for scaling histories:

```bash
python qsearch.py sweep
python qsearch.py sweep --n-values 5,6,7,8 --sample-counts 256,512,1024,2048
```

Build per-candidate proof-obligation status records:

```bash
python qsearch.py proofs
```

Build certificate-gated directed reduction routes and block ontology-adjacency
claims that lack model, promise, overhead, uniformity, preprocessing, family
coverage, or proof provenance:

```bash
python qsearch.py reductions --verbose
```

Audit those routes against exact primary-source theorem contracts. This catches
the non-composable step between, for example, Regev's dihedral coset samples and
a candidate that assumes a public coherent phase evaluator:

```bash
python qsearch.py reduction-contracts --verbose
```

Build a ranked proof-debt work queue with commands, success criteria, and kill
criteria:

```bash
python qsearch.py proof-queue --verbose
```

Build conjecture, assumption, reduction, and blocker records:

```bash
python qsearch.py conjectures
```

Generate blocker-guided mutation proposals:

```bash
python qsearch.py mutate
```

Cluster active blockers into actionable failure modes:

```bash
python qsearch.py blockers --verbose
```

Rank research frontiers from the current evidence:

```bash
python qsearch.py frontiers --verbose
```

Build candidate-level query-model and lower-bound obligations:

```bash
python qsearch.py query-models --verbose
```

Ingest local paper text, LaTeX, Markdown, or PDFs when available:

```bash
python qsearch.py ingest-papers papers/
python qsearch.py ingest-papers --arxiv-id 0911.4724
```

arXiv ingestion prefers source archives over flattened PDFs. Theorem records
retain LaTeX, labels, source-line locators, and confidence. The live Regev
source audit corrected the DCP contract to include its `f=1` bad-register
promise and the `N=(2M)^n`, `M=2^(4n)` parameter map.

Register built-in proof-gated seed candidates:

```bash
python qsearch.py propose
```

Validate the registry:

```bash
python qsearch.py validate
```

List registry records:

```bash
python qsearch.py list
```

Run structural-test unit checks:

```bash
python -m unittest discover -s tests
```

Generated outputs:

- `research/agenda.json` - machine-readable domains, candidates, scores, and
  experiments.
- `research/project_plan.md` - readable diagnosis, ranked leads, and experiment
  roadmap.
- `research/exhaustive_audit.md` - ranked intervention portfolio, module
  deletion decisions, proof obligations, and self-critique passes.
- `research/interventions.json` - machine-readable improvement ranking with
  expected breakthrough lift, difficulty, dependencies, failure modes, and
  falsifiers.
- `research/proof_obligations.json` - hard rejection criteria for future
  candidate algorithms.
- `research/problem_ontology.json` - problem/reduction/no-go graph.
- `research/literature_index.json` - curated seed papers tagged by mechanism
  and barrier.
- `research/literature_records.json` - extracted mechanism, problem family,
  reduction, no-go barrier, proof technique, open question, and reusable
  abstraction records.
- `research/registry/candidates.json` - proof-gated research candidates.
- `research/registry/experiments.json` - falsifiable experiment records.
- `research/registry/experiment_results.json` - executed experiment/workbench
  results with metrics, artifacts, and triggered falsifiers.
- `research/registry/dequantization_checks.json` - blocking classical-baseline
  findings generated from candidates, experiment results, and negative-result
  anti-patterns.
- `research/registry/proof_status.json` - per-candidate proof-obligation
  statuses linking proof text, experiment evidence, falsifiers, and
  dequantization blockers.
- `research/registry/scaling_runs.json` - parameter sweep summaries and links
  to scaling artifacts.
- `research/registry/conjectures.json` - candidate-level conjectures, explicit
  assumptions, reduction links, supporting evidence, and blocking evidence.
- `research/registry/mutation_proposals.json` - blocker-guided proposal records
  that suggest how to mutate away from dequantized families; strong mutations
  are proof-gated before promotion and weak mutations are rejected.
- `research/registry/rejected_candidates.json` - generated or submitted
  hypotheses rejected by the proof gate, with exact proof-obligation issues.
- `research/registry/negative_results.json` - negative results and legacy
  anti-patterns.
- `research/phase_workbench/hidden_shift_audit.json` - explicit cyclic
  and F_2 hidden-shift family audits, query-model-aware classical baselines,
  derivative spectra, query lower-bound probes, scaling histories, explicit
  phase-state merge traces, and DHSP phase-label sieve search.
- `research/phase_workbench/dcp_sample_native_sieve.json` - full-family DCP
  state-input contract, physical branch/postselection accounting, generic
  signed-label merge-rule trials, and explicit parity-versus-full-decoder debt.
- `research/phase_workbench/phase_family_triage.json` - cross-baseline hidden
  shift family decisions: rejected by reconstruction, query/time gap only, or
  unresolved without being counted as positive evidence.
- `research/phase_workbench/phase_family_naturalness.json` - naturalness and
  description-complexity audit that rejects hash-masked/noisy phase families
  unless a real algebraic/reduction source is supplied.
- `research/phase_workbench/trace_function_search.json` - generated rational
  finite-field trace-function families, immediately attacked by low-degree,
  sparse-spectrum, and sampled candidate-elimination baselines.
- `research/coset_workbench/nonabelian_hsp_audit.json` - strongly regular
  graph-pair audits, scalable CFI-style parity benchmarks, WL/spectral/classical
  invariant baselines with higher-k tuple scaling caps, low-register
  relation-observable checks, exact GI sanity certificates, and coset
  negative-result records when classical invariants already explain a signal.
- `research/coset_workbench/individualized_tensor_observables.json` -
  individualized rooted graphlet/tensor signatures that classify separators as
  classical shadows and cap-limited rows as proof debt.
- `research/coset_workbench/godsil_mckay_switching_search.json` -
  Godsil-McKay cospectral row search with WL, graphlet, individualization, and
  rooted-tensor dequantization checks.
- `research/coset_workbench/coset_frontier_triage.json` - aggregate gate that
  rejects graph/coset rows killed by WL, tensor, individualization, rooted
  tensor, CFI base-family, CFI scaling, or structural CFI evidence before
  measurement design.
- `research/representation/coset_holevo_information.json` - exact one-copy
  Holevo character formula, same-hidden multi-copy information bound, and
  class-specific Fano copy budgets; explicitly records that the polynomial
  bound constructs neither a collective measurement nor a decoder.
- `research/code_equivalence/code_equivalence_audit.json` - binary linear-code
  equivalence controls, weight enumerators, support-splitting fingerprints,
  known-permutation certificates, and code-invariant negative results.
- `research/code_equivalence/code_frontier_triage.json` - aggregate code gate
  that merges structural, tuple-profile, information-set, canonicalization,
  low-weight matroid, profile-collision, cyclic-code, BCH, Reed-Muller,
  rank-metric, affine-geometry, projective-geometry, and quasi-cyclic evidence before code rows can feed
  nonabelian coset measurement design.
- `research/code_equivalence/code_low_weight_structure.json` - low-weight
  codeword support hypergraph/matroid baseline that rejects rows separated by
  minimum distance, support spectra, coordinate/pair support profiles, or
  incidence-WL signatures; imports cyclic/QC/BCH/Goppa/Tanner/Reed-Muller/
  rank-metric/affine-geometry/projective-geometry control certificates and runs exact low-weight
  incidence-graph isomorphism under a cap.
- `research/code_equivalence/qc_information_set_resolver.json` - exact
  ordered information-set resolver for quasi-cyclic rows left as proof debt by
  restricted automorphism checks.
- `research/code_equivalence/cyclic_code_search.json` - binary cyclic-code
  divisor search that treats tuple-profile collisions as suspect until
  dihedral/multiplier automorphisms and profile-pruned canonicalization fail
  to explain them.
- `research/code_equivalence/bch_code_search.json` - primitive BCH search from
  GF(2^m) cyclotomic cosets and minimal polynomials; duplicate defining sets,
  decimation controls, dual-code classical rejections, and unresolved dual
  canonicalization caps are recorded as negative controls or proof debt, not
  evidence.
- `research/code_equivalence/goppa_code_search.json` - binary Goppa/alternant
  code search over small `GF(2^m)` windows with structural, tuple-profile,
  semilinear automorphism, and canonicalization controls.
- `research/code_equivalence/goppa_scaling_frontier.json` - punctured
  Goppa/alternant scaling rows through length 160 with exact dual
  weight/incidence signatures where feasible, Schur/hull invariants,
  permutation controls, semilinear support checks, and explicit baseline-cap
  proof debt.
- `research/code_equivalence/tanner_code_search.json` - regular Tanner/LDPC
  code-family search that treats tuple-profile collisions as suspect until
  Tanner graph isomorphism, information-set canonicalization, and code triage
  fail to explain them.
- `research/code_equivalence/reed_muller_code_search.json` - punctured
  Reed-Muller/evaluation-code search with affine-support automorphism controls,
  tuple-profile buckets, low-weight support checks, and canonicalization.
- `research/code_equivalence/rank_metric_code_search.json` -
  binary-expanded Gabidulin/rank-metric search with symbol-block permutation
  controls, tuple-profile buckets, low-weight support checks, and
  canonicalization.
- `research/code_equivalence/code_incidence_resolver.json` - exact
  support-colored codeword-coordinate incidence-isomorphism certificates for
  tractable rank-metric and quasi-cyclic proof-debt rows, including verified
  coordinate permutations and explicit expansion/time caps.
- `research/code_equivalence/self_dual_code_boundary_search.json` - certified
  growing-hull self-dual families, polynomial invariant collisions, exact
  finite controls, and explicit cap/timeout proof debt.
- `research/code_equivalence/self_dual_local_profile_obstruction.json` -
  minimum-distance certificates and the self-dual puncture/shorten theorem
  showing when bounded local rank-hull signatures are forced to collapse.
- `research/code_equivalence/self_dual_global_orbit_audit.json` -
  information-set orbit measurements, exact normalized-key controls,
  Construction-A unimodular lattice invariants, and reverse-reduction debt.
- `research/representation/self_dual_code_hsp_applicability.json` - exact
  `GL_k(F_2) x S_n` wreath-product HSP contract, group-size accounting,
  per-hypothesis literature no-go checks, and the high-rate applicability gap.
- `research/code_equivalence/code_schur_filtration.json` - primal and dual
  Schur-power dimensions plus coordinate puncture/shortening square profiles
  for every available binary code-equivalence pair.
- `research/code_equivalence/code_closure_attack.json` - exact prime-field
  conductors, t-closures, local closure signatures, and ambient evaluation-code
  support-recovery calibrations.
- `research/code_equivalence/affine_geometry_code_search.json` -
  affine-plane line-incidence code search with AGL(2,q) support automorphism
  controls, affine line/parallel-class support profile collision search, and
  standard code-baseline attacks.
- `research/code_equivalence/projective_geometry_code_search.json` -
  projective-plane line-incidence code search with projective-linear support
  automorphism controls, support line-intersection profile collision search,
  and standard code-baseline attacks.
- `research/dequantization_report.json` - summary report of active
  dequantization blockers.
- `research/dequantization_attack_matrix.json` - attack-legality and
  query-model matrix for hidden-shift baselines.
- `research/classical_baselines/hidden_shift_baselines.json` - sampled,
  evaluator, and full-table hidden-shift baseline sweeps across families,
  n-values, and query budgets.
- `research/classical_baselines/hidden_shift_query_lower_bounds.json` -
  family-agnostic sample-fingerprint probes that separate undersampled
  random-access gaps from polynomial-sample/exhaustive-decoding query-time
  gaps.
- `research/classical_baselines/learnability_baselines.json` - direct
  low-degree learnability audits, including exact ANF degree over `F_2^n` and
  finite-difference degree tests over prime-field/vector-space phase families.
- `research/classical_baselines/fourier_compressibility_baselines.json` -
  sparse Fourier and derivative-spectrum audits with query estimates,
  sample-budget legality, and negative-result records for spectrally
  compressible hidden-shift families.
- `research/classical_baselines/character_shift_baselines.json` -
  Legendre/quartic-character shift sample-elimination traces that separate
  polynomial sample information from domain-size candidate enumeration.
- `research/classical_baselines/character_decoder_search.json` -
  non-exhaustive decoder attempts, shift-invariant obstruction probes, and
  exhaustive moment-signature baselines for multiplicative-character shifts.
- `research/classical_baselines/character_shift_lower_bound.json` -
  Legendre/quartic sample fingerprints, chosen-query fingerprints, full-degree
  cyclotomic GCD recovery, pair-ratio candidate filtering, and explicit
  decoding lower-bound obligations.
- `research/classical_baselines/character_query_information.json` -
  Legendre/quartic pairwise agreement profiles and union-bound random-sample
  query ceilings, blocking superlogarithmic query-lower-bound claims.
- `research/classical_baselines/character_moment_obstruction.json` -
  exact finite-field moment checks showing where low-degree full-domain moment
  regression first sees multiplicative-character signal.
- `research/classical_baselines/character_shift_complexity.json` -
  literature-backed query/time upper bounds and executable fixed-prefix
  preprocessing attacks, with separate uniform, nonuniform, advice, amortized,
  lower-bound, and natural-reduction fields.
- `research/proof_status_report.json` - summary report of active proof
  obligation blockers.
- `research/proof_debt_report.json` - ranked proof debts, lemma obligations,
  reduction edges, and counterexample searches.
- `research/proof_work_queue.json` - clustered proof-debt work items with
  executable commands, dependencies, success criteria, and kill criteria.
- `research/reductions/reduction_ledger.json` - typed reduction edge
  certificates and complete-route decisions from natural source problems to
  restricted candidate algorithm families.
- `research/reductions/theorem_contracts.json` - exact source promise, target
  solver interface, access capabilities, parameter regime, success condition,
  and limitations for each accepted primary-source reduction construction.
- `research/reductions/interface_audit.json` - candidate-by-route checks for
  group/domain compatibility, access conversion, full-family coverage,
  parameters, decoder success, and uniform instance construction.
- `research/registry/reductions.json` - registry copy of the reduction ledger
  used by validation, proof status, and conjecture tracking.
- `research/experiment_run_history.json` - append-only experiment execution
  history.
- `research/experiment_trends.json` - trend summaries over repeated experiment
  runs and falsifier histories.
- `research/scaling/hidden_shift_sweep.json` - hidden-shift scaling rows over
  n, sample budgets, sieve strategies, dequantization risk, and restricted query
  model survival.
- `research/conjecture_report.json` - summary of active conjectures and their
  falsification/blocker state.
- `research/mutation_report.json` - mutation proposals tied to specific
  conjecture blockers, proof debts, proof-gate preflights, and negative-result
  lessons.
- `research/blocker_taxonomy.json` - ranked blocker classes across
  dequantization findings, proof debts, and negative results, with the top
  actionable failure mode.
- `research/frontier_map.json` - evidence-based ranking of next research
  frontiers, currently favoring nonabelian coset/code collective-observable
  work over dead hidden-shift phase-family reuse.
- `research/query_model_ledger.json` - candidate-level access-model ledger
  listing quantum access assumptions, comparable classical access models,
  attacks that must be excluded, and missing lower-bound obligations.
- `research/representation/coset_pgm_capacity.json` - PGM copy/capacity
  ledger for involution coset states, recording explicit-measurement scale and
  measurement-design proof debt.
- `research/paper_ingestion.json` - extracted mechanism records from local
  papers, LaTeX sources, text files, Markdown notes, or PDFs.
- `research/literature_no_go_index.json` - extracted no-go/lower-bound/barrier
  statements from ingested literature.

## Important Files

- `research_engine.py` - ranks research hypotheses and writes the agenda.
- `research_lab.py` - produces the exhaustive audit and intervention portfolio.
- `literature_radar.py` - stores seed literature and can refresh arXiv metadata.
- `literature_pipeline.py` - ingests literature records and generates
  proof-gated hidden-shift/coset-state hypotheses with falsifiable experiments.
- `phase_state_workbench.py` - generates explicit hidden-shift phase families,
  including prime-field chirps, finite-field multiplicative characters,
  Kloosterman-style finite-field trace phases, noncyclic `F_p^2` quadratic
  forms, F_2 quadratic/bent forms, and masked/noisy
  algebraic phases, plus Maiorana-McFarland-style split Boolean phases; audits Fourier/derivative structure,
  full-table/sample-limited/evaluator baselines, algebraic reconstruction
  attacks, and generic/family-specific DHSP phase-label sieve schedules.
- `dcp_sample_workbench.py` - replaces the idealized favorable-branch sieve as
  the authoritative DHSP baseline: it consumes only independent DCP states,
  admits zero-information Fourier labels, charges physical combine outcomes,
  searches generic signed merge rules, and blocks valuation-only success
  claims until a complete uniform decoder and lattice composition exist.
- `dcp_recursive_decoder.py` - exhaustively checks accumulated low-residue phase
  correction, runs fresh-batch LSB-first reflection decoding, charges all state
  samples, and records empirical recovery separately from unproved bounded-error
  and asymptotic claims.
- `dcp_recurrence_analysis.py` - verifies exact one-pair transition kernels,
  compares stronger legal bucket matchings, excludes raw-input target hits, and
  sweeps endpoint yields with confidence intervals. Its finite scaling fits are
  blocked from promotion until adaptive bucket dependence and recursive failure
  are controlled symbolically.
- `dcp_schedule_search.py` - mutates legal bucket schedules, selects only on
  training seeds, and compares once against the default schedule on disjoint
  holdout seeds. Statistical gains remain blocked until converted into a
  uniform recurrence and named resource-frontier improvement.
- `dcp_uniform_schedule_family.py` - compresses per-size schedules into one
  `ceil(c sqrt(log N))` block grammar, freezes `c`, and tests larger unseen
  moduli. Any gain is classified as constant tuning inside the known generic
  subexponential class, not a new algorithmic class.
- `dcp_bad_register_audit.py` - injects hidden arbitrary basis-state registers
  at the exact `f=1` theorem rate, propagates contamination through legal
  merges, and measures corrupted endpoints and recursive parity-bit risk.
- `dcp_contamination_witness.py` - derives exact hidden-reflection-averaged
  density operators from public Fourier labels, proves local and
  collision-free-batch indistinguishability from allowed randomized bad basis
  states, and isolates global subset-sum correlations without pretending that
  exponential relation enumeration is an efficient measurement.
- `dcp_collective_witness_search.py` - formalizes bounded-support X/Y
  correlators as signed modular label relations, exhaustively searches the
  finite regime, and certifies that logarithmic-locality Pauli witness classes
  have negligible aggregate signal over polynomial random-label pools.
- `dcp_clifford_witness_search.py` - exactly evaluates public-label-derived
  global CZ-plus-Hadamard measurements, separating unrestricted output total
  variation from polynomial-time Hamming-weight decoding and refusing to treat
  finite bias as an adversarial robustness or full-decoder theorem.
- `dcp_clifford_contamination.py` - replaces every coordinate in turn by each
  allowed bad basis value, minimizes the efficient Clifford statistic without
  exposing the bad location, and keeps one-bad survival separate from the full
  `f=1` theorem promise.
- `dcp_hadamard_scaling.py` - sweeps phase-state count relative to `log2(N)`,
  computes exact Hamming distributions for every hidden reflection, and proves
  an average-case full-output TV upper bound below the critical ratio
  `1/log2(3/2)` before treating supercritical finite signals as proof debt.
- `dcp_random_design_decoder.py` - measures random-label phase states in local
  X/Y bases, recovers the planted noisy Fourier peak with a full length-`N`
  FFT, and records the polynomial-sample but exponential-time/memory gap rather
  than presenting it as an efficient DCP algorithm.
- `dcp_decoder_frontier.py` - compares FFT, Grover likelihood search, generic
  Kuperberg/Regev sieves, illegal chosen-label phase estimation, Clifford
  statistics, and the polynomial target under one access, robustness, decoder,
  and lattice-composition ledger.
- `dcp_multiscale_aliasing_audit.py` - proves raw random labels need about
  `2^(n-b)` samples and pair differences need birthday scale
  `2^((n-b)/2)` to expose an effective `b`-bit modulus, while explicitly
  leaving deeper global/quantum decoders outside the restricted no-go.
- `dcp_hidden_number_bridge.py` - derives the exact random-label X/Y
  observation channel, proves logarithmic sample sufficiency for exhaustive
  correlation under the `f=1` bad-register promise, and keeps HNP/LPN/LWE
  analogies separate from reductions.
- `dcp_sparse_fourier_transfer_audit.py` - checks sparse-Fourier access models
  against iid DCP samples and proves only a restricted constant-arity schedule
  synthesis obstruction; it does not claim a general random-example lower
  bound.
- `dcp_iid_hash_estimator_audit.py` - applies normalized Parseval identities to
  certify the sample-versus-bucket tradeoff for exact unbiased one-pass linear
  iid hash estimators.
- `dcp_likelihood_branch_bound.py` - implements exact nonlinear likelihood
  localization with rigorous interval upper bounds and records that the tested
  branch-and-bound still evaluates all `N` reflection candidates.
- `dcp_biased_linear_margin_audit.py` - extends the Parseval obstruction from
  exact indicators to one-pass linear scores with a uniform decision margin and
  an explicit empirical-mean MSE contract.
- `dcp_multirecord_estimator_hierarchy.py` - proves a restricted no-go for
  fixed-degree multilinear kernels on disjoint iid blocks, verifies signed-label
  uniformity, and keeps overlapping, adaptive, implicit, and collective classes
  open as separate obligations.
- `dcp_ustatistic_variance_audit.py` - applies exact Hoeffding variance
  coefficients to overlapping product kernels, separating exponential explicit
  tuple evaluation from the still-open possibility of a polynomial implicit
  contraction.
- `dcp_factorized_contraction_audit.py` - proves that the rank-one
  elementary-symmetric implicit contraction remains sample-exponential, while
  isolating polynomial-rank and low-bond tensor contractions as the next open
  classes.
- `dcp_low_rank_contraction_search.py` - searches polynomial-rank closed-form
  response dictionaries with a worst-point margin LP and exact all-order
  covariance, rejecting finite separators whose records, precision, or total
  contraction work are superpolynomial.
- `dcp_subset_sum_measurement_audit.py` - proves the compute-sum/QFT
  no-information identity, certifies exponential exact residue-tracking bond
  dimension, and isolates approximate fiber symmetrization as the surviving
  collective architecture.
- `dcp_subset_sum_bridge.py` - formalizes the primary-source conditional route
  from a density-one partial modular subset-sum solver to exact `f=1` DCP and
  separates that weaker sufficient primitive from full-fiber PGM preparation.
- `dcp_subset_sum_lattice_search.py` - tests deterministic exact-LLL embeddings
  with fixed-arity extraction, verifies every witness, and refuses to promote
  small-instance recovery without a uniform coverage and reversibility theorem.
- `dcp_subset_sum_two_adic_search.py` - audits symbolic opportunities specific
  to modulus `2^n` by measuring carry-lift degree and affine overcoverage while
  recording exponential truth-table fitting as negative evidence, not an
  algorithm.
- `dcp_subset_sum_resource_frontier.py` - records source-linked exact,
  dissection, generalized-birthday, representation, and quantum subset-sum
  exponents; separates theorem and heuristic assumptions; and rejects every
  positive exponential exponent as insufficient for Regev's polynomial
  partial-solver contract.
- `dcp_subset_sum_carry_anf.py` - computes exact full-domain carry-bit ANFs by
  Boolean Mobius transform, eliminating restricted-fiber interpolation as an
  explanation; it gates bounded-degree algebraic reconstruction without
  claiming a lower bound against other subset-sum algorithms.
- `dcp_subset_sum_solver_synthesis.py` - composes typed lattice, 2-adic,
  representation, decoding-reduction, and coherent-walk primitives into
  falsifiable research programs; weak negative-result matches are rejected and
  survivors remain proposal-only until all source-contract theorems exist.
- `dcp_subset_sum_low_bit_bdd.py` - proves an exact polynomial branching
  program and conditional state-preparation route for `O(log n)` low congruence
  bits, while certifying that linear residual entropy leaves the high-bit
  witness problem open.
- `dcp_subset_sum_conditioned_quotient.py` - computes the exact high-bit
  quotient law after logarithmic low-bit conditioning and rejects explicit
  polynomial residue lists without turning broad finite entropy into a lower
  bound against implicit decoders.
- `dcp_subset_sum_carry_slice_lattice.py` - compares unsliced modular LLL with
  every polynomially enumerable exact low-carry slice and keeps the route
  blocked until an average-case short-vector separation and coverage theorem
  exists.
- `dcp_carry_high_part_no_go.py` - proves the exact low/high product law,
  carry-target translation bijection, and polynomial carry-family union bound.
  It rejects low-only quotient-bias claims while leaving genuinely joint
  low/high reduced-basis geometry open.
- `dcp_subset_sum_preconditioned_geometry.py` - proves that every fixed
  logarithmic low-bit fiber has pairwise-independent uniform high residuals,
  with exact window-count mean and variance. It rejects count-only geometry
  explanations while leaving higher-order and reduced-basis mechanisms open.
- `dcp_subset_sum_fourth_moment_obstruction.py` - proves three-wise residual
  independence, localizes the first possible fixed-order signal to xor-zero
  affine quadruples, and computes their exact low-fiber additive energy by
  Walsh transform without promoting finite energy trends to a decoder theorem.
- `dcp_subset_sum_signed_l2_obstruction.py` - proves conditional pairwise
  independence and the exact signed variance identity for sparse exact-hit
  scores chosen from exposed low bits, while preserving full-label adaptive,
  dense implicit, nonlinear, and reduced-basis routes as explicit open cases.
- `dcp_subset_sum_sparse_character_obstruction.py` - proves a simultaneous
  growing-moment bound over all nonzero subset-sum Fourier characters, closing
  every polynomially sparse dictionary even under full-label and target
  adaptation while leaving dense implicit contraction explicitly open.
- `dcp_subset_sum_qtt_contraction_search.py` - tests direct target-bit
  quantized tensor trains using exact count vectors, multiple bit orderings,
  additive-half singular-tail rank requirements, and histogram-preserving
  controls without promoting finite rank growth to a lower bound.
- `dcp_pgm_gram_block_encoding.py` - constructs and finite-checks the exact
  projected DCP Gram encoding, proves its factor-`N` normalization and
  source-conditioned generic fiber-amplification obstruction, while leaving
  structured preconditioners and collision walks open.
- `dcp_pgm_qsvt_degree_obstruction.py` - applies Markov's inequality to prove
  exponential bounded-polynomial degree for generic transforms of the direct
  count and amplitude encodings, with an exact all-`n` source certificate and
  a quenched random-source transfer gate.
- `dcp_subset_sum_quenched_occupancy_theorem.py` - extends fixed-order
  lattice transfer to two target groups, proves concentration of empirical
  factorial moments and the Poisson(1) quenched fiber law, and validates the
  theorem against exact small source ensembles.
- `dcp_coherent_fiber_erasure_boundary.py` - separates black-box index
  erasure from public arithmetic and independent-state DCP access, proves
  target-addressable support-decision and fixed-variable witness reductions,
  and preserves global collective channels as an explicit open interface.
- `dcp_global_erasure_inversion_reduction.py` - proves that PGM-compatible
  common-garbage coherent erasure is invertible into normalized fibers and,
  using the quenched target-law bound, conditionally equivalent to an average
  density-one subset-sum witness solver.
- `dcp_approximate_erasure_coherence_reduction.py` - extends the conditional
  reduction to exact erasure isometries with arbitrary target-dependent
  garbage by preparing their weighted mean and proving a polynomial
  uniform-legal fidelity transfer.
- `dcp_erasure_perturbation_reduction.py` - propagates operator-norm circuit
  error through reference postselection and inverse witness preparation,
  proving that inverse-polynomial precision preserves the solver reduction.
- `dcp_subset_sum_target_distribution.py` - separates independent uniform,
  uniform-legal, and planted target multiplicity laws so size-biased planted
  experiments cannot masquerade as evidence under Regev's source contract.
- `dcp_coherent_matching_interface.py` - extracts every deterministic use in
  Regev's matching routine, proves a conditional lift for explicit
  target-independent shared-seed randomized solvers, and gives a zero-visibility
  counterexample for arbitrary quantum relation solvers with orthogonal
  workspaces. This broadens the eligible solver search but constructs no solver.
- `dcp_symmetric_relation_lift.py` - replaces deterministic selection and
  native one-call workspace overlap with a proved symmetric double-evaluation
  interface. It establishes conditional fixed-list and global-source success
  transfers but still requires a polynomial relation solver.
- `dcp_two_adic_fiber_transport.py` - proves exact low-fiber child transports,
  then closes polynomial explicit local dictionaries at linear depth while
  retaining target-dependent partial and walk-based architectures.
- `dcp_fiber_transport_graph.py` - exactly audits local-move fiber components,
  absolute spectral gaps, cross-child mass, and same-graph classical BFS. All
  tested linear-depth graphs fragment; finite gaps are never promoted.
- `dcp_signed_permutation_transport.py` - proves that every total coordinate
  permutation with bit complements collapses exactly to the original
  exact-valuation pivot condition. This closes the signed-coordinate global
  transport class at linear depth without overclaiming against nonlinear,
  coordinate-mixing, partial, or walk transports.
- `dcp_affine_transport.py` - derives necessary and sufficient integer-ANF
  congruences for every GF(2)-affine transport and proves that `T(0)` is already
  the target subset-sum witness. The total affine route is closed by the more
  general Fourier theorem; the verifier remains useful for partial proposals.
- `dcp_fiber_balance_obstruction.py` - proves by factored Fourier coefficient
  that every total full-cube next-bit bijection, including nonlinear maps,
  exists exactly when the original exact-valuation pivot exists. It separately
  measures target-fiber balance and optimal partial-pairing mass without
  treating set-theoretic pairability as an efficient algorithm.
- `dcp_partial_relation_coverage.py` - proves that at linear 2-adic depth all
  fixed signed-difference masks have linear support with exponentially high
  probability, so polynomial explicit dictionaries have exponentially small
  subset-sample-weighted coverage. It leaves only implicitly target-indexed or
  nontranslation partial maps in this branch.
- `dcp_target_indexed_locality.py` - removes the remaining local loophole:
  for a fixed source, target dependence chooses a flip support but the source
  fixes every sign, giving an exact `H_2(beta)-alpha` Hamming-ball exponent.
  Thus arbitrary target-indexed maps below the entropy-distance threshold fail
  on all but exponentially rare random inputs. Linear-support relation samplers
  remain open because output distance is not a computational lower bound.
- `dcp_fiber_entanglement.py` - gives the exact Schmidt spectrum of a modular
  subset-sum fiber from left/right residue multiplicities and proves that a
  constant fraction of random linear-depth fibers have exponential exact bond
  dimension. A second-moment purity theorem also forces exponential bond rank
  for 99-percent Schmidt mass with high probability, simultaneously across any
  fixed polynomial dictionary of balanced coordinate layouts. This deletes
  exact and approximate low-bond density-one tensor preparation and naive
  layout search, but deliberately leaves fully label-adaptive layouts, general
  quantum circuits, and inverse-polynomial partial solvers open.
- `dcp_adaptive_layout_audit.py` - attacks the remaining label-adaptive tensor
  loophole. A binomial large-deviation theorem rules out growing balanced
  2-adic subgroup compression even when the cut is chosen after seeing all
  labels. Exact small-cut optimization and heuristic additive-layout search are
  retained only as conjecture probes because every Schmidt score costs
  `O(n 2^q)`; no polynomial selector, contraction, or relation solver exists.
- `dcp_subset_sum_random_self_reduction.py` - proves exact signed/odd-unit
  witness and source bijections, proves sign-only centered embeddings are
  isometric controls, and tests polynomially many odd-unit presentations as a
  shared-seed randomized LLL class without promoting finite rescues to coverage.
- `dcp_odd_unit_orbit_geometry.py` - certifies the full 2-adic invariant
  boundary of odd-unit orbits, records normalized LLL geometry, and evaluates
  fixed feature thresholds on disjoint held-out units. Surviving enrichment is
  hypothesis input only until an easy-orbit measure and decoding theorem exist.
- `candidate_quarantine.py` - removes mutation candidates from the accepted
  registry when an exact theorem-contract audit proves their access model is
  unavailable, while preserving the failure in rejected and negative-result
  registries.
- `phase_family_triage.py` - merges hidden-shift, low-degree, sparse Fourier,
  query-lower-bound, and character-shift baseline artifacts into a single
  reject/unresolved/query-gap decision table so dead families are not reused as
  evidence.
- `phase_family_naturalness.py` - rejects phase families whose apparent
  hardness comes from artificial hash masks, noise, hidden tables, or unclear
  descriptions rather than natural algebraic/reduction structure.
- `trace_function_search.py` - searches natural Kloosterman/two-pole/cubic
  rational trace phases over finite fields and records any survivor only as
  lower-bound debt.
- `classical_baseline_suite.py` - runs hidden-shift classical baseline sweeps
  over sampled, full-table, and evaluator access models and writes
  negative-result records for dequantized families.
- `hidden_shift_query_lower_bounds.py` - counts candidate shifts consistent
  with sampled hidden-shift fingerprints, labels undersampled rows, and blocks
  query-only claims when polynomial samples identify shifts only through
  exhaustive enumeration.
- `learnability_baselines.py` - detects low-degree and sparse algebraic
  structure directly, including exact ANF degree/sparsity over `F_2^n`, so
  phase families that are classically interpolable or sparse-polynomial
  learnable are rejected before they become hidden-shift evidence.
- `fourier_compressibility_baselines.py` - applies sparse Fourier and
  derivative-spectrum dequantization pressure, distinguishing full-table,
  evaluator, and sample-limited access before a hidden-shift signal is treated
  as meaningful.
- `character_shift_baselines.py` - audits multiplicative-character hidden
  shifts by candidate-set elimination, making explicit when samples identify a
  shift only through exponential-time enumeration.
- `character_decoder_search.py` - searches for non-exhaustive character-shift
  decoders and records pair-ratio candidate filtering, exhaustive
  candidate-scoring, and full-degree algebraic successes as lower-bound debt,
  not speedup evidence.
- `character_shift_lower_bound.py` - compares random/chosen sample
  fingerprinting, pair-ratio candidate filtering, full-degree cyclotomic GCD
  decoding, and candidate enumeration for Legendre/quartic shifts; emits
  lower-bound debt only.
- `character_query_information.py` - computes exact pairwise agreement profiles
  and random-sample union-bound query ceilings for multiplicative-character
  shifts, forcing any remaining claim to be a computational decoding-time
  lower-bound claim.
- `character_moment_obstruction.py` - computes exact multiplicative-character
  field moments and records the first nonzero degree as a narrow obstruction to
  low-degree moment-regression attacks.
- `character_shift_complexity.py` - records shifted-power classical upper
  bounds and tests fixed chosen-query fingerprint tables, preventing query or
  online-with-advice gaps from being promoted as uniform speedup evidence.
- `coset_state_workbench.py` - audits hidden-permutation graph pairs, including
  Shrikhande vs 4x4 rook and scalable CFI-style parity twists, against WL,
  spectrum, relation-algebra, exact small-instance GI, and walk-count
  baselines; tracks higher-k WL tuple caps as a classical proxy for
  low-register collective relation observables.
- `individualized_tensor_observables.py` - runs individualized rooted
  graphlet/tensor signature baselines so apparent collective-observable signals
  must survive rooted classical shadows, not only unrooted graphlet counts.
- `godsil_mckay_search.py` - generates natural cospectral graph rows by
  Godsil-McKay switching, verifies non-isomorphism, and rejects rows separated
  by classical WL, graphlet, individualization, or rooted-tensor baselines.
- `coset_frontier_triage.py` - aggregates coset/nonabelian row evidence across
  classical baselines, CFI base/scaling probes, and CFI structural decoders;
  writes reject/proof-debt decisions before any row can feed
  collective-measurement search.
- `code_equivalence_workbench.py` - audits binary linear-code equivalence
- `code_hull_projector_reduction.py` - certifies the trivial-hull code-to-weighted-GI iff reduction, samples unconditioned hull scaling, and audits planted random-code controls
  controls with GF(2) rank, weight enumerators, column invariants,
  weak-invariant collision pairs, support-splitting-style fingerprints,
  known-permutation certificates, and bounded exact permutation sanity checks.
- `cfi_code_reduction.py` - proves an explicit graph-isomorphism iff binary
  code-equivalence construction using multiplicity-tagged vertex points,
  recovers the unlabeled graph after arbitrary row operations and coordinate
  permutations, separates explicit-generator access from sample/state-only
  models, and rejects current promised CFI code rows when graph-side parity
  decoders remain legal.
- `code_frontier_triage.py` - aggregates code-equivalence row evidence across
  structural invariants, tuple profiles, information-set canonicalization,
  low-weight matroid baselines, profile collisions, cyclic-code controls,
  Reed-Muller affine-support controls, and quasi-cyclic automorphism
  canonicalization.
- `code_low_weight_structure.py` - enumerates low-weight codeword supports
  under an explicit cap, compares support hypergraph/matroid signatures, imports
  known automorphism/canonicalization controls, and runs exact colored
  incidence-graph isomorphism for small matching rows so code-coset rows killed
  by classical low-weight structure are rejected early.
- `qc_information_set_resolver.py` - runs exact ordered information-set
  canonicalization on quasi-cyclic proof-debt rows so restricted automorphism
  non-equivalence cannot masquerade as full code non-equivalence.
- `cyclic_code_search.py` - enumerates binary cyclic codes from divisors of
  `x^n - 1`, searches tuple-profile collisions, and rejects reciprocal or
  dihedral/multiplier controls before any row can influence code-coset
  experiments.
- `bch_code_search.py` - generates primitive BCH codes from cyclotomic cosets,
  checks defining-set decimation controls before exact baselines, and attacks
  high-rate BCH rows through low-dimensional dual/parity-check generators
  before leaving any row as canonicalization proof debt.
- `goppa_code_search.py` - builds binary Goppa/alternant-style codes from
  finite-field parity checks, searches tuple-profile collisions, and rejects
  rows explained by affine semilinear field automorphisms.
- `goppa_scaling_frontier.py` - generates natural punctured Goppa/alternant
  rows at scalable lengths and gates every surviving invariant collision behind
  exact classical signatures, support-orbit checks, and explicit cap debt.
- `tanner_code_search.py` - generates regular bipartite Tanner graphs, converts
  parity-check matrices into binary codes, and rejects graph-structured rows
  explained by Tanner graph isomorphism or exact code canonicalization.
- `reed_muller_code_search.py` - generates punctured RM(r,m) evaluation-code
  rows, rejects affine-equivalent support controls, and attacks collisions with
  structural, tuple-profile, low-weight, and canonicalization baselines.
- `rank_metric_code_search.py` - generates binary-expanded small Gabidulin/
  rank-metric rows, rejects symbol-block coordinate permutation controls, and
  attacks collisions with structural, tuple-profile, low-weight, and
  canonicalization baselines.
- `code_incidence_resolver.py` - reduces complete finite binary-code
  equivalence to colored bipartite graph isomorphism, verifies recovered
  coordinate permutations on full codeword sets, and preserves `2^k` caps or
  timeouts as proof debt.
- `self_dual_code_boundary_search.py` - generates certified `[I|A]` self-dual
  codes from orthogonal transvections and separates scalable invariant
  collisions from exact finite controls and unresolved canonicalization debt.
- `self_dual_local_profile_obstruction.py` - proves and audits the bounded
  puncture/shorten rank-hull no-go below self-dual code minimum distance.
- `self_dual_global_orbit_audit.py` - audits exponential information-set
  canonization, exact normalized-key witnesses, and the forward-only
  Construction-A lattice route without turning architecture failures into
  lower bounds.
- `self_dual_hsp_applicability.py` - formalizes the code-equivalence hidden
  shift/HSP and checks whether published single-coset no-go hypotheses actually
  apply before routing the family into representation-theoretic experiments.
- `self_dual_rowspace_hsp_reduction.py` - removes the public-generator
  `GL_k` row-scrambler gauge, certifies the exact `S_n` rowspace hidden shift,
  and exposes automorphism-group certification as the remaining no-go debt.
- `self_dual_automorphism_workbench.py` - exactly enumerates fixed-weight
  self-dual supports, certifies rigidity from automorphism-invariant singleton
  colors, verifies explicit nontrivial automorphisms on the full rowspace, and
  preserves sparse-support rows as unresolved debt.
- `self_dual_high_order_automorphism_resolver.py` - preserves the weight-eight
  failure, then uses packed exact weight-ten support enumeration to resolve the
  current length-64 automorphism debt and expose the collective-measurement
  barrier.
- `self_dual_fixed_order_sparsity_obstruction.py` - derives the exact uniform
  self-dual low-weight expectation, calibrates the finite artifacts, and proves
  that explicit fixed-order support rigidity cannot scale.
- `self_dual_wreath_spectrum.py` - models the rigid code-equivalence HSP in
  its actual wreath product, derives the exact one-copy irrep/frame spectrum,
  and isolates the growing-copy covariant-decoder obligation.
- `self_dual_wreath_hecke_audit.py` - proves the centralizer homogeneous
  space is scalar-multiplicity-free, rejects its substitution for the actual
  non-Gelfand hidden subgroup, and shows the natural scalar overlap kernel has
  no hidden-permutation cycle geometry.
- `self_dual_wreath_pgm_polar_audit.py` - derives the exact mixed-state PGM
  polar isometry and average-frame LCU, computes its threshold spectral
  moments, and charges the factorial generic inversion/search baseline while
  isolating the structured-preconditioner target.
- `self_dual_wreath_subset_carrier_algebra.py` - computes exact sparse
  overlapping and symmetrized subset-operator commutators, certifies
  noncommutative word-algebra growth, and rejects scalar subset-weight
  preconditioning.
- `self_dual_wreath_carrier_orbit_growth.py` - reduces carrier words to
  simultaneous-conjugacy tuples, proves factorial orbit growth from depth
  three, and cuts explicit orbit tables in favor of compressed harmonic
  blocks.
- `self_dual_wreath_character_moments.py` - derives the exact mixed physical
  frame trace-character expansion, validates every `W_3` threshold tuple
  through fourth order, proves the all-`n` second-moment class sum, and records
  the unresolved factorial third-moment contraction barrier.
- `self_dual_wreath_third_moment_contraction.py` - removes the factorial
  permutation-pair sum for repeated trivial-standard unequal irreps using a
  weighted-rook and cycle-index recurrence, while keeping all-sector and
  support-gap obligations explicit.
- `self_dual_wreath_all_unequal_third_moment.py` - contracts arbitrary mixed
  unequal-only tuples through exact class connection coefficients and records
  the `S_4` obstruction showing why equal-pair commutator terms need richer
  recoupling data.
- `self_dual_wreath_natural_unequal_dominance.py` - proves that physical
  labels are pairs of iid Plancherel draws and that information-threshold
  natural tuples are all unequal with probability `1-o(1)`, retargeting the
  moment frontier away from equal-sector recoupling.
- `self_dual_wreath_natural_moment_word_map.py` - uses exact character column
  orthogonality to reduce all-order natural normalized frame moments to
  identity and bridge-class subset word counts, while keeping the growing-
  order contraction and concentration gaps explicit.
- `self_dual_wreath_word_map_mixing.py` - proves uniform lazy bridge-walk
  mixing of the one-word statistic to `2/(n!)^2` and quantifies why the
  shared-generator `k`th moment still needs a coupled-walk or concentration
  theorem.
- `self_dual_wreath_coupled_word_walk_gap.py` - identifies the shared-sequence
  `k`th moment with a coupled bridge walk, proves its `k`-independent `1/4`
  spectral gap, and shows that rare equal sectors still prevent a typical
  all-unequal moment conclusion.
- `self_dual_wreath_all_unequal_conditioned_kernel.py` - subtracts diagonal
  Plancherel pairs to derive the exact signed all-unequal character kernel,
  validates its all-order word expansion, and isolates the missing
  simultaneous `k`-coordinate contraction.
- `self_dual_wreath_global_partition_collision.py` - proves that all `2k`
  source Plancherel partitions are globally distinct with probability
  `1-o(1)`, excludes known repeated-source half-norm blocks, and retargets the
  contraction problem to collision-free tuples.
- `self_dual_wreath_collision_free_frame_probe.py` - constructs mixed
  collision-free frame operators matrix-free, finds finite norms within a
  small constant factor of `2^{1-k}`, and keeps the all-`n` polynomial-factor
  theorem explicitly open.
- `self_dual_wreath_character_ratio_contract.py` - reduces unequal frame
  moments to ordinary symmetric-group character ratios, links sharp primary
  bounds, and formalizes the critical short-subset-word anti-concentration
  obligation.
- `self_dual_wreath_short_word_profile.py` - proves exact uniform fixed-mask
  bridge-word marginals, computes unsigned-Stirling short-length tails, and
  removes mask diagonals while retaining non-diagonal shared-generator
  correlations as the active blocker.
- `self_dual_wreath_mask_hypergraph_reduction.py` - proves private-column
  joint character vanishing, reduces all surviving terms to incidence
  two-cores, and records exact nonzero collision-free triangle residuals.
- `self_dual_wreath_equal_commutator_audit.py` - proves the pure commutator
  Frobenius contraction, constructs finite four-class mixed kernels, and
  records their unresolved factorial construction cost.
- `self_dual_wreath_stable_commutator_rank.py` - measures bounded-tail
  physical feature-algebra rank and proves those stable sectors have vanishing
  Plancherel and natural physical-label mass.
- `self_dual_wreath_typical_partition_portfolio.py` - computes exact
  constant-mass Plancherel catalogs and finite typical feature ranks, then uses
  the maximal-atom theorem to rule out polynomial precertified catalogs.
- `self_dual_wreath_typical_recoupling_transfer.py` - maps known
  symmetric-group primitives onto the physical four-class decoder contract and
  rejects scope-mismatched transfers.
- `code_schur_filtration.py` - applies componentwise-product dimensions and
  local shortening/puncturing filtrations as polynomial-time algebraic-code
  invariants; matches remain proof debt rather than quantum evidence.
- `code_closure_attack.py` - implements conductors and t-closures over prime
  fields, audits all binary code pairs locally, and verifies support recovery
  on a proper Reed-Solomon subcode.
- `affine_geometry_code_search.py` - generates punctured AG(2,q)
  line-incidence code rows over prime fields, searches affine support-profile
  collisions, rejects AGL(2,q) support controls, and attacks collisions with
  structural, tuple-profile, low-weight, and canonicalization baselines.
- `projective_geometry_code_search.py` - generates punctured PG(2,q)
  line-incidence code rows, searches support line-intersection profile
  collisions, rejects projective-linear support controls, and attacks
  collisions with structural, tuple-profile, low-weight, and canonicalization
  baselines.
- `dequantization_checks.py` - turns classical baseline failures, attack
  legality, query-model gaps, and triggered falsifiers into blocking registry
  findings.
- `problem_ontology.py` - stores problems, reductions, and no-go barriers.
- `proof_gate.py` - executable hard-rejection gate for candidate algorithms that
  lack proof obligations.
- `research_registry.py` - candidate, experiment, rejected-candidate, and
  negative-result registry.
- `qsearch.py` - CLI for audit, literature, hypothesis, proposal, validation,
  and listing workflows.
- `experiment_runner.py` - dispatches registry experiment IDs to executable
  workbench backends, selects the next run, appends run history, and builds
  trend reports; dynamic `EXP-MUT-*` experiments from promoted mutation
  candidates run the appropriate learnability, baseline, query-model,
  hidden-shift, coset, or code-equivalence backend.
- `proof_tracker.py` - converts proof obligations into candidate-level status
  records and ranked proof-debt reports with lemmas, reductions, and
  counterexample searches.
- `reduction_gate.py` - validates reduction direction, input models,
  parameter/query overhead, oracle and promise preservation, uniformity,
  preprocessing/advice, full-family coverage, and proof provenance; ontology
  adjacency never passes as a reduction.
- `reduction_theorem_catalog.py` - records the exact composable contracts of
  primary-source reductions instead of treating a citation label as a theorem.
- `reduction_contract_audit.py` - attempts to compose each theorem contract
  with the candidate interface and emits concrete mismatch witnesses.
- `proof_work_queue.py` - clusters proof debt into prioritized work items,
  recommended commands, dependencies, success criteria, and kill criteria.
- `scaling_runner.py` - runs parameter sweeps over executable workbenches and
  records scaling histories in the registry.
- `conjecture_tracker.py` - builds candidate conjectures with assumptions,
  reduction links, evidence, blockers, and next proof actions.
- `mutation_engine.py` - proposes next candidate directions from blockers,
  proof debts, dequantization findings, and negative results; proof-gates and
  promotes strong mutated candidates while avoiding recursive mutation loops,
  including learnability-resistant hidden-shift mutations when low-complexity
  reconstruction is the dominant blocker, and materializes candidate-specific
  `EXP-MUT-*` experiment records. Exact reduction-interface failures also
  generate proposal-only coset-sample-native and full-family-lift repairs;
  these are deliberately not promoted until the candidate schema can express
  and verify the linked theorem contract.
- `blocker_taxonomy.py` - clusters dequantization findings, proof debts, and
  negative results into ranked blocker classes so the next pass attacks the
  dominant failure mode.
- `research_frontier_map.py` - converts blockers and workbench artifacts into
  ranked frontier decisions and explicit next experiments/kill criteria.
- `query_model_ledger.py` - makes access-model gaps explicit by mapping each
  candidate to comparable classical models, excluded attacks, and lower-bound
  proof obligations.
- `coset_pgm_capacity.py` - computes PGM-style copy thresholds and explicit
  measurement/decoder obligations for symmetric-group involution coset states,
  blocking information-theoretic distinguishability from being promoted as an
  efficient algorithm.
- `coset_jucys_murphy_label_transform.py` - verifies exact finite diagonal YJM
  spectra and records a uniform polynomial tableau-label circuit contract,
  while proving by multiplicity degeneracy that this is not a full internal
  Kronecker transform or decoder.
- `coset_multiplicity_commutant_search.py` - searches polynomial-description
  bounded-support commutant Hamiltonians inside YJM-degenerate multiplicity
  registers, charging LCU normalization and keeping the asymptotic gap theorem
  as a blocking proof obligation.
- `paper_ingestion.py` - extracts mechanisms, reductions, no-go barriers, proof
  techniques, theorem-like statements, citation keys, open questions, no-go
  index entries, and reusable abstractions from local paper files or optional
  arXiv source archives, with PDFs used only as fallback.
- `structural_tests.py` - Fourier, periodicity, hidden-shift, coset-fingerprint,
  Gowers/higher-order Fourier, and quantum-walk spectral tests.
- `tests/test_structural_tests.py` - regression tests for structural metrics.
- `tests/test_research_artifacts.py` - consistency tests for the research
  artifacts.
- Legacy tiny-circuit files and raw result outputs were removed. Their lessons
  are preserved in `research/registry/negative_results.json`.

## Experiment Roadmap

Highest-upside experiments should run first:

1. **Density-one modular subset-sum partial solver**
   - Positive signal: a uniform polynomial method has inverse-polynomial
     coverage on legal random inputs and a reversible Regev-compatible
     interface.
   - Kill criterion: tail success collapses, coverage comes from explicit
     candidate enumeration, or compact representations have no witness solver.

2. **Hard code-equivalence/coset family generation**
   - Positive signal: a natural scalable family survives support, Schur,
     closure, tuple, canonicalization, and WL-style classical invariants before
     any collective measurement is designed.
   - Kill criterion: every row is classically split or survives only because a
     baseline was capped.

3. **Approximate-period collision landscape for lattice maps**
   - Positive signal: period-preserving collision ridges survive polynomial
     precision.
   - Kill criterion: false periods dominate or exponential precision is needed.

4. **Graph-isomorphism no-go boundary mapping**
   - Positive signal: an observable separates instances that strong Fourier
     sampling cannot.
   - Kill criterion: gains reduce to classical refinement invariants.

5. **Quantum-walk spectral sweep on algebraic state spaces**
   - Positive signal: gap and marked-overlap geometry beats Grover-style scaling.
   - Kill criterion: the walk gives only quadratic or worse behavior.

6. **Higher-order Fourier derivative lift**
   - Positive signal: nonlinear hidden structure becomes sparse after
     polynomially many controlled derivatives.
   - Kill criterion: sparsity requires exponentially many derivative settings or
     collapses to classical low-degree learning.

7. **Block-encoded invariant separation**
   - Positive signal: quantum-estimable spectral invariants separate hard
     instances.
   - Kill criterion: classical trace or Lanczos estimators recover the same
     invariant at comparable cost.

## Cut List

Do not spend research time on:

- More arbitrary "secret finding" oracle variants.
- More N<=3 or N<=4 circuit searches unless used as a subroutine sanity check.
- Claims of exponential speedup without a scalable algorithm and classical lower
  bound or reduction.
- Dashboard polish before the research engine can reject bad hypotheses.
- State-prep or unitary-synthesis tasks unless they serve one of the high-upside
  programs above.

## Hard Proof Gate

Future candidates should be rejected unless they satisfy the proof obligations
in `research/proof_obligations.json`: explicit asymptotic family, input model,
classical baseline, reduction or lower-bound target, quantum mechanism, state
preparation and encoding costs, measurement and decoding, success proof target,
full complexity accounting, no-go-barrier analysis, dequantization check, and
falsifiers.
