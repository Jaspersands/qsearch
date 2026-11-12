# Independent review: logarithmic-collision Merkl atlas

2026-11-12. Core analytical review of
`../../MERKL_LOG_COLLISION_ATLAS.md`. The current `STATE.md`, actual local
Javanpeykar source, and completed paid proof report were read. No Git,
network, API call, numerical experiment, or arithmetic transfer was used.
The interpreter for commands was `/opt/anaconda3/bin/python`.

## Disposition

ACCEPTED, with the Whitney net made precise below. For every finite
holomorphic map `pi:Y -> P1(C)` of degree `d`, with `Y` compact connected
of positive genus and branch locus contained in `r>=3` distinct points,
there is a Merkl atlas for the canonical probability Arakelov measure
with

```
r1 = 3/4,
N <= C_r d(d+L),
c1 <= d^2,
M <= 500 d (4/3)^d,
L = 1+log(1/delta),
```

where `delta` is the minimum pairwise chordal distance of the specified
branch set. In particular `log M=O(d)`, uniformly in branch positions,
cover monodromy, and genus. The actual Merkl theorem therefore gives

```
sup_(Y x Y minus diagonal) gr_Y <= C_r d^3(d+L).
```

This is an analytic existence statement. There is no supplied-chart
advice, but neither this argument nor Merkl's theorem is an algorithm
for constructing or evaluating the charts from binary equations.

REPAIRED/PRECISIFIED: the parent's informal maximal-net step, clustering
count, and full-overlap comparison now have explicit definitions and
inequalities. The paid report's compressed nearest-branch argument is
replaced by the direct distance estimate below. No failed cover or
degeneration was found.

OPEN/OUTSIDE SCOPE: replacing an averaged `L` by algebraic branch height;
stable Faltings height; finite-place terms; supplied-coordinate divisor
heights; constructive arithmetic chart data; uniform lifting and CRT
reconstruction. The candidate's arithmetic paragraph is not certified by
this review. No full classical surface point-counting or quantum claim
is promoted.

## Actual source scope and conventions

The source is
`../sources/classical_surface_2026/javanpeykar.txt`, *Polynomial bounds
for Arakelov invariants of Belyi curves*, with Peter Bruin's appendix.
The relevant statements were checked directly:

* Section 2.1, physical lines 221-244: the inner product is
  `(i/2) integral omega wedge conjugate(eta)`, and the canonical measure
  is `(i/(2g)) sum omega_nu wedge conjugate(omega_nu)`, of total mass one.
  Its Green function has a `log|z(x)-z(y)|` singularity with the source's
  sign convention.
* Definition 3.1.1, lines 716-722: charts are biholomorphic to the open
  unit disk, their `r1` inner disks cover, transition derivatives are
  bounded for EVERY ORDERED PAIR on the FULL overlap, and the density
  relative to `i dz wedge d(conjugate z)` is bounded on the FULL chart.
* Theorem 3.1.2, lines 727-734, states

```
sup gr_Y <= 330N/(1-r1)^(3/2) * log(1/(1-r1))
            +13.2N c1 +(N-1)log M.
```

  It also bounds the absolute local regularized Green function for two
  points in a common `r1` inner chart. It does not bound `|gr_Y|`
  globally, which diverges at the diagonal.
* The entire appendix beginning at line 1837 was inspected, including
  its local construction, chaining lemma 6.0.11, and final proof at
  2423-2500. It starts with ANY smooth nonnegative probability measure
  on a compact connected Riemann surface. Its chart argument uses the
  four atlas conditions above. There is no extra Belyi, modular,
  arithmetic, spectral-gap, or injectivity-radius promise.

The appendix's final optimization of the displayed constants says to
check an elementary inequality numerically for variable `r1`. The
present claim needs only a universal constant at `r1=3/4`; it does not
depend on independently validating that optimization. For example, in
the preceding exact formulas one may take `r2=7/8`, let `r4` tend to one,
and use cutoff slope tending to eight. The logarithmic ratio in `c3`
is then 98 and its square-root factor is `sqrt(15)`. The elementary
bounds `log(98)<5`, `sqrt(15)<4`, and `pi>3` give `c3<500`, and the
subsequent formulas give

```
sup gr_Y <= C N + C N c1 +(N-1)log M
```

for an absolute effective `C`. Thus the needed fixed-radius dependence
also follows from the appendix before its last numerical optimization.

