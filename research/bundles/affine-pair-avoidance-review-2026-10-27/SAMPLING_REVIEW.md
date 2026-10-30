# Independent Review: Exact Classical Native Norm Sampling

Date: 2026-10-27. Scope: the parent's
[exact sampling proof](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/EXACT_SAMPLER.md),
[earlier approximate proof](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/RESULT.md),
[norm_sampling.py](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/norm_sampling.py),
[exact_control.py](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/exact_control.py),
and the reused norm backend, including the parent's stronger rank-size-biased
derivation. The latter supersedes the approximate-only verdict. This review
is separate from the completed LLL audit in REVIEW.md.

## Verdict

**The proposed rank-size-biased sampler is EXACT uniform on the original
full-support syndrome fiber, conditional on success, under the stated
algebraic premises and exact independent random draws.** The density and
fiber-size factors cancel, including deficient ranks and unreachable targets.
Its guaranteed per-whole-trial success probability is

```text
success >= alpha/Z,
alpha = (1-delta1)(1-eta),     Z = 1+delta0.
delta0 = (q^k-1)q^(-2R),      delta1 = |T|q^2 delta0,
eta = |T|/q^2.
```

No forgotten q^k factor or lambda-rank weighting was found. Arbitrary
admissible zero patterns of h, variable outside coordinates including the
punctured point, and mixtures over admissible h preserve exact native
uniformity. The small-e systematic branch is also exact.

This supports an expected-polynomial EXACT sampling theorem in the covered
range. It does not solve the fixed-prime asymptotic problem or implement
the theoretical matrix-only adapter. The final RankWeightedNormSampler
implementation was independently inspected and its 14 focused tests passed;
no defect affecting the exact-law argument was found.

## Assumptions That Must Remain Explicit

Fix B,s,A,h and nonsquare nu over an explicitly represented odd finite field.
Require full row rank of B and A_T, nonempty T=support(h), nonzero columns
of A_T, and every mixed cancellation identity. The universal restriction
rank lower bound R is a promise or a proved consequence of the native AG
structure, not something certified by a few rank samples. It must be an
integer with 0<=R<=r and r_lambda>=R for every nonzero lambda. Conditions
delta1<1 and eta<1 provide the stated success bound; constant expected trial
count also requires Z bounded. Exactness itself does not require these
success inequalities.

The nonzero-column condition is substantive, not implied by full row rank.
For example, take k=1, A=[I_3 | I_3 | 0],
B=(1,1,1,-1,-1,-1,1), and h=(1,...,1). Cancellation and restriction rank
R=3 hold, but the last marginal rank is zero, so G is empty even though
7(q-1)/q^4<1. The current proof and sampler constructor explicitly exclude
this example. The native A=ev L(8eP0) has nonzero columns because it contains
the constant section. Thus this attempted falsifier does not break the
revised native claim.

## Independent Exact Counting Check

Write t=|T|, o=|O|, V=F_q^(2t), and
S=im(A_T^t) direct-sum im(A_T^t), of dimension 2r. Set

```text
C = q^(2t-2r)     number of S-cosets,
F = q^(2r-k)      reference fiber size,
W = (q-1)^o      number of outside assignments.
```

**Coset invariance.** Mixed cancellation gives Q(s0)=0 for s0 in S and
vanishing polarization between any two elements of S. Hence
Q(x+s0)=Q(x)+M_x(s0), and M_(x+s0)=M_x. Thus rank(M), its kernel, and all
coordinate kernel-image ranks are coset invariants. Neither G nor F depends
on the adjusted syndrome. Full row rank of A_T makes coefficient-to-pair
evaluation injective, so F on good cosets, and F*q^d on reachable deficient
cosets, count actual pairs, not duplicate coefficient representations.
Any particular solution and kernel basis give
the same uniform affine-fiber law.

**Correct incidence rank.** For nonzero lambda in F_q^k, let

```text
c_lambda = B^t lambda,
U_lambda = A_T diag(h_T * (c_lambda)_T),
r_lambda = rank(U_lambda) = rank(A_support(h*c_lambda)).
```

The rank equality follows by deleting zero columns and scaling remaining
columns by nonzero field elements. With odd characteristic and nu!=0,
M^t lambda=(2 U_lambda a, -2 nu U_lambda b), so its vanishing is precisely
the two kernel conditions. Mixed cancellation gives U_lambda A_T^t=0.
Thus the two-component S is contained in these kernels, and conditioning
offsets there does not introduce unequal representatives of an S-coset.

