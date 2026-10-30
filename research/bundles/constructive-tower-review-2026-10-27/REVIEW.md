# Independent Review: Constructive Dyadic Tower

Date: 2026-10-27. Scope: mathematical composition, representations and cost,
not implementation, a new hardness claim, or a matrix-only recovery theorem.

## Verdict

**ACCEPT at theorem level, with the bounded-representation construction below
included in the claim.** There is a classical Las Vegas expected
output-polynomial route, at fixed q = p = 100003, to a nested chain with a
level of every degree 2^j in the specified maximal unramified S-split pro-2
extension. At every requested level e >= 8 it can additionally output an
exactly uniform good degree-(2g+1) prime G and the complete evaluation matrix
whose Schur cube has full rank.

This is not acceptance of an unspecified arithmetic oracle. SOURCE.md,
Section 3, explicitly leaves representation obligations open; Sections 4-6
of this review supply a sufficient classical construction and size invariant.
Merely citing a normalization routine, or merely observing that a small plane
model exists, would not close those obligations. The remaining gap is an
implementation/verification gap for a particular backend, not a missing
class-group algorithm or a mathematical obstruction established by this audit.

There is **no BLOCK finding**. The initial PRIME_CLASS.md had an off-by-one
in the section dimension, and conflicting wording about accepted-prime
uniformity. Both were corrected by the parent during this review, before
the saved snapshot. The corrected mathematical claims survive.

Precisely, "all dyadic levels" means one indefinitely extendible chain,
not enumeration of all subfields, all degree-2^j covers, or a chain proved
cofinal in the entire maximal extension. The curve construction starts at
e = 1; the advertised code parameters and probability statement here are
for the tail e >= 8. No native higher level, order, torsion basis, RR basis,
prime G or parity matrix was constructed by this review.

## 1. Reviewed State And Main Findings

The local snapshot contains the final reviewed SOURCE.md and PRIME_CLASS.md.
References to source line numbers below refer to these snapshots, which
matched the parent at the last comparison.

| Issue | Finding |
| --- | --- |
| Even-divisor Kummer sequence | Correct, including rational descent |
| Local splitting with zeros and poles | Correct; use the leading unit, never raw evaluation |
| Arbitrary quadratic choice in the infinite tower | Correct; no repeated GS test or cofinality required |
| Rational torsion to principal function | Classical RR problem with complete divisor; not hard principal-ideal search |
| Exact order and rational 2-primary presentation | Compose with charged geometric arithmetic; no odd-primary discrete logarithm |
| Fixed-characteristic normalization | Polynomial finite-module construction available, including degree >= p |
| Height reset | Valid with explicit function, divisor and branch representations; existence of a plane equation alone is insufficient |
| Maximum prime-class mass | Correct; does not assume prime classes are uniform |
| Prime section probability | Corrected exponent is 3g+5; unchanged expected-polynomial conclusion |
| Output law after cube rejection | Uniform on good closed primes of the generated curve, not on classes or matrices |

The prior resolutions actually used were the plane-adapter resolution and
PLANE_REVIEW.md; the prime-sampler resolution and SAMPLER_REVIEW.md; the
auxiliary-construction review's relation-lattice argument; and the tower
seed and generic-class review. Their conditional arithmetic interfaces are
not treated as implemented facts. The existing seed infinitude certificate
is retained as a reviewed premise, rather than rerunning its residue scan.

## 2. Kummer Classes, Principal Functions And Local Splitting

Let X/k be smooth, projective and geometrically connected, k = F_q of odd
characteristic, with rational O. Send an even-divisor class [f] to
[div(f)/2]. Its image is in Pic^0(X)[2] = J(k)[2]. If that image is zero,
div(f)/2 = div(h) for h in k(X), and f/h^2 is a nonzero constant. Conversely
a rational 2-torsion divisor class has a rational divisor representative D
and 2D is principal over k. A rational point identifies rational Picard
points with line bundles over k; rational meromorphic sections give rational
divisors. Equivalently, descent of a principal function follows from Hilbert
90, or directly from base change for the one-dimensional RR space below.
This proves exactly

```text
0 -> k^*/k^{*2} -> {f : div(f) even}/k(X)^{*2} -> J(k)[2] -> 0.
```

