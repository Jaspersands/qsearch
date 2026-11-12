# Trace-lattice normalization, exact jets, and a bad-prime certificate

2026-11-12. Focused independent review of the parent's proposed trace-lattice
construction. Read current `STATE.md`, the completed
`audits/openai_runs/2026-11-12-native-good-model/response.md`, and actual
primary sources:

* `audits/sources/surface_torsion_selection/kozen_resolution.txt`, especially
  Sections 2.1--2.2, 3.2, 4, and 5;
* `audits/sources/surface_module_2026/bilu_borichev_eisenstein.txt`, Theorems
  6.1 and 6.3 and their proofs;
* `audits/sources/surface_module_2026/poteaux_good_reduction.txt`, Definition
  13, Theorems 3--5, and conditions C1--C5 in Section 4.

No Git, network, API, archive search, new code, or numerical control.
Interpreter if needed: `/opt/anaconda3/bin/python`. The native Jacobian-atlas
review is a separate stable artifact and is not modified here.

## Verdict and scope

The specific trace-lattice construction works, with an important addition:
the local inverse reparametrizations must be COMPOSED AS CENTERED TRUNCATED
MAPS. This gives a polynomial coefficient-bit bound for the actual local
jet matrices; a bare arithmetic-operation count would not do so.

Let `K` be a charged number field, given by an integral primitive-element
order and its exact arithmetic data. Let `F(x,y) in K[x,y]` be monic in
`y`, irreducible and geometrically integral, and separable over `K(x)`.
Write

```
d=deg_y F,      s=max_i deg_x(coeff_(y^i) F),
Delta=disc_y(F) != 0,      q=deg_x Delta.
```

The curve may be singular in its displayed plane model. With degrees
treated NUMERICALLY and with coefficient/number-field encodings charged,
one can compute, in deterministic polynomial bit time:

1. a free `K[x]` basis of its integral closure `B0` in `K(C)`, its
   multiplication table, and both generic coordinate identifications;
2. the analogous free algebra `Binf/K[u]`, `u=1/x`, and Laurent
   transition matrices between the two bases;
3. a nonzero integer `M` of polynomial bit length such that, for every
   rational prime `P` not dividing `M` and every prime of the chosen
   coefficient order above `P`, these two algebras reduce to the respective
   normalizations and their gluing gives the smooth proper reduction.

The number-field order discriminant is included in `M`; no maximal-order
calculation or integer factorization is needed. No compositum of local
residue fields is constructed. The result is for a SUPPLIED, charged
plane equation and coefficient field. It does not bound the cost or
height of constructing that equation from an upstream torsion cover.

The only local-resolution algorithm imported is Kozen's explicit
polynomial-bit passive-factorization algorithm. The exact jet, global
lattice, and reduction arguments below are additional arguments, not
claims made by that source. The other two sources support the height
and specialization checks but do not by themselves supply a global
integral basis or field-coordinate bit bound.

## 1. The finite trace lattice is the right ambient search space

Put `A=K[x]`, `O=A[y]/(F)`, and let `B` be the integral closure of `A`
in `K(C)`. The trace Gram matrix of `1,y,...,y^(d-1)` has determinant
`Delta` up to the usual harmless sign convention. If `b in B`, then
`Tr(b*y^i)` is integral over `A` and belongs to `K(x)`, hence belongs
to `A` because `A` is integrally closed. Solving the trace linear system
by its adjugate gives

```
O subset B subset Delta^(-1) O.
```

Therefore every class in `B/O` has a unique representative

```
p(x,y)/Delta(x),
p = sum_(i=0..d-1) a_i(x)y^i,      deg a_i < q.
```

There are only `d*q` scalar unknowns over `K`. This is a finite linear
search, not a nonlinear search for integral elements. When `q=0`,
`Delta` is a unit of `A`, the order is already finite etale and normal,
and this chart needs no local correction.

Factor `Delta` only squarefreely, using polynomial gcds. For a closed
root `alpha` with multiplicity `m_alpha`, and each normalization place
`Q` above it, write `e_Q=ord_Q(x-alpha)`. Since the input is monic in
`y`, both `x` and `y` are regular at every place above finite `x`.
Consequently

```
p/Delta is integral at Q
    iff ord_Q(p) >= e_Q*m_alpha.
```

Thus one needs numerator jets only, not a Laurent-series division by
`Delta`. In a local parameter `tau_Q`, impose that the coefficients of
`tau_Q^0,...,tau_Q^(e_Q*m_alpha-1)` in `p` vanish. These are LINEAR
conditions on the coefficients of all `a_i`.

