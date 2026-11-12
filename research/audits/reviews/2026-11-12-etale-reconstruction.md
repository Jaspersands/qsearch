# Finite etale reconstruction and actual target Frobenius

2026-11-12. Independent core review of
`../openai_runs/2026-11-12-target-etale-reconstruction/response.md`
against its explicit target-closure obligation and the current `STATE.md`.
Read the full report and the completed full-similitude, target-unramified,
target-prime-model, closed-divisor-encoding, and numerical-closed-algebra
reviews. The last microlemma is reused under its precise input contract,
not re-proved. No shared note, Git, network, API, archive, implementation,
or numerical sweep was used. Commands used `/opt/anaconda3/bin/python`.

## Disposition

ACCEPTED as a complete reconstruction/readout bridge under the native
geometric hypotheses and the already proved effective interfaces. The
report's conditional finite-set theorem is correct. Its assumption of
an actual globally stable group is supplied explicitly below, rather
than inferred from a dimension check or a concatenation of component
socles.

The most efficient safe specialization reconstructs the actual torsion
subgroup

```
U = {phi(s0) : phi in Hom_Gamma(S,V)},
S=N^vee constant,       0!=s0 in S,
V=J_(C_full)[ell].                                      (1)
```

Evaluation is an injective Galois-equivariant map. Thus `U` has rank
`m=(r-2)n=13516` for `n=62,r=220`, and its ACTUAL Frobenius is exactly
the desired multiplicity-space Frobenius. It is generally not
Gamma-stable. This specialization does not reconstruct a deck action
on `U` or subsequently take another Hom space.

The report's original full-natural-socle route is also valid. Its rank
is `R=n*m=837992`, not `(ell-1)*R`; Section 2 gives its explicit
polynomial construction. Both routes use the whole full-frame geometry.
A class chosen only in one symplectic component would not by itself
give the required global arithmetic object.

All-pairs scalar coordinates are genuinely Galois equivariant; intrinsic
height bounds imply an effective rational reconstruction threshold;
the relation idempotent and linear equalizer give the ACTUAL coordinate
algebra of the group; and known-prime maximalization recovers its
faithful target reduction. The matrix-only kernel-rank method is valid
and avoids a target splitting field entirely.

The original basepoint fibre need not be unramified at the target prime
when quotienting is performed BEFORE maximalization. Only the final
group `U` or `E` needs that property.

## 1. Inputs, notation, and which earlier gates are being composed

Let `Gamma=GSp_n(F_ell)` and `G=Sp_n(F_ell)`. The genuine normalized
frame cover and its rational right deck action come from
`SURFACE_NATIVE_COVER_CONSTRUCTION.md` and the normalized-frame review.
Its geometric compactification is the disjoint union of the components
`C_zeta`, indexed by primitive roots. Write `g_C` for one component's
genus, `s=|Gamma|`, and

```
A(h)=R_h^*,             P(h)=(R_h)_*=A(h^-1).
rho_S(h)=h^(-T).
```

All deck maps are defined over `Q`; Galois acts trivially on the
CONSTANT coefficient space `S`. The geometric compact/open comparison
and dimension `dim Hom_Gamma(S,V)=m=(r-2)n` are already proved.

At a small auxiliary prime `P`, the native module algorithm supplies
the complete relevant primary space and exact Hom basis on a chosen
component. Its pairing-rank certificate, common field bound, and finite
clocks remain in force. The good auxiliary normalization/RR input and
unique prime-to-`P` torsion lifts are supplied by the native-normalization
and numerical-lifting results. The stable support-height chain and
closed `A,B,C` coefficient-height theorem are also supplied.

The formerly separate numerical conversion to `A,B,C` is now paid by
`2026-11-12-numerical-closed-algebra.md`: ONE subspace
`H^0(A-D)` inside an enlarged fixed-pole `H^0(A)`, a smaller pole space
surjecting onto the quotient, and unit-minor solves produce the genuine
closed algebra and coordinate multiplication matrices at full precision.
Its cyclic power-basis solves use no integer divisions and retain jets.
The enlarged evaluation bank and all normalization-denominator zeros
are charged there. This is the precise interface used below; a numerical
Groebner calculation over a nonfield is not substituted for it.

