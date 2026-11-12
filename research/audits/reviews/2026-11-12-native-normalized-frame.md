# Native normalized Weil pairing and frame: constructive review

2026-11-12. Independent attack on the parent's Segre-specialization,
divisor/norm, and normalized-frame recipe. Read current `STATE.md`,
`SURFACE_NATIVE_COVER_CONSTRUCTION.md`, the complete native-Jacobian-atlas
review, the level-cover review, and the relevant actual Anderson and
Couveignes sources. The paid normalized-frame request was EMPTY and is
not evidence; no retry was made. No Git, network, API, archive, numerical
sweep, or implementation was used. Commands used
`/opt/anaconda3/bin/python`; source lines use physical newline counting.

## Disposition

ACCEPTED as a constructive polynomial-bit algorithm in the fixed native
`(5,3)` format, composed with the already reviewed unmarked level-cover
construction. The Segre row has the proposed PLUS sign, and norm descent
works for primes `ell>15`. The correct norm operation is divisor
pushforward with multiplicities, not scheme-theoretic image.

There is also a simpler route to the pairing/frame conclusion: lift the
two torsion classes to actual divisors over ONE common extension of
constant relative degree, evaluate the pairing there, and compare it
exactly with the known powers of `zeta_ell`. This requires no norm descent
or coprimality of the extension degree, so it works for small odd primes
as well. Norm descent is separately proved below for the requested
`ell>15` range.

The new bit proof uses the fixed complete-intersection section spaces,
closed divisor ideals and jets, polynomial-size linear systems, and
determinant norms. It is not an inference from Couveignes' finite-field
complexity theorem. It avoids an inverse-Abel oracle, rational-point
advice, support-splitting composita, and a Brauer-obstruction assumption.

The output is the genuine normalized GENERIC frame algebra and evaluation
over `Q(t)` and its cyclotomic base, with polynomial degrees, coefficient
heights, and bit cost. Constructing a growing-cover integral/good model,
controlling every specialization or auxiliary prime, and downstream
reconstruction remain separate.

## 1. Exact input and arithmetic parameters

Let `K0=Q(t)`, and let `C/K0` be the smooth geometrically connected
complete intersection of degrees `(5,3)` in `P^3`. Thus `g=31`,
`deg C=15`. Use the established native data:

```
E = reduced union of five etale pencil fibres,
deg E=75,       n=h^0(E)=45,
L(kE) = {Q/F_E^k : Q in H^0(C,O_C(5k))}.
```

The Koszul description computes these section spaces and multiplication
maps. The finite evaluation divisor `T` has degree 26715 and consists
of 1781 degree-15 etale fibres disjoint from `E`. It detects every source
Jacobi discriminant, whose per-slot pole divisor is at most `356 E`.
These are established inputs, not new numerical assertions.

Let `k=Q(zeta_ell)`. The reviewed level-cover algorithm supplies a field

```
F=k(t)[Y]/R(t,Y)
```

and genuine ordered basis points `P_1,...,P_62` of `J_C[ell]`, as points
of the native Jacobi model. Under the full geometric monodromy promise,
`[F:k(t)]=|Sp_62(F_ell)|`, its constant field is `k`, and its deck
matrices preserve a computed nondegenerate alternating form `B`, known
up to scalar relative to the actual Weil form.

For arithmetic bookkeeping write `D=[F:Q(t)]`, and charge the degree
and logarithmic coefficient height of its multiplication tables, all
point coordinates, and the native curve/atlas data. The reviewed cover
construction bounds all these quantities by a polynomial in numerical
`ell` and the native input bit size, with fixed-format exponent. The
proof below is polynomial jointly in these explicit parameters; `F`
is not an oracle field.

## 2. Constructive Jacobi inversion over a constant-degree extension

Anderson Proposition 3.7.2, physical lines 1045--1065, says that if a
specialized Jacobi discriminant is nonzero, specializing slots
`1,...,n+1` produces an actual Segre matrix `X` in `L(2E)`, whose
abeliant represents the original Jacobi point. It is a polynomial
specialization, not an inverse to an unspecified map.

