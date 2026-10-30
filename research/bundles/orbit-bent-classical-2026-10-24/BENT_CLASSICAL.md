# A Classical Perfect Solver For The Coordinate Bent Extension

2026-10-24. LOCAL UNREVIEWED PROOF with native classical witnesses.
This is a falsifier for a natural proposed extension of the existing orbit
candidate, not a new candidate, a toy-oracle separation, or a claim about
all bent functions. It does NOT solve the anisotropic cubic-orbit problem.

## Question And Decision

The preceding pass extends the EXISTING cubic-orbit source to a high-rate
perfect-search guarantee using source truncation. Its general rank law
needs uniform free Fourier frequencies, not quadraticity itself. A tempting
next step is to use higher-dimensional bent functions for more folded rows
and a sufficient rate approaching1/2. The large Maiorana-McFarland (MM)
family supplies exactly such Fourier laws, with arbitrary nonlinear terms.

Reject the COORDINATE MM version in that perfect-search regime. A classical
randomized linear solve returns a polynomial satisfying EVERY original
halfset, on every fixed promised instance, with one-attempt failure <=M/p.
This includes forward-only permutations: hard inversion does not rescue it.

The existing CUBIC_RS_AFFINE_FLATS module already searches local flats and
solves composed linear systems, with a conditional random-flat rank law.
The present delta is different: a direct low-degree determinant certificate
for every fixed MM input, without a flat search, random-instance assumption,
permutation inverse, or supplied preimage. Do not create a duplicate generic
flat-search subsystem during integration.

## Exact Input And Access

Let m=2k+1, k>=1, and take M disjoint ordered nonzero m-point orbits over
the odd prime field F_p. This guarantees mM<=p-1. The argument actually
works for any disjoint evaluation points with that cardinality. Output ONE
polynomial P of degree<n, using its original point evaluations per block:

    (x_i in F_p^k, y_i in F_p^k, z_i in F_p).

Each public predicate is

    z_i + b_i*(x_i dot pi_i(y_i) + g_i(y_i)) in F_i,

where b_i!=0, pi_i:F_p^k->F_p^k is a PERMUTATION with efficient forward
evaluation, g_i is efficiently evaluable, and F_i is an explicit nonempty
set. Halfsets of size(p-1)/2 are the quantum comparison; the classical
solver needs only one explicit member t_i of each F_i. No restriction on
g's algebraic degree is needed. All table reads, circuit evaluation,
sampling, linear algebra and verification are charged.

The coordinate split is part of the contract. An arbitrary hidden or
block-dependent linear mixing of x and y with the scalar evaluation
coordinates is NOT automatically covered by the determinant proof below.
A mere claim that a function is bent or weakly normal is insufficient.

## Why The Quantum Source Looks Attractive

For f(x,y)=x dot pi(y)+g(y), any v!=0, and free frequencies (u,w),

    p^(-2k) sum_(x,y) exp(2*pi*i*(v*f(x,y)-u dot x-w dot y)/p)
      = p^(-k) exp(2*pi*i*(v*g(y*)-w dot y*)/p),

where y*=pi^(-1)(u/v). This is a proof identity, not a required computational
inverse. Sum over x first: exactly one y survives. The magnitude is p^-k
for every (u,w). Scaling by b merely replaces v by b*v.

For centered h(z+b*f(x,y)), the last Fourier frequency v=0 vanishes,
and each free frequency tuple is uniform conditional on v!=0. Thus it
meets the earlier rank-law premise exactly. A triangular residual-map
source preparation uses forward f, not inversion of pi. The ideal
truncation/guard argument would give perfect search for

    R=n/((2k+1)M) > (k+1)/(2k+1).

This Fourier law is genuine. It does not imply a computational advantage.

## Classical Algorithm

Assume n>=L=(k+1)M. Work with L unknown coefficients, so deg(P)<L<=n.
Choose independent uniform y_i in F_p^k. Evaluate v_i=b_i*pi_i(y_i), and
fix any t_i in F_i. Impose the following L LINEAR equations on P:

    P(a_(i,k+j)) = y_i,j,                       j=0,...,k-1,
    P(a_(i,2k)) + sum_(j<k) v_i,j*P(a_(i,j))
                        = t_i-b_i*g_i(y_i).

