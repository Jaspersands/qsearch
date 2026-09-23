# Recursive Edge Preparation: Clean Composition, Noise Failure

Status: LOCAL DERIVATION / REVIEW PENDING. No independent review, formal
verification, novelty or improvement over known DCP algorithms is claimed.
This is a mathematical specification, not a completed implementation pass.

The main-model role is theory and adversarial verification. Gemini owns the
implementation/integration and routine workflows specified at the end.
`core/dcp_recursive_edge_sieve.py` is the earlier fixed-time draft, not an
implementation of the stronger coherent-schedule construction below.

Scope correction (2026-09-24): `research/DCP_MEASURED_FIBER_COLLIMATION.md`
describes the established alternative of measuring a COMMON low-sum syndrome
before invoking an ordinary two-witness finder in separate workspace. It does
not need the source-controlled coherent preparers or reciprocal mass used
here. Keep those obligations scoped to THIS construction. The alternative's
one-shot noisy parity bound is not a repair of the recursive noise failure
below, and neither route supplies fast near-density-one arithmetic.

## Research Decision

The direct parity readout can be made into an exactly composable IDEAL phase
state primitive without a unique partner, degree oracle or exponential list.
This gives another route to the KNOWN polynomial-space subexponential class.
It does not solve the polynomial-time bottleneck. More importantly, its clean
recursion does NOT preserve the inverse-n-noise promise of the one-shot result.
Do not spend research time tuning this into a purported new noisy decoder.

The reusable ingredient is coherent schedule symmetrization with feedforward:
different purified support preparers can be combined without amplitude-balance
or sign assumptions, and accessible solver workspace can be ordered rather
than erased. The remaining computational target is a faster arithmetic
support preparer with enough reciprocal probability mass, not a deterministic
partner oracle. Constant witness success alone does not suffice: Section 3
gives a natural-source counterexample. These are sufficient routes, not
restrictions on all decoders.

## 1. Setup And Legal Access

Let N=2^n and take m=2r ideal independent phase states, 2<=r<n, with independent
uniform public labels a_i in Z_N. Their product is

    |psi_d> = 2^(-m/2) sum_b exp(2*pi*i*d*f_a(b)/N)|b>,
    f_a(b) = sum_i a_i b_i mod N.

Use the fixed capped balanced support family already defined in
`DCP_COHERENT_EDGE_READOUT.md`: L=ceil(sqrt(2^r)) supports of equal weight k
from each r-coordinate block, with k minimal such that C(r,k)>=L. Thus
D=L^2, each full support S_j has weight w=2k, and the padded index space has
size P=next_power_of_two(D). This is procedurally unranked, not stored.

For this primitive the edge condition is DIFFERENT from the parity readout:

    E(b,j) iff j<D and f_a(b xor S_j)-f_a(b) = 0 mod 2^r.

It is symmetric under b <-> c=b xor S_j. The output label will be the full
signed difference, with r zero bits, not necessarily the final half-period.
Let q_b count valid indices. No operation is allowed to use q_b for free.

First take a clean support preparer U_b mapping |0> to sum_j alpha_(b,j)|j>,
controlled by unchanged b and public low labels. V_b similarly supplies beta.
Section 2 extends this to purified preparers WITH accessible solver workspace;
clean witness preparation is not a universal requirement. The coherent
evaluations and workspace must be implemented and charged. A measured host
sampler or assumed witness table cannot simply be called coherently for free.

## 2. Symmetrization With Both Outcomes Kept

Prepare one control qubit z in |+>. On z=0 run U at b; on z=1 run V at b.
Herald E(b,j), retaining j and the COHERENT z register. Compute c=b xor S_j
reversibly. Prepare a second index k using V_c on z=0 and U_c on z=1.
XOR j into k and herald k=0. This projection is charged; it is not a free
reflection or amplitude-normalized resampling. Uncompute c and arithmetic
scratch. Both failures consume the input batch.

For an accepted edge define

    A_b = alpha_(b,j) beta_(c,j),
    B_b = beta_(b,j) alpha_(c,j).

