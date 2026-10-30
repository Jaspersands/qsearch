# Random-Column Rees Parameter Bound

30 October 2026. Conditional derivation checked by an independent automated
adversarial reviewer, with a separate codimension/source audit. Neither
review found a fatal mathematical error; this is not human peer review,
a verified whole-HSP implementation, or a novelty certificate. See the
[review and prior-art disposition](audits/reviews/2026-10-30-random-column-rees.md).
The input model remains explicit prime-field Lie coordinates,
actual nilpotency class c<p, and an ordinary exact coherent hiding oracle.

## Scientific Question

The existing whole-grade solver handles arbitrary label columns but needs
a degree-dependent large-field guard. Actual central-character labels are
IID uniform on an unknown subspace. Can this source law replace the guard
without recursively multiplying the number of quantum inputs by classical
retry costs?

The construction below gives a conditional affirmative answer. Classical rejection INSIDE THE KERNEL
of one measured label bank costs exponentially in the research parameter,
not in log p. Quantum banks have only linearly many columns in that parameter.
Bad banks still exist and are charged. Whole-tree restart, with a fixed
global attempt cap, avoids an n-dependent per-node confidence cost in the
recursive quantum arity.

Subject to the inherited Rees dependencies, two conditional parameter bounds improve:

- Derived dimension r=dim[L,L]: `2^O(r log(r+2))*poly(n,log p,label width,log(1/epsilon))`
  for ALL primes with c<p, instead of only the previous large-field or
  fixed-effective-degree regimes.
- Hidden codimension <=k: `2^O(k log(k+2))*poly(n,log p,label width,log(1/epsilon))`
  for ALL primes with c<p, rather than the previous `2^O(k^2 log(k+2))`.

These are candidate upper bounds, not lower bounds on classical algorithms.
Both depend on the existing Rees pointwise conversion and uniform compilation
arguments. Costs inside the original oracle remain `Q*T_f` separately.
No native hard application follows, and no tiny hidden-oracle benchmark is
being substituted for that missing application.

## 1. Exact Projective Second Moment

Let d divide p-1, h=(p-1)/d, and let P_d contain zero and all nonzero dth
powers in F_p. For M columns define

    S = P_d^M minus {0},       |S|=(h+1)^M-1.

Every projective line meeting S contains exactly h elements of S. Indeed,
for nonzero v in S and a scalar t!=0, tv is in S iff t is a nonzero dth
power, as seen from any nonzero coordinate. Consequently the number of
represented projective directions is

    D = ((h+1)^M-1)/h.

Let A be a uniformly random a-by-M matrix over F_p. Choose one representative
from each of those D directions for this COUNTING argument only. The algorithm
never enumerates them. For distinct directions v,w, the pair Av,Aw is uniform
on F_p^a times F_p^a, so their zero indicators are pairwise independent.
If X counts annihilated directions, then exactly

    E[X] = mu = D/p^a,
    Var(X) = D*p^(-a)*(1-p^(-a)).

Chebyshev gives `Pr[X<mu/2] <=4/mu`. For M>a, the independent-row product
formula also gives `Pr[rank(A)<a] <=2*p^(a-M)`. Thus except on a bank event
of probability at most

    beta = min(1, 4/mu + 2*p^(a-M)),

the bank has full intrinsic row rank and a uniformly sampled kernel vector
lies in S with probability at least

    h*(mu/2) / p^(M-a) = |S|/(2*p^M).

When (p/d)^M>=2 this is at least `1/(4*d^M)`, since h+1>=p/d.
For a=0 the bank is zero and a coordinate-unit witness is immediate; no
random-bank failure is needed.

Unknown intrinsic coordinates pose no algorithmic access issue. For IID
columns in a fixed unknown a-dimensional subspace W of F_p^R, choose a
basis of W only in the proof. The intrinsic matrix is uniform and has the
same kernel as the supplied ambient matrix. Ordinary Gaussian elimination
on the ambient columns produces the required kernel. The algorithm does
not need to know a, W, a basis of a hidden intersection, or whether the bank
is good. The probability bound is NOT a guarantee for every fixed matrix.
A canonical observed bank whose rank exceeds the supplied intrinsic-rank
upper bound aborts. Noncanonical measured records likewise abort before
arithmetic; the complete policy must be defined even off the ideal source
support. These checks cannot certify that an accepted bank was IID.

## 2. Bounded Arithmetic On A Fixed Bank

Sample a uniform vector w from ker(A) by choosing uniform coefficients in
a computed kernel basis. Reject zero and any vector with a nonzero entry
outside the dth-power subgroup. For an accepted w, extract dth roots of its
nonzero entries and leave its zero entries zero. Verify the original
simultaneous equation exactly. This gives a nonzero s with

    sum_i s_i^d * lambda_i = 0.

