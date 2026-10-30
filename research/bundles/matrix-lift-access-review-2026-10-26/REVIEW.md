# Independent Matrix-Lift and Arithmetic-Access Review

Date: 2026-10-26. All review outputs are confined to this directory. Parent
sources were read, imported with bytecode disabled, and hash-checked; none
were edited. No Git, UI, Desktop-project changes, or subagents were used.
The parent's multi-list effective mod-2 coset search and length budget are
outside this review.

## Verdict

**ACCEPT the geometric lift under the explicit complete-AG promise, including
both equalities d=2g+1 and m=2d+4. REVISE the implementation-scope and access
ledger. REJECT any stronger inference to an implemented or uniformly
polynomial native solver.**

No counterexample was found inside the promised range. There is an explicit
counterexample to lowering the length bound by one: on an elliptic curve over
F_17, m=9=2d+3 gives quotient dimension 5 instead of 4. Thus the endpoint is
substantive, not merely a conservative strictness convention.

The most important access correction is positive: recovering the quadratic
ideal does supply fixed-degree graded multiplication, and that supplies
ordinary represented-divisor and Jacobian group operations. It does not
supply the zeta polynomial or a basis of rational 2-torsion. Those are distinct
claims, not one undifferentiated "Jacobian access" assumption.

## 1. Exact Input Contract

The theorem needs a smooth, projective, geometrically integral curve X/F_q,
of genus g, a rational divisor G of degree d, and an ordered reduced divisor
D=P_1+...+P_m of distinct F_q-rational points disjoint from supp(G). It needs

    rowspace(B) = u * ev_D H^0(X,O(G)),  u in (F_q^*)^m,
    d >= 2g+1,  m >= 2d+4.

"Complete" means the FULL section space, not a subcode, a subfield subcode,
or a trace code. It does not mean D contains every rational point of X.
The rows of B must be independent. Calling B a native parity matrix is fine,
but the geometric promise concerns its ROW SPACE, not merely its kernel.

Arbitrary generator-row changes, unknown nonzero coordinate multipliers, and
an ordering of the evaluation points are allowed. Repeated points, jets,
singular curves, and generic matrices with matching ranks are not covered.
The dimension checks in the helper are necessary checks, not recognition of
this promise.

The mathematical construction works over finite fields generally and includes
g=0. In contrast, `point_lift.py:35-47` accepts only canonical integer entries
over an odd prime below 2^63, and expressly rejects g=0. This is a documented
scope mismatch to correct, not a failure on the actual genus-41 prime-field
fixture. The independent genus-zero control reproduces the rejection.

## 2. Quotient Identity and Equality Cases

First take u=1, select P in D, and put D'=D-P and n=m-1. Shortening BEFORE
puncturing computes C(G-P); simply puncturing does not. All codes below are
evaluated on D'. Completeness and normal generation give

    Vminus=C(G-P),  V0=C(G),  W=V0*V0=C(2G).

