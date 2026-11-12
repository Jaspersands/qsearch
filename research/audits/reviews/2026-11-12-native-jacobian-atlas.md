# Native fixed-format Jacobian equations and a complete addition atlas

2026-11-12. Independent source/construction review. Read current `STATE.md`,
`TRAPS.md`, `GOAL.md`, the narrowly supplied native-atlas corpus results, and
the actual primary `audits/sources/surface_module_2026/anderson_abeliants.txt`.
The source is Anderson, *Abeliants and their application to an elementary
construction of Jacobians*, arXiv:math/0112321v1, published in Adv. Math.
172 (2002), 169--205. Retained PDF SHA256:
`8893c5b76ee1da7ffd82f031b622b1f4078e892bc12fb60c0e29b9aa34fa432c`.
No Git, network, API, archive search, new code, or numerical experiment.
Interpreter if needed: `/opt/anaconda3/bin/python`.

## Verdict and exact theorem

The native fixed-format atlas input can be constructed. This is a
source-supported construction plus the finite evaluation/descent and exact
complexity arguments below; it is not a bit-complexity theorem stated in
Anderson's paper.

Let `K=Q(t)`. Supply homogeneous equations of degrees 5 and 3 defining a
smooth geometrically connected complete-intersection curve `C/K` in `P^3`.
Their coefficient rational functions have bounded `t`-degree and rational
coefficient bit size at most `B`. Here the ambient dimension, equation
degrees and `t`-degree bound are FIXED. Then `deg C=15` and `g(C)=31`.
There is a deterministic algorithm, polynomial in `B`, producing:

* a projective embedding of `Jac(C)` over `K`, with bounded ambient dimension;
* a saturated radical homogeneous defining ideal, with bounded number and
  degree of generators;
* the identity and inversion;
* a finite family of bihomogeneous polynomial addition formulas whose
  nonzero domains cover EVERY geometric point of `Jac(C) x Jac(C)`.

All numbers of variables, equations, formulas, their degrees, and the
degrees in `t` are bounded by constants depending only on the fixed input
format. Their rational coefficient bit sizes are `O(B+1)` with such a
constant; the weaker polynomial-height assertion follows. The constants
are enormous. This is an asymptotic native-construction result, not a
practical implementation claim or a genus-uniform polynomial bound.

No rational point of `C`, supplied Jacobian atlas, support-splitting field,
or extension of `K` is needed. Closed finite etale algebras suffice. The
initial task's description as a smooth plane curve was corrected by the
parent: the native genus-31 curve is the smooth `(5,3)` complete
intersection. Anderson's plane-curve Remark 4.5 is not used as though it
covered this input.

## 1. What the source proves, and what it does not supply

Anderson works over an ALGEBRAICALLY CLOSED field in Sections 3 and 4
(physical source lines 567ff and 1249ff). For an effective divisor `E`
of degree at least `2g+1`, put

```
n = h0(E) = deg(E)-g+1,
L = L(2E),
A = H0(C \ supp(E), O_C).
```

The full local source includes Section 2, omitted from one later paid
packet. Its definition (1)--(2) extracts coefficients from

```
trace(X0 * adj(sum_i t_i Xi) * X_(n+1) * adj(sum_i s_i Xi)).
```

Thus the abeliant is a universal polynomial with INTEGER coefficients,
valid over any commutative coefficient ring, homogeneous of total
degree `1+(n-1)+1+(n-1)=2n` in the matrix array. Transformation law
(3) multiplies it by `(det U)^2(det V)^2` when every matrix is
replaced by `U X V`. These statements are checked in the actual
source, not deduced merely from its abstract or the later equations.

The Jacobi matrices of Definition 3.7.3, equations (40)--(47), give a
projective variety identified with the Jacobian by Theorems 3.7.6 and
4.4.6. The source treats varieties, hence reduced structures; it does
NOT assert that the displayed generating equations themselves generate
a radical ideal. A radical/saturation computation is paid below.

Lemma 4.4.5 is stronger than a generic addition formula. For every pair
of Jacobi matrices `Z,Z'`, SOME specializations `s,s'` and row/column
permutations `P,Q` give a nonzero output. EVERY nonzero output produced
by the lemma represents their sum. The discriminant prefactors in that
lemma are essential to the latter assertion. The source ranges over
infinitely many specializations in `S=C\supp(E)` and invokes the
Nullstellensatz. It does not, by that invocation alone, supply a finite
native atlas, rational descent, or coefficient-height bound.

