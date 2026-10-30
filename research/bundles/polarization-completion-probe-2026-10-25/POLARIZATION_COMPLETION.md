# Polarization Completion: A Conditional Classical Primitive, Not A Quantum Result

2026-10-25. Status: scoped deductions and exact supplied-order controls.
The new deductions below are not independently reviewed. The separate review
of the combined source/suborder chain does not review this bundle.

## Decision

The constructive question was whether one known quadratic endomorphism can
define a polarization whose geometric decomposition exposes a second,
noncommuting endomorphism. There is a precise extraction mechanism, but no
successful native algorithm or useful hitting-probability theorem. Moreover:

1. If the mechanism worked with polynomial probability, it would already be
   a CLASSICAL completion algorithm, not intrinsically a quantum advantage.
2. Small-height successes have a direct bounded-degree classical competitor.
3. The free-original-E-factor search has an even stronger small-a competitor.
4. Frobenius scalar on 2-torsion rules out new information from decomposition
   projectors altogether, at every height and number of copies.
5. Stabilizing an indecomposable surface does not turn it into elliptic
   factors. A28 returns irreducible PPAVs, not necessarily elliptic curves.

Do not extend the small-form sweep by inertia. A remaining worthwhile proposal
must exhibit a legal high-height family outside the obstruction, a reason for
noncommuting decomposition projectors, and a native sampling/cost analysis.

## Native Input And Legal Query

Let E be a supersingular elliptic curve in odd characteristic p>3. The input
contains its curve model and an efficiently evaluable nonscalar endomorphism
alpha with charged representation, degree bound, and definition field.
Only K=Q(alpha) is known, not a quaternion-order basis. Choose integers a,d>0
and beta=u+v*alpha with

    H = [[a,beta],[bar(beta),d]],     a*d - Norm(beta) = 1.

The diagonal polarization on E^2 identifies conjugation with Rosati adjoint.
Thus H is positive, integral and unimodular, and defines a principal
polarization. Its trace parameter t=a+d obeys H^2-t*H+I=0. A matrix with
nonintegral quaternion coordinates or beta outside K is not this input.

The generic converter in the adjacent smooth-repolarization bundle applies
to H directly. It does not need an unknown isogeny or weak oracle. For t>2
choose an even squarefree D>t+2 excluding p, set Q=D^2, and construct

    C^dagger C = C C^dagger = Q H8,
    F = H8^(-1) C^dagger,
    F C = C F = Q I,       F^dagger H8 F = Q I.

Here H8 is eight copies of H and X=(E^2)^8 has its old product polarization.
Use actual small r^2-torsion, including 4, to form ker(F); call the fixed-
dimension quotient interface at each r^2. This is the GENERIC prime-square
converter, not an automatic use of the later prime-only half-polarization
variant. The largest r and log(D) can be polynomial in input length, but
enumerating r^32-point kernels is a very large fixed polynomial.

Pay all field arithmetic, actual torsion construction, quotient computation,
and geometric representation costs. Keep the prime-power extension fields
separate. The expected polynomial four-square algorithm is an imported
mathematical dependency; the SymPy witness finder is only a verifier here.

The resulting known polarized quotient q:X->Y has ker(q)=ker(F). There
exists a polarized isomorphism u:Y->(E^2,H)^8 such that u*q=F. The algorithm
does not know or compute u. A28 decomposes Y into irreducible polarized
factors, with actual inclusion and projection maps.

