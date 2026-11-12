# Independent review: native natural torsion-module extraction

2026-11-12. Scoped analytical review of
`../../SURFACE_NATIVE_TORSION_MODULE.md`. No Git, network, API call, code,
numerical sweep, or quantum implementation. The interpreter, if needed, is
`/opt/anaconda3/bin/python`. The already reviewed open-cohomology dimension
lemma in `2026-11-12-surface-modular-descent.md` is an input to this review,
not re-proved here.

## Disposition and exact scope

The proposed construction correctly produces the COMPLETE geometric space

```
W = Hom_G(S,J_C[ell]),       S = M^vee,
```

from the presented curve and deck maps, with no supplied torsion basis,
zeta numerator, eigenvalues, or full torsion splitting field. For fixed
natural dimension `n` and branch number `r`, its bounded randomized cost
is polynomial in numerical `ell`, numerical characteristic `P`, the
charged presentation size, and `log(1/eta)`. Its accepted algebraic output
is exact; exhausting a clock returns `FAIL`.

The single field degree

```
H = ell^ceil(log_ell(2g)) * product_(1 <= j <= m)(ell^j-1),
m = (r-2)n,
```

works without assuming semisimple Frobenius. The nondegenerate-pairing
rank certificate handles Couveignes's possible strict-subgroup output.
Closed divisors over one explicit common constant field suffice; their
individual support points need not be simultaneously rational.

There is one arithmetic contract clarification. Actual `F_q` is computed
unconditionally on the containing space `V_small`. To call its restriction
an endomorphism of the natural isotypic span `E`, arithmetic conjugation
on `G` must preserve the natural representation. This is the intended
natural symplectic-normalizer setting. It should be stated, and can be
certified by the intertwiner equations below or directly by testing
`F_q(E)=E`. Mere knowledge that an arbitrary arithmetic automorphism
normalizes an abstract deck group should not silently replace that check.
No classification of all abstract symplectic-group automorphisms is used
in this review. This clarification does not obstruct construction of the
complete geometric `W`.

Even after this check, `F_q|E` does not select the scalar normalization of
Frobenius on the separate coefficient module. The original family's
arithmetic matrix on `W` remains conditional on its genuine coefficient
linearization. This is a separate input, not a failure of the torsion
construction.

## Primary statements actually checked

* `../sources/surface_module_2026/couveignes.txt`: model convention,
  physical lines 224-280; divisor arithmetic and RR, 285-370; Weil pairing
  Lemma 10, 621-660; Sections 6-8, 674-993; actual Theorem 1, 967-993.
* `../sources/surface_module_2026/lauder_wan_published.txt`: Theorem 1,
  83-99; Corollary 3 and its surrounding curve discussion, 157-193;
  actual Theorem 37, 1554-1573; Corollary 3 proof, 1577-1606.
* `../sources/surface_torsion_selection/kozen_resolution.txt`:
  introduction, problem statement, local reparametrization and the
  nonsingular stopping condition in Sections 2-4.
* `../sources/classical_surface_2026/function_rr.txt`: divisor conventions
  and numerical height, 260-282; Appendix B, 844-984, including Algorithm
  B.8 and Theorem B.9. These are classical RR statements.

The Kozen/RR interpretation agrees with the already reviewed scope in
`../../SURFACE_CLASSICAL_HEIGHT_UNIFORMITY.md`. The paid report was read
only for the stated arithmetic-normalizer/scalar warning. Its optional
prime-support and sharper descent claims are neither needed nor accepted
by this review.

## 1. Native zeta, normalization, and the degree-one divisor

Lauder--Wan Theorem 1 explicitly allows singular affine hypersurfaces.
For a bivariate equation, Theorem 37 has a fixed polynomial dependence
on the equation degree, numerical `P`, and `log q`. It is not a
`poly(log P)` theorem. A geometrically irreducible affine plane model and
its smooth projective normalization differ at finitely many closed
points. The Corollary 3 proof writes

```
Z_aff(T) = P_C(T) Q(T)/(1-qT),
```

where `P_C` is the desired smooth-projective numerator and every zero or
pole of `Q` is a root of unity. The proof explicitly recovers `P_C`, before
evaluating `P_C(1)` for the corollary's Jacobian-order output. Thus citing
that proof for the whole numerator is justified; citing only the wording
of Corollary 3 would have been insufficient.

