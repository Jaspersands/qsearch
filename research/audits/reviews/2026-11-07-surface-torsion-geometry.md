# Surface torsion covers: constructive geometry and source review

2026-11-07. Read STATE/TRAPS, the reselection proposal as UNVERIFIED, and the
retained actual surface-P1, Pila, Khuri-Makdisi and Kedlaya texts. Interpreter
`/opt/anaconda3/bin/python`; no network/Git/API, implementation or tests.

**Disposition:** the fixed-genus geometry can be made constructive with the
canonical-divisor/chart compiler below. Adopt cubic-Veronese pencils as the
DEFAULT: genus19, base36, nodes132. The arithmetic/t-degree bounds and the
constant-field descent are essential parts of the argument, not consequences
of a cover-degree bound alone. This closes a WRITTEN geometry reduction with
the specified safe-characteristic/fallback convention. It does NOT certify
the separately reviewed modular representation/twisted-trace extraction or
the whole P2 algorithm, novelty, separation or execution.

## What the actual sources supply

All following paths are under `audits/sources/`.

- `surface_torsion_selection/surface_p1.txt`130–149 explicitly EXCLUDES P2;
  Theorems1.3/1.4 at236–254 compute P1. Thus no native P2 subsumption follows.
  Its Algorithm3,902–928, pays a Lefschetz pencil AFTER a cubic Veronese;
  Proposition4.5,883–888, does not itself guarantee the original quartic's
  genus-three plane pencil. Use the supplied Veronese fallback instead.
- `pila_frobenius.txt`30–35/TheoremA assumes an explicit projective abelian
  model AND addition atlas. Lines54–61 and140–150 expressly leave uniform
  Jacobian construction open there. Do not cite TheoremB as that constructor.
  However its atlas-composition bounds408–454, Propositions3.1/3.2, and its
  any-field ideal-membership bound343–355 are usable once fixed charts exist.
- `khuri_makdisi_divisors.txt`82–108 explains the bounded linear-algebra
  representation and its required section-multiplication input. It explicitly
  uses NONUNIQUE divisor representatives (149–160,880–893). Membership is
  Theorem/Algorithm3.14 at815–851, group addition4.5 at1024–1030, equality4.1
  at895–920, and Riemann-Roch5.5 at1252–1275. These work over a field, not
  only finite fields. They alone do not make a finite torsion coordinate scheme.
- `legendre_prf/kedlaya_zeta_0411623.txt`52–65 proves quantum curve zeta in
  polynomial genus/log-field size, for an EXPLICIT smooth projective
  GEOMETRICALLY IRREDUCIBLE curve. Its input protocol281–309 allows a singular
  plane model and explicitly imports polynomial normalization/resolution
  without a common field rationalizing every singular point. Neither this
  theorem nor the surface paper constructs our torsion covers for free.
- `surface_torsion_selection/kozen_resolution.txt`89–101 specifies the actual
  output: exceptional places, places above them, ramification indices, local
  parameters and birational rational reparametrizations. Lines204–234 give
  the place/parameter tree;366–424 give passive factorization;488–500 bound
  its depth, splits and extension-degree products. The polynomial-BIT claim
  at14–24 applies over ANY finite field and avoids explicit common high-degree
  extensions. This is stronger than a black-box genus calculation.

## Pencil, point and fixed-size section data

For a quartic K3, the source-paid cubic pencil has class3H. Its base scheme
has degree36, genus is `1+(3H)^2/2=19`, and its nodal-fiber count is
`(24+36)-2(2-2*19)=132`. Geometric basepoints need not all be rational.

Every reduced singular Lefschetz fiber is geometrically irreducible. Otherwise
connectedness and its single ordinary node give `D=A+B`, `A.B=1`. Put
`a=H.A`, choosing the smaller positive degree, so1<=a<=6. Then
`A^2=3a-1`, whereas Hodge index gives `A^2<=a^2/4`, an impossibility in
that interval. A nonreduced component is incompatible with having only an
ordinary node. This proves irreducibility rather than adding a promise.

