# Compressed Construction Reviewed, Demo Verifier Corrected

Date: 2026-10-26. Read
`../auxiliary-four-list-review-2026-10-26/COMPRESSED_REVIEW.md`.
This supersedes pending-review wording in the frozen handoff. The proposed
construction and FULL written certificate were accepted; the native backend
is still unimplemented.

The reviewer supplied a counterexample to the demo verifier: conjugating
the elliptic actions by diag(1,-1,-1,1) preserved the checked identities
while mapping1 to the negative of each named beta basis vector. Parent
reproduced the incorrect acceptance BEFORE editing. `certify()` now checks
U=uI,V=vI and both designated beta actions on1, as well as gamma. Added
regression tests reject the conjugated basis and altered pencil action.
These checks do not make the helper a general-purpose native certificate;
it remains specific to the explicit four-dimensional elliptic control.

Required Gemini implementation qualifications:

- Include EVERY cubic row i<j and every k, including k=i and k=j. The
  independent genus-two example loses rank6 to2 if repeated indices are
  omitted. Test A3=0; the expected A1,A2 dimensions alone allow bad pencils.
- Keep reduction maps evaluable via generator actions and expression trees.
  Do not materialize a dense column for every ambient high-degree monomial.
- If the pencil is chosen over an extension, Frobenius may MOVE the pencil.
  Holding u,v fixed while conjugating coefficients is not correct descent.
- A concrete descent of any requested finite graded piece starts with1,
  multiplies the already chosen ORIGINAL-Fq section basis by every original
  degree-one generator, selects a linearly independent spanning subset over
  the extension, and expresses products in those selected bases. The
  selected elements are Fq-defined. Uniqueness forces structure constants
  into Fq; verify q-Frobenius invariance and extract base-field coordinates.
  This descends the graded pieces, not necessarily a free module over the
  same pencil. All expression trees and coordinate frames must be retained.
- Charge quadratic normalization, coordinate changes, polynomial identities,
  field construction and descent in addition to the cubic solve. The actual
  cubic system size is36,162 rows by1,722 unknowns plus212 right sides.
  Streaming can save memory; initial sparsity does not prevent fill-in.

The independent reconstruction uses a genuine genus-two curve, solves all
missing actions from the quadratic table, checks identities and compares
true graded dimensions through degree7. A bad pencil passes A1,A2 but fails
A3 as required. Parent code was not used for that construction. Its separate
demo-counterexample imports the frozen OLD helper and is expected still to
show the old defect; the new regression tests verify the corrected helper.

The new `one-point-plane-adapter-2026-10-26` reduction uses this all-degree
module certificate as a premise to reach a growing degreeO(g) space. It has
its own review; accepting this compression alone does not accept that adapter.
