# Classical Orbit-Module Filter For Succinct Polynomial Symmetry

2026-10-22. A written classical reduction with an executable capped
representation learner and independent exact controls. Not a new quantum
algorithm, an asserted novel classical theorem, or a general implemented
matrix-group stabilizer solver.

2026-10-22 follow-up: MOORE_GRADIENT_CLASSICAL_FILTER.md removes the
small-orbit-rank requirement for scalar Moore forms, recognizing their
controlling subspace semantically from the public circuit. In a fixed
class-nine family the orbit rank is exactly10^m, but this classical
recognizer and a known subspace-stabilizer reduction still apply. Do not
use a rank-cap failure to rescue these families.

## 1. Question And Decision

Does high formal degree rescue the circuit-stabilizer application in
SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md from classical algorithms?
Not when the orbit of the polynomial spans a small vector space. We can
DISCOVER that space from the public circuit using extension-field
evaluation, without listing monomials, the group, or the polynomial orbit.
This covers cases where both existing derivative guards fail.

The strongest control uses the actual class-nine, derived-class-four
ambient group already used in the provisional HSP theorem. A formal
polynomial of degree 11,966,490,760,401 has a 10-dimensional orbit span.
All learned generator identities are independently verified as formal
identities by exterior-power coordinates. Its symmetry problem reduces
classically to a 20-dimensional faithful matrix vector stabilizer.
It is NOT a hard application for the proposed quantum algorithm.

The useful general output is the classical filter, not this example.
The examples are falsifiers of bad hardness arguments, not newly generated
oracle problems. No candidate or central negative-result record is admitted.

## 2. Input And Access Model

Input consists of a prime p; r generators of Gamma <= GL(D,p); a public
polynomial circuit C over F_p; a valid formal total-degree upper bound
Delta; an integer rank cap R>=1; and an error budget 0<epsilon<1.
The circuit can be evaluated over any explicitly constructed extension
of F_p. For ordinary division-free binary circuits the syntactic degree
bound has polynomial bit length, even if Delta is exponential in size.

Write (T_g F)(x)=F(g^-1 x) and

```
M = span over F_p {T_g F : g in Gamma}.
```

The discovery procedure applies to arbitrary supplied matrix groups.
The efficient stabilizer conclusion below needs the additional solvable
group/prime-factor premise. In particular it applies to matrix p-groups
in characteristic p; it does not need a nilpotency-class bound, exponent
p, p>D, a derivative degree guard, or an exposed Frobenius factorization.

This is NOT legal for a hiding oracle accessible only on group elements,
or a function defined only by its values on F_p^D. Such an oracle does
not automatically evaluate a public polynomial over extension fields.
The same public circuit is available to both competitors in this
application. This access distinction is essential to the classical claim.

## 3. Discovery Algorithm And Error Proof

Set T=1+rR. Choose E=F_q, q=p^k, with k>=1 and

```
q >= Delta*T/epsilon.
```

For Delta=0 use k=1. Keep an ordered list of basis polynomials
B_i=T_(g_i) F, represented only by the public D-by-D matrices g_i and
their inverses. Keep evaluation points z_l in E^D. Expand each evaluation
B_i(z_l) into its k coordinates over F_p, and concatenate these
coordinates into a sketch v_i. ALL coordinate solving is over F_p,
not over E. Using E-coefficients could change the orbit module.

Begin with candidate F. For every newly accepted basis element T_g F,
enqueue T_(a g) F for each original generator a. Process as follows.

1. Evaluate the candidate at all stored points and solve whether its
   sketch is in the F_p-span of existing basis sketches.
2. If it is outside that span, the actual polynomials are independent.
   Insert it. If this would give R+1 basis elements, return
   RANK_CAP_EXCEEDED with the exact evaluation-rank witness.
3. Otherwise fix the unique candidate coefficients lambda FIRST. Draw a
   fresh independent uniform z in E^D, and evaluate
   P(z)=T_g F(z)-sum_i lambda_i B_i(z). Append z to all sketches.
   A nonzero value proves independence and invokes step 2. A zero value
   provisionally accepts the polynomial relation.
