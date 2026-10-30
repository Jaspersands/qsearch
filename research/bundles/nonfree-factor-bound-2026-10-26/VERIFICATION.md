# Verification And Execution Boundary

2026-10-26. Isolated workspace:
/Users/jaspersands/Developer/qsearch-research-work.

## Changes

Added NONFREE_FACTOR_BOUND.md, nonfree_factor_bound.py,
test_nonfree_factor_bound.py, replay_nonfree_bound.py, receipt.json,
HANDOFF.md and this record. Updated the root research checkpoint only.
Previous proof/code/test/receipt files and independent review are unchanged.

The proof extends the small-diagonal competitor to all elliptic factors,
not just free original-E factors. It separately handles binary H-unitary
automorphisms, the integral elliptic-unit residual phase, and product powers
by unique polarized decomposition. The code checks supplied rank-one
projectors and binary automorphisms, not geometric objects or their origin.

## Checks

- Initial test setup incorrectly used a nonprincipal form in the legacy
  free-factor cross-check; the expected rejection exposed the fixture error.
  Replaced it with an explicitly verified principal form. No source fix or
  relaxed assumption was used to make that test pass.
- Intermediate new-plus-old suite: 32 PASS in1.74s; after the basis-change
  control, 33 PASS in1.82s.
- Expanded standalone automorphism suite: 14 PASS in0.50s.
- Five-bundle intermediate regression: 100 PASS in11.24s.
- FINAL fourteen-bundle regression: 350 PASS in51.24s, warnings as errors,
  no skips. Includes all 16 final new controls.
- All three final Python files pass py_compile.
- Final receipt --write --check and separate --check: PASS.

Final regression command:

    /opt/anaconda3/bin/python -W error -m pytest -q nonfree-factor-bound-2026-10-26 partial-quotient-symmetries-2026-10-26 interpolation-leakage-2026-10-26 native-nonbass-realization-2026-10-26 local-order-scope-2026-10-26 classical-symmetry-harvest-2026-10-26 additive-framed-source-2026-10-26 polarization-completion-probe-2026-10-25 native-suborder-preprocessing-2026-10-26 smooth-repolarization-2026-10-23 prime-square-flags-2026-10-23 source-field-audit-2026-10-23 elliptic-theta-input-2026-10-26 elliptic-field-normalization-2026-10-25

New receipt SHA256:
30ec92f99648a15388217d0b7a1f4b11da5b2586d85a046a281aefc7c47b86ca.

Preserved prior polarization-probe receipt:
46f63d034d745df6fb20e2fdfbdc27c9effc78fbdf44b4cb45d34e252272b194.
Preserved additive-source receipt:
57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9.
Preserved combined-source independent review:
471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49.

## What Was Not Verified

No new independent reviewer, native geometric decomposition, nonfree
geometric factor, native low-degree enumeration, unknown endomorphism or
quantum algorithm. The nonfree and product-power coverage is deductive;
the positive fixtures have a supplied free factor basis and known ambient
order. Passing tests do not establish novelty or a speedup.

The main local checkout remains absent at the live check. No migrating
source/staging files, main CLI/UI/registry, commit or push were changed.
This is focused research validation, not whole-repository validation.
All command sessions finished. Handoff names the cut direction and the
remaining high-height/nonbinary scope without promoting an untested family.
