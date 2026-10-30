# Verification And Execution Scope

2026-10-23. Isolated local bundle; the moving repository and staging directory
were not edited. No commits, CLI/registry writes, UI changes or iCloud repairs.

## Completed Controls

- **35 tests passed**, including:
  - all 260 nonzero singular probes in the split six-dimensional F3 space;
  - all probe fibers (81 parameter values each) against an opaque oracle;
  - geometric reconstruction on all 80 hidden maximal singular spaces when
    the stated three-functional independence condition holds;
  - all 6,400 candidate/hidden-space pairs for the exact certificate;
  - an explicit Levi-only false certificate and the rank-two chart exception;
  - opaque-label, dense coset/QFT reference recovery at ranks 3 and 4;
  - a 127-bit-prime rank-eight SUPPLIED-KERNEL geometry control, not a learner;
  - full query/error-budget arithmetic and invalid-field rejection.
  - exact common-chart polynomial linearizations at ranks 2, 3 and 4 over
    three primes: a four-dimensional linear kernel at rank two, but only the
    scalar line at ranks three and four, with the quadratic B block forced zero.
- Combined with the preceding quadratic, scalar and rank-composer suites:
  **231 tests passed in 3.38 seconds**. This is a selected local milestone,
  NOT full-repository validation.
- Three Python files pass `py_compile`.
- A second complete replay matches the stored JSON data, including sampled
  frequencies, kernels, certificates and query counts. All four source hashes
  match the current files.
- Four live dense reference executions recover and certify their fixtures:

| Witt Rank | Field | Attempts | Actual Classical Oracle Calls |
|---:|---:|---:|---:|
| 3 | F3 | 1 | 251 |
| 3, other fixture | F3 | 1 | 251 |
| 4 | F3 | 1 | 2,201 |
| 5 | F3 | 1 | 19,705 |

These include each dense p^(2n-2) table and the final certificate. They are
NOT measured quantum query counts. The receipt separately reports proposed
scalable budgets, with fields preventing their substitution for these costs.
No physical QPU execution or native scalable gate compilation occurred.

The proof applies to effective odd-characteristic finite fields; executed
controls use prime fields only. The reference simulations use numerical FFTs
with normalization/support checks, whereas the geometry and field identities
are exact integer modular arithmetic.

## Reproduction

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-orthogonal-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-orthogonal-pycache \
  /opt/anaconda3/bin/python replay.py
```

`orthogonal_probe_receipt.json` contains the recovered bases, every probe,
Fourier sample and table ledger, and four source hashes. It is a control
receipt, not independent proof review, a novelty determination, or evidence
for a natural classical hardness assumption. Full-repository pytest and
`qsearch.py validate` remain deferred until migration permits integration.
