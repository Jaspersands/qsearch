# Modular descent in the surface torsion-cover construction

2026-11-12. Independent core review. No Git, network, API call, numerical
sweep, or new quantum claim. Read the current `STATE.md` and `TRAPS.md` and
the local primary source `../sources/classical_surface_2026/surfaces.txt`,
especially physical lines 198-318 and 985-1108. The interpreter, if needed,
is `/opt/anaconda3/bin/python`.

Version follow-up: also read physical lines 1000-1057 of
`../sources/classical_surface_2026/surfaces-arxiv.txt`, the arXiv v1 snapshot
whose PDF SHA256 is
`c11807b90ab78528102ddb69fb46b3e7009bcd5c60c023de6326d7591c73e5ba`.
Its proof differs from the author-hosted PDF; the version-specific
disposition below separates their arguments.

## Finding and exact scope

The ordinary-invariant isomorphism in the displayed Theorem 4.1 is false
already on the natural vanishing-cycle summand with no constant part. This
is a geometric dimension obstruction, so arithmetic Galois conventions,
Tate twists, duals, or a choice of sufficiently large odd coefficient prime
cannot remove it. The Hochschild--Serre passage for the OPEN cover is
correct in this case. The unproved passage from the open cover to the
compact cover changes neither side of that open-cover isomorphism: it
retains all of open-curve cohomology, including the non-parabolic classes.

This refutes the displayed identification and its use to justify Algorithm
8's dimension stopping test. It does not prove that the fixed-surface
point-counting theorem cannot be repaired, that no classical polynomial
algorithm exists, or that there is a quantum separation. A conditional
repair retaining local descent data is described below.

## Lemma: modular ramification hides every open residue

Let `k=F_ell`, with `ell` an odd prime. Work over the complex numbers; by
comparison this is enough to test the geometric cohomology in a claimed
number-field theorem. Let

* `U=P1(C) \ {z_1,...,z_r}`, with `r>=3`, and `j:U -> P1`;
* `rho:pi_1(U) -> G` be a surjection to a finite group;
* `M` be a finite-dimensional `k[G]`-module and `L` its local system;
* `V -> U` be the connected Galois cover with group `G`, and `C` its smooth
  compactification;
* `T_i=rho(gamma_i)` for a positively oriented peripheral loop, with order
  `e_i`.

Assume `H^1(G,M)=H^2(G,M)=0`, and assume every local norm operator vanishes:

```
N_i := 1 + T_i + ... + T_i^(e_i-1) = 0  on M.
```

Then restriction and inflation--restriction induce a natural isomorphism

```
H^1(U,L)  ~=  (H^1(C,k) tensor_k M)^G.                 (A)
```

Here the geometric `G` action is the diagonal action appropriate to
Hochschild--Serre, including the coefficient action on `M`. In particular,
this is not an isomorphism with `H^1(P1,j_*L)` in general.

### Proof

Write `Pi=pi_1(U)` and `N=ker(rho)`. The five-term sequence gives

```
H^1(Pi,M) ~= H^1(N,M)^G
           ~= (H^1(V,k) tensor_k M)^G.                (B)
```

Represent a class on the left by a crossed homomorphism
`f(ab)=f(a)+rho(a)f(b)`. Since `N` acts trivially on `M`, its restriction to
`N` is an ordinary homomorphism. A small boundary loop at a point of `C\V`
is conjugate in `Pi` to `gamma_i^(e_i)`. We have

```
f(gamma_i^(e_i)) = N_i f(gamma_i) = 0.
```

For any `a in Pi` and `n in N`, the cocycle identity also gives
`f(a n a^-1)=rho(a)f(n)`. Thus the value is zero on ALL these conjugate
boundary loops, not just on one chosen inertia subgroup per branch point.
Consequently `f|N` factors through `pi_1(C)` and extends to `H^1(C,M)`.

Restriction `H^1(C,M) -> H^1(V,M)` is injective: filling punctures gives a
surjection of fundamental groups. Its image consists precisely of the
characters that vanish on the boundary loops. Since the restriction is
`G`-equivariant, the unique extension of a `G`-invariant class remains
`G`-invariant. Hence its invariant image contains every class in (B),
proving (A). No exactness of the modular invariant functor has been used.

## Specialization to the symplectic natural module

