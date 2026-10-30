# An Isotropic Birthday Attack On The Same Orthogonal HSP

2026-10-23. **Proposed classical algorithm and local proof; independent
review pending.** This replaces the weaker generic classical baseline for
the preceding quantum proposal. It does not establish a new quantum result.

## 1. Problem And Improvement

Use the SAME oracle f on O+(2n,q) or SO+(2n,q), hiding the FULL stabilizer
of a maximal totally singular L. Labels can be arbitrary opaque names;
the attack uses only equality. Here n>=3 and q has odd characteristic.
The mathematical algorithm works over an effective finite field. Executable
controls currently implement prime fields.

The old birthday attack sampled the full line probe and cost
`poly(n,log(1/epsilon))*q^((n-1)/2)` expected queries. The refined attack
below costs

    poly(n,log(1/epsilon))*q^((n-2)/2)

queries and expected polynomial overhead per query, with the same order
of exponential storage. This matches the new classical lower bound's
q-and-n exponent up to polynomial factors. No classical polynomial-time
dequantization of the opaque problem follows. No best-possible claim for
natural explicitly encoded inputs follows either.

## 2. Restrict To A Random Maximal Singular Subspace

For a public nonzero singular e outside L, the preceding probe lemma gives
an abelian group E_e(W), with W split orthogonal of dimension 2r, r=n-1,
and hidden kernel T maximal totally singular of dimension r. Select a
uniformly random maximal totally singular A of W, of dimension r.

The two components of maximal singular subspaces have equal size. For
fixed T, the parity of dim(A intersect T) is constant within each component
and different between them. Thus at least half of all A have

    K=A intersect T nonzero.

On such A, w -> f(E_e(w)) has at most q^(r-1) cosets. This is smaller by a
factor q than the unrestricted probe's q^r cosets. All restricted query
matrices are legal original group elements. No oracle extension or hidden
coordinate map is supplied.

## 3. Uniform Sampler Without An Unanalysed Group Walk

In a standard split space of rank r, choose a uniform nonzero singular e0
using the preceding exact sampler. Construct a public hyperbolic complement
W0 and choose a uniform maximal singular subspace there recursively.
Return its span together with e0. The base r=1 has the two singular lines.

For every e0, maximal singular spaces containing e0 correspond bijectively
to those in W0. Every maximal singular space contains exactly q^r-1 choices
of nonzero e0. Hence induction proves uniformity, including equal component
weights. A finite histogram is not the justification.

Public complement construction does not require finding the hidden T.
In the standard ambient split space take its KNOWN coordinate maximal
space L0. For the current probe, let

    A0 = W0 intersect span(L0,e0).

It is a known maximal singular subspace of W0. If e0 belongs to L0, one
dual-orthogonality constraint removes its e0 direction. Otherwise, first
restrict L0 to e0-perp and project along e0 into W0. Either description
gives dimension r-1 and zero quadratic form. Solve public linear equations
for its dual basis in W0 and subtract half the dual Gram matrix to make
the duals singular. This supplies the public hyperbolic coordinates used
by the recursive sampler. There is no hidden maximal-subspace argument in
the controller.

## 4. One Collision Gives An Unbiased Hidden Direction

Take distinct uniform parameters in A until the first equal oracle labels.
The nonzero difference lies in K, hence T. Parameter repeats are discarded
BEFORE queries; they are not informative collisions.

Write N=q^r and k=|K|>=q. Conditioned on no collision after i parameters,
there are i(k-1) forbidden unused points. The probability of no nonzero
collision among m distinct parameters is therefore

    product_{i=0}^{m-1} (N-i*k)/(N-i),

until a factor reaches zero. It is at most

    exp[-m(m-1)(k-1)/(2N)].

Set `m=min(N,3*ceil(sqrt(q^(r-1)))+1)`. If m=N, a nonzero K forces a
collision. Otherwise the exponent is at least 3 because k>=q>=3.
Therefore collision success conditional on K nonzero is at least 3/4.
An unconditional round succeeds with probability at least 3/8.

Given success, the output direction is uniform on T minus zero. To see
this, use the stabilizer of T in O(W). It acts transitively on the nonzero
vectors of T through its GL_r Levi factor. The uniform A distribution,
uniform ordered distinct parameters, and first-equality stopping rule are
equivariant under this action. The stopping rule does not inspect the
numeric label names. Thus the successful-output distribution is invariant
under a transitive action and must be uniform. This reasoning would FAIL
for an arbitrary nonuniform family of coordinate restrictions or a rule
that inspected the label encodings.

## 5. Complete Kernel And Full Recovery

Repeat independent rounds and span the successful outputs. Given a proper
current span S<T, a uniform nonzero T vector lies outside S with probability
at least 1-1/q >=2/3. Therefore each round, while incomplete, increases
rank with conditional probability at least (3/8)*(2/3)=1/4.

A bounded schedule uses R rounds with

    2^r * (7/8)^R <= delta.

Indeed, dominate progress by Bernoulli(1/4) variables, continuing fictitious
progress after completion. The exponential-moment bound on the chance of
fewer than r increments is at most the displayed expression. Independence
of the actual increments is not assumed. Hence
`R=O(r+log(1/delta))` suffices, with a hard oracle-query cap R*m and storage
O(m) field vectors and labels per round. Distinct-parameter rejection and
uniform-bit sampling have expected polynomial overhead; no worst-case
wall-clock guarantee is being claimed for the reference RNG.

Apply this learner to each of three fresh public probes and use the
existing intersection reconstruction and exact certificate. A good triple
has independent classes modulo L, hence every probe is outside L. It
occurs with probability greater than 1/3. With B independent triples,
geometric failure is at most (2/3)^B. Taking each kernel failure allowance
delta<=epsilon/(6B), and B with (2/3)^B<=epsilon/2, gives overall failure
at most epsilon by a union bound. Bad triples, including e in L, can be
discarded. The certificate prevents a wrong candidate from being accepted.

Every incomplete learned span is reported as incomplete and causes a new
triple, not a claim of recovery or an uncharged restart. The execution
adapter has an explicit safety limit to avoid starting an exponential
classical run by accident. Fixed default attempts/error bits are reference
settings, not a claim of arbitrarily small error without rescheduling.

## 6. Adversarial Checks And Remaining Scope

- This beats the previous birthday baseline by sqrt(q), not by hiding full
  table construction or giving the attack the secret T.
- Uniformity of the isotropic sampler is proved by incidence and checked
  exactly at rank two. Higher-rank correctness is not a histogram claim.
- Uniform successful directions use the group action on the FULL random
  experiment. Uniformity inside one fixed intersection alone is insufficient.
- The full-kernel promise requires e outside L. The final exact certificate,
  not that unobservable promise, controls acceptance in the full algorithm.
- No restrictions on classical query adaptivity or extra computation are
  introduced. All calls go to the original oracle, also for SO inputs.
- The finite field may be fixed or growing. The attack still needs
  exponential queries in n at fixed q; finite successes do not dequantize it.
- No novelty claim is made for isotropic incidence or birthday techniques.
  The improvement is a stronger matched comparator for this proposal.

The next work should not optimize this baseline's finite constants. The
independent Rees review is a separate task. For the orthogonal proposal,
independent proof/prior-art review and a useful actual input source remain
more valuable than extra opaque-label benchmarks.
