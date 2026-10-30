# Verification

2026-10-23, isolated local bundle. No moving source/staging files changed.

- New suite: 27 passed in 32.28 seconds, with pytest plugin autoload and
  cacheprovider disabled and bytecode redirected outside the checkout.
- Direct smooth-repolarization dependency: 56 passed in 0.40 seconds.
- Kernel-output and uniform-source-bound bundle: 47 passed in 7.40 seconds.
- Total rerun at this milestone: 130 passing tests, in separate processes.
- Python syntax checks passed for all three Python files in this bundle.
- Replay passed three dimension-16 controls with five checks each, plus
  two negative controls. All six recorded source SHA-256 hashes matched.
- One initial assertion incorrectly expected a free rank of 16 at r=5.
  The exact Smith decomposition gives 8; the test was corrected and the
  mixed-kernel case now also checks the residual quotient pairing.

No geometric quotient or quantum algorithm ran. These are exact algebraic
controls, not experimental evidence of an asymptotic speedup. Full repository
tests, UI syntax checks and qsearch.py validate were not rerun against the
moving repository. Earlier unrelated isolated bundles were not rerun in
this milestone. No Git commit or push was made.
