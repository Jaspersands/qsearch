# Universal Right-Fiber Cocycle Refinement

2026-10-22. This pass supplies a direct algebraic derivation, universal
coefficient certificates and formal operator-specialization lemmas for
the general induced cocycle. It does not implement the complete quantum
receiver or reduce its erasure-tree cost. Metabelian BCH formulas are
established mathematics; compare
[Kurlin's free-metabelian BCH formula](https://arxiv.org/pdf/math/0606330).
The contribution here is a simpler, independently checkable refinement
of this project's source and compiler, not a claim of new Lie theory.

## Question And Result

Does the public compiler compute the actual right-fiber cocycle for
EVERY admissible nilpotent Lie algebra, including nonsplit extensions,
or does agreement only hold in the filiform controls?

Let N be nilpotent of class <=k, with an abelian ideal I containing N'.
Choose any A,X in N and B in I. On I put R=ad(A), S=ad(X), C=[A,X].
Jacobi gives [R,S]z=[[A,X],z]=0 for z in I. Thus R,S commute ON I,
although ad(A),ad(X) need not commute on all of N. No Lie-algebra splitting
or commuting quotient-section image is assumed.

For p>k, the right-fiber cocycle has the explicit finite expression

    log(exp(-A-X) exp(A+B) exp(X))
      = sum_(i+j<=k-1) (-1)^(i+j) R^i S^j B / ((i+1)! j!)
      + sum_(i+j<=k-2) (-1)^(i+j) R^i S^j C / ((i+1)! j! (i+j+2)).

There are exactly k^2 universal operator terms. Each denominator divides
k!, so all are invertible when p>k. These are scalar divisions only:
there is NO inverse of R or S, which are generally singular/nilpotent.
Notation involving phi(z)=(exp(z)-1)/z below means its power series,
not matrix division.

## Derivation Without Fitting

First work with formal series in characteristic zero, modulo Lie degree
>k. Let g(t)=exp(-t(A+X)) exp(t(A+B)) exp(tX). Its abelian-quotient
coordinate is zero, so g(t) belongs to exp(I). Set K(t)=log(g(t)).
Since I is abelian, K'(t)=g'(t)g(t)^(-1). Product differentiation gives

    K'(t) = -(A+X) + exp(-t ad(A+X))
                        (A+B+exp(t ad(A+B)) X).

On I, ad(A+B)=R and ad(A+X)=R+S. The first commutator of A+B with X
is C-SB; each subsequent commutator is an application of R. Therefore

    K'(t) = exp(-t(R+S)) (B + t phi(tR)(C-SB))
          = exp(-t(R+S)) B + t exp(-tS) phi(-tR)(C-SB).

Commutation is used only for the actions on I. Write the proposed K(t)
as sum b_ij t^(i+j+1) R^i S^j B plus
sum c_ij t^(i+j+2) R^i S^j C. The entire differential identity becomes

    (i+j+1)b_ij = (-1)^(i+j)/(i!j!) - [j>0] b_(i,j-1),
    (i+j+2)c_ij = b_ij,
    K(0)=0.

The displayed coefficients satisfy these recurrences identically.
Uniqueness degree by degree proves the formula, then t=1 gives the
desired word. This is an exact formal argument, not numerical integration.
All surviving coefficients lie in Z[1/k!]. The corresponding universal
Lie identity reduces modulo every p>k and identifies the Lazard group
word there. Differentiation is not being used to invert degree p in
characteristic p; truncation and denominator control precede reduction.

## Why The Coefficient Certificate Is Universal

Use the graded Lie algebra with generators A,X and abelian module basis

    B_ij, i+j+1<=k;    C_ij, i+j+2<=k.
    [A,X]=C_00;
    [A,B_ij]=B_(i+1,j), [X,B_ij]=B_(i,j+1),
    [A,C_ij]=C_(i+1,j), [X,C_ij]=C_(i,j+1).

All brackets of module elements vanish; terms past the degree bound are
zero. The two shift actions commute, which verifies Jacobi. The
action/curvature Jacobi condition is RS=SR; repeated A or X cases cancel
by alternation. Positive grading makes the discarded high-degree part
an ideal. This model has dimension k^2+2.

For ANY admissible N and choices A0,X0,B0, map A to A0, X to X0,
B_ij to ad(A0)^i ad(X0)^j B0 and C_ij to the same actions on [A0,X0].
Ideal membership, commuting actions and class-k nilpotence prove that
this map preserves every bracket, including truncation. Hence it is a
Lie homomorphism. It need not be injective and the target may have any
dimension. Equality in this model therefore specializes to ALL such
targets, not just the model's own group.

The function word_normal_form(k) evaluates the independently certified
universal free-associative exp/log Lie word in this module. It must equal
every coefficient of the closed formula. The live artifact verifies k=1,...,7:

| k | Closed operator terms | Existing right-nested word terms |
| --- | ---: | ---: |
| 1 | 1 | 1 |
| 2 | 4 | 7 |
| 3 | 9 | 23 |
| 4 | 16 | 63 |
| 5 | 25 | 179 |
| 6 | 36 | 505 |
| 7 | 49 | 1468 |

These are universal rational identities at each listed class, not tests
at finitely many field points. The separate coefficient-ODE verifier also
checks classes 8,16,32,64 without constructing their exponential words.
The written derivation covers arbitrary k; do not relabel an ODE-only
check as an independently expanded word certificate at k=64.

## Connection To The Public Compiler

The source uses A=s(pr_A Q), B=Q-A, X=s(x). The formula is valid for this
choice without accessing Q. Compile A and B as formal log-Q coordinate
variables, X as public carrier variables, and use only the public Lie
structure tensor to implement R,S and C. The new cocycle_template does
exactly this. The function lie_word_cocycle_template retains the older,
independent exp/log-word implementation as an audit reference, not a
runtime fallback.

Polynomial extension and substitution preserve the universal identity.
Consequently substituting the common FORMAL potential coefficients,
Q(Y+s*q), and the public affine carrier L^-1(t,zeta) gives the actual
full aligned cocycle polynomial, coefficientwise. Character projection
and the NEGATIVE sign produce the phase already identified by the
original-oracle source theorem. No hidden coefficient values,
interpolation, new quantum access or favorable-label selection are introduced.

This explains the support directly. Each B term has i+1 Q factors
and j carrier factors. Each C term has i+1 Q factors and j+1 carrier
factors. There is at most one ideal coefficient, every term has a Q
factor, and pure-A terms require a carrier factor. Substitution therefore
gives q degree <=hD and jet degree <=k-h at parameter degree h. The
previous resource certificate's support assumptions remain unchanged.

If B lies in N', it starts at lower-central degree two rather than one.
Its terms with i+j>=k-1 vanish, proving the stronger k-1 total degree for
the B contribution in that case. This observation is not used to silently
change the conservative resource artifact or full weighted phase degree.

## Machine-Checked Boundary

Formal/InducedCocycleOperators.lean proves, for arbitrary Lie algebras
over a field and an explicitly abelian ideal containing all brackets:

- Restricted adjoint actions commute.
- Normal-form A and X action rules, and module-module bracket zero.
- The full coordinate bracket needed for specialization.
- Iterated ad(A+B) on X reduces to ad(A)^n(C-SB).
- Lower-central membership and vanishing past the declared class.

These justify specialization and truncation, independently of the
Python structure-tensor examples. They do NOT formalize exponential
differentiation, Lazard correspondence, rational coefficient-checker
execution, polynomial compiler code extraction or the entire quantum
controller. The source-to-compiler refinement now has a written universal
algebraic proof plus coefficient certificates and formal specialization
lemmas, but not one end-to-end Lean theorem.

## Falsification And Research Decision

A nonsplit universal extension is used for whole-coefficient compiler
comparisons. Its C_00 coordinate in [A,X] is one, while [A,I] and [X,I]
have zero C_00 coordinate. Thus changing the section by ANY ideal offsets
cannot make its image commute. This rules out accidental reliance on
the semidirect-product structure of the earlier filiform fixtures.

Nonabelian I really breaks the formula: inside ut_5 take
A=E12+E34, X=E23+E45, B=E13. Then [[A,X],B] is nonzero, R,S do not
commute on I=N', and the closed formula disagrees with exact matrix
exp/log over F_101. This is a counterexample to dropping the premise,
not a new HSP candidate or a limitation on other quantum methods.

Other controls perturb one rational coefficient, remove a term, duplicate
a key, use a bad characteristic, change the public section and ideal
basis, and disable the exponential-word compiler during the new backend.
The existing original-oracle, aligned-phase, Taylor-pullback, higher-degree
merge and actual c9 ambient tests remain necessary integration evidence.
The c9 witness now compares every public template coefficient between
both backends at p43 and p2^127-1, in addition to its matrix exp/log controls.

This removes a concrete mathematical ambiguity in the general compiler.
It does NOT reduce quantum samples, diagonal-system arities, hidden class
dependence or the need for fresh complete-instrument execution. No new
classical separation, external application or novelty claim follows.
The next research work should address the complete adaptive receiver or
a justified way around its giant tree, rather than another local cocycle
example. General SDE and physical synthesis remain implementation gaps.

## Reproduce

    python -m theorems.induced_cocycle_formula --write
    python -m pytest -q tests/test_induced_cocycle_formula.py -W error::RuntimeWarning
    cd formal
    lake build --wfail

No central registry, qsearch/UI admission, commit or push is part of this
pass. This is algebraic verification for an unadmitted research route.

Verified: 539 connected Python tests pass in 157.18s with RuntimeWarning
fatal, including 20 new tests. Two final strengthened c9 witness checks
pass in 3.78s. Full cached Lean build with warnings fatal passes (3467 jobs)
and all six new axiom guards pass. Syntax, formal crosscheck, site
JavaScript/site checks, registry validation and whitespace pass. Full
repository Python suite not run. All owned processes are terminal.
