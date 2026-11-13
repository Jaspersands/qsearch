# Relative squareclasses: the exact support-obstruction kernel

2026-11-13. CLOSED WRITTEN exact lemma and fixed-quartic composition, using
the already admitted quadratic squareclass compiler and conic backend.
The odd S-class promise is unnecessary for computing the answer: it is
replaced by a finite binary obstruction kernel. The norm image can be a
PROPER subspace of the locally norm-compatible space. One exact Sage/PARI
control below demonstrates this, including an inert prime and denominators.
No growing-tower complexity or new conic backend is claimed.

Read STATE/TRAPS, QUARTIC_RELATIVE_NORM_CLASSICAL.md, the earlier kernel
proposal, and the retained support/coordinate proof. No paid report,
network, API, Git, archive, or scan was used. Only this file was written.

## 1. Exact statement and required interfaces

Let L=F(z), z^2=d, be a quadratic extension of number fields. Let S contain
all primes of F above 2 and every prime ramified in L/F. Write S_L for all
primes above S, and

    F(T,2)={a in F*/F*2 : v_P(a) is even for every P outside T}.

No condition on Cl(O_F,S)/2 is imposed. Unramifiedness implies v_P(d) is
even outside S, so [d] is a nonzero member of F(S,2). Put

    V=F(S,2) intersect N_(L/F)(L*).

The intersection is in squareclasses; F*2 is already contained in the norm
group. Suppose the following exact interfaces are available:

1. Complete explicit bases of F(S,2) and F(S union E,2), together with
   signed valuations at specified primes. For the original basis we also
   need coordinates of [d]; Section 4 pays this without a coordinate oracle
   when F is quadratic over Q.
2. A complete basis a_1,...,a_r of V in original-basis coordinates, and exact
   witnesses beta_i in L*, c_i in F* with N(beta_i)=a_i c_i^2.
3. Exact field arithmetic and a finite support list E outside S containing
   every prime below a nonzero outside-S valuation of a beta_i. Section 2
   constructs it from denominator clearing and charged integer factoring.

Let J_i in F_2^E be the outside-S parity vector of beta_i, pulled back from
F as proved below, and let

    W=image(F(S union E,2) --val_E mod2--> F_2^E),
    C=ker(F_2^r -> F_2^E/W),       c |-> sum_i c_i J_i.      (1)

Then the exact sequence is

    0 -> F(S,2)/<[d]> -> L(S_L,2) --N--> a(C) ->0,          (2)

where a(c)=prod_i[a_i]^(c_i). Corrections for a basis of C and a quotient
basis of F(S,2)/<[d]> construct a complete independent basis of L(S_L,2).
In particular

    dim L(S_L,2)=dim F(S,2)−1+dim C.                       (3)

No enumeration of either squareclass group, class group, or unit group is
part of this interface. A basis of V alone is not presumed to lift with
the required support.

## 2. Parities at split and inert primes; safe finite support

For P outside S, the norm identity has even valuation at P. At a split
prime the two valuations of beta_i therefore have the SAME parity. At
an inert prime there is one prime above P; its residue degree is 2, so its
valuation may be odd even though the norm valuation is even. Define J_i(P)
to be this common/single parity. Since the ramification index is 1, this
is precisely the parity of the pullback of a base-prime divisor. Negative
valuations obey the same statements; denominators are not discarded.

There is a useful base-field formula. Write beta=x+y z, and set
r_P=v_P(d)/2. Since the residue characteristic is odd,

    J_beta(P)=min(v_P(x), v_P(y)+r_P) mod 2.               (4)

Use v_P(0)=+infinity. After locally rescaling z by a uniformizer to make
its square a unit, and extracting the indicated minimum valuation, at
least one coefficient is a unit. In the inert case the two residue basis
elements are independent, so the remaining element is a unit. In the
split case its two residues cannot both vanish: their difference involves
2 times a nonzero square root. At least one valuation therefore equals
the minimum, and the norm identity makes the two parities equal. This
proves (4), including unequal split valuations and negative minima.