The paid report's reference to a false displayed surface Theorem 4.1
as being in this source is a SOURCE MIX-UP. That finding belonged to the
separate Saxena--Venkatesh surface audit. It supplies no objection to
Javanpeykar/Bruin Theorem 3.1.2 and must not be propagated here.

## 1. Coordinates and the branch charts

Use angular distance `theta` on the unit sphere. If `phi_s` is a unitary
Mobius coordinate sending `s` to zero, then

```
|phi_s(x)| = tan(theta(s,x)/2).
```

For distances at most `pi/2`, this lies between `theta/2` and `theta`.
Chordal distance is `sin(theta/2)`. Thus the angular distance between
distinct specified branch points is at least `2 delta`.

Set

```
h=delta/100,       r1=3/4,       theta0=h*r1^d.
```

The disks `D_b^+={|phi_b|<2h}` are disjoint: each has angular radius
less than `4h`, whereas their center separation is at least `2 delta`.
They contain no specified branch point other than their center.

For each component of `pi^-1(D_b^+)`, the punctured component is a
connected finite cover of a punctured disk. Such a cover is a power map.
Filling its puncture gives a single ramification point and a coordinate
`w` with

```
phi_b composed_with pi = h*w^e,
|w| < 2^(1/e),
1 <= e <= d.
```

This is an EMBEDDED coordinate disk on `Y`, not a multivalued local root
on its base. Take its subdisk `|w|<1` as a branch chart. There are at most
`rd` of them, including index-one charts above any extraneous points in
the specified branch set.

Its inner disk contains every point of that component lying above
`|phi_b|<h*r1^d`, because `e<=d`. In particular all points above
`theta(x,B)<theta0` lie in branch inner disks, since
`tan(theta/2)<=theta` at these small distances. This handles the entire
inner-hole region uniformly, without knowing individual indices.

## 2. A precise Whitney net and its count

For `s` on the sphere define

```
a(s)=min(1/4, theta(s,B)),
rho(s)=epsilon*a(s),             epsilon=1/100.
```

The function `a` is one-Lipschitz for angular distance. Let
`E={theta(s,B)>=theta0}`. Choose a maximal set `S subset E` satisfying

```
theta(s,t) >= (1/4) min(rho(s),rho(t))   for distinct s,t in S.
```

Such a finite maximal set exists: `E` is compact and every selected
radius is at least `epsilon*theta0>0`. Finiteness alone is not the desired
bound; the sharper packing argument below pays the dependence on
`theta0`.

For each `s`, use the base chart `D_s={|phi_s|<rho(s)}`. Its enlargement
`D_s^+={|phi_s|<(3/2)rho(s)}` has angular radius less than `3rho(s)`.
Since `3epsilon*a(s)<theta(s,B)`, it contains no branch point. Its
preimage has exactly `d` components, each mapped biholomorphically to
`D_s^+`. On each component the coordinate

```
z=(phi_s composed_with pi)/rho(s)
```

gives a unit chart extending to the disk `|z|<3/2`. Even the doubled
base disks avoid the branch set.

Maximality gives the required INNER coverage. For any `x in E`, either
`x in S`, or there is `s in S` such that

```
theta(x,s)<(1/4)min(rho(x),rho(s)) <= rho(s)/4.
```

These distances are small, so `|phi_s(x)|<=theta(x,s)<r1*rho(s)`.
Every lift of `x` is therefore in a Whitney inner chart. Points on the
hole boundaries belong to `E`, so no equality boundary is missed.

For the count, put angular balls `A_s=B_theta(s,rho(s)/16)` around the
selected centers. These balls are disjoint. Indeed, an intersection
would give

```
theta(s,t)<(rho(s)+rho(t))/16,
|rho(s)-rho(t)| <= epsilon*theta(s,t).
```

The second inequality implies that the larger radius is less than twice
the smaller. The first then makes `theta(s,t)` less than
`3 min(rho(s),rho(t))/16`, contradicting the separation rule.

Group uncapped centers into dyadic layers `t<=a(s)<2t`. Each `A_s` in
one layer has area at least `c epsilon^2 t^2`. Its center is within
`2t` of some `b in B`, so the ball is contained in a cap about that
branch point of radius less than `3t`. The union of these `r` caps has
area at most `C r t^2`. Disjointness gives at most `C_r` centers per
layer. Overlaps among the branch caps only reduce the area bound;
there is no disjoint-cluster assumption. The capped layer `a=1/4` has
a constant count by total sphere area.

