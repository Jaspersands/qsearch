# Repository Map

Q-Search organizes its 792 scientific theorem verification modules within a dedicated `theorems/` package, while keeping core framework engine modules in `core/` and the unified CLI at the repository root.

## Entry Points & Core Framework (`core/`)

- `qsearch.py` - unified command-line interface for every registered workflow (at root). Since 2026-10-19 it is a short shim; `python qsearch.py ...` works as before.
- `qsearch_cli/` - where the commands live: `commands/<domain>.py` holds each subcommand's parser lines and function, `registry.py` lists them in `--help` order. See `tools/split_cli/README.md` for how to add one.
- `core/research_registry.py` - proof-gated candidates, experiments, results, and negative-result persistence.
- `core/experiment_runner.py` - supported experiment dispatch and run history.
- `core/proof_gate.py` - mandatory candidate proof obligations.
- `core/dequantization_checks.py` - automated classical attack matrix scanner.

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
- `tools/corpus/` - searchable index and MCP server over notes, registries, theorem modules and literature ("has this been tried?"); index lives in the git-ignored `research/corpus_index/`.
- `tools/arxiv_watch/` - weekly arXiv collision watch; digest in `research/audits/ARXIV_WATCH.md`; reviewed verdicts in `research/audits/arxiv_verdicts.json`, recorded with `watch.py --verdict` or by the `judge.py` export/import loop for unreviewed flags.
- `tools/audit/` - read-only audits of the registry (failure modes, rediscovery); outputs in `research/audits/`.
- `tools/claim_checker/` - flags the fine print (input loading, readout, oracle-only, baselines) in a quantum-advantage abstract.
- `tools/circuit_search/` - searches local readout circuits (product, adaptive) against certified PPT and collective bounds; DCP packets first.
- `packages/qsearch_classical/` - installable copy of the classical solvers (prime-character OPI, polar Gibbs source, Jacobi sums), generated from `theorems/` by `sync.py` and checked for parity in CI.
- `tools/benchmark/` - "dead ends", a benchmark for AI research agents built from retained negatives plus literature controls; held-out baselines in `research/audits/DEAD_ENDS_BASELINES.md`.
- `tools/split_cli/` - the generator and verifier that split the old 30,000-line `qsearch.py` into `qsearch_cli/`; `migrate.py sweep` moves old-style additions into the package. Manifest in `research/audits/cli_manifest.json`.
- `tools/cockpit/` - builds `site/data/cockpit.json` for `cockpit.html`, a dashboard of what the agents are working on.
- `tools/spend/` - spend ledger, opt-in timing wrapper (`timed.py`) and per-day Codex token totals; report in `research/audits/SPEND_REPORT.md`.
- `formal/` - Lean 4 project formalizing parts of the prime-character exterior bound; built by its own workflow, not by `validate.yml`.
- `docs/` - human-readable project maps and research documentation.
- `docs/papers/classical-competitors/` - draft preprint on three classical or local competitors; every number is generated from a committed report, and `reproduce.sh` regenerates them.
- `docs/outreach/` - unsent drafts to outside researchers and an open-problems post; nothing there has been sent.
- `tests/` - unit, integration, theorem-contract, and registry tests.

## Organization Policy

1. All new scientific theorem verification modules belong under `theorems/`.
2. All framework and OS modules belong under `core/`.
3. New generated research data belongs under `research/`, never at repository root.
4. New website assets belong under `site/`.
5. Maintenance scripts belong under `tools/`.
6. Only `qsearch.py`, its `qsearch_cli/` package, the site's HTML pages, `README.md`, `conftest.py` and configuration files reside at the repository root.
