# Source-Aware Clean Bases, Not Cubic Feature Matrices

Classical comparator and conditional source theorem; external review pending.
No multiple producer or quantum algorithm is provided. Original-radius fits
do NOT by themselves establish uniqueness, planted truth or a Gaussian law.

## Actual Algorithm And Paid Access

Extract the known quotient from an EXTERNAL nonzero coefficient/multiple
pair as before. Partition the actual original records into DISJOINT n-row
blocks. For each unit label minor mod3, compute and verify its inverse over
the full missing-quotient ring g=3^d. Round the corrected original responses
by Q=q/g, solve the basis equations, lift the candidate, check c*candidate=w,
and verify EVERY original circular distance against a radius4R<q.

There is no requirement that the OTHER original responses round exactly to
the candidate's missing quotient. Nonbasis noise is allowed by the original
radius, not hidden by conditioning. Singular blocks, wrong fits, exhausted
fixed schedules and caps stay incomplete results, not no-secret assertions.
Unit coefficients directly give an algebraic preimage with original checks;
g3 is also supported. Classical linear observations need not be paired, so
odd dimensions and odd record counts require no invented padding or copies.

The unknown-coefficient workflow completely scans the declared centered
coefficient range and public valuation scope, unless it finds an original
radius fit. Labels alone enter cached block ranks and ring inverses. Values,
truth and errors never choose the basis. Every original verification is
charged. A whole scan/schedule cap aborts BEFORE partial execution. The
source theorem requires the full declared work or a fit, not a hidden cap.
Public basis ranks and inverse counts, selected-response rounding evaluations
and every full-bank radius evaluation are explicit in the scan artifact.
Logical matrix caps do not include certificate/interpreter overhead. For a
coefficient domain of size2C and K supplied vectors, multiply the per-pair
work by2CK; do not treat a polynomial-sized bound as a constant-cost oracle.

## Source-Wide Clean-Basis Event

For IID uniform original labels, an n-by-n block is invertible mod3 with
probability product_(j=1..n)(1-3^-j), which is at least1/2 by
product(1-x_j)>=1-sum x_j. Original Gaussian errors must be independent
of the labels AND independent across originals. Distinct IDs are not proof.

Let d_max be the maximum supported nonunit valuation, g_max=3^d_max.
For the TRUE counterfactual quotient at that valuation, the exact derived
error is round(g_max*X), by odd-divisor double rounding. Its probability
of being zero is p0=erf(sqrt(pi)/(2*alpha*g_max)). A unit block whose n
unwrapped derived errors are all zero is successful with probability at
least(1/2)*p0^n. Disjoint original blocks give independent source events,
so T=floor(m/n) complete trials fail with probability at most

    (1-(1/2)*p0^n)^T.

Probability powers are enclosed using EXACT integer arithmetic on rational
CDF endpoints. Large-power caps remain unknown and have a separate
reciprocal-Bernoulli half-block bound, never a falsely rounded-down budget.
Gaussian special-function endpoints use trusted Arb, not a claimed
independent transcendental proof.

If the SAME successful block is clean at g_max, it is clean at every smaller
3^d: zero-error intervals in the ORIGINAL X are nested. Its mod3 unit minor
is the same. Every true coefficient unit part at that valuation extracts
the SAME lower prefix. Thus ONE common source event covers every true pair
at every d<=d_max before any data-dependent producer chooses one. No
valuation/unit-part multiplier or fresh dataset per hypothesis is needed.

Original Gaussian radius failure and GLOBAL original-code separation failure
are also unioned, not multiplied. On those events any original radius fit
must be the planted secret, including fits from adaptive wrong hypotheses.
If external coverage supplies a true usable pair (or a completely scanned
small coefficient), the common clean block guarantees a verified fit.
That external coverage and source law are still MISSING. They are not
established by the verifier, control seeds, caches or hashes.

### Algebra Behind The Common Event

Use nearest rounding floor(z+1/2), including negative ties. If Q is odd,
write Q=2k+1. The integers e satisfying floor((e+k)/Q)=t are exactly
Qt-k,...,Qt+k. The union of their continuous rounding intervals is
[Q(t-1/2),Q(t+1/2)). Therefore

    nearest(nearest(qX)/Q) = nearest(gX), q=Qg.

