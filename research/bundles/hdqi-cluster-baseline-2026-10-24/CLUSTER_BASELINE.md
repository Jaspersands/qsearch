# A Uniform-Degree Classical Partition Comparator

Date: 2026-10-24. Status: LOCAL, UNREVIEWED deduction, with an executable
finite reference. Not a quantum algorithm, a parent-gap proof, a novelty
claim, or an implemented production FPRAS.

## 1. Correction And Why This Pass Exists

The enumeration bound in Hastings--Schmidhuber, Section III.3, is

    m (m/epsilon)^[O(log d / log(1/kappa))].

The source explicitly fixes d and kappa when calling this polynomial.
At constant small kappa and growing d, its stated bound alone does not
establish uniform polynomial time. Earlier external notes said classical
partition tractability was already known throughout the target regime;
that wording was too broad. This note supersedes that wording in
`hdqi-parent-gap-2026-10-23/PARENT_GAP_TARGET.md` and
`hdqi-filtered-parent-2026-10-24/FILTERED_PARENT.md`. Their frozen receipts
are not retroactively edited.

Randomized cluster sampling is not our invention. Putterman--Zlokapa--Cotler,
Section 5.5, uses importance sampling and a spanning-tree correction to
avoid enumerating every cluster. Its physical locality/strength theorem
does not automatically imply an anticommutation-degree theorem. Below is
an explicit adaptation using even multiplicities and resummed SET polymers.
No positivity assumption on polymer activities is needed.

Primary sources inspected:
- https://arxiv.org/html/2610.03697v1 (Sections III.1--III.3).
- https://arxiv.org/html/2607.28536v1 (Facts 5.1--5.2 and Section 5.5).
- https://arxiv.org/html/2608.19489v1 (nonnegative polymer sampler scope).

## 2. Model And Local Theorem

Input: the public graph G on m vertices, rational beta >= 0, real rational
couplings |J_i| <= 1, and the canonical independent Pauli generators

    O_i = X_i prod_{j<i, j~i} Z_j, H=sum_i J_i O_i.

Let tau be normalized trace, Z=tau(exp(-beta H)), d=max degree, D=d+1,
Jmax=max |J_i|, lambda=(beta Jmax)^2. If lambda=0, log Z=0 exactly.

LOCAL THEOREM: if D lambda <= 1/64, log Z has a randomized classical
additive-epsilon approximation with failure probability <= delta in time
polynomial in the explicit input bit length, m, 1/epsilon and log(1/delta),
with an exponent independent of d. A complete real-arithmetic construction
and a finite-precision reduction are given below. Constants are deliberately
loose. This does not cover every possible constant called "small kappa".

An additive log error implies a multiplicative factor exp(+/-epsilon) for
Z. This is NOT the physical redundant Hamiltonian's partition function,
nor a sampler for pilot amplitudes, nor a TFD preparation algorithm.

## 3. Activities And An Explicit Envelope

For each nonempty connected vertex SET S, let w(S) be the sum of terms
in the exponential word expansion whose support is exactly S. Only words
in which every label occurs a positive EVEN number of times survive tau:
independence of the canonical generators is essential. Word traces are
signs. Taking absolute values BEFORE summing over even counts gives

    |w(S)| <= prod_{i in S} [cosh(beta J_i)-1] <= lambda^|S|.       (1)

The last bound uses |beta J_i|<=1, implied by the theorem's condition.
Signs of the J_i disappear for these even counts, not for arbitrary words.
Disconnected word supports factor into connected components after all
interleavings are summed. Thus Z is the hard-core polymer partition sum,
with S,T incompatible iff they overlap or an edge connects them.

For k ordered polymers, including REPEATED polymers, let B be their simple
incompatibility graph on their k occurrence indices. Write phi(B) for the
alternating sum over connected spanning subgraphs, and t(B) for the number
of spanning trees. For k=1 both quantities are one. Then

    log Z = sum_{k>=1} (1/k!) sum_{S_0,...,S_{k-1}}
               phi(B) prod_i w(S_i).                            (2)

Disconnected B contributes zero. The tree-graph inequality |phi(B)|<=t(B)
follows by partitioning connected subgraphs according to their minimum
spanning tree with a fixed edge order; each interval contributes 0 or
(-1)^(k-1). Convergence and identification with log Z follow below.

## 4. Two Primitive Importance Samplers

### Rooted Set

For a supplied host vertex v and size s, choose a uniform labeled tree
on [s], root it at label 0, and put label 0 at v. Traverse away from the
root. Each child chooses uniformly one of D slots at its parent's host
vertex; real slots are its neighbors, remaining slots fail. Reject repeated
host vertices. For s=1 use the unique singleton tree and no slot choice.

If the resulting induced vertex set is S, output the pair (S,Y) with

    Y = w(S) C_s D^(s-1) / [(s-1)! t(G[S])],
    C_1=1, C_s=s^(s-2) for s>=2.                                (3)

