# Four adjacent binary BONG moves: an exact polynomial compiler

13 November 2026. STATE/TRAPS, the retained binary/three-word proof, actual
Beli Section5 and Theorem3.1, and the separate exact ramified counterexample
were read. No network, API, Git, new controls, or shared-status edits.

**Proved:** deterministic polynomial search for every word of either alternating
orientation of length at most four, with actual coordinate realization of a
successful word. **Not proved:** that four moves connect every isometric
ternary good-BONG pair. The strict high-alpha subcase is complete with two.

## 1. Native interfaces and notation

Let F be the supplied growing-degree dyadic completion, v(pi)=1, e=v(2),
residue degree f. Let a_i,b_i be good-BONG norms of the actual lattices,
v(a_i)=v(b_i)=R_i, R_1<=R_3. The local arithmetic, Hilbert fingerprints,
unit-squareclass basis, defect filtration and good-BONG coordinate matrices
are the previously charged native interfaces. No unknown transporter is input.

Write V=O^*/O^*2, s=dim_F2 V=ef+1, and use multiplicative squareclass notation.
All Hilbert symbols below are bits in F2. Set

    C=-a1*a2, D=-a2*a3, m=R2-R1, n=R3-R2,
    x=b1/a1, z=b3/a3,
    H(b)=min(e+m/2, m+b), K(a)=min(e+n/2, n+a),
    h(q)=H(d(C*q)),       k(p)=K(d(D*p)).              (1)

For infinity use H(infinity)=e+m/2, K(infinity)=e+n/2. U_r is the unit
squareclass subgroup of defect >=r: U_r=V for r<=0, U_r={1} for r>2e.
Half-integer thresholds use the next integer; unsupported defect levels may
simply have empty strata. Source: Beli physical LF26--40 and LF980--997 in
`sources/dyadic_seed_selection/beli_classification.txt`.

Determinant matching gives b2/(a2*x*z) a unit square. Equality of rational
ternary Hasse invariants is exactly

    <C,x> + <D,z> + <x,z> = 0.                       (2)

The already proved binary-order norm operation realizes an adjacent move
ij(eta) iff eta is in U_alpha intersect N(-a_i*a_j). This uses the actual
binary BONG lattice, then Beli's adjacent-sub-BONG replacement; it does not
assume an orthogonal lattice summand. See the 174-LF dyadic seed review,
Sections1--2, and `DYADIC_QUADRATIC_ORDER_NORMS.md`.

## 2. Exact four-word equations

Consider

    12(t), 23(u), 12(x/t), 23(z/u),       t,u in V.    (3)

The cumulative endpoint squareclass coordinates are
(1,1), (t,1), (t,u), (x,u), (x,z). The four filtration conditions are

    t in U_h(1),  u in U_k(t),
    x/t in U_h(u),  z/u in U_k(x).                   (4)

The four norm conditions before simplification are

    <C,t>=0,       <D*t,u>=0,
    <C*u,x/t>=0,   <D*x,z/u>=0.                     (5)

Using symmetry/bilinearity and (2), these are EQUIVALENT to

    <C,t>=0,  <D*x,u>=<C,x>,  <t,u>=<D,u>.          (6)

In particular the last condition of (5) is automatic, not silently dropped:
<D*x,z>=<C,x>, and the second linear condition in (6) pays it.
No division by 2 or nondegeneracy of the restriction to V is used.

## 3. Exact-defect strata turn (4) into affine conditions

Enumerate a=d(D*t), b=d(C*u) in {0,1,...,2e,infinity}. Redundant empty
levels cost only O(e^2) branches. If v(D) is even, regard D as a unit
squareclass by removing its even uniformizer power. For finite a the exact
condition is

    t in D*U_a,    t NOT in D*U_(a+1);               (7)

for a=infinity it is the singleton t=D. If v(D) is odd, ONLY a=0 is
possible, and it imposes NO coset condition or exclusion on the unit t.
Indeed every D*t then has odd valuation and defect zero. The same rules
apply to C,u,b. Imposing D*U_0 in the odd-valuation case would be an error.

For even-valuation C,D and finite a,b, form the affine spaces

    T = U_h(1) intersect x*U_H(b) intersect D*U_a
                       intersect {t:<C,t>=0},
    W = U_K(a) intersect z*U_k(x) intersect C*U_b
                       intersect {u:<D*x,u>=<C,x>}.  (8)

Use the singleton/no-condition replacements just stated in the other cases.
The remaining exclusions are D*U_(a+1) and C*U_(b+1), respectively, when
the corresponding defect is finite and its coefficient has even valuation.
These spaces and exclusions are computed by F2 row reduction.

For any forbidden affine coset E=v+L, choose a basis l_1,...,l_j of the
annihilator of L, j<=s. Its complement is the UNION of the affine conditions

    l_i(w)=1+l_i(v),       1<=i<=j.                  (9)

