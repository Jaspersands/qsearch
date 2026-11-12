# Native dyadic fields: squareclasses and consistent square roots

2026-11-13. Independent constructive audit of ONLY the local-field backend
in `LOCAL_KUMMER_NATIVE_END_TO_END.md`. No API, network, Git, numerical
control or whole-saturation inference. The native backend works. The
uniformizer paragraph needs the full integral kernel of reduction; its
mod-2 kernel alone fails for an unramified extension. A deterministic
construction below removes that ambiguity. Teichmuller lifts are valid
but unnecessary.

## 1. Exact scope and retained sources

Input is monic squarefree `f in Z[x]`, degree `n`, coefficient bits `B`.
Put `D=v_2 Disc(f)`. The discriminant is a nonzero integer of polynomial
bit size, so `D=O(n(B+log(n+1)))` and is computable from the native input.
The backend computes explicit squareclass coordinates for

    L=Q_2[x]/f = product E_i,

and, when all component labels vanish, one ACTUAL square root of an
element of `L*`, with a fixed selector permitting consistent refinement.
For a query element, a bound on its component valuations/nonzeroness is
required to bound the number of input digits read. Section 7 derives that
bound from the native coefficient/resultant bounds used by the candidate.
It is not an independent field/order/index input.

The following actual source passages were read.

* `audits/sources/dyadic_reset/om2012.txt`, physical lines 1171--1206:
  the computation model, precision cost and finite-field factorization;
  lines 1699--1789: Theorems 5.15, 5.17 and 5.18, including arbitrary
  requested factor precision. At base prime 2 their cost is polynomial in
  `n,D,P`; the displayed bound includes `n^(1+epsilon)D^(2+epsilon)`.
  Lines 128--175 also explicitly describe the stored residue-field tower,
  valuations and residual operators. Theorem 3.14, lines 865--867, pays a
  common OM factor description at precision `D+1`.
* `audits/sources/local_kummer_cluster/integral_bases.txt`, lines
  194--240: Proposition 1 constructs the local integral basis
  `g_j(theta)/2^eta_j` from an Okutsu frame, with denominators bounded by
  the integrality exponent. The OM approximant selects its actual factor.
  Lines 328--398 give the finite-precision OM stability theorem and its
  proof. Lines 119--124 explicitly distinguish computation at a specified
  prime from global integral-basis computation. The global Theorem 1's
  supplied index factorization is NOT being used as native advice.
* `audits/sources/local_kummer_cluster/local_factorization.txt`, lines
  516--558: Theorem 4, Corollary 3 and Remark 8. At residue characteristic
  2 retain the extra `D^2` term; do not import the `p>degree` estimate.
  Remark 8 explicitly pays a primitive representation of a residual
  extension when the chosen finite-field factorization routine requires
  one. Alternatively the subsequent finite-ring operations below work
  directly in a finite-dimensional field algebra and need no primitive
  element.

These results supply computed integral bases and multiplication tables,
not the finite-ring claims proved below. They require neither an integer
factorization of the discriminant nor a compositum of local fields.

### Actual-factor and basis selection: the omitted primary-text chain

The subsequently completed paid unit report flags missing excerpt-level
justification here. The following additional passages of the FULL retained
primary resolve its mathematical questions.

1. In `om2012.txt`, physical lines 670--713, Proposition 3.8 identifies
   condition (12) with being an OM factorization. Corollary 3.10 then
   supplies faithful representation. Lines 749--752 explicitly state
   that Montes produces that faithful family and the required OM
   factorization. These are output properties, not extra inputs to
   Theorem 5.18.
2. The actual algorithm, lines 1054--1106, takes ANY monic separable
   polynomial and returns OM representations of its actual local
   irreducible factors. The paragraph following OUTPUT says the leaves
   correspond one-to-one with those factors. This does not assume that
   the native squarefree polynomial is irreducible over Q.
3. Lines 101--130 define an OM representation of an ACTUAL irreducible
   factor from its Okutsu frame. Therefore the stored lower frame
   polynomials are already a frame for that actual factor. The local
   Proposition 1 of `integral_bases.txt` applies to precisely this datum:
   its local `F in O_p[x]` is irreducible, irrespective of whether the
   original input had several rational factors.
4. The integral basis is `g_j(theta_i)/2^eta_j`, with
   `theta_i=x mod F_i` in the ACTUAL selected factor. It is never first
   constructed at a root of the finite approximant and then transferred
   by an unjustified root identification. The `g_j` use only the lower
   frame polynomials, not the last degree-`d` approximant. Their
   valuations, hence `eta_j`, follow from the explicit frame valuation
   formula in `om2012.txt` Lemma 1.5(3), physical lines 231--237.
