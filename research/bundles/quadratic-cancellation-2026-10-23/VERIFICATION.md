# Verification

2026-10-23. Work is isolated in this directory while PID 4829's migration
continues. No source/staging edits, Git operations, UI edits or registry writes.

## Executed

- 99 quadratic tests, plus 65 scalar and 32 rank-composer tests: **196 passed**.
- Five `py_compile` checks: implementation, replay, tests and two dependencies.
- `replay.py --output arithmetic_receipt.json`: **66 exact witnesses** across
  eleven primes and ranks 1, 2, 4, 8, 16; eleven forced four-cell scalar cases.
- Largest primes are 127 bits, including both previously supported and newly
  supported congruence regimes. A 64-bit prime has a 32-bit 2-primary component.
- The receipt retains all matrices, witness coefficients, exact counters,
  conditional failure bounds, acquired-bank counts, and five source hashes.
- A second complete replay matches the stored JSON data exactly, including
  all 66 matrices, witnesses and counters. All five source hashes match.

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-quadratic-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider \
  test_quadratic_cancellation.py \
  ../scalar-cancellation-2026-10-23/test_scalar_cancellation.py \
  ../central-rank-2026-10-23/test_central_rank.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-quadratic-pycache \
  /opt/anaconda3/bin/python replay.py --output arithmetic_receipt.json
```

These are deterministic arithmetic controls. Seeded results do not empirically
certify the uniform-randomness assumption in the failure analysis. Full-repo
pytest, `qsearch.py validate`, instrument integration and quantum execution
were NOT run. Dependency imports are local to the nonmoving work area.
