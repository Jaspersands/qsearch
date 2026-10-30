# Growing-Prime Polynomial Phase Copies: A Known-Technique Baseline

2026-10-22. Local adaptation under review, with exact public-controller and
bounded physical-instrument tests. NOT a new quantum algorithm claim,
classical dequantization, implemented scalable learner, or independent proof.

## 1. Question And Decision

Could the copy-only Rees receiver provide the first efficient learner of
unknown multivariate polynomial phases over a growing prime field?

The input is fresh IID copies of

    |psi_F> = p^(-n/2) sum_(x in F_p^n) omega_p^F(x) |x>,
    total_degree(F) <= d < p,

with fixed d, variable n and odd prime p given in binary. Output all
coefficients except the physically unobservable constant. No F evaluator,
known preparation circuit, preparation inverse, conjugate copies, chosen
restricted source, or hidden coefficient is supplied to the controller.

**Decision: do not promote this as an application needing the Rees receiver.**
There is a local direct polynomial-time argument using known diagonal phase
elimination, with a copy-only front end described below. It is still under
review: adapting published components does NOT itself establish that this
exact learning theorem was previously published. This weakens the case
that the family needs Rees, without settling priority, proving classical
learnability from quantum copies, or refuting the Rees construction.
Comparing polynomial exponents is not evidence of a major new speedup.

2026-10-28 update: an explicit fixed-axis rank invariant sharpens the source
envelope below. Its exact public-map checker and countercontrols are now
implemented; there is still no executed scalable learner or independent
review of this new rank argument. A requested reviewer hit its usage limit
before returning findings. Do not count that as an approved review.

## 2. Access-Matched Prior Art

