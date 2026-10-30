# A Native Obstruction To Nonnegative Paired-Support Sampling

2026-10-24. LOCAL UNREVIEWED proof and exact rational controls.
This rejects one concrete classical sampling proposal. It establishes
neither classical hardness nor a quantum algorithm or speedup.

## 1. Research Question And Prior Art

The previous offline-tangent pass leaves preparation exponential in patch
size. Before trying to compress it, this pass tests a more consequential
classical alternative: turn the already convergent paired-word expansion
into a positive polymer sampler for the full pilot-label law.

[Yin--Lucas](https://arxiv.org/html/2305.18514) obtains classical Gibbs
measurement samples through controlled conditional probabilities under
its high-temperature assumptions. That is not automatically a sampler
for our pure pilot. [Mann's polymer framework](https://arxiv.org/html/2608.19489v1#S2.SS2)
requires nonnegative polymer weights. Its general mechanism cannot simply
be applied to signed quantum activities. These are prior-art techniques,
not new algorithms introduced here.

The existing cluster/defect constructions efficiently estimate certain
quantities, conditionally on their local proofs, at small degree-scale
temperature. They do not supply all positive-pinning conditional laws.
The proposed alternative would avoid rare conditional probabilities:
sample connected paired-word visit supports and their output labels
directly. Its essential positivity assumption is FALSE.

## 2. Exact Native Input And Proposed Representation

Use the same explicit canonical independent Pauli Hamiltonian

    O_i = X_i product_{j<i, j~i} Z_j, H=sum_i O_i,
    t=beta/2, a_T(y)=<y|exp(-t H_T)|0>, H_T=sum_{i in T} O_i.

The pilot is exp(-tH)|0>/sqrt(Z), with Z=sum_y a_V(y)^2. All couplings
in the witness are one. There is no oracle, unknown input or special
state-preparation advice. Real amplitudes suffice; all Pauli signs remain.

For a visited generator set S and output label y subset S, define

    W(S,y)=sum_{y subset T subset S} (-1)^|S\T| a_T(y)^2.   (1)

This is exactly the sum of paired exponential words with equal parity y
and union of visited generators S. Inclusion-exclusion removes words
that failed to visit a generator in S. The unnormalized output weight is

    a_V(y)^2 = sum_{S superset y} W(S,y).                  (2)

Disconnected visit supports factor over their induced graph components,
since generators in different components commute and the exponential
interleavings factor. Thus connected S with label y are the candidate
colored polymers; compatibility requires disjoint nonadjacent supports.
Unoccupied output bits may still belong to a visited support through even
generator multiplicities. Omitting them changes the representation.

The absolute paired-word envelope obeys

    sum_y |W(S,y)| <= product_{i in S}(cosh(beta)-1).

Consequently this proposal is not being rejected because of a missing
small-activity bound: it fails because individual colored weights have
the wrong sign. Summing over labels can conceal the failure.

## 3. Explicit Connected Witness

Take vertices 0,...,5 and edges

    (0,1), (0,2), (1,3), (2,4), (2,5), (3,5).

This is a five-cycle with a leaf attached to vertex 2. Its maximum degree
is three. Set Y={1,2,3,4}, represented by bit mask 30. The only supersets
of Y are Y, Y+{0}, Y+{5}, and V, so (1) has exactly four terms.

Let sigma exchange 0 with 5 and 1 with 3, fixing 2 and 4. This preserves
the graph and unit couplings. The canonical generators are independent,
so sending O_i to O_sigma(i) defines a trace-preserving *-automorphism of
their algebra: it preserves squares and every commutation relation, and
permutes the orthonormal ordered-word basis up to signs.

Write P(Y)=O_1 O_2 O_3 O_4. Reordering its image gives

    sigma(P(Y)) = O_3 O_2 O_1 O_4 = -P(Y).

Only the inversion of the anticommuting pair 1,3 contributes a minus sign.
Since sigma(H)=H and trace is invariant,

    a_V(Y)=tau(P(Y)* exp(-tH)) = -a_V(Y) = 0              (3)

for EVERY t. This is an exact symmetry zero, not a tiny numerical amplitude.
The usual transpose/reversal parity test alone misses it: G[Y] has two
edges, an even number.

On Y itself the Hamiltonian splits into two commuting anticommuting pairs,
(O_1+O_3) and (O_2+O_4). Each pair's exponential has only identity and
single-generator terms, so a_Y(Y)=0. The same sigma exchanges the two
five-vertex restrictions and flips P(Y), hence

    a_(Y+{0})(Y) = A(t), a_(Y+{5})(Y) = -A(t).

Equation (1) now yields the EXACT identity

    W(V,Y) = -2 A(t)^2.                                  (4)

Meanwhile W(Y+{0},Y)=W(Y+{5},Y)=A(t)^2. Their cancellation with (4) is
necessary to recover the zero true output weight in (3).

## 4. Strict Negativity At Arbitrarily High Temperature

The first nonzero Taylor coefficient of A is

    A(t) = t^6/45 + O(t^8).                              (5)

At orders below six a missing bridge leaves two pair sectors with zero
amplitude; an even-output label also excludes all odd orders. At order
six, the contributing bridge multiset is (0,0,1,2,3,4). Its 360 distinct
words have 188 positive and 172 negative signs. Their signed sum 16,
divided by 6!=720, gives 1/45. Exact independent matrix powers and a
multivariate rational recurrence check this finite combinatorial identity.

The restricted Hamiltonian norm is <=5. Bound the remainder, for 0<t<=1/64,
by exp(5t)(5t)^8/8!. Relative to t^6/45 this is at most

    [45*5^8/(8!*64^2)] * (64/59)
      = 390625/3383296 < 1/8,

using exp(5t)<=1/(1-5t). Therefore

    A(t) >= (7/8)t^6/45 > 0,
    W(V,Y) <= -2[(7/8)t^6/45]^2 < 0                      (6)

throughout 0<beta<=1/32. In particular

    (d+1) beta^2 <= 1/256 < 1/64,

strictly inside the earlier observable-estimator regime. Lowering
temperature parameter beta cannot repair positivity except at beta=0.
The leading colored-weight coefficient is -2t^12/2025, or
-beta^12/4147200. This is a leading negative activity, not merely a negative
higher-order coefficient whose total might still be positive.

The implemented order-20 Taylor intervals use rational endpoints and a
geometric tail majorant. No floating-point cancellation certifies (6).

## 5. It Persists Beyond A Six-Vertex Control

Attach an arbitrarily long path to the fixed leaf 4, retaining all unit
couplings. The graph remains connected with maximum degree three; the
same automorphism extends by identity on the new vertices. The six-vertex
induced support retains exactly the negative weight (4), since its
restricted Hamiltonians are unchanged. Moreover every full label whose
restriction to the first six vertices is Y is still fixed with sign -1,
so its amplitude vanishes. Extra tail indices cause no additional word
inversions. The symbolic checker verifies explicit 128- and 1024-vertex
members without constructing statevectors or exponential tables.

This is not a claim that these bounded-width examples are hard to sample.
They are counterexamples inside an arbitrarily large native family to a
universal positivity assumption.

## 6. Clipping Is Not A Free Repair

Replacing each negative colored polymer weight by zero produces nonzero
weight 2A(t)^2 on the forbidden label Y of the six-vertex block. Thus it is
not an exact sampler. An approximate method must bound the total lost
mass, not appeal to the small size of one correction.

There is also an asymptotic warning. The partition of this clipped model
is at most the absolute paired-word sum cosh(beta)^6, which is <2 in our
range: cosh(beta)<=1/(1-beta^2). Hence the clipped distribution assigns
Y probability at least r=[(7/8)t^6/45]^2>0. On N DISJOINT copies of this
block, both the true and clipped constructions factor. The true law
never contains Y on any block, whereas the clipped law does with
probability at least 1-(1-r)^N. Their TV distance is at least that number.
For fixed beta and N>=1/r this lower bound is >=1-exp(-1).

This amplification uses disjoint blocks; no analogous connected-family
TV bound is asserted. The numerical reciprocal-r ledger is not an executed
large instance. Regrouping signed contributions before sampling, or a
separate globally controlled truncation, is NOT ruled out.

## 7. What Was Falsified And What Was Not

Falsified: sampling these exact connected visit-support/color activities
as nonnegative weights, including the argument that even total generator
multiplicity by itself guarantees positivity. A supplied graph symmetry
can create exact output zeros beyond elementary reversal parity.

Not falsified: the earlier signed cluster estimator, observable comparator,
offline tangent lemma, a different positive representation, tensor-network
sampling, signed methods with controlled variance, general classical
sampling, coherent quantum preparation, or the possibility of a speedup.
The witness is deliberately a decisive falsifier, not a proposed hard task.

The general positive-polymer idea is prior art. Novelty of this local
counterexample is unassessed. No independent reviewer or proof assistant
was used. Passing controls validate these formulas, not the full research
goal. Main CLI, registries and UI remain untouched during migration.

Next meaningful work must change the mechanism: a charged resummation
that absorbs this interference without exponential signed variance, or a
genuinely compressed quantum preparation construction. Do not add more
nearby negative polymer examples or rerun the same small-graph scan.