For the native fixed-degree application, write elements in an explicit
integral basis of F. Choose an integer M_0 with M_0^2 d integral; then
M_0 z is integral. For each beta_i=x_i+y_i z choose a positive integer R_i
clearing the coordinates of x_i and y_i/M_0. Thus R_i beta_i is integral
in L. Factor

    R_i * abs(N_(L/Q)(R_i beta_i)).                        (5)

Outside the rational prime factors of (5), R_i is a unit and the integral
element R_i beta_i has norm a unit, hence beta_i has valuation zero at
EVERY prime above that rational prime. Let E contain all F-primes above
all newly obtained rational primes, excluding S. Taking all such primes
is essential: a correcting element must not introduce odd valuations at
an unlisted conjugate prime. Enlarging this auxiliary list changes neither
the target S nor the answer; (1) enforces even parity on the entire list.

For quartic L the integers (5) have polynomial bit length whenever the
conic witnesses do. Their union has polynomially many distinct rational
prime factors. Factoring these intermediates is charged; factoring only
the original discriminant is not the claimed resource model.

## 3. Completeness, independence, and choice of witnesses

The elementary norm-kernel identity is the entire completeness argument.
If xi in L* has N(xi)=c^2, c in F*, and xi != −c, then

    (xi+c)^2=(Tr(xi)+2c)xi.                               (6)

Its trace factor is nonzero, since otherwise xi=−c in this separable
quadratic field. Formula (6) writes xi=gamma delta^2 with gamma in F*.
For xi=−c this is immediate with gamma=xi. If xi has even outside-S
valuations, the ramification index 1 implies that gamma does also.
Thus the norm kernel on supported squareclasses is the image of F(S,2).
The restriction kernel is exactly <[d]>: if (u+vz)^2 lies in F, then
2uv=0, so a base element becoming a square in L is a square or d times
a square. This proves the left side of (2).

For c in C, binary linear algebra supplies a product gamma of the enlarged
base-basis representatives with val_E(gamma)=sum c_i J_i. Then

    alpha_c=gamma prod_i beta_i^(c_i)

has even valuation at every prime outside S_L, including those outside E,
and N(alpha_c) has squareclass prod_i[a_i]^(c_i). This proves construction
of all the claimed norm images. The correcting sign is immaterial modulo
2, so multiplication rather than division by gamma is convenient.

Conversely, suppose alpha in L(S_L,2) has norm squareclass a(c). Set
beta=prod_i beta_i^(c_i). Then beta/alpha has square norm, so (6) writes
beta/alpha=gamma delta^2 for gamma in F*. At every outside-S prime the
ramification index is 1. Therefore gamma has parity sum c_i J_i on E
and parity zero outside S union E. Hence gamma belongs to F(S union E,2),
so sum c_i J_i lies in W and c belongs to C. This proves the reverse
inclusion with no principalization or class-group hypothesis.

Changing a conic witness multiplies it by an element of square norm;
the same identity shows its parity column changes by an element of W
after enlarging E if needed. Thus the computed norm image is independent
of the witnesses and auxiliary support. Intrinsically the quotient records
the relevant ideal classes modulo 2 in Cl(O_F,S); computing that class
group is unnecessary. When Cl(O_F,S)/2=0, W=F_2^E and the old full-V
surjectivity statement is recovered, but it need not hold otherwise.

Finally, norm images of the corrected lifts of a basis of C are independent.
Any relation among those lifts and base-field representatives first has
zero lift coefficients by applying norm, and then has zero remaining
coefficients by the restriction kernel <[d]>. Subtracting a corresponding
norm lift from any supported class leaves precisely that base-field kernel.
This proves both spanning and independence in (2)--(3).

## 4. Coordinates of [d] and the fixed-quartic bit clock

