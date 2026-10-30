# Full Pauli Conjugation Symmetry From Purity And Separation

Status: a constructive mathematical deduction and finite/public controls,
not a compiled quantum learner, novelty certificate, or classical-input
speedup. This extends the quadratic part of
[peak-weight learning](PEAKED_PHASE_NOISE_LEARNING.md), not its higher-degree
polynomial-phase theorem. The supplied gap below is a substantive promise.

Decision after adversarial review: **prefer the direct skew Bell route below**.
An extension of an existing operator identity removes the random graph charts,
isotropic extraction and eigenlabel completion stages from the main algorithm.
Those stages remain an independently checked alternative and classical-access
control, not additional work required by the preferred route.

Application update: the [query-and-discard source filter](PARTITION_SOURCE_CLASSICAL_FILTER.md)
constructively dequantizes H recovery for that matched classical-evaluator
source family under these same promises. Other examples have excellent
purity/gap but H independent of the intended hidden object. Neither is a
general quantum-input simulation theorem; both require solution decoding
to be checked before interpreting this learner as an algorithmic advantage.

## Problem And Identifiable Target

Let p be an odd prime, and let rho on n p-level systems be exactly diagonal
in some unknown maximal commuting Pauli basis L. Arbitrary eigenweights,
including full support, are allowed. The input is IID copies, not a density
matrix, eigenweight table, state-preparation circuit, or classical evaluator.
Supply an integer R>=1 and rational delta>0 such that

    gamma = Tr(rho^2) >= 1/R,
    d(v) = gamma - Tr(rho W_v rho W_v^dagger) is either 0 or >= delta.

The target is the FULL phase-free conjugation group

    H = {v : W_v rho W_v^dagger = rho}.

Since d(v)=||rho-W_v rho W_v^dagger||_2^2/2, zero loss is exactly this
condition. H is an F_p-linear subspace containing L. Hence H^perp is
contained in H (coisotropic), but H itself can contain noncommuting Paulis.
Recovering the original L or original pure-state eigenvalue signs is not
promised: those need not be identifiable. Complexity is polynomial in
n, R, delta^-1, log p and inverse failure probability. Polynomial R and
inverse gap are needed for an efficient guarantee. This is not arbitrary
mixed-state tomography; extensive maximally mixed noise can make R
exponential. No R<p assumption is imposed.

## Preferred Direct Skew Bell Route

