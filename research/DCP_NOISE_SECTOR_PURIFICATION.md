# Phase-State Purification: Exact Sector Benchmark And A Positive Filter

Date: 2026-09-23

Status: LOCAL DERIVATION / REVIEW PENDING. No novelty, independent proof,
asymptotic speedup, efficient large-instance implementation, or general DCP
lower bound is claimed. Only focused mathematical controls were executed.
Gemini owns production implementation, registry wiring and routine runs.

## 1. Decision And What Changed

The fixed-weight recursive sieve loses visibility as a product of support
weights. Simply saying "purify before the next level" is not a solution.
This note derives an exact physical benchmark for doing so, without limiting
the quantum operation to the existing sieve or to basis permutations.

For a collision-free FULL-modulus subset-sum spectrum, the best output
visibility is the largest input coherence connecting the requested frequency
difference. Independent noise then gives a minimum-Hamming-distance bound.
No postselection, however rare, improves that conditional benchmark.

This obstruction genuinely fails when full-frequency sectors have internal
degeneracy. An explicit five-input filter below preserves an unknown phase
of order eight, cancels every single-qubit dephasing error, and changes
conditional error from p to (3/2)*p^2+O(p^3), with clean acceptance 2/15.
It is a finite feasibility control, not an algorithmic improvement.

New research target: exploit degeneracy by matching the low-degree error
responses of two frequency sectors, while retaining coherent sector labels.
The unresolved costs are locating the sectors, constructing the responses,
and implementing the resulting filter on natural scalable inputs. Dense
linear algebra on enumerated fibers does NOT meet those obligations.

This complements `DCP_MULTI_OUTPUT_FREQUENCY_BOUND.md`: substantial retained
Holevo quantity does not imply that the retained block can be purified into
a useful phase qubit by a cheap operation, or even with arbitrary success.

FOLLOW-UP: section 11 now supplies a natural-label, useful-success existence
bound. In the inverse-n noise regime, a simpler uniform-fiber filter dominates
the proposed low-degree moment solver as a research target. Its efficient
implementation is still missing and runs into the clean PGM normalization
problem. Do not build more error-response matrix infrastructure on the
assumption that natural physical feasibility remains the main obstacle.

## 2. Physical Model

Let N=2^n, M=2^m, omega=exp(2*pi*i/N), and

    f(b) = sum_i a_i*b_i mod N,     b in {0,1}^m.
    D_d |b> = omega^(d*f(b)) |b>.

The source family is rho_d=D_d Q D_d^dagger for a known positive-semidefinite
density matrix Q. The secret d is uniform over Z_N. The main noise case is
independent input dephasing of visibility nu in [0,1):

    Q_(b,c) = nu^Hamming(b,c) / M.

For unequal independent visibilities replace nu^Hamming by the product of
nu_i on the differing coordinates. Inaccessible noise environments are not
available as coherent solver scratch.

The target is one phase qubit

    |phi_(d,delta)> = (|0> + omega^(d*delta)|1>)/sqrt(2),

with delta != 0 modulo N. Arbitrary secret-independent quantum instruments,
known ancillas, coherent workspace, feedforward and postselection are allowed.
All additional secret-bearing inputs/oracle uses must be counted. Known d,
extra uncounted information about d, and a different prior are different models.

As in the previous note, s is average accepted probability and h is average
UNNORMALIZED target fidelity. Conditional fidelity is h/s, weighted by Born
success over d, not a uniform average of separately normalized successes.

## 3. Exact Arbitrary-Instrument Benchmark

Define full-frequency sectors F_t={b:f(b)=t}. Let

    A_t = Q[F_t,F_t],
    C_t = Q[F_t,F_(t+delta)].

For nonempty sectors set

    mu_(t,delta) = ||A_t^(-1/2) C_t A_(t+delta)^(-1/2)||_op,
    mu_delta = max_t mu_(t,delta).                         (1)

For singular A use the Moore-Penrose inverse on its support. Positivity of Q
ensures that C has no components outside the corresponding supports. Empty
sector pairs contribute zero. For independent nu<1, Q and all nonempty A_t
are strictly positive definite. Do not numerically truncate small positive
eigenvalues and then pretend the resulting optimum is certified.

The exact optimal conditional fidelity, allowing arbitrarily small positive
success and unlimited implementation cost, is

    F_opt(delta) = (1+mu_delta)/2.                         (2)

