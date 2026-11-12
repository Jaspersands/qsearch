# Supplied-atlas symplectic level cover: independent review

2026-11-12. Reviewed the completed report
`audits/openai_runs/2026-11-12-closure-level-cover/response.md`, its exact
`audits/api_inputs/2026-11-12-surface-closure/level-cover.md` obligation,
the retained Pila excerpts in `pila-source.md`, current `STATE.md`, and
`SURFACE_NATIVE_TORSION_MODULE.md`. Report labels are not evidence.
No Git, network, API, archive, new code, or numerical sweep was used.

**Disposition.** A polynomial degree, logarithmic coefficient-height and
bit-cost construction is valid for the unmarked cover, base map, torsion
coordinates and deck generators, under the strong supplied-atlas contract.
The proof below replaces the report's delicate deformation-elimination
sketch by Pila's explicit fixed-variable membership construction and makes
the factorization search precise. A specified zeta-normalized universal
symplectic frame is still missing one pairing evaluation. Construction of
the atlas from native curves remains a separate assumption.

## 1. Hypotheses and the exact output

Fix the original fibre genus a and a specified atlas type
`tau=(N,S,d_0,R,D)` bounded by functions of a alone. Supply:

- a projective model A/Q(t) of the Jacobian, with at most S equations of
  projective degree <=d_0 in P^N;
- equations generating the actual radical ideal on EVERY standard affine
  patch, not just equations with the right geometric zero set;
- a complete geometric addition atlas of <=R charts, of bounded
  bidegrees <=(D,D), and the identity;
- all coefficient and identity-coordinate numerators/denominators with
  t-degree <=T and integer logarithmic coefficient height <=B;
- the Jacobian/principal-polarization promise over Q(t), and full geometric
  mod-ell image Sp_(2a)(F_ell), for an odd PRIME ell.

Completeness is over geometric points, not merely Q(t)-rational points.
Neither the Jacobian, radicality, completeness nor monodromy promise is
proved by this construction. Put n=2a and
`k=Q(zeta_ell), K=k(t)`. All arithmetic in the degree-(ell-1) field k is
charged, using its cyclotomic power basis.

The admitted output is a monic irreducible `q(t,Y)` over K of Y-degree
`s_ell=ell^(a^2) product_(i=1)^a(ell^(2i)-1)`, an ordered torsion basis in
K[Y]/q, and explicit deck generators `Y -> u_g(t,Y)/v_g(t)` with
`deg_Y u_g<s_ell`. The normalization of this plane function field is the
compact cover. Degree, logarithmic coefficient height, dense output size
and deterministic bit cost have an envelope

    (2+ell+B+T)^(C_tau).

The exponent depends on the fixed type and a, never on a particular
surface or curve. Calling this `poly_a(ell,B)` additionally requires a
genus-uniform polynomial bound for T in B. Neither an uncharged t-degree
nor a family-dependent atlas type can be suppressed.

## 2. Expanded multiplication charts and scheme correctness

The binary chart construction is sound. Doubling substitutes the SAME
parent chart into both entries of one addition chart; an odd binary step
then adds the original point. There are at most `R^(2L+2)` charts after
L=ceil(log_2 m) binary levels, and projective degree satisfies

    d_(j+1) <= (2D^2+D)d_j.

Pointwise completeness follows by choosing a nonzero parent chart and
then a nonzero addition chart. Independently branching on two parent
charts is unnecessary. Identically zero composed tuples can be discarded
or retained as harmless zero equations, but must not count as a
nonvanishing chart.

Clear input denominators chart by chart. The logarithm of the full
polynomial coefficient l1 norm is subadditive under products. Substitution
therefore gives a height recurrence
`h_(j+1)<=(2D^2+D)h_j+O_tau(B+log(T+2))`, and an analogous t-degree
recurrence. There are O(log m) levels, so all expanded chart counts,
degrees and logarithmic heights are polynomial in numerical m,B,T.
All expansions use the original fixed projective variables. A claim
based instead on eliminating O(log ell) straight-line-program variables
would not be the proof here.