For a nonzero f in L(-2D), div(f)-2D is effective of degree zero, hence zero.
If 2D is principal, L(-2D) has dimension one over k. Its sign in SOURCE.md
line 32 is correct. A nontrivial D has L(-D) = 0 but L(-2D) != 0, so taking
the latter space does not imply or require a square root of f in k(X).

The hard principal-ideal problem does not supply all valuations at the
places at infinity and asks for them or a generator. Here the entire
divisor is specified with polynomially bounded height. The distinction is
substantive, not terminology. In the one-infinity representation used below
the missing infinity coefficient is particularly easy to control, but the
algorithm never invokes an unrestricted principal-ideal oracle.

If f = t_P^(2a) u in the completion at a marked rational point, the
quadratic extension is unramified there and splits exactly when the nonzero
residue of u is a square in k. Replacing t_P by t_P v multiplies the residue
by v(P)^(-2a), a square, including when a is negative. Multiplication of
functions adds these character bits. Thus the matrix M is a well-defined
linear map on the even-divisor square-class space. Even valuations at all
closed places imply unramifiedness everywhere, not just at marked places.

Adjoining a nonsquare constant to arbitrary lifts of a certified torsion
basis gives a basis of that square-class space. Therefore a nonzero kernel
vector cannot yield a square radicand. The nontrivial constant class has
bit one at every rational marked point; it is not in the kernel. A quadratic
extension with enlarged constant field would be precisely this constant
extension. Hence the selected cover is connected and geometric.

It is not enough to label classes as independent: the 2-primary algorithm
must certify its presentation using the true h and exact arithmetic. With
that certificate, no further exponential square-class enumeration is needed.

## 3. Why Every Chosen Step Can Continue

Fix the maximal unramified S_0-split pro-2 extension K_infty/K_0. Inductively
let N be the normal closure over K_0 of the previously chosen finite chain.
It is a finite 2-extension. For a new quadratic step, compose N with its
finitely many K_0-conjugates. Over N these are quadratic or trivial, so their
compositum has elementary-abelian 2-power degree over N. Its normal closure
therefore still has 2-power degree over K_0.

Unramified covers stay unramified under base change and composition; complete
splitting of S_0 stays complete under these conjugates and composita. Thus
the new field lies in K_infty. This argument is not an instruction to
compute the potentially large normal closure.

For every finite chosen K_j, H = Gal(K_infty/K_j) is an infinite open
pro-2 subgroup. A nonidentity element survives in a finite 2-group quotient;
that quotient has an index-two normal subgroup. Pulling back gives an
index-two subgroup of H and a further quadratic extension of K_j inside
K_infty. Kummer theory therefore guarantees ker(M) != 0 at every step.

All marked places split in this further extension, since their decomposition
groups in K_infty/K_0 are trivial. Hurwitz gives g_(j+1) = 2g_j-1; the
number of marked rational places doubles. Starting from genus six and
23 points gives g_j = 5*2^j+1 and 23*2^j marked places. No assumption that
the chosen chain contains a particular degree-eight or elementary cover is
allowed. The earlier special-cover attack does not automatically transfer
by degree alone.

## 4. A Concrete Bounded Representation Invariant

The following is an additional constructive deduction for this proposal,
not a claim that the existing backend already maintains these data.

At each reset retain:

1. A geometrically integral plane equation F(x,y) over k, monic and separable
   in y, of total degree at most 2g+2, and its function-field interpretation.
   Choose the separating coordinate from pole orders 2g+1 and 2g+2.
2. Integral bases over k[x] and over k[1/x], together with their power-basis
   conversion matrices and normalized polynomial-module/HNF representations.
3. Divisors as fractional ideals plus complete infinity multiplicities;
   marked places as ideals/residue maps of the normalization, not just their
   pairs of plane coordinates. Keep one rational marked place O.
4. Actual RR functions in those coordinates and multiplication in the field.
   Build R_j = L(j*ell*O), ell = 2g+2, through j=7 afresh from RR.

The coefficient degree of F and its field degree are both O(g). The
normalization bound in Section 5 makes basis conversion sizes polynomial.
The explicit genus-six seed can be normalized and reset once to initialize
this invariant; its fixed-size setup adds only a constant to the asymptotic
cost.
For an effective finite divisor E, its ideal has k-colength deg(E). In HNF
relative to the normalized integral basis, the determinant degree is that
colength, bounding its polynomial entries. Negative parts use fractional
ideal inverses. Infinity multiplicities and support degrees are charged.
Thus divisors of height polynomial in g have polynomial representations in
this invariant. Here height means max(deg D_+, deg D_-), NOT abs(deg D).