Take `G=Sp_(2g)(F_ell)`, `n=2g>0`, and its natural module `M`. Its central
subgroup `Z={1,-I}` has order two and acts on `M` by a nontrivial sign.
Since two is invertible, `H^q(Z,M)=0` for every `q>=0`: invariants vanish,
and higher cohomology vanishes by averaging. The spectral sequence for
`Z -> G -> G/Z` therefore gives

```
H^q(G,M)=0  for every q>=0.                            (C)
```

For a nontrivial Picard--Lefschetz transvection,
`T=I+D`, `D^2=0`, `rank(D)=1`. Its order is exactly `ell` and

```
sum_(a=0)^(ell-1) T^a
  = ell I + [ell(ell-1)/2] D = 0.                     (D)
```

Thus the lemma applies whenever all critical fibres have a nonzero
vanishing cycle modulo `ell`. For a Lefschetz nodal fibre, the natural
constructible sheaf `F=R^1 pi_* mu_ell` has the invariant-cycle stalk, so
its extension across that puncture is `j_*L`. In the paper's case with
`H^1(X,mu_ell)=0`, the entire `M` is this natural summand, with no issue
from its separately discussed constant summand.

Since `U` has free fundamental group of rank `r-1` and `M^G=0`,

```
dim H^1(U,L) = (r-2)n.
```

The localization sequence is

```
0 -> H^1(P1,j_*L) -> H^1(U,L)
  -> direct_sum_i M/(T_i-I)M -> H^2(P1,j_*L) -> 0.
```

The last group vanishes. Indeed `j_*L/j_!L` is a skyscraper sheaf, so
`H^2(P1,j_*L)=H_c^2(U,L)`; its dual is `H^0(U,L^vee)=0`. Therefore, after
using (A), there is an exact sequence

```
0 -> H^1(P1,j_*L) -> (H^1(C,k) tensor M)^G
  -> direct_sum_i M/(T_i-I)M -> 0.                    (E)
```

Each rightmost summand has dimension `n-1`, so

```
dim H^1(P1,j_*L) = (r-2)n-r(n-1) = r-2n = r-4g,
dim (H^1(C,k) tensor M)^G = (r-2)2g.
```

The excess is exactly `r(2g-1)`. The map in (E) is a DESCENT-residue map:
it cannot be obtained by taking residues on `C`, where these classes are
all unramified. The information was lost from ordinary upstairs residues
because the modular norm (D) is zero.

Equivalently, quotient-stack descent retains stabilizer cohomology at
the branch points. For each cyclic inertia group `C_ell`,
`H^1(C_ell,M)=ker(N_i)/(T_i-I)M=M/(T_i-I)M`. These are exactly the local
terms that ordinary tame coarse-space descent would discard when the
stabilizer order were invertible in the coefficient field. Here it is not.

## Small explicit elliptic examples

Use the Legendre family `E_t: y^2=x(x-1)(x-t)` on
`P1 \ {0,1,infinity}`. In one symplectic basis its local monodromies are

```
A = [1  2;  0  1],
B = [1  0; -2  1],
C = (AB)^-1 = [1 -2; 2 -3].
```

Thus `ABC=I`; `A,B` are nontrivial unipotents, and `C=-I+D` with
`D^2=0`, `rank(D)=1`. Reduction of `A,B` generates `SL_2(F_ell)` for
EVERY odd prime: their powers give all upper and lower elementary
unipotents, which generate `SL_2`. The norm is zero at the first two
punctures by (D). At infinity, `C-I` is invertible and
`(C-I)(1+C+...+C^(2ell-1))=C^(2ell)-I=0`, so its norm is also zero.

Consequently the three-puncture Legendre example has

```
dim H^1(P1,j_*E[ell]) = 2-(1+1+0) = 0,
dim (H^1(C_ell,F_ell) tensor E[ell])^SL2 = 2.
```

Here `C_ell` denotes the smooth compactification of the full geometric
`ell`-torsion trivializing cover, not the cyclic inertia group.

For an example with ALL inertia unipotent, pull back by `t=s^2`:

```
E_s: y^2=x(x-1)(x-s^2),
U_s=P1 \ {0,1,-1,infinity}.
```

