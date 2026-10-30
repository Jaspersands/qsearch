# Verification And Exact Scope

Completed 2026-10-25 in the isolated local research workspace.

## What Was Established

MIXED_AVERAGE.md gives a written conditional deduction: a weighted
one-register partial-trace channel decodes the spectral-wedge packet to
the normalized rounded density, covariantly under the native action.
Contractivity transfers subgroup-average robustness, removing the previous
pointwise displacement promise from the low-rank mixed source for class<=3,
p>=131. This composition is not independently reviewed or Lean-verified.

The finite controls check identities and falsifiers, not that uniform theorem
or a speedup. No spectral acquisition, quantum learner or receiver was run.

## Checks Completed

- 24 new tests PASS in 0.74s, warnings as errors, no skips.
- Combined source dependency suite: 155 tests PASS in 1.12s, no skips.
  Files: new test_mixed_average.py; the coarse-spectrum, code-support and
  spectral-mixture suites; and both dilation-average/source-independence suites.
- py_compile PASS for mixed_average.py, test_mixed_average.py, replay.py,
  using /tmp/qsearch-mixed-average-pycache, not the moving checkout.
- replay.py --write and --check PASS. The receipt pins five local source/
  proof/handoff files and six directly reused dependency source/proof files.
  This note and the checkpoint are deliberately outside that manifest.
- The controls include normalization and covariance on arbitrary entangled
  inputs, degenerate bins, discarded tiny weights, false-promise failure,
  whole-support information loss, and changing grids within a moment packet.
- Two increasing-prime mixed-state controls check the analytic distinction:
  subgroup-twirl distance 1/4 versus minimum pointwise sin(pi/p)/2. Both
  are classically easy calibration, not algorithm candidates.
- Exact integer/rational ledgers recompute all acquisition/growth/QPE/action
  caps and charge fresh-scale rejection. Total allocated error is 29epsilon/32.
  Total gate cost is explicitly uncertified; no copy/query-to-gate conversion.

The full combined test command, from the isolated workspace root, was:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error rees-mixed-average-2026-10-25/test_mixed_average.py rees-coarse-spectrum-2026-10-24/test_coarse_spectrum.py rees-code-support-2026-10-24/test_code_support.py rees-spectral-mixture-2026-10-24/test_spectral_mixture.py rees-dilation-average-2026-10-25/test_dilation_average.py rees-dilation-average-2026-10-25/test_source_independence_control.py
```

The existing pure-source independent review was reused only within its scope.
No reviewer was launched for this composition. A targeted primary-paper scope
comparison is in the proof note; it is not an exhaustive novelty review.

## Files And Operational Boundary

Created this seven-file bundle: proof, reference/ledger module, tests, replay,
receipt, handoff and this verification note. Updated the shared isolated
RESEARCH_CHECKPOINT_2026-10-23.md with the result and its limitations.
Previous dependency proofs, code and receipts were not modified.

Live filesystem check: /Users/jaspersands/Developer/quantum algorithm search
still absent. No main/staging, CLI, UI, central registry, Git or migration
changes. No commit or push. Main pytest, node --check and qsearch validate
were NOT run; the checks above cover only this source dependency chain.
All test/check processes finished. No quantum or background search remains
running from this pass. The overall research goal remains ACTIVE.

Still missing: useful native application, matched classical benefit, specialist
novelty review, independent scrutiny of the full assembled source, and an
implemented receiver with complete physical gate costs. This result closes
one assumption-transfer gap, not those scientific obligations.
