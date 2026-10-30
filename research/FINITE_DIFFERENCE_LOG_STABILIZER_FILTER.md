# Finite-Difference Logarithms: An Exact Obstruction

30 October 2026. Bounded exact regression controls, not a candidate, a new
algorithm, a hardness result, or a general stabilizer implementation.
This is a counterexample to a tempting extension of the classical filters
in SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md,
POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md, and
ITERATED_QUADRATIC_JET_FILTER.md. It does not invalidate those guarded filters.

## 1. Tempting Generalization And Decision

For an order-p substitution operator T in characteristic p, N=T-I satisfies
N^p=0. Its finite logarithm is well-defined:

    L_T = sum_(j=1..p-1) (-1)^(j+1) * (T-I)^j / j.

Moreover L_T=N*Q(N), where Q(0)=1. Since N is nilpotent, Q(N) is invertible,
so ker(L_T)=ker(T-I). Unlike an ordinary first derivative, this operator
has the EXACT finite-invariance kernel for this one group element.

It is nevertheless UNSOUND to compute such logarithms on an ambient Lie
basis, learn their linear relations on F, and interpret that linear kernel
as log(Stab(F)) using only p>class(Gamma). The induced logarithms need not
depend linearly on the ambient Lie coordinates. The counterexample below
has class ONE, exponent p, matrix dimension FOUR, and p>4. Even the
original matrices have square-zero augmentation algebra.

## 2. Public Circuit And Full Stabilizer

For any prime p>=5, let

    g(a,b,c) = I + a*E14 + b*E24 + c*E34,   a,b,c in F_p,
    Gamma = {g(a,b,c)} = (C_p)^3.

Its forward action is

    (x,y,w,z) -> (x+a*z, y+b*z, w+c*z, z).

The formal stabilizer is unchanged if inverse substitutions are used.
Write u=x-y and v=y-w, and supply the public circuit

    F = u^(p-1)*v.

Repeated squaring builds this circuit in O(log p) arithmetic gates. Its
formal degree is p. Thus numeric p and degree can already be exponential
in circuit size; the example does not require dense input coefficients.

The EXACT full stabilizer is

    H = {g(a,a,a) : a in F_p}.

Proof: substitution sends F to

    (u+(a-b)*z)^(p-1) * (v+(b-c)*z).

In the polynomial UFD F_p[x,y,w,z], these are distinct irreducible linear
factors: the first has a nonzero x coefficient and the second does not.
Their multiplicities p-1 and 1 are distinct. Equality with u^(p-1)*v
therefore forces the first factor to be associated to u and the second
to v. Comparing their normalized x and y coefficients forces both
association scalars to be 1. Hence a=b=c. Conversely those equations fix
u and v separately, proving sufficiency. This proves the full formal
stabilizer, not just a subgroup or an evaluation-based guess.

This is an EASY FACTORIZATION FAMILY: its exposed factors give the two
linear equations a=b and b=c immediately. No hardness or advantage follows.

## 3. Actual Finite Logarithms And False Rejection

Let T_x,T_y,T_w denote substitution by g(1,0,0), g(0,1,0), g(0,0,1),
respectively. Define L_x,L_y,L_w using the actual finite logarithm above.
Their values on F are

    L_x F = -z*u^(p-2)*v,
    L_y F =  z*(u^(p-2)*v + u^(p-1)) + z^p,
    L_w F = -z*u^(p-1).

To derive these identities, on a univariate polynomial of degree <p the
truncated translation logarithm is z*d/dy: the exponential/logarithm
identities truncate before any noninvertible factorial is needed. On
y^p, however, (T_y-I)y^p=z^p and (T_y-I)^2 y^p=0, so L_y(y^p)=z^p.
Consequently on degree <=p,

    L_y F = z*partial_y(F) + z^p*D_y^(p)(F),

where D_y^(p) is the Hasse derivative, the coefficient of t^p in
F(x,y+t,w,z). The y-degree-p coefficient of our F is 1, whereas its
x and w degrees are below p. This gives all three formulas.

For the basis-linear combination one obtains

    (a*L_x+b*L_y+c*L_w)F
      = z*((b-a)*u^(p-2)*v + (b-c)*u^(p-1)) + b*z^p.

Since u,v,z are independent coordinates and p>=5, the z^p coefficient
first forces b=0, and the remaining two distinct monomials force a=c=0.
Thus the basis-linear kernel is TRIVIAL, although |H|=p. In particular,

    (L_x+L_y+L_w)F = z^p != 0,
    log(T_x*T_y*T_w)F = 0.