Proof of upper bound. For one Kraus operator K write its output-0 row on F_t
as x_t and its output-1 row as y_t. Fourier averaging over d gives

    s_K = sum_t [x_t A_t x_t^dagger + y_t A_t y_t^dagger],
    h_K = s_K/2 + Re sum_t x_t C_t y_(t+delta)^dagger.

Whitening, Cauchy-Schwarz and 2ab<=a^2+b^2 bound the absolute cross term by
mu_delta*s_K/2. Every x_t and y_t enters at most once in this last bound.
This allows dense, complex, noncovariant K and secret-dependent success.
Summing over Kraus indices also allows traced workspace and arbitrary
measurement histories.

Proof of achievability. Choose a maximizing pair and unit singular vectors
u,v with u^dagger A_t^(-1/2) C_t A_(t+delta)^(-1/2) v=mu_delta. Define K by

    K[0,F_t]         = c*u^dagger*A_t^(-1/2),
    K[1,F_(t+delta)] = c*v^dagger*A_(t+delta)^(-1/2),

with all other entries zero. The input supports of the two rows are
disjoint. Choose positive c so ||K||_op<=1. Both output populations are c^2;
the coherence is c^2*mu_delta with the required unknown phase. Hence success
is 2c^2, independent of d, and (2) is attained. Failure completes the map.

This is a physical EXISTENCE construction. It is not a gate synthesis,
polynomial algorithm, or claim that the selected sector can be found cheaply.
The largest-fidelity filter may have negligible acceptance. For a useful
algorithm, the success/fidelity frontier and implementation cost are needed.

The general optimal-probabilistic-map framework is established prior art:
Fiurasek's generalized Choi eigenvalue formula provides an independent
benchmark. Equation (2) is the finite cyclic, phase-qubit sector reduction
used here, not a claim to a new optimization principle.

## 4. Collision-Free Noise Obstruction

When f is injective, every nonempty A_t is the scalar 1/M. For independent
dephasing, (1) reduces to

    mu_delta = max_(b,c: f(c)-f(b)=delta) nu^Hamming(b,c)
             = nu^w_min(delta),                          (3)

with zero if no pair exists. This needs only injectivity, NOT uniqueness of
all signed difference representations. Even if many pairs realize delta,
their different frequency sectors do not add free purification power.

Thus no arbitrary postselected quantum operation on this batch produces
average target fidelity greater than (1+nu^w_min)/2. Unequal independent
visibilities give the maximum corresponding product of nu_i instead.

For independent uniform labels, a signed-difference union bound gives

    Pr[f not injective] <= (3^m-1)/2^n.                   (4)

If every eligible nonzero delta is divisible by 2^r, define a bad low-label
event: there is a nonempty signed support of weight less than k summing to
zero modulo 2^r. Each fixed signed support vanishes with probability 2^-r.
Together with (4), its total exceptional probability is bounded by

    epsilon_k = min(1, (3^m-1)/2^n
                      + 2^(-r)*sum_(w=1)^(k-1) C(m,w)*2^w).       (5)

On every ordinary label tuple, EVERY eligible output label obeys mu_delta
<=nu^k. The candidate may choose delta after seeing its labels and its
measurement outcome. Averaging over natural labels and using h_a<=s_a<=1
on exceptional tuples gives

    h <= (1+nu^k)*s/2 + (1-nu^k)*epsilon_k/2.             (6)

If requested accepted fidelity is at least (1+v_req)/2 with v_req>nu^k,

    s <= (1-nu^k)*epsilon_k/(v_req-nu^k).                 (7)

For m=2r,n>=6r,k=ceil(m/16), epsilon_k decays exponentially in r. Indeed,
H_2(1/16)+1/16 < 1/2 bounds the weighted binomial tail in (5).
The exact integer/rational bound, not its entropy relaxation, should be used
in finite artifacts. Analytic examples (not large circuit executions):

| r | k | epsilon_k, n=6r,m=2r |
|---|---|---|
| 16 | 2 | 9.765625000234e-4 |
| 32 | 4 | 7.951259613037e-5 |
| 64 | 8 | 6.751897478063e-7 |
| 128 | 16 | 6.649079438796e-11 |