For the simplest uniform Jacobian input, choose the pencil through a known
Fp-rational surface point P0. Such points can be found at large p by random
line intersection and quartic factoring: a noncontained line contributes at
most four points and expected incidence is bounded below. The Hilbert scheme
of lines on a smooth quartic is zero-dimensional: a line's normal bundle in
the K3 is O(-2), with no tangent deformations. Its fixed-degree Grassmannian
equations uniformly bound its size. Thus contained lines contribute only
O(p^-3) to expected incidence, while total expected incidence is
`#X(Fp)/(p^2+1)=1+O(1/p)`; success has a constant lower bound. Reject contained
lines explicitly. Selecting a root gives surface points with bounded bias.
For selecting a good pointed pencil use the
fixed-degree incidence variety of `(P0,F,G)` with F(P0)=G(P0)=0. It is an
irreducible bundle over X; its good-pencil locus is nonempty open, because
the source's good pencils have basepoints. Its bad loci have uniformly
bounded degrees, independent of p. Fixed-degree point sampling/Lang-Weil
and exact nodal/transversality verification pay a capped randomized search.
This avoids assuming a rational point on the generic fiber without payment.

Let `k0=Fp(t)`, `g=19`, `d0=2g+1=39`, `D0=d0 P0`, `L=O_C(3D0)` and
`N=deg L=117`. All these numerical parameters are ABSOLUTE CONSTANTS.
The generic fiber is the smooth complete intersection of degrees4 and3 in P3,
with coefficients of bounded t-degree. The finite input spaces
`H0(L),H0(2L),H0(3L)` and their multiplication maps can be built uniformly:
choose a hyperplane section `H0=P0+B` transverse at P0. A function in
`H0(s P0)` is a section of `O_C(s H0)` vanishing on `s B`, divided by the
hyperplane equation to power s. For s<=351, these spaces are kernels of
fixed-size linear systems, computed in the fixed-degree complete-intersection
coordinate ring, with vanishing imposed by the corresponding Cartier-ideal
powers. Fixed-variable ideal quotients/elimination suffice. Matrix sizes,
degrees and rational-function t-heights are bounded constants. Cramer's rule
therefore bounds all preprocessing t-heights independently of p. No torsion,
class-group, rational-point or Riemann-Roch oracle is supplied as advice.

## A unique-representative bounded-variable Jacobian atlas

The nonuniqueness in Khuri-Makdisi must be removed BEFORE torsion elimination.
For every class there is a unique `E-mP0`, with0<=m<=g minimal, E effective,
`h0(E)=1` and P0 absent from E. This is the actual reduced-form lemma in
`surface_p1.txt`377–384: minimality makes h0 one, and uniqueness follows from
that one-dimensional space. Conversely these conditions force minimality.

Encode it by the degree-d0 divisor `D=E+(d0-m)P0` and its Grassmannian
subspace `W_D=H0(L-D)`. On fixed row-echelon charts impose:
membership as a degree39 divisor; `D>=(d0-m)P0` but not the next multiple;
and `h0(D-(d0-m)P0)=1`. The first is Khuri-Makdisi3.14; containment is
subspace containment. For the last, apply5.5 with
`D1=D+d0P0` of degree78 and `D2=(2d0-m)P0` of degree59..78.
These satisfy its hypotheses EXACTLY: `N-2g-1=78`.

The same calculation canonicalizes the output of each group addition.
Choose the smallest m with nonzero Riemann-Roch space, obtain its unique
effective E by5.5, then use
`W_Dcanonical=W_E intersect W_((d0-m)P0)`; the supports are disjoint.
Theorem4.5 plus this bounded canonicalization gives a finite rational
addition atlas. Every choice of a nonzero section or pivot is made by a fixed
ordered rule, and all its possible rank/minor charts are included. g, matrix
sizes, variable count, chart count and initial chart degrees are CONSTANT.
The atlas is a constructible stratified presentation, not a claimed new
projective theta model. Canonical Abel strata give one geometric point per
Jacobian class, which is the property needed by torsion elimination.

