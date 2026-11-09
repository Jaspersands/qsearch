# Exact Elliptic Two-Selmer Dimension From Paid Arithmetic

Status: EXPLICIT COMPOSITION OF PUBLISHED MACHINERY,
independent core and ACTUAL-NOTE review ACCEPTED,
2026-11-06. This is not a novelty, separation or quantum execution claim.
The subsequent primary audit in Section7 finds the classical polynomial
reduction already explicit in Siksek--Smart1997. No new Selmer subsystem
or new quantum mechanism is admitted.

Subsequent source extension: ODD_GALOIS_CLASS_GROUP_COMPOSITION.md Section6
removes the class-generator GRH premise for EVERY retained irreducible
cubic, including non-Galois fields. Stark's fixed-degree zero gap pays the
random prime source; adjoin its outputs to the fixed bad-prime set S.
The compact T-unit, mod2, small-representative and local/real arguments
still apply; cubic maximal-order preprocessing was already paid. Independent
core and actual-text integration reviews ACCEPTED the extension and its
additional source-failure budget. No rank, points, covering-curve, novelty
or execution claim.

## 1. Native problem, selection and sources

Input: a monic irreducible separable cubic
f(X)=X^3+a2 X^2+a4 X+a6 in Z[X], in binary. Let E/Q be y^2=f(x),
and let b be the total coefficient bit length. The proposed primary output
is the INTEGER dim_F2 Sel^(2)(E/Q), with error <=eta. The written target
is unconditional quantum time polynomial(b,log(1/eta)), using the paid
fixed-degree class-generator source described below. It is NOT Mordell--Weil
rank, rational points, or explicit covering curves. Irreducibility is a restriction of this theorem, not advice about
class groups, units, local points or torsion.

Independent direction comparison selected this over further unconditional
class-generator work: elliptic descent is an established external task,
and one paid local-image operation could complete an arithmetic pipeline.
The corpus been-tried lookup preceded literature inspection. The baselines
lookup returned only an irrelevant reverse-isogeny-transport entry; it
does not apply here. The actual matched classical baseline is the SAME
two-descent using classical class/unit arithmetic and classical covering
methods. The class/unit comparator now includes rigorous fixed-degree
subexponential ERH arithmetic (UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md
Section4). No absence of a classical polynomial algorithm is asserted.

Primary source actually read: Michael Stoll, *Implementing 2-descent for
Jacobians of hyperelliptic curves*, Acta Arith.98 (2001),245--277,
<https://www.impan.pl/shop/en/publication/transaction/download/product/83397>.
Lemma4.1, Proposition4.2 and Corollary4.7 give the odd-degree descent
identification and finite local conditions. Lemmas4.4 and6.3 give local
dimensions and squareclass stability. Section6's original routine scans
the entire residue field, gives qualitative termination, and warns that
random searches can miss generators in tiny p-adic sets. Section4 below
is a DERIVED CUBIC REPLACEMENT with a bit clock, not a runtime theorem
quoted from Stoll. Schaefer--Stoll's *How to do a p-descent* explicitly
assumes an ODD descent prime and is not used as a p=2 certificate.

Paid quantum primitive: Biasse--Song Theorem1, compact recovery in
Section8.1 and Proposition7, and Algorithms5--6, corrected manuscript
<https://arxiv.org/abs/2510.02280v2>. These supply a COMPLETE free basis of
T-units modulo roots of unity in polynomial-size compact representation,
with bounded error. The source audit is in
ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md. Completeness is one
probabilistic event, not a certificate obtained from a few valid units.

Decisive falsifiers: a residue loop costing p; a random local source with
unpaid rare generators; integer instead of mod2 valuation kernels;
incomplete/redundant units treated as a basis; expanding huge units;
missing the dyadic or real local condition; or interpreting Selmer
dimension as rational rank. No new quantum subsystem is built.

## 2. Paid global preparation and virtual units

Put L=Q[theta]=Q[X]/f. Factor 2 disc(f) using Shor with its error budget.
An integral basis of O_L can be computed in polynomial time after this
factorization. A direct fixed-degree justification is as follows. Starting
from R=Z[theta], for each prime p dividing its discriminant compute
J=rad(pR) and replace R by (J:J) until unchanged. Mod p, the nilradical
is the kernel of the Fp-linear Frobenius-power map z->z^(p^k), p^k>=3.
Rational lattice intersections/HNF compute the idealizer, contained in
p^(-1)R. Its elements preserve a full lattice, hence are integral.

