# Paid A3 Pullback Verification

27 October 2026. This verifies finite controls and the implemented public
reduction. It does NOT execute the imported quantum parabolic algorithm.

## Executed

With /opt/anaconda3/bin/python, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and
PYTHONPYCACHEPREFIX=/tmp/qsearch-a3-pycache, pytest -q -p no:cacheprovider
-W error on these four modules passed121 tests in9.74s:

* test_a3_pullback.py (18 new tests)
* ../orthogonal-exterior-2026-10-27/test_exterior_probe.py
* ../orthogonal-three-probe-2026-10-23/test_orthogonal_probe.py
* ../orthogonal-general-rank-2026-10-27/test_general_rank.py

Three-file py_compile passed for a3_pullback.py, test_a3_pullback.py and
run_controls.py. The deterministic live workflow passed both commands:

```text
python run_controls.py --write live_receipt.json
python run_controls.py --check live_receipt.json
```

The receipt checks all730 F3 flags/corresponding singular spaces: counts
130/520/80 at hidden ranks1/2/3. It also checks12 opaque pullback cases
across four flag types and p=3,5,2^127-1. Each makes13 legal SL queries
and exactly13 original SO queries; no field-sized table is queried.
These checks use supplied-secret fixtures, NOT a solver recovering the
secret from those13 queries. Tests separately compare every pair of
19 selected opaque labels against flag-image equality for each field/type.

Main qsearch.py validate passed: valid=true, issues=[], unchanged
8 candidates,796 experiments,807 results,973 negative results.

## Mathematical Review Scope

An independent AI review confirmed the imported SL4 oracle interface for
all four types. Parent read the entire report, including scalar-root
cleanup, constant-density sampling, containment verification and the later
GL3 quotient oracle. The review did not reprove the exterior-square map,
audit code, execute tests, supply human validation or certify novelty.

SHA256 of final result and preserved evidence:

```text
RESULT.md
edf8dc351d89d7f23048b2f9000449237eafb331d1b9ef18a6cc3a15b2e64f62
live_receipt.json
84f0339b4681972fcf609970afc809ee032d7be4a679de9056699140d1b6c7ba
../orthogonal-a3-prior-art-review-2026-10-27/REVIEW.md
5513a87cbb02d566390e2fe1e16077bcffd5e7482ed6dd9f30aaed562441225c
```

No full main-suite or JavaScript checks, compiled quantum solver, hardware
execution, registry promotion, CLI/UI work, commit/push, dependency install,
storage repair or external contact. Existing dirty user files preserved.
Bundle/review remain outside Git; main handoff pointers are not a backup.
