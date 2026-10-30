# Unmarked Integral Pencils Reduce To Integral Similarity

Date: 2026-10-30. A constructive, classical reduction with explicit promises.
Not a new quantum primitive, a generic tensor-isomorphism algorithm, or an
implementation of a quantum principal-ideal solver.
An independent adversarial review confirmed the decision reduction and its
uniform bit-cost argument. This is not external peer review or formalization.

## Native Problem And Action

Input two ordered pairs A=(A0,A1), B=(B0,B1) of n by n integer matrices,
with n>=3. Promise that A0 is unimodular and both homogeneous determinant
forms det(x*A0+y*A1), det(x*B0+y*B1) are irreducible over Q. The first
slice of B need not be unimodular. We ask if there exist

```
g=[[a,b],[c,d]] in GL(2,Z),     L,R in GL(n,Z),
B0=L*(a*A0+b*A1)*R,            B1=L*(c*A0+d*A1)*R.
```

This is the full ordered GL(2,Z) x GL(n,Z) x GL(n,Z) action, not an
action which fixes the first slice. Factor permutations are not included.
Irreducibility implies det(B0)!=0: otherwise the homogeneous determinant
would have the rational linear factor y. It also ensures the irreducible
degree-n characteristic polynomials used below.

## Polynomial Classical Preprocessing

Set M=A0^(-1)*A1, N=B0^(-1)*B1, f=charpoly(M), h=charpoly(N), and
K=Q[alpha]=Q[t]/f. M is integral; N need only be rational.

1. Factor h over K and retain its linear factors, equivalently its roots
   beta in K. There are at most n. This enumerates field identifications,
   not permutations of roots in a normal closure. Use established
   polynomial-time factorization over explicit number fields.
2. For each beta, solve over Q the four-variable linear system
   `a*beta+b*alpha*beta-c-d*alpha=0`. Express its coefficients in the
   power basis of K. A nonzero solution has `a+b*alpha!=0` and gives
   `beta=(c+d*alpha)/(a+b*alpha)`. Its 2x2 determinant cannot vanish,
   since that would make beta rational, contradicting its degree n.
3. The kernel, if nonzero, is a single rational line. Two invertible
   fractional-linear expressions agreeing at alpha give a polynomial
   of degree at most two vanishing at alpha. Since n>=3, it vanishes
   identically, so the two projective matrices coincide.
4. Clear denominators and remove the gcd of the four entries to obtain
   a primitive integer matrix g0 on this line. Every integral matrix on
   the line is an integer multiple of g0. Thus the line meets GL(2,Z)
   exactly when det(g0)=+1 or -1; the possibilities are then +/-g0.