With `K=4*d^M*B` trials, a good bank has kernel-rejection failure at most
`exp(-B)<=2^-B`. These are CLASSICAL trials on the SAME saved bank. No
additional phase states are measured or prepared. Each trial costs a
polynomial in ambient dimension, M and log p. There are at most M root
calls after the first accepted coefficient vector; root failure aborts
that node rather than launching an uncharged retry loop.

Use the existing bounded degree-d polynomial root splitter and capped fair-
bit field sampler. Choose root and bit caps so each contributes at most
2^-B to the node failure probability. Degree-d polynomial arithmetic is
uniform polynomial in d and log p. In particular, this does not inherit a
fixed-degree exponent hidden in a published solver. The sampler's d^M
factor remains explicit and can be very large.

For an original grade exponent e, use d=gcd(e,p-1), then the existing
Bezout lifting converts the coefficient roots into e-power weights. A
linear d=1 grade can use an ordinary nonzero dependence directly. Zero
weights consume their input slots but receive identity, never Delta_0.

## 3. Uniform Bank Size And One-Output Trees

Choose an integer u>=2 such that c<=u and every central label subspace has
dimension a<=u-1. Set

    M=4u,       p>=16u^2,       P_tree=M^(c-1).

Use M children at every grade, including smaller-rank grades, to keep the
bank failure probability uniform over the entire tree. For d<=u, a<=u-1,
and h>=(p/(2d)),

    mu >= h^(M-1)/p^a
       >= p^(M-1-a)/(2d)^(M-1)
       >= 2^(8u+1)*u^(2u+1).

This bound also holds for d=1, though that grade needs no random solver.
The tree has

    T_tree = sum_{j=0}^{c-2} M^j <= P_tree

merge nodes. With `B=ceil(log2(64*P_tree))`, the three capped arithmetic
failures sum to at most 3/64 over the tree. The bank contribution obeys

    T_tree * (4/mu + 2*p^(a-M)) <= 1/64,

using the preceding lower bound, P_tree<=(4u)^(u-1), and u>=2. For example,
the first summand is at most `2^(-6u-1)*u^(-u-2)` and the second at most
`2^(-10u-5)*u^(-5u-3)`. Therefore total one-tree abort probability is at
most 1/16; the looser 1/4 is sufficient below.

The arithmetic work per node is at most

    (1+d^M)*poly(n,u,log p,B).

Since d<=u and M=4u, both this and the number of nodes are
`2^O(u log(u+2))*poly(n,log p)`. Node costs are SUMMED over the tree, not
multiplied into its quantum-source branching factor.

## 4. Paid Restart And Complete-Channel Error

The pointwise central conversion is essential. Conditional on any accepted
classical label/witness record and fresh ideal child coset states, its
output is the SAME target coset state. Therefore the successful instrument
on the promised input factors as that state tensor a subnormalized record
distribution. Inductively, distinct successful child trees give independent
ideal coset states even after their success records are known. Their next
central labels retain the IID uniform-subspace law.

Union-bound each node's failure conditional on the preceding required
successes; no independence of node events is asserted. A whole successful
tree outputs the exact terminal abelian coset state, independent of its
accepted transcript. Invalid or aborted predecessors are not silently
treated as promised inputs: they make their entire tree fail.

Let `m=n+ceil(log2(3/epsilon))`. Attempt 4m independent whole trees with
fresh leaves and private coins. Keep the first m successful output states;
if there are fewer, emit ABORT. All failed-tree inputs are charged. Given
one-tree failure <=1/4, a union over subsets of 3m failed attempts gives

    Pr[fewer than m successes] <=2^(4m)*(1/4)^(3m)=2^(-2m).

This is <=epsilon/3. Final abelian Fourier sampling of the m successful
states has rank failure <=1/((p-1)*p^(m-n))<=epsilon/3. There is no n-dependent
confidence parameter inside M or B: this prevents an accidental
`(log n)^c` cost from invalidating the fixed-parameter statement.

Finally allocate epsilon/3 across the complete bounded quantum schedule,
including ALL attempted trees, their source preparations, final readouts,
records and abort flags. The previous canonical-input ideal-prefix hybrid
applies. Actual outputs need not retain exact independence or support after
approximation; closeness is measured for the whole flagged algorithm.
Do not postselect and divide by a small success probability.

The [uniform compilation argument](REES_UNIFORM_INSTRUMENT_COMPILATION.md)
uses polynomial-size arithmetic and QFTs with only logarithmic precision
overhead. Here that precision is `O(u log(u+2)+log(n/epsilon))`. This argument
proves circuit existence under the Rees hypotheses, not an emitted circuit.