At the prescribed target `p!=ell`, use the native unramifiedness theorem:
under the original smooth-pencil, disjoint-branch, and genuine-open-frame
hypotheses, tame Kummer killing and purity give a smooth proper compact
cover without a ramified base extension. Thus its Jacobian ell-torsion
and every Galois-stable subgroup used below are unramified. The theorem's
actual native hypotheses must remain in the composition; generic
horizontal inertia alone would not suffice.

### The class-dependent section subspace is constructed, not supplied

The remaining apparent input `W=H^0(A-D_t)` can itself be obtained from
the paid numerical Jacobian algorithms. This step must be included;
the closed-algebra microlemma alone would not have supplied it.

After selecting the canonical basepoint `b`, initialize the known KM
background with

```
D0=d0*b,       d0>=2g_C+1,
E1=(d0-g_C)*b,       B=(d0+g_C)*b.
```

Convert the residue class by ordinary closed RR in this background and
perform its unique numerical ell-torsion lift there. Re-running the
lift is allowed and has the same polynomial bound; a cost-free numerical
change of KM representation is not assumed. If separate backgrounds
are used for the polynomially many basepoints, uniqueness identifies
their lifts with the same actual torsion points.

Mascot, `mascot_lift.txt`, Section 2.2.3, Algorithm 7, physical lines
713--780, gives

```
[D0-E1-E_x]=x.
```

Feed `x=-t` and stop at line 5, as Remark 2.21 explicitly permits
(physical lines 832--849). Then `E_x=D_t`, and the actual output is

```
W0=H^0(2D0-E1-D_t)=H^0(B-D_t).                           (1a)
```

Its intermediate rank-one space is precisely the line bundle class
`t+g_C*b`; the imposed residue `h^0=1` gives `h^1=0`, so the primitive
section and all source DivAdd/DivSub steps have the compatible
unit-rank lifts. The source Remark's prose has the opposite class
sign from its equation (2.15); the equation and algorithm above fix
the sign. There is no use of the optional second-divisor scalar map.

To convert (1a) to the microlemma's fixed-pole space, let
`H=pi^*(infinity)` and let `Cpole=D_plane*H` be the known coordinate
pole allowance after the paid monic-generator transformation. Increase
the pole choice to

```
A0=k0*H,       deg A0 >= d0+3g_C+1,
A=A0+Cpole.
```

This keeps `deg A=O(g_C+D_plane^2)` and all of the microlemma's
coordinate-multiplication room. It also gives

```
deg(B-D_t)=d0>=2g_C+1,
deg(A-B)>=2g_C+1.
```

Compute the KNOWN-basepoint space `H^0(A-B)`: it only imposes jets
at `b` in the already paid `H^0(A)`. The chosen fibre is unbranched
and faithful modulo `P`, so `x-a` is a local parameter and the
required implicit-series/jet solves use units. Since `H^1(A-B)=0`,
restriction to these jets is surjective and its kernel has unit
minors; no unknown canonical-divisor ideal is used.

The actual multiplication theorem quoted by Anderson 4.3.1,
physical lines 1358--1363, states

```
deg L>=2g_C+1, deg M>=2g_C
  => H^0(L+M)=span H^0(L)*H^0(M).
```

Apply it to `L=B-D_t` and `M=A-B`. Thus on the residue curve

```
W0 * H^0(A-B) = H^0(A-D_t).                              (1b)
```

The two factors and the target are nonspecial and have free section
modules with base change. Surjectivity modulo `P`, followed by
Nakayama, proves (1b) over the complete finite-precision ring too.
Select the requisite residue-independent product columns; their unit
minor gives a basis of the FULL target subspace inside `H^0(A)`.
Poles at `b` cancel against the known vanishing imposed by `A-B`.
Products can be converted from evaluations to coefficients using the
microlemma's enlarged bank and unit interpolation matrix.

Consequently the class-dependent input to the closed-algebra
microlemma is now explicitly paid. Its finalized Section 7 independently
checks this same product construction, including the degree and Smith
rank conditions in Algorithm 7 and the enlarged multiplication ambient.
It uses only known-background section spaces and the actual source
algorithms; no canonical ideal or inverse-Abel oracle is supplied.