Every S containing v has exactly (s-1)! t(G[S]) labeled-tree embeddings.
Their probability is this count divided by C_s D^(s-1). Consequently,
for any test function f,

    E[Y f(S)] = sum_{S connected, |S|=s, v in S} w(S) f(S).

C_s/(s-1)! <= exp(s), so, with a=e D lambda,

    |Y| <= a^s/D.                                             (4)

No search over all connected subsets occurs in the sampler.

### Set Touching A Vertex

Choose one of D closed-neighborhood slots at v; unused slots fail. With
chosen u, run the rooted sampler at u. For its returned S let
r=|S intersect N[v]|, which is positive, and output Y_touch=D Y/r.
Then E[Y_touch f(S)] is the sum over sets S touching v, with weights w(S),
and |Y_touch|<=a^s. Both the D factor and r divisor are necessary.

## 5. Cluster Draw And Its Exact Multiplicity

Choose h in {1,...,L} with probability p_h=2^(-h)/(1-2^(-L)).
Choose uniformly one of the 2^(h-1) positive ordered compositions
(s_0,...,s_{k-1}) of h. Choose the root host vertex uniformly from m.
Run the rooted set sampler of size s_0 there.

For k>=2 choose a labeled tree on the k polymer indices, rooted at 0,
with probability prod_{i>0} s_parent(i) / A, where

    A=s_0 h^(k-2); for k=1, A=1.

A weighted Prufer sequence of length k-2, with symbol probabilities s_i/h,
implements this distribution exactly. Traverse this tree. For each child
i choose v uniformly in its parent's polymer, then run the touching-set
sampler at v with size s_i. Failed draws return zero; never renormalize
after failure.

Build B. It is connected on every successful draw. Let

    b_i = |{v in S_parent(i): S_i touches v}| >=1.

Return

    X = [m 2^(h-1)/p_h] [A/(k! s_0)] [phi(B)/t(B)]
             prod_{i>0}(1/b_i) prod_{i>=0} Y_i.                (5)

Here Y_0 is rooted and the other Y_i are touching weights. Cancellation
of the root-host choice leaves s_0 embeddings, removed by 1/s_0.
The weighted tree probability cancels A and the choices of parent
vertices cancel prod s_parent. For each tree, exactly prod b_i valid
attachments remain, removed by the b_i divisors. Finally, summing over
the t(B) possible trees cancels t(B). Thus E[X] is exactly (2) truncated
to total polymer SET size <=L, with its 1/k! factor intact.

Repeated polymers are NOT discarded. In particular m=1 gives the usual
alternating series log(1+w), not just its first term. This is an explicit
negative control for wrong cluster factorials.

## 6. Uniform Bounds, Tail And Precision

For k>=2, A/(k! s_0)=h^(k-2)/k! <=exp(h); for k=1 it is 1/s_0<=1.
Combining (4), its touching version, and the tree-graph inequality yields

    |X| <= [m/(2D p_h)] R^h,
    R=16 D lambda >= 2 e^2 D lambda.                         (6)

Under D lambda<=1/64, R<=1/4. Thus |X|<=m (in fact much smaller).
The absolute cluster contribution at order h is at most m R^h/(2D):
the preceding probability cancellations also hold with |w| and |phi|.
Hence the total absolute tail beyond L is bounded by

    m R^(L+1) / [2D(1-R)] <= m 4^(-L).                    (7)

The same estimate holds for complex temperature z with |z|<=beta. The
cluster sum is analytic there and agrees with log Z near zero by its
formal power series. Exponentiating and analytic continuation gives Z
throughout the disk and excludes zeros. On the real path it is the real
logarithm of positive Z. This avoids assuming convergence in order to
prove convergence.

Take L=ceil(log_4(4m/epsilon)) and N=ceil(32m^2 epsilon^-2 log(2/delta)).
Independent averaging, Hoeffding and (7) allocate at most epsilon/4 to
truncation and epsilon/2 to statistical error with failure <=delta.

Activities are not free oracles. Inclusion-exclusion gives

    w(S)=sum_{T subset S} (-1)^|S\T| tau(exp(-beta H_T)).

Each restricted canonical H_T has only |T| qubits. Computing these
normalized traces to absolute accuracy lambda^s eta/2^s costs exp(O(s))
times polynomial precision work, using rational arithmetic with certified
Taylor remainders, or interval matrix exponentials. Set eta=epsilon/(4mL).
Compute w(S)/lambda^s to error <=eta and clip to [-1,1]. The product of
at most L such bounded factors changes (5) by <=mL eta, so bias <=epsilon/4.
Required precision is O(s log(1/lambda)+s+log(1/eta)) bits; input bit length
accounts for very small rational beta or couplings. A zero lambda is handled
separately, not divided by. There is no unpriced cancellation assumption.

Graph/tree draws have rational probabilities and use exact random integers.
phi takes O(3^k) arithmetic steps by subset recurrence; tree counts use
integer Laplacian minors. Since s,k<=L=O(log(m/epsilon)), each draw costs
polynomial time with degree-independent exponent. Rational combinatorial
weights have polynomial bit length; precision overhead remains polynomial.

