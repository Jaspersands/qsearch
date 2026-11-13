# A ramified ternary pair needing four binary BONG moves

2026-11-13. Independent exact falsifier. STATE/TRAPS, the 174-line word
review, DYADIC_QUADRATIC_ORDER_NORMS, and the actual Beli classification
source were read. No network, API, Git, archives, or shared-status edits.
A bounded exact Sage search found this example; the proof below stands
without that search. One isolated verification control is retained.

**Disposition: REFUTED.** Neither of the two proposed three-move words
connects every isometric ternary good-BONG pair. The following native pair
requires exactly FOUR adjacent binary scaling moves, even allowing unit
square rescalings for free. This does not refute four-word completeness,
a polynomial longer-word compiler, or any local-isometry algorithm.

## 1. Explicit native matrices and local arithmetic

Let K=Q(pi), pi^2=2, O_K=Z[pi], and F=K_(pi)=Q_2(sqrt(2)). Normalize
v(pi)=1, so e=2 and the residue field is F2. Put

    r=1+pi,  s=1+2pi=1+pi^3,  delta=5,
    A=diag(1,r,pi^3),
    B=diag(s,delta*r*s,delta*pi^3)
     =diag(1+2pi,25+15pi,10pi).

These are explicit nonsingular integral Gram matrices. Their displayed
orthogonal bases are good BONGs, with the SAME valuations R=(0,0,3).
Indeed the norm generator at each step has the smallest remaining valuation,
and R1<=R3. Both are indefinite, of signature (1,2), at pi=-sqrt(2), and
positive definite at the other real embedding. Thus the example lies in the
native totally-real indefinite ternary input model, with a ramified dyadic place.
Set C=-a1*a2=-r, D=-a2*a3=-r*pi^3. The target endpoint ratios are x=s,z=5.

The needed defects and symbols are

    d(r)=d(C)=1,  d(s)=3,  d(5)=4,  d(D)=0,
    (C,s)=-1,    (D,5)=-1,         (s,5)=+1.          (1)

Here is an elementary certificate for the nontrivial entries. Every unit
square modulo pi^2 is 1, giving d(r)=d(-r)=1. Modulo 4=pi^4 the unit squares
are exactly {1,3+2pi}; nonunit squares are {0,2}. Since s-1=pi^3 but s is
not a unit square modulo 4, d(s)=3. The polynomial Z^2-Z-1 is irreducible
modulo pi and has unit derivative; its root generates the unramified
quadratic extension, with discriminant 5. Thus 5 is the unramified class,
d(5)=2e=4, and (a,5)=(-1)^v(a). This proves the last two symbols in (1).

To prove (C,s)=-1, suppose p^2+r*q^2=s with p,q in F. If their minimum
valuation is negative and unequal, the norm has negative even valuation.
If both have the same negative valuation t, divide by pi^t: for units p0,q0,
p0^2+r*q0^2 has valuation exactly 1, because -r has defect 1. The original
norm then has valuation 2t+1<0. Hence a unit norm requires integral p,q.
Both cannot be units (the norm would have valuation 1), or both nonunits.
Using the two square sets above, every possible unit norm modulo 4 belongs to

    {1, 3+2pi, 1+pi, 3+pi}.

The target s=1+2pi is absent. Hence s is not a norm from F(sqrt(C)), as claimed.
No numerical p-adic approximation or heuristic Hilbert-symbol test is used.

## 2. Actual isometry certificate from Beli's theorem

Primary: audits/sources/2026-11-13-expanded-norm/beli_classification.txt.
Good-BONG existence/valuation conditions are LF85–97; the sub-BONG replacement
is LF107–109; Theorem3.1 is LF680–686; the binary criterion is LF980–997.
All source locators here are physical LF lines.

For a binary adjacent pair with valuation difference u, write

    h=min(e+u/2, u+d(C)),  k=min(e+v/2, v+d(D)),
    alpha1=min(h,u+k),    alpha2=min(k,v+h).

