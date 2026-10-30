# Classical Sampling From The Same Native Full-Support Fiber

27 October 2026. Scoped deduction independently AI-reviewed, including
the stronger exact sampler. No quantum advantage, novelty certification, or fixed-prime
asymptotic algorithm is claimed.

UPDATE: EXACT_SAMPLER.md supplies a stronger rank-size-biased proposal
that removes the statistical error. This note preserves the approximate
sampler and its bias countercontrols; it is no longer the final scope.

## Scientific Decision

The preceding norm attack only claimed search. Its implementation is NOT
a uniform sampler: it freezes h-zero coordinates and retries within a
selected affine fiber. A different rejection schedule gives a classical
sampler with an explicit total-variation bound on the ORIGINAL witness set

    Y_s = {y in (F_q^*)^m : B y = s}.

This removes a remaining sampling distinction in the already covered
large-field range. It does not solve the fixed-q, unbounded-size problem.
The earlier complete-AG matrix-only adapter remains a paid theoretical
construction, not a native implementation.

## Input And Structural Premises

Use the preceding bundle's verified odd-field data B, A, h and nonsquare nu.
B has k independent rows, A has r independent rows, T=support(h), t=|T|,
and O is its complement. Require A_T to have independent rows, nonzero
columns, and the mixed identity B*(h*A_u*A_v)=0 for every u,v. Suppose

    rank(A_support(h*c)) >= R for all nonzero c in rowspan(B).

The universal R premise is a mathematical input promise, not inferred
from sampled codewords. The executable checks the mixed identity and
local ranks, not the universal premise or an AG representation.

Set

    delta0 = (q^k-1) q^(-2R),
    delta1 = t q^2 delta0,
    eta = t/q^2.

Assume delta1<1 and eta<1. The useful constant-success regime has both
at most 1/2. No change of input relation, secret geometry, uncharged
oracle or supplied witness is allowed.

## Algorithm: One Kernel Sample Per Independent Trial

Each complete trial independently:

1. Draw every y_i for i in O uniformly from F_q^*. This includes any
   punctured coordinate used by the matrix-only adapter. Never fix it to1.
2. Draw a,b uniformly in F_q^T. Form the same k-by-2r syndrome matrix M
   as in the preceding norm construction.
3. Reject unless M has rank k and every two-component coordinate map on
   ker(M) has rank2. This admission condition is independent of s.
4. Solve the adjusted affine system for the original s and the newly
   chosen outside coordinates. Draw ONE uniform kernel coefficient vector.
5. Form y_T=h_T*(u^2-nu*v^2), verify original B y=s, and reject the WHOLE
   trial if a coordinate is zero. Otherwise emit y.

Repeated independent trials have success probability at least

    alpha = (1-delta1)(1-eta).

A cap L has failure probability at most (1-alpha)^L. Conditional on
success, the cap does not change the output law. Exhaustion means UNKNOWN,
not infeasibility. The theoretical random draws are exact; seeded Python
replays are reproducibility controls, not a proof about pseudorandomness.

## Why It Samples Nearly Uniformly

Let S=im(A_T^t) direct_sum im(A_T^t), and let

    Q(u,v) = B_T [h_T*(u^2-nu*v^2)].

The mixed identity makes Q zero on S and makes Q affine on every S-coset.
Its linear part M is unchanged when a,b are shifted inside that coset.
The good-coset event G (full rank and rank2 coordinate marginals) is
therefore also invariant. Every good coset has EXACTLY q^(2r-k) solutions
to every adjusted syndrome. Drawing uniform offsets, then a uniform
solution, consequently gives the uniform law on all solutions in good
cosets. This statement is about the pair (u,v), not merely coefficients.

For a uniformly chosen coset put d=k-rank(M). For each coefficient
lambda!=0, the two blocks of M^t lambda are independent uniform vectors
in a subspace of dimension at least R. Thus

    E[q^d-1] = sum_(lambda!=0) Pr[M^t lambda=0] <= delta0.   (1)