If R_p is not maximal, the finite nonzero module O_(L,p)/R_p has a
nonzero socle element x mod R_p annihilated by J. Thus Jx is contained
in R_p. Since x is integral, Jx is also in rad(O_(L,p)), whose contraction
is J; hence x is in (J:J) but not R_p. Every strict enlargement lowers
v_p disc(R) by at least2. The total index divides a number <=sqrt|disc f|,
so all HNF coordinates and the number of steps have polynomial bit bounds.
This argument includes2 and3; no loop through p residue values is used.

Let S contain all L-primes over rational primes dividing2 disc(f). Run the
classical raw prime-generator source in ODD_GALOIS_CLASS_GROUP_COMPOSITION.md
Section6 with total failure allowance1/100, and let T be S together with
its outputs. For degree3, Stark's denominator4*3!*log|disc L| is a fixed
constant times log|disc L|; the resulting prime norms have O(b) bits and
the list size is polynomial in b. Except on the budgeted source-failure
event, T generates Cl(L) without GRH. Its numerical norms need not be
small, but the compact T-unit primitive charges their LOG norms.
Computing prime decomposition from the explicit maximal order is paid
classical finite-algebra/finite-field arithmetic. No numerical class number
or class-membership oracle is needed. The original all-primes-up-to-
48 ceil(log2|disc L|)^2 factor base is a GRH alternative, not an assumption
of this updated composition.

Call the complete compact T-unit primitive ONCE. If r is the ordinary
unit rank, the free output has r+|T| elements. The actual source pays
lattice-basis extraction before compact recovery; a longer redundant list
cannot silently replace this basis. Since L is cubic, its roots of unity
are exactly{+1,-1}; append -1. These give a basis of U_T/U_T^2.

Let V be the integer valuation matrix at T\S. Then

    L(S,2) := {a in L*/L*^2: v_P(a) even for P outside S}
             = ker(V mod2) inside U_T/U_T^2.                 (1)

Proof of surjectivity: write the divisor of a outside S as2A. As T
generates Cl(L), choose a fractional divisor B supported on T with
[A]=[B], and let A-B=div(gamma). Then a/gamma^2 has divisor supported
on T. For injectivity, a square root in L of a T-unit is itself a T-unit.
Thus(1) includes class-group2-torsion without supplied Cl(L)[2] generators.
The INTEGER kernel would be wrong: a nonprincipal order2 ideal with
P^2=(a) contributes even nonzero valuations, not a zero valuation vector.

Impose the norm-square condition using residue-degree-weighted valuation
rows at all rational primes below T, plus the real sign of Norm(a).
Stoll's identification for odd degree is

    H^1(Q,E[2]) = ker(N:L*/L*^2 -> Q*/Q*^2).                (2)

The rows use the ORIGINAL T-unit valuations. This norm condition, (1),
and the local images at S and infinity describe exactly Sel^(2), by the
actual Corollary4.7; using all prime divisors of2 disc(f) is a harmless
superset of its required places.

## 3. Small representatives and local arithmetic

Choose compact base2. The source's representation
a=gamma0 gamma1^2 gamma2^4 ... gives [a]=[gamma0] in L*/L*^2, with
gamma0 of polynomial height. More generally, reduce every compact
power-product exponent modulo2, then multiply the polynomially many small
factors. This has polynomial bit length. Multiplication of basis elements
selected by an F2 vector also stays polynomial. Clear denominators by a
rational SQUARE if integral coordinates are convenient.

The resulting small representative need not be a T-unit; it can have
EVEN valuations outside T. Therefore do not recompute(1) from its raw
support or discard it on that account. The original unit valuation matrix
supplies the global parity data. This is squareclass reduction, not
expansion of a huge unit or a small representative of that SAME unit.

