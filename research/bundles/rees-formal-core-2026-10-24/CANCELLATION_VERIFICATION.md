# Cancellation Verification

2026-10-24. Eight new files: ReesCancellation.lean,
AuditCancellation.lean, verify_cancellation.py,
test_cancellation_verifier.py, REES_CANCELLATION_SCOPE.md,
CANCELLATION_HANDOFF.md, cancellation_receipt.json and this report.
The parent research checkpoint was updated. No previous formal source,
audit, verifier, documentation or frozen receipt was modified.

## Executed Checks

- Lean 4.35.0, mathlib revision
  `56a005855ea17e0b0958f73ec801ae140b0a1679`.
- verify_cancellation.py rebuilt the five frozen modules and compared their
  two verification records to the frozen receipts. It compiled the new
  module and audited all 28 new explicit declarations. No final compiler
  errors or warnings. Only propext, Classical.choice and Quot.sound.
- New work: 15 theorems and 13 explicit definitions. Combined six-module
  total: 104 theorem declarations and 153 explicit audited declarations.
  Axiom checks do not discharge mathematical hypotheses.
- Focused tests: 55 passed in 1.44 seconds, including 14 new verifier
  tests plus prior verifier and physical central controls.
- Expanded external selection: 939 passed in 33.65 seconds, warnings as
  errors, no skips, plugin autoload disabled. This is the previous
  925-test selection plus test_cancellation_verifier.py.
- Both new Python files passed py_compile.
- All six new source/document hashes, six frozen group-bridge hashes,
  18 frozen base hashes and both frozen receipt hashes were checked
  after the successful full compilation.
- One successful full verifier run generated this receipt. A second
  complete rebuild/byte-identical replay was not performed this pass.

Receipt SHA256:

    0ed9290e03ebf710f4cde4fa122076b6873fa06c89c9bbc3b56ac529de10d141

Initial compile errors were a reserved identifier, explicit scalar-equivalence
type arguments, an over-broad rewrite through the hidden-decomposition
expression, and different decidable equality instances for the same Fourier
condition. They were repaired directly; deprecated names and unused section
variables were corrected. No axiom, linter suppression, weakening of the
claimed channel or removal of the nonzero witness was used.

## Reproduce

From this directory:

```sh
PYTHONPYCACHEPREFIX=/tmp/qsearch-cancellation-pycache /opt/anaconda3/bin/python verify_cancellation.py --output cancellation_receipt.json
PYTHONPYCACHEPREFIX=/tmp/qsearch-cancellation-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_cancellation_verifier.py test_group_bridge_verifier.py test_verify.py test_central_controls.py
PYTHONPYCACHEPREFIX=/tmp/qsearch-cancellation-pycache /opt/anaconda3/bin/python -m py_compile verify_cancellation.py test_cancellation_verifier.py
```

The broad command is the 913-test command in
../pencil-norm-filter-2026-10-24/VERIFICATION.md, with
rees-formal-core-2026-10-24/test_group_bridge_verifier.py and
rees-formal-core-2026-10-24/test_cancellation_verifier.py prepended.
It ran from qsearch-research-work with the same flags.

## Not Established

No quantum execution, new natural hard application, new independent review,
novelty certification, diagonal solver or full recursive algorithm. The base
BCH law, complete Fourier family and nonzero moment witness finder remain
explicit. The result constructs the first central channel from these inputs;
the compatible graded quotient chain remains outside this proof.

The main Developer checkout was absent at both checks this pass. Main
Desktop/staging, registry, CLI, UI and Git were not modified. Whole-repository
tests, qsearch validate, Node checks, commit and push were not run against
the unverified moving source. These 939 tests are an external regression
selection, not the whole main repository. All owned compiler/test sessions
returned terminal results; none remains running.
