# Class-Three Normal-Word Bridge

**Status: explicit public classical conversion with finite independent
controls; complete HSP composition and novelty review pending.**

The previous receiver required public Lie structure constants. The
published nilpotent reduction instead supplies polycyclic presentations.
Naming the Lazard correspondence is not enough to connect these
interfaces: conversion must work coherently on unknown coset states,
without an uncharged coordinate oracle.

For exponent-`p`, class-at-most-three groups with `p>3`, this note gives
explicit forward and inverse algorithms using only the supplied
normal-word collector. No hidden subgroup is involved.

## The Published Interface

[Ivanyos, Sanselme and Santha, author-hosted March 2, 2010 version,
Section 3](https://www.irif.fr/~santha/Papers/iss12.pdf) assumes unique
refined polycyclic normal words and efficient collection. Its Theorem 2
reduces a subgroup/quotient-closed constant-class family to exponent-`p`
groups with trivial or order-`p` hidden subgroup. Subgroup and quotient
presentations remain available. Lemma 2 uses polynomially many calls
through normalizers. Lemma 3 separately invokes known bounded-exponent
machinery when the prime is at most the class.

This is an oracle reduction, not a claim that a single original coset
sample suffices to simulate arbitrary restricted-oracle queries.
The reduction and its group-algorithm dependencies are PRIOR ART.
This repository has not implemented its normalizer recursion or
black-box presentation acquisition.

The new bridge starts AFTER the public presentation is available. Its
input promises are:

- `p>3`, exponent exactly dividing `p`, class at most three;
- `G=G_1 > ... > G_(d+1)=1` with cyclic order-`p` factors;
- generators `g_i in G_i` whose normal words
  `g_1^a_1 ... g_d^a_d`, `0<=a_i<p`, are unique;
- a deterministic polynomial-time normal-word multiplication routine.

These are mathematical input promises, not properties inferred from
passing a handful of random tests. The finite module rejects invalid
coordinates and characteristic but does not certify an arbitrary
adversarial collector as a valid group.

## Constant-Length Lie Operations

Fix the group commutator convention

```
[g,h]_grp = g^-1 h^-1 g h.
```

Write `g=exp(X)`, `h=exp(Y)`, `B=[X,Y]`, `C=[X,B]`, `D=[Y,B]`.
The class-three truncated BCH identity gives

```
log([g,h]_grp) = B-(C+D)/2.
```

With `w=[g,h]_grp`, the commutators `[g,w]_grp` and `[h,w]_grp`
are central, with logarithms `C` and `D`. Therefore

```
Bracket(g,h) = w * [g,w]_grp^(1/2) * [h,w]_grp^(1/2)

Add(g,h) = g*h*w^(-1/2)
             * [g,w]_grp^(-1/12) * [h,w]_grp^(1/12)
```

represent exactly `exp([X,Y])` and `exp(X+Y)`. All exponents are
interpreted modulo `p`. Scalar multiplication is ordinary group powering.

For the addition formula, BCH gives
`log(g*h*w^(-1/2))=X+Y+(C-D)/12`; the final central factors cancel
that residual. Omitting them silently applies a class-two formula and
is wrong in class three. The test suite exhibits this failure.

Each operation uses a constant number of group powers, each computed
with `O(log p)` collection calls. This does not require evaluating a
logarithm, identifying a hidden generator, or enumerating the group.
The exp/log symbols are the mathematical proof, not oracle primitives
provided to the algorithm.

## Recover Coordinates Along The Flag

Every subgroup `G_i` is closed under these group words and powering,
so it is an additive `Fp` subspace under `Add`. Since
`G_(i+1)` is normal in `G_i`, the corresponding quotient is an additive
one-dimensional space. In that quotient, `Add` agrees with multiplication:
all commutator corrections disappear.

Consequently `g_1,...,g_d`, interpreted as additive elements, form a
vector-space basis. To obtain the additive coordinates of a normal word:

```
current = input
for i=1,...,d:
    a_i = ith normal-word digit of current
    current = Add(current, g_i^(-a_i))
return (a_1,...,a_d)
```

At iteration `i`, `current` lies in `G_i`. Removing its leading quotient
coordinate puts it in `G_(i+1)`. The algorithm ends at the identity.
It requires `O(d log p)` collection calls.

The inverse is `Add`-summing `g_i^a_i`. It has the same polynomial cost.
Normal-word digits generally differ from additive coordinates. No
discrete logarithm or search is hidden in extracting a digit: that is
the supplied encoding.

The flag need not be central in the whole group. A test uses Heisenberg
normal words `X^a Z^b Y^c`: the final subgroup `<Y>` is normal in
`<Z,Y>` but not in the whole group. Peeling still works, and the
derived basis must be moved from the middle to the end.

## Public Structure Constants And Coherent Encoding

Compute `Bracket(g_i,g_j)` and decode it for every pair. Those are
the Lie structure constants in the additive basis. Row-reduce their
span, choose a vector-space complement, and change basis so the derived
ideal is last. The existing `ClassThreeBCH` checks Jacobi, the derived
span, its commutativity and class at most three on the resulting tensor.

The preprocessing uses `O(d^3 log p)` collection calls with this simple
implementation, plus polynomial field arithmetic. The exact count in
the artifact is a diagnostic ledger, not a universal tight bound.

Both coordinate maps are explicit deterministic polynomial-time
classical functions with explicit inverses. Reversible compilation can
therefore implement a clean basis permutation: compute the new encoding,
swap output registers, and erase the old encoding using the inverse.
The same applies to the public adapted-basis matrix and the existing
Lie-to-`exp(n)exp(q)` chart map.

This supplies a WRITTEN efficient coherent relabeling argument from the
normal-word interface. No quantum gate compiler was executed. It does
NOT obtain normal words from an arbitrary black-box encoding for free.

## Two Missing Promise Cases In The Current Receiver

The executed receiver currently assumes a nontrivial cyclic subgroup
transverse to the derived ideal. The published reduction may also
produce the trivial subgroup or a subgroup contained in that ideal.
These must be handled, not silently discarded.

Under the trivial/order-`p` promise there is a direct dispatch:

1. Let `N=[L,L]`, abelian in class three. On fresh original coset states,
   measure quotient coordinate `q`, then apply `Phi(-q)` to the normal
   register. This gives standard abelian coset states for `H intersect N`.
   For a transverse cyclic `H`, fixing `q` fixes its parameter, so the
   normal state is maximally mixed after averaging original cosets.
   For `H<=N`, inverse conjugation removes the measured quotient twist.
2. Learn `H intersect N` by abelian Fourier sampling. A nontrivial result
   is the whole `H` under the promised cardinality bound.
3. Otherwise run the phase-erasure construction. If `H` is trivial,
   each conditional quotient source is `I/|A|=rho({0},P)` for ANY `P`.
   The mixed-instrument lemma still applies; its phase erasure leaves
   `I/|A|`. For a transverse `H`, it gives `rho(span(v),0)`.
4. Collect enough quotient Fourier samples to learn the annihilator,
   allowing its rank to reach `m`, not stopping at `m-1`. Full rank
   means trivial `H`; codimension one supplies the learned quotient
   line. A larger nullspace is an incomplete run, not a larger found H.
5. Only on the nonzero learned line invoke the known quadratic HPGP
   completion.

For an annihilator of dimension `r<=m`, `t` uniform samples fail to span
it with probability at most `p^(r-t)/(p-1)`. Taking
`t=m+ceil(log_p(1/epsilon))+1` suffices. Source copies for all samples,
including zero/dependent samples, are charged.

The current `learn_quotient_line` diagnostic stops upon finding a line.
It is therefore NOT this complete dispatch. Do not run it on the trivial
case and interpret the first `m-1` independent frequencies as proof of a
hidden line. The written dispatch above is not yet an executed all-case
HSP receiver.

## What Can Now Be Proposed, Not Admitted

Combining the exact mixed-source lemma, published general SDE solvers,
normal-word bridge, guarded trivial/cyclic dispatch and known ISS
reduction suggests a polynomial-time class-three HSP algorithm in the
paper's normal-word/oracle model. This is a substantially sharper
candidate theorem than a finite UT4 signal.

It remains a LOCAL proposed composition, not an accepted new theorem.
Independent review must check:

- the common cubic potential on every allowed class-three presentation;
- adaptive coefficient-rank bounds and full bit/gate/error accounting;
- the guarded dispatch and the ISS recursive oracle interfaces;
- prior-art overlap, including whether an existing result already
  implies this restricted-class statement;
- a useful external computational problem reducible to this HSP family,
  with stronger classical baselines than opaque-label collision search.

The present pass executes only the public coordinate bridge. No
arbitrary-H recursion, black-box setup, external reduction, cryptographic
speedup or Shor-level result is claimed. DCP's unbounded nilpotency class
is not covered by fixing class three.

Follow-up: `NIL3_POLYNOMIAL_HIDING_ATTACK.md` rules out a tempting
application in a precise input model. If the ORIGINAL hiding function is
field-valued of trusted degree `e` in these public Lie coordinates and
`p>2(e+1)`, a charged value-only classical derivative attack recovers its
stabilizer in polynomial time. This does not apply to arbitrary opaque
labels merely because their quantum source potential is cubic.

## Reproduction

```
python -m theorems.nil3_normal_word_bridge --write
python -m pytest -q tests/test_nil3_normal_word_bridge.py -W error::RuntimeWarning
```

Independent checks use ordinary upper-unitriangular matrix multiplication
and the finite matrix logarithm. They verify Lie addition/bracket, inverse
encodings, computed adapted structure constants, BCH multiplication, the
wrong class-two formula, and a non-globally-central polycyclic flag.
