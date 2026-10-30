# Mersenne Block Resampling: Mixing Versus Transition Cost

2026-10-30. Task C. Self-contained conditional mixing deductions, with
exact finite arithmetic controls; not independently reviewed or formally
verified. No native sampler was executed. No hardness or novelty claim.

## Result And Prior-Work Boundary

The residual count bound DOES imply rapid mixing of a specific family of
ideal overlapping-block heat baths. With a fixed buffer of 2K+1 coordinates,
updating the buffer plus one outside coordinate has spectral gap at least
rho^2/(6K), where rho is a positive absolute constant defined below. This
buffer-plus-coordinate comparison is the candidate incremental result of
this audit, not a claim of literature novelty. The two-large-block coupling
in Section 3 is PRIOR WORK by Popper, respecialized here to a 2K+1 buffer.
Both statements concern ideal conditional draws, not executed native chains.

Neither gives polynomial total runtime with the currently specified
classical implementation: exact systematic completion takes approximately
2^K trials PER heat bath. Making one trial and otherwise holding gives a
polynomial-cost, exactly reversible transition, but it needs exponentially
many steps to mix. A polynomial-cost conditional sampler meeting the
explicit contract below would close this particular algorithmic gap.

Read before deriving: the current top of `AGENT_HANDOFF.md`, the
[native target](../../MERSENNE_RECIPROCAL_RESEARCH_TARGET.md),
[global Fourier access](../../MERSENNE_GLOBAL_FOURIER_ACCESS.md),
[completion moments](../../MERSENNE_COMPLETION_MOMENTS.md), and the
classical-access audit's residual-completion section. Also checked the
inverse-trace completion-transfer and hash-heat-bath notes, and
[menu refresh](../../INVERSE_TRACE_MENU_REFRESH.md).

Follow-up provenance correction: the
[2026-10-29 six-agent report](2026-10-29-six-agent-research-burst.md),
under "Popper: nonlocal sampling and adversarial review", already records
two overlapping heat baths with a 3K reservoir, coalescence probability
at least (1-eta)/(1+eta), and the approximately 2^K direct implementation
cost. Parent had checked that argument. This source was inspected after
the initial draft, following the user's pointer; the draft's broad claim
of a new two-block mixing argument is withdrawn. Section 3 merely uses
the sharper existing all-syndrome count threshold to shrink the reservoir.

The menu-refresh mobility theorem uses only MDS and balanced alphabets;
it already transfers unchanged to this predicate. It is NOT a new
Mersenne result here. Our updates use whole accepted alphabets and a shared
large buffer, not independent small menus. Section 2 supplies a separate
buffer-plus-one-coordinate spectral comparison; no claim is made that an
exhaustive prior-art search establishes its novelty.
The systematic-completion acceptance formula is an existing comparator,
reused to charge the implementation, not presented as a new obstruction.
No coordinate Schmidt bound is used or rederived.

Evidence scope: the all-n native bounds below are analytic consequences
of the cited all-syndrome count theorem and the displayed proofs. The
count theorem is inherited, not newly proved or tested here. The finite
F_8 controls in Section 7 check formulas only; they neither establish the
canonical n>=17 theorem nor certify native execution, efficient conditional
sampling, or practical runtime. This audit's additional proofs have not
received independent review or formal verification.

## 1. Exact Input And The Count Premise

Keep, without modification,

```text
n odd prime >= 17; q = 2^n; N = n^2 = 8K+1; K = (N-1)/8;
s = floor((n-3)/4); f_s(x) = Tr(inv0(x)^(2^s-1)); inv0(0) = 0;
H[j,i] = alpha_i^j, 0 <= j < K;
A_i = {x in F_q : f_s(x) = b_i}; |A_i| = q/2;
Omega = {x in product_i A_i : Hx = 0}; pi = Uniform(Omega).
```

The public field representation, distinct alpha_i, and bits b_i are
arbitrary. No supplied witness, special layout, or changed predicate is
assumed. For a coordinate set B and syndrome h define

