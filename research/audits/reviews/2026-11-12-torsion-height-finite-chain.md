# Independent review: finite torsion-height transfer chain

2026-11-12. Scope: the finite model-transfer, vertical-pole graph bound,
book 9.2.5 assembly, and generic support-avoidance assertions in
`../../SURFACE_TORSION_HEIGHT_CHAIN.md`. Current `STATE.md` and `TRAPS.md`
were read. The parent argument was attacked before reading the completed
advisory report `../openai_runs/2026-11-12-native-contraction/response.md`.
The actual retained Javanpeykar and Couveignes--Edixhoven sources were
checked. Physical source lines below use `split("\n")`, not `splitlines()`.
No Git, network, API, archive, or numerical sweep was used. Commands used
`/opt/anaconda3/bin/python`.

## Disposition and boundary

ACCEPTED for the stated regular reduced semistable models, with the
normalizations made explicit below. In fact the sharper finite bound is

```
V_pi <= d*(h_Z(b)-h_Y(b)+Delta_st(C))
     <= d*(h_Z(b)+Delta_st(C)).                            (1)
```

The original anchor using `v_s(a)` is valid. The integral translation
`u=pi-(a-1)` gives an equally valid cleaner proof with `u(b)=1` and exactly
the same negative vertical valuations. Loops, genus one, repeated pole
points, and arbitrary subsequent finite extensions do not break (1).

The previously established point-height calculation genuinely bounds
`h_Z(b)` on the particular Javanpeykar normalization-resolution model;
it does not only bound the stable height `h_Y(b)`. This is essential and
is checked directly in Section 1. No bound for arbitrary extra blowups
of `Z` is asserted.

The book assembly has the proposed MINUS sign and must use
`(g/2)*log(2*pi)`, not `(g/2)*log 2`. Its terms must each be multiplied by
`d` when summing the inequalities for the degree-`d` pole divisor. Generic
support avoidance costs at most `N*g^3` bad points per forbidden point
in characteristic zero, or characteristic greater than `2g-1`.

This review admits the finite chain and the book intersection bridge.
It does not independently admit the new archimedean Green-moment lemma,
the full proposed coordinate-height theorem, any reconstruction encoding,
or construction of the models or their number fields. The earlier global
Green lower bound is used only as an explicitly identified input in the
book cross-intersection term.

## 1. Exact models and the previously hidden `h_Z` input

Let `pi:C -> P^1` have degree `d`, with `C` smooth, connected, and of genus
`g>=1`. Let `a` be an integer outside the branch set, and choose `b` above
`a`. Enlarge a field of definition to contain `b`, the specified torsion
classes, and all generic zero and pole points of `pi`; further horizontal
supports may also be split for convenience. Then apply
Javanpeykar Theorem 4.3.2 to THIS field and the given morphism. It produces,
after a further finite extension, the normalization of `P^1` in `C`, and
its regular semistable minimal resolution `Z`, with a morphism

```
pi_Z:Z -> P^1_(O_K).
```

This is the STANDARD integral target with its original coordinate. The
finite normalization map has vertical branch only in residue
characteristics at most `d`. These are source physical lines 1413--1438.
Further splitting of the finitely many bad components/nodes is harmless
as described in Section 5; alternatively absorb it into the existential
model/field choice. Write `Y` for the relatively minimal regular
semistable model over the resulting field and `f:Z -> Y` for its
birational morphism. Put `M=[K:Q]`.

For either model define

```
h_X(b) = (b,omega_(X/O_K))_Ar / M,
```

using the adjunction Arakelov metric. Javanpeykar defines `h_Y(b)` on the
minimal model at physical lines 451--459. His Lemma 2.3.1, lines 468--500,
gives the birational morphism, point-blowup factorization, and canonical
metric formula used below.

The source's actual calculation, physical lines 1569--1587, is

```
M*h_Y(b) <= (b,omega_Z)_Ar
          = (b,div_Z(d pi))_fin
             + sum_sigma -log ||d pi||_Ar(sigma b).       (2)
```

In particular the right-hand side is EXACTLY `M*h_Z(b)`. Proposition
4.2.4, physical lines 1319--1322, bounds this same finite canonical-divisor
intersection on the normalization-resolution. It does not first contract
to `Y`. Replacing the Belyi branch set by the containing branch set `B`,
as already justified in the Faltings-transfer review, gives

```
(b,div_Z(d pi))_fin/M
  <= d*sum_beta I_fin(a,beta)/M + 2*d^2*log d.
```

