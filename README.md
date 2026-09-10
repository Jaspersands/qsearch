# Q-Search: Proof-Gated Quantum Algorithm Research Engine

[![Validate research snapshot](https://github.com/Jaspersands/qsearch/actions/workflows/validate.yml/badge.svg)](https://github.com/Jaspersands/qsearch/actions/workflows/validate.yml)
[![Pages build and deployment](https://github.com/Jaspersands/qsearch/actions/workflows/pages-build-deployment/badge.svg)](https://jaspersands.github.io/qsearch/)
[![Registry Valid](https://img.shields.io/badge/Registry-100%25%20Valid-176c4a)](https://jaspersands.github.io/qsearch/)
[![Negative Results](https://img.shields.io/badge/Negative%20Results-807%20Retained-a43d2b)](https://jaspersands.github.io/qsearch/negative-results.html)

**Q-Search** is an automated, proof-gated research platform designed to investigate structural quantum algorithms for hard classical computational problems.

Rather than optimizing for small-scale demonstrations, toy circuits, or premature speedup claims on trivial instances, Q-Search systematically formulates high-upside quantum mechanisms, subjects them to automated classical attack suites, and permanently preserves negative results.

---

## Quick Navigation

- [Executive Summary](#executive-summary)
- [Live Research Dashboards](#live-research-dashboards)
- [Repository Architecture & Codebase Layout](#repository-architecture--codebase-layout)
- [Primary Research Tracks](#primary-research-tracks)
- [The Proof-Gated Operating System](#the-proof-gated-operating-system)
- [Getting Started & Quick Start](#getting-started--quick-start)
- [Categorized CLI Command Reference](#categorized-cli-command-reference)
- [Operating Contract & Model Allocation](#operating-contract--model-allocation)

---

## Executive Summary

The central question driving Q-Search is: **Can genuine polynomial or super-polynomial quantum speedups be established for non-abelian hidden subgroup problems, linear code equivalence, or dihedral coset instances without falling to classical dequantization?**

### Current Research Decision

The latest audit rules out one specific target: a single bounded-norm,
inverse-polynomial-gap operator cannot completely label typical hidden-involution
multiplicity blocks. The same packing bound applies to any fixed number of
commuting operators. This is not an HSP or general circuit lower bound.
The next useful target is an adaptive coarse-label hierarchy or direct
source-aware transform, not another fitted global separator.
See [the derivation, assumptions, and attempted refutations](research/SPECTRAL_LABEL_BUDGET.md).
The follow-up [signed-tensor access audit](research/SIGNED_TENSOR_ACCESS.md)
also shows why the faithful diagram regime misses typical required K-types.
It leaves physical quotient representations and implicit copy registers open.
The [encoded restriction workbench](research/ENCODED_RESTRICTION.md) now checks
normalized two-QFT carrier extraction, noncommuting logical orbit averages,
and physical coset-register conventions. Its reference-orbit audit bounds
fixed-reference invariant **identification**, not binary class detection.
The [reference-discard audit](research/REFERENCE_TWIRL_INFORMATION.md) separately
bounds binary information after independent carrier/type discard. A joint
measurement on the remaining copy codes cannot recover the erased signal;
classical adaptive references still obey a weaker bound when fresh inputs
are twirled before memory interaction. A constructive coherent-reference
countercheck recovers the original input after carrier erasure by moving
its information first. This escapes that assumption, not the hard decoding
problem. Fully coherent access and one global reference twirl remain open.
The [binary instrument evaluator](research/BINARY_CARRIER_INSTRUMENTS.md)
now measures actual outcome laws and disturbance. Its small-group alternating
carrier gains are reproduced by a latent-irrep model after a joint quantum
label front end; that front end has not been classically replaced. These
are calibration controls, not candidate algorithms.
Its [instrument implementation audit](research/BINARY_CARRIER_INSTRUMENTS.md#clean-label-access-is-not-reference-discard)
now checks clean GPE compute-copy-uncompute. Discarding the Fourier workspace
can preserve label probabilities while destroying the needed quantum state.
The clean label primitive is available conditionally on charged QFT/group-action
access; the growing-copy decision rule remains missing.
Exact fixed-point-free character arithmetic now scores supplied labels through
degree 4096 without tableau enumeration. Typed mutation search distinguishes
binary detection from hidden-element identification and retains one explicitly
incomplete growing-copy binary proposal. Known logarithmic-copy information
bounds are no longer listed as unresolved compiler requirements.
The first growing-copy route tested has a precise limitation: a fixed subset
palette exposes only one effective coset sample per membership-pattern cell.
This rules out amplifying raw copy counts with a fixed small palette. A
[separate source-conditioned bound](research/SOURCE_CONDITIONED_PALETTE.md)
also limits fixed preselected cell profiles when all classical source labels
are kept, by retaining small cells as fully charged quantum inputs.
It explicitly tests persistent conditional modes and missing-irrep measurement
extensions. Classical adaptation among a small predetermined whole-execution
catalogue is also bounded without normalizing selected successes. Succinct
exponential catalogues, coherent selectors and growing palettes remain outside
the useful bound; the derivation is review-pending, not an algorithm or a
novelty claim.
The [classical value-access audit](research/CLASSICAL_VALUE_ACCESS_AUDIT.md)
replaces hidden full-table quadratic reconstruction with counted point queries,
including exact-residue controls on nonmaterializable domains. Sample-limited
exhaustive recovery is now distinguished from polynomial-time dequantization;
value-oracle attacks are not treated as attacks on DHSP phase states.
The same audit retracts the Fourier diagnostic's unsupported learner claims:
spectral concentration is not shift recovery, and superseded negatives are
preserved in a separate quarantine archive.
The [proof-route audit](research/PROOF_ROUTES.md) now checks scoped dependency
contracts and pinned evidence. It catches unsupported assertions without
pretending to check mathematical truth or cover the entire repository.

Source-ranked S_14 scans remain **numerical algebra diagnostics**. Reports now
retain generator matrices and separator coefficients for replay; caches are
bound to the branch, numerical basis, and contraction source. Failed numerical
searches remain inconclusive unless independently certified. No decoder or
new quantum speedup has been established.

### The Core Problem with Standard Circuit Searches
1. **Toy Instance Illusions**: Small circuits ($n \le 3$) often show high simulated success rates that merely rediscover trivial parity relations (Bernstein-Vazirani) without scaling.
2. **Classical Dequantization**: Many heuristic quantum observables can be simulated efficiently by classical Information-Set Decoding (ISD), Weisfeiler-Leman (WL) graph refinements, sparse Fourier sampling, or lattice BDD heuristics.
3. **Erased Dead Ends**: Unrecorded negative experiments lead subsequent research into cyclical, redundant investigations.

#### The Q-Search Solution: Proof-Gated Defense
Q-Search enforces a strict **claim-gating policy**:
- **Executable Research Checks**: Modules contain derivations, finite diagnostics, and assumptions. Passing Python tests is not a machine-checked mathematical proof.
- **Classical Baselines and Access Audits**: Implemented attacks and model checks can falsify proposals; surviving them is not a classical lower bound.
- **Negative Results**: Scoped obstructions and failed hypotheses are retained in `research/registry/negative_results.json`; record counts are not independent discoveries.
- **Speedup Claims Blocked**: The registry actively gates `speedup_claim_allowed = False` until a candidate provably defeats all named classical baselines across asymptotic families.

---

## Interactive Documentation Pages

The repository automatically publishes interactive research telemetry and database dashboards via GitHub Pages:

| Dashboard | Description | Live Page |
| :--- | :--- | :--- |
| **Progress Overview** | Real-time candidate pipeline, falsifier telemetry, and validation status | [index.html](https://jaspersands.github.io/qsearch/) |
| **Methodology** | Formal research principles, no-go mechanisms, and claim-gating philosophy | [methodology.html](https://jaspersands.github.io/qsearch/methodology.html) |
| **Frontier Map** | Machine-readable topological map of active research frontiers and kill criteria | [frontier.html](https://jaspersands.github.io/qsearch/frontier.html) |
| **Negative Results** | Searchable database of 807 retained no-go theorems and dequantization findings | [negative-results.html](https://jaspersands.github.io/qsearch/negative-results.html) |
| **Proof Debt** | Live ledger of 24 open proof obligations, 1,184 lemmas, and reduction edges | [proof-debt.html](https://jaspersands.github.io/qsearch/proof-debt.html) |
| **Repository Map** | Interactive codebase architecture explorer and 792-module taxonomy | [repomap.html](https://jaspersands.github.io/qsearch/repomap.html) |

---

## Repository Architecture & Codebase Layout

### Why is the Root Directory Structured with Flat Modules?
Q-Search contains **792 scientific verification modules**. The codebase organizes modules into domain-specific packages (`core/` and `theorems/`):

```text
quantum-algorithm-search/
├── core/                          # 22 Core Operating System & Proof Engine modules
│   ├── research_registry.py       # Canonical schema for candidates, experiments & results
│   ├── experiment_runner.py       # Experiment execution dispatcher and run history
│   ├── proof_gate.py              # Formal candidate proof obligation and verification engine
│   ├── dequantization_checks.py   # Automated classical attack matrix scanner
│   └── mutation_engine.py         # Automated hypothesis mutation generator
│
├── theorems/                      # 792 Scientific Theorem Verification modules
│   ├── dcp_*.py                   # Dihedral Coset Problem (DHSP) & state-native sieves
│   ├── coset_*.py, cfi_*.py       # Non-abelian coset observables & S_n representation theory
│   ├── self_dual_wreath_*.py      # Self-dual wreath product representations & polar audits
│   ├── code_*.py, goppa_*, bch_*  # Linear code equivalence & automorphism baselines
│   └── character_*, phase_*       # Phase family naturalness & Fourier bridge baselines
│
├── research/                      # Canonical JSON registries & empirical attack artifacts
│   ├── registry/                  # candidates.json, experiments.json, negative_results.json, etc.
│   ├── classical_baselines/       # Dequantization and classical attack outputs
│   ├── progress_snapshot.json     # Curated telemetry feed powering public web dashboards
│   └── frontier_map.json          # Structured research frontier topology
│
├── site/                          # Frontend dashboard assets (styles.css, progress.js)
├── tools/                         # Maintenance utilities (build_progress_snapshot.py, etc.)
├── docs/                          # Human-readable repository maps and specifications
├── tests/                         # Unit tests, integration tests, and runner dispatch suites
│
├── qsearch.py                     # The ONLY Python script at root (unified CLI entry point)
├── README.md                      # Modernized project guide
├── requirements.txt               # Dependencies
└── [6 HTML Dashboards]            # index.html, methodology.html, frontier.html, etc.
```

**Benefits of this Architecture:**
1. **Uncluttered Root**: Only `qsearch.py` and configuration files reside at root.
2. **Zero Packaging Friction**: All 792 workflows execute seamlessly via `python3 qsearch.py <command>`.
3. **Clean Separation of Concerns**: Core platform orchestration (`core/`) is cleanly separated from domain theorem proofs (`theorems/`).

---

## Primary Research Tracks

### 1. Dihedral Hidden Subgroup Problem (DHSP) & Sieve (`DHS-GOWERS-SIEVE`)
- **Objective**: Recover hidden dihedral reflections from independent coset-state samples over $D_N$.
- **Key Mechanisms**: Uniform state-native sum/difference measurements, recursive multi-stage decoders, and bad-register contamination witnesses ($1/\log N$ arbitrary error rate).
- **Core Results & No-Go Theorems**:
  - *Lucas Carry ANF Invariance*: Proved that arbitrary dense invertible affine Boolean preprocessing $\text{GL}(m, 2)$ preserves linear algebraic-normal-form degree for 2-adic carries.
  - *High-Quotient Distribution No-Go*: Proved that low-only carry selection leaves the high quotient distribution generic, preventing shortcut lattice attacks without full joint constraints.

### 2. Non-Abelian Coset States & Code Equivalence (`CODE-COSET-COLLECTIVE`)
- **Objective**: Test linear code equivalence over finite fields using collective coset observables.
- **Key Mechanisms**: Commutant algebras of symmetric group representations, Jucys-Murphy elements, Racah recoupling coefficients, and wreath product Hecke algebras.
- **Core Results & No-Go Theorems**:
  - *PGM Polar Boundary*: Established exact quantum capacity limits on low-register tensor observables.
  - *Master Walsh Flatness No-Go*: Proved that hyperoctahedral adaptive Walsh operators suffer exponential signal cancellation on regular orbits.
  - *Multiplicity Twirl Falsifier*: Sparse signed-sector projection matches an exact hyperoctahedral twirl and shows selected rank-seven multiplicity-three and nontrivial-beta blocks close by moved-point support at most five, refuting strict support-growth extrapolation while leaving uniformity and coherent access open.
  - *Source-Weighted High-Mass Scan*: A matrix-free signed-YJM fiber trace reaches the highest-mass previously untested repeated `S_14` branch (`b=26`, source mass `0.008705`). Support three generates only dimension 7, while a support-four subset has direct common-commutant nullity one with next singular value `0.223`. Audited source coverage rises to `0.008736`, still below one percent; exact all-rank closure, gap scaling, coherent access, and decoding remain open.

### 3. Graph Isomorphisms & Combinatorial Reductions
- **Objective**: Investigate algebraic and combinatorial invariants beyond strong Fourier sampling.
- **Key Mechanisms**: Cai-Fürer-Immerman (CFI) gadget pairs, higher-order Weisfeiler-Leman invariants, and graphlet tensor contractions.

---

## The Proof-Gated Operating System

```mermaid
graph TD
    A[Curated Literature & Ontologies] --> B[Hypothesis Formulation]
    B --> C[Theorem Module Implementation]
    C --> D[Classical Attack Matrix / Dequantization]
    D -->|Classical Collision Found| E[Permanent Negative Result Record]
    D -->|Survives Classical Attack| F[Proof Gate & Lemma Obligations]
    F -->|Proof Debts Open| G[Active Candidate / Frontier]
    F -->|Proof Complete & Asymptotic Separation| H[Speedup Claim Gate Passed]
    E --> I[807 Retained No-Go Theorems]
```

---

## Getting Started & Quick Start

### Prerequisites
- Python 3.11+ (Tested on Python 3.13)
- Node.js (for frontend static checking)

### Installation
```bash
git clone https://github.com/Jaspersands/qsearch.git
cd qsearch
pip install -r requirements.txt
```

### Core Audit & Verification Commands
Run a complete registry audit, check proof obligations, and validate data snapshots:

```bash
# 1. Run full registry and dequantization attack audit
python3 qsearch.py audit

# 2. Run dequantization scanner across all candidates
python3 qsearch.py dequantize

# 3. Validate entire research registry integrity (zero issues expected)
python3 qsearch.py validate

# 4. Rebuild the public dashboard progress snapshot
python3 tools/build_progress_snapshot.py
```

### Running Unit & Dispatch Tests
```bash
# Run candidate-specific unit tests
python3 -m pytest tests/test_dcp_carry_affine_degree_invariance.py

# Run dispatch verification across experiment runners
python3 -m pytest tests/test_experiment_runner.py
```

---

## Categorized CLI Command Reference

All 792 research workflows are accessible via `python3 qsearch.py <subcommand>`.

### Core Operating System Commands
```bash
python3 qsearch.py audit                # Full literature, hypothesis, and registry audit
python3 qsearch.py hypothesize          # Generate proof-gated hypotheses from ontology
python3 qsearch.py dequantize           # Run classical attack matrix and dequantization scan
python3 qsearch.py validate             # Validate registry consistency and claim gates
python3 qsearch.py literature           # Extract mechanisms from seed literature
python3 qsearch.py frontier             # Rebuild and inspect research frontier topology
```

<details>
<summary><strong>Dihedral Coset Problem (DCP) & Phase Sieve Commands (Click to expand)</strong></summary>

```bash
python3 qsearch.py dcp-samples --n-values 8,10,12 --sample-count 4096
python3 qsearch.py dcp-decode --n-values 8,10,12 --samples-per-stage 4096
python3 qsearch.py dcp-recurrence --n-values 8,12,16,20,24 --trials-per-point 12
python3 qsearch.py dcp-schedules --n-values 20,24,28,32 --budget-multiplier 2.0
python3 qsearch.py dcp-uniform-schedules --train-n-values 20,24,28 --unseen-n-values 32,36,40
python3 qsearch.py dcp-bad-registers --n-values 12,16,20,24
python3 qsearch.py dcp-contamination --n-values 8,10,12,14,16 --register-fractions 0.25,0.5,1.0
python3 qsearch.py dcp-witness-search --n-values 12,16,20,24 --maximum-weight 4
python3 qsearch.py dcp-clifford-witnesses --n-values 8,10,12,14,16
python3 qsearch.py dcp-clifford-contamination --n-values 6,8,10,12
python3 qsearch.py dcp-hadamard-scaling --n-values 6,8,10,12 --register-ratios 0.5,1.0,1.5,2.0
python3 qsearch.py dcp-random-decoder --n-values 8,10,12,14,16
python3 qsearch.py dcp-decoder-frontier
python3 qsearch.py dcp-multiscale-aliasing
python3 qsearch.py dcp-carry-high-part
python3 qsearch.py dcp-carry-affine-degree-invariance
python3 qsearch.py dcp-boolean-coset-separation
python3 qsearch.py dcp-marker-list-decoder
python3 qsearch.py dcp-marker-deviations
python3 qsearch.py dcp-marker-all-targets
python3 qsearch.py dcp-marker-vulnerable-coordinates
python3 qsearch.py dcp-marker-chart-union
python3 qsearch.py dcp-marker-target-beam
python3 qsearch.py dcp-pgm-gram-block-encoding
python3 qsearch.py dcp-pgm-qsvt-degree-obstruction
python3 qsearch.py dcp-coherent-fiber-erasure-boundary
python3 qsearch.py dcp-global-erasure-inversion-reduction
python3 qsearch.py dcp-approximate-erasure-coherence-reduction
python3 qsearch.py dcp-erasure-perturbation-reduction
```
</details>

<details>
<summary><strong>Non-Abelian Coset States & Symmetric Group Commands (Click to expand)</strong></summary>

```bash
python3 qsearch.py coset-state
python3 qsearch.py coset-collective-search
python3 qsearch.py coset-pgm-capacity
python3 qsearch.py coset-holevo
python3 qsearch.py coset-stable-fourth-moment
python3 qsearch.py coset-stable-racah-spectrum
python3 qsearch.py coset-hidden-involution-binary-identification-self-reduction
python3 qsearch.py coset-hidden-involution-boundary-gauge-projection-commutation
python3 qsearch.py coset-hidden-involution-centralizer-fourier-transversal
python3 qsearch.py coset-hidden-involution-commutant-basis-closure
python3 qsearch.py coset-hidden-involution-degree-profile-subduction-uniqueness
python3 qsearch.py coset-hidden-involution-gelfand-tsetlin-chain-orthogonality
python3 qsearch.py coset-hidden-involution-hecke-generator-exchange-reduction
python3 qsearch.py coset-hidden-involution-highest-weight-multiplicity-separation
python3 qsearch.py coset-hidden-involution-pair-matching-charge-hierarchy
python3 qsearch.py coset-hidden-involution-racah-tensor-inversion-stability
python3 qsearch.py coset-hidden-involution-multiplicity-twirl-projection
python3 qsearch.py coset-hidden-involution-multiplicity-fiber-trace
python3 qsearch.py coset-hidden-involution-high-mass-support-scan
python3 qsearch.py coset-hidden-involution-source-weighted-support-portfolio
python3 qsearch.py coset-hidden-involution-spectral-label-budget
python3 qsearch.py coset-hidden-involution-signed-tensor-access
python3 qsearch.py coset-hidden-involution-encoded-restriction
python3 qsearch.py coset-hidden-involution-reference-twirl-information
python3 qsearch.py coset-binary-carrier-instruments
python3 qsearch.py proof-routes
python3 qsearch.py run EXP-COSET-HIDDEN-INVOLUTION-SPECTRAL-LABEL-BUDGET
python3 qsearch.py coset-hidden-involution-natural-support-six-mass-audit
python3 qsearch.py cfi-code-reduction
python3 qsearch.py cfi-structural-decoder
```
</details>

<details>
<summary><strong>Self-Dual Wreath Product Representation Commands (Click to expand)</strong></summary>

```bash
python3 qsearch.py self-dual-wreath-spectrum
python3 qsearch.py self-dual-wreath-hecke-audit
python3 qsearch.py self-dual-wreath-pgm-polar-audit
python3 qsearch.py self-dual-wreath-adaptive-walsh-support-concentration-reduction
python3 qsearch.py self-dual-wreath-mrs-identification-escape-theorem
python3 qsearch.py self-dual-wreath-carrier-subspace-invariance
python3 qsearch.py self-dual-wreath-gpe-fusion-tree-cs-boundary
python3 qsearch.py self-dual-wreath-hyperoctahedral-subduction-rigidity
python3 qsearch.py self-dual-wreath-regular-master-walsh-flatness-no-go
python3 qsearch.py self-dual-wreath-orientation-fixed-space-recoupling
python3 qsearch.py self-dual-wreath-racah-decoupling-gauge-uniqueness
python3 qsearch.py self-dual-wreath-source-adaptive-walsh-collision-reduction
python3 qsearch.py self-dual-wreath-trace-biased-adaptive-walsh-no-go
python3 qsearch.py self-dual-wreath-branch-character-cyclic-polar-compiler
python3 qsearch.py self-dual-wreath-branch-character-cyclic-quadrant-overlap
python3 qsearch.py self-dual-wreath-branch-character-equivariant-multiplier-normal-form
python3 qsearch.py self-dual-wreath-branch-character-gpe-dilation-separation
python3 qsearch.py self-dual-wreath-branch-character-label-coherent-power-map-boundary
python3 qsearch.py self-dual-wreath-branch-character-naimark-autocorrelation-fourier-boundary
python3 qsearch.py self-dual-wreath-branch-character-natural-frobenius-word-map
python3 qsearch.py self-dual-wreath-branch-character-polar-naimark-completion
python3 qsearch.py self-dual-wreath-branch-character-power-map-fourier-access-boundary
python3 qsearch.py self-dual-wreath-branch-character-raw-concentration-central-fourier-bridge
python3 qsearch.py self-dual-wreath-branch-character-raw-polar-matched-filter-boundary
python3 qsearch.py self-dual-wreath-branch-character-sector-resolved-whitening-no-go
python3 qsearch.py self-dual-wreath-branch-character-whole-sum-path-erasure-boundary
python3 qsearch.py self-dual-wreath-joint-character-analysis-map-normalization
python3 qsearch.py self-dual-wreath-joint-character-natural-sector-mass
python3 qsearch.py self-dual-wreath-joint-character-purification-access-boundary
python3 qsearch.py self-dual-wreath-orientation-kernel-character-tensor-boundary
python3 qsearch.py self-dual-wreath-orientation-kernel-hash-normalization-no-go
python3 qsearch.py self-dual-wreath-schur-branch-merger-polar-equivalence
python3 qsearch.py self-dual-wreath-schur-dilated-multiplicity-access
python3 qsearch.py self-dual-wreath-split-sector-branch-regularity
python3 qsearch.py self-dual-wreath-trace-biased-coefficient-rank-no-go
python3 qsearch.py self-dual-wreath-schur-companion-transform-scope-boundary
python3 qsearch.py self-dual-wreath-addressed-cross-map-pair-polar-gram-boundary
python3 qsearch.py self-dual-wreath-addressed-cross-map-linear-assembly-normalization-boundary
python3 qsearch.py self-dual-wreath-natural-q-scale-spectral-window-no-go
python3 qsearch.py self-dual-wreath-final-root-metric-access-width-no-go
python3 qsearch.py self-dual-wreath-final-root-scalar-mixer-no-go
python3 qsearch.py self-dual-wreath-final-root-byproduct-covariance-no-go
python3 qsearch.py self-dual-wreath-final-root-physical-preparation-extension-scope-boundary
python3 qsearch.py self-dual-wreath-final-root-program-contraction-normalization-no-go
python3 qsearch.py self-dual-wreath-final-root-purification-naimark-program-boundary
python3 qsearch.py self-dual-wreath-final-root-state-preparation-oracle-query-boundary
python3 qsearch.py self-dual-wreath-final-root-addressed-weyl-assembly-boundary
python3 qsearch.py self-dual-wreath-recursive-polar-normalization-conservation-boundary
python3 qsearch.py self-dual-wreath-affine-gpe-nodelocal-naimark-access-boundary
python3 qsearch.py self-dual-wreath-positive-naimark-access-equivalence-boundary
python3 qsearch.py self-dual-wreath-hierarchical-endpoint-schur-algebra-boundary
python3 qsearch.py self-dual-wreath-affine-flag-aggregate-schur-query-boundary
python3 qsearch.py self-dual-wreath-affine-node-frame-response-boundary
python3 qsearch.py self-dual-wreath-scale-free-endpoint-graph-transfer-boundary
python3 qsearch.py self-dual-wreath-cayley-endpoint-gauge-compiler
python3 qsearch.py self-dual-wreath-affine-star-cayley-compiler
python3 qsearch.py self-dual-wreath-pair-carrier-label-contextuality
python3 qsearch.py self-dual-wreath-occupied-carrier-octahedral-boundary
python3 qsearch.py self-dual-wreath-plancherel-carrier-contextuality
python3 qsearch.py self-dual-wreath-plancherel-carrier-nonidentity-tail
python3 qsearch.py self-dual-wreath-plancherel-carrier-near-derangement-reduction
python3 qsearch.py self-dual-wreath-plancherel-carrier-asymptotic-closure
python3 qsearch.py self-dual-wreath-plancherel-carrier-racah-access-boundary
python3 qsearch.py self-dual-wreath-carrier-noncentral-readout-boundary
python3 qsearch.py self-dual-wreath-carrier-conditioned-pgm-boundary
python3 qsearch.py self-dual-wreath-carrier-holevo-budget-theorem
python3 qsearch.py self-dual-wreath-carrier-branch-pgm-success-certificate
python3 qsearch.py self-dual-wreath-disjoint-pair-branch-pgm-compiler-boundary
python3 qsearch.py self-dual-wreath-disjoint-pair-covariance-polar-reduction
python3 qsearch.py self-dual-wreath-dimensionless-pgm-truncation-bridge
python3 qsearch.py self-dual-wreath-local-block-metric-normalization-no-go
```
</details>

<details>
<summary><strong>Linear Code Equivalence & Classical Attack Commands (Click to expand)</strong></summary>

```bash
python3 qsearch.py code-equivalence
python3 qsearch.py goppa-codes
python3 qsearch.py reed-muller-codes
python3 qsearch.py cyclic-codes
python3 qsearch.py bch-codes
python3 qsearch.py quasi-cyclic-codes
python3 qsearch.py code-structural-invariants
python3 qsearch.py code-tuple-profile-baseline
python3 qsearch.py code-schur-filtration
python3 qsearch.py support-splitting-baseline
python3 qsearch.py information-set-decoding-baseline
```
</details>

---

## Operating Contract & Model Allocation

Q-Search strictly separates cognitive research roles to maximize scientific output and precision:

1. **High-Reasoning Models (Codex)**:
   - Reserved for theorem derivations, mathematical mechanism formulation, representation-theoretic proofs, asymptotic complexity reductions, and decisive experiment design.
2. **Mechanical & Agentic Execution (Gemini / Antigravity)**:
   - Dedicated to CLI subparser generation, registry upserts, unit test creation, snapshot rebuilding, website maintenance, and GitHub Actions CI synchronization.

### Strict Claim Gating Rule
**No finite experiment or empirical success rate ($N \le 12$) is ever promoted to a quantum algorithmic speedup.** Breakthrough claims require a complete, uniform mathematical complexity proof establishing an asymptotic separation against all named classical baselines.