At `0` the monodromy is `A^2=[1 4;0 1]`, at `1` it is `B`, at `-1` it
is a conjugate of `B`, and at infinity it is conjugate to
`C^2=[-3 4;-4 5]`. Every one is a nontrivial rank-one unipotent modulo
every odd prime. The image contains `A^2` and `B`, so is again all of
`SL_2(F_ell)`. Thus

```
dim H^1(P1,j_*E_s[ell]) = 0,
dim (H^1(C_ell,F_ell) tensor E_s[ell])^SL2 = 4.        (F)
```

Four punctures are minimal for an irreducible rank-two example with all
inertia nontrivial unipotent: the parabolic dimension formula would give
the impossible negative dimension `r-4` for `r<4`. The four-puncture
family is semistable with fibres of types `I4,I2,I2,I4`; it is a clean
counterexample to the claimed descent mechanism, not itself a pencil
with exactly one node per critical fibre.

For orientation only, Riemann--Hurwitz gives
`genus(C_ell)=1+(ell^2-1)(ell-2)` for the four-puncture cover. At `ell=3`
it is genus nine. These are derived checks, not evidence replacing (A)-(F).

## Instances inside the stated Lefschetz-pencil regime

A generic pencil of plane cubics on `P2`, viewed as hyperplane sections
under its cubic Veronese embedding, has nine base points and twelve
irreducible nodal fibres. Its blowup has `b2=10`, its smooth fibre has
`g=1`, and `r=12`. For the sufficiently large odd primes for which the
paper invokes full symplectic monodromy, the two sides of Theorem 4.1
have dimensions

```
8 = b2(blowup)-2 = r-4g,
20 = (r-2)2g,
```

respectively. Thus the issue is not confined to non-Lefschetz examples.

For the parent's fixed-degree quintic surface example, take `L=3H`.
Adjunction gives `g=31`; `L^2=45` gives 45 base points. A smooth quintic
has Euler characteristic 55 and `b2=53`, so its blowup has Euler
characteristic 100 and `b2=98`. The nodal-fibration Euler formula gives
`r=100-4+4*31=220`. The dimensions are therefore

```
dim H^1(P1,F) = 96,
dim (H^1(C,F_ell) tensor M)^G = 218*62 = 13516.
```

The excess is `220*61=13420`. All these statements retain the full
symplectic/nonzero-transvection hypotheses; no finite test is being used
to establish those hypotheses for an arbitrary pencil.

## Duals, twists, arithmetic, and the purity sentence

The canonical open-cover tensor identity uses
`H^1(V,F_ell) tensor M`. The paper displays `H^1(C,mu_ell) tensor M`.
Possible Tate-twist bookkeeping deserves its own arithmetic check, but
it is irrelevant to this obstruction: over an algebraically closed base
`mu_ell` is a one-dimensional constant space with trivial GEOMETRIC `G`
action. Dualizing or a Tate twist does not change any dimension above.
The natural symplectic module is geometrically self-dual.

Theorem 4.1 claims an isomorphism of arithmetic Galois modules, and hence
must first be an isomorphism of the underlying geometric vector spaces.
It fails that necessary condition. No unspecified arithmetic condition
can fix the displayed ordinary invariant space. A new specified
arithmetic/local restriction would define a different space and needs a
new proof. In particular, invoking purity after good reduction cannot
turn the two different geometric dimensions into equal dimensions.

## Version-specific check: arXiv v1's excision diagram

The arXiv snapshot displays the same ordinary compact-invariant target,
but its proof is DIFFERENT from the author-hosted PDF. It explicitly
isolates the vanishing-cycle sheaf `E` and takes `M=E_eta` before using
Hochschild--Serre. Its final step is an excision diagram, not the
author-hosted PDF's purity sentence. Consequently, neither that purity
sentence nor the author-hosted constant-summand reasoning should be
attributed to the arXiv proof. The dimension obstruction still applies
unchanged to its displayed Theorem 4.1.

Write `q:C -> P1` for the compact cover and `j:U -> P1` for the open
immersion, to avoid the source's overloaded notation. The lower-left
term of the arXiv diagram is

```
H^1(C, q^*j_*E)^G,
```

