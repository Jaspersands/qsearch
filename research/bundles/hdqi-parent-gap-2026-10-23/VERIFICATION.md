# Verification: Coefficient-Space HDQI Parent

## Executed

- 56 tests pass, including exact dyadic second-order matrices on seven graph
  families, signed couplings, number conservation, relative-form bounds,
  kernel/idempotent/projector identities and canonical-order conjugacy.
- Independent matrix exponentials and QR projectors check the rotated
  second-order expansion. Fixed-graph regular-bipartite gap expansions and
  commuting-family exact gaps are checked separately.
- The raw star norm formula matches dense controls. The bounded two-term
  star-sector gap formula matches independent four-dimensional QR controls,
  an actual invariant block of a full five-qubit star, and a 100-digit
  Decimal calculation from the direct analytic formula.
- Two Python files pass py_compile with cache outside the checkout.
- Two receipt generations match byte for byte. All three recorded source
  SHA-256 hashes match the code, tests and research note.
- Receipt includes 14 algebra rows, 70 finite spectra (m<=6), seven analytic
  star norm rows and seven analytic pair-gap rows. All exact algebra flags
  pass; the largest finite pilot-kernel residual is about 4.1e-15.

At d=100,000,000 and beta=0.00001 (kappa=0.01), the ANALYTIC formulas give
log2(raw hub term norm)=2830.2392323 and
log2(flat two-term restricted-sector gap)=-2778.0883539. No matrix of this
size was built or diagonalized. This is NOT the full-parent gap.

The finite controls' positive gaps are not an extrapolation certificate.
The star asymptotics follow from the written formulas, not a fit to data.

## Not Executed Or Established

No quantum preparation circuit, real device experiment, useful physical
HDQI decoding application, uniform global gap proof, efficient projector
construction, classical-hardness result, novelty certification, formal
verification or independent review of the new lemmas.

No full-repository test suite, qsearch validate, node --check, registry
admission, UI changes, commit or push. The migration worker was still live
and the final Developer checkout absent. All writes were confined to this
external bundle and its external research checkpoint. The Desktop source
and staging copy were left unchanged.

## Files

- parent_gap.py: dense algebra controls plus two scalable analytic formulas.
- test_parent_gap.py: targeted correctness and counterexample controls.
- PARENT_GAP_TARGET.md: problem, derivations, costs, falsifiers and next theorem.
- receipt.json: reproducible control output and source provenance.
- HANDOFF.md: research next steps and explicitly scoped routine integration.
- VERIFICATION.md: tested scope and non-claims.

The parent checkpoint RESEARCH_CHECKPOINT_2026-10-23.md was updated to point
here. No other research bundle was modified in this pass.
