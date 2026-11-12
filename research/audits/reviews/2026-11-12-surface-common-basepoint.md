# Common base point for canonical degree-g representatives

2026-11-12. Independent exact review of
`audits/claude_runs/2026-11-12-closure-basepoint/response.md` against
`audits/api_inputs/2026-11-12-surface-closure/basepoint.md`, current
`STATE.md`, and the native torsion-module representation contract.
`result.json` is terminal `truncated`, `MaxTokens`, with reported usage;
the visible response stops at the start of section 6. Verdict labels and
unprinted arguments are not evidence. No Git, network, API, archive,
code, or numerical control was used.

**Disposition.** The geometric theorem, its explicit constants, and the
characteristic-3 counterexample are valid. A corrected closed-fibre-place
algorithm gives a polynomial-degree common base point and exact RR
certificates for an explicitly supplied finite set. Fixed-rank torsion
enumeration is polynomial under the already charged divisor-arithmetic
contract. This pays canonical representative choice; it pays neither a
torsion-support height nor a characteristic-zero lifting algorithm.

## 1. Exact geometric theorem and independent proof

Let C/k be smooth, projective and geometrically connected of genus g>=1,
and let T be N geometric degree-zero line-bundle classes. Assume
`char(k)=0` or `char(k)=p>2g-2`. There is a bad set of geometric points of
cardinality at most

    M = [O in T](g^3-g)
        + |T\{O}| floor(g(g-1)^2/2) <= N g^3

outside which `h^0(E(gb))=1` simultaneously for every E in T.

For g=1, the residual bundle `K-E-gb` has degree -1, so it has no
sections and every point works. For g>=2, RR and duality give

    h^0(E(gb)) = 1+h^0((K tensor E^-1)(-gb)).

Put L=K tensor E^-1, of degree d=2g-2. Its complete space of sections has
dimension r+1=g when E=O, and r+1=g-1 otherwise. At any point b, its
distinct vanishing orders satisfy
`0<=a_0<...<a_r<=d`: each jet quotient has dimension at most one, and a
nonzero global section has a zero divisor of degree d. Define
`w(b)=sum_i(a_i-i)>=0`. A bad point has `a_r>=g`, hence weight at least
one for E=O and at least two for E!=O.

Here is the complete nonvanishing issue in the Wronskian argument. Over
the algebraic closure, choose a local parameter u and local generator e
of L. After a constant basis change, write the sections as
`(c_i u^(a_i)+higher terms)e`, with c_i nonzero. Ordinary derivatives
are legitimate: du generates the local differential module on a smooth
curve. The Wronskian coefficient in degree
`sum_i a_i-r(r+1)/2` is

    (product_i c_i) det(a_i(a_i-1)...(a_i-j+1))_(i,j)
       = (product_i c_i) product_(i<j)(a_j-a_i).

Every difference is between 1 and d, so it is nonzero in characteristic
zero or p>d. Terms with j>a_i have zero leading coefficient, as required;
they do not invalidate this determinant computation. In particular the
Wronskian is not identically zero. The chain and Leibniz rules show that
it glues to a regular nonzero section of

    L^(r+1) tensor Omega_C^(r(r+1)/2),

whose local vanishing order is exactly w(b). Base points of the complete
series are allowed and included in these orders. Its total degree is
`(r+1)d+r(r+1)(g-1)`. This is `g^3-g` for E=O and `g(g-1)^2` for
E!=O. Dividing the latter by the minimum bad weight two gives the stated
floor; taking a union gives M. No independence of the bad sets is used.

The condition is strict `p>2g-2`, not a degree bound on an incomplete
subseries, and not merely separability of some unrelated map. It proves
the finiteness needed for the algorithm uniformly over every supplied T.

## 2. Characteristic-3 falsifier and descent

The report's plane quartic

    C: y^3 z + y z^3 = x^4

is smooth in characteristic 3: its three partial derivatives are
`2x^3,z^3,y^3`, with no common projective zero. It has genus three and
canonical bundle O_C(1). At an affine point (a,b), the tangent is
`y=a^3 x-b^3`; substitution gives exactly

    -x^4+a^9 x^3+a^3 x-a^12=(x-a^9)(a-x)^3.