4. At queue exhaustion, assemble each generator's action on the basis
   from those relations. Earlier coordinate vectors are padded by zeros
   when the basis has grown. No unprocessed generator image is omitted.

Every inserted basis is certified independent by an evaluation matrix.
That remains true even on a history containing a missed identity test.
The R+1 output is therefore a genuine rank LOWER bound, not a probabilistic
failure to find a smaller representation. It is not a hardness bound.

There are at most T processed candidates, and at most T fresh identity
tests. Conditional on the complete past, a tested lambda and hence P are
fixed before the new point is chosen. A nonzero P has degree <=Delta and
vanishes with probability at most Delta/q. A first-error union bound
gives probability at most T*Delta/q<=epsilon of any false dependence.
There is no union bound over all possible coefficients, group elements,
or adaptive histories. The new point must not be reused to SELECT lambda.

If no false dependence occurs, every accepted relation is an identity,
and closure under the generators is exact. The span contains F and is
generator-invariant. Each generator acts injectively on polynomials;
its restriction to the finite-dimensional span is therefore surjective.
Thus the span is invariant under inverse generators as well and equals M.
Consequently the returned matrices rho(a) define the actual representation
of Gamma on M, with the original F represented by the first basis vector.
If F=0, the module is zero-dimensional and the whole group stabilizes it.

This gives two distinct outputs: exact R+1 independence, or a Monte Carlo
closed representation. An exact rank witness does NOT certify closure.
The tests deliberately force every sample to zero: the learner can then
mistake a nonzero polynomial for zero, while the empty independence
certificate is still valid. The separate formal checker rejects it.

## 4. Cost And Faithful Stabilizer Reduction

The extension degree is

```
k = O(1 + (log(max(1,Delta)) + log(T) + log(1/epsilon))/log(p)).
```

There are at most T points, R basis elements on a closed run, or R+1
on a rank-capped run. Sketch linear algebra, evaluation of the original
circuit at matrix-transformed points, and matrix multiplication/inversion
are polynomial in the circuit/input size, D, r, R, log(p), log(Delta),
and log(1/epsilon). Even naive repeated evaluation uses only polynomially
many calls. No circuit substitution tree or coefficient list is expanded.

Extension-field construction also costs resources: standard randomized
irreducible-polynomial construction with verification suffices. The
executable uses FLINT's field constructor and verifies its modulus. It
does not implement a separately capped field-construction controller, and
its evaluation counter excludes construction and linear-algebra work.

The orbit action rho can have a kernel, even the WHOLE nonabelian group.
Do not solve the problem in the quotient and silently lose its preimage.
Instead construct the faithful public representation

```
rho_tilde(g) = diag(g, rho(g)),     v = (0_D, e_0).
```

The first block is the original supplied matrix, so rho_tilde is faithful.
Its vector stabilizer is precisely rho_tilde(Stab_Gamma(F)). Projecting
the returned subgroup generators onto their first blocks recovers the
original stabilizer, without a new kernel or constructive-membership task.
For F=0 use v=0_D and retain just the original block.

