# Affine Pair Avoidance: Bounded Constructive-Method Audit

Date: 2026-10-27. Independent, bounded literature and mathematical audit.

## Conclusion

**No verified fixed-q polynomial-time extractor follows from the supplied
marginal ranks, kernel dimension, or additional small-set joint ranks.**
There is an explicit linear-algebraic resampling certificate, but the native
AG distance forces its dependency neighborhoods to grow linearly with e.
Small-set independence is not a substitute for the missing certificate.

The most relevant remaining constructive framework is the point-to-set
local-search theorem of Achlioptas--Iliopoulos--Sinclair. It accommodates
dense interactions, but its transition charges are not joint event
probabilities. No applicable charge bound was obtained here. This is neither
a hardness result for the native family nor a claim that no extractor exists.

## Exact Scope

Read the supplied [RESULT.md](/Users/jaspersands/Developer/qsearch-research-work/two-component-norm-2026-10-27/RESULT.md)
and [ALL_INPUT_SCOPE.md](/Users/jaspersands/Developer/qsearch-research-work/two-component-norm-2026-10-27/ALL_INPUT_SCOPE.md).
Also read the existing [AJT review](/Users/jaspersands/Developer/qsearch-research-work/ajt-extraction-review-2026-10-27/review.md)
only to respect its boundary; no AJT re-audit or parent sequential-assignment
algorithm was attempted.

Fix an accepted h, offsets a,b, and syndrome. Write

```text
d = dim ker(M) >= e-3,       xi in F_q^d,
H_i = E_i N,                c_i = E_i t0 + (a_i,b_i),
B_i = {xi : H_i xi + c_i = 0},       rank(H_i) = 2.
```

Let n=|T| be the number of active constraints, with n<=m'=22e-1.
Here q is odd and at least 1019; the asymptotic question fixes q as e grows.
For uniform xi, every bad-event probability is exactly p=q^(-2), regardless
of c_i. Intersections have probability zero if inconsistent, otherwise
q^(-rank(H_J)), where H_J stacks the blocks indexed by J. All these individual
linear-system computations are polynomial in n,d,log q, with an explicit
finite-field representation. Enumerating exponentially many J is not.
No uniform distribution on native witnesses is required or claimed.

The supplied AG promises are retained, including A=ev L(8eP0), independent
rows of A, injective N, and distinct evaluation points away from P0.
For e>=64, the accepted h has at most 4e+6+floor(e/4) zero coordinates.
The audit does not re-prove the upstream curve/adapter/offset construction.

## What The Constructive LLL Actually Requires