**Unnormalized offset density.** Write L=q^k-1. The incident branch chooses
each particular lambda with probability

```text
(delta0/Z)/L = q^(-2R)/Z.
```

Uniform independent a,b in ker(U_lambda) have density q^(2r_lambda) on
E_lambda={M^t lambda=0}, relative to uniform offsets. Thinning by
q^(-2(r_lambda-R)) therefore contributes exactly

```text
[q^(-2R)/Z] * q^(2r_lambda) * q^(-2(r_lambda-R)) = 1/Z
```

on E_lambda and zero elsewhere. Include the base branch's density 1/Z.
For d=k-rank(M), the total successful offset-generation density is

```text
[1 + #{lambda!=0 : M^t lambda=0}]/Z = q^d/Z.
```

This is a SUBPROBABILITY density, not a normalized offset distribution:
its integral is E(q^d)/Z<=1. Indeed E(q^d-1)<=L*q^(-2R)=delta0 by summing
the individual incidence probabilities q^(-2r_lambda). Remaining mass is
whole-trial thinning failure. There is no missing normalization or need to
sample lambda with rank-dependent weights.

**Exact mass per valid lift.** Fix outside assignment z and any valid pair
w in any coset of deficiency d. That coset is reachable for the adjusted
target because w itself reaches it; its coefficient/pair fiber has size
F*q^d. The proposed algorithm gives this lift unconditional probability

```text
(1/W) * [q^d/(C*Z)] * [1/(F*q^d)] = 1/(W*C*F*Z).
```

This constant is independent of target, outside values, coset, deficiency,
and w. Inconsistent target-coset combinations contribute no valid lifts
and are simply rejected. Zero-norm rejection leaves EXACT uniformity on
ALL valid lifts, not only good ones. It is essential to sample exactly one
point uniformly in each reached affine fiber, including deficient M.

**Pushforward.** The nonzero norm fiber over any value has q+1 elements:
the norm on F_(q^2)^* is x -> x^(q+1), surjective onto F_q^*, with kernel
size q+1. Multiplication by each h_i!=0 changes the target norm value but
not this cardinality. Every original full-support y with By=s therefore
has exactly (q+1)^t valid lifts, while z=y_O is uniquely determined.
Uniformity on all valid lifts therefore pushes to EXACT uniformity on Y_s.

**Success and caps.** Good cosets occupy at least 1-delta1 of all cosets;
they have deficiency zero and valid-fiber fraction at least 1-eta. Their
contribution alone gives success >=alpha/Z. Other cosets can only increase
success. More precisely, it equals |Y_s|(q+1)^t/(W*C*F*Z).
Repeating whole independent trials preserves exactness. A cap K adds
UNKNOWN with probability at most (1-alpha/Z)^K without biasing the
conditional output. No arbitrary-accuracy approximation parameter is needed
for this exact conditional law; failure probability remains controllable.

**Earlier approximate result.** The previously reviewed good-coset-only
algorithm still satisfies TV<=beta/(alpha+beta), beta=delta1+delta0.
That proof was sound, but it is now the weaker alternative. The exact
proposal must NOT retain its G admission filter.

## Outside Values And Mixtures Over h

Different outside assignments can have different numbers of valid lifts.
Uniformly choosing z before whole-trial rejection automatically supplies the
required weighting after acceptance; forcing z uniform AFTER independently
solving each adjusted target would not. A punctured coordinate belongs in
O with h=0 and must vary like every other outside coordinate. No norm-lift
factor is attached to O.

For each fixed admissible h, the exact pushforward is the SAME uniform law
on Y_s, even though T and its norm-lift multiplicity may change. Choosing h
once therefore preserves exactness. Redrawing h from pi each trial changes
accepted mixture weights to pi(h)*success_h, normalized, but every component
is still exactly that same uniform native law. Uniformity over h or over a
combined (h,z,u,v) space is neither required nor claimed. Fresh trials must
remain independent conditional on h; candidate-dependent selection not
covered by this rule needs a separate argument. For a uniform time bound,
use a common lower bound on alpha_h/Z_h.

## Exact Small-e Branch And Quantitative Scope