This is a deduction from the operator identity in Allcock et al.,
[Theorem 43 and Corollary 46](https://arxiv.org/html/2510.06848v3#S3),
combined with the finder/verifier perspective of Tang and Steckmann,
[Algorithm 4 and the paragraph following Theorem VI.2](https://arxiv.org/html/2610.03307v1#S6.SS1).
The latter already discusses allowing noncommuting symmetries. This is not
claimed as a new general discovery paradigm.

Choose public a,b in F_p with a^2+b^2=-1 and set

    M = [[a,b],[b,-a]], so M^T M=-I.

Finite-field sampling and square roots find such a pair with constant
success probability; charge bounded search and verify the equation. For
p=3, a=b=1 works; zero entries are allowed for suitable other primes.
Use the eight-copy M-skew Bell difference experiment and retain one marginal
Pauli label X. Put D=p^n and c(u)=|Tr(rho W_u)|^2. Its law is

    q_rho(x) = D^-2 sum_u omega^[x,u] c(u)c(a u)c(b u).

The operator/Fourier identity extends to mixed tensor-power inputs by taking
the trace term by term. The later pure-state convolution simplification in
the cited theorem does NOT extend: sum c(u)/D=Tr(rho^2), not generally 1.
Our finite reference tests the actual four-copy skew/Bell measurement and
the difference of two independent outcomes against this Fourier expression.
The finite Bell reference labels a single qudit by (phase,shift); public
symplectic algebra uses global (x_1,...,x_n,z_1,...,z_n). A future receiver
must explicitly reorder these labels, not pass raw tuples between them.

From the Weyl expansion, H=(span{u:c(u)!=0})^perp. Thus q is constant on
each H-coset: its Fourier support is contained in the support of c. Samples
conditioned on belonging to H are uniform on ALL of H, including when H
is noncommuting. This conditional law is only used in the proof, not an
unavailable membership postselection oracle.

In a witnessing diagonalizing basis (used for analysis, never supplied to
the algorithm), c is supported on L and is the squared Fourier transform
of the eigenlabel law w. With six independent labels B_i,B_i' drawn from w,
Fourier orthogonality gives

    q(0) = D^-1 Pr[(B_0-B_0')+a(B_1-B_1')+b(B_2-B_2')=0].

The event B_i=B_i' for all three pairs has probability gamma^3. Since
|H|>=D and q is constant on H,

    Pr[X in H] = |H| q(0) >= (|H|/D) gamma^3 >= R^-3.

Generate candidates, apply the fresh-copy purity/overlap verifier, and span
ALL accepted labels. Do not impose commutativity, do not try to infer a
designated original L, and do not accept their unverified span wholesale.
Use an ideal-classifier coupling for the spanning analysis and add the
simultaneous estimation failure separately. Before H is spanned, each
proposal increases its span with probability at least (1-1/p)R^-3. The
dimension is at most 2n. Output the final span after a fixed cap; no early
rank-n stopping rule is valid for this full-H target.

`PurityGapPlan.direct_caps` sets beta=epsilon/4 and

    T = 16 R^3 (2n+ceil(log_2(1/beta))), K=T+1,
    m = ceil(128 delta^-2 ceil(log_2(2K/beta))),
    raw copies <= 8T + 2K m.

Purity is estimated once; each overlap uses m fresh SWAP pairs. Means have
accuracy delta/8 and loss threshold delta/2. The four beta allocations are
candidate spanning, all mean estimates, bounded public field constructions,
and complete-instrument approximation across the entire adaptive run.
This preferred route has logarithmic failure-probability dependence.

Arithmetic on p-level registers and the skew linear map must be compiled
using modular arithmetic and approximate Fourier transforms; treating a
qudit gate as unit cost is NOT itself a bit-complexity proof. The gate
construction remains an explicit imported obligation here. It needs
polynomial(log p, log(1/eta)) precision cost per primitive, and the sum of
instrument half-diamond errors must fit the last beta budget.
Arbitrary-modulus approximate Fourier circuits are an established primitive;
see [Cleve-Watrous](https://arxiv.org/abs/quant-ph/0006004). The repository
does not yet implement that binary-encoding compilation for this receiver.

## Alternative: Finding Any Diagonalizing Basis

Use a uniformly sampled Clifford graph chart. A fixed Lagrangian becomes
a graph with probability product_(j=1)^n (1+p^-j)^-1 > 1/2. Uniform
symplectic sampling and its bounded rejection clocks are required; a short
random Clifford word is not a substitute. The constructive sampler and
compiler obligations are detailed in the peak-weight note.

On a good chart the eigenbasis consists of common quadratic phases
q(x)+b.x. The [four-copy instrument](NOISY_QUADRATIC_PHASE_FILTER.md) gives

    y uniform in F_p^n, z=A y+e, e=sum_(i=1)^4 a_i b_i,
    sum a_i=sum a_i^2=0, a != 0.

Zero entries of a are allowed and their copies remain charged. The labels
are independent with weights w. The unobserved all-equal event gives

    Pr(e=0) >= sum_b w_b^4 >= (sum_b w_b^2)^3 = gamma^3 >= R^-3.

For the second inequality, apply Jensen to w_B^3 with B sampled from w.
This event is not postselected or requested. Its y labels are uniform,
independently of the event, and thus generate L with polynomial samples.

Verify EVERY proposed Pauli using fresh-copy SWAP estimates of purity and
conjugated overlap. Pull chart labels back before verifying on original
copies; no conjugated unknown state is supplied for free. Estimating each
mean to delta/8 makes the estimated loss accurate to delta/4. The threshold
delta/2 therefore separates H from its complement on the simultaneous
estimation event. Proposals may be adaptive, but verification pairs are
fresh, so the conditional Hoeffding bounds and union bound still apply.

Let V be the span of accepted labels. On honest verification, V is a
subspace of H. On a good chart sufficiently many zero-error proposals
ensure L is contained in V. Accepted extra symmetries must NOT be discarded
merely for noncommutation or forced onto a single graph matrix.

Symplectic Gram-Schmidt extracts a maximum-dimensional isotropic subspace
of V. Its dimension is (dim V + dim rad V)/2. Return only if this is n;
otherwise abort the chart. Any returned L' is a maximal commuting Pauli
space inside H, so rho is diagonal in its basis. This success test is sound
even on bad charts, where the regression law is NOT asserted. The existing
public Witt-extension and Clifford compiler can map L' to the standard Z
basis. Phases of the chosen Clifford only relabel the measured eigenvalues.

## Alternative: Classical Completion Once L' Is Known

Measure fresh copies in the known L' eigenbasis, obtaining classical labels
B with an unknown distribution w' on F_p^n. Its translation period group U
satisfies H/L' = U. If u=|U| and q_C are the masses of its cosets, then

    gamma = (1/u) sum_C q_C^2 <= 1/u, hence |U| <= R.

Also max w' >= gamma >= 1/R. For an empirical histogram from m independent
labels, E||hat w'-w'||_2^2 <= 1/m, independently of the domain size. With
m>=16R^2/beta, Markov implies ||hat w'-w'||_infinity <= 1/(4R) except
with probability beta. Choose its empirical mode b0 (deterministic ties).
Then w'(b0)>=1/(2R). Store only observed labels, never the p^n-entry table.

In 2R ceil(log_2(R/beta)) further independent samples, all members of
b0+U appear except with probability beta: each has probability at least
1/(2R), and there are at most R. Propose only differences B-b0 observed in
that batch, not every possible field vector.

These proposals require NO further collective quantum measurement. For
fresh independent measured pairs (B,B'),

    E[1_(B=B')] = gamma,
    E[1_(B-B'=f)] = sum_b w'_b w'_(b-f).

Thus classical Bernoulli collision estimates implement the same purity-loss
test. With simultaneous accuracy delta/8 and threshold delta/2, accept
exactly the true periods among the proposals. Their span is U; together
with L' and the known label-shift Pauli lifts it generates H. The labels
come from a basis learned using quantum copies. Granting that basis to a
classical competitor from the start would change the input problem.

The independent classical review found a stronger implementation bound:
use s=R ceil(log_2(R/beta)) discovery samples and propose all pairwise
differences (at most s^2). A fixed unknown heaviest orbit has at most R
members of mass >=1/R each, so coverage fails with probability <=beta.
For an empirical histogram a from t labels, bounded differences gives
||a-w'||_2 <= (1+sqrt(ln(1/beta)))/sqrt(t), except with probability beta.
Take t=ceil(64 delta^-1(1+ceil(log_2(1/beta)))). Then simultaneously for
every shift f,

    f in U:     d_a(f) <= delta/16,
    f not in U: d_a(f) >= 9 delta/16,
    d_a(f) = ||a-T_f a||_2^2/2.

Threshold at delta/4. Sparse-histogram evaluation costs polynomial time
without enumerating the domain. This gives O(R log(R/beta) +
delta^-1 log(1/beta)) classical label samples, trading more pairwise
proposals for fewer samples. It follows from a distribution-wide l2 error
event, so adaptive proposals cause no additional union-bound problem.
The executable alternative clocks below deliberately retain the simpler,
looser independent-pair baseline; they are not sample-optimality claims.

## Alternative Route Clocks

`theorems/pauli_symmetry_source.py::PurityGapPlan` uses beta=epsilon/8:

    h = ceil(log_2(1/beta)) graph charts,
    t = 16 R^3 (n+ceil(log_2(h/beta))) proposals per chart,
    Q = h t, K_Q = Q+1,
    m_Q = ceil(128 delta^-2 ceil(log_2(2 K_Q/beta))).

Analyze spanning first with an ideal exact membership classifier, then
charge estimation errors by a separate union/coupling bound. Conditioning
on the eventual event of accurate verification could bias the proposals.
Before the correct n-dimensional graph is spanned, a proposal extends its
zero-error span with probability at least (2/3)R^-3. A binomial lower
coupling and Chernoff give failure at most beta/h for the stated t. There
is no union over all p^n hyperplanes and no hidden numeric-p cost here.
For SWAP outcomes in {-1,+1}, Hoeffding with accuracy delta/8 gives the
stated m_Q. One purity estimate is shared, with its error included.

Let A=ceil(16R^2/beta), C=2R ceil(log_2(R/beta)), K_C=C+1, and
m_C=ceil(128 delta^-2 ceil(log_2(2K_C/beta))). The classical collision
Bernoulli estimates obey the same conservative bound. Total raw copies:

    4Q + 2K_Q m_Q + A + C + 2K_C m_C.

The eight beta allowances are: no good chart; failed candidate span on
good charts; all SWAP estimates; finding a heavy anchor; covering its
period coset; all classical collision estimates; bounded public random
constructions; and complete quantum instrument approximation. Reserve the
last allowance across ALL physical calls, including failed charts and
rejected candidates, using conditional-instrument composition. No exact
physical sampling or free repeated source reuse is asserted.

## Falsifiers And Scope

- Full-rank noncommuting example: p=3, n=2, computational eigenweights
  w_(a,b)=(3,2,1)_b/18. Purity is 7/54>=1/8; U=F_3 times {0}; outside
  loss is 1/36. H has dimension 3 and contains X_1,Z_1,Z_2. Its original
  maximal commuting basis is not unique. Forcing all accepted symmetries
  into one Lagrangian would be incorrect.
- A supplied inverse-purity bound alone does not imply a positive uniform
  symmetry gap. On one qutrit, w_t=(1-t)uniform+t delta_0 has purity
  (1+2t^2)/3>=1/3. At t=0 the conjugation group is all Pauli labels; at
  every t>0 it is only the diagonal Z line, and each outside loss is t^2.
  The single-copy trace distance from t=0 is 2t/3. By telescoping, m copies
  have distance at most 2mt/3. Exact full-group identification with constant
  success therefore needs Omega(1/t) copies in this family. This is a
  conservative lower bound, not a tight complexity claim.
- A positive tiny eigenvalue tail can break exact periods. Approximate
  invariance is a different target; do not use these clocks without delta.
- A stronger lower bound does not rely on small eigenvalues. Let
  q=(2/3,1/6,1/6), r_t=(1/3+t,1/3-t,1/3), and rho_t=diag(r_t) tensor
  diag(q), for rational 0<t<=1/6. All nine eigenvalues are >=1/36,
  purity=1/6+t^2, and the smallest positive loss is delta_t=3t^2/2.
  The group drops from dimension 3 at t=0 to dimension 2 at every t>0.
  Trace distance is t and chi-square divergence of the eigenweights is
  6t^2. For N copies the trace distance is at most
  sqrt((1+6t^2)^N-1)/2. Constant-error exact-group recovery therefore
  requires Omega(1/delta_t) copies, even with arbitrary collective
  measurements. Both inputs obey the SAME R=6 and supplied gap delta_t.
  This does not establish optimality of our delta^-2 SWAP budget.
- Thresholded approximate symmetries need not form a group. For p=5 and
  weights (5,4,3,4,4)/20, d(X)=1/200 but d(X^2)=3/400. Taking the span of
  small-loss candidates without exact-gap classification can manufacture
  elements that fail the same tolerance. State closeness likewise does not
  imply closeness of uniform distributions on their exact symmetry groups.
- Exact diagonality, IID copies and a usable inverse-purity promise are
  not learned or validated by this code. An arbitrary mixed state need not
  admit any Lagrangian inside its Pauli symmetry group.
- Known-basis classical samples solve the remaining period problem above.
  No matched-access classical lower bound or hard classical-input source
  reduction has been established for finding the basis itself.

## Prior Art And Implemented Scope

The candidate/verifier paradigm is not new. Tang-Steckmann's stated theorem
uses qubits, approximate containment and a commuting-group algorithm, but
explicitly suggests its noncommuting extension. Allcock et al.'s stated
learning theorem uses pure inputs. Neither is literally the mixed odd-prime
theorem above; nevertheless their existing machinery supplies the short
direct route after an explicit mixed-input identity check. Treat this as
a corollary assembled from prior machinery pending specialist review,
not a new Shor-level algorithm. Mixed qubit stabilizer bootstrapping also
exists but targets fidelity/list guarantees, not this exact full group
([Chen et al., Section 6](https://arxiv.org/html/2408.06967v3#S6)).

Implemented: polynomial public isotropic extraction without a hidden basis;
eigenlabel proposal/collision/decision kernels; rational resource clocks;
finite independent geometry, mixed skew Bell reference, and actual
density-matrix falsifiers. These do not implement a scalable quantum
candidate instrument, SWAP receiver, or complete adaptive physical learner. Run
`python qsearch.py phase-copy-baseline --pauli-symmetry --write` for the
explicitly scoped report. No registry candidate is promoted by this command.
