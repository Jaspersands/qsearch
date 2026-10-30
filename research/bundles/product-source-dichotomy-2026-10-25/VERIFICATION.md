# Verification And Scope

2026-10-25, isolated workspace /Users/jaspersands/Developer/qsearch-research-work.

## Established In This Pass

Written fixed-dimension product-target dichotomy, plus a surface-only
classifier and access-preserving elliptic response restriction. The general
proof has NOT been independently reviewed or formalized. Arithmetic
controls are not actual geometric weak-isogeny instances.

The final suite contains 20 new tests. The five-file scoped regression run
completed with 150 PASS in 38.61 seconds, warnings treated as errors, no
skips. Before the added unpolarized-shear countercontrol, the initial new
suite passed 19 tests and the earlier combined run passed 149. Only the
final 150-test result is the completed milestone.

Commands run from the isolated workspace:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error product-source-dichotomy-2026-10-25/test_product_dichotomy.py source-pullback-2026-10-23/test_pullback.py product-corner-attack-2026-10-23/test_product_corners.py bielliptic-source-2026-10-24/test_bielliptic.py source-residual-algebra-2026-10-24/test_residual_algebra.py
/opt/anaconda3/bin/python -m py_compile product-source-dichotomy-2026-10-25/product_dichotomy.py product-source-dichotomy-2026-10-25/check_controls.py product-source-dichotomy-2026-10-25/test_product_dichotomy.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python product-source-dichotomy-2026-10-25/check_controls.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python product-source-dichotomy-2026-10-25/check_controls.py --check
```

All three syntax checks PASS. Final receipt write/check and a separate
read-only replay PASS. Receipt SHA256:

    b6f693c1236fe9311c85eb0a204187977772637f3c6b87c44762f3f9ad135271

At characteristic 11 and ell=5 the constructed mixed control recovers a
two-dimensional kernel. Diagonal and permuted controls return elliptic
routing (0,1) and (1,0), respectively, and NO kernel. Both verify masked
elliptic blocks against the fixture's exact maps. All controls use weak
observations at 3,7,13, with CRT modulus 273 > 2*17. The common masks are
not recovered. No weak query is made at ell; the PUBLIC algebra split at
ell is separately supplied, using a small enumerative fixture.

The tests reject insufficient levels before callbacks, invalid exact
projector identities, a nonfaithful split, illegal routing, singular
elliptic blocks, and a nonunitary unpolarized shear. All geometry, elliptic
backend and classical-hardness flags remain false. No quantum execution.

## Files Added

- PRODUCT_DICHOTOMY.md: proof, input model, falsifiers and general-g scope.
- product_dichotomy.py: surface arithmetic classifier and mask-preserving
  response restriction; reuses the existing source pullback code.
- test_product_dichotomy.py: 20 tests including invalid-advice controls.
- check_controls.py and receipt.json: reproducible integral controls.
- LITERATURE_GATE.md: versioned withdrawal audit, qualified global-oracle
  composition and follow-on division-runtime check.
- sources/2026-1198-revised-2026-10-12.pdf: retained primary evidence,
  hash checked against the downloaded original; not edited.
- HANDOFF.md and this file: integration instructions and verification.

The shared isolated RESEARCH_CHECKPOINT_2026-10-23.md is the only pre-existing
file edited in this pass. Existing dependency code/receipts were not changed.

## Not Run Or Claimed

No main-checkout tests, qsearch validation, node check, CLI/registry/UI
integration, Git changes, commit or push. The intended verified-local
main destination was still absent on the live check. The Desktop source,
migration staging area and migration jobs were not modified.

The standalone controls finish; no research/test process is left running.
The overall goal remains active. General modeled Jacobians, exact geometric
source implementation, matched classical advantage and independent review
remain unresolved. Do not present the new classification as a Shor-level
result or the known elliptic reductions as newly invented algorithms.
