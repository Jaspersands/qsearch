# Vector Short-Mask Join: A Costed Frontier, Not A Speedup

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty, polynomial-time
receiver, hard natural reduction, efficient decoder or new sieve exponent.

Run `python qsearch.py dcp-vector-short-mask-join`, then
`node research/certificates/dcp_vector_short_mask_join_crosscheck.js`.

## Research Decision

The preceding disjoint-Gaussian baseline has quadratic original supply and
exponentially poor native visibility even at v=1-1/n. That is NOT a barrier
to all pairings. This workbench implements a counter-frontier: linear original
supply, O(n)-width masks, constant native mean coverage and constant per-level
visibility under that same independent balanced-noise promise.

The price is EXPLICIT exponential time AND coherent work space. This extends
the existing scalar balanced-support meet-in-the-middle baseline to vector
Z4^n descent; it is not a new mechanism. The important research question is
whether a structured receiver can beat BOTH that cost and one-output recursive
supply, not whether short useful partners can exist at all.

## The Group Is Not One Cyclic Integer

Read only A mod4, with n components and m original phase qubits. Require
A(y-x)=0 componentwise modulo4. Each emitted useful label is
A(y-x)/4 modulo2^(t-2), nonzero after the paid full-label check.

Keys may be stored as packed base-four digits AFTER componentwise arithmetic.
Never add packed keys as integers modulo4^n: carries change the group.
Examples for two components:

```text
(1,1)+(3,3)=(0,0) in Z4^2; packed5+15=4 mod16, not0.
(3,0)+(1,3)=(0,3) in Z4^2; packed3+13=0 mod16, a false match.
```

The evaluator calculates every signed vector sum componentwise and negates
the right vector componentwise. Packed keys are only compared for equality.

## Balanced Support Program

Split an even m into two halves. Keep the first L lexicographic weight-k
supports in each half, without inspecting labels, assignments or noise.
There are S=L^2 distinct physical masks, ALL of width r=2k. For an original
assignment x, a left mask u and right mask v match when

```text
sum_{i in u} (1-2*x_i) A_i = -sum_{i in v} (1-2*x_i) A_i in Z4^n,
H(u)=H(v).
```

Mark vertices by H(x)+c=0 with a uniformly sampled binary affine seed.
Hash rows, including singular/all-zero matrices, and offsets are NEVER
rank-filtered or success-filtered for the source theorem.

Records carry vector-sum/hash key, side and original support mask. Reuse the
existing fixed-address bitonic sort, full prefix join histories, inverse
scan/sort and reverse record generation. The proposal returns the neighbor
only when x is marked and it has exactly one matching neighbor. The existing
six-XOR-F compiler additionally checks reciprocity and a useful nonzero full
label; no faulty degree-one endpoint is promoted to a valid pair.

The scalar and vector implementations now share the same group-agnostic
record-join helper. Old scalar arithmetic and semantics are unchanged. The
new module does not inherit scalar fault fields that use a DIFFERENT parameter
called n: here n counts vector components, and log2|Z4^n|=2n.

## Native Mean Coverage Proof

Let G=4^n and mu=S/G. For fixed x each nonempty signed mask sum is uniform.
Two distinct masks have a signed2-by-2 minor of determinant+/-1: use an
exclusive coordinate and either a common or another exclusive coordinate.
This proves their joint sums uniform over Z4^n x Z4^n, including nested masks.
Thus E[D]=mu and E[D^2]=mu^2+mu*(1-1/G).

Any three distinct Boolean vertices are affine-independent once augmented
by a constant coordinate. Independent affine vertex marking with probability
theta therefore gives the same two/three-vertex thinning law as the scalar
baseline. Charge both possible competing endpoints of every marked edge:

```text
E[mutual unique marked source fraction]
  >= mu*theta^2 - 2*mu*(mu-1/G)*theta^3.
```

