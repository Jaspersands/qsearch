# Inverse-Trace Residual Sampling By Global Binary Hash Heat Baths

29 October 2026. Deduction by Pasteur, independently AI-reviewed by Popper
and parent. No correction required in the saved proof. Independent review
ran26 tests; after nine additional capped-initialization controls, parent
reran all35 successfully. Parent also checked the explicit single-algorithm
premise clarification. Not human-reviewed or claimed novel.
The distributional claims below have proofs and exact finite controls. The essential complete-cell
enumeration algorithm and its polynomial expected cost are UNKNOWN. This is not
a production sampler, an executed polynomial-time algorithm, a hardness result,
or a quantum-speedup claim. Initial witnesses may be biased; worst-start
contraction, not an assumed uniform initialization, pays for that bias.

## 1. Scope And Fixed Native Input

Use the SAME explicit input as [completion transfer](INVERSE_TRACE_COMPLETION_TRANSFER.md):

```
q = 2^n, N = n^2, K = floor(N/8),
H[j,i] = alpha_i^j, 0 <= j < K,
Tr(inv0(x_i)) = b_i, inv0(0) = 0.
```

The public points are arbitrary distinct elements in the SUPPLIED polynomial-basis
field, not newly sampled points. The targets are arbitrary fixed bits. Field
arithmetic, absolute trace, point ordering, and the legal zero convention must
not change. Assume N <= q, 1 <= K < m, and the nonnegative integer B-K defined
below. These conditions hold in the intended native regime.

Fix residual indices U before sampling the prefix. The default is

```
r = ceil(4K/n), m = K+r, |U| = m, T = complement(U).
```

The residual relation is H_U x_U = h. The analysis averages over uniform
h in F_q^K, not over syndromes selected because a solver succeeded. In the
composition, the original accepted prefix produces h = s-H_T x_T, with native
s=0. The residual kernel receives only the public residual instance and h,
and fresh randomness. It does not inspect hidden prefix details or restart the
prefix. The existing transfer theorem pays for induced versus uniform h.

The hash theorem also applies to another explicitly declared fixed residual
size. A smaller surplus justified by Section 3 is NOT permission to change a
saved instance, prefix, or syndrome during a comparison.

## 2. Accepted-Free Binary Coordinates And Exact Prange Comparator

Partition U into K pivot coordinates I and r free coordinates J, deterministically
from the public input. Every K columns of H_U are invertible. Precompute

```
a(h) = H_I^(-1) h, D = H_I^(-1) H_J,
x_I = a(h) - D x_J.
```

The minus sign equals plus in characteristic two. This is exactly the affine
elimination in `theorems/inverse_trace_smt.py::vandermonde_eliminate_residual`.
There remain r FIELD variables, not r Boolean variables.

Compute a basis v_1,...,v_(n-1) of ker(Tr) and a field element c with Tr(c)=1,
using binary linear algebra in the original field. For each free coordinate,

```
y_i = b_i*c + sum_l u_(i,l)*v_l,   u_(i,l) in F_2,
x_i = inv0(y_i).
```

This is a bijection between F_2^(n-1) and the original accepted alphabet A_i.
It includes x_i=0 exactly when b_i=0 and y_i=0. Put B=(n-1)r, concatenate
these bits in a fixed documented order, and let Decode_h(u) perform this map
and pivot elimination. Let S_h be the subset of F_2^B whose K pivot predicates
also pass. Decode_h restricts to a BIJECTION from S_h onto the accepted
residual fiber. No auxiliary-variable multiplicity is present in this encoding.

Write Z_h=|S_h|. Counting all accepted residual assignments gives

```
mu = E_uniform_h Z_h = (q/2)^m / q^K = 2^(B-K),
g(h) = Z_h/mu, E_h g(h) = 1.
```

The exact accepted Prange sampler draws u uniformly, checks the K pivots, and
retries on failure at the SAME h. Its per-trial success is

```
Z_h/2^B = g(h)*2^(-K).
```