## 2. Explicit full-Gamma construction and the fixed ranks

Fix a component `C_0=C_zeta0`. The small-prime algorithm computes

```
W0=Hom_G(S|G,J_C0[ell]),
phi_1,...,phi_m a basis of W0.
```

Choose, for every `a in F_ell^*`, a matrix `g_a in Gamma` of multiplier
`a`, with `g_1=1`. The already checked Shapiro extension is explicit:

```
phi_(j,a)(v) = P(g_a) phi_j(g_a^(-T) v),                 (2)
```

on `C_(zeta0^a)`. Its direct sum over the components is a full
Gamma-equivariant map `Phi_j:S -> V`. This follows from the exact
pullback convention, equivalently
`A(h) Phi_j = Phi_j rho_S(h)`; changing coset representatives cancels
by the original `G` intertwiner relation. No averaging over the modular
group is used.

Each component in (2) is computed by an explicit fixed-dimensional
linear combination of the known torsion classes, followed by a known
deck map. It is not just the deck translate of `phi_j(v)`: the
precomposition `g_a^(-T)` is essential. All values lie in the native
module's ONE common auxiliary field, which already contains the
cyclotomic component field. No new support field is needed.

For a basis `e_1,...,e_n` of `S`, the `n*m` full tuples

```
T_(i,j) = Phi_j(e_i)
```

are linearly independent. Projection to component zero is the
evaluation map `S tensor W0 -> J_C0[ell]`, whose injectivity follows
from absolute simplicity of `S|G` and its scalar endomorphism ring.
Their span is exactly the natural Gamma-socle

```
E=im(S tensor Hom_Gamma(S,V) -> V),
dim E=n*m=R.                                            (3)
```

Thus constructing and enumerating this group has size `ell^R`.
Concatenating independently chosen component socles instead gives
dimension `(ell-1)*R` and would destroy the fixed-rank polynomial
bound. That larger group is not the output of (2)--(3).

### Evaluation at one fixed vector gives the smaller actual subgroup

Now fix a nonzero vector `s0` of the CONSTANT `S`. A nonzero
Gamma-map from the simple module `S` is injective. Equivalently, the
Gamma orbit of `s0` spans `S`. Hence

```
Phi(s0)=0  =>  Phi=0.
```

Moreover, for every Galois element `sigma`,

```
sigma(Phi(s0)) = (sigma composed_with Phi)(s0),
```

and `sigma composed_with Phi` is again a Gamma-map because deck maps
are rational. This proves that (1) is an actual Galois-stable subgroup
of the product Jacobian's ell-torsion and that

```
ev_s0: W=Hom_Gamma(S,V) -> U
```

is an isomorphism of Galois modules. Its basis is the explicit list

```
u_j = Phi_j(s0),
(u_j)_a = P(g_a) phi_j(g_a^(-T) s0).                     (4)
```

The vectors `phi_j(s0)` on component zero are already independent;
the same holds after projection to any component since
`g_a^(-T)s0!=0`. Consequently all components of a point of `U` are
computed from its `m` coefficients in this basis. Enumerate only
`ell^m` combinations, with polynomially many component/deck operations.

This repairs, rather than ignores, the warning that a multiplicity
space is not automatically a set of torsion classes. Here a specific
injective Galois-equivariant evaluation into actual torsion was proved.
The proof would fail for a scalar-ambiguous geometric coefficient
action on a single component. It uses the genuine FULL frame and
constant domain `S`.

In general `A(h)U` is the evaluation subgroup for `rho_S(h)s0`, not
`U` itself. Thus output-deck action on `U` is not claimed. The full
`E` route remains available if a Gamma-module output is required.

Unique torsion lifting preserves all these statements at the auxiliary
prime: any two lifted group/deck expressions with the same reduction
are equal prime-to-`P` torsion points. Hence the locally constructed
groups are the reductions/lifts of the global `E` and `U`, not just
subspaces with matching dimensions.

## 3. Global scalar coordinates, not component basis coordinates

