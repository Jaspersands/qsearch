# Next Target: Lift Supplied-Hull PSD Duals To Global Support Proofs

IMPLEMENTED. All four full-model support tests give exact escapes. One bounded
hull refinement yields an exact PSD continuation on an independently empty
native prefix; three expanded hulls remain unknown. See
`TERNARY_PSD_SUPPORT_LIFT.md` and `NATIVE_TERNARY_LOCAL_MARGINAL_TARGET.md`.
The original specification below is retained for scope and proof review.
Research task, not an accepted candidate or a speedup.
Read `TERNARY_MOMENT_PSD_MIXTURES.md`. Four exact positive-SOS functionals
exclude four small supplied hulls. The full native moment relaxation is unknown.

## Question That Changes The Next Action

For each existing PSD dual Z, is its support over the ENTIRE original native
moment LP negative, or does a certified point outside the supplied hull escape?
Do not increase the finite grid, import its hull-specific zero rows globally,
or call a finite-hull obstruction a full SDP result.

The compressed matrix is a principal submatrix of the original indicator
moment matrix. Embed each dual vector by zero outside the saved free indices.
Then `Z_full=sum alpha_j v_full,j v_full,j^T` is PSD on the full indicator
space. Its trace functional is `Phi(x)=kappa+c.x` in the ORIGINAL p/J variables.
Any globally realizable or PSD moment point has Phi>=0, regardless of which
source/hull reconstruction relations were used in the earlier proposal search.

## Exact Support Alternatives

The base model is `E*x=B`, `x>=0`, with original assigned/digit-conditioned
equations, retained domains and the SAME fixed winding. Solve the classical
LP maximizing c.x, not another arbitrary feasibility LP.

1. A rational verified moment point with `kappa+c.x>=0` is an EXACT escape
   from THIS dual's exclusion, not necessarily a PSD point. Add it to the
   supplied hull if mathematically useful. No optimization guarantee is needed
   merely to prove an escape.
2. An exact signed equality dual y with `E^T*y>=c` and `kappa+B^T*y<0`
   proves Phi<0 for EVERY feasible base point. Since Z is PSD, this excludes
   the whole degree-two PSD relaxation for THIS winding, not merely four points.
3. Failed numerical optimization or exact reconstruction stays UNKNOWN.
   Never interpret negative Phi at the numerical optimizer as a global bound.

Clear all SOS coefficient denominators by a positive scale. Reconstruct
original unscaled y from proposed active columns and check every column and
the strict upper bound exactly. Retain Z's nonnegative rational weights,
embedded vectors, objective coefficients, all LP proof data and bit sizes.
No unavailable SDP package is needed for this support test: the current
SciPy/FLINT infrastructure suffices, with exact proof authority unchanged.

## Experiment And Falsifiers

Start with the four existing duals and their actual source/winding models.
Verify all honest native-word controls and correct dimension/order of embedded
indicator vectors. A hull-zero-row accidentally imposed as a global constraint
invalidates the experiment. Prove each SOS trace/objective identity independently.

If any global bound is negative, expand only where justified to all required
windings. A whole-prefix exclusion still requires EVERY allowed winding;
old reconstruction unknowns cannot be silently filled in. If support points
escape, record them as exact new moments, audit their PSD matrices, and use
them for a bounded source-aware hull refinement rather than blind new seeds.

Likely failure: every restricted-hull dual has nonnegative support on the full
polytope. That shows the selected hull was misleadingly narrow, not that a PSD
point exists. Alternating dual/point refinements may require exponentially many
steps or large rational bit complexity. Even complete degree-two exclusions
may only eliminate easy selected empty prefixes and never find two witnesses.
No candidate acceptance without source-law success, total receiver cost,
classical comparisons and all original native-phase/reduction obligations.