Every accepted u has the same proposal probability. Conditional on acceptance,
the output is EXACTLY uniform, with expected trials 2^K/g(h) when Z_h>0. With
t trials, ABORT has probability (1-g(h)*2^(-K))^t; conditional output remains
uniform. Empty fibers abort under a finite cap. This is the benchmark, not a
biased search heuristic; see `independent_review_2026_10_22/CLASSICAL_SAMPLING.md`.

## 3. Good Syndromes And The Sharpened Variance Bound

Only a bound v_m=E_h(g-1)^2 <= rho is needed below. The earlier bound
rho=9^m q^(K-m) suffices. Here is a proof of the sharper support/Parseval bound,
to make the alternative count premise explicit without relying on a new oracle.

For a block of j>K original columns, let

```
r_i(a) = (2/q) sum_(x in A_i) (-1)^Tr(a*x).
```

Since |A_i|=q/2, r_i(0)=1. Fourier Parseval gives sum_a |r_i(a)|^2=2,
and hence sum_(a!=0) |r_i(a)|^2=1. Orthogonality gives the exact identity

```
v_j = sum_(z != 0 in F_q^K) product_i |r_i((H_j^T z)_i)|^2.
```

Use the existing inverse-trace coefficient bound |r_i(a)|<=beta for a!=0,
where beta=(1+2*sqrt(q))/q. Its character-sum input is the one already used
by the completion/restriction notes; it is not reproved here.

Fix an EXACT nonzero support S of size w in the [j,K] RS evaluation code.
Shortening outside S leaves dimension d=K-j+w, provided w>=j-K+1; otherwise
there is no nonzero word. Choose d information coordinates in S. Projection
is injective, and exact-support words project into (F_q^*)^d. Sum the product
of their d Fourier-square weights over this subset: it is at most the product
of the d nonzero square masses, namely one. The remaining w-d=j-K factors
are at most beta^2 each. Zero coordinates contribute exactly one. Thus

```
v_j <= sum_(w=j-K+1)^j binom(j,w)*beta^(2(j-K))
    <= 2^j*beta^(2(j-K)).
```

There is no extra q^d: the weighted information-coordinate sum already pays for
those values. Exact supports are disjoint, so there is no multiple counting.
This proof is uniform in the supplied points and target bits.

For j=m=K+r, take rho=2^(K+r)*beta^(2r), or any smaller certified upper bound.
Then log2(rho)=K-(n-3)r+O(r*2^(-n/2)). For fixed gamma>0, surplus
r=ceil((1+gamma)K/n) therefore suffices asymptotically for 2^-Omega(K) variance.
At any finite size use the actual bound, not that asymptotic statement.

Chebyshev gives Pr_h[|g(h)-1|>1/2] <= min(1,4*rho). Call the complementary
syndromes GOOD: 1/2<=g(h)<=3/2, so their fibers are nonempty. The algorithm
need not recognize goodness. An upper bound exceeding one is simply vacuous.

## 4. The Hash Law: All Matrices, Including Rank-Deficient Ones

Set k=B-K=log2(mu), an integer known without counting. Independently sample
each of the kB entries of M in F_2^(k by B) uniformly. For t in F_2^k define

```
C(M,t) = {u in S_h : M*u = t}.
```

Do NOT condition M on full rank, reject a hash because it is deficient, or
redraw until its cell is solvable. For any distinct u,v,

```
Pr_M[M*u=M*v] = p,  where p=2^(-k).
```

For three distinct binary vectors u,v,w, v-u and w-u are linearly independent
over F_2. Consequently their simultaneous collision probability is p^2.
This argument concerns BINARY hashes; it must not be substituted unchanged
for hashes over F_q, where three distinct points can lie on a field line.

If rank(M)=k, the ambient affine slice has dimension B-k=K BOOLEAN variables,
not K field variables. For rank d<k, a consistent slice has dimension B-d>K;
an independent t can instead make it inconsistent. Anchored slices are always
consistent. Row elimination is allowed, but it must retain these alternatives
and the originally sampled distribution. Even M=0 is included. For k=0 the
unique empty-row matrix is permitted and its cell is S_h.

