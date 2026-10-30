# Verification Receipt

Completed 2026-10-24, after the all-active witness controls and matched
classical comparison were added.

## Executed

- 17 new tests and 106 existing external HDQI tests: **123 passed**,
  warnings treated as errors, pytest plugin autoload disabled. Exit 0.
- `py_compile class_three.py test_class_three.py`: exit 0; bytecode sent
  to `/tmp/qsearch-class-three-pycache`.
- Two live `class_three.py` runs: exit 0. The local `receipt.json` and
  `/tmp/qsearch-class-three-replay-2026-10-24.json` compare byte-identical
  with `cmp` (exit 0).
- Four SHA-256 values returned by `shasum -a 256` match the receipt.

The combined test command, run from the external research-work directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-class-three-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
```

## Exact Control Scope

- 281 independent associative-exponential/BCH comparisons.
- 1,000 cover-basis Jacobi checks.
- 600 evaluation and 600 dilation basis-bracket checks.
- Two cubic and three quadratic quotient stages.
- 5,831 complete positive-label tuples, one selected witness each;
  five additional all-active witnesses.
- 49 explicitly stored, exact nonzero moments per main record; all
  unlisted moments are zero. This represents a function on each entire
  group, not a dense enumeration of its elements.
- 10,240 main address-entry checks using two sections; 2,048 additional
  checks in the center-contained control.
- All 16,807 final Fourier frequencies checked. Exactly 2,401 have mass
  1/2,401. The recovered line is span(x+u), retaining the central tilt.
- Independent-source cost ledger: 432 lifted / 1,296 original inputs per
  terminal state for this scalar-flag schedule. No quantum inputs were
  actually prepared or consumed by this classical checker.

## Final Hashes

```text
4550a5536e35b19cd530b7f2915b7e731b15b9701de477109e4fd261fdf69475  class_three.py
75c8af07e78c1a26860489107d9fdcfb61909708d57f268d741de3ea32ff6fe5  test_class_three.py
f08f4b3de38e9a66bd03670583d298e085d45e63b4414b9e19e88aa4d79cb74a  CLASS_THREE.md
e8f5cc47e6788d7a67f46be3b78f9aa0b3a3855e6646077485028a39cd27eab5  HANDOFF.md
```

## Not Executed Or Claimed

No quantum circuit, generic finite-field SDE solver, black-box outer
algorithm, new independent review, or formal proof checker was run. The
matched classical comparison is a written standard collision argument,
not a benchmark or novel lower bound. Literature scope was checked, but
originality is not certified.

No original-checkout full test suite, `qsearch.py validate`, Node check,
central registry/CLI/UI update, commit, or push was performed. That checkout
remains incompletely available after the migration stopped; no source or
staging files were edited. The only files created are this six-file bundle;
the external research checkpoint was updated separately. Earlier Rees
manuscript and reviewer files are unchanged.