For F=Q(sqrt(Delta)), the admitted quadratic compiler returns a structured
basis: rational representatives of Q(S_Q,2)/<[Delta]>, and conic lifts
b_j of an explicit rational norm-subspace basis nu_j. It records the
coordinates of each nu_j in the signed rational prime basis.

To recover [d], compute its rational norm squareclass and solve for its
nu_j coordinates e_j. Divide d by prod b_j^(e_j), obtaining t with square
rational norm. Compute an exact rational square root c of N(t). If t=−c,
use that rational representative; otherwise (6), now for F/Q, supplies
the nonzero rational factor Tr(t)+2c. Its outside-S_Q valuations are even
because those primes are unramified and t belongs to F(S,2). Its sign and
the known-prime valuation parities give its rational squareclass. Solve
for this vector modulo <Delta> in the retained rational quotient basis.
Together with e_j this is the requested coordinate vector of [d]. It is
nonzero because d is nonsquare in F. No exponential basis enumeration or
squareclass-coordinate oracle is used. Intermediate numerator/denominator
factoring, if used in extracting rational squareclasses, is charged.

For a native irreducible quartic containing a quadratic subfield, the
existing native radical construction supplies F,d and coordinate maps.
All primes ramified in F are already among those ramified in L, so the
quadratic compiler's support hypotheses hold. The local Hilbert-symbol
matrix at S and the real places computes V: outside S an unramified local
extension has every even-valued a as a norm. Hasse--Minkowski supplies
the global quadratic norm criterion. The already checked fixed-quadratic
relative conic backend supplies the beta_i; no new relative solver is used.

There are polynomially many polynomial-bit conics, factors (5), and enlarged
base generators. Formula (4), one enlarged quadratic squareclass call, and
binary linear algebra compute (1). A product of polynomially many bounded-
height representatives has polynomial expanded coordinate size in this fixed
degree. The same holds for the corrected quartic lifts and the coordinate
recovery above. Allocate the requested ABORT bound across the finitely many
randomized certified backends. Accepted witnesses and linear relations are
checked exactly. Consequently complete native L(S_L,2) reduces to polynomially
many integer-factorization calls with a polynomial-BIT classical remainder,
for EVERY quartic with a quadratic subfield, without the odd S-class promise.
This does not address quartics lacking a quadratic subfield or growing towers.

## 5. One decisive exact control, including the inert denominator obstruction

Use F=Q(a), a^2=−14, S_Q={2,7}, and L=F(b), b^2=2. Sage 10.9/PARI,
with proof=True, returned

    disc(F)=−56,  Cl(F)=(4),  Cl(O_F,S)=(2),
    absolute polynomial L: X^4+24X^2+256,
    disc(L)=3136=2^6*7^2,  relative discriminant L/F=(1),
    dim F(S,2)=4,  dim L(S_L,2)=6.

Thus S includes 2 and ALL quartic ramification while the S-class quotient
modulo 2 is nonzero. A verified base squareclass basis is

    a_i=[−1, 2, a, (a−2)/9].

All four pass every local norm test, so dim V=4. Choose exact norm-class lifts

    beta_1=3(b−1),                      N(beta_1)=−9,
    beta_2=b+2,                         N(beta_2)=2,
    beta_3=(a/4−1)b−1/2,                N(beta_3)=a,
    beta_4=[2(a+7)−(a+10)b]/12,          N(beta_4)=(a−2)/9.

The only new rational support prime is 3. In the order
P_1=(3,a+1), P_2=(3,a+2), both base primes are INERT in L/F because 2
is nonsquare in their residue field F_3. The beta_4 coefficient valuations
(v_P(x),v_P(y)) are (1,0) at P_1 and (−1,−1) at P_2. Hence its pulled-back
parity column is (0,1): an odd denominator valuation at an inert prime.

The complete expanded base basis returned independently by Sage is

    [3, (a−2)/9, (a+7)/9, 2a−5, −1].

Its valuation matrix and the lift columns are exactly

    W_matrix = [1 0 0 0 0]       J = [1 0 0 0]
               [1 0 0 0 0]           [1 0 0 1].