For a fixed column basis I, each free nonzero assignment determines exactly
one solution on I. Each native full-support solution has exactly one such
free assignment. Rejecting zeros on I is consequently exact-uniform,
independently of the efficiency argument.

The disjoint second basis J makes every row of B_I^(-1) B_J nonzero.
Condition on all free variables but one with a nonzero coefficient: the
dependent coordinate vanishes for at most one of its q-1 possible values.
Thus acceptance is at least 1-k/(q-1). With e<=63, k<=318 and q>=1019,
this is at least 350/509>1/2. Distance d(V)>k supplies such a second basis
for any chosen I; the executable correctly labels efficiency as unverified
for arbitrary matrices.

For e>=64 in the inherited complete-AG scope, q>=1019 and q^2>=44e,
the monotone real envelopes give

```text
delta0 <= q^(25-e/2) <= 1019^(-7),
delta1 <= (22e-1)q^(27-e/2) <= 1407*1019^(-5),
eta <= 1/2.
```

The middle envelope decreases with real e>=64; no false monotonicity of
the floor-dependent integer expression is used. Consequently, uniformly
through this covered range,

```text
exact sampler success >= (1-1407*1019^(-5)) / [2*(1+1019^(-7))]
                      > 0.4999999999993,
conditional native TV = 0.
```

These are theoretical bounds, not large-instance measurements. The fixed
q=1019 constant-success certificate stops at e=23599 under q^2>=44e.
This review makes no claim for unbounded e at fixed q. Within the covered
range, unlike the earlier approximate sampler, there is no residual
statistical error floor under ideal randomness.

## Exact Coins And Polynomial Cost

Use an integer mixture coin with denominator D=q^(2R)+q^k-1: choose a uniform
integer below D, taking the base branch on its first q^(2R) values. Each
remaining value can index one nonzero lambda, or lambda can be drawn
separately uniformly conditional on the incident branch. D has
O((k+r)log q) bits. Uniform integer generation by rejection from a bit string
uses fewer than two attempts on average, even if the incident branch is
exponentially rare.

Thin by drawing 2(r_lambda-R) uniform field elements and checking that all
are zero, or by the equivalent exact integer coin. This takes polynomial
work whether it passes or fails. DO NOT repeat until this rare thinning
passes with lambda or the branch fixed. DO NOT use floating-point coins:
for native parameters delta0 can be below machine precision near one, so
rounding 1/Z to one silently removes the correction needed for exactness.
If a sampled r_lambda<R, report an invalid premise; clipping the thinning
probability is not justified.

Computing c_lambda, U_lambda, its kernel, and a uniform affine solution are
polynomial finite-field operations. No enumeration of q^k lambda values or
q^d solutions is required. Per-trial work and randomness are polynomial in
the explicit matrix sizes and log q; alpha/Z bounded away from zero gives
polynomial expected total work. The inherited h/adapter costs remain paid
separately.

Universal R=0 is algebraically valid and gives Z=q^k, but generally only an
exponential-time exact fallback when Y_s is nonempty. Its success equals
the probability that fresh uniform pairs and nonzero outside values satisfy
the original target. It does not extend the fixed-prime efficiency scope.

## Counting Corollary

**The FPRAS corollary is sound:** for fixed admissible h with known normalizer
K=W*C*F*Z/(q+1)^t and a constant lower bound on whole-trial success P,
|Y_s|=K*P, so O(epsilon^(-2) log(1/delta)) independent whole trials and a
multiplicative Chernoff bound give relative error epsilon with failure
probability delta, using polynomial-bit rational arithmetic; this is
approximate counting, not exact counting, and batching draw-until-success
calls or silently changing h would require a different normalization.
For a strict worst-case polynomial-runtime FPRAS convention, cap the
geometric bit-rejection draws and preprocessing with part of the allowed
failure budget; their known success bounds make the extra cost polynomial.

## Implementation And Verification Boundary

Final bounded inspection of
[RankWeightedNormSampler](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/norm_sampling.py:173)
and EXACT_SAMPLER.md found no actionable defect in the reviewed exact-law
path. The class retains structural checks through its parent constructor,
but correctly overrides the approximate trial:

- offset_proposal uses integer randrange coins, uniform integer encoding
  of every nonzero lambda, the actual U_lambda rank/kernel, independent
  nullspace coefficients for a and b, and one thinning test. An observed
  violated rank promise raises an error rather than clipping a probability.
