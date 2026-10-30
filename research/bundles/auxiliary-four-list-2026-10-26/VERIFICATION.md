# Verification

Date: 2026-10-26. Python3.13.5, python-flint0.9.0.

- Parent tests:36 passed, including exact nonuniform mixture moments,
  all1296 overlap/support cases, rank residues, caps and degree budgets.
- Independent review accepted the conditional theorem and supplied an
  analytical rank proof. Parent replayed all independent controls, including
  7104 matcher comparisons;5506 returned valid label matches.
- Final16-bundle regression:394 passed in13.67s, warnings as errors,
  no skipped tests. This includes81 new tests across the four-list,
  sampler-contract, compressed-algebra and plane-adapter control bundles.
- Ten new Python files compiled successfully across those four bundles.
- `python -B verify_four_list.py --write` followed by `--check` passed.
  Eight-hash receipt SHA256:
  `d49fc4cefa14ae3e48b85785ef90df70700cb31677c50f3e3466ac1a33cb185c`.
- The earlier native matrix-lift receipt also replayed unchanged:
  `6aa7a3ab2e26d66a00fd523e37c4eb92938c39b34b8ce0741b8602676c4a1009`.

Run from this bundle with `/opt/anaconda3/bin/python`:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_four_list.py
/opt/anaconda3/bin/python -B verify_four_list.py --check
```

No primes, Jacobian labels, auxiliary divisors or native witnesses were
constructed. No list of length2^214 was allocated. The conditional exponent
is a mathematical bound, not a timing measurement or hardness conclusion.

This isolated Developer research directory is not a Git checkout. The
intended main Developer checkout is still absent. No full-repository test
claim, qsearch validation, JS/UI change, commit or push is made here.
