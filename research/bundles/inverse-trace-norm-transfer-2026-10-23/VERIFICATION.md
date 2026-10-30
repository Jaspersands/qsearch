# Verification

2026-10-23. Scoped local verification; not full repository validation.

## Completed

- 20 new tests pass. The related native residual and inverse-span suites
  also pass: 63 selected tests in total, 0.88 seconds in the final run.
- Both new Python files pass py_compile with bytecode outside the checkout.
- Two report generations are byte-for-byte equivalent as parsed JSON, with
  all four recorded implementation/test/proof/dependency hashes verified.
- The fixed native input has n=7, N=49, K=6, distinct points and all-one
  targets. Its derivative square root has irreducible factors of degrees
  5 and 19. Explicit Rabin polynomial equalities/gcd checks independently
  verify the irreducibility conditions rather than trusting factor output
  alone. Both still use FLINT arithmetic; this is not a second library.
- Existing integer field arithmetic independently reconstructs the point
  polynomial, derivative square, factor product and nonvanishing at points.
- A SAME-input witness passes all six field parity checks and all 49 local
  inverse-trace predicates. The charged classical baseline used 44 trials
  and 3,694 field draws. The recorded seed and cap reproduce this result.
- Positive norm identities cover all four trace-one constants in F8, plus
  common factors. Repeated odd-degree factors are charged with their full
  multiplicity. Even-degree factors are not falsely prohibited.
- Negative controls demonstrate the trace-one assumption and the strict
  global-versus-modular degree guard. Invalid native shapes, duplicate or
  noncanonical points, zero D and an exhausted search cap are rejected.

Commands, run from this bundle:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider test_norm_transfer.py ../inverse-trace-residual-2026-10-23/test_residual_sat.py ../inverse-span-audit-2026-10-23/test_inverse_span_audit.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache /opt/anaconda3/bin/python -m py_compile norm_transfer.py test_norm_transfer.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache /opt/anaconda3/bin/python norm_transfer.py
```

## Not Established

No universal classical lower bound, classical dequantization, quantum
speedup, asymptotic frequency of the obstruction, formal proof-assistant
verification, independent review, or quantum/geometric execution.
The native input remains solvable, as its explicit witness demonstrates.
No full repository tests, qsearch validation, node check, registry admission,
commit or push was performed. Migration PID 4829 remains active and the
verified destination checkout is still absent at the final live check.
The moving source and staging were not edited.
