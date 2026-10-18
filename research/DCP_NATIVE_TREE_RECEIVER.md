# Executable Bounded Native Tree Program

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No new speedup or novelty claim.

Run `python qsearch.py dcp-native-tree-receiver`. This completes the abstract
clean XOR-F program missing from DCP_NATIVE_TREE_MOMENT_SPEC.md. It does NOT
export X/CX/Toffoli gates or execute unknown quantum source preparations.
The interpreter operates a reversible fixed-address record schedule on basis
wires. Linearity then defines its action on superpositions; density controls
separately test the existing reciprocal six-call instrument.

## Construction

Use n=b(a+1) components, k=2^a disjoint physical blocks and L=4^b fixed,
distinct nonempty supports per leaf. The default block size is4b and support
weight is the least w with binom(4b,w)>=L. Each leaf record contains its
physical support ID and its componentwise signed sum in Z4^n. Packing is an
injective comparison-key encoding only, never the group addition operation.

At nonroot level r, visit EVERY pair of fixed child slots. A candidate is
valid exactly when both children are valid and their signed sum vanishes on
chunk r. Generate invalid sentinels for failed candidates. A fixed bitonic
network sorts by (invalid,support ID,packed value), keeping every compare flag.
Physical supports are never deduplicated merely because their sums coincide.

Retain min(C,child_slots^2) records, with this slot count fixed publicly before
any input assignment. If the complete valid count exceeds C, flag overflow.
Every prefix count is retained as a wire; the count is never saturated at C.
Continue the same schedule even after overflow. A prefix sum of all node
overflow flags suppresses the ENTIRE proposal, not only the overflowing node.

At the root, join the two retained lists by opposite vector sum AND equal
linear hash of their support IDs. The independent affine vertex mark checks
the source assignment. This realizes marking both endpoints because offsets
cancel in the difference hash. A proposal is copied only for exactly one
marked neighbor and zero whole-attempt overflow.

The root reuses evaluate_record_join, which reverses scan states, comparison
histories and root records. Then reverse nonroot levels: erase copied records
against their still-live sorted parents, erase overflow/prefix histories,
unsort and erase candidates against still-live child lists. Finally erase
the signed leaf records. All discarded wires are checked to be zero.
The operation XORs its answer into arbitrary target wires, not just zero.

The existing six-call compiler independently checks proposal reciprocity and
coarse divisibility plus a nonzero FULL descended label. Thus a program that
proposes an image at only one endpoint cannot be accepted as a phase pair.
No error labels, secret, source-state inverse or quantum RAM is supplied.

## Why Whole-Attempt Overflow Is Essential

The report includes a native three-row, sixteen-column matrix with an
untruncated tree edge2 <->10368. At capacity4, endpoint2 overflows one node
whereas endpoint10368 overflows none. The full filtered relation is invariant
under partner negation; the overflow event is NOT. Capping lists and accepting
without reciprocal/overflow accounting would silently change the proof.

With the complete IID source and independent unfiltered marks, the preceding
moment audit supplies E[D]=1 and M=E[D^2]. At

    C >= 256*ceil(M)*k*L,
    theta = largest reciprocal power of two <= 1/(4*(M-1)),

the coarse accepted endpoint mass is at least3*theta^2/8. The proof subtracts
overflow-incident edges using2*theta^2*sqrt(M*P[overflow]); it does NOT assume
degree and overflow independent. This implementation satisfies the exact
nonoverflow graph/clean-work premises of that local derivation. External
mathematical review remains open. Smaller capacities are useful finite failure
controls but are explicitly denied that inherited source lower bound.

## Cost And Research Value

Every candidate cell, retained copy, root record, forward/reverse comparator,
list scan and overflow-prefix step has a fixed operation count independent
of x, marks or success. All levels' record/count/comparison histories remain
charged in coherent basis-wire storage. Polynomial arithmetic scratch is
excluded and disclosed, not confused with a complete qubit count.

The conservative time AND coherent storage bound is
O(k*C^2*poly(n,m,log C)); this is not the classical expected Wagner O(kL)
bound. Low-level gate costs have not been exported. For fixed a and large b,
the exponential factor is at most2^(4n/(a+1)), with polynomial factors and
large capacity constants still charged. At a4 this exponent is4n/5, versus
the two-list2^n baseline. This is a baseline improvement within this particular
record architecture, NOT an improvement over known best quantum algorithms.

Original mask weight is k*w. Independent original dephasing visibility v
therefore multiplies the output coherence by v^(k*w), not v^tree_depth.
For fixed a, v=1-1/n gives a constant depending on a. Growing a to reduce list
cost can destroy visibility; no growing-a noisy efficiency theorem is claimed.
One batch still yields ONE phase qubit, so repeated descent still compounds
fresh supply and noise. Natural source reductions, that recursion bottleneck,
efficient final decoding and matched classical attacks remain unresolved.

Interpreter work caps return UNKNOWN, never an impossibility/negative result.
The saved finite controls are selected implementation tests, not probability
estimates under the native source. None authorizes a central speedup promotion.

## Next High-Judgment Task

Compare the joint list-cost / physical-width / recursive-supply frontier,
including fresh-batch and visibility-matched restoration costs. In particular,
do not select a growing tree arity on the basis of the list exponent alone.
The priority is an amortized multi-output or collective primitive that changes
the recursion, not further polishing these finite sorting controls.