The maximum required truncation order is at most `N=d*q`. The total
dimension of all these local jet targets over `K` is exactly

```
sum_Q e_Q*m_alpha*[k(Q):K] = d*q.
```

Here the sum includes all closed roots and all places above them.
There is no constraint at another finite place: the denominator is a
unit there. The resulting principal-part matrix, denoted `J`, has
`d*q` columns and at most `d*q` scalar rows over `K`, after expanding
each local residue algebra in its own basis. Its kernel is exactly
`B/O`, via division of the numerator by `Delta`.

## 2. What is taken from Kozen, including the field accounting

Kozen returns a passive-factorization tree with triangular squarefree
coefficient algebras, centered local equations, local parameters,
ramification indices, and explicit birational changes. At a terminal
leaf the local equation is

```
H(tau,w)=0,      H(0,0)=0,      c=H_w(0,0) a unit.
```

Its algorithm refines a passive component whenever a tested coefficient
is zero at some represented roots and nonzero at others. On a final
component every required nonzero coefficient is a UNIT in its finite
reduced algebra. Section 4 uses subresultants and squarefree
decompositions to avoid coefficient swell; Section 5 bounds the tree
and the products of tower degrees. This is the actual bit-complexity
algorithm, not the algebraically closed unit-cost description in
Section 3 alone.

The bound of `d` on branch/residue degrees is local over one base
place. Over all roots of `Delta` the total must be multiplied by the
degree of its squarefree part. In particular the direct sum of the
terminal residue algebras has dimension at most `d*q` over `K`.
The local algebras contain residues of rational functions on the
branch, not independently chosen splitting fields of unrelated
polynomials.

For `K=Q` this is the source's stated bit model. For a charged number
field `K=Q[theta]`, initialize the same passive representation with
the given monic relation of `theta` and the coefficient polynomials
in `theta`. This is exactly the type of triangular coefficient data
used in Section 4, now present initially instead of first appearing
at a later root choice. The tower-degree bounds acquire the factor
`[K:Q]`; subresultant matrices, squarefree refinements, and coefficient
reductions have polynomial size in that charged factor and the
given order height. There is no call to unit-cost arithmetic in an
unrepresented algebraic closure. Flatten each resulting triangular
finite algebra to its product basis using its explicit monic
relations. Its dimension and multiplication-table bit sizes remain
polynomial. This is an adaptation of the actual passive
representation, not an assumption that an arbitrary black-box field
has efficient arithmetic.

In what follows let `r` bound a leaf algebra's dimension, `L` the
length of its reparametrization chain, and `H_*` a common bound on
the bit sizes of the leaf equation, its residue constants, its
multiplication tables, and the inverse of the unit `c`. All these
are polynomial in the charged input. The inverse of `c` is obtained
by inverting its multiplication matrix; determinant bounds pay its
coordinate size.

## 3. Polynomial-bit jets: the missing calculation is explicit

### 3.1 Smooth-leaf coefficients

There is a unique series `w(tau)` with constant coefficient zero
satisfying `H(tau,w)=0`. Substituting a series and solving coefficient
by coefficient divides only by the fixed unit `c`. Up to order `N`,
the coefficients are universal polynomial expressions in the
coefficients of `H` and `c^(-1)`, of degree `O(N)`.

One way to see the degree bound is to write `w=tau*z`, divide the
equation by `tau`, and isolate its linear `c*z` term. Every remaining
nonconstant recursive term has positive `tau`-weight. A term
contributing to coefficient `tau^(N-1)` has at most `N-1` such
internal nodes and at most `N` constant leaves. Thus at most
`2N-1` coefficient/inverse factors are needed. This also bounds
denominator exponents; it is not repeated squaring with uncontrolled
degree. Truncate the equation first, and use exact common-denominator
arithmetic or reduced fractions. The operation count and coordinate
bits are polynomial in `N,r,H_*`.

### 3.2 Recovering the ORIGINAL coordinates

Kozen's Newton step chooses positive coprime integers `m,n` and a
minimal nonnegative Bezout solution

```
s*m-t*n=1,      0<=t<m,      1<=s<=n.
```

After combining its monomial substitution with the next translation
by a nonzero residue root `a`, the INVERSE transformation between
centered coordinate pairs is

```
X = u^m (v+a)^t,
Y = u^n (v+a)^s.
```

Both maps send `(0,0)` to `(0,0)`. When `m=1`, one may and the
source does take `s=1,t=0`. The initial translations by `alpha` and
the original `y`-residue are applied only after the centered chain.
There are no finite-`x` reciprocal steps for the monic model: `y`
is integral there. The infinity chart is separately made monic
before applying the same argument.

