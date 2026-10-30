# Integration Handoff

## Result To Preserve

This is a scoped negative result about applying the existing Rees receiver
to the actual cyclotomic coset input of arXiv:2609.34996v1. It is NOT a
negative result for that published algorithm, a refutation of the existing
fixed-class Rees proof, or evidence of native hardness.

New exact controls: ramified ring/character arithmetic, parameter-scope
gate, filtered Fermat null polynomial, Newton-basis dilation and its
nontrivial unipotent action, secret-digit loss under mod-p reduction, and
the secret-dependent normalizer formula. No native solver is implemented.

Read CYCLOTOMIC_BRIDGE.md before importing any result. The non-diagonal
matrix obstruction has a general proof for every p and t>=2; changing
basis alone does not solve it. A new receiver must handle the full action and pay the
full sample tree, not just a per-layer cost.

## Files And Verification

- bridge_controls.py: FLINT-backed exact arithmetic, with explicit caps on
  exhaustive ring/fidelity controls. Enumeration is not the algorithm.
- test_bridge_controls.py: regressions and algebraic counterexamples.
- replay.py: deterministic receipt generation, hashes and source flags.
- receipt.json / VERIFICATION.md: executed scope and reproducibility.
- CYCLOTOMIC_BRIDGE.md: general arguments and scope restrictions.

Use `/opt/anaconda3/bin/python`, with python-flint and pytest. Commands:

    python -B -W error -m pytest -q -p no:cacheprovider test_bridge_controls.py
    python -B replay.py --output receipt.json

The isolated bundle is intentional: the Desktop checkout is cloud-backed
and dirty, and the verified Developer destination was absent during this
pass. Do not edit a moving source or staging copy. After migration is
verified, Gemini can integrate a literature link and scoped negative
record into the EXISTING schemas, then run full repository validation.
Do not add a replacement CLI, registry schema, dashboard or search engine.

Do not overwrite the earlier Rees proof, reviewer files or frozen receipts.
No automatic candidate promotion, proof-complete status, cryptanalytic
claim or new independent-review label is justified. This pass has not been
committed or pushed.
