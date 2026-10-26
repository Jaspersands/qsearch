# Nonlinear Taylor-Jet Receiver Proposal

2026-10-21. CONSTRUCTIVE DERIVATION, UNDER REVIEW. Public symbolic algebra
and finite channel controls are implemented. No complete quantum receiver,
independent proof review, novelty certification, central candidate admission
or useful external speedup is established. In particular, passing these
tests does not establish a new quantum algorithm.

CLASS-THREE-NORMAL EXTENSION UNDER REVIEW (2026-10-21): see
CLASS_THREE_MONOMIAL_FULL_JET.md. It uses an additional COHERENT Fourier
coordinate, FULL Taylor jets and GL alignment instead of this note's
top-cancelling Weyl alignment. Its phase bound is max(c,3D), and its
second erasure runs D,...,1. The old counts and source compiler below
cannot be reused unchanged. This is not yet an independently validated
scope extension or a universal resource improvement.

PREFERRED SOURCE UPDATE (2026-10-21): CENTRAL_REGULAR_JET_SOURCE.md replaces
the irreducible matrix-source construction below by central-only Fourier
and a fixed-width regular carrier. It removes radical selection, nonzero
label rejection, equivariance-dependent rank selection and mixed padding.
The Taylor transport and both erasures below remain necessary. Sections
4 and 10.2 retain the older irrep variant for comparison; use the replacement
note's source/rank/cost formulas for the preferred route. Neither variant
is a completed quantum implementation or independently validated theorem.

## 1. Question, Scope, And Proposed Gain

The previous receiver needs a quadratic noncentral potential. The valid
class-five counterexample in CLASS_FOUR_HSP_THEOREM_DRAFT.md defeats that
premise: its cubic coefficient does not commute with the derived algebra.
Do not retract that counterexample. Instead retain a NONLINEAR graph,
erase its phase using a public weighted affine action, Fourier-measure the
graph registers, then erase the resulting ordinary polynomial phase.

Fix c>=4. Input: a public finite-dimensional Lie algebra L/F_p of class
at most c, p>max(c,2(c-2)), with L' of class at most TWO; ordinary coherent
HSP access on exp(L), unique Lie coordinates, and arbitrary hidden H.
All bracket arithmetic, oracle access, Fourier precision and source
consumption are charged. The target conclusion is bounded-error quantum
polynomial time in dim L, log p and input/oracle cost, for each FIXED c.
This is a proposed theorem conditional on the complete source/composition
arguments below, not a result promoted from experiments.