[Couvreur, Marquez-Corbella and Pellikaan, Theorem 5 and Proposition 7](https://arxiv.org/html/1401.6025v3#S2.SS2)
use the inclusive hypotheses deg(F)>=2g and deg(E)<=n-3 for
`C(E-F)=(C(F)*C(E)^perp)^perp`. Substituting E=2G and F=G-P gives exactly

    (Vminus * W^perp)^perp = C(G+P).

At the simultaneous endpoints, deg(F)=2g and deg(E)=n-3. In the duality
argument the complementary divisor has degree

    deg(K + D' - 2G) = 2g-2+n-2d = 2g+1.

Thus the product theorem has degrees 2g and 2g+1, not two possibly exceptional
degree-2g bundles. Supports are disjoint from D': the fact that F has
coefficient -1 at P is harmless because P was removed. No effectiveness
assumption on F is needed.

Riemann-Roch and evaluation injectivity give dimensions k-1, k, k+1. The
inferred formulas d=w-k and g=w-2k+1 are correct under this promise, since
k=d+1-g and w=2d+1-g. None of this uses an invalid degree-3G vanishing
argument on too few points.

### Column scaling

For the punctured multiplier vector u, `(u*C)^perp=u^(-1)*C^perp`. Therefore

    ((u*C(G-P)) * (u^2*C(2G))^perp)^perp
      = (u^(-1) * (C(G-P)*C(2G)^perp))^perp
      = u*C(G+P).

The quotient has weight u, not u^(-1) or u^2. The selected coordinate's
nonzero weight does not change the shortening kernel. The recovered columns
are the correct projective points even without factoring out the unknown
weights. An adapted extension row need not scale identically across two runs;
the whole recovered spaces do. Tests should compare spaces, not extension-row
bytes.

### Why one fewer evaluation point can fail

The independent control uses `y^2=x^3+2x+2` over F_17, G=3O, and the nine
points, in order,

    (3,16), (6,14), (5,1), (10,11), (16,4),
    (6,3), (7,6), (0,11), (7,11).

Their elliptic group sum is O, hence D is linearly equivalent to 9O. Select
the first point as P. Then D'-6O is equivalent to 3O-P. The two degree-two
bundles in the dual product coincide; the multiplication span has dimension
3 rather than 4. Direct independent elimination gives quotient dimension 5,
whereas H^0(3O+P) has dimension 4. The helper correctly rejects this input
as out of range. This is not a counterexample to LIFT.md.

## 3. Recovering P, H-P, and the Native Frame

Write L=O(G+P), e=d+1, and let H denote its hyperplane class. Evaluation on
D' is injective, so every computed row has a unique section interpretation.
Keeping the original k rows and adjoining one genuinely new row gives a
basis `(s_1,...,s_k,t)` of H^0(L). The original section space is precisely
H^0(L(-P)). In the exact sequence at P it is the kernel of evaluation.
Consequently the image of P is

    [0:...:0:1].

The 1 is a choice of fiber frame, not a recovered numerical residue. Since
the new section is outside H^0(L(-P)), its value in the L-fiber is nonzero.
The assertion is invariant under adding any original section to t.

More strongly, the image of the original sections has base divisor EXACTLY P:
O(G) is globally generated, so there are no additional common zeros and the
common multiplicity at P is one. Hence

    O_X(H-P) = O_X(G)

as a line-bundle class over F_q. This is not just an equality of degrees, not
an unspecified twist, and not a choice of a random class in Pic^d. It does
not recover a unique original divisor representative G: equivalent divisors
and adjusted trivializations describe the same marked code.

There is also a concrete first-order normalization check. In the chart t!=0,
let z_i=s_i/t. The tangent vector `(dz_i(P))` is proportional to the original
selected column B_P. Choose j with B_jP!=0; then z_j is a local parameter
and `(z_i/z_j)(P)=B_iP/B_jP`. Multiplying this local evaluation frame by
B_jP reproduces B_P exactly. On D' the first k adapted rows already are the
original matrix entries. Unknown historical multipliers therefore need not
be separately identified merely to retain the original evaluation map on
H^0(H-P).

This tangent/local-parameter construction is consistent with the explicit
method in [Marquez-Corbella et al., corrected 2014 paper, Section 4.2](https://ruudp.win.tue.nl/paper/66.pdf).
An arbitrary future function-field or divisor backend must preserve these
frames, row identifications and coordinate order. Replacing the original
matrix by projectively normalized columns can change Bz=s and its coordinate
constraints. An isomorphism of divisor classes alone is not an equality of
native evaluation matrices.

## 4. Explicit Quadrics and Truncated Algebra

At the length endpoint,

    n=2d+3=2e+1 > 2e.

A quadratic relation detected on D' is a section of L^2 vanishing at more
than its degree, hence is globally zero. The matrix kernel is exactly I_2(X).
Because e>=2g+2, the homogeneous ideal is generated by these quadrics, not
merely set-theoretically cut out by them. The degree endpoint is recalled in
[Brown-Erman, Theorem 1.1 and its p=1 discussion](https://www.cambridge.org/core/journals/compositio-mathematica/article/linear-syzygies-of-curves-in-weighted-projective-space/C7B17880FDA1605421F0E5297B3E64BA)
and used over finite fields in the [2014 AG-reconstruction paper, Sections
3-4](https://ruudp.win.tue.nl/paper/66.pdf). This is the usual complete,
high-degree embedding theorem; no characteristic-zero-only inference from
numerical examples is needed. Kernel construction and ideal generation
descend from an algebraic closure to F_q by field extension.

Let N=k+1 and S=F_q[X_1,...,X_N]. Here is an explicit construction, rather
than an appeal to a general Groebner solver:

1. Compute a basis Q of I_2 by the quadratic evaluation kernel.
2. For each fixed j<=h, form the coefficient rows of all `M*q`, with q in Q
   and M a degree-(j-2) monomial. Their span is exactly I_j.
3. Row-reduce to choose a basis of R_j=S_j/I_j and a linear reduction map.
4. Multiply basis polynomial representatives and reduce in R_(a+b), for
   a+b<=h. Retain the reductions and labels, not only Hilbert dimensions.

Normal generation identifies R_j with H^0(X,L^j), so this constructs the
entire truncated graded multiplication contract. Degree-j monomial count is
`binomial(N+j-1,j)`. For fixed h=7 this is polynomial in matrix size and
log(q), although a naive dense construction can require O(N^21) field
operations and O(N^14) field storage. These are deliberately coarse upper
bounds, not a recommendation to allocate such matrices.

For the supplied N=44 instance, S_7 already has 99,884,400 monomials, whereas
R_7 has dimension 7*84+1-41=548. Practical implementation needs compressed
quotient bases or sparse/incremental relations. The helper currently emits
neither quadrics nor these multiplication tables; reporting 862 quadratic
relations is not the same as exporting them.

Do NOT construct R_3,...,R_7 by simply evaluating degree-j monomials on D'.
Evaluation ceases to be injective. The elliptic control demonstrates this:
the genuine cubic piece has dimension 12 while its nine-point evaluation
has rank 9. Using that sample kernel would add three false relations.

## 5. What Arithmetic This Actually Supplies

Put `R_a=H^0(aH)` and `W_(a,A)=H^0(aH-A)` for an effective represented
divisor A. The following deductions concern represented objects, not finding
an unknown divisor satisfying an external search condition.

### Fixed-degree linear algebra

Known rational points give W_(a,P_i) by evaluation kernels. A nonzero h in
R_1 gives an effective hyperplane divisor A with W_(2,A)=h*R_1. The zero
Jacobian class is therefore available without splitting A into primes.
Given valid divisor subspaces, products give

    W_(a,A) * W_(b,B) = W_(a+b,A+B)

when both residual line-bundle degrees are at least 2g+1. Colon computations
are simultaneous linear containment equations; their geometric use requires
the dividing section system to be globally generated. Retain these degree
conditions for overlaps and multiplicities rather than assuming every
subspace is a divisor.

In the medium model, degree-e effective divisors A represent the class H-A
by W_(2,A). Zero testing solves `{s in R_1: s*R_1 subset W_(2,A)}`. For
addflip, multiply W_(2,A),W_(2,B), divide by R_1, choose a nonzero section
in H^0(3H-A-B), and divide its R_2-multiples by that section system. The
residual divisor C represents `-(H-A)-(H-B)`. All multiplications have total
degree at most 5. This supplies negation, addition, subtraction, equality,
and scalar multiplication by an addition chain. See [Khuri-Makdisi,
Section 5, Proposition/Algorithm 5.1](https://arxiv.org/html/math/0105182#S5).

No canonical divisor or zeta data are required for these group operations.
Complexity is polynomial in e and log(q); the familiar genus-only bounds
assume e=O(g+1). For the general input promise, e=O(m) is sufficient, but
one must not silently replace e by g.

For a represented A with deg(A)<=a*e-2g+1, and BOTH W_(a,A) and W_(2a,A)
available, restriction spaces are explicit quotients `R_a/W_(a,A)` and
`R_(2a)/W_(2a,A)`. Their induced product is a perfect pairing between
invertible modules over O_A.

Here is a direct linear-algebra variant, derived in this review. Write that
pairing as mu:M x N -> T. Solve for triples of linear endomorphisms (U,V,W):

    mu(Ux,y) = mu(x,Vy) = W mu(x,y)   for all basis pairs (x,y).

After abstractly identifying M,N,T with the rank-one free O_A-module O_A,
these equations say U(x)y=xV(y)=W(xy). Setting x or y to 1 proves that
U,V,W are all multiplication by the same element of O_A. Thus projection
to U gives exactly the regular algebra O_A, and composing U-matrices gives
its multiplication table. This proof does not require finding those abstract
identifications or a random module generator. For s=deg(A) it uses 3s^2
unknowns and at most 2s^3 scalar linear equations. Decomposing the resulting
algebra, or choosing useful module trivializations, is a separate step.

### Bruin input checklist

The following source contracts are from [Bruin, Computing in Picard groups
of projective curves over finite fields](https://arxiv.org/html/1003.2563).
Here h means the required truncation degree.

| Primitive | Contract beyond the recovered algebra |
|---|---|
| Section 2.1 | L very ample, deg(L)>=2g+1; graded bases and multiplication, not ranks |
| Algorithms 2.10, 2.11 | h=2 zero test; h=5 addflip; represented valid classes |
| Algorithm 2.12 | h=4 normalization; rational basepoint and its divisor subspace |
| Algorithm 2.4 | h=2a; deg(A)<=ae-2g+1; both divisor subspaces; primary decomposition |
| Algorithm 3.1 | Frobenius: coefficient q-th powers over an explicit finite extension |
| Algorithm 3.2 | h=2a+2; prime degree r<=ae-2g; nonempty degree-r place set; factorization; no zeta |
| Algorithm 3.5 / Section 3.5 | Uniform divisors/Jacobian sampling requires L_X(T); Jacobian sampling uses h=6 |
| Algorithm 3.8 | h=7; supplied torsion x and class y; nx=0, n divides q-1; no zeta input |
| Algorithms 3.10, 3.11 | Relation finding uses uniform samples; torsion discovery additionally takes Frobenius characteristic polynomial chi |

Thus h=7 is sufficient for the displayed bounded-degree routines, NOT for
arbitrary-degree prime sampling. For a=2 the prime-degree ceiling is 2e-2g;
for larger r the required a, and hence truncation, increases.

### What is still charged

Finite-algebra primary decomposition, residue-field construction and unit
choices are not plain Gaussian elimination. Over explicitly represented
finite fields they have randomized polynomial algorithms (Bruin Sections
1.1-1.2), so they are backend work rather than an unexplained exponential
barrier. Field extensions and any descent to the native field must be
included. The current nmod implementation cannot perform these extensions.

A bounded-degree line-bundle computation is not automatically a map from a
newly obtained divisor or differential into the native coordinate convention.
In particular a future auxiliary construction using K-3G+D must supply an
actual representation of the canonical/differential class and the required
section isomorphisms, with evaluation/residue normalization. Neither the
reviewed helper nor the construction above implements that adapter. Ordinary
group operations must not be confused with computing this input, or with
solving an arbitrary Riemann-Roch problem from an unspecified divisor encoding.

Zeta remains an independent input to the cited exact uniform sampler and
torsion-discovery route. The verified fixture has p=100003, g=41, d=83 and
m=176; no zeta computation for it occurs in the reviewed files. A theorem
polynomial in log(q) for FIXED geometric complexity is not uniform polynomial
in both growing genus and log(q). In particular [Pila's Theorem A](https://people.maths.ox.ac.uk/pila/Frobenius.pdf)
has an exponent and constants depending on the abelian-variety presentation;
it does not close this gap from our curve quadrics.

For rational 2-torsion in odd characteristic, roots of unity and their
discrete logarithms are trivial (+1 and -1), but finding a full torsion basis
is not. The multiplicity of T-1 in chi modulo 2 is not by itself r_2:
the identity and a nontrivial unipotent Jordan block have the same
characteristic polynomial and different fixed-space dimensions. One needs
the Frobenius action on the appropriate torsion, not only eigenvalue
multiplicity. Even successful torsion coordinates would not construct the
short effective divisor sought by the separate auxiliary search.

## 6. Independent Verification

Reproduction from this directory:

    .venv/bin/python -B independent_controls.py
    .venv/bin/python -B -m pytest -q -p no:cacheprovider \
      ../matrix-geometry-lift-2026-10-26/test_point_lift.py \
      --rootdir=/Users/jaspersands/Developer/qsearch-research-work/matrix-lift-access-review-2026-10-26

Environment: Python 3.13, python-flint 0.9.0, pytest 9.1.1, installed only in
the review directory's .venv; pip cache is local here too.

Results:

- Parent tests: **10 passed in 6.97s**. Their original fixtures were replayed
  read-only, without pytest cache or Python bytecode writes.
- **48 exact-space comparisons** at both equalities on independent genus-1
  and genus-2 hyperelliptic fixtures, at every selected non-ramified point,
  with and without nonzero column scaling plus a row-basis change.
- Oracle basis for G=(2g+1)O: `1,x,...,x^g,y`; the extra section is
  `(y+y(P))/(x-x(P))`. Its removable value at -P is evaluated by the derivative.
  Thus the expected lift is independently known, not inferred from ranks.
- For the elliptic quartic: both recovered quadrics checked on all 19 rational
  curve points, including held-out points and O; P tangent matches the native
  column; quotient Hilbert dimensions through degree 7 are
  `1,4,8,12,16,20,24,28`.
- The one-below-length counterexample and genus-zero helper exclusion are
  reproduced. Finite controls do not certify the complete-AG promise.
- The compatible-endomorphism algebra recovery passes independent-basis
  controls for F_2^3 and F_17[epsilon]/(epsilon^3), including dimension,
  identity, commutativity and multiplicative closure. These exercise both
  a split small-field algebra and a nonreduced divisor algebra.

`control_results.json` contains exact data and SHA-256 hashes of all four
audited files. The hashes were unchanged across the control run. No full
genus-41 graded backend, canonical-class adapter, zeta polynomial, torsion
basis, or native witness was produced.

## 7. Sharp Next Step

Build one **matrix-to-medium-model adapter**, not another search framework.
On the frozen native matrix, emit I_2, compressed R_0,...,R_5 and their
multiplication maps; retain the marked points, H-P, the inclusion of every
original row, and the selected-point tangent normalization. Verify Hilbert
dimensions, multiplication associativity, zero/addflip identities, and an
EXACT original-matrix evaluation round trip, including the punctured point.
Do not allocate the naive 99-million-monomial degree-7 basis.

Only then extend to h=7 and finite-algebra factorization as needed. The next
source-specific go/no-go input for the uniform-sampling/torsion route is a
certified chi for this actual family with a resource bound in BOTH g and
log(p), or a substitute access construction with its distribution proved.
Track the canonical/differential-to-native adapter separately if the
auxiliary certificate requires it. None of these steps settles the parent's
effective-coset search or length budget, which were deliberately not audited.
