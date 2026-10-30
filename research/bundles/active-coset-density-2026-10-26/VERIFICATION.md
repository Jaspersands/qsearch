# Verification: Active Coset Counting

2026-10-26, /Users/jaspersands/Developer/qsearch-research-work.
Interpreter: /opt/anaconda3/bin/python. Tests use exact SymPy arithmetic.

Commands completed:

    /opt/anaconda3/bin/python -W error -m pytest -q active-coset-density-2026-10-26

26 passed in16.32s, no skips, warnings as errors.

    /opt/anaconda3/bin/python -W error -m pytest -q active-coset-density-2026-10-26 full-suborder-impact-audit-2026-10-26 native-suborder-preprocessing-2026-10-26 additive-framed-source-2026-10-26 classical-symmetry-harvest-2026-10-26

123 passed in21.88s, no skips, warnings as errors. This is a focused
five-bundle regression, NOT a main-repository all-tests run.

    /opt/anaconda3/bin/python -m py_compile active-coset-density-2026-10-26/coset_controls.py active-coset-density-2026-10-26/test_coset_controls.py
    /opt/anaconda3/bin/python classical-symmetry-harvest-2026-10-26/replay_harvest.py --check
    /opt/anaconda3/bin/python additive-framed-source-2026-10-26/replay_additive_source.py --check

All completed with exit0. The earlier reviewed source and extraction
implementation were not edited. The new proof has no independent review
or proof-assistant certificate.

## What Was Checked

Cross-nilpotent products, exact quadratic conjugation, mixed third
differences, nonzero-query fixed-frame congruence, quotient-value versus
zero-event descent, COMPLETE group generators in the p=11 fixture, all17
hidden translations, polarized isometry checks, stabilized conjugation,
the signed-permutation extraction identity, all nonzero bivariate degree2
polynomials over F3, a composite-target character control, an even-index
counterexample, exact uniform/conditional probabilities, and invalid inputs.

The complete unit list uses an existing bounded norm enumeration whose
box completeness is checked; the finite monomial generating-set argument
is mathematical, not enumeration of the enormous group. The tests do not
prove the general counting theorem by finite sampling.

## Scope Flags

- Exact supplied-order controls: true.
- New parent counting proof: written, not independently reviewed.
- Native geometric automorphism enumeration: false.
- Unknown-order translation sampler: false.
- Uniform active-coset density lower bound: false.
- Native classical recovery / quantum execution / advantage: false.
- Main-repository integration, qsearch.py validation or node checks: not run.

The intended local main checkout was checked and remained absent. This
standalone research folder has no qsearch.py or index.js. No claim of CLI,
UI, native registry integration or a commit/push is made.

## SHA-256

New scientific artifacts at verification:

    60fdb0114a04c292ccbfb459938a29f6d083586e550347f70e5eec7d80ad06d6 ACTIVE_COSETS.md
    6cac9d3af90a984ad7ffd16ae2980dd6f4608fbbb3a9a0e19f89817b910d78e4 coset_controls.py
    1cb185f2b0224ae9eed4a5c3641d7381f3c4e857d9695387ca9ec541e7f3f39a test_coset_controls.py

Preserved prior artifacts:

    2c4b7ea6b15d6783dd9da827dd4b66bce33aeab1036bc9f9aa90f24d78fad9cc additive-source-independent-review-2026-10-26/REVIEW.md
    57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9 additive-framed-source-2026-10-26/receipt.json
    49ba449fa189ddd10b9c52db7d8ea13885bd6962a9e4889cd169799b842dae08 classical-symmetry-harvest-2026-10-26/receipt.json
