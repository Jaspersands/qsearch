# Full Native Sampling Beyond Path Powers

2026-10-25. Local written argument, NOT independently reviewed or formally
verified. No novelty or optimality claim. The new result is a composition
of known graph structure and approximation tools with an explicit signed
two-replica contraction for this project's native output task.

## Research Decision

The preceding rational-transfer pass proposed a quasipolynomial classical
full-output bound only for path powers. Changing the frustration graph to
a branching ECF graph does NOT by itself escape that attack. The same
asymptotic upper-bound argument extends to ALL even-hole/claw-free graphs
with explicit canonical generators and local X/Z readout, at polynomial
inverse temperature and inverse error. Graph construction and both amplitude
replicas must be charged. This is not a polynomial sampler and does not
rule out a polynomial quantum versus quasipolynomial classical separation.

Implemented here: exact complex-rational finite-transfer-product sampling
on any VERIFIED tree decomposition, including the full signed output law;
explicit rational circular-arc decomposition; verified bag-tree gluing;
conditional thermal resource plans and bounded direct-Pauli controls.

Still not implemented: automatic general ECF recognition/clique-atom and
arc-model construction; certified thermal polynomial roots; the composed
large-instance approximate thermal sampler. Published polynomial graph
algorithms and root-refinement algorithms enter the WRITTEN upper bound,
not a claim that those compilers ran here.

## 1. Same Native Problem, Not A Sector Or Marginal Substitute

Let G be an explicit labelled graph on vertices 0,...,m-1, and define

    O_i = X_i product_{j<i, {j,i} in E(G)} Z_j,
    H = sum_i J_i O_i,   0 < |J_i| <= 1, J_i rational.

For the canonical ordered word P(y)=O_0^y_0 ... O_(m-1)^y_(m-1), applying
operators from right to left gives P(y)|0>=|y>. Its normalized trace is
zero unless y=0. Thus for A=sum_y a_y P(y),

    A|0> = sum_y a_y |y>,    ||A|0>||^2 = tau(A^dagger A).

The target thermal vector is exp(-beta H/2)|0>/sqrt(tau(exp(-beta H))).
The sampled output is its complete native bit string, after any selected
local Hadamards, followed by arbitrary efficient CLASSICAL postprocessing.
An arbitrary entangled measurement or coherent decoder is not covered.
Nor is an arbitrary physical representation of the same frustration graph:
its initial state need not realize this faithful native word isometry.

Define T(u)=sum_{S independent} (-u)^|S| product_{i in S} J_i O_i and
A=T(u_0)...T(u_(L-1)). The exact sampler works for any graph and explicit
Gaussian-rational u, independently of whether that product is thermal.

## 2. The Crossing Phase Is A Local Edge Factor

Expand the product using binary selections s_(i,l): layer l selects an
independent set. Initially terms are ordered by layer and then by vertex.
To put them in vertex order, a selection at earlier vertex i in later
layer p crosses a selection at later vertex j in earlier layer q iff p>q.
It gives a minus sign exactly when {i,j} is an edge. Equal-vertex copies
cancel in pairs without an extra sign. Consequently

    a_y = sum_{s: XOR_l s_(i,l)=y_i}
          product_i product_l (-u_l J_i)^s_(i,l)
          product_{i<j, {i,j} in E} (-1)^[sum_{p>q} s_(i,p)s_(j,q)],

where each layer independently satisfies the graph's edge exclusions.
This is a signed factor graph, not a positive independent-set model.

For probabilities introduce a second selection array t, and multiply the
first weight by the COMPLEX CONJUGATE of the second. The phase is the sum
of the two edge exponents. Write a_i=XOR_l s_(i,l), b_i=XOR_l t_(i,l).
The local measurement factor at vertex i is:

    unobserved:             1[a_i=b_i],
    pinned Z outcome z:     1[a_i=z] 1[b_i=z],
    pinned X outcome z:     (-1)^(z*(a_i+b_i))/2.

The X factor includes its normalization. Summing either basis's two pinned
factors gives the same unobserved equality constraint. This proves that
contraction gives the EXACT unnormalized mass of any partially specified
output event, including mixed local bases. There are 2L layers, not L.

## 3. Tree Decomposition With Small Bag Independence

Suppose a tree decomposition has B bags, each with independence number at
most k. For each bag, list its independent subsets, including the empty
set. Their count is at most sum_{j<=k} binom(m,j) <= (m+1)^k.