Since the affine projection has derivative F_y=1, x-a is a local
parameter there. The contact multiplicity is at least three. At the
unique point (0:1:0), the line z=0 has contact four. Thus every point
admits a canonical divisor containing 3b, so RR gives `h^0(3b)>=2`
everywhere. This refutes the unrestricted-characteristic assertion even
for N=1 and E=O. The generic canonical orders are 0,1,3, rather than
0,1,2. Say that the ordinary Wronskian and finite bad-set bound fail;
do not infer that nonclassical/Hasse ramification theory has no divisor
formula. No optimal threshold for all genera is established.

When h^0(E(gb))=1, its one-dimensional section space gives a unique
effective geometric divisor D_E of degree g. If b and the class E are
fixed by the Galois group of a perfect definition field k', every
conjugate of D_E lies in the same complete linear system, hence equals
D_E. Therefore D_E is a rational divisor over k', represented by closed
places/ideals; its support need not split. This argument also supplies
descent when only the geometric class E was initially known to be
Galois-invariant. Automorphism equivariance requires fixing b, or the
explicit correction in section 4 below.

## 3. Corrected finite-field construction and cost

Use the report's separable plane/function-field presentation
`F(x,y)=0` over F_q, with `deg_y F=D`, `deg_x F=d_x`, and F_y nonzero.
Take its charged smooth normalization. Since F is irreducible and
separable over F_q(x),

    Delta(x)=lc_y(F) disc_y(F) != 0,
    deg Delta <= R=(2D-1)d_x.

For Delta(alpha)!=0, the fibre has exactly D distinct geometric points,
all nonsingular in this affine presentation. There are no omitted points
at infinity in that fibre: the leading coefficient is a unit and all D
roots are accounted for. At most M base values lie in x(B_T), and at
most R are excluded by Delta. A fibre outside their union consists
entirely of good points.

Use the following repair of printed variant 1:

1. Choose a positive s with `q^s>=M+R+1`, minimal subject to s>=1.
2. Enumerate exactly M+R+1 distinct base values in F_(q^s), including
   those where Delta vanishes; skip those zeros.
3. For every remaining value factor F(alpha,y) and choose ONE irreducible
   factor h of degree f<=D. Adjoin its one residue field and use the
   rational point `b=(alpha, y mod h)` over K_b=F_(q^(sf)).
4. For every E=[A_E-B_E] in the explicit list, compute exactly
   `h^0(A_E-B_E+gb)` in a field containing b and E. Accept the candidate
   only if every dimension is one. An RR generator gives the unique
   effective representative by adding its principal divisor.

There are at least M+1 nonexcluded candidates among these total base
values, so one avoids x(B_T). Every point of that fibre passes, whatever
irreducible factor was chosen. The printed demand for M+R+1
*non-discriminant* values is unnecessary and does not match its initial
field-size bound. The repaired algorithm needs no enlargement loop and
at most M+R+1 base-value trials.

The output is a geometric degree-one point after adjoining ONE residue
field, with total extension degree at most
`Ds=O(D(1+log_q(M+R+1)))`. It is not the original closed-place divisor:
using g times a degree-f closed place before that extension would give
degree gf and certify the wrong statement.

If E is represented over F_(q^c_E), its test can use degree
`lcm(sf,c_E)<=sf c_E`. These embeddings must be compatible with the
same chosen b and the supplied definitions of E. The native torsion-module
application already supplies all classes over one common field K_0;
joining K_0 with K_b has degree at most `[K_0:F_q] sf` and avoids this
ambiguity. No common field splitting the geometric supports is required.
No claim is made that arbitrary repeated joins of unrelated class fields
have polynomial total degree.

The RR cost contract must use divisor presentation size and positive/
negative degrees, not net degree alone: `A_E-B_E+gb` has net degree g
even when A_E and B_E are large. Here its positive degree is at most
delta_E+g and negative degree at most delta_E, both explicitly charged.
Field construction/embeddings, polynomial factorization, model
normalization, RR and principal-divisor/ideal arithmetic remain charged
standard algorithms; this review does not reprove their bit complexity.
Under that contract the trial count and field bounds give expected time
polynomial in

    N, g, D, d_x, max delta_E, presented model/divisor sizes,
    max c_E, log q.

For random trials, choosing `q^s>=2(M+R)` gives success probability at
least 1/2 for a uniformly drawn *total* base value, treating Delta zeros
as failed trials. Conditioning on nonzeros also works, since
`M/(q^s-R)<=1/2`. The geometric trial count has an exponential tail.
However, an expected polynomial bound for a Las Vegas subroutine alone
does NOT give such a tail for its runtime. The printed bounded-clock
claim needs independent restarts with per-run caps from Markov's
inequality (or explicit subroutine tail bounds). O(log(1/eta)) capped
independent runs then give FAIL probability at most eta and never accept
an uncertified candidate. The degree-one variant's Weil point count is
also correct, conditional on that imported bound; its gcd polynomial of
rational roots still needs charged root extraction/factorization.

