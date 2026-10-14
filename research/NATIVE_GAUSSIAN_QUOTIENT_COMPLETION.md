# Source-Correct Gaussian Quotient Completion

Conditional classical comparison and local split-rank derivation; external
review and prior-art audit pending. No multiple producer, Gaussian LWE solver,
decision circuit or new quantum algorithm is supplied.

## Exact Original-Record Adapter

Given an EXTERNAL nonzero coefficient c and claimed w=c*s modq, extract
g=gcd(c,q), Q=q/g, and x=s modQ by the unit part of c. This extraction checks
algebraic image membership, NOT membership in the planted secret's orbit.
For each actual original record(a,y), derive

    a'=a modg,
    y'=floor(((y-a.x) modq+floor(Q/2))/Q) modg.

IF w is true, y'=a'.h+round(e/Q) modg for h=(s-x)/Q. Every output keeps its
original ID and a parent hash; no mixture, fresh Gaussian error or independent
original sample was created. The source model is conditional, not certified
by hashes. Completion now defaults to the certified partial-coordinate
decoder at g, lifts its result back to x+Q*h, verifies c*candidate=w,
and checks ALL original error distances
against a public radius4R<q. A bounded fit still does not certify planted truth
under a false source or false multiple premise. Caps are incomplete results,
never nonexistence proofs. g<9 is outside this divided-cubic mechanism.

For odd Q, round(round(Z)/Q)=round(Z/Q) EXACTLY under floor(z+1/2):

    floor((floor(Z+1/2)+(Q-1)/2)/Q)=floor(Z/Q+1/2).

Thus with original e=round(qX), X~D_alpha, the derived error is exactly
round(gX). Its continuous width is alpha*g. There is no discrete-Gaussian
substitution, extra half-unit loss or noise resampling. Even divisors fail
this identity. All Gaussian probability boxes use trusted FLINT/Arb erf/erfc
at exact rational inputs and directed rational dyadic endpoints. A separate
replay detects modified boxes using the same library; it is NOT an independent
transcendental proof certificate. Extreme tiny masses can have lower bound0,
which must yield a vacuous rank budget rather than a fictitious positive floor.

## Improved Rank Argument: Base Plus Quadratic Features

The generic cubic hyperplane union bound charges the rarest noise mass on
every feature. That is unnecessarily weak when derived Gaussian errors are
usually zero. Let D be the full cubic feature dimension and K=n(n+1)/2.
Translate the secret to zero ONLY IN THE PROOF: canonical low trits translate
affinely overF3, while next-trit carries are univariate degree<=2 functions.
Together with constants, the feature space is preserved by an invertible
affine map, so coefficient rank is unchanged. No secret enters the decoder.
The carry polynomial identity kappa(z+3b)=kappa(z)-b mod3 verifies the shift.

Replace each u_i^2 column by u_i^2+v_i. At zero translated response, these n
columns and all pair-quadratic columns vanish. The remaining D-K base columns
contain independent high-label trits, linear low monomials, and canonical
mixed cubics. A nonzero base dual escapes with probability>=2/9 conditional
on zero error: high-label dependence escapes with2/3, otherwise a nonzero
canonical polynomial of total degree<=3 has support>=2/9.

Once zero-error rows span that base, a full annihilator can contain only
quadratic coefficients. A nonzero-error row contributes its nonzero trit
times every quadratic monomial; nonzero degree<=2 polynomials have support
at least1/3. If p0 and p* bound the zero and nonzero probabilities IN THE
TRUNCATED triplet law, rank failure is at most

    ((3^(D-K)-1)/2)*(1-2p0/9)^m
      + ((3^K-1)/2)*(1-p*/3)^m.

This yields sufficient row order O(D/p0+K/p*), not O(D/min(p_e)). It is a
source rank bound, not an optimal sample lower bound. The exact full F3 solve
and nonlinear feature checks are unchanged. Complete n1,n2,n3 structural
grids verify the two ranks; they do not replace the general polynomial proof.

