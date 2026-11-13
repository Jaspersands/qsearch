# Stable top-degree inputs: the existing small-LR BIT baseline

2026-11-13. Narrow primary-source/interface audit. Fresh STATE/TRAPS and
`KRONECKER_STABLE_LR_BASELINE.md` were read. Sources used: actual
Briand--Orellana--Rosas `stability.txt`, Ikenmeyer `small_lr.txt`,
Burgisser--Ikenmeyer `positive_lr.txt`, and Ikenmeyer--Panova `reduced.txt`.
No network, API, Git, agent, implementation or finite control was used.

**Disposition:** at the retained primary theorems' scope, this native family
has an exact classical algorithm in poly(n,g+1) BIT time. Under the fixed-K
promise R<=n^K it is polynomial in numerical n. A new sampler is unnecessary
to match this narrow region. No compact-binary or full-ratio theorem follows.

## 1. Exact coefficient identification and the dimension bound

Write a=|alpha|, b=|beta|, s=a+b=|gamma| and theta[n]=(n-|theta|,theta).
The native assumption n>=4s makes all three augmented labels partitions.
Actual `stability.txt`, Theorem 1.2, states
    stab(alpha,beta)=a+b+alpha_1+beta_1<=2s<=n.
Its section 3 proof identifies stabilization of the entire Kronecker product,
so the target ordinary coefficient equals the reduced coefficient at this n.
The actual 2024 `reduced.txt`, equations (1.1)--(1.2) and section 1.1,
identifies the top-degree case |gamma|=|alpha|+|beta| with the LR coefficient:
    g(alpha[n],beta[n],gamma[n])=c_(alpha,beta)^gamma=:g.
Permutation symmetry reconciles that source's ordering of the three labels.
If either alpha or beta is empty, return the corresponding partition-equality
indicator directly; s=0 gives one. Zero LR coefficients remain included.

For every ordinary partition triple, independently of stability,
    f^lambda f^mu=sum_tau g(lambda,mu,tau) f^tau
implies g(lambda,mu,nu)<=f^lambda f^mu/f^nu=R.
Thus the native promise R<=n^K implies g<=n^K. The classical algorithm does
not need to know g, receive a hive, or verify R before it runs to completion.

## 2. What the enumeration source actually supplies

Let ell=max(length(alpha),length(beta),length(gamma))<=s<=n; this is the
triangular graph parameter called n in `small_lr.txt`. Its section 2.4
Connectedness Theorem 2.15 and section 3 Theorem 3.1 supply a connected
integral hive-flow graph and a constructive polynomial-delay neighborhood
superset contained in the same integral hive polytope. Theorem 3.3 enumerates
all g points by breadth-first search, returning their number. Its advertised
clock counts arithmetic operations, so it is NOT by itself a BIT conclusion.

The actual section 5.2 Algorithm 3 is used, not section 5.1's hypothetical
secure-extension oracle. Every recursive leaf outputs a feasible point,
including the shortest-path fallback in line 13. Lemma 5.8 and the concluding
NeighGen construction bound duplicates and the work through exhaustion.
Consequently the empty-neighborhood and g=1 cases do not hide unbounded
delay after the last output. The exact-count variant returns zero on an
empty polytope and |S| when the queue is exhausted. We use (g+1), rather than
the source's shorthand g, in the clock to include initialization and g=0.

## 3. Constructing the integral seed without an LP-to-integer inference

The seed is paid by the actual `positive_lr.txt`, section 4.4 Algorithm 1
and Theorems 4.8/4.23, rather than by assuming that saturation makes an
arbitrary rational LP output integral. Start with the zero bounded hive flow.
While the residual graph has a shortest source-to-target turnpath p, update
    f <- f+pi(p).
The source's Shortest Path Theorem preserves feasibility and integrality.
Each augmentation increases total throughput by exactly one; capacities
bound it by |gamma|=s. Thus at most s<=n augmentations occur. At termination
the optimality criterion either certifies no capacity-achieving hive, hence
g=0, or supplies the required integral seed. Returning the final stored f
along with the Boolean answer does not require an additional search.

These residual graphs have O(ell^2) vertices/edges and use ordinary shortest
paths. A path projection is an integer linear combination of O(ell^2) unit
edge incidences. The seed's signed throughput coordinates therefore have
magnitude O(s ell^2), with O(log(n+2)) bits. All slacks/capacity tests are
small integer linear combinations of these coordinates. The unit version
is already polynomial in NUMERICAL n. The source's faster capacity-scaling
Algorithm 2/Theorem 5.4 is optional; no binary-input claim is needed here.

## 4. Enumeration bit sizes and the completed clock

Store a flow by its O(ell^2) signed throughputs on the triangular graph.
The actual BI12 section 2.2 identifies these coordinates injectively with
flow classes and identifies integral classes with integer coordinates.
NeighGen changes a stored flow by pi(c), or pi(pq), where the paths/cycles
have O(ell^2) length. Each coordinate change is therefore O(ell^2).
A newly discovered point can be assigned a discovery-tree parent. That
tree has at most g vertices, so every stored coordinate has magnitude
    O((s+g+1)ell^2).
Temporary candidate flows satisfy the same bound up to a constant factor.
Thus all flow/slack values have O(log(n+g+2)) bits. Graph distances, indices,
recursion stacks and queue counters also have polynomial bit length.

The actual routines use these additions, small linear slack tests and graph
searches; the arithmetic-operation count does not conceal repeated squaring
of unconstrained integers. Comparing/storing a flow, and duplicate detection
by an explicit sorted dictionary or even a naive scan of the at-most-g stored
records, has polynomial bit cost in n and g+1. Combining this with the
source's O((g+1)^2 poly(ell)) enumeration and the paid seed gives
    exact total BIT time poly(n,g+1),
including output, termination and g=0. Substituting g<=R<=n^K proves the
claimed classical polynomial clock for fixed K in this native family.

## 5. Source and selection boundaries

The imported mathematical results are the retained preprints' shortest-path,
connectedness and NeighGen theorems; this audit checks their native interface
and bit accounting, not a new proof of every geometric cycle lemma. A public
journal erratum exists, but its full primary text was inaccessible. No
unknown correction or mirrored summary is imported. The actual section 3
exact-count algorithm and section 5 fallback references used above were read
directly; the integral-seed interface was independently paid from BI12.

This closes only the proposed stable TOP-DEGREE LR-sampler selection gate.
It does not settle arbitrary stable deficit, general ratio-promised triples,
compact binary complexity, coherent transforms, hardness or quantum advantage.
