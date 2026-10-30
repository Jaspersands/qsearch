# Exact Uniform Sampling By Kernel-Witness Size Biasing

27 October 2026. Scoped proof and exact implementation independently
AI-reviewed; no flaw found. See sibling
affine-pair-avoidance-review-2026-10-27/SAMPLING_REVIEW.md. Parent read the
report and closed the reviewer. This is not human or novelty certification.
This supersedes the approximation-only conclusion of RESULT.md. That
earlier argument and implementation remain useful countercontrols.

## The Additional Step

Keep the native relation, odd field, verified mixed annihilator, A_T
full-row-rank, and restriction-rank promise from RESULT.md. Allow R=0,
which is an unconditional but potentially inefficient choice. Write

    r_lambda = rank(A_T diag(h_T*(B_T^t lambda))),
    delta0 = (q^k-1)/q^(2R),      Z = 1+delta0.

For EVERY lambda!=0, require r_lambda>=R. This must be proved, not
estimated from a random list of lambda. The complete-AG proof supplies
such an R; the generic executable does not verify that upstream promise.

Each complete independent trial draws outside coordinates uniformly
nonzero and uses the following OFFSET proposal, which can reject:

1. With probability1/Z, draw a,b uniformly in F_q^T.
2. Otherwise, choose lambda uniformly from F_q^k minus0. Compute
   U_lambda=A_T diag(h_T*(B_T^t lambda)) and its rank r_lambda.
   With probability q^(-2(r_lambda-R)), draw a,b independently uniformly
   from ker(U_lambda). Otherwise reject the entire trial.
3. Form M and solve the adjusted affine syndrome. M MAY be rank deficient.
   Reject if the target is unreachable. Otherwise take ONE uniform point
   in its FULL affine solution space and form the norm output.
4. Reject the entire trial if a norm is zero. Verify original B y=s and
   emit only a full-support word.

Do not loop inside the rare second branch until it succeeds. Do not
discard rank-deficient systems or retain only rank2 coordinate marginals.
All failures restart outside values, the mixture branch and offsets.

## Exact Law

Let C be an S-coset, S=im(A_T^t) direct_sum im(A_T^t). There are
N=q^(2t-2r) such cosets. The mixed identity implies S is contained in
ker(U_lambda) direct_sum ker(U_lambda), and M is constant on C.

For a fixed nonzero lambda, its mixture weight is q^(-2R)/Z. Conditioning
both offsets to ker(U_lambda) multiplies their ambient density by
q^(2r_lambda). Thinning multiplies it by q^(-2(r_lambda-R)). These three
factors multiply to1/Z on M^t lambda=0, and zero elsewhere. Adding the
base branch, the accepted OFFSET proposal has UNNORMALIZED coset mass

    [1 + #{lambda!=0 : M^t lambda=0}]/(Z*N)
        = q^d/(Z*N),       d=k-rank(M).                    (E1)

The missing mass is rejection, not an uncharged conditional sampler.
Reachable targets have exactly q^(2r-k+d) solutions in C. Dividing(E1)
by that cardinality cancels the deficiency factor. Every produced pair
(u,v) satisfying the adjusted syndrome has the same unnormalized mass

    q^(k-2t)/Z.

After including outside values and rejecting zero norms, every valid
native y has exactly(q+1)^t equally weighted lifts. Thus the emitted
word is EXACT UNIFORM on the ORIGINAL Y_s, conditional on success.
This holds for every syndrome and every fixed admissible h. Mixtures over
admissible h and independent capped repetitions preserve exact uniformity.

This is not a quantum algorithm, a hardness result, or a claim of novelty.
It is a constructive correction to the rejection schedule, not an
assumption of efficient sampling from rank-deficient cosets.

## Cost And The Complete-AG Range

The mixture coin is a uniform integer in a range of size

    q^(2R)+q^k-1.

The first q^(2R) outcomes select the base branch; all others select the
incident branch. Uniform nonzero lambda, uniform nullspace coefficients,
and the thinning coin all use polynomially many random bits and field
operations. A tiny event probability does NOT require a long wait: draw
the coin once and reject on failure. No rank-deficiency stratum is found
by ambient rejection or exhaustive enumeration.

For the good cosets counted in RESULT.md, each target has at least a
1-eta fraction of nonzero norm outputs. By(E1), whole-trial success is
at least

    alpha_exact = (1-delta1)(1-eta)/(1+delta0).              (E2)

Use this bound only when delta1<1 and eta<1. With both at most1/2 and
delta0 bounded, expected trial count is constant. The q>=1019, e>=64,
q^2>=44e complete-AG range satisfies it using the previously proved
R=3e-floor(e/4)-11 and t<=22e-1. The e<64 systematic branch was already
exact uniform. Therefore the ENTIRE previously covered complete-AG
search range has an expected-polynomial EXACT classical uniform sampler,
with the same paid theoretical matrix-only adapter and h construction.

A finite cap L fails with probability at most(1-alpha_exact)^L; conditional
on success the law is exact, not approximately uniform. Increasing L
reduces failure, not sampling bias. For R=0, Z=q^k and the algorithm is
still exact but need not be efficient. Fixed q and e->infinity remain
unresolved because the nonzero-norm acceptance bound becomes vacuous.

## Required Adversarial Checks

- Every conditional offset sampler must use the actual U_lambda and its
  exact rank; a rank below the promised R invalidates the input contract.
- The incident branch must use UNIFORM nonzero lambda, not a guessed
  distribution on low-rank combinations.
- Omitting thinning biases cases with unequal r_lambda.
- Keeping only full-rank M removes exactly the fibers(E1) was intended to
  restore. Reachable deficient systems must use their larger nullspaces.
- Zero norms and unreachable syndromes reject the WHOLE trial.
- Native relation, nonzero conditions, all outside values and all norm
  multiplicities are retained. No uniformity on a restricted chart is
  silently upgraded to uniformity on Y_s.

Exhaustive small controls are finite checks of these equalities, not a
substitute for them. The generic executable accepts a declared R promise;
only R=0 is unconditional without a separate proof. Native higher-level
matrix-only source construction remains unimplemented.

## Counting Corollary

Fix one admissible h. The exact one-trial success probability is

    P_success = |Y_s| (q+1)^t / [(q-1)^o q^(2t-k) Z].      (E3)

All factors except |Y_s| are public and have polynomial bit descriptions.
When(E2) is a constant lower bound, independent success indicators estimate
|Y_s| to relative error epsilon with failure probability delta using
O(epsilon^(-2) log(1/delta)) trials (or include the inverse success lower
bound outside the constant regime). This is a randomized multiplicative
approximation to the count, NOT exact counting. The h construction and
native structural promises are still charged. No new counting experiment
or FPRAS implementation is needed to establish this elementary corollary;
the exact finite controls verify(E3) against enumerated native counts.
For a worst-case polynomial-runtime FPRAS convention, cap random-bit
rejection and preprocessing with an allocated part of the failure budget.
Known success bounds make this overhead polynomial. Count WHOLE trials,
not draw-until-success calls, and keep the h-dependent normalizer fixed.
