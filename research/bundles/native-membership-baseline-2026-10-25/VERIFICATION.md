# Verification

2026-10-25. All changes stayed in the isolated local research workspace.
The intended `/Users/jaspersands/Developer/quantum algorithm search` checkout
was checked and remains absent. No moving source, staging, old dependency,
main registry, CLI, UI, Git commit or push was changed.

## Final Checks

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error native-membership-baseline-2026-10-25 double-level-source-2026-10-25 odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

337 PASS in 58.40s, warnings-as-errors, no skips. Includes 55 new tests.
The new bundle separately passed 47 tests before the Boolean-interface
incidence controls, then all 55 in 2.91s. No test failures occurred.

```sh
/opt/anaconda3/bin/python -m py_compile native-membership-baseline-2026-10-25/native_membership.py native-membership-baseline-2026-10-25/controls_membership.py native-membership-baseline-2026-10-25/test_native_membership.py native-membership-baseline-2026-10-25/replay_membership.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python native-membership-baseline-2026-10-25/replay_membership.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python native-membership-baseline-2026-10-25/replay_membership.py --check
```

Four syntax checks PASS; write/check and separate replay PASS. Receipt SHA256:
`47fbb300f37accd5638c08631390049bfcc0338597e1fd6f1f13c2021f813ff6`.
Receipt hashes the six implementation/theory/handoff files, imported local
Python dependencies, proof dependencies, and the retained PPAV paper.

## Evidence And Limits

- Supplied maps of degrees 2, 5, 25, 200, 36, 13 require respectively
  10, 16, 28, 42, 12, 32 membership calls. Exact rational conjugation
  integrality agrees with an independent adjugate-kernel containment check.
  Reconstructed original left ideals equal O*phi in both lattice directions.
  The known phi and target order are CONTROL INPUTS, not native advice.
- Exhaustive small projective-line prefix tests include dyadic and odd,
  nonfree kernels. Public lifts retain singular matrices and norms sharing
  factors with n, while their characteristic factors are excluded by CRT.
- A single planned weak-prime set suffices after per-query norm omissions;
  insufficient or malformed finite transcripts are rejected. No actual
  torsion-point transcript was acquired.
- Shared-mask cancellation is tested on nonintegral gamma. Different column
  masks fail despite passing determinant tests. Nonintegral candidate images
  give valid dimension-8 maximal isotropic graph data at three primes.
- A genuine supplied degree-100 endomorphism gives a false membership answer
  at level 3 if only the paper's integral-interpolant uniqueness bound is
  imposed. The stronger native bound rejects this shortcut.
- Dyadic exponent controls at 1,4,8,16,32 use 6,18,34,66,130 direction calls
  PLUS 4,10,18,34,66 content calls. This is exact protocol accounting, not
  native runtime evidence.
- Exhaustive matrices over F_2,F_3,F_5,F_7 confirm the at-most-two invariant
  line lemma for nonscalars and unique-line unipotent witnesses. The general
  Boolean-interface query bound is a proof deduction, not inferred from these
  examples, and does not apply to the undiscarded native geometric input.

No native geometric interpolation, unknown native kernel recovery, quantum
execution, native classical hardness, speedup, novelty, or independent review
was established. Main tests, `qsearch.py validate`, and Node/UI checks were
not run because the migrating main project was not edited. The goal stays
ACTIVE; the earlier authorized Rees reviewer was not reused.
