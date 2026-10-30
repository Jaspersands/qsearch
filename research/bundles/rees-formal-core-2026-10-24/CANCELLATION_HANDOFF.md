# Mechanical Handoff: Constructed Cancellation

All changes live in this external bundle, outside the migrating checkout.
Do not integrate into the main repository until its local copy is verified.
Do not change the previous five Lean modules, frozen receipts or mathlib.

Run from this directory:

```sh
PYTHONPYCACHEPREFIX=/tmp/qsearch-cancellation-pycache /opt/anaconda3/bin/python verify_cancellation.py --output cancellation_receipt.json
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_cancellation_verifier.py test_group_bridge_verifier.py test_verify.py test_central_controls.py
/opt/anaconda3/bin/python -m py_compile verify_cancellation.py test_cancellation_verifier.py
```

The first command actually rebuilds six proof modules and audits all 153
explicit declarations. The Python tests only exercise verifier guards and
existing finite physical controls. A green Python test is not a Lean proof.

Keep the scope: 104 total theorem declarations, but only the first central
Rees channel is constructed. Base BCH law, complete Fourier characters and
the nonzero diagonal witness finder remain explicit dependencies. No quantum
circuit, full descent, arithmetic runtime or novelty is certified.

After migration, integration should preserve source hashes and these scope
flags, not translate them into an accepted speedup claim. Expose the proof
receipt only as a checked conditional reduction. Registry/CLI/UI changes and
mechanical replay are suitable Gemini tasks; quotient/source composition is
a mathematical task, not a request to auto-fill assumptions.