Choose the smallest hash width g with2^g*G>=4S, theta=2^-g. The bound is at
least mu*theta^2/2. This is an UNCONDITIONAL mean over IID uniform A and the
complete independent hash seed. It is not a guarantee for each fixed A/seed,
nor a source law after selecting favorable examples.

With m=4n choose the minimum k with binom(2n,k)>=2^n, and L=2^n. Such k<=n
exists: picking one element from each of n disjoint pairs already gives2^n
distinct n-subsets. Then mu=1,g=2 and the exact lower bound is

```text
coarse coverage >= 1/32 + 1/(32*4^n),   mask width2k<=2n.
```

Coarse selection is independent of all higher lifts. The prior fresh-label
theorem therefore applies: useful nonzero-label acceptance has the extra
factor1-2^(-(t-2)n), with failed attempts paid. Discard higher parent transcripts
and use fresh independent batches. The separate noisy restoration module
only applies under its explicit independent balanced-source premises.

## Noise Contrast

Homogeneous independent original visibility v gives EXACT per-pair visibility
v^(2k), not a merge-depth surrogate. Heterogeneous visibilities bounded below
by v give the same lower bound. No arbitrary correlated-noise claim is made.
For v=1-1/n and n>=2, width<=2n gives a constant guarantee. An elementary
bound is v^(n-1)>1/3, since (1+1/(n-1))^(n-1)<sum_j1/j!<3. Thus
v^(2n)>=1/36. With t>=3 the useful higher-label factor is>=3/4, yielding
native mean useful visibility>=1/1536 under the stated promises.

The report uses tighter exact dyadic values on its growing parameter grid,
not this loose universal constant. These are source-mean bounds, NOT executed
large quantum systems. They falsify extending the disjoint-block noise barrier
to every short-mask pairing, but do not solve its computational bottleneck.

## Honest Computational Cost

L=2^n records PER HALF. One XOR-F replay generates4L records including
uncomputation, performs both sorting passes and both prefix scans, and retains
all comparison flags and clean prefix registers until reversed. The resource
ledger includes padding, counter widths and coherent record/prefix/history bits.

```text
time:  O(L log(L)^2 poly(n,m))
space: O(L poly(n,m)) COHERENT work bits for superposed input x.
```

Linear ORIGINAL phase supply is not linear total quantum space. One cannot
store the x-dependent records classically, measure sorting flags, grant free
QRAM, or erase prefix histories without disturbing the unknown phase.
Elementary sorting-network gate export/hardware transpilation is NOT supplied;
the bounded classical basis-wire replay verifies the reversible algorithm and
its charged schedule. Work caps return UNKNOWN, never an algorithmic negative.

Repeating any one-output descent still compounds original supply with phase
depth. Even a hypothetical polynomial join alone would not establish efficient
growing-depth recovery. An advance needs amortized multi-output/packet retention,
a different collective readout, or another way around both bottlenecks.
Classical partner search is a baseline for the public subproblem, not a classical
secret solver given only the quantum phase-state source.

## Verification And Falsifiers

- Complete native source censuses: n1,m4,L2, including every coarse matrix,
  all1024 affine seeds and16 original assignments; plus n2,m2,L1.
  Degree moments, mutual isolation and probability lower bounds are checked.
- Original-assignment program/reciprocity/full-label/phase-density checks on
  vector controls, including both cyclic-packing counterexamples.
- Exact inverse join/sort/record cleanup and operation counts use the existing
  scalar tests as regressions as well as new vector controls.
- Independent JS replay rebuilds direct vector neighbors, all source census
  counts and symbolic resource/noise arithmetic without trusting pass flags.
- Forged costs, missing higher-label lineage, zero output credit, packed cyclic
  substitutions or claimed polynomial coherent space must fail verification.

Primary background, not novelty evidence:
[Beals et al., Efficient Distributed Quantum Computing](https://arxiv.org/abs/1207.2307)
for reversible sorting/memory context;
[Remaud, Schrottenloher and Tillich, DCP Time/Query Tradeoffs](https://arxiv.org/abs/2206.14408)
for why few original queries with exponential computation is not a new speedup.
