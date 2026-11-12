# Independent review: full similitude-frame arithmetic repair

2026-11-12. Focused core review of
`../claude_runs/2026-11-12-closure-full-similitude/response.md`, against
the explicit obligation in
`../api_inputs/2026-11-12-surface-closure/full-similitude.md` and
`../../SURFACE_NATIVE_TORSION_MODULE.md`. Current `STATE.md` was read.
The already closed geometric compact/open lemma and finite-field
torsion-extraction primitives are inputs, not re-audited here.
The input hypotheses are the parent's fixed even `n`, fixed `r`, odd
`ell`, `P` prime to `ell*|GSp_n(F_ell)|`, and a smooth proper family
`f:X -> U=P^1 minus B` with `|B|=r`, its genuine torsion sheaf
`L=J_fibre[ell]=R^1 f_*mu_ell`, full geometric `Sp_n` monodromy, and
nontrivial transvection inertia at the punctures. Its full frame scheme,
evaluation, and deck maps are presented and charged.
No Git, network, API, archive, numerical sweep, or native construction
was used. Commands used `/opt/anaconda3/bin/python`.

## Disposition

ACCEPTED under the actual presented-frame hypothesis. The full torsor
removes the unknown arithmetic coefficient scalar because its evaluation
map identifies the associated local system with the ORIGINAL family
torsion sheaf. It does not merely normalize an intertwiner of an abstract
deck group.

With the precise action conventions below, the arithmetic identity is

```
Hom_GSp(N^vee, H^1(C_full_bar,mu_ell))
  ~= H^1(U_bar,L)(1),             L=J_fibre[ell].          (A)
```

The actual arithmetic `q`-Frobenius on the left is post-composition by
the Galois action on divisors. Hence the arithmetic Frobenius matrix on
`H^1(U_bar,L)` is exactly `q^-1` times that output matrix. If the desired
coefficient system is instead `R^1 f_*F_ell=L(-1)`, the factor is
`q^-2`. These are explicit Tate factors, not unknown scalars.

The disconnected-cover and field overheads remain polynomial in
numerical `ell`, numerical characteristic `P`, the charged presentation
size, and `log(1/eta)`, for fixed natural dimension `n` and branch number
`r`. No full ambient torsion splitting is needed.

Two errors in the paid procedure require correction, without changing
this conclusion:

* Other geometric components need not all be Frobenius conjugates of
  a selected component. They are rational DECK TRANSLATES over the
  cyclotomic field, which is enough to reuse its zeta numerator.
* A regular-fibre avoidance extension may precede adjoining one residue
  field. The literal bound `b<=ord_ell(q)*|Sp|` omits that factor; the
  corrected bound remains polynomial.

The full frame scheme, its right action, and its genuine evaluation map
are still assumed to be presented and charged. Constructing them from a
native surface/family is not proved here. The output is OPEN cohomology;
the parabolic filter remains separate.

## 1. Exact right action, left cohomology action, and associated sheaf

Let

```
Gamma=GSp_n(F_ell),     G=Sp_n(F_ell),
lambda:Gamma -> F_ell^*,
N=F_ell^n,
S=N^vee,               rho_S(g)=g^(-T).
```

Here `N` and `S` are constant coefficient vector spaces over `F_q`.
The local system `L=J_fibre[ell]` has its actual arithmetic action and
its Weil pairing with values in `mu_ell`. Its geometric monodromy is
promised to be all of `G`, with nontrivial transvection inertia.

The presented torsor `T -> U` has points `(c,zeta)`, where
`c:N -> L_t` is an isomorphism and

```
e(cu,cv)=zeta^(u^T J v).
```

Its RIGHT action is

```
(c,zeta).g=(c composed_with g, zeta^lambda(g)).
```

For `R_g(x)=x.g`, composition satisfies

```
R_(gh)=R_h composed_with R_g.
```

Consequently

