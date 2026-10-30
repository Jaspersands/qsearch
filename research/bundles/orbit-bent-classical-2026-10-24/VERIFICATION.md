# Verification And Integration Boundary

2026-10-24. Six-file external bundle. No main checkout, staging, registry,
UI, Git or migration state changed. No additional independent reviewer.

- **14 new plus559 prior controls: 573 passed in6.42s**, warnings as errors,
  no skips, plugin autoload disabled. Six syntax checks across both new
  bundles passed. The tests are external controls, not main repo validation.
- Both receipts replay byte-for-byte. All seven bent-bundle source/dependency
  hashes, six orbit-bundle source hashes, and eight original predecessor
  hashes match. The late cubic-orbit provenance correction is included.
- Forward-only classical runs produced native perfect polynomials at
  (p,width,M,n)=(13,3,4,9),(31,5,6,20),(43,7,6,28),(941,5,188,565).
  All four took one recorded attempt; that is not a success-rate estimate.
  The last polynomial has degree at most563 and independently passes all
  188 original halfsets via Horner evaluation at all940 original points.
- All49 small-field y choices were checked:6 singular,43 nonsingular.
  The exact fraction6/49 is below the proved bound2/7. A separate capped
  seed control records a singular failed attempt with no coefficients.
- Numerical Fourier controls cover every nonzero v at (p,k)=(7,1),(3,2),
  with a nonpermutation negative control. They do not prove general bentness;
  the character-sum identity in the note does that for the specified class.

The determinant theorem remains LOCAL UNREVIEWED, with no novelty claim.
It is a classical falsifier of coordinate-MM perfect search, not evidence
of an advantage, not a solution of the anisotropic cubic problem, and not
a classification of arbitrary bent functions or coordinate changes.

## Bounded Gemini Handoff

After the local repository migration is genuinely verified, register this
as a negative result linked to the orbit extension, not a new candidate.
Keep its exact coordinate/permutation/rate assumptions. Reuse existing
generic affine-flat tools rather than integrating a second search engine.
Preserve native coefficients, input-generation definitions, hashes and
all failed-attempt accounting from receipt.json.

For the live anisotropic candidate, the next execution task is to REUSE
the existing cubic intrinsic-manifold portfolio on high-rate instances,
especially rates just above2/3 and around4/5, across growing fields/seeds.
The old438/684 result is at low rate and does not answer this question.
Do not alter the anisotropic residual or give the solver planted witnesses.
Save complete polynomial coefficients and original-table verification.
Report successes, failures, time, memory and actual work separately from
the ideal quantum probability certificate. A successful polynomial is a
search witness, not a claim about the quantum output distribution.

High-reasoning work remains the structured-MQ/norm analysis or a natural
problem reduction. Do not add coordinate-MM width sweeps: this pass supplies
an explicit classical solver throughout their proposed perfect-search regime.
