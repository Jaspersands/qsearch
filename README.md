# Quantum Algorithm Research Engine

This project is being reshaped around one goal: increase the chance of finding
or clarifying a genuinely major quantum algorithmic idea. It should not optimize
for demos, toy circuits, small benchmark wins, or unsupported speedup claims.

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
python qsearch.py dcp-subset-sum-preconditioned-geometry
python qsearch.py dcp-subset-sum-fourth-moment
python qsearch.py dcp-subset-sum-smith-moments
python qsearch.py dcp-subset-sum-smith-transfer
python qsearch.py dcp-subset-sum-fixed-moments
python qsearch.py dcp-subset-sum-conditioned-tail
python qsearch.py dcp-subset-sum-growing-moments
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

Growing order is partially closed as well. A k-tuple transfer path can enlarge
its Boolean-generated lattice at most `2^k` times. Counting those transition
positions and patterns shows the bad source contribution vanishes whenever
`4^k log n=o(n)`, including every `k <= (1/2-epsilon) log_2 n`. Moment proposals
must now operate at the half-logarithmic boundary or above and charge
`q=2^k` patterns, estimation variance, memory, and decoding.

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
through `S_6`, including multiplicity five. Most sectors remain finite structural
witnesses rather than scalable transforms.

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
```

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