For a given Jacobi point over `F`, specialize its 46 slots successively.
Maintain that the remaining tensor of sections is nonzero. At each
stage, evaluation on the fixed divisor `T` is injective after ANY
field extension. Some evaluation in one of its degree-15 fibre algebras
therefore leaves a nonzero remaining tensor. Factor that finite etale
algebra over the current field and choose a field factor on which the
remaining tensor is nonzero. The new extension degree is at most 15.
This is an exact nonzero-coefficient test in explicit section bases.

After 46 steps one obtains a field `L/F` and an actual matrix

```
X in Mat_45(L(2E)_L),
[L:F]=m=product_(i=1..46) e_i,       1<=e_i<=15.           (1)
```

The enormous bound `m<=15^46` is a FORMAT CONSTANT. In characteristic
zero all extensions are separable. For a prime `ell>15`, `gcd(m,ell)=1`.
It would be incorrect to infer coprimality merely from a general bound
`m<=15^46`; it follows from the displayed tower factors.

The source is written over an algebraic closure. Apply it there to
prove the identities, then observe that this matrix is defined over
`L`. Rank one and geometric linear independence of the rows/columns
give the required Segre properties over `L`. Its associated geometric
Jacobian point is the original point base changed to `L`.

For two points, repeat the second 46-step construction over the first
extension. One common field of degree at most `15^92` over `F` suffices.
This is a fixed-length tower, not a compositum of a growing list of
torsion-support fields.

### The factorization in this step is paid

Only constant-degree finite etale algebras need be factored over a
growing field. A concrete reduction to the same rational-factorization
dependency already charged in the level-cover review is as follows.

First present the current field as `Q(t)[theta]`. A primitive element
is found by a polynomial-size integer grid, excluding the at most
quadratically many collisions among its distinct embeddings; verify
full degree by linear algebra. Every change of basis and coefficient
has a ratios-of-minors bound. For a monic squarefree polynomial `h(X)`
of degree at most 15 over this field, choose a small integer `c` such
that

```
Norm_(F/Q(t))(h(X-c*theta))
```

is squarefree. The tagged pairs of conjugates `(theta_i,beta_ij)` give
at most quadratically many forbidden values of `c`. Compute the norm
by a resultant/determinant, factor it over `Q(t)`, and pull the factors
back by gcd after the reverse shift. Squarefreeness ensures that these
are the irreducible factors over the original field. Clearing/scaling
denominators reduces to monic polynomials in `Q[t,X]`; the existing
LLL/specialization-Hensel factorization argument has polynomial degree,
height, and bit cost. No integer-factorization or irreducibility oracle
is inserted. The number of successive field stages is fixed at 46 or
92, so their polynomial size bounds compose to a polynomial.

## 3. The row divisor: sign, degree, and support on E

The source dictionary is explicit. Anderson 4.2.3--4.2.6, physical
lines 1287--1348, assigns a `2E`-form `X=u*v` to the class represented
by the column section space. Section 4.4.2, lines 1539--1548, sends a
degree-zero class `t` to a form representing `E+t`.

Over an algebraic closure write

```
u spans L(E+t),       v spans L(E-t),       X=u*v.
```

Both degree-75 line bundles are globally generated, since `75>=2g`.
For any nonzero row `u_i*v`, the common zero divisor of its entries as
sections of `O(2E)` is

```
D_row = 2E + div(u_i) + min_j div(v_j)
      = E+t+div(u_i).                                     (2)
```

It is effective of degree 75 and has class `E+t`. A column similarly
has class `E-t`. Nonzero rows have linearly independent entries: this
follows from rank one and the Segre generality condition, source
3.1.4, physical lines 594--602. The source's direct reconstruction
`G+min_j div(v_j)` in 4.2.5 confirms the same PLUS sign for a row.

