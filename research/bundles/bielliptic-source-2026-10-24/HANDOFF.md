# Bounded Handoff

Read BIELLIPTIC_SOURCE.md first. This is an external research bundle while
the Desktop checkout remains unverified/migrating. Do not copy into the
main repository, change Git, or repair migration as part of this handoff.

## Established Locally, Not Independently Reviewed

- Constant-size branch-triple discovery finds an actual elliptic curve
  involution when one exists over the paid splitting/lift field.
- A genuine self-adjoint surface pullback has image rank zero or two.
- Rank two recovers K under the original input promises. Rank zero on the
  GIVEN product source has an explicit monomial involution; a smooth
  Jacobian target excludes diagonal signs and leaves a unitary exchange.
- Explicit degree-two target quotients reduce the exchange case to two
  degree-ell elliptic weak isogenies, with proved [2]-division and preserved
  masks. An independently valid full Sp4 source instead restricts to two
  old SL2 Borel problems. Neither backend was executed.

## Mechanical Work Worth Doing Later

1. In a verified local checkout, use an existing finite-field/curve backend
   for degree-six factorization, bounded extensions and even-model transport.
   Retain the original curve isomorphism and its y multiplier, not just
   moduli invariants. Failed factoring/root budgets must be explicit aborts.
2. Evaluate curve pushforward on actual degree-zero Jacobian divisors. Handle
   moved base divisors. Use the same weak basis to extract gamma's small-
   torsion action, then the existing bounded-CRT reconstruction with norm 4.
3. Construct ONE actual weak (ell,ell)-isogeny fixture to a smooth bielliptic
   target. Keep its kernel/phi private to fixture generation and comparison.
   The existing product-target arithmetic fixtures are NOT this instance.
4. In rank zero, implement q_s, i_s and the weak psi_s interface exactly as
   Section 5. Charge every field, torsion point and doubled even level.
   Preserve restricted access if the original source lacks arbitrary levels.
5. Record the returned source kernel only after a matched solver supplies
   both elliptic kernels. Do not turn the (ell+1)^2 count into a hardness
   flag or a successful result. Do not replace SL2 calls with arbitrary GL2.

An order-four lift is valid geometry but NOT a self-adjoint involution.
Pass it to the pre-existing general/skew-map analysis, not this rank gate.

Do not implement a new quantum Borel demo, add more opaque-label benchmarks,
or claim a Shor-level result. The highest-value remaining thinking lies
outside this special family, unless the native composition reveals a real
counterexample to the stated reduction.

## Reproduction

Use /opt/anaconda3/bin/python. Run test_bielliptic.py with pytest, warnings
as errors, then run replay.py --output receipt.json. See VERIFICATION.md
for the direct-dependency checks. Replaying compares mathematical outputs,
not timings. No cloud/API execution, background search or quantum execution
is performed by this bundle.
