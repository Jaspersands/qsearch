# Verification

2026-10-23. The final deterministic eight-chart solver has 24 passing
tests (2.32 seconds), including all 40 Lagrangians over F_3, exact chart
coverage, fresh opaque labels, and truncated-budget ABORT controls.
All three Python files pass py_compile.

The final replay recovered all 15 independently generated kernels at
primes 3, 13, 101, 1009 and 65537. At 65537 it charged 1136, 930 and 1211
actual oracle calls, each below the deterministic bound 5135. These are
exact equality-oracle proof controls, NOT geometric source timings.
The receipt fingerprints the final solver, tests, replay, notes and its
imported finite-field helper. Earlier randomized receipts are superseded.

Independent proof review and novelty review remain pending. No real
geometric oracle or quantum receiver ran; no polynomial-time
dequantization or speedup was admitted. Source and staging were untouched.