Thus W=span(1,1), and the obstruction matrix is [0 0 0 1]. Its kernel
has dimension 3. The scalar gamma=3 corrects beta_1, while beta_4 cannot
be corrected into the required support. Coordinates of d=2 in the displayed
base basis are (0,1,0,0). The six resulting elements

    −1, a, (a−2)/9, 9(b−1), b+2, (a/4−1)b−1/2

have rank 6 in the independently computed complete L(S_L,2). Independently
taking relative norms of that complete PARI-based basis gives rank 3 in
F(S,2), matching C, whereas all four base classes were norm-compatible.
This falsifies unrestricted full-V surjectivity and verifies the nontrivial
obstruction correction on one complete example. It is not asymptotic evidence
for the conic/factoring clock. Class and unit computations are used ONLY for
this control, not in the proposed algorithm.

## 6. Reproducible control

Run the following with `/opt/anaconda3/envs/qsearch-cas/bin/python` (the Sage
interpreter from TOOLBOX). It was run on this one field and printed
`EXACT_CONTROL_PASS`. Every norm comparison uses `relative_norm()`;
Sage's default `norm()` instead goes to Q and is unsuitable here.

```python
from sage.all import *
proof.all(True)
Qx = PolynomialRing(QQ, 'x'); x = Qx.gen()
F = NumberField(x*x+14, 'a'); a = F.gen()
S = F.primes_above(2)+F.primes_above(7)
E = F.primes_above(3); T = S+E
RF = PolynomialRing(F, 'z'); z = RF.gen()
L = F.extension(z*z-2, 'b'); b = L.gen()
A = L.absolute_field('t'); fromA, toA = A.structure()
SA = A.primes_above(2)+A.primes_above(7)
FS, fg, ff, ft = F.selmer_space(S, ZZ(2), proof=True)
FT, tg, tf, tt = F.selmer_space(T, ZZ(2), proof=True)
LS, lg, lf, lt = A.selmer_space(SA, ZZ(2), proof=True)
base = [F(-1), F(2), a, (a-2)/9]
betas = [3*(b-1), b+2, (a/4-1)*b-F(1)/2,
         (-(a+10)*b+2*(a+7))/12]
def parity_column(beta):
    xx, yy = map(F, beta.list())
    return vector(GF(2), [ZZ(min(xx.valuation(P),
        yy.valuation(P)+F(2).valuation(P)/2)) % 2 for P in E])
J = matrix(GF(2), [parity_column(t) for t in betas]).transpose()
W = matrix(GF(2), [[ZZ(t.valuation(P)) % 2 for t in tg] for P in E])
O = W.left_kernel().basis_matrix()*J
out = [L(-1), L(a), L((a-2)/9), F(3)*betas[0], betas[1], betas[2]]
outcoords = matrix(GF(2), [lt(toA(t)) for t in out])
normcols = matrix(GF(2), [ft(F(fromA(t).relative_norm()))
                        for t in lg]).transpose()
assert F.class_group(proof=True).invariants() == (4,)
assert F.S_class_group(S=S, proof=True).invariants() == (2,)
assert FS.dimension() == 4 and FT.dimension() == 5
assert matrix(GF(2), [ft(t) for t in base]).rank() == 4
assert all(F.hilbert_symbol(t, F(2), P) == 1 for t in base for P in S)
assert W.rank() == O.rank() == 1 and O.right_kernel().dimension() == 3
assert list(O.row(0)) == [0, 0, 0, 1]
assert W*tt(F(3)) == J.column(0)
assert outcoords.rank() == LS.dimension() == 6 and normcols.rank() == 3
assert A.discriminant() == 3136 and L.relative_discriminant() == F.ideal(1)
assert [t.relative_norm() for t in betas] == [F(-9), F(2), a, base[3]]
assert all(not F.residue_field(P)(2).is_square() for P in E)
print('EXACT_CONTROL_PASS')
```