There is a useful stronger choice of torsion representatives. Bruin's medium
model represents a class by an effective E_i of degree ell with class
[ell*O-E_i]. For order two, its negative is the same class, so choose

```text
D_i = E_i - ell*O,
0 != f_i in L(2*ell*O - 2*E_i),
div(f_i) = 2*E_i - 2*ell*O.
```

Every f_i lies in L(2*ell*O): it is regular away from O. For r <= 2g
torsion basis elements, the product radicand lies in L(2*ell*r*O) and has
pole degree at most 2*ell*r = O(g^2). Including the nonsquare constant
does not change this. This removes any need to trust a raw nested product
of unbounded historical representatives.

Recovering E_i from its represented subspace is also constructive. Its
space W_E = L(2*ell*O-E) has base divisor exactly E as sections of
O(2*ell*O), since its residual line bundle has degree ell >= 2g+1. The
ideal generated by its actual function basis is the ideal of E away from
O; the coefficient at O is 2*ell plus the minimum valuation of that basis.
Ideal/HNF operations and valuations recover the complete divisor. This
avoids interpreting a mere abstract Jacobian label as a divisor oracle.

Finite algebra decomposition and finite-field polynomial factorization give
the closed-place data when needed. Their dimensions are bounded by the
divisor degrees; they do not enumerate points over exponentially large
extensions. A rational local uniformizer can be obtained from P/P^2 on the
normalization. Leading residues, ideal powers, and truncated local arithmetic
have polynomial cost in the explicit degree and valuation bounds above.
This is sufficient for the marked-point matrix, including zeros and poles.

## 5. Normalization And RR In Fixed Positive Characteristic

### Primary-Source Check

