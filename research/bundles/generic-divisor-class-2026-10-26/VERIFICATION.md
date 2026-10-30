# Verification And Scope: 2026-10-26

-14 focused arithmetic tests passed.
- Independent review in tower-independent-review-2026-10-26/REVIEW_GENERIC.md
  accepted the scoped per-curve existence result and its rational3-torsion
  factor. It also checked144,258 finite-group cases and a real elliptic
  rational-torsion countercontrol. These are not tower Jacobian samples.
- Live class_bound.py outputs for e8,16,32,64 respectively give conservative
  bad-class upper bounds5.491307e-130,1.602376e-211,6.948336e-375,6.593419e-702.
- Subsequent actual construction is in ag-divisor-class-control-2026-10-26,
  not performed by this arithmetic helper. It has a full cube but is
  classically easy at its finite size.
- Eleven-bundle parent regression:303 tests passed in5.62s, warnings as
  errors, no skips. Ten implementation/test files compiled successfully.

The auxiliary-divisor analysis and separate construction review now narrow
the remaining question: suitable auxiliaries EXIST at sufficiently high
levels. Their construction cost, source/access costs and rational2-rank
remain unresolved. MATRIX_GEOMETRY.md records the next access audit.

No main repository integration, full-repository test, qsearch validation,
JavaScript validation, Git commit or push occurred in this isolated workspace.
