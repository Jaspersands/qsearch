# Verification

2026-10-25. Changes remained in the isolated local research workspace.
No moving source, staging, old hashed dependencies, main registry, CLI/UI,
Git commit, or push was changed. The earlier authorized Rees reviewer was
not reused. This field deduction has no independent mathematical review.

## Commands And Results

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error elliptic-field-normalization-2026-10-25 source-field-audit-2026-10-23 native-membership-baseline-2026-10-25 double-level-source-2026-10-25 odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

386 PASS in 58.06s, warnings-as-errors, no skips. This includes the 31 new
field tests, 18 earlier field tests, and all 337 tests from the preceding
membership/source milestone. The focused new/old field run passed 49 tests
in 0.44s. No test failures occurred.

```sh
/opt/anaconda3/bin/python -m py_compile elliptic-field-normalization-2026-10-25/elliptic_fields.py elliptic-field-normalization-2026-10-25/test_elliptic_fields.py elliptic-field-normalization-2026-10-25/replay_elliptic_fields.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python elliptic-field-normalization-2026-10-25/replay_elliptic_fields.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python elliptic-field-normalization-2026-10-25/replay_elliptic_fields.py --check
```

Three syntax checks and both replay checks PASS. Receipt SHA256:
`fae48179979f865a00b9d78cbbbc1117133a8d9a5498ea4d41280a14d32d7bcd`.

## Tested Scope

- Every necessary supersingular trace class for characteristics 5,7,11,13,37
  and base degrees 1,2,3,4 gives pi^12=q^6. This does not assert realization
  of every trace class at every characteristic.
- Actual curves y^2=x^3+(1+u)x and y^2=x^3+(1+2u) over F_11[u]/(u^2+1)
  have 122 and 111 points. Both Hasse invariants vanish. Their sixth
  Frobenius powers are opposite scalars; their twelfth powers match.
- The repeated-root characteristic-polynomial countercontrol distinguishes
  a false companion-matrix nilpotent from actual elliptic Frobenius.
- For p=11 and base degree 2, the fixed base degree is 24. Separate torsion
  fields for orders 3,5,49 have absolute degrees at most 48,96,1008; the sum
  is 1152. No compositum or large field was constructed.

These are exact arithmetic/curve checks supporting the general proof. No
unknown isogeny, field embedding, theta model, geometric source, or quantum
algorithm was executed. No new algorithm or native hardness was established.
The removal of an extra common-field promise applies only to the specified
elliptic endpoint inputs and their products, not arbitrary supplied surfaces.
Main tests and `qsearch.py validate` were not run because the moving main
checkout was not edited. The research goal remains ACTIVE.