The true symmetry g(1,1,1) is falsely rejected. This is not another raw
gradient counterexample: every individual finite logarithm has the correct
finite-invariance kernel. It is their proposed LINEAR combination in
ambient group coordinates that is unsound.

## 4. General Direction And Nonlinear Carry

For a direction (a,b,c), take L_g to mean the finite logarithm of its
actual substitution operator. Then

    L_g F = z*((b-a)*u^(p-2)*v + (b-c)*u^(p-1))
              + z^p*(a-b)^(p-1)*(b-c).

Indeed the coefficient of t^p in

    (u+t*(a-b)*z)^(p-1) * (v+t*(b-c)*z)

is z^p*(a-b)^(p-1)*(b-c). Applying the preceding degree-p translation
calculation along this direction gives the formula. The zero direction
is immediate. The degree-p Hasse contribution is nonlinear in a,b,c;
replacing it by the basis-linear value b*z^p is exactly the error.

Extending the evaluation field cannot repair this identity failure.
An exact dependence test, or a successful extension-field PIT procedure,
would correctly recover the WRONG basis-linear kernel. The nonzero
polynomial z^p is already detected at z=1. No distinction between formal
polynomials and base-field functions is being exploited to hide the defect.

## 5. Module Action Length, Not Just Group Class

Let M=span_(F_p){T_g F:g in Gamma} and let I be the augmentation ideal
of F_p[Gamma]. Put N_x=T_x-I, N_y=T_y-I, N_w=T_w-I. Then

    N_w F = -z*u^(p-1),
    N_x^(p-1)*N_w F = -(p-1)!*z^p = z^p != 0.

The last equality uses Wilson's theorem. Thus I^p M != 0.

Every translate of F has total degree at most p in the MOVING variables
x,y,w, with coefficients in F_p[z]. Each generator difference N_i lowers
this moving-variable degree by at least one or annihilates the polynomial.
It follows that every product of p+1 generator differences kills M.
The three N_i commute and generate I as an ideal, so I^(p+1)M=0. Together
with the witness this gives action length exactly p+1, although Gamma
has class 1. The claim concerns total moving degree, not total degree
including the invariant z coordinate.

The published module-level Lazard correspondence explicitly bounds BOTH
the group class c and the module action length d by c,d<p:
[Garaialde Ocana and Gonzalez-Sanchez, Transporting cohomology in Lazard
correspondence, Theorem 6 and Section 5](https://arxiv.org/pdf/1405.4654).
Our module violates this separate action-length premise. Merely bounding
the original matrix-group class does not justify logarithm linearity on
its polynomial module. This reference is a premise check, not a claimed
general algorithm for finding a short module filtration from a circuit.

## 6. Paid Costs And Bounded Regression

For a general order-p substitution, expanding the finite logarithm gives
a linear combination of at most p translates T^k F, 0<=k<p. A reference
evaluation therefore uses O(p) original circuit evaluations, plus matrix
action costs and, for example, O(p^2) scalar work to form coefficients.
This is NOT a poly(log p) algorithm. The executable instead repeatedly
applies T-I to explicit sparse coefficient dictionaries and accumulates
the powers with the actual modular coefficients (-1)^(j+1)/j. Its cost
also pays for intermediate sparse supports; it is not claimed to meet
the circuit-evaluation reference bound.

The executable accepts ONLY p=5,7,11, with no cap override, and public
polynomial operations reject total degree >p. It checks all p^3 directions
against the actual finite action, the displayed nonlinear formula, and
the individual-kernel equivalence. The basis-linear kernel is computed
from the actual logarithms, not from the displayed formulas.

For the upper module-length certificate it computes all commuting mixed
products N_x^i*N_y^j*N_w^k F with i+j+k=p+1: binomial(p+3,2) products.
Since the N_i commute, vanishing on F implies vanishing on every translate
and hence on M. The nonzero order-p witness is separately computed by
actual successive differences. These finite controls corroborate the
general proof; they do not replace it.

Implementation: theorems/finite_difference_log_filter.py. Tests:
tests/test_finite_difference_log_filter.py. The standalone module prints
exact JSON to stdout only; no CLI, registry, or candidate record is updated.

    python -B -m theorems.finite_difference_log_filter
    python -B -m pytest -p no:cacheprovider -q tests/test_finite_difference_log_filter.py

This is a regression against a false generalization, not a new stabilizer
algorithm or a residual hard family.
