# Field Core: Constructive Bottleneck And Next Step

30 October 2026. Focused read-only assessment, except for this note. No
subagents, commits, installs, network writes, outreach, or receiver execution.
The parent owns the newly proposed witness-only selector calculations; this
note records its interface and priority without repeating those calculations.

## Decision

**The missing general diagonal implementation is a reproduction dependency,
not the most consequential open primitive.** The implemented random/unit
policies already buy small source banks, but do not buy polynomial classical
time at growing rank. Conversely, implemented arbitrary-input solvers already
give polynomial rank/time bounds above a degree-only field cutoff. At fixed
class, the remaining prime range is bounded and has published alternatives.

**The highest-impact candidate is an efficiently implementable, invariant,
complete witness-only all-grade selector.** It could change the sequential
source-product theorem while preserving noncentral character coherence.
Existence, efficient construction, and its complete quotient-channel identity
remain open. Solving classical moment equations alone does not provide it.

This assessment uses the manuscript review brief and Argon disposition,
the whole-grade and random-column bounds, the small-prime subset note, and
the latest ring-to-field reduction. The latter supersedes direct mixed-order
receiver work as an end-to-end priority. None of the inherited Rees claims
is independently proved or promoted here.

## 1. Exact Implemented Arithmetic Split

For original grade d<=c<p, first set g=gcd(d,p-1). Let a be the equation
rank, or a public upper bound used to schedule the bank. An unconditional
Rees schedule can use r_d=dim gamma_d(L). The intrinsic character rank may
be smaller, but the observed rank of one bank is not an upper bound on
unseen source support. Put

    H_g = 16*g^(2*g+2),
    J_g = 4*((g-1)*(g-2))^2.

The live dispatch in `theorems/weighted_two_erasure_cascade.py`, functions
`required_bezout_arity` and `solve_bezout_sde_weights`, has this coverage:

| Reduced-degree/prime regime | Sufficient columns for arbitrary input | Current arithmetic |
| --- | --- | --- |
| a=0 | 1 | Immediate nonzero witness |
| g=1 | a+1 | Linear dependence and zero-guarded Bezout lift |
| g=2, p=3 mod 4 | (a+1)^2 | Implemented quadratic/conic solver |
| g=3 | (a+1)(2a+1) | Implemented cubic curve solver, all relevant primes |
| g>=2, p>=H_g | (a+1)((g-1)a+1) | Implemented symmetric solver; bounded-randomness variant available |
| odd g>=5, J_g<=p<H_g | product over j=0,...,g-2 of ((g-1)^j*a+1) | Implemented exterior fallback |

The exact uncovered positive-rank dispatch cases are therefore:

- g=2, p=1 mod 4, p<1024;
- even g>=4, p<H_g;
- odd g>=5, p<J_g.

These are **implementation domains**, not impossibility statements. The
small-field conic/cubic/exterior implementations have capped declared
sampling but retain backend-clock obligations. Do not identify them with
the fully bounded symmetric wrapper or an emitted quantum receiver.

For uncovered cases, the manuscript can import

    B_g(a) = [g^(g*(g-1)/2)*(a+1)^g]^ceil(log2(g+1)).