The correct computational object is the whole common-zero SCHEME of
the row sections. If `X_ij=Q_ij/F_E^2`, use the degree-10 homogeneous
numerators `Q_ij` on `C`, with projective saturation or an equivalent
fixed affine cover. This includes points on `E` and their exact
multiplicities. Taking common zeros only on `C\E`, or radicalizing the
divisor ideal, would be wrong. On the smooth curve the generated ideal
is locally principal with valuation the minimum of the row valuations,
so its length is exactly 75.

All equations have fixed degree and fixed curve-coordinate dimension.
Their coefficients are explicit elements of `L`. Thus this step is
fixed-format ideal/linear algebra. It outputs an actual closed divisor

```
delta_L = D_row-E_L
```

whose class in `Pic^0(C_L)` is the given torsion point. No rational
curve point and no assertion that every `F`-rational Picard point
already has an `F`-divisor is used.

## 4. Norm descent with its multiplicities

Let `q:C_L -> C_F`. Since `C/F` is geometrically connected, this is a
finite etale constant-field morphism of degree `m=[L:F]`. Set

```
A = q_* D_row,          delta_0=A-mE.
```

Then `A` is effective of degree `75m`, and norm/pullback on the
Jacobian gives

```
[delta_0]=m*t.
```

For `ell>15`, choose the integer `j` with

```
1<=j<ell,        jm=1 mod ell.
```

The closed `F`-divisor

```
delta=j*A-jm*E                                            (3)
```

represents the ORIGINAL point `t`, with positive and negative degrees
at most `75m*(ell-1)`. The norm descent has degree polynomial in
numerical `ell`; no torsion-order logarithmic claim is required.

This also resolves the descent obstruction correctly: an actual
divisor for `m*t` has been constructed and `m` is invertible modulo
`ell`. The injection from divisor line-bundle classes into the
relative Picard group ensures that the resulting class is indeed `t`.
It is not a presumed inverse-Abel or Brauer splitting oracle.

Computing `q_*D_row` requires more than projecting its support. If
conjugate points coincide after descent, their multiplicities ADD.
A precise computation is the zeroth Fitting ideal of

```
q_* O_(D_row)
```

as a torsion module on the regular curve `C_F`. Locally its order is
the module length, exactly the coefficient of the pushforward divisor.
Choose an `F`-basis of `L`; multiplication by the row generators gives
a presentation matrix over each curve chart. Its maximal minors give
the Fitting ideal. Equivalently one may use the norm of the invertible
divisor ideal. Matrix sizes and this extension degree are constants.
Projective gluing/saturation uses the fixed curve-coordinate format.
The degree check is `deg A=75m`, including repeated factors.

Norm the two torsion divisors separately if this route is used. No
common growing compositum is required. The alternative common-field
pairing route in Section 7 avoids norm descent altogether.

## 5. Riemann--Roch for the required divisors is explicit

The available spaces `L(kE)` suffice even when `k` grows polynomially
in `ell`. The complete-intersection Koszul sequence works for every
nonnegative degree, not only the constant `k` used to construct the
atlas. Homogeneous degree `5k` polynomials in four variables form a
polynomial-size coefficient space, and quotienting by the fixed
degree-5 and degree-3 equations gives `H^0(C,O_C(5k))` by linear
algebra. Its dimension is `75k-30` for `k>=1`.

For an effective closed divisor `A` of degree `s`, restriction of
`O(5k)` to its possibly nonreduced finite scheme gives the full jet
conditions for vanishing along `A`. These are linear conditions in
the polynomial coefficients. To trivialize the line bundle on `A`,
choose a hyperplane from the basepoint-free pencil which avoids its
support. At most `s` integer pencil values are forbidden, so at most
`s+1` trials suffice. Dehomogenization then computes its length-`s`
Artin algebra and restriction map; nilpotents must be retained.

Here is a direct general reduction. For effective `P,Q`, choose `k`
with `75k-deg P>=2g`, and a nonzero section