For jets modulo `tau^N`, truncate each of these polynomial maps to
TOTAL DEGREE less than `N` before composing. If `m>=N`, the first
output contributes zero. Otherwise `t<m<N`, so its surviving
coefficients involve powers of `a` of exponent less than `N`.
If `n>=N`, the second output contributes zero; otherwise `s<=n<N`.
This observation is essential: a large Newton exponent encoded in
binary never forces the computation of an enormous nonzero
constant `a^exponent` for a term that is already zero at the
requested jet precision.

Composition of centered maps preserves the `tau`-adic precision.
Moreover every monomial of degree less than `N` in a composition
of `L` such maps has at most `N` coefficient factors at each level,
hence at most `N*L` factors overall. This follows by drawing its
substitution tree: all nodes have positive arity, the number of
leaves is at most the final degree, and each of the `L` levels
has at most that many nodes. Together with the smooth-leaf bound,
this gives a polynomial bound on both coefficient numerators and
common-denominator exponents. The logarithm of the number of terms
is also polynomial in `N,L`.

For example a deliberately generous coordinate-bit bound is

```
O((N+1)^3*(L+1)^2*(r+1)^2
  *(H_*+1+log((N+2)*(L+2)*(r+2)))).
```

No sharp exponent is used later. Products of a bounded number of
elements in an explicit `r`-dimensional algebra obey the same bound
by expanding in its multiplication tables; the total number of
factors, not just the circuit depth, has been bounded above.

Finally compute the jets of `x^j*y^i` with `j<q`, `i<d` by truncated
arithmetic. The added exponent bound `q+d` is polynomial. Therefore
EVERY entry of the actual matrix `J`, in the supplied residue
algebra bases, has polynomial bit size and is computable in
polynomial time. Direct sums of these coefficient spaces suffice;
they are never put in a common splitting field.

## 4. Global basis by bounded linear systems, not growing-variable elimination

Set `Lcal=Delta*B`, viewed as an `A`-submodule of `A^d` in the
power basis. It contains `Delta*A^d`. A polynomial vector `v`
belongs to `Lcal` exactly when its componentwise remainder modulo
`Delta` belongs to `ker J`.

One could use a polynomial-matrix Hermite algorithm, but its bit
cost need not be left as an opaque import. The following elementary
construction gives an upper-triangular column Hermite basis.

Inductively, for column `j`, require entries in rows greater than
`j` to be zero. Its row-`j` entry is monic of degree `h_j`, and
its row-`i` entry, `i<j`, has degree less than the already chosen
diagonal degree `h_i`. For `h_j=0,1,...,q`, solve the affine
`K`-linear system expressing this shape and membership in `Lcal`
through the remainder map and `J`. The trial `h_j=q` always has
a solution, starting from `(Delta/lc(Delta))*e_j` and reducing
the earlier rows by existing columns. Choose the first successful
degree.

This is the usual Hermite induction: projection of the module in
the first `j` coordinate directions to its last coordinate is an
ideal of `K[x]`; the least-degree monic polynomial is its unique
generator, and the earlier columns reduce its lift uniquely.
Thus the resulting triangular matrix `H(x)` is an `A`-basis of
`Lcal`. There are at most `d*(q+1)` trials; each has polynomially
many scalar unknowns and equations. Every entry of `H` has degree
at most `q`. Kernel and affine-solution coordinates have ordinary
determinant bit bounds in the polynomial-size matrix entries.

Consequently

```
(b_1,...,b_d) = (1,y,...,y^(d-1))*H(x)/Delta(x)
```

is a polynomial-size free basis of `B`. Multiplication is explicit:
multiply its numerator vectors, reduce powers of `y` by the monic
equation, then apply `Delta*H^(-1)` to the old power-basis
coordinates. Because `B` is an algebra, the resulting coordinates
are polynomials in `x`. Compute and check these exact divisions.
Adjugate, polynomial-division, and determinant bounds give
polynomial degrees and coefficient bits. The same computations
give both generic coordinate identifications.

For later reduction it is enough to retain the membership
identities for the columns of `H`, their monic diagonal degrees,
and a nonzero rank witness for `J`. Indeed

```
deg det H = dim_K(A^d/Lcal) = rank J.
```

After these data preserve under reduction, the column module of
`H` is contained in the reduced principal-part kernel and has the
same finite colength; it must equal that kernel. Alternatively one
may retain the entire linear-algebra transcript, still of
polynomial size.