Branch on one violated equation for each exclusion. This is exact even when
the coset intersects an existing affine space nontrivially. Empty intersections
are dropped; E=V gives no permissible branch; no exclusion gives one branch.
There are at most (s+1)^2 branch pairs, not 2^s or q choices.

## 4. One bilinear equation is solved explicitly

On a nonempty branch write

    t=t0+sum_i alpha_i*t_i,  u=u0+sum_j beta_j*u_j

in additive F2 coordinates. The last condition in (6) is

    F(alpha,beta)=c + sum_i A_i alpha_i + sum_j B_j beta_j
                         + sum_ij M_ij alpha_i beta_j = 0,
    c=<t0+D,u0>, A_i=<t_i,u0>,
    B_j=<t0+D,u_j>, M_ij=<t_i,u_j>.                 (10)

If c=0, the two base points work. If c=1 and some A_i or B_j is 1, turn
on just that coordinate. If all linear coefficients vanish but M_ij=1 for
some pair, turn on exactly alpha_i,beta_j. If every coefficient vanishes
and c=1, this branch has no solution. These alternatives are exhaustive.
This is a bilinear polynomial on two independent affine parameter sets;
it is not a general system of quadratic equations in squareclass coordinates.

Hence the search is NECESSARY AND SUFFICIENT for (3). Perform the same search
after exchanging the edge triples (C,m,x) and (D,n,z). It tests

    23(t), 12(u), 23(z/t), 12(x/u).                  (11)

This exchanges the names of the two edges and their already defined threshold
functions; it does NOT reverse the physical BONG or negate m,n. Consecutive
moves on one edge merge, since the pair's ratio/group remains unchanged.
Identity moves are allowed. Thus (3),(11) cover all words of length <=4.

## 5. Clock and coordinate output

There are at most (2e+2)^2*(s+1)^2 affine branch pairs. Row reduction and
forming (10) take O((s+1)^3) F2 operations per branch, after the Hilbert
matrix and filtration bases are available. The resulting bound
O((e+1)^2*(s+1)^5) is polynomial in the charged local degree. Valuation gaps
m,n are only compared in thresholds, never enumerated up to their size.

A returned pair of squareclasses is represented by products of at most s
stored unit generators. Use the actual unit ratios x=b1/a1 and z=b3/a3 in
the third and fourth moves, and the paid quadratic-order norm-preimage/root
operation for each move. The resulting exact tuple is (a1*x,a2*x*z,a3*z).
One unit square-root rescaling of the middle vector gives the target tuple.
Matching the two BONG coordinate frames then yields the original-basis map.

Only four moves occur. The existing bounded precision losses for unit products,
binary norm preimages, roots and BONG denominators therefore compose with a
polynomial guard. Verify det X is a unit and X^T A X=B modulo pi^M; the retained
local-offset verifier uses M=s_B+2e+3 and lifts the certified seed. Randomized
root subroutines retain their capped ABORT budgets. Exhausting all exact
branches certifies NO_WORD_4, not nonisometry. A realization ABORT is separate.

## 6. A complete subcase and the remaining theorem

Let alpha1=min(h(1),m+k(1)), alpha2=min(k(1),n+h(1)) be the rank-three
Beli invariants, equal at the target. If alpha1+alpha2>2e, then

    alpha1=h(1), alpha2=k(1),
    alpha1=h(z), alpha2=k(x).                        (12)

Indeed alpha1<h(1) would give alpha1=m+k(1), and h(1)<=e+m/2 implies
alpha1+alpha2<=m+2k(1)<2e, a contradiction. The other cases are identical.
Beli Theorem3.1(iv), LF680--686, now requires b1 to be represented by
[a1,a2], which is exactly <C,x>=0. Condition(iii) gives d(x)>=alpha1 and
d(z)>=alpha2. Consequently 12(x) is legal, and 23(z) is legal by (12)
and <D*x,z>=<C,x>=0. Thus TWO moves suffice in this strict high-alpha case.

The unresolved universal four-word claim is confined to alpha1+alpha2<=2e.
The separate exact example over Q2(sqrt2), R=(0,0,3), has alpha=(1,3): both
three-word orientations fail and the four-word compiler admits t=1+pi,
u=1+pi^3 (multipliers differing by unit squares from the displayed certificate).
Its single 16-state graph has diameter four; that is not a universal proof.

No argument here forces at least one branch of (8)--(10) to be feasible for
every isometric low-alpha pair. Beli's arbitrary-word connectivity statement
for residue size >2 supplies neither this bound nor the residue-F2 rank-three
case. His rank-four counterexample is not a rank-three obstruction. The exact
remaining task is to prove this finite affine/bilinear feasibility implication
from rank-three classification, or exhibit an isometric pair with NO_WORD_4.
