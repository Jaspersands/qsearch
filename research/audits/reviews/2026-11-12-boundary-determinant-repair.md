# Boundary determinants replace parabolic-subspace extraction

2026-11-12. Independent core review. Read current `STATE.md`, the actual
nodal-fiber passages in `audits/sources/classical_surface_2026/surfaces.txt`
and `audits/sources/surface_module_2026/etale_p1.txt`, the stable
`2026-11-12-surface-full-similitude.md` review, and the actual primary
Pila sources `sources/surface_torsion_selection/pila_frobenius.txt` and
`sources/legendre_prf/pila_curve_families_0504570.txt`, including the latter's
Theorems D--F and H and their proofs. Source paths in this paragraph are
relative to `research/audits/` where not already specified.
No Git, network, API, archive search, new code, or numerical sweep.
Interpreter if needed: `/opt/anaconda3/bin/python`.

## Verdict and the two useful formulas

The proposed determinant repair is correct. It does not require
constructing, recognizing, or splitting off the parabolic subspace.
The Tate factors are essential, but they give exactly the proposed
`q^2` formula for the untwisted cohomological local system.

Let `f:Y->P1/F_p` be the actual Lefschetz fibration, `U` its smooth
locus, and `j:U->P1`. Put

```
L'=R^1 f_*F_ell on U,
O=H^1(U_bar,L'),
P=H^1(P1_bar,j_*L').
```

Assume `ell!=p`, with `ell` odd; the geometric generic fiber has
genus `g`; every singular geometric fiber is geometrically irreducible
with exactly one ordinary node and nontrivial transvection inertia;
and the geometric global invariants of `L'` and its dual vanish.
The actual full-natural-monodromy hypothesis ensures the last condition.

For each CLOSED branch point `z`, write

```
f_z=[k(z):F_p],       q_z=p^f_z,
C_z = the nodal fiber over k(z),
Ctilde_z = its smooth normalization,
epsilon_z = +1 if the two tangent branches split over k(z), -1 otherwise,
P_z(S)=det(1-S*Frob_geom,q_z | H^1(Ctilde_z,F_ell)).
```

The normalization polynomial can equivalently be computed integrally
as the zeta numerator and reduced modulo `ell`. If `O_geom(T)` is the
characteristic polynomial of GEOMETRIC Frobenius on `O`, then

```
P_geom(T) = O_geom(T) / B_geom(T),

B_geom(T) = product_z
    [(1-epsilon_z*q_z^2*T^f_z) * P_z(q_z*T^f_z)].       (1)
```

There is an even simpler formula for the ACTUAL output of the
full-similitude repair. Its proved convention is

```
W = Hom_GSp(N^vee,H^1(C_full_bar,mu_ell))
    ~= H^1(U_bar,L')(2),
```

and its computed `Phi_W` is ARITHMETIC Frobenius acting on divisors.
For precisely that convention,

```
P_geom(T) = det(1-T*Phi_W) / B_W(T),

B_W(T) = product_z
    [(1-epsilon_z*T^f_z) * P_z(T^f_z)].                (2)
```

Formula (2) also uses the perfect parabolic self-duality proved in
Section 5 below. It does not silently identify arithmetic and
geometric Frobenius on open cohomology. Both divisions are EXACT
polynomial divisions over `F_ell`, including when factors or
eigenvalues coincide and representations are not semisimple.

For the native cubic pencil on a smooth quintic, `g=31` and the
number of GEOMETRIC branch points is

```
r=sum_z f_z=220.
```

The open dimension is 13516, the boundary dimension 13420, and
the parabolic dimension is 96. Only this determinant, not an
embedded 96-dimensional submodule, is needed for the characteristic
polynomial.

## 1. The exact sequence and why its final obstruction vanishes

For the open immersion `j`, the stalk of `R^1 j_*L'` at a geometric
branch point is `H^1(I_z,M)`, where `M` is the geometric generic
fiber of `L'`. It is a skyscraper sheaf, and higher inertia
cohomology vanishes in this tame prime-to-characteristic setting.
The Leray five-term sequence gives the Frobenius-equivariant sequence

```
0 -> P -> O -> direct_sum_(geometric z) H^1(I_z,M)
  -> H^2(P1_bar,j_*L') -> H^2(U_bar,L').
```

To check the advertised zero, use the ordinary-sheaf exact sequence

```
0 -> j_!L' -> j_*L' -> direct_sum_z i_(z,*) M^I_z -> 0.
```

Skyscraper sheaves on the geometric curve have no positive-degree
cohomology. Hence

```
H^2(P1_bar,j_*L') ~= H_c^2(U_bar,L').
```

