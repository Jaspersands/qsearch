# A Paid A3 Pullback: The Entire Six-Dimensional Case Is Prior-Art Scope

27 October 2026. Mathematical reduction and novelty demotion, not a new
quantum algorithm. The final conclusion imports the published SL4
parabolic extension checked in the companion interface review.
The parent read that complete independent AI review; it accepts all four
flag types and supplies their ordinary-oracle cost accounting. It does not
independently reprove the exterior-square correspondence or audit the code.

## Question And Native Contract

The local exterior receiver includes n=3,k=1, and the older receiver
includes n=3,k=3, for V=F_q^3+F_q^3 and q odd. The n3/k2 gap was left open
by those particular constructions. Does a PAID ordinary-oracle reduction
to existing SL4 parabolic algorithms cover all three ranks already?

The answer below is yes, using the Klein exterior-square correspondence.
Input is the same coherent fixed-width oracle on O^+(6,q) or SO^+(6,q)
hiding the FULL stabilizer of an unknown nonzero totally singular U. No
basis or rank of U and no GL4 oracle are granted. Both q and label width
are charged; the ambient dimension in this result is fixed at six.

## 1. A Public One-Query Pullback

Let E=F_q^4 with public basis e1,...,e4. Identify exterior_square(E) with V
using the ordered basis

    e12, e13, e14, e34, -e24, e23.

For w with these coordinates (x,y), the coefficient of the top form in
(w wedge w)/2 is Q(w)=x.y. Define

    phi: SL4(F_q) -> SO^+(6,q),     phi(g)=exterior_square(g).

The matrix entries are signed2-by-2 minors of g. Wedge multiplication shows
Q(phi(g)w)=det(g)Q(w)=Q(w), and det(phi(g))=(det g)^3=1. Thus all calls
f(phi(g)) are legal even on the SO-only oracle. The homomorphism need NOT
be surjective for this reduction. Its kernel or image index introduces no
postselection factor.

Define the pullback oracle F(g)=f(phi(g)). A reversible circuit computes
phi(g), calls f once, and uncomputes the public matrix workspace from g.
This is one original call and poly(log q) arithmetic/gate overhead at fixed
dimension, preserving label width. No f inverse or oracle outside O/SO is
needed. An arbitrary GL4 matrix is NOT a legal replacement: its exterior
square is generally a similitude, not an isometry.

## 2. Singular Spaces Correspond To Ordinary Flags

A nonzero bivector w is singular exactly when w wedge w=0, equivalently
its alternating4-by-4 coefficient matrix has rank2. It is then a wedge
u wedge v, with associated2-space A=span(u,v), uniquely determined by its
projective line. The rank2 support can be recovered from a SUPPLIED w by
ordinary linear algebra; the oracle reduction never accesses a hidden w.

Every nonzero totally singular space U in exterior_square(E) has one of
the following unique descriptions:

| dim U | Ordinary flag in E | Reconstruction from the flag |
| --- | --- | --- |
| 1 | A of dimension2 | U=exterior_square(A) |
| 2 | a subset B, dimensions1<3 | U=a wedge B |
| 3, first family | a of dimension1 | U=a wedge E |
| 3, second family | B of dimension3 | U=exterior_square(B) |

Proof of completeness: for independent w1,w2 in U, total singularity
implies w1 wedge w2=0. Their associated2-planes intersect in a unique line
a and span a3-space B. Thus their span is a wedge B. Any further independent
decomposable w3 must have its2-plane intersecting both original2-planes.
If it contains a, independence forces its other direction outside B,
giving a wedge E. Otherwise both intersection lines are distinct and span
its plane inside B, giving exterior_square(B). This also proves uniqueness
and precludes a fourth independent singular direction. The one-dimensional
case is the rank2 coefficient criterion above.