The established full-atlas differential estimate applies to the same
generic differential and all embeddings. Therefore, with

```
S_a = sum_(beta in B) [h(beta)+h(a)+log 2],
```

the previous proof actually yields the strengthening

```
h_Z(b) <= Lambda_bar + (d+1)*S_a
                       +2*d^2*log d + log 800.           (3)
```

This requires `b` not to lie in the generic divisor of `d pi`, which is
ensured by the unbranched finite base value `a`. The number field degree
has disappeared from (3); no size bound or algorithm for its construction
is being supplied. One cannot replace this `Z` by an arbitrary sequence
of additional smooth-point blowups and retain (3).

## 2. Contraction losses are exact and involve only smooth fibre points

The factorization theorem quoted in Javanpeykar Lemma 2.3.1 expresses
`f:Z -> Y` as a sequence of blowups of regular closed points, read from
`Y` toward `Z`. All nontrivial centres are on finite fibres. In this
sequence every centre is a SMOOTH point of the fibre:

* Both endpoints have reduced nodal fibres.
* The first blowup of a node would create an exceptional component of
  multiplicity two in the fibre.
* Its strict transform persists under every later blowup, with that same
  multiplicity, contradicting reducedness of `Z`.

Inductively, only smooth-point blowups occur; they preserve reduced nodal
fibres. In the contraction direction a smooth rational `(-1)` component
meets the remainder of its reduced fibre once, since `F.E=0` and
`E^2=-1`. It is a tail. A rational `(-2)` bridge is NOT contracted to a
singular stable model in this argument; the target remains regular.

A section of a regular semistable model cannot meet a node. In completed
local coordinates `xy=varpi`, a section through the node would give two
positive integral valuations whose sum is one. Thus it meets one
component at a smooth point, with intersection multiplicity one with the
whole fibre.

For a single smooth-point blowup `rho:X' -> X`, let `E` be its exceptional
curve, and let `epsilon_Q` be one or zero according as a section `Q`
passes through its centre. Any centre met by a section is rational over
the residue field of that base place. The exact formulas are

```
omega_X' = rho^*omega_X + E,
rho^*Q = Q' + epsilon_Q E,
(Q',E)_s = epsilon_Q,
I_X,s(Q,R)-I_X',s(Q',R') = epsilon_Q*epsilon_R.            (4)
```

Here `I_s` is the UNWEIGHTED local finite intersection and the last
formula is for generically distinct sections. The canonical metrics
agree on the complex generic curve; `E` has no archimedean contribution.
Consequently

```
M*(h_X'(Q')-h_X(Q)) = epsilon_Q*log #k(s).
```

Define `L_s(b)` as the number of these centres traversed by the successive
images of `b`. Each contribution is exactly one, even for long chains of
infinitely near points. Telescoping gives

```
sum_s L_s(b)*log #k(s)/M = h_Z(b)-h_Y(b),                 (5)
0 <= I_Y,s(b,P)-I_Z,s(b,P) <= L_s(b).                    (6)
```

For an effective horizontal divisor `H` of generic degree `e`, not
containing `b`, the same argument gives

```
0 <= I_Y,s(b,H)-I_Z,s(b,H) <= e*L_s(b).                  (7)
```

One can prove (7) without splitting `H`: the change at a centre is its
multiplicity times `epsilon_b`, and its multiplicity there is bounded
by its total intersection `e` with the fibre. Splitting horizontal
supports is therefore convenient, not essential to the finite bound.

The minimal height is nonnegative. For `g>=2`, source Theorem 2.4.1
gives `e(C)<=4*g*(g-1)*h_Y(b)`, and minimal canonical self-intersection
is nonnegative. For `g=1`, the source explicitly uses the nonnegativity
of this SAME Arakelov point height at physical line 672. This is not
the claim that stable Faltings height is nonnegative. Thus (5) is at
most `h_Z(b)` in every genus under consideration.

The distinction is indispensable: on a nonminimal genus-one model
`omega_Z^2` and `omega_Z.E` may be negative, as already documented in
the book-minimality review. Neither is assumed nonnegative here.

## 3. The anchor and the dual-graph bound

First check the parent's original anchor. Let `Z0,Pinf` denote the
horizontal zero and pole divisors of `pi`, each of degree `d`. Since
`a` is integral, the sections `a` and infinity on the standard integral
projective line are disjoint. The morphism `pi_Z` gives

```
I_Z,s(b,Pinf)=0.
```

