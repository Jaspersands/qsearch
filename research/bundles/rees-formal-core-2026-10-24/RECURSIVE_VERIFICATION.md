# Recursive Source Verification

2026-10-24. New formal artifacts: ReesStageInstrument.lean,
ReesRecursiveSource.lean, AuditRecursiveSource.lean,
verify_recursive_source.py, test_recursive_source.py,
REES_RECURSIVE_SCOPE.md, RECURSIVE_HANDOFF.md,
recursive_source_receipt.json and this report. A separate mathematical
resource/prior-art note was added; it is not included in the Lean proof
receipt. The parent research checkpoint was updated.

## Executed Checks

- Full nine-module Lean rebuild and axiom audit passed without diagnostics.
  The rebuilt seven-module base matched its frozen quotient receipt.
- Lean 4.35.0; mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679.
- 25 new theorems and 22 new explicit definitions/structures/inductive
  declarations. Combined: 167 theorems / 264 audited explicit declarations.
  Only propext, Classical.choice and Quot.sound occur. The theorem
  hypotheses remain obligations, not discharged algorithmic procedures.
- Focused test selection: 83 passed in 1.48 seconds, warnings as errors.
- Expanded external regression selection: 967 passed in 33.44 seconds,
  warnings as errors, no skips. This is the preceding 950-test selection
  plus the 17 new recursive-source tests. It is not the main repo suite.
- Both new Python files passed py_compile.
- All 43 recorded source/document hashes and four frozen receipt hashes
  matched after the successful rebuild. Prior files/receipts are unchanged.
- The correlated-source falsifier covers both an entangled bank and a
  separable bank with shared classical phase records. Local marginals agree
  exactly, but the controlled-discard output has trace distance 1/2 from
  the independent-input output. This tests an invalid assumption, not a
  prospective quantum speedup.

Receipt SHA256:

    a35fa15c5516a8654e8f3c26314c4a485595a241b0d3686649961d8ef47b20ac

Development compiler failures were resolved through explicit binder types,
finite quotient instances derived via the actual surjection, and dependent
state-family annotations. No desired-source premise, sorry, or warning
suppression was added. The final full verifier, not Python manifest tests,
performed the actual Lean kernel checks.

## Reproduce

From this directory:

```sh
/opt/anaconda3/bin/python verify_recursive_source.py --output recursive_source_receipt.json
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-recursive-source-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_recursive_source.py test_quotient_verifier.py test_cancellation_verifier.py test_group_bridge_verifier.py test_verify.py test_central_controls.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-recursive-source-pycache /opt/anaconda3/bin/python -m py_compile verify_recursive_source.py test_recursive_source.py
```

The broad selection is the exact selection documented in
QUOTIENT_VERIFICATION.md, with
rees-formal-core-2026-10-24/test_recursive_source.py prepended, run from the
parent qsearch-research-work directory with the same environment/pytest flags.

## Scope And State

Every actual adjacent stage, every retained record branch and the recursive
averaged source identity are checked. Fresh leaf count is the product of
packet arities. Complete characters and nonzero diagonal witnesses remain
explicit imported plan data; the starting source is supplied. No native
source acquisition circuit, final Fourier receiver, efficient extracted
program, new independent review, hardness result or novelty certification.

The main Developer checkout is still absent. Main Desktop/staging files,
registry, CLI, UI and Git were untouched. Main-repository tests, qsearch
validate, Node syntax checks, commit and push were not run on the moving
source. All owned compiler/test sessions completed; no job remains running.