The recovery is effective polynomial arithmetic. One can factor over
the rationals as described there, or remove cyclotomic factors. In the
latter route, a degree bound `N` implies `phi(s)<=N` for an occurring
cyclotomic factor, and the elementary bound `phi(s)>=sqrt(s/2)` bounds
the required indices by `2N^2`. There is no unbounded root-of-unity
search. Weight-one and weight-zero factors cannot cancel since their
complex root absolute values differ.

The smooth-model interface is also paid. Kozen produces branch data and
local parameters over individual residue fields. At a terminal local
chart the defining equation has nonzero derivative in the other
coordinate; ordinary formal Hensel expansion therefore supplies the
finite Laurent expansions requested by Couveignes. The model,
reparametrizations, residue degrees and requested precision are charged.
This does not require a common splitting field for every singular
branch.

After adjoining the fields of a fixed number of deck generators, choose
a regular fibre of the supplied separable map of degree `D`. A field
with more elements than the degree of the bad-fibre polynomial supplies
a good value by polynomially many tests; it has logarithmic extension
degree in that polynomial degree. Factoring the fibre and choosing ONE
irreducible factor gives a place with residue degree at most `D` over
that field. Adjoining its residue field makes it an actual rational
point `O`. Requiring the whole fibre to be irreducible is unnecessary
and would be wrong for many noncyclic covers.

The divisor `O` meets Couveignes Theorem 1's degree-one requirement with
positive degree one and negative degree zero. Moving the chosen regular
fibre to infinity also pays the conservative rational-infinite-place
convention of the RR source. Neither operation needs simultaneous
splitting of all places.

If `k0=F_(q^b)`, the known original numerator determines every required
extension numerator by powering its reciprocal roots algebraically,
using recurrences or resultants. An extension of degree `a` has
coefficient bit lengths `O(g*a*log q+g)`. All used extension degrees are
polynomial, so this is a paid computation, not new zeta advice.

## 2. The natural socle and bounded Frobenius factors

Write `F0=F_q^b`. Deck maps are defined over `k0`, so `F0` commutes with
their `G` action. Absolute simplicity and `End_G(S)=F_ell` imply that
evaluation induces an injection

```
S tensor Hom_G(S,V) --> V,       V=J_C[ell].
```

Its image `E` is the sum of all simple submodules isomorphic to `S`.
Equivalently it is the natural isotypic part of the socle. This argument
does not assert that the ambient modular representation is semisimple,
and uses no division by `|G|`.

Every endomorphism commuting with `G` acts on `E` as `I_S tensor B`.
Here `B` is an invertible `m` by `m` matrix because `F0` is invertible
on prime-to-characteristic torsion. Consequently every irreducible factor
of its characteristic polynomial has degree at most `m`. This is a
degree bound on the multiplicity space, not the much larger ambient
Jacobian dimension. The previously closed geometric lemma provides the
fixed value `m=(r-2)n`.

Let `a` contain the FULL powers of all irreducible factors of
`chi_F0 mod ell` of degree at most `m`, and let `b_poly` contain all
remaining primary factors. They are coprime. Primary decomposition gives

```
V = ker a(F0) direct_sum ker b_poly(F0),
dim ker a(F0) = deg a = u,
E subset V_small := ker a(F0).
```

Using full characteristic multiplicities is sufficient even if those
multiplicities exceed the minimal-polynomial exponents. Replacing them
by one copy of each irreducible factor would not be sufficient.

## 3. Self-duality and the universal field

After identifying `mu_ell` with the additive group `F_ell`, the Weil
pairing satisfies

```
<F0 x,F0 y> = q0 <x,y>,          q0=q^b mod ell.
```

Over an algebraic closure of the coefficient field, generalized
eigenspaces for `lambda` and `mu` pair to zero unless `lambda*mu=q0`.
For generalized eigenspaces this follows either from the adjoint
identity `F0^*=q0 F0^-1` and Bezout, or by applying that identity to the
primary polynomials. The map `lambda -> q0/lambda` is defined over
`F_ell` and preserves minimal-polynomial degree. Thus the union of ALL
primary factors of degree at most `m` contains each of its dual
partners. Its restriction of the Weil pairing is nondegenerate. This
does not assert nondegeneracy on a single arbitrary primary factor or
on `E` itself.

