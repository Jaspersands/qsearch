# Paid Adaptive CNOT-Tree Receiver Benchmark

This implements a real public-feedback controller and an EXACT, explicitly
bounded exponential policy benchmark. It does not implement an efficient DCP
solver, a general optimal quantum measurement, or a newly hard oracle family.
The input is the existing compiled sine-localized lattice phase source.

CLI: `python qsearch.py dcp-paid-tree-receiver`.
Artifact: `research/phase_workbench/dcp_paid_tree_receiver.json`.

## Physical Model and What the Controller Receives

Assume independent balanced phase registers rho(k;s,v_i), with public labels
k modulo N=2^ell, one common unknown s, and externally supplied v_i>=v0.
The controller sees only labels, ancestry and actual measurement outcomes.
It cannot inspect densities, obtain exact expectations, choose a CNOT branch,
request a label, clone/reprepare a register, or receive the hidden shift.
The visibility/source promise is NOT established by a public label table.

An allowed merge is physical CNOT followed by target Z measurement. Both
branches have probability1/2 independently of s and all input labels, and
the surviving state has label k_left+/-k_right with visibility v_left*v_right.
Induction on disjoint ancestry proves that all remaining registers are still
conditionally product given s and the public transcript, even for feedback
pairing. This is a conditional model theorem, not an arbitrary-noise claim.

Target one parity-label register k=N/2. An X readout has parity bias v and
requires no higher-bit knowledge. Label zero is NOT a successful target.
All other live registers may be ignored at stopping; every supplied root
is still charged. This class does not include collective output measurements,
general POVMs, coherent arithmetic/filtering or decoding from all local bits.

## Exact Bellman Benchmark

A state is a forest of (public label, original-leaf bitmask) pairs. All
bitmasks are disjoint. Output visibility is at least v0^L for actual leaf
count L, NOT v0^(2^maximum_merge_depth). For exact common v0 this is equality.
Different tree shapes with the same label/mask induce the same balanced state;
their discarded branch histories are secret-independent. This justifies
the finite Markov representation.

Let stop(S) be the largest v0^L of a parity-label register, or zero. Then

    V(S)=max(stop(S), max_ordered_pairs [V(S_plus)+V(S_minus)]/2).

Each merge reduces the forest size by one. Include both control orientations
and EVERY measurement branch; no favorable branch is chosen for free.
Induction proves this recurrence is the optimal expected output visibility
within precisely this single-target policy class. If failure branches are
replaced by fair guesses, average one-bit success is (1+V)/2. Actual execution
instead reports an abort when it has no target; it does not claim recovery.

The full Bellman certificate stores EVERY reached subproblem, its value and
chosen action. Independent replay checks all legal alternatives, not only
the favorable trace. The state forest can grow exponentially with root count.
Root/state caps fail UNKNOWN, never as evidence that no receiver exists.
Actual visited states/actions are reported, including work off the chosen path.

The physical executor uses only the public backend API. It computes a complete
plan first, applies each prescribed merge ONCE, follows the sampled branch,
and measures at most one terminal target. All roots, failed branches and
unconsumed registers remain paid. The fixed visibility promise is not taken
from the private audit. Private source/density checks occur separately.

## Matched Nonadaptive Forest Baseline

A fixed tree on L specified roots has uniformly random leaf signs modulo one
global sign. The CNOT branch bits are independent fair bits, and this sign
parameterization is a bijection for any fixed topology. Global sign does not
matter at target t=N/2. Its target probability is therefore the fraction of
the 2^(L-1) signed sums equal to t, independent of tree shape.

Compare against EVERY set partition of the roots into precommitted trees,
not just one tree. Disjoint trees have independent branch laws. Execute all
trees and choose the highest-visibility target after their outcomes. For
blocks ordered by increasing leaf count, their expected best output bias is

    sum_B v0^|B| p_B product_(earlier C)(1-p_C).

The baseline enumerates all partitions, includes this terminal selection,
and reports partition and signed-assignment work. This is also bounded
exponential work, not a proposed scalable classical or quantum solver.

### A Real Local Feedback Gain and Its Source Falsifier

