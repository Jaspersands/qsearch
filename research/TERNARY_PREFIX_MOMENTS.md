# Coupled Native Prefix Moments

LOCAL DERIVATIONS / REVIEW PENDING. Classical falsification baseline, not a
quantum algorithm, full native decoder, average-case theorem or novelty claim.

## Representation

The previous real-prefix and modulo-two tests both miss 16 known false native
prefixes. This pass retains cross-block correlations. For each allowed native
digit d at block j use a first moment `p_(j,d)`. For EVERY pair of distinct
blocks use nonnegative joint moments `J_(i,d;j,e)`, with exact consistent
marginals. A forbidden digit has no variable. Same-block products are exact
one-hot identities, not independent Boolean variables.

Each assigned primitive GS direction h imposes the ORIGINAL equation

```text
sum_j (h_(3j)-h_(3j+1))*u_j
      +(h_(3j)-h_(3j+2))*v_j = B,
B = the same functional applied to the exact native integer anchor.
```

For an equation `sum_(j,d) a_(j,d) X_(j,d)=B`, retain its mean AND every
digit-conditioned identity

```text
(a_(i,d)-B)*p_(i,d)
  + sum_(j!=i,e) a_(j,e)*J_(i,d;j,e) = 0.
```

Include the original scalar equation at each allowed fixed integral winding
`A.z=t+Q*k`. Test the COMPLETE winding disjunction. An actual native prefix
word gives valid moments in every required row. Pairwise consistency is only
a relaxation: it does not imply a global native probability distribution.
No positive-semidefinite moment-matrix constraint is included yet.

## Exact Certificates

Every optimization variable is nonnegative. Write the original integer
equations as `E*x=B`. A primal proof retains exact rational x, checked against
all rows and nonnegativity. A dual proof retains signed rational equation
multipliers y with

```text
E^T*y >= 0 componentwise; B^T*y < 0.
```

This is impossible for any nonnegative solution because
`B^T*y=x^T*E^T*y>=0`. Signed multipliers are valid for EQUALITY rows; they are
not the nonnegative inequality multipliers used in the earlier prefix LP.
The distinction is explicit in both code and independent proof replay.

Sparse HiGHS LPs only propose supports and faces. Reconstruct ORIGINAL
unscaled rational equations, verify every column/row, and reject any failed
proposal. A 500,000-cell full reconstruction preflight prevents silently
truncating an exact proof. Duplicate supports at different float tolerances
are processed only once. Guards, LP statuses and failure paths are retained
as UNKNOWN. Timing includes exact reconstruction, with model building separate;
original LLL compilation and physical source preparation remain additional.

## Live Results

All 16 frozen, independently certified fixed-winding gaps were tested, eight
at root16 and eight at root24. These are selected real search prefixes, not
population samples or newly planted targets. The complete schedule has 186
winding branches, with 635..1,545 variables and 689..2,395 equations per model.

| Winding result | Count |
| --- | ---: |
| Exact coupled-moment obstruction | 73 |
| Exact coupled-moment continuation | 8 |
| Unknown after dual/reconstruction attempts | 95 |
| Numerical primal without an exact certificate | 10 |

Two root16 prefixes are eliminated at EVERY allowed winding. Three other
root16 false prefixes have exact surviving coupled moments (1,2,5 windings).
The remaining 11 prefixes are unresolved, NOT eliminated. No root24 prefix
has a complete proof either way. Of 105 unknown winding classifications,
103 encounter exact-reconstruction guards. Increasing that guard may resolve
certification debt, but is not evidence of better native decoding.

The final producer charges 354 LP calls. On this shared host its recorded
analysis work including exact reconstruction totals about106 seconds and model
building about23 seconds, excluding original basis/source costs. Timings are
not comparative speedup evidence. Runtime decoder integration is not yet
justified by two selected-prefix eliminations: pair recovery and larger-root
scaling have NOT been retested with this much more expensive model.

## Attempts To Kill The Apparent Progress

- A fixed favorable winding is insufficient: both eliminated prefixes have
  exact dual proofs for every branch in the allowed schedule.
- The model might reject true native words: exhaustive small original sources,
  including nonunits/zero labels, test every actual word at every assigned
  prefix, including retained-domain restrictions and its correct winding.
- A numerical infeasibility flag might be misleading: every claimed obstruction
  verifies original integer coefficients and exact nonnegative columns.
- A positive pairwise continuation might be spurious: it is explicitly NOT a
  global native distribution, and no PSD moment constraint is claimed.
- Guarded models might be feasible or infeasible: neither status is inferred.
- Empty selected-prefix elimination might never help pair finding: both ordinary
  two-witness source-law success and total cost remain unproved.
- Fixed-degree improvements might disappear with size: growing hierarchy ranks
  could conceal exponential work. Do not automatically extend to rank3/rank4.

## Next Decisive Question

Audit the exact moment matrices of the eight surviving primal certificates.
Any globally realizable distribution has PSD matrix for `(1,X_(j,d))`.
An exact negative quadratic form supplies a valid linear moment cut, but
refutes ONLY that supplied point, not all feasible pairwise moments. A bounded
cut loop must re-solve and re-certify. An exact PSD continuation would show
even this stronger degree-two relaxation misses a known false prefix.
See `NATIVE_TERNARY_MOMENT_PSD_TARGET.md`.

```sh
python theorems/ternary_prefix_moments.py --prefixes 16 --write
python -m pytest -q tests/test_ternary_prefix_moments.py
node research/certificates/ternary_prefix_integrality_crosscheck.js
```

The independent BigInt checker rebuilds ALL original assigned/marginal/
conditioned/winding rows, checks every rational primal or signed dual proof,
and verifies both the explicit prefix schedule and entire winding verdict.
It uses exact common-denominator integer arithmetic for the large certificates;
no eigenvalue tolerance or numerical LP is trusted. Human review remains owed.
Gemini/Antigravity owns routine CLI/registry/UI/full-production validation.
