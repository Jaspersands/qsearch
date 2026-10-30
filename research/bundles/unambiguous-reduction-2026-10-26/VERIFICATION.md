# Verification: 2026-10-26

Workdir: `/Users/jaspersands/Developer/qsearch-research-work`.
Python: `/opt/anaconda3/bin/python` 3.13.5. No independent review or formal
proof-assistant verification was performed for the transfer refinement.

## Observed Commands

All pytest runs used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`PYTHONPYCACHEPREFIX=/tmp/qsearch-usd-pycache`, `-p no:cacheprovider`,
and `-W error`.

1. `test_usd_reduction.py`: **19 passed in 0.24s** at initial completion.
2. After adding the explicit Schur-relaxation consistency check, the six
   suites below passed **206 tests in 4.13s**, no skips or warnings:
   new USD suite, `schur-growth-classical-gate-2026-10-26/test_schur_gate.py`,
   `inverse-trace-local-list-2026-10-26/test_local_list.py`,
   `inverse-trace-modular-norm-2026-10-25/test_modular_norm.py`,
   `inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py` and
   `inverse-trace-residual-2026-10-23/test_residual_sat.py`.
3. `python -m py_compile` on usd_reduction.py, test_usd_reduction.py and
   verify_usd.py: exit0.
4. `python unambiguous-reduction-2026-10-26/verify_usd.py --write` then
   `--check`: signed replay passes, six hashes. Receipt SHA256:
   `e6435c5275c7db6d593e5af002a82bf1e7f6e758beea3309af5dd30770949eeb`.
5. The previous Schur-gate `--check` passes unchanged, eight hashes,
   receipt SHA256:
   `778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64`.

## What Was Checked

- Fixed signed F3 pair isometry and inverse, original target-syndrome Fourier
  phases and full-support verification, for all three syndromes at lengths
  1,2,3,4. At most81 statevector amplitudes; this is NOT quantum execution.
- Integer Gram numerators verify orthogonality of distinct successful labels.
- Exhaustive 3^2-variable checks verify that the repetition decoder agrees
  with uniqueness of the Schur relaxation on actual ensemble transcripts.
- Direct target fidelity agrees with p_bar/lambda_s within1e-12.
- Length4 syndrome1 has valid-output probability strictly above target
  fidelity, guarding against a false uniform-sampling interpretation.
- No accepted branch at length1; no division by zero or false empty-fiber
  guarantee. Invalid analytic inputs and enlarged dense controls are refused.
- Exact rational eight-state countercontrol: decoder success5/8, target
  fidelity1/10. Removing unambiguity invalidates the proposed guarantee.

Raw numerical values may exceed1 by floating-point roundoff below1e-12;
the receipt records exact predicted fidelities and rounds valid-output
probabilities to ten decimals after checking identities. No numerical
control is used as proof of an asymptotic family or hardness claim.

## Files And Limits

Created usd_reduction.py, test_usd_reduction.py, verify_usd.py,
USD_REDUCTION.md, HANDOFF.md, receipt.json and this verification note.
Updated only the isolated top-level research checkpoint. The preceding
classical bundle and its receipt remain unchanged.

Main checkout remains absent and this workspace is not Git. No application
CLI/UI/registry integration, full-repository tests, qsearch validate,
JavaScript checks, commit or push were performed. Independent review,
novelty review, an actual scalable family and stronger matched classical
attacks remain required. Neither this refinement nor its passing controls
establish a Shor-level algorithm or solve the native inverse-trace problem.