One can use genuine `Q`-rational coordinate functions on the full
cover. To make this explicit, if its current function field is
`Q(zeta)(x)[Y]`, choose `theta=Y+c*zeta`. Distinct embeddings of the
field exclude at most quadratically many integer values of `c`.
Test that the characteristic polynomial has full degree and is
squarefree. This constructs a primitive element over `Q(x)` in
polynomial degree/height/bit cost using the presented field matrices.
Clear and scale its denominators to obtain a monic plane equation

```
F(x,y) in Q[x,y],        x=pi,
```

of polynomial degree and coefficient height. Its geometric components
may be distinct; the polynomial and its coordinate functions are
nevertheless defined over `Q`. Each component is a finite cover of the
`x`-line. The native normalization data can be used componentwise.

Exclude the finite normalization points outside the affine nonsingular
locus of this GLOBAL plane equation, its coordinate poles, its charged
leading/discriminant denominator zeros, and values at which the chosen
plane fibre does not separate all normalized fibre points. Their counts
are polynomial in the presentation degrees. In particular the global
plane may have intersections between different geometric components;
these must be included in the singular-plane exclusions. A field basis
on one arbitrarily labelled component is not a replacement for these
global scalar functions.

Write `T` for either `U` (rank `k=m`) or `E` (rank `k=R`), and let

```
B_a = full regular frame fibre over a,
S_a = B_a(Qbar) x T,
M=|T|=ell^k,       N=|S_a|=s*M.                          (5)
```

For each pair `(b,t)` and each FIXED `h in Gamma`, take the component
containing `R_h b`, project the actual full class `t` to it, and let
`D_(b,t,h)` be the unique effective degree-`g_C` divisor in that class
plus `g_C R_h b`. Encode it by the intrinsic closed polynomials
`A,B,C` in the common coordinate `z=x+c y`. Include actual global
coordinates of `b` and its cyclotomic coordinate in the tuple. All
tuple positions, including `h`, are fixed in advance.

For every Galois automorphism,

```
sigma D_(b,t,h) = D_(sigma b,sigma t,h).                  (6)
```

The reasons are rationality of `R_h`, genuine transport of component
classes, and uniqueness of the effective divisor. Since `x,y,c` are
global rational functions/constants and the `A,B,C` normalizations
are unique, the WHOLE scalar tuple satisfies

```
sigma enc(b,t) = enc(sigma b,sigma t).                    (7)
```

The auxiliary RR bases and pivot choices disappear from these intrinsic
coordinates. No arbitrary global number-field basis is included in
the encoding.

The tuple is injective on the auxiliary residue set: the fibre
coordinates distinguish `b`; for fixed `b`, its divisor tuples determine
the relevant component classes. Formula (4), or (3), makes the projection
to any one component injective on the chosen group, and the all-`h`
encoding in any event contains every component.

The field of one fibre point is a Galois splitting field of that
constant torsor, of degree at most `s`. The group `T` is split by a
field of degree at most `|GL_k(F_ell)|`. Uniqueness places every
encoding scalar in their compositum. This is only an existential
degree bound; the algorithm does not construct the torsion splitting
field or any individual divisor-support splitting field.

If exact basepoint-field RR data is needed, the field of `b` IS
constructible: factor the polynomial fibre equation over `Q`, choose
the factor containing the selected auxiliary root, and use that
primitive root with its selected unramified local embedding. Its
degree is at most `s` and its polynomial coefficient-height bound
comes from specializing the charged plane equation at `a`. The torsor
deck maps provide every other fibre point over this same field.

## 4. Auxiliary scheduling, admissibility, and full-precision encoding

All avoidance counts are fixed before choosing `P`. On all components,
charge the class-uniqueness bad sets, all support/chart exclusions just
listed, and a faithful plane-coordinate fibre. The ordinary Wronskian
bounds apply when `P>2g_C-1`. There are polynomially many classes,
components and exclusions, so one obtains a known polynomial bound
`L` on bad base values, uniform in the eventual residue classes.

Freeze a list of `L+1` integer candidates before choosing `P`.
It can be the proposed `a0+p*j`, with `P!=p` and `P>L`, or simply
positive integers `1,...,L+1` on the quotient-first route. The height
of every candidate is controlled in advance. Include zero among the
bad values if the nonzero-basevalue version of the height theorem is
used.