**Moser--Tardos.** [Theorem 1.2](https://arxiv.org/pdf/0903.0544v3)
uses independent underlying variables and their shared-variable dependency
graph, with

```text
p_i <= x_i product_{j in Gamma(i)} (1-x_j),   0<x_i<1.       (LLL)
```

It is a randomized witness finder, not generally a uniform sampler.
Dense H_i give dense variable supports; a change of kernel basis cannot
automatically remove the native obstruction below.

**Harvey--Vondrak.** [Section 1.1.1, Theorem 1.2, Lemma 2.3 and
Corollary 2.4](https://arxiv.org/pdf/1504.02044v3) replace variable resampling
by oracles satisfying both:

```text
(R1) r_i sends mu conditioned on B_i to mu.
(R2) r_i never creates a bad event at a nonneighbor of i.
```

Efficient oracles, event tests, initial sampling, and (LLL) yield an
expected-polynomial witness finder when the theorem's parameter bound is
polynomial. Abstract oracle existence is equivalent to lopsided association,
not merely pairwise independence, and does not ensure efficient construction.
The transport formulation is over the state space, here of size q^d.

Sampling an affine fiber by elimination is easy but does not establish R2.
Also, after adaptively selecting a violated event, the current state need not
have law mu|B_i; R1 is a theorem hypothesis, not an invariant of arbitrary repair.

### An Explicit, Checkable Oracle Certificate

The following is this audit's direct specialization, not a claimed new theorem.
Given an undirected candidate graph, let S_i be all nonneighbors other than i.
Compute K_i=intersection_{j in S_i} ker(H_j). The sufficient certificate is

```text
rank(H_i restricted to K_i) = 2,
equivalently rank(H_{S_i union {i}}) = rank(H_{S_i}) + 2.    (C)
```

Under (C), elimination finds D_i in F_q^(d by 2) with H_i D_i=I_2 and
H_j D_i=0 for every j in S_i. Draw U uniformly in F_q^2 and set

```text
r_i(xi) = xi + D_i [U - (H_i xi + c_i)].
```

On B_i this is xi+D_i U. Since F_q^d=ker(H_i) direct-sum image(D_i),
it satisfies R1; it preserves every nonneighbor pair, giving R2.
For a supplied graph all certificates/oracles are computable in polynomial
time. With maximum degree Delta and exp(1)*(Delta+1)<=q^2, (LLL) has a
symmetric certificate, so the cited algorithm is an explicit Las Vegas
poly(n,d,log q) witness finder. It is not a uniform sampler or a deterministic
extractor. Finding a suitable graph is not provided by this test.

Crucially, (C) concerns the **entire nonneighbor set**, not each small subset
separately. A guarantee rank(H_J)=2|J| for |J|<=L cannot be substituted when
|S_i|>L-1.

## Native Obstruction To Sparse Value-Preserving Resampling

For any nonzero v in F_q^d, Nv specifies two functions in L(8eP0), at least
one nonzero. That function has at most 8e zeros among the evaluation points.
Consequently the pair-evaluation change has support at least

```text
D0 = n-8e >= 10e-7-floor(e/4).                             (D)
```

This follows from the pole-degree bound, without MDS or generic-divisor
assumptions. In particular, fixing the pairs on more than 8e active
coordinates fixes xi completely. Any oracle preserving all nonneighbor
pairs and satisfying R1 therefore needs

```text
degree(i) >= n-8e-1 = D0-1 = Omega(e).
```

This applies even to nonlinear oracles if they preserve those pair values.
It also obstructs ordinary shared-variable Moser--Tardos graphs in **every
linear kernel basis**: each nonzero basis direction affects at least D0
events, and each event depends on some basis direction.

For the fixed-D_i oracle above, if every pair of coordinate blocks has joint
rank four, every j with H_j D_i!=0 must actually be a neighbor even under
the weaker no-new-bad-event rule R2. Indeed choose u with H_j D_i u!=0;
joint rank four supplies an x in B_i with H_j x+c_j=-H_j D_i u!=0.
Resampling with U=u creates B_j. Thus stronger pairwise ranks do not rescue
the sparse graph of this natural oracle.

Even asymmetric (LLL) weights cannot fix an unbounded minimum degree delta:
choose the smallest x_i=x. Then necessarily

```text
q^(-2) <= x(1-x)^delta <= delta^delta/(delta+1)^(delta+1).
```

The right side tends to zero. Hence these graphs cannot certify fixed-q
asymptotics through (LLL). A complete-graph fallback is no improvement:
its Shearer polynomial is 1-n/q^2, returning the union-bound threshold.
This does **not** rule out a different, state-dependent oracle that changes
many nonneighbor values without creating their zero pairs, or all stronger
LLL/local-search analyses.

## Decisive Dependency Counterexamples

These are exact affine-pair systems over every F_q, not claimed native AG
instances. F_Q below, Q=q^2, is simply a convenient representation of two
F_q coordinates; multiplication by its constants is F_q-linear.

**Arbitrarily high small-set rank still does not justify an empty graph.**
Take independent X_1,...,X_s in F_Q, with even s, and bad events

```text
B_j = {X_j=0}, j=1,...,s;       B_0 = {sum_j X_j=0}.
```

Every s of the s+1 output blocks have joint F_q-rank 2s. Nevertheless

```text
Pr[B_0 | X_1,...,X_s all nonzero]
    = 1/Q + 1/[Q (Q-1)^(s-1)] > 1/Q.
```

To count, use a nontrivial additive character: summing it over F_Q^* gives
-1, yielding ((Q-1)^s+(Q-1)(-1)^s)/Q zero-sum tuples. The displayed strict
increase violates even the lopsided dependency condition for an empty graph,
so an empty-graph resampling oracle cannot exist. A suitable nonempty graph
can still work; this refutes the unjustified independence inference, not LLL.

**Pairwise independent rank-two events can cover the whole space.**
In F_Q^2 take B_a={Y=aX} for all a in F_Q, and B_infinity={X=0}.
Each has probability 1/Q; every two have joint rank four over F_q and
intersection probability 1/Q^2. But their union is all F_Q^2. Thus marginal
rank two and pairwise independence do not even imply existence. Extra free
dimensions do not cure this cover; this observation alone is not a native
counterexample because the AG structure adds substantial promises.

**Independence does not make full rejection polynomial.** For independent
pair blocks, avoiding n zero pairs has probability (1-q^(-2))^n. Full redraws
therefore take exponential expected time at fixed q despite an immediate
coordinatewise witness. Counts, existence, witness finding, and uniform
sampling must remain separate claims.

## One Remaining Constructive Lead: Point-To-Set Charges

[Achlioptas--Iliopoulos--Sinclair, Theorem 2.4, equations (3)--(6)](https://arxiv.org/pdf/1805.02026v4)
allows dense interactions. For explicit transition kernels rho_i and uniform
reference measure mu, treat all flaws as nonprimary and bound

```text
gamma_i^S = max_y sum_{x in B_i: transition x->y introduces every j in S}
                         mu(x) rho_i(x,y) / mu(y),
zeta_i = (1/psi_i) sum_{S subset [n]} gamma_i^S product_{j in S} psi_j.
```

The theorem gives a randomized witness algorithm for a fixed priority order
when all zeta_i<1. Polynomial time additionally needs efficient transitions,
inverse-polynomial slack and polynomial logarithmic weight bounds; here
log(1/min mu)=d log q. This is a precise conditional route, not an extractor
already supplied for these affine constraints.

**Why raw ranks do not pay its cost:** for the fixed-D_i update, every target
y has exactly one possible source in B_i,

```text
x = y - D_i(H_i y+c_i),
```

with transition probability q^(-2). Thus, for this unrestricted transition
kernel, gamma_i^S is either zero or q^(-2), according to whether some such
transition introduces S. It is not q^(-2|S|). These are maxima over target
states, not the probabilities of rare target intersections. Strong joint
ranks can actually make more of these targets attainable.

The one useful next gate for this framework is an explicit different repair
kernel plus a proved bound zeta_i<=1-epsilon on the **same native residual**,
with paid implementation and polynomial slack. No such kernel/bound was
verified in this audit. Merely renaming rank estimates as charges is invalid.

## Other Close Matches And Audit Boundary

- [Guo--Jerrum--Liu, Algorithm 6 and Theorems 24--25](https://arxiv.org/pdf/1611.01647v4)
  give exact conditional sampling in the variable model, but exactness on
  termination is separate from rapid termination. Their general runtime
  criterion includes 6*exp(1)*p*Delta^2<=1 and an additional boundary-expansion
  bound. With p=q^(-2) and the native variable-graph obstruction above, it
  does not cover fixed-q growth. The simpler extremal case requires disjoint
  events on overlapping variable supports, not pairwise statistical
  independence; joint-rank-four pairs instead have positive intersection.
- [Arvind--Guruswami, Sections 1.3 and 2.3](https://arxiv.org/html/2108.05914v1)
  explicitly study union-of-affine-subspace avoidance, but the relevant
  results are binary and include exponential algorithms and hardness.
  They provide neither a poly(n,log q) method for this odd-field family nor
  a native hardness reduction.

Primary-paper searches covered constructive LLL, resampling oracles,
point-to-set correlations, partial rejection sampling, and finite-field
subspace avoidance. The listed theorem hypotheses were inspected; search
absence is not a literature nonexistence proof. No broad AJT audit, new
infrastructure, native large instance, Git operation, UI change, or external
message was performed. Network use was limited to public literature retrieval.

Small in-memory exact checks, executed with Python and exit code zero:
over F_9, the s=2 and s=4 examples have all claimed joint ranks and conditional
probabilities 1/8 and 57/512, both above 1/9; the ten-event spread cover has
45 pair intersections of size one and covers 81/81 states. These corroborate
the symbolic counterexamples, not native scaling or solver performance.

**File from this literature audit:** REVIEW.md only. No fixed-q solver was implemented
or certified, and no claim about the parent's separate rank-expansion method
is made.