A bag state gives one such subset for each of the 2L layers. Adjacent bags
must agree on every selected vertex in their separator. There are at most

    (m+1)^(2kL)

states per bag. Root the tree and assign each unary and edge factor to
the highest bag containing its arguments. The relevant bags form a
connected subtree, so this owner is unique. A bottom-up message sums local
states with fixed separator assignment, multiplying child messages and
the owned factors. No factor or eliminated variable is counted twice.
Bag constraints enforce all graph edges because edge coverage is checked.

Running intersection, vertex/edge coverage, tree connectivity and the bag
independence bound are verified. Checking the latter by all (k+1)-subsets
is polynomial for fixed k, not an unchecked annotation. Empty separators
are allowed and disconnected graph components retain their proper products.

Messages can be signed or complex. Only the final mass is required to be
real and nonnegative. The implementation NEVER replaces intermediate
weights by their absolute values, clips a negative answer, or samples a
positive surrogate measure. An identically zero product has no output
distribution and is rejected.

One contraction uses poly(m,B,L)*(m+1)^(2kL) exact arithmetic operations.
Sequentially compute both extensions of the current output prefix and draw
the next bit with their normalized mass. At most 2m contractions per sample
are needed; exact partition identities are checked. The vertex order is
arbitrary and need not follow a path decomposition. An exact rational coin
uses expected polynomial random-bit work, not rare-event rejection.

All global summands have a common denominator with polynomial bit length
in m,L and the explicit coefficient precision. Products use each owned
factor once, and summing at most 2^(2mL) configurations adds O(mL) bits.
This also bounds intermediate-message bit lengths. Very small conditional
probabilities are not an uncharged inverse-probability runtime cost.

## 4. Why ALL ECF Graphs Have k <= 2 Decompositions