Choose `P` above the known bad-base, bad-coordinate and bad-separator
bounds and outside the explicit model/RR certificate and required
group/order primes. These thresholds depend on the polynomial ranks
and degrees, not on as-yet-computed torsion coordinates. The certificate
integer has polynomial bit length, hence only polynomially many prime
divisors. A polynomial numerical prime search above the threshold is
therefore sufficient; gcd and primality tests do not factor it.

The fixed chart and fixed-pole RR spaces are certified before the
class-dependent calculations. If fixed data depends on the candidate
base value, its entire already-frozen polynomial-size list can be
processed. The subsequent canonical RR and closed-algebra calculations
use the proven residue-unit-pivot mechanism; they do not invent a new
prime-exclusion requirement after selecting `P`.

In particular, the later `b`-dependent KM backgrounds in Section 1
must NOT be handled by enlarging the excluded integer after choosing
`P`. There is a direct integral construction on the already-good model.
The chosen regular fibre has a monic separating polynomial with
`P`-unit discriminant. Each rational irreducible factor is monic over
`Z_(P)` and has `P`-unit discriminant too. Thus

```
R_b=Z_(P)[y(b)]
```

is a finite etale semilocal power-basis order in the constructible
field `K_b`; no global number-field maximal-order algorithm is needed.
All conjugates of the chosen fibre point have good reduction.

On the chosen connected component (split using the cyclotomic coordinate
already in `K_b`), let `H_a=pi^-1(a)` and `H=pi^-1(infinity)`.
For the known pole spaces,

```
H^0(j H_a)=(x-a)^(-j) H^0(j H).
```

The right-hand fixed-pole spaces can be included in the precomputed
polynomial degree range. In the finite free thick-fibre algebra
`B0/(x-a)^j`, lift the `b` idempotent by unit Hensel operations. For
`f=(x-a)^(-j)g`, requiring `(1-e_b)g=0` in this algebra removes all
other fibre poles and gives precisely `H^0(j b)`. The needed known
orders `j>=d0>=2g_C+1` are nonspecial, so the exact sequence for those
principal parts has surjective restriction and free base change.
Likewise `H^0(A-B)` is the surjective known-`b` jet kernel described
above. The jets use the unit derivative/regular parameter, not a
division by a possibly nonunit factorial.

These coefficient kernels are computed and saturated over `R_b` by
expanding its power basis and using `Z_(P)` linear/Hermite/Smith
arithmetic. Residue bases can be patched across the finite etale
factors modulo `P`, then lifted; their determinant is a unit in this
semilocal order. Polynomial matrix/minor bounds charge the exact
coefficients. All class-dependent products and kernels subsequently
use the established unit residue minors. This pays the post-`P`
known-background RR work without a new prime choice or an uncharged
denominator certificate depending on `b`.

Compute the group `T` at `P` by Section 2. Test all fibre points and
all projected classes for the chosen candidate. The uniform avoidance
bound guarantees a successful candidate. The auxiliary torsion
algorithm's original basepoint need not be this canonical basepoint.
Residue `h^0(t+g_C b)=1` and support avoidance imply the required generic
uniqueness and compatible canonical lift. For the zero class the
divisor is `g_C b`; poles are taken at infinity, so this is not a
compulsory forbidden-support collision.

A regular fibre of a constant Gamma torsor over a finite field has
Frobenius acting by one group element. All its points are rational over
an extension of degree `s`. Combine this with the native torsion and
evaluation field by ONE bounded product of degrees, such as `s*f0`.
This is polynomial; there is no lcm over separate support fields.

For each divisor the bad integers `c` for `z=x+c y` are at most
`binom(g_C,2)+g_C`: pair collisions and tangent zeros. A common good
integer is found in the known polynomial interval, with `P` larger
than its length. The closed-algebra microlemma then gives the exact
`A,B,C` modulo `P^e` using unit determinants, even for nonreduced
divisors. All coordinate values are integral in the common unramified
local coefficient ring.

Let `q` denote the tuple length in (7). The scalar

```
alpha_u(b,t) = sum_(j=0..q-1) u^j enc_j(b,t)
```