```text
Z_B(h) = #{z in product_(i in B) A_i : H_B z = h};
mu_B = (q/2)^|B| / q^K;
g_B(h) = Z_B(h)/mu_B.
```

Use the proved all-subset, all-syndrome bound from Completion Moments,
Section 3, not an average-syndrome assertion. Put

```text
m = 2K+1;
beta = (1 + 2^s*ceil(sqrt(q)))/q;
eta = beta*(1+beta)^m < exp(5/2)/30 < 1/2;
l = 1-eta; u = 1+eta; rho = l/u > 1/3.
```

For every fixed buffer U of size m, l <= g_U(h) <= u for EVERY h.
For any disjoint coordinate set V, independent accepted roots give

```text
g_(U union V)(h) = E_(z_V uniform product roots) g_U(h-H_V z_V).       (1)
```

Thus the same interval [l,u] holds for every superset of U. No count
evaluation is needed to prove (1). Let T be the complement of U,
F = |T| = 6K, nu = product_(i in T) Uniform(A_i), and

```text
g(a) = g_U(-H_T a); G = E_nu g = g_[N](0).
pi_T(a) = nu(a)*g(a)/G.                                           (2)
```

All prefixes a in this Cartesian product extend. The density in (2) is
bounded between rho and 1/rho. This bounded-density fact will control
mixing; it is not itself a way to generate a completion.

## 2. A Precise Fixed-Buffer Heat Bath

Fix U from the public indices, independently of any sampled values. For
each update, choose i uniformly in T, set B_i = U union {i}, and:

1. Retain x_(T\{i}). Compute h = -H_(T\{i}) x_(T\{i}).
2. Draw z EXACTLY uniformly from the accepted fiber H_B_i z = h.
3. Replace x_B_i by z. The resulting full word is still in Omega.

Every block has 2K+2 coordinates. All its conditional fibers are nonempty
by (1). Each update is a heat bath for pi; their random-scan average P is
reversible. Its transition does not depend on the old buffer values.

Here is a positive mixing proof. On the prefix a=x_T the induced chain Q
is the ordinary random-scan single-coordinate heat bath for (2):

```text
Q_i(a_i -> z | a_-i)
  = nu_i(z)*g(a_-i,z)/h_i(a_-i),
h_i(a_-i) = E_(w~nu_i) g(a_-i,w) in [l,u].                         (3)
```

After ONE ideal block update, conditional on the entire output prefix a,
the buffer is exactly uniform on its required fiber. Consequently for
every t>=1 and every initial native state,

```text
TV(Law(X_t), pi) = TV(Law((X_t)_T), pi_T).                         (4)
```

To prove a quantitative gap, let Q0 independently refresh a random prefix
coordinate under nu. For a real test function v, the Dirichlet form is

```text
E_Q(v,v) = (1/(2FG)) sum_i E_(nu_-i nu_i nu_i')
             [g(a)g(a')/h_i(a_-i) * (v(a)-v(a'))^2],
```

where a and a' differ only at i. Therefore

```text
E_Q(v,v) >= l^2/(uG) * E_Q0(v,v);
Var_pi_T(v) <= (u/G)*Var_nu(v);
E_Q0(v,v) >= Var_nu(v)/F.
```

The last inequality is the product-measure variance inequality, obtained
by revealing independent coordinates one at a time. Hence

```text
gap(Q) >= rho^2/F > 1/(9F).                                      (5)
```

There is no hidden full-state slow mode: conditional-mean-zero functions
of the buffer are killed by P in one step. On prefix-only functions P is
Q. Equivalently, apply (4). Also Q is an average of conditional-expectation
projections, so its eigenvalues are nonnegative. Expanding in its
orthonormal eigenbasis and applying Cauchy-Schwarz gives

```text
sup_(x in Omega) TV(P^t(x,.),pi)
  <= (1/(2*sqrt(rho))) * (q/2)^(F/2) * exp(-rho^2*t/F), t>=1.      (6)
```

Here pi_T(a)>=rho*(2/q)^F. In particular, for 0<epsilon<=1/4 it suffices
to take the ceiling of

