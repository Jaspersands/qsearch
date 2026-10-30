# Verification: Double-Level Source

2026-10-25. Work stayed in the isolated local research workspace. The
intended main checkout was checked and remained absent. No main/staging,
old dependency, CLI, UI, registry, Git commit or push changes were made.

## Final Commands

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error double-level-source-2026-10-25 odd-content-reduction-2026-10-25 cyclic-odd-degree-source-2026-10-25 prime-only-source-2026-10-25 kernel-output-2026-10-23/test_uniform_source_bound.py kernel-output-2026-10-23/test_kernel_output.py smooth-repolarization-2026-10-23/test_smooth_repolarization.py prime-square-flags-2026-10-23/test_prime_square_flags.py
```

282 PASS in 55.44s, warnings-as-errors, no skips. Includes 50 new tests.
The new bundle separately passed 45 tests initially and 50 after extending
the controls. The FINAL combined run includes the subsequently strengthened
counterexample with a valid mod-n lift but nonintegral conjugated half.
No test failures occurred during this pass.

```sh
/opt/anaconda3/bin/python -m py_compile double-level-source-2026-10-25/double_level_source.py double-level-source-2026-10-25/half_norm.py double-level-source-2026-10-25/local_baseline.py double-level-source-2026-10-25/controls_double.py double-level-source-2026-10-25/test_double_level.py double-level-source-2026-10-25/replay_double.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python double-level-source-2026-10-25/replay_double.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python double-level-source-2026-10-25/replay_double.py --check
```

All PASS. Six syntax checks; write/check and separate replay matched.
Receipt SHA256:
`7d298a2d1d0ee4d530a6159e63e31544ffbcce1ffb7b8ad91ee07bf43d33ddc7`.

## Scope Of Evidence

- Compatible generic dyadic order splits were checked in characteristics
  7, 11, 19 and 23 through modulus 32. A ramified-at-2 order was rejected.
- Even, odd and mixed degrees verify exact lift inverses, unchanged query
  reduction, Gram congruence at 2n, quadratic identity, trace class and
  public bounds. Identity queries exercise trace 2, rather than assuming
  every successful trace is at least 3.
- Formal half-ring norm identities include trace 2 and nonsemisimple
  specializations. The supplied degree-2 map checks five odd-prime kernels;
  the supplied noncyclic degree-200 map checks the ORIGINAL left ideal.
- Classical prefix tests cover both charts, dyadic and odd prime powers,
  nonfree kernels, scalar components, query-budget rejection and malformed
  responses. The finite controls use supplied kernels, never native labels.
- Dyadic exponents 1, 4, 8, 16, 32 used respectively 6, 18, 34, 66, 130
  DIRECTION comparisons. Add 2(e+1) content comparisons and one shared
  identity evaluation. These are linear counts, not timing evidence of a
  native isogeny attack. The same-source conditional dequantization record
  is stored inside receipt.json, not promoted into the main registry.
- For degree 6 and characteristic 11, the uniform plan uses 313 quotient
  primes, maximum weak order 2099, a 1465-bit trace bound and 2936-bit
  multiplier. Dimension 16 and r^16 kernel lists remain; no such points
  were enumerated.

No geometric source, unknown native kernel, quantum execution, classical
hardness or speedup was established. These extensions have no independent
review. Main tests, `qsearch.py validate` and Node/UI checks were not run
because the moving main checkout was not edited. Goal remains ACTIVE.