Poincare duality identifies the latter with the dual of
`H^0(U_bar,(L')^vee)`, with a Tate twist. It is zero under the
stated dual-invariant hypothesis. The cup-product pairing on
`L'` identifies its geometric dual with itself up to a constant
Tate twist, so the natural symplectic-monodromy hypothesis
indeed kills both invariant spaces. In a general nonsemisimple
representation, merely asserting that its own invariant space
vanishes would not suffice to kill invariants of its dual.

Thus the sequence needed here is genuinely SHORT EXACT:

```
0 -> P -> O -> Boundary -> 0.                           (3)
```

No averaging over the monodromy group is used. In particular
`ell` dividing its order does not obstruct (3). Also, the exact
sequence for `j_! -> j_*` shows that `P` is precisely the image
of `H_c^1(U_bar,L')->H^1(U_bar,L')`.

The tame Euler characteristic and vanishing of global invariants
give `dim O=(r-2)*2g`. Each transvection has coinvariant
dimension `2g-1`, so

```
dim Boundary=r*(2g-1),       dim P=r-4g.
```

For `(g,r)=(31,220)` these are respectively `13516,13420,96`.

## 2. The local Tate calculation

Fix a closed `z`, set `q=p^f_z`, and let `F_z` denote GEOMETRIC
Frobenius on the inertia invariants `V=M^I_z`. We use the
convention that geometric Frobenius acts on `F_ell(1)` by
`q^(-1)` and on `F_ell(-1)` by `q`.

Evaluation of an inertia cocycle at a tame generator gives the
canonical, Frobenius-equivariant identification

```
H^1(I_z,M) ~= M_I_z(-1).                              (4)
```

The twist can be checked directly: replacing the generator by
its `a`-th power multiplies cocycle evaluation modulo
`(T-1)M` by `a`. Equivalently, geometric Frobenius conjugates a
tame generator by `q^(-1)`, while its action on cochains uses
the inverse conjugation, producing the factor `q` in (4).

The fiber cup pairing is perfect alternating,

```
M x M -> F_ell(-1).
```

Its annihilator of `M^I_z` is `(T-1)M`: inclusion follows from
invariance of the pairing and equality follows from dimensions.
It therefore induces a perfect pairing of the coinvariants with
the invariants, giving

```
M_I_z ~= (M^I_z)^vee(-1),
H^1(I_z,M) ~= V^vee(-2).                              (5)
```

Consequently the local geometric boundary matrix is

```
q^2 * F_z^(-T).                                      (6)
```

The transpose has no effect on its characteristic polynomial.
Using `q*F_z`, or omitting either of the two negative Tate
twists, would be an error for this `L'` convention.

A split nodal elliptic degeneration is a useful exact local
check: its invariant line is `F_ell`, its coinvariant line
is `F_ell(-1)`, and its boundary line is `F_ell(-2)`.
The geometric boundary eigenvalue is therefore `q^2`.

## 3. Nodal invariants, normalization, and the tangent sign

Proper base change and the invariant-cycle statement for a
regular one-node Lefschetz degeneration identify

```
M^I_z ~= H^1(C_z,F_ell).
```

This is also visible directly in the retained nodal source:
the specialization map is injective of dimension `2g-1`,
while the transvection invariant space has that same dimension.
The map is equivariant for the residue-field Frobenius. The
source uses `mu_ell`; untwisting gives the present convention.

Let `nu:Ctilde_z->C_z` be normalization. The unique geometric
node is rational over `k(z)`. Its two preimages are either
both rational or exchanged by Frobenius. The quotient of the
two constant stalks by the diagonal is a one-dimensional sign
representation. The normalization sheaf sequence therefore gives

```
0 -> F_ell(epsilon_z)
  -> H^1(C_z,F_ell)
  -> H^1(Ctilde_z,F_ell) -> 0.                        (7)
```

In particular, without assuming a splitting of (7),

```
det(1-S*F_z)=(1-epsilon_z*S)*P_z(S).                  (8)
```

The sign can also be checked without cohomological conventions:
over `F_(q^k)` the two preimages of the node contribute
`1+epsilon_z^k` points, whereas the node contributes one.
Thus `#C_z(F_(q^k))=#Ctilde_z(F_(q^k))-epsilon_z^k`,
which gives the graph trace `epsilon_z^k` in (8).

The normalization is geometrically connected of genus `g-1`.
Its Frobenius `F_norm` satisfies
`F_norm^T J F_norm=q J` for its perfect cup pairing. Hence the
EXACT matrix identity up to conjugation with a transpose gives

```
det(1-q^2*S*F_norm^(-1))=det(1-q*S*F_norm)=P_z(q*S).
```

Combining with (6)--(8), the local boundary determinant is

```
(1-epsilon_z*q^2*S)*P_z(q*S).                        (9)
```

This calculation uses determinant identities, not diagonalization
or a choice of Frobenius eigenspaces. It remains valid modulo
`ell` at repeated eigenvalues.

