# Global Support Of Native Moment PSD Functionals

LOCAL DERIVATION / REVIEW PENDING. A scoped relaxation counterexample, not
a quantum algorithm, population theorem, complexity lower bound or novelty claim.

## Decision

All four saved finite-hull SOS separators fail to exclude their full original
moment models: each admits an exact escaping moment point. One bounded
source-aware hull refinement now gives a PSD continuation on an independently
known empty native prefix. Further degree-two positivity cuts CANNOT reject
this particular continuation. More eigenvectors, square cuts or a larger
grid are therefore not the right response for that branch.

The continuation does not preclude branching, integer constraints, stronger
local marginal conditions or a different decoder. Three other expanded hulls
remain unknown; neither their grid failures nor a failed separator LP proves
PSD feasibility or infeasibility.

## Exact Global Test

The earlier compression uses a principal submatrix C=M[F,F]. Embed its SOS
vectors by zero outside F, NOT through its hull-specific reconstruction T.
For nonnegative rational weights alpha summing to one,

```
Z = sum_j alpha_j v_j v_j^T >= 0
Phi(x) = Tr(Z M(x)) = kappa + c.x
```

Native one-hot identities determine the coefficient expansion: constant
`sum alpha*v0^2`, p_i coefficient `sum alpha*(2*v0*vi+vi^2)`, and cross-block
J_ij coefficient `sum alpha*2*vi*vj`. Same-block distinct products vanish.
Clear denominators and divide by a positive gcd. All trace identities are
checked against the original saved vertices. No shared zero row of the
old hull is added to the global model.

The full classical base relaxation is E*x=B,x>=0 at the SAME original
fixed winding, with all source, conditional and marginal equations retained.

- A verified rational x with Phi(x)>=0 escapes THIS separator. It need not
  optimize support, be PSD or correspond to a native distribution.
- Signed rational y with E^T*y>=c in EVERY column and kappa+B^T*y<0 excludes
  the entire degree-two PSD relaxation at that winding.
- Numerical optimizer statuses, failed reconstruction and preflight caps
  yield UNKNOWN. One excluded winding never establishes whole-prefix exclusion.

HiGHS proposes support points and duals. Exact FLINT reconstruction and
whole-model checks decide acceptance. The exact reconstruction budget is
500,000 cells. Objectives are numerically scaled; proposed duals are recovered
against exact c/scale and multiplied by scale only in exact arithmetic.
Two saved objectives require 9,031 and 17,712 coefficient bits. This is real
certificate complexity, not an uncharged numerical implementation detail.
Canonical rational parsing now uses FLINT rather than Python's decimal-int
string conversion, without disabling interpreter-wide protections.

## Live Findings

Four original hull duals: target11366831/winding3 and target11672586/windings2,3,4.
All FOUR admit exactly certified base moment escapes, all individually
indefinite. Four support LP calls, approximately three seconds of support
analysis in the recorded run, excluding source compilation and hull refinement.
No global support obstruction and no unknown support verdict.

ONE refinement per escape adds that actual base point to the four old points.
Each five-point hull uses denominator8, 495 floating eigenvalue proposals and
at most eight exact positivity checks. Floating eigenvalues have no proof role.
Total 1,980 proposals, 25 exact checks: one positive, 24 negative. No new hull
SOS separator was found; the other three hulls are UNKNOWN, not feasible.

At target11366831/winding3 the exact convex weights are
`[3/8,0,1/4,0,3/8]`. All five original matrices reconstruct exactly from the
new 16-dimensional principal face. Exact compressed LDL proves positivity
of the mixture; the retained full moment array satisfies EVERY base row and
nonnegativity condition. The independent original-digit reference audit
proves the corresponding prefix has NO native word at ANY winding.

This is an exact degree-two relaxation gap at ONE native prefix/winding.
It does NOT establish a typical-instance gap, a hierarchy degree lower bound,
an inefficient-or-efficient recovery theorem, or source dequantization.
No new whole-prefix elimination or witness recovery was obtained.

## Reproduce

```sh
python theorems/ternary_psd_support_lift.py --write
node research/certificates/ternary_psd_support_lift_crosscheck.js
PYTHONPATH=theorems python -m pytest -q tests/test_ternary_psd_support_lift.py
```

The report pins hull, PSD, moment, prefix and source fixture SHA256 values.
Regenerate downstream artifacts after an upstream producer changes. The
BigInt checker first replays the original geometry, native emptiness and
earlier certificates, then derives all SOS objective coefficients, verifies
the four escaping full arrays, the refined hull faces/positivity, and the
retained PSD-gap array's exact mixture identity.

Twenty-three focused tests cover actual native-word controls, escaping full
models despite excluded hulls, global upper-bound controls, tiny rational
column violations, huge normalizations, winding/model tampering, false LP
success and unknown reconstruction guards. No toy-oracle algorithm is proposed.

## Falsification And Next Action

Audit the positive continuation's three-block marginal extendability before
building a generic higher-degree hierarchy. A constant-size exact separator
would reveal a missing non-PSD realizability constraint, potentially producing
a cheap native-valid pruning cut. If ALL three-block marginals extend, record
that stronger local gap and assess genuinely nonlocal mechanisms rather than
blindly raising moment degree or spending more time on this selected prefix.
See `NATIVE_TERNARY_LOCAL_MARGINAL_TARGET.md`.

Even a useful cut does not solve the two-witness bottleneck. Any decoder
integration requires charged source-law coverage, larger-root witness evidence
and comparison with ordinary classical native search. Independent mathematical
and novelty review remain outstanding.
