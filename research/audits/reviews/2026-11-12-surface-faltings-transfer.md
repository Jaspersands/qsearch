# Independent review: uniform stable Faltings-height transfer

2026-11-12. Core review of the completed report
`../claude_runs/2026-11-12-closure-faltings/response.md` and its explicit
request/excerpts in `../api_inputs/2026-11-12-surface-closure/`.
The independently proved full atlas in `2026-11-12-merkl-log-atlas.md`
is used as established. Actual statements and relevant proofs were read
in `../sources/classical_surface_2026/javanpeykar.txt`.
No Git, network, API, archive, numerical sweep, or implementation was
used. Commands used `/opt/anaconda3/bin/python`.

## Disposition and exact theorem

ACCEPTED as a consequence of the established atlas and the actual
Javanpeykar source statements specified below. Two minor inaccuracies
in the paid report are repaired: a Galois-stable containing branch set
need not be the actual branch locus, and the source Wronskian has
factorial-normalized derivatives. Neither changes the claimed bound.
The extra differential-coordinate condition required for arithmetic
transfer is verified below for the precise atlas used in the independent
review; it is not inferred from four numerical atlas parameters alone.

Fix `r>=3`. Let `Y/Qbar` be smooth projective connected of genus `g>=1`,
and let `pi:Y -> P1_Qbar` be finite of degree `d`. Suppose the total
Galois orbit of its geometric branch locus contains at most `r` points.
Let `B` be that orbit closure, and put

```
h_B = max_(beta in B) h(beta),
```

using the ABSOLUTE LOGARITHMIC projective point height. Then

```
h_Fal(Y) <= C_r d^5(d+1+h_B),
```

for an effective constant depending only on `r`, with the source's
normalization of stable Faltings height. No height bound for a presented
model of `Y`, no quantitative semistable-reduction field, and no uniform
archimedean separation of a chosen base value are additional hypotheses.

This closes the scoped UNIFORM STABLE FALTINGS-HEIGHT inequality. It does
not close heights of supplied coordinates, torsion divisors or functions,
native model construction, arithmetic lifting precision, or reconstruction.
It does not establish a polynomial-time algorithm for calculating the
Faltings height or constructing a semistable model.

## Primary-source ledger and normalization

The source file is the actual Javanpeykar text for arXiv:1403.6404,
SHA256 of the supplied PDF
`59357cc190f89098d32e4dd1d1c1c7802e25b26aeeea3a8766cafea8089086bc`.
The following are source theorems/conventions used here, not new claims
obtained merely from the paid report's verdict:

* Section 1.3, physical lines 101-112, calls `H_B` an EXPONENTIAL
  height. Our parameter is `h_B=log H_B`. Source Theorem 1.3.1 is not
  being reinterpreted as a logarithmic-height theorem.
* Section 2.1, lines 221-244, fixes the probability canonical measure,
  the orthonormal differential inner product, and

```
-log ||dz||_Ar(x)
  = lim_(y -> x) [gr_Y(x,y)-log|z(x)-z(y)|].
```

* Lines 289-303 define

```
W_z(omega) = det( f_k^(j)(z)/j! )_(0<=j<=g-1,1<=k<=g),
omega_k=f_k dz,
Wr = W_z(omega) (dz)^(g(g+1)/2).
```

  Its zero divisor is effective of degree `g^3-g`. The norm is
  independent of unitary changes of the orthonormal basis.
* Section 2.3, lines 404-464, defines stable `h_Fal(Y)` and the stable
  Arakelov point height
  `h(b)=(P,omega_min)/[K:Q]` on a semistable minimal regular model.
  It defines `log||Wr||_Ar(b)` by the average over ALL embeddings
  `K -> C`, including both members of a nonreal conjugate pair.
  Field-independence is part of those source definitions/results.
* Lemma 2.3.1, lines 468-500, compares `h(b)` from above with
  `(P',omega_Y')/[K:Q]` on another regular model.
* Theorem 2.4.1, lines 506-514, states for a non-Weierstrass point

```
h_Fal(Y) <= A_g h(b)+log||Wr||_Ar(b),
A_g=g(g+1)/2.
```

  Its proof at lines 668-691 invokes the cited de Jong result and the
  source's own formula (4). That underlying theorem remains a cited
  mathematical input, not something proved by this review. The actual
  statement includes genus one.
* Proposition 4.2.4, lines 1314-1398, gives the finite intersection bound
  for covers of arithmetic surfaces; `D1` includes horizontal components
  AND vertical components of residue characteristic greater than `d`.
* Theorem 4.3.2, lines 1413-1438, applies to ANY finite map of a smooth
  projective geometrically connected curve to `P1`, not only Belyi maps.
  After some finite extension, its finite flat normalization has a
  semistable minimal resolution, and all vertical branch components have
  residue characteristic at most `d`.