fails to separate a given pair for at most `q-1` residue values of `u`.
Thus `(q-1)*binom(N,2)+1` integer trials suffice, provided `P` exceeds
this known bound. Fix a residue-successful `u`. Every difference
between its `N` lifted values is then a `P`-unit. This is an AUXILIARY
prime condition only.

## 5. Intrinsic height bounds give certified rational reconstruction

The support-height chain and the closed-encoding theorem bound every
scalar coordinate in (7) by a known polynomial absolute logarithmic
height `H`. The fibre point coordinates have the same kind of bound
from the charged plane equation at `a`; the cyclotomic coordinate has
height zero. These estimates do not require the height of a global
torsion-field basis. All displayed asymptotic constants are to be
replaced by computable dominating bounds from the proved inequalities
when setting precision; no ineffective height constant is needed.

For `0<=u<=U0`, a safe bound for each separator value is

```
H_alpha=q*H+q^2*log(U0+2)+log(q+1).
```

Write these values as `alpha_v`, indexed by `v in S_a`. Their monic
polynomial

```
Q(X)=product_v (X-alpha_v)
```

has rational coefficients by (7), of height at most
`N*(H_alpha+log 2)`. It is separable because residue separation was
certified. For the Lagrange polynomials

```
lambda_v(X)=product_(w!=v)(X-alpha_w)/(alpha_v-alpha_w),
```

each coefficient has height at most

```
H_lambda=3*(N-1)*H_alpha+2*(N-1)*log 2.                  (8)
```

Indeed the numerator coefficient height is at most
`(N-1)*(H_alpha+log 2)` and the product denominator has height at most
`(N-1)*(2H_alpha+log 2)`. Product-formula height bounds include inverse
separations; no uncharged lower bound on complex root distances is used.

For a Galois-equivariant binary operation `h:S_a^2 -> S_a`, its
separator table is

```
T_h(X,Y)=sum_(v,w) alpha_(h(v,w))*lambda_v(X)*lambda_w(Y).
```

Its coefficients are rational and have height at most

```
N^2*(H_alpha+2*H_lambda)+2*log N.                         (9)
```

The same proof covers unary tables, coordinate tables, and Boolean
relation tables, using the corresponding output-height bound. Every
needed coefficient therefore has a known polynomial height bound `K`.

All input coordinates and all Lagrange denominators are integral/units
at `P`, so these rational coefficients lie in `Z_(P)`. Choose an
integer `T0>=exp(K)` and precision

```
P^e > 2*T0^2.                                           (10)
```

Every reduced numerator and denominator has absolute value at most
`T0`, and the denominator is prime to `P`. Two candidates with the
same residue would have a nonzero cross-product of absolute value
at most `2*T0^2` divisible by `P^e`, which is impossible. Standard
exact rational reconstruction therefore recovers the true coefficients.
The required bit precision `e*log P=O(K+log P)` is polynomial.

Use a charged integral power basis of the common unramified local
field, with `1` as its first vector. The rational invariant coefficients
have only that scalar coordinate; exact finite-precision arithmetic
reads it without loss. Another integral basis can be changed to this
form by a unit basis transformation. The geometric rationality proof
is (7), not invariance under the one auxiliary Frobenius or a local
numerical test.

Thus one reconstructs the genuine finite etale coordinate algebra

```
A_Q=Q[X]/Q(X) ~= Map_Gal(S_a,Qbar),                     (11)
```

with the required tables. This is generally not the split algebra
`Q^N`, and it is not a group algebra.

## 6. The relation idempotent gives the actual group quotient

The local enumeration uses arbitrary labels for the points of `T`,
but its equality and group-law tables are exact. Define

```
r(v,w)=1 if t(v)=t(w), and 0 otherwise.
```

Equality in the actual group is Galois invariant even though its
chosen auxiliary basis is not. Interpolation and (8)--(10) reconstruct

```
r=sum_(t(v)=t(w)) lambda_v tensor lambda_w in A_Q tensor A_Q.
```

It is an idempotent. Compute the rational linear kernel

```
C_Q={f in A_Q : r*(f tensor 1-1 tensor f)=0}.             (12)
```

