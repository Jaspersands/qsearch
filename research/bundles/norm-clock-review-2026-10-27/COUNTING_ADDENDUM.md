# Counting Addendum: Deterministic FPTAS Under The Square Gap

27 October 2026. Independent bounded proof audit of the proposed counting
corollary. **PASS:** the character grouping, accuracy threshold, running
time uniformly in q, and stated AG square-gap argument are correct.
No counterexample to the promised theorem was found. This supplies the
additional arbitrary-epsilon argument left open in REVIEW.md.

## Contract And Accuracy

Let q be a prime power, B an explicit full-row-rank k-by-m matrix over
an effectively represented F_q, s in F_q^k, and k >= 1. Promise a lower
bound d on the minimum nonzero rowspace weight satisfying

    (q-1)^d >= q^(2k).

Arithmetic, equality tests, and canonical element enumeration in the
supplied field representation must have deterministic polynomial bit
cost. No distance-computation oracle or free field-construction oracle
is assumed. This counting theorem does not require q odd, although the
source norm construction does. For q=2 the gap is impossible when k>=1.
For k=0, return the trivial exact count (q-1)^m separately; the proposed
threshold 1/(q^k-1) is undefined in that case.

Write Q=q^k and H=(q-1)^m/Q. The Fourier bound gives

    N_s = H(1+theta_s),
    |theta_s| <= a <= (Q-1)/Q^2 < 1/Q < 1.

In particular EVERY syndrome has N_s>0, so relative error is defined.
The correct conversion, relative to the true count, is

    |H-N_s|/N_s <= a/(1-a) < 1/(Q-1).

Thus returning H whenever epsilon >= 1/(Q-1) is valid, including equality
at the threshold. H is an exact rational output, not a rounded integer.
The remaining branch returns the exact integer N_s and has zero error.

## Projective Formula

For any fixed nontrivial additive character chi of F_q, orthogonality
gives the unnormalized expansion

    Q N_s = sum_(lambda in F_q^k)
              chi(-lambda.s) (-1)^wt(lambda B)
              (q-1)^(m-wt(lambda B)).

For a projective representative lambda != 0, every nonzero scalar
multiple has the same weight w. Its character sum is

    sum_(c in F_q^*) chi(-c lambda.s)
      = q-1  if lambda.s = 0,
      = -1   otherwise.

When lambda.s != 0, multiplication by that element permutes F_q^*, so
the identity holds over extension fields as well as prime fields.
The test is equality to zero IN F_q, not zero absolute trace or
chi(lambda.s)=1. Either alternative test would be wrong in general.

Separating lambda=0 therefore proves exactly

    N_s = [(q-1)^m + sum_projective_lines
            c_lambda (-1)^w (q-1)^(m-w)] / Q,
    c_lambda = q-1 if lambda.s=0, and -1 otherwise.

The expression is independent of the chosen representatives. The final
numerator is a nonnegative integer divisible by Q. Its summands may be
negative; signed exact arithmetic is required. No character values,
complex arithmetic, or numerical approximation are needed to execute it.

## Uniform Bit Complexity

In the exact branch epsilon < 1/(Q-1), so the number of lines is

    L = (Q-1)/(q-1) < 1/((q-1) epsilon) <= 1/epsilon.

Enumerate each line once by putting its first nonzero coordinate equal
to 1, all preceding coordinates equal to 0, and enumerating all suffixes.
This produces sum_(j=0)^(k-1) q^j = L representatives without requiring
a precomputed field-element table. Each representative needs O(km)
field operations to obtain lambda B, its weight, and lambda.s. Streaming
the representatives avoids space proportional to L.

For epsilon=u/v>0 supplied as binary integers, compare u(Q-1) with v
exactly. Q and (q-1)^m have O((m+k) log q) bits and are computable by
integer exponentiation in polynomial bit time. Return H as the numerator
and denominator, optionally reducing by a gcd; no decimal precision
choice is necessary. In the exact branch compute powers (q-1)^(m-w)
on demand or precompute them for exponents 0 through m.

An absolute bound on every partial numerator sum is

    (q-1)^m + L(q-1)(q-1)^m = Q(q-1)^m.

Hence even intermediate signed sums have only O((m+k) log q) bits.
Computing the terms and performing the final exact division have
polynomial bit cost, not unit-cost large-integer cost. A straightforward
implementation has time

    (1+1/epsilon) * poly(k, m, log q, bits(epsilon), field_encoding_size)

and polynomial space, with polynomial exponents independent of q.
Full-rank verification by elimination is also within this bound.
An implementation that constructs F_q from q alone must separately pay
and justify that construction; the usual supplied effective field
encoding suffices. Astronomical exact-branch runtimes do not contradict
the FPTAS definition, which is polynomial in 1/epsilon, not log(1/epsilon).

## AG Square Gap

Use the ORIGINAL promised parameters k=5e+3, d>=12e-3, e>=8, q>=1019.
Set F(e)=(q-1)^(12e-3)/q^(10e+6). At e=8, Bernoulli's inequality gives

    F(8) = q^7 (1-1/q)^93
         >= q^7 (1-93/q) = q^6(q-93) > 1.

For every increment of e,

    F(e+1)/F(e) = q^2 (1-1/q)^12
                >= q^2 (1-12/q) = q(q-12) > 1.

Thus F(e)>1 for every integer e>=8, which is stronger than the required
weak square gap. All exponents and inequality directions check out.
There is no need for q^2>=44e or for any auxiliary matrix, annihilator,
norm sampler, or geometric adapter to run this counting algorithm on B.

Inferring e from k (and checking m=22e when that is the native format)
only checks parameter consistency. It does not certify the AG provenance
or its distance theorem. Those remain promises; they are not established
for an arbitrary matrix by matching dimensions or checking full rank.
The algorithm does not need to compute the minimum distance.

## Scope And Boundary Example

This is a deterministic FPTAS for multiplicative approximate counting on
the promised class, for every syndrome and every positive rational
epsilon. It is not a claim of polynomial-time exact counting in the
ordinary input length, nor a certification of historical novelty.
It removes this approximate-counting task as a hardness-based candidate
for superpolynomial quantum advantage at inverse-polynomial precision;
it does not rule out better polynomial or precision dependence.

No search or sampling reduction follows from this result alone: the
conditional counting calls required by self-reduction need not retain
the distance/square-gap promise. For example, over F_3 take
B=[1 1 1 1] and s=0. Here k=1, d=4 and (q-1)^d=16>=9=q^(2k);
there are six full-support solutions. Fixing the nonzero prefix (1,1,1)
leaves B'=[1], residual syndrome 0, and no full-support completion.
Now d'=1 and 2<9, so the square gap is lost. Applying the promised
main-term branch to this unpromised instance at epsilon=1/2 would return
2/3 instead of zero. This is a counterexample to dropping the promise,
not to the FPTAS. Exact projective counting remains correct there, but
the proposed approximation/runtime guarantee cannot simply be imported.

Only this addendum was written. No implementation, experimental
controls, parent edits, Git/UI changes, or external contact were made.
