# Verification: 2026-10-26

Workdir: `/Users/jaspersands/Developer/qsearch-research-work`.
Python: `/opt/anaconda3/bin/python` 3.13.5; python-flint0.9.0.
No independent review or proof-assistant check was completed this pass.

## Observed Results

All pytest commands used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-pycache`, `-p no:cacheprovider`
and `-W error`.

1. Final focused `test_affine_sampling.py`: **29 passed in0.14s**, no skips.
2. Seven-suite regression: **235 passed in4.15s**, no skips or warnings.
   Files: new affine suite, USD test_usd_reduction.py, Schur test_schur_gate.py,
   inverse-trace test_local_list.py, test_modular_norm.py, test_norm_transfer.py
   and test_residual_sat.py in their existing dated bundles.
3. `python -m py_compile` on affine_sampling.py, curve_countercontrol.py,
   test_affine_sampling.py and verify_affine.py: exit0.
4. `python ag-affine-sampling-2026-10-26/verify_affine.py --write` then
   `--check`: original-input replay PASS, nine source/dependency hashes.
   Receipt SHA256:
   `960726d49e2faaac7a8d427a370b04d4f90337262694c98cd6fa641062b742ce`.
5. Prior USD six-hash and Schur eight-hash replays PASS unchanged, retaining
   receipts `e6435c5275c7db6d593e5af002a82bf1e7f6e758beea3309af5dd30770949eeb`
   and `778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64`.

## Scope Of Checks

- All729 elements of each of three small affine fibers, full-support counts
  42/43/43, and all21 five-coordinate marginal sets. Every marginal is uniform.
- Exhaustive two-trial ideal-coin control: each of the two valid words has
  four equally likely coin transcripts, and one transcript fails. The cap
  preserves conditional uniformity, not merely feasibility.
- Original-matrix solve with noninitial pivot columns and all25 kernel
  coefficient choices; canonical input and field checks.
- An actual smooth genus3 F13 curve with19 fixed evaluation points. Computed
  Schur square/cube dimensions12/19 and exactly zero cube-annihilator dimension.
- 38 test targets plus eight receipt targets return verified original-relation
  witnesses. Counts overlap; this is not an all-syndrome empirical sweep.
  The all-syndrome probability statement comes from the written distance and
  Bonferroni proofs, not the finite replay count.
- Exact lower probability30126834384/137858491849, expected trials at most
  4.575937, and exact inequality for failure below10^-12 after128 ideal trials.
- Exact analytic Taylor-remainder/half-product comparisons at lengths100,
  200 and1000. These are analytic checks, not asserted curve constructions.
- A false-independence countercontrol has an impossible forced-zero target
  despite a positive formal bound. The helper does not certify its own premise.
- A fixed-field high-zero-count case gets no positive short-moment certificate;
  this is not converted into hardness. Finite caps return UNKNOWN.

## Files And Limitations

Created affine_sampling.py, curve_countercontrol.py, test_affine_sampling.py,
verify_affine.py, AFFINE_SAMPLING.md, HANDOFF.md, receipt.json and this note.
Updated the isolated top-level research checkpoint. Earlier results unchanged.

Main local checkout remains absent; isolated workspace is not Git. No main
application CLI/UI/registry changes, full-repository tests, qsearch validate,
JavaScript checks, commit or push were performed. No quantum execution,
Shor-level result, native inverse-trace solution or universal AG dequantization
is claimed. The USD independent-review permission request remains pending
at this checkpoint; no reviewer was launched.