The construction below pays exactly those points. In particular, it
does not replace the infinitely many specializations by one generically
good choice and then silently claim completeness.

## 2. One fixed search constructs the divisor and all evaluation algebras

Choose two rational linear forms `l0,l1` whose common zero line misses
`C`. This is effective in a fixed finite grid. Indeed the resultant of
the degree-5 equation, degree-3 equation, `l0`, and `l1` is a nonzero
polynomial in the eight coefficients of the two linear forms, of
bidegree `(15,15)`. Its nonzero locus is nonempty since a general line
misses a projective curve in `P^3`. The grid `{0,...,30}^8` therefore
contains a successful choice. Test its resultant exactly over `K`.
All search sizes and resultant degrees are constants.

The basepoint-free pencil

```
u = l1/l0 : C -> P^1
```

is a finite separable morphism of degree 15. Its ramification divisor
has degree `2g-2+2*15=90`. Consequently at most 90 finite geometric
values have a non-etale fiber, and at most 90 rational integer
constants do.

For any integer `c`, form the degree-15 fiber algebra by dehomogenizing
`l0=1` and imposing `l1=c` together with the two curve equations.
Its length is 15. Compute its multiplication tables and test whether
the trace pairing is nondegenerate; in characteristic zero this is
equivalent to being finite etale. Each operation has fixed algebraic
format and polynomial bit cost.

For the explicit conservative pole bound used below, scan
`c=0,...,1875`. At least 1786 of these 1876 fibers are etale. Let the
first five successful values be `c1,...,c5` and set

```
F_E = product_i (l1-ci*l0),
E = div_C(F_E),        deg E=75,
n=75-31+1=45.
```

Here `E` is the REDUCED union of five disjoint hyperplane fibers, not
five times one fiber. It is linearly equivalent to `5H` and is defined
over `K`. Let `B_E=H0(E,O_E)`, a finite etale `K`-algebra of dimension
75. It is computed as the product of the five fiber algebras without
factoring them into fields or splitting any closed points.

The remaining 1781 successful fibers define a reduced divisor `T`
disjoint from `E`, of degree

```
N_T=1781*15=26715.
```

Let `B_T=H0(T,O_T)`, again given by its multiplication tables. This
is the single finite etale evaluation algebra used throughout. Its
geometric points need not be rational over `K`. No field extension,
primitive element, normal closure, or compositum is being supplied for
free.

## 3. Explicit RR spaces and the compression functional

For every positive integer `k` needed by the construction,

```
L(kE) = { Q/F_E^k : Q in H0(C,O_C(5k)) }.
```

All needed `k` are fixed constants. The homogeneous coordinate ring
computes these section spaces exactly. The Koszul resolution for the
`(5,3)` complete intersection is

```
0 -> O_P3(m-8)
  -> O_P3(m-5) + O_P3(m-3)
  -> I_C(m) -> 0.
```

The intermediate cohomology of line bundles on `P^3` vanishes, so
restriction of homogeneous degree-`m` polynomials onto
`H0(C,O_C(m))` is surjective. Its kernel is the degree-`m` part of
the homogeneous ideal generated by the two input equations. Thus
bases, multiplication maps, and all required subspace inclusions are
computed by fixed-size exact linear algebra over `K`; arbitrary RR
or normalized-plane-model oracles are unnecessary for this native
complete-intersection input. For `k>=1`,

```
dim L(kE)=75k-30.
```

Define a rational function

```
f_G = (F_E/l0^5)^4.
```

It has order exactly 4 at every point of `E`. For `h in L(4E)`, the
product `f_G*h` is regular along `E`; define

```
rho(h) = Tr_(B_E/K)((f_G*h)|_E).
```

This is explicitly computed: if `h=Q/F_E^4`, then
`f_G*h=Q/l0^20`, whose restriction is obtained in the finite fiber
algebras with `l0=1`. The trace is the trace of a known multiplication
matrix.