At each p, write L tensor Qp=product L_i with degrees e_i f_i and sum<=3.
Local squareclass coordinates consist of valuation parity and unit class.
At odd p, the unit coordinate is the residue-field quadratic character,
computed by powering with an O(log p)-bit exponent. At2, unit squareclasses
are determined modulo pi_i^(2e_i+1). Each such residue ring has size
2^(f_i(2e_i+1))<=2^9, so exact enumeration here is a bounded constant.
All these arithmetic operations use the paid maximal order, prime ideals,
local uniformizers and finite quotient rings. They do not require a
sampled local point or a supplied local image.

Valuations and normalized residues of each small representative are
computed with precision bounded by its OWN coefficient/norm bit length,
in addition to the field discriminant. Do not transfer the smaller local
image precision bound below to an arbitrary larger input representative.
Ideal-power membership/HNF and repeated squaring supply the required
polynomial bit algorithms. Fixed-degree p-adic factorization or the
equivalent completion arithmetic has no enumeration over p elements.

## 4. Classical polynomial-bit local Kummer images

For Qp-rational P=(x,y) away from two-torsion,
delta(P)=[x-theta]. Include the images of ALL rational two-torsion points
first. For a root a in Qp, replace the vanishing component by f'(a), or
equivalently evaluate (a-theta)+h(theta), h(X)=f(X)/(X-a).
Stoll Lemma4.3 gives this convention. These are paid fixed-degree local
computations, with polynomial precision.

### 4.1. A bounded root tree

For odd p set F=f and Theta=theta. At p=2 use

    X=4x, Y=8y, F(X)=64 f(X/4), Theta=4theta.

F is monic integral, all its roots have v2>=2, and X-Theta=4(x-theta)
preserves the Kummer squareclass. Here D'=v2 disc(F)=v2 disc(f)+12.
At odd p put D'=vp disc(f). Nonintegral X contributes only the trivial
class: at odd p this is Stoll Lemma6.3(3); at2 both F(X)/X^3 and
1-Theta/X are in1+8O, so F(X) square forces X square and X-Theta square.
It therefore suffices to cover Zp.

A node is the ball X=c+p^k Zp. Compute the full content valuation m of
F(c+p^k T), and the primitive integral polynomial

    g(T)=p^(-m)F(c+p^k T).

Retain m parity. Find roots xi of g mod p by degree-at-most3 finite-field
factoring, and recurse on those child balls. Never enumerate all p
children at a large prime. Generic children are handled below.

The Gauss-norm factorization of primitive g shows that a generated
level-(k+1) child has an algebraic root alpha with

    vp(alpha-(c+p^k xi)) > k.                               (3)

Distinct centers modulo p^(k+1) have disjoint root sets satisfying(3).
Hence there are at most3 nodes per positive level. The STRICT inequality
is essential: fractional root distances need not be >=k+1.

Stop at depth M=D'+5. All roots are integral, so every pairwise root
separation valuation is <=D'/2. For a level-M node, its associated root
is closer to its Qp center than to every conjugate; Krasner's lemma makes
it rational. Its distance valuation is then integral and >=M. Every
point in the whole ball lies in the two-torsion tail from Stoll
Lemma6.3(2), since M>D'/2+vp(4); its image was already included. The tree
therefore has at most N=1+3M nodes, with no qualitative termination gap.

### 4.2. Odd-prime generic children

For a nonroot xi of g mod p, all valuations of X-Theta_i are fixed on
the child ball; the image and local square status are constant there by
Stoll Lemma6.3(1). Their variation AS xi VARIES is controlled as follows.

For a local factor, put h_i=v_i(c-Theta_i). Only its comparison with
k e_i is needed; a value beyond the available precision is treated as
>k e_i, not recovered exactly. Equality residues are computed only in
the bounded case. If h_i<k e_i, the unit
squareclass is constant. If h_i>k e_i, its varying residue is xi, with polynomial P_i(T)=T
and residue norm exponent f_i (even f_i gives a constant character). If
h_i=k e_i, its varying residue is xi-beta_i, with beta_i the residue of
(Theta_i-c)/p^k. Taking the residue-field norm to Fp gives its minimal
irreducible polynomial P_i(xi), raised to f_i/deg(P_i). Fixed normalized
uniformizer factors contribute only constant signs.

