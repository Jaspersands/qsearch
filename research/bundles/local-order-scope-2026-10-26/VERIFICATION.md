# Verification And Limits

2026-10-26. Workspace: /Users/jaspersands/Developer/qsearch-research-work.

## Changes

- SCOPE.md: matched classical baseline, precise existing-fixture
  classifications, non-Bass residual family, adversarial research decision.
- local_orders.py: exact supplied-frame local membership and known
  Eichler-path interval selection; explicit enumerative small-prime controls.
- test_local_orders.py: 24 controls, including reconstruction of both old
  fixtures, large-prime path selection, rational neighbor membership,
  UNKNOWN rejection, and execution-scope flags.
- replay_scope.py / receipt.json: reproducible controls and dependency hashes.
- eisentraeger-scullard-v2.html: retained versioned primary source.
- HANDOFF.md and this verification record.
- Root RESEARCH_CHECKPOINT_2026-10-23.md: current result and next question.

No old receipt, source proof, independent report, or test was edited.

## Executed

Initial focused controls: 23 PASS in 0.64s. After adding the scope-regression
test, standalone: 24 PASS in 0.66s. No failures or skips.

Ten-bundle regression: 279 PASS in 39.86s, warnings as errors, no skips:

    /opt/anaconda3/bin/python -W error -m pytest -q local-order-scope-2026-10-26 classical-symmetry-harvest-2026-10-26 additive-framed-source-2026-10-26 polarization-completion-probe-2026-10-25 native-suborder-preprocessing-2026-10-26 smooth-repolarization-2026-10-23 prime-square-flags-2026-10-23 source-field-audit-2026-10-23 elliptic-theta-input-2026-10-26 elliptic-field-normalization-2026-10-25

All three new Python files pass py_compile. Receipt --write --check and a
separate --check pass. The large-prime local control selects vertex 23 of
a length-31 path at q=2305843009213693951 using 20 membership calls; its
target frame is supplied, not discovered on a native curve.

Receipt SHA256:
d7b8b158fe7371ab352404e912e791c2cd3a54ff43dba4de59141cdb0c651f40

Unchanged old receipt/report hashes:

- Harvest: 0d68b2df50149d61fdec2fdfe6f71e3f71507a8df9faf4f2f7472efe1ae73272
- Additive: 57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9
- Review: 471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49

## Not Executed Or Established

No native geometric algorithm, endomorphism division, unknown-target
recovery, general dequantization, hardness, novelty, or quantum advantage.
No new reviewer was spawned: the latest reply referred to the already-used
combined-source review authorization, not the newer additive-source request.

This is a focused research regression, not all-repository validation.
The intended local main checkout remains absent at the live check. No
qsearch.py validate, node --check, main CLI/UI/registry edits, commit or push
was performed. No source/staging edits or active command sessions remain.