## 4. Module enumeration and the actual Frobenius

For a supplied verified rank-m ell-torsion basis over the already paid
class field, with m fixed, enumerate its ell^m coefficient tuples. RR
reduction to some degree-g representative is possible at any rational
reference point by RR, even before uniqueness is obtained. Thus standard
charged group arithmetic keeps representatives bounded while the list
is built. Testing this explicit list costs polynomial in ell^m, hence
polynomial in ell at fixed m. This is an independent argument completing
only the fixed-rank obligation; the paid report stops before supplying
its section-6 argument. It does not enumerate all geometric Jacobian
torsion unless that whole set was explicitly the supplied fixed-rank T.
For growing rank, the cardinality bound still gives existence over a field
whose degree is logarithmic in N, but this review admits no efficient
global certification or unprinted lazy-certification theorem.

Write D_E^b for the canonical divisor with `[D_E^b-gb]=E`. For a
geometric automorphism sigma (including the original q-power coefficient
Frobenius), the exact formula is

    D_(sigma E)^b = the unique effective member of
                   |sigma(D_E^b)+gb-g sigma(b)|.

One RR computation gives it, PROVIDED sigma(E) belongs to the certified
T (or its uniqueness is separately certified). The same correction is
required for deck maps. If sigma fixes b, coefficient action alone is
enough. Enlarging the working field makes some power of Frobenius fix b;
it does not replace the original Frobenius whose action is required.
Changing base point from b to b' likewise requires canonicalization of
`D_E^b+g(b'-b)`. Equality of classes becomes equality of effective
divisors only after this common-base-point canonicalization and compatible
ideal/field representation.

## 5. Limited characteristic-zero consequences proved here

The report's verdict announces height and specialization conclusions,
but no corresponding proof was printed. The following narrower statements
are independently justified and must retain their hypotheses.

**Small base value, not an unqualified point-height bound.** Over a number
field, let x:C->P^1 be a given finite degree-D map. Among the M+1 rational
integers 0,...,M, one avoids x(B_T), since that image has at most M points.
Any point over that value is good and has definition-field degree at most
D. Its base value alpha has
`h(alpha)<=log(max(1,M))`. If the plane-model exclusions must also be
avoided, use 0,...,M+R and the corresponding bound
`log(max(1,M+R))`. This controls h(x(b)). It is not a coordinate or
Arakelov height bound for b without a specified height and paid comparison
constants depending on the curve/map; it gives no height bound for D_E
or torsion supports.

**Specialization under an actual extension.** Let R be a DVR, and let
`pi:C_R->Spec(R)` be a smooth proper geometrically connected genus-g
curve, with an R-section b and an actual relative degree-zero line
bundle E_R. Put L=E_R(gb). Suppose `h^0(L_special)=1`. Then RR gives
`h^1(L_special)=0`. The multiplication-by-uniformizer exact sequence
shows that multiplication is surjective on the finite R-module H^1(L),
so Nakayama gives H^1(L)=0. Consequently
`H^0(L)/varpi=H^0(L_special)`. H^0(L) is finite and torsion-free over
the DVR, hence free of rank one. A generator reduces to a nonzero
section and gives a relative effective Cartier divisor whose generic
and special fibres are the respective unique degree-g divisors.
There is no vertical component; equivalently, the generator and varpi
are a regular sequence locally. Its zero scheme is therefore finite
flat of degree g, and the generic canonical divisor specializes to the
special canonical divisor.

This proves compatibility once the curve, section and line bundle have
already extended. It neither constructs a lift from finite-field torsion,
nor bounds extension/model heights, torsion-support heights or the cost
of characteristic-zero recovery.

**Claim gates remain false:** whole classical surface closure, supplied
torsion lifting, uniform arithmetic/support height, unchanged coefficient
Frobenius at a moving b, efficient certification of growing-rank torsion,
or any conclusion from unprinted report sections. Parent handoff/state
should record the exact geometric lemma and corrected finite-field
certificate as paid; subsequent lifting and height obligations remain
separate. No finite parameter sweep is needed for this exact argument.
