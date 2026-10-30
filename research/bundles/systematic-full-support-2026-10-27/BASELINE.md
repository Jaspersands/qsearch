# Compare Native Search Costs Before Improving Divisor Search

Status: independent mathematical review accepted the counting and output-law
claims; comparison qualifications are incorporated below. See REVIEW_RESOLUTION.md.
No novelty, hardness,
quantum speedup or implemented large-tower claim. This is a matched classical
baseline for the existing full-support relation, not a new research problem.

## Native Problem And Algorithm

Input is an explicit full-row-rank B in F_q^(k by m), an arbitrary s in F_q^k,
and the task is to find z with Bz=s and every z_i nonzero. No curve, Jacobian,
valid starting point, distributional advice or oracle is supplied. The code
below supports odd prime fields; the argument holds over explicit finite fields.

Choose k pivot columns I by Gaussian elimination, with complement J. Sample
z_J uniformly from (F_q^*)^(m-k), then set

    z_I = B_I^(-1) (s - B_J z_J).

Accept exactly when every pivot is nonzero, and verify the ORIGINAL B,s.
Preprocessing is polynomial matrix arithmetic. Each trial uses m-k nonzero
field draws and O(k(m-k)+m) field operations, plus native verification.
If m=k the proposal is deterministic; invalid output is not a hardness claim.

This is the elementary systematic/information-set rejection baseline. It is
not the distinct enhanced Prange optimization algorithm of Shutty et al.
[2604.24633v2](https://arxiv.org/abs/2604.24633v2). That paper is relevant as
a warning to compare quantum decoders with matched classical constructions.

## Exact Counting, Including All Syndromes

Write V=rowspan(B) and choose a nontrivial additive character psi of F_q.
For u in F_q^k, let c=uB. Character orthogonality gives the number N_s of
full-support solutions:

    N_s = (q-1)^m / q^k * (1 + R_s),
    R_s = sum_(u != 0) psi(-u.s) (-1/(q-1))^wt(uB).

The expression is real, even though individual character terms can be complex.
No random-code or independent-pivot assumption is used. If the minimum weight
of V is at least delta, then

    |R_s| <= alpha := (q^k-1)/(q-1)^delta.

Every full-support solution corresponds to exactly one nonzero assignment on
J, irrespective of which invertible pivot set was selected. Consequently

    P_systematic(s) = (1-1/q)^k (1+R_s),
    P_affine(s)     = (1-1/q)^m (1+R_s).

When a fiber is nonempty, their success-probability ratio is EXACTLY
(q/(q-1))^(m-k). Under ideal independent uniform coins, both accepted output
laws are exactly uniform on the SAME full-support fiber, also conditional on
success before a fixed attempt cap. Seeded replay does not prove that law.

If alpha<1, every syndrome has a witness and expected systematic trials are
at most (q/(q-1))^k/(1-alpha). A conservative cap using a proved lower bound
p0>0 is ceil(bits/p0), since failure <= exp(-bits) <= 2^(-bits).
The helper does not verify a user-supplied minimum-distance promise. A false
promise can yield a positive formal bound for an empty native fiber.

## Actual Tower Parameters

For the existing promised complete AG source over q=100003,

    g=5e+1, d=10e+3, m=22e, k=5e+3, delta >= m-d=12e-3.

This applies to all admissible divisor classes and monomially equivalent
matrices; it does not require a cubic annihilator or geometric reconstruction.
For e>=8, (q-1)^2>q implies

    alpha < q^(5-e) <= q^(-3) < 1/2.

Thus the expected native search cost is bounded by

    poly(m,log q) * (q/(q-1))^(5e+3) / (1-q^(5-e)).

At fixed q this is STILL EXPONENTIAL in e. It does not dequantize a proved
polynomial quantum algorithm on an efficiently constructible unbounded family.
But its leading binary trial exponent is

    5 log2(100003/100002) * e,

whereas the known four-list upper bound uses ceil(r_2/3), at most roughly
10e/3 at worst rational 2-rank. On the COMMON CERTIFIED RANGE e>=64, the
systematic rate is much smaller than that worst-rank specialization. Actual
rational2-rank has not been established. The four-list analysis remains useful
as a structural attack. Comparing upper bounds is not
a runtime lower bound on either algorithm. Polynomial factors and the
four-list sampling, pairing, order and witness-conversion costs remain charged.

If r_2/e tends to rho, the DISPLAYED four-list exponential term improves the
systematic rate when rho < 15 log2(100003/100002), assuming the other charged
costs are polynomial. Equality is inconclusive at leading order; this is not
a necessary condition on every possible improved implementation.
A truly sublinear rank or polynomial effective-divisor constructor remains
potentially decisive. Another constant-factor improvement of a linear-rank
birthday exponent is not the next research priority.

## Falsifiers And Next Question

Decisive controls: enumerate every syndrome and every nonzero free assignment
in small explicit matrices; compare both exact probabilities and output counts;
test coordinate permutations and nonzero scalings; include forced-zero and
false-distance cases. Replay the existing degree-eight AG matrix without
using its geometry inside the sampler. These are correctness tests, NOT
evidence of asymptotic quantum advantage or a new family.

For the arbitrary-admissible-divisor-class family, what remains open is a
polynomial classical solver or a genuine end-to-end quantum candidate on
efficiently generated growing inputs, not a faster
exponential divisor join. The present argument supplies neither a polynomial
classical construction nor classical hardness. It also does not settle the
different inverse-trace, DCP or histogram-constrained problems. The known
near-canonical cofinal SUBCLASS already has a polynomial cubic/norm witness
solver. That stronger special-case baseline is not superseded here.

The two-sided estimate also bounds this particular ideal sampler's trial
count below by (q/(q-1))^k/(1+alpha). Thus at fixed q its expected trial
count really grows exponentially in e, or as exp(Theta(sqrt(input bits)))
for a dense Theta(e^2)-entry input. This is NOT a classical lower bound.

The refined unambiguous quantum transfer guarantee remains conditional on
the audited coherent construction and margin. See
../usd-review-resolution-2026-10-26/RESOLUTION.md. The current primary
[Ragavan-Shutty paper](https://arxiv.org/html/2610.00502v2) distinguishes the
two-fold quantum and three-fold classical mechanisms; this counting argument
does not close that general gap.