## 7. Extension: Pilot Generating Functions, Not Pilot Sampling

The same argument also covers more than the ordinary partition. For
t_i in [-1,1], let S=exp(-beta H/2)=sum_y a_y P(y) and define

    Z_t = sum_y |a_y|^2 prod_i t_i^y_i.                       (8)

For real beta this equals tau(S Phi_t(S)), where Phi_t independently
conjugates by Z_i with probability (1-t_i)/2. This random-unitary channel
multiplies P(y) by prod t_i^y_i. Both S and Phi_t(S) are positive definite,
so Z_t>0. Also Z_t<=Z by the absolute-value triangle bound.

Expand the two exponentials in this expression. A nonzero paired-word
contribution has EVEN total multiplicity of every generator, and the
field multiplier has magnitude at most one. The sum of the absolute
paired-word coefficients, with every label in a set U present, is bounded
by prod_{i in U}(cosh(beta J_i)-1): summing the two segment lengths combines
their beta/2 weights into beta. Disjoint, nonadjacent supports factor, as
do their field multipliers. Hence Z_t has precisely the set-polymer form
used above with the SAME lambda^|U| activity envelope.

For complex temperature use the analytic continuation of the real
coefficient squares, not an absolute-square expression. The same majorant
applies, permitting the convergence argument of Section 6. Activities
are obtained by inclusion-exclusion of the restricted Z_t on at most |U|
coefficient qubits. Their evaluation remains exp(O(|U|)) with polynomial
precision work. Thus the local theorem applies uniformly to rational
fields in [-1,1], including zero and minus one.

Consequences for the pilot distribution mu(y)=|a_y|^2/Z:

- t_i=0 on A and 1 elsewhere gives Z_t/Z=Pr[Y_A=0]. Log avoidance
  probabilities can be estimated even if the probability is very small.
- t_i=-1 on A and 1 elsewhere gives the parity expectation
  E[(-1)^sum_{i in A}Y_i]. It is positive and classically estimable here,
  including for a global subset A supplied explicitly.
- For A=all vertices, Phi_t sends H to -H, so Z_t=1 exactly. The total
  parity expectation is 1/Z. This is a useful analytic negative control
  against advertising pilot parity readout as a new quantum output.

Approximating log Z_t and log Z to additive eta gives the ratio an
additive O(eta) error because 0<Z_t/Z<=1. These are NOT samples from mu.
For disjoint A,B, mixed pins require

    Pr[Y_A=0,Y_B=1] = sum_{T subset B} (-1)^|T| Pr[Y_(A union T)=0]. (9)

This generic conversion has 2^|B| terms and potentially severe cancellation.
Already on one anticommuting edge the pilot has no |11> amplitude, so
the four terms for B={0,1} cancel EXACTLY. Efficient avoidance or parity
estimation does not supply a uniformly priced sequential sampler or a
coherent preparation circuit. This is a limitation of this conversion,
not a hardness theorem for other classical algorithms.

## 8. Attempted Falsification And Remaining Limits

- Removing any embedding/tree/contact divisor biases the estimate. Exact
  small-graph expectations, rather than Monte Carlo confidence alone,
  check those divisors and repeated-polymer factorials in the reference.
- Positive-weight polymer dynamics cannot simply be imported: the proof
  above allows signed activities and uses bounded signed estimators.
- A non-redundant physical relation can allow odd multiplicities. For
  ZI, IZ, ZZ the word containing each once has nonzero trace; (1) fails.
  The theorem is deliberately restricted to the canonical relaxation.
- The doubled-word extension preserves the envelope for fields in [-1,1].
  Arbitrary mixed pinning is different: positive pins remove the unit
  constant term and can have zero weight. Do not reuse the zero-free/log
  argument or claim a pilot sampler without resolving that change.
- General low-locality/strength results cannot be invoked by substituting
  anticommutation degree for physical support overlap. This proof instead
  establishes the needed specific polymer and importance envelopes.
- The live implementation is a finite reference with deliberately small
  enumeration guards and rational activity controls, NOT the above fully
  general precision-managed estimator. Its finite success is not the proof.
- This is an adaptation of known importance-sampling machinery. It has
  not received independent review. No claim of new literature priority.

## Research Decision

Use these local uniform-degree comparators provisionally, subject to review,
instead of relying on a misread deterministic bound. Do not promote a
partition, pilot-parity or avoidance-estimation advantage in
D beta^2 Jmax^2<=1/64. Full pilot sampling, the separate degree-scale
filtered-parent gap, and a useful physical decoder/output remain open.
The next theorem task is thermal weighted geometry or a constructive
mixed-pin sampling argument, not another unweighted norm estimate.
Gemini's bounded implementation handoff is in HANDOFF.md; no central
registry admission is authorized by this finite receipt alone.
