# Rejected Low-Degree Norm Transfer

2026-10-23. Exact local deduction and a native-input counterexample.
Not independently reviewed. Not a classical hardness theorem, new quantum
algorithm, or claim that the native inverse-trace problem is unsatisfiable.

## Decision

A tempting transfer of the existing odd-characteristic polynomial-norm
attack does NOT give a universal classical inverse-trace solver. The
particular proposed shortcut is to use a square polynomial codeword and
enforce the local trace tests through ONE low-degree Artin-Schreier lift.
There is a polynomial-factorization certificate against that shortcut.

The fixed native counterexample has n=7, q=128, N=49, K=6, 49 distinct
supplied evaluation points, and all-one targets. It is NOT a new oracle
problem. The code's degree budget is 21, while the certificate forces 24.
An explicit independently checked witness for the SAME input is included:
the existing systematic-root baseline finds it in 44 trials / 3,694 field
draws. This is an exponential baseline succeeding on a small proof control,
not a scalable dequantization or a comparison of quantum runtimes.

## Native Relation And Proposed Shortcut

Over F=F_(2^n), retain exactly

    sum_i alpha_i^j x_i = 0,  0 <= j < K,
    Tr(inv0(x_i)) = b_i,
    N=n^2, K=floor(N/8), inv0(0)=0.

Let F0(X)=product_i (X-alpha_i). For distinct points, the entire kernel
code is

    x_i=P(alpha_i)/F0'(alpha_i),  deg(P)<N-K.

Indeed the Lagrange coefficient identity gives zero parity sums for every
such P; injectivity and dimension N-K give equality with the code. In
characteristic two F0'=D^2 for a unique polynomial D, nonzero at every point.
For odd N its degree is (N-1)/2.

The proposal restricts P=Q^2, with

    deg(Q) <= floor((N-K-1)/2).

For all-one targets Q must be nonzero at every evaluation point. The local
test becomes Tr(D(alpha_i)/Q(alpha_i))=1, since Tr(z^2)=Tr(z).
Fix ANY c in F with absolute trace one. An Artin-Schreier lift at the points
exists precisely when some polynomial U of degree <N satisfies

    U^2 + U Q + c Q^2 = D Q   (mod F0).                 (1)

This pointwise equivalence is not a solver: the joint choice of Q and U
is still unknown. The proposed norm shortcut strengthens (1) to a GLOBAL
polynomial identity, avoiding the modulus. Equivalently D/Q=c+t^2+t with
t=U/Q in F(X).

## Exact Obstruction, Including Repeated Factors

For a nonzero polynomial D, define A(D) as the product, WITH FULL
MULTIPLICITY, of all its irreducible factors of odd degree.

**Lemma.** If Q is nonzero and

    U^2 + UQ + cQ^2 = DQ

as polynomials, with Tr_F/F2(c)=1, then A(D) divides Q. In particular
deg(Q)>=deg(A(D)). This works in every finite binary field; odd n is needed
only to choose the convenient c=1, not for the lemma with general c.

Proof. Let h be an odd-degree irreducible factor of D, with multiplicity m.
In F[X]/(h), the absolute trace of c is deg(h)*Tr(c)=1. Hence
T^2+T+c has no root there, and the binary form a^2+ab+cb^2 vanishes only
when a=b=0. If a=v_h(U) and b=v_h(Q), with v_h(0)=infinity, this gives

    v_h(U^2+UQ+cQ^2)=2*min(a,b).

The identity therefore implies m+b=2*min(a,b)<=2b, so b>=m. Doing this
for every such h proves the assertion. This is why retaining only the
parity of m would give an unnecessarily weak bound. No coprimality
assumption on U and Q is required.

An equivalent primitive norm calculation explains the mechanism. Put
U=h0*u, Q=h0*v, gcd(u,v)=1. The identity implies v divides h0. Writing
h0=k*v gives

    D=k*(u^2+uv+c*v^2), Q=k*v^2, U=k*u*v.

The primitive norm factor cannot have ANY odd-degree irreducible factor:
reduction at such a factor would make both u and v vanish. Thus every
odd-degree primary factor of D stays in k, and hence in Q. This is a
standard quadratic norm obstruction applied to this proposed ansatz;
no general new norm theorem or novelty priority is claimed.

## The Native Certificate

The receipt supplies every point, field polynomial and coefficient. Its
field presentation is F2[z]/(z^7+z+1). For the supplied 49 distinct points,

    deg(D)=24,
    D = h5*h19,

where FLINT verifies irreducibility of h5 and h19, of degrees 5 and 19.
Separate explicit Rabin checks verify X^(128^d)=X modulo each factor and
gcd(h_d,X^128-X)=1; because d=5,19 are prime these certify irreducibility.
The factors multiply exactly to D. Thus A(D)=D and every global lift forces
deg(Q)>=24. But K=6 requires deg(Q)<=floor(42/2)=21.

There is also a pointwise, low-degree consequence: if deg(U)<=24 and
deg(Q)<=21, the residual in (1) has degree at most 48. A residual divisible
by F0, of degree 49, must therefore vanish identically. The global lemma
then gives a contradiction. Hence no such low-degree U exists for ANY
admissible Q or ANY constant trace-one c on this input.

This does NOT exclude higher-degree U, a non-square P, a nonconstant c,
other parameterizations, or arbitrary classical algorithms. A valid native
witness is included precisely to prevent confusing failure of this
parameterization with infeasibility of the search relation.

The points were found on draw eight of a capped 100-draw exploration using
Python Random(20261023), sampling 49 elements without replacement from the
128-element field. The retained certificate uses fixed points and does not
rerun that exploration or interpret its frequency as an asymptotic result.

## Self-Attack And Research Decision

- **Pointwise is not global.** Equation (1) always admits sufficiently
  high-degree U when a suitable square-polynomial witness exists. Dropping
  its modulus is the restrictive step. A test contains a nonzero multiple
  of F0 that vanishes at every evaluation point.
- **The code restriction matters.** Restricting P to squares of low-degree
  polynomials is not an innocuous change of coordinates on the full code.
  No conclusion about all native witnesses follows.
- **The constant matters.** c must have trace one; trace-zero c makes the
  residue form split and invalidates the obstruction.
- **Even-degree factors remain available.** Their residue fields split the
  quadratic extension. Positive exact controls exercise norm constructions
  supported there and check local trace identities, including common factors.
- **There is no hardness claim.** Failure of this particular transfer does
  not strengthen the unproved classical hardness of the native problem.

Do not launch a factor-orientation seed campaign around this shortcut. To
revive it, supply a constructive method for the MODULAR identity (1) beyond
the degree guard, or an actually adequate different polynomial codeword
family. That is still the coupled nonlinear task, not a removed blocker.

## Other Routes Checked In This Pass

The newer [DQI Gibbs-sampling paper, Appendix B](https://arxiv.org/html/2609.40345v1)
uses retained linear constraints and Gaussian elimination. It does not
provide the missing nonlinear conditional sampler here. The repository's
`CLASSICAL_SAMPLING.md` already supplies the native latent-constraint
specialization and its rare-witness limitation. No duplicate was implemented.

The generic surface chirp receiver, the orthogonal rank-dependent comparison,
and their primary-source links were rechecked. No new covering theorem,
fatal proof gap, or novelty conclusion was established. This rechecking is
NOT a new research result. The Frobenius residual reduction from the prior
pass remains separate; this pass does not extend it.
