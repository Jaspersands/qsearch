# Verification, 2026-10-25

Isolated research workspace only. No source/staging/main repository edits,
CLI or UI integration, commit, or push. The intended stable local main
checkout was absent. Main qsearch validate and JavaScript checks were not
run or claimed; neither file was edited.

Executed with /opt/anaconda3/bin/python:

- Initial splitting tests: 24 passed in 1.06s.
- Added a changed-integral-basis control; final splitting bundle: 25 tests.
- Final eight-bundle regression: 296 passed in 20.14s, warnings as errors,
  no skips. Included source-algebra-splitting, polarization-completion-probe,
  double-level-source, kernel-output, smooth-repolarization,
  one-endomorphism-access-audit, suborder-transcript, large-prime-source-audit.
- py_compile passed for all six Python files in the two new bundles.
- replay_source_split.py --write --check passed, six live controls.
- Separate replay_source_split.py --check passed with identical receipt.

Receipt SHA256:

    b3a743b9289506be1aa3281597907dcecba1409c373bec84861711453a75c68f

Independent review retained unchanged, SHA256:

    471723b406440c0e73723a5d77e41dbc680cf10b88d9c8355de1e8b5fbeacc49

The reviewer was closed after completion. The repair itself was implemented
after that review and is not independently reviewed again. All command jobs
were finished; there is no background search worker.

The live workflow builds six source splits, including large odd primes,
prime powers and mixed levels, checks every multiplication/involution table,
and sends each result through the existing 2m extension. These are finite
exact source-algebra controls, not a native elliptic/PPAV computation or
unknown-kernel recovery. The analytic polynomial-cost statement is in
SOURCE_SPLITTING.md and is conditional on its exact source/factor promises.

Native-input preprocessing and the uniformly bounded geometric-source
contract remain open. No quantum speedup or general native-suborder-only
theorem was established.
