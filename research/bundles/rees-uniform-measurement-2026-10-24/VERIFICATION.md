# Verification

2026-10-24. All checks below completed; no owned test or audit process was
left running. Main checkout integration and Git were deliberately untouched.

## New Pass

-33 new tests passed in13.99s with warnings treated as errors and no skips.
- The expanded external selection passed1027 tests in46.56s, warnings as
  errors and no skips. This is the exact994-test selection documented by
  `../rees-formal-core-2026-10-24/NATIVE_SOURCE_VERIFICATION.md`, plus this
  directory's `test_measurement.py`.
- `py_compile` passed for all three new Python files.
- Live audit completed and `measurement_receipt.json` was generated.
- An independent fresh execution of audit() exactly matched its recorded
  report. All55 recorded source/document hashes and six frozen proof
  receipt hashes matched. This is an integrity check, not another review.
- No Lean file changed; the previous180-theorem/283-declaration proof audit
  was NOT rerun or expanded in this pass.

Receipt SHA256:

    a740b2eaab8fa20492ebdf626fbf1db7ffd378413b4cdf42403bf30a82177a27

## Reproduce New Checks

Run from this directory using `/opt/anaconda3/bin/python`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-uniform-measurement-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_measurement.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-uniform-measurement-pycache /opt/anaconda3/bin/python measurement_controls.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-uniform-measurement-pycache /opt/anaconda3/bin/python -m py_compile measurement_plan.py measurement_controls.py test_measurement.py
```

The recorded live command also supplied `--output measurement_receipt.json`.
The report contains five source hashes and the native-source receipt hash.
That native receipt in turn binds50 source files and five earlier receipts.

## Meaning Of Results

Complete source-plus-reference instrument distances in the four finite
controls are0.022786,0.0028433,0.0091674 and0.0060970. Each is below its
derived isometry bound. Norm errors are below3.2e-15. These numerical
values are bounded falsification controls, not universal proofs.

The wrong-sign control has complete instrument distance0.9984056. Retaining
the measured central register in the wrong basis changes its public
translation correlation by modulus1. Both shortcuts are rejected.

For the public resource example p=2^127-1, rank73 and eta=10^-6, the
certificate uses179 phase bits per coordinate,26134 controlled modular
translations and146 binary-QFT blocks. There are22338 phase/label qubits
before target/decoder work. These are not T counts or a quantum execution.
The apparently enormous M=2^179 is not an enumerated circuit or runtime.

No qsearch registry status, CLI, UI, main-repository suite, node check,
commit or push occurred. The intended Developer checkout remained absent
on recheck. No speedup, application-hardness or novelty claim is admitted.

## Files

New: measurement_plan.py, measurement_controls.py, test_measurement.py,
UNIFORM_MEASUREMENT.md, HANDOFF.md, measurement_receipt.json, VERIFICATION.md.
Updated outside this directory: the parent research checkpoint only.