5. Finite computation of this datum is paid by Theorem 3.14 at `D+1`
   digits and the subsequent Montes/SFL complexity theorems. A
   conservative `D+2` starting precision avoids endpoint conventions.
   Independently, `integral_bases.txt` Theorem 3, lines 353--398,
   proves stability from finite precision, including its actual-factor
   approximation guarantee; this is a theorem with a printed proof,
   not merely an organisation paragraph.

Thus a factor can be named by its finite, faithful OM identifier together
with the original exact `f`. Refinement means refining that unique factor.
An infinite list of factor coefficients, a chosen embedding into an
algebraic closure, and an isomorphism from an approximant field are not
inputs. The global irreducibility assumption in the integral-basis paper's
global complexity section is not transplanted to the local Proposition 1.
No Round-2 maximality criterion recalled from memory is used.

## 2. No missing order or CRT index

Let `A=Z_2[x]/f` and `O=product O_E`. The discriminant identity gives

    D = v_2 disc(O) + 2 length_Z2(O/A).

Thus the total index length `I` is at most `D/2`; every elementary divisor
of `O/A` is at most `I`. In particular `2^I O subset A`. This bounds all
denominators in the combined integral-basis/CRT conversion by a known
native quantity. For an individual factor, the Okutsu basis denominators
are also at most `D/2`. The actual index need not be supplied or guessed.

Freeze the finitely represented OM factors, frame polynomials and basis
numerators after preprocessing. Their meaning is evaluation in the actual
factor of the original `f` selected by the OM description. Later refinement
uses the SAME factor, via single-factor lifting. An approximate factor is
not silently substituted for that actual local field.

Products of basis numerators, monic reduction modulo the selected factor,
and triangular conversion give its integral multiplication table to any
requested precision, with a polynomial additional `D` guard. One may use
the coarse denominator bound above instead of discovering the optimal
guard. For example, basis entries in a power basis have poles at most
`D/2`; their pairwise products have poles at most `D`, and conversion from
the power order into the integral basis is integral. Rational matrix
inversions incur at most twice their bounded denominator loss when their
input coefficients are refined. This is a fixed guard, independent of the
requested output precision.

## 3. Residue field and a deterministic uniformizer from the table

Fix one factor `E`, degree `d`, with computed integral basis
`omega_1,...,omega_d`. Write `O=O_E`, `m=m_E`. Work first in the explicit
`d`-dimensional F2-algebra `T=O/2O`.

Let `h=ceil(log_2 d)`. The kernel of the F2-linear map

    T -> T,       z |-> z^(2^h)

is precisely its nilradical `m/2O`: the latter has nilpotence exponent
`e<=d`, while the induced Frobenius on the residue field is injective.
Compute this kernel by repeated squaring and binary elimination. Its
quotient is the actual residue field `k=O/m`, with a multiplication table.
Its F2 dimension is `f_res`, and `e=d/f_res`. Fixed quotient pivots give an
F2 basis of `k` and integral lifts `beta_1,...,beta_f_res`.

Lift a basis of that kernel to the integral basis with 0/1 coordinates,
and add `2 omega_1,...,2 omega_d`. Their Z2-span is the FULL lattice `m`.
An integer Hermite calculation on this small 0/1/2 matrix produces a
Z2-basis `v_1,...,v_d` of `m`. Its inverse coordinate conversion loses at
most one binary digit, because `2O subset m`.

Here is an explicit construction of `m^2` sufficient to choose a
uniformizer without an OM valuation call. Compute the `d^2` products
`v_i v_j`, express them in the `v` basis, and reduce those coordinates
modulo 2. Their F2-span is `m^2/2m`, since `2m subset m^2` and products of
the Z2-basis generate the product ideal. The quotient

    (m/2m)/(m^2/2m) = m/m^2

has dimension `f_res`. Choose the first `v_j` whose class is nonzero.
It is a uniformizer `pi`. Only multiplication-table accuracy modulo 4
is needed for this step, after the basis-conversion guard.

An independent alternative is to test the norms of the `v_j`: some has
`v_2 Norm(v_j)=f_res`, since otherwise the whole basis would lie in
`m^2`. Norms modulo `2^(f_res+1)` suffice to identify one. Both procedures
are deterministic and use polynomial-size matrices.

The candidate's random construction is also valid if it samples the full
lattice `m/2m`: this surjects uniformly onto `m/m^2`, so success probability
is `1-2^(-f_res)`. Sampling only lifts of `ker(O/2O -> k)` omits necessary
generators; in the unramified case that kernel is zero whereas `m=2O`.

## 4. Exact triangular presentation, without unit enumeration

Normalize the discrete valuation `w` by `w(pi)=1`, so `w(2)=e`. Set

    N=2e+1,   U_i=1+pi^i O,
    g_(i,j)=1+pi^i beta_j  (1<=i<N, 1<=j<=f_res),
    M=(N-1)f_res=2d.