Thus the application uses actual general-cover statements. The special
archimedean base interval and modular-lambda estimate in Theorem 4.5.1
are replaced by the argument below, rather than applied outside their
hypotheses. The source's semistable-reduction and height theorems are
used with their stated mathematical scope; this is not an independent
re-proof of every foundational result cited in that paper.

## 1. Product formula: finite intersections and collisions

For a number field `K`, let `D_K=[K:Q]`. At a finite place `v`, use
`|x|_v=(#k(v))^(-ord_v(x))`. At archimedean places use the local-degree
weight, equivalently sum ordinary complex logarithms over every
embedding `sigma:K -> C`. These conventions give the product formula.
For projective points, use

```
h((x0:x1)) = (1/D_K) sum_v log max(|x0|_v,|x1|_v).
```

Let distinct `P=(x0:x1), Q=(y0:y1)` belong to `P1(K)`, and write
`Delta=x0*y1-x1*y0`. Let `I_fin(P,Q)` be the finite intersection of their
sections in `P1_O_K`, including the logarithms of residue norms. Define

```
vartheta_sigma(P,Q)
 = |sigma(Delta)| /
   [max(|sigma x0|,|sigma x1|) max(|sigma y0|,|sigma y1|)].
```

Primitive local homogeneous coordinates give

```
I_v(P,Q) = [ord_v(Delta)-min_i ord_v(x_i)-min_i ord_v(y_i)] log #k(v).
```

Summing and applying the product formula to `Delta` proves the EXACT
identity

```
I_fin(P,Q)+sum_sigma log(1/vartheta_sigma(P,Q))
  = D_K*(h(P)+h(Q)).                                      (1)
```

Here the finite intersection is nonnegative. Also `vartheta<=2`, and
the Euclidean homogeneous norm differs from the maximum norm by a
factor between one and `sqrt(2)`. For chordal distance `dist_ch`, (1)
therefore gives both

```
I_fin(P,Q)/D_K <= h(P)+h(Q)+log 2,                         (2)

(1/D_K) sum_sigma log(1/dist_ch(sigma P,sigma Q))
  <= h(P)+h(Q)+log 2.                                     (3)
```

These formulas include `infinity=(1:0)`, whose height is zero. No affine
denominator or bounded-coordinate promise is needed.

For the branch set, let `delta_sigma` be its minimum pairwise chordal
distance and `L_sigma=1+log(1/delta_sigma)`. Every logarithmic pairwise
collision is nonnegative, so the maximum is bounded by their sum.
Applying (3), for example to all ordered distinct pairs, yields

```
average_sigma L_sigma
 <= 1+r(r-1)*(2h_B+log 2).                                (4)
```

For a rational finite `a` outside `B`, put
`D_sigma(a)=min_(beta in B) dist_ch(a,sigma beta)`. Again using
nonnegativity and (3),

```
average_sigma log(1/D_sigma(a))
 <= S_a := sum_(beta in B) [h(beta)+h(a)+log 2].             (5)
```

Only these averages enter the proof. In particular, no claim that a
small rational `a` stays a prescribed distance from every complex
branch point is necessary.

## 2. Local Merkl control pays both signs of the cotangent norm

For each complex fibre, the established atlas gives a common bound

```
Lambda_sigma <= C_r d^3(d+L_sigma)
```

for the absolute local regularized Green function on an inner chart.
Letting its second argument tend to its first inside that chart and
using the source metric convention gives

```
|log||dz||_Ar(x)| <= Lambda_sigma.                         (6)
```

This uses the TWO-SIDED local part of Merkl's theorem. The global
upper bound on `gr` alone would not provide (6). Averaging (4) gives

```
Lambda_bar := average_sigma Lambda_sigma
 <= C_r d^3(d+1+h_B).                                    (7)
```

The Arakelov point-height calculation uses the original global affine
coordinate `t` on `P1`. The unitary Mobius coordinates of the analytic
atlas are not used to change the arithmetic model. Instead the relation
to `dt` is paid by the following differential estimate.

For a unitary Mobius coordinate `u`,

```
|du/dt|=(1+|u|^2)/(1+|t|^2),
|dt/du| >= 1/2                 when t is finite and |u|<=1. (8)
```

In the actual independent atlas, a Whitney chart centered at `s` has
coordinate `z=u_s(t composed_with pi)/rho(s)`, with

```
rho(s)=(1/100)*min(1/4,theta(s,B)),
```

