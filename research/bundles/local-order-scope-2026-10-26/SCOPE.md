# Remove Easy Local Orders Before Testing Source Advantage

2026-10-26. A matched-baseline correction and exact local arithmetic audit.
No new quantum candidate, native recovery, or independent review is claimed.

## Decision

Do not use the previous index-9 positive harvest or index-17 zero-query
failure fixture as evidence about the hard full-suborder regime. Both are
locally Eichler. Retain them as exact identity/failure controls. Large index
or a large prime alone does not make a supplied suborder difficult.

Before investigating a nonzero source query, remove the already classically
accessible local components: cheap native units, ramified completion, small
bad primes, and Bass components at any prime. Factorization and native
endomorphism representations remain charged. The scientifically relevant
residual question concerns NON-BASS components at LARGE primes, unless a
different task explicitly targets factoring itself.

## Published Baseline: Read The Full Theorem

[Eisentrager--Scullard v2](https://arxiv.org/html/2402.05059v2), revised
2026-01-21, Theorem 1.1, charges linear dependence on the largest bad prime
besides polynomial bit-size terms. Proposition 7.2 gives polynomial bit cost
for Bass local inputs using interval selection. General local selection
uses prime-sized branching (Section 6); Algorithm 8.1 combines the components.
These bounds require factored discriminant and suitable efficient native
map representations. Proposition 4.1 identifies scalar orders with tree
balls. The landing-page abstract omits the large-prime factor, unlike the
full theorem. Use the latter. The retained versioned HTML is source evidence,
not an implemented dependency. Local Bass overorder enumeration also appears
in [EHLMP, Section 4](https://msp.org/obs/2020/4-1/obs-v4-n1-p14-s.pdf).

For our general native rank-four basis, apply the local steps to its own
multiplication table and integrality tests. Do not select two basis elements,
replace R by the possibly smaller generated order, and silently preserve R's
Bass type or discriminant. Local-to-global lifting and numerator evaluation
in the original basis must be provided for every division query. Our previous
trace-coordinate preprocessing is relevant; an abstract matrix callback is
not that native implementation.

## Exact Classification Of The Existing Fixtures

### Index 17, characteristic 11

The zero-query control defines R as the inverse image of the stabilizer of
the line (4,1) in O/17O = M_2(F_17). That stabilizer is a Borel algebra of
dimension three. Choosing the line as the first basis vector gives

    R_17 = [[Z_17, Z_17], [17 Z_17, Z_17]].

It is the intersection of the central maximal order and the neighbor
attached to that line. Its maximal overorders are exactly those two vertices.
This follows also from the elementary-divisor description: R contains both
diagonal idempotents, so every stable lattice splits into its two axes;
stability under E_12 and 17 E_21 leaves two relative valuations.

The new test reconstructs the OLD fixture without changing it. Its images
have precisely one common invariant line, (1,13), the same line as (4,1).
Thus the earlier full-automorphism failure is logically valid, but is not
a failure on a difficult order-completion instance.

### Index 9, characteristic 11

The positive harvest fixture is R=<1,3i,h,3ih>, h=(1+j)/2, j^2=-11. Locally

    R_3 = Z_3[h] + 3 O_3,       h^2-h+3=0.

The polynomial has distinct roots 0 and 1 modulo 3, lifting modulo 9 to 3
and 7. Its derivative is a unit at each root, so Hensel lifting gives
Z_3[h] = Z_3 x Z_3 inside M_2(Z_3), after an integral basis change. Hence
R_3 has arbitrary diagonal entries and off-diagonal entries in 3Z_3.
Conjugating by diag(1,3) gives the standard Eichler order with lower-left
entry divisible by 9 and unrestricted upper-right entry. Stable-lattice
axis valuations now give three maximal overorders on a length-two path.

The successful pullback recovered an already easy elliptic unit. The old
receipt said so. This audit adds an independent structural reason the
fixture cannot test large-prime non-Bass behavior.

## A Concrete Residual Local Family

This is an arithmetic regime specification, NOT an invented opaque-oracle
candidate or a native hard-instance generator. In M_2(Q_q), let

    M = M_2(Z_q),       R = Z_q I + q M.

The basis I,qE_11,qE_12,qE_21 has index q^3 in M. Write a lattice vertex as
L=U diag(1,q^r) Z_q^2, U in GL_2(Z_q), r>=0. Since U normalizes qM,
R preserves L exactly when q M preserves diag(1,q^r) Z_q^2, namely r<=1.
Thus the containing maximal orders are M and its q+1 neighbors: q+2 total.
They form a branching ball, not the containing-order path of a Bass order.
This order is non-Bass.
All containing maximal orders have the same local covolume, so [M':R]=q^3
for each of them. The reduced discriminant has valuation 3, not q or q+2.

The center is computable abstractly, but need NOT equal the native target
End(E)_q. Testing whether the center is native-integral can reject it; that
does not select a particular neighbor. For example the neighbor defined by
diag(1,q) contains E_12/q but not E_21, whereas M contains E_21 but not
E_12/q. Substituting any convenient abstract maximal overorder changes the
problem. The controls explicitly reject this substitution.

For a native global input, the local family must be realized in the SAME
supplied evaluable suborder and curve. No such unknown-target realization
was generated here. Handing a test the full order or its target lattice
would only supply the answer again.

## Why Boolean Division Is Still Not A Coset Label

For X integral in M, membership in a neighboring order is precisely
invariance of its associated line under X mod q. A nonscalar two-dimensional
linear map has at most two invariant lines; a scalar fixes every line.
If X is nonintegral in M, it cannot belong to two distinct neighbors: their
intersection is contained in the center. To check this directly, move the
two residue lines to the coordinate axes by GL_2(Z_q). Their intersection
has integral diagonal entries and both off-diagonals divisible by q.
Therefore arbitrary rational
element-membership tests do not evade the existing eigenline-interface
argument merely by allowing denominators.

This reuses, rather than rediscovers, the proof in
../native-membership-baseline-2026-10-25/NATIVE_MEMBERSHIP.md, Section 6.
Its classical linear / quantum square-root query bounds apply ONLY after
discarding native curve and representation data. They are not native
EndRing lower bounds. A division routine's returned maps, PPAV canonical
models, or automorphisms might expose additional information. Neither this
audit nor finite incidence enumeration excludes such classical leakage.

## Bit Cost And The Implemented Controls

Let M_k=End(diag(1,q^k) Z_q^2). For 0<=a<=b,

    M_a intersect M_b = <E_11, q^(-a)E_12, q^b E_21, E_22>.

This order is contained in M_k exactly for a<=k<=b. A binary path selector
therefore takes at most 4*ceil(log2(e+1)) element tests on a known length-e
Eichler path, independently of the VALUE of q. Four tests are deliberately
charged per iteration; no hidden callback short-circuit changes the count.
The result depends on an exact containment callback and a promised path.
UNKNOWN is an error, not a negative branch.

The code checks this at q=2^61-1 without enumerating q directions. Its
neighbor enumerator is instead explicitly O(q), restricted to small exact
controls. All target frames are supplied, all arithmetic is rational, and
no division, torsion, PPAV backend, or native algorithm ran.

## Adversarial Assessment And Next Decisive Work

1. The direct additive-source proposal remains unreviewed. Its possible
   contribution is a source/assumption change for an already-studied endpoint,
   not a first quantum solution or a demonstrated separation.
2. Full-suborder access is itself strong advice. Do not transfer this result
   to OneEnd, bare EndRing, ECDSA, or an unspecified cryptographic input.
3. Missing factorization prevents claiming a complete classical polynomial
   baseline. Conversely, a speedup solely from factoring reuses Shor and
   does not fulfill the research objective.
4. Generic nonzero polarization forms may have only the known symmetries;
   a universal inverse-polynomial harvest probability remains unsupported.
   A successful easy unit or Bass fixture cannot establish that probability.
5. The next question is whether the ACTUAL native additive source either
   supplies exact labels or leaks classical information on a unit-saturated,
   large-prime non-Bass component. First seek a mathematical information
   argument, not another small opaque-label experiment.
6. Falsifiers: a conjugation/field/native-evaluation gap blocks the source;
   a polynomial classical extraction on the same residual input defeats
   its proposed separation; a proof that useful nonzero automorphisms are
   too rare defeats that particular harvest strategy, not all baselines.

No general hardness, hitting theorem, novelty, or advantage follows from
these classifications. No additional independent reviewer was launched.