This has `N` unknowns and at most `N^2` equations. After extending to
`Qbar`, (12) says exactly that the values are constant on every fibre
`B_a x {t}`. Kernel formation commutes with this flat extension, so

```
C_Q ~= Map_Gal(T,Qbar),        dim_Q C_Q=ell^k.           (13)
```

It is a finite etale subalgebra of `A_Q`. Rational kernel bases,
multiplication tables, and basis changes have polynomial bit size by
the usual ratios-of-minors bounds for these polynomial matrices.
No global Galois labels or arbitrary high-height field basis are
supplied at this stage.

The auxiliary binary map

```
((b,t),(c,u)) -> (b,t+u)
```

is Galois equivariant but is not a group law on `S_a`. Its comorphism
on functions in (12) lands in `C_Q tensor C_Q`: its values depend
only on `t,u`. Solve in that known tensor subspace to compute the
actual Hopf comultiplication. Inversion and scalar maps descend in
the same way. The zero-projector `(b,t)->(b,0)` sends each function
of `C_Q` to a rational scalar, giving the counit. All identities
hold because they are the true group operations after scalar
extension to `Qbar`.

For the Gamma-stable `E` route, the actual deck action on `t` also
descends, with the checked pullback/right-pushforward conventions.
For the smaller `U` route it is deliberately omitted: that action
generally does not preserve `U`. Deck action on the basepoint and
its use in (2), (4), and the all-component encoding remain legitimate.

## 7. Quotient first, then use the known-prime order theorem

The reconstructed `C_Q` is unramified at `p` by the intrinsic
target-prime theorem and the Galois stability proved in Section 2.
Apply the independently reviewed Buchmann--Lenstra prime-maximal
order algorithm to this algebra, with its complete rational tables.
It constructs an initial order by scaling a basis containing `1`,
then performs nilradical/idealizer/Hermite steps. The discriminant
valuation bounds the number of steps, and the original trace-dual
lattice bounds all intermediate bits. Its cost is polynomial in
the algebra rank, input bits, and `log p`; it does not enumerate `p`
values or factor an integer discriminant.

At termination the `p`-local order is the integral closure in
`C_Q tensor Q_p`. Unramifiedness makes it finite etale. Its tensor
powers are also finite etale and already integrally closed in their
rational algebras. Hence all Hopf maps, scalars, and any valid supplied
deck maps extend to these orders. Their transported rational coefficients
have denominators prime to `p`; they need not be integral at other
primes. Reduction gives the actual finite etale coordinate Hopf
algebra

```
C_p over F_p,           rank C_p=ell^k.
```

No property of the original monogenic encoding's discriminant at `p`
is assumed. In particular the `X(X-p)` coordinate-collision example
is repaired by the maximal order, not by finding another target
separator.

Only (13) needs to be unramified here. The larger algebra `A_Q` can
be ramified at `p` because the auxiliary basepoint fibre is ramified
there. Quotienting before maximalization removes that factor. Thus
neither an unbranched target residue basepoint nor a target-faithful
canonical divisor encoding is a remaining requirement.

## 8. Actual Frobenius from deterministic kernel ranks

On `C_p`, compute the algebra automorphism

```
F_alg:a -> a^p
```

by binary powering. On a geometric point `v:C_p -> F_pbar`, it induces
`v o F_alg`, with values `v(a)^p`; this is ARITHMETIC Frobenius on the
actual finite group. It is not a curve-Frobenius pullback substitution.

The Hopf counit makes the identity a rational point. Its idempotent
`e0` is the unique solution of the linear equations

```
e0*ker(counit)=0,        counit(e0)=1.
```

For any polynomial `q(X) in F_ell[X]`, construct the group endomorphism
`q(F)` from the Hopf addition, scalar operations and `F_alg`. Addition
of two endomorphisms has comorphism
`multiplication o (f^* tensor g^*) o comultiplication`, so this step
is explicit algebra arithmetic. Scalar multiplication uses binary
addition, not a loop of length `p`.

