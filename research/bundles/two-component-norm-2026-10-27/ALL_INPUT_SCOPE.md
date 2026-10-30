# Stronger Scope: Pay Rank Loss Instead Of Assuming Generic Divisors

27 October 2026. Scoped independent AI adversarial review completed; see
REVIEW_RESPONSE.md. No human specialist or novelty certification.
This supersedes the NEED for the random-prime basepoint argument in
AG_SCOPE.md and MATRIX_ONLY_BRIDGE.md. Those stronger full-rank promises
remain sufficient, but they are not needed for the following bound.

## General Rank-Loss Version Of The Offset Lemma

Replace the full-rank-r restriction hypothesis of RESULT.md by

    rank(A_support(h*c)) >= R  for every nonzero c in rowspan(B).

For fixed nonzero coefficient lambda, put c=B^t lambda. Each block of
M^t lambda is uniform in a subspace of dimension
at least R. Its intersection with span(A_i) has at most q points, so
the probability of landing there is at most q^(1-R). Independence of
the two offset blocks remains exact. Provided A_i!=0 on T, the same
rowspace-intersection argument gives

    Pr[rank(M)<k OR some rho_i<2]
        <= min(1, |T|(q^k-1)q^(2-2R)).                     (S1)

No uniformity over the full F_q^r or unproved rank heuristic is used.

## Base Points Of An Arbitrary Complete Annihilator

Use the MATRIX_ONLY_BRIDGE puncture, so m'=22e-1, g=5e+1, d=10e+3,
k=5e+3, over ODD q. G is now ANY divisor of that degree satisfying the complete-code
promise and disjoint evaluation support, not a uniformly sampled prime.
The exact underlying divisor representative is irrelevant to this argument.

The complete annihilator corresponds, up to nonzero coordinate weights,
to L(J) of degree 6e-4. Riemann-Roch gives ell(J)>=e-4>1. Let F be
the full fixed/base divisor of its complete linear series and M=J-F.
Then ell(M)=ell(J), and M is base-point-free.

If M is nonspecial, Riemann-Roch gives

    ell(J)=ell(M)=deg(J)-deg(F)-g+1=e-4-deg(F).

Comparing with ell(J)>=e-4 forces deg(F)=0. Otherwise Clifford's theorem
gives deg(M)>=2ell(M)-2>=2e-10, hence

    deg(F)<=4e+6.                                         (S2)

This includes the trivial/canonical equality cases; ell(J)>1 excludes
the trivial zero-dimensional corner. There is no randomness or rational-
Picard distribution premise in (S2).

The actually computed mixed-annihilator space contains this complete
annihilator with the inverse nonzero column scaling explained in
MATRIX_ONLY_BRIDGE.md. Zero patterns are unchanged. Its identically zero
coordinate set therefore has size
b<=4e+6. The algorithm computes b directly from its nullspace basis.
For uniform h from that actual space, let w be the number of ADDITIONAL
zero coordinates outside these base positions. Then E[w]<=(22e-1)/q.
At e>=64, keep only h with

    w<=floor(e/4).

Markov bounds rejection by at most (22e-1)/(q(floor(e/4)+1))<88/q.
In particular this is less than 1/2 for q>=1019. The zero vector is
rejected by this same check at these parameters.

## A Uniform Restriction-Rank Lower Bound

For every nonzero c in the punctured V, wt(c)>=12e-4. A retained h thus
gives, with a=floor(e/4),

    |support(h*c)| >= 12e-4-(4e+6+a) = 8e-10-a.

The kernel of restricting A=ev L(8eP0) to a set S is L(8eP0-S), whose
degree is at most a+10. The elementary bound ell(D)<=max(0,deg(D)+1)
therefore gives

    rank(A_S)>=r-a-11 >= 3e-a-11 =: R.                    (S3)

This remains a valid bound for dependent evaluation columns. It neither
assumes MDS behaviour of the auxiliary code nor needs to list codewords.

Combining (S1)-(S3), random-offset failure is at most

    (22e-1) q^(27-e+2 floor(e/4))
        <= (22e-1) q^(27-e/2).                            (S4)

For all integer e>=64 and q>=1019, this is below 1/2. Use
floor(e/4)<=e/4 and the decreasing real envelope (22e-1)q^(27-e/2),
whose consecutive ratio is ((22e+21)/(22e-1))*q^(-1/2)<1.
The raw integer bound need not decrease, even over two steps; e67 and
e69 both have exponent -8 while the coefficient increases. No integer
monotonicity assumption is used in the guarantee.

## All-Input Classical Consequence

For e>=64, q>=1019 and q^2>=44e, the h, offset and kernel stages each
have constant success probability. With the paid matrix-only adapter,
this gives an EXPECTED-POLYNOMIAL classical solver for EVERY complete
AG input in this promised parameter range and EVERY original syndrome.
No source-distribution exception or full-cube-conditioning factor remains.
The original extra coordinate is restored as 1 and B,s are verified.

For 8<=e<64, the existing two-basis greedy method applies because
k=5e+3<=318<q-1. Two bases exist since d(V)>=12e-3>k. It completes
arbitrary syndromes without changing the original input.

Together these cover every integer e>=8 with q>=1019 and q^2>=44e
under the complete-code promise. At q=1019 the dyadic cutoff remains
16384 (integer cutoff23599). No matrix at that scale was built. This
does NOT prove polynomial search for e->infinity at fixed q, where the
norm-zero bound fails. It does NOT establish uniform witness sampling.

## Implementation Boundary And Falsifiers

The executable norm solver and geometry-assisted original-input replay
exist. The matrix-only bounded-degree section-ring adapter is a written
construction with exact small-curve controls, not a native implementation.
It remains a Gemini implementation task, with all ring/frame/ratio checks.

Break the all-input deduction by invalidating the base-divisor bound,
the complete-annihilator containment, the restriction kernel identification,
the rank-R offset bound, or the paid matrix-only adapter. Failure of a
random offset or finite control is not itself a counterexample to the
expected-time theorem; the explicit probabilities must be checked.

Clifford, Riemann-Roch, AG duality and the quadratic-annihilator principle
are standard prior tools. This is not an independently established novelty
claim or a Shor-level result. Its research value is removing another
classical-access/parameter loophole from this project's quantum candidates.
