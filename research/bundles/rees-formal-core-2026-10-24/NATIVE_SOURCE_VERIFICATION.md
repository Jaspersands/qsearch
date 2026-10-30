# Native Source Verification

2026-10-24. Nine new artifacts: ReesNativeSource.lean,
AuditNativeSource.lean, verify_native_source.py, native_source_controls.py,
test_native_source.py, REES_NATIVE_SOURCE_SCOPE.md, NATIVE_SOURCE_HANDOFF.md,
native_source_receipt.json and this report. Parent checkpoint updated.
All nine preceding Lean modules and their frozen receipts remain unchanged.

## Executed Checks

- Full ten-module Lean rebuild passed without warnings or errors. The
  fresh recursive-source base report exactly matched its frozen receipt.
- Lean 4.35.0; mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679.
- 13 new theorems and six new definitions. Combined: 180 theorems and
  283 explicit audited declarations. Only propext, Classical.choice and
  Quot.sound occur. This does not discharge remaining theorem hypotheses.
- 27 new Python tests. Focused selection: 122 passed in 1.93 seconds.
- Expanded external regression selection: 994 passed in 32.75 seconds,
  warnings as errors, no skips. This is the preceding 967-test selection
  plus test_native_source.py, not the complete main repository suite.
- All three new Python files passed py_compile.
- All 50 recorded source/document hashes and five frozen receipt hashes
  matched after the successful rebuild.
- The live finite control was also executed by the verifier. Maximum
  source-entry error was 6.94e-18 across all three hidden-subgroup cases.
  Wrong-side trace distance: approximately 0.5925925926; dirty evaluation
  workspace trace distance: 2/3. Naive projection success for ten F_3
  Heisenberg factors is exactly 1/3486784401 by the dimension formula.

Receipt SHA256:

    24a331c78d1240bd3719b1067d632a9dc0500d88e20bb37761ddc77faf917eb0

Initial compiler diagnostics concerned a documentation-comment position,
deprecated ite lemma names and unused section instances. These were fixed
without new mathematical assumptions, sorry terms, or warning suppression.
The final verifier actually invokes Lean; the Python manifest tests alone
are not proof evidence.

## Reproduce

From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python verify_native_source.py --output native_source_receipt.json
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-native-source-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_native_source.py test_recursive_source.py test_quotient_verifier.py test_cancellation_verifier.py test_group_bridge_verifier.py test_verify.py test_central_controls.py ../rees-channel-2026-10-23/test_physical_channel.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-native-source-pycache /opt/anaconda3/bin/python -m py_compile verify_native_source.py native_source_controls.py test_native_source.py
```

The broad command uses the exact selection documented in
RECURSIVE_VERIFICATION.md with
rees-formal-core-2026-10-24/test_native_source.py prepended. It ran from
the parent qsearch-research-work directory with the same environment and
pytest flags. The finite controls are matrix calculations, not quantum
hardware execution or a scalable quantum simulator.

## Scope And Checkout State

Resolved: native copy-only pullback, actual Rees top-source acquisition,
public top-coordinate equivalence, and substitution into the recursive
record/average source identities. No source inverse, strong hiding-function
oracle, hidden inverse map or kernel-index postselection is used.

Still required: independent native source supply, uniform public addresses,
reversible arithmetic and clean workspace; base BCH/Lazard correspondence,
complete character and diagonal-witness plans, final Fourier recovery,
uniform circuit/resource guarantees, useful application and novelty review.
No new independent reviewer or full-algorithm/speedup claim.

Main Developer checkout remained absent at the start and end. Main
Desktop/staging, registry, CLI, UI and Git were untouched. Main tests,
qsearch validate, Node checks, commit and push were not run against the
unverified moving checkout. All owned compiler/test sessions completed.
