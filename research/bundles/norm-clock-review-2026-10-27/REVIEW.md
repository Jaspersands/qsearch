# Focused Audit: Rank-Weighted Norm Trial Clock

27 October 2026. Independent mathematical audit, including the proposed
ideal normalized size-biased oracle. No counterexample to the scoped
acceptance bound was found. No experiments, Git/UI actions, external
contact, or changes outside this new directory were used.

## Verdict And Required Qualification

**PASS for the specified fresh whole-trial family, including its ideal
normalized version.** The matrix inequality, exact acceptance identity,
uniform auxiliary-choice bound, and fixed-field AG decay are valid.

One wording correction: expected *completed* trials are at least `1/U`
for a policy that continues until success and succeeds almost surely
(infinite expectation is allowed). This is not true for a capped or
abandoning policy. For any such policy the correct statement is
`Pr(success) <= U E[completed trials]`; in particular an L-trial cap has
success probability at most `L U`. Details below.

The conclusion concerns this proposal family, not every algorithm using
norms, every classical search algorithm, or quantum advantage.

## Algebra And Ideal Normalization

Use odd q, k >= 1, full-row-rank native B, a genuine quadratic field norm,
T = support(h), t = |T|, and r = rank(A_T), with A_T represented by r
independent rows. The verified mixed annihilator gives, for every lambda,

    U_lambda = A_T diag(h_T * (B_T^t lambda)),
    U_lambda A_T^t = 0.

Thus im(A_T^t), of dimension r, lies in ker(U_lambda). Independently,
U_lambda has r rows. Hence

    r_lambda <= min(r, t-r),     2 r_lambda <= t,

and any valid common lower bound R satisfies 2R <= t. This is a dimension
argument, not a generic-rank or auxiliary-divisor assumption. Dependent
auxiliary rows can first be removed without changing the represented
subspace. Sparse h simply reduces t and does not escape the inequality.

Let C range uniformly over the N = q^(2t-2r) cosets of
S = im(A_T^t) direct_sum im(A_T^t), and let D(C) = k-rank(M_C).
The mixed identity makes M_C well defined on a coset. For uniform
ambient offsets, its two transposed blocks at lambda are nonzero scalar
multiples of U_lambda a and U_lambda b. They vanish independently with
probability q^(-2 r_lambda). Coset invariance therefore gives exactly

    Z* = E_C q^D(C) = 1 + sum_(lambda != 0) q^(-2 r_lambda).

There is no missing factor q^k, number of cosets, or projective factor
q-1: the sum is over all nonzero coefficient vectors, not lines.
Consequently

    1 + (q^k-1) q^(-t) <= Z* <= 1 + (q^k-1) q^(-2R) = Z.

For the ideal proposal q^D(C)/(N Z*), a reachable coset contains exactly
q^(2r-k+D(C)) affine solutions. One uniform solution therefore gives
each satisfying pair the same unnormalized mass q^(k-2t)/Z*.
Unreachable cosets remain failures; conditioning them away for free would
be a different oracle. The explicit thinned proposal has the identical
calculation with Z instead of Z*: its offset-stage acceptance is Z*/Z.

Uniform fresh nonzero outside coordinates contribute (q-1)^(-(m-t)).
Every native full-support y has exactly (q+1)^t norm lifts, since every
h_i on T is nonzero. Thus, with Z0 equal to Z or Z*, respectively,

    P_s = N_s (q+1)^t / [(q-1)^(m-t) q^(2t-k) Z0].

The Fourier expansion is

    q^k N_s/(q-1)^m
      = sum_lambda chi(-lambda.s) (-1/(q-1))^wt(B^t lambda).

Full row rank ensures every nonzero lambda gives weight at least d.
Therefore theta_s = q^k N_s/(q-1)^m - 1 is real, |theta_s| <= a,
where a = (q^k-1)/(q-1)^d. Substitution proves the claimed identity

    P_s = (1+theta_s) rho^t/Z0,     rho = 1-q^(-2).

This calculation needs neither rank(M)=k nor rank-two coordinate
marginals. Discarding reachable deficient systems would change it.

## Uniform Bound And Adaptive Clock