```
A(g)=R_g^*                   is a LEFT representation,
P(g)=(R_g)_*=A(g^-1)          is a RIGHT representation.
```

The second equality is the usual pullback/pushforward equality for a
curve AUTOMORPHISM. In particular `P(gh)=P(h)P(g)`; it must not be
treated as a left representation with the same matrix labels.

Evaluation descends to a canonical sheaf isomorphism

```
T x^Gamma N -> L,
[(c,zeta),v] |-> c(v),
```

because `[(c g,zeta^lambda(g)),g^-1 v]` has the same image. This is
also arithmetic-equivariant: Frobenius acts on the frame by acting on
its values in `L`, and it fixes the input vector in the constant space
`N`. Thus a constant associated coefficient space does NOT assert that
the original family local system has trivial Frobenius. Its arithmetic
information is carried by the actual frame torsor.

The mod-ell cyclotomic character is denoted by `chi`; arithmetic
Frobenius `sigma= sigma_q` has `chi(sigma)=q mod ell`. It sends
`(c,zeta)` to `(sigma_L c,zeta^q)` and commutes with EVERY `R_g`.
Thus all deck maps are `F_q`-rational even if the arithmetic monodromy
image is smaller than `Gamma`.

## 2. Components and disconnected Cartan--Leray

There are `ell-1` geometric components `T_zeta`, one for each primitive
root. Each is geometrically connected by full geometric `Sp` monodromy.
Let `C_zeta` be its smooth compactification and put

```
C_full_bar = disjoint_union_zeta C_zeta,
V_F=H^1(C_full_bar,F_ell),
V=H^1(C_full_bar,mu_ell)=direct_sum_zeta J_C_zeta[ell].
```

The right deck maps and Frobenius extend to the compactifications.
`P(g)` sends a divisor on `C_zeta` to one on
`C_(zeta^lambda(g))`; `A(g)` acts in the opposite component direction.
Arithmetic Frobenius sends `V_zeta` to `V_(zeta^q)`.

Writing `s=ord_ell(q)`, the arithmetic image is
`lambda^-1(<q>)`: it contains `G`, and its quotient multiplier image is
exactly the cyclic group generated by `q`. This gives
`(ell-1)/s` arithmetic connected components and Frobenius cycles of
length `s` on the geometric components. The full right `Gamma` action
still exists on the entire torsor and can permute these arithmetic
components.

On the OPEN finite etale torsor, Cartan--Leray gives

```
E2^(p,j)=H^p(Gamma,H^j(T_bar,F_ell) tensor N)
  => H^(p+j)(U_bar,L),
```

where the action is `A(g) tensor rho_N(g)`. This convention can be
checked already on sections: an invariant vector-valued function obeys
`f(t.g)=g^-1 f(t)`, exactly the associated-bundle descent relation.

The `H^0` term is the permutation representation on the components.
Tensor-induction and Shapiro identify its group cohomology with
`H^p(G,N)`. This vanishes for EVERY `p`: the central element `-I` has
order two, fixes the component labels, and acts as minus one on `N`.
Equivalently, the group of order two has zero cohomology with these
coefficients, and its invariant subspace is zero. Only the invertibility
of two is used. There is no averaging over `G` or `Gamma`, whose orders
are divisible by `ell`.

In particular the two obstruction terms `E2^(1,0)` and `E2^(2,0)`
vanish, giving the arithmetic-equivariant edge isomorphism

```
H^1(U_bar,L)
 ~= (H^1(T_bar,F_ell) tensor N)^Gamma
 ~= Hom_Gamma(S,H^1(T_bar,F_ell)).                         (B)
```

Connectedness of the TOTAL geometric torsor is not required. It would
be wrong to replace its permutation `H^0` by a single copy of `F_ell`,
but the correct permutation term causes no surviving obstruction.

## 3. Compactification and the exact Tate twist