Because `E` is reduced and `B_E/K` is finite etale, the pairing
`(a,b) -> Tr(ab)` on `B_E` is perfect. Anderson Lemma 4.3.5 now
proves that `rho` is an `E`-compression functional on `L(4E)` for
EVERY relevant divisor class. For clarity, the required inequality
is `deg E>2g-2`, and the quotient maps used in that lemma are
isomorphisms by RR. This is not a separate generic condition on each
Jacobian point.

One must not use this ordinary trace argument on `E=5H` interpreted
as a nonreduced thickening: the trace pairing on a nonreduced finite
algebra is degenerate. Taking five distinct etale fibers above avoids
that error while retaining the same line-bundle class and degree.

## 4. Equations, identity, and the reduced projective structure

Use source Definition 3.7.3 in the finite-dimensional tensor spaces
just constructed. A convenient projective coordinate space for the
entry `Z12`, which determines every Jacobi matrix, is

```
W = L(2E)^(0) tensor L(2E)^(1) tensor L(2E)^(2)
    tensor [tensor_(i=3..n) L(4E)^(i)]
    tensor L(2E)^(n+1).
```

The superscripts label tensor factors. The source writes the middle
factors as the product space `L*L`; this is `L(4E)` by its stated
multiplication theorem (4.3.1). Here

```
dim W = 120^4 * 270^43.
```

This impractical but constant number is an honest bound on the native
ambient dimension. Reconstruct other matrix entries using the source's
linear permutation/identification rules and impose all consistency
identities. Expand the rank-one identity and abeliant identity in
bases of bounded-pole tensor spaces. This gives a finite homogeneous
ideal over `K`. Its displayed equations have degree at most `2n=90`
in the projective coordinates; all tensor spaces and multiplication
tables involved have fixed dimension.

For the identity, take a column `v` and a row `w` whose entries are
the computed basis of `L(E)`. The matrix `X0=v*w` represents the
divisor `E`, hence the zero class in Section 4.4.2. Its abeliant gives
the identity projective point. It is nonzero by Proposition 3.4.3.
Inversion is matrix transpose, as Lemma 4.4.3 states, and therefore
a linear coordinate operation on this model.

Take the saturation and radical of the homogeneous ideal. This extra
exact-algebra step is necessary: set-theoretic identification in a
source written in the category of varieties is not a proof that its
raw equations are a reduced scheme presentation.

Here is one explicit fixed-format way to pay that step, without an
integer-factorization oracle. Choose an affine chart containing the
computed identity. Its underlying variety is irreducible of dimension
31 by Anderson's Jacobian identification. Compute a Noether
normalization by 31 generic linear combinations of its coordinates;
the good choices contain an open set cut out by bounded-degree
conditions, so a fixed grid search with exact Groebner tests suffices.
Localize the resulting finite algebra at the rational function field
in these 31 normalization coordinates. It is a finite-dimensional
commutative algebra of bounded dimension over a characteristic-zero
field. Its nilradical is exactly the radical of the multiplication
trace pairing: nilpotents lie in that radical, and the reduced
quotient is a product of separable fields with perfect trace pairing.
Thus linear algebra computes the generic radical. Contract it using
denominator clearing and saturation (or localization/elimination).
Since the underlying affine variety is irreducible and dominant over
the normalization space, this contraction is precisely its prime
radical ideal. Homogenize and saturate to recover the reduced closure,
which is the whole projective Jacobian.

All Groebner/elimination degrees and finite-algebra dimensions in this
procedure are bounded in terms of the fixed number and degree of
the input equations. The procedure therefore uses a bounded-format
number of exact rational-function operations, whose coefficient
sizes are polynomial in `B`. Section 8 gives the common arithmetic
accounting. This is an additional effective-algebra argument; it is
not an assertion that Anderson analyzed radical algorithms.

## 5. A finite evaluation set detects EVERY discriminant

For every Jacobi matrix, each of its entries has per-tensor-factor
pole divisor at most `4E`. This follows directly from (42): `Z12`
has a factor `L(2E)` or `L(4E)` in each slot, and the only merging
used for a diagonal entry, `[1->2]`, combines two `L(2E)` factors.

The discriminant in (47) is a product of

```
3 + 2(n-2) = 2n-1
```