Here u=0,v=3, so h=1,k=3 and (alpha1,alpha2)=(1,3).
For B, the corresponding product classes are C*z and D*x, up to squares.
Multiplying C by 5 preserves defect 1; D*x still has odd valuation. Thus B
has the SAME alpha invariants. The prefix defects required by Theorem3.1(iii)
are d(x)=3>=1 and d(z)=4>=3. Also det(B)/det(A)=(5s)^2, and the ternary
Hasse difference is (C,x)(D,z)(x,z)=(-1)(-1)(+1)=+1, by (1).
The rational quadratic spaces are therefore isometric over F. Finally,
alpha1+alpha2=4=2e, so the STRICT inequality in condition(iv) is false and
no additional representation condition is required. Theorem3.1 proves that
the integral lattices are isometric. Failed words are not being confused
with nonisometry. Section4 gives a second, constructive four-move certificate.

## 3. BOTH three-move words fail for every parameter

An adjacent move ij(eta) multiplies BOTH norms by the unit eta. The exact
binary criterion is eta in U_alpha intersect N(-a_i*a_j), where U_alpha is
the unit-squareclass defect filtration. Work modulo squares throughout;
free rescaling of individual BONG vectors cannot change any obstruction.

For 23(t),12(x),23(z/t), the FIRST move has alpha=k=3, so d(t)>=3.
Since d(s)=3, the Hilbert filtration rule gives (s,t)=+1: the defect sum
is >2e=4. The middle pair's product class is C*t, and consequently

    (C*t,x)=(C,s)(t,s)=-1.

Thus the middle move is impossible, regardless of the final move.

For 12(t),23(z),12(x/t), the middle product class is D*t. Every permitted
t is a unit, so v(D*t) is odd. The unramified norm character gives

    (D*t,z)=(D*t,5)=-1.

Thus this middle move is impossible for EVERY possible first move.
Consecutive moves on the same pair merge because that pair's ratio and
binary group are unchanged. Every word of length at most three therefore
reduces to one of these alternating words, with identity moves allowed.
The obstruction rules out all such words, not merely a failed chosen seed.

## 4. Four moves DO suffice for this example

Use the exact unit multipliers

    12(r), 23(s), 12(r*s), 23(delta*s).                 (2)

The first and third moves have threshold 1 and satisfy their norm conditions
by (-r,r)=+1 and (-r*s,r*s)=+1. For the second, its product class is -pi,
and s=1+pi^3=Norm_(F(sqrt(-pi))/F)(1+pi*sqrt(-pi)); its threshold is 3.
For the last, the product class is E=-r*s*pi. Its valuation is odd, so
(E,delta)=-1. Moreover

    (E,s)=(C,s)(s,s)(pi,s)=(C,s)(-pi,s)=-1.

Hence (E,delta*s)=+1, and d(delta*s)=3 meets the threshold 3.
The already proved quadratic-order unit-norm compiler realizes each move
inside the ACTUAL adjacent binary lattice; Beli's sub-BONG lemma embeds it.
The resulting norm tuple is

    (r^2*s, delta*r^3*s^3, delta*pi^3*s^2).

Rescale its three vectors by 1/r,1/(r*s),1/s, respectively. These are units,
and the result is exactly B. Thus the minimum adjacent scaling-word length
for this pair is four. No free nonadjacent lattice summand was assumed.

## 5. Retained exact control and bounded extension

Control: audits/controls/ramified_three_word/verify.py and result.json,
run with /opt/anaconda3/envs/qsearch-cas/bin/python through the prescribed
/opt/anaconda3/bin/python driver. It verifies the local Hilbert matrix,
defects, all Theorem3.1 conditions, both empty three-word parameter sets,
and every move in (2). An initial discovery-only script needed one routine
Sage coercion repair for the empty generator product; the retained control
uses explicit field coercion and passes.

The optional cheapest extension used ONLY this same fixed valuation and
determinant squareclass graph. Its 16 Beli-isometric states are connected,
and its exact graph diameter is 4 (start-distance counts 1,4,5,4,2).
Thus this one graph gives no >4 counterexample. It is NOT evidence for
all-field or all-valuation four-word completeness; no wider extension scan was run.
The decisive conclusion remains the explicit universal THREE-word falsifier;
any four-word theorem needs a separate all-input argument or counterexample.
