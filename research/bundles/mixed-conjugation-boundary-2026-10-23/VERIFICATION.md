# Verification

2026-10-23. This bundle is outside the moving repository. No source checkout,
migration staging, Git metadata, registry, or UI was changed. No commit/push.

Executed with /opt/anaconda3/bin/python:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-conjugation-pycache \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-conjugation-pycache \
  python -m py_compile copy_boundary.py test_copy_boundary.py make_receipt.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-conjugation-pycache \
  python make_receipt.py --output copy_boundary_receipt.json
```

- 60 tests passed in 0.95s.
- Three Python syntax checks passed.
- Four live exhaustive joint-state controls and four analytical scaling rows
  were generated. The largest joint enumeration is 5,832 words.
- Direct hidden-orientation averaging independently checks the count-based
  likelihood. Exact rational moments check the classical collision score.
- Equal spectra, nonidentity orbit distance, projector endpoint, fixed
  versus redrawn orientations, likelihood cross moments, ceilings, invalid
  inputs and enumeration caps are explicitly tested.
- Canonical-purification overlap formulas have independent finite floating
  amplitude checks; resource bounds use rational square-root enclosures.

For M=2^64, p=3, v=3/4 and error <=1/3, the birthday argument alone requires
at least 3,506,826,113 copies. This is a necessary worst-case bound, not a
measurement, not a claim that this many copies suffice, and not a bound
against a different access model. The conservative matching-order classical
upper bound is 1,954,687,338,269 copies; its constant is not optimized.

Finite tests do not independently prove the asymptotic information bound
or audit arbitrary quantum circuits. Those arguments are in the note and
await independent review. No succinct-circuit hardness, low-rank obstruction,
new quantum advantage, full-repository test run, qsearch validation, native
quantum execution, or completed migration is asserted.
