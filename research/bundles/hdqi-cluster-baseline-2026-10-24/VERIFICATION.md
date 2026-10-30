# Verification

Completed 2026-10-24. All owned processes completed successfully.

## Executed

- **36 new tests plus 141 earlier external regressions: 177 passed**, warnings
  treated as errors; pytest plugin autoload disabled. Exit 0.
- `py_compile cluster_baseline.py test_cluster_baseline.py`: exit 0.
- Two live receipt workflows: exit 0. `cmp` confirms byte-identical
  `receipt.json` and `/tmp/qsearch-cluster-replay-2026-10-24.json`.
- Four SHA-256 values match the receipt and the values below.

Combined command, from the external research-work directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-cluster-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-cluster-baseline-2026-10-24/test_cluster_baseline.py hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
```

## What Was Checked

Exact rational enumeration checks the actual proposal probabilities and
weights against the independent ordered-tuple cluster definition. It covers
signed activities, disconnected hosts, singleton/repeated polymers, a path,
a triangle with multiple spanning trees, weighted Prufer probabilities,
touching multiplicities and failed draws. Deliberately omitting a contact
divisor or conditioning on successful proposals is detected as biased.
All four-vertex graphs satisfy the implemented tree-graph inequality.

Rational word-series activities have explicit analytic remainder bounds.
Independent dense exponentials check their inclusion-exclusion values and
the truncated log partition. A dependent three-Pauli control violates the
even-multiplicity envelope, verifying that redundancy-freeness is substantive.

The doubled-word controls compare arbitrary fields in [-1,1] against
independent dense pilot probabilities and the exact cluster expectation.
They include zero pins, subset parity, total parity and fractional fields.
Total parity has exactly unit unnormalized partition; two positive pins on
one anticommuting edge cancel exactly. Neither check claims a sampler.

The receipt has three 4,000-draw DIAGNOSTIC Monte Carlo runs; all three also
have exact expectation checks. Four field rows have exact expectation
checks and log-reference residuals <=1.1e-12. Four million-vertex parameter
ledgers include growing degree and an out-of-regime rejection; these do NOT
construct large matrices or execute a large-scale classical estimator.

## Hashes

```text
95de565cd743c7ffa1b81ac8d057374f1d952d5b8e5949bc2862f9ee8f8bc7fe  cluster_baseline.py
b4d603ddd81b6c4db5a3fa47e85018826ec412a4799bc41f96b22d1c204b969e  test_cluster_baseline.py
f32572252c925e5ab6e09b74837e659c1a5206893b21ad34408e41f67cfd8d29  CLUSTER_BASELINE.md
efcfb8b316352c76b8c091bf3b5b9cce6c086ba86eb4f6bcfcdca7c73253d352  HANDOFF.md
```

## Scope

The all-size theorem rests on the written argument, not these small tests.
It is a local, unreviewed adaptation of known importance-sampling machinery.
No general production FPRAS, full pilot sampler, thermal gap, quantum state
preparation, independent review, novelty certification or speedup is admitted.

The original checkout and staging remain untouched. The Developer checkout
is absent and migration status is `needs_inspection`. Consequently no full
original-repository suite, central `qsearch.py validate`, Node check, central
registry/CLI/UI edit, commit or push was performed. The six-file new bundle
and the external checkpoint are the complete edit scope. Prior bundles stay
frozen, retaining their earlier hashes; the checkpoint supersedes their
overbroad classical-baseline wording.