Restriction from compact to open cohomology is componentwise injective
and commutes with `Gamma` and arithmetic Frobenius. By restriction to
one component and Shapiro, the corresponding `Gamma` Hom map is the
`G` Hom map in the already closed geometric lemma. Its hypotheses hold:
the central-minus-one cohomology vanishing above, and for a transvection
`T=I+N_T` of order `ell`,

```
1+T+...+T^(ell-1)=0
```

on the natural module, since `N_T^2=0` and `ell` is odd. Hence every
invariant open class extends to the compactification. This is NOT an
application of etale descent to the ramified compact cover.

Thus (B) becomes

```
Hom_Gamma(S,V_F) ~= H^1(U_bar,L),
dim Hom_Gamma(S,V_F) = m=(r-2)n.                          (C)
```

The coefficient sheaf `mu_ell` is trivial under deck transformations
but has arithmetic character `chi`. Therefore

```
V=V_F tensor mu_ell,
Hom_Gamma(S,V) ~= H^1(U_bar,L)(1),
```

which proves (A) with the genuine arithmetic action.

The multiplier character as an associated rank-one local system is
`mu_ell`: the map `[(c,zeta),a] |-> zeta^a` is well-defined because
right multiplication changes `zeta` to `zeta^lambda(g)`. Consequently,
for any integer `k`, the precise general twist formula is

```
Hom_Gamma(S tensor lambda^k,V) ~= H^1(U_bar,L)(1-k).         (D)
```

The minus sign in `1-k` comes from dualizing the Hom input. Since
`N ~= S tensor lambda` through the fixed standard symplectic form,

```
Hom_Gamma(N,V)              ~= H^1(U_bar,L),
Hom_Gamma(N^vee,V_F)        ~= H^1(U_bar,L),
Hom_Gamma(N^vee,V)          ~= H^1(U_bar,L)(1).
```

For `L'=R^1 f_*F_ell=L(-1)`, the last output is
`H^1(U_bar,L')(2)`. Thus `q^-1` and `q^-2` are respectively the required
arithmetic matrix factors for `L` and `L'`. Geometric Frobenius is the
inverse of the declared arithmetic matrix.

Arithmetic Galois action on `H^1(C,mu_ell)` is implemented by sending
divisor coefficients/points to their `q`-th powers. Do not substitute
pullback by the inseparable absolute-Frobenius morphism for this
operation. Pullback/pushforward inversion above was stated for DECK
AUTOMORPHISMS, not for that inseparable morphism.

## 4. Explicit one-component arithmetic formula

Fix a primitive `zeta0`, write `V0=J_C_zeta0[ell]`, and let

```
W0=Hom_G(S|G,V0).
```

Restriction to the `zeta0` component identifies `W` with `W0` as vector
spaces. This identification alone does not make `sigma` an operator on
`V0` when `q!=1 mod ell`.

For each `a in F_ell^*`, choose a known matrix `g_a in Gamma` with
`lambda(g_a)=a`. The inverse to component restriction is explicitly

```
phi_a(v)=A(g_a)^-1 phi_0(rho_S(g_a)v),                    (E)
```

on the component indexed by `zeta0^a`. This is independent of the
choice of representative: replacing `g_a` by `h g_a`, `h in G`,
cancels by the `G`-equivariance of `phi_0`. Formula (E) also verifies
the full `Gamma` intertwiner relation directly, without invoking
semisimplicity of any modular representation.

Choose `g_q` with multiplier `q mod ell`; in a standard symplectic
basis one may take `diag(q I_(n/2),I_(n/2))`. The component of
`sigma phi` at `zeta0` comes from `phi` at `zeta0^(q^-1)`. Substituting
`g_(q^-1)=g_q^-1` into (E) gives the CORRECT transport formula

```
(F_W phi_0)(v)
 = A(g_q) sigma phi_0(rho_S(g_q^-1)v)
 = P(g_q^-1) sigma phi_0(g_q^T v).                        (F)
```