not `H^1(C,constant M)^G`. At a point above `z_i`, the former sheaf has
stalk `M^(T_i)`, of dimension `n-1`; the latter has stalk `M`, of
dimension `n`. Trivializing `E` over the OPEN cover does not identify
these sheaves over the branch points. Therefore the diagram cannot
supply the constant-sheaf compact invariant space asserted in the
theorem.

There is also a direct error in the displayed bottom row's initial
injection, under the same full-symplectic/transvection hypotheses.
Let `A=q^*j_*E`, let `B=constant M` with its natural equivariant
structure, and let `Q` be their boundary quotient. Stalkwise pullback
and the natural map to the extended constant sheaf give

```
0 -> A -> B -> Q -> 0,
Q_x = M/M^(T_i)  at x over z_i.
```

The one-dimensional quotient `M/M^(T_i)` has trivial inertia action,
since `(T_i-I)M` lies in `M^(T_i)`. Thus, writing `Q_0=H^0(C,Q)`,

```
Q_0 ~= direct_sum_i Ind_(<T_i>)^G (M/M^(T_i)),
dim Q_0^G = r.
```

Moreover `H^0(C,A)=0`: a constant global vector in its stalks would
belong to the intersection of all `G`-conjugates of a proper inertia
fixed subspace; that intersection is a proper `G`-submodule of the
simple natural module. The sheaf cohomology sequence consequently
identifies the kernel of `H^1(C,A) -> H^1(C,B)` with
`K=Q_0/M`. Because `M^G=H^1(G,M)=0`, the group cohomology sequence for
`0 -> M -> Q_0 -> K -> 0` gives `K^G ~= Q_0^G`. Finally restriction
`H^1(C,B) -> H^1(V,B)` is injective. Therefore

```
dim ker[H^1(C,q^*j_*E)^G -> H^1(V,E|V)^G] = r.
```

So the claimed lower row beginning with zero is not exact even before
one tries to replace its constructible pullback sheaf by the constant
sheaf. Ordinary excision includes the preceding local-support term;
in this situation that term cannot simply be omitted. This is a
version-specific verification of the same obstruction, not a new
whole-paper review. The arXiv Tate-twist remark likewise cannot alter
the underlying geometric dimensions.

## Algorithm 8: precise consequence

Let `H=H^1(C,F_ell)` and

```
E = sum_(phi in Hom_G(M^vee,H)) im(phi).
```

By this definition, every equivariant map into `H` factors through `E`,
so

```
(E tensor M)^G ~= Hom_G(M^vee,E)
                 = Hom_G(M^vee,H)
                 ~= H^1(U,L).
```

Thus once Algorithm 8 has reached the full subspace it defines, its
invariant dimension is `(r-2)2g`, exceeding its intended
`b2(blowup)-2=r-4g`. The natural module is absolutely simple and its
endomorphism ring is `F_ell`; hence the sum above is an isotypic socle
of dimension `2g * (r-2)2g`, still independent of `ell` for a fixed
pencil, but the wrong representation for the asserted surface quotient.

Do NOT claim that the written loop necessarily never stops on every
input. An intermediate rationality field could accidentally yield the
numerical target, in which case equality of dimensions alone does not
identify the parabolic subspace. Alternatively, no intermediate field
may attain that target. What is proved is that the asserted full-space
identification and its stopping proof fail. Replacing the target by the
larger dimension may locate all open cohomology, but does not compute
the kernel of (E), which is the required surface contribution.

## Conditional repair by retaining Kummer and inertia data

The larger open-cohomology space still has fixed dimension for a fixed
pencil. A plausible repair is to realize its elements as actual
equivariant covers and apply the local restriction in (E). This is a
mathematical repair target, not a completed complexity theorem.

For a nonzero invariant tensor `beta`, the corresponding equivariant
character `psi:pi_1(C) -> M` is surjective because `M` is simple. It
defines an unramified `M`-cover `W -> C` of degree `ell^n`. Its composite
over `P1` is Galois, with an extension

```
1 -> (M,+) -> E_beta -> G -> 1.
```

This extension admits a particularly explicit complement. Let `z_hat`
be ANY lift of central `-I`. Its square lies in `M` and is fixed by
conjugation by `z_hat`, which acts on `M` by negation; therefore
`z_hat^2=1`. The centralizer `C_(E_beta)(z_hat)` meets `M` trivially. For
any lift `e` of `g in G`, write
`e z_hat e^-1 = c z_hat`, with `c in M`. Then

