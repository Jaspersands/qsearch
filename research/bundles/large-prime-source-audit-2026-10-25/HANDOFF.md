# Integration Handoff

Scientific result: pointwise weak images at small auxiliary primes can be
converted to the common-scalar transcript required by the existing source.
See LARGE_PRIME_AUDIT.md for the proof and limits. This is an input repair,
not an executed native solver or a quantum advantage.

When the main repository is stationary and verified locally:

1. Expose projective_calibration.calibrate_basis as PREPROCESSING of original
   weak evaluations. Supply actual curve-point operations, field embeddings
   and basis generation; the vector controls are not that backend.
2. Cache one calibrated tuple per prime. Reuse it across both elliptic
   copies and all group queries. Never silently upgrade a basis-only stored
   transcript: bridge-point evaluations are additional charged inputs.
3. Retain the 2d-1 weak-call cost and O(r^d) table cost, with a hard budget.
   Keep global_isogeny_promise_verified false unless established separately.
4. Link the paper audit to candidate blockers. Powersmooth-lifting and
   upstream suborder norm-solving are distinct obligations. Do not mark the
   latter resolved by the former.
5. Run the receipt and listed tests before importing artifacts. Preserve
   previous negative controls: their naive masking procedure really fails.

Do not implement a new circuit search, speculate about novelty, or fabricate
native execution. Actual elliptic point integration is mechanical follow-up
for Gemini only after the backend and field contracts are available. The
next high-reasoning task is the global validity of suborder intertwiners.