Impose, for EVERY multiplication chart H, the cross-products
`H_i E_j-H_j E_i`. A nonzero local chart makes these the pullback of the
identity ideal under [ell]. In characteristic zero [ell] is finite etale
of degree ell^n. Together with the actual affine ideal of A this cuts out
the reduced torsion scheme. This is precisely the situation of Pila's
Theorem 2.5 in the retained source.

Use disjoint patches `X_i=1, X_j=0 for j<i`. Since the torsion algebra is
a product of fields, adding these zero-coordinate conditions preserves
radicality and simply selects components. The patch dimensions sum to
ell^n. No saturation at unspecified chart denominators or projective
compactification is being silently substituted for these equations.

## 3. A direct fixed-variable elimination and height proof

There is no need to rely on the report's limiting-Chow-form argument.
The retained Pila Theorems 2.6--2.7 and its section-3 construction give a
simpler explicit route. The imported algebraic membership bound is:

    If f_1,...,f_s have degree <=d in r variables and deg b<=b_0,
    b in (f_1,...,f_s) implies b=sum_j G_j f_j with
    deg G_j <= b_0+(s d)^(2^r).

Here r=N is fixed; t is a coefficient variable in K, not an additional
elimination unknown. For a reduced finite patch with <=L=ell^n geometric
points, monomials of degree <=L span its coordinate algebra. To test all
relations and multiply basis elements by coordinates, take b_0=L+1 and
`H=L+1+(s d)^(2^r)`. Form the coefficient matrix of all
`X^alpha f_j`, `|alpha|<=H`, in monomials of degree <=H+d. Its intersection
with polynomials of degree <=L+1 is EXACTLY the ideal intersection in
that degree, by the displayed bound. Linear algebra selects a monomial
basis of degree <=L and reduces all coordinate-times-basis products.
Empty patches give the zero algebra. This constructs the multiplication
tables and coordinates, rather than assuming a quotient-algebra oracle.

The number of monomials is polynomial in s,d,L because r is fixed. This
is also exactly why the source's fixed embedding dimension matters.
Each input entry is an original coefficient shifted to another monomial
position. After a single charged denominator clearing, the entire
computation is polynomial-size linear algebra with polynomial t-degrees
and coefficient bit lengths. Expanding the cyclotomic power basis, if
necessary, replaces a matrix by one at most ell-1 times larger over
Q(t). The cyclotomic reduction coefficients are explicit and bounded.

Every output entry of exact row reduction can be represented by ratios
of minors of these original bounded matrices. A size-m minor has
t-degree at most m times the entry-degree bound and logarithmic height
`O(m(h+log m+log(support size)))`. Fraction-free elimination prevents an
algorithm from introducing unrelated repeated rational expressions.
These determinant bounds give polynomial coefficient height AND bit
cost, not just Pila's finite-field operation count. In particular the
whole torsion algebra `T_ell=K[A[ell]]`, of dimension ell^n, is paid.

This replaces, rather than silently certifies, the report's more delicate
deformation proof. To retain that alternative, one would additionally
spell out the valuation factorization of the epsilon-initial determinant,
why its divergent-branch factor is a product of nonzero linear forms in
U, and that the coordinate-derivative formula uses that initial
polynomial. A general nonzero polynomial c(U) alone does not justify a
moment-curve search. None of those extra arguments is needed above.

## 4. All frames, open conditions, and bounded representations

The fixed tensor power `R_0=T_ell^(tensor n)` has dimension ell^(n^2).
For every nonzero v in F_ell^n, compute the equality locus
`sum_i v_i P_i=0` with the bounded multiplication/addition atlases and
retain its complement. There are ell^n-1 tests and n is fixed.