5. Inverse-mix the target using g0: `(B0',B1')=g0^(-1)*(B0,B1)`.
   Reject this branch unless det(B0')=+1 or -1. Otherwise form the
   integral matrix C=(B0')^(-1)*B1'. Ask whether C and M are similar
   over Z. Accept the original problem iff at least one branch succeeds.

There are at most n integral-similarity queries. Changing g0 to -g0
negates both mixed slices and leaves C unchanged, so no additional query
is needed for the other sign.

## Correctness And Witness Interface

A genuine transporter satisfies

```
N=R^(-1)*(a*I+b*M)^(-1)*(c*I+d*M)*R.
```

Therefore `(c+d*alpha)/(a+b*alpha)` is a root of h in K and the correct
projective line is enumerated. Inverse mixing gives B0'=L*A0*R and
B1'=L*A1*R, hence C=R^(-1)*M*R and B0' is unimodular. This proves
completeness without an unknown target slice as advice.

Conversely, if a surviving branch has C=S*M*S^(-1), take

```
L=B0'*S*A0^(-1),       R=S^(-1).
```

These are integral unimodular matrices and satisfy both slice equations.
This proves soundness. The witness conversion is polynomial in the size
of the supplied representation of S. It does NOT guarantee polynomial
size for an expanded integer S; see INTEGRAL_SIMILARITY_OUTPUT_SIZE.md.
Straight-line arithmetic representations stay compact under these
formulas, but their general bit-level consumption is a separate obligation.

Input entries with B bits lead to polynomial-bit rational inverses and
characteristic polynomials (a safe coefficient bound is
O(n^2*(B+log n))). Field degree remains n. Number-field factorization,
rational kernels, denominator/gcd normalization, determinant tests and
inverse mixing all have polynomial bit cost in the explicit input.
No degree-n! Galois closure or growing-variable polynomial-system search
is required.

There is a direct bound on root-coordinate denominators as well. Put
D=abs(det B0), Delta=disc(f), and write beta=sum_j x_j*alpha^j. Both
alpha and D*beta are algebraic integers. The trace system
`D*G*x=v`, with `G_ij=Tr(alpha^(i+j))` and
`v_i=Tr(D*beta*alpha^i)`, is integral and det(G)=Delta!=0. Coordinate
denominators therefore divide D*Delta. Root and cofactor bounds give
polynomial bit lengths for the numerators. This avoids assuming that a
small algebraic root automatically has small coordinates in any basis.

Primary background for the factorization step is
[Landau's number-field factorization algorithm](https://doi.org/10.1137/0214015)
and [Lenstra, Section2.9](https://arxiv.org/pdf/math/9204234).
Lenstra's [Theorem4.5](https://ir.cwi.nl/pub/2541/2541D.pdf) explicitly
gives polynomial-time factorization over an algebraic number field.
Classical Mobius equivalence algorithms are also discussed in
[Lercier--Ritzenthaler--Sijsling, Sections2A--2B](https://msp.org/obs/2013/1-1/obs-v1-n1-p23-p.pdf).
The exact reduction above does not assume that every binary-form
equivalence lifts to a tensor equivalence: the integral-similarity query
is precisely the missing lattice test.

## Why Maximal-Order PIP Alone Is Not The Endpoint

For T=M or C, set D_T=[e1,T*e1,...,T^(n-1)*e1]. Irreducibility makes
every nonzero vector cyclic, so D_T is invertible. Identify the companion
representation with K and define the full Z[alpha]-lattice
I_T=D_T^(-1)*Z^n. Then

```
C similar to M over Z  <=>  gamma*I_M=I_C for some gamma in K^*.
```

This follows because an intertwiner in companion coordinates commutes
with multiplication by alpha and is therefore multiplication by an
element of K. Polynomial-bit bases are computable by rational linear
algebra. These are not automatically invertible ideals of O_K.

With an additional verified O_K-stability promise for both lattices,
one can test principality of I_C*I_M^(-1). Without it, extending to O_K
forgets conductor and local-lattice information. Even after finding
gamma0*O_K*I_M=O_K*I_C, one still needs

```
exists u in O_K^*: gamma0*u*I_M=I_C.
```

For example, in Q(sqrt(5)), Z[sqrt(5)] and O_K extend to the same
O_K-ideal but are not homothetic: their multiplier orders differ.
Multiplication by sqrt(5) has matrices
`[[0,5],[1,0]]` and `[[-1,2],[2,1]]`. These have identical determinant
forms. This is a degree-two counterexample to dropping lattice data,
not an instance of the n>=3 projective-line proof.

BHJ2022v3 Theorem9.14 includes the necessary broader arithmetic reduction;
Corollary9.16 already states quantum polynomial time for integral similarity.
Composing a decision implementation with the preprocessing above transfers
its decision complexity. It is not a new quantum mechanism, and the
expanded-witness caveat must not be erased by citing the corollary.
[Versioned source](https://arxiv.org/pdf/2202.03526v3).

## Decision And Falsifiers

Do not prioritize the unmarked mixing layer of this promised family as a
new quantum bottleneck. It is classical preprocessing. No novelty claim
is made for this reduction; nearby binary-form and ideal correspondences
are existing machinery.

The argument is falsified if any genuine transporter is missing from the
field-root enumeration, the rational kernel has two independent invertible
solutions for n>=3, or the inverse-mixing reconstruction fails. Exact
controls are in `tests/test_unmarked_pencil_reduction.py`. The theorem,
not finite experiments, establishes completeness and asymptotic cost.

Removing the supplied unimodular slice, allowing reducible/singular
determinant forms, or adding geometric metric constraints changes the
problem. These are not solved or proved hard here. Before selecting one,
state what mathematical information is lost and check existing integral
module and arithmetic-orbit algorithms rather than adding an oracle wrapper.