The A18/A21/A26/A27/A28 interfaces were checked on pages 13-14 of
[Corte-Real Santos, Piasecki and Wesolowski](https://eprint.iacr.org/2026/1142).
They require represented inputs and actual kernel points. This bundle has
not executed those interfaces.

## Extraction Without Knowing The Comparison Isomorphism

For a returned projector e on Y, compute the integral map

    L = q^dagger e q
      = F^dagger H8 P F
      = Q F^(-1) P F,             P = u e u^(-1).

All entries of F and F^(-1) lie in K. Consequently L is in M16(K) if and
only if P is. Extract the corners of L using the known inclusions and
projections of the ORIGINAL E^16. An outside-K corner gamma is exactly an
endomorphism with [alpha,gamma] != 0. All maps used to compute L are known;
u occurs only in the correctness argument. Commutator equality testing must
use the charged map/degree representation, not an assumed End(E) coordinate
oracle. Also 0<=L<=Q I for the old Rosati metric, so each corner has degree
at most Q^2, giving an explicit (potentially enormous) bound.

Such alpha,gamma span the full quaternion algebra with 1 and alpha*gamma.
Integral trace/norm identities give an effective full-rank generated order.
This alone does NOT automatically provide every input of the earlier
suborder reduction, notably its supplied rational algebra dictionary to a
known source order. That conversion must be charged or independently proved.

Every geometric operation above is classical. A polynomially samplable
successful H family would therefore be a classical result first. No quantum
receiver or amplitude amplification should be attached without comparing
this same classical success probability and per-query cost.

## Falsifier 1: Small Trace Gives A Bounded-Degree Attack

Let P be any H8-orthogonal integral projector. The positive square root gives
an ordinary orthogonal projector H8^(1/2) P H8^(-1/2), hence

    ||P||_op <= sqrt(kappa(H)),
    Norm(P_ij) <= kappa(H) <= t^2.

The last inequality uses determinant one and eigenvalues lambda,1/lambda
with lambda<=t. If P is outside M16(K), one corner is a noncommuting
endomorphism of degree at most t^2.

There is a native classical exhaustive competitor polynomial in the VALUE
B=t^2 and the input length: enumerate degree<=B isogenies from the given E
and all isomorphisms of their targets back to E, checking the commutator.
For prime-to-p degrees, enumerate subgroups of E[n] and use explicit quotient
maps. Their count and torsion splitting degrees are polynomial in n, and
trial division is polynomial in B. Include inseparable Frobenius factors
when p<=B; this does not alter the polynomial-in-B qualification. Charge
evaluation/equality of alpha using its representation and degree bound.

Thus polynomial t in input BIT length cannot support a superpolynomial
separation from classical completion. This is NOT polynomial in log(t),
and is not a classical algorithm for unbounded-height inputs. The native
curve enumerator was not executed; the supplied-order probe is not it.

## Falsifier 2: The Unit-Vector Search Has A Stronger Bound

The implemented probe searches columns v=(x,y) in End(E)^2 with v^dagger H v=1.
It generates P=v v^dagger H, a projector onto a factor isomorphic to the
ORIGINAL E. Completing the square, with z=a*x+beta*y, gives

    Norm(z)+Norm(y)=a.

If both z and y commute with alpha, they are in K. Since beta is also in K,
x=(z-beta*y)/a is in K and every corner of P is in K. Contrapositively,
an outside-K projector of this type implies a noncommuting y or z of
degree<=a. Small a is therefore classically attacked even when d and beta
are huge. The certificate checker rejects beta that already supplies the
missing noncommuting information.

This is only a sufficient projector search. A polarized elliptic factor
need not be isomorphic to E. Nonfree rank-one modules are absent from this
enumeration. Failure to find a unit vector proves neither indecomposability
nor absence of useful projectors. The form box is finite as well.

## Falsifier 3: Scalar Frobenius On 2-Torsion

Assume E/F_p has Frobenius pi, K=Q(pi), and pi is scalar on E[2]. Over F_2
that scalar is 1; integrality of (1+pi)/2 is a sufficient condition. The
polarization H in M2(K) is defined over F_p. Consider the canonical primitive
polarized factor projectors of (E^2,H)^s over the algebraic closure.

Uniqueness of polarized decomposition implies Frobenius permutes these
projectors. For a projector e and its conjugate e^(p), naturality gives
pi*e=e^(p)*pi. On 2-torsion, pi=I, so e and e^(p) act identically there.
Distinct primitive factor projectors cannot do this: on nonzero 2-torsion
of the first factor one is the identity and the other is zero. Thus every
projector is Frobenius-fixed and commutes with diagonal pi. The centralizer
is M_(2s)(K), so ALL these projectors lie in the known matrix algebra.
The extraction identity then places every L in M_(2s)(K) as well.

This closes the projector-extraction route on this input subfamily for all
heights and s. It does not close other algorithms, non-Frobenius alpha,
Frobenius nonscalar modulo 2, or arbitrary automorphism extraction.

The imported uniqueness statement is Theorem 4.20 in
[Ibukiyama, Karemaker and Yu](https://arxiv.org/html/2205.13180v3#S4.SS5).
The mod-2 obstruction and its application here are our deductions, not a
claimed theorem of that paper. The local matrix test only checks the
permutation obstruction; it is not the proof of geometric uniqueness.

## Falsifier 4: Stabilization Does Not Create New Factors

By the same uniqueness statement, the primitive factors of A_H^8 are the
primitive factors of the original A_H in each copy. If A_H is an
indecomposable polarized surface, its eight factor projectors are the
known copy projections, all in M16(K). Isomorphic factors can be permuted,
but this does not create new embedded factors. Therefore stabilization
solves a representation issue, not the existence of useful projectors.

## Controls And Prior Art

The order fixture is a supplied maximal order of a 3-isogenous neighbor
in B=(-1,-p). It verifies multiplication, discriminant p^2, orientation,
and the absence of extra units. No curve equation, native torsion point,
geometric decomposition, or unknown map is produced.

- p=23, half-Frobenius orientation, a<=8: 46 forms, no outside-K free factor.
- p=47, twisted-Frobenius orientation, a<=8: 76 forms, none.
- p=47, same orientation, a<=16: 256 forms, none in the extended control.
- p=23 twisted branch has six units; excluded as an already-easy
  extra-automorphism fixture, not used as positive evidence.
- H=[[2,pi],[-pi,24]], pi^2=-47: t=26, D=30, and
  (t+2)*3+(t-2)*34=900. The generic eight-square certificate verifies.
  That checks conversion algebra, not a useful decomposition.
- The deliberately invalid H=[[1,beta],[bar(beta),1+Norm(beta)]] with
  beta outside K yields noncommuting projectors but is rejected as advice.

[Kirimli and Korpal](https://arxiv.org/html/2607.25552v1), Algorithm 1 and
Section 3.5, study refined Humbert invariants and polarization type using
explicit quaternion coordinates. Their enumeration costs include powers
of p, not a demonstrated poly(log p) algorithm from a single given
endomorphism. This is relevant structure/prior art, not a supplied native
solver for the missing input. No novelty assessment is complete.

## What Would Justify Reopening This Lead

Provide a family H(alpha) using only legal known maps, outside the
scalar-Frobenius obstruction, with a proof or targeted structural argument
that a noncommuting factor occurs with nonnegligible probability. Account
for input lengths, curve fields, converter and decomposition costs, and
the native degree-enumeration competitor. Search beyond free E-factor
unit vectors only if that family makes nonfree factors relevant.

Until then: no candidate promotion, no hardness claim, and no broadening
the search solely because a finite supplied-order test was negative.
