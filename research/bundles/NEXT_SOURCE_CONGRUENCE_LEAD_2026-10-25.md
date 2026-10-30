# Next Source Lead: Congruence Normalization At Twice The Degree

Resolution on 2026-10-25: the arithmetic construction, conditional proof
and controls are now in double-level-source-2026-10-25. The compatible
dyadic split is computed generically by idempotent lifting, not granted.
50 new tests and a 282-test scoped regression pass. Native geometry and
independent review remain unexecuted. The proposed dyadic quantum receiver
was NOT built: a stronger same-source classical digit baseline makes that
branch unnecessary. The text below is retained as the original lead, not
as current implementation status.

2026-10-25. PROPOSED NEXT PASS, not an implemented or reviewed result.
No source/registry promotion is authorized by this note. The completed
bundles remain restricted to odd degree. This records a specific route
worth trying to falsify, rather than silently extending their contracts.

## Question

Can a lift at modulus2n make the prime-only source work for EVEN n,
without weak evaluations at2 or high-order dyadic torsion points?

For even n the old odd-trace trick cannot work: S=I mod n forces even
trace. Merely applying its coprime t+2,t-2 coin argument is invalid.
The following different normalization may bypass that obstruction.

## Proposed Algebra

Lift each public M in Sp4(Z/n) to M' in Sp4(Z/2n), reducing to the SAME M.
Use the full source order's compatible abstract splitting at2n and a
bounded elementary compiler to lift M' to an integral quaternion matrix
automorphism sigma. Then

    S=sigma^dagger sigma=I+2nT0,
    H=Phi S Phi^-1=I+2 Phi T0 Phi^dagger.

In particular H-I is divisible by2 as an ACTUAL integral endomorphism;
this is stronger than pretending that division by2 is always integral.
The surface norm identity gives H^2-tH+I=0, t>=2. Since the corresponding
S is congruent to I modulo2, its Moore determinant1 forces t=2 mod4.
Put s=(t-2)/4 and A=(H-I)/2. Both are integral, and

    A^2=sH,    (A+I)^2=(s+1)H.

The coefficients s and s+1 are consecutive. Choose one odd squarefree
multiplier D, coprime to pn, larger than the uniform trace bound squared.
For s>0 let X=D mod s and Y=(D-(s+1)X)/s; for s=0 take X=D,Y=0.
Both are nonnegative and (s+1)X+sY=D. Four-square decompositions of X,Y
give eight INTEGRAL commuting coefficients of the form a_i(A+I), b_i A.
The same norm-matrix identity would give

    C^dagger C=C C^dagger=D H8,
    F=H8^-1 C^dagger,
    FC=CF=D I,   F^dagger H8 F=D I.

At an odd auxiliary prime r the matrix A is computable as (H-I)/2 modulo
r, using the same original weak data. This would require no weak Phi
evaluation at2. It does not eliminate public level-4 theta-model costs.
The case t=2 must be retained, not rejected by an old trace>=3 schema.

## Explicit Symplectic Lift To Double Level

For odd n, combine M mod n and I mod2 by CRT. For even n choose an integer
representative M and put E=(M^T J M-J)/n mod2. This is alternating.
Choose upper triangular Y with Y+Y^T=E, and solve

    M^T J X=Y mod2.

Then M'=M+nX is symplectic modulo2n: the n^2 X^T J X term vanishes at
that modulus, and the linear correction cancels E. The generic determinant
identity via the Pfaffian gives det(M')=1 modulo2n. All steps are public.

The abstract order splitting at2n is a real remaining interface obligation.
Do not substitute the old odd-prime formula that divides by2. For the
existing characteristic p=3 mod4 fixture with basis 1,i,h,ih, a possible
2-adic split is

    i=[[0,-1],[1,0]],    h=[[a,b],[b,1-a]],
    a^2-a+b^2+(p+1)/4=0 mod2^k.

Take b=(p+1)/4 mod2 and start a=0 mod2. The derivative2a-1 is odd, so
bitwise Hensel lifting determines a. Verify the ENTIRE multiplication,
involution and coordinate-isomorphism tables, not just this equation.
This fixture is not a proof of a generic full-order splitting backend.

With a generic CRT unit-pivot compiler, the36 physical-factor bound should
still hold when2 is among the factors. Centered quaternion coefficients
modulo2n have absolute value at most n; a candidate bound is

    t <= (2+4n^2 B0)^144.

No odd-trace shear should be appended in this path. Every congruence and
the bound need explicit controls before replacing an existing lift.

## Dyadic Receiver Check

If the SOURCE extension survives, the local square-unit method also has a
plausible dyadic extension. Over Z/2^e, square units have1,2,4 roots for
e=1, e=2, e>=3 respectively; their density in the full additive ring is
1/2,1/4,1/8. The unit-frequency filter costs1/2, giving correct-candidate
probability at least1/16. Root enumeration by bit lifting has at most four
branches after the initial levels; a uniform root-index register must be
uncomputed rather than left entangled.

The two-query full-source certificate and scalar-content period proof
depend only on a local ring having a unit coordinate, not on oddness.
Still check them at2 explicitly. The existing input validators deliberately
reject2 and must NOT be bypassed without a separately verified path.

## Decisive Work, In Order

1. Try to refute the integral A identity, the t=2 mod4 deduction, or the
   claimed double-level lift. Check n=2,4,6,8 and mixed prime powers.
2. Verify the2-adic order fixture and exact integral lift inverse, residue,
   Gram congruence, quadratic relation and public coefficient bound.
3. Use a ring with generator A and relation A^2=2sA+s for certificates;
   do not feed half-integral coefficients to the old integer-only schema.
4. Check odd-prime quotient kernels at nonsemisimple discriminant primes,
   with a supplied genuine EVEN-degree isogeny when feasible.
5. Test dyadic phase probability, root-index cleanup and certificates.
6. Only then write a conditional all-degree extension and update receipts.

Even success would leave the large-dimension geometric source, uniform
backend clocks, novelty and same-input classical leakage unresolved.
Do not confuse removing a self-imposed degree restriction with a Shor-level
discovery. Independent review remains the critical scientific debt.