For fixed nu<1 and r=omega(log n), useful phase visibility cannot be
recovered with inverse-polynomial fresh-batch acceptance in this regime.
For nu=1-1/n, (3) instead gives a quantitative, smaller per-merge noise
penalty. Do not extrapolate (7) to an arbitrary recursive pipeline without
checking the conditional source law at every level.

Adaptive regrouping from a larger pool, dense full spectra, correlated noise,
additional state copies, and non-phase-qubit outputs are not covered by this
natural sparse-spectrum conclusion. A low-bit collision alone is NOT the
full-modulus degeneracy needed to escape (3).

## 5. Positive Degeneracy Controls

Two equal input labels illustrate why injectivity matters. For a=(1,1),
N=16, target delta=1, the sectors of weights zero and one give

    mu_delta = nu*sqrt(2/(1+nu^2)) > nu,   0<nu<1.

A physical filter with success 1/2 attains this value. For target delta=2,
the best visibility is instead nu^2. Purification and frequency addition
are different transformations, even on the same inputs. Repeated random
full labels are not a free natural-source resource.

A distinct-label dense control a=(1,3,5,7,11), N=16, delta=8 has minimum
pair distance two but stronger collective purification:

| nu | Best pair visibility | Sector visibility | Filter acceptance |
|---|---|---|---|
| .5 | .25 | .5247431755 | .0749345098 |
| .9 | .81 | .9832962682 | .1360460580 |

These finite numerical optima were independently checked against the FULL
Choi generalized-eigenvalue problem, not only the sector formula. They are
not rational optimality certificates, natural scaling results, or proof of
efficiently accessible purification. The optimal sector differed with nu.

## 6. Low-Degree Error-Response Matching

There is a concrete way to design positive filters rather than merely
optimize a matrix numerically. Let p=(1-nu)/2 be independent Z-error
probability. Choose weights w_t on F_t and w_u on F_u, with u=t+delta,
and define their error responses

    L(e)=sum_(b in F_t) w_t(b)*(-1)^(e dot b),
    R(e)=sum_(b in F_u) w_u(b)*(-1)^(e dot b).

Require L(0)=R(0)=1 and L(e)=R(e) for every error mask of weight at most k.
Weights may be signed or complex; nonnegative weights can sometimes suffice.
Set the two rows of K to c*w_t and c*w_u, supported on the respective
sectors, and choose c so ||K||<=1. For error mask e the unnormalized output is

    c/sqrt(M) * omega^(d*t)
        * [L(e)|0> + omega^(d*delta)*R(e)|1>].

Therefore, with P_p(e)=p^|e|*(1-p)^(m-|e|),

    success = c^2/M * sum_e P_p(e)*(|L(e)|^2+|R(e)|^2),
    infidelity = sum_e P_p(e)*|L(e)-R(e)|^2
                 / [2*sum_e P_p(e)*(|L(e)|^2+|R(e)|^2)].            (8)

All errors of weight <=k contribute ZERO infidelity numerator, even when
their accepted amplitudes are nonzero. For FIXED m and fixed weights this
gives O(p^(k+1)) infidelity and positive clean acceptance. It is not a
uniform growing-m theorem. The error tail, norms, success and coefficients
must be bounded again in any asymptotic proposal.

Finite construction: solve the linear moment constraints on the two
enumerated fibers, with a nonzero zeroth moment. Existence is a rank or
affine-hull question; merely counting unknowns is not a proof. Finding the
fibers and implementing the rows remains the hard algorithmic part.

## 7. Exact Full-Order Positive Filter

Take N=8, a=(1,2,3,5,7), t=3, u=4 and delta=1. This target has order eight,
so the example is not just purification of a binary secret/parity state.
Integers below index the five-qubit computational basis in little-endian
label order. Use only these nonzero weights:

    w_t:  b=3:1/8, 4:3/8, 15:1/8, 21:3/8;
    w_u:  b=5:5/8, 22:1/4, 24:1/8.

Every listed input belongs to the indicated FULL-frequency sector. Both
weights sum to one and their first moments match on all five coordinates,
so L(e)=R(e) for every singleton error and for e=0. These identities were
checked with exact rational arithmetic.

The squared row norms before scaling are 5/16 and 15/32. Take c^2=32/15;
the resulting K has operator norm one. c^2 is a normalization coefficient,
NOT a probability. Actual acceptance is

    s(p) = p^4/6 - 11*p^3/15 + 14*p^2/15 - 7*p/15 + 2/15.