After deleting repetitions and even powers, there are at most3 distinct
irreducible polynomials, with TOTAL degree<=sum f_i<=3. Thus every generic
Kummer vector, and the norm-square restriction deciding whether F(X) is
a square, is determined by an affine function of their Legendre signs.
Products of distinct such polynomials are squarefree and nonsquare.
Weil's bound and character orthogonality give EVERY sign pattern at least

    p/8 - 2 sqrt(p) - 3 >= p/16,  for p>=4096,              (4)

residues, after excluding the at-most3 nongeneric roots. With
L=ceil(16 log(8N/epsilon_p)) independent uniform residues per node, the
probability of missing ANY generic pattern anywhere is <=epsilon_p.
Compute F(X)'s square status exactly locally; retain a label only if it
comes from a Qp-point. For odd p<4096, enumeration is a bounded constant.
This is stratified sampling inside each root-tree node, not unconditioned
sampling of x in Zp, which can miss tiny generator regions.

### 4.3. The dyadic generic children and certification

For each nonroot digit xi modulo2, test its four lifts xi+2j modulo8,
0<=j<4. Root distances on that child have valuation<=k. The remaining
variation has valuation>=k+3, so it is STRICTLY larger than
vp(4)+every root-distance valuation. Stoll Lemma6.3(1) makes both square
status and Kummer image constant on each subcell. There are at most8
tests per node; no dyadic density assumption is made.

Every retained label comes from a certified local square or an actual
two-torsion point, so its span is a subgroup of the true image. By actual
Stoll Lemma4.4, the required dimension is

    d_p = number of Qp-irreducible factors of f -1 + 1_(p=2).

