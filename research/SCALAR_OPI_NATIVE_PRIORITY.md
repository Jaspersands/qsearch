# Explicit Random Scalar OPI: Native Classical Falsifier

31 October 2026. Direction-selection and experiment contract. This reuses
published DQI, not a new quantum algorithm or a claimed separation.

2026-11-05 comparator update: SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md
supplies a source-specific proof for the known Johnson-radius sampler on
these exact binary IID half-set tables. Its asymptotic score approaches
1/2+sqrt(a*(1-a)), a=min(1/2,1-sqrt(1-R)); at R1/4 this is0.840625.
The score curve and list-sampling operations are prior art. The new note
pays their normalization on one global high-probability table event.
The unique-radius mean and finite comparisons below remain as executed;
they are not claimed to be the strongest asymptotic quantum benchmark.

## External Question And Comparison

Can a polynomial-time classical algorithm on the FULL EXPLICIT accepted
sets reach the known DQI score on random scalar optimal polynomial
intersection? The oracle separation does not answer this question:
[2610.02145v2, Sections1 and3](https://arxiv.org/html/2610.02145v2) explicitly
distinguishes scalar OPI from its random folded-oracle theorem. This has
greater immediate value than building another receiver with no native use.

Independent bounded reviews found no new paid operation reopening Goppa
key recovery, one-endomorphism EndRing, or lattice/hidden-shift sampling.
The new permutable StateHSP theorem is retained, but its explicit classical
applications are matched and T-conjugated-stabilizer learning fails its
promise outside already-solved central cases. Oracle sketching is also not
a free succinct-source compiler: [2604.07639v2, SectionIII.1, Eq5/Theorem7](https://arxiv.org/html/2604.07639v2)
charges roughly N Q^2/epsilon samples for Q queries to size-N data. Its
space advantages do not give a polynomial-in-logN source for this project.
These are selection decisions, not general impossibility claims.

## Fixed Candidate Contract

For the first experiment choose q=2^t, m=q-1 distinct nonzero evaluation
points, and k=floor(Rm), with fixed R in (0,1). Input contains independently
uniform q/2-element subsets F_i of F_q as COMPLETE explicit tables, plus
the field basis and points. Both algorithms see the same input. This is a
prime-power scalar OPI family, not a prime-field experiment, compact cubic
predicate, folded symbol oracle, or secretly planted solution.

Output coefficients of degree-<k P maximizing the verified fraction of
P(a_i) in F_i. The quantum mechanism is known balanced DQI with reversible
RS dual unique decoding and a polynomial filter. For ell=floor((k-1)/2),
2ell+1<k+1 pays the finite score identity. Its mean tends to
1/2+sqrt((R/2)(1-R/2)). Full table loading, coherent indexed evaluation,
field arithmetic, reversible decoding, repetitions and precision all cost
polynomial time in the explicit input length O(m q); no QRAM is free.
The hoped advantage is a constant approximation improvement at polynomial
cost. It is NOT a proved superpolynomial runtime advantage or our algorithm.

Prange completion has mean 1/2+k/(2m); actual finite comparisons require
restarts. Stronger published systematic-basis line search and annealing
already inspect every candidate on a line and were run for up to a million
moves: [2610.06753v1, SectionsC.3 andD](https://arxiv.org/html/2610.06753).
Do not rerun a weaker small line-search benchmark and call its failure
new evidence. Full-input Groebner, partial-symbol interpolation and other
structured classical algorithms remain legal. Generic oracle lower bounds
and the published restricted Prange tail bound do not cover them.

## The Specific Test

Try the retained accepted-affine-flat attack on actual random half-set
TABLES. The existing cubic_rs_affine_flats.find_flat routine only needs
bits/evaluate; its extension tests can therefore use a table directly.
Its failed budget is UNKNOWN, but any partial flat it actually found may
be checked point by point and used with its true dimension. Obtain its
annihilator with FLINT, compose the constraints with the original binary
RS EVALUATION map, solve the accumulated system, and verify the resulting
polynomial using independent native-field Horner evaluation. This avoids
confusing an unweighted Vandermonde kernel with the original RS code.

Use a precommitted prefix, retain all seeds and failed extensions, charge
every table probe and linear solve, and compare against actual Prange
restarts on the SAME tables and the retained rational DQI mean enclosure.
No new quantum implementation or benchmark framework is warranted.

Proof obligations before an asymptotic claim: give a uniform polynomial
clock, a source-correct rank/success bound for the actual partial-symbol
constraints, the output-score law under adaptive table use, and a matched
quantum time/tail comparison. Full tables can guide attacks; a random-query
lower bound cannot prohibit that. Finite success can falsify a finite
score claim, and finite failure proves neither hardness nor a separation.

## Cheapest Test: The Straightforward Forcing Certificate Fails

This mathematical test was done BEFORE implementing the proposed adapter.
There are exactly 2^(t-d) [t choose d]_2 affine d-flats in F2^t. For any
fixed flat, the probability a uniform half-set contains it is

    (q/2)_(2^d) / (q)_(2^d) <= 2^(-2^d),

with probability zero if 2^d>q/2. A union bound over all m tables gives

    Pr(any table contains a d-flat)
      <= m 2^(t-d) [t choose d]_2 2^(-2^d).

Its base-two logarithm is at most
log2(m)+(d+1)(t-d)+O(1)-2^d. With m=2^t-1, even d=ceil(2log2(t))
is absent with high probability. Thus all available flats have dimension
O(log t)=o(t). This is a property of this random TABLE ensemble, not a
transferred result for compact cubic predicates.

Consider ONLY the proposed FULL-ROW-RANK forcing certificate: force L
precommitted prefix coordinates into dimension-d flats and choose a
polynomial using those prefix tables alone. Its L(t-d) binary equations
can have full row rank only if L(t-d)<=kt. An untouched independent
suffix then has exact unconditioned mean score 1/2+L/(2m). The relaxed
certificate is consequently at most min(1,1/2+R/[2(1-d/t)])+O(1/m).
Reaching the DQI limit requires

    d/t >= 1-sqrt(R/(2-R))+o(1).

For every fixed 0<R<1 this requires linear-dimensional flats, contradicting
the counting bound. The straightforward certificate therefore reaches at
most the Prange limit plus o(1). Independent review accepted this scoped
deduction. Dimension counting DOES NOT establish full row rank, or bound
consistent rank-deficient constraints. Do not condition the independent
suffix calculation on the global no-flat event; these are separate claims,
and the rare exceptional event must be budgeted separately.

The exact integer-count artifact is
classical_baselines/scalar_random_opi_flat_count.json. It compares to the
existing rational-filter LOWER bound, so rounding the target cannot favor
the rejection. At t=10,m=1023,k=306 the relaxed forcing certificate needs
d>=6, while the probability ANY table has such a flat is at most 2^-24.
At t=12,m=4095,k=1228 it needs d>=7, with probability at most 2^-74.
Eight predeclared parameter rows were retained, including small rows where
the bound is vacuous. No random instance, SAT run, or quantum circuit was
executed; this is an exact counting falsifier of the proposed certificate.

Decision: do not build the adapter or expand a sweep. The highest-value
question remains full-input scalar OPI, but a further pass must supply an
actual operation exploiting dependent constraints or adaptive table data
before implementing it. The count is not a generic hardness result and
does not rule out additional unforced satisfaction by such attacks.

Next command: corpus been-tried/baselines for a SPECIFIED adaptive
partial-symbol operation, followed by its primary literature. Expected
artifact: an explicit algorithm with charged input use and a correctness
or failure calculation on the original RS source. Acceptance test: it must
use more information than the rejected full-row-rank prefix certificate
and the already-published systematic line search. Without that operation,
do not replace the missing mechanism by another benchmark or interface.

## 31 October Checkpoint: No Further Mechanism Admitted

`SCALAR_OPI_SOFT_DECODING.md` now records two reviewed exact restrictions
and a completed six-instance freeze-aware experiment. All 18 returned
native witnesses passed independent Sage verification. The repair did not
reach the retained DQI mean bound at q64 or q256 and is stopped. Finite
failure does not strengthen a hardness claim or justify a larger sweep.
Unequal symbol weights, adaptive full-table attacks and exact joint
messages remain outside the restrictions; they need an actual algorithm
before another implementation is justified.

A bounded independent comparison was made because the OPI work was
producing restrictions rather than a competitive algorithm:

| Direction | Concrete mechanism tested or inspected | Decisive baseline or missing obligation | Decision |
|---|---|---|---|
| Reciprocal-trace bit hidden shift | Paid elliptic-curve Fourier signs would give constant-success poly(n) recovery | Generic Boolean injectivization plus Simon already gives polynomial recovery on the same input; no independently motivated native application was established | Park; retain the full-value versus bit-oracle correction in `RECIPROCAL_TRACE_SHIFT_SCOPE.md` |
| DQI beyond the unique radius | Complete list decoding and coherent index erasure | Jo2607.16541 Sections4-7 already supplies this mechanism and its normalization obligations | No new implementation or novelty claim |
| Public Goppa jet quotient | Lexicographic cancellation of known internal/pair relations | Existing exact sequence leaves rank(E)+dim(ker(E)/L), with a public single-block rank certificate; global reduction and locator extraction remain unpaid | Keep parked; not a new compact quotient algorithm |
| Fixed-field AG four-base extraction | Existing AJT/formal completion reductions | No new constructive extractor was found | Keep parked |
| One-endomorphism EndRing | Existing geometric transport route | No new paid transverse map was found | Keep parked |

For Goppa, the native input is the binary public matrix and jet parameters,
not expanded coefficient vectors or a known support. Expanded dimensions
binom(k,d) and sum_j sum_(u<s_j) binom(k,u), growing degree, intermediate
expressions and locator readout must all be charged. The competitor is
Weis's matrix-free/tiled finite-field solver, not dense elimination. The
reused exact sequence and rank certificate are in
`GOPPA_LOCAL_QUOTIENT_PRESENTATION.md` Sections7-8; no new Goppa lower bound
was derived. The other parked directions retain their notes' exact promises.

The single highest-value unresolved question remains whether full-explicit
random scalar OPI admits a polynomial classical algorithm matching the
known quantum score. This ranking is based on the native open problem and
the absence of a newly paid alternative, not on treating failed controls
as evidence of quantum advantage. No new algorithm is admitted at this
checkpoint. The next useful artifact must specify a full-table operation,
its cost and source-correct analysis; another empirical schedule or barrier
without such a mechanism does not meet this pass's research criterion.