[Eisentraeger-Hallgren, Appendix B, Algorithms B.6/B.8, Proposition B.7 and
Theorem B.9, printed pp. 353-356](https://msp.org/obs/2013/1-1/obs-v1-n1-p17-s.pdf)
are the relevant classical portions: two ideal lattices, polynomial-matrix
reduction and their intersection compute RR. Section 2 supplies the
finite/infinite ideal model and cites Chistov for integral bases. Section 5,
Theorems 5.1-5.3, instead uses quantum hidden-subgroup methods for units,
principal ideals and class groups; none is used here. The paper's compressed
parameter list must retain defining-equation and basis sizes: extension
degree alone cannot bound genus, e.g. hyperelliptic fields of unbounded
genus have extension degree two. Its RR analysis also depends on divisor
height, not the logarithm of unbounded multiplicities. Our explicit invariant
bounds all these inputs.

For normalization, the following finite-module derivation supplies an
independent small-characteristic justification. It does NOT assert a
polynomial bound for an arbitrary growing-variable Groebner implementation.
The normality test used is [Greuel-Laplagne-Seelisch, Proposition 2.2 and
Lemma 3.1](https://arxiv.org/html/0904.3561v3#S2); it applies to reduced
Noetherian rings, not only when characteristic exceeds extension degree.

### Polynomial Normalization Deduction

Take a monic separable defining polynomial P(x,T) of degree N in T with
coefficient x-degrees at most H. Put A_0 = k[x][alpha] and
delta = disc_T(P) != 0. Both deg(delta) and the power-basis multiplication
table are polynomial in N,H. Let B be its normalization. The trace-dual
inclusions give

```text
A_0 subset B subset A_0^vee subset delta^(-1) A_0.
```

Indeed products of integral elements have integral trace in k[x]; inverse
of the trace matrix has denominator delta. Consequently delta*B subset
A_0, and dim_k(B/A_0) <= N*deg(delta).

For any intermediate order A, take J = radical(delta*A). Outside delta,
A_0 is finite etale over a localization of k[x], hence normal, and every
intermediate order equals B there. Thus J contains a nonzerodivisor and
its vanishing set contains the nonnormal locus. The cited criterion says
that A = (J:J) exactly when A is normal; otherwise (J:J) strictly enlarges
A inside B. There are at most N*deg(delta) strict enlargements.

All computations can stay in finite k[x]-modules. Normalize delta*A as
an HNF submodule between delta*A_0 and A_0 after every step; coefficient
degrees are bounded by their polynomial colength. The algebra A/delta*A
has k-dimension N*deg(delta). Its nilradical is the kernel of the k-linear
map a -> a^(q^b) once q^b is at least that dimension. Compute the matrix
by repeated modular powering and linear algebra; its inverse image is J.
The colon (J:J) is a polynomial-module membership problem: for candidates
in delta^(-1)A_0 impose multiplication into J for every basis element of J.
Polynomial-module kernels/HNF solve it with polynomial matrix sizes and
degrees. The determinant trick ensures these endomorphisms are integral,
so the fixed ambient denominator bound continues to apply. A nonzero
constant delta is the already-normal special case.

This proves a polynomial normalization route for the supplied separable
model over k, with no assumption p > N. Apply the same construction over
k[u], u=1/x, after multiplying alpha by a bounded power of u to make its
equation monic integral there, and localize at u=0 for infinity arithmetic.
The exponent and new equation degrees are polynomial in N,H.

RR then uses the two supplied bases, fractional ideals and polynomial-
matrix reduction. All operations and their output coordinates have
polynomial bit size in these explicit inputs and divisor heights. In
particular, computing f_i is not justified by its divisor degree alone:
the normalized-coordinate input bound is doing necessary work. No rational
point is obtained by extending constants: a retained rational O already
exists at every step.

### Why One Step Reaches The Reset In Polynomial Size

Starting from the invariant, form L = K(z), z^2=f. Since f is not square
and p != 2, this is a separable quadratic field. In the basis
{y^i, y^i*z} over k(x), its dimension is twice the previous field degree,
O(g); its multiplication entries have polynomial degree. The radicand's
functions are computed and reduced in the fixed current field, not a
recursively expanded tower expression.

To obtain a primitive presentation if a routine requires one, use
alpha = y+c(x)z. Among the N embeddings of L/k(x), each pair excludes at
most one value of c, unless it excludes none; equality of both y and z
would mean the embeddings were identical. A list of more than N(N-1)/2
distinct c in k[x] therefore contains a primitive choice. Such a list has
polynomial size and coefficient degrees O(log_q N); no constant extension
is required. Test full minimal-polynomial degree by linear algebra over
k(x). Monicity/integrality follows because y,z are regular away from the
old infinity fiber. Computing the minimal polynomial and its conversion
matrices has polynomial degree/size. Its discriminant bound therefore
puts normalization within the preceding argument.

This closes the potential circularity "first normalize cheaply in order
to obtain a cheap model": the pre-reset model itself already has polynomial
size in the CURRENT genus. The reset in Section 6 prevents this polynomial
bound from being repeatedly composed on a growing historical encoding.

## 6. Reset, Branches, Order And The 2-Primary Group

On the normalized cover choose a rational lift O'. RR computes functions
with exact sole pole orders 2g'+1 and 2g'+2 at O'. Their generated subfield
has index dividing both pole orders, hence index one, including inseparable
degree. Choose as separating coordinate the one whose pole order is prime
to p. Such a coordinate exists because the orders are consecutive.

The unique weighted relation gives a monic, geometrically integral plane
equation of total degree 2g'+2. Relation recovery uses actual functions
of pole order O(g'^2), so polynomial-size RR arithmetic suffices. Here the
construction starts with an explicit function field: it need not first
recover a compact section ring from a native matrix. Recompute the two
normalized integral bases on this fresh bounded-degree equation.

Keep the expressions for the new coordinates in the previous presentation.
They identify the function fields, not just their finite point sets. If
explicit inverse coordinate maps are wanted, bounded rational expressions
can be recovered by coefficientwise linear algebra: multiply a function of
bounded pole degree by an RR denominator vanishing at its finite poles,
then by the new equation's discriminant. Both resulting functions lie in
the plane coordinate ring with polynomial degree bounds from the trace
dual. Searching A(new_x,new_y) - f*B(new_x,new_y) = 0 in those bounded
spaces gives the inverse without arbitrary elimination. Adjacent maps can
be stored separately; do not expand a full historical composition.

**Track branches, not just plane coordinates.** Distinct smooth points can
map to the same singular plane point. Transfer each marked residue map by
evaluating the new integral-basis elements, using their pullbacks and local
leading residues when a displayed quotient has 0/0. Store the resulting
maximal ideal/residue map and the infinity-branch label. The finite list
has O(g') entries and all needed functions/local precisions have polynomial
bounds. Splitting the previous O leaves two branches; choosing O' does not
permit dropping the other marked one.

[Lauder-Wan, Corollary 3, printed pp. 582-583, and its proof on pp. 610-611](https://library.slmath.org/books/Book44/files/18lauder.pdf)
apply to the possibly singular plane model's smooth projective curve. The
proof separates the weight-one numerator from root-of-unity corrections;
its value at one is the Jacobian order. With two variables and one equation,
the bit cost is polynomial in plane degree, p and the constant-field
extension degree. There is no p > degree hypothesis. Fixing p=100003 thus
gives polynomial cost in g, not uniform polynomial cost in log(p).

Build the degree-ell one-point algebra through seven by RR and multiplication.
[Bruin, Algorithm 3.8 and Section 3.6](https://arxiv.org/html/1003.2563)
give the normalized perfect Frey-Ruck pairing on supplied rational 2-torsion
and J/2J; 2 divides q-1. No high-order roots of unity or rational torsion
basis is needed to evaluate it. The alternating Weil pairing restricted to
rational torsion would not be a valid replacement.

Now the reviewed relation-lattice construction composes: exact
h=2^s*M, fresh prime-class samples with mod-two character bias <=1/2,
exact group operations and those order-two pairings generate and certify
the entire rational 2-primary subgroup. The HNF saturation uses at most
st strict relation enlargements for t supplied generators. At most s
strict subgroup enlargements are needed, with conditional escape probability
at least 1/4. Since s <= log_2(h) = O(g log q), the reviewed O(s^4) internal
sample-row bound and O(s) pairings per row are polynomial. The 4s outer
proposal bound alone is not the total cost. Taking 2-adic valuation needs
no factorization of the odd part of h.

Use new independent draws for adaptive relation tests; a frozen bank or
success-conditioned group-generation samples can invalidate expected cost.
Verification of a sampled relation space certifies correctness, and the
known exact order certifies completeness. No odd-primary discrete logarithm
or arbitrary full class-group presentation enters this construction.

The source of these samples is also charged: the smallest sufficient prime
degree n obeying q^n >=16(g+1)^2(n+6)^2 is <=g+1 for this q, and the reviewed
conversion of P to [P-nO] uses bounded operations. With ell=2g+2, i=2,
the required prime sampler and pairings fit the algebra just constructed.

After each reset all state has size polynomial in the new genus, with a
fixed exponent independent of j. Therefore summing expected per-step costs
along g_j=5*2^j+1 is polynomial in final genus. This is not polynomial time
in the bit length of e; an explicit k-by-m matrix already has Theta(e^2)
field entries. Arbitrary choices of nonzero kernel vectors do not change
these uniform bounds.

This does not solve the broader class-field-tower problem discussed in the
2013 paper's introduction: no full Hilbert class field at each stage is
constructed, no cofinality is promised, and polynomial dependence on log(p)
is not obtained. Those scope differences must accompany any comparison.

## 7. Uniform Primes And Maximum Class Mass

Let d=2g+1 and H be the bad degree-d classes. For every rational class C,
Riemann-Roch gives exactly

```text
M_d = (q^(g+2)-1)/(q-1)
```

effective rational representatives. Primes in C are a subset. Thus the
maximum atom of the prime-class law is at most min(1,M_d/N_d), and

```text
Pr([G] in H) <= |H| M_d/N_d
             <= B_e * h M_d/N_d
             <  B_e * (2d*q/(q-1)) * (318^2/q)^g = R_e.
```

Here N_d >= q^d/(2d) follows from the reviewed prime-count estimate under
q^d >=4(g+1)^2(d+6)^2, and h <318^(2g). This is exactly the factor needed
to transfer the previous bad-class bound; no uniform or nearly uniform
prime-class assumption is made. The rational 3-torsion factor 9^g remains
inside B_e. Neither N_d nor h needs to be estimated empirically for this
inequality.

At e=8, exact rational arithmetic gives

```text
g=41, d=83, a=7,
R_8 = 1.4397191670194628283986631691824725196876643186065... * 10^(-127)
    < 10^(-126).
```

The source's successive-ratio argument is valid:
R_(e+1)/R_e < 8*9^5/q^3 = 472392/1000090002700027 < 1.
The prime-count condition also holds at e=8 and grows thereafter. In
particular the good-prime set is nonempty at every claimed level.

[Bruin, Algorithm 3.2, pp. 25-26](https://arxiv.org/html/1003.2563)
uses truncated algebra through 2i+2, needs no zeta input, and samples
closed primes with the component-count rejection correction. Reduced
degree-d components, not multiplicities or arbitrary factors, enter that
correction. For ell=2g+2, i=2, our independent RR substitution is

```text
dim L(2*ell*O) = 3g+5,
dim L(2*ell*O-G) = g+4,
floor((4g+4)/(2g+1)) = 2,
p_trial = (N_d/2) * (q^(g+4)-1)/(q^(3g+5)-1)
        >= (1-q^(-g-4))/(4d).
```

The initial text used 3g+4 instead of 3g+5 in both exponents. The current
snapshot fixes it. At g=41 these dimensions are 128 and 45, not 127 and
44. The corrected expected section-trial bound is at most
4d/(1-q^(-g-4)); it leaves the claimed Omega(1/d) acceptance intact.

Since d>1, a closed degree-d prime cannot contain a rational evaluation
point. No moving lemma or full-support word is needed. Complete L(G)
has dimension g+2; for e>=8, evaluation on L(2G) is injective and normal
generation gives square dimension 3g+3. Normal generation and RR also give

```text
dim((V^3)^perp) = m - (ell(3G)-ell(3G-D)) = ell(K-3G+D).
```

This does not assume injection on L(3G). Exact cube-rank rejection is
therefore sound. Its expected number of prime proposals is <=1/(1-R_e).
Conditional on the generated curve and marked set, rejection from an exact
uniform prime sampler is exactly uniform on its good degree-d primes.
It is generally not uniform on Pic^d, matrices, or native witnesses.

The escaped obstruction is specifically the nonzero same-code cubic
annihilator. Auxiliary-code norm attacks, systematic search, and special
tower methods remain separate. No classical hardness or quantum advantage
follows from the generator or this rejection bound.

## 8. Controls, Reproduction And Remaining Work

The parent owns probability and local-unit implementation. I did not modify
or duplicate those tests. Two independent exact controls were added here:

- In characteristic 3, Y^4-X^3 with X=t^4,Y=t^3 has separable function-field
  degree 4 > p. Its monomial radical/endomorphism normalization steps have
  gap sets {1,2,5}, {1,2}, empty; the discriminant is 2*X^9. This checks
  a small-characteristic example of the finite-module argument, not its
  general asymptotic implementation.
- On Y^2=X^2(X+1) over F_5, normalization X=t^2-1,Y=t(t^2-1) maps two
  different rational branches t=1 and t=4 to the same plane point (0,0).
  This is an exact countercontrol to storing only marked plane coordinates.

Both passed. Results are in exact_controls.json. Run from this directory:

```sh
/Users/jaspersands/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B exact_controls.py
```

The rational R_8 calculation was independently executed inline, not installed
as a competing parent probability helper. Its decimal above is a displayed
upper bound, not an observed frequency or an actual prime-class distribution.

The actual next experiment remains one genuine cover beyond the explicit
elementary presentation, carrying normalized bases and distinct marked
branches, followed by a degree-(2g+1) prime, its complete L(G), and the actual
matrix dimension/square/cube certificates. Backend omissions in any of
those representations would invalidate that implementation's cost/correctness
claim. They do not revive an intrinsic class-group or principal-ideal barrier
against the specific theoretical route established above.

Primary sources were checked beyond abstracts. Local PDF copies are kept
for Eisentraeger-Hallgren, Bruin, Lauder-Wan, and Greuel-Laplagne-Seelisch.
The old Diem URL returned 404 and direct Chistov retrieval failed; no claim
of checking those full texts is made. The normalization proof here uses
the separately inspected normality criterion and explicit module bounds,
not an unverified quotation from either inaccessible source.

Snapshot SHA-256:

```text
SOURCE.md
7570024d51052cbdb71a0533fdf04c6501cf3db006095eea374bd4ec18951654
PRIME_CLASS.md
a224881008fb02bc41554b2681b978e8bff5c69283d4dcb9e77a2b3975c6c525
```

All writes were confined to this new review directory. Parent files, Git,
and UI were untouched. No subagents were used. This is an independent
mathematical audit and small exact-control record, not a native run receipt.
