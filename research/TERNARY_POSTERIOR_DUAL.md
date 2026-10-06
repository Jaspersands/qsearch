# Exact Paired-Noise Posterior And Receiver Support Frontier

LOCAL DERIVATIONS / REVIEW PENDING. A real joint classical reference now
computes a least-trit posterior without enumerating secrets. Its generic cost
is EXPONENTIAL. No polynomial higher-root weak learner, accepted candidate,
general classical hardness theorem or quantum speedup is claimed.

Read [covariant noise](TERNARY_COVARIANT_NOISE.md) and
[least-trit bootstrap](TERNARY_LEAST_TRIT_BOOTSTRAP.md) first. This pass fills
the missing joint baseline rather than repeating the existing SQ screen.

## Correct Joint Likelihood

The source is fresh IID even-native qutrits at q=3^r with independent full
frequency rows a,c in Z_q^n. After the actual covariant readout, a record is
(a,c,y1,y2). Its density relative to uniform labels/outcomes is

    L_s = |1+chi_q(y1-a.s)+chi_q(y2-c.s)|^2/3
        = 1 + (1/3)*sum_(u,v in Delta_nonzero)
                         chi_q(u*y1+v*y2 - (u*a+v*c).s),
    Delta_nonzero = {+/-(1,0),+/-(0,1),+/-(1,-1)}.

Pairs are correlated. Replacing this by two independent marginal likelihoods
changes the inference problem. For example at zero error the correct density
is3; the independent-marginal substitute is25/9.

For M records, write their product as sum_F C_F*chi_q(F.s). Under a uniform
ALL-secret prior, the first-trit conditional density only needs

    C_0, C_+, C_-, with F_+ = (q/3)e_j, F_- = (2q/3)e_j.
    Z_t = C_0 + C_+*omega^t + C_-*omega^(2t),
    posterior(s_j mod3=t | records) = Z_t/(3*C_0).

This is an exact weighted signed-root partition function, not a single
modular relation or a sparsity promise after multiplication. All high digits
and other coordinates are integrated out using full-group orthogonality.
Primitive-only or externally restricted priors need different formulas.

## Implemented Exact Solver

Split the records into two halves. Each factor has seven frequency/phase
choices, with integer weight3 for its identity and1 for the six others.
Hash the half expansions by full modular frequency; join only buckets that
sum to the three target frequencies. All phases and cancellations remain.
The common3^M denominator cancels in posterior normalization.

Phase coefficients live EXACTLY in

    Z[X]/(X^(2q/3)+X^(q/3)+1), X=exp(2*pi*i/q).

They are sparse integer maps. There is no dense q-entry root table, even at
q=3^32. Reduction by the cyclotomic polynomial proves cancellations and
zero likelihoods exactly; small floating values are not used as zero tests.

Arb complex/real balls enclose all remaining evaluations. Exact conjugacy is
checked algebraically, the normalizer must be certified positive, and trit
ordering must be proved by disjoint balls or exact equality. Precision is
increased within a declared budget. Unresolved precision, zero normalizer
and exhausted state/join budgets return NO trit certificate. Tied maxima
are explicit. A reported per-record posterior is not a uniform-secret
success theorem for the missing weak learner.

