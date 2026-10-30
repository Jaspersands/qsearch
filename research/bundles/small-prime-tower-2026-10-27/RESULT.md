# Smaller Prime, Same Native Problem, Stronger Classical Check

Status: exact source and native degree-eight code constructed; independent
agent review ACCEPTS the scoped source, complete code and fixed-p bound
transfer, with no required mathematical fixes. See
../small-prime-review-2026-10-27/REVIEW.md and VERIFICATION.md. This is an
independent agent check, not external peer review. No quantum circuit,
higher tower, hardness, novelty or speedup is claimed. The finite code is
classically easy. Do not admit it as an advantage candidate merely because
its Schur cube is full.

## Decision And Scientific Question

The highest-value open issue remains a polynomial classical algorithm for
the SAME explicit relation `Bz=s`, with every coordinate nonzero, on the
arbitrary-divisor-class AG family. A bounded independent literature audit
did not obtain a general polynomial extractor from affine Alon-Jaeger-Tarsi
existence. Its concrete low-dimension greedy extractor is now implemented
as a mandatory baseline. See ../ajt-extraction-review-2026-10-27/review.md.

The original fixed prime 100003 made all available examples nearly trivial
for rejection sampling. This pass changes the source to prime 1019 while
retaining its geometric and decoder conditions. The goal is a more decisive
eventual experiment, not optimization of a demonstration. No claim that 1019
is the smallest possible prime is made.

## Actual Source

Over F_1019 take the smooth projective model of

    y^2 = product_(a in A) (x-a),
    A = (63,66,86,98,105,107,188,554,570,578,673,773,866).

The eleven split x values are

    (0,468,568,571,614,634,696,882,926,942,965).

Every one of the 143 differences x-a is a NONZERO square. The certificate
contains their square roots and both y values. A bounded bitset beam search
found this configuration in 235285 intersection tests; its completeness and
smallest-prime status are UNKNOWN. Bounded searches at 503 and 719 failed;
that is not evidence of nonexistence there.

The old tower argument does not require consecutive branch points. Distinct
linear factors give 13 independent valuation classes over F_p(x); adjoining
y kills exactly their product, leaving Kummer rank 12 over the genus-six
base. Each x-a has divisor 2P_a-2O. Its local leading unit at infinity is 1:
with t=y/x^7, (x-a)t^2 tends to 1. Thus all these quadratic extensions are
unramified and split at the 22 listed finite points and O. The split rational
place excludes a constant-field extension. With S of size 23,

    (12-2)^2 - 4*(23+1) = 4 > 0.