The imported graph result is the polynomial clique-atom decomposition into
unit circular-arc graphs, cliques, or joins of the former with a clique;
see Cameron, Chaplick and Hoang, Theorems 2.3 and 5.9 and Section 6:
[On the structure of (pan, even hole)-free graphs](https://arxiv.org/html/1508.03062).
Its algorithmic constructions, not mere existential treewidth, are used.

The following small-bag-INDEPENDENCE deduction is local to this note:

1. A pan contains an induced claw at its attachment vertex. Therefore every
   ECF graph is (pan, even hole)-free, and the imported decomposition applies.
2. Given a circular-arc representation, cut at a point that is not an arc
   endpoint. All arcs crossing the cut form a clique C. The remaining arcs
   are intervals on a line; the intervals covering a point form a clique D_t.
   Sweep their endpoints and take bags C union D_t. Edges incident to C are
   covered when the other endpoint appears, all vertices have connected bag
   occurrences, and each bag is a union of TWO cliques. Thus alpha(bag)<=2,
   even if the bag's cardinality grows with m. No Helly property for the
   entire circular-arc graph is assumed.
3. Add any universally joined clique K to every bag. C union K and D_t are
   still two cliques. Clique atoms themselves need one bag of independence 1.
4. For a clique separator S, each piece's tree decomposition contains a bag
   containing all of S. This follows from the Helly property of pairwise
   intersecting SUBTREES of a tree, not of circular arcs. Connect those bags
   across the two pieces. Their only shared vertices lie in S, so running
   intersection is preserved and no bag grows. Repeat the clique gluing.

The published polynomial atom/arc constructions and this sweep/gluing give
a polynomial-size, polynomial-time constructible certificate. Disconnected
components can be joined by empty separators. The code verifies supplied
certificates and implements the explicit arc sweep and gluing, but does not
port the complete published recognition algorithm.

An especially important distinction: ordinary treewidth can be large
because cliques are large, while per-layer independent subsets remain
quadratically many per bag. A treewidth-only baseline misses this attack.

## 5. Thermal Composition, Including All Costs

For ECF canonical generators the established transfer/mode identities give
T(u)=product_k(I-u epsilon_k Z_k), H=sum_k epsilon_k Z_k, with equally
weighted occupation sectors under the faithful trace. These are imported
from [Elman, Chapman and Flammia](https://arxiv.org/html/2012.07857), Lemmas
1-2 and the mode/logarithmic-derivative construction. They are NOT implied
by having a tree decomposition alone. The exact finite-product sampler does
not require the ECF identities, while this thermal consequence does.

Use the preceding sibling bundle's exact paired-pole rational construction
with A=beta*sum|J|/2 and delta=epsilon/(4m). It returns an odd rational
r(x)=O(x)/E(x), with |r-tanh|<=delta on [-A,A], E even with strictly positive
coefficients and E(0)>0, and degree

    L = O(log(2+beta*sum|J|*m/epsilon) * log(m/epsilon)).

Set p(z)=E(beta*z/2)-O(beta*z/2) using the parity convention of that bundle,
and factor p(z)/p(0)=product_j(1-u_j z). In occupation k its transfer
product has factor [E(beta*epsilon_k/2)/E(0)] [I-r(beta*epsilon_k/2) Z_k].
The scalar in front is positive and independent of the occupation sign.
Normalized mode angles differ by at most delta. Orthogonality under the
faithful occupation trace therefore bounds full native vector error by
sqrt(alpha)*delta <= epsilon/4, without assuming any energy gap or overlap.
Using m rather than a path-specific formula for alpha is conservative.

The positive even polynomial also gives E(beta*epsilon_k/2)>=E(0), hence
the reference transfer vector has norm >=1. The previous root-rounding proof
then applies unchanged to a general graph: independent sets are a subset
of all vertex subsets, so ||T(u)||<=(1+|u|)^m. If |u_j|<=U, B0=U+2 and
each factor is rounded within zeta<=epsilon/[8Lm B0^(mL)], telescoping
bounds operator error by epsilon/8 and normalized vector error by epsilon/4.
Required precision is polynomially many BITS, not B0^(mL) bits. Square-free
factorization retains multiplicities; certified complex refinement is
charged, not replaced by floating roots. The exact sampler above accepts
the resulting Gaussian rationals and conjugates them on its bra copy.

The reference rational argument and root compiler specification are in
[RATIONAL_TRANSFER.md](../hdqi-rational-transfer-2026-10-25/RATIONAL_TRANSFER.md).
The rational approximation is an adaptation of known multipole methods,
not a new approximation claim. Its published analytic starting point is
[Lin, Lu, Ying and E](https://arxiv.org/html/0906.1319); polynomial-bit complex
isolation/refinement is described by
[Mehlhorn, Sagraloff and Wang](https://arxiv.org/abs/1301.4870).

This is first a generic-coupling argument. Degenerate nonzero couplings do
not require running unstable mode extraction: approximate by generic real
couplings, use the SAME explicit transfer polynomials and uniform scalar
error/norm inequalities, then pass to the limit in finite-dimensional
operators. The sampler/root precision never depends on a mode separation.
This continuity step does not extend the identities to non-ECF graphs.

Combining k=2 with L=O(log^2 n) for polynomial beta and inverse epsilon,
where n is the EXPLICIT input bit length, yields the local upper bound

    exp(O(log^3 n)) expected classical time per complete sample.

The exponent includes both replicas and polynomial coefficient precision.
No information is supplied about individual eigenmodes, probe residues,
partition functions, or preparation success probabilities. Exponentially
large beta has log(beta) dependence and can make L polynomial rather than
polylogarithmic in n; do not retain the stated quasipolynomial conclusion
under that changed parameter regime.

## 6. Adversarial Checks And Remaining Limits

- The signed expansion is checked against direct bitwise Pauli actions,
  which do not call its edge-sign formula. Complex factors are not restricted
  to conjugate pairs. X readout exposes sign errors hidden by Z probabilities.
- All partial-output events on a bounded fixture are compared to exhaustive
  suffix sums, not only sample histograms. Empty/zero products are distinct.
- The arc construction is verified as a graph certificate, and branching
  gluing must pass running intersection. A wrong link is rejected.
- An even cycle is deliberately accepted as an exact transfer-product input
  but is NOT labelled ECF or a certified thermal input. Small ECF recognition
  in controls is exhaustive and explicitly limited to small fixtures.
- Finite controls include a non-line-graph ECF input, but they do not prove
  the all-size statement. The mathematical derivation and cited theorems do
  that work, subject to further review.
- No sampled bond truncation, positivity hypothesis, mixing-time promise,
  average-sign estimate or supplied normalization replaces the stated costs.
- The degree constants and bag state counts can be enormous. This is an
  asymptotic narrowing of a research direction, not a practical thermal run.

Next reasoning task: compare a useful end-to-end native source/reduction
outside this full-output model with the existing Rees/native-source work.
Do not spend another pass merely replacing paths by ECF trees or building
a quantum mode compiler without a useful reduction and a better separation.
Coherent downstream computation or graphs with even holes are possible
ways outside the scope, but each changes an assumption and needs its own
algorithm and classical comparison; neither is evidence of hardness.
