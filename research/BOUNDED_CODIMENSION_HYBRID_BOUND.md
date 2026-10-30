# Bounded Codimension: A Hybrid Parameter Bound

30 October 2026. Conditional composition of existing repository arguments,
not an independently established quantum algorithm, novelty claim, practical
advantage, or new native application. The exact resource certificate does
not execute a hidden-subgroup solver. An independent automated reviewer
checked the composition and its input/error contracts; this is not human
review, formal verification, or a certification of the underlying receiver.

## Result And Premises

Supply an explicit n-dimensional nilpotent Lie algebra L over an odd prime
field F_p, with ACTUAL class c<p, and an ordinary coherent fixed-width
oracle hiding H=exp(h) in exp(L). Promise codim(h)<=k, 0<=k<=n. The task is
to recover a basis of h. All structure constants, group arithmetic, oracle
evaluation and label width are part of the input/cost model.

Conditional on pointwise/source correctness of the growing-class whole-grade
Rees receiver, the [uniform compilation derivation](REES_UNIFORM_INSTRUMENT_COMPILATION.md),
and the already written
[abelian-ideal reduction](BOUNDED_CODIMENSION_HSP_REDUCTION.md), there is a
bounded-error algorithm with both oracle calls and non-oracle operations
bounded by

    2^O(k^2 log(k+2)) * poly(n, log p, label width, log(1/epsilon)).

For an actual oracle evaluation cost T_f, the implemented running-time
bound is `T_nonoracle + Q*T_f`. Label width alone does not bound T_f.
Correctness of a fixed-class receiver alone would not establish the
growing-class uniformity used here. The compilation follow-up derives this
uniformity from public reversible arithmetic and uniform arbitrary-modulus
QFTs; it is no longer an extra unspecified receiver-efficiency premise.
The certificate includes its terminal primitive counts. This remains a
written argument, not an emitted or formally verified quantum circuit.

This improves the previous sufficient `2^O(k^3 log(k+2))` parameter factor.
For a sufficiently large prime the factor is instead `2^O(k log(k+2))`.
The all-prime statement uses a CLASSICAL branch where its sufficient cost
is smaller; it does not extrapolate the large-field SDE construction.
The split is a simple valid policy, not a pointwise optimal selector.

This is an ordinary-oracle statement. Copy-only input does not supply the
classical collision queries or the abelian subgroup restrictions for free.
No arbitrary black-box growing-class presentation conversion is assumed.
The actual class condition is still required even on the classical branch.

## 1. Split On Public Parameters

For k>=1 set

    P_k = 16*(2k)^(4k+2).

If p<P_k, use the classical collision learner in Section 2 on the ORIGINAL
instance. If p>=P_k, use the abelian-ideal reduction and whole-grade Rees
solver in Section 3. For k=0 the promise already says h=L, so no oracle
query is needed. These comparisons use integer arithmetic, not floating
logarithms or a scan through field elements.

The large-field threshold is deliberately conservative. Actual reduced
degrees gcd(d,p-1) can allow a cheaper whole-grade route below this cutoff.
Known abelian/nil-2 algorithms can also be preferable for k<=2. None of
these improvements is needed for the stated universal bound.

## 2. Classical Collision Learner With A Paid Clock

Let J=[G:H]<=I=p^k. Choose independent uniform elements of G using the
given Lie coordinates. A batch of

    B = floor(sqrt(2I))+2

has a repeated f-label with probability at least one half. If B>J this is
certain; otherwise its no-collision probability is at most
`exp(-B*(B-1)/(2J)) <= exp(-1) < 1/2`. Use sorting or a dictionary on the
fixed-width labels, not quadratic comparison of every pair.