For odd `p`, compute `epsilon_z` from the nondegenerate binary
quadratic tangent cone at the node. After eliminating the one
linear ambient equation, write the quadratic as
`a u^2+b u v+c v^2`. Its discriminant `b^2-4ac` is nonzero;
its quadratic character in `F_q` is exactly `epsilon_z`.
Binary powering computes this in `poly(log q)` field-bit cost;
no choice of either tangent branch is needed. The native large
characteristic assumption excludes the characteristic-two
variant of this test.

The irreducibility hypothesis matters. A reducible one-node
fiber has a different normalization/dual-graph sequence; one
must not apply (7) with a connected genus-`g-1` normalization
to that case.

## 4. Closed points and determinant multiplicativity

Over `F_pbar`, a closed point of degree `f` gives `f` boundary
summands cyclically permuted by geometric Frobenius. The `f`-th
power on one summand is its local `F_q` geometric Frobenius.
For any such cyclic block representation and any local matrix
`A`, elementary block elimination gives

```
det(1-T*Frob_p on the f summands)=det(1-T^f*A).
```

This is the determinant formula for induction from the residue
field. It is valid in every coefficient characteristic, even
when `ell` divides `f`. Substitution `S=T^f` in (9) gives
exactly the closed-point factor in (1).

Choose any vector-space basis adapted to the invariant subspace
in (3). Frobenius is block upper triangular. Its determinant
is the product of the determinants of the subspace and the
quotient whether or not the extension splits. This proves (1)
and establishes exact divisibility. Shared factors between the
boundary and parabolic polynomials do not affect this division.

One should verify the computed identity by multiplying the
quotient back by the boundary polynomial. Failure is an input,
convention, or computation error; it is not repaired by selecting
a nearby polynomial or cancelling only some matching roots.

## 5. Direct use of the actual full-similitude output

The stable full-similitude review proves

```
W ~= H^1(U_bar,J_fiber[ell])(1)
   ~= H^1(U_bar,L')(2)
```

with the actual ARITHMETIC Frobenius on the left. Thus the
geometric open matrix, if wanted explicitly, is

```
Phi_open,geom = p^2 * Phi_W^(-1).
```

At a closed point of degree `f`, the arithmetic boundary matrix
on the twist by `(2)` is

```
q^2 * (q^2*F_z^(-T))^(-1)=F_z^T.
```

Its induced characteristic factor over `F_p` is therefore
`(1-epsilon_z*T^f)*P_z(T^f)`, precisely `B_W` in (2).
After division the result is the arithmetic characteristic
polynomial on `P(2)`.

To identify this with the geometric polynomial on `P`, use
parabolic duality, not a purity or semisimplicity assumption.
Poincare duality and the alternating coefficient pairing give
a perfect pairing

```
A x O -> F_ell(-2),       A=H_c^1(U_bar,L').
```

Let `h:A->O` be the natural map. Its induced pairing
`(a,b)-><a,h(b)>` is symmetric: the degree-one cup sign and
the alternating coefficient sign cancel. Thus `h` is
self-adjoint. On `P=im h`, define

```
<h(a),h(b)>_P = <a,h(b)>.
```

It is well-defined because `ker h` annihilates `im h`.
If `h(a)` annihilates all `h(b)`, self-adjointness and the
perfect pairing `A x O` force `h(a)=0`. Therefore this is a
perfect symmetric pairing

```
P x P -> F_ell(-2),      equivalently P(2) ~= P^vee.
```

Arithmetic Frobenius on `P^vee` has the characteristic
polynomial of geometric Frobenius on `P` (the matrices are
inverse transposes). This proves formula (2) directly. There
is no need to materialize `P`, invert a large open matrix, or
match its eigenvalues with the nodal ones.

If an implementation uses a different natural-module/dual
convention, it must first establish its actual arithmetic
identity. In particular for `J_fiber[ell]=L'(1)` alone the
geometric local boundary factor would instead be
`(1-epsilon_z*q*T^f)*P_z(T^f)`. Mixing these conventions is
not justified by the abstract dimension of the module.

## 6. Computing all boundary factors on the native input

Only fixed-complexity curves occur here. A branch fiber is a
degree-15 `(5,3)` complete intersection in `P^3` of arithmetic
genus 31, with one ordinary node. Its normalization has genus
30. The branch degree `f` is at most 220, so
`log q=f log p=O(log p)` with a fixed constant.

There is a direct bounded-format normalization construction.
Locate the unique node over `F_q` by fixed-degree elimination
of the curve and singularity equations. It is rational because
it is the unique geometric node. Blow up `P^3` at this point
and take the strict transform of the curve. One blowup resolves
an ordinary node, including a nonsplit one. The blowup embeds
as the graph of the direction map in `P^3 x P^2`; a Segre
embedding puts the smooth strict transform in `P^11`. Its
degree is