## 5. Derived-Dimension Corollary

For r=dim[L,L]>=1, take u=r+1. The actual class satisfies c<=r+1 and every
central label rank is at most r_d<=r. Thus the preceding construction covers
p>=16(r+1)^2 with `2^O(r log(r+2))` parameter cost. For smaller p, invoke
the published small-commutator algorithm:
[Ivanyos--Magniez--Santha, Theorem 11](https://arxiv.org/html/quant-ph/0102014v1#S5).
Its time is polynomial in input size plus |G'|; here |G'|=p^r. Since the
remaining p are O(r^2), this is also `2^O(r log(r+2))*poly(input size)`.
It is a QUANTUM fallback, not a claim of classical HSP recovery. The r=0
case is the ordinary abelian algorithm.

This is an all-prime extension of the earlier large-field parameter bound,
conditional on the same Rees whole-proof dependencies. Neither the imported
small-commutator algorithm nor the elementary second-moment identity is
claimed as new. The composite theorem needs its own prior-art assessment.

## 6. Hidden-Codimension Corollary

Use the [existing abelian-ideal/normalizer reduction](BOUNDED_CODIMENSION_HSP_REDUCTION.md).
Hidden codimension does not increase; the nonabelian terminal has dimension
<=k(k+1)/2 and class c<=2k-1. Each central character rank is

    a_d = dim gamma_d(L) - dim(h intersect gamma_d(L))
        <= codim_L(h) <= k.

This remains true after removing higher Rees grades: the hidden grade-d
intersection is still t^d(h intersect gamma_d(L)). The ambient grade size
can be O(k^2); confusing it with the intrinsic character rank would lose
the following improvement.
The full lifted hidden codimension can be sum_d a_d<=c*k; it is NOT
claimed to remain at most k. Only the per-grade character rank is bounded.
Nor are a bank's own labels claimed to remain IID after conditioning on
its own acceptance. The next bank's IID law follows from the accepted
predecessor STATES being independent of their records.

Take u=2k and M=8k for k>=1. When p>=64k^2, the random-column tree has
`2^O(k log(k+2))` quantum source and total nonoracle cost. Preliminary abelian
calls and oracle transports retain their previously charged polynomial cost.
Split the overall error budget between those calls and the terminal solver.
When p<64k^2, the earlier classical birthday algorithm has
`p^(k/2)*poly(n,log p,log(1/epsilon)) = 2^O(k log(k+2))*poly(...)` cost.
The k=0 promise and abelian/nil-2 special cases remain separately covered.

## Falsifiers And Boundaries

- Adversarial banks need not have a power-valued nonzero kernel. At p=5,
  d=4, A=(1,1,1), all power coordinates are 0 or 1 and no nonzero triple
  sums to zero. Repeating the sampler cannot fix that bank. Only the IID
  bank analysis licenses the average failure bound.
- Pairwise independence is between DISTINCT projective directions, not
  between all raw vectors in the power cube. Ignoring collinearity gives
  a false variance formula.
- Rank-deficient banks must be charged separately when using the p^(M-a)
  kernel-size denominator. Observed rank alone does not certify the unknown
  intrinsic source rank or its distribution.
- Successful-tree state/record independence is required; correctness only
  after averaging over accepted records would not justify the induction.
- All failed trees, capped kernel trials, roots, fair bits and oracle calls
  remain paid. This is not polynomial in growing u and is not a practical
  improvement for every instance over the existing worst-case solver.
- No classical hardness, native useful source, specialist validation or
  priority claim follows from these bounds or finite arithmetic controls.

## Executable Scope

Run `python qsearch.py power-sde --random-column --write` to regenerate
`research/reductions/random_column_rees.json`. This runs the bounded
CLASSICAL fixed-bank sampler on two seeded controls and one adversarial
bank, and computes exact resource caps for four conditional Rees schedules.
It neither executes those quantum schedules nor implements the imported
small-commutator fallback. The sampler takes the reduced degree d;
original-grade Bezout lifting remains the existing controller operation.

The arithmetic API accepts canonical finite Python arrays. It now returns
an explicit ABORT for an observed rank exceeding the supplied promise.
Malformed Python arguments still raise; a future binary measurement
controller must validate its encoding and map noncanonical measured words
to ABORT before calling this API. Genuine backend errors must not be
disguised as statistical failures. No complete instrument implementation
is claimed by the helper.

The exhaustive small-field controls enumerate 881 matrices and independently
check the projective first and second moments, rank event, and good-bank
kernel density. Other tests cover deterministic branches, bounded roots,
bit exhaustion, invalid witnesses, source/error budgets and CLI write
isolation. Passing these tests is evidence about arithmetic and accounting,
not proof of the source law, full Rees theorem, or research novelty.