The previous offset lemma gives Pr[not G]<=delta1. Hence

    E[1_(not G) q^d] <= delta1+delta0.                    (2)

This weighted bound is essential. Simply conditioning a small ambient
bad probability on k equations and multiplying it by q^k loses the useful
guarantee. Equation(2) instead pays the actual excess fiber size q^d.

In each good coset and for each outside assignment, at least a fraction
1-eta of the q^(2r-k) solutions have every norm nonzero. In a bad coset,
the total number of solutions is either zero or q^(2r-k+d), regardless
of outside assignment. Normalize by the number of cosets times q^(2r-k)
and by the number of nonzero outside assignments. Good valid lifts have
mass >=alpha; bad valid lifts have mass <=beta=delta1+delta0.

The algorithm is EXACT uniform on the good valid lifts. The uniform law
on ALL valid lifts loses exactly its bad-lift fraction when conditioned
on G. Its total-variation distance from the algorithm is therefore at most

    epsilon = beta/(alpha+beta).                          (3)

Finally, u^2-nu*v^2 is the norm F_(q^2)->F_q. Each nonzero value has
exactly q+1 preimages, since the multiplicative norm has kernel size q+1.
Every original y in Y_s has exactly (q+1)^t lifts, including when O is
nonempty. Uniform valid lifts push forward to EXACT uniform on Y_s.
Data processing proves the bound(3) for the emitted native y.

The outside values must be redrawn in the SAME rejection loop. Repeated
kernel attempts inside one coset weight that coset incorrectly; freezing
outside coordinates restricts the target set. Neither shortcut is used.

## Complete-AG Consequence

For every promised complete AG input with g=5e+1, degG=10e+3, m=22e,
k=5e+3, odd q>=1019, e>=64, and q^2>=44e, use the prior paid matrix-only
construction after puncturing P0. Take A=ev L(8eP0). The accepted h
construction gives R>=3e-floor(e/4)-11 and t<=22e-1. Use these worst-case
values in(1)-(3). A_T has independent rows because |T|>8e, while a nonzero
section of L(8eP0) has at most8e zeros. No divisor-distribution assumption
is added. Random choice of an accepted h is a mixture of samplers each
within the same epsilon of the SAME native uniform law, so preserves it.

For 8<=e<64, use EXACT systematic rejection instead: choose a k-column
basis, draw all other coordinates uniformly nonzero, and solve for the
basis coordinates. A disjoint second basis exists from d(V)>k, so every
solved coordinate is a nonconstant affine form in at least one free
nonzero coordinate. Each vanishes with probability <=1/(q-1). Acceptance
is at least1-k/(q-1)>1/2. Every valid native y has one equally likely free
assignment, proving EXACT uniformity in this small-e branch.

Thus the prior search scope also has polynomial expected-time classical
sampling with an explicit small statistical error (exact for e<64).
This is NOT an arbitrary-accuracy FPAUS claim: the stated norm error floor
is not tunable by repeating samples. No exact-uniform norm sampler has
been proved. Fixed q and e->infinity are still outside the certificate.

## Resources, Attribution, And Falsifiers

Each trial uses polynomial finite-field linear algebra and O(m+r) random
field elements. The existing matrix-only adapter and h preprocessing are
charged separately. The executable backend is restricted to primes below
2^63; the mathematical statement uses ordinary finite-field arithmetic.
Norm cancellation with auxiliary codes is prior art, notably
[Ragavan--Shutty Section6.1](https://arxiv.org/html/2610.00502v1#S6.SS1).
The present counting/sampling deduction has not had a novelty audit.

Falsifiers: coset-dependent M; nonconstant good-fiber cardinality; failure
of(1); any native y with a different nonzero-norm lift count; a target-
dependent admission rule; or a sampling loop that does not redraw outside
values and offsets together. Exact distribution controls, not witness
success rates, are required. The same-input fixed-prime problem remains
open; generic pairwise independence is not an efficient resampling oracle.
