# Native Tree Filters: Moment And Overflow Contract

LOCAL DERIVATION / REVIEW PENDING. This is a native-source research contract,
not a new generalized-birthday algorithm, implemented quantum receiver, source
oracle, efficient decoder or novelty claim. Primary background:
[Wagner, A Generalized Birthday Problem](https://people.eecs.berkeley.edu/~daw/papers/genbday.html),
[Lin and Vasudevan, rigorous k-tree analysis](https://arxiv.org/abs/2410.06856).
Their results must not be imported as an independence or coherent-memory
certificate for our native signed subset lists.

Run `python qsearch.py dcp-native-tree-moment-audit` and
`node research/certificates/dcp_native_tree_moment_audit_crosscheck.js`.
The implemented subsystem verifies graph moments, modulo4 constraint ranks,
partner invariance and overflow/source arithmetic. It does NOT implement the
clean bounded-list receiver required by its conditional acceptance contract.

## Exact Native Model

Set tree depth a>=1, leaf count k=2^a, component chunk size b>=1,
vector components n=b*(a+1), and leaf list length L=4^b. Split the physical
coordinates into k disjoint public blocks. Each leaf list consists of L
distinct nonempty fixed supports from its own block. All labels are IID
uniform in Z4^n; x is an original Boolean assignment. A support contributes
its signed vector sum sum_i A_i*(1-2*x_i) modulo4.
Records with equal group values but different supports remain DISTINCT;
deduplicating them would change this graph and its source moments.

At internal level r=1,...,a require each selected subtree sum to vanish on
component chunk r. At the root also require chunk a+1 to vanish. Earlier
chunks already vanish on the final full sum because lower subtrees partition
the leaves. This is componentwise Z4 arithmetic, not packed cyclic addition.

For a full chosen support u, changing x to x XOR u NEGATES every selected
subtree sum. All zero filters are preserved. Thus these filters define an
UNDIRECTED graph on original Boolean assignments, even though which support
tuples pass depends on A and x. Every graph edge preserves Ax modulo4.

## Why Native List Correlations Are Not Ignored

List entries in one leaf are generally NOT mutually independent. However,
any TWO distinct support sums are jointly uniform: their coefficient rows
have a signed unit2-by-2 minor. Identical choices give the same random vector.
Different physical blocks are independent. Those facts suffice for the first
and second moments; no random list oracle or higher-wise independence is used.

For one selected tuple, each chunk's subtree constraints are disjoint linear
sum constraints. Across chunks they involve independent label components.
Their total rank is b*k, so a tuple survives with probability L^(-k).
There are L^k tuples, hence E[D]=1.
These are native means BEFORE selecting favorable labels, syndromes or hashes;
they are not inherited by a postselected packet without a new source law.

For two tuples let S be the leaves where their choices agree. For each chunk
r, paired subtree equations are redundant precisely when EVERY leaf in that
subtree belongs to S; otherwise an exclusive random leaf gives a unit pivot.
Let c(S) count all fully shared internal subtrees plus one additional shared
root for the last chunk. The joint survival probability is L^(-2k+c(S)).
There are L^k*(L-1)^(k-|S|) ordered tuple pairs with that exact equality pattern.

Consequently the exact second moment has a compact recurrence:

```text
f_0 = 1
f_r = f_(r-1)^2 + (L-1)/L^2
M = E[D^2] = f_a + 1 - 1/L.
```

For a new internal root, the all-shared probability times its previous weight
is L^-2, so the extra factor L contributes (L-1)/L^2 independently of level.
The final root chunk contributes1-1/L. At a1 this recovers
M=2-1/L^2, exactly the two-list vector baseline.

Also f_a<=(1+1/L)^(k-1). If L>=2*(k-1), the geometric binomial bound gives
f_a<=2 and M<=3. Outside that regime use the EXACT recurrence; do not assert
a universal constant second moment.

## Reciprocal Isolation And Overflow

For any such undirected graph with E[D]=1 and second moment M, independent
uniform affine vertex marks of probability theta give mutual-isolated endpoint
mass at least theta^2-2*theta^3*(M-1). This is the existing general wedge-count
argument, not a new quantum measurement theorem.

Every NONROOT intermediate list has exact expected untruncated size L. Let a
receiver cap each list at C records and REJECT THE ENTIRE ATTEMPT if ANY
nonroot list overflows. If it behaves exactly like the full tree when there
is no overflow, then delta=P[overflow] <=(k-2)*L/(C+1) by Markov and a union
bound. Filters/caps do not inspect the independent affine mark seed.

Rejecting both endpoints of an overflow-incident edge costs at most

```text
2*theta^2*E[D*1_overflow] <= 2*theta^2*sqrt(M*delta).
```

The two endpoints have equal global incident-edge sums because the original
graph is undirected and the source assignment is uniform. Cauchy-Schwarz uses
the actual second moment, not an assumption that overflow is independent of
high-degree vertices. Dropping that correlation would be an invalid proof.

Choose theta the LARGEST reciprocal power of two <=1/(4*(M-1)), and
C=256*ceil(M)*k*L. Then M*delta<1/256, so the resulting coarse mass is at least
3*theta^2/8. When M<=3, theta>=1/8 and this is at least3/512.
One may charge a tighter dyadic square-root bound, but must not silently omit
overflow or count a first successful branch as the whole source.

Simply truncating and accepting is NOT covered: at the partner, other partial
candidates change, so even sorting by public support IDs can retain a different
set of records. Whole-attempt overflow rejection plus reciprocal checking is
essential to this contract.

## Honest Cost Target And Failure Modes

A conservative static implementation can generate C^2 candidate cells per
nonroot node, sort valid records into the first C slots, retain comparison and
prefix histories, propagate overflow, perform a final unique join, copy the
proposal, and reverse ALL work. Charge O(k*C^2*poly(n,m,log C)) time and coherent
workspace if using this straightforward method. No O(kL) quantum implementation
or free QRAM is supplied by a classical expected-time Wagner bound.

For default leaf block size4b, choose the least w with binom(4b,w)>=4^b;
w<=2b and full physical mask width is k*w. At original visibility v, the
balanced independent-noise factor is v^(k*w), NOT tree depth. With fixed a and
v=1-1/n it is a constant depending on a; growing k can destroy this benefit.
The saved grid uses a dyadic visibility LOWER bound, never a rounded-up
approximation of1-1/n. All claims remain conditional on the noise promise.
At large b and fixed a4, the conservative C^2 exponent is4n/5 versus the
two-list2^n baseline, but large cap constants delay any finite crossover.
This is a baseline tradeoff, NOT a new known-best result. One-output recursive
supply remains exponential with phase depth even if list evaluation improves.
The report stores useful visibility as exact factors: coarse acceptance,
physical-width visibility, and1-2^(-n^2) for its t=n+2 higher-label example.
This charges the zero-label filter without expanding a huge near-one numerator
or pretending that uninformative zero labels are useful output.

Required executable falsifiers before any receiver claim:

1. Enumerate equality patterns and verify the moment recurrence with exact
   modulo4 unit elimination, preserving any nonzero even residual constraints.
2. Recover the existing two-list moment exactly at a1.
3. Verify every sampled original-label filtered edge also passes at its partner;
   include full-coarse-zero controls with huge degree, not only nice instances.
4. Show overflow is charged and attempt-wide, and that cap failure is not
   promoted to a generic no-go or pointwise source lower bound.
5. Implement actual clean fixed-address work before claiming a coherent receiver;
   a relation graph, moment formula or expected classical list length is not one.

Natural source noise, unknown source supply, independent growing-batch interface,
hard reductions and final decoding remain separate obligations. No candidate
or active negative result should be admitted solely from this moment audit.
