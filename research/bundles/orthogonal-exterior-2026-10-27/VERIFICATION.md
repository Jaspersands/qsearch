# Verification Ledger

27 October 2026. Finite reference checks support debugging and reproduction;
they do not prove the theorem or establish novelty/natural-input advantage.

## Executed Checks

Runtime: /opt/anaconda3/bin/python, existing NumPy/python-flint/pytest.

From this bundle, with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and
PYTHONPYCACHEPREFIX=/tmp/qsearch-exterior-pycache:

```text
python -m pytest -q -p no:cacheprovider -W error test_exterior_probe.py
  ../orthogonal-three-probe-2026-10-23/test_orthogonal_probe.py
  ../orthogonal-general-rank-2026-10-27/test_general_rank.py
103 passed in 9.34s
```

The actual invocation supplied all three test paths on one command line.
28 tests are new; 75 cover the two reused orthogonal bundles. Earlier
combined collection found a generic controls.py import collision; the new
file was renamed exterior_controls.py and the complete selected set rerun.
No existing test modules were changed or skipped to obtain this result.

Four-file py_compile passed for exterior_probe.py, exterior_controls.py,
run_controls.py and test_exterior_probe.py. Both commands below completed:

```text
python run_controls.py --write live_receipt.json
python run_controls.py --check live_receipt.json
```

The deterministic native cases are (n,k,q)=(3,1,3),(4,1,3),(4,2,3), using
81,2187,2187 CLASSICAL original oracle calls respectively. Each is three
full-table probes, with 24 simulated Fourier samples per table. The
controller receives neither U nor k. Every query's determinant is checked
to be1; the fixture exposes only opaque labels. No quantum algorithm was
executed. These are reference counts, not the analytic quantum ledger.

Exhaustive controls include:

* All80 maximal singular spaces in dimension6 over F3, all27 radical
  parameters per probe, and hidden ranks1/2/3: exact fibers and screen.
* All2240 maximal spaces in dimension8 over F3 with hidden rank2:
  648 distinct good supports, each with exactly3 good maximal extensions.
* All121 hyperplanes of the five-dimensional Uperp in the n3/k1/F3 case:
  conditional support-containment fractions0,1/4 or1/9 as predicted.
* Explicit d=0,1 blindness and an undersampled-kernel superspace whose
  proper image support is polluted outside Uperp.
* Exact fixed-line fractions for selected reflection, root, unipotent-Levi
  and frame matrices over F5/F7, and universal +/-I collision controls.
* Prime-field group law/determinant and rotated kernel algebra up to the
  prime2^127-1. These use supplied-secret fixtures, not large-field learning.
* All geometric, rank, row-sampler, random-integer and instrument budget
  terms, including a64-dimensional-Witt-rank analytic resource case.

Main-repository qsearch.py validate passed: valid=true, issues=[], with
8 candidates,796 experiments,807 experiment results and973 negative results.
No central registry was changed or speedup candidate promoted.

## Independent Review

The separate AI reviewer reconstructed both mathematical arguments and
found no fatal flaw. The parent read the full report and applied its
precision/wording clarifications; see REVIEW_RESPONSE.md. The reviewer
did not inspect code, run tests, certify novelty or perform human review.

SHA256 after those clarifications:

```text
RESULT.md
32ac5623e9c0c145d8219f2504eb4668c7a4fc4c58439a04215f64e79d62fb7a
CLASSICAL_COMPARATOR.md
d7e8a8d3ce1a970d5adf8946315afb37a5729429e7cc3497cdddcae068f06b79
live_receipt.json
af8e43729ca51d5e40b9c02913e628d0b0ec3d6475f918501e9001c659b73321
../orthogonal-exterior-review-2026-10-27/REVIEW.md
9c1d3df3680b8b95d5db49e9e818974472e23b5525eabae1fc84eb52926a8089
```

Not run or claimed: full main-repository test suite, JavaScript checks,
quantum compilation/hardware execution, a combined low/high-rank CLI,
extension-field Python implementation, natural-input reduction, literature
novelty certification or outside specialist review. No UI/CLI changes,
dependency installation, migration, commit/push or external contact.
The bundle and review are outside Git; a repository pointer is not a backup.