such entries after permutations of slots. Lemma 3.7.4 says it is
nonzero and has slots only `1,...,n+1`. Consequently

```
Delta_Z in tensor_(i=1..n+1) L(qE),
q=4(2n-1)=8n-4=356.
```

Evaluation `L(qE) -> B_T` is injective even after base change to an
algebraic closure: a nonzero function with pole divisor at most
`qE` has at most `q*deg E=26700` zeroes, whereas `T` contains 26715
distinct geometric points. Tensor products preserve injectivity over
a field. Therefore the universal evaluation of `Delta_Z` in

```
R = B_T tensor_K ... tensor_K B_T   (n+1 factors)
```

is nonzero for EVERY geometric Jacobian point `Z`. Over an algebraic
closure, `R` splits as the product of copies of that field indexed by
tuples in `T^(n+1)`. Hence some tuple has nonzero discriminant, for
each `Z`. The same finite `T` works simultaneously for ALL `Z`.

This is the effective replacement for the point-dependent
Nullstellensatz choices in Proposition 3.7.2 and Lemma 4.4.5.
There is no appeal to random generic specializations or an uncharged
enumeration of points of `C(K)`.

## 6. Polynomial coefficient descent gives a complete atlas over K

Perform the formula of Lemma 4.4.5 with the specialization slots
evaluated universally in `R` for `Z` and a separate copy of `R`
for `Z'`. For each of the finitely many `n^2`-by-`n^2` permutation
pairs `P,Q`, this produces a polynomial coordinate vector

```
F_(P,Q)(Z,Z') with coefficients in R tensor_K R.
```

Use the source's adjugate/determinant formula, INCLUDING both
specialized discriminant factors. No inverses in the finite etale
algebra are taken. The original function algebra of the curve is
still the domain `A`; the finite etale algebra is only a coefficient
algebra for evaluating polynomial formulas. We do not apply a
domain-dependent source theorem directly to an algebra with zero
divisors.

Choose a `K`-basis `e_1,...,e_r` of `R tensor R` and expand

```
F_(P,Q) = sum_j e_j * F_(P,Q,j),
```

where each `F_(P,Q,j)` is a vector of polynomials over `K` in the
two input projective-coordinate lists. These coefficient vectors
are the desired addition laws. The following argument proves both
correctness and completeness, including at special inputs.

Fix ANY geometric pair `(Z,Z')`. After splitting `R tensor R` over
the algebraic closure, each component of `F_(P,Q)(Z,Z')` is exactly
one of Anderson's point-specialized formulas. By Lemma 4.4.5(ii),
that vector is either zero or lies on the one projective line
representing `Z+Z'`. Changing from the primitive-idempotent basis to
the `e_j` basis expresses EVERY coefficient vector as a linear
combination of those component vectors. Therefore every
`F_(P,Q,j)(Z,Z')` is either zero or represents the same sum.

By Section 5 there are specializations with both discriminants
nonzero; Lemma 4.4.4 then supplies permutation matrices making the
output nonzero. Thus at least one component of some `F_(P,Q)` is
nonzero. Since basis change is invertible, some `F_(P,Q,j)` is
nonzero. This proves that their nonzero loci cover ALL geometric
pairs. It also explains why coefficient expansion is valid descent
here: it is not generally legitimate to expand an arbitrary
extension-defined projective map coefficientwise. It is legitimate
because every split component is zero or belongs to the SAME output
line at every input.

The intermediate formula can be computed in a larger bounded-pole
space. On the Jacobian product its nonzero outputs belong to the
required Jacobi coordinate space by the source lemma, and its other
outputs are zero. A fixed `K`-linear projection onto that coordinate
space, equal to the identity there, therefore puts every law into
the chosen ambient coordinates without altering its values on the
Jacobian product.

The formulas have a uniform bidegree. If `e=deg E`, the block `z`
in Lemma 4.4.5 has bidegree

```
(2n+3e, 2n+3e).
```

Indeed each specialized discriminant has degree `2n-1`, the
compression determinant has degree `e`, the two triangular factors
each have degree `e`, and the middle block has degree one in each
input. The abeliant is homogeneous of degree `2n`. Thus the output
laws can be taken of bidegree

```
(2n(2n+3e), 2n(2n+3e)) = (28350,28350).
```

