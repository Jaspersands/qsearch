# Verification

Completed 2026-10-24. All owned test/replay processes finished successfully.

## Executed Checks

- 18 new tests plus 123 existing external Rees/HDQI tests: **141 passed**,
  warnings treated as errors, pytest plugin autoload disabled. Exit 0.
- `py_compile relative_flow.py test_relative_flow.py`: exit 0, with bytecode
  outside the checkout.
- Two live `relative_flow.py` runs: exit 0. `cmp` confirms byte-identical
  local `receipt.json` and `/tmp/qsearch-relative-flow-replay-2026-10-24.json`.
- Six `shasum -a 256` values match the receipt, including both dependency
  implementations.

Combined regression command from the external research-work directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-relative-flow-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-relative-flow-2026-10-24/test_relative_flow.py rees-class-three-2026-10-24/test_class_three.py hdqi-parent-gap-2026-10-23/test_parent_gap.py hdqi-filtered-parent-2026-10-24/test_filtered_parent.py hdqi-gap-baseline-2026-10-24/test_gap_baseline.py
```

## Receipt Coverage

Thirty dense rows cover seven small graphs, including commuting, matching,
path, star and clique cases, with negative and nonuniform dyadic couplings.
They check the exact defect Gram identity, its degree-weighted bound,
real-time propagation, and the Gaussian-filter commutator estimate.
Twenty-three tagged-sector rows independently compare filter coefficient
vectors with the energy-basis construction of the actual operator jump.

Additional tests numerically integrate the folded-Gaussian moments and an
outer squared bound; check the strict moment-domain threshold; reject
discarding a nonzero action on a seminorm kernel; and match the two
counterexample formulas against independent small dense calculations.

Four connected-circulant PARAMETER ledgers hold beta^2(d+1)=0.01. Their
new squared relative bounds stay below 0.037 even as the earlier mass-gap
perturbation radius exceeds one. These are not constructed large matrices,
gap estimates, or quantum runs. Small relative bounds never set the
`parent_gap_certified` flag.

Four product-state metric ledgers and four matching imaginary-time ledgers
record analytic counterexamples. They falsify proof shortcuts, not fast
mixing or preparation of those easy tensor-product examples.

## Hashes

```text
15bf4323d0ec4bbf5b6fef1060b486c500c46e2de90d4d00ad5bc09e260350c6  relative_flow.py
6d0f1afed6c5dc21c208dd22c0adec24f000a2d8b833a9186a768d2bc4c7cf0c  test_relative_flow.py
84a40280bf99e215e44dd43493e8c5a58effc61124388634c02c21d361b77bbc  RELATIVE_FLOW.md
a37f9f3a6b5492bf207db5f858d0c3c38277c1ad06e9491e4e0b1a327d3fdef1  HANDOFF.md
ac5e1491f4c65993bdbdd8b06bb7b437fba5695fbcb56b9f095cb8f22af738d5  ../hdqi-parent-gap-2026-10-23/parent_gap.py
e0795edac6a4789d5f7eccf8da78615194a3750f5bb9c82f77d8ffdd8ba5f90b  ../hdqi-filtered-parent-2026-10-24/filtered_parent.py
```

## Scope Limits

The general deductions rest on the written algebra and inequalities, not
finite tests. They have not had an independent review or comprehensive
novelty check. No global parent gap or preparation algorithm was established.

The Desktop checkout was not edited and the intended Developer checkout
was rechecked and remains absent. No central `qsearch.py validate`, full
repository test suite, Node check, registry/CLI/UI change, commit or push
was attempted. The six new bundle files and the external checkpoint are
the complete edit scope.