where `theta` is spherical angular distance. If `x` lies in its unit
chart, then `theta(pi(x),s)<2rho(s)`. In the uncapped case,
`dist_ch(pi(x),B)<=theta(pi(x),B)<=102rho(s)`. In the capped case,
`rho(s)=1/400` and chordal distance is at most one. Thus uniformly

```
rho(s) >= (1/400) dist_ch(pi(x),B).
```

Combining this with (8) gives

```
|d(t composed_with pi)/dz| >= (1/800) dist_ch(pi(x),B).      (9)
```

For a branch chart, `u_b(pi(w))=h*w^e`, `|w|<1`. Away from its center,

```
|d(t composed_with pi)/dw|
  = |dt/du_b| * e*|u_b(pi(w))|/|w|
  >= (1/2) dist_ch(pi(w),b)
  >= (1/2) dist_ch(pi(w),B).                               (10)
```

At a ramification center the inequality extends with zero right-hand
side. Our eventual point lies over `a` outside `B`, so that case is not
used. A branch chart centered at infinity is also covered by (8)-(10)
for every finite evaluation value `t=a`: the large derivative of `t`
near infinity helps the lower bound.

Inner charts cover the whole compact curve, and (9)-(10) hold on their
full unit charts. Therefore, at a point `b_sigma` above finite `a notin B`,
(6) gives

```
-log||pi^*dt||_Ar(b_sigma)
 <= Lambda_sigma + log 800 + log(1/D_sigma(a)).             (11)
```

The factor from branch collision in (11) is logarithmic and is averaged
using (5); no uncharged coordinate derivative remains.

## 3. Wronskian bound from full-chart density

Let `omega_k=f_k(z)dz` be an orthonormal differential basis in a unit
chart whose inner disk contains `x`. The FULL-chart density estimate
`c1<=d^2` gives

```
sum_k |f_k(z)|^2 <= 2g*d^2              throughout |z|<1.
```

The radius-`1/4` closed disk around `z(x)` lies inside the unit disk,
because `|z(x)|<3/4`. Cauchy's estimate for the actual factorial-
normalized Wronskian entries is

```
|f_k^(j)(z(x))/j!| <= 4^j sqrt(2g*d^2).
```

Hadamard's determinant inequality consequently gives

```
log|W_z(omega)(x)|
 <= [g(g-1)/2] log 4 + (g/2)log(2g^2 d^2) =: W0.          (12)
```

Together with the UPPER side of (6), this proves

```
log||Wr||_Ar(x) <= A_g Lambda_sigma + W0.                  (13)
```

The bound holds everywhere, interpreting a zero of `Wr` as log norm
minus infinity; the later point is non-Weierstrass. It works for genus
one, where `A_g=1`, the Wronskian is one nonzero holomorphic
differential, and the Weierstrass divisor has degree zero.

The paid report used unnormalized derivative bounds and retained
factorial factors. That still gives a valid weaker upper bound, but
its equality with the source's `W_z` should use the normalized entries.
Equation (12) fixes the convention directly.

## 4. Finite places and the semistable extension

Choose a number field `K0` containing a field of definition of `Y,pi`,
all points of `B`, and the chosen fibre `pi^-1(a)`. Apply actual
Theorem 4.3.2, and write `K` for its finite extension. Let

```
pi_model: mathcal Y -> P1_O_K
psi: mathcal Y' -> mathcal Y
```

be the finite flat normalization and its semistable minimal resolution.
The algebraic point `b` above `a` is still `K`-rational and gives a
section `P'` of the proper regular model `mathcal Y'`.

This step is an EXISTENCE step in a height proof. No bound on `[K:K0]`,
no algorithm for producing `K`, and no size bound for the model is
claimed. Every intersection and archimedean sum is divided by `[K:Q]`,
and the source's stable quantities are independent of this enlargement.

Let `K_Y'=div(pi^*dt)` on `mathcal Y'`. Its generic support is CONTAINED
in `pi^-1(B union {infinity})`; equality need not hold. Because
`a notin B union {infinity}`, the section is not contained in that
support, and the metric degree formula and Lemma 2.3.1 give

```
[K:Q] h(b)
 <= (P',K_Y')_fin + sum_sigma -log||pi^*dt||_Ar(sigma b).   (14)
```

For Section 4.2 choose `D` to contain every horizontal section
`beta_bar`, `beta in B`, together with the vertical branch components.
Section 4.2 permits a reduced effective containing divisor with the
map etale over its complement. This is important: the total Galois
orbit closure `B` can strictly contain the actual branch locus of a
particular cover. Alternatively one can use the actual horizontal
branch support and then enlarge the upper bound by nonnegative
intersections.

Theorem 4.3.2 removes every vertical branch component of characteristic
greater than `d`. Thus in Proposition 4.2.4,

```
D1 = sum_(beta in B) beta_bar.
```