If the square coefficient matrix is nonsingular, solve it. Verify all
original point evaluations, all original residuals, and deg(P)<n; return
the coefficients only when verification passes. If singular, count the
attempt as failed and either stop or retry with fresh randomness. The
solver never asks for pi^(-1), a zero of pi, a quantum sample or a witness.

## Determinant Proof And Failure Probability

Let V(a)=(1,a,...,a^(L-1)). The kM fixed rows V(a_(i,k+j)) do not depend
on y; only their right sides do. Each of the M remaining rows is

    V(a_(i,2k)) + sum_j v_i,j V(a_(i,j)).

The determinant Delta(v) is a polynomial of total degree <=M, because
each of these M rows is affine in its own v tuple. Its constant term is
the determinant of the Vandermonde matrix on the kM y points and M last
points. They are all distinct. Hence Delta is NOT the zero polynomial.

Since pi_i is a permutation and b_i!=0, independent uniform y_i induce
independent uniform v_i over F_p^k. Schwartz-Zippel gives

    Pr[singular] <= M/p < 1/(2k+1).

No independence between a matrix and its right side is required:
nonsingularity solves EVERY right side. This is why arbitrary g and
arbitrary fixed F_i do not disturb the result. Zero v is only a formal
nonzero-determinant witness, not a rare event the algorithm waits for.

With T fresh independent attempts, failure is <=(M/p)^T. An uncapped
Las Vegas implementation has expected attempts <=1/(1-M/p). Each
attempt uses kM field draws, M forward pi/g evaluations, O(L^2+MkL)
matrix storage/construction work up to field-exponentiation choices, and
O(L^3) field arithmetic for naive elimination. Field operation bit costs,
public evaluations and final full verification remain part of the cost.
The implementation uses FLINT, not a claimed optimized asymptotic backend.

The theorem needs ideal independent draws. The saved seeded runs are
deterministic finite controls, not certified IID trials and not empirical
estimates of this failure probability. Singular attempts are explicitly
recorded and never converted into SAT or UNSAT conclusions.

## Consequence And Limits

The classical threshold n>=(k+1)M includes the ENTIRE sufficient quantum
perfect-search regime above. For fixed k, adding arbitrary nonlinear g,
an invertible triangular permutation, or a permutation with difficult
inversion does not create a perfect-search advantage in this class.
This is an asymptotic algorithmic comparison, not just a finite failure.

It does not compare approximate scores below that threshold, prove every
MM-related coordinate transformation easy, or classify non-MM bent
functions. In particular x^2-nu*y^2 with nonsquare nu has no nonconstant
accepted affine line and is not the coordinate MM x*pi(y)+g(y) ansatz.
The original anisotropic perfect-search candidate therefore stays open,
with substantial classical and natural-reduction obligations.

The repository's existing low-rate cubic intrinsic baseline438/684 already
exists. Reuse it on high-rate instances before adding another attack engine.
An absence of known MM flats in another function is not evidence of hardness.

## Independent Controls And Prior Art

`bent_classical.py` supplies a concrete public triangular permutation and
cubic g, the forward-only classical algorithm and a separate native Horner
replay. The receipt contains actual polynomial coefficients, public input
seeds and hashes, degree bounds, complete residuals and failed-attempt logs.
These are countercontrols of the extension, not a new benchmark problem.

Tests check exact finite permutation bijectivity; every nonzero-scale
Fourier flatness in small fields; a nonpermutation failure control; a full
49-choice singular census; the zero-image Vandermonde special case; native
perfect witnesses through p941/M188; and strict malformed-input rejection.

The MM construction and bent-function normality are established subjects.
[Meidl and Pirsic](https://link.springer.com/article/10.1007/s12095-017-0259-0)
study p-ary bent normality and examples outside maximal-normality classes.
The paper motivates why flatness must be checked, but is not cited as a
proof of our code-specific determinant claim. This note proves that claim
directly; its novelty has not been checked independently. No additional
reviewer was invoked. The authorized Rees review was a separate proof.

Next: high-rate attacks on the existing anisotropic problem, or a genuine
natural-problem reduction. Do not grow the orbit width using coordinate MM
functions and present the improved quantum rate as research progress.
