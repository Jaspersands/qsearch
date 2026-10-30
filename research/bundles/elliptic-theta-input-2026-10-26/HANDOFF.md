# Handoff

Work remains in the isolated research directory. Do not edit the migrating
Desktop or staging checkout. Verify a stable main checkout before integration.

Implemented: elliptic_theta.py constructs actual signed genus-one level-four
theta coordinates from a short Weierstrass curve in a field containing E[8].
It uses FLINT constant-degree roots, exact linear algebra, and symbolic
translation verification. Tests include a generic-j supersingular curve.

Gemini mechanical tasks:

1. Port the converter only after deciding the common finite-field adapter.
   Encode coefficients through specified base-field embeddings; the local
   code does not implement tower conversion between different FLINT contexts.
   Its declared field must also contain the normalization quartic roots; a
   further degree-four extension after E[8] is a proved sufficient bound.
2. Preserve equality-to-zero tests: this installed fq_default binding makes
   bool(field_zero) true. Never use field elements as Boolean pivots.
3. Keep signed four-coordinate points, origin handling, inverse conversion,
   and a single theta frame per endpoint across all levels. Do not substitute
   x-only or level-two Kummer coordinates.
4. Add the new receipt as GENUS_ONE_NATIVE_CONVERSION evidence only. Do not
   set geometric_quotient_executed or coherent_source_executed to true.
5. Link the written uniform-clock proof as a subsequent, unreviewed response
   to Finding 3. Finding 1 remains OPEN. Preserve the original independent
   review and older receipts unchanged.
6. Run targeted tests and replay, then the main registry validator after
   integration. A backend that accumulates auxiliary composita fails the
   resource contract even if small tests pass.

Next high-reasoning work: assemble and adversarially test a single theorem
with explicit augmented-input and reference-construction assumptions, then
compare its conclusion against the full prior quantum suborder algorithms.
Do not turn genus-one conversion into a new standalone algorithm candidate.