```
(m e) z_hat (m e)^-1 = (c+2m) z_hat.
```

Choosing `m=-c/2` makes `m e` centralize `z_hat`. Therefore this
centralizer projects bijectively onto `G` and is a complement, yielding
`E_beta ~= M semidirect G`. This gives a direct constructive explanation
of the relevant `H^2(G,M)=0` fact when the finite extension group itself
is available.

Write a lifted local inertia generator in this splitting as `(a_i,T_i)`.
Then `beta` is parabolic if and only if

```
a_i belongs to (T_i-I)M  for every i.                 (G)
```

Changing a complement adds a coboundary, hence does not change this
criterion. Geometrically it says the lifted inertia is conjugate by an
element of `M` to `(0,T_i)`. All lifted inertia still has order `ell`
because the norm is zero, so the ramification ORDER alone does not
detect (G).

There is also an intrinsic version requiring no chosen complement. If
`tau_i` is a lifted inertia generator and `p:E_beta -> G` is the quotient,
then (G) is equivalent to

```
C_(E_beta)(tau_i) intersects p^-1(-I).               (H)
```

To prove this, use a temporary splitting only for the calculation.
Write `tau_i=(a,T)` and an arbitrary lift of `-I` as `z=(b,-I)`. Then

```
z tau_i = (b-a,-T),
tau_i z = (a+Tb,-T).
```

They commute exactly when `(I-T)b=2a`. Since `ell` is odd, solvability
is exactly `a in (T-I)M`. Thus the existence in (H), rather than a
selected lift, is essential. All lifts of `-I` have order two by the
preceding argument.

The predicate (H) is invariant under conjugating the inertia generator
in `E_beta`, because `-I` is central in `G`. It is invariant under
replacing `tau_i` by a unit power: this generates the same cyclic
inertia subgroup and has the same centralizer. Here `tau_i` has order
`ell`; the same argument works for any finite inertia order with a
power relatively prime to that order. Finally, it is preserved under
any arithmetic automorphism of the extension that preserves `M` and
fixes scalar `-I` in the quotient, as arithmetic conjugation on the
natural symplectic module does. Such an automorphism sends the two
sets in (H) to their counterparts. No common path, basis, or transport
between different punctures is needed for this zero-membership test:
the individual inertia conjugacy classes suffice. This is a local
membership simplification, not a construction of those classes or a
complete arithmetic representation algorithm.

To turn this into an algorithm, one must actually construct Kummer
functions (divisors `D` together with functions of divisor `ell D`),
the extension group with its quotient map, and its local inertia
conjugacy classes, with controlled fields, heights, and arithmetic
Galois action. Linear
`G`-action matrices on Jacobian torsion alone do not provide that
extension and local data. The degree `ell^n |G|` is polynomial in `ell` when `n`
is fixed, which removes one obvious degree objection, but it pays none
of the remaining representation, height, or arithmetic obligations.

## Handoff boundary and next hard question

PROVED: the lemma and dimension obstruction, including the exact local
quotient and the explicit Legendre examples. REFUTED: Theorem 4.1 as
displayed and its ordinary-invariant justification of Algorithm 8.
CONDITIONAL: the Kummer/local-inertia repair as an effective bounded-cost
procedure. OPEN: a repaired fixed-surface algorithm and, separately,
uniform native finite-field coefficient complexity. All novelty,
hardness, separation, and end-to-end implementation gates remain false.

The parent should record this finding in the current handoff and state;
this focused review does not edit their shared coordination files.
Mechanical acceptance item: verify one frozen `SL_2(F_3)` Legendre cover
calculation against the proved geometric dimensions, without promoting
that finite control into the theorem. Next hard question: whether the
local descent map in (E) can be computed from explicitly represented
Kummer functions and local inertia conjugacy classes (or the equivalent
intrinsic predicate (H)) with polynomial fixed-surface field/height
bounds. A changed dimension threshold alone is not an
acceptance test for that repair.

## Independent review of the finite-field filtering primitive

The parent's subsequent finite-field construction closes the group,
constant-field, and local-inertia obstacles for a substantially stronger
PRESENTED input. This is an algorithm for filtering a supplied module,
not a reconstruction of that module from a native surface equation.