For example, Pr[rank(M)<k] <= (2^k-1)*2^(-B) < 2^(-K) when k>0, by a union
bound over nonzero row dependencies. This small probability does not license
discarding the event: its cost must be included in the expected-clock premise.

## 5. Conditional Algorithm And Initialization Proof

Use the UNKNOWN complete-cell primitive specified in Section 7:

1. Draw fresh independent M and uniform t. Completely enumerate C(M,t).
   Retry an empty cell with fresh M,t at the SAME h. Choose any member of
   the first nonempty cell, without needing it to be uniformly selected.
2. Given current u, draw fresh M independently of the entire history and
   completely enumerate C(M,M*u). Select a uniformly random member of that
   complete, deduplicated list, including u itself.
3. Perform s transitions. Verify decoded outputs against all original
   residual equations. The composition also verifies the original full word.
4. Apply the single total clock in Section 8. Clock exhaustion or an invalid
   result produces ABORT, never a partial-list draw or a prefix restart.

For a nonempty S=S_h of size Z, set lambda=Zp=g(h). For independent uniform
M,t, each member is included with probability p, and each distinct pair with
probability p^2. For X=|C(M,t)|,

```
E X = Zp = lambda,
E X^2 = Zp + Z(Z-1)p^2,
Pr[X>0] >= (E X)^2/E X^2 = lambda/(1+(Z-1)p).
```

The inequality follows from Cauchy--Schwarz applied to X*1_(X>0). On good
syndromes initialization succeeds with probability at least 1/3 per trial.
No initial witness is supplied for free. Expected unanchored cell size is
at most 3/2. For EVERY fixed anchor u in S, the expected anchored size is
1+(Z-1)p<=5/2. These cardinality facts are not algorithms for finding cells.

## 6. Exact Reversibility And Uniform Minorization

Let P(u,v) denote the ideal anchored transition. For a fixed M the transition
is uniform inside a partition cell; its matrix is symmetric and stochastic.
Averaging over ALL M preserves both properties. The uniform distribution
pi on S is therefore stationary and reversible.

For u!=v let E be the event M*u=M*v. Conditional on E, both u and v lie in
the anchored cell, and each other w lies there with probability p, by the
three-point binary collision calculation. Thus

```
E[ |C(M,M*u)| | E ] = 2+(Z-2)p,
P(u,v) = p*E[ 1/|C(M,M*u)| | E ]
       >= p/(2+(Z-2)p).
```

The last step is Jensen's inequality for 1/x. For the diagonal, the per-M
probability of staying at u is at least its probability of going to any
fixed v, so the same bound applies when Z>=2. If Z=1 the chain is trivially
uniform and the bound also holds. Therefore, with

```
alpha = Zp/(2+(Z-2)p),
P(u,v) >= alpha*pi(v).
```

On good syndromes alpha>=lambda/(2+lambda)>=1/5. Write
P=(1/5)Pi+(4/5)R, where Pi has every row pi. The remainder R is stochastic
and has stationary law pi. Total-variation contraction under a Markov kernel
then gives, for EVERY initial distribution nu,

```
TV(nu*P^s, pi) <= (4/5)^s.
```

This includes the biased initialization above. There is no unproved mixing
assumption in this statement. Uniform cell selection, not an arbitrary SAT
model, is essential. It is a global parity-hash chain, not a coordinate-menu
chain, and imports none of the excluded menu arguments.

## 7. UNKNOWN Complete-Cell Enumeration Primitive

A sufficient missing lemma requires a SINGLE uniform algorithm ENUM and known
polynomial bounds, not a different advice-dependent solver for each h. For
every fixed supplied public residual instance there is a set E of uniform
syndromes of measure <=delta such that, for every good h outside E, ENUM has:

- Correct COMPLETE enumeration of distinct u in C(M,t), including correct
  termination on empty cells. It is Las Vegas, not a solver that sometimes
  declares UNKNOWN to be UNSAT or silently omits a subset of solutions.
- A KNOWN polynomial P(n) bounding expected cost per unanchored trial over
  fresh uniform M,t and ENUM's fresh internal coins.