Each vector's nonzero locus is an explicitly given open subset.
If an atlas of affine formulas is desired, refine it by the choice
of a nonzero output coordinate and divide the other coordinates by
that one. The number of refinements remains a fixed constant.
Completeness can also be certified computationally: on each pair
of standard projective input charts, append the vanishing of every
coordinate of every law and verify the unit ideal. Fixed-format
effective elimination pays that certificate as well.

## 7. Scheme identification, families, and descent to K

The source is applied over an algebraic closure only to prove its
geometric identification and the componentwise addition assertion.
All input section spaces, multiplication maps, `E`, compression,
defining equations, identity, and the descended laws above were
constructed over `K`. A bijection of geometric points alone would
not prove an isomorphism of varieties. The following family argument
supplies the missing morphism and verifies the scheme conclusion.

Work temporarily over an algebraic closure `Omega` and write
`P=Pic^0(C_Omega)`. A Poincare line bundle `Pcal` exists on `C x P`
after choosing a geometric basepoint for its normalization. The
bundles `Pcal tensor O(E)` and `Pcal^(-1) tensor O(E)` have degree
75 on every curve fiber, so their `H1` vanishes and their
pushforwards to `P` are locally free of rank 45, with formation
commuting with base change. On a local open set of `P`, choose
frames of both vector bundles. Their pairwise products give a
matrix with entries in the fixed vector space `L(2E)` tensored
with the coordinate ring of that open set. Each geometric fiber
is the Segre matrix representing its degree-zero divisor class.

Apply the universal abeliant polynomial. It is nonzero on every
fiber, and a change of either local frame multiplies it by the
unit `(det U)^2(det V)^2`. Consequently these local projective
maps glue to a MORPHISM

```
phi : Pic^0(C_Omega) -> J_red,Omega.
```

The target can indeed be the radical model: the source is reduced,
and every radical equation pulls back to a regular function
vanishing at all geometric points, hence to zero. Anderson's
Theorem 3.7.6 and divisor dictionary say that `phi` is bijective
on geometric points. Its image is closed by properness and is the
whole target; in particular `J_red,Omega` is irreducible. This
also justifies the irreducibility used in the radical algorithm.

The finite atlas of Section 6 defines an honest morphism on
`J_red x J_red`: its formulas agree on every overlap because they
agree at all geometric points of a reduced variety. Associativity,
identity, and inverse identities likewise hold as morphism
identities, since products of reduced varieties over a
characteristic-zero field are reduced. Thus `J_red,Omega` is a
group variety. Its smooth locus is nonempty, and translation
isomorphisms carry one smooth point to any geometric point.
It is therefore smooth, and hence normal.

The morphism `phi` is proper and quasi-finite, so it is finite.
In characteristic zero its generic field extension is separable;
bijectivity on geometric points forces degree one. It is a finite
birational morphism to a normal variety, hence an isomorphism.
It respects addition by the source's pointwise correspondence,
and consequently by equality of morphisms. This gives the claimed
isomorphism of group schemes, not just a set-theoretic dictionary.

Finally the correspondence is Galois-equivariant: `E` is defined
over `K`, changes of section bases do not change its projective
class, and changing the normalization of the Poincare bundle
does not change the geometric class correspondence. For every
Galois automorphism, the conjugate of `phi` agrees with `phi` on
geometric points and therefore as a morphism. Descent of morphisms
gives the isomorphism over `K`. No geometric basepoint was an
algorithmic input or a claimed `K`-rational point.

In particular, this does not identify every `K`-rational Picard
point with an actual `K`-rational divisor while ignoring its possible
descent obstruction. The identification is of the Jacobian varieties;
geometric divisor classes establish it, and the equations/laws
descend. The particular identity construction does use the actual
effective `K`-divisor `E`, which is already explicitly available.

## 8. Bit complexity, heights, and remaining boundaries

For fixed input format, every polynomial ring used has a fixed
number of variables and fixed degree bounds. Effective elimination
and Groebner degree bounds depend only on these quantities. Every
matrix has fixed size, including the huge tensor algebras and
radical calculation. Generic choices are made in fixed finite grids
and checked exactly. No search bound is allowed to depend on a
nonvanishing assertion without its fixed-degree bound.

