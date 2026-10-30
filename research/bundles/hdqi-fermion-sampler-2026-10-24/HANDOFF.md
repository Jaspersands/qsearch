# Mechanical Handoff And Admission Boundary

Do not edit the migrating Desktop/staging checkout. This external bundle is
self-contained except for the frozen `parent_gap.py` dense audit constructor.
No qsearch CLI, main registry, UI, Git or migration change is authorized here.

## What Exists

- `FERMION_SAMPLER.md`: complete local derivation, native promises, prior art,
  classical complexity, coherent reduction, precision obligation and falsifiers.
- `fermion_sampler.py`: incidence/chord coordinates; explicit flux matrices;
  rational DPP sampling, Pfaffians and interference rejection. No native
  2^m-dimensional state or density matrix is constructed by this module.
- `audit_controls.py`: capped dense native and exact exhaustive controls.
- `test_fermion_sampler.py`: tests for the exact rational backend and numerical
  native correspondence; not independent proof review.
- `replay.py --write`: deterministic receipt, scalable backend runs and hashes.

## Reproduce

From this directory, with `/opt/anaconda3/bin/python`:

```sh
python -m pytest -q -W error test_fermion_sampler.py
python -m py_compile fermion_sampler.py audit_controls.py test_fermion_sampler.py replay.py
python replay.py --write
python replay.py --check
```

The Python name above means the stated interpreter, not an unspecified system
installation. The receipt deliberately contains no wall-clock benchmark claim.

## Do Not Overclaim

All native matrix functions are currently FLOATING POINT. Exact rational
sampling from their skew-preserving approximation is not certified sampling
from the true pilot. Do not change `native_error_certified` without a real
interval/arbitrary-precision source certificate and the propagation bound.
The conditional bound function does not create that certificate itself.

Do not discard flux sectors, average them incoherently, use a symmetric-only
DPP routine, divide by a zero-probability event, hide exponential cycle work,
or rename known free-fermion/DPP methods as a new quantum algorithm.
Do not translate the classical word sampler into an arbitrary coherent
decoder simulator. Gaussian coherent preparation is a mathematical reduction,
not an implemented quantum circuit in this bundle.

## Appropriate Later Wiring

Only after the intended repository copy is verified and editable:

1. Add a supplied-root certificate check against the exact native graph and
   generator order; then use a maintained line-graph recognizer if desired.
2. Expose this as a scoped classical baseline with cycle-rank/precision costs.
3. Preserve explicit statuses for surrogate sampling, interval certification,
   quantum compilation, independent review and generic gap, separately.
4. Any result registry must distinguish a root forest from a forest of the
   anticommutation graph. They are not the same condition.

The next THINKING task is not more forest simulations: investigate paid clean
flux-amplitude preparation for extensive cycle rank, and try to dequantize
the same full word distribution. Evaluating sector partition functions or
sampling a classical flux mixture is not a solution to that coherent task.