```text
(F/rho^2) * [F*(n-1)*ln(2)/2 + ln(1/rho)/2 + ln(1/(2epsilon))],
```

and at least one update. This is O(n^5+n^2*log(1/epsilon)) ideal block
updates, uniformly in the public points and targets. It is a worst-start
bound, not a stationary-start argument.

## 3. Prior Two-Block Coupling, Respecialized

This is Popper's prior coupling mechanism, not a new positive mechanism.
Only the reservoir-size specialization uses the sharper count premise:
2K+1 here instead of the prior 3K. Partition T=A union B
with |A|=|B|=3K. A sweep refreshes A union U conditional on B, followed by
B union U conditional on A. Each refreshed block has 5K+1 coordinates.
Each heat bath preserves pi; their ordered composition need not be reversible.

For every fixed B assignment b, the conditional marginal of A is

```text
pi(A=a | B=b) = nu_A(a)*g_U(-H_A a-H_B b)
                         /E_(a'~nu_A) g_U(-H_A a'-H_B b)
             >= rho*nu_A(a).                                    (7)
```

Couple the first updates from ANY two native starting states by using
the common component rho*nu_A. With probability at least rho their new
A assignments agree. Their buffers need not agree yet. On this event,
the second update has exactly the same conditional distribution in both
chains, so it can make the entire states agree. Once equal, keep them
equal. Thus, for the sweep kernel S,

```text
sup_x TV(S^t(x,.),pi) <= (1-rho)^t < (2/3)^t, t>=1.               (8)
```

This is O(log(1/epsilon)) sweeps. The coupling is a mathematical proof
device; implementing the common-component decomposition is not being
granted for free. The algorithm only needs the two specified conditional
block draws, whose implementation cost is addressed next.

## 4. The Actual Classical Transition Cost

For either block B above, choose K pivot columns I in U, once and for all.
Every such minor is invertible. A systematic trial for fixed h is:

1. Draw the |B|-K free coordinates J independently and uniformly from A_j.
2. Solve x_I = H_I^(-1)(h-H_J x_J).
3. Accept iff every pivot predicate passes; otherwise reject.

There is one free-coordinate preimage for every accepted block word.
Consequently this is an exact uniform conditional sampler upon success,
with the EXACT per-trial success probability

```text
p_B(h) = Z_B(h)/(q/2)^(|B|-K) = 2^(-K)*g_B(h);
l*2^(-K) <= p_B(h) <= u*2^(-K).                                 (9)
```

It takes between 2^K/u and 2^K/l expected trials. Repeating at the SAME
h until success implements the ideal heat bath, but exponentially slowly.
At most L trials leave failure probability (1-p_B(h))^L; a uniform
failure bound delta is ensured by L >= (2^K/l)*ln(1/delta). Retain failure as
ABORT, rather than silently replacing it with a conditional sample.

These trials do not need a Walsh oracle or a field table. Write
d=2^s-1 and e=-d^(-1) mod(q-1). An accepted local root is x=v^e, with
0 mapped to 0, for a uniformly sampled trace-hyperplane element Tr(v)=b.
This takes n-1 fair bits and O(n) field operations per coordinate after
public trace-basis preprocessing. Zero is included exactly when b=0.

One can precompute H and H_I^(-1)H in O(NK+K^3+K^2N) field operations.
A conservative uncached trial costs O(KN+|B|n) field operations and
(n-1)(|B|-K) random bits. Schoolbook field multiplication costs O(n^2)
bit operations; input/modulus validation and preprocessing are polynomial
and charged. Full native verification costs O(NK+Nn) field operations.
The exponential factor in (9) remains after all of this polynomial work.

### One Trial Per Step Is Implementable, But Slow

Instead do just one systematic trial and hold at the old word on rejection.
For a chosen i in Section 2, its kernel is exactly

```text
R_i(x,.) = p_B_i(h)*P_i(x,.) + (1-p_B_i(h))*delta_x.               (10)
```

The probability p_B_i(h) is constant throughout each conditional fiber;
it need not be evaluated to execute (10). Thus R, the random-scan average,
is exactly reversible for pi and has polynomial expected cost per step.
Uniform selection of i uses fair-bit rejection with expected fewer than
two proposals; a strict cap can retain its separately bounded ABORT.