For very small escape epsilon, the old fixed16 power block can have a zero
decay exponent. The new ledger uses T=ceil(1/epsilon) and
(1-epsilon)^T<=1/(1+T*epsilon)<=1/2 by reciprocal Bernoulli. The certificate
checks T*epsilon>=1 exactly and avoids expanding huge rational powers.

## Truncation, Adaptive Multiples And Original Verification

For derived width beta=alpha*g,

    p0=erf(sqrt(pi)/(2beta)),
    p+=p-=(erfc(sqrt(pi)/(2beta))-erfc(3sqrt(pi)/(2beta)))/2,
    tail=erfc(3sqrt(pi)/(2beta)).

Pay m*tail BEFORE using a truncated law. Independent scalar conditioning
preserves IID noise and independent uniform labels, and unconditional bin
probability lower bounds remain valid after dividing by a good mass<=1.
Rank failure is conditional; tail+rank is an unconditional union bound.
Original Gaussian radius failure and global original-code separation failure
are also charged. They are NOT independent events, nor inferred from a fit.

For every predetermined valuation d, the true counterfactual prefix
x_d=s mod(q/3^d) is fixed given the secret. Union the source failures over
DECLARED d before selecting a data-dependent true multiple. Unit parts at
one valuation share the same counterfactual dataset, not fresh samples.
Wrong multiples do not inherit that source law. External list coverage is
missing; composed unconditional recovery is therefore unset by default.
The completion API consumes KNOWN coefficient/multiple pairs. A list of
vectors with unknown coefficients is not this coverage promise: its complete
coefficient scan and repeated matrix work must be implemented and paid.
The old zero-error scan does not automatically invoke this new decoder.

Constant beta eventually has a vacuous whole-bank tail budget as m grows.
The live ledgers compare constant beta1/2 with a decreasing rational width
1/[2*(floor(sqrt(ceil(log2 n)-1))+1)]. They choose sufficient row counts,
sometimes extremely large, without materializing those hypothetical banks.
The source width alpha is declared as beta/3^d, not silently substituted for
an existing source. Logical matrix costs, actual caps and the scalar source
hardness interface stay explicit. Clearing that scalar guard is NOT a full
worst-case lattice reduction. These are source-conditional completion targets,
not hard-source experiments or a constructed quantum advantage.

## Self-Critique: Full Feature Rank Is Only Sufficient

A subsequent actual-record probe falsifies the need for FULL feature rank.
Using source_data(4,16,90,False,103001), add1 to only the first response.
The180 original rows have34 cubic features but coefficient rank25. RREF
nevertheless fixes all four low-secret coordinates uniquely. Enforcing their
canonical nonlinear features fixes the next digits, and the existing paid
full-root lift reconstructs the original secret. The old decoder rejects
this case as insufficient feature rank. No secret was assigned to solve it;
truth was used only for the final forward-calibration comparison.

This suggests a more valuable NEXT decoder: certify coordinate uniqueness
in an affine solution space, then impose the recovered canonical features,
rather than requiring every auxiliary feature to be independently determined.
Zero-error base rank may then suffice by itself, without the rare-noise
quadratic-rank event. That general implementation and source-budget upgrade
are now implemented in native_partial_coordinate_decoder.py with independent
coordinate/canonical-feature replay. The finite probe working contract is
preserved as superseded provenance; see NATIVE_PARTIAL_COORDINATE_DECODER.md
and hypotheses/native_partial_coordinate_decoder_contract.json.
The split FULL-rank bounds above remain valid but unnecessarily strong for
that prospective decoder. Do not turn their sample costs into lower bounds.
Established Arora-Ge linearization is relevant prior art; only primary
abstract/introduction scope was checked, not a full theorem comparison.

    python theorems/native_gaussian_quotient_completion.py --write
    python theorems/native_gaussian_quotient_completion.py --check-probabilities
    node research/certificates/native_gaussian_quotient_completion_crosscheck.js
    python -m pytest -q tests/test_native_gaussian_quotient_completion.py