Both normalizers satisfy Z0 >= 1+(q^k-1)q^(-t). If t >= k, use Z0 >= 1.
If t < k, use Z0 >= (1-q^(-k))q^(k-t) and q rho > 1. In both cases,

    P_s <= U := (1+a) rho^k/(1-q^(-k)).

The ideal oracle therefore cannot remove this obstruction merely by
improving rank-dependent lambda weights. The bound is pointwise in all
admissible A,h and every original syndrome. No union bound over the
number of auxiliary choices is necessary.

A policy may choose A,h, R and other admissible parameters using the
target and all preceding history, before the next trial's fresh draws.
Conditional on that history and choice, it must still draw outside values
uniformly nonzero, use the specified size-biased coset proposal, take one
uniform full affine solution if reachable, and reject the whole trial on
any zero norm. Then conditional success is at most u = min(1,U).
Consequently

    Pr(success by L) <= 1-(1-u)^L <= L u <= L U.

For indefinite repetition, Pr(T > L) >= (1-u)^L, hence E[T] >= 1/u.
For a stopped policy with C completed trials, summing the conditional
success indicators instead gives Pr(success) <= u E[C]. A one-trial
cap with u < 1 is already a counterexample to the unqualified assertion
E[C] >= 1/U. Ignoring preprocessing and granting unit-cost ideal proposal
draws only strengthens this trial-count lower bound; emitting a witness
from preprocessing is outside its scope.

## AG Scaling And Counting Caveat

For the ORIGINAL parameters k = 5e+3 and d >= 12e-3,

    a < q^3 (q-1)^3 [q^5/(q-1)^12]^e.

At every fixed odd q >= 1019 the bracket is strictly below one. Its
negative log is 12 log(q-1)-5 log(q), approximately 48.4743 at q=1019.
Thus a decays exponentially, uniformly in s. For any growing sequence
of inputs satisfying these promises,

    E[T] >= (1-q^(-k))/(1+a) * rho^(-k) = exp(Omega(k))

at FIXED q. The exponential rate is -log(rho), approximately 1/q^2,
not a q-independent constant. This does not contradict the earlier
large-field range q^2 >= 44e and does not prove an exponential lower
bound when q grows with e. Existence/construction of a promised AG
sequence and the matrix-only adapter were not re-audited here.

For a < 1, the deterministic main term H = (q-1)^m/q^k already satisfies
|H-N_s|/N_s <= a/(1-a). The earlier sampling-based counting corollary
can remain correct, but is not evidence of counting hardness or a novelty
certificate. The main term alone only supplies this accuracy; do not call
it an arbitrary-epsilon FPRAS without an additional argument.

Root counts do not supply the needed conditional counts for search.
Fixing j coordinates punctures B; its row distance can fall to d-j,
and even while rank k survives the Fourier error bound deteriorates to
(q^k-1)/(q-1)^(d-j). Eventually rank/reachability must also be reconsidered.

Explicit boundary example: over F_3, let B = [1 1 1 1], s = 0.
There are six full-support solutions, with root main term 16/3 and
a = 1/8. The nonzero prefix (1,1,1) forces the last coordinate to zero,
so its completion count is zero, not the residual main term 2/3.
More strongly, B = [1 ... 1] of length m = 3n+1 has d = m and root
a = 2^(-3n), yet the all-ones prefix of length 3n still has zero
completions. Arbitrarily accurate root estimates do not fix this issue.

Correlated repair, different proposers, conditioning on reachable or
nonzero solutions, nonuniform search, and quantum methods remain outside
the falsifier. No counterexample to the restricted theorem was found.

## Sources And Verification Scope

Read the requested
[EXACT_SAMPLER.md](/Users/jaspersands/Developer/qsearch-research-work/norm-sampling-2026-10-27/EXACT_SAMPLER.md)
and
[ALL_INPUT_SCOPE.md](/Users/jaspersands/Developer/qsearch-research-work/two-component-norm-2026-10-27/ALL_INPUT_SCOPE.md),
plus their supporting RESULT.md definitions. The conclusions above are
independently checked algebraic deductions, not inferred from earlier
review verdicts. Parent proof/controls were deliberately not duplicated.
