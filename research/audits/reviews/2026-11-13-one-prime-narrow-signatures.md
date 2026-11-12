# One-prime Galois 2-fields: narrow classes and signatures

2026-11-13. Independent proof-only check of the parent's strengthening of
`2026-11-13-one-prime-two-class-coverage.md`. Current STATE and that full
review were consulted. No Git, network, external API, archives, numerical
experiment, or shared-note edit.

**Accepted.** If K/Q is a totally real finite Galois extension of 2-power
degree n, ramified at at most one finite rational prime, then its NARROW
ideal class group Cl^+(K) has odd order. The unit-signature map is an
isomorphism

    O_K^*/O_K^{*2}  ->  {+1,-1}^n.

In particular Cl^+(K)->Cl(K) is an isomorphism, every sign pattern occurs
among units, and every totally positive unit is a square of a unit.
This is an algebraic existence statement, with no unit construction,
height, local-image, runtime, or novelty claim.

## 1. The narrow extension is canonical

Use the narrow class group for the modulus consisting of ALL real places.
The maximal abelian extension unramified at every finite prime, with
ramification at real places allowed, is its class field. Let M/K be the
subextension corresponding to

    Cl^+(K)/2 Cl^+(K).

It is finite, abelian of exponent 2, and unramified at every FINITE prime.
It need not be assumed totally real.

This extension is canonical under Aut(K/Q). Explicitly, an automorphism
of K permutes its real embeddings and preserves the subgroup of totally
positive elements: sigma(alpha) is totally positive whenever alpha is.
Thus it acts on Cl^+(K), preserves 2 Cl^+(K), and sends the corresponding
class field to itself. Equivalently, every Q-conjugate of M is again the
maximal elementary-2 extension of K unramified at finite primes, with no
restriction at infinity. Since K/Q is Galois, this proves M/Q is Galois.
Its group Gamma is a finite 2-group. Put H=Gal(M/K).

Using all real places is essential to this canonicity argument. One must
not replace M by an arbitrarily chosen quadratic narrow class extension,
or use a non-invariant subset of real places and assume normality over Q.

## 2. Finite inertia still forces H=1

Let p be the sole possible finite ramified rational prime. Because M/K is
unramified at finite primes, M/Q is unramified at every finite prime other
than p. Let I be its inertia subgroup at a prime above p.

If I were proper, it would lie in a maximal subgroup N of Gamma. A maximal
subgroup of a finite 2-group is normal of index 2. It therefore contains
all conjugates of I. The quadratic field M^N/Q would be unramified at p
and every other finite prime. This is impossible for BOTH real and
imaginary quadratic fields: a nontrivial quadratic field has fundamental
discriminant of absolute value greater than 1. Hence I=Gamma.

The relative finite inertia subgroup for M/K is `I intersect H`. It is
trivial by the definition of M, even if a real place ramifies in M/K.
Since I=Gamma, this forces H=1. Therefore `Cl^+(K)/2 Cl^+(K)=0`, and the
finite group Cl^+(K) has odd order. If K has no finite ramification, the
same quadratic-quotient argument first gives K=Q, whose narrow group is
trivial.

There is no hidden assumption about infinite behavior here. Before the
conclusion, M may be allowed to acquire complex embeddings; that does not
alter finite inertia or the quadratic discriminant contradiction. In fact
M/Q being Galois precludes mixed real/complex behavior among its absolute
embeddings, but the argument does not need to choose either possibility.
The conclusion M=K rules out the complex case automatically.

## 3. Signature consequence and its boundary

Weak approximation and the definitions of ordinary/narrow principal ideals
give the exact sequence

    O_K^* --sgn--> {+1,-1}^n -> Cl^+(K) -> Cl(K) -> 1.

Thus the kernel of Cl^+(K)->Cl(K) is the elementary 2-group
`{+1,-1}^n/sgn(O_K^*)`. Since Cl^+(K) is odd, this kernel is trivial.
The signature map on units is consequently surjective.

Squares have positive signature. Dirichlet's unit theorem for a totally
real degree-n field gives

    O_K^* ~= {+1,-1} times Z^(n-1),
    dim_F2 O_K^*/O_K^{*2}=n.

The induced surjection onto the n-dimensional signature space is therefore
an isomorphism. Its kernel assertion is exactly
`O_K^{*,+}=O_K^{*2}`. A unit with any specified single negative embedding,
and hence a unit of norm -1, exists.

This does not produce any of those units or bound the cost of naming them.
Although a unit squareclass is abstractly determined by its real signs,
its finite-place squareclass coordinates are not computed by this proof.
No unit, local-image, global-dimension, or end-to-end algorithm shortcut
follows without a separate constructive argument.
