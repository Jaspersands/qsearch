# Constructing The Signed Elliptic Theta Input

2026-10-26. Constructive response to the original-curve conversion part of
Finding 3 in the independent combined-source review. This subsequent work
has not received another independent review. No native dimension-16 quotient,
canonical marked label, unknown-kernel recovery, or quantum algorithm ran.

## Result And Input Boundary

For an explicit nonsingular short Weierstrass curve E: y^2=x^3+a*x+b in
characteristic greater than three, over a represented finite field containing
E[8], construct a symmetric level-four theta embedding after at most one
further degree-four field extension, by constant-size
linear algebra and constant-degree polynomial root finding. The forward and
inverse maps preserve signed points. The curve need not be supersingular
for this conversion, though the executed controls are supersingular.

The earlier elliptic field-normalization lemma puts both supplied endpoints
over one fixed F_(q^12), with common scalar Frobenius [q^6] and full rational
8-torsion. Finite-field extension construction and embeddings are charged
classical preprocessing. They are not unknown-isogeny advice. The converter
implemented here consumes that declared field; it does NOT implement general
finite-field tower/embedding management. A missing 8-torsion field is rejected,
not silently repaired by identifying conjugate coefficients.

The purpose is to replace a representability-only appeal with an algorithm
on the actual input curve. It does not convert an arbitrary unknown surface
polarization directly; that remains the separate stabilized quotient route.

## 1. The Explicit Section Space

The known basis of L(4O) is 1,x,y,x^2. It embeds E as the complete intersection

    r(P) = (1:x:y:x^2),     r(O)=(0:0:0:1),
    r0*r3 = r1^2,
    r2^2 = r1*r3+a*r0*r1+b*r0^2.

Unlike an x-only or level-two Kummer representation, this separates P from
-P. A pair (P,Q) and (P,-Q) can have identical x-coordinates without being
related by ONE common unit scalar. The executable order-four basis control
checks this distinction. Independent point-sign loss is not the weak tuple
equivalence relation used by the source proof.

## 2. Compute Constant Torsion Without Scanning The Field

Find E[2] by rooting the cubic. The x-coordinate doubling formula is

    x(2P) = (x^4-2*a*x^2-8*b*x+a^2)/(4*(x^3+a*x+b)).

To find all preimages of an x-coordinate u, root its quartic numerator after
subtracting u times the denominator. Apply this twice to the three nonzero
2-torsion x-coordinates, always retaining E[2]. Root y^2-(x^3+a*x+b) at the
resulting 33 x-coordinates. There are 64 points including O. Check [8]P=O
for every point and that the points are distinct.

This uses 46 polynomial root calls of degree at most four, independent of q.
It is not enumeration of F_q or a large auxiliary-torsion algorithm.
Constant-degree finite-field factorization is a standard expected polynomial
bit-cost primitive. The local code uses FLINT and exact checks; timings do
not certify the implementation's asymptotic bound.

Select an E[4] basis T,U from the doubles of E[8]: both have order four and
[2]T,[2]U are independent nonzero 2-torsion points. All choices occur among
constant-size sets. No given Heisenberg matrix or hidden theta frame is used.

## 3. Recover And Certify The Translation Matrices

Translation by T preserves the linear equivalence class 4O, because [4]T=O.
It therefore induces an invertible projective linear map M_T on L(4O)^*.
For nine distinct affine points P avoiding -T, impose the linear conditions

    M_T r(P) proportional to r(P+T).

There are 16 unknown matrix entries and six cross-product equations per
point. Each cross product is a section with pole divisor at most 4O+4(-T),
of degree eight. Nine distinct zeros therefore force the identity on the
whole curve, not merely on the selected subgroup. The solution space is
one-dimensional: a nonzero map acting correctly on the nondegenerate quartic
is invertible and its projective action is determined there.

