# Replace Exact Jacobian Uniformity By Mod-Two Anti-Concentration

Date: 2026-10-26. Parent deduction; independent review pending.

## Change To The Access Contract

The relation-lattice rational-halving reduction in
`../auxiliary-construction-check-2026-10-26/REVIEW.md` does not require
exact uniform samples from the full Jacobian. It suffices to have fresh
independent samples X whose images in J/2J satisfy

```text
|E chi(X)| <=1/2 for every nontrivial character chi of J/2J.       (1)
```

Exact group order h=2^s M, M odd, is STILL an external input. Exact bounded
group arithmetic and the effective perfect pairing J[2] x J/2J -> {+1,-1}
are STILL required. This is not an order-finding algorithm or native solver.

For the actual q=100003 curve family, an exact uniform degree-n prime P,
represented as X=[P-nO], satisfies (1) whenever

```text
q^n >=16 (g+1)^2 (n+6)^2.                              (2)
```

The prime-character bound was independently reviewed in the earlier bundle.
The required prime sampler does not need a zeta polynomial:
[Bruin, Algorithm 3.2](https://arxiv.org/html/1003.2563) takes the truncated
graded algebra and a degree bound, whereas the exact uniform Jacobian route
uses the zeta numerator. This note replaces that route for THIS halving
algorithm only. It does not assert that prime classes are uniform, or that
every algorithm using uniform Jacobian samples can use this replacement.

Consequently, full zeta/Frobenius data are unnecessary solely to supply
this algorithm's samples, IF the exact order h is acquired some other way.
If h itself is computed through a zeta routine, that computation still
costs whatever it costs. No uniform polynomial h-from-B theorem is supplied.

## Why The Relation Routine Still Works

Let T_1,...,T_t be represented order-two elements and U their span. For
any nonzero T in U, perfection makes chi_T(X)=e(T,X) a nontrivial
character. Hence Pr(e(T,X)=1)<=3/4 by (1). For b independent sample rows,

```text
Pr(some nonzero T in U survives every row) <= (2^dim U-1)(3/4)^b.
```

Take b=4(t+1) for t>=1. The upper bound is less than1/4: it is bounded by
(81/256)(81/128)^t, already below1/4 at t=1 and decreasing. A basis for
the sampled sign-matrix kernel is checked by exact group evaluation. All
true relations are always in that kernel; verification therefore certifies
the full relation space, without any torsion-basis assumption. Failed
verification triggers fresh rows/batches; it cannot accept a false relation.
Expected batches are <4/3. The original exact lattice-saturation proof and
polynomial bit bounds are unchanged.

Fresh independence is essential. Repeating one marginally unbiased sample
does not make b independent tests. Sampling only the current subgroup or
only divisors of a fixed line bundle can violate (1).

## Why The Two-Primary Group Is Still Generated

Let H=J[2^infinity]. Multiplication by the known odd part M maps J onto H.
For any proper subgroup H' of H, choose an index-two subgroup K containing
H'. Its nontrivial character pulls back under multiplication by M to a
nontrivial character of J/2J. Thus

```text
Pr(MX notin H') >= Pr(MX notin K) >=1/4.
```

Retain MX only when exact relation-lattice saturation shows a strict
increase in the generated subgroup order. At most s increases are needed;
expected proposals <=4s. The known order 2^s certifies termination, so
there is no unverified stopping criterion. The samples in H may be very
far from uniform. Only their escape from every proper subgroup is needed.

Now extract a basis of H[2] from its certified presentation, obtain class
labels by pairings, and solve doubling using the reviewed integer-lattice
congruence. The same odd-part recombination solves 2y=x in J. All per-row
pairings, prime representations, normalization and group operations recur
and remain charged. No odd-part discrete logarithm is introduced.

## Prime Degree And Graded-Algebra Budget

Choose the smallest positive n satisfying (2), using exact integer powers.
For q=100003 and g>=1, n<=g+1: at n=g+1 inequality (2) holds already at
g=1; its left/right ratio increases by a factor greater than q/16 each
time g increases. Indeed ((g+2)/(g+1))^2*((g+8)/(g+7))^2<16.
The chosen n is O(log(g+1)) at fixed q. The reviewed character estimate
implies nonempty degree-n primes, so the sampler's empty-set nontermination
case is excluded.

For the recovered line bundle of degree ell=2g+2, take Bruin's i=2:
n<=g+1<=2ell-2g=2g+4. Truncation through6 suffices for prime sampling;
the existing through7 contract also covers supplied order-two pairings.
The divisor class [P-nO] and its bounded representation must be constructed
using the represented-divisor routines; neither a label nor an uncharged
normalization oracle is supplied by the inequality. For the genus41,
81,161,321,641 examples the smallest sufficient n is2. These primes are
for relation/group-generation sampling, NOT the degree-a auxiliary divisor;
there is no change to that search's total-degree constraint.

## Tests And Falsifiers

Exact finite-group controls test distributions supported on one representative
of each parity class, mixed with an atom of weight1/2. They have maximum
nontrivial mod-two bias1/2, although they can be far from uniform on H.
They are proof controls, not implemented curve samplers or native algorithms.

Falsifiers: nonindependent draws; wrong prime-degree estimate; unknown or
incorrect h; an imperfect/misnormalized pairing; failure to represent
P-nO with charged polynomial cost. Uniformity is relaxed only as stated.
The perfect-pairing and exact-order premises are not removed. A future
probabilistic order estimate needs its own verification and error budget.