Hensel at 1 proves `U_N subset U_1^2`: for `u in U_N`, the equation
`z^2=u` has a unique solution in `1+pi^(e+1)O`. Its derivative has
valuation `e`, while the initial residual has valuation at least `2e+1`.

For an element in `U_i`, reduce `(u-1)/pi^i` in `k`, express the residue in
the fixed F2 basis, and divide by the corresponding product of
`g_(i,j)`. The result belongs to `U_(i+1)`. Successively doing this gives
a 0/1 vector `c(u)` of length `M`, representing `u modulo U_N`. At each
level the quotient is the additive group of `k`, so collection requires
only linear algebra and field operations, never enumeration of `k`.

Every `g_(i,j)^2` lies in `U_(i+1)`, because

    g_(i,j)^2-1 = 2 pi^i beta_j + pi^(2i) beta_j^2.

Collect its square to a 0/1 vector `c_j` supported only at later levels.
Let `R` have columns `2 e_j-c_j`. In increasing level order it is
triangular with diagonal 2, hence `|det R|=2^M`. The map

    Z^M/R Z^M -> U_1/U_N,    e_j |-> g_j

is surjective. The target has order
`product_(i=1)^(N-1) |U_i/U_(i+1)|=2^M`, so it is an isomorphism.
Consequently

    U_1/U_1^2 = F2^M / image(R mod 2).                 (1)

The first equality uses the already proved `U_N subset U_1^2`. Compute
explicit coordinates for this quotient by binary elimination. Relations
have entries only 0, -1 and 2; their number is linear in `d`.

## 5. Labels and roots: inverse Frobenius replaces Teichmuller lifting

For `a in E*`, compute `r=w(a)` and write `a=pi^r u`, with `u` a unit.
The residue field has characteristic 2, so squaring is an automorphism.
Compute `gamma=sqrt(bar u)` by inverse Frobenius, using `f_res-1`
squarings, and take its fixed integral lift `beta` via the residue basis.
It is a unit, and

    v=u/beta^2 belongs to U_1.

The squareclass label is `r mod 2` together with the image of `c(v)` in
(1). This is exact: the residue part removed was an actual square, and
any other lift changes `v` by a square in `U_1`. Multiplication of labels
therefore agrees with multiplication in `E*/E*^2`. There are at most
`2d+1` displayed bits before discarding dependent coordinates.

If the label is zero, `r=2t` and `c=c(v)` belongs to `image(R mod 2)`.
Solve

    R lambda = c mod 2,    lambda in {0,1}^M,
    x=(c-R lambda)/2 in Z^M.                           (2)

Every coordinate of `x` has magnitude at most `M+2`. Equation (2)
implies `2x=c` in the presented group. Thus

    v_0=product_j g_j^(x_j),
    s_0=pi^t beta v_0,
    a/s_0^2 in U_N.

Negative exponents are inversions of units. Only polynomially many
multiplications and binary linear operations occur. In particular the
halving equation does not require integer SNF, a discrete logarithm, an
enumeration of `2^d` unit classes, or a search over root signs.

Let `h` be the unique square root of `a/s_0^2` in
`1+pi^(e+1)O`. Then `s=s_0 h` is an ACTUAL square root in `E`.
For the product algebra perform this independently in each actual factor
and use the paid CRT conversion. The sum of field degrees is `n`.

The candidate's Teichmuller alternative is also correct: the derivative
of `z^(2^f_res)-z` is a unit, and binary exponentiation needs only
`O(f_res)` multiplications. Its exponential polynomial degree is never
materialized. The construction above avoids this additional lifting step.

## 6. Consistent selectors and a fixed additive precision guard

Freeze the factor identifiers, integral bases, residue pivots, chosen
`pi`, generator order and binary-elimination pivots. Then the finite
data `r,c,lambda` are stable once the requisite unit residue is known.
The selected root is specified by the exact target expression together
with the certified ball

    s in s_0 (1+pi^(e+1)O).                            (3)

There is exactly one root in (3). Thus subsequent computations refine
the same root, rather than repeating an arbitrary sign choice. The
description uses finite arithmetic expressions and a Hensel ball in the
already selected actual factor, not supplied infinite coefficients.

For a wholly finite residual certificate, let `r=w(a)` and keep an
approximation `a_tilde` with `w(a_tilde-a)>2e+r`, together with
`s_tilde` satisfying

    w(s_tilde)=r/2,
    w(s_tilde^2-a_tilde)>2e+r.                         (4)

Then the same strict residual inequality holds for the actual target.
Hensel identifies the unique root with
`w(s-s_tilde)>e+r/2`; the other root is at distance exactly `e+r/2`.
The constructed `s_0` satisfies (4) before numerical truncation, since
`a/s_0^2 in U_(2e+1)`. Approximating it beyond `e+r/2` preserves the
strict certificate. Retain this ball during every refinement instead of
re-solving (2) with newly chosen elimination data.