```
w in H^0(O(kE)(-P)).
```

Its section-zero divisor is `P+R` with `R>=0`. Multiplication by `w`
identifies

```
L(P-Q) ~= H^0(O(kE)(-Q-R)).                               (4)
```

Both sides are thus computed from the native homogeneous section
space and finite jet constraints. The residual divisor `R` is the
Cartier ideal quotient of the section-zero ideal by `I_P`, with
multiplicities. Effective-divisor sums, residuals, restrictions, and
empty-support tests all use fixed-variable ideal membership and linear
algebra of polynomial size. There is no genus-growing curve algorithm
being invoked: this is still the ORIGINAL fixed genus-31 curve over
the growing coefficient field.

### Moving to disjoint support

Suppose `delta` is one degree-zero divisor and `S` is the finite
support to be avoided. Choose an effective divisor `H`, supported on
an etale pencil fibre disjoint from `S`, of degree at least `2g`.
For example five copies of one degree-15 fibre give degree 75. A
bounded search over integers avoids its at most `deg S` bad values
and the at most 90 ramified values.

The complete linear system `L(delta+H)` is globally generated. A
section which is nonzero at every point of `S` gives

```
delta+div(r)=A'-H,       A'>=0,       Supp(A') intersect S=empty.
```

Find it deterministically: for a computed basis `r_0,...,r_(v-1)`, try
`sum_i c^i r_i`. At each geometric point of `S`, its evaluation in
the appropriate line-bundle fibre is a nonzero polynomial in `c`
of degree at most `v-1`. Thus `deg S*(v-1)+1` integer candidates
suffice. Test the resulting effective divisor's intersection with
`S` exactly. Evaluation here means the line-bundle value, including
any forced orders in a rational-function presentation; ordinary
substitution at a pole would not be the test. The residual-divisor
calculation in (4) supplies that exact test.

This constructs two linearly equivalent, disjoint degree-zero divisor
representatives. It can also compress their positive and negative
degrees to fixed degree 75, although a polynomial degree bound is
already sufficient. No geometric support points need be split.

### Principal functions and the potential 0/0 trap

Let `delta=A-B` represent an `ell`-torsion class, and let `S` be the
support of the other, disjoint divisor. Choose `k` with
`75k-ell*deg B>=2g`. In `H^0(O(kE)(-ell B))`, choose a denominator
SECTION `w` which does not vanish on `S`; the same finite candidate
argument applies. Write its section-zero divisor as

```
D_w=ell B+R.
```

Compute

```
h in H^0(O(kE)(-ell A-R)).
```

This last line bundle has degree zero and is trivial because
`ell*[A-B]=0`, so its section space has dimension one. A nonzero
solution gives

```
f=h/w,                 div(f)=ell*(A-B).                 (5)
```

Its denominator section is a unit on `S`, and its numerator is also
nonvanishing there. Work in a hyperplane chart avoiding `S` and
evaluate the ratio of the homogeneous numerators in that chart.
This deals with support on `E` without assuming `F_E` is nonzero.

Without the nonvanishing choice for `w`, a representation `h/w` can
be `0/0` on the evaluation divisor, even though the rational function
itself is a unit there. Disjointness of the FINAL principal divisor
alone does not justify inverting an arbitrary displayed denominator.

## 6. Polynomial bit bounds, not a field-operation assertion

Let `s` bound all effective-divisor degrees in a stage; it is polynomial
in numerical `ell`. The powers, section numerators, jet algebras, and
RR matrices above have polynomial degree and size in `s`. The number
of curve-coordinate variables is fixed. Effective ideal membership
bounds therefore give polynomial Macaulay matrices for every quotient,
saturation, and residual calculation. For a finite length-`s` algebra,
monomials of degree at most `s-1` span it; fixed-variable membership
computes a basis and its multiplication tables, including nilpotents.

