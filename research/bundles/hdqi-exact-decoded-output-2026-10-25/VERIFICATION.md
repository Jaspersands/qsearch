# Verification

2026-10-25. All listed commands completed. No owned research process remains.
No independent mathematical reviewer, commit, push or automation was used.

## Tests And Syntax

Focused command from this directory:

```sh
/opt/anaconda3/bin/python -m pytest -q -W error
```

49 tests PASS in 1.33 seconds after correcting the two issues below.

Combined command from /Users/jaspersands/Developer/qsearch-research-work:

```sh
/opt/anaconda3/bin/python -m pytest -q -W error hdqi-hidden-mode-access-2026-10-25 hdqi-transfer-word-sampler-2026-10-25 hdqi-rational-transfer-2026-10-25 hdqi-ecf-tree-sampler-2026-10-25 hdqi-decoded-observables-2026-10-24 hdqi-output-sampling-2026-10-24 hdqi-exact-decoded-output-2026-10-25
```

294 tests PASS in 13.03 seconds, with warnings treated as errors. This is
seven related isolated bundles, NOT the full main repository.

All five new Python files pass py_compile: transfer_access.py,
decoded_transfer.py, decoded_controls.py, test_decoded_transfer.py, replay.py.

## Live Exact Replay

```sh
/opt/anaconda3/bin/python replay.py write
/opt/anaconda3/bin/python replay.py check
```

Both PASS, including deterministic source/context hashes and all exact data.
Receipt SHA256:

    8df019469688eac110b057a7ea20632d3c1185318243f188e5791cb357d911b6

The receipt hashes six new source/test/proof files and six direct context
files. This note and HANDOFF.md are intentionally outside the hash set.
The frozen preceding ECF receipt is unchanged:

    6cbb7188ed53314322643acac2bc2fc7347365f132098252d031bb18f72174b5

The older signed physical-output receipt remains:

    db1a6cf12c67bb68ee7a4b6b2c8a375b2614c1433fdfe87af2733d5eec9fdae8

### Exact Controls

Four controls verify EVERY actual physical-output event against direct
Pauli actions, not the production ordered-phase routine. One-trial success
is exactly 1/2, 1/2, 1/4, 1/2 respectively, agreeing with 2^-k. They cover
Y phases, redundant generators, bad decoders and a complex-phase countercase.
Three physical observables per case have exact matching importance means
and second moment <=1.

The imaginary-phase countercase has expectation
1184047661160/494569255353923 for observable (x,z,p)=(2,3,1). Discarding the
imaginary partner phase loses this nonzero result. This does NOT identify
a bug in the frozen real-sign estimator: it identifies why its real-only
phase helper cannot be reused for arbitrary complex transfer pilots.

The tests also cover all amplitudes, huge rare weights (10^80), explicit
abort behavior, source mismatch, inexact inputs, work-budget refusal,
zero-amplitude rows, and high-rank sampling refusal with Pauli estimation
still available. The high-rank commuting control is NOT a hard instance.

### Live Physical Output

24 physical qubits, 25 native generators, two complex-rational transfer
factors, interference rank k=1. Four actual output samples completed in
2,1,1,1 trials respectively, using 10 amplitude evaluations and 15 decoder
calls across the successful/rejected attempts. No dense physical state or
native amplitude table was used. The transfer ledger records 26,001 pair
states per contraction and 729 single-copy amplitude states across 21 bags.

Four Pauli draws on this larger input are DIAGNOSTIC ONLY, not an accurate
estimate. A separate one-generator implementation control executes the
complete 2,112-draw median-of-means plan with epsilon=1/4, delta=1/16. Its
estimate -7/12 differs from exact -3/5 by 1/60. The proof of the guarantee,
not this seed's outcome, requires independent random bits; the seeded PRNG
is used only for reproducibility. None of these controls is a new candidate.

## Corrected During This Pass

The first focused run had 47 passes and two failures:

1. A test compared SymPy's Gaussian zero directly with Python integer zero;
   its equality convention differs. The test now uses the domain's boolean
   zero check, as production code already did.
2. The inherited rational parser accepted floating failure probabilities.
   The new sampler/estimator now use the strict exact int/Fraction parser,
   and the rejection test passes. No predecessor source was edited.

All final tests, syntax checks, and replay write/check ran AFTER these fixes.

## Scope Still Open

The general ECF thermal composition is a local, unreviewed argument inherited
from the preceding bundles. Certified thermal roots and full thermal
execution remain absent. The actual decoder output is not asserted to be
the physical Gibbs state. General high-interference-rank full sampling,
arbitrary extra quantum operations, polynomial dequantization, novelty and
quantum advantage are not established.

The Developer main checkout was still absent when this pass began. Main,
staging, CLI/UI, registry, Git and migration state were untouched. Main
tests/qsearch validate/node --check were NOT run or claimed; this external
proof pass changes no JavaScript and integrates no main source files.
