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
There is a direct polynomial-time route using known diagonal phase
elimination, with a copy-only front end described below. This removes a
plausible novelty argument; it does NOT prove classical learnability from
quantum copies or refute the Rees construction. Comparing polynomial
exponents is a separate question, not evidence of a major new speedup.

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
known-technique route defeats the claim that this creates a first efficient
learner. A valid reduction is not automatically a valuable new application.

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

Verification after final code edits:219 connected tests pass (116.43s),
including11 new controls. Python syntax, all12 site JavaScript syntax checks,
qsearch validate (valid=true, issues=[]), the live --write workflow and
whitespace checks pass. Full repository suite and Lean were not run.

Next scientific work: review this adaptation, then seek an application
OUTSIDE full-domain or pure-affine fixed-degree phase learning. Prioritize
genuine mixed-coherence or nonmetabelian structure only if its source is
naturally available and its gap is proved. Do not promote an abstract oracle
promise, add another planted family, or optimize this baseline's constants
by inertia.