Its coefficient before measuring z is (A_b|0>+B_b|1>)/sqrt(2).
Choose the least set bit of S_j as pivot, write e=b_pivot, and map b to
the common representative x=b xor e*S_j. Measure z in the X basis, writing
s=0 for '+' and s=1 for '-'. The endpoint coefficient is

    h_s(b,j) = (A_b + (-1)^s B_b)/2.

Exchanging endpoints swaps A and B, hence

    h_s(c,j) = (-1)^s h_s(b,j).

Apply Z^s to the orientation qubit e. For each common outcome (x,j,s), its
two amplitudes now agree EXACTLY, including arbitrary complex phases.
Consequently the remaining qubit is the ideal phase state with label

    delta = f_a(x xor S_j)-f_a(x) mod N.

The common x,j,s records can be measured/discarded. They are not endpoint
tags. The s=1 branch must NOT be discarded or left uncorrected. Both outcomes
are usable and their combined weight for each oriented b,j is

    sum_s |h_s(b,j)|^2 = (|A_b|^2+|B_b|^2)/2.

If U=V, the '-' branch has zero amplitude and this reduces to the simpler
same-preparer double-endpoint construction in the draft. Taking two different
classical schedules WITHOUT the coherent swap does not give equal amplitudes.
The X measurement and Z correction are essential, not a probabilistic relabel.

### Accessible Workspace Need Not Be Erased

More generally write U_b|0> = sum_(j,g) alpha_(b,j,g)|j,g>, and similarly
V_b with amplitudes beta. Retain BOTH solver workspaces. After mapping to
representative x and orientation e, swap the first and second workspace
registers iff e=1, BEFORE measuring the control. Pad unequal register sizes
to a common size. The canonical record is now (g_x,g_(x xor S_j)).

For each fixed canonical record the two coefficients are

    A_x = alpha_(x,j,g_x) beta_(c,j,g_c),
    B_x = beta_(x,j,g_x) alpha_(c,j,g_c).

Endpoint exchange still swaps A and B. The identical X-measurement and Z
feedforward proof applies term by term. Even mutually orthogonal endpoint
histories are allowed: both histories are now recorded in the same ORDER
at both orientations. Do not trace or measure the unordered histories first.
Summing canonical workspace outcomes gives the accepted mass

    2^-m sum_(b,j valid) p_U(b,j)*p_V(b xor S_j,j),
    p_U(b,j) = sum_g |alpha_(b,j,g)|^2,

where edge reversal equates the two terms arising from the control outcomes.
This is a concrete instance of the repo's earlier symmetric relation lift,
not a claim to have invented workspace symmetrization.

Purifying a specified classical randomized procedure by keeping its coins
and reversible history is permitted, with all computation/storage charged.
This does not grant a cheap implementation of an unspecified sampler or
undo an actual measurement performed outside the controlled computation.
Input/environment dephasing is different: its inaccessible environment is
NOT one of the two solver workspaces that the algorithm can reorder.

## 3. Constant Natural-Source Success Without Degree Classification

Instantiate U,V with ordinary uniform-index Grover preparation using independent
PUBLIC geometric times t,u, but coherently swap their roles as above. The
marked-index amplitude of a t-step preparation is

    g_t(q) = sin((2t+1)*theta_q)/sqrt(q),
    theta_q = asin(sqrt(q/P)).

Let h=ceil(log2(P)/2), p=2^-h and rho=1-p; Pr(t)=p*rho^t. From the previous
exact geometric kernel, the mean search success at any positive degree is

    H(q) = E_t[q*g_t(q)^2] = [1-F(2*theta_q)]/2,
    F(x) = p^2*cos(x)/(p^2+4*rho*sin(x)^2).

For q<=P/2, p^2<=1/P and rho>=1/2 imply

    F(2*theta_q) <= 1/(1+4q), so H(q)>=2/5.

For q>P/2, the numerator of F is nonpositive, so H(q)>=1/2. Thus
E_t[g_t(q)^2]>=2/(5q) for EVERY q>0. This is a squared-amplitude statement,
not the off-diagonal positive-kernel statement used by the one-pass readout.

After summing both corrected control outcomes, independence of t and u gives
mean accepted edge weight at least 4/(25*q_b*q_c). The oriented-edge sum
already counts both orientations with source factor 2^-m; do not divide it
by two again or normalize by first-stage heralding.

