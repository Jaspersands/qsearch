# Verification Record

2026-10-23. All work is in the separate local research directory. The
migration worker was confirmed live and the verified destination checkout
was still absent at the final check. No repository/staging writes, commits,
pushes, registry updates or UI changes were made.

Executed with /opt/anaconda3/bin/python:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-walsh-pycache \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-walsh-pycache \
  python -m py_compile walsh_attack.py test_walsh_attack.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-walsh-pycache \
  python -u walsh_attack.py --output native_attack_receipt.json
```

- 17 focused tests pass; final focused rerun took 0.55s.
- Two Python syntax checks pass.
- The four-run native workflow was executed and then deterministically
  replayed after strengthening field/point provenance checks. Both executions
  produced the same four scores and accepted-move counts. No new seeds, extra search
  sweeps or favorable-run selection were introduced.
- Per reproduction: 2,520 scanned lines and 20,641,320 FFT-represented scalar
  displacements. All returned witnesses were scored on all 6,000 rows.
- 25,231,360 exact scalar congruences verify binary translation covariance;
  independent direct sums check the Walsh implementation.
- The original field polynomial, generator, point lists, center hash and
  inherited witness match the saved artifact. The explicit matrix SHA256 is
  9e05f406a159800ae97f6136c2dc237594b7f800a9fe0dba4e83bd291ff5097e.
- Six receipt hashes (three new inputs and three resident dependencies)
  were checked and match.
- Every returned witness passed the unchanged exact fast convolution and
  explicit-matrix replay. Arb final-score intervals certify all four below
  0.3; they do not certify the floating line-search optimization decisions.

A broader local milestone ran this suite together with the preceding
mixed-conjugation copy-bound suite: **77 passed in 1.30s**. This is not
full-repository validation. qsearch.py validate, the full test collection,
UI syntax checks and integration were not run against the moving checkout.

The bounded failure is not classical hardness, a mixing-time lower bound,
an improved quantum result or a novelty claim. See RESULT.md for the exact
research decision and limitations.