- [Ivanyos--Santha, Section 5 and Theorem 3](https://arxiv.org/pdf/1503.09016)
  provide the relevant public-coefficient phase elimination and polynomial
  diagonal-system solver. The local work below supplies the multivariate
  copy-only front end and an explicit local-retry budget. It is an adaptation
  of that method, not an independently invented cancellation algorithm.
- [Decker--Ivanyos--Santha--Wocjan, Section 5.3](https://arxiv.org/pdf/1107.2189)
  already solve multivariate constant-degree scalar HPGP with oracle input.
  Their chosen restrictions must not be silently supplied by unknown copies.
- [Arunachalam--Bravyi--Dutt--Yoder, equations 3--4, Table 1, Section 5](https://arxiv.org/html/2208.07851v2)
  use Boolean-domain generalized phase states. Their generalized learner's
  stated runtime is not polynomial; the binary separable learner is efficient.
  The earlier blanket binary/generalized efficiency statement is corrected.

No absent search hit establishes novelty. The application uses a metabelian
translation/phase group, so it would not demonstrate the necessity of the
new proposed beyond-metabelian Rees scope in any case.

### July 2026 Learning Question

[Alrabiah--Arunachalam--Grewal--Wright, Sections 1.3 and 4](https://arxiv.org/html/2608.00265v1)
ask for the optimal copy complexity over prime fields, conjecturing the
same Theta(n^(d-1)) behavior as the binary case. Their Section 4 distinguishes
generic polynomial-copy tomography from an optimal measurement analysis.
The introductory open-learning statement is not a contradiction to our
much looser, fixed-degree resource argument. Conversely, this local
construction does not settle their conjecture or their growing-degree
testing question. Gate efficiency, optimal samples, degree dependence and
dependence on numeric p versus log(p) are different claims. Independent
verification and a fuller priority check of our exact copy-only adaptation
remain outstanding.

## 3. Copy-Only Front End

Maintain a PUBLIC affine description

    F = G + sum_(k=1..ell) eta_k B_k  (mod constants),

where G is known and B_k are independent, nonconstant coefficient vectors.
Initially G=0 and B_k are the N=binomial(n+d,d)-1 nonconstant monomials.
The eta_k are unknown and are not controller inputs.

Select a coordinate j occurring in some B_k. Because d<p, dependence is
formal and functional, without x^p-x aliases. On ONE fresh copy, measure
all coordinates other than j in the computational basis. The outcome
y in F_p^(n-1) is uniform, independent of F. Do not request a chosen y or
try to collect a repeated y. Apply the known restricted diagonal phase
-G(y,t) to the retained coordinate. Its state is, up to global phase,

    p^(-1/2) sum_t omega^(sum_(r=1..d) t^r sum_k Y[r,k] eta_k) |t>,

with Y publicly computed by polynomial restriction. Accept if Y is not
identically zero. Some nonzero coefficient polynomial in y has degree at
most d-1. Schwartz--Zippel gives acceptance at least

    a = 1-(d-1)/p >= 2/(d+1).

Every rejected copy is charged. Different accepted packets may have
different Y. Their distribution need not be uniform and may change after
each learned relation. The next step only requires their public maps.

## 4. Degree Elimination And A New Equation

Suppose independently prepared packets have degree at most r>=2 and
nonzero public maps. If one has degree below r, use it directly. Otherwise
every top row is nonzero. Obtain a nonzero PUBLIC solution delta to

    sum_i delta_i^r Y_i[r,k] = 0 for every k.

At sufficiently many packets the cited fixed-degree SDE theorem provides
such a solution in polynomial time in ell and log p. The conservative
arity reused from the repository is

    B_r(ell) = [r^(r(r-1)/2) (ell+1)^r]^ceil(log2(r+1)).

Prepare a fresh uniform t register, subtract delta_i*t from source
coordinate i, and measure the source coordinates to obtain mu_i. The
joint distribution of mu is uniform: all premeasurement amplitudes have
equal magnitude. The retained phase has public rows

    Z[s,k] = sum_i sum_(j=s..r)
                 binomial(j,s) delta_i^s mu_i^(j-s) Y_i[j,k].

The degree-r row vanishes. Some nonzero delta_i multiplies a nonzero
Y_i[r,k]; hence the corresponding coefficient of mu_i in Z[r-1,k] is
r*delta_i^(r-1)*Y_i[r,k] != 0. Thus the entire new map is nonzero with
probability at least 1-1/p. Discard and retry if it is zero. A lower-degree
nonzero result is also useful; requiring degree EXACTLY r-1 is unnecessary.
No unknown eta occurs in the acceptance test or diagonal-system equations.

Repeat down to degree one. Inverse Fourier measurement returns b=v.eta
for a PUBLIC nonzero row v. Even if b=0, this is a useful equation. Solve
for a pivot eta_j and substitute it into G and the remaining B_k. Their
independence modulo constants is preserved; ell decreases by one. Repeat
until ell=0. This recovers linear terms too, unlike ray symmetry alone.

This argument does not require a polynomial orbit gap or the Rees theorem.
The public controller is exactly the existing PhasePacket/translate_combine
mechanism plus the new restriction and affine-parameter updates.

## 5. Whole-Run Cost And Precision

Use local restarts, NOT the potentially useless bound "number of merges/p"
when p is smaller than the source tree. Each merge generator retries using
fresh independent successful child packets. Conditional on any child maps
meeting the contract, its success probability is at least 1-1/p. Iterated
conditioning gives the conservative expected ORIGINAL copy envelope

    E <= (N/a) product_(r=2..d) [B_r(N) * p/(p-1)].

Skipped degrees only reduce this envelope. N rounds upper-bound the number
of parameter eliminations; using the initial N overcharges every later SDE.
For total error epsilon, abort after ceil(2E/epsilon) original copies.
Markov bounds this abort probability by epsilon/2. Allocate epsilon/2 to
the complete-circuit approximation error, including field-uniform sources,
Fourier transforms and controlled phase rotations. Their precision depends
on the logarithm of the capped circuit length, not numerical p.

At fixed d the copy count and arithmetic work are polynomial in n, log p
and 1/epsilon. The dimension of the known coefficient space is polynomial;
all SDE, polynomial restriction and field operations are on that space.
The envelope is NOT a numerical gate estimate or a practical runtime claim.
The general SDE backend and quantum execution remain unimplemented here.

### Fixed-Axis Coefficient Filtration

Fix one coordinate j for the ENTIRE recursive tree producing one equation.
It may change between learning rounds, after discarding old packets and
constructing a new public frame. For each original nonconstant monomial
alpha, let b_alpha be its coefficient row in the current unknown eta
coordinates, so its coefficient is known_alpha + b_alpha.eta. Define

```
W_(j,r) = span_Fp {b_alpha : alpha_j >= r},
K_r = binomial(n+d-r, d-r).
```

There are exactly K_r such original monomials: subtract r from alpha_j
and count total degree at most d-r in n variables. Consequently
`dim W_(j,r)<=min(ell,K_r)`, and W_(j,r+1) is contained in W_(j,r).
This is a sufficient equation-rank bound, NOT an SDE arity lower bound.

An initial restricted t^r coefficient is a linear combination of b_alpha
with alpha_j=r. For a general translated/dilated merge, its new t^r row
is a linear combination of child t^s rows with s>=r. If child rows lie
in W_(j,s), nesting puts their combination in W_(j,r). Induction over the
actual tree proves the invariant after arbitrarily many legal merges,
including zero scales and lower-degree outputs. Known diagonal correction
removes known terms without altering these unknown-coefficient spaces.
Affine parameter elimination simply maps every b_alpha linearly to the
new eta coordinates; it cannot increase the bound. Packet maps from the
old frame must not be used unchanged in the new one.

Thus degree-r cancellation has at most K_r equations after compression,
not N. Replace B_r(N) in the earlier envelope by B_r(K_r). The copy bound is

```
E_coordinate <= (N/a) product_(r=2..d) [B_r(K_r)*p/(p-1)].
```

The original slice and merge rejection factors remain paid. For the
large-field symmetric construction, reduce each erasure exponent r to
g_r=gcd(r,p-1). Use K_r+1 if g_r=1; otherwise require
`p>=16*g_r^(2*g_r+2)` and use `(K_r+1)*((g_r-1)*K_r+1)`.
For fixed d and all these field guards, the resulting coarse source
bound is O_d(n^(d^2-2*d+2)) at constant failure allowance: N=O_d(n^d),
and the quadratic arity factors contribute exponent
`2*sum_(r=2..d)(d-r)=(d-2)*(d-1)`. Cubic degree gives O(n^5), NOT the
optimal O(n^2) target. This is a written source-count deduction, not a new
implemented quantum algorithm or a total gate-count theorem.

At n=8,d=3, K_3=1 and K_2=9. The symmetric arities are6 and100 at the
127-bit control prime. The source envelope is evaluated with exact
Fractions and local rejection costs; no field table is constructed.

The axis condition is essential: the x^3 and y^3 coefficient rows of
two different coordinate restrictions are independent, even though
K_3=1. Combining them invalidates the sharpened bound. Conversely, the
cubic signed pair at one axis can produce quadratic rows of rank n+1;
discarding the higher original-coordinate monomials would undercount.
Tests check both phenomena, as well as arbitrary affine frame updates.

`coordinate_row_space` and `check_coordinate_packet` certify only the
PUBLIC coefficient-map invariant. They do not certify state preparation,
fresh-copy provenance or physical evolution. `coordinate_copy_envelope`
reports both the published and guarded symmetric schedules. Like the old
source envelope, it does NOT include arithmetic failure/runtime or an
implemented approximation budget. The bounded SDE from
POWER_SDE_RANDOMNESS_BUDGET.md can supply local failure guarantees, but a
complete adaptive learner still needs the whole-tree allocation.

## 6. Why The Rees Application Initially Looked Plausible

There is also an analytic orbit-gap argument, not a sampled gap promise.
Let V be polynomials of degree <=d-1 including constants, and

    R(a,Q)=Z_Q X_a,
    (a,Q)(b,P)=(a+b,Q(x)+P(x-a)).

This is a public linear representation of a metabelian group of class at
most d. For p>d its exponent is p: summing a translated degree-(d-1)
polynomial over a p-step orbit is zero. The ray stabilizer is exactly
Q(x)=F(x)-F(x-a)+constant. Its Lie graph is

    h_F = {(a, D_a F + constant)}.

Consequently a correct ray-stabilizer learner would expose all derivatives
mod constants, hence all degree>=2 coefficients (division by exponents is
legal). Subtract the known nonlinear part and a final QFT recovers the
linear coefficients. Forgetting that last step loses information.

For an element outside the stabilizer, the overlap is the mean of omega^P
for a nonconstant polynomial P of degree D<=d-1. Iterated Cauchy--Schwarz
gives |E omega^P|^(2^D) <= E omega^(Delta_h1 ... Delta_hD P). The last
phase is the nonzero multilinear polarization of the top part, since p>D.
Averaging h_D turns it into the probability that a linear functional is
zero. A nonzero coefficient has degree D-1 in the earlier h blocks, so
that probability is at most (D-1)/p. For D=1 the overlap is zero.
For any bound r>=D with r<p, concavity therefore gives the safe gap

    gamma >= (1-(r-1)/p)/2^r.

Take r=d-1 for d>=2. This is constant at fixed degree, independent of n
and numeric p. It is a written analytic argument, not a formal proof.
It removes an access/gap objection to THIS family, but Section 4's simpler
known-technique adaptation weakens the case that Rees is needed. That
adaptation and its precise priority still require review. A valid reduction
is not automatically a valuable new application.

## 7. Falsifiers And Boundaries

- PURE AFFINE SUPPORT IS NOT AN ESCAPE: for a uniform-magnitude pure phase
  state on a single unknown affine space a+U, computational measurements
  give uniform samples there. Fix one sample x0 and span t further sample
  differences. If dim(U)=k, the failure probability is at most
  (p^k-1)*p^(-t)/(p-1), by a union bound over nonzero linear functionals
  modulo scalars. Taking t=n+s gives a bound <=p^(-s)/(p-1), without knowing
  k. Pay these n+s+1 copies. On success, complete the recovered basis to an
  ambient invertible matrix and perform the known affine coordinate change.
  The remaining k coordinates give full-domain degree<=d phase copies.
  Only the restriction of F to the support is identifiable; ambient
  coefficients outside the support cannot be recovered. For k=0 there is
  no relative phase to learn. This elementary extension is a written
  reduction, not an implemented source-learning backend.
- MIXED COHERENCE IS DIFFERENT: the mixed kernel proportional to
  1_(x-y in U)*omega^(F(x)-F(y)) has a uniform ambient diagonal; measuring
  points does NOT reveal U. For U=0 it is maximally mixed, independent of F.
  The earlier unknown-U obstruction to recovering EVERY ambient coefficient
  remains valid. This is NOT a hardness result for learning U: existing
  affine_phase_erasure machinery already addresses phase cancellation on
  parallel affine supports and must be checked before proposing that task.
  Arbitrary amplitude-weighted or nonaffine support is outside this argument.
- SMALL CHARACTERISTIC: d>=p invalidates the derivative/polarization and
  formal independence arguments. x^p-x is the simplest counterexample.
- GROWING DEGREE: the SDE arity/exponents and monomial count are not uniform
  polynomials in d. This does not make growing-depth phase states learnable.
- UNCHARGED POSTSELECTION: collecting a fixed repeated slice would cost
  p^(n-1). The actual front end uses different random slices and public Y.
- FALSE DEQUANTIZATION: this is a collective quantum-copy algorithm. With
  ordinary value-oracle access, polynomial interpolation is already easy;
  without it, a classical-access speedup comparison is not defined here.
- GENERALIZED BINARY STATES: the Boolean domain and even phase modulus in
  the cited learner are different promises. Neither result can simply be
  relabeled as the other.
- NOVELTY: an efficient corollary of established elimination methods is
  insufficient justification for a breakthrough candidate. Independent
  review may simplify the argument further or identify an existing theorem.

## 8. Implemented Scope And Next Decision

theorems/polynomial_phase_copy_learning.py implements public coordinate
restriction, coefficient-basis substitution, checked degree erasure using
existing machinery, and exact rational copy envelopes. Its APIs never take
the unknown eta. The standalone --write report preserves all blocked flags.

Tests check the random-slice physical state, a tight rejected-slice bound,
all25 records of a cubic instrument, all125 records for distinct public maps,
an actual two-instrument branch followed by Fourier readout,
coefficient-preserving parameter elimination, and
127-bit-prime budget arithmetic. The selected two-stage branch has mass
5^-6 and consumes FOUR independent original copies. It is not a free
postselection or an end-to-end learner benchmark. Source enumeration and
hidden eta are confined to test fixture state construction and expectations.

Earlier verification:219 connected tests pass (116.43s),
including11 new controls. Python syntax, all12 site JavaScript syntax checks,
qsearch validate (valid=true, issues=[]), the live --write workflow and
whitespace checks pass. Full repository suite and Lean were not run.

2026-10-28 fixed-axis update:304 connected tests PASS in41.29s, including
22 phase-copy cases (11 added in this update). Five changed Python files
compile, all12 actual site JavaScript syntax checks pass, and registry
validation returns valid=true, issues=[]. The live report was regenerated
with `python qsearch.py phase-copy-baseline --write`; its bounds are prior
resource estimates, not observed quantum copy consumption. Full repository
suite and Lean were not run. Independent review of this update did not
complete and remains required.

### Bounded Controller Implementation (Completed 2026-10-28)

The end-to-end instrument controller has been implemented in
`theorems/polynomial_phase_copy_learning.py` (`PhaseCopyController`), with an
opaque test backend in `theorems/phase_copy_statevector_backend.py`
(`StateVectorPhaseSource`) and tests in `tests/test_polynomial_phase_copy_learning.py`.
The initial implementation was reported to satisfy the following constraints;
the parent audit below found and corrected missing boundary enforcement:
- Operates exclusively on opaque integer handle IDs and public outcomes;
  hidden coefficients, state vectors, and value oracles are never accessed.
- Freezes both `LearningFrame` and coordinate `axis` per tree, starting fresh
  with new tree IDs after each `frame.learn_relation`.
- Charges every original copy against `CopyLedger`: `drawn == discarded_slices +
  zero_scale_consumed + failed_merges + used_in_relations + aborted_leaves`.
- Reads out linear-phase relations physically via simulated Fourier measurement.
- Allocates solver failure bits across the tree (`ControllerBudget.solver_bits`)
  and handles `SourceCapExhausted` and solver randomness exhaustion as explicit `ABORT`.
- Six negative controls pass: state reuse rejection, mixed-axis filtration check,
  stale frame rejection, invalid witness rejection, Fourier convention sign, and
  source-cap exhaustion.
- Fails closed with `ValueError` when $p < 1024$ (below the certified symmetric regime).

Independent adversarial review was completed in
`research/audits/reviews/2026-10-28-phase-copy-power-sde-review.md`. The fixed-axis
rank bound is verified; `coordinate_rank_bound_independently_reviewed` is updated to True.
No quantum speedup, scalable quantum learner, or novelty claim is promoted.

#### Parent Adversarial Follow-Up (28 October)

The received review's controller verdict was too strong. Three new failing
controls reproduced these defects before repair:

1. `ControllerBudget.copy_cap` was computed but never checked before source
   draws. With a forced cap of one and an uncapped physical fixture, the
   learner returned OK instead of ABORT. The controller now checks its own
   original-copy cap before every draw; it does not rely on a backend cap.
2. When children were already below the erasure degree, the branch called
   `shear_merge` then returned a consumed input handle. It now returns the
   new handle and applies the observed translation to the public packet.
   For a retained quadratic, the shift by five really introduces the
   linear coefficient ten; preserving the old packet is wrong.
3. A mixed batch with an already usable lower-degree child unnecessarily
   entered the SDE path. The controller now selects ANY such child before
   SDE. Consequently all children entering SDE have nonzero degree-D maps.
   A nonzero SDE witness must activate one of those maps, so the degree-D-1
   row depends nontrivially and linearly on a fresh uniform shear outcome.
   This supplies the premise behind the at-most-1/p merge failure bound.

`tests/test_phase_copy_controller_boundaries.py` retains the failures, a
non-first-child control and a small-field countercontrol. Its opaque
branch fixture checks controller ownership and symbolic transport only;
it is not an independent quantum simulation. The existing state-vector
tests still check full finite recovery and both Fourier conventions.

The received review also incorrectly promoted the d=p-1 border obstruction
to SDE nonexistence. At the proposed arity M=(r+1)((d-1)r+1),
M-dr=(d-1)r^2+1>0. Chevalley-Warning therefore guarantees a nonzero solution
for EVERY homogeneous r-equation system, even in the small-field regime;
see [Ivanyos--Santha, Introduction](https://arxiv.org/html/1503.09016v2).
The actual obstruction concerns only a universal two-level contraction
using the specified axis identities. It is not an impossibility result
for SDE or the Rees receiver. The test exhausts all five-column scalar
inputs over F5 and constructs a zero subsum; three unused columns embed
each witness into the arity-eight case. This is a finite countercontrol,
not a general efficient solver at the Chevalley-Warning threshold.

The original Gemini review is preserved unchanged. Its rank-filtration
argument remains valid; the code review corrections do not alter K_r.
Quantum gate synthesis/precision, general physical backends and native
applications remain outside the implemented finite-fixture controller.
Backend release of discarded and aborted registers is a remaining concrete
lifecycle task, not a reason to infer new quantum leverage.

Next scientific work: review this adaptation, then seek an application
OUTSIDE full-domain or pure-affine fixed-degree phase learning. Prioritize
genuine mixed-coherence or nonmetabelian structure only if its source is
naturally available and its gap is proved. Do not promote an abstract oracle
promise, add another planted family, or optimize this baseline's constants
by inertia.