- The same bound for anchored calls over fresh uniform M and internal coins,
  for EVERY u in S_h, not merely an average over uniform anchors. This is
  what permits adaptive, initially nonstationary trajectories.

The bounds include hash generation, setup, complete enumeration, memory/output
handling, independent verification, and exact uniform list selection for an
anchored call. They include rank-deficient hashes. Preprocessing costs a known
polynomial C0(n), including the original field/basis operations and elimination.
ENUM must be interruptible by the total operation clock even on bad syndromes.
Calls use fresh internal coins and no hidden trajectory-dependent state beyond
fixed public preprocessing. Reusing evolving solver state requires proving the
same conditional expected-cost bound after every possible preceding history.

Expected constant cell cardinality does not prove any of these runtime bounds.
Finding one verified model is not complete enumeration. In particular, the
final empty remainder must be decided after blocking all projected solutions.
No implementation in this note or its tests supplies this missing lemma.

## 8. Expected Work, A Fixed Clock, And ABORT Error

Fix 0<epsilon<1 and choose the least integer s>=0 with
(4/5)^s<=epsilon/2. This can be computed with exact rational arithmetic.
On good h outside E, let a>=1/3 be initialization success probability and
c<=P(n) its expected single-trial work. Trial cost may correlate with success.
Fresh independent retries nevertheless give expected initialization work
c/a<=3P(n): sum the expected cost of trial j times the probability the
preceding j-1 trials failed. No cost/success independence within a trial is used.

For transitions, condition on the complete history. The every-anchor premise
bounds the next expected work by P(n). The tower property therefore gives

```
E W <= Wbar = C0(n)+(3+s)*P(n).
```

An exact uniform choice from a list of length L can use unbiased random-bit
rejection on ceil(log2 L) bits; its expected cost is included above. Modulo
reduction of a fixed-width random integer is not an exact substitute.

Run the ENTIRE residual stage with deterministic operation budget

```
T = ceil(2*Wbar/epsilon).
```

If the ideal execution has not completed within T operations, output ABORT.
By Markov, Pr[clock exhaustion]<=epsilon/2 on every good h outside E. Couple
ideal and capped executions using the same coins until exhaustion. Their TV
distance is at most that probability, even if delays correlate adversarially
with the final witness. Combining with mixing gives e(h)<=epsilon, where
e(h) includes ABORT and compares to uniform on the nonempty fiber.

On other syndromes, the same clock still applies and e(h)<=1. For an empty
fiber, verified enumeration cannot output a witness, and the capped algorithm
outputs ABORT, matching the ideal empty-fiber kernel. Therefore

```
E_uniform_h e(h) <= min(1, epsilon + delta + 4*rho).
```

This supplies exactly the kernel hypothesis of completion transfer Section 4,
CONDITIONAL ON the enumeration lemma. With any valid variance bounds rho_U,
rho_T for the two original blocks and rho_U*rho_T<1, its full-fiber bound is

```
TV <= min(1, sqrt(rho_U)/2 + sqrt(rho_U*rho_T)
             + epsilon + delta + 4*rho_U + sqrt(rho_T)/2).
```

The ideal expected work on good syndromes is polynomial in n and log(1/epsilon).
This particular fixed-clock conversion is polynomial in n and 1/epsilon, NOT
in log(1/epsilon). Inverse-polynomial epsilon gives a polynomial clock;
exponentially small epsilon need not. No uncapped expectation is claimed on
exceptional syndromes. An ordinary backend timeout is not automatically a hard
clock for setup, enumeration, verification, or the whole workflow.

## 9. What Hashing Does Not Solve

For a full-rank M, scanning its ambient slice costs 2^K candidate checks.
Brute-force complete enumeration followed by mixing is no improvement over
the exact accepted Prange sampler and adds transition overhead. Reducing r
reduces B and k together: B-k=K remains EXACT. The new variance estimate
therefore improves the restriction but does not remove this solving exponent.