The published general algorithm is deterministic and polynomial in its
input arity and log p for fixed g. Its quadratic special case already
achieves (a+1)^2 for every odd prime, so the first gap above does not need
the full general construction. These are published algorithms, not new
mathematical primitives. [Ivanyos--Santha, Proposition 9, Theorem 11 and
Section 3.3](https://arxiv.org/html/1503.09016v2).

`theorems/span_regular_sde.py:published_sde_arity` only calculates B_g;
`published_bound=True` explicitly reports an imported, unimplemented
backend. For example B_4(2)=36,520,347,436,056,576. This is a chosen
sufficient atom count, not a necessary number of field sources or ring
queries. Its extra spanning-block/pilot factors are not required by the
preferred ring-to-field route.

In particular, implementing that general solver does NOT solve an arbitrary
bank of only 4(a+1) columns: its stated arity guarantee must still hold.
Nor does a bank below B_g require failure; supported local solvers, special
relations, and random-input methods can use fewer columns.

## 2. Source Counts Are Not Total Time

Write r=dim[L,L], u=max(c,r+1,2), and
m=n+ceil(log2(3/epsilon)). In a genuine nonabelian field algebra c<=r+1,
so u=r+1. The following counts refer to independent lifted sources before
the initial factor c of original oracle calls/copies.
For the direct-module comparator rows, use their cyclic rank R and
u=max(c,R+1,2); the original ring need not satisfy c<=R+1.

| Route | Source branching | Classical bottleneck |
| --- | --- | --- |
| General fixed-degree SDE | P=product B_(g_d)(r_d) | Polynomial in r, log p at fixed c; imported general backend |
| Supported symmetric/cubic/quadratic stages | Each nonlinear arity O_c((r_d+1)^2) | Polynomial at fixed c, subject to the stated clock dependencies |
| Field random kernel, p>=16u^2 | M=4u; P=M^(c-1); 4m attempted trees | Per nonlinear node K=4*g^M*ceil(log2(64P)) kernel trials |
| Direct unit-module tree, p>=16u^2 | 8u slots per grade, INCLUDING 4u pilots | K=2*(2g)^(4u)*B per node, plus roots/lifting |
| Direct small-prime subset tree, p<16u^2 | W<=16u*ceil(log2(16u)) per grade | Up to p^R residue states per node |

The random field schedule pays exactly 4*c*m*(4u)^(c-1) original inputs.
At fixed c this is polynomial in r, but its prescribed nonlinear search
budget is exponential in r. The unit policy is no cure and adds a
full-support condition unnecessary after reduction to the field. The
subset policy avoids exponential additive-exponent cost, not exponential
rank cost. Its pilot-based counts are a conservative available field
specialization too, not an optimal field-source prescription.

**Consequences for the requested regimes:**

1. For the conditional `2^O(r log(r+2))*poly(input)` theorem, general SDE
   is unnecessary: random columns handle p>=16(r+1)^2; the imported quantum
   small-commutator algorithm handles smaller p. Neither that fallback nor
   the full receiver is implemented. On ring sections use the LOCAL field
   derived rank, not the original commutator order or original ring class.
2. For fixed c and unrestricted growing r, random/unit/DP bounds alone
   do not establish polynomial total time. Their exponential terms are
   polynomial in full input length I only in restricted regimes: the
   displayed exponential factors require M*log g=O(log I) for the random
   field budget, 4u*log(2g)=O(log I) for the unit budget, and
   R*log p=O(log I) for the full DP budget. These are cost tests for those
   prescribed budgets, not hardness thresholds or lower bounds on actual
   instance runtimes.
3. Above H_c=16*c^(2*c+2), every grade has an implemented polynomial-rank
   arithmetic branch, with P=O_c((r+1)^(2(c-1))). No general SDE import is
   needed there. In particular H_c<=p<16(r+1)^2 can reject the RANDOM
   planner while remaining covered by the SYMMETRIC planner.
4. Below H_c, p is bounded as a function of fixed c. The uncovered cases
   in Section 1 can use the published general solver, but do not logically
   require it: the published deterministic zero-sum algorithm gives
   S(p,a)=p^O(p log^2 p)*a^O(p log p) columns and polynomial time in S.
   Its Boolean witness satisfies every power degree. Thus symmetric
   large-prime arithmetic plus this bounded-prime import supplies another
   fixed-c polynomial schedule. This is a deduction, not an implemented
   fallback. [Imran--Ivanyos, Theorem 2](https://arxiv.org/html/2304.08376v1#S5).

Hence **no source-size lower bound or new HSP coverage follows from the
absence of the general backend**. Its implementation would realize the
historical schedule in unsupported branches. A source-saving theorem needs
something stronger than substituting one already-published algorithm.

## 3. Falsifier For A Cheap Random-Sampler Fix

The exponential rejection cost is not merely a pessimistic lower bound
on success. Here is a separate proved deduction about this sampler, not
a lower bound on other algorithms.

Condition an IID a-by-M matrix A on full row rank and draw w uniformly
from ker A. Its kernel is a uniform (M-a)-dimensional subspace. Conditional
on w!=0, the marginal w is uniform over all nonzero vectors of F_p^M.
For h=(p-1)/g and S=(powers including zero)^M minus {0}, this gives

    E_A Pr[w in S | A]
      = (1-p^(-(M-a))) * ((h+1)^M-1)/(p^M-1).

For K fresh uniform-kernel trials on the SAME bank, the average chance of
ever hitting S is at most K times this expression, by a union bound.
For fixed g>1, M=Theta(r), p>=16(r+1)^2, the expression is exp(-Omega(r)).
Polynomially many such trials cannot supply a constant-success algorithm.
For full-support unit witnesses replace the numerator by h^M, making
the test stricter. This does not rule out a structured search algorithm.

In-memory exact rational evaluation at p=998244353, g=4, a=32, M=132
gave log2(mean hit probability) approximately -264; K=M^3 gives a success
upper bound approximately 2^-242.87. This is an arithmetic check of the
displayed identity, not random-instance benchmarking or quantum execution.

## 4. Highest-Impact Open Primitive: Witness-Only Selection

The parent's new target is not covered by
[the premature-measurement obstruction](../../REES_PREMATURE_GRADE_MEASUREMENT.md).
That obstruction assumes individual noncentral labels have already been
measured. A selector retaining cross-character coherence is expressly
outside its scope. Conversely, avoiding that obstruction is not a proof
that a selector exists.

For the parent's class-three filiform/Rees test, fix top labels ell_i and
spectator labels beta_i. The supplied action on the unmeasured labels is

    alpha_i -> alpha_i + t*s_i*ell_i.

A nonzero witness s must satisfy

    sum s_i^3*ell_i = 0,
    sum s_i^2*beta_i = 0,
    sum s_i^2*alpha_i = 0.

The parent identifies invariance of the last solution hyperplane for a
FIXED valid s. The outstanding constructive object is a collection of
nonnegative weights, supported on valid witnesses, with BOTH

    sum_s w_s(alpha) = 1,
    w_s(alpha+t*(s_i*ell_i)_i) = w_s(alpha)  for every t.

This is an invariant partition of unity, not an ordinary SDE witness
finder. Uniform weighting over the witnesses at alpha is not justified:
its normalizing count can change along the s-dependent action. Reversible
evaluation of a conventional label-dependent solver does not by itself
repair this problem; measuring its chosen witness can still distinguish
characters whose coherence is needed.

**Completion contract:** construct a uniform polynomial-cost dilation of
the witness-only Kraus operators, with a paid bank size and finite precision;
uncompute all scratch that could leak individual alpha; and prove the
complete quotient-channel identity for the promised hidden inputs. Positive
square-root amplitudes avoid adding arbitrary phase choices, but the
displayed X-action invariance alone does not establish intertwining for
all required actions or the whole channel. Explicit aborts are acceptable
only with an unconditional, paid failure bound. An exponentially large
weight table or exponentially rare successful postselection is not a
completion.

If such an instrument converts ONE common M_joint-source bank directly
to the required terminal quotient state, its source factor becomes
M_joint, instead of the sequential P=product M_d. With constant-success
paid restarts this means O(c*m*M_joint) original inputs rather than
O(c*m*P). A certified M_joint<P with matched polynomial total time would
change the resource theorem. No value of M_joint, linear-arity claim, or
rank-growing extension is established here. A lone filiform finite control
would not establish those claims either.

This is the research priority over general-solver wiring. The weaker
alternative, a polynomial-time IID SDE finder on linear-size banks, would
also improve the time/source tradeoff but would retain sequential stages.
The existing random sampler and its second moment do not supply it.

## 5. Falsifier, Novelty Boundary, Next Action

**Selector falsifier, parent-owned:** an admissible bank for the proposed
complete contract with no invariant normalized nonnegative weight family
(an exact infeasibility certificate suffices), or a constructed selector
whose accepted complete channel differs from the target quotient density.
Failure of uniform-over-witness weights only falsifies that normalization,
not every witness-only selector. Likewise, an aborting proposal must be
judged against its promised source-distribution failure budget, not against
an adversarial record it explicitly pays to reject.

**Novelty boundary:** fixed-degree SDE, quadratic/class-two HSP, bounded-
prime zero sums, and exponent reduction are prior art. The ring reduction
adds no reason to revisit general-exponent receiver machinery here. A new
selector could improve the conditional field resource theorem; it would
not itself provide a natural input oracle, classical hardness, or a useful
application-level quantum advantage. No toy oracle separation is offered.

**Next action:** finish the parent's class-three invariant-completeness
decision before coding a receiver: obtain either a constructive succinct
weight rule with a polynomial-cost coherent implementation, or an exact
obstruction to the stated selector class. Only after that decision pursue
the full-channel identity and a scalable paid source bound. Do not use a
general SDE port, fresh small benchmark, or another ring budget as a proxy
for this missing instrument.

Verification scope: inspected the named notes and solver dispatch/source
budget code; checked the two primary papers above; performed only the
in-memory rational calculation in Section 3. No repository tests, Lean
builds, generated reports, or parent selector calculations were run. Only
this assigned review note was created.