Set `L=product_(j=1..m)(ell^j-1)`. Every semisimple eigenvalue of `F0`
on `V_small` has order dividing `L`. Therefore `F0^L-I` is nilpotent
there, with nilpotence index at most `2g`. If `ell^c>=2g`, then in
characteristic `ell`

```
(I+N)^(ell^c) = I+N^(ell^c) = I.
```

Hence `F0^(ell^c L)=I` on `V_small`, including every ambient primary
nilpotent block. This proves rationality over the ONE field
`K=F_(q^(bH))`, with

```
H=ell^c L <= ell*(2g)*ell^(m(m+1)/2).
```

The bound is polynomial for fixed `m`. Since `m>=1` in the nontrivial
cover contract, `ell-1` divides `H`, so `mu_ell` also lies in `K`.
An empty target is handled separately without a torsion call; an empty
product must not be used to assert that `ell-1` divides `H`.

Some other ambient torsion may happen to become rational over `K`, but
no argument requires all of it to do so. Couveignes Theorem 1 computes
rational torsion over its input field, not the entire geometric torsion.
Its internal auxiliary extensions are already paid by that theorem's
polynomial bound and do not change its stated rational-divisor output.

## 4. Completeness despite a strict-subgroup trial

The actual Theorem 1 accepts the plane curve, its smooth model, the
degree-one divisor, `ell^k`, and the smooth-model zeta function. It
returns correct rational `ell^k`-torsion generators with probability at
least one half. On failure it may return nothing or a STRICT subgroup.
Its coordinate assertion must not be used as a membership/completeness
oracle on such a failed run.

The parent's stronger acceptance certificate avoids that trap. First
check every returned class is degree zero and killed by `ell`. Then
apply the CRT projector `p(F0)` with `p=1 mod a` and `p=0 mod b_poly`.
All accepted projected classes lie in `V_small`, regardless of whether
the generating call succeeded. Coefficients of `p` act by ordinary
integer multiplication modulo `ell` on torsion; they are not embedded
as scalars in the characteristic-`P` ground field.

For any projected list `v_1,...,v_t`, let

```
M_ij = log_zeta e_ell(v_i,v_j),       T=span(v_1,...,v_t).
```

The discrete logarithms are an `ell`-element lookup table after finding
and verifying a primitive `ell`-th root in `K`. Then

```
rank M <= dim T <= u.
```

If `rank M=u`, necessarily `T=V_small`. Conversely a spanning list has
rank `u` because the restricted pairing is nondegenerate. Thus a strict
subgroup can pass only if its projection already spans the ENTIRE needed
space. That outcome is sufficient. A nonsingular `u` by `u` pairing
minor supplies `u` independent classes, hence a basis. This certificate
does not infer absence from repeated failure and does not use the false
parabolic dimension as a stopping threshold.

## 5. Common closed divisors, coordinates, and Hom

Couveignes explicitly represents a returned class as `D-gO`, with `D`
an effective degree-`g` divisor rational over the input field. This
means a closed divisor, not a list of `K`-rational geometric points.
Each closed support place has degree at most `g`; an arbitrary lcm of
all those degrees can be superpolynomial and is never taken here.

All basic operations can retain closed-place ideals or orbit data.
RR constraints over a residue field are expanded as linear equations
over `K`; evaluation of a function at a closed divisor uses the
corresponding residue-field norm. Distinct places can be processed in
their individual residue fields. The total residue degrees are bounded
by the divisor degree, not by an uncharged common splitting degree.
This is the representation accepted by the classical ideal/infinite-
place RR algorithm and is also compatible with Couveignes's forms and
local-branch implementation.

Reduce after additions, scalar multiplications and CRT evaluations.
Every class then has a representative `D-gO`; intermediate divisor
degrees and requested RR heights remain polynomial. Frobenius and a
deck map act on BOTH parts of a degree-zero divisor. In particular,

```
F_q(D-gO) = F_q(D)-g F_q(O),
```

and `F_q(O)=O` must not be assumed when `O` was adjoined over `k0`.
The result can subsequently be reduced back relative to `O`.

