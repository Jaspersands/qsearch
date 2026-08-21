# Repository Map

Q-Search organizes its 723 scientific theorem verification modules within a dedicated `theorems/` package, while maintaining core workflow entry points at the root.

## Entry Points & Core OS

- `qsearch.py` - unified command-line interface for every registered workflow.
- `research_registry.py` - proof-gated candidates, experiments, results, and negative-result persistence.
- `experiment_runner.py` - supported experiment dispatch and run history.
- `proof_gate.py` - mandatory candidate proof obligations.
- `dequantization_checks.py` - automated classical attack matrix scanner.

## Research Domains (`theorems/`)

- `theorems/dcp_*.py` - dihedral hidden subgroup (DHSP), phase-state, subset-sum, and decoder workbenches.
- `theorems/coset_*.py`, `theorems/cfi_*.py` - nonabelian coset states, symmetric-group representation theory, and graph-isomorphism reductions.
- `theorems/self_dual_wreath_*.py` - hyperoctahedral wreath product representations, Racah recoupling, and PGM polar audits.
- `theorems/code_*.py`, `theorems/goppa_*.py`, `theorems/bch_*.py` - linear code equivalence generators and classical attacks.
- `theorems/character_*.py`, `theorems/phase_*.py`, `theorems/trace_*.py` - hidden-shift families and dequantization checks.

## Persistent Artifacts (`research/`)

- `research/registry/` - canonical structured JSON registries (`candidates.json`, `experiments.json`, `negative_results.json`, `experiment_results.json`, `dequantization_checks.json`).
- `research/classical_baselines/` - dequantization and attack outputs.
- `research/phase_workbench/` - hidden-shift and DHSP outputs.
- `research/representation/` - symmetric-group and collective-measurement outputs.
- `research/code_equivalence/` - code-family and reduction outputs.
- `research/progress_snapshot.json` - small curated website data file.
- `research/frontier_map.json` - active research frontiers topology.

## Supporting Directories

- `site/` - public progress-page styles, assets, and frontend behavior.
- `tools/` - maintenance and artifact-generation utilities (`build_progress_snapshot.py`).
- `docs/` - human-readable project maps and research documentation.
- `tests/` - unit, integration, theorem-contract, and registry tests.

## Organization Policy

1. All new scientific theorem verification modules belong under `theorems/`.
2. New generated research data belongs under `research/`, never at repository root.
3. New website assets belong under `site/`.
4. Maintenance scripts belong under `tools/`.
5. Core operating system entry points (`qsearch.py`, `research_registry.py`, `experiment_runner.py`) remain at the repository root.
