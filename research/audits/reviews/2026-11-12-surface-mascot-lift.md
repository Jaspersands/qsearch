# Surface torsion lifting: Mascot source and model prerequisites

2026-11-12. Independent source/algorithm audit. Read current `STATE.md`,
`SURFACE_NATIVE_TORSION_MODULE.md`, and the actual primary
`audits/sources/surface_module_2026/mascot_lift.txt`: Sections 2, 4, 5,
especially Remark 2.4, Theorem 2.23, Algorithms 9 and 10, and Remark 1.6.
Source PDF SHA256:
`4da85f621b32b68e2673c71bc8b8cac7bfe1666fbd4c9f975c181a2474811880`.
No Git, network, API, archive search, code, or numerical control.
Interpreter, if needed: `/opt/anaconda3/bin/python`.

## Result and exact input boundary

Mascot's Algorithm 10 pays prime-to-`P` torsion lifting to a prescribed
NUMERICAL precision once a compatible integral evaluation model is
available. Its finite-field input may be an actual torsion class represented
by CLOSED divisors: its geometric support need not split, and those support
points need not be the auxiliary evaluation points. One polynomial-degree
common unramified field suffices for the evaluation model.

The integral model can be constructed by the RR/coefficient-lattice method
below if the supplied plane chart reduces faithfully to the GOOD special
curve and the exact RR functions have a charged polynomial-size coordinate
presentation. This explicitly removes an additional requirement to supply
integral RR bases or independently reduced evaluation matrices.

Do not replace that presentation condition by the mere assertion that an
abstract curve has good reduction. A generic separable plane equation need
not reduce faithfully. For example, replacing `y` by `Y=P y` changes a good
hyperelliptic equation into `Y^2=P^2 f(x)`, whose displayed reduction is
nonreduced. Mascot does not construct a compatible smooth model from an
arbitrary such presentation. The upstream native-cover construction must
provide/check a good presentation (or explicitly repair it), including
the relevant coordinate and RR-size bounds. No new arithmetic height bound
for that upstream construction is proved here.

Under this model condition, the lift has polynomial bit cost in genus,
presented model/RR/divisor size, residue extension degree, numerical output
precision, `log P`, and `log ell`. The construction is independent of full
ambient torsion splitting and independent of geometric divisor-support
splitting. It does NOT certify rational reconstruction or a global height.

## 1. Closed divisors supply the actual finite-field Jacobian input

Let `C` have genus `g>=1`, good reduction at the unramified prime `P`,
and a supplied actual rational point `O` with good reduction. Put

```
d0=2g+1,       D0=d0 O,       V_j=L(jD0).
```

Suppose the supplied actual torsion class is represented over the residue
field by `T=D-gO`, with `D` a rational effective CLOSED divisor of degree
`g`. Set `D'=D+(d0-g)O`. Then `D'` is effective of degree `d0`,
`[D'-D0]=T`, and

```
W_D=L(2D0-D')=L((d0+g)O-D)
```

has the required dimension `d0+1-g`. Finite-field RR on closed-place
ideals computes this subspace and its evaluations without splitting the
support of `D`. If the input is another degree-zero divisor presentation,
ordinary RR first gives an equivalent effective presentation of degree
`d0`; no prime-support representative theorem is needed.

Verify the supplied relation `[ell]T=0` in the finite Jacobian, using its
exact divisor/RR representation. Neither the source nor this review
substitutes an arbitrary matrix for an actual torsion class. Source
Remark 1.7 expressly warns that most matrices of the right dimensions
do not represent Jacobian points.

## 2. Constructing one evaluation field and the auxiliary points

Let the common residue field already containing the input data be
`k0=F_(P^a)`. Work with a separable affine plane chart of the good special
curve. Let `d` be the projection degree and let `T_bad` bound the number
of geometric points excluded by:

* poles and exceptional places of the chosen chart;
* vanishing of the selected unit derivative for point lifting;
* `O` and the denominators of the chosen RR function presentation.

This is a numerical degree bound computed from the presented functions
and is polynomial in their charged sizes. Choose a SINGLE extension
`k=F_(P^(a s))` large enough that

```
#C(k) >= |k|+1-2g sqrt(|k|) > T_bad+5d0+1.
```

A field size larger than `(4g+2T_bad+2(5d0+1)+2)^2` is more than
sufficient. Thus `s=O(1+log(g+T_bad)/log |k0|)` suffices. This is a
degree bound, not enumeration of that field, and all auxiliary points
are constructed over this same field.