But from a point start x, the probability of no successful trial in t
steps is at least (1-u*2^(-K))^t. Hence

```text
TV(R^t(x,.),pi) >= (1-u*2^(-K))^t - 1/|Omega|
                >= 1-t*u*2^(-K)-1/|Omega|.                      (11)
```

In particular worst-start 1/4-mixing takes Omega(2^K) raw steps. This
is a cost statement about (10), not a lower bound on other algorithms.
For completeness, Dirichlet comparison gives the matching exponential
scale up to polynomial factors:

```text
gap(R) >= l*2^(-K)*gap(P) >= l*2^(-K)*rho^2/F.
```

Each R_i is also positive semidefinite. Since pi is uniform and
log|Omega|=O(nN), this yields an upper bound of
O(2^K*F*(nN+log(1/epsilon))) steps. Thus neither an unproved mixing
assertion nor a stationary-only calculation is hiding the runtime issue.

## 5. Exact Missing Contract, Initialization, And Failure Budget

The positive result would become a polynomial classical sampler if there
were a uniform algorithm S(B,h,delta) for the indicated original-coordinate
blocks, with all of the following properties:

- It uses the supplied points, targets and field, with no planted witness.
- For EVERY h, its law is within TV delta of Uniform({z in product A_i:
  H_B z=h}), including ABORT and invalid-output rejection in that error.
- Its entire running time is polynomial in n and 1/delta, including
  arithmetic, randomness, queries, preprocessing, and verification.
- Each call uses fresh randomness and the guarantee is uniform over the
  adaptively chosen h, not merely an average under a convenient source.

For Section 2 only the fixed family B_i=U union {i} is needed. Initialize
without a witness by drawing accepted roots outside one B_i and calling
S on the induced syndrome. This is a genuine initialization obligation,
not an assumed warm start. Then run t updates from (6), using error
delta per call. Uniform kernel-error coupling gives

```text
TV(actual full output,pi) <= ideal_mixing_error + (t+1)*delta.      (12)
```

For Section 3 the same argument uses 2t+1 calls. For example, budget half
epsilon to mixing and half to all call errors. Uniform-index draw failures
can be included in the same error ledger, with logarithmic per-draw caps.
No failure is discarded by conditioning. Finite-time mixing gives an
epsilon-approximate uniform sampler, not an exact uniform sampler.

For FIRST WITNESS, a verified completion from the initialization call
already suffices; uniformity and mixing are unnecessary. Conversely, a
chain defined only on Omega has not found its first witness by proving a
gap. The available systematic initialization costs approximately 2^K
trials, just as the full-instance comparator in the target note does.

### Scalar-Flat Work Does Not Automatically Instantiate S

The follow-up also inspected the mathematical construction in
[MERSENNE_SCALAR_FLAT_ATTACK.md](../../MERSENNE_SCALAR_FLAT_ATTACK.md).
This audit did NOT inspect or certify the sixth agent's implementation,
live artifact, or native execution results. That note explicitly separates
local construction success from global consistency/rank, and witness search
from uniform sampling. Its testing is separate from this audit's controls.

Even a proved polynomial-cost restricted-flat residual WITNESS routine
would not meet the conditional-law contract above. Sampling uniformly
inside a fixed product-flat intersection gives the uniform law on that
restriction, not on the entire accepted syndrome fiber. Randomizing the
flats does not by itself fix this: their incidence weights, varying
intersection sizes, success conditioning, and failures must be accounted
for in a proof of the full output law. A separate valid transition and
mixing analysis could exploit such a routine; substituting it for Step 2
does not inherit (4)-(8). A verified witness remains sufficient for the
separate first-witness objective.

The established signed Walsh evaluator and approximate local Fourier
sampler are polynomial written constructions, not missing-oracle blockers
and not native execution. This audit does not challenge them. What is
needed here is joint conditional completion, not another local query.
For example, the direct exact formula

