# Verification Record

2026-10-23. All checks below completed locally. No running test/replay process
is required to retain the results.

## Completed

- 42 new tests in test_residual.py and test_borel_residual.py.
- 315 selected tests PASS in 61.17 seconds: this bundle plus source-pullback,
  kernel-output, quadratic-cancellation, scalar-cancellation and central-rank.
- Six new Python files pass py_compile. Bytecode is outside the checkout at
  /tmp/qsearch-residual-pycache; pytest plugin autoload and cache were disabled.
- replay_residual.py --output receipt.json completes. A second independent
  invocation of run() produces exactly the same parsed JSON.
- All 12 recorded SHA-256 hashes match the current implementation/test files
  and imported research dependencies.
- Supplemental ell=3 split and nonsplit frame-construction probes complete.
  These are not included as additional pytest cases or geometric evidence.

The selected test command, run from this bundle with /opt/anaconda3/bin/python:

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-residual-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider \
      ../frobenius-residual-2026-10-23 ../source-pullback-2026-10-23 \
      ../kernel-output-2026-10-23 ../quadratic-cancellation-2026-10-23 \
      ../scalar-cancellation-2026-10-23 ../central-rank-2026-10-23

Syntax check:

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-residual-pycache \
      /opt/anaconda3/bin/python -m py_compile residual.py residual_controls.py \
      borel_residual.py replay_residual.py test_residual.py test_borel_residual.py

## Receipt Outcomes

| Arithmetic input | ell | Image rank | Compatible planes | Outcome |
| --- | --- | --- | --- | --- |
| p=11 split | 5 | 0 | 8 | GL2 embedding; actual fixture is a classically verified exceptional plane |
| p=11 split | 5 | 1 | 2 | Correct reference kernel selected with 2 original opaque-label calls |
| p=11 split | 5 | 2 | 1 | Correct reference kernel from image; no label calls |
| p=7 nonsplit | 5 | 0 | 6 | SL2 embedding; published receiver NOT executed |
| Previous p=7 fixture | 11 | 1 | 2 | Correct reference kernel selected with 2 original opaque-label calls |

Each of these first reconstructs alpha from weak arithmetic packets using
the previous bounded CRT implementation. Secret phi is confined to callbacks
and final reference comparison. Counts describe compatibility with this map,
not all available input information.

An additional integral source map satisfying the exact skew/square relations
has nonsplit rank one and ZERO compatible kernels. It is rejected as
inconsistent with the genuine-input promise. This falsifies the tempting
inference that exact source identities alone certify a geometric input.

At ell=2^127-1 the local rank-one control produces two candidates and both
rank-zero public embeddings pass equivariance checks. These matrices are
local arithmetic controls without a certified global geometric origin.
Random-source calls, including the separate scalar backend, are accounted.

## Failures Found And Corrected

The first run had 15 passing and three failing tests. The fixture compared
a residue-reduced symplectic form against an integer form containing -1,
incorrectly rejecting valid transvections. Comparing the difference modulo
ell fixes this; the final complete collision checks pass. The mathematical
transvection formula was unchanged. A subsequent accounting self-check added
scalar-backend generator and curve draws to the reported random-draw count;
three explicit counting-RNG tests pass.

## Not Established

No PPAV geometry, target Frobenius extraction, source oracle implementation,
quantum receiver, new natural instance, cryptanalytic result or independent
review was executed. The Borel receiver is imported from published work.
No registry candidate or real-input negative result was admitted.

This is NOT a full-repository test pass. qsearch validate and node --check
index.js were not run. No source/UI changes, commits or pushes were made.
The live migration check still showed PID 4829 running migrate-projects.py
and no /Users/jaspersands/Developer/quantum algorithm search destination.
Only this isolated bundle and the research checkpoint were edited. Do not
integrate into the moving source/staging tree; follow HANDOFF.md afterward.
