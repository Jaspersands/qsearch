# Verification And Integration Boundary

2026-10-24. Read FLAT_OPTIMALITY.md after RESULT.md: the addendum closes
the proposed non-extension-linear escape without changing the solver or
its fixed input. Both mathematical deductions remain LOCAL UNREVIEWED.
The previously authorized Rees reviewer did not review either deduction.

## What Was Run

- 40 focused controls passed in0.55s: 23 norm-flat solver controls and
  17 all-base-field optimality controls.
- The broad external research suite passed **626 tests in6.26s**, warnings
  as errors, no skips, plugin autoload disabled. This includes the 586
  preceding controls. It is NOT the whole repository's test suite.
- All five Python files in this bundle passed py_compile.
- The full make_receipt.py workflow ran twice on the same saved inputs
  and seeds. Its two JSON outputs were byte-identical (cmp exit0).
- flat_optimality.py generated its six certificates, then regenerated
  the same JSON byte-for-byte in a fresh process.
- All14 distinct source/data/dependency entries across both manifests
  matched their SHA256 hashes after the runs.
- A further fresh-process Horner replay of the SAVED native polynomial
  reproduced all684 predicates and degree1709, independently of rerunning
  the solver. The first ad-hoc replay command hit a generic module-name
  collision with the preceding bundle's make_receipt.py; it did not run
  that verification. The corrected fresh process asserted the exact
  imported module path before the successful replay. Integration should
  use package-qualified imports, not assume generic names are unique.

All owned commands finished. No unfinished solver/verification job was
left running.

## Actual Outputs

Every saved solver run below succeeded in one recorded attempt. This is
deterministic replay evidence, not an empirical probability certificate.

| p | M | n | Output degree | Score | Derivative rank |
|---|---|---|---|---|---|
|19|6|15|14|6/6|3|
|31|10|27|26|10/10|3|
|43|14|36|35|14/14|6|
|97|32|81|80|32/32|15|
|193|64|162|161|64/64|30|
|769|256|642|641|256/256|126|
|2053|684|1710|1709|684/684|342|

The last row retains the frozen author's halfsets, multipliers, nonsquare
and ordered cubic orbits, but changes the degree budget from n204 to
n1710. It does NOT solve the original low-rate n204 task. It used1359
norm-candidate checks, a2053-entry square lookup table,1368 random field
draws, one linear system and2052 native point replays. These are partial
named operation counts, not full bit-time or quantum resource estimates.

The p12289,M4096,n9828 rate0.8 ledger still has r2460>D1636. The addendum
proves that1636 is the maximum dimension of ANY common quadratic-zero
F_p-linear direction space, not only extension-linear ones. It does not
prove the original problem hard or exclude target-dependent consistency.

Receipt hashes:

- receipt.json:
  `48bb9a6fc5591e68cb0be2012a3ac735eb7844ef50e5c5e6a44adebae5ea2ae0`
- flat_optimality_receipt.json:
  `aa50721280cbe9a92492c83898a32b36f9018711341b2e28d2c2a25db3c5e0a2`

## Files Changed In These Linked Passes

All changes are external to the migrating repository:

- norm_flat.py: exact native classical completion and paid rank retries.
- test_norm_flat.py: solver, provenance-contract and falsifier controls.
- make_receipt.py: fixed-input runs and source-bound result producer.
- RESULT.md: every-fixed-input classical probability proof and scope.
- HANDOFF.md: bounded integration instructions for the original solver.
- data/native.npz: frozen public reference input, not a generated witness.
- data/cubic-parent.json: frozen resident original geometry/provenance.
- receipt.json: actual native witnesses, failed-center control and hashes.
- FLAT_OPTIMALITY.md: stronger all-base-field theorem and revised next step.
- flat_optimality.py: exact moment/annihilator/projection certificates.
- test_flat_optimality.py: assumption and non-extension-linear controls.
- flat_optimality_receipt.json: six certificates and bound/provenance ledger.
- VERIFICATION.md: this evidence and change record.
- ../RESEARCH_CHECKPOINT_2026-10-23.md: current conclusion and continuation.

Generated Python caches are not research artifacts. No original Desktop
file, migration staging file, main CLI, main registry, UI or Git metadata
was changed. The intended Developer checkout was absent when checked in
this pass. No whole-repository tests, qsearch.py validate, node --check,
commit or push was performed. Preserve the user's infrequent-commit rule.

## Reproduction

From this bundle, using the existing Python with python-flint/numpy/pytest:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_norm_flat.py test_flat_optimality.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python make_receipt.py --output /tmp/norm-flat-replay.json
cmp receipt.json /tmp/norm-flat-replay.json
/opt/anaconda3/bin/python flat_optimality.py --output /tmp/flat-bound-replay.json
cmp flat_optimality_receipt.json /tmp/flat-bound-replay.json
```

Integrate only after verified migration, reconciling concurrent changes.
Use the ADDENDUM's next-step instructions rather than the superseded
non-extension-linear suggestion in the frozen RESULT.md/HANDOFF.md.
Do not promote this into a whole-family dequantization or speedup claim.
