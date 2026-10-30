# Verification

- New isolated suite: 18 passed in 0.60s after correcting the sign of the
  displayed minimal polynomial to j^2-6j-6. The exact field calculation
  caught that error; no failing assertion was weakened or removed.
- Three Python files pass py_compile, with bytecode outside the repository.
- replay_source_field.py completed and wrote source_field_receipt.json:
  three conditional field plans and two actual curve counts of 1444.
- Related suites rerun separately: 27 prime-square flag tests passed in
  59.34s, 37 weak-mark/source tests passed in 0.02s and 22 effective-output
  tests passed in 2.00s.
- The geometric model, quotient/descent and coherent oracle are NOT run.
- Full repository tests, qsearch.py validate and UI syntax checks are NOT
  run on the moving checkout. No commit, push, or migration changes.

Commands, from this directory:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile source_field_controls.py test_source_field_controls.py replay_source_field.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay_source_field.py
```
