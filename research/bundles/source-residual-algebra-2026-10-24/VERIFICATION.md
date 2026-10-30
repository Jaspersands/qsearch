# Verification: 2026-10-24

Status: checked local deduction and arithmetic prototype; independent
mathematical review, novelty assessment and actual geometric execution
remain unperformed. No quantum execution or speedup claim.

## Executed Checks

- Final focused dependency selection: 237 tests PASS in 84.92 seconds,
  warnings as errors, no skips. This includes 29 new tests.
- Four new Python files pass py_compile.
- Live replay completes the three bounded-CRT source reconstructions;
  old ranks are (1,1) in each case, and new compatibility counts are
  respectively 2, 1, 12. Independent quaternion Hom-module checks agree
  on every one of the twelve completions in each fixture.
- The two strict controls have target-map minimal polynomial degree four,
  excluding a scalar-shifted quadratic Frobenius interpretation.
- The unique control recovers the reference kernel with no label call;
  the two-candidate control uses two original-relation opaque labels.
  ACTUAL geometric label calls remain zero in both cases.
- All 81 residual operators over F3 are checked against all 40 Lagrangians.
  Further controls cover noncommuting operators, invalid common lines,
  both residue digits, adjoints, coordinate/chart changes and root aborts.
- A 127-bit local-only control returns two candidates without enumeration;
  its scalar counterpart retains ell+1 symbolically.
- Fresh replay equals saved JSON exactly. All 12 recorded source/document/
  dependency hashes match. Receipt SHA256:
  `47657c405ed5fe2e11af1cba0931fadab61f342140b6bb1948e264df24f17b9d`.

The initial run exposed four errors in the NEW test's invocation of the
existing lift API: it requires a four-coordinate shift, not a scalar.
Those calls were corrected without changing the helper or theorem. The
final selection was rerun after the last new adjoint regression was added.

## Reproduce

From /Users/jaspersands/Developer/qsearch-research-work, use
OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1,
PYTHONPYCACHEPREFIX=/tmp/qsearch-residual-algebra-pycache,
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and /opt/anaconda3/bin/python.

Run `-m pytest -q --tb=short -p no:cacheprovider -W error` on:

    source-residual-algebra-2026-10-24/test_residual_algebra.py
    source-pullback-2026-10-23/test_pullback.py
    frobenius-residual-2026-10-23/test_residual.py
    frobenius-residual-2026-10-23/test_borel_residual.py
    kernel-output-2026-10-23/test_kernel_output.py
    kernel-output-2026-10-23/test_uniform_source_bound.py
    scalar-cancellation-2026-10-23/test_scalar_cancellation.py
    product-corner-attack-2026-10-23/test_product_corners.py

From this bundle, run `replay.py --output receipt.json`. It is a proof-control
runner, not qsearch integration or a real geometric attack. Its public
extraction routines never receive the fixture's secret isogeny.

## Files And Exclusions

Eight new external files: residual_algebra.py, algebra_controls.py,
test_residual_algebra.py, replay.py, RESIDUAL_ALGEBRA.md, HANDOFF.md,
receipt.json, and this verification record. The parent research checkpoint
is updated. No older frozen source or receipt is edited.

The intended Developer checkout is absent. No main/staging edits, registry
admissions, CLI/UI changes, migration operations, commits or pushes occurred.
No full-repository tests, qsearch.py validate, node check or Lean rebuild is
claimed. Those are not replaced by the focused external selection. All
owned execution sessions completed; the broader research goal remains active.
