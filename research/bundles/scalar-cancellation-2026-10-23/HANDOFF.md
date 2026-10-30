# Integration Handoff

Do not edit the source checkout or migration staging while copying continues.
This bundle is local research work, not a registered result or committed code.

## What Is Ready

- `scalar_cancellation.py`: public scalar diagonal solver, all reduced
  degrees g dividing p-1, exact roots and witnesses, explicit sampling caps.
- `composer_bridge.py`: connects it to the EXISTING isolated rank-compressed
  composer without copying or rewriting that module.
- `replay_scalar.py`: nine exact matrix controls, original inputs and scale
  witnesses, method/cost counters, source hashes, and an even-power falsifier.
- `SCALAR_CANCELLATION.md`: proof, randomness assumptions, cost argument,
  adversarial review and precise exclusions.

After migration verification, move reviewed code into the repository's
existing theorem modules. Replace the prototype's path-based composer import
with the normal repository package import. Preserve its input semantics and
original-matrix check; do not remove its rank-cap or degree<p guards.

## Claims To Preserve

The general scalar callback is implemented. The bounded-index public-label
composer can use it without a tiny-field exhaustive placeholder. Its bank
cost remains (g+1)^rank, so this is NOT the general fixed-degree,
polynomial-in-rank SDE implementation. Nor is it a full quantum receiver.

The full-field scan is deliberately restricted to p<=16*g^4 and counted.
The large-field method factors g, strips only those factors from p-1, and
uses small-order Pohlig-Hellman digits. Do not replace it with a scan, a
general discrete-log call, an unrestricted p-1 factorization or an unclocked
polynomial-root dependency while keeping the current complexity claim.

Choose each backend's security_bits using the complete receiver's number of
classical merge nodes. A local 2^-64 abort budget is not automatically a
2^-64 global budget. All source copies, unused targets, and retries stay paid.
Only public saved labels may be retried; do not draw new labels to obtain a
friendlier branch. A seeded replay does not verify the IID randomness premise.

## Routine Work After Migration

1. Integrate the reviewed modules and add a narrowly named CLI diagnostic.
2. Register the result as classical arithmetic verification, never speedup.
3. Run the new suite, central-rank suite, and relevant complete-instrument
   suites, then full repository tests, syntax checks and qsearch validate.
4. Preserve existing honest blockers for source preparation, receiver
   compilation, independent proof review, and a hard native application.
5. Do not launch a larger scalar benchmark campaign or new dashboard work.

The useful next GPT task is whole-reduction scrutiny or a new native input
bridge, not routine wiring or expansion of this arithmetic test grid.
