# Review And Integration Handoff

Work remains isolated while the Desktop repository migration is active.

## Research Decisions

- Independently audit the root perturbation, uniform column bound, and
  rounding/correction proof in GENERAL_SMOOTH_SOS.md. A passing certificate
  test does not prove the uniform theorem.
- Compare the constructive statement with prior sums-of-squares algorithms
  over orders. Do not treat the proposed result as novel without review.
- Retain the eight-copy surface construction. This generic extension is
  astronomically larger and should not replace it.
- Do not start a higher-dimensional geometric backend merely because the
  algebraic identity passes. The receiver and practical relevance remain
  unresolved. First identify an actual new algorithmic problem it unlocks.

## Gemini Tasks After Migration

- Integrate the weighted certificate checker and exact tests under a unique
  module name, preserving the existing registry schema.
- Record CONDITIONAL_ALGEBRAIC_SOURCE_EXTENSION and link the preceding
  source/field-stability notes. Do not record a discovered quantum algorithm.
- Report the number of weights, padded square count, stabilization dimension,
  denominator bit length and largest auxiliary prime. Do not collapse these
  into a single "polynomial" status.
- Keep four-square expansion explicitly unexecuted until a justified
  arithmetic implementation is wired and verified.
- Wire only into existing proof artifacts. No new UI or experiment search
  loop is needed for this lemma.
- Run full repository tests and qsearch.py validate only after the destination
  checkout is verified complete and stable.

## Replay

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      /opt/anaconda3/bin/python replay_smooth_sos.py