Here `sigma` takes `C_zeta0` to `C_(zeta0^q)`, and `P(g_q^-1)`
takes that component back. It need not take a selected origin back to
the SAME point; it returns it to the same COMPONENT.

The result is `G`-equivariant. For `h in G`, move `A(h)` past
`A(g_q)` using `g_q^-1 h g_q in G`, use the original intertwiner
relation, and obtain

```
A(h)(F_W phi_0)=(F_W phi_0)rho_S(h).
```

For representative independence one may write another multiplier-`q`
matrix as `g_q h`, `h in G`; the extra factors cancel immediately in
(F). Thus replacing a lift by its negative changes both the divisor
transport and the coefficient action, with no residual sign.

As a further exact consequence,

```
F_W^s(phi_0)=sigma^s composed_with phi_0,
s=ord_ell(q),
```

because `g_q^s in G`, and its two factors in the iterated formula
cancel by equivariance. This is an identity, not a finite-example
validation of the whole construction.

When using pushforward matrices, the `G` intertwiner equations are

```
phi_0 g^T = P(g) phi_0                       (g in G).     (G)
```

They are equivalent to `A(g)phi_0=phi_0 g^(-T)`. Both sides of (G)
use right representations, so equations on group generators suffice.
Using `g^(-T)` with `P(g)` instead would mix conventions and generally
compute the wrong space. Dimension and Frobenius-stability tests cannot
replace this convention proof.

## 5. Polynomial fields, zeta data, and the primary certificate

Let `D=|Sp_n(F_ell)|` and let `g_C` be the genus of one compact
component. For fixed `n,r`,

```
D < ell^(n(n+1)/2),
g_C=O_r(D),
G_tot=sum_zeta g(C_zeta)=(ell-1)g_C.
```

All geometric components are defined over
`k_cyc=F_(q^s)=F_q(mu_ell)`, `s<=ell-1`. They are mutually isomorphic
over this COMMON field by the known deck maps. Thus one component's
Lauder--Wan zeta computation suffices. The paid claim that they are
all `sigma^i`-conjugates is false when `s<ell-1`: for instance, when
`q=1 mod ell`, Frobenius fixes every component label. Deck isomorphism,
not Frobenius transitivity, supplies the required equality of zeta data.

For completeness, if `chi0(X)` is the characteristic polynomial of
`sigma^s` on `V0`, the characteristic polynomial of ORIGINAL `sigma`
on the full geometric `V` is explicitly

```
chi_full,sigma(X)=chi0(X^s)^((ell-1)/s).                  (H)
```

A Frobenius cycle of length `s` has characteristic polynomial
`det(X^s I-sigma^s|V0)`, and deck maps identify the return maps on
different cycles. Formula (H) pays the combined spectrum without
supplying any target eigenvalues.

Choose one regular-fibre point on `C_zeta0` using the already reviewed
procedure. If necessary, first extend `k_cyc` by degree `t` until there
are more base values than the total degree of the presented bad-fibre
polynomial. Then choose ONE residue factor of degree `e<=D`.
The field

```
k0=F_(q^b),        b=s*t*e,
```

contains a rational origin `O0`; `t` is logarithmic in the bad-fibre
degree, hence polynomial in the charged presentation. The origins on
all other components can be the deck translates `R_(g_a)(O0)` over
the SAME field. There is no product or lcm over separately selected
component point fields.

Put `F0=sigma^b`. It preserves every component, commutes with all deck
maps, fixes `mu_ell`, and is the identity on the constant coefficient
space `S`. Since `S|G` is absolutely simple and has endomorphism ring
`F_ell`, the natural socle on `V0` is

```
E0 ~= S tensor W0,
F0|E0=I_S tensor B,
dim W0=m=(r-2)n.
```

Every irreducible Frobenius factor needed for `E0` therefore has degree
at most the FIXED `m`. The same statement holds on the full `Gamma`
socle. No semisimplicity of the ambient `V` is assumed.