For [ell], use O(log ell) doubling/addition steps. Constant branching per
step gives ell^O(1) chart paths; rational numerator, denominator and t-degree
grow by a fixed multiplicative constant per step, hence are ell^O(1).
Flatten each path to rational formulas in the ORIGINAL fixed coordinates.
Do NOT eliminate a growing log-ell list of intermediate circuit variables.
Ordered pivot decisions make paths disjoint. The identity conditions and
path-validity minors define finite constructible torsion cells; one inverse
variable handles each product of required nonzero minors. There remain only
a fixed number of elimination variables, so Pila's any-field bound gives
polynomial-size Macaulay linear systems over Fp(t). Their solutions and
multiplication tables have polynomial t-height by determinant bounds.

Take the reduced coordinate algebras of these cells and their disjoint
product A. It has rank exactly ell^(2g)=ell^38 and is étale for ell!=p.
A completely conservative characteristic guard is available: let M(ell) be
the explicit polynomial bound on unreduced cell-algebra dimensions from
the fixed-variable elimination bound, and require p>2M(ell)^2. Since all
geometric residue fields here are separable, the trace-pairing kernel is
then exactly the nilradical (local multiplicities are<p); quotienting removes
any nonradical defining equations by linear algebra. This avoids an unpaid
general radical oracle. If that guard fails for an ell=O(log p), brute-force
surface counting over the finitely many required extension degrees costs
polynomial(log p), because p is then itself bounded by a FIXED polynomial
in log p. The exponent is huge but fixed. This stronger safe-characteristic
guard does not change the complexity claim.

## Full arithmetic frame torsor, degrees and t-heights

Form `A^tensor38` EXPLICITLY, rank ell^1444. For every nonzero vector in
Fell^38 (there are ell^38-1), evaluate its linear combination of the universal
38 torsion points, and retain the locus where it is nonzero. Evaluate each
relation atlas separately, not all possible chart branches simultaneously.
In a finite étale algebra, a denominator's zero/nonzero support is found by
the kernel/image of its multiplication matrix; the associated idempotent
allows inversion only on its nonzero support. Keep the ambient algebra fixed.
For height control flatten each rational relation map BEFORE evaluation, so
only its final expanded denominators need algebra inverses. Repeated nested
matrix inversions are not used as a degree-growth bound. Multiply the final
independence idempotents, using common coordinate denominators.

The resulting algebra is the full GL38(Fell) FRAME TORSOR: possibly
disconnected, degree `|GL38(Fell)|<ell^1444`, with all deck actions explicitly
obtained by those same linear-combination formulas. It is defined over Fp,
so full arithmetic monodromy is retained automatically. No geometric-only
group, unknown torsion basis, exact monodromy or Frobenius matrix is advice.
The fixed-coordinate formulas, polynomial-degree substitutions and one-shot
finite-algebra linear solves bound all multiplication/deck-map t-heights by
ell^O(1), not just their ranks. Normalizing extends the generic cover over U;
coordinate poles do not become genuine ramification. Semistable nodal
Picard-Lefschetz monodromy is tame for ell!=p; p>|GL38| is also a sufficient
safe fallback. Riemann-Hurwitz bounds every geometric compact component genus
by `1+65|GL38|`. Twists retain the same genus/branch bounds.

## Components, twists and actual curve inputs

For h in GL38, over Fp^r let m=ord(h)<=|GL38|. Tensor the frame algebra
with Fp^(r m), and take the fixed algebra of h combined with the generator
of this CONSTANT extension's Galois group. This is semilinear descent,
implemented as ordinary Fp^r(t)-linear algebra on rank<=|GL38|*m.
Its invariant algebra has the desired rank and explicitly computed table.
There is no averaging/division by the group order in Fell, and no supplied
Frobenius on a hidden function field. All t-heights remain polynomial by
the linear-system determinant bounds.

Choose primitive elements and plane equations by finite-algebra Krylov tests,
factor their dense finite-field polynomial equations, and normalize using
the polynomial curve algorithms imported in Kedlaya281–309. Degrees in both
plane variables are polynomial in ell. For each arithmetic component,
`H0(O)` of its smooth projective normalization computes its FULL constant
field. Rebase over that field before a Kedlaya call, so its curve really is
geometrically irreducible. Do not assert that an Fp-irreducible equation
already has that property. Genus-zero components are handled directly;
normalization/Riemann-Roch or a low-degree plane-model conversion pays the
explicit input protocol in all other cases.

