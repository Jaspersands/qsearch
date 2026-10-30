# Compact Pencil Norms Do Not Supply Hard Stabilizer Instances

2026-10-24. LOCAL WRITTEN PROOF with exact finite controls and a restricted
classical implementation. Not independently reviewed, machine checked,
claimed novel, or a quantum algorithm. This closes a gap left by the
previous small-factor-support filter; it does not extend that filter by
silently crossing its sharp p-factor boundary.

## Scientific Question And Decision

Can a compact product over p low-degree factors produce a hard native
polynomial-stabilizer application for the Rees HSP reduction? Its degree
and even its orbit-module dimension can be exponential in log p, while
its circuit remains small. This is a real gap in the previous sufficient
classical filters, but not evidence of classical hardness.

For an exposed, coprime polynomial pencil with sufficiently small atom
degrees, the answer is no: the stabilizer reduces to two linear
infinitesimal constraints. Importantly, the answer allows permutations of
the p factors; it is NOT the intersection of their individual stabilizers.
The large norm and its large orbit module need never be expanded.

The putative quantum route was the existing fixed extension-field
fingerprint followed by the conditional Rees receiver, with its source
and class-dependent costs retained. Each exposed norm evaluation adds
only O(log p) field multiplications to the atom evaluations; its degree
cost enters the fingerprint field's bit length, not a coefficient table.
But the classical solver below is already polynomial on the stated input
regime, so this family does not yield an exponential quantum separation.
No assumption about the receiver's correctness is used to establish that
negative application result.

## Native Input And Assumptions

Let Gamma be a finite p-subgroup of GL_D(F_p). The actual public input is
nonzero P and nonconstant Q in F_p[x_1,...,x_D], with gcd(P,Q)=1. Define

    F = N(P,Q) = product_(t in F_p) (P+tQ) = P^p-P Q^(p-1).

The task is to output generators of the FORMAL polynomial stabilizer of
F in Gamma. Substitution by g or g^-1 defines the same stabilizer. P and
Q are part of the real input expression, not hidden factoring advice for
an arbitrary circuit. Binary powering implements this expression with
O(log p) extra arithmetic gates. This is a structured mathematical input,
not a toy oracle with artificially restricted classical access.

Put a=degree(P), b=degree(Q). Require

    p > a+b+1.                                      (multiplicity guard)

The structural reduction below needs no squarefreeness of Q, no
irreducibility of any pencil member, and no bounded class of Gamma.
The implemented solver separately requires full UT_D(F_p), explicit
polynomial atoms, and

    p > max(D, (D-1)*max(a,b)).                      (Lie guard)

Both guards are strict. No speedup is claimed if either fails.

## 1. A Canonical Divisor Exposes The Denominator

Write J(F) for a gcd of all first partial derivatives. Since

    partial_j F = Q^(p-2) (P partial_j Q - Q partial_j P),

put R_j=P partial_j Q-Q partial_j P, of degree at most a+b-1.
For an irreducible h with multiplicity m in Q, coprimality implies
h does not divide P. Also m<=b<p. Writing Q=h^m U gives

    R_j = m P h^(m-1) U partial_j h + h^m (...).

There is a j with h not dividing partial_j h: an irreducible polynomial
over the perfect field F_p cannot have all derivatives zero, and a
nonzero derivative has lower total degree. Thus

    min_j valuation_h(R_j) = m-1,
    valuation_h(J(F)) = m(p-1)-1 >= p-2.

In particular the gradient is not identically zero. For any irreducible
h not dividing Q, its multiplicity in J(F) is at most a+b-1<p-2, by
choosing a nonzero R_j. Therefore the factors of J(F) with multiplicity
at least p-2 are EXACTLY the factors of Q, and their multiplicities recover
the corresponding multiplicity of Q by

    m = (valuation_h(J(F))+1)/(p-1).

This is a proof of intrinsic recovery, not an algorithm that factors the
huge derivative. Invertible linear substitution takes the gradient to an
invertible constant linear combination of its substituted coordinates.
It consequently preserves the gcd up to a nonzero scalar. Thus every
g stabilizing F sends Q to c_g Q. Since g has p-power order, c_g has
p-power order in F_p^*, so c_g=1.

## 2. Exact Pencil Stabilizer, Including Factor Permutations

With Q(gx)=Q, the equation F(gx)=F(x) becomes

    U^p-U Q^(p-1)=0,        U=P(gx)-P(x).

In the rational function field, u=U/Q satisfies u^p-u=0. Its only roots
are the constants F_p, because T^p-T splits into its p distinct linear
factors over F_p. Hence U=tQ for some t in F_p. The converse follows by
the same identity. We obtain the exact equality

    Stab_Gamma(F) = {g in Gamma: Q(gx)=Q, P(gx)=P+t_g Q, t_g in F_p}.

The translation t_g is allowed and generally nonzero. Dropping it would
incorrectly discard symmetries that permute the p factors. Q may have
repeated factors; their multiplicities were retained in the argument.

## 3. Classical Solver And Resource Accounting

Under the Lie guard, let L=log(Gamma). For full UT_D, L is the strict
upper-triangular matrix space. For a general supplied matrix p-group,
the previously proved logarithm/commutator-closure construction supplies
L; that more general backend is not implemented in this bundle.

For A in L, D_A P=gradient(P)^T A x. The desired Lie subalgebra is the
projection onto A of the linear solution space

    D_A Q=0,     D_A P=t Q,       t in F_p.

