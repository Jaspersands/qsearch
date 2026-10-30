# Mechanical Handoff: Quotient Chain

Keep all files in the external research workspace until the main local
checkout is verified. Do not edit frozen modules or receipts to make replay
pass. No additional independent reviewer is authorized by this handoff.

```sh
PYTHONPYCACHEPREFIX=/tmp/qsearch-quotient-pycache /opt/anaconda3/bin/python verify_quotients.py --output quotient_receipt.json
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_quotient_verifier.py test_cancellation_verifier.py test_group_bridge_verifier.py test_verify.py test_central_controls.py
/opt/anaconda3/bin/python -m py_compile verify_quotients.py test_quotient_verifier.py
```

The verifier rebuilds seven modules and audits217 explicit declarations,
including142 theorem declarations. Python manifest tests are not kernel
proof checks. Retain the false full-algorithm, quantum-execution and novelty
flags. The base BCH law and quantum composition must not be auto-filled.

Suitable later Gemini work: integrate the exact checked source/receipt after
migration, expose it as a conditional algebraic reduction, and replay existing
tests. Do not restore circuit search or generate a new synthetic HSP campaign.

Next reasoning task: instantiate the physical central instrument on each
actual stage kernel with its additive coordinates and public section. Check
the output is precisely the next stage's coset source, with classical
records handled, before claiming recursive quantum composition. The present
module constructs the group chain but does not already prove that composition.
