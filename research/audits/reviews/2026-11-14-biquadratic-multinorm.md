# Three quadratic norm groups over Q — independent proof, 2026-11-14

**Claim proved.** Let a,b be independent positive squareclasses in Q*/Q*²,
let L_a=Q(sqrt(a)), L_b=Q(sqrt(b)), L_ab=Q(sqrt(ab)), and suppose
F=Q(sqrt(a),sqrt(b)) has local degree four at some place v_0. Then

    N_(L_a/Q)(L_a*) N_(L_b/Q)(L_b*) N_(L_ab/Q)(L_ab*) = Q*.

The three L's are quadratic subfields of the totally real biquadratic F.
This is a rational norm-product EXISTENCE theorem. It supplies neither
integral/S-unit factors nor a polynomial construction or prime-search clock.
The simultaneous Hilbert-symbol realization needed by the proposed proof
is valid over Q; the elementary CRT–Dirichlet argument below pays it.

## 1. Notation and local choice

Replace a,b by positive squarefree integer representatives. Write
[d,x]_v in F_2 for the Hilbert symbol (d,x)_v=(-1)^[d,x]_v.
The local Hilbert pairing is nondegenerate on Q_v*/Q_v*², and the
quadratic norm criterion is [d,x]_v=0. At an odd prime not dividing 2ab,
the classes of a,b lie in the one-dimensional unit-squareclass subgroup;
therefore a degree-four place necessarily is a finite prime dividing 2ab.
In particular there is no degree-four real place (and here a,b are positive).

Fix arbitrary t in Q*. Put g_v=[ab,t]_v. This is finitely supported and
sum_v g_v=0 by Hilbert reciprocity. We seek finitely supported h,k with

    h_v+k_v=g_v,   sum_v h_v=sum_v k_v=0,
    [a,x_v]_v=0, [b,x_v]_v=h_v,
    [b,y_v]_v=0, [a,y_v]_v=k_v.                         (1)

All possible local types are as follows; zero denotes the square class.

    a=0, b!=0: h may be arbitrary, k=0; set h=g.
    b=0, a!=0: h=0, k may be arbitrary; set k=g.
    a=b!=0:   h=k=0 and g=[ab,t]=0.
    a=b=0:    h=k=g=0.
    a,b independent: h arbitrary and k=g+h.

For the last line nondegeneracy makes the two Hilbert functionals
independent, so the maps x -> ([a,x],[b,x]) and their swapped versions
are onto F_2². Thus every listed choice has genuine local representatives.
This includes the dyadic place; no odd-residue formula is assumed there.

Take finite S containing 2, all primes dividing a,b or the numerator or
denominator of t, and v_0. Set h=k=0 outside S and at infinity. At every
place of S other than v_0 choose any allowed pair above (e.g. h=0 at
independent places). At v_0 set

    h_(v_0)=sum_{v!=v_0} h_v,   k_(v_0)=g_(v_0)+h_(v_0).

Then both sums in (1) vanish, the second because sum g=0. This is exactly
where the degree-four hypothesis is used: its two independent local
classes allow either value of h while keeping h+k=g.

## 2. Simultaneous realization over Q, including the new prime

Here is the required elementary lemma. For fixed nonzero rationals a,b,
suppose pairs A_v,B_v of Hilbert bits have finite support, are locally
realizable by a common x_v, and have separately even global parity.
Then some x in Q* has [a,x]_v=A_v and [b,x]_v=B_v at EVERY place v.

Enlarge finite S to contain 2, all primes dividing a or b, and all finite
support places. At each p in S choose a representative x_p of the desired
local squareclass, scaled by a local square so v_p(x_p)=e_p in {0,1}.
At infinity choose a compatible sign epsilon in {+1,-1}. Put

    c=epsilon product_{p in S} p^{e_p}.

The ratios x_p/c are p-adic units. At each odd p in S choose a nonzero
residue r_p mod p representing their unit squareclass. At 2 choose the
odd residue r_2 mod 8 of x_2/c. This is sufficient because an odd 2-adic
unit is a square precisely when it is 1 mod 8. Negative c is harmless:
its sign is simply included in these unit ratios.

CRT gives an invertible residue r modulo M=8 product_{odd p in S} p.
Dirichlet's theorem supplies a positive prime q congruent to r modulo M;
choose it outside S. Set x=cq. At each p in S the elements x and x_p have
the same squareclass, and at infinity x has the prescribed sign. Hence
all requested symbols at these places are correct. At every finite
v outside S union {q}, both a,b and x are units at an odd prime, so both
Hilbert symbols are +1. Consequently reciprocity separately gives

    [a,x]_q = sum_{v!=q}[a,x]_v = sum_v A_v = 0,
    [b,x]_q = sum_{v!=q}[b,x]_v = sum_v B_v = 0.

This accounts for the only possible new symbol. Since v_q(x)=1 and
v_q(a)=v_q(b)=0, it equivalently says (a/q)=(b/q)=+1: the selected
progression automatically forces q to split in both quadratic fields.
No additional Chebotarev condition or unsupported simultaneous-symbol
surjectivity is being imposed. Fractional original inputs are covered by
including their denominator primes; the Hilbert data only depend on
local squareclasses. The proof is existence, not bounded-time prime search.

## 3. Global factors and exact conclusion

Apply Section 2 first to the pair (A_v,B_v)=(0,h_v), obtaining x, and
then to (A_v,B_v)=(k_v,0), obtaining y. The local representatives in
Section 1 and the adjusted parities supply every hypothesis. Therefore

    [a,x]_v=0, [b,y]_v=0,
    [ab,t/(xy)]_v = g_v+h_v+k_v = 0   for all v.

The local-global theorem for the quadratic conic X²-dY²=zZ² says that
vanishing of all [d,z]_v is equivalent to z in N_(Q(sqrt(d))/Q)(Q(sqrt(d))*).
Here d is a nonsquare, so a rational point has Z!=0. This also explains
why the conclusion concerns field norms of possibly fractional elements.
We obtain x in N_a, y in N_b and t/(xy) in N_ab, proving the claim.
For negative t the same proof applies: a,b,ab are positive at infinity,
so all three quadratic algebras there are split and their norm is
surjective onto R*. No positivity restriction on t was inserted.

## 4. Source comparison and limits

Actual Prasad–Rapinchuk Lemma 4.8, physical LF817–865 of
`audits/sources/integral_quaternion_selection/prasad_rapinchuk.txt`, proves
failure when EVERY local degree is at most two, despite local product
surjectivity. Its LF857–862 footnote only states ONE-symbol realization;
it is not being silently promoted to the two-symbol lemma proved above.
Our degree-four hypothesis removes precisely the parity obstruction used
there. This is not a statement that all biquadratic choices work.

Actual Page LF116–152 of `audits/sources/integral_quaternion_selection/page.txt`
states strong approximation and the integral Eichler norm theorem for
indefinite quaternion maximal orders. Neither supplies integral factors
for this argument: c,q and the rational norm preimages need not preserve
any preassigned support/order. Conversely our rational proof does not
establish those integral conclusions or an integral quaternion generator.
A compact solver for the product etale algebra L_a x L_b x L_ab, or an
expanded algorithm, remains a separate algorithmic composition. No
extension of this elementary proof to general base fields is claimed.