```text
g_U(h) = sum_(t in F_q^K) (-1)^Tr(t dot h)
                       * product_(i in U) r_i((H_U^T t)_i),
r_i(0)=1; r_i(v)=(-1)^b_i W(v)/q for v!=0
```

has q^K summands even with polynomial signed Walsh evaluation. This
particular formula does not supply polynomial counts, let alone conditional
draws. It is not a lower bound on better ways to compute either.

## 6. Two Distinct Incorrect Inferences

**Near-uniform syndrome does not make conditional buffers close.** For
h!=h', the uniform accepted buffer laws at h and h' have disjoint
supports, so their TV distance is EXACTLY ONE, despite both g_U values
lying in [l,u]. This is a counterexample within every native input, not
a replacement predicate. A proposed coupling cannot identify whole
buffers merely because their fiber sizes are almost equal. Section 3
couples a different marginal first and only then refreshes the buffer.

**A completion witness is not a conditional uniform sample.** Existence
lets us define c(a) as the lexicographically first accepted buffer
completion of each accepted prefix a, using the public field encoding.
This is a mathematical selector, NOT a claimed efficient algorithm.
Any algorithm outputting only (a,c(a)) is supported on a section E with

```text
pi(E) = (q/2)^F/|Omega| = 1/(mu_U*G);
mu_U = 2^(n*(K+1)-(2K+1)) = 2^((n-2)K+n-1).
```

Its TV error is at least 1-1/(mu_U*G), irrespective of how well it mixes
the prefix. At n=17 this is at least 1-2^(-556)/(1-eta_N), using the
native full-count bound |G-1|<=eta_N. This quantifies on the exact native
relation why replacing the block sampler by an arbitrary solver destroys
the uniform-sampling conclusion. It does not impair that solver's value
for first-witness search. The general witness-versus-sampler distinction
was already explicit in the completion-transfer note.

## 7. Bounded Checks And Disposition

Exact rational calculation of the displayed canonical envelopes gave:

| n | K | Buffer m | Heat-bath block | eta upper, rounded | rho^2, rounded |
|---|---|---|---|---|---|
|17|36|73|74|0.10980441|0.64339546|
|19|45|91|92|0.16213385|0.51980087|
|31|120|241|242|0.00536966|0.97875021|
|61|465|931|932|0.00001090|0.99995641|

The proofs use rational beta*(1+beta)^m and rho, not rounded table entries.
Also checked n=23 and 127. These are analytic parameter calculations, not
native execution timings or measured transition probabilities.

A standalone inline standard-library control used F_8 with modulus
X^3+X+1, inverse trace (s=1), N=5, K=1, alpha_i=i, targets (0,1,0,1,1),
U={0,1,2}. This is explicitly NONCANONICAL and proves no native runtime.
Enumerating the 120 witnesses and both 120-row transition matrices with
exact Fraction arithmetic verified stochasticity and detailed balance
for P and R, the acceptance identity (9), and the exact conditional-buffer
refresh used in (4). The eight buffer fiber sizes were
(6,10,10,6,10,6,10,6), giving eta=1/4. The selector section had uniform
native mass 2/15, agreeing with 1/(mu_U*G).

A second exact control formed the 16-state projected chain and checked
that diag(pi_T)*(I-Q) - (9/50)*(diag(pi_T)-pi_T*pi_T^T) is positive
semidefinite by rational Schur elimination. Here 9/50=rho^2/F, directly
testing (5). For two overlapping blocks with one outside coordinate each,
the exact one-sweep Dobrushin coefficient was 1/8, below the proved
1-rho=2/5; stationarity was also checked exactly. These are finite checks
of the positive mixing arguments, not only their invariant distributions.
No tables were used as a scalable algorithm, and no code or registry
artifact was added.

Disposition: **buffer-plus-coordinate gap deduction; prior two-block
coupling correctly attributed; explicit exponential cost for the specified
implementation; polynomial total-time uniform sampler still unproved.**
The specific remaining constructive target for these heat baths is
S(B,h,delta), with the all-syndrome distribution guarantee and charged cost
in Section 5. Better residual counts or restricted-flat witnesses alone do
not instantiate it.