## 5. Infinity and the exact two-chart transition

Write `F=y^d+sum_(i<d) f_i(x)y^i`. Choose

```
h=max_(i<d) ceil(deg f_i/(d-i)),
u=1/x,      z=u^h*y.
```

Then

```
Finf(u,z)=u^(h*d)*F(u^(-1),u^(-h)*z)
```

is monic in `z` and has polynomial degree and coefficient size in
the original input. Apply Sections 1--4 to it. This supplies
`Binf`, the integral closure over `K[u]`, with polynomial-size
basis and multiplication table.

On `x!=0`, express `z=x^(-h)y` and convert the two bases. Since
both orders are the same normalization after localization,

```
b_inf=b_0*T(x),
T,T^(-1) in Mat_d(K[x,x^(-1)]).
```

Compute these rational matrices, cancel exactly, and verify that
their denominators are monomials in `x`. Their degree and bit
bounds follow from the already paid numerator degrees, determinant
bounds, and exact polynomial division. Verify inverse and
multiplication compatibility identities and retain them. This is
an explicit finite-free two-chart presentation, not a claim based
only on abstract existence of a proper model.

If the original plane input was not monic, one can preserve a
specified map `x` by replacing `y` with `z=a_d(x)*y`, where
`a_d` is its nonzero leading coefficient. The equation
`a_d^(d-1)*F(x,z/a_d)` is monic in `z`, with polynomial degree and
bit growth. Retain the inverse generic identification and the
nonvanishing coefficient needed for `a_d` after reduction. Thus
monicity here does not require a rational point or a field
extension; it is a paid change of generator.

## 6. One polynomial-bit integer controls reduction

Fix a power-basis order of `K`. Invert its discriminant and all
rational denominators used in the input and computed data. For
each nonzero element required to be a unit in a passive finite
etale algebra `C`, use

```
det_K(multiplication by c on C),
then its norm from K to Q,
```

after clearing its coordinate denominators. These are nonzero
determinants of polynomial-size matrices with polynomial-bit
entries. Avoiding the resulting integer makes `c` a unit in
EVERY residue component, not merely nonzero at one selected
embedding.

Include the following finite records for BOTH charts in `M`:

1. input, coefficient-algebra, local equation, jet, lattice-basis,
   multiplication-table, and transition denominators;
2. leading coefficients and squarefreeness/subresultant witnesses
   for discriminants and passive coefficient relations;
3. every nonzero comparison that determines a Kozen split, Newton
   support, unit translation, or terminal smooth derivative;
4. rank witnesses for the principal-part matrix, basis conversion
   matrices, and any retained exact linear systems;
5. the nonzero scalar in the Laurent-unit determinant of `T`,
   and the identities certifying the inverse transition;
6. the small-prime exclusion `d!` (and the analogous maximum
   degree if the preliminary monic change enlarged it).

Structural zero tests and algebraic identities survive by their
exact coefficient identities after denominator clearing; only
the required nonzero tests need additional integer factors.
For polynomial nonvanishing or degree preservation record an
appropriate nonzero coefficient or leading coefficient, rather
than trying to invert the polynomial at every value of `x`.

All lists, determinants and matrix dimensions are polynomially
bounded. Norms have polynomial bit length by determinant bounds,
and the bit length of their product is the sum of those lengths.
Thus `M!=0` is COMPUTABLE with polynomial `log|M|`. It need not
be minimal and it is never factored.

For any allowed residue field the passive algebras remain finite
etale, required local units stay units, and the polynomial
reparametrization identities and their branch constraints persist.
The same local resolution computation therefore gives the complete
normalization places and parameters in that residue characteristic.
The trace-lattice inclusion remains valid for a separable monic
polynomial over a field, as does the numerator-integrality test.
The jet recurrences commute with reduction because their only
divisors are recorded units. Preserved matrix rank makes the
principal-part kernel commute with reduction. The colength
argument of Section 4 makes the output basis the FULL reduced
normalization, not merely an integral suborder.

These arguments apply componentwise if an intermediate reduced
plane fiber is reducible: local branch resolution and the
trace-lattice test concern the separable total quotient algebra,
and monic separability prevents nilpotent generic components.
The next paragraph in fact forces geometric connectedness of the
proper reduced fiber in this family.