Here `q(F)` is a polynomial in GROUP endomorphisms with coefficients
in `F_ell`. It is not the polynomial obtained by adding the coordinate
algebra's `F_p`-linear Frobenius matrices. In particular the zero group
endomorphism has comorphism `unit composed_with counit`, not the zero
linear map. The Hopf construction above preserves this distinction.

The idempotent `q(F)^*e0` is the characteristic function of the kernel
of that endomorphism. Therefore

```
rank_(F_p)(multiplication_by_(q(F)^*e0))
   = |ker q(F_T)|
   = ell^(dim_(F_ell) ker q(F_T)).                       (14)
```

Rank is unchanged after a splitting-field extension, where the claim
is diagonal and immediate. Recover the exponent by exact integer
powers/division, not floating logarithms.

Enumerate the monic irreducibles over `F_ell` of degree at most the
FIXED `k`, and apply (14) to their powers through the necessary
dimension bound. This is polynomial in numerical `ell` for fixed
`k`; irreducibility is checked by finite-field powering and gcd.
If `r_a=dim ker f(F_T)^a`, then

```
(r_a-r_(a-1))/deg f
```

is the number of `f`-primary Jordan blocks of length at least `a`.
Successive differences determine every elementary divisor. Thus the
procedure returns a rational-canonical matrix for the TRUE `F_T`
up to basis conjugation, not just a coordinate-algebra permutation
or a characteristic polynomial with an unknown scalar.

For `T=U`, (1) identifies this matrix directly with `F_W`. No final
Gamma action, Hom restriction, or division of multiplicities is
needed. For the backup `T=E`, one has

```
E=S tensor W,        F_E=I_S tensor F_W,
```

so all kernel dimensions in (14) are `n` times the corresponding
dimensions for `F_W`. Dividing by `n` is valid because (3), not rank
alone, established the actual isotypic module. Alternatively split
`C_p` over one structurally bounded field and recover all point and
deck matrices as in the report; that randomized route is unnecessary
for the matrix-only output.

The full-similitude comparison gives

```
W ~= H^1(U_base,R^1 f_*F_ell)(2).
```

Consequently arithmetic Frobenius on the untwisted open cohomology is
`p^(-2)*F_W`, and geometric Frobenius is its inverse. For the torsion
sheaf `J_fibre[ell]` convention the corresponding correction is
`p^(-1)`. These are the previously proved Tate factors, with no new
scalar or sign ambiguity.

## 9. Cost, completeness, and the remaining composition boundary

On the primary route `k=m=13516` and `N=s*ell^m`. Every enumeration,
component tuple, closed RR calculation, interpolation matrix, relation
kernel, Hopf table, order calculation, and kernel-rank computation
has polynomial size and bit cost in numerical `ell` and the native
input size `B`, including `B=log p`. The constants/exponents are
enormous but fixed. This is not a claim uniform in a growing `k`,
nor a practical complexity estimate.

The only randomness needed is that of the previously admitted
certifying auxiliary primitives. Their finite clocks, completeness
certificates, and a union-bounded failure allocation across polynomially
many calls give the same capped polynomial-time/ABORT contract. The
deterministic reconstruction threshold and target kernel-rank readout
introduce no new heuristic acceptance or unknown-tail search.

Thus no additional global torsion-field, component descent, normalized
arithmetic coefficient action, numerical closed-divisor quotient,
rational reconstruction, or target coordinate-model oracle remains
inside THIS finite-group reconstruction/readout. The earlier source
results now compose to this bridge with their stated hypotheses.

The full native surface point count is a different final claim. This
review does not prove the geometric pencil/monodromy hypotheses for
inputs outside their admitted scope, the open-to-parabolic/boundary
comparison, the full surface cohomology exact sequence and polynomial
assembly, or its final CRT/Weil-bound recovery. Those must use their
own reviewed arguments. In particular the false displayed surface
Theorem 4.1 is not rehabilitated by this reconstruction theorem.

Strong falsifiers of a weaker procedure remain: a component-only
arithmetic scalar, a concatenated `(ell-1)*R` space, a component-labelled
field basis used as scalar coordinates, local Frobenius invariance
standing in for rationality, lost jet multiplicities, target reduction
of a nonmaximal encoding order, or a deck action asserted on the
non-Gamma-stable subgroup `U`. None is used by the construction above.