If `a!=0`, the function `pi` is regular near the entire section `b` on
`Z`, because this section lies in the inverse image of the affine
target. Its divisor there is effective, and restriction to `b` gives

```
I_Z,s(b,Z0) <= v_s(a).
```

Here a possible effective vertical zero contribution only improves the
inequality. By (7),

```
I_Y,s(b,Pinf) <= d*L_s(b),
I_Y,s(b,Z0) <= v_s(a)+d*L_s(b).                           (8)
```

Write `div_Y(pi)=Z0-Pinf+sum_C v_C C` near the fibre at `s`. Restriction
to `b` is legitimate because `a!=0,infinity`, and gives exactly

```
v_Cb = v_s(a)-I_Y,s(b,Z0)+I_Y,s(b,Pinf) >= -d*L_s(b).      (9)
```

Thus the original proof properly charges primes dividing `a`; no hidden
assumption that `a` is a unit is present.

The paid report supplies an optional cleaner anchor, independently
checked here. Put `u=pi-(a-1)`. Integral translation is an automorphism
of the integral projective line, `u(b)=1`, and `u` has the same horizontal
poles. For every vertical valuation, `v_C(pi)<0` implies
`v_C(u)=v_C(pi)`, whereas `v_C(pi)>=0` implies `v_C(u)>=0`. Hence

```
max_C max(0,-v_C(u)) = max_C max(0,-v_C(pi)).
```

The zero divisor of `u` and `b` are disjoint on `Z`, since their base
values differ by one. The analogue of (9) follows from (7) without the
`v_s(a)` term. This translation is used ONLY for the finite proof; no
translated branch-height budget or changed archimedean moment is needed.

For either function, let `H0,Hinf` be its degree-`d` horizontal zero and
pole divisors. At each component of the minimal fibre set

```
alpha_C = (H0,C)_s >=0,
beta_C  = (Hinf,C)_s >=0,
sum_C alpha_C = sum_C beta_C = d.
```

The last equality uses reducedness of the fibre. The component
intersection matrix is minus the unit-edge graph Laplacian, so
intersection of the principal divisor with components gives

```
L_graph v = alpha-beta.                                  (10)
```

Its source vector has total positive mass at most `d`. For any edge
with `v_i>v_j`, choose a threshold strictly between these two values
and sum (10) over the superlevel vertices. Internal edges cancel, and

```
sum_(edges crossing cut) (v_high-v_low)
  = sum_(high vertices)(alpha-beta) <= d.
```

Every summand on the left is nonnegative; the selected edge drop is
therefore at most `d`. Connect a maximum vertex to a minimum vertex by
a simple path. It has at most `#vertices-1<=delta_s` edges, yielding

```
max_C v_C - min_C v_C <= d*delta_s.                        (11)
```

Self-loops contribute zero to the Laplacian and need never be used by
this path. Counting them in `delta_s` only enlarges the bound. A
one-vertex fibre has potential range zero, whether smooth or self-nodal.
Thus there is no omitted genus-one or loop case and no spectral-gap
assumption. This also supplies a precise cut proof for the electrical
argument in book Lemma 9.2.6, physical lines 9610--9628.

Combining (9) and (11), or their translated versions, gives

```
m_s(pi)=max(0,-min_C v_C) <= d*(L_s(b)+delta_s).
```

After multiplying by `log #k(s)`, summing, and dividing by `M`, (5)
proves (1), since the normalized node count on `Y` is precisely
`Delta_st(C)`.

## 4. Finite height comparison without support-etaleness

Let `Q` be a section not in the generic pole support, and first suppose
`pi(Q)!=0`. It meets a unique component `C_Q` smoothly. Pulling back
the principal divisor gives

```
v_s(pi(Q)) = I_s(Q,Z0)-I_s(Q,Pinf)+v_CQ.
```

All horizontal intersections are nonnegative. Consequently

```
max(0,-v_s(pi(Q))) <= I_s(Q,Pinf)+m_s(pi).                 (12)
```

No assumption that horizontal zero and pole closures are disjoint is
used. They can collide at finite primes. If `pi(Q)=0` generically,
the finite contribution to its projective height is zero, and (12) is
replaced by the trivial inequality `0<=I_s(Q,Pinf)+m_s(pi)`. Thus it is
not necessary to forbid generic zero points when summing the height
inequality. Generic POLE avoidance remains necessary.

For a degree-`g` effective divisor `D_t` avoiding the generic poles,
summing this finite estimate costs exactly `g*V_pi`, including all
multiplicities. The new archimedean assertion proposed to accompany
it remains the separate analytic review; (12) alone is not an
application of book 9.1.3 outside that theorem's written hypotheses.

