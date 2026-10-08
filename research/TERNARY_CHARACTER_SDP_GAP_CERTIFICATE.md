# Exact Finite Gap In The Native Character SDP

FINITE PRIMAL COUNTERCERTIFICATE / NOT A POPULATION OR ASYMPTOTIC NO-GO.
A numerical relaxed score alone cannot establish non-tightness. This
subsystem turns a public saved moment point into an independently checkable
exact feasible point, and bounds the scores of ALL genuine group characters.
It does not trust SCS status, floating eigenvalues, planted truth or heldout
data. The exhaustive character census is research verification, NOT part
of the candidate decoder and NOT an efficient growing-dimensional method.

## Exact Primal Feasibility And PSD

Average saved entries over each actual frequency difference, impose
conjugation across opposite differences and mix1/32 of the identity. Round
the resulting real/imaginary moments to denominator S=2^24, fixing moment0
EXACTLY1. All unit diagonals and complete difference constraints are now
exact rational equalities. The finite word frequencies are distinct; thus
identity mixing also respects every difference equality.

For the Hermitian rational point X, form its realification

    A = [[Re(X), -Im(X)], [Im(X), Re(X)]] = A_integer/S.

A>=0 iff X>=0. A floating Cholesky of A-I/64 proposes a lower triangular
factor L_integer/S. That computation is NOT trusted. Recompute exactly

    R_integer = S*A_integer - L_integer*L_integer^T.

Check symmetry and every Gershgorin margin

    R_ii - sum_(j!=i) |R_ij| >= 0.

Then R_integer is positive semidefinite, and
A=(L_integer*L_integer^T+R_integer)/S^2 is EXACTLY PSD. Arithmetic uses
checked integer bounds, not eigenvalue tolerances. A failed factor or
dominance check is a failed certificate. There is no assertion that the
numerical optimizer solved its problem or supplied a dual optimum.

## Rational Root Intervals

Use pi=16*atan(1/5)-4*atan(1/239). Its identity follows from the tangent
addition formula: tan(4*atan(1/5))=120/119 and subtracting atan(1/239) gives
tan=1 in the first quadrant. Bound each arctangent by40 alternating rational
terms and its next term; round the resulting pi interval outward to2^-64.

For chi_q(e), reduce e to its signed representative. Evaluate sine and
cosine rational Taylor polynomials at the midpoint angle. Add the angle
interval error, since both functions are1-Lipschitz. The common Taylor
error (22/7)^41/41! safely covers the chosen cosine degree40 and sine
degree41 polynomials for |angle|<pi<22/7. Outward round to denominator2^48.
The zero root is exact. The verifier independently rebuilds all intervals.
Standard series context: [NIST DLMF4.19](https://dlmf.nist.gov/4.19) and
[DLMF4.45](https://dlmf.nist.gov/4.45). No novelty for this arithmetic.

## Bound Every Realizable Character

For each full-root s in Z_q^n, the exact character score is the sum over
original records of

    cos(2*pi*(y1-a.s)/q) + cos(2*pi*(y2-c.s)/q)
      + cos(2*pi*((y1-y2)-(a-c).s)/q).

Use the rational cosine UPPER for every term. Enumerate ALL q^n secrets
within an explicit finite verification cap; its maximum integer numerator
is a rigorous upper bound U for all character scores. No secret, including
zero/divisible values, is dropped. A cap exhaustion cannot certify a gap.
The implementation also retains a lower witness, without claiming a unique
optimum from rounded interval scores.

For the rational moment point, Re[chi_q(-y)*X_uv] equals
cos(2*pi*y/q)*Re(X_uv)+sin(2*pi*y/q)*Im(X_uv). Choose each interval endpoint
according to the SIGN of its exact dyadic coefficient to obtain a rigorous
lower L for the feasible SDP objective. Put L and U over denominator2^72.
If L-U>0, the SDP optimum is at least L, while every true character and
every mixture of true characters scores at most U. Thus this feasible point
is NOT such a mixture and no rank-one point can optimize this instance.
The inherited rank-one soundness proof identifies rank-one feasible points
with characters; numerical rank is unnecessary for this conclusion.

## Meaning And Next Work

A certified gap refutes universal tightness of THIS full-difference
polynomial circuit lift. It does not refute low-noise/population tightness,
larger-sample regimes, other lifted hierarchies, classical postprocessors,
collective quantum receivers or the original hidden-shift problem. Inputs
are saved actual-native-law measurement cohorts, not invented oracle tasks.
The classical baselines consume quantum-produced records, so their recovery
is not classical simulation of the original quantum source.

The next useful question is WHICH additional globally realizable relation
excludes the certified point at polynomial representation cost. Do not
interpret merely enforcing rank1, adding more random starts, or observing
more numerical PSD as an efficient solution. Alternatively change the
optimizer/measurement architecture. The verifier itself expends q^n work;
it is a falsification tool, not a new algorithm.

```
python theorems/ternary_character_sdp_gap_certificate.py --write
node research/certificates/ternary_character_sdp_gap_certificate_crosscheck.js
python -m pytest -q tests/test_ternary_character_sdp_gap_certificate.py
```

Gemini owns routine CLI/registry/UI integration and full production validation.
Link to a scoped finite negative result; admit no speedup candidate. General
derivations still need review even though these finite witnesses are replayed
with exact interval/integer checks.