Why finite and infinitesimal conditions agree:

* If exp(A) fixes Q and adds tQ to P, its j-th power adds jtQ for all
  j in F_p. The polynomials Q(exp(TA)x) and P(exp(TA)x) have T-degree
  strictly below p. Interpolation on the p distinct scalars proves
  Q(exp(TA)x)=Q and P(exp(TA)x)=P+TtQ identically, hence the equations.
* Conversely the two derivative equations imply derivatives 0 and tQ
  along exp(TA). In degree below p their antiderivatives are uniquely
  Q and P+TtQ after fixing T=0. In particular exp(A) is a finite symmetry.

The auxiliary t is unique because Q is nonzero. Projecting the solution
space therefore loses no dimension. Exponentiating an F_p basis generates
the full stabilizer by Lazard correspondence, not just some valid members.

The executable forms exact coefficient equations, solves them over F_p,
exponentiates the answer, and independently checks Q(gx)=Q and
P(gx)-P in F_p Q for every returned generator. It does not expand F,
enumerate Gamma, enumerate p factors, or construct the polynomial orbit.
Its arithmetic is polynomial in the dense atom representation dimension,
D and log p, using standard polynomial gcd and finite-field linear
algebra. SymPy may expand expressions when creating atom Poly objects:
this is NOT a polynomial bound in arbitrary succinct atom-circuit size.
The implementation checks a primality screen; primality remains a caller
input promise. The live 127-bit instance also has a Lucas-Lehmer check.

## 4. An Exponential Orbit Is Still Classically Easy

For D>=3 choose Gamma=UT_D(F_p), P=x_0+x_1^2, Q=x_1 and
p>max(4,D,2(D-1)). Every P+tQ is irreducible, since it is monic linear
in x_0, and these are p distinct factors. Thus the previous fewer-than-p
factor argument cannot be used. The norm has formal degree 2p; its
ordinary derivative-degree guard and exposed mixed-Frobenius no-carry
guard fail.

Its orbit-module rank is at least p. Apply the p shears
x_1 -> x_1+c x_2 and project each orbit polynomial to its coefficient of
x_0. These projections are -(x_1+c x_2)^(p-1). Their coefficient matrix
is a Vandermonde matrix times the nonzero diagonal entries
binomial(p-1,j)=(-1)^j mod p, and is invertible. Independence of the
projections implies independence of the original p orbit polynomials.
For fixed D and growing p this is exponential in log p.

Nevertheless the new equations force the second row to be fixed, allow
only the x_1 entry of the first row to move, and leave UT_(D-2) on the
remaining coordinates. The exact Lie dimension is

    1+(D-2)(D-3)/2.

The live cases D=3,6,10 at p=2^127-1 return dimensions 1,7,29 without
expanding any norm. The orbit-rank lower bound at this p is a written
Vandermonde proof, not an executed p-by-p calculation. Small p controls
check that calculation independently. This does not claim every previous
classical method fails; it shows why high degree and high orbit rank
jointly do not establish hardness.

## 5. Adversarial Checks And Limits

**Dropping the multiplicity guard is false.** Set

    P=x^p-x z^(p-1),   Q=y^p-y z^(p-1).

These are coprime, but degree(P)=degree(Q)=p. Their norm is
product_(a,b in F_p)(x+a y+b z). The shear z->z+y preserves this entire
product by permuting (a,b), but does not preserve Q. With variable order
(x,z,y), this is an element of UT_3. Exact controls at p=3,5 verify the
counterexample, and the solver rejects it. Nested norms are NOT proved
hard; only this unjustified shortcut is ruled out.

**The p-group hypothesis matters.** At p=5, (x,y)->(x,2y) preserves
x^p-x y^(p-1) but does not fix y. Scalar factors may not be dropped for
arbitrary groups.

**Base-field tables give the wrong problem.** At p=7, P=x and Q=y^2+1
give a norm vanishing at every base-field point, since Q never vanishes
there. Its formal UT_2 stabilizer is trivial. The solver checks the formal
atoms and does not mistake this table for a constant polynomial.

The Lie guard, coprimality and nonconstant-denominator contract have
separate rejection tests. Failure means OUT_OF_SCOPE, not quantum
evidence. Completeness is checked on small fields by comparing the
generated group to exhaustive stabilizers of the expanded ORIGINAL norm.

## Prior Art And Next Decision

Norms and transfers are standard in modular invariant theory, not new
quantum mechanisms. See [Wehlau, modular cyclic invariants, Section 2.4](https://arxiv.org/abs/0912.1107)
and [Campbell--Shank--Wehlau, vector invariants](https://kar.kent.ac.uk/23885/1/arXiv0901.2811.pdf).
These papers contextualize the construction; they are not cited as proving
this exact algorithm or a general circuit-stabilizer theorem. The current
search did not establish novelty for the local divisor argument.

Do not respond by adding larger pencil controls as quantum candidates.
The remaining application question needs a naturally specified input
outside the proved filters and a reason its compact representation does
not expose a small classical flag. A general orbit resultant, non-pencil
norm, or hidden decomposition requires its own same-input analysis; this
pass gives no hardness evidence for any of them. The Rees theorem's
correctness, novelty and a natural hard application remain distinct
questions. No speedup, end-to-end quantum execution or publication-level
novelty certification has been established here.