Neither near-flat syndrome counts nor the small expected list size supplies
conditional counts, a rational parametrization, a fast SAT solver, or the
complete enumeration lemma. Hashes operate on reciprocal trace-hyperplane
parameters; after elimination, the remaining K predicate equations are still
nonlinear. The zero-syndrome norm search and its restricted output family are
not arbitrary-syndrome cell solvers. Failed probes prove no hardness.

## 10. Exact SAT/XOR Probe Contract For A Later Implementation

This is a specification, not an implementation request in this change.

1. Load and preserve the original instance fields `bits`, `points`, `targets`,
   `checks`, `field_modulus_coefficients`, and its digest. For a saved residual
   run retain its `residual_indices`, accepted prefix, and `residual_syndrome`.
   Record I,J and their ordering. Do not replace the field modulus, public
   points, targets, U, prefix, or h because a backend prefers another input.
   For separate uniform-syndrome experiments draw h uniformly and label that
   source; do not silently replace a saved induced h with it or vice versa.
2. Compute and record c, the trace-kernel basis, and the u bit ordering from
   Section 2. Build y_i as affine binary expressions in u on J. Introduce
   x_i with `(x_i=0 AND y_i=0) OR x_i*y_i=1`, using carryless products reduced
   by the SAME field modulus. This includes legal zeros without extra lifts.
3. Express x_I=a(h)-D*x_J using original field constant multiplication.
   Introduce pivot inverse variables with the same total inverse graph and
   require their traces to equal the original b_i. These variables are
   uniquely determined by x_I; arbitrary circuit auxiliaries need not be.
4. Sample kB IID bits for M and, for initialization, k IID bits for t.
   Anchored t is M*u_current. Add the k XOR equations on u, NOT on raw x
   bits or all SAT auxiliaries. Record original M,t, rank, and any equivalent
   row-reduced system. Never silently force full rank or select easy hashes.
5. Enumerate projected u assignments. After a model, independently decode
   and check the original residual relation and M*u=t. Block that whole u
   with `OR_l(u_l != returned_u_l)`, not just a full auxiliary SAT model.
   Continue until UNSAT. Record UNKNOWN, time/resource limits, invalid models,
   and partial lists separately. A partial list is NOT a completed cell.
   Retain the final UNSAT status and, where available, its proof artifact;
   solver-reported completeness is not an independently checked certificate.
6. An anchored completed list must contain its supplied current u. Select
   uniformly only after completeness, retaining self-loops. Empty anchored
   cells indicate an error. A timeout/partial-list event aborts the proposed
   capped sampling run; do not draw from a partial list or keep only fast
   cells. Search-only witnesses may be reported as such, not as sampler output.
7. Charge field setup, encoding, XOR handling, every SAT/UNSAT call, blocking,
   deduplication, verification, index sampling, and whole-run clock control.
   Retain source, seeds, full hashes, complete/partial status, cardinality,
   ranks, elapsed times and operation/resource counts. Seeded probes are
   reproducible observations, not proofs of IID randomness or polynomial work.
8. Compare against accepted Prange on the EXACT same h and input. Independently
   enumerate small calibration fibers to test completeness and output laws.
   Distinct-looking witnesses, small observed cells, or fast successful calls
   alone do not establish the missing every-anchor expected-cost lemma.

## 11. Finite Controls And Limits

`tests/test_inverse_trace_hash_heatbath.py` is self-contained test arithmetic,
not a production sampler module. It exhausts small binary hashes INCLUDING
deficient matrices; checks moments, initialization success, reversibility,
minorization, contraction, and biased-choice countercontrols; checks restart
and clock/ABORT probability identities; and independently enumerates genuine
GF(16) native residual relations with N=16,K=2,m=4,r=2,B=6,k=4.

The GF(16) controls check the reciprocal-basis bijection, pivot elimination,
legal zeros, all 256 syndromes, exact Prange acceptance, and selected original
hash equations against direct accepted-word enumeration. They also check the
support/Parseval variance calculation. They do not exhaust all 2^24 native
hash matrices and do not measure native-size solver performance. No finite
control proves a polynomial enumeration algorithm, the unknown lemma, or a
speedup. No production solver, CLI, registry, or other file is changed here.