A bounded randomized construction samples the plane coordinate `x`,
factors the degree-at-most-`d` fiber polynomial, and retains rational
points passing the exclusions. With a slightly generous version of the
above size bound there are at least `|k|/2` admissible rational points.
Their images occupy at least `|k|/(2d)` coordinate values. Consequently
each trial succeeds with probability at least `1/(2d)`, up to excluding
the already selected `O(g)` points. This gives a polynomial capped clock
for `n_Z=5d0+1` distinct evaluation points, with a stated FAIL probability.
Finite-field factorization and arithmetic are charged in the field's
explicit degree and `log P`. No common field for unrelated divisor
support degrees is formed.

Lift these evaluation points to the unramified integer ring `O_K` by
fixing a lift of the free coordinate and using the unit partial
derivative to Hensel-lift the other coordinate. This is quadratic
lifting with no loss of digits. The residue points remain distinct,
and the lifted points are actual curve points in ONE unramified local
field of degree `a s`.

For torsion lifting alone, `Z` need not be stable under the original
`P`-Frobenius. If Mascot's row-permutation Frobenius Algorithm 8 is also
used, its stated conditions must hold: `D0` and `Z` must be defined over
the arithmetic base, and the permutation must be recorded. Taking
unions of Frobenius orbits in the chosen single field supplies a stable
`Z` at polynomial cost (possibly slightly increasing `n_Z`). If `O`
is not defined over that original base, its conjugation/basepoint change
must be included, just as in the native-module note. No uncorrected
row-permutation formula is asserted in that case.

## 3. The integral RR bases are constructible under the good-presentation check

This is the specific bridge not supplied merely by quoting Mascot.
Assume the exact generic RR calculation gives a basis of `L(D0)` in
polynomial-size rational-function coordinates in the supplied separable
plane function field. Choose one common denominator and reduce the
numerators to a normal form of degree below the plane polynomial's
degree in `y`. Require that the reduced plane function field is the
actual good special curve, with the same normal-form degree, and that
the common denominator is nonzero after primitive reduction.

Take the coefficient vectors of these normal-form numerators and compute
their saturated lattice over the local integer ring. Exact coefficient
linear algebra gives a basis whose coefficient columns are independent
modulo `P`. With an exact number-field/function-field presentation this
is a finite lattice computation; its valuations and bit costs are
bounded by the sizes of the supplied RR coefficient matrices. If only
unconditioned finite approximations to those matrices are supplied, this
argument is NOT a license to infer exact rank from them.

The resulting functions have integral values at the chosen evaluation
points because their common denominator is a unit there. They form
the true integral `H0(D0)` lattice, for the following reason. On the
smooth proper good model, `H0(O(D0))` is a free lattice of rank
`d0+1-g`, and its reduction is the full special-fiber RR space: degree
`d0>2g-2` makes `H1` vanish. For any generic section, take the least
power `P^k` making it integral. If `k>0` while all its evaluation values
are integral, the nonzero reduction of that primitive integral section
vanishes at more than `d0` distinct points away from `O`. This is
impossible for a nonzero section of degree `d0`. Hence evaluation
integrality already implies membership in the true lattice.

Finally, independent reduced normal-form coefficient columns give
independent rational functions on the faithful special curve. Thus the
constructed integral sections have `d0+1-g` independent reductions and
are an integral RR basis by Nakayama. No numerical formal-log inversion,
support splitting, or torsion-coordinate height enters this argument.

Evaluation at `n_Z>5d0` points is injective on `V5`, over both the
generic and special curves. Starting from this `V1` basis, the source's
multiplication constructions therefore build `V2`, `V3`, their equation
matrices, and the other required spaces with unit pivots and independent
reductions. Normal generation at degree at least `2g+1` supplies the
required product-space dimensions.

This gives a constructive RR/saturation route, not a theorem that ANY
generic plane presentation automatically has a faithful reduction or
polynomial generic RR coordinate sizes. Those checks belong to the
presented-curve input and upstream arithmetic model construction. The
source itself says at the beginning of Section 2 that constructing an
explicit `V1` basis can depend on the model and assumes it available.

## 4. No unbounded generic-choice retries are needed for the lift

The source describes practical randomized shortcuts, but a polynomial
clock need not rely on its “rare failure” comments:

* In DivAdd, compute ALL pairwise products of basis sections and take
  their span; the degree hypothesis proves surjectivity.
* In DivSub, impose the constraints from ALL basis sections. The source
  explicitly gives this option when dimension is not known in advance.
* In Algorithm 9, solve the full polynomial-size linear system instead
  of selecting random combinations of its equations.

These choices increase the genus exponent but remain polynomial. The
known RR dimensions and good reductions give the rank hypotheses of
Theorem 2.23 where it is used. Arbitrary p-adic matrices with unknown
characteristic-zero rank are not being admitted. The actual Jacobian
point and the high-degree effective-divisor presentation are essential
to this regularity argument.

