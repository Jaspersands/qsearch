# Terminal Receiver Integration Handoff

2026-10-25. Changes are confined to the external research directory.
The intended Developer checkout remained absent at the start of this pass.
Do not modify the incomplete Desktop checkout or migration staging to wire
this in. All older proofs and frozen receipts remain unchanged.

After the authoritative local checkout is verified, Gemini may integrate:

- ReesTerminalRecovery.lean and AuditTerminalRecovery.lean.
- verify_terminal_recovery.py, terminal_controls.py and test_terminal_recovery.py.
- REES_TERMINAL_SCOPE.md, this handoff and the terminal receipt/verification.

Attach this to the EXISTING Rees candidate as conditional proof evidence.
Resolve only the exact native-to-terminal measurement and span-to-answer
obligations. Do not mark the full theorem formally verified, independently
reviewed, novel, practical or a quantum speedup. Do not create a new candidate
from the finite controls. Preserve old receipt hashes and explicit remaining
BCH, SDE, gate/runtime, independent-source and application obligations.

Reproduction, from this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /opt/anaconda3/bin/python -B verify_terminal_recovery.py --output terminal_receipt.json
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_terminal_recovery.py
```

The verifier rebuilds all earlier modules and compares their live report
with native_source_receipt.json before checking the new module. It rejects
compiler warnings, missing declarations, extra axiom dependencies and a
changed audit. Actual verification results belong in TERMINAL_VERIFICATION.md.

Run normal repository validation only after safe integration. No CLI/UI
redesign, general framework, more toy examples or frequent commits are
requested. This pass does not execute the quantum receiver or SDE solver.