## 5. Extension and normalization audit

All arguments may be made after a common finite extension used only
for the height proof. After a further extension of ramification index
`e` at `s`, a regular node acquires local equation `xy=unit*varpi'^e`.
Its minimal resolution inserts the usual chain of `e-1` components.
The resolution is crepant, including when the residue characteristic
divides `e`. Sections already present avoid the old nodes. The relative
dualizing line bundle commutes with the flat base change and this
crepant resolution; its normalized section height is unchanged.

On the relatively minimal model every original graph edge is subdivided
into `e` edges, so the new node count is `e*delta_s`. Original vertical
coefficients of `pi` are multiplied by `e`. Because its generic zero and
pole supports have first been split into sections, they avoid the old
nodes. The function is therefore a unit times a vertical monomial at
each old node, and coefficients on a new chain linearly interpolate the
endpoint values. Its extrema are among the endpoints. Therefore the new
`m_s` is `e*m_s`. For split
horizontal supports, the normalized finite intersections in (6) scale
in the same way. The height difference in (5) gives the corresponding
normalization for `L_s`.

Weighting by residue degrees and using
`sum_(s'|s) e_(s'/s)*f_(s'/s)=[K':K]` proves invariance of all normalized
terms in this already split situation. The archimedean sums simply
repeat embeddings. Before splitting horizontal supports, one must not
assert this interpolation argument at a node met by a horizontal zero
or pole divisor; the direct proof of (1) can instead be rerun on the
eventual chosen field/model. In particular,
one must not try to bound an UNNORMALIZED individual `m_s` independently
of ramification; that assertion is false, but is not used in (1).

This argument also explains how to impose split-component hypotheses
after obtaining the particular `Z` of (3): take compatible base change
and node resolution, whose normalized height stays the same, rather
than arbitrary extra blowups. There is no assertion that these fields
or resolutions have polynomial presentation size.

## 6. The exact book intersection assembly

Use the already reviewed book theorem on the RELATIVELY MINIMAL `Y`,
and put `D=g*b`. For a torsion class `t`, assume `h^0(t+g*b)=1`, so
`D_t` is the unique effective representative. The source hypotheses are
at physical lines 9349--9375; the bound is at 9538--9559, printed page
199 / PDF page 211. The actual PDF minus sign, already checked in the
book-minimality and theta reviews, gives

```
(D_t,P)/M + log #R^1 p_*O_Y(D_t)/M
 <= -(D,D-omega_Y)/(2*M)
       +2*g^2*Delta_st +Theta_av
       +(g/2)*log(2*pi) +(1/2)*h_Fal +(D,P)/M.             (13)
```

The logarithm of cardinality is nonnegative; generic uniqueness and
degree `g` imply generic `H^1=0`, so this is the source's finite torsion
cohomology module. Dropping the term is valid. The constants use all
complex embeddings, with the same theta and Faltings metrics as the
reviewed source bridge. In particular the paid contraction report's
`log 2` in this term and its related Noether formula are transcription
errors; both require `log(2*pi)`.

Arithmetic adjunction gives `b^2=-M*h_Y(b)`, so

```
-(D,D-omega_Y)/(2*M) = [g*(g+1)/2]*h_Y(b).                (14)
```

For each pole section `P`, (6) and disjointness on `Z` show that its
finite intersection with `b`, normalized by `M`, is at most
`h_Z(b)-h_Y(b)`. Let

```
A_pi(a)=0.5*log(1+a^2)+log(C*d)+Lambda'_bar.
```

The EXISTING global lower Green bound and
`dist_ch(a,infinity)=1/sqrt(1+a^2)` give the upper bound

```
(b,P)_Ar/M <= h_Z(b)-h_Y(b)+A_pi(a).                     (15)
```

The sign is correct because Arakelov intersection is finite intersection
MINUS the sum of logarithmic Green functions. Combining (14) and (15)
even gives the slightly sharper assembly

```
-(D,D-omega_Y)/(2*M)+(D,P)/M
 <= g*h_Z(b)+[g*(g-1)/2]*h_Y(b)+g*A_pi(a)
 <= [g*(g+1)/2]*h_Z(b)+g*A_pi(a).                         (16)
```

In genus one the `h_Y` coefficient cancels in the first line. Finally
sum (13) over all poles with multiplicities, whose total degree is `d`:

