# Handoff

This is an external mathematical proof-and-control bundle, not a central
registry admission. The original Desktop checkout remains incompletely
available after its migration stopped. No source/staging/Git files were
changed. Do not integrate until there is a verified local checkout.

Dependencies: the sibling `hdqi-parent-gap-2026-10-23` and
`hdqi-filtered-parent-2026-10-24` bundles, NumPy, SciPy, and pytest for
tests. The existing `/opt/anaconda3/bin/python` supplies these packages.

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-relative-flow-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_relative_flow.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-relative-flow-pycache /opt/anaconda3/bin/python -m py_compile relative_flow.py test_relative_flow.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python -B relative_flow.py --output receipt.json
```

All-size deductions are written in RELATIVE_FLOW.md; dense controls do not
prove them. Parameter rows are ledgers, not quantum or large-instance
executions. The remaining gap obligation is equation (7), not the smaller
unweighted inequality. Preserve all false gap/novelty/preparation flags.

No new reviewer, candidate, UI page or general-purpose workbench is needed.
No outreach, commit or push was performed. Before integration, preserve
source hashes and reproduce the focused tests and receipt.
