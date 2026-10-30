# Verification: 2026-10-24

## Executed

- `/opt/anaconda3/bin/python -W error -m pytest -q test_native_sketch.py`:
  **63 passed in 0.47s**, no skips, warnings treated as errors.
- `/opt/anaconda3/bin/python -m py_compile native_sketch.py test_native_sketch.py replay.py`:
  PASS for all three files.
- `replay.py --output receipt.json`: completed, followed by a separate
  fresh `build_receipt()` and parsed JSON equality comparison: PASS.
- All five bundle source/document SHA256 values in the receipt: rechecked,
  all match. Main source-authority hashes and primary PDF hash were read
  directly before receipt generation and retained in the receipt.
- Non-admission and scope guards: PASS. No gates executed, no accepted
  speedup, no all-native-algorithm lower bound, no source-paper refutation.

Receipt SHA256:

    637f435424e57a94a39002c0a939a67988abd489a2cef2fbeef4895a45bee131

## What These Checks Establish

Exact cyclotomic quarter-turn evolution agrees with an independently
implemented dense numerical readout. Noiseless support saturation, frozen
replay, noisy arbitrary-angle support bounds, composite-root character
orthogonality, exact compressed-harmonic cancellation and surviving higher
harmonics, classical recovery on a labeled balanced-noise fixture, and
invalid-input/control caps all pass.

The actual averaged conjugation channel is used in the IID controls, not
conjugation by the expected unitary. At q=3, n=1, visibility 1/2, M=48/192,
trace distances to the ideal are approximately 0.391814/0.123953, below
the analytic half-diamond bounds 0.668254/0.167064. These floating-point
diagnostics are not proof certificates or quantum hardware executions.

The large cost ledgers enumerate no addresses: for n=8/16/32 and q=3^(2n),
the address counts have 203/812/3247 bits. At favorable visibility one,
the conservative classical sample budgets are 9248/33824/132128; the local
sketch cost still scales with the full address count. These are symbolic
resource controls, not hard source executions or asymptotic measurements.

## What Was Not Done

No full repository test suite, `qsearch.py validate`, Node/UI check,
registry mutation, Git operation, quantum execution, independent review,
or formal theorem-prover check was performed. The theory proof is local
and self-reviewed. The intended local checkout was still absent, so all
writes are in this independent external bundle and its parent checkpoint.
No existing source/staging files, other agent's work, or migration state
were changed. All owned test and replay processes completed.

The negative result rules out the literal local-sketch/Fourier recovery
proposal at polynomial native cost. It does not rule out a different
native receiver, prove LWE hardness, or challenge the paper's stated
space advantages. The Rees review authorization was not reused.