For a true pair, x=s modQ and h=(s-x)/Q. Corrected responses are
Q*a.h+nearest(qX) modq. Periodicity of odd rounding gives the exact
derived equation a.h+nearest(gX) modg, with ORIGINAL a and X.
If nearest(g_max X)=0 then -1/(2g_max)<=X<1/(2g_max), which lies
inside every smaller-g zero interval. A unit matrix modulo3 remains a
unit matrix over every3^d. The coefficient unit part changes neither x
nor h for a true pair at that modulus. This is a deterministic coupling,
not a claim that hypothetical adaptations make independent observations.

On the common successful block, each true pair completes to s. On the
original-radius and global-distance events, every returned fit is s, even
if an adaptive scan visits false pairs first. Let delta_basis,
delta_radius and delta_code be the three failure bounds. A true-pair
coverage failure delta_cover then yields the CONDITIONAL source guarantee

    P(recovery failure) <= min(1, delta_basis + delta_radius
                                + delta_code + delta_cover).

No independence between the coverage event and the other events is used.
Without a proved coverage bound, the composed recovery field remains null.
The scalar alpha*q>=2*sqrt(n) guard is checked separately; satisfying it
does not certify an applicable worst-case lattice reduction or supply a
quantum distinguisher. Widths in live profiles are DECLARED premises.

## Failure Modes And Falsifiers

A full-rank combined bank can have only singular fixed blocks. This schedule
can fail despite a secret being recoverable by another method. Conversely,
a wrong basis candidate may fit a loose original radius: return a compatible
candidate, not a truth certificate. Global separation is a SOURCE event,
not a runtime claim that all alternative secrets were enumerated.

Unwrapped zero errors are sufficient, not necessary: errors that are nonzero
multiples of g are harmless in the ring. The constant-width countercontrol
therefore bounds ring-zero mass by p0 plus the tail beyond g-1, not just p0.
Any correct solution from a unit basis requires all basis errors to vanish
MOD g. A union over T blocks bounds the chance any basis succeeds.
For constant derived width and growing g, this still decays exponentially
in n for polynomially many trials. This is a limitation of this clean-basis
strategy, not a lower bound on all classical or quantum decoders.
At fixed positive derived width, p0 is strictly less than1. Even extremely
small nonzero-error mass eventually defeats polynomially many clean bases
as n grows. Success at n128 is not evidence of an asymptotic polynomial
attack at constant width. The three live source profiles are finite
conditional bounds at n8,n32,n128 with1024,4096,32768 originals; no such
large IID Gaussian banks were generated or solved in these profiles.

The live falsifiers include a full-rank combined bank with two singular
scheduled blocks, a wrong planted-secret candidate that fits all original
distances, and an unwrapped errorq that is zero modulo the missing ring.
The latter explicitly prevents a false "clean errors necessary" claim.

## Live Workflows

    python theorems/native_basis_lottery.py --write
    node research/certificates/native_basis_lottery_crosscheck.js
    python theorems/native_basis_lottery.py --check-probabilities
    python -m pytest -q tests/test_native_basis_lottery.py

Actual controls and the unknown-coefficient scan consume original records
and charge their work. Gaussian row/probability profiles are conditional
ledgers, not claimed huge-bank experiments or a discovered quantum speedup.
The JS checker independently recomputes ring inverses, basis membership,
response rounding, all original distances, scan/cache work, exact probability
powers and source unions. It does NOT independently prove erf/erfc endpoints;
the separate Arb replay reconstructs those with the same trusted library.

## Research Decision

Use this comparator BEFORE attributing value to a narrow-noise phase or
quotient mechanism. It removes unnecessary cubic feature matrices and
whole-bank triplet truncation from this sufficient classical route.
It does not weaken the principal quantum obligation: construct a genuine
source-compatible collective decision mechanism or multiple producer.
Prior-art/novelty review and theorem review remain open. Production CLI and
registry wiring belong to Gemini; standalone scientific workflows are live.