Conditional infidelity is exactly

    E(p) = (3*p^4 - 13*p^3 + 12*p^2)
           / (10*p^4 - 44*p^3 + 56*p^2 - 28*p + 8)
         = (3/2)*p^2 + O(p^3).                            (9)

| p | Acceptance | Conditional infidelity |
|---|---|---|
| .1 | .0952833333 | .0187685849 |
| .01 | .1287592683 | .0001536498 |
| .001 | .1328675993 | .0000015036 |

Independent physical density-matrix evaluation checked (9) for EVERY secret
d=0,...,7 at all three p values. Both success and fidelity match the symbolic
formula within 3e-16. The map consumes all five input qubits. No failed input
reuse or unknown-state reflection is assumed.

IMPORTANT IMPLEMENTATION RULE: the two sectors must be selected/coherently
processed together. Measuring f(b) and recording whether it was t or u
destroys their relative phase and reduces target fidelity to 1/2. A circuit
that first measures the sector and then "forgets" it does not implement K.
The formula for K proves a valid contraction, not an efficient gate exporter.

## 8. Adversarial Review And Checks

Executed only short in-memory mathematical probes, not a pipeline or bulk
test suite. This pass created no production code or accepted theorem record.

1. Compared sector optima with the full Choi problem for eight cases: sparse
   labels (1,5,25)/256 at delta=4; repeated labels (1,1)/16 at delta=1 and 2;
   and dense distinct labels (1,3,5,7,11)/16 at delta=8, all at nu=.5 and .9.
   Agreement was within 1e-10. Constructed the physical maximizing filters,
   verified K^dagger*K<=I, and averaged actual density matrices over every d.
2. Sparse control has w_min=2. At nu=.5 its best fidelity is .625, and at .9
   it is .905, both with a selected filter's acceptance 1/4. This confirms
   the no-purification case without restricting K to a basis-only search.
3. The dense controls above violate a deliberately overbroad extension of
   the sparse bound. They are positive counterexamples, not anomalies to
   remove. The full-modulus injectivity premise is essential.
4. First found a half-period filter at N=8 on the same five labels with
   weights 1/2 at b=(12,17) versus b=(5,24), clean acceptance 1/8 and error
   4*p^2+O(p^3). Then tested a full-order target to remove the binary-secret
   loophole. The initially chosen sectors 0 and 1 had NO usable first-moment
   solution; searching the eight sector pairs found the explicit 3/4 pair
   in section 7. Do not turn this finite existence search into a claim that
   every pair or natural large instance has a suitable filter.
5. Tested correlated input noise: identity with probability (1+nu)/2, or
   a global Z on all inputs otherwise. At a=(1,5,25),N=256, the two inputs
   b=1 and 2 differ on two coordinates and give perfect delta=4 output at
   success 1/4 even when each qubit's marginal visibility is .5. Independent
   noise would cap fidelity at .625. Marginal noise levels alone do not
   justify (3); the general Q-sector formula must be used instead.
6. Computed (5) using exact integers/Fractions for the analytic table. These
   are not measured failure rates or large executed source ensembles.
7. Physically dephased the section 7 source between FULL-frequency sectors
   before applying K. For every d=0,...,7 at p=0,.01,.1, target fidelity was
   exactly 1/2 to numerical tolerance. Forgetting a which-sector measurement
   record does not restore the purification signal.

Still needed: independent proof review of (1)-(7), sharp useful-success
frontiers, efficient coherent filter construction, and accounting across any
recursive application. Section 11 gives a feasible natural-instance bound in
one noise regime, not an optimal frontier or an efficient implementation.
No quantum advantage follows from the current controls.

## 9. Research Priorities And Kill Criteria

1. First determine whether a compact moment-matching family can be built
   without enumerating exact subset-sum fibers. Demand actual arithmetic or
   circuit structure; a nullspace of an exponentially listed matrix is not
   an algorithm. Kill the proposal if finding its supports already costs the
   claimed improvement or if it hides a witness/inversion oracle.
2. Bound acceptance jointly with fidelity, not just mu_delta. Kill a proposed
   purification advantage when the required row normalization, label selection
   or noise-tail rejection makes useful fresh-batch success negligible.
3. Compare coherent error-response matching with known probabilistic clock
   purification and error-detecting code constructions. Do not claim novelty
   from a rederived Choi optimum or a small postselected filter.
