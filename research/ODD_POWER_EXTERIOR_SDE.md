# Odd-Power Exterior SDE Fallback

28 October 2026. Local deduction with independent automated mathematical
review. Not a novelty claim, Lean proof, or quantum speedup. The stronger
[symmetric method](POWER_SDE_SYMMETRIC_CONTRACTION.md) is preferred when its
larger field guard holds; this method retains a useful lower-field regime.

## Claim

For fixed odd d>=3 dividing p-1, prime p satisfying
`p>=4*((d-1)*(d-2))^2`, arbitrary vectors of rank r have a constructively
verified nonzero SDE witness from

```
A_(d-1)(r,d) = product_{j=0}^{d-2} ((d-1)^j*r+1)
```

columns. This is O_d(r^(d-1)), versus the published odd-degree O_d(r^d)
collision bound, not versus a claimed lower bound. Arithmetic time is
expected polynomial for fixed d with the same unclocked-root qualification
as the symmetric method. No input-label distribution is assumed.

## Construction

Let z_i represent the d power cosets, and W=ker(z), dim(W)=d-1. Recursively
construct the [published disjoint-support collision tensors](https://arxiv.org/html/1503.09016v2)
but solve each dependence only on its free coordinates, those with no
index d-1. The axis constraints recover all other coordinates. Level l
therefore needs `(d-1)^(l-1)*r+1` child tensors, not d^(l-1)*r+1.

At level l normalize one nonzero dependence coefficient into coset l-1.
This preserves nonempty representation support at index `(0,1,...,l-1)`.
The tensor belongs to `W^(tensor l) tensor F_p^r`, with pairwise disjoint
supports and root weights representing every cell value. All axes are
checked explicitly by the implementation.

Stop at level d-1. Let U_i be the signed alternating sum of cells whose
indices omit i, with the remaining indices in increasing base order.
The one-dimensional exterior power of W gives

```
U_i = (-1)^(d-1-i)*(z_i/z_(d-1))*U_(d-1).
```

This is a linear identity on the whole tensor space, not an assumption that
the tensor is decomposable or a nonzero volume. No factorial denominator
is introduced. Tests check it on a spanning tensor basis and repeated
basis vectors whose alternation vanishes.

Choose a_last=1, all other scales except a_0,a_1 zero, and solve
`z_0*a_0^d-z_1*a_1^d+z_last=0`. The corresponding weighted sum of the U_i
vanishes. Because d is odd, permutation signs can be absorbed into root
weights. Different omitted-index permutations have disjoint supports, so
the distinguished cell in U_last survives regardless of its vector value.

## Scalar Curve And Caps

The homogeneous curve `z_0*x^d-z_1*y^d+z_last*z^d=0` is smooth since p>d
and all coefficients are nonzero. Its genus is `(d-1)*(d-2)/2`. Distinct
power cosets and the fact that -1 is an odd power exclude rational points
on all three coordinate axes. All points therefore have a unique chart
with z=1. [Hasse--Weil](https://math.mit.edu/~poonen/papers/Qpoints.pdf)
gives at least `p+1-(d-1)*(d-2)*sqrt(p) >= p/2` points under the guard.
Each successful uniform a_0 has exactly d roots a_1. Acceptance probability
is at least 1/(2d). Extract one root and verify the original scalar equation.

With J generator draws and K scalar draws, the union abort bound is
`(1-phi(d)/d)^J+(1-1/(2d))^K`, clipped at one. Uniform independent draws
are required. Fixed seeded controls are not a proof of this probability.
Root extraction and random-integer internals are not an enforced clock.

## Decisive Controls And Boundaries

- At p11,d5 with representatives (1,2,4,8,5), `a^5-2*b^5+5=0` has no
  solutions, including zero a,b. This falsifies deleting the field guard.
- At p13,d4, -1 is not a fourth power. This method intentionally rejects
  even d; the symmetric method is the separate resolution in large fields.
- Degree5 p601 rank2 uses 114939 columns; the symmetric large-field method
  needs only27 at the same degree/rank, but does NOT apply at p601.
- Composite degree9 scalar controls verify coset generation and closure,
  not the potentially enormous full tensor construction for degree9.
- Original equations are checked after compression, and again after any
  Bezout exponent lift. False zero-rank compression is a rejection, not an
  unchecked accepted witness.
- The weighted phase-stage control forbids `evaluate_fixture`, checks actual
  degree reduction and charges every input packet, including zero scales.

Implementation: `theorems/odd_power_sde.py`. Run
`python qsearch.py odd-power-sde --write`; read `research/AGENT_HANDOFF.md`
for actual test counts and scope. No general-prime or practical receiver
claim is made.