The coefficient field is `Q(t)`, not an oracle field. A bounded
number of additions, products, determinants, gcds, and exact
divisions on bounded-degree rational functions with input
coefficient bit size `B` leaves degrees bounded and coefficient
bit sizes `O(B+1)`, with constants depending on the format.
Fixed-format Groebner and linear-algebra computations have the
same property through their bounded degree/size matrices. Rational
integer arithmetic then has polynomial bit cost. Trace algebras,
the radical procedure, and the coefficient descent use these same
operations; they do not require solving an arithmetic Diophantine
problem or finding rational points on `C`.

Thus the native atlas input is paid in the stated fixed genus AND
fixed ambient/degree/parameter-degree regime. The proof should not
be quoted as polynomial in a growing genus, growing plane degree,
or growing number of input equations. Nor does the original source
by itself pay arbitrary normalized-plane presentations; the
complete-intersection RR calculation above is why the actual
native input is covered without that extra step.

This is a result over `Q(t)`. Denominators and rank witnesses should
be retained for any later specialization. A claim about every
specialized fiber or every auxiliary prime requires its own good
specialization conditions. The construction proves no torsion
splitting-field degree bound, uniform torsion-coordinate height,
lifting precision, or rational-reconstruction theorem by itself.

## Disposition and next handoff

Accepted: Anderson supplies the geometric Jacobi model and genuinely
all-point addition mechanism. Proved here for the native `(5,3)`
format: bounded-height RR and compression data; a fixed closed-fiber
evaluation set detecting every discriminant; finite-etale
coefficient descent producing a COMPLETE finite atlas over `Q(t)`;
and a fixed-format radical/saturation step. Rejected as shortcuts:
using the algebraically closed convention without descent, calling
one generic law complete, assuming the raw ideal radical, or using
ordinary trace on a nonreduced `5H` divisor.

This changes the next mathematical obligation: the native Jacobian
atlas no longer needs to be an additional supplied oracle in this
fixed-format branch. Its use in the separate torsion-cover or
coordinate-height argument still requires checking that argument's
own hypotheses. No numerical control is needed to establish this
symbolic construction. Parent owns the shared `STATE.md`/handoff
updates; a mechanical source locator/cross-reference update is
sufficient after independent review of this note.

## Subsequent advisory-report check

After the independent construction above, read the completed
`audits/claude_runs/2026-11-12-native-atlas/response.md`. Its finite
evaluation and coefficient-descent arguments agree with this proof.
Its explicit obligations have these dispositions:

* O1, universal abeliant polynomial: resolved by actual source
  Section 2.1--2.2, including the integral polynomial definition,
  degree `2n`, and scalar frame-transformation law.
* O2, radicality/bit cost: supplied here by fixed-format exact
  elimination and the finite-algebra trace-radical procedure.
  No claim that the raw Jacobi equations are already radical.
* O3, identification as `Pic^0` over `K`: supplied by the Poincare
  family morphism, smooth group-variety argument, finite birational
  criterion, and descent in Section 7.
* O4, RR and multiplication: the complete-intersection Koszul
  calculation is explicit above; the required multiplication
  theorem is stated in actual source Section 4.3.1 with its precise
  degree hypotheses, which our degrees satisfy.

The report's alternative Gorenstein compression on a nonreduced
`E=5H` is mathematically repairable. Its degree-20 graded piece
must first be identified with `H0(E,O_E)` by division by the
chosen nonvanishing linear form to the twentieth power; that
graded piece is not an algebra under its raw graded multiplication.
Once trivialized, a generic perfect-pairing functional is found by
a fixed determinant grid. The reduced-fiber/trace construction in
Section 3 avoids this convention and its possible implementation
mistake entirely.

The report correctly warns against projecting the INTERMEDIATE
block `z` into `L(2E)` before computing its abeliant. The present
construction projects only the final output, after the source
proves that each such output is either zero or in the true Jacobi
space. Its explicit polynomial-time claim is accepted; any phrase
suggesting LINEAR bit running time is stronger than established.
Coefficient heights are linear in input coefficient heights at
fixed format; exact arithmetic time is polynomial. No finite
control or empirical confirmation is used to promote these claims.