The following loss ledger makes the guard independent of the number of
refinements. Suppose `|w(a)|<=V`; round `V` up to a nonnegative integer.

* Multiplication matrices of integral elements have integral entries.
  A unit has an integral inverse. These operations do not lose digits
  in an integral basis.
* `v_2 Norm(pi)=f_res`. The adjugate formula therefore bounds the poles
  of the matrix of multiplication by `pi^(-i)` by `i f_res`.
  The collection procedure has `i<N`, so this loss is at most `2d`;
  allowing `i=N` still costs at most `3d`. Refining the inverse matrix
  itself costs at most twice this guard, by
  `A^(-1)-B^(-1)=A^(-1)(B-A)B^(-1)`.
* Normalizing `a` by `pi^(-r)` costs at most `dV` digits by the same
  conservative adjugate bound. The final factor `pi^(r/2)` costs at
  most `dV` when its exponent is negative. Refining these fixed powers
  and their inverses costs at most twice their pole bounds. Unit
  products and their possibly negative exponents in (2) add no loss.
* On the selected unit ball the square map has an exact distance rule:
  for `h_1,h_2 in 1+pi^(e+1)O`,

      w(h_1^2-h_2^2)=w(h_1-h_2)+e,

  because `w(h_1+h_2)=e`. Its inverse loses exactly ONE binary digit,
  independent of the requested precision. Newton's map
  `(z+u/z)/2` contracts errors on this ball; its fresh rounding loss
  is one digit and does not accumulate once per iteration. Doubling
  precision, or computing with this fixed extra guard, yields the
  selected root in polynomial bit cost. This is stronger than merely
  invoking an unquantified root routine.
* Conversions to and from native polynomial coordinates incur the
  index/CRT guards of Section 2, bounded by a polynomial in `d,D`.

For example, the deliberately loose additional binary precision

    C_local=20(d+1)^2(D+V+1)

dominates these table, inverse, normalization, collection and root
guards. Computing the target and fixed field data to `P+C_local` digits
is sufficient for `P` output integral-basis digits. For all factors and
the combined native CRT map replace `d` by `n` in this coarse bound.
The assertion is an additive `P+C_local` bound, not a recursive
precision assignment `P_next=poly(P_previous)`.

Valuation discovery also fits the same fixed budget. Scale an element
into `O`, compute its multiplication determinant to the known valuation
cap, and use `v_2 Norm(a)=f_res w(a)`. No exact zero test at unbounded
precision is used. Alternatively division by the now computed `pi`
and residue testing terminates after at most the explicit valuation cap.

## 7. Native caps and bounded-error bit cost

If a polynomial representative `A(theta)` has coefficient poles at
most `S`, all component values have normalized valuation at least `-S`.
If it is nonzero in all factors and

    v_2 Res(f,A) <= K,

then, writing `d_i=[E_i:Q_2]` and normalizing `v_2(2)=1`,

    sum_i d_i v_2(A(theta_i)) <= K,
    v_2(A(theta_i)) <= (K+(n-d_i)S)/d_i <= K+nS.

Thus one can take, for every field,

    V=n(K+nS+S+1)

in Section 6. The source/half/pencil coefficient and branch-resultant
caps already supply such polynomial `S,K` in the candidate. This is
the precise reason nonzero component valuations are polynomially bounded.

For an initial branch divisor, `a` is a product of distinct local factors
of `f` and `f_1=f/a`. The stated branch representative is, up to sign,
`a-f_1`: it equals `-f_1` on components of `a` and `a` on the other
components. It is nonzero everywhere and integral. Its norm has
valuation `2 v_2 Res(a,f_1)<=D`, by the discriminant product formula.
No branch-value zero is mistaken for a squareclass representative.

OM preprocessing is Las Vegas with expected polynomial bit cost;
finite-field factorization and, when used, residual primitive-element
construction are included. Given an expected bound `T`, stop an attempt
after `2T` steps and restart with independent randomness. Each attempt
finishes with probability at least one half, by Markov's inequality.
After `ceil(log_2(1/eta))` attempts the only remaining outcome is explicit
ABORT of probability at most `eta`. This changes the bound by a factor
polynomial in `log(1/eta)`, rather than `1/eta`. Correct completed outputs
are not probabilistic guesses. Later SFL refinement and the finite-ring
backend are deterministic for the frozen preprocessing data.

The resulting local-field backend has bounded bit cost polynomial in
`n,B,P,S,K,log(1/eta)` and no missing order, residue, valuation, root-sign
or splitting-field advice. This review establishes that interface only.
The separate whole-DAG review must still assign the native `S,K,P` and
the total error budget to every call; the backend proof does not by
itself establish the entire local-image/saturation algorithm.
