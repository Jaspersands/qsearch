# Conditional readout from cyclic-character torsion-cover twists

2026-11-07. CLOSED conditional algebraic/readout review. STATE/TRAPS and the
working SURFACE_TORSION_COVER_RECONSTRUCTION.md were read. No network, API,
implementation or numerical control. This proves the supplied repair, not the
existence of a polynomial-time native K3 algorithm. Explicit cover, twist,
compactification, boundary-action and curve-zeta interfaces remain assumptions
to be paid by their separate source/construction audit.

## Contract and fixed-rank cost

Fix a rank r, independent of p and ell. Let U/F_p be a smooth curve, ell!=p,
and let Z->U be an EXPLICIT right Gamma-torsor, with Gamma=GL_r(F_ell) allowed.
Z need not be connected or geometrically connected. All deck actions are
defined over F_p. A rank-r module V of Gamma defines the lisse coefficient
sheaf of interest. For the frame torsor of the raw Jacobian ell-torsion, use
the natural DUAL representation for H^1(F_ell); do not replace it by the
natural module while silently discarding the arithmetic Tate/cyclotomic action.

Using the full frame torsor avoids an oracle for the exact arithmetic monodromy
image. The identity constructed for Gamma restricts to every image subgroup.
Replacing Gamma by only geometric monodromy, without arithmetic Frobenius,
would not justify the same L-function identity.

Assume the explicit models, their total geometric genus g, boundary size b,
all component/boundary actions, and required twists can be constructed with
size and time polynomial in ell and log p. Assume the curve-zeta subroutine
applies to these models, including disconnected forms or a paid decomposition
into its supported connected inputs. Those assumptions are NOT inferred from
the abstract bound |Gamma|<ell^(r^2).

Put L=lcm(1,...,r), k=F_(ell^L), e=ell^L-1 and E=Q(zeta_e). Every ell-regular
matrix in Gamma is semisimple with eigenvalues lying in k: each eigenvalue's
minimal polynomial has degree at most r, dividing L. Thus its order divides e.
Every cyclic ell-prime subgroup and all of its linear characters are defined
over k. Both |Gamma| and e are numerical polynomials in ell for FIXED r, with
enormous constants/exponents. Nothing here is polynomial in growing r.

## Rational induction is valid for cyclic characters

Plain permutation induction is insufficient, as the SL2(F7)/order8 example
shows. The repaired columns are P_(H,chi)=Ind_H^Gamma chi for every cyclic
H of order prime to ell and every one-dimensional k-character chi. Each is
projective because k[H] is semisimple and induction preserves projectivity.
The following proof does not assume semisimplicity of k[Gamma].

Use Brauer characters, lifting ell-prime roots of unity into E, on ell-regular
conjugacy classes. For these induced modules their Brauer characters equal the
restriction of the corresponding ordinary induced characters. Suppose a complex
class function on ell-regular classes is orthogonal to every such column,
with the usual conjugacy-class weights. Frobenius reciprocity makes its
restriction to each H orthogonal to every linear character of H. Fourier
inversion on the cyclic H makes that restriction zero. Every ell-regular
element generates one of these H, so the original class function is zero.
Therefore the induction columns span all ell-regular class functions over C.

By the basic Brauer-character theorem, irreducible Brauer characters form a
basis of those class functions and identify G0 over characteristic zero.
The induction columns have INTEGER composition multiplicities in that basis.
Full rank over C of this integer matrix therefore gives full rank over Q.
Consequently there are integers m>0 and a_i such that

    m[V] = sum_i a_i [P_(H_i,chi_i)]  in G0(kbar[Gamma]).

The basic Brauer independence/class-count theorem is the standard modular
representation fact used here; no false modular permutation-induction theorem
or characteristic-ell trace independence is substituted for it. Equality can
also be read after restriction to the actual arithmetic image. Since all
modules in the identity are k-defined, scalar extension loses no G0 equality:
simple modules over a finite field split into disjoint Galois orbits of
absolutely simple modules.

This is constructive in polynomial(ell) bit operations at fixed r. Enumerate
Gamma, its cyclic ell-prime subgroups, and their characters. Compute the Brauer
character of V from the eigenvalues of each ell-regular matrix, using their
specified root-of-unity lifts. Compute induction columns by the finite coset
character formula. Expand every entry in the power basis of E and solve the
resulting RATIONAL linear system. There are polynomially many rows and columns
and polynomially many coefficient bits; roots of unity and the cyclotomic
polynomial have polynomial-size representations in numerical e. Exact linear
algebra gives m and a_i with polynomial BIT length by determinant bounds.
Their numerical magnitudes need not be polynomial and are never loop bounds.
All required root tables can even be enumerated in numerical e if necessary;
no discrete-log or character-table oracle is implicit.

## Frobenius, sector orientation and exact characteristic-zero recovery

Fix the following convention to remove a possible inverse-character error.
For a right Gamma-torsor let Gamma act on W=H_c^i(Zbar) by deck PULLBACK.
Then the sheaf associated with a left module V has cohomology computed by
(W tensor V)^Gamma when that invariant operation is exact. For Ind_H chi,
Shapiro reduces this to (W tensor chi)^H. Since |H| is prime to ell, invariants
are exact, and this is the chi^(-1)-sector of W. Its projector is

    e_(chi^-1) = (1/|H|) sum_(h in H) chi(h)*h.