No exponential common splitting field is needed. Each connected arithmetic
component of the original frame torsor is Galois of degree dividing |GL38|.
Its constant degrees divide |GL38|, and residue degrees above a closed bad
point of degree d<=132 divide d*|GL38|. Thus a common boundary/constant
extension of degree `lcm(1,...,132)*|GL38|` suffices. Twisting uses commuting
deck/Frobenius permutations, so a polynomial multiple suffices there too.
Alternatively retain orbit algebras throughout. Never replace this torsor
argument by the lcm of arbitrary degree-D polynomial factor degrees.
All finite-field arithmetic costs polynomial in extension DEGREE and log p;
one factors polynomials, rather than enumerating those enormous fields.

For explicit boundary permutations, apply Kozen's rational local-parameter
charts to each connected plane model. A terminal chart has a regular local
parameter and one coordinate solved by a nonsingular implicit equation.
Evaluate each deck-map rational function there. A nonzero numerator or
denominator has local zero/pole order bounded by the model/function degrees
via Bezout; functions identically zero are tested in the explicit function
algebra. Thus a polynomially bounded local expansion computes valuations
and leading residues. Compose the place constraints with deck maps to match
their target places; residue Frobenius is ordinary finite-field powering.
No arbitrary-depth Puiseux expansion, unspecified precision or free local
Frobenius/decomposition group is required. Kozen's passive factors may be
kept as orbit algebras or split in the torsor-paid boundary extension.

## Arithmetic representation and bad fibers

The desired sheaf is `V=R1 pi_* Fell`, canonically dual to raw J[ell].
An arithmetic element sigma acts by `rho_J(sigma)^(-T)`. Local zeta uses
geometric Frobenius sigma^(-1), giving `rho_J(sigma)^T` and the familiar
torsion-arithmetic characteristic polynomial. This avoids choosing a
cyclotomic generator. The surface paper624–628 instead uses mu_ell and
omits twists after such a choice; that simplification cannot silently be
copied into arithmetic Fp(t) data.

At an irreducible ordinary node, the integral nearby-cycle sequence has
`H1(special)->H1(generic)->Zell(-1)->H2(special)->H2(generic)`.
The last map is an isomorphism because there is one geometric component.
The evaluation on the nonseparating vanishing cycle is therefore primitive
and surjective. Picard-Lefschetz gives `N=delta tensor eval_delta`, with
primitive delta. Reduction modulo EVERY ell!=p gives the same kernel as
inertia invariants, not just a characteristic-zero invariant-cycles claim.
This matches the paper's actual mod-ell formula641–644. Proper base change
therefore gives `R1 pi_* Fell=j_*V`; R0 is constant and R2 is Fell(-1).
The assertions are arithmetic-equivariant. Inertia fixed spaces are common
kernels, computed by linear algebra; no division by |GL38| is needed.

Euler factors/Leray then give, without spectral-sequence degeneration,
`zeta(tilde X)=zeta(P1,T) zeta(P1,pT)/L(P1,j_*V)` and
`P2(X,T) P_base(pT)=(1-pT)^2 L(P1,j_*V)`.
The base scheme is the degree36 scheme with its computable Frobenius
permutation, not36 assumed rational points. Boundary decomposition/inertia
and Frobenius permutations are computed in the normalized cover and the
polynomial-degree residue/constant fields just described. Extracting the
L-function from the twists, including its modular representation identities,
remains the separate core review; this geometry review does not replace it.

Every construction has polynomial size in ell and log p, with finite capped
randomized field/pencil/model routines. Kedlaya calls can receive individual
error budgets summing to eta, with standard bounded-error repetition. For
ell=O(log p), all genera, model degrees, extension degrees and call counts
are polynomial(log p). These are extremely large sufficient exponents,
not practical costs or a proof of a quantum/classical separation.
