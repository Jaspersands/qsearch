# Outcome-Adaptive Affine Carry-Packet Receiver

Exact bounded benchmark, not an efficient receiver or a new speedup.
No novelty claim. The physical grammar and derived source statements remain
subject to independent external review.

Run `python qsearch.py dcp-adaptive-affine-packet-receiver` and
`node research/certificates/dcp_adaptive_affine_packet_receiver_crosscheck.js`.

## Why This Is The Next Search Space

The pre-complement rank gate rules out one particular way of evading carry
cost: choose ONE direction using all A, then measure its complement. It does
not rule out keeping a packet and choosing later measurements from earlier
outcomes. This module implements precisely that distinction, with an exact
static comparator and complete branch accounting, not a post-hoc choice of
the most favorable unobserved branch.

INPUT is m supplied pure unknown phase qubits with public n-component labels
A modulo q=2^t. The source is the native vector phase model, not a designed
oracle problem. All initial parity-chart syndromes are retained.

Success requires an output label modulo Q=q/2 with EVERY component even and
at least one component NONZERO. The result is one nonconstant phase qubit
at the next modulus q/4. Zero labels are useless and receive no credit.
Neither this event nor a large finite probability constitutes secret recovery.

## Instrument And Exact Policy Optimization

A state in the search is the current physical affine chart x0+V, where
V is a subspace of ker(A mod2). The packet has flat amplitudes on this
chart, with the original unknown phase retained. Allowed actions are:

1. Choose any nonzero binary linear functional on current chart coordinates.
2. Implement an invertible binary change of chart and measure that coordinate
   in Z. The two affine hyperplanes have probability exactly1/2 for every secret.
3. Choose subsequent chart operations using only public A and observed bits.
4. At dimension1 retain the pair (x0,x0+u), with its original signed label
   difference divided by2. No secret or density is consulted by the controller.

Every invertible binary chart change is a reversible linear basis permutation
and can be implemented with CNOTs; origins add known X operations. This
finite benchmark does not supply a hardware/source backend. Its opaque port
interface requests actual measurements and returns an unknown-state receipt.
Tests implement those requests by physical projectors on original amplitudes,
checking every final branch and several secrets. The workflow itself executes
ZERO physical source preparations, and claims no mixed-state noise law.

Let F(V,x0) count the original basis assignments leading to useful descent.
At dimension1 it is0 or2; otherwise

    F(V,x0)=max_h [F(child_h,0)+F(child_h,1)].

The two children each contain half the assignments. Thus the recurrence
charges both outcomes, and division by2^m after summing ALL initial syndromes
gives the source success probability conditional on the supplied public A.
The certificate contains EVERY legal h and both children, not merely the
chosen policy. State coordinates and transitions are independently replayed.

The comparator searches ALL nonzero physical directions in ker(B), and may
choose a different best fixed direction for every initial syndrome, just as
the adaptive controller may. Zero labels are excluded for both methods.

## Quadratic Representation For Future Synthesis

Write V's basis as u_1,...,u_k. The next low phase, relative to the origin,
is the public vector quadratic map

    f(z)=[A(x0 XOR sum_j u_j z_j)-Ax0]/2 mod2,
    f(z)=sum_j l_j z_j + sum_(i<j) B(u_i AND u_j) z_i z_j.

Its linear coefficients depend on higher A and background. Its polar
coefficients depend only on B and V. Higher-degree terms in the XOR expansion
vanish modulo2 after division by2. Root maps are exported and checked against
EVERY original chart assignment, including the selected counterexample.
This is a mathematical representation for instrument synthesis, NOT a grant
of unknown-phase evaluation/preparation or a solution to simultaneous MQ.

This reframes the open task: find a PAID, polynomial-size adaptive chart or
nonlinear fibre-pairing rule that keeps useful unknown phase information as
both n and t grow, with a valid noise law. Merely finding many public collisions
or supplying a reversible forward evaluator does not implement that receiver.

## Stronger Arbitrary-Pairing Comparator

For each initial parity chart, compute full public residual phase values
g(x)=(Ax-Ax0)/2 modQ. A pair gives useful descent iff g(x) and g(y) have the
same low vector but are unequal full values. Each low-vector color class
therefore gives a complete multipartite pairing graph: equal full values
form parts, and edges connect different parts.

If a class has N vertices and its largest part has L, the maximum useful
pair count is min(floor(N/2),N-L). The first bound counts vertices; the second
counts partners outside the largest part. Both are attainable: if L>N/2,
match every outside vertex to the largest part; otherwise repeatedly pair
vertices from the two largest nonempty parts to leave at most one vertex.
Sum this over colors. Arbitrary leftover pairs can be discarded as failures.