In a finite etale algebra an ideal is a direct sum of field components.
Its support idempotent can be obtained from the ideal and annihilator
subspaces by linear algebra; no field splitting is required. These are
exact open-condition exclusions. Compute all idempotents in the ORIGINAL
tensor basis and multiply them there before making one basis change.
Products of polynomially many separately bounded elements have additive
logarithmic-height growth (plus the charged multiplication-table cost).
Repeatedly re-presenting intermediate quotients without such a bound
would be an unjustified height argument.

For evaluating a projective map inside this algebra, partition by the
first nonzero chart/coordinate using the same idempotents and invert only
on its nonzero support. Compute the bounded chart expressions directly;
there is no division by a zero divisor on the whole algebra. This also
pays chart selection when torsion points fall outside a preferred affine
chart. The final algebra R is reduced and has dimension

    D_ell=|GL_n(F_ell)|=product_(i=0)^(n-1)(ell^n-ell^i).

For a basis b_0,...,b_(D_ell-1), the primitive-element trial
`w(s)=sum_j s^j b_j` works. Distinct geometric points give a nonzero
polynomial of degree <=D_ell-1 in s; fewer than D_ell^3 integers are bad
over all pairs. Integers of this size give coefficient bit lengths
O(D_ell log D_ell), still polynomial. A squarefree characteristic
polynomial is the exact separation test. Recover coordinates by linear
algebra in the powers of w.

For integrality, choose delta(t) clearing the entries of the
MULTIPLICATION MATRIX of w, including its structure-constant denominators;
clearing only the displayed coordinate vector of w would not suffice.
Then Y=delta w has a monic characteristic polynomial
`f(t,Y) in Z[zeta_ell][t,Y]` of polynomial degree and height. Its
discriminant is nonzero. Original chart and coordinate denominators remain
explicit and are included in the final displayed open set.

## 5. Component factorization: precise search and bit costs

Factoring f over k(t) is a charged exact operation. Standard deterministic
LLL rational factorization is the arithmetic algorithmic dependency here,
not an irreducibility oracle and not a consequence of Pila's finite-field
count alone. The report's reductions to that dependency can be made
precise as follows.

Let d=deg_Y f and T_f=deg_t f. Choose a small integer t_0 avoiding the
nonzero discriminant by trying at most its degree plus one values. Factor
the squarefree specialization over k. The shift-and-norm reduction is
valid: for `Y -> Y+c zeta_ell`, collisions between roots in distinct
embeddings exclude at most quadratically many integers c; roots within
one embedding are already distinct. A squarefree norm over Q therefore
has polynomial degree and height, and rational factors pull back by
gcds to the factors over k. Cyclotomic degree and coefficient sizes are
included throughout.

For each irreducible specialized factor h_0, Hensel-lift it to precision
`k_0>2dT_f` in t-t_0. It divides exactly one genuine monic irreducible
global factor G. Since f is monic and k[t] is integrally closed, G lies
in k[t,Y]; also `deg_t G<=T_f`, since t-degrees add under multiplication.
Search IN INCREASING Y-DEGREE for a nonzero polynomial h with
`deg_t h<=T_f` divisible by the lifted h_0 modulo `(t-t_0)^k_0`.
These are polynomial-size linear systems. The first solution exists no
later than deg_Y G. Its resultant with G has t-degree <=2dT_f and
vanishes to order >=k_0, so it is identically zero. Therefore G divides
h, and minimal Y-degree makes `gcd(f,h)=G`. Without this increasing-
degree/nonzero condition, the printed search could simply return f.

Initial Sylvester inverses have polynomial-height entries. Hensel
coefficient recursion uses their powers with exponents polynomial in the
lifting order; weighted-degree/majorant bounds give polynomial bit lengths
for the truncated coefficients. The subsequent linear-system solutions
and gcds have the determinant/subresultant bounds already described.
Process the specialized factors against the same original f, and remove
duplicate global factors, rather than recursively multiplying uncontrolled
height bounds. Thus all components can be extracted with the claimed
polynomial envelope. This is an arithmetic addition to the supplied-
atlas source theorem; no fixed-curve height constant has been imported.