Since `a(s)>=theta0`, the number of layers is at most

```
C*(1+log(1/theta0)) <= C*(L+d).
```

Thus `|S|<=C_r(L+d)`, and including all lifted charts and branch charts
gives `N<=rd+d|S|<=C_r d(d+L)`.

## 3. Density on the whole unit disk

Let a chart extend as an embedded disk `|z|<R`, `R>1`. For an
orthonormal global holomorphic differential `omega_nu=f_nu(z)dz` and
any `p` with `|z(p)|<1`, the disk centered at `z(p)` of radius `R-1`
lies in the enlarged chart. Subharmonic mean value and the global
unit norm give

```
|f_nu(p)|^2 <= 1/[pi*(R-1)^2].
```

The canonical density is `F=(1/(2g)) sum_nu |f_nu|^2`; hence

```
0 <= F(p) <= 1/[2*pi*(R-1)^2].
```

For a Whitney chart, `R=3/2`, so this is `2/pi`. For a branch chart,
`R=2^(1/e)` and `R-1>=log(2)/e`, giving
`F<=e^2/[2*pi*log(2)^2]`. Since `d>=2` for positive-genus `Y`, the
safe common choice `c1=d^2` works. Every inequality holds for all
points of the FULL unit disk. No boundary blowup has been ignored.

## 4. All ordered transition derivatives

Distinct branch charts do not overlap: charts above different branch
points lie over disjoint base disks, and distinct components above one
disk are disjoint.

For two Whitney charts with overlapping unit disks, their centers
satisfy

```
theta(s,t)<2(rho(s)+rho(t)).
```

Lipschitz continuity of `a` now gives
`|rho(s)-rho(t)|<2epsilon(rho(s)+rho(t))`. Their radius ratio is less
than two in either direction. In the small unitary coordinates used
here, the derivative of the Mobius coordinate change and its inverse
are bounded by two. This follows directly from

```
G(zeta)=exp(i alpha)*(zeta-a)/(1+conjugate(a)*zeta),
|G'(zeta)|=(1+|a|^2)/|1+conjugate(a)*zeta|^2.
```

The centers and chart arguments have uniformly small coordinate
moduli. Therefore both normalized Whitney transition derivatives are
bounded by four, on their FULL overlaps and on every overlapping sheet.

Now let a Whitney unit chart centered at `s` meet a branch unit chart
over `b`, and put `t=theta(s,b)`. At an overlap point with base image
`x`, one has `theta(x,b)<2h` and
`theta(s,x)<2rho(s)<=2epsilon*t`. Consequently

```
t < 2epsilon*t+2h,
t < 2h/(1-2epsilon) < 3h.
```

Because distinct branch points are at angular distance at least
`2delta`, this makes `b` the unique nearest branch point to `s`.
Also `t<1/4`, so `a(s)=t` and `rho(s)=epsilon*t`. This is the direct
nearest-branch proof; no circular use of that assertion is needed.

On the entire overlap,

```
(1-2epsilon)t < theta(x,b) < (1+2epsilon)t,
(49/100)t <= |phi_b(x)| <= (51/50)t.
```

The center belongs to `E`, so `t>=theta0`. With
`|phi_b(x)|=h|w|^e`, it follows that

```
|w|^e >= (49/100) r1^d,
|w| >= (49/100)^(1/e) r1^(d/e) >= (49/100) r1^d.
```

The relevant Mobius change has derivative between `1/2` and two on
this overlap: its zero has modulus less than `3h` and its argument has
modulus less than `h`. The chain rule therefore gives

```
|dz_Whitney/dw|
  <= 2*h*e*|w|^(e-1)/(epsilon*t)
  <= 500 d r1^(-d),

|dw/dz_Whitney|
  <= 2*epsilon*t*|w|/(e*h|w|^e)
  <= (4/49)*|w|/e < 1.
```

The last displayed constant is deliberately loose. Both ordered
derivatives are bounded, including points near the boundaries of either
unit chart. The factor `h` has canceled. Thus
`M=500d(4/3)^d` is valid and `log M<=C d`. There is no hidden
`delta^-1` in the transition charge.

## 5. Assembly and paid-report disposition

At fixed `r1=3/4`, the actual theorem is

