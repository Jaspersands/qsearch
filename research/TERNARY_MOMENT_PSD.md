# Exact Native Moment Positivity And Valid Quadratic Cuts

LOCAL DERIVATIONS / REVIEW PENDING. No scalable native decoder, full SDP
infeasibility, population theorem, source dequantization or quantum speedup.

## What Was Missing

The previous pairwise LP has eight exact continuations on three known false
native prefixes. Pairwise probabilities need not be globally realizable.
For the original indicator vector `Y=(1,X_(j,d))`, every true native
distribution necessarily has `M=E[Y Y^T]>=0`.

The matrix uses `M00=1`, `M0i=Mii=p_i`, unequal same-block products0, and
cross-block entries J. Every original source/marginal/winding equation is
verified BEFORE building M. Added slack variables are NOT indicators.

## Exact Proof Authority

Symmetric rational elimination keeps a unit lower factor L and a diagonal D.
A positive pivot produces a Schur complement. A zero pivot is legal only
when its remaining row is zero. A nonzero off-diagonal at a zero diagonal
gives an exact negative quadratic direction; a negative diagonal does too.
The direction is lifted through completed squares back to ORIGINAL coordinates
and checked by direct exact evaluation. PSD requires complete exact
`M=L D L^T` with every diagonal of D nonnegative, including zero pivots.

Floating eigensolvers only propose shorter dyadic/integer negative vectors.
The exact rational quadratic value decides acceptance; a tiny negative value
cannot be rounded to a PSD conclusion. Bad eigenvector proposals fall back
to the already checked exact elimination witness.

For a certified negative vector v, every true native moment distribution
still satisfies `v^T M v>=0`. This is a LINEAR inequality in p and J:

```text
v0^2 + sum_i (2*v0*vi+vi^2)*p_i
       + sum_(i,j in different blocks) 2*vi*vj*J_ij >= 0,
```

where the last sum counts each unordered pair once. Clear denominators and
divide the common positive integer gcd, then introduce one nonnegative slack.
Retain all preceding source, domain, winding and cut equations. Re-solve and
exactly re-certify after EVERY cut. A negative vector rejects ONE supplied
point; only a checked dual for the whole strengthened LP proves a branch empty.
Generator flags are not trusted: the cut loop rechecks signed dual multipliers
against all original and added rows before accepting any obstruction.

## Live Outcome

The pilot retains ALL 26 windings of the three prefixes with prior exact
continuations:15 old exact obstructions and3 old unknowns are carried faithfully.
All eight previously feasible winding branches receive a three-cut budget.

- All eight original moment matrices are exactly indefinite.
- All24 added cuts are valid nonnegative-square inequalities with primitive
  integer coefficient sizes of6 or7 bits.
- All24 re-solved LP points have exact rational certificates; all are STILL
  indefinite. Together with initial points this gives32 negative forms.
- There are ZERO PSD continuations, ZERO new complete branch obstructions,
  and eight explicit `PSD_CUT_CAP_UNKNOWN` outcomes.
- No whole prefix is newly eliminated; no ordinary pair recovery is attempted.

Matrix dimensions42/43 include normalization/source kernels. The next pass,
`TERNARY_MOMENT_PSD_MIXTURES.md`, exploits them exactly instead of treating
zero eigenvalues as numerical failures or just increasing the cut budget.

The linked source moment report is SHA-256 pinned. Its initial large rational
arrays are referenced rather than copied; every later point carries its own
certificate. Recomputing the source report requires refreshing downstream
reports/checkers, even if only producer timestamps change.

## Attempted Refutations

Tests cover singular PSD matrices, zero diagonals with nonzero off-diagonals,
tiny negative rational pivots, lifted Schur directions, exact native mixtures,
every original three-register word under valid cuts, malformed factors,
false numerical eigenvectors, fake dual generator flags and cap semantics.
A frustrated pairwise-control example shows that rejecting one point can
leave honest native words feasible; no point refutation is promoted to emptiness.

The independent BigInt checker first replays all upstream native geometry and
moment proofs. It reconstructs every moment matrix, negative form, integer cut,
slack equation and strengthened primal/dual model. It checks the entire
cut/re-solve ledger and all windings, not only a chosen successful branch.
Human review and a scalable source-law theorem are still owed.

```sh
python theorems/ternary_moment_psd.py --cuts 3 --write
python -m pytest -q tests/test_ternary_moment_psd.py
node research/certificates/ternary_moment_psd_crosscheck.js
```

Gemini/Antigravity owns routine qsearch/registry/UI/full-production integration.
Do not expose these caps as SDP infeasibility, a new decoder or a quantum signal.