Select a pair of DISTINCT SAMPLE INDICES by labels and indices alone,
for example the first repeated label. If x and y share a left H-coset,
output x^-1*y. Conditional on the whole label sequence, x and y are
independent uniform elements of that coset. Therefore x^-1*y is exactly
uniform in H, including the identity. This also holds for nonnormal H.
Do not reject x=y or choose a pair by its coordinates: those changes can
alter the uniform law. The failure/success flag depends on labels only.

Use fresh independent batches for every attempt and requested output.
Write ceil_log2(x) for the least nonnegative integer a with 2^a>=x. Set

    t = n + ceil_log2(3/epsilon),
    a = ceil_log2(3*t/epsilon),
    Q = t*a*B.

For each of t requested hidden elements allow at most a batches; abort
if all fail. Collision exhaustion is at most t*2^-a<=epsilon/3. On the
ideal uniform input process, the t outputs are independent uniform H
elements. Lazard log makes them uniform in the vector space h. Their
failure to span is at most p^(dim(h)-t)<=2^(n-t)<=epsilon/3. Ordinary
linear algebra returns the span; no unknown subgroup oracle certifies it.

Every group draw consumes n uniform field coordinates. For each of the
at most n*Q coordinates, sample `(p-1).bit_length()` fair bits, accept a
value below p, and cap attempts at

    L = ceil_log2(3*n*Q/epsilon).

Each rejection probability is below one half. A first-error coupling to
the ideal uniform process bounds coordinate-sampling abort by
`n*Q*2^-L<=epsilon/3`. Fair bits are capped by
`n*Q*L*(p-1).bit_length()`. Thus the complete algorithm has a deterministic
work cap and total failure at most epsilon; no repeat-until-success or
conditioning away discarded inputs is hidden in the bound.

The query cap is Q and working storage is polynomial in B and the public
input. Uniform BCH arithmetic is polynomial in n,c,log p, with c<=n.
Consequently non-oracle time is
`p^(k/2)*poly(n,log p,label width,log(1/epsilon))`, with Q*T_f charged
separately for oracle evaluation. Since

    log_2(P_k) = 4 + (4k+2)*log_2(2k),

the small-prime branch has factor `2^O(k^2 log(k+2))`. This is a standard
birthday upper bound with explicit sampling accounting, not a new
classical algorithm or a classical lower bound.

## 3. Retain The Terminal Class Bound

The public abelian-ideal procedure repeatedly learns the COMPLETE hidden
intersection with an abelian ideal, then normalizes and quotients it.
There are at most n strict dimension decreases. Its terminal nonabelian
algebra has dimension m<=k*(k+1)/2 and actual class c_*<=2k-1. It retains
class<p, and section composition uses ONE original query per restricted
oracle query, not one query for each previously traversed quotient.

For d=2,...,c_*, set r_d=dim(gamma_d) and g_d=gcd(d,p-1). The
[whole-grade construction](REES_FULL_GRADE_PARAMETER_BOUND.md) uses arity

    A_d = r_d+1                              if g_d=1,
    A_d = (r_d+1)*((g_d-1)*r_d+1)           otherwise.

The [symmetric contraction](POWER_SDE_SYMMETRIC_CONTRACTION.md) requires
`p>=16*g_d^(2*g_d+2)`. Here g_d<=d<=2k-1, so p>=P_k suffices at EVERY
stage. There is no assumption that d divides p-1, no full-field table,
and no failed small-prime SDE call hidden in the policy.

Since r_d<=m=O(k^2), every arity is O(k^5). There are only O(k) stages.
Thus

    product_(d=2..c_*) A_d = 2^O(k log(k+2)).

This uses BOTH bounds, on m and on c_*. Substituting only derived rank
r=O(k^2) into a generic derived-rank formula loses this improvement.
The cover has dimension at most c_*m=O(k^3); construction and arithmetic
remain polynomial in that dimension and log p.