Divisor multiplicities must not be implemented by an uncontrolled
height recurrence. For a power `I^a`, products of original generators
have degree at most `a` times the original bound and logarithmic
coefficient height at most a polynomial in `a` and the original size.
Although the list of products can be exponential, its span in every
relevant bounded-degree polynomial space has polynomial dimension.
Iterated multiplication can retain a basis consisting of ACTUAL
products, selected by linear independence, rather than recursively
row-reduced rational combinations. Multiplying such a basis by the
original generators still spans the next products. This computes
polynomial-size generating spaces while retaining the direct product
degree/height bound. Add the fixed curve ideal and perform the needed
fixed-variable saturation/membership calculation afterward.

For all field operations expand the explicit multiplication tables
over `Q(t)`. An `a`-by-`b` linear system over a field of degree `D'`
becomes one of polynomial size over `Q(t)`; here `D'<=15^92 D`.
Clear the denominators ONCE for each matrix. If its polynomial entries
have degree at most `T` and logarithmic height at most `H`, a size-`v`
minor has degree at most `vT` and logarithmic height

```
O(v*(H+log(v+1)+log(T+1))).                              (6)
```

These bounds also control ratios of minors and fraction-free solves.
The finite number of algebraic stages and fixed-length extension
towers preserve polynomial bounds. Searches are independent trials
from the same bounded data, not chains that compound height bounds.

For powers and polynomial substitutions one can check the bound
directly using multiplication matrices. Products of `a` matrices
with bounded polynomial entries have degree at most `aT`, and log
coefficient size `O(a*(H+log D'+log(T+1)))`, after choosing common
denominators. This prevents the spurious exponential estimate obtained
by multiplying a worst-case field-reduction factor at every operation.
The same observation pays the polynomial-degree divisor powers and
finite norms.

The addition/multiplication atlas used later for changing torsion
bases also has a direct bound: expand its `O(log ell)` fixed-degree
composition as polynomials in the original, FIXED number of point
coordinates, then substitute/reduce in the field once. The total
degree and coefficient height are polynomial in numerical `ell`.
There is no need to apply a growing-degree field-height inflation
factor separately at every doubling.

Every determinant norm used to push a divisor or evaluate a function
is a polynomial-size determinant with these same bounds. Therefore
all `t`-degrees, logarithmic heights, dense intermediate/output sizes,
and exact rational bit costs are polynomial in the charged field and
native input parameters. No source is being credited with a
characteristic-zero bit theorem it did not state.

For a determinant whose VALUE is required in `F`, retain that `F`-valued
determinant, using for example a division-free determinant algorithm and
the polynomial product bounds above. Taking the determinant of the
expanded `Q(t)` multiplication matrix would instead take an additional
field norm and generally give the wrong pairing value. Expansion is
used for linear solving and size bounds, not to change the target of
the determinant.

## 7. Actual Weil-pairing evaluation and the simpler common-field route

Use disjoint representatives `delta,epsilon` and functions

```
div(f)=ell*delta,       div(g)=ell*epsilon.
```

The RETAINED COUVEIGNES convention is

```
e_ell(delta,epsilon) = g(delta)/f(epsilon).                (7)
```

This is the displayed formula at physical lines 624--629 of
`couveignes.txt`. It is the inverse of another commonly used
convention; do not interchange them during normalization. The source
defines this pairing from the diagonal correspondence and original
Jacobian polarization, physical lines 583--605. Equation (7) is
algebraic and valid in characteristic zero as well. The source's
finite-field algorithmic Lemma 10, lines 655--660, is NOT the bit-cost
justification here; Section 6 supplies it.

As a direct sign/root check, Weil reciprocity gives
`[g(delta)/f(epsilon)]^ell = g(div f)/f(div g)=1`.
The source convention is kept throughout the subsequent scalar
normalization. Using the globally inverse pairing instead would require
the known change `zeta -> zeta^-1`; it is not an unspecified scalar.

For an effective closed divisor `A` and a function unit on its support,
evaluate by