[Schoof, Theorem 2.3](https://reneschoof.github.io/CurvesF2.pdf) therefore
gives an infinite S-split unramified pro-2 tower. Its construction is known
class-field theory, not a new algorithmic mechanism. The previously reviewed
output-polynomial source argument applies at this new FIXED odd prime;
normalization, exact order, RR, marked branches, and actual prime sampling
remain charged. No backend for arbitrary higher levels was implemented here.

## Actual Genus-41 Matrix

Adjoin w_i with w_i^2=(x-a_0)(x-a_i), i=1,2,3. This is an unramified
degree-eight cover of the base, hence genus 41. Above each listed x there
are 16 distinct rational points, giving 176 evaluation points D.

Let I be the pullback of base infinity. At x=6 choose the five points with
sign indices (0,3,5,9,14), in lexicographic product((1,-1), repeat=4) order
for (w_1,w_2,w_3,y); call their sum E. Set G=11I-E, of degree 83=2g+1.
These are actual points disjoint from D, not a random Picard class.
The extra fiber need only split in this degree-eight cover; several of its
13 branch differences are nonsquares, so it does NOT split in the entire
elementary Kummer extension. Also K~10I and L(I-E)=0, checked from the
complete pole-bound-one space: this G is not canonical-plus-effective-three.

The character masks are the eight even subsets of {0,1,2,3}, and their
complements in the 13 branch indices. The functions x^j sqrt(product_T(x-a))
with 2j+|T|<=11 give a COMPLETE 48-dimensional L(11I): the integral
character bases have no finite poles, and character projection separates
the infinity pole bounds. Five explicit evaluation constraints have rank
5. Their kernel supplies a complete 43-dimensional L(G), whose actual
evaluation matrix has

    k=43, m=176, rank(V^2)=126, rank(V^3)=176.

The denominator in the evaluator matters: a product of w_i includes extra
powers of x-a_0. The tests check all 16 radical-square identities at every
evaluation point and at the extra fiber. Complementary characters use y
divided by the low-character radical, not an independent square-root sign.

The full cube excludes the SAME-code cubic-annihilator construction on this
matrix. It excludes neither auxiliary-code attacks nor other classical
algorithms. Both systematic sampling and deterministic avoidance produce
checked full-support witnesses for this finite input.

## Bounds For An Actual Higher-Level Input

For every dyadic e>=8 in the new tower, a degree-(2g+1) divisor gives

    g=5e+1, d=10e+3, k=5e+3, m=22e, w=15e+6,
    delta >= m-d = 12e-3.

The reviewed unambiguous-decoder and verified-output reduction has

    E_dec <= (p^k-1)*p^w/(p-1)^m < p^9*(2/p^2)^e,
    alpha = (p^k-1)/(p-1)^delta,
    raw verified quantum success >= (1-E_dec)^2/(1+alpha).

The square on (1-E_dec) is intentional; the older unsquared raw-success
formula must not be reused. At e=8 the exact error upper bound is about
1.041906e-21. This is a CONDITIONAL theorem bound, not a quantum execution.
State preparation, reversible decoding, inverses, all failures and precision
remain charged. Single-symbol synthesis is polynomial in p, not log p.

The prime-class source bound also survives. Using
L=floor(sqrt(p))-1=30 and U=floor(sqrt(p))+2=33 gives

    B_e = 9^(5e+1)*(5e+1) / (p^(3e+9)*L^2),
    Pr(bad sampled degree-d prime) <= B_e * 2dp/(p-1) * (U^2/p)^g.

This uses [Cascudo-Cramer-Xing, Proposition 3.4](https://arxiv.org/html/1207.2936)
and the previously reviewed maximum-class-mass transfer, not uniform Picard
sampling. At e=8 it is below 8.247e-59. The one-degree-step ratio is at most
4*9^5/p^3*(U^2/p)^5 < 0.000312, since each of g and d grows by a factor <2.
The prime-count condition p^d>=4(g+1)^2(d+6)^2 holds initially and improves
at each integer step (the polynomial RHS ratio is <16, versus p^10).
Thus the argument extends to every dyadic e>=8. Actual cube rank must still
be checked and bad primes rejected. The displayed finite G=11I-E is not
claimed to be a draw from this sampler or to retain full cube upon pullback.

## Stronger Classical Baseline

If the rowspace distance is greater than k, deletion of a k-column basis
leaves rank k. Choose disjoint bases I,J; fix all remaining coordinates to 1.
Set M=B_I^-1 B_J and b=B_I^-1(s-B_R*1). Find x_i!=0 and (Mx)_i!=b_i,
then set z_J=x and z_I=b-Mx. The code checks actual ranks and the original
equation, without trusting a distance flag.

For each output row, identify its last nonzero variable. Assign variables
in order, excluding zero and the affine root of each row finalized there.
At most k+1 values are excluded. Hence p>=k+2 gives a deterministic witness
in polynomial time. More generally, a smaller maximum bucket can suffice;
outside this guarantee a dead end is UNKNOWN, not UNSAT. Tests include an
invertible matrix where greedy fails although a full witness exists.

For this family the unconditional low-dimension range is e<=202 at p1019
(dyadic maximum 128), versus e<=19999 at p100003 (dyadic maximum 16384).
This is a search algorithm, NOT a uniform sampler. General affine AJT
existence at fixed p does not supply a polynomial extractor for unbounded k.

Systematic rejection still succeeds with the exact probability
(1-1/p)^k*(1+R_s), |R_s|<=alpha. Its binary trial exponent per e changes
from about 0.000072133 to about 0.0070824, roughly 98-fold. This compares
one baseline, NOT a classical lower bound. The potential asymptotic advantage
remains conditional polynomial quantum time versus this exponential upper
bound; that comparison alone does not establish an advantage.

## Next Decisive Experiment And Falsifiers

Implement the previously specified native tower/RR backend for this smaller
seed, then construct a genuine e=256 input with a verified full cube. At
that point the general greedy cutoff no longer applies, but rejection is
still cheap. Increase to e=512 and e=1024 only with actual input matrices,
matched original-syndrome attacks and measured costs. These rows are NOT
generated by this pass. At e=1024 the dense matrix has 115410944 entries.

Kill or revise this route if the source/representation contract fails, the
cube remains deficient, auxiliary norms solve the new classes, a general
AJT extractor applies, or classical attacks scale polynomially. Do not claim
hardness from any capped attack. Do not prioritize more parameter sweeps of
unconstructed curves. The next valuable mathematical question is a
constructive general classical attack or a useful-problem reduction, not
another generic existence or nearby-barrier note.