### Exact input and cost boundary

Fix `n=2g` and `r`. Let `k` be an explicitly represented finite field of
characteristic `P` with `P` prime to `ell |G|`, where `ell` is odd and
`G=Sp_n(F_ell)`. Supply the smooth compact cover `C -> P1` by a
separable primitive function-field model and supply its `G` deck maps.
Promise that its geometric branch locus has `r` points, all with
nontrivial transvection inertia of order `ell`. Supply a COMPLETE basis
of `W=Hom_G(M^vee,H^1(Cbar,mu_ell))`, each of its `n` components by an
actual degree-zero torsion divisor representative. Numerical positive
and negative divisor degrees, finite-field degrees, model and function
coordinate sizes, and integral/ideal representations are charged.

These representatives must live over an explicitly represented common
finite field, or over at most the fixed number `n dim(W)` of explicitly
represented fields. In the latter case their compositum degree is at
most the product of that fixed number of degrees, hence polynomial in
the charged representation size. A divisor encoded by arbitrarily many
unrelated geometric support fields does not provide a free common
field. Closed places and residue fields may be handled individually.

Supply the GENUINE arithmetic Frobenius matrix on `W`, with compatible
action on `M`, the normalizer action on `G`, and the coefficient twist.
This is a semantic input promise. The filter does not prove that an
arbitrary supplied matrix has this meaning or construct it from torsion
points. Arithmetic stability and the returned restricted Frobenius
depend on this promise.

Under these input conditions, the reviewed procedure has randomized
bounded cost polynomial in `ell`, the NUMERICAL characteristic `P`,
the charged presentation size, and `log(1/eta)`, for fixed `n,r`, with
failure probability at most `eta`. Failure must be reported as failure,
not as a partial parabolic space. This is not a uniform `poly(log P)`
claim and not a `poly(log ell)` claim. For a separately paid auxiliary
prime with numerical `P` polynomial in the intended parameters, it
removes this finite filtering obstruction.

### Kummer construction and finite constant-field clock

Adjoin `mu_ell` with degree at most `ell-1`. Enumerating `ell^dim(W)`
vectors is polynomial in `ell` because `dim(W)<=(r-2)n` is fixed. A
nonzero `beta` is injective on the simple module `M^vee`; its component
torsion classes are consequently independent. Computing a nonzero
element of `L(-ell D_i)` gives `f_i` with divisor `ell D_i`. The
Kummer equations `y_i^ell=f_i` therefore define a geometrically
connected unramified cover `Y_beta -> C` of degree `ell^n`. Arbitrary
nonzero scalar normalizations of these functions change only its
arithmetic form, not the geometric cover or local membership test.

The composite has geometric deck group `E_beta` of order
`D=ell^n |G|`. Its function-field presentation is obtained from a fixed
number of root equations. Standard elimination in this fixed-length
tower has polynomial degree and coordinate size in the charged model
parameters and `ell`; this does not assert such a bound for an
arbitrary high-ambient implicit input. A primitive linear combination
can be found over a constant field with more than `D^2` elements:
nonprimitive choices lie in at most `D(D-1)/2` equality hyperplanes
between embeddings. This costs an extension of degree `O(log D)`,
not literally constant degree. The proposed element's degree is
verified in the `D`-dimensional presented field.

Every geometric deck map is defined over a polynomial-degree constant
extension. Indeed all type-C root elements with parameter one generate
`G`, since `ell` is prime and their powers supply all root parameters.
Lifts of those elements, together with `n` kernel generators, generate
`E_beta`; the explicit bound `s=n+n^2` suffices. An automorphism is
determined by its values on these generators, so

```
|Aut(E_beta)| <= D^s,             s=n+n^2.
```

Because `Y_beta` is a defined, geometrically connected finite-field
model, arithmetic Frobenius acts on its GEOMETRIC deck maps as an
actual group automorphism. This is not merely an outer action. Its
order is at most `D^s`; over the corresponding constant extension all
deck maps are defined. Thus searching `1<=h<=D^s` is a valid finite
clock. Geometric connectedness ensures `k_h(Y_beta)` is a field for
every `h`. Factoring the primitive minimal polynomial over that field
and finding `D` distinct linear roots is equivalent to obtaining all
`D` deck maps. No lcm of arbitrary factor degrees is invoked.