The implementation additionally verifies the identity SYMBOLICALLY in
F[x,y]/(y^2-x^3-a*x-b). Writing T=(u,v), delta=x-u, l=y-v, set

    X'=l^2-(x+u)*delta^2,
    Y'=-y*delta^3+l*(x*delta^2-X'),
    r(P+T)=(delta^4, X'*delta^2, Y'*delta, X'^2).

All six cross products with M_T r(P) reduce to zero polynomials. This also
certifies the identity on extension-field points. The projective map extends
over the affine poles; O and -T are checked separately in the finite control.
The same construction gives M_U.

## 4. Normalize The Symmetric Heisenberg Frame

In the old basis, inversion is J=diag(1,1,-1,1). Normalize each translation
matrix by a scalar so that

    A^4=B^4=I,     J A J=A^-1,     J B J=B^-1.

The scalars are among the roots of two quartics. Their existence does not need
to be imported as an unspecified model conversion. Since E[4] is rational,
the field k contains the fourth roots of unity by the Weil pairing. Every
element of k* becomes a fourth power in its degree-four extension: for
q=|k|, q^3+q^2+q+1 is divisible by four. Normalize M_T^4=cI using a root
of X^4-c^-1 in that extension, and do likewise for M_U.

For an order-four normalized A, projective translation/inversion gives
J A J=eta A^-1 with eta^4=1. The primitive Weil commutator with the other
translation makes all four eigenspaces of A one-dimensional. If eta were
a primitive fourth root, J would interchange these eigenspaces with no
fixed one, forcing trace(J)=0, contrary to trace(J)=2. Thus eta is +1 or -1.
Multiplying A by a fourth root epsilon with epsilon^2*eta=1 fixes symmetry
without changing A^4=I. This proves compatible normalizations exist and are
found among the enumerated quartic roots. Repeat for B. The code verifies
symmetry explicitly. If the declared field lacks a required root, it fails
rather than silently choosing a different model.

The controls need no extra extension. A general adapter can always start
with the earlier F_(q^12) field and perform this normalization in F_(q^48),
using specified embeddings and retaining the original torsion points. This
is still fixed-degree preprocessing with scalar Frobenius; the adapter
itself has not been implemented in the local FLINT prototype.

Verify A B A^-1 B^-1=zeta I with zeta^2=-1. Choose a nonzero eigenvector v0
of A of eigenvalue one and let vj=B^j v0 for j=0,1,2,3. The columns form an
invertible V, with V^-1 A V=diag(1,zeta,zeta^2,zeta^3) and V^-1 B V the cyclic
shift. Since J fixes the one-dimensional first eigenspace up to sign, its
matrix in this basis is plus or minus index reversal. Its trace is two, so
the sign is plus in characteristic greater than three. Verify this exactly.

Thus theta(P)=V^-1 r(P) is the signed symmetric level-four theta embedding.
This is the Schrödinger-basis characterization of a theta structure, not
an arbitrary projective change of coordinates called theta by convention.
The argument explicitly COMPUTES the basis from the curve and verifies its
identities, rather than using theta-structure existence as a conversion call.

The relevant primary interface is Definition 6.1, Proposition 6.3 and
Lemma 6.17 of [Corte-Real Santos, Piasecki and Wesolowski](https://eprint.iacr.org/2026/1142),
retained PDF pages 24-27 and 33. The paper's representation theorem alone
was not the missing input algorithm. The construction above supplies it in
genus one; no attribution of novelty is made.

## 5. Point Conversion And Model Checks

Compute theta null t=V^-1 r(O), normalize by its first nonzero coordinate,
and use the SAME V for all points. The controls verify t1=t3 and

    2*t1^4=t0*t2*(t0^2+t2^2).

The elliptic theta equations are

    t1^2*(X0^2+X2^2)=(t0^2+t2^2)*X1*X3,
    t1^2*(X1^2+X3^2)=(t0^2+t2^2)*X0*X2.

The inverse uses r=V*theta, recovers x=r1/r0,y=r2/r0 away from O, and checks
both original quadrics. These are genuine degree-one coordinate conversions.
There is no sign recovery oracle, scalar ambiguity or point search. Over an
auxiliary extension, apply the specified embedding to V's base coefficients;
do not choose a fresh theta structure independently for each point or level.

Products use the published product representation and its Segre coordinates.
Known endomorphism evaluators can be applied on original curve points and
then converted. They need not first become theta morphism programs just to
produce the paid small-level action transcript.

## Executed Controls And Limitations

Actual curves over F_(p^2): (p,a,b)=(7,1,0),(23,1,2),(31,1,0). Hasse-invariant
checks verify supersingularity. The p=23 curve has j neither 0 nor 1728.
For each: 64 torsion points constructed, both translations symbolically
verified, symmetric Heisenberg identities and theta equations checked, and
all 64 signed encodings distinct with exact inverse round trips. Additional
points outside E[8] are checked for p=23 and 31. Corrupted matrices, singular
curves, invalid points and inadequate fields are rejected.

An initial run exposed a binding hazard: fq_default(0) has Python truth value
True in this installed FLINT version. A pivot test attempted inversion of
zero and aborted the process. All field-zero tests now use equality to zero;
regression tests cover the failure. This was an implementation defect, not
evidence against the geometric construction.

Only genus-one conversion executed. No complete PPAV quotient/canonicalization
backend, coherent circuit, reference-order construction, or speedup did.
The uniform-source composition is a separate written argument in
UNIFORM_SOURCE_CLOCK.md, dependent on the imported geometric model theorem.