Algorithm 9 then lifts a valid point modulo `P^e` to a valid point
modulo `P^(2e)`. Its geometric existence and the source's membership/
tangent-space construction are separate from merely lifting its matrix
entries. Properness/smoothness of the good model supplies actual points
behind these finite-level representatives.

## 5. Algorithm 10, uniqueness, and the characteristic-two correction

Assume `ell!=P`. The finite etale group scheme `J[ell]` gives a unique
`ell`-torsion lift of every residue `ell`-torsion point over the same
unramified local field. In a precision-doubling stage, any lifted point
differs from that torsion lift by an element of `J_e/J_(2e)`. This
quotient has exponent `P^e`. Hence an integer

```
N=0 mod P^e,          N=1 mod ell
```

removes the difference while preserving the desired torsion point.
This is exactly Algorithm 10. `N` can be chosen below `ell P^e`, so its
addition-chain length is `O(log ell+e log P)`. There are `O(log E)`
stages to output precision `P^E`. Ring arithmetic in the unramified
degree-`a s` extension has polynomial bit cost in `a s`, `E`, and
`log P`; together with Algorithm 9 this proves the stated lifting bound.

The source justifies the finite-layer exponent by claiming
`log:J1 -> P O_K^g` is an isomorphism. That assertion is false as
written at `P=2`, even with good reduction and an unramified base.
A concrete symbolic example is

```
E: y^2+xy=x^3+4x+1,       discriminant=-4225.
T=(-1/4,1/8).
```

The discriminant is odd, `T` satisfies the equation, and
`-(x,y)=(x,-y-x)` fixes `T`, so it is nonzero rational 2-torsion.
It reduces to the origin and has formal parameter `-x/y=2`.
Any formal logarithm kills this torsion, so it cannot be injective on
all of `J1`.

Algorithm 10 nevertheless remains valid at two: for EVERY smooth
commutative formal group, the ideal `P^e/P^(2e)` is square-zero, so
the formal group law there is its additive tangent law. This directly
identifies `J_e/J_(2e)` with the corresponding additive Lie module
and proves the exponent, without any global logarithm assertion.
Alternatively the available auxiliary restriction `P>2g` avoids two
for `g>=1`. Neither route changes the prime-to-`P` torsion hypothesis.

If the original torsion class was defined over the smaller residue
field before the evaluation-field enlargement, uniqueness implies its
lift descends to the corresponding smaller unramified field. Temporary
evaluation coordinates do not enlarge the intrinsic torsion field.
The same uniqueness makes lifting compatible with arithmetic Frobenius.

## 6. Canonical degree-g divisors are a separate regularity condition

Suppose one also wants the unique effective divisor in the class
`T+gO`. The necessary loss-free condition is

```
h0(C_bar, T_bar+g O_bar)=1
```

on the RESIDUE curve, not just `h0=1` on the characteristic-zero generic
fiber. At an effective divisor `D` of degree `g`, the tangent kernel of
the Abel map `Sym^g C -> Pic^g C` is
`H0(O(D))/H0(O)`. Its cokernel is `H1(O(D))`. Riemann--Roch makes
both vanish when `h0(D)=1`. Thus the Abel map is etale there, and
the residue divisor has a unique compatible Hensel lift along the
lifted line bundle. RR with independent reduction computes the
one-dimensional section space, or the corresponding closed-divisor
ideal, with unit-pivot precision.

The divisor can be retained as a closed effective Cartier divisor;
its individual geometric support need not split and may be nonreduced.
The required condition and the corresponding divisor/ideal chart must
be certified. If the residue class lies on the special locus where
`h0>1`, Mascot's arbitrary effective degree-`d0` representation still
lifts the torsion POINT, but this canonical degree-`g` extraction is
not supplied by the same unit-Jacobian argument.

## Unchanged global boundary

The source's Remark 1.6 explicitly says its subsequent identification
of p-adic values with rational coefficients is not guaranteed correct
and requires certification. None of the lifting arguments above bounds
the heights needed for that identification. A polynomial numerical
precision lifting algorithm is not a polynomial native reconstruction
precision theorem.

Accepted: closed-divisor conversion, one common polynomial-degree
evaluation field, actual evaluation-point lifts, the integral RR
saturation bridge under the stated faithful-presentation check, and
prime-to-`P` torsion lifting with a finite precision clock. Corrected:
the source's global logarithm assertion at two. Separate: residue
`h0=1` canonical-divisor extraction. Open upstream: the native
arithmetic good-model/RR presentation and uniform coordinate/height
bounds whenever they are not already supplied by the charged model.
No full surface point-counting or rational-reconstruction theorem is
claimed by this scoped lift result.