For N>=8 and t=N/2, suppose original labels are (1,t-1,2). Merge the first
two. The sum branch is already t: stop and retain visibility v^2. The
difference branch is 2-t; merge it with label2. One branch now gives -t=t
with visibility v^3, and the other fails. Thus the public-feedback bias is

    V_feedback = v^2/2 + v^3/4.

For these three roots, the best fixed forest has bias v^2/2: its only useful
two-root tree hits t with probability1/2; its full three-root tree hits with
probability1/4 and unnecessarily damages an early success. Exhausting its
five set partitions proves the comparison, including parallel output selection.
The Bellman recurrence verifies this policy is optimal in its stated class.
The same mechanism holds for (a,t-a,2a) when a is not 0,t,t/2,3t/2.

This gain is NOT a quantum/classical runtime separation. For three original
IID uniform labels, the ordered literal template has probability (N-4)/N^3:
there is one b and c for each of N-4 permitted a values. Among M originals,
union bound gives at most M(M-1)(M-2)(N-4)/N^3, below M^3/N^2. At
M=poly(log N) it is exponentially rare. Public filtering must pay its failures.
Generated/sieved labels, broader feedback mechanisms and correlated sources
are NOT covered by this literal-pattern bound. They require a new source law.
The worthwhile open question is a costed transformation that makes useful
completion relations common without destroying visibility, not promoting this
rare template into an algorithm.

## Falsifiers and Research Leverage

For N=8 and labels(1,1,2), successful three-leaf trees have maximum depth2
but visibility v0^3, not v0^4. For labels(1,N/2-1), a two-leaf sum branch
can jump directly to parity valuation with probability1/2. Thus valuation
height is neither a leaf count nor an end-to-end resource bound.

Prefix-demodulated quadrature scores have mean +/-v/2 only after the needed
label and correct prefix exist. Raw target acquisition is exponential at the
first bit. For scores in [-1,1], Hoeffding requires a sufficient quota
8*v^-2*ln(ell/delta), separately from acquisition. The existing algebraic
tree audit has been corrected accordingly; it no longer calls secret-dependent
exact-expectation evaluations an implemented O(ell) decoder.

The old factor-two quota is independently falsified INSIDE the inverse-log
noise promise. At ell3, stage2, label1, correct prefix1 and true bit0,
alpha=pi/4. With visibility4/5, both Pauli choices give D=z/sqrt(2) and
p(z=+1)=(1+v/sqrt(2))/2. For35 shots and total delta=1/10000, the single
event of17 positive spins has probability at least8.15128e-5, above the
allowed stage error1/30000. Bad rate1/5 is below1/ell.

The certificate uses rational lower sqrt(2)>1414213/1000000 to bound p
from above. The negative-score binomial term decreases in p above1/2, so
substituting that rational upper endpoint gives a rigorous probability LOWER
bound. A positive Taylor sum through degree16 proves
exp(35*v^2/2)>2*ell/delta, so35 shots really meet the former quota.
No floating-point tail estimate or tie convention is needed. The corrected
conservative dyadic Hoeffding quota is188 shots, separately from label supply.

This benchmark can falsify optimistic merge policies and expose small public
feedback mechanisms worth deriving symbolically. A finite optimum is NOT a
scalable algorithm. Any promising policy must generalize with charged source
access, polynomial control work, noise robustness, full-bit recovery and
matched classical competitors. General collective quantum receivers remain
outside this benchmark and are not ruled out.

The live workflow uses four fresh six-register batches from the actual public
sine source, not stored densities reinterpreted as free quantum copies. It
targets one bit of a classically easy calibration lattice. Twenty-four preparations
are paid even when a batch produces no target. The full physical source law
and these finite results do not certify a hard growing lattice reduction.
Three live batches stop at an already emitted parity label. The fourth follows
three actual merges and measures a three-leaf output. These are single-trajectory
channel checks, not empirical success-rate estimates. The independent checker
replays all Bellman alternatives, all fixed-forest partitions, every sampled
physical branch/density, raw source costs and the confidence counterexample.

Relevant known-solver comparison: the recent prime-power cyclotomic sieve
explicitly distinguishes its ideal sample algorithm from the limited number
of approximate states furnished by known LWE reductions:
https://arxiv.org/abs/2609.34996 . This benchmark neither implements nor improves
that algorithm. Source supply is an algorithmic obligation, not a free oracle.