`V_small` is `G`-stable because `F0` commutes with `G`, and is stable
under original `F_q` because `F_q` commutes with `F0`. For an image `x`
known to lie in this space, its pairings with the basis determine its
coordinates uniquely by a nonsingular linear system. Exact RR
principality checks may additionally certify reconstructed identities.

Solving the generator intertwiner equations computes
`Hom_G(S,V_small)`. Every map from `S` into `V` lands in `E`, already
contained in `V_small`; therefore this Hom space is exactly `W`.
Its dimension is `m`, and the `n*m` component vectors of a Hom basis
span `E` with that dimension. Thus there is no hidden target Hom lattice
or advice in this step.

## 6. Original arithmetic action and its scalar boundary

Fix the deck action convention, for example pushforward of divisors.
Applying `q`-power Frobenius to deck-map coefficients computes

```
alpha(g) = F_q g F_q^-1.
```

The induced map is compared with the explicitly supplied group action.
For the intended normalizer action, solve

```
A rho_S(g) = rho_S(alpha(g)) A
```

on the fixed set of generators. A nonzero solution is invertible by
absolute simplicity and is unique up to a nonzero scalar. This is a
polynomial, exact compatibility certificate. Its existence implies
`F_q(E)=E`; alternatively that equality is directly checkable in the
already complete basis of `V_small`. The actual matrix `F_q|E` comes
from the divisor action, not from a guessed characteristic polynomial.

For a SUPPLIED or CONSTRUCTED genuine coefficient linearization `A`,
the multiplicity-space action is

```
F_W(phi) = F_q composed_with phi composed_with A^-1.
```

Replacing `A` by `cA` changes this matrix by `c^-1`. Even a prescribed
symplectic multiplier can leave the sign ambiguity. An arbitrary
normalized solution of the intertwiner equations consequently cannot
be identified with the original family's coefficient Frobenius.

The choice `A=I` is valid only for the Frobenius of a base over which the
coefficient representation itself is specified to be constant. Making
the deck maps constant by passing to `k0` only makes `F0` commute with
`G`; it does not prove that the original coefficient action, or its
`b`-th power, has scalar one. The original coefficient, dual, and Tate-
twist conventions remain separate semantic data.

## 7. Finite clocks and final boundary

All acceptance operations above are exact finite-field/divisor or
linear-algebra calculations. Random factorization or field-construction
results can be verified by product and irreducibility checks. A failed
trial never returns a partial space as a complete one.

Let `T` be a proved expected polynomial bound for a full generating
trial, including its randomized arithmetic subroutines. If its success
probability is at least `1/2`, truncating at `4T` leaves success
probability at least `1/4` by Markov's inequality and a union bound.
Consequently

```
t = ceil(log(1/eta)/log(4/3))
```

independent trials fail with probability at most `eta`. Preprocessing
can be clocked with a separate allocated failure budget, or included
in the repeated trial. Polynomially many subsidiary calls require only
polynomial overhead and logarithmic error-budget dependence. Effective
clock polynomials are taken from the actual arithmetic algorithms;
this review establishes a constructive complexity theorem, not a tested
implementation with a newly measured bit-operation constant.

The strongest classical comparator is the existing Couveignes algorithm
with Lauder--Wan paying its zeta prerequisite. The new synthesis removes
the need to supply the complete natural torsion module for the presented
curve in the numerical-small-characteristic regime. It does not remove
native surface-to-cover construction, original coefficient arithmetic
linearization, good auxiliary-prime selection, characteristic-zero
lifting, uniform model/divisor heights, or CRT reconstruction. It does
not repair the false ordinary-invariant/parabolic identification.

No full point-counting algorithm, uniform `poly(log P)` algorithm,
novelty, hardness, speedup, or quantum-separation claim follows.

The parent should record this scoped conclusion and arithmetic contract
clarification in its shared handoff/state. No numerical control is needed
to establish these algebraic claims. A future implementation acceptance
test must verify the zeta/model prerequisites, `rank M=u`, the exact Hom
dimension, actual Frobenius action on both divisor parts, and the
normalizer compatibility certificate; it must preserve `FAIL` on any
exhausted or incomplete trial.