### Root finding and local places have polynomial presented size

The primary algorithm sources inspected in this review are:

* Voloch, `../sources/classical_surface_2026/function_factor.txt`,
  Lemma 3.1, Algorithm 1, Remark 3.3, Theorem 4.1 and its suitable-place
  discussion. The displayed cost is polynomial in numerical `P`,
  not automatically in `log P`.
* Kozen, `../sources/surface_torsion_selection/kozen_resolution.txt`,
  introduction and problem statement: polynomial-bit resolution of
  plane curves over any finite field, with local parameters and
  individual branch data.
* Eisentraeger--Hallgren,
  `../sources/classical_surface_2026/function_rr.txt`, the input
  convention and divisor height definition, Appendix B Algorithm B.8
  and Theorem B.9. This Riemann--Roch subroutine is CLASSICAL; its cost
  is polynomial in extension degree, `log q`, and numerical divisor
  height, for the supplied ideal/infinite-place representation.

For the monic primitive polynomial `P(t,T)`, choose an effective
divisor `A` on `P1` bounding the poles of every coefficient. Its degree
is polynomial in the presented polynomial degrees. Every root lying
in `k_h(Y_beta)` belongs to

```
L_(Y_beta)(q^*A),  of dimension <= D deg(A)+1,
```

by Voloch's root-valuation inequality. For his Wronskian bound one
must also allow quotient fields of polynomial factors of degree up to
`D`; the conservative bound `Delta<=D^2 deg(A)` pays that additional
degree. Thus neither the coefficient space nor the derivative order
is an uncharged search parameter. Remark 3.3 may return only one
factor at a time; at most `D` repetitions suffice. Constants obtained
from residue fields must be tested for membership in the current
constant field, so an absolute factor over a larger field is not
mistaken for a deck map over `k_h`.

A suitable place for that root algorithm is explicit here. Choose
`t=a` avoiding the presented denominators and discriminant, in a
finite extension with more elements than their total degree. Factor
the specialized plane polynomial. ANY irreducible factor gives a
place of residue degree at most `D deg(a)` and a known uniformizer.
It is unnecessary, and can be impossible for a noncyclic Galois
cover, to require the WHOLE specialized polynomial to be irreducible.
Thus no such Chebotarev assumption or large residue-field lcm enters
the bound.

The Riemann--Roch source globally assumes one rational infinite place.
Its Appendix B calculation does not visibly use that condition, but
a conservative literal application can ensure it: choose ONE infinite
place and adjoin its residue field, of degree at most the presented
cover degree. For `C` this can precede the component Riemann--Roch
computations; for `Y_beta` it can precede fixing the root-search base
field. Subsequent constant extensions preserve that rational place.
This remains polynomial and requires no simultaneous splitting of all
infinite places. It does not change which original Frobenius matrix
the input promises.

### Inertia and arithmetic output

The `D` computed maps give the multiplication table by composition,
and restriction to the supplied `C` generators identifies their
quotient in `G`. For each CLOSED branch point `z`, choose one place
`w` above it. Its absolute residue degree is at most `D deg(z)`, with
`deg(z)<=r`. Enumerating the deck maps that stabilize `w` and act
trivially on its residue field computes the actual inertia subgroup.
Since `Y_beta -> C` is unramified, this subgroup has order `ell`.
The intrinsic centralizer test (H) therefore decides parabolicity
using any nonidentity element of that subgroup. Individual local
residue fields suffice; no common splitting field for all branches
is required.

Checking one such place for each closed branch point suffices by
geometric conjugacy and arithmetic invariance of (H). Collecting all
accepted vectors gives exactly the parabolic kernel, hence an
`F_ell`-linear subspace. The supplied genuine Frobenius preserves it,
and its restricted matrix is then obtained by linear algebra. The
temporary fields used to construct individual covers need not be a
common field for all `beta`.

This proves the scoped finite primitive with the stated input and
numerical-characteristic charge. It does NOT supply the complete
torsion-module basis, its arithmetic Frobenius, a small good auxiliary
prime, characteristic-zero lifting, or uniform reconstruction heights.
Those upstream promises and height obligations remain separate. No
whole-paper rehabilitation, native point-counting algorithm, hardness,
or quantum-separation claim follows from this filtering result.
