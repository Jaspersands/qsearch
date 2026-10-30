# Rees Streaming Workspace: Conditional Resource Comparison

30 October 2026. Written scheduling argument independently checked by Ohm
and Parfit with complementary prior-art and composition scopes. Neither
found a blocking defect; Parfit's cost/schedule wording corrections are
included below. These are AI-agent reviews, not human peer review.
Not a new receiver implementation, new time bound, novelty certificate,
classical-input application or quantum speedup. The purpose is to decide
whether another regular mixed-order SDE backend removes a real blocker.

## 1. Claim And Scope

Retain the explicit finite nilpotent Lie-ring input and rank-preserving
outer reduction in UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md. The supplied
odd prime is p, actual class c<p, the full explicit input bit length is B,
and R is the additive cyclic rank of the derived subring. Coordinate
precision e_i*log2(p), bracket constants and oracle-label width are in B.
The hiding oracle has a separately charged implementation cost and workspace.

Conditional on the existing Rees algebra/source/conversion arguments,
the all-prime FIELD pivot method in PIVOT_POWER_SDE.md permits the same

    2^O(R log(R+2)) * poly(B,log(1/epsilon))

PUBLIC-time and original-query envelope. Total implementation time adds
Q_oracle*T_f; public WORKING space is polynomial in B and log(1/epsilon),
plus the oracle/source implementation's workspace. The model allows
intermediate measurement, discard and reset. This claim
does not require a new regular mixed-order pivot solver or the p^a-state
small-prime subset table. It changes the workspace justification, not the
already proposed input coverage or time dependence.

For a copy-only interface, specify streaming delivery of fresh independent
coset copies and efficient public controlled group actions. The one-copy
transport channel in REES_COPY_ONLY_OUTER_REDUCTION.md can supply each
outer local restriction/quotient using a flattened public section. It does
not reconstruct a hiding-function oracle. An exponential bank delivered
and physically held at the outset is NOT polynomial total storage merely
because only a few copies are actively used. Non-IID banks require the
separate established joint-source contract; one-copy marginals do not suffice.

This is an adaptive quantum instrument with a polynomial-size live
workspace, not a claim that deferring every measurement and retaining all
environment/history registers produces a polynomial-width unitary circuit.
Discarded transcripts are genuinely discarded, not stored in an uncharged
coherent history. No source-preparation inverse is used.

## 2. Local Field Core

On a local p-torsion field section, compute its derived dimension r. The
outer rank proof gives r<=R and actual local class c0<=r+1, with c0<p
inherited from the original input. The r=0 case is abelian HSP. Otherwise
set

    u=r+1, t=ceil(log2(u+2)), M=8*u*t.

The field pivot theorem uses a fixed pilot and suffix of M/2 columns
each. Every central support rank is at most u-1 and each grade exponent
is at most u. It supplies a conditional one-output tree abort bound
strictly below1/16 with an explicitly paid finite classical attempt cap.
This works for all p compatible with c0<p; no small-prime group table is
inserted into this local core.

An arithmetic trial stores only the current power-valued suffix proposal,
pivot coefficients and counters. Rejected proposals are overwritten;
root work starts only after an accepted coefficient vector. No field,
candidate or full trial-history table is required. The bit length of the
attempt cap and root/bit caps is polynomial in u and input precision.
The separately recorded source bad-bank and arithmetic failures retain
their meanings. A finite witness does not certify the IID source law.

## 3. Depth-First Source Schedule

Consider a uniform-arity M tree with D=c0-1 merge levels. Generate each
child subtree to completion before starting the next child. Retain its
one output state, discard its completed classical working records, then
generate the next child. Once all M child states are present, execute
their central measurement and the bounded classical controller. A rejected
classical coefficient trial reuses those same measured quantum registers;
it does not prepare new children.

If a node aborts, abort its entire attempted output tree, discard its
retained states and charge every source already acquired. A later retry
starts a wholly fresh tree. Incomplete children are not silently reused.

Let L_D count live subtree OUTPUT tokens, excluding the polynomial local
instrument scratch and the currently constructed leaf's internal scratch.
Then

    L_0=1,
    L_D=max(M,L_(D-1)+M-1)=1+D*(M-1).

For nonuniform arities, the same recurrence gives one plus the sum of
(M_j-1) along a deepest path. This is not the leaf count M^D, nor a claim
that each group token is one qubit. Multiply by the largest canonical
group-register width and add local ancillas, labels, frame data and public
arithmetic workspace. Those widths are polynomial in B and u; u<=B.
The current central instrument may hold its address/output token alongside
all M targets, adding another constant number of such tokens.

Why may records be discarded? The existing conversion premise says that,
for EACH accepted complete record, the child output is the SAME intended
coset state, independent of that record. Thus its accepted joint output is
that state tensor a subnormalized classical record distribution. Tracing
the record preserves the child state, and independent fresh successful
subtrees provide the promised product source at their parent. Mere equality
of one-register marginals would not justify this step.

The physical schedule does not regenerate a child from its record, copy
an unknown child, run a source inverse or replace a consumed state by a
classical description. The retained child token is held until the parent
consumes it.

## 4. Whole-Run Readout And Precision

