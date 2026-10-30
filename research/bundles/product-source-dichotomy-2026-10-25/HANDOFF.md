# Integration Handoff

## Research Decision

For an ACTUALLY product-polarized surface target and the full known
product-polarized source order, do not treat the failed corner-saturation
branch as a novel surface problem. The complete dichotomy is:

- Nonzero projector pullback modulo ell: recover K classically.
- Zero projector pullbacks: route two elliptic weak-isogeny instances;
  retain UNKNOWN for their unsolved kernels. Preserve their query model.

The fixed-g proof also separates isolated elliptic factors from a
classically recoverable active block. Only g=2 is implemented here.

## Mechanical Integration After Migration

1. Port this bundle and its existing source-pullback/kernel-output
   dependencies only AFTER the main checkout is verified local. Do not
   edit the currently moving source or staging directory.
2. For target geometry that already supplies product projections, call
   reconstruct_pullbacks with squared target norms (2,2). Then call
   classify_projectors. Do not obtain projections by granting an unknown
   unpolarized product decomposition of a Jacobian.
3. Record the status separately from proof acceptance. A conditional K
   is not verified geometric input. Elliptic routing is not a solved K.
4. Expose the original allowed torsion levels and field costs. The helper
   restrict_weak_blocks needs PRODUCT source/target frames. Its blocks
   preserve the masks; it must not normalize them or query extra levels.
5. Retain the older corner/lattice controls as independent reference
   checks. The new direct projector route need not build full End(B).
6. Add CLI/registry coverage using the main project's current schema, then
   run its full tests, syntax checks, node --check index.js and qsearch
   validate. None of those main-checkout runs happened in this pass.

## Theory Work Still Worth Doing

The high-upside residual target is a genuinely modeled Jacobian lacking
supplied product projections or an exploitable extra automorphism. It is
not enough to generate another product arithmetic fixture. The next test
should either expose a source/construction flaw on that actual input or
find a new computable target map that the existing pullback machinery can
use. A full target order, Hom lattice or global splitting oracle cannot
be used as free advice to make that test pass.

LITERATURE_GATE.md separately records a withdrawn published reduction and
the global-oracle Hom-module composition. Do not mark the withdrawn result
as proved, and do not turn its global oracle into a native local input.

One independent reviewer previously authorized by the user has already
completed the Rees/source assignment. This new deduction is NOT covered
by that review. No additional independent review is claimed.