This scope includes every class-five algebra: [L',[L',L']] is contained
in gamma_6(L)=0. It strictly weakens [gamma_3(L),L']=0 in the previous
structural note. It does NOT include all class-six algebras, growing c,
arbitrary black-box encodings, prime-power exponent, or DCP. The smaller
primes excluded by this presentation are not handled by the new code.
Known bounded-prime algorithms are a possible separately charged fallback.

Expected advantage, if correct and not already known: time-efficient HSP
for a broader growing-prime nilpotent family, rather than another query
advantage with exponential postprocessing. There is still no natural hard
application. Explicit sparse-object and suitable polynomial stabilizer
families remain subject to the classical attacks in the application audit.
Opaque-oracle scope alone is not a Shor-level practical contribution.

## 2. Common Potential And Its Degree

First assume H intersect N=1, N=exp(L'). Then H is abelian. Fix the SAME
proof-only projection pi:V=L/L' -> U=HN/N, public linear section s, and
linear hidden lift a:U->L' throughout the experiment. Define

```
g(q)=exp(s(q-pi(q))) exp(s(pi(q))+a(pi(q))) exp(-s(q)),
Q(q)=log g(q), W=L'/Z(L'), w=dim W, m=dim V, z=dim Z(L').
```

The section-word identity and mixed-source Fourier reduction in
CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md use only transversality and class-two
N, not a quadratic Q. Their group/source argument therefore supplies the
same matrix source, now with higher-degree Q. This reuse must retain the
full measured transcript, trace the oracle-output register and multiplicity
row, and keep radical characters. It is not an assumed oracle for Q.

Truncated BCH gives deg Q<=c. A homogeneous degree-j coefficient is a
sum of Lie words of filtration weight at least j: s(q) has weight one,
whereas a(pi(q)) is linear in q but has weight two. For j>=c-1 these
coefficients lie in gamma_(c-1)(L), which commutes with L'. Hence, with
D=c-2,

```
deg Q_W <= D,                  deg Q_Z <= c.
```

This filtration argument distinguishes polynomial degree from Lie weight.
The old cubic obstruction in UT6 is now within the allowed D=3 potential.
If w=0, use the existing scalar/metabelian argument; no matrix jet is needed.

## 3. A Finite Common Jet Closed Under Translations

Write Q_W(q)=sum_nu theta_nu q^nu, with theta_nu in W and |nu|<=D.
For 1<=k<D and |alpha|+k<=D retain the W-valued homogeneous components

```
F_(alpha,k)(q) = sum_(|beta|=k) binom(alpha+beta,beta)
                              theta_(alpha+beta) q^beta.
```

Stack scalar coordinates in (k,alpha,a) order, a in W. The retained width
is J=w*(binom(m+D,m+1)-1). This is polynomial for fixed D. Do not replace
these redundant but closed coordinates by an arbitrary compressed basis.
Let Q_D be the homogeneous degree-D part, which is NOT retained. Then

```
Q_W(Y+s*q)=Q_W(Y)
          +sum_(alpha,k) s^k Y^alpha F_(alpha,k)(q) + s^D Q_D(q).       (1)
```

The retained vector satisfies a second, crucial identity:

```
F_(alpha,k)(Y+s*q)=F_(alpha,k)(Y)
 +sum_(|delta|<k) binom(alpha+delta,delta) Y^delta s^(k-|delta|)
                  F_(alpha+delta,k-|delta|)(q).
```

Thus F(Y+s*q)=F(Y)+A(Y,s)F(q), where A is PUBLIC. Its diagonal is s^k
on weight-k coordinates and all other entries go to lower weights. It is
invertible for s!=0. The binomial identity follows coefficient by
coefficient from

```
binom(alpha+delta+nu,delta+nu) binom(delta+nu,nu)
 = binom(alpha+delta,delta) binom(alpha+delta+nu,nu).
```

No theta, pi, a, F(Y), or F(q) is evaluated by the receiver. Computing
A requires only Y,s and the chart. At D=2 it reduces to the old linear jet.

## 4. Matrix Alignment And Rank Probability

Use the same public alternating-form factor D_lambda:W->carrier as before,
including variable radicals and zero-dimensional irreps. Collect a verified
label relation sum_i s_i^(2D) lambda_i=0. After the fresh quotient shear,
define blocks

```
K_i=s_i^D D_lambda_i,
J_i=[s_i^k Y_i^alpha D_lambda_i]_(alpha,k).
```

The image of K is isotropic. If [K J] has full column rank w+J, the
existing deterministic symplectic isometry extension, with REAL maximally
mixed padding to R>=w+J, gives (SK)_X=0 and (SJ)_X=(I_J,0).
Consequently the aligned X displacement is (a_Y+F(q),b_Y), with the SAME
nonlinear F for every batch. Z displacement has ordinary degree <=D.
The exact Clifford phases and paid circuit synthesis are inherited, not
replaced by projective equality or a free dense unitary.

Here is a sufficient rank bound, not an empirical extrapolation. Use B
independent relation blocks. Canonical-row-space degree-2D SDE selection
makes the first active label uniform nonzero by the existing equivariance
argument. Select it without using Y or a rank test, and multiply its
block witness by an independent uniform tau in F_p*. The selected s is
then uniform nonzero conditional on its label/witness. Y is independent
uniform from the actual mixed-source shear.

For any fixed nonzero vector in the w+J-dimensional proposed kernel,
divide its selected row by s. Its W-valued polynomial is

```
s^(D-1)*v_top + sum_(alpha,k) s^(k-1) Y^alpha v_(alpha,k).             (2)
```

These monomials are distinct and have degree <=D-1. Some coefficient
v!=0 survives D_lambda with probability at least 1-1/p, since the common
radical is zero. Conditional on survival, Schwartz--Zippel on
F_p* x F_p^m bounds polynomial vanishing by (D-1)/(p-1). A block fails
for this vector with probability at most D/(p-1)<=1/2. Independence gives

```
Pr[rank deficient] <= (p^(w+J)-1)*(D/(p-1))^B,
B=(w+J+1)*bit_length(p)+2  ==> bound <= 1/(4p).
```

This is a marginal rank argument, NOT uniformity conditional on the entire
new transcript. Abort/selection must respect the earlier equivariance
contract. Shared blocks, truth-dependent selection, label-dependent aborts
or copied source purifications invalidate the proof. `rank_schedule` only
evaluates the bound; it does not certify any of these premises or solve SDE.

## 5. The Nonlinear Scalar Source

Measure ONLY the spectator positions. Every outcome is uniform. Put
v=m+J. Direct contraction of symmetric Weyl matrix entries gives

```
rho[(q,t),(q',t')] = p^(-v) [q'-q in U]
                    [t'+F(q')=t+F(q)] omega^(P(q,t)-P(q',t')),
P=-psi-A_X.B_Z/2-B_Z.(t,spectator).
```

This is a positive normalized density: a proof-only controlled translation
and phase applied to rho_U tensor I/p^J. It is generally NOT a subgroup
state. NonlinearJetChannel now checks the spectator contraction, not a
general density-operator positivity theorem. The old common-LINEAR-graph
theorem must not be used for this nonlinear support.

Give q coordinates weight one and t_(alpha,k,a) weight k. Since A_X has
degree <=D-1 and B_Z degree <=D, P has weighted degree

```
e=max(c,2D-1).
```

Its coefficients are public linear maps of a fixed lift containing Q_W,
Q_Z coefficients and pairwise products of Q_W coefficients. They are not
new independent unknown coefficients for every batch. The new compiler
checks the COMPLETE nonconstant X map against F, not only its degree.

## 6. Physical Merge And Weighted Cancellation

For independent packets from the SAME fixed hidden instance/chart:

1. Choose scales from public weighted leading-coefficient maps BEFORE
   observing new outcomes. Discard zero-scale inputs and charge them.
2. Prepare fresh coherent uniform q; subtract s_i*q from input q_i and
   measure Y_i. Do not use an old packet as the fresh pivot.
3. Prepare fresh coherent uniform t; compute A(Y_i,s_i), subtract A_i*t
   from input t_i, then measure Z_i. No unknown F(Y_i) is subtracted.

The inverse addresses are q_i=Y_i+s_i*q and t_i=Z_i+A_i*t. For each
active input, its support becomes exactly

```
q'-q in U,  A_i*(t'-t+F(q')-F(q))=0,
```

which equals the required common relation because A_i is invertible.
Every outcome tuple has probability p^(-v*b), b active inputs. The branch
Kraus amplitude is p^(-v/2) times its address indicators. Completeness is
also immediate from the two reversible subtractions and measurements.
Independent normalized source diagonals give the uniform probability law;
this is not postselection or evidence of success from uniform rates alone.

The pulled-back phase is sum_i P_i(Y_i+s_i*q,Z_i+A_i*t). Its top weighted
degree-d coefficient map is sum_i s_i^d C_i, independent of Y_i,Z_i:
the associated graded action is q->s_i*q and t_k->s_i^k*t_k. A verified
diagonal identity for EVERY unknown-parameter row removes that degree.
Iterate d=e,...,1 on disjoint trees. Translation cross-terms are necessary
even though they do not affect the leading graded action. Ordinary total
degree, which weights every t equally, gives invalid witnesses here.

After this stage P is constant. The support remains nonlinear; DO NOT
apply ordinary subgroup Fourier sampling to the combined (q,t) registers.

## 7. Fourier Readout And A Second Erasure

Apply negative Fourier to t and measure eta in F_p^J. All eta are uniform,
and ALL are retained. Summing the relation t'=t+F(q)-F(q') gives

```
rho_eta[q,q'] = p^(-m) [q'-q in U]
                omega^(eta.F(q)-eta.F(q')).
```

The remaining phase has ordinary degree <=D-1; its coefficient map is
public in eta, using the original SAME theta. `fourier_curve_packet`
constructs that map without evaluating F. Now use ordinary scalar affine
phase erasure through degrees D-1,...,1 on independent first-stage roots.
Only after this SECOND erasure is ordinary Fourier sampling of U valid.
Postselecting eta=0 would instead incur p^J cost and ruin the argument.

## 8. Cost And Arbitrary-H Finish

Let hW=w*binom(m+D,D), hZ=z*binom(m+c,c), and
P=1+hW+hZ+hW*(hW+1)/2. Safe public equation counts are
E_d=P*binom(v+d,d) in weighted erasure and
E'_j=hW*binom(m+j-1,j) in final ordinary erasure. These intentionally
overcount zeros and dependencies. No sparse-equation heuristic is required.

Use the already-audited fixed-degree diagonal solver of
[Ivanyos--Santha, Theorem 11 and Section 3.3](https://arxiv.org/pdf/1503.09016):

```
a_j(E)=(j^(j*(j-1)/2)*(E+1)^j)^ceil(log2(j+1)), j>=2;
a_1(E)=E+1.
```

For t final Fourier samples a conservative raw scalar-root count is

```
M=t * product_(j=1..D-1) a_j(E'_j) * product_(d=1..e) a_d(E_d).
```

Each such root needs a matrix batch of T=B*a_(2D)(z) accepted nonzero
central labels. Cap rejection sampling for each label at
ceil(log_(p^z)(8T)) draws; cap rejection for each nonzero random block
multiplier so its total failure is <=1/8. Together with the rank bound,
a fresh matrix trial fails with probability <1/2. Repeating at most
ceil(log2(4M/epsilon)) times per requested root gives a bounded source
schedule. Charge ALL attempted queries, solver work, discarded inputs,
padding, phase tables, transformations, approximate gates and classical
records. Final samples t=m+ceil(log_p(4/epsilon)) suffice for the usual
subspace spanning bound. Split the other failure/precision budgets over
the complete workflow; these formulas are not an optimal resource bound.

Every factor is polynomial in dimension and log p at FIXED c, but the
degree and constants are very large. No old class-four query exponent or
live resource artifact applies unchanged. The new module only verifies
supplied high-degree SDE witnesses; the generic solver is NOT implemented.

For arbitrary H, use the known nil-2 solver to learn K=H intersect N,
pass to N_G(K)/K and apply the transverse image receiver. Class-two derived
algebra is inherited by subalgebras and quotients. H is then abelian. For
T=HN, T' is contained in gamma_3(G), so the ambient class drops by at
least one. Repeat quotient-image descent at most c-2 times and finish with
known nil-2 HSP. Later derived groups need NOT be abelian at general c;
do not blindly switch every subsequent call to the old scalar receiver.
Retain bounded off-promise clocks and canonical-output amplification in
one fixed chart. A wrong early K is a charged failure, not a new promise.

## 9. Prior Art, Attempts To Falsify, And Remaining Work

Polynomial phase cancellation is prior art:
[Decker--Hoyer--Ivanyos--Santha](https://arxiv.org/abs/1305.1543).
The class-two QFT, SDE theorem, Fourier conversion of graph coordinates,
and subgroup descent are not claimed as new. Compare also
[Imran--Ivanyos](https://arxiv.org/abs/2304.08376), whose bounded-prime
result does not by itself give a growing-prime runtime. A current search
also found [Morales](https://arxiv.org/abs/2608.05321) on particular
semidirect products and quasi-Hamiltonian groups, not a demonstrated match
to this entire proposed scope. This is NOT exhaustive novelty certification.

### 9.1 Access-Matched Prior-Art Audit (2026-10-21)

Do not claim that existing polynomial-graph algorithms only handle fixed
dimension. [Decker--Ivanyos--Santha--Wocjan, Theorem 5 and Section 5.3](https://arxiv.org/pdf/1107.2189)
already solve constant-degree MULTIVARIATE scalar-output HPGP with an
oracle, using restrictions and interpolation. Section 5.2 also treats
function-graph groups: translation actions on polynomial spaces are not
themselves new. The [Decker--Hoyer--Ivanyos--Santha state algorithm](https://arxiv.org/pdf/1305.1543)
uses full-domain univariate graph superpositions.
[Ivanyos--Santha, Theorem 5 and Corollary 6](https://arxiv.org/pdf/1503.09016)
extend that state-input setting to growing output dimension and constant
degree. These are essential predecessors, not unrelated benchmarks.

The interface difference that still needs resolving is UNKNOWN proper U:
our mixed source has coherence only when q-q' lies in U. It does not
provide arbitrary restricted HPGP oracle queries or full-domain graph
states. In fact, for U=0 its density is I/p^(m+J), independent of F and
the unit phase. More generally F and F+C give identical kernels whenever
C is constant on U-cosets. These are exact source nonidentifiability
statements, now machine-checked below. They invalidate a black-box demand
to learn every coefficient from this abstract source. They are NOT a
lower bound against all HSP-to-HPGP reductions: actual group-derived F
has additional constraints; for H=1 the chosen potential is zero.

Simply measuring down to random affine lines does not close this gap.
For U of dimension k in V of dimension m, a uniform nonzero line
direction lies in U with probability (p^k-1)/(p^m-1). Otherwise the
restricted source is diagonal in the line coordinate. This can cost
p^(m-k); it is not an automatic efficient simulation of the published
univariate graph-state interface. This observation rules out that
specific shortcut, not every possible reduction.

The general fixed-degree SDE dependency also survived source-level
inspection: Section 3 reduces the exponent using a gcd/Bezout calculation;
Section 3.1 constructs representatives with bounded restarts, without
assuming an uncharged discrete-log or nonresidue oracle. This checks the
published dependency, not a local implementation or the equivariance of
an arbitrary solver wrapper. The proposed scope is not subsumed by the
bounded-prime theorem merely by treating p as a parameter. Morales's
scalar-action and quasi-Hamiltonian families do not establish the full
nonabelian-derived class-five scope. No exhaustive novelty claim follows.

### 9.2 Machine-Checked Nonlinear Channel

`formal/Formal/NonlinearJetChannel.lean` derives the actual two-sum Kraus
contraction for a tensor product of same-curve sources. Public transport
`(q,t)->(Y+s*q,Z+A(Y,s)t)` preserves and reflects the nonlinear relation
under nonzero s, injective A and the stated curve identity. The module
checks complete Kraus normalization, uniform joint-outcome probabilities,
the nonlinear Weyl-spectator conversion, every unit-character Fourier
residual, and the two nonidentifiability statements above. It does NOT
substitute a linear graph for the nonlinear support. The nine headline
theorems have standard-axiom guards and are imported by the normal build.

This removes one FORMAL channel gap, not the full receiver proof debt.
Taylor closure is a hypothesis of this GENERIC channel module. The later
FullTaylorTransport.lean discharges it on the full finite coefficient
space, and FullJetAlignment.lean derives public source alignment from
feature injectivity for the full-jet replacement. Neither result should
be silently relabeled as a proof of this older truncated/Weyl protocol.
WeightedPhaseErasure.lean now proves coefficientwise weighted cancellation
from strictly lower-weight generator images and a verified diagonal
relation. FullJetWeightedErasure.lean now derives the full Taylor
coefficient matrix and composes the erasure law with the actual mixed
branch for the full-jet replacement. Random rank/SDE guarantees, all-stage source
independence, efficient gates and arbitrary-H recursion are not formally composed.
Positivity is not separately proved in a general density-operator library.
The character calculation is for each unit additive character, not a
standalone proof of a complete implementable character transform.
Noncomputable matrix kernels are specifications, not quantum execution.

### 9.3 Falsifiers And Next Work

Decisive controls and limitations:

- Multivariate exact Taylor/transport identities and composition checked
  at small primes and a 127-bit prime. Cubic top-degree public alignment
  and symbolic phase compilation checked across distinct batches. This
  checks coefficient maps, not exponentially sized quantum executions.
- Actual Weyl spectator contraction gives the nonlinear density. Physical
  two-step Kraus contractions check full/proper U; an exhaustive small
  instrument sums to identity. Their small fields need not satisfy the
  proposed higher-class HSP bound: these test channel identities only.
- Removing the Y-dependent cross-term damages the retained state while
  keeping uniform trace. Using ordinary instead of weighted degree and
  cancelling only at a hidden test value are rejected.
- All Fourier outcomes give the stated residual polynomial phase. Only
  eta=0 is phase-free in the closed-curve control. A second erasure is
  mathematically essential, not optional cleanup.
- Physical independence, one common hidden potential and adaptive timing
  are protocol obligations, not properties proved by equal Python schema
  strings. The algebra helpers do not own or consume quantum sources.

What would kill the route: a legal source transcript outside the stated
Weyl kernel; a failure of common-parameter compilation; nonuniform rank
selection under the actual bounded SDE controller; a hidden-dependent
transport or survivor choice; a weighted term not reduced by the diagonal
identity; or a superpolynomial dependency at fixed c. Known classical
algorithms or matching prior art could also eliminate its research value
even if the algebra is correct. None is ruled out by the finite controls.

Section 10 now gives a concrete costed controller at the WRITTEN-proof
level. The rank argument, common hidden-potential construction and adaptive
two-erasure composition still need independent review. The new nonlinear
channel theorem has explicit premises; existing linear Lean theorems must
not be relabeled as covering the whole receiver. Further work should attack
a substantive dependency, scope obstruction or useful application, not
start another nearby finite-fixture campaign or promote a speedup claim.

## 10. One Controller For The Whole Two-Erasure Construction

2026-10-21 composition audit. The following is a WRITTEN argument under
review, not a new Lean theorem or an executed receiver. Its purpose is to
instantiate the probabilistic and quantum premises in ONE algorithm,
rather than assume that separately correct local lemmas compose.

### 10.1 Fixed Instance And Complete Classical Record

Fix the original hiding function and a correct public chart for the
current transverse image problem. Fix pi, a, Q, F and the coefficient
lift ONCE as mathematical witnesses. They are not sampled anew, estimated,
or supplied to any controller. Conditioning below is on the receiver's
classical record r: measured representation labels, solver seeds/outputs,
random multipliers, measured shear/spectator coordinates, rank decisions
and retry counts. Discarded oracle outputs and multiplicity rows are NOT
additional conditioned records.

At every program boundary the retained CQ state has the form

```
sum_r mu(r) |r><r| tensor product_(a in live(r)) sigma_a(r; H,Q).
```

The classical law mu need NOT factor over packets. Coefficient tables may
be correlated or chosen adaptively. The assertion is conditional PRODUCT
form of the unconsumed quantum registers, for this fixed instance. No
decoupling from an inaccessible external quantum purification is claimed.

Proof by program induction:

- A fresh ordinary uniform query on new registers, with hiding output
  traced, supplies an independent rho_H. The measured class-two normal
  QFT gives the previously derived matrix kernel in each observed sector.
- Label selection, solver work, retries and grouping read only r and fresh
  independent random bits. Such classical processing does not alter the
  conditional quantum factors. Keep the complete record; forgetting a
  shared random choice before asserting a product can invalidate this step.
- A physical merge acts only on its selected, disjoint quantum factors.
  Its exact local branch identity replaces those factors by ONE new
  normalized factor. Untouched factors remain a tensor product because
  the operation and its outcome probability act only on the consumed
  subsystem. All used inputs are removed from live(r), including zero-scale
  discards; none can be reused in a sibling or later tree.
- A public rank rejection discards the entire attempted matrix batch. A
  fresh trial starts from new sources. Acceptance may correlate classical
  records inside that batch; its conditional output still has the exact
  formula for its observed record. No accepted-label uniformity is needed.

Consequently state correctness can be proved conditional on FULL r,
although selected-label uniformity cannot. The latter is used only for
the ex-ante chance of preparing a fresh matrix leaf.

### 10.2 A Bounded Matrix-Leaf Procedure

Set L=w+J, B=(L+1)*bit_length(p)+2 and A=a_(2D)(z). Set T=B*A.
For each attempted matrix leaf:

1. Independently prepare B blocks of A accepted nonzero central labels,
   keeping every radical character and quantum carrier. For each slot
   allow at most r_lambda=ceil(log_(p^z)(8T)) raw ordinary queries;
   a slot that sees only zero labels makes this whole attempt ABORT.
2. Apply the deterministic published SDE solver to each label matrix's
   canonical row space. Verify the degree-2D witness against the original
   labels. Select the first nonzero coordinate using only that witness.
   The proof uses the all-input fixed-degree solver guarantee, not a
   heuristic expected success rate. Invalid outputs are never used.
3. Independently multiply each block witness by a uniform nonzero tau.
   Generate it by at most r_tau=ceil(log_p(8B)) uniform field draws,
   aborting this attempt if all are zero. Discard zero-scale packets.
4. Perform the single fresh-q matrix shear across the active packets.
   Record all Y, construct K/J, and reject if full rank fails. On success
   perform the deterministic symplectic alignment with actual mixed
   padding and exact Weyl covariance, then measure the spectators.
   Return the nonlinear source and its public coefficient table.

Step 2 can choose no quantum state based on its unknown contents. Its
canonical input, deterministic solver, witness and selected index are
unchanged by a simultaneous GL_z transform of the nonzero labels. This
gives uniformity of the selected label before conditioning on new labels.
Discarding lambda=0 independently in each slot preserves a product law.
Tau supplies an independent uniform nonzero selected scale. Conditional
on labels/scales, the COMPLETE Y tuple is uniform by the matrix-channel
identity, even though a single fresh q was shared by the shear. Thus the
selected triples (lambda,s,Y) factor over blocks for the rank estimate.

This law is valid conditional on any PRIOR controller history and valid
fixed chart. It is not asserted after conditioning on the new full record,
or on passing the rank test. The per-attempt failure bound is

```
T*p^(-z*r_lambda) + B*p^(-r_tau) + (p^L-1)*(D/(p-1))^B
 <= 1/8 + 1/8 + 1/(4p) < 1/2.
```

There is no solver-abort term in the ideal deterministic published
construction. A practical partial solver would need its OWN uniform
success/runtime theorem and cannot inherit this bound. The deterministic
bit-operation clock must depend on the public input size, not on labels
or irrep rank. The controller never conditions away a failed attempt.

### 10.3 Fixed Trees, Changing Public Coefficients

Use fixed maximum arities, not outcome-dependent tree sizes. Define the
bottom-up arity list

```
(a_e(E_e), ..., a_1(E_1), a_(D-1)(E'_(D-1)), ..., a_1(E'_1)).
```

At a weighted node collect the prescribed number of fresh child roots,
form all public leading-weight coefficient columns, and solve/verify
the degree-d diagonal relation BEFORE measuring any new Y or Z. Zero
scales are discarded. The nonlinear channel and associated-graded law
then give degree <=d-1 for EVERY branch, using the SAME parameter lift.
The SDE theorem handles arbitrary coefficient matrices; independence of
those classical columns is neither assumed nor needed.

After weight one is removed, each successful root is exactly the same
phase-free nonlinear density, independent of its record. Fourier-measure
all jet coordinates and retain every eta. The conditional state becomes
rho(U,eta.F), with a public table linear in the fixed noncentral theta.
At each subsequent ordinary node, the affine channel removes the leading
ordinary degree for every outcome. At the final root the phase is constant
and cancels from the density: the output is exactly rho(U,0).

In particular, on successful transcripts r the joint root and record are
`mu(r) |r><r| tensor rho(U,0)`. Summing any collection of successful records
does not change the normalized root. Fresh completed roots therefore give
uniform U-perp Fourier rows even conditional on all earlier rows and
controller records. This is the justification for the spanning estimate,
not an assumption that all adaptive public coefficient tables are IID.

### 10.4 Whole-Call Failure, Queries And Workspace

Let eta be this image call's error allowance and put
`t=m+ceil(log_p(4/eta))`. Let M be the Section 8 number of matrix leaves
across t final roots. Allow
`R=ceil(log_2(4M/eta))` complete attempts for EACH matrix leaf. A
first-failure/conditional union bound gives

```
Pr[any exhausted leaf] <= M*2^(-R) <= eta/4,
Pr[Fourier rows fail to span] <= (p^m-1)/((p-1)*p^t) <= eta/4,
Q_image <= M*R*T*r_lambda.
```

These count discarded leaves and entire rejected batches. With all
arities at least two, the number of scalar merge calls across both stages
is strictly less than M. A level's node count is t times the product of
the arities AFTER that level, not the product before it.

Exact uniform classical field draws are not free unbounded loops. There
are at most S=M*R*B*r_tau such draws for the multipliers. Uniform binary
sampling of bit_length(p) bits rejects values >=p with probability <1/2.
Cap each such rejection sampler at ceil(log_2(8S/eta)) trials. Its global
exhaustion probability is <=eta/8, and accepted field elements are exactly
uniform. Reserve another eta/8 for the sum of COMPLETE quantum-instrument
errors, including uniform-state preparation, QFTs, phase/Clifford synthesis
and all adaptive branch labels and ABORT. Contractivity/hybrid composition
is performed BEFORE any conditioning; no rare-branch division is allowed.
The resulting bound is at most 3*eta/4, with slack for other charged
implementation details. Approximate arithmetic or heuristic SDE failures
cannot silently spend that slack without a bound.

For fixed c every arity and table dimension is polynomial in dim L and
log p. A depth-first traversal retains at most the sum of (arity-1)
sibling roots along one path, plus one matrix-leaf workspace. Bound each
root by v field registers and the latter's retained source registers by
O(T*(m+w+z)+L). Add coherent arithmetic/synthesis and oracle workspace;
this logical-register count is not their gate-level space bound.
Classical coefficient tables have at most
`P*binom(v+e,e)` entries per weighted packet, and bounded-degree pullback
does not require an expanding expression tree. Solver bit work and
reversible arithmetic remain charged. This is a polynomial existence
bound at FIXED c, not a practical gate estimate or a growing-class claim.

To avoid an unsupported precision-complexity claim, build the whole HSP
procedure at constant error first. Amplify by independent repetitions and
majority of canonical Lie-subalgebra outputs in ORIGINAL coordinates,
as in the class-four draft. This gives logarithmic repetition overhead
without an oracle for verifying that a proposed subgroup is complete.

### 10.5 Arbitrary-H Composition And What This Does Not Establish

The initial nil-2 call obtains K=H intersect G'. On its correct-output
event, the public normalizer quotient contains H/K transverse to its
derived group. Apply the image call above. Restrict to the public preimage
T=HN. Because H is abelian in this transverse problem, T' lies in gamma_3
of the current group and its class drops by at least one. Transversality
and class-two derived algebra persist under these subgroup/quotient
operations. Repeat at most c-2 image calls, then use the final nil-2 solver.
If a derived algebra becomes abelian, use the scalar/metabelian image
routine; do not pass w=0 to the positive-width matrix construction.
There is no product of the image-query costs ACROSS descent levels: each
level queries the original f through public representative maps. The
products within each erasure tree are real and must remain in M.

Allocate a constant total failure budget over those at most c calls.
Every operation has a public size-dependent cap even on an incorrect
earlier K or image. Validate public chart/class/rank conditions, but do
not claim that membership checks prove hidden-subgroup completeness.
A first-error union bound covers the bad earlier-answer event; it is not
a conditional correctness promise offered to a later caller for free.

This audit supplies a concrete written composition, rather than leaving
freshness, selection and adaptive state form as mutually incompatible
assumptions. It found no new failure under the stated ordinary-oracle and
explicit-chart promises. It does NOT independently validate the BCH degree
argument, cited solver/nil-2 algorithms, all Clifford/QFT cost results or
novelty, nor machine-check the whole controller. A real implementation
that shares preparation randomness, inspects states for witness selection,
forgets a shared record or reuses consumed packets falls outside the proof.
No useful external speedup or Shor-level result is established.

Validation for this written pass: 65 exact-rational arithmetic cases
checked rank, label/multiplier retry caps, merge counts in the correct
direction, Fourier spanning, binary-sampling truncation and total error.
They covered c=4..7, positive small dimension bounds and one 127-bit-prime
case with error 2^-64. These are arithmetic spot checks, not a proof of
the controller or quantum executions. The 71 connected nonlinear-jet,
variable-radical source and affine-channel tests passed. No new source
manager, SDE backend, Lean controller or resource-planner API was added.