This is also a TIME bound, not merely a source-count bound. The explicit
bounded symmetric solver has at most `g_d^O(g_d)` scalar proposal/root
work, times a polynomial in r_d, log p and failure bits. Thus each call
costs `2^O(k log(k+2))*poly(log p,log(1/epsilon))`. The number of calls is
bounded by the source forest. Multiplying these factors stays within the
same asymptotic parameter exponent. Uniform BCH computation avoids
enumerating a basis of all free Lie words.

Allocate epsilon/4 to rank failure in all preliminary abelian calls and
epsilon/4 to their complete-sampler implementation error. At most n calls,
each with at most `n+ceil_log2(4n/epsilon)` Fourier samples, suffice for
the former. This count INCLUDES a final abelian solve if the reduction
terminates at an abelian remainder of any dimension: every preceding
intersection call strictly decreases dimension, so adding that final
nonzero solve still leaves at most n calls. Such an early abelian remainder
is NOT charged to the size-bounded Rees envelope. Give epsilon/2 to the
entire size-bounded terminal receiver, if needed. Its existing
certificate splits that allowance among terminal rank, all SDE aborts,
and whole-instrument approximation. Every failed leaf and arithmetic
retry is paid. Error accumulation is across complete instruments, not
postselected successful branches.

The executable uses the upper envelope

    m_bar=k*(k+1)/2,
    c_bar=min(2k-1,m_bar-1),
    (r_1,...,r_cbar)=(m_bar,m_bar-2,m_bar-3,...,m_bar-c_bar),

with `(1,)` for k=1. It bounds every size-bounded Rees terminal lower-central
profile, not earlier abelian exits. For k=1 no nonabelian terminal is
possible; `(1,)` is a conservative placeholder that may never be invoked.
The envelope is NOT certified to be a realizable terminal input.
Its source numbers are conservative parameter certificates, not measured
resources. No input dimension or class is inferred from a generated
example.

## 4. What Would Falsify Or Limit This Result

- A flaw in the original Rees source/pointwise conversion proof invalidates
  the large-prime branch. Exact arithmetic tests cannot establish that proof.
- Incomplete learned intersections can lose hidden directions during the
  normalizer restriction. Membership of sampled hidden elements is not
  enough to certify completeness.
- A cost exponential in the numerical prime, or a polynomial exponent
  depending on k in the non-SDE arithmetic, would invalidate uniformity.
  The specified circuit arithmetic and bounded power-root routines must
  retain their existing paid interfaces.
- Reusing samples across collision batches or selecting pairs by coordinate
  values invalidates the stated IID hidden-element argument.
- A dishonest index promise, wrong group law, composite field parameter,
  or non-exact hiding labels is outside the theorem. The planner does not
  verify an unknown hidden subgroup or public group promises.
- No practical application, hardness separation, quantum execution or
  novelty certification follows. The application triage found no new
  surviving native family. Do not manufacture one to accompany this bound.

The fixed-degree diagonal solver and nil-2 algorithms are published
ingredients, not discoveries here: [Ivanyos--Santha](https://arxiv.org/html/1503.09016v2)
and [Ivanyos--Sanselme--Santha](https://arxiv.org/abs/0707.1260).
The [bounded-prime result of Imran--Ivanyos](https://arxiv.org/abs/2304.08376)
has different hypotheses. This bounded comparison is not a complete
priority search or evidence that no prior theorem subsumes the claim.

## Replay

    python qsearch.py power-sde --codimension-budget --write

Writes `research/reductions/codimension_hybrid_budget.json`. The command
evaluates exact counts and guards, not either HSP algorithm. It leaves
candidate, experiment and proof-status registries unchanged.

The [independent automated review](audits/reviews/2026-10-30-codimension-hybrid-review.md)
records its exact earlier snapshot, nonnormal collision-law control and
two exposition qualifications. The early-abelian-exit accounting and
standalone label-width charge above incorporate those qualifications.
The parent additionally replaced a quadratic comparison cap in the initial
calculator with a sorting comparison cap; its final sources are identified
by the regenerated resource artifact, not the review's historical hashes.