An opposite deck-action convention is possible, but the induction columns and
Fourier weights must both change. Enumerating all characters does not excuse
using the wrong sector for a particular column.

Compactify Z to a disjoint union of smooth proper curves Zbar, and let D be
the boundary. For every required h and j construct the twist OVER F_(p^j)
whose cohomological Frobenius is h*F^j. Choose the inverse descent cocycle if
the Frobenius convention requires it. A single twist over F_p would instead
provide h^j*F^j at its j-th power and is not interchangeable. Deck actions
commute with F because they are defined over F_p.

From the twist's point count, subtract the explicitly known H0 and H2
component traces to obtain Tr(h F^j | H^1(Zbar)). In particular H2 contributes
p^j times the corresponding component-permutation trace. Boundary terms are
finite permutation representations and are computed separately. Apply the
displayed Fourier projector over E EXACTLY to recover the power traces on each
character sector. Newton identities through j=2g suffice for the H1 polynomial;
no prior knowledge of the sector dimension is required, since trailing
coefficients beyond its dimension vanish. The H0, H2 and boundary sector
polynomials are obtained from their explicit finite permutation actions.

For each sector the open-curve L-factor is

    P1(T)*P_D(T) / (P0(T)*P2(T)),

using the compactification H1 and component/boundary factors. This avoids
guessing an H_c^1 trace from an alternating point count. Equivalently one may
recover the compact-support groups directly after making these corrections.
Dimensions and the number of h,j twists are polynomial under the stated
geometry assumptions; twists reused between subgroups need not be recomputed.

All Newton divisions occur in CHARACTERISTIC ZERO, including j divisible by
ell. These sector polynomials have coefficients in E and are algebraic
integers: their roots are subsets, with multiplicity, of the integral
Frobenius eigenvalues of the compact curve, and their traces are the exact
Fourier sums in E. Thus their coefficients lie in Z[zeta_e]. At minimum,
ell-integrality follows because |H| is invertible in the unramified ell-adic
coefficient ring and the projector is an integral direct summand. Only AFTER
the exact Newton computation are coefficients reduced by the specified map
zeta_e -> a primitive e-th root in k. Reducing traces first would lose the
information needed at ell-divisible Newton indices.

The torsion-free assertion needed here is valid for smooth curves. Proper
H0, H1 and H2 over Z_ell are free. For an open curve, the compact-support
sequence adds the cokernel of H0(Zbar)->H0(D). On each geometric component
this is a primitive diagonal embedding of a free rank-one module into the
boundary permutation lattice, so its cokernel is free. Proper components
can instead be handled separately. Thus all H_c groups are free, and their
finite-coefficient reductions have no extra torsion terms. Projecting by
the ell-prime H preserves freeness. No semisimplicity of Frobenius or of the
full Gamma action is being assumed.

## Euler factors and an ell-divisible power

The Euler L-function is multiplicative on short exact sequences of lisse
finite-coefficient sheaves, either directly by triangular local Frobenius
matrices or by the Frobenius-equivariant compact-support long exact sequence.
The Grothendieck identity therefore yields

    L_U(V,T)^m = product_i L_U(P_(H_i,chi_i),T)^(a_i).

This is valid for the FULL arithmetic local system and does not divide by
|Gamma| or require its cohomology to be semisimple.

The power map is NOT injective on all kbar(T)^*: constant roots of unity are
a counterexample when m has a prime-to-ell factor. It IS injective on the
group of rational functions regular at T=0 with value 1, which contains all
the L-functions here. Indeed R^m=1 implies m*div(R)=0, hence R is a constant,
and its value at zero fixes it to 1. This also works when ell divides m.

Factor the individual reduced numerator/denominator polynomials over k,
normalizing irreducible factors to constant term 1. Combine their multiplicities
with the BINARY integers a_i. The identity proves each resulting signed
multiplicity is divisible by m; divide those integers exactly. This computes
the unique normalized m-th root without expanding a degree-m polynomial or
trying to divide formal derivatives by m. Inseparable factors in characteristic
ell are handled by ordinary finite-field polynomial factorization/power-root
operations. An elementary example is Gamma=C_ell: its regular module has
class ell*[1], so its L-function is an ell-th power, recovered precisely by
this multiplicity operation.

The output can remain a polynomial-size factored rational function. Expansion
to the desired fixed-degree surface polynomial uses the separately proved
geometric Euler and boundary identities and their degree bounds; it does not
follow from treating numerical m as small.

## Final disposition and unclosed gates

The cyclic-character/full-arithmetic Grothendieck repair and the exact twist
readout are sound under the explicit data/construction assumptions above.
The two corrections to keep in the main text are normalized-rational-function
power injectivity and a consistent inverse-character/deck-action convention.

Still unpaid by THIS lemma: a polynomial-size Jacobian torsion/frame scheme;
curve normalization and geometric-component bookkeeping; explicit finite-field
twist descent; quantitative genus, ramification and coefficient-height bounds;
the exact native scope and finite clocks of quantum curve zeta; and the
surface's pencil, boundary, integral-cohomology and CRT reconstruction gates.
In particular polynomial cover DEGREE alone does not prove those algorithmic
operations polynomial. No full K3 algorithm, novelty or separation is promoted.
