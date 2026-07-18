# Repository Map

Q-Search currently keeps its Python modules in a flat import namespace. That is
not aesthetically ideal, but moving hundreds of interconnected modules without
a staged package migration would create import churn with no research benefit.
New non-core material is organized by purpose while the package boundary is
introduced gradually.

## Entry Points

- `qsearch.py` - command-line interface for every registered workflow.
- `research_registry.py` - proof-gated candidates, experiments, results, and
  negative-result persistence.
- `experiment_runner.py` - supported experiment dispatch and run history.
- `proof_gate.py` - mandatory candidate proof obligations.

## Research Domains

- `dcp_*.py` - dihedral hidden subgroup, phase-state, subset-sum, and decoder
  workbenches.
- `coset_*.py`, `cfi_*.py` - nonabelian coset states, symmetric-group
  representation theory, and graph-isomorphism reductions.
- `coset_stable_*_certificate.py` - exact falling-cycle and relative-orbit
  certificates for stable Racah characteristic coefficients.
- `code_*.py` plus named code-family modules - code-equivalence generators and
  classical attacks.
- `character_*.py`, `phase_*.py`, `trace_function_search.py` - hidden-shift
  families and dequantization checks.
- `literature_*.py`, `paper_ingestion.py` - literature records and hypothesis
  extraction.

## Persistent Artifacts

- `research/registry/` - canonical structured registries.
- `research/classical_baselines/` - dequantization and attack outputs.
- `research/phase_workbench/` - hidden-shift and DHSP outputs.
- `research/representation/` - symmetric-group and collective-measurement
  outputs.
- `research/code_equivalence/` - code-family and reduction outputs.
- `research/progress_snapshot.json` - small curated website data file.

## Supporting Material

- `site/` - public progress-page styles and behavior.
- `tools/` - maintenance and artifact-generation utilities.
- `docs/` - human-readable project maps and research documentation.
- `tests/` - unit, integration, theorem-contract, and registry tests.

## Organization Policy

1. New generated research data belongs under `research/`, never at repository
   root.
2. New website assets belong under `site/`.
3. Maintenance scripts belong under `tools/`.
4. New scientific modules should use an existing domain prefix until a tested
   package migration replaces the flat namespace.
5. Cached papers, Python bytecode, credentials, logs, and local environments
   remain untracked.
