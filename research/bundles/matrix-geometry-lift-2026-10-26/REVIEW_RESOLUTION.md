# Independent Review Resolution

Date: 2026-10-26. Read
`../matrix-lift-access-review-2026-10-26/REVIEW.md` for the frozen audit,
48 equality/scaling controls, sharp below-length counterexample and two
finite-algebra controls. The audited files and original receipt are unchanged.

Accepted: the lift identity includes d=2g+1 and m=2d+4, respects column
scaling, reconstructs P, and recovers the exact class H-P. The explicit
m=2d+3 counterexample rules out lowering this length premise universally.

Scope correction: the mathematical theorem covers general finite fields
and genus zero under the complete-AG promise. `point_lift.py` implements
only canonical integer matrices over odd primes below2^63 and g>=1.
Necessary rank checks do not recognize an AG code. This implementation
restriction is retained because the actual fixture is genus41 over F100003;
no general finite-field backend is claimed.

Positive access correction: exact quadratic generators yield truncated
graded multiplication through any fixed degree by polynomial linear algebra,
without a general Groebner-basis claim. This gives represented-divisor
operations and Jacobian group operations. It does not provide zeta data,
discover torsion, or solve the short effective-divisor search. The dense
degree-seven bound is polynomial but impractical; compressed quotient
construction is the appropriate implementation task for a separate wiring
pass. Higher-degree evaluation kernels must NOT replace ideal relations.

The adapted original rows preserve native evaluation on unpunctured points;
the tangent at recovered P restores its local evaluation frame. A future
backend must keep those frames, row identification and coordinate order.
Canonical/differential construction and residue normalization remain separate
work. Do not replace B by projectively normalized columns when solving Bz=s.

No genus41 graded backend, zeta polynomial, torsion basis or auxiliary native
witness has been produced. The new `prime-sampler-halving-2026-10-26` note
separately investigates relaxing uniform-sampler access; it does not alter
this review's frozen conclusions or supply unknown group order.
