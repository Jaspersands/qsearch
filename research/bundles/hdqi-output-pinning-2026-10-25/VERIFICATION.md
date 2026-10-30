# Verification

2026-10-25, /opt/anaconda3/bin/python, isolated external bundle.

- `python -m pytest -q -W error test_pinning_control.py`: 21 passed,
  no skips or warnings; final run after the connected-input extension.
- `python -m py_compile pinning_control.py test_pinning_control.py replay.py`:
  passed after the final Python edits.
- Fresh deterministic receipt generation and comparison passed after the
  final mathematical scope clarification. Final receipt SHA256:
  b8facd0fd612540a4756b74f9992bfb8685ecdff5302772c3fa911be4eadfe45.
- Five source hashes and three external context-note hashes are included
  and recomputed by replay. No direct runtime import of the main checkout.

Checked: exact physical matrix identities; every Taylor coefficient of the
three-generator vector through order 16; exact forbidden-word zeros;
normalization coefficients; rigorous rational positive-boundary/influence
certificates at beta=1/16,1/64,1/256; all seven unconditional inclusion
events at each temperature; symbolic Perron polynomial; limiting heat-bath
matrix both by its formula and independently from physical leading powers;
connected L(K_4) integer-power controls; malformed inputs and precision
guards. The general induced-path extension is a written analytic proof,
not an exhaustive graph or temperature experiment.

Not checked or claimed: independent mathematical review, formal proof,
novelty, a production sampler, large native sampling runs, an advantage,
or full-repository integration. Main tests, qsearch.py validate and UI
syntax checks were not run against the migration-sensitive checkout.
No new reviewer was spawned, no commit/push was made, and no owned
subprocess remains running. The broad research goal remains active.