This is an attainable bound for arbitrary computational-basis regrouping,
NOT an optimum for all quantum measurements, and not a polynomial circuit
construction. Tests independently compare it with NetworkX maximum matching
on explicit original-label graphs. It is a useful comparator for rejecting
an overly narrow affine search grammar.

## Live Results And A Falsifier

The primary cohort is fixed BEFORE inspection: unfiltered native label seeds
0,1,2 at(n,m)=(1,5), and3,4,5 at(2,6), all q16. All syndromes and all
feedback outcomes count; no source-hardness or asymptotic frequency estimate.

- Seed2 improves useful descent from1/2 (best static) to1 (affine feedback).
- Seed5 at n2,m6 improves1/2 to3/4.
- The other four have no gain. All six saturate the arbitrary-pairing bound.

Trying to falsify that last pattern succeeds: a SEPARATELY SELECTED native
n2,m6,q16 control, seed94, gives affine optimum9/16 versus arbitrary pairing
11/16. It was found by examining95 fixed seeds and is labeled as selected,
not added silently to the primary unfiltered cohort. Its public rows are

    (5,3,8,9,13,0)
    (15,11,9,13,8,0).

Every affine policy is covered by the Bellman census. Thus affine feedback
does not generally realize even the best computational-basis pairing.
This is a concrete finite reason to search nonlinear/coherent packet tools,
not to declare all adaptive extraction optimal or all quantum receivers blocked.

## Why The Search Is Not Efficient

For initial kernel dimension k and parity rank r, the complete search visits

    2^r sum_(d=1)^k 2^(k-d) [k choose d]_2

affine charts, with2^d-1 actions for each chart of dimension d>1. The Gaussian
binomial already has order2^(k^2/4) near d=k/2. At k64 the ledger exceeds
2^1000 states; this is parameter arithmetic, not an executed search.
Exact counts are checked against the finite traversal. Caps return UNKNOWN,
never a negative result or a polynomial-time claim. The observed policy may
have small depth, but discovering/encoding a uniform policy is a separate cost.

## Known-Algorithm Boundary And Access Model

Do not treat success at fixed q as a new generalized-dihedral HSP algorithm.
For base(Z_(2^t))^n with inversion action, nilpotency class is t. Constant t
therefore lies in known constant-class, bounded-prime HSP territory.
[Imran and Ivanyos, Zero sum subsequences and hidden subgroups](https://arxiv.org/html/2304.08376v1),
Theorem1 and its introduction, state the relevant exact result using a
subgroup-state-creating unitary AND its inverse. This is not automatically
the copy-only phase-state interface here. Nor does that constant-class theorem
give a uniform polynomial bound when t grows. The existing
`research/reductions/hsp_campaign_claim_audit.json` provides related context.

Importantly, the SAME paper's Proposition3 supplies a non-exact HSMC variant
without inverse calls, with class-dependent complexity. Missing inverse access
is therefore NOT a blanket rejection of known methods. The repository already
has a genuine [native copy-to-coset compiler](NATIVE_ORBIT_SOURCE_ACCESS.md)
and relative inverse. Do not rebuild it or confuse its return of the original
unknown seed with a blank-state purification oracle. This pass does not prove
the full phase-only receiver transfer; use the existing access audit to identify
the remaining forward-access, group-model and growing-class costs precisely.

[Ivanyos, Sanselme and Santha, nil-2 groups](https://arxiv.org/html/0707.1260)
also supply a relevant quadratic/linear cancellation technique using many
variables. Its hiding-function/group-action prerequisites must be mapped,
not silently substituted for supplied phase copies. Borrow mechanisms; do
not count rediscovering solved oracle regimes as breakthrough progress.

## Next Experiments Ranked By Leverage

1. Derive a compact rule realizing useful nonlinear fibre pairings, starting
   with the9/16 versus11/16 counterexample; count reversible implementation cost.
2. Reuse the existing copy-to-coset compiler and map the published non-exact
   zero-sum/subgroup conversion to the phase-only interface. Identify the
   remaining forward-access and growing-class costs, not just an inverse gap.
3. Seek a uniform growing-n AND growing-t policy family and prove its output
   label distribution and inter-level composition. Finite success alone fails.
4. Derive mixed/noisy packet transitions and visibility loss. Pure flat states
   cannot stand in for the lattice source's unknown contamination.
5. Attach a hard natural reduction and stronger classical attacks only after
   a candidate receiver/source pair survives those structural obligations.

No accepted candidate or broad negative theorem is added by this benchmark.