4. Keep the clean DCP arithmetic bottleneck ahead of noise engineering in
   research priority. Noise purification is valuable only if it enables a
   competitive measurement/sieve or a distinct worthwhile noisy-DCP result.
   A better noise curve alone does not move the clean Shor-level objective.

Prior art:

- Fiurasek, optimal probabilistic transformations and purification; section II
  supplies the general Born-weighted Choi benchmark used for cross-checking:
  https://arxiv.org/html/quant-ph/0403165v1#S2
- Fang et al., probabilistic coherence distillation. Its operation classes
  differ from arbitrary unknown-phase instruments here; do not transplant
  its no-go statements without checking the model:
  https://arxiv.org/abs/1804.09500
- Marvian, limits on coherence distillation under time-translation symmetry.
  Continuous symmetry, asymptotic rates and the finite cyclic problem here
  must be distinguished:
  https://arxiv.org/abs/1805.01989

## 10. Gemini Implementation Contract

1. Add a bounded diagnostic for (1), reporting sector multiplicities, minimum
   eigenvalues/conditioning, whitening residuals, maximizing sector, mu,
   K-contraction residual, physical acceptance and Born-weighted fidelity.
   Enumerated dimension and memory must be explicit. Do not silently clamp
   a badly conditioned numerical answer into a theorem.
2. Independently construct the full Choi A=E[rho_d^T tensor I] and
   R=E[rho_d^T tensor |phi_d><phi_d|] on tiny controls and compare its largest
   whitened eigenvalue with (2). Include arbitrary dense Kraus controls.
3. Implement the exact analytic sparse-source bounds (4)-(7) with explicit
   independent-noise, natural fresh-batch, full-spectrum and prior checks.
   Dense or selected-label inputs must not inherit those claims.
4. Encode the section 7 filter using exact rational weights, and verify its
   error-mask moment equations before physical simulation. Include all
   secrets, noise endpoints, the clean success 2/15, the exact polynomial,
   and the deliberately sector-measured failure control.
5. Include repeated-label, dense-distinct-label, half-period, full-order,
   independent-noise and correlated-noise controls. Both positive and
   negative examples are necessary to validate scope.
6. Expose this as a feasibility/purification benchmark in the existing DCP
   research flow, linked to the existing noise blocker. No new breakthrough
   candidate or automatic proof-gate promotion. Preserve the distinction
   between a physical contraction and an efficiently executable circuit.

Next main-model task should attack a compact clean measurement or the
arithmetic needed for coherent filters. Routine integration and additional
matrix-size sweeps belong to Gemini, not the main theorist.

## 11. Natural Uniform-Fiber Filters: Revised Direction

LOCAL DERIVATION / REVIEW PENDING. This follows the positive filter by proving
useful physical feasibility on natural labels rather than assuming that a
small handpicked instance scales. The derivation also eliminates an
unnecessary complication: for constant no-error mass, solving high-order
moment-matching systems is not needed for an existence result.

### Source, Quantifiers And An Exact Identity

Let a be independent uniform in Z_N^m, M=2^m and lambda=M/N. Fix nonzero
delta independently of a. The phase-error mask E has ANY distribution q_e
chosen independently of a; correlations among its bits are allowed. Let
p0=q_0>0. The instrument below does not need to know q, but its probability
guarantee is for each fixed such law, not simultaneously for all
label-adaptive noise laws.

For residue t and mask e set

    A_t(e) = sum_(b:f_a(b)=t) (-1)^(e dot b),
    D_t = A_t(0).

For a uniform auxiliary target t, the exact natural-label identities are

    E_(a,t) D_t = lambda,
    E_(a,t) (D_t-lambda)^2 = lambda*(1-1/N),
    E_(a,t) [A_t(e)-A_(t+delta)(e)]^2 = 2*lambda           (10)

for EVERY fixed e, including zero. Proof of the last identity: equal
Boolean assignments cannot have the two distinct target residues. For
distinct assignments b,c, their signed difference has a unit coefficient,
so the two constraints with uniform t have probability 1/N^2. For e=0,
the square has mean lambda^2+lambda*(1-1/N), and the cross product has
mean lambda^2-lambda/N. For e!=0 these are respectively
lambda*(1-1/N) and -lambda/N. Both differences give 2*lambda.

