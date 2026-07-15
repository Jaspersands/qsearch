# Quantum Algorithm Research Engine

## Blunt diagnosis

- The old loop is not a credible path to a Shor-level algorithm.
- It searches tiny circuits and arbitrary oracle puzzles, then lets an LLM label complexity from N<=3 data.
- Most successful runs rediscover Bernstein-Vazirani-like parity structure; most exotic names are unsolved or unsupported.
- The dashboard's 'solved novel algorithms' criterion is just success_rate >= 1.0 on tiny instances, not a research result.
- The project needs explicit scalable families, classical baselines, structural quantum handles, and kill criteria.

Repository scan:
- Scanned files, excluding vendor and git: 29
- Historical runs: 0
- Tiny-instance success_rate >= 1.0 runs: 0
- Claimed speedups: `{}`
- Toy-term counts: `{"bernstein-vazirani": 0, "bitwise": 0, "oracle": 0, "secret finding": 0, "state preparation": 0, "unitary synthesis": 0}`

## Revised direction

Make this a research-program generator and structural-test harness for high-upside quantum algorithm mechanisms.

Cut or deprioritize:
- Arbitrary secret-bitstring oracle variants with no natural problem family.
- N<=3 circuit searches used as evidence for asymptotic speedup.
- State-preparation and unitary-synthesis tasks unless they directly support a larger algorithm.
- LLM-only complexity claims without a lower bound, reduction, or scalable mechanism.
- Dashboard labels that call tiny solved instances 'novel algorithms'.

Only admit a lead when it has:
- Explicit scalable family.
- Known or conjectured classical barrier.
- Quantum mechanism tied to Fourier sampling, coset states, phase estimation, walks, block-encodings, or tensor measurements.
- A structural experiment with a positive signal and a kill criterion.
- A path from toy finite instances to asymptotic proof obligations.

## Top research leads

