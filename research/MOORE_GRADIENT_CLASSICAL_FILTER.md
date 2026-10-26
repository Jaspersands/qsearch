# High Orbit Rank Does Not Rescue Moore-Form Symmetry

2026-10-22. Written classical reduction and executable Monte Carlo
recognizer, under review. Not a new quantum algorithm, a general polynomial
stabilizer solver, independent verification, or a novelty claim.

## 1. Research Decision

The remaining succinct-polynomial application needs more than high formal
degree AND failure of the small-orbit-module filter. Even together these
conditions do not supply a credible hard family. There is a scalable
class-nine example with exponential orbit rank that admits an ordinary
classical attack from its PUBLIC circuit, without its construction advice.

The attack recognizes scalar Moore determinants of unknown base-field
linear forms. Ordinary reverse derivatives recover their row space, and
a fresh extension-field polynomial identity test verifies the complete
form. This turns the original problem into a known subspace-stabilizer
problem in the original matrix dimension. It does not enumerate the
polynomial's linear factors, monomials, orbit, or an exterior-power module.

This is a stricter classical falsifier, not evidence that the remaining
uncovered circuits are hard. A targeted literature search still did not
establish a natural hard application for the Rees theorem. Do not create
a campaign of larger Moore examples or treat this negative application
result as an attack on the Rees HSP theorem itself.

## 2. Public Input And Exact Scope

Input is a division-free arithmetic DAG C over F_p in D variables, p>4,
with canonical base-field constants and binary addition/multiplication.
The circuit, not just base-field evaluations or quantum copies, is public.
The syntactic degree bound Delta is computed from the DAG. Its bit length
is polynomial in circuit size even when the degree is enormous.

For independent rows ell_1,...,ell_r in F_p^D, define

```
M_W(x) = det(ell_j(x)^(p^i))_(0 <= i < r, 1 <= j <= r),
W = span_Fp{ell_1,...,ell_r}.
```

A change of row basis multiplies M_W by a nonzero base-field determinant.
The recognized class is F=a M_W with a in F_p^*, 1<=r<=D. Recognition
does NOT assume that the row basis, r, scalar, determinant gates, or
Frobenius gates are exposed. The exact tested identity, rather than a
syntactic template match, is what authorizes the subsequent reduction.

Zero, nonzero constants, general p-th powers, arbitrary sums/products of
Moore forms and extension-field coefficient actions are not automatically
accepted. Returning no recognized form is not a hardness certificate.

The implementation reuses the existing arithmetic DAG validation and
reverse differentiation in frobenius_circuit_lift.py, but accepts ONLY
ordinary gates. In particular it does not replace a p-th power by an
independent variable or use the old no-carry guard.

## 3. Why The Gradient Reveals W

For any formal F define W_F to be the F_p-span of all coefficient vectors
of its row gradient. This is a subspace of F_p^D of dimension at most D.
At any extension-field point z, expand every gradient coordinate in the
same F_p basis of the extension. Every resulting row belongs to W_F.

For a Moore form, let y_j=ell_j(x). Only the exponent-one determinant row
has nonzero ordinary derivative in characteristic p. Consequently

```
grad_x F = a sum_j (-1)^(1+j) M_(all y except y_j)(y)^p * ell_j.
```

For r=1 the coefficient is one. For r>1 these cofactor polynomials are
linearly independent: each has nonempty monomials involving precisely all
y variables except one, so their monomial supports are disjoint. They are
nonzero since the powers 1,p,...,p^(r-2) are distinct. Independence of
the ell_j makes substitution from formal y variables injective. Therefore

```
W_F = W.
```

No requirement p>r, p>D, or p>(D-1)*Delta appears. The proof does NOT say
that zero first derivatives make an arbitrary polynomial constant. That
false statement would erase inseparable terms; Section 5 prevents it.

## 4. Costed Randomized Recovery And Verification

Let D_max=sum_(i=0..D-1) p^i and B=max(Delta,D_max). Choose E=F_q,
q=p^k, such that

```
q >= (D+2)*B/epsilon.
```

Here log(q)=O(log(max(1,Delta))+D*log(p)+log(D/epsilon)). Field elements
are still polynomial-length. Standard randomized irreducible-polynomial
construction with verification supplies E; construction costs are paid.
The executable uses FLINT and verifies its modulus. It does not implement
a separately capped field-construction controller.

1. At D fresh independent uniform points of E^D, evaluate the circuit and
   reverse gradient. Expand gradient coordinates over F_p, and accumulate
   their row space S by F_p Gaussian elimination. Stop early only at rank D.
2. If S=0, return an inconclusive no-gradient status. Otherwise use its
   canonical basis to define M_S. At a NEW anchor z, abort if M_S(z)=0.
   Compute a=F(z)/M_S(z). Reject if a=0 or a is outside F_p.
