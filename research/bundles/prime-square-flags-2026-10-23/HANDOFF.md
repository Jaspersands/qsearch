# Integration Handoff

Do not edit the moving Desktop source or migration staging checkout.
Integrate only after the destination has been verified complete and stable.

## Research Review First

1. Review W=(rG)^perp and the residual-pairing calculation independently.
2. Verify that the source's common field actually defines the full supplied
   source-order basis AND phi. Geometric existence is insufficient.
3. Check that the chosen A26 implementation preserves the subgroup's
   definition field, rather than silently accumulating torsion fields.
4. Keep the direct r^2 quotient fallback for inputs lacking scalar Frobenius.
5. Preserve the existing unproved classical-hardness, source-implementation,
   quantum-receiver and novelty obligations. Do not label this a speedup.

## Gemini Wiring After Migration

- Integrate prime_square_flags.py under a unique theorem/module name and
  adapt its tests to the existing smooth-repolarization implementation.
- Record computed Smith type, both kernel orders and both pairing checks.
- Add a source-field obligation: full source order and phi over paid k.
  A user-supplied boolean is not evidence that this obligation is proved.
- Associate the note with the existing smooth-repolarization proof node.
  Record CONDITIONAL_SOURCE_REFINEMENT, not accepted quantum algorithm.
- Replace the direct list cost by two prime lists only when the stable-flag
  obligation is discharged. Report list cost separately from total cost.
- Expose the receipt through existing research artifacts, not a new UI.
- Run the repository tests, syntax checks, node --check index.js and
  python qsearch.py validate after integration in the stable checkout.

## Local Replay

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      /opt/anaconda3/bin/python replay_prime_square_flags.py

The replay writes prime_square_flags_receipt.json with source hashes.
No geometric backend, secret-kernel recovery or quantum circuit is run.