Use the existing cap of4m independent whole-tree attempts to obtain m
successful terminal states, where m is polynomial in local dimension and
log(1/epsilon). Immediately Fourier-measure each successful terminal
abelian state and update an incremental row-echelon basis. Storing m
quantum outputs is unnecessary. Fewer than m successes at the cap is
ABORT, with all failed-tree source costs retained. This changes neither
the exact independent-sample law nor the existing spanning-error bound.
Do not stop collecting samples merely because the observed basis has
stopped growing; retain the predetermined m-success target.

The full execution may contain exponentially many operations in R, but
its bounded count Q_prim of ALL relevant primitive/instrument invocations,
not just original-oracle queries, has

    log Q_prim=O(R log(R+2)+log(B+2)+log(1+log(1/epsilon)))

up to the polynomial arithmetic/precision overhead already included in
the time envelope. Uniform primitive synthesis uses accuracy of order
epsilon/Q_prim, requiring polynomially many precision bits, not Q_prim
ancillas. Generate the bounded schedule and individual gate descriptions
on demand; do not materialize an exponentially long gate list in memory.
Keep the complete flagged-channel error allocation from
REES_UNIFORM_INSTRUMENT_COMPILATION.md. Depth-first execution and record
discard are CPTP operations, so the ideal-prefix hybrid remains applicable.
No accepted-branch error is divided by a success probability.

The classical controller retains only a polynomial-depth recursion stack,
local labels/weights and bounded counters. The algorithm does not need a
chronological list of every measurement outcome or rejected coefficient
trial as an OUTPUT. Requiring such an audit transcript would change the
output specification and its unavoidable storage requirement.

## 5. Outer Ring Reduction And Copy Transport

The ring-to-field proof has at most b(b+1)/2 local calls, where b=sum e_i
is bounded by B. Run them sequentially, retaining the current known hidden
subring, normalizer, canonical module maps and previously established
public reconstruction data. All are polynomial-bit objects under the
existing HNF/SNF and bounded-coordinate arguments. Do not unroll all
local solvers or keep their successful quantum outputs simultaneously.

For ordinary access, compose local representative maps into a forward
map to the original group, make one original oracle call, and clean the
public scratch. For copies, use the same representative in the existing
controlled right-action transport channel, consuming one fresh original
copy per requested local coset source. Known K<=H and normality in the
CURRENT normalizer are still mandatory. Neither a section homomorphism
nor a reusable f oracle is supplied by this channel.

Allocate errors across the bounded number of local invocations by the
existing first-error argument. The logarithmic precision increment and
sequential public module work preserve polynomial workspace. This is a
composition claim about specified interfaces, not a new implementation of
the outer quantum normalizer procedure.

## 6. Research Decision And Falsifiers

A nonzero-pivot regular variant may remove the p^a table in the DIRECT
mixed-order route. It is not automatically needed for polynomial working
space in the full explicit-input route above. Compare complete algorithms,
not just two local backends. Known arbitrary-input SDE algorithms also
have different guarantees from this IID-bank argument; their sufficient
arities are not lower bounds on what is possible.

There is also a simpler local comparator. The existing small-prime subset
schedule has suffix length L=O(u log u), including its confidence budget.
Enumerate its2^L Boolean masks, retain one current residue sum and mask,
and stop on the same target completion predicate. This requires polynomial
workspace and2^O(u log u) work per node, hence the same overall parameter
class. It succeeds on exactly the banks on which COMPLETE DP can find a
completion, although the first returned witness need not be identical.
Its reserved prefix gives the same regularity. This is a brute-force
upper bound used to reject an unnecessary backend, not a practical or
novel algorithm. The existing DP may be much faster in finite regimes.

The published arbitrary-input SDE comparison is also important:
[Ivanyos--Santha, Theorem11 and Section3.3](https://arxiv.org/html/1503.09016v2#S3.SS3)
gives a sufficient polynomial-in-rank arity at fixed degree. Pivot rejection
instead has exponential rank dependence, but needs a smaller IID bank.
Neither dominates in every regime, and applying the pivot promise to
spanning-conditioned sums of arbitrary atom blocks is unjustified.

Before implementing another regular solver, require a specific advantage
outside the existing outer-reduction contract, or a concrete use of the
direct mixed-order instrument. The immediate native-application and
prior-art obligations are not resolved by a workspace observation.
The next constructive priority is the existing weak-input geometric
conversion problem, not another SDE controller; see
WEAK_SIEGEL_CONVERSION_AUDIT.md and SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md.
That geometric route uses a published degree-two polynomial-graph primitive,
not the Rees core. It cannot be advertised as a distinctive Rees application.

Decisive falsifiers of the scheduling claim include:

- A supposedly finished child retains hidden-subgroup-dependent record
  correlations needed by its parent rather than the stated pointwise
  product-output property.
- A local instrument needs simultaneous access to the raw leaves of a
  child, not only its retained output state and public arithmetic.
- A source interface can only deliver a jointly correlated batch, or
  requires an uncharged inverse/retained purification to deliver new copies.
- A primitive's required workspace grows with its total trial count,
  rather than with current operands and logarithmic counters.
- The input requires fully coherent deferred measurement/history output
  instead of the specified measured, discardable-record computation.

No finite scheduler simulation or passing arithmetic suite would prove
those quantum interface premises. They must be checked against the actual
source/conversion theorem; this pass does not manufacture a hardware claim.
