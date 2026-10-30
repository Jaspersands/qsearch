# Handoff: Classical Sampling Gate

Read AFFINE_SAMPLING.md. This pass removes low-gonality/high-alphabet AG
families as advantage evidence for the current full-support construction,
including an actual curve with a nonvacuous refined quantum bound and zero
cubic-annihilator kernel. It does NOT refute the USD transfer lemma or
solve every remaining AG family. No inverse-trace status changes.

The intended main checkout is still unavailable. This is isolated research,
not an integrated CLI/registry update. Preserve the moving original/staging
tree. No commit/push was made.

## Gemini Integration Once A Verified Checkout Exists

1. Add uniform affine-fiber rejection sampling as a matched full-support
   classical baseline. Preserve original B,s and exact witness checking.
2. Attach the Bonferroni bound only when dual distance/t-wise independence
   is independently justified. The helper explicitly does not verify it.
3. Record the genus3 F13 countercontrol as a negative result, not a failed
   quantum algorithm. Both quantum and classical sufficient bounds hold.
4. Preserve exact-conditional-uniform sampling scope, ideal coin assumptions,
   finite cap, field draws and UNKNOWN statuses. A seeded replay is not a
   distributional test. Do not reuse the older norm solver's biased-output
   metadata for this different sampler.
5. Run focused tests/replays, then full main tests, syntax and qsearch validate
   after integration. No UI polish or generic search framework is needed.

## High-Reasoning Work

The remaining candidate question needs an actual high-gonality family over
an appropriate prime field, not parameter arithmetic alone. Compare strong
auxiliary-code attacks before implementation. A request for ONE independent
reviewer of the preceding USD lemma was sent during this pass; at the time
this handoff was written no reply had arrived. Do not launch a reviewer or
duplicate the request without checking that authorization.

Replay from `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error ag-affine-sampling-2026-10-26/test_affine_sampling.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-pycache /opt/anaconda3/bin/python ag-affine-sampling-2026-10-26/verify_affine.py --check
```