Take the full-multiplicity union of all factors of degree at most `m`
in the characteristic polynomial of `F0`. The direct-sum Weil pairing
on `V` is perfect; `F0` has multiplier `q^b=1 mod ell`. Reciprocal
partners of primary factors have the same degree. Thus the selected
space `V_small` is self-dual and its pairing is nondegenerate. The
target `Gamma` socle itself need not be nondegenerate; it is not used
as the pairing-completeness certificate.

The single extension degree

```
H=ell^ceil(log_ell(max(1,2G_tot)))
    *product_(j=1..m)(ell^j-1)
```

kills every selected semisimple eigenvalue and every possible ambient
nilpotent block. Hence `V_small` is rational over
`K=F_(q^(bH))`. This is polynomial for fixed `n,r`. One may instead use
the smaller single-component dimension `2g_C` when extracting `V_small,0`
on `C_zeta0`; its deck translates provide the full selected space.

Couveignes over that one component, CRT projection, and the exact
pairing-rank certificate are exactly the reviewed construction. A
strict-subgroup trial is accepted only if its projection already spans
the entire selected component space. Translating its certified basis
supplies all components without multiplying independent success
probabilities. If separate calls are used instead, amplify each with
failure budget `eta/(ell-1)`; demanding simultaneous raw one-half
success would be an unnecessary exponential loss.

The operator `A(g_q)sigma` commutes with `F0`, so it preserves
`V_small,0`. Its images in (F) have exact pairing coordinates. The
coefficient precomposition in (F) is fixed-dimensional linear algebra.
All Frobenius/deck operations act on BOTH parts of a divisor:

```
[D-g_C O0] |-> [R_(g_q^-1)(sigma D)
                 -g_C R_(g_q^-1)(sigma O0)].
```

Reduce the result back relative to `O0`; do not assume the displayed
image of the origin equals `O0`.

## 6. Multidegrees, semantic promises, and boundary

For a disconnected curve, `ell`-torsion in its Picard group has degree
zero on EACH component, since multiplication by `ell` multiplies each
integer degree. The paid report's mathematical observation is correct.
Nevertheless a verifier must either keep this multidegree condition
explicit or use componentwise principal-divisor verification. A nonzero
global RR vector on a disconnected curve may vanish identically on
some components; that is not a rational function defining a principal
divisor on all components. The one-component implementation avoids this
trap entirely.

The output can be represented by closed places/ideals over `K`, with
one rational origin per component. Individual support points need not
all become rational. No common support splitting field or hidden
component-field compositum is introduced.

Geometric connectedness of the full `zeta0` frame fibre is a genuine
promise implied by full `Sp` monodromy. Computing the constant field of
one SELECTED irreducible factor alone would not certify that the entire
frame fibre is geometrically connected: other factors could remain.
If certification is desired, also account for every factor and the full
degree `D`. The report's dimensional and constant-field checks are
useful falsifiers, not substitutes for the native frame/evaluation and
monodromy promises.

The genuine evaluation map is crucial. An abstract cover with the same
geometric deck group, branch data, and dimensions could encode a
different arithmetic twist. The identity here pertains to the actual
similitude-frame scheme of the original `L`, with its actual `F_q`
structure. Under that explicit input contract, the coefficient-action
ambiguity is removed; it has not been solved for an arbitrary abstract
cover by a sign test.

The asymptotic cost remains

```
poly_(n,r)(ell, NUMERICAL P, presented size, log(1/eta)).
```

This is not `poly(log P)`, and no new oracle is supplied. The source
algorithms and finite clocks remain the already reviewed ones.

The parabolic residue kernel, native construction of the full frame
presentation, characteristic-zero lifting, model/support heights and
reconstruction are separate obligations. No whole-paper rehabilitation,
native surface point count, novelty, hardness, or quantum speedup is
claimed by this arithmetic repair.
