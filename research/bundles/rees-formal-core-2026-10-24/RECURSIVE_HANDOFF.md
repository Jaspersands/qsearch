# Bounded Integration Handoff

The high-reasoning result is in REES_RECURSIVE_SCOPE.md. Do not promote it
to a speedup claim or change the frozen older receipts to match new code.

After the main repository migration is verified, Gemini may:

1. Add these two Lean modules and their scoped verifier/tests to the
   existing formal bundle. Preserve every prior source/receipt hash.
2. Register the new recursive-source receipt as conditional proof evidence
   linked to the existing Rees candidate. Mark only the stage-composition
   obligation resolved under its listed premises.
3. Keep native source acquisition, diagonal solver, complete character
   implementation, final Fourier recovery, gate/error accounting, novelty
   and useful classical-hard application as unresolved obligations.
4. Run the normal main-repository validation and syntax/test workflow after
   integration. Report exactly what ran; this external pass is not a full
   main-checkout test run.

Do not change CLI/UI architecture, run larger opaque-label demonstrations,
infer independent targets from correct marginals, memoize identical quantum
source leaves, restore legacy circuit search, or commit every small edit.

Local verification:

```sh
/opt/anaconda3/bin/python verify_recursive_source.py --output recursive_source_receipt.json
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_recursive_source.py
```

The verifier rebuilds all prior modules and compares their reports with the
frozen quotient receipt before checking the new modules. The receipt lists
source hashes and explicit limitations; test counts alone are not evidence
of an end-to-end algorithm.
