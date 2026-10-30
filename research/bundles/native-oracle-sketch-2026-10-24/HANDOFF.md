# Bounded Integration Handoff

The reasoning pass is complete only after the local tests and receipt replay
recorded in VERIFICATION.md pass. Do not infer a speedup from them.

## Current Decision

Do not implement an oracle-sketch native decoder or launch occupancy sweeps.
The literal address-local proposal needs Omega(q^n) visited labels for
constant correct-herald Fourier success. A same-record exhaustive classical
correlation baseline has the same leading exponential time factor and
polynomial sample count and space. Read ORACLE_SKETCH_ACCESS.md for scope.
This does not refute the source paper or rule out other native algorithms.

## Mechanical Tasks After Migration Is Verified

1. Confirm the complete local checkout and preserve all other agents' work.
   No edits to the moving Desktop source or staging copy are authorized by
   this note. The intended Developer checkout was absent during this pass.
2. Add this result to the existing negative-result registry using its real
   schema. Link arxiv:2604.07639v2, the original native input, the support
   proof and the receipt. Scope it to THIS sketch/readout, never all DCP or
   LWE algorithms. Do not create an accepted candidate or resolve a general
   receiver/hardness obligation.
3. Integrate the focused controls only if the existing access-accounting
   subsystem can reuse them. No new generic pipeline, API, UI or framework
   is needed. Keep deterministic balanced fixtures distinct from IID runs.
4. If files move, regenerate their local hash receipt and run the project's
   relevant tests/validation. Do not describe this external focused test
   run as a passing repository-wide suite.

## Reproduce Locally

From this directory, using the available Python with numpy, sympy and pytest:

```sh
/opt/anaconda3/bin/python -W error -m pytest -q test_native_sketch.py
/opt/anaconda3/bin/python -m py_compile native_sketch.py test_native_sketch.py replay.py
/opt/anaconda3/bin/python replay.py --output receipt.json
```

`replay.py` writes only the explicitly selected output path. It does not
contact a source oracle, execute quantum gates, mutate any registry, or
consume secret values inside an attack. Secrets appear only in labeled
fixture generation and evaluation controls.
