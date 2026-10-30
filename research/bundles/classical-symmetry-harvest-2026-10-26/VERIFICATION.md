# Verification, 2026-10-26

Status: PROGRESS on a concrete matched classical attack and its failure
conditions. No complete dequantization, native EndRing algorithm, quantum
advantage or novelty is established.

## Changes

Added HARVEST.md, harvest.py, test_harvest.py, replay_harvest.py, receipt.json,
HANDOFF.md and this verification record. Updated the root research checkpoint.
No previous research implementation or receipt was changed. No main CLI,
registry, UI, source/staging or Git changes were made.

The implementation checks exact pullback/recovery identities, order
enlargement and closure, trace-coordinate extraction, prime-to-p scalar
shift selection, and an integral product factorization for the Pell family.
It does not implement the geometric operations in the native attack.

The math note supplies the coprime-index information equivalence, mandatory
2-saturation repair, conditional index-descent algorithm, basis-height and
map-compression accounting, and the complete zero-query symmetry-group
failure control. These new deductions have not been independently reviewed.

## Executed

Interpreter: /opt/anaconda3/bin/python.

- First targeted run: 5 failed, 14 passed. The failures reproduced a SymPy
  cached QQ-domain issue after integral quaternion multiplication. Fixed by
  reusing integer_matrix, which checks integrality BEFORE rebuilding an
  integer-domain matrix. No fractional values are rounded or truncated.
- After that repair: 19 passed in 0.87s.
- Final standalone controls: 21 passed in 1.26s.
- FINAL nine-bundle regression: 255 passed in 39.39s, warnings as errors,
  no skips. Includes this bundle, additive-framed-source,
  polarization-completion-probe, native-suborder-preprocessing,
  smooth-repolarization, prime-square-flags, source-field-audit,
  elliptic-theta-input and elliptic-field-normalization.
- All three Python files passed py_compile after final code edits.
- Replay --write --check passed; a separate --check passed identically.

Receipt SHA256:

    0d68b2df50149d61fdec2fdfe6f71e3f71507a8df9faf4f2f7472efe1ae73272

Earlier additive-source receipt SHA256, unchanged:

    57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9

Earlier independent review SHA256, unchanged:

    471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49

The recorded easy-unit control enlarges index 9 -> 3 -> 1 when Q=4, but
not when Q=9. This verifies a conversion condition, not a difficult native
algorithm. Pell controls cover (n,k)=(3,2),(17,12),(99,70),(577,408).
The complete-group index-17 control is checked in tests through generators
of the proven monomial automorphism group, not a sampled subset.

## Not Run

Native PPAV automorphism enumeration, native pullback maps, actual
2-saturation, native interpolation/compression, unknown order recovery and
any quantum source/receiver. No probability theorem for useful nonzero
queries was proved. No independent reviewer was launched in this pass.
The main repository's full tests, qsearch validation and Node checks were
not run or claimed in this isolated directory. All code-command sessions
finished; the asynchronous reviewer-permission question remains separate.

## Later Independent Review And Correction

The earlier paragraphs record the original pre-review pass. Subsequently,
one newly authorized independent reviewer completed and was closed. Read
additive-source-independent-review-2026-10-26/REVIEW.md and RESPONSE.md.
No fatal flaw was found under the stated native/geometric assumptions.
The parent's follow-up corrected the P2 sampler quantifiers: one uniform
sampler and one polynomial must cover all adaptively reached orders in
the original paid input length. Hitting remains unproved.

Post-correction two-bundle tests: 50 passed in5.23s. Final fifteen-bundle
regression: 376 passed in52.13s, warnings as errors, no skips. All three
Python files pass py_compile. Regenerated harvest write/check and separate
check pass; the preserved additive and stable-product replays also pass.
See the review folder's VERIFICATION.md for the complete command and scope.

New v2 receipt SHA256:
49ba449fa189ddd10b9c52db7d8ea13885bd6962a9e4889cd169799b842dae08.
This supersedes the original harvest receipt hash above. The original
additive receipt and independent review files remain unchanged. No native
geometric operation, successful uniform sampler, dequantization theorem,
quantum advantage, novelty or practical attack was added by this follow-up.