3. Fix S and a. Draw one more INDEPENDENT point w. Accept only if
   F(w)=a M_S(w).

**Recovery bound.** If S is a proper subspace of W_F, fix a vector v in
S-perp but not W_F-perp for the proof. The polynomial grad(F).v is nonzero
of degree at most Delta-1. By Schwartz--Zippel a fresh sample fails to
increase rank with probability at most (Delta-1)/q. Conditional on the
complete previous history, S and v are already fixed. A first-failure
union bound over D samples gives D*max(Delta-1,0)/q. This does not union
bound over every possible subspace or every coefficient vector.

**Identity bound.** Once S is fixed, M_S has degree at most D_max, and its
zero anchor probability is at most D_max/q. Once the scalar is fixed,
a false identity passes the fresh final test with probability at most
B/q, even conditional on an earlier bad rank history. Both false
recognition and failure to recognize a true nonzero Moore form are covered
conservatively by (D+2)*B/q<=epsilon. An anchor failure is explicit ABORT,
not an unbounded retry loop. Bounds assume genuine independent uniform
draws; printed seeded diagnostics are not probabilistic certificates.

Circuit evaluation/differentiation, extension arithmetic, at most D+2
probes, and row solving are polynomial in the original circuit size, D,
log(p), and log(1/epsilon). The candidate determinant is evaluated in
polynomial time. Neither q, numeric Delta, p^r, nor the orbit rank is a
loop bound. A circuit for a positive control is compiled by the standard
[division-free Samuelson--Berkowitz construction](https://cs.uwaterloo.ca/~r5olivei/courses/2021-winter-cs487/berkowitz-paper.pdf),
with each power implemented by charged binary multiplication gates. The
simple implementation uses polynomial sequential size; it does not claim
the paper's optimized parallel complexity.

## 5. Why Recognition Cannot Stop At The Gradient

F=x_0+x_1^p and G=x_0 have the same ordinary gradient but different finite
symmetries. For instance, the shear x_1 -> x_1+t*x_0 preserves G but not F
for nonzero t. Therefore recovering W_F does not generally identify the
stabilizer. The test forces the scalar-selection anchor to hide x_1^p,
then checks that the independent final point exposes it.

Similarly F=x_0^p is nonconstant with zero gradient. This recognizer
returns no-gradient rather than asserting that every matrix fixes it.
Other existing filters may handle it. A vanishing derivative is neither
an accepted Moore identity nor a universal no-go theorem.

## 6. The Actual Stabilizer Reduction

Use the original action T_g F(x)=F(g^-1 x), with g in GL(D,p).
The gradient coefficient space transforms as W_(T_g F)=W_F*g^-1.
Hence T_g F=F implies W*g^-1=W. Conversely, if W*g^-1=W, write

```
(ell_1,...,ell_r)^T g^-1 = A_g (ell_1,...,ell_r)^T.
```

Frobenius commutes with base-field coefficients, so

```
T_g F = det(A_g)*F.
```

Thus the exact general condition is preservation of W AND det(A_g)=1.
The implementation retains both conditions when checking a supplied matrix.
Dropping the determinant for arbitrary GL(D,p) is wrong; diagonal controls
test this explicitly.

For a supplied promised p-subgroup Gamma<=GL(D,p), A_g has p-power order.
Its determinant belongs to F_p^*, whose order is coprime to p, and is
therefore one. In THIS setting

```
Stab_Gamma(F) = Stab_Gamma(W).
```

Use the faithful contragredient generators g^(-T) to act on the columns
W^T and apply the published solvable matrix-group subspace-stabilizer
algorithm. Convert a returned generator h back to h^(-T). There is no
lost representation kernel and no exponential exterior representation.
[Luks, Computing in Solvable Matrix Groups](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
states the polynomial-time dependency with a bound on prime factors OTHER
than the field characteristic. For a p-group over F_p that condition is
satisfied. The later [Luks--Miyazaki normalizer paper, Section 5](https://ix.cs.uoregon.edu/~luks/polytimenormalizers.pdf)
supplies further detail on the subspace-stabilizer divide-and-conquer
machinery. These are imported algorithms, not implementations in this pass.
No bounded nilpotency-class or exponent-p premise is needed for this
classical reduction.

### Elementary Backend When The Common Matrix Algebra Has Small Index

For an additional checkable sufficient regime, even the general Luks
subspace backend is unnecessary. Form the nonunital associative algebra J
generated by the public matrices g_i-I: start with their span and close
under left multiplication by each g_i-I. There are at most D^2 independent
matrices. Compute powers of J until J^nu=0, and require nu<=p. This is a
test of the COMMON algebra, not just the nilpotency of individual matrices.
Failure of this guard does not imply a hard group.

All products and inverses of supplied generators belong to 1+J. Under the
guard, log(1+X) and exp(A) are finite polynomials with denominators below p.
The whole algebra group has class at most nu-1<p, so the matrix BCH and
Lazard correspondence apply. Close the F_p-span of log(g_i) under matrix
commutators to obtain L=log(Gamma). For a recognized row space W,

```
h = {A in L : W*A is contained in W}
```

is the exact hidden Lie subalgebra. Indeed exp(A) preserves W when A does,
and log(g) preserves W when g does, since both maps are polynomials in
the corresponding endomorphism. No polynomial-degree bound for F is used.
If N has columns spanning the annihilator of W, the conditions W*A*N=0
are LINEAR in the coordinates of A in L. Solve that system and exponentiate
a basis of its kernel. The resulting matrices generate the full stabilizer.

This procedure is polynomial in matrix/input dimensions and log(p), using
ordinary linear algebra; all algebra-closure loops have a dimension cap.
It is a written route, not an implemented general generator-recovery
backend in this pass. It gives a precise mechanical follow-up without
requiring a new general-purpose computational-group implementation.

For UT_b(F_p)^m, J is block-diagonal strictly upper triangular and J^b=0.
Thus p>b-1 suffices regardless of D=b*m. The class-nine family therefore
has this elementary attack as well, including the live D50,p43 control.

**Guard falsifier.** Let X=J_p tensor I_p and Y=I_p tensor J_p, where J_p
is a nilpotent Jordan block. The matrices g=I+X and h=I+Y commute and
have order p; every element of their group has order dividing p. However,
the common algebra has nilpotency index 2p-1, and the truncated individual
logs need not satisfy log(g*h)=log(g)+log(h). The exact p5,D25 control
verifies this failure. Exponent-p and small ABSTRACT group class alone
do not license a matrix-log embedding. Do not weaken the common-J guard
when implementing this follow-up.

## 7. An Exponential Orbit Rank With Fixed Class

Let Gamma=UT_b(F_p)^m act block-diagonally on D=b*m variables, b>=3 fixed,
p>b-1. Set ell_i=x_(i,1), the first coordinate of each block, and take
the rank-m Moore form. Its degree is sum_(j=0..m-1) p^j; its division-free
circuit size is polynomial in m, b, and log(p).

In each block, the first inverse row ranges over every (1,a_2,...,a_b).
Their F_p-span is the full b-dimensional row space: subtract (1,0,...,0)
to obtain every remaining coordinate vector. The independent block orbits
therefore span their m-fold tensor product, of dimension b^m.

Expanding the Moore determinant over F_p-linear forms gives the coordinate
Moore minors with exactly one selected variable in each block. There are
b^m of them. They are independent formal polynomials because distinct
selected variable sets have disjoint monomial supports. Thus the cyclic
polynomial orbit module has EXACT rank b^m, not merely a lower bound from
a failed random search.

Nevertheless the recognizer recovers the m-dimensional W in polynomial
time, and the preceding subspace reduction solves its stabilizer. In the
displayed coordinates H=UT_(b-1)(F_p)^m, embedded by requiring the first
row's off-diagonal entries to vanish. Conjugating the supplied group and
changing the public polynomial circuit's coordinates preserves the argument;
the recognizer need not be given that coordinate transformation.

Taking b=10 gives class nine with growing dimension and prime. The live
control uses p=43,m=5,D=50: polynomial degree 3,500,201 and orbit rank
100,000. It uses 449 binary arithmetic nodes, recovers rank5 with 50
gradient probes and one fresh identity test, and never builds that orbit
module. The 100,000 rank is from the proof, not an executed enumeration.
The smaller two-UT3 control independently constructs the exact rank9
module; a cap4 fails before the gradient recognizer succeeds.

## 8. Falsifiers, Status And Reproduction

- Correctness of the general recognition argument still needs independent
  review. Ordinary Monte Carlo tests do not create formal certificates.
- The full subspace-stabilizer backend is not implemented here. Exact
  supplied-matrix decisions and finite exhaustive UT3 controls are narrower.
- No arbitrary circuit root extraction, polynomial factorization, or
  universal high-degree stabilizer algorithm follows.
- Public gradients are not available from unknown quantum copies or an
  oracle limited to base-field values. Do not transfer this dequantization.
- Large orbit rank remains compatible with both easy and unresolved
  families. This result only closes the Moore-form escape route.
- If a new candidate differs by an inseparable term, analyze the whole
  polynomial; do not discard that term based on its derivative.

Run:

```
python -m pytest tests/test_moore_gradient_filter.py -q
python -m theorems.moore_gradient_filter --write
```

Artifact: research/reductions/moore_gradient_filter.json. All novelty,
independent-review, formal-proof, executed-group-solver and quantum-advantage
flags remain false. No candidate or central registry entry is admitted.