## 6. Why any component is correct, and what pairing remains

Let F be the splitting field of A[ell] over K. An ordered basis generates
F, because every torsion point is a prime-field linear combination of
its entries. Hence every connected component of the all-frame scheme
has function field F (up to its displayed K-isomorphism); no special
component is supplied as advice.

The principal polarization is defined over K. Because K contains
mu_ell, arithmetic Galois preserves the actual Weil-pairing form, so its
image is contained in its symplectic group. It contains the promised full
geometric image. The two images are therefore equal. Consequently every
irreducible factor has degree s_ell, the constant field of F is exactly
k, and each component is geometrically connected. A factor of another
degree falsifies the promises or an implementation; a passing degree test
alone is not a proof of the geometric-monodromy promise.

For each M in GL_n(F_ell), transform the universal frame by M and
evaluate the primitive-element expression directly, obtaining Y_M.
The exact test `q(t,Y_M)=0 in K[Y]/q` selects the stabilizer H of the
chosen component. Every passing map `Y -> Y_M` is a field automorphism,
and the preserving matrices give the actual conjugate symplectic group.
All maps are over the SAME k(t); no lcm over separate deck-definition
fields is needed. Output polynomially bounded formulas after reduction
in the power basis. The plane model may be singular, and its
discriminant zeros need not all be genuine branch points of the
normalized cover.

Solving `M^T B M=B` for alternating B gives a one-dimensional invariant
space. A nonzero form is nondegenerate by irreducibility of the natural
module. The ratio of two such forms commutes with all transvections,
hence preserves every line and is scalar. Symplectic Gram--Schmidt and
the standard transvections along e_i,f_i and their listed two-coordinate
sums provide O(a^2) generators; powers supply all F_ell parameters
because ell is prime. Their elementary symplectic row operations generate
the group. One can also check the subgroup against the enumerated H,
without composing successively enlarged rational maps.

This recovers the actual pairing matrix only up to `E=cB`. Therefore the
cover and group action are explicitly presented, but a universal frame
satisfying `e_ell(P_i,P_j)=zeta_ell^(J_ij)` has NOT been output. One
certified value with B_ij nonzero determines c by a table of ell roots
of unity and then pays normalization. No polynomial pairing circuit was
assumed. This marking scalar is distinct from the unresolved genuine
arithmetic coefficient-module/Frobenius linearization; this construction
does not return that Frobenius matrix.

## 7. Boundaries and decisive falsifiers

The retained Pila Theorem A explicitly assumes the projective variety
and addition law. Its Theorem B is a fixed-curve precomputation statement,
and its accompanying text identifies genus-uniform Jacobian/addition
construction as a further task. It does not pay the native atlas here.
The fixed-variable linear systems plus the explicit arithmetic bounds
above do pay the supplied-atlas theorem uniformly in its displayed data.

Essential falsifiers are a common zero of all alleged charts; a
nonradical torsion algebra; dimension other than ell^n or |GL_n| at the
two stages; an incorrect component degree; a failed deck identity; or
a degree/height recurrence outside the fixed-type polynomial envelope.
For example, replacing a true transverse equation z=0 by z^2=0 gives
the same geometric variety but can retain nilpotents in the alleged
torsion algebra. Radical input ideals are a substantive hypothesis.

Still unpaid: native radical complete atlas construction and its uniform
height/type bounds; the required geometric-monodromy and transvection-
inertia promises for the downstream native-module theorem; a normalized
universal frame if requested; genuine arithmetic coefficient action;
and the separate reduction/lifting/height-recovery tasks. Full symplectic
monodromy alone does not imply that every branch inertia is a transvection.
No full native surface algorithm, fixed-X uniformity claim, or statement
about the parent's separate all-cyclotomic-component task follows.
