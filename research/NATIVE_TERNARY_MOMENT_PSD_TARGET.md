# Next Target: Exact Positivity Of Native Moment Continuations

IMPLEMENTED: see `TERNARY_MOMENT_PSD.md` and `TERNARY_MOMENT_PSD_MIXTURES.md`.
All eight initial points and24 re-solved points are exactly indefinite;
bounded valid cuts leave eight cap unknowns. Four of eight supplied hulls are
excluded by exact PSD-SOS duals, not by a full moment-SDP proof.
The next target is `NATIVE_TERNARY_PSD_SUPPORT_LIFT_TARGET.md`.

Original specification follows. Mathematical research; no accepted candidate.
Read `TERNARY_PREFIX_MOMENTS.md`. Eight exact pairwise continuations survive
across three independently known false root16 native prefixes.

## Question

Do these points survive the necessary PSD moment condition? If not, do a few
exact quadratic-form cuts eliminate ALL allowed windings of those prefixes,
or merely move the spurious continuation to another feasible point?

Construct the ORIGINAL indicator moment matrix for `(1,X_(j,d))`:
`M00=1`, `M0i=p_i`, `Mii=p_i`, same-block unequal-digit moments0, and cross-block
entries from the recorded J. Any true native distribution has `M>=0` since
`v^T M v=E[(v0+sum_i vi Xi)^2]>=0` for every real v.

## Implementation And Proof Obligations

1. Reuse and verify the exact saved pairwise certificates before building M.
2. Use exact rational symmetric elimination. Singular pivots require genuine
   range tests; do not divide by zero or silently discard a nonzero off-diagonal.
3. An indefinite verdict must retain an exact rational vector v with
   `v^T M v<0`, replayed independently in original matrix coordinates.
4. A PSD verdict must retain a complete exact nonnegative LDL^T factorization
   or equivalent proof, including zero pivots. Numerical eigenvalues are proposals.
5. Negative v yields a valid LINEAR inequality in the moment variables. Add
   it with a nonnegative slack and exact integer-scaled coefficients, retaining
   all prior source, domain and winding rows. Cap the number of cuts explicitly.
6. Re-solve/re-certify after every cut. One negative-vector certificate rules
   out ONE point only; it does not prove the entire coupled relaxation empty.
7. Native true-word controls, exact tiny negative pivots, singular PSD matrices,
   zero-diagonal/nonzero-off-diagonal matrices and affine mixtures are essential.
8. Preserve complete winding schedules and unknown reconstruction cases. First
   target the three prefixes with exact surviving pairwise moments, not all
   16 indiscriminately or arbitrary newly planted tests.

## Failure Modes

A PSD locally consistent moment matrix need not arise from any global native
distribution. Fixed-degree semidefinite relaxations may be inadequate; a
growing-degree hierarchy may cost exponentially. A polynomial LP size says
nothing about the bit complexity of these rational certificates. Even complete
elimination of selected empty prefixes is not scalable two-witness recovery.
Improved pruning may be outweighed by source retention and exact proof work.

Decision: if an exact PSD continuation survives a known false native prefix,
record the stronger relaxation gap and deprioritize blind hierarchy inflation.
If a small bounded cut family eliminates all windings, seek a structural
explanation and a charged matched decoder experiment before calling it useful.
Either outcome is a falsification result, not a Shor-level algorithm.