Uniform t is essential to these moment identities. For example, the zero
assignment contributes deterministically when t is fixed to zero. Do not
replace the averaged target by a preferred target without another proof.

### An Entire Instrument, Not One Rare Sector Pair

Call t good when lambda/2 <= D_t <= 3*lambda/2. For every t such that t
and t+delta are both good, define one accepted Kraus operator by

    K_t[0,b] = 1/sqrt(3*lambda) if f_a(b)=t, else 0,
    K_t[1,b] = 1/sqrt(3*lambda) if f_a(b)=t+delta, else 0.   (11)

Include ALL such t, not just a selected pair. Each full-frequency sector
appears in at most two Kraus rows. The corresponding part of sum K_t^* K_t
has norm at most 2*D_t/(3*lambda)<=1, so (11) is a valid instrument,
completed by failure. This also holds for order-two delta, where both
orientations are counted; the normalization already pays for them.

If at most one eighth of residues are bad, at least 3N/4 oriented pairs are
good. On the clean source each such branch has success at least 1/(6N).
Thus clean success is at least 1/8 and noisy total acceptance s(a)>=p0/8.
This holds for every secret d. Success is allowed to depend on a, not on d.

Let B(a)=s(a)-h(a) be the UNNORMALIZED infidelity numerator. By the exact
error-response formula in section 6,

    B(a) = 1/(6*M*lambda) * sum_(good pairs t) sum_e q_e
                              [A_t(e)-A_(t+delta)(e)]^2.

All terms are nonnegative. Dropping the good-pair restriction and applying
(10) proves

    E_a B(a) <= 1/(3*lambda).                             (12)

The average fraction of bad residues is at most 4/lambda. Markov therefore
bounds the probability of more than one eighth bad residues by 32/lambda.
Another Markov bound, this time on B(a), shows that for any requested
conditional infidelity xi>0, with probability at least

    1 - 32/lambda - 8/(3*lambda*p0*xi)                    (13)

over NATURAL label tuples, instrument (11) has

    accepted probability >= p0/8,
    accepted fidelity >= 1-xi,

simultaneously for all secret values d. Cap a negative probability bound at
zero. The all-secret statement follows from the explicit frequency-sector
action, not from promoting an average-secret calculation.

The good-sector count bound is uniform over delta. The second Markov bound
was proved for a FIXED delta. A polynomial palette can use a charged union
bound, but the result must not be silently applied to a label-adaptive choice
among all N target labels.

### Near-Linear Samples In The Inverse-n Noise Regime

For independent Z error p<=1/(2n), if m<=2n then

    p0=(1-p)^m >= (1-1/(2n))^(2n) >= 1/4,

where Bernoulli's inequality on the n-th power proves the last step. Fix
positive constants c,q, choose xi=n^(-c), and take

    lambda >= 64*n^(c+q),
    m = n + ceil(log2(64*n^(c+q))).                       (14)

For sufficiently large n, m<=2n. Equations (13)-(14) imply, with probability
at least 1-n^(-q) over labels, acceptance >=1/32 and infidelity <=n^(-c).
This is m=n+O(log n) raw phase states. Label failures are charged; the
unconditional useful-source mass is at least (1-n^(-q))/32.

For c=q=2, the explicit sample counts at n=256,1024,4096 are 294,1070,4150.
These are analytic resource parameters, NOT executed large measurements.
No efficient gate implementation has been constructed.

This regime does not include every noisy-DCP promise. In particular,
p=Theta(1/log n) with m=Theta(n) makes p0 exponentially small in n/log n;
the present acceptance bound is then inadequate. Do not call this a solution
for that stronger-noise regime or for arbitrary adversarial quantum noise.

### Why The Natural Existence Result Is Not An Algorithm

The maps in (11) require coherent aggregation over full subset-sum fibers.
Determining the good residues also uses their counts. Neither enumeration
nor a classical nullspace calculation is a polynomial-time implementation.
Measuring the exact frequency first destroys the two-sector phase as before.

A familiar cheap projected block can be built by computing f_a(b), applying
Hadamards to b and heralding all-zero b:

    T[t,b] = [f_a(b)=t]/sqrt(M).

Its nonzero singular values are sqrt(D_t/M). Good sectors therefore have
singular values between 1/sqrt(2N) and sqrt(3/(2N)), even though their ratio
and the corresponding relative Gram conditioning are constant. The desired
normalized uniform-fiber map needs constant singular scale instead.

