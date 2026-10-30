# Verification: Low-Rank Mixed-Conjugation Source

2026-10-24. Conditional local mathematical construction, not independent
review, formal verification, quantum execution, novelty, or a speedup claim.

## Executed Checks

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -W error -m pytest -q -p no:cacheprovider rees-coarse-spectrum-2026-10-24/test_coarse_spectrum.py rees-code-support-2026-10-24/test_code_support.py rees-spectral-mixture-2026-10-24/test_spectral_mixture.py
```

Result: **77 passed in 0.24s**, warnings treated as errors, no skips.
This includes 30 new tests and 47 predecessor tests. Syntax compilation of
`coarse_spectrum.py`, `test_coarse_spectrum.py`, and `run_audit.py` passed.

Replayed `run_audit.py --output receipt.json`. A second independently
generated in-memory receipt equaled the saved parsed JSON. All five local
source/document hashes and six dependency hashes matched. Separately,
all 16 source/dependency hashes recorded by the two predecessor receipts
matched, using each receipt's original path base. An initial wrong receipt
filename was corrected before this verification and has a regression test.

Final receipt SHA256:

`f973c633df9cb7efc081714c25333e8f418bf00903955d4a25630ca707b5974c`

## What The Controls Establish

- Exact rational rounding, finite offset counting, error budgets, and
  resource caps agree with the stated proof. Supplied spectra are reference
  controls, not source access granted to a quantum algorithm.
- A seven-dimensional fixture has weight `2^-300` and splitting below
  `2^-200`, while retaining its promised orbit gap. Separate spectral-bin
  wedges preserve its full subgroup; a whole-support wedge does not.
- A Heisenberg-group fixture preserves the actual nonnormal subgroup of
  order 3, not merely its trivial normal core. It is classically easy.
- Non-diagonal order-three actions satisfy the projector/determinant gap
  inequalities in a floating-point check. This is not their proof.
- Literal corrected nonflat growth maintains the antisymmetric sector
  through three failure histories at each of two stages. Leakage is below
  `1e-12`; the final wedge trace error is below `1e-12`. Growth beyond the
  true rank has zero success in this finite reference calculation.
- A false global-gap promise produces a wrong enlarged subgroup. Internal
  degenerate rotations defeat chosen-eigenray methods. Fine spectral
  measurement dephases within a coarse bin: the source proof relies on
  fresh density-matrix targets, not an arbitrary-input coarse-projector
  diamond guarantee. These countercontrols remain active.

## Explicit Limits

The illustrative planner uses 101 QPE bits and gives a raw-copy cap with
101 decimal digits. Its counts are deliberately loose polynomial bounds,
not practical resource estimates or executed experiments. Exact IID copies,
a supplied polynomial rank bound, a global orbit gap, and the existing
controlled fixed-class Rees model remain assumptions. Unknown-rank
antisymmetrization and its nonflat growth bound are published prior art.

No central registry, CLI/UI, Git, main/staging checkout, or migration files
were changed. The intended Developer checkout was checked and is absent.
No repository-wide suite, `qsearch.py validate`, `node --check`, new Lean
check, quantum circuit execution, or additional independent review ran.
The existing authorized Rees review is not a review of this new source.

Seven files in this external bundle and the parent research checkpoint
record this pass. All owned test and replay processes finished.
