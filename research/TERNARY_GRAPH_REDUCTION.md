# Graph Coloring Does Not Gain From This Decoder Or Padding

SCOPED FALSIFIER, WRITTEN ARGUMENT PENDING INDEPENDENT REVIEW.
No general quantum-coloring no-go, hardness proof, or novelty claim.
An exact classical sampler is implemented. The native quantum circuit is not.

## Question And Input

Can the two-fold multiplication decoder supply the missing whole-input
receiver for the repository's [natural coloring proposal](TERNARY_COLORING_BPQM.md)?
This is a concrete test of a useful target, not another histogram calibration.
We also test the proposed repair of subdividing edges to improve decoding.

Input: a connected simple undirected graph H with an arbitrary fixed
orientation. Let B be its reduced incidence matrix and let the rows of G
span D=ker B over F3. Finding y in {+1,-1}^M with Gy=0 is equivalent to
proper three-coloring, after fixing one vertex color to zero. A tension is
the gradient of vertex colors; nonzero entries enforce unequal endpoints.
This correspondence is standard; see
[Cameron, Jackson and Rudd](https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/bcc20_cjr.pdf).
The supplied matrix/code and graph are explicit, not oracle inputs.

The local pair measurement and Schur-square relaxation being tested come
from [Ragavan and Shutty, Section5](https://arxiv.org/html/2610.00502v1).
We do not turn failure of their particular relaxation on this family into
failure of arbitrary quantum receivers, BPQM, or quantum algorithms.

## Exact Cycle-Square Structure

For a bridge, every circulation has coordinate zero. For two nonbridge
edges in the same series class, circulation coordinates agree up to a fixed
sign. Their products therefore agree WITHOUT that sign. Consequently

    D*D is contained in the span of nonbridge series-class indicators.

The reverse inclusion also holds. Here is the written constructive argument.
Fix a series class S and contract all but one representative edge e in S.
Those contracted edges form a forest. If e becomes a loop, its lifted cycle
has support exactly S, and its coordinatewise square is the indicator of S.
Otherwise e is neither a bridge nor in a two-edge cut: a cut after contraction
lifts to a cut before contraction avoiding the contracted edges, and any
second member of a two-edge cut with e would have belonged to S.

The edge version of Menger's theorem gives two edge-disjoint paths between
the endpoints of e after deleting e. Add e to each and lift the resulting
cycles. They share exactly S: outside S the detours are edge-disjoint, and
every cycle using e uses all of S. Orient both circulations to have value1
at e. Their relative signs agree throughout S, so their product is its
indicator. Thus

    dim(D*D) = number of nonbridge series classes.         (1)

This statement is written, not Lean-formalized. The producer independently
computes cycle columns and actual Schur-square ranks on all142 connected
simple graphs with2 through6 vertices. This census is an identity control,
not the proof.

On a three-edge-connected core every series class is a singleton, so
D*D=F3^M. For EACH native core edge the artifact saves two actual
edge-disjoint detours. Their signed cycles are checked against the incidence
matrix, and their product is checked to be that edge's unit vector.

## The Specific Decoder Completely Loses Its Constraint

The pair-list relaxation has unknown v in D and w in D*D and equations

    w_i - (a_i+b_i)*v_i + a_i*b_i = 0.

When D*D=F3^M, ANY v in D can satisfy these equations by defining w
coordinatewise. The projection onto v has dimension dim D for EVERY
transcript. This is stronger than a vacuous sufficient error bound.
For nontrivial D, this relaxation never certifies unique recovery.

The 40-vertex,80-edge,4-regular native core has dim D=41 and
dim(D*D)=80. An actual legal exclusion transcript leaves all41 v dimensions
free. The input graph, cycle basis, incidence matrix, local outcome
transcript construction, and unit-vector witnesses are reproducible.
The degree-four/five collective BPQM questions remain unresolved.

## Why Subdivision Appears To Help

Replace every core edge by a directed path of length L. Circulation values
are constant along a path, so the physical source has L product trines for
each core symbol. Two distinct exclusions on a path determine that symbol.
The probability that all exclusions are identical is

    r = 2^(1-L).

This is a classical-codeword input law, not a factorization of a coherent
sum of codewords. Call such a path unresolved. If unresolved core edges
form a forest, flow conservation recovers every missing symbol by leaf
elimination. Conversely, when the core square is full, a cycle among the
unresolved edges supplies a nonzero homogeneous ambiguity. Thus the
projected relaxation is unique exactly when that subgraph is a forest.
Tests check this against actual relinearization for every unresolved-edge
pattern on K4, with two different transmitted codewords.

For a simple core, any unresolved cycle needs at least three unresolved
edges. Therefore a valid, loose decoding failure bound is

    delta <= min(1, binom(M,3)*r^3).                       (2)

Its sufficiency does not require a full core square. Preparing the code
label, all physical source coordinates, reversible decoding, label erasure
and inverse decoding gives the conditional near-uniform output estimate

    TV <= min(1, 4*sqrt(3^k*delta) + epsilon_circuit),
    k=M-V+1.                                             (3)

The exponential coherence factor is retained. A small expected number of
unresolved edges alone would NOT prove a useful quantum sampler.
With sufficiently large L, (3) does become small. All ML physical
coordinates and arithmetic/precision costs must be paid.

But the output is a coloring of the SUBDIVIDED graph, not of the core.
For L>=2 any pair of endpoint colors has a proper three-color path between
them. Thus subdivision already removes the original endpoint restriction.
Extra physical channel copies are purchased by changing the problem.

## A Classical Sampler For The Full Padded Distribution

Let N_L(t) count proper length-L color walks with endpoint difference t:

    N_L(0)   = (2^L + 2*(-1)^L)/3,
    N_L(1) = N_L(2) = (2^L - (-1)^L)/3.                   (4)

The reference checks these identities against complete small-path
enumeration. Given core colors x, the number of completions is
W(x)=product_edges N_L(x_v-x_u). Write Nmax=max_t N_L(t).

An actual classical sampler:

1. Draw uniform core colors, with x_0=0 fixing the gauge.
2. Accept with probability W(x)/Nmax^M, using exact per-edge integer coins.
3. For each edge, independently sample a uniform proper path with the
   chosen endpoint colors. Three-state backward counts implement this
   step without enumerating paths or completing an exponential table.
4. Return all expanded colors, or explicitly abort at the paid trial cap.

The accepted core law is proportional to W(x). Each bridge path has
probability1/N_L(t), so every complete proper coloring of the subdivided
graph has the SAME probability. This matches the full target distribution,
not merely a score or a witness. Uniformity is an ideal-random-bit algorithm
statement; the saved seeded PRNG replay is not statistical proof of it.

For L>=2, max_t N_L(t)-min_t N_L(t)=1. Every proposal has acceptance
at least

    (1-1/Nmax)^M >= max(0,1-M/Nmax).                      (5)

For L=Omega(log M) with a sufficient constant, this is bounded away from
zero. The sampler has polynomial bit complexity in the explicit expanded
input, including O(L)-bit random choices and path counts. A cap T gives
abort probability at most min(1,M/Nmax)^T. On non-abort the law is EXACT.
Constant short padding is not silently granted this success guarantee.

Native replay: V40,M80,L64, hence5080 vertices and5120 expanded edges.
It produces and verifies every path, with one trial in the saved replay.
The classical per-trial acceptance lower bound exceeds1-1e-16. The
conditional quantum estimate is below1e-15 at circuitTVbudget2^-64;
the classical16-trial abort bound is below2^-800. No native quantum
sampler was executed, and the classical runtime is not a quantum timing
comparison. The returned core colors are NOT a proper core coloring.

## Restoring The Original Target Restores The Old Source

Require every path's increment sum to be nonzero. This enforces the
original core's unequal-endpoint constraint. It is not free verification
with a guaranteed polynomial acceptance probability.

For a uniform allowed block, let |F_+> and |F_-> be normalized uniform
vectors over the paths whose increment sums are +1 and -1. Negation gives
equal fiber sizes. For a cycle symbol c the whole block state is exactly

    |Psi_c> = (omega^c|F_+> + omega^-c|F_->)/sqrt(2).      (6)

The isometry |+> -> |F_+>, |-> -> |F_-> is independent of c. Thus the
three-state Gram has diagonal1 and off-diagonal -1/2, for EVERY L.
The unrestricted product source instead has off-diagonal (-1/2)^L.
Equation(6) supplies no extra logical discrimination information.
Its tensor product over core edges is the original codeword ensemble
up to a public isometry, not independent extra trine copies.

Keeping the old coordinatewise pair decoder is invalid after imposing
this block constraint. The probability its first-coordinate pair falsely
excludes the true symbol is exactly

    (1/3)*(1-N_(L-1)(0)/N_L(1)),

which is1/3 at L2. Full complex-amplitude, Gram, and false-exclusion
controls check this, including the no-padding limit L1.

There is also a direct output falsifier: K4 has no proper three-coloring,
but its subdivided graph has many. The exact restored-constraint
acceptance probability is ZERO. Empty original targets are retained.

Even colorable instances need not provide cheap rejection. The complete
tripartite core K_(t,t,t) has exactly6 proper colorings. For even L,
N_L(1) is the minimum count, so the probability that a uniform padded
coloring obeys every original endpoint constraint is at most

    6/3^(3t).

At t10 this is below3e-14. This particular core is classically easy;
it is a counterexample to a general rejection guarantee, not a hardness
instance or a quantum lower bound.

## Decision

This closes one proposed bridge from the two-fold decoder to a useful
problem: raw three-edge-connected coloring cores defeat this relaxation,
and padding either changes the task into a classically samplable one
in the certified long-path regime or restores the old discrimination
problem when the original constraints are enforced.

Do not continue with more subdivision lengths, larger graph seeds, or
calling ordinary-coloring failure a generic quantum-decoding no-go.
The next constructive route needs a genuinely different receiver on
the original input, or a different useful problem with small Schur square.
Independent review of (1), the coherent transfer, and reduction scope is
still required. No central negative-result admission has been made.

## Reproduce

    python -m theorems.ternary_graph_reduction
    python -m pytest -q tests/test_ternary_graph_reduction.py \
      tests/test_ternary_coloring_bpqm.py tests/test_ternary_tilted_type.py \
      tests/test_ternary_type_transfer.py tests/test_ternary_decoder_filter.py \
      tests/test_ternary_quotient_decoder.py -W error::RuntimeWarning

The new producer, test file, and `research/reductions/ternary_graph_reduction.json`
are separate from previous reports. No CLI/UI wiring or older producer edits.