An odd polynomial bounded on [-1,1] that raises such singular values to a
constant requires degree Omega(sqrt(N)), by the interior Bernstein derivative
bound. This rules out a cheap GENERIC bounded-polynomial amplification of
this block. It is not a lower bound for source-aware arithmetic algorithms,
alternative block access, other measurements, or DCP itself. Implementing an
exact clipping threshold may impose further costs; no matching gate upper
bound is asserted here.

Once a correctly normalized frequency-aggregation map were available, the
remaining two-sector pairing is elementary: introduce a fair qubit c, map
frequency s to anchor s-c*delta, and measure the anchor without measuring c.
Reject anchors whose two frequencies are not good. The obstacle is the
normalization/access to the aggregate map, not that final arithmetic step.

This is the same underlying implementation issue as the clean PGM audit in
`theorems/dcp_pgm_gram_block_encoding.py`. The standard clean-DCP distinction
between information-theoretic measurements and efficient subset-sum access
is prior work, not a new quantum speedup:
https://arxiv.org/abs/quant-ph/0501044

### A More Complicated Route Was Checked And Deprioritized

For the L=sum_(j=0)^k C(m,j) low-weight Walsh characters, let V_t be their
evaluation matrix on F_t and G_t=V_t V_t^*. Exact moments give

    E_(a,t) ||G_t-lambda*I||_F^2 = L^2*lambda*(1-1/N).

This supplies well-conditioned natural sectors when lambda is large enough.
Rows V_t^* G_t^(-1) e_0 exactly reject errors of weights 1 through k. A
jointly normalized all-sector instrument then gives useful acceptance.
However, attaining inverse-polynomial error through that route leads to a
large feature space and roughly log-squared sample overhead. Equation (14)
gives a simpler existence argument for constant p0. Do NOT make a growing
low-degree Gram solver the default implementation target for this regime.

The Gram identity was exhaustively checked with exact Fractions at
(n,m,k)=(2,3,1),(2,4,2),(3,3,1), giving expectations 24,363,14. A separate
natural draw at n=2,m=15,k=1 had four good sectors; its all-sector instrument
had clean acceptance .5, rejected all singleton error states for every secret,
and satisfied the binomial-tail bounds at p=.01,.001. These are finite
controls, not evidence for a scalable decoder. They remain useful checks of
normalization and of the discarded, more elaborate approach.

### Falsification Checks And Revised Gemini Tasks

Equation (10) was checked for EVERY error mask by exact enumeration at
(n,m)=(2,3), delta=1,2,3, and (3,3), delta=1,4. The means were respectively
4 and 2. A separate complete n=2,m=3 natural-label ensemble used a correlated
but prelabel error law q_0=.4,q_1=.2,q_7=.4. All 64 label tuples passed
physical completeness and all-secret density-matrix checks. Mean acceptance
was .2875 and mean B was .0875, below 1/(3*lambda)=1/6. Thirty-eight source
tuples met the good-fraction criterion. The asymptotic probability bound is
vacuous at this size and was not fitted to these outcomes.

The prelabel condition has an explicit counterexample. Set E_i=a_i mod 2
with probability 1/2 and E=0 otherwise. The nonzero error changes secret d
to d+N/2. For odd delta the two targets are orthogonal, but their noisy
source states are identical, so no instrument beats fidelity 1/2 on the
uniform-secret ensemble. Here p0>=1/2 but the noise depends on the labels.
For a=(1,2,3,5,7),N=8 the alias mask is 29; exact response tables obey
A_t(29)=(-1)^t D_t. This is not an allowed counterexample to (13), but it
falsifies dropping its noise-independence premise.

Gemini should extend the existing purification diagnostic with (10)-(14),
the ENTIRE instrument completeness check and exact noise/source-law fields.
Do not test isolated filters and assume their sum is trace-nonincreasing.
Keep the analytic high-probability certificate separate from finite runs,
and do not normalize on good sources without charging their failure rate.
Preserve the noise-alias countercontrol and the distinction between fixed
target labels and adaptive target selection. No new candidate, bulk feature
solver, speedup gate, or claim of efficient purification is warranted.

The main theoretical obligation is now sharper: find a full-label-sensitive,
polynomial-cost coherent arithmetic construction with useful aggregate
normalization. Another natural-instance purity or Gram-conditioning lemma
does not address that obligation.