```
f(A)=det(multiplication_by_f on H^0(A,O_A)).               (8)
```

On a nonreduced divisor this is the residue-field norm raised to the
appropriate multiplicity, exactly the ordinary divisor evaluation.
For a signed divisor divide the positive and negative evaluations.
The denominator choice in (5) makes every inverse in these finite
algebras legitimate. Thus (7) is obtained by explicit linear algebra
and determinants, without splitting the supports.

For the norm-descent route, (3) supplies the original two points as
divisors over `F`, and (7) is computed directly in `F`.

For the simpler route, put both actual degree-75 Segre divisors over
the common constant-degree field `L` of Section 2, move them and use
(5)--(8) there. Functoriality of the geometric Weil pairing identifies
the answer with the pairing of the original `F`-rational Jacobian
points. It is therefore in `mu_ell(F)`. Since `zeta_ell` is already
given in `F`, compare the answer, as an element of `L`, with

```
1,zeta_ell,...,zeta_ell^(ell-1).
```

Exactly one comparison succeeds. This is polynomial in numerical
`ell`, with no discrete-log oracle. It also descends the answer
without solving for a general invariant subfield. Coprimality of
`[L:F]` with `ell` is not needed: the pairing is evaluated on the
actual lifted points, not on their norms. Hence this route also
handles the small odd primes excluded from the optional norm-divisor
recipe.

## 8. Fixing the scalar and selecting the genuine frame algebra

Let `B` be the nonzero invariant alternating form from the unmarked
cover. Full geometric `Sp` monodromy makes its invariant-form space
one-dimensional, so the actual exponent matrix of (7) is `cB` for a
unique `c in F_ell^*`. Choose `i,j` with `B_ij!=0`, compute the actual
pairing as above, and find `a` with

```
e_ell(P_i,P_j)=zeta_ell^a.
```

Then `a!=0` and `c=a/B_ij`. The nontriviality and root-of-unity tests
are exact consistency checks. Symplectic Gram--Schmidt produces an
explicit matrix `M` such that

```
M^T*(cB)*M=J.
```

The actual torsion points `Q=P*M`, computed by the complete native
atlas, now satisfy

```
e_ell(Q_i,Q_j)=zeta_ell^(J_ij).                           (9)
```

Only one pairing evaluation is needed by the invariant-form proof.
The recovered scalar is a measured normalization of the original
polarization, not a free choice of an arithmetic Frobenius lift.

Over `k(t)`, evaluate the ordered-basis finite algebra at these
normalized coordinates. The resulting map onto `F` is surjective:
`M` is invertible, so the new basis generates the same field as the
old one. Its kernel is computed by polynomial-size linear algebra.
Because the algebra is finite etale, this selects a reduced factor,
or equivalently a support idempotent. Full geometric `Sp` monodromy
and its degree show that this factor is exactly the WHOLE
`zeta_ell`-normalized symplectic-frame scheme, not a proper subset.

Now regard the SAME field `F` as a `Q(t)`-algebra, retaining `zeta_ell`
as a coordinate. This is NOT the Weil-restriction functor, which
would produce a different and much larger scheme. Its degree is

```
[F:Q(t)]=(ell-1)*|Sp_62(F_ell)|=|GSp_62(F_ell)|.
```

The native base is `Q(t)`, whose mod-ell cyclotomic character has full
image. Arithmetic monodromy contains geometric `Sp` and surjects
under the multiplier, so it is all of `GSp`. Every conjugate of (9)
is therefore one of the genuine frames `(Q,zeta)`, and their count
is exactly the displayed degree. Equivalently, evaluate the
all-basis algebra together with the primitive-root coordinate into
`F`; its kernel selects the entire full-similitude frame algebra.
This is a generic finite etale SCHEME identification, not just a
claim that some coordinates have the right dimension.

The tautological evaluation is explicit:

```
c(v)=sum_i v_i Q_i in the ORIGINAL J_C[ell].
```

For `g in GSp`, the right deck action is the genuine one

