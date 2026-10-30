# Direct Scalar Flats For The Mersenne Predicate

2026-10-30. Constructive classical attack on the unchanged explicit relation.
This extends the existing `RECIPROCAL_TRACE_FLATS.md` construction; it is not
a new quantum mechanism or a claimed novel general theorem. Lovelace
independently checked the local algebra and root-count proof without finding
an error; Raman separately checked them during the priority audit. These are
automated reviews, not human peer review or formal verification.

## 1. Exact Task And Construction

Keep the input in `MERSENNE_RECIPROCAL_RESEARCH_TARGET.md`: binary field
F_q, q=2^n, d=2^s-1 coprime to q-1, arbitrary distinct supplied alpha_i,
arbitrary supplied target bits b_i, and the ORIGINAL equations

    sum_i alpha_i^j*x_i=0, 0<=j<K;
    Tr(inv0(x_i)^d)=b_i, with inv0(0)=0.

The canonical regime is prime n>=17, s=floor((n-3)/4), N=n^2,
K=(N-1)/8. The following local construction also works for the broader
coprime parameters. It neither changes H by a coordinate power nor uses
a planted witness. The implementation uses the strict tagged instance
validator and its checked backend field representation; a different valid
modulus is not silently reinterpreted as that representation.

Choose an ell-dimensional binary subspace V, M=2^ell<n, and draw a
uniform a in F_q. Reject a in V. For the M nonzero z in a+V solve

    Tr(mu*z^(-d))=b

as binary LINEAR equations in the n bits of mu. If inconsistent, try
another translation within a fixed cap. When b=1 every solution is nonzero.
When b=0 the nullspace has dimension at least n-M>0, so choose an explicit
nonzero solution instead of accepting zero or using an unbounded retry.
Let

    lambda=mu^(d^(-1) mod(q-1)).

Then the direct affine flat (a+V)/lambda is accepted, because

    Tr(inv0(z/lambda)^d)=Tr(lambda^d*z^(-d))=b.

Multiplication by nonzero lambda preserves its binary dimension. Every
point is checked with the original predicate. In particular, using mu
itself as the scaling factor would be wrong when d!=1.

The construction gives a direct x-flat, not an affine flat in a chosen
quadratic lifting of the predicate. The existing lifted-flat dimension
bounds therefore do not rule out this attack. All these flats avoid zero;
that restriction is legal for finding a witness but must not be confused
with sampling every accepted local root when b=0.

## 2. Paid Local Success Guarantee

The M trace equations are independent precisely when the field elements
(a+v)^(-d), v in V, are binary independent, by nondegeneracy of the trace
pairing. A failure gives some nonempty subset S of V with

    sum_(v in S) (a+v)^(-d)=0.

As a rational function of a, this sum is NONZERO: it has an uncancelled
pole of order d at every distinct v in S. On clearing the denominator,
its numerator has degree at most d*(|S|-1). Thus it has at most that many
roots outside S. A union bound, also discarding the M origins in V, gives

    Pr[bad translation] <= min(1, B/q),
    B=M+d*((M-2)*2^(M-1)+1).

This is a proof bound, not an instruction to enumerate subsets S. The
algorithm enumerates ONLY the M points in the sampled flat and performs
binary elimination. Each field power costs polynomial work in n, including
the inverse exponent d^(-1), which has O(n) bits. A fixed translation cap
makes all outcomes finite; a local abort does not assert unsatisfiability.
The implementation draws exactly n bits per translation; origins in V
consume a trial. Each free coefficient of mu consumes one further bit,
without a `randrange` rejection loop. At most n*(L+1) requested random
bits per coordinate are used. Analytic probability bounds assume independent
uniform bits; seeded PRNG executions are reproducible controls, not proofs
of those probabilities.
For independent translations the probability of exhausting L trials is
at most min(1,B/q)^L. For N local constructions a union bound gives N
times that quantity, clipped at one. No global-rank guarantee follows.

For the conservative choice M<=n/2 in the canonical family, the bound is
O(n*2^(-n/4)). The useful local dimension is still only Theta(log n).

## 3. Global Solve And Limits

For every coordinate construct

    x_i=o_i+sum_j u_ij*v_ij, u_ij in F_2.

Substituting these expressions into the ORIGINAL field parity equations
gives nK binary linear equations in Nell variables. Solve that system,
decode its x coordinates, and verify all original syndromes and target
bits. A second verifier uses polynomial-basis integer multiplication,
exponentiation and trace, independently of FLINT and the source predicate.

Full row rank is sufficient for every affine right-hand side; it is
checked, not assumed. If inconsistent, only THIS product of flats is ruled
out. No global native unsatisfiability, hardness, or asymptotic separation
is inferred from that result. One trial can also succeed without full
row rank. A verified witness is not a uniform native sampler.

At the two predeclared canonical sizes:

| n | s | ell | Binary variables | Binary equations | Local failure bound |
|---|---|---|---|---|---|
|17|3|3|867|612|5391/131072|
|31|7|4|3844|3720|58261647/2147483648|

At n61, ell5 gives only18605 variables for28365 equations. Asymptotically
N*Theta(log n)<nK. This prevents a general full-row-rank guarantee from
THIS dimension alone, not all classical solvers or specially consistent
lower-rank restrictions. Changing the exponent or selecting a new problem
to hide a successful finite attack is not justified.

## 4. Fixed Experiments And Replay

The inputs and seeds were chosen before execution, without screening:

- n17, s3, points0..288, K36, all-one targets, ell3, seed17030.
- The same n17 points/checks, targets popcount(i) mod2, ell3, seed17031.
- n31, s7, points0..960, K120, all-one targets, ell4, seed31030.

Every local translation has cap32. The experiment is one global product
flat per input, not a success-conditioned sweep. Retain failures and exact
input/modulus/witness certificates. Report all ranks and local attempt
counts. The larger-size comparison above is a count, not an executed run.

Implementation: `theorems/mersenne_scalar_flats.py`.
Tests: `tests/test_mersenne_scalar_flats.py`.
Live artifact: `research/classical_baselines/mersenne_scalar_flats.json`.

    python -m theorems.mersenne_scalar_flats --output research/classical_baselines/mersenne_scalar_flats.json
    python -m pytest -q tests/test_mersenne_scalar_flats.py -W error

All three fixed executions returned independently verified native witnesses:

| Input | Observed parity rank | Requested random bits | Local trials |
|---|---|---|---|
|n17 all-one|612/612|7515|289|
|n17 popcount parity|612/612|7514|289|
|n31 all-one|3720/3720|44206|961|

Every coordinate succeeded at its first translation. No global restart,
seed search, planted witness or input change was used. The JSON retains the
complete witnesses and checked field representations. These specific native
SEARCH fixtures therefore cannot be used as evidence of classical difficulty.

Passing these finite controls does not establish the missing global rank
theorem or a uniform sampler. The asymptotic family remains unresolved.
The independent priority audit recommends retaining it as a test case,
not treating further receiver implementation or failed classical attacks
as a leading route to a major new quantum algorithm.
