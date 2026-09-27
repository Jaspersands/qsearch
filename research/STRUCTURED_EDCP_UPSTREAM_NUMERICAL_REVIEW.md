# Upstream Mixing Certificate: Numerical Review

Date: 2026-09-25. RESEARCH-CRITICAL CORRECTIONS REQUIRED.

This is a targeted mathematical review of
`theorems/structured_edcp_upstream_mixing.py` and the generated
`research/reductions/structured_edcp_upstream_mixing.json`, inspected after
commit 8cac27ae. It is not a full repository review or full-suite result.
The theoretical note remains LOCAL DERIVATION / REVIEW PENDING.

## 1. Current Certification Is Not Supported

The code hardcodes `forward_carry_and_mixing_reduction_certified: True`.
The numerical fields do not validly implement the accompanying upper/lower
bounds. Until corrected and independently checked, neither this flag nor
dependent generated reports discharge the source's proof obligations.
`speedup_claim_allowed: False` is correctly retained.

The following reference evaluations use 110-digit arithmetic, the exact
integer parameter recipe, and log1p/expm1. They corroborate the theory note;
they are not interval-certified enclosures themselves.

| d | Reported log10 delta_amp Upper | Correct Formula Reference |
|---:|---:|---:|
| 64 | -99.3398985691 | -33.6294285738 |
| 256 | -158.9438377106 | -148.3397131413 |
| 1024 | -25872.3240073365 | -231.7930966613 |

All three `compute_joint_regularity` calls also return `delta_eval_upper=0.0`,
although the finite evaluation discrepancy is strictly positive. The analytic
clean-weight report at d=1024 returns 1.0, whereas the formula reference is
0.999999999329953752. A positive error upper bound cannot be rounded down to
zero, and a nonunit lower bound cannot be rounded up to one.

## 2. Causes And Required Repairs

### Missing Positive Regularity Terms

`compute_lpr_beta` forms a0=(1+2^(-2d))^m in ordinary floats, then a0-1.
At d=64 already, 1+2^(-2d) rounds to 1, deleting a positive term. At larger
d there is additional exponent underflow. The intended expression is

    beta=(a0-1)*(1+q^(-(m-n)))^d
         +a0*(d/r_mix)^(d*m)*q^(d*n)*(1+q^(-n))^d,
    a0=(1+2^(-2d))^m,
    delta_amp <= min(1, p_badminor^t + M*t*beta),
    t=floor(m/n).

The analytic table independently omits M*t*beta altogether. Its d=1024
branch also substitutes d*12 for the required logarithm of d^12 in the
bad-minor term. The table and certificate function consequently disagree.
Use ONE implementation of the actual finite expression, in a rigorously
bounded representation. log1p/expm1 repair cancellation but ordinary floating
arithmetic alone still does not provide outward-rounded certificates.

### Invalid Probability Orientations

`10.0**log_eval` underflows. Preserve an authoritative logarithmic or exact
bound with explicit direction; a display value of zero must never mean a
proved zero loss. Likewise calculate the clean weight through log1p and retain
an outward-rounded lower enclosure or a safe algebraic lower bound. Validate
the half-margin premise with exact integers rather than a rounded probability.

The d>256 error-tail branch drops the other two strictly positive terms and
labels exp(-d) an upper bound on their sum. Preserve the full log-sum even if
the omitted terms are tiny. "Numerically negligible" does not change which
side of an inequality a quantity lies on.

### Unsupported Fallback Parameters

The no-SymPy fallback calls numbers d^12+1 "primes". Those displayed integers
are not a certified substitute for nextprime(d^12); for these powers, the
sum-of-powers factorizations already give composite examples. The floating
root fallback also attempts enormous powers. Missing required exact arithmetic
should fail explicitly, or use a verified integer/primality implementation.
It must not silently change the theorem's hypotheses.

### Circular Counterexample Check

`lemma_46_carry_counterexample` sets the carry coordinates directly to
j-d/2 and compares their norm to 26.5. This checks a claimed closed form,
not that the original paper's operations produce that carry. The independent
reference must construct a=h*sum X^i, s=sum X^i, evaluate their negacyclic
product, perform the stated Phi/centering operation, derive the carry and
THEN compare it with j-d/2. Include a below-threshold case that does not refute
the bound. Keep the correction scoped to that intermediate lemma, not the
entire source paper.

### Revealed Coins Are An Access Condition, Not A Blanket Prohibition

The revealed-W control correctly rules out claiming that W*A is uniform
INDEPENDENT OF (A,W). It does not rule out every downstream algorithm that
uses W under a correctly specified access model. The current statement
"Rules out exposing W to downstream solvers or verifying oracles" is too
strong. For instance, the new readout sampler uses fresh selectors whose
fixed-matrix law is unaffected by pre-existing side information. It needs
only the matrix marginal bound, not uniformity of that matrix given W.

## 3. Gemini Acceptance Criteria

1. Do not claim a fully certified forward reduction based on a hardcoded flag.
   Distinguish bounded arithmetic checks, local mathematical derivation and
   independent/formal proof review. Derive any narrower machine-checkable gate
   from its actual checks and prerequisites.
2. Use the full finite formula for every artifact path. Preserve strict width
   premises, integer carry budgets, hybrid factors and source row counts.
3. Add independent reference tests at d=64,256,1024, including positive values
   below ordinary float range, a tiny but nonzero clean-weight loss, a vacuous
   width, missing exact dependencies and the original carry counterexample.
4. Separate non-authoritative decimal displays from certified bounds; test
   bound direction, not merely approximate agreement or a status string.
5. Regenerate dependent artifacts through the normal registry workflow and
   identify which prior fields were invalid. Do not overwrite the theory's
   caveats or claim the entire repository was verified by these targeted tests.

GPT's role in this pass was mathematical diagnosis and independent formula
evaluation. Gemini owns production repair, regression tests and regeneration.