For uniform labels and fixed distinct nonempty supports, signed sums for two
different supports are pairwise independent modulo 2^r: their coefficient
matrix has a 2x2 minor of determinant +/-1. Hence, with lambda=D/2^r,

    E q_b = lambda,   M2 = E q_b^2 = lambda^2+lambda*(1-2^-r).

Define a measure on ALL labels and oriented valid edges with total mass lambda.
Normalize this measure to a probability distribution nu. Edge reversal gives

    E_nu q_b = E_nu q_c = M2/lambda.

The function 1/(xy) is jointly convex for x,y>0: its Hessian is positive
definite, with determinant 3/(x^4*y^4). Jensen therefore gives

    E_a[2^-m sum_(b,j valid) 1/(q_b*q_c)] >= lambda^3/M2^2.

The infinite-schedule merge success is consequently at least

    (4/25)*lambda/(lambda+1-2^-r)^2 >= 8/225,

because 1<=lambda<2. This is a SOURCE AVERAGE, not a guarantee on each fixed
label list. There is no degree threshold, degree oracle or postselection of
favorable natural labels in this proof.

Abort an entire attempt if either geometric draw reaches T=B*2^h. Do not
renormalize the schedule. Each tail has probability <=2^-B, so finite success
is at least 8/225-2^(1-B). Taking B=10 gives 3871/115200 > 1/32.

The two control arms require a common clock up to max(t,u), not the smaller
or an uncharged average branch time. A conservative mean Boolean-predicate
budget is 4*E[max(t,u)]+2 <= 8*(2^h-1)+2. Coin generation also takes charged
expected O(2^h) work. Worst-case calls are at most 4*(T-1)+2. Arithmetic,
unranking, controlled scheduling, heralding and feedforward cost polynomial
overhead. This is O(2^(r/2)*poly(n,r)) time and polynomial workspace.

### Witness Success Does Not Certify Reciprocity

The preceding Jensen bound uses the specific Grover sampler's probability
lower bound on EVERY valid support. It does not follow from a sampler's
average probability of finding some valid witness.

Here is a counterexample on the same natural DCP graph, not a new oracle
problem. At b, return the first valid S_j with c=b xor S_j<b in numerical
order; fail if none exists. Every answer is valid, but the same sampler
at c can never return to larger b. Its reciprocal mass is exactly zero.

Complementing every bit of b negates each signed sum, preserves the
zero-mod-2^r edge predicate, and reverses numerical order. Consequently the
probabilities of having a lower or an upper neighbor agree. Their union is
the nonisolated event. By the degree moment bound,

    Pr(valid downward answer) >= (1/2)*Pr(q>0)
        >= lambda^2/(2*M2) >= 1/4.

Thus even CONSTANT success over the full natural source does not imply any
success of the same-sampler reciprocal construction. The enumerating routine
is an exponential countercontrol, not a proposed efficient solver. This is
not a lower bound against other readouts: the repo's permutation readout,
for example, need not impose reciprocal two-cycles.

An arithmetic replacement must establish reciprocal probability mass (or
use a different proved readout), not just report witness recovery rates.
Changing to a second complementary sampler is allowed, but its cross-mass
must be proved. It cannot be inferred from both marginal success rates.

## 4. Why The Natural Input Law Restarts

Write a_i=l_i+2^r h_i. The edge predicate, preparers, common representative,
accepted weights and control outcome probabilities depend only on l, b and
public schedules, not on h or d. No orientation measurement is performed.

For any fixed successful common outcome x,j,s and low vector l,

    delta/2^r = carry(l,x,S_j) + sum_(i in S_j) (+/-h_i) mod 2^(n-r).

Every support is nonempty and one coefficient is +/-1. Conditional on all
other high coordinates, this quotient is uniform. The output phase state
depends on discarded records only by a global phase. Thus after discarding
the obsolete labels/records, each fresh successful batch gives an ideal
phase state with a uniform quotient label. Separate batches remain independent
for a fixed secret d. Do not reuse destroyed inputs or condition on known
favorable high labels. Selecting oracles using high bits invalidates this
particular recursion proof, even if the pairing operation itself remains legal.