```
(2H-E).Ctilde = 2*15-2 = 28,
```

because the original curve has multiplicity two at the node.
The graph equations and strict-transform saturation involve
a FIXED number of variables and bounded degrees. They can
therefore be constructed by exact finite-field elimination
in polynomial time in `log q`, with fixed format constants.
This constructs the normalization over `F_q`; it does not
split its two exceptional points or change its field of
definition.

For the subsequent zeta computation, the source distinction
is important. Pila 1990 Theorem A requires a COMPLETE explicit
Jacobian addition atlas, and its fixed-`Q` curve Theorem B
does not alone imply the required native uniformity. The
actual retained Pila 2005 paper pays this: Theorems D and E
construct finitely many complete Jacobian presentations by
stratification, E removes the rational-divisor input, and F
gives a deterministic `B1*(log q)^B2` algorithm for every
good specialization of a fixed curve presentation. These
presentations allow relations and constituent prime ideals
over `Z[a]` and specializations to arbitrary fields. Theorem
H explicitly handles fixed singular plane families by finite
normalization strata as an alternative route.

Our marked one-node complete-intersection family and its
degree-28 strict transforms have fixed ambient and degree
format. The finitely many coordinate/pivot charts and the
source's finite all-field stratification provide exactly the
fixed presentations required by Theorem F. Their finite
precomputation depends only on that fixed family, not on the
input coefficients, `p`, or `ell`. Therefore each `P_z` is
classically computable in `poly(log q)=poly(log p)` time.
This is a fixed-family theorem; no growing-genus polynomial
bound is being claimed or used.

To list closed branch points, factor the fixed-degree branch
polynomial over `F_p`, including the point at infinity when
present. Standard bounded randomized finite-field
factorization costs `poly(log p,log(1/eta))` here; its output
is exactly checkable. Given the branch residue fields, all
the curve-zeta calls above are deterministic. There are at
most 220 such calls. Polynomial products, evaluation at
`q*T^f`, reduction modulo `ell`, and exact division have
polynomial bit cost. No numerical-`p` factor is hidden in
the large-characteristic boundary calculation.

For any additionally required fixed polynomial threshold
`p<=Q(ell)`, the native surface can instead be counted
directly over `F_(p^j)`, `1<=j<=53`; brute-force enumeration
has `p^{O(1)}` cost because the ambient dimension and 53
are fixed, hence is polynomial in numerical `ell` in this
regime. Newton identities recover the degree-53 `P2`.
Thus an excluded small-characteristic implementation case
need not become an uncharged exceptional-prime oracle.

## 7. Optional final Leray determinant for the quintic surface

Let `X` be the smooth quintic and `Y=Bl_B X` its pencil
blowup, with the transverse base scheme `B` of degree 45.
All singular fibers being irreducible gives

```
R^0 f_*F_ell=F_ell,
R^1 f_*F_ell=j_*L',
R^2 f_*F_ell=F_ell(-1).
```

The two relevant Leray differentials vanish: their source
or target is `H^0(P1_bar,j_*L')=0` or
`H^2(P1_bar,j_*L')=0`. Consequently `H^2(Y_bar,F_ell)`
has a Frobenius-stable filtration with graded pieces
`F_ell(-1), P, F_ell(-1)`. Determinant multiplicativity
therefore gives

```
P2(Y,T)=(1-p*T)^2 * P_geom(T).
```

No section, degree-45 section-sum projector, or semisimple
splitting is needed for this identity. The blowup formula
then gives

```
P2(X,T) = (1-p*T)^2 * P_geom(T)
          / product_(b closed in B)(1-p^deg(b)*T^deg(b)).
```

Its degree is `96+2-45=53`. The base-point factor is the
permutation/Tate representation of the exceptional divisors
and is computed from another fixed-degree finite etale
scheme. This is again an exact determinant identity,
including modulo `ell`; no eigenvalue matching is required.

## Consequence and remaining boundary

For characteristic-polynomial output, the full parabolic
membership/Kummer-cover/inertia-transport interface is
unnecessary once the genuine complete OPEN module and its
Frobenius are computed. Fixed-genus normalization zeta
polynomials and the tangent signs remove the boundary
determinant, and the final Leray/blowup factors give the
native surface polynomial. This does not rehabilitate the
false compact-invariants-equals-parabolic theorem: those
ordinary invariants still give the larger OPEN module.

The upstream module, true arithmetic action, native cover,
certified reconstruction and prescribed-prime reduction
obligations remain whatever their separate proofs establish.
This result removes the parabolic-subspace extraction
obligation; it does not assume those upstream inputs.
Parent owns shared state/handoff updates after independent
review. No numerical sweep is needed for these determinant
identities.