```
(c,zeta).g=(c composed_with g, zeta^lambda(g)).
```

Its coordinate formulas follow by changing the basis with the
complete atlas and evaluating the known primitive-element expression;
the root coordinate is changed as displayed. This includes the
nontrivial action on `zeta`; it must not be frozen when constructing
multiplier-nonone deck maps. All formulas and quotient maps retain
the polynomial bounds of Section 6 and the earlier cover review.

Thus the evaluation identifies the associated local system with the
actual original Jacobian torsion. The generic normalized-frame input
to the previously checked full-GSp arithmetic identity is now
constructed in this native fixed format.

## 9. Intrinsic extension over a smooth p-adic family

Suppose separately that the ORIGINAL curve family is smooth, proper,
and geometrically connected over `U_(Z_p)`, with `p!=ell`. Its relative
`Pic^0` is the intrinsic principally polarized abelian scheme `J/U`.
Then `J[ell]` and `mu_ell` are finite etale over `U`, and the Weil pairing
is a perfect alternating pairing of those etale group schemes.

The functor of pairs `(c,zeta)` with `zeta` primitive, `c` an ordered
torsion basis, and

```
e_ell(cu,cv)=zeta^(u^T Jv)
```

is locally the constant finite `GSp_62(F_ell)` set in the etale topology.
It is therefore represented by a genuine finite etale frame torsor over
`U_(Z_p)`, with its tautological evaluation and constant right deck
action. This conclusion uses `ell` invertible on the smooth family;
it does not require `p` to be prime to the order of `GSp`.

The generic algebra constructed above is identified with THIS intrinsic
frame functor, because the native Jacobi identification is with the
original `Pic^0`, the measured pairing is its actual Weil pairing, and
the basis evaluation was retained. Consequently it has that abstract
finite etale extension. If `U` is normal, as for the stated regular
open base, the extension is also characterized as its normalization in
the generic finite algebra, and uniqueness extends the evaluation and
deck maps.

This does NOT say that the selected characteristic-zero Jacobi equations,
addition laws, Segre specializations, or their denominators reduce well
at `p`. Those formulas may invert `p`. They are used here to identify the
generic object; the abstract extension follows from the original smooth
family. Thus an independently proved finite-algebra reconstruction and
`p`-maximalization readout can use the intrinsic extension without first
repairing every coordinate formula at `p`. Construction/cost of that
readout and its height hypotheses are not proved in this review.

## 10. Scope and rejected shortcuts

The exact row-divisor, constant-degree specialization, optional norm
descent, moving, principal functions, closed evaluation, and scalar
normalization all survive independent attack. Important rejected
shortcuts are:

* dropping divisor support on `E`, radicalizing jets, or using a column
  while retaining the row's sign;
* taking a scheme image in place of the divisor norm;
* deriving extension-degree coprimality from its size bound alone;
* invoking finite-field pairing time as a characteristic-zero bit bound;
* evaluating a displayed `0/0` quotient merely because its divisor is
  disjoint from the evaluation support;
* iterating a generic height bound once per field operation;
* replacing the underlying `Q(t)`-algebra by Weil restriction, or
  fixing `zeta` under a multiplier-nonone deck action.

The algorithm is polynomial in numerical `ell`, the charged native
input size, and the already polynomial level-cover presentation. All
constants may depend on the fixed `(5,3)` format and are impractically
large. No polynomial-in-`log ell` claim is made. Field extensions here
are actually constructed and paid, of constant degree RELATIVE TO the
presented splitting field; they are not unspecified existential
arithmetic extensions.

The proof concerns the generic function field and true pairing/frame
semantics. Denominators, rank witnesses, and discriminants can be
retained, but this does not prove a good growing-cover model at every
auxiliary prime, nor a uniform integral specialization theorem. Native
cover normalization at growing genus, arithmetic lifting, a complete
closed-divisor reconstruction encoding, and the final point-counting
claim remain separate.