The numerical backend follows the official
[Arb](https://python-flint.readthedocs.io/en/latest/arb.html) and
[Acb](https://python-flint.readthedocs.io/en/latest/acb.html) interfaces.
Working precision is scoped; it is restored after every evaluation.

### Cost Is Part Of The Answer

Raw half assignments number7^floor(M/2),7^ceil(M/2). Exact collision/cyclotomic
aggregation can reduce stored states, with a trivial maximum of
q^n*(2q/3) canonical monomials per table. Neither bound is polynomial in n,r.
Phase-bucket products at a frequency join can still cost as much as the
product of the half table sizes. Meet-in-the-middle does NOT certify a
square-root counting algorithm in dense collision regimes.

The ledger records every half-phase update, peak per-half stored monomials,
joined phase product and original qutrit. Distinct original IDs are mandatory;
their uniqueness does not prove sampling independence. All original labels
are retained. No classical simulator of unknown native states, chosen-label
oracle, cloned input or hidden secret is passed to the solver.

## Live Controls And A False-Positive Killer

Four fixed-seed IID native controls at(n,r,M)=(1,4,8),(1,8,8),(2,4,8),(4,32,8)
produce approximate trit posteriors

    (0.30506,0.17472,0.52022),
    (0.36998,0.24928,0.38074),
    (0.32159,0.32098,0.35744),
    (1/3,1/3,1/3) EXACTLY.

The last case has no nonzero target coefficient, not a numerical near-zero
fit. These are tiny-copy CALIBRATIONS at actual growing moduli, not evidence
for a polynomial recovery method or an average weak advantage.

A deterministic legal q9 record a=3,c=6,y=(0,3) has three formal nonzero
target-frequency terms. Their phases1,omega,omega^2 cancel EXACTLY. Its
least-trit posterior is uniform. Counting target relations alone is invalid;
signed phase weights and cancellations are essential.

The actual q3,n3 positive countercontrol uses19 fresh IID records. The existing
polynomial cubic incidence decoder recovers(2,0,1); the exact joint posterior
places all first-trit mass on2. The largest half table has52 monomials although
its raw expansion counts are7^9,7^10. This is a known-easy field counterexample
to promoting generic SQ/dual-expansion costs into classical hardness.

## Any-Processing Classical Least-Trit Copy Bound

With Q the uniform record reference, the six public-record characters are
orthogonal across ALL secrets, including zero and nonprimitive secrets:

    <L_s-1,L_t-1>_Q = (2/3)*1[s=t].
    <product_i L_s - 1, product_i L_t - 1> = d_M*1[s=t],
    d_M = (5/3)^M-1.

Average within a trit class and subtract the unconditional-secret mixture.
Coefficient squares sum to2/q^n, giving EXACT L2 norm squared2*d_M/q^n.
For any randomized classifier h_t in[0,1], sum_t h_t=1. Its excess success
over1/3 is(1/3)*sum_t<h_t,D_t>. Since D_t has zero mean, subtract1/2 from h_t,
use ||h_t-1/2||_2<=1/2, and apply Cauchy-Schwarz:

    mean least-trit advantage <= sqrt(((5/3)^M-1)/(2*q^n)).

This bounds ANY processing of the full raw paired records at that density,
not just SQ answers. It does not cover unmeasured states, different POVMs,
or extra legitimately acquired records. A necessary condition for advantage
epsilon is(5/3)^M>=1+2*q^n*epsilon^2. Polynomial surplus remains open.

## Low Record Degree: A Separate Restricted Screen

Project the product likelihood to ANOVA/Efron-Stein degree<=d in the COMPLETE
independent records. Different record subsets are orthogonal. Its centered
norm is

    V_(M,d) = sum_(j=1..d) binom(M,j)*(2/3)^j.

For classifiers whose OUTPUT FUNCTIONS have this bounded degree, the same
argument bounds mean advantage by sqrt(V_(M,d)/(2*q^n)). At d=M this agrees
with the preceding any-processing bound.

Do not infer this restriction merely because an algorithm starts from low-
order features. Nonlinear thresholding/elimination can raise output degree.
Coefficients depending on all labels are not automatically low degree in
COMPLETE records. Arbitrary ML, adaptive raw inference, growing degree and
the field incidence decoder are not excluded by this scoped screen.

## Full-Label Quantum Support Gate

Here is a distinct structural receiver gate. For M original qutrits, any two
computational words differing at j sites have a frequency difference described
by a j-supported word in Delta_nonzero. There are binom(M,j)*6^j such words.
For every nonzero word its frequency sum is uniform Z_q^n: one independent
row has a unit coefficient. The positive trit target has probability1/q^n.
Negative-target existence is equivalent because the difference family is
closed under negation. Thus

    Pr(any trit-relevant relation of weight<=k)
      <= min(1, sum_(j=1..k) binom(M,j)*6^j / q^n).

Outside this event, the secret-twirled trit classes have identical matrix
elements at word Hamming distance<=k. ANY full-label-controlled POVM whose
FINAL effects have radius<=k therefore has success1/3 there. On the remaining
sources allow success1; mean advantage is at most2/3 times the above event
probability. Labels/POVMs may be adaptive to the full source, but no extra
uncharged states or postselected success conditioning are granted.

At n8,r32,M4096, advantage1/10 requires final-effect radius at least38 by
this union gate. This is only necessary, not a receiver or runtime guarantee.
The earlier arbitrary-POVM copy gate is also necessary and remains separate.

CRITICAL: final-effect radius is measured in the ORIGINAL native word basis.
Local gates, sparse Hamiltonians and shallow circuits can generate wide final
effects. Even tensor-product POVMs generally have radiusM, not1. The bound
does NOT require entanglement or rule out these circuit classes. A hidden
basis-change compiler cannot be ignored when stating radius.

## Failure Audit And Revised Next Work

The exact solver can still be exponentially expensive, phase cancellation
can destroy an apparent relation signal, and a single MAP guess proves no
uniform weak advantage. Low-degree, near-entropy and short-radius screens
are not general hardness. The field positive control explicitly falsifies
that overreach. Every natural problem/source reduction remains separately
owed before a speedup claim.

Next focus: an ACTUAL source-valid wide-effect least-trit operation and a
computable estimator. Investigate an overlapping triple-cover instrument;
the existing Gaussian incoming oracle is complete ONLY for corner2, not the
three-corner cover. Corner1 still has a three-choice nonlinear witness problem.
Resolve that missing role or redesign the cover before claiming a compiler;
prove its output law and recursive copy cost, not just forward coverage.
Retain the original phase and outcome pointer, and reject free inverses or
exponentially costly recursive single-output extraction. Do not spend another
pass only plotting a dense optimum or counting unsigned relations.

## Verification And Ownership

Producer: `python theorems/ternary_posterior_dual.py --write`.
Tests: `python -m pytest -q tests/test_ternary_posterior_dual.py`.
Independent replay: `node research/certificates/ternary_posterior_dual_crosscheck.js`.

The JS checker expands the NINE original Born-amplitude cross terms, rather
than reusing the Python seven-term DP. It replays five exact posteriors through
52,498 half leaves, independently enumerates13,203 bounded calibration secrets,
and checks all27 field secrets exactly. Secret enumeration occurs ONLY in
bounded certificates, never inside the baseline solver.

GPT owns derivations and targeted verification. Gemini/Antigravity owns routine
CLI/dequantization/registry/site wiring and full production validation. Suggested
command: `qsearch.py ternary-posterior-dual`. Preserve cost and claim gates.