```
(D_t,Pinf)_Ar/M
 <= d*{ [g*(g+1)/2]*h_Z(b) + g*A_pi(a)
        +2*g^2*Delta_st +Theta_av
        +(g/2)*log(2*pi) +(1/2)*h_Fal }.                  (17)
```

No logarithmic-cardinality, theta, or discriminant term is omitted from
this multiplication by `d`. Formula (17) is a checked book/intersection
bridge. Inferring support-coordinate heights additionally requires the
analytic coordinate-height comparison under its own precise hypotheses.

## 7. Ordinary Wronskian support avoidance

Fix a geometric point `P` to be forbidden, a degree-zero class `t`, and
suppose the effective divisor in `|t+g*b|` is unique. Then

```
P in D_t
 <=> h^0(t(g*b-P))>0
 <=> h^0(K_C tensor t^-1(P-g*b))>0,                        (18)
```

the second equivalence being Riemann--Roch in degree `g-1`. Set
`A=K_C tensor t^-1(P)`. It has degree `2g-1` and

```
h^0(A)=g,
```

because its Serre-dual line bundle `t(-P)` has negative degree. The
order-`g` jet evaluation from this `g`-dimensional space is singular
exactly when a nonzero section vanishes to order at least `g` at `b`.
Its determinant is the ordinary Wronskian, a section of

```
A^g tensor omega_C^(g*(g-1)/2),
```

whose degree is exactly

```
g*(2g-1)+g*(g-1)^2 = g^3.                                (19)
```

It is not identically zero in characteristic zero. In characteristic
`p>2g-1`, an adapted basis at any point has distinct vanishing orders
between zero and `2g-1`; its leading Wronskian determinant is a
Vandermonde divided by factorials. Both the differences of these orders
and all relevant factorials are nonzero modulo `p`. Hence it is also
nonzero under that stated positive-characteristic hypothesis. This
proof permits base points of `|A|`; they simply contribute Wronskian
zeros. For `g=1`, the determinant is the single degree-one section,
so (19) and the exceptional-point count still hold.

Thus (18) is excluded outside at most `g^3` geometric points `b` per
pair `(t,P)`. For `N` classes and a finite forbidden set of `f` distinct
geometric points the union costs at most `N*f*g^3` points. Add the
already proved at-most-`N*g^3` uniqueness bad set and the branch values.
The images on the base cannot be more numerous than these points.
Consequently an integer

```
1 <= a <= r+N*(f+1)*g^3+1
```

avoids every bad base value, and then every point in its fibre works.
It is automatically nonzero and integral. All assertions are algebraic
and persist under embeddings and field extension; no algorithmic
splitting of all the selected divisors is being asserted.

For the pole support, `f<=d`, and `g<=C_r*d`, so

```
h(a)=log a <= O_r(1+log(d+1)+log(N+1)).
```

Together with (3), this yields exactly the parent's budget
`h_Z(b)<=C_r*d^3*(d+1+h_B+log(N+1))`. If an additional plane-chart
forbidden set has size `f` not already polynomially bounded in `d`, its
`log(f+1)` dependence must be charged separately. No unrestricted-
characteristic support-avoidance assertion is admitted.

## 8. What this review now pays

The finite vertical budget, finite support-collision comparison, and
book intersection bound are proved with the stated model and support
hypotheses. Substitution of the already checked stable discriminant
bound pays their finite quantities in fixed-branch polynomial scale;
the paid contraction report left that substitution conditional only
because its packet lacked this already completed source bridge.

In particular, for pole avoidance and
`S_N=d+1+h_B+log(N+1)`, the established input budgets and `g<=C_r*d`
give the explicit scoped consequences

```
V_pi <= C_r*d^7*S_N,
(D_t,Pinf)_Ar/[K:Q] <= C_r*d^9*S_N.
```

The second inequality uses the previously proved global Green lower
bound in (15); it is still an Arakelov INTERSECTION bound, not yet the
newly proposed absolute support-coordinate height bound.

There is no finite counterexample to the displayed parent chain under
these hypotheses. A counterexample to silently contracting rational
bridges to a singular stable model would attack a different statement:
the section-intersection change there need not be charged by canonical
height loss. Likewise, arbitrary extra blowups of `Z`, an unnormalized
ramification-independent `m_s`, or omitting the factor `d` in (17) would
invalidate proposed extensions of this proof.

The parent must still combine this scoped result with the independent
analytic review before admitting the complete displayed support-height
bound. Native model construction, a closed-divisor coordinate/jet
encoding, reconstruction precision, and a full point-counting algorithm
remain separate.