These descriptions are equivariant for every g in GL4. In particular,
phi(g) preserves U iff g preserves the UNIQUE indicated flag. Therefore

    phi^-1(Stab_(O/SO)(U)) = Stab_(SL4)(the indicated flag).

This is the full ordinary parabolic subgroup in SL4, not its unipotent
radical, a normal core or a subgroup requiring hidden flag advice. Type
is unknown, but the existing parabolic algorithm permits unknown type.

## 3. Imported Solver And Exact Output

[Decker et al., arXiv1406.6511v2, Section8](https://arxiv.org/html/1406.6511v2)
explicitly states the extension of its parabolic algorithm to special and
projective special linear groups using techniques from
[Ivanyos, arXiv1105.4416](https://arxiv.org/abs/1105.4416).
The companion review checks how that extension uses an SL oracle rather
than granting access to a GL oracle. Keep this imported interface separate
from the elementary exterior-square proof. The numbered DIKQS Theorem1 is
GL-only; the SL parabolic statement is in Section8. Ivanyos's numbered SL
theorem is Borel-only. Cite the combination with those exact qualifications,
not either numbered theorem with an enlarged scope.

The review makes the fixed-dimension access explicit: scalar extension is
legal only on matrices whose determinants are fourth powers, of index
gcd(4,q-1)<=4. It costs one original SL query after public fourth-root
computation and cleanup. Legal additive probes and a constant-density
affine-complement sampler find a certified line in the smallest flag member.
Only THEN does determinant compensation on that known line furnish a
genuine smaller GL3 oracle. It never manufactures a full GL4 oracle before
the invariant direction is known. See the independent report for the
bounded clocks, cleanup and distinction between containment and a flag step.

Run that existing solver on F. Its recovered flag determines U by the
table, using wedge products and row reduction. If its internal convention
uses right cosets, input inversion converts f(g) to f(g^-1) with public
matrix inversion, retaining one original call. All costs remain polynomial
in log q, label width and error control. This is a reduction to a published
solver, not a claim that the solver was implemented or executed here.

## 4. Research Consequence And Boundaries

The n=3 hidden-line and maximal-space cases must NOT support a novelty
claim for the local orthogonal receiver. The missing n=3/k=2 case also has
an existing constructive route through the flag1<3; implementing another
tiny-rank receiver would not establish new algorithmic scope.

The line-only classical query lower bound remains compatible with this:
an older quantum algorithm can have the same oracle separation. Neither
passing finite controls nor proving the separation establishes novelty.

This reduction is specific to exterior_square(F_q^4) in dimension6.
It does NOT subsume the variable-Witt-rank n>=4 receiver, does not produce
a GL oracle from a general O/SO oracle, and does not turn a public linear
representation embedding into a general HSP reduction. Do not generalize
the special A3/D3 relationship to every orthogonal group.

The Denney--Moore--Russell general intersection observation is an antecedent
method, not by itself an orthogonal receiver. Its almost3-transitivity
hypothesis does not hold for the action on singular lines when n>=3:
distinct pairs may have B=0 or B!=0, an invariant distinction. This blocks
that literal application, not every possible use of their ideas. Their
SL2/PSL2/PGL2 result is not a blanket theorem for all classical groups.

Next substantial gate remains a paid prior-art reduction in VARIABLE rank,
or a useful natural input supplying the ordinary full-stabilizer oracle.
No claim that either has been ruled out or supplied is made here.

## 5. Verification Scope

a3_pullback.py implements the public map, one-query oracle wrapper, and
flag postprocessing. supplied_space_to_flag is a secret-aware algebra
control ONLY and is never called by the oracle wrapper. The tests check
all730 relevant flags over F3 (130 hiddenlines,520 hiddenplanes,80 maximal
spaces), equivariance, literal opaque-label fibers, SL/SO legality and
large-prime arithmetic. They do not execute the imported quantum solver.
Verification and independent interface-review conclusions are recorded in
VERIFICATION.md and the sibling review. No outside contact is authorized.