With `Q=a_bar`, that proposition gives exactly

```
(P',K_Y')_fin
 <= d*sum_(beta in B) I_fin(beta,a)
    +2d^2 log d * [K:Q].                                 (15)
```

This source result is not restricted to horizontal branch sections
which are disjoint modulo every prime. Collisions at finite primes are
precisely the intersections in (15), paid by (2).

The wild-term normalization can also be checked in the actual proof.
At a vertical component of characteristic `p<=d`, Proposition 4.1.3
and Lemma 4.2.3 bound the different by
`r_ij<=2 e_ij floor(log(d)/log(p)) e_v`. Since
`sum_j e_ij f_ij=d`, and for primes of `K` above `p` one has
`sum_v e_v f_v=[K:Q]`, summing over any subset of those primes gives

```
wild/[K:Q]
 <= 2d sum_(p<=d) floor(log(d)/log(p))*log p
 <= 2d^2 log d.
```

Use an inequality if only a subset of the primes above `p` occurs.
For `p>d`, reduced semistable fibres have vertical ramification index
one, and residue inseparability of degree at least `p` is impossible
in degree `d`. Thus the extension is tame with different exponent
`e-1=0`. This is the precise justification for the vertical-support
claim; the source's informal wording should not be read as saying
that the tame different exponent equals `e`.

Combining (2), (5), (11), (14), and (15) proves the explicit intermediate
bound

```
h(b) <= Lambda_bar +(d+1) S_a +2d^2 log d +log 800.         (16)
```

Neither a discriminant of the unknown field `K` nor an unbounded
semistable-extension degree remains in this normalized inequality.

## 5. Choosing a non-Weierstrass fibre and assembling the result

Riemann--Hurwitz gives

```
2g-2 <= -2d+r(d-1),
g <= (r-2)(d-1)/2 <= r*d.                                (17)
```

There are at most `g^3-g` Weierstrass points, including zero such
points in genus one. Hence at most `g^3-g+r` finite base values lie
in `pi(Supp Wr) union B`. Among

```
a in {1,2,...,g^3+r+1}
```

one avoids all of them. It is finite, outside the branch set, and every
point above it is non-Weierstrass. This is an explicit finite candidate
set, with

```
h(a)<=log(g^3+r+1)=O_r(1+log d).                         (18)
```

If a literal choice is desired, testing the candidates against the
finite algebraic branch set and the images of the canonical
Weierstrass divisor terminates within this bound. This proof does not
supply a uniform bit-cost bound for computing that divisor or its
images from an arbitrary presented model.

Choose any `b` above this `a`. Equations (7), (16), and (18) give

```
h(b) <= C_r d^3(d+1+h_B).                                (19)
```

By (13),

```
log||Wr||_Ar(b) <= A_g Lambda_bar + W0.                   (20)
```

Theorem 2.4.1 now applies with the SAME source height and metric
normalizations. By (17), `A_g=O_r(d^2)` and
`W0=O_r(d^2+d log d)`. Substitution of (7), (19), and (20) proves

```
h_Fal(Y)
 <= A_g h(b)+log||Wr||_Ar(b)
 <= C_r d^5(d+1+h_B).
```

No division by `g-1`, positive-genus lower bound stronger than one, or
absence of infinity from `B` has been used. The same argument covers
compact genus-one curves. For an integer `a`, the finite intersection
with the infinity section is actually zero, although the uniform
projective bound was sufficient.

## Final claim boundary and report disposition

The report's main deduction is accepted after the explicit repairs and
source checks above. Its formerly provisional atlas obligation is now
closed by the independent atlas proof. Its structural derivative
condition is closed here for that precise angular Whitney construction,
with `c0=1/800`. Its metric and Wronskian conventions have been read in
the actual source. The remaining dependence on established source
height/model theorems is stated openly, with their real hypotheses.

There is no added arithmetic model-height promise. The semistable field
and a non-Weierstrass point are used to prove an intrinsic normalized
inequality, not supplied as efficiently computable advice.

The twist family `y^2=a*x*(x-1)*(x-2)` is consistent with this theorem:
over `Qbar` all nonzero twists have the same curve isomorphism class
and stable Faltings height, while the displayed model coefficients
can have unbounded height. Therefore this result cannot alone bound
an arbitrary supplied plane model, divisor coordinates, Kummer
functions, arithmetic linearization data, or reconstruction precision.
Additional model-dependent comparison theorems and costs remain needed.

No novelty, hardness, quantum speedup, whole-paper rehabilitation, or
completed surface point-counting algorithm follows. The parent may
close the stable Faltings-height sub-obligation and should preserve the
separate coordinate/lifting/reconstruction height gates in the shared
state. No numerical control is needed to establish this inequality.