[Luks, Computing in Solvable Matrix Groups, Theorem 3.2(5)](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
provides the published vector-stabilizer dependency for solvable matrix
groups, polynomial in the matrix dimension, field bit length, and the
largest group-order prime other than the characteristic. For a p-group
over F_p the last parameter is bounded. The faithful block construction
preserves the group and this premise. The cited conference text announces
some structural proofs for a fuller version; this pass does not reprove
its matrix-group algorithms. This backend is NOT implemented here.

Hence a polynomial orbit-rank bound supplies a randomized classical
polynomial-time route for this circuit problem, conditional only on the
stated published dependency and ordinary arithmetic/PIT contracts. The
orbit-span and identity-testing ingredients are standard; no novelty
claim is made for their combination.

## 5. Independent Exact Controls

For a k-element coordinate subset I define the Moore minor

```
F_I(x) = det(x_j^(p^i))_(0<=i<k, j in I).
```

It has degree sum_(i<k) p^i. Repeated Frobenius powering and determinant
evaluation take polynomial time in k and log(p). The branching Gaussian
evaluation routine computes this known polynomial at every point,
including singular matrices; a division-free determinant circuit is also
available. An arbitrary branching callback is NOT a polynomial promise.

For base-field matrices h, Frobenius commutes with their coefficients.
Cauchy--Binet gives

```
F_I(g^-1 x) = sum_(|J|=k) det((g^-1)_(I,J)) F_J(x).
```

Distinct F_J have disjoint monomial supports, so these coordinates are
formally linearly independent. The checker computes these small minors
and verifies every learned generator image coefficient by coefficient.
It is independent of the random evaluation sketch and certifies the
complete representation for these controls. Its binomial(D,k) cost is
explicit; the general learner does not enumerate those coordinates.

| Control | Degree | Learned Rank | Consequence |
| --- | ---: | ---: | --- |
| F5, D=6, I=(0,1,3,4,5), UT3 on first three coordinates | 781 | 3 | Lift degree k=p fails old no-carry guard; orbit filter succeeds |
| p=2^127-1, D=3, I=(0,1), UT3 | p+1 | 3 | Extension degree 2; base-field rather than extension-field linear algebra matters |
| F43, D=10, I=(0,...,8), actual class-nine group | 11,966,490,760,401 | 10 | Old mixed guard 43>9*9 fails; exact 20-dimensional faithful reduction |

The third group is generated by exp(J) and exp(sum_i i^2 E_(i,i+1)),
J=sum_i E_(i,i+1), with i=1,...,9. Existing independent Lie calculations
give dimension 19, class 9, derived dimensions [19,17,10,0], and class 4
for its metabelian derived subgroup. The module search processes 21
candidates, not its 43^19 elements. A regular unipotent generator already
makes the 9th exterior-power orbit cyclic of dimension 10; the result is
not a dimension inferred from numerical fitting.

An exhaustive UT3(F5) check verifies ALL 125 stabilizer decisions for
the 2-by-2 minor, including noncommuting generator actions. The stabilizer
is b=c=0 in [[1,a,c],[0,1,b],[0,0,1]], a nonnormal subgroup. Constant and
invariant-coordinate controls test the faithful-block requirement.

**Opposite control.** For F=x0^(p-1) in UT3(F_p), the orbit span has
dimension p(p+1)/2: expansions of (x0+u*x1+v*x2)^(p-1) have every
multinomial coefficient nonzero, and parameter monomials of individual
degree <p are independent functions on F_p^2. At p=127, cap 5 returns
six exactly independent translates. Nevertheless unique factorization
immediately gives the stabilizer a=c=0. Exceeding a rank cap is neither
dequantization resistance nor evidence that a quantum algorithm is needed.

## 6. Critique, Remaining Work, And Reproduction

- A small circuit need not have small orbit rank. The opposite control
  proves this filter cannot decide all succinct-polynomial cases.
- Large rank still does not imply hard symmetry recovery. Factorization,
  derivatives, deflation, and construction-specific attacks must remain.
- The learner trusts the formal-degree and extension-evaluator contract.
  Invalid bounds, field-valued lookup tables, hidden-H-generated circuits,
  or an evaluator that changes between calls invalidate the theorem.
- Seeded runs are reproducible diagnostics. Their printed ideal-random
  bounds are not probabilistic certificates for chosen seeds. The Moore
  examples instead pass a separate exact formal identity checker.
- The learned representation can be wrong on a missed PIT event. Singular
  learned generator matrices cause explicit failure, not promotion, but
  nonsingularity alone does not establish correctness.
- No general stabilizer backend, complete quantum receiver, application
  hardness proof, or novelty certificate was created in this pass.

New code: theorems/polynomial_orbit_module.py. New tests:
tests/test_polynomial_orbit_module.py. Live diagnostic artifact:
research/classical_baselines/polynomial_orbit_module.json.

```
python -m theorems.polynomial_orbit_module --write
python -m pytest -q tests/test_polynomial_orbit_module.py -W error::RuntimeWarning
```

Do not make more high-degree determinant families into quantum candidates.
The next useful application must survive this filter AND independent
structural attacks, with its input model and meaningful output specified.
An alternative high-value task is an independent check of the provisional
HSP theorem's scope/novelty or a mechanism avoiding its enormous erasure
tree. Routine CLI/UI work does not address either scientific question.
