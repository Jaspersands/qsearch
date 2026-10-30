# Verification: 2026-10-23

## Results

- 30 new tests passed in the final local suite (6.10 seconds).
- 119 tests passed across source-pullback, product-corner-attack,
  kernel-output and source-field-audit (15.72 seconds). These include the
  30 new tests; the totals are not additive.
- Four new Python files passed py_compile with external pycache.
- The deterministic four-case replay ran successfully and receipt.json was
  written using apply_patch. It records five source/dependency SHA-256 hashes.
- The final receipt-comparison command below independently reruns the
  arithmetic and checks exact equality to the saved JSON.

Recorded rank histories:

| Control | Ranks | Outcome |
|---|---|---|
| Known map with useful quadratic words | 1, 2 | Complete under input promise |
| Frobenius relation, both factors stable | 0 | No image information |
| Frobenius relation, one factor stable | 1, 1 | Partial kernel line |
| Frobenius relation, neither factor stable | 2 | Complete under input promise |

The word example reconstructed its source map from levels 3,7,13, with
CRT modulus 273 > 2*67. Each Frobenius-relation control used 3,5,13,17,
with modulus 3315 > 2*116. Different common weak masks and a changed target
symplectic frame are included. No ell-torsion points or full target-order
data are arguments to the extractor. The reference fixture has phi only
to synthesize small-level observations and check the result afterwards.

## Reproduction

From this directory:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-pullback-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-pullback-pycache /opt/anaconda3/bin/python -m py_compile pullback.py controls.py test_pullback.py replay.py
/opt/anaconda3/bin/python -B replay.py
/opt/anaconda3/bin/python -B -c 'import json; from pathlib import Path; from replay import run; assert run() == json.loads(Path("receipt.json").read_text()); print("receipt and five hashes match")'
```

The combined test invocation lists these four sibling directories explicitly:
source-pullback-2026-10-23, product-corner-attack-2026-10-23,
kernel-output-2026-10-23 and source-field-audit-2026-10-23.

## What Was Not Verified

No geometric torsion points, surface quotient, actual target Frobenius
self-conjugacy, or quantum operation was executed. Point-access counts in
the receipt are requirements, not executions. The small-prime splitting
fixture is not a large-prime algorithm. The global weak-source/norm/map
promises cannot be certified by these finite observations. The new proof
has not had an independent review; the authorized Rees reviewer did not
inspect it. Novelty and general classical hardness are not established.

This is not full repository validation. qsearch.py validate, node --check
and the full repository test suite were not run against the migrating
checkout. No checkout, staging files, registry entries, Git state, commits
or pushes were changed. Integration work is specified in HANDOFF.md.
