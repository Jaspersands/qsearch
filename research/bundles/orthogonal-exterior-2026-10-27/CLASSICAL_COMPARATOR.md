# Same-Oracle Classical Lower Bound For Hidden Singular Lines

27 October 2026. One independent AI review accepts the scoped argument;
see REVIEW_RESPONSE.md. Not human-reviewed or novelty-certified. This is a
black-box query separation, NOT classical hardness of a natural explicit task.

## Contract And Claim

Keep the ordinary opaque full-stabilizer oracle of RESULT.md, take k=1,
q odd and n>=3. The hidden U is a uniformly random singular line of the
split 2n-dimensional space. Its number of possibilities is

    N=(q^n-1)(q^(n-1)+1)/(q-1).

For either O or SO, independently relabel the left cosets of P_U by a
uniform injection into a sufficiently large fixed-width label set. A
classical adaptive randomized algorithm making at most t queries satisfies

    Pr[correct U] <= 1/N + binomial(t,2)*min(1,3/q).

Thus bounded-error recovery for every allowed U and opaque labeling needs
Omega(sqrt(q)) classical queries as q grows. The exterior receiver gives
poly(n,log q,log(1/epsilon)) quantum time on these SAME oracles. In
particular at fixed n>=3 this is an exponential-in-log(q) oracle query
separation, if the receiver proof holds. It is not a natural-input
exponential speedup or a new general HSP query-complexity phenomenon.

## 1. Uniform Fixed-Line Bound

For g outside Z={I,-I}, every fixed line is contained in one of its eigenspaces
over F_q. These eigenspaces have dimensions d_i with sum d_i<=2n. A scalar
orthogonal matrix is either I or -I; both are central and are treated
separately. Thus no eigenspace has dimension 2n.

If every d_i<=2n-2, the number of nonzero vectors on fixed singular lines
is at most sum_i(q^(d_i)-1), even when we ignore the quadratic condition.
Convexity, or repeatedly moving dimensions to the larger summand, gives

    sum_i(q^(d_i)-1) <= q^(2n-2)+q^2-2 <= 2q^(2n-2).

This bound also covers missing eigenvectors by filling the unused dimension;
there is no diagonalizability assumption. The total nonzero singular-vector
count is D=(q^n-1)(q^(n-1)+1)>=q^(2n-1). Hence the fixed-line fraction is
at most 2/q.

If an eigenspace E has dimension 2n-1, Q|E is a nonzero quadratic polynomial:
E cannot be totally singular, whose maximal possible dimension is n. A
nonzero degree-two polynomial on F_q^(2n-1) has at most 2q^(2n-2) zeros.
All other eigenspaces together have dimension at most one, contributing
at most q-1 additional nonzero vectors. Thus the fixed-line fraction is

    <= [2q^(2n-2)+(q-1)]/D <= 3/q.

Using the same nonzero-vector counts above and below cancels the q-1
vectors per line. The bound is deliberately conservative and may exceed
one at q=3, so cap it at one. It is uniform in the chosen g and n. It is
not the earlier maximal-singular-subspace fixed-point estimate.

For completeness the common kernel of the action on all singular lines
is exactly {I,-I}. If g fixes every such line, it fixes each coordinate
e_i and f_i. Fixing e_i+e_j, f_i+f_j and e_i+f_j for i!=j forces all their
eigenvalues equal. Orthogonality then forces that common scalar to be +/-1.
All these test vectors are singular. The same argument applies to SO.

## 2. Adaptive Opaque Labels And Universal Collisions

Work modulo the known central scalar subgroup Z={I,-I}. Queries whose
ratio is in Z have the same answer for EVERY hidden U; they carry no
information and must not be counted as distinguishing collisions.

Couple the real oracle to a fake oracle which assigns fresh distinct random
labels to successive new classes gZ, repeating labels only on the same
known central class. Run any randomized adaptive classical learner against
this fake oracle. Its entire query sequence and final output are independent
of U. Conditional on that sequence, each pair of distinct central classes
has ratio g_i^-1 g_j outside Z, and the probability it lies in P_U is at
most mu=min(1,3/q), by Section1.

Until the first such pair occurs, real and fake transcripts have identical
distributions under lazy uniformly injective coset labeling. The union
bound over all pairs in the fake sequence gives divergence probability
at most binomial(t,2)*mu. This does NOT condition U on prior failed queries
and then incorrectly reapply an unconditional fixed-point estimate.
The fake final output is independent of uniform U, with success at most
1/N. Adding divergence proves the claim, allowing arbitrary classical
computation, adaptivity and random coins.

Choose label width large enough to permit both lazy injections for the
bounded-query comparison, for example O(log|G|) bits with at least |G|
labels. Such opaque labelings are allowed by the receiver's oracle promise.
The theorem is a worst-case-oracle lower bound (via this distribution),
not a claim about functions whose labels explicitly reveal the subspace.

## 3. What This Changes And Does Not Change

The old O(nq^k) reflection attack is an upper bound, not evidence of
optimality. For k=1 it leaves a gap between Omega(sqrt(q)) and O(nq)
classical queries. We do not close that gap; no such closing is needed for
the polynomial-log(q) versus superpolynomial-log(q) comparison.

The lower bound is for hidden LINES ONLY. Do not transfer it to every
nonmaximal rank, explicitly given generators, algebraic labels, or a
natural problem supplying an efficiently computable hiding function.
Nor does it establish literature novelty: this fixed-point/collision
argument is standard in HSP comparisons and may already cover this orbit.
In particular [Decker et al., Section7.2](https://arxiv.org/html/1406.6511v1)
use nonscalar query ratios and fixed-subspace counts to prove classical
query lower bounds for GL parabolics. The argument here supplies a separate
singular-line count and treats universal +/-I collisions for the O/SO
domain; it does not present the collision method as a new technique.
The construction's relevant question is whether its orthogonal oracle
receiver has an additional published scope, not whether birthday bounds
or exponential quantum oracle separations are new.

Decisive falsifiers: a nonscalar isometry fixing more than 3/q of singular
lines; a flaw in the adaptive coupling accounting for universal central
collisions; or a receiver that needs more than the same opaque oracle.
Finite counts below are regression controls, not the proof of the bound.
