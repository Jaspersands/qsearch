# Verification And Scope

2026-10-26. Isolated workspace: /Users/jaspersands/Developer/qsearch-research-work.

Added STABLE_PRODUCTS.md, stable_product_controls.py,
test_stable_product_controls.py, replay_stable_products.py, receipt.json,
HANDOFF.md and this verification record. Updated the root checkpoint.
No earlier proof, source, test or receipt was changed.

- Initial standalone suite: 24 PASS in0.45s; initial fifteen-bundle regression:
  374 PASS in52.00s, warnings as errors, no skips.
- A final self-audit added explicit nonintegral-entry rejection to the
  modular checker. Rational entries must not be truncated to integers.
  Final standalone suite: 25 PASS in0.42s. FINAL fifteen-bundle regression:
  375 PASS in50.56s, warnings as errors, no skips.
- All three Python files pass py_compile.
- Final receipt --write --check and separate --check: PASS after the final
  prose clarification and the rational-entry rejection regression.
- The exact formulas cover all moduli in the written proof. Tests include
  every modulus2..256, large prime powers, mixed moduli, reduction
  compatibility, symbolic identities and invalid input rejection.

Regression command:

    /opt/anaconda3/bin/python -W error -m pytest -q stable-product-access-2026-10-26 nonfree-factor-bound-2026-10-26 partial-quotient-symmetries-2026-10-26 interpolation-leakage-2026-10-26 native-nonbass-realization-2026-10-26 local-order-scope-2026-10-26 classical-symmetry-harvest-2026-10-26 additive-framed-source-2026-10-26 polarization-completion-probe-2026-10-25 native-suborder-preprocessing-2026-10-26 smooth-repolarization-2026-10-23 prime-square-flags-2026-10-23 source-field-audit-2026-10-23 elliptic-theta-input-2026-10-26 elliptic-field-normalization-2026-10-25

Final receipt SHA256:
b6f4780c5769973c32a2cabd2657a4f9d025d13d07bf2b8a546b661815845d71.

Preserved prior hashes checked live:

- nonfree-factor receipt:
  30ec92f99648a15388217d0b7a1f4b11da5b2586d85a046a281aefc7c47b86ca.
- additive-source receipt:
  57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9.
- classical-harvest receipt:
  0d68b2df50149d61fdec2fdfe6f71e3f71507a8df9faf4f2f7472efe1ae73272.
- combined-source independent review:
  471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49.

The test command completed; no test or download process remains running.
The separately authorized additive-source reviewer was interrupted with
the parent turn, recovered by SAME agent ID, and resumed. Its report is
not yet a result of this bundle. This product audit remains unreviewed.

These checks do not execute native finite-field curves, geometric
canonicalization, a class-product compressor, a quantum source, or unknown
ideal recovery. They do not establish a general computational lower bound.
The main local checkout remains absent at the live check. No whole-project
qsearch validation, Node check, UI/registry integration, commit or push was
performed in this isolated research directory.

Later same-day follow-up: the additive-source reviewer completed and was
closed. Its report is in additive-source-independent-review-2026-10-26.
The parent corrected the harvest theorem's uniform sampler quantifiers
and regenerated that bundle's receipt; the earlier hash above records
the pre-review snapshot. This product bundle's source and receipt are
unchanged, and it has NOT received independent review. See the separate
review RESPONSE.md and VERIFICATION.md for the correction and new tests.