- one_trial draws all outside values anew. Its s-B_O(z-1) correction cancels
  the reused backend's outside values of one, producing s-B_O z as required.
  It calls case.prepare directly, not the approximate sampler's G-filtering
  wrapper. Full-rank systems with low-rank marginals are therefore retained.
- The rank-deficient fallback calls affine_solution on the actual adjusted
  system, rejects only inconsistency, then samples its entire kernel once.
  It restores outside values and verifies the original syndrome/full support.
- draw inherits the whole-trial retry loop by dynamic dispatch to this
  overridden one_trial. Rejection restarts outside values, branch and offsets.
  Output metadata distinguishes a declared positive R from the unconditional
  rank bound R=0; neither substitutes for a native source proof.

The approximate GlobalNormSampler remains a separate comparison algorithm;
its rank/admission filters have not leaked into the exact path.

Each trial is polynomial finite-field linear algebra with O(m+r) random
field elements. Checking mixed cancellation is polynomial. Verifying the
universal R promise by enumerating all row combinations is not a paid
polynomial preprocessing step; retain the native structural proof instead.
The existing adapter remains theoretical, and the backend supports primes
below 2^63 rather than arbitrary prime powers.

The proof assumes exact independent random draws. The public draw helpers
use seeded Python Random, so their executions are deterministic replay
controls, not an information-theoretic certification of their PRNG output.
This limitation is explicitly acknowledged in the parent proof. The
mathematical sampling theorem must not be interpreted as a guarantee for a
fixed seed or repeatedly reusing the same seed.

Earlier independent rerun: **19 focused tests passed, 9 deselected**, using the
existing flint 0.9.0 / pytest 9.1.1 environment, Python -B, and pytest with
its cache provider disabled. Selected tests include exhaustive small-fiber
counting, the weighted deficiency control, wrong-retry/frozen-outside
countercontrols, coset/admission invariance, the actual one-trial schedule,
and the systematic bijection. No source or cache files were written there.
Large parameter-bound tests and the main repository suite were not rerun.
Subsequent parent changes to the bounds early exit, iterable normalization,
and control reporting were inspected without rerunning the suite. The
uniform numerical envelopes were checked by decimal arithmetic, not native
matrices. These tests concern the earlier approximate implementation.

Final exact-class rerun: **14 tests passed in 0.19 seconds**, using the same
no-bytecode/no-pytest-cache setup and only test_rank_weighting.py. It checks
625-coset incidence weights for R=0 and R=1 with unequal restriction ranks,
actual kernel offsets, non-looping thinning, invalid promises, reachable
rank-zero retention, unreachable-target rejection, native verification,
success bounds, and polynomial-bit coin sizes. No large/main suite was run.
The inspected exact code's SHA-256 was
`b37fefd08971a9c66803ba5447332d29d04bb2caf49059baa9434a3aa299c531`;
this is a bounded snapshot review, not a guarantee for subsequent changes.

An additional independent, in-memory algebra control tested the EXACT
proposal with q=5, k=r=2, A=[I_2 | I_2], B=[I_2 | -I_2], h=1, nu=2, R=1.
Among 24 nonzero lambda values, eight have r_lambda=1 and sixteen have
r_lambda=2, so thinning is genuinely nontrivial. All incident density factors
equaled 1/Z for Z=49/25. All 625 cosets satisfied the incidence identity and
the q^d/fiber-size cancellation; their deficiency counts were 576,48,1 for
d=0,1,2. This checks the delicate variable-rank factors, not an implemented
exact sampler or a large native instance.

The parent's larger test reports, direct weighted-native-law count control,
recovered counts 205/52, and nine native 43-by-176 outputs are parent-reported
evidence, not independent reruns by this reviewer. The stated native replay
premise R=32 from d(V)>=93>deg(A)=64 and full-support h is consistent with
the restriction-injectivity argument; this review did not independently
reconstruct that fixture's source geometry. No new large input or native
distribution campaign was created here. Mathematical conclusions rest on
the structural promises and counting proof, not those finite controls.

**Changed files in this isolated directory:** SAMPLING_REVIEW.md and the
separate literature REVIEW.md. No parent files, main repository, Git, or UI
were edited. No novelty or human-specialist certification is implied.
