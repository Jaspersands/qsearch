# Verification

2026-10-25, isolated bundle, Python 3.13.5 and python-flint 0.9.0.

- Final `python -m pytest -q -W error test_exterior_sde.py`: 56 passed
  in 8.74 seconds, no skips or warnings.
- Preserved predecessor `test_quadratic_cancellation.py`: 99 passed in
  0.62 seconds. That backend was not edited or replaced.
- `python -m py_compile exterior_sde.py test_exterior_sde.py replay.py`:
  passed after final Python edits.
- `python replay.py --write` and `python replay.py --check`: identical
  receipt SHA256
  8e2f31784c0642fbac6a9370b43ba130533f6daecd379730da0a4bf7de9bec55.
  Five source files and three predecessor context notes are hashed.

## Checked Scope

Exact original moments at twelve parameter settings, including genuine
power indices four and five, two 127/128-bit primes, and original degrees
different from the reduced index. A separate FLINT matrix multiplication
checks the same original equations. Contraction-kernel dimensions and
projection injectivity cover all exterior levels for indices two through
six. Additional repeated-column collision controls use eight seeds.

Both even-degree accumulation paths are forced through every round:

| Prime | Degree | Width | Full acquired bank | Exterior nodes | Field enumeration |
|---|---:|---:|---:|---:|---:|
| 13 | 4 | 1 | 262144 | 178923 | 13 elements |
| 2^128-275 | 4 | 1 | 4096 | 2795 | none |

These deliberately simple all-one fixtures test recursive accounting, not
hardness or efficient scalar solving. Nine live receipt cases include
random public matrices, full recursion, and zero labels with a charged
suffix. Every receipt residual is exactly zero and every witness nonzero.
Positive finite replay does not establish the stated randomized failure
bound; that bound requires independent uniform draws and the written
number-theoretic argument.

Negative controls reject wrong even-degree sign handling, bad roots,
all-zero/overlong scalar rows, forged plans, insufficient banks, invalid
field/degree/width inputs, and out-of-range random values. Exhausted
generator and Fermat sampling caps abort without full-field fallback.

During development the extra independent matrix test initially called an
unsupported FLINT `is_zero` method. It was corrected to inspect all exact
residual entries; the final suite above passed. The initial standalone
41-test run passed before this test extension. No failing final test is
hidden by the final counts.

## Not Established

The general exterior proof is a local written deduction, not an independent
review or a proof-assistant result. Novelty, best-known complexity, quantum
implementation, end-to-end resource bounds, native reductions and speedup
remain unclaimed. Root/primality/RNG timing is not certified by loop caps.

The main Desktop checkout remains migration-sensitive, and the intended
local repository destination was absent when rechecked. No main/staging,
CLI/UI/registry, Git or migration changes were made. Main repository tests,
qsearch.py validate and UI syntax checks were not run. No commit/push or
additional reviewer was started. The broad research goal remains active.