```
sup gr_Y <= C*N +13.2*N*c1 +(N-1)*log M.
```

Substituting the independently proved bounds gives
`sup gr_Y<=C_r d^3(d+L)`. The theorem also provides its stated local
regularized bound, in THESE atlas coordinates. Relating these analytic
coordinates to a prescribed algebraic model remains a separate task.

The completed report
`../claude_runs/2026-11-12-fast-merkl-proof/response.md` is substantively
correct about the atlas. Its density normalization and both transition
directions agree with the independent proof. Its dyadic union-of-caps
argument correctly avoids a cluster-separation assumption. I do not
need or promote its optimized decimal constants: the coarser explicit
construction above proves the same claimed asymptotic statement.

Two dispositions should be recorded: its branch/Whitney nearest-center
argument needs the direct `t<1.17h` estimate before invoking its Lemma B;
the estimate is available and the conclusion survives. Its suggestion
that this Javanpeykar source contained the unrelated false surface
Theorem 4.1 is rejected as a source mix-up.

The analytic lemma removes an exponential collision-height dependence
from this particular Green-function estimate if a separately proved
arithmetic collision inequality is later substituted. It does not by
itself move the full uniform arithmetic-height gate to closed.

No finite control is required to prove this atlas. The next theorem-level
question is the exact source-to-target arithmetic transfer, including
which additional local, model-height, Wronskian, and lifting terms remain.
The parent should record the accepted geometric lemma and those open
boundaries in its handoff and state; no shared coordination file was
edited by this focused reviewer.

## 2026-11-12 addendum: a global Green lower bound from the same atlas

Independently checked consequence. For the same cover, and any points
`b,x in Y` with `pi(b)!=pi(x)`, including images at infinity,

```
gr_Y(b,x) >= log dist_ch(pi(b),pi(x))
             -log(C*d)-C_r d^3(d+L).                     (G-)
```

This is a purely analytic statement. No arithmetic intersection,
coordinate-height, or support-height consequence is claimed here.

Apply the ACTUAL Merkl theorem again to the SAME unit charts, now with
inner radius `r1'=7/8`. The inner disks still cover, since the smaller
`3/4` inner disks already did. The full-unit density and full-overlap
transition bounds are unchanged. Only the fixed-radius numerical
constant changes, so its local two-sided regularization bound is

```
|gr_Y(y,z)-log|u(y)-u(z)|| <= Lambda',
Lambda' <= C_r d^3(d+L),
```

when both points lie in a common `7/8` inner chart.

Choose a chart `u` for which `|u(b)|<3/4`, and put
`D={|u-u(b)|<1/8}` inside that chart. The CLOSED circle bounding `D`
lies strictly in `|u|<7/8`, because `|u(b)|<3/4` is strict. Therefore

```
gr_Y(b,x) >= -log 8-Lambda'           for x on boundary(D).
```

The source convention is `d* d gr_Y(b,.)=2*pi*(delta_b-mu_Ar)`.
Hence away from `b` the Green function is superharmonic: its Laplacian
is a nonpositive measure. On the compact complement of `D`, the minimum
principle puts its minimum on the boundary. Consequently the same
lower bound holds EVERYWHERE outside `D`. This is the minimum principle
with the correct sign, not a lower bound inferred from the global
upper Green estimate.

Inside `D`, the straight coordinate segment from `u(b)` to `u(x)` stays
inside the unit chart. In a branch chart the base map, in a unitary
coordinate, is `v=h*u^e`; its spherical length derivative is

```
2*h*e*|u|^(e-1)/(1+|h*u^e|^2) <= 2*h*d <= C*d.
```

In a Whitney chart it is `v=rho*u`, whose spherical length derivative
is at most `2rho<=C`. Unitary Mobius transformations preserve the
spherical metric, so these bounds also hold if an original base image
is infinity. Integrating along the straight coordinate segment and
using chordal distance at most half the angular distance gives

```
dist_ch(pi(b),pi(x)) <= C*d*|u(b)-u(x)|.
```

The local regularization lower bound thus proves (G-) inside `D`.
Outside `D`, enlarge the absolute `C` so that `C*d>=8` and use
`dist_ch<=1`; then its right-hand side is at most
`-log 8-Lambda'`. This proves (G-) there as well. Distinct base images
ensure that the logarithm is finite. The omitted equal-image case
would give only the trivial extended-real lower bound minus infinity.