Return a basis if that dimension is reached; otherwise return ABORT.
On correct ordinary arithmetic, every non-ABORT answer is exact. The odd
large-prime failure is bounded by(4); dyadic and small-prime coverage is
deterministic. Precision O(D'+1) suffices for these tree/torsion labels
(a conservative2D'+10 digits can be used). Each node has polynomial-bit
coordinates; M log p is polynomial in b. Cap and amplify the ordinary
finite-field/local factoring operations within the allocated error budget.

## 5. Real place, linear algebra and the final error event

If f has one real root, the real Kummer image is trivial. If its three
real roots are ordered a<b<c, it is generated by the sign pattern(+,-,-)
on the interval(a,b); the unbounded positive interval gives the identity.
Exact real-root isolation and signs of the small representatives compute
this condition in polynomial bit time. Complex components have no
squareclass coordinate. Norm sign alone must not replace this real image.

Intersect the global F2 kernel from(1)--(2) with the preimages of all
local images by Gaussian elimination. Its dimension is the desired
Selmer dimension. The number of columns, local places, finite quotient
coordinates and their bit sizes are polynomial in b. Arithmetic success
does not constitute a proof that a quantum unit list is complete; on the
ONE complete T-unit event, however, the entire calculation is exact.

Allocate total factoring/local/numerical failure or ABORT below1/20 per
run. With a complete T-unit success probability at least2/3, the correct
dimension has probability at least2/3-1/20-1/100>1/2, also allowing
the class-generator source failure. Use fresh independent
whole-output runs and majority of the CANONICAL INTEGER dimension for
error eta, at overhead O(log(1/eta)). Cap malformed outputs and every
branch at the prescribed polynomial clock. No majority of noncanonical
bases or unverified unit-completeness test is assumed. Polynomial-height
representatives exist on a correct run, but this confidence claim is for
the dimension, not an amplified canonical basis of embedded squareclasses.

The fixed-degree source replacement removes the sole former GRH premise.
Nothing here changes the meaning of the Selmer group or eliminates the
possible Tate--Shafarevich contribution. No quantum circuit was executed.

## 6. Controls, review and continuation

The parent independently checked the global kernel, exponent-parity
compression, radical-idealizer order construction and local tree/character
proof. Separate helper derivations cover global arithmetic and local
images. Independent local-section and whole-note actual-text reviews
accepted the composition, controls and prior-art scope. No remaining
review correction is open.

The parent ran one native Sage/PARI control for E:y^2=x^3-2, with
/opt/anaconda3/envs/qsearch-cas/bin/python. The polynomial and maximal
field discriminant are both-108; bnfcertify=1 and h(L)=1. The primes2,3
are totally ramified, generated respectively by theta and theta+1.
Norm(theta-1)=1; the point(3,5) has Kummer norm Norm(3-theta)=25,
and (3-theta)/(theta-1) is an exact square in L. PARI ellrank returns
[1,1,0,[[3,5]]]. Its documented identity R_upper=C-T-s, with no rational
2-torsion here and s=0, gives Selmer dimension C=1. See the actual
[PARI ellrank documentation](https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html#ellrank).
This is a certified CLASSICAL native baseline and squareclass check,
not execution of our new root-tree receiver, quantum primitive, global
T-unit kernel pipeline or a large-prime confidence experiment. No broad
scan or new runner is queued.

A second, targeted control tests a REAL dyadic falsifier rather than
adding a sweep. Let f=x^3-x^2+8x-10 (irreducible mod3, disc=-3284).
The point(x,y)=(5/4,5/8) is exact. Over Q2, f has one simple odd root
and a ramified quadratic factor whose roots have v2=1/2 by its Newton
polygon. In that quadratic completion,

    [x-theta]=[5-4theta]=[5],

because (5-4theta)/5 lies in1+{u:v2(u)>2}. The element5 is NOT a square
in a ramified quadratic extension: adjoining sqrt5 gives the unramified
quadratic extension (the integral polynomial Z^2-Z-1 is irreducible mod2).
Thus this NONINTEGRAL point has NONTRIVIAL local Kummer image. It refutes
extending the odd-prime trivial-tail rule unchanged to2; it does not by
itself prove that a particular integral-point search misses a generator.

The parent verified the point identity/discriminant/irreducibility exactly
and factored over Q2 to50 digits in Sage: local degrees[1,2], ratio square,
5 nonsquare, 5-4theta nonsquare. Sage's displayed quadratic root valuation1
uses its uniformizer normalization, i.e. v2=1/2. These p-adic computations
check the analytic witness above, not all-input coverage or a quantum run.
No new runner or broader test expansion was added.

## 7. Decisive prior-art audit and disposition

The bounded follow-up audit found a more direct primary source:
Siksek--Smart, *On the complexity of computing the 2-Selmer group of an
elliptic curve*, Glasgow Math.J.39 (1997),251--257,
[actual full text](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DBD707DAF3FCBE4AE46D0AC20E547F67/S0017089500032183a.pdf/on_the_complexity_of_computing_the_2selmer_group_of_an_elliptic_curve.pdf).
The parent read its Sections1--3, including the compact-representation
warning and the final complexity conclusion, not just its abstract.

Section1 already uses the constant size of cubic local squareclass groups
and polynomial local-solubility tests. Section2 computes the global
virtual-unit group from complete class/unit and principal-ideal arithmetic,
and explicitly requires COMPACT representations because expanded elements
can be too large. Section3 filters global generators through successive
local conditions in polynomial time. Thus the polynomial classical
reduction used by this quantum composition is PRIOR ART. The source's
historical total subexponential estimate assumes GRH plus its stated
smooth-ideal conjecture; the updated classical arithmetic comparator in
Section1 has its own ERH scope. Neither statement proves a factoring-only
classical polynomial algorithm for the same target.

The parent also read Djabri--Smart1998's direct-method discussion and
Lemma1: [original HP report mirror](https://shiftleft.com/mirrors/www.hpl.hp.com/techreports/97/HPL-97-137.pdf).
It identifies class/unit computations as the difficult global step and
uses finite local tests with the group structure, rather than necessarily
enumerating every global squareclass. Its odd-prime lemma states a
randomized polynomial local-solubility algorithm; the discussion treats
small primes separately. Simon2002's actual Sections1.2 and1.5 retain
virtual units, local quartic/conic tests and the distinction between
Selmer and rational points. These are established descent mechanisms,
not a new application invented by this repository.

The independently reviewed mathematical composition above and its explicit
compact/dyadic/error accounting are retained. They are a reuse of
published arithmetic, with no claim that this quantum substitution itself
is unpublished. No new library, benchmark campaign, local receiver
infrastructure or descent-prime/genus extension is justified by this pass.
Select an independent high-upside native mechanism or decisive classical
attack next. Full rational rank and rational points remain outside scope.