| Rank | Score | Lead | Domains | Main kill criterion |
| ---: | ---: | --- | --- | --- |
| 1 | 72.66 | [Collective coset measurements for code equivalence](#collective-coset-measurements-for-code-equivalence) | nonabelian-hsp, code-equivalence | Max pairwise overlap stays above 0.9 or rank saturates at a constant. |
| 2 | 67.62 | [Structured hidden-shift sieve beyond generic dihedral HSP](#structured-hidden-shift-sieve-beyond-generic-dihedral-hsp) | hidden-shift, lattice-periodicity | Large autocorrelation aliases or a simple classical correlation recovers the shift. |
| 3 | 65.90 | [Approximate period finding for lattice and number-field maps](#approximate-period-finding-for-lattice-and-number-field-maps) | lattice-periodicity | False periods dominate or the ridge requires exponential precision. |
| 4 | 61.22 | [Graph-isomorphism observables beyond strong Fourier sampling](#graph-isomorphism-observables-beyond-strong-fourier-sampling) | nonabelian-hsp, graph-isomorphism | All gains reduce to known classical refinement invariants. |
| 5 | 51.86 | [Higher-order Fourier search for nonlinear hidden structure](#higher-order-fourier-search-for-nonlinear-hidden-structure) | query-separations, hidden-shift | Sparsity appears only after using exponentially many derivative settings. |
| 6 | 35.98 | [Block-encoded spectral invariants for isomorphism-like problems](#block-encoded-spectral-invariants-for-isomorphism-like-problems) | hamiltonian-tensor, graph-isomorphism, code-equivalence | Classical randomized estimators recover the invariant within the same asymptotic cost. |
| 7 | 35.26 | [Quantum walks over algebraic solution complexes](#quantum-walks-over-algebraic-solution-complexes) | quantum-walks, code-equivalence, lattice-periodicity | Gap-overlap product predicts only quadratic or worse behavior. |

## Experiment roadmap

1. **Coset-state relation rank sweep** (`E1-CODE-COSET-RANK`)
   - Lead: Collective coset measurements for code equivalence
   - Protocol: Generate code families with known permutation automorphisms. For each hidden permutation, compute equality-relation fingerprints and rank, then scale length and field size.
   - Positive signal: Rank and pairwise distinguishability grow with instance count using low-degree invariants.
   - Kill criterion: Max pairwise overlap stays above 0.9 or rank saturates at a constant.
2. **Hidden-shift Fourier flatness and alias test** (`E3-HSHIFT-SPECTRUM`)
   - Lead: Structured hidden-shift sieve beyond generic dihedral HSP
   - Protocol: For each algebraic base function, measure Fourier flatness, autocorrelation aliases, and shift distinguishability over growing domains.
   - Positive signal: Flat spectra with low autocorrelation aliases and no obvious classical correlation handle.
   - Kill criterion: Large autocorrelation aliases or a simple classical correlation recovers the shift.
3. **Approximate-period collision landscape** (`E5-APPROX-PERIOD-COLLISIONS`)
   - Lead: Approximate period finding for lattice and number-field maps
   - Protocol: Construct maps with known planted periods and noise. Measure whether period-preserving collisions dominate all other collisions as dimension grows.
   - Positive signal: A stable period ridge remains visible under polynomial precision.
   - Kill criterion: False periods dominate or the ridge requires exponential precision.
4. **Map the no-go boundary** (`E7-GI-NOGO-BOUNDARY`)
   - Lead: Graph-isomorphism observables beyond strong Fourier sampling
   - Protocol: Reproduce failures of strong Fourier sampling on small GI-HSP instances, then mutate observables and record exactly which barrier is bypassed, if any.
   - Positive signal: A candidate observable separates instances that strong Fourier labels cannot.
   - Kill criterion: All gains reduce to known classical refinement invariants.
5. **Derivative Fourier lift test** (`E9-DERIVATIVE-FOURIER-LIFT`)
   - Lead: Higher-order Fourier search for nonlinear hidden structure
   - Protocol: For each nonlinear family, compute whether controlled finite differences produce sparse Fourier spectra over polynomially many derivative orders.
   - Positive signal: Higher-order spectra become sparse while the original family remains classically hard.
   - Kill criterion: Sparsity appears only after using exponentially many derivative settings.
6. **Spectral gap and marked-overlap sweep** (`E8-WALK-SPECTRAL-SWEEP`)
   - Lead: Quantum walks over algebraic solution complexes
   - Protocol: Build local-move graphs for each algebraic family. Track normalized spectral gap, marked overlap, and classical conductance proxies.
   - Positive signal: Quantum hitting-time proxy improves asymptotically over classical and Grover baselines.
   - Kill criterion: Gap-overlap product predicts only quadratic or worse behavior.
7. **Tensor ansatz for collective measurements** (`E2-COLLECTIVE-MEASUREMENT-ANSATZ`)
   - Lead: Collective coset measurements for code equivalence
   - Protocol: Represent k-register measurement candidates as tensor networks over irrep labels. Optimize distinguishability on generated code instances.
   - Positive signal: Bond dimension grows polynomially while success probability beats individual-register tests.
   - Kill criterion: Required bond dimension or sample count grows exponentially on the first three scales.
8. **Phase-combination sieve simulation** (`E4-PHASE-SIEVE`)
   - Lead: Structured hidden-shift sieve beyond generic dihedral HSP
   - Protocol: Simulate phase-state frequency samples and search for merge rules that increase useful phase precision faster than generic Kuperberg-style sieves.
   - Positive signal: Sample count and merge depth fit a polynomial or clearly improved subexponential law.
   - Kill criterion: Scaling matches generic subset-sum sieving with no family-specific gain.
9. **Reversible arithmetic cost audit** (`E6-REVERSIBLE-MAP-COST`)
   - Lead: Approximate period finding for lattice and number-field maps
   - Protocol: Estimate reversible circuit and precision costs for candidate maps before claiming any quantum advantage.
   - Positive signal: Map evaluation cost is polynomial with realistic precision overhead.
   - Kill criterion: State preparation or arithmetic cost dominates the proposed speedup.
10. **Invariant separation and access-model audit** (`E10-INVARIANT-SEPARATION`)
   - Lead: Block-encoded spectral invariants for isomorphism-like problems
   - Protocol: Search for operator families whose spectra separate hard paired instances. For every hit, compare against classical trace/Lanczos estimators.
   - Positive signal: A separating invariant is quantum-estimable in polylog or polynomially lower cost.
   - Kill criterion: Classical randomized estimators recover the invariant within the same asymptotic cost.

## Lead details

### Collective coset measurements for code equivalence

- Candidate id: `NAHSP-COLLECTIVE-CODE-EQUIV`
- Score: `72.66`
- Hypothesis: Code equivalence instances with structured automorphism groups may expose low-rank collective coset-state observables missed by strong Fourier sampling.
- Problem family: Families of linear codes with controlled automorphism strata, moving from small finite fields to asymptotic length n.
- Quantum mechanism: Prepare multiple coset states for hidden permutation subgroups, search over entangled measurements using representation labels and tensor-network ansatzes.
- Classical barrier: Code equivalence has hard average-case regimes and is a canonical hidden permutation problem.
- Why this is not toy: The family is explicit, scales with code length, and has a real classical algorithmic baseline rather than an arbitrary oracle.
- First failure modes:
  - Coset fingerprints collapse to near-identical relation data.
  - Useful measurements require exponential tensor bond dimension.
  - The structured automorphism promise excludes hard instances.
- Evaluation flags: `known no-go barriers must be confronted explicitly`

### Structured hidden-shift sieve beyond generic dihedral HSP

- Candidate id: `DHS-SIEVE-STRUCTURED-SHIFTS`
- Score: `67.62`
- Hypothesis: Some explicit hidden-shift families have phase-state distributions that avoid generic subset-sum hardness and admit polynomial-time sieving.
- Problem family: Cyclic and dihedral hidden shifts where the shifted object comes from bent, multiplicative-character, or low-degree algebraic functions.
- Quantum mechanism: Fourier sampling creates phase states whose frequency support has algebraic structure. A custom sieve combines phases without losing signal.
- Classical barrier: Generic hidden shift and dihedral HSP connect to lattice-relevant hard cases; classical correlation search is exponential without exploitable structure.
- Why this is not toy: The work tests entire algebraic families and asks whether a known barrier has structured exceptions.
- First failure modes:
  - Fourier support is either too sparse and classical, or too random and subset-sum hard.
  - The sieve only works because the family is classically easy.
  - Noise in approximate shifts destroys phase coherence.
- Evaluation flags: `known no-go barriers must be confronted explicitly`

### Approximate period finding for lattice and number-field maps

- Candidate id: `APPROX-PERIOD-LATTICE`
- Score: `65.9`
- Hypothesis: There may be number-field or lattice maps with approximate periods stable enough for phase estimation but hidden enough to resist classical sampling.
- Problem family: Explicit maps from lattice points or ideals to coarse invariants with tunable noise, period rank, and collision profile.
- Quantum mechanism: Use approximate QFT and phase estimation to recover dual-period information from coherent evaluations of noisy periodic maps.
- Classical barrier: Relevant regimes should map to lattice problems with worst-case or average-case evidence.
- Why this is not toy: The objective is a reduction-quality scalable family, not a hand-marked solution state.
- First failure modes:
  - Coherence requirements exceed the precision needed to define the map.
  - Classical lattice reduction exploits the same approximate periods.
  - The candidate map is not efficiently reversible.
- Evaluation flags: `weak structural quantum handle`

### Graph-isomorphism observables beyond strong Fourier sampling

- Candidate id: `GI-COLLECTIVE-OBSERVABLES`
- Score: `61.22`
- Hypothesis: Graph families with controlled refinement structure may admit collective observables that distinguish isomorphism cosets without solving full HSP.
- Problem family: Strongly regular graphs, CFI-like constructions, and refinement-hard families with known automorphism behavior.
- Quantum mechanism: Prepare graph-indexed coset or coherent refinement states and search for collective observables using tensor-network contractions.
- Classical barrier: Meaningful wins must beat modern quasi-polynomial classical GI baselines on well-defined families.
- Why this is not toy: Graph isomorphism is a real structural problem with known quantum no-go zones.
- First failure modes:
  - The observable is equivalent to classical color refinement.
  - The family is already easy for modern classical GI.
  - Collective measurement construction scales exponentially.
- Evaluation flags: `classical baseline not hard enough yet, known no-go barriers must be confronted explicitly`

### Higher-order Fourier search for nonlinear hidden structure

- Candidate id: `HIGHER-ORDER-FOURIER-HIDDEN-STRUCTURE`
- Score: `51.86`
- Hypothesis: Nonlinear hidden structure may become tractable when expressed through higher-order Fourier or Gowers-uniformity observables rather than plain BV-style parity.
- Problem family: Explicit low-degree phase polynomials, bent-function shifts, and locally testable hidden constraints over finite fields.
- Quantum mechanism: Use phase queries and controlled derivatives to turn high-order structure into linear Fourier information over an expanded domain.
- Classical barrier: Choose distributions with known classical query lower bounds or reductions to hard property-testing tasks.
- Why this is not toy: Candidates must supply a scalable distribution and lower-bound target before any circuit search starts.
- First failure modes:
  - Derivative queries collapse the problem to classical low-degree learning.
  - The promise is artificial and has no explicit computational analogue.
  - The quantum routine is just BV on a relabeled oracle.
- Evaluation flags: `weak structural quantum handle, known no-go barriers must be confronted explicitly`

### Block-encoded spectral invariants for isomorphism-like problems

- Candidate id: `BLOCK-ENCODED-INVARIANTS`
- Score: `35.98`
- Hypothesis: Quantum singular value transformation may expose algebraic invariants of graphs or codes that are expensive to estimate classically.
- Problem family: Sparse matrices derived from graph lifts, code Tanner graphs, association schemes, and coherent constraint systems.
- Quantum mechanism: Block-encode structured operators and use polynomial transformations or phase estimation to estimate invariants that separate hard instances.
- Classical barrier: Candidate invariants must not be cheaply approximable by classical randomized linear algebra on the same sparse access model.
- Why this is not toy: The input model and block-encoding cost are part of the score, preventing hidden data-loading wins.
- First failure modes:
  - The invariant is classically estimable by Lanczos or trace estimation.
  - Block-encoding construction costs more than the classical baseline.
  - The invariant fails to separate hard instances.
- Evaluation flags: `weak structural quantum handle, classical baseline not hard enough yet, known no-go barriers must be confronted explicitly`

### Quantum walks over algebraic solution complexes

- Candidate id: `WALK-ALGEBRAIC-STATE-SPACES`
- Score: `35.26`
- Hypothesis: Some hard algebraic search problems have state-space graphs where the quantum walk spectral gap and marked overlap beat Grover-like behavior.
- Problem family: Cayley and local-move graphs over code bases, lattice bases, isomorphism certificates, or partial algebraic assignments.
- Quantum mechanism: Use coined or Szegedy walks to amplify structured marked subspaces whose geometry is invisible to unstructured search.
- Classical barrier: Classical local search and MCMC mixing can be slow on these spaces; the target is a provable hitting-time separation.
- Why this is not toy: The experiment studies graph families, spectral gaps, and marked geometry over scaling instances.
- First failure modes:
  - The walk only recovers a quadratic Grover speedup.
  - The marked overlap vanishes faster than the gap helps.
  - Classical random walks mix just as well after better coordinates are chosen.
- Evaluation flags: `weak structural quantum handle, classical baseline not hard enough yet, known no-go barriers must be confronted explicitly`

## Structural-test harness

The current executable tests are smoke checks for the metrics, not proof of advantage.
Use them to reject bad leads early and to decide which finite families deserve deeper math.

Available checks:
- Walsh-Fourier concentration for Boolean phase oracles.
- Gowers uniformity and derivative Fourier sparsity for higher-order structure.
- Periodicity collision landscapes for exact or approximate periods.
- Hidden-shift spectral flatness and autocorrelation aliasing.
- Coset equality-relation rank and pairwise distinguishability.
- Quantum-walk spectral gap and marked-overlap proxies.

Run:

```bash
python discover_algorithms.py --output-dir research
python -m unittest discover -s tests
```