The retained Laurent transition glues these two finite free
algebras to a scheme finite flat over `P^1` over the localized
coefficient order. It is proper and flat over that order. At
each residue field, both charts are the normalization of a curve;
a normal curve over a perfect field is regular and smooth.
The generic fiber is the given smooth normalization. Flatness,
finite presentation and geometric regularity of every fiber
therefore imply smoothness of the model over this base. Proper
smooth fibers have locally constant geometric connected-component
count; the base order is connected and the generic fiber is
geometrically connected. All these fibers are geometrically
connected. This proves the required good model and specialization
statement without a growing-variable Groebner smoothness atlas
or an unquantified appeal to spreading out.

## 7. Independent primary-source checks on heights and specialization

Bilu--Borichev Theorem 6.3 bounds ramified-series coefficients at
ALL places: the logarithmic height of coefficient number `k` is
bounded by a constant term plus `(k/e-floor(kappa/e))` times a
quantity polynomial in the equation height, its bidegrees, and
ramification `e`. After shifting to a closed discriminant root,
the equation and root heights are polynomially bounded by
resultant/root bounds. Thus this theorem is consistent with the
polynomial truncation-height claim above. It does not alone
bound coordinates in an arbitrarily chosen algebraic basis, nor
the degree of a compositum of all coefficient fields. Sections
2--3 pay those representation issues directly.

Poteaux--Rybowicz supplies a separate local reduction check. Write

```
Delta=c*product_j q_j(x)^j
```

with squarefree pairwise-coprime `q_j`. In `K[alpha]/q_j(alpha)`,
the trailing nonzero coefficient of `Delta(alpha+X)` is the unit

```
c*q_j'(alpha)^j*product_(h!=j) q_h(alpha)^h.
```

Compute it and its norm in this finite etale algebra. Include its
integer norm, the squarefree-factor discriminants/pairwise
resultants, and coefficient denominators if they were not already
included. For `P>d`, these data ensure the source's local good
reduction condition at every branch root after reduction.
Theorems 3 and 4 then give integral Puiseux coefficients and
preservation of the Puiseux cycles; Theorem 5 preserves its
GENERIC polygon tree. This argument also uses closed algebras,
not a common field of all series coefficients.

The source explicitly warns that non-characteristic coefficients
can vanish and classical Newton polygons can change despite
this smaller criterion. Therefore this smaller norm alone is
not represented here as preserving every Kozen decision. The
additional recorded nonzero comparisons in Section 6 pay that
stronger transcript claim. The source criteria confirm that the
branch-specialization assertion is not being inferred merely
from generic characteristic-zero resolution.

## 8. Disposition of the completed good-model report and RR consequence

The report correctly rejects the inference from local resolution,
unit-cost normalization, or abstract spreading out ALONE to the
full native bit certificate. Its conditional two-chart RR argument
is sound: a regular-fiber point `O=(a,b)` in one charged extension
of degree at most `d` and the Laurent transition bound give a
finite coefficient system for `L(kO)`. If the transition exponents
are in `[-A,A]`, the numerator polynomial-vector degrees are at
most `k+A`; the system has `d(k+A+1)` columns and at most
`d(k+2A)` rows over the point field. Idempotents in the truncated
fiber algebra isolate `O` without splitting the remaining fiber.
Its stated polynomial bit bounds follow from the numerical `k`
and the charged presentation/field tables.

The trace-lattice construction above now supplies that report's
previously missing TWO-CHART INPUT from the arbitrary singular
plane equation. A separate standard-smooth atlas is unnecessary:
the normalized-fiber/transcript and finite-flat gluing argument
already certifies the proper smooth model at every allowed prime.
Adjoin the report's regular-fiber, point-order-discriminant and
retained RR-rank factors to `M`; their determinant bounds preserve
polynomial `log|M|`. Its elementary search for a numerically
polynomial auxiliary prime, by avoiding the at most
`log_2|M*ell*|G||` prime divisors, remains valid without integer
factorization. The condition is `P` coprime to `ell*|G|`, not an
unpaid requirement `P>ell*|G|`.

Accepted: the trace lattice and linear integrality test; direct-sum
residue algebra accounting; centered inverse-map jet bit bound;
bounded-linear-system integral basis; explicit infinity transition;
and polynomial-size bad-prime transcript proving reduction of the
FULL normalization. Corrected shortcuts: arbitrary repeated
composition without centering/truncation, ordinary field-operation
counts without coefficient-factor bounds, and bare spreading out.

Remaining upstream: construction and height of the native supplied
cover equation/number field when not already charged. Remaining
downstream: torsion-coordinate height and certified reconstruction
precision. This note does not turn numerical lifting or the new
good-model certificate into either of those theorems. Parent owns
the shared state/handoff update after independent scrutiny of this
construction; no numerical sweep is needed for its symbolic proof.
