# Integration Handoff

This isolated work must not be merged into the moving source/staging copy.

- Replace the rank-two random-transvection baseline as the primary upper
  bound with this equality-only O(sqrt(ell)) meet-in-the-middle algorithm.
- Preserve the actual source contract: Sp_4(F_ell), odd prime ell, LEFT
  stabilizer cosets, and exact labels. Do not wire a ring source by analogy.
- Pass only a real oracle callback to recover(); never pass hidden K or
  graph coefficients. The fixture oracle belongs only to proof controls.
- Charge calls, label width, stored table, arithmetic and source evaluation
  separately. The existing geometric source still has huge constants.
- The default eight public charts guarantee recovery under the oracle
  promise. A deliberately truncated chart_budget can return ABORT; that
  is neither dequantization nor a negative mathematical result.
- Keep quantum speedup claims blocked pending geometric implementation,
  independent review and stronger same-input classical attacks.
- After migration, integrate into existing dequantization/proof artifacts,
  run all repository tests, syntax checks and qsearch.py validate. No new
  candidate family, toy experiment registry or UI is needed.

Local commands:

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      /opt/anaconda3/bin/python replay_classical_siegel.py