## 5. Charged Recursion And Prior Art

Use deterministic level sizes r_i>=2 summing to n-1, absorbing a remainder of
one into another block. Let p0=1/32, m_i=2r_i, and let C_i bound expected
primitive work in one attempt. With fresh batches after each failure,

    S_i <= m_i*S_(i-1)/p0,
    W_i <= [m_i*W_(i-1)+C_i]/p0.

This renewal calculation does not assume the cost of an attempt is independent
of its success. Fresh attempts must have the same law. The final uniform Z_2
label is one with probability 1/2; rejecting zero costs another factor two.
For r=Theta(sqrt(n log n)), expected fresh-state and time costs are
2^O(sqrt(n log n)), with polynomial depth-first workspace. The recursion is
NOT a polynomial-sample algorithm merely because each individual merge uses
2r inputs. Public labels along the recursion stack cost O(n^2) bits, plus
polynomial coherent arithmetic scratch.

Known low-bit phase corrections on fresh input states reduce recovery of the
remaining secret to smaller moduli. The n=1,2 base cases can use direct
constant-size rejection. Account for rotations to adequate precision and all
n parity stages. Ideal successful terminal outcomes are correct; a global
runtime cap produces a charged timeout, not an undetected wrong answer.

[Regev, Section 3](https://arxiv.org/html/quant-ph/0406151v1#S3) already gives
a polynomial-space recursive sieve in this asymptotic class. The explicit
merge considered here is not presented as a new complexity improvement.
[Kuperberg's later collimation](https://arxiv.org/abs/1112.3333) and
[DCP time/query tradeoffs](https://arxiv.org/abs/2206.14408) are necessary
comparators before claiming any better resource tradeoff. Novelty of this
local symmetrization formulation has NOT been established.

## 6. Exact Noise Accumulation: A Falsifier

Consider independent, label-independent dephasing of the original input
states, with visibility eta in [0,1]. In the product computational basis,
the b,c matrix element is attenuated by eta^Hamming(b,c). Each retained pair
here differs on EXACTLY w_i=2k_i coordinates at level i. The operation and
success probability do not use off-diagonal input elements: summing both
corrected control outcomes does not postselect on the physical dephasing.

Conditioned on any successful common label, the output visibility is exactly
eta^w_i. Symmetrization repairs preparation-amplitude imbalance; it does not
purify the input qubits. Fresh disjoint batches and fixed level weights give

    eta_final = eta_initial^W,   W = product_i w_i.

For the allowed example eta_initial=1-1/n,

    eta_final <= exp(-W/n),   W>=2^(number of levels).

For the clean-optimal block scaling, the number of levels is
Theta(sqrt(n/log n)), so even this weak W lower bound makes visibility smaller
than every inverse polynomial asymptotically. The actual w_i grow with r_i,
so the loss is worse. This refutes carrying the one-shot inverse-n-noise
claim into this recursive architecture without a new mechanism.

More generally, require eta_final>=n^-c for fixed c>0. Necessarily
W<=c*n*ln(n), hence L<=log2(c*n*ln(n)). As sum r_i=n-1, some block obeys

    max r_i >= (n-1)/log2(c*n*ln(n)) = Omega(n/log n).

This is a structural constraint on this fixed-weight, fresh-batch recursive
family with inverse-polynomial output visibility. Its specified Grover
subroutine on such a block has exponential-in-block-size search work. It is
NOT a lower bound on every arithmetic implementation, adaptive sieve, noisy
DCP algorithm, or measurement retaining multiple output qubits. Allowing much
smaller visibility and paying enormous repetition is a separate resource
optimization, not covered by this polynomial-visibility statement.

## 7. Adversarial Checks Performed

Only focused mathematical probes were run by the main model, not integration
tests or live registry workflows. On the actual zero-mod-4 graph with labels
(0,1,1,1) modulo 8 and secret 1:

- Same schedules t=u=0 or t=u=2 give success 1/16 and pure-state residual
  below 9e-19 in the existing explicit two-index evolution.
- Unsymmetrized t=0,u=1 has success 5/32, endpoint amplitude mismatch 1/4,
  and unnormalized pure-state residual 3/512. It cannot be silently treated
  as a reusable ideal phase state.
- Coherently combine the executed (0,1) and (1,0) branches, perform the
  control Hadamard, and apply the outcome-dependent orientation sign. The
  endpoint residual is zero and both outcomes retain total success 5/32.
  Omitting feedforward leaves coherence numerator 1/8 instead of 5/32.
- Exact rational geometric diagonal kernels for P=2,4,...,128 and ALL
  degrees 1..P have minimum search success 13/28, consistent with the
  analytic all-P lower bound 2/5. This finite check is not that proof.
- The finite-tail arithmetic is exact: 8/225-1/512=3871/115200>1/32.
- A separately assembled two-level mixed-state calculation used four child
  branches from modulo-32 labels (0,1,4k,1), k=(0,1,3,1), then a modulo-8
  parent with labels (0,1,3,1). Executed support indices gave visibility
  eta^4 for eta=0.5,0.9,0.99, with maximum matrix residual below 1.7e-16.
  Every selected child/parent branch had probability 1/128, explicitly
  retained in the calculation. These are selected physical channel controls,
  not natural-source probability estimates or uncharged state preparation.
- An explicit two-orientation state with orthogonal unordered solver tags
  had zero reduced visibility; controlled canonical ordering restored
  visibility one to numerical precision. This checks accessible workspaces,
  not inaccessible dephasing environments.
- Exhausting all 256 low-label lists and 16 assignments gives downward
  witness success 99/256, nonisolated mass 43/64 and reciprocal mass ZERO.
  High lifts do not change this predicate or ordering; no favorable low
  lists were selected. This is the counterexample to marginal-success gating.

These checks reuse the existing finite oracle/reflection evaluator. An
independent full control/index/orientation simulation is still required;
neither these checks nor a green test suite establish novelty or a proof.

## 8. Gemini Implementation Contract

Implement the symmetrized path separately from the draft's fixed-time path;
do not merely change its success constant or relabel existing artifacts.

1. Execute a coherent control plus BOTH support registers, opposite schedule
   assignments, first-edge and equal-index heralding, orientation mapping,
   canonical workspace ordering, control Hadamard, and Z feedforward. Keep
   both outcomes and charge failures. The Grover special case has no history.
2. Cross-check arbitrary complex purified-preparer amplitudes and arbitrary
   accessible workspace against an independently constructed linear map.
   Omit canonical ordering or feedforward in negative controls. Endpoint
   tags by themselves are NOT an obstruction once ordering is implemented.
3. Exhaust every low transcript and its high lifts on the 8^4 small source.
   Check zero-target degree moments and uniform quotient labels, retaining
   unsuccessful natural-source mass. Add a high-label-dependent selection
   countercontrol showing why that uniformity assumption matters.
4. Check the exact geometric H(q) formula, pointwise 2/5 bound, edge-weighted
   Jensen lower bound, finite cutoff without resampling, and shared-clock cost.
   Preserve the downward-sampler natural-source counterexample: marginal
   witness success must not pass a reciprocal-mass evidence gate.
5. Add resource recurrences with p0=1/32 ONLY for the new symmetrized clipped
   geometric path; keep the fixed-time draft's distinct 2^-17 certificate.
   Include full-secret/base-case/repetition factors and polynomial overhead.
6. Check one- and two-level explicit mixed states against eta^(product w_i).
   Reusing the same formula for expected and observed data is not a test.
   No automatic promotion to a noise-robust or novel-speedup claim is allowed.
7. Wire into the existing matching experiment/report, not a duplicate
   candidate. Expose clean composability and noise failure separately. Record
   the latter as a scoped negative, not classical dequantization or a generic
   impossibility theorem. Preserve strict literal evidence gates.
8. Run focused tests, then normal syntax/registry/full-suite validation as
   appropriate. Preserve concurrent changes and avoid duplicate active test
   processes. Refresh artifacts and use infrequent bundled checkpoints.

Return mathematical discrepancies to the main model rather than weakening
assertions to get a passing suite. The next main-model research target is a
structured preparer or a different information-preserving measurement, not
mechanical completion of this baseline.
